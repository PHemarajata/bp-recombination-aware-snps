#!/usr/bin/env bash
# A real global tree: core-genome alignment over the 82 unit medoids (parsnp),
# then maximum likelihood with branch support (IQ-TREE, UFBoot + SH-aLRT).
#
# WHY THIS REPLACES THE MASH NJ BACKBONE. L1_GLOBAL_BACKBONE.nwk is a
# neighbour-joining tree on Mash distances. It is fine for a quick overview but
# it has two defects for a deliverable: the branch lengths are Mash distances
# rather than substitutions, and a distance tree built this way has no
# likelihood, so there is nothing to bootstrap. This builds the alignment-based
# equivalent so the global tree carries the same kind of support values as the
# 164 per-unit trees.
#
# ONE TIP PER UNIT, the medoid -- the genome minimising mean Mash distance to
# its own unit, i.e. its most typical member. Within-unit relationships are NOT
# this tree's job; they are in L1_TREES_SUPPORTED/.
#
# **THIS TREE IS NOT RECOMBINATION-CORRECTED, AND MUST NOT BE.** Gubbins detects
# recombination by finding regions of unusually dense SNPs relative to a clonal
# background. Across 82 different lineages there is no shared clonal background:
# the between-lineage differences ARE the dense regions, and Gubbins would call
# most of the alignment recombinant. That is precisely the failure mode the whole
# partition exists to avoid -- it is why recombination is measured WITHIN units
# and never across them. So the backbone shows how the units relate, with branch
# lengths that include recombination, and no r/m may be computed from it.
set -uo pipefail
BASE=/home/phemarajata/Downloads/snp-mod-local-working
OUT=${OUT:-$BASE/L1_GLOBAL_ML}
THREADS=${THREADS:-4}          # deliberately modest: the main run may be using the box
UFBOOT=${UFBOOT:-1000}
ALRT=${ALRT:-1000}
COLL=/home/phemarajata/Downloads/final_deduped_all_BP_with_locations
PARSNP=quay.io/biocontainers/parsnp:1.7.4--hdcf5f25_2
IQTREE=quay.io/biocontainers/iqtree:2.2.6--h21ec9f0_0

mkdir -p "$OUT/genomes"
rm -f "$OUT/genomes"/*.fasta 2>/dev/null

# --- gather one medoid genome per unit ---------------------------------------
python3 - "$BASE" "$OUT" "$COLL" <<'PY'
import csv, os, shutil, sys
base, out, coll = sys.argv[1:4]
n = 0
for r in csv.DictReader(open(os.path.join(base, "L1_unit_medoids.tsv")), delimiter="\t"):
    src = os.path.join(coll, r["medoid"] + ".fasta")
    if not os.path.exists(src):
        hits = [f for f in os.listdir(coll) if f.startswith(r["medoid"])]
        if not hits:
            sys.exit("ERROR: no FASTA for medoid %s" % r["medoid"])
        src = os.path.join(coll, hits[0])
    # Name the tip for the UNIT, not the genome: the tree is a tree of units and
    # a reader should not have to join two files to know what a tip is.
    shutil.copy(src, os.path.join(out, "genomes", r["unit"] + ".fasta"))
    n += 1
print("medoid genomes staged: %d" % n)
PY
[ $? -eq 0 ] || exit 1

# parsnp needs a reference; use the most complete medoid so the core is large.
REF=$(python3 - "$OUT" <<'PY'
import os, sys
g = os.path.join(sys.argv[1], "genomes")
best, bestn = None, 10**9
for f in sorted(os.listdir(g)):
    n = sum(1 for line in open(os.path.join(g, f)) if line.startswith(">"))
    if n < bestn:
        best, bestn = f, n
print(best)
PY
)
echo "parsnp reference (fewest contigs): $REF"

echo "=== parsnp core-genome alignment over $(ls "$OUT/genomes" | wc -l) unit medoids ==="
docker run --rm -v "$OUT":/d -w /d -u "$(id -u):$(id -g)" "$PARSNP" \
    parsnp -r "/d/genomes/$REF" -d /d/genomes -o /d/parsnp -p "$THREADS" -c \
    > "$OUT/parsnp.log" 2>&1
rc=$?
if [ $rc -ne 0 ] || [ ! -s "$OUT/parsnp/parsnp.xmfa" ]; then
    echo "ERROR: parsnp failed (exit $rc); see $OUT/parsnp.log" >&2
    tail -20 "$OUT/parsnp.log" >&2
    exit 1
fi

echo "=== converting the core alignment to FASTA ==="
docker run --rm -v "$OUT":/d -w /d -u "$(id -u):$(id -g)" "$PARSNP" \
    harvesttools -i /d/parsnp/parsnp.ggr -M /d/core.aln >> "$OUT/parsnp.log" 2>&1
[ -s "$OUT/core.aln" ] || { echo "ERROR: harvesttools produced no core.aln" >&2; exit 1; }

python3 - "$OUT/core.aln" <<'PY'
import sys
n = 0; L = None; cur = 0
for line in open(sys.argv[1]):
    if line.startswith(">"):
        if L is None and cur: L = cur
        n += 1; cur = 0
    else:
        cur += len(line.strip())
print("core alignment: %d taxa, %d bp" % (n, L or cur))
PY

echo "=== IQ-TREE with UFBoot ${UFBOOT} + SH-aLRT ${ALRT} ==="
docker run --rm -v "$OUT":/d -w /d -u "$(id -u):$(id -g)" "$IQTREE" \
    iqtree2 -s /d/core.aln -st DNA -m GTR+G -T "$THREADS" \
    --prefix /d/global -bb "$UFBOOT" -alrt "$ALRT" \
    > "$OUT/iqtree.log" 2>&1
rc=$?
if [ $rc -ne 0 ] || [ ! -s "$OUT/global.treefile" ]; then
    echo "ERROR: IQ-TREE failed (exit $rc); see $OUT/iqtree.log" >&2
    tail -20 "$OUT/iqtree.log" >&2
    exit 1
fi

cp "$OUT/global.treefile" "$BASE/L1_GLOBAL_ML_TREE.nwk"
echo
echo "wrote $BASE/L1_GLOBAL_ML_TREE.nwk"
echo "  tips are UNIT names; support is SH-aLRT/UFBoot"
echo "  NOT recombination-corrected -- see the header of this script for why"
