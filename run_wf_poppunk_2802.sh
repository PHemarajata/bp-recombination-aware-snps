#!/usr/bin/env bash
# FASTA-ONLY 2,802-GENOME RUN, PARTITIONED BY POPPUNK INSIDE THE WORKFLOW.
#
# 2,802 FASTAs in. PopPUNK (create-db -> bgmm -> refine) partitions them, the
# n >= 7 gate keeps 34 strains covering 2,382 genomes, each strain gets a
# COMPLETE reference (internal where one exists, otherwise the nearest complete
# genome borrowed from the collection), the reference is split per replicon, and
# each replicon runs SNIPPY -> GUBBINS -> IQTREE_ASC at production Gubbins
# settings.
#
# WHY POPPUNK AND NOT MASH. Mash single-linkage cannot partition this
# collection: one connected component at threshold >= 0.007, 786/1,094
# singletons below it, nothing workable between. PopPUNK's refined fit gives 271
# strains, 100% of the collection assigned.
#
# WHY --pick_complete_references IS NOT OPTIONAL HERE. 2,541 of 2,802 genomes
# (90.7%) are drafts. A medoid representative is therefore usually multi-contig,
# and --split_replicons fails loudly on anything over --max_replicons. Most
# strains will use a BORROWED reference; that path is the common case, not an
# edge case.
#
# ERROR STRATEGY OVERRIDE, and this is the reason for the -c file below.
# The local_workstation_rtx4070 profile sets errorStrategy 'finish' for
# non-retryable exits. Gubbins exits 1 when RAxML cannot fit a model to a
# cluster's data -- observed on real (if degenerate) input during testing. With
# 'finish', ONE such strain out of 34 terminates the whole multi-day run. The
# HPC profiles in this repo already use 'ignore' for exactly this reason, and
# SUMMARIZE_CLUSTER_PHYLOGENY's Tier system exists to record per-cluster
# failures -- i.e. failures were designed to be survivable. Override GUBBINS and
# IQTREE only, so a strain that cannot be analysed is reported as Tier3/Tier4
# rather than taking everything else down with it.
#
# CHECK THE SUMMARY WHEN IT FINISHES. Silence is not success: read
# Summaries/cluster_phylogeny_summary.csv and count how many strains actually
# reached Tier1, rather than trusting the exit code.
set -uo pipefail
source /home/phemarajata/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda deactivate 2>/dev/null || true; conda deactivate 2>/dev/null || true
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export JAVA_CMD="$JAVA_HOME/bin/java"; export PATH="$JAVA_HOME/bin:$PATH"
BASE=/home/phemarajata/Downloads/snp-mod-local-working

# RESOURCE OVERRIDES.
#
# The local_workstation_rtx4070 profile sizes the per-cluster stages for the
# units the manual analysis actually ran -- its GUBBINS_CLUSTER comment says
# "measured peak 0.89 GB at 27 taxa; headroom for 50". This run feeds them
# PopPUNK strains of 917, 416 and 261, which is 20x larger than that budget was
# built for, so every downstream stage needs raising:
#
#   stage               profile default   why it is not enough at 917 taxa
#   SNIPPY_CORE_GATHER  4 GB /  4 h       merges 917 sample dirs into a
#                                         ~3.6 GB full-genome alignment
#   IQTREE_FAST         4 GB /  4 h       917-taxon starting tree
#   GUBBINS_CLUSTER     6 GB / 24 h       pyjar ancestral reconstruction scales
#                                         with taxa x sites; 5 RAxML iterations
#   IQTREE_ASC          4 GB / 12 h       917-taxon ML tree + ASC correction
#
# Memory escalates explicitly per attempt rather than via check_max(), which is
# not in scope in an external -c file. The ladder stops below max_memory (58 GB)
# so a retry can always still be scheduled -- an allocation above the executor
# limit would never run at all, which is worse than an OOM.
#
# The executor block caps total concurrent usage so the raised per-task figures
# cannot collectively oversubscribe the box (22 cores / 62 GB, with other
# containers of the user's also running).
#
# errorStrategy 'ignore' on the two per-cluster stages: with 'finish' (this
# profile's default) one unanalysable strain out of 35 kills the whole run after
# hours or days. The repo's HPC profiles already use 'ignore', and
# SUMMARIZE_CLUSTER_PHYLOGENY's Tier system exists to record per-cluster
# failures -- they were designed to be survivable.
# cache 'lenient' -- WHY THIS MATTERS MORE THAN IT LOOKS.
# Nextflow's default cache mode hashes input files by name, size AND last
# modified timestamp. Any regenerated-but-identical intermediate therefore
# rehashes and invalidates everything downstream. That is exactly what cost 6.5
# hours of snippy on the first restart: MASH_SKETCH_BATCH missed cache (its
# batches come from .collate() over an unordered channel), so MASH_TRIANGLE
# rewrote a byte-identical matrix with a new timestamp, PICK_CLUSTER_REFERENCES
# rewrote byte-identical references, and all ~3,000 snippy tasks rehashed.
# 'lenient' hashes name and size only. Safe here because regeneration is
# verified deterministic: the re-derived partition and reference selection came
# back identical (35 strains, 2,395 genomes, 19 internal / 16 borrowed).
cat > "${BASE}/poppunk_run_overrides.config" <<'CFG'
executor {
    $local {
        cpus   = 20
        memory = '52 GB'
    }
}

process {
    // NOTE the `task.attempt <= 2` guard. Without it the closure returns
    // 'retry' for every listed exit code, INCLUDING 137 (OOM) -- so once
    // maxRetries is exhausted the strategy still says 'retry', there are no
    // retries left, and Nextflow terminates the whole pipeline. The 'ignore'
    // branch is unreachable for exactly the codes most likely to exhaust
    // retries. That killed the 2,802-genome run 28 h in, on strain_1's
    // KEEP_INVARIANT_ATCG OOM, while exit-1 and exit-2 failures were correctly
    // ignored throughout.
    //
    // errorStrategy 'ignore' on EVERY per-cluster stage, not just Gubbins.
    // A degenerate replicon fails at whichever stage first demands sane data,
    // and that is often SNIPPY_CORE_GATHER rather than Gubbins: strain_12's
    // reference has 4 contigs, and its replicon 4 is a small plasmid present in
    // fewer than 2 genomes, so snippy-core correctly refused to build an
    // alignment from <2 samples and exited 2. Covering only GUBBINS_CLUSTER and
    // IQTREE_ASC left that hole, and one plasmid killed a 17-hour run.
    //
    // DO NOT add `cache = 'lenient'` here. It was tried on 2026-08-13 to survive
    // regenerated-but-identical intermediates, and it invalidated the ENTIRE
    // cache instead: changing cache mode changes how task hashes are computed,
    // so every previously completed task missed and the run restarted from
    // INFILE_HANDLING_UNIX with 0 cached. errorStrategy and resource directives
    // are NOT part of the hash and can be changed freely on a resume; the cache
    // mode is not.
    withName: 'SNIPPY_CORE_GATHER' {
        cpus     = 4
        memory   = { task.attempt == 1 ? 16.GB : (task.attempt == 2 ? 28.GB : 40.GB) }
        time     = { task.attempt == 1 ? 24.h  : 48.h }
        maxForks = 2
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'IQTREE_FAST' {
        cpus     = 4
        memory   = { task.attempt == 1 ? 12.GB : (task.attempt == 2 ? 24.GB : 40.GB) }
        time     = { task.attempt == 1 ? 24.h  : 48.h }
        maxForks = 3
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'KEEP_INVARIANT_ATCG' {
        // Profile pins this to a FIXED 4 GB ("measured peak 1.20 GB"), sized on
        // units of n <= 155 and NOT scaled by attempt. Its footprint tracks
        // alignment size: strain_3 (n=261, ~1.0 GB) passed at 4 GB, strain_2
        // (n=416, ~1.7 GB) OOMed on one replicon, strain_1 (n=917, ~3.6 GB)
        // OOMed on both. A fixed ceiling means the retry fails identically.
        cpus     = 2
        memory   = { task.attempt == 1 ? 24.GB : (task.attempt == 2 ? 36.GB : 48.GB) }
        time     = { task.attempt == 1 ? 12.h  : 24.h }
        maxForks = 2
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'ASC_PREFLIGHT' {
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'GUBBINS_CLUSTER' {
        cpus     = 6
        memory   = { task.attempt == 1 ? 20.GB : (task.attempt == 2 ? 36.GB : 48.GB) }
        time     = { task.attempt == 1 ? 96.h  : 168.h }
        maxForks = 2
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'IQTREE_ASC' {
        cpus     = 6
        memory   = { task.attempt == 1 ? 16.GB : (task.attempt == 2 ? 28.GB : 44.GB) }
        time     = { task.attempt == 1 ? 48.h  : 96.h }
        maxForks = 2
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
}
CFG

cd /home/phemarajata/wf-assembly-snps-mod
nextflow run . \
  -profile bp,local_workstation_rtx4070,docker \
  -c "${BASE}/poppunk_run_overrides.config" \
  --input "${BASE}/wf_2802_samplesheet.csv" \
  --clustering_method poppunk \
  --min_cluster_size 7 \
  --pick_complete_references true \
  --split_replicons true \
  --max_cluster_size 1000 \
  --gubbins_min_snps 3 \
  --gubbins_iterations 5 \
  --gubbins_use_hybrid false \
  --gubbins_skip_starting_tree true \
  --outdir "${BASE}/pp2802_out" \
  -work-dir "${BASE}/pp2802_work" \
  -ansi-log false \
  -resume \
  && echo "POPPUNK 2802 RUN OK" || echo "POPPUNK 2802 RUN FAILED (exit $?)"
echo "FINISHED"
