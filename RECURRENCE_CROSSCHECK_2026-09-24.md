# Our recurrence result against Yuyi's, 2026-09-10

**2026-09-24.** Cross-reference of `RESULTS_DRAFT_2026-08-23.md` §R3.1 against
`Burkholderia_pseudomallei_RECURRENCE_SERIES_260910.docx` and
`Result_recurrence_pairwise_260910.xlsx`.

**Headline: every structural number matches exactly, and the two are not
competing pipelines.** Yuyi's document states it was "built with the reported
pipeline's method", naming snippy per genome against the group medoid,
snippy-core retaining invariant sites, Gubbins 3.4.3 with RAxML at 5 iterations,
min-snps 3, invariant-site correction on, filter-percentage 25, then IQ-TREE
GTR+ASC with 1,000 ultrafast bootstrap and SH-aLRT replicates.

**This corrects something I wrote on 2026-09-24.** I checked the closeout deck,
found no mention of relapse or recurrence, and concluded there was no such
analysis. The deck genuinely has none. This work postdates it by a month, and
the conclusion was wrong.

---

## 1. Exact agreements

| | ours (§R3.1) | Yuyi, 2026-09-10 |
|---|---|---|
| patients | 13 | 13 in the pairwise sheet |
| episode pairs | 20 | 20 rows |
| isolates | 29 | 29 |
| classification | 19 relapse, 1 reinfection | 19 "Relapse", 1 "Reinfection" |
| the reinfection | patient 9 | patient 9 |
| patient 9, ancestor subtends | 35 other genomes | 35 other genomes |
| patient 9, nearer other patient | 81 SNPs against 1,102 | 81 SNPs against 1,102 |
| exclusive clades | 12 of 13 | 12 of 13 |
| relapse range | 1 to 14 SNPs | "every relapse pair sits between 1 and 14 SNPs" |
| thin margin | patient 8, 14 against 30 | patient 8, 14 against 30 |

The 20 and 29 reconcile the same way in both: eleven patients contribute one
pair each, patient 13 contributes three pairs from three episodes, and patient
14 contributes six from four.

## 2. What Yuyi's files add that we do not have

- **The environmental isolate is named.** Patient 8's 30-SNP neighbour is
  **`IE-0044`**. Ours says only "an environmental isolate from the same
  collection".
- **Patient 9's two isolates are different sequence types, ST70 and ST68.** Ours
  argues the reinfection from topology and distance alone. The ST difference is
  an independent line and it is free.
- **Per-pair dates, intervals and STs for all 20 pairs**, including intervals
  from 16 days to 395 days.
- **Gubbins was given an explicit seed, "which the pipeline omits".** That is
  the zero-seed bug this repository already tracks. Her run is seeded where the
  production run is not.

## 3. Three discrepancies to settle

**3.1 The clinical series is 14 cases, the genomic analysis is 13 patients.**
Sheet 2 is headed "Recurrent/Reinfection cases total 14 cases" and lists
**patient 11 (`IP-0253-5`, `IP-0272-5`)**, who has no row in the pairwise sheet.
Our §R3.1 says "thirteen patients in the Nakhon Phanom collection had
culture-confirmed recurrent melioidosis", which describes the analysed set, not
the clinical series. If the abstract or the paper ever says how many patients
had recurrent disease, 14 is the clinical number and 13 is the analysable one.

**3.2 Patient 12 has a third isolate that is not in the analysis.** Sheet 2
lists `IP-0264-2` as patient 12's third episode. The pairwise sheet has one row
for patient 12, covering episodes 1 and 2 only. With three episodes it would
contribute three pairs rather than one, so the totals would move from 20 to 22
and from 29 to 30.

**3.3 The patristic column is not convertible to SNPs by one factor, so the
two distance sets cannot be compared directly.** Patient 8 at 14 SNPs against a
patristic of 1.47e-4 implies roughly 95,000 sites. On that scale the reinfection
at 0.1153 would be about **10,981 SNPs, not 1,102**, and patient 14's widest
relapse pair at 2.02e-4 would be **19 SNPs, exceeding the stated maximum of 14**.

This is expected rather than alarming. Her document says each patient is "placed
against the local genomes it could plausibly be confused with", so every patient
has its own context alignment of its own length, and patristic distances are not
comparable across patients without those lengths. **It does mean the spreadsheet
cannot be used to verify our 1-to-14 range.** One pair, patient 13 episodes 1
and 3, carries a patristic of exactly **0**, which sits oddly beside a stated
floor of 1 SNP and is the clearest case where the two measurements need
reconciling in the same units.

## 4. One cross-link worth noticing

**`IP-0253` appears in both analyses and is absent from ours.** It is patient 11
in the recurrence series, the case missing from the pairwise sheet. It is also
the patient whose isolates are the two closest environmental matches in the
closeout deck, `IE-0019` at 0.000177 and `IE-0022` at 0.000216, the tightest
pairs in that whole comparison.

So the one recurrence case dropped from the genomic recurrence analysis is the
same patient carrying the strongest environmental match in the collection. That
may be coincidence. It is worth one look.

## 5. What this changes in the abstract

**Nothing in the submission text.** Every figure the abstract quotes agrees with
Yuyi's independent write-up. The recurrence sentence stands as written.

**One nuance for the talk.** "Our pipeline, their isolates" was accurate but
incomplete. Her analysis follows the same method on the same isolates and
reaches the same calls, which is a reproducibility result and worth a sentence
on a slide if the question comes up.

**The deck's tree is still the open one.** Its appendix says "whether
recombination was filtered before tree inference is not yet confirmed". That
warning applies to the deck's core-SNP tree, not to this recurrence work, which
is explicitly recombination-filtered.
