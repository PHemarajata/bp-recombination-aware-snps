#!/usr/bin/env python3
"""Tier 1.4 -- does VARIANCE in per-genome callable fraction explain the r/m
residue?

THE HYPOTHESIS. Section 9.4 records a set of units with clean modality, adequate
size and healthy union coverage that nonetheless return depressed pooled r/m,
with five candidate explanations tested and refuted. This is the sixth: if the
genomes within a unit differ a lot in how much of the reference they actually
call -- some near-complete, others heavily N-masked -- then the effective
alignment shared by all of them is small and patchy, and recombination detection
could degrade for a reason that has nothing to do with biology.

Note this is a hypothesis about VARIANCE, not about level. A unit where every
genome calls 80% of sites is uniformly reduced but internally consistent; a unit
where genomes range from 40% to 99% has the same mean and a much worse shared
core. Both are reported so the two can be told apart.

WHAT IT MEASURES, per unit and replicon, from the full-length alignment that
entered Gubbins:
    callable_i   = fraction of non-N, non-gap positions for genome i
    mean, sd, cv = across genomes within the unit
    min          = the worst genome, which is what a shared core is limited by

then regresses pooled r/m on each, marginally and controlling for unit size and
diversity (both of which are already known to matter).

HOW TO READ A NULL RESULT. A flat regression here does NOT mean callable
fraction is irrelevant to recombination detection in general -- only that
variation in it does not explain the r/m spread ACROSS THESE UNITS. That is
still worth having: it is the fifth of five candidate explanations to be
excluded, and the plan budgets for the residue remaining unexplained.

Usage:
    python3 callable_variance_bp.py
    python3 callable_variance_bp.py --selftest
"""

import argparse
import math
import os
import statistics
import sys

import tier0_evidence_bp as E

SELF = os.path.dirname(os.path.abspath(__file__))
OUT_TSV = os.path.join(SELF, "callable_variance.tsv")

# Anything that is not a called base. Gubbins treats N and - as missing; lower
# case appears in some pipelines and must not be counted as missing.
MISSING = set(b"Nn-.?")


def callable_fractions(path):
    """[fraction of called positions] per record, streaming.

    Reads in binary and counts bytes rather than building sequence strings --
    these alignments run to hundreds of MB per unit and holding one in memory
    per record is what makes the naive version unusable.
    """
    fracs = []
    called = total = 0
    started = False
    with open(path, "rb") as fh:
        for line in fh:
            if line.startswith(b">"):
                if started:
                    fracs.append(called / total if total else 0.0)
                called = total = 0
                started = True
                continue
            s = line.strip()
            if not s:
                continue
            total += len(s)
            called += len(s) - sum(1 for b in s if b in MISSING)
    if started:
        fracs.append(called / total if total else 0.0)
    return fracs


def find_alignment(armdir):
    for f in sorted(os.listdir(armdir)):
        if f.startswith("aln.full.") and f.endswith((".fa", ".fasta")):
            return os.path.join(armdir, f)
    return None


def collect(verbose=True):
    recs = E.collect()
    out = []
    for i, r in enumerate(recs):
        per_arm = []
        for arm, _, _ in r["arms"]:
            armdir = os.path.join(SELF, "prod_" + r["unit"], "arms", arm)
            p = find_alignment(armdir)
            if not p:
                continue
            f = callable_fractions(p)
            if len(f) < 3:
                continue
            per_arm.append({
                "mean": statistics.mean(f),
                "sd": statistics.pstdev(f),
                "min": min(f),
                "n_seq": len(f),
            })
        if not per_arm:
            continue
        mean = statistics.mean(a["mean"] for a in per_arm)
        sd = statistics.mean(a["sd"] for a in per_arm)
        rec = dict(r)
        rec.update({
            "callable_mean": mean,
            "callable_sd": sd,
            "callable_cv": (sd / mean) if mean else float("nan"),
            "callable_min": min(a["min"] for a in per_arm),
            "n_seq": max(a["n_seq"] for a in per_arm),
        })
        out.append(rec)
        if verbose:
            print("  %-18s mean %.3f  sd %.4f  min %.3f  (r/m %.2f)"
                  % (r["unit"], mean, sd, rec["callable_min"], r["rm"]),
                  file=sys.stderr)
    return out


def report(recs):
    print("=" * 82)
    print("TIER 1.4 -- callable-fraction variance vs pooled r/m")
    print("=" * 82)
    print("\n%d units. Callable fraction = non-N, non-gap positions in the "
          "full-length\nalignment that entered Gubbins, averaged over both "
          "replicons.\n" % len(recs))

    rm = [r["rm"] for r in recs]
    logn = [math.log(r["n"]) for r in recs]
    div = [float(r["ska"]) for r in recs]

    print("%-40s %8s %10s %10s" % ("predictor of pooled r/m", "r", "p", "r|n,div"))
    print("-" * 72)
    for key, label in (("callable_sd", "sd of callable fraction  <- THE TEST"),
                       ("callable_cv", "cv of callable fraction"),
                       ("callable_mean", "mean callable fraction"),
                       ("callable_min", "worst genome's callable fraction")):
        xs = [r[key] for r in recs]
        m = E.pearson(xs, rm)
        # control for size and diversity together, sequentially
        rx = E.residuals(xs, logn)
        ry = E.residuals(rm, logn)
        ctrl = E.pearson(E.residuals(rx, div), E.residuals(ry, div))
        print("%-40s %+8.3f %10.3g %+10.3f"
              % (label, m, E.pvalue(m, len(recs)), ctrl))

    print("\nfor reference, the predictors already known to matter:")
    for xs, label in ((logn, "log(unit size)"), (div, "diversity")):
        m = E.pearson(xs, rm)
        print("%-40s %+8.3f %10.3g" % (label, m, E.pvalue(m, len(recs))))

    # The three named A.11l units, called out individually -- the hypothesis is
    # specifically about them, so a group-level regression could wash them out.
    named = ("s1_L1_19", "s3_L1_10", "s1_L1_13")
    sus = [r for r in recs if r["unit"] in named]
    rest = [r for r in recs if r["unit"] not in named]
    if sus:
        print("\n" + "=" * 82)
        print("THE THREE UNEXPLAINED UNITS (A.11l / plan 9.4), individually")
        print("=" * 82)
        print("%-14s %5s %7s %7s %9s %9s %9s"
              % ("unit", "n", "ska", "r/m", "call.mean", "call.sd", "call.min"))
        for r in sorted(sus, key=lambda r: r["unit"]):
            print("%-14s %5d %7d %7.2f %9.3f %9.4f %9.3f"
                  % (r["unit"], r["n"], r["ska"], r["rm"], r["callable_mean"],
                     r["callable_sd"], r["callable_min"]))
        print("\n%-14s %5s %7s %7.2f %9.3f %9.4f %9.3f"
              % ("all others", "", "", statistics.mean(r["rm"] for r in rest),
                 statistics.mean(r["callable_mean"] for r in rest),
                 statistics.mean(r["callable_sd"] for r in rest),
                 statistics.mean(r["callable_min"] for r in rest)))
        hi = statistics.mean(r["callable_sd"] for r in sus)
        lo = statistics.mean(r["callable_sd"] for r in rest)
        print("\nthe three suspect units have %s callable-fraction variance than "
              "the rest\n(%.4f vs %.4f)." % ("HIGHER" if hi > lo else "LOWER", hi, lo))
        if hi <= lo:
            print("The hypothesis predicts HIGHER. It is not supported.")

    with open(OUT_TSV, "w") as fh:
        cols = ("unit", "n", "ska", "rm", "union", "callable_mean",
                "callable_sd", "callable_cv", "callable_min", "n_seq")
        fh.write("\t".join(cols) + "\n")
        for r in sorted(recs, key=lambda r: r["rm"]):
            fh.write("\t".join(("%.6f" % r[c]) if isinstance(r[c], float)
                               else str(r[c]) for c in cols) + "\n")
    print("\nwrote %s" % OUT_TSV)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    recs = collect(verbose=not args.quiet)
    if len(recs) < 5:
        print("too few units with alignments (%d)" % len(recs), file=sys.stderr)
        return 1
    report(recs)
    return 0


def selftest():
    import tempfile
    fails = []

    def chk(desc, got, want, tol=1e-9):
        ok = (abs(got - want) <= tol) if isinstance(want, float) else (got == want)
        print("%-56s %s" % (desc, "ok" if ok else "FAIL got=%r want=%r" % (got, want)))
        if not ok:
            fails.append(desc)

    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "aln.full.x.fa")
        with open(p, "w") as fh:
            fh.write(">a\nACGTACGTAC\n")          # 10/10 called
            fh.write(">b\nACGTNNNNNN\n")          # 4/10
            fh.write(">c\nACGT------\n")          # 4/10
        f = callable_fractions(p)
        chk("one fraction per record", len(f), 3)
        chk("fully called genome", f[0], 1.0, 1e-12)
        chk("N counts as missing", f[1], 0.4, 1e-12)
        chk("gap counts as missing", f[2], 0.4, 1e-12)

        # multi-line records must be joined, not treated as separate genomes
        p2 = os.path.join(td, "aln.full.y.fa")
        with open(p2, "w") as fh:
            fh.write(">a\nACGTA\nCGTAC\n>b\nNNNNN\nACGTA\n")
        f2 = callable_fractions(p2)
        chk("wrapped records counted once", len(f2), 2)
        chk("wrapped record fraction", f2[1], 0.5, 1e-12)

        # lower case is a CALLED base and must not be scored as missing
        p3 = os.path.join(td, "aln.full.z.fa")
        with open(p3, "w") as fh:
            fh.write(">a\nacgtACGT\n")
        chk("lower case is called", callable_fractions(p3)[0], 1.0, 1e-12)

        # lower-case n IS missing
        p4 = os.path.join(td, "aln.full.w.fa")
        with open(p4, "w") as fh:
            fh.write(">a\nnnnnACGT\n")
        chk("lower-case n is missing", callable_fractions(p4)[0], 0.5, 1e-12)

        chk("alignment discovered by prefix",
            os.path.basename(find_alignment(td)).startswith("aln.full."), True)

        # An empty file must yield no records rather than a spurious 0.0, which
        # would enter the regression as a real observation.
        p5 = os.path.join(td, "empty")
        os.makedirs(p5)
        pe = os.path.join(p5, "aln.full.e.fa")
        open(pe, "w").close()
        chk("empty alignment yields no records", callable_fractions(pe), [])

    print("\n%d test(s) failed" % len(fails) if fails else "\nall tests passed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
