#!/usr/bin/env python3
"""
Classify ENA records by how much their ORIGIN metadata can be trusted.

The panel's value for attribution depends entirely on whether a genome's
recorded country is where the organism came FROM, or merely where it was
isolated. Those are different things and ENA does not distinguish them: the
`country` field holds "USA: NJ ex Trinidad and Tobago" for a travel case and
plain "USA: FL" for a domestic one, in the same column.

Four tiers, in decreasing strength as origin evidence:

  A_exposure_stated   ENA country carries "X ex Y" -- Y is the exposure country,
                      stated by the submitter. Directly usable as ground truth.
  B_external_evidence origin established by published investigation rather than
                      by the record. Requires an EXPOSURE_OVERRIDES.tsv entry
                      with a citation. Strongest evidence of all where it
                      exists, because it does not depend on the depositor.
  C_deposit_only      a country is recorded but nothing distinguishes local
                      acquisition from unrecorded travel. Fine as a PANEL
                      member; must NOT be used as origin ground truth.
  D_unusable          no country, or a country that is not a place ("missing"),
                      or wrong species.

The distinction that matters: **C is not a weaker version of A, it is a
different quantity.** A US clinical isolate with no travel field could be
domestic or an unrecorded import. Counting it as "USA origin" would inject
exactly the error we are trying to measure.

Usage:  classify_ena_origin_bp.py --in ENA_FETCH_TARGETS.tsv --out CLASSIFIED.tsv
"""
import argparse
import collections
import csv
import os
import re
import sys

B = os.path.dirname(os.path.abspath(__file__))
TAXID_BP = "28450"
EX = re.compile(r"\bex\s+(.+)$", re.I)
NOT_A_PLACE = {"", "missing", "not applicable", "not collected", "unknown",
               "na", "n/a", "none", "null", "-"}


def classify(row, overrides):
    """-> (tier, exposure_country, note)"""
    run = row.get("run_accession", "")
    tax = row.get("tax_id", "")
    sci = row.get("scientific_name", "")
    country = (row.get("country") or "").strip()

    if tax and tax != TAXID_BP:
        return "D_unusable", "", f"wrong species: {sci} (taxid {tax})"

    if run in overrides:
        o = overrides[run]
        return "B_external_evidence", o["exposure_country"], o["evidence"]

    if country.lower() in NOT_A_PLACE:
        return "D_unusable", "", "no country recorded"

    # "USA: NJ ex Trinidad and Tobago" -> exposure is what follows 'ex'
    m = EX.search(country)
    if m:
        exp = m.group(1).strip()
        if exp.lower() in NOT_A_PLACE:
            return "C_deposit_only", "", f"'ex' present but unparseable: {country}"
        return "A_exposure_stated", exp, f"ENA country: {country}"

    return "C_deposit_only", "", f"deposit location only: {country}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default=f"{B}/ENA_FETCH_TARGETS.tsv")
    ap.add_argument("--tax", default="", help="optional TSV with run_accession,tax_id,scientific_name")
    ap.add_argument("--out", default=f"{B}/ENA_TARGETS_CLASSIFIED.tsv")
    a = ap.parse_args()

    rows = list(csv.DictReader(open(a.inp), delimiter="\t"))
    if a.tax and os.path.isfile(a.tax):
        tx = {r["run_accession"]: r for r in csv.DictReader(open(a.tax), delimiter="\t")}
        for r in rows:
            t = tx.get(r["run_accession"], {})
            r["tax_id"] = t.get("tax_id", "")
            r["scientific_name"] = t.get("scientific_name", "")

    overrides = {}
    p = f"{B}/EXPOSURE_OVERRIDES.tsv"
    if os.path.isfile(p):
        overrides = {r["sample_id"]: r for r in csv.DictReader(open(p), delimiter="\t")}

    for r in rows:
        tier, exp, note = classify(r, overrides)
        r["origin_tier"] = tier
        r["exposure_country"] = exp
        r["origin_note"] = note

    cols = [c for c in rows[0] if c not in ("origin_tier", "exposure_country", "origin_note")]
    cols += ["origin_tier", "exposure_country", "origin_note"]
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t", lineterminator="\n",
                           extrasaction="ignore")
        w.writeheader(); w.writerows(rows)

    c = collections.Counter(r["origin_tier"] for r in rows)
    print(f"{len(rows)} records classified -> {a.out}\n")
    for t in ("A_exposure_stated", "B_external_evidence", "C_deposit_only", "D_unusable"):
        print(f"  {t:<22} {c.get(t,0)}")
    print("\n--- A: exposure country stated by the submitter ---")
    for r in rows:
        if r["origin_tier"] == "A_exposure_stated":
            print(f"  {r['run_accession']:<13} -> {r['exposure_country']:<24} ({r.get('collection_date','')})")
    print("\n--- D: excluded ---")
    for r in rows:
        if r["origin_tier"] == "D_unusable":
            print(f"  {r['run_accession']:<13} {r['origin_note']}")


if __name__ == "__main__":
    main()
