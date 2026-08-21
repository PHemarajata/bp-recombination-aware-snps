#!/usr/bin/env python3
"""
PRE-REGISTERED controls for the accessory-attribution experiment.

Written and committed BEFORE the accessory attribution result was computed, per
HANDOFF 2026-08-21 evening §1.2: "Do not skip and do not run it after the fact."
Check `git log` on this file against accessory_bp/ATTR_ACCESSORY.tsv's mtime.

WHY. Assembly fragmentation causes apparent gene absence. On the 57 QC'd genomes
that showed up as contigs vs cgMLST call rate rho = -0.642 (p = 7.5e-08). For
core genes a missing call costs a few points of call rate and is survivable.
For accessory presence/absence, ABSENCE IS THE SIGNAL, so the same effect is
fatal. And it is confounded in the worst possible direction: assembly quality
tracks sequencing centre, which tracks country. An uncontrolled accessory
analysis can recover a signal about who did the sequencing and report it as
geography.

THE FOUR CONTROLS, as specified:

  1. Stratify by contig count. Tertiles of the panel; score attribution within
     each. If accuracy tracks assembly quality rather than geography it shows
     up as accuracy varying across strata.
  2. Regress accessory distance on contig-count difference. Per pair, does
     |contigs_A - contigs_B| predict accessory distance? Also the per-genome
     form, which is the more interpretable one: does a genome's MEAN accessory
     distance to everything else track its own contig count? A fragmented
     genome that is "far" from everything is measuring its own assembly.
  3. Permutation null within contig-count strata. Shuffle country labels inside
     each stratum, keeping assembly quality fixed. If accuracy survives the
     signal is geographic; if it collapses to the permuted distribution it was
     a batch effect.
  4. Distance stratification, as for core. If accessory scores BETTER where no
     close relative exists, it is the same attractor artifact as region (§3.3),
     not attribution. Stratified on the CORE distance, because "does a genuine
     close relative exist" is a fact about ancestry, not about accessory
     content -- and the accessory scale is not comparable to the cgMLST one.

Passing means: accuracy is flat across contig strata, contig difference explains
little of accessory distance, the real accuracy sits outside the permutation
null, and accuracy is not concentrated in the no-relative stratum.
"""
import argparse
import csv
import os
import sys
from collections import Counter, defaultdict

import numpy as np
from scipy import stats

B = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, B)
from score_accessory_bp import (CondensedDist, ESTIMATORS, NOTC, build_labels,  # noqa: E402
                                load_drops, load_pp_dists, score)

N_PERM = 1000
SEED = 20260821  # fixed: the date, so the null is reproducible and not shopped


def load_assembly_stats(path):
    return {r["sample_id"]: {k: (int(v) if k in ("contigs", "total_bp", "n50",
                                                 "longest_contig",
                                                 "ambiguous_bases")
                                 else float(v) if k == "gc" else v)
                             for k, v in r.items()}
            for r in csv.DictReader(open(path), delimiter="\t")}


def control_1_strata(samples, dist_row, labels, truth_c, val, contigs, panel_counts):
    """Accuracy within contig-count tertiles of the PANEL (the pool), with the
    validation genomes' own stratum reported too."""
    print("\n" + "=" * 72)
    print("CONTROL 1 — attribution accuracy within contig-count strata")
    print("=" * 72)
    c = np.array([contigs.get(s, np.nan) for s in samples], dtype=float)
    ok = np.isfinite(c)
    q1, q2 = np.nanquantile(c[ok], [1 / 3, 2 / 3])
    print(f"panel contig tertiles: <= {q1:.0f} | {q1:.0f}-{q2:.0f} | > {q2:.0f}")

    def stratum(x):
        return 0 if x <= q1 else (1 if x <= q2 else 2)

    names = ["low (best assemblies)", "mid", "high (most fragmented)"]
    # (a) restrict the POOL to one stratum at a time: does the answer depend on
    #     which assemblies are available to match against?
    for si, nm in enumerate(names):
        keep = [i for i, s in enumerate(samples)
                if np.isfinite(contigs.get(s, np.nan))
                and stratum(contigs[s]) == si]
        keepset = {samples[i] for i in keep}
        sub_lab = {sc: {k: v for k, v in lab.items()
                        if k in keepset or k in set(val)}
                   for sc, lab in labels.items()}
        sub_samples = [s for s in samples if s in keepset or s in set(val)]
        idx = {s: i for i, s in enumerate(samples)}
        remap = np.array([idx[s] for s in sub_samples])
        rows = score(sub_samples,
                     lambda i, _r=remap: dist_row(int(_r[i]))[_r],
                     sub_lab, truth_c, [s for s in val if s in sub_samples],
                     panel_counts)
        line = []
        for sc in labels:
            rs = [r for r in rows if r["scale"] == sc]
            if rs:
                h = sum(r["ok_nearest_neighbour"] for r in rs)
                line.append(f"{sc} {h}/{len(rs)} ({100*h/len(rs):.0f}%)")
        print(f"  pool = {nm:<24}n_pool={len(keep):<5} " + "   ".join(line))

    # (b) split the VALIDATION genomes by their own contig count
    print("\n  validation genomes split by their OWN assembly quality:")
    return q1, q2, stratum


def control_1b_by_query(rows, contigs, q1, q2):
    for sc in ("country", "region"):
        rs = [r for r in rows if r["scale"] == sc]
        if not rs:
            continue
        buckets = defaultdict(lambda: [0, 0])
        for r in rs:
            n = contigs.get(r["sample_id"])
            if n is None:
                continue
            b = "low" if n <= q1 else ("mid" if n <= q2 else "high")
            buckets[b][0] += int(r["ok_nearest_neighbour"])
            buckets[b][1] += 1
        parts = [f"{b} {v[0]}/{v[1]}" for b, v in
                 sorted(buckets.items(), key=lambda x: ["low", "mid", "high"].index(x[0]))]
        print(f"     {sc:<8}" + "   ".join(parts))


def control_2_regression(samples, vec_acc, vec_core, n_all, keep, contigs):
    print("\n" + "=" * 72)
    print("CONTROL 2 — does contig count predict accessory distance?")
    print("=" * 72)
    c = np.array([contigs.get(s, np.nan) for s in samples], dtype=float)
    cd_a = CondensedDist(vec_acc, n_all)
    cd_c = CondensedDist(vec_core, n_all)

    # per-genome form: mean distance to everything else vs own contig count
    ma = np.array([np.nanmean(cd_a.row(int(keep[i]))[keep]) for i in range(len(samples))])
    mc = np.array([np.nanmean(cd_c.row(int(keep[i]))[keep]) for i in range(len(samples))])
    good = np.isfinite(c) & np.isfinite(ma)
    ra, pa = stats.spearmanr(c[good], ma[good])
    rc, pc = stats.spearmanr(c[good], mc[good])
    print(f"  per-genome, n={good.sum()}")
    print(f"    contigs vs MEAN ACCESSORY distance : rho = {ra:+.3f}  p = {pa:.3g}")
    print(f"    contigs vs MEAN CORE distance      : rho = {rc:+.3f}  p = {pc:.3g}")
    print("    (core is the internal control: it should be much weaker, because"
          " a\n     missing contig costs core distance far less than it costs"
          " accessory)")

    # pairwise form, on a random sample of pairs (all 4.6M is unnecessary)
    rng = np.random.default_rng(SEED)
    m = len(samples)
    npair = 400_000
    ii = rng.integers(0, m, npair)
    jj = rng.integers(0, m, npair)
    sel = ii != jj
    ii, jj = ii[sel], jj[sel]
    da = np.array([cd_a.row(int(keep[i]))[int(keep[j])] for i, j in zip(ii, jj)])
    dc = np.array([cd_c.row(int(keep[i]))[int(keep[j])] for i, j in zip(ii, jj)])
    dcontig = np.abs(c[ii] - c[jj])
    scontig = c[ii] + c[jj]
    g = np.isfinite(da) & np.isfinite(dcontig)
    print(f"  pairwise, n={g.sum()} random pairs")
    for nm, x, y in (("|contigs_A - contigs_B| vs accessory d", dcontig, da),
                     ("contigs_A + contigs_B  vs accessory d", scontig, da),
                     ("|contigs_A - contigs_B| vs core d", dcontig, dc)):
        r, p = stats.spearmanr(x[g], y[g])
        print(f"    {nm:<40} rho = {r:+.3f}  p = {p:.3g}")
    return ma, mc


def control_3_permutation(samples, dist_row, labels, truth_c, val, contigs,
                          panel_counts, q1, q2, real_rows):
    print("\n" + "=" * 72)
    print(f"CONTROL 3 — permutation null, labels shuffled WITHIN contig strata "
          f"({N_PERM} perms)")
    print("=" * 72)
    rng = np.random.default_rng(SEED)

    def stratum(s):
        n = contigs.get(s)
        if n is None:
            return -1
        return 0 if n <= q1 else (1 if n <= q2 else 2)

    for sc in ("country", "region"):
        lab = labels[sc]
        real = [r for r in real_rows if r["scale"] == sc]
        if not real:
            continue
        real_acc = sum(r["ok_nearest_neighbour"] for r in real) / len(real)

        # pool members by stratum, so the shuffle preserves assembly quality
        by_str = defaultdict(list)
        for s in samples:
            if lab.get(s):
                by_str[stratum(s)].append(s)

        null = []
        for _ in range(N_PERM):
            perm = dict(lab)
            for st_, mem in by_str.items():
                vals = [lab[s] for s in mem]
                rng.shuffle(vals)
                for s, v in zip(mem, vals):
                    perm[s] = v
            for s in val:                       # truth of the query is untouched
                perm[s] = lab[s]
            rows = score(samples, dist_row, {sc: perm}, truth_c, val, panel_counts)
            if rows:
                null.append(sum(r["ok_nearest_neighbour"] for r in rows) / len(rows))
        null = np.array(null)
        p = (np.sum(null >= real_acc) + 1) / (len(null) + 1)
        print(f"  {sc:<8} real {100*real_acc:5.1f}%   "
              f"null mean {100*null.mean():5.1f}%  "
              f"95th pct {100*np.quantile(null,0.95):5.1f}%   "
              f"p = {p:.4f}")


def control_4_strata(acc_rows, core_nn, contigs):
    print("\n" + "=" * 72)
    print("CONTROL 4 — accuracy by whether a genuine close relative exists")
    print("=" * 72)
    print("  stratified on the CORE cgMLST nearest-neighbour distance, so the")
    print("  strata mean the same thing they mean for the core-genome result.")
    for sc in ("country", "region"):
        rs = [r for r in acc_rows if r["scale"] == sc]
        if not rs:
            continue
        print(f"  {sc}:")
        for lo, hi, nm in ((0, .05, "d_core < 0.05  (close relative)"),
                           (.05, .30, "d_core 0.05-0.30 (distant)"),
                           (.30, 9e9, "d_core >= 0.30 (no real relative)")):
            sub = [r for r in rs
                   if r["sample_id"] in core_nn
                   and lo <= core_nn[r["sample_id"]] < hi]
            if sub:
                h = sum(int(r["ok_nearest_neighbour"]) for r in sub)
                print(f"     {nm:<36}{h}/{len(sub)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ppdb", default=f"{B}/accessory_bp/ppdb3033/ppdb3033")
    ap.add_argument("--stats", default=f"{B}/accessory_bp/ASSEMBLY_STATS_3033.tsv")
    ap.add_argument("--manifest", default=f"{B}/cgmlst_lichtenegger/MANIFEST.tsv")
    ap.add_argument("--core-ref", default=f"{B}/CGMLST_LICHT_ATTRIBUTION.tsv",
                    help="core cgMLST result, for the control-4 strata")
    ap.add_argument("--skip-perm", action="store_true")
    a = ap.parse_args()

    stats_ = load_assembly_stats(a.stats)
    contigs = {k: v["contigs"] for k, v in stats_.items()}
    drop = load_drops()
    names, core, acc = load_pp_dists(a.ppdb)
    keep = np.array([i for i, s in enumerate(names) if s not in drop])
    samples = [names[i] for i in keep]
    cd = CondensedDist(acc, len(names))
    cache = {}

    def dist_row(i, _cache=cache):
        r = _cache.get(i)
        if r is None:
            r = cd.row(int(keep[i]))[keep]
            _cache[i] = r
        return r

    country, region, truth_c, is_val = build_labels(samples, a.manifest)
    labels = {"country": country, "region": region}
    val = [s for s in samples if is_val.get(s)]
    panel_counts = {sc: Counter(lab[x] for x in samples if lab.get(x))
                    for sc, lab in labels.items()}
    print(f"panel {len(samples)} genomes, {len(val)} validation genomes")
    missing = [s for s in samples if s not in contigs]
    if missing:
        print(f"WARNING: {len(missing)} genomes without assembly stats")

    real_rows = score(samples, dist_row, labels, truth_c, val, panel_counts)

    q1, q2, _ = control_1_strata(samples, dist_row, labels, truth_c, val,
                                 contigs, panel_counts)
    control_1b_by_query(real_rows, contigs, q1, q2)
    control_2_regression(samples, acc, core, len(names), keep, contigs)
    if not a.skip_perm:
        control_3_permutation(samples, dist_row, labels, truth_c, val, contigs,
                              panel_counts, q1, q2, real_rows)
    core_nn = {}
    if os.path.exists(a.core_ref):
        for r in csv.DictReader(open(a.core_ref), delimiter="\t"):
            if r["scale"] == "country":
                core_nn[r["sample_id"]] = float(r["nn_distance"])
    control_4_strata(real_rows, core_nn, contigs)


if __name__ == "__main__":
    main()
