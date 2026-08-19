#!/usr/bin/env python3
"""
cluster_diversity_bp.py

GAP1 sec 11 "Step 0": read within-cluster diversity off the Mash distance
matrix that already exists. No new compute.

Answers the question the size cap makes urgent: how many of the current
clusters are actually low-diversity partitions of the kind Gubbins needs, and
how many are diffuse fragments that only LOOK like clusters because they were
cut at 50 genomes?

Reference points, all established elsewhere in this project:
  * Seng's three B. pseudomallei lineages, which Gubbins handled successfully,
    had mean pairwise core-SNP distances of 351, 517, 549.
  * The derived Gubbins-contrast rule (GAP2 sec 2) caps mean pairwise core SNPs
    at ~1,000 for >=20x contrast against a 0.5% divergent donor.
  * Measured here: cluster_53 = 1,435 post-Gubbins SNPs (tight, behaves),
    cluster_0 = 16,197 (diffuse).
  * SKA2 landmarks: <0.005 divergence = strain regime (~90% recall);
    >0.01 = too coarse for split-kmer work.

Mash distance approximates 1 - ANI, i.e. per-site divergence, so
   approx pairwise SNPs = mash_distance * core_alignment_length.
Wu's core alignment (3,805,619 bp) is the denominator used, and that is an
approximation the output labels as such.

Stdlib only.
"""

import argparse
import csv
import sys
from collections import defaultdict

CORE_ALN = 3_805_619          # Wu et al. 2026 core alignment, 52.5% of K96243
SENG_MAX = 549                # largest Seng lineage mean pairwise core SNPs
DERIVED_CAP = 1000            # GAP2 sec 2 derived ceiling
SKA_STRAIN = 0.005            # SKA2 strain-regime boundary
SKA_COARSE = 0.010            # above this, too coarse for split-kmers


def read_phylip(path, wanted=None):
    """Lower/full-triangle PHYLIP distance matrix -> {(a,b): d}. Returns
    (names, dist). Only pairs among `wanted` are retained if given."""
    with open(path) as fh:
        first = fh.readline().split()
        n = int(first[0])
        names = []
        rows = []
        for line in fh:
            parts = line.split()
            if not parts:
                continue
            names.append(parts[0])
            rows.append([float(x) for x in parts[1:]])
            if len(names) == n:
                break
    # The matrix carries filenames (GCA_x_1.fasta); membership carries bare
    # sample ids. Index under every plausible spelling so the join does not
    # silently drop every taxon.
    idx = {}
    for i, nm in enumerate(names):
        for v in {nm,
                  nm.rsplit(".", 1)[0] if "." in nm else nm,
                  nm.replace(".fasta", "").replace(".fa", "").replace(".fna", "")}:
            idx.setdefault(v, i)
    return names, rows, idx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phylip", required=True)
    ap.add_argument("--membership", required=True)
    ap.add_argument("--id-col", default="sample_id")
    ap.add_argument("--cluster-col", default="cluster_id")
    ap.add_argument("--core-len", type=int, default=CORE_ALN)
    ap.add_argument("--out", default="cluster_diversity.tsv")
    a = ap.parse_args()

    names, rows, idx = read_phylip(a.phylip)
    print("distance matrix: %d taxa" % len(names))

    with open(a.membership, newline="") as fh:
        head = fh.readline()
        fh.seek(0)
        d = "\t" if "\t" in head else ","
        mem = list(csv.DictReader(fh, delimiter=d))
    clusters = defaultdict(list)
    for r in mem:
        cid = (r.get(a.cluster_col) or "").strip()
        sid = (r.get(a.id_col) or "").strip()
        if cid and sid:
            clusters[cid].append(sid)

    def dist(i, j):
        if i == j:
            return 0.0
        # lower-triangle safe access
        if j < len(rows[i]):
            return rows[i][j]
        if i < len(rows[j]):
            return rows[j][i]
        return None

    out = []
    unresolved = 0
    for cid, sids in clusters.items():
        ii = [idx[s] for s in sids if s in idx]
        unresolved += len(sids) - len(ii)
        if len(ii) < 2:
            out.append((cid, len(sids), None, None, None, None))
            continue
        ds = []
        for x in range(len(ii)):
            for y in range(x + 1, len(ii)):
                v = dist(ii[x], ii[y])
                if v is not None:
                    ds.append(v)
        if not ds:
            out.append((cid, len(sids), None, None, None, None))
            continue
        mean_d = sum(ds) / len(ds)
        max_d = max(ds)
        out.append((cid, len(sids), mean_d, max_d,
                    mean_d * a.core_len, max_d * a.core_len))

    out.sort(key=lambda t: -(t[4] or -1))

    print("\n%-14s %5s %10s %10s %12s %12s"
          % ("cluster", "n", "mean_mash", "max_mash", "~mean_SNPs", "~max_SNPs"))
    print("-" * 70)
    for cid, n, md, xd, ms, xs in out[:18]:
        if md is None:
            print("%-14s %5d %10s %10s %12s %12s"
                  % (cid, n, "-", "-", "-", "-"))
        else:
            print("%-14s %5d %10.5f %10.5f %12.0f %12.0f"
                  % (cid, n, md, xd, ms, xs))

    scored = [t for t in out if t[4] is not None]
    multi = [t for t in scored if t[1] > 1]
    over_cap = [t for t in multi if t[4] > DERIVED_CAP]
    over_seng = [t for t in multi if t[4] > SENG_MAX]
    over_ska = [t for t in multi if t[3] > SKA_COARSE]
    in_strain = [t for t in multi if t[3] <= SKA_STRAIN]

    gen_total = sum(t[1] for t in multi)
    gen_over = sum(t[1] for t in over_cap)

    print("\n" + "=" * 70)
    print("HOW MANY CLUSTERS ARE ACTUALLY LOW-DIVERSITY?")
    print("=" * 70)
    print("multi-genome clusters scored          : %d" % len(multi))
    print("  above the derived ~%d-SNP cap      : %d  (%.1f%% of clusters,"
          " %.1f%% of their genomes)"
          % (DERIVED_CAP, len(over_cap),
             100.0 * len(over_cap) / max(len(multi), 1),
             100.0 * gen_over / max(gen_total, 1)))
    print("  above Seng's largest lineage (%d)   : %d" % (SENG_MAX, len(over_seng)))
    print("  max Mash > %.3f (too coarse for SKA) : %d"
          % (SKA_COARSE, len(over_ska)))
    print("  max Mash <= %.3f (SKA strain regime) : %d"
          % (SKA_STRAIN, len(in_strain)))
    if unresolved:
        print("\n%d cluster members were absent from the distance matrix"
              % unresolved)
    print("\nNOTE: SNP counts are Mash distance x %s bp and are APPROXIMATE."
          % format(a.core_len, ","))
    print("They index diversity for triage; they are not core-SNP distances.")

    with open(a.out, "w") as fh:
        fh.write("cluster_id\tn\tmean_mash\tmax_mash\tapprox_mean_snps\t"
                 "approx_max_snps\tover_derived_cap\n")
        for cid, n, md, xd, ms, xs in out:
            fh.write("%s\t%d\t%s\t%s\t%s\t%s\t%s\n"
                     % (cid, n,
                        "" if md is None else "%.6f" % md,
                        "" if xd is None else "%.6f" % xd,
                        "" if ms is None else "%.0f" % ms,
                        "" if xs is None else "%.0f" % xs,
                        "" if ms is None else ("yes" if ms > DERIVED_CAP else "no")))
    print("\nWrote %s" % a.out)


if __name__ == "__main__":
    sys.exit(main())
