#!/usr/bin/env bash
# FASTA-ONLY RUN over the full 2,802-genome collection.
#
# This is the DEFAULT pipeline path: no --cluster_assignments, no
# --cluster_references. The workflow does its own Mash sketching, clustering and
# medoid-representative selection, then the per-cluster
# SNIPPY -> GUBBINS -> IQTREE_ASC chain, then backbone + graft. It answers
# "what does this pipeline do when handed nothing but FASTAs?"
#
# THREE THINGS TO EXPECT, all measured beforehand -- see handoff §5 and below.
#
# 1. THE PARTITION WILL BE IMPOSED, NOT FOUND. Handoff §5: at mash_threshold
#    0.028 the whole collection is ONE connected component, chopped into
#    size-capped parts (Gini 0.059, max/min 2.78). A threshold sweep on the real
#    matrix found NO value that works -- it fuses into one component between
#    0.005 and 0.007 and shatters into 786/1,094 singletons below. Single-linkage
#    chains straight through this collection. Cluster boundaries from this run
#    are therefore an artefact of the size cap, not biology, and r/m values
#    computed within them are NOT comparable to the curated per-unit baselines.
#
# 2. NO REPLICON SPLIT. --split_replicons is deliberately omitted: it requires a
#    reference with <= --max_replicons (4) contigs, and 2,541 of the 2,802
#    genomes (90.7%) are drafts, so a Mash-selected medoid will almost certainly
#    be one and the run would fail loudly by design (4a10de4). The consequence is
#    that Gubbins sees a whole-genome alignment spanning chromosome I and II and
#    its 0.1-10 kb sliding window scans across the junction -- which this
#    project's own methods reject for B. pseudomallei. This run tests the
#    pipeline path; it does not produce publishable r/m.
#
# 3. IT IS BIG. 2,802 genomes. Handoff §8 records a full run's work dir reaching
#    254 GB, and the earlier attempt was killed at ~20 min once the partition was
#    seen to be meaningless. -work-dir MUST stay on /home, never /tmp.
#
# Gubbins runs at PRODUCTION settings so that anything it does produce is at
# least internally comparable to the fidelity results (see handoff §9).
set -uo pipefail
source /home/phemarajata/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda deactivate 2>/dev/null || true; conda deactivate 2>/dev/null || true
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export JAVA_CMD="$JAVA_HOME/bin/java"; export PATH="$JAVA_HOME/bin:$PATH"
BASE=/home/phemarajata/Downloads/snp-mod-local-working
cd /home/phemarajata/wf-assembly-snps-mod
nextflow run . \
  -profile bp,local_workstation_rtx4070,docker \
  --input "${BASE}/wf_2802_samplesheet.csv" \
  --gubbins_min_snps 3 \
  --gubbins_iterations 5 \
  --gubbins_use_hybrid false \
  --gubbins_skip_starting_tree true \
  --outdir "${BASE}/full2802_out" \
  -work-dir "${BASE}/full2802_work" \
  -ansi-log false \
  -resume \
  && echo "FASTA-ONLY 2802 RUN OK" || echo "FASTA-ONLY 2802 RUN FAILED (exit $?)"
echo "FINISHED"
