#!/usr/bin/env python3
"""
compare_partitions_bp.py

Does a network-based partition (PopPUNK) hold the diversity bound where single
linkage chained?

Context. The current Mash partition caps cluster SIZE at 50, and 79% of its
multi-genome clusters exceed the ~1,000-SNP diversity ceiling Gubbins needs
(Appendix A.3d). A single-linkage sweep on the same distance matrix could not
hold the bound either -- max within-cluster diversity ran 2.6-3.5x the
threshold at every setting, which is the recombinant-bridge chaining Hennart
2022 documented. An archived PopPUNK run on 3,592 genomes exists and overlaps
the current collection by ~75%, so it can be scored on the SAME distance matrix
and compared like for like.

This scores any number of partitions on a common set of genomes and reports,
per partition: cluster count, size distribution, within-cluster diversity, and
the fraction of clusters and genomes inside the derived cap. Restricting every
partition to the shared genome set is what makes the comparison fair.

Stdlib only.
"""

import argparse
import csv
import sys
from collections import defaultdict

from cluster_diversity_bp import read_phylip

CORE_ALN = 3_805_619
DERIVED_CAP = 1000
SENG_MAX = 549


def load_partition(path, id_col, cl_col):
    with open(path, newline="") as fh:
        head = fh.readline()
        fh.seek(0)
        d = "\t" if "\t" in head else ","
        rows = list(csv.DictReader(fh, delimiter=d))
    out = {}
    for r in rows:
        sid = (r.get(id_col) or "").strip()
        cid = (r.get(cl_col) or "").strip()
        if sid and cid:
            out[sid] = cid
    return out


def gini(vals):
    v = sorted(vals)
    n, tot = len(v), sum(v)
    if not n or not tot:
        return float("nan")
    cum = sum((i + 1) * x for i, x in enumerate(v))
    return (2.0 * cum) / (n * tot) - (n + 1.0) / n


def score(name, assign, idx, rows, core_len, restrict):
    groups = defaultdict(list)
    for sid, cid in assign.items():
        if sid in restrict and sid in idx:
            groups[cid].append(idx[sid])

    def d(i, j):
        if i == j:
            return 0.0
        if j < len(rows[i]):
            return rows[i][j]
        if i < len(rows[j]):
            return rows[j][i]
        return None

    sizes, means, maxes = [], [], []
    in_cap = in_cap_genomes = multi = 0
    for cid, members in groups.items():
        sizes.append(len(members))
        if len(members) < 2:
            continue
        ds = []
        for x in range(len(members)):
            for y in range(x + 1, len(members)):
                v = d(members[x], members[y])
                if v is not None:
                    ds.append(v)
        if not ds:
            continue
        multi += 1
        m = sum(ds) / len(ds)
        means.append(m * core_len)
        maxes.append(max(ds) * core_len)
        if m * core_len <= DERIVED_CAP:
            in_cap += 1
            in_cap_genomes += len(members)
    sizes.sort(reverse=True)
    gen = sum(sizes)
    return {
        "name": name, "genomes": gen, "clusters": len(sizes),
        "largest": sizes[0] if sizes else 0,
        "singletons": sum(1 for s in sizes if s == 1),
        "gini": gini(sizes),
        "multi": multi,
        "median_div": sorted(means)[len(means) // 2] if means else 0,
        "mean_div": sum(means) / len(means) if means else 0,
        "max_div": max(maxes) if maxes else 0,
        "in_cap": in_cap,
        "in_cap_genomes": in_cap_genomes,
        "cap_frac": (100.0 * in_cap / multi) if multi else 0,
        "cap_gen_frac": (100.0 * in_cap_genomes / gen) if gen else 0,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phylip", required=True)
    ap.add_argument("--partition", action="append", required=True,
                    metavar="NAME=PATH:IDCOL:CLCOL",
                    help="repeatable")
    ap.add_argument("--core-len", type=int, default=CORE_ALN)
    a = ap.parse_args()

    names, rows, idx = read_phylip(a.phylip)

    parts = []
    for spec in a.partition:
        nm, rest = spec.split("=", 1)
        path, idc, clc = rest.split(":")
        parts.append((nm, load_partition(path, idc, clc)))
        print("%-12s %6d genomes assigned" % (nm, len(parts[-1][1])))

    # fair comparison: only genomes present in EVERY partition and in the matrix
    shared = set(idx)
    for _, p in parts:
        shared &= set(p)
    print("\nshared genomes scored by all partitions: %d" % len(shared))
    if len(shared) < 50:
        sys.exit("ERROR: too few shared genomes to compare.")

    res = [score(nm, p, idx, rows, a.core_len, shared) for nm, p in parts]

    print("\n%-12s %7s %7s %7s %6s %6s %10s %10s %10s"
          % ("partition", "genomes", "clust", "largest", "singl", "Gini",
             "med_div", "mean_div", "max_div"))
    print("-" * 86)
    for r in res:
        print("%-12s %7d %7d %7d %6d %6.3f %10.0f %10.0f %10.0f"
              % (r["name"], r["genomes"], r["clusters"], r["largest"],
                 r["singletons"], r["gini"], r["median_div"], r["mean_div"],
                 r["max_div"]))

    print("\n%-12s %10s %14s %16s"
          % ("partition", "multi-clu", "within cap", "genomes in cap"))
    print("-" * 60)
    for r in res:
        print("%-12s %10d %8d (%4.1f%%) %9d (%4.1f%%)"
              % (r["name"], r["multi"], r["in_cap"], r["cap_frac"],
                 r["in_cap_genomes"], r["cap_gen_frac"]))

    print("\nCap = mean pairwise <= %d approx SNPs (GAP2 derived; Seng's"
          % DERIVED_CAP)
    print("successful lineages sat at %d-549). 'max_div' is the chaining"
          % 351)
    print("check: a partition whose worst cluster greatly exceeds the others")
    print("is fusing groups through recombinant bridges.")


if __name__ == "__main__":
    sys.exit(main())
