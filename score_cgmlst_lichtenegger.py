#!/usr/bin/env python3
"""
Attribution scoring on the Lichtenegger cgMLST profiles, expanded panel.

Differences from the earlier PubMLST-scheme run:
  scheme      published B. pseudomallei cgMLST v1.1, 4,221 loci (was PubMLST
              scheme 2, 4,090 loci, unpublished)
  panel       3,033 genomes (was 2,976): + 40 TheiaProk + 17 Mexican references
  validation  44 (was 31): + 13 tier-A/B from the 2026-08-21 batch
              (India 6, Thailand 4, Australia 2, Trinidad and Tobago 1)

The point of the expansion: until now, country attribution was tested almost
entirely on countries with zero or near-zero reference genomes, which is the
most attackable feature of the negative result. India, Thailand and Australia
are the best-represented countries in the collection, and Mexico goes from 4
references to 21. This is the fair test.

Regime is unchanged: leave-group-out, dropping every validation genome sharing
the target's exposure country, so a country cannot be predicted from its own
held-out siblings.

Distance: normalised allelic distance over loci called in BOTH genomes.
Missing-data tokens (LNF, PLOT3, PLOT5, NIPH, NIPHEM, ALM, ASM, LOTSC, PAMA)
are treated as missing, never as a shared state. INF- prefixes are calls.
"""
import argparse
import csv
import os
import statistics as st
from collections import Counter, defaultdict

import numpy as np

B = os.path.dirname(os.path.abspath(__file__))
MISS = {"LNF", "PLOT3", "PLOT5", "NIPH", "NIPHEM", "ALM", "ASM", "LOTSC", "PAMA", "-"}


def load_outbreak_groups():
    """group_id -> {sample_id, ...} for leave-OUTBREAK-out.

    An outbreak group is a set of isolates that are the SAME epidemiological
    source -- one investigation, one strain, one place -- so they are not
    independent observations of geography and must be held out together when any
    member is scored as a validation genome.

    This is an EXPLICIT register, not an automatic same-BioProject / near-clone
    rule, and the reason is a measured counterexample. The two 'USA: CA ex
    Vietnam' validation genomes (SRR31608433/435) sit ~0.01 from two 'USA: GA'
    clinical cases (SRR31608437/438, 1983 and 2024) in the same BioProject. An
    automatic rule holds those out and 'corrects' Viet Nam from 0/2 to 2/2 -- but
    those Georgia cases are INDEPENDENT cases of a lineage that spans Vietnam and
    the US (the 1983 Georgia case is very plausibly a Vietnam-war veteran), not
    co-deposits. Removing them would fake a Viet Nam answer by hiding real
    references, which is the opposite of what a leak control should do. Only
    verified same-source clusters (e.g. the Mississippi environmental+clinical
    isolates, one source on one property, Petras 2023 NEJM) belong here.
    """
    path = f"{B}/OUTBREAK_GROUPS.tsv"
    groups = {}
    if os.path.exists(path):
        for r in csv.DictReader(open(path), delimiter="\t"):
            groups.setdefault(r["group_id"], set()).add(r["sample_id"])
    return groups


def load_profiles(path):
    with open(path) as fh:
        rd = csv.reader(fh, delimiter="\t")
        hdr = next(rd)
        loci = hdr[1:]
        samples, rows = [], []
        for r in rd:
            samples.append(r[0].replace(".fasta", ""))
            out = np.full(len(loci), -1, dtype=np.int32)
            for i, v in enumerate(r[1:]):
                v = v.strip()
                if not v or v in MISS:
                    continue
                if v.startswith("INF-"):
                    v = v[4:]
                if v.startswith("*"):
                    v = v[1:]
                try:
                    out[i] = int(v)
                except ValueError:
                    pass
            rows.append(out)
    return samples, loci, np.vstack(rows)


def dist_one_vs_all(mat, i, pool):
    a = mat[i]
    P = mat[pool]
    both = (a >= 0) & (P >= 0)
    n = both.sum(axis=1)
    diff = ((P != a) & both).sum(axis=1)
    d = np.where(n > 0, diff / np.maximum(n, 1), np.nan)
    return d, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profiles",
                    default=f"{B}/cgmlst_lichtenegger/results/results_alleles.tsv")
    ap.add_argument("--manifest",
                    default=f"{B}/cgmlst_lichtenegger/MANIFEST.tsv")
    ap.add_argument("--out-prefix", default=f"{B}/CGMLST_LICHT")
    ap.add_argument("--estimator", default="modal_k10",
                    help="nearest_neighbour | modal_k5 | modal_k10 | modal_k20 "
                         "| enrichment_k20")
    a = ap.parse_args()

    samples, loci, mat = load_profiles(a.profiles)
    idx_of = {s: i for i, s in enumerate(samples)}
    print(f"profiles: {len(samples)} genomes x {len(loci)} loci")

    drop = {r["sample_id"] for r in
            csv.DictReader(open(f"{B}/PANEL_DUPLICATES_2026-08-21.tsv"),
                           delimiter="\t") if r["action"] == "drop"}
    if drop:
        keep = [i for i, s in enumerate(samples) if s not in drop]
        samples = [samples[i] for i in keep]
        mat = mat[keep]
        idx_of = {s: i for i, s in enumerate(samples)}
        print(f"dropped {len(drop)} duplicate BioSamples -> {len(samples)} genomes")

    ovr = {r["sample_id"]: r["exposure_country"] for r in
           csv.DictReader(open(f"{B}/EXPOSURE_OVERRIDES.tsv"), delimiter="\t")}

    man = {r["sample_id"]: r for r in
           csv.DictReader(open(a.manifest), delimiter="\t")}
    meta = {r["sample_id"]: r for r in
            csv.DictReader(open(f"{B}/L1v4c_MERGED_METADATA.tsv"), delimiter="\t")}

    # leave-outbreak-out: explicit same-source clusters, held out as a unit.
    outbreak_groups = load_outbreak_groups()
    group_of = {s: g for g, mem in outbreak_groups.items() for s in mem}

    # region map, built from the panel's own assignments then applied to new genomes
    reg_of_sample = {r["sample_id"]: r["country"] for r in
                     csv.DictReader(open(f"{B}/assign_region.tsv"), delimiter="\t")}
    c2r = {}
    for s, rg in reg_of_sample.items():
        c = (meta.get(s) or {}).get("country")
        if c and rg:
            c2r.setdefault(c, Counter())[rg] += 1
    country2region = {c: v.most_common(1)[0][0] for c, v in c2r.items()}
    for c, r in [("India", "South Asia"), ("Thailand", "East Asia & Pacific"),
                 ("Australia", "East Asia & Pacific"),
                 ("Trinidad and Tobago", "Latin America & Caribbean"),
                 ("Mexico", "Latin America & Caribbean"),
                 ("Puerto Rico", "Latin America & Caribbean"),
                 ("USA", "North America"), ("Bangladesh", "South Asia")]:
        country2region.setdefault(c, r)

    # labels for the whole pool: country = where the organism was found, except
    # validation genomes, which the panel labels by exposure country already.
    country, region, truth_c, is_val = {}, {}, {}, {}
    for s in samples:
        m = man.get(s, {})
        c = ""
        if m.get("batch") == "v4c_panel":
            c = (meta.get(s) or {}).get("country", "")
            if (meta.get(s) or {}).get("origin_basis") == "travel_reattributed":
                truth_c[s] = (meta[s].get("acquired_from") or c)
                is_val[s] = True
        else:
            c = m.get("country", "")
            if m.get("role") == "ground_truth" and m.get("exposure_country"):
                truth_c[s] = m["exposure_country"]
                c = m["exposure_country"]
                is_val[s] = True
        # a compound value is not a country: treat as missing in the pool as
        # well as in truth, matching origin_resolution == "multi_country" in
        # the core-genome scorer. Left in, it wins nearest-neighbour ties and
        # scores as a wrong answer that is really a metadata artifact.
        if c in ("Panama and Peru", "Africa"):
            c = ""
        if s in ovr:                      # documented exposure beats the label
            truth_c[s] = ovr[s]
            c = ovr[s]
            is_val[s] = True
        country[s] = c
        region[s] = country2region.get(c, "")

    NOTC = {"Africa", "Panama and Peru", ""}
    val = [s for s in samples if is_val.get(s)]
    print(f"validation genomes with a profile: {len(val)}")
    print(f"  by exposure country: "
          f"{dict(Counter(truth_c[s] for s in val).most_common())}")

    scales = {"country": country, "region": region}
    out, summary, allest = [], [], []
    for scale, lab in scales.items():
        hit = tot = unatt = 0
        percountry = defaultdict(lambda: [0, 0])
        for s in val:
            t = truth_c[s]
            if t in NOTC or not lab.get(s):
                unatt += 1
                continue
            held = {x for x in val if truth_c[x] == t}
            # leave-OUTBREAK-out: also hold out the query's whole same-source
            # cluster (verified co-deposits: the environmental + clinical isolates
            # of one investigation), so a near-identical sibling cannot win
            # nearest-neighbour at ~0 distance and leak the true label. Explicit
            # register only -- see load_outbreak_groups for why an automatic
            # same-BioProject/near-clone rule is wrong (the Vietnam/Georgia
            # lineage-spanning counterexample). Empty register => exact no-op.
            if s in group_of:
                held = held | outbreak_groups[group_of[s]]
            pool = [idx_of[x] for x in samples
                    if x not in held and lab.get(x) and x != s]
            if not pool:
                unatt += 1
                continue
            d, n = dist_one_vs_all(mat, idx_of[s], pool)
            if not (~np.isnan(d)).any():
                unatt += 1
                continue
            order = np.argsort(np.where(np.isnan(d), np.inf, d))
            labs = [lab[samples[pool[int(x)]]] for x in order]
            dd = [d[int(x)] for x in order]
            preds = {}
            preds["nearest_neighbour"] = labs[0]
            for K in (5, 10, 20):
                preds[f"modal_k{K}"] = Counter(labs[:K]).most_common(1)[0][0]
            # sampling-corrected enrichment over the k=20 pool, matching the
            # core-genome scorer: a label should not win by being 60% of the panel
            panel_n = Counter(lab[x] for x in samples if lab.get(x))
            tot_n = sum(panel_n.values())
            k20 = Counter(labs[:20])
            preds["enrichment_k20"] = max(
                k20, key=lambda L: (k20[L] / 20) / max(panel_n.get(L, 1) / tot_n, 1e-9))
            j = int(order[0])
            pred = preds[a.estimator]
            ok = int(pred == lab[s])
            tot += 1
            hit += ok
            allest.append({"sample_id": s, "scale": scale, "truth": lab[s],
                           **{k: int(v == lab[s]) for k, v in preds.items()}})
            percountry[t][0] += ok
            percountry[t][1] += 1
            out.append({"sample_id": s, "scale": scale, "exposure_country": t,
                        "truth": lab[s], "predicted": pred, "correct": ok,
                        "nn_distance": f"{np.nanmin(d):.5f}",
                        "nn_sample": samples[pool[j]],
                        "n_loci_compared": int(n[j])})
        base = Counter(lab[s] for s in val if truth_c.get(s) not in NOTC and lab.get(s))
        bl = base.most_common(1)[0][1] if base else 0
        print(f"\n=== {scale} ===")
        print(f"  {hit}/{tot} correct ({100*hit/tot:.0f}%)   "
              f"majority baseline {bl}/{sum(base.values())} "
              f"({100*bl/max(sum(base.values()),1):.0f}%)   "
              f"{unatt} unattributable")
        okc = sum(1 for c, v in percountry.items() if v[0] == v[1])
        print(f"  by exposure country: {okc}/{len(percountry)} fully correct")
        for c, v in sorted(percountry.items(), key=lambda x: -x[1][1]):
            print(f"     {c:<24}{v[0]}/{v[1]}")
        summary.append({"scale": scale, "correct": hit, "scorable": tot,
                        "pct": f"{100*hit/max(tot,1):.1f}",
                        "baseline": bl, "baseline_n": sum(base.values()),
                        "unattributable": unatt,
                        "countries_fully_correct": okc,
                        "countries_tested": len(percountry)})

    with open(f"{a.out_prefix}_ATTRIBUTION.tsv", "w", newline="") as fh:
        w = csv.DictWriter(fh, delimiter="\t", lineterminator="\n",
                           fieldnames=["sample_id", "scale", "exposure_country",
                                       "truth", "predicted", "correct",
                                       "nn_distance", "nn_sample",
                                       "n_loci_compared"])
        w.writeheader(); w.writerows(out)
    with open(f"{a.out_prefix}_SUMMARY.tsv", "w", newline="") as fh:
        w = csv.DictWriter(fh, delimiter="\t", lineterminator="\n",
                           fieldnames=list(summary[0]))
        w.writeheader(); w.writerows(summary)
    print(f"\nwrote {a.out_prefix}_ATTRIBUTION.tsv and _SUMMARY.tsv")

    print("\n=== all estimators, side by side ===")
    ests = ["nearest_neighbour", "modal_k5", "modal_k10", "modal_k20",
            "enrichment_k20"]
    for scale in scales:
        rs = [r for r in allest if r["scale"] == scale]
        if not rs:
            continue
        print(f"  {scale}:")
        for e in ests:
            print(f"     {e:<20}{sum(r[e] for r in rs)}/{len(rs)}"
                  f"  ({100*sum(r[e] for r in rs)/len(rs):.0f}%)")

    # distance stratification: is a "correct" region call backed by a real relative?
    print("\n=== region accuracy stratified by nearest-neighbour distance ===")
    rr = [r for r in out if r["scale"] == "region"]
    for lo, hi, nm in ((0, .05, "d < 0.05  (close relative)"),
                       (.05, .30, "0.05-0.30 (distant)"),
                       (.30, 9, "d >= 0.30 (no real relative)")):
        rs = [r for r in rr if lo <= float(r["nn_distance"]) < hi]
        if rs:
            print(f"  {nm:<34}{sum(r['correct'] for r in rs)}/{len(rs)}")


if __name__ == "__main__":
    main()
