#!/usr/bin/env python3
"""Sweep the Mash clustering threshold to find a FOUND partition, not an imposed one.

WHY. The full workflow run at the bp profile's `mash_threshold = 0.028` produced
**one connected component containing all 2,802 genomes**, which was then chopped
into 60 parts to satisfy `max_cluster_size = 50`. Diagnostics: Gini 0.059,
max/min 2.78, sizes pinned at the 50 cap. REVISED_STRATEGY Phase 0 item 3 says
Gini near 0 with max/min near 1 means the partition was IMPOSED; reference points
are Chewapreecha (found) Gini 0.456 / max-min 34.2, and Wu's deliberately imposed
ten-way cut Gini 0.095 / max-min 2.0. At 0.059 this run sat BELOW the known
imposed cut. Its clusters are arbitrary slices of one blob.

The bp profile's own comment anticipated this: "Captures geographic clades rather
than fine-scale outbreak clusters; tune tighter (0.005-0.007) when fine-scale
relatedness is the question. ALWAYS VALIDATE WITH A SWEEP ON THE ACTUAL DATASET
BEFORE COMMITTING TO A THRESHOLD." That sweep was never run. This is it.

WHAT IS MEASURED. For each candidate threshold, connected components of the graph
where an edge joins two genomes with Mash distance <= t. Reported per threshold:

  n_comp        number of components (candidate clusters, BEFORE any size cap)
  largest       size of the biggest -- if this is ~2802 the threshold is too loose
  singletons    components of size 1 -- if most genomes are singletons, too tight
  gini/maxmin   shape diagnostics, per Phase 0 item 3
  over_cap      components larger than max_cluster_size, i.e. how much of the
                partition would have to be IMPOSED by splitting
  n_usable      components with n >= MIN_UNIT, the ones actually analysable

GOAL: the loosest threshold at which the partition is FOUND rather than imposed --
high Gini, few components over the cap, and a usable number of analysable units.
This is a diagnostic to inform a judgement, not an automatic selection rule.
"""

import argparse
import statistics
import sys

MAX_CLUSTER_SIZE = 50   # matches the bp profile
MIN_UNIT = 6            # smallest cluster the project ever analysed


def load_matrix(path):
    """Read the pipeline's mash_distances_matrix.tsv -> (names, rows of floats)."""
    names, rows = [], []
    with open(path) as fh:
        header = fh.readline().rstrip("\n").split("\t")
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if len(p) < 2:
                continue
            names.append(p[0])
            rows.append([float(x) if x else 0.0 for x in p[1:]])
    return names, rows


def components(names, rows, t):
    """Connected components of the <=t graph, via union-find."""
    n = len(names)
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for i in range(n):
        ri = rows[i]
        # matrix is symmetric; only scan the upper triangle
        for j in range(i + 1, n):
            if ri[j] <= t:
                union(i, j)
    sizes = {}
    for i in range(n):
        sizes[find(i)] = sizes.get(find(i), 0) + 1
    return sorted(sizes.values(), reverse=True)


def gini(xs):
    n = len(xs)
    if n < 2:
        return 0.0
    mu = sum(xs) / n
    if mu == 0:
        return 0.0
    s = sum(abs(a - b) for a in xs for b in xs)
    return s / (2 * n * n * mu)


def report(matrix, thresholds):
    names, rows = load_matrix(matrix)
    print("=" * 104)
    print("MASH THRESHOLD SWEEP -- %d genomes" % len(names))
    print("=" * 104)
    print("\nPhase 0 item 3: Gini near 0 + max/min near 1 => IMPOSED partition.")
    print("Reference: Chewapreecha (found) gini 0.456 max/min 34.2 | "
          "Wu imposed 10-way cut gini 0.095 max/min 2.0\n")
    print("%9s %7s %8s %8s %11s %7s %8s %9s %9s"
          % ("threshold", "n_comp", "largest", "median", "singletons",
             "gini", "max/min", "over_cap", "n_usable"))
    print("-" * 104)
    for t in thresholds:
        s = components(names, rows, t)
        n_comp = len(s)
        largest = s[0]
        med = statistics.median(s)
        singles = sum(1 for x in s if x == 1)
        nz = [x for x in s if x > 0]
        mm = (s[0] / s[-1]) if s[-1] else float("inf")
        over = sum(1 for x in s if x > MAX_CLUSTER_SIZE)
        usable = sum(1 for x in s if x >= MIN_UNIT)
        flag = ""
        if largest > 0.5 * len(names):
            flag = "  <-- one blob, TOO LOOSE"
        elif singles > 0.7 * n_comp:
            flag = "  <-- mostly singletons, TOO TIGHT"
        print("%9.4f %7d %8d %8.0f %11d %7.3f %8.2f %9d %9d%s"
              % (t, n_comp, largest, med, singles, gini(s), mm, over, usable, flag))
    print("\nREADING")
    print("  Pick the LOOSEST threshold whose partition is found rather than")
    print("  imposed: gini well above 0.095, few components over the %d cap, and"
          % MAX_CLUSTER_SIZE)
    print("  enough components with n >= %d to be worth analysing." % MIN_UNIT)
    print("  over_cap counts components that would still be arbitrarily split.")
    return 0


def selftest():
    fails = []

    def chk(d, got, want):
        ok = got == want
        print("%-52s %s" % (d, "ok" if ok else "FAIL got=%r want=%r" % (got, want)))
        if not ok:
            fails.append(d)

    # two tight pairs, far apart -> two components of 2 at a tight threshold,
    # one component of 4 at a loose one. Guards the union-find and the symmetry
    # assumption in one shot.
    names = ["a", "b", "c", "d"]
    rows = [[0.0, 0.001, 0.5, 0.5],
            [0.001, 0.0, 0.5, 0.5],
            [0.5, 0.5, 0.0, 0.001],
            [0.5, 0.5, 0.001, 0.0]]
    chk("tight threshold splits into 2+2", components(names, rows, 0.01), [2, 2])
    chk("loose threshold merges to one", components(names, rows, 0.6), [4])
    chk("below-all threshold gives singletons",
        components(names, rows, 0.0001), [1, 1, 1, 1])
    chk("gini of equal sizes is 0", round(gini([50, 50, 50]), 6), 0.0)
    chk("gini of skewed is >0", gini([100, 1, 1]) > 0.4, True)
    print("\n%d test(s) failed" % len(fails) if fails else "\nall tests passed")
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--matrix", default="mash_matrix_2802.tsv")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--thresholds",
                    default="0.0005,0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.010,0.015,0.028")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    ts = [float(x) for x in a.thresholds.split(",")]
    return report(a.matrix, ts)


if __name__ == "__main__":
    sys.exit(main())
