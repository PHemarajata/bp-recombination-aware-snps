#!/usr/bin/env bash
# DEFINITIVE RUN: 82 fastbaps L1 units, curated mode.
#
# THE PARTITION RULE, applied uniformly:
#   PopPUNK defines strains. fastbaps (PopPIPE, levels=3) subdivides within each
#   strain. Analysis units are fastbaps LEVEL 1 subclusters, kept at n >= 7.
#   A strain fastbaps does not split yields one L1 unit; no strain is subdivided
#   because it is large and none is left whole because it is small.
#
# WHY THIS REPLACES THE all35 RUN. That run analysed the 35 PopPUNK strains
# whole. Its three largest swallowed 12, 9 and 5 of the previous analysis's
# units, and strain_2 returned r/m = 10.31 against a manual-analysis maximum of
# 6.28 -- both replicons agreeing to 4 s.f., which shows the estimate is PRECISE,
# not that it is VALID. High r/m is exactly the signature of inferring
# recombination across nine lumped populations. Subdividing only the inconvenient
# strains would have been a post-hoc size-based cut; the rule above is applied to
# all 35.
#
# SCOPE, versus what came before:
#   this run          82 units, 2,070 genomes, 73.9% of the 2,802 collection
#   all35 run         35 units, 2,395 genomes, but at the wrong granularity
#   manual analysis   37 units, 1,051 genomes
#
# COST. Subdividing makes this run CHEAPER, not dearer, because Gubbins scales
# superlinearly (measured: n=90 ~13 min, n=261 ~62 min, n=416 ~177 min per
# replicon at 5 iterations; strain_1 at n=917 was still inside iteration 1 after
# 10.5 h and was killed). The largest unit here is n=155. Fitting those measured
# points gives t ~ 0.006 * n^1.71 min, so the whole Gubbins stage is ~6 h serial,
# ~2 h at maxForks 3. Mapping dominates instead: ~2,070 snippy jobs.
#
# REFERENCES. Chosen by completeness-gate + centrality-ranking, with the three
# empirically bad references blocklisted (reference_blocklist.txt). All 82 units
# sit within Mash 0.005 of their reference -- SKA2's strain boundary -- median
# 0.00236. Note 18 of the 31 references in use have never been exercised in a
# successful run, covering ~975 genomes; at the observed 3-in-26 failure rate
# expect roughly two more bad references to surface here. That is what
# retry_failed_references.sh is for; do not treat a Gubbins model-fit failure as
# a property of the population until the alternate reference has been tried.
#
# ERROR STRATEGY. Note the `task.attempt <= 2` guard: without it the closure
# returns 'retry' for every listed exit code including 137 (OOM), so when
# maxRetries is exhausted the strategy STILL says retry, there are none left, and
# Nextflow terminates the pipeline. That killed a 28-hour run.
#
# CURATED MODE IS NOT OPTIONAL FOR A RUN THIS LONG. In PopPUNK mode
# MASH_SKETCH_BATCH misses cache on every restart (batches come from .collate()
# over an unordered channel), default cache hashing includes file TIMESTAMPS, so
# MASH_TRIANGLE rewrites a byte-identical matrix with a new mtime and everything
# downstream rehashes. Measured three times: the snippy stage was invalidated on
# every restart -- ~6.5 h, then ~27 h, then ~27 h. The curated resume preserved
# 3,668 of 3,685 snippy tasks. Never set `cache = 'lenient'` to work around it:
# it changes how hashes are computed and invalidates the ENTIRE cache.
#
# WHEN IT FINISHES, read Summaries/cluster_phylogeny_summary.csv and count Tier1
# units. With errorStrategy 'ignore' a zero exit code does NOT mean every unit
# succeeded. Then run collect_L1_results.sh before quoting any figure -- six
# appendix numbers in this project were once computed from a partial run.
set -uo pipefail
source "${CONDA_SH:-/home/phemarajata/miniforge3/etc/profile.d/conda.sh}" 2>/dev/null || true
conda deactivate 2>/dev/null || true; conda deactivate 2>/dev/null || true
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export JAVA_CMD="$JAVA_HOME/bin/java"; export PATH="$JAVA_HOME/bin:$PATH"
# BASE/NFDIR/PROFILE/COLLDIR/OVERRIDES: everything machine-specific, in one place.
# Defaults are the workstation; the A100 stage sets them in run_a100.sh.
BASE="${BASE:-/home/phemarajata/Downloads/snp-mod-local-working}"
NFDIR="${NFDIR:-/home/phemarajata/wf-assembly-snps-mod}"
PROFILE="${PROFILE:-bp,local_workstation_rtx4070,docker}"
COLLDIR="${COLLDIR:-/home/phemarajata/Downloads/final_deduped_all_BP_with_locations}"
OVERRIDES="${OVERRIDES:-}"   # if set, used verbatim instead of the generated config
export COLLDIR

# EXCLUDE_UNITS: L1 units to leave out, space separated, e.g.
#   EXCLUDE_UNITS="strain_1_L1_27 strain_2_L1_6" ./run_wf_curated_L1.sh
# CLUSTERS/REFS: override to re-drive a subset, which is how
# retry_failed_references.sh promotes units to their alternate reference.
EXCLUDE_UNITS="${EXCLUDE_UNITS:-}"
CLUSTERS="${CLUSTERS:-${BASE}/curated_L1_clusters.tsv}"
REFS="${REFS:-${BASE}/curated_L1_refs.tsv}"
OUTDIR="${OUTDIR:-${BASE}/L1_out}"
WORKDIR="${WORKDIR:-${BASE}/L1_work}"
# ALLSS: canonical sample -> assembly path map the run samplesheet is built FROM.
# GENSS: the samplesheet this script WRITES and nextflow then reads.
# Override both together to drive a different panel, e.g. the v4b 2,973 set.
ALLSS="${ALLSS:-${BASE}/wf_2802_samplesheet.csv}"
GENSS="${GENSS:-${BASE}/wf_L1_samplesheet.csv}"
export ALLSS GENSS
# RESUME_SESSION: resume a SPECIFIC nextflow session id instead of "the last one".
#
# Bare `-resume` resumes whatever ran most recently in the project directory --
# and that includes `nextflow run -preview` invocations, which register a session
# with zero cached tasks. Measured: two preview runs used to compile-check a
# change silently became "the last session", so the next -resume re-executed the
# whole pipeline instead of reusing an 11-hour run. Find the id with
#   awk -F'\t' '{print $1, $3, $6}' ~/wf-assembly-snps-mod/.nextflow/history
RESUME_SESSION="${RESUME_SESSION:-}"

# --- build the samplesheet and filtered inputs -------------------------------
python3 - "$BASE" "$CLUSTERS" "$REFS" $EXCLUDE_UNITS <<'PY'
import csv, sys, os, collections, io
sys.path.insert(0, sys.argv[1])
from write_if_changed_bp import write_if_changed
base, clusters_in, refs_in = sys.argv[1], sys.argv[2], sys.argv[3]
exclude = set(sys.argv[4:])

rows = [r for r in csv.DictReader(open(clusters_in), delimiter="\t")
        if r["cluster_id"] not in exclude]
refs = [r for r in csv.DictReader(open(refs_in), delimiter="\t")
        if r["cluster_id"] not in exclude]
if not rows:
    sys.exit("ERROR: every unit excluded, nothing to run")

units = {r["cluster_id"] for r in rows}
have  = {r["cluster_id"] for r in refs}
if units - have:
    sys.exit("ERROR: no reference for %s" % sorted(units - have))

# Resolve every reference against the live collection. A reference recorded by
# an in-workflow PICK_CLUSTER_REFERENCES is the path it was STAGED at inside its
# own task dir, which dies with the work dir.
COLL = os.environ["COLLDIR"]
for r in refs:
    if not os.path.exists(r["reference_path"]):
        cand = os.path.join(COLL, os.path.basename(r["reference_path"]))
        if not os.path.exists(cand):
            sys.exit("ERROR: cannot resolve reference %s" % r["reference_path"])
        r["reference_path"] = cand

allss = {r["sample"]: r["file"]
         for r in csv.DictReader(open(os.environ["ALLSS"]))}

# Build in memory, then write ONLY if the content changed. Nextflow's default
# cache hashing includes file mtime, so rewriting byte-identical inputs
# invalidates every downstream task -- measured: a no-op resume resubmitted all
# 2,070 INFILE_HANDLING tasks and was about to redo 4,140 snippy jobs.
seen = set()
cbuf, sbuf = io.StringIO(), io.StringIO()
# lineterminator="\n" everywhere: csv.writer defaults to CRLF, splitCsv then
# carries a trailing \r into reference_path and checkIfExists fails.
w = csv.writer(cbuf, delimiter="\t", lineterminator="\n"); w.writerow(["cluster_id", "sample_id"])
s = csv.writer(sbuf, lineterminator="\n"); s.writerow(["sample", "file"])
for r in rows:
    sid = r["sample_id"]
    if sid in seen:
        sys.exit("ERROR: %s appears in more than one unit" % sid)
    seen.add(sid)
    if sid not in allss:
        sys.exit("ERROR: %s absent from %s" % (sid, os.environ["ALLSS"]))
    w.writerow([r["cluster_id"], sid])
    s.writerow([sid, allss[sid]])

rbuf = io.StringIO()
w = csv.writer(rbuf, delimiter="\t", lineterminator="\n"); w.writerow(["cluster_id", "reference_path"])
for r in refs:
    if r["cluster_id"] in units:
        w.writerow([r["cluster_id"], r["reference_path"]])

changed = []
for name, buf in ((".L1_run_clusters.tsv", cbuf), (os.environ["GENSS"], sbuf),
                  (".L1_run_refs.tsv", rbuf)):
    if write_if_changed(name if os.path.isabs(name) else os.path.join(base, name), buf.getvalue()):
        changed.append(name)
print("inputs rewritten: %s" % (", ".join(changed) if changed else "none (cache preserved)"))

c = collections.Counter(r["cluster_id"] for r in rows)
print("curated scope: %d L1 units, %d genomes (largest %d, median %d)%s"
      % (len(c), len(rows), max(c.values()),
         sorted(c.values())[len(c) // 2],
         (" | EXCLUDED: %s" % sorted(exclude)) if exclude else ""))
PY
[ $? -eq 0 ] || exit 1

# NORMALIZE THE REFERENCE DEFLINES. Not cosmetic -- it is the difference between
# a unit running and dying.
#
# SPLIT_REFERENCE_REPLICONS names each replicon after the first token of its
# defline, the workflow keys the unit as <cluster_id>__<replicon id>, and Gubbins
# hands RAxML "<unit>.core.full.iteration_N_reconstruction" as its -n run id.
# raxmlHPC v8 SEGFAULTS (exit 139) at a -n run id of 128 characters or more --
# measured directly, 127 exits 0 and 128 exits 139, with the -w path length
# irrelevant. RAxML crashes before printing its own "run id too long" error and
# Gubbins' bare `except` reports only "Unable to fit model to data".
#
# This collection's deflines are the entire filename plus a contig index, up to
# 108 characters. Measured on this partition BEFORE normalizing: 40 of 164
# replicon-units (24%) were over the limit, including strain_1_L1_9 (n=90).
# After normalizing, the longest run id is 70. Sequence content is verified
# byte-identical; only '>' lines change.
python3 "${BASE}/normalize_reference_headers_bp.py" \
  --refs "${BASE}/.L1_run_refs.tsv" \
  --outdir "${BASE}/refs_normalized" \
  --out-refs "${BASE}/.L1_run_refs_normalized.tsv" || exit 1

# RESOURCES. The local_workstation_rtx4070 profile sizes per-cluster stages for
# n <= 155 and several ceilings are FIXED strings rather than
# check_max(x * task.attempt), so an OOM retries at the same memory and fails
# identically. The largest unit here IS 155, so the profile is at its design
# limit rather than beyond it -- but KEEP_INVARIANT_ATCG is pinned at 4 GB and
# was measured to pass only up to n=261, so it is scaled anyway. maxForks is
# raised relative to the all35 run because units are small: the binding
# constraint is now the 20-core/52 GB executor budget, not any single task.
if [ -n "${OVERRIDES}" ]; then
  cp "${OVERRIDES}" "${BASE}/curated_L1_overrides.config"
  echo "resource overrides: taken verbatim from ${OVERRIDES}"
else
cat > "${BASE}/curated_L1_overrides.config" <<'CFG'
executor {
    $local { cpus = 20; memory = '52 GB' }
}
process {
    withName: 'SNIPPY_CORE_GATHER' {
        cpus     = 2
        memory   = { task.attempt == 1 ? 8.GB : (task.attempt == 2 ? 16.GB : 28.GB) }
        time     = { task.attempt == 1 ? 12.h : 24.h }
        maxForks = 4
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'KEEP_INVARIANT_ATCG' {
        cpus     = 2
        memory   = { task.attempt == 1 ? 8.GB : (task.attempt == 2 ? 16.GB : 28.GB) }
        time     = { task.attempt == 1 ? 6.h  : 12.h }
        maxForks = 4
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'IQTREE_FAST' {
        cpus     = 3
        memory   = { task.attempt == 1 ? 6.GB : 12.GB }
        time     = { task.attempt == 1 ? 12.h : 24.h }
        maxForks = 4
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'ASC_PREFLIGHT' {
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'GUBBINS_CLUSTER' {
        cpus     = 5
        memory   = { task.attempt == 1 ? 12.GB : (task.attempt == 2 ? 20.GB : 32.GB) }
        time     = { task.attempt == 1 ? 72.h : 168.h }
        maxForks = 3
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
    withName: 'IQTREE_ASC' {
        cpus     = 5
        memory   = { task.attempt == 1 ? 10.GB : (task.attempt == 2 ? 20.GB : 32.GB) }
        time     = { task.attempt == 1 ? 48.h : 96.h }
        maxForks = 3
        errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
        maxRetries    = 2
    }
}
CFG
fi

# DRY_RUN=1 builds and validates every input, writes the overrides config, and
# stops before Nextflow. Use it to check a retry's inputs before committing the
# machine to a multi-hour run.
if [ "${DRY_RUN:-0}" = "1" ]; then
  echo "DRY_RUN: inputs built, stopping before nextflow"
  echo "  samplesheet : ${GENSS}"
  echo "  clusters    : ${BASE}/.L1_run_clusters.tsv"
  echo "  references  : ${BASE}/.L1_run_refs_normalized.tsv"
  echo "  overrides   : ${BASE}/curated_L1_overrides.config"
  echo "  outdir      : ${OUTDIR}"
  exit 0
fi

# Resume flag: `-resume <id>` for a specific session, bare `-resume` otherwise.
# The old inline `${RESUME_SESSION:+..} ${RESUME_SESSION:--resume}` expanded to
# `-resume <id> <id>` when set (the :- returns the VALUE, not the fallback),
# duplicating the session id as a stray positional arg. Nextflow tolerated it,
# but it was wrong; build the flag explicitly instead.
if [ -n "${RESUME_SESSION}" ]; then
  RESUME_ARG="-resume ${RESUME_SESSION}"
else
  RESUME_ARG="-resume"
fi

cd "${NFDIR}"
nextflow run . \
  -profile "${PROFILE}" \
  -c "${BASE}/curated_L1_overrides.config" \
  --input "${GENSS}" \
  --cluster_assignments "${BASE}/.L1_run_clusters.tsv" \
  --cluster_references "${BASE}/.L1_run_refs_normalized.tsv" \
  --split_replicons true \
  --max_cluster_size 1000 \
  --min_replicon_length 100000 \
  --gubbins_min_snps 3 \
  --gubbins_iterations 5 \
  --gubbins_use_hybrid false \
  --gubbins_skip_starting_tree true \
  --iqtree_support true \
  --outdir "${OUTDIR}" \
  -work-dir "${WORKDIR}" \
  -ansi-log false \
  ${RESUME_ARG} \
  && echo "CURATED L1 RUN OK" || echo "CURATED L1 RUN FAILED (exit $?)"
echo "FINISHED"
