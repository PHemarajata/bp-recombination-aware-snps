#!/usr/bin/env python3
"""
cgMLST vs recombination-filtered SNP concordance, on the FROZEN BASIS.

The filed CGMLST_CONCORDANCE.tsv (median +0.846) has two problems:

  1. It was built by globbing DISTANCES_v4c/, which follows the hybrid
     L1v4c_out/Clusters -- 88 unit files, including strain_1_L1_36 /
     strain_1_L1_37 (A100-only) and strain_1_L1_10 (dropped from the basis).
  2. Within units, it uses whatever taxa the distance file holds, which for
     strain_1_L1_8, strain_14_L1_4 and strain_1_L1_26 still includes the
     duplicate BioSamples and the register-excluded SRR2896257.

It also runs on the OLD PubMLST scheme by default (cgmlst_results/,
4,089 loci), not the published Lichtenegger scheme the project now uses.

This recomputes it restricted to FINAL_BASIS_2026-08-22 -- 85 units, and within
each unit only frozen members -- and reports BOTH schemes, so the figure is
unambiguous about which one it belongs to and the scheme swap is visible.

Method is otherwise identical to cgmlst_analysis_bp.py: chr1 filtered per-taxon
SNP distances vs normalised cgMLST allelic distance over loci called in both
genomes, Pearson r per unit, median across units.
"""
import argparse
import csv
import glob
import os

import numpy as np

B = os.path.dirname(os.path.abspath(__file__))
# reuse the validated loaders rather than reimplementing them
exec(open(f"{B}/cgmlst_analysis_bp.py").read().split("def main()")[0])


def frozen_members():
    m = {}
    for r in csv.DictReader(open(f"{B}/FINAL_BASIS_2026-08-22/FINAL_PARTITION.tsv"),
                            delimiter="\t"):
        m.setdefault(r["unit"], set()).add(r["sample_id"])
    return m


def concordance(profiles, members, label):
    samples, loci, mat = load_profiles(profiles)
    idx_of = {s: i for i, s in enumerate(samples)}
    rows, skipped = [], []
    for f in sorted(glob.glob(f"{B}/DISTANCES_v4c/*_1.filtered_pertaxon.tsv")):
        unit = os.path.basename(f).split("__")[0]
        if unit not in members:
            skipped.append(unit)
            continue
        keep = members[unit]
        r = list(csv.reader(open(f), delimiter="\t"))
        hdr = r[0][1:]
        pos = {t: k for k, t in enumerate(hdr)}
        taxa = [t for t in hdr if t in idx_of and t in keep]
        if len(taxa) < 5:
            continue
        snp, cg = [], []
        for x in range(len(taxa)):
            i = idx_of[taxa[x]]
            others = [idx_of[t] for t in taxa[x + 1:]]
            if not others:
                continue
            d, n = dist_one_vs_all(mat, i, others)
            for y, t in enumerate(taxa[x + 1:]):
                if np.isnan(d[y]):
                    continue
                snp.append(int(r[pos[taxa[x]] + 1][pos[t] + 1]))
                cg.append(d[y])
        if len(snp) < 10:
            continue
        c = np.corrcoef(snp, cg)[0, 1]
        rows.append((unit, len(taxa), len(snp), c))
    good = [x for x in rows if not np.isnan(x[3])]
    cs = [x[3] for x in good]
    print(f"\n=== {label} ===")
    print(f"  units on the frozen basis with a concordance: {len(good)}")
    print(f"  unit files skipped as off-basis: {sorted(skipped)}")
    print(f"  median Pearson r  {np.median(cs):+.4f}")
    print(f"  range             {min(cs):+.4f} to {max(cs):+.4f}")
    print(f"  units r >= 0.7    {sum(1 for c in cs if c >= 0.7)} of {len(cs)}")
    return rows, float(np.median(cs))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=f"{B}/CGMLST_CONCORDANCE_FROZEN.tsv")
    a = ap.parse_args()
    mem = frozen_members()
    print(f"frozen basis: {len(mem)} units, {sum(len(v) for v in mem.values())} genomes")

    out = []
    for label, prof in (("Lichtenegger v1.1 (4,221 loci) -- the scheme now used",
                         f"{B}/cgmlst_lichtenegger/results/results_alleles.tsv"),
                        ("PubMLST scheme 2 (4,089 loci) -- what the filed +0.846 used",
                         f"{B}/cgmlst_results/results_alleles.tsv")):
        if not os.path.exists(prof):
            print(f"\n=== {label} ===\n  profiles absent: {prof}")
            continue
        rows, med = concordance(prof, mem, label)
        out.append((label.split(" --")[0], rows, med))

    if len(out) == 2:
        a_, b_ = out
        da = {u: c for u, n, p, c in a_[1]}
        db = {u: c for u, n, p, c in b_[1]}
        both = sorted(set(da) & set(db))
        d = [da[u] - db[u] for u in both if not (np.isnan(da[u]) or np.isnan(db[u]))]
        print(f"\n=== scheme agreement on the frozen basis ===")
        print(f"  units in both: {len(both)}   median difference "
              f"(Lichtenegger - PubMLST): {np.median(d):+.4f}")

    with open(a.out, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["scheme", "unit", "n_taxa", "n_pairs",
                    "pearson_r_cgmlst_vs_filtered_snp"])
        for label, rows, _ in out:
            for u, n, p, c in sorted(rows, key=lambda t: t[0]):
                w.writerow([label, u, n, p,
                            f"{c:.4f}" if not np.isnan(c) else ""])
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
