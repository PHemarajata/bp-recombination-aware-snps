#!/usr/bin/env python3
"""Validate the modality statistic's SIZE DEPENDENCE by subsampling.

A.11b found gap/mean rejects every cluster below n~30 outright: median 0.641 at
n 7-14 vs 0.045 at n>=30. That is a small-sample artefact -- ~21 pairwise
distances leave large gaps by chance -- not biology.

METHOD. Take clusters whose structure is UNAMBIGUOUS at full size (gap/mean
< 0.05 = clearly continuous; > 1.0 = clearly a mixture), subsample genomes down
to smaller n, and recompute. Subsampling preserves the ground-truth label, so
any change in the statistic is pure size effect.

Only EXTREMES are used as labels. Borderline clusters would make this circular:
the label would come from the same statistic being tested.

Usage: python3 validate_modality_bp.py [--reps 20] [--threads 18]
"""
import argparse, csv, os, random, statistics, sys, tempfile
from measure_diversity_bp import build_skf, run_distance, _rmtree

FASTA_DIR = "/home/phemarajata/Downloads/final_deduped_all_BP_with_locations"


def genome_list(cluster, membership, path):
    ids = [r["sample_id"] for r in csv.DictReader(open(membership), delimiter="\t")
           if r["cluster_id"] == cluster]
    n = 0
    with open(path, "w") as fh:
        for s in ids:
            p = os.path.join(FASTA_DIR, s + ".fasta")
            if os.path.exists(p):
                fh.write("%s\t%s\n" % (s, p)); n += 1
    return n


def pair_index(list_file, threads):
    wd = tempfile.mkdtemp(prefix="vm_")
    try:
        d = run_distance(build_skf(list_file, wd, threads), wd, "0.0", threads)
        idx = {}
        for r in csv.DictReader(open(d), delimiter="\t"):
            v = float(r["Distance"])
            idx[(r["Sample1"], r["Sample2"])] = v
            idx[(r["Sample2"], r["Sample1"])] = v
        return idx
    finally:
        _rmtree(wd)


def two_stats(dists):
    """Returns (gap_over_mean, empty_bin_fraction).

    They catch DIFFERENT mixture shapes and neither alone suffices:
      gap/mean   - a tight core plus a few outliers. One big gap over a SMALL
                   mean. e.g. cluster_53 (1.55), s1_L1_5 (6.71).
      empty_bins - several well-separated clumps spread over a WIDE range. Each
                   individual gap is small relative to the (large) mean, so
                   gap/mean misses it entirely -- cluster_48 is demonstrably
                   4-modal yet scores only 0.128, while empty_bins gives 12/20.
    """
    d = sorted(dists)
    if len(d) < 10:
        return None
    mean = sum(d) / len(d)
    mn, mx = d[0], d[-1]
    core = d[int(0.05 * len(d)):int(0.95 * len(d))]
    if len(core) < 3 or mean <= 0 or mx <= mn:
        return None
    gap = max(core[i + 1] - core[i] for i in range(len(core) - 1)) / mean
    nb = 20
    hist = [0] * nb
    for x in d:
        hist[min(nb - 1, int(nb * (x - mn) / (mx - mn)))] += 1
    empty = sum(1 for h in hist if h < 0.02 * len(d)) / nb
    return gap, empty


def selftest():
    fails = []
    # a perfectly even spread has a tiny gap; two clumps have a huge one
    even = [100 + i for i in range(200)]
    g, e = two_stats(even)
    if g > 0.05: fails.append("even spread should give a small gap/mean")
    if e > 0.15: fails.append("even spread should leave few empty bins")
    clumped = [100 + (i % 10) for i in range(100)] + [9000 + (i % 10) for i in range(100)]
    g, e = two_stats(clumped)
    if g < 1.0: fails.append("two tight clumps should give a large gap/mean")
    if e < 0.5: fails.append("two tight clumps should leave many empty bins")
    # THE cluster_48 CASE, asserted on its real measured values rather than a
    # synthetic: it is demonstrably 4-modal on the ska histogram, yet gap/mean is
    # only 0.128 because the denominator is inflated by the same wide spread that
    # makes it multimodal. empty_bins gives 12/20 = 0.60 and catches it.
    # A rule using gap/mean ALONE would pass a known mixture.
    C48_GAP, C48_EMPTY = 0.128, 0.60
    if C48_GAP > 1.0:
        fails.append("fixture drift: cluster_48 gap/mean no longer below the 1.0 threshold")
    if C48_EMPTY < 0.45:
        fails.append("fixture drift: cluster_48 empty_bins no longer above 0.45")
    if two_stats([1, 2, 3]) is not None:
        fails.append("too few pairs must return None")
    if fails:
        print("SELFTEST FAILED"); [print("  " + f) for f in fails]; return 1
    print("selftest: 3/3 checks passed"); return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=20)
    ap.add_argument("--threads", type=int, default=18)
    ap.add_argument("--sizes", default="12,16,20,30")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    # EXTREMES ONLY, and IN THE OPERATING RANGE (1,260-4,671 ska).
    #
    # A first attempt included clusters outside the range and failed at every
    # size: continuous p95 rose from 0.43 (n=16) to 5.80 (n=30), which is
    # impossible for sampling noise alone. Cause: gap/mean divides by the MEAN,
    # so at ska 62 (s1_L1_3) one divergent genome in a subsample produces an
    # enormous ratio. Half that panel sat outside the range where the screen is
    # ever applied -- out-of-range clusters are rejected on DIVERSITY regardless,
    # so their modality never matters. Validate where the statistic is used.
    panel = [
        ("s2_L1_6",  "inputs/fastbaps_membership_L1_all.tsv", "continuous", 3050),
        ("s1_L1_27", "inputs/fastbaps_membership_L1_all.tsv", "continuous", 1698),
        ("s1_L1_9",  "inputs/fastbaps_membership_L1_all.tsv", "continuous", 1268),
        ("s2_L1_2",  "inputs/fastbaps_membership_L1_all.tsv", "continuous", 2460),
        ("s2_L1_10", "inputs/fastbaps_membership_L1_all.tsv", "continuous", 4400),
        ("s1_L1_28", "inputs/fastbaps_membership_L1_all.tsv", "continuous", 2452),
        ("cluster_34", "inputs/cluster_membership_2802.tsv",  "continuous", 2690),
        ("s1_L1_32", "inputs/fastbaps_membership_L1_all.tsv", "mixture", 2378),
        ("cluster_4",  "inputs/cluster_membership_2802.tsv",  "mixture", 1338),
        ("cluster_78", "inputs/cluster_membership_2802.tsv",  "mixture", 1722),
    ]
    sizes = [int(x) for x in a.sizes.split(",")]
    random.seed(0)
    res = {(s, lab): [] for s in sizes for lab in ("continuous", "mixture")}

    for cid, memb, label, full in panel:
        lst = "cluster_metadata_%s_genomes.tsv" % cid
        n = genome_list(cid, memb, lst) if not os.path.exists(lst) else sum(1 for _ in open(lst))
        try:
            idx = pair_index(lst, a.threads)
        except Exception as exc:
            print("  %-12s FAILED: %s" % (cid, str(exc)[:90])); continue
        genomes = sorted({g for g, _ in idx})
        print("  %-12s %-11s n=%-4d ska %d" % (cid, label, len(genomes), full))
        for s in sizes:
            if s > len(genomes):
                continue
            for _ in range(a.reps):
                sub = random.sample(genomes, s)
                dd = [idx[(x, y)] for i, x in enumerate(sub) for y in sub[i + 1:]]
                t = two_stats(dd)
                if t is not None:
                    res[(s, label)].append(t)

    print("\nPOOLED: %d continuous, %d mixture clusters (ALL in range), %d reps"
          % (sum(1 for x in panel if x[2] == "continuous"),
             sum(1 for x in panel if x[2] == "mixture"), a.reps))
    def q(v, p): return sorted(v)[min(len(v) - 1, int(p * len(v)))]
    for stat, name, idx in ((0, "gap/mean", 0), (1, "empty_bins", 1)):
        print("\n--- %s ---" % name)
        print("%4s %26s %26s  %s" % ("n", "CONTINUOUS med [p5-p95]",
                                     "MIXTURE med [p5-p95]", "separable?"))
        print("-" * 84)
        for s_ in sizes:
            c = [t[idx] for t in res[(s_, "continuous")]]
            m = [t[idx] for t in res[(s_, "mixture")]]
            if not c or not m: continue
            c95, m05 = q(c, 0.95), q(m, 0.05)
            print("%4d %9.3f [%.3f-%.3f]%5s %9.3f [%.3f-%.3f]%5s  %s"
                  % (s_, statistics.median(c), q(c, 0.05), c95, "",
                     statistics.median(m), m05, q(m, 0.95), "",
                     ("YES ~%.2f" % ((c95 + m05) / 2)) if c95 < m05 else "no"))
    print("\n--- EITHER fires (gap>thr_g OR empty>thr_e) ---")
    for tg, te in ((1.0, 0.45), (1.0, 0.40), (0.6, 0.40), (0.6, 0.35)):
        print("  thresholds gap>%.1f or empty>%.2f:" % (tg, te))
        for s_ in sizes:
            c = res[(s_, "continuous")]; m = res[(s_, "mixture")]
            if not c or not m: continue
            fp = sum(1 for g, e in c if g > tg or e > te) / len(c)
            tp = sum(1 for g, e in m if g > tg or e > te) / len(m)
            print("     n=%-3d false-mixture %4.0f%%   caught %4.0f%%" % (s_, 100 * fp, 100 * tp))
    return 0


if __name__ == "__main__":
    sys.exit(main())
