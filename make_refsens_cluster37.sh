#!/usr/bin/env bash
# Reference-sensitivity experiment, cluster_37 -- the SIXTH cluster.
#
# THE QUESTION: does RECOVERY REPRODUCE? Across five clusters, r/m ~1.0-1.5 is
# the norm (9 of 10 measurements) and only cluster_16 (measured 3,639) departs
# from it at 6.25/8.66. Two hypotheses remain undistinguished (A.9 Finding 2):
#   (a) a NARROW detection window with an upper bound between 3,639 and 5,362;
#   (b) cluster_16 is an atypical, more-recombinogenic lineage.
# cluster_37 sits INSIDE the candidate window at measured 2,894 -- the closest
# CONTINUOUS cluster to cluster_16 -- so it tests (a) vs (b) directly.
#   recovers -> the window is real, recovery is replicated, and the r/m-based
#               cap can be reinstated on two clusters instead of one.
#   fails    -> cluster_16 is atypical. Retire the r/m envelope entirely and
#               keep only the union-coverage and dating-threshold findings.
#
# SELECTED BY MODALITY SCREEN, not by mean (A.9 Finding 3). gap/mean 0.060,
# 5/20 empty bins -- continuous, comparable to cluster_16's 0.043 / 4-of-20.
# cluster_5 was the original pick and FAILED this screen (gap/mean 0.399, a
# 1,447-SNP internal gap, 3x worse than cluster_48). Do not select on mean,
# median, or their ratio: cluster_48 had mean 4,562 vs median 4,581 and is a
# three-sub-lineage mixture.
#
#   close reference : GCF_000260515_1_Thailand = strain **1026b** -- COMPLETE
#                     (2 contigs), constrained MEDOID of cluster_37
#                     (ref_mean_mash 0.000854), and a cluster member.
#   distant ref     : K96243 (GCF_000011545.1).
#
# BONUS, unplanned but valuable (see 2.4): the field is split between K96243
# (Chewapreecha and the Thai literature) and 1026b (the 2026 Vietnam study,
# 1,468 genomes) with NO PUBLISHED BRIDGE. Because this cluster's medoid IS
# 1026b, the close-vs-distant contrast here is a direct, same-genomes
# quantification of how much of the difference between those two literatures is
# reference artefact. Report it as such.
#
# Replicon slots matched by size, per Appendix A.4 (IDs are per-reference):
#   chr1  4,092,668 (1026b) vs 4,074,542 (K96243)
#   chr2  3,138,747 (1026b) vs 3,173,005 (K96243)
#
# n = 49, 46 dated over 32 years (1993-2025). 100% Thailand, 8 BioProjects,
# top BioProject 42.9% -- so also a further test of whether Thai-dominated
# sampling produces mixture structure. It does NOT here: this cluster is
# 100% Thai and still continuous.
set -euo pipefail
cd "$(dirname "$0")"

C37_CHR1="Burkholderia_pseudomallei_1026b_GCF_000260515.1_Thailand.fasta_1"
C37_CHR2="Burkholderia_pseudomallei_1026b_GCF_000260515.1_Thailand.fasta_2"

python3 reference_sensitivity_bp.py plan \
    --cluster-list cluster_metadata_cluster_37_genomes.tsv \
    --ref "close=refs/C37_close.fasta#${C37_CHR1},${C37_CHR2}" \
    --ref "K96243=refs/K96243.fasta#NC_006350.1,NC_006351.1" \
    --outdir refsens_cluster37 \
    --existing-preset snippy-contigs \
    --env-caller snp-phylogeny \
    --env-recomb bp-gubbins \
    --threads 16
