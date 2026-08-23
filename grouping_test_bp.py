#!/usr/bin/env python3
"""
Which grouping of isolates supports the most accurate prediction?

Two things are tested together, because they interact:

  GROUPINGS   country, the 7-region World Bank scheme, and four coarser splits
              (SEA vs not, Asia vs not, Eastern vs Western hemisphere,
              endemic-core vs not).

  ESTIMATORS  nearest neighbour and modal-k20, which both ask "who is my closest
              relative", versus a GROUP-LEVEL test which asks "am I systematically
              closer to group X than to everything else". The group test is the
              one that recovered South Asia for the aromatherapy strain at
              d ~ 0.74, where nearest neighbour is meaningless.

Raw accuracy is not comparable across groupings: a binary split with a 90%
majority class scores 90% by saying nothing. So the headline statistic is
**Cohen's kappa**, which corrects for chance agreement, alongside accuracy and
its own baseline.

Leave-group-out throughout: every validation genome sharing the target's
exposure country is removed from the pool.

OUTPUTS (added 2026-08-23). This script used to print and persist NOTHING, so
the region headline (modal k=20, 41/46, kappa 0.832) and the whole kappa ladder
lived only in terminal output and in prose. They were therefore outside
generate_numbers.py and outside freeze_basis_bp.py -- nothing would have caught
drift in them, and a reader following the project rule "quote NUMBERS.tsv" would
have published the NEAREST-NEIGHBOUR region figure (37/46, 80%) instead. Two
tables are now written:

  GROUPING_LADDER.tsv       one row per (grouping, estimator): n, correct,
                            accuracy, baseline, kappa.
  GROUPING_PREDICTIONS.tsv  per-genome calls for every (grouping, estimator),
                            with the within-pool nearest-neighbour distance, so
                            a stratification can be computed against the SAME
                            estimator as the headline it accompanies. Pairing
                            NN strata with a modal headline is the specific
                            error this file exists to prevent.
"""
import csv
import os
from collections import Counter, defaultdict

import numpy as np

B = os.path.dirname(os.path.abspath(__file__))
exec(open(f"{B}/score_cgmlst_lichtenegger.py").read().split("def main()")[0])

SEA = {"Thailand", "Viet Nam", "Vietnam", "Cambodia", "Laos", "Malaysia",
       "Singapore", "Indonesia", "Myanmar", "Philippines", "Brunei",
       "Timor-Leste"}
ASIA_REG = {"East Asia & Pacific", "South Asia"}
WEST_REG = {"Latin America & Caribbean", "North America"}

LADDER = f"{B}/GROUPING_LADDER.tsv"
PREDS = f"{B}/GROUPING_PREDICTIONS.tsv"

# Stable machine keys for the display names. generate_numbers.py joins on these,
# so it never depends on a display string that someone might reword.
GKEY = {"country": "country",
        "region (7-way)": "region_7way",
        "SEA vs not": "sea_vs_not",
        "Asia vs not": "asia_vs_not",
        "East vs West hemi": "east_vs_west"}


def kappa(truth, pred):
    labs = sorted(set(truth) | set(pred))
    n = len(truth)
    po = sum(t == p for t, p in zip(truth, pred)) / n
    ct, cp = Counter(truth), Counter(pred)
    pe = sum((ct[l] / n) * (cp[l] / n) for l in labs)
    return (po - pe) / (1 - pe) if pe < 1 else 0.0


def main():
    samples, loci, mat = load_profiles(
        f"{B}/cgmlst_lichtenegger/results/results_alleles.tsv")
    drop = {r["sample_id"] for r in
            csv.DictReader(open(f"{B}/PANEL_DUPLICATES_2026-08-21.tsv"),
                           delimiter="\t") if r["action"] == "drop"}
    keep = [i for i, s in enumerate(samples) if s not in drop]
    samples = [samples[i] for i in keep]
    mat = mat[keep]
    idx = {s: i for i, s in enumerate(samples)}

    # leave-outbreak-out: same explicit register the attribution scorer uses, so
    # the ladder is not inflated by a cluster-derived genome leaking to its
    # same-source siblings (without it the Mississippi cases read region 93%
    # instead of the honest 89%).
    outbreak_groups = load_outbreak_groups()
    group_of = {s: g for g, mem in outbreak_groups.items() for s in mem}

    meta = {r["sample_id"]: r for r in
            csv.DictReader(open(f"{B}/L1v4c_MERGED_METADATA.tsv"), delimiter="\t")}
    man = {r["sample_id"]: r for r in
           csv.DictReader(open(f"{B}/cgmlst_lichtenegger/MANIFEST.tsv"),
                          delimiter="\t")}
    ovr = {r["sample_id"]: r["exposure_country"] for r in
           csv.DictReader(open(f"{B}/EXPOSURE_OVERRIDES.tsv"), delimiter="\t")}
    regof = {r["sample_id"]: r["country"] for r in
             csv.DictReader(open(f"{B}/assign_region.tsv"), delimiter="\t")}
    c2r = {}
    for s, rg in regof.items():
        c = (meta.get(s) or {}).get("country")
        if c and rg:
            c2r.setdefault(c, Counter())[rg] += 1
    C2R = {c: v.most_common(1)[0][0] for c, v in c2r.items()}
    C2R.update({"India": "South Asia", "Thailand": "East Asia & Pacific",
                "Australia": "East Asia & Pacific", "Bangladesh": "South Asia",
                "Mexico": "Latin America & Caribbean", "USA": "North America",
                "Puerto Rico": "Latin America & Caribbean",
                "Trinidad and Tobago": "Latin America & Caribbean"})

    country, truth_c, isval = {}, {}, {}
    for s in samples:
        m = man.get(s, {})
        if m.get("batch") == "v4c_panel":
            c = (meta.get(s) or {}).get("country", "")
            if (meta.get(s) or {}).get("origin_basis") == "travel_reattributed":
                truth_c[s] = meta[s].get("acquired_from") or c
                isval[s] = True
        else:
            c = m.get("country", "")
            if m.get("role") == "ground_truth" and m.get("exposure_country"):
                truth_c[s] = m["exposure_country"]
                c = m["exposure_country"]
                isval[s] = True
        if s in ovr:
            truth_c[s] = ovr[s]
            c = ovr[s]
            isval[s] = True
        country[s] = "" if c in ("Panama and Peru", "Africa") else c

    def region(s):
        return C2R.get(country.get(s, ""), "")

    GROUPINGS = {
        "country": lambda s: country.get(s, ""),
        "region (7-way)": region,
        "SEA vs not": lambda s: ("SEA" if country.get(s) in SEA
                                 else ("non-SEA" if country.get(s) else "")),
        "Asia vs not": lambda s: ("Asia" if region(s) in ASIA_REG
                                  else ("non-Asia" if region(s) else "")),
        "East vs West hemi": lambda s: ("Western" if region(s) in WEST_REG
                                        else ("Eastern" if region(s) else "")),
    }

    val = [s for s in samples if isval.get(s)]
    print(f"validation genomes: {len(val)}\n")
    hdr = (f"{'grouping':<20}{'estimator':<14}{'classes':>8}{'n':>5}"
           f"{'acc':>8}{'baseline':>10}{'kappa':>8}")
    print(hdr); print("-" * len(hdr))

    ladder, preds = [], []
    for gname, gf in GROUPINGS.items():
        pooled = {s: gf(s) for s in samples}
        for est in ("nearest_nb", "modal_k20", "group_test", "hybrid"):
            T, P = [], []
            for s in val:
                t = truth_c.get(s)
                if not t or not pooled.get(s):
                    continue
                held = {x for x in val if truth_c.get(x) == t}
                if s in group_of:
                    held = held | outbreak_groups[group_of[s]]
                cand = [x for x in samples
                        if x not in held and x != s and pooled.get(x)]
                if not cand:
                    continue
                ii = [idx[x] for x in cand]
                d, _ = dist_one_vs_all(mat, idx[s], ii)
                if not (~np.isnan(d)).any():
                    continue
                # distance to the closest usable relative IN THIS POOL. The pool
                # is grouping-specific (a genome with no region label is not a
                # candidate for the region groupings), so this is the honest
                # stratifier for this row and may differ slightly between
                # groupings for the same genome.
                dmin = float(np.nanmin(d))
                if est == "hybrid":
                    # a close relative is the best evidence when one exists;
                    # when none does, the only signal left is whether this
                    # genome sits systematically nearer one group than another
                    if np.nanmin(d) < 0.30:
                        o = np.argsort(np.where(np.isnan(d), np.inf, d))[:20]
                        pred = Counter(pooled[cand[int(x)]]
                                       for x in o).most_common(1)[0][0]
                    else:
                        byg = defaultdict(list)
                        for k, x in enumerate(cand):
                            if not np.isnan(d[k]):
                                byg[pooled[x]].append(d[k])
                        pred = min(byg, key=lambda g: np.median(byg[g]))
                elif est == "group_test":
                    # median distance to each group; pick the closest group.
                    # asks "am I systematically nearer this group", not
                    # "who is my single closest relative"
                    byg = defaultdict(list)
                    for k, x in enumerate(cand):
                        if not np.isnan(d[k]):
                            byg[pooled[x]].append(d[k])
                    pred = min(byg, key=lambda g: np.median(byg[g]))
                elif est == "modal_k20":
                    o = np.argsort(np.where(np.isnan(d), np.inf, d))[:20]
                    pred = Counter(pooled[cand[int(x)]] for x in o).most_common(1)[0][0]
                else:
                    o = int(np.nanargmin(d))
                    pred = pooled[cand[o]]
                T.append(pooled[s]); P.append(pred)
                preds.append(dict(grouping=GKEY[gname], estimator=est,
                                  sample_id=s, truth=pooled[s], predicted=pred,
                                  correct=int(pooled[s] == pred),
                                  nn_distance=f"{dmin:.5f}"))
            if not T:
                continue
            nok = sum(t == p for t, p in zip(T, P))
            acc = nok / len(T)
            bl = Counter(T).most_common(1)[0][1] / len(T)
            k = kappa(T, P)
            ladder.append(dict(grouping=GKEY[gname], grouping_label=gname,
                               estimator=est, classes=len(set(T)), n=len(T),
                               correct=nok, accuracy=f"{acc:.4f}",
                               baseline=f"{bl:.4f}", kappa=f"{k:.4f}"))
            print(f"{gname:<20}{est:<14}{len(set(T)):>8}{len(T):>5}"
                  f"{acc:>7.0%}{bl:>10.0%}{k:>8.3f}")
        print()

    def dump(path, rows, cols):
        with open(path, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                               lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {os.path.basename(path)}  ({len(rows)} rows)")

    dump(LADDER, ladder, ["grouping", "grouping_label", "estimator", "classes",
                          "n", "correct", "accuracy", "baseline", "kappa"])
    dump(PREDS, preds, ["grouping", "estimator", "sample_id", "truth",
                        "predicted", "correct", "nn_distance"])


if __name__ == "__main__":
    main()
