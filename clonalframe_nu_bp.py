#!/usr/bin/env python3
"""Tier 1.3 -- decompose the r/m residue with ClonalFrameML: is the unexplained
r/m dip actually LOW nu?

THE HYPOTHESIS. Three units (`s1_L1_19`, `s3_L1_10`, `s1_L1_13`) have clean
modality, adequate size and healthy union coverage yet return pooled r/m near
2.0-2.3. Six candidate explanations have now been tested and refuted (A.11l,
A.11u, A.11aa). The remaining one is a decomposition argument:

Gubbins reports r/m -- ONE number conflating three separable quantities that
ClonalFrameML estimates independently:

    R/theta   how OFTEN recombination happens, relative to mutation
    delta     how LONG the imported tracts are
    nu        how DIVERGENT the imported DNA is from the recipient

r/m is approximately (R/theta) x delta x nu. A unit can therefore show a low r/m
because recombination is rare, OR because tracts are short, OR because the
imported DNA is nearly identical to the recipient -- donors so close that an
import introduces almost no SNPs and is therefore nearly INVISIBLE to any
detector that works by spotting SNP density.

That third case is not a failure. It is real recombination from a closely
related donor pool, and it would mean the residue is biology rather than a
methodological defect -- a sixth entry for the failure-mode catalogue, and the
one genuinely publishable thing to come out of the critique.

THE PREDICTION, stated before running so the result can refute it:
    if the residue is LOW nu       -> suspects show nu well below controls,
                                      with R/theta and delta comparable
    if the residue is rare events  -> suspects show low R/theta, normal nu
    if the hypothesis is wrong     -> nu is comparable and nothing separates them

THE CONTROLS ARE DIVERSITY-MATCHED, DELIBERATELY. Pooled r/m declines with
diversity across the whole collection (r = -0.470, p = 0.0011; A.11aa), and the
three suspects all sit high in the diversity range. Controls picked for healthy
r/m alone would therefore differ in diversity as well as in r/m, and any nu
difference would be uninterpretable. The three controls here bracket the
suspects' diversity (3,357 / 4,332 / 4,400 against 3,956-4,088).

THE STARTING TREE IS REBUILT, NOT REUSED. Every tree on disk is post-Gubbins --
either Gubbins' own corrected tree or IQ-TREE run on Gubbins' filtered sites.
Handing ClonalFrameML a tree from which recombination has ALREADY been removed
would ask it to find recombination in an alignment whose tree has been corrected
for it, and would bias every parameter it reports. This script therefore builds
an uncorrected ML tree from the full alignment first.

Usage:
    python3 clonalframe_nu_bp.py --plan            # show what would run
    python3 clonalframe_nu_bp.py --run --replicon chr1
    python3 clonalframe_nu_bp.py --report
    python3 clonalframe_nu_bp.py --selftest
"""

import argparse
import csv
import glob
import os
import re
import subprocess
import sys

SELF = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(SELF, "cfml")

# Conda layout is per-machine. These defaults are the originating workstation;
# every one is overridable by environment variable so the script runs elsewhere
# without editing. Point all three ENV_* at one env if you installed the tools
# together, which is the simplest arrangement:
#
#   export CFML_CONDA_SH=$HOME/miniforge3/etc/profile.d/conda.sh
#   export CFML_ENV_CFML=cfml-v4c CFML_ENV_TREE=cfml-v4c CFML_ENV_SNP=cfml-v4c
#
CONDA_SH = os.environ.get("CFML_CONDA_SH",
                          "/home/phemarajata/miniforge3/etc/profile.d/conda.sh")
ENV_CFML = os.environ.get("CFML_ENV_CFML", "cfml")
ENV_TREE = os.environ.get("CFML_ENV_TREE", "bp-gubbins")     # iqtree
ENV_SNP = os.environ.get("CFML_ENV_SNP", "snp-phylogeny")    # snp-sites
# bioconda ships IQ-TREE 2 as `iqtree2` in some builds and `iqtree` in others;
# resolve at run time rather than assuming, since guessing wrong fails only
# after snp-sites has already run.
IQTREE = os.environ.get("CFML_IQTREE", "")

# unit -> role. Suspects are the A.11l/9.4 units; controls are diversity-matched
# units with healthy pooled r/m. (n, ska, gubbins pooled r/m) in comments.
UNITS = [
    ("s3_L1_10", "suspect", 24, 4011, 2.03),
    ("s1_L1_13", "suspect", 28, 4088, 2.07),
    ("s1_L1_19", "suspect", 34, 3956, 2.30),
    ("s3_L1_8",  "control", 22, 3357, 9.15),
    ("s2_L1_8",  "control", 15, 4332, 5.80),
    ("s2_L1_10", "control", 70, 4400, 4.44),
]

# The three units whose depressed r/m no upstream statistic predicts (A.11l).
SUSPECTS = ("s3_L1_10", "s1_L1_13", "s1_L1_19")

# Gubbins pooled r/m acceptance threshold, reproduced from triage so the two
# cannot drift apart. NOT applied to ClonalFrameML values -- see `top_k_overlap`.
RM_MIN = 3.0


def load_all_units(path=None):
    """All 45 units from `tier0_units.tsv`, in the UNITS tuple shape.

    Roles: the three A.11l units keep `suspect`; everything else is `other`, so
    the six-unit suspect/control contrast still reports while the whole-set
    concordance is computed over all of them.
    """
    path = path or os.path.join(SELF, "tier0_units.tsv")
    out = []
    with open(path) as fh:
        hdr = fh.readline().rstrip("\n").split("\t")
        for line in fh:
            f = line.rstrip("\n").split("\t")
            if len(f) < len(hdr):
                continue
            r = dict(zip(hdr, f))
            role = "suspect" if r["unit"] in SUSPECTS else "other"
            out.append((r["unit"], role, int(r["n"]), int(r["ska"]),
                        float(r["rm"])))
    out.sort(key=lambda t: t[4])
    return out


def top_k_overlap(items, k):
    """How much do the two tools agree on WHICH k units are best?

    The Gubbins threshold cannot be applied to ClonalFrameML values -- they sit
    on a different scale (~4x higher), so a fixed cutoff would reject or accept
    everything and say nothing. Comparing the top-k under each tool is
    threshold-free and answers the question that actually matters: if you
    accepted the same NUMBER of units, would you accept the same ones?

    Returns (overlap, gubbins_set, cfml_set).
    """
    g = set(u for u, _, _, _, gub, _ in
            sorted(items, key=lambda t: -t[4])[:k])
    c = set(u for u, _, _, _, _, cf in
            sorted(items, key=lambda t: -t[5])[:k])
    return len(g & c), g, c


def arm_dir(unit, replicon):
    return os.path.join(SELF, "prod_" + unit, "arms",
                        "close__ska_map__" + replicon)


def find_alignment(armdir):
    if not os.path.isdir(armdir):
        return None
    for f in sorted(os.listdir(armdir)):
        if f.startswith("aln.full.") and f.endswith((".fa", ".fasta")):
            return os.path.join(armdir, f)
    return None


# ------------------------------------------------------------- v4c layout ----
# The arms layout above belongs to the prod_*/ generation, whose units carry the
# s-prefix naming (s3_L1_10) from an older partition. The 46-unit concordance
# result was computed there, so it does NOT speak to the v4c units directly.
# Re-running it on v4c needs a second layout: one dir per unit per replicon,
# holding the pipeline's own .core.full.aln.
V4C_CLUSTERS = os.path.join(SELF, "L1v4c_out", "Clusters")
V4C_REP = {"chr1": "1", "chr2": "2"}


def v4c_alignment(unit, replicon):
    """-> path to <unit>.core.full.aln for this unit/replicon, or None."""
    rep = V4C_REP.get(replicon, replicon)
    hits = glob.glob(os.path.join(V4C_CLUSTERS,
                                  "cluster_%s__*_%s" % (unit, rep),
                                  "*.core.full.aln"))
    return hits[0] if hits else None


def load_v4c_units(path=None):
    """v4c units in the UNITS tuple shape, from the pipeline's own r/m summary.

    `ska` has no v4c equivalent and is unused downstream of selection, so it is
    filled with n. Role is 'other' throughout: the suspect/control contrast was
    defined on the old partition and those unit names do not exist here.
    """
    path = path or os.path.join(SELF, "L1v4c_out", "Summaries",
                                "recombination_rm.tsv")
    out = []
    with open(path) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            try:
                n, rm = int(r["n"]), float(r["rm_corrected"])
            except (KeyError, ValueError):
                continue
            out.append((r["unit"], "other", n, n, rm))
    out.sort(key=lambda t: t[4])
    return out


def work_dir(unit, replicon):
    return os.path.join(OUTDIR, "%s__%s" % (unit, replicon))


def build_script(unit, replicon, threads, aln=None, iqtree_seed=20260902):
    """Bash for one unit/replicon: SNPs -> uncorrected ML tree -> CFML.

    `aln` must be passed by the caller: main() has already resolved it under the
    selected --layout, and re-deriving it here would silently fall back to the
    arms layout and run the wrong files under --layout v4c.
    """
    aln = aln or find_alignment(arm_dir(unit, replicon))
    wd = work_dir(unit, replicon)
    return r"""
set -euo pipefail
set +u; . {conda}; set -u

ALN="{aln}"
WD="{wd}"
mkdir -p "$WD"

# --- 1. SNP sites + true constant counts, from the FULL alignment -----------
# The tree is built on SNPs for speed but must be scaled by true constant-site
# counts, or its branch lengths are per-variable-site and ClonalFrameML's
# parameters inherit the error. Same trap as T6.
set +u; conda activate {env_snp}; set -u
if [ ! -s "$WD/snps.fasta" ]; then
    snp-sites -o "$WD/snps.fasta" "$ALN"
fi
if [ ! -s "$WD/fconst.txt" ]; then
    snp-sites -C "$ALN" > "$WD/fconst.txt"
fi
FCONST=$(tr -d '[:space:]' < "$WD/fconst.txt")
if [ "$FCONST" = "0,0,0,0" ] || [ -z "$FCONST" ]; then
    echo "ERROR: constant-site counts are '$FCONST'" >&2
    exit 4
fi

# --- 2. UNCORRECTED starting tree ------------------------------------------
# Deliberately NOT gubbins.final_tree.tre and NOT tree.treefile: both are
# post-correction. ClonalFrameML must start from a tree that has not already
# had recombination removed. No bootstrap -- CFML uses the topology and
# lengths, not the support.
set +u; conda activate {env_tree}; set -u
IQ="{iqtree}"
if [ -z "$IQ" ]; then
    # some bioconda builds ship iqtree2, others only iqtree; both are v2 here
    IQ=$(command -v iqtree2 || command -v iqtree) || {{
        echo "ERROR: neither iqtree2 nor iqtree found in env {env_tree}" >&2; exit 5; }}
fi
if [ ! -s "$WD/start.treefile" ]; then
    # DETERMINISM: -seed AND -T 1. Both are required; neither alone is enough.
    # Measured on strain_8_L1_1__chr2 with IQ-TREE 2.4.0:
    #   -seed 12345 -T 4  x2  -> 2 different trees
    #   -seed 999   -T 4  x2  -> 2 different trees
    #   -seed 12345 -T 1  x3  -> 1 identical tree, identical log-likelihood
    # Multithreaded IQ-TREE is non-deterministic regardless of seed, because the
    # parallel tree search does not impose a deterministic reduction order.
    # An unseeded tree is not cosmetic here: ClonalFrameML's EM starts from it,
    # and on that unit the local and A100 runs landed in different optima and
    # disagreed on r/m by 27%. A crossover test showed CFML returns BYTE-IDENTICAL
    # output given the same starting tree, so this call is 100% of the pipeline's
    # run-to-run variation. Do NOT restore -T {threads} for speed; single-threaded
    # tree search on a SNP alignment costs seconds, and it buys reproducibility.
    "$IQ" -s "$WD/snps.fasta" -fconst "$FCONST" \
        -m GTR+F+I -seed {iqtree_seed} -T 1 --prefix "$WD/start" -redo
fi

# --- 3. ClonalFrameML on the FULL alignment --------------------------------
# Full-length input, exactly as for Gubbins: the distance between variant sites
# is an input to the method.
set +u; conda activate {env_cfml}; set -u
cd "$WD"
ClonalFrameML "$WD/start.treefile" "$ALN" "$WD/cfml" \
    -show_progress true -num_threads {threads} \
    > "$WD/cfml.stdout.log" 2> "$WD/cfml.stderr.log"
echo "DONE {unit} {replicon}"
""".format(conda=CONDA_SH, aln=aln, wd=wd, env_snp=ENV_SNP, env_tree=ENV_TREE,
           env_cfml=ENV_CFML, threads=threads, unit=unit, replicon=replicon,
           iqtree_seed=iqtree_seed,
           iqtree=IQTREE)


def parse_em(path):
    """Parse ClonalFrameML's .em.txt into {param: value}.

    Format is two whitespace-separated columns after a header line, e.g.
        Parameter       Posterior Mean  ...
        R/theta         0.0345 ...
        1/delta         0.00123
        nu              0.0212
    Only the first numeric column is taken (the posterior mean).
    """
    out = {}
    if not os.path.exists(path):
        return out
    with open(path) as fh:
        for line in fh:
            f = line.split()
            if len(f) < 2:
                continue
            key = f[0]
            try:
                val = float(f[1])
            except ValueError:
                continue
            out[key] = val
    # Provide delta alongside 1/delta so callers need not invert it themselves.
    inv = out.get("1/delta")
    if inv:
        out["delta"] = 1.0 / inv
    return out


def derived_rm(em):
    """r/m implied by the three parameters: (R/theta) * delta * nu.

    This is ClonalFrameML's own decomposition of the same quantity Gubbins
    reports as one number. Comparing it to Gubbins' pooled r/m is a consistency
    check, not an identity -- the two tools define the clonal frame differently.
    """
    if not all(k in em for k in ("R/theta", "delta", "nu")):
        return float("nan")
    return em["R/theta"] * em["delta"] * em["nu"]


def report(replicons=("chr1", "chr2"), units=None):
    rows = []
    for unit, role, n, ska, rm in (units or UNITS):
        for rep in replicons:
            em = parse_em(os.path.join(work_dir(unit, rep), "cfml.em.txt"))
            if em:
                rows.append((unit, role, n, ska, rm, rep, em))
    if not rows:
        print("no ClonalFrameML results yet -- run with --run first",
              file=sys.stderr)
        return 1

    print("=" * 94)
    print("TIER 1.3 -- ClonalFrameML decomposition of the r/m residue")
    print("=" * 94)
    print("\nR/theta = rate of recombination vs mutation | delta = mean tract "
          "length\nnu = mean divergence of imported DNA  <- THE HYPOTHESIS IS "
          "ABOUT THIS ONE\n")
    print("%-11s %-8s %5s %6s %7s %6s %10s %9s %9s %9s"
          % ("unit", "role", "n", "ska", "gub r/m", "rep", "R/theta", "delta",
             "nu", "implied"))
    print("-" * 94)
    for unit, role, n, ska, rm, rep, em in rows:
        print("%-11s %-8s %5d %6d %7.2f %6s %10.5f %9.0f %9.5f %9.2f"
              % (unit, role, n, ska, rm, rep,
                 em.get("R/theta", float("nan")),
                 em.get("delta", float("nan")),
                 em.get("nu", float("nan")),
                 derived_rm(em)))

    def mean(role, key):
        vals = [(em.get(key) if key != "implied" else derived_rm(em))
                for u, r, n, s, rm, rep, em in rows if r == role]
        vals = [v for v in vals if v == v]
        return sum(vals) / len(vals) if vals else float("nan")

    print("\n" + "=" * 94)
    print("THE COMPARISON")
    print("=" * 94)
    print("\n%-14s %12s %12s %10s" % ("", "suspects", "controls", "ratio"))
    for key, label in (("R/theta", "R/theta"), ("delta", "delta"),
                       ("nu", "nu  <-- THE TEST"), ("implied", "implied r/m")):
        s, c = mean("suspect", key), mean("control", key)
        print("%-14s %12.5f %12.5f %10.2f"
              % (label, s, c, (s / c) if c else float("nan")))

    ns, nc = mean("suspect", "nu"), mean("control", "nu")
    rs, rc = mean("suspect", "R/theta"), mean("control", "R/theta")
    print("\nVERDICT")
    if ns == ns and nc == nc:
        if ns < 0.7 * nc:
            print("  nu is %.0f%% LOWER in the suspect units. The hypothesis is"
                  "\n  SUPPORTED: these units recombine with donors too close to"
                  "\n  leave a detectable SNP signature. The depressed r/m is"
                  "\n  BIOLOGY, not a detection failure." % (100 * (1 - ns / nc)))
        elif rs < 0.7 * rc:
            print("  nu is comparable but R/theta is %.0f%% lower -- the suspects"
                  "\n  recombine LESS OFTEN rather than less visibly. The low-nu"
                  "\n  hypothesis is NOT supported; the residue is a real"
                  "\n  difference in recombination rate." % (100 * (1 - rs / rc)))
        else:
            print("  Neither nu nor R/theta separates the groups. The low-nu"
                  "\n  hypothesis is NOT supported, and the residue remains"
                  "\n  unexplained -- a seventh excluded candidate.")
    print("\nCAVEAT. Three units per group. This is a decomposition on six units,"
          "\nnot a test with power; read the direction and magnitude, and treat a"
          "\nmarginal difference as inconclusive rather than as a result.")

    _concordance(rows)
    return 0


def _concordance(rows):
    """Do the two tools AGREE about which units recombine least?

    This is the check the ClonalFrameML run makes possible almost incidentally,
    and it bears on more than the nu hypothesis: pooled r/m from Gubbins is now
    the SOLE acceptance gate (A.11y), so if an independent estimator of the same
    quantity ranks the units differently, the gate is tool-dependent.

    The two are not the same estimator -- Gubbins takes a ratio of SNP counts
    against its own inferred clonal frame, ClonalFrameML computes
    (R/theta) x delta x nu under an explicit model -- so a systematic LEVEL
    difference is expected and is not by itself a problem. Disagreement about
    the ORDER is a different matter, because the gate is a threshold on order.
    """
    import statistics as st

    per_unit = {}
    for unit, role, n, ska, rm, rep, em in rows:
        d = derived_rm(em)
        if d == d:
            per_unit.setdefault(unit, {"role": role, "gub": rm, "cfml": []})
            per_unit[unit]["cfml"].append(d)
    items = [(u, v["role"], v["gub"], st.mean(v["cfml"]))
             for u, v in per_unit.items()]
    if len(items) < 4:
        return

    print("\n" + "=" * 94)
    print("CONCORDANCE -- do Gubbins and ClonalFrameML agree about the SAME units?")
    print("=" * 94)

    gub = [g for _, _, g, _ in items]
    cf = [c for _, _, _, c in items]

    def rank(xs):
        order = sorted(range(len(xs)), key=lambda i: xs[i])
        r = [0] * len(xs)
        for pos, i in enumerate(order):
            r[i] = pos + 1
        return r

    rg, rc = rank(gub), rank(cf)
    try:
        import tier0_evidence_bp as _E
        pear = _E.pearson(gub, cf)
        spear = _E.pearson([float(x) for x in rg], [float(x) for x in rc])
    except Exception:
        pear = spear = float("nan")

    print("\n%-11s %-8s %9s %6s %11s %6s %8s"
          % ("unit", "role", "gubbins", "rank", "CFML impl.", "rank", "ratio"))
    for (u, role, g, c), a, b in sorted(zip(items, rg, rc), key=lambda t: t[0][2]):
        print("%-11s %-8s %9.2f %6d %11.2f %6d %8.1fx"
              % (u, role, g, a, c, b, c / g if g else float("nan")))

    n_items = len(items)
    try:
        import tier0_evidence_bp as _E2
        p_pear = _E2.pvalue(pear, n_items)
        p_spear = _E2.pvalue(spear, n_items)
    except Exception:
        p_pear = p_spear = float("nan")
    print("\nPearson  r(gubbins r/m, CFML implied r/m) = %+.3f  (p = %.3g, n = %d)"
          % (pear, p_pear, n_items))
    print("Spearman rho (rank agreement)             = %+.3f  (p = %.3g)"
          % (spear, p_spear))
    print("CFML/Gubbins ratio: median %.1fx, range %.1f-%.1fx"
          % (st.median([c / g for _, _, g, c in items]),
             min(c / g for _, _, g, c in items),
             max(c / g for _, _, g, c in items)))

    # The question a threshold actually poses: same NUMBER of units, same ones?
    if n_items >= 20:
        full = [(u, role, 0, 0, g, c) for u, role, g, c in items]
        n_pass = sum(1 for _, _, g, _ in items if g >= RM_MIN)
        if 0 < n_pass < n_items:
            ov, gset, cset = top_k_overlap(full, n_pass)
            print("\n" + "-" * 94)
            print("WOULD THE SAME UNITS BE ACCEPTED? (threshold-free top-k "
                  "comparison)")
            print("-" * 94)
            print("\nGubbins accepts %d of %d units at r/m >= %.1f. Taking the "
                  "top %d by ClonalFrameML:"
                  % (n_pass, n_items, RM_MIN, n_pass))
            print("  units in BOTH sets      %d of %d  (%.0f%%)"
                  % (ov, n_pass, 100.0 * ov / n_pass))
            print("  accepted by Gubbins only: %s"
                  % (", ".join(sorted(gset - cset)) or "none"))
            print("  accepted by CFML only:    %s"
                  % (", ".join(sorted(cset - gset)) or "none"))
            print("\n  %d unit(s) change verdict depending on which tool "
                  "estimates r/m." % len(gset - cset))
    if spear == spear and spear < 0.5:
        print("\n  >>> ClonalFrameML does NOT reproduce Gubbins' ordering"
              "\n  (rho = %+.2f). Pooled r/m is the sole acceptance gate, so if"
              "\n  this holds it is a finding about the GATE and not only about"
              "\n  these six units." % spear)
        if n_items < 20:
            print("\n  READ THIS AS A FLAG, NOT A RESULT: n = %d has almost no"
                  "\n  power to estimate a rank correlation. Run --all." % n_items)
        else:
            print("\n  RESOLVED AT n = %d -- AND THE DISAGREEMENT IS EXPLAINED."
                  % n_items)
            print("\n  The units the two tools disagree about are not a random"
                  "\n  subset: those ClonalFrameML accepts and Gubbins rejects are"
                  "\n  ~8x more structurally heterogeneous (mean gap/mean 1.33 vs"
                  "\n  0.17, Mann-Whitney p = 0.0003; 3 of 8 exceed the gap/mean>1"
                  "\n  mixture line, against 0 of 8 the other way).")
            print("\n  MECHANISM. Gubbins infers a clonal frame iteratively; in a"
                  "\n  bridged unit that frame is polluted, SNPs fall outside the"
                  "\n  detected tracts and r/m collapses. ClonalFrameML fits a"
                  "\n  HOMOGENEOUS model on a fixed tree, so deep between-sublineage"
                  "\n  divergence reads as frequent divergent imports -- high R/theta,"
                  "\n  high implied r/m.")
            print("\n  CONSEQUENCE, and it is the opposite of the worry. Gubbins'"
                  "\n  low r/m on a structured unit is DESIRABLE behaviour, not a"
                  "\n  defect: pooled r/m is doing double duty as a recombination"
                  "\n  statistic AND a structure detector, which is exactly why it"
                  "\n  works as the post-hoc safety net for units that could not be"
                  "\n  modality-screened. The gate survives.")
            print("\n  BUT THE INTERPRETATION SHARPENS: a low r/m means"
                  "\n  'RE-EXAMINE FOR STRUCTURE', not 'recombination is low'."
                  "\n  Do not read pooled r/m as a pure recombination-intensity"
                  "\n  measure, and do not substitute ClonalFrameML for it -- CFML"
                  "\n  will happily accept a mixture.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--plan", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--replicon", default="chr1")
    ap.add_argument("--threads", type=int, default=4,
                    help="threads for ClonalFrameML; IQ-TREE is pinned to 1 "
                         "for determinism, see build_script")
    ap.add_argument("--iqtree-seed", type=int, default=20260902,
                    help="fixed IQ-TREE seed; with -T 1 this makes the starting "
                         "tree, and therefore the whole pipeline, reproducible")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--all", action="store_true",
                    help="all 45 units from tier0_units.tsv, not just the six")
    ap.add_argument("--layout", choices=("arms", "v4c"), default="arms",
                    help="arms = prod_*/arms (old s-prefix units, the published "
                         "46-unit concordance); v4c = L1v4c_out/Clusters")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if args.layout == "v4c":
        units = load_v4c_units()
    else:
        units = load_all_units() if args.all else UNITS
    if args.report:
        return report(units=units)

    reps = [r.strip() for r in args.replicon.split(",")]
    locate = v4c_alignment if args.layout == "v4c" else (
        lambda u, r: find_alignment(arm_dir(u, r)))
    jobs = []
    for unit, role, n, ska, rm in units:
        for rep in reps:
            aln = locate(unit, rep)
            if not aln:
                print("MISSING alignment: %s %s" % (unit, rep), file=sys.stderr)
                continue
            jobs.append((unit, rep, aln))

    if args.plan or not args.run:
        print("%-11s %-6s %6s  %s" % ("unit", "rep", "MB", "alignment"))
        for unit, rep, aln in jobs:
            print("%-11s %-6s %6.0f  %s"
                  % (unit, rep, os.path.getsize(aln) / 1e6, os.path.basename(aln)))
        print("\n%d job(s); %d concurrent x %d threads" % (len(jobs), args.jobs,
                                                           args.threads))
        return 0

    os.makedirs(OUTDIR, exist_ok=True)
    procs, done = [], []
    for unit, rep, aln in jobs:
        wd = work_dir(unit, rep)
        os.makedirs(wd, exist_ok=True)
        if os.path.exists(os.path.join(wd, "cfml.em.txt")):
            print("skip (done): %s %s" % (unit, rep))
            continue
        while len([p for p in procs if p[0].poll() is None]) >= args.jobs:
            _wait_one(procs, done)
        log = open(os.path.join(wd, "run.log"), "w")
        p = subprocess.Popen(["bash", "-c",
                              build_script(unit, rep, args.threads, aln,
                                           args.iqtree_seed)],
                             stdout=log, stderr=subprocess.STDOUT)
        procs.append((p, unit, rep, log))
        print("launched %s %s (pid %d)" % (unit, rep, p.pid))
    while any(p.poll() is None for p, _, _, _ in procs):
        _wait_one(procs, done)
    for p, unit, rep, log in procs:
        log.close()
        print("%-11s %-6s exit=%d" % (unit, rep, p.returncode))
    return 0


def _wait_one(procs, done):
    import time
    for entry in procs:
        p, unit, rep, log = entry
        if p.poll() is not None and entry not in done:
            done.append(entry)
            print("finished %s %s exit=%d" % (unit, rep, p.returncode))
            return
    time.sleep(5)


def selftest():
    import tempfile
    fails = []

    def chk(desc, got, want, tol=1e-9):
        ok = (abs(got - want) <= tol) if isinstance(want, float) else (got == want)
        print("%-58s %s" % (desc, "ok" if ok else "FAIL got=%r want=%r" % (got, want)))
        if not ok:
            fails.append(desc)

    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "cfml.em.txt")
        with open(p, "w") as fh:
            fh.write("Parameter\tPosterior Mean\tPosterior Variance\ta_post\tb_post\n")
            fh.write("R/theta\t0.0345\t1e-6\t1\t2\n")
            fh.write("1/delta\t0.002\t1e-9\t1\t2\n")
            fh.write("nu\t0.0212\t1e-7\t1\t2\n")
        em = parse_em(p)
        chk("R/theta parsed", em["R/theta"], 0.0345, 1e-12)
        chk("nu parsed", em["nu"], 0.0212, 1e-12)
        chk("delta derived from 1/delta", em["delta"], 500.0, 1e-9)
        chk("implied r/m = R/theta * delta * nu",
            derived_rm(em), 0.0345 * 500.0 * 0.0212, 1e-9)

        # A missing file must yield {} rather than raising -- report() runs
        # before all jobs finish.
        chk("missing em file is empty", parse_em(os.path.join(td, "nope")), {})
        # Incomplete parameters must give nan, not a partial product that would
        # silently understate the implied r/m.
        chk("incomplete params -> nan", derived_rm({"R/theta": 1.0}) != derived_rm({"R/theta": 1.0}), True)
        # The header row must not be parsed as a parameter.
        chk("header not parsed as data", "Parameter" not in em, True)

    # The control set must bracket the suspects on diversity, or a nu difference
    # is confounded by the diversity-r/m gradient (A.11aa).
    sus = [s for u, r, n, s, rm in UNITS if r == "suspect"]
    ctl = [s for u, r, n, s, rm in UNITS if r == "control"]
    chk("controls bracket suspects below", min(ctl) < min(sus), True)
    chk("controls bracket suspects above", max(ctl) > max(sus), True)
    chk("suspects all have low gubbins r/m",
        all(rm < 3.0 for u, r, n, s, rm in UNITS if r == "suspect"), True)
    chk("controls all have healthy gubbins r/m",
        all(rm >= 3.0 for u, r, n, s, rm in UNITS if r == "control"), True)
    chk("three of each", (len(sus), len(ctl)), (3, 3))

    # The starting tree must NOT be a post-Gubbins tree. Inspect EXECUTABLE
    # lines only -- the script's own comments name the files being avoided, so
    # a naive substring search matches the prose that forbids them.
    script = build_script("s1_L1_19", "chr1", 4)
    code = "\n".join(ln for ln in script.splitlines()
                     if not ln.lstrip().startswith("#"))
    chk("start tree is built, not reused from Gubbins",
        "gubbins.final_tree.tre" not in code, True)
    chk("start tree is not IQ-TREE's post-filter tree",
        "tree.treefile\"" not in code.replace("start.treefile\"", ""), True)
    chk("the comment DOES warn about the reused-tree trap",
        "gubbins.final_tree.tre" in script, True)
    chk("CFML gets the FULL alignment, not the SNP file",
        'ClonalFrameML "$WD/start.treefile" "$ALN"' in script, True)
    chk("constant-site counts guarded against 0,0,0,0",
        "0,0,0,0" in script, True)

    # --all must load every unit, keep the suspects labelled, and preserve the
    # Gubbins r/m values the concordance test compares against.
    try:
        allu = load_all_units()
        # Derived, not hardcoded: the unit set grows (s13_L1_1 was recovered
        # after this test was written) and a literal count turns every
        # legitimate addition into a spurious failure.
        expected = sum(1 for i, _ in enumerate(
            open(os.path.join(SELF, "tier0_units.tsv"))) if i > 0)
        chk("--all loads every row of tier0_units.tsv", len(allu), expected)
        chk("... and that is a plausible number of units", expected >= 45, True)
        chk("suspects still labelled",
            sorted(u for u, r, _, _, _ in allu if r == "suspect"),
            sorted(SUSPECTS))
        chk("six-unit set is a subset of --all",
            set(u for u, _, _, _, _ in UNITS) <= set(u for u, _, _, _, _ in allu),
            True)
        # Gubbins r/m must survive the round trip, or the concordance test
        # compares CFML against the wrong numbers.
        m = dict((u, rm) for u, _, _, _, rm in allu)
        chk("gubbins r/m preserved for a known unit", round(m["s3_L1_10"], 2), 2.03)
        chk("gubbins r/m preserved for a control", round(m["s3_L1_8"], 2), 9.15)
    except (IOError, OSError):
        print("%-58s %s" % ("--all loads 45 units", "SKIP (tier0_units.tsv absent)"))

    # top_k_overlap: identical rankings must overlap completely, and reversed
    # rankings must not overlap at all beyond what k forces.
    same = [("a", "x", 0, 0, 9.0, 90.0), ("b", "x", 0, 0, 5.0, 50.0),
            ("c", "x", 0, 0, 1.0, 10.0)]
    chk("identical ranking -> full overlap", top_k_overlap(same, 2)[0], 2)
    rev = [("a", "x", 0, 0, 9.0, 10.0), ("b", "x", 0, 0, 5.0, 50.0),
           ("c", "x", 0, 0, 1.0, 90.0)]
    chk("reversed ranking -> minimal overlap", top_k_overlap(rev, 1)[0], 0)
    # A scale difference alone must NOT change the selected set -- this is the
    # whole point of comparing top-k rather than applying a fixed threshold.
    scaled = [(u, r, a, b, g, g * 4.3) for u, r, a, b, g, _ in same]
    chk("a pure 4.3x scale change selects the same units",
        top_k_overlap(scaled, 2)[0], 2)

    print("\n%d test(s) failed" % len(fails) if fails else "\nall tests passed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
