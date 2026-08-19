#!/usr/bin/env python3
"""Do snippy's clustered SNPs sit in mobile elements or rRNA (paralogy)?

WHY THIS EXISTS. `caller_repeat_overlap_bp.py` defined repeats by nucmer
self-alignment and found snippy's tightly-clustered SNPs are NOT repeat-enriched
(28 of 2,474 even under permissive settings). But self-alignment only catches
sequence that is *near-identical elsewhere in the same replicon*. It misses two
mismapping sources that matter in B. pseudomallei:

  - MOBILE ELEMENTS whose copies have diverged past the alignment threshold, or
    whose other copies live on the OTHER replicon / a plasmid.
  - rRNA OPERONS, multi-copy and highly conserved, a classic mismapping sink.

This uses the RefSeq annotation instead of sequence self-similarity, so it is an
independent test of the same alternative hypothesis: that snippy's excess
clustered SNPs are mapping artefacts rather than real recombination.

ESTIMAND. Enrichment = (fraction of snippy's CLUSTERED SNPs in mobile/rRNA
features) / (fraction of its ISOLATED SNPs in the same features). Snippy is its
own control, so caller-level differences in filtering cancel.

SCOPE. Annotation is available for K96243 chromosome 1 only, so this covers the
`K96243__existing__chr1` arm. That is the DISTANT-reference arm; the production
configuration uses the close reference, for which no annotation was supplied.
"""

import argparse
import os
import re
import sys

SELF = os.path.dirname(os.path.abspath(__file__))
CLUSTERED_MAX = 10
ISOLATED_MIN = 500

MOBILE_RE = re.compile(
    r"transposase|integrase|recombinase|insertion sequence|\bIS\d|phage|transposon",
    re.I)

LOC_RE = re.compile(r"(\d+)\.\.(\d+)")


def parse_genbank_features(path):
    """Return (mobile_intervals, rrna_intervals, all_cds_intervals).

    Handles `123..456`, `complement(123..456)` and `join(...)` by taking every
    numeric span in the location string -- adequate for interval overlap.
    """
    mobile, rrna, cds = [], [], []
    cur_type = None
    cur_loc = []
    cur_qual = []

    def flush():
        if not cur_type or not cur_loc:
            return
        loc = "".join(cur_loc)
        spans = [(int(a), int(b)) for a, b in LOC_RE.findall(loc)]
        if not spans:
            return
        qual = " ".join(cur_qual)
        if cur_type == "rRNA":
            rrna.extend(spans)
        elif cur_type == "CDS":
            cds.extend(spans)
            if MOBILE_RE.search(qual):
                mobile.extend(spans)

    try:
        with open(path) as fh:
            in_features = False
            for line in fh:
                if line.startswith("FEATURES"):
                    in_features = True
                    continue
                if not in_features:
                    continue
                if line.startswith("ORIGIN") or line.startswith("CONTIG") \
                        or line.startswith("//"):
                    flush()
                    break
                # new feature: 5 spaces, type, then location
                m = re.match(r"^ {5}(\S+)\s+(.*)$", line.rstrip("\n"))
                if m:
                    flush()
                    cur_type = m.group(1)
                    cur_loc = [m.group(2)]
                    cur_qual = []
                elif line.startswith(" " * 21):
                    body = line.strip()
                    if body.startswith("/"):
                        cur_qual.append(body)
                    elif cur_qual:
                        cur_qual.append(body)
                    else:
                        cur_loc.append(body)
    except OSError:
        return None, None, None
    return merge(mobile), merge(rrna), merge(cds)


def merge(ivs):
    if not ivs:
        return []
    ivs = sorted((min(a, b), max(a, b)) for a, b in ivs)
    out = [list(ivs[0])]
    for s, e in ivs[1:]:
        if s <= out[-1][1] + 1:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [tuple(x) for x in out]


def count_in(pos, ivs):
    if not ivs:
        return 0
    import bisect
    starts = [i[0] for i in ivs]
    n = 0
    for p in pos:
        i = bisect.bisect_right(starts, p) - 1
        if i >= 0 and ivs[i][0] <= p <= ivs[i][1]:
            n += 1
    return n


def read_vcf_positions(vcf):
    pos = []
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
    return sorted(pos)


def nn_distances(pos):
    n = len(pos)
    out = []
    for i, p in enumerate(pos):
        c = []
        if i > 0:
            c.append(p - pos[i - 1])
        if i < n - 1:
            c.append(pos[i + 1] - p)
        out.append(min(c) if c else 10 ** 9)
    return out


def report(gb, arm="K96243__existing__chr1", cluster="refsens_cluster37",
           genome_len=4074542):
    mobile, rrna, cds = parse_genbank_features(gb)
    if mobile is None:
        print("could not parse %s" % gb, file=sys.stderr)
        return 1
    vcf = os.path.join(SELF, cluster, "arms", arm, "core.vcf")
    pos = read_vcf_positions(vcf)
    d = nn_distances(pos)
    clustered = [p for p, dd in zip(pos, d) if dd < CLUSTERED_MAX]
    isolated = [p for p, dd in zip(pos, d) if dd >= ISOLATED_MIN]

    def bp(ivs):
        return sum(e - s + 1 for s, e in ivs)

    print("=" * 100)
    print("ANNOTATION OVERLAP -- are snippy's clustered SNPs in mobile elements / rRNA?")
    print("=" * 100)
    print("\narm: %s   (annotation: K96243 chr1, RefSeq)" % arm)
    print("clustered = NN < %d bp (n=%d);  isolated = NN >= %d bp (n=%d)\n"
          % (CLUSTERED_MAX, len(clustered), ISOLATED_MIN, len(isolated)))
    print("%-22s %10s %12s %12s %10s" %
          ("feature class", "genome %", "clustered", "isolated", "enrich"))
    print("-" * 100)
    for name, ivs in (("mobile elements", mobile), ("rRNA", rrna),
                      ("mobile + rRNA", merge(list(mobile) + list(rrna))),
                      ("any CDS", cds)):
        c = count_in(clustered, ivs)
        i = count_in(isolated, ivs)
        cf = c / len(clustered) if clustered else 0
        isf = i / len(isolated) if isolated else 0
        enr = (cf / isf) if isf else float("nan")
        print("%-22s %9.2f%% %6d (%5.2f%%) %6d (%5.2f%%) %9s"
              % (name, 100 * bp(ivs) / genome_len, c, 100 * cf, i, 100 * isf,
                 ("%.2fx" % enr) if enr == enr else "n/a"))

    mr = merge(list(mobile) + list(rrna))
    c = count_in(clustered, mr)
    print("\n  READING")
    print("    %d of %d clustered SNPs (%.2f%%) fall in a mobile element or rRNA."
          % (c, len(clustered), 100 * c / len(clustered) if clustered else 0))
    if clustered and (c / len(clustered)) < 0.05:
        print("    Mobile elements and rRNA cannot account for snippy's clustered")
        print("    SNPs. Combined with the nucmer self-alignment result, the")
        print("    mismapping explanation is quantitatively excluded, not merely")
        print("    unsupported.")
    else:
        print("    A material share is mobile/rRNA-associated -- mismapping may")
        print("    explain part of snippy's clustered excess.")
    return 0


def selftest():
    fails = []

    def chk(desc, got, want):
        ok = got == want
        print("%-58s %s" % (desc, "ok" if ok else "FAIL got=%r want=%r" % (got, want)))
        if not ok:
            fails.append(desc)

    chk("merge joins touching intervals", merge([(1, 10), (11, 20)]), [(1, 20)])
    chk("merge keeps disjoint", merge([(1, 10), (50, 60)]), [(1, 10), (50, 60)])
    chk("count_in inclusive", count_in([1, 10], [(1, 10)]), 2)
    chk("count_in excludes outside", count_in([11], [(1, 10)]), 0)
    chk("LOC_RE reads complement()", LOC_RE.findall("complement(100..200)"),
        [("100", "200")])
    chk("LOC_RE reads join()", LOC_RE.findall("join(1..5,10..20)"),
        [("1", "5"), ("10", "20")])
    chk("MOBILE_RE catches transposase", bool(MOBILE_RE.search("IS3 family transposase")), True)
    chk("MOBILE_RE ignores ordinary gene",
        bool(MOBILE_RE.search("50S ribosomal protein L2")), False)
    print("\n%d test(s) failed" % len(fails) if fails else "\nall tests passed")
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--gb", default="")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.report:
        if not a.gb:
            print("need --gb", file=sys.stderr)
            return 1
        return report(a.gb)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
