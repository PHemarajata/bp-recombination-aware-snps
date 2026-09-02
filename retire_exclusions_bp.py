#!/usr/bin/env python3
"""
Retire the four unevidenced PANEL_EXCLUSIONS rows. Idempotent; re-runnable.

WHY THIS IS A SCRIPT AND NOT A HAND EDIT. `*.tsv` is gitignored by design
(isolate-level data), so an edit to PANEL_EXCLUSIONS.tsv is invisible to git and
unreproducible on another checkout. The register is the source of truth for what
is excluded, so a change to it has to be replayable. This script is the record.

WHAT IT DOES. Sets `status = retired` on four rows, rewrites their `reason` to
the measurement that superseded them, and repoints `evidence`. It does NOT
delete them: a register exists to say what was decided and why, and a deleted
row cannot say "this was decided and it was wrong". Readers honour `status`.

THE EVIDENCE, from EXCLUSION_RECHECK_2026-08-23.md:

  All four were excluded on `core coverage <85%`, measured on the SKESA batch.
  The panel and the cgMLST reference pool both use the SPAdes re-assemblies, and
  on those all four pass every operative gate. The SPAdes re-QC of 2026-08-18
  had already recorded all four as `pass` with empty fail_reasons; that result
  was never reconciled against the register, which was written afterwards from
  the superseded numbers.

  Compounding it, the register's `core=na%` was a TRANSCRIPTION ERROR, not an
  unmeasured field: NEW200_QC_2026-08-17.tsv carries the value in
  `core_cov_unfiltered_pct`, and the register read the adjacent
  `core_cov_filtered_pct`, which is empty for every row in that file.

  The `wrong_species_or_divergent` class on SRR2896271 is refuted outright. Its
  0.0135 mash is the SKESA figure; the assembly in use measures 0.0087, inside
  the operative <=0.012 code gate (the 0.008 in the README is prose and is not
  enforced anywhere). Confirmed wrong-species genomes in this register sit at
  core 18-50% / mash 0.022-0.064; this one is core 89.1%. Divergent, not wrong
  species. The class is left unchanged as the historical record of what was
  decided -- `status = retired` is what makes it inert.

DECIDED 2026-08-23 by the project owner, with ERR9980356 explicitly kept: it is
the weakest passing assembly in the batch on both axes (core 86.2 and mash
0.0093, each rank 172/172), but it clears every operative gate, and excluding a
genome for placing last in a passing distribution is post-hoc unless the
threshold is set independently.

CONSEQUENCE: none, for any headline. The cgMLST reference pool already contained
all four, so no attribution number moves. The panel grows 2,955 -> 2,959 and the
four are `assign_only` -- none is in the frozen partition, which stays at 2,340
genomes in 85 units.
"""
import csv
import os
import shutil

B = os.path.dirname(os.path.abspath(__file__))
REG = f"{B}/PANEL_EXCLUSIONS.tsv"
EVID = "EXCLUSION_RECHECK_2026-08-23.tsv (supersedes NEW200_QC_2026-08-17.tsv)"
ACTION = "re-included 2026-08-23; see EXCLUSION_RECHECK_2026-08-23.md"

RETIRE = {
    "SRR2896259":
        "RETIRED 2026-08-23, unevidenced. Excluded on SKESA core 81.5%; the "
        "SPAdes assembly in use passes cleanly -- core 93.3%, mash 0.0065, "
        "ratio 0.97, 826 contigs at N50 15.8 kb. Nothing distinguishes it from "
        "a routine pass.",
    "SRR2896257":
        "RETIRED 2026-08-23, unevidenced. Excluded on SKESA core 80.7%; the "
        "SPAdes assembly in use passes every gate -- core 90.5%, mash 0.0077, "
        "ratio 0.89. CAVEAT: 3,315 contigs / 7,452,260 bp is the most "
        "fragmented assembly in the batch. That is a confounder for ACCESSORY "
        "analysis and is not a core-attribution gate; if it is ever excluded "
        "again, exclude it for fragmentation and say so.",
    "ERR9980356":
        "RETIRED 2026-08-23, unevidenced. Excluded on SKESA core 83.1%; the "
        "SPAdes assembly in use passes -- core 86.2%, mash 0.0093, ratio 0.90. "
        "KEPT KNOWINGLY: it is the weakest passing assembly in the batch on "
        "both axes at once (core and mash each rank 172/172). It clears every "
        "operative gate; excluding it would need a stated panel-wide threshold "
        "(core >=87% or mash <=0.009) applied to all 172, not to this genome.",
    "SRR2896271":
        "RETIRED 2026-08-23, reason_class REFUTED. Not wrong-species: the "
        "SPAdes assembly in use is core 89.1%, mash 0.0087, inside the "
        "operative <=0.012 code gate (the 0.008 in PANEL_EXCLUSIONS_README is "
        "prose and is enforced nowhere). The 0.0135 was the superseded SKESA "
        "assembly. True B. thailandensis in this register sits at mash 0.0635, "
        "7x higher, and non-pseudomallei genomes here are core 18-50%. "
        "Divergent, not wrong species. reason_class left as decided, for the "
        "record; status=retired is what makes the row inert.",
}


def main():
    rows = list(csv.DictReader(open(REG), delimiter="\t"))
    cols = list(rows[0])
    for c in ("status", "action", "reason", "evidence", "decided"):
        if c not in cols:
            raise SystemExit(f"register lacks a '{c}' column -- schema changed")

    missing = RETIRE.keys() - {r["sample_id"] for r in rows}
    if missing:
        raise SystemExit(f"not in the register: {sorted(missing)}")

    changed = already = 0
    for r in rows:
        if r["sample_id"] not in RETIRE:
            continue
        if r["status"] == "retired":
            already += 1
            continue
        r["status"] = "retired"
        r["action"] = ACTION
        r["reason"] = RETIRE[r["sample_id"]]
        r["evidence"] = EVID
        r["decided"] = "2026-08-23"
        changed += 1

    if not changed:
        print(f"nothing to do -- all {already} rows already retired")
        return

    shutil.copy2(REG, f"{REG}.bak_2026-08-23")
    with open(REG, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                           lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    active = sum(1 for r in rows if r["status"] != "retired")
    print(f"retired {changed} row(s) ({already} already retired)")
    print(f"register: {len(rows)} rows, {active} ACTIVE, "
          f"{len(rows)-active} retired")
    print(f"backup: {os.path.basename(REG)}.bak_2026-08-23")


if __name__ == "__main__":
    main()
