#!/usr/bin/env bash
# DEFINITIVE RUN: all 35 PopPUNK strains, curated mode, correctly resourced.
#
# Scope: the 35 strains (2,395 genomes) that PopPUNK found in the 2,802-genome
# collection at min_cluster_size 7. The partition and per-strain references are
# taken from the PopPUNK run's own published Summaries/ -- they are NOT
# re-derived.
#
# WHY CURATED MODE, after three attempts in PopPUNK mode.
#   1. RESUMABILITY. In PopPUNK mode, MASH_SKETCH_BATCH misses cache on every
#      restart (its batches come from .collate() over an unordered channel).
#      Default cache hashing includes file TIMESTAMPS, so MASH_TRIANGLE then
#      rewrites a byte-identical matrix with a new mtime, and every downstream
#      task rehashes. Measured three times: the snippy stage was invalidated on
#      every single restart, costing ~6.5 h, then ~27 h, then ~27 h again.
#      With no Mash or PopPUNK stage upstream there is nothing to rehash, so
#      THIS run can actually be resumed.
#   2. DETERMINISM. PopPUNK's bgmm+refine fit is stochastic: two fits of the
#      same 2,802 genomes gave 264 vs 271 clusters (30/35 strains set-identical,
#      4 differing slightly). Re-deriving would silently change the analysis set
#      mid-project. Supplying the partition freezes it.
# The cost is that this does not exercise the FASTA -> PopPUNK path. That path
# is already proven: PopPUNK ran inside the workflow over all 2,802 genomes,
# produced the partition used here, and cached cleanly across three restarts.
#
# RESOURCES. The local_workstation_rtx4070 profile sizes per-cluster stages for
# units of n <= 155 ("measured peak 1.20 GB", "peak 0.89 GB at 27 taxa"). This
# run has strains of 917, 416 and 261. Several profile ceilings are FIXED
# strings, not check_max(x * task.attempt), so an OOM retries at the same memory
# and fails identically -- that is what ended the previous run at 28 h on
# strain_1's KEEP_INVARIANT_ATCG. Every per-cluster stage is scaled below.
#
# ERROR STRATEGY. Note the `task.attempt <= 2` guard: without it the closure
# returns 'retry' for every listed exit code including 137 (OOM), so when
# maxRetries is exhausted the strategy STILL says retry, there are none left,
# and Nextflow terminates the pipeline. The 'ignore' branch is unreachable for
# exactly the codes most likely to exhaust retries.
#
# EXPECTED FAILURES, which are recorded rather than fatal:
#   strain_12 replicons 3 and 4 -- ~2.5 kb pseudo-replicons on a 4-contig
#     reference, present in <2 genomes, so snippy-core refuses them (exit 2).
#   small strains on distant borrowed references (strain_21 n=13 @0.00339,
#     strain_23 n=12 @0.00376) -- too few informative sites for Gubbins to fit
#     a model (exit 1).
#
# WHEN IT FINISHES, read Summaries/cluster_phylogeny_summary.csv and count the
# Tier1 strains. With errorStrategy 'ignore' a zero exit code does NOT mean
# every strain succeeded.
set -uo pipefail
source /home/phemarajata/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda deactivate 2>/dev/null || true; conda deactivate 2>/dev/null || true
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export JAVA_CMD="$JAVA_HOME/bin/java"; export PATH="$JAVA_HOME/bin:$PATH"
BASE=/home/phemarajata/Downloads/snp-mod-local-working
MAIN_OUT="${BASE}/pp2802_out"

# EXCLUDE_STRAINS: strains to leave out of this run, space separated.
#
# strain_1 (n=917) was excluded on 2026-08-15 after its Gubbins ran 10.5 h and
# was still inside ITERATION 1 of 5, with RAxML log-likelihood still improving
# (~15-20 min per optimisation round, 31 and 44 rounds deep on the two
# replicons). Measured scaling on the same run -- n=90 ~13 min, n=261 ~62 min,
# n=416 ~177 min for ALL five iterations -- makes 917 a multi-day job, and
# because it holds 2 x 20 GB of the 52 GB executor budget it blocks IQTREE_ASC
# for every other unit. 56 of 70 units were already complete at that point.
#
# strain_1 is also the unit whose analysis validity is most doubtful: 917
# genomes spanning 12 of the previous analysis's units, with an INTERNAL
# reference at mean Mash 0.00337 -- more distant from its own members than
# several borrowed references are from theirs. Run it separately (see
# run_wf_bigstrains.sh) if it is wanted at all.
EXCLUDE_STRAINS="${EXCLUDE_STRAINS:-}"

# --- build inputs from the PopPUNK run's published partition -----------------
python3 - "$MAIN_OUT" "$BASE" $EXCLUDE_STRAINS <<'PY'
import csv, sys, os, collections
main_out, base = sys.argv[1], sys.argv[2]
exclude = set(sys.argv[3:])
rows = [r for r in csv.DictReader(open(os.path.join(main_out,"Summaries","clusters.tsv")), delimiter="\t")
        if r["cluster_id"] not in exclude]
refs = [r for r in csv.DictReader(open(os.path.join(main_out,"Summaries","cluster_references.tsv")), delimiter="\t")
        if r["cluster_id"] not in exclude]
strains = {r["cluster_id"] for r in rows}
have    = {r["cluster_id"] for r in refs}
missing = strains - have
if missing:
    sys.exit("ERROR: no reference for %s" % sorted(missing))
# PICK_CLUSTER_REFERENCES records the reference as the path it was STAGED at
# inside its own task dir (pp2802_work/xx/yyyy/genomes/<name>.fasta). Those
# paths die with the work dir, so resolve every reference back to the original
# collection by basename instead of trusting what was recorded.
COLL = "/home/phemarajata/Downloads/final_deduped_all_BP_with_locations"
for r in refs:
    if not os.path.exists(r["reference_path"]):
        cand = os.path.join(COLL, os.path.basename(r["reference_path"]))
        if not os.path.exists(cand):
            sys.exit("ERROR: cannot resolve reference %s" % r["reference_path"])
        r["reference_path"] = cand
allss = {r["sample"]: r["file"] for r in csv.DictReader(open(os.path.join(base,"wf_2802_samplesheet.csv")))}
seen = set()
with open(os.path.join(base,"curated_all35_clusters.tsv"),"w",newline="") as fh, \
     open(os.path.join(base,"wf_all35_samplesheet.csv"),"w",newline="") as sh:
    w=csv.writer(fh,delimiter="\t",lineterminator="\n"); w.writerow(["cluster_id","sample_id"])
    s=csv.writer(sh,lineterminator="\n"); s.writerow(["sample","file"])
    for r in rows:
        sid=r["sample_id"]
        if sid in seen: sys.exit("ERROR: duplicate sample %s" % sid)
        seen.add(sid)
        if sid not in allss: sys.exit("ERROR: %s absent from the 2802 samplesheet" % sid)
        w.writerow([r["cluster_id"], sid]); s.writerow([sid, allss[sid]])
with open(os.path.join(base,"curated_all35_refs.tsv"),"w",newline="") as fh:
    w=csv.writer(fh,delimiter="\t",lineterminator="\n"); w.writerow(["cluster_id","reference_path"])
    for r in refs: w.writerow([r["cluster_id"], r["reference_path"]])
c=collections.Counter(r["cluster_id"] for r in rows)
print("curated scope: %d strains, %d genomes (largest %d)%s" % (len(c), len(rows), max(c.values()), (" | EXCLUDED: %s" % sorted(exclude)) if exclude else ""))
PY
[ $? -eq 0 ] || exit 1

cat > "${BASE}/curated_all35_overrides.config" <<'CFG'
executor {
    $local { cpus = 20; memory = '52 GB' }
}
process {
    withName: 'SNIPPY_CORE_GATHER' {
        cpus     = 4
        memory   = { task.attempt == 1 ? 20.GB : (task.attempt == 2 ? 32.GB : 44.GB) }
        time     = { task.attempt == 1 ? 24.h  : 48.h }
        maxForks = 2
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'KEEP_INVARIANT_ATCG' {
        cpus     = 2
        memory   = { task.attempt == 1 ? 20.GB : (task.attempt == 2 ? 32.GB : 44.GB) }
        time     = { task.attempt == 1 ? 12.h  : 24.h }
        maxForks = 2
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'IQTREE_FAST' {
        cpus     = 4
        memory   = { task.attempt == 1 ? 12.GB : 24.GB }
        time     = { task.attempt == 1 ? 24.h  : 48.h }
        maxForks = 3
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'ASC_PREFLIGHT' {
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'GUBBINS_CLUSTER' {
        cpus     = 6
        memory   = { task.attempt == 1 ? 20.GB : (task.attempt == 2 ? 32.GB : 44.GB) }
        time     = { task.attempt == 1 ? 168.h : 240.h }
        maxForks = 2
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'IQTREE_ASC' {
        cpus     = 6
        memory   = { task.attempt == 1 ? 16.GB : (task.attempt == 2 ? 28.GB : 44.GB) }
        time     = { task.attempt == 1 ? 96.h  : 168.h }
        maxForks = 2
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
}
CFG

cd /home/phemarajata/wf-assembly-snps-mod
nextflow run . \
  -profile bp,local_workstation_rtx4070,docker \
  -c "${BASE}/curated_all35_overrides.config" \
  --input "${BASE}/wf_all35_samplesheet.csv" \
  --cluster_assignments "${BASE}/curated_all35_clusters.tsv" \
  --cluster_references "${BASE}/curated_all35_refs.tsv" \
  --split_replicons true \
  --max_cluster_size 1000 \
  --gubbins_min_snps 3 \
  --gubbins_iterations 5 \
  --gubbins_use_hybrid false \
  --gubbins_skip_starting_tree true \
  --outdir "${BASE}/all35_out" \
  -work-dir "${BASE}/all35_work" \
  -ansi-log false \
  -resume \
  && echo "CURATED ALL35 RUN OK" || echo "CURATED ALL35 RUN FAILED (exit $?)"
echo "FINISHED"
