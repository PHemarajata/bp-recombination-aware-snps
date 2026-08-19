#!/usr/bin/env python3
"""The SimBac nu-slice: at the nu we actually measured, would we detect
recombination if it were there?

WHY THIS EXISTS, AND WHY IT IS NOT THE TIER 2 NULL. A.11ag ran 1,302
zero-recombination replicates and established that every detection we report is
real -- observed r/m sits 300-433x above anything the null ever produced. But a
null with no recombination can only bound FALSE POSITIVES. It is structurally
silent on SENSITIVITY: "would we have seen it if it were there?" That question
needs simulation WITH recombination at known parameters, which is what this does.

WHY THE nu AXIS SPECIFICALLY. A.11ab measured nu -- the divergence of imported
DNA -- at **0.0021-0.0024 in every unit**, varying less between units than
between replicons. That refuted low nu as an explanation for the unexplained r/m
residue. But it raised a question the comparison could not answer: nu is
uniformly ~0.002 everywhere, and we do not know whether that value sits
comfortably inside Gubbins' detection regime or near its cliff. If it is near
the cliff, that is a COLLECTION-WIDE sensitivity limit rather than a property of
any unit -- and it would mean our r/m values are systematically low by an unknown
factor.

At nu = 0.002 an imported tract differs from the recipient at ~1 site in 500. Our
median tract is ~5 kb, so a typical import carries only ~10 SNPs for Gubbins to
find. Whether 10 SNPs in 5 kb is comfortably detectable is exactly the question.

TREE BUILDER: IQ-TREE, NOT PRODUCTION'S RAxML -- AND THAT IS MEASURED, NOT
ASSUMED. Gubbins' default RAxML/ASC step fails on every SimBac alignment
("Unable to fit model to data"; 1 of 80 replicates produced output), while it
works on all 46 real units. Running the simulations under `--tree-builder iqtree`
therefore deviates from production, which a reviewer is entitled to challenge.
`treebuilder_equivalence_bp.py` answers that with data: on 12 real
unit-replicons spanning r/m 1.81-14.13, the two builders give
    r/m       median 2.3% deviation, worst 15.0%
    union     median 0.3 points, worst 1.5 points
    r         +0.989
    verdicts  0 of 12 change side of the r/m >= 3.0 acceptance line
The threshold acts on ORDER, and order is preserved. Quote the 15% worst case
alongside the median; do not present the builders as identical.

THE DESIGN IS A SLICE, NOT A GRID, and that is deliberate. Everything except nu
is held FIXED at our measured values -- sample size, genome length, mutation
rate, tract length, and the external recombination rate. The amount of true
recombination is therefore constant across the sweep, so any change in what
Gubbins recovers is pure detectability. A full R/theta x delta x nu grid would
cost far more and answer a question we did not ask.

WHAT IS MEASURED. SimBac's `-f` log gives the TRUE external recombinant
intervals, so detection efficiency is measured directly rather than inferred:

    true_cov      union of true recombinant intervals / genome length
    recovered_cov Gubbins' union coverage on the same data
    efficiency    recovered_cov / true_cov

Efficiency near 1 means detection is comfortable at that nu; efficiency
collapsing toward 0 locates the cliff.

Usage:
    python3 nu_slice_bp.py --calibrate      # match theta to our diversity
    python3 nu_slice_bp.py --sweep --replicates 10
    python3 nu_slice_bp.py --report
    python3 nu_slice_bp.py --selftest
"""

import argparse
import math
import os
import statistics
import subprocess
import sys

import null_simulation_bp as NS

SELF = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(SELF, "nu_slice")
CONDA_SH = "/home/phemarajata/miniforge3/etc/profile.d/conda.sh"
ENV_SIM = "sim"
ENV_RECOMB = "bp-gubbins"

# Held FIXED across the sweep, at our measured values.
#
# R_EXTERNAL WAS ORIGINALLY 0.0005 AND UNCALIBRATED -- the comment claimed
# otherwise. At that rate the simulation SATURATES: true recombinant union
# coverage 99.9%, against 64-70% in our real units. An efficiency curve measured
# in a saturated regime would not describe our operating point at all.
#
# Calibrated against true union coverage (single seed, so stochastic):
#     R=2e-5 -> 22%   R=3e-5 -> 38%   R=4e-5 -> 41%
#     R=5e-5 -> 75%   R=7e-5 -> 66%   R=1e-4 -> 82%
# 6e-5 sits in our 64-70% window. Mean simulated tract length across these runs
# is 4,715-5,290 bp against our measured ~5,000 -- an independent confirmation
# that the tract parameterisation is right.
N_ISOLATES = 30          # median size of an accepted unit
GENOME = 1000000         # 1 Mbp; our replicons are 3-4 Mbp, see --report note
TRACT = 5000             # measured median tract length, 5.0-6.9 kb
R_EXTERNAL = 0.00006     # external recombination rate -- CALIBRATED, see below
R_INTERNAL = 0.0         # zero, so ALL recombination has controlled divergence

# The measured value, and the swept range around it.
NU_MEASURED = 0.0021
NU_GRID = (0.0002, 0.0005, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05)

# Calibrated with EXTERNAL RECOMBINATION OFF so that mutation alone reproduces
# our observed diversity: measured relation is diversity ~= 0.53 * theta, and the
# target is 3.5e-4 per site (~2,500 mean pairwise SNPs / 7.2 Mbp), so theta
# ~= 6.6e-4.
#
# THE FIRST CALIBRATION WAS RUN WITH RECOMBINATION ON and looked flat -- 4.9e-3
# to 5.8e-3 across a 10x theta range -- because at nu = 0.0021 the imported
# material dominates diversity and theta is a minor contributor. That was
# correct behaviour, misread as an unresponsive parameter.
#
# WHAT ACTUALLY GOVERNS DETECTABILITY is the RATIO of imported divergence (nu) to
# background divergence (theta) -- the "recombination-import density approaching
# point-mutation density" tension of handoff §1. Our real units sit at
# nu = 0.0021 against ~3.5e-4 background, i.e. imports ~6x more divergent than
# the genome average, and this theta reproduces that ratio.
THETA = 0.00052
TARGET_DIVERSITY_PER_SITE = 3.5e-4


def simbac_cmd(nu, theta, seed, out_fa, ext_log, genome=GENOME, n=N_ISOLATES):
    return ("SimBac -N %d -T %g -R %g -r %g -e %d -D %d -m %g -M %g "
            "-B %d -s %d -o '%s' -f '%s'"
            % (n, theta, R_INTERNAL, R_EXTERNAL, TRACT, TRACT, nu, nu,
               genome, seed, out_fa, ext_log))


def run_bash(script, env=None):
    full = "set +u; . %s; %sset -u\n%s" % (
        CONDA_SH, ("conda activate %s; " % env) if env else "", script)
    return subprocess.run(["bash", "-c", full], capture_output=True, text=True)


def read_fasta(path):
    recs, name, cur = [], None, []
    with open(path) as fh:
        for line in fh:
            if line.startswith(">"):
                if name is not None:
                    recs.append((name, "".join(cur)))
                name = line[1:].strip()
                cur = []
            else:
                cur.append(line.strip())
    if name is not None:
        recs.append((name, "".join(cur)))
    return recs


def mean_pairwise(recs, max_pairs=200):
    """Mean pairwise differences per site, over a capped number of pairs."""
    seqs = [s for _, s in recs]
    if len(seqs) < 2:
        return 0.0
    L = min(len(s) for s in seqs)
    pairs = []
    for i in range(len(seqs)):
        for j in range(i + 1, len(seqs)):
            pairs.append((i, j))
    step = max(1, len(pairs) // max_pairs)
    pairs = pairs[::step]
    tot = 0.0
    for i, j in pairs:
        a, b = seqs[i], seqs[j]
        d = sum(1 for k in range(L) if a[k] != b[k] and a[k] in "ACGT" and b[k] in "ACGT")
        tot += d / L
    return tot / len(pairs)


def union_fraction(intervals, genome):
    """Merged interval coverage as a fraction of a CIRCULAR genome.

    >>> SimBac simulates a circular chromosome, so an interval that crosses the
    origin is recorded with start > end -- e.g. (995000, 3000) means "from
    995000 to the end, plus 1 to 3000", a 8,001 bp tract.

    An earlier version "handled" that by swapping the endpoints, which yields
    (3000, 995000) -- the COMPLEMENT, 992,001 bp. Every wrap-around tract was
    therefore counted as almost the whole genome, inflating true coverage and
    producing a negative mean tract length (the tell that exposed it). The
    selftest asserted the swapping behaviour, so it encoded the bug as correct.

    Wrapped intervals are now split into two segments.
    """
    if not intervals:
        return 0.0
    spans = []
    for s, e in intervals:
        if s <= e:
            spans.append((s, e))
        else:
            spans.append((s, genome))
            spans.append((1, e))
    merged = []
    for s, e in sorted(spans):
        if merged and s <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    return sum(e - s + 1 for s, e in merged) / float(genome)


def mean_tract(intervals, genome):
    """Mean tract length, splitting wrapped intervals. Never negative."""
    if not intervals:
        return 0.0
    tot = 0
    for s, e in intervals:
        tot += (e - s + 1) if s <= e else ((genome - s + 1) + e)
    return float(tot) / len(intervals)


def read_ext_log(path):
    """[(start, end)] of TRUE external recombinant intervals."""
    out = []
    if not os.path.exists(path):
        return out
    with open(path) as fh:
        first = fh.readline()
        if first and not first[0].isdigit():
            pass  # header
        else:
            f = first.split()
            if len(f) >= 2:
                out.append((int(f[0]), int(f[1])))
        for line in fh:
            f = line.split()
            if len(f) >= 2:
                try:
                    out.append((int(f[0]), int(f[1])))
                except ValueError:
                    pass
    return out



def rename_and_check(src, dst):
    """Prefix SimBac's numeric taxon names, and ASSERT the alignment is
    rectangular (handoff T8) before Gubbins ever sees it.

    >>> SimBac names taxa "0", "1", ... "29". Gubbins ACCEPTS that input, filters
    it, calls SNPs, and then dies at iteration 1 inside its own
    `get_alignment_length()` with "Sequences must all be the same length" --
    an error about the intermediate SNP alignment, not the input, and therefore
    deeply misleading. The input is perfectly rectangular; the names are the
    problem. Renaming to `taxon_N` fixes it outright (verified: same data, exit 0,
    5.6 s).

    The rectangularity assert is here because this project's own T8 says to make
    it every run, and I did not apply it to simulated input -- which is exactly
    how three hours were spent watching 80 replicates fail one at a time.
    """
    recs, name, cur = [], None, []
    with open(src) as fh:
        for line in fh:
            if line.startswith(">"):
                if name is not None:
                    recs.append((name, "".join(cur)))
                name = line[1:].strip()
                cur = []
            else:
                cur.append(line.strip())
    if name is not None:
        recs.append((name, "".join(cur)))
    if not recs:
        raise ValueError("no records in %s" % src)
    lens = set(len(s) for _, s in recs)
    if len(lens) != 1:
        raise ValueError("alignment is not rectangular: %d distinct lengths %r"
                         % (len(lens), sorted(lens)[:5]))
    with open(dst, "w") as out:
        for n, seq in recs:
            out.write(">taxon_%s\n%s\n" % (n, seq))
    return len(recs)


def calibrate(seeds=3):
    print("=" * 84)
    print("CALIBRATION -- pick theta so simulated diversity matches our units")
    print("=" * 84)
    print("\ntarget: %.2e mean pairwise differences per site "
          "(~2,500 SNPs / 7.2 Mbp)\n" % TARGET_DIVERSITY_PER_SITE)
    os.makedirs(OUTDIR, exist_ok=True)
    print("%-12s %16s %12s" % ("theta", "diversity/site", "ratio to target"))
    best = None
    for theta in (0.0001, 0.00025, 0.00035, 0.0005, 0.001):
        divs = []
        for s in range(seeds):
            fa = os.path.join(OUTDIR, "_cal.fa")
            lg = os.path.join(OUTDIR, "_cal.log")
            # calibrate on a shorter genome for speed; diversity is per-site
            # -r 0: isolate MUTATION. With external recombination on, imported
            # material dominates diversity and theta appears inert.
            cmd = simbac_cmd(NU_MEASURED, theta, 100 + s, fa, lg,
                             genome=200000).replace("-r %g" % R_EXTERNAL, "-r 0")
            r = run_bash(cmd, ENV_SIM)
            if r.returncode != 0 or not os.path.exists(fa):
                continue
            divs.append(mean_pairwise(read_fasta(fa), max_pairs=60))
        if not divs:
            continue
        d = statistics.mean(divs)
        ratio = d / TARGET_DIVERSITY_PER_SITE
        print("%-12g %16.3e %12.2f" % (theta, d, ratio))
        if best is None or abs(math.log(ratio)) < abs(math.log(best[1])):
            best = (theta, ratio)
    if best:
        print("\nclosest theta: %g (%.2fx target)" % best)
        print("THETA in this script is set to %g" % THETA)
    return 0


def sweep(replicates, jobs):
    os.makedirs(OUTDIR, exist_ok=True)
    procs = []
    for nu in NU_GRID:
        for rep in range(replicates):
            tag = "nu%g_rep%02d" % (nu, rep)
            wd = os.path.join(OUTDIR, tag)
            if os.path.exists(os.path.join(
                    wd, "gubbins.per_branch_statistics.csv")):
                continue
            os.makedirs(wd, exist_ok=True)
            # PAIRED DESIGN: the seed depends on the REPLICATE ONLY, not nu.
            # Verified: SimBac with a fixed seed produces a byte-identical ARG at
            # nu = 0.0002, 0.002 and 0.05 (181 intervals, 56.8% coverage in all
            # three), because nu governs mutation WITHIN recombinant intervals and
            # is applied after the genealogy is built.
            #
            # Replicate r therefore has the SAME true recombination events at
            # every nu, and only their VISIBILITY differs. The earlier
            # `4000 + int(nu*1e6) + rep` gave each nu a different ARG: true
            # coverage varied 55-83% ACROSS nu when it was supposed to be
            # constant, so any efficiency difference mixed detectability with
            # genealogy variation.
            #
            # It also makes the low-nu CRASHES interpretable: an identical ARG
            # that completes at high nu and fails at low nu has failed for a pure
            # nu reason, which is the cliff itself rather than missing data.
            seed = 4000 + rep
            script = """
set -euo pipefail
set +u; . {conda}; set -u
WD="{wd}"

set +u; conda activate {env_sim}; set -u
{sim}

python3 "{selfpath}" --rename "$WD/sim.fa" "$WD/aln.fa"

set +u; conda activate {env_recomb}; set -u
# Each run gets its OWN CWD. Gubbins writes intermediates (<basename>.start,
# .phylip, .snp_sites.aln) to the working directory, NOT to --prefix. Every
# replicate here uses the basename `aln.fa`, so without this cd they overwrite
# and delete one another's scratch under concurrency -- which is what caused
# ~60-70% of this sweep to fail, independently of nu, and was misdiagnosed
# twice as a simulator problem (A.11ai).
cd "$WD"
run_gubbins.py --prefix "$WD/gubbins" --threads 1 \\
    --tree-builder iqtree \\
    --invariant-site-correction --filter-percentage 25 \\
    "$WD/aln.fa" > "$WD/gubbins.progress.log" 2>&1 || true
rm -f "$WD/aln.fa"
echo OK
""".format(conda=CONDA_SH, wd=wd, env_sim=ENV_SIM, env_recomb=ENV_RECOMB,
           selfpath=os.path.abspath(__file__),
           sim=simbac_cmd(nu, THETA, seed,
                          os.path.join(wd, "sim.fa"),
                          os.path.join(wd, "true_ext.log")))
            while len([p for p in procs if p.poll() is None]) >= jobs:
                import time
                time.sleep(2)
            procs.append(subprocess.Popen(["bash", "-c", script],
                                          stdout=subprocess.DEVNULL,
                                          stderr=subprocess.DEVNULL))
    for p in procs:
        p.wait()
    print("sweep complete: %d nu values x %d replicates" % (len(NU_GRID), replicates))


def report():
    if not os.path.isdir(OUTDIR):
        print("run --sweep first", file=sys.stderr)
        return 1
    by_nu = {}
    for d in sorted(os.listdir(OUTDIR)):
        wd = os.path.join(OUTDIR, d)
        if not os.path.isdir(wd) or not d.startswith("nu"):
            continue
        try:
            nu = float(d.split("_")[0][2:])
        except ValueError:
            continue
        true_iv = read_ext_log(os.path.join(wd, "true_ext.log"))
        true_cov = union_fraction(true_iv, GENOME)
        try:
            st = NS._stats_from_files(wd, "gubbins")
        except (ValueError, OSError):
            st = None
        if st is None or true_cov <= 0:
            continue
        rec_cov = union_fraction(
            [(s, e) for s, e in _gff_intervals(wd)], GENOME)
        by_nu.setdefault(nu, []).append({
            "true_cov": true_cov, "rec_cov": rec_cov,
            "rm": st["rm"], "eff": rec_cov / true_cov if true_cov else 0.0,
            "blocks": st["n_blocks"], "tract": st["tract"],
        })
    if not by_nu:
        print("no completed replicates", file=sys.stderr)
        return 1

    print("=" * 92)
    print("THE nu-SLICE -- detection efficiency vs divergence of imported DNA")
    print("=" * 92)
    print("\nEverything except nu is fixed: N=%d, genome=%d, tract=%d, "
          "R_ext=%g, theta=%g.\nTrue recombination is therefore CONSTANT across "
          "rows; only detectability changes.\n"
          % (N_ISOLATES, GENOME, TRACT, R_EXTERNAL, THETA))
    print("%-10s %5s %11s %12s %12s %10s %9s"
          % ("nu", "reps", "true cov", "recovered", "efficiency", "r/m", "blocks"))
    print("-" * 92)
    for nu in sorted(by_nu):
        v = by_nu[nu]
        mark = "   <-- MEASURED" if abs(nu - 0.002) < 1e-9 else ""
        print("%-10g %5d %10.3f%% %11.3f%% %11.2f %10.3f %9.1f%s"
              % (nu, len(v),
                 100 * statistics.mean(x["true_cov"] for x in v),
                 100 * statistics.mean(x["rec_cov"] for x in v),
                 statistics.mean(x["eff"] for x in v),
                 statistics.mean(x["rm"] for x in v),
                 statistics.mean(x["blocks"] for x in v), mark))

    lo = [nu for nu in sorted(by_nu)
          if statistics.mean(x["eff"] for x in by_nu[nu]) < 0.5]
    at = [nu for nu in by_nu if abs(nu - 0.002) < 1e-9]
    print("\nREADING")
    if at:
        e = statistics.mean(x["eff"] for x in by_nu[at[0]])
        print("  At nu = 0.002 -- the value measured in EVERY unit (A.11ab) --"
              "\n  Gubbins recovers %.0f%% of the recombination that is truly there."
              % (100 * e))
        if e < 0.5:
            print("\n  THAT IS A COLLECTION-WIDE SENSITIVITY LIMIT. Our r/m values"
                  "\n  are systematically LOW by roughly %.1fx, and the acceptance"
                  "\n  threshold is being applied to a systematically deflated"
                  "\n  statistic. This affects every unit equally, so it does not"
                  "\n  change the ORDERING -- but it does change what an r/m of 3"
                  "\n  means." % (1 / e if e else float("inf")))
        else:
            print("\n  Detection is comfortable at our measured nu. The r/m values"
                  "\n  are not systematically deflated by donor similarity, and the"
                  "\n  unexplained residue cannot be attributed to a sensitivity"
                  "\n  limit at this nu.")
    if lo:
        print("\n  Efficiency falls below 50%% at nu <= %g." % max(lo))
        print("  Our measured nu (%g) sits %s that cliff."
              % (NU_MEASURED, "BELOW OR AT" if NU_MEASURED <= max(lo) else "ABOVE"))
    # --- the paired view, which is what the design supports -------------
    import collections
    eff, status = paired_report()
    complete = [r for r in eff if len(eff[r]) >= 2]
    if complete:
        nus = sorted({n for r in eff for n in eff[r]})
        print("\n" + "=" * 92)
        print("PAIRED VIEW -- same ARG within each row; only nu changes")
        print("=" * 92)
        print("\n%-6s %s" % ("rep", " ".join("%9g" % n for n in nus)))
        print("-" * 92)
        for r in sorted(complete):
            cells = []
            for n in nus:
                if eff[r].get(n) is not None and n in eff[r]:
                    cells.append("%9.2f" % eff[r][n])
                elif status[r].get(n) == "CRASH":
                    cells.append("    CRASH")
                else:
                    cells.append("        -")
            print("%-6d %s" % (r, " ".join(cells)))
        crashes = collections.Counter(n for r in status for n, v in status[r].items()
                                      if v == "CRASH")
        if crashes:
            print("\nCRASHES BY nu (Gubbins could not run; identical ARG "
                  "succeeded elsewhere):")
            for n in sorted(crashes):
                print("    nu=%-9g %d" % (n, crashes[n]))
            print("  A crash concentrated at LOW nu is the cliff expressing "
                  "itself as a\n  hard failure rather than as a low efficiency "
                  "score. Count it as\n  detection failure, not as missing data.")

    print("\nCAVEATS.")
    print("  Genome length is %d bp against 3-4 Mbp real replicons, and SimBac's"
          "\n  coalescent is not our collection's history. Read the SHAPE of the"
          "\n  curve and the location of the cliff, not absolute efficiency." % GENOME)
    print("  True coverage across replicates runs above the 64-70%% calibration"
          "\n  target (calibrated on one seed, run on ten); efficiency normalises"
          "\n  per replicate, so this shifts the regime slightly, not the shape.")
    print("  Tree builder is IQ-TREE, not production's RAxML; measured deviation"
          "\n  median 2.3%%, worst 15.0%%, 0 of 12 acceptance verdicts changed.")
    return 0


def paired_report():
    """Within-replicate comparison across nu -- the analysis the paired design
    supports, and a strictly stronger one than comparing per-nu means.

    Each replicate carries an IDENTICAL ARG at every nu (verified: byte-identical
    true-interval sets), so replicate r's efficiency at nu1 versus nu2 differs
    only by detectability. Averaging within nu and comparing the means throws
    that pairing away and reintroduces between-replicate variance -- the same
    cross-sectional-vs-paired distinction as handoff §6.5, where a size effect
    was invisible between units and obvious within a lineage.

    THREE OUTCOMES ARE DISTINGUISHED, because they are not the same thing:
        efficiency  Gubbins ran and recovered this fraction of true recombination
        0.0         Gubbins ran and recovered NOTHING
        CRASH       Gubbins could not run at all (e.g. no starting tree)
    A crash at low nu with an identical ARG that completes at high nu is itself
    evidence of the cliff, not missing data, so crashes are reported rather than
    silently dropped.
    """
    import collections
    if not os.path.isdir(OUTDIR):
        return {}
    eff = collections.defaultdict(dict)
    status = collections.defaultdict(dict)
    for d in sorted(os.listdir(OUTDIR)):
        wd = os.path.join(OUTDIR, d)
        if not os.path.isdir(wd) or not d.startswith("nu"):
            continue
        try:
            nu = float(d.split("_")[0][2:])
            rep = int(d.split("_rep")[1])
        except (ValueError, IndexError):
            continue
        true_iv = read_ext_log(os.path.join(wd, "true_ext.log"))
        true_cov = union_fraction(true_iv, GENOME)
        per = os.path.join(wd, "gubbins.per_branch_statistics.csv")
        if not os.path.exists(per):
            log = os.path.join(wd, "gubbins.progress.log")
            if os.path.exists(log):
                status[rep][nu] = "CRASH"
            continue
        rec_cov = union_fraction(_gff_intervals(wd), GENOME)
        if true_cov > 0:
            eff[rep][nu] = rec_cov / true_cov
            status[rep][nu] = "ok"
    return eff, status


def _gff_intervals(wd):
    for name in ("gubbins.recombination_predictions.gff",):
        p = os.path.join(wd, name)
        if not os.path.exists(p):
            return []
        out = []
        with open(p) as fh:
            for line in fh:
                if line.startswith("#"):
                    continue
                f = line.rstrip("\n").split("\t")
                if len(f) > 4:
                    try:
                        out.append((int(f[3]), int(f[4])))
                    except ValueError:
                        pass
        return out
    return []


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--replicates", type=int, default=10)
    ap.add_argument("--jobs", type=int, default=12)
    # Helper mode invoked from the generated bash. MUST be handled BEFORE
    # parse_args(): argparse rejects the unknown flag and exits 2, which under
    # `set -e` kills the replicate before Gubbins is ever reached -- 80 sim.fa
    # files written and not one progress log, with no error anywhere to see.
    if len(sys.argv) >= 4 and sys.argv[1] == "--rename":
        rename_and_check(sys.argv[2], sys.argv[3])
        return 0
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if args.calibrate:
        return calibrate()
    if args.sweep:
        sweep(args.replicates, args.jobs)
        return report()
    if args.report:
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

    import tempfile as _tf
    with _tf.TemporaryDirectory() as _td:
        a = os.path.join(_td, "a.fa"); b = os.path.join(_td, "b.fa")
        open(a, "w").write(">0\nACGT\n>1\nACGA\n")
        n = rename_and_check(a, b)
        chk("records renamed", n, 2)
        chk("numeric names prefixed", ">taxon_0" in open(b).read(), True)
        chk("no bare numeric name survives",
            "\n>0\n" not in open(b).read(), True)
        # T8: a ragged alignment must RAISE here, not fail inside Gubbins.
        c = os.path.join(_td, "c.fa")
        open(c, "w").write(">0\nACGT\n>1\nACG\n")
        try:
            rename_and_check(c, b); raised = False
        except ValueError:
            raised = True
        chk("ragged alignment raises (T8)", raised, True)

    chk("union of disjoint intervals",
        union_fraction([(1, 100), (201, 300)], 1000), 0.2, 1e-9)
    chk("overlapping intervals merged",
        union_fraction([(1, 100), (50, 150)], 1000), 0.15, 1e-9)
    chk("adjacent intervals merged",
        union_fraction([(1, 100), (101, 200)], 1000), 0.2, 1e-9)
    # CIRCULAR wrap: (995, 5) on a 1000 bp genome is 995..1000 plus 1..5 = 11 bp,
    # NOT the 991 bp complement that swapping would give.
    chk("wrapped interval split, not swapped",
        union_fraction([(995, 5)], 1000), 0.011, 1e-9)
    chk("wrapped tract length is positive",
        mean_tract([(995, 5)], 1000), 11.0, 1e-9)
    chk("unwrapped tract length unchanged",
        mean_tract([(1, 100)], 1000), 100.0, 1e-9)
    chk("wrap does not swallow the genome",
        union_fraction([(995, 5)], 1000) < 0.05, True)
    chk("empty gives zero", union_fraction([], 1000), 0.0, 1e-12)

    # nu MUST be the only thing that varies -- guard the command builder.
    a = simbac_cmd(0.001, THETA, 1, "a", "b")
    b = simbac_cmd(0.010, THETA, 1, "a", "b")
    da = [x for x in a.split() if x not in b.split()]
    chk("only nu differs between grid points",
        sorted(set(da)), sorted({"0.001"}))
    chk("internal recombination is zero", "-R 0" in a, True)
    # Derived, not hardcoded: R_EXTERNAL is a calibrated value that changes,
    # and a literal here turns every recalibration into a false failure.
    chk("external recombination is on", "-r %g" % R_EXTERNAL in a, True)
    chk("external recombination is nonzero", R_EXTERNAL > 0, True)
    chk("tract length matches our measurement", "-e 5000" in a, True)

    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "e.log")
        open(p, "w").write("Start\tEND\n10\t20\n30\t40\n")
        chk("header skipped in ext log", read_ext_log(p), [(10, 20), (30, 40)])
        p2 = os.path.join(td, "e2.log")
        open(p2, "w").write("10\t20\n")
        chk("headerless ext log read", read_ext_log(p2), [(10, 20)])

        fa = os.path.join(td, "x.fa")
        open(fa, "w").write(">a\nAAAA\n>b\nAAAC\n")
        chk("mean pairwise per site", mean_pairwise(read_fasta(fa)), 0.25, 1e-9)

    print("\n%d test(s) failed" % len(fails) if fails else "\nall tests passed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
