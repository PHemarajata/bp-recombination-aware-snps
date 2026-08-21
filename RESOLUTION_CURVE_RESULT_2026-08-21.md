# Attribution vs typing resolution — the curve

2026-08-21. `resolution_curve_bp.py`, data `RESOLUTION_CURVE.tsv`.

> **Numbers below are from the first run on 26 validation genomes.** Re-run on
> the corrected 31-genome set gives the same shape with slightly lower values —
> country flat (2 loci 2.0%, 7 loci 7.3%, 1,000 loci 1.0%, 4,089 loci **0.0%**);
> region rising 49.5% -> 82.1% against a 48% baseline. **The conclusion is
> unchanged**: country flat across the range, region rises and plateaus.

Subsampled **k loci at random** from the 4,089-locus cgMLST profile, k = 2 →
4,089, 10 replicates each, and scored attribution by nearest neighbour under the
**same leave-group-out regime** as the main analysis. This converts our three
fixed points (7-locus MLST, cgMLST, whole-genome) into a continuous curve.

---

## The result

| loci | **country** | **region** |
|---|---|---|
| *baseline (majority class)* | **0%** | **50%** |
| 2 | 1.6% ± 2.0 | 51.0% ± 3.9 |
| 3 | 2.4% ± 2.0 | 59.2% ± 14.2 |
| 5 | 0.8% ± 1.6 | 69.6% ± 12.6 |
| 7 | 3.2% ± 2.4 | 68.8% ± 6.0 |
| 10 | 3.2% ± 3.0 | 77.1% ± 9.4 |
| 20 | 1.6% ± 2.0 | 78.3% ± 6.7 |
| 50 | 1.6% ± 2.7 | 79.6% ± 6.6 |
| 100 | 1.6% ± 2.7 | 81.2% ± 4.7 |
| 250 | 0.4% ± 1.2 | 78.7% ± 5.7 |
| 500 | 1.6% ± 2.0 | 81.7% ± 5.7 |
| 1,000 | 1.2% ± 1.8 | **85.4% ± 3.4** |
| 2,000 | 2.4% ± 2.0 | 84.6% ± 1.9 |
| 4,089 | **0.0%** | 83.3% |

---

## Why this is stronger than "resolution doesn't help"

**The two scales behave completely differently, and that is the point.**

**Region rises from baseline to a plateau.** 51% at 2 loci — indistinguishable
from the 50% majority-class baseline — climbing to ~85% and saturating somewhere
between 100 and 1,000 loci. **The method demonstrably converts extra resolution
into accuracy when there is signal to convert.**

**Country stays flat at zero** across a **2,000-fold** range. The 0.4–3.2%
excursions are noise — they are within one or two genomes of zero on a 25-genome
denominator, and the full 4,089-locus set scores exactly 0.

So the region curve is a **built-in positive control**. It rules out the obvious
alternative explanation for the country result — that our estimator is simply too
blunt to exploit fine differences. It plainly is not: the same estimator, same
holdout, same genomes, gains 35 points at region scale.

**The conclusion tightens to:** country-level attribution fails not because we
lack resolution, but because the country-level signal is not present in the
genome to be found. Adding loci cannot manufacture information that is not there.

---

## Where the plateau sits, and what it implies practically

Region accuracy is within a few points of its maximum by **~100 loci** and flat
after ~1,000. So for regional attribution, a scheme of a few hundred loci is
about as good as the whole core genome.

That has an operational implication worth stating: **a moderate cgMLST-sized
scheme is sufficient for regional attribution**, and the added cost of
whole-genome SNP analysis buys resolution that matters for *cluster membership*
(the Mississippi ≤20-SNP rule) rather than for *geography*.

---

## The caveat that must travel with this

**Random loci are a lower bound for a curated scheme of the same size.**

The published PBP dual-locus scheme
([10.1371/journal.pntd.0009882](https://doi.org/10.1371/journal.pntd.0009882))
selected its two loci *because* they carried geographic signal. Our 2-locus point
samples two loci *at random*. A curated pair can beat a random pair, and our
curve does not refute that.

**State the claim precisely:** resolution alone does not buy country-level
attribution. That is weaker than, and must not be confused with, "no two-locus
scheme can work."

The honest comparison would be to implement the PBP scheme itself and score it
through the identical holdout. Their 11 SNPs across two PBP-3 genes are
specified in the paper; that remains open work.

**A second caution on their loci specifically:** PBP genes are β-lactam targets
and therefore under drug selection. Geographic signal in selected loci may track
antibiotic-use patterns and selection-driven homoplasy rather than descent. That
is a reason to prefer neutral core-genome markers, and a reason a curated
selected-locus scheme might perform well for reasons that do not generalise.

---

## Note on the baseline

Baseline here is **50%** (12 of 24 scorable at region scale), against **58%**
quoted earlier from the core-genome analysis, which scored 19 genomes. Different
scorable denominators — cgMLST places genomes the unit-based method cannot.
**Quote the baseline alongside the denominator it belongs to**, never on its own.
