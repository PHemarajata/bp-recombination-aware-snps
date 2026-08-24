#!/usr/bin/env python3
"""Does BioProject structure the tree WITHIN a single country?

WHY THIS TEST EXISTS
--------------------
R6's BioProject control is a discriminant, not an adjustment: a unit is reported
only if geography clusters on the tree AND BioProject does not. At national
scale that rule discards 14 of the 26 units in which country signal is
detectable, as "confounded".

The rule is only valid if BioProject and country are separable. In this panel
they largely are not. 113 of 119 BioProjects (95%) are entirely single-country,
and among near-clonal pairs 48.4% share a BioProject while 48.0% share BOTH --
so ~99% of same-BioProject pairs are also same-country. A genuine within-country
clonal expansion deposited by one study therefore makes BOTH variables fire on
the SAME clade, and the unit is discarded as confounded when nothing artefactual
has been shown.

This script runs the conditional test that separates the two explanations.
Holding country FIXED, it asks whether BioProject still structures the tree:

  * significant  -> there IS batch structure independent of geography, and
                    "confounded" was the right verdict for that unit.
  * null         -> the unit's BioProject signal was country signal wearing a
                    different label. "Confounded" over-controlled, and the
                    verdict should be softened rather than treated as a null
                    geographic result.

METHOD
------
Identical statistic to `phylogeography_association_bp.py`, whose functions are
imported rather than reimplemented (same Fitch small-parsimony, same permutation
scheme, same BH FDR, same seed). The only difference is the label set and who is
permuted:

  * State = BioProject, assigned ONLY to tips of the country under test; every
    other tip is set to None. Fitch treats None as fully ambiguous and it never
    forces a change, so scoring the full topology with the rest masked is
    equivalent to scoring the induced subtree -- no pruning code, nothing to get
    wrong.
  * The permutation shuffles BioProject labels among the tested country's tips
    ONLY, so topology and label composition are both preserved and geography is
    held fixed by construction.

Guards, mirroring the vacuous-control rule that the R6 interpretation document
insists on: a (unit, country) cell is tested only with >= MIN_N genomes carrying
a BioProject and >= 2 distinct BioProjects among them.

  python3 bioproject_within_country_bp.py
  python3 bioproject_within_country_bp.py --perms 5000

Output: BIOPROJECT_WITHIN_COUNTRY_2026-08-24.tsv
"""
import argparse
import collections
import csv
import os
import random
import sys

B = os.path.dirname(os.path.abspath(__file__))

# Reuse the frozen implementation verbatim -- parse_newick, leaves, fitch_score,
# bh_qvalues, state_of_value, state_of_row. Same trick grouping_test_bp.py uses.
_src = open(f"{B}/phylogeography_association_bp.py").read().split("def main()")[0]
exec(_src)

MIN_N = 8


def tree_path(unit):
    """Replicon-1 Gubbins tree for exactly this unit.

    NEVER glob `<unit>__*`: L1v4c_out/Clusters is the hybrid 88-unit directory
    and `strain_1_L1_2__*` also matches `strain_1_L1_26__*`. Match the directory
    name exactly up to the `__` separator.
    """
    root = f"{B}/L1v4c_out/Clusters"
    pref = f"cluster_{unit}__"
    hits = []
    for d in os.listdir(root):
        if not d.startswith(pref) or not d.endswith("_1"):
            continue
        # the segment after `__` must be <ref>_1 with no further `__`
        if "__" in d[len(pref):]:
            continue
        t = f"{root}/{d}/Gubbins/{d[len('cluster_'):]}.node_labelled.final_tree.tre"
        if os.path.isfile(t):
            hits.append(t)
    if len(hits) != 1:
        return None
    return hits[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--perms", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=20260815)
    ap.add_argument("--fdr", type=float, default=0.05)
    ap.add_argument("--out",
                    default=f"{B}/BIOPROJECT_WITHIN_COUNTRY_2026-08-24.tsv")
    a = ap.parse_args()
    # A low --perms run must not silently overwrite the canonical output. This
    # bit me on 2026-08-24: `--perms 1`, run as a coverage sanity check, wrote
    # p-values of 1.0 over the real 1,000-permutation table under the same
    # default --out.
    if a.perms < 1000 and a.out == ap.get_default("out"):
        sys.exit(f"REFUSING to write the canonical output with only {a.perms} "
                 f"permutations. Pass --out to a scratch path for a quick run.")
    rng = random.Random(a.seed)

    meta = {r["sample_id"]: r for r in
            csv.DictReader(open(f"{B}/L1v4c_MERGED_METADATA.tsv"), delimiter="\t")}
    frozen = collections.defaultdict(set)
    for r in csv.DictReader(
            open(f"{B}/FINAL_BASIS_2026-08-22/FINAL_PARTITION.tsv"), delimiter="\t"):
        frozen[r["unit"]].add(r["sample_id"])

    # Classify units by their R6 national-scale verdicts.
    v = collections.defaultdict(dict)
    for r in csv.DictReader(
            open(f"{B}/PHYLOGEO_FROZEN_national_2026-08-23.tsv"), delimiter="\t"):
        v[r["unit"]][r["variable"]] = r
    groups = {}
    for u, d in v.items():
        c, bp = d.get("country"), d.get("bioproject")
        if not c or not bp:
            continue
        if c["verdict"] == "clustered" and bp["verdict"] == "clustered":
            groups[u] = "confounded"
        elif c["verdict"] == "clustered":
            groups[u] = "country_only"

    rows = []
    for unit, grp in sorted(groups.items()):
        t = tree_path(unit)
        if not t:
            print(f"  no unique replicon-1 tree for {unit}", file=sys.stderr)
            continue
        tree = parse_newick(open(t).read())
        tips = [x for x in leaves(tree)
                if x and x != "Reference" and x in frozen[unit]]
        if len(tips) < 4:
            continue

        bycountry = collections.defaultdict(list)
        for tip in tips:
            m = meta.get(tip, {})
            c = state_of_row(m, "country")
            bp = state_of_value(m.get("bioproject", ""))
            if c and bp:
                bycountry[c].append((tip, bp))

        for country, members in sorted(bycountry.items()):
            labs = [bp for _, bp in members]
            distinct = len(set(labs))
            row = {
                "unit": unit, "r6_group": grp, "country": country,
                "n_tips_unit": len(tips), "n_country_with_bioproject": len(members),
                "n_distinct_bioprojects": distinct,
                "top_bioproject_share": f"{collections.Counter(labs).most_common(1)[0][1]/len(labs):.3f}",
            }
            if len(members) < MIN_N or distinct < 2:
                row.update({"parsimony_score": "", "p_value": "",
                            "verdict": f"untestable: n<{MIN_N} or <2 BioProjects"})
                rows.append(row)
                continue

            names = [tip for tip, _ in members]
            # Everything outside this country is ambiguous -> contributes nothing.
            base = {tip: None for tip in tips}

            def score(assignment):
                st = dict(base)
                st.update(assignment)
                return fitch_score(tree, st)

            obs = score(dict(zip(names, labs)))
            pool = list(labs)
            hits = 0
            for _ in range(a.perms):
                rng.shuffle(pool)
                if score(dict(zip(names, pool))) <= obs:
                    hits += 1
            p = (hits + 1) / (a.perms + 1)
            row.update({
                "parsimony_score": obs,
                "p_value": f"{p:.4f}",
                "verdict": ("batch structure within country" if p <= 0.05
                            else "no batch structure within country"),
            })
            rows.append(row)

    # BH FDR across the tested cells, applied within each R6 group separately:
    # the confounded set is the primary analysis and the country-only set is its
    # comparison group, so they are not one family of tests.
    for grp in ("confounded", "country_only"):
        tested = [r for r in rows if r["r6_group"] == grp and r["p_value"]]
        if not tested:
            continue
        q = bh_qvalues([float(r["p_value"]) for r in tested])
        for r, qq in zip(tested, q):
            r["q_value"] = f"{qq:.4f}"
    for r in rows:
        r.setdefault("q_value", "")

    cols = ["unit", "r6_group", "country", "n_tips_unit",
            "n_country_with_bioproject", "n_distinct_bioprojects",
            "top_bioproject_share", "parsimony_score", "p_value", "q_value",
            "verdict"]
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    print(f"wrote {a.out}  ({len(rows)} rows, {a.perms} permutations, "
          f"seed {a.seed})\n")
    for grp, title in (("confounded", "CONFOUNDED units — R6 discarded these"),
                       ("country_only", "COUNTRY-ONLY units — R6 kept these (comparison)")):
        sub = [r for r in rows if r["r6_group"] == grp]
        tested = [r for r in sub if r["p_value"]]
        sig = [r for r in tested if float(r["p_value"]) <= 0.05]
        sigq = [r for r in tested if r["q_value"] and float(r["q_value"]) <= a.fdr]
        units = {r["unit"] for r in sub}
        tunits = {r["unit"] for r in tested}
        print(f"=== {title} ===")
        print(f"  units {len(units)}, of which testable {len(tunits)}")
        print(f"  (unit,country) cells: {len(sub)} total, {len(tested)} testable")
        print(f"  BioProject structures the tree WITHIN country: "
              f"{len(sig)}/{len(tested)} at p<=0.05, "
              f"{len(sigq)}/{len(tested)} after BH FDR {a.fdr}")
        if sig:
            print("   significant cells:")
            for r in sorted(sig, key=lambda x: float(x["p_value"])):
                print(f"     {r['unit']:22s} {r['country']:22s} "
                      f"n={r['n_country_with_bioproject']:>3} "
                      f"bp={r['n_distinct_bioprojects']:>2} "
                      f"p={r['p_value']} q={r['q_value']}")
        print()


main()
