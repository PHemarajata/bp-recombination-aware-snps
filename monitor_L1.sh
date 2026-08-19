#!/usr/bin/env bash
# Heartbeat monitor for the 82-unit L1 recombination-aware SNP run.
#
# Same shape as monitor_pp2802.sh and detached from any Claude Code session on
# purpose: parented to init, so closing a terminal does not touch it. Every
# INTERVAL it appends a readable block to MONITOR_L1.log and one TSV row to
# MONITOR_L1.tsv.
#
#   start :  setsid nohup ./monitor_L1.sh >/dev/null 2>&1 &
#   watch :  tail -f MONITOR_L1.log
#   stop  :  kill "$(cat .monitor_L1.pid)"
#   test  :  ONCE=1 ./monitor_L1.sh
#
# Env knobs:
#   INTERVAL=900        seconds between heartbeats
#   DISK_WARN_GB=80     warn when free space drops below this
#   ONCE=1              emit a single heartbeat and exit
#
# WHAT IT WATCHES FOR, beyond progress. Three failure modes have already cost
# this project real time, and each has a distinct signature:
#
#   "Unable to fit model to data"  Gubbins' bare `except` around a raxmlHPC call
#                                  that SEGFAULTED because its -n run id reached
#                                  128 characters. Deflines are normalized and
#                                  SPLIT_REFERENCE_REPLICONS now gates on this,
#                                  so ANY occurrence here is a regression, not a
#                                  reference problem. Flagged loudly.
#   exit 137                       OOM -- but also what `docker kill` produces,
#                                  so a burst of 137s right after a manual stop
#                                  is not an OOM. Counted separately, never
#                                  silently folded into "failed".
#   pipeline terminated early      the errorStrategy closure returning 'retry'
#                                  with no retries left. Detected as "nextflow
#                                  gone but stages incomplete".
set -uo pipefail
export PATH=/usr/bin:/bin:/usr/local/bin:$PATH

BASE=/home/phemarajata/Downloads/snp-mod-local-working
OUTDIR=${OUTDIR:-$BASE/L1_out}
WORKDIR=${WORKDIR:-$BASE/L1_work}
INFO=$OUTDIR/pipeline_info
HB_LOG=$BASE/MONITOR_L1.log
HB_TSV=$BASE/MONITOR_L1.tsv
PIDFILE=$BASE/.monitor_L1.pid
RUNLOG=$BASE/L1_run.log

INTERVAL=${INTERVAL:-900}
DISK_WARN_GB=${DISK_WARN_GB:-80}
ONCE=${ONCE:-0}

# Expected totals, derived from the run's own inputs rather than hardcoded, so
# an EXCLUDE_UNITS run reports against its own scope.
CL=$BASE/.L1_run_clusters.tsv
N_GENOMES=$(( $(wc -l < "$CL") - 1 ))
N_UNITS=$(tail -n +2 "$CL" | cut -f1 | sort -u | wc -l)
N_REPLICON_UNITS=$(( N_UNITS * 2 ))
N_SNIPPY=$(( N_GENOMES * 2 ))

[ "$ONCE" = "1" ] || echo $$ > "$PIDFILE"

trace_file() { ls -t "$INFO"/execution_trace*.txt 2>/dev/null | head -1; }

# Tasks a process has finished, from the newest trace.
#
# CACHED counts as done. On a resumed run most of the work IS cached -- the
# relaunch after normalizing deflines reused all 2,070 INFILE_HANDLING tasks --
# and counting only COMPLETED reports 0/2070 for a stage that is entirely
# finished, which reads as a stall.
count_stage() {
    local t="$1" proc="$2"
    [ -f "$t" ] || { echo 0; return; }
    awk -F'\t' -v p="$proc" '
        NR>1 && index($4,p)>0 && ($5=="COMPLETED" || $5=="CACHED") { n++ }
        END { print n+0 }' "$t"
}

nextflow_alive() {
    ps -eo cmd 2>/dev/null | grep -q "nextflow-.*\.jar run" && return 0 || return 1
}

heartbeat() {
    local t now
    t=$(trace_file); now=$(date '+%Y-%m-%d %H:%M:%S')

    local infile split snippy gather gub iqtree
    infile=$(count_stage "$t" INFILE_HANDLING_UNIX)
    split=$(count_stage  "$t" SPLIT_REFERENCE_REPLICONS)
    snippy=$(count_stage "$t" SNIPPY_SCATTER)
    gather=$(count_stage "$t" SNIPPY_CORE_GATHER)
    gub=$(count_stage    "$t" GUBBINS_CLUSTER)
    iqtree=$(count_stage "$t" IQTREE_ASC)

    # Failures, split by kind. 137 is reported apart from everything else.
    local fail137 failother
    if [ -f "$t" ]; then
        fail137=$(awk  -F'\t' 'NR>1 && $5=="FAILED" && $6=="137" {n++} END{print n+0}' "$t")
        failother=$(awk -F'\t' 'NR>1 && $5=="FAILED" && $6!="137" {n++} END{print n+0}' "$t")
    else fail137=0; failother=0; fi

    local modelfit=0
    if [ -f "$RUNLOG" ]; then
        modelfit=$(grep -ci "unable to fit model to data" "$RUNLOG" 2>/dev/null) || modelfit=0
    fi

    local free_gb alive
    free_gb=$(df -BG --output=avail "$BASE" | tail -1 | tr -dc '0-9')
    if nextflow_alive; then alive=running; else alive=STOPPED; fi

    local pct=0
    [ "$N_SNIPPY" -gt 0 ] && pct=$(( 100 * snippy / N_SNIPPY ))

    {
        echo "=============================================================="
        echo "[$now]  nextflow: $alive   free: ${free_gb} GB"
        printf '  %-26s %6d / %-6d\n' "INFILE_HANDLING"    "$infile" "$N_GENOMES"
        printf '  %-26s %6d / %-6d\n' "SPLIT_REPLICONS"    "$split"  "$N_UNITS"
        printf '  %-26s %6d / %-6d  (%d%%)\n' "SNIPPY_SCATTER" "$snippy" "$N_SNIPPY" "$pct"
        printf '  %-26s %6d / %-6d\n' "SNIPPY_CORE_GATHER" "$gather" "$N_REPLICON_UNITS"
        printf '  %-26s %6d / %-6d\n' "GUBBINS_CLUSTER"    "$gub"    "$N_REPLICON_UNITS"
        printf '  %-26s %6d / %-6d\n' "IQTREE_ASC"         "$iqtree" "$N_REPLICON_UNITS"
        [ "$fail137" -gt 0 ]   && echo "  NOTE   : $fail137 task(s) exit 137 -- OOM, *or* a manual docker kill"
        [ "$failother" -gt 0 ] && echo "  FAILED : $failother task(s) with a non-137 exit"
        if [ "$modelfit" -gt 0 ]; then
            echo "  *** REGRESSION: $modelfit 'Unable to fit model to data' ***"
            echo "      Deflines are normalized and the unit-id gate is in place,"
            echo "      so this should be impossible. Check the run id length in"
            echo "      the unit's diagnostics.log before blaming the reference."
        fi
        [ "$free_gb" -lt "$DISK_WARN_GB" ] && echo "  *** DISK: only ${free_gb} GB free ***"
        if [ "$alive" = "STOPPED" ] && [ "$gub" -lt "$N_REPLICON_UNITS" ]; then
            echo "  *** nextflow is gone with $(( N_REPLICON_UNITS - gub )) Gubbins unit(s) outstanding."
            echo "      Check the tail of L1_run.log: a zero exit does NOT mean every"
            echo "      unit succeeded, and errorStrategy 'ignore' hides per-unit failures."
        fi
    } >> "$HB_LOG"

    [ -f "$HB_TSV" ] || printf 'timestamp\talive\tinfile\tsplit\tsnippy\tgather\tgubbins\tiqtree\tfail137\tfailother\tmodelfit\tfree_gb\n' > "$HB_TSV"
    printf '%s\t%s\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n' \
        "$now" "$alive" "$infile" "$split" "$snippy" "$gather" "$gub" "$iqtree" \
        "$fail137" "$failother" "$modelfit" "$free_gb" >> "$HB_TSV"
}

if [ "$ONCE" = "1" ]; then heartbeat; cat "$HB_LOG" | tail -20; exit 0; fi

while true; do
    heartbeat
    nextflow_alive || { echo "[$(date '+%F %T')] nextflow gone; monitor exiting" >> "$HB_LOG"; break; }
    sleep "$INTERVAL"
done
rm -f "$PIDFILE"
