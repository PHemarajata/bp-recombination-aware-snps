#!/usr/bin/env python3
"""Figure 2 -- the Gate 1 detection window, generated so it cannot go stale.

The paper's central claim is that r/m is a MEASUREMENT inside a bounded range of
population diversity and a DETECTION FAILURE outside it. This figure is that
claim: r/m against mean pairwise core SNPs, with the window shaded, on the
frozen basis.

Read the shape, not just the points. Inside the window r/m is high and scattered,
which is what a real measurement of a recombinogenic species looks like. Outside
it, on BOTH sides, r/m collapses toward zero. A low r/m here is therefore not a
clonal lineage; it is Gubbins failing to detect, and it fails at both extremes for
different reasons -- too little diversity to place a recombination block below the
floor, too much for the clonal frame to be recovered above the ceiling.

SAFETY. Like make_figure1_bp.py this reads a canonical source and exits non-zero
rather than emitting a figure it cannot stand behind. It goes further: it
recomputes the headline from the per-unit table and ABORTS if that disagrees with
NUMBERS.tsv. A figure that silently disagrees with the manuscript's own numbers
table is worse than no figure.

  python3 make_figure2_bp.py           # FIGURE2_GATE1_WINDOW.svg
  python3 make_figure2_bp.py --dark    # screen/slide variant
"""
import csv
import os
import statistics as st
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

B = os.path.dirname(os.path.abspath(__file__))
GATE1 = f"{B}/GATE1_ALIGNMENT_2026-08-21.tsv"
NUMBERS = f"{B}/NUMBERS.tsv"
DARK = "--dark" in sys.argv
OUT = f"{B}/FIGURE2_GATE1_WINDOW{'_dark' if DARK else ''}.svg"

# The reported alignment-derived window. These are the relocated bounds, not the
# ska-unit (1270, 4671) pair -- see gate1_from_alignment_bp.py, where using the
# wrong one silently reported 39 in-window units at 8.05 instead of 47 at 7.70.
FLOOR, CEIL = 700.0, 4700.0

for p in (GATE1, NUMBERS):
    if not os.path.isfile(p):
        sys.exit(f"FATAL: {p} not found.")

N = {r["key"]: r["value"] for r in csv.DictReader(open(NUMBERS), delimiter="\t")}


def need(key):
    if key not in N:
        sys.exit(f"FATAL: NUMBERS.tsv has no key {key!r}. Run generate_numbers.py.")
    return N[key]


rows = []
for r in csv.DictReader(open(GATE1), delimiter="\t"):
    if not r["rm_corrected"] or not r["aln_mean_pairwise_snps"]:
        continue
    rows.append({
        "unit": r["unit"],
        "x": float(r["aln_mean_pairwise_snps"]),
        "y": float(r["rm_corrected"]),
        "k": r["gate1_alignment"],
    })
if not rows:
    sys.exit("FATAL: no usable rows in the Gate 1 table.")

strata = {k: [r for r in rows if r["k"] == k] for k in ("below", "in", "above")}
med = {k: st.median([r["y"] for r in v]) for k, v in strata.items() if v}
outside = [r["y"] for r in rows if r["k"] != "in"]

# ---- refuse to draw a figure that disagrees with NUMBERS.tsv ----------------
exp_units, exp_med = int(need("rm.gate1_units")), float(need("rm.median_gate1"))
exp_out = float(need("rm.median_outside_gate1"))
got_units, got_med, got_out = len(strata["in"]), med["in"], st.median(outside)
problems = []
if got_units != exp_units:
    problems.append(f"in-window units: figure {got_units}, NUMBERS.tsv {exp_units}")
if abs(got_med - exp_med) > 0.005:
    problems.append(f"median r/m: figure {got_med:.2f}, NUMBERS.tsv {exp_med:.2f}")
if abs(got_out - exp_out) > 0.005:
    problems.append(f"outside median: figure {got_out:.2f}, NUMBERS.tsv {exp_out:.2f}")
if problems:
    sys.exit("FATAL: the figure disagrees with NUMBERS.tsv.\n  "
             + "\n  ".join(problems)
             + "\nOne of them is stale. Do not publish either until they agree.")

# ---- palette ---------------------------------------------------------------
if DARK:
    bg, fg, muted, grid = "#0C1413", "#E7F0EE", "#8B9E9B", "#273634"
    band, c_in, c_out = "#1C3A38", "#4CB8B1", "#D6A442"
else:
    bg, fg, muted, grid = "#FFFFFF", "#131E1D", "#5C6E6B", "#DCE4E3"
    band, c_in, c_out = "#DCEDEB", "#0E6E6B", "#96650A"

fig, ax = plt.subplots(figsize=(8.4, 5.4))
fig.patch.set_facecolor(bg)
ax.set_facecolor(bg)

ax.axvspan(FLOOR, CEIL, color=band, zorder=0,
           label=f"Gate 1 window [{FLOOR:.0f}, {CEIL:.0f}]")
for xv in (FLOOR, CEIL):
    ax.axvline(xv, color=c_in, lw=1.0, ls="--", alpha=.8, zorder=1)

for k, mk in (("below", "v"), ("above", "^"), ("in", "o")):
    v = strata.get(k) or []
    if not v:
        continue
    ax.scatter([r["x"] for r in v], [r["y"] for r in v],
               s=46 if k == "in" else 34, marker=mk,
               c=c_in if k == "in" else c_out,
               alpha=.9 if k == "in" else .75,
               edgecolors=bg, linewidths=.6, zorder=3)

ax.hlines(med["in"], FLOOR, CEIL, color=c_in, lw=2.0, zorder=4)
ax.text(CEIL * .96, med["in"] * 1.09, f"median {med['in']:.2f}",
        ha="right", va="bottom", color=c_in, fontsize=10.5, fontweight="bold")
for k, x0, x1 in (("below", ax.get_xlim()[0], FLOOR), ("above", CEIL, None)):
    if k in med:
        ax.hlines(med[k], x0 if x1 else CEIL, x1 or ax.get_xlim()[1],
                  color=c_out, lw=1.6, zorder=4)

ax.set_xscale("log")
ax.set_xlabel("Mean pairwise core SNPs per unit  (log scale)", color=fg, fontsize=11.5)
ax.set_ylabel("r/m  (recombination-derived : mutation-derived substitutions)",
              color=fg, fontsize=11.5)
ax.set_title("Recombination is measurable only inside a bounded range of diversity",
             color=fg, fontsize=13.5, fontweight="bold", pad=14, loc="left")
ax.tick_params(colors=muted, labelsize=10)
for s in ax.spines.values():
    s.set_color(grid)
ax.grid(True, which="both", color=grid, lw=.6, alpha=.7, zorder=0)
ax.set_axisbelow(True)

handles = [
    plt.Rectangle((0, 0), 1, 1, fc=band, ec=c_in, ls="--",
                  label=f"Gate 1 window [{FLOOR:.0f}, {CEIL:.0f}] SNPs"),
    Line2D([], [], ls="", marker="o", ms=7, c=c_in,
           label=f"in-window, n={len(strata['in'])}, median r/m {med['in']:.2f}"),
    Line2D([], [], ls="", marker="v", ms=6.5, c=c_out,
           label=f"below floor, n={len(strata['below'])}, median {med['below']:.2f}"),
    Line2D([], [], ls="", marker="^", ms=6.5, c=c_out,
           label=f"above ceiling, n={len(strata['above'])}, median {med['above']:.2f}"),
]
leg = ax.legend(handles=handles, loc="upper left", frameon=True, fontsize=9.5)
leg.get_frame().set_facecolor(bg)
leg.get_frame().set_edgecolor(grid)
for t in leg.get_texts():
    t.set_color(fg)

ax.text(0.5, -0.165,
        f"{len(rows)} units, frozen basis (FINAL_BASIS_2026-08-22). "
        f"Outside the window r/m collapses to a median of {st.median(outside):.2f}: "
        "a detection failure, not a clonal population.",
        transform=ax.transAxes, ha="center", va="top", color=muted, fontsize=9.5)

fig.tight_layout()
fig.savefig(OUT, format="svg", facecolor=bg, bbox_inches="tight")
print(f"wrote {OUT}")
print(f"  {len(rows)} units: {len(strata['in'])} in, "
      f"{len(strata['below'])} below, {len(strata['above'])} above")
print(f"  median r/m in-window {med['in']:.2f}, outside {st.median(outside):.2f}")
print("  cross-checked against NUMBERS.tsv: agrees")
