#!/usr/bin/env python3
"""
Gap 4 companion: sampling-frame and phylogeography diagnostics for
Burkholderia pseudomallei.

Five independent things live here. Each answers a question the Gap 4 pass
opened, and each runs on data already in this directory.

  (A) sampling_frame()   - how many independent geographic draws does this
      collection actually contain? Hill numbers on the country distribution,
      on the year distribution, and a Kish design effect for the BioProject
      pseudo-replication. The headline is the gap between 47 country labels
      and the effective number of countries.

  (B) root_state_demo()  - the closed-form demonstration that a discrete-trait
      root-state posterior tracks tip-state *counts*. Runs an Mk model on a
      star tree at the observed country proportions, then again on
      Chewapreecha's n-per-country balanced design, and reports how far the
      answer moves. This is the sampling-bias critique made arithmetic on this
      specific dataset rather than cited from a viral paper.

  (C) subsample_design()  - what Chewapreecha's "equal n per country, discard
      countries below n" rule actually retains from this collection, swept
      across n. Tells you the price of the only subsampling protocol in the
      literature for this organism.

  (D) dateability()       - which cluster properties predicted successful
      dating in the one study that tried? Computed from Chewapreecha's own 20
      clusters and their published dated/not-dated outcome, then turned into a
      screen you can apply before spending BEAST time.

  (E) temporal_power()    - can a cluster possibly carry temporal signal? The
      expected number of substitutions accumulated across the sampling window,
      against the within-cluster diversity. A cluster that cannot accumulate
      one substitution across its sampling window cannot be dated, and this is
      checkable before any MCMC.

  (F) burden_vs_sampling() - the denominator. Genome counts per region against
      Limmathurotsakul et al.'s predicted melioidosis burden per region. This
      is the argument that "country" in a phylogeographic model is measuring
      research capacity rather than the organism's distribution, made as a
      ratio rather than as an assertion.

Nothing here is a published threshold. Derivations are flagged as mine.
Published numbers carry their source inline.

Usage:
    python3 phylogeography_diagnostics_bp.py
    python3 phylogeography_diagnostics_bp.py --section A
    python3 phylogeography_diagnostics_bp.py --audit bp_public_genome_audit_2026-08-09.csv
    python3 phylogeography_diagnostics_bp.py --section E --rate 1.7e-7 --length 3805619
"""

import argparse
import csv
import math
import os
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))

DEFAULT_AUDIT = os.path.join(HERE, "bp_public_genome_audit_2026-08-09.csv")
DEFAULT_CLUSTERS = os.path.join(HERE, "chewapreecha_hierbaps_clusters_2026-08-09.csv")

# --------------------------------------------------------------------------
# Published constants. Every number here is sourced.
# --------------------------------------------------------------------------

# Seng R, et al. 2024, PMID 38972886. ENA PRJEB25606 (682) + PRJEB35787 (582)
# = 1,265 clinical isolates, nine hospitals, northeast Thailand, 2015-2018.
SENG_BIOPROJECTS = {"PRJEB25606": 682, "PRJEB35787": 582}
SENG_SITES = 9
SENG_YEARS = 4

# The three dominant Thai BioProjects, RESOLVED 2026-08-09 by re-running the
# audit query with assembly_info.bioproject_accession retained (the original
# audit script never collected that field, which is why this stayed open).
# Counts are assemblies, taxid 28450, n = 5,728 total / 3,414 Thailand.
#
#   PRJEB3409    1,506   44.1% of Thai, 26.3% of the whole collection
#   PRJEB25606     682   20.0%
#   PRJEB35787     582   17.0%
#                        -----
#                        81.1%  <- reproduces the audit's "81% from three"
#
# PRJEB3409 was the missing one, and it is the largest single contributor to
# the entire global collection. ENA title:
# "Burkholderia_pseudomallei___case_control_study_", Wellcome Sanger
# Institute, first public 2014-11-26. Three properties matter:
#
#   - It is a CASE-CONTROL design, i.e. isolates selected by outcome rather
#     than sampled at random from a population.
#   - It is majority ENVIRONMENTAL: host = "environmental" 760 (50.5%) plus
#     "environment" 96 (6.4%) = 856 (56.9%); "homo sapiens" 650 (43.2%).
#     So ~15% of the entire global collection is environmental isolates from
#     one Thai study.
#   - It is 93.6% UNDATED (1,410 of 1,506 blank; the 96 dated run 2010-2012).
#     It supplies 1,410 of the 1,554 undated Thai genomes - 91% of them.
#
# By contrast PRJEB25606 and PRJEB35787 (Seng et al. 2024) are 100% dated,
# 100% Homo sapiens, and span 2015-2018 only. Consequence worth stating: of
# the 1,860 DATED Thai genomes, 1,264 (68%) are that single nine-hospital
# study over four years.
BIOPROJECTS_THAI = {"PRJEB3409": 1506, "PRJEB25606": 682, "PRJEB35787": 582}
PRJEB3409_ENVIRONMENTAL = 856
PRJEB3409_CLINICAL = 650
PRJEB3409_UNDATED = 1410
THAI_TOTAL = 3414
THAI_UNDATED = 1554

# Pearson T, Sahl JW, Hepp CM, et al. "Pathogen to commensal? Longitudinal
# within-host population dynamics, evolution, and adaptation during a chronic
# >16-year Burkholderia pseudomallei infection." PLoS Pathog 2020;16(3):
# e1008298. PMID 32149236. Verbatim: "The median evolutionary rate across the
# entire genomic dataset was 1.7 x 10-7 substitutions/site/year (95% HPD
# 1.3 x 10-7 - 2.1 x 10-7)."
#
# This is provably the prior Seng et al. 2024 used ("prior mutation rate
# derived from Pearson and colleagues"), so there is a Nature Communications
# precedent for importing it into a B. pseudomallei BactDating analysis.
#
# Two caveats that must travel with the number. It is a WITHIN-HOST rate from
# a chronic infection, and B. pseudomallei spends most of its existence as a
# soil saprophyte; and short-timescale rate estimates systematically exceed
# long-timescale ones. Both biases push the same way - the rate is probably
# too fast, so node ages derived from it are probably too young.
BP_RATE = 1.7e-7
BP_RATE_LO = 1.3e-7
BP_RATE_HI = 2.1e-7

# Murray GGR, Wang F, Harrison EM, et al. "The effect of genetic structure on
# molecular dating and tests for temporal signal." Methods Ecol Evol
# 2016;7(1):80-89. PMID 27110344. Their MRSA ST22 danger zone, verbatim:
# "fewer than 7 nucleotide substitutions per genome would be expected during
# this entire sampling period" - the regime in which "the standard tests
# failed for the confounded subsample, resulting in false confidence."
MURRAY_DANGER_SUBS = 7.0

# Chewapreecha C, et al. 2017, Nat Microbiol 2:16263, PMID 28112723.
# Subsampling for stochastic character mapping, verbatim from Methods:
# "equal numbers of isolates from Thailand, Laos, Cambodia, Vietnam, Malaysia
# and Singapore (n = 15 for each country), and resampled 1,000 times.
# Countries containing less than 15 isolates were excluded".
CHEWAPREECHA_N_PER_COUNTRY = 15
CHEWAPREECHA_RESAMPLES = 1000

# Labels in the NCBI geo_loc_name field that are not countries.
NON_COUNTRY_LABELS = {
    "MISSING", "missing", "unknown", "Unknown", "NA", "N/A", "not applicable",
}

# Limmathurotsakul D, Golding N, Dance DAB, et al. "Predicted global
# distribution of Burkholderia pseudomallei and burden of melioidosis."
# Nat Microbiol 2016;1:15008. PMID 26877885. DOI 10.1038/nmicrobiol.2015.8.
# Table 1, "Estimated burden of melioidosis in 2015, by continent."
# Cases and deaths in THOUSANDS per year, with 95% credible intervals.
# Regions are World Bank regions, as used in that table.
BURDEN_2015 = OrderedDict([
    # region                    (cases, lo, hi,   deaths, dlo, dhi)
    ("South Asia",              (73.0, 31.0, 171.0,  42.0, 18.0, 101.0)),
    ("East Asia & Pacific",     (65.0, 28.0, 161.0,  31.0, 13.0,  77.0)),
    ("Sub-Saharan Africa",      (24.0,  8.0,  72.0,  15.0,  6.0,  45.0)),
    ("Latin America & Caribbean", (2.0, 1.0,   7.0,   1.0,  0.0,   3.0)),
    ("Middle East & North Africa", (0.5, 0.0,  1.0,   0.5,  0.0,   1.0)),  # "<1"
    ("Europe & Central Asia",   (0.0,  0.0,   0.0,   0.0,  0.0,   0.0)),
    ("North America",           (0.0,  0.0,   0.0,   0.0,  0.0,   0.0)),
])
BURDEN_GLOBAL_CASES = 165.0   # thousands, 95% CrI 68-412
BURDEN_GLOBAL_DEATHS = 89.0   # thousands, 95% CrI 36-227

# Same paper, Supplementary Information TABLE 1, "Predicted incidence and
# mortality of melioidosis in 2015, by countries" (page 11 of the publisher
# supplement, 41564_2016_BFnmicrobiol20158_MOESM367_ESM.pdf). Retrieved
# 2026-08-09. Cases per year with 95% credible interval.
#
# The table's own footnote markers are carried through because they matter:
#   "*" = endemic but under-reported
#   "+" = predicted to be endemic but NEVER reported
#
# Country names are as printed in the table; COUNTRY_ALIASES maps the audit's
# NCBI geo_loc_name spellings onto them.
BURDEN_COUNTRY = {
    # East Asia & Pacific
    "Indonesia":      (20038,  7859, 52812, "*"),
    "Vietnam":        (10430,  4097, 27480, "*"),
    "Philippines":     (9116,  4819, 18999, "*"),
    "Thailand":        (7572,  3396, 17685, "*"),
    "China":           (7174,  3099, 15752, "*"),
    "Myanmar":         (6247,  2513, 15400, "*"),
    "Cambodia":        (2083,   850,  5451, "*"),
    "Malaysia":        (1752,   718,  4581, "*"),
    "Lao PDR":          (420,   172,  1072, "*"),
    "Singapore":        (276,    66,   925, ""),
    "Australia":        (149,    56,   416, ""),
    "Papua New Guinea": (129,    43,   337, "*"),
    "Hong Kong SAR, China": (67,  23,   288, "*"),
    "Brunei Darussalam": (29,    12,    71, ""),
    "Timor-Leste":       (10,     3,    35, "*"),
    "Fiji":               (4,     1,    14, "*"),
    # South Asia
    "India":          (52506, 22335, 124652, "*"),
    "Bangladesh":     (16931,  7814,  37794, "*"),
    "Sri Lanka":       (1881,   705,   4488, "*"),
    "Nepal":            (914,   317,   2354, "+"),
    "Pakistan":         (442,    95,   1718, "*"),
    "Bhutan":            (13,     5,     42, "+"),
    # Sub-Saharan Africa
    "Nigeria":        (13481,  4839,  38348, "*"),
    "Guinea":          (1372,   472,   3810, "+"),
    "Cote d'Ivoire":   (1144,   414,   3368, "*"),
    "Benin":            (919,   348,   2580, "+"),
    "Madagascar":       (880,   326,   2464, "*"),
    "Burkina Faso":     (627,   196,   2102, "+"),
    "Sierra Leone":     (600,   212,   1715, "*"),
    "Mali":             (580,   190,   1912, "+"),
    "Cameroon":         (540,   169,   1699, "+"),
    "Liberia":          (445,   148,   1288, "+"),
    "Chad":             (401,   114,   1432, "*"),
    "Ghana":            (389,   111,   1446, "*"),
    "Niger":            (368,    78,   1371, "+"),
    "Tanzania":         (307,    74,    991, "+"),
    "Congo, Rep.":      (262,    98,    716, "+"),
    "Ethiopia":         (261,    61,    885, "+"),
    "Mozambique":       (238,    65,    795, "+"),
    "Congo, Dem. Rep.": (222,    53,    772, "+"),
    "Malawi":           (221,    69,    636, "*"),
    "Togo":             (157,    43,    500, "+"),
    "Central African Republic": (142, 45, 422, "+"),
    "Zambia":           (112,    30,    374, "+"),
    "Guinea-Bissau":    (100,    28,    345, "+"),
    "Kenya":            (100,    27,    327, "*"),
    "Somalia":           (71,    13,    254, "+"),
    "Sudan":             (62,     8,    247, "+"),
    "Senegal":           (60,    13,    247, "+"),
    "Gabon":             (45,    16,    127, "*"),
    "South Sudan":       (39,     8,    131, "+"),
    "Uganda":            (30,     5,    131, "+"),
    "Angola":            (29,     6,    116, "+"),
    "South Africa":      (28,     6,    103, "*"),
    "Mauritania":        (28,     6,    110, "+"),
    "Eritrea":           (27,     6,    101, "+"),
    "Gambia, The":        (8,     1,     33, "*"),
    "Zimbabwe":           (7,     2,     28, "+"),
    "Equatorial Guinea":  (6,     2,     17, "+"),
    "Mauritius":          (5,     1,     18, "*"),
    # Latin America & Caribbean
    "Brazil":           (872,   273,   2905, "*"),
    "Mexico":           (550,   158,   1712, "*"),
    "Colombia":         (157,    43,    496, "*"),
    "El Salvador":      (114,    37,    295, "*"),
    "Venezuela, RB":    (103,    31,    311, "*"),
    "Panama":            (86,    22,    264, "*"),
    "Guatemala":         (66,    20,    197, "+"),
    "Nicaragua":         (65,    18,    196, "+"),
    "Peru":              (39,    10,    128, "*"),
    "Haiti":             (24,     5,     86, "*"),
    "Cuba":              (20,     4,     89, "*"),
    "Argentina":         (18,     3,     75, "*"),
    "Costa Rica":        (16,     5,     49, "*"),
    "Suriname":          (14,     4,     39, "*"),
    "Paraguay":          (13,     2,     59, "+"),
    "Bolivia":           (13,     3,     49, "+"),
    "Guyana":            (12,     3,     36, "*"),
    # Middle East & North Africa
    "Yemen, Rep.":       (99,    29,    302, "+"),
    "Saudi Arabia":      (52,    13,    197, "*"),
    "Iraq":              (21,     4,    127, "+"),
    "Iran, Islamic Rep.": (15,    3,     73, "*"),
    "Oman":               (6,     2,     19, "+"),
}

# NCBI geo_loc_name spelling -> Supplementary Table 1 spelling.
COUNTRY_ALIASES = {
    "Viet Nam": "Vietnam",
    "Laos": "Lao PDR",
    "Hong Kong": "Hong Kong SAR, China",
    "Venezuela": "Venezuela, RB",
}

# World Bank region for each country label appearing in the audit CSV.
# Assignments follow the World Bank classification used in that Table 1.
COUNTRY_REGION = {
    # South Asia
    "India": "South Asia", "Bangladesh": "South Asia",
    "Sri Lanka": "South Asia", "Pakistan": "South Asia",
    # East Asia & Pacific
    "Thailand": "East Asia & Pacific", "Australia": "East Asia & Pacific",
    "China": "East Asia & Pacific", "Singapore": "East Asia & Pacific",
    "Malaysia": "East Asia & Pacific", "Viet Nam": "East Asia & Pacific",
    "Hong Kong": "East Asia & Pacific", "New Caledonia": "East Asia & Pacific",
    "Laos": "East Asia & Pacific", "Micronesia": "East Asia & Pacific",
    "Papua New Guinea": "East Asia & Pacific", "Taiwan": "East Asia & Pacific",
    "Japan": "East Asia & Pacific", "New Zealand": "East Asia & Pacific",
    "South Korea": "East Asia & Pacific", "Philippines": "East Asia & Pacific",
    # Sub-Saharan Africa
    "Ghana": "Sub-Saharan Africa", "Madagascar": "Sub-Saharan Africa",
    "South Africa": "Sub-Saharan Africa", "Chad": "Sub-Saharan Africa",
    # Latin America & Caribbean
    "Mexico": "Latin America & Caribbean",
    "Puerto Rico": "Latin America & Caribbean",
    "Ecuador": "Latin America & Caribbean",
    "Venezuela": "Latin America & Caribbean",
    "Virgin Islands": "Latin America & Caribbean",
    "Guadeloupe": "Latin America & Caribbean",
    "Brazil": "Latin America & Caribbean",
    # Middle East & North Africa
    "Israel": "Middle East & North Africa",
    # Europe & Central Asia
    "United Kingdom": "Europe & Central Asia", "France": "Europe & Central Asia",
    "Switzerland": "Europe & Central Asia",
    "Czech Republic": "Europe & Central Asia",
    "Russia": "Europe & Central Asia", "Portugal": "Europe & Central Asia",
    # North America
    "USA": "North America", "Canada": "North America",
}


# --------------------------------------------------------------------------
# Input
# --------------------------------------------------------------------------

def load_audit(path):
    """Read the NCBI audit CSV into {category: OrderedDict(key -> count)}."""
    out = {}
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            cat = row["category"]
            out.setdefault(cat, OrderedDict())[row["key"]] = int(row["count"])
    return out


def load_clusters(path):
    with open(path, newline="") as fh:
        return [r for r in csv.DictReader(fh) if r.get("cluster")]


def countries_only(counts):
    """Drop the non-country placeholder labels."""
    return OrderedDict(
        (k, v) for k, v in counts.items() if k not in NON_COUNTRY_LABELS
    )


# --------------------------------------------------------------------------
# Diversity arithmetic (Hill numbers)
# --------------------------------------------------------------------------

def hill(counts, q):
    """
    Hill number of order q on a count vector.

    q=0 is richness (the raw label count), q=1 is exp(Shannon), q=2 is the
    inverse Simpson index. All three are in units of "effective number of
    categories", which is what makes them comparable to the raw label count.

    Hill MO. Diversity and evenness: a unifying notation and its consequences.
    Ecology 1973;54(2):427-432. Standard in ecology; used here because
    "47 countries" and "effectively 2.5 countries" need to be on one scale.
    """
    n = sum(counts)
    if n == 0:
        return 0.0
    p = [c / n for c in counts if c > 0]
    if q == 0:
        return float(len(p))
    if abs(q - 1.0) < 1e-12:
        return math.exp(-sum(pi * math.log(pi) for pi in p))
    return sum(pi ** q for pi in p) ** (1.0 / (1.0 - q))


def pielou(counts):
    """Shannon evenness, in [0,1]. 1 is perfectly even."""
    p = [c for c in counts if c > 0]
    if len(p) < 2:
        return float("nan")
    return math.log(hill(p, 1)) / math.log(len(p))


def kish_design_effect(group_sizes, icc):
    """
    Kish's design effect for cluster sampling:  deff = 1 + (m_eff - 1) * ICC,
    with m_eff the mean cluster size weighted by cluster size.

    Kish L. Survey Sampling. Wiley, 1965. The effective sample size is
    n / deff. ICC (intra-cluster correlation) is not measurable from the audit
    table, so this is reported across a range rather than at a point.
    """
    n = sum(group_sizes)
    if n == 0:
        return float("nan"), float("nan")
    m_eff = sum(s * s for s in group_sizes) / n
    deff = 1.0 + (m_eff - 1.0) * icc
    return deff, n / deff


# --------------------------------------------------------------------------
# (A) Sampling frame
# --------------------------------------------------------------------------

def sampling_frame(audit, args):
    print(header("A. What is the effective sampling frame?"))

    geo = countries_only(audit.get("geo_loc_name", {}))
    total_geo = sum(geo.values())
    dropped = sum(v for k, v in audit.get("geo_loc_name", {}).items()
                  if k in NON_COUNTRY_LABELS)

    print(f"Country-labelled genomes : {total_geo:,}")
    print(f"Placeholder / missing    : {dropped:,}")
    print()

    counts = list(geo.values())
    h0, h1, h2 = hill(counts, 0), hill(counts, 1), hill(counts, 2)
    print("Hill numbers on the country distribution")
    print(f"  q=0  richness            : {h0:.0f} distinct country labels")
    print(f"  q=1  exp(Shannon)        : {h1:.2f} effective countries")
    print(f"  q=2  inverse Simpson     : {h2:.2f} effective countries")
    print(f"  Pielou evenness          : {pielou(counts):.3f}")
    print()
    print(f"  Interpretation: {h0:.0f} country labels collapse to {h2:.2f} at q=2.")
    print(f"  A phylogeographic model given {h0:.0f} discrete states is being asked to")
    print(f"  estimate on the order of {h0 * (h0 - 1):.0f} pairwise migration rates from")
    print(f"  what is effectively a {h2:.1f}-state dataset.")
    print()

    # Years
    yr = audit.get("collection_year", {})
    yr_counts = [v for k, v in yr.items() if k.isdigit()]
    yr_missing = sum(v for k, v in yr.items() if not k.isdigit())
    yr_total = sum(yr_counts)
    print("Hill numbers on the collection-year distribution")
    print(f"  Dated genomes            : {yr_total:,}"
          f"   ({100.0 * yr_total / (yr_total + yr_missing):.1f}% of collection)")
    print(f"  q=0  distinct years      : {hill(yr_counts, 0):.0f}")
    print(f"  q=1  exp(Shannon)        : {hill(yr_counts, 1):.2f} effective years")
    print(f"  q=2  inverse Simpson     : {hill(yr_counts, 2):.2f} effective years")
    print(f"  Pielou evenness          : {pielou(yr_counts):.3f}")
    print()
    span = max(int(k) for k in yr if k.isdigit()) - min(int(k) for k in yr if k.isdigit())
    print(f"  The nominal temporal span is {span} years. The effective span, in the")
    print(f"  sense of independent-year-equivalents, is {hill(yr_counts, 2):.1f}.")
    print(f"  Root-to-tip regression is driven by the effective span, not the nominal one.")
    print()

    # BioProject pseudo-replication
    print("BioProject pseudo-replication (Kish design effect)")
    thai = geo.get("Thailand", 0)
    seng_n = sum(SENG_BIOPROJECTS.values())
    print(f"  Thailand genomes             : {thai:,}")
    print("  The three dominant Thai BioProjects (resolved 2026-08-09):")
    for acc, n in BIOPROJECTS_THAI.items():
        print(f"    {acc:<12} {n:>5,}  {100.0 * n / thai:>5.1f}% of Thai  "
              f"{100.0 * n / total_geo:>5.1f}% of collection")
    print(f"    {'':12} {sum(BIOPROJECTS_THAI.values()):>5,}  "
          f"{100.0 * sum(BIOPROJECTS_THAI.values()) / thai:>5.1f}% combined")
    print()
    print(f"  PRJEB3409 is a CASE-CONTROL study and is majority environmental:")
    print(f"    environmental {PRJEB3409_ENVIRONMENTAL:,} ({100.0 * PRJEB3409_ENVIRONMENTAL / 1506:.1f}%)"
          f"   clinical {PRJEB3409_CLINICAL:,} ({100.0 * PRJEB3409_CLINICAL / 1506:.1f}%)")
    print(f"    undated {PRJEB3409_UNDATED:,} ({100.0 * PRJEB3409_UNDATED / 1506:.1f}%) - "
          f"{100.0 * PRJEB3409_UNDATED / THAI_UNDATED:.0f}% of all undated Thai genomes")
    print()
    dated_thai = THAI_TOTAL - THAI_UNDATED
    print(f"  So of the {dated_thai:,} DATED Thai genomes, {seng_n:,} "
          f"({100.0 * seng_n / dated_thai:.0f}%) are Seng et al.,")
    print(f"  drawn from {SENG_SITES} hospitals over {SENG_YEARS} years "
          f"({SENG_SITES * SENG_YEARS} site-year strata, "
          f"{seng_n / (SENG_SITES * SENG_YEARS):.0f} genomes each).")
    print("  The dated Thai signal is therefore one hospital network over four")
    print("  years. That is the confounding Murray et al. 2016 describe, and it")
    print("  is why section E's effective temporal span is 11 years, not 90.")
    print()
    # Dominant cluster is PRJEB3409, not the Seng pair. Treat it as one
    # cluster against a remainder of singletons: a conservative floor.
    dom = max(BIOPROJECTS_THAI.values())
    rest = total_geo - dom
    sizes = [dom] + [1] * rest
    print(f"  Design effect below treats the largest single project "
          f"(PRJEB3409, n={dom:,})")
    print("  as one cluster against a remainder of singletons - a deliberately")
    print("  conservative floor, since the other two projects are also blocks.")
    print("  deff and effective n, sweeping the unmeasured ICC:")
    print(f"    {'ICC':>6}  {'deff':>8}  {'effective n':>12}  {'% of nominal':>13}")
    for icc in (0.01, 0.05, 0.10, 0.25, 0.50):
        deff, neff = kish_design_effect(sizes, icc)
        print(f"    {icc:>6.2f}  {deff:>8.2f}  {neff:>12,.0f}  "
              f"{100.0 * neff / total_geo:>12.1f}%")
    print()
    print("  ICC is not measurable from the audit table; it is measurable from your")
    print("  own data as the fraction of core-SNP variance falling between rather")
    print("  than within BioProjects. Until it is measured, quote the range.")
    print()


# --------------------------------------------------------------------------
# (B) Root-state posterior follows tip counts
# --------------------------------------------------------------------------

def mk_root_posterior(state_counts, qt, root_prior=None):
    """
    Marginal root-state posterior under an equal-rates Mk model on a STAR tree.

    For a K-state equal-rates (ER) Markov model with per-transition rate q and
    branch length t, the transition probability matrix has the closed form

        P_ii(t) = 1/K + (K-1)/K * exp(-K*q*t)
        P_ij(t) = 1/K -   1/K   * exp(-K*q*t)      (i != j)

    On a star tree every tip hangs off the root by t, so Felsenstein pruning
    collapses to a product over tips and the root conditional likelihood for
    state i is

        L(i) = prod_over_states_s  P_is(t) ** n_s

    which depends on the data only through the state COUNTS n_s. That is the
    point: the root-state posterior is a function of how many tips carry each
    state, and nothing in the model distinguishes "many tips because the deme
    is large or ancestral" from "many tips because that country was sequenced
    more". This is the sampling-bias critique of discrete trait analysis,
    stated in the simplest model that exhibits it.

    A star tree is the extreme case and is labelled as such. A real tree with
    structure dilutes the effect but does not remove it, because the tip
    counts still enter the likelihood in exactly this way.

    Returns an OrderedDict state -> posterior probability.
    """
    states = list(state_counts.keys())
    k = len(states)
    if k < 2:
        return OrderedDict((s, 1.0) for s in states)
    e = math.exp(-k * qt)
    p_same = 1.0 / k + (k - 1.0) / k * e
    p_diff = 1.0 / k - (1.0 / k) * e
    # Guard against underflow at large qt.
    p_same = max(p_same, 1e-300)
    p_diff = max(p_diff, 1e-300)

    if root_prior is None:
        root_prior = {s: 1.0 / k for s in states}

    logl = {}
    for i in states:
        tot = 0.0
        for s in states:
            n_s = state_counts[s]
            tot += n_s * math.log(p_same if s == i else p_diff)
        logl[i] = tot + math.log(root_prior[i])

    m = max(logl.values())
    w = {s: math.exp(logl[s] - m) for s in states}
    z = sum(w.values())
    return OrderedDict(sorted(((s, w[s] / z) for s in states),
                              key=lambda kv: -kv[1]))


def root_state_demo(audit, args):
    print(header("B. Does the root-state answer follow the sampling?"))

    geo = countries_only(audit.get("geo_loc_name", {}))
    # Keep the states a DTA would plausibly be given: countries with >= 10
    # genomes, which is already generous.
    obs = OrderedDict((k, v) for k, v in geo.items() if v >= 10)
    print(f"States retained (>= 10 genomes): {len(obs)}")
    print(f"Genomes in those states        : {sum(obs.values()):,}")
    print()

    # Balanced design: Chewapreecha's rule, applied to the same state set.
    n_bal = args.n_per_country
    bal = OrderedDict((k, n_bal) for k, v in obs.items() if v >= n_bal)

    print("Equal-rates Mk root-state posterior on a star tree, sweeping q*t.")
    print("(q*t is the expected number of state changes per branch; small means")
    print(" geography is conserved, large means it is saturated.)")
    print()
    print("Reported as log10 of the Bayes factor for the top state against the")
    print("runner-up, because the posterior itself saturates at 1.0000 and hides")
    print("the magnitude. A log10 BF above 2 is 'decisive' on Kass and Raftery's")
    print("scale; these run to several hundred.")
    print()
    print(f"  {'q*t':>6}   {'top state':<12} {'log10 BF':>10}   "
          f"{'balanced top':<12} {'log10 BF':>10}")
    for qt in (0.001, 0.01, 0.05, 0.1, 0.5):
        so, vo, bfo = top_and_bf(mk_root_posterior(obs, qt), obs, qt)
        sb, vb, bfb = top_and_bf(mk_root_posterior(bal, qt), bal, qt)
        print(f"  {qt:>6.3f}   {so:<12} {bfo:>10.1f}   {sb:<12} {bfb:>10.1f}")
    print()

    po = mk_root_posterior(obs, 0.01)
    print("At q*t = 0.01, the ranked posterior under the observed sampling:")
    for s, v in list(po.items())[:6]:
        print(f"    {s:<20} {v:.4f}   (n = {obs[s]:,})")
    print()
    print(f"Under the balanced design (n = {n_bal} per country, "
          f"{len(bal)} countries retained), every state has the same count, so")
    print(f"the posterior is exactly flat at 1/{len(bal)} = {1.0 / len(bal):.4f}.")
    print()
    print("  Read those two blocks together. The unbalanced run puts posterior")
    print("  1.0000 on Thailand with a log10 Bayes factor in the hundreds - a")
    print("  result that looks overwhelming and is entirely an artefact of the")
    print("  state counts. The balanced run is exactly uninformative. Neither")
    print("  number is evidence about where the organism came from.")
    print()
    print("  A star tree is the extreme case and is labelled as such: real tree")
    print("  structure dilutes the effect, because correlated tips stop counting")
    print("  as independent observations. It does not remove it. The tip counts")
    print("  enter the likelihood in exactly this way on any topology, which is")
    print("  why the fix is to change the sample, not the model.")
    print()
    print("  Practical consequence: a root-state or ancestral-area posterior from")
    print("  an unbalanced run carries no information that the sample-size table")
    print("  does not already carry. It must not be reported as a result.")
    print()


def top_and_bf(post, counts, qt):
    """Top state, its posterior, and log10 BF against the runner-up."""
    items = list(post.items())
    s0, v0 = items[0]
    if len(items) < 2:
        return s0, v0, float("inf")
    # Recompute on the log scale so the ratio survives saturation.
    states = list(counts.keys())
    k = len(states)
    e = math.exp(-k * qt)
    p_same = max(1.0 / k + (k - 1.0) / k * e, 1e-300)
    p_diff = max(1.0 / k - (1.0 / k) * e, 1e-300)
    def ll(i):
        return sum(counts[s] * math.log(p_same if s == i else p_diff)
                   for s in states)
    lls = sorted((ll(s) for s in states), reverse=True)
    return s0, v0, (lls[0] - lls[1]) / math.log(10)


# --------------------------------------------------------------------------
# (C) Subsampling design
# --------------------------------------------------------------------------

def subsample_design(audit, args):
    print(header("C. What does the balanced-subsample rule cost?"))

    geo = countries_only(audit.get("geo_loc_name", {}))
    total = sum(geo.values())

    print("Chewapreecha's rule, verbatim from Methods: equal numbers per country,")
    print("countries below the threshold excluded entirely. Applied here to the")
    print("full country distribution, swept across the threshold.")
    print()
    print(f"  {'n/country':>10}  {'countries kept':>15}  {'genomes used':>13}"
          f"  {'% of collection':>16}  {'% of Thailand used':>19}")
    thai = geo.get("Thailand", 0)
    for n in (5, 10, 15, 20, 30, 50, 100, 150, 200):
        kept = [k for k, v in geo.items() if v >= n]
        used = n * len(kept)
        thai_used = n if thai >= n else 0
        print(f"  {n:>10}  {len(kept):>15}  {used:>13,}  "
              f"{100.0 * used / total:>15.2f}%  "
              f"{100.0 * thai_used / thai:>18.2f}%")
    print()

    n = args.n_per_country
    kept = sorted([k for k, v in geo.items() if v >= n],
                  key=lambda k: -geo[k])
    print(f"At Chewapreecha's own n = {n}, the countries retained from THIS "
          f"collection are:")
    for k in kept:
        print(f"    {k:<20} {geo[k]:>6,} available -> {n} used "
              f"({100.0 * n / geo[k]:.1f}% retained)")
    print()
    lost = sorted([(k, v) for k, v in geo.items() if v < n], key=lambda kv: -kv[1])
    print(f"Countries discarded entirely ({len(lost)}), "
          f"{sum(v for _, v in lost):,} genomes:")
    print("    " + ", ".join(f"{k} ({v})" for k, v in lost[:20]))
    if len(lost) > 20:
        print(f"    ... and {len(lost) - 20} more")
    print()
    print("  Read the last two blocks together. The rule throws away 99.6% of the")
    print("  Thai genomes and 100% of every country below the threshold - which is")
    print("  most of Africa, most of the Americas, and Papua New Guinea. It buys")
    print("  an unbiased comparison among the survivors at the price of saying")
    print("  nothing at all about anywhere else. State that limitation explicitly")
    print("  rather than letting the map imply global coverage.")
    print()
    print(f"  Chewapreecha resampled {CHEWAPREECHA_RESAMPLES:,} times and summarised")
    print("  across replicates. Do the same: the point of resampling is that the")
    print("  between-replicate spread IS the sampling-uncertainty estimate, and it")
    print("  is the number to report alongside any transition rate.")
    print()


# --------------------------------------------------------------------------
# (D) What predicted dateability
# --------------------------------------------------------------------------

def dateability(args):
    print(header("D. What predicted successful dating in the reference study?"))

    rows = load_clusters(args.clusters)
    for r in rows:
        r["n"] = int(r["n"])
        r["n_STs"] = int(r["n_STs"])
        r["year_span"] = int(r["year_span"])
        r["n_countries"] = int(r["n_countries"])
        r["dated"] = r["dated_in_paper"].strip().lower() == "true"
        # Derived predictors.
        r["st_per_iso"] = r["n_STs"] / r["n"]
        r["span_per_iso"] = r["year_span"] / r["n"]
        r["iso_per_year"] = r["n"] / max(r["year_span"], 1)

    dated = [r for r in rows if r["dated"]]
    undated = [r for r in rows if not r["dated"]]
    print(f"Clusters: {len(rows)} total, {len(dated)} dated, {len(undated)} not.")
    print(f"Dated: {', '.join(r['cluster'] for r in dated)}")
    print()

    predictors = [
        ("n (cluster size)", "n", "lower"),
        ("n_STs", "n_STs", "lower"),
        ("year_span", "year_span", "either"),
        ("n_countries", "n_countries", "either"),
        ("STs per isolate", "st_per_iso", "lower"),
        ("isolates per year of span", "iso_per_year", "higher"),
    ]

    print(f"  {'predictor':<28} {'dated median':>13} {'undated median':>15} "
          f"{'AUC':>7}  {'separates?':>11}")
    for label, key, _direction in predictors:
        d = sorted(r[key] for r in dated)
        u = sorted(r[key] for r in undated)
        auc = mann_whitney_auc([r[key] for r in dated],
                               [r[key] for r in undated])
        # AUC is symmetric about 0.5; report the informative direction.
        strength = abs(auc - 0.5) * 2
        verdict = ("strong" if strength >= 0.6 else
                   "weak" if strength >= 0.3 else "no")
        print(f"  {label:<28} {median(d):>13.3f} {median(u):>15.3f} "
              f"{auc:>7.3f}  {verdict:>11}")
    print()
    print("  AUC is the probability that a randomly chosen dated cluster scores")
    print("  above a randomly chosen undated one. 0.5 is no information; values")
    print("  far from 0.5 in either direction are informative.")
    print()
    print("  Caveat stated up front: 20 clusters, 5 of them dated. Nothing here")
    print("  survives a multiple-testing correction and none of it is a published")
    print("  result. It is a screen for deciding where to spend MCMC time, not an")
    print("  inference. Treat a cluster that fails it as 'try last', not 'skip'.")
    print()

    print("  The clusters that were dated, in full:")
    print(f"    {'cluster':<9} {'n':>4} {'STs':>4} {'span':>5} {'ctry':>5} "
          f"{'top country':<14}")
    for r in dated:
        print(f"    {r['cluster']:<9} {r['n']:>4} {r['n_STs']:>4} "
              f"{r['year_span']:>5} {r['n_countries']:>5} {r['top_country']:<14}")
    print()
    print("  The largest clusters that were NOT dated, for contrast:")
    for r in sorted(undated, key=lambda x: -x["n"])[:5]:
        print(f"    {r['cluster']:<9} {r['n']:>4} {r['n_STs']:>4} "
              f"{r['year_span']:>5} {r['n_countries']:>5} {r['top_country']:<14}")
    print()


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    if n == 0:
        return float("nan")
    return xs[n // 2] if n % 2 else 0.5 * (xs[n // 2 - 1] + xs[n // 2])


def mann_whitney_auc(pos, neg):
    """AUC via the Mann-Whitney U statistic, ties counted as half."""
    if not pos or not neg:
        return float("nan")
    wins = 0.0
    for a in pos:
        for b in neg:
            wins += 1.0 if a > b else (0.5 if a == b else 0.0)
    return wins / (len(pos) * len(neg))


# --------------------------------------------------------------------------
# (E) Temporal signal power
# --------------------------------------------------------------------------

def temporal_power(args):
    print(header("E. Can this cluster carry temporal signal at all?"))

    mu = args.rate            # substitutions per site per year
    L = args.length           # callable alignment length, sites
    print(f"Assumed clock rate      : {mu:.3g} substitutions/site/year")
    print(f"  95% HPD               : {args.rate_lo:.3g} - {args.rate_hi:.3g}")
    print(f"  Source                : Pearson et al. 2020, PLoS Pathog "
          f"16(3):e1008298, PMID 32149236")
    print(f"Assumed alignment length: {L:,} sites")
    print(f"  => {mu * L:.4g} substitutions per genome per year "
          f"({args.rate_lo * L:.3g} - {args.rate_hi * L:.3g})")
    print(f"  => one substitution every {1.0 / (mu * L):.1f} years on a lineage")
    print()
    print("  This rate is a WITHIN-HOST estimate from a chronic infection, and")
    print("  it is the prior Seng et al. 2024 used, so it is citable. But this")
    print("  organism is mostly a soil saprophyte, and short-timescale rates run")
    print("  fast; both biases inflate it, so node ages derived from it skew")
    print("  young. Override with --rate for your own estimate, and --length")
    print("  with your own callable core, per replicon.")
    print()

    print("Expected substitutions separating the oldest from the newest tip,")
    print("as a function of the sampling window. Below roughly 1, root-to-tip")
    print("regression has nothing to regress on and no clock model can rescue it.")
    print()
    print(f"  {'span (yr)':>10}  {'expected subs':>14}  {'verdict':<34}")
    for span in (2, 4, 5, 8, 10, 11, 15, 20, 30, 46, 50, 70):
        subs = mu * L * span
        if subs < 1:
            v = "cannot resolve one change"
        elif subs < MURRAY_DANGER_SUBS:
            v = "Murray false-confidence zone"
        elif subs < 20:
            v = "plausible, test formally"
        else:
            v = "adequate span"
        print(f"  {span:>10}  {subs:>14.2f}  {v:<34}")
    print()
    print(f"  The middle band is not a guess. Murray et al. 2016 (PMID 27110344)")
    print(f"  located their MRSA failure at \"fewer than {MURRAY_DANGER_SUBS:.0f} nucleotide")
    print(f"  substitutions per genome ... during this entire sampling period\" -")
    print(f"  the regime where \"the standard tests failed for the confounded")
    print(f"  subsample, resulting in false confidence.\" A cluster landing here")
    print(f"  will not merely fail to date; it can PASS an unclustered")
    print(f"  date-randomisation test and still be wrong.")
    print()

    # The convergence with section A.
    eff_years = args.effective_years
    eff_subs = mu * L * eff_years
    print(f"  Now put that next to section A. The EFFECTIVE temporal span of this")
    print(f"  collection - inverse Simpson on the collection-year distribution -")
    print(f"  is {eff_years:.1f} years, not the nominal 90. At this rate that is")
    print(f"  {eff_subs:.1f} expected substitutions across the whole sampling window.")
    if eff_subs < MURRAY_DANGER_SUBS * 1.5:
        print(f"  That lands the collection AS A WHOLE inside, or at the edge of,")
        print(f"  the Murray false-confidence zone. It is the single most")
        print(f"  persuasive number in this document for the claim that dating")
        print(f"  failure is the expected outcome rather than a defect of the")
        print(f"  analysis - and it is computed from the metadata alone, before")
        print(f"  any alignment exists.")
    print()

    print("Now the same check on the reference study's own clusters, which is the")
    print("only place the prediction can be scored against a known outcome:")
    print()
    rows = load_clusters(args.clusters)
    print(f"  {'cluster':<9} {'n':>4} {'span':>5} {'exp. subs':>10} "
          f"{'predicted':<12} {'actual':<10}")
    tp = fp = tn = fn = 0
    for r in sorted(rows, key=lambda x: -int(x["year_span"])):
        span = int(r["year_span"])
        subs = mu * L * span
        pred = subs >= args.min_subs
        actual = r["dated_in_paper"].strip().lower() == "true"
        if pred and actual:
            tp += 1
        elif pred and not actual:
            fp += 1
        elif not pred and actual:
            fn += 1
        else:
            tn += 1
        print(f"  {r['cluster']:<9} {int(r['n']):>4} {span:>5} {subs:>10.2f} "
              f"{'dateable' if pred else 'not':<12} "
              f"{'dated' if actual else 'not dated':<10}")
    print()
    n_dated = tp + fn
    n_undated = fp + tn
    print(f"  Threshold {args.min_subs:g} expected substitutions across the window:")
    print(f"    of {n_dated} clusters actually dated, {tp} pass and {fn} fail "
          f"(sensitivity {tp / max(n_dated, 1):.2f})")
    print(f"    of {n_undated} not dated,          {tn} fail and {fp} pass "
          f"(specificity {tn / max(n_undated, 1):.2f})")
    print()
    print("  THE FILTER DOES NOT WORK, AND THAT IS THE FINDING.")
    print()
    print("  Group 4 (span 8) and Group 7 (span 9) were dated. Group 3 (span 70),")
    print("  Group 1 (span 46), Group 18 (51) and the bin cluster (64) were not.")
    print("  Sampling window is anti-correlated with the outcome here, not")
    print("  correlated with it. Section D finds the same for cluster size, ST")
    print("  count, country count and isolates per year: every AUC sits near 0.5.")
    print()
    print("  So the honest planning assumption is that dateability CANNOT be")
    print("  triaged from cluster metadata. You cannot look at a cluster table and")
    print("  decide where to spend MCMC time. What actually decided it in the")
    print("  reference study was within-cluster diversity relative to the clock -")
    print("  a quantity that is not in any cluster summary table and has to be")
    print("  measured from the alignment.")
    print()
    print("  What this arithmetic IS good for is the physical floor. A cluster")
    print("  whose window cannot accumulate one substitution cannot be dated by")
    print("  any method, and that is worth checking before anything else. Above")
    print("  that floor, run the formal test on everything and expect most to")
    print("  fail: 5 of 19 in Chewapreecha, 1 of 10 sub-lineages in Seng.")
    print()


# --------------------------------------------------------------------------

def burden_vs_sampling(audit, args):
    print(header("F. Genomes per predicted case: the denominator"))

    geo = countries_only(audit.get("geo_loc_name", {}))
    by_region = OrderedDict((r, 0) for r in BURDEN_2015)
    unmapped = {}
    for country, n in geo.items():
        r = COUNTRY_REGION.get(country)
        if r is None:
            unmapped[country] = n
        else:
            by_region[r] += n
    total_mapped = sum(by_region.values())

    print("Burden from Limmathurotsakul et al. 2016, Nat Microbiol 1:15008,")
    print("PMID 26877885, Table 1 ('Estimated burden of melioidosis in 2015,")
    print("by continent'), cases in thousands per year with 95% CrI.")
    print("Genome counts from the NCBI audit, mapped to the same World Bank")
    print("regions.")
    print()
    print(f"  {'region':<27} {'cases/yr':>10} {'% burden':>9} "
          f"{'genomes':>8} {'% genomes':>10} {'gen/1k cases':>13}")
    rows = []
    for r, (cases, lo, hi, *_rest) in BURDEN_2015.items():
        n = by_region[r]
        pct_burden = 100.0 * cases / BURDEN_GLOBAL_CASES
        pct_gen = 100.0 * n / total_mapped if total_mapped else 0.0
        per_1k = (n / cases) if cases > 0 else float("nan")
        rows.append((r, cases, pct_burden, n, pct_gen, per_1k))
        cases_s = "<1" if cases < 1 else f"{cases:,.0f}k"
        per_s = "-" if cases <= 0 else f"{per_1k:,.1f}"
        print(f"  {r:<27} {cases_s:>10} {pct_burden:>8.1f}% "
              f"{n:>8,} {pct_gen:>9.1f}% {per_s:>13}")
    print(f"  {'-' * 27} {'-' * 10} {'-' * 9} {'-' * 8} {'-' * 10} {'-' * 13}")
    print(f"  {'Global':<27} {BURDEN_GLOBAL_CASES:>9,.0f}k {100.0:>8.1f}% "
          f"{total_mapped:>8,} {100.0:>9.1f}% "
          f"{total_mapped / BURDEN_GLOBAL_CASES:>13,.1f}")
    if unmapped:
        print()
        print(f"  Unmapped country labels ({sum(unmapped.values())} genomes): "
              f"{', '.join(sorted(unmapped))}")
    print()

    # The headline ratio.
    scored = [r for r in rows if r[1] > 0 and r[3] >= 0]
    scored.sort(key=lambda t: -t[5])
    if len(scored) >= 2:
        top, bot = scored[0], scored[-1]
        print(f"  Sampling intensity spans {top[5] / max(bot[5], 1e-9):,.0f}-fold "
              f"between {top[0]} ({top[5]:,.1f} genomes per 1,000")
        print(f"  predicted cases) and {bot[0]} ({bot[5]:,.1f}).")
    eap = dict((r[0], r) for r in rows).get("East Asia & Pacific")
    sa = dict((r[0], r) for r in rows).get("South Asia")
    ssa = dict((r[0], r) for r in rows).get("Sub-Saharan Africa")
    if eap and sa and ssa:
        print()
        print(f"  The three that matter:")
        print(f"    East Asia & Pacific  {eap[2]:>5.1f}% of burden, "
              f"{eap[4]:>5.1f}% of genomes")
        print(f"    South Asia           {sa[2]:>5.1f}% of burden, "
              f"{sa[4]:>5.1f}% of genomes")
        print(f"    Sub-Saharan Africa   {ssa[2]:>5.1f}% of burden, "
              f"{ssa[4]:>5.1f}% of genomes")
        print()
        print(f"  Per predicted case, East Asia & Pacific is sampled "
              f"{eap[5] / sa[5]:,.0f}x more heavily")
        print(f"  than South Asia and {eap[5] / ssa[5]:,.0f}x more heavily than "
              f"Sub-Saharan Africa.")
    print()
    print("  Verbatim from that paper's abstract: \"melioidosis is severely")
    print("  underreported in the 45 countries in which it is known to be endemic")
    print("  and ... melioidosis is likely endemic in a further 34 countries which")
    print("  have never reported the disease.\"")
    print()
    print("  And from the Results: \"We predict that only 40% of all melioidosis")
    print("  cases occur in the East Asia and Pacific region, where melioidosis is")
    print("  considered highly endemic. By contrast, South Asia is predicted to")
    print("  bear 44% of the overall burden.\"")
    print()
    print("  This is the strongest single argument in Gap 4 and it needs no model.")
    print("  The region predicted to carry the largest share of disease contributes")
    print("  a rounding error of the genomes. A discrete geographic state fitted to")
    print("  this collection is not estimating where the organism is; it is")
    print("  estimating where sequencing happened. Any migration rate involving an")
    print("  under-sampled region is estimated from close to no data, and any")
    print("  ancestral-area claim inherits that directly.")
    print()

    # ---- country level, from Supplementary Table 1 ----
    print(header("F2. The same comparison at country level"))
    print("Supplementary Information Table 1 of the same paper, retrieved")
    print("2026-08-09. Predicted cases/year with 95% CrI, against genome counts.")
    print("Footnotes are the table's own:  * endemic but under-reported,")
    print("+ predicted endemic but NEVER reported.")
    print()

    def burden_for(country):
        return BURDEN_COUNTRY.get(COUNTRY_ALIASES.get(country, country))

    scored = []
    for country, n in geo.items():
        b = burden_for(country)
        if b:
            scored.append((country, n, b[0], b[1], b[2], b[3]))
    # countries with burden but zero genomes
    have = {COUNTRY_ALIASES.get(c, c) for c in geo}
    missing = [(k, v) for k, v in BURDEN_COUNTRY.items() if k not in have]
    missing.sort(key=lambda t: -t[1][0])

    scored.sort(key=lambda t: -(t[1] / t[2]))
    print(f"  {'country':<22} {'genomes':>8} {'cases/yr':>10} "
          f"{'gen/1k cases':>13}  note")
    for c, n, cases, lo, hi, flag in scored:
        print(f"  {c:<22} {n:>8,} {cases:>10,} {1000.0 * n / cases:>13,.1f}  {flag}")
    print()

    if scored:
        top, bot = scored[0], scored[-1]
        print(f"  Sampling intensity spans "
              f"{(top[1]/top[2]) / (bot[1]/bot[2]):,.0f}-fold across countries,")
        print(f"  from {top[0]} to {bot[0]}.")
        aus = next((s for s in scored if s[0] == "Australia"), None)
        ind = next((s for s in scored if s[0] == "India"), None)
        tha = next((s for s in scored if s[0] == "Thailand"), None)
        if aus and ind:
            print(f"  Australia is sampled {(aus[1]/aus[2]) / (ind[1]/ind[2]):,.0f}x "
                  f"more heavily per predicted case than India,")
        if tha and ind:
            print(f"  and Thailand {(tha[1]/tha[2]) / (ind[1]/ind[2]):,.0f}x more "
                  f"heavily than India.")
    print()

    print("  Countries with predicted burden and ZERO genomes in the collection,")
    print("  ranked by predicted cases per year:")
    shown = 0
    for k, (cases, lo, hi, flag) in missing:
        if cases < 100:
            continue
        print(f"    {k:<26} {cases:>7,} cases/yr  ({lo:,}-{hi:,})  {flag}")
        shown += 1
    tot_missing = sum(v[0] for _, v in missing)
    print()
    print(f"  {shown} countries above 100 predicted cases/year have no genomes at all.")
    print(f"  Across every country with zero genomes, the predicted burden totals")
    print(f"  {tot_missing:,} cases per year - {100.0 * tot_missing / (BURDEN_GLOBAL_CASES * 1000):.0f}% "
          f"of the global estimate.")
    print()
    print("  Read the two lists together. Indonesia is the second-highest-burden")
    print("  country on earth for this organism and contributes nothing. Nigeria,")
    print("  Myanmar and the Philippines are in the same position. Meanwhile")
    print("  Australia, at 149 predicted cases a year, contributes 586 genomes.")
    print("  No discrete-trait model can repair a state space in which the")
    print("  highest-burden states are absent and the lowest-burden ones are")
    print("  saturated - the states simply are not comparable observations.")
    print()


def header(title):
    bar = "=" * 74
    return f"\n{bar}\n{title}\n{bar}"


def main():
    ap = argparse.ArgumentParser(
        description="Gap 4 companion: sampling-frame and phylogeography "
                    "diagnostics for B. pseudomallei.")
    ap.add_argument("--audit", default=DEFAULT_AUDIT,
                    help="NCBI audit CSV (category,key,count,pct_of_total)")
    ap.add_argument("--clusters", default=DEFAULT_CLUSTERS,
                    help="Per-cluster summary CSV")
    ap.add_argument("--section", default="ABCDEF",
                    help="Subset of ABCDEF to run (default all)")
    ap.add_argument("--n-per-country", type=int,
                    default=CHEWAPREECHA_N_PER_COUNTRY,
                    help="Balanced-subsample threshold (default 15, "
                         "Chewapreecha 2017)")
    ap.add_argument("--rate", type=float, default=BP_RATE,
                    help="Clock rate, substitutions/site/year "
                         "(default 1.7e-7, Pearson et al. 2020 PMID 32149236; "
                         "see --rate-lo/--rate-hi for the HPD)")
    ap.add_argument("--length", type=int, default=3_805_619,
                    help="Callable alignment length in sites "
                         "(default: Wu et al. 2026 core, 52.5%% of K96243)")
    ap.add_argument("--rate-lo", type=float, default=BP_RATE_LO,
                    help="Lower 95%% HPD on the clock rate (default 1.3e-7)")
    ap.add_argument("--rate-hi", type=float, default=BP_RATE_HI,
                    help="Upper 95%% HPD on the clock rate (default 2.1e-7)")
    ap.add_argument("--effective-years", type=float, default=11.05,
                    help="Effective temporal span in independent-year "
                         "equivalents; default 11.05 is the inverse-Simpson "
                         "value computed by section A on this audit")
    ap.add_argument("--min-subs", type=float, default=MURRAY_DANGER_SUBS,
                    help="Expected substitutions across the sampling window "
                         "below which a cluster is called undateable "
                         "(default 5; see section E, the filter fails "
                         "validation and is reported as such)")
    args = ap.parse_args()

    for path in (args.audit, args.clusters):
        if not os.path.exists(path):
            sys.exit(f"missing input: {path}")

    audit = load_audit(args.audit)
    sec = args.section.upper()

    if "A" in sec:
        sampling_frame(audit, args)
    if "B" in sec:
        root_state_demo(audit, args)
    if "C" in sec:
        subsample_design(audit, args)
    if "D" in sec:
        dateability(args)
    if "E" in sec:
        temporal_power(args)
    if "F" in sec:
        burden_vs_sampling(audit, args)


if __name__ == "__main__":
    main()
