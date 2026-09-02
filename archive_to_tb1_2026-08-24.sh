#!/usr/bin/env bash
# Move superseded directories to TB1 to buy disk headroom for the running
# reproducibility job (SUBMISSION_TODO D1).
#
# SAFETY MODEL. After this runs, TB1 holds the ONLY copy — the same situation
# recorded for pp2802 and all35_out. So a source directory is deleted ONLY after
# a full checksum verification of the copy passes. The sequence per item is:
#
#     rsync -a                      copy
#     rsync -ain --checksum         verify: MUST report zero differing files
#     rm -rf                        only if verification was clean
#
# If verification reports anything at all, the source is left in place and the
# item is marked FAILED. Nothing is ever deleted on a size or file-count match
# alone.
#
# Politeness: nice + ionice idle, because the Gubbins/Snippy run is live and
# competing for the same spindle-equivalent. This will be slow. That is fine.
#
# NOT MOVED, deliberately:
#   L1v4c_out            the reported run's output; source of the frozen tables
#   REPRO_2026-08-24_*   the live run
#   additions/           the live run reads 126 assemblies from it
#   cgmlst_lichtenegger/ live scorers + the Zenodo archive list
#   cgmlst_results/      concordance_frozen_bp.py and resolution_curve_bp.py
#                        (Figure 2) both read it
set -uo pipefail

WS=/home/phemarajata/Downloads/snp-mod-local-working
DEST=/media/phemarajata/TB1/snp_superseded
LOG="$WS/ARCHIVE_TB1_2026-08-24.log"

ITEMS=(v4c_local L1_out a100_stage a100_v4c_partition prod_s2_L1_6 fbL1_s1_L1_27)

mountpoint -q /media/phemarajata/TB1 || { echo "FATAL: TB1 not mounted"; exit 1; }
mkdir -p "$DEST" || exit 1

{
  echo "=== archive to TB1, started $(date -Is) ==="
  echo "destination: $DEST"
  df -h --output=avail "$WS" | tail -1 | xargs echo "root free before:"
  df -h --output=avail "$DEST" | tail -1 | xargs echo "TB1 free before: "
  echo
} | tee "$LOG"

for d in "${ITEMS[@]}"; do
  SRC="$WS/$d"
  [ -d "$SRC" ] || { echo "SKIP  $d — not present" | tee -a "$LOG"; continue; }
  [ -e "$DEST/$d" ] && { echo "SKIP  $d — already at destination, refusing to merge" | tee -a "$LOG"; continue; }

  SZ=$(du -sh "$SRC" | cut -f1)
  NF=$(find "$SRC" -type f | wc -l)
  echo "---- $d  ($SZ, $NF files)  $(date -Is)" | tee -a "$LOG"

  if ! nice -n 19 ionice -c3 rsync -a "$SRC/" "$DEST/$d/" >>"$LOG" 2>&1; then
    echo "FAILED $d — rsync copy errored, source LEFT IN PLACE" | tee -a "$LOG"
    continue
  fi

  # Full checksum verification. -n dry-run, -c force checksum, -i itemise.
  DIFF=$(nice -n 19 ionice -c3 rsync -ain --checksum "$SRC/" "$DEST/$d/" 2>>"$LOG" \
         | grep -vE '^\.d|^$' | head -50)
  if [ -n "$DIFF" ]; then
    echo "FAILED $d — checksum verification found differences, source LEFT IN PLACE:" | tee -a "$LOG"
    echo "$DIFF" | tee -a "$LOG"
    continue
  fi

  NF2=$(find "$DEST/$d" -type f | wc -l)
  if [ "$NF" -ne "$NF2" ]; then
    echo "FAILED $d — file count $NF -> $NF2, source LEFT IN PLACE" | tee -a "$LOG"
    continue
  fi

  rm -rf "$SRC" && echo "MOVED $d — verified clean ($NF files), source removed  $(date -Is)" | tee -a "$LOG"
  df -h --output=avail "$WS" | tail -1 | xargs echo "  root free now:" | tee -a "$LOG"
done

{
  echo
  echo "=== finished $(date -Is) ==="
  df -h --output=avail "$WS" | tail -1 | xargs echo "root free after:"
  df -h --output=avail "$DEST" | tail -1 | xargs echo "TB1 free after: "
} | tee -a "$LOG"
