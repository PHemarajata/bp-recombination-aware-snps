#!/usr/bin/env python3
"""
Gate 1 diversity from ALIGNMENT-derived distances instead of the Mash proxy.

Closes weak spot W3 of MANUSCRIPT_OUTLINE_2026-08-21.md.

THE PROBLEM. Gate 1 (METHODS_DRAFT §2.6.1) requires units to fall in
~1,270-4,671 **mean pairwise core SNPs, calibrated in `ska distance` units**.
But membership has been decided from `trackA_diversity_*.tsv`, whose
`approx_mean_snps` is `mash_distance x 3,805,619` -- a conversion whose own
docstring calls itself triage-grade, in a different unit system from the
calibration, and the project records sketching mis-scaling against
alignment-derived distances by 0.88x-91x depending on the cluster.

That gate is not cosmetic: it decides which units enter the headline r/m median
at all. The entire 7.38-vs-7.26 discrepancy resolved on 2026-08-21 came down to
ONE unit's position relative to this window. A mis-specified window has already
moved that number once.

THE FIX. `DISTANCES_v4c_SUMMARY.tsv` carries `raw_mean` -- the mean pairwise SNP
distance computed directly on each unit's core alignment, per replicon. That is
a SNP count, the same kind of quantity the window is calibrated in, rather than
a rescaled sketch divergence.

  genome-wide mean pairwise core SNPs = raw_mean(replicon 1) + raw_mean(replicon 2)

Summed, because the two replicons are two parts of one genome and the original
`ska distance` calibration was whole-genome. `--combine` offers mean and chr1
as sensitivity checks, since that choice is a judgement.

`raw_mean` is used, not `filt_*`: Gate 1 is applied BEFORE trusting Gubbins, so
the relevant diversity is the unfiltered core divergence. Using the
recombination-filtered distance would condition the gate on the very output it
exists to validate.

WHAT THIS DOES AND DOES NOT SETTLE. It replaces a triage-grade sketch proxy with
a directly comparable SNP count, which is much closer to the calibration's units
than Mash is. It does NOT prove identity with `ska distance`: SKA counts SNPs
from split k-mers over whole assemblies, this counts them on a reference-mapped
core alignment, and the two need not agree exactly. The residual risk is a
systematic offset between those two SNP-counting conventions, which is a smaller
and much better-characterised gap than the one it replaces -- but it is not zero,
and the gate's own bracket width (the floor is (405, 1,268], 3.1x wide) probably
dominates it either way.
"""
import argparse
import csv
import os
import statistics as st
from collections import defaultdict

B = os.path.dirname(os.path.abspath(__file__))
# Two metrics, two windows. Keeping one pair of constants for both was a live
# defect: `klass()` fell back to the ska-unit bounds for the ALIGNMENT metric
# too, so running this script with default arguments silently reported 39
# in-window units at median r/m 8.05 instead of the reported 47 at 7.70. It did
# not crash and the wrong number is plausible, which is the dangerous kind. The
# script's own --floor help already said the ska-unit 1270 is too high for the
# alignment metric; nothing enforced it. Same family as E0, E1 and E4.
MASH_FLOOR, MASH_CEIL = 1270.0, 4671.0   # ska-unit bounds, for the Mash proxy
ALN_FLOOR, ALN_CEIL = 700.0, 4700.0      # relocated bounds, for the ALIGNMENT
                                         # metric -- these are the REPORTED ones
FLOOR, CEIL = MASH_FLOOR, MASH_CEIL      # back-compat for klass()'s fallback


def load_alignment_diversity(path, combine):
    per = defaultdict(dict)
    for r in csv.DictReader(open(path), delimiter="\t"):
        try:
            per[r["unit"]][int(r["replicon"])] = float(r["raw_mean"])
        except (KeyError, ValueError):
            continue
    out = {}
    for u, reps in per.items():
        v = [reps[k] for k in sorted(reps)]
        if not v:
            continue
        if combine == "sum":
            out[u] = sum(v)
        elif combine == "mean":
            out[u] = st.mean(v)
        else:                                   # chr1
            out[u] = reps.get(1, v[0])
    return out, {u: len(r) for u, r in per.items()}


def klass(x, floor=None, ceil=None):
    f = FLOOR if floor is None else floor
    c = CEIL if ceil is None else ceil
    return "below" if x < f else ("in" if x <= c else "above")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--distances", default=f"{B}/DISTANCES_v4c_SUMMARY.tsv")
    # E1. This defaulted to trackA_diversity_86units.tsv -- note "86", an older
    # partition than the frozen 85-unit basis. The Mash proxy is secondary here
    # (the alignment-derived window is the reported one, and the proxy misplaced
    # 22 of 85 units), but a default naming a stale partition is exactly the
    # pattern behind E0 and E4. No default: name the file you mean.
    ap.add_argument("--mash", required=True,
                    help="Mash diversity table; must match --distances and --rm")
    ap.add_argument("--rm", default=f"{B}/L1v4c_out/Summaries/recombination_rm.tsv")
    ap.add_argument("--combine", default="sum", choices=["sum", "mean", "chr1"])
    ap.add_argument("--floor", type=float, default=None,
                    help="override the Gate 1 floor for the ALIGNMENT metric "
                         f"(default {700.0:.0f}, the relocated value; the "
                         "ska-unit 1270 applies to the Mash proxy only)")
    ap.add_argument("--ceiling", type=float, default=None,
                    help="override the Gate 1 ceiling for the ALIGNMENT metric "
                         f"(default {4700.0:.0f}, essentially unchanged from "
                         "the ska-unit 4671)")
    ap.add_argument("--out", default=f"{B}/GATE1_ALIGNMENT_2026-08-21.tsv")
    a = ap.parse_args()

    aln, nrep = load_alignment_diversity(a.distances, a.combine)
    mash = {r["cluster_id"]: float(r["approx_mean_snps"])
            for r in csv.DictReader(open(a.mash), delimiter="\t")
            if r.get("approx_mean_snps")}
    rm = {r["unit"]: r for r in csv.DictReader(open(a.rm), delimiter="\t")}

    units = sorted(set(rm) & set(aln))
    print(f"units with both an r/m value and an alignment distance: {len(units)}")
    missing = sorted(set(rm) - set(aln))
    if missing:
        print(f"  no alignment distance for {len(missing)}: {missing[:6]}")
    odd = [u for u in units if nrep.get(u) != 2]
    if odd:
        print(f"  WARNING: not 2 replicons for {len(odd)}: {odd[:6]}")

    rows, moved = [], []
    for u in units:
        A, M = aln[u], mash.get(u)
        ka = klass(A,
                   ALN_FLOOR if a.floor is None else a.floor,
                   ALN_CEIL if a.ceiling is None else a.ceiling)
        km = klass(M) if M is not None else ""
        try:
            v = float(rm[u]["rm_corrected"])
        except ValueError:
            continue
        rows.append({"unit": u, "n": rm[u]["n"],
                     "aln_mean_pairwise_snps": f"{A:.1f}",
                     "mash_approx_mean_snps": f"{M:.0f}" if M is not None else "",
                     "ratio_mash_over_aln": f"{M/A:.3f}" if M and A else "",
                     "gate1_alignment": ka, "gate1_mash": km,
                     "changed": "yes" if km and ka != km else "",
                     "rm_corrected": rm[u]["rm_corrected"]})
        if km and ka != km:
            moved.append((u, rm[u]["n"], M, A, km, ka, v))

    # --- how badly do the two disagree at all? --------------------------------
    both = [(mash[u], aln[u]) for u in units if u in mash and aln[u] > 0]
    ratios = sorted(m / x for m, x in both)
    print(f"\n=== mash proxy vs alignment distance, {len(ratios)} units ===")
    print(f"  ratio mash/alignment: min {ratios[0]:.2f}  median "
          f"{st.median(ratios):.2f}  max {ratios[-1]:.2f}")
    print(f"  units where the proxy is >2x off: "
          f"{sum(1 for r in ratios if r > 2 or r < 0.5)}")

    # --- classification, both ways -------------------------------------------
    print(f"\n=== Gate 1 classification (combine={a.combine}) ===")
    print(f"  {'class':<8}{'MASH proxy':>22}{'ALIGNMENT':>22}")
    for k in ("in", "below", "above"):
        vm = sorted(float(r["rm_corrected"]) for r in rows if r["gate1_mash"] == k)
        va = sorted(float(r["rm_corrected"]) for r in rows
                    if r["gate1_alignment"] == k)
        f = lambda v: f"n={len(v)} med={st.median(v):.2f}" if v else "n=0"
        print(f"  {k:<8}{f(vm):>22}{f(va):>22}")

    print(f"\n=== units that CHANGE class: {len(moved)} ===")
    if moved:
        print(f"  {'unit':<20}{'n':>5}{'mash':>9}{'aln':>9}  {'was':<6}->{'now':>6}"
              f"{'r/m':>8}")
        for u, n, M, A, km, ka, v in sorted(moved, key=lambda x: -abs(x[6])):
            print(f"  {u:<20}{n:>5}{M:>9.0f}{A:>9.0f}  {km:<6}->{ka:>6}{v:>8.2f}")

    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, delimiter="\t", lineterminator="\n",
                           fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print(f"\nwrote {a.out}")

    ia = sorted(float(r["rm_corrected"]) for r in rows
                if r["gate1_alignment"] == "in")
    im = sorted(float(r["rm_corrected"]) for r in rows if r["gate1_mash"] == "in")
    print(f"\n=== THE HEADLINE ===")
    print(f"  in-window median r/m, mash proxy   : {st.median(im):.2f}  (n={len(im)})")
    print(f"  in-window median r/m, ALIGNMENT    : {st.median(ia):.2f}  (n={len(ia)})")


if __name__ == "__main__":
    main()
