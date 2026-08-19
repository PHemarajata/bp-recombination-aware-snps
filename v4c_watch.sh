#!/usr/bin/env bash
# v4c SNP run watch. Writes V4C_STATUS.txt every 3 min. No notifications --
# this is the "cat one file and know" view. Alerts come from the Monitor.
#
# Denominators are DERIVED, not hardcoded from a previous run:
#   analysed genomes = rows in curated_L1v4c_clusters.tsv      -> 2352
#   analysis units   = rows in curated_L1v4c_refs.tsv          -> 86
#   replicon-units   = units x 2 (--split_replicons, BP is 2 chromosomes) -> 172
#   SNIPPY_SCATTER   = genomes x 2                             -> 4704
# Counting before a stage has been reached gives a partial denominator, which is
# how six appendix figures in this project once went wrong. Percentages below are
# always <completed>/<expected>, never <completed>/<seen so far>.
set -uo pipefail
B="/home/phemarajata/Downloads/snp-mod-local-working"
OUT="$B/V4C_STATUS.txt"
LOG="$B/L1v4c_run.log"
WORK="$B/L1v4c_work"
RESULTS="$B/L1v4c_out"

GEN=$(( $(wc -l < "$B/curated_L1v4c_clusters.tsv") - 1 ))
UNITS=$(( $(wc -l < "$B/curated_L1v4c_refs.tsv") - 1 ))
RU=$(( UNITS * 2 ))
SCAT=$(( GEN * 2 ))

pct () { [ "$2" -gt 0 ] && awk -v a="$1" -v b="$2" 'BEGIN{printf "%.1f%%", 100*a/b}' || echo "-"; }

while true; do
  T=$(ls -t "$RESULTS"/pipeline_info/execution_trace_*.txt 2>/dev/null | head -1)
  {
    echo "v4c SNP run  --  $(date '+%F %T %z')"
    echo "host $(hostname)   up $(uptime -p 2>/dev/null | sed 's/^up //')"
    echo

    # STATE: `pgrep -x java` matches the process NAME only. Never `pgrep -f` --
    # that matches any shell whose command line merely CONTAINS the pattern,
    # including this script's own, and it has already caused one false
    # "still running" on the A100 and killed one shell here.
    # Secondary signal: a live run touches the trace within a few minutes.
    STALE=99999
    [ -n "$T" ] && STALE=$(( $(date +%s) - $(stat -c %Y "$T" 2>/dev/null || echo 0) ))
    if pgrep -x java >/dev/null 2>&1; then
      if [ "$STALE" -gt 1800 ]; then
        echo "STATE : RUNNING but trace untouched for $((STALE/60)) min  <-- possible stall"
      else
        echo "STATE : RUNNING   (trace touched ${STALE}s ago)"
      fi
    else
      echo "STATE : NOT RUNNING  <-- finished, or died; check the tail below"
    fi
    echo "session c90e1105-5b12-455e-9b31-4ecde888d559   (RESUME_SESSION=<that> to restart)"
    echo

    echo "-- progress (completed / expected) --"
    if [ -n "$T" ] && [ -s "$T" ]; then
      awk -F'\t' -v gen="$GEN" -v ru="$RU" -v scat="$SCAT" '
        NR>1 {
          split($4,a,"("); p=a[1]; gsub(/^.*:/,"",p); gsub(/ +$/,"",p);
          seen[p]++; if ($5=="COMPLETED"||$5=="CACHED") ok[p]++;
          if ($5!="COMPLETED"&&$5!="CACHED") bad[p"|"$5]++;
        }
        END {
          want["INFILE_HANDLING_UNIX"]=gen; want["SNIPPY_SCATTER"]=scat;
          want["SNIPPY_CORE_GATHER"]=ru; want["KEEP_INVARIANT_ATCG"]=ru;
          want["GUBBINS_CLUSTER"]=ru; want["IQTREE_ASC"]=ru;
          want["SELECT_UNIT_MEDOID"]=ru; want["ASC_PREFLIGHT"]=ru;
          want["SPLIT_REFERENCE_REPLICONS"]=int(ru/2);
          n=split("SPLIT_REFERENCE_REPLICONS INFILE_HANDLING_UNIX SNIPPY_SCATTER SNIPPY_CORE_GATHER KEEP_INVARIANT_ATCG GUBBINS_CLUSTER ASC_PREFLIGHT IQTREE_ASC SELECT_UNIT_MEDOID GLOBAL_CORE_ALIGNMENT GLOBAL_ML_TREE SUMMARIZE_CLUSTER_PHYLOGENY POOL_RECOMBINATION_STATS", order, " ");
          for (i=1;i<=n;i++) {
            p=order[i]; if (!(p in seen) && !(p in want)) continue;
            e=(p in want)?want[p]:0;
            if (e>0) printf "  %-28s %5d / %-5d %6.1f%%\n", p, ok[p]+0, e, 100*(ok[p]+0)/e;
            else if (p in seen) printf "  %-28s %5d\n", p, ok[p]+0;
          }
          print "";
          f=0; for (k in bad) { split(k,x,"|"); printf "  NON-OK: %-26s %-10s %d\n", x[1], x[2], bad[k]; f=1 }
          if (!f) print "  no failed/aborted tasks";
        }' "$T"
    else
      echo "  (no execution trace yet)"
    fi
    echo

    echo "-- deliverable --"
    echo "  cluster dirs published : $(ls "$RESULTS/Clusters" 2>/dev/null | wc -l) / $RU"
    echo "  tasks submitted (log)  : $(grep -c 'Submitted process' "$LOG" 2>/dev/null || echo 0)"
    echo

    echo "-- disk --"
    FREE_G=$(df -BG --output=avail / | tail -1 | tr -dc '0-9')
    echo "  /        : ${FREE_G}G free   ($(df -h / | tail -1 | awk '{print $5}') used)"
    echo "  work dir : $(du -sh "$WORK" 2>/dev/null | cut -f1)"
    echo "  outdir   : $(du -sh "$RESULTS" 2>/dev/null | cut -f1)"
    echo "  TB1      : $(df -h /media/phemarajata/TB1 2>/dev/null | tail -1 | awk '{print $4}' ) free   (escape valve)"
    if   [ "${FREE_G:-999}" -lt 35 ]; then echo "  !! CRITICAL: under 35G -- free space now"
    elif [ "${FREE_G:-999}" -lt 60 ]; then echo "  !  WARNING: under 60G"
    elif [ "${FREE_G:-999}" -lt 100 ]; then echo "  .  notice: under 100G"
    fi
    echo

    echo "-- resources --"
    echo "  mem  : $(free -g | awk '/^Mem:/{print $7" GB avail of "$2}')"
    echo "  load : $(cut -d' ' -f1-3 /proc/loadavg)"
    echo
    echo "-- last log lines --"
    tail -4 "$LOG" 2>/dev/null | sed 's/^/  /'
    echo
    echo "(errorStrategy is 'ignore': a clean exit does NOT mean every unit succeeded."
    echo " Run collect_L1_results.sh and read Summaries/cluster_phylogeny_summary.csv"
    echo " before quoting any number.)"
  } > "$OUT.tmp" 2>&1
  mv -f "$OUT.tmp" "$OUT"
  sleep 180
done
