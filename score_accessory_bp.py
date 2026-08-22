#!/usr/bin/env python3
"""
Accessory-genome attribution, scored under the same regime as the core genome.

The question (HANDOFF 2026-08-21 evening §1): the core genome resolves only deep
splits, so it separates Asia from non-Asia perfectly and countries not at all.
Accessory content -- phage, plasmids, ICEs -- is acquired locally and circulates
in a place, so it may carry the shallow signal vertical descent does not. The
Salmonella precedent reached country macro-F1 0.661 on accessory unitigs.

Distance is PopPUNK's accessory distance (a), the intercept of the regression of
log(Jaccard) on k over k = 15..31; core (pi) is the slope. Both come from the
same sketch database, so `--distance core_pp` is a free internal control: same
genomes, same sketches, same estimators, only the axis differs.

`--distance cgmlst` reproduces score_cgmlst_lichtenegger.py through this script's
own label-building code. It exists to prove the two scorers are like-for-like:
if this mode does not reproduce CGMLST_LICHT_ATTRIBUTION.tsv row for row, the
comparison between core and accessory is not trustworthy and the accessory
numbers must not be reported. Run --validate before believing anything here.

Everything except the distance is held fixed: leave-group-out on exposure
country, the same five estimators, the same exposure overrides, the same
duplicate drops, the same region map.
"""
import argparse
import csv
import os
import pickle
import sys
from collections import Counter, defaultdict

import numpy as np

B = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, B)
import score_cgmlst_lichtenegger as tmpl  # noqa: E402  (load_profiles, dist_one_vs_all)

ESTIMATORS = ["nearest_neighbour", "modal_k5", "modal_k10", "modal_k20",
              "enrichment_k20"]
NOTC = {"Africa", "Panama and Peru", ""}


# ---------------------------------------------------------------- distances

def load_pp_dists(prefix):
    """PopPUNK self-mode distances -> (names, core, accessory).

    Self-mode row order is `for i in range(n): for j in range(i+1, n)`, i.e. the
    standard condensed upper triangle (poppunk_extract_distances.listDistInts).
    """
    with open(f"{prefix}.dists.pkl", "rb") as fh:
        rlist, qlist, self_mode = pickle.load(fh)
    if not self_mode:
        raise SystemExit(f"{prefix}: not a self-comparison database")
    if rlist != qlist:
        raise SystemExit(f"{prefix}: ref and query name lists differ")
    d = np.load(f"{prefix}.dists.npy")
    n = len(rlist)
    if d.shape[0] != n * (n - 1) // 2:
        raise SystemExit(f"{prefix}: {d.shape[0]} rows for {n} genomes, expected "
                         f"{n*(n-1)//2}")
    return rlist, d[:, 0].astype(np.float64), d[:, 1].astype(np.float64)


class CondensedDist:
    """One-vs-all lookup into a condensed upper-triangle distance vector."""

    def __init__(self, vec, n):
        self.v = vec
        self.n = n
        # start offset of row i in the condensed vector
        i = np.arange(n)
        self.off = (i * n - i * (i + 1) // 2).astype(np.int64)

    def row(self, i):
        """Distances from i to every genome, self set to nan."""
        n = self.n
        out = np.empty(n, dtype=np.float64)
        j = np.arange(i + 1, n)
        if j.size:
            out[i + 1:] = self.v[self.off[i] + (j - i - 1)]
        k = np.arange(0, i)
        if k.size:
            out[:i] = self.v[self.off[k] + (i - k - 1)]
        out[i] = np.nan
        return out


# ---------------------------------------------------------------- labels
# Copied from score_cgmlst_lichtenegger.py so the two scorers cannot drift
# apart silently; --validate is what proves they have not.

def build_labels(samples, manifest_path):
    ovr = {r["sample_id"]: r["exposure_country"] for r in
           csv.DictReader(open(f"{B}/EXPOSURE_OVERRIDES.tsv"), delimiter="\t")}
    man = {r["sample_id"]: r for r in
           csv.DictReader(open(manifest_path), delimiter="\t")}
    meta = {r["sample_id"]: r for r in
            csv.DictReader(open(f"{B}/L1v4c_MERGED_METADATA.tsv"), delimiter="\t")}

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
        if c in ("Panama and Peru", "Africa"):
            c = ""
        if s in ovr:
            truth_c[s] = ovr[s]
            c = ovr[s]
            is_val[s] = True
        country[s] = c
        region[s] = country2region.get(c, "")
    return country, region, truth_c, is_val


def load_drops():
    return {r["sample_id"] for r in
            csv.DictReader(open(f"{B}/PANEL_DUPLICATES_2026-08-21.tsv"),
                           delimiter="\t") if r["action"] == "drop"}


# ---------------------------------------------------------------- scoring

def score(samples, dist_row, labels, truth_c, val, panel_counts_of):
    """Leave-group-out scoring. dist_row(i) -> distances to all samples.

    Returns per-genome rows for every scale in `labels`.
    """
    idx_of = {s: i for i, s in enumerate(samples)}
    # leave-outbreak-out: same explicit same-source register the cgMLST scorer
    # uses, so the two stay equivalent (--validate). No-op with an empty register.
    outbreak_groups = tmpl.load_outbreak_groups()
    group_of = {s: g for g, mem in outbreak_groups.items() for s in mem}
    out = []
    for scale, lab in labels.items():
        panel_n = panel_counts_of[scale]
        tot_n = sum(panel_n.values())
        for s in val:
            t = truth_c[s]
            if t in NOTC or not lab.get(s):
                continue
            held = {x for x in val if truth_c[x] == t}
            if s in group_of:
                held = held | outbreak_groups[group_of[s]]
            pool = [idx_of[x] for x in samples
                    if x not in held and lab.get(x) and x != s]
            if not pool:
                continue
            d = dist_row(idx_of[s])[pool]
            if not np.isfinite(d).any():
                continue
            order = np.argsort(np.where(np.isnan(d), np.inf, d))
            labs = [lab[samples[pool[int(x)]]] for x in order]
            preds = {"nearest_neighbour": labs[0]}
            for K in (5, 10, 20):
                preds[f"modal_k{K}"] = Counter(labs[:K]).most_common(1)[0][0]
            k20 = Counter(labs[:20])
            preds["enrichment_k20"] = max(
                k20, key=lambda L: (k20[L] / 20) / max(panel_n.get(L, 1) / tot_n, 1e-9))
            j = int(order[0])
            out.append({"sample_id": s, "scale": scale, "exposure_country": t,
                        "truth": lab[s],
                        "nn_distance": float(np.nanmin(d)),
                        "nn_sample": samples[pool[j]],
                        **{f"pred_{k}": v for k, v in preds.items()},
                        **{f"ok_{k}": int(v == lab[s]) for k, v in preds.items()}})
    return out


def report(rows, labels, val, truth_c, samples, estimator, title):
    print(f"\n================ {title} ================")
    for scale in labels:
        rs = [r for r in rows if r["scale"] == scale]
        if not rs:
            continue
        lab = labels[scale]
        base = Counter(lab[s] for s in val
                       if truth_c.get(s) not in NOTC and lab.get(s))
        bl = base.most_common(1)[0][1] if base else 0
        hit = sum(r[f"ok_{estimator}"] for r in rs)
        print(f"\n=== {scale} ===   ({estimator})")
        print(f"  {hit}/{len(rs)} correct ({100*hit/len(rs):.0f}%)   "
              f"majority baseline {bl}/{sum(base.values())} "
              f"({100*bl/max(sum(base.values()),1):.0f}%)")
        print("  all estimators:")
        for e in ESTIMATORS:
            h = sum(r[f"ok_{e}"] for r in rs)
            print(f"     {e:<20}{h}/{len(rs)}  ({100*h/len(rs):.0f}%)")
        print("  stratified by nearest-neighbour distance:")
        for lo, hi, nm in ((0, .05, "d < 0.05  (close relative)"),
                           (.05, .30, "0.05-0.30 (distant)"),
                           (.30, 9e9, "d >= 0.30 (no real relative)")):
            st_ = [r for r in rs if lo <= r["nn_distance"] < hi]
            if st_:
                h = sum(r[f"ok_{estimator}"] for r in st_)
                print(f"     {nm:<34}{h}/{len(st_)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--distance", default="accessory",
                    choices=["accessory", "core_pp", "cgmlst"])
    ap.add_argument("--ppdb", default=f"{B}/accessory_bp/ppdb3033/ppdb3033")
    ap.add_argument("--profiles",
                    default=f"{B}/cgmlst_lichtenegger/results/results_alleles.tsv")
    ap.add_argument("--manifest",
                    default=f"{B}/cgmlst_lichtenegger/MANIFEST.tsv")
    ap.add_argument("--estimator", default="nearest_neighbour")
    ap.add_argument("--out-prefix", default=None)
    ap.add_argument("--validate", action="store_true",
                    help="check --distance cgmlst against CGMLST_LICHT_ATTRIBUTION.tsv")
    a = ap.parse_args()

    drop = load_drops()

    if a.distance == "cgmlst":
        samples, loci, mat = tmpl.load_profiles(a.profiles)
        keep = [i for i, s in enumerate(samples) if s not in drop]
        samples = [samples[i] for i in keep]
        mat = mat[keep]
        print(f"cgmlst: {len(samples)} genomes x {len(loci)} loci "
              f"({len(drop)} duplicates dropped)")

        def dist_row(i, _mat=mat):
            allidx = np.arange(_mat.shape[0])
            d, _ = tmpl.dist_one_vs_all(_mat, i, allidx)
            d[i] = np.nan
            return d
    else:
        names, core, acc = load_pp_dists(a.ppdb)
        vec = acc if a.distance == "accessory" else core
        keep = np.array([i for i, s in enumerate(names) if s not in drop])
        cd = CondensedDist(vec, len(names))
        cache = {}

        def dist_row(i, _cd=cd, _keep=keep, _cache=cache):
            r = _cache.get(i)
            if r is None:
                r = _cd.row(int(_keep[i]))[_keep]
                _cache[i] = r
            return r

        samples = [names[i] for i in keep]
        print(f"poppunk {a.distance}: {len(names)} genomes -> {len(samples)} "
              f"after dropping {len(names)-len(samples)} duplicates")
        print(f"  {a.distance} distance: min {np.nanmin(vec):.5f}  "
              f"median {np.nanmedian(vec):.5f}  max {np.nanmax(vec):.5f}")

    country, region, truth_c, is_val = build_labels(samples, a.manifest)
    labels = {"country": country, "region": region}
    val = [s for s in samples if is_val.get(s)]
    print(f"validation genomes present: {len(val)}")
    print(f"  by exposure country: "
          f"{dict(Counter(truth_c[s] for s in val).most_common())}")

    panel_counts_of = {sc: Counter(lab[x] for x in samples if lab.get(x))
                       for sc, lab in labels.items()}
    rows = score(samples, dist_row, labels, truth_c, val, panel_counts_of)
    report(rows, labels, val, truth_c, samples, a.estimator,
           f"{a.distance} distance")

    prefix = a.out_prefix or f"{B}/accessory_bp/ATTR_{a.distance.upper()}"
    fields = ["sample_id", "scale", "exposure_country", "truth", "nn_distance",
              "nn_sample"] + [f"pred_{e}" for e in ESTIMATORS] + \
             [f"ok_{e}" for e in ESTIMATORS]
    with open(f"{prefix}.tsv", "w", newline="") as fh:
        w = csv.DictWriter(fh, delimiter="\t", lineterminator="\n",
                           fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.5f}" if isinstance(v, float) else v)
                        for k, v in r.items()})
    print(f"\nwrote {prefix}.tsv  ({len(rows)} rows)")

    if a.validate:
        ref = f"{B}/CGMLST_LICHT_ATTRIBUTION.tsv"
        old = {(r["sample_id"], r["scale"]): r
               for r in csv.DictReader(open(ref), delimiter="\t")}
        new = {(r["sample_id"], r["scale"]): r for r in rows}
        # the reference file was written with estimator=modal_k10 as `predicted`
        miss = set(old) - set(new)
        extra = set(new) - set(old)
        bad = [k for k in set(old) & set(new)
               if old[k]["truth"] != new[k]["truth"]
               or old[k]["nn_sample"] != new[k]["nn_sample"]]
        print(f"\n=== validation against {os.path.basename(ref)} ===")
        print(f"  rows only in reference: {len(miss)}")
        print(f"  rows only here:         {len(extra)}")
        print(f"  truth/nn_sample mismatches: {len(bad)}")
        for k in list(miss)[:5] + list(extra)[:5] + bad[:5]:
            print(f"    {k}")
        ok = not miss and not extra and not bad
        print(f"  RESULT: {'PASS - scorers are like-for-like' if ok else 'FAIL'}")
        if not ok:
            sys.exit(1)


if __name__ == "__main__":
    main()
