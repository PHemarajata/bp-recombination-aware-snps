#!/usr/bin/env bash
# Build the A100 transfer bundle: one flat, compressed archive of every assembly
# in the panel, named <sample_id>.fasta so no path rewriting is needed on the
# other side.
set -euo pipefail
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
W="$S/.build"
rm -rf "$W"; mkdir -p "$W"

python3 - "$S" <<'PY'
import csv, os, sys
S = sys.argv[1]
rows = list(csv.DictReader(open(os.path.join(os.path.dirname(S), 'L1v4b_MERGED_METADATA.tsv')), delimiter='\t'))
with open(os.path.join(S, '.build', 'list.tsv'), 'w') as fh:
    for r in rows:
        fh.write(r['assembly_path'] + '\t' + r['sample_id'] + '.fasta\n')
print(f"{len(rows)} assemblies to stage")
PY

cd "$W"
mkdir -p fasta
while IFS=$'\t' read -r src name; do
  ln -s "$src" "fasta/$name"
done < list.tsv
echo "symlinks: $(ls fasta | wc -l)"

# -h follows the symlinks so the archive carries real bytes.
tar -chf - fasta | zstd -T4 -3 -q -o "$S/fasta.tar.zst"
sha256sum "$S/fasta.tar.zst" > "$S/fasta.tar.zst.sha256"
rm -rf "$W"
ls -la "$S/fasta.tar.zst"
echo "BUNDLE DONE"
