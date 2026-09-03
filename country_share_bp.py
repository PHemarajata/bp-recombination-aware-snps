#!/usr/bin/env python3
"""
country_share_bp.py

Report the dominant-country share of a genome set, with its denominator named.

WHY THIS EXISTS. Four different Thailand shares are in circulation across this
project's documents, and each one is correct for a denominator that is never
stated beside it:

    59.5%   NUMBERS.tsv panel.top_country.Thailand, 1,753 of 2,946
            (2,946 is panel.region_labelled, NOT panel.corrected_v4d at 2,959,
             so even this key's own percentage uses a different denominator
             from the one its name implies)
    66.4%   phylogeography_association_bp.py docstring, over the 2,352-genome
            and 86-unit set that preceded the freeze
    67%     PLAN_TO_SUBMISSION
    ~70%    the manuscript Discussion

None is over the reported basis of 85 units and 2,340 genomes. A share without
its denominator is not a number, and four of them looking individually plausible
is worse than one that is wrong, because nothing prompts anybody to check.

THE SECOND DENOMINATOR PROBLEM. `phylogeography_association_bp.py` uses two
different country filters in one run. `genome_state` (line 80) refuses a genome
whose `origin_resolution` is `multi_country`, because 'Panama and Peru' is not
evidence for a country. `report_single_country` does not apply that filter when
it builds the counter behind its "dominant country" line. So the share and the
tree scoring are computed over different sets. This script reports both and
names the difference rather than silently picking one.

WHAT IT PRINTS. Every denominator it could reasonably be asked for, so that
whichever one the manuscript quotes, the text can state it:

    rows in the assignments file
    rows carrying a usable country
    rows also surviving the multi_country exclusion

No defaults on any input. Every path must be named, because a default pointing
at one partition is the bug class `audit_defaults_bp.py` exists to catch, and it
has already produced a wrong number in this repository more than once.

Stdlib only. No isolate data is read beyond the columns named below.
"""

import argparse
import collections
import csv
import sys

MISSING = {"", "na", "n/a", "unknown", "none", "null", "-", "missing"}


def usable_country(row, country_col):
    """The country string, or None if this row cannot stand for one country."""
    v = (row.get(country_col) or "").strip()
    return None if v.lower() in MISSING else v


def main():
    ap = argparse.ArgumentParser(
        description="Dominant-country share of a genome set, with the "
                    "denominator stated. All inputs must name the same run.")
    ap.add_argument("--assignments", required=True,
                    help="TSV of the analysed set, one row per genome, keyed "
                         "by sample_id. For the reported basis this is the "
                         "frozen partition, not a register.")
    ap.add_argument("--metadata",
                    help="optional TSV to join country from, if --assignments "
                         "does not carry it. Joined on sample_id.")
    ap.add_argument("--country-col", default="country")
    ap.add_argument("--unit-col", default="unit")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--out", help="write the full country table here")
    a = ap.parse_args()

    with open(a.assignments) as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    if not rows:
        print(f"ABORT: --assignments is empty: {a.assignments}", file=sys.stderr)
        sys.exit(2)
    if "sample_id" not in rows[0]:
        print(f"ABORT: --assignments has no 'sample_id' column. "
              f"Columns present: {list(rows[0])}", file=sys.stderr)
        sys.exit(2)

    if a.country_col not in rows[0]:
        if not a.metadata:
            print(f"ABORT: --assignments has no '{a.country_col}' column and "
                  f"no --metadata was given to join it from.\n"
                  f"Columns present: {list(rows[0])}", file=sys.stderr)
            sys.exit(2)
        with open(a.metadata) as fh:
            meta = {r["sample_id"]: r for r in csv.DictReader(fh, delimiter="\t")}
        missing = [r["sample_id"] for r in rows if r["sample_id"] not in meta]
        for r in rows:
            m = meta.get(r["sample_id"], {})
            r[a.country_col] = m.get(a.country_col, "")
            r.setdefault("origin_resolution", m.get("origin_resolution", ""))
        if missing:
            print(f"WARNING: {len(missing)} of {len(rows)} genomes are absent "
                  f"from --metadata and count as no-country. First: "
                  f"{missing[:3]}", file=sys.stderr)

    units = {r[a.unit_col] for r in rows if r.get(a.unit_col)} \
        if a.unit_col in rows[0] else set()

    # Denominator A: every genome with a usable country. This is what
    # report_single_country counts today.
    with_country = [r for r in rows if usable_country(r, a.country_col)]
    # Denominator B: the same, minus genomes whose origin names more than one
    # country. This is what genome_state scores on the tree.
    single = [r for r in with_country
              if (r.get("origin_resolution") or "").strip() != "multi_country"]

    print("=" * 70)
    print(f"COUNTRY SHARE  {a.assignments}")
    print("=" * 70)
    print(f"  genomes in the assignments file : {len(rows)}")
    if units:
        print(f"  analysis units                  : {len(units)}")
    print(f"  carrying a usable country       : {len(with_country)}")
    print(f"  also not multi-country          : {len(single)}")
    if len(single) != len(with_country):
        print(f"     {len(with_country) - len(single)} genome(s) name more than "
              f"one country. They are scored by neither test but ARE counted")
        print(f"     in the share that phylogeography_association_bp.py prints.")

    for label, subset in (("all genomes with a country", with_country),
                          ("excluding multi-country", single)):
        counts = collections.Counter(usable_country(r, a.country_col)
                                     for r in subset)
        total = sum(counts.values())
        if not total:
            continue
        print(f"\n  --- {label}, denominator {total} ---")
        for c, n in counts.most_common(a.top):
            print(f"     {c:<28} {n:>6}   {100.0 * n / total:5.1f}%")
        top, topn = counts.most_common(1)[0]
        print(f"     QUOTE AS: {top} {topn}/{total} "
              f"({100.0 * topn / total:.1f}%), and state that denominator")

    if a.out:
        counts = collections.Counter(usable_country(r, a.country_col)
                                     for r in single)
        total = sum(counts.values())
        with open(a.out, "w", newline="") as fh:
            w = csv.writer(fh, delimiter="\t", lineterminator="\n")
            w.writerow(["country", "n", "pct_of_with_country_excl_multi"])
            for c, n in counts.most_common():
                w.writerow([c, n, f"{100.0 * n / total:.2f}"])
        print(f"\n  wrote {a.out}")

    print()
    print("  The share is meaningless without its denominator. Whichever of the")
    print("  two above the manuscript quotes, name the denominator in the same")
    print("  sentence and add it to NUMBERS.tsv with the same annotation.")


if __name__ == "__main__":
    main()
