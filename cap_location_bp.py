#!/usr/bin/env python3
"""Locate the Gubbins diversity cap from the reference-sensitivity runs.

The ~1,000 mean-pairwise-core-SNP cap in REVISED_STRATEGY §2.3 is *derived*
from a contrast-ratio argument, not measured. Seng's 351-549 is the only
empirical anchor. Appendix A.5 bracketed the cap to (535, 9433] using two
clusters; this assembles every cluster that has been run into one table so the
bracket can be closed.

For each cluster it reports, on the CLOSE reference only (the unbiased arm):

  measured mean pairwise SNPs   ground truth, whole genome, from the alignments
  proxy / measured              the Mash-proxy bias factor (A.5)
  union coverage                fraction of the replicon recombinant on at
                                least one branch. Compare to 78% of K96243.
                                NOT a per-branch sum -- see union_coverage().
  median block bp               real tracts are ~5 kb (Nandi). The mapping
                                caller emits sub-100 bp "blocks"; the
                                reference-free callers do not, at ANY
                                diversity, so those are a caller artefact.
  pooled r/m                    NOT the per-branch median, which is dominated
                                by zero-SNP branches in tight clusters and
                                inverts the ordering (A.5).
  reference inflation           tracks the POST-Gubbins SNP count, i.e. the
                                denominator -- not raw cluster diversity.

Usage:
    python3 cap_location_bp.py [--clusters 0,53,16] [--selftest]
"""

import argparse
import csv
import glob
import os
import statistics
import sys

# Mash-proxy values from cluster_diversity.tsv, keyed by cluster id.
DIVERSITY_TSV = "cluster_diversity.tsv"
SENG_BAND = (351, 549)


def load_ska_measured():
    """ska-derived measured diversity, the units DATING_MAX is expressed in.

    `measured_mean_pairwise` computed from core.aln runs ~10% ABOVE ska for the
    same cluster (A.11: cluster_37 3,193 vs 2,894; cluster_16 3,639 vs 3,291).
    DATING_MAX = 4700 is a ska-scale number, so comparing it against an
    alignment-scale value would misclassify anything near the boundary.
    """
    out = {}
    p = "cluster_diversity_measured.tsv"
    if not os.path.exists(p):
        return out
    with open(p) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r.get("status") == "ok" and (r.get("mean_snps") or "").strip():
                out[r["cluster_id"]] = float(r["mean_snps"])
    return out


def load_proxy():
    out = {}
    if not os.path.exists(DIVERSITY_TSV):
        return out
    with open(DIVERSITY_TSV) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            v = (r.get("approx_mean_snps") or "").strip()
            if v:
                out[r["cluster_id"]] = float(v)
    return out


def measured_mean_pairwise(cluster_dir, caller="existing"):
    """Whole-genome mean pairwise SNPs on the close reference, pre-Gubbins.

    Summed across replicons, because a per-replicon figure is half an answer
    and comparing one replicon against a whole-genome cap is the mistake A.3d
    made.
    """
    try:
        from calibrate_mash_snp_bp import read_fasta, pairwise_stats
    except ImportError:
        return None, None
    pre = post = 0.0
    seen = 0
    for rep in ("chr1", "chr2"):
        d = os.path.join(cluster_dir, "arms", "close__%s__%s" % (caller, rep))
        aln = os.path.join(d, "core.aln")
        gub = os.path.join(d, "gubbins.filtered_polymorphic_sites.fasta")
        if os.path.exists(aln):
            st = pairwise_stats([(n, s) for n, s in read_fasta(aln)
                                 if not n.startswith("Node_")])
            if st:
                pre += st["mean_scaled"]
                seen += 1
        if os.path.exists(gub):
            st = pairwise_stats([(n, s) for n, s in read_fasta(gub)
                                 if not n.startswith("Node_")])
            if st:
                post += st["mean_scaled"]
    return (pre if seen else None), (post if seen else None)


def union_coverage(gff, glen):
    """Fraction of the replicon flagged recombinant on AT LEAST ONE branch.

    This is the correct 'how much of the genome has ever recombined' statistic
    and the one comparable to the literature's 78% for K96243. Summing the
    per-branch masked bases instead (as an earlier version of this file did)
    counts shared sites once per branch, so it exceeds 1.0 whenever branch
    count x per-branch masking does -- which says nothing about saturation.
    """
    iv = []
    for line in open(gff):
        if line.startswith("#"):
            continue
        f = line.rstrip("\n").split("\t")
        if len(f) >= 5:
            try:
                iv.append((int(f[3]), int(f[4])))
            except ValueError:
                pass
    iv.sort()
    total = 0
    cs = ce = None
    for s, e in iv:
        if cs is None:
            cs, ce = s, e
        elif s <= ce + 1:
            ce = max(ce, e)
        else:
            total += ce - cs + 1
            cs, ce = s, e
    if cs is not None:
        total += ce - cs + 1
    return total / glen if glen else float("nan")


def gubbins_stats(arm_dir):
    """Union coverage, block sizes and pooled r/m for one arm."""
    pb = os.path.join(arm_dir, "gubbins.per_branch_statistics.csv")
    gff = os.path.join(arm_dir, "gubbins.recombination_predictions.gff")
    if not os.path.exists(pb):
        return None
    with open(pb) as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    if not rows:
        return None
    snp_in = sum(int(r["Number of SNPs Inside Recombinations"]) for r in rows)
    snp_out = sum(int(r["Number of SNPs Outside Recombinations"]) for r in rows)
    recbp = sum(int(r["Bases in Recombinations Excluding Gaps"]) for r in rows)
    glen = max(int(r["Genome Length"]) for r in rows)
    per_branch = [float(r["r/m"]) for r in rows if r["r/m"] not in ("", "NA")]
    zero = sum(1 for v in per_branch if v == 0.0)

    lens = []
    if os.path.exists(gff):
        for line in open(gff):
            if line.startswith("#"):
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) >= 5:
                try:
                    lens.append(int(f[4]) - int(f[3]) + 1)
                except ValueError:
                    pass
    lens.sort()

    def q(p):
        return lens[int(p * len(lens))] if lens else 0

    return {
        "rec_over_genome": recbp / glen if glen else float("nan"),
        "union": union_coverage(gff, glen) if os.path.exists(gff) else float("nan"),
        "pooled_rm": snp_in / snp_out if snp_out else float("nan"),
        "median_rm": statistics.median(per_branch) if per_branch else float("nan"),
        "zero_branch_frac": zero / len(per_branch) if per_branch else float("nan"),
        "n_blocks": len(lens),
        "median_block": statistics.median(lens) if lens else 0,
        "q1_block": q(0.25),
        "q3_block": q(0.75),
        "sub100_frac": (sum(1 for x in lens if x < 100) / len(lens)) if lens else float("nan"),
    }


def snp_counts(cluster_dir):
    """Post-Gubbins SNP counts per (reference, caller, replicon) from the summary."""
    p = os.path.join(cluster_dir, "reference_sensitivity_summary.tsv")
    if not os.path.exists(p):
        return {}
    out = {}
    with open(p) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            key = (r.get("reference"), r.get("caller"), r.get("replicon"))
            try:
                out[key] = int(float(r["post_gubbins_snps"]))
            except (KeyError, TypeError, ValueError):
                pass
    return out


def ref_inflation(cluster_dir):
    """existing-caller SNP inflation, close -> K96243, per replicon."""
    sc = snp_counts(cluster_dir)
    out = {}
    for rep in ("chr1", "chr2"):
        close = sc.get(("close", "existing", rep))
        far = sc.get(("K96243", "existing", rep))
        if close and far:
            out[rep] = 100.0 * (far - close) / close
    return out


LIT_UNION = 0.78   # 78% of K96243 ever recombined
LIT_RM = 7.2       # Nandi genome-wide r/m -- SPECIES-WIDE, see caveat below

# Detection gate, CALIBRATED 2026-08-11 on 19 measured units (Appendix A.11c).
# Sorted union values leave a 41.4-point EMPTY BAND between 18.0% and 59.5%, so
# any cutoff in 0.20-0.58 classifies identically: 17/19 pass, and only cluster_62
# (0.7%) and cluster_53 (18.0%) are excluded. 0.47 is retained because it sits in
# the middle of that band -- NOT because 0.6 x 0.78 was principled.
UNION_MIN = 0.47
UNION_BAND = (0.20, 0.58)   # any value here gives the same verdicts

# Dating ceiling, in SKA units. RE-CORRECTED 2026-08-11 (third revision).
#
# Measured on 11 CONTINUOUS clusters using the REFERENCE-FREE caller (ska_map),
# which is the arbiter for every other statistic here and must be for slopes too:
#   sound   2,894 / 3,291 / 3,833 / 4,671  (3.9e-06, 5.4e-07, 1.5e-06, 3.3e-06)
#   unsound 6,342 / 8,872 / 9,411 / 9,635 / 10,018 / 13,826
#   ANOMALY 9,617 (cluster_0) is sound at 3.7e-06 -- unexplained, 1 of 11.
# => ceiling bracketed to (4,671, 6,342], the SAME bracket as the r/m collapse.
#
# Two earlier errors, both recorded so they are not repeated:
#  1. It was lowered to 3,300 because cluster_48 fails at ska 4,562 -- but
#     cluster_48 is a MIXTURE, and A.10 established that mixtures cannot set a
#     diversity threshold because their failures are confounded by structure.
#     Both failures below 6,342 (cluster_48, cluster_8) are mixtures.
#  2. Slopes were being read off the MAPPING caller, which inflates them via
#     false positives -- it reports 1.8e-05 for cluster_0 where ska_map reports
#     3.7e-06. Read slopes from ska_map.
#
# The dating ceiling and the r/m ceiling COINCIDE. A.11d's "two ceilings" claim
# is withdrawn.
DATING_MAX = 4700
DATING_BRACKET = (4671, 6342)   # continuous clusters, reference-free caller

# There is deliberately NO union requirement for dating. The obvious hypothesis
# -- that residual contamination (LIT_UNION - union) drives the ~50x slope
# inflation -- was tested and REFUTED (A.11c): cluster_0 has the highest union
# (86.5%) and an inflated slope, cluster_53 the lowest (18.0%) and a sound one.
# Diversity predicts datability; union does not. Do not add one back.


def verdict(union, rm_free, mean_pw=None):
    """Judge an arm. Revised 2026-08-10 per Appendix A.9.

    DO NOT judge on r/m against LIT_RM. That was a category error: 7.2 is a
    species-wide, genome-wide figure, and within a shallow cluster r/m should be
    lower regardless. Nine of ten measurements across five clusters sit at
    0.94-1.49, so that IS the norm, not a "contrast loss" failure. Only
    cluster_16 (6.25/8.66) departs from it, and whether that reflects a narrow
    detection window or an atypical lineage is UNRESOLVED.

    What is solid (5/5 clusters):
      union << 0.78            -> genuine under-detection of recombination
      mean_pw above DATING_MAX -> root-to-tip returns nonsense (large magnitude,
                                  sometimes negative). Do not date it.
    """
    if union != union:
        return "incomplete"
    if union < UNION_MIN:
        return "under-detection (recombination missed)"
    if mean_pw is not None and mean_pw > DATING_MAX:
        return "recombination OK; DO NOT DATE (diversity > %d)" % DATING_MAX
    return "recombination OK; datable"


def selftest():
    fails = []

    def chk(desc, got, want, tol=1e-9):
        if abs(got - want) > tol:
            fails.append("%s: got %r want %r" % (desc, got, want))

    # cluster_53: union 0.173 -> recombination genuinely missed
    if not verdict(0.173, 1.12, 535).startswith("under-detection"):
        fails.append("cluster_53 should be under-detection")
    # cluster_16: ska 3,291 (NOT the alignment value 3,639 -- DATING_MAX is ska-scale)
    if verdict(0.732, 6.25, 3291) != "recombination OK; datable":
        fails.append("cluster_16 at ska 3,291 should be datable")
    # cluster_48/8/0: union fine but too diverse to date. Low r/m must NOT matter.
    # ska-scale values. cluster_48 is DELIBERATELY absent: at ska 4,562 it sits
    # BELOW the ceiling, so the diversity gate passes it. Its dating failure is
    # structural (it is a mixture) and is screened upstream by modality, not here.
    for cl, u, rm, pw in (("c8", 0.765, 1.10, 8012), ("c0", 0.848, 1.02, 9617)):
        if "DO NOT DATE" not in verdict(u, rm, pw):
            fails.append("%s should be OK-but-not-datable" % cl)
    # CALIBRATION (A.11c): every cutoff in UNION_BAND must give identical verdicts.
    # The two failures and the two extremes of the working range are the anchors.
    lo, hi = UNION_BAND
    if not (lo <= UNION_MIN <= hi):
        fails.append("UNION_MIN %.2f outside its calibrated band %r" % (UNION_MIN, UNION_BAND))
    for cut in (lo, UNION_MIN, hi):
        if not (0.007 < cut and 0.180 < cut):
            fails.append("cutoff %.2f fails to exclude cluster_62/cluster_53" % cut)
        if cut > 0.595:
            fails.append("cutoff %.2f would wrongly exclude s1_L1_27" % cut)
    # s1_L1_27 (union 0.595) must PASS; cluster_53 (0.180) must NOT
    if verdict(0.595, 2.57, 1698) != "recombination OK; datable":
        fails.append("s1_L1_27 should pass the calibrated gate")
    if not verdict(0.180, 1.25, 535).startswith("under-detection"):
        fails.append("cluster_53 should fail the calibrated gate")
    # DATING_MAX must lie inside its measured bracket, not below it
    lo_d, hi_d = DATING_BRACKET
    if not (lo_d <= DATING_MAX <= hi_d):
        fails.append("DATING_MAX %d outside measured bracket %r" % (DATING_MAX, DATING_BRACKET))
    # every CONTINUOUS cluster with a sound reference-free slope must be datable
    for cl, pw in (("c37", 2894), ("c16", 3291), ("c26", 3833), ("c15", 4671)):
        if verdict(0.76, 5.0, pw) != "recombination OK; datable":
            fails.append("%s at ska %d has a sound slope and must be datable" % (cl, pw))
    # every CONTINUOUS cluster with an unsound slope must be refused
    for cl, pw in (("c10", 6342), ("c11", 8872), ("c51", 9411), ("c2", 13826)):
        if "DO NOT DATE" not in verdict(0.82, 1.5, pw):
            fails.append("%s at ska %d has an unsound slope and must be refused" % (cl, pw))
    # mixtures must NOT be used to set the ceiling: cluster_48 (4,562) is a
    # mixture and sits BELOW the ceiling, so the gate lets it through on
    # diversity. Structure is screened separately, upstream.
    if "DO NOT DATE" in verdict(0.73, 1.2, 4562):
        fails.append("cluster_48 (mixture, ska 4,562) must not be refused on DIVERSITY")

    # union must NOT gate dating (A.11c refutation)
    if verdict(0.865, 1.0, 9617) == verdict(0.865, 1.0, 3000):
        fails.append("dating verdict must depend on diversity, not union")
    if verdict(0.50, 5.0, 3000) != verdict(0.86, 5.0, 3000):
        fails.append("union level must NOT change the datable verdict")

    # r/m must not change the verdict at all
    if verdict(0.75, 1.0, 3000) != verdict(0.75, 8.0, 3000):
        fails.append("r/m must not affect the verdict (A.9)")
    if verdict(float("nan"), 6.0, 3000) != "incomplete":
        fails.append("NaN union should be incomplete")

    # union_coverage must merge overlaps rather than sum them
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".gff", delete=False) as fh:
        fh.write("##gff-version 3\n")
        fh.write("c\t.\tr\t1\t100\t.\t.\t.\tx\n")     # 1-100
        fh.write("c\t.\tr\t50\t150\t.\t.\t.\tx\n")    # overlaps -> union 1-150
        fh.write("c\t.\tr\t500\t599\t.\t.\t.\tx\n")   # disjoint 100 bp
        p = fh.name
    chk("union merges overlaps", union_coverage(p, 1000), 0.250)
    os.unlink(p)

    # Seng band membership, used only for annotation.
    if not (SENG_BAND[0] <= 535 <= SENG_BAND[1]):
        fails.append("535 should sit inside Seng's band")
    if SENG_BAND[0] <= 9433 <= SENG_BAND[1]:
        fails.append("9433 should sit outside Seng's band")

    if fails:
        print("SELFTEST FAILED (%d)" % len(fails))
        for f in fails:
            print("  " + f)
        return 1
    print("selftest: 26/26 checks passed")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--clusters", default="",
                    help="comma-separated ids, e.g. 0,53,16 (default: all refsens_cluster*)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()

    if args.clusters.strip():
        dirs = ["refsens_cluster%s" % c.strip() for c in args.clusters.split(",")]
    else:
        dirs = sorted(glob.glob("refsens_cluster*"))
    missing = [d for d in dirs if not os.path.isdir(d)]
    for d in missing:
        print("WARNING: %s does not exist -- skipped. Reduced runs live under "
              "reduced_<cluster>/ or fbL1_<cluster>/, not refsens_<cluster>/."
              % d, file=sys.stderr)
    dirs = [d for d in dirs if os.path.isdir(d)]
    if not dirs:
        print("no refsens_cluster* directories found", file=sys.stderr)
        return 2

    proxy = load_proxy()
    ska = load_ska_measured()
    recs = []
    for d in dirs:
        cid = "cluster_" + d.replace("refsens_cluster", "")
        pre, post = measured_mean_pairwise(d)
        g1 = gubbins_stats(os.path.join(d, "arms", "close__existing__chr1"))
        g2 = gubbins_stats(os.path.join(d, "arms", "close__existing__chr2"))
        # the reference-free arms are the arbiter: they carry no mapping step,
        # so they cannot manufacture the false positives the mapping caller does
        f1 = gubbins_stats(os.path.join(d, "arms", "close__ska_map__chr1"))
        f2 = gubbins_stats(os.path.join(d, "arms", "close__ska_map__chr2"))
        infl = ref_inflation(d)
        px = proxy.get(cid)
        # clonal frame is a whole-genome property; average the two replicons
        def avg(items, key):
            vals = [i[key] for i in items if i and i[key] == i[key]]
            return sum(vals) / len(vals) if vals else float("nan")

        recs.append({
            "cid": cid, "proxy": px, "pre": pre, "post": post,
            "ska": ska.get(cid),
            "bias": (px / pre) if (px and pre) else None,
            "union_map": avg((g1, g2), "union"),
            "union_free": avg((f1, f2), "union"),
            "rm_map": avg((g1, g2), "pooled_rm"),
            "rm_free": avg((f1, f2), "pooled_rm"),
            "tract_map": avg((g1, g2), "median_block"),
            "tract_free": avg((f1, f2), "median_block"),
            "g1": g1, "g2": g2, "infl": infl,
        })

    recs.sort(key=lambda r: (r["pre"] is None, r["pre"] or 0))

    print("=" * 100)
    print("CAP LOCATION -- measured on the close (within-cluster) reference")
    print("=" * 100)
    print()
    def fmt(v, spec="%.2f"):
        return (spec % v) if (v is not None and v == v) else "-"

    h = "%-12s %9s %9s %9s %14s %14s %13s  %s" % (
        "cluster", "proxy", "ska", "align", "union map/free",
        "r/m map/free", "tract m/f", "verdict")
    print(h)
    print("-" * len(h))
    for r in recs:
        print("%-12s %9s %9s %9s %14s %14s %13s  %s" % (
            r["cid"],
            fmt(r["proxy"], "%.0f"), fmt(r["ska"], "%.0f"), fmt(r["pre"], "%.0f"),
            "%s / %s" % (fmt(100 * r["union_map"], "%.0f") + "%",
                         fmt(100 * r["union_free"], "%.0f") + "%"),
            "%s / %s" % (fmt(r["rm_map"], "%.1f"), fmt(r["rm_free"], "%.1f")),
            "%s / %s" % (fmt(r["tract_map"], "%.0f"), fmt(r["tract_free"], "%.0f")),
            verdict(r["union_free"], r["rm_free"], r["ska"] if r["ska"] else r["pre"])))

    print()
    print("map  = existing (mapping) caller;  free = ska_map (reference-free) caller.")
    print("union = fraction of replicon recombinant on >=1 branch (NOT a per-branch sum).")
    print("Anchors: union 78%% of K96243 ever recombined; r/m %.1f genome-wide (Nandi);" % LIT_RM)
    print("         median tract ~5 kb. Verdict is judged on the REFERENCE-FREE columns.")
    print("Seng's empirically-successful lineages: %d-%d mean pairwise SNPs." % SENG_BAND)
    print()

    print("Reference inflation (existing caller, close -> K96243) -- the dose-response axis")
    print("-" * 80)
    print("%-12s %12s %10s %10s" % ("cluster", "measured", "chr1", "chr2"))
    for r in recs:
        i = r["infl"]
        if not i:
            continue
        print("%-12s %12s %9s%% %9s%%" % (
            r["cid"], "%.0f" % r["pre"] if r["pre"] else "-",
            "%+.1f" % i["chr1"] if "chr1" in i else "-",
            "%+.1f" % i["chr2"] if "chr2" in i else "-"))

    print()
    print("Block-length detail (sub-100 bp blocks are a MAPPING-CALLER artefact, not tracts)")
    print("-" * 80)
    print("%-12s %-6s %8s %9s %9s %9s %11s %11s" % (
        "cluster", "rep", "blocks", "q1_bp", "med_bp", "q3_bp", "<100bp", "zero_rm_brch"))
    for r in recs:
        for rep, g in (("chr1", r["g1"]), ("chr2", r["g2"])):
            if not g:
                continue
            print("%-12s %-6s %8d %9d %9d %9d %10.0f%% %10.0f%%" % (
                r["cid"], rep, g["n_blocks"], g["q1_block"], g["median_block"],
                g["q3_block"], 100 * g["sub100_frac"], 100 * g["zero_branch_frac"]))

    with open("cap_location.tsv", "w") as fh:
        fh.write("cluster\tproxy_mean_snps\tmeasured_mean_pairwise_pre\t"
                 "measured_mean_pairwise_post\tproxy_bias\tunion_mapping\t"
                 "union_reffree\trm_mapping\trm_reffree\ttract_mapping\t"
                 "tract_reffree\tverdict\tinfl_chr1_pct\tinfl_chr2_pct\n")
        for r in recs:
            fh.write("%s\t%s\t%s\t%s\t%s\t%.4f\t%.4f\t%.3f\t%.3f\t%.0f\t%.0f\t%s\t%s\t%s\n" % (
                r["cid"],
                "%.0f" % r["proxy"] if r["proxy"] else "",
                "%.1f" % r["pre"] if r["pre"] else "",
                "%.1f" % r["post"] if r["post"] else "",
                "%.3f" % r["bias"] if r["bias"] else "",
                r["union_map"], r["union_free"], r["rm_map"], r["rm_free"],
                r["tract_map"], r["tract_free"],
                verdict(r["union_free"], r["rm_free"], r["ska"] if r["ska"] else r["pre"]),
                "%.1f" % r["infl"]["chr1"] if r["infl"].get("chr1") is not None else "",
                "%.1f" % r["infl"]["chr2"] if r["infl"].get("chr2") is not None else ""))
    print("\nwrote cap_location.tsv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
