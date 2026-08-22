#!/usr/bin/env python3
"""
Downsampling control: is region attribution an artifact of panel imbalance?

The panel is 60% Thailand (1,753 of 2,955), all SE Asia. The attractor concern
(MANUSCRIPT_OUTLINE W2, HANDOFF 2026-08-21 §3.3): region scores 93% partly
because a genome with no close relative snaps to the dominant cluster, and coarse
7-way region labels make that "correct" often enough to look like a capability.

THE TEST. Cap each country's reference representation and re-score. If region
accuracy is real -- genomes actually resemble their regional cohort -- shrinking
Thailand 70x will not hurt it. If it is the attractor, accuracy falls toward the
balanced baseline and kappa collapses toward 0.

WHY THIS AND NOT PHASE 1. It answers the exact question Phase 1 was meant to
answer -- does a balanced reference panel change attribution -- at zero download
and zero assembly cost, holding the data type fixed. Phase 1 could only add
references where they are obtainable (SE Asia), which is where the panel is
already dense; this removes the imbalance directly.

DESIGN
  - cgMLST Lichtenegger distance (partition-independent, so no dependence on the
    frozen partition; this is why the control is cheap).
  - leave-group-out on exposure country, identical to the scored attribution.
  - cap the NON-validation reference pool per country; validation genomes always
    stay in (they are references for each other and are held out per-group).
  - sweep caps, 20 seeded replicate draws each; report mean +/- sd.
  - PRIMARY METRIC IS KAPPA. Raw accuracy is reported beside it, but kappa is
    chance-corrected and therefore the honest metric when the whole question is
    whether accuracy is a majority-class effect.
  - NN and modal_k20 separately: modal_k is the estimator most exposed to pool
    composition, so the attractor, if real, should crack there first.
"""
import csv
import os
import random
import statistics as st
from collections import Counter, defaultdict

import numpy as np

B = os.path.dirname(os.path.abspath(__file__))
import score_accessory_bp as S
import score_cgmlst_lichtenegger as tmpl

CAPS = [None, 500, 200, 100, 50, 25]
REPS = 20
SEED = 20260822
PROFILES = f"{B}/cgmlst_lichtenegger/results/results_alleles.tsv"
MANIFEST = f"{B}/cgmlst_lichtenegger/MANIFEST.tsv"


def kappa(pairs):
    """Cohen's kappa from (truth, pred) pairs."""
    n = len(pairs)
    if not n:
        return float("nan")
    po = sum(t == p for t, p in pairs) / n
    tc = Counter(t for t, _ in pairs)
    pc = Counter(p for _, p in pairs)
    pe = sum(tc[k] * pc.get(k, 0) for k in tc) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def main():
    drop = S.load_drops()
    samples, loci, mat = tmpl.load_profiles(PROFILES)
    keep = [i for i, s in enumerate(samples) if s not in drop]
    samples = [samples[i] for i in keep]
    mat = mat[keep]
    idx_of = {s: i for i, s in enumerate(samples)}
    country, region, truth_c, is_val = S.build_labels(samples, MANIFEST)
    val = [s for s in samples if is_val.get(s)]
    print(f"cgmlst {len(samples)} genomes; {len(val)} validation genomes")

    # per-country membership of the NON-validation reference pool (region scale
    # is what we score, but the imbalance is a country/BioProject fact, so we cap
    # by country to shrink it without collapsing within-region diversity)
    valset = set(val)
    ref_by_country = defaultdict(list)
    for s in samples:
        if s not in valset and country.get(s):
            ref_by_country[country[s]].append(s)
    th = len(ref_by_country.get("Thailand", []))
    print(f"Thailand references: {th}  ({100*th/len(samples):.0f}% of the panel)\n")

    # cache each validation genome's distance to ALL samples once; only the pool
    # selection changes across caps, never these rows
    dist_cache = {}
    for s in val:
        d, _ = tmpl.dist_one_vs_all(mat, idx_of[s], np.arange(len(samples)))
        d[idx_of[s]] = np.nan
        dist_cache[s] = d

    def score_pool(keep_set):
        """One leave-group-out pass restricted to keep_set. Returns
        {scale: {est: [(truth,pred), ...]}}."""
        out = {sc: {"nearest_neighbour": [], "modal_k20": []}
               for sc in ("country", "region")}
        for scale, lab in (("country", country), ("region", region)):
            for s in val:
                t = lab.get(s)
                if not t or truth_c[s] in S.NOTC:
                    continue
                held = {x for x in val if truth_c[x] == truth_c[s]}
                pool = [x for x in keep_set
                        if x != s and x not in held and lab.get(x)]
                if not pool:
                    continue
                d = dist_cache[s]
                pi = [idx_of[x] for x in pool]
                dd = d[pi]
                fin = np.isfinite(dd)
                if not fin.any():
                    continue
                order = np.argsort(np.where(np.isnan(dd), np.inf, dd))
                labs = [lab[pool[int(x)]] for x in order]
                out[scale]["nearest_neighbour"].append((t, labs[0]))
                out[scale]["modal_k20"].append(
                    (t, Counter(labs[:20]).most_common(1)[0][0]))
        return out

    # fixed majority baseline: property of the validation set, not the pool
    for scale, lab in (("country", country), ("region", region)):
        base = Counter(lab[s] for s in val
                       if truth_c.get(s) not in S.NOTC and lab.get(s))
        bl = base.most_common(1)[0][1]
        n = sum(base.values())
        print(f"  {scale:<8} majority baseline {bl}/{n} ({100*bl/n:.0f}%)")
    print()

    rng = random.Random(SEED)
    print(f"{'cap/country':<12}{'Thai_n':>7}{'pool':>7}   "
          f"{'region NN':>16}{'region k20':>18}{'country NN':>16}")
    print(f"{'':12}{'':7}{'':7}   {'acc / kappa':>16}{'acc / kappa':>18}"
          f"{'acc / kappa':>16}")
    for cap in CAPS:
        agg = defaultdict(lambda: defaultdict(list))
        pool_sizes, thai_sizes = [], []
        nreps = 1 if cap is None else REPS
        for r in range(nreps):
            keep_set = list(valset)
            for c, refs in ref_by_country.items():
                if cap is None or len(refs) <= cap:
                    keep_set += refs
                else:
                    keep_set += rng.sample(refs, cap)
            keep_set = set(keep_set)
            pool_sizes.append(len(keep_set))
            thai_sizes.append(min(cap, th) if cap else th)
            res = score_pool(keep_set)
            for sc in ("country", "region"):
                for est in ("nearest_neighbour", "modal_k20"):
                    pairs = res[sc][est]
                    if pairs:
                        agg[(sc, est)]["acc"].append(
                            sum(t == p for t, p in pairs) / len(pairs))
                        agg[(sc, est)]["kap"].append(kappa(pairs))

        def cell(sc, est):
            a = agg[(sc, est)]["acc"]
            k = agg[(sc, est)]["kap"]
            if not a:
                return " " * 16
            if len(a) == 1:
                return f"{100*a[0]:3.0f}% /{k[0]:+.2f}    "
            return (f"{100*st.mean(a):3.0f}%/{k and st.mean(k):+.2f}"
                    f"±{st.pstdev(k):.2f}")

        capn = "full" if cap is None else str(cap)
        print(f"{capn:<12}{int(st.mean(thai_sizes)):>7}"
              f"{int(st.mean(pool_sizes)):>7}   "
              f"{cell('region','nearest_neighbour'):>16}"
              f"{cell('region','modal_k20'):>18}"
              f"{cell('country','nearest_neighbour'):>16}")

    print("\nread: if region kappa is flat as Thai_n shrinks ~70x, the signal is")
    print("real; if it falls toward 0, region accuracy was the panel imbalance.")

    # ---- the stronger test: balance at the REGION level directly -------------
    # Per-country capping leaves East Asia & Pacific dominant (many countries),
    # so cap each REGION's reference pool. At cap 30 the 2,692-genome EAP region
    # drops to 30 -- from 89% of references to ~15% -- and the panel is region-
    # balanced. If region kappa holds here, the attractor is dead outright.
    ref_by_region = defaultdict(list)
    for s in samples:
        if s not in valset and region.get(s):
            ref_by_region[region[s]].append(s)
    eap = len(ref_by_region.get("East Asia & Pacific", []))
    print(f"\n--- REGION-level equalization (East Asia & Pacific = {eap} refs) ---")
    print(f"{'cap/region':<12}{'EAP_n':>7}{'pool':>7}   "
          f"{'region NN':>18}{'region k20':>18}")
    for cap in (200, 100, 50, 30):
        aggr = defaultdict(list)
        pool_sizes, eap_sizes = [], []
        for r in range(REPS):
            keep_set = list(valset)
            for rg, refs in ref_by_region.items():
                keep_set += refs if len(refs) <= cap else rng.sample(refs, cap)
            keep_set = set(keep_set)
            pool_sizes.append(len(keep_set))
            eap_sizes.append(min(cap, eap))
            res = score_pool(keep_set)
            for est in ("nearest_neighbour", "modal_k20"):
                pairs = res["region"][est]
                if pairs:
                    aggr[(est, "acc")].append(sum(t == p for t, p in pairs) / len(pairs))
                    aggr[(est, "kap")].append(kappa(pairs))

        def rcell(est):
            a = aggr[(est, "acc")]; k = aggr[(est, "kap")]
            return (f"{100*st.mean(a):3.0f}%/{st.mean(k):+.2f}±{st.pstdev(k):.2f}"
                    if a else " " * 18)
        print(f"{cap:<12}{int(st.mean(eap_sizes)):>7}{int(st.mean(pool_sizes)):>7}   "
              f"{rcell('nearest_neighbour'):>18}{rcell('modal_k20'):>18}")
    print("\nEAP from 2,692 -> 30 is a 90x cut, 89% -> ~15% of the pool. Flat region")
    print("kappa through that is the attractor hypothesis refuted outright.")


if __name__ == "__main__":
    main()
