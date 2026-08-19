#!/usr/bin/env bash
# Fix the CRLF that killed the v4c SNP run, then launch it.
#
# WHAT HAPPENED (2026-08-18 15:00:15, rc=141, both logs 0 bytes)
#   curated_L1v4c_refs.tsv is CRLF, so every reference_path carries a trailing
#   \r. In bin/run_wf_curated_L1.sh the preflight is
#
#     RMISS=$(awk ... | while read -r f; do [ -f "$f" ] || echo "$f"; done | head -3)
#
#   `read -r` keeps the \r (it is not in IFS), so all 86 paths test as missing.
#   The 4th echo hits a closed pipe because `head -3` already exited -> SIGPIPE
#   -> 141 -> `set -o pipefail` propagates it -> `set -e` aborts the script
#   BEFORE it can print its own "references file points at missing files"
#   diagnostic. Hence rc=141 with a 0-byte log, identically for the dry run.
#
#   Reproduced end-to-end against a copy of the real script and the real
#   refs file: original+CRLF -> rc=141 silent; patched or de-CRLF'd -> rc=0.
#
# Run from ~/v4c_partition on the A100. Safe to re-run; every step is idempotent.
set -euo pipefail
S="${S:-$HOME/v4c_partition}"
cd "$S"

REFS="$S/curated_L1v4c_refs.tsv"
WF="$S/bin/run_wf_curated_L1.sh"

echo "=== 1/4  confirm the diagnosis before changing anything ==="
CR=$(grep -c $'\r' "$REFS" || true)
echo "    CR-terminated lines in curated_L1v4c_refs.tsv : $CR   (expect 87)"
if [ "$CR" -eq 0 ]; then
  echo "    no CRLF here -- the cause is something else. STOP and re-diagnose:"
  echo "      bash -x ./bin/run_wf_curated_L1.sh 2>&1 | tail -40"
  exit 1
fi

echo "=== 2/4  strip the CR (backup kept) ==="
[ -f "$REFS.crlf.bak" ] || cp -p "$REFS" "$REFS.crlf.bak"
sed -i 's/\r$//' "$REFS"
BAD=$(awk -F'\t' 'NR>1{print $2}' "$REFS" | while read -r f; do [ -f "$f" ] || echo "$f"; done | wc -l)
echo "    reference paths that still do not resolve : $BAD   (expect 0)"
[ "$BAD" -eq 0 ] || { echo "    STOP: references genuinely missing, not a line-ending problem."; exit 1; }

echo "=== 3/4  make the preflight incapable of dying silently again ==="
python3 - "$WF" <<'PY'
import sys
p = sys.argv[1]
s = open(p).read()
old = '''| while read -r f; do [ -f "$f" ] || echo "$f"; done | head -3)'''
new = '''| while read -r f; do f=${f%$'\\r'}; [ -f "$f" ] || echo "$f"; done | awk 'NR<=3')'''
n = s.count(old)
if n:
    open(p, "w").write(s.replace(old, new))
    print(f"    patched {n} preflight pipeline(s)")
else:
    print("    already patched")
PY
bash -n "$WF" && echo "    syntax OK"
# awk drains its input so it cannot SIGPIPE the writer; ${f%$'\r'} tolerates CRLF.

echo "=== 4/4  dry run, then the real run ==="
source "$HOME/miniforge3/etc/profile.d/conda.sh"
conda activate nextflow-wf
export JAVA_HOME="$CONDA_PREFIX"; export PATH="$JAVA_HOME/bin:$PATH"
export NXF_ANSI_LOG=false

DRY_RUN=1 ./bin/run_wf_curated_L1.sh > "$S/snp_dryrun.log" 2>&1 && DRC=0 || DRC=$?
echo "    dry run rc=$DRC  ($(wc -c < "$S/snp_dryrun.log") bytes of log)"
if [ "$DRC" -ne 0 ]; then
  echo "    dry run failed -- NOT launching. Last lines:"
  tail -25 "$S/snp_dryrun.log"
  exit 1
fi

echo "    launching the real run detached; it will survive logout"
setsid nohup ./bin/run_wf_curated_L1.sh > "$S/snp_run.log" 2>&1 < /dev/null &
sleep 20
echo "    snp_run.log is now $(wc -c < "$S/snp_run.log") bytes (0 means it died again)"
tail -5 "$S/snp_run.log" || true
echo
echo "Watch:   tail -f $S/snp_run.log"
echo "When it finishes, per-unit verification (exit 0 != every unit succeeded):"
echo "         ./bin/collect_L1_results.sh > $S/L1V4C_RESULTS_SUMMARY.txt"
