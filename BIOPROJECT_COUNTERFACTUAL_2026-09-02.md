# What would this project look like if we had not cared about BioProjects?

**2026-09-02.** A deliberate counterfactual, run on the frozen basis. The
question is not rhetorical: BioProject structure could in principle be doing
hidden work in any of the three headline results, and each is testable.

**The answer differs completely by result.** One collapses, one is robust, and
one cannot be tested at all. That last is itself a finding.

---

## Summary

| result | without the BioProject control | with it | verdict |
|---|---|---|---|
| **Geography** | 26 of 85 units "clustered" | **6** | **collapses.** 77% of the signal was batch |
| **r/m headline** | 7.70 (n=47) | 7.48 restricted to multi-BioProject (n=46) | **robust.** Moves 2.9% |
| **Attribution** | — | — | **untestable.** Only 13 of 46 have the metadata |

---

## 1. Geography: the control removes 77% of the signal

Of 85 units, **26 cluster by country** at p <= 0.05 on the permutation test taken
alone. **Six survive** the BioProject control run on identical trees with
identical machinery.

| raw verdict | after the control | units |
|---|---|---|
| uninformative, single-valued | untestable | 37 |
| not distinguishable from chance | null | 22 |
| **clustered** | confounded by BioProject | 12 |
| **clustered** | vacuous control | 5 |
| **clustered** | null | 3 |
| **clustered** | **geographic, control passes** | **6** |

**Had we not cared about BioProjects, this paper would have claimed 26 units of
geographic structure instead of 6, overstating the result more than fourfold.**
Two of the six clear the control only barely (BioProject p = 0.060 and 0.063), so
the robust set is arguably four, which pushes the overstatement toward sixfold.

This is why the finding was reframed: the control *is* the result. See Results
section 8 and Figure 4.

## 1a. Are the six passing units an artifact of missing metadata?

**No, and the control handles this explicitly.** The obvious failure mode is that
a unit passes the control because its BioProject data is too sparse for the
confounder test to find anything. Absent values are normalised to ambiguous, so
missing metadata *weakens* the BioProject signal, raises its p-value, and makes a
unit **more** likely to pass. The leniency runs toward claiming geography.

Coverage by outcome:

| interpretation | units | median BioProject coverage | min |
|---|---|---|---|
| **geographic (control passes)** | 6 | **79%** | 75% |
| confounded by BioProject | 12 | 89% | 75% |
| null | 25 | 80% | 20% |
| **vacuous control** | 5 | **44%** | 18% |
| untestable, single-valued | 37 | 92% | 9% |

The six passing units have 75-100% coverage, comparable to the confounded ones.
They are not passing on absent data. Units that genuinely lack the metadata are
classified **`vacuous control`** and are **not** counted as geographic, which is
the control behaving correctly.

**But six remains an upper bound.** At 79% median coverage, roughly a fifth of
tips in the passing units are still ambiguous for BioProject, so the confounder
test is somewhat underpowered in exactly the units that carry the claim.
Recovering the missing values can only push the count down, never up. That makes
the recovery in §4 a test of the result rather than metadata housekeeping.


## 2. r/m: the headline is robust, and Gate 1 already screens batch out

Across the 85 units, BioProject concentration barely predicts r/m at all:

| relationship | Pearson r |
|---|---|
| dominant-BioProject share vs r/m | **-0.066** |
| number of distinct BioProjects vs r/m | -0.136 |
| dominant-BioProject share vs mean pairwise SNPs | -0.312 |

Restricting the reported headline to units drawing on more than one BioProject
moves it from **7.70 (n=47) to 7.48 (n=46)**, a change of 2.9%. Only one
in-window unit is single-BioProject. **The recombination result does not depend
on batch structure.**

**But BioProject concentration strongly predicts falling below the Gate 1 floor**,
which is the interesting part:

| Gate 1 class | median dominant-BioProject share | median distinct BioProjects | median r/m |
|---|---|---|---|
| in-window | 0.50 | 3 | 7.70 |
| **below floor** | **0.91** | 3 | 1.32 |
| above ceiling | 0.48 | 4 | 2.14 |

Units below the floor are dominated by a single submitter, at a 0.91 median
share against 0.50 in-window. All six single-BioProject units sit below the
floor, with a median of 264.5 mean pairwise SNPs against a floor of 700.

That is coherent rather than alarming: a low-diversity unit is often one outbreak
sequenced by one laboratory, so low diversity and single-batch sampling co-occur.
The useful consequence is that **Gate 1, derived purely from alignment SNP
density, incidentally excludes the batch-concentrated units as well.** It was not
designed to control for batch and it does so anyway.

## 3. Attribution: this cannot be answered, and that is the finding

The test would be whether a validation genome's nearest neighbour shares its
BioProject, since a "correct" attribution whose NN is a batch-mate may be
recovering collection history rather than genomic geography.

**It cannot be run.** Of the 46 validation genomes:

| | n |
|---|---|
| present in the panel at all | 33 |
| BioProject known for the query | 17 |
| BioProject known for the nearest neighbour | 38 |
| **known for BOTH, i.e. testable** | **13** |

**33 of 46 (72%) are untestable.** The gap is not random: the in-house isolates
that make up much of the validation set carry `bioproject = unknown` or blank,
which is the same metadata gap recorded in SUBMISSION_TODO B2. The metadata is
missing precisely where the test is needed.

For completeness, the n=13 result runs *against* the leakage hypothesis: country
attribution is 0/3 when the NN shares a BioProject and 1/10 when it does not;
region is 1/3 against 8/10. **Do not quote these.** At n=3 versus n=10 they are
uninformative, and the direction is as likely to be an artifact of which genomes
happen to have metadata as anything real.

**What would settle it:** registering the BioProject (SUBMISSION_TODO B1) and
depositing the 312 in-house assemblies (B2) would populate the missing field and
make this testable. It is one more reason to start that chain early.

---

## What this changes

1. **Nothing about r/m.** The headline stands at 7.70 and does not lean on batch.
2. **Everything about geography**, and that change is already made.
3. **One open question is now explicitly open** rather than silently assumed.
   Attribution has not been shown to be free of batch leakage; it has been shown
   to be *untestable* with current metadata. Those are different claims and the
   manuscript should make the second, not the first.

The general lesson is worth stating in the Discussion. Batch structure did not
behave uniformly across three results computed from the same collection: it
destroyed one, left another untouched, and could not be evaluated for the third.
A single blanket statement about confounding would have been wrong in all three
directions.

---

## 4. Recovering the missing BioProjects is a test, not housekeeping

426 of 2,340 analysis genomes (18.2%) have no usable BioProject. They split into
two groups that need completely different actions:

| group | n | action |
|---|---|---|
| public read runs (SRR/ERR) | **150** | **recoverable now** by ENA lookup |
| in-house (IP/IE) | **276** | no BioProject exists; needs B1/B2 deposition |

**The 150 are worth recovering before submission**, because missing metadata
makes the control lenient (§1a) and the recovery can only reduce the six. Use
**ENA, not NCBI efetch**, which has silently returned a different sample with
HTTP 200 on SAMEA accessions in this project before; always diff requested
against returned accessions.

**The 276 in-house genomes are one study.** They are the Nakhon Phanom
collection, and on the author's confirmation they would all be deposited under a
single BioProject. That is testable *now* without waiting for deposition, by
assigning them one synthetic identifier and re-running the control. All 276
currently count as ambiguous, and 274 are Thailand, so they form a large
single-country single-batch block that the control is currently blind to. Five
of the six passing units contain them, at 5% to 23% of their tips. See §5.

---

## 5. Testing the in-house BioProject assumption: 6 becomes 5

The 276 in-house genomes are one study and would be deposited under a single
BioProject (author's confirmation). All 276 currently carry `unknown`, and 274
are Thailand, so they form a large single-country single-batch block that the
control cannot presently see. **That is testable now**, by assigning them one
synthetic identifier and re-running.

**Control run first.** Re-running the frozen assignments at 1,000 permutations
and seed 20260815 **reproduces the frozen table exactly** (interpretation counts
identical), so any change below is the assumption and not run-to-run noise.

| interpretation | frozen | rerun | IP/IE as one BioProject |
|---|---|---|---|
| **geographic (control passes)** | 6 | 6 | **5** |
| confounded | 12 | 12 | **16** |
| null | 25 | 25 | 25 |
| untestable, single-valued | 37 | 37 | 37 |
| vacuous control | 5 | 5 | **2** |

**Two units lose the control, one gains it.**

| unit | IP/IE share | country p | BioProject p, before | after | outcome |
|---|---|---|---|---|---|
| `strain_1_L1_11` | 3/24 | 0.0040 | 0.0589 | **0.0330** | geographic -> **confounded** |
| `strain_2_L1_2` | 14/75 | 0.0120 | 0.3636 | **0.0360** | geographic -> **confounded** |
| `strain_7_L1_5` | 2/20 | 0.0020 | 0.1269 | 0.1818 | vacuous -> **geographic** |

`strain_2_L1_2` is the substantive one: it moves from clearly passing at p = 0.36
to clearly confounded at p = 0.036, because 19% of its tips are the in-house
block. `strain_1_L1_11` was already one of the two marginal passes. The gain is
real rather than cosmetic: `strain_7_L1_5` previously had too little BioProject
data to test, and the assumption makes it testable.

**The count is not the whole story. Robustness degrades too.** Among the five
that pass under the assumption, the BioProject p-values spread widely:

| unit | BioProject p (with assumption) | reading |
|---|---|---|
| `strain_11_L1_5` | 0.894 | solid |
| `strain_5_L1_3` | 0.360 | solid |
| `strain_7_L1_5` | 0.182 | moderate |
| `strain_1_L1_28` | **0.167** (was 0.925) | moderate, moved a long way |
| `strain_1_L1_5` | **0.071** | marginal |

**Only two units pass the control comfortably.** `strain_1_L1_28` fell from 0.93
to 0.17 on a 23% in-house share and is no longer a clean pass.

## What to report

Report **6 on the frozen basis**, because that is what the deposited metadata
supports today, and report this sensitivity beside it: under an assumption the
authors know to be true but cannot yet evidence, it is **5, of which only 2 pass
comfortably**. Do not quietly adopt 5 as the headline; the synthetic BioProject
is a defensible assumption, not a fact in the archive, and it becomes a fact only
when B1/B2 land.

> **RETRACTED, same day.** The sentence that stood here said "every improvement
> to BioProject metadata has reduced the geographic count, never increased it.
> Six is an upper bound." **That was wrong, and it was wrong because I only
> looked at one of the two ways this control fails.** See §6.

---

## 6. The synthetic BioProject was a bad idea, and "upper bound" was wrong

**Raised by the author**: we have never investigated *why* the BioProjects in
this collection group the genomes they group. Submissions are bundled by study,
by laboratory, by funding source, by collection period, by region -- reasons that
differ between BioProjects and some of which carry no biological meaning.
Assigning 276 in-house genomes a single synthetic identifier asserts that their
grouping reason is equivalent to the grouping reason behind PRJEB25606's 543
genomes. **Nothing establishes that, and it matters.**

It matters in a specific direction. The 276 are one study from **one province,
Nakhon Phanom**, over one collection period. Their geographic coherence is
**real, not administrative**. Feeding them to the control as a batch label and
watching units turn "confounded" is not detecting an artifact; it is removing
genuine geography.

### This was already known, and I failed to connect it

`bioproject_within_country_bp.py` (2026-08-24) exists precisely for this. Its
own docstring: **113 of 119 BioProjects (95%) are entirely single-country**, and
~99% of same-BioProject pairs are also same-country, so "a genuine within-country
clonal expansion deposited by one study makes BOTH variables fire on the SAME
clade, and the unit is discarded as confounded when nothing artefactual has been
shown."

It runs the conditional test: hold country fixed, ask whether BioProject still
structures the tree. The result:

| among units discarded as "confounded" and testable | n |
|---|---|
| **no independent batch structure -> the discard OVER-CONTROLLED** | **14** |
| genuine batch structure at nominal p | 8 |
| of those, surviving FDR | **2** |

**Both units my synthetic BioProject flipped show no independent batch
structure**: `strain_2_L1_2` (Thailand, p = 0.36, q = 1.00) and `strain_1_L1_11`
(China, p = 0.58, q = 1.00). The flip removed geography, not artifact. It is a
worked example of the over-control this project had already documented.

### What is actually true about the control

It errs in **both** directions, and I reported only one:

| failure mode | effect on the count | evidence |
|---|---|---|
| missing metadata weakens the confounder test | pushes the count **up** | 18.2% of genomes lack BioProject; §1a |
| BioProject is nested inside country | pushes the count **down** | 95% single-country; 14 of 22 testable discards over-controlled |

**Six is not an upper bound. It is a discriminant result whose error bars run in
both directions**, and the documented over-control is the larger of the two
effects on present evidence.

### Recommendations, revised

1. **Do not adopt the synthetic BioProject.** Not in the manuscript, not as a
   sensitivity. The assumption it encodes is untested and points the wrong way.
   §5 is retained as a record of what was tried and why it was rejected.
2. **Report six as a discriminant result**, stating plainly that the control is a
   discriminant and not an adjustment, and that it over-controls where BioProject
   and country are not separable.
3. **The conditional within-country test is the right instrument** and it already
   exists. Where a unit is discarded as confounded, report whether batch
   structure survives holding country fixed. On present evidence that softens 14
   of 22 testable discards.
4. **A6 still stands but for a narrower reason.** Recovering the 150 public
   SRR/ERR BioProjects is worth doing because they are genuine archived facts.
   It is no longer justified as "can only reduce the count".
5. **The open question the author identified is real and unaddressed**:
   characterise what the BioProjects in this collection actually represent, at
   least for the largest few. Until then, BioProject is a proxy of unknown
   construct validity being used as a confounder, which is a Methods limitation
   worth stating rather than a solved problem.
