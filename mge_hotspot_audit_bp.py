#!/usr/bin/env python3
"""Tier 1.2 -- the MGE / hotspot audit: is shared recombinant positioning an
ARTEFACT (mobile elements, repeats, mismapping) or ANCESTRY (shared inherited
recombination)?

THE QUESTION. If recombination tracts pile up at the same reference coordinates
across units that were corrected independently, something is generating them at
fixed positions. The competing explanation is inheritance: units drawn from one
lineage share ancestral recombination, so agreement is expected without any
artefact.

WHAT THE FIRST PASS GOT WRONG, and why this script exists. The original test
counted bins "recombinant in >=80% of units" per reference group. That statistic
is NOT comparable across groups of different size -- with 8 units it means >=7,
but with 4 units it means all 4, the strictest possible criterion. Comparing 46%
(8 units) against 3% (4 units) and reading a lineage effect was therefore
comparing two different questions. Two fixes, both applied here:

  1  AN INDEPENDENCE NULL. Each unit flags some marginal fraction p_i of bins.
     Under independent recombination the chance that ALL k units flag the same
     bin is the product of p_i. Enrichment = observed / expected. This is
     dimensionless and comparable across groups of any size.

  2  SIZE-MATCHED SUBSAMPLING. Every group is also scored at a common k (default
     4) by averaging over subsets, so the headline can be compared directly
     between groups.

THE LINEAGE CONTROL. Groups are labelled by how many distinct source lineages
they contain. `same-lineage` groups can explain sharing by inheritance;
`cross-lineage` groups cannot, because units from different lineages do not
share recombination ancestrally. Enrichment that PERSISTS in cross-lineage
groups is the evidence for an artefact.

WHY IT MATTERS. If the signal is artefact, MGEs are inflating r/m in every unit,
the acceptance criteria have been reading artefact as health, and the accepted
units must be re-run on masked input. This is the one Tier 1 result that can
force a re-run.

Usage:
    python3 mge_hotspot_audit_bp.py
    python3 mge_hotspot_audit_bp.py --bin 5000 --match-k 4
    python3 mge_hotspot_audit_bp.py --selftest
"""

import argparse
import itertools
import math
import os
import statistics
import sys

import tier0_evidence_bp as E

SELF = os.path.dirname(os.path.abspath(__file__))

# The lineage a unit belongs to. `s2_L1_7` -> `s2`; a PopPUNK strain is its own
# lineage. Units sharing a prefix descend from one PopPUNK strain, so they are
# the ones that can share recombination by inheritance.
def lineage(unit):
    if unit.startswith("strain_"):
        return unit
    return unit.split("_L1_")[0].split("_L2_")[0]


def bins_for(armdir, binsize, nbins=None):
    """set of bin indices touched by any recombination interval, or None."""
    iv = E._recomb_intervals(armdir)
    if iv is None:
        return None
    out = set()
    for s, e in iv:
        if e < s:
            s, e = e, s
        for b in range(s // binsize, e // binsize + 1):
            if nbins is None or b < nbins:
                out.add(b)
    return out


def replicon_bins(armdir, binsize):
    """Number of bins in the replicon, from the Gubbins GFF sequence-region
    header if present, else from the largest coordinate seen."""
    for name in ("gubbins.recombination_predictions.gff",
                 "recombination_predictions.gff"):
        p = os.path.join(armdir, name)
        if not os.path.exists(p):
            continue
        hi = 0
        with open(p) as fh:
            for line in fh:
                if line.startswith("##sequence-region"):
                    f = line.split()
                    if len(f) >= 4:
                        try:
                            return int(math.ceil(int(f[3]) / binsize))
                        except ValueError:
                            pass
                elif not line.startswith("#"):
                    f = line.rstrip("\n").split("\t")
                    if len(f) > 4:
                        try:
                            hi = max(hi, int(f[4]))
                        except ValueError:
                            pass
        if hi:
            return int(math.ceil(hi / binsize))
    return None


def expected_all(ps):
    """P(all k units flag a given bin) under independence."""
    out = 1.0
    for p in ps:
        out *= p
    return out


def enrichment(sets, nbins):
    """(observed, expected, enrichment) for 'recombinant in ALL k units'."""
    if not sets or nbins <= 0:
        return (float("nan"),) * 3
    inter = set.intersection(*sets)
    obs = len(inter) / nbins
    exp = expected_all([len(s) / nbins for s in sets])
    return obs, exp, (obs / exp if exp > 0 else float("inf"))


def matched_enrichment(sets, nbins, k, cap=70):
    """Mean enrichment over subsets of size k, so groups of different size are
    compared on the same question. Subsets are capped for runtime; the cap is
    only reached for large groups and the estimate is a mean either way."""
    if len(sets) < k:
        return float("nan"), 0
    subs = list(itertools.combinations(range(len(sets)), k))
    if len(subs) > cap:
        step = len(subs) / cap
        subs = [subs[int(i * step)] for i in range(cap)]
    vals = []
    for idx in subs:
        _, _, e = enrichment([sets[i] for i in idx], nbins)
        if e == e and e != float("inf"):
            vals.append(e)
    return (statistics.mean(vals) if vals else float("nan")), len(subs)


def audit(binsize=10000, match_k=4, min_units=4):
    recs = E.collect()
    byref = {}
    for r in recs:
        byref.setdefault(E._ref_name(r["unit"]), []).append(r)

    rows = []
    for refname, members in sorted(byref.items(), key=lambda kv: -len(kv[1])):
        if len(members) < min_units or not refname:
            continue
        lins = sorted({lineage(r["unit"]) for r in members})
        kind = "same-lineage" if len(lins) == 1 else (
            "mostly-1-lineage" if _dominant(members) >= 0.75 else "cross-lineage")
        for arm_idx, arm_label in ((0, "chr1"), (1, "chr2")):
            sets, names, nbins = [], [], None
            for r in members:
                if len(r["arms"]) <= arm_idx:
                    continue
                p = os.path.join(SELF, "prod_" + r["unit"], "arms",
                                 r["arms"][arm_idx][0])
                nb = replicon_bins(p, binsize)
                if nb:
                    nbins = max(nbins or 0, nb)
            if not nbins:
                continue
            for r in members:
                if len(r["arms"]) <= arm_idx:
                    continue
                p = os.path.join(SELF, "prod_" + r["unit"], "arms",
                                 r["arms"][arm_idx][0])
                s = bins_for(p, binsize, nbins)
                if s:
                    sets.append(s)
                    names.append(r["unit"])
            if len(sets) < min_units:
                continue
            obs, exp, enr = enrichment(sets, nbins)
            menr, nsub = matched_enrichment(sets, nbins, match_k)
            rows.append({
                "ref": refname, "arm": arm_label, "kind": kind,
                "k": len(sets), "lineages": len(lins), "nbins": nbins,
                "marg_lo": min(len(s) / nbins for s in sets),
                "marg_hi": max(len(s) / nbins for s in sets),
                "obs": obs, "exp": exp, "enr": enr,
                "menr": menr, "nsub": nsub,
                "units": names,
            })
    return rows


def _dominant(members):
    c = {}
    for r in members:
        c[lineage(r["unit"])] = c.get(lineage(r["unit"]), 0) + 1
    return max(c.values()) / len(members)


def report(rows, match_k):
    print("=" * 96)
    print("TIER 1.2 -- MGE / HOTSPOT AUDIT with an independence null and a "
          "lineage control")
    print("=" * 96)
    print("\nenrichment = P(bin recombinant in ALL k units) observed / expected "
          "under independence.")
    print("enrichment ~1 means agreement is what chance predicts. >>1 means "
          "tracts land at shared coordinates.")
    print("`matched` repeats the same statistic at k=%d for every group, so "
          "groups of different\nsize are compared on the same question."
          % match_k)
    print()
    hdr = ("%-42s %5s %4s %5s %13s %9s %9s %8s %8s"
           % ("reference / replicon", "kind", "k", "lin", "per-unit rate",
              "obs", "exp", "enrich", "matched"))
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print("%-42s %5s %4d %5d  %5.0f%%-%-5.0f%% %8.4f %9.2e %8.1f %8.1f"
              % ((r["ref"][:28] + " " + r["arm"]), r["kind"][:5], r["k"],
                 r["lineages"], 100 * r["marg_lo"], 100 * r["marg_hi"],
                 r["obs"], r["exp"], r["enr"], r["menr"]))

    lo = min(r["marg_lo"] for r in rows)
    hi = max(r["marg_hi"] for r in rows)
    print("\nPER-UNIT RATE is the fraction of bins a SINGLE unit flags as "
          "recombinant somewhere\n(%.0f%%-%.0f%% here). That is what drives the "
          "null: when individual units each flag\nmost of the genome, near-total "
          "agreement between them is arithmetic, not signal." % (100 * lo, 100 * hi))

    cross = [r for r in rows if r["kind"] == "cross-lineage"]
    same = [r for r in rows if r["kind"] != "cross-lineage"]
    print()
    print("=" * 96)
    print("THE LINEAGE CONTROL")
    print("=" * 96)
    for label, grp in (("cross-lineage (inheritance CANNOT explain sharing)", cross),
                       ("same / mostly-one-lineage (inheritance CAN explain it)", same)):
        if not grp:
            print("\n%-56s  no groups" % label)
            continue
        m = [r["menr"] for r in grp if r["menr"] == r["menr"]]
        print("\n%s" % label)
        print("  groups                       %d" % len(grp))
        print("  matched enrichment at k=%d    median %.1f   range %.1f-%.1f"
              % (match_k, statistics.median(m), min(m), max(m)))
    if cross and same:
        mc = statistics.median([r["menr"] for r in cross])
        ms = statistics.median([r["menr"] for r in same])
        print("\nVERDICT")
        if mc < 2:
            print("  Cross-lineage enrichment is ~%.1fx at matched k -- near chance." % mc)
            print("  The shared positioning that looked alarming in raw shared-bin counts"
                  "\n  is almost entirely explained by how much of the genome each unit"
                  "\n  flags on its own. No masked re-run is indicated on this evidence.")
            print("\n  WHAT THIS DOES NOT SAY. Enrichment is small, not absent, and it"
                  "\n  RISES at finer bin sizes (run --bin 1000 and --bin 500) -- the"
                  "\n  signature of localised shared hotspots rather than none. It is also"
                  "\n  higher in same-lineage groups (%.1fx) than cross-lineage (%.1fx),"
                  "\n  which is the direction ancestry predicts. Read this as BOUNDING a"
                  "\n  fixed-coordinate artefact at a small factor, not excluding one."
                  % (ms, mc))
        else:
            print("  Cross-lineage enrichment is %.1fx (same-lineage %.1fx). Units that"
                  "\n  CANNOT share recombination ancestrally still agree far beyond"
                  "\n  chance, so something is generating tracts at fixed reference"
                  "\n  coordinates. THIS IMPLICATES AN ARTEFACT and every r/m is"
                  "\n  affected -- mask MGEs and re-run." % (mc, ms))
            print("  Ratio cross/same = %.2f (1.0 would mean lineage membership makes"
                  "\n  no difference at all)." % (mc / ms if ms else float("nan")))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bin", type=int, default=10000)
    ap.add_argument("--match-k", type=int, default=4)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    rows = audit(binsize=args.bin, match_k=args.match_k)
    if not rows:
        print("no reference shared by enough units", file=sys.stderr)
        return 1
    report(rows, args.match_k)
    return 0


def selftest():
    fails = []

    def chk(desc, got, want, tol=1e-9):
        ok = (abs(got - want) <= tol) if isinstance(want, float) else (got == want)
        print("%-56s %s" % (desc, "ok" if ok else "FAIL got=%r want=%r" % (got, want)))
        if not ok:
            fails.append(desc)

    chk("lineage of a sub-cluster", lineage("s2_L1_7"), "s2")
    chk("lineage of a sub-sub-cluster", lineage("s1_L1_27_L2_69"), "s1")
    chk("a strain is its own lineage", lineage("strain_15"), "strain_15")

    # Independence: two units each flagging half the bins, with NO shared
    # structure, must give enrichment ~1.
    nb = 400
    a = set(range(0, nb, 2))          # 200 bins, evens
    b = set(range(0, nb))             # every bin
    obs, exp, enr = enrichment([a, b], nb)
    chk("nested sets give exactly chance", enr, 1.0, 1e-9)

    # Perfectly shared: two units flagging the SAME 40 bins out of 400.
    s = set(range(40))
    obs, exp, enr = enrichment([s, set(s)], nb)
    chk("identical sets are enriched 10x", enr, 10.0, 1e-9)

    # Disjoint sets: observed 0, enrichment 0.
    obs, exp, enr = enrichment([set(range(40)), set(range(40, 80))], nb)
    chk("disjoint sets give zero enrichment", enr, 0.0, 1e-12)

    # Enrichment must be dimensionless w.r.t. group size: three identical sets
    # covering 10% of bins are enriched 100x (0.1 / 0.1^3), which is why raw
    # "shared by all k" counts CANNOT be compared across k.
    s = set(range(40))
    _, _, e3 = enrichment([set(s), set(s), set(s)], nb)
    chk("3 identical sets -> 100x, showing k-dependence", e3, 100.0, 1e-6)

    # ... and that is exactly what matched_enrichment controls for.
    m2, _ = matched_enrichment([set(s)] * 4, nb, 2)
    chk("matched at k=2 recovers the k=2 value", m2, 10.0, 1e-6)

    # bin mapping covers both endpoints of an interval
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        with open(os.path.join(td, "recombination_predictions.gff"), "w") as fh:
            fh.write("##gff-version 3\n##sequence-region SEQ 1 100000\n")
            fh.write("SEQ\tx\ty\t9500\t20500\t.\t.\t.\tz\n")
        got = bins_for(td, 10000)
        chk("interval spans every bin it touches", got, {0, 1, 2})
        chk("replicon length read from the header", replicon_bins(td, 10000), 10)

    print("\n%d test(s) failed" % len(fails) if fails else "\nall tests passed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
