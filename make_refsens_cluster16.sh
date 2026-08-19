#!/usr/bin/env bash
# Reference-sensitivity experiment, cluster_16 -- the THIRD cluster.
#
# Why this one: it is the only measurement that locates the diversity cap.
# cluster_0 measured 9,433 mean pairwise SNPs (saturated -- cumulative
# recombination 2.70x genome length, no usable clonal frame) and cluster_53
# measured 535 (clean, inside Seng's 351-549 band). So the cap is bracketed
# only to (535, 9433], and the derived ~1,000 sits near the bottom of a
# bracket spanning more than an order of magnitude. cluster_16's predicted
# true diversity is ~1,900 -- the middle of that bracket, and exactly on the
# 1,000-vs-2,000 decision boundary.
#
# One run answers four questions:
#   1. Locates the cap (clonal-frame-retained diagnostic at ~1,900).
#   2. Third anchor for the Mash->SNP proxy, which overestimates 1.36x-4.23x
#      and needs a mid-range point to be correctable at all (Appendix A.5).
#   3. The intermediate reference-bias point: cluster_0 gave +28% at 9,433 and
#      cluster_53 gave +630% at 535, so this turns two points into a
#      dose-response curve.
#   4. Third independent test of the no-clock claim -- 30 dated genomes over
#      60 years (1965-2025), a span comparable to cluster_53's 62.
#
#   close reference : GCF_003547055_1_Malaysia (strain PMC2000) -- COMPLETE
#                     (2 contigs), the constrained MEDOID of cluster_16
#                     (ref_mean_mash 0.001155, ref_max_mash 0.002094), and a
#                     member of the cluster. Complete matters: Gubbins cannot
#                     use a multi-contig reference.
#   distant ref     : K96243 (GCF_000011545.1).
#
# Replicon slots matched by size, per Appendix A.4 (IDs are per-reference, so
# match by position and VERIFY by length):
#   chr1  4,013,273 (PMC2000) vs 4,074,542 (K96243)
#   chr2  3,173,851 (PMC2000) vs 3,173,005 (K96243)
set -euo pipefail
cd "$(dirname "$0")"

C16_CHR1="Burkholderia_pseudomallei_PMC2000_GCF_003547055.1_Malaysia.fasta_1"
C16_CHR2="Burkholderia_pseudomallei_PMC2000_GCF_003547055.1_Malaysia.fasta_2"

python3 reference_sensitivity_bp.py plan \
    --cluster-list cluster_metadata_cluster_16_genomes.tsv \
    --ref "close=refs/C16_close.fasta#${C16_CHR1},${C16_CHR2}" \
    --ref "K96243=refs/K96243.fasta#NC_006350.1,NC_006351.1" \
    --outdir refsens_cluster16 \
    --existing-preset snippy-contigs \
    --env-caller snp-phylogeny \
    --env-recomb bp-gubbins \
    --threads 16
