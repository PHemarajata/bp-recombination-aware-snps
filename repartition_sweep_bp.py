#!/usr/bin/env python3
"""
repartition_sweep_bp.py

Replace `max_cluster_size = 50` with a DIVERSITY criterion, and show what each
threshold would cost.

The current partition caps cluster SIZE, which is why 29 clusters sit at
exactly 50 and 79% of multi-genome clusters exceed the diversity ceiling
Gubbins actually needs (Appendix A.1, A.3d). The principled alternative is to
subdivide until within-cluster diversity falls inside the recombination
detector's useful range -- Chewapreecha's stated rule, which she could not
publish a number for because Gubbins has never published one.

GAP2 §2 derives that number: cap mean pairwise core-SNP distance at ~1,000 for
>=20x contrast against a 0.5% divergent donor. Seng's three lineages, which
Gubbins handled, sat at 351/517/549.

This sweeps a Mash-distance threshold, clusters by single linkage (union-find),
and reports for each threshold: cluster count, size distribution, and -- the
part that matters -- how many resulting clusters fall inside the diversity cap.

CAVEAT, stated rather than hidden: single linkage CHAINS. Hennart 2022 showed
recombinant genomes bridging and fusing distinct groups under single linkage in
K. pneumoniae, and this organism has r/m 7.2. So the max within-cluster
diversity is reported alongside the mean; if max >> threshold, chaining is
happening and average linkage or PopPUNK's network model is required instead.
This sweep is a costing exercise, not a final partition.

Stdlib only.
"""

import argparse
import csv
import sys
from collections import defaultdict

from cluster_diversity_bp import read_phylip

CORE_ALN = 3_805_619
DERIVED_CAP_SNPS = 1000
SENG_MAX_SNPS = 549


class UF:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phylip", required=True)
    ap.add_argument("--core-len", type=int, default=CORE_ALN)
    ap.add_argument("--thresholds", default=None,
                    help="comma-separated Mash distances; default is a sweep "
                         "bracketing the ~1,000-SNP cap")
    ap.add_argument("--out", default="repartition_sweep.tsv")
    a = ap.parse_args()

    names, rows, idx = read_phylip(a.phylip)
    n = len(names)
    print("taxa: %d" % n)

    # collect all pairs once
    pairs = []
    for i in range(n):
        ri = rows[i]
        for j in range(len(ri)):
            if j < i:
                pairs.append((ri[j], i, j))
    pairs.sort()
    print("pairwise distances: %d" % len(pairs))

    if a.thresholds:
        ths = [float(x) for x in a.thresholds.split(",")]
    else:
        cap = DERIVED_CAP_SNPS / a.core_len          # ~0.000263
        ths = [cap * m for m in (0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0)]

    print("\n%-11s %9s %7s %7s %7s %8s %9s %9s %9s"
          % ("mash_thr", "~SNP_thr", "clust", "single", "largest",
             "median", "mean_div", "max_div", "in_cap"))
    print("-" * 88)

    out = []
    for t in ths:
        uf = UF(n)
        for d, i, j in pairs:
            if d > t:
                break
            uf.union(i, j)
        groups = defaultdict(list)
        for k in range(n):
            groups[uf.find(k)].append(k)
        sizes = sorted((len(v) for v in groups.values()), reverse=True)
        singles = sum(1 for s in sizes if s == 1)

        # within-cluster diversity of the resulting partition
        means, maxes, in_cap = [], [], 0
        for g in groups.values():
            if len(g) < 2:
                continue
            ds = []
            for x in range(len(g)):
                for y in range(x + 1, len(g)):
                    i, j = g[x], g[y]
                    if j < len(rows[i]):
                        ds.append(rows[i][j])
                    elif i < len(rows[j]):
                        ds.append(rows[j][i])
            if not ds:
                continue
            m = sum(ds) / len(ds)
            means.append(m)
            maxes.append(max(ds))
            if m * a.core_len <= DERIVED_CAP_SNPS:
                in_cap += 1
        multi = len(means)
        med = sorted(sizes)[len(sizes) // 2] if sizes else 0
        mean_div = (sum(means) / len(means) * a.core_len) if means else 0
        max_div = (max(maxes) * a.core_len) if maxes else 0
        print("%-11.6f %9.0f %7d %7d %7d %8d %9.0f %9.0f %6d/%d"
              % (t, t * a.core_len, len(sizes), singles, sizes[0], med,
                 mean_div, max_div, in_cap, multi))
        out.append((t, t * a.core_len, len(sizes), singles, sizes[0], med,
                    mean_div, max_div, in_cap, multi))

    with open(a.out, "w") as fh:
        fh.write("mash_threshold\tapprox_snp_threshold\tn_clusters\t"
                 "n_singletons\tlargest\tmedian_size\tmean_within_snps\t"
                 "max_within_snps\tclusters_in_cap\tmulti_clusters\n")
        for r in out:
            fh.write("\t".join(str(x) for x in r) + "\n")
    print("\nWrote %s" % a.out)
    print("\nRead 'max_div' as the chaining check: if it greatly exceeds the")
    print("threshold, single linkage is fusing groups through recombinant")
    print("bridges (Hennart 2022) and a network/average-linkage method is")
    print("needed. This sweep costs the criterion; it does not fix linkage.")


if __name__ == "__main__":
    sys.exit(main())
