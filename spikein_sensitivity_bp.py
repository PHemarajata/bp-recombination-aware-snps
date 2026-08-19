#!/usr/bin/env python3
"""Detection sensitivity, measured by SPIKING KNOWN RECOMBINATION INTO REAL DATA.

WHY NOT SIMULATION -- WE TRIED, AND IT FAILED. The SimBac nu-slice (A.11ai) ran
80 replicates and produced 18 usable ones with no relationship to nu
(r = +0.389, p = 0.34; 100% failure at nu = 0.05 where detection should be
trivial). Gubbins simply cannot process SimBac output reliably: under its default
RAxML builder it failed on 79 of 80. The diagnosis is that simulated alignments
do not resemble real ones -- uniform base composition against our 68% GC, no
missing data against our heavily structured N patterns, no repeat content.

Note that the Tier 2 null (A.11ag) DID work, and the one thing it did
differently was apply each genome's real N mask verbatim. That is direct evidence
that resemblance to real data is what matters.

TREE BUILDER: IQ-TREE, NOT THE RAxML DEFAULT. Gubbins' RAxML/ASC step fails at
iteration 3-5 on SPIKED alignments ("Unable to fit model to data") while the SAME
alignment UNSPIKED completes in 66 s and this unit's production run succeeded. So
the failure follows the implants, not the data source -- which also means the
nu-slice failure (A.11ai) was probably NOT "simulated data is unlike real data".
The implants add only ~3% more SNPs and create no multiallelic sites (allele
profile inside a spiked tract: 2758 invariant / 10 biallelic, against 2760 / 8 in
the control), so the likely mechanism is iterative masking depleting the SNP
alignment until ASC cannot fit. UNCONFIRMED, but consistent with both runs.

IQ-TREE is justified by measurement, not convenience: on 12 real unit-replicons
the builders agree to median 2.3% on r/m (worst 15.0%), 0.3 points on union, and
0 of 12 acceptance verdicts change.

THIS DESIGN REMOVES THE SIMULATOR ENTIRELY. Take a real unit's real alignment --
real base composition, real missing data, real repeat structure, real
phylogeny -- and implant tracts of KNOWN position, KNOWN length and KNOWN
divergence into KNOWN genomes. Then ask what fraction Gubbins recovers.

THE DONOR IS EXACT BY CONSTRUCTION. nu is defined as the divergence of imported
DNA from the recipient, so an implant is made by taking the recipient's own
sequence over the tract and mutating each callable site with probability nu.
That gives imported DNA that is exactly nu-divergent -- no donor choice, no
coalescent, no assumptions.

THE CONTROL IS THE SAME ALIGNMENT UNSPIKED, and it is essential. Real alignments
already contain real recombination, so a block detected at an implant site might
have been detected anyway. Every condition is therefore run twice -- spiked and
unspiked -- and an implant counts as RECOVERED only if a block overlaps its
coordinates FOR THAT TAXON in the spiked run and not in the control. Gubbins'
GFF carries a `taxa=` attribute, so attribution is exact rather than positional.

WHAT IS MEASURED
    recovery(nu) = implants detected / implants placed
Recovery near 1 at our measured nu means detection is comfortable and our r/m
values are not deflated by donor similarity. Recovery collapsing near nu = 0.002
would mean a collection-wide sensitivity limit.

Usage:
    python3 spikein_sensitivity_bp.py --plan
    python3 spikein_sensitivity_bp.py --run --replicates 3
    python3 spikein_sensitivity_bp.py --report
    python3 spikein_sensitivity_bp.py --selftest
"""

import argparse
import collections
import os
import random
import re
import statistics
import subprocess
import sys

SELF = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(SELF, "spikein")
CONDA_SH = "/home/phemarajata/miniforge3/etc/profile.d/conda.sh"
ENV_RECOMB = "bp-gubbins"

# Base unit: real, moderate size, well-behaved, high r/m so the background is
# typical rather than exceptional.
BASE_UNIT = "s13_L1_1"
BASE_ARM = "close__ska_map__chr1"

TRACT = 5000              # our measured median tract length
IMPLANTS_PER_GENOME = 2
FRACTION_SPIKED = 0.4     # share of genomes receiving implants
NU_GRID = (0.0005, 0.001, 0.002, 0.005, 0.01)
NU_MEASURED = 0.002

BASES = "ACGT"
AMBIG = set("Nn-.?")


def armdir():
    return os.path.join(SELF, "prod_" + BASE_UNIT, "arms", BASE_ARM)


def find_aln(d=None):
    d = d or armdir()
    for f in sorted(os.listdir(d)):
        if f.startswith("aln.full.") and f.endswith((".fa", ".fasta")):
            return os.path.join(d, f)
    return None


def read_fasta(path):
    recs, name, cur = [], None, []
    with open(path) as fh:
        for line in fh:
            if line.startswith(">"):
                if name is not None:
                    recs.append([name, "".join(cur)])
                name = line[1:].strip()
                cur = []
            else:
                cur.append(line.strip())
    if name is not None:
        recs.append([name, "".join(cur)])
    return recs


def implant(recs, nu, seed, tract=TRACT, per_genome=IMPLANTS_PER_GENOME,
            frac=FRACTION_SPIKED):
    """Insert nu-divergent tracts. Returns (modified recs, [(taxon, s, e, nsub)]).

    Only CALLABLE sites are mutated -- an implant must not resurrect a position
    the genome does not actually call, or the implant would be detectable as a
    missing-data anomaly rather than as recombination.
    """
    rng = random.Random(seed)
    L = min(len(s) for _, s in recs)
    n_spike = max(1, int(round(len(recs) * frac)))
    chosen = rng.sample(range(len(recs)), n_spike)
    placed = []
    for i in chosen:
        name, seq = recs[i]
        seq = list(seq)
        for _ in range(per_genome):
            start = rng.randrange(0, max(1, L - tract))
            end = start + tract - 1
            nsub = 0
            for p in range(start, end + 1):
                c = seq[p]
                if c in AMBIG:
                    continue
                if rng.random() < nu:
                    alt = [b for b in BASES if b != c.upper()]
                    seq[p] = rng.choice(alt)
                    nsub += 1
            placed.append((name, start + 1, end + 1, nsub))   # 1-based
        recs[i][1] = "".join(seq)
    return recs, placed


def write_fasta(recs, path):
    with open(path, "w") as out:
        for name, seq in recs:
            out.write(">%s\n%s\n" % (name, seq))


def parse_gff(path):
    """[(start, end, {taxa})] from a Gubbins recombination GFF."""
    out = []
    if not os.path.exists(path):
        return out
    with open(path) as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) < 9:
                continue
            try:
                s, e = int(f[3]), int(f[4])
            except ValueError:
                continue
            m = re.search(r'taxa="([^"]*)"', f[8])
            taxa = set(m.group(1).split()) if m else set()
            out.append((s, e, taxa))
    return out


def recovered(placed, spiked_gff, control_gff, min_overlap=0.5):
    """How many implants are detected in the spiked run but NOT in the control.

    An implant counts as recovered when a detected block covers at least
    `min_overlap` of it AND lists the implanted taxon. Requiring taxon match is
    what makes this exact: a block at the right coordinates on a different branch
    is not a recovery of this implant.
    """
    def hit(gff, taxon, s, e):
        need = (e - s + 1) * min_overlap
        for gs, ge, taxa in gff:
            if taxon not in taxa:
                continue
            ov = min(e, ge) - max(s, gs) + 1
            if ov >= need:
                return True
        return False

    rec = 0
    already = 0
    for taxon, s, e, nsub in placed:
        in_ctrl = hit(control_gff, taxon, s, e)
        in_spk = hit(spiked_gff, taxon, s, e)
        if in_ctrl:
            already += 1
        elif in_spk:
            rec += 1
    return rec, already


def gubbins_script(aln, wd, threads=4):
    """Run Gubbins with the working directory as CWD.

    >>> THIS `cd` IS THE WHOLE FIX FOR A FAILURE THAT COST TWO EXPERIMENTS.
    Gubbins writes intermediate files -- `<basename>.start`, `<basename>.phylip`,
    `<basename>.snp_sites.aln` and others -- into the CURRENT WORKING DIRECTORY,
    not into `--prefix`. Every spiked replicate used the same alignment basename
    (`spiked.fa`), and all of them ran concurrently from the project root, so
    they overwrote and deleted each other's intermediates. The symptom is
    `FileNotFoundError: 'spiked.fa.start'` in one run because another finished
    and cleaned up.

    This explains BOTH previous failures and refutes both earlier diagnoses:
      - the nu-slice (A.11ai) gave all 80 replicates the basename `aln.fa`,
        which is why ~60-70% failed INDEPENDENTLY OF nu and why an isolated
        single run in /tmp succeeded;
      - it is not "simulated data is unlike real data", and not ASC/masking
        depletion.
    The unspiked control survived only because it uses the real alignment's
    unique filename. The tree-builder equivalence runs survived because each
    used a distinct real alignment path.
    """
    return """
set -euo pipefail
set +u; . {conda}; conda activate {env}; set -u
mkdir -p "{wd}"
cd "{wd}"
run_gubbins.py --prefix "{wd}/gubbins" --threads {threads} \\
    --tree-builder iqtree \\
    --invariant-site-correction --filter-percentage 25 \\
    "{aln}" > "{wd}/progress.log" 2>&1
echo OK
""".format(conda=CONDA_SH, env=ENV_RECOMB, wd=wd, aln=aln, threads=threads)


def run(replicates=3, jobs=3, threads=4):
    os.makedirs(OUTDIR, exist_ok=True)
    src = find_aln()
    if not src:
        print("no base alignment", file=sys.stderr)
        return 1
    base = read_fasta(src)
    print("base: %s %s, %d genomes, %d bp"
          % (BASE_UNIT, BASE_ARM, len(base), len(base[0][1])))

    jobsl = []
    # control: unspiked, one per replicate is unnecessary -- the alignment is
    # identical, so a single control run serves every condition.
    ctrl = os.path.join(OUTDIR, "control")
    if not os.path.exists(os.path.join(ctrl, "gubbins.recombination_predictions.gff")):
        os.makedirs(ctrl, exist_ok=True)
        jobsl.append((gubbins_script(src, ctrl, threads), "control"))

    for nu in NU_GRID:
        for rep in range(replicates):
            tag = "nu%g_rep%d" % (nu, rep)
            wd = os.path.join(OUTDIR, tag)
            if os.path.exists(os.path.join(
                    wd, "gubbins.recombination_predictions.gff")):
                continue
            os.makedirs(wd, exist_ok=True)
            recs = [[n, s] for n, s in base]     # deep-ish copy
            recs, placed = implant(recs, nu, seed=hash((nu, rep)) % 10**6)
            aln = os.path.join(wd, "spiked.fa")
            write_fasta(recs, aln)
            with open(os.path.join(wd, "implants.tsv"), "w") as fh:
                fh.write("taxon\tstart\tend\tsubs\n")
                for t, s, e, k in placed:
                    fh.write("%s\t%d\t%d\t%d\n" % (t, s, e, k))
            jobsl.append((gubbins_script(aln, wd, threads), tag))

    procs = []
    for script, tag in jobsl:
        while len([p for p in procs if p.poll() is None]) >= jobs:
            import time
            time.sleep(5)
        print("launched %s" % tag, flush=True)
        procs.append(subprocess.Popen(["bash", "-c", script],
                                      stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL))
    for p in procs:
        p.wait()
    print("all runs finished")
    return 0


def report():
    ctrl_gff = parse_gff(os.path.join(OUTDIR, "control",
                                      "gubbins.recombination_predictions.gff"))
    if not ctrl_gff:
        print("control run missing -- cannot score without it", file=sys.stderr)
        return 1
    by_nu = collections.defaultdict(list)
    for d in sorted(os.listdir(OUTDIR)):
        if not d.startswith("nu"):
            continue
        wd = os.path.join(OUTDIR, d)
        gff = os.path.join(wd, "gubbins.recombination_predictions.gff")
        imp = os.path.join(wd, "implants.tsv")
        if not (os.path.exists(gff) and os.path.exists(imp)):
            continue
        placed = []
        with open(imp) as fh:
            next(fh)
            for line in fh:
                f = line.rstrip("\n").split("\t")
                placed.append((f[0], int(f[1]), int(f[2]), int(f[3])))
        rec, already = recovered(placed, parse_gff(gff), ctrl_gff)
        scorable = len(placed) - already
        nu = float(d.split("_")[0][2:])
        by_nu[nu].append({
            "placed": len(placed), "already": already,
            "rec": rec, "scorable": scorable,
            "rate": (rec / scorable) if scorable else float("nan"),
            "subs": statistics.mean(p[3] for p in placed) if placed else 0,
        })
    if not by_nu:
        print("no scorable replicates yet", file=sys.stderr)
        return 1

    print("=" * 92)
    print("SPIKE-IN SENSITIVITY on REAL data -- known tracts, known divergence")
    print("=" * 92)
    print("\nBase: %s %s. Tract %d bp. An implant is RECOVERED if a Gubbins block"
          "\ncovers >=50%% of it FOR THAT TAXON in the spiked run and not in the "
          "control.\n" % (BASE_UNIT, BASE_ARM, TRACT))
    print("%-9s %5s %8s %10s %9s %10s %9s"
          % ("nu", "reps", "implants", "SNPs/tract", "pre-det", "recovered", "rate"))
    print("-" * 92)
    for nu in sorted(by_nu):
        v = by_nu[nu]
        rates = [x["rate"] for x in v if x["rate"] == x["rate"]]
        mark = "  <-- ours" if abs(nu - NU_MEASURED) < 1e-9 else ""
        print("%-9g %5d %8.0f %10.1f %9.0f %10.0f %8.2f%s"
              % (nu, len(v),
                 statistics.mean(x["placed"] for x in v),
                 statistics.mean(x["subs"] for x in v),
                 statistics.mean(x["already"] for x in v),
                 statistics.mean(x["rec"] for x in v),
                 statistics.mean(rates) if rates else float("nan"), mark))

    at = by_nu.get(NU_MEASURED)
    print("\nREADING")
    if at:
        r = statistics.mean(x["rate"] for x in at if x["rate"] == x["rate"])
        print("  At nu = %g -- the value A.11ab measured in EVERY unit -- Gubbins"
              "\n  recovers %.0f%% of implanted recombination." % (NU_MEASURED, 100 * r))
        if r >= 0.8:
            print("  Detection is comfortable at our operating point. Our r/m values"
                  "\n  are NOT systematically deflated by donor similarity.")
        elif r <= 0.5:
            print("  DETECTION IS POOR AT OUR OPERATING POINT. Every r/m we report is"
                  "\n  systematically low, by roughly %.1fx. This affects all units"
                  "\n  equally so it does not reorder them, but it changes what an"
                  "\n  r/m of 3 MEANS." % (1 / r if r else float("inf")))
        else:
            print("  Detection is partial (%.0f%%) at our operating point -- neither"
                  "\n  comfortable nor collapsed. Report r/m as a lower bound." % (100 * r))
    print("\n  'pre-det' counts implants landing where the control already detected"
          "\n  recombination; those are excluded from the denominator rather than"
          "\n  scored, since they cannot be attributed to the implant.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--replicates", type=int, default=3)
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--threads", type=int, default=4)
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if args.report:
        return report()
    if args.plan:
        src = find_aln()
        recs = read_fasta(src)
        n_sp = int(round(len(recs) * FRACTION_SPIKED))
        print("base %s %s: %d genomes, %d bp" % (BASE_UNIT, BASE_ARM,
                                                 len(recs), len(recs[0][1])))
        print("%d genomes spiked x %d implants = %d implants per replicate"
              % (n_sp, IMPLANTS_PER_GENOME, n_sp * IMPLANTS_PER_GENOME))
        print("%d nu values x %d replicates + 1 control = %d Gubbins runs"
              % (len(NU_GRID), args.replicates, len(NU_GRID) * args.replicates + 1))
        for nu in NU_GRID:
            print("   nu=%-8g expected ~%.0f SNPs per %d bp tract"
                  % (nu, nu * TRACT, TRACT))
        return 0
    if args.run:
        return run(args.replicates, args.jobs, args.threads)
    ap.print_help()
    return 0


def selftest():
    fails = []

    def chk(desc, got, want, tol=1e-9):
        ok = (abs(got - want) <= tol) if isinstance(want, float) else (got == want)
        print("%-58s %s" % (desc, "ok" if ok else "FAIL got=%r want=%r" % (got, want)))
        if not ok:
            fails.append(desc)

    # implant() must mutate at approximately nu, skip ambiguous sites, and
    # report the tract coordinates it actually used.
    recs = [["a", "ACGT" * 5000], ["b", "ACGT" * 5000], ["c", "N" * 20000]]
    out, placed = implant([r[:] for r in recs], nu=0.01, seed=1,
                          tract=1000, per_genome=1, frac=1.0)
    chk("one implant per genome", len(placed), 3)
    subs = [p[3] for p in placed if not p[0] == "c"]
    chk("substitution count near nu*tract", all(3 <= s <= 25 for s in subs), True)
    cs = [p[3] for p in placed if p[0] == "c"]
    chk("all-ambiguous genome gets zero substitutions", cs, [0])
    chk("coordinates are 1-based and tract-length wide",
        all(e - s + 1 == 1000 for _, s, e, _ in placed), True)

    # a nu of 0 must implant nothing -- the negative control of the design
    _, placed0 = implant([r[:] for r in recs], nu=0.0, seed=2,
                         tract=1000, per_genome=1, frac=1.0)
    chk("nu=0 makes no substitutions", sum(p[3] for p in placed0), 0)

    # recovery scoring: taxon must match, overlap must be sufficient
    gff_hit = [(1000, 6000, {"a"})]
    gff_wrongtaxon = [(1000, 6000, {"b"})]
    gff_small = [(1000, 1200, {"a"})]
    pl = [("a", 1000, 5999, 10)]
    chk("overlapping block for right taxon recovers",
        recovered(pl, gff_hit, [])[0], 1)
    chk("same block, wrong taxon does not",
        recovered(pl, gff_wrongtaxon, [])[0], 0)
    chk("insufficient overlap does not",
        recovered(pl, gff_small, [])[0], 0)
    # control subtraction: a block present in the CONTROL is not a recovery
    r, already = recovered(pl, gff_hit, gff_hit)
    chk("pre-existing detection is not counted as recovery", r, 0)
    chk("pre-existing detection is reported separately", already, 1)

    # GFF parsing must capture the taxa attribute
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "g.gff")
        open(p, "w").write('##gff-version 3\n'
                           'SEQ\tGUBBINS\tCDS\t100\t200\t0.0\t.\t0\t'
                           'node="X";taxa="s1 s2";snp_count="5";\n')
        g = parse_gff(p)
        chk("gff interval parsed", (g[0][0], g[0][1]), (100, 200))
        chk("gff taxa parsed", g[0][2], {"s1", "s2"})

    print("\n%d test(s) failed" % len(fails) if fails else "\nall tests passed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
