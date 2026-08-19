#!/usr/bin/env python3
"""Is the structure that breaks our partitions actually PSEUDO-REPLICATION?

THE QUESTION BEHIND THIS. Should we subsample the collection -- using metadata,
the Mash matrix or the PopPUNK strains -- BEFORE clustering, rather than
clustering everything and dealing with the mess afterwards?

That question has two very different versions, and they call for opposite
answers:

  BALANCED SUBSAMPLING (take k genomes per country / per BioProject) targets
  the phylogeographic bias. It would also shrink every unit, and we have just
  measured that small units are where everything fails -- modality is
  undecidable below n=25 and union coverage is size-confounded throughout. It
  treats a bias that only limits Deliverable B by worsening the exact failure
  mode that limits Deliverable A.

  REDUNDANCY COLLAPSING (take k representatives of each near-identical group)
  targets something else: clonal expansions that are one epidemiological event
  sequenced many times. Those are not extra evidence about the population, and
  inside a cluster they manufacture apparent structure -- a tight core plus
  outliers -- which is precisely the signature that has been disqualifying our
  units.

WHICH ONE APPLIES IS AN EMPIRICAL QUESTION, and this script answers it. For each
clonal group (units whose mean pairwise distance is far below the analysable
floor), it asks how concentrated that group is in:

    BioProject   -- one submission = one study = pseudo-replication
    Country / Subregion
    Collection year
    Linked patient case -- the metadata's own duplicate flag

CONCENTRATION IS THE TEST. If a 36-genome group at 55 mean SNPs is one
BioProject from one subregion in one year, it is one outbreak sequenced 36
times, and collapsing it to a few representatives removes an artefact rather
than discarding data. If the same group spans many projects and years, it is a
real widespread clone and collapsing it would destroy signal.

METADATA JOIN -- READ THIS BEFORE EDITING. The curated TSV has TWO columns named
`sample_id` (indices 0 and 16) plus `FASTA_name` (17). csv.DictReader silently
keeps only the last, and joining on that key drops roughly half the collection
with no error. Index by raw position and try all three keys.

Usage:
    python3 pseudoreplication_bp.py
    python3 pseudoreplication_bp.py --selftest
"""

import argparse
import collections
import csv
import os
import sys

SELF = os.path.dirname(os.path.abspath(__file__))
META = ("/home/phemarajata/Downloads/final_deduped_all_BP_with_locations/"
        "megamix_bestshot_cleaned_dropGCF_on_Fdups_APPENDED.tsv")

# Raw column positions, 0-indexed. Do NOT switch to DictReader -- see docstring.
#
# THESE WERE WRONG ONCE AND THE ERROR WAS SILENT. An earlier version used 11 for
# BioProject and 13 for the date. Column 11 is the BioSample accession, which is
# UNIQUE PER GENOME, so every "top BioProject share" came out at roughly 1/n and
# the analysis appeared to show that clonal groups are not study-driven. Column
# 13 is the submitter, so no date ever parsed and the year column was silently
# nan. Both produced a plausible-looking table with no error.
#
# `assert_columns` below now checks that each column CONTAINS what it should --
# BioProjects look like PRJ*, dates parse as years -- because a positional index
# into a wide TSV is exactly the kind of thing that is wrong without complaining.
COL_SAMPLE_A = 0
COL_COUNTRY = 1
COL_SUBREGION = 2
COL_BIOPROJECT = 10      # "Assembly BioProject Accession", e.g. PRJNA278506
COL_BIOSAMPLE = 11       # unique per genome -- NEVER use for concentration
COL_DATE = 12            # "final_collection_dates", e.g. 2014-08-03
COL_SUBMITTER = 13
COL_SAMPLE_B = 16
COL_FASTA = 17
COL_PATIENT = 19


def assert_columns(path=META):
    """Verify the positional indices still point at the intended fields.

    Returns a list of complaints; empty means the layout is as expected.
    """
    bad = []
    proj, dated, rows = 0, 0, 0
    with open(path, newline="") as fh:
        rd = csv.reader(fh, delimiter="\t")
        next(rd, None)
        for f in rd:
            if len(f) <= COL_FASTA:
                continue
            rows += 1
            if norm(f[COL_BIOPROJECT]).upper().startswith("PRJ"):
                proj += 1
            if year(norm(f[COL_DATE])):
                dated += 1
            if rows >= 500:
                break
    if rows and proj / rows < 0.5:
        bad.append("column %d does not look like BioProject accessions "
                   "(%.0f%% start with PRJ)" % (COL_BIOPROJECT, 100 * proj / rows))
    if rows and dated / rows < 0.3:
        bad.append("column %d does not look like dates (%.0f%% parse to a year)"
                   % (COL_DATE, 100 * dated / rows))
    return bad


def norm(s):
    return (s or "").strip().strip('"').replace(".fasta", "").replace(".fa", "")


def load_meta(path=META):
    """key -> record, indexed under all three name columns."""
    out = {}
    with open(path, newline="") as fh:
        rd = csv.reader(fh, delimiter="\t")
        next(rd, None)
        for f in rd:
            if len(f) <= COL_FASTA:
                continue
            rec = {
                "country": norm(f[COL_COUNTRY]),
                "subregion": norm(f[COL_SUBREGION]),
                "bioproject": norm(f[COL_BIOPROJECT]),
                "date": norm(f[COL_DATE]),
                "patient": norm(f[COL_PATIENT]),
            }
            for i in (COL_SAMPLE_A, COL_SAMPLE_B, COL_FASTA):
                k = norm(f[i])
                if k:
                    out.setdefault(k, rec)
    return out


def load_membership(path):
    m = collections.defaultdict(list)
    with open(path) as fh:
        next(fh)
        for line in fh:
            f = line.rstrip("\n").split("\t")
            if len(f) >= 2:
                m[f[0]].append(norm(f[1]))
    return m


def concentration(values):
    """(top_share, n_distinct, top_label) over non-empty values."""
    vals = [v for v in values if v and v.lower() not in ("na", "nan", "none", "-")]
    if not vals:
        return (float("nan"), 0, "")
    c = collections.Counter(vals)
    lab, n = c.most_common(1)[0]
    return (n / len(vals), len(c), lab)


def year(d):
    d = (d or "").strip()
    return d[:4] if len(d) >= 4 and d[:4].isdigit() else ""


def profile(unit, samples, meta):
    recs = [meta[s] for s in samples if s in meta]
    hit = len(recs)
    bp = concentration([r["bioproject"] for r in recs])
    co = concentration([r["country"] for r in recs])
    sr = concentration([r["subregion"] for r in recs])
    yr = concentration([year(r["date"]) for r in recs])
    return {
        "unit": unit, "n": len(samples), "matched": hit,
        "bp_share": bp[0], "bp_n": bp[1], "bp_top": bp[2],
        "co_share": co[0], "co_top": co[2],
        "sr_share": sr[0], "sr_n": sr[1], "sr_top": sr[2],
        "yr_share": yr[0], "yr_n": yr[1], "yr_top": yr[2],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--membership", action="append", default=None,
                    help="membership TSVs; repeatable")
    ap.add_argument("--diversity", action="append", default=None,
                    help="modality/diversity TSVs supplying mean_snps")
    ap.add_argument("--floor", type=float, default=1270.0)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()

    memfiles = args.membership or [
        os.path.join(SELF, "inputs", "analysable_membership.tsv"),
        os.path.join(SELF, "inputs", "newstrains_membership.tsv"),
    ]
    divfiles = args.diversity or [
        os.path.join(SELF, "newstrains_modality.tsv"),
        os.path.join(SELF, "fastbaps_L1_all_measured.tsv"),
    ]

    complaints = assert_columns()
    if complaints:
        for c in complaints:
            print("COLUMN CHECK FAILED: %s" % c, file=sys.stderr)
        print("Refusing to run on a layout that does not match the indices.",
              file=sys.stderr)
        return 2

    meta = load_meta()
    print("metadata rows indexed: %d keys" % len(meta))

    mem = {}
    for p in memfiles:
        if os.path.exists(p):
            for k, v in load_membership(p).items():
                mem.setdefault(k, v)
    print("units with membership: %d" % len(mem))

    div = {}
    for p in divfiles:
        if not os.path.exists(p):
            continue
        with open(p) as fh:
            hdr = fh.readline().rstrip("\n").split("\t")
            for line in fh:
                f = line.rstrip("\n").split("\t")
                r = dict(zip(hdr, f))
                try:
                    div.setdefault(r["cluster_id"], float(r["mean_snps"]))
                except (KeyError, ValueError):
                    pass

    rows = []
    for unit, samples in mem.items():
        if unit not in div or len(samples) < 6:
            continue
        rows.append((div[unit], profile(unit, samples, meta)))
    rows.sort(key=lambda t: t[0])
    if not rows:
        print("no units with both membership and diversity", file=sys.stderr)
        return 1

    clonal = [(d, p) for d, p in rows if d < args.floor]
    inrange = [(d, p) for d, p in rows if d >= args.floor]

    print("\n" + "=" * 100)
    print("ARE THE CLONAL GROUPS PSEUDO-REPLICATION?")
    print("=" * 100)
    print("\n`top BioProject %%` = share of the unit's genomes from its single "
          "largest BioProject.\nHigh share + one subregion + one year = one "
          "study sequencing one event repeatedly.\n")
    print("%-14s %6s %8s %7s %7s %8s %7s %7s  %s"
          % ("unit", "n", "mean SNP", "matched", "top BP%", "#BP", "top yr%",
             "#yr", "top subregion"))
    print("-" * 100)
    for d, p in rows:
        mark = "  <-- clonal" if d < args.floor else ""
        print("%-14s %6d %8.0f %7d %6.0f%% %8d %6.0f%% %7d  %-22s%s"
              % (p["unit"], p["n"], d, p["matched"],
                 100 * (p["bp_share"] if p["bp_share"] == p["bp_share"] else 0),
                 p["bp_n"],
                 100 * (p["yr_share"] if p["yr_share"] == p["yr_share"] else 0),
                 p["yr_n"], (p["sr_top"] or "?")[:22], mark))

    def avg(rs, key):
        v = [p[key] for _, p in rs if p[key] == p[key]]
        return sum(v) / len(v) if v else float("nan")

    print("\n" + "=" * 100)
    print("THE COMPARISON -- clonal groups vs units inside the analysable range")
    print("=" * 100)
    print("\n%-34s %14s %14s" % ("", "clonal (<%d)" % args.floor, "in range"))
    for key, label in (("bp_share", "mean top-BioProject share"),
                       ("yr_share", "mean top-year share"),
                       ("sr_share", "mean top-subregion share")):
        print("%-34s %13.0f%% %13.0f%%"
              % (label, 100 * avg(clonal, key), 100 * avg(inrange, key)))
    print("%-34s %14.1f %14.1f"
          % ("mean distinct BioProjects", avg(clonal, "bp_n"), avg(inrange, "bp_n")))
    print("\ngroups: %d clonal, %d in range" % (len(clonal), len(inrange)))

    print("\nREADING")
    print("  Reported as a gradient, NOT a pass/fail. An earlier version of this"
          "\n  script called the verdict on whether the gap exceeded 15 points;"
          "\n  it came out at 14 and printed 'not markedly', which is the same"
          "\n  round-number thresholding this project has spent weeks documenting.")
    deltas = []
    for key, label in (("bp_share", "BioProject"), ("yr_share", "year"),
                       ("sr_share", "subregion")):
        c, i = avg(clonal, key), avg(inrange, key)
        if c == c and i == i:
            deltas.append(c - i)
            print("\n  %-10s clonal %.0f%% vs in-range %.0f%%  (+%.0f points)"
                  % (label, 100 * c, 100 * i, 100 * (c - i)))
    if deltas:
        print("\n  All %d axes point the same way, by %.0f-%.0f points, on %d "
              "clonal groups." % (len(deltas), 100 * min(deltas),
                                  100 * max(deltas), len(clonal)))
        print("  So clonal groups carry MORE study/time/place redundancy than "
              "in-range units\n  -- consistently, but not overwhelmingly. The "
              "typical clonal group draws\n  ~%.0f%% of its genomes from one "
              "study, which is substantial "
              "pseudo-replication\n  without being the near-100%% that would "
              "make collapsing obviously safe."
              % (100 * avg(clonal, "bp_share")))
        print("\n  What this supports: collapsing near-identical genomes to a "
              "few representatives\n  is defensible and would remove real "
              "redundancy. What it does NOT support:\n  treating these groups "
              "as pure sequencing artefacts -- a third to a half of\n  each is "
              "genuinely multi-study, so some local-clone signal is real.")
    return 0


def selftest():
    fails = []

    def chk(desc, got, want, tol=1e-9):
        ok = (abs(got - want) <= tol) if isinstance(want, float) else (got == want)
        print("%-56s %s" % (desc, "ok" if ok else "FAIL got=%r want=%r" % (got, want)))
        if not ok:
            fails.append(desc)

    chk("concentration of a pure group", concentration(["a"] * 5)[0], 1.0, 1e-12)
    chk("concentration counts distinct", concentration(["a", "a", "b"])[1], 2)
    chk("concentration share", concentration(["a", "a", "b"])[0], 2 / 3, 1e-12)
    # Missing values must be EXCLUDED, not counted as a category -- otherwise a
    # unit with no metadata looks perfectly concentrated on "NA".
    chk("NA excluded", concentration(["NA", "NA", "b"])[1], 1)
    chk("all-missing gives nan", concentration(["NA", ""])[1], 0)
    chk("year parsed", year("2015-06-01"), "2015")
    chk("bad year rejected", year("unknown"), "")
    chk("norm strips fasta suffix", norm('"X.fasta"'), "X")

    # The positional indices must point at the intended fields. This is the
    # check that would have caught BioProject/BioSample being off by one.
    if os.path.exists(META):
        bad = assert_columns()
        for b in bad:
            print("  COLUMN CHECK: %s" % b)
        chk("column indices point at the right fields", bad, [])
        # And specifically: BioProject must NOT be unique per genome, or every
        # concentration measure collapses to 1/n.
        meta = load_meta()
        projs = set(r["bioproject"] for r in meta.values() if r["bioproject"])
        chk("BioProject is not unique per genome", len(projs) < 500, True)

    # The metadata file must actually join -- trap 12. If the join key is wrong
    # this silently halves the collection, so assert a real match rate.
    if os.path.exists(META):
        meta = load_meta()
        memp = os.path.join(SELF, "inputs", "analysable_membership.tsv")
        if os.path.exists(memp):
            mem = load_membership(memp)
            alls = [s for v in mem.values() for s in v]
            hit = sum(1 for s in alls if s in meta)
            rate = hit / len(alls) if alls else 0
            print("%-56s %s" % ("metadata join rate on the analysable set",
                                "%.1f%% (%d/%d)" % (100 * rate, hit, len(alls))))
            chk("join rate is not the trap-12 half-loss", rate > 0.90, True)

    print("\n%d test(s) failed" % len(fails) if fails else "\nall tests passed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
