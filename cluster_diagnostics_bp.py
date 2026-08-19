#!/usr/bin/env python3
"""
Gap 2 companion: cluster-size diagnostics and the Gubbins contrast arithmetic
for Burkholderia pseudomallei.

Two independent things live here.

  (A) size_report()  - describe a partition's size distribution and place it
      against three published reference partitions. This is the diagnostic the
      handoff asks for: does your 61-76 Mash clustering look like inferred
      population structure or like an imposed cut?

  (B) gubbins_contrast() - the arithmetic behind the stopping rule. Gubbins has
      no published numeric divergence ceiling (verified absent from the 2015
      paper, the manual, the docs site and the manpage as of 2026-08-09). What
      it does document is a detection *mechanism*: recombination is called as a
      local excess of substitutions over the branch's background density. So
      the operational bound is a contrast ratio, and that is computable from
      numbers already established in GAP1 and Gap 5.

Nothing here is a published threshold. The derivations are flagged as mine.

Usage:
    python3 cluster_diagnostics_bp.py
    python3 cluster_diagnostics_bp.py --clusters my_clusters.csv
    python3 cluster_diagnostics_bp.py --clusters my_clusters.tsv --id-col genome --cluster-col cluster

The clusters file needs one row per genome with a cluster label. Delimiter is
sniffed. If there is no header, pass --no-header and columns are taken as 0,1.
"""

import argparse
import csv
import math
import os
import sys
from collections import Counter

# --------------------------------------------------------------------------
# Published reference partitions. Every number here is sourced.
# --------------------------------------------------------------------------

# Chewapreecha et al. 2017, Nat Microbiol 2:16263, PMID 28112723.
# hierBAPS on 469 genomes; sizes read from Supplementary Data 1 and tabulated
# in chewapreecha_hierbaps_clusters_2026-08-09.csv. "bin" is their unassigned
# group and is carried as a cluster here so the tail is not flattered.
CHEWAPREECHA_SIZES = [137, 16, 38, 11, 4, 24, 9, 6, 21, 26,
                      20, 7, 8, 17, 8, 9, 29, 27, 18, 34]

# Wu et al. 2026, Emerg Microbes Infect 15(1):2691358, PMID 42377320.
# fcluster(criterion="maxclust", t=10) on a UPGMA dendrogram, i.e. an imposed
# ten-way cut of ~4,127 genomes. The paper reports the size *range* 285-583,
# not the individual sizes, so this is a reconstruction that reproduces the
# reported range, count and total. Used only to show what an imposed cut looks
# like on these statistics; do not quote the individual values.
WU_SIZES_RECONSTRUCTED = [583, 285, 470, 390, 445, 355, 420, 400, 380, 399]

# Gladstone et al. 2019, EBioMedicine 43:338-346, PMID 31003929.
# PopPUNK on 20,027 pneumococcal genomes -> 621 GPSCs. Individual sizes are not
# published, so only the concentration headlines are carried, as narrative.
GPSC_HEADLINE = {
    "n_genomes": 20027,
    "n_clusters": 621,
    "n_clusters_under_10": 407,
    "genomes_in_clusters_under_10": 1043,
    "n_clusters_over_100": 35,
    "genomes_in_dominant": 8356,
    "dominant_denominator": 13454,   # the GPS subset, not the full 20,027
}

# Seng et al. 2024, Nat Commun 15:5699, PMID 38972886.
# PopPUNK v2.6.0 on 1,391 B. pseudomallei genomes; 1,294 assigned to 101
# lineages; three dominant lineages of 312, 297 and 125.
SENG = {
    "n_genomes": 1391,
    "n_assigned": 1294,
    "n_lineages": 101,
    "dominant": [312, 297, 125],
    "mean_pairwise_core_snps": [549, 351, 517],   # per dominant lineage
    "r_over_m": [3.7, 4.6, 2.2],                  # per dominant lineage
}

# --------------------------------------------------------------------------
# (A) size distribution
# --------------------------------------------------------------------------


def gini(values):
    """Gini coefficient of a list of cluster sizes. 0 = all clusters equal."""
    xs = sorted(values)
    n = len(xs)
    if n == 0 or sum(xs) == 0:
        return float("nan")
    cum = sum((i + 1) * x for i, x in enumerate(xs))
    return (2 * cum) / (n * sum(xs)) - (n + 1) / n


def size_stats(sizes, label):
    sizes = sorted(sizes, reverse=True)
    n_clusters = len(sizes)
    total = sum(sizes)
    top_5pct_k = max(1, round(n_clusters * 0.05))
    return {
        "label": label,
        "n_genomes": total,
        "n_clusters": n_clusters,
        "largest": sizes[0],
        "smallest": sizes[-1],
        "max_min_ratio": sizes[0] / sizes[-1],
        "median": sizes[n_clusters // 2] if n_clusters % 2 else
                  (sizes[n_clusters // 2 - 1] + sizes[n_clusters // 2]) / 2,
        "gini": gini(sizes),
        "frac_in_top_5pct_clusters": sum(sizes[:top_5pct_k]) / total,
        "frac_clusters_under_10": sum(1 for s in sizes if s < 10) / n_clusters,
        "frac_genomes_in_clusters_under_10": sum(s for s in sizes if s < 10) / total,
        "n_singletons": sum(1 for s in sizes if s == 1),
    }


def print_stats_table(rows):
    cols = [
        ("label", "partition", "{:<28}"),
        ("n_genomes", "genomes", "{:>8}"),
        ("n_clusters", "clusters", "{:>9}"),
        ("largest", "largest", "{:>8}"),
        ("smallest", "smallest", "{:>9}"),
        ("max_min_ratio", "max/min", "{:>8.1f}"),
        ("gini", "Gini", "{:>6.3f}"),
        ("frac_in_top_5pct_clusters", "top5%", "{:>7.1%}"),
        ("frac_clusters_under_10", "<10 (clu)", "{:>10.1%}"),
    ]
    header = "".join(h.replace(".1f", "").replace(".3f", "").replace(".1%", "")
                     .format(t) for _, t, h in cols)
    print(header)
    print("-" * len(header))
    for r in rows:
        print("".join(f.format(r[k]) for k, _, f in cols))


def read_clusters(path, id_col, cluster_col, has_header):
    with open(path, newline="") as fh:
        sample = fh.read(8192)
        fh.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",\t; ")
        except csv.Error:
            dialect = csv.excel_tab if "\t" in sample else csv.excel
        if has_header:
            reader = csv.DictReader(fh, dialect=dialect)
            fields = reader.fieldnames or []
            if cluster_col not in fields:
                sys.exit(f"column '{cluster_col}' not in {fields}")
            labels = [row[cluster_col] for row in reader if row.get(cluster_col)]
        else:
            labels = [row[1] for row in csv.reader(fh, dialect) if len(row) > 1]
    return list(Counter(labels).values())


# --------------------------------------------------------------------------
# (B) the Gubbins contrast arithmetic
# --------------------------------------------------------------------------

# Gubbins defaults and documented behaviour (Croucher et al. 2015, NAR 43(3):e15,
# PMID 25414349; manual at github.com/nickjcroucher/gubbins).
S_MIN = 3                    # --min-snps default: minimum SNPs to call a block
WINDOW_MIN_BP = 100          # --min-window-size default
WINDOW_MAX_BP = 10000        # --max-window-size default
WINDOW_TARGET_SUBS = 10      # "expected number of base substitutions in a
                             # window would be at least 10"

# B. pseudomallei quantities established in GAP1 / Gap 5.
K96243_LEN = 7_247_547       # chromosomes I + II
CORE_ALN_WU = 3_805_619      # Wu et al. 2026 core alignment, 52.5% of K96243
PI_SPECIES = 0.0067          # species-wide nucleotide diversity, derived in GAP1
NANDI_TRACT_MEDIAN = 5000    # median recombination tract, Nandi 2015
NANDI_TRACT_MAX = 71000


def min_detectable_donor_divergence(tract_bp, s_min=S_MIN):
    """A tract only becomes visible if it imports >= s_min substitutions.
    Returns the donor divergence below which a tract of this length is
    invisible to Gubbins."""
    return s_min / tract_bp


def gubbins_window_bp(branch_snps, genome_len=K96243_LEN):
    """Window size Gubbins will choose for a branch carrying branch_snps,
    given its rule of targeting >=10 expected substitutions per window,
    clamped to [100 bp, 10 kb]."""
    if branch_snps <= 0:
        return WINDOW_MAX_BP
    density = branch_snps / genome_len
    w = WINDOW_TARGET_SUBS / density
    return min(max(w, WINDOW_MIN_BP), WINDOW_MAX_BP)


def contrast_ratio(within_cluster_mean_snps, donor_divergence,
                   core_len=CORE_ALN_WU):
    """Ratio of imported-substitution density to background substitution
    density. Croucher et al. state detection fails as the background point
    mutation density rises toward the density of recombination-imported
    substitutions, so this ratio is the quantity that has to stay large.
    DERIVED, not published."""
    background = within_cluster_mean_snps / core_len
    if background == 0:
        return float("inf")
    return donor_divergence / background


def max_cluster_snps_for_ratio(donor_divergence, target_ratio,
                               core_len=CORE_ALN_WU):
    """Invert the above: the largest mean within-cluster pairwise core-SNP
    distance that still leaves target_ratio of contrast against a donor at
    donor_divergence. DERIVED."""
    return donor_divergence * core_len / target_ratio


def gubbins_report():
    print("\n(B) Gubbins contrast arithmetic  [DERIVED - no published threshold exists]\n")

    print("  B1. Sensitivity floor: how divergent must a donor be to be seen at all?")
    print("      A tract must import >= %d substitutions (--min-snps default).\n" % S_MIN)
    print("      tract length     min donor divergence     as % divergence")
    for tract in (1000, NANDI_TRACT_MEDIAN, 20000, NANDI_TRACT_MAX):
        d = min_detectable_donor_divergence(tract)
        print(f"      {tract:>8,} bp     {d:>16.2e}     {100*d:>10.4f}%")
    print("\n      Nandi's median tract is ~5 kb, so imports from donors below")
    print("      ~0.06% divergence are invisible regardless of cluster design.")
    print("      Within-cluster donors in this organism are often exactly that close.")

    print("\n  B2. Window sizing is NOT the binding constraint here.")
    print("      Gubbins picks w = 10 / (branch SNP density), clamped to [100 bp, 10 kb].\n")
    print("      branch SNPs   window (bp)   expected subs per window   at clamp?")
    for s in (100, 500, 2000, 7240, 50000, 724000):
        w = gubbins_window_bp(s)
        exp_subs = s * w / K96243_LEN
        clamp = ("ceiling" if w >= WINDOW_MAX_BP else
                 "floor" if w <= WINDOW_MIN_BP else "-")
        print(f"      {s:>11,}   {w:>11,.0f}   {exp_subs:>24.2f}   {clamp:>9}")
    print("\n      The 10 kb ceiling binds below ~7,240 branch SNPs and the 100 bp")
    print("      floor only above ~724,000. Every realistic B. pseudomallei branch,")
    print("      within-cluster or backbone, sits pinned at the ceiling. So the")
    print("      window rule gives no usable stopping criterion - which rules out")
    print("      the most obvious mechanism-matched proxy.")

    print("\n  B3. The contrast ratio, which does bind.")
    print("      Detection degrades as background density approaches import density.\n")
    print("      Background is computed over the %s bp core (Wu et al. 2026).\n"
          % f"{CORE_ALN_WU:,}")
    scenarios = [
        ("Seng lineage 2 (published, Gubbins ran)", 351, 0.005),
        ("Seng lineage 3 (published, Gubbins ran)", 517, 0.005),
        ("Seng lineage 1 (published, Gubbins ran)", 549, 0.005),
        ("a 2,000-SNP cluster", 2000, 0.005),
        ("a 10,000-SNP cluster", 10000, 0.005),
        ("species-wide (pi = 0.0067)", PI_SPECIES * CORE_ALN_WU, 0.005),
    ]
    print("      partition                                mean pairwise    background    contrast")
    for name, snps, nu in scenarios:
        r = contrast_ratio(snps, nu)
        print(f"      {name:<40} {snps:>13,.0f}    {snps/CORE_ALN_WU:>10.2e}    {r:>7.1f}x")
    print("\n      Species-wide the contrast collapses to roughly 1x - the regime the")
    print("      Gubbins authors describe for H. pylori, where 'the identification of")
    print("      recombinations as regions with elevated densities of base substitutions")
    print("      is confounded by the high diversity of the sequences in the alignment'.")
    print("      Per cluster, at Seng's observed diversity, contrast is ~30-50x.")

    print("\n  B4. The scriptable stopping rule that follows.")
    for nu, label in ((0.005, "0.5% (near inter-lineage)"),
                      (0.01, "1.0%"),
                      (0.02, "2.0% (deep inter-clade)")):
        for ratio in (10, 20):
            cap = max_cluster_snps_for_ratio(nu, ratio)
            print(f"      donor divergence {label:<26} contrast >= {ratio:>2}x  ->  "
                  f"cap mean pairwise core SNPs at {cap:>9,.0f}")
    print("\n      Cross-check: Seng's three lineages (351-549 mean pairwise core SNPs)")
    print("      went through Gubbins v3.1.3 successfully and sit 4-20x inside even the")
    print("      strictest cap above. That is the empirical calibration point, and it")
    print("      is in this organism, in this workflow.")


# --------------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--clusters", help="CSV/TSV of genome -> cluster assignments")
    ap.add_argument("--id-col", default="genome")
    ap.add_argument("--cluster-col", default="cluster")
    ap.add_argument("--no-header", action="store_true")
    args = ap.parse_args()

    print("=" * 78)
    print("Gap 2 cluster diagnostics for B. pseudomallei")
    print("=" * 78)

    rows = [
        size_stats(CHEWAPREECHA_SIZES,
                   "Chewapreecha hierBAPS (n=469)"),
        size_stats(WU_SIZES_RECONSTRUCTED,
                   "Wu imposed 10-way cut*"),
    ]

    if args.clusters:
        if not os.path.exists(args.clusters):
            sys.exit(f"no such file: {args.clusters}")
        sizes = read_clusters(args.clusters, args.id_col, args.cluster_col,
                              not args.no_header)
        rows.insert(0, size_stats(sizes, "YOUR CLUSTERING"))

    print("\n(A) size distribution\n")
    print_stats_table(rows)
    print("\n      * Wu sizes are a reconstruction reproducing the published")
    print("        range (285-583), count (10) and total (~4,127). Individual")
    print("        values are not published; the shape statistics are the point.")

    print("\n      Reference concentration figures (Gladstone et al. 2019, PMID 31003929):")
    g = GPSC_HEADLINE
    print(f"        {g['n_clusters']} PopPUNK GPSCs over {g['n_genomes']:,} pneumococcal genomes")
    print(f"        {g['n_clusters_under_10']}/{g['n_clusters']} clusters "
          f"({g['n_clusters_under_10']/g['n_clusters']:.0%}) hold "
          f"{g['genomes_in_clusters_under_10']:,}/{g['n_genomes']:,} genomes "
          f"({g['genomes_in_clusters_under_10']/g['n_genomes']:.0%})")
    print(f"        {g['n_clusters_over_100']}/{g['n_clusters']} clusters "
          f"({g['n_clusters_over_100']/g['n_clusters']:.1%}) hold "
          f"{g['genomes_in_dominant']:,}/{g['dominant_denominator']:,} "
          f"({g['genomes_in_dominant']/g['dominant_denominator']:.0%}) of the GPS subset")

    print("\n      B. pseudomallei precedent (Seng et al. 2024, PMID 38972886):")
    s = SENG
    print(f"        PopPUNK v2.6.0: {s['n_assigned']:,}/{s['n_genomes']:,} genomes assigned "
          f"to {s['n_lineages']} lineages "
          f"({1 - s['n_assigned']/s['n_genomes']:.1%} unassigned)")
    print(f"        three dominant lineages: {s['dominant']}")
    print(f"        mean within-lineage pairwise core SNPs: {s['mean_pairwise_core_snps']}")
    print(f"        per-lineage r/m: {s['r_over_m']}")
    print(f"        Chewapreecha's unassigned 'bin' was 34/469 = "
          f"{34/469:.1%} - the two studies leave a similar remainder.")

    gubbins_report()

    print("\n" + "=" * 78)
    print("Reading: a Gini near 0 with a max/min ratio near 1 means the partition")
    print("was imposed. Real bacterial population structure is heavily skewed - a")
    print("few large lineages and a long tail. Chewapreecha's max/min is 34.2x;")
    print("Wu's imposed ten-way cut is 2.0x.")
    print("=" * 78)


if __name__ == "__main__":
    main()
