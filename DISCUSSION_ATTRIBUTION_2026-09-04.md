# Discussion: the resolution ceiling on genomic source attribution

Draft, 2026-09-04. Written against the frozen basis (85 units, 2,340 genomes) and
the 46 scorable validation genomes. Every number here is in `GROUPING_LADDER.tsv`,
`GROUPING_PREDICTIONS.tsv`, `ABSTENTION_OPERATING_POINTS.tsv` or `NUMBERS.tsv`.

**Placement note.** This is the attribution discussion, not the recombination
one. The current manuscript reports geographic *structure* (Results 8) and cites
the absence of any published attribution accuracy only as motivation. This
material either becomes a new Results section plus these paragraphs, or it is the
core of the second paper. It should not be merged into the existing Discussion
without that decision being taken first.

---

## The ceiling is real, it is measurable, and it sits between country and region

The question this collection was assembled to answer is where a melioidosis case
was acquired. The answer is that a genome will tell you the region and will not
tell you the country, and the gap between those two statements is not gradual.

Across 46 validation genomes with a registered country of exposure, region-level
attribution is correct for 41, an accuracy of 89% against a majority baseline of
46%, with Cohen's kappa of 0.832. Country-level attribution is correct for 10, an
accuracy of 22% against a majority baseline of 26%. **Country attribution does not
merely perform poorly. It performs below the strategy of ignoring the genome and
labeling every case Thailand.** Kappa of 0.193 formalizes what that comparison
already shows.

No study has previously published an attribution accuracy or a misclassification
rate for *B. pseudomallei* at any spatial scale, so there is no prior estimate to
compare against and no established expectation to revise. That absence is the
reason a measured ceiling, with the controls that establish it as a ceiling rather
than an unlucky run, is worth reporting even though half of it is negative.

## The failures are not noise, and identifying what they are is the result

Five genomes are misplaced at region level. They are not distributed across the
confusion matrix in the way classifier error usually is. Four of the five land in
a single cell, and each of the three mechanisms behind them is identifiable.

**Two are a lineage that genuinely spans the label boundary.** Both misplaced
North American genomes are from the Mississippi Gulf Coast focus, and they belong to
a sequence type that is pan-American. Thirty-six genomes in the panel carry their
exact seven-locus profile, distributed across seven countries every one of which is
in the Americas: the United States (26), Mexico (3), Brazil (3), Guadeloupe,
Martinique, Colombia and Nicaragua. The regional scheme divides that single lineage
between two of its regions, so a genome from it can be scored wrong at region level
without anything having gone wrong genomically.

The same fact is visible in the analysis panel. Both genomes sit in `strain_4_L1_1`,
a unit of 22 comprising 21 from the United States and one from Colombia. Validation
requires holding out the entire outbreak rather than the single genome being scored,
because the Mississippi cases sit within 0.005 allelic distance of one another and
scoring one against its siblings measures nothing. Once the outbreak is held out, the
only member of that lineage remaining in the panel is the Colombian genome, at a
distance of 0.153. The panel answers Latin America and Caribbean because that is the
only evidence left standing, and for a lineage of this distribution that answer is
arguably the true one. It is scored wrong because the label is a political boundary
and the lineage is not.

**Two are sparsity compounding a real phylogenetic adjacency.** Both African
genomes are misplaced into Latin America and Caribbean. For the Nigerian genome the
single nearest genome in the panel is itself Nigerian, and a nearest-neighbor
estimator places it correctly; the 20-neighbor vote does not, because beyond the
first neighbor the neighborhood fills with American genomes. There are too few
African references for a neighborhood of any size to remain African. The direction
of the error is not arbitrary either. South American isolates have been reported to
fall within the African clade, consistent with dissemination from West Africa to the
Americas, so the region the classifier reaches for is the one the published
phylogeny already links to Africa.

**One is ordinary error.** A Thai genome whose nearest relative anywhere in the
panel is a Sri Lankan genome at a distance of 0.721 is placed in South Asia. Nothing
in the collection is close to it, the vote share of 0.65 is the lowest recorded for
any of the 46, and no phylogeographic story is needed to explain it.

Two consequences follow. First, **every region represented by six or more validation
genomes is correct 41 times out of 42**; all five errors fall in the two regions
represented by exactly two genomes each. That is a statement about reference
sampling, and it comes with a remedy.

Second, and more sharply than a confusion matrix shows: **of the seven regions in the
scheme, the 20-neighbor vote only ever emits three.** East Asia and Pacific, Latin
America and Caribbean, and South Asia are the only labels it returns for any genome
in the set. North America, Sub-Saharan Africa, Europe and Central Asia, and Middle
East and North Africa are not wrong answers, they are unreachable ones, because no
region sampled that thinly can win a vote of twenty. A nearest-neighbor estimator
reaches six of the seven. This is the price of the more robust estimator, and it
should be stated as a trade rather than left implicit: the 20-neighbor vote corrects
five of the nearest-neighbor errors and introduces one, moving region accuracy from
37 to 41 of 46, and it buys that by collapsing the output space onto the three
densest regions. A confusion matrix built only on the observed rows hides this
entirely, because the unreachable regions look merely untested.

## Coarsening only helps when it follows the phylogeny

The ladder from country to region to hemisphere is not monotone in the number of
classes, and the exception is instructive. Separating Southeast Asia from everything
else is a two-class problem and reaches kappa 0.461, well below the five-class
regional grouping at 0.832. Separating Asia from everything else is also a two-class
problem and reaches kappa 1.000, with no observed error.

The difference is not granularity, it is whether the boundary coincides with a
division the phylogeny already makes. Asia against the rest tracks the deepest split
in the species, the one separating the ancestral Australasian reservoir from the
populations derived from it. Southeast Asia against the rest draws a line through
the interior of the densest and most recombinogenic part of the tree, where
diversity is continuous across the borders being used to divide it.

The practical form of this is that attribution cannot be rescued by coarsening
alone. A scheme that aggregates countries into groups which do not correspond to
clades will inherit the country-level failure at a coarser grain, and will do so
while appearing more defensible because it has fewer classes. Groupings must be
chosen along the grain of the tree, and the fact that a grouping is coarse is not
evidence that it is easier.

## More markers lift the region and do not rescue the country

The obvious objection to a country-level negative is that it reflects insufficient
resolution rather than an absent signal, and that a denser typing scheme would
recover it. The same validation genomes scored on seven-locus MLST rather than the
4,221-locus core-genome scheme answer that directly.

On seven loci, region attribution is correct for 17 of 33 scorable genomes, 51.5%
against a majority baseline of 45.5%, which is barely distinguishable from the
baseline. On 4,221 loci it is correct for 41 of 46, 89% against a baseline of 46%.
Region attribution is therefore strongly resolution-limited, and the additional loci
are what make it work.

Country attribution does not behave that way. On seven loci it is correct for 0 of
33. On 4,221 loci it is correct for 10 of 46, which is 22% against a baseline of 26%
and therefore still no better than ignoring the genome. **Three orders of magnitude
more loci move region from marginal to reliable and leave country below its own
baseline at both ends.** The two denominators differ, 33 against 46, because fewer
genomes are scorable on the MLST scheme, so the comparison is between trends rather
than between paired figures; the direction is nonetheless unambiguous.

This is the strongest available evidence that the country-level ceiling is a property
of the organism and its sampling rather than of the marker set. Densifying the scheme
is a solved problem and it does not help. What the failing regions need is references
from places that have none, which is a different and harder problem than sequencing
more of what is already represented.

## Abstention converts ignorance into a declared limit, and does no more than that

Because the collection is unevenly sampled, an obvious refinement is to decline the
cases the panel is least equipped to answer. Distance to the nearest panel genome is
the only signal that provides any lift. Declining the 22% of cases whose nearest
neighbor lies beyond an allelic distance of 0.462 raises accuracy on the remainder
from 89.1% to 94.4%, and the operating point is stable out of sample, at 94.3%
selective accuracy over 76.1% coverage under leave-one-out.

Two qualifications keep that in proportion. The gain is 5.3 percentage points, which
is real but modest, and it is purchased by declining to answer roughly one case in
five. More importantly, **abstention cannot protect against the failure mode that
matters most here.** It declines three of the five errors, all of them cases where
nothing close exists. It cannot decline the two Mississippi errors, because those
genomes have a genuine close relative and are called with a vote share of 0.85 and a
margin of 0.70, which is as confident as the median correct call. Confidence does not
separate the errors from the successes: correct calls have a median vote share of
0.85 and the errors reach 0.85 as well.

The honest description is therefore narrow. Abstention makes ignorance explicit when
ignorance is the problem. It offers nothing against a lineage that truly spans the
boundary the label draws, and such a lineage will be reported confidently and
incorrectly.

## What this licenses

A laboratory working from a genome and this panel may report the region of probable
exposure, may report Asia against non-Asia and eastern against western hemisphere,
and may decline to answer with a stated and validated threshold. It may not report a
country. It may not report a country even when a close match exists, which is the
circumstance in which country attribution performs worst, at 2 correct of 14. It may
not return North America or Sub-Saharan Africa as a positive finding at all on the
present panel.

That is a narrower claim than the one this field has been reaching for, and it is a
usable one. A regional attribution delivered with a calibrated accuracy and an
explicit refusal to go further is more useful to an investigation than a country
name with no error rate attached, which is what the absence of any published
misclassification rate has meant in practice.

## What bounds the claim

The validation set is 46 genomes and five regions, two of which carry two genomes
each; the regional estimate is correspondingly better determined for East Asia and
the Pacific, Latin America and the Caribbean, and South Asia than for the rest. The
reference panel is approximately two-thirds Thailand, so the country baseline of 26%
is set by a single country and the regional baseline of 46% by a single region. The
attribution distances are cgMLST allelic distances on a 4,221-locus scheme, and the
operating threshold for abstention is a property of that scheme and this panel rather
than a species constant. None of these bounds is repaired by adding genomes from
countries already well represented; what the two failing regions need is references
from the Americas outside Colombia and from Africa, which is a specific and
actionable request rather than a general call for more data.
