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

WHY BIOPROJECT IS RUN ALONGSIDE, and why the answer is not optional. In the v4c
analysed set (2,352 genomes over 86 units) **66.4% of genomes are Thailand**, and
the two largest BioProjects -- PRJEB25606 (543) and PRJEB35787 (468) -- are 43%
of everything between them. A BioProject is typically one study, one lab, one
country, often one outbreak or one hospital -- so "country" and "BioProject" are
largely the same variable wearing different labels. A geographic signal that is no
stronger than the BioProject signal is not evidence of phylogeography; it is
evidence that related isolates get sequenced together. Both are tested on
identical trees with identical machinery so the two scores are directly
comparable.

MISSING VALUES. The metadata encodes "no data" inconsistently: `country` uses an
empty cell, but `bioproject` uses the literal string "unknown" for 274 of the
2,352 v4c tips. Taken at face value those 274 would form a single spurious
274-member "study", mis-measuring the very confounder this test exists to check
-- and measurement error in a confounder understates it, biasing toward a false
positive for geography. Every value in MISSING below is therefore normalised to
None and treated as fully ambiguous, so absent metadata weakens signal rather
than inventing it.

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


# Placeholders that mean "no data" and must not become a shared state.
MISSING = {"", "unknown", "na", "n/a", "none", "null", "missing", "-", "."}


def state_of_value(v):
    v = (v or "").strip()
    return None if v.lower() in MISSING else v


def state_of_row(row, col):
    """Country state for one genome, or None if it cannot be one country.

    A genome whose origin resolves to more than one country ('Panama and Peru')
    is not evidence for a country -- scoring it as its own state invents a
    singleton label and adds a spurious Fitch change. Treat it as missing, the
    same as an unknown. Keyed on origin_resolution rather than string-matching
    the value, because 'Trinidad and Tobago' is one country.
    """
    if col == "country" and row.get("origin_resolution") == "multi_country":
        return None
    return state_of_value(row.get(col, ""))


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


def bh_qvalues(pvals):
    """Benjamini-Hochberg step-up. -> q in the same order as the input."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    q = [0.0] * m
    prev = 1.0
    for rank, i in enumerate(reversed(order), start=1):
        k = m - rank + 1                       # 1-based rank of this p ascending
        prev = min(prev, pvals[i] * m / k)
        q[i] = prev
    return q


def annotate(rows, alpha, cov_min, distinct_min):
    """Add q_value, control_status and interpretation.

    Both of these were applied by hand and lived only as prose -- the BH step in
    PHYLOGEOGRAPHY_ASSOCIATION_INTERPRETATION.md and the >=70% / >=3-project
    control gate at its lines 155-157. Nothing in the repo reproduced either, so
    the four-outcome taxonomy could not be regenerated from the outputs.

    The correction family is the testable country rows of THIS run -- one scale,
    country only. BioProject rows are the control, not hypotheses, so folding
    them in would dilute the very comparison they exist to make.
    """
    bp = {r["unit"]: r for r in rows if r["variable"] == "bioproject"}
    ctry = [r for r in rows if r["variable"] == "country" and r["p_value"]]

    qs = bh_qvalues([float(r["p_value"]) for r in ctry])
    for r, q in zip(ctry, qs):
        r["q_value"] = f"{min(q, 1.0):.4f}"

    for r in rows:
        c = bp.get(r["unit"])
        if not c:
            status = "absent"
        elif int(c["n_known"]) == 0:
            status = "absent"
        elif (int(c["n_known"]) / max(int(c["n_tips"]), 1) >= cov_min
              and int(c["n_distinct"]) >= distinct_min):
            status = "ok"
        else:
            status = "vacuous"
        r["control_status"] = status
        r.setdefault("q_value", "")

        if r["variable"] != "country":
            r["interpretation"] = ""
            continue
        if not r["p_value"]:
            r["interpretation"] = "untestable: single-valued"
        elif float(r["q_value"]) > alpha:
            r["interpretation"] = "null"
        elif status != "ok":
            r["interpretation"] = f"{status} control"
        elif c["p_value"] and float(c["p_value"]) <= alpha:
            # country and study are clustered on the same tree at the same level
            r["interpretation"] = "confounded"
        else:
            r["interpretation"] = "geographic (control passes)"


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
    ap.add_argument("--fdr", type=float, default=0.05)
    ap.add_argument("--control-coverage", type=float, default=0.70)
    ap.add_argument("--control-distinct", type=int, default=3)
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
            states = [state_of_row(meta.get(t, {}), col) for t in tips]
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

    annotate(rows, a.fdr, a.control_coverage, a.control_distinct)

    cols = ["unit", "n_tips", "variable", "n_known", "n_distinct",
            "parsimony_score", "top_share", "p_value", "verdict",
            "q_value", "control_status", "interpretation"]
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
        if var == "country":
            surv = [r for r in g if float(r["q_value"]) <= a.fdr]
            print(f"  surviving BH-FDR {a.fdr:.0%}  : {len(surv)}")

    print("\ncountry interpretation:")
    for k, n in collections.Counter(
            r["interpretation"] for r in rows
            if r["variable"] == "country" and r["interpretation"]).most_common():
        print(f"  {k:<32}: {n}")
    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
