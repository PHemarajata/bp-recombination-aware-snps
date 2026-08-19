#!/usr/bin/env bash
# Alert stream for the v4c SNP run. One stdout line = one notification, so this
# emits ONLY on state change, never per poll.
#
# Coverage rule: silence must not be able to look like success. This emits on
# every terminal state -- completion, death, stall, task failure -- not just on
# the happy path. If the run crashed right now, the java-gone branch fires.
#
# ONE_SHOT=1 prints current state once and exits (for testing).
set -uo pipefail
B="/home/phemarajata/Downloads/snp-mod-local-working"
GEN=$(( $(wc -l < "$B/curated_L1v4c_clusters.tsv") - 1 ))   # 2352
RU=$(( ($(wc -l < "$B/curated_L1v4c_refs.tsv") - 1) * 2 ))  # 172
SCAT=$(( GEN * 2 ))                                          # 4704

d100=0; d60=0; d35=0; prev_bad=0; prev_done=""; stall_fired=0

snapshot () {   # -> "stage:done/expected ..." for the stages that matter
  local T="$1"
  awk -F'\t' -v gen="$GEN" -v ru="$RU" -v scat="$SCAT" '
    NR>1 && ($5=="COMPLETED"||$5=="CACHED") {
      split($4,a,"("); p=a[1]; gsub(/^.*:/,"",p); gsub(/ +$/,"",p); ok[p]++
    }
    END {
      want["INFILE_HANDLING_UNIX"]=gen; want["SNIPPY_SCATTER"]=scat
      want["SNIPPY_CORE_GATHER"]=ru; want["KEEP_INVARIANT_ATCG"]=ru
      want["GUBBINS_CLUSTER"]=ru; want["IQTREE_ASC"]=ru
      n=split("INFILE_HANDLING_UNIX SNIPPY_SCATTER SNIPPY_CORE_GATHER KEEP_INVARIANT_ATCG GUBBINS_CLUSTER IQTREE_ASC", o, " ")
      s=""
      for (i=1;i<=n;i++) { p=o[i]; s=s sprintf("%s:%d/%d ", p, ok[p]+0, want[p]) }
      print s
    }' "$T" 2>/dev/null
}

# Quarter-milestones only: 25/50/75/100% per stage, so a 14 h run yields ~24
# progress events, not one per poll.
milestones () {
  local snap="$1"
  for kv in $snap; do
    p=${kv%%:*}; rest=${kv#*:}; d=${rest%%/*}; e=${rest##*/}
    [ "${e:-0}" -gt 0 ] || continue
    q=$(( d * 4 / e ))
    echo "$p:$q"
  done
}

while true; do
  T=$(ls -t "$B"/L1v4c_out/pipeline_info/execution_trace_*.txt 2>/dev/null | head -1)
  FREE=$(df -BG --output=avail / | tail -1 | tr -dc '0-9'); FREE=${FREE:-999}

  # ---- disk, one event per threshold ----
  if [ "$FREE" -lt 35 ] && [ "$d35" = 0 ]; then
    echo "DISK CRITICAL: ${FREE}G free on / -- act now. TB1 has $(df -BG --output=avail /media/phemarajata/TB1 2>/dev/null | tail -1 | tr -dc '0-9')G free."; d35=1
  elif [ "$FREE" -lt 60 ] && [ "$d60" = 0 ]; then
    echo "DISK WARNING: ${FREE}G free on / (work dir $(du -sh "$B/L1v4c_work" 2>/dev/null | cut -f1))."; d60=1
  elif [ "$FREE" -lt 100 ] && [ "$d100" = 0 ]; then
    echo "disk notice: ${FREE}G free on / -- still fine, watching."; d100=1
  fi

  if [ -n "$T" ] && [ -s "$T" ]; then
    # ---- task failures ----
    bad=$(awk -F'\t' 'NR>1 && $5!="COMPLETED" && $5!="CACHED"' "$T" 2>/dev/null | wc -l)
    if [ "$bad" -gt "$prev_bad" ]; then
      echo "TASK FAILURES now $bad (was $prev_bad): $(awk -F'\t' 'NR>1 && $5!="COMPLETED" && $5!="CACHED"{split($4,a,"("); p=a[1]; gsub(/^.*:/,"",p); print p" "$5" exit="$6}' "$T" 2>/dev/null | sort | uniq -c | sort -rn | head -3 | tr '\n' '; ')"
      prev_bad=$bad
    fi
    # ---- quarter milestones ----
    snap=$(snapshot "$T")
    done_now=$(milestones "$snap" | tr '\n' ' ')
    if [ "$done_now" != "$prev_done" ] && [ -n "$prev_done" ]; then
      for kv in $done_now; do
        case " $prev_done " in *" $kv "*) ;; *)
          p=${kv%%:*}; q=${kv##*:}
          [ "$q" -gt 0 ] && echo "progress: $p at $(( q*25 ))% -- $(echo "$snap" | tr ' ' '\n' | grep "^$p:" | cut -d: -f2)"
        ;; esac
      done
    fi
    [ -n "$done_now" ] && prev_done="$done_now"

    # ---- stall: java alive but trace untouched ----
    stale=$(( $(date +%s) - $(stat -c %Y "$T" 2>/dev/null || echo 0) ))
    if pgrep -x java >/dev/null 2>&1 && [ "$stale" -gt 2700 ] && [ "$stall_fired" = 0 ]; then
      echo "STALL: nextflow alive but execution trace untouched for $(( stale/60 )) min."; stall_fired=1
    fi
    [ "$stale" -lt 900 ] && stall_fired=0
  fi

  # ---- terminal: nextflow gone ----
  if ! pgrep -x java >/dev/null 2>&1; then
    sleep 30
    if ! pgrep -x java >/dev/null 2>&1; then
      final=""
      [ -n "$T" ] && final=$(snapshot "$T")
      nbad=0; [ -n "$T" ] && nbad=$(awk -F'\t' 'NR>1 && $5!="COMPLETED" && $5!="CACHED"' "$T" 2>/dev/null | wc -l)
      echo "RUN ENDED. failed/aborted tasks=$nbad. $final"
      echo "RUN ENDED. Clusters published: $(ls "$B/L1v4c_out/Clusters" 2>/dev/null | wc -l) / $RU. Verify per unit before quoting numbers: collect_L1_results.sh, then Summaries/cluster_phylogeny_summary.csv"
      exit 0
    fi
  fi

  [ "${ONE_SHOT:-0}" = "1" ] && { echo "one-shot: free=${FREE}G bad=${prev_bad:-0} $(snapshot "$T")"; exit 0; }
  sleep 120
done
