#!/usr/bin/env bash
# FULL WORKFLOW RUN -- 2,802 B. pseudomallei genomes.
#
# CALLER DECISION: snippy (the bp profile default). Rationale in the handoff --
# an estimator's sensitivity must not depend on the quantity it estimates, and
# ska map's split k-mers lose ~85% of SNPs within 10 bp, which is exactly the
# density Gubbins reads as recombination. The competing explanation (snippy
# inflating via mismapping) was tested twice and refuted.
#
# HOW THE COMPARISON WORKS. The manual analysis used ska map, so
# workflow-vs-manual confounds workflow with caller. The bridge is
# s1_L1_19 and s1_L1_9: both were re-called manually WITH SNIPPY, so
#   workflow(snippy) vs manual-snippy on those two = PURE WORKFLOW TEST
#   workflow(snippy) vs manual-ska on all 26      = workflow + caller
# Anchor any discrepancy on the first before blaming the second.
#
# DISK: archived run needed ~254 GB work + ~20 GB results. -work-dir is pinned
# to /home deliberately; /tmp is far too small and this is where it lands.
set -uo pipefail

# Java: conda base ships Java 11 and .bashrc pointed JAVA_HOME at a missing env.
# Deactivating conda alone is NOT enough -- miniforge3/bin stays ahead on PATH.
source /home/phemarajata/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda deactivate 2>/dev/null || true
conda deactivate 2>/dev/null || true
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export JAVA_CMD="$JAVA_HOME/bin/java"
export PATH="$JAVA_HOME/bin:$PATH"

cd /home/phemarajata/wf-assembly-snps-mod

IN=/home/phemarajata/Downloads/final_deduped_all_BP_with_locations
OUT=/home/phemarajata/Downloads/snp-mod-local-working/fullrun_out
WORK=/home/phemarajata/Downloads/snp-mod-local-working/fullrun_work

mkdir -p "$OUT" "$WORK"

exec nextflow run . \
  -profile bp,local_workstation_rtx4070,docker \
  --input "$IN" \
  --outdir "$OUT" \
  -work-dir "$WORK" \
  -ansi-log false \
  -resume
