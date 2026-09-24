# ID Lab Con 2027 abstract, draft 2026-09-24

> ⚠ **CORRECTED 2026-09-24, NOT YET VERIFIED AGAINST `NUMBERS.tsv`.** The
> review in `ABSTRACT_IDLABCON_REVIEW_2026-09-24.md` found five claims wrong as
> written. Methodology and Results are rebuilt on
> `ATTRIBUTION_SPECIFICATION_CURVE_2026-09-02.md`: the resolution-curve sentence
> and the bare 14/14 stratum are gone, every accuracy now names its estimator,
> and country carries both baselines. The 85-unit partition is no longer
> mentioned, because this abstract reports no partition-based result.
> **Before submitting**, run the two commands in
> `MAC_VERIFICATION_REQUEST_2026-09-24.md` and check these figures against
> `NUMBERS.tsv`.

APHL ID Lab Con 2027, Hyatt Regency Atlanta, March 15-18, 2027. Everything below
is taken from the official call for abstracts PDF (`idlc27_callforabstracts.pdf`,
supplied 2026-09-24), not from the event webpage.

| | |
|---|---|
| **Submission deadline** | **October 2, 2026** |
| **Accept or reject notice** | November 18, 2026 |
| **Presentation types** | oral or poster (no plenary abstract, see below) |
| **Category** | Pathogen Genomics, also considered for the AMD Workshop |
| **Submission** | `abstractscorecard.com`, EventKey `JZTEGVTP` |
| **Contact** | Kelly Wroblewski, MPH, MT(ASCP), `id.conference@aphl.org` |

**The submission is four separate fields with character caps, not one block.**
The call for abstracts PDF states no word limit, and that is a red herring: the
online form imposes its own, per field. Taken from the form itself.

| field | cap | this draft (form count) | margin |
|---|---|---|---|
| Submission title | 10-200 chars, 1-75 words | 75 chars, 15 words | 125 |
| Objectives | 500 chars | 423 | 77 |
| Methodology | 750 chars | 638 | 112 |
| Results | 1,250 chars | 1042 | 208 |
| Conclusions | 500 chars | 380 | 120 |

**The form counts characters excluding spaces.** It reported the chosen title as
75 characters where a raw count gives 89, and the difference is exactly the 14
inter-word spaces. Both counts are given below, so the drafts fit either way.
The *word* count does include every word.

**The title must contain no abbreviations.** The chosen one has none. Keep it
that way if you edit it.

**Three form questions to answer** beyond the text: the topic (pick Pathogen
Genomics), whether to be considered for the AMD Workshop (yes), and whether the
committee may consider the abstract for a poster if it is not taken for an oral
(yes, and the call already says this happens anyway).

**Presenters pay their own way.** Registration is $750 early through
February 10, 2027 and $800 late, plus travel from Bangkok, and speakers must
attend in person. Worth settling before submission rather than after acceptance.

**Scope note, corrected 2026-09-24.** This abstract covers the *global
attribution* work: 2,959 genomes, 85 recombination-aware analysis units, and
accuracy measured against 46 documented-exposure cases. It is **not** the
Nakhon Phanom paired human and residential analysis, which is a separate study
on its own 2,773-genome framework.

⚠ **An earlier version of this file said that dataset "does not appear anywhere
in this repository". That was wrong.** The paired-household *analysis* is not
here, but the *isolates* are: **312 in-house Nakhon Phanom genomes (259 `IP-`,
53 `IE-`) sit inside this panel**, 276 of them in the analysis basis
(`METHODS_DRAFT_2026-08-19.md` §2.1, `BIOPROJECT_COUNTERFACTUAL_2026-09-02.md`
§4, `SUBMISSION_TODO.md` B2). They are unpublished and undeposited, all
carrying `bioproject = unknown` or blank. This changes the clearance position,
see open item 6.

Source of every number: `ABSTRACT_DRAFT_2026-08-23.md`, which draws from
`NUMBERS.tsv` on the frozen basis `FINAL_BASIS_2026-08-22/`. `NUMBERS.tsv` is
not in this repo (it is generated, and the working copy moved to the Mac on
2026-09-14). Revalidate before submission with `freeze_basis_bp.py` and
`generate_numbers.py`.

---

## Title

**Chosen, 2026-09-24.** Confirmed against the form at 75 characters and 15
words, inside the 10-200 character and 1-75 word limits, and containing no
abbreviations.

> **Where was this patient exposed? What the melioidosis genome answers, and
> what it does not**

The six alternates considered are in git history at `b5755c9`. Two wording
constraints still apply to any edit. **Avoid "continent"**, because the regional
result is a 7-way split and a reviewer who checks will find the mismatch.
**Avoid "cannot be determined" or "impossible"**, because we measured our own
estimators on this panel rather than every possible method.

## Authors

[AUTHORS]. Association of Public Health Laboratories, [AFFILIATION LINE].

## Submission type and category

**Oral presentation**, with poster as the fallback. The call states that
abstracts not accepted for oral presentation may be considered for poster, so
this is one submission and not two. Orals run 15 to 30 minutes, slotted into 60,
90 or 120-minute sessions, with the length set during review.

There is no plenary or roundtable abstract to submit. Those are **educational
session proposals**, a separate submission type wanting a session topic,
objectives, suggested speakers and tentative talk titles. An earlier version of
this file recommended plenary, which was wrong.

**Category: Pathogen Genomics**, which the call marks *also considered for the
AMD Workshop*. That workshop is new this year, runs Monday March 15, 2027, and
takes poster and oral submissions, so this category puts the abstract in front of
two audiences from one submission. The listed examples for it are metagenomics,
bioinformatics workflows and regulatory frameworks, and a measured accuracy floor
for a genomic method sits comfortably among them.

Infectious Disease Outbreaks and Surveillance is the plausible alternate, since
its examples name molecular epidemiology approaches. Pathogen Genomics is the
better fit and carries the AMD consideration, so it is the one to pick.

---

## Submission text, field by field
Paste each block into its own box. Counts are given as *form count* (spaces
excluded, which is what the box reports) and *raw*, so the fit holds either way.

### Objectives — 423 / 500 characters (raw 497)

Burkholderia pseudomallei causes melioidosis and is a Tier 1 select agent. Exposure origin is both a clinical and an epidemiologic question, and without a travel history it is assigned from the genome. Locally acquired cases in Mississippi and a presumptive focus in Georgia have made that a domestic question for United States laboratories. The accuracy of genomic assignment below continental scale is not well established. We measured that accuracy at sub-national, country and regional scales.

### Methodology — 638 / 750 characters (raw 744)

We compiled 2,959 B. pseudomallei genomes, 41% of the country-labelled public record: mostly public assemblies, with local assembly where none existed, and 312 isolates from an ongoing genomic study now being submitted to SRA. Attribution was scored on a published 4,221-locus core-genome multilocus sequence typing scheme, under a holdout removing same-country references and same-source outbreak isolates, so no case was scored against its own epidemiological neighbors. Accuracy was measured against 46 cases from 45 individuals with documented exposure in 16 countries, and is reported per estimator, because the estimator is part of the number. Recombination detection was calibrated on this collection in separate work, not included here.

### Results — 1042 / 1250 characters (raw 1246)

Country attribution did not exceed chance. Nearest neighbor, the best country estimator, scored 10 of 46 (21.7%, 95% confidence interval 10.9 to 36.4) against a 26.1% majority-class baseline, exact binomial p = 0.80. Kappa reads 0.19 only against 3.0% marginal chance. Across twelve specifications country accuracy spans 0.000 to 0.261, and sub-national failed outright at 0 of 5. Region behaved differently. The modal label among the 20 closest genomes scored 41 of 46 (89.1%, 95% confidence interval 76.4 to 96.4) against a 45.7% baseline, p < 0.001. It was the only one of four tested to beat its baseline in every stratum. Nearest neighbor reached 80.4% but failed where a close relative existed. Asia versus elsewhere was recovered without error. Applied to the 2021 multistate aromatherapy outbreak with those genomes held out, the method placed the strain in South Asia (p = 2.8e-34). It could not separate India from the rest of South Asia (p = 0.351), reproducing the boundary the CDC investigation itself reached. Across 20 recurrence pairs, 19 relapses differed by 1 to 14 SNPs and one reinfection by 1,102, so resolution is not the limit. For 7 of 16 exposure countries no public genome exists, all in Latin America and the Caribbean.

### Conclusions — 380 / 500 characters (raw 450)

Genomic exposure attribution should be reported by geographic scale. A laboratory can state that a case is consistent with acquisition in South Asia. It cannot yet name the country, and these data do not support doing so. Closing the reference gap in Latin America and the Caribbean is necessary before anything finer. More references alone will not be enough, because country-level signal in this collection is not separable from collection history.

Total across the four fields: 2187 form characters, 2588 raw, against a 3,000 character ceiling.

---

## Why these numbers and not others

**Baselines stay in, every time.** "22%" on its own reads as partial success.
"22% against a 26% baseline" is the finding. The same holds for 89% against 46%.

**45 individuals, not just 46 cases.** Two isolates come from one patient. It
costs four words and answers the question before it is asked.

**The recurrence clause is measured on recombination-filtered SNPs, not
cgMLST.** `RESULTS_DRAFT_2026-08-23.md` §R3.1: for 16 of the 20 pairs the
distances "are the production per-unit Gubbins output itself". The attribution
is scored on cgMLST alleles. So "the same pipeline" overstated the link and is
gone. The defensible claim is the one the source's own heading makes, that a
finer distinction resolves on the same genomes, so the country failure is not a
resolution problem. "Separated" is also gone, because nothing was separated.
The distances simply differ, and the sentence now says so.

⚠ **These 20 pairs are Nakhon Phanom isolates.** §R3.1 opens "thirteen patients
in the Nakhon Phanom collection". **This corrects what open item 6 previously
said.** That item argued the clearance conversation was light because the
abstract reported no isolate-level result from the 312 in-house isolates. It
does: this clause is one. The partner conversation is heavier than stated.

**The recurrence clause earns its space.** The first objection to any negative
result is that a better method would have worked. The relapse and reinfection
separation answers it with the pipeline's own output rather than with an
argument. It is the sentence to protect if the Results box gets tight.

**Sub-national is now reported, at 0 of 5.** It was cut from the earlier drafts
because n = 5 invites a question the data cannot answer well. It goes back in
because Objectives promises three scales and Results has to deliver three, and
because the Results box has 300 characters spare. Quote the denominator with it
every time.

**The one-locus US and Vietnam clause.** Without it the work reads as "we did
not have enough reference genomes", which is only half the story and the weaker
half. With it, the ceiling is a property of the organism as well as of the
collection.

**The aromatherapy reproduction replaced the one-locus clause, and that is an
upgrade rather than a trade.** The dropped clause (a US autochthonous cluster one
cgMLST locus from a Viet Nam-acquired case) argued that the ceiling is a property
of the organism and not only of our panel. The aromatherapy result argues the
same thing harder, because **India is not a reference gap**: the panel holds 56
Indian genomes, and country still cannot be separated from the rest of South
Asia. That is absence of signal where coverage is good, which is the stronger
form of the claim and the reason Conclusions now says the reference gap is
necessary to close but not sufficient.

⚠ **Two p-values here are not in `NUMBERS.tsv`.** 2.8e-34 and 0.351 are quoted
from prose in `GROUPING_AND_CDC_2026-08-21.md` §1. `generate_numbers.py` does not
emit them, so they are the one place in this abstract that breaks the project's
own cite-do-not-restate rule. See `MAC_VERIFICATION_REQUEST_2026-09-24.md` §4.

**"How often the genome is correct" was a category error, and it overclaimed.**
A genome is not correct or incorrect. What was measured is how often an
*estimator* applied to genomic data recovers the documented exposure location,
so Objectives now names the assignment and reports *its* accuracy.

It also dropped a qualifier that matters. `PUBLICATION_STRATEGY_2026-09-02.md`
states the gap precisely: no published work reports a misclassification rate, a
confidence measure or a cross-validated accuracy figure **at any spatial scale
finer than a two-population continental split from MLST**. Unqualified, the
sentence claimed nobody had measured anything, while our own Results reports the
Asia-versus-elsewhere split recovered without error, which is exactly that
scale. "Below continental scale" restores it.

**Objectives had four pronouns in a row, and one had no antecedent.** "it is
assigned", "made it a domestic question", "Its accuracy", "We measured it". The
third was the broken one: exposure origin does not have an accuracy, an
assignment does. The noun was there and this file removed it. `cb90db4` wrote
"the accuracy of **that assignment**" and then, in the same commit while curbing
the novelty claim, replaced the phrase with "**Its** accuracy", dropping the
antecedent it had deliberately created two edits earlier. It now reads "the
accuracy of genomic assignment", which is self-contained and reaches back to
nothing, and the closing pronoun is named as "that accuracy".

**Novelty claims are curbed throughout.** Objectives previously said "no
published study reports the accuracy of that assignment below continental
scale". That is a priority claim, and an unqualified one invites a reviewer to
produce a counterexample. It now reads "its accuracy below continental scale is
not well established", which motivates the work without claiming to be first.
In Results, "the only estimator to beat its baseline in every stratum" reads as
absolute and is bounded to "the only one of four tested", which is what the
specification curve actually shows.

**The recombination work gets one clause, and no number.** "Recombination
detection was calibrated on this collection in separate work, not included
here." It does two jobs: it signals the workstream exists, and it stops a
reviewer assuming the attribution is recombination-corrected, which it is not,
since cgMLST allele calls are not Gubbins-filtered.

**r/m 7.70 was tried and does not fit.** Carrying the figure needs the operating
window to be explained, or the number is meaningless, and that version runs 783
of 750 characters even on the space-excluding count. The clause above is what
fits.

**The structure result goes in Conclusions, not Results, and carries no
number.** Results has six raw characters of margin, so nothing fits there
without cutting something load-bearing. Conclusions had room. The clause reads
"country-level signal in this collection is not separable from collection
history", which is `STATE_2026-09-02.md`'s own wording, and it holds across the
entire 6-to-26 specification range, so it costs nothing to defend.

**No number, deliberately.** Region's association index on the curated framework
is 0.193 and country's attribution kappa on the validation set is 0.193. Those
are different quantities on different frameworks and the match is coincidence.
Quoting either alongside the other invites a reviewer to assume one was copied
from the other. Qualitative, the collision cannot arise.

**Sentence length.** Results had a 41-word and a 45-word sentence against a
house limit of about 35. Both are split, the longest is now 27 words, and the
split cost one character.

**Left out on purpose.** The recombination operating range and r/m 7.70 are
load-bearing for the methods paper, not for this audience. The abstention rule
(region 94% on 76% of cases at an allelic distance of 0.462) is a good slide and
a poor abstract sentence, because it needs the threshold explained. The South
Asia burden inversion (2.5% of genomes, 44% of predicted cases) is a strong
closing slide for the same reason.

---

## Open items before submission

1. **Statistical significance. Computed, but not yet in `NUMBERS.tsv`.**
   `attribution_significance_bp.py` generates it, and the abstract now carries
   the result. Run these two on the Mac and append the rows, so the figures come
   from the generator like every other number:

   ```
   python3 attribution_significance_bp.py --correct 10 --n 46 \
       --baseline-correct 12 --label attribution.country.nearest_neighbour --tsv
   python3 attribution_significance_bp.py --correct 41 --n 46 \
       --baseline-correct 21 --label attribution.region.modal_k20 --tsv
   ```

   The inputs are counts already frozen in `RESULTS_DRAFT_2026-08-23.md`
   (10/46 and 41/46, with majority classes 12 and 21 of 46, which give the
   published 26.1% and 45.7% baselines), and the arithmetic needs no basis
   files, so the value does not depend on where it runs. What the Mac run adds
   is the audit trail.

   **The interval reads wider than the design strictly justifies**, and the
   script prints why: the baseline is estimated from the same 46 cases, and the
   trials are not independent, since the set is 46 genomes from 45 individuals
   with outbreak groups held out together. A label-permutation test over the
   per-genome assignments would be the better instrument and needs the holdout
   output rather than these counts. Worth doing before the manuscript, not
   before October 2.
2. **Field limits. Settled.** The form caps each field separately at 500, 750,
   1,250 and 500 characters, counting characters without spaces. Every field
   above fits with margin under both counting conventions. Nothing to do.
3. **Author list and order.** Not drafted. [AUTHORS] is a placeholder.
4. **Revalidate every number** against `NUMBERS.tsv` on the current frozen
   basis. The panel figure in particular: 2,959 is the deduplicated panel and
   2,976 is the count of assemblies considered, and the two are not
   interchangeable.
5. **"41% of publicly archived isolates with a recorded country"** is the
   careful phrasing. Read as "41% of all public *B. pseudomallei* genomes" it is
   wrong, and the correct figure there is 36.8%.
6. **Select agent and partner clearance. Reassessed, and it is heavier than
   this file first claimed.** `PUBLICATION_STRATEGY_2026-09-02.md` flags data
   availability as the highest-risk item across all three papers, because the
   metadata joins accession to location, date and exposure label.

   ⚠ **An earlier version of this item argued that "no partner institution has
   to release unpublished isolates for this abstract to go out". That was
   wrong**, and it was the main practical reason given for preferring this
   submission over the Nakhon Phanom one. The panel contains **312 unpublished
   in-house Nakhon Phanom isolates**, undeposited, and they are part of the
   2,959 the abstract reports. Whoever owns those isolates has standing here.

   Two things soften it but do not remove it. `MANUSCRIPT_OUTLINE_2026-08-21.md`
   records that the epidemiology team handled the IRB for all 312. And the
   abstract reports no isolate-level result from them: they are panel
   background, not the finding. That is a much easier conversation than
   presenting paired household distances, but it is still a conversation to
   have before October 2 rather than after.

   **One discrepancy to settle on the Mac.** `METHODS_DRAFT_2026-08-19.md`
   §2.12.11a.2 describes the 48 exposure-labelled genomes as CDC submissions,
   named older assemblies and published cases, all public.
   `BIOPROJECT_COUNTERFACTUAL_2026-09-02.md` §3 instead says "the in-house
   isolates that make up much of the validation set carry `bioproject =
   unknown`". Those cannot both be right, and which is true decides whether
   partner isolates are in the **headline 46** or only in the reference panel.
   Check `EXPOSURE_OVERRIDES.tsv` against the `IP-`/`IE-` list before
   submitting.

7. **Relationship to the manuscripts.** This is the attribution work, listed as
   Paper 3 in the publication strategy and the least finished of the three. The
   abstract cites calibration work that is still unpublished. That is normal for
   a conference, but the talk needs one slide on why the recombination
   correction is trustworthy.

---

## Corroborating material from the Burk-Genome closeout deck

**Separate project. Do not merge these numbers with the ones above.** The deck
is `BurkGenome_close_KK260812_final.pptx`, presented by Kornthara (Yuyi) Kawang
at the first-phase closeout, and it reports the Nakhon Phanom study: 312
*B. pseudomallei* genomes (259 patient, 53 environmental) set inside a curated
**2,773**-genome global framework. The abstract above uses a **2,959**-genome
panel built for a different question. The two frameworks are not the same object
and a figure from one must never be quoted against the other.

What the deck is useful for is the **talk**, not the abstract.

**It independently corroborates the scale-dependence conclusion.** Slide 25
reports an association index for how strongly each trait tracks the phylogeny,
where lower means more structured, all at p < 0.01:

| trait | association index |
|---|---|
| geographic region | 0.193 |
| country | 0.236 |
| collection decade | 0.581 |
| isolation source | 0.710 |
| Thai province | 0.721 |

Region is more structured than country, and province is close to unstructured.
That is the same ordering the attribution result gives from a different
collection and a different statistic, and it is worth one slide. It is
corroboration, not evidence to restate as though it were ours.

**Slide 27 explains the mechanism behind the country failure.** Australasia is a
genetically isolated reservoir, while mainland Southeast Asia is one continuous
mixed population crossing national borders. That is precisely why the Asia
versus elsewhere split comes back without error while country does not, and it
answers the obvious question from the floor better than any restatement of the
accuracy table.

**Slide 3 sharpens the Georgia case for the background.** Two men admitted after
Hurricane Helene in September 2024 with no travel history, matched by CDC to two
fatal cases in the same county in 1983 and 1989 carrying the same genotype, four
genomes differing by fewer than 20 SNPs across four decades, and the closest
relatives worldwide in Vietnam. Brennan *et al.*, *Emerg Infect Dis*
2025;31(9), which is the same record this repository cites as PMID 40835221.
