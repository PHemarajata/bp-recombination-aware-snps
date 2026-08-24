#!/usr/bin/env bash
# End-to-end reproducibility run — SUBMISSION_TODO.md D1.
#
# Re-executes the reported analysis from the pinned commit and inputs so the
# headline figures can be diffed against the frozen basis.
#
# The command line is IDENTICAL to the one recorded in
# PRODUCTION_RUN_PIN_2026-08-24.md §2 except for three things, all deliberate:
#   --input      the reconstructed samplesheet (the original was lost; the
#                reconstruction is itself under test here)
#   --outdir     a fresh directory. NEVER point this at L1v4c_out: that is the
#                reported run's 17 GB output and the source of the frozen tables
#   -work-dir    a fresh work dir, for the same reason
#
# Pipeline is a DETACHED git worktree at 79ab645, so the user's own checkout of
# wf-assembly-snps-mod (branch fix/crlf-writers-and-pipefail-sigpipe) is
# untouched.
#
# Expected landing point: 86 units / 2,352 genomes / 172 replicon-units. The
# reported basis of 85 / 2,340 / 170 is a POST-HOC correction of this run's
# output (METHODS §2.12.5) and is not reproduced by the pipeline itself.
set -uo pipefail

WS=/home/phemarajata/Downloads/snp-mod-local-working
PIPE=/home/phemarajata/wf-assembly-snps-mod-79ab645
TAG=2026-08-24
OUT="$WS/REPRO_${TAG}_out"
WORK="$WS/REPRO_${TAG}_work"
LOG="$WS/REPRO_${TAG}.log"
WDOG="$WS/REPRO_${TAG}.watchdog.log"

# Free space below which the watchdog stops the run. A full root filesystem on
# this workstation is a worse outcome than a failed run: / holds the 425 GB
# working directory, the desktop session and everything else.
MIN_FREE_GB=40

[ -d "$PIPE" ] || { echo "FATAL: pipeline worktree $PIPE missing"; exit 1; }
[ "$(git -C "$PIPE" rev-parse HEAD)" = "79ab6459940b232790dc68d6592b72de3cdeb750" ] \
  || { echo "FATAL: worktree is not at 79ab645"; exit 1; }
for f in "$WS/wf_L1v4c_run_samplesheet.RECONSTRUCTED.csv" \
         "$WS/.L1_run_clusters.tsv" "$WS/.L1_run_refs_normalized.tsv" \
         "$WS/curated_L1_overrides.config"; do
  [ -s "$f" ] || { echo "FATAL: input missing or empty: $f"; exit 1; }
done
[ -e "$OUT" ] && { echo "FATAL: $OUT already exists — refusing to overwrite"; exit 1; }

echo "launching at $(date -Is)" | tee "$LOG"
echo "  pipeline $PIPE @ $(git -C "$PIPE" rev-parse --short HEAD)" | tee -a "$LOG"
echo "  outdir   $OUT" | tee -a "$LOG"
echo "  workdir  $WORK" | tee -a "$LOG"

cd "$PIPE" || exit 1

nextflow run . \
  -profile bp,local_workstation_rtx4070,docker \
  -c "$WS/curated_L1_overrides.config" \
  --input "$WS/wf_L1v4c_run_samplesheet.RECONSTRUCTED.csv" \
  --cluster_assignments "$WS/.L1_run_clusters.tsv" \
  --cluster_references "$WS/.L1_run_refs_normalized.tsv" \
  --split_replicons true \
  --max_cluster_size 1000 \
  --min_replicon_length 100000 \
  --gubbins_min_snps 3 \
  --gubbins_iterations 5 \
  --gubbins_use_hybrid false \
  --gubbins_skip_starting_tree true \
  --iqtree_support true \
  --outdir "$OUT" \
  -work-dir "$WORK" \
  -ansi-log false >>"$LOG" 2>&1 &

NFPID=$!
echo "  nextflow pid $NFPID" | tee -a "$LOG"

# --- disk watchdog -------------------------------------------------------
# Polls every 5 minutes. On breach it sends SIGTERM to the Nextflow process
# group, which lets Nextflow finish its bookkeeping and leave a resumable
# cache, rather than the filesystem filling and tasks dying arbitrarily.
(
  echo "watchdog started $(date -Is), floor ${MIN_FREE_GB} GB" > "$WDOG"
  while kill -0 "$NFPID" 2>/dev/null; do
    FREE=$(df -BG --output=avail "$WS" | tail -1 | tr -dc '0-9')
    echo "$(date -Is) free=${FREE}G" >> "$WDOG"
    if [ -n "$FREE" ] && [ "$FREE" -lt "$MIN_FREE_GB" ]; then
      echo "$(date -Is) BREACH: ${FREE}G < ${MIN_FREE_GB}G — stopping nextflow" >> "$WDOG"
      kill -TERM "$NFPID" 2>/dev/null
      break
    fi
    sleep 300
  done
  echo "$(date -Is) watchdog exiting" >> "$WDOG"
) &

wait "$NFPID"
RC=$?
echo "nextflow exited rc=$RC at $(date -Is)" | tee -a "$LOG"
exit "$RC"
