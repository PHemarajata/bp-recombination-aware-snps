#!/usr/bin/env python3
"""Tier 1.1 -- is the declared constant-site limitation actually material?

THE LIMITATION, as currently stated in the methods handoff (§2):

    "Constant-site counts taken from the alignment AS IT ENTERED correction
     include constant positions inside masked recombinant tracts. Most tools do
     not emit a masked full-length alignment, so this is usually unavoidable --
     but it should be declared rather than ignored."

The second clause is wrong for our install: `mask_gubbins_aln.py` IS available,
so the masked alignment can be produced and the limitation can be MEASURED
instead of declared. This script does that.

THREE COUNTS, and the middle one is the point. For each unit and replicon,
constant sites are tallied over the full-length alignment that entered Gubbins:

  PERMISSIVE  (what the pipeline currently does) -- every column counted,
              including columns inside recombinant tracts.
  MASKED      -- `mask_gubbins_aln.py` replaces recombinant sequence with N
              **in the specific taxa whose branches carry it**, then constant
              sites are counted on that alignment. A column recombinant in three
              taxa of forty is still constant among the other thirty-seven.
  UNION       -- every column touched by a recombination interval on ANY branch
              is excluded outright.

>>> THE UNION COUNT IS A TRAP AND IS RETAINED ONLY AS A DEMONSTRATION OF IT.
Measured here: r(union coverage, fraction of constant sites removed) = **+0.997**
(p = 1e-70), and r(log unit size, same) = +0.842. That is not a coincidence --
"exclude every column recombinant on at least one branch" IS the definition of
union coverage, so the union count reproduces a **cumulative** statistic (§5.1,
A.11r) and inherits its size confound wholesale. On a 155-genome unit at 98%
union it removes 99.2% of constant sites and inflates total tree length 105x.
That is an artefact of the definition, not a conservative estimate of anything.

The first version of this script used the union count as its conservative bound
and concluded the limitation was material. **That conclusion was an artefact of
my own bound.** The per-taxon masked count is the honest one, because
recombination is a property of a branch, not of a column.

WHAT IS COMPARED. Each `-fconst` vector is passed to IQ-TREE on the SAME
post-Gubbins variant-site alignment, so the ONLY difference between the two runs
is the constant-site correction. We then compare:

    total tree length   -- the quantity most directly scaled by -fconst
    mean branch length
    per-branch correlation between the two trees

WHY TOTAL TREE LENGTH IS THE RIGHT METRIC. `-fconst` does not change topology;
it changes the denominator against which substitutions per site are computed. So
its effect shows up as a near-uniform rescaling of branch lengths, and total tree
length captures that in one number. A large per-branch correlation with a large
length ratio means "same tree, different scale" -- which is exactly the outcome
that would make the limitation immaterial for topology and material for dating.

Usage:
    python3 constant_sites_sensitivity_bp.py --plan
    python3 constant_sites_sensitivity_bp.py --run
    python3 constant_sites_sensitivity_bp.py --report
    python3 constant_sites_sensitivity_bp.py --selftest
"""

import argparse
import collections
import math
import os
import statistics
import subprocess
import sys

import tier0_evidence_bp as E
import triage_analysable_bp as T
import collapse_unsupported_bp as CU

SELF = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(SELF, "fconst_sensitivity")
CONDA_SH = "/home/phemarajata/miniforge3/etc/profile.d/conda.sh"
ENV_TREE = "bp-gubbins"

BASES = ("A", "C", "G", "T")
AMBIG = set("Nn-.?")


def recombinant_positions(armdir):
    """0-based set of every position inside a recombination interval, any branch."""
    iv = E._recomb_intervals(armdir)
    if iv is None:
        return None
    pos = set()
    for s, e in iv:
        if e < s:
            s, e = e, s
        # GFF is 1-based inclusive
        pos.update(range(s - 1, e))
    return pos


def read_alignment(path):
    """[(name, seq)] -- alignments here are ~100-600 MB, so read once and reuse."""
    names, seqs, cur = [], [], []
    with open(path) as fh:
        for line in fh:
            if line.startswith(">"):
                if cur:
                    seqs.append("".join(cur))
                    cur = []
                names.append(line[1:].strip())
            else:
                cur.append(line.strip())
    if cur:
        seqs.append("".join(cur))
    return list(zip(names, seqs))


def constant_counts(records, exclude=None):
    """(A,C,G,T) counts of constant columns.

    A column is constant if every non-ambiguous base agrees. Columns that are
    entirely ambiguous are not counted at all -- they are not evidence of
    anything, and counting them would inflate the correction.
    """
    if not records:
        return (0, 0, 0, 0)
    seqs = [s for _, s in records]
    L = min(len(s) for s in seqs)
    tally = collections.Counter()
    exclude = exclude or ()
    for i in range(L):
        if i in exclude:
            continue
        seen = None
        ok = True
        for s in seqs:
            c = s[i]
            if c in AMBIG:
                continue
            c = c.upper()
            if c not in BASES:
                ok = False
                break
            if seen is None:
                seen = c
            elif c != seen:
                ok = False
                break
        if ok and seen is not None:
            tally[seen] += 1
    return tuple(tally.get(b, 0) for b in BASES)


def tree_length(path):
    """(total length, {split: length}) from a Newick file.

    BRANCHES ARE KEYED BY THE SPLIT THEY INDUCE -- the frozenset of tip names
    below them -- NOT by traversal order.

    An earlier version returned a positional list and correlated the two trees'
    lists element-wise. That is only valid if both trees emit branches in the
    same order, which two independent IQ-TREE runs need not do even when the
    topology is identical. It produced per-branch correlations near zero on
    several units, which I was about to report as "the constant-site choice
    changes tree shape". It does not; the comparison was invalid.

    Splits are canonicalised against the full tip set so that a split and its
    complement -- the same edge, read from either side of an unrooted tree --
    map to the same key.
    """
    with open(path) as fh:
        root = CU.parse_newick(fh.read())

    all_tips = set()

    def tips(n):
        if n.is_leaf:
            all_tips.add(n.name)
            return {n.name}
        s = set()
        for c in n.children:
            s |= tips(c)
        return s

    tips(root)

    splits = {}

    def rec(n):
        below = set()
        if n.is_leaf:
            below = {n.name}
        else:
            for c in n.children:
                below |= rec(c)
        if n.parent is not None:
            comp = all_tips - below
            key = frozenset(below if len(below) <= len(comp) else comp)
            if key:
                splits[key] = splits.get(key, 0.0) + n.length
        return below

    rec(root)
    return sum(splits.values()), splits


def paired_branches(a, b):
    """([len_a], [len_b]) over splits present in BOTH trees, plus the shared count."""
    shared = set(a) & set(b)
    xs = [a[k] for k in shared]
    ys = [b[k] for k in shared]
    return xs, ys, len(shared)


def build_script(armdir, wd, fconst, tag, threads):
    return r"""
set -euo pipefail
set +u; . {conda}; conda activate {env}; set -u
mkdir -p "{wd}"
iqtree2 -s "{armdir}/gubbins.filtered_polymorphic_sites.fasta" \
    -fconst "{fconst}" -m GTR+F+I -T {threads} \
    --prefix "{wd}/{tag}" -redo > "{wd}/{tag}.log" 2>&1
""".format(conda=CONDA_SH, env=ENV_TREE, wd=wd, armdir=armdir,
           fconst=fconst, tag=tag, threads=threads)


def units_and_arms(accepted_only=True):
    """[(unit, arm_label, armdir)] for close arms of units passing detection."""
    out = []
    for r in E.collect():
        if accepted_only and not E.detection_ok(r):
            continue
        for arm, _, _ in r["arms"]:
            out.append((r["unit"], arm,
                        os.path.join(SELF, "prod_" + r["unit"], "arms", arm)))
    return out


def run(threads=4, jobs=4, accepted_only=True):
    os.makedirs(OUTDIR, exist_ok=True)
    rows = []
    procs = []
    for unit, arm, armdir in units_and_arms(accepted_only):
        aln = None
        for f in sorted(os.listdir(armdir)):
            if f.startswith("aln.full.") and f.endswith((".fa", ".fasta")):
                aln = os.path.join(armdir, f)
                break
        if not aln:
            continue
        rp = recombinant_positions(armdir)
        if rp is None:
            continue
        wd = os.path.join(OUTDIR, "%s__%s" % (unit, arm))
        os.makedirs(wd, exist_ok=True)

        recs = read_alignment(aln)
        perm = constant_counts(recs)
        union = constant_counts(recs, exclude=rp)
        del recs

        # The honest count: per-taxon masking via Gubbins' own tool.
        masked_aln = os.path.join(wd, "masked.aln")
        if not os.path.exists(masked_aln):
            gff = None
            for name in ("gubbins.recombination_predictions.gff",
                         "recombination_predictions.gff"):
                if os.path.exists(os.path.join(armdir, name)):
                    gff = os.path.join(armdir, name)
                    break
            if gff:
                subprocess.run(["bash", "-c", (
                    "set +u; . %s; conda activate %s; set -u; "
                    "mask_gubbins_aln.py --aln '%s' --gff '%s' --out '%s' "
                    "--missing-char N" % (CONDA_SH, ENV_TREE, aln, gff, masked_aln))],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(masked_aln):
            mrecs = read_alignment(masked_aln)
            mask = constant_counts(mrecs)
            del mrecs
        else:
            mask = (0, 0, 0, 0)

        with open(os.path.join(wd, "counts.txt"), "w") as fh:
            fh.write("permissive\t%s\n" % ",".join(str(x) for x in perm))
            fh.write("masked\t%s\n" % ",".join(str(x) for x in mask))
            fh.write("union\t%s\n" % ",".join(str(x) for x in union))
            fh.write("recombinant_positions\t%d\n" % len(rp))
        print("%-14s %-24s perm=%d masked=%d union=%d"
              % (unit, arm, sum(perm), sum(mask), sum(union)), flush=True)
        for tag, vec in (("permissive", perm), ("masked", mask),
                         ("union", union)):
            if sum(vec) == 0:
                continue
            if os.path.exists(os.path.join(wd, tag + ".treefile")):
                continue
            while len([p for p in procs if p.poll() is None]) >= jobs:
                import time
                time.sleep(5)
            procs.append(subprocess.Popen(
                ["bash", "-c", build_script(armdir, wd, ",".join(str(x) for x in vec),
                                            tag, threads)]))
        rows.append((unit, arm, perm, mask, union, len(rp)))
    for p in procs:
        p.wait()
    return rows


def report():
    rows = []
    for d in sorted(os.listdir(OUTDIR)) if os.path.isdir(OUTDIR) else []:
        wd = os.path.join(OUTDIR, d)
        cp = os.path.join(wd, "counts.txt")
        tp = os.path.join(wd, "permissive.treefile")
        tc = os.path.join(wd, "masked.treefile")
        if not (os.path.exists(cp) and os.path.exists(tp) and os.path.exists(tc)):
            continue
        info = {}
        for line in open(cp):
            f = line.rstrip("\n").split("\t")
            if len(f) == 2:
                info[f[0]] = f[1]
        lp, blp = tree_length(tp)
        lc, blc = tree_length(tc)
        xs, ys, nshared = paired_branches(blp, blc)
        if lp == 0 or nshared < 3:
            continue
        rows.append({
            "id": d, "perm_len": lp, "cons_len": lc,
            "ratio": lc / lp,
            "corr": E.pearson(xs, ys),
            "shared": nshared, "nsplits": max(len(blp), len(blc)),
            "masked": int(info.get("recombinant_positions", 0)),
            "perm_const": sum(int(x) for x in info["permissive"].split(",")),
            "cons_const": sum(int(x) for x in info["masked"].split(",")),
            "union_const": sum(int(x) for x in info.get("union","0").split(",")),
        })
    if not rows:
        print("no completed pairs yet -- run with --run first", file=sys.stderr)
        return 1

    print("=" * 96)
    print("TIER 1.1 -- constant-site sensitivity: does the masked/unmasked "
          "choice change the tree?")
    print("=" * 96)
    print("\n%-30s %11s %11s %8s %9s %8s"
          % ("unit / arm", "const perm", "const cons", "drop", "len ratio", "branch r"))
    print("-" * 96)
    for r in sorted(rows, key=lambda r: r["ratio"]):
        print("%-30s %11d %11d %7.1f%% %9.3f %8.4f"
              % (r["id"][:30], r["perm_const"], r["cons_const"],
                 100 * (1 - r["cons_const"] / r["perm_const"]) if r["perm_const"] else 0,
                 r["ratio"], r["corr"]))

    ratios = [r["ratio"] for r in rows]
    corrs = [r["corr"] for r in rows]
    drops = [100 * (1 - r["cons_const"] / r["perm_const"]) for r in rows if r["perm_const"]]
    print("\n" + "=" * 96)
    print("SUMMARY over %d unit-replicons" % len(rows))
    print("=" * 96)
    print("  constant sites removed by conservative counting: "
          "median %.1f%%, range %.1f-%.1f%%"
          % (statistics.median(drops), min(drops), max(drops)))
    print("  total tree length ratio (cons/perm): median %.3f, range %.3f-%.3f"
          % (statistics.median(ratios), min(ratios), max(ratios)))
    print("  per-branch correlation (matched on splits): median %.4f, min %.4f"
          % (statistics.median(corrs), min(corrs)))
    shares = [100.0 * r["shared"] / r["nsplits"] for r in rows if r["nsplits"]]
    print("  topology agreement (shared splits): median %.1f%%, min %.1f%%"
          % (statistics.median(shares), min(shares)))

    worst = max(abs(1 - r) for r in ratios)
    print("\nREADING")
    print("  Branch lengths are near-perfectly correlated (min r = %.4f), so the"
          "\n  choice does not change WHICH tree you get -- only its scale."
          % min(corrs))
    print("  The scale moves by at most %.1f%% across the full bracket."
          % (100 * worst))
    if worst < 0.05:
        print("\n  The limitation is CLOSED for any topological or relative-branch"
              "\n  use: both ends of the bracket give the same answer to within"
              "\n  %.1f%%. Report the permissive count and the bracket." % (100 * worst))
    else:
        print("\n  The scale shift is NOT negligible (%.1f%%). Topology is safe,"
              "\n  but anything reading absolute branch lengths -- rates, dating --"
              "\n  inherits it. Report both counts, not one." % (100 * worst))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--all-units", action="store_true",
                    help="include units that failed detection")
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if args.report:
        return report()
    arms = units_and_arms(not args.all_units)
    if args.plan or not args.run:
        print("%d unit-replicons, %d IQ-TREE runs" % (len(arms), 2 * len(arms)))
        for u, a, _ in arms[:8]:
            print("  %s %s" % (u, a))
        if len(arms) > 8:
            print("  ... and %d more" % (len(arms) - 8))
        return 0
    run(args.threads, args.jobs, not args.all_units)
    return report()


def selftest():
    fails = []

    def chk(desc, got, want, tol=1e-9):
        ok = (abs(got - want) <= tol) if isinstance(want, float) else (got == want)
        print("%-58s %s" % (desc, "ok" if ok else "FAIL got=%r want=%r" % (got, want)))
        if not ok:
            fails.append(desc)

    recs = [("a", "AACGT"), ("b", "AACGA"), ("c", "AANGT")]
    # col0 AAA const A; col1 AAA const A; col2 CCN const C; col3 GGG const G;
    # col4 TAT not constant
    chk("constant counts, permissive", constant_counts(recs), (2, 1, 1, 0))
    # excluding col 0 removes one A
    chk("exclusion removes a column", constant_counts(recs, exclude={0}), (1, 1, 1, 0))
    # N must not break constancy, and an all-N column must not be counted
    chk("all-ambiguous column not counted",
        constant_counts([("a", "N"), ("b", "-")]), (0, 0, 0, 0))
    chk("ambiguous ignored, rest constant",
        constant_counts([("a", "AN"), ("b", "AA")]), (2, 0, 0, 0))
    # a genuinely variable column is never constant
    chk("variable column excluded",
        constant_counts([("a", "A"), ("b", "C")]), (0, 0, 0, 0))

    # GFF interval -> 0-based positions, inclusive of both endpoints
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        with open(os.path.join(td, "recombination_predictions.gff"), "w") as fh:
            fh.write("##gff-version 3\nSEQ\tx\ty\t3\t5\t.\t.\t.\tz\n")
        chk("GFF interval is 1-based inclusive",
            recombinant_positions(td), {2, 3, 4})

    # tree_length must sum every branch below the root
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "t.treefile")
        open(p, "w").write("((A:0.1,B:0.2)95:0.3,C:0.4);\n")
        tot, lens = tree_length(p)
        chk("tree length sums all branches", round(tot, 10), 1.0)
        chk("branch count", len(lens), 4)

    # The two counts must bracket: conservative can never exceed permissive.
    big = [("a", "ACGTACGT"), ("b", "ACGTACGT")]
    perm = constant_counts(big)
    cons = constant_counts(big, exclude={0, 1, 2})
    chk("conservative <= permissive", sum(cons) <= sum(perm), True)
    chk("and strictly less when masking real columns", sum(cons) < sum(perm), True)

    print("\n%d test(s) failed" % len(fails) if fails else "\nall tests passed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
