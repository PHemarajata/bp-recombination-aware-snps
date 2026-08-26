# Data availability — statement, and the deposition checklist behind it

2026-08-24. Closes the writing half of open item 2. **The depositions themselves
are not done** and cannot be done from here; §3 is the checklist, and the
statement in §1 contains bracketed placeholders that must be filled from the
deposition receipts before submission.

---

## 1. The statement (draft, for the manuscript)

> **Data availability.** The genome panel analysed in this study comprises
> **2,959** *Burkholderia pseudomallei* assemblies. **2,647 (89.5%) derive from
> public data**: 1,398 GenBank (`GCA_`) and 1,033 RefSeq (`GCF_`) assemblies
> downloaded from NCBI, and 216 assembled in this study from public short-read
> sets deposited in the ENA/SRA under their run accessions. Per-genome
> accessions, assembly source, country and collection date for all 2,959 are in
> **Supplementary Table S1**.
>
> The remaining **312 genomes (10.5%) are newly reported here**: 259 clinical
> (`IP-`) and 53 environmental (`IE-`) isolates from Nakhon Phanom Province,
> Thailand. Assemblies and, where available, raw reads have been deposited in
> **[ARCHIVE]** under BioProject **[PRJNAxxxxxxx]**; individual BioSample and
> assembly accessions are listed in Supplementary Table S1. **[Confirm before
> submission: 11 of these are laboratory reference stock rather than
> case-associated isolates and are flagged as such in Supplementary Table S1.]**
>
> The **frozen analysis basis** — the 85 lineage units and 2,340 genomes on
> which every reported figure is computed — is given as `FINAL_PARTITION.tsv`
> in **[REPOSITORY/DOI]**, together with the per-unit recombination estimates,
> the cgMLST allele calls, the attribution predictions and the validation-set
> exposure register. Every quantity quoted in the manuscript is regenerable from
> those files with the scripts below; the file `NUMBERS.tsv` maps each reported
> figure to the key and script that produce it.
>
> **Code availability.** The analysis pipeline is
> `wf-assembly-snps-mod` (https://github.com/PHemarajata/wf-assembly-snps-mod),
> and the reported run used release **`v1.0.5-mod`** (commit `79ab645`) on branch
> `main` under Nextflow 25.04.6. Note that the pipeline manifest at that release
> still self-reports `v1.0.3-mod`, so run logs carry that string; the manifest was
> never bumped and was deliberately left uncorrected so the reported commit
> remains citable as-is. That release **predates the addition of a Gubbins seed
> parameter**, so the analysis is not seed-reproducible: Gubbins draws RAxML's
> parsimony seed at random and, with the workflow's `errorStrategy 'ignore'`, a
> rejected draw silently drops one analysis unit while the run still exits zero.
> A re-execution should therefore be checked against per-unit task counts, not the
> exit code. An end-to-end re-run is reported in `REPRO_RESULT_2026-08-26.md`; it
> lost one unit this way and otherwise recovered the reported figures. The exact invocation, the four input files it consumed, and the
> resource-override configuration are given in Supplementary Methods and
> archived at **[DOI]**. Downstream analysis scripts (partition freezing and
> validation, attribution scoring, the grouping ladder, the abstention rule and
> figure generation) are archived at the same DOI.
>
> **Restrictions.** The clinical isolates were collected under
> **[IRB/ETHICS APPROVAL NUMBER]**; no patient-identifying information is
> included in any deposited record or supplementary file. Collection dates are
> reported to the year and geographic origin to the province, which is the
> resolution at which the analysis was performed.

## 2. Where each number comes from

Not decorative — the panel composition has been miscounted in this project
before, so it is recomputed rather than quoted:

| quantity | value | source |
|---|---|---|
| panel | **2,959** | `L1v4c_MERGED_METADATA.tsv` (2,976) − duplicates − **active** exclusions |
| GenBank `GCA_` | 1,398 | accession prefix over the corrected panel |
| RefSeq `GCF_` | 1,033 | " |
| public reads assembled here | 216 | " (`SRR`/`ERR`/`DRR` prefix) |
| in-house clinical `IP-` | 259 | " |
| in-house environmental `IE-` | 53 | " |
| public-derived subtotal | **2,647 (89.5%)** | `NUMBERS.tsv` `panel.public_derived` |
| in-house subtotal | **312 (10.5%)** | `NUMBERS.tsv` `panel.in_house` |

> ⚠ **Do not build Supplementary Table S1 from `PANEL_v4d_2026-08-21.tsv`.**
> That file holds **2,955** rows — it is a 2026-08-21 snapshot taken while four
> exclusions later retired as unevidenced (`ERR9980356`, `SRR2896257`,
> `SRR2896259`, `SRR2896271`) were still active. `NUMBERS.tsv` cited it as the
> source for the 2,959 figure until 2026-08-24, which named a file whose own row
> count contradicted the value; that attribution is now corrected. Build S1 the
> way `generate_numbers.py` builds the panel: metadata minus the duplicate
> register minus **`status != retired`** exclusions.

## 3. Deposition checklist — none of this is done

| # | item | state | blocker |
|---|---|---|---|
| 1 | **312 in-house assemblies** (259 `IP-`, 53 `IE-`) | ❌ not deposited | needs a BioProject; **no accession exists** — all 312 carry `bioproject = unknown` or blank in the metadata |
| 2 | Raw reads for the 312, if retained | ❌ unknown | confirm what exists from the lab record |
| 3 | **216 assemblies built here from public reads** | ❌ not deposited | the *reads* are already public under their own run accessions; our assemblies are derived data and should be deposited or attached to the archive in item 5 |
| 4 | **Supplementary Table S1** — per-genome accession table for all 2,959 | ❌ not written | needs items 1 and 3 to have accessions first |
| 5 | **Archive of the frozen basis + scripts** (Zenodo or equivalent) → DOI | ❌ not created | can be done now; does not depend on the others |
| 6 | **IRB / ethics approval number** | ❌ missing | **the lab record — this is the one item nobody in this repository can supply** |
| 7 | Pipeline commit tag/release at `79ab645` | ✅ **tagged 2026-08-26** | annotated tag **`v1.0.5-mod`** at `79ab645`, pushed to origin. Tag message records that the manifest self-reports `v1.0.3-mod` and that the commit predates the `gubbins_seed` fix, so runs from it are not seed-reproducible |

**Items 5 and 7 are unblocked and could be done today.** Items 1–4 chain off a
BioProject registration. Item 6 is external.

## 4. What must go into the archive (item 5)

The test is not "did we upload the results" but **"can a reader regenerate every
number in the paper"**. That means:

**The frozen basis** — `FINAL_BASIS_2026-08-22/` in full (`FINAL_PARTITION.tsv`,
`FINAL_PANEL.tsv`, `MANIFEST.sha256`, `README.md`), plus the registers that
define it: `PANEL_DUPLICATES_2026-08-21.tsv`, `PANEL_EXCLUSIONS.tsv` **with its
`status` column intact**, `EXPOSURE_OVERRIDES.tsv`, `OUTBREAK_GROUPS.tsv`.

**Derived tables** — `NUMBERS.tsv`, `GROUPING_LADDER.tsv`,
`GROUPING_PREDICTIONS.tsv`, `CGMLST_LICHT_ATTRIBUTION.tsv`,
`CGMLST_CONCORDANCE_FROZEN.tsv`, `DISTANCES_v4c_SUMMARY.tsv`,
`L1v4c_out/Summaries/recombination_rm.tsv`, the three
`PHYLOGEO_FROZEN_*_2026-08-23.tsv`, and the MLST and accessory outputs.

**Scripts** — `generate_numbers.py`, `freeze_basis_bp.py`,
`grouping_test_bp.py`, `score_cgmlst_lichtenegger.py`, `score_accessory_bp.py`,
`accessory_control_bp.py`, `abstention_rule_bp.py`, `gate1_from_alignment_bp.py`,
`mlst_to_allele_table_bp.py`, `reconstruct_v4c_samplesheet_bp.py`,
`make_figure1_bp.py`, `retire_exclusions_bp.py`.

**The run pin** — the four input files in `PRODUCTION_RUN_PIN_2026-08-24.md` §8,
including the reconstructed samplesheet **under its RECONSTRUCTED name**, and
the run's `pipeline_info/` (trace, report, `software_versions.yml`).

**Trees** — `L1v4c_TREES_SUPPORTED_FCONST/` (170 trees). **Publish this set, not
`L1v4c_TREES_SUPPORTED/`**, which is the superseded `+ASC` set retained only for
comparison.

## 5. Two things a reviewer will ask, that the statement should not dodge

**"Why 2,959 in the panel but 2,340 analysed?"** Because 619 genomes fell in
units below the n ≥ 7 floor or were removed by the corrections in §2.12.5. The
statement above deliberately gives both numbers and names the file that defines
the smaller one, rather than quoting only the larger.

**"The samplesheet is reconstructed?"** Yes, and it says so. The honest position
is that the input *set* is corroborated by two independent artifacts that agree
exactly (2,352 both ways) while the row *order* is not recoverable — and that
order cannot affect the result. Reviewers forgive a disclosed reconstruction;
they do not forgive discovering one.
