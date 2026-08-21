#!/usr/bin/env python3
"""
cgMLST layer: QC, concordance with the v4c units, and attribution scoring.

Input is chewBBACA's `results_alleles.tsv` (2,976 genomes x 4,089 loci) against
the PubMLST B. pseudomallei cgMLST scheme.

Three questions, in order of what they buy us:

1. QC -- what fraction of loci were actually called per genome? chewBBACA emits
   non-numeric tokens (LNF, PLOT3, PLOT5, NIPH, NIPHEM, ALM, ASM, LOTSC, PAMA)
   for loci it could not resolve cleanly. Those are missing data, not alleles,
   and treating them as a shared state would invent similarity the way the
   literal string "unknown" did in the BioProject column.

2. Concordance -- do cgMLST allelic distances agree with our recombination-
   filtered core SNP distances within units? This is the orthogonal-typing check
   both external reviews asked for.

3. Attribution -- does the extra resolution of 4,089 loci rescue country-level
   attribution where 7-locus MLST and core SNPs both failed? Same leave-group-out
   regime, so the numbers are directly comparable.

Pairwise distance is computed only where needed rather than as a full
2,976^2 matrix: allelic distance over loci called in BOTH genomes, normalised by
that count so genomes with different call rates stay comparable.
"""
import argparse
import collections
import csv
import glob
import os
import sys

import numpy as np

B = os.path.dirname(os.path.abspath(__file__))
MISSING_TOKENS = ("LNF", "PLOT", "NIPH", "ALM", "ASM", "LOTSC", "PAMA", "INF-")


def load_profiles(path):
    """-> (samples, loci, matrix int32 with -1 for uncalled).

    chewBBACA writes inferred alleles as 'INF-123'. Those ARE calls -- strip the
    prefix and keep the number. Everything else non-numeric is missing.
    """
    with open(path) as fh:
        hdr = fh.readline().rstrip("\n").split("\t")
        loci = hdr[1:]
        samples, rows = [], []
        for line in fh:
            f = line.rstrip("\n").split("\t")
            samples.append(f[0].replace(".fasta", ""))
            row = np.full(len(loci), -1, dtype=np.int32)
            for j, v in enumerate(f[1:]):
                if v.startswith("INF-"):
                    v = v[4:]
                if v.isdigit():
                    row[j] = int(v)
            rows.append(row)
    return samples, loci, np.vstack(rows)


def dist_one_vs_all(mat, i, idx):
    """Normalised allelic distance from row i to rows idx, over co-called loci."""
    a = mat[i]
    b = mat[idx]
    both = (a >= 0) & (b >= 0)
    n = both.sum(axis=1)
    diff = ((a != b) & both).sum(axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        d = np.where(n > 0, diff / np.maximum(n, 1), np.nan)
    return d, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profiles", default=f"{B}/cgmlst_results/results_alleles.tsv")
    ap.add_argument("--out-prefix", default=f"{B}/CGMLST")
    ap.add_argument("--min-call-rate", type=float, default=0.90)
    a = ap.parse_args()

    samples, loci, mat = load_profiles(a.profiles)
    idx_of = {s: i for i, s in enumerate(samples)}
    called = (mat >= 0).sum(axis=1)
    rate = called / len(loci)
    print(f"genomes {len(samples)}   loci {len(loci)}")
    print(f"call rate: median {np.median(rate):.3f}  mean {rate.mean():.3f}  "
          f"min {rate.min():.3f}")
    for t in (0.95, 0.90, 0.80):
        print(f"  >= {t:.0%} of loci called: {(rate >= t).sum()} genomes "
              f"({100*(rate>=t).mean():.1f}%)")

    meta = {r["sample_id"]: r for r in
            csv.DictReader(open(f"{B}/L1v4c_MERGED_METADATA.tsv"), delimiter="\t")}
    scales = {}
    for s, p in (("country", "assign_country_norm"), ("region", "assign_region")):
        scales[s] = {r["sample_id"]: r["country"].strip()
                     for r in csv.DictReader(open(f"{B}/{p}.tsv"), delimiter="\t")
                     if r["country"].strip().lower() not in
                     ("", "unknown", "na", "n/a", "none", "null", "missing", "-", ".")}

    with open(f"{a.out_prefix}_QC.tsv", "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["sample_id", "loci_called", "call_rate", "unit", "role", "country"])
        for s in samples:
            m = meta.get(s, {})
            w.writerow([s, int(called[idx_of[s]]), f"{rate[idx_of[s]]:.4f}",
                        m.get("subcluster", ""), m.get("role", ""), m.get("country", "")])
    print(f"\nwrote {a.out_prefix}_QC.tsv")

    # ---- 2. concordance: cgMLST distance vs recombination-filtered SNP distance
    print("\n=== concordance with recombination-filtered core SNP distances ===")
    rows = []
    for f in sorted(glob.glob(f"{B}/DISTANCES_v4c/*_1.filtered_pertaxon.tsv")):
        unit = os.path.basename(f).split("__")[0]
        r = list(csv.reader(open(f), delimiter="\t"))
        taxa = [t for t in r[0][1:] if t in idx_of]
        if len(taxa) < 5:
            continue
        pos = {t: k for k, t in enumerate(r[0][1:])}
        snp, cg = [], []
        for x in range(len(taxa)):
            i = idx_of[taxa[x]]
            others = [idx_of[t] for t in taxa[x + 1:]]
            if not others:
                continue
            d, n = dist_one_vs_all(mat, i, others)
            for y, t in enumerate(taxa[x + 1:]):
                if np.isnan(d[y]):
                    continue
                snp.append(int(r[pos[taxa[x]] + 1][pos[t] + 1]))
                cg.append(d[y])
        if len(snp) < 10:
            continue
        c = np.corrcoef(snp, cg)[0, 1]
        rows.append((unit, len(taxa), len(snp), c))
    rows.sort(key=lambda t: -t[3] if not np.isnan(t[3]) else 0)
    good = [r for r in rows if not np.isnan(r[3])]
    print(f"  units compared: {len(good)}")
    if good:
        cs = [r[3] for r in good]
        print(f"  Pearson r (cgMLST allelic vs filtered SNP), per unit:")
        print(f"    median {np.median(cs):+.3f}   range {min(cs):+.3f} to {max(cs):+.3f}")
        print(f"    units with r >= 0.7: {sum(1 for c in cs if c >= 0.7)} of {len(cs)}")
    with open(f"{a.out_prefix}_CONCORDANCE.tsv", "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["unit", "n_taxa", "n_pairs", "pearson_r_cgmlst_vs_filtered_snp"])
        for u, n, p, c in rows:
            w.writerow([u, n, p, f"{c:.4f}" if not np.isnan(c) else ""])
    print(f"  wrote {a.out_prefix}_CONCORDANCE.tsv")

    # ---- 3. attribution, same leave-group-out regime as the core-genome test --
    print("\n=== attribution by nearest cgMLST neighbour (leave-group-out) ===")
    val = [s for s, r in meta.items()
           if r.get("origin_basis") == "travel_reattributed" and s in idx_of]
    truth_c = {s: (meta[s].get("acquired_from") or meta[s].get("country")) for s in val}
    n_val = sum(1 for r in meta.values()
                if r.get("origin_basis") == "travel_reattributed")
    print(f"  validation genomes with a cgMLST profile: {len(val)} of {n_val}")

    out = []
    for scale, lab in scales.items():
        hit = tot = unatt = 0
        for s in val:
            held = {x for x in val if truth_c[x] == truth_c[s]}
            pool = [idx_of[t] for t in samples
                    if t not in held and lab.get(t) and t != s]
            if not pool or not lab.get(s):
                unatt += 1
                continue
            d, n = dist_one_vs_all(mat, idx_of[s], pool)
            ok = ~np.isnan(d)
            if not ok.any():
                unatt += 1
                continue
            pred = lab[samples[pool[int(np.nanargmin(d))]]]
            tot += 1
            hit += (pred == lab[s])
            out.append({"sample_id": s, "scale": scale, "truth": lab[s],
                        "predicted": pred, "correct": int(pred == lab[s]),
                        "nn_distance": f"{np.nanmin(d):.5f}",
                        "exposure_country": truth_c[s]})
        print(f"  {scale:<9} {hit}/{tot} correct   ({unatt} unattributable)")

    with open(f"{a.out_prefix}_ATTRIBUTION.tsv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["sample_id", "scale", "exposure_country",
                                           "truth", "predicted", "correct",
                                           "nn_distance"],
                           delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(out)
    print(f"  wrote {a.out_prefix}_ATTRIBUTION.tsv")


if __name__ == "__main__":
    main()
