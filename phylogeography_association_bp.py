#!/usr/bin/env python3
"""
phylogeography_association_bp.py

Test whether the phylogeny carries geographic signal, and whether that signal
survives the thing most likely to be producing it.

THE TEST. For each unit's recombination-corrected tree, compute the Fitch
small-parsimony score of the country labels: the minimum number of state changes
needed to explain the tips given the topology. Few changes means samples from a
country sit together on the tree. Compare that score to a null built by shuffling
the labels across tips of the SAME tree, 1,000 times. The permutation null holds
the topology AND the label composition fixed, so a unit that is 90% Thailand is
compared against other 90%-Thailand arrangements, not against an even mix. This
is the Slatkin-Maddison style test, and it is the right shape here because the
marginal country distribution is wildly uneven and no parametric null would
respect that.

WHY BIOPROJECT IS RUN ALONGSIDE, and why the answer is not optional. In this
collection **70.5% of genomes are Thailand and the top 3 BioProjects are 58.4%**
of everything. A BioProject is typically one study, one lab, one country, often
one outbreak or one hospital -- so "country" and "BioProject" are largely the
same variable wearing different labels. A geographic signal that is no stronger
than the BioProject signal is not evidence of phylogeography; it is evidence that
related isolates get sequenced together. Both are tested on identical trees with
identical machinery so the two scores are directly comparable.

WHAT A SIGNIFICANT RESULT DOES AND DOES NOT MEAN. It means tips sharing a label
are closer on the tree than chance. It does NOT establish direction of spread,
dates, or migration rates -- nothing here is a phylogeographic reconstruction,
and this collection's sampling cannot support one.

Units where every genome carries one country are reported separately: their
parsimony score is trivially 0 and no permutation can differ, so they carry no
information and must not be counted as "significant".

Stdlib only.
"""

import argparse
import collections
import csv
import glob
import os
import random
import re
import sys


# ---------------------------------------------------------------- newick ----
def parse_newick(s):
    """Return a nested tuple tree: (children_list, label). Leaves have []."""
    s = s.strip().rstrip(";")
    pos = [0]

    def node():
        children = []
        if pos[0] < len(s) and s[pos[0]] == "(":
            pos[0] += 1
            while True:
                children.append(node())
                if pos[0] < len(s) and s[pos[0]] == ",":
                    pos[0] += 1
                    continue
                if pos[0] < len(s) and s[pos[0]] == ")":
                    pos[0] += 1
                break
        start = pos[0]
        while pos[0] < len(s) and s[pos[0]] not in "(),":
            pos[0] += 1
        token = s[start:pos[0]]
        label = token.split(":")[0].strip().strip("'\"")
        return (children, label)

    return node()


def leaves(tree):
    ch, lab = tree
    if not ch:
        return [lab]
    out = []
    for c in ch:
        out.extend(leaves(c))
    return out


def fitch_score(tree, state_of):
    """
    Fitch small parsimony, iterative post-order to avoid recursion limits.

    Returns the minimum number of state changes on the topology. Tips whose
    state is unknown are treated as fully ambiguous (they never force a change),
    so missing metadata weakens the signal rather than inventing one.
    """
    changes = [0]

    def rec(node):
        ch, lab = node
        if not ch:
            st = state_of.get(lab)
            return None if st is None else {st}
        sets = [rec(c) for c in ch]
        sets = [s for s in sets if s is not None]
        if not sets:
            return None
        inter = set.intersection(*sets)
        if inter:
            return inter
        changes[0] += 1
        return set.union(*sets)

    sys.setrecursionlimit(100000)
    rec(tree)
    return changes[0]


def permutation_p(tree, labels, states, n_perm, rng):
    """
    p = P(shuffled score <= observed). Shuffling only the ASSIGNMENT of the
    observed multiset of states preserves both topology and label composition.
    """
    obs = fitch_score(tree, dict(zip(labels, states)))
    pool = list(states)
    hits = 0
    for _ in range(n_perm):
        rng.shuffle(pool)
        if fitch_score(tree, dict(zip(labels, pool))) <= obs:
            hits += 1
    return obs, (hits + 1) / (n_perm + 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--assignments", default="L1_ASSIGNMENTS.tsv")
    ap.add_argument("--trees", default="L1_out/Clusters")
    ap.add_argument("--perms", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=20260815)
    ap.add_argument("--out", default="PHYLOGEOGRAPHY_ASSOCIATION.tsv")
    a = ap.parse_args()

    rng = random.Random(a.seed)
    meta = {}
    for r in csv.DictReader(open(a.assignments), delimiter="\t"):
        meta[r["sample_id"]] = r

    rows = []
    for tre in sorted(glob.glob(os.path.join(
            a.trees, "*", "Gubbins", "*.node_labelled.final_tree.tre"))):
        base = os.path.basename(tre).replace(".node_labelled.final_tree.tre", "")
        m = re.match(r"^(.*?)__(.*)_(\d+)$", base)
        if not m:
            continue
        unit, _, rep = m.groups()
        # One tree per unit is enough; the two replicons share a genealogy.
        if rep != "1":
            continue
        try:
            tree = parse_newick(open(tre).read())
        except Exception as e:
            print(f"  cannot parse {base}: {e}", file=sys.stderr)
            continue

        tips = [t for t in leaves(tree) if t and t != "Reference"]
        if len(tips) < 4:
            continue

        for var, col in (("country", "country"), ("bioproject", "bioproject")):
            states = [meta.get(t, {}).get(col, "") or None for t in tips]
            known = [s for s in states if s]
            distinct = len(set(known))
            base_row = {
                "unit": unit, "n_tips": len(tips), "variable": var,
                "n_known": len(known), "n_distinct": distinct,
            }
            if distinct < 2:
                base_row.update({
                    "parsimony_score": 0 if distinct else "",
                    "p_value": "", "verdict": "uninformative: <2 distinct values",
                    "top_share": "1.000" if distinct else "",
                })
                rows.append(base_row)
                continue
            obs, p = permutation_p(tree, tips, states, a.perms, rng)
            top = collections.Counter(known).most_common(1)[0][1] / len(known)
            base_row.update({
                "parsimony_score": obs,
                "p_value": f"{p:.4f}",
                "verdict": "clustered" if p <= 0.05 else "not distinguishable from chance",
                "top_share": f"{top:.3f}",
            })
            rows.append(base_row)

    cols = ["unit", "n_tips", "variable", "n_known", "n_distinct",
            "parsimony_score", "top_share", "p_value", "verdict"]
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                           lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"units tested: {len({r['unit'] for r in rows})}\n")
    for var in ("country", "bioproject"):
        g = [r for r in rows if r["variable"] == var and r["p_value"]]
        sig = [r for r in g if float(r["p_value"]) <= 0.05]
        uninf = [r for r in rows if r["variable"] == var and not r["p_value"]]
        print(f"{var}:")
        print(f"  testable units        : {len(g)}  (plus {len(uninf)} uninformative, single-valued)")
        print(f"  clustered (p <= 0.05) : {len(sig)}  ({100.0*len(sig)/max(len(g),1):.0f}% of testable)")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
