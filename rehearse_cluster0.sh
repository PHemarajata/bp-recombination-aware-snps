#!/usr/bin/env bash
# Rehearse the cluster_0 analysis on SYNTHETIC Gubbins-shaped output that
# carries the REAL cluster_0 sample IDs and collection years.
#
# This spends no real compute and proves the part most likely to fail
# silently: that sample_id -> tree tip label -> dates join actually resolves,
# so section E (root-to-tip) will not come back empty after a multi-hour run.
set -euo pipefail
cd "$(dirname "$0")"

python3 reference_sensitivity_bp.py demo \
    --outdir _rehearsal \
    --pattern positive \
    --taxa-from cluster_metadata_cluster_0_dates.csv
