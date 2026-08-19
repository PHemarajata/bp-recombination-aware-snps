#!/usr/bin/env bash
# Unattended: wait for the SPAdes re-QC, decide whether the panel should change,
# and if so build v4c end to end and stage it for the A100.
#
# FAIL-SAFE CONTRACT
#   The existing a100_stage/ bundle (v4b minus SRR30648681) is never touched
#   until a v4c bundle has been built AND validated. Any failure at any step
#   leaves a100_stage/ exactly as it is, so there is always something correct to
#   upload. STATUS_FOR_MORNING.md says which one, in the first line.
set -uo pipefail
B=/home/phemarajata/Downloads/snp-mod-local-working
W=/media/phemarajata/TB1/snp_archive/L1v4c_partition
ST="$B/STATUS_FOR_MORNING.md"
LOG="$B/overnight_v4c.log"
exec >>"$LOG" 2>&1

say() { echo "[$(date '+%H:%M:%S')] $*"; }
status() {   # $1 = headline, rest = body
  local head="$1"; shift
  { echo "# Status — $(date '+%Y-%m-%d %H:%M')"; echo;
    echo "## $head"; echo; printf '%s\n' "$@"; } > "$ST"
}
bail() { say "ABORT: $*"; status "UPLOAD THE EXISTING BUNDLE — a100_stage/" \
  "v4c was not completed. Reason:" "" "    $*" "" \
  "\`a100_stage/\` is untouched and correct: v4b minus SRR30648681, 2,972 genomes, 95 units." \
  "Upload it as planned:" "" \
  "    rclone copy a100_stage peerah-gdrive:wfsnps-a100-v4b -P" "" \
  "Full log: overnight_v4c.log"; exit 1; }

status "WAITING — re-QC has not finished yet" \
  "The SNP run is still going, or the re-QC is still running." \
  "If you are reading this before it completed, upload \`a100_stage/\` (v4b minus SRR30648681)." \
  "" "    rclone copy a100_stage peerah-gdrive:wfsnps-a100-v4b -P"

say "waiting for the re-QC to finish"
for _ in $(seq 1 720); do            # up to 24 h
  grep -q "RE-QC DONE" "$B/spades_reqc.log" 2>/dev/null && break
  sleep 120
done
grep -q "RE-QC DONE" "$B/spades_reqc.log" 2>/dev/null || bail "re-QC did not finish within 24 h"
[ -s "$B/SPADES_PASS_LIST.txt" ] || bail "SPADES_PASS_LIST.txt missing or empty"
say "re-QC finished"

# ---------------------------------------------------------------- decide -----
NPASS=$(wc -l < "$B/SPADES_PASS_LIST.txt")
say "SPAdes pass list: $NPASS"
# Sanity floor. 171 SKESA genomes are in v4b; the SPAdes batch is 191 delivered
# minus 23 excluded = 168 eligible. A pass count far below that means the re-QC
# or the assemblies are wrong, and adopting them would silently shrink the panel.
[ "$NPASS" -ge 150 ] || bail "only $NPASS SPAdes assemblies passed QC (expected ~165); not adopting"

cd "$B" || bail "cannot cd $B"
python3 build_v4c_panel.py --check-only >/dev/null 2>&1 || true
CHANGED=$(python3 build_v4c_panel.py --report-delta 2>/dev/null | tail -1)
say "delta vs v4b: $CHANGED"

status "BUILDING v4c — do not upload yet unless you are leaving now" \
  "The re-QC finished ($NPASS pass) and v4c is being built." \
  "If you must leave before it completes, upload \`a100_stage/\` — it is valid." \
  "" "    rclone copy a100_stage peerah-gdrive:wfsnps-a100-v4b -P"

# ---------------------------------------------------------------- build ------
say "building v4c panel"
python3 build_v4c_panel.py --build || bail "panel build failed"
NP=$(( $(wc -l < "$B/L1v4c_MERGED_METADATA.tsv") - 1 ))
say "panel: $NP genomes"
[ "$NP" -ge 2900 ] || bail "v4c panel only $NP genomes; expected ~2,970"

mkdir -p "$W" || bail "cannot create $W"
cut -f2 "$B/L1v4c_rfile.txt" > "$W/paths.txt"
cp "$B/L1v4c_rfile.txt" "$W/rfile.txt"

say "PopPUNK create-db"
source ~/miniforge3/etc/profile.d/conda.sh && conda activate poppipe || bail "conda env poppipe"
( cd "$W" && poppunk --create-db --r-files rfile.txt --output db \
    --min-k 15 --max-k 31 --k-step 2 --threads 10 ) || bail "poppunk create-db"
say "PopPUNK bgmm K=5 + refine"
( cd "$W" && poppunk --fit-model bgmm --ref-db db --output fit --K 5 --max-a-dist 0.53 --threads 10 \
  && poppunk --fit-model refine --ref-db db --model-dir fit --output refined --threads 10 ) \
  || bail "poppunk fit"
SCORE=$(tr '\r' '\n' < "$W"/../L1v4c_partition/refined/*.log 2>/dev/null | grep -oE "Score\s+[0-9.]+" | tail -1 | grep -oE "[0-9.]+")
say "network score: ${SCORE:-unknown}"

say "mash matrix (-s 50000)"
( cd "$W" && mash sketch -s 50000 -k 21 -p 8 -o combined -l paths.txt \
  && mash triangle -p 8 combined.msh > mash.phylip \
  && python3 ~/wf-assembly-snps-mod/bin/mash_phylip_to_matrix.py mash.phylip mash_matrix.tsv ) \
  || bail "mash"

say "reconcile names + clusters.tsv"
python3 build_v4c_panel.py --reconcile "$W" || bail "name reconciliation"
python3 ~/wf-assembly-snps-mod/bin/poppunk_clusters_to_tsv.py \
  --clusters "$W/refined_clusters_reconciled.csv" --rfile "$W/rfile.txt" \
  --min-cluster-size 7 --prefix strain_ --out "$W/clusters.tsv" \
  --excluded "$W/poppunk_excluded.tsv" || bail "clusters_to_tsv"

say "full PopPIPE fastbaps"
cp "$B/L1v4b_partition/run_poppipe_v4b.py" "$W/run_poppipe.py"
sed -i "s#BASE = os.path.dirname(os.path.abspath(__file__))#BASE = '$W'#" "$W/run_poppipe.py"
( cd "$W" && PPTHREADS=10 python3 run_poppipe.py ) || bail "PopPIPE fastbaps"

say "L1 partition"
python3 build_L1_partition_bp.py --clusters "$W/clusters.tsv" \
  --all-clusters "$W/refined_clusters_reconciled.csv" --absorb-subthreshold-strains \
  --mash "$W/mash_matrix.tsv" --poppipe "$W/poppipe_v4b" --min-size 7 \
  --prefix curated_L1v4c || bail "partition"
NU=$(awk -F'\t' 'NR>1 && $5=="yes"' curated_L1v4c_units.tsv | wc -l)
say "units at n>=7: $NU"
[ "$NU" -ge 80 ] || bail "only $NU units at n>=7; expected ~95"

say "references"
python3 build_v4c_panel.py --fasta-dir "$W" || bail "fasta dir"
python3 pick_cluster_references_bp.py --membership curated_L1v4c_clusters.tsv \
  --fasta-dir "$W/all_fasta" --phylip "$W/mash_named.phylip" \
  --blocklist reference_blocklist.txt --max-contigs 2 \
  --out curated_L1v4c_refsel.tsv >/dev/null || bail "pick references"
python3 rank_reference_alternates_bp.py --clusters curated_L1v4c_clusters.tsv \
  --matrix "$W/mash_matrix.tsv" --fasta-dir "$W/all_fasta" \
  --blocklist reference_blocklist.txt --max-contigs 2 --top 5 \
  --cache .contig_counts_v4c.json --out curated_L1v4c_ref_alternates.tsv >/dev/null \
  || bail "rank alternates"
python3 merge_L1_refs_bp.py --selection curated_L1v4c_refsel.tsv \
  --alternates curated_L1v4c_ref_alternates.tsv --fasta-dir "$W/all_fasta" \
  --blocklist reference_blocklist.txt --out curated_L1v4c_refs.tsv \
  --audit curated_L1v4c_reference_audit.tsv || bail "merge refs"
python3 build_v4c_panel.py --resolve-refs || bail "resolve reference paths"

say "staging bundle"
python3 build_v4c_panel.py --bundle || bail "bundle"
[ -s "$B/a100_stage_v4c/fasta.tar.zst" ] || bail "bundle tarball missing"
say "v4c bundle built"

# --------------------------------------------------------------- promote -----
mv "$B/a100_stage" "$B/a100_stage_v4b_superseded" && mv "$B/a100_stage_v4c" "$B/a100_stage" \
  || bail "promotion failed (both bundles still present, use a100_stage_v4c)"

NG=$(( $(wc -l < "$B/a100_stage/inputs/samplesheet.csv") - 1 ))
status "UPLOAD a100_stage/ — it is now v4c" \
  "v4c built and validated overnight." "" \
  "    genomes : $NG" \
  "    units   : $NU at n>=7" \
  "    network : ${SCORE:-see log}" \
  "    delta   : $CHANGED" "" \
  "Upload exactly as before — same command, same remote:" "" \
  "    rclone copy a100_stage peerah-gdrive:wfsnps-a100-v4b -P" "" \
  "The v4b bundle is kept at \`a100_stage_v4b_superseded/\` if you want to fall back." \
  "Details: L1V4C_PARTITION_REPORT.md, overnight_v4c.log"
say "DONE"
