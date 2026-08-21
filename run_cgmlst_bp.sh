#!/usr/bin/env bash
# cgMLST over the v4c panel: adapt the PubMLST scheme, then allele-call.
#
# Scheme: PubMLST B. pseudomallei scheme 2 (cgMLST), 4,090 loci, fetched by
# fetch_cgmlst_scheme_bp.py. PubMLST rather than Ridom's cgMLST.org because the
# latter is a commercial platform whose allele definitions we cannot assume we
# may redistribute; PubMLST is open and has a documented API.
#
# Two steps, both resumable, both skipped if their output already exists:
#   1. PrepExternalSchema  -- chewBBACA cannot consume raw PubMLST FASTAs. It
#      re-validates every allele (CDS, no internal stops, length within the
#      locus mode) and writes its own representative set. Run once; slow.
#   2. AlleleCall          -- the actual typing of 2,976 assemblies.
#
# Usage:  ./run_cgmlst_bp.sh [threads]
set -euo pipefail

B="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
THREADS="${1:-18}"
ENVBIN="$HOME/miniforge3/envs/chewbbaca/bin"
RAW="$B/cgmlst_scheme/alleles"
PREP="$B/cgmlst_scheme/prepared"
INPUT="$B/cgmlst_scheme/genomes"
OUT="$B/cgmlst_results"

command -v "$ENVBIN/chewBBACA.py" >/dev/null || { echo "chewBBACA not found in $ENVBIN"; exit 1; }

n_raw=$(ls "$RAW"/*.fasta 2>/dev/null | wc -l)
echo "locus FASTAs present: $n_raw"
[ "$n_raw" -ge 4090 ] || { echo "scheme incomplete ($n_raw/4090) -- let the fetch finish"; exit 1; }

# --- genome input dir: one symlink per panel genome ---------------------------
# chewBBACA takes a directory. Symlinks keep this from duplicating 22 GB, and
# naming them by sample_id means the output matrix joins straight back to the
# metadata instead of by file path.
if [ ! -d "$INPUT" ]; then
    mkdir -p "$INPUT"
    python3 - "$B" "$INPUT" <<'PY'
import csv, os, sys
B, dest = sys.argv[1], sys.argv[2]
n = 0
for r in csv.DictReader(open(f"{B}/L1v4c_MERGED_METADATA.tsv"), delimiter="\t"):
    p = r["assembly_path"]
    if p and os.path.isfile(p):
        link = os.path.join(dest, r["sample_id"] + ".fasta")
        if not os.path.islink(link):
            os.symlink(p, link)
        n += 1
print(f"  linked {n} genomes")
PY
fi
echo "genomes linked: $(ls "$INPUT" | wc -l)"

# --- 1. adapt the scheme ------------------------------------------------------
if [ ! -d "$PREP" ]; then
    echo "=== PrepExternalSchema (once, slow) ==="
    "$ENVBIN/chewBBACA.py" PrepExternalSchema \
        -g "$RAW" -o "$PREP" --cpu "$THREADS" 2>&1 | tail -20
else
    echo "=== PrepExternalSchema already done ($(ls "$PREP"/*.fasta 2>/dev/null | wc -l) loci) ==="
fi

# --- 2. allele call -----------------------------------------------------------
if [ ! -f "$OUT/results_alleles.tsv" ]; then
    echo "=== AlleleCall over $(ls "$INPUT" | wc -l) genomes ==="
    rm -rf "$OUT"
    "$ENVBIN/chewBBACA.py" AlleleCall \
        -i "$INPUT" -g "$PREP" -o "$OUT" --cpu "$THREADS" 2>&1 | tail -30
else
    echo "=== AlleleCall already done ==="
fi

echo
echo "profiles: $OUT/results_alleles.tsv"
[ -f "$OUT/results_alleles.tsv" ] && \
  echo "  $(( $(wc -l < "$OUT/results_alleles.tsv") - 1 )) genomes x $(( $(head -1 "$OUT/results_alleles.tsv" | tr '\t' '\n' | wc -l) - 1 )) loci"
