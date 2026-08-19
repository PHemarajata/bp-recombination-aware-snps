#!/usr/bin/env python3
"""Tier 0 evidence base: recompute, from disk, every number the Tier 0
corrections assert.

WHY THIS EXISTS. Tier 0 rewrites five load-bearing claims in the record
(FINISHING_PLAN_2026-08-11.md Part 3). Four of them are numeric. Copying those
numbers out of the plan into the record would make the record agree with the
plan without either agreeing with the data, so every figure quoted in a Tier 0
edit is regenerated here from the `prod_*` run directories and the input tables.

WHAT IT EMITS
  tier0_units.tsv       one row per unit: n, ska, screened, reference source and
                        borrow distance, per-replicon union/rm/tract/ufboot
  stdout                the four analyses below, formatted for pasting

THE FOUR ANALYSES
  1  UFBOOT SWEEP (Tier 0.1). Units and genomes surviving detection at each
     candidate median-UFBoot gate. The point is the SPREAD: a headline that
     moves 4x across the range of conventions someone might reasonably pick is
     not a measurement of anything.

  2  PARTIAL CORRELATIONS (Tier 0.3). r(log n, union) and r(diversity, union),
     marginally and each controlling for the other. Partials are computed as the
     correlation of OLS residuals, which is the definition; scipy is used only
     for the p-values.

  3  BORROWED vs INTERNAL REFERENCES (Tier 0.4). Every statistic compared across
     the two reference classes, plus the regression of each statistic on borrow
     distance. This is the test that replaces "validated once" -- 33 borrows ran
     in production, so the n=1 validation the handoff cites was never the whole
     evidence, it was just the only part anyone had looked at.

  4  SHARED-BIN CONCENTRATION (context for Tier 1.2). Recombinant 10-kb bins
     shared across units on a common reference. Reported here only so Tier 0 and
     Tier 1 read the same file; the lineage-confound caveat is in the plan.

Usage:
    python3 tier0_evidence_bp.py                 # analyse, write tier0_units.tsv
    python3 tier0_evidence_bp.py --selftest
"""

import argparse
import math
import os
import re
import statistics
import sys

import cap_location_bp as C
import triage_analysable_bp as T

SELF = os.path.dirname(os.path.abspath(__file__))
OUT_TSV = os.path.join(SELF, "tier0_units.tsv")
REFS_FINAL = os.path.join(SELF, "analysable_references_final.tsv")

# Candidate gates for analysis 1. 70 is what was adopted; 95 is the convention
# UFBoot actually carries (Minh 2013 -- UFBoot >= 95 is the "supported" line, NOT
# 70, which is the SBS convention the adoption note mistakenly imported).
UFBOOT_GATES = (None, 70.0, 80.0, 90.0, 95.0)


# ---------------------------------------------------------------- loading

def load_reference_class(path=REFS_FINAL):
    """unit -> (source, borrow_mash or nan).

    `ref_mean_mash` is blank for internal medoids (distance to self is not a
    borrow distance) and populated for borrows.
    """
    out = {}
    with open(path) as fh:
        hdr = fh.readline().rstrip("\n").split("\t")
        for line in fh:
            f = line.rstrip("\n").split("\t")
            if len(f) < 2:
                continue
            r = dict(zip(hdr, f + [""] * (len(hdr) - len(f))))
            raw = (r.get("ref_mean_mash") or "").strip()
            try:
                d = float(raw)
            except ValueError:
                d = float("nan")
            src = (r.get("source") or "").strip()
            # A borrow recorded with distance 0 is an internal medoid mislabelled
            # by the runner format; treat the source column as authoritative.
            if src == "internal_medoid":
                d = float("nan")
            out[r["unit"]] = (src, d)
    return out


def per_replicon(outdir):
    """[(arm_name, stats, ufboot)] for the two close__ska_map arms, sorted."""
    d = os.path.join(outdir, "arms")
    if not os.path.isdir(d):
        return []
    rows = []
    for arm in sorted(os.listdir(d)):
        if not arm.startswith("close__ska_map"):
            continue
        p = os.path.join(d, arm)
        if not os.path.isdir(p):
            continue
        s = C.gubbins_stats(p)
        if s:
            rows.append((arm, s, T.median_ufboot(p)))
    return rows


def collect():
    """One record per unit with results on disk."""
    units = T.load_units()
    refs = load_reference_class()
    recs = []
    for unit, meta in sorted(units.items()):
        arms = per_replicon(os.path.join(SELF, "prod_" + unit))
        if len(arms) != 2:
            continue
        src, mash = refs.get(unit, ("", float("nan")))
        recs.append({
            "unit": unit,
            "n": meta["n"],
            "ska": meta["ska"],
            "screened": meta["screened"],
            "source": meta["source"],
            "ref_class": "borrowed" if src == "borrowed" else "internal",
            "borrow_mash": mash,
            "union": statistics.mean(s["union"] for _, s, _ in arms),
            "rm": statistics.mean(s["pooled_rm"] for _, s, _ in arms),
            "tract": statistics.mean(s["median_block"] for _, s, _ in arms),
            "ufboot": min(b for _, _, b in arms),
            "ufboot_mean": statistics.mean(b for _, _, b in arms),
            "arms": arms,
        })
    return recs


# ---------------------------------------------------------------- statistics

def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return float("nan")
    mx, my = statistics.mean(xs), statistics.mean(ys)
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return float("nan")
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy)


def residuals(ys, xs):
    """Residuals of ys after OLS regression on xs (single predictor)."""
    mx, my = statistics.mean(xs), statistics.mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return [y - my for y in ys]
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    a = my - b * mx
    return [y - (a + b * x) for x, y in zip(xs, ys)]


def partial(ys, xs, zs):
    """Partial correlation r(x, y | z), as the correlation of both residuals."""
    return pearson(residuals(xs, zs), residuals(ys, zs))


def pvalue(r, n, k=0):
    """Two-sided p for a (partial) correlation controlling k variables."""
    df = n - 2 - k
    if df <= 0 or not (-1 < r < 1):
        return float("nan")
    try:
        from scipy import stats
    except ImportError:
        return float("nan")
    t = r * math.sqrt(df / (1 - r * r))
    return 2 * stats.t.sf(abs(t), df)


def mannwhitney(a, b):
    """Two-sided Mann-Whitney U p-value, or nan without scipy.

    Used rather than a t-test because the borrowed/internal groups are small and
    the statistics are bounded fractions.
    """
    try:
        from scipy import stats
    except ImportError:
        return float("nan")
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    return stats.mannwhitneyu(a, b, alternative="two-sided").pvalue


# ---------------------------------------------------------------- analyses

def detection_ok(rec):
    """Does the unit pass DETECTION, i.e. the screens minus any UFBoot gate?

    This is `triage` with the resolution step removed, which is exactly what
    Tier 0.1 prescribes.
    """
    flag, _ = T._detect(rec["union"], rec["rm"], rec["screened"], rec["n"])
    return flag in T._USABLE


def analysis_ufboot_sweep(recs, total=2802):
    print("=" * 78)
    print("1. UFBOOT SWEEP -- what the headline does across bootstrap conventions")
    print("=" * 78)
    passed = [r for r in recs if detection_ok(r)]
    print("%-34s %6s %8s %9s" % ("gate", "units", "genomes", "coverage"))
    rows = []
    for g in UFBOOT_GATES:
        if g is None:
            keep = passed
            label = "detection only, no bootstrap gate"
        else:
            keep = [r for r in passed if r["ufboot"] >= g]
            label = "median UFBoot >= %.0f (worse replicon)" % g
        gen = sum(r["n"] for r in keep)
        rows.append((g, len(keep), gen, gen / total))
        print("%-34s %6d %8d %8.1f%%" % (label, len(keep), gen, 100 * gen / total))
    hi = max(r[3] for r in rows)
    lo = min(r[3] for r in rows)
    print("\nspread across conventions: %.1f%% -> %.1f%% = %.1fx"
          % (100 * lo, 100 * hi, hi / lo if lo else float("inf")))
    print("A headline that moves %.1fx on the choice of convention is not a result."
          % (hi / lo if lo else float("inf")))
    return rows


def analysis_partials(recs):
    print()
    print("=" * 78)
    print("2. PARTIAL CORRELATIONS -- is the size effect on union a confound?")
    print("=" * 78)
    n = len(recs)
    logn = [math.log(r["n"]) for r in recs]
    div = [float(r["ska"]) for r in recs]
    uni = [r["union"] for r in recs]

    tests = [
        ("marginal r(log n, union)", pearson(logn, uni), 0),
        ("marginal r(diversity, union)", pearson(div, uni), 0),
        ("r(log n, diversity)  [the putative confounder]", pearson(logn, div), 0),
        ("partial r(log n, union | diversity)", partial(uni, logn, div), 1),
        ("partial r(diversity, union | log n)", partial(uni, div, logn), 1),
    ]
    print("n = %d units\n" % n)
    print("%-46s %8s %10s" % ("", "r", "p"))
    for label, r, k in tests:
        print("%-46s %+8.3f %10.2g" % (label, r, pvalue(r, n, k)))

    conf = pearson(logn, div)
    print("\nreading: size and diversity are %s (r = %+.3f), so there was %s"
          % ("essentially uncorrelated" if abs(conf) < 0.2 else "correlated",
             conf,
             "no confound to control for" if abs(conf) < 0.2 else "a real confound"))
    return dict((label, r) for label, r, _ in tests)


def analysis_references(recs):
    print()
    print("=" * 78)
    print("3. BORROWED vs INTERNAL REFERENCES -- does borrowing degrade anything?")
    print("=" * 78)
    bor = [r for r in recs if r["ref_class"] == "borrowed"]
    inte = [r for r in recs if r["ref_class"] == "internal"]
    print("borrowed: %d units (%d genomes) | internal: %d units (%d genomes)\n"
          % (len(bor), sum(r["n"] for r in bor),
             len(inte), sum(r["n"] for r in inte)))

    print("%-10s %22s %22s %10s" % ("statistic", "borrowed (median)",
                                    "internal (median)", "MWU p"))
    for key, fmt in (("union", "%.3f"), ("rm", "%.2f"),
                     ("tract", "%.0f"), ("ufboot", "%.1f")):
        a = [r[key] for r in bor]
        b = [r[key] for r in inte]
        print("%-10s %22s %22s %10.2g"
              % (key,
                 (fmt + "  (%d)") % (statistics.median(a), len(a)),
                 (fmt + "  (%d)") % (statistics.median(b), len(b)),
                 mannwhitney(a, b)))

    # Dose-response: if borrowing hurts, the harm should grow with distance.
    d = [(r["borrow_mash"], r) for r in bor if r["borrow_mash"] == r["borrow_mash"]]
    print("\ndose-response over %d borrows with a recorded distance "
          "(range %.5f-%.5f):" % (len(d), min(x for x, _ in d), max(x for x, _ in d)))
    print("%-34s %8s %10s" % ("", "r", "p"))
    xs = [x for x, _ in d]
    for key in ("union", "rm", "tract", "ufboot"):
        ys = [r[key] for _, r in d]
        rr = pearson(xs, ys)
        print("%-34s %+8.3f %10.2g" % ("r(borrow distance, %s)" % key, rr,
                                       pvalue(rr, len(d))))
    # n also matters for union, so control for it -- otherwise a borrow class
    # that happens to be smaller would look worse for the wrong reason.
    lg = [math.log(r["n"]) for _, r in d]
    ru = partial([r["union"] for _, r in d], xs, lg)
    print("%-34s %+8.3f %10.2g" % ("  ... union, controlling log n", ru,
                                   pvalue(ru, len(d), 1)))
    return {"borrowed": len(bor), "internal": len(inte)}


def analysis_shared_bins(recs, binsize=10000):
    """Recombinant-bin sharing across units mapped to the SAME reference."""
    print()
    print("=" * 78)
    print("4. SHARED RECOMBINANT BINS (context for Tier 1.2)")
    print("=" * 78)
    refs = load_reference_class()
    byref = {}
    for r in recs:
        # group by the actual reference NAME, from the runner table
        byref.setdefault(_ref_name(r["unit"]), []).append(r)
    groups = [(k, v) for k, v in byref.items() if len(v) >= 4 and k]
    if not groups:
        print("no reference shared by >=4 units; skipped")
        return
    for refname, members in sorted(groups, key=lambda kv: -len(kv[1])):
        for arm_idx, arm_label in ((0, "chr1"), (1, "chr2")):
            bins = {}
            used = 0
            for r in members:
                if len(r["arms"]) <= arm_idx:
                    continue
                p = os.path.join(SELF, "prod_" + r["unit"], "arms",
                                 r["arms"][arm_idx][0])
                iv = _recomb_intervals(p)
                if iv is None:
                    continue
                used += 1
                for s, e in iv:
                    for b in range(s // binsize, e // binsize + 1):
                        bins.setdefault(b, set()).add(r["unit"])
            if used < 4 or not bins:
                continue
            counts = [len(v) for v in bins.values()]
            allu = sum(1 for c in counts if c == used)
            most = sum(1 for c in counts if c >= 0.8 * used)
            one = sum(1 for c in counts if c == 1)
            print("\n%s %s -- %d units sharing this reference" % (refname, arm_label, used))
            print("  bins with any recombination      %5d" % len(bins))
            print("  recombinant in ALL %2d units      %5d" % (used, allu))
            print("  recombinant in >=80%% of units    %5d  (%.0f%% of bins)"
                  % (most, 100 * most / len(bins)))
            print("  recombinant in exactly ONE unit  %5d" % one)


def _ref_name(unit):
    if not hasattr(_ref_name, "_map"):
        m = {}
        with open(os.path.join(SELF, "analysable_refs_runner.tsv")) as fh:
            hdr = fh.readline().rstrip("\n").split("\t")
            for line in fh:
                f = line.rstrip("\n").split("\t")
                r = dict(zip(hdr, f))
                m[r["cluster_id"]] = r.get("reference", "")
        _ref_name._map = m
    return _ref_name._map.get(unit, "")


def _recomb_intervals(armdir):
    """[(start, end)] from a Gubbins GFF, or None if absent."""
    for name in ("gubbins.recombination_predictions.gff",
                 "recombination_predictions.gff"):
        p = os.path.join(armdir, name)
        if os.path.exists(p):
            iv = []
            with open(p) as fh:
                for line in fh:
                    if line.startswith("#"):
                        continue
                    f = line.rstrip("\n").split("\t")
                    if len(f) > 4:
                        try:
                            iv.append((int(f[3]), int(f[4])))
                        except ValueError:
                            pass
            return iv
    return None


def write_tsv(recs, path=OUT_TSV):
    cols = ("unit", "n", "ska", "screened", "source", "ref_class", "borrow_mash",
            "union", "rm", "tract", "ufboot", "ufboot_mean")
    with open(path, "w") as fh:
        fh.write("\t".join(cols) + "\tdetection\n")
        for r in recs:
            fh.write("\t".join(
                ("%.5f" % r[c]) if isinstance(r[c], float) else str(r[c])
                for c in cols) + "\t%s\n" % ("pass" if detection_ok(r) else "fail"))
    print("\nwrote %s (%d units)" % (path, len(recs)))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--skip-bins", action="store_true",
                    help="skip analysis 4 (it reads every GFF)")
    args = ap.parse_args()
    if args.selftest:
        return selftest()

    recs = collect()
    if not recs:
        print("no completed prod_* units found", file=sys.stderr)
        return 1
    analysis_ufboot_sweep(recs)
    analysis_partials(recs)
    analysis_references(recs)
    if not args.skip_bins:
        analysis_shared_bins(recs)
    write_tsv(recs)
    return 0


def selftest():
    fails = []

    def chk(desc, got, want, tol=1e-9):
        ok = (abs(got - want) <= tol) if isinstance(want, float) else (got == want)
        print("%-52s %s" % (desc, "ok" if ok else "FAIL got=%r want=%r" % (got, want)))
        if not ok:
            fails.append(desc)

    # pearson against hand-computed values
    chk("pearson perfect +", pearson([1, 2, 3, 4], [2, 4, 6, 8]), 1.0, 1e-12)
    chk("pearson perfect -", pearson([1, 2, 3, 4], [8, 6, 4, 2]), -1.0, 1e-12)
    chk("pearson orthogonal", pearson([1, 2, 3, 4], [1, -1, -1, 1]), 0.0, 1e-12)

    # A partial correlation must remove a pure confound. x and y are driven by z
    # plus INDEPENDENT jitter -- without the jitter both residual vectors are
    # identically zero and the partial is undefined rather than 0 (tested next).
    # jx and jy are each orthogonal to z AND to one another by construction, so
    # the residuals are exactly 0.3*jx and 0.3*jy and the partial is exactly 0.
    z = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    jx = [1, -1, -1, 1, 1, -1, -1, 1]
    jy = [1, -1, 1, -1, -1, 1, -1, 1]
    x = [2 * v + 0.3 * j for v, j in zip(z, jx)]
    y = [3 * v + 0.3 * j for v, j in zip(z, jy)]
    chk("marginal r(x,y) with shared driver", pearson(x, y) > 0.99, True)
    chk("partial r(x,y|z) removes it", abs(partial(y, x, z)), 0.0, 1e-12)

    # Degenerate case: if z explains x and y EXACTLY there is no residual
    # variance and the partial is undefined. It must return nan rather than a
    # confident number -- a silent 0.0 here would read as "confound fully
    # controlled" when the truth is "not identifiable".
    xe = [2 * v for v in z]
    ye = [3 * v for v in z]
    pe = partial(ye, xe, z)
    chk("partial is nan when z explains both exactly", pe != pe, True)

    # And it must LEAVE an effect that is genuinely independent of z.
    x2 = [1.0, 3.0, 2.0, 5.0, 4.0, 6.0]
    y2 = [v + 0.5 * w for v, w in zip(x2, z)]
    p = partial(y2, x2, z)
    chk("partial keeps an independent effect", p > 0.9, True)

    # residuals of an exact fit are zero
    chk("residuals of exact fit", max(abs(v) for v in residuals(xe, z)), 0.0, 1e-12)

    # detection_ok must ignore UFBoot entirely -- this is the Tier 0.1 contract
    lo = {"union": 0.80, "rm": 7.2, "screened": "yes", "n": 50, "ufboot": 12.0}
    hi = dict(lo, ufboot=99.0)
    chk("detection ignores a terrible UFBoot", detection_ok(lo), True)
    chk("detection ignores a perfect UFBoot", detection_ok(hi), True)
    chk("detection still rejects a real failure",
        detection_ok({"union": 0.10, "rm": 0.4, "screened": "yes", "n": 50}), False)

    # reference-class loader: blank distance must not become 0.0, which would
    # put every internal medoid at the friendly end of a dose-response curve.
    rc = load_reference_class()
    intern = [d for s, d in rc.values() if s == "internal_medoid"]
    chk("internal medoids carry no borrow distance",
        all(d != d for d in intern), True)
    bor = [d for s, d in rc.values() if s == "borrowed"]
    chk("borrows carry a distance", all(d == d for d in bor) and len(bor) > 0, True)

    print("\n%d test(s) failed" % len(fails) if fails else "\nall tests passed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
