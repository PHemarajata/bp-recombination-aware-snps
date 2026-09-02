# Results — draft prose, 2026-08-23

First prose draft of R1–R7, written from `MANUSCRIPT_OUTLINE_2026-08-21.md` on
the frozen basis. **Every figure is annotated with its `NUMBERS.tsv` key** in
`[brackets]` so it can be re-verified without re-reading the code; strip the
annotations before submission. Run `generate_numbers.py` and `freeze_basis_bp.py`
before treating any number here as current.

✅ **Verification status: every figure in this draft is now regenerable on the
frozen basis.** R5, R6 (all three scales) and R7's distances were recomputed
2026-08-23; the rest cite `NUMBERS.tsv` keys. Re-run `generate_numbers.py` and
`freeze_basis_bp.py` before treating any of it as current.

---

## R1. The collection, and the frame it is drawn from

We assembled **2,959** *Burkholderia pseudomallei* genomes `[panel.corrected_v4d]`
spanning **50** countries `[panel.countries]`. The collection is dominated by
three countries: Thailand contributes **1,753 (59.5%)**
`[panel.top_country.Thailand]`, China **295 (10.0%)** and Australia **282
(9.6%)`[panel.top_country.*]`, together **79.0%** of the panel
`[panel.top3_share]`.

To place this in the context of the public record, we re-censused the European
Nucleotide Archive as a union of read-run and assembly depositions — a union
being necessary because a read-run-only query is blind to assembly-only
submissions. ENA holds **9,040** unique *B. pseudomallei* BioSamples
`[ena.biosamples_union]`, of which **7,192** carry a country label
`[ena.biosamples_with_country]` across **56** countries `[ena.countries]`. Our
panel is therefore **41.1%** of the country-labelled public record
`[panel.coverage_of_ena]`. Because **312** of our genomes are in-house isolates
not represented in public archives `[panel.in_house]`, the strictly comparable
figure — public-derived genomes against the public record — is **36.8%**
`[panel.public_derived]`.

**The collection is inverted against the distribution of disease.** Assigning
each of the **2,946** region-labelled genomes `[panel.region_labelled]` to a
World Bank region and comparing with predicted melioidosis burden:

| region | predicted cases/yr | % of burden | genomes | % of labelled | genomes per 1,000 cases |
|---|---|---|---|---|---|
| **South Asia** | 73,000 | **44.2%** | **75** | **2.5%** | **1.0** |
| **East Asia & Pacific** | 65,000 | 39.4% | **2,705** | **91.8%** | **41.6** |
| **Sub-Saharan Africa** | 24,000 | **14.5%** | **30** | **1.0%** | **1.2** |
| Latin America & Caribbean | 2,000 | 1.2% | 79 | 2.7% | 39.5 |
| Middle East & North Africa | <1,000 | 0.3% | 3 | 0.1% | 6.0 |
| Europe & Central Asia | <1,000 | 0.0% | 12 | 0.4% | — |
| North America | <1,000 | 0.0% | 42 | 1.4% | — |
| **Global** | **165,000** | 100% | **2,946** | 100% | 17.9 |

Burden estimates from Limmathurotsakul *et al.* (PMID 26877885). East Asia and
the Pacific is sampled **41× more heavily per predicted case than South Asia**
and **33× more heavily than sub-Saharan Africa**. The region predicted to carry
the largest share of disease contributes 2.5% of the genomes.

> The country label attached to a genome in this collection is not primarily
> measuring where the organism lives. It is measuring where sequencing happened —
> and across the top of the burden distribution the two are inverted.

*Caveat:* roughly 15% of the global public collection is environmental isolates
from a single Thai case–control study, so this compares a clinical-plus-
environmental mixture rather than clinical isolates alone.

After partitioning (Methods §2.12.4–5), **2,340** genomes fall in **85**
recombination-aware analysis units `[genomes.analysed, units.analysed]`, of unit
size 7 to 159 (median 18), spanning 170 replicon-units.

## R2. Exposure country cannot be recovered; region can

We assembled a validation set of **48** genomes with an independently documented
country of *exposure* rather than merely of deposit `[validation.total]`. Two
carry a non-country exposure and are unattributable by construction, leaving
**46 scorable genomes** `[validation.scorable]` drawn from **16 exposure
countries** `[validation.source_countries]`. **Two of the 46 are isolates from a
single patient** sampled five years apart (Brennan *et al.*, PMID 40835221), so
the set represents **45 individuals**; we report this alongside the other
non-independence in the set (§R2.4).

Attribution was scored on core-genome MLST (Lichtenegger scheme, 4,221 loci;
PMID 33980649) so that the result does not depend on the lineage partition, under
a holdout that removes both same-country validation genomes and same-source
outbreak members (Methods §2.12.11a.4).

**Table 1. Attribution accuracy by geographic scale.**

| scale | estimator | correct | accuracy | majority baseline | **κ** |
|---|---|---|---|---|---|
| **country** | nearest neighbour | **10/46** | **21.7%** | **26.1%** | **0.193** |
| country | modal k = 20 | 7/46 | 15.2% | 26.1% | 0.132 |
| sub-national | either | 0/5 | 0% | — | — |
| region (7-way) | nearest neighbour | 37/46 | 80.4% | 45.7% | 0.715 |
| **region (7-way)** | **modal k = 20** | **41/46** | **89.1%** | 45.7% | **0.832** |

`[attribution.country.nearest_neighbour, attribution.region.modal_k20, ladder.*.kappa]`

**Country-level attribution does not exceed chance.** At 21.7% against a 26.1%
majority baseline it is, if anything, below it. Sub-national attribution fails
outright. **Regional attribution succeeds**, reaching 89.1% against a 45.7%
baseline (κ 0.832).

Because the best estimator differs by scale, both are reported with the estimator
named; a nearest-neighbour figure and a modal figure are different analyses and
are never compared with one another.

### R2.1 The failure is not an estimator artefact

Region and country were scored on the same genomes, the same pool and the same
holdout, and differ by three-quarters of a κ unit. Whatever prevents country
attribution is not a property of the estimator.

### R2.2 The apparent country signal under a weaker holdout is entirely circular

Under leave-*one*-out, nearest-neighbour country attribution appears to reach
**29%**. Every one of those hits is a validation genome predicting another
validation genome of the same country, and all of them disappear under
leave-group-out. **Country accuracy quoted with same-country validation genomes
retained is artefactual, not merely optimistic** — and we report the collapse
itself as the result, because it quantifies how much apparent attribution
performance is circularity.

### R2.3 Accuracy depends on whether a relative exists — in opposite directions

| stratum | country (NN) | region (modal k=20) |
|---|---|---|
| d < 0.05 — **a close relative exists** | **2/14** | **14/14** |
| 0.05 ≤ d < 0.30 | 2/10 | 8/10 |
| d ≥ 0.30 — no real relative | 6/22 | 19/22 |

`[attribution.*.d_lt_0.05 etc.]`

**Where a close relative exists — the condition under which attribution should be
easiest — region is perfect (14/14) and country is 2/14.** The same 14 genomes,
the same pool, opposite outcomes at two geographic scales. This is the clearest
statement of the limit: the signal is present at depth and absent at the
shallow end.

The d ≥ 0.30 row should not be read as success. At that distance 30–79% of loci
differ and no meaningful relative exists; nine of those 22 genomes share a single
Ecuadorian nearest neighbour, and because most are Latin American the catch-all
region label scores them correct — while **both sub-Saharan African genomes in
the stratum are confidently assigned to Latin America and scored wrong**. The
estimator is reporting *"unlike the Asian majority of the panel"*.

We tested the obvious alternative explanation, that genomes with fewer callable
loci have inflated distances. It does not hold: across the 46, loci compared
against nearest-neighbour distance gives Spearman ρ = **−0.247** (n.s.), and the
median loci compared is flat across the three strata (4,042 / 4,040 / 4,024).

### R2.4 Non-independence in the validation set, stated three ways

The set is small and structured, and we report this rather than leaving it to be
discovered. (i) The Philippines contributes 12 of 46. (ii) Two of the 46 are one
patient. (iii) 16 of 46 come from a single assembly batch that is 5.9% of the
panel and has the weakest call-rate tail (p05 87.1% vs 95.8%) — though this does
**not** bias the distance strata, as shown above.

## R3. Resolution is not the limiting factor

| layer | loci | country | region |
|---|---|---|---|
| MLST **[MLST/33]** | 7 | **≤ 8/33 (24%)**, baseline 36% | 19/33 (58%), baseline 46% |
| **cgMLST** | **4,221** | **10/46 (22%), baseline 26%** | **41/46 (89%), baseline 46%** |
| core-genome SNP **[SNP/24]** | whole genome | 0/24 | 22/24 (92%) |

Across a **584-fold** span in locus count, country attribution never clears its
baseline. Each row is a different validation set because each typing system
covers different genomes; that is inherent, not an error.

**The MLST country cell is an upper bound, not an accuracy, and the reason is
itself a resolution result.** At seven loci the nearest neighbour is *not unique*
for 30 of the 33 validation genomes — the median tied set is 21 genomes and the
largest is 52 — so the call is settled by an arbitrary tie-break rather than by
the data. The true country appears anywhere in that tied set for only 8 of 33, so
no tie-breaking rule whatever can score above 24%, and an adversarial one scores
zero. **Even an oracle tie-break therefore fails to reach the 36% majority
baseline.** At 4,221 loci the nearest neighbour is unique for every genome. The
MLST bound and the cgMLST point estimate must not be read as like-for-like.

Region, by contrast, is **monotonic in locus count — 58%, 89%, 92%** — over the
same span in which country stays at or below chance. That contrast is the result:
the instrument sharpens, and only one of the two questions responds.

**Randomly subsampling loci provides the positive control.** Sampling *k* loci at
random for *k* = 2 to 4,089, with 10 replicates, country accuracy stays flat at
0–7.3% across the whole range and is **0.0% at the full locus set**, while
regional accuracy rises from **49.5% to 82.1%** against a 48% baseline and
plateaus by roughly 100 loci. The estimator demonstrably converts resolution into
accuracy when the signal is there; the country failure is therefore absence of
signal, not bluntness of instrument.

*Caveat that must travel with this figure:* randomly chosen loci are a lower
bound for a curated scheme. The permitted claim is *"resolution alone does not
buy country-level attribution"*, not *"no targeted scheme can work"*.

### R3.1 The pipeline resolves a finer distinction than country, on the same genomes

The resolution curve shows the estimator converting resolution into accuracy when
signal exists. A second control asks something stronger: give the *same pipeline*
a harder question at a finer scale, and see whether it answers.

Thirteen patients in the Nakhon Phanom collection had culture-confirmed recurrent
melioidosis, giving **20 episode pairs across 29 isolates** `[recurrence.pairs]`.
Distinguishing a relapse of the original infection from a reinfection with a new
strain is the finest epidemiological question these data support, and unlike
exposure country it has a genomic answer that is not in doubt.

**The separation is categorical.** On recombination-filtered SNPs, **19 pairs fall
between 1 and 14 SNPs** and **one pair falls at 1,102** `[recurrence.gap]`. The gap
spans **79-fold with nothing inside it**, so no threshold anywhere between those
values changes a single call. For **16 of the 20 pairs the distances are the
production per-unit Gubbins output itself**, not a separate calculation; the
remaining four required a local analysis because those isolates fall outside the
analysed panel or in different units.

**Tree topology confirms it independently.** Against local context, **12 of the 13
patients form an exclusive clade** containing their own episodes and nothing else,
at **94.4/94 to 100/100** SH-aLRT and ultrafast bootstrap support
`[recurrence.clades]`. The thirteenth is the reinfection: patient 9's two isolates
do not form a clade at all, their common ancestor subtends **35 other genomes**,
and each isolate is closer to another patient's genome (**81 SNPs**) than to its
own previous episode (**1,102**).

**Recombination correction sharpens this contrast rather than blurring it.**
Gubbins removes **44% of SNPs between unrelated genomes but 1 of 9 within a
patient**, so correcting for recombination widens the relapse/reinfection gap. This
is the expected direction in an organism importing roughly eight recombined SNPs
per point mutation, and it is worth stating because the opposite is often assumed.

Seven-locus MLST agrees on all 20 calls but with no margin behind it: this
collection contains **18 pairs of isolates from different patients carrying
byte-identical seven-locus profiles**, so same-ST does not imply same strain here.
The calls survive on MLST only because the true within-patient pairs are another
10 to 20 times closer than the chance ST matches.

*Caveat that must travel with this result:* it establishes that assembly, variant
calling, recombination correction and phylogenetics resolve a within-patient
distinction at single-SNP scale **on these genomes and through this pipeline**, so
the country result is not an instrument failure. It does **not** show that country
is attainable. Relapse-versus-reinfection and exposure-country differ in kind and
not merely in scale: the first asks whether two genomes descend from one infecting
population, which the genome records directly, while the second asks where that
population was acquired, which it records only through a reference panel. One pair
also carries a thin margin worth naming: patient 8's episodes differ by 14 SNPs
against 30 to an environmental isolate from the same collection, so same strain
remains the better explanation but a locally circulating clone is not excluded.

## R4. Why: the panel does not contain the source countries

**For 7 of the 16 exposure countries in our validation set, no public genome
exists in ENA at all** — Aruba, Costa Rica, El Salvador, Guatemala, Martinique,
Nicaragua and Trinidad and Tobago. **All seven are in Latin America and the
Caribbean.** The gap is not scattered across the tropics; it is one region.

Two countries that might be assumed absent are not. **Mexico has 21 public
genomes** and the **Philippines has 1** — so the claim that we hold the only
genomes in existence is false for Mexico and marginal for the Philippines.

**Mexico is also the case that proves absence is not the whole mechanism.** Three
Mexican-exposure genomes retained genuine same-country references under
leave-group-out — three in a thirty-genome pool — and attribution still failed.
Absence of references explains most of the failure; Mexico shows it is not all
of it.

**The same gap at species scale.** Against the ENA union census, **21 countries
with ≥100 predicted cases per year have zero public genomes**, together
**8,939 cases/year, about 5% of the global estimate**. **Nineteen of the 21 are
sub-Saharan African** (the exceptions are Nepal and El Salvador). Read with R1's
burden table — sub-Saharan Africa at 14.5% of predicted burden and 1.0% of the
panel — the argument closes: country attribution fails for our validation cases
because their source countries have no reference genomes, and that is not a
peculiarity of our 16 countries but the shape of the entire public collection
relative to where the disease is.

## R5. Independent typing systems fail in the same places

Seven-locus sequence types were called for all analysed genomes and compared with
the recombination-aware partition. **All counts below are over the 2,340 analysed
genomes and were recomputed on the frozen basis 2026-08-23**, taking unit
membership from `FINAL_PARTITION.tsv`.

- **ST92 spans seven countries and three distinct lineages.** Thirty-five
  analysed genomes carry ST92 — USA 25, Brazil 3, Mexico 3, Colombia 1,
  Nicaragua 1, Guadeloupe 1, Martinique 1 — distributed across **three separate
  analysis units** (`strain_4_L1_1` n=22, `strain_4_L1_4` n=9, `strain_4_L1_3`
  n=4). A single sequence type therefore covers the entire region of applied
  interest while resolving into three lineages that the whole-genome partition
  keeps apart. *(Across the full 2,959-genome panel the ST92 count is 36, with
  USA 26; the seven countries are unchanged.)*
- **ST58 spans five countries** — China 25, Thailand 20, Philippines 9, Cambodia
  1, Taiwan 1 (n = 56) — and is the sequence type of most Philippine validation
  genomes.
- **Homoplasy is systemic.** Of the **278** sequence types present in the
  analysed set, **52 (19%) span more than one analysis unit**, and **ST70 spans
  eight**.
- cgMLST allelic distance and recombination-filtered SNP distance agree closely:
  **median Pearson r = +0.861** across the 85 frozen units, with **66 of 85** at
  r ≥ 0.7 (`CGMLST_CONCORDANCE_FROZEN.tsv`, restricted to the Lichtenegger
  scheme).

Prior work established that 7-locus MLST lacks the resolution to pin geographic
origin, and that sequence types shared between continents reflect homoplasy
rather than descent (De Smet *et al.*, PMID 25392354). **The novel half is that
whole-genome, recombination-corrected clustering does not rescue it.** Notably,
that same study found whole-genome analysis *did* correctly identify Asian versus
Australian origin — an independent instance of the depth ceiling we report.

## R6. Where geographic signal exists, and where it is indistinguishable from study of origin

Fitch parsimony of geographic labels on each unit's recombination-corrected
topology against a null of 1,000 label permutations across the tips of the same
tree, with **BioProject tested identically on the same trees** as a companion
control. **Re-run at all three scales on the reported 85-unit basis, 2026-08-23**
(`PHYLOGEO_FROZEN_{subnational,national,regional}_2026-08-23.tsv`, seed 20260823).
Only the label column changes between scales.

| scale | labels | testable units | clustered p ≤ 0.05 | survives FDR | **passes the BioProject control** |
|---|---|---|---|---|---|
| sub-national | `country :: subregion` | 81 | 16 | 10 | **1** |
| national | country | 48 | 26 | 23 | **6** |
| regional | World Bank region | 17 | 4 | 3 | **1** |

Populated-label fractions are 79.6%, 99.8% and 99.8% respectively.

**How much can even be asked differs enormously by scale, and that is a sampling
fact rather than a biological one.** At regional scale **68 of 85 units contain a
single region** and no test can run on them, because 91.8% of the panel is East
Asia & Pacific. At national scale 37 units are single-country.

**The BioProject control does the decisive work.** At national scale it removes
**12 units as confounded** — country and BioProject equally significant — plus 5
where the control could not run, cutting 23 FDR survivors to 6.

**The discarded set is graded, not flat** (adopted 2026-08-26 from
`BIOPROJECT_WITHIN_COUNTRY_RESULT_2026-08-24.md` §5). "Confounded" is the
automatic verdict whenever a within-country clonal expansion was deposited by one
study, because 95% of BioProjects here are single-country and ~99% of
same-BioProject near-clonal pairs are also same-country. Testing the study-effect
explanation directly, conditional on country, splits the discarded units three
ways:

| verdict | n |
|---|---|
| confounded, batch structure **confirmed** within country | 8 nominal, of which **2 survive FDR** |
| not separable, **no batch structure detected**, geography unproven | 4 |
| not separable, untestable | 2 |

Batch structure is real in aggregate (8 of 22 testable cells at p ≤ 0.05 against
1.1 expected, binomial P = 6.6 × 10⁻⁶) but is FDR-confirmed in only two units,
both Thailand. So for at least a third of the discarded set the artefact
explanation was tested and **not** found; describing them as artefact overstates
what the control established. **No headline moves**: every reported R6 count is a
*pass*, and no pass changes.

> **On 12 versus 14** (reconciled 2026-08-26 from
> `PHYLOGEO_FROZEN_national_2026-08-23.tsv`; both are the frozen 85-unit basis and
> neither is stale). Of the 23 country-clustered FDR survivors, **14 have
> BioProject also clustered**, and the R6 conditional-test document counts all 14
> as confounded. This paragraph counts **12**, because it files two of them,
> `strain_1_L1_35` and `strain_3_L1_6`, under "the control could not run" instead:
> their BioProject control is `vacuous` in the frozen table. The five vacuous
> units are therefore not disjoint from the confounded ones, two of them are the
> same units seen from the other side. Both descriptions partition the same 23
> (12 + 5 + 6 = 23; equivalently 14 + 3 + 6). Keep one convention per document and
> say which. Note the R6 document's own "untestable" pair
> (`strain_1_L1_17`, `strain_3_L1_6`) is a **third**, unrelated criterion (no
> testable (unit, country) cell at ≥ 8 genomes and ≥ 2 BioProjects) and overlaps
> this one only at `strain_3_L1_6`.

**The six national-scale passes are all dominated by Southeast and East Asian
countries**: `strain_5_L1_3` (Thailand 35 / Laos 6), `strain_1_L1_5` (Singapore
10 / France 5 / Malaysia 2), `strain_11_L1_5` (Thailand 37 / Cambodia 3),
`strain_2_L1_2` (Thailand 72 / Laos 2), `strain_1_L1_28` (Thailand 53 / China 2)
and `strain_1_L1_11` (China 8 / Thailand 8 / Laos 3). *(`strain_1_L1_5` carries a
substantial French component and should not be described as purely Southeast
Asian; it is also the single unit that passes at regional scale, where the
Singapore/Malaysia-versus-France split is genuinely inter-regional.)*

**Every Americas-dominated unit fails**, by three distinct routes: the Mississippi
Gulf Coast unit `strain_4_L1_1` is **null at p = 1.0000**, `strain_4_L1_2` is null
at p = 0.068, `strain_4_L1_3` has a vacuous control, and `strain_4_L1_4` and
`strain_1_L1_7` are **confounded** at p = 0.0010, country and BioProject equally
significant. The conditional test separates these last two, and they should not be
described together: `strain_4_L1_4` does carry within-country batch structure
(USA, 13 genomes across 4 BioProjects, p = 0.0450), so for it "confounded" is
supported. `strain_1_L1_7` does **not**: its only testable cell is Singapore at
p = 0.0569, and it is one of the four units where the study-effect explanation was
tested and not found. It is better described as *not separable* than as a
well-powered negative. The
Viet Nam/Georgia unit `strain_22_L1_1` is **null (p = 0.0430, not surviving
FDR)**, consistent with the one-locus boundary in R7.2.

### Sub-national signal is very nearly absent, but not quite zero

⚠ **This corrects an earlier claim.** On the previous 88-unit basis the
sub-national scale returned **0 of 83** units passing the control, and the
generalisation "sub-national geography is indistinguishable from study of origin"
was written on that. On the reported basis **1 of 81 passes**, and the claim must
be stated as *very nearly* absent rather than absent.

The single unit is `strain_1_L1_33` (n = 27, 24 labelled, 6 distinct sub-national
labels, p = 0.0060). Three things should be said with it. It is **dominated by one
Thai province** — Ubon Ratchathani, 16 of 24 — which is among the most intensively
sampled melioidosis sites in the world. Its **q = 0.0486 only barely survives**
FDR correction at 5%. And it is **1 unit in 81**.

The honest statement is therefore: **sub-national geography is indistinguishable
from study of origin in 80 of 81 testable units**, and the single exception is a
marginal result in the most heavily sampled province in the collection. A label
such as `Thailand :: Nakhon Phanom` is very nearly the name of a collection
effort — but "very nearly" is doing real work in that sentence and we should not
round it to zero.

## R7. What is operationally usable: two US autochthonous foci

Attribution of *origin* fails, but *cluster membership* is callable, and the two
questions should not be conflated.

### R7.1 The Gulf Coast cluster

Unit `strain_4_L1_1` (n = 22) contains the Mississippi Gulf Coast lineage
(Petras *et al.*, PMID 38118023). Distances verified against
`DISTANCES_v4c_SUMMARY.tsv` restricted to the frozen basis, 2026-08-23.

| | chromosome 1 | chromosome 2 |
|---|---|---|
| internal median, raw / filtered | 8 / **5** | 5 / **4** |
| maximum to the nearest outside genome, raw / filtered | 1,136 / **492** | 1,432 / **528** |

**A new US case within roughly 20 SNPs is this lineage; one 500 SNPs away is not.
The call is never borderline.** The same data bound what cannot be said: because
the nearest genome outside the cluster is ~490 filtered SNPs away, **the origin
of the lineage cannot be stated**. The Colombian genome is *the nearest relative
in this panel*, not *a near relative*.

### R7.2 A second focus, in Georgia — and the sharpest limit in the study

A second unit contains five genomes from four patients in Georgia, USA, spanning
**1983–2024**, reported as presumptive autochthonous cases with no recent
international travel (Brennan *et al.*, PMID 40835221). The same unit holds two
isolates from one Viet Nam-exposure patient and three isolates collected in Viet
Nam from two independent studies. **The lineage is genuinely present on both
sides of the Pacific**, and the published investigation leaves open that the
Georgia environmental focus itself may derive from Vietnam-War-era introduction.

**This is the condition under which attribution should work — both countries
represented, by independent studies, with published epidemiology on both sides —
and it still fails.**

| | cgMLST allelic distance |
|---|---|
| Georgia cluster, internal maximum | **8.67 × 10⁻³** |
| nearest non-Georgia genome in all 3,033 (a Viet Nam-exposure case) | **8.91 × 10⁻³** |
| **separation** | **0.25 × 10⁻³ = 1.0 locus of 4,221** |

A published US autochthonous cluster and a documented Viet Nam-acquired infection
are separated by **one locus** more than the cluster's own internal spread. No
distance threshold places them on opposite sides reliably.

The estimator behaves accordingly, and instructively. For both Viet Nam-exposure
isolates, **nearest neighbour is wrong at every scale** — including the deep
Asia/non-Asia split — because their closest relative in 3,033 genomes is a
Georgia case; **modal k = 20 recovers both**. They are **2 of only 3 errors the
deep split makes under nearest neighbour** (43/46, κ 0.869), and modal k = 20 is
**46/46, κ 1.000**.

This is not a BioProject artefact: the Georgia and Viet Nam-exposure genomes
share a BioProject, and within that single project distances to the Georgia
cluster span 8.91 to 16.47 × 10⁻³.

*Context for every distance in this paper:* across the 170 replicon-units the
median filtered-to-raw distance ratio is **0.090** — roughly **91% of raw
pairwise distance is imported DNA rather than inherited mutation**. A distance
quoted without saying which kind it is means very little.

## R8. What does work: a ladder of claims, and knowing when to abstain

Coarsening the geographic question until it becomes answerable locates the
ceiling precisely (modal k = 20 throughout):

| grouping | classes | accuracy | baseline | **κ** |
|---|---|---|---|---|
| **Asia vs non-Asia** | 2 | **100%** | 58.7% | **1.000** |
| Eastern vs Western hemisphere | 2 | 95.7% | 63.0% | **0.909** |
| region, 7-way | 5 present | 89.1% | 45.7% | **0.832** |
| SEA vs non-SEA | 2 | 76.1% | 58.7% | 0.461 |
| country | 16 | 21.7% | 26.1% | **0.193** |

`[ladder.*.kappa]`

**The deep splits are recovered without error and the shallow ones are not** — on
the same genomes, the same pool and the same holdout. The limit is depth of
signal, not volume of data.

Because the estimator answers confidently even when no relative exists, we pair
it with an **abstention rule**: where no genome lies closer than **0.462**
allelic distance, return *unattributable* rather than a region. Reported
out-of-sample, with the threshold selected on the other 45 genomes and applied to
the held-out one:

| | coverage | selective accuracy |
|---|---|---|
| in-sample | 78.3% | 94.4% |
| **leave-one-out** | **76.1%** | **94.3%** |

`[abstention.region.*]`

The rule declines **3 of the 5 region errors, including both sub-Saharan African
misassignments**, at a cost of 7 correct answers. Two caveats belong with it.
First, **the retained-subset majority baseline also rises** (45.7% → 50.0%), so
lift over chance improves only from +43.4 to +44.4 points: **the value is in
which errors remain, not in the accuracy number.** Second, the rule **cannot**
decline errors of the Georgia type, which have genuine close relatives and high
neighbourhood agreement — **two distinct failure modes, of which this addresses
one.**

**The same rule fails at country scale, and we report that as a result.** Its
best operating point reaches 37.5% selective accuracy against an answer-everything
21.7% — but the **retained-subset majority baseline is also exactly 37.5%**. On
the half of cases it elects to answer, always guessing the commonest exposure
country scores identically. **Country attribution is not rescued by abstaining.**

### R8.1 The same shape of result in another organism

An independent hierarchical machine-learning study of *Salmonella enterica*
serovar Enteritidis (Bayliss *et al.*, PMID 37042517) attributed 2,313 genomes to
four continents, eleven sub-regions and 38 countries using unitig features, and
reports macro F1 of **0.954, 0.718 and 0.661** at those three levels. **The decay
with geographic depth is the same shape we report** — near-perfect at the deepest
split, degrading monotonically as the question narrows — and those authors
attribute the country-level shortfall to the same mechanism, noting *"a
correlation between a lack of training data and lower prediction accuracy"*.

Two differences explain why they retain usable country signal where we do not,
and both are consistent with our thesis rather than in tension with it. First,
*S.* Enteritidis is comparatively clonal and geographically structured, whereas
*B. pseudomallei* is environmentally acquired, recombinogenic (in-window r/m
7.70) and carries lineages that span continents — ST92 across seven Americas
countries, and the Viet Nam/Georgia lineage separated by a single locus (R7.2).
Second, their classes are countries commonly visited by UK travellers and are
correspondingly well referenced, whereas **7 of our 16 validation source
countries have no public genome at all** (R4).

Their evaluation also used a **country-stratified random 75:25 split**, which
does not separate near-identical genomes of the same lineage between training and
test. Our own country attribution reaches 29–37% under an equivalent
leave-one-out design and falls below baseline only under leave-group-out (R2.2) —
so the two results are not necessarily in conflict, and the comparison is best
read as **the same curve sampled at two different points**.

A subsequent deep-learning method reports higher figures on the same benchmark
(91.9 / 87.1 / 80.8% at region, subregion and country; Liang *et al.*, PMID
41185308). Two things make that number not directly comparable with either
Bayliss's or ours: it is an **accuracy** rather than a macro-averaged F1, which on
38 imbalanced classes weights the well-sampled classes heavily; and **in the
released reference implementation the test path is set to the validation path,
with the reported checkpoint chosen by maximising accuracy on that same set.**
The hierarchical decay with geographic depth is nonetheless preserved in their
results too.

The deployable statement is therefore a ladder, not an answer: *Asia or not —
certain. Region — where a relative exists, and the method says when one does not.
Country — no.*
