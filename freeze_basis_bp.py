#!/usr/bin/env python3
"""
Freeze the analysis basis: one panel, one partition, coordinated, checkable.

WHY THIS EXISTS. Results in this project have flip-flopped because "the panel"
and "the partition" were never pinned to each other. Two partitions of the same
collection are in play -- a in-house/workstation run (86 units) and an A100 run
(88, which splits strain_1_L1_26 into three) -- and the panel has been corrected
underneath both. Tables were then built by globbing an output directory that
contains BOTH, so some rows describe one partition and some the other. That is
not a bookkeeping annoyance; it silently changed r/m, Gate 1 membership and the
cgMLST concordance median.

THE BASIS, decided 2026-08-22: the CORRECTED WORKSTATION PARTITION.
85 units, 2,340 genomes. Reasons, in order of weight:

  1. It is the only partition that is actually corrected. Both partitions carry
     the same 7 duplicate BioSamples; the A100 additionally cannot be corrected
     without re-deriving it, which was ruled out (REDO_DECISION). This basis has
     zero duplicate BioSamples and zero register-excluded genomes.
  2. Every alignment is local. The A100's strain_1_L1_36 / strain_1_L1_37 have
     no .core.full.aln here, so their r/m can never be re-derived locally.
  3. r/m was re-derived on it (2026-08-21); generate_numbers.py reads it;
     NU_HYPOTHESIS is keyed to it.
  4. The A100 refinement buys nothing measurable: its n=98 child of
     strain_1_L1_26 is a clonal expansion at 72 mean pairwise SNPs, an order of
     magnitude below the Gate 1 floor, and refinement did not increase the
     in-window set.
  5. It retroactively makes DISTANCES_v4c_SUMMARY.tsv and CGMLST_CONCORDANCE.tsv
     CORRECT. Their contamination is exactly the two A100-only rows plus units
     whose membership is the workstation's -- so restricted to this basis, both
     are internally consistent and need no repair.

CONSEQUENCE FOR THE METHODS. METHODS_DRAFT §2.12 currently calls the A100 run
"production" and this one "control". That designation must be FLIPPED: this is
the reported partition, and the A100 run becomes the cross-hardware
reproducibility control -- which is a stronger use of it, since the two agree to
0.46% median relative r/m across the 82 units they share.

WHAT THIS SCRIPT DOES
  --build     writes FINAL_BASIS_2026-08-22/ (partition, panel, manifest)
  (default)   VALIDATES the frozen basis and exits non-zero on any drift

The validator also pins the ATTRIBUTION artifacts to each other (added
2026-08-23), for the same reason it pins the panel to the partition: the two
attribution scorers were free to disagree and did, silently.

Run the validator before quoting any number. It is cheap and it is the only
thing standing between this collection and the next silent partition mismatch.
"""
import argparse
import csv
import hashlib
import os
import sys
from collections import Counter, defaultdict

B = os.path.dirname(os.path.abspath(__file__))
OUT = f"{B}/FINAL_BASIS_2026-08-22"
PARTITION = f"{OUT}/FINAL_PARTITION.tsv"
PANEL = f"{OUT}/FINAL_PANEL.tsv"
MANIFEST = f"{OUT}/MANIFEST.sha256"

SRC_PARTITION = f"{B}/rederive_2026-08-21/curated_L1v4c_clusters_corrected.tsv"
SRC_PANEL = f"{B}/PANEL_v4d_2026-08-21.tsv"
RM = f"{B}/L1v4c_out/Summaries/recombination_rm.tsv"

EXPECT_UNITS = 85
EXPECT_GENOMES = 2340


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_partition(path):
    m = defaultdict(set)
    for r in csv.DictReader(open(path), delimiter="\t"):
        m[r["cluster_id"]].add(r["sample_id"])
    return m


def build():
    os.makedirs(OUT, exist_ok=True)
    part = load_partition(SRC_PARTITION)
    members = {s for v in part.values() for s in v}
    drops = {r["sample_id"] for r in
             csv.DictReader(open(f"{B}/PANEL_DUPLICATES_2026-08-21.tsv"),
                            delimiter="\t") if r["action"] == "drop"}
    excl = {r["sample_id"] for r in
            csv.DictReader(open(f"{B}/PANEL_EXCLUSIONS.tsv"), delimiter="\t")}

    with open(PARTITION, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["unit", "sample_id"])
        for u in sorted(part, key=lambda x: (int(x.split("_")[1]),
                                             int(x.split("_L1_")[1]))):
            for s in sorted(part[u]):
                w.writerow([u, s])

    # Panel: re-role the orphans and separate MEMBERSHIP from ASSIGNMENT.
    # The old `subcluster` column carried a unit label for 615 genomes that are
    # NOT members -- for assign_only genomes it is a nearest-unit label. Any
    # join on it silently picks up non-members. Split the two meanings.
    rows = list(csv.DictReader(open(SRC_PANEL), delimiter="\t"))
    cols = list(rows[0])
    for c in ("unit_membership", "nearest_unit", "basis_role"):
        if c not in cols:
            cols.append(c)
    unit_of = {s: u for u, v in part.items() for s in v}
    reroled = 0
    for r in rows:
        s = r["sample_id"]
        if s in unit_of:
            r["unit_membership"] = unit_of[s]
            r["nearest_unit"] = ""
            r["basis_role"] = "analysis"
        else:
            r["unit_membership"] = ""
            r["nearest_unit"] = r.get("subcluster", "")
            r["basis_role"] = "assign_only"
            if r.get("role") == "analysis":
                reroled += 1
    with open(PANEL, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                           lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    with open(MANIFEST, "w") as fh:
        for p in (PARTITION, PANEL):
            fh.write(f"{sha(p)}  {os.path.basename(p)}\n")

    print(f"wrote {PARTITION}: {len(part)} units, {len(members)} genomes")
    print(f"wrote {PANEL}: {len(rows)} rows, {reroled} re-roled analysis -> assign_only")
    print(f"wrote {MANIFEST}")
    if reroled:
        print("  re-roled (role=analysis but in no unit after the corrections):")
        for r in rows:
            if r["basis_role"] == "assign_only" and r.get("role") == "analysis":
                print(f"    {r['sample_id']}  (was {r.get('subcluster')})")


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))
    return ok


def validate():
    if not os.path.exists(PARTITION):
        sys.exit(f"no frozen basis at {OUT}; run --build first")
    print(f"validating {OUT}\n")
    part = defaultdict(set)
    for r in csv.DictReader(open(PARTITION), delimiter="\t"):
        part[r["unit"]].add(r["sample_id"])
    members = {s for v in part.values() for s in v}
    panel = {r["sample_id"]: r for r in csv.DictReader(open(PANEL), delimiter="\t")}
    drops = {r["sample_id"] for r in
             csv.DictReader(open(f"{B}/PANEL_DUPLICATES_2026-08-21.tsv"),
                            delimiter="\t") if r["action"] == "drop"}
    excl = {r["sample_id"] for r in
            csv.DictReader(open(f"{B}/PANEL_EXCLUSIONS.tsv"), delimiter="\t")}

    ok = True
    ok &= check("manifest intact (no edit since freeze)",
                all(line.split("  ")[0] == sha(f"{OUT}/{line.split('  ')[1].strip()}")
                    for line in open(MANIFEST)))
    ok &= check(f"unit count == {EXPECT_UNITS}", len(part) == EXPECT_UNITS,
                f"got {len(part)}")
    ok &= check(f"genome count == {EXPECT_GENOMES}", len(members) == EXPECT_GENOMES,
                f"got {len(members)}")
    ok &= check("no genome in two units",
                sum(len(v) for v in part.values()) == len(members))
    ok &= check("every member is in the panel", not (members - set(panel)),
                f"{len(members - set(panel))} missing")
    ok &= check("no duplicate BioSample in the partition", not (members & drops),
                f"{len(members & drops)} present")
    ok &= check("no register-excluded genome in the partition", not (members & excl),
                f"{len(members & excl)} present")
    orph = [s for s, r in panel.items()
            if r.get("basis_role") == "analysis" and s not in members]
    ok &= check("no panel row claims analysis without membership", not orph,
                f"{len(orph)}: {orph[:4]}")
    bad = [s for s in members if panel[s].get("unit_membership") !=
           next(u for u, v in part.items() if s in v)]
    ok &= check("panel unit_membership agrees with the partition", not bad,
                f"{len(bad)} disagree")
    leak = [s for s, r in panel.items()
            if r.get("unit_membership") and s not in members]
    ok &= check("no unit_membership set for a non-member", not leak,
                f"{len(leak)} leaked")

    # The attribution artifacts must agree WITH EACH OTHER. Two scorers build
    # their pools independently -- score_cgmlst_lichtenegger.py writes
    # CGMLST_LICHT_ATTRIBUTION.tsv (one estimator per run) and grouping_test_bp.py
    # writes GROUPING_LADDER.tsv (all four) -- so agreement is a real
    # cross-check, not a tautology. It is checked here because the failure it
    # catches already happened: the region headline (modal k=20, 41/46) was
    # cited to the attribution table, which is nearest-neighbour and says 37/46.
    # Nothing was watching the two, because the ladder persisted no file at all.
    ATT, LAD = f"{B}/CGMLST_LICHT_ATTRIBUTION.tsv", f"{B}/GROUPING_LADDER.tsv"
    if os.path.exists(ATT) and os.path.exists(LAD):
        att = list(csv.DictReader(open(ATT), delimiter="\t"))
        lad = list(csv.DictReader(open(LAD), delimiter="\t"))
        ns = ({len([r for r in att if r["scale"] == sc])
               for sc in ("country", "region")} | {int(r["n"]) for r in lad})
        ok &= check("attribution artifacts agree on the scorable denominator",
                    len(ns) == 1, f"saw {sorted(ns)}")
        lnn = {r["grouping"]: int(r["correct"]) for r in lad
               if r["estimator"] == "nearest_nb"}
        dis = []
        for sc, g in (("country", "country"), ("region", "region_7way")):
            a = sum(int(r["correct"]) for r in att if r["scale"] == sc)
            if g in lnn and a != lnn[g]:
                dis.append(f"{sc}: table {a} vs ladder {lnn[g]}")
        ok &= check("both scorers agree on the nearest-neighbour calls",
                    not dis, "; ".join(dis) or "country + region match")

    if os.path.exists(RM):
        rm = {r["unit"] for r in csv.DictReader(open(RM), delimiter="\t")}
        ok &= check("r/m table covers exactly the frozen units", rm == set(part),
                    f"extra {sorted(rm - set(part))[:3]} missing {sorted(set(part) - rm)[:3]}")
        rmn = {r["unit"]: r["n"] for r in csv.DictReader(open(RM), delimiter="\t")}
        mism = [u for u in part if u in rmn and rmn[u].isdigit()
                and int(rmn[u]) != len(part[u])]
        ok &= check("r/m table unit sizes match the partition", not mism,
                    f"{len(mism)}: {mism[:4]}")

    print(f"\n{'BASIS IS CONSISTENT' if ok else 'BASIS IS BROKEN -- do not quote numbers'}")
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    a = ap.parse_args()
    if a.build:
        build()
        sys.exit(validate())
    sys.exit(validate())
