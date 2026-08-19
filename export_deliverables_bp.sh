#!/usr/bin/env bash
# Copy the END RESULTS to the external drive. Results only -- no alignments, no
# work dirs, no process logs.
#
# WHAT IS DELIBERATELY EXCLUDED, and why, so nobody has to guess later:
#   *.core.full.aln            per-unit whole-genome alignments, ~40 MB each,
#                              ~7 GB total. Regenerable from the pipeline and of
#                              no use for reading results.
#   *.filtered_polymorphic_sites.fasta
#                              the SNP alignments the trees were built from.
#                              Bulky; the trees themselves are what is wanted.
#   L1_work / L1_clean_work    Nextflow scratch.
#   *.diagnostics.log, pipeline_info/
#                              per-task logs and execution traces. Kept OUT of
#                              the results folder but see PROVENANCE below --
#                              the traces are small and ARE copied, because
#                              without them there is no record of what ran.
#
# WHAT IS INCLUDED: the assignment table, r/m results, every tree, the
# recombination predictions (small GFFs -- these ARE a result, they say where
# recombination was detected), the per-unit summary, the phylogeography tests,
# and the written analysis.
set -uo pipefail
BASE=/home/phemarajata/Downloads/snp-mod-local-working
# PART selects the partition generation. v1 = the original 82-unit run
# (curated_L1_*, L1_out); v3 = the merge-not-delete 91-unit run (curated_L1v3_*,
# L1v3_out). Table basenames and the run directory both follow from it, so a new
# partition needs one variable changed, not a dozen string edits.
PART=${PART:-v3}
case "$PART" in
  v1) CLU_PREFIX=curated_L1;   ASSIGN=L1_ASSIGNMENTS.tsv;    PHYLO=PHYLOGEOGRAPHY_ASSOCIATION.tsv;      DEFRUN=L1_out   ;;
  v3) CLU_PREFIX=curated_L1v3; ASSIGN=L1v3_ASSIGNMENTS.tsv;  PHYLO=L1v3_PHYLOGEOGRAPHY_ASSOCIATION.tsv; DEFRUN=L1v3_out ;;
  *)  echo "ERROR: unknown PART=$PART (expected v1 or v3)"; exit 2 ;;
esac
DEST=${DEST:-/media/phemarajata/TB1/snp_results_$(date +%Y-%m-%d)_${PART}}
RUN=${RUN:-$DEFRUN}         # which run's per-unit outputs to take trees from

say(){ printf '  %s\n' "$*"; }

[ -d /media/phemarajata/TB1 ] || { echo "ERROR: TB1 not mounted"; exit 1; }
mkdir -p "$DEST"/{tables,trees/per_unit,trees/global,recombination,provenance,analysis} || exit 1

# ---- tables -----------------------------------------------------------------
for f in "$ASSIGN" "$PHYLO" \
         "${CLU_PREFIX}_clusters.tsv" "${CLU_PREFIX}_units.tsv" \
         "${CLU_PREFIX}_stragglers.tsv" "${CLU_PREFIX}_reference_audit.tsv" \
         "${CLU_PREFIX}_ref_alternates.tsv" "${CLU_PREFIX}_merges.tsv" \
         "${CLU_PREFIX}_assignments_all.tsv" \
         L1_unit_medoids.tsv ISOLATION_SOURCE_2026-08-16.tsv \
         ADDITIONS_MANIFEST.tsv SRA_TO_ASSEMBLE.tsv; do
    [ -f "$BASE/$f" ] && cp -p "$BASE/$f" "$DEST/tables/" && say "table   $f"
done
[ -f "$BASE/$RUN/Summaries/cluster_phylogeny_summary.csv" ] && \
    cp -p "$BASE/$RUN/Summaries/cluster_phylogeny_summary.csv" "$DEST/tables/" && \
    say "table   cluster_phylogeny_summary.csv"
# r/m is now produced IN-PIPELINE (POOL_RECOMBINATION_STATS) rather than by a
# downstream script, so it comes from the run directory.
[ -f "$BASE/$RUN/Summaries/recombination_rm.tsv" ] && \
    cp -p "$BASE/$RUN/Summaries/recombination_rm.tsv" "$DEST/tables/" && \
    say "table   recombination_rm.tsv  (in-pipeline r/m)"

# ---- trees ------------------------------------------------------------------
# Per-unit ML trees. From v3 the run's own *.final.treefile already carries
# SH-aLRT/UFBoot support inline (--iqtree_support true), so no separate
# L1_TREES_SUPPORTED staging directory is needed; fall back to it for v1.
n=0
for f in "$BASE/$RUN"/Clusters/*/*.final.treefile; do
    [ -e "$f" ] || break
    cp -p "$f" "$DEST/trees/per_unit/" && n=$((n+1))
done
if [ "$n" -eq 0 ]; then
    for f in "$BASE"/L1_TREES_SUPPORTED/*.support.treefile; do
        [ -e "$f" ] || break
        cp -p "$f" "$DEST/trees/per_unit/" && n=$((n+1))
    done
fi
say "trees   $n per-unit ML trees with SH-aLRT/UFBoot support"

# The recombination-corrected Gubbins trees are a distinct product from the ML
# trees: same data, different estimator. Keep both.
n=0
for f in "$BASE/$RUN"/Clusters/*/Gubbins/*.node_labelled.final_tree.tre; do
    [ -e "$f" ] || break
    cp -p "$f" "$DEST/trees/per_unit/" && n=$((n+1))
done
say "trees   $n per-unit Gubbins (recombination-corrected) trees"

for f in L1_GLOBAL_ML_TREE.nwk L1_GLOBAL_BACKBONE.nwk; do
    [ -f "$BASE/$f" ] && cp -p "$BASE/$f" "$DEST/trees/global/" && say "trees   $f"
done
[ -f "$BASE/$RUN/global_ml_tree.treefile" ] && \
    cp -p "$BASE/$RUN/global_ml_tree.treefile" "$DEST/trees/global/${PART}_global_ml_tree.treefile" && \
    say "trees   ${PART} global ML tree (from the run)"
[ -f "$BASE/L1_GLOBAL_ML/globalml.iqtree" ] && \
    cp -p "$BASE/L1_GLOBAL_ML/globalml.iqtree" "$DEST/trees/global/L1_GLOBAL_ML_TREE.iqtree" && \
    say "trees   global ML model report"

# ---- recombination predictions (small, and they ARE a result) ---------------
n=0
for f in "$BASE/$RUN"/Clusters/*/Gubbins/*.recombination_predictions.gff; do
    [ -e "$f" ] || break
    cp -p "$f" "$DEST/recombination/" && n=$((n+1))
done
say "recomb  $n recombination prediction GFFs"

# per-branch statistics: the numbers r/m is computed from. Small and the only
# copy outside the work dir.
mkdir -p "$DEST/recombination/per_branch_statistics"
n=0
for f in "$BASE/$RUN"/Clusters/*/Gubbins/*.per_branch_statistics.csv; do
    [ -e "$f" ] || break
    cp -p "$f" "$DEST/recombination/per_branch_statistics/" && n=$((n+1))
done
say "recomb  $n per-branch statistics files"

# ---- analysis and provenance ------------------------------------------------
for f in RESULTS_NARRATIVE.md METHODS_DRAFT_2026-08-11.md CLEAN_RUN_COMPARISON.md \
         L1_RESULTS_AND_THE_REFERENCE_DISTANCE_PROBLEM.md \
         REFERENCE_FAILURE_SOLVED.md HANDOFF_2026-08-15_SESSION4.md \
         HANDOFF_2026-08-16_SESSION5.md INTERPRETATION_2026-08-16.md \
         V3_RUN_RESULTS.md L1_PARTITION_V2.md GENOME_ADDITIONS_PROPOSAL.md; do
    [ -f "$BASE/$f" ] && cp -p "$BASE/$f" "$DEST/analysis/" && say "analysis $f"
done

# Provenance: what ran, with what, at what version. Small, and without it the
# results are unreproducible.
for f in "$BASE/$RUN"/pipeline_info/execution_trace*.txt \
         "$BASE/$RUN"/pipeline_info/software_versions.yml \
         "$BASE"/CLEAN_RUN_TIMING.txt; do
    [ -e "$f" ] && cp -p "$f" "$DEST/provenance/"
done
( cd /home/phemarajata/wf-assembly-snps-mod && \
  printf 'pipeline commit: %s\nbranch: %s\nstatus:\n' "$(git rev-parse HEAD)" "$(git rev-parse --abbrev-ref HEAD)" && \
  git status --porcelain ) > "$DEST/provenance/pipeline_commit.txt" 2>/dev/null
say "provenance  traces, versions, pipeline commit"

# ---- manifest ---------------------------------------------------------------
{
    echo "B. pseudomallei recombination-aware phylogenomics -- results export"
    echo "exported: $(date '+%F %T')  host: $(hostname)"
    echo "source run: $RUN"
    echo
    echo "READ analysis/RESULTS_NARRATIVE.md FIRST."
    echo
    echo "PARTITION: $PART"
    if [ "$PART" = "v3" ]; then
      echo "  91 units, 2,282 genomes. SUPERSEDES the 82-unit v1 export"
      echo "  (snp_results_2026-08-16), which discarded 26% of the collection"
      echo "  through a size floor applied twice. See analysis/V3_RUN_RESULTS.md"
      echo "  and analysis/L1_PARTITION_V2.md."
    fi
    echo
    echo "r/m: use tables/recombination_rm.tsv column 'rm_corrected'."
    echo "  It is produced IN-PIPELINE (POOL_RECOMBINATION_STATS) from v3 on."
    echo "  Do NOT use 'rm_uncorrected': it includes the external reference's"
    echo "  branch, which contributed 52% of all non-recombinant SNPs."
    echo
    echo "  QUOTE r/m ON THE CLEAN SUBSET, NOT THE OVERALL MEDIAN. The 91-unit"
    echo "  median is 4.87, but that is diluted by newly-analysable small units"
    echo "  (unchanged units 6.20, merged 4.44, new 1.77). Filter on"
    echo "  'max_kept_branch_len': 29 of 91 units carry a >=1000-substitution"
    echo "  surviving branch and their r/m is depressed by a divergent member,"
    echo "  not by biology."
    echo
    echo "trees/global/L1_GLOBAL_ML_TREE.nwk is NOT recombination-corrected and"
    echo "must not be: across divergent lineages Gubbins would call most of the"
    echo "alignment recombinant. No r/m may be derived from it."
    echo
    echo "EXCLUDED from this export: whole-genome and SNP alignments, Nextflow"
    echo "work directories, per-task logs. Regenerable from the pipeline."
    echo
    echo "file listing:"
} > "$DEST/README.txt"
( cd "$DEST" && find . -type f -printf '%-92p %10s bytes\n' | sort ) >> "$DEST/README.txt"

echo
say "destination : $DEST"
say "total size  : $(du -sh "$DEST" | cut -f1)"
say "files       : $(find "$DEST" -type f | wc -l)"
