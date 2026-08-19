#!/usr/bin/env bash
# Rescue the per-unit Gubbins outputs the workflow does NOT publish, as each
# unit finishes rather than in one pass at the end.
#
# WHY INCREMENTALLY. publishDir copies only four files per unit
# (diagnostics.log, filtered_polymorphic_sites.fasta, node_labelled.final_tree.tre,
# recombination_predictions.gff). Everything else lives only in the Nextflow work
# directory and dies with it. The most important omission is
# <unit>.per_branch_statistics.csv -- the ONLY source of pooled r/m, which is the
# headline number of the whole analysis. Waiting until the run ends means one
# late failure (a full disk, an interrupted run, an over-eager cleanup) loses it
# for every unit at once.
#
# Note the filename: it is PREFIXED with the unit name, so `find -name
# per_branch_statistics.csv` matches nothing. That mistake is easy to make and
# looks exactly like "Gubbins never produced it".
#
#   start :  setsid nohup ./archive_L1_stats.sh >/dev/null 2>&1 &
#   once  :  ONCE=1 ./archive_L1_stats.sh
#   stop  :  kill "$(cat .archive_L1.pid)"
#
# Only small files are taken. branch_base_reconstruction.embl is ~1.9 MB/unit and
# is reconstructible from the published tree plus the alignment, so it is skipped
# by default -- disk is the binding constraint late in this run. Set
# HEAVY=1 to include it.
set -uo pipefail
export PATH=/usr/bin:/bin:/usr/local/bin:$PATH

BASE=/home/phemarajata/Downloads/snp-mod-local-working
WORKDIR=${WORKDIR:-$BASE/L1_work}
DEST=${DEST:-$BASE/RUN_STATS_ARCHIVE/L1}
LOG=$BASE/ARCHIVE_L1.log
PIDFILE=$BASE/.archive_L1.pid
INTERVAL=${INTERVAL:-300}
ONCE=${ONCE:-0}
HEAVY=${HEAVY:-0}

mkdir -p "$DEST"
[ "$ONCE" = "1" ] || echo $$ > "$PIDFILE"

PATTERNS=( '*.per_branch_statistics.csv'
           '*.summary_of_snp_distribution.vcf'
           '*.recombination_predictions.embl'
           '*.final_tree.tre'
           '*.diagnostics.log' )
[ "$HEAVY" = "1" ] && PATTERNS+=( '*.branch_base_reconstruction.embl' )

sweep() {
    local n=0 skipped=0
    for pat in "${PATTERNS[@]}"; do
        while IFS= read -r f; do
            [ -s "$f" ] || continue
            local b; b=$(basename "$f")
            # gubbins.log carries the citation manifest and is the authoritative
            # record of the version actually used; keep it under the unit name.
            local dst="$DEST/$b"
            if [ -e "$dst" ] && [ "$dst" -nt "$f" ]; then skipped=$((skipped+1)); continue; fi
            cp -p "$f" "$dst" 2>/dev/null && n=$((n+1))
        done < <(find "$WORKDIR" -name "$pat" -type f 2>/dev/null)
    done
    local stats; stats=$(ls "$DEST"/*.per_branch_statistics.csv 2>/dev/null | wc -l)
    printf '[%s] copied %d new file(s), %d already current; per_branch_statistics: %d/164 units\n' \
        "$(date '+%F %T')" "$n" "$skipped" "$stats" >> "$LOG"
}

if [ "$ONCE" = "1" ]; then sweep; tail -3 "$LOG"; exit 0; fi

while true; do
    sweep
    ps -eo cmd 2>/dev/null | grep -q "nextflow-.*\.jar run" || {
        sweep   # one final pass after the run exits, before anything is cleaned
        echo "[$(date '+%F %T')] run finished; final sweep done" >> "$LOG"
        break
    }
    sleep "$INTERVAL"
done
rm -f "$PIDFILE"
