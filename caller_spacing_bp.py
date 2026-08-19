#!/usr/bin/env python3
"""Snippy vs SKA: is SNP recovery coupled to local SNP spacing?

THE QUESTION. Gubbins detects recombination as elevated SNP DENSITY. Split
k-mers (SKA2, k=31) cannot call a variant whose flanking window contains another
variant, so SKA's sensitivity falls exactly where the signal lives -- the
instrument goes blind on the quantity being measured. Mapping-based calling
(snippy) has no such coupling in the low-divergence within-cluster regime; its
failure mode is mismapping in repeats, which produces the OPPOSITE error (false
clustered SNPs).

Neither caller is safe by assertion. This measures the coupling directly.

DESIGN. The `refsens_cluster*` runs already carry paired arms: the same cluster,
same reference, same replicon, called by `existing` (snippy) and `ska_map`. For
each pair we take the SNP positions Gubbins actually received
(`gubbins.snps.vcf`) and ask:

  1. How many SNPs did each caller deliver?
  2. Stratified by NEAREST-NEIGHBOUR DISTANCE, where does SKA lose them?
     If the loss is flat across spacing bins, the coupling is not operating at
     this divergence and SKA is vindicated here. If it concentrates in the tight
     bins, the mechanism is live and r/m is biased low.
  3. What does that do to pooled r/m?

WHY NEAREST-NEIGHBOUR SPACING is the right axis: it is the property the split
k-mer failure depends on. Binning by anything else (position, chromosome, unit)
would average over it and could not see the effect -- the same reason the
project's spike-in, which varied donor divergence but held spacing ~constant at
1 SNP per ~550 bp, structurally could not detect this.

CAVEAT ON DIRECTION. A raw count difference is not by itself evidence of SKA
undercalling: snippy may be ADDING false SNPs from mismapping. The spacing
profile is what separates the two stories. SKA-undercalling predicts the deficit
concentrates at SHORT spacing. Snippy-false-positives predicts its excess sits in
repeat-dense regions and need not be spacing-dependent.
"""

import argparse
import glob
import os
import statistics
import sys

import cap_location_bp as C

SELF = os.path.dirname(os.path.abspath(__file__))
# Nearest-neighbour distance bins (bp). The first two bracket the split k-mer
# failure zone for k=31; the rest are controls that should show no effect.
BINS = [(0, 10), (10, 31), (31, 100), (100, 500), (500, 10**9)]


# DO NOT USE gubbins.snps.vcf FOR SPACING. Its POS column indexes the SNP-ONLY
# alignment (verified: positions run 1..N where N == filtered_polymorphic_sites
# width exactly), so every nearest-neighbour distance is 1 bp by construction and
# the whole spacing panel collapses into the first bin. An earlier version of this
# script did exactly that and produced a clean, plausible, entirely meaningless
# ratio of 0.623. Genomic coordinates only.
def read_snp_positions_vcf(vcf):
    """GENOMIC positions from snippy's core.vcf. Returns sorted list of ints."""
    pos = []
    try:
        with open(vcf) as fh:
            for line in fh:
                if line.startswith("#"):
                    continue
                f = line.split("\t", 3)
                if len(f) >= 2:
                    try:
                        pos.append(int(f[1]))
                    except ValueError:
                        pass
    except OSError:
        return None
    return sorted(pos)


def read_snp_positions_alignment(fasta):
    """GENOMIC positions of variable columns in a full-length, genome-ORDERED
    alignment (what `ska map` emits). Column index == reference coordinate, so
    variable columns give true spacing.

    A column counts as variable if it carries >1 distinct unambiguous base.
    N/-/? are ignored rather than treated as a state: SKA emits N where a split
    k-mer failed to match, and counting that as an allele would score its own
    dropouts as SNPs -- inverting the very effect being measured.
    """
    seqs = []
    cur = []
    try:
        with open(fasta) as fh:
            for line in fh:
                if line.startswith(">"):
                    if cur:
                        seqs.append("".join(cur))
                        cur = []
                else:
                    cur.append(line.strip())
        if cur:
            seqs.append("".join(cur))
    except OSError:
        return None
    if len(seqs) < 2:
        return None
    width = min(len(s) for s in seqs)
    valid = set("ACGTacgt")
    pos = []
    for i in range(width):
        seen = set()
        for s in seqs:
            c = s[i]
            if c in valid:
                seen.add(c.upper())
                if len(seen) > 1:
                    break
        if len(seen) > 1:
            pos.append(i + 1)
    return pos


def nn_distances(pos):
    """Nearest-neighbour distance for each SNP (min of left/right gap)."""
    n = len(pos)
    if n < 2:
        return []
    out = []
    for i, p in enumerate(pos):
        left = p - pos[i - 1] if i > 0 else None
        right = pos[i + 1] - p if i < n - 1 else None
        cands = [d for d in (left, right) if d is not None]
        out.append(min(cands))
    return out


def bin_counts(dists):
    counts = [0] * len(BINS)
    for d in dists:
        for i, (lo, hi) in enumerate(BINS):
            if lo <= d < hi:
                counts[i] += 1
                break
    return counts


def collect(pattern="refsens_cluster*"):
    """Pair snippy and ska arms by (cluster, reference, replicon)."""
    rows = []
    for cdir in sorted(glob.glob(os.path.join(SELF, pattern))):
        cluster = os.path.basename(cdir)
        armdir = os.path.join(cdir, "arms")
        if not os.path.isdir(armdir):
            continue
        for ref in ("close", "K96243"):
            for rep in ("chr1", "chr2"):
                sn = os.path.join(armdir, "%s__existing__%s" % (ref, rep))
                sk = os.path.join(armdir, "%s__ska_map__%s" % (ref, rep))
                if not (os.path.isdir(sn) and os.path.isdir(sk)):
                    continue
                # snippy: genomic coords straight from core.vcf.
                sn_pos = read_snp_positions_vcf(os.path.join(sn, "core.vcf"))
                # ska: derive from the genome-ordered full-length alignment.
                sk_aln = sorted(glob.glob(os.path.join(sk, "aln.full.*.fa")))
                sk_pos = (read_snp_positions_alignment(sk_aln[0])
                          if sk_aln else None)
                if not sn_pos or not sk_pos:
                    continue
                rows.append({
                    "cluster": cluster.replace("refsens_", ""),
                    "ref": ref, "rep": rep,
                    "sn_pos": sn_pos, "sk_pos": sk_pos,
                    "sn_stats": C.gubbins_stats(sn),
                    "sk_stats": C.gubbins_stats(sk),
                })
    return rows


def report(pattern="refsens_cluster*"):
    rows = collect(pattern)
    if not rows:
        print("no paired snippy/ska arms found", file=sys.stderr)
        return 1

    print("=" * 100)
    print("CALLER SPACING COUPLING -- snippy (mapping) vs ska_map (split k-mer)")
    print("=" * 100)
    print("\nGENOMIC SNP positions, paired by cluster/reference/replicon.")
    print("  snippy: core.vcf (true reference coordinates)")
    print("  ska   : variable columns of the genome-ordered aln.full.*.fa")
    print("  NOT gubbins.snps.vcf -- its POS column indexes the SNP-only")
    print("  alignment (1..N), which makes every gap 1 bp and silently collapses")
    print("  the spacing panel into a single bin.\n")

    print("%-12s %-8s %-5s %9s %9s %8s" %
          ("cluster", "ref", "rep", "snippy", "ska", "ska/sn"))
    print("-" * 100)
    ratios = []
    for r in sorted(rows, key=lambda x: (x["cluster"], x["ref"], x["rep"])):
        ns, nk = len(r["sn_pos"]), len(r["sk_pos"])
        ratio = nk / ns if ns else float("nan")
        ratios.append(ratio)
        print("%-12s %-8s %-5s %9d %9d %8.3f"
              % (r["cluster"], r["ref"], r["rep"], ns, nk, ratio))
    print("\n  median ska/snippy SNP-count ratio: %.3f" % statistics.median(ratios))

    # ---- THE DECISIVE PANEL -------------------------------------------------
    print("\n" + "=" * 100)
    print("SNP COUNT BY NEAREST-NEIGHBOUR SPACING  --  where does the difference live?")
    print("=" * 100)
    print("\nIf SKA's split k-mers are the cause, its deficit CONCENTRATES in the")
    print("0-10 and 10-31 bp bins (k=31). If the ratio is flat across bins, the")
    print("coupling is not operating at this divergence.\n")

    tot_sn = [0] * len(BINS)
    tot_sk = [0] * len(BINS)
    for r in rows:
        for i, c in enumerate(bin_counts(nn_distances(r["sn_pos"]))):
            tot_sn[i] += c
        for i, c in enumerate(bin_counts(nn_distances(r["sk_pos"]))):
            tot_sk[i] += c

    labels = ["0-10 bp", "10-31 bp", "31-100 bp", "100-500 bp", ">=500 bp"]
    print("%-14s %12s %12s %10s   %s" %
          ("NN spacing", "snippy", "ska", "ska/sn", "interpretation"))
    print("-" * 100)
    base = None
    for i, lab in enumerate(labels):
        ratio = tot_sk[i] / tot_sn[i] if tot_sn[i] else float("nan")
        if i == len(labels) - 1:
            base = ratio
        print("%-14s %12d %12d %10.3f" % (lab, tot_sn[i], tot_sk[i], ratio))

    print("\n  Reference bin (>=500 bp, isolated SNPs) ratio = %.3f" % base)
    if base and base == base:
        for i, lab in enumerate(labels[:2]):
            ratio = tot_sk[i] / tot_sn[i] if tot_sn[i] else float("nan")
            if ratio == ratio and base:
                rel = ratio / base
                print("  %-10s relative to isolated SNPs: %.3f  %s"
                      % (lab, rel,
                         "<-- DEPLETED, coupling is live" if rel < 0.8
                         else "no depletion" if rel > 0.95 else "mild depletion"))

    # ---- consequence for r/m ------------------------------------------------
    print("\n" + "=" * 100)
    print("CONSEQUENCE FOR POOLED r/m")
    print("=" * 100)
    print("\n%-12s %-8s %-5s %10s %10s %8s" %
          ("cluster", "ref", "rep", "r/m snippy", "r/m ska", "ska/sn"))
    print("-" * 100)
    rm_ratios = []
    for r in sorted(rows, key=lambda x: (x["cluster"], x["ref"], x["rep"])):
        a, b = r["sn_stats"], r["sk_stats"]
        if not a or not b:
            continue
        ra, rb = a.get("pooled_rm"), b.get("pooled_rm")
        if not ra:
            continue
        rm_ratios.append(rb / ra)
        print("%-12s %-8s %-5s %10.2f %10.2f %8.3f"
              % (r["cluster"], r["ref"], r["rep"], ra, rb, rb / ra))
    if rm_ratios:
        below = sum(1 for x in rm_ratios if x < 1.0)
        print("\n  median r/m ratio (ska/snippy): %.3f   range %.3f-%.3f"
              % (statistics.median(rm_ratios), min(rm_ratios), max(rm_ratios)))
        print("  %d of %d comparisons have ska BELOW snippy" % (below, len(rm_ratios)))
    return 0


def selftest():
    fails = []

    def chk(desc, got, want):
        ok = got == want
        print("%-56s %s" % (desc, "ok" if ok else "FAIL got=%r want=%r" % (got, want)))
        if not ok:
            fails.append(desc)

    # nearest-neighbour distance is the min of both gaps, not just the forward one
    chk("nn of [100,105,300]", nn_distances([100, 105, 300]), [5, 5, 195])
    chk("nn of single SNP is empty", nn_distances([50]), [])
    # binning is half-open and must not double count
    chk("d=10 lands in 10-31 bin", bin_counts([10]), [0, 1, 0, 0, 0])
    chk("d=9 lands in 0-10 bin", bin_counts([9]), [1, 0, 0, 0, 0])
    chk("d=31 lands in 31-100 bin", bin_counts([31]), [0, 0, 1, 0, 0])
    chk("bins sum to input size", sum(bin_counts([1, 20, 50, 200, 9000])), 5)

    # GUARD AGAINST THE BUG THAT ALREADY HAPPENED ONCE. If positions are
    # SNP-alignment indices rather than genomic coordinates they are exactly
    # 1,2,3,...,N -- every gap is 1 bp and the whole spacing panel collapses into
    # the first bin while still printing a clean, plausible ratio.
    contiguous = list(range(1, 501))
    d = nn_distances(contiguous)
    chk("contiguous indices are detectable (all gaps 1)", set(d), {1})
    chk("...and they collapse into one bin (the smell)",
        sum(1 for c in bin_counts(d) if c > 0), 1)
    # Real genomic SNPs on a multi-Mbp replicon must NOT look like that.
    chk("real-looking spacing spreads across bins",
        sum(1 for c in bin_counts([3, 15, 60, 300, 5000]) if c > 0), 5)
    print("\n%d test(s) failed" % len(fails) if fails else "\nall tests passed")
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--pattern", default="refsens_cluster*")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.report:
        return report(a.pattern)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
