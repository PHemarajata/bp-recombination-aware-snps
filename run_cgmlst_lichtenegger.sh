#!/usr/bin/env bash
# cgMLST over the expanded panel using the PUBLISHED scheme.
#
# Scheme: B. pseudomallei cgMLST v1.1, 4,221 loci, seed genome K96243
#   (NC_006350.1 / NC_006351.1 -- the same reference this project uses).
#   Curators Steinmetz / Wagner / Lichtenegger, Medical University Graz.
#   Lichtenegger S et al. J Clin Microbiol 2021;59:e00093-21, PMID 33980649.
#   Downloaded 2026-08-21 from https://www.cgmlst.org/ncs/schema/Bpseudomallei/alleles
#
# This REPLACES the earlier run on PubMLST scheme 2 (4,090 loci, unpublished,
# flagged "experimental in development"). The PubMLST results are kept so the
# two can be compared -- concordance between schemes is a robustness result,
# not just a defensive footnote.
#
# Genomes: the 2,976-genome v4c panel + the 57 additions QC'd 2026-08-21
#          (40 TheiaProk SPAdes + 17 Mexican GenBank) = 3,033.
#
set -euo pipefail

B="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENVBIN="$HOME/miniforge3/envs/chewbbaca/bin"
RAW="$B/cgmlst_lichtenegger/raw"
PREP="$B/cgmlst_lichtenegger/prepared"
INPUT="$B/cgmlst_lichtenegger/genomes"
OUT="$B/cgmlst_lichtenegger/results"
THREADS="${CGTHREADS:-18}"

TERRA40="/home/phemarajata/Downloads/bp_spades_assemblies_2"
MEX17="$B/additions_mexico_2026-08-21/fasta"

command -v "$ENVBIN/chewBBACA.py" >/dev/null || { echo "chewBBACA not found in $ENVBIN"; exit 1; }

n_raw=$(ls "$RAW"/*.fasta 2>/dev/null | wc -l)
echo "locus FASTAs: $n_raw"
[ "$n_raw" -eq 4221 ] || { echo "expected 4221 loci, found $n_raw"; exit 1; }

# --- genome input dir ---------------------------------------------------------
# Symlinks named by sample_id, so the output matrix joins straight back to
# metadata rather than by file path. New genomes keep their bare accession as
# sample_id; MANIFEST.tsv carries the metadata rather than encoding it in the
# filename.
if [ ! -d "$INPUT" ]; then
    mkdir -p "$INPUT"
    python3 - "$B" "$INPUT" "$TERRA40" "$MEX17" <<'PY'
import csv, os, re, sys
B, dest, terra, mex = sys.argv[1:5]
rows = []
n_panel = n_new = 0

for r in csv.DictReader(open(f"{B}/L1v4c_MERGED_METADATA.tsv"), delimiter="\t"):
    p = r["assembly_path"]
    if p and os.path.isfile(p):
        link = os.path.join(dest, r["sample_id"] + ".fasta")
        if not os.path.islink(link):
            os.symlink(p, link)
        n_panel += 1
        rows.append(dict(sample_id=r["sample_id"], batch="v4c_panel",
                         country=r["country"], role=r.get("role", ""),
                         origin_basis=r.get("origin_basis", ""),
                         exposure_country=r.get("acquired_from", ""),
                         path=p))

tier = {r["run_accession"]: r for r in
        csv.DictReader(open(f"{B}/ENA_TARGETS_CLASSIFIED.tsv"), delimiter="\t")}
for f in sorted(os.listdir(terra)):
    if not f.endswith(".fasta"):
        continue
    s = re.sub(r"_filtered_contigs\.fasta$", "", f)
    src = os.path.join(terra, f)
    link = os.path.join(dest, s + ".fasta")
    if not os.path.islink(link):
        os.symlink(src, link)
    n_new += 1
    t = tier.get(s, {})
    gt = t.get("origin_tier", "") in ("A_exposure_stated", "B_external_evidence")
    rows.append(dict(sample_id=s, batch="terra40",
                     country=(t.get("country", "") or "").split(":")[0].strip(),
                     role="ground_truth" if gt else "context",
                     origin_basis=t.get("origin_tier", ""),
                     exposure_country=t.get("exposure_country", ""),
                     path=src))

for f in sorted(os.listdir(mex)):
    if not f.endswith(".fasta"):
        continue
    s = f[:-6]
    src = os.path.join(mex, f)
    link = os.path.join(dest, s + ".fasta")
    if not os.path.islink(link):
        os.symlink(src, link)
    n_new += 1
    rows.append(dict(sample_id=s, batch="mexico17", country="Mexico",
                     role="context", origin_basis="C_deposit_only",
                     exposure_country="", path=src))

cols = ["sample_id", "batch", "country", "role", "origin_basis",
        "exposure_country", "path"]
with open(f"{B}/cgmlst_lichtenegger/MANIFEST.tsv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
    w.writeheader()
    for r in rows:
        w.writerow({c: r.get(c, "") for c in cols})
print(f"  linked {n_panel} panel + {n_new} new = {n_panel + n_new}")
PY
fi
echo "genomes linked: $(ls "$INPUT" | wc -l)"

# --- 1. adapt the scheme ------------------------------------------------------
# Re-validates every allele: CDS, no internal stops, length within the locus mode.
if [ ! -d "$PREP" ]; then
    echo "=== PrepExternalSchema ==="
    "$ENVBIN/chewBBACA.py" PrepExternalSchema \
        -g "$RAW" -o "$PREP" --cpu "$THREADS" 2>&1 | tail -20
else
    echo "=== PrepExternalSchema already done ($(ls "$PREP"/*.fasta 2>/dev/null | wc -l) loci) ==="
fi

# --- 2. allele call -----------------------------------------------------------
if [ ! -f "$OUT/results_alleles.tsv" ]; then
    echo "=== AlleleCall over $(ls "$INPUT" | wc -l) genomes, $THREADS cpu ==="
    rm -rf "$OUT"
    "$ENVBIN/chewBBACA.py" AlleleCall \
        -i "$INPUT" -g "$PREP" -o "$OUT" --cpu "$THREADS" 2>&1 | tail -30
else
    echo "=== AlleleCall already done ==="
fi

echo
echo "profiles: $OUT/results_alleles.tsv"
[ -f "$OUT/results_alleles.tsv" ] && \
    echo "  $(($(wc -l < "$OUT/results_alleles.tsv") - 1)) genomes x $(($(head -1 "$OUT/results_alleles.tsv" | tr '\t' '\n' | wc -l) - 1)) loci"
