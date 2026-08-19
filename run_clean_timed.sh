#!/usr/bin/env bash
# Single-shot clean run with every fix in place, timed end to end.
# Fresh outdir and workdir, no cache, so the elapsed time is a true cold-start
# figure comparable to what a new machine would see.
BASE=/home/phemarajata/Downloads/snp-mod-local-working
START=$(date +%s)
echo "CLEAN RUN START: $(date '+%F %T')" | tee "$BASE/CLEAN_RUN_TIMING.txt"
OUTDIR="$BASE/L1_clean_out" WORKDIR="$BASE/L1_clean_work" bash "$BASE/run_wf_curated_L1.sh"
END=$(date +%s)
{
  echo "CLEAN RUN END:   $(date '+%F %T')"
  echo "ELAPSED SECONDS: $((END-START))"
  printf 'ELAPSED: %dh %dm\n' $(( (END-START)/3600 )) $(( ((END-START)%3600)/60 ))
} | tee -a "$BASE/CLEAN_RUN_TIMING.txt"
