# Where our methods sit relative to the published B. pseudomallei literature

Compiled 2026-08-21. Literature retrieved via **PubMed** and publisher sites;
DOIs linked throughout. Methods for our own work are from this repository.

**Purpose:** know precisely what is standard, what we do differently and why,
and what appears to be genuinely new — so that in review we can defend each
choice rather than discover it under fire.

---

## 1. The comparison set

| # | study | n | scope | why it matters to us |
|---|---|---|---|---|
| **A** | Seng, Chomkatekaew, Chewapreecha *et al.* 2024, *Nat Commun* — [10.1038/s41467-024-50067-9](https://doi.org/10.1038/s41467-024-50067-9) | **1,391** | 9 hospitals, NE Thailand, 2015–2018 + neighbours | The state of the art. Densest Bp collection published. Closest methodological sibling. |
| **B** | Gee *et al.* 2017, *EID* 23(7) — [Western Hemisphere phylogeography](https://wwwnc.cdc.gov/eid/article/23/7/16-1978_article) | 26 | Western Hemisphere | Established the ST92 / "Western Hemisphere strain" framing our Mississippi result sits inside. |
| **C** | Petras, Elrod, **Gulvik** *et al.* 2023, *NEJM* — [10.1056/NEJMoa2306448](https://doi.org/10.1056/NEJMoa2306448) | 3 clinical + 3 environmental | Mississippi Gulf Coast | The reference event for our tightest cluster. |
| **D** | McLaughlin, **Gulvik**, Sue 2022, *PLoS NTD* — [10.1371/journal.pntd.0009882](https://doi.org/10.1371/journal.pntd.0009882) | 1,523 RefSeq | global, *in silico* | A rival typing scheme (PBP dual-locus) aimed at the same geographic-origin question. |
| **E** | Ashcroft *et al.* 2021, *JCM* — [10.1128/jcm.00093-21](https://doi.org/10.1128/jcm.00093-21) | 469 | scheme development | The cgMLST scheme we used. |
| **F** | Chomkatekaew, Chewapreecha *et al.* 2021, *Front Microbiol* — [10.3389/fmicb.2020.612568](https://doi.org/10.3389/fmicb.2020.612568) | review | host–pathogen evolution | Context for why Bp diversity is what it is. |
| **★** | **This work** | **2,976** (2,352 analysed) | global, 43 countries | — |

**Note on lineage:** our pipeline is a fork of
`bacterial-genomics/wf-assembly-snps`; the manifest reads
`author = "Christopher A. Gulvik, PHemarajata"`. We share tooling ancestry with
CDC (**C**, **D**). Worth stating in the methods — it is a strength, not a
footnote.

---

## 2. Method-by-method comparison

| dimension | **A** — Chewapreecha 2024 | **B** — Gee 2017 | **★ Ours** | verdict |
|---|---|---|---|---|
| **Population structure** | PopPUNK v2.6.0 → 3 dominant lineages; rhierbaps for sub-lineages | none (parsimony tree only) | PopPUNK → fastbaps → 88 units | **Same family.** Ours cuts finer because our diversity is global, not one region. |
| **Recombination** | **Gubbins v3.1.3, per lineage** | **not addressed at all** | **Gubbins per unit** + ClonalFrameML second detector | **Same as A.** Independent convergence on partition-then-correct is reassuring. |
| **r/m reported?** | **Yes — L1 3.7, L2 4.6, L3 2.2** | no | yes, per unit + per replicon | Directly comparable. Their range brackets ours. |
| **Reference strategy** | K96243 population-wide; **custom reference per lineage** | reference-free (kSNP3) | **constrained medoid per unit**, completeness as a hard gate | Same instinct as A, formalised into a rule. |
| **Variant calling** | Snippy v4.6.0 | kSNP3 | ska map / contig mapping, coordinate-carrying | Equivalent. |
| **Tree** | IQ-TREE v2.0.3, **TVM+F+ASC+R6**, 1000 bootstraps | maximum parsimony | IQ-TREE, **true constant-site counts (`-fconst`)** | **We differ, deliberately — see §3.1.** |
| **Pangenome / accessory** | **Panaroo — 15,237 genes (5,577 core, 9,660 accessory)** | no | **not yet** | **They are ahead of us here.** See §5. |
| **Sampling-bias control** | **subsample to equal n per province (15), permute ×1,000**; date-randomisation | none stated | **permutation holding composition fixed** + **BioProject companion test** | **Different confounders targeted — see §3.2.** |
| **Study / batch confound** | not addressed | not addressed | **explicit BioProject control per unit** | **Appears novel — §4.1.** |
| **Geographic aim** | **reconstruct** historical dispersal between 9 provinces | **assign** origin, case-study style | **predict** origin of an unknown isolate | Different questions. |
| **Geographic method** | ancestral state reconstruction (phytools `make.simmap`, Markov jumps); terrain/river/monsoon correlates | visual clade inspection | Fitch parsimony + permutation null, 3 scales | |
| **Dating** | **BactDating**; only sub-lineage 1.3 had temporal signal | no | **explicitly ruled out** — no clock signal | Consistent: both find Bp mostly undateable. |
| **Validation of geographic claims** | permutation tests on the reconstruction | **none systematic** | **leave-one-out AND leave-group-out on 26 known-exposure genomes** | **Appears novel — §4.2.** |
| **Resolution claimed** | province-level *within* NE Thailand | subregion within Western Hemisphere | **region yes, country no** | We are the most conservative. |

---

## 3. Where we differ from the state of the art, and why

### 3.1 Constant sites: true counts vs ascertainment correction

**They use `ASC`** (ascertainment-bias correction) in the IQ-TREE model.
**We pass true constant-site counts** via `-fconst`.

Both address the same problem — a tree built only from variable sites thinks
every site varies and inflates branch lengths. But `ASC` *estimates* the
correction from the data, while `-fconst` *supplies the measured counts*.

**Why it matters for this organism:** at ~68% GC, ascertainment correction pulls
base composition toward 25/25/25/25, which is badly wrong. With true counts the
tree reproduces the full-alignment base frequencies exactly.

**Defensible position:** ours is the more conservative choice and we can show the
composition argument. Not a criticism of theirs — with one dominant reference and
one region, the difference is likely small. **We should quantify it rather than
assert it**: run one unit both ways and report the branch-length difference.

### 3.2 Two different meanings of "sampling bias control"

This is the subtlest and most important comparison, and it would be easy to
mis-state in review.

**They control spatial sampling density.** Provinces contributed unequal numbers
of isolates, so they subsampled to 15 per province and permuted 1,000 times.
That answers: *is the dispersal pattern an artefact of some provinces being
sampled harder?*

**We control study of origin.** Country and BioProject are near-collinear in a
public collection, so we run the identical clustering test on both. That answers:
*is the geographic pattern actually a pattern of who did the sequencing?*

**These are not substitutes.** Their design largely avoids our problem — one
consortium, one protocol, one period, so study effects are near-constant.
Ours largely avoids theirs — we are not making within-country dispersal claims.

**The honest framing:** each collection's design forces a different control.
Ours is necessary *because* the collection is public and multi-study; theirs is
necessary *because* the sampling is spatially uneven. We should say this
explicitly rather than imply prior work was careless.

### 3.3 Reconstruct vs predict — the deepest difference

**A reconstructs history**: given the tree and the labels, where did lineages
move? **We predict for an unknown**: given a new isolate, where did it come from?

Reconstruction is scored by internal consistency; prediction is scored by whether
held-out cases come out right. **Prediction is a strictly harder test, and it is
why our headline result is more negative than theirs.** They report province-
level dispersal within NE Thailand; we report that country-level prediction fails
globally. Both can be true — theirs is within one country with dense sampling,
ours is between countries with sparse sampling.

---

## 4. What appears to be new in our approach

**Caveat, stated once and meant:** based on targeted searching, not a systematic
review. Write **"we are not aware of"**, never "first".

### 4.1 BioProject as a measured companion control

Found no example in the Bp literature or the wider bacterial-phylogeography
literature of study-of-origin used as a covariate in an association test.

**The advantage:** it converts "this cluster is Brazilian" into a testable claim.
Without it, 13 of our 88 units would have been reported as geographic signal when
they are indistinguishable from study signal. **That is 13 false claims avoided.**

Supporting context: the closest analogue,
[biased sampling confounding AMR prediction](https://doi.org/10.1371/journal.pbio.3003539)
(*PLOS Biology*, 24,000 genomes, five pathogens), is entirely about sampling bias
and never mentions BioProject, study or lab batch — the recognised confounder
there is phylogenetic structure.

### 4.2 Leave-group-out validation of geographic attribution

**The advantage:** it is the difference between 37% and 0%. Every apparent
country-level success under leave-one-out was a validation genome predicting
another validation genome of the same country. **Publishing the 37% would have
been reporting an artefact.**

The same *PLOS Biology* paper independently recommends "phylogeny-aware
cross-validation testing on held-out clades" — so the principle has support even
though we found no Bp application.

### 4.3 The resolution-invariance test

Scoring **7-locus MLST, 4,089-locus cgMLST, and whole-genome SNPs** through the
identical holdout: **0 / 17, 0 / 25, 0 / 19** at country level.

**The advantage:** it pre-empts the first reviewer question — *did you just need
more resolution?* — with a measurement across a 584-fold range rather than an
argument. We are not aware of this being done for any bacterial pathogen.

### 4.4 Raw and recombination-filtered distances reported as a pair

Standard practice reports one distance. We report both plus the masked fraction,
which exposes when closeness is an artefact of masking rather than relatedness.

**The advantage:** it is self-validating — filtered/raw tracks 1/(1+r/m) at rank
correlation +0.75 across 86 units, so two independent computations check each
other.

### 4.5 Two-detector concordance as a gate check

Running Gubbins **and** ClonalFrameML across the whole panel and comparing.
**A reports r/m from Gubbins alone**; nobody we found runs both at scale.

**The advantage:** it tells you whether "usable unit" is a property of the data or
of the tool. Current answer: absolute r/m differs ~5× between tools and rank
agreement is only rho ≈ 0.59, so **a threshold calibrated on one tool does not
transfer to the other.** That is a caution the field currently lacks.

### 4.6 Measured yield, not nominated count

We report that 44% of genomes were nominated for analysis and **25% survived**
acceptance criteria, per unit and with reasons.

**The advantage:** honest denominators. It also surfaced the analysability bias —
under-sampled countries fall into units too small to analyse, so the cases most
needing attribution are least likely to get it.

---

## 5. Where the literature is ahead of us

Worth being blunt about, since these are the gaps a reviewer will find.

| gap | who has it | what we should do |
|---|---|---|
| **Pangenome / accessory analysis** | **A** — Panaroo, 15,237 genes, lineage-specific gene sets | **Highest-value gap.** Accessory content may attribute geography where core cannot — see `IDEAS_AND_OPEN_QUESTIONS.md` §5. |
| **Functional follow-through** | **A** — transcriptomics of lineage-specific genes under environmental conditions | Out of scope for us; acknowledge. |
| **Environmental covariates** | **A** — terrain, altitude, river direction, monsoon | We have no environmental layer. Possible future work. |
| **Dense within-country sampling** | **A** — 9 hospitals, 4 years, one region | Structural. Our collection is public and global; we cannot fix this, only report it. |
| **Rival typing scheme** | **D** — PBP dual-locus typing for geographic origin | We should compare against it, or at least cite and explain why we chose cgMLST. |

---

## 6. Suggestions for what else belongs in this table

You asked for ideas. Dimensions worth adding as the work matures:

1. **Code and data availability** — is the analysis reproducible from published
   material? Ours is scripted end to end; this is a real differentiator and
   currently unrecorded.
2. **Whether recombination-corrected trees were merged**, and whether branch
   lengths were interpreted afterwards. We treat the merge as unsolved; anyone
   who grafted subtrees and then dated them has a problem worth noting.
3. **Reference-choice sensitivity** — did they test it? We measured it; most do not.
4. **How missing data is encoded** — the literal string `unknown` scored as a
   shared state was a real bug in our own code affecting 274 genomes. A cheap,
   embarrassing, and probably widespread failure mode.
5. **Multiple-testing correction** — applied at all, and over what family?
6. **Effective sample size vs nominal n** — 1,391 isolates from 9 hospitals in
   one region is not 1,391 independent observations, and neither is our 2,976
   from a few large BioProjects.
7. **Was the acceptance/exclusion rule stated before or after seeing results?**
   Ours has a written record of withdrawn thresholds; that is unusual and
   defensible.
8. **Organism-appropriate clock assumptions** — who attempted dating, on what
   evidence of temporal signal. **A** did it properly with a date-randomisation
   test and found only one sub-lineage dateable; that is the standard to match.

---

## 6a. Addendum 2026-08-21 — the Gulvik *in silico* paper and two newer CDC studies

Read after the main comparison. Three of these materially change our position.

### New rows for the comparison set

| # | study | n | what it does |
|---|---|---|---|
| **D** | McLaughlin, **Gulvik**, Sue 2022, *PLoS NTD* — [10.1371/journal.pntd.0009882](https://doi.org/10.1371/journal.pntd.0009882) | 1,523 RefSeq | Dual-locus (PBP) typing scheme for geographic origin |
| **G** | Brennan, Thompson, **Gulvik**, Paisie *et al.* 2025, *EID* — [10.3201/eid3109.250804](https://doi.org/10.3201/eid3109.250804) | 4 cases | **Melioidosis cases with unknown exposure source, Georgia USA, 1983–2024** |
| **H** | Sprenger, Gee, Elrod, Weiner, **Gulvik** 2026, *Microbiol Spectr* — [10.1128/spectrum.02926-25](https://doi.org/10.1128/spectrum.02926-25) | 1 MAG | Metagenome-assembled genome from the contaminated aromatherapy spray |
| **I** | Klimko *et al.* 2026, *EID* — [10.3201/eid3208.260069](https://doi.org/10.3201/eid3208.260069) | panel | Virulence of Western Hemisphere and Africa strains in mice |

### 6a.1 The DLST paper strengthens our validation claim considerably

**D makes country-level geographic claims with no held-out validation.** Direct
from the paper: *"Several STs were unique to strains originating from a specific
country or region."* Assignment was assessed against 127 strains and then 1,523
RefSeq genomes, but **no independent test set and no cross-validation**.

This is a CDC paper making precisely the class of claim our leave-group-out
regime shows collapses. It does not make them wrong — but it means **our §4.2
contribution is not a straw man**: the field genuinely makes country-level
attribution claims without prospective validation.

**Handle respectfully.** Their aim was a cheap two-locus assay for laboratories
without WGS, not a prediction system. The right framing is *we tested
prospectively what prior schemes asserted descriptively*, never *they were
careless*.

### 6a.2 A metadata example we should cite verbatim

D reports that **"the four ST-1 strains described as originating from the United
Kingdom are in fact laboratory cultures of the Thai B. pseudomallei strain
K96243."**

That is independent published documentation of the exact failure mode we hit —
deposit location recorded as origin, lab stock counted as a case. It supports
our own metadata curation (11 lab-stock genomes identified; 10 of 21 "USA"
genomes actually Puerto Rico or USVI) and it is a far better citation than
asserting the problem exists.

They also note metadata came **from NCBI BioSample without verification**.

### 6a.3 They acknowledge ST homoplasy; we quantify it

D observes *"several STs populated with strains originating from both Thailand
and Australia"* and cites known ST homoplasy across continents.

**We can extend this from anecdote to measurement:** 52 of 279 STs span more than
one of our units, ST70 spans eight, and ST92 spans four units and seven
countries. Same phenomenon, now with a denominator.

### 6a.4 A methodological point we should make gently

**PBP genes are β-lactam targets and therefore under drug selection.** D does not
address whether antibiotic-exposure patterns — which correlate with geography and
healthcare setting — could drive the SNP patterns used for geographic typing.
Selection also generates convergent evolution, which is homoplasy by another
route.

**This is a reason to prefer core/whole-genome markers over selected loci for
phylogeography**, and it is worth one sentence in our discussion explaining why
we did not build on locus-targeted schemes. Frame as a design rationale, not a
criticism.

### 6a.5 The finding that most needs engaging: H claims country-level origin

**H concludes the aromatherapy-spray *B. pseudomallei* "originated from South
Asia (specifically India)"** — a country-level attribution, from CDC, reached
from a metagenome-assembled genome.

We must not appear to contradict this. **It is a different task from ours:**

| | H (aromatherapy MAG) | ★ ours |
|---|---|---|
| task | attribute **one** strain with corroborating product provenance | **predict** origin for an unknown isolate, blind |
| external evidence | strong — imported consumer product, traceable supply chain | none by design |
| scored against | the known answer | 26 held-out exposures, leave-group-out |
| what failure would look like | conclusion contradicted by the supply chain | measured accuracy |

**Both are legitimate; they answer different questions.** A single attribution
supported by independent epidemiological evidence is a much easier problem than
systematic blind prediction, and our result does not say such attributions are
wrong. **Our claim is narrower and should be stated that way: country-level
attribution does not work *as a general predictive method on this panel*,
particularly for source countries with few or no reference genomes.**

South Asia is a case in point — India has ~56 genomes in our collection, so it is
better represented than Ghana or Nigeria, where our region-level attribution
also failed.

### 6a.6 G is our applied use case, already published

**G is the closest published precedent for what the Mississippi cluster rule is
for**: four melioidosis cases in Georgia, 1983–2024, **no international travel**,
geographically linked, where genomic relatedness supported a **shared exposure**.

That is exactly the operational question our ≤20-SNP cluster rule addresses. We
should cite it as the use case rather than describing the use case abstractly —
and note that **CDC is already making shared-exposure inferences from relatedness
in cases with unknown source**, which is precisely where a calibrated distance
threshold and an honest statement of what cannot be inferred are most useful.

### 6a.7 What to add to our own analysis as a result

1. **Extend the resolution ladder downward.** DLST is a **2-locus** scheme. Adding
   it would give 2 → 7 → 4,089 → whole genome. Cheap, and it strengthens §4.3.
   Note the tension worth reporting neutrally: DLST has *lower* discriminatory
   power than MLST (D = 0.8512; explicitly weaker for Australasia/Asia
   separation), yet reports country-specific STs — while MLST in our hands gives
   0/17 at country level.
2. **Cite D's UK/K96243 example** in the metadata-limitations section.
3. **Cite G** as the applied precedent for the Mississippi operational rule.
4. **Add a sentence distinguishing single-strain attribution with external
   evidence from systematic blind prediction**, citing H. This pre-empts the
   reviewer who says CDC already attributes to country.
5. **One sentence on why we avoided selected loci** (§6a.4).

---

## 7. The two-sentence positioning statement

> Prior work establishes that *B. pseudomallei* carries continental-scale
> phylogeographic signal despite high recombination, and the densest published
> collection reconstructs province-level dispersal within one endemic region
> using partition-then-Gubbins on 1,391 isolates
> ([10.1038/s41467-024-50067-9](https://doi.org/10.1038/s41467-024-50067-9)).
> We apply the same architecture to a globally distributed public collection and
> ask the harder, prospective question — can the origin of an *unknown* isolate be
> predicted — and show, under study-of-origin control and leave-group-out
> validation across three typing resolutions, that regional attribution is
> achievable where reference genomes exist while country-level attribution is
> not.
