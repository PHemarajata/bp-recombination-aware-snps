#!/usr/bin/env python3
"""
Feasibility arithmetic for applying SKA2 to Burkholderia pseudomallei.

Two questions:
  1. Where does B. pseudomallei sit on SKA2's published recall-vs-divergence curve?
  2. How much memory would `ska align` / `ska build` need at a given sample count?

Both are estimates from published anchors, not measurements. They are here so the
assumptions are visible and so the numbers can be re-derived when better inputs
(e.g. a measured within-cluster Mash distance) become available.

Published anchors
-----------------
Divergence landmarks: Derelle et al. 2024, Genome Res 34(10):1661-1673,
  PMID 39406504, doi:10.1101/gr.279449.124, Figure 2.
    pi <= 0.0005 SNPs/site ("within lineage") -> recall > 99%
    pi <= 0.005  SNPs/site ("within strain")  -> recall ~ 90%
    pi >= 0.05   SNPs/site ("whole species")  -> recall 10-50%

B. pseudomallei segregating sites: Chewapreecha et al. 2017, Nat Microbiol 2:16263,
  PMID 28112723, doi:10.1038/nmicrobiol.2016.263 -- 469 globally distributed
  isolates mapped to K96243 chromosomes I+II, 324,637 SNPs.

Memory calibration points, both from PMID 39406504:
    28 S. pneumoniae (same strain, ~2.1 Mb): 3.2e6 split-mers, 38 MB SKF on disk
    240 S. pneumoniae PMEN1 via `ska map` vs Spn23F: 3.6 GB peak RAM
"""

import math

# --- K96243 reference (GCA_000011545.1) ---
CHR1 = 4_074_542   # NC_006350.1
CHR2 = 3_173_005   # NC_006351.1
REF_LEN = CHR1 + CHR2

# --- Chewapreecha et al. 2017 ---
SEGREGATING_SITES = 324_637
N_ISOLATES = 469

# --- SKA2 recall landmarks (Derelle et al. 2024, Fig 2) ---
LANDMARKS = [
    ("within lineage", 0.0005, ">99%"),
    ("within strain",  0.005,  "~90%"),
    ("whole species",  0.05,   "10-50%"),
]


def harmonic(n):
    """a_n = sum_{i=1}^{n-1} 1/i, the Watterson normalisation constant."""
    return sum(1.0 / i for i in range(1, n))


def species_diversity(callable_fraction=1.0):
    """
    Watterson's theta per site, used as a stand-in for average pairwise
    divergence pi. Assumes neutrality and panmixia; B. pseudomallei satisfies
    neither, so under clade structure the true pi is typically HIGHER than this.
    Treat the result as a lower bound.
    """
    density = SEGREGATING_SITES / (REF_LEN * callable_fraction)
    return density / harmonic(N_ISOLATES)


def split_mers(n_samples, seg_sites, ref_len=REF_LEN, k=31):
    """
    Distinct split-mer keys.

    A segregating site changes the *key* of every split-mer whose flank spans it
    -- about (k-1) of them -- while the split-mer centred on the site itself
    varies only in its stored middle base, so contributes no new key. Baseline is
    one split-mer per reference position.
    """
    return ref_len + seg_sites * (k - 1)


def align_memory_gb(n_samples, seg_sites, k=31, calibration=5.0):
    """
    Peak memory for holding the merged split-mer dictionary.

    The dominant term is the middle-base matrix: one byte per sample per
    split-mer. Keys add 8 bytes each for k <= 31 (64-bit packing).

    `calibration` accounts for allocator overhead, the per-split-mer sample
    counts, and hash-table load factor. It is set to 5.0 by reproducing the
    published 240-genome / 3.6 GB PMEN1 figure -- see calibrate() below. It is a
    crude single-point fit, so treat these as order-of-magnitude only.
    """
    n_sm = split_mers(n_samples, seg_sites, k=k)
    raw_bytes = n_sm * (8 + n_samples)
    return calibration * raw_bytes / 1e9


def calibrate():
    """Reproduce the published 240-genome PMEN1 `ska map` figure of 3.6 GB."""
    spn_len = 2_100_000
    pmen1_seg_sites = 30_000          # order of magnitude for a single strain
    n_sm = split_mers(240, pmen1_seg_sites, ref_len=spn_len)
    raw_gb = n_sm * (8 + 240) / 1e9
    return raw_gb, 3.6 / raw_gb


def main():
    print("=" * 74)
    print("1. WHERE DOES B. PSEUDOMALLEI SIT ON THE SKA2 RECALL CURVE?")
    print("=" * 74)
    print(f"K96243 length            : {REF_LEN:,} bp "
          f"(chr I {CHR1:,} + chr II {CHR2:,})")
    print(f"Segregating sites        : {SEGREGATING_SITES:,} across n={N_ISOLATES}")
    print(f"Segregating-site density : {SEGREGATING_SITES/REF_LEN:.5f} per site")
    print(f"a_n                      : {harmonic(N_ISOLATES):.4f}")
    print()

    pi = species_diversity()
    print(f"Species-wide pi (Watterson): {pi:.5f} SNPs/site  "
          f"(~{100*(1-pi):.2f}% ANI)")
    print(f"  ~= {pi*REF_LEN:,.0f} SNPs between two random genomes")
    print()
    print("  Sensitivity to the callable-core assumption:")
    for frac in (1.00, 0.90, 0.85, 0.80):
        p = species_diversity(frac)
        print(f"    callable core {frac:.0%} of ref -> pi = {p:.5f} "
              f"({100*(1-p):.2f}% ANI)")
    print()

    print("  Against the SKA2 landmarks:")
    for label, d, recall in LANDMARKS:
        print(f"    {label:<15} pi ~ {d:<7} recall {recall:<8} "
              f"-> B. pseudomallei is {pi/d:>5.1f}x this")
    print()
    print("  Read: species-wide diversity is just past the 'strain' boundary")
    print("  where recall is ~90%, and roughly 7x BELOW the 'species' regime")
    print("  where recall collapses. Per-cluster it should be comfortably safe.")
    print()
    print("  CAVEAT: Watterson's theta assumes neutrality and panmixia. Under the")
    print("  clade structure B. pseudomallei actually has, pairwise pi is usually")
    print("  higher. Treat 0.0067 as a lower bound; 0.01 is a plausible upper one,")
    print("  and even that stays 5x below the collapse regime.")
    print()

    print("=" * 74)
    print("2. MEMORY")
    print("=" * 74)
    raw_gb, factor = calibrate()
    print(f"Calibration: 240 PMEN1 genomes, naive estimate {raw_gb:.2f} GB vs "
          f"3.6 GB published")
    print(f"  -> calibration factor {factor:.1f}x (using {5.0:.1f}x below)")
    print()
    print(f"{'n genomes':>10} {'seg sites':>12} {'split-mers':>14} {'est. RAM':>12}")
    print("-" * 52)

    a469 = harmonic(N_ISOLATES)
    for n in (100, 200, 500, 1000, 3000, 5728):
        # segregating sites scale with the harmonic number
        seg = SEGREGATING_SITES * harmonic(n) / a469
        gb = align_memory_gb(n, seg)
        print(f"{n:>10,} {seg:>12,.0f} {split_mers(n, seg):>14,.0f} "
              f"{gb:>9.1f} GB")
    print()
    print("Per-cluster, where within-cluster diversity is far lower:")
    print(f"{'n genomes':>10} {'seg sites':>12} {'split-mers':>14} {'est. RAM':>12}")
    print("-" * 52)
    for n, seg in ((100, 20_000), (200, 30_000), (500, 50_000)):
        gb = align_memory_gb(n, seg)
        print(f"{n:>10,} {seg:>12,} {split_mers(n, seg):>14,.0f} "
              f"{gb:>9.1f} GB")
    print()
    print("Read: species-wide `ska align` on the full collection is not viable on")
    print("ordinary hardware; per-cluster runs are cheap. This reproduces, from")
    print("resource arithmetic alone, the partition-first advice the SKA authors")
    print("give on accuracy grounds.")
    print()
    print("REPLACE THESE ESTIMATES WITH A MEASUREMENT. Run `ska build` + `ska align`")
    print("on one existing cluster and record peak RSS; that single number")
    print("calibrates the whole table.")


if __name__ == "__main__":
    main()
