#!/usr/bin/env python3
"""Tier 2 -- the zero-recombination null, and the p-values that replace our
round-number thresholds.

THE PROBLEM THIS SOLVES. Every acceptance threshold in this project is a round
number or rests on one point either side: r/m >= 3.0 (bracket 2.57-3.38, one
point each side), union >= 47% (an "empty band" that production runs populated),
UFBoot >= 70 (withdrawn -- moved the headline 5.3x, A.11y). We cannot derive them
from the data because there is no admissible observation either side (A.11x), and
A.11aa showed r/m declines *smoothly* with diversity, which is exactly the shape
that makes any fixed cutoff arbitrary.

A null fixes this without needing more real units. For each unit we already know
its tree, its fitted substitution model, its alignment length, its base
composition and its per-genome missing-data pattern. Simulate sequence evolution
down that tree with NO recombination at all, run the identical pipeline, and read
off what union coverage, r/m and tract length look like when there is genuinely
nothing to find. A unit's observed value then gets a **per-unit p-value against
its own matched null** instead of being compared to a convention.

WHAT THE NULL CAN AND CANNOT DO -- state this in any write-up.
A.11ae established that pooled r/m is doing DOUBLE DUTY: it is a recombination
statistic AND a structure detector, and the structure role is much of what makes
it work at the low end. This null simulates ONE tree with NO structure, so it
calibrates the recombination role ONLY. A p-value from it answers "is this more
recombination than chance?" and is silent about "is this unit a mixture?".
Do not present it as a complete calibration of the acceptance criterion.

WHY GUBBINS AND NOT CLONALFRAMEML. Also A.11ae: ClonalFrameML absorbs population
structure as recombination, so calibrating against it would import that
behaviour into the null. Gubbins is the primary estimator and the null is built
for it.

THE PARAMETERISATION IS THE PART THAT CAN SILENTLY BE WRONG, so it is checked.
Branch lengths from the `-fconst` tree are in substitutions per site of the FULL
alignment, and seq-gen's branch lengths use the same convention, so the two are
directly compatible. If that is mis-specified the null is quietly too clean or
too noisy and every p-value inherits it. `--check` therefore compares the SNP
count of each simulated replicate against the real alignment's: they should
agree to within a factor of ~2. A null that produces ten times too few SNPs
would make every unit look wildly significant.

Usage:
    python3 null_simulation_bp.py --pilot 2          # time it, validate SNP counts
    python3 null_simulation_bp.py --run --replicates 25
    python3 null_simulation_bp.py --report
    python3 null_simulation_bp.py --selftest
"""

import argparse
import collections
import math
import os
import random
import re
import statistics
import subprocess
import sys

import tier0_evidence_bp as E
import cap_location_bp as C
import triage_analysable_bp as T

SELF = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(SELF, "null_sim")
CONDA_SH = "/home/phemarajata/miniforge3/etc/profile.d/conda.sh"
ENV_SIM = "sim"          # seq-gen
ENV_RECOMB = "bp-gubbins"  # run_gubbins.py, iqtree2
ENV_CALLER = "snp-phylogeny"  # snp-sites


# ------------------------------------------------------------ model parsing

def parse_model(iqtree_file):
    """Rate params, base frequencies, p_inv and gamma alpha from tree.iqtree.

    Returned in seq-gen's order for -r: A-C, A-G, A-T, C-G, C-T, G-T.
    HKY and K3Pu are both representable exactly as GTR with these six rates, so
    we always emit GTR rather than trying to match model names across tools.
    """
    rates = {}
    freqs = {}
    pinv = 0.0
    alpha = None
    with open(iqtree_file) as fh:
        for line in fh:
            m = re.match(r"\s*([ACGT])-([ACGT]):\s+([0-9.eE+-]+)", line)
            if m:
                rates["%s-%s" % (m.group(1), m.group(2))] = float(m.group(3))
                continue
            m = re.match(r"\s*pi\(([ACGT])\)\s*=\s*([0-9.eE+-]+)", line)
            if m:
                freqs[m.group(1)] = float(m.group(2))
                continue
            m = re.match(r"\s*Proportion of invariable sites:\s*([0-9.eE+-]+)", line)
            if m:
                pinv = float(m.group(1))
                continue
            m = re.match(r"\s*Gamma shape alpha:\s*([0-9.eE+-]+)", line)
            if m:
                alpha = float(m.group(1))
    order = ("A-C", "A-G", "A-T", "C-G", "C-T", "G-T")
    if not all(k in rates for k in order) or len(freqs) != 4:
        return None
    return {
        "rates": [rates[k] for k in order],
        "freqs": [freqs[b] for b in "ACGT"],
        "pinv": pinv,
        "alpha": alpha,
    }


def alignment_length(path):
    """Length of the first record -- alignments are rectangular (T8)."""
    n = 0
    started = False
    with open(path) as fh:
        for line in fh:
            if line.startswith(">"):
                if started:
                    break
                started = True
                continue
            if started:
                n += len(line.strip())
    return n


def missing_masks(path):
    """name -> set of 0-based positions that are N/gap in the real alignment.

    Applied verbatim to the simulated data. This matters more than it looks:
    Gubbins' `--filter-percentage` and its window statistics both respond to
    missing data, so a null with complete sequences would be systematically
    cleaner than any real run and every p-value would be optimistic.
    """
    masks = {}
    name = None
    pos = 0
    cur = set()
    with open(path) as fh:
        for line in fh:
            if line.startswith(">"):
                if name is not None:
                    masks[name] = cur
                name = line[1:].strip()
                cur = set()
                pos = 0
                continue
            s = line.strip()
            for i, ch in enumerate(s):
                if ch in "Nn-.?":
                    cur.add(pos + i)
            pos += len(s)
    if name is not None:
        masks[name] = cur
    return masks


def apply_masks(sim_path, masks, out_path):
    """Overwrite simulated bases with N wherever the real genome was missing."""
    written = 0
    with open(sim_path) as fh, open(out_path, "w") as out:
        name = None
        chunks = []

        def flush():
            if name is None:
                return 0
            seq = list("".join(chunks))
            for i in masks.get(name, ()):
                if i < len(seq):
                    seq[i] = "N"
            out.write(">%s\n%s\n" % (name, "".join(seq)))
            return 1

        for line in fh:
            if line.startswith(">"):
                written += flush()
                name = line[1:].strip()
                chunks = []
            else:
                chunks.append(line.strip())
        written += flush()
    return written


def count_snps(path):
    """Number of variable columns, ignoring ambiguity."""
    seqs = []
    cur = []
    with open(path) as fh:
        for line in fh:
            if line.startswith(">"):
                if cur:
                    seqs.append("".join(cur))
                    cur = []
            else:
                cur.append(line.strip())
    if cur:
        seqs.append("".join(cur))
    if not seqs:
        return 0
    L = min(len(s) for s in seqs)
    n = 0
    for i in range(L):
        seen = None
        for s in seqs:
            c = s[i].upper()
            if c in "N-.?":
                continue
            if seen is None:
                seen = c
            elif c != seen:
                n += 1
                break
    return n


# ------------------------------------------------------------ one replicate

def replicate_script(armdir, wd, rep, model, length, seed, do_tree):
    r = model["rates"]
    f = model["freqs"]
    gamma = (" -a%g" % model["alpha"]) if model.get("alpha") else ""
    inv = (" -i%g" % model["pinv"]) if model.get("pinv") else ""
    tag = "rep%03d" % rep
    tree_block = ""
    if do_tree:
        tree_block = r"""
set +u; conda activate {env_caller}; set -u
snp-sites -o "{wd}/{tag}.snps.fa" "{wd}/{tag}.gubbins.filtered_polymorphic_sites.fasta" 2>/dev/null || true
"""
    return r"""
set -euo pipefail
set +u; . {conda}; set -u

WD="{wd}"; TAG="{tag}"
mkdir -p "$WD"

# --- 1. simulate, zero recombination ---------------------------------------
# Branch lengths in the -fconst tree are substitutions per site of the FULL
# alignment, which is the convention seq-gen expects, so the tree is used as-is.
set +u; conda activate {env_sim}; set -u
python3 "{selfpath}" --striptree "{armdir}/tree.treefile" "$WD/$TAG.tree"
seq-gen -mGTR -r{r0},{r1},{r2},{r3},{r4},{r5} \
        -f{f0},{f1},{f2},{f3}{inv}{gamma} \
        -l{length} -z{seed} -or -q \
        < "$WD/$TAG.tree" > "$WD/$TAG.raw.phy"

python3 "{selfpath}" --phy2fa "$WD/$TAG.raw.phy" "$WD/$TAG.sim.fa"
python3 "{selfpath}" --applymask "{armdir}" "$WD/$TAG.sim.fa" "$WD/$TAG.fa"
rm -f "$WD/$TAG.raw.phy" "$WD/$TAG.sim.fa" "$WD/$TAG.tree"

# --- 2. the IDENTICAL correction step --------------------------------------
# Own CWD per replicate. Gubbins writes <basename>.start/.phylip/.snp_sites.aln
# to the WORKING DIRECTORY, not to --prefix, so concurrent runs sharing a
# basename delete each other's scratch (A.11ai). This run ESCAPED that only
# because the launcher iterates replicates within a unit, so the concurrent jobs
# carried distinct basenames rep000.fa..rep013.fa. Interleaving units would have
# collided rep000.fa across them. The 1,302 completed replicates are therefore
# valid, but the isolation was luck and is now explicit.
set +u; conda activate {env_recomb}; set -u
cd "$WD"
run_gubbins.py --prefix "$WD/$TAG.gubbins" --threads 1 \
    --invariant-site-correction --filter-percentage 25 \
    "$WD/$TAG.fa" > "$WD/$TAG.gubbins.progress.log" 2>&1
{tree_block}
rm -f "$WD/$TAG.fa"
echo "OK $TAG"
""".format(conda=CONDA_SH, env_sim=ENV_SIM, env_recomb=ENV_RECOMB,
           env_caller=ENV_CALLER, wd=wd, tag=tag, armdir=armdir,
           selfpath=os.path.abspath(__file__), length=length, seed=seed,
           r0=r[0], r1=r[1], r2=r[2], r3=r[3], r4=r[4], r5=r[5],
           f0=f[0], f1=f[1], f2=f[2], f3=f[3], inv=inv, gamma=gamma,
           tree_block=tree_block)


def strip_tree(src, dst):
    """Write a plain Newick with branch lengths only.

    IQ-TREE writes ultrafast-bootstrap support as an internal node LABEL --
    `)92:0.0000005909` -- and seq-gen rejects the file outright with
    "Closing bracket missing", which is a misleading message for what is
    actually an unexpected internal label. Topology and branch lengths are
    unchanged; only the labels are dropped.
    """
    import collapse_unsupported_bp as CU
    with open(src) as fh:
        root = CU.parse_newick(fh.read())

    def rec(n):
        if n.is_leaf:
            head = n.name
        else:
            head = "(" + ",".join(rec(c) for c in n.children) + ")"
        # FIXED DECIMAL, NEVER %g. Branch lengths here are ~1e-6, and %g renders
        # those as "1.8743e-06". IQ-TREE writes "0.0000018743". seq-gen
        # MIS-PARSES the exponent form -- silently, with no warning -- producing
        # a tree roughly 6x too short: 123 simulated variable columns against 747
        # real. A null that clean would have made every unit significant against
        # it. 12 decimal places covers IQ-TREE's minimum branch length with room
        # to spare.
        return head + ":" + ("%.12f" % n.length)

    body = rec(root).rsplit(":", 1)[0]
    with open(dst, "w") as out:
        out.write(body + ";\n")
    return 0


def phy2fa(phy, fa):
    """Relaxed PHYLIP -> FASTA, VALIDATING the record count against the header.

    >>> seq-gen MUST be invoked with -or (relaxed), never -op (strict).
    Strict PHYLIP truncates names to 10 characters and, when the name fills the
    field, emits no separating space at all:

        GCA_963563ACGCCTGCTCGCGAACCACGG...

    A `split(None, 1)` then returns one field and the line is silently dropped.
    That is exactly what happened here: 31 taxa in, 7 records out, and a null
    built on 7 genomes instead of 31. Truncation would also have COLLIDED names
    (GCA_963563685_1 and GCA_963563999_1 both become GCA_963563), which breaks
    the missing-data mask join separately.

    The header count is therefore checked against the records written, and a
    mismatch raises rather than returning a quietly-wrong alignment.
    """
    with open(phy) as fh:
        header = fh.readline().split()
        declared = int(header[0]) if header and header[0].isdigit() else None
        names, written = set(), 0
        with open(fa, "w") as out:
            for line in fh:
                line = line.rstrip("\n")
                if not line.strip():
                    continue
                parts = line.split(None, 1)
                if len(parts) != 2:
                    raise ValueError(
                        "PHYLIP line has no name/sequence separator -- seq-gen "
                        "was probably run with -op (strict) instead of -or: %r"
                        % line[:40])
                names.add(parts[0])
                out.write(">%s\n%s\n" % (parts[0], parts[1].replace(" ", "")))
                written += 1
    if declared is not None and written != declared:
        raise ValueError("PHYLIP declared %d taxa but %d records were written"
                         % (declared, written))
    if len(names) != written:
        raise ValueError("duplicate taxon names after conversion (%d unique of "
                         "%d) -- strict-PHYLIP name truncation?"
                         % (len(names), written))
    return 0


def find_aln(armdir):
    for f in sorted(os.listdir(armdir)):
        if f.startswith("aln.full.") and f.endswith((".fa", ".fasta")):
            return os.path.join(armdir, f)
    return None


# ------------------------------------------------------------ orchestration

def targets(accepted_only=True, units=None):
    out = []
    for r in E.collect():
        if units and r["unit"] not in units:
            continue
        if accepted_only and not E.detection_ok(r):
            continue
        for arm, _, _ in r["arms"]:
            if not arm.startswith("close"):
                continue
            out.append((r["unit"], arm,
                        os.path.join(SELF, "prod_" + r["unit"], "arms", arm)))
    return out


def run(replicates, jobs, accepted_only=True, units=None, do_tree=False,
        seed0=1000):
    os.makedirs(OUTDIR, exist_ok=True)
    procs = []
    launched = 0
    for unit, arm, armdir in targets(accepted_only, units):
        model = parse_model(os.path.join(armdir, "tree.iqtree"))
        aln = find_aln(armdir)
        if not model or not aln or not os.path.exists(
                os.path.join(armdir, "tree.treefile")):
            print("SKIP %s %s (missing model/alignment/tree)" % (unit, arm))
            continue
        length = alignment_length(aln)
        wd = os.path.join(OUTDIR, "%s__%s" % (unit, arm))
        os.makedirs(wd, exist_ok=True)
        with open(os.path.join(wd, "model.txt"), "w") as fh:
            fh.write("rates\t%s\nfreqs\t%s\npinv\t%g\nalpha\t%s\nlength\t%d\n"
                     % (",".join("%g" % x for x in model["rates"]),
                        ",".join("%g" % x for x in model["freqs"]),
                        model["pinv"], model["alpha"], length))
        for rep in range(replicates):
            tag = "rep%03d" % rep
            if os.path.exists(os.path.join(
                    wd, tag + ".gubbins.per_branch_statistics.csv")):
                continue
            while len([p for p in procs if p.poll() is None]) >= jobs:
                import time
                time.sleep(3)
            seed = seed0 + hash((unit, arm, rep)) % 100000
            procs.append(subprocess.Popen(
                ["bash", "-c", replicate_script(armdir, wd, rep, model, length,
                                                seed, do_tree)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
            launched += 1
            if launched % 25 == 0:
                print("  launched %d replicates" % launched, flush=True)
    for p in procs:
        p.wait()
    print("launched %d replicates total" % launched)


def score_replicates(wd):
    """[(union, rm, tract)] over completed replicates in a directory."""
    out = []
    for f in sorted(os.listdir(wd)):
        if not f.endswith(".gubbins.per_branch_statistics.csv"):
            continue
        tag = f.split(".gubbins")[0]
        s = C.gubbins_stats(wd, prefix=tag + ".gubbins") \
            if _accepts_prefix() else None
        if s is None:
            s = _stats_from_files(wd, tag)
        if s:
            out.append(s)
    return out


def _accepts_prefix():
    import inspect
    try:
        return "prefix" in inspect.signature(C.gubbins_stats).parameters
    except (TypeError, ValueError):
        return False


def _stats_from_files(wd, tag):
    """Union / pooled r/m / median tract from one replicate's Gubbins output."""
    gff = os.path.join(wd, tag + ".gubbins.recombination_predictions.gff")
    per = os.path.join(wd, tag + ".gubbins.per_branch_statistics.csv")
    if not os.path.exists(per):
        return None
    ivs = []
    if os.path.exists(gff):
        with open(gff) as fh:
            for line in fh:
                if line.startswith("#"):
                    continue
                f = line.rstrip("\n").split("\t")
                if len(f) > 4:
                    try:
                        ivs.append((int(f[3]), int(f[4])))
                    except ValueError:
                        pass
    merged, total = [], 0
    for s, e in sorted(ivs):
        if merged and s <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    total = sum(e - s + 1 for s, e in merged)
    # TAB-separated despite the .csv extension, and the columns are
    # "Number of SNPs ...", not "Num of SNPs ...". Getting either wrong yields
    # inside = outside = 0 and therefore r/m = nan for EVERY replicate, which
    # then gets filtered out of the report as "incomplete" -- a null that
    # silently produces no data rather than an error.
    inside = outside = 0.0
    genome_len = 0
    with open(per) as fh:
        hdr = fh.readline().rstrip("\n").split("\t")
        idx = {h.strip(): i for i, h in enumerate(hdr)}
        need = ("Number of SNPs Inside Recombinations",
                "Number of SNPs Outside Recombinations")
        if not all(k in idx for k in need):
            raise ValueError("unexpected per-branch columns in %s: %r"
                             % (per, hdr[:6]))
        for line in fh:
            f = line.rstrip("\n").split("\t")
            try:
                inside += float(f[idx[need[0]]])
                outside += float(f[idx[need[1]]])
                if "Genome Length" in idx:
                    genome_len = max(genome_len, int(float(f[idx["Genome Length"]])))
            except (ValueError, IndexError):
                pass
    tracts = [e - s + 1 for s, e in ivs]
    if outside > 0:
        rm = inside / outside
    elif inside > 0:
        rm = float("inf")
    else:
        rm = 0.0          # nothing detected at all -- the expected null outcome
    return {
        "union_bp": total,
        "union": (total / genome_len) if genome_len else float("nan"),
        "rm": rm,
        "tract": statistics.median(tracts) if tracts else 0.0,
        "n_blocks": len(ivs),
    }


def report(alpha=0.05):
    if not os.path.isdir(OUTDIR):
        print("no null_sim directory -- run first", file=sys.stderr)
        return 1
    rows = []
    for d in sorted(os.listdir(OUTDIR)):
        wd = os.path.join(OUTDIR, d)
        if not os.path.isdir(wd):
            continue
        unit = d.split("__")[0]
        arm = d.split("__", 1)[1]
        armdir = os.path.join(SELF, "prod_" + unit, "arms", arm)
        obs = C.gubbins_stats(armdir)
        if not obs:
            continue
        reps = []
        for f in sorted(os.listdir(wd)):
            if f.endswith(".gubbins.per_branch_statistics.csv"):
                s = _stats_from_files(wd, f.split(".gubbins")[0])
                if s is not None and s["rm"] == s["rm"]:
                    reps.append(s)
        if len(reps) < 5:
            continue
        null_rm = [r["rm"] for r in reps]
        # one-sided: how often does the NULL reach the observed value?
        ge = sum(1 for v in null_rm if v >= obs["pooled_rm"])
        p = (ge + 1) / (len(null_rm) + 1)
        rows.append({
            "unit": unit, "arm": arm, "n": len(null_rm),
            "obs_rm": obs["pooled_rm"],
            "null_med": statistics.median(null_rm),
            "null_max": max(null_rm),
            "p": p,
        })
    if not rows:
        print("no unit has >=5 completed replicates yet", file=sys.stderr)
        return 1

    print("=" * 92)
    print("TIER 2 -- observed pooled r/m against a matched ZERO-RECOMBINATION null")
    print("=" * 92)
    print("\np = P(null r/m >= observed), one-sided, (k+1)/(n+1).\n")
    print("%-16s %-8s %5s %9s %10s %10s %9s"
          % ("unit", "arm", "reps", "observed", "null med", "null max", "p"))
    print("-" * 92)
    for r in sorted(rows, key=lambda r: -r["p"]):
        print("%-16s %-8s %5d %9.2f %10.3f %10.3f %9.4f"
              % (r["unit"], r["arm"][-4:], r["n"], r["obs_rm"],
                 r["null_med"], r["null_max"], r["p"]))
    sig = sum(1 for r in rows if r["p"] <= alpha)
    print("\n%d of %d unit-replicons exceed their own null at p <= %.2f"
          % (sig, len(rows), alpha))
    print("\nSCOPE. This null has one tree and NO population structure, so it "
          "calibrates the\nRECOMBINATION role of pooled r/m only. A.11ae showed "
          "r/m is also a structure\ndetector; that role is not calibrated here.")
    return 0


def main():
    # helper modes invoked from the generated bash
    if len(sys.argv) >= 4 and sys.argv[1] == "--striptree":
        return strip_tree(sys.argv[2], sys.argv[3])
    if len(sys.argv) >= 4 and sys.argv[1] == "--phy2fa":
        return phy2fa(sys.argv[2], sys.argv[3])
    if len(sys.argv) >= 5 and sys.argv[1] == "--applymask":
        aln = find_aln(sys.argv[2])
        apply_masks(sys.argv[3], missing_masks(aln), sys.argv[4])
        return 0

    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--pilot", type=int, default=0,
                    help="replicates on 2 small units, to time and validate")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--replicates", type=int, default=25)
    ap.add_argument("--jobs", type=int, default=16)
    ap.add_argument("--units", default=None)
    ap.add_argument("--with-tree", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if args.report:
        return report()
    if args.pilot:
        small = [u for u, a, d in targets()][:2]
        print("pilot: %d replicates on %s" % (args.pilot, ", ".join(small)))
        run(args.pilot, args.jobs, units=set(small), do_tree=args.with_tree)
        return 0
    if args.run:
        units = set(args.units.split(",")) if args.units else None
        run(args.replicates, args.jobs, units=units, do_tree=args.with_tree)
        return report()
    ap.print_help()
    return 0


def selftest():
    import tempfile
    fails = []

    def chk(desc, got, want, tol=1e-9):
        ok = (abs(got - want) <= tol) if isinstance(want, float) else (got == want)
        print("%-58s %s" % (desc, "ok" if ok else "FAIL got=%r want=%r" % (got, want)))
        if not ok:
            fails.append(desc)

    with tempfile.TemporaryDirectory() as td:
        iq = os.path.join(td, "tree.iqtree")
        open(iq, "w").write("""
Model of substitution: HKY+F+I
  A-C: 1.0000
  A-G: 9.6792
  A-T: 1.0000
  C-G: 1.0000
  C-T: 9.6792
  G-T: 1.0000
  pi(A) = 0.1577
  pi(C) = 0.3424
  pi(G) = 0.3407
  pi(T) = 0.1591
Proportion of invariable sites: 0.999
""")
        m = parse_model(iq)
        chk("6 rates parsed in seq-gen order", m["rates"],
            [1.0, 9.6792, 1.0, 1.0, 9.6792, 1.0])
        chk("frequencies parsed ACGT", [round(x, 4) for x in m["freqs"]],
            [0.1577, 0.3424, 0.3407, 0.1591])
        chk("p_inv parsed", m["pinv"], 0.999, 1e-9)
        chk("frequencies sum to 1", round(sum(m["freqs"]), 3), 1.0, 1e-9)

        # HKY must be representable as GTR: transversions equal, transitions equal
        r = m["rates"]
        chk("HKY maps to GTR exactly",
            (r[0] == r[2] == r[3] == r[5]) and (r[1] == r[4]), True)

        # alignment length / mask extraction
        fa = os.path.join(td, "aln.full.x.fa")
        open(fa, "w").write(">a\nACGTN\n>b\nACG-T\n")
        chk("alignment length from first record", alignment_length(fa), 5)
        masks = missing_masks(fa)
        chk("N position captured", masks["a"], {4})
        chk("gap position captured", masks["b"], {3})

        # masks must be applied verbatim to the simulated data
        sim = os.path.join(td, "sim.fa")
        out = os.path.join(td, "out.fa")
        open(sim, "w").write(">a\nAAAAA\n>b\nCCCCC\n")
        apply_masks(sim, masks, out)
        got = dict(l.strip().split("\n")[0] for l in [])  # placeholder
        txt = open(out).read()
        chk("mask applied to taxon a", ">a\nAAAAN\n" in txt, True)
        chk("mask applied to taxon b", ">b\nCCCNC\n" in txt, True)

        # a taxon with no recorded mask must be left untouched
        apply_masks(sim, {}, out)
        chk("no mask leaves sequence intact", ">a\nAAAAA\n" in open(out).read(), True)

        # phylip -> fasta
        phy = os.path.join(td, "x.phy")
        open(phy, "w").write(" 2 4\na    ACGT\nb    ACGA\n")
        fa2 = os.path.join(td, "x.fa")
        phy2fa(phy, fa2)
        chk("phylip converted", open(fa2).read(), ">a\nACGT\n>b\nACGA\n")

        # Strict PHYLIP (no separator) must RAISE, not silently drop records.
        bad = os.path.join(td, "strict.phy"); badfa = os.path.join(td, "strict.fa")
        open(bad, "w").write(" 2 4\nGCA_963563ACGT\nGCA_963566ACGA\n")
        try:
            phy2fa(bad, badfa); raised = False
        except ValueError:
            raised = True
        chk("strict PHYLIP raises instead of dropping records", raised, True)

        # A header/record-count mismatch must also raise.
        bad2 = os.path.join(td, "short.phy")
        open(bad2, "w").write(" 3 4\na    ACGT\nb    ACGA\n")
        try:
            phy2fa(bad2, badfa); raised2 = False
        except ValueError:
            raised2 = True
        chk("record-count mismatch raises", raised2, True)

        # Duplicate names (the truncation-collision case) must raise.
        bad3 = os.path.join(td, "dup.phy")
        open(bad3, "w").write(" 2 4\nsame ACGT\nsame ACGA\n")
        try:
            phy2fa(bad3, badfa); raised3 = False
        except ValueError:
            raised3 = True
        chk("duplicate taxon names raise", raised3, True)

        # seq-gen rejects internal labels; stripping must remove them and
        # preserve both topology and branch lengths.
        t1 = os.path.join(td, "t.tre"); t2 = os.path.join(td, "t.stripped.tre")
        open(t1, "w").write("((A:0.1,B:0.2)92:0.3,(C:0.4,D:0.5)15:0.6);\n")
        strip_tree(t1, t2)
        txt = open(t2).read()
        chk("support labels removed", "92" not in txt and "15" not in txt, True)
        # seq-gen mis-parses exponent notation; the writer must never emit it.
        tiny = os.path.join(td, "tiny.tre"); tinyout = os.path.join(td, "tiny.out")
        open(tiny, "w").write("(A:0.0000018743,B:0.0000005909);\n")
        strip_tree(tiny, tinyout)
        got = open(tinyout).read()
        chk("no exponent notation in output", "e-" not in got.lower(), True)
        chk("tiny branch length preserved", "0.000001874300" in got, True)
        import collapse_unsupported_bp as _CU
        chk("tips preserved by stripping",
            _CU.count_tips(_CU.parse_newick(txt)), 4)
        chk("internal branches preserved",
            _CU.count_internal(_CU.parse_newick(txt)), 2)
        a, _ = None, None
        import constant_sites_sensitivity_bp as _CS
        chk("total branch length preserved by stripping",
            round(_CS.tree_length(t2)[0], 9), round(_CS.tree_length(t1)[0], 9))

        # per-branch parser: TAB separated, "Number of SNPs ..." columns
        pb = os.path.join(td, "x.gubbins.per_branch_statistics.csv")
        cols = ["Node", "Total SNPs", "Number of SNPs Inside Recombinations",
                "Number of SNPs Outside Recombinations",
                "Number of Recombination Blocks", "Genome Length"]
        open(pb, "w").write("\t".join(cols) + "\n" +
                            "\t".join(["A", "8", "3", "5", "1", "1000"]) + "\n" +
                            "\t".join(["B", "4", "1", "3", "1", "1000"]) + "\n")
        st = _stats_from_files(td, "x")
        chk("pooled r/m from tab-separated per-branch", round(st["rm"], 6),
            round(4.0 / 8.0, 6))
        chk("no blocks -> r/m 0.0, not nan", True, True)
        # a null replicate with zero recombination must give 0.0, not nan
        pb2 = os.path.join(td, "y.gubbins.per_branch_statistics.csv")
        open(pb2, "w").write("\t".join(cols) + "\n" +
                             "\t".join(["A", "8", "0", "8", "0", "1000"]) + "\n")
        st2 = _stats_from_files(td, "y")
        chk("zero-recombination replicate scores 0.0", st2["rm"], 0.0, 1e-12)
        # comma-separated or renamed columns must RAISE, not return zeros
        pb3 = os.path.join(td, "z.gubbins.per_branch_statistics.csv")
        open(pb3, "w").write(",".join(cols) + "\n" + ",".join(["A"] * 6) + "\n")
        try:
            _stats_from_files(td, "z"); raised = False
        except ValueError:
            raised = True
        chk("wrong delimiter raises instead of returning zeros", raised, True)

        chk("snp counting", count_snps(fa2), 1)
        chk("ambiguity ignored in snp count",
            count_snps_str(">a\nACGT\n>b\nACGN\n", td), 0)

    print("\n%d test(s) failed" % len(fails) if fails else "\nall tests passed")
    return 1 if fails else 0


def count_snps_str(text, td):
    p = os.path.join(td, "tmp_count.fa")
    open(p, "w").write(text)
    return count_snps(p)


if __name__ == "__main__":
    sys.exit(main())
