#!/usr/bin/env bash
# FOLLOW-UP RUN: the oversized PopPUNK strains that the main run could not finish.
#
# WHY THIS EXISTS. In the 2,802-genome PopPUNK run, KEEP_INVARIANT_ATCG is
# pinned by the local_workstation_rtx4070 profile to a FIXED 4 GB:
#     withName:KEEP_INVARIANT_ATCG { cpus = 1; memory = '4.GB' }  // peak 1.20 GB
# That figure was measured on the units the manual analysis ran (n <= 155). It
# does not scale with task.attempt, so an OOM (exit 137) retries at the same
# 4 GB and fails identically until maxRetries is exhausted. Measured outcome:
#     strain_3 (n=261, ~1.0 GB alignment)  PASSED at 4 GB
#     strain_2 (n=416, ~1.7 GB alignment)  OOM on replicon 1
#     strain_1 (n=917, ~3.6 GB alignment)  OOM on both replicons
# So the ceiling bites as a function of alignment size, not simply "big strain".
#
# CURATED MODE, DELIBERATELY. The partition and references are supplied from the
# main run's own output rather than re-derived. That bypasses Mash and PopPUNK
# entirely, which:
#   1. removes the stochastic PopPUNK re-fit (two fits of the same data gave 264
#      vs 271 clusters), so this run analyses exactly the strains the main run
#      did, and
#   2. removes the MASH_SKETCH_BATCH cache miss that invalidated the whole
#      downstream chain twice, costing ~6.5 h and then ~27 h of snippy. With no
#      Mash stage there is nothing upstream to rehash, so THIS run is safely
#      resumable.
# The cost is that it does not exercise the FASTA -> PopPUNK path. That path was
# already demonstrated end-to-end by the main run and needs no re-testing.
#
# Edit BIG_STRAINS to whichever strains actually failed -- confirm against
# Summaries/cluster_phylogeny_summary.csv rather than assuming.
set -uo pipefail
source /home/phemarajata/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda deactivate 2>/dev/null || true; conda deactivate 2>/dev/null || true
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export JAVA_CMD="$JAVA_HOME/bin/java"; export PATH="$JAVA_HOME/bin:$PATH"
BASE=/home/phemarajata/Downloads/snp-mod-local-working
MAIN_OUT="${BASE}/pp2802_out"

BIG_STRAINS="${BIG_STRAINS:-strain_1 strain_2}"

# --- subset the main run's partition and references to those strains ---------
python3 - "$MAIN_OUT" "$BASE" $BIG_STRAINS <<'PY'
import csv, sys, os
main_out, base = sys.argv[1], sys.argv[2]
want = set(sys.argv[3:])
rows = [r for r in csv.DictReader(open(os.path.join(main_out,"Summaries","clusters.tsv")), delimiter="\t")
         if r["cluster_id"] in want]
if not rows:
    sys.exit("ERROR: no members found for %s in the main run's clusters.tsv" % sorted(want))
refs = [r for r in csv.DictReader(open(os.path.join(main_out,"Summaries","cluster_references.tsv")), delimiter="\t")
         if r["cluster_id"] in want]
missing = want - {r["cluster_id"] for r in refs}
if missing:
    sys.exit("ERROR: no reference recorded for %s" % sorted(missing))
with open(os.path.join(base,"curated_big_clusters.tsv"),"w",newline="") as fh:
    w=csv.writer(fh,delimiter="\t"); w.writerow(["cluster_id","sample_id"])
    for r in rows: w.writerow([r["cluster_id"], r["sample_id"]])
with open(os.path.join(base,"curated_big_refs.tsv"),"w",newline="") as fh:
    w=csv.writer(fh,delimiter="\t"); w.writerow(["cluster_id","reference_path"])
    for r in refs:
        assert os.path.exists(r["reference_path"]), "missing reference file: "+r["reference_path"]
        w.writerow([r["cluster_id"], r["reference_path"]])
# the samplesheet must cover exactly these genomes
allss = {r["sample"]: r["file"] for r in csv.DictReader(open(os.path.join(base,"wf_2802_samplesheet.csv")))}
with open(os.path.join(base,"wf_big_samplesheet.csv"),"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["sample","file"])
    for r in rows:
        w.writerow([r["sample_id"], allss[r["sample_id"]]])
import collections
print("follow-up scope:", dict(collections.Counter(r["cluster_id"] for r in rows)), "=", len(rows), "genomes")
PY
[ $? -eq 0 ] || exit 1

# --- resource overrides: every per-cluster stage scaled for large alignments --
cat > "${BASE}/bigstrain_overrides.config" <<'CFG'
executor {
    $local { cpus = 20; memory = '52 GB' }
}
process {
    // KEEP_INVARIANT_ATCG is the one the main run tripped over. Fixed 4 GB in
    // the profile; scaled here, since its footprint tracks alignment size
    // (n x genome length) and strain_1's is ~3.6 GB on disk alone.
    withName: 'KEEP_INVARIANT_ATCG' {
        cpus     = 2
        memory   = { task.attempt == 1 ? 24.GB : (task.attempt == 2 ? 36.GB : 48.GB) }
        time     = { task.attempt == 1 ? 12.h  : 24.h }
        maxForks = 2
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'SNIPPY_CORE_GATHER' {
        cpus     = 4
        memory   = { task.attempt == 1 ? 24.GB : (task.attempt == 2 ? 36.GB : 48.GB) }
        time     = { task.attempt == 1 ? 24.h  : 48.h }
        maxForks = 2
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'IQTREE_FAST' {
        cpus = 4
        memory = { task.attempt == 1 ? 16.GB : 32.GB }
        time   = { task.attempt == 1 ? 24.h : 48.h }
        maxForks = 2
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'ASC_PREFLIGHT' {
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'GUBBINS_CLUSTER' {
        cpus     = 8
        memory   = { task.attempt == 1 ? 24.GB : (task.attempt == 2 ? 36.GB : 48.GB) }
        time     = { task.attempt == 1 ? 168.h : 240.h }
        maxForks = 1
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'IQTREE_ASC' {
        cpus     = 8
        memory   = { task.attempt == 1 ? 24.GB : (task.attempt == 2 ? 36.GB : 44.GB) }
        time     = { task.attempt == 1 ? 96.h  : 168.h }
        maxForks = 1
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
}
CFG

cd /home/phemarajata/wf-assembly-snps-mod
nextflow run . \
  -profile bp,local_workstation_rtx4070,docker \
  -c "${BASE}/bigstrain_overrides.config" \
  --input "${BASE}/wf_big_samplesheet.csv" \
  --cluster_assignments "${BASE}/curated_big_clusters.tsv" \
  --cluster_references "${BASE}/curated_big_refs.tsv" \
  --split_replicons true \
  --max_cluster_size 1000 \
  --gubbins_min_snps 3 \
  --gubbins_iterations 5 \
  --gubbins_use_hybrid false \
  --gubbins_skip_starting_tree true \
  --outdir "${BASE}/bigstrain_out" \
  -work-dir "${BASE}/bigstrain_work" \
  -ansi-log false \
  -resume \
  && echo "BIGSTRAIN RUN OK" || echo "BIGSTRAIN RUN FAILED (exit $?)"
echo "FINISHED"
