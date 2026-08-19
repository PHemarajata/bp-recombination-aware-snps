#!/usr/bin/env bash
# Reference-sensitivity experiment, cluster_8 -- the FOURTH cluster.
#
# Why this one: it is the single measurement that separates the two competing
# explanations for A.6. cluster_16 (measured 3,639 mean pairwise SNPs) recovers
# all three published recombination anchors, while cluster_53 (535)
# under-detects and cluster_0 (9,433) loses contrast. That pattern is either
#   (a) a DIVERSITY DETECTION ENVELOPE centred well above the derived ~1,000
#       cap, or
#   (b) cluster_16 simply being a more recombinogenic lineage.
# With three points the two are indistinguishable. cluster_8's predicted true
# diversity is ~4,500 -- just above cluster_16. Under (a) it should also recover
# r/m ~7 and union ~78%; under (b) it should fall back toward ~1.0 like its
# neighbours. Either answer is decisive.
#
#   close reference : GCF_000755945_1_Australia (strain MSHR5858) -- COMPLETE
#                     (2 contigs), the constrained MEDOID of cluster_8
#                     (ref_mean_mash 0.002134), and a cluster member.
#   distant ref     : K96243 (GCF_000011545.1).
#
# Replicon slots matched by size, per Appendix A.4 (IDs are per-reference):
#   chr1  3,925,545 (MSHR5858) vs 4,074,542 (K96243)
#   chr2  3,146,583 (MSHR5858) vs 3,173,005 (K96243)
#
# n = 50, 44 dated over 49 years (1976-2025) -> also a fourth dating test.
set -euo pipefail
cd "$(dirname "$0")"

C8_CHR1="Burkholderia_pseudomallei_MSHR5858_GCF_000755945.1_Australia.fasta_1"
C8_CHR2="Burkholderia_pseudomallei_MSHR5858_GCF_000755945.1_Australia.fasta_2"

python3 reference_sensitivity_bp.py plan \
    --cluster-list cluster_metadata_cluster_8_genomes.tsv \
    --ref "close=refs/C8_close.fasta#${C8_CHR1},${C8_CHR2}" \
    --ref "K96243=refs/K96243.fasta#NC_006350.1,NC_006351.1" \
    --outdir refsens_cluster8 \
    --existing-preset snippy-contigs \
    --env-caller snp-phylogeny \
    --env-recomb bp-gubbins \
    --threads 16
