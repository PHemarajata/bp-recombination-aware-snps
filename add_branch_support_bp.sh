#!/usr/bin/env bash
# Recompute each unit's ML tree WITH branch support, from published outputs.
#
# WHY NOT JUST RESUME THE PIPELINE WITH --iqtree_support true. That was tried.
# The runner regenerates its inputs on every launch and Nextflow's default cache
# hashing includes file mtime, so the resume invalidated the run instead of
# reusing it (1,313 of 2,070 INFILE_HANDLING tasks re-running before it was
# stopped). The runner is now idempotent, but the damage to this run's cache is
# done, and redoing 4,140 snippy mappings to add bootstrap values to trees would
# be absurd. Everything IQ-TREE needs is already published.
#
# FIDELITY: this reproduces the pipeline's own IQTREE_ASC invocation exactly --
# same container, same alignment, same model and -fconst taken from the unit's
# published ASC preflight decision -- and adds only `-bb <ufboot> -alrt <alrt>`,
# which is precisely what --iqtree_support true would have added. So the
# topology is computed the same way; only support values are new.
#
#   ./add_branch_support_bp.sh            # all 164 replicon-units
#   FORKS=4 ./add_branch_support_bp.sh    # tune parallelism
set -uo pipefail
BASE=/home/phemarajata/Downloads/snp-mod-local-working
OUT=${OUT:-$BASE/L1_TREES_SUPPORTED}
IMG=quay.io/biocontainers/iqtree:2.2.6--h21ec9f0_0
UFBOOT=${UFBOOT:-1000}
ALRT=${ALRT:-1000}
FORKS=${FORKS:-3}
THREADS=${THREADS:-4}
LOG=$BASE/SUPPORT_TREES.log

mkdir -p "$OUT"
: > "$LOG"

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
        # UFBoot needs >=4 taxa to mean anything; below that there is no topology
        # to support. Record it rather than emitting a tree with fake values.
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

find "$BASE/L1_out/Clusters" -maxdepth 1 -mindepth 1 -type d -print0 \
  | xargs -0 -P "$FORKS" -I{} bash -c 'run_one "$@"' _ {} "$OUT" "$IMG" "$UFBOOT" "$ALRT" "$THREADS" "$LOG"

echo "---- summary ----" >> "$LOG"
printf 'OK %d, SKIP %d, FAIL %d\n' \
    "$(grep -c '^OK'   "$LOG")" "$(grep -c '^SKIP' "$LOG")" "$(grep -c '^FAIL' "$LOG")" >> "$LOG"
tail -4 "$LOG"
