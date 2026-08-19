#!/usr/bin/env bash
# Generate the reference-sensitivity experiment for cluster_0.
#
#   close reference : GCF_003547015_1 (strain R15) -- a COMPLETE genome that is
#                     itself a member of cluster_0. Complete matters: Gubbins
#                     cannot use a multi-contig reference, and the pipeline's
#                     own cluster_0 representative (GCF_028621445_1_missing) is
#                     a 135-contig draft, so it cannot serve as a reference.
#   distant ref     : K96243 (GCF_000011545.1), the literature standard.
#
# Replicon slots are matched by size: chr1 4.07 Mb both, chr2 3.17 / 3.11 Mb.
set -euo pipefail
cd "$(dirname "$0")"

R15_CHR1="CP025304.1_Burkholderia_pseudomallei_strain_R15_chromosome_R15.1_complete_sequence"
R15_CHR2="CP025305.1_Burkholderia_pseudomallei_strain_R15_chromosome_R15.2_complete_sequence"

python3 reference_sensitivity_bp.py plan \
    --cluster-list cluster_metadata_cluster_0_genomes.tsv \
    --ref "close=refs/R15_close.fasta#${R15_CHR1},${R15_CHR2}" \
    --ref "K96243=refs/K96243.fasta#NC_006350.1,NC_006351.1" \
    --outdir refsens_cluster0 \
    --existing-preset snippy-contigs \
    --env-caller snp-phylogeny \
    --env-recomb bp-gubbins \
    --threads 16
