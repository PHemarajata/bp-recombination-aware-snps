#!/usr/bin/env bash
# FIDELITY CHECK: curated + split, with the LAST free variable closed.
#
# The 10d1669 re-run confirmed the alignment is right (total SNPs within 0.7% of
# the manual arms, Reference kept, kept_fraction 1.0) but pooled r/m still came
# in at 0.47-0.78x of target, because Gubbins was still running at the pipeline
# author's speed settings. This run matches the production Gubbins invocation:
#
#   run_gubbins.py --prefix ... --threads ... --invariant-site-correction \
#                  --filter-percentage 25  aln.full.<replicon>.fa
#
# i.e. NO --min-snps (default 3), NO --iterations (default 5), NO --tree-builder
# (default raxml), NO --starting-tree. So:
#   gubbins_min_snps            2     -> 3    (Gubbins default)
#   gubbins_iterations          3     -> 5    (Gubbins default)
#   gubbins_use_hybrid          true  -> false
#   gubbins_skip_starting_tree  false -> true (substitutes assets/NO_FILE)
# tree_builder/first_tree_builder are already "raxml" and filter_percentage is
# already 25, so they are left at their defaults.
#
# Targets (pooled r/m = sum SNPs inside recombinations / sum outside, which
# reproduces the frozen values exactly -- median and mean do not):
#   s1_L1_19 chr1 2.0342 / chr2 1.8855 ; s1_L1_9 chr1 5.1075 / chr2 6.2825
#
# Expect this to be SLOWER than the 10d1669 run: 5 iterations instead of 3, and
# Gubbins builds its own first tree with RAxML instead of being handed one.
set -uo pipefail
source /home/phemarajata/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda deactivate 2>/dev/null || true; conda deactivate 2>/dev/null || true
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export JAVA_CMD="$JAVA_HOME/bin/java"; export PATH="$JAVA_HOME/bin:$PATH"
BASE=/home/phemarajata/Downloads/snp-mod-local-working
cd /home/phemarajata/wf-assembly-snps-mod
for UNIT in "$@"; do
  echo "=== FIDELITY (production Gubbins params) on ${UNIT} ==="
  nextflow run . \
    -profile bp,local_workstation_rtx4070,docker \
    --input "${BASE}/wf_${UNIT}_samplesheet.csv" \
    --cluster_assignments "${BASE}/curated_${UNIT}_clusters.tsv" \
    --cluster_references "${BASE}/curated_${UNIT}_refs.tsv" \
    --split_replicons true \
    --max_cluster_size 200 \
    --gubbins_min_snps 3 \
    --gubbins_iterations 5 \
    --gubbins_use_hybrid false \
    --gubbins_skip_starting_tree true \
    --outdir "${BASE}/fid_${UNIT}_out" \
    -work-dir "${BASE}/fid_${UNIT}_work" \
    -ansi-log false \
    && echo "UNIT ${UNIT} OK" || echo "UNIT ${UNIT} FAILED (exit $?)"
done
echo "ALL UNITS FINISHED"
