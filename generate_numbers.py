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
add("validation.total", len(val), "origin_basis + EXPOSURE_OVERRIDES + MANIFEST")
truth = {}
for r in meta:
    if r["sample_id"] in val:
        truth[r["sample_id"]] = r.get("acquired_from") or r.get("country")
for r in man:
    if r["sample_id"] in val and r.get("exposure_country"):
        truth[r["sample_id"]] = r["exposure_country"]
truth.update({k: v for k, v in ovr.items() if k in val})
NOTC = {"Africa", "Panama and Peru", ""}
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

att = maybe(f"{B}/CGMLST_LICHT_ATTRIBUTION.tsv")
if att:
    for sc in ("country", "region"):
        rs = [r for r in att if r["scale"] == sc]
        if not rs:
            continue
        ok = sum(int(r["correct"]) for r in rs)
        add(f"attribution.{sc}.correct", f"{ok}/{len(rs)} ({100*ok/len(rs):.0f}%)",
            "CGMLST_LICHT_ATTRIBUTION.tsv", "estimator as run; see NOTE below")
        for lo, hi, nm in ((0, .05, "d_lt_0.05"), (.05, .30, "d_0.05_0.30"),
                           (.30, 9, "d_ge_0.30")):
            s = [r for r in rs if lo <= float(r["nn_distance"]) < hi]
            if s:
                add(f"attribution.{sc}.{nm}",
                    f"{sum(int(r['correct']) for r in s)}/{len(s)}",
                    "CGMLST_LICHT_ATTRIBUTION.tsv",
                    "ALWAYS report the stratification with the headline")

add("attribution.NOTE_estimator",
    "country best under nearest_neighbour; region best under modal_k20",
    "score_cgmlst_lichtenegger.py",
    "NEVER compare an NN number to a modal one")

# ------------------------------------------------------------------- r/m ----
rm = [float(r["unit_rm"]) for r in meta
      if r.get("unit_rm") and r["sample_id"] in corrected]
if rm:
    per = {}
    for r in meta:
        if r.get("subcluster") and r.get("unit_rm") and r["sample_id"] in corrected:
            try:
                per[r["subcluster"]] = float(r["unit_rm"])
            except ValueError:
                pass
    v = sorted(per.values())
    add("rm.units_with_value", len(v), "L1v4c_MERGED_METADATA.tsv")
    add("rm.median_all_units", f"{st.median(v):.2f}", "L1v4c_MERGED_METADATA.tsv",
        "DO NOT QUOTE: mixes measurements with detection failures")
    add("rm.gate1_note",
        "quote 7.38, the median of the 47 in-window units, not the all-unit median",
        "METHODS_DRAFT 2.6.1", "Gate 1 window ~1270-4671 mean pairwise core SNPs")

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
