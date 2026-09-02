#!/usr/bin/env bash
# Re-derive the units affected by the 2026-08-21 panel corrections.
# Closes HANDOFF_2026-08-21_EVENING.md §5 item 2.
#
# WHICH UNITS, AND WHY -- the handoff lists four units under one heading, but
# they are affected by TWO SEPARATE defects. Verified against
# curated_L1v4c_clusters.tsv, the endorsed membership source:
#
#   duplicate BioSamples (PANEL_DUPLICATES_2026-08-21.tsv, 18 drops):
#     strain_1_L1_8    91 -> 89   drop SRR11097784_SPAdes, SRR11097783_SPAdes
#     strain_14_L1_4   14 -> 12   drop SRR11097780_SPAdes, SRR11097779_SPAdes
#     strain_1_L1_10    7 ->  4   drop SRR11097772/82/81_SPAdes -- UNIT DROPPED,
#                                 below the n>=5 floor, so it is not re-run
#   register-excluded genome (a different list entirely):
#     strain_1_L1_26  154 -> 153  drop SRR2896257 (broken_assembly)
#
#   The other 11 duplicate drops sit in no analysed unit, so they cost nothing.
#   82 of 86 units are untouched.
#
# PARAMETERS ARE PINNED TO THE PRODUCTION RUN AND MUST NOT BE "IMPROVED".
# r/m shifts 0.47-0.78x with Gubbins settings and there is no correction factor,
# so a re-derived unit computed under different settings cannot be pooled with
# the other 82. Same container digest, same iterations, same tree builder, same
# --invariant-site-correction, same --filter-percentage as
# modules/local/gubbins_cluster/main.nf.
#
# TWO DEVIATIONS, both deliberate:
#   1. --seed is set explicitly. The pipeline passes no seed, and Gubbins then
#      draws randint(0,10000) for RAxML; a draw of 0 makes RAxML fail and
#      Gubbins misreports it as "Unable to fit model to data". Fixing the seed
#      removes a ~1/10001 per-run coin flip and makes these runs reproducible.
#      It does not change the model.
#   2. Runs are STRICTLY SEQUENTIAL, each in its own working directory. Gubbins
#      writes scratch to the CWD rather than under --prefix, so concurrent runs
#      in a shared directory overwrite each other's intermediates. That cost
#      this project three wrong conclusions.
set -euo pipefail

BASE="/home/phemarajata/Downloads/snp-mod-local-working"
SRC="$BASE/L1v4c_out/Clusters"
OUT="$BASE/rederive_2026-08-21"
IMG="quay.io/biocontainers/gubbins:3.4.3--py310h5140242_0"
THREADS="${THREADS:-16}"
SEED=20260821

mkdir -p "$OUT"
LOG="$OUT/rederive.log"
exec > >(tee -a "$LOG") 2>&1
echo "=== re-derivation started $(date -Is) ==="
echo "container $IMG | threads $THREADS | seed $SEED"

# unit_prefix : space-separated taxa to drop
declare -A DROPS=(
  ["strain_1_L1_26__GCF_003546995_3"]="SRR2896257"
  ["strain_1_L1_8__GCF_027856475_2"]="SRR11097784_SPAdes SRR11097783_SPAdes"
  ["strain_14_L1_4__GCF_000755925_1"]="SRR11097780_SPAdes SRR11097779_SPAdes"
)

filter_aln() {  # $1 in  $2 out  $3.. taxa to drop
  local in="$1" out="$2"; shift 2
  python3 - "$in" "$out" "$@" <<'PY'
import sys
src, dst, drop = sys.argv[1], sys.argv[2], set(sys.argv[3:])
kept = skipped = 0
seen = set()
with open(src) as fh, open(dst, "w") as out:
    emit = False
    for line in fh:
        if line.startswith(">"):
            name = line[1:].split()[0]
            seen.add(name)
            emit = name not in drop
            kept += emit
            skipped += (not emit)
        if emit:
            out.write(line)
missing = drop - seen
if missing:
    sys.exit(f"FATAL: taxa not present in {src}: {sorted(missing)}")
print(f"    kept {kept} taxa, removed {skipped}")
PY
}

for unit in "${!DROPS[@]}"; do
  for rep in 1 2; do
    id="${unit}_${rep}"
    aln="$SRC/cluster_${id}/${id}.core.full.aln"
    wd="$OUT/$id"
    if [ ! -s "$aln" ]; then echo "SKIP $id: no alignment at $aln"; continue; fi
    if [ -s "$wd/${id}.per_branch_statistics.csv" ]; then
      echo "SKIP $id: already done (resumable)"; continue
    fi
    echo
    echo "--- $id  $(date -Is) ---"
    rm -rf "$wd"; mkdir -p "$wd"
    echo "  filtering: dropping ${DROPS[$unit]}"
    filter_aln "$aln" "$wd/${id}.reduced.aln" ${DROPS[$unit]}

    # isolated CWD: Gubbins scratch lands here, not in a shared directory
    # --shm-size=2g is REQUIRED, not tuning. Docker defaults /dev/shm to 64 MB;
    # Gubbins' pyjar allocates its ancestral-reconstruction arrays in shared
    # memory, and on a large unit it runs off the end of the segment and dies
    # with SIGBUS ("Bus error (core dumped)") *after* RAxML has already
    # succeeded. strain_1_L1_26 (154 taxa) failed exactly this way at rc=135
    # while the 90- and 13-taxon units passed. nextflow.config sets the same
    # 2g for the same documented reason, so this is production parity.
    docker run --rm -u "$(id -u):$(id -g)" \
      --shm-size=2g \
      -v "$wd":/wd -w /wd \
      -e NUMBA_CACHE_DIR=/wd/.numba_cache \
      "$IMG" bash -lc "
        mkdir -p /wd/.numba_cache
        run_gubbins.py \
          --prefix '${id}' \
          --tree-builder raxml \
          --iterations 5 \
          --min-snps 3 \
          --invariant-site-correction \
          --filter-percentage 25.0 \
          --seed ${SEED} \
          --threads ${THREADS} \
          '${id}.reduced.aln'
      " > "$wd/${id}.gubbins.log" 2>&1 && rc=0 || rc=$?
    if [ "$rc" -ne 0 ]; then
      echo "  FAILED rc=$rc -- see $wd/${id}.gubbins.log"
      tail -5 "$wd/${id}.gubbins.log" | sed 's/^/     /'
      continue
    fi
    n=$(grep -c '^>' "$wd/${id}.reduced.aln" || true)
    echo "  OK  n=$n  $(date -Is)"
    # the reduced alignment is large and reconstructible; drop it once used
    rm -f "$wd/${id}.reduced.aln"
  done
done

echo
echo "=== finished $(date -Is) ==="
echo "Next: recompute r/m with consolidate_L1_rm_bp.py over $OUT, then splice"
echo "those three units into RM_RESULTS_L1_CORRECTED.tsv and DROP strain_1_L1_10."
