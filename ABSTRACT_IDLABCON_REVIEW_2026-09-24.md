# Review of the ID Lab Con abstract against the current basis

**2026-09-24.** Prompted by two objections: cgMLST was not performed, and the
partitions are fully utilized. Checking those turned up more.

**Root cause, and it is a repeat.** The abstract was built from
`ABSTRACT_DRAFT_2026-08-23.md` and `RESULTS_DRAFT_2026-08-23.md`. Both predate
`ATTRIBUTION_SPECIFICATION_CURVE_2026-09-02.md`, which is Tier 3 of the
2026-09-02 document map and revises the attribution conclusions.
`STATE_2026-09-02.md` says plainly that it and `NUMBERS.tsv` win when documents
disagree, and this session did not treat it as the index.

`PR3_CORRECTIONS_2026-09-02.md` describes the same failure in a prior session:
"the manuscript's numbers are correct *for the tree the session could see*", and
warns that "any future session branched from `main` will reproduce them again."
It did.

`git fetch` confirms `main` has not moved since 2026-09-14 (`9700bad`), so this
is not a stale checkout. It is stale *source selection* within a current tree.

---

## 1. The two objections

**cgMLST: both things are true, and that is the problem.**

cgMLST *was* performed. `CGMLST_LICHTENEGGER_RESULT_2026-08-21.md` records the
Lichtenegger v1.1 scheme, 4,221 loci, seed K96243, PMID 33980649, panel 3,033
genomes, validation 44, scored by `score_cgmlst_lichtenegger.py`. The grouping
ladder that carries the region headline was run "on the Lichtenegger cgMLST
profiles, 3,031 genomes, 45 validation" (`GROUPING_AND_CDC_2026-08-21.md`).

But **`MANUSCRIPT_DRAFT_2026-09-02.md` contains no cgMLST at all**, and none of
the attribution numbers. A grep for cgMLST, "core-genome multilocus", 4,221 and
Lichtenegger returns nothing. Its nine Results sections are the partition, the
operating range, r/m, subdivision, detection bounds, tree-builder robustness,
the two failure modes, country-versus-collection-history, and reproducibility.
`PUBLICATION_STRATEGY_2026-09-02.md` says of geography: "Cut it entirely. Not
deferred, cut."

So the abstract straddles two streams: an August attribution analysis on cgMLST
and a September manuscript that contains neither. That is the real defect.

**The partition: the abstract's claim is incoherent as written.**

Methodology currently says the genomes were "partitioned into 85
recombination-aware analysis units, and attribution was scored on core-genome
multilocus sequence typing (4,221 loci), so the result does not depend on the
partition." The second clause is `RESULTS_DRAFT`'s, and it is about cgMLST
scoring being partition-independent. Naming the 85 units and then saying they do
not matter is either wrong or pointless in an attribution abstract. The current
manuscript is partition-central throughout.

---

## 2. Claims that are wrong as written

**2.1 The 584-fold resolution range, on both ends.**

The abstract says "flat across a 584-fold range of genomic resolution, from 7
loci to whole-genome recombination-filtered variants."

`RESOLUTION_CURVE_RESULT_2026-08-21.md` subsampled **k cgMLST loci at random,
k = 2 to 4,089**, and calls it a **2,000-fold** range. 584-fold is 4,089 / 7,
that is 7-locus MLST to the full cgMLST scheme. **Whole-genome
recombination-filtered SNPs are not an endpoint of that curve.**

**2.2 The 50% to 82% region rise sits on a different denominator.**

Same document: the first run scored **26** validation genomes, the corrected
re-run **31** (country flat 2.0% to 0.0%; region 49.5% to 82.1% against a 48%
baseline). The abstract places this in a sentence that reads as the same 46
cases. The document's own closing note is explicit: "Quote the baseline
alongside the denominator it belongs to, never on its own."

**2.3 The 14/14 and 2/14 stratum, without its baselines.**

`ATTRIBUTION_SPECIFICATION_CURVE_2026-09-02.md` §4 corrects exactly this class of
comparison: "an artifact of comparing raw accuracies across strata with
different baselines. The close-relative stratum has a much higher majority
baseline (0.739 against 0.522 at region scale, 0.435 against 0.217 at country
scale) ... Beating the baseline there is harder, not easier."

`METHODS_DRAFT` §2.12.11a.5 gives 2/14 and 14/14 with **no baseline column**.
Quoting them bare is the artifact the September document warns against.

**2.4 The region figure has no estimator attached, and the estimator is the number.**

89.1% is **`modal_k20`**. The September curve finds it is the only estimator
beating its baseline in all three strata (0.891 / 0.913 / 0.870), while
**nearest-neighbour fails where a close relative exists** (0.696 against a 0.739
baseline). Region across all twelve specifications spans 0.348 to 0.913. The
abstract's Methodology lists both estimators as if interchangeable.

**2.5 Country needs both baselines, not one.**

The same document: majority-class 0.261 against marginal chance 0.030, differing
by 0.231 and giving opposite verdicts. "Reporting only kappa would present a
failing classifier as a working one." The abstract gives kappa 0.19 with the
majority baseline only. Country spans 0.000 to 0.261 across twelve
specifications; only one beats its stratum baseline, by one genome in 23, which
the document calls "within noise and not a result."

---

## 3. Denominator drift across the attribution stream

| figure | value | source |
|---|---|---|
| cgMLST run panel | 3,033, validation 44 | `CGMLST_LICHTENEGGER_RESULT_2026-08-21.md` |
| grouping ladder panel | 3,031, validation 45 | `GROUPING_AND_CDC_2026-08-21.md` |
| deduplicated panel | 2,959 | `METHODS_DRAFT` §2.12.1 |
| analysis basis | 2,340 in 85 units | `STATE_2026-09-02.md` |
| scorable validation | 46 from 45 individuals | `RESULTS_DRAFT` R2 |
| resolution curve | 26, then 31 | `RESOLUTION_CURVE_RESULT_2026-08-21.md` |

The abstract asserts 2,959 and 46 and cgMLST together. That combination is not
attested in any single document.

---

## 4. What survives unchanged

- Country 10/46, 21.7%, majority baseline 26.1%, kappa 0.193. Confirmed by the
  September curve.
- Region `modal_k20` 41/46, 89.1%, baseline 45.7%, kappa 0.832.
- Asia versus non-Asia, kappa 1.000 (`GROUPING_AND_CDC_2026-08-21.md`).
- Recurrence: 20 pairs, 1 to 14 SNPs against 1,102, a 79-fold gap.
- 7 of 16 exposure countries with no public genome, all Latin America and the
  Caribbean.
- One cgMLST locus in 4,221 between the US autochthonous cluster and the
  Viet Nam-acquired case.
- Sub-national 0/5.
- The binomial test and intervals in `attribution_significance_bp.py` are
  unaffected: their inputs (10, 41, 46, and majority counts 12 and 21) are all
  confirmed above.

---

## 5. One result the abstract does not use, and probably should

`GROUPING_AND_CDC_2026-08-21.md` §1 scores the 2021 aromatherapy outbreak
against the panel with the outbreak held out. South Asia leads on minimum,
median and mean distance; South Asia against all other regions gives
Mann-Whitney **p = 2.8e-34** with a rank-biserial effect of 0.82; **India
against the rest of South Asia gives p = 0.351**.

That reproduces the CDC's own published conclusion on their own outbreak from a
different panel and a different method: their genomics gave South Asia, and
India came from the product supply chain. For a US public health laboratory
audience this is the most directly recognizable evidence in the whole project,
and it converts the negative result from a limitation of this collection into a
reproduction of a published investigation's limit.
