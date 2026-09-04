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

IT CROSS-CHECKS THE MANUSCRIPT AND SAYS SO WHEN THEY DISAGREE. The draft states
1,519 null replicates and a separation of 427 to 2,234 fold. This script
recomputes both from `TIER2_null.txt` and prints the comparison. It warns rather
than failing, because the table rounds null values to three decimals and may be a
reported subset of a larger run, so a mismatch here is a question about
provenance and not necessarily an error. It must not be ignored, and it must not
be silently absorbed into a figure either.

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

# What the manuscript currently claims, so a drift is visible at generation time.
CLAIM_REPS = 1519
CLAIM_LO, CLAIM_HI = 427, 2234
CLAIM_RECOVERY = 0.91
CLAIM_NU = 0.002

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
    reps = sum(r["reps"] for r in nulls)
    obs = [r["obs"] for r in nulls]
    gmax = max(r["null_max"] for r in nulls)
    lo, hi = min(obs) / gmax, max(obs) / gmax
    sig = sum(1 for r in nulls if r["p"] <= 0.05)

    print(f"null: {len(nulls)} unit-replicons, {reps} replicates")
    print(f"  observed r/m {min(obs):.2f} to {max(obs):.2f}")
    print(f"  greatest null r/m {gmax:.5f}")
    print(f"  separation {lo:.0f}x to {hi:.0f}x")
    print(f"  {sig} of {len(nulls)} exceed their own null at p <= 0.05")

    drift = []
    if reps != CLAIM_REPS:
        drift.append(f"replicates: manuscript {CLAIM_REPS}, this table {reps}")
    if abs(lo - CLAIM_LO) > 1 or abs(hi - CLAIM_HI) > 1:
        drift.append(f"separation: manuscript {CLAIM_LO}-{CLAIM_HI}x, "
                     f"this table {lo:.0f}-{hi:.0f}x")
    if drift:
        print("\n  *** DISAGREES WITH THE MANUSCRIPT ***")
        for d in drift:
            print(f"    {d}")
        print("    The figure is drawn from the table, not from the claim.")
        print("    Reconcile before submission: either the table is a reported")
        print("    subset of a larger null run, or the draft is on a stale one.")

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
    axA.set_ylabel(f"unit-replicon, sorted by observed r/m  (n = {len(nulls)})",
                   color=fg, fontsize=10)
    axA.set_title("A  Lower bound: observed against a matched\n"
                  "zero-recombination null",
                  color=fg, fontsize=11, loc="left")
    axA.axvline(FLOOR, color=grid, ls=":", lw=1)
    axA.text(FLOOR * 1.15, len(nulls) * 0.02,
             "null below display\nprecision (<0.001)",
             color=fg, fontsize=7.5, va="bottom")
    axA.annotate("", xy=(min(obs), len(nulls) * 0.62),
                 xytext=(gmax, len(nulls) * 0.62),
                 arrowprops=dict(arrowstyle="<->", color=fg, lw=1.1))
    axA.text((gmax * min(obs)) ** 0.5, len(nulls) * 0.645,
             f"{lo:.0f}x to {hi:.0f}x", color=fg, fontsize=9,
             ha="center", va="bottom")
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
             f"A: {sig} of {len(nulls)} unit-replicons exceed their own null at "
             f"p <= 0.05 over {reps} replicates. The null has one tree and no "
             f"population structure, so it calibrates the recombination role of "
             f"pooled r/m only.",
             color=fg, fontsize=7.6, ha="center", wrap=True)

    fig.tight_layout(rect=(0, 0.045, 1, 1))
    fig.savefig(OUT, facecolor=bg, bbox_inches="tight")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
