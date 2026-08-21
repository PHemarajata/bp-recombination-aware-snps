#!/usr/bin/env python3
"""
Score origin attribution against the genomes whose exposure country is known.

The applied goal is attributing origin for a US case with no travel history. The
panel contains 26 genomes where the exposure country IS known, and nothing has
ever been scored against them. This does that.

Selecting the validation set -- both obvious selectors are wrong
----------------------------------------------------------------
The set is `origin_basis == 'travel_reattributed'`, 26 genomes in two families:

  16 CDC genomes (PRJNA908850) carrying `validation_label`. Their `bioproject`
     column is BLANK, so they cannot be selected by BioProject.
  10 older genomes (PRJNA352974) whose exposure country was parsed from the
     assembly name (`..._USA_California_ex_Mexico`). Their `validation_label` is
     BLANK, so selecting on that column silently drops them.

Two holdout regimes, because they answer different questions
------------------------------------------------------------
  leave-one-out    drop only the genome. "Given that reference genomes for this
                   country exist, can we attribute?" Circular where several
                   validation genomes share a unit -- 9 of strain_1_L1_12's
                   members are Philippine validation genomes, so 8 remain.
  leave-group-out  drop every validation genome sharing the exposure country.
                   "Can we attribute to a country with no reference?" For the
                   Philippines this is unattributable by construction: those 12
                   genomes are the only Philippine genomes in the panel.

Reporting accuracy without a baseline would be meaningless
----------------------------------------------------------
East Asia & Pacific is 91.8% of the panel, so a classifier that always answers
"East Asia & Pacific" scores ~92% at region scale while knowing nothing. Every
accuracy below is reported beside the majority-class baseline on the same
holdout, and it is the margin over that baseline that carries information.

Usage
-----
    attribution_score_bp.py [--out FILE] [--summary FILE]
"""
import argparse
import collections
import csv
import glob
import os
import sys

B = os.path.dirname(os.path.abspath(__file__))
META = f"{B}/L1v4c_MERGED_METADATA.tsv"
ASSIGN = f"{B}/wfsnps-v4c-results/partition/curated_L1v4c_assignments_all.tsv"
DIST = f"{B}/DISTANCES_v4c"
SCALES = {"country": f"{B}/assign_country_norm.tsv",
          "subnational": f"{B}/assign_subnational.tsv",
          "region": f"{B}/assign_region.tsv"}
MISSING = {"", "unknown", "na", "n/a", "none", "null", "missing", "-", "."}


def load(path, key=None):
    rows = list(csv.DictReader(open(path), delimiter="\t"))
    return {r[key]: r for r in rows} if key else rows


def clean(v):
    v = (v or "").strip()
    return "" if v.lower() in MISSING else v


def load_scale(path):
    return {r["sample_id"]: clean(r["country"]) for r in load(path)}


def load_distances(unit):
    """Recombination-filtered pairwise SNP distances for a unit, replicon 1 by
    preference. Filtered rather than raw: nearest-neighbour on raw distance would
    be steered by imported sequence, which is the thing we corrected for."""
    for rep in ("1", "2"):
        hits = glob.glob(f"{DIST}/{unit}__*_{rep}.filtered_pertaxon.tsv")
        if hits:
            rows = list(csv.reader(open(hits[0]), delimiter="\t"))
            taxa = rows[0][1:]
            return {t: {taxa[j]: int(v) for j, v in enumerate(r[1:])}
                    for t, r in zip(taxa, rows[1:])}
    return {}


def predict(pool_labels, panel_counts, panel_n, nn_order):
    """-> {estimator: predicted label or ''} given the surviving pool."""
    out = {"modal": "", "nearest_neighbour": "", "enrichment": ""}
    if not pool_labels:
        return out
    c = collections.Counter(pool_labels.values())
    if c:
        out["modal"] = c.most_common(1)[0][0]
        # enrichment: over-representation vs the panel, which stops a label from
        # winning purely by being 66% of the collection
        best, score = "", -1.0
        for lab, k in c.items():
            base = panel_counts.get(lab, 0) / panel_n if panel_n else 0
            e = (k / len(pool_labels)) / base if base > 0 else 0.0
            if e > score:
                best, score = lab, e
        out["enrichment"] = best
    for t in nn_order:                      # already sorted by ascending distance
        if t in pool_labels:
            out["nearest_neighbour"] = pool_labels[t]
            break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=f"{B}/ATTRIBUTION_SCORES.tsv")
    ap.add_argument("--summary", default=f"{B}/ATTRIBUTION_SUMMARY.tsv")
    a = ap.parse_args()

    meta = load(META, key="sample_id")
    assign = load(ASSIGN, key="sample_id")
    scales = {s: load_scale(p) for s, p in SCALES.items()}

    val = [s for s, r in meta.items() if r.get("origin_basis") == "travel_reattributed"]
    analysed = {s for s, r in assign.items() if r.get("role") == "analysis"}
    members = collections.defaultdict(list)
    for s, r in assign.items():
        if r.get("role") == "analysis":
            members[r["cluster_id"]].append(s)

    print(f"validation genomes: {len(val)}  "
          f"(in analysed set: {sum(1 for s in val if s in analysed)})")

    dist_cache, rows = {}, []
    for g in sorted(val):
        unit = assign.get(g, {}).get("cluster_id", "")
        role = assign.get(g, {}).get("role", "")
        truth_country = clean(meta[g].get("acquired_from")) or clean(meta[g].get("country"))
        same_country = {x for x in val
                        if (clean(meta[x].get("acquired_from"))
                            or clean(meta[x].get("country"))) == truth_country}

        if unit not in dist_cache:
            dist_cache[unit] = load_distances(unit)
        dmat = dist_cache[unit].get(g, {})
        nn_order = sorted((t for t in dmat if t != g), key=lambda t: dmat[t])

        for scale, lab in scales.items():
            truth = lab.get(g, "")
            for regime, held in (("leave_one_out", {g}),
                                 ("leave_group_out", same_country)):
                base = {"sample_id": g, "unit": unit, "role": role,
                        "exposure_country": truth_country, "scale": scale,
                        "regime": regime, "truth": truth,
                        "unit_n": len(members.get(unit, []))}
                if role != "analysis" or len(members.get(unit, [])) < 2:
                    # Not a failure of the method: these genomes fall in n=1
                    # assign_only units, below the analysis floor. Four of the
                    # six are the sole panel representative of their exposure
                    # country -- the countries most in need of attribution are
                    # the ones least likely to land in an analysable unit.
                    rows.append({**base, "modal": "", "nearest_neighbour": "",
                                 "enrichment": "", "pool_n": 0,
                                 "same_truth_refs_in_pool": 0,
                                 "note": "unattributable: no unit with >=2 members"})
                    continue
                pool = {t: lab[t] for t in members[unit]
                        if t not in held and lab.get(t)}
                panel = collections.Counter(
                    lab[t] for t in analysed if t not in held and lab.get(t))
                p = predict(pool, panel, sum(panel.values()), nn_order)
                note = "" if pool else "unattributable: no reference left in unit"
                if not truth:
                    note = note or "not scorable: no truth label at this scale"
                # Makes the circularity auditable per row rather than something
                # the reader has to reconstruct: every leave-one-out hit at
                # country scale comes from a surviving same-country genome.
                same_ref = sum(1 for t, v in pool.items() if v == truth) if truth else 0
                rows.append({**base, **p, "note": note,
                             "pool_n": len(pool),
                             "same_truth_refs_in_pool": same_ref,
                             "majority_baseline": (panel.most_common(1)[0][0]
                                                   if panel else "")})
        # end scales
    cols = ["sample_id", "unit", "unit_n", "role", "exposure_country", "scale",
            "regime", "truth", "pool_n", "same_truth_refs_in_pool", "modal",
            "nearest_neighbour", "enrichment", "majority_baseline", "note"]
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                           lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})

    # ---- summary: accuracy per estimator, beside the no-information baseline --
    out = []
    for scale in SCALES:
        for regime in ("leave_one_out", "leave_group_out"):
            g = [r for r in rows if r["scale"] == scale and r["regime"] == regime]
            scorable = [r for r in g if r["truth"] and not r["note"]]
            rec = {"scale": scale, "regime": regime, "n_total": len(g),
                   "n_scorable": len(scorable),
                   "n_no_unit": sum(1 for r in g if "no unit" in r["note"]),
                   "n_no_truth_label": sum(1 for r in g if not r["truth"]),
                   # how many scorable rows still had a same-country reference
                   # surviving the holdout: the circularity, counted
                   "n_with_same_truth_ref": sum(
                       1 for r in scorable if int(r["same_truth_refs_in_pool"]) > 0)}
            for est in ("modal", "nearest_neighbour", "enrichment"):
                k = sum(1 for r in scorable if r[est] and r[est] == r["truth"])
                rec[est] = (f"{k}/{len(scorable)} ({100*k/len(scorable):.0f}%)"
                            if scorable else "-")
            k = sum(1 for r in scorable if r["majority_baseline"] == r["truth"])
            rec["baseline_majority"] = (f"{k}/{len(scorable)} ({100*k/len(scorable):.0f}%)"
                                        if scorable else "-")
            out.append(rec)
    with open(a.summary, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]), delimiter="\t",
                           lineterminator="\n")
        w.writeheader(); w.writerows(out)

    print(f"\n{'scale':<13}{'regime':<17}{'scor':<6}{'same-ref':<10}"
          f"{'modal':<13}{'NN':<13}{'enrich':<13}{'baseline':<13}")
    for r in out:
        print(f"{r['scale']:<13}{r['regime']:<17}{r['n_scorable']:<6}"
              f"{r['n_with_same_truth_ref']:<10}{r['modal']:<13}"
              f"{r['nearest_neighbour']:<13}{r['enrichment']:<13}"
              f"{r['baseline_majority']:<13}")
    print("\n'same-ref' = scorable genomes that still had a same-country reference\n"
          "in the pool. At country scale under leave-one-out every hit comes from\n"
          "one of these; leave-group-out removes them and accuracy goes to zero.")
    print(f"\nwrote {a.out}\nwrote {a.summary}")


if __name__ == "__main__":
    main()
