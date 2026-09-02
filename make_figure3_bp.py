#!/usr/bin/env python3
"""Figure 3 -- the global maximum-likelihood tree over unit medoids.

One tip per analysis unit, annotated by dominant country and Gate 1 class, on the
frozen basis.

WHAT THIS FIGURE IS FOR. It shows that the partition is not an artifact of the
clustering: the tree recovers known *B. pseudomallei* biogeography without
geography being an input to PopPUNK, fastbaps or IQ-TREE at any stage. The two
most divergent units in the collection, by terminal branch length, are
strain_9_L1_1 (92% Australia) and strain_15_L1_1 (100% Australia), and they sit
on the two single-tip arms of the root trifurcation with the other 83 units
between them. That is consistent with the established view that Australia
harbours the ancestral population.

THE TREE IS UNROOTED, and the claim above is phrased to survive that. IQ-TREE was
run without an outgroup (`-o`), so the root is a trifurcation and NOTHING here is
"basal" in a rooted sense. An earlier draft of this script said Australia falls
basal and that the deepest internal branch separates it; both were wrong. The
longest internal branch is in fact the strain_8 clade at 0.094, while
strain_9_L1_1 and strain_15_L1_1 have the longest TERMINAL branches at 0.149 and
0.145. Divergence is what the data supports; ancestry is not.

WHAT IT IS NOT FOR, AND THE CAPTION MUST SAY SO. This tree is NOT
recombination-corrected. It is built from a core alignment over unit medoids, so
its branch lengths carry recombination as well as mutation. **No r/m, no rate and
no date may be derived from it.** Those come from the per-unit Gubbins runs, and
the reason this project keeps a Gate 1 window at all is that recombination
signal is not uniformly recoverable across this tree.

SAFETY. Follows make_figure2_bp.py: reads canonical sources, and refuses to draw
if the unit set disagrees with NUMBERS.tsv.

  python3 make_figure3_bp.py           # FIGURE3_GLOBAL_ML_TREE.svg
  python3 make_figure3_bp.py --dark
"""
import collections
import csv
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

B = os.path.dirname(os.path.abspath(__file__))
TREE = f"{B}/L1v4c_out/global_ml_tree.treefile"
PANEL = f"{B}/FINAL_BASIS_2026-08-22/FINAL_PANEL.tsv"
GATE1 = f"{B}/GATE1_ALIGNMENT_2026-08-21.tsv"
NUMBERS = f"{B}/NUMBERS.tsv"
DARK = "--dark" in sys.argv
OUT = f"{B}/FIGURE3_GLOBAL_ML_TREE{'_dark' if DARK else ''}.svg"

for p in (TREE, PANEL, GATE1, NUMBERS):
    if not os.path.isfile(p):
        sys.exit(f"FATAL: {p} not found.")

N = {r["key"]: r["value"] for r in csv.DictReader(open(NUMBERS), delimiter="\t")}


def need(k):
    if k not in N:
        sys.exit(f"FATAL: NUMBERS.tsv has no key {k!r}. Run generate_numbers.py.")
    return N[k]


# ---- newick, keeping branch lengths -----------------------------------------
def parse_newick(s):
    """(children, label, length). The parser in phylogeography_association_bp.py
    discards lengths; this figure needs them, so it is not reused."""
    s = s.strip().rstrip(";")
    pos = [0]

    def node():
        ch = []
        if pos[0] < len(s) and s[pos[0]] == "(":
            pos[0] += 1
            while True:
                ch.append(node())
                if pos[0] < len(s) and s[pos[0]] == ",":
                    pos[0] += 1
                    continue
                if pos[0] < len(s) and s[pos[0]] == ")":
                    pos[0] += 1
                break
        st = pos[0]
        while pos[0] < len(s) and s[pos[0]] not in "(),":
            pos[0] += 1
        tok = s[st:pos[0]]
        lab, _, ln = tok.partition(":")
        try:
            length = float(ln) if ln else 0.0
        except ValueError:
            length = 0.0
        return [ch, lab.strip().strip("'\""), length]

    return node()


def tips_of(n):
    return [n[1]] if not n[0] else [t for c in n[0] for t in tips_of(c)]


tree = parse_newick(open(TREE).read())
tree_tips = [t for t in tips_of(tree) if t]

# ---- frozen basis: membership, dominant country ------------------------------
members = collections.defaultdict(list)
for r in csv.DictReader(open(PANEL), delimiter="\t"):
    if r["basis_role"] == "analysis" and r["unit_membership"]:
        members[r["unit_membership"]].append((r["country"] or "").strip())
basis_units = set(members)

dominant, share = {}, {}
for u, cs in members.items():
    known = [c for c in cs if c and c.lower() not in ("na", "unknown")]
    if known:
        c, k = collections.Counter(known).most_common(1)[0]
        dominant[u], share[u] = c, k / len(known)
    else:
        dominant[u], share[u] = "unknown", 0.0

gate = {r["unit"]: r["gate1_alignment"]
        for r in csv.DictReader(open(GATE1), delimiter="\t")}

# ---- refuse to draw a tree that is not the frozen basis ----------------------
exp_units = int(need("units.analysed"))
drop = [t for t in tree_tips if t not in basis_units]
keep = [t for t in tree_tips if t in basis_units]
missing = sorted(basis_units - set(tree_tips))
if len(basis_units) != exp_units:
    sys.exit(f"FATAL: panel has {len(basis_units)} units, NUMBERS.tsv says "
             f"{exp_units}. One is stale.")
if missing:
    sys.exit("FATAL: the frozen basis has units with no tip in the tree: "
             + ", ".join(missing) +
             "\nThe tree predates the basis. Rebuild it before publishing.")
print(f"tree tips: {len(tree_tips)}   frozen basis: {len(basis_units)}")
if drop:
    print(f"  pruning {len(drop)} tip(s) not in the frozen basis: {', '.join(sorted(drop))}")


# ---- prune to the basis, then lay out ----------------------------------------
def prune(n):
    if not n[0]:
        return n if n[1] in basis_units else None
    kids = [k for k in (prune(c) for c in n[0]) if k]
    if not kids:
        return None
    if len(kids) == 1:                      # collapse, preserving path length
        kids[0][2] += n[2]
        return kids[0]
    return [kids, n[1], n[2]]


tree = prune(tree)
ordered = tips_of(tree)
ypos = {t: i for i, t in enumerate(ordered)}


def layout(n, x0, seg):
    x = x0 + n[2]
    if not n[0]:
        y = ypos[n[1]]
    else:
        ys = [layout(c, x, seg) for c in n[0]]
        y = (min(ys) + max(ys)) / 2.0
        seg.append(("v", x, min(ys), max(ys)))
    seg.append(("h", x0, x, y))
    return y


segs = []
layout(tree, 0.0, segs)

# ---- palette -----------------------------------------------------------------
if DARK:
    bg, fg, muted, grid = "#0C1413", "#E7F0EE", "#8B9E9B", "#3A4D4A"
    cls_c = {"in": "#4CB8B1", "below": "#D6A442", "above": "#E27C6F"}
else:
    bg, fg, muted, grid = "#FFFFFF", "#131E1D", "#5C6E6B", "#7C8E8B"
    cls_c = {"in": "#0E6E6B", "below": "#96650A", "above": "#9C3227"}

fig, ax = plt.subplots(figsize=(9.6, 13.2))
fig.patch.set_facecolor(bg)
ax.set_facecolor(bg)

for s in segs:
    if s[0] == "h":
        ax.plot([s[1], s[2]], [s[3], s[3]], color=grid, lw=1.0, zorder=2)
    else:
        ax.plot([s[1], s[1]], [s[2], s[3]], color=grid, lw=1.0, zorder=2)

xmax = max(s[2] for s in segs if s[0] == "h")
tipx = {}


def collect(n, x0):
    x = x0 + n[2]
    if not n[0]:
        tipx[n[1]] = x
    for c in n[0]:
        collect(c, x)


collect(tree, 0.0)

for t in ordered:
    k = gate.get(t, "")
    ax.scatter([tipx[t]], [ypos[t]], s=34, zorder=4,
               c=cls_c.get(k, muted), edgecolors=bg, linewidths=.6)
    ax.text(xmax * 1.035, ypos[t],
            f"{t}  ·  {dominant[t]} ({share[t]*100:.0f}%)",
            va="center", ha="left", fontsize=7.4, color=fg)

ax.set_xlim(-xmax * .02, xmax * 1.5)
ax.set_ylim(-1, len(ordered))
ax.axis("off")
ax.set_title("The two most divergent units are both Australian,\n"
             "and geography was never an input to the partition",
             color=fg, fontsize=14, fontweight="bold", loc="left", pad=16)

handles = [Line2D([], [], ls="", marker="o", ms=7, c=cls_c["in"],
                  label="Gate 1: in-window (r/m is a measurement)"),
           Line2D([], [], ls="", marker="o", ms=7, c=cls_c["below"],
                  label="below floor (detection failure)"),
           Line2D([], [], ls="", marker="o", ms=7, c=cls_c["above"],
                  label="above ceiling (detection failure)")]
leg = ax.legend(handles=handles, loc="lower right", frameon=True, fontsize=9)
leg.get_frame().set_facecolor(bg)
leg.get_frame().set_edgecolor(grid)
for t in leg.get_texts():
    t.set_color(fg)

ax.text(0, -0.045,
        f"{len(ordered)} analysis units, one tip per unit medoid, frozen basis "
        f"(FINAL_BASIS_2026-08-22). Tip labels give the dominant country and its "
        f"share.\nNOT RECOMBINATION-CORRECTED: branch lengths carry recombination "
        f"as well as mutation. No r/m, rate or date may be derived from this tree.",
        transform=ax.transAxes, ha="left", va="top", color=muted, fontsize=8.8)

fig.tight_layout()
fig.savefig(OUT, format="svg", facecolor=bg, bbox_inches="tight")
print(f"wrote {OUT}")
print(f"  {len(ordered)} tips drawn; "
      f"{sum(1 for t in ordered if gate.get(t)=='in')} in-window")
print(f"  most divergent tips sit on the trifurcation arms; tree is UNROOTED")
