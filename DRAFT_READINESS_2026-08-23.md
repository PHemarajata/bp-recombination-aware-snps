# Are we ready to draft? — assessment, 2026-08-23

Scope: can Paper 1 (A+D fused — the limits/capability paper) be drafted now,
Methods and Results in particular. Assessed by reading the artifacts, not the
summaries.

> **Verdict: draft the Results now. Do not draft the Methods yet.**
>
> The Results outline is in good shape — internally consistent, every figure
> tied to a regenerable key, all major weak spots resolved or bounded.
> **`METHODS_DRAFT_2026-08-19.md` is not**: its "production analysis" section
> describes a partition that is not the reported one, and its attribution
> section describes an analysis that has been superseded twice. Drafting Results
> against it would import those errors into prose, which is exactly how this
> project accumulated the stale-number problem in the first place.

---

## 1. Results — ready, with four small gaps

`MANUSCRIPT_OUTLINE_2026-08-21.md` is now the mature document. As of today:

- Every attribution figure carries a provenance tag and cites a `NUMBERS.tsv`
  key; **[cg-Licht/46] is the single cgMLST headline** and cg-Pub/29 has left the
  body.
- The estimator is explicit everywhere (country NN, region modal k=20), so the
  forbidden NN-vs-modal comparison cannot be made silently.
- **W2 resolved** — strata are estimator-matched (14/14 · 8/10 · 19/22), the
  attractor mechanism is confirmed on current data, and the abstention rule is
  built, scored and validated out-of-sample.
- **W3 resolved** (r/m 7.70, alignment-derived). **W8 resolved** (exclusions
  retired; register now reaches the cgMLST pool).
- **W8b added** — the assembler effect, quantified.
- Table 1, Table 2, Table 3 and the abstract all recomputed on the current panel.

**Remaining Results gaps, all small:**

> **✅ ALL FOUR CLOSED as of 2026-08-24 — see §7.** Retained as written because
> the estimate ("three are re-run a script and update a row") turned out to be
> wrong about one of them in an instructive way: the MLST re-run did not update a
> row, it invalidated the cell. Left here as a calibration note.

| gap | effort | blocking? | outcome |
|---|---|---|---|
| MLST row of Table 5 predates the correction — re-run on n=46 | small | no, tag it | ✅ **changed the claim** — the cell is now a bound, not an accuracy |
| Accessory control sub-numbers still n=43 (headline already corrected) | small | no | ✅ all sub-numbers at n=46. ⚠ "conclusions unchanged" holds for the headline but **not** for the contiguity-matched control: at n=46 it reads 11/46 (24%), which is **below** the 26% majority baseline, so that sub-analysis now fails outright rather than merely weakening |
| R7 needs Georgia added as a second autochthonous focus (below) | small | no | ✅ was already drafted; figures re-verified |
| Flow diagram (Figure 1) does not exist; all five numbers now do | small | no | ✅ `make_figure1_bp.py` |

None of these blocks writing. Three are "re-run a script and update a row".

## 2. Methods — not ready. Three distinct problems

### 2.1 §2.12 describes the wrong partition ⚠ **the main blocker**

The preamble is **correct**: it states the reported partition is the corrected
workstation run, **85 units / 2,340 genomes**, with the A100 88-unit run as the
cross-hardware reproducibility control (lines 1183–1189).

**The body was never rewritten to match.** Eight subsections still report the
88-unit A100 partition as the analysis:

| section | stale content |
|---|---|
| 2.12.1 Genome panel | "**2,976** assemblies" (now 2,959) |
| 2.12.4 Partition | "86 units, 2,352 genomes"; sketch over "all 2,976" |
| 2.12.5 Unit refinement | "**Final partition: 88 units, 2,342 genomes**" |
| 2.12.6 Reference selection | "served the **88 units**" |
| 2.12.7 Alignment / r/m | "misplaces 15 of these **88 units**" |
| 2.12.8 Phylogenies | "over those **88 medoids**"; "across **88** divergent lineages" |
| 2.12.9 Phylogeny–geography | ✅ **fixed 2026-08-26**: the national verdict tally read "39, 25, 5, 13 and 6" (sums to 88, the A100 control) and is now the reported 85-unit basis "**37, 25, 5, 12 and 6**". The graded-verdict paragraph was added in the same edit. *(The "56 of 88" string this row cited no longer appears in METHODS; the row itself was stale.)* |

§2.12 spans lines 1173–1671 — **about 30% of the draft.** A reader following the
Methods would reconstruct a different analysis from the one reported.

### 2.2 §2.12.11a describes a superseded attribution analysis ⚠ **worst, because it is the central result**

The attribution Methods section describes the **n=26, SNP-unit, modal-label**
analysis from mid-August:

> *"Twenty-six genomes … three estimators … the unit's modal label, its nearest
> neighbour by recombination-filtered SNP distance … correct for 19 of 19
> scorable genomes against a 58% baseline."*

Every element is superseded. The current headline is **cgMLST (Lichtenegger,
4,221 loci), 46 scorable, region modal k=20 41/46 (89%) against a 46% baseline,
κ 0.832**. Grep counts across the whole draft:

| term | mentions |
|---|---|
| Lichtenegger · modal k=20 · kappa · abstention · GROUPING_LADDER | **0 each** |
| leave-outbreak-out · retired | **0 each** |

So the Methods contain **no description of**: the cgMLST scheme actually used,
the modal-k20 estimator, Cohen's κ as the headline statistic, leave-**outbreak**-out
(as distinct from leave-group-out), the abstention rule, or the exclusion-register
retirement mechanism.

### 2.3 Two live self-contradictions

1. **§2.6.3, union coverage** — W10 flagged this and it is **still present**.
   Line 432 establishes union *is* size-confounded (`r(log n, union) = +0.80`,
   p = 4×10⁻¹¹); line 480 states it was "found **not** to scale with unit size
   (r = 0.142)". Both in the same section, 48 lines apart. Delete the second.
2. **§2.12.13 vs the §2.12 preamble** — line 1658 still reads *"The **production
   run** used an NVIDIA DGX Station A100 …; the **control run** a 22-core
   workstation"*, directly contradicting the preamble's flip 470 lines earlier.
   The designation was corrected in one place only.

## 3. What is genuinely ready in the Methods

Worth stating, because the rewrite is smaller than §2 suggests:

- **§2.1–§2.11 (calibration track) is in good shape.** The r/m headline is
  already **7.70** on the alignment-derived Gate 1 (lines 10, 1407, 1419), and
  the Gate 1 window is described in alignment units.
- **§2.8 method validation** (constant sites, tree-builder equivalence,
  zero-recombination null, spike-in recovery) is self-contained and unaffected by
  the partition question.
- **§2.9 "analyses deliberately not performed"** and **§2.11 known limitations**
  are the right shape and mostly survive.
- The **§2.12 preamble** already states the correct basis and the correct reason
  for it — it is the model for what the body should say.

## 4. Recommended order

1. **Draft Results now**, from the outline, citing `NUMBERS.tsv` keys. It is the
   mature document and drafting will surface any remaining prose gaps cheaply.
2. **Rewrite §2.12 onto the frozen basis** — mechanical, and every number needed
   is already in `NUMBERS.tsv` and `FINAL_BASIS_2026-08-22/`. Fix §2.12.13's
   designation while there.
3. **Write §2.12.11a from scratch.** This is new writing, not editing: cgMLST
   scheme + snapshot, the estimator per scale and why, κ as the headline
   statistic, leave-group-out **and** leave-outbreak-out with the Vietnam/Georgia
   counterexample as the justification, the distance stratification, and the
   abstention rule with both baselines.
4. **Delete the stale union paragraph** in §2.6.3 (one paragraph, already
   identified).
5. **Then** the cheap Results gaps (MLST row, accessory sub-numbers, Figure 1).
6. **Then** the non-science blockers: IRB number, data availability + deposition,
   pinned production command line.

**The reproducibility test (open item 1) should come after step 3, not before.**
*(Ran 2026-08-25 regardless of this ordering, and passed; see `REPRO_RESULT_2026-08-26.md`. The advice stands for any future re-run.)*
Re-deriving the collection against a Methods section that describes a different
partition would produce a diff nobody can interpret.

## 5. Honest risk register for drafting

- **The Methods rewrite is where stale numbers will try to re-enter.** Every
  figure in §2.12 must come from `NUMBERS.tsv` or `FINAL_PARTITION.tsv` at the
  moment of writing, not from the existing prose.
- **Two partitions will remain in the paper** (85 reported, 88 control). That is
  correct and defensible, but §2.12.10 must make the roles unmistakable, because
  this is the single most confusing thing in the corpus.
- **n=46 is small** and the paper's honesty depends on saying so four ways
  (W1 pseudoreplication, W7 the effective class count, the batch-enrichment
  check, and **the same-patient pair**). Those are drafted; keep them. The fourth
  was added 2026-08-26: the 46 scorable genomes come from **45 patients**, since
  `SRR31608433` and `SRR31608435` are one person sampled five years apart. It
  changes no number, and is registered in `OUTBREAK_GROUPS.tsv` as
  `VN_same_patient_2012_2017`. Write "46 cases from 45 individuals"; both abstract
  versions, RESULTS §R2.4, DISCUSSION limitations, METHODS §2.12.11a.2 and the
  outline's W1 now all carry it.
- **The abstention threshold is calibrated on 46 genomes** and its signal was
  chosen after seeing which won. Disclosed in `ABSTENTION_RESULT` §7 — carry that
  caveat into the paper verbatim rather than softening it.

---

## 6. Status update — end of 2026-08-23 autonomous session

**Methods §2.12 is now rewritten and §2.12.11a written from scratch**, so the
main blocker in §2 is cleared. Remaining, in priority order:

| item | state |
|---|---|
| §2.12 body on the frozen basis | ✅ done |
| §2.12.11a attribution Methods | ✅ written from scratch |
| §2.6.3 union self-contradiction | ✅ stale paragraph deleted |
| §2.12.13 production/control designation | ✅ fixed |
| **reproducibility of the reported run** | ✅ **verified 2026-08-25/26**: re-run end to end from the pin; Gate 1 = 47 units, median r/m **7.70**, matching. 81 of 84 comparable units identical in r/m *and* raw SNP counts; per-unit alignment distances identical for 85 of 86. `REPRO_RESULT_2026-08-26.md` |
| **pipeline release cited** | ✅ **tagged 2026-08-26**: `v1.0.5-mod` at `79ab645`, pushed. ⚠ Methods must state the run is **not seed-reproducible**: the pin predates the `gubbins_seed` fix, so Gubbins draws a random RAxML seed and can silently drop a unit while still exiting 0 |
| **R6 discarded set described as graded** | ✅ **done 2026-08-26**: 8 nominal / 2 FDR, 4 none, 2 untestable. Adopted in RESULTS R6, MANUSCRIPT_OUTLINE R6, METHODS §2.12.9, PHYLOGEO_INTERP verdict table, PRIMER §1.3, WHAT_THE_ANALYSES_SHOW (+TH). No pass changes |
| branch support on the reported basis | ✅ 170/170, all trees now carry SH-aLRT/UFBoot |
| **`+ASC` vs `-fconst`** | ✅ **RESOLVED** — quantified on two units. §2.5 is right (`+ASC` estimates 41.9–72.1% GC, median 56.3%, against a true 68.1%; `-fconst` gives 67.6–68.7%, median 68.1%) but **it changes no reported number**, because every reported quantity derives from Gubbins outputs. `ASC_FCONST_RESULT_2026-08-23.md`. Support trees rebuilt with `-fconst`: `L1v4c_TREES_SUPPORTED_FCONST/`, 170/170 — **publish that set** |
| Results R1–R8 draft | ✅ written, figures annotated with their keys |
| R6 country scale | ✅ re-run on the frozen basis (48/26/23/6) |
| R6 sub-national + regional | ✅ re-run on the frozen basis; **sub-national is 1 of 81, not 0 of 88** |
| R5 ST/homoplasy counts | ✅ recomputed from `MLST_v4c.tsv`; ST92 is **3** lineages not 4, ST58 is **5** countries not 3 |
| citations | ✅ 13 verified, 6 resolved, 2 added; "Pearson 2020" unciteable |
| **DeepSANet rebuttal** | ✅ **answerable without the PDF** — the released code sets `TEST_PATH == VAL_PATH` and selects the checkpoint by max val accuracy. Phrase as *"in the released reference implementation"*, and note accuracy ≠ macro F1. Obtaining the paywalled PDF (open item 5) would sharpen the wording but does not gate the Discussion |
| run designation (production/control) | ✅ **fixed 2026-08-23 evening** — the flip had reached 3 files of 6; `GATE1_ALIGNMENT_RESULT` was telling readers to publish **7.44**. `RUN_DESIGNATION_CORRECTION_2026-08-23.md` |

**The verdict is unchanged in shape but the balance has shifted: Methods is no
longer the blocker, and both of the risks flagged above — the `+ASC` question and
the DeepSANet comparison — are now closed.** What remains is not analysis but
assembly: the four small Results gaps in §1, Figure 1, and the non-science
submission blockers.

## 7. Status update — 2026-08-23 evening

The remaining work is bounded and none of it is a data problem:

| item | state |
|---|---|
| §1 gap: MLST row of Table 5 | ✅ **done, and it changed the claim** — at 7 loci NN is not unique for 30 of 33; the cell is now a bound (≤ 8/33) below its own baseline. `MLST_TABLE5_RERUN_2026-08-23.md` |
| §1 gap: accessory sub-numbers at n=43 | ✅ **done** — all four controls, the headline table, the Mexico leave-two-out and the permutation null re-run at n=46; conclusions unchanged. The last figure (contiguity-matched pool) was re-run at n=46 on 2026-08-26 via the new `--contiguity-match` flag: country 24%, region 72%. Nothing remains at n=43 |
| §1 gap: R7 Georgia | ✅ **done, and it was already written** — R7.2 is drafted in `RESULTS_DRAFT` and the outline; all its figures re-verified 2026-08-24 (Asia/non-Asia NN 43/46 κ 0.869 vs modal k=20 46/46 κ 1.000; filtered/raw median 0.090 over exactly 170 replicon-units). The outline's ⚠ 4-vs-5 case-count warning was stale and is now closed |
| §1 gap: Figure 1 flow diagram | ✅ **done** — `make_figure1_bp.py` → `FIGURE1_STUDY_FLOW.svg` (+ `_dark` variant). Reads `NUMBERS.tsv` and **exits non-zero on a missing key**, so it cannot ship with a hole in it. Regenerate with `python3 generate_numbers.py && python3 make_figure1_bp.py` |
| IRB approval number in Methods | **needs the lab record** — cannot be resolved from artifacts |
| data availability statement | ✅ **written** — `DATA_AVAILABILITY_2026-08-24.md` §1, with bracketed placeholders for the accessions/DOI/IRB that do not exist yet |
| deposit new assemblies | ❌ **open, and now itemised** — 7-item checklist in `DATA_AVAILABILITY_2026-08-24.md` §3. Item 7 (tag the pipeline) is ✅ **done 2026-08-26** — `v1.0.5-mod` at `79ab645`, pushed. Item 5 (Zenodo archive → DOI) is unblocked today; 1–4 chain off a BioProject registration; 6 is the IRB number |
| pinned production command line (branch + commit) | ✅ **done**, `main` @ release **`v1.0.5-mod`** = **`79ab645`**, Nextflow 25.04.6, verbatim invocation in `PRODUCTION_RUN_PIN_2026-08-24.md`. Two gaps found and disclosed: the run used `nextflow run .` so no git revision was recorded (commit established by bracketing), and the `--input` samplesheet was lost and is reconstructed |
| reproducibility test end-to-end | ✅ **done 2026-08-25/26**: ran from the pin, rc=0 in 6h37m across two segments. Gate 1 = 47 units, median r/m **7.70**, matching. `REPRO_RESULT_2026-08-26.md` |

**The one item nobody in this repository can close is the IRB number.** Every
other open item is either mechanical or a compute run.
