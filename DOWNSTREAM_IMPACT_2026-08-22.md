# Downstream impact of the basis freeze

2026-08-22. Every partition-dependent artifact, checked against the frozen basis
(`FINAL_BASIS_2026-08-22/`, 85 units, 2,340 genomes).

**Nothing reverses. Two headline numbers move, one conclusion is unchanged but
needs its numbers regenerated, and eight artifacts are superseded or must be
restricted.**

---

## 1. Conclusions that survive unchanged

| result | status |
|---|---|
| **ν hypothesis refuted** | **survives** — see §2 |
| Country attribution fails; region ~89% (was 93% pre-Track-0) | **unaffected by the freeze** — cgMLST-based; region moved only because Track 0 added testable North America |
| Accessory attribution fails its controls | **unaffected** — same reason |
| Phylogeography: 46 significant unit-variable tests | **unaffected** — see §3 |
| cgMLST vs SNP concordance | **recomputed: +0.861** — see §4 |

The entire attribution programme — the paper's spine — never used the partition.
`CGMLST_LICHT_ATTRIBUTION.tsv` scores 46 validation genomes of which 19 are not
in the frozen partition at all, exactly as it should be.

## 2. ν refutation — survives, numbers move in the third decimal

Recomputed on the frozen basis (drops `strain_1_L1_10`, uses the re-derived r/m
for `strain_1_L1_8`, `strain_1_L1_26`, `strain_14_L1_4`):

| | as published (n=86) | frozen basis (n=85) |
|---|---|---|
| ν vs Gubbins r/m, chr1 | −0.286 (p=0.0077) | **−0.274 (p=0.0112)** |
| ν vs Gubbins r/m, chr2 | −0.367 (p=0.0005) | **−0.346 (p=0.0012)** |
| ν vs δ, chr1 / chr2 | −0.791 / −0.785 | **−0.786 / −0.778** |

Still negative, still significant, still opposite to the prediction. **The
refutation stands.** `NU_HYPOTHESIS.tsv` must be regenerated on the frozen basis
and `NU_HYPOTHESIS_RESULT_2026-08-21.md` updated — the script rewrites the TSV
but **not** the prose, so the .md goes stale unless edited by hand.

## 3. Phylogeography — unaffected

`strain_1_L1_10` carried `verdict = "uninformative: <2 distinct values"` with an
empty p-value, so it never contributed. **46 of 172 unit-variable tests
significant, on the full table and on the frozen basis alike.**

## 4. Two tables become correct by restriction, not repair

`DISTANCES_v4c_SUMMARY.tsv` and `CGMLST_CONCORDANCE.tsv` were built by globbing
the hybrid `L1v4c_out/Clusters`. Their contamination is **exactly** the three
rows absent from the frozen basis — `strain_1_L1_36`, `strain_1_L1_37`,
`strain_1_L1_10`. Restricted to the 85, every remaining row carries this basis's
membership.

**Action: restrict on read; do not rebuild.**

`CGMLST_CONCORDANCE` has been **recomputed** on the frozen basis
(`concordance_frozen_bp.py` → `CGMLST_CONCORDANCE_FROZEN.tsv`), restricting both
the unit set *and* the taxa within each unit to frozen membership:

| | units | median r | r ≥ 0.7 |
|---|---|---|---|
| **Lichtenegger v1.1 — the scheme now used** | **85** | **+0.861** | 66/85 |
| PubMLST scheme 2 — what the filed figure used | 85 | +0.865 | 69/85 |
| *filed value, PubMLST over 88 hybrid units* | *88* | *+0.846* | *69/88* |

**Quote +0.861.** Two things had been conflated in the filed number: it was on
the hybrid 88-unit set *and* on the superseded PubMLST scheme. Separating them,
0.846 → 0.865 is the basis correction and 0.865 → 0.861 is the scheme. The two
schemes differ by a median of **0.0005** per unit, which is a further
scheme-robustness result in line with `SCHEME_CONCORDANCE_2026-08-21.md`.

Three unit files were skipped as off-basis: `strain_1_L1_10`,
`strain_1_L1_36`, `strain_1_L1_37`.

## 5. Superseded — A100-keyed, do not quote against the frozen basis

`PHYLOGEOGRAPHY_ASSOCIATION_v4c_A100.tsv`, `SCALE_country_raw.tsv`,
`SCALE_country_norm.tsv`, `SCALE_region.tsv`, `SCALE_subnational.tsv`,
`trackA_diversity_88units.tsv`, `GATE1_ALIGNMENT_A100_2026-08-21.tsv`.

All carry `strain_1_L1_36` / `strain_1_L1_37` / `strain_1_L1_10`. They remain
valid **as the A100 reproducibility control** and should be labelled that way,
not deleted.

✅ **The `SCALE_*` caveat is resolved, not carried forward.** `grouping_test_bp.py`
reads cgMLST profiles, the panel, `EXPOSURE_OVERRIDES` and `assign_region.tsv` —
**no `SCALE_*` file**. Re-run after retirement it reproduces the ladder exactly:

| grouping (modal k=20) | acc | baseline | kappa |
|---|---|---|---|
| Asia vs non-Asia | 100% | 59% | **1.000** |
| East vs West hemisphere | 96% | 63% | **0.909** |
| region, 7-way | 89% | 46% | **0.832** |
| SEA vs non-SEA | 76% | 59% | 0.461 |
| country | 15% | 26% | 0.132 |

The granularity ladder is partition-independent and unaffected by the freeze.
(Country is quoted at 22% / κ=0.193 in the results because country's best
estimator is nearest neighbour, not modal k=20 — name the estimator.) **Numbers
are the Track 0 integrated set, n=46 (2026-08-23); the pre-integration values
were 93%/κ0.890 region, 21%/κ0.188 country — `TRACK0_INTEGRATION_2026-08-23.md`.**

## 6. Must not be trusted for unit membership

`MLST_v4c.tsv` and `CGMLST_QC.tsv` each carry **179 distinct unit labels** —
labels accumulated across partition generations, 94 of which are not in the
frozen basis. Their per-genome content (ST, call rate) is fine; **their `unit`
column is not.** Join to `FINAL_PANEL.tsv` on `unit_membership` instead.

`cfml/` has the same problem: 95 v4c-shaped units across generations, plus an
abbreviated `sN_L1_M` naming convention. `NU_HYPOTHESIS` is unaffected because
`nu_hypothesis_bp.py` intersects with the r/m table, which is on-basis.

## 7. Already on basis

`GATE1_ALIGNMENT_2026-08-21.tsv` (85 units), `L1v4c_out/Summaries/recombination_rm.tsv`
(85), `NUMBERS.tsv`, `FINAL_PARTITION.tsv`, `FINAL_PANEL.tsv`.

## 8. The r/m headline: 7.70

Freezing on this basis settles a number that has moved four times. For the
record, every value and what it is:

| value | what it is |
|---|---|
| **7.70 (n=47)** | **the reported figure** — frozen basis, alignment-derived Gate 1 |
| 7.44 (n=48) | A100 run, alignment-derived Gate 1 — now the reproducibility control |
| 7.38 (n=47) | A100 run under the Mash proxy — what the 08-19 documents quote |
| 7.26 (n=47) | frozen basis under the Mash proxy — superseded by the unit-system fix |

`generate_numbers.py` already emits **7.70**. `METHODS_DRAFT` §2.12.7 was set to
7.44 on 2026-08-21 and **has been corrected back to 7.70**, with the
production/control designation flipped to match.

**None of these is a data change. All four are the same r/m values under
different partitions and different diversity metrics.** That is precisely why
the basis had to be frozen.
