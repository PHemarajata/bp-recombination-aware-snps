#!/usr/bin/env python3
"""Panel-wide assembly statistics for the accessory-attribution control.

Contig count is the confounder of record (HANDOFF 2026-08-21 evening §1.2):
a gene that is present but unassembled reads as absent, and assembly quality
tracks sequencing centre, which tracks country. Also emits total length, N50
and GC so the control can distinguish fragmentation from genuine size
differences.
"""
import glob, os, sys
from concurrent.futures import ProcessPoolExecutor

def stats(path):
    name = os.path.basename(path)[:-6]
    lens, gc, n = [], 0, 0
    cur = 0
    with open(path) as fh:
        for line in fh:
            if line[0] == '>':
                if cur:
                    lens.append(cur)
                cur = 0
            else:
                s = line.strip()
                cur += len(s)
                gc += s.count('G') + s.count('C') + s.count('g') + s.count('c')
                n += s.count('N') + s.count('n')
    if cur:
        lens.append(cur)
    lens.sort(reverse=True)
    total = sum(lens)
    half, run, n50 = total / 2, 0, 0
    for L in lens:
        run += L
        if run >= half:
            n50 = L
            break
    return (name, len(lens), total, n50, lens[0] if lens else 0,
            round(gc / total, 5) if total else 0, n)

if __name__ == "__main__":
    files = sorted(glob.glob(sys.argv[1]))
    with ProcessPoolExecutor(max_workers=16) as ex:
        rows = list(ex.map(stats, files, chunksize=8))
    with open(sys.argv[2], "w") as out:
        out.write("sample_id\tcontigs\ttotal_bp\tn50\tlongest_contig\tgc\tambiguous_bases\n")
        for r in sorted(rows):
            out.write("\t".join(str(x) for x in r) + "\n")
    print(f"wrote {sys.argv[2]}: {len(rows)} genomes")
