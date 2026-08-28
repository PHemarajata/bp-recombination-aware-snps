# Genomic attribution of exposure country in *Burkholderia pseudomallei*

**Manuscript draft, compiled 2026-08-28.**

This document contains the current draft of each written manuscript section:
Abstract, Methods, Results and Discussion. The Introduction has not yet been
written and is not represented here.

All figures are computed on a single analysis basis: 2,959 genomes in the panel,
of which 2,340 fall in 85 recombination-aware analysis units.

---

## Contents

1. Abstract
2. Introduction (not yet written)
3. Methods
4. Results
5. Discussion

---

# 1. Abstract

*Burkholderia pseudomallei* causes melioidosis throughout the tropics, and cases
increasingly present in patients with no travel history, where clinicians and
public health agencies ask genomics to supply the place of exposure. We assembled
2,959 genomes, 41% of country-labelled public isolates, and tested whether
exposure country is recoverable, using 46 cases from 45 individuals with
independently documented exposure as ground truth. Under a holdout removing both
same-country validation genomes and same-source outbreak isolates, country
attribution did not exceed chance: 10 of 46 (22%) against a 26% majority
baseline, κ 0.19. Regional attribution reached 41 of 46 (89%) against a 46%
baseline, κ 0.83, and the deepest split, Asia versus elsewhere, was recovered
without error (κ 1.00). The contrast is sharpest where attribution should be
easiest: among the 14 cases with a close relative in the panel, region was
correct 14/14 and country 2/14. Country accuracy remained flat across a 584-fold
range of resolution, from 7 MLST loci to whole-genome recombination-filtered
SNPs, while regional accuracy rose from 50% to 82% over the same range,
indicating absence of signal rather than insufficient resolution. Two causes are
separable in kind: for 7 of 16 exposure countries no public genome exists, all
seven in Latin America and the Caribbean; and some lineages span continents, with
a published US autochthonous cluster and a Viet Nam-acquired case differing by
one cgMLST locus in 4,221. Declining to answer where no relative lay within 0.462
allelic distance raised regional accuracy to 94% on 76% of cases out of sample,
but did not rescue country attribution. Reporting should therefore be graded by
geographic scale. The collection is also inverted against disease burden: South
Asia contributes 2.5% of genomes and 44% of predicted global cases.

---

# 2. Introduction

Not yet written.

---

# 3. Methods

## 3.1 Genome panel

2,976 *B. pseudomallei* assemblies were considered: 2,802 from an established
curated collection and 174 newly added isolates. Seventeen assemblies were
removed as duplicate BioSamples, giving an analysed panel of 2,959 genomes
spanning 50 countries. Of these, 312 are in-house isolates not represented in
public archives.

To place the panel in the context of the public record, the European Nucleotide
Archive was re-censused as a union of read-run and assembly depositions, a union
being necessary because a read-run-only query is blind to assembly-only
submissions.

## 3.2 Species identification

Species identity was confirmed for all assemblies by three criteria. First, Mash
distance to *B. pseudomallei* K96243 of 0.012 or less, which excludes
*B. thailandensis*, *B. oklahomensis* and *B. humptydooensis*; these sit at 0.064,
0.081 and 0.066 from K96243 respectively, roughly seven times further than any
genome in the collection. Second, assembly size between 6.3 and 7.6 Mb. Third,
presence of at least 50% of 540 cgMLST loci that are present in *B. pseudomallei*
reference genomes and absent from all eight complete *B. mallei* genomes examined.

The third criterion is required because *B. mallei* is a host-restricted,
genome-reduced clone that arose within *B. pseudomallei* diversity and is not
separable from it by sequence similarity: the *B. mallei* reference lies 0.0101
from K96243, inside the Mash gate. Held-out validation across all 70 four-versus-
four splits of the *B. mallei* panel gave a worst-case held-out *B. mallei* score
of 0.061 against a worst-case *B. pseudomallei* score of 0.685.

All assemblies satisfied all three criteria except 20 that exceeded the upper
size bound and were retained after review.

## 3.3 Partition into analysis units

The analysis unit is a fastbaps level-1 sub-cluster within a PopPUNK strain,
retained at n ≥ 7. The rule was applied uniformly: no lineage was subdivided
because it was large, and none was left whole because it was small.

Strains were assigned with PopPUNK v2.7.6 over all assemblies (k = 15 to 31, step
2), fitted with a Gaussian mixture (bgmm, K = 5) followed by boundary refinement,
yielding 310 clusters of which the largest held 901 genomes. Within each strain,
PopPIPE built a split-k-mer alignment (SKA v0.4.0), a neighbour-joining guide tree
and a fastbaps hierarchical partition (levels = 3), analysed at level 1.

After partitioning and the exclusions above, 2,340 genomes fall in 85 analysis
units of size 7 to 159 (median 18), spanning 170 replicon-units.

## 3.4 Alignment, recombination correction and r/m

Within each unit, reference-based variant calling was performed with Snippy 4.6.0
against a per-unit reference, with replicons split and replicons below 100 kb
discarded, so that no alignment spans a contig junction. Recombination was removed
per unit with Gubbins 3.4.3 at 5 iterations, minimum 3 SNPs per recombination
block, hybrid tree builder disabled and starting tree skipped.

These parameters are pinned rather than left at defaults because Gubbins settings
shift r/m by 0.47 to 0.78-fold non-uniformly, with no correction factor, so
estimates obtained under different settings cannot be pooled.

r/m is pooled rather than averaged: the sum of SNPs inside recombinations divided
by the sum of SNPs outside, summed over branches and over both replicons of a
unit. Units were assessed within a diversity window derived from alignment
distances; within that window the median r/m is 7.70 across 47 units. Across the
170 replicon-units the median ratio of filtered to raw pairwise distance is 0.090,
indicating that approximately 91% of raw pairwise distance is imported DNA rather
than inherited mutation.

### 3.4.1 The recurrence control

Thirteen patients in the Nakhon Phanom collection had culture-confirmed recurrent
melioidosis, giving 29 isolates and 20 episode pairs. Patient identity, episode
number and collection date come from the clinical record; all 40 isolate-date
assertions were verified against the collection metadata.

Distances were obtained on two independent bases. For the 16 pairs whose isolates
share an analysis unit, the distance is read directly from that unit's Gubbins
output as the number of recombination-filtered sites at which the two sequences
differ, counting only positions unambiguous in both and summing across replicons.
For all 20 pairs, including the four that no single unit contains, a local context
analysis was run over the 259 genomes from the same collection: single-linkage
clustering of mash distances at a 0.002 radius gave seven groups covering every
pair, each group padded to a minimum of 12 genomes. Each group was then put through
the chain of §3.4 at the same parameters, with Snippy against the group medoid,
a whole-genome alignment retaining invariant sites, Gubbins, and IQ-TREE under
GTR+ASC with 1,000 ultrafast bootstrap and SH-aLRT replicates.

Two departures from the production settings are deliberate. The snippy-core
Reference record is dropped, because here the reference is a member of the group
and would otherwise duplicate a sample. Gubbins is given an explicit seed, which
the pipeline omits; without one it draws an unseeded integer for the RAxML seed
and RAxML rejects a value of zero.

For each pair we also report the distance to the nearest genome in the same group
belonging to a different patient, which tests whether a locally circulating clone
could explain the second episode equally well. r/m is not reported for these
groups: they are tight single lineages built to a 0.002 radius, below the
diversity window in which recombination is detectable, so a low value there would
reflect detection failure rather than biology.

## 3.5 Phylogenies

Per-unit maximum-likelihood trees were built with IQ-TREE 2.2.6 on
recombination-filtered alignments. A global core-genome alignment was produced
with parsnp 1.7.4.

## 3.6 Association between phylogeny and geography

For each unit, the minimum number of geographic label changes on the
recombination-corrected topology was computed by Fitch parsimony and compared
against a null distribution built by permuting the observed labels across the tips
of the same tree, 1,000 times. Permuting only the assignment of labels holds both
the topology and the exact multiset of labels fixed, which is necessary on a
collection this skewed.

BioProject was tested identically on the same trees as a companion control, on the
reasoning that isolates sequenced together are frequently related for reasons
unrelated to geography. A unit is reported as carrying geographic signal only
where geography is significant after Benjamini-Hochberg correction at 5% and
BioProject is not, with the BioProject control counted as informative only where
it covers at least 70% of tips across at least 3 distinct projects.

Units in which every genome carries the same label are reported as uninformative
and excluded from all counts of significant units.

The test was run at three scales, differing only in the label column:
sub-national, national and regional.

Because "confounded" is the automatic verdict wherever a within-country clonal
expansion was deposited by a single study, a conditional test was added: BioProject
was assigned only to the tips of the country under test and permuted among those
tips alone, holding geography fixed by construction, with the same statistic,
permutation scheme, correction and seed.

## 3.7 Attribution

**Validation set.** 48 genomes carry an independently documented country of
exposure rather than merely of deposit. Two carry a non-country exposure and are
unattributable at country scale by construction, leaving 46 scorable genomes
drawn from 16 exposure countries. Two of the 46 are isolates from a single patient
sampled five years apart, so the set represents 45 individuals.

**Distance.** Attribution was scored on core-genome MLST (Lichtenegger scheme,
4,221 loci) so that the result does not depend on the lineage partition. Loci
missing in either genome of a pair are excluded from that pair rather than imputed,
making the denominator pair-specific; the median loci compared is 4,039 of 4,221.

**Holdout.** Scoring removes both every validation genome sharing the target's
exposure country and every member of the target's same-source outbreak group. The
second condition is necessary because outbreak siblings leak across country labels.

**Estimators.** Four estimators were computed for every held-out genome against
the same pool: nearest neighbour, modal k = 20, a group test using the lowest
median distance, and a hybrid. The best estimator differs by scale, so both the
figure and the estimator are always reported together; country is best under
nearest neighbour and region under modal k = 20. Nearest-neighbour and modal
figures are different analyses and are never compared with one another.

**Abstention.** Because the estimator answers confidently even when no relative
exists, an abstention rule was added: where no genome lies closer than 0.462
allelic distance, the result is returned as unattributable. Performance is reported
out of sample, with the threshold selected on the other 45 genomes and applied to
the held-out one.

## 3.8 Software and reproducibility

Nextflow 25.04.6; PopPUNK 2.7.6; SKA 0.4.0; Mash (sketch size 50,000, k = 21);
Snippy 4.6.0; Gubbins 3.4.3 with RAxML 8.2.12; IQ-TREE 2.2.6; parsnp 1.7.4;
BUSCO 5.8.2.

The reported analysis is pinned to a tagged pipeline release. A clean exit does
not establish that every unit succeeded, because the workflow ignores per-task
errors; verification is therefore per-unit, comparing units requested against
units that produced output.

The reported analysis is not seed-reproducible. At the pinned release Gubbins
derives the tree-search seed at random, and a rejected draw silently drops one
analysis unit while the run still exits successfully; the probability that at
least one unit is affected across a full panel is approximately 16%. A re-execution
from the pin recovered the reported figures, losing one unit to this behaviour: per
unit r/m was identical in both value and raw SNP counts for 81 of 84 comparable
units, per-unit alignment distances were identical for 85 of 86 units, and the
diversity window returned 47 units with a median r/m of 7.70, matching the reported
figures.

Two partitions exist for this collection. The reported partition is the corrected
85-unit run; a second run of 88 units, executed on different hardware, serves as a
cross-hardware control. The two agree closely, but unit labels are not comparable
between them and must not be quoted across partitions.

---

# 4. Results

## 4.1 The collection, and the frame it is drawn from

We assembled 2,959 *B. pseudomallei* genomes spanning 50 countries. The collection
is dominated by three countries: Thailand contributes 1,753 (59.5%), China 295
(10.0%) and Australia 282 (9.6%), together 79.0% of the panel.

The European Nucleotide Archive holds 9,040 unique *B. pseudomallei* BioSamples,
of which 7,192 carry a country label across 56 countries. Our panel is therefore
41.1% of the country-labelled public record. Because 312 of our genomes are
in-house isolates not represented in public archives, the strictly comparable
figure, public-derived genomes against the public record, is 36.8%.

**The collection is inverted against the distribution of disease.** Assigning each
of the 2,946 region-labelled genomes to a World Bank region and comparing with
predicted melioidosis burden:

| region | predicted cases/yr | % of burden | genomes | % of labelled | genomes per 1,000 cases |
|---|---|---|---|---|---|
| South Asia | 73,000 | 44.2% | 75 | 2.5% | 1.0 |
| East Asia & Pacific | 65,000 | 39.4% | 2,705 | 91.8% | 41.6 |
| Sub-Saharan Africa | 24,000 | 14.5% | 30 | 1.0% | 1.2 |
| Latin America & Caribbean | 2,000 | 1.2% | 79 | 2.7% | 39.5 |
| Middle East & North Africa | <1,000 | 0.3% | 3 | 0.1% | 6.0 |
| Europe & Central Asia | <1,000 | 0.0% | 12 | 0.4% | n/a |
| North America | <1,000 | 0.0% | 42 | 1.4% | n/a |
| **Global** | **165,000** | 100% | **2,946** | 100% | 17.9 |

Burden estimates from Limmathurotsakul *et al.* East Asia and the Pacific is
sampled 41 times more heavily per predicted case than South Asia and 33 times more
heavily than sub-Saharan Africa. The region predicted to carry the largest share of
disease contributes 2.5% of the genomes.

The country label attached to a genome in this collection is not primarily
measuring where the organism lives. It is measuring where sequencing took place,
and across the top of the burden distribution the two are inverted.

Approximately 15% of the global public collection consists of environmental
isolates from a single Thai case-control study, so this comparison is between a
clinical and environmental mixture rather than clinical isolates alone.

## 4.2 Exposure country cannot be recovered; region can

**Table 1. Attribution accuracy by geographic scale.**

| scale | estimator | correct | accuracy | majority baseline | κ |
|---|---|---|---|---|---|
| **country** | nearest neighbour | **10/46** | **21.7%** | **26.1%** | **0.193** |
| country | modal k = 20 | 7/46 | 15.2% | 26.1% | 0.132 |
| sub-national | either | 0/5 | 0% | n/a | n/a |
| region (7-way) | nearest neighbour | 37/46 | 80.4% | 45.7% | 0.715 |
| **region (7-way)** | **modal k = 20** | **41/46** | **89.1%** | 45.7% | **0.832** |

Country-level attribution does not exceed chance. At 21.7% against a 26.1%
majority baseline it is, if anything, below it. Sub-national attribution fails
outright. Regional attribution succeeds, reaching 89.1% against a 45.7% baseline.

### 4.2.1 The failure is not an estimator artefact

Region and country were scored on the same genomes, the same pool and the same
holdout, and differ by three-quarters of a κ unit. Whatever prevents country
attribution is not a property of the estimator.

### 4.2.2 The apparent country signal under a weaker holdout is circular

Under leave-one-out, nearest-neighbour country attribution appears to reach 29%.
Every one of those correct calls is a validation genome predicting another
validation genome of the same country, and all disappear under leave-group-out.
Country accuracy quoted with same-country validation genomes retained is
artefactual rather than merely optimistic. We report the collapse itself as a
result, because it quantifies how much apparent attribution performance is
circularity.

### 4.2.3 Accuracy depends on whether a relative exists, in opposite directions

| stratum | country (NN) | region (modal k=20) |
|---|---|---|
| d < 0.05, a close relative exists | **2/14** | **14/14** |
| 0.05 ≤ d < 0.30 | 2/10 | 8/10 |
| d ≥ 0.30, no real relative | 6/22 | 19/22 |

Where a close relative exists, the condition under which attribution should be
easiest, region is perfect at 14/14 and country is 2/14. The same 14 genomes, the
same pool, opposite outcomes at two geographic scales. The signal is present at
depth and absent at the shallow end.

The d ≥ 0.30 row should not be read as success. At that distance 30 to 79% of loci
differ and no meaningful relative exists; nine of those 22 genomes share a single
Ecuadorian nearest neighbour, and because most are Latin American the catch-all
region label scores them correct, while both sub-Saharan African genomes in the
stratum are confidently assigned to Latin America and scored wrong. The estimator
is reporting that these genomes are unlike the Asian majority of the panel.

We tested the alternative explanation that genomes with fewer callable loci have
inflated distances. It does not hold: across the 46, loci compared against
nearest-neighbour distance gives Spearman ρ = −0.247, not significant, and the
median loci compared is flat across the three strata (4,042, 4,040, 4,024).

### 4.2.4 Non-independence in the validation set

The set is small and structured. The Philippines contributes 12 of 46. Two of the
46 are one patient. Sixteen of 46 come from a single assembly batch that is 5.9%
of the panel and has the weakest call-rate tail, though this does not bias the
distance strata as shown above.

## 4.3 Resolution is not the limiting factor

| layer | loci | country | region |
|---|---|---|---|
| MLST | 7 | ≤ 8/33 (24%), baseline 36% | 19/33 (58%), baseline 46% |
| cgMLST | 4,221 | 10/46 (22%), baseline 26% | 41/46 (89%), baseline 46% |
| core-genome SNP | whole genome | 0/24 | 22/24 (92%) |

Across a 584-fold span in locus count, country attribution never clears its
baseline. Each row is a different validation set because each typing system covers
different genomes.

The MLST country cell is an upper bound rather than an accuracy, and the reason is
itself a resolution result. At seven loci the nearest neighbour is not unique for
30 of the 33 validation genomes; the median tied set is 21 genomes and the largest
is 52, so the call is settled by an arbitrary tie-break rather than by the data.
The true country appears anywhere in that tied set for only 8 of 33, so no
tie-breaking rule can score above 24%, and an adversarial one scores zero. Even an
oracle tie-break therefore fails to reach the 36% majority baseline. At 4,221 loci
the nearest neighbour is unique for every genome.

Region, by contrast, is monotonic in locus count at 58%, 89% and 92% over the same
span in which country stays at or below chance.

Randomly subsampling loci provides a positive control. Sampling k loci at random
for k = 2 to 4,089 with 10 replicates, country accuracy stays flat at 0 to 7.3%
across the whole range and is 0.0% at the full locus set, while regional accuracy
rises from 49.5% to 82.1% against a 48% baseline and plateaus by roughly 100 loci.
The estimator converts resolution into accuracy when the signal is present; the
country failure is therefore absence of signal rather than bluntness of instrument.

Randomly chosen loci are a lower bound for a curated scheme. The supported claim is
that resolution alone does not buy country-level attribution, not that no targeted
scheme could work.

### 4.3.1 The pipeline resolves a finer distinction than country

The resolution curve shows that the estimator converts resolution into accuracy
when signal is present. A second control asks something stronger: give the same
pipeline a harder question at a finer scale and see whether it answers.

Thirteen patients had culture-confirmed recurrent melioidosis, giving 20 episode
pairs. Separating a relapse of the original infection from reinfection with a new
strain is the finest epidemiological question these data support, and unlike
exposure country it has an answer the genome records directly.

The separation is categorical. On recombination-filtered SNPs, 19 pairs fall
between 1 and 14 SNPs and one falls at 1,102, a 79-fold gap with nothing inside
it, so no threshold between those values changes any call. For 16 of the 20 pairs
these are the production run's own per-unit Gubbins distances rather than a
separate calculation.

Tree topology confirms the same split independently. Against local context, 12 of
the 13 patients form an exclusive clade containing their own episodes and nothing
else, at 94.4/94 to 100/100 SH-aLRT and ultrafast bootstrap support. The
thirteenth is the reinfection: that patient's two isolates do not form a clade at
all, their common ancestor subtends 35 other genomes, and each isolate is closer
to another patient's genome at 81 SNPs than to its own previous episode at 1,102.

Removing recombination sharpens this contrast rather than blurring it. Gubbins
removes 44% of the SNPs between unrelated genomes but 1 of 9 within a patient, so
the correction widens the gap between the two classes. Seven-locus MLST agrees on
all 20 calls, but with no margin behind it: the collection contains 18 pairs of
isolates from different patients carrying identical seven-locus profiles, so the
calls hold on MLST only because the true within-patient pairs are another 10 to 20
times closer than the chance matches.

This establishes that assembly, variant calling, recombination correction and
phylogenetics resolve a within-patient distinction at single-SNP scale on these
genomes, so the country result is not a failure of the instrument. It does not
show that country is attainable. The two questions differ in kind and not only in
scale: relapse versus reinfection asks whether two genomes descend from one
infecting population, which the genome records directly, while exposure country
asks where that population was acquired, which it records only through a panel of
placed relatives. One pair carries a thin margin worth naming, at 14 SNPs between
episodes against 30 to an environmental isolate from the same collection, so a
locally circulating clone is not excluded there.

## 4.4 The panel does not contain the source countries

For 7 of the 16 exposure countries in our validation set, no public genome exists
in ENA at all: Aruba, Costa Rica, El Salvador, Guatemala, Martinique, Nicaragua and
Trinidad and Tobago. All seven are in Latin America and the Caribbean. The gap is
not scattered across the tropics; it is one region.

Two countries that might be assumed absent are not. Mexico has 21 public genomes
and the Philippines has 1.

Mexico also shows that absence is not the whole mechanism. Three Mexican-exposure
genomes retained genuine same-country references under leave-group-out, three in a
thirty-genome pool, and attribution still failed.

The same gap appears at species scale. Against the ENA census, 21 countries with at
least 100 predicted cases per year have zero public genomes, together approximately
8,939 cases per year or about 5% of the global estimate. Nineteen of the 21 are
sub-Saharan African, the exceptions being Nepal and El Salvador. Read with the
burden table above, the argument closes: country attribution fails for our
validation cases because their source countries have no reference genomes, and that
is not a peculiarity of our 16 countries but the shape of the entire public
collection relative to where the disease is.

## 4.5 Independent typing systems fail in the same places

Seven-locus sequence types were called for all analysed genomes and compared with
the recombination-aware partition.

- **ST92 spans seven countries and three distinct lineages.** Thirty-five analysed
  genomes carry ST92 (USA 25, Brazil 3, Mexico 3, Colombia 1, Nicaragua 1,
  Guadeloupe 1, Martinique 1), distributed across three separate analysis units. A
  single sequence type therefore covers the entire region of applied interest while
  resolving into three lineages that the whole-genome partition keeps apart.
- **ST58 spans five countries** (China 25, Thailand 20, Philippines 9, Cambodia 1,
  Taiwan 1) and is the sequence type of most Philippine validation genomes.
- **Homoplasy is systemic.** Of the 278 sequence types present in the analysed set,
  52 (19%) span more than one analysis unit, and ST70 spans eight.
- cgMLST allelic distance and recombination-filtered SNP distance agree closely:
  median Pearson r = +0.861 across the 85 units, with 66 of 85 at r ≥ 0.7.

Prior work established that 7-locus MLST lacks the resolution to determine
geographic origin, and that sequence types shared between continents reflect
homoplasy rather than descent (De Smet *et al.*). The new finding is that
whole-genome, recombination-corrected clustering does not rescue it. That same
study found whole-genome analysis did correctly identify Asian versus Australian
origin, an independent instance of the depth ceiling reported here.

## 4.6 Where geographic signal exists, and where it cannot be separated from study of origin

| scale | labels | testable units | clustered p ≤ 0.05 | survives FDR | passes the BioProject control |
|---|---|---|---|---|---|
| sub-national | country :: subregion | 81 | 16 | 10 | **1** |
| national | country | 48 | 26 | 23 | **6** |
| regional | World Bank region | 17 | 4 | 3 | **1** |

How much can be asked differs by scale, and that is a sampling fact rather than a
biological one. At regional scale 68 of 85 units contain a single region and no
test can run on them, because 91.8% of the panel is East Asia and the Pacific. At
national scale 37 units are single-country.

The BioProject control is decisive. At national scale it removes 12 units as
confounded, country and BioProject being equally significant, plus 5 where the
control could not run, reducing 23 FDR survivors to 6.

**The discarded set is graded rather than flat.** Because 95% of BioProjects in
this panel are single-country and approximately 99% of same-BioProject near-clonal
pairs are also same-country, "confounded" is the automatic verdict for any
within-country clonal expansion deposited by one study, whether or not anything
artefactual is present. Testing the study-effect explanation directly, conditional
on country, splits the discarded units three ways:

| verdict | n |
|---|---|
| confounded, batch structure confirmed within country | 8 nominal, of which 2 survive FDR |
| not separable, no batch structure detected, geography unproven | 4 |
| not separable, untestable | 2 |

Batch structure is real in aggregate (8 of 22 testable cells at p ≤ 0.05 against
1.1 expected, binomial P = 6.6 × 10⁻⁶) but is confirmed after correction in only
two units, both Thailand. For at least a third of the discarded set the artefact
explanation was tested and not found, so describing the whole set as artefact
overstates what the control established. No reported count changes: every reported
result is a pass, and no pass moves.

The six national-scale passes are dominated by Southeast and East Asian countries:
Thailand/Laos, Singapore/France/Malaysia, Thailand/Cambodia, Thailand/Laos,
Thailand/China, and China/Thailand/Laos. The Singapore/France/Malaysia unit carries
a substantial French component and should not be described as purely Southeast
Asian; it is also the single unit that passes at regional scale, where the
Singapore and Malaysia versus France split is genuinely inter-regional.

Every Americas-dominated unit fails, by three distinct routes. The Mississippi Gulf
Coast unit is null at p = 1.0000 and a second Americas unit is null at p = 0.068; a
third has a vacuous control; and two are confounded at p = 0.0010. The conditional
test separates these last two: one does carry within-country batch structure (USA,
13 genomes across 4 BioProjects, p = 0.0450), so for it the confounded verdict is
supported, while the other does not (its only testable cell is Singapore at
p = 0.0569) and is better described as not separable. The Viet Nam and Georgia unit
is null at p = 0.0430, not surviving correction, consistent with the one-locus
boundary described below.

### 4.6.1 Sub-national signal is very nearly absent

On the reported basis, 1 of 81 testable units passes at sub-national scale. The
single unit (n = 27, 24 labelled, 6 distinct sub-national labels, p = 0.0060) is
dominated by one Thai province, Ubon Ratchathani at 16 of 24, which is among the
most intensively sampled melioidosis sites in the world, and its q = 0.0486 only
barely survives correction at 5%.

Sub-national geography is therefore indistinguishable from study of origin in 80 of
81 testable units, and the single exception is a marginal result in the most
heavily sampled province in the collection.

## 4.7 What is operationally usable: two US autochthonous foci

Attribution of origin fails, but cluster membership is callable, and the two
questions should not be conflated.

### 4.7.1 The Gulf Coast cluster

One unit (n = 22) contains the Mississippi Gulf Coast lineage (Petras *et al.*).

| | chromosome 1 | chromosome 2 |
|---|---|---|
| internal median, raw / filtered | 8 / 5 | 5 / 4 |
| maximum to nearest outside genome, raw / filtered | 1,136 / 492 | 1,432 / 528 |

A new US case within roughly 20 SNPs belongs to this lineage; one 500 SNPs away
does not. The call is never borderline. The same data bound what cannot be said:
because the nearest genome outside the cluster is approximately 490 filtered SNPs
away, the origin of the lineage cannot be stated. The Colombian genome is the
nearest relative in this panel, not a near relative.

### 4.7.2 A second focus in Georgia, and the sharpest limit in the study

A second unit contains five genomes from four patients in Georgia, USA, spanning
1983 to 2024, reported as presumptive autochthonous cases with no recent
international travel (Brennan *et al.*). The same unit holds two isolates from one
Viet Nam-exposure patient and three isolates collected in Viet Nam by two
independent studies. The lineage is genuinely present on both sides of the Pacific,
and the published investigation leaves open that the Georgia environmental focus
may itself derive from Vietnam War-era introduction.

This is the condition under which attribution should work, with both countries
represented by independent studies and published epidemiology on both sides, and it
still fails.

| | cgMLST allelic distance |
|---|---|
| Georgia cluster, internal maximum | 8.67 × 10⁻³ |
| nearest non-Georgia genome (a Viet Nam-exposure case) | 8.91 × 10⁻³ |
| **separation** | **0.25 × 10⁻³ = 1.0 locus of 4,221** |

A published US autochthonous cluster and a documented Viet Nam-acquired infection
are separated by one locus more than the cluster's own internal spread. No distance
threshold places them on opposite sides reliably.

The estimator behaves accordingly. For both Viet Nam-exposure isolates, nearest
neighbour is wrong at every scale including the deep Asia versus non-Asia split,
because their closest relative among all genomes is a Georgia case; modal k = 20
recovers both. They are 2 of only 3 errors the deep split makes under nearest
neighbour (43/46, κ 0.869), and modal k = 20 is 46/46, κ 1.000.

This is not a BioProject artefact: the Georgia and Viet Nam-exposure genomes share
a BioProject, and within that single project distances to the Georgia cluster span
8.91 to 16.47 × 10⁻³.

## 4.8 A ladder of claims, and knowing when to abstain

Coarsening the geographic question until it becomes answerable locates the ceiling
precisely (modal k = 20 throughout):

| grouping | classes | accuracy | baseline | κ |
|---|---|---|---|---|
| Asia vs non-Asia | 2 | **100%** | 58.7% | **1.000** |
| Eastern vs Western hemisphere | 2 | 95.7% | 63.0% | 0.909 |
| region, 7-way | 5 present | 89.1% | 45.7% | 0.832 |
| SEA vs non-SEA | 2 | 76.1% | 58.7% | 0.461 |
| country | 16 | 21.7% | 26.1% | 0.193 |

The deep splits are recovered without error and the shallow ones are not, on the
same genomes, the same pool and the same holdout. The limit is depth of signal
rather than volume of data.

Abstention performance, reported out of sample:

| | coverage | selective accuracy |
|---|---|---|
| in-sample | 78.3% | 94.4% |
| leave-one-out | **76.1%** | **94.3%** |

The rule declines 3 of the 5 region errors, including both sub-Saharan African
misassignments, at a cost of 7 correct answers. Two qualifications belong with it.
First, the retained-subset majority baseline also rises, from 45.7% to 50.0%, so
lift over chance improves only from +43.4 to +44.4 points: the value is in which
errors remain rather than in the accuracy figure. Second, the rule cannot decline
errors of the Georgia type, which have genuine close relatives and high
neighbourhood agreement.

The same rule fails at country scale. Its best operating point reaches 37.5%
selective accuracy against an answer-everything 21.7%, but the retained-subset
majority baseline is also exactly 37.5%: on the half of cases it elects to answer,
always guessing the commonest exposure country scores identically. Country
attribution is not rescued by abstaining.

### 4.8.1 The same shape of result in another organism

An independent hierarchical machine-learning study of *Salmonella enterica* serovar
Enteritidis (Bayliss *et al.*) attributed 2,313 genomes to four continents, eleven
sub-regions and 38 countries using unitig features, reporting macro F1 of 0.954,
0.718 and 0.661 at those three levels. The decay with geographic depth is the same
shape reported here, near-perfect at the deepest split and degrading monotonically
as the question narrows, and those authors attribute the country-level shortfall to
the same mechanism, noting a correlation between a lack of training data and lower
prediction accuracy.

Two differences explain why they retain usable country signal where we do not, and
both are consistent with our interpretation. First, *S.* Enteritidis is
comparatively clonal and geographically structured, whereas *B. pseudomallei* is
environmentally acquired, recombinogenic and carries lineages that span continents.
Second, their classes are countries commonly visited by UK travellers and are
correspondingly well referenced, whereas 7 of our 16 validation source countries
have no public genome at all.

Their evaluation used a country-stratified random 75:25 split, which does not
separate near-identical genomes of the same lineage between training and test. Our
own country attribution reaches 29 to 37% under an equivalent leave-one-out design
and falls below baseline only under leave-group-out, so the two results are not
necessarily in conflict and are best read as the same curve sampled at two
different points.

A subsequent deep-learning method reports higher figures on the same benchmark
(91.9, 87.1 and 80.8% at region, subregion and country; Liang *et al.*). Two things
make that number not directly comparable with either: it is an accuracy rather than
a macro-averaged F1, which on 38 imbalanced classes weights the well-sampled
classes heavily; and in the released reference implementation the test path is set
to the validation path, with the reported checkpoint chosen by maximising accuracy
on that same set. The hierarchical decay with geographic depth is nonetheless
preserved in their results.

The deployable statement is a ladder rather than an answer: Asia or not, certain;
region, where a relative exists, with the method stating when one does not; country,
no.

---

# 5. Discussion

We set out to test whether the country in which a melioidosis patient acquired
their infection can be recovered from the genome of the infecting isolate. Across
2,959 genomes and 46 scorable cases with independently documented exposure, it
cannot. Country attribution reached 10 of 46 (21.7%) against a 26.1% majority
baseline, κ 0.193, while regional attribution reached 41 of 46 (89.1%) against a
45.7% baseline, κ 0.832. Sub-national attribution failed entirely.

The value of this result is not that our estimator failed. It is that the failure
is structured, measurable and explicable, and that the same data show where the
recoverable signal stops.

## 5.1 Four findings license the negative result

A negative result invites the reply that a better method would succeed. Four
features of this study answer that.

**First, the estimator demonstrably works when signal exists.** Region and country
were scored on the same genomes, the same reference pool and the same holdout, and
differ by three-quarters of a κ unit. Randomly subsampling loci from 2 to 4,089
raises regional accuracy from 49.5% to 82.1% while country accuracy stays flat at
zero, a built-in positive control showing that the method converts resolution into
accuracy whenever resolution helps.

**Second, the failure is invariant to resolution.** Across a 584-fold span in locus
count, country attribution never clears its baseline, while regional accuracy over
the same span rises monotonically from 58% to 92%. A finer instrument does not help
because the quantity being measured is not there. At the coarse end the statement is
stronger than a point estimate: with seven loci the nearest neighbour is not even
unique for 30 of 33 genomes, and no tie-breaking rule can lift country accuracy to
its own majority baseline.

**Third, the failure is invariant to the analytical framework.** The result holds
under a lineage partition and under two partition-free typing systems, so it is not
an artefact of how we defined units.

**Fourth, the same pipeline answers a finer question cleanly.** Across 20 recurrence
episode pairs from 13 patients, recombination-filtered distances separate 19
same-strain relapses at 1 to 14 SNPs from a single reinfection at 1,102, a 79-fold
gap with nothing inside it, and 12 of the 13 patients form an exclusive clade
against local context at 94.4/94 to 100/100 support. Sixteen of those distances are
the production run's own per-unit output. The assembly, variant calling,
recombination correction and phylogenetics therefore resolve a within-patient
distinction at single-SNP scale on these very genomes. Whatever defeats country
attribution, it is not the instrument.

That fourth control has a boundary worth stating, because it is easy to overread.
Relapse versus reinfection and exposure country differ in kind and not only in
scale. The first asks whether two genomes descend from one infecting population,
which the genome records directly. The second asks where that population was
acquired, which it records only through a panel of placed relatives. A pipeline can
be arbitrarily good at the first and still fail the second, which is the shape of
the result reported here.

Taken together these license the stronger claim: for most source countries in this
collection, exposure country is not recoverable from the genome by the methods
tested, until those countries are sequenced.

## 5.2 Attribution reaches as far as the reference panel and no further

The most generalisable finding is a single mechanism visible at three scales. At
country scale, attribution fails where no same-country reference exists, and 7 of
our 16 source countries have no public genome in ENA at all, every one of them in
Latin America and the Caribbean. At regional scale, the misses concentrate on
regions the panel barely represents: both sub-Saharan African genomes in the
no-relative stratum are confidently assigned to Latin America. At the level of the
individual case, the genomes that cannot be placed at all are disproportionately the
sole panel representative of their exposure country.

One mechanism, three observations: a genome can only be attributed to a place that
is already in the reference set. This applies to any pathogen with an uneven
reference panel and is the result most likely to transfer beyond *B. pseudomallei*.

Absence of references is not the whole mechanism. Mexico retained genuine
same-country references under leave-group-out, three in a thirty-genome pool, and
attribution still failed. The sharpest case is one where the reference condition is
fully satisfied.

## 5.3 When both countries are represented and attribution still fails

A single lineage contains five genomes from four patients in Georgia, USA, spanning
1983 to 2024, reported after epidemiologic investigation as presumptive
autochthonous cases with no recent international travel, together with isolates
from a Viet Nam-exposure patient and three isolates collected in Viet Nam by two
independent studies. Both countries are represented, by separate laboratories, with
published epidemiology on both sides.

The Georgia cluster's internal maximum allelic distance is 8.67 × 10⁻³, and its
nearest neighbour among all genomes is a Viet Nam-acquired case at 8.91 × 10⁻³, a
separation of one locus in 4,221. No distance threshold places those on opposite
sides reliably.

This is a different and harder failure than absence of references. The lineage is
simultaneously established in the southeastern United States and Asian in ancestry,
and the published investigation leaves open that the Georgia environmental focus may
itself derive from Vietnam War-era introduction. A genome drawn from such a lineage
does not have a country of origin to recover, not because the data are missing but
because the organism's history does not respect the question. Comparable cases are
on record: a *B. pseudomallei* isolate from a Second World War prisoner of war,
presumed to represent 62-year latency after Southeast Asian exposure, was reassigned
by genomic analysis to Central or South America.

That two of our validation genomes are wrong at every geographic scale under a
nearest-neighbour rule, including the otherwise perfect Asia versus non-Asia split,
because their closest relative in the collection lies across the Pacific, is the
same phenomenon measured at the level of a single call.

## 5.4 Two failure modes, and a system that knows which one it is in

The abstention rule answers 76.1% of cases at 94.3% accuracy out of sample, and
declines both sub-Saharan African misattributions.

Reporting it requires two baselines, and they disagree. Declining cases at random
leaves the expected error rate unchanged, so the first baseline is the
answer-everything accuracy. But abstention also changes the class mix, so the
majority share of the retained subset must be reported as well, and it rises from
45.7% to 50.0%. Lift over chance therefore improves only from +43.4 to +44.4 points.
The rule's value lies in which errors remain rather than in the accuracy figure.

More importantly, the rule addresses only one of two distinct failure modes.

- **Attractor errors** arise when no real relative exists and the genome is assigned
  to whatever small cluster is least unlike it, with a catch-all regional label
  converting that into a confident answer. These are catchable, and the rule catches
  them.
- **Depth-ceiling errors** arise when close relatives genuinely exist but are
  geographically uninformative, because the lineage spans the geography. These are
  not catchable by any confidence signal of this kind; the Georgia and Mississippi
  genomes rank 26th and 27th of 46 in abstainability while being wrong.

Abstention on distance therefore mitigates sparse sampling rather than shared
ancestry. Distinguishing the two matters operationally: the first improves with more
sequencing, the second does not.

Abstention also does not rescue country attribution. Its best country operating
point reaches 37.5% selective accuracy against an answer-everything 21.7%, an
apparent gain of nearly 16 points reproduced exactly out of sample, but the
retained-subset majority baseline is also exactly 37.5%. The apparent improvement is
entirely a change in class mix.

What emerges is a ladder of claims, each with its own evidence: Asia versus
elsewhere, recovered without error; region, recoverable where a relative exists,
with the system stating when one does not; country, not recoverable, and not rescued
by declining the hard cases.

## 5.5 The same curve in another organism

Geographic source attribution has been reported to succeed elsewhere. A hierarchical
machine-learning study of *Salmonella enterica* serovar Enteritidis attributed 2,313
genomes to four continents, eleven sub-regions and 38 countries, reporting macro F1
of 0.954, 0.718 and 0.661 respectively.

We read that as corroboration rather than contradiction, for two reasons. Its
accuracy decays monotonically with geographic depth, the same shape we report, and
its authors attribute the country-level shortfall to the same mechanism we identify,
noting a correlation between scarce training data and poor prediction, with United
States samples consistently misclassified. Two organisms, one curve, sampled at
different points on it.

That *S.* Enteritidis retains usable country signal where *B. pseudomallei* does not
is itself consistent with our interpretation. It is comparatively clonal and
geographically structured, its classes are countries commonly visited by UK
travellers and correspondingly well referenced, and the surveillance archive behind
it is orders of magnitude denser than the entire public *B. pseudomallei* record.
*B. pseudomallei* is environmentally acquired, highly recombinogenic, with
approximately 91% of raw pairwise distance attributable to imported DNA, and carries
lineages that span continents.

Two methodological cautions belong with any such comparison. Evaluations in this
area typically use random, class-stratified splits, which do not separate
near-identical genomes of one lineage between training and test; our own country
attribution reaches 29 to 37% under an equivalent design and falls below baseline
only under leave-group-out. And accuracy and macro-averaged F1 are not
interchangeable on strongly imbalanced class sets. We would encourage
phylogeny-aware evaluation as the default in this literature.

## 5.6 Where the collection is, and where the disease is

The strongest public health finding here needs no model. Assigning the
region-labelled panel to World Bank regions and comparing with predicted melioidosis
burden, East Asia and the Pacific is sampled 41 times more heavily per predicted case
than South Asia and 33 times more heavily than sub-Saharan Africa. South Asia is
predicted to carry 44.2% of global cases and contributes 2.5% of genomes; East Asia
and the Pacific carries 39.4% and contributes 91.8%.

The same gap appears at country level: 21 countries with at least 100 predicted
annual cases have no public genome at all, together roughly 5% of estimated global
burden, and 19 of the 21 are sub-Saharan African.

This yields two distinct recommendations. The first is derived from what is already
downloadable and would most improve this analysis. The second follows from the burden
comparison and matters more: the highest-value sequencing is in countries where
nothing exists to download at all, across South Asia and sub-Saharan Africa. The
first list is drawn from a frame that is itself biased; the second is drawn from
where the disease is.

## 5.7 Implications for outbreak response

Cluster membership and geographic origin are different questions, and this study
answers them differently. Within the Gulf Coast lineage, isolates differ by a median
of 5 recombination-filtered SNPs while the nearest genome outside it lies roughly 490
SNPs away, so assigning a new case to that lineage is unambiguous and the call is
never borderline. That operational capability is real and is already in use.

The same data cannot state where the lineage came from: its nearest outside relative
is the nearest in this panel, not a near relative. Sequencing an isolate answers
whether the case belongs to a known cluster; it does not answer where the patient was
exposed. Keeping those separate is how genomics avoids being over-promised to an
incident team.

## 5.8 Limitations

**The validation set is small and structured.** Forty-six scorable cases from 45
individuals, two isolates coming from one patient, drawn from 16 exposure countries,
with the Philippines contributing 12. Sixteen of the 46 come from a single assembly
batch representing 5.9% of the panel; we verified that this does not bias the distance
strata (Spearman ρ = −0.247, not significant, with median loci compared flat across
strata), but the non-independence is real.

**The regional task is effectively coarser than seven-way.** Five of seven World Bank
regions are represented among scorable cases, and the classes are unevenly filled.
Regional attribution should be read as the specific, operationally relevant
discrimination it is, not as a general seven-way assignment.

**The abstention threshold is calibrated on 46 genomes.** Leave-one-out removes
threshold-selection circularity but not signal-selection circularity: three candidate
signals were compared on the same set and nearest-neighbour distance was chosen partly
because it performed best. The value 0.462 is specific to this scheme and this panel
and should be re-derived rather than transferred.

**Assembly method affects the measurements.** On four isolates assembled both ways,
SPAdes versus SKESA shifted core completeness by a median of +10.8 percentage points
and Mash distance by −27%, and the effect is per-genome rather than uniform. Our panel
mixes assembly provenance, so Mash-derived quantities are not strictly comparable
across it; the reported diversity window and the cgMLST attribution avoid this by
using alignment-derived and allelic distances respectively.

**Two partitions exist for this collection.** We report the corrected 85-unit
partition and use the 88-unit run as a cross-hardware control. The two agree closely,
but unit labels are not comparable between them. That agreement is evidence of
comparability across hardware rather than of determinism: at the reported release the
pipeline draws an unseeded tree-search seed, so it is not seed-reproducible on either
host. Reproducibility was tested directly, by re-executing the reported analysis from
its pin; it recovered the reported figures, losing one unit to that seeding behaviour.

**We cannot separate the two causes of failure quantitatively.** Most of the
country-level failure we observe is associated with absent references, which is a
statement about the archive; but the Georgia and Mississippi cases show that some of
it arises from lineages that genuinely span continents, which is a statement about the
organism. We can demonstrate that both contribute. We cannot say in what proportion,
because the cases where references exist are too few, 14 of 46, to estimate it.
Sequencing the countries currently at zero is a testable intervention, and it would
also be the experiment that separates the two.

## 5.9 Conclusion

Exposure country cannot presently be recovered from the *B. pseudomallei* genome for
most source countries, and this is not a limitation of resolution or of method: the
same data, estimator and holdout recover region at κ 0.832 and the Asia versus
elsewhere split without error.

Two things stand between a genome and a country, and they differ in kind rather than
in size. Sparse reference sampling is the tractable one: seven of our sixteen source
countries have no public genome at all, and for those cases no method can succeed.
Sequencing where the record is empty would address this directly, and we recommend it
on public health grounds regardless of what it does for attribution. Shared ancestry
across continents is the stubborn one: where a lineage is established on two
continents, as the Georgia and Viet Nam isolates are, one locus apart, there may be no
country-level answer to recover, and more sequencing would sharpen the description of
that lineage without making the question answerable.

We resist calling either the dominant cause. It is tempting to treat sparse sampling
as the main effect because it is the more visible, but country attribution failed for
12 of the 14 cases that did have a close relative available, the regime in which
sampling is not the limitation. On these data the stubborn mode is not a small residue.

We therefore do not claim that sequencing alone would deliver country-level
attribution, and our data cannot say how much of the gap it would close. What they do
support is narrower: report a graded claim rather than a single answer, decline when
no comparable genome exists, and treat a confident country call on a
continent-spanning lineage as the failure mode that no confidence measure will catch.
