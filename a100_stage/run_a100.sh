#!/usr/bin/env bash
# One command to run the v4b panel on the DGX Station A100.
#
#   cd <stage dir> && ./run_a100.sh              # real run
#   DRY_RUN=1 ./run_a100.sh                      # build + validate inputs only
#
# Everything machine-specific is set here; run_wf_curated_L1.sh reads it from the
# environment. That script carries the fixes that matter and is unchanged from
# the workstation copy -- do not fork it.
set -uo pipefail

A100_BASE="${A100_BASE:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"
NFDIR="${NFDIR:-$HOME/wf-assembly-snps-mod}"
CONDA_SH="${CONDA_SH:-$HOME/miniforge3/etc/profile.d/conda.sh}"
NFENV="${NFENV:-nextflow-wf}"

echo "=== preflight ==="
CORES=$(nproc)
MEMGB=$(awk '/MemTotal/{printf "%d", $2/1024/1024}' /proc/meminfo)
echo "  logical cores : ${CORES}"
echo "  physical cores: $(lscpu 2>/dev/null | awk -F: '/^Core\(s\) per socket/{c=$2} /^Socket\(s\)/{s=$2} END{printf "%d", c*s}')"
echo "  total RAM     : ${MEMGB} GB"
echo "  free disk here: $(df -h "${A100_BASE}" | tail -1 | awk '{print $4}')"
# The overrides assume a 118-core / 460 GB executor budget. If the box is
# smaller, Nextflow will happily accept the config and then never schedule the
# heavy stages -- fail here instead, where it costs five seconds.
if [ "${CORES}" -lt 100 ] || [ "${MEMGB}" -lt 400 ]; then
  echo "  WARNING: box is smaller than the overrides assume (118 cores / 460 GB)." >&2
  echo "           Edit curated_L1_overrides_a100.config: executor \$local cpus/memory," >&2
  echo "           then re-run. Not stopping, but the heavy stages will queue." >&2
fi
for t in docker nextflow java; do
  command -v "$t" >/dev/null || echo "  MISSING: $t" >&2
done
[ -d "${NFDIR}" ] || { echo "ERROR: workflow repo not at ${NFDIR}" >&2; exit 1; }

echo "=== resolving staged paths ==="
# The staged inputs carry __A100_BASE__ so they are location-independent. Resolve
# in place, idempotently.
for f in inputs/wf_L1v4b_samplesheet.csv inputs/curated_L1v4b_refs.tsv; do
  sed -i "s#__A100_BASE__#${A100_BASE}#g" "${A100_BASE}/${f}"
done
MISS=$(awk -F, 'NR>1{print $2}' "${A100_BASE}/inputs/wf_L1v4b_samplesheet.csv" \
       | while read -r f; do [ -f "$f" ] || echo "$f"; done | head -5)
if [ -n "${MISS}" ]; then
  echo "ERROR: staged assemblies missing, e.g.:" >&2; echo "${MISS}" >&2
  echo "  did fasta/ finish extracting? expected 2973 files, found $(ls "${A100_BASE}/fasta" 2>/dev/null | wc -l)" >&2
  exit 1
fi
echo "  all referenced assemblies present ($(ls "${A100_BASE}/fasta" | wc -l) files staged)"

source "${CONDA_SH}" 2>/dev/null && conda activate "${NFENV}" 2>/dev/null || true

echo "=== launching ==="
export BASE="${A100_BASE}" NFDIR CONDA_SH
export PROFILE="bp,dgx_station_a100_updated,docker"
export COLLDIR="${A100_BASE}/fasta"
export OVERRIDES="${A100_BASE}/curated_L1_overrides_a100.config"
export ALLSS="${A100_BASE}/inputs/wf_L1v4b_samplesheet.csv"
export GENSS="${A100_BASE}/inputs/wf_L1v4b_run_samplesheet.csv"
export CLUSTERS="${A100_BASE}/inputs/curated_L1v4b_clusters.tsv"
export REFS="${A100_BASE}/inputs/curated_L1v4b_refs.tsv"
export OUTDIR="${A100_BASE}/L1v4b_out"
export WORKDIR="${WORKDIR:-${A100_BASE}/L1v4b_work}"
export DRY_RUN="${DRY_RUN:-}"

exec "${A100_BASE}/bin/run_wf_curated_L1.sh"
