# How to split this work into papers, and what to write first

Written 2026-09-02. A recommendation, not a decision. It assumes the current
state: the 88-unit v4c run complete and verified, the calibration and validation
work done, the literature closed in `GAP1`-`GAP4` and
`BACKGROUND_RESEARCH_2026-09-02.md`, and the phylogeography analysis specified
but not yet run.

## The short answer

Three papers, not more, and one optional review. Write the calibration and
measurement paper first, because it is close to finished and because it does not
need the phylogeography analysis at all. That last point is the one that matters
for scheduling. The thing least ready is not on the critical path for the thing
most ready.

| | Paper | Ready | Blocking |
|---|---|---|---|
| 1 | Operating range and the recombination rate | ~80% | figures, `[CONFIRM]`s, data availability |
| 2 | Geographic structure under recombination correction | ~40% | run the analyses, sampling frame |
| 3 | Attribution of exposure origin | ~15% | targeted sampling, a validated accuracy figure |
| R | Review, optional | ~60% raw | choose a narrower question |

## What there is to divide

Ten things, and they do not divide evenly.

The calibrated operating range for Gubbins, roughly 1,270 to 4,671 mean pairwise
core SNPs, with both bounds reported as brackets. The validation suite: a matched
zero-recombination null over 1,519 replicates, spike-in sensitivity at the
measured donor divergence, and a three-way tree-builder comparison. Two silent
failure modes, the RAxML 128-character run identifier and the reference branch in
the r/m denominator. The recombination result itself, r/m 7.38 across 47
in-window units of 2,342 genomes. Reproducibility at 0.38% across two independent
executions. The partitioning method. The phylogeography, pending. The attribution
angle, including the Americas unit with mainland US cases carrying no travel
history. The four literature reviews. And the pipeline.

## Paper 1. The operating range, and what it does to the reported rate

**Claim.** The recombination rate quoted for this species depends on a step
nobody reports. Detection works only inside a bounded range of population
diversity, we measured that range, and inside it r/m is 7.38 while outside it the
published-looking values are detection failures.

**Contents.** Calibration, the validation suite, both failure modes, the r/m
result, reproducibility. The `MANUSCRIPT_DRAFT_2026-09-02.md` already is this
paper, minus the geography section.

**Why it goes first.** It is the most complete. It is the enabling citation for
Papers 2 and 3, which both depend on recombination-corrected trees being
trustworthy. And it is genuinely unclaimed: three groups state the principle that
you subdivide until diversity falls inside the range where detection works, and
nobody has published where that range is.

**Cut geography from it entirely.** Not deferred, cut. The paper is complete
without it, and including a weak version would invite a reviewer to attack the
sampling frame in a paper whose argument does not depend on sampling at all.

**Journal.** *Microbial Genomics* is the best fit. It publishes calibration and
negative results, the audience is people who run these pipelines, it is open
access, and the format tolerates the amount of validation detail this work
carries. *Genome Research* or *Nature Communications* are reachable if you want
more visibility, at the cost of compressing the validation into supplementary
material, which would weaken the part of the paper most likely to survive.

**The reviewer objection to prepare for.** The floor is bracketed 3.1-fold wide
and every observation supporting it is inadmissible on its own terms, for reasons
the draft states. A reviewer will push there. The answer is not to defend a
precision the data do not have. It is to lead with the bracket, call the floor
the lowest diversity at which a unit has been observed to work, and name the
experiment that would settle it, which is a unimodal unit of n at least 25
between 535 and 1,265. The ceiling has a counter-example and the same treatment
applies. A working range honestly bracketed is more useful to the field than a
threshold asserted, and it is also what the evidence supports.

## Paper 2. SUPERSEDED 2026-09-02 -- this claim did not survive its own control

> **The analysis has since been run, and the claim below is false for this
> collection.** 26 of 85 units cluster by country taken alone; **6 survive the
> BioProject control**, and two of those clear it by a hair. The control removes
> **77% of the apparent signal**. The single-country enrichment listed under
> "contents" turns out to describe the *untestable* stratum, not evidence: those
> 37 units are ones where the permutation test cannot run at all, and 30 of the
> 37 are Thailand against Thailand being 67% of the collection.
>
> **The finding moved to Paper 1** as Results section 8, reframed again on
> 2026-09-02 as what it actually is: **country and collection history are not
> separable in this collection**, and the count ranges 6-24 depending on a
> confounder specification the data cannot settle. That belongs beside the
> detection window,
> because both say the same thing -- an apparent signal is not a measurement
> until you have shown what else could produce it.
>
> **Paper 2 therefore needs a different subject, or none.** Do not write the
> paper below. Options worth considering: the attribution work (currently Paper
> 3), or a melioidosis-community paper built on the six units as case studies
> rather than as a structural claim. Neither is drafted.

**Claim, as originally written and now known to be wrong.** After removing
recombination, country structure persists in the phylogeny and is not explained
by which laboratory sequenced what.

**Contents.** The per-unit Fitch permutation test, the BioProject confounder
control run on identical trees, the single-country enrichment test against the
collection's own country distribution, replicon concordance, and an honest
sampling-frame section.

**Why second and not merged into Paper 1.** Different audience. Paper 1 is read
by people choosing a recombination tool. This one is read by people who study
melioidosis. It also carries a liability Paper 1 does not, which is that the
collection is about 70% one country, and that has to be argued rather than
mentioned.

**Journal.** *PLoS Neglected Tropical Diseases* reaches the melioidosis
community and cares about the public health framing. *Microbial Genomics* again
if you would rather keep both papers in one venue.

**What it must not claim.** No direction of spread, no migration rates, no dates.
The sampling cannot support any of it, and `GAP4` documents why in detail. The
paper is stronger for saying so.

## Paper 3. Attribution of exposure origin

**Claim.** A genome can place an unplaced case, and here is how accurately.

**Why it is furthest out and worth waiting for.** It is the paper closest to
APHL's actual mission and the only one that addresses a genuine hole in the
literature. Whole-genome sequencing is repeatedly asserted to resolve strain
origin, but no published work reports a misclassification rate, a confidence
measure, or a cross-validated accuracy figure at any spatial scale finer than a
two-population continental split from MLST. Nobody has claimed it.

**What it needs.** The two units that remain assign-only, Mississippi at n of 5
and Mexico at n of 6, need the additions to cross the analysis threshold. It
needs a cross-validation design, holding out genomes of known origin and
measuring how often the method places them correctly and how confident it is when
it is wrong. And it needs the sampling frame to be defensible rather than
inherited.

**Do not attempt it before Papers 1 and 2.** An attribution claim built on
uncalibrated recombination correction is exactly the failure this project exists
to avoid.

## Optional. A review

`GAP1` through `GAP4` are roughly 470 KB of verified synthesis, and the most
publishable slice is the reference-choice problem in recombinogenic bacteria.
That section already assembles evidence nobody has assembled: the general
bacterial literature showing distance-to-reference dominates pipeline choice, the
observation that this organism sits in the worst part of that range, at least
four references in concurrent use with no work bridging their coordinate systems,
and the fact that closest-relative reference selection is widely practised in
this field and has never been validated in it.

Low marginal cost, since the research is done. Useful as a citation anchor for
Papers 1 to 3. And a reasonable first-author opportunity for an early-career
colleague if you have one, since the shaping work is real but the retrieval is
finished.

## What not to split out

**The pipeline as a software note.** It belongs in Paper 1 as a code-availability
item. A separate note on a modified workflow would be thin and would fragment
citations across two papers that need to be cited together.

**The failure modes as a short correspondence.** They are more convincing
embedded in a paper that shows what they did to real results than as a standalone
caution nobody cites.

**Calibration separately from the r/m result.** They need each other. The
calibration is only convincing because it was applied at scale, and the r/m
figure is only meaningful because of the calibration. Splitting them would
produce two papers that each fail their reviewer for lack of the other half.

## Sequencing, and the one dependency that matters

Paper 1 does not depend on any analysis that has not been run. Everything in it
is measured. The remaining work is figures, filling `[CONFIRM]` markers from run
artefacts, and settling data availability.

Papers 2 and 3 both depend on the phylogeography analysis, which is now runnable
via `run_manuscript_analyses.sh`. Running it does not block Paper 1 and should
not delay it.

The single highest-risk item across all three is not analytical. It is the data
availability statement. *B. pseudomallei* is a Federal Select Agent and the study
metadata joins accession to isolation location, collection date and exposure
label, which is re-identifiable for rare cases. Some journals will not accept a
restriction that broad. Settle it with biosafety and legal review before choosing
a journal, not after a desk rejection.
