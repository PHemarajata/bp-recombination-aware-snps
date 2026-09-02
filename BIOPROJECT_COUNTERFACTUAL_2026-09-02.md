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
