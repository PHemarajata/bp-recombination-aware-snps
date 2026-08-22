# The frozen analysis basis — 2026-08-22

**85 units, 2,340 genomes.** This is the single coordinated panel + partition
that all reported results are computed on. It is frozen. Nothing downstream may
be quoted against a different unit set.

Validate before quoting anything:

```bash
python3 freeze_basis_bp.py
```

Twelve checks; exits non-zero on any drift. It passes as of the freeze.

---

## 1. Why a freeze was needed

Two partitions of the same collection were in play — an in-house workstation run
(86 units) and an A100 run (88, which splits `strain_1_L1_26` into three) — and
the panel was corrected underneath both. Worse, `L1v4c_out/Clusters` physically
contains **both**: 88 unit directories, with the A100's split children sitting
beside their own unsplit parent, so the 153 genomes of that lineage are present
twice. Any table built by globbing that directory mixes the two.

That is the mechanism behind the repeated corrections. It silently moved r/m,
Gate 1 membership and the cgMLST concordance median.

## 2. What the basis is, and why this one

**The corrected workstation partition.** In order of weight:

1. **It is the only partition that is actually corrected.** Both carry the same
   7 duplicate BioSamples; the A100 cannot be corrected without re-deriving it,
   which `REDO_DECISION_2026-08-21.md` ruled out. This basis has **zero**
   duplicate BioSamples and **zero** register-excluded genomes.
2. **Every alignment is local.** The A100's `strain_1_L1_36` / `strain_1_L1_37`
   have no `.core.full.aln` here, so their r/m can never be re-derived locally.
3. r/m was re-derived on it (2026-08-21); `generate_numbers.py` reads it;
   `NU_HYPOTHESIS` is keyed to it.
4. **The A100 refinement buys nothing measurable.** Its n=98 child of
   `strain_1_L1_26` is a clonal expansion at 72 mean pairwise SNPs — an order of
   magnitude below the Gate 1 floor — and refinement did not increase the
   in-window set.
5. **It retroactively makes the two contaminated tables correct.**
   `DISTANCES_v4c_SUMMARY.tsv` and `CGMLST_CONCORDANCE.tsv` are contaminated by
   exactly the rows that are not in this basis (`strain_1_L1_36`,
   `strain_1_L1_37`, `strain_1_L1_10`). Restricted to the 85, both are
   internally consistent and need no repair.

## 3. Two changes this makes to the Methods

- **The production/control designation flips.** `METHODS_DRAFT` §2.12 called the
  A100 run "production" and this one "control". This is now the **reported**
  partition; the A100 run becomes the **cross-hardware reproducibility control**,
  which is a stronger use of it — the two agree to **0.46% median relative r/m**
  across the 82 units they share.
- **The r/m headline is 7.70 (n=47)**, the alignment-derived Gate 1 on this
  basis. Not 7.44 (that is the A100 run), not 7.38 (A100 under the Mash proxy),
  not 7.26 (this basis under the Mash proxy).

## 4. Files

| file | what |
|---|---|
| `FINAL_PARTITION.tsv` | `unit`, `sample_id` — 85 units, 2,340 genomes |
| `FINAL_PANEL.tsv` | 2,955 rows, with the membership/assignment split below |
| `MANIFEST.sha256` | checksums; the validator fails if either file is edited |

**`FINAL_PANEL.tsv` separates two meanings that were conflated.** The old
`subcluster` column carried a unit label for 615 genomes that are *not* members —
for `assign_only` genomes it is a nearest-unit label — so any join on it silently
picked up non-members. Now:

- `unit_membership` — set **only** for the 2,340 members. Join on this.
- `nearest_unit` — the old label, for non-members. Never a membership claim.
- `basis_role` — `analysis` (2,340) or `assign_only` (615).

Four genomes were re-roled `analysis` → `assign_only`: `GCF_014712825_1_Laos`,
`GCF_014712875_1_Laos`, `GCF_014712915_1_Laos`, `GCF_014712935_1_Laos`. They are
the remnant of `strain_1_L1_10`, which fell 7 → 4 after the duplicate drops and
was removed as a unit for falling below the n ≥ 5 floor.

## 5. Rules

1. **Take membership from `FINAL_PARTITION.tsv`.** Never by globbing
   `L1v4c_out/Clusters` (hybrid, 88 dirs) or `cfml/` (95 v4c-shaped units
   accumulated across partition generations).
2. **Join the panel on `unit_membership`, never on `subcluster`.**
3. **Run the validator before quoting a number.**
4. If the partition ever must change, change it here and re-run everything in
   §6 of `DOWNSTREAM_IMPACT_2026-08-22.md`. Do not patch a downstream table.
