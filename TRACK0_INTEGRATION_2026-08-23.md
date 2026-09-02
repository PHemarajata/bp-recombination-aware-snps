# Track 0 integration — validation set 43 → 46

2026-08-23. The deliberate batched refresh: the verified Track 0 genomes are
registered, every attribution analysis re-run, and the numbers propagated. This
is the single authoritative before→after for the change; `NUMBERS.tsv` is
regenerated and remains the source of truth.

## What integrated

Three validation genomes, from `TRACK0_VERIFIED_EXPOSURES_2026-08-23.tsv`:

| genome | exposure | evidence | scored result |
|---|---|---|---|
| `GCF_001611585_1_Portugal_Lisbon` | Thailand | Pelerito 2016 IDCases PMID 26962474 (documented travel) | **correct**, d=0.020, a genuine close-relative country hit |
| `GCF_035776835_1` (MS2020a) | USA | Petras 2023 NEJM PMID 38118023 (autochthonous) | → Colombia / Latin America, d=0.15 |
| `GCF_035776895_1` (MS2022a) | USA | same source, same strain | → Colombia / Latin America, d=0.15 |

The two Mississippi cases are scored with the `MS_gulf_coast_2020` outbreak group
(21 isolates) held out, so the d=0.15 result is genuine, not the d=0.005 leak.
They are one Western Hemisphere lineage represented by two clinical isolates.

## Headline numbers, before → after

Scorable validation genomes **43 → 46** (present 45 → 48; 2 remain unattributable).

| figure | before (n=43) | after (n=46) |
|---|---|---|
| **country**, nearest neighbour | 9/43 (21%) | **10/46 (22%)** |
| country, modal k=20 | 6/43 (14%) | **7/46 (15%)** |
| country baseline (majority) | 12/43 (28%) | **12/46 (26%)** |
| **country, d < 0.05** (close relative) | 1/13 | **2/14** |
| country, 0.05–0.30 | 2/8 | **2/10** |
| country, d ≥ 0.30 | 6/22 | **6/22** |
| **region**, modal k=20 | 40/43 (93%) | **41/46 (89%)** |
| region, nearest neighbour | 36/43 (84%) | **37/46 (80%)** |
| region baseline | 20/43 (47%) | **21/46 (46%)** |
| region, d < 0.05 | 11/13 | **11/14** |

### Granularity ladder (kappa, modal k=20)

| grouping | before κ | after κ | after acc |
|---|---|---|---|
| **Asia vs non-Asia** | 1.000 | **1.000** | 100% |
| East vs West hemisphere | 0.901 | **0.909** | 96% |
| **region, 7-way** | 0.890 | **0.832** | 89% |
| SEA vs non-SEA | 0.425 | **0.461** | 76% |
| country | 0.188 | **0.132** | 15% |

### Other attribution analyses, re-run on the integrated set

- **Accessory** country NN 13/43 (30%) → **14/46 (30%)** — the "looks positive,
  fails its controls" story is intact.
- **Downsampling control** region κ (modal k=20): full-panel 0.89 → **0.83**,
  most-rebalanced (EAP capped at 30) 0.81 → **0.77**. The W2 conclusion holds —
  region survives a 90× rebalancing; it is not a panel-imbalance artifact.
- **Resolution curve** — unaffected. Its validation set is the
  `travel_reattributed` metadata set, which does not include the EXPOSURE_OVERRIDES
  genomes.
- **cgMLST↔SNP concordance, ν, freeze basis** — do not use the validation set;
  unchanged.

## What the change means, and why it is an improvement

Two things move the region headline down (93% → 89%), and both are gains, not
losses:

1. **North America is now testable (was n = 0).** The Mississippi autochthonous
   strain — a genome of *certain* US origin — misattributes to Latin America at
   both region and country. That is a controlled demonstration of the
   divergence-depth ceiling on a genome whose truth is not in doubt, and it is
   stronger evidence than any imported case.

2. **The same genome makes the depth thesis visible within one isolate.** The
   Mississippi case is **correct at the deep splits** (Asia vs non-Asia κ still
   1.000; East vs West hemisphere κ 0.909 — it is correctly Western) and **wrong
   at the shallow ones** (region 7-way, country). Legibility tracks divergence
   depth, shown in a single genome.

3. **Country, where a close relative exists, is now 2/14, not 1/13.** Portugal is
   a genuine success — an imported case whose Thai strain has a real Thai relative
   in the panel (d = 0.020). It slightly softens the "1/13" claim but with a real
   example of when country *can* work, which is more honest than the round
   number.

Report the region drop as *"89%, now including North America, where the sole
lineage misattributes"* — not as a regression.

## Provenance and mechanism

- `EXPOSURE_OVERRIDES.tsv`: +3 rows (Portugal, MS2020a, MS2022a).
- `OUTBREAK_GROUPS.tsv`: `MS_gulf_coast_2020`, 21 isolates, now active.
- Leave-outbreak-out is applied in all four validation-set scorers
  (`score_cgmlst_lichtenegger`, `score_accessory`, `grouping_test`,
  `downsample_control`) — each had its own pool-building and each needed it; the
  Mississippi leak surfaced in three of them in turn.
- Verified: `--validate` PASS, `freeze_basis` CONSISTENT, `generate_numbers` 40
  keys, all attribution scorers agree on region 89% / κ 0.832.

## Carried forward

- The Vietnam/Georgia lineage question (`LEAVE_OUTBREAK_OUT_2026-08-23.md` §6).
- The three Mississippi *environmental* isolates remain references, not validation
  genomes — a deliberate choice (same lineage as the clinical cases; adding them
  would pseudo-replicate).
- Duplicated pool-building across five scorers is fragile tech debt — a shared
  leave-group-out/outbreak helper would prevent the next scorer from silently
  leaking. Noted, not done.
