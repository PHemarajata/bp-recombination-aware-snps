#!/usr/bin/env bash
# Local smoke test for the finalized workflow: 9 real B. pseudomallei genomes
# (unit s4_L1_5), no NCBI staging, exercising the clustered Gubbins path we
# changed (RAxML pinned + --invariant-site-correction, container 3.4.3).
set -uo pipefail

# Java: conda base ships Java 11 and .bashrc points JAVA_HOME at a missing env,
# so pin a 17+ JDK explicitly. Deactivating conda alone is not enough because
# miniforge3/bin is still ahead on PATH.
source /home/phemarajata/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda deactivate 2>/dev/null || true
conda deactivate 2>/dev/null || true
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export JAVA_CMD="$JAVA_HOME/bin/java"
export PATH="$JAVA_HOME/bin:$PATH"

cd /home/phemarajata/wf-assembly-snps-mod

SS=/home/phemarajata/Downloads/snp-mod-local-working/smoketest_s4_L1_5_samplesheet.csv
OUT=/home/phemarajata/Downloads/snp-mod-local-working/smoketest_out

exec nextflow run . \
  -profile bp,local_workstation_rtx4070,docker \
  --input "$SS" \
  --outdir "$OUT" \
  -work-dir "$OUT/work" \
  -ansi-log false
