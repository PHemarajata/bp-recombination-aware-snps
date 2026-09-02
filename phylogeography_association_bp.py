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

WHY BIOPROJECT IS RUN ALONGSIDE, and why the answer is not optional. A BioProject
is typically one study, one lab, one country, often one outbreak or one hospital,
so "country" and "BioProject" are largely the same variable wearing different
labels. A geographic signal that is no stronger than the BioProject signal is not
evidence of phylogeography; it is evidence that related isolates get sequenced
together. Both are tested on identical trees with identical machinery so the two
scores are directly comparable.

WHAT A SIGNIFICANT RESULT DOES AND DOES NOT MEAN. It means tips sharing a label
are closer on the tree than chance. It does NOT establish direction of spread,
dates, or migration rates. Nothing here is a phylogeographic reconstruction, and
this collection's sampling cannot support one.

SINGLE-COUNTRY UNITS ARE THE CLEAN EVIDENCE, AND THEY NEED A DIFFERENT TEST.
A unit in which every genome shares one country has a parsimony score of zero
that no permutation can better, so the permutation test is uninformative by
construction and such units must never be counted as "significant" alongside the
others. They are instead tested as a group, against the probability of drawing
n genomes of one country at random from the collection's own country
distribution, sampling without replacement. The null distribution of the COUNT of
single-country units is Poisson-binomial over units and is computed exactly by
dynamic programming rather than simulated. This is the test that produces the
headline geographic result, and before this version it existed only in the
methods text and not in any code.

THREE THINGS THIS VERSION CHANGES, each because of a defect that actually
occurred:

1. --assignments and --trees are REQUIRED and have no defaults. A previous run
   passed --assignments for a new partition while --trees silently kept its old
   default, joining new assignments to old trees and reporting entirely plausible
   numbers. It was caught only by noticing the unit count. Defaults that point at
   one particular partition are a trap, so there are none.

2. A preflight cross-checks the unit set in the assignments file against the unit
   set on disk and ABORTS on mismatch. A silent join is now impossible: either the
   two agree, or the run stops and prints what differs.

3. Both replicons are tested and their agreement is reported. The two replicons of
   a unit share one genealogy, so concordance is a free check that a result is
   real. Replicon 1 remains the reported value; replicon 2 is the check.

Stdlib only.
"""

import argparse
import collections
import csv
import glob
import math
import os
import random
import re
import sys


# ---------------------------------------------------------------- newick ----
def parse_newick(s):
    """
    Return a nested tuple tree: (children_list, label). Leaves have [].

    Iterative, with an explicit stack. A recursive descent parser recurses once
    per level of nesting, so a ladder-shaped tree of n tips needs n frames and
    overflows the interpreter stack well before it runs out of memory. Unit
    sizes here reach 159, which a recursive parser survives, but the failure is
    silent-adjacent (a RecursionError deep in a loop over hundreds of files) and
    costs nothing to remove.
    """
    s = s.strip().rstrip(";")
    stack = []        # child-lists of the enclosing, still-open nodes
    children = []     # children of the node currently being built
    i, n = 0, len(s)

    def read_label(j):
        start = j
        while j < n and s[j] not in "(),":
            j += 1
        return s[start:j].split(":")[0].strip().strip("'\""), j

    while i < n:
        c = s[i]
        if c == "(":
            stack.append(children)
            children = []
            i += 1
        elif c == ",":
            i += 1
        elif c == ")":
            label, i = read_label(i + 1)
            node = (children, label)
            if not stack:                     # unbalanced parentheses
                return node
            children = stack.pop()
            children.append(node)
        else:
            label, i = read_label(i)
            children.append(([], label))

    if not children:
        return ([], "")
    return children[0] if len(children) == 1 else (children, "")


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
    Fitch small parsimony over an explicit stack, so tree depth cannot exhaust
    the interpreter stack. (An earlier version claimed to be iterative in its
    docstring while in fact recursing; it is genuinely iterative now.)

    Returns the minimum number of state changes on the topology. Tips whose
    state is unknown are treated as fully ambiguous: they contribute no set and
    therefore never force a change, so missing metadata weakens the signal rather
    than inventing one.
    """
    changes = 0
    # Post-order via an explicit stack of (node, visited_flag).
    stack = [(tree, False)]
    results = {}
    while stack:
        node, visited = stack.pop()
        key = id(node)
        ch, lab = node
        if not ch:
            st = state_of.get(lab)
            results[key] = None if st is None else {st}
            continue
        if not visited:
            stack.append((node, True))
            for c in ch:
                stack.append((c, False))
            continue
        sets = [results[id(c)] for c in ch]
        sets = [s for s in sets if s is not None]
        if not sets:
            results[key] = None
            continue
        inter = set.intersection(*sets)
        if inter:
            results[key] = inter
        else:
            changes += 1
            results[key] = set.union(*sets)
    return changes


def permutation_p(tree, labels, states, n_perm, rng):
    """
    p = P(shuffled score <= observed). Shuffling only the ASSIGNMENT of the
    observed multiset of states preserves both topology and label composition.

    Unknown states (None) are shuffled along with the rest, so the null preserves
    how MANY tips are unknown but not WHICH. That is the intended null: it asks
    whether the observed arrangement of the labels we have is more clustered than
    chance, holding the amount of missing data fixed.
    """
    obs = fitch_score(tree, dict(zip(labels, states)))
    pool = list(states)
    hits = 0
    for _ in range(n_perm):
        rng.shuffle(pool)
        if fitch_score(tree, dict(zip(labels, pool))) <= obs:
            hits += 1
    return obs, (hits + 1) / (n_perm + 1)


# ------------------------------------------------- single-country testing ----
def p_all_one_country(n, country_counts, total):
    """
    P(a random draw of n genomes, without replacement, from the whole collection
    is entirely one country) = sum over countries C of C(N_C, n) / C(N, n).

    Without replacement is the right model: units are disjoint subsets of one
    finite collection, not independent draws.
    """
    if n < 2 or n > total:
        return 0.0
    denom = math.comb(total, n)
    if denom == 0:
        return 0.0
    return sum(math.comb(nc, n) for nc in country_counts.values() if nc >= n) / denom


def poisson_binomial_tail(probs, k):
    """
    Exact P(X >= k) where X is the number of successes among independent
    Bernoulli trials with the given (unequal) probabilities. Exact DP, not a
    simulation, because with ~88 units the state space is trivial and a
    simulated p-value would bottom out at 1/nsim and hide the true magnitude.
    """
    dist = [1.0]
    for p in probs:
        nxt = [0.0] * (len(dist) + 1)
        for i, d in enumerate(dist):
            nxt[i] += d * (1.0 - p)
            nxt[i + 1] += d * p
        dist = nxt
    return sum(dist[k:]) if k <= len(dist) - 1 else 0.0


# ------------------------------------------------------------- preflight ----
def collect_tree_files(trees_dir):
    """unit -> {replicon -> path} for every Gubbins node-labelled tree found."""
    found = collections.defaultdict(dict)
    pattern = os.path.join(trees_dir, "*", "Gubbins",
                           "*.node_labelled.final_tree.tre")
    for tre in sorted(glob.glob(pattern)):
        base = os.path.basename(tre).replace(".node_labelled.final_tree.tre", "")
        m = re.match(r"^(.*?)__(.*)_(\d+)$", base)
        if not m:
            continue
        unit, _, rep = m.groups()
        found[unit][rep] = tre
    return found


def preflight(assign_units, tree_units, allow_partial):
    """
    Fail loudly when the assignments and the trees describe different partitions.

    This exists because that exact mismatch has happened: new assignments were
    joined to an old tree directory and produced entirely plausible numbers,
    caught only by someone noticing the unit count. A plausible wrong answer is
    the worst failure mode available here, so it is now an abort rather than a
    warning.
    """
    only_assign = sorted(assign_units - tree_units)
    only_trees = sorted(tree_units - assign_units)
    both = assign_units & tree_units

    print("PREFLIGHT")
    print(f"  units in assignments : {len(assign_units)}")
    print(f"  units with trees     : {len(tree_units)}")
    print(f"  in both              : {len(both)}")
    if only_assign:
        print(f"  in assignments only  : {len(only_assign)}  "
              f"e.g. {', '.join(only_assign[:5])}")
    if only_trees:
        print(f"  in trees only        : {len(only_trees)}  "
              f"e.g. {', '.join(only_trees[:5])}")

    if only_assign or only_trees:
        if not allow_partial:
            print("\nABORT: the assignments file and the tree directory describe "
                  "different partitions.\n"
                  "       Repoint --assignments and --trees at the SAME run, or "
                  "pass --allow-partial\n"
                  "       if you genuinely intend to analyse only the "
                  "intersection.", file=sys.stderr)
            sys.exit(2)
        print("  --allow-partial given: continuing on the intersection only.")
    print()
    return both


# ------------------------------------------------------------------ main ----
def main():
    ap = argparse.ArgumentParser(
        description="Phylogeny-geography association, per unit, with a "
                    "BioProject confounder control and an exact "
                    "single-country enrichment test.")
    # No defaults. See module docstring, change 1.
    ap.add_argument("--assignments", required=True,
                    help="TSV with sample_id, country, bioproject, unit")
    ap.add_argument("--trees", required=True,
                    help="Clusters/ directory holding <unit>/Gubbins/*.tre")
    ap.add_argument("--unit-col", default="unit",
                    help="column in --assignments naming the analysis unit")
    ap.add_argument("--perms", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=20260815)
    ap.add_argument("--out", required=True)
    ap.add_argument("--allow-partial", action="store_true",
                    help="proceed on the intersection when assignments and "
                         "trees disagree (default: abort)")
    a = ap.parse_args()

    rng = random.Random(a.seed)

    # ---- load assignments -------------------------------------------------
    meta = {}
    assign_units = set()
    with open(a.assignments) as fh:
        rdr = csv.DictReader(fh, delimiter="\t")
        if a.unit_col not in (rdr.fieldnames or []):
            print(f"ABORT: --assignments has no column '{a.unit_col}'. "
                  f"Columns present: {rdr.fieldnames}", file=sys.stderr)
            sys.exit(2)
        for r in rdr:
            meta[r["sample_id"]] = r
            if r.get(a.unit_col):
                assign_units.add(r[a.unit_col])

    # Collection-wide country composition, for the single-country null.
    country_counts = collections.Counter(
        r["country"] for r in meta.values() if r.get("country"))
    total_known_country = sum(country_counts.values())

    tree_files = collect_tree_files(a.trees)
    usable = preflight(assign_units, set(tree_files), a.allow_partial)

    rows = []
    single_country = []          # (unit, n, country)
    concordance = []             # (unit, p_rep1, p_rep2) for country

    # Parse every tree once. Re-parsing inside the variable loop was a real
    # cost and an easy place to get the wrong tree.
    parsed = {}          # unit -> {replicon -> (tree, tips)}
    for unit in sorted(usable):
        per_rep = {}
        for rep, tre in sorted(tree_files[unit].items()):
            try:
                tree = parse_newick(open(tre).read())
            except Exception as e:
                print(f"  cannot parse {unit} replicon {rep}: {e}",
                      file=sys.stderr)
                continue
            tips = [t for t in leaves(tree) if t and t != "Reference"]
            if len(tips) < 4:
                continue
            per_rep[rep] = (tree, tips)
        if per_rep:
            parsed[unit] = per_rep

    for unit in sorted(parsed):
        per_rep = parsed[unit]
        if "1" not in per_rep:
            continue
        tree1, tips = per_rep["1"]

        for var, col in (("country", "country"), ("bioproject", "bioproject")):
            states = [meta.get(t, {}).get(col, "") or None for t in tips]
            known = [s for s in states if s]
            distinct = len(set(known))
            row = {
                "unit": unit, "n_tips": len(tips), "variable": var,
                "n_known": len(known), "n_distinct": distinct,
                "replicon2_p_value": "", "replicon2_agrees": "",
            }

            if distinct < 2:
                # Uninformative for the permutation test by construction.
                row.update({
                    "parsimony_score": 0 if distinct else "",
                    "p_value": "",
                    "verdict": "uninformative: <2 distinct values",
                    "top_share": "1.000" if distinct else "",
                })
                # A single-COUNTRY unit is the clean evidence and gets the
                # group-level test below, but only when every tip is known:
                # an unknown tip could be a second country.
                if (var == "country" and distinct == 1
                        and len(known) == len(tips) and len(tips) >= 2):
                    single_country.append((unit, len(tips), known[0]))
                rows.append(row)
                continue

            obs, p = permutation_p(tree1, tips, states, a.perms, rng)
            top = collections.Counter(known).most_common(1)[0][1] / len(known)
            row.update({
                "parsimony_score": obs,
                "p_value": f"{p:.4f}",
                "verdict": "clustered" if p <= 0.05
                           else "not distinguishable from chance",
                "top_share": f"{top:.3f}",
            })

            # Replicon 2 as a free consistency check on the same genealogy.
            if "2" in per_rep:
                tree2, tips2 = per_rep["2"]
                states2 = [meta.get(t, {}).get(col, "") or None for t in tips2]
                if len(set(s for s in states2 if s)) >= 2:
                    _, p2 = permutation_p(tree2, tips2, states2, a.perms, rng)
                    row["replicon2_p_value"] = f"{p2:.4f}"
                    row["replicon2_agrees"] = str(
                        (p <= 0.05) == (p2 <= 0.05))
                    if var == "country":
                        concordance.append((unit, p, p2))
            rows.append(row)

    cols = ["unit", "n_tips", "variable", "n_known", "n_distinct",
            "parsimony_score", "top_share", "p_value", "verdict",
            "replicon2_p_value", "replicon2_agrees"]
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                           lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # ---- report -----------------------------------------------------------
    print(f"units tested: {len({r['unit'] for r in rows})}\n")
    for var in ("country", "bioproject"):
        g = [r for r in rows if r["variable"] == var and r["p_value"]]
        sig = [r for r in g if float(r["p_value"]) <= 0.05]
        uninf = [r for r in rows if r["variable"] == var and not r["p_value"]]
        print(f"{var}:")
        print(f"  testable units        : {len(g)}  "
              f"(plus {len(uninf)} uninformative, single-valued)")
        print(f"  clustered (p <= 0.05) : {len(sig)}  "
              f"({100.0 * len(sig) / max(len(g), 1):.0f}% of testable)")

    if concordance:
        agree = sum(1 for _, p1, p2 in concordance
                    if (p1 <= 0.05) == (p2 <= 0.05))
        print(f"\nreplicon concordance (country): {agree}/{len(concordance)} "
              f"units give the same verdict on both replicons")

    print("\nSINGLE-COUNTRY UNITS  (the clean geographic evidence)")
    if not single_country:
        print("  none")
    else:
        obs_k = len(single_country)
        # The null count is over every unit with >=2 fully-known-country tips.
        all_probs = []
        for unit in sorted(parsed):
            if "1" not in parsed[unit]:
                continue
            _, tips = parsed[unit]["1"]
            st = [meta.get(t, {}).get("country", "") or None for t in tips]
            if len(tips) >= 2 and all(s for s in st):
                all_probs.append(p_all_one_country(
                    len(tips), country_counts, total_known_country))
        exp_all = sum(all_probs)
        p_enrich = poisson_binomial_tail(all_probs, obs_k)
        print(f"  observed              : {obs_k}")
        print(f"  expected by chance    : {exp_all:.2f}  "
              f"(Poisson-binomial over {len(all_probs)} eligible units,")
        print(f"                           sampling without replacement from "
              f"{total_known_country} genomes in "
              f"{len(country_counts)} countries)")
        print(f"  P(X >= observed)      : {p_enrich:.3g}  (exact)")
        print("  NOTE: this counts only units in which EVERY tip has a known "
              "country.")
        print("        A unit with an unknown tip cannot be called "
              "single-country.")
        byc = collections.Counter(c for _, _, c in single_country)
        print("  by country            : " + ", ".join(
            f"{c}={k}" for c, k in byc.most_common()))

    print(f"\nwrote {a.out}")


if __name__ == "__main__":
    main()
