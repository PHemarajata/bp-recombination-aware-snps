#!/usr/bin/env python3
"""
The attribution resolution ceiling -- publication figure.

Four panels carrying one argument: a genome will tell you the region and will not
tell you the country, the failures are identifiable rather than noise, the result
survives the control that would expose it as luck, and the ceiling is not a
resolution problem.

  A  the ladder            accuracy against baseline, country through Asia-vs-not
  B  where the 46 landed   region confusion, modal k = 20
  C  the depth control     accuracy by distance to the nearest panel genome
  D  the resolution curve  7 loci against 4,221

DELIBERATELY NOT NUMBERED. Every other figure script here is make_figureN_bp.py,
and this one is not, because the placement of this material is undecided: the
current manuscript reports geographic STRUCTURE in Results 8 and cites the absence
of any published attribution accuracy only as motivation, so this is either a new
Results section or the core of the second paper. Numbering it Figure 7 would
commit to the first by default. Rename once that decision is taken.

THE ESTIMATOR IS PART OF EVERY NUMBER HERE, and mixing two is the single easiest
way to get this wrong. Country's best estimator is nearest neighbour; region's is
the modal vote over k = 20 neighbours. CGMLST_LICHT_ATTRIBUTION.tsv is
nearest-neighbour throughout and reports region as 37/46; the 89% headline is the
modal vote, in GROUPING_LADDER.tsv. This script asserts the estimator it uses for
each grouping is in fact that grouping's best by kappa, and refuses to draw if not.

  python3 make_figure_attribution_bp.py           # light
  python3 make_figure_attribution_bp.py --dark

Needs matplotlib.
"""

import collections
import csv
import os
import statistics as st
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

B = os.path.dirname(os.path.abspath(__file__))
LADDER = f"{B}/GROUPING_LADDER.tsv"
PRED = f"{B}/GROUPING_PREDICTIONS.tsv"
MLST = f"{B}/MLST_ATTRIBUTION_SUMMARY.tsv"
DARK = "--dark" in sys.argv
OUT = f"{B}/FIGURE_ATTRIBUTION_CEILING{'_dark' if DARK else ''}.svg"

# The estimator each grouping is reported at. Asserted below, not assumed.
EST = {"country": "nearest_nb", "sea_vs_not": "modal_k20",
       "region_7way": "modal_k20", "east_vs_west": "modal_k20",
       "asia_vs_not": "modal_k20"}
ORDER = ["country", "sea_vs_not", "region_7way", "east_vs_west", "asia_vs_not"]
NICE = {"country": "Country", "sea_vs_not": "SE Asia vs. not",
        "region_7way": "Region", "east_vs_west": "East vs. West hemi.",
        "asia_vs_not": "Asia vs. not"}
SHORT = {"East Asia & Pacific": "E Asia\n& Pacific",
         "Latin America & Caribbean": "Latin Am.\n& Carib.",
         "South Asia": "South\nAsia",
         "North America": "North\nAmerica",
         "Sub-Saharan Africa": "Sub-Sah.\nAfrica"}
ROWS = ["East Asia & Pacific", "Latin America & Caribbean", "South Asia",
        "North America", "Sub-Saharan Africa"]
STRATA = [("close", "< 0.05", lambda d: d < 0.05),
          ("mid", "0.05 – 0.30", lambda d: 0.05 <= d < 0.30),
          ("far", "≥ 0.30", lambda d: d >= 0.30)]


def load(p):
    return list(csv.DictReader(open(p), delimiter="\t"))


def main():
    for p in (LADDER, PRED, MLST):
        if not os.path.isfile(p):
            sys.exit(f"FATAL: {p} not found.")

    lad = load(LADDER)
    by = {(r["grouping"], r["estimator"]): r for r in lad}

    # --- refuse to draw if we are not using each grouping's best estimator ---
    for g, e in EST.items():
        cand = [r for r in lad if r["grouping"] == g]
        best = max(cand, key=lambda r: float(r["kappa"]))["estimator"]
        if best != e:
            sys.exit(f"FATAL: {g} is reported at {e} but its best estimator by "
                     f"kappa is {best}. Refusing to draw a mixed-estimator figure.")

    pred = load(PRED)
    reg = [r for r in pred
           if r["grouping"] == "region_7way" and r["estimator"] == "modal_k20"]
    ctry = [r for r in pred
            if r["grouping"] == "country" and r["estimator"] == "nearest_nb"]
    n_reg = sum(int(r["correct"]) for r in reg)
    n_ctry = sum(int(r["correct"]) for r in ctry)
    if (n_reg, len(reg)) != (41, 46) or (n_ctry, len(ctry)) != (10, 46):
        sys.exit(f"FATAL: recomputed region {n_reg}/{len(reg)} and country "
                 f"{n_ctry}/{len(ctry)}; expected 41/46 and 10/46.")

    # confusion, and what is never emitted
    cm = collections.Counter((r["truth"], r["predicted"]) for r in reg)
    emitted = sorted({r["predicted"] for r in reg})
    print(f"region modal k=20: {n_reg}/{len(reg)}")
    print(f"  emits {len(emitted)} of 7 regions: {', '.join(emitted)}")

    # depth strata
    def strat(rs):
        out = []
        for _, lab, f in STRATA:
            s = [r for r in rs if f(float(r["nn_distance"]))]
            out.append((lab, sum(int(r["correct"]) for r in s), len(s)))
        return out
    d_reg, d_ctry = strat(reg), strat(ctry)
    print("  depth region :", d_reg)
    print("  depth country:", d_ctry)

    # resolution curve
    m = {r["scale"]: r for r in load(MLST)}
    mr, mc = m["region"], m["country"]

    # ---------------- draw ----------------
    fg = "#E7EEF1" if DARK else "#141A1F"
    bg = "#0E1316" if DARK else "#FFFFFF"
    mut = "#7E8D97" if DARK else "#6E7D88"
    grid = "#26323A" if DARK else "#DCE3E7"
    SIG = "#46B5A9" if DARK else "#0E6E6B"
    CLAY = "#D8975C" if DARK else "#A9662F"
    NUL = "#75828D" if DARK else "#8A94A0"

    plt.rcParams.update({"font.size": 8.5, "font.family": "DejaVu Sans"})
    fig = plt.figure(figsize=(11.6, 8.3), facecolor=bg)
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.05],
                          hspace=.52, wspace=.34,
                          left=.075, right=.965, top=.885, bottom=.175)
    axA = fig.add_subplot(gs[0, :])
    axB = fig.add_subplot(gs[1, 0])
    axC = fig.add_subplot(gs[1, 1])
    axD = fig.add_subplot(gs[1, 2])
    for ax in (axA, axB, axC, axD):
        ax.set_facecolor(bg)
        for s in ax.spines.values():
            s.set_color(grid)

    # ---- A: the ladder ----
    ys = range(len(ORDER))
    for i, g in enumerate(ORDER):
        r = by[(g, EST[g])]
        acc, base, k = float(r["accuracy"]), float(r["baseline"]), float(r["kappa"])
        col = NUL if acc <= base else (CLAY if k < .6 else SIG)
        axA.barh(i, acc * 100, height=.52, color=col, zorder=3)
        axA.plot([base * 100] * 2, [i - .34, i + .34], color=fg, lw=1.6, zorder=5)
        # Value inside the bar once it is long enough, so it never collides with
        # the kappa column on the right.
        inside = acc > .92
        axA.text(acc * 100 + (-1.6 if inside else 1.4), i, f"{acc*100:.0f}%",
                 va="center", ha="right" if inside else "left", fontsize=8.5,
                 color="#FFFFFF" if inside else fg, zorder=6)
        axA.text(108, i, f"κ {k:.3f}", va="center", ha="left", fontsize=8.5,
                 color=fg if k > .6 else mut, family="DejaVu Sans Mono")
        axA.text(-1.5, i, f"{NICE[g]}", va="center", ha="right", fontsize=9,
                 color=fg)
        axA.text(-1.5, i - .30, f"{r['classes']} classes · {r['correct']}/{r['n']}",
                 va="center", ha="right", fontsize=7, color=mut)
    axA.set_yticks([]); axA.set_ylim(len(ORDER) - .4, -.75)
    axA.set_xlim(0, 128)
    axA.set_xticks([0, 25, 50, 75, 100])
    axA.set_xticklabels(["0", "25", "50", "75", "100%"], color=fg)
    axA.tick_params(colors=fg, labelsize=8)
    axA.xaxis.grid(True, color=grid, lw=.6, zorder=0)
    axA.set_axisbelow(True)
    for s in ("top", "right", "left"):
        axA.spines[s].set_visible(False)
    axA.set_title("A   The ceiling sits between country and region",
                  loc="left", color=fg, fontsize=10.5, pad=9)
    axA.plot([], [], color=fg, lw=1.6, label="majority baseline")
    axA.legend(loc="upper right", frameon=False, fontsize=7.6,
               labelcolor=fg, bbox_to_anchor=(1.005, 1.14))
    # Sits just under the country bar, pointing up at its baseline tick, so the
    # note never crosses the other rows.
    # Above the country row, in the empty band under the panel title, so neither
    # line can fall behind the SE Asia bar below it.
    axA.annotate("bar stops short of its own baseline: worse than ignoring the genome",
                 xy=(26.3, -.30), xytext=(31, -.60), fontsize=7.4, color=CLAY,
                 va="center", ha="left",
                 arrowprops=dict(arrowstyle="->", color=CLAY, lw=1,
                                 connectionstyle="arc3,rad=.25"))

    # ---- B: confusion ----
    mx = max(cm.values())
    for i, tr in enumerate(ROWS):
        for j, pr in enumerate(ROWS):
            v = cm.get((tr, pr), 0)
            if v:
                c = SIG if i == j else CLAY
                axB.add_patch(Rectangle((j - .46, i - .46), .92, .92,
                                        facecolor=c,
                                        alpha=.25 + .75 * v / mx, lw=0))
                axB.text(j, i, str(v), ha="center", va="center", fontsize=9,
                         color="#FFFFFF" if v / mx > .45 else fg, zorder=4)
            else:
                axB.text(j, i, "·", ha="center", va="center", fontsize=8,
                         color=mut)
    axB.set_xlim(-.5, 4.5); axB.set_ylim(4.5, -1.25)
    axB.set_xticks(range(5)); axB.set_yticks(range(5))
    axB.set_xticklabels([SHORT[r] for r in ROWS], fontsize=6.4, color=fg)
    axB.set_yticklabels([SHORT[r] for r in ROWS], fontsize=6.4, color=fg)
    axB.set_xlabel("predicted", color=mut, fontsize=8, labelpad=16)
    axB.set_ylabel("true region of exposure", color=mut, fontsize=8)
    axB.tick_params(length=0)
    axB.set_title(f"B   Where the 46 landed   ·   {n_reg}/{len(reg)}",
                  loc="left", color=fg, fontsize=10.5, pad=9)
    for j in (3, 4):
        axB.add_patch(Rectangle((j - .5, -.5), 1, 5, facecolor="none",
                                edgecolor=mut, lw=.8, ls=(0, (2, 2))))
    axB.annotate("never emitted", xy=(3.5, -.5), xytext=(3.5, -1.02),
                 ha="center", va="center", fontsize=6.8, color=mut,
                 style="italic",
                 arrowprops=dict(arrowstyle="-", color=mut, lw=.7))

    # ---- C: depth control ----
    x = range(3)
    w = .36
    for k, (dat, col, lab) in enumerate([(d_reg, SIG, "region"),
                                         (d_ctry, NUL, "country")]):
        vals = [100 * c / n for _, c, n in dat]
        pos = [i + (k - .5) * w for i in x]
        axC.bar(pos, vals, width=w, color=col, label=lab, zorder=3)
        for p, v, (_, c, n) in zip(pos, vals, dat):
            axC.text(p, v + 2.5, f"{c}/{n}", ha="center", fontsize=7, color=fg)
    axC.set_xticks(list(x))
    axC.set_xticklabels([f"{lab}\n(n={n})" for (_, lab, _), (_, _, n)
                         in zip(STRATA, d_reg)], fontsize=7.4, color=fg)
    axC.set_ylim(0, 116)
    axC.set_yticks([0, 25, 50, 75, 100])
    axC.set_yticklabels(["0", "25", "50", "75", "100%"], color=fg)
    axC.set_xlabel("distance to nearest panel genome", color=mut, fontsize=8)
    axC.tick_params(colors=fg, labelsize=7.6, length=0)
    axC.yaxis.grid(True, color=grid, lw=.6, zorder=0); axC.set_axisbelow(True)
    for s in ("top", "right"):
        axC.spines[s].set_visible(False)
    axC.legend(frameon=False, fontsize=7.6, labelcolor=fg, loc="upper center",
               ncol=2, bbox_to_anchor=(.5, 1.02))
    axC.set_title("C   It is not proximity doing the work",
                  loc="left", color=fg, fontsize=10.5, pad=9)

    # ---- D: resolution curve ----
    loci = [7, 4221]
    r_acc = [float(mr["pct"]), 100 * n_reg / len(reg)]
    c_acc = [float(mc["pct"]), 100 * n_ctry / len(ctry)]
    r_base = [100 * int(mr["baseline"]) / int(mr["baseline_n"]),
              100 * float(by[("region_7way", "modal_k20")]["baseline"])]
    c_base = [100 * int(mc["baseline"]) / int(mc["baseline_n"]),
              100 * float(by[("country", "nearest_nb")]["baseline"])]
    axD.plot(loci, r_acc, "-o", color=SIG, lw=1.8, ms=6, zorder=4, label="region")
    axD.plot(loci, c_acc, "-o", color=NUL, lw=1.8, ms=6, zorder=4, label="country")
    axD.plot(loci, r_base, ":", color=SIG, lw=1.2, alpha=.75, zorder=3)
    axD.plot(loci, c_base, ":", color=NUL, lw=1.2, alpha=.75, zorder=3)
    axD.set_xscale("log")
    axD.set_xlim(4, 9000); axD.set_ylim(-6, 108)
    axD.set_xticks([7, 4221]); axD.set_xticklabels(["7\nMLST", "4,221\ncgMLST"],
                                                   color=fg, fontsize=7.6)
    axD.set_yticks([0, 25, 50, 75, 100])
    axD.set_yticklabels(["0", "25", "50", "75", "100%"], color=fg)
    axD.set_xlabel("loci compared", color=mut, fontsize=8)
    axD.tick_params(colors=fg, labelsize=7.6, length=0)
    axD.yaxis.grid(True, color=grid, lw=.6, zorder=0); axD.set_axisbelow(True)
    for s in ("top", "right"):
        axD.spines[s].set_visible(False)
    axD.legend(frameon=False, fontsize=7.6, labelcolor=fg,
               loc="upper left", bbox_to_anchor=(-.02, 1.02))
    axD.text(9000, -3, "dotted = majority baseline", fontsize=6.6,
             color=mut, ha="right", va="bottom")
    axD.set_title("D   More loci lift region, not country",
                  loc="left", color=fg, fontsize=10.5, pad=9)

    fig.suptitle("A genome resolves the region of exposure and not the country",
                 color=fg, fontsize=13.5, x=.075, ha="left", y=.965)
    cap = [
        "46 validation genomes with a registered exposure country, scored against the 2,340-genome frozen panel. Country is scored at nearest neighbour and every other",
        "grouping at the modal vote over k = 20, each being that grouping's best estimator by kappa; figures from the two estimators must not be compared across.",
        f"(B) The modal vote emits only {len(emitted)} of the 7 regions, so North America and Sub-Saharan Africa are unreachable rather than merely wrong. (D) Dotted lines are the",
        "majority baseline within each scored set; the MLST denominator is 33, not 46, so D compares trends rather than paired figures.",
    ]
    for i, line in enumerate(cap):
        fig.text(.075, .088 - i * .019, line, fontsize=6.9, color=mut,
                 ha="left", va="top")

    fig.savefig(OUT, facecolor=bg, bbox_inches="tight")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
