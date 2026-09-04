#!/usr/bin/env python3
"""
Figure 5 -- detection is bounded from both sides.

Results section 5 makes a two-sided claim and currently has no figure. This is
it. Panel A is the lower bound: observed pooled r/m against a matched
ZERO-recombination null, per unit-replicon, so the separation can be read rather
than asserted. Panel B is the upper bound on sensitivity: spike-in recovery
against donor divergence, with the value measured in this collection marked.

WHY THE TWO PANELS BELONG TOGETHER. A recombination estimate is only a
measurement if it is above what the method produces from no recombination at all,
and only useful if the method would have found the recombination that is there.
Panel A answers the first, Panel B the second. Reporting either alone leaves the
obvious objection open.

⚠ `TIER2_null.txt` IS A MID-RUN SNAPSHOT AND MUST NOT BE SUMMARISED. It reports
1,302 replicates over 54 unit-replicons. The completed run is **1,519 replicates
over 62 unit-replicons**, and `REVISED_STRATEGY_2026-08.md` A.11ag carries an
addendum saying so outright: "THE COUNTS BELOW ARE STALE; THE VERDICT IS NOT ...
Quote the completed figures, not these, in the paper."

That is why the headline numbers here are constants taken from the completed run
rather than recomputed from the file. Summarising the file instead gives 434x to
2,131x, which is wrong, and wrong in the most dangerous way available: close
enough to the right answer to look like rounding. The first version of this
script did exactly that and reported the manuscript as being in error when the
manuscript was correct.

The project has now hit this same shape seven times, and its own note on the
sixth is the rule: *do not record a count until the run that produces it has
stopped.* The per-replicate statistics files for the completed run are not on
this workstation, so the per-unit detail plotted in panel A is the 54-replicon
subset and is drawn and labelled AS a subset, while every quantity the figure
actually claims comes from the completed run.

  python3 make_figure5_bp.py            # FIGURE5_DETECTION_BOUNDS.svg
  python3 make_figure5_bp.py --dark     # dark variant

Reads TIER2_null.txt and SPIKEIN_RESULT.txt. Needs matplotlib.
"""

import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

B = os.path.dirname(os.path.abspath(__file__))
NULL = f"{B}/TIER2_null.txt"
SPIKE = f"{B}/SPIKEIN_RESULT.txt"
DARK = "--dark" in sys.argv
OUT = f"{B}/FIGURE5_DETECTION_BOUNDS{'_dark' if DARK else ''}.svg"

# The COMPLETED run (REVISED_STRATEGY_2026-08.md A.11ag addendum, recomputed
# there from the 1,519 per-replicate statistics files; METHODS_DRAFT 2.8.3).
# These are the figure's claims. They are not recomputed from TIER2_null.txt,
# which is the superseded mid-run snapshot.
RUN_REPS = 1519
RUN_REPLICONS = 62
RUN_CLEARING = 59           # unit-replicons at p <= 0.05
RUN_FP_BLOCKS = 20          # replicates producing any false-positive block
RUN_NULL_MAX = 0.00668
RUN_OBS_LO, RUN_OBS_HI = 2.85, 14.92
CLAIM_NU = 0.002

# Sanity: the separation quoted in the Abstract must be these numbers' ratio.
SEP_LO = round(RUN_OBS_LO / RUN_NULL_MAX)
SEP_HI = round(RUN_OBS_HI / RUN_NULL_MAX)

# The null table prints three decimals, so a null max of 0.000 means "below
# display precision", not zero. Clamping to half the last place keeps the log
# axis honest and the censoring is stated on the figure.
FLOOR = 0.0005


def read_null():
    rows = []
    for ln in open(NULL):
        m = re.match(r"^(\S+)\s+(chr[12])\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+"
                     r"([\d.]+)\s+([\d.]+)\s*$", ln)
        if m:
            u, arm, reps, obs, nmed, nmax, p = m.groups()
            rows.append({"unit": u, "arm": arm, "reps": int(reps),
                         "obs": float(obs), "null_med": float(nmed),
                         "null_max": float(nmax), "p": float(p)})
    if not rows:
        sys.exit(f"FATAL: no data rows parsed from {NULL}")
    return rows


def read_spike():
    rows = []
    for ln in open(SPIKE):
        m = re.match(r"^([\d.]+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+(\d+)\s+(\d+)\s+"
                     r"([\d.]+)", ln)
        if m:
            nu, reps, imp, snps, pre, rec, rate = m.groups()
            rows.append({"nu": float(nu), "snps": float(snps),
                         "rate": float(rate)})
    if not rows:
        sys.exit(f"FATAL: no data rows parsed from {SPIKE}")
    return rows


def main():
    for p in (NULL, SPIKE):
        if not os.path.isfile(p):
            sys.exit(f"FATAL: {p} not found.")

    nulls, spikes = read_null(), read_spike()
    sub_reps = sum(r["reps"] for r in nulls)
    sub_sig = sum(1 for r in nulls if r["p"] <= 0.05)

    print(f"COMPLETED RUN (what this figure claims):")
    print(f"  {RUN_REPS} replicates over {RUN_REPLICONS} unit-replicons")
    print(f"  greatest null r/m {RUN_NULL_MAX:.5f}, median 0.000")
    print(f"  observed r/m {RUN_OBS_LO:.2f} to {RUN_OBS_HI:.2f}")
    print(f"  separation {SEP_LO}x to {SEP_HI}x")
    print(f"  {RUN_CLEARING} of {RUN_REPLICONS} clear p <= 0.05; "
          f"{RUN_FP_BLOCKS} replicates produced any false-positive block")

    print(f"\nTIER2_null.txt (mid-run snapshot, plotted as detail only):")
    print(f"  {len(nulls)} unit-replicons, {sub_reps} replicates, "
          f"{sub_sig} clearing p <= 0.05")
    if sub_reps != RUN_REPS or len(nulls) != RUN_REPLICONS:
        print("  ^ superseded by the completed run; see REVISED_STRATEGY A.11ag.")
        print("    Do NOT summarise this file. Summarising it gives 434x-2131x,")
        print("    which is wrong by just enough to look like rounding.")

    if abs(SEP_LO - 427) > 1 or abs(SEP_HI - 2234) > 1:
        sys.exit(f"FATAL: separation recomputes to {SEP_LO}x-{SEP_HI}x but the "
                 f"manuscript states 427x-2234x. One of them has moved.")

    fg = "#e8e8e8" if DARK else "#1a1a1a"
    bg = "#111111" if DARK else "#ffffff"
    grid = "#333333" if DARK else "#dddddd"
    c_obs, c_null, c_mark = "#4575b4", "#d95f02", "#1b9e77"

    fig, (axA, axB) = plt.subplots(
        1, 2, figsize=(12.4, 6.4), facecolor=bg,
        gridspec_kw={"width_ratios": [1.55, 1]})

    # ---- Panel A: observed against its own null ----
    axA.set_facecolor(bg)
    order = sorted(range(len(nulls)), key=lambda i: nulls[i]["obs"])
    for y, i in enumerate(order):
        r = nulls[i]
        nx = max(r["null_max"], FLOOR)
        axA.plot([nx, r["obs"]], [y, y], color=grid, lw=0.8, zorder=1)
        axA.plot(nx, y, "o", ms=3.4, color=c_null, zorder=3)
        axA.plot(r["obs"], y, "o", ms=4.4, color=c_obs, zorder=3)
    axA.set_xscale("log")
    axA.set_xlabel("pooled r/m (log scale)", color=fg, fontsize=10)
    axA.set_ylabel(f"unit-replicon, sorted by observed r/m\n"
                   f"(detail: {len(nulls)} of {RUN_REPLICONS} available here)",
                   color=fg, fontsize=9.5)
    axA.set_title("A  Lower bound: observed against a matched\n"
                  "zero-recombination null",
                  color=fg, fontsize=11, loc="left")
    axA.axvline(FLOOR, color=grid, ls=":", lw=1)
    axA.text(FLOOR * 1.15, len(nulls) * 0.02,
             "null below display\nprecision (<0.001)",
             color=fg, fontsize=7.5, va="bottom")
    # The separation is stated from the COMPLETED run, not from the points drawn.
    axA.axvline(RUN_NULL_MAX, color=c_null, ls="--", lw=1.2, alpha=0.9)
    axA.axvline(RUN_OBS_LO, color=c_obs, ls="--", lw=1.2, alpha=0.9)
    axA.annotate("", xy=(RUN_OBS_LO, len(nulls) * 0.62),
                 xytext=(RUN_NULL_MAX, len(nulls) * 0.62),
                 arrowprops=dict(arrowstyle="<->", color=fg, lw=1.1))
    axA.text((RUN_NULL_MAX * RUN_OBS_LO) ** 0.5, len(nulls) * 0.645,
             f"{SEP_LO}x to {SEP_HI}x", color=fg, fontsize=9,
             ha="center", va="bottom")
    axA.text(RUN_NULL_MAX * 1.15, len(nulls) * 0.40,
             f"greatest null r/m\n{RUN_NULL_MAX:.5f}", color=c_null,
             fontsize=7.5, va="center")
    axA.text(RUN_OBS_LO * 1.10, len(nulls) * 0.30,
             f"lowest observed\n{RUN_OBS_LO:.2f}", color=c_obs,
             fontsize=7.5, va="center")
    axA.tick_params(colors=fg, labelsize=8)
    for s in axA.spines.values():
        s.set_color(grid)
    axA.grid(axis="x", color=grid, lw=0.5, alpha=0.5)

    # ---- Panel B: spike-in recovery ----
    axB.set_facecolor(bg)
    xs = [r["nu"] for r in spikes]
    ys = [r["rate"] * 100 for r in spikes]
    axB.plot(xs, ys, "-o", color=c_obs, ms=6, lw=1.6, zorder=3)
    here = [r for r in spikes if abs(r["nu"] - CLAIM_NU) < 1e-9]
    if here:
        r = here[0]
        axB.plot(r["nu"], r["rate"] * 100, "o", ms=13, mfc="none",
                 mec=c_mark, mew=2.2, zorder=4)
        axB.annotate(f"measured in this\ncollection: {r['rate']*100:.0f}%",
                     xy=(r["nu"], r["rate"] * 100),
                     xytext=(r["nu"] * 1.35, r["rate"] * 100 - 34),
                     color=fg, fontsize=8.5,
                     arrowprops=dict(arrowstyle="->", color=c_mark, lw=1.3))
    for r in spikes:
        axB.annotate(f"{r['snps']:.0f}", xy=(r["nu"], r["rate"] * 100),
                     xytext=(0, 9), textcoords="offset points",
                     color=fg, fontsize=7, ha="center", alpha=0.75)
    axB.set_xscale("log")
    axB.set_ylim(0, 112)
    axB.set_xlabel("donor divergence nu (log scale)", color=fg, fontsize=10)
    axB.set_ylabel("implanted tracts recovered (%)", color=fg, fontsize=10)
    axB.set_title("B  Upper bound on sensitivity:\nspike-in recovery",
                  color=fg, fontsize=11, loc="left")
    axB.tick_params(colors=fg, labelsize=8)
    for s in axB.spines.values():
        s.set_color(grid)
    axB.grid(color=grid, lw=0.5, alpha=0.5)
    axB.text(0.5, -0.19, "small numbers are SNPs per implanted 5 kb tract",
             transform=axB.transAxes, color=fg, fontsize=7.5, ha="center",
             alpha=0.8)

    fig.text(0.5, 0.015,
             f"A: completed null run, {RUN_REPS} replicates over "
             f"{RUN_REPLICONS} unit-replicons; {RUN_CLEARING} of "
             f"{RUN_REPLICONS} exceed their own null at p <= 0.05 and "
             f"{RUN_FP_BLOCKS} replicates ({100*RUN_FP_BLOCKS/RUN_REPS:.2f}%) "
             f"produced any false-positive block. Points show the "
             f"{len(nulls)} unit-replicons available on this machine; the "
             f"dashed lines and the fold range are the completed run. The null "
             f"has one tree and no population structure, so it calibrates the "
             f"recombination role of pooled r/m only.",
             color=fg, fontsize=7.2, ha="center", wrap=True)

    fig.tight_layout(rect=(0, 0.045, 1, 1))
    fig.savefig(OUT, facecolor=bg, bbox_inches="tight")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
