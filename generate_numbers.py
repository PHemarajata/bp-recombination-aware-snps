#!/usr/bin/env python3
"""
Regenerate every quotable figure from primary data into one file: NUMBERS.tsv.

The problem this solves: across 60+ documents, figures were written into prose,
copied onward and never re-derived. Of six headline numbers checked on
2026-08-21, four were wrong in at least one circulating document, and in every
case the code had been right all along. A rewrite would not fix that, because
the mechanism survives it.

The rule this enforces: **documents cite NUMBERS.tsv, they do not restate
values.** If a figure is not in here, it is not quotable.

Each row carries: key, value, and the file it was computed from, so any figure
can be traced without re-reading the code.

Run before quoting anything, and immediately before submission.
"""
import csv
import os
import re
import statistics as st
from collections import Counter

import numpy as np

B = os.path.dirname(os.path.abspath(__file__))
OUT = f"{B}/NUMBERS.tsv"
ROWS = []


def add(key, value, source, note=""):
    ROWS.append(dict(key=key, value=value, source=source, note=note))


def tsv(p):
    with open(p) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def maybe(p):
    return tsv(p) if os.path.exists(p) else []


# ---------------------------------------------------------------- panel -----
meta = tsv(f"{B}/L1v4c_MERGED_METADATA.tsv")
dup = {r["sample_id"] for r in maybe(f"{B}/PANEL_DUPLICATES_2026-08-21.tsv")}
exc = {r["sample_id"] for r in maybe(f"{B}/PANEL_EXCLUSIONS.tsv")}
panel = {r["sample_id"] for r in meta}
removed = (dup | exc) & panel
corrected = panel - removed

add("panel.v4c", len(panel), "L1v4c_MERGED_METADATA.tsv")
add("panel.removed_duplicate", len(dup & panel), "PANEL_DUPLICATES_2026-08-21.tsv")
add("panel.removed_excluded", len(exc & panel), "PANEL_EXCLUSIONS.tsv")
add("panel.corrected_v4d", len(corrected), "PANEL_v4d_2026-08-21.tsv",
    "quote this, not 2976")
add("panel.countries", len({r["country"] for r in meta
                            if r["sample_id"] in corrected and r["country"]}),
    "L1v4c_MERGED_METADATA.tsv")

cc = Counter(r["country"] for r in meta if r["sample_id"] in corrected and r["country"])
tot = sum(cc.values())
for c, n in cc.most_common(3):
    add(f"panel.top_country.{c}", f"{n} ({100*n/tot:.1f}%)", "L1v4c_MERGED_METADATA.tsv")
add("panel.top3_share", f"{100*sum(n for _, n in cc.most_common(3))/tot:.1f}%",
    "L1v4c_MERGED_METADATA.tsv")

prov = Counter()
for r in meta:
    if r["sample_id"] not in corrected:
        continue
    s = r["sample_id"]
    prov["in_house" if s.startswith(("IP-", "IE-")) else "public_derived"] += 1
add("panel.in_house", prov["in_house"], "sample_id prefix")
add("panel.public_derived", prov["public_derived"], "sample_id prefix")

# ------------------------------------------------------------- clusters -----
clus = maybe(f"{B}/curated_L1v4c_clusters.tsv")
if clus:
    size = Counter(r["cluster_id"] for r in clus
                   if r["sample_id"] not in removed)
    add("units.analysed", len([u for u, n in size.items() if n >= 7]),
        "curated_L1v4c_clusters.tsv", "after removals, n>=7")
    add("units.below_floor_after_removal",
        ";".join(f"{u}(n={n})" for u, n in sorted(size.items()) if n < 7) or "none",
        "curated_L1v4c_clusters.tsv", "must be dropped as units")
    add("genomes.analysed", sum(n for n in size.values() if n >= 7),
        "curated_L1v4c_clusters.tsv")

# ----------------------------------------------------------- validation -----
ovr = {r["sample_id"]: r["exposure_country"] for r in
       maybe(f"{B}/EXPOSURE_OVERRIDES.tsv")}
man = maybe(f"{B}/cgmlst_lichtenegger/MANIFEST.tsv")
val = {r["sample_id"] for r in meta
       if r.get("origin_basis") == "travel_reattributed"} | set(ovr)
newgt = {r["sample_id"] for r in man if r.get("role") == "ground_truth"}
val = (val | newgt) - removed
add("validation.total", len(val), "origin_basis + EXPOSURE_OVERRIDES + MANIFEST",
    "REGISTERED genomes. This is NOT the denominator of any attribution "
    "number: 2 carry a non-country exposure ('Africa', 'Panama and Peru') and "
    "are unattributable, leaving 46 SCORABLE. The frozen validation set is "
    "quoted as 46 -- see validation.scorable")
truth = {}
for r in meta:
    if r["sample_id"] in val:
        truth[r["sample_id"]] = r.get("acquired_from") or r.get("country")
for r in man:
    if r["sample_id"] in val and r.get("exposure_country"):
        truth[r["sample_id"]] = r["exposure_country"]
truth.update({k: v for k, v in ovr.items() if k in val})
NOTC = {"Africa", "Panama and Peru", ""}
add("validation.scorable", sum(1 for v in truth.values() if v not in NOTC),
    "exposure country",
    "THE ATTRIBUTION DENOMINATOR. Every x/46 in this file is over this set")
add("validation.source_countries",
    len({v for v in truth.values() if v not in NOTC}),
    "exposure country", "excludes 'Africa' and 'Panama and Peru'")

# ------------------------------------------------------------ ENA census ----
S = ("/tmp/claude-1000/-home-phemarajata-Downloads-snp-mod-local-working/"
     "c4b0a8cc-da3c-4dda-a59f-74514bfa4ad8/scratchpad")
if os.path.exists(f"{S}/ena_all_runs.tsv"):
    bs = {}
    for f, a in ((f"{S}/ena_all_runs.tsv", "run_accession"),
                 (f"{S}/ena_all_asm.tsv", "accession")):
        for r in tsv(f):
            k = r["sample_accession"]
            c = (r.get("country") or "").split(":")[0].strip()
            if k and (k not in bs or (not bs[k] and c)):
                bs[k] = c
    withc = sum(1 for v in bs.values() if v)
    add("ena.biosamples_union", len(bs), "ENA portal API, read_run + assembly",
        "MUST union both; read_run alone misses assembly-only depositions")
    add("ena.biosamples_with_country", withc, "ENA portal API")
    add("ena.countries", len({v for v in bs.values() if v}), "ENA portal API")
    add("panel.coverage_of_ena", f"{100*len(corrected)/withc:.1f}%",
        "derived", "quote this, not 44%")

# ---------------------------------------------------- cgMLST + attribution --
stats = maybe(f"{B}/cgmlst_lichtenegger/results/results_statistics.tsv")
if stats:
    TOTL = 4221
    rates = [100*(int(r["EXC"])+int(r["INF"]))/TOTL for r in stats]
    add("cgmlst.scheme", "Lichtenegger v1.1, 4221 loci, PMID 33980649",
        "cgmlst.org/ncs/schema/Bpseudomallei")
    add("cgmlst.genomes", len(stats), "results_statistics.tsv")
    add("cgmlst.call_rate_median", f"{st.median(rates):.1f}%", "results_statistics.tsv")
    add("cgmlst.genomes_above_90pct",
        f"{100*sum(1 for x in rates if x >= 90)/len(rates):.1f}%",
        "results_statistics.tsv")

# Attribution is reported PER ESTIMATOR, with the estimator IN THE KEY.
#
# Why the keys changed (2026-08-23). CGMLST_LICHT_ATTRIBUTION.tsv holds exactly
# one estimator's calls -- whichever was passed to --estimator -- and the frozen
# copy is NEAREST NEIGHBOUR. Country's best estimator is NN, so that row was
# right. Region's best estimator is modal k=20, so the old
# `attribution.region.correct` row published 37/46 (80%) while every document
# quoted the modal 41/46 (89%), and the region strata printed beside it were
# NN-derived. A modal headline over NN strata is precisely the comparison this
# project forbids, and it was latent in the one file everyone is told to quote.
# The modal figures now come from GROUPING_LADDER.tsv / GROUPING_PREDICTIONS.tsv,
# which grouping_test_bp.py persists as of the same date; before that they
# existed only as terminal output and prose.
STRATA = ((0, .05, "d_lt_0.05"), (.05, .30, "d_0.05_0.30"), (.30, 9, "d_ge_0.30"))


def strata_rows(prefix, rows, src):
    for lo, hi, nm in STRATA:
        s = [r for r in rows if lo <= float(r["nn_distance"]) < hi]
        if s:
            add(f"{prefix}.{nm}", f"{sum(int(r['correct']) for r in s)}/{len(s)}",
                src, "ALWAYS report the stratification with its headline, and "
                     "ONLY against the same estimator")


att = maybe(f"{B}/CGMLST_LICHT_ATTRIBUTION.tsv")
if att:
    for sc in ("country", "region"):
        rs = [r for r in att if r["scale"] == sc]
        if not rs:
            continue
        ok = sum(int(r["correct"]) for r in rs)
        add(f"attribution.{sc}.nearest_neighbour",
            f"{ok}/{len(rs)} ({100*ok/len(rs):.0f}%)",
            "CGMLST_LICHT_ATTRIBUTION.tsv",
            "QUOTE THIS as the country headline: NN is country's best estimator"
            if sc == "country" else
            "NOT the region headline -- region's best estimator is modal k=20; "
            "quote attribution.region.modal_k20 (41/46) instead")
        strata_rows(f"attribution.{sc}.nearest_neighbour", rs,
                    "CGMLST_LICHT_ATTRIBUTION.tsv")

lad = maybe(f"{B}/GROUPING_LADDER.tsv")
prd = maybe(f"{B}/GROUPING_PREDICTIONS.tsv")
if lad:
    L = {(r["grouping"], r["estimator"]): r for r in lad}
    hr = L.get(("region_7way", "modal_k20"))
    if hr:
        add("attribution.region.modal_k20",
            f"{hr['correct']}/{hr['n']} "
            f"({100*int(hr['correct'])/int(hr['n']):.0f}%)",
            "GROUPING_LADDER.tsv",
            "QUOTE THIS as the region headline. The NN region figure is 37/46 "
            "(80%) and is a DIFFERENT estimator, not a correction")
        if prd:
            strata_rows("attribution.region.modal_k20",
                        [x for x in prd if x["grouping"] == "region_7way"
                         and x["estimator"] == "modal_k20"],
                        "GROUPING_PREDICTIONS.tsv")
    # Cohen's kappa is the only statistic comparable ACROSS groupings: raw
    # accuracy rewards a binary split with a lopsided majority class for saying
    # nothing. The ladder is the depth-ceiling result -- deep splits are
    # recovered perfectly, shallow ones are not.
    for g, est in (("country", "nearest_nb"), ("region_7way", "modal_k20"),
                   ("sea_vs_not", "modal_k20"), ("asia_vs_not", "modal_k20"),
                   ("east_vs_west", "modal_k20")):
        r = L.get((g, est))
        if r:
            add(f"ladder.{g}.kappa", f"{float(r['kappa']):.3f}",
                "GROUPING_LADDER.tsv",
                f"{est}, n={r['n']}, {r['classes']} classes; accuracy "
                f"{100*float(r['accuracy']):.0f}% vs baseline "
                f"{100*float(r['baseline']):.0f}%")

add("attribution.NOTE_estimator",
    "country best under nearest_neighbour; region best under modal_k20",
    "score_cgmlst_lichtenegger.py + grouping_test_bp.py",
    "NEVER compare an NN number to a modal one -- the estimator is in every "
    "key above precisely so that comparison cannot be made by accident")

# ------------------------------------------------------------------- r/m ----
# r/m comes from the pipeline's own POOL_RECOMBINATION_STATS output, not from
# the unit_rm column of the metadata. That column is a per-genome DENORMALISED
# COPY of a per-unit quantity, and a copy is exactly what goes stale: after the
# 2026-08-21 re-derivation it still read 3.1042 for strain_1_L1_26 (true value
# 4.4713) and still carried a value for strain_1_L1_10, a unit that no longer
# exists. Read the authoritative table; fall back only if it is absent.
RM_TSV = f"{B}/L1v4c_out/Summaries/recombination_rm.tsv"
per = {}
rm_src = "L1v4c_out/Summaries/recombination_rm.tsv"
if os.path.isfile(RM_TSV):
    for r in csv.DictReader(open(RM_TSV), delimiter="\t"):
        try:
            per[r["unit"]] = float(r["rm_corrected"])
        except (KeyError, ValueError):
            pass
else:
    rm_src = "L1v4c_MERGED_METADATA.tsv (FALLBACK - authoritative table missing)"
    for r in meta:
        if r.get("subcluster") and r.get("unit_rm") and r["sample_id"] in corrected:
            try:
                per[r["subcluster"]] = float(r["unit_rm"])
            except ValueError:
                pass
if per:
    v = sorted(per.values())
    add("rm.units_with_value", len(v), rm_src)
    add("rm.median_all_units", f"{st.median(v):.2f}", rm_src,
        "DO NOT QUOTE: mixes measurements with detection failures")
    cl = sorted(float(r["rm_corrected"])
                for r in csv.DictReader(open(RM_TSV), delimiter="\t")
                if r.get("rm_corrected") not in (None, "", "NA")
                and r.get("max_kept_branch_len")
                and float(r["max_kept_branch_len"]) < 1000) if os.path.isfile(RM_TSV) else []
    if cl:
        add("rm.median_no_divergent_member", f"{st.median(cl):.2f}", rm_src,
            f"n={len(cl)} units whose longest surviving branch is <1000 subs; "
            "the rest are depressed by a divergent member, not by biology")
    # Gate 1 membership from ALIGNMENT-derived distances, not the Mash proxy.
    # Two prior versions of this block were wrong in instructive ways:
    #   - it hardcoded "7.38" copied from METHODS_DRAFT (that is the A100 /
    #     88-unit variant, not this 85-unit table);
    #   - it then computed 7.26 from `mash x 3,805,619`, a triage-grade
    #     conversion in a different unit system from the window's calibration.
    # GATE1_ALIGNMENT_RESULT_2026-08-21.md shows the proxy is off by a median
    # 1.30x and up to 17x, and misplaces 22 of 85 units. The window's structure
    # is confirmed on alignment distances; its FLOOR was in the wrong place.
    # Relocated on union coverage and tract length -- NOT on r/m, which would be
    # circular -- to [700, 4700], floor bracketed (588, 755].
    DIST = f"{B}/DISTANCES_v4c_SUMMARY.tsv"
    G1_FLOOR, G1_CEIL = 700.0, 4700.0
    if os.path.isfile(DIST) and os.path.isfile(RM_TSV):
        aln = {}
        for r in csv.DictReader(open(DIST), delimiter="\t"):
            try:
                aln[r["unit"]] = aln.get(r["unit"], 0.0) + float(r["raw_mean"])
            except (KeyError, ValueError):
                continue
        g1 = [v for u, v in per.items()
              if u in aln and G1_FLOOR <= aln[u] <= G1_CEIL]
        out = [v for u, v in per.items()
               if u in aln and not (G1_FLOOR <= aln[u] <= G1_CEIL)]
        if g1:
            add("rm.gate1_units", len(g1),
                "DISTANCES_v4c_SUMMARY + recombination_rm",
                "units inside Gate 1, [700, 4700] mean pairwise core SNPs, "
                "ALIGNMENT-derived (floor bracketed (588, 755])")
            add("rm.median_gate1", f"{st.median(sorted(g1)):.2f}",
                "DISTANCES_v4c_SUMMARY + recombination_rm",
                "QUOTE THIS. Was 7.26 on the Mash proxy; the proxy misplaced 22 "
                "of 85 units. Outside the window a low r/m is a detection "
                "failure, not a measurement")
        if out:
            add("rm.median_outside_gate1", f"{st.median(sorted(out)):.2f}",
                "DISTANCES_v4c_SUMMARY + recombination_rm",
                f"n={len(out)}; the contrast against rm.median_gate1 is what "
                "makes the window a detection window rather than a filter")
    add("rm.gate1_caveat",
        "union coverage does not reproduce the calibration's 76-88% "
        "(max band median 68%) -- disclose",
        "GATE1_ALIGNMENT_RESULT_2026-08-21.md §7",
        "the floor does not depend on it, but the coverage criterion does not "
        "reproduce quantitatively")

# ------------------------------------------------------------------ write ---
with open(OUT, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["key", "value", "source", "note"],
                       delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(ROWS)
print(f"wrote {OUT}  ({len(ROWS)} figures)")
for r in ROWS:
    flag = "  <-- " + r["note"] if r["note"] else ""
    print(f"  {r['key']:<44}{str(r['value'])[:34]:<36}{flag}")
