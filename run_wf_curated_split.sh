#!/usr/bin/env bash
# FEATURE 3 VALIDATION: workflow in curated + split mode vs the manual snippy
# baseline, with partition, reference, replicon AND caller all held constant.
#   manual snippy: s1_L1_19 chr1 2.03 / chr2 1.89 ; s1_L1_9 chr1 5.11 / chr2 6.28
# If the workflow reproduces these per-replicon r/m values, it faithfully
# reproduces the manual pipeline and the whole comparison is validated.
set -uo pipefail
source /home/phemarajata/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda deactivate 2>/dev/null || true; conda deactivate 2>/dev/null || true
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export JAVA_CMD="$JAVA_HOME/bin/java"; export PATH="$JAVA_HOME/bin:$PATH"
BASE=/home/phemarajata/Downloads/snp-mod-local-working
cd /home/phemarajata/wf-assembly-snps-mod
for UNIT in "$@"; do
  echo "=== CURATED+SPLIT workflow on ${UNIT} ==="
  nextflow run . \
    -profile bp,local_workstation_rtx4070,docker \
    --input "${BASE}/wf_${UNIT}_samplesheet.csv" \
    --cluster_assignments "${BASE}/curated_${UNIT}_clusters.tsv" \
    --cluster_references "${BASE}/curated_${UNIT}_refs.tsv" \
    --split_replicons true \
    --max_cluster_size 200 \
    --outdir "${BASE}/cs_${UNIT}_out" \
    -work-dir "${BASE}/cs_${UNIT}_work" \
    -ansi-log false \
    && echo "UNIT ${UNIT} OK" || echo "UNIT ${UNIT} FAILED (exit $?)"
done
echo "ALL UNITS FINISHED"
