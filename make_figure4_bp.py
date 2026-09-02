#!/usr/bin/env python3
"""Figure 4 -- geography against its own confounder, per unit.

The confounder control in one panel. Each point is an analysis unit, plotted by
its permutation p-value for COUNTRY against the same test on the same tree with
the same machinery for BIOPROJECT.

WHY THIS COMPARISON AND NOT A SIGNIFICANCE TEST. In this collection a BioProject
is typically one study, one lab, one country, often one outbreak. Country and
BioProject are largely the same variable wearing different labels, so a country
signal that is no stronger than the BioProject signal is not evidence of
phylogeography -- it is evidence that related isolates get sequenced together.
The diagonal is the honest null: points on it have no geographic signal beyond
batch. Only the lower-right region, where country is significant and BioProject
is not, is geography.

WHAT THIS FIGURE IS FOR, BLUNTLY. It exists so the scope decision on the
geography paper is made looking at the evidence rather than at a summary
sentence. Of 85 units: 37 cannot be tested at all (single-valued country), 25 are
null, 12 are confounded, 5 have a vacuous control, and **6 pass**. The 37
untestable units are the ones sometimes quoted as "single-country" evidence; they
are the stratum where the question could not be asked, and 30 of the 37 are
Thailand against Thailand being 67% of the collection.

SAFETY. Reads the frozen association table and refuses to draw if its
interpretation counts disagree with what this docstring claims.

  python3 make_figure4_bp.py           # FIGURE4_CONFOUNDER_CONTROL.svg
  python3 make_figure4_bp.py --dark
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
ASSOC = f"{B}/PHYLOGEOGRAPHY_ASSOCIATION_FROZEN_2026-08-23.tsv"
DARK = "--dark" in sys.argv
OUT = f"{B}/FIGURE4_CONFOUNDER_CONTROL{'_dark' if DARK else ''}.svg"
ALPHA = 0.05

if not os.path.isfile(ASSOC):
    sys.exit(f"FATAL: {ASSOC} not found.")

by = collections.defaultdict(dict)
for r in csv.DictReader(open(ASSOC), delimiter="\t"):
    by[r["unit"]][r["variable"]] = r

interp = collections.Counter(
    d["country"].get("interpretation", "") for d in by.values() if "country" in d)
EXPECT = {"untestable: single-valued": 37, "null": 25, "confounded": 12,
          "geographic (control passes)": 6, "vacuous control": 5}
bad = [f"{k}: table {interp.get(k, 0)}, expected {v}"
       for k, v in EXPECT.items() if interp.get(k, 0) != v]
if len(by) != 85:
    bad.append(f"units: table {len(by)}, expected 85")
if bad:
    sys.exit("FATAL: the association table is not the one this figure describes.\n  "
             + "\n  ".join(bad)
             + "\nEither the table changed or this figure's text is stale.")

pts, floor = [], 1.0
for u, d in by.items():
    c, b = d.get("country", {}), d.get("bioproject", {})
    try:
        pc, pb = float(c.get("p_value") or ""), float(b.get("p_value") or "")
    except ValueError:
        continue
    pts.append((u, pc, pb, c.get("interpretation", "")))
    floor = min(floor, pc or 1, pb or 1)
lo = max(floor, 1e-4) / 2.0
for i, (u, pc, pb, k) in enumerate(pts):
    pts[i] = (u, max(pc, lo), max(pb, lo), k)

if DARK:
    bg, fg, muted, grid = "#0C1413", "#E7F0EE", "#8B9E9B", "#273634"
    c_pass, c_conf, c_null, c_vac = "#4CB8B1", "#E27C6F", "#8B9E9B", "#D6A442"
else:
    bg, fg, muted, grid = "#FFFFFF", "#131E1D", "#5C6E6B", "#DCE4E3"
    c_pass, c_conf, c_null, c_vac = "#0E6E6B", "#9C3227", "#8797A9", "#96650A"
col = {"geographic (control passes)": c_pass, "confounded": c_conf,
       "null": c_null, "vacuous control": c_vac}

fig, ax = plt.subplots(figsize=(7.8, 7.0))
fig.patch.set_facecolor(bg); ax.set_facecolor(bg)

ax.fill_between([lo, ALPHA], ALPHA, 1.0, color=c_pass, alpha=.10, zorder=0)
ax.plot([lo, 1], [lo, 1], color=muted, lw=1.0, ls=":", zorder=1)
ax.axvline(ALPHA, color=muted, lw=.9, ls="--", zorder=1)
ax.axhline(ALPHA, color=muted, lw=.9, ls="--", zorder=1)

for k in ("null", "vacuous control", "confounded", "geographic (control passes)"):
    v = [p for p in pts if p[3] == k]
    if not v:
        continue
    passing = k.startswith("geographic")
    ax.scatter([p[1] for p in v], [p[2] for p in v],
               s=86 if passing else 44, c=col[k], zorder=4 if passing else 3,
               alpha=.95 if passing else .72,
               edgecolors=bg if passing else "none", linewidths=.9)

for u, pc, pb, k in pts:
    if k.startswith("geographic"):
        ax.annotate(u, (pc, pb), textcoords="offset points", xytext=(7, 4),
                    fontsize=7.6, color=fg)

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(lo, 1.35); ax.set_ylim(lo, 1.35)
ax.set_xlabel("COUNTRY  permutation p-value  (log)", color=fg, fontsize=11.5)
ax.set_ylabel("BIOPROJECT  permutation p-value  (log)", color=fg, fontsize=11.5)
ax.set_title("Only 6 of 85 units show geography that survives its confounder",
             color=fg, fontsize=13.5, fontweight="bold", loc="left", pad=14)
ax.tick_params(colors=muted, labelsize=10)
for s in ax.spines.values():
    s.set_color(grid)
ax.grid(True, which="major", color=grid, lw=.6, alpha=.6, zorder=0)
ax.set_axisbelow(True)

ax.text(lo * 1.25, .78, "geography survives\nthe control",
        fontsize=9.5, color=c_pass, fontweight="bold", va="top")
ax.text(.30, lo * 1.6, "batch explains it\nas well or better",
        fontsize=9.5, color=muted, va="bottom")

handles = [Line2D([], [], ls="", marker="o", ms=9, c=c_pass,
                  label=f"geographic, control passes  ({EXPECT['geographic (control passes)']})"),
           Line2D([], [], ls="", marker="o", ms=7, c=c_conf,
                  label=f"confounded by BioProject  ({EXPECT['confounded']})"),
           Line2D([], [], ls="", marker="o", ms=7, c=c_null,
                  label=f"no signal  ({EXPECT['null']})"),
           Line2D([], [], ls="", marker="o", ms=7, c=c_vac,
                  label=f"vacuous control  ({EXPECT['vacuous control']})"),
           Line2D([], [], ls=":", c=muted, label="equal signal (the honest null)")]
leg = ax.legend(handles=handles, loc="lower left", frameon=True, fontsize=9)
leg.get_frame().set_facecolor(bg); leg.get_frame().set_edgecolor(grid)
for t in leg.get_texts():
    t.set_color(fg)

ax.text(0, -0.135,
        f"{len(pts)} of 85 units are testable on both variables. A further "
        f"{EXPECT['untestable: single-valued']} have a single country value and "
        f"cannot be tested at all;\nthose are the units sometimes quoted as "
        f"\"single-country\" evidence, and 30 of the 37 are Thailand, against "
        f"Thailand being 67% of the collection.\n"
        f"Two of the six clear the control only barely (strain_1_L1_5, "
        f"BioProject p=0.060; strain_1_L1_11, p=0.063), so the robust set is "
        f"arguably four.",
        transform=ax.transAxes, ha="left", va="top", color=muted, fontsize=9)

fig.tight_layout()
fig.savefig(OUT, format="svg", facecolor=bg, bbox_inches="tight")
print(f"wrote {OUT}")
print(f"  {len(pts)} units testable on both; "
      f"{sum(1 for p in pts if p[3].startswith('geographic'))} pass the control")
for u, pc, pb, k in sorted(pts, key=lambda p: p[1]):
    if k.startswith("geographic"):
        flag = "  <- MARGINAL on the control" if pb < 0.10 else ""
        print(f"    {u:18s} country p={pc:.4f}  bioproject p={pb:.4f}{flag}")
