#!/usr/bin/env bash
# Finish the v4c partition on the workstation, resuming from PopPIPE, now that
# swap makes the 901-genome strain's ska build fit. Reuses the existing PopPUNK
# fit + mash matrix in $W -- does NOT re-fit. On success it promotes the v4c
# bundle into a100_stage/ AND uploads it to Google Drive, so v4c reaches the A100
# even if you have already left.
#
# FAIL-SAFE: a100_stage/ (v4b) is only replaced by a VALIDATED v4c. Any failure
# leaves v4b intact and STATUS_FOR_MORNING.md telling you to upload it.
set -uo pipefail
B=/home/phemarajata/Downloads/snp-mod-local-working
W=/media/phemarajata/TB1/snp_archive/L1v4c_partition
REMOTE="peerah-gdrive:wfsnps-a100-v4b"
LOG="$B/finish_v4c.log"
ST="$B/STATUS_FOR_MORNING.md"
exec >>"$LOG" 2>&1
say(){ echo "[$(date '+%H:%M:%S')] $*"; }
status(){ local h="$1"; shift; { echo "# Status — $(date '+%Y-%m-%d %H:%M')"; echo; echo "## $h"; echo; printf '%s\n' "$@"; } > "$ST"; }
bail(){ say "ABORT: $*"; status "UPLOAD v4b — a100_stage/" \
  "v4c did not complete. Reason:" "" "    $*" "" \
  "a100_stage/ (v4b, 2,972 genomes) is intact and correct." "" \
  "    rclone copy a100_stage $REMOTE -P" "" "Log: finish_v4c.log"; exit 1; }

# swap sanity: ska build on strain_1 needs ~60 GB; RAM+swap must clear that.
TOTAL=$(free -g | awk '/Mem:/{m=$2} /Swap:/{s=$2} END{print m+s}')
say "RAM+swap addressable: ${TOTAL} GB"
[ "$TOTAL" -ge 85 ] || bail "RAM+swap only ${TOTAL} GB; add more swap (need >=85). ska will OOM again."

for f in db/db.h5 clusters.tsv refined_clusters_reconciled.csv mash_matrix.tsv mash_named.phylip rfile.txt run_poppipe.py; do
  [ -f "$W/$f" ] || bail "missing $W/$f (work dir not resumable)"
done

status "BUILDING v4c in place (swap route) — do not upload yet unless leaving now" \
  "PopPIPE is running with swap. If you must leave before it finishes, upload v4b:" \
  "" "    rclone copy a100_stage $REMOTE -P"

source ~/miniforge3/etc/profile.d/conda.sh && conda activate poppipe || bail "cannot activate poppipe env"
say "conda env: $(command -v sketchlib || echo NO-SKETCHLIB)"
say "clearing strain_1 partial (OOM leftover)"
rm -rf "$W/poppipe_v4b/output/strains/1"

say "PopPIPE fastbaps (strain_1 now fits in RAM+swap) $(date)"
( cd "$W" && PPTHREADS=8 python3 run_poppipe.py ) || bail "PopPIPE fastbaps failed"
DONE=$(ls "$W"/poppipe_v4b/output/strains/*/fastbaps_clusters.txt 2>/dev/null | wc -l)
say "fastbaps complete for $DONE strains"

say "L1 partition"
cd "$B"
python3 build_L1_partition_bp.py --clusters "$W/clusters.tsv" \
  --all-clusters "$W/refined_clusters_reconciled.csv" --absorb-subthreshold-strains \
  --mash "$W/mash_matrix.tsv" --poppipe "$W/poppipe_v4b" --min-size 7 \
  --prefix curated_L1v4c || bail "partition failed"
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
python3 build_v4c_panel.py --resolve-refs || bail "resolve refs"

say "staging SNP-run bundle"
python3 build_v4c_panel.py --bundle || bail "bundle failed"
[ -s "$B/a100_stage_v4c/fasta.tar.zst" ] || bail "bundle tarball missing"

say "promote a100_stage -> v4c (v4b kept as fallback)"
rm -rf "$B/a100_stage_v4b_superseded"
mv "$B/a100_stage" "$B/a100_stage_v4b_superseded" && mv "$B/a100_stage_v4c" "$B/a100_stage" \
  || bail "promotion failed (use a100_stage_v4c manually)"
NG=$(( $(wc -l < "$B/a100_stage/inputs/samplesheet.csv") - 1 ))
say "v4c bundle promoted: $NG genomes, $NU units"

say "uploading v4c to Google Drive $(date)"
if rclone copy "$B/a100_stage" "$REMOTE" -P --exclude '.build/**'; then
  status "v4c is DONE and UPLOADED — pull it on the A100" \
    "v4c built on the workstation (swap route) and pushed to $REMOTE." "" \
    "    genomes : $NG" "    units   : $NU at n>=7" "" \
    "On the A100, pull the SAME remote you already use and run as before:" "" \
    "    rclone copy $REMOTE . -P" "    (then run_a100.sh per A100_SETUP.md)" "" \
    "The bundle IS v4c now. v4b fallback: a100_stage_v4b_superseded/." "" \
    "Detail: finish_v4c.log, curated_L1v4c_units.tsv"
  say "DONE — v4c uploaded"
else
  status "v4c BUILT but upload failed — upload it manually" \
    "v4c is complete in a100_stage/ ($NG genomes) but the rclone push failed." "" \
    "    rclone copy a100_stage $REMOTE -P" "" "Log: finish_v4c.log"
  say "DONE — v4c built, upload pending"
fi
