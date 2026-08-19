#!/usr/bin/env python3
"""Calibrate the Mash-to-SNP proxy against measured mean pairwise distances.

`cluster_diversity_bp.py` estimates within-cluster diversity as
  approx_mean_snps = mean_mash * 3_805_619
and every "genomes in cap" figure downstream inherits that estimate's error.
It was validated on a single cluster against a number that is NOT the same
statistic (cluster_0's 16,197 is a *count of polymorphic sites*, not a mean
pairwise distance).

This computes the actual mean pairwise SNP distance from the alignments the
reference-sensitivity run already produced, so the proxy can be checked
against the quantity it claims to estimate.

Two alignments per arm are scored:
  core.aln                              pre-Gubbins polymorphic sites
  gubbins.filtered_polymorphic_sites.fasta   post-Gubbins (recombination removed)

Pairwise distances use pairwise deletion: only columns where both taxa have
an unambiguous ACGT base are counted, and the raw mismatch count is rescaled
by the fraction of columns usable for that pair.

Usage:
    python3 calibrate_mash_snp_bp.py [--arms-glob PATTERN] [--selftest]
"""

import argparse
import glob
import os
import sys

CORE_BP = 3_805_619  # Wu core alignment length, the proxy's multiplier
BASES = frozenset(b"ACGT")


def read_fasta(path):
    """Return [(name, seq_bytes), ...]. Uppercases; leaves ambiguity codes in."""
    names, seqs, chunks, name = [], [], [], None
    with open(path, "rb") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if line[:1] == b">":
                if name is not None:
                    names.append(name)
                    seqs.append(b"".join(chunks))
                name = line[1:].split()[0].decode("utf-8", "replace")
                chunks = []
            else:
                chunks.append(line.upper())
    if name is not None:
        names.append(name)
        seqs.append(b"".join(chunks))
    return list(zip(names, seqs))


def pairwise_stats(records):
    """Mean/median pairwise SNPs over an alignment, with pairwise deletion.

    Returns dict with n_taxa, n_cols, mean_raw, mean_scaled, max_scaled,
    and mean_usable_frac. `mean_raw` counts mismatches in shared-ACGT columns;
    `mean_scaled` extrapolates that rate to the full column count, which is
    what makes pairs with different missingness comparable.
    """
    n = len(records)
    if n < 2:
        return None
    ncols = len(records[0][1])
    for name, seq in records:
        if len(seq) != ncols:
            raise ValueError("ragged alignment at %s (%d != %d)" % (name, len(seq), ncols))

    # Precompute a validity mask per taxon as a bytes object of 0/1.
    seqs = [s for _, s in records]
    masks = [bytes(1 if c in BASES else 0 for c in s) for s in seqs]

    raw_list, scaled_list, usable_list = [], [], []
    for i in range(n):
        si, mi = seqs[i], masks[i]
        for j in range(i + 1, n):
            sj, mj = seqs[j], masks[j]
            usable = 0
            diff = 0
            for k in range(ncols):
                if mi[k] and mj[k]:
                    usable += 1
                    if si[k] != sj[k]:
                        diff += 1
            raw_list.append(diff)
            usable_list.append(usable)
            scaled_list.append(diff * ncols / usable if usable else float("nan"))

    valid = [x for x in scaled_list if x == x]
    raw_list.sort()
    valid_sorted = sorted(valid)
    return {
        "n_taxa": n,
        "n_cols": ncols,
        "n_pairs": len(raw_list),
        "mean_raw": sum(raw_list) / len(raw_list),
        "median_raw": raw_list[len(raw_list) // 2],
        "mean_scaled": (sum(valid) / len(valid)) if valid else float("nan"),
        "max_scaled": (valid_sorted[-1] if valid else float("nan")),
        "mean_usable_frac": (sum(usable_list) / len(usable_list) / ncols) if ncols else 0.0,
    }


def score_arm(arm_dir):
    """Score both alignments in one arm directory."""
    out = {}
    targets = {
        "pre_gubbins": os.path.join(arm_dir, "core.aln"),
        "post_gubbins": os.path.join(arm_dir, "gubbins.filtered_polymorphic_sites.fasta"),
    }
    for label, path in targets.items():
        if not os.path.exists(path):
            continue
        try:
            recs = read_fasta(path)
        except Exception as exc:  # keep going; one bad arm must not kill the sweep
            out[label] = {"error": str(exc)}
            continue
        # Gubbins writes the reconstructed internal nodes into some outputs but
        # not this one; still, drop anything that looks like a Gubbins node label.
        recs = [(nm, sq) for nm, sq in recs if not nm.startswith("Node_")]
        try:
            st = pairwise_stats(recs)
        except ValueError as exc:
            out[label] = {"error": str(exc)}
            continue
        if st:
            out[label] = st
    return out


def selftest():
    """Small, exact checks on pairwise_stats."""
    fails = []

    def check(desc, got, want, tol=1e-9):
        if abs(got - want) > tol:
            fails.append("%s: got %r want %r" % (desc, got, want))

    # 1. Two taxa, 4 columns, 1 mismatch, no missing data.
    st = pairwise_stats([("a", b"ACGT"), ("b", b"ACGA")])
    check("2-taxon raw", st["mean_raw"], 1.0)
    check("2-taxon scaled", st["mean_scaled"], 1.0)
    check("2-taxon usable", st["mean_usable_frac"], 1.0)

    # 2. Missing data must rescale: 1 mismatch over 2 usable of 4 cols -> 2.0.
    st = pairwise_stats([("a", b"ACNN"), ("b", b"AGNN")])
    check("rescale raw", st["mean_raw"], 1.0)
    check("rescale scaled", st["mean_scaled"], 2.0)
    check("rescale usable", st["mean_usable_frac"], 0.5)

    # 3. Identical sequences give zero.
    st = pairwise_stats([("a", b"ACGT"), ("b", b"ACGT"), ("c", b"ACGT")])
    check("identical mean", st["mean_scaled"], 0.0)
    if st["n_pairs"] != 3:
        fails.append("n_pairs: got %d want 3" % st["n_pairs"])

    # 4. Three taxa, known distances: ab=1, ac=2, bc=1 -> mean 4/3.
    st = pairwise_stats([("a", b"AAAA"), ("b", b"AAAC"), ("c", b"AACC")])
    check("3-taxon mean", st["mean_scaled"], 4.0 / 3.0)
    check("3-taxon max", st["max_scaled"], 2.0)

    # 5. Gaps count as missing, same as N.
    st = pairwise_stats([("a", b"AC--"), ("b", b"AG--")])
    check("gap scaled", st["mean_scaled"], 2.0)

    # 6. Single taxon is not scoreable.
    if pairwise_stats([("a", b"ACGT")]) is not None:
        fails.append("single taxon should return None")

    # 7. Ragged alignment must raise.
    try:
        pairwise_stats([("a", b"ACGT"), ("b", b"ACG")])
        fails.append("ragged alignment should raise")
    except ValueError:
        pass

    if fails:
        print("SELFTEST FAILED (%d)" % len(fails))
        for f in fails:
            print("  " + f)
        return 1
    print("selftest: 7/7 checks passed")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arms-glob",
                    default="refsens_cluster*/arms/*__*__chr*",
                    help="glob for arm directories")
    ap.add_argument("--only-close", action="store_true",
                    help="restrict to close-reference arms (the unbiased ones)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    arm_dirs = sorted(d for d in glob.glob(args.arms_glob) if os.path.isdir(d))
    if args.only_close:
        arm_dirs = [d for d in arm_dirs if os.path.basename(d).startswith("close__")]
    if not arm_dirs:
        print("no arm directories matched %r" % args.arms_glob, file=sys.stderr)
        return 2

    hdr = ("%-18s %-26s %-14s %6s %8s %10s %10s %10s %7s"
           % ("cluster", "arm", "alignment", "taxa", "cols", "mean_raw",
              "mean_scal", "max_scal", "usable"))
    print(hdr)
    print("-" * len(hdr))

    rows = []
    for d in arm_dirs:
        cluster = os.path.basename(os.path.dirname(os.path.dirname(d)))
        arm = os.path.basename(d)
        res = score_arm(d)
        for label in ("pre_gubbins", "post_gubbins"):
            st = res.get(label)
            if not st:
                continue
            if "error" in st:
                print("%-18s %-26s %-14s  ERROR %s" % (cluster, arm, label, st["error"]))
                continue
            print("%-18s %-26s %-14s %6d %8d %10.1f %10.1f %10.1f %6.1f%%"
                  % (cluster, arm, label, st["n_taxa"], st["n_cols"],
                     st["mean_raw"], st["mean_scaled"], st["max_scaled"],
                     100.0 * st["mean_usable_frac"]))
            rows.append((cluster, arm, label, st))

    with open("mash_snp_calibration.tsv", "w") as fh:
        fh.write("cluster\tarm\talignment\tn_taxa\tn_cols\tn_pairs\t"
                 "mean_raw\tmedian_raw\tmean_scaled\tmax_scaled\tmean_usable_frac\n")
        for cluster, arm, label, st in rows:
            fh.write("%s\t%s\t%s\t%d\t%d\t%d\t%.2f\t%d\t%.2f\t%.2f\t%.4f\n"
                     % (cluster, arm, label, st["n_taxa"], st["n_cols"], st["n_pairs"],
                        st["mean_raw"], st["median_raw"], st["mean_scaled"],
                        st["max_scaled"], st["mean_usable_frac"]))
    print("\nwrote mash_snp_calibration.tsv (%d rows)" % len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
