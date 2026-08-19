#!/usr/bin/env bash
# PopPUNK refit on the current 2,802-genome collection.
#
# Parameters are Seng et al. 2024's published in-organism fit (PMID 38972886),
# which is the only configuration demonstrated to feed Gubbins successfully in
# B. pseudomallei:
#     --min-k 15 --max-k 31 --k-step 2 --K 4 --max-a-dist 0.53
# Their fit gave density 0.028, transitivity 0.992, network score 0.8961.
# The documented bar for a good fit is a network score >= 0.8; report ours
# against that.
#
# Why refit rather than reuse the archived run: the archived combined_clusters
# .csv covers 3,592 genomes of which only 2,297 still resolve to a FASTA (the
# rest were dropped when the collection was deduplicated). A fresh fit matches
# the current collection exactly and removes the stale-path and naming
# problems that stalled PopPIPE-bp.
set -euo pipefail
cd "$(dirname "$0")"

# `set -u` must be OFF for BOTH the hook and the activate. The hook activates
# the BASE env, which runs miniforge3/etc/conda/activate.d/activate-gcc_linux-64.sh,
# and that dereferences an unbound SYS_SYSROOT. Wrapping only `conda activate`
# is not enough -- the hook dies first, silently, before anything runs.
set +u
eval "$(conda shell.bash hook)"
conda activate poppipe
set -u

FASTA_DIR=/home/phemarajata/Downloads/final_deduped_all_BP_with_locations
OUT=poppunk_bp
THREADS=${THREADS:-16}

mkdir -p "$OUT"

# rfile: <name>\t<path>, one per genome. This is the file whose truncation to a
# single line is what killed PopPIPE-bp at Snakefile:25.
if [ ! -s "$OUT/rfile.txt" ]; then
    : > "$OUT/rfile.txt"
    for f in "$FASTA_DIR"/*.fasta; do
        n=$(basename "$f" .fasta)
        printf '%s\t%s\n' "$n" "$f" >> "$OUT/rfile.txt"
    done
fi
echo "rfile lines: $(wc -l < "$OUT/rfile.txt")"

# Guard: the failure mode that stalled the previous attempt was an rfile with
# one line against a clusters file with thousands. Refuse to proceed on a
# suspiciously short rfile.
N=$(wc -l < "$OUT/rfile.txt")
if [ "$N" -lt 100 ]; then
    echo "ERROR: rfile has only $N lines. That is the PopPIPE-bp failure mode." >&2
    exit 2
fi

# PopPUNK builds some output paths as os.path.join(prefix, prefix + ext), so a
# multi-component --output such as "poppunk_bp/db" becomes
# "poppunk_bp/db/poppunk_bp/db.png" and crashes on a missing directory. Run
# from inside the output directory and use FLAT names so this cannot happen.
RFILE_ABS="$(cd "$OUT" && pwd)/rfile.txt"
cd "$OUT"

echo "=== 1. create database (sketching) ==="
if [ ! -s "db/db.h5" ]; then
    poppunk --create-db --r-files "$RFILE_ABS" --output db \
            --min-k 15 --max-k 31 --k-step 2 --threads "$THREADS"
else
    echo "db/db.h5 already present -- skipping sketching"
fi

echo "=== 2. fit model (Seng parameters) ==="
poppunk --fit-model bgmm --ref-db db --output fit \
        --K 4 --max-a-dist 0.53 --threads "$THREADS"

echo "=== done ==="
ls -la fit | head
echo "--- cluster assignment ---"
CL=$(ls fit/*_clusters.csv 2>/dev/null | head -1)
if [ -n "$CL" ]; then
    echo "clusters file: $CL"
    python3 - "$CL" <<'PY'
import csv, sys, collections
rows=list(csv.DictReader(open(sys.argv[1])))
c=collections.Counter(r["Cluster"] for r in rows)
s=sorted(c.values(), reverse=True)
print("genomes: %d  clusters: %d  largest: %d  singletons: %d"
      % (len(rows), len(c), s[0], sum(1 for x in s if x==1)))
PY
fi
