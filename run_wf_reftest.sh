#!/usr/bin/env bash
# REFERENCE-SWAP TEST: is the reference causal for the 6 Gubbins failures?
#
# In the 34-strain curated run, 6 units failed Gubbins with RAxML "Unable to fit
# model to data". The failures are almost perfectly explained by WHICH REFERENCE
# was used, and by nothing else:
#
#   GCF_003798365_1_Thailand_Ubon_Ratchathani   0 OK / 4 FAIL
#   GCF_026315045_1_Australia_Northern_Territory 0 OK / 1 FAIL
#   GCF_002843645_1_Australia_Northern_Territory 0 OK / 1 FAIL
#   all 23 other references                     28 OK / 0 FAIL
#
# RULED OUT with data, none of which separates the two classes:
#   * reference assembly quality -- all 2 contigs, ~7 Mb, N50 ~4 Mb, ~0 non-ACGT
#   * within-strain diversity    -- FAIL 0.00038-0.00357 vs OK 0.00008-0.00352;
#                                   strain_28 at 0.000081 (most clonal) SUCCEEDED
#   * reference distance         -- FAIL 0.0003-0.0052; strain_20 OK at 0.0047,
#                                   and strain_34 FAILED at 0.00041 (near-perfect)
#   * variable site count        -- strain_28 OK on 91 sites, strain_14 FAIL on 1,091
#   * alignment missingness      -- FAIL 0.0386 vs OK 0.0413 (failures cleaner)
#   * invariant-site composition -- normal 68.6% GC profile, all bases non-zero
#
# So: a strong association with no mechanism. This run is the decisive test.
# Each failing strain is re-run against the nearest reference that SUCCEEDED
# elsewhere, holding everything else constant:
#
#   strain_14 -> GCF_000511915_1_Australia        strain_23 -> GCF_000755945_1_Australia
#   strain_15 -> GCF_000755945_1_Australia        strain_33 -> GCF_000511915_1_Australia
#   strain_21 -> GCF_000755905_1_unknown          strain_34 -> GCF_000755905_1_unknown
#
# INTERPRETATION, decided in advance so the result cannot be rationalised after
# the fact:
#   all 6 succeed  -> the reference is causal. Fix the reference picker to
#                     exclude/deprioritise these three, and the failures are a
#                     tooling artefact rather than a property of the strains.
#   all 6 fail     -> the reference is NOT causal; the strains themselves are
#                     unanalysable and should be reported as such.
#   mixed          -> neither; the interaction is strain-specific and needs a
#                     per-unit judgement, not a rule.
#
# Cheap: 100 genomes, 200 snippy tasks, 12 Gubbins runs on small alignments.
set -uo pipefail
source /home/phemarajata/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda deactivate 2>/dev/null || true; conda deactivate 2>/dev/null || true
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export JAVA_CMD="$JAVA_HOME/bin/java"; export PATH="$JAVA_HOME/bin:$PATH"
BASE=/home/phemarajata/Downloads/snp-mod-local-working

cat > "${BASE}/reftest_overrides.config" <<'CFG'
executor { $local { cpus = 20; memory = '52 GB' } }
process {
    withName: 'SNIPPY_CORE_GATHER' {
        cpus = 4; memory = { task.attempt == 1 ? 12.GB : 24.GB }; maxForks = 3
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries = 2
    }
    withName: 'KEEP_INVARIANT_ATCG' {
        cpus = 2; memory = { task.attempt == 1 ? 12.GB : 24.GB }; maxForks = 3
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries = 2
    }
    withName: 'IQTREE_FAST' {
        cpus = 2; memory = 8.GB; maxForks = 3
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries = 2
    }
    withName: 'ASC_PREFLIGHT' {
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries = 2
    }
    withName: 'GUBBINS_CLUSTER' {
        cpus = 4; memory = { task.attempt == 1 ? 12.GB : 24.GB }; maxForks = 3
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries = 2
    }
    withName: 'IQTREE_ASC' {
        cpus = 4; memory = { task.attempt == 1 ? 12.GB : 24.GB }; maxForks = 2
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries = 2
    }
}
CFG

cd /home/phemarajata/wf-assembly-snps-mod
nextflow run . \
  -profile bp,local_workstation_rtx4070,docker \
  -c "${BASE}/reftest_overrides.config" \
  --input "${BASE}/wf_reftest_samplesheet.csv" \
  --cluster_assignments "${BASE}/reftest_clusters.tsv" \
  --cluster_references "${BASE}/reftest_refs.tsv" \
  --split_replicons true \
  --max_cluster_size 1000 \
  --gubbins_min_snps 3 \
  --gubbins_iterations 5 \
  --gubbins_use_hybrid false \
  --gubbins_skip_starting_tree true \
  --outdir "${BASE}/reftest_out" \
  -work-dir "${BASE}/reftest_work" \
  -ansi-log false \
  -resume \
  && echo "REFTEST OK" || echo "REFTEST FAILED (exit $?)"
echo "FINISHED"
