#!/usr/bin/env bash
# Measure how the parsnp core shrinks with genome count.
#
# The question: an all-sample global tree is only worth building if the shared
# core stays large. parsnp's core shrinks toward the most fragmented member, and
# across 2,342 divergent B. pseudomallei genomes it may collapse. Measuring that
# on a ladder is far cheaper than finding out after a full run.
#
# Matches GLOBAL_CORE_ALIGNMENT: anchors on the member with the fewest contigs,
# and passes -c so parsnp includes EVERY genome. Without -c parsnp silently drops
# genomes it considers too divergent, which would make the core look stable by
# discarding exactly the genomes that shrink it.
#
# Seeded sampling, so the ladder is reproducible and nested.
set -uo pipefail
B=/home/phemarajata/Downloads/snp-mod-local-working
FASTA=$B/v4c_local/fasta
OUT=$B/core_shrinkage
IMG=quay.io/biocontainers/parsnp:1.7.4--hdcf5f25_2
mkdir -p "$OUT"
RESULT=$OUT/core_vs_n.tsv
[ -f "$RESULT" ] || printf 'n\tanchor_contigs\tcore_bp\tlcbs\truntime_s\tgenomes_in_aln\n' > "$RESULT"

# the analysed set (A100 final partition)
python3 - <<'PY' > "$OUT/analysed_ids.txt"
p="/tmp/claude-1000/-home-phemarajata-Downloads-snp-mod-local-working/e0d996af-e0e5-40f6-b70a-dba36df0e128/scratchpad/a100/partition/curated_L1v4c_clusters.final.tsv"
seen=set()
for i,l in enumerate(open(p)):
    if i==0: continue
    f=l.rstrip("\r\n").split("\t")
    if len(f)>=2: seen.add(f[1])
print("\n".join(sorted(seen)))
PY
TOTAL=$(wc -l < "$OUT/analysed_ids.txt")
echo "analysed genomes available: $TOTAL"

for N in "$@"; do
  D=$OUT/n$N
  if [ -s "$D/core_bp" ]; then echo "n=$N already done ($(cat $D/core_bp) bp), skipping"; continue; fi
  rm -rf "$D"; mkdir -p "$D/in"
  # seeded, nested subsample
  python3 - "$OUT/analysed_ids.txt" "$N" > "$D/ids.txt" <<'PY'
import sys, random
ids = open(sys.argv[1]).read().split()
random.seed(20260819)          # fixed: the ladder must be reproducible and nested
random.shuffle(ids)
print("\n".join(ids[:int(sys.argv[2])]))
PY
  while read -r s; do [ -f "$FASTA/$s.fasta" ] && ln -sf "$FASTA/$s.fasta" "$D/in/$s.fasta"; done < "$D/ids.txt"
  n_in=$(ls "$D/in" | wc -l)
  # anchor = fewest contigs, same rule as GLOBAL_CORE_ALIGNMENT
  REF=$(for f in "$D"/in/*.fasta; do printf '%s\t%s\n' "$(grep -c '^>' "$f")" "$f"; done | sort -n | awk -F'\t' 'NR==1{print $2}')
  RC=$(grep -c '^>' "$REF")
  echo "[n=$N] $n_in genomes, anchor $(basename "$REF") ($RC contigs) -- starting $(date '+%H:%M:%S')"
  t0=$(date +%s)
  timeout 21600 docker run --rm -v "$B":"$B" -w "$D" "$IMG" \
    parsnp -r "$REF" -d "$D/in" -o "$D/out" -p 20 -c --skip-phylogeny \
    > "$D/parsnp.log" 2>&1
  rc=$?; t1=$(date +%s); dt=$((t1-t0))
  if [ $rc -ne 0 ] || [ ! -s "$D/out/parsnp.xmfa" ]; then
    echo "[n=$N] FAILED rc=$rc after ${dt}s -- see $D/parsnp.log"
    printf '%s\t%s\tFAILED\t-\t%s\t-\n' "$N" "$RC" "$dt" >> "$RESULT"
    continue
  fi
  # core = summed LCB length for a single sequence in the xmfa
  read -r CORE LCB NSEQ < <(python3 - "$D/out/parsnp.xmfa" <<'PY'
import sys, re
core=0; lcb=0; seqs=set(); cur=None; buf=0; first=None
for line in open(sys.argv[1]):
    if line.startswith('>'):
        m=re.match(r'>\s*(\d+):', line)
        if m: seqs.add(m.group(1))
        if first is None and m: first=m.group(1)
        cur = (m.group(1)==first) if m else False
        if cur: lcb+=1
    elif line.startswith('='):
        core+=buf; buf=0
    elif cur:
        buf += len(line.strip())
core+=buf
print(core, lcb, len(seqs))
PY
)
  echo "$CORE" > "$D/core_bp"
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$N" "$RC" "$CORE" "$LCB" "$dt" "$NSEQ" >> "$RESULT"
  echo "[n=$N] core=${CORE} bp over ${LCB} LCBs, ${NSEQ} genomes in alignment, ${dt}s"
  rm -rf "$D/out/blocks" 2>/dev/null
done
echo "=== ladder ==="; column -t "$RESULT"
