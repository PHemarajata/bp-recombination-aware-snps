#!/usr/bin/env bash
# run_manuscript_analyses.sh
#
# Produce every outstanding manuscript number for the v4c (88-unit) run.
#
# Run this on the machine that holds the run outputs. It does three things:
#   1. the phylogeny-geography association, which has never been run on v4c
#   2. the reference-branch correction, re-measured on v4c
#   3. a consolidated numbers report that fills the manuscript's [CONFIRM] gaps
#
# Everything is written to a dated directory. Nothing is overwritten in place.
#
# Usage:
#   ./run_manuscript_analyses.sh /path/to/run_root [outdir]
#
# where run_root contains Clusters/ and Summaries/, e.g. the A100 production
# output directory.

set -euo pipefail

RUN_ROOT="${1:?usage: $0 <run_root> [outdir]}"
OUT="${2:-manuscript_numbers_$(date +%Y-%m-%d)}"

CLUSTERS="$RUN_ROOT/Clusters"
SUMMARIES="$RUN_ROOT/Summaries"

# ---------------------------------------------------------------- inputs ----
# Set these to the real paths. They are deliberately not guessed: a wrong
# default is what produced the one silent mismatch this project has recorded.
ASSIGNMENTS="${ASSIGNMENTS:-}"      # per-genome TSV: sample_id, unit, country, bioproject
DIVERSITY="${DIVERSITY:-}"          # cluster_diversity_bp.py output for THIS partition
MASH_PHYLIP="${MASH_PHYLIP:-}"      # needed only if DIVERSITY must be regenerated
UNIT_COL="${UNIT_COL:-unit}"        # unit column name inside ASSIGNMENTS
STATS_DIR="${STATS_DIR:-}"          # *.per_branch_statistics.csv for THIS run
REF_AUDIT="${REF_AUDIT:-}"          # per-cluster reference audit TSV for THIS run

die() { echo "ABORT: $*" >&2; exit 2; }

[ -d "$CLUSTERS" ]  || die "no Clusters/ under $RUN_ROOT"
[ -d "$SUMMARIES" ] || die "no Summaries/ under $RUN_ROOT"
[ -n "$ASSIGNMENTS" ] || die "set ASSIGNMENTS=/path/to/L1v4c_ASSIGNMENTS.tsv"
[ -f "$ASSIGNMENTS" ] || die "no such file: $ASSIGNMENTS"

mkdir -p "$OUT"
echo "run root    : $RUN_ROOT"
echo "assignments : $ASSIGNMENTS"
echo "output      : $OUT"
echo

# --------------------------------------------------- 0. sanity, per-unit ----
# The project rule: check per-item values, never infer from a summary line.
n_tree_units=$(find "$CLUSTERS" -name '*.node_labelled.final_tree.tre' \
    | sed 's#.*/Clusters/##; s#/.*##' | sort -u | wc -l)
n_assign_units=$(awk -F'\t' -v want="$UNIT_COL" \
    'NR==1{for(i=1;i<=NF;i++) if($i==want) u=i; next} u && $u!="" {print $u}' \
    "$ASSIGNMENTS" | sort -u | wc -l)
echo "units with trees on disk : $n_tree_units"
echo "units in assignments     : $n_assign_units"
if [ "$n_tree_units" -ne "$n_assign_units" ]; then
    echo "  NOTE: these differ. The phylogeography step will abort and print" >&2
    echo "        exactly which units are on which side. That is intended." >&2
fi
echo

# -------------------------------------------- 1. diversity, if not given ----
if [ -z "$DIVERSITY" ]; then
    [ -n "$MASH_PHYLIP" ] || die "set DIVERSITY= or MASH_PHYLIP= so Gate 1 can be applied"
    DIVERSITY="$OUT/cluster_diversity_v4c.tsv"
    echo "== regenerating diversity from $MASH_PHYLIP"
    python3 cluster_diversity_bp.py \
        --phylip "$MASH_PHYLIP" \
        --membership "$ASSIGNMENTS" \
        --cluster-col "$UNIT_COL" \
        --out "$DIVERSITY" | tee "$OUT/cluster_diversity.log"
    echo
fi

# ------------------------------------------------ 2. reference branches -----
REFBRANCH_TABLE=""
if [ -n "$STATS_DIR" ] && [ -n "$REF_AUDIT" ]; then
    echo "== reference-branch correction, re-measured on this partition"
    echo "   All four inputs are named explicitly. That script no longer has"
    echo "   defaults, because every one of them pointed at the v1 run."
    REFBRANCH_TABLE="$OUT/RM_CORRECTED_v4c.tsv"
    python3 exclude_reference_branches_bp.py \
        --stats-dir "$STATS_DIR" \
        --clusters-out "$CLUSTERS" \
        --clusters "$ASSIGNMENTS" \
        --audit "$REF_AUDIT" \
        --out "$REFBRANCH_TABLE" 2>&1 | tee "$OUT/refbranch.log"
else
    echo "== reference-branch correction SKIPPED"
    echo "   Set STATS_DIR= and REF_AUDIT= to re-measure it on this partition."
    echo "   Until then the manuscript must keep citing the 82-unit figures and"
    echo "   must say so in text."
fi
echo

# ------------------------------------------------------ 3. phylogeography ---
echo "== phylogeny-geography association  (never yet run on this partition)"
echo "   Both --assignments and --trees are passed explicitly. Neither has a"
echo "   default, so the silent join that happened once cannot happen again."
python3 phylogeography_association_bp.py \
    --assignments "$ASSIGNMENTS" \
    --trees "$CLUSTERS" \
    --unit-col "$UNIT_COL" \
    --perms 1000 \
    --out "$OUT/PHYLOGEOGRAPHY_ASSOCIATION_v4c.tsv" \
    2>&1 | tee "$OUT/phylogeography.log"
echo

# ------------------------------------------------- 4. consolidated report ---
echo "== consolidated manuscript numbers"
RM_TABLE="$SUMMARIES/recombination_rm.tsv"
[ -n "$REFBRANCH_TABLE" ] && [ -f "$REFBRANCH_TABLE" ] && RM_TABLE="$REFBRANCH_TABLE"
[ -f "$RM_TABLE" ] || die "no r/m table found at $RM_TABLE"
echo "   r/m table: $RM_TABLE"

python3 manuscript_numbers_bp.py \
    --rm "$RM_TABLE" \
    --diversity "$DIVERSITY" \
    --assignments "$ASSIGNMENTS" \
    ${REFBRANCH_TABLE:+--refbranch "$REFBRANCH_TABLE"} \
    ${FIND_GENOMES:+--find-genomes "$FIND_GENOMES"} \
    2>&1 | tee "$OUT/MANUSCRIPT_NUMBERS.txt"

echo
echo "Done. Everything is under $OUT/"
echo
echo "Paste into the manuscript:"
echo "  Results 3  <- the r/m distribution table and THE REPORTED RESULT block"
echo "  Results 7  <- the reference-branch section"
echo "  Results 8  <- phylogeography.log, plus the composition section"
echo
echo "To re-identify the Americas unit across partitions, re-run with"
echo "  FIND_GENOMES='GCF_000959265,GCF_002111085,GCF_002110925,GCF_002111105,GCF_002111205,GCF_013265695,GCF_002111145'"
echo "Those are the seven genomes of the v3 unit strain_9_L1_7. Strain labels do"
echo "not transfer between PopPUNK fits, so they must be located by membership."
