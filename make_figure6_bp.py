#!/usr/bin/env python3
"""
Figure 6 -- the global genome-level tree, with the PopPUNK strains as shaded
slices.

Figure 3 is 85 tips, one per unit, and answers "how do the units relate". This is
the other view: **all 2,340 analysed genomes**, with the 28 strains shaded, and
it answers "what does the collection look like". The units are the analysis
objects; the strains are the thing a reader recognises.

IT IS DRAWN AS A CLADOGRAM, ON PURPOSE. The grafted tree splices two branch-length
scales: backbone edges are substitutions per site over the parsnp core, within-unit
edges are substitutions per site over that unit's recombination-filtered variable
sites, and the two differ by roughly 133-fold. Plotting those radially would put
almost all visible length in the backbone and compress every unit to a dot, while
implying the distances are comparable. They are not. Topology is what this figure
is for, so branch lengths are dropped and the caption says so, rather than being
drawn and quietly disclaimed.

A SLICE IS ONLY DRAWN WHERE IT IS A REAL CLADE. Contiguity in tip order is not
monophyly. Each candidate slice is checked against the MRCA's leaf set and
refused if it does not match, on the same rule and with the same result as
`make_itol_grafted_bp.py`: strain_1 occupies three blocks rather than one, and
one of those three is not a clade and is left unshaded.

  python3 make_figure6_bp.py           # FIGURE6_GLOBAL_STRAIN_TREE.svg
  python3 make_figure6_bp.py --dark

Needs matplotlib.
"""

import collections
import csv
import math
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Wedge

B = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, B)
from make_itol_bp import parse_newick, tips_of, prune  # noqa: E402

TREE = f"{B}/L1v4c_out/global_grafted_chr1.treefile"
PART = f"{B}/FINAL_BASIS_2026-08-22/FINAL_PARTITION.tsv"
NUMBERS = f"{B}/NUMBERS.tsv"
DARK = "--dark" in sys.argv
OUT = f"{B}/FIGURE6_GLOBAL_STRAIN_TREE{'_dark' if DARK else ''}.svg"

PALETTE = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00",
           "#F0E442", "#8C564B", "#7570B3", "#1B9E77", "#A6761D", "#666666"]
SPAN = 352.0          # degrees of circle used, leaving a gap at the top
START = 94.0          # where the first tip sits


def strain_of(u):
    m = re.match(r"(strain_\d+)", u)
    return m.group(1) if m else u


def main():
    for p in (TREE, PART, NUMBERS):
        if not os.path.isfile(p):
            sys.exit(f"FATAL: {p} not found.")
    numbers = {r["key"]: r["value"]
               for r in csv.DictReader(open(NUMBERS), delimiter="\t")}
    exp_g = int(numbers["genomes.analysed"])
    exp_u = int(numbers["units.analysed"])

    g2u = {r["sample_id"]: r["unit"]
           for r in csv.DictReader(open(PART), delimiter="\t")}
    root = parse_newick(open(TREE).read())
    keep = {t for t in tips_of(root) if t in g2u}
    if len(keep) != exp_g:
        sys.exit(f"FATAL: {len(keep)} tips kept, NUMBERS.tsv says {exp_g}.")
    root = prune(root, keep)
    order = [t for t in tips_of(root) if t]
    units = {g2u[t] for t in order}
    if len(units) != exp_u:
        sys.exit(f"FATAL: {len(units)} units, NUMBERS.tsv says {exp_u}.")
    print(f"{len(order)} genomes, {len(units)} units")

    # ---- cladogram geometry -------------------------------------------------
    height, parent, leafset = {}, {}, {}

    def h(n):
        if not n.children:
            height[id(n)] = 0
            leafset[id(n)] = {n.name}
            return 0, {n.name}
        best, ls = 0, set()
        for c in n.children:
            parent[id(c)] = n
            hh, l = h(c)
            best = max(best, hh + 1)
            ls |= l
        height[id(n)], leafset[id(n)] = best, ls
        return best, ls

    H, _ = h(root)
    idx = {t: i for i, t in enumerate(order)}
    step = SPAN / max(1, len(order))

    ang, rad = {}, {}

    def place(n):
        rad[id(n)] = 1.0 - height[id(n)] / H
        if not n.children:
            ang[id(n)] = START + idx[n.name] * step
            return ang[id(n)]
        a = [place(c) for c in n.children]
        ang[id(n)] = (min(a) + max(a)) / 2.0
        return ang[id(n)]

    place(root)

    def xy(a, r):
        t = math.radians(a)
        return r * math.cos(t), r * math.sin(t)

    segs = []

    def draw(n):
        for c in n.children:
            a = ang[id(c)]
            segs.append([xy(a, rad[id(n)]), xy(a, rad[id(c)])])
        if n.children:
            lo = min(ang[id(c)] for c in n.children)
            hi = max(ang[id(c)] for c in n.children)
            r = rad[id(n)]
            k = max(2, int((hi - lo) / 1.5) + 2)
            pts = [xy(lo + (hi - lo) * i / (k - 1), r) for i in range(k)]
            # .extend, not '+=': augmented assignment would rebind `segs` as a
            # local of draw() and break the .append above it.
            segs.extend([[pts[i], pts[i + 1]] for i in range(k - 1)])
        for c in n.children:
            draw(c)

    draw(root)

    # ---- strain blocks, checked for monophyly -------------------------------
    seq = [strain_of(g2u[t]) for t in order]
    blocks, s0 = [], 0
    for i in range(1, len(seq) + 1):
        if i == len(seq) or seq[i] != seq[s0]:
            blocks.append((seq[s0], s0, i - 1))
            s0 = i
    nodes_by_tip = {}

    def collect(n):
        if not n.children:
            nodes_by_tip[n.name] = n
        for c in n.children:
            collect(c)

    collect(root)

    def mrca(a, b):
        seen, n = set(), nodes_by_tip[a]
        while True:
            seen.add(id(n))
            if id(n) not in parent:
                break
            n = parent[id(n)]
        n = nodes_by_tip[b]
        while id(n) not in seen:
            n = parent[id(n)]
        return n

    good, refused = [], []
    for s, b, e in blocks:
        want = set(order[b:e + 1])
        node = nodes_by_tip[order[b]] if b == e else mrca(order[b], order[e])
        (good if leafset[id(node)] == want else refused).append((s, b, e))
    per = collections.Counter(s for s, _, _ in blocks)
    split = sorted({s for s in per if per[s] > 1})
    print(f"{len(blocks)} blocks over {len(per)} strains; "
          f"{len(good)} are clades, {len(refused)} refused")
    for s, b, e in refused:
        print(f"  unshaded: {s} block of {e-b+1} genomes is not a clade")

    strains = sorted(per, key=lambda s: int(s.split("_")[1]))
    cmap = {s: PALETTE[i % len(PALETTE)] for i, s in enumerate(strains)}

    # ---- draw ---------------------------------------------------------------
    fg = "#e8e8e8" if DARK else "#1a1a1a"
    bg = "#111111" if DARK else "#ffffff"
    tree_c = "#c8c8c8" if DARK else "#555555"

    fig, ax = plt.subplots(figsize=(12.6, 12.6), facecolor=bg)
    ax.set_facecolor(bg)
    ax.set_aspect("equal")
    ax.axis("off")

    for s, b, e in good:
        a0, a1 = START + b * step, START + (e + 1) * step
        ax.add_patch(Wedge((0, 0), 1.02, a0, a1, width=1.02,
                           facecolor=cmap[s], alpha=0.16, lw=0, zorder=0))
        ax.add_patch(Wedge((0, 0), 1.10, a0, a1, width=0.055,
                           facecolor=cmap[s], alpha=0.95, lw=0, zorder=4))
    for s, b, e in refused:
        a0, a1 = START + b * step, START + (e + 1) * step
        ax.add_patch(Wedge((0, 0), 1.10, a0, a1, width=0.055, facecolor="none",
                           edgecolor=cmap[s], lw=1.1, ls=(0, (2, 2)), zorder=4))

    ax.add_collection(LineCollection(segs, colors=tree_c, linewidths=0.30,
                                     zorder=2, alpha=0.9))

    for s, b, e in good + refused:
        n = e - b + 1
        if n < 45:
            continue
        a = START + (b + e + 1) / 2 * step
        x, y = xy(a, 1.20)
        rot = a % 360
        if 90 < rot < 270:
            rot -= 180
        ax.text(x, y, s.replace("strain_", "S"), color=fg, fontsize=7.6,
                ha="center", va="center", rotation=rot,
                rotation_mode="anchor", zorder=5)

    ax.set_xlim(-1.34, 1.34)
    ax.set_ylim(-1.34, 1.34)

    ax.text(0, 0.07, f"{len(order):,}", color=fg, fontsize=17, ha="center",
            va="center", weight="bold")
    ax.text(0, -0.015, "genomes", color=fg, fontsize=9, ha="center", va="center")
    ax.text(0, -0.075, f"{len(units)} units · {len(strains)} strains",
            color=fg, fontsize=8, ha="center", va="center", alpha=0.85)

    fig.suptitle("The analysed collection, by PopPUNK strain",
                 color=fg, fontsize=14, y=0.95)
    note = (f"Grafted genome-level tree, all {len(order):,} analysed genomes, "
            f"{len(units)} units in {len(strains)} strains. Shaded slices are "
            f"strains.\n"
            f"CLADOGRAM: branch lengths are NOT drawn. The tree splices two "
            f"scales (backbone vs within-unit, ~133x), so radial distance "
            f"would be meaningless. No rate, date or r/m may be derived from "
            f"it, and it is unrooted.\n"
            f"{len(good)} of {len(blocks)} strain blocks are true clades and "
            f"are shaded; ")
    if split:
        note += (f"strain_1 occupies {per['strain_1']} separate blocks rather "
                 f"than one; ")
    note += (f"{len(refused)} block(s) whose MRCA subtends other strains are "
             f"outlined, not filled.\n"
             f"Strain membership came from PopPUNK on the whole panel and was "
             f"not derived from this tree.")
    fig.text(0.5, 0.055, note, color=fg, fontsize=8.1, ha="center", va="top")

    fig.savefig(OUT, facecolor=bg, bbox_inches="tight")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
