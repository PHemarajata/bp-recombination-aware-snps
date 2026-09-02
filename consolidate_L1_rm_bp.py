#!/usr/bin/env python3
"""
consolidate_L1_rm_bp.py

Pool r/m per analysis unit from the archived Gubbins per-branch statistics.

POOLED, NOT AVERAGED, and the distinction is the whole point. Gubbins reports a
per-branch r/m; the per-branch value is undefined where a branch has zero SNPs
outside recombination, and it is wildly noisy on short branches carrying a
handful of SNPs. Averaging those per-branch ratios lets the shortest, least
informative branches dominate. The pooled estimate

    r/m = sum(SNPs inside recombinations) / sum(SNPs outside recombinations)

weights every branch by how much evidence it actually carries, which is what the
manual analysis reported and what these numbers must stay comparable to.

Branches with zero SNPs outside recombination are counted and reported rather
than silently dropped: if many branches are in that state the pooled ratio is
resting on very little clonal signal, and that is worth seeing.

Both replicons are reported separately AND combined. They are not independent
replicates -- they are two parts of one genome sharing one genealogy -- so the
combined value is the estimate and the per-replicon pair is a consistency check.
Session 3 saw two replicons agree to 4 significant figures on a unit whose
partition was wrong: concordance between replicons shows the estimate is
PRECISE, never that it is VALID.
"""

import argparse
import collections
import csv
import glob
import os
import re
import sys


def read_branches(path):
    """(inside, outside, blocks, n_branches, n_zero_outside) for one replicon."""
    inside = outside = blocks = 0
    n = zero_out = 0
    with open(path) as fh:
        r = csv.DictReader(fh, delimiter="\t")
        for row in r:
            try:
                i = float(row["Number of SNPs Inside Recombinations"])
                o = float(row["Number of SNPs Outside Recombinations"])
                b = float(row["Number of Recombination Blocks"])
            except (KeyError, ValueError):
                continue
            inside += i
            outside += o
            blocks += b
            n += 1
            if o == 0:
                zero_out += 1
    return inside, outside, blocks, n, zero_out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats-dir", default="RUN_STATS_ARCHIVE/L1")
    # DANGEROUS DEFAULT REMOVED: named a specific v1-era run artifact.
    ap.add_argument("--clusters", required=True)
    ap.add_argument("--audit", default="curated_L1_reference_audit.tsv")
    ap.add_argument("--out", default="RM_RESULTS_L1.tsv")
    a = ap.parse_args()

    sizes = collections.Counter()
    with open(a.clusters) as fh:
        r = csv.reader(fh, delimiter="\t")
        next(r)
        for row in r:
            sizes[row[0]] += 1

    ref = {}
    if os.path.exists(a.audit):
        for row in csv.DictReader(open(a.audit), delimiter="\t"):
            ref[row["cluster_id"]] = (row["reference"], row["source"],
                                      row["mean_mash"])

    per_unit = collections.defaultdict(dict)
    for path in sorted(glob.glob(os.path.join(a.stats_dir,
                                              "*.per_branch_statistics.csv"))):
        base = os.path.basename(path).replace(".per_branch_statistics.csv", "")
        m = re.match(r"^(.*?)__(.*)_(\d+)$", base)
        if not m:
            print(f"  cannot parse unit from {base}", file=sys.stderr)
            continue
        unit, _, rep = m.groups()
        per_unit[unit][int(rep)] = read_branches(path)

    rows = []
    for unit in sorted(per_unit, key=lambda u: (int(u.split("_")[1]),
                                                int(u.split("_L1_")[1]))):
        reps = per_unit[unit]
        tot_i = sum(v[0] for v in reps.values())
        tot_o = sum(v[1] for v in reps.values())
        combined = (tot_i / tot_o) if tot_o else float("nan")
        rname, rsrc, rmash = ref.get(unit, ("", "", ""))
        row = {
            "unit": unit,
            "n": sizes.get(unit, ""),
            "n_replicons": len(reps),
            "rm_pooled": f"{combined:.4f}" if tot_o else "NA",
            "snps_in_recomb": int(tot_i),
            "snps_outside": int(tot_o),
            "recomb_blocks": int(sum(v[2] for v in reps.values())),
            "n_branches": sum(v[3] for v in reps.values()),
            "branches_zero_outside": sum(v[4] for v in reps.values()),
            "reference": rname, "ref_source": rsrc, "ref_mean_mash": rmash,
        }
        for rep in sorted(reps):
            i, o, _, _, _ = reps[rep]
            row[f"rm_replicon{rep}"] = f"{i/o:.4f}" if o else "NA"
        rows.append(row)

    cols = ["unit", "n", "n_replicons", "rm_pooled", "rm_replicon1",
            "rm_replicon2", "snps_in_recomb", "snps_outside", "recomb_blocks",
            "n_branches", "branches_zero_outside", "reference", "ref_source",
            "ref_mean_mash"]
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                           lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)

    vals = sorted(float(r["rm_pooled"]) for r in rows if r["rm_pooled"] != "NA")
    print(f"units with a pooled r/m : {len(vals)} of {len(rows)}")
    if vals:
        print(f"  range                 : {vals[0]:.3f} - {vals[-1]:.3f}")
        print(f"  median                : {vals[len(vals)//2]:.3f}")
        q1, q3 = vals[len(vals)//4], vals[3*len(vals)//4]
        print(f"  IQR                   : {q1:.3f} - {q3:.3f}")
    part = sum(1 for r in rows if r["n_replicons"] != 2)
    if part:
        print(f"  units missing a replicon: {part}")
    zb = sum(r["branches_zero_outside"] for r in rows)
    tb = sum(r["n_branches"] for r in rows)
    print(f"  branches with zero SNPs outside recombination: {zb} of {tb} "
          f"({100.0*zb/tb:.1f}%)")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
