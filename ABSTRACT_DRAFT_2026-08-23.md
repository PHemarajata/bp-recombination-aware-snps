# Abstract — draft, 2026-08-23

Written to match `RESULTS_DRAFT_2026-08-23.md` and `DISCUSSION_DRAFT_2026-08-23.md`
on the frozen basis. Supersedes the version in `MANUSCRIPT_OUTLINE` §8, which
predates the abstention result and carried a conclusion since softened.

---

## Main version (~300 words — eLife, PLoS, Microbial Genomics)

> *Burkholderia pseudomallei* causes melioidosis throughout the tropics, and
> cases increasingly present in patients with no travel history, where clinicians
> and public-health agencies ask genomics to supply the place of exposure. We
> assembled 2,959 genomes — 41% of country-labelled public isolates — and tested
> whether exposure country is recoverable, using 46 cases from 45 individuals
> with independently documented exposure as ground truth. Under a holdout
> removing both same-country validation genomes and same-source outbreak
> isolates, **country attribution did not exceed chance: 10 of 46 (22%) against a
> 26% majority baseline, κ 0.19.** Regional attribution reached **41 of 46 (89%)
> against a 46% baseline, κ 0.83**, and the deepest split — Asia versus elsewhere
> — was recovered **without error (κ 1.00)**. The contrast is sharpest where
> attribution should be easiest: among the 14 cases with a close relative in the
> panel, region was correct **14/14** and country **2/14**. Country accuracy
> remained flat across a **584-fold** range of resolution, from 7 MLST loci to
> whole-genome recombination-filtered SNPs, while regional accuracy rose from 50%
> to 82% over the same range, indicating absence of signal rather than
> insufficient resolution. Two causes are separable in kind: for **7 of 16**
> exposure countries no public genome exists, all seven in Latin America and the
> Caribbean; and some lineages span continents — a published US autochthonous
> cluster and a Viet Nam-acquired case differ by **one cgMLST locus in 4,221**.
> Declining to answer where no relative lay within 0.462 allelic distance raised
> regional accuracy to **94% on 76% of cases** out-of-sample, but did not rescue
> country attribution. Reporting should therefore be graded by geographic scale.
> The collection is also inverted against disease burden: South Asia contributes
> **2.5%** of genomes and **44%** of predicted global cases.

## Short version (~150 words — Nature Communications, EID)

> Melioidosis increasingly presents in patients with no travel history, and
> genomics is asked to supply the place of exposure. Across 2,959
> *Burkholderia pseudomallei* genomes and 46 cases from 45 individuals with
> independently documented
> exposure, **country attribution did not exceed chance (10/46, 22%; baseline
> 26%; κ 0.19)** under a holdout removing same-country and same-source
> references, while **regional attribution reached 89% (κ 0.83)** and the
> Asia-versus-elsewhere split was recovered without error. Among the 14 cases
> with a close relative available, region was correct 14/14 and country 2/14.
> Country accuracy was flat across a 584-fold range of genomic resolution,
> indicating absent signal rather than insufficient resolution. For 7 of 16
> exposure countries no public genome exists, and some lineages span continents:
> a US autochthonous cluster and a Viet Nam-acquired case differ by one cgMLST
> locus. Abstaining where no close relative exists raised regional accuracy to
> 94%, but did not rescue country attribution.

---

## Notes on what is in, out, and why

**Every figure is regenerable.** 2,959 `[panel.corrected_v4d]`; 41%
`[panel.coverage_of_ena]`; 46 `[validation.scorable]`; 10/46, 26%, κ 0.193
`[attribution.country.nearest_neighbour, ladder.country.kappa]`; 41/46, 46%,
κ 0.832 `[attribution.region.modal_k20, ladder.region_7way.kappa]`; κ 1.000
`[ladder.asia_vs_not.kappa]`; 14/14 and 2/14 `[…d_lt_0.05]`; 0.462, 94%, 76%
`[abstention.region.*]`; 2.5% `[panel.region.South_Asia]`.

**Deliberately included, against the temptation to cut for space:**

- **The baselines, every time.** "22%" alone reads as partial success; "22%
  against a 26% baseline" is the finding. Same for 89% against 46%.
- **45 individuals, not just 46 cases.** Two isolates are from one patient. It
  costs four words and pre-empts the reviewer who finds it.
- **The one-locus Georgia/Viet Nam clause.** Without it the paper reads as "we
  lacked references", which is only part of the story and is the weaker part.
- **"did not rescue country attribution".** Reporting the abstention rule's
  failure at country scale in the abstract keeps the tool's claim honest.

**Deliberately excluded:**

- **r/m 7.70 and the recombination machinery.** Load-bearing for Methods, not for
  a reader deciding whether to read on.
- **The 21-countries/5%-of-burden figure.** The South Asia contrast is the more
  robust of the two and does not move between censuses; one burden statistic is
  enough for an abstract.
- **"by any method".** The earlier draft concluded country attribution is
  "currently unachievable for most source countries by any method". We cannot
  support "any method" — we tested our estimators, not all possible ones — and
  the Discussion has been softened accordingly. The abstract now states what was
  measured and stops.
- **Sub-national (0/5).** True but n=5; it would invite a question the data
  cannot answer well.

⚠ **One number to re-check at submission.** "41% of country-labelled public
isolates" is the panel against ENA BioSamples carrying a country
`[panel.coverage_of_ena]`. If a reviewer reads it as "41% of all public
*B. pseudomallei* genomes", that is a different and smaller fraction (36.8%
against the public-derived count). Consider "41% of publicly archived isolates
with a recorded country" if space allows.
