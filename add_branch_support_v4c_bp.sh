#!/usr/bin/env bash
# Branch support for the REPORTED partition: 85 units / 170 replicon-units.
#
# WHY A SECOND SCRIPT rather than editing add_branch_support_bp.sh. That script
# documents a run that happened (2026-08-15, 164 replicon-units) and its log is
# the record of it. It also has two properties that make it wrong for the
# reported basis, and both are silent:
#
#   1. It reads $BASE/L1_out/Clusters -- an EARLIER run's output directory, not
#      L1v4c_out/. That is why it covered 164 replicon-units.
#   2. It globs the cluster directory. L1v4c_out/Clusters holds 176 dirs = 88
#      units x 2 replicons, because it is HYBRID: it contains both the reported
#      workstation partition (85 units) and A100-only units. Globbing it would
#      silently add units that are not in the frozen basis -- the same error that
#      corrupted two summary tables previously.
#
# So this script takes membership from FINAL_PARTITION.tsv and refuses to run if
# the unit set does not come out at exactly 85 / 170.
#
# Production ran with iqtree_support=false (conf/params.config), so no tree in
# the reported analysis carries UFBoot or SH-aLRT values. This recomputes each
# unit's ML tree with -bb/-alrt from the PUBLISHED filtered alignment, reusing
# the unit's own ASC preflight decision (model, and -fconst only where the
# preflight chose the fconst fallback), so topology is computed the same way and
# only support values are new.
#
#   ./add_branch_support_v4c_bp.sh
#   FORKS=4 THREADS=4 ./add_branch_support_v4c_bp.sh
set -uo pipefail
BASE=/home/phemarajata/Downloads/snp-mod-local-working
CLUSTERS=$BASE/L1v4c_out/Clusters
PARTITION=$BASE/FINAL_BASIS_2026-08-22/FINAL_PARTITION.tsv
OUT=${OUT:-$BASE/L1v4c_TREES_SUPPORTED}
IMG=quay.io/biocontainers/iqtree:2.2.6--h21ec9f0_0
UFBOOT=${UFBOOT:-1000}
ALRT=${ALRT:-1000}
FORKS=${FORKS:-3}
THREADS=${THREADS:-4}
LOG=$BASE/SUPPORT_TREES_V4C.log

[ -s "$PARTITION" ] || { echo "no frozen partition at $PARTITION" >&2; exit 1; }
mkdir -p "$OUT"

# The allowlist: replicon-unit directory names whose UNIT is in the frozen basis.
UNITS=$(tail -n +2 "$PARTITION" | cut -f1 | sort -u)
NUNITS=$(printf '%s\n' "$UNITS" | wc -l)
[ "$NUNITS" -eq 85 ] || { echo "expected 85 frozen units, got $NUNITS" >&2; exit 1; }

DIRS=()
while IFS= read -r u; do
    for d in "$CLUSTERS"/cluster_"$u"__*; do
        [ -d "$d" ] && DIRS+=("$d")
    done
done <<< "$UNITS"

echo "frozen units: $NUNITS   replicon-unit dirs matched: ${#DIRS[@]}"
[ "${#DIRS[@]}" -eq 170 ] || { echo "expected 170 replicon-units, got ${#DIRS[@]}" >&2; exit 1; }

: > "$LOG"
echo "basis=FINAL_BASIS_2026-08-22  units=$NUNITS  replicon_units=${#DIRS[@]}" >> "$LOG"

run_one() {
    local d="$1" OUT="$2" IMG="$3" UFBOOT="$4" ALRT="$5" THREADS="$6" LOG="$7"
    local unit; unit=$(basename "$d" | sed 's/^cluster_//')
    local pre="$d/${unit}.asc_preflight.txt"
    local aln="$d/Gubbins/${unit}.filtered_polymorphic_sites.fasta"
    [ -s "$pre" ] || { echo "SKIP $unit: no preflight" >> "$LOG"; return; }
    [ -s "$aln" ] || { echo "SKIP $unit: no filtered alignment" >> "$LOG"; return; }

    # shellcheck disable=SC1090
    . "$pre"
    if [ "${DEGENERATE_TREE:-0}" = "1" ] || [ "${N_TAXA:-0}" -lt 4 ]; then
        echo "SKIP $unit: N_TAXA=${N_TAXA:-?} (<4, no supportable topology)" >> "$LOG"
        return
    fi

    local work="$OUT/$unit"; mkdir -p "$work"
    cp "$aln" "$work/aln.fasta"
    local extra=""
    [ -n "${IQ_FCONST:-}" ] && extra="-fconst ${IQ_FCONST}"

    docker run --rm -v "$work":/d -w /d -u "$(id -u):$(id -g)" "$IMG" \
        iqtree2 -s aln.fasta -st DNA -m "${IQ_MODEL}" -T "$THREADS" \
        --prefix supported -bb "$UFBOOT" -alrt "$ALRT" $extra \
        > "$work/iqtree.stdout" 2>&1
    local rc=$?
    if [ $rc -eq 0 ] && [ -s "$work/supported.treefile" ]; then
        cp "$work/supported.treefile" "$OUT/${unit}.support.treefile"
        cp "$work/supported.iqtree"   "$OUT/${unit}.support.iqtree" 2>/dev/null
        rm -rf "$work"
        echo "OK   $unit (N_TAXA=${N_TAXA}, model=${IQ_MODEL})" >> "$LOG"
    else
        echo "FAIL $unit exit=$rc -- see $work/iqtree.stdout" >> "$LOG"
    fi
}
export -f run_one

printf '%s\0' "${DIRS[@]}" \
  | xargs -0 -P "$FORKS" -I{} bash -c 'run_one "$@"' _ {} "$OUT" "$IMG" "$UFBOOT" "$ALRT" "$THREADS" "$LOG"

echo "---- summary ----" >> "$LOG"
printf 'OK %d, SKIP %d, FAIL %d (of %d replicon-units)\n' \
    "$(grep -c '^OK'   "$LOG")" "$(grep -c '^SKIP' "$LOG")" \
    "$(grep -c '^FAIL' "$LOG")" "${#DIRS[@]}" >> "$LOG"
tail -4 "$LOG"
