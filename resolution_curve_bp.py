#!/usr/bin/env python3
"""
Attribution accuracy as a function of how many loci you type.

Motivation
----------
We already have three points -- 7-locus MLST, 4,089-locus cgMLST, and
whole-genome SNPs -- all scoring zero at country level. A reviewer can still ask
whether the answer is peculiar to those three schemes.

Published two-locus schemes make the opposite claim: the PBP dual-locus scheme
(McLaughlin, Gulvik & Sue 2022, doi:10.1371/journal.pntd.0009882) reports that
"several STs were unique to strains originating from a specific country or
region" from just 11 SNPs in two genes.

Rather than reimplement one more fixed scheme, subsample k loci at random from
the cgMLST profile and sweep k. That turns three points into a curve and asks
the general question: **does attribution accuracy depend on typing resolution at
all?**

Important caveat on interpretation
----------------------------------
Random loci are a LOWER BOUND for a curated scheme of the same size. DLST's two
loci were *chosen* for geographic signal; two random loci were not. So if the
curve is flat at zero, that does not by itself refute a curated small scheme --
it shows that resolution alone does not buy country-level attribution, which is
a different and weaker claim. Say it that way.

Method is identical to the main attribution scorer so numbers are comparable:
nearest neighbour by allelic distance over co-called loci, leave-group-out
(every validation genome sharing the target's exposure country is removed),
scored against the majority-class baseline.

Usage:  resolution_curve_bp.py [--reps 10] [--out FILE]
"""
import argparse
import collections
import csv
import os
import sys

import numpy as np

B = os.path.dirname(os.path.abspath(__file__))
MISSING = {"", "unknown", "na", "n/a", "none", "null", "missing", "-", "."}
K_GRID = [2, 3, 5, 7, 10, 20, 50, 100, 250, 500, 1000, 2000, 4089]


def load_profiles(path):
    with open(path) as fh:
        hdr = fh.readline().rstrip("\n").split("\t")
        n_loci = len(hdr) - 1
        samples, rows = [], []
        for line in fh:
            f = line.rstrip("\n").split("\t")
            samples.append(f[0].replace(".fasta", ""))
            row = np.full(n_loci, -1, dtype=np.int32)
            for j, v in enumerate(f[1:]):
                if v.startswith("INF-"):
                    v = v[4:]
                if v.isdigit():
                    row[j] = int(v)
            rows.append(row)
    return samples, np.vstack(rows)


def clean(v):
    v = (v or "").strip()
    return "" if v.lower() in MISSING else v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profiles", default=f"{B}/cgmlst_results/results_alleles.tsv")
    ap.add_argument("--reps", type=int, default=10)
    ap.add_argument("--seed", type=int, default=20260821)
    ap.add_argument("--out", default=f"{B}/RESOLUTION_CURVE.tsv")
    a = ap.parse_args()

    samples, mat = load_profiles(a.profiles)
    idx = {s: i for i, s in enumerate(samples)}
    meta = {r["sample_id"]: r for r in
            csv.DictReader(open(f"{B}/L1v4c_MERGED_METADATA.tsv"), delimiter="\t")}
    scales = {}
    for s, p in (("country", "assign_country_norm"), ("region", "assign_region")):
        scales[s] = {r["sample_id"]: clean(r["country"])
                     for r in csv.DictReader(open(f"{B}/{p}.tsv"), delimiter="\t")}

    val = [s for s, r in meta.items()
           if r.get("origin_basis") == "travel_reattributed" and s in idx]
    truth_c = {s: (clean(meta[s].get("acquired_from")) or clean(meta[s].get("country")))
               for s in val}
    print(f"genomes {len(samples)}  loci {mat.shape[1]}  validation {len(val)}")

    rng = np.random.default_rng(a.seed)
    out = []
    for scale, lab in scales.items():
        # majority-class baseline on the scorable set
        panel = collections.Counter(lab[t] for t in samples if lab.get(t))
        top = panel.most_common(1)[0][0]
        base_hits = sum(1 for s in val if lab.get(s) == top)
        base_n = sum(1 for s in val if lab.get(s))
        print(f"\n=== {scale} ===  baseline (always '{top}'): "
              f"{base_hits}/{base_n} = {100*base_hits/max(base_n,1):.0f}%")
        print(f"{'loci':>6}  {'accuracy (mean over reps)':<28} {'scorable':>9}")
        for k in K_GRID:
            if k > mat.shape[1]:
                continue
            accs = []
            reps = 1 if k == mat.shape[1] else a.reps   # full set has no variation
            for _ in range(reps):
                cols = (np.arange(mat.shape[1]) if k == mat.shape[1]
                        else rng.choice(mat.shape[1], size=k, replace=False))
                sub = mat[:, cols]
                hit = tot = 0
                for s in val:
                    held = {x for x in val if truth_c[x] == truth_c[s]}
                    pool = [idx[t] for t in samples
                            if t not in held and t != s and lab.get(t)]
                    if not pool or not lab.get(s):
                        continue
                    q = sub[idx[s]]
                    P = sub[pool]
                    both = (q >= 0) & (P >= 0)
                    n = both.sum(axis=1)
                    diff = ((q != P) & both).sum(axis=1)
                    ok = n > 0
                    if not ok.any():
                        continue
                    d = np.where(ok, diff / np.maximum(n, 1), np.inf)
                    pred = lab[samples[pool[int(np.argmin(d))]]]
                    tot += 1
                    hit += (pred == lab[s])
                if tot:
                    accs.append(hit / tot)
            if not accs:
                continue
            m, sd = float(np.mean(accs)), float(np.std(accs))
            print(f"{k:>6}  {100*m:>5.1f}% +/- {100*sd:<4.1f}"
                  f"{'  (' + str(reps) + ' reps)':<14} {tot:>9}")
            out.append({"scale": scale, "n_loci": k, "reps": reps,
                        "mean_accuracy": f"{m:.4f}", "sd": f"{sd:.4f}",
                        "n_scorable": tot,
                        "baseline": f"{base_hits/max(base_n,1):.4f}"})

    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]), delimiter="\t",
                           lineterminator="\n")
        w.writeheader(); w.writerows(out)
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
