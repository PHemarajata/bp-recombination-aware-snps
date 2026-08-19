#!/usr/bin/env bash
# Reference-sensitivity experiment, cluster_48 -- the FIFTH cluster.
#
# Why this one: RECOVERY IS UNREPLICATED. Across four clusters the regime tally
# is under-detection 1 (c53), contrast loss 2 (c8, c0), and recovery exactly 1
# (c16, measured 3,639). Every downstream claim -- the ~3,600 cap, the
# two-failure-mode structure, the 11.9% -> 39.4% usable-genome gain, and the
# case for rebuilding the pipeline around a corrected cap -- rests on that
# single observation. cluster_8 replicated FAILURE, which does not protect
# against cluster_16 being atypical.
#
# cluster_48 is the first cluster selected from MEASURED diversity rather than
# the Mash proxy (which mis-scaled by 0.90x-91x and caused two targeting misses
# of 1.9x and 2.1x). Measured mean 4,562, median 4,581 -- skew 1.00, i.e.
# homogeneous, not a tight core plus outliers like cluster_38 (mean 4,112,
# median 73).
#
# Two outcomes, both useful:
#   recovers -> recovery is REPLICATED and the envelope extends to >=4,562,
#               raising the cap and the usable fraction to ~47.6% of genomes.
#   fails    -> the envelope is narrow. NOTE this outcome is ambiguous: it is
#               consistent both with a narrow envelope AND with cluster_16
#               being atypical, and it would NOT settle reproducibility. In
#               that case run a cluster AT ~3,600 next -- cluster_5 (3,623) or
#               cluster_26 (3,833) -- which tests reproducibility directly.
#
#   close reference : GCF_027856475_2_China_Hong_Kong (strain 22MB031188) --
#                     COMPLETE (2 contigs), constrained MEDOID of cluster_48
#                     (ref_mean_mash 0.000761), and a cluster member. 3 of its
#                     members are complete, so this was not a borrow.
#   distant ref     : K96243 (GCF_000011545.1).
#
# Replicon slots matched by size, per Appendix A.4 (IDs are per-reference):
#   chr1  3,968,196 (22MB031188) vs 4,074,542 (K96243)
#   chr2  3,087,390 (22MB031188) vs 3,173,005 (K96243)
#
# n = 50, 48 dated over 22 years (2002-2024). The span is short, so this is a
# WEAK dating test -- Duchene 2016 calls <10 years unreliable and 22 is modest.
# Treat the root-to-tip result here as supporting, not as a fifth independent
# negative.
set -euo pipefail
cd "$(dirname "$0")"

C48_CHR1="Burkholderia_pseudomallei_22MB031188_GCF_027856475.2_China_Hong_Kong.fasta_1"
C48_CHR2="Burkholderia_pseudomallei_22MB031188_GCF_027856475.2_China_Hong_Kong.fasta_2"

python3 reference_sensitivity_bp.py plan \
    --cluster-list cluster_metadata_cluster_48_genomes.tsv \
    --ref "close=refs/C48_close.fasta#${C48_CHR1},${C48_CHR2}" \
    --ref "K96243=refs/K96243.fasta#NC_006350.1,NC_006351.1" \
    --outdir refsens_cluster48 \
    --existing-preset snippy-contigs \
    --env-caller snp-phylogeny \
    --env-recomb bp-gubbins \
    --threads 16
