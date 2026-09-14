#!/usr/bin/env python3
"""
make_itol_grafted_bp.py -- iTOL package for the GENOME-level global tree,
with shaded slices per PopPUNK strain.

`make_itol_bp.py` exports the 85-tip tree of unit medoids. This exports the other
one: the grafted tree carrying **every analysed genome**, with the 28 strains
shaded as ranges so the global structure is readable at a glance.

WHAT A "SLICE" HAS TO EARN. iTOL's `range` shades the clade subtended by the
most recent common ancestor of two leaves. Handing it the first and last leaf of
a visually contiguous run is not enough, because contiguity in tip order is not
monophyly: the MRCA can subtend leaves belonging to other strains, and iTOL will
shade them without complaint. So every candidate slice here is checked -- the
MRCA's leaf set must equal the block exactly, or no range is written for it and
the script says which one failed and why.

WHAT THAT CHECK FINDS. 27 of the 28 strains form a single block. **strain_1 does
not**: it falls in three separate blocks of 548, 139 and 195 genomes. Shading it
as one slice would have drawn a wedge across two other strains. It is emitted as
three slices instead, sharing one colour and one legend entry.

THE TREE MIXES TWO BRANCH-LENGTH SCALES BY CONSTRUCTION and that is not a defect
to be fixed here, it is a property to be disclosed. Backbone edges are
substitutions per site over the parsnp core; within-unit edges are substitutions
per site over that unit's recombination-filtered variable sites. Comparisons
within either level are valid, comparisons across the join are not, and no rate
or date may be derived from this tree at all.

  python3 make_itol_grafted_bp.py

Writes itol_global_strains/. Stdlib only.
"""

import collections
import csv
import os
import re
import sys

B = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, B)
from make_itol_bp import parse_newick, tips_of, prune, to_newick  # noqa: E402

TREE = f"{B}/L1v4c_out/global_grafted_chr1.treefile"
PART = f"{B}/FINAL_BASIS_2026-08-22/FINAL_PARTITION.tsv"
GATE1 = f"{B}/GATE1_ALIGNMENT_2026-08-21.tsv"
NUMBERS = f"{B}/NUMBERS.tsv"
OUTDIR = f"{B}/itol_global_strains"

# Okabe-Ito extended, cycled. 28 strains need more than any one safe palette, so
# the legend carries the mapping and the colours are not asked to be unique.
PALETTE = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00",
           "#F0E442", "#8C564B", "#7570B3", "#1B9E77", "#A6761D", "#666666"]
GATE_COLOR = {"in": "#1b9e77", "below": "#d95f02", "above": "#7570b3"}
GATE_LABEL = {"in": "in-window", "below": "below floor", "above": "above ceiling"}


def strain_of(unit):
    m = re.match(r"(strain_\d+)", unit)
    return m.group(1) if m else unit


def index_tree(root):
    """parent map and leaf sets, computed once."""
    parent, leaves = {}, {}

    def walk(n):
        ls = []
        for c in n.children:
            parent[id(c)] = n
            ls += walk(c)
        if not n.children:
            ls = [n.name]
        leaves[id(n)] = ls
        return ls

    walk(root)
    return parent, leaves


def mrca(nodes_by_tip, parent, a, b):
    seen = set()
    n = nodes_by_tip[a]
    while True:
        seen.add(id(n))
        if id(n) not in parent:
            break
        n = parent[id(n)]
    n = nodes_by_tip[b]
    while id(n) not in seen:
        n = parent[id(n)]
    return n


def main():
    for p in (TREE, PART, GATE1, NUMBERS):
        if not os.path.isfile(p):
            sys.exit(f"FATAL: {p} not found.")

    numbers = {r["key"]: r["value"]
               for r in csv.DictReader(open(NUMBERS), delimiter="\t")}
    exp_units = int(numbers["units.analysed"])
    exp_genomes = int(numbers["genomes.analysed"])

    part = list(csv.DictReader(open(PART), delimiter="\t"))
    g2u = {r["sample_id"]: r["unit"] for r in part}

    root = parse_newick(open(TREE).read())
    all_tips = [t for t in tips_of(root) if t]
    keep = {t for t in all_tips if t in g2u}
    dropped = [t for t in all_tips if t not in g2u]
    print(f"tree tips {len(all_tips)}   frozen genomes {len(g2u)}   "
          f"keeping {len(keep)}")
    if dropped:
        print(f"  pruning {len(dropped)} tip(s) not in the frozen basis")
    if len(keep) != exp_genomes:
        sys.exit(f"FATAL: {len(keep)} tips after pruning, NUMBERS.tsv says "
                 f"genomes.analysed = {exp_genomes}.")

    root = prune(root, keep)
    order = [t for t in tips_of(root) if t]
    units = {g2u[t] for t in order}
    if len(units) != exp_units:
        sys.exit(f"FATAL: {len(units)} units present, NUMBERS.tsv says "
                 f"units.analysed = {exp_units}.")

    parent, leafsets = index_tree(root)
    nodes_by_tip = {}

    def collect(n):
        if not n.children:
            nodes_by_tip[n.name] = n
        for c in n.children:
            collect(c)

    collect(root)

    # maximal contiguous blocks per strain, in tip order
    seq = [strain_of(g2u[t]) for t in order]
    blocks, start = [], 0
    for i in range(1, len(seq) + 1):
        if i == len(seq) or seq[i] != seq[start]:
            blocks.append((seq[start], start, i - 1))
            start = i

    per_strain = collections.Counter(b[0] for b in blocks)
    split = sorted(s for s, k in per_strain.items() if k > 1)
    print(f"\nstrains {len(per_strain)}   contiguous blocks {len(blocks)}")
    if split:
        for s in split:
            sizes = [e - b + 1 for st, b, e in blocks if st == s]
            print(f"  NOT ONE SLICE: {s} falls in {per_strain[s]} blocks, "
                  f"sizes {sizes}")
        print("  Each is emitted as separate ranges sharing one colour.")

    # verify each block is a genuine clade before shading it
    good, bad = [], []
    for s, b, e in blocks:
        want = set(order[b:e + 1])
        node = mrca(nodes_by_tip, parent, order[b], order[e]) if b != e \
            else nodes_by_tip[order[b]]
        got = set(leafsets[id(node)])
        (good if got == want else bad).append((s, b, e, len(got), len(want)))
    print(f"\nblocks that are true clades: {len(good)} of {len(blocks)}")
    for s, b, e, g, w in bad:
        print(f"  REFUSING to shade {s} [{b}:{e}]: MRCA subtends {g} leaves "
              f"but the block is {w}. Shading it would colour other strains.")

    strains = sorted(per_strain, key=lambda s: int(s.split("_")[1]))
    cmap = {s: PALETTE[i % len(PALETTE)] for i, s in enumerate(strains)}
    nseq = collections.Counter(g2u[t] for t in order)

    os.makedirs(OUTDIR, exist_ok=True)
    nwk = f"{OUTDIR}/global_grafted_chr1_frozen.nwk"
    with open(nwk, "w") as fh:
        fh.write(to_newick(root) + ";\n")

    # ---- the shaded slices ----
    with open(f"{OUTDIR}/itol_strain_ranges.txt", "w") as fh:
        fh.write("TREE_COLORS\nSEPARATOR TAB\nDATA\n")
        for s, b, e, *_ in good:
            n = e - b + 1
            fh.write(f"{order[b]}|{order[e]}\trange\t{cmap[s]}\t{s} (n={n})\n")

    # ---- strain legend as a colorstrip, one entry per leaf ----
    with open(f"{OUTDIR}/itol_strain_strip.txt", "w") as fh:
        fh.write("DATASET_COLORSTRIP\nSEPARATOR TAB\n"
                 "DATASET_LABEL\tPopPUNK strain\nCOLOR\t#0072B2\n"
                 "STRIP_WIDTH\t30\nMARGIN\t3\nBORDER_WIDTH\t0\n"
                 "LEGEND_TITLE\tPopPUNK strain\n"
                 "LEGEND_SHAPES\t" + "\t".join("1" for _ in strains) + "\n"
                 "LEGEND_COLORS\t" + "\t".join(cmap[s] for s in strains) + "\n"
                 "LEGEND_LABELS\t" + "\t".join(strains) + "\nDATA\n")
        for t in order:
            s = strain_of(g2u[t])
            fh.write(f"{t}\t{cmap[s]}\t{s}\n")

    # ---- Gate 1 class per leaf, inherited from the genome's unit ----
    gate = {r["unit"]: r["gate1_alignment"]
            for r in csv.DictReader(open(GATE1), delimiter="\t")}
    with open(f"{OUTDIR}/itol_gate1_strip.txt", "w") as fh:
        fh.write("DATASET_COLORSTRIP\nSEPARATOR TAB\n"
                 "DATASET_LABEL\tGate 1 class\nCOLOR\t#1b9e77\n"
                 "STRIP_WIDTH\t30\nMARGIN\t3\nBORDER_WIDTH\t0\n"
                 "LEGEND_TITLE\tGate 1 class\n"
                 "LEGEND_SHAPES\t1\t1\t1\n"
                 "LEGEND_COLORS\t" + "\t".join(
                     GATE_COLOR[k] for k in ("in", "below", "above")) + "\n"
                 "LEGEND_LABELS\t" + "\t".join(
                     GATE_LABEL[k] for k in ("in", "below", "above")) + "\nDATA\n")
        for t in order:
            c = gate.get(g2u[t], "")
            if c in GATE_COLOR:
                fh.write(f"{t}\t{GATE_COLOR[c]}\t{GATE_LABEL[c]}\n")

    # ---- collapse every unit clade, so the tree opens readable ----
    ublocks, ustart = [], 0
    useq = [g2u[t] for t in order]
    for i in range(1, len(useq) + 1):
        if i == len(useq) or useq[i] != useq[ustart]:
            ublocks.append((useq[ustart], ustart, i - 1))
            ustart = i
    with open(f"{OUTDIR}/itol_collapse.txt", "w") as fh:
        fh.write("COLLAPSE\nDATA\n")
        for u, b, e in ublocks:
            if b != e:
                fh.write(f"{order[b]}|{order[e]}\n")
    with open(f"{OUTDIR}/itol_unit_labels.txt", "w") as fh:
        fh.write("LABELS\nSEPARATOR TAB\nDATA\n")
        for u, b, e in ublocks:
            if b != e:
                fh.write(f"{order[b]}|{order[e]}\t{u} (n={nseq[u]})\n")

    readme(nwk, len(keep), len(units), strains, per_strain, split, blocks,
           good, bad, cmap)

    print(f"\nwrote {OUTDIR}/ :")
    for f in sorted(os.listdir(OUTDIR)):
        print(f"  {f}")
    print(f"\n  {len(keep)} genomes, {len(units)} units, {len(strains)} strains")
    print(f"  {len(good)} shaded slices")


def readme(nwk, ngen, nunit, strains, per_strain, split, blocks, good, bad, cmap):
    with open(f"{OUTDIR}/README.md", "w") as fh:
        fh.write(f"""# iTOL: the global genome-level tree, sliced by strain

Generated by `make_itol_grafted_bp.py`. Do not edit; regenerate.

**{ngen} genomes, {nunit} units, {len(strains)} PopPUNK strains**, matching
`genomes.analysed` and `units.analysed` in `NUMBERS.tsv`. The source treefile
carries 2,352 tips on the 86-unit basis; the extras are pruned and the script
refuses to write if the remainder does not match the frozen basis.

## Load order

1. Upload **`{os.path.basename(nwk)}`**.
2. Drag the `itol_*.txt` files on. Start with `itol_collapse.txt` and
   `itol_unit_labels.txt`, then add the slices.

| file | dataset | shows |
|---|---|---|
| `itol_strain_ranges.txt` | TREE_COLORS range | **the shaded strain slices** |
| `itol_strain_strip.txt` | COLORSTRIP | strain per leaf, with the full legend |
| `itol_gate1_strip.txt` | COLORSTRIP | Gate 1 class, inherited from each genome's unit |
| `itol_collapse.txt` | COLLAPSE | collapses all {nunit} unit clades |
| `itol_unit_labels.txt` | LABELS | unit name and size on each collapsed clade |

Keep branch lengths **on** and the units **collapsed** for the overview.

## What the slices are, and what was refused

A slice is an iTOL `range`, which shades the clade under the MRCA of two leaves.
Contiguity in tip order is **not** monophyly, so each candidate slice is checked:
the MRCA's leaf set must equal the block exactly. {len(good)} of {len(blocks)}
blocks passed and were written.

""")
        if split:
            fh.write("**Strains that are not one slice.** Shading these as a "
                     "single range would have drawn a wedge across other "
                     "strains:\n\n")
            for s in split:
                sizes = [e - b + 1 for st, b, e in blocks if st == s]
                fh.write(f"- `{s}` falls in {per_strain[s]} separate blocks "
                         f"of {', '.join(str(x) for x in sizes)} genomes. "
                         f"Emitted as {per_strain[s]} ranges sharing one "
                         f"colour and one legend entry.\n")
            fh.write("\n")
        if bad:
            fh.write("**Blocks refused.** The MRCA subtended leaves outside "
                     "the block, so no range was written:\n\n")
            for s, b, e, g, w in bad:
                fh.write(f"- `{s}` block of {w} leaves: MRCA subtends {g}.\n")
            fh.write("\n")
        fh.write(f"""## What this tree does not support

**Two branch-length scales are spliced together.** Backbone edges are
substitutions per site over the parsnp core; within-unit edges are substitutions
per site over that unit's recombination-filtered variable sites. Comparisons
*within* either level are valid. Comparisons *across* the join are not, and **no
rate, date or r/m may be derived from this tree.**

**It is unrooted**, so no unit or strain is ancestral because of where it sits.

**Strain membership came from PopPUNK on the whole panel, not from this tree.**
The slices are an annotation laid over the topology afterwards. That they mostly
coincide with clades is a result; it was not imposed.

## Strain colours

| strain | units | colour |
|---|---|---|
""")
        for s in strains:
            fh.write(f"| {s} | {per_strain[s]} block(s) | `{cmap[s]}` |\n")


if __name__ == "__main__":
    main()
