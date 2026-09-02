# Does BioProject structure the tree within a country? — the conditional test

2026-08-24. Tests whether R6's BioProject control over-controls. **The answer is
partly yes, and the split is not where I expected it.**

`bioproject_within_country_bp.py` → `BIOPROJECT_WITHIN_COUNTRY_2026-08-24.tsv`

---

## 1. Why the test was needed

R6's BioProject control is a **discriminant, not an adjustment**: a unit is
reported only if geography clusters on the tree *and* BioProject does not. At
national scale that discards **14 of the 26** units in which country signal is
detectable.

That rule is only valid if the two labels are separable. In this panel they
largely are not:

- **113 of 119 BioProjects (95%) are entirely single-country**, covering 81.4% of
  the analysed genomes that carry both labels.
- Among **near-clonal pairs** (closest decile within a unit), 48.4% share a
  BioProject and **48.0% share both** — so ~99% of same-BioProject pairs are also
  same-country.

So a genuine within-country clonal expansion deposited by a single study makes
**both** variables fire on the **same clade**. "Confounded" is then the automatic
verdict, whether or not anything artefactual is present.

## 2. Method

Same statistic as `phylogeography_association_bp.py` — its functions are
`exec`-imported rather than reimplemented, so Fitch small-parsimony, the
permutation scheme, BH FDR and the seed (20260815) are identical. Two changes:

- **State = BioProject, assigned only to the tips of the country under test**;
  every other tip is set to `None`. Fitch treats `None` as fully ambiguous and it
  never forces a change, so scoring the full topology with the rest masked is
  exactly equivalent to scoring the induced subtree — no pruning code to get
  wrong.
- **The permutation shuffles BioProject labels among that country's tips only**,
  so topology and label composition are preserved and **geography is held fixed
  by construction**.

A `(unit, country)` cell is tested only with **≥ 8 genomes carrying a BioProject
and ≥ 2 distinct BioProjects** — the same anti-vacuity discipline the R6
interpretation document requires. 1,000 permutations.

## 3. Result

| | confounded units (R6 discarded) | country-only units (R6 kept) |
|---|---|---|
| units | 14 (12 with a testable cell) | 12 (8 with a testable cell) |
| testable `(unit, country)` cells | 22 | 8 |
| median cell size / distinct BioProjects | 18 / 4 | **33 / 4** |
| **significant at p ≤ 0.05** | **8 / 22** | **0 / 8** |
| chance expectation | 1.1 | 0.4 |
| binomial P(X ≥ observed) | **6.6 × 10⁻⁶** | 1.00 |
| **surviving BH FDR 5%** | **2 / 22** | 0 / 8 |

Cells with within-country batch structure, in p order:

| unit | country | n | BioProjects | p | q |
|---|---|---|---|---|---|
| `strain_1_L1_29` | Thailand | 33 | 5 | 0.0020 | **0.0330** |
| `strain_1_L1_35` | Thailand | 35 | 7 | 0.0030 | **0.0330** |
| `strain_1_L1_15` | Viet Nam | 18 | 3 | 0.0130 | 0.0917 |
| `strain_2_L1_6` | Thailand | 129 | 7 | 0.0200 | 0.0917 |
| `strain_1_L1_26` | China | 100 | 5 | 0.0230 | 0.0917 |
| `strain_2_L1_10` | Thailand | 17 | 4 | 0.0250 | 0.0917 |
| `strain_1_L1_12` | Thailand | 22 | 4 | 0.0360 | 0.1131 |
| `strain_4_L1_4` | USA | 13 | 4 | 0.0450 | 0.1237 |

Per unit, of the 12 testable confounded units:

- **8 show batch structure at nominal p**, **2 survive FDR**
  (`strain_1_L1_29`, `strain_1_L1_35` — both Thailand).
- **4 show none at all**: `strain_1_L1_7`, `strain_1_L1_8`, `strain_1_L1_22`,
  `strain_1_L1_34`.
- 2 further units are untestable (`strain_1_L1_17`, `strain_3_L1_6`) — no country
  reaches 8 genomes with ≥ 2 BioProjects.

## 4. What this licenses, and what it does not

**Real batch structure exists, and the aggregate evidence is strong.** Eight
significant cells against a chance expectation of 1.1 is P = 6.6 × 10⁻⁶. **The
hypothesis that BioProject clustering is *purely* country clustering in disguise
is refuted.** Batch structure is concentrated in Thailand (5 of 8 cells), which
is where the panel is deepest and studies are most numerous.

**But it is not demonstrable in most of the discarded units.** Only 2 of 12
survive FDR, and 4 show nothing whatever. Those units were discarded on the
strength of the nesting, not on evidence of an artefact.

**The comparison group is the reassuring half, and it is not underpowered.**
Zero of 8 cells in the units R6 *kept* show within-country batch structure —
with **larger** cells than the confounded group (median n = 33 vs 18) and the
same number of distinct BioProjects. So R6's *passes* are not concealing batch
effects. That is worth stating in the paper: the control's positive findings
survive the conditional test.

**What a null does not prove.** Finding no within-country batch structure removes
one alternative explanation; it does not establish that the unit's country signal
is real. A unit can be free of batch effects and still have no geography.

## 5. Recommendation for R6

Do not restore the 14 units, and do not leave them as a flat discard either.
**Replace the binary verdict with a graded one:**

| current | proposed | n units |
|---|---|---|
| confounded | **confounded — batch structure confirmed within country** | 2 (FDR), 8 (nominal) |
| confounded | **not separable — no batch structure detected, but geography unproven** | 4 |
| confounded | **not separable — untestable** | 2 |

The middle row is the honest description of a unit where BioProject and country
cannot be told apart *and* the study-effect explanation found no support. It is
weaker than a pass and stronger than a discard, and it is the category the
current rule collapses away.

**This does not change any headline.** R6's reported counts (national 6 of 48,
regional 1 of 17, sub-national 1 of 81) are all *passes*, and no pass moves. What
changes is the description of the discarded set — currently implied to be
artefact, when for at least a third of it the artefact explanation was tested and
not found.

## 6. Caveat carried from the design

The test conditions on country, so it inherits the panel's country imbalance.
Thailand supplies 9 of 22 testable cells and 5 of 8 significant ones. A batch
effect detectable only where sampling is deepest may exist elsewhere and be
invisible for want of power — the four "no batch structure" units have a median
cell size of 18. **Read this as "not demonstrable here", not "absent".**

## 7. Reproduce

```bash
python3 bioproject_within_country_bp.py
```

Deterministic under seed 20260815. The script **refuses** to write the canonical
output with `--perms < 1000` — a `--perms 1` coverage check overwrote the real
table once on 2026-08-24 before that guard existed.
