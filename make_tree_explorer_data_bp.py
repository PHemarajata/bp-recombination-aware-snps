#!/usr/bin/env python3
"""
Build the data payload for the interactive global tree.

Reads the grafted chr1 tree (2,352 tips), prunes it to the 2,340 genomes of the
frozen basis, ladderizes it, lays it out as a CLADOGRAM, and emits one compact
JSON that a canvas viewer can render without any further computation.

IT IS A CLADOGRAM ON PURPOSE, on the same rule as make_figure6_bp.py. The grafted
tree splices two branch-length scales that differ by roughly 133-fold: backbone
edges are substitutions per site over the parsnp core, within-unit edges are
substitutions per site over that unit's recombination-filtered variable sites.
Drawing them would put nearly all visible length in the backbone, compress every
unit to a dot, and imply the distances are comparable. They are not.

A CLADE BLOCK IS ONLY EMITTED WHERE IT IS A REAL CLADE. Contiguity in tip order is
not monophyly, so each candidate is checked against its MRCA's leaf set, on the
same rule and with the same result as make_figure6_bp.py and
make_itol_grafted_bp.py.

Fails rather than writing if any count disagrees with NUMBERS.tsv.

  python3 make_tree_explorer_data_bp.py      # writes TREE_EXPLORER_DATA.json
"""

import csv
import json
import os
import re
import sys

B = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, B)
from make_itol_bp import parse_newick, tips_of, prune  # noqa: E402

TREE = f"{B}/L1v4c_out/global_grafted_chr1.treefile"
PART = f"{B}/FINAL_BASIS_2026-08-22/FINAL_PARTITION.tsv"
META = f"{B}/L1v4c_MERGED_METADATA.tsv"
GATE = f"{B}/GATE1_ALIGNMENT_2026-08-21.tsv"
REGION = f"{B}/assign_region.tsv"
NUMBERS = f"{B}/NUMBERS.tsv"
OUT = f"{B}/TREE_EXPLORER_DATA.json"


def strain_of(u):
    m = re.match(r"(strain_\d+)", u)
    return m.group(1) if m else u


def main():
    for p in (TREE, PART, META, GATE, REGION, NUMBERS):
        if not os.path.isfile(p):
            sys.exit(f"FATAL: {p} not found.")

    numbers = {r["key"]: r["value"]
               for r in csv.DictReader(open(NUMBERS), delimiter="\t")}
    exp_g = int(numbers["genomes.analysed"])
    exp_u = int(numbers["units.analysed"])

    g2u = {r["sample_id"]: r["unit"]
           for r in csv.DictReader(open(PART), delimiter="\t")}
    if len(g2u) != exp_g:
        sys.exit(f"FATAL: partition has {len(g2u)} rows, NUMBERS.tsv says {exp_g}.")

    # Column 9 of the merged metadata is the real country.
    meta = {}
    for r in csv.DictReader(open(META), delimiter="\t"):
        meta[r["sample_id"]] = r.get("country") or ""

    # assign_region.tsv's column named "country" holds WORLD REGION values, not
    # countries. That mislabeling is a documented trap. It is read here for the
    # region only, and the country above never comes from this file.
    region = {}
    for r in csv.DictReader(open(REGION), delimiter="\t"):
        region[r["sample_id"]] = r.get("country") or ""

    gate = {r["unit"]: (r["gate1_alignment"],
                        float(r["aln_mean_pairwise_snps"]),
                        float(r["rm_corrected"]),
                        int(r["n"]))
            for r in csv.DictReader(open(GATE), delimiter="\t")}
    if len(gate) != exp_u:
        sys.exit(f"FATAL: Gate 1 table has {len(gate)} units, NUMBERS.tsv says {exp_u}.")

    root = parse_newick(open(TREE).read())
    all_tips = tips_of(root)
    keep = {t for t in all_tips if t in g2u}
    if len(keep) != exp_g:
        sys.exit(f"FATAL: {len(keep)} tips kept, NUMBERS.tsv says {exp_g}.")
    dropped = len(all_tips) - len(keep)
    root = prune(root, keep)
    if len(tips_of(root)) != exp_g:
        sys.exit("FATAL: prune did not leave the expected tip set.")

    # DO NOT LADDERIZE. make_figure6_bp.py draws the pruned tree in its natural
    # tip order, and the 29-of-30 monophyly result is a property of that order.
    # Reordering the children changes which strain blocks are contiguous, and the
    # check at the bottom of this file catches it.

    # Flatten. Parent array plus depth, tips in drawing order.
    nodes = []          # (parent_index, is_tip)
    tip_order = []

    def walk(n, parent):
        idx = len(nodes)
        nodes.append([parent, 1 if not n.children else 0])
        if not n.children:
            tip_order.append((idx, n.name))
        for c in n.children:
            walk(c, idx)
        return idx
    walk(root, -1)

    depth = [0] * len(nodes)
    for i in range(1, len(nodes)):
        depth[i] = depth[nodes[i][0]] + 1
    maxdepth = max(depth)

    # y for a tip is its rank; y for an internal node is the mean of its children.
    y = [0.0] * len(nodes)
    kids = [[] for _ in nodes]
    for i in range(1, len(nodes)):
        kids[nodes[i][0]].append(i)
    for rank, (idx, _name) in enumerate(tip_order):
        y[idx] = float(rank)
    for i in range(len(nodes) - 1, -1, -1):
        if kids[i]:
            y[i] = (y[kids[i][0]] + y[kids[i][-1]]) / 2.0

    # Cladogram geometry, on make_figure6_bp.py's rule. A node's radius there is
    # 1 - height/H, where height is the distance to the farthest leaf below it.
    # The rectangular equivalent is x = H - height, so every tip lands at H and
    # the root at 0. Using depth instead would ragged the tips.
    height = [0] * len(nodes)
    for i in range(len(nodes) - 1, -1, -1):
        height[i] = 0 if not kids[i] else 1 + max(height[k] for k in kids[i])
    H = height[0]
    x = [float(H - height[i]) for i in range(len(nodes))]

    # Per-tip attributes, as small integer codes.
    units, countries, regions = [], [], []
    ui, ci, ri = {}, {}, {}

    def code(v, table, arr):
        if v not in table:
            table[v] = len(arr)
            arr.append(v)
        return table[v]

    tip_idx, tip_name, tip_unit, tip_country, tip_region = [], [], [], [], []
    for idx, name in tip_order:
        u = g2u[name]
        c = meta.get(name, "")
        sr = region.get(name, "")
        tip_idx.append(idx)
        tip_name.append(name)
        tip_unit.append(code(u, ui, units))
        tip_country.append(code(c or "unknown", ci, countries))
        tip_region.append(code(sr or "unknown", ri, regions))

    # Leaf set of every internal node, as a first and last tip rank plus a count.
    rank_of = {idx: r for r, (idx, _n) in enumerate(tip_order)}
    lo = [0] * len(nodes)
    hi = [0] * len(nodes)
    cnt = [0] * len(nodes)
    for i in range(len(nodes) - 1, -1, -1):
        if nodes[i][1]:
            lo[i] = hi[i] = rank_of[i]
            cnt[i] = 1
        else:
            lo[i] = min(lo[k] for k in kids[i])
            hi[i] = max(hi[k] for k in kids[i])
            cnt[i] = sum(cnt[k] for k in kids[i])

    def mrca(ranks):
        """Lowest node whose leaf span covers every rank and nothing else."""
        want_lo, want_hi = min(ranks), max(ranks)
        best = 0
        stack = [0]
        while stack:
            i = stack.pop()
            if lo[i] <= want_lo and hi[i] >= want_hi:
                best = i
                stack.extend(kids[i])
        return best

    # Blocks, per unit and per strain. A block is emitted with is_clade set only
    # when the MRCA subtends exactly the members, on the make_figure6_bp.py rule.
    def blocks_for(group_of):
        by = {}
        for r, (_idx, name) in enumerate(tip_order):
            by.setdefault(group_of(g2u[name]), []).append(r)
        out = []
        for g, ranks in sorted(by.items()):
            ranks.sort()
            # Contiguous runs, so a non-monophyletic group yields several blocks.
            runs, start = [], ranks[0]
            for a, b in zip(ranks, ranks[1:]):
                if b != a + 1:
                    runs.append((start, a))
                    start = b
            runs.append((start, ranks[-1]))
            for a, b in runs:
                node = mrca(range(a, b + 1))
                out.append({"g": g, "lo": a, "hi": b, "node": node,
                            "clade": bool(cnt[node] == (b - a + 1))})
        return out

    unit_blocks = blocks_for(lambda u: u)
    strain_blocks = blocks_for(strain_of)

    n_strain_blocks = len(strain_blocks)
    n_shaded = sum(1 for b in strain_blocks if b["clade"])
    if n_strain_blocks != 30 or n_shaded != 29:
        sys.exit(f"FATAL: strain blocks {n_shaded} of {n_strain_blocks} shaded, "
                 "expected 29 of 30 as in make_figure6_bp.py.")

    unit_meta = {}
    for u in units:
        cls, div, rm, n = gate[u]
        unit_meta[u] = {"cls": cls, "div": div, "rm": rm, "n": n,
                        "strain": strain_of(u)}

    payload = {
        "_note": ("Cladogram. Branch lengths are deliberately absent because the "
                  "grafted tree splices two scales differing by about 133-fold. "
                  "No rate or date may be derived from this tree. Generated by "
                  "make_tree_explorer_data_bp.py from the frozen basis."),
        "n_tips": len(tip_order),
        "n_units": len(units),
        "n_nodes": len(nodes),
        "maxdepth": H,
        "dropped_tips": dropped,
        "parent": [n[0] for n in nodes],
        "x": [round(v, 3) for v in x],
        "y": [round(v, 3) for v in y],
        "istip": [n[1] for n in nodes],
        "tip_idx": tip_idx,
        "tip_name": tip_name,
        "tip_unit": tip_unit,
        "tip_country": tip_country,
        "tip_region": tip_region,
        "units": units,
        "countries": countries,
        "regions": regions,
        "unit_meta": unit_meta,
        "unit_blocks": unit_blocks,
        "strain_blocks": strain_blocks,
    }

    with open(OUT, "w") as fh:
        json.dump(payload, fh, separators=(",", ":"))
    print(f"wrote {OUT}")
    print(f"  {len(tip_order)} tips, {len(nodes)} nodes, {dropped} pruned, "
          f"max depth {maxdepth}")
    print(f"  {len(units)} units, {len(countries)} countries, "
          f"{len(regions)} regions")
    print(f"  strain blocks {n_shaded} of {n_strain_blocks} are real clades")
    nc = sum(1 for b in unit_blocks if not b["clade"])
    print(f"  unit blocks {len(unit_blocks)}, {nc} not monophyletic")
    print(f"  {os.path.getsize(OUT)/1024:.0f} KB")


if __name__ == "__main__":
    main()
