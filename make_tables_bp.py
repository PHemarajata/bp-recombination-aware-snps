#!/usr/bin/env python3
"""
make_tables_bp.py -- Tables 1 to 5, generated from the frozen basis.

The figures are generated so they cannot go stale. The tables were not: four of
them are typed into the Results by hand and the fifth does not exist. This closes
that, on the same rule -- every number comes from a file, and where one cannot,
it is a named constant with its provenance beside it rather than a number of
unknown origin.

  Table 1  Panel and partition summary          (was missing entirely)
  Table 2  Gate 1 classification and r/m        GATE1_ALIGNMENT_2026-08-21.tsv
  Table 3  The strain_1_L1_26 refinement        GATE1 + control gate + A.7b
  Table 4  Spike-in recovery                    SPIKEIN_RESULT.txt
  Table 5  Tree-builder comparison              TREEBUILDER_EQ + RAPIDNJ_EQ

IT CHECKS ITSELF AGAINST THE MANUSCRIPT. Every table that already exists inline
is compared against the values typed there, and any drift is printed and made to
fail. That is the whole point: a table regenerated from data that quietly
disagrees with the prose is worse than no table.

ONE NUMBER IS A CONSTANT, AND IT IS THE ONE THAT MATTERS. Table 3's n = 98 child
sits at 72 mean pairwise core SNPs. That value is not in any file here: it was
recomputed on control membership from `core.tab` and recorded in
GATE1_ALIGNMENT_RESULT_2026-08-21.md section 7b, which also shows why the value
in the distances file, 1,310, is the unsplit parent's diversity arriving through
a join on unit name. Taking it from the file would put a number in the table that
is wrong by a factor of eighteen and would flip the row's Gate 1 class.

  python3 make_tables_bp.py            # writes TABLES.md

Stdlib only.
"""

import collections
import csv
import decimal
import os
import re
import statistics as st
import sys
from math import comb


def r3(x, places=3):
    """
    Round half-UP, not half-to-even.

    Table 5's rapidnj-against-RAxML median is exactly 0.9215, a tie. Python's
    round() breaks ties to even and returns 0.921; the source file and the
    manuscript carry 0.922. Neither is wrong, but the table must not disagree
    with its own source over a rounding convention.
    """
    q = decimal.Decimal(10) ** -places
    return float(decimal.Decimal(repr(x)).quantize(
        q, rounding=decimal.ROUND_HALF_UP))

B = os.path.dirname(os.path.abspath(__file__))
NUMBERS = f"{B}/NUMBERS.tsv"
PART = f"{B}/FINAL_BASIS_2026-08-22/FINAL_PARTITION.tsv"
META = f"{B}/L1v4c_MERGED_METADATA.tsv"
GATE1 = f"{B}/GATE1_ALIGNMENT_2026-08-21.tsv"
A100 = f"{B}/RETIRED_2026-08-22/a100_control/GATE1_ALIGNMENT_A100_2026-08-21.tsv"
SPIKE = f"{B}/SPIKEIN_RESULT.txt"
EQ_IQ = f"{B}/TREEBUILDER_EQ_RESULT.txt"
EQ_NJ = f"{B}/RAPIDNJ_EQ_RESULT.txt"
OUT = f"{B}/TABLES.md"

# GATE1_ALIGNMENT_RESULT_2026-08-21.md section 7b: diversity of the n=98 child
# recomputed on its OWN membership from core.tab. The distances file gives 1,310,
# which is the unsplit parent's value inherited through a join on unit name.
L1_26_CHILD_TRUE_DIVERSITY = 72

GATE_ORDER = [("in", "In-window"), ("below", "Below floor"),
              ("above", "Above ceiling")]

problems = []


def check(label, got, want, tol=0.0):
    ok = abs(got - want) <= tol if isinstance(want, float) else got == want
    if not ok:
        problems.append(f"{label}: computed {got}, manuscript {want}")
    return ok


def load(path, delim="\t"):
    return list(csv.DictReader(open(path), delimiter=delim))


def fmt(x, n=2):
    return f"{x:,.{n}f}"


def sign_p(below, n):
    k = max(below, n - below)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k, n + 1)) / 2 ** n)


def parse_eq(path):
    """The per-comparison block of a *_EQ_RESULT.txt."""
    rows = []
    for ln in open(path):
        m = re.match(r"^(\S+)\s+(chr[12])\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+"
                     r"([\d.]+)%\s+([\d.]+)%", ln)
        if m:
            u, arm, a, b, ratio, ua, ub = m.groups()
            rows.append({"unit": u, "arm": arm, "a": float(a), "b": float(b),
                         "ratio": float(ratio), "ua": float(ua),
                         "ub": float(ub)})
    if not rows:
        sys.exit(f"FATAL: no comparison rows parsed from {path}")
    return rows


def main():
    for p in (NUMBERS, PART, META, GATE1, A100, SPIKE, EQ_IQ, EQ_NJ):
        if not os.path.isfile(p):
            sys.exit(f"FATAL: {p} not found.")

    N = {r["key"]: r["value"] for r in load(NUMBERS)}
    part = load(PART)
    meta = {r["sample_id"]: r for r in load(META)}
    gate = {r["unit"]: r for r in load(GATE1)}
    ctrl = {r["unit"]: r for r in load(A100)}

    units = collections.Counter(r["unit"] for r in part)
    genomes = {r["sample_id"] for r in part}
    nU, nG = len(units), len(genomes)
    check("units.analysed", nU, int(N["units.analysed"]))
    check("genomes.analysed", nG, int(N["genomes.analysed"]))

    sizes = sorted(units.values())
    countries = collections.Counter(
        (meta[g]["country"] or "").strip() for g in genomes if g in meta)
    top_c, top_n = countries.most_common(1)[0]
    known = sum(v for k, v in countries.items() if k)

    cls = collections.Counter(gate[u]["gate1_alignment"] for u in units
                              if u in gate)
    rms = collections.defaultdict(list)
    for u in units:
        if u in gate and gate[u]["rm_corrected"] not in ("", "NA"):
            rms[gate[u]["gate1_alignment"]].append(float(gate[u]["rm_corrected"]))

    check("Table 2 in-window units", cls["in"], 47)
    check("Table 2 below-floor units", cls["below"], 12)
    check("Table 2 above-ceiling units", cls["above"], 26)
    check("Table 2 in-window median r/m", round(st.median(rms["in"]), 2), 7.70, 0.005)
    check("Table 2 below median r/m", round(st.median(rms["below"]), 2), 1.32, 0.005)
    check("Table 2 above median r/m", round(st.median(rms["above"]), 2), 2.14, 0.005)
    check("rm.median_gate1", round(st.median(rms["in"]), 2),
          float(N["rm.median_gate1"]), 0.005)

    out = [
        "# Tables 1 to 5\n",
        "Generated by `make_tables_bp.py` from the frozen basis "
        "(`FINAL_BASIS_2026-08-22`). Do not edit; regenerate. Every value is "
        "read from a file except where a source is named in the notes.\n",
    ]

    # ---------------- Table 1 ----------------
    out += [
        "\n## Table 1. Panel and partition summary\n",
        "| | value | source |",
        "|---|---|---|",
        f"| Assemblies in the v4c panel | {int(N['panel.v4c']):,} | "
        f"`L1v4c_MERGED_METADATA.tsv` |",
        f"| Panel after duplicate and exclusion correction | "
        f"{int(N['panel.corrected_v4d']):,} | `NUMBERS.tsv` panel.corrected_v4d |",
        f"| Countries represented in the panel | {int(N['panel.countries'])} | "
        f"`NUMBERS.tsv` panel.countries |",
        "| | | |",
        f"| **Analysis units (reported basis)** | **{nU}** | "
        f"`FINAL_PARTITION.tsv` |",
        f"| **Genomes in analysis units** | **{nG:,}** | `FINAL_PARTITION.tsv` |",
        f"| Genomes per unit, median (range) | {int(st.median(sizes))} "
        f"({min(sizes)} to {max(sizes)}) | `FINAL_PARTITION.tsv` |",
        f"| Countries in the analysed set | "
        f"{len([k for k in countries if k])} | joined to metadata |",
        f"| Most-represented country | {top_c} {top_n:,} "
        f"({100*top_n/known:.1f}% of {known:,} with a known country) | "
        f"joined to metadata |",
        "| | | |",
        f"| Units in-window (Gate 1) | {cls['in']} | "
        f"`GATE1_ALIGNMENT_2026-08-21.tsv` |",
        f"| Units below floor | {cls['below']} | as above |",
        f"| Units above ceiling | {cls['above']} | as above |",
        f"| **Median r/m, in-window units** | **{st.median(rms['in']):.2f}** | "
        f"`NUMBERS.tsv` rm.median_gate1 |",
        "\n*The panel is 2,976 assemblies as submitted to PopPUNK and 2,959 "
        "after removing 17 duplicate BioSamples; both appear in the Results and "
        "they are different stages, not a discrepancy. The analysed set is "
        "smaller again because a unit must reach n >= 5 to be analysed.*\n",
    ]

    # ---------------- Table 2 ----------------
    out += [
        "\n## Table 2. Gate 1 classification and r/m by class\n",
        "| Gate 1 class | units | median r/m | IQR | genomes |",
        "|---|---|---|---|---|",
    ]
    for key, label in GATE_ORDER:
        v = sorted(rms[key])
        q = st.quantiles(v, n=4, method="inclusive") if len(v) > 3 else [0, 0, 0]
        ng = sum(units[u] for u in units
                 if u in gate and gate[u]["gate1_alignment"] == key)
        bold = "**" if key == "in" else ""
        out.append(f"| {bold}{label}{bold} | {bold}{cls[key]}{bold} | "
                   f"{bold}{st.median(v):.2f}{bold} | "
                   f"{q[0]:.2f} to {q[2]:.2f} | {ng:,} |")
    out.append(
        f"\n*Window [{N.get('rm.gate1_floor','700')}, "
        f"{N.get('rm.gate1_ceiling','4700')}] mean pairwise core SNPs, "
        f"alignment-derived, floor bracketed (588, 755]. The contrast between "
        f"{st.median(rms['in']):.2f} in-window and "
        f"{st.median(rms['below'] + rms['above']):.2f} outside is what makes "
        f"this a detection window rather than a filter.*\n")

    # ---------------- Table 3 ----------------
    parent, c26 = gate.get("strain_1_L1_26"), ctrl.get("strain_1_L1_26")
    c36, c37 = ctrl.get("strain_1_L1_36"), ctrl.get("strain_1_L1_37")
    if not all((parent, c26, c36, c37)):
        sys.exit("FATAL: strain_1_L1_26 refinement rows missing.")
    out += [
        "\n## Table 3. The `strain_1_L1_26` refinement, before and after\n",
        "| | n | mean pairwise core SNPs | r/m | Gate 1 |",
        "|---|---|---|---|---|",
        f"| Before, `strain_1_L1_26` | {int(float(parent['n']))} | "
        f"{float(parent['aln_mean_pairwise_snps']):,.0f} | "
        f"{float(parent['rm_corrected']):.2f} | In-window |",
        f"| After, `strain_1_L1_26` | {int(float(c26['n']))} | "
        f"{L1_26_CHILD_TRUE_DIVERSITY} | {float(c26['rm_corrected']):.2f} | "
        f"Below floor |",
        f"| After, `strain_1_L1_36` | {int(float(c36['n']))} | "
        f"{float(c36['aln_mean_pairwise_snps']):,.0f} | "
        f"{float(c36['rm_corrected']):.2f} | In-window |",
        f"| After, `strain_1_L1_37` | {int(float(c37['n']))} | "
        f"{float(c37['aln_mean_pairwise_snps']):,.0f} | "
        f"{float(c37['rm_corrected']):.2f} | Below floor |",
        "\n*Diversities are alignment-derived, on the same metric as the "
        "window. An earlier version of this table reported the Mash "
        "approximation against the alignment-derived floor, which is the "
        "cross-unit-system comparison Results section 4 exists to warn about. "
        "The n = 98 child's 72 is recomputed on its own membership "
        "(`GATE1_ALIGNMENT_RESULT_2026-08-21.md` section 7b); joining the split "
        "children to the unsplit parent by unit name assigns that child the "
        "parent's 1,310 instead. The split is the cross-hardware control run's; "
        "the reported basis keeps `strain_1_L1_26` unsplit.*\n",
    ]
    check("Table 3 parent n", int(float(parent["n"])), 153)
    check("Table 3 parent r/m", round(float(parent["rm_corrected"]), 2), 4.47, 0.005)

    # ---------------- Table 4 ----------------
    spikes = []
    for ln in open(SPIKE):
        m = re.match(r"^([\d.]+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+(\d+)\s+(\d+)\s+"
                     r"([\d.]+)", ln)
        if m:
            nu, reps, imp, snps, pre, rec, rate = m.groups()
            # The rate comes from the file, not from these integers. The
            # nu = 0.002 and nu = 0.01 rows print identical counts (24 implants,
            # 3 pre-detected, 19 recovered) and different rates, 0.91 and 0.90,
            # so the printed integers are rounded summaries across replicates
            # and do not determine the rate. Recomputing 19/21 would silently
            # change the reported 91% to 90%.
            den = int(imp) - int(pre)
            spikes.append({"nu": float(nu), "snps": float(snps),
                           "rec": int(rec), "den": den,
                           "pct": 100.0 * float(rate)})
    out += [
        "\n## Table 4. Spike-in recovery\n",
        "| Donor divergence | SNPs per 5 kb tract | Recovered |",
        "|---|---|---|",
    ]
    for s in spikes:
        b = "**" if abs(s["nu"] - 0.002) < 1e-9 else ""
        lab = f"{s['nu']}, the measured value" if b else f"{s['nu']}"
        out.append(f"| {b}{lab}{b} | {b}{s['snps']:.1f}{b} | "
                   f"{b}{s['rec']} of {s['den']}, {s['pct']:.0f}%{b} |")
    out.append(
        "\n*Denominator is implanted tracts minus those already detected in the "
        "control. Recovery is non-monotonic at the top because a tract carrying "
        "45 SNPs can be split into two called blocks, neither covering 50% of "
        "it.*\n")
    m2 = [s for s in spikes if abs(s["nu"] - 0.002) < 1e-9][0]
    check("Table 4 recovery at nu=0.002", round(m2["pct"]), 91)

    # ---------------- Table 5 ----------------
    iq, nj = parse_eq(EQ_IQ), parse_eq(EQ_NJ)
    key = lambda r: (r["unit"], r["arm"])
    njmap = {key(r): r for r in nj}
    rows = []

    def summarise(label, ratios, ua, ub, bold=False):
        below = sum(1 for r in ratios if r < 1.0)
        dev = [abs(r - 1.0) * 100 for r in ratios]
        p = sign_p(below, len(ratios))
        b = "**" if bold else ""
        rows.append(f"| {b}{label}{b} | {b}{r3(st.median(ratios)):.3f}{b} | "
                    f"{b}{st.median(dev):.1f}%{b} | {b}{max(dev):.1f}%{b} | "
                    f"{b}{below} of {len(ratios)}{b} | "
                    f"{b}p = {p:.2g}{b} |")
        return r3(st.median(ratios)), below, p

    r_iq = [r["ratio"] for r in iq]
    r_nj = [r["ratio"] for r in nj]
    # rapidnj against IQ-TREE, holding the model fitter constant
    r_nj_iq = [njmap[key(r)]["b"] / r["b"] for r in iq if key(r) in njmap]

    m_iq, b_iq, p_iq = summarise("IQ-TREE against RAxML", r_iq, None, None)
    m_nj, b_nj, p_nj = summarise("rapidnj against RAxML", r_nj, None, None, True)
    m_ni, b_ni, p_ni = summarise("rapidnj against IQ-TREE", r_nj_iq, None, None)

    out += [
        "\n## Table 5. Tree-builder comparison\n",
        "| Comparison | Median ratio | Median deviation | Worst | "
        "Ratios below 1.0 | Sign test |",
        "|---|---|---|---|---|---|",
    ] + rows + [
        f"\n*Six units by two replicons, {len(iq)} comparisons, on the same "
        f"real alignments, spanning r/m {min(r['a'] for r in iq):.2f} to "
        f"{max(r['a'] for r in iq):.2f}. The sign test is two-sided on the "
        f"count of ratios below 1.0. The third row holds the model fitter "
        f"constant, because Gubbins delegates model fitting to IQ-TREE when a "
        f"distance-based constructor is selected, so it isolates the "
        f"constructor alone. That third row is derived from the other two "
        f"files' r/m values, which they print to two decimals, so its "
        f"extremes carry about +/-0.2 points of rounding; the manuscript "
        f"reports its worst case as 51.6%.*\n",
    ]
    check("Table 5 IQ/RAx median ratio", round(m_iq, 3), 0.988, 0.0005)
    check("Table 5 rapidnj/RAx median ratio", round(m_nj, 3), 0.922, 0.0005)
    check("Table 5 rapidnj/IQ median ratio", round(m_ni, 3), 0.938, 0.0005)
    check("Table 5 IQ/RAx below 1.0", b_iq, 7)
    check("Table 5 rapidnj/RAx below 1.0", b_nj, 11)
    check("Table 5 rapidnj/IQ below 1.0", b_ni, 10)

    with open(OUT, "w") as fh:
        fh.write("\n".join(out) + "\n")

    print(f"wrote {OUT}")
    print(f"  Table 1  panel {int(N['panel.corrected_v4d']):,} -> "
          f"{nU} units / {nG:,} genomes")
    print(f"  Table 2  {cls['in']} in / {cls['below']} below / "
          f"{cls['above']} above, median r/m {st.median(rms['in']):.2f}")
    print(f"  Table 3  strain_1_L1_26 n={int(float(parent['n']))} -> "
          f"98 / 47 / 8")
    print(f"  Table 4  {len(spikes)} divergence levels, "
          f"{m2['pct']:.0f}% at nu = 0.002")
    print(f"  Table 5  {len(iq)} comparisons, medians "
          f"{m_iq:.3f} / {m_nj:.3f} / {m_ni:.3f}")

    if problems:
        print("\n  *** TABLE DISAGREES WITH THE MANUSCRIPT ***")
        for p in problems:
            print(f"    {p}")
        sys.exit(1)
    print("\n  all cross-checks against the manuscript and NUMBERS.tsv agree")


if __name__ == "__main__":
    main()
