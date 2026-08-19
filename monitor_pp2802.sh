#!/usr/bin/env bash
# Heartbeat monitor for the PopPUNK 2802-genome recombination-aware SNP run.
#
# Detached from any Claude Code session on purpose: it is parented to init, so
# closing a terminal or an editor window does not touch it. Every INTERVAL it
# appends a human-readable block to MONITOR_pp2802.log, one TSV row to
# MONITOR_pp2802.tsv, and (optionally) raises a desktop notification.
#
#   start :  setsid nohup ./monitor_pp2802.sh >/dev/null 2>&1 &
#   watch :  tail -f MONITOR_pp2802.log
#   stop  :  kill "$(cat .monitor_pp2802.pid)"
#
# Env knobs (all optional):
#   INTERVAL=900        seconds between heartbeats
#   NOTIFY_EVERY=1      desktop notification every Nth beat; 0 = alerts only
#   DISK_WARN_HOURS=6   warn when disk runway drops below this
#   ONCE=1              emit a single heartbeat and exit (for testing)

set -uo pipefail
export PATH=/usr/bin:/bin:/usr/local/bin:$PATH

BASE=/home/phemarajata/Downloads/snp-mod-local-working
OUTDIR=$BASE/pp2802_out
WORKDIR=$BASE/pp2802_work
INFO=$OUTDIR/pipeline_info
HB_LOG=$BASE/MONITOR_pp2802.log
HB_TSV=$BASE/MONITOR_pp2802.tsv
STATE=$BASE/.monitor_pp2802.state
PIDFILE=$BASE/.monitor_pp2802.pid
EXPECTED_CACHE=$BASE/.monitor_pp2802.expected

INTERVAL=${INTERVAL:-900}
NOTIFY_EVERY=${NOTIFY_EVERY:-1}
DISK_WARN_HOURS=${DISK_WARN_HOURS:-6}
ONCE=${ONCE:-0}

# Desktop notifications need the session bus even when detached.
export DISPLAY=${DISPLAY:-:1}
export DBUS_SESSION_BUS_ADDRESS=${DBUS_SESSION_BUS_ADDRESS:-unix:path=/run/user/1000/bus}

# ---------------------------------------------------------------- helpers ---
log()  { printf '%s\n' "$*" >> "$HB_LOG"; }
now()  { date '+%Y-%m-%d %H:%M:%S'; }

notify() { # urgency, title, body
  command -v notify-send >/dev/null 2>&1 || return 0
  notify-send -u "$1" -a "pp2802 monitor" "$2" "$3" 2>/dev/null || true
}

# Newest trace wins, so a mid-flight restart is picked up automatically.
newest_trace() { ls -t "$INFO"/execution_trace_*.txt 2>/dev/null | head -1; }

# The java process is identified by the work dir it was launched against, not by
# a remembered PID, so it survives a pipeline restart.
nf_pid() { pgrep -f "nextflow.*pp2802_work|pp2802_work.*nextflow" 2>/dev/null | head -1; }

# Follow the launcher's stdout redirect rather than hardcoding a scratch path.
nf_log() {
  local pid parent
  pid=$(nf_pid) || return 1
  [ -z "$pid" ] && return 1
  parent=$(ps -o ppid= -p "$pid" 2>/dev/null | tr -d ' ')
  [ -n "$parent" ] && readlink -f "/proc/$parent/fd/1" 2>/dev/null
}

fmt_hm() { # minutes -> "Xh Ym"
  local m=${1%.*}
  [ -z "$m" ] && { echo "?"; return; }
  printf '%dh %02dm' $((m/60)) $((m%60))
}

# --------------------------------------------------------------- expected ---
# SNIPPY_SCATTER denominator = sum over kept clusters of (members x replicons).
# Computed from the run's own outputs, never guessed; if any input is missing we
# emit no percentage rather than a percentage against a partial denominator.
compute_expected() {
  local trace=$1 gate tmp_repl tmp_size
  [ -s "$EXPECTED_CACHE" ] && { cat "$EXPECTED_CACHE"; return; }
  gate=$(sed -n 's/.*min cluster size gate *: *\([0-9]*\).*/\1/p' \
         "$OUTDIR/Summaries/cluster_summary.txt" 2>/dev/null | head -1)
  [ -z "$gate" ] && { echo ""; return; }
  tmp_repl=$(mktemp); tmp_size=$(mktemp)

  # cluster_id -> replicon count, read off each SPLIT_REFERENCE_REPLICONS work dir
  awk -F'\t' 'NR>1 && $4 ~ /SPLIT_REFERENCE_REPLICONS/ {print $2"\t"$4}' "$trace" \
  | while IFS=$'\t' read -r h name; do
      cid=$(printf '%s' "$name" | sed -E 's/.*\(([^)]*)\).*/\1/')
      d=$(ls -d "$WORKDIR/${h}"* 2>/dev/null | head -1)
      [ -z "$d" ] && continue
      n=$(ls "$d/replicons" 2>/dev/null | wc -l)
      [ "$n" -gt 0 ] && printf '%s\t%s\n' "$cid" "$n"
    done | sort -u > "$tmp_repl"

  # cluster_id -> member count, kept clusters only
  awk -F'\t' -v g="$gate" 'NR>1{c[$1]++} END{for(k in c) if(c[k]>=g) print k"\t"c[k]}' \
      "$OUTDIR/Summaries/clusters.tsv" 2>/dev/null | sort -u > "$tmp_size"

  # every kept cluster must have a known replicon count or we refuse to answer
  awk -F'\t' '
    NR==FNR { rep[$1]=$2; next }
    { if (!($1 in rep)) { missing=1; exit } ; total += $2 * rep[$1] }
    END { if (missing || total==0) print ""; else print total }
  ' "$tmp_repl" "$tmp_size" | tee "$EXPECTED_CACHE"
  rm -f "$tmp_repl" "$tmp_size"
}

# -------------------------------------------------------------- heartbeat ---
beat() {
  local trace pid alive avail_kb avail_gb done_n exp pct rate eta_min eta_clock
  local d_done d_avail burn runway containers stage bad cached ts elapsed
  local prev_ts prev_done prev_avail beat_no alerts=""

  ts=$(now); trace=$(newest_trace)
  [ -z "$trace" ] && { log "[$ts] no execution_trace yet"; return; }

  pid=$(nf_pid); alive=$([ -n "$pid" ] && echo yes || echo no)
  elapsed=$([ -n "$pid" ] && ps -o etime= -p "$pid" 2>/dev/null | tr -d ' ' || echo "-")

  done_n=$(awk -F'\t' 'NR>1 && $4 ~ /SNIPPY_SCATTER/ && $5=="COMPLETED"' "$trace" | wc -l)
  cached=$(awk -F'\t' 'NR>1 && $5=="CACHED"' "$trace" | wc -l)
  bad=$(awk -F'\t' 'NR>1 && $5!="COMPLETED" && $5!="CACHED"' "$trace" | wc -l)
  containers=$(docker ps -q 2>/dev/null | wc -l)
  exp=$(compute_expected "$trace")

  # stage: most recent process name Nextflow submitted, from the launcher's log
  local nlog; nlog=$(nf_log)
  if [ -n "${nlog:-}" ] && [ -r "$nlog" ]; then
    stage=$(tail -400 "$nlog" | sed -n 's/.*Submitted process > \([A-Z_:]*\).*/\1/p' \
            | tail -1 | sed 's/.*://')
  fi
  [ -z "${stage:-}" ] && stage=$(awk -F'\t' 'NR>1{n=$4} END{split(n,a," ");
      sub(/.*:/,"",a[1]); print a[1]}' "$trace")

  avail_kb=$(df -P "$BASE" | awk 'NR==2{print $4}')
  avail_gb=$(awk -v k="$avail_kb" 'BEGIN{printf "%.0f", k/1048576}')

  # deltas against the previous beat
  beat_no=1; prev_ts=""; prev_done=""; prev_avail=""; first_ts=""; first_avail=""
  if [ -s "$STATE" ]; then . "$STATE"; beat_no=$((PREV_BEAT+1))
     prev_ts=$PREV_TS; prev_done=$PREV_DONE; prev_avail=$PREV_AVAIL
     first_ts=${FIRST_TS:-$PREV_TS}; first_avail=${FIRST_AVAIL:-$PREV_AVAIL}; fi
  [ -z "$first_ts" ] && { first_ts=$(date +%s); first_avail=$avail_kb; }

  # Long-run task rate taken from the trace, not from the last interval. The
  # interval rate swings wildly on short windows (a 30 s sample put the ETA 8 h
  # out); the trace spans the whole stage and survives monitor restarts.
  local first_submit first_epoch span_min trace_rate
  first_submit=$(awk -F'\t' 'NR>1 && $4 ~ /SNIPPY_SCATTER/ {if(m==""||$7<m) m=$7} END{print m}' "$trace")
  if [ -n "$first_submit" ]; then
    first_epoch=$(date -d "${first_submit%.*}" +%s 2>/dev/null)
    if [ -n "$first_epoch" ]; then
      span_min=$(awk -v a="$first_epoch" -v b="$(date +%s)" 'BEGIN{printf "%.2f", (b-a)/60}')
      trace_rate=$(awk -v d="$done_n" -v m="$span_min" 'BEGIN{if(m>0) printf "%.2f", d/m}')
    fi
  fi

  local mins=0
  if [ -n "$prev_ts" ]; then
    mins=$(awk -v a="$prev_ts" -v b="$(date +%s)" 'BEGIN{printf "%.2f", (b-a)/60}')
    d_done=$((done_n - prev_done))
    d_avail=$(( (prev_avail - avail_kb) / 1048576 ))
    rate=$(awk -v d="$d_done" -v m="$mins" 'BEGIN{if(m>0) printf "%.1f", d/m; else print "?"}')
  fi

  # Disk burn measured against the monitor's own baseline rather than the last
  # interval, so a single quiet beat cannot fake an infinite runway.
  local base_min
  base_min=$(awk -v a="$first_ts" -v b="$(date +%s)" 'BEGIN{printf "%.2f", (b-a)/60}')
  if awk -v m="$base_min" 'BEGIN{exit !(m>=5)}'; then
    burn=$(awk -v k="$((first_avail - avail_kb))" -v m="$base_min" \
           'BEGIN{printf "%.1f", (k/1048576)*60/m}')
    runway=$(awk -v a="$avail_gb" -v b="$burn" 'BEGIN{if(b+0>0.05) printf "%.1f", a/b; else print ""}')
  fi

  # ETA from the trace-derived rate, only when a real denominator exists
  if [ -n "$exp" ]; then
    pct=$(awk -v d="$done_n" -v e="$exp" 'BEGIN{printf "%.1f", 100*d/e}')
    if [ -n "${trace_rate:-}" ]; then
      eta_min=$(awk -v e="$exp" -v d="$done_n" -v r="$trace_rate" \
                'BEGIN{if(r+0>0) printf "%.0f", (e-d)/r; else print ""}')
      [ -n "$eta_min" ] && eta_clock=$(date -d "+${eta_min} minutes" '+%a %H:%M')
    fi
  fi

  # ---- alerts -------------------------------------------------------------
  [ "$bad" -gt 0 ] && alerts+="${bad} task(s) not COMPLETED/CACHED. "
  if [ "$alive" = no ]; then
    if [ -n "$exp" ] && [ "$done_n" -ge "$exp" ]; then alerts+="Nextflow exited, scatter complete. "
    else alerts+="NEXTFLOW IS GONE — run stopped early. "; fi
  elif [ -n "$prev_ts" ] && [ "${d_done:-0}" -eq 0 ] \
       && awk -v m="$mins" 'BEGIN{exit !(m>=5)}'; then
    # only meaningful over a real window; back-to-back beats are not a stall
    alerts+="STALLED: no task completed in the last $(printf '%.0f' "$mins") min. "
  fi
  if [ -n "${runway:-}" ] && awk -v r="$runway" -v w="$DISK_WARN_HOURS" 'BEGIN{exit !(r<w)}'; then
    alerts+="Disk runway ${runway}h < ${DISK_WARN_HOURS}h. "
  fi

  # ---- write --------------------------------------------------------------
  {
    printf '\n[%s]  beat %d   nextflow=%s (%s)  stage=%s\n' \
           "$ts" "$beat_no" "$alive" "$elapsed" "${stage:-?}"
    if [ -n "$exp" ]; then
      printf '  SNIPPY_SCATTER  %d / %d  (%s%%)   +%s since last beat\n' \
             "$done_n" "$exp" "${pct:-?}" "${d_done:-0}"
      printf '  rate            %s/min last interval   %s/min over the stage\n' \
             "${rate:-?}" "${trace_rate:-?}"
      [ -n "${eta_min:-}" ] && printf '  scatter ETA     %s  (~%s)\n' \
             "$(fmt_hm "$eta_min")" "${eta_clock:-?}"
    else
      printf '  SNIPPY_SCATTER  %d done (denominator unavailable — no %% reported)\n' "$done_n"
    fi
    printf '  containers %-4s cached %-6s failed/aborted %s\n' "$containers" "$cached" "$bad"
    printf '  disk       %s GB free' "$avail_gb"
    [ -n "${burn:-}" ] && printf '   burn %s GB/h' "$burn"
    [ -n "${runway:-}" ] && printf '   runway %sh' "$runway"
    printf '\n'
    [ -n "$alerts" ] && printf '  ** %s\n' "$alerts"
  } >> "$HB_LOG"

  [ -s "$HB_TSV" ] || printf 'timestamp\tbeat\talive\tstage\tsnippy_done\tsnippy_expected\tdelta\trate_per_min\trate_stage\tavail_gb\tburn_gb_h\tcontainers\tbad\n' > "$HB_TSV"
  printf '%s\t%d\t%s\t%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$ts" "$beat_no" "$alive" "${stage:-?}" "$done_n" "${exp:-NA}" "${d_done:-NA}" \
    "${rate:-NA}" "${trace_rate:-NA}" "$avail_gb" "${burn:-NA}" "$containers" "$bad" >> "$HB_TSV"

  cat > "$STATE" <<EOF
PREV_TS=$(date +%s)
PREV_DONE=$done_n
PREV_AVAIL=$avail_kb
PREV_BEAT=$beat_no
FIRST_TS=$first_ts
FIRST_AVAIL=$first_avail
EOF

  # ---- notify -------------------------------------------------------------
  local body="${done_n}${exp:+/$exp} scatter${pct:+ (${pct}%)}, ${avail_gb} GB free${eta_clock:+, ETA ${eta_clock}}"
  if [ -n "$alerts" ]; then
    notify critical "pp2802: attention" "$alerts"
  elif [ "$NOTIFY_EVERY" -gt 0 ] && [ $((beat_no % NOTIFY_EVERY)) -eq 0 ]; then
    notify low "pp2802 heartbeat" "$body"
  fi

  # stop once the pipeline is no longer running
  if [ "$alive" = no ]; then
    log "  monitor exiting: no nextflow process for pp2802_work"
    rm -f "$PIDFILE"
    exit 0
  fi
}

# ------------------------------------------------------------------- main ---
if [ -s "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "monitor already running as PID $(cat "$PIDFILE")" >&2; exit 1
fi
echo $$ > "$PIDFILE"
trap 'rm -f "$PIDFILE"' EXIT

log "=== monitor started $(now)  interval=${INTERVAL}s  notify_every=${NOTIFY_EVERY} ==="
if [ "$ONCE" = 1 ]; then beat; exit 0; fi
while :; do beat; sleep "$INTERVAL"; done
