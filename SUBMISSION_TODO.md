# Submission to-do

Started 2026-08-24. One list, ordered by what blocks what. Update in place; when
an item closes, mark it and name the artifact that closed it.

**Status of the science: no open analysis blockers.** D1 is complete: the reported headline reproduced (Gate 1 = 47 units, median r/m 7.70). Everything below is
deposition, archiving, administration, or verification of work already done.

---

## A. Unblocked — can be done today, nothing depends on them first

| # | item | notes |
|---|---|---|
| A1 | **Create the Zenodo (or equivalent) archive → DOI** | Contents specified in `DATA_AVAILABILITY_2026-08-24.md` §4: the frozen basis + its registers, the derived tables, the twelve scripts, the run pin's four inputs, and `L1v4c_TREES_SUPPORTED_FCONST/`. **Publish the FCONST tree set, not `L1v4c_TREES_SUPPORTED/`.** |
| A2 | **Tag the pipeline at `79ab645`** | So the data availability statement cites a release rather than a bare SHA. `wf-assembly-snps-mod`, branch `main`. |
| A3 | **Pin the A100 control's command line** | Must be read off the A100 host's `.nextflow.log`; it is not in this working directory. `PRODUCTION_RUN_PIN_2026-08-24.md` §7. If it cannot be recovered, say so in the Methods rather than reconstructing it. |
| A4 | **Verify or drop the control's Nextflow version** | §2.12.13 claims 25.10.0 for the A100 run, carried over from an earlier draft and never checked. The reported run's 25.04.6 *is* verified. |

## B. Deposition — chains off a BioProject registration

| # | item | blocker |
|---|---|---|
| B1 | **Register a BioProject** for the newly reported isolates | none — this is the head of the chain |
| B2 | **Deposit the 312 in-house assemblies** (259 `IP-`, 53 `IE-`) | B1. All 312 currently carry `bioproject = unknown` or blank |
| B3 | **Deposit raw reads for the 312**, if retained | B1 + confirm from the lab record what still exists |
| B4 | **Deposit or attach the 216 assemblies built here from public reads** | B1. The *reads* are already public under their own run accessions; our assemblies are derived data |
| B5 | **Build Supplementary Table S1** — per-genome accessions for all 2,959 | B2–B4. ⚠ Build it the way `generate_numbers.py` builds the panel. **Do not build it from `PANEL_v4d_2026-08-21.tsv`, which holds 2,955 rows** |
| B6 | **Fill the placeholders** in the data availability statement | B1–B5 + C1 |

## C. External — nobody in this repository can close these

| # | item | who |
|---|---|---|
| C1 | **IRB / ethics approval number** for the clinical isolates | the lab record. *The single hardest-blocked item in the project* |
| C2 | Confirm the 11 lab-stock (non-case) isolates are correctly flagged | lab record; they are already flagged in the metadata, this is a confirmation |
| C3 | **Obtain the DeepSANet PDF** (PMID 41185308) and read its splitting section | paywalled, no lawful free copy found; corresponding authors in `CITATION_AUDIT_2026-08-23.md` §5.2.3. **Not a blocker** — the rebuttal stands on the released code |

## D. Verification — do before submission

| # | item | notes |
|---|---|---|
| D1 | ✅ **DONE 2026-08-25 23:34**, rc=0, 6h37m | **The headline reproduces exactly: Gate 1 = 47 units, median r/m = 7.70.** Landed on 86 units / 2,352 genomes / **171** replicon-units against an expected 172; the missing one is the known zero-seed bug (`GUBBINS_CLUSTER strain_1_L1_30__GCF_000755905_1_2`, iteration 5 drew `-p 0`, error **ignored** by `errorStrategy`, so rc=0 is not evidence of success). 84 comparable units: **81 identical in r/m and raw SNP counts**, 3 shifted (`strain_1_L1_26` 0.694x, `strain_14_L1_4` 0.947x, `strain_1_L1_8` 0.992x). ⚠ **`REPRO_2026-08-24_out/Clusters` holds 172 Gubbins outputs but the r/m table counts 171**, because the failed unit kept its pre-pause Aug-24 publish output. Do not glob it; see the memory note. **Gate 1 gap CLOSED 2026-08-26**: distances recomputed from the repro alignments over a clean 171-unit tree (`REPRO_DISTANCES_v4c_SUMMARY.tsv`). Per-unit `raw_mean` reproduces **exactly** for 85 of 86 units (ratio 1.0000). Excluding the zero-seed casualty, Gate 1 = **47 units, median 7.70**, matching the reported figure. Naively the independent run reads 48 / 7.48, because Gate 1 *sums* `raw_mean` across replicons and `strain_1_L1_30` lost one, halving 6629.2 to 3317.9 and dropping it under the 4700 ceiling: an artifact of the lost replicon, not a membership finding. ⚠ The pin `79ab645` (2026-08-16) **predates the 08-19 `gubbins_seed` fix**, so the reported analysis is not seed-reproducible by construction. ⚠ `recomb_filtered_distances_bp.py` hardcodes the reported r/m at line 209, so `unit_rm`/`expected_ratio_from_rm`/`ratio_over_expected` in the new summary are hybrid columns; do not read them |
| D2 | **Re-run the contiguity-matched accessory pool at n=46** | The only accessory figure still at n=43 (country 30%→23%, region 79%→74%). Flagged in place in `ACCESSORY_ATTRIBUTION_RESULT_2026-08-21.md` §4. Directional support, not a headline |
| D3 | **Batched register refresh** | Register the same-patient Viet Nam pair in `OUTBREAK_GROUPS.tsv` (a no-op for current numbers, which is exactly why it should be deliberate), and decide whether to drop the four retired genomes from the cgMLST pool. The Georgia same-patient pair needs **no** entry — none of those five genomes is in the validation set |
| D4 | **Adopt the graded R6 verdict** | `BIOPROJECT_WITHIN_COUNTRY_RESULT_2026-08-24.md` §5. No headline moves — every reported R6 count is a *pass* and no pass changes. What changes is the description of the 14 discarded units, of which only 2 have FDR-confirmed batch structure and 4 have none |

## E. Tech debt — not blocking, worth doing

| # | item |
|---|---|
| E0 | `phylogeography_association_bp.py` defaults `--trees` to `L1_out/Clusters`, which was archived to TB1 on 2026-08-24 — it now fails loudly rather than silently scoring v1 trees. Repoint the default or drop it. `TB1_ARCHIVE_REGISTER.md` |
| E1 | `gate1_from_alignment_bp.py` still defaults `--mash` to `trackA_diversity_86units.tsv` — note **86**, an older partition |
| E2 | Four scorers each rebuild their own pool and each re-implement leave-outbreak-out. `abstention_rule_bp.py` is the precedent for not adding a fifth (it consumes `GROUPING_PREDICTIONS.tsv`); the MLST re-run followed it by reshaping input instead |
| E3 | "Pearson 2020" remains **unciteable** — two conflicting PMIDs, one a materials-chemistry paper. Remove it or replace it |

---

## Closed

| item | closed by |
|---|---|
| Figure 1 flow diagram | `make_figure1_bp.py` → `FIGURE1_STUDY_FLOW.svg` |
| MLST row of Table 5 on n=46 | `MLST_TABLE5_RERUN_2026-08-23.md` — became a bound, not an accuracy |
| Accessory sub-numbers at n=43 | all four controls + headline + leave-two-out re-run at n=46 |
| R7 Georgia second focus | already drafted; figures re-verified 2026-08-24 |
| Production/control designation | `RUN_DESIGNATION_CORRECTION_2026-08-23.md` |
| Pin the production command line | `PRODUCTION_RUN_PIN_2026-08-24.md` |
| Data availability statement (writing) | `DATA_AVAILABILITY_2026-08-24.md` §1 |
| `+ASC` vs `-fconst` | `ASC_FCONST_RESULT_2026-08-23.md` — changes no reported number |
