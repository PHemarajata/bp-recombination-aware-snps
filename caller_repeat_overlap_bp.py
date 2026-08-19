#!/usr/bin/env python3
"""Are snippy's tightly-clustered SNPs real, or mismapping artefacts in repeats?

THE QUESTION THIS SETTLES. `caller_spacing_bp.py` showed snippy and ska_map
disagree sharply and specifically at short SNP spacing: ska recovers ~12% of
SNPs within 10 bp of a neighbour, ~56% at 10-31 bp, and ~100% beyond 31 bp --
a boundary at the k=31 split k-mer length. Two stories fit that equally well:

  (A) SKA UNDERCALLS. Split k-mers cannot call a variant whose flank carries
      another variant, so ska loses real clustered SNPs -- exactly the density
      Gubbins reads as recombination. r/m is then biased LOW.
  (B) SNIPPY OVER-CALLS. Read/contig mapping mismaps in repeats and paralogues,
      manufacturing false clustered SNPs. r/m is then biased HIGH by snippy, and
      ska is simply more specific.

These predict different things about WHERE snippy's clustered SNPs sit.
B. pseudomallei is repeat-rich (IS elements, paralogous families), and
mismapping happens where the reference is NOT unique. So:

  (A) predicts snippy's 0-10 bp SNPs are NOT enriched in repeats -- they are
      real recombinant tracts in unique sequence.
  (B) predicts they ARE strongly enriched in repeats relative to snippy's own
      isolated SNPs.

METHOD. Repeats are defined by nucmer self-alignment of each reference
(`--maxmatch --nosimplify`), EXCLUDING the identity diagonal -- without that
exclusion every base trivially matches itself and the whole genome scores as
repetitive. Any reference interval aligning to a DIFFERENT locus is repetitive.
Then, per arm, compare the repeat-overlap rate of snippy's clustered SNPs
against its own isolated SNPs. Using snippy as its own control removes any
between-caller difference in filtering or coverage.

WHY THE INTERNAL CONTROL MATTERS. Comparing snippy-clustered against
ska-clustered would confound the repeat question with the caller difference
being investigated. The enrichment RATIO within snippy is the estimand.
"""

import argparse
import glob
import os
import statistics
import sys

SELF = os.path.dirname(os.path.abspath(__file__))
CLUSTERED_MAX = 10      # nearest-neighbour distance defining "clustered"
ISOLATED_MIN = 500      # ...and "isolated"


def parse_delta_repeats(delta_path, min_len=100, min_offset=100):
    """Repeat intervals on the REFERENCE from a nucmer self-alignment delta.

    Excludes the identity diagonal: an alignment whose reference and query
    intervals start within `min_offset` bp of each other is the sequence
    matching itself, not a repeat. Without this the entire genome is 'repeat'.
    """
    ivs = []
    try:
        with open(delta_path) as fh:
            for line in fh:
                p = line.split()
                # alignment header: rs re qs qe errors sim stop
                if len(p) == 7 and all(x.lstrip("-").isdigit() for x in p):
                    rs, re_, qs, qe = int(p[0]), int(p[1]), int(p[2]), int(p[3])
                    if rs > re_:
                        rs, re_ = re_, rs
                    q_lo = min(qs, qe)
                    if abs(rs - q_lo) < min_offset:
                        continue                      # identity diagonal
                    if re_ - rs + 1 < min_len:
                        continue
                    ivs.append((rs, re_))
    except OSError:
        return None
    if not ivs:
        return []
    ivs.sort()
    merged = [list(ivs[0])]
    for s, e in ivs[1:]:
        if s <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return [tuple(x) for x in merged]


def in_repeat(pos_sorted, repeats):
    """Count how many positions fall inside merged repeat intervals."""
    if not repeats:
        return 0
    import bisect
    starts = [r[0] for r in repeats]
    n = 0
    for p in pos_sorted:
        i = bisect.bisect_right(starts, p) - 1
        if i >= 0 and repeats[i][0] <= p <= repeats[i][1]:
            n += 1
    return n


def read_vcf_positions(vcf):
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


def nn_distances(pos):
    n = len(pos)
    if n < 2:
        return []
    out = []
    for i, p in enumerate(pos):
        c = []
        if i > 0:
            c.append(p - pos[i - 1])
        if i < n - 1:
            c.append(pos[i + 1] - p)
        out.append(min(c))
    return out


def report(deltadir, cluster="refsens_cluster37"):
    arms = ["K96243__existing__chr1", "K96243__existing__chr2",
            "close__existing__chr1", "close__existing__chr2"]
    print("=" * 100)
    print("REPEAT OVERLAP OF SNIPPY SNPs -- are the clustered ones mismapping artefacts?")
    print("=" * 100)
    print("\nRepeats = nucmer self-alignment of the reference, identity diagonal excluded.")
    print("Snippy is its OWN control: clustered (NN < %d bp) vs isolated (NN >= %d bp).\n"
          % (CLUSTERED_MAX, ISOLATED_MIN))
    print("%-26s %10s %12s %10s %12s %9s" %
          ("arm", "clustered", "in repeat", "isolated", "in repeat", "enrich"))
    print("-" * 100)

    enrichments = []
    genome_rep_frac = []
    for arm in arms:
        d = os.path.join(SELF, cluster, "arms", arm)
        vcf = os.path.join(d, "core.vcf")
        delta = os.path.join(deltadir, arm + ".delta")
        pos = read_vcf_positions(vcf)
        reps = parse_delta_repeats(delta)
        if not pos or reps is None:
            print("%-26s  (missing data)" % arm)
            continue
        dists = nn_distances(pos)
        clustered = [p for p, dd in zip(pos, dists) if dd < CLUSTERED_MAX]
        isolated = [p for p, dd in zip(pos, dists) if dd >= ISOLATED_MIN]
        cr = in_repeat(clustered, reps)
        ir = in_repeat(isolated, reps)
        cfrac = cr / len(clustered) if clustered else float("nan")
        ifrac = ir / len(isolated) if isolated else float("nan")
        enr = (cfrac / ifrac) if ifrac else float("nan")
        if enr == enr:
            enrichments.append(enr)
        rep_bp = sum(e - s + 1 for s, e in reps)
        genome_rep_frac.append(rep_bp)
        print("%-26s %10d %11.1f%% %10d %11.1f%% %9.2fx"
              % (arm, len(clustered), 100 * cfrac, len(isolated), 100 * ifrac, enr))

    print()
    if enrichments:
        med = statistics.median(enrichments)
        print("  median enrichment of clustered vs isolated SNPs in repeats: %.2fx" % med)
        print()
        print("  READING")
        if med >= 2.0:
            print("    STRONG enrichment -- snippy's clustered SNPs sit disproportionately")
            print("    in repetitive sequence. Consistent with story (B): mismapping is")
            print("    manufacturing false clustered SNPs, and ska's lower count is")
            print("    SPECIFICITY, not lost signal.")
        elif med <= 1.3:
            print("    NO meaningful enrichment -- snippy's clustered SNPs sit in unique")
            print("    sequence at about the same rate as its isolated SNPs. Story (B) is")
            print("    NOT supported; the clustered SNPs look real, so ska is losing")
            print("    genuine recombination signal and r/m built on ska is biased LOW.")
        else:
            print("    PARTIAL enrichment -- some of snippy's clustered excess is")
            print("    repeat-associated, but not enough to explain it all. Both effects")
            print("    are likely operating; neither caller is clean.")
    print("\n  (Repeat fraction of each reference, for scale: %s)"
          % ", ".join("%.1f%%" % (100 * f / t) for f, t in
                      zip(genome_rep_frac, [4074542, 3173005, 4092668, 3138747])))
    return 0


def selftest():
    fails = []

    def chk(desc, got, want):
        ok = got == want
        print("%-58s %s" % (desc, "ok" if ok else "FAIL got=%r want=%r" % (got, want)))
        if not ok:
            fails.append(desc)

    chk("in_repeat finds a contained position", in_repeat([50], [(10, 100)]), 1)
    chk("in_repeat rejects an outside position", in_repeat([5], [(10, 100)]), 0)
    chk("in_repeat handles boundaries inclusively",
        in_repeat([10, 100], [(10, 100)]), 2)
    chk("in_repeat with no repeats is zero", in_repeat([50], []), 0)
    chk("nn distances", nn_distances([100, 105, 300]), [5, 5, 195])

    # THE LOAD-BEARING GUARD: the identity diagonal must be excluded, or every
    # base matches itself and the genome scores as 100% repetitive.
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".delta", delete=False) as fh:
        fh.write("/a /b\nNUCMER\n>r q 1000 1000\n")
        fh.write("1 500 1 500 0 0 0\n")        # identity diagonal -> must drop
        fh.write("0\n")
        fh.write("600 900 20000 20300 0 0 0\n")  # true repeat -> must keep
        fh.write("0\n")
        p = fh.name
    got = parse_delta_repeats(p)
    os.unlink(p)
    chk("identity diagonal excluded, true repeat kept", got, [(600, 900)])

    print("\n%d test(s) failed" % len(fails) if fails else "\nall tests passed")
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--deltadir", default="")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.report:
        if not a.deltadir:
            print("need --deltadir", file=sys.stderr)
            return 1
        return report(a.deltadir)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
