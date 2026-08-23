# Discussion — draft prose, 2026-08-23

Written from the outline's D1–D5 arcs on the frozen basis, incorporating this
session's material. **Figures annotated with their `NUMBERS.tsv` keys** in
`[brackets]`; strip before submission. Companion to
`RESULTS_DRAFT_2026-08-23.md`.

---

We set out to test whether the country in which a melioidosis patient acquired
their infection can be recovered from the genome of the infecting isolate. Across
**2,959** genomes `[panel.corrected_v4d]` and **46 scorable cases** with
independently documented exposure `[validation.scorable]`, it cannot. Country
attribution reached **10 of 46 (21.7%)** against a **26.1%** majority baseline —
κ 0.193 — while regional attribution reached **41 of 46 (89.1%)** against a 45.7%
baseline, κ 0.832 `[attribution.*, ladder.*.kappa]`. Sub-national attribution
failed entirely.

The value of this result is not that our estimator failed. It is that the failure
is **structured, measurable and explicable**, and that the same data show exactly
where the recoverable signal stops.

## The negative result is the useful one, and three findings license it

A negative result invites the reply that a better method would succeed. Three
features of this study are designed to answer that.

**First, the estimator demonstrably works when signal exists.** Region and
country were scored on the same genomes, the same reference pool and the same
holdout, and differ by three-quarters of a κ unit. Randomly subsampling loci from
2 to 4,089 raises regional accuracy from 49.5% to 82.1% while country accuracy
stays flat at zero — a built-in positive control showing that the method converts
resolution into accuracy whenever resolution helps.

**Second, the failure is invariant to resolution.** Across a 584-fold span in
locus count — 7 MLST loci, 4,221 cgMLST loci, and whole-genome
recombination-filtered SNPs — country attribution never clears its baseline. A
finer instrument does not help because the quantity being measured is not there.

**Third, the failure is invariant to the analytical framework.** The result holds
under a lineage partition and under two partition-free typing systems, so it is
not an artefact of how we defined units.

Taken together these license the stronger claim: **for most source countries in
this collection, exposure country is not recoverable from the genome by any
method, until those countries are sequenced.**

## Attribution reaches exactly as far as the reference panel, and no further

The most generalisable finding here is a single mechanism visible at three
scales. **At country scale**, attribution fails where no same-country reference
exists — and **7 of our 16 source countries have no public genome in ENA at
all**, every one of them in Latin America and the Caribbean. **At regional
scale**, the misses concentrate on regions the panel barely represents: both
sub-Saharan African genomes in the no-relative stratum are confidently assigned
to Latin America. **And at the level of the individual case**, the genomes that
cannot be placed at all are disproportionately the sole panel representative of
their exposure country.

One mechanism, three observations: **a genome can only be attributed to a place
that is already in the reference set.** This applies to any pathogen with an
uneven reference panel and is, we think, the result most likely to transfer
beyond *B. pseudomallei*.

But absence of references is not the whole mechanism, and two findings show why.
**Mexico retained genuine same-country references under leave-group-out — three
in a thirty-genome pool — and attribution still failed.** And the sharpest case
is one where the reference condition is fully satisfied.

## When both countries are represented and attribution still fails

A single lineage in this collection contains five genomes from four patients in
Georgia, USA, spanning 1983–2024 — reported after epidemiologic investigation as
presumptive autochthonous cases with no recent international travel — together
with isolates from a Viet Nam-exposure patient and three isolates collected in
Viet Nam by two independent studies. Both countries are represented, by separate
laboratories, with published epidemiology on both sides.

**The Georgia cluster's internal maximum allelic distance is 8.67 × 10⁻³, and its
nearest neighbour among all 3,033 genomes is a Viet Nam-acquired case at
8.91 × 10⁻³ — a separation of one locus in 4,221.** No distance threshold places
those on opposite sides reliably.

This is a different and harder failure than absence of references. The lineage is
simultaneously established in the southeastern United States and Asian in
ancestry; the published investigation leaves open that the Georgia environmental
focus may itself derive from Vietnam-War-era introduction. **A genome drawn from
such a lineage does not have a country of origin to recover** — not because the
data are missing, but because the organism's history does not respect the
question. Comparable cases are on record: a *B. pseudomallei* isolate from a
Second World War prisoner of war, presumed to represent 62-year latency after
Southeast Asian exposure, was reassigned by genomic analysis to Central or South
America.

That two of our validation genomes are wrong at *every* geographic scale under a
nearest-neighbour rule — including the otherwise perfect Asia/non-Asia split —
because their closest relative in the collection lies across the Pacific, is the
same phenomenon measured at the level of a single call.

## Two failure modes, and a system that knows which one it is in

Because the estimator answers confidently even when no relative exists, we paired
it with an abstention rule: where no genome lies closer than 0.462 allelic
distance, return *unattributable*. Reported out-of-sample, it answers **76.1%**
of cases at **94.3%** accuracy `[abstention.region.*]`, and declines **both**
sub-Saharan African misattributions.

Reporting it honestly requires two baselines, and they disagree. Declining cases
at random leaves the expected error rate unchanged, so the first baseline is
simply the answer-everything accuracy. But abstention also changes the class mix,
so the **majority share of the retained subset** must be reported too — and it
rises from 45.7% to 50.0%. Lift over chance therefore improves only from +43.4 to
+44.4 points. **The rule's value lies in which errors remain, not in the accuracy
figure**, and we report it that way.

More importantly, the rule addresses only one of two distinct failure modes.

- **Attractor errors** arise when no real relative exists and the genome snaps to
  whatever small cluster is least unlike it, with a catch-all regional label
  converting that into a confident answer. These are **catchable**, and the rule
  catches them.
- **Depth-ceiling errors** arise when close relatives genuinely exist but are
  geographically uninformative, because the lineage spans the geography. These
  are **not catchable by any confidence signal of this kind** — the Georgia and
  Mississippi genomes rank 26th and 27th of 46 in abstainability while being
  wrong.

**Abstention on distance therefore mitigates sparse sampling, not shared
ancestry.** Distinguishing the two matters operationally: the first improves with
more sequencing, the second does not.

**Nor does abstention rescue country attribution, and we report the attempt.** Its
best country operating point reaches 37.5% selective accuracy against an
answer-everything 21.7% — an apparent gain of nearly 16 points, reproduced
exactly out-of-sample. But the retained-subset majority baseline is **also exactly
37.5%**: on the half of cases the rule elects to answer, always guessing the
commonest exposure country performs identically. The apparent improvement is
entirely a change in class mix.

What emerges is not a single answer but a **ladder of claims**, each with its own
evidence: *Asia versus elsewhere — recovered without error (κ 1.000). Region —
recoverable where a relative exists, with the system stating when one does not.
Country — not recoverable, and not rescued by declining the hard cases.*

## The same curve in another organism

Geographic source attribution has been reported to succeed elsewhere. A
hierarchical machine-learning study of *Salmonella enterica* serovar Enteritidis
attributed 2,313 genomes to four continents, eleven sub-regions and 38 countries,
reporting macro F1 of 0.954, 0.718 and 0.661 respectively.

We read that as **corroboration rather than contradiction**, for two reasons.
Its accuracy decays monotonically with geographic depth — the same shape we
report, from near-perfect at the deepest split to weakest at country — and its
authors attribute the country-level shortfall to the same mechanism we identify,
noting a correlation between scarce training data and poor prediction, with
United States samples consistently misclassified. **Two organisms, one curve,
sampled at different points on it.**

That *S.* Enteritidis retains usable country signal where *B. pseudomallei* does
not is itself consistent with our thesis. It is comparatively clonal and
geographically structured, its classes are countries commonly visited by UK
travellers and correspondingly well referenced, and the surveillance archive
behind it is orders of magnitude denser than the entire public
*B. pseudomallei* record. *B. pseudomallei* is environmentally acquired, highly
recombinogenic — in-window r/m 7.70 `[rm.median_gate1]`, with roughly 91% of raw
pairwise distance attributable to imported DNA — and carries lineages that span
continents.

Two methodological cautions belong with any such comparison. Evaluations in this
area typically use **random, class-stratified splits**, which do not separate
near-identical genomes of one lineage between training and test; our own country
attribution reaches 29–37% under an equivalent design and falls below baseline
only under leave-group-out. And **accuracy and macro-averaged F1 are not
interchangeable** on strongly imbalanced class sets. We would encourage
phylogeny-aware evaluation as the default in this literature.

## Where the collection is, and where the disease is

The strongest public-health finding here needs no model. Assigning the
region-labelled panel to World Bank regions and comparing with predicted
melioidosis burden, **East Asia and the Pacific is sampled 41 times more heavily
per predicted case than South Asia and 33 times more heavily than sub-Saharan
Africa**. South Asia is predicted to carry 44.2% of global cases and contributes
2.5% of genomes; East Asia and the Pacific carries 39.4% and contributes 91.8%
`[panel.region.*]`.

The same gap appears at country level: **21 countries with at least 100 predicted
annual cases have no public genome at all**, together roughly 5% of estimated
global burden, and **19 of the 21 are sub-Saharan African**.

> The country label attached to a genome in this collection is not primarily
> measuring where the organism lives. It is measuring where sequencing happened.

This yields two distinct recommendations, and conflating them would be a mistake.
The first is derived from what is already downloadable and would most improve
*this* analysis. The second follows from the burden comparison and matters more:
the highest-value sequencing is in countries where **nothing exists to download
at all** — across South Asia and sub-Saharan Africa. The first list is drawn from
a frame that is itself biased; the second is drawn from where the disease is.

## What this means for outbreak response

Cluster membership and geographic origin are different questions, and this study
answers them differently. Within the Gulf Coast lineage, isolates differ by a
median of 5 recombination-filtered SNPs while the nearest genome outside it lies
roughly 490 SNPs away — so **assigning a new case to that lineage is
unambiguous**, and the call is never borderline. That operational capability is
real and is already in use.

But the same data cannot state where the lineage came from: its nearest outside
relative is *the nearest in this panel*, not *a near relative*. **"We sequenced
it" answers whether this case belongs to a known cluster; it does not answer
where the patient was exposed.** Keeping those separate is how genomics avoids
being over-promised to an incident team.

## Limitations

**The validation set is small and structured.** Forty-six scorable cases from
**45 individuals** — two isolates come from one patient — drawn from 16 exposure
countries, with the Philippines contributing 12. Sixteen of the 46 come from a
single assembly batch representing 5.9% of the panel; we verified that this does
not bias the distance strata (Spearman ρ = −0.247, n.s., with median loci
compared flat across strata), but the non-independence is real and we report it
rather than leaving it to be found.

**The regional task is effectively coarser than seven-way.** Five of seven World
Bank regions are represented among scorable cases, and the classes are unevenly
filled. "Regional attribution works" should be read as the specific,
operationally relevant discrimination it is, not as a general seven-way
assignment.

**The abstention threshold is calibrated on 46 genomes.** Leave-one-out removes
threshold-selection circularity but not signal-selection circularity: three
candidate signals were compared on the same set and nearest-neighbour distance
was chosen partly because it performed best. The value 0.462 is specific to this
scheme and this panel and should be re-derived, not transferred.

**Assembly method affects the measurements.** On four isolates assembled both
ways, SPAdes versus SKESA shifted core completeness by a median of +10.8
percentage points and mash distance by −27%, and the effect is per-genome rather
than uniform. Our panel mixes assembly provenance, so mash-derived quantities are
not strictly comparable across it; the reported diversity window and the cgMLST
attribution avoid this by using alignment-derived and allelic distances
respectively.

**Two partitions exist for this collection.** We report the corrected
85-unit partition and use the 88-unit run as a cross-hardware reproducibility
control; the two agree closely, but unit labels are not comparable between them
and must never be quoted across partitions.

**Finally, this is a study of the public record as it stands, and we cannot
separate the two causes of failure quantitatively.** Most of the country-level
failure we observe is associated with absent references, which is a statement
about the archive; but the Georgia and Mississippi cases show that some of it
arises from lineages that genuinely span continents, which is a statement about
the organism. **We can demonstrate that both contribute. We cannot say in what
proportion**, because the cases where references exist are too few — 14 of 46 —
to estimate it. Sequencing the countries currently at zero is a testable
intervention, and it would also be the experiment that separates the two.

## Conclusion

Exposure country cannot presently be recovered from the *B. pseudomallei* genome
for most source countries, and this is not a limitation of resolution or of
method: the same data, estimator and holdout recover region at κ 0.832 and the
Asia-versus-elsewhere split without error.

Two things stand between a genome and a country, and they differ in kind rather
than in size. **Sparse reference sampling is the tractable one**: seven of our
sixteen source countries have no public genome at all, and for those cases no
method can succeed. Sequencing where the record is empty would address this
directly, and we recommend it on public-health grounds regardless of what it does
for attribution. **Shared ancestry across continents is the stubborn one**: where
a lineage is established on two continents — as the Georgia and Viet Nam isolates
are, one locus apart — there may be no country-level answer to recover, and more
sequencing would sharpen the description of that lineage without making the
question answerable.

We resist calling either the dominant cause. It is tempting to treat sparse
sampling as the main effect because it is the more visible, but **country
attribution failed for 12 of the 14 cases that did have a close relative
available** — the regime in which sampling is not the limitation. On these data
the stubborn mode is not a small residue.

We therefore do not claim that sequencing alone would deliver country-level
attribution, and our data cannot say how much of the gap it would close. What
they do support is narrower and, we think, more useful: **report a graded claim
rather than a single answer, decline when no comparable genome exists, and treat
a confident country call on a continent-spanning lineage as the failure mode that
no confidence measure will catch.**
