# Laboratory and collection period as batch proxies: an audit, then a test

**2026-09-02.** Prompted by the finding that BioProject is a poor batch proxy
here. Acceptance criteria were fixed **before** looking at any result:

1. **Coverage** -- usable for a large majority of the 2,340 analysis genomes
2. **Cardinality** -- not one value, not ~n values
3. **Unbiased missingness** -- missingness must not track country, or the proxy
   inherits BioProject's nesting problem
4. **Interpretability** -- the field must mean what its name claims

---

## 1. Laboratory: FAILS. There is no such field.

| candidate | coverage | distinct | verdict |
|---|---|---|---|
| `acquired_from` | 100% | 43 | **fails (4).** Values are *countries* -- Thailand=1561, China=265. Using it would literally re-control for country |
| `source_batch` | 100% | **3** | **fails (2) and (4).** Our own pipeline pass; 93% is one value (`v3_panel`) |
| `isolation_location` | **7%** | 50 | **fails (1)** |
| `country_source`, `origin_basis`, `origin_resolution` | 100% | 2-4 | **fails (4).** Our own metadata bookkeeping |
| `reference`, `ref_source` | 100% | 34, 2 | **fails (4).** Analysis artifacts, not metadata |

**No field in the panel encodes laboratory.** `acquired_from` is the trap: it
reads like a provenance field and is in fact a country field. A genuine
laboratory proxy would have to come from the archive (`center_name`,
`collected_by`), which is unfetched, and would be unavailable for the 276
in-house genomes regardless.

## 2. Collection period: PASSES on 1, 2, 4; FAILS on 3, but not where it matters

| criterion | result |
|---|---|
| coverage | **90%** (2,115 of 2,340) -- pass |
| cardinality | 342 dates, 1960-2025, 42 years -- pass |
| **unbiased missingness** | **FAIL globally**: Singapore **76%** missing, Australia **55%**, against Thailand 4%, USA 2% |
| interpretability | pass |

**The global failure does not land where the analysis happens.** Of the 18 units
that carry the geography claim (6 passing + 12 confounded), **16 have >= 60%
dated with >= 2 distinct years**; most are 85-100%. The two exceptions are named:
`strain_1_L1_5` (44% dated) and `strain_1_L1_7` (38%).

## 3. Period is much less nested inside country than BioProject

This is the specific defect period would fix, and it does:

| confounder | Cramer's V vs country | single-country groups |
|---|---|---|
| **BioProject** | **0.857** | 113/119 (**95%**) |
| collection year | **0.379** | 12/42 (29%) |
| 3-year bin | 0.419 | 5/21 (24%) |
| 5-year bin | 0.460 | 2/13 (15%) |

Period is **less than half** as associated with country. It is **not**
independent of it -- median dominant-country share per bin is 72-82% -- so period
has the same structural problem as BioProject, materially less severely.

## 4. The test, pre-specified

Both binnings were run (year, 3-year), 1,000 permutations, seed 20260815, and a
unit counts as period-confounded **only if both agree**. This was fixed before
the runs so a binning could not be chosen after seeing results.

| confounder used | geographic | confounded | vacuous |
|---|---|---|---|
| BioProject | 6 | 12 | 5 |
| collection year | 5 | 16 | 2 |
| 3-year bin | 4 | 18 | 2 |
| **year AND 3-year agreeing** | **3** | -- | -- |

**Period is the stricter control**, and the two binnings agree on all six
BioProject-passing units, so the result is not binning-sensitive where it counts:

| unit | BioProject control | period, year | period, 3-yr | both agree |
|---|---|---|---|---|
| `strain_11_L1_5` | pass | **pass** | **pass** | yes |
| `strain_1_L1_11` | pass | **pass** | **pass** | yes |
| `strain_1_L1_28` | pass | confounded | confounded | yes |
| `strain_2_L1_2` | pass | confounded | confounded | yes |
| `strain_5_L1_3` | pass | confounded | confounded | yes |
| `strain_1_L1_5` | pass | vacuous (44% dated) | vacuous | yes |

**Two units pass both the BioProject and the period control**: `strain_11_L1_5`
and `strain_1_L1_11`.

## 5. What I am NOT concluding, and why

**This is not "the real answer is 2."** Three reasons, stated because the
temptation to treat each new control as a tightening is exactly the error already
made once in this project.

1. **Conjunction gets stricter by construction.** Requiring a unit to pass every
   control ever applied is not a better estimator; it is a filter whose severity
   grows with the number of tests, each with its own false-positive rate.
2. **Period has the same structural flaw**, at V = 0.38 rather than 0.86. A unit
   sampled in one place over one period is period-coherent *and*
   country-coherent for legitimate reasons, so "period-confounded" is not
   automatically "not geographic".
3. **`strain_1_L1_11` is unstable across specifications**: it passes here, but
   it is one of the two marginal BioProject passes (p = 0.063) and it flips to
   confounded under the in-house synthetic-BioProject test. Its status depends on
   the specification, which is itself the finding for that unit.

**What is defensible** is the specification curve: the count runs 6 (BioProject),
5 (year), 4 (3-year), 3 (both period binnings), 2 (period and BioProject). It
never rises. And **`strain_11_L1_5` is the only unit that survives every
specification tried** -- BioProject p = 0.988 frozen, 0.894 under the synthetic
in-house project, and both period binnings.

## 6. Recommendation

- **Do not replace the BioProject control with period.** Report both. They fail
  differently, and a unit passing both is a stronger claim than a unit passing
  either.
- **Report the specification curve in the Methods**, not a single count. The
  honest summary is "between 2 and 6 units depending on the confounder, with one
  unit robust to every specification tested".
- **State that laboratory was sought and is unavailable.** That is a real
  limitation, not an omission, and `acquired_from` is a trap for the next person.
- **Do not add further controls hoping to converge.** Each additional filter
  lowers the count mechanically. The curve is the result.

---

## 7. Isolation source: a factor that touches r/m, but weakly

Checked because it is biologically meaningful rather than administrative, and
because it could act on the headline directly rather than only on geography.

**Availability.** `ISOLATION_SOURCE_2026-08-16.tsv` covers **86%** of the
analysis basis with four classes: clinical 1,674, environmental 285, animal 45,
laboratory 11. Missingness is biased (USA 55%, Laos 27%, against Thailand 8%).
Nesting vs country is **V = 0.578**, between BioProject (0.857) and collection
year (0.379). So it is a usable but country-entangled variable, and 83% of
genomes are one class, which limits within-unit contrast.

**Effect on r/m.** Across all 76 units with >= 5 classified genomes, non-clinical
share (environmental + animal) correlates with r/m at **r = -0.341**. That is
*not* a Gate 1 artifact: the 10 units that are >= 50% non-clinical split 4
in-window, 3 below, 3 above, and the correlation holds within every stratum
(in -0.226, below -0.339, above -0.394).

**But the effect on the headline is small:**

| within the Gate 1 window | n | median r/m |
|---|---|---|
| >= 25% non-clinical | **8** | 7.16 |
| < 25% non-clinical | 37 | 8.05 |
| all source-classified in-window | 45 | 7.78 |

Restricting the headline to clinical-dominated units moves it from 7.78 to 8.05,
about 3-4%, on a subgroup of **n = 8**. Consistent in direction, weak in
magnitude, and underpowered on the non-clinical side.

**Verdict: report it as checked and small.** Environmental and animal isolates
trend toward lower r/m, plausibly because soil populations are sampled differently
from patients, but the effect does not threaten the reported figure. This is a
negative result worth stating, because the alternative is a reviewer asking
whether source composition drives r/m and nobody having looked.

## 8. Factors examined, and what each does

| factor | available? | affects geography | affects r/m |
|---|---|---|---|
| **BioProject** | 82% | **decisive** -- 26 units to 6 | negligible (7.70 to 7.48) |
| **collection period** | 90% | **stricter still** -- 6 to 3 | not tested |
| **isolation source** | 86% | not tested as a confounder | **weak** (r = -0.34 overall, 3-4% on the headline) |
| **laboratory** | **absent** | -- | -- |

The pattern across every factor examined is the same: **geography is fragile to
specification and r/m is not.** That asymmetry is itself reportable, and it is
the strongest argument for the paper leading with the measurement result rather
than the geographic one.

---

## 9. Reference choice: a large apparent effect that does not survive checking

Tested because the project already knows the reference taxon's branch distorts
r/m, and because `ref_source` is a clean, fully covered binary (borrowed 58 units,
own 27).

**The headline number looks alarming:**

| in-window units | n | median r/m |
|---|---|---|
| all | 47 | **7.70** |
| borrowed reference | 35 | **8.05** |
| own reference | 12 | **6.71** |

A difference of 1.34, or **17% of the headline**, larger than any other factor
examined. At that point it looked like the most important thing found all day.

**It does not survive stratification.** Splitting the window at its median SNP
density:

| stratum | borrowed | own |
|---|---|---|
| lower half | 8.05 (n=17) | 6.40 (n=6) |
| upper half | 7.79 (n=18) | **8.90 (n=6)** |

**The effect reverses sign.** In the upper half of the window, own-reference
units score *higher*. At six units per cell this is noise, not a reference
effect.

Two further checks leave nothing to explain. Within the window the two groups are
**matched on diversity** (median 2,014.6 SNPs borrowed against 1,959.5 own), so
it is not a diversity artifact either, which was my first hypothesis for it. And
within the window neither SNP density (r = -0.104) nor unit size (r = +0.018)
predicts r/m.

The one real difference is that own-reference units are **much larger** (median
n = 47 against 14), which is unsurprising: a larger unit is likelier to contain a
suitable internal reference. That does not translate into an r/m effect.

**Verdict: not established.** The 17% figure rests on 12 units and reverses when
split. Reported here because it is exactly the kind of large, plausible,
mechanism-having number that would have survived into a manuscript unchallenged,
and because the check that killed it took one command.

**Also a metadata gap worth recording:** `ref_mean_mash` is empty for all 85
units in the frozen panel, so the continuous version of this test -- reference
divergence against r/m -- cannot be run at all. Only the binary own/borrowed
split is available.

## 10. Factor table, updated

| factor | available? | affects geography | affects r/m |
|---|---|---|---|
| **BioProject** | 82% | **decisive** but **over-adjusted** (26 to 6; correctly specified 18-24) | negligible, 7.70 to 7.48 |
| **collection period** | 90% | **stricter** (6 to 3) | not tested |
| **isolation source** | 86% | not tested | **weak but consistent**, 3-4% |
| **reference source** | 100% | not applicable | **apparent 17%, not established** -- reverses on stratification |
| **laboratory** | **absent** | -- | -- |
| **ref_mean_mash** | **empty** | -- | -- |

The asymmetry holds and is now better evidenced: **every factor that moves the
geographic count leaves r/m essentially where it was**, and the one factor that
appeared to move r/m substantially did not survive a stratified check.
