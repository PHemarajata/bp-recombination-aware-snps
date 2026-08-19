#!/usr/bin/env python3
"""
rank_reference_alternates_bp.py

For every analysis unit, rank the complete genomes that could serve as its
mapping reference, so that a unit whose reference breaks Gubbins has a stated
next choice instead of an ad-hoc one.

WHY A RANKED LIST AND NOT A RETRY INSIDE GUBBINS. The failure being recovered
from is a property of the REFERENCE, and the reference is consumed far upstream
of Gubbins -- it determines the mapping, hence the alignment, hence the site
patterns RAxML cannot fit. Nothing Gubbins can retry fixes it. Recovery means
re-mapping the unit against a different genome, which is a new pass over the
pipeline, not a new attempt at one process. So the ordering is decided here,
once, in advance, and `retry_failed_references.sh` walks it.

THE ORDER IS THE SAME CRITERION AS THE PRIMARY PICK, so the fallback is not a
second, weaker rule: candidates must pass the completeness gate (Gubbins cannot
use a multi-contig reference at all), must not be blocklisted, and are then
ranked by mean Mash distance to the unit's members, ties broken by max. Rank 1
is therefore what the picker would have chosen had it been searching the whole
collection; the primary already in use is marked IN_USE wherever it appears.

Distances come from the same Mash matrix as everything else, so a promotion
never changes the distance basis mid-analysis.
"""

import argparse
import collections
import csv
import json
import os
import sys


def norm(name):
    out = "".join(ch if ch.isalnum() else "_" for ch in name)
    return "_".join(x for x in out.split("_") if x)


def contig_count(path):
    n = 0
    try:
        with open(path) as fh:
            for line in fh:
                if line.startswith(">"):
                    n += 1
    except OSError:
        return None
    return n or None


def load_contig_cache(fasta_dir, cache_path):
    """
    Contig counts for the whole collection, cached.

    Counting headers across ~2,800 multi-megabyte FASTAs is minutes of pure I/O
    and the answer never changes, so it is written once and reused. The cache is
    keyed on the directory it was built from.
    """
    if cache_path and os.path.exists(cache_path):
        with open(cache_path) as fh:
            blob = json.load(fh)
        if blob.get("fasta_dir") == os.path.abspath(fasta_dir):
            return blob["counts"]
    counts = {}
    for fn in sorted(os.listdir(fasta_dir)):
        if fn.endswith((".fasta", ".fa", ".fna")):
            stem = fn.rsplit(".", 1)[0]
            c = contig_count(os.path.join(fasta_dir, fn))
            if c:
                counts[stem] = c
    if cache_path:
        with open(cache_path, "w") as fh:
            json.dump({"fasta_dir": os.path.abspath(fasta_dir),
                       "counts": counts}, fh)
    return counts


def read_matrix(path, wanted):
    keep = {norm(w) for w in wanted}
    with open(path) as fh:
        names = [norm(n) for n in fh.readline().rstrip("\n").split("\t")[1:]]
        col = {n: i for i, n in enumerate(names)}
        rows = {}
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            key = norm(parts[0]) if parts else ""
            if key in keep:
                rows[key] = parts[1:]
    return rows, col, names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clusters", required=True, help="curated_L1_clusters.tsv")
    ap.add_argument("--refs", default=None,
                    help="refs currently in use, only to mark IN_USE; omit on "
                         "the first pass, when nothing is in use yet")
    ap.add_argument("--matrix", required=True, help="labelled square Mash TSV")
    ap.add_argument("--fasta-dir", required=True)
    ap.add_argument("--blocklist", default=None)
    ap.add_argument("--max-contigs", type=int, default=2)
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--cache", default=".contig_counts.json")
    ap.add_argument("--out", default="curated_L1_ref_alternates.tsv")
    a = ap.parse_args()

    blocked = []
    if a.blocklist:
        with open(a.blocklist) as fh:
            for line in fh:
                line = line.split("#", 1)[0].strip()
                if line:
                    blocked.append(line)

    units = collections.defaultdict(list)
    with open(a.clusters) as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r)
        for row in r:
            units[row[0]].append(row[1])

    in_use = {}
    if a.refs:
        with open(a.refs) as fh:
            r = csv.reader(fh, delimiter="\t")
            next(r)
            for row in r:
                in_use[row[0]] = os.path.basename(row[1]).rsplit(".", 1)[0]

    counts = load_contig_cache(a.fasta_dir, a.cache)
    candidates = [s for s, c in counts.items()
                  if c <= a.max_contigs
                  and not any(s.startswith(p) for p in blocked)]
    print(f"collection            : {len(counts)} assemblies")
    print(f"complete (<= {a.max_contigs} contigs): {len(candidates)}, after blocklist")

    members = {s for v in units.values() for s in v}
    rows, col, names = read_matrix(a.matrix, members)
    cand_idx = {c: col[norm(c)] for c in candidates if norm(c) in col}
    print(f"candidates in matrix  : {len(cand_idx)}")
    missing = [u for u in units if any(norm(s) not in rows for s in units[u])]
    if missing:
        sys.exit(f"members absent from the Mash matrix in units: {missing[:3]}")

    out = []
    for cid in sorted(units, key=lambda c: (int(c.split("_")[1]),
                                            int(c.split("_L1_")[1]))):
        mem = [rows[norm(s)] for s in units[cid]]
        memset = {norm(s) for s in units[cid]}
        scored = []
        for cand, j in cand_idx.items():
            if norm(cand) in memset and len(units[cid]) < 2:
                continue
            ds = []
            for row in mem:
                v = row[j]
                if v != "":
                    ds.append(float(v))
            if ds:
                scored.append((sum(ds) / len(ds), max(ds), cand))
        scored.sort()
        cur = in_use.get(cid)
        for rank, (mean_d, max_d, cand) in enumerate(scored[:a.top], start=1):
            out.append((cid, rank, cand, f"{mean_d:.6f}", f"{max_d:.6f}",
                        "IN_USE" if cand == cur else ""))
        if cur and cur not in [t[2] for t in scored[:a.top]]:
            for mean_d, max_d, cand in scored:
                if cand == cur:
                    out.append((cid, 0, cand, f"{mean_d:.6f}", f"{max_d:.6f}",
                                "IN_USE"))
                    break

    with open(a.out, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["cluster_id", "rank", "reference", "mean_mash",
                    "max_mash", "note"])
        for row in sorted(out, key=lambda t: (int(t[0].split("_")[1]),
                                              int(t[0].split("_L1_")[1]),
                                              t[1])):
            w.writerow(row)

    ranked_first = collections.Counter()
    for cid in units:
        top = [t for t in out if t[0] == cid and t[1] == 1]
        if top:
            ranked_first["primary is rank 1" if top[0][5] == "IN_USE"
                         else "primary is not rank 1"] += 1
    print(f"\nunits ranked          : {len(units)}, up to {a.top} alternates each")
    for k, v in ranked_first.most_common():
        print(f"  {k}: {v}")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
