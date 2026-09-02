#!/usr/bin/env python3
"""
manuscript_numbers_bp.py

Emit every number the manuscript needs, in one pass, from the run artefacts.

WHY THIS EXISTS. The manuscript draft carries [CONFIRM] markers where a value has
to come from a run rather than from a document. Filling them by hand, from
several files, across two partitions, is exactly the situation that produced
every serious defect in this project: a plausible number, read off a summary
line, that turned out to describe something else. This script reads per-item
values, recomputes the summaries itself, and refuses to print a figure it cannot
derive.

WHAT IT WILL NOT DO. It will not guess a Gate 1 class, will not average across
units of different diversity classes, and will not report an all-unit r/m median.
A low r/m in this organism is a detection failure rather than a clean unit, so
mixing classes produces a number that reads as a rate and is not one.

INPUTS (all optional except --rm and --assignments; each section is skipped, with
a note, when its input is absent):

  --rm            Summaries/recombination_rm.tsv, or the output of
                  exclude_reference_branches_bp.py. Needs a unit column and a
                  corrected r/m column; both are auto-detected.
  --diversity     output of cluster_diversity_bp.py (cluster_id, n,
                  approx_mean_snps). Supplies the Gate 1 classification.
  --assignments   per-genome TSV: sample_id, unit, country, bioproject, date.
  --refbranch     output of exclude_reference_branches_bp.py, for the
                  reference-branch contamination figures.
  --find-genomes  comma-separated sample_ids to locate by membership, for
                  re-identifying a unit across partitions. Strain LABELS do not
                  transfer between PopPUNK fits; membership does.

Gate 1 window defaults to the calibrated 1270-4671 mean pairwise core SNPs and
can be overridden, because the bounds are brackets rather than constants.

Stdlib only.
"""

import argparse
import collections
import csv
import os
import sys

# TWO METRICS, TWO WINDOWS, and this script accepts either depending on which
# --diversity file it is handed. A single fixed default pair was a live defect:
# the ska-unit bounds applied to an ALIGNMENT-derived diversity column reports 39
# in-window units at median r/m 8.05 instead of the reported 47 at 7.70. It does
# not crash and 8.05 is plausible, which is the dangerous kind. Same family as
# E0, E1, E4 and the identical bug in gate1_from_alignment_bp.py.
#
# The window is now chosen from the column actually present, so the mismatch is
# structurally impossible rather than a convention someone has to remember.
MASH_FLOOR, MASH_CEIL = 1270.0, 4671.0   # ska-unit, for approx_mean_snps
ALN_FLOOR, ALN_CEIL = 700.0, 4700.0      # relocated, for mean_pairwise_snps
FLOOR_DEFAULT, CEIL_DEFAULT = None, None  # resolved from the input, see main()


def die(msg):
    print(f"ABORT: {msg}", file=sys.stderr)
    sys.exit(2)


def read_tsv(path):
    with open(path) as fh:
        sample = fh.read(8192)
        fh.seek(0)
        delim = "\t" if "\t" in sample.splitlines()[0] else ","
        return list(csv.DictReader(fh, delimiter=delim))


def pick(fieldnames, *candidates):
    """First matching column name, case-insensitive, or None."""
    low = {f.lower(): f for f in fieldnames}
    for c in candidates:
        if c.lower() in low:
            return low[c.lower()]
    return None


def quantiles(xs):
    """median and quartiles by the same rule everywhere: lower-median halves."""
    s = sorted(xs)
    n = len(s)
    if n == 0:
        return None, None, None

    def med(v):
        m = len(v)
        return v[m // 2] if m % 2 else (v[m // 2 - 1] + v[m // 2]) / 2.0

    lo = s[: n // 2]
    hi = s[(n + 1) // 2:]
    return med(s), (med(lo) if lo else s[0]), (med(hi) if hi else s[-1])


def hdr(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


# --------------------------------------------------------------------------
def section_rm(rm_rows, div_by_unit, floor, ceil):
    hdr("1. RECOMBINATION  (manuscript Results 3, and the r/m distribution)")

    ucol = pick(rm_rows[0].keys(), "unit", "cluster", "cluster_id")
    rcol = pick(rm_rows[0].keys(), "rm_corrected", "rm", "r_m", "rm_pooled")
    ncol = pick(rm_rows[0].keys(), "n", "n_genomes", "n_tips")
    if not ucol or not rcol:
        die(f"--rm has no recognisable unit/r-m columns. Saw: "
            f"{list(rm_rows[0].keys())}")
    print(f"  columns used: unit='{ucol}'  r/m='{rcol}'"
          f"{('  n=' + repr(ncol)) if ncol else ''}")

    units = {}
    unparsed = []
    for r in rm_rows:
        u = r[ucol]
        v = r[rcol]
        if v in ("", "NA", None):
            unparsed.append(u)
            continue
        try:
            units[u] = float(v)
        except ValueError:
            unparsed.append(u)
    print(f"  units with an r/m value : {len(units)}")
    if unparsed:
        print(f"  units with no value     : {len(unparsed)}  "
              f"e.g. {', '.join(sorted(unparsed)[:5])}")

    if not div_by_unit:
        print("\n  NO --diversity SUPPLIED, so Gate 1 cannot be applied.")
        print("  Refusing to print an all-unit median: it would mix "
              "measurements with")
        print("  detection failures. Supply cluster_diversity_bp.py output.")
        return None

    classes = collections.defaultdict(list)
    missing = []
    for u, v in units.items():
        d = div_by_unit.get(u)
        if d is None:
            missing.append(u)
            continue
        cls = ("in-window" if floor <= d <= ceil
               else "below floor" if d < floor else "above ceiling")
        classes[cls].append((u, v, d))

    if missing:
        print(f"\n  WARNING: {len(missing)} units have r/m but no diversity "
              f"value: {', '.join(sorted(missing)[:8])}")
        print("  These are unclassified and are excluded from every figure "
              "below.")

    print(f"\n  Gate 1 window: {floor:.0f} to {ceil:.0f} mean pairwise core SNPs")
    print(f"  {'class':<14}{'units':>7}{'median r/m':>13}{'IQR':>20}"
          f"{'range':>20}")
    print("  " + "-" * 72)
    for cls in ("in-window", "below floor", "above ceiling"):
        g = classes.get(cls, [])
        if not g:
            print(f"  {cls:<14}{0:>7}")
            continue
        vals = [v for _, v, _ in g]
        m, q1, q3 = quantiles(vals)
        print(f"  {cls:<14}{len(g):>7}{m:>13.2f}"
              f"{f'{q1:.2f} to {q3:.2f}':>20}"
              f"{f'{min(vals):.2f} to {max(vals):.2f}':>20}")

    inw = classes.get("in-window", [])
    if inw:
        print("\n  THE REPORTED RESULT")
        vals = [v for _, v, _ in inw]
        m, q1, q3 = quantiles(vals)
        print(f"    r/m = {m:.2f}  (median of {len(inw)} in-window units, "
              f"IQR {q1:.2f} to {q3:.2f}, range {min(vals):.2f} to "
              f"{max(vals):.2f})")
        print("    Do not report an all-unit median. It averages measurements "
              "with failures.")
        lo = sorted(inw, key=lambda t: t[1])[:3]
        hi = sorted(inw, key=lambda t: -t[1])[:3]
        print(f"    lowest  : " + ", ".join(f"{u}={v:.2f}" for u, v, _ in lo))
        print(f"    highest : " + ", ".join(f"{u}={v:.2f}" for u, v, _ in hi))
    return classes


def section_composition(rows):
    hdr("2. COLLECTION COMPOSITION  (manuscript Results 8 and Discussion)")
    n = len(rows)
    print(f"  genomes in --assignments : {n}")

    ccol = pick(rows[0].keys(), "country", "origin_country")
    pcol = pick(rows[0].keys(), "bioproject", "project")
    ucol = pick(rows[0].keys(), "unit", "cluster", "cluster_id")
    dcol = pick(rows[0].keys(), "date", "collection_date", "year")

    for label, col in (("country", ccol), ("bioproject", pcol),
                       ("unit", ucol), ("date", dcol)):
        if col is None:
            print(f"  no {label} column found, skipping that breakdown")

    if ucol:
        units = collections.Counter(r[ucol] for r in rows if r.get(ucol))
        print(f"  units represented        : {len(units)}")
        sizes = sorted(units.values())
        m, q1, q3 = quantiles(sizes)
        print(f"  unit size                : median {m:.0f}, "
              f"IQR {q1:.0f} to {q3:.0f}, range {min(sizes)} to {max(sizes)}")

    if ccol:
        known = [r[ccol] for r in rows if r.get(ccol)]
        cc = collections.Counter(known)
        print(f"\n  country known for        : {len(known)} of {n} "
              f"({100.0 * len(known) / n:.1f}%)")
        print(f"  distinct countries       : {len(cc)}")
        for c, k in cc.most_common(6):
            print(f"    {c:<28}{k:>6}  ({100.0 * k / len(known):.1f}% of known)")
        top = cc.most_common(1)[0]
        print(f"  DOMINANT                 : {top[0]} at "
              f"{100.0 * top[1] / len(known):.1f}% of known-country genomes")
        # US territories are conflated with the mainland in this column.
        us = [r for r in rows if (r.get(ccol) or "").upper() in ("USA", "US",
                                                                "UNITED STATES")]
        if us:
            sub = pick(rows[0].keys(), "subregion", "sub_region", "region",
                       "state")
            print(f"  genomes labelled USA     : {len(us)}")
            if sub:
                terr = collections.Counter(
                    (r.get(sub) or "unknown") for r in us)
                print("    by subregion           : " + ", ".join(
                    f"{k}={v}" for k, v in terr.most_common()))
                print("    NOTE Puerto Rico and the US Virgin Islands are "
                      "labelled USA in this column.")
                print("         Disaggregate before any statement about "
                      "mainland US origin.")
            else:
                print("    no subregion column, so mainland cannot be "
                      "separated from territories")

    if pcol:
        known = [r[pcol] for r in rows if r.get(pcol)]
        pc = collections.Counter(known)
        print(f"\n  bioproject known for     : {len(known)} of {n} "
              f"({100.0 * len(known) / n:.1f}%)")
        print(f"  distinct bioprojects     : {len(pc)}")
        top3 = pc.most_common(3)
        share = sum(k for _, k in top3) / len(known)
        for p, k in top3:
            print(f"    {p:<28}{k:>6}  ({100.0 * k / len(known):.1f}%)")
        print(f"  TOP 3 SHARE              : {100.0 * share:.1f}% of "
              f"known-bioproject genomes")
        print("  This is the confounder the BioProject control exists for.")

    if dcol:
        yrs = []
        for r in rows:
            v = (r.get(dcol) or "")[:4]
            if v.isdigit():
                yrs.append(int(v))
        if yrs:
            print(f"\n  collection year known    : {len(yrs)} of {n} "
                  f"({100.0 * len(yrs) / n:.1f}%)")
            print(f"  year range               : {min(yrs)} to {max(yrs)}")


def section_refbranch(rows):
    hdr("3. REFERENCE-BRANCH CONTAMINATION  (manuscript Results 7)")
    cols = rows[0].keys()
    c_corr = pick(cols, "rm_corrected")
    c_unc = pick(cols, "rm_uncorrected")
    c_out = pick(cols, "snps_outside")
    c_ref = pick(cols, "ref_branch_snps_outside")
    if not all((c_corr, c_unc, c_out, c_ref)):
        print(f"  --refbranch does not look like exclude_reference_branches_bp "
              f"output. Saw: {list(cols)}")
        return
    corr = [float(r[c_corr]) for r in rows if r[c_corr] not in ("", "NA")]
    unc = [float(r[c_unc]) for r in rows if r[c_unc] not in ("", "NA")]
    tot_out = sum(int(r[c_out]) + int(r[c_ref]) for r in rows)
    ref_out = sum(int(r[c_ref]) for r in rows)
    mc, _, _ = quantiles(corr)
    mu, _, _ = quantiles(unc)
    print(f"  units                                    : {len(rows)}")
    print(f"  median r/m WITHOUT the correction         : {mu:.2f}")
    print(f"  median r/m WITH the correction            : {mc:.2f}")
    print(f"  outside-recombination SNPs from reference : {ref_out} of "
          f"{tot_out} ({100.0 * ref_out / tot_out:.1f}%)")
    print("\n  These are the numbers for this partition. The manuscript "
          "currently quotes")
    print("  52%, 1.85 and 6.30, which were measured on the superseded "
          "82-unit run.")
    print("  Either replace them with the values above, or state the "
          "partition in text.")


def section_find(rows, wanted):
    hdr("4. LOCATE GENOMES BY MEMBERSHIP  (cross-partition re-identification)")
    ucol = pick(rows[0].keys(), "unit", "cluster", "cluster_id")
    if not ucol:
        print("  no unit column in --assignments")
        return
    idx = {r["sample_id"]: r for r in rows if r.get("sample_id")}
    print("  PopPUNK strain labels do not transfer between fits. This locates "
          "genomes")
    print("  by identity, which does.\n")
    found = {}
    for s in wanted:
        r = idx.get(s)
        if r is None:
            print(f"    {s:<24} NOT IN THIS PARTITION")
            continue
        u = r.get(ucol) or "(no unit: not analysed)"
        found.setdefault(u, []).append(s)
        print(f"    {s:<24} {u}")
    if found:
        print()
        for u, members in sorted(found.items()):
            if u.startswith("("):
                continue
            total = sum(1 for r in rows if r.get(ucol) == u)
            print(f"    unit {u}: {len(members)} of the {len(wanted)} sought, "
                  f"and {total} genomes in total")
            if len(members) == len(wanted) and total == len(wanted):
                print("      -> the same set forms a unit in this partition")
            else:
                print("      -> NOT the same set. Report membership, never the "
                      "label.")


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="Emit the manuscript's [CONFIRM] numbers from run "
                    "artefacts.")
    ap.add_argument("--rm", help="Summaries/recombination_rm.tsv")
    ap.add_argument("--diversity", help="cluster_diversity_bp.py output")
    ap.add_argument("--assignments", help="per-genome assignments TSV")
    ap.add_argument("--refbranch", help="exclude_reference_branches_bp.py output")
    ap.add_argument("--find-genomes", default="",
                    help="comma-separated sample_ids to locate by membership")
    ap.add_argument("--floor", type=float, default=None,
                    help="override; default is chosen from the --diversity "
                         "column (alignment 700, Mash proxy 1270)")
    ap.add_argument("--ceiling", type=float, default=None,
                    help="override; default is chosen from the --diversity "
                         "column (alignment 4700, Mash proxy 4671)")
    a = ap.parse_args()

    if not any((a.rm, a.assignments, a.refbranch)):
        die("supply at least one of --rm, --assignments, --refbranch")

    for p in (a.rm, a.diversity, a.assignments, a.refbranch):
        if p and not os.path.exists(p):
            die(f"no such file: {p}")

    div_by_unit = {}
    if a.diversity:
        drows = read_tsv(a.diversity)
        dcol = pick(drows[0].keys(), "cluster_id", "unit", "cluster")
        # aln_mean_pairwise_snps is the column name in the frozen artifact
        # GATE1_ALIGNMENT_2026-08-21.tsv, so that file can be passed directly.
        # Order matters: alignment columns are preferred over the Mash proxy,
        # because the alignment window is the reported one.
        scol = pick(drows[0].keys(), "aln_mean_pairwise_snps",
                    "mean_pairwise_snps", "approx_mean_snps", "mean_snps")
        if not dcol or not scol:
            die(f"--diversity has no recognisable columns. Saw: "
                f"{list(drows[0].keys())}")
        # Resolve the window from the metric actually supplied.
        if scol in ("mean_pairwise_snps", "aln_mean_pairwise_snps"):
            auto_floor, auto_ceil, metric = ALN_FLOOR, ALN_CEIL, "ALIGNMENT"
        else:
            auto_floor, auto_ceil, metric = MASH_FLOOR, MASH_CEIL, "Mash proxy"
        if a.floor is None:
            a.floor = auto_floor
        if a.ceiling is None:
            a.ceiling = auto_ceil
        print(f"diversity column {scol!r} -> {metric} metric, "
              f"Gate 1 window [{a.floor:.0f}, {a.ceiling:.0f}]")
        if metric == "Mash proxy":
            print("  NOTE: the reported window is the ALIGNMENT-derived one. The "
                  "Mash proxy misplaced 22 of 85 units.")
        for r in drows:
            if r[scol] not in ("", None):
                try:
                    div_by_unit[r[dcol]] = float(r[scol])
                except ValueError:
                    pass

    if a.floor is None:
        a.floor, a.ceiling = ALN_FLOOR, ALN_CEIL
    if a.rm:
        section_rm(read_tsv(a.rm), div_by_unit, a.floor, a.ceiling)
    if a.assignments:
        arows = read_tsv(a.assignments)
        section_composition(arows)
        if a.find_genomes:
            section_find(arows,
                         [s.strip() for s in a.find_genomes.split(",")
                          if s.strip()])
    if a.refbranch:
        section_refbranch(read_tsv(a.refbranch))

    print("\n" + "=" * 72)
    print("Every figure above was recomputed from per-item values in the files "
          "given.")
    print("None was carried from a document or from a previous partition.")
    print("=" * 72)


if __name__ == "__main__":
    main()
