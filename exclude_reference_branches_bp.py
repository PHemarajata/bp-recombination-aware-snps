#!/usr/bin/env python3
"""
exclude_reference_branches_bp.py

Recompute pooled r/m with the external Reference taxon's branches excluded.

THE PROBLEM. The pipeline keeps the mapping reference as a taxon in the Gubbins
input (deliberately -- it keeps the alignment full-length and the invariant-site
counts honest). But Gubbins then reconstructs substitutions along the branch
leading to that reference, and because the reference sits OUTSIDE the population
by construction, that branch is enormous. Measured on strain_18_L1_1:

    (Reference:3859.7,( ...7 real genomes... )Node_6:3774.9)Node_7:0.0

every real genome sits on a branch of 4-52; the reference's is 3,860. Those
substitutions are divergence between the population and an outgroup, not
evolution within the population, and Gubbins scores nearly all of them as
"outside recombination" because they are spread genome-wide rather than
clustered. They land in r/m's denominator and crush the ratio:

    strain_18_L1_1  including reference branches  r/m = 0.42
                    excluding them                r/m = 8.73
                    manual analysis (7 taxa)      r/m = 9.14

The effect scales with reference distance because the branch length IS the
reference distance -- which is why it masqueraded as a caller x distance
interaction when this run was first compared against the manual analysis.

WHICH BRANCHES. Gubbins emits an unrooted tree written with an arbitrary root.
When the reference is the outgroup, its divergence is SPLIT between the
Reference leaf and the sibling clade at the root -- above, 3859.7 and 3774.9,
two halves of one quantity. Excluding only the leaf would leave half the
inflation behind, so both children of the root are dropped whenever one of them
is the Reference leaf.

If Reference is NOT at the root (it should be, but the tree is data), only its
own branch is dropped and the unit is flagged, because that is a topology worth
looking at rather than silently handling.
"""

import argparse
import collections
import csv
import glob
import os
import re
import sys


def root_children(newick):
    """
    Labels of the two (or more) children of the root.

    Walks the top-level comma split of the outermost parenthesis pair, taking
    each child's trailing label -- a leaf name, or the Node_N label a clade
    carries after its closing bracket.
    """
    s = newick.strip().rstrip(";").strip()
    if not s.startswith("("):
        return []
    # strip the outermost parens
    depth = 0
    for i, ch in enumerate(s):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                inner = s[1:i]
                break
    else:
        return []
    parts, depth, cur = [], 0, []
    for ch in inner:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(cur)); cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))

    labels = []
    for p in parts:
        p = p.strip()
        tail = p[p.rfind(")") + 1:] if ")" in p else p
        lab = tail.split(":")[0].strip()
        if lab:
            labels.append(lab)
    return labels


def branches_to_drop(tree_path, ref_name="Reference"):
    """(labels_to_drop, note)"""
    try:
        newick = open(tree_path).read()
    except OSError:
        return set(), "no tree"
    if ref_name not in newick:
        return set(), "no Reference taxon in tree"
    kids = root_children(newick)
    if ref_name in kids:
        return set(kids), "reference at root; dropped both root children"
    return {ref_name}, "REFERENCE NOT AT ROOT -- only its own branch dropped"


def pooled(path, drop):
    inside = outside = 0.0
    dropped_in = dropped_out = 0.0
    with open(path) as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            try:
                i = float(row["Number of SNPs Inside Recombinations"])
                o = float(row["Number of SNPs Outside Recombinations"])
            except (KeyError, ValueError):
                continue
            if row["Node"] in drop:
                dropped_in += i; dropped_out += o
            else:
                inside += i; outside += o
    return inside, outside, dropped_in, dropped_out


def main():
    # No defaults on the four inputs. Every one of them previously pointed at
    # the v1 "L1" run, so running this against a later partition while forgetting
    # any single flag silently mixed two partitions and produced a plausible
    # r/m table. That failure has happened once in this project, on the sibling
    # phylogeography script, and was caught only because someone noticed a unit
    # count. The inputs must now be named.
    ap = argparse.ArgumentParser(
        description="Recompute pooled r/m with external reference branches "
                    "excluded. All inputs must name the SAME run.")
    ap.add_argument("--stats-dir", required=True,
                    help="directory of *.per_branch_statistics.csv for this run")
    ap.add_argument("--clusters-out", required=True,
                    help="that run's Clusters/ directory")
    ap.add_argument("--clusters", required=True,
                    help="TSV of cluster membership for this run")
    ap.add_argument("--audit", required=True,
                    help="per-cluster reference audit TSV for this run")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    for label, path in (("--stats-dir", a.stats_dir),
                        ("--clusters-out", a.clusters_out),
                        ("--clusters", a.clusters),
                        ("--audit", a.audit)):
        if not os.path.exists(path):
            print(f"ABORT: {label} does not exist: {path}", file=sys.stderr)
            sys.exit(2)

    sizes = collections.Counter()
    with open(a.clusters) as fh:
        r = csv.reader(fh, delimiter="\t"); next(r)
        for row in r:
            sizes[row[0]] += 1
    ref = {}
    for row in csv.DictReader(open(a.audit), delimiter="\t"):
        ref[row["cluster_id"]] = (row["reference"], row["source"], row["mean_mash"])

    per = collections.defaultdict(dict)
    notes = {}
    for path in sorted(glob.glob(os.path.join(a.stats_dir, "*.per_branch_statistics.csv"))):
        base = os.path.basename(path).replace(".per_branch_statistics.csv", "")
        m = re.match(r"^(.*?)__(.*)_(\d+)$", base)
        if not m:
            continue
        unit, _, rep = m.groups()
        tre = os.path.join(a.clusters_out, f"cluster_{base}", "Gubbins",
                           f"{base}.node_labelled.final_tree.tre")
        drop, note = branches_to_drop(tre)
        notes.setdefault(unit, []).append(note)
        per[unit][int(rep)] = pooled(path, drop) + (sorted(drop),)

    rows, flagged = [], []
    for unit in sorted(per, key=lambda u: (int(u.split("_")[1]), int(u.split("_L1_")[1]))):
        reps = per[unit]
        i = sum(v[0] for v in reps.values()); o = sum(v[1] for v in reps.values())
        di = sum(v[2] for v in reps.values()); do = sum(v[3] for v in reps.values())
        rname, rsrc, rmash = ref.get(unit, ("", "", ""))
        if any("NOT AT ROOT" in n for n in notes[unit]):
            flagged.append(unit)
        rows.append({
            "unit": unit, "n": sizes.get(unit, ""),
            "rm_corrected": f"{i/o:.4f}" if o else "NA",
            "rm_uncorrected": f"{(i+di)/(o+do):.4f}" if (o + do) else "NA",
            "snps_in_recomb": int(i), "snps_outside": int(o),
            "ref_branch_snps_outside": int(do), "ref_branch_snps_inside": int(di),
            "dropped_branches": ";".join(sorted({b for v in reps.values() for b in v[4]})),
            "reference": rname, "ref_source": rsrc, "ref_mean_mash": rmash,
            "note": "; ".join(sorted(set(notes[unit]))),
        })

    cols = ["unit", "n", "rm_corrected", "rm_uncorrected", "snps_in_recomb",
            "snps_outside", "ref_branch_snps_outside", "ref_branch_snps_inside",
            "dropped_branches", "reference", "ref_source", "ref_mean_mash", "note"]
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow(row)

    vals = sorted(float(r["rm_corrected"]) for r in rows if r["rm_corrected"] != "NA")
    print(f"units: {len(rows)}")
    print(f"  corrected r/m  median {vals[len(vals)//2]:.2f}   range {vals[0]:.2f}-{vals[-1]:.2f}")
    unc = sorted(float(r["rm_uncorrected"]) for r in rows if r["rm_uncorrected"] != "NA")
    print(f"  uncorrected    median {unc[len(unc)//2]:.2f}   range {unc[0]:.2f}-{unc[-1]:.2f}")
    tot_out = sum(r["snps_outside"] + r["ref_branch_snps_outside"] for r in rows)
    ref_out = sum(r["ref_branch_snps_outside"] for r in rows)
    print(f"  SNPs outside recombination attributable to reference branches: "
          f"{ref_out} of {tot_out} ({100.0*ref_out/tot_out:.1f}%)")
    if flagged:
        print(f"  FLAGGED (Reference not at root): {len(flagged)} -> {flagged[:5]}")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
