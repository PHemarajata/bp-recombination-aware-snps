#!/usr/bin/env bash
# Reference-sensitivity experiment, cluster_53 -- the SECOND cluster.
#
# Why this one: 49 genomes, 8 countries, 22 BioProjects, 41 dated over a
# 62-YEAR span (cluster_0 spanned 28). The longer temporal window is the point:
# it tests the DATING conclusion rather than re-testing the reference
# conclusion, which cluster_0 already settled.
#
#   close reference : GCF_003546995_3_Malaysia (strain H10) -- COMPLETE
#                     (2 contigs), and a member of cluster_53. Complete
#                     matters: Gubbins cannot use a multi-contig reference.
#   distant ref     : K96243 (GCF_000011545.1).
#
# Replicon slots matched by size: chr1 4.10 vs 4.07 Mb, chr2 3.19 vs 3.17 Mb.
set -euo pipefail
cd "$(dirname "$0")"

H10_CHR1="Burkholderia_pseudomallei_H10_GCF_003546995.3_Malaysia.fasta_1"
H10_CHR2="Burkholderia_pseudomallei_H10_GCF_003546995.3_Malaysia.fasta_2"

python3 reference_sensitivity_bp.py plan \
    --cluster-list cluster_metadata_cluster_53_genomes.tsv \
    --ref "close=refs/H10_close.fasta#${H10_CHR1},${H10_CHR2}" \
    --ref "K96243=refs/K96243.fasta#NC_006350.1,NC_006351.1" \
    --outdir refsens_cluster53 \
    --existing-preset snippy-contigs \
    --env-caller snp-phylogeny \
    --env-recomb bp-gubbins \
    --threads 16
