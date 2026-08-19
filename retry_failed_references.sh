#!/usr/bin/env bash
# Re-drive the units that failed Gubbins model fitting, against their next-best
# reference.
#
# WHY THIS IS A SEPARATE PASS AND NOT AN errorStrategy. The failure being
# recovered from is a property of the REFERENCE, and the reference is consumed
# far upstream of Gubbins: it determines the mapping, hence the alignment, hence
# the site patterns RAxML cannot fit. No number of Gubbins retries changes any of
# that. Recovery means re-mapping the unit against a different genome, which is a
# fresh pass over the pipeline rather than a fresh attempt at one process.
#
# WHAT JUSTIFIES DOING IT AT ALL. Six units previously failed with RAxML "Unable
# to fit model to data"; three references accounted for all six (one of them for
# four, 0/4) while 23 other references gave 28/28 successes. Re-running all six
# with ONLY the reference changed recovered 12/12 replicon-units -- three of them
# against a reference MORE distant than the one they failed on, so it is not
# divergence. The three known-bad references are blocklisted up front; this
# script exists for the ones not yet identified, and 18 of the 31 references in
# the current run have never been exercised.
#
# WHAT IT DELIBERATELY DOES NOT DO. It does not promote a unit that failed for
# any other reason -- OOM, timeout, too few sequences, snippy-core refusing a
# replicon. Those are not reference problems and swapping the reference would
# hide them. Only the model-fit signature is matched.
#
# LIMIT. A unit is promoted at most --max-promotions times (default 2, i.e. down
# to rank 3). A unit still failing after that is a finding about the unit, and
# should be reported as one rather than walked further down the list.
set -uo pipefail
BASE=/home/phemarajata/Downloads/snp-mod-local-working
OUTDIR="${OUTDIR:-${BASE}/L1_out}"
PASS="${PASS:-2}"                       # which retry pass this is; 2 = first retry
MAX_PROMOTIONS="${MAX_PROMOTIONS:-2}"

STATE="${BASE}/.L1_reference_promotions.tsv"
[ -f "$STATE" ] || printf 'cluster_id\trank\tpass\treference\n' > "$STATE"

echo "=== scanning ${OUTDIR} for reference-attributable Gubbins failures ==="
python3 - "$BASE" "$OUTDIR" "$STATE" "$PASS" "$MAX_PROMOTIONS" <<'PY'
import csv, glob, os, re, sys

base, outdir, state_path, pass_no, max_promo = sys.argv[1:6]
pass_no, max_promo = int(pass_no), int(max_promo)

# The signature, and nothing else. Gubbins truncates RAxML's error to one line;
# this is that line as it appears in the diagnostics log.
SIGNATURE = re.compile(r"unable to fit model to data", re.I)

failed = {}
for path in glob.glob(os.path.join(outdir, "Clusters", "*", "Gubbins",
                                   "*.diagnostics.log")):
    try:
        text = open(path, errors="replace").read()
    except OSError:
        continue
    if SIGNATURE.search(text):
        unit = os.path.basename(path).replace(".diagnostics.log", "")
        # Replicon-split units are named <unit>_replicon<N>; the reference is a
        # property of the unit, so strip the replicon suffix before promoting.
        unit = re.sub(r"_replicon\d+$", "", unit)
        failed.setdefault(unit, []).append(os.path.relpath(path, outdir))

if not failed:
    print("no reference-attributable failures found -- nothing to promote")
    sys.exit(3)

promotions = {}
if os.path.exists(state_path):
    for r in csv.DictReader(open(state_path), delimiter="\t"):
        promotions[r["cluster_id"]] = int(r["rank"])

alternates = {}
for r in csv.DictReader(open(os.path.join(base, "curated_L1_ref_alternates.tsv")),
                        delimiter="\t"):
    alternates.setdefault(r["cluster_id"], {})[int(r["rank"])] = r["reference"]

current = {}
for r in csv.DictReader(open(os.path.join(base, "curated_L1_refs.tsv")),
                        delimiter="\t"):
    current[r["cluster_id"]] = r["reference_path"]

COLL = "/home/phemarajata/Downloads/final_deduped_all_BP_with_locations"
promote, stuck = [], []
for unit in sorted(failed):
    at = promotions.get(unit, 1)
    nxt = at + 1
    if at - 1 >= max_promo:
        stuck.append((unit, "already promoted %d times" % (at - 1)))
        continue
    ref = alternates.get(unit, {}).get(nxt)
    if not ref:
        stuck.append((unit, "no rank-%d alternate available" % nxt))
        continue
    path = os.path.join(COLL, ref + ".fasta")
    if not os.path.exists(path):
        hit = glob.glob(os.path.join(COLL, ref + "*"))
        if not hit:
            stuck.append((unit, "alternate %s not in the collection" % ref))
            continue
        path = hit[0]
    promote.append((unit, nxt, ref, path))

print("\nfailed with the model-fit signature: %d units" % len(failed))
for unit, logs in sorted(failed.items()):
    print("  %-20s %d replicon log(s)" % (unit, len(logs)))

if stuck:
    print("\nNOT promoted -- report these as findings about the unit, not the "
          "reference:")
    for unit, why in stuck:
        print("  %-20s %s" % (unit, why))

if not promote:
    print("\nnothing left to promote")
    sys.exit(3)

print("\npromoting %d units to their next reference:" % len(promote))
for unit, rank, ref, _ in promote:
    print("  %-20s -> rank %d  %s" % (unit, rank, ref))

# Retry inputs: only the promoted units, so the retry run is small and its
# results land in their own outdir rather than overwriting the first pass.
units = {u for u, _, _, _ in promote}
rows = [r for r in csv.DictReader(open(os.path.join(base, "curated_L1_clusters.tsv")),
                                  delimiter="\t") if r["cluster_id"] in units]
with open(os.path.join(base, "retry_L1_clusters.tsv"), "w", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["cluster_id", "sample_id"])
    for r in rows:
        w.writerow([r["cluster_id"], r["sample_id"]])
with open(os.path.join(base, "retry_L1_refs.tsv"), "w", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["cluster_id", "reference_path"])
    for unit, _, _, path in promote:
        w.writerow([unit, path])

with open(state_path, "a", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    for unit, rank, ref, _ in promote:
        w.writerow([unit, rank, pass_no, ref])

print("\nwrote retry_L1_clusters.tsv (%d genomes) and retry_L1_refs.tsv" % len(rows))
PY
rc=$?
if [ "$rc" -eq 3 ]; then echo "nothing to do"; exit 0; fi
[ "$rc" -eq 0 ] || exit 1

echo
echo "=== re-running promoted units into L1_retry${PASS}_out ==="
CLUSTERS="${BASE}/retry_L1_clusters.tsv" \
REFS="${BASE}/retry_L1_refs.tsv" \
OUTDIR="${BASE}/L1_retry${PASS}_out" \
WORKDIR="${BASE}/L1_retry${PASS}_work" \
  bash "${BASE}/run_wf_curated_L1.sh"

echo
echo "Retry pass ${PASS} finished. A unit that now succeeds is a REFERENCE"
echo "artefact, not an unanalysable population -- record which reference failed"
echo "in reference_blocklist.txt so the next run never picks it."
