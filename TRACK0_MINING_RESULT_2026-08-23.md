# Track 0 — metadata mining, first pass

2026-08-23. Executes the free half of the validation-power acquisition
(`ACQUISITION_SCOPE_VALIDATION_POWER_2026-08-22.md`): attach published exposure
evidence to panel genomes already held, turning tier-C references into tier-B
validation genomes at zero sequencing cost.

**Outcome: 3 exposures verified against publications, 1 clean and ready, 2
verified-but-blocked on a leave-outbreak-out requirement that this pass surfaced.
Staged, not integrated — integration is a deliberate batched step, for the reason
in §4.**

Per-isolate findings are in the gitignored `TRACK0_VERIFIED_EXPOSURES_2026-08-23.tsv`.

---

## 1. Method

95 panel genomes from non-endemic countries (52 US, plus European and others),
not already validation, grouped into 31 BioProjects. Each BioProject triaged by
its ENA study title, then the promising ones verified against their publication
via PubMed and against per-sample ENA/NCBI metadata. **An exposure was recorded
only where a specific publication explicitly states it for that isolate, with a
PMID** — no inference from title or country.

## 2. Verified (with citation)

According to PubMed:

- **`GCF_001611585_1_Portugal_Lisbon` → Thailand.** Pelerito et al. 2016,
  *IDCases*, PMID 26962474, [DOI](https://doi.org/10.1016/j.idcr.2016.01.004):
  "the first case of imported melioidosis in Portugal," with "a recent patient's
  travel to Thailand." The travel history is independent of genomics. **Clean and
  ready** — single isolate, no sibling in the panel; scored, its nearest neighbour
  is a genuine Thai genome at d = 0.020 and it attributes correctly to Thailand at
  both scales.
- **`GCF_035776835_1` (MS2020a) and `GCF_035776895_1` (MS2022a) → USA.** Petras
  et al. 2023, *NEJM* 389:2355, PMID 38118023,
  [DOI](https://doi.org/10.1056/NEJMoa2306448): "Locally Acquired Melioidosis
  Linked to Environment — Mississippi," local acquisition confirmed by an
  environmental source found on-property; CDC declared the pathogen endemic in the
  continental US (Torres 2023, PMID 37619236,
  [DOI](https://doi.org/10.1371/journal.pntd.0011550)). Both are clinical blood
  isolates, autochthonous US origin. **Verified but blocked — see §3.**

These would fill the **North America n = 0** gap in the validation set — the
Mississippi strain is a "Western Hemisphere" lineage, so it is a genuinely
informative test (a US-origin genome that attribution will likely misplace to
Latin America).

## 3. The blocker this pass surfaced: leave-outbreak-out

Registering the two Mississippi clinical cases and scoring them gave USA **2/2 at
country** — which is a **leak, not a success.** Their nearest neighbours sit at
d ≈ 0.005 — the same-strain Mississippi *environmental* isolates
(`SRR30648677`, `SRR30648667`) that remain in the reference pool. It is the exact
failure mode the BioProject audit caught with the aromatherapy isolate: a
validation genome with a near-clone of itself in the pool leaks through
leave-group-out.

The Mississippi outbreak deposited ≥5 same-Western-Hemisphere-strain isolates
(2 clinical + 3 environmental, all `PRJNA942243`). Scoring any of them honestly
requires holding out **all** of them — leave-*outbreak*-out, not just
leave-exposure-country-out. That is a scorer change, and it must not be rushed
into the frozen basis at the end of a session. **The Mississippi cases are
verified and queued behind it.**

## 4. Why staged, not integrated

The clean Portugal genome alone moves a load-bearing number: it is a close
relative (d = 0.020, the d < 0.05 stratum) that country attribution gets *right*,
so it takes the paper's strongest anti-country result — country 1/13 where a
close relative exists — to **2/14**. That is a real, defensible improvement, but
propagating one genome from an unfinished batch through the whole corpus is the
piecemeal drift this session's discipline exists to prevent.

So Track 0 is treated like the partition freeze: **the register
(`EXPOSURE_OVERRIDES.tsv`) is a frozen input, and changing it triggers a
deliberate refresh** — regenerate the attribution result, recompute the strata,
propagate n across the docs — done **once, when the batch is assembled**, not per
genome. Until then the live files are unchanged (register 11 rows, attribution
n = 43; `--validate` PASS), and the verified evidence waits in the staging file.

## 5. Excluded, with reason

- **`PRJNA782614` (Texas)** — *Macaca fascicularis* wound/abscess isolates
  (imported macaques). No publication or ENA field states the primates' origin
  country, so exposure is unverifiable. Also animal, not human, cases.
- **`PRJNA486512` (UK: London, Salisbury ×2, Exeter)** — the study is
  "re-sequencing of **laboratory stocks**"; Salisbury is Porton Down. Reference
  strains, not cases. Consistent with the known lab-stock caveat.

## 6. What remains

~24 BioProjects were triaged by title but not yet deep-verified — the Gee 2017
"Western Hemisphere" set (`PRJNA352974`, 12 genomes, some with possible travel
history), several single-genome US/European case reports, and the environmental
USVI/Caribbean isolates. Each needs the same publication-level verification. This
is the long tail of Track 0 and can be worked incrementally; the yield per
BioProject is 0–1 validation genomes.

## 7. Next actions

1. **Implement leave-outbreak-out** (hold out same-outbreak / same-strain isolates
   when scoring a validation genome), then integrate the Mississippi cases. This
   also retro-hardens the aromatherapy and any future cluster-derived validation
   genome.
2. **Batch-integrate** the verified Track 0 genomes (Portugal + Mississippi +
   whatever the long tail yields) in one deliberate refresh: register → regenerate
   attribution → recompute strata → propagate n. Expect country-with-relative to
   move from 1/13 (Portugal is a genuine +1; Mississippi will likely be a
   misattribution, strengthening the ceiling claim for North America).
3. Work the ~24 remaining BioProjects incrementally.
