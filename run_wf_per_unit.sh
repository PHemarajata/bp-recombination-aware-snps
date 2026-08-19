#!/usr/bin/env bash
# WORKFLOW-vs-MANUAL, with the partition held constant (option B).
#
# WHY PER-UNIT. Feeding the workflow all 2,802 genomes made it cluster with Mash,
# which at threshold 0.028 collapsed the whole collection into ONE connected
# component that was then chopped into 60 size-capped parts (gini 0.059, sizes
# pinned at the 50 cap -- an IMPOSED partition, below even Wu's deliberately
# imposed 10-way cut at 0.095). A threshold sweep on the real distance matrix
# showed no threshold works: the collection fuses into one blob between 0.005 and
# 0.007 -- straddling the bp profile's own suggested 0.005-0.007 range -- and
# tighter values shatter into hundreds of singletons. Single-linkage Mash cannot
# partition this collection, which independently reproduces why the project
# moved to PopPUNK/fastbaps.
#
# The pipeline has no way to accept a pre-defined partition (CLUSTER_GENOMES is
# hardwired). So instead we give it ONE UNIT AT A TIME: with only that unit's
# genomes as input, clustering has nothing to do but recover the unit itself, and
# the workflow analyses exactly the genome set the manual pipeline analysed.
#
# WHAT THIS ISOLATES. Both these units were ALSO re-called manually with snippy
# (snippy_s1_L1_19/, snippy_s1_L1_9/), so the caller is held constant too:
#     workflow(snippy) vs manual-snippy  ==  PURE WORKFLOW TEST
# Remaining confound, stated not hidden: the workflow picks its own reference
# (medoid of the cluster) while the manual runs used a specified close reference.
#
# max_cluster_size is raised to 200 so a unit is never split by the size cap
# (s1_L1_9 has n=90, which the default 50 would have chopped in two).
set -uo pipefail

source /home/phemarajata/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda deactivate 2>/dev/null || true
conda deactivate 2>/dev/null || true
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export JAVA_CMD="$JAVA_HOME/bin/java"
export PATH="$JAVA_HOME/bin:$PATH"

BASE=/home/phemarajata/Downloads/snp-mod-local-working
cd /home/phemarajata/wf-assembly-snps-mod

for UNIT in "$@"; do
  SS="${BASE}/wf_${UNIT}_samplesheet.csv"
  OUT="${BASE}/wf_${UNIT}_out"
  WORK="${BASE}/wf_${UNIT}_work"
  echo "=== WORKFLOW on ${UNIT} ==="
  mkdir -p "$OUT" "$WORK"
  nextflow run . \
    -profile bp,local_workstation_rtx4070,docker \
    --input "$SS" \
    --outdir "$OUT" \
    --max_cluster_size 200 \
    -work-dir "$WORK" \
    -ansi-log false \
    && echo "UNIT ${UNIT} OK" || echo "UNIT ${UNIT} FAILED (exit $?)"
done
echo "ALL UNITS FINISHED"
