> # ⚠ NUMBERS ON THIS DRAFT WERE COMPUTED ON A SUPERSEDED BASIS
>
> This draft was written from `origin/main` at `32a08a4` (2026-08-19), which
> predates the analysis freeze. In that tree the A100 88-unit run was still
> called *production* and r/m 7.38 was still current. **Neither is true.**
>
> The reported basis is **`FINAL_BASIS_2026-08-22/` — 85 units, 2,340 genomes**,
> the corrected workstation run. The A100 88-unit run is the **cross-hardware
> control**. The r/m headline is **7.70 (n=47)**.
>
> **Corrected 2026-09-02.** The manuscript is now on the reported basis
> throughout: **85 units, 2,340 genomes, r/m 7.70**. The 88-unit A100 run is the
> cross-hardware control (section 9), and both runs executed byte-identical
> pipeline code. Sections 1, 3 and 9 and the abstract were reconciled to this
> basis. Any remaining "82-unit" mention refers to a specific superseded
> demonstration and is labelled as such in place.
> - ~~The geography section~~ **DONE 2026-09-02, reframed twice.** Section 8 no
>   longer reports a count. 26 units cluster by country with no control; the
>   correctly specified control retains **18-24**, the submission-accession
>   discriminant retains **6**, and that discriminant **over-adjusts** because
>   country causes BioProject rather than the reverse. Both instruments are
>   inadequate in opposite directions. The section now reports the **range and
>   its mechanism**, and concludes that country and collection history are not
>   separable in a collection assembled this way. See Figure 4.
>
> Full list: `PR3_CORRECTIONS_2026-09-02.md`. Canonical numbers: `NUMBERS.tsv`.
> Current state: `STATE_2026-09-02.md`.

# A measured operating range for recombination detection in *Burkholderia pseudomallei*, and what it changes about the reported recombination rate

**Draft 1, 2026-09-02.** Submission-shaped draft assembled from
`METHODS_DRAFT_2026-08-19.md` (the authoritative methods),
`FINDINGS_2026-08-19_workstation.md`, `TRACK_A_VS_A100_COMPARISON.md`,
`V3_RUN_RESULTS.md` and `BACKGROUND_RESEARCH_2026-09-02.md`.

Two conventions are used throughout and both are deliberate. **[CONFIRM]** marks a
number that must be filled or checked against a run artifact before submission.
**[NAME]**, **[n]** and similar brackets mark information this draft does not have
and must not invent. Nothing in this file was rounded, carried across partitions,
or inferred from a summary line.

**Results section 8 has been run and reframed (2026-09-02).** It is no longer a
specification. The analysis was executed on the frozen basis, and the honest
result is neither the geographic structure an earlier draft anticipated nor its
simple negation: **the count depends almost entirely on a confounder
specification these data cannot settle**, ranging from 6 to 24 units. The section
reports that range with its mechanism rather than a point estimate. This was
worked out deliberately before submission rather than discovered in review.

**Scope, resolved 2026-09-02.** `PUBLICATION_STRATEGY_2026-09-02.md` argued that
section 8 should be cut from this paper and carried into a second paper on
geographic structure. That recommendation was written when the section was
expected to report geographic structure. It does not: it reports that the
structure is largely batch. **That is a calibration finding, not a
phylogeography finding, and it belongs in this paper** alongside the detection
window, because both say the same thing about the same collection -- an apparent
signal is not a measurement until you have shown what else could produce it.

The consequence for the second paper is that it needs a subject other than "this
collection shows geographic structure". Whether it shows it is exactly what
cannot be settled here, which is a limitation of the collection rather than a
result to build a paper on.

To run the outstanding analyses when they are wanted, see
`run_manuscript_analyses.sh`, which drives the phylogeography association, the
reference-branch re-measurement, and a consolidated report that fills the
`[CONFIRM]` markers below.

---

## Title page

**Title.** A measured operating range for recombination detection in
*Burkholderia pseudomallei*, and what it changes about the reported recombination
rate

**Short title.** Bounded recombination detection in *B. pseudomallei*

**Authors.** Peera Hemarajata [ORCID], [NAME], [NAME], [NAME]

**Affiliations.** [n] [Association of Public Health Laboratories, Bangkok,
Thailand, confirm the exact institutional string and address to use], [n] [NAME]

**Corresponding author.** Peera Hemarajata, [email], [postal address]

**Keywords.** melioidosis, *Burkholderia pseudomallei*, homologous recombination,
Gubbins, phylogenomics, genomic attribution, source attribution

**Word counts.** Abstract [CONFIRM], main text [CONFIRM], figures [CONFIRM],
tables [CONFIRM], references [CONFIRM].

**Target journal.** *Microbial Genomics* is the closest fit, since the paper is a
measurement of method behavior with a population-genomic result attached, and the
journal publishes negative and calibration results. *Nature Communications* is
possible if the geography analysis in section 8 comes back strong. Decide before
formatting the references.

---

## Abstract

*Burkholderia pseudomallei* causes melioidosis, an environmentally acquired
infection modeled at 165,000 cases and 89,000 deaths per year, and one whose
exposure origin often cannot be established from patient history. Genomic
attribution is therefore the remaining evidence, and it depends on separating
descent from recombination in a species where recombination dominates. Every
published *B. pseudomallei* recombination analysis subdivides the population
first, and three state that the purpose is to bring diversity inside the range
where detection works, but no study has measured where that range lies.

We measured it. Using 2,976 assemblies partitioned by PopPUNK and fastbaps into
analysis units, we calibrated the operating range of Gubbins directly and found
that estimates are interpretable only between approximately 700 and 4,700 mean
pairwise core SNPs, measured on the alignment. Below the floor recombination is
not detected at all, and above the ceiling the ratio of recombination-derived to
mutation-derived substitutions collapses. Both bounds are brackets rather than
points, the floor to (588, 755] and the ceiling to approximately 4,700, and we
report them as such.

Applying that window to the reported partition of 85 units and 2,340 genomes,
r/m is a measurement for 47 units and a detection failure for 38. The median r/m across the
47 in-window units is 7.70, against 1.32 below the floor and 2.14 above the
ceiling. A low r/m in this species is therefore a detection failure rather than a
clonal unit, and the all-unit median of 5.51 mixes measurements with failures.
Detection was bounded from both sides. A matched zero-recombination null over
1,519 replicates produced a maximum pooled r/m of 0.00668, between 427 and 2,234
times below any observed value, and spike-in of tracts at the measured donor
divergence recovered 91%.

Two failure modes silently corrupt results and are reported so others can avoid
them. RAxML segfaults when its run identifier reaches 128 characters, which
Gubbins reports as a model-fitting failure and which would have destroyed 42 of
172 replicon-units in this partition. And retaining the mapping reference as a
tree tip places population-to-outgroup divergence in the denominator of r/m,
which moved the median in an earlier partition from 1.85 to 6.30. Two independent
executions on different hardware agreed to a median absolute difference of 0.0145
in r/m across 82 units of identical membership.

---

## Importance

[Journal-dependent. Include only if the target journal asks for it.]

Melioidosis is under-reported across most of its range, and the number of
countries where the organism is probably endemic but has never been reported is
larger than the number where it is recognized. Patients therefore present without
usable exposure histories, and the recent identification of locally acquired
melioidosis on the Mississippi Gulf Coast was settled by genomics rather than by
epidemiology. Attribution of that kind rests on SNP distances, and in this species
SNP distances are mostly recombination. We show that the standard tool for
removing recombination works only inside a bounded range of population diversity,
we measure that range, and we show that the values reported outside it are
detection failures that read as clean results. The practical consequence is
direct. Recombination is most consequential and least detectable at exactly the
scale where outbreak and source-attribution calls are made.

---

## Introduction

*Burkholderia pseudomallei* is an environmental saprophyte of soil and surface
water across the tropics and subtropics, and the cause of melioidosis [1,2]. It is
not host-adapted, and person-to-person transmission is exceptionally rare, so each
infection is an independent sample of a local environmental population. That
ecology is what makes the genome informative about place, because there is no
transmission chain homogenizing genotypes across geography.

The burden is large and unevenly observed. A global model estimates 165,000 cases
per year, 95% credible interval 68,000 to 412,000, and 89,000 deaths, 36,000 to
227,000 [3]. The same model concludes that melioidosis is under-reported in the 45
countries where it is known to be endemic and is probably endemic in a further 34
that have never reported it. It also predicts that South Asia carries 44% of the
global burden against 40% for East Asia and the Pacific, so the region with most
of the disease is not the region with most of the sequenced isolates.

Exposure history is consequently unreliable, and genomics has repeatedly supplied
what history could not. Four patients in four US states with no travel abroad were
linked to each other and to an imported aromatherapy spray by whole-genome
sequencing, and the strain clustered with South Asian genomes consistent with the
product's origin in India [4]. Three patients in one Mississippi Gulf Coast county
were linked to soil and water on one patient's property, by a strain more than
1,000 SNPs from any other available genome, which established local endemicity in
the continental United States for the first time [5]. And a 62-year latency claim,
the field record for over a decade, was overturned when the isolate was placed in
the Western Hemisphere clade rather than in Southeast Asia [6].

Every one of those results is a SNP-distance argument, and in this species SNP
distances are dominated by recombination. Nandi and colleagues reported an overall
per-site r/m of 7.2 from 106 genomes, with clade values of 4.5, 8.5 and 6 [7].
Seng and colleagues reported per-lineage values of 3.7, 4.6 and 2.2 with
confidence intervals from 1,391 genomes, and found that between 96.6% and 99.9% of
genes had recombined at least once within a single lineage [8]. The frequently
quoted claim that *B. pseudomallei* has the highest recombination rate reported in
bacteria derives from a per-allele multilocus sequence typing quantity of 18 to 30
[9], which is not comparable to any per-site genome-wide estimate and should not
be placed beside one.

The mechanism that makes partitioning necessary is also documented. Recombination
in this species occurs predominantly within clades, interclade exchange is rare,
and each clade carries a distinct complement of restriction-modification systems
that inhibit uptake of non-self DNA, so genomic clades behave as functional units
of genetic isolation [7]. A recombination rate estimated across clades is
therefore not estimating a rate that exists in nature.

Practice reflects this. Every published *B. pseudomallei* recombination analysis
runs within lineages rather than across the species, and three state why. Nandi
applied ClonalFrame separately to each clade [7]. Seng ran Gubbins on
lineage-specific alignments [8]. Chewapreecha used hierarchical Bayesian
clustering to let Gubbins "operate within its best performing range" and continued
subdividing "until the diversity observed in secondary or tertiary clusters fell
within the limit of recombination detection" [10]. That study also reports that
one cluster, the Australasian group, could not be subdivided far enough, which is
a named failure of the standard pipeline in the most basal part of the population.

The rule cannot be implemented as written, because no such limit has ever been
published. Gubbins is described as most effective on "a densely sampled collection
of closely-related isolates" and its authors state that high sequence diversity
confounds detection and that such populations "would need to be split into sets of
closely-related isolates," but no divergence bound is given [11]. In the opposite
regime the same paper reports that Gubbins "was only able to predict 5–10% of the
actual number of recombinations" when imports carry too few substitutions to
register. ClonalFrameML is explicitly a within-lineage tool and both of its
documented failure modes bias r/m downward [12]. The only numeric operating
threshold anywhere in the *B. pseudomallei* literature is an unvalidated rule of
thumb of 5,000 pairwise SNP distances, from a single study [13].

So the field has a stated principle, one unvalidated ceiling, and no floor. We set
out to measure the range in both directions, to apply it to a large collection,
and to report what it does to the recombination rate that gets quoted for this
species. A secondary aim was to establish how much geographic structure survives
recombination correction, since attribution depends on it and no study has ever
quantified whole-genome attribution accuracy at any spatial scale [14].

---

## Results

### 1. A collection of 2,976 assemblies partitioned into 85 analysis units

The panel comprised 2,976 *B. pseudomallei* assemblies, 2,802 from an established
curated collection and 174 newly added isolates. Of 188 newly produced SPAdes
assemblies, 19 were not admitted, comprising 13 duplicates of runs already held,
5 that were not *B. pseudomallei* or were grossly divergent, and one mixed sample
that SPAdes revealed as 12.00 Mb of foreign content. Every exclusion carries a
recorded reason and evidence.

The analysis unit is a fastbaps level-1 subcluster within a PopPUNK strain,
retained at n of 7 or more. The rule was applied uniformly. No lineage was
subdivided because it was large and none was left whole because it was small.
PopPUNK v2.7.6 over all 2,976 assemblies yielded 310 clusters, the largest holding
901 genomes. Within each strain, PopPIPE built a split-k-mer alignment, a
neighbor-joining guide tree and a fastbaps partition analyzed at level 1. Levels 2
and 3 were computed but not used, so unit size was set by one stated rule rather
than chosen per lineage.

That gave 86 units and 2,352 genomes, 79.0% of the panel, with a largest unit of
159 and a median of 18. A post-hoc correction removed seven duplicate BioSamples
and one unit that fell below the n >= 5 floor, giving the **reported basis of 85
units and 2,340 genomes** (Table 1), on which every result below is computed. An
independent execution on different hardware refined one unit into three, giving
88 units and 2,342 genomes; that run is the cross-hardware reproducibility
control (Results section 9), not the reported basis.

Two observations from the partitioning step are worth reporting because both are
easy to get wrong.

PopPUNK's Gaussian mixture fit at fixed K is deterministic per input and exposes
no seed, so cluster boundaries are a property of the panel rather than of the run.
It follows that strain labels are not comparable between fits on different panels.
This is not a technicality. The strain numbered 4 in the previous panel and the
strain numbered 4 in this one share zero members, and all 261 genomes of the
former fall inside strain 1 here. Comparisons across fits must be made by
membership.

Overall diversity did not diagnose internal structure, but modality did. Units
drawn from more than one prior-partition unit were about fourfold more internally
diverse, median of medians 0.00221 against 0.00054, yet the most diverse
single-provenance unit exceeded every one of them at 0.00538. By contrast
`strain_1_L1_26`, at n of 154 and among the tightest units in the panel with a
median pairwise distance of 0.00060, held three clonal groups at 0.00007 internal
against separations of 0.00088 and 0.00134. It was split into 98, 47 and 8.

### 2. Recombination detection has a bounded operating range, and both bounds are brackets

We calibrated the operating range directly, using a reduced four-arm protocol per
unit, two references crossed with two replicons, validated against a full 12-arm
protocol. The evidence base is 6 full 12-arm runs, 13 reduced four-arm runs and 2
level-1 subcluster runs, with 91 clusters measured for diversity.

Units are interpretable between approximately **700 and 4,700 mean pairwise core
SNPs**, measured on the alignment. The calibration itself was performed in `ska
distance` units, where the corresponding window is 1,270 to 4,671. The two bounds
translate very differently, and only the alignment-derived window is applied to
this collection.

The bounds were located on union recombination coverage and median tract length
alone, without reference to r/m, because choosing them to maximise in-window r/m
would be circular. Across seven diversity bands of 12 units each, coverage jumps
from 4.3% to 28.0% and the median tract from 1.12 to 3.37 kb between the 15–588
and 755–1,349 bands, which brackets the **floor to (588, 755]**. The tract falls
from 3.77 to 2.69 kb between the 3,403–4,732 and 4,750–6,532 bands, placing the
**ceiling near 4,700**. The bottom band reproduces the original calibration's
failure signature, which recorded union coverage of 0.7% and an abnormal 1,002 bp
median tract for a cluster at 405.

The ceiling translates essentially unchanged from the 4,671 obtained in `ska`
units, which is a genuine check on the exercise, since nothing forced the two
unit systems to agree at the top. The floor does not translate, and the Mash
proxy placed it at 1,270, nearly twice too high. Where in the bracket the floor is
put does not matter: 588, 700, 755 and 840 give median in-window r/m of 7.70,
7.70, 7.74 and 7.78.

We report both bounds as brackets, because that is what they are. The floor is
bracketed to (588, 755], a 1.28-fold interval measured on 12 units either side. It
replaces the (405, 1,268] bracket obtained in `ska` units, which was 3.1-fold wide
and rested on one cluster either side. The ceiling sits near 4,700, between the
3,403–4,732 and 4,750–6,532 bands. In `ska` units it is bracketed to
(4,671, 6,342], a 1.36-fold interval, and it has a counter-example, since one
continuous cluster at 9,617 has a sound root-to-tip slope, the only one of seven
above the ceiling to do so. The ceiling is a strong tendency rather than a law,
and the gate refuses that cluster as the conservative choice.

A second gate screens for multimodality, and the order is load-bearing. Applying
modality first fails, because the statistic divides by the mean and a single
divergent genome in a tight cluster produces an enormous ratio. A calibration
attempt that included out-of-range clusters failed at every sample size, with the
continuous 95th percentile rising with n, which is impossible for sampling noise
and is the signature of a mis-composed panel. Calibrating instead by subsampling
clusters whose structure is unambiguous at full size gave the rule that at n of 25
or more a unit is a mixture if the largest gap over the mean exceeds 1.0 or the
empty-bin fraction exceeds 0.45. That catches 100% of known mixtures from n of 25
upward at a 15% to 21% false-mixture rate. Below n of 25 modality is undecidable,
with both statistics overlapping between classes at every threshold tested. This
is a limit of the data rather than of tuning.

### 3. Applying the window, r/m is a measurement for 47 of 85 units

Classifying all 85 reported units against the window reproduces the calibration
exactly (Table 2).

| Gate 1 class | units | median r/m |
|---|---|---|
| **In-window** | **47** | **7.70** |
| Below floor | 12 | 1.32 |
| Above ceiling | 26 | 2.14 |

**The recombination result for this collection is r/m 7.70, the median of 47
in-window units.** The all-unit median of 5.51 mixes measurements with detection
failures and is not reported. The collapse is symmetric, which makes the reading
error easy to commit in both directions, and the consequence is the single most
important qualification on these results. **A low r/m in this species is a
detection failure, not a clean unit.**

Two units illustrate how the error is made. `strain_1_L1_35` and `strain_4_L1_3`
returned r/m of 1.31 and 0.75, among the lowest in the run, and an earlier reading
of this analysis cited them as evidence that declining to subdivide them was
correct. Measured against the window they sit at 9,042 and 13,099 mean pairwise
SNPs, 1.9-fold and 2.8-fold above the ceiling. Their low values are the documented
above-ceiling collapse. Leaving them intact was still right, because both are
unimodal and that is a sound structural reason, but not for the reason given, and
their r/m values should not be quoted.

Across the 47 in-window units the r/m distribution is right-skewed: median 7.70,
interquartile range 5.51 to 9.44, full range 1.52 to 18.03. The lower quartile,
5.51, is numerically the same as the all-unit median named above, and the two are
unrelated statistics rather than one number repeated. The spread is genuine
biological heterogeneity in recombination rate among lineages, not measurement
noise, since every unit in this set sits inside the calibrated detection window.

### 4. Subdividing a unit can remove it from the measurable set

The refinement step provides a worked example of the window governing
interpretation rather than merely filtering output. `strain_1_L1_26` was split on
unambiguous modality evidence. Read against the window, the split converted one
measurable unit into one measurable unit plus two clonal expansions lying below
the floor at which recombination can be detected at all (Table 3).

| | n | mean pairwise core SNPs | r/m | Gate 1 |
|---|---|---|---|---|
| Before, `strain_1_L1_26` | 154 | 3,421 | 3.10 | In-window |
| After, `strain_1_L1_26` | 98 | 955 | 1.07 | Below floor |
| After, `strain_1_L1_36` | 47 | 3,374 | 6.68 | In-window |
| After, `strain_1_L1_37` | 8 | 229 | 2.63 | Below floor |

The count of in-window units was 47 both before and after refinement, and 106 of
153 genomes moved out of the measurable set. We therefore report `strain_1_L1_36`
as the recombination result arising from the split, and `strain_1_L1_26` and
`strain_1_L1_37` as identified clonal expansions of epidemiological interest with
no r/m.

The split remains defensible on population structure, which is independent of r/m.
Three clonal groups at 0.00007 internal separation against 0.00088 and 0.00134
between them is a real finding, and analyzing separate populations as one unit is
objectionable whatever r/m does. The split also revealed 6.2-fold heterogeneity
among the children, from 1.07 to 6.68, that the combined unit averaged away. What
it does not support is a recombination-inflation rationale. The pre-split parent
measured 3.10 and was in-window, which is a valid measurement and not an inflated
one, and the n-weighted mean of the three children is 2.87, only 7% below the
parent rather than the step change that un-lumping would predict.

One further caution. `strain_1_L1_22` moved from r/m 4.12 at n of 34 to 7.21 at n
of 32 when two isolates were removed. The unit sits at about 4,762 mean pairwise
SNPs, immediately above the ceiling, where the estimate is unstable. Trims of that
size near a window boundary should carry the caveat or should not be performed.

### 5. Detection is bounded from both sides

Neither bound of the operating range would mean much without knowing the false
positive and false negative rates of the detector itself, so both were measured on
this genome.

For false positives we built a matched zero-recombination null of **1,519
replicates across 62 unit-replicons**. Each replicate inherits from the real unit
it matches its tree, fitted substitution model, alignment length, base composition
and per-genome missing-data pattern applied verbatim, with sequences simulated
under that model and passed through the identical Gubbins invocation used in
production. By construction the truth is zero recombination. **Twenty of 1,519
replicates, 1.32%, produced any false-positive block**, one block each. The maximum
pooled r/m the null ever reached is **0.00668** and the median is zero, against
observed values in real units of 2.85 to 14.92, which is **427-fold to 2,234-fold
above the null maximum**.

That result also settles something about the low-r/m units, and it settles it
against the interpretation one would reach by intuition. Every unit with any
detected recombination receives the same minimum p-value against this null,
because the null's entire support is [0, 0.00668]. A p-value cannot distinguish
r/m 2.03 from r/m 12.89 when both sit hundreds of times above anything the null
produces. Units at the bottom of the distribution are as significant as units at
the top. **The low-r/m units are not units in which recombination went undetected.
They are units with abundant real recombination and simply less of it relative to
mutation.**

For false negatives we implanted recombinant tracts of known length and divergence
into a real unit, leaving every other property of real data intact. Tracts are
5,000 bp, and an implant counts as recovered if a Gubbins block covers at least
50% of it for that recipient taxon in the spiked run and not in the unspiked
control (Table 4).

| Donor divergence | SNPs per 5 kb tract | Recovered |
|---|---|---|
| 0.0005 | 2.4 | 4 of 20, 20% |
| 0.001 | 4.2 | 8 of 20, 40% |
| **0.002, the measured value** | **9.0** | **19 of 21, 91%** |
| 0.005 | 25.0 | 19 of 19, 100% |
| 0.01 | 45.0 | 19 of 21, 90% |

At the donor divergence measured in every unit, 0.0021 to 0.0024, Gubbins recovers
91% of the recombination really present. Detection becomes reliable somewhere
between 4 and 9 SNPs per 5 kb tract, and this collection sits above that
threshold, so the reported r/m values are not systematically deflated by donor
similarity. Recovery plateaus at roughly 90% to 100% above a divergence of 0.002
rather than saturating cleanly, and on three replicates and about 20 scorable
implants per cell the difference between 90% and 100% is about two implants, so
the honest statement is a plateau rather than a ceiling.

### 6. The estimate is robust to the maximum-likelihood tree builder but not to a distance-based one

Because a tree-builder effect would confound comparisons between production and
simulation arms, three builders were run on the same real alignments, 6 units by 2
replicons for 12 comparisons, chosen to span r/m from 1.81 to 14.13 (Table 5).

| Comparison | Median ratio | Median deviation | Worst | Ratios below 1.0 | Sign test |
|---|---|---|---|---|---|
| IQ-TREE against RAxML | 0.988 | 2.3% | 15.0% | 7 of 12 | p = 0.77 |
| **rapidnj against RAxML** | **0.922** | **7.8%** | **45.5%** | **11 of 12** | **p = 0.0063** |
| rapidnj against IQ-TREE | 0.938 | 6.2% | 51.6% | 10 of 12 | p = 0.039 |

The two maximum-likelihood builders agree with no directional bias, and the 7 of
12 split is what chance predicts. Union coverage differed by a median of 0.3
percentage points and at most 1.5. No unit changed its position within the r/m
distribution.

The distance-based builder is different in kind. It underestimates r/m
systematically, at three to four times the magnitude, and the bias is significant
by a two-sided sign test. The bias belongs to tree construction rather than to
model fitting, because Gubbins delegates model fitting to IQ-TREE when a
distance-based constructor is selected, so the third row of the table holds the
model fitter constant and isolates the constructor alone. The underestimation
persists there. It is the neighbor-joining topology, not the model, that loses
recombination signal.

Every number reported in this work comes from the RAxML production arm, so no
result is affected. But a pipeline configured with rapidnj would not reproduce
them, and would report r/m biased low by a median of 8% and by as much as 46% in
individual replicons. We pin the tree builder and recommend against distance-based
builders for recombination inference at this scale. The finding also argues that
builder equivalence should be verified per builder class rather than assumed from
a single comparison, since agreement between two maximum-likelihood builders
carried no information about a distance-based one.

### 7. Two silent failure modes

Both produce entirely plausible output, which is what makes them worth reporting.

**RAxML segfaults at a run identifier of 128 characters or more.** Gubbins
constructs that identifier from the reference genome's FASTA defline, as
`<unit>__<replicon>.core.full.iteration_N_reconstruction`, and passes it to RAxML
as the `-n` argument. Gubbins catches the resulting crash and reports it as
"Unable to fit model to data," which is indistinguishable from a genuinely
unsuitable reference. On this partition **42 of 172 replicon-units, 24.4%, would
have exceeded the limit**, the longest at 161 characters. After defline
normalization the longest was 70. Sequence content was verified byte-identical and
only `>` lines were rewritten.

The diagnostic value of this is that the failure was previously misattributed. An
earlier investigation ruled out species misidentification, assembly quality,
contiguity, GC content, ambiguous bases, cluster size and clonality, concluded
that three particular reference genomes were toxic, blacklisted them and wrote off
six of 34 units. Holding the alignment byte-identical and changing only the
filename settled it. A run identifier of 136 characters fails and one of 65
succeeds, and all 12 affected unit-replicons then succeeded against the reference
that had supposedly broken them. No reference is bad.

**Retaining the mapping reference as a tree tip corrupts r/m.** The reference sits
outside the population by construction, so its terminal branch carries
population-to-outgroup divergence, which Gubbins scores as outside recombination
and which therefore enters the denominator of r/m. In one unit that branch carried
7,307 of 7,574 SNPs assigned to the non-recombinant class. Across an earlier
82-unit partition, **52% of all outside-recombination SNPs, 458,688 of 881,582,
came from reference branches**, and excluding them moved the median r/m from
**1.85 to 6.30**. Where the reference is a true outgroup its divergence splits
between the reference leaf and the sibling clade at the root, so both children of
the root are dropped whenever one is the reference. Where the reference nests
inside the population nothing is removed. The exclusion is built into the current
pipeline and the per-unit record of dropped branches is retained.

These figures (52%, and the 1.85 to 6.30 shift) were measured on a superseded
82-unit partition and are presented as an illustrative demonstration of the
mechanism, labelled as such, not as reported-basis numbers. The exclusion itself
is built into the reported pipeline, and the reported r/m of 7.70 already
incorporates it.

### 8. Country structure and collection history cannot be separated in this collection

**Reframed 2026-09-02**, twice, and both revisions are recorded because the
sequence is the argument. This section first read as a specification with
placeholders, then as "most apparent phylogeographic signal is batch structure",
and now as what the evidence actually supports: **the number of units showing
country structure depends almost entirely on a specification choice that these
data cannot settle.**

#### The test

Per unit we computed the Fitch small-parsimony score of country labels on the
recombination-corrected topology, against a null of 1,000 label permutations
across tips of the same tree. Permutation holds topology and country composition
fixed, so a unit that is 90% Thai is compared against other 90%-Thai
arrangements, which is necessary because the marginal country distribution is
extremely uneven. Tips of unknown country are treated as fully ambiguous, so
missing metadata weakens signal rather than inventing it.

**Twenty-six of 85 units cluster by country** at p <= 0.05 with no confounder
applied. Thirty-seven have a single country value and cannot be tested at all;
the remainder show no signal.

#### Why the confounder is the whole question

Related isolates get sequenced together, so apparent geographic clustering may be
collection history. The obvious control is the submission accession, tested
identically on the same trees. **That control is mis-specified here, and its
error has a direction.**

A confounder must be a common cause of both the exposure and the outcome.
Submission accession is not: it does not cause country, **country causes it**,
because a study is defined by where it sampled. In this panel **113 of 119
BioProjects (95%) are entirely single-country** and the two variables associate
at Cramer's V = 0.857. Conditioning on a variable that is largely determined by
the exposure is over-adjustment; it removes part of the effect being estimated
rather than widening its uncertainty.

Three observations show this is the operative situation and not a theoretical
caveat. Of the 12 units the accession control discards, **four are driven by
deliberately diverse reference panels and five by geographically defined sampling
frames** (for example a survey titled "Northeast Thailand", and an island
transmission study); **none is driven by an identifiable clonal batch**. The two
genuinely batch-like projects in the collection, 26 genomes from a single soil
sample and a set of serial within-patient isolates, drive no discard at all.
And **12 of the 26 clustering units are discarded despite showing no batch
structure when country is held fixed**.

#### The count is a function of the specification

| control | units retained |
|---|---|
| none | 26 |
| discount only where within-country batch structure survives FDR | **24** |
| discount where any nominal within-country batch structure is present | **18** |
| discriminant on submission accession | **6** |
| the same, plus collection period | 2 |

**The correctly specified control -- one that asks whether batch structure exists
independent of geography -- retains 18 to 24 units. The accession discriminant
retains 6.** We report the range and its mechanism rather than a point estimate,
because we cannot justify either endpoint.

**Neither instrument is adequate, and the failures are opposite.** The accession
discriminant over-adjusts, for the reasons above. The conditional within-country
test is **68% untestable** (64 of 94 unit-country rows lack the tips or the
distinct accessions to run), so its higher count is inflated by absence of
evidence rather than evidence of absence.

#### Sensitivity

Collection period is available for 90% of genomes and is **less than half as
nested inside country** as submission accession (Cramer's V 0.379 against 0.857).
Applied as an additional discriminant, with two binnings pre-specified and
agreement required, it retains 3 units, and 2 units pass both it and the
accession control. This is reported as sensitivity, not as an estimate: each
further discriminant is another filter, and every candidate available here is
entangled with geography to some degree, so the count falls mechanically with the
number of tests applied. **`strain_11_L1_5` is the only unit robust to every
specification examined.** Laboratory, which would be a genuine batch variable,
is not recorded for this collection.

#### What we conclude

We do not report a count of geographically structured units, because we cannot
defend one. **We report that country and collection history are not separable in
a collection assembled this way**, and that the apparent answer ranges from 6 to
24 units depending on a choice between two inadequate instruments.

That is a limitation of the collection rather than of the method, and it is the
reason this paper leads with the recombination measurement. **Every factor
examined -- submission accession, collection period, isolation source -- moves
the geographic count substantially and moves r/m by at most a few percent.** The
recombination result is robust to specification in a way the geographic one is
not.

### 9. Reproducibility

Two executions were run to completion independently, on different hardware. The
**reported run** covered the 86-unit workstation partition (85 units after the
post-hoc correction) on a 22-core workstation, 8,178 tasks; the **cross-hardware
control** covered the 88-unit refinement on an NVIDIA DGX Station A100, 8,174
tasks. Both completed with zero task failures, zero cached and zero ignored, and
verification was per-unit rather than by exit code, comparing units requested
against units that produced Gubbins output and reading status, exit code and
confidence tier per replicon-unit. **172 of 172 and 176 of 176 replicon-units
completed at the highest confidence tier.** The two executions recorded the same
Nextflow script identifier (a hash of the workflow definition) and identical
containerized tool versions, so they ran byte-identical pipeline code and differ
only in Nextflow version and resource profile. Across the 82 units of shared
membership, r/m agreed to a median relative difference of 0.36%.

**Across the 82 units of identical membership, r/m agrees to a median absolute
difference of 0.0145, 0.38% relative, with a maximum of 1.32.** Two independent
runs on different hardware agreeing to about 0.4% on the median unit is the
empirical basis for treating the partitions as comparable, rather than assuming it
from configuration. The two units deliberately left unrefined as controls
reproduce almost exactly, at 1.32 against 1.31 and 0.75 against 0.75.

This matters more than a routine reproducibility statement, because Gubbins
parameter settings shift r/m by 0.47-fold to 0.78-fold non-uniformly with no
correction factor, so estimates from different settings cannot be pooled. All
parameters were pinned rather than left at repository defaults for that reason.

---

## Discussion

**The reported recombination rate for this species depends on a step nobody has
been reporting.** Our in-window median of 7.70 sits close to Nandi's 7.2 [7] and
above Seng's per-lineage values of 3.7, 4.6 and 2.2 [8]. Read naively, our
all-unit median of 5.51 would have sat between them and looked unremarkable. It is
not a rate. It is a median taken across 47 measurements and 38 detection
failures, and the failures pull it down from both directions at once. That the two published
genome-wide estimates were both computed within clades or lineages is not
incidental, and it means the comparison is like for like only once the window is
applied.

**A low r/m is the most misleading output this method produces.** The collapse is
symmetric, so a unit that is too clonal and a unit that is too diverse both return
values that read as evidence of clonal evolution. Our own analysis made this error
before the window was applied, treating two above-ceiling units as clean because
their r/m was among the lowest in the run. The null experiment shows why the
intuition fails. Units at the bottom of the r/m distribution exceed a matched
zero-recombination null by more than 300-fold, so they contain abundant real
recombination and simply less of it relative to mutation. Low r/m and low
recombination are different statements, and only one of them is supported.

**The operating range is a construct calibrated on one dataset, and we say so.**
The floor is bracketed 3.1-fold wide and every observation supporting it is
inadmissible on its own terms. Only three units fall below the bound, two are
unambiguous mixtures so their failures are attributable to structure rather than
diversity, and the third cannot be assessed because modality is interpretable only
inside the diversity range whose lower bound is the quantity being derived. That
circularity is real and we could not break it. The honest description of the floor
is the lowest diversity at which a unit has been observed to work, not a measured
threshold. Resolving it requires a unimodal unit of n of 25 or more between 535
and 1,265 mean pairwise SNPs, which this partition does not contain. The ceiling
is better bracketed at 1.36-fold but has a counter-example. Both should be treated
as a working range for this genome and this tool version, and re-verified against
any new partition.

**The consequence for outbreak and attribution genomics is specific and
uncomfortable.** Published *B. pseudomallei* transmission calls use SNP thresholds
of 0 to 5, with an upper bound of 15 taken from 17 informative pairs in a single
study that applied no recombination correction [15]. That regime is precisely
where Gubbins detects only 5% to 10% of real recombination events [11]. One step
up in scale, recombination accounts for most of the SNP distance. Recombination is
therefore most consequential and least detectable at exactly the scale where
outbreak calls are made. The published examples bear this out in both directions.
A genuine point-source outbreak spanned 1,328 SNPs of which only about 5% survived
recombination filtering, and isolates sharing a sequence type have been reported
more than 20,000 SNPs apart. [CONFIRM] retrieve and cite the primary sources for
both figures before using them, per `BACKGROUND_RESEARCH_2026-09-02.md` section
12.3.

**Partitioning before measuring is a biological requirement, not a computational
convenience.** Clade-specific restriction-modification systems restrict interclade
DNA uptake, and genomic clades behave as functional units of genetic isolation
[7]. A species-wide r/m would average across barriers that exist in nature. This
also explains how geographic signal survives the recombination load at all,
because recombination homogenizes within a population while leaving between-
population structure largely intact. The caveat is that the restriction-
modification result comes from 106 strains in one restricted Asian locale, and
whether it holds globally has not been tested.

**Two failure modes are worth the field's attention regardless of the biology.**
The RAxML run-identifier crash would have destroyed a quarter of this partition
while reporting a model-fitting failure, and it was misdiagnosed for an entire
prior investigation as reference toxicity. The reference-branch contamination of
r/m moved a median from 1.85 to 6.30 in an earlier partition, which is the
difference between reporting a moderately recombinogenic organism and a strongly
recombinogenic one. Neither produced an error. Both produced plausible numbers.
The general lesson is the one this project adopted as a working rule, which is to
check per-item values and never infer from a summary line. In the reference-branch
case the diagnosis that broke it open was sorting the per-branch numbers, where a
single branch held 96% of the signal, and that check should have preceded the
correlation analysis that was attempted first.

**What this work does not support.** No dating was attempted and none should be
inferred. The global tree across units is not recombination-corrected and must not
be, because across 85 divergent lineages no shared clonal background exists and
Gubbins would call most of the alignment recombinant. Its branch lengths include
recombination and no r/m may be derived from it. Grafted per-unit trees mix branch
length units and are a topology aid rather than a rate-comparable object. Nothing
here reconstructs direction of spread or migration rates. A collection that is
about 70% one country cannot support that, and no amount of analysis will fix it.

**Limitations.** Beyond the floor bracket already discussed, a quarter of the
analyzable set is unscreened for modality because it falls below n of 25 where
modality is undecidable, and the r/m safety net acts only after the fact.
Within-BioProject correlation is unmeasured, so effective sample size is uncertain.
No published benchmark exists for these tools on a two-replicon 7.2 Mb genome, and
the behavior of the subtree merge under recombination remains unvalidated. The
sensitivity bound rests on one unit and one replicon with terminal-branch implants
only, so it does not speak to clade-level imports. Variant calling by split k-mers
under-recovers clustered SNPs, at about 15% recovery within 10 bp of a neighbor
and 72% at 10 to 31 bp, which materially affects median tract length and makes the
5 kb figure caller-dependent, though pooled r/m is not shifted in a consistent
direction and no stable correction factor exists. The collection carries no
assembly-quality screen beyond a non-binding file-size minimum, retaining 45
assemblies above 500 contigs and 9 above 1,000, and although the measured effect
on the reported statistics is not detectable, the screen that found the two
oversized assemblies was ad hoc.

**What would settle the open questions.** A unimodal unit of adequate size between
535 and 1,265 mean pairwise SNPs would fix the floor. Extending the ClonalFrameML
comparison from six units to the full in-window set would establish whether the
rank disagreement between estimators is real or is an artifact of six points.
[CONFIRM] state the ClonalFrameML result in Results or drop it from the
Discussion, since the current draft mentions it nowhere. And quantifying
whole-genome geographic attribution accuracy, with a cross-validated
misclassification rate, remains unclaimed by anyone [14] and is the natural next
step for this collection once the sampling frame is defensible.

---

## Methods

Condensed from `METHODS_DRAFT_2026-08-19.md`, which remains the authoritative
record. Sections 2.1 to 2.11 of that document describe method development and
calibration, and section 2.12 describes the production analysis. Where they
conflict, 2.12 governs.

### Genome collection and assembly

[CONFIRM] Full provenance of the 2,802-genome curated collection, including
accession sources and inclusion dates.

Short-read isolates were assembled with SPAdes via TheiaProk `digger_denovo` with
`assembler=spades`, overriding the pipeline default of SKESA explicitly. Three
isolates retained SKESA assemblies for documented reasons. For two, the library
insert of 145 bp was shorter than the 151 bp read length, so pairs overlapped
fully and read through into adapter, and `--only-assembler` bypassed error
correction, collapsing SPAdes to 4.3 Mb against SKESA's 6.96 Mb. For the third,
SPAdes assembled 11.88 Mb and revealed foreign content that SKESA had suppressed.

Assemblies were gated on core-genome coverage and gene-count ratio rather than on
length or contiguity. The gene-count-ratio threshold of 1.20 or less was
calibrated on PacBio CLR failures at 1.35 or more and has no discriminating power
on near-complete assemblies, where contiguity cannot mask residual indel error.
Two Oxford Nanopore assemblies were therefore re-screened with BUSCO v5.8.2
against contiguity-matched complete genomes. Three complete two-contig genomes
each returned 688 complete, 0 fragmented and 0 missing, against 654/22/12 and
623/44/21 for the two Nanopore assemblies, the latter worse than a 1,388-contig
short-read draft. Because contiguity cannot explain a fragmented BUSCO score in a
two-contig assembly, the deficit is attributed to frameshifts from residual
indels, and gene calls agreed, with one Nanopore assembly predicting 6,474 CDS at
a mean length of 308 aa and 11.8% under 100 aa against 5,765 to 5,967 CDS at 343
aa and 8.0% to 8.6% for the complete genomes.

Tree geometry confirmed this independently. Both Nanopore isolates fell in a
10-isolate unit from one Ghanaian batch, 8 short-read and 2 Nanopore, sharing
provenance, batch and reference so that only platform differs. Terminal branch
lengths were 0.11838 and 0.15568 for one Nanopore isolate and 0.05415 and 0.08450
for the other, against a longest short-read tip of 0.00142 and 0.00144 and a
short-read median of 0.00056 and 0.00077, so the Nanopore terminal branches are 38
to 59 times the longest short-read tip in their own unit while every short-read
member falls within 0.4 to 2.5 times the median. Both were excluded. The
discriminating signal was rank within batch, the top 2 of 171 against a batch
median of 0.97, rather than the absolute ratio. **We recommend that assemblies at
5 contigs or fewer be screened on BUSCO fragmented plus missing against a
complete-genome baseline of zero, and that gene-count ratio be treated as a
within-batch outlier test rather than an absolute threshold.**

### Partitioning

PopPUNK v2.7.6, sketch database over all assemblies at k of 15 to 31 in steps of
2, fitted with a Gaussian mixture at K of 5 followed by boundary refinement.
Within each strain, PopPIPE built a split-k-mer alignment with SKA v0.4.0, a
neighbor-joining guide tree and a fastbaps hierarchical partition at three levels,
analyzed at level 1. Units were retained at n of 7 or more.

Units were screened for internal population structure using the pairwise core
distances already present in the PopPUNK database, all 4,426,800 pairs. Gate 1 is
diversity and Gate 2 is modality, applied in that order.

### Reference selection and defline normalization

Per-unit references were chosen by a completeness gate of 2 contigs or fewer and
centrality ranking within the unit, with empirically poor references blocklisted.
Units containing no complete genome borrow the nearest from outside. 35 distinct
references served the 85 units. Reference deflines were normalized before analysis
for the reason given in Results section 7, with sequence content verified
byte-identical.

### Variant calling, recombination and r/m

Snippy 4.6.0 against the unit reference with replicons split and replicons below
100 kb discarded, so that no alignment spans a contig junction. Gubbins 3.4.3 at 5
iterations, minimum 3 SNPs per recombination block, hybrid tree builder disabled,
starting tree skipped, maximum unit size 1,000. These parameters are pinned rather
than left at defaults because Gubbins settings shift r/m by 0.47-fold to 0.78-fold
non-uniformly with no correction factor.

r/m is pooled rather than averaged, as the sum of SNPs inside recombinations over
the sum of SNPs outside, summed over branches and over both replicons of a unit.
Per-branch ratios are undefined where a branch carries no SNPs outside
recombination and are noisy on short branches, so averaging lets the least
informative branches dominate. Both replicons are pooled because they share one
genealogy, and their agreement is a consistency check rather than evidence of
validity. External reference branches are excluded before pooling.

### Phylogenetics

Per unit, after recombination removal, IQ-TREE 2.2.6 under GTR with
ascertainment-bias correction, with model and constant-site counts from a per-unit
preflight and branch support enabled. Gubbins' own node-labelled trees are
retained as a second estimator. Across units, one medoid per unit, the member
minimizing mean SNP distance to the rest of its unit computed on the
recombination-filtered alignment and excluding the reference taxon, then a parsnp
1.7.4 core-genome alignment over those medoids and IQ-TREE under GTR with
ascertainment-bias correction.

Constant-site handling was tested across 62 unit-replicons. Conservative counting
removes a median of 0.0% of constant sites, total tree length moves by a median
ratio of 1.001, and per-branch lengths on shared splits correlate at a median r of
1.0000 and a minimum of 0.9988. The permissive count is reported. Shared-split
agreement is a median of 100% but falls to 69.1% in the worst unit, so the
invariance claim is about branch-length scale rather than about identity of every
split.

### Metadata

Country, sub-region, BioProject and collection date were joined from a curated
table, attempted against `sample_id`, `FASTA_name` and `Assembly Accession` in
that order. A naive exact join on `sample_id` alone matches 73% and accession
prefix alone 86%, whereas all three together reach 99.9%. Genomes without metadata
are retained with empty fields rather than dropped, so per-unit denominators
remain correct. The country column conflates US territories with the mainland, and
of 21 genomes labelled USA, 10 are Puerto Rico or the US Virgin Islands, leaving
11 from the mainland, so analyses of US origin must disaggregate them.

### Software, compute and reproducibility

| Tool | Version | Role |
|---|---|---|
| Nextflow | 25.10.0 production, 25.04.6 control | workflow |
| PopPUNK | 2.7.6 | strain assignment |
| SKA | 0.4.0 | split-k-mer alignment within strains |
| fastbaps via PopPIPE | 3 levels | within-strain subclustering |
| Mash | sketch size 50,000, k = 21 | distances for reference choice and medoids |
| Snippy | 4.6.0 | reference-based variant calling |
| Gubbins | 3.4.3 | recombination detection |
| RAxML | 8.2.12 within Gubbins | tree builder inside Gubbins |
| IQ-TREE | 2.2.6 | per-unit and global trees |
| parsnp | 1.7.4 | core-genome alignment for the global tree |
| BUSCO | 5.8.2, `burkholderiales_odb10` | assembly base-accuracy screening |

The Mash sketch size is 50,000 rather than the 10,000 named in the repository
configuration, and the sketch header is authoritative.

No stage is GPU-accelerated. The hardware requirement is memory and it falls on
partitioning rather than on the SNP analysis. Building a split-k-mer alignment for
the 901-genome strain monolithically requires about 500 to 600 GB, which exceeded
the control workstation, so it was executed in 8 batches of 113 followed by a
merge. Equivalence was verified rather than assumed. On a 60-genome subset,
monolithic and batched builds produced the same taxa and identical alignment
column multisets, differing only in column order, which the aligner does not
define and which the site-independent model does not use.

The workflow was driven in curated mode, in which partition and references are
taken as given. A clean exit does not establish that every unit succeeded, because
the workflow uses `errorStrategy 'ignore'`, so verification is per-unit against
`Summaries/cluster_phylogeny_summary.csv`.

---

## Data availability

[CONFIRM] and decide before submission. This is the section most likely to attract
editorial pushback, and the project's own constraints make it non-trivial.

Accessions for all publicly derived genomes will be listed in Supplementary Table
S1. [CONFIRM] whether newly generated assemblies will be deposited, and where.

Analysis-unit membership and per-unit references are available as
`curated_L1v4c_clusters.final.tsv` and `curated_L1v4c_refs.final.tsv`. [CONFIRM]
the deposition venue.

**A restriction must be stated and justified.** *B. pseudomallei* is a US Federal
Select Agent, and the study metadata joins accession to isolation location,
collection date and exposure label, which is re-identifiable for rare cases. The
analysis code repository therefore tracks no isolate-level data by design.
[CONFIRM] with the corresponding institution's biosafety and legal offices what
may be released, and draft the availability statement to match. Journals will
accept a documented restriction, but they will not accept a vague one.

## Code availability

Analysis, partitioning, reference selection, calibration and diagnostic code is at
`github.com/PHemarajata/bp-recombination-aware-snps`. The Nextflow workflow is at
`github.com/PHemarajata/wf-assembly-snps-mod`. [CONFIRM] whether both are public
at submission, and archive a release to Zenodo for a DOI.

## Author contributions

[CONFIRM] using CRediT taxonomy once the author list is settled.

## Acknowledgements

[NAME]. [CONFIRM] whether the compute resources used require specific
acknowledgement text.

## Funding

[CONFIRM]. State "no specific grant" if that is accurate, rather than omitting the
section.

## Competing interests

[CONFIRM]. The authors declare no competing interests, if accurate.

## Ethics

[CONFIRM] whether institutional review was sought or whether an exemption applies,
given that the collection is derived from previously sequenced isolates and public
data.

---

## Figures and tables

Planned. None of these has been produced yet.

**Figure 1.** The operating range. Pooled r/m against mean pairwise core SNPs for
all 85 units, log x-axis, with the window shaded and the three Gate 1 classes
colored. This is the paper's central figure and it should carry the argument
alone. [CONFIRM] whether union coverage is added as a second panel, since it fails
in only one direction and that asymmetry is itself the reason single-statistic
approaches do not work.

**Figure 2.** Detection bounds. Panel A, the null distribution of pooled r/m over
1,519 replicates against the observed range, on a log scale so the 427-fold to
2,234-fold separation is visible. Panel B, spike-in recovery against donor
divergence with the measured value marked.

**Figure 3.** The global maximum-likelihood tree over 88 unit medoids, annotated
by dominant country and Gate 1 class. Must carry the caption warning that it is
not recombination-corrected and that no r/m may be derived from it.

**Figure 4.** The confounder control, per unit: country permutation p-value
against BioProject permutation p-value, log-log, on identical trees with
identical machinery. The diagonal is equal signal, and only the upper-left region
is geography. Six of 85 units land there, two of them marginally. The 37
single-country units are absent by construction, since the test cannot run on
them. Generated by `make_figure4_bp.py`, which refuses to draw if the association
table's interpretation counts disagree with its caption.

**Table 1.** Panel and partition summary.
**Table 2.** Gate 1 classification and r/m by class.
**Table 3.** The `strain_1_L1_26` refinement, before and after.
**Table 4.** Spike-in recovery.
**Table 5.** Tree-builder comparison.

**Supplementary Table S1.** Per-genome accession, unit, country, BioProject,
collection date, subject to the data availability decision.
**Supplementary Table S2.** Per-unit r/m, diversity, Gate 1 class, reference,
union coverage, median tract length, maximum surviving branch length.
**Supplementary Table S3.** Per-unit phylogeography test results.

---

## References

Verified against PubMed records. Full provenance and per-citation caveats are in
`BACKGROUND_RESEARCH_2026-09-02.md`.

1. Wiersinga WJ, Virk HS, Torres AG, Currie BJ, Peacock SJ, Dance DAB,
   Limmathurotsakul D. Melioidosis. *Nat Rev Dis Primers* 2018;4:17107. PMID
   29388572. doi:10.1038/nrdp.2017.107
2. Meumann EM, Limmathurotsakul D, Dunachie SJ, Wiersinga WJ, Currie BJ.
   *Burkholderia pseudomallei* and melioidosis. *Nat Rev Microbiol*
   2024;22(3):155–169. PMID 37794173. doi:10.1038/s41579-023-00972-5
3. Limmathurotsakul D, Golding N, Dance DAB, Messina JP, Pigott DM, Moyes CL,
   Rolim DB, Bertherat E, Day NPJ, Peacock SJ, Hay SI. Predicted global
   distribution of *Burkholderia pseudomallei* and burden of melioidosis. *Nat
   Microbiol* 2016;1:15008. PMID 26877885. doi:10.1038/nmicrobiol.2015.8
4. Gee JE, Bower WA, Kunkel A, Petras J, Gettings J, Bye M, et al. Multistate
   outbreak of melioidosis associated with imported aromatherapy spray. *N Engl J
   Med* 2022;386(9):861–868. PMID 35235727. doi:10.1056/NEJMoa2116130
5. Petras JK, Elrod MG, Ty MC, Dawson P, O'Laughlin K, Gee JE, et al. Locally
   acquired melioidosis linked to environment, Mississippi, 2020–2023. *N Engl J
   Med* 2023;389(25):2355–2362. PMID 38118023. doi:10.1056/NEJMoa2306448
6. Gee JE, Gulvik CA, Elrod MG, Batra D, Rowe LA, Sheth M, Hoffmaster AR.
   Phylogeography of *Burkholderia pseudomallei* isolates, Western Hemisphere.
   *Emerg Infect Dis* 2017;23(7):1133–1138. PMID 28628442.
   doi:10.3201/eid2307.161978
7. Nandi T, Holden MTG, Didelot X, Mehershahi K, Boddey JA, Beacham I, et al.
   *Burkholderia pseudomallei* sequencing identifies genomic clades with distinct
   recombination, accessory, and epigenetic profiles. *Genome Res*
   2015;25(1):129–141. PMID 25236617. doi:10.1101/gr.177543.114
8. Seng R, Chomkatekaew C, Tandhavanant S, Saiprom N, Phunpang R, Thaipadungpanit
   J, et al. Genetic diversity, determinants, and dissemination of *Burkholderia
   pseudomallei* lineages implicated in melioidosis in Northeast Thailand. *Nat
   Commun* 2024;15:5699. PMID 38972886. doi:10.1038/s41467-024-50067-9
9. Pearson T, Giffard P, Beckstrom-Sternberg S, Auerbach R, Hornstra H, Tuanyok A,
   et al. Phylogeographic reconstruction of a bacterial species with high levels
   of lateral gene transfer. *BMC Biol* 2009;7:78. PMID 19922616.
   doi:10.1186/1741-7007-7-78
10. Chewapreecha C, Holden MTG, Vehkala M, Välimäki N, Yang Z, Harris SR, et al.
    Global and regional dissemination and evolution of *Burkholderia
    pseudomallei*. *Nat Microbiol* 2017;2:16263. PMID 28112723.
    doi:10.1038/nmicrobiol.2016.263
11. Croucher NJ, Page AJ, Connor TR, Delaney AJ, Keane JA, Bentley SD, Parkhill J,
    Harris SR. Rapid phylogenetic analysis of large samples of recombinant
    bacterial whole genome sequences using Gubbins. *Nucleic Acids Res*
    2015;43(3):e15. PMID 25414349. doi:10.1093/nar/gku1196
12. Didelot X, Wilson DJ. ClonalFrameML: efficient inference of recombination in
    whole bacterial genomes. *PLoS Comput Biol* 2015;11(2):e1004041. PMID
    25675341. doi:10.1371/journal.pcbi.1004041
13. Zheng H, Qin J, Chen H, Hu H, Zhang X, Yang C, et al. Genetic diversity and
    transmission patterns of *Burkholderia pseudomallei* on Hainan island, China,
    revealed by a population genomics analysis. *Microb Genom* 2021;7(11). PMID
    34762026. doi:10.1099/mgen.0.000659
14. Dale J, Price EP, Hornstra H, Busch JD, Mayo M, Godoy D, et al.
    Epidemiological tracking and population assignment of the non-clonal
    bacterium, *Burkholderia pseudomallei*. *PLoS Negl Trop Dis* 2011;5(12):e1381.
    doi:10.1371/journal.pntd.0001381. **PMID 22163051 unconfirmed against an
    index. Verify.**
15. Webb JR, Mayo M, Rachlin A, Woerle C, Meumann EM, Rigas V, et al. Genomic
    epidemiology links *Burkholderia pseudomallei* from individual human cases to
    *B. pseudomallei* from targeted environmental sampling in northern Australia.
    *J Clin Microbiol* 2022;60(3):e0164821. PMID 35080450. doi:10.1128/JCM.01648-21

Additional references to add once the corresponding sections are written.

16. Lees JA, Harris SR, Tonkin-Hill G, Gladstone RA, Lo SW, Weiser JN, et al. Fast
    and flexible bacterial genomic epidemiology with PopPUNK. *Genome Res*
    2019;29(2):304–316. PMID 30679308. doi:10.1101/gr.241455.118
17. [CONFIRM] fastbaps. Tonkin-Hill G, Lees JA, Bentley SD, Frost SDW, Corander J.
    Fast hierarchical Bayesian analysis of population structure. *Nucleic Acids
    Res* 2019. Retrieve and verify.
18. [CONFIRM] SKA2, Snippy, IQ-TREE 2, parsnp, BUSCO, seq-gen, RAxML. Retrieve and
    verify each before submission.
19. Godoy D, Randle G, Simpson AJ, Aanensen DM, Pitt TL, Kinoshita R, Spratt BG.
    Multilocus sequence typing and evolutionary relationships among the causative
    agents of melioidosis and glanders, *Burkholderia pseudomallei* and
    *Burkholderia mallei*. *J Clin Microbiol* 2003;41(5):2068–2079. PMID 12734250.
    doi:10.1128/JCM.41.5.2068-2079.2003
20. Holden MTG, Titball RW, Peacock SJ, Cerdeño-Tárraga AM, Atkins T, Crossman LC,
    et al. Genomic plasticity of the causative agent of melioidosis, *Burkholderia
    pseudomallei*. *Proc Natl Acad Sci U S A* 2004;101(39):14240–14245. PMID
    15377794. doi:10.1073/pnas.0403302101

---

## Submission checklist

Ordered by what blocks submission first.

1. ~~Run the phylogeography analysis.~~ **Done.** Results section 8
   is otherwise a specification. Repoint both `--assignments` and `--trees`
   together, since the default points at an old output directory and a mismatch
   produces entirely plausible numbers. A previous run of this script silently
   joined v3 assignments to v1 trees and reported 82 units against a 91-unit
   partition, caught only by noticing the unit count.
2. **Fill the remaining [CONFIRM] markers.** The analysis markers are cleared
   (Results 3's r/m distribution is filled from NUMBERS.tsv). What remains is
   categorized in `SUBMISSION_TODO.md`: two editorial decisions resolvable now
   (the ClonalFrameML mention, the union-coverage panel), three citation retrievals,
   and the external chain (deposition, funding, author roles, IRB), which is the
   real critical path.
3. **Settle the data availability position** with biosafety and legal review
   before choosing a journal, because some journals will not accept a restriction
   this broad.
4. **Produce Figures 1 to 4 and Tables 1 to 5.**
5. **Verify the remaining citations**, including the 12 items listed in
   `BACKGROUND_RESEARCH_2026-09-02.md` section 12.3 and reference 14 above.
6. **Decide the ClonalFrameML comparison.** It currently appears in the Discussion
   only. Either report the six-unit result in Results with its caveats, or remove
   the Discussion sentence.
7. **Author list, affiliations, contributions, funding and ethics.**
