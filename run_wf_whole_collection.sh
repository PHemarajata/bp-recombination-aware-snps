#!/usr/bin/env bash
# WHOLE-COLLECTION RUN -- curated + split, production Gubbins settings.
#
# Scope: the 45 analysable units (1,233 distinct genomes) from
# analysable_units.tsv, minus s13_L1_1. Curated mode can only cover genomes that
# already have a partition, and §5 of the handoff established that Mash cannot
# produce one for the rest of the 2,802 -- so these 45 units ARE the whole
# collection in the only sense the pipeline can act on.
#
# s13_L1_1 (n=31) is dropped because strain_13 (n=36) fully contains it: all 31
# genomes are shared. Analysing both would yield two non-independent r/m values
# from the same genomes. strain_13 is kept because it has a decided reference in
# analysable_references_final.tsv and s13_L1_1 is the only one of the 46 without
# one. User-confirmed 2026-08-13.
#
# Inputs are generated, not hand-written -- see the build step in the session log:
#   curated_all_clusters.tsv   cluster_id -> sample_id, 45 units, no duplicates
#   curated_all_refs.tsv       cluster_id -> refs/<unit>_close.fasta (all 2-contig)
#   wf_all_samplesheet.csv     sample -> FASTA path, all verified to exist
#
# Gubbins runs at PRODUCTION settings, matching the fidelity check that
# reproduced all four frozen baselines (see §9). Do NOT drop these four flags:
# at the pipeline's speed defaults the same alignments give 0.47-0.78x of target,
# non-uniformly, so the results would not be comparable to the manual baselines
# or to each other.
#
# Expect this to be long and disk-hungry: 45 units x 2 replicons = 90 Gubbins
# runs, each at 5 iterations with its own RAxML first tree. Handoff §8 records a
# full run's work dir reaching 254 GB -- keep an eye on free space.
set -uo pipefail
source /home/phemarajata/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda deactivate 2>/dev/null || true; conda deactivate 2>/dev/null || true
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export JAVA_CMD="$JAVA_HOME/bin/java"; export PATH="$JAVA_HOME/bin:$PATH"
BASE=/home/phemarajata/Downloads/snp-mod-local-working
cd /home/phemarajata/wf-assembly-snps-mod
nextflow run . \
  -profile bp,local_workstation_rtx4070,docker \
  --input "${BASE}/wf_all_samplesheet.csv" \
  --cluster_assignments "${BASE}/curated_all_clusters.tsv" \
  --cluster_references "${BASE}/curated_all_refs.tsv" \
  --split_replicons true \
  --max_cluster_size 200 \
  --gubbins_min_snps 3 \
  --gubbins_iterations 5 \
  --gubbins_use_hybrid false \
  --gubbins_skip_starting_tree true \
  --outdir "${BASE}/whole_out" \
  -work-dir "${BASE}/whole_work" \
  -ansi-log false \
  -resume \
  && echo "WHOLE-COLLECTION RUN OK" || echo "WHOLE-COLLECTION RUN FAILED (exit $?)"
echo "FINISHED"
