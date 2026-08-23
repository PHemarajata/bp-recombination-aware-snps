# Manuscript outline — the genomics paper

Drafted 2026-08-21 from a full re-read of the 62-document corpus plus direct
recomputation from the result tables. Every number below was either verified
against the primary TSV or is cited to the document that owns it.

> ## ⚑ FIGURE PROVENANCE KEY — read before quoting any attribution number
>
> **Reconciled 2026-08-23.** The outline reports **five distinct attribution
> analyses**, each on its own validation set and typing system. They are NOT one
> number at different times; do not find-replace across them. Every attribution
> figure below is tagged with one of these codes:
>
> | code | typing system | validation n | country | region | source |
> |---|---|---|---|---|---|
> | **[SNP/24]** | core-genome SNP, unit-based | 24 | 0/24 (LGO) | 22/24 = 92% (modal), 67% (NN); baseline 54% | `ATTRIBUTION_SCORES.tsv` |
> | **[MLST/17]** | 7-locus MLST | 17 | 0/17 | 13/15 = 87% | typing-resolution table (§4) |
> | **[cg-Pub/29]** | cgMLST, PubMLST scheme (4,089 loci) | 29–30 | 0/30 | 23/29 = 79% | superseded by cg-Licht |
> | **[REScurve]** | cgMLST subsampled k loci | travel-reattributed set | flat 0 | 49.5% → 82.1%; baseline 48% | `RESOLUTION_CURVE_RESULT` |
> | **[cg-Licht/46]** ← **CURRENT HEADLINE** | cgMLST, Lichtenegger (4,221 loci) | **46** | **NN 10/46 = 22%; modal-k20 7/46 = 15%; close-relative 2/14** | **modal-k20 41/46 = 89%, κ 0.832; NN 37/46 = 80%; baseline 46%** | `NUMBERS.tsv`, `CGMLST_LICHT_ATTRIBUTION.tsv` (NN), `GROUPING_LADDER.tsv` (modal + κ) |
>
> **Ladder (cg-Licht/46, κ):** Asia/non-Asia 1.000, East/West hemisphere 0.909,
> region 7-way 0.832, SEA/non-SEA 0.461, country 0.132 (modal) / 0.193 (NN).
> North America is now testable — the Mississippi autochthonous strain (US origin
> certain) misattributes to Latin America. `TRACK0_INTEGRATION_2026-08-23.md`.
>
> ### ⚠ The estimator is part of the number — added 2026-08-23
>
> **Country's best estimator is nearest neighbour; region's is modal k=20.** They
> are different analyses of the same data and must never be mixed within a row:
>
> - Region, **modal k=20 → 41/46 (89%)**. This is the headline.
> - Region, **NN → 37/46 (80%)**. A *different estimator*, not a correction.
> - Every stratification must use **its own headline's estimator.** The region
>   strata under modal k=20 are **14/14 · 8/10 · 19/22**; under NN they are
>   11/14 · 6/10 · 20/22. W2 below previously carried the NN strata beside the
>   modal headline.
>
> `CGMLST_LICHT_ATTRIBUTION.tsv` stores **only nearest neighbour** — the scorer
> persists one estimator per run. Modal and κ figures come from
> `GROUPING_LADDER.tsv` / `GROUPING_PREDICTIONS.tsv`. All of it is surfaced in
> `NUMBERS.tsv` with the estimator in the key
> (`attribution.region.modal_k20`, `ladder.*.kappa`). **Cite the key, not the
> file**, and run `generate_numbers.py` first.
>
> **The scheme citation, verified 2026-08-23:** the headline scheme is
> **Lichtenegger S, et al. *J Clin Microbiol* 2021;59(8):e0009321, PMID 33980649,
> doi:10.1128/JCM.00093-21** — abstract confirms **4,221 core targets**, matching
> ours exactly. ⚠ **§6.5 below says to remove the Lichtenegger citation. That
> instruction is now inverted** and applies only to the superseded cg-Pub run.
>
> **The paper must pick ONE cgMLST analysis as the headline** — cg-Licht/46 (it is
> the published scheme, the largest validation set, and the only one with North
> America). cg-Pub/29 and the intermediate n=24/43 cgMLST runs are superseded and
> should be dropped from the manuscript, kept only as robustness/scheme-swap
> support. [SNP/24], [MLST/17] and [REScurve] are genuinely separate analyses and
> stay, each tagged.

**Read §1 first. It is the only part that is a decision rather than a finding.**

---

## 1. The decision that has to come first

The corpus contains **four candidate papers**, not one. The reason this project
feels like "chasing stars between chats" is not scientific drift — it is that
the deliverable was chosen once, on 2026-08-09, and never revisited while the
work moved twice.

| | candidate | evidence state |
|---|---|---|
| **A** | *What the public* B. pseudomallei *collection can and cannot support* — a limits paper | in hand |
| **B** | *Recombination-aware subtree merging* — a methods paper | **not started**; needs SimBac benchmark |
| **C** | *The operating envelope of Gubbins-based r/m estimation* — what the 40-section calibration programme actually produced | in hand, unwritten |
| **D** | *Rapid origin-of-exposure attribution for melioidosis* — a public-health capability paper | in hand |

`REVISED_STRATEGY_2026-08.md` §0 chose **A first, B later**, gave three good
reasons, and was then never amended across 3,500 further lines — even as the
work became C (the calibration programme) and then D (attribution).

**Recommendation: write one paper that is A and D fused, and a second that is C.**

A and D are not two papers. **The limit *is* the capability statement.** "You
can get the region, you cannot get the country, and here is exactly why" is
simultaneously the limits result and the operational guidance. Splitting them
would leave A without a purpose and D without its central caveat.

C is a genuinely separate paper with a different reviewer pool, and it is the
one that is currently invisible. B stays deferred.

**The reassuring part, and it is worth saying plainly:** §1.3, written on
2026-08-09 from literature alone, predicted *"continental-level strain origin is
well supported; dated, directional, between-country migration inference is
not."* Twelve days of measurement and nine of attribution work produced exactly
that, empirically. **The science did not drift. The deliverable did.**

---

## 2. The story spine (Paper 1)

> Melioidosis is diagnosed in travellers and in newly-endemic areas where the
> exposure location is unknown, and clinicians and public-health agencies ask
> genomics to supply it. Across 2,955 *B. pseudomallei* genomes we show that
> **exposure country cannot be recovered from the genome at any resolution**
> — 7 loci, 4,221 loci, and whole-genome recombination-filtered SNPs all return
> at or below chance — while **region is recoverable**, and that the boundary
> between the two is set not by genomic resolution but by **which countries have
> public reference genomes at all**. For 7 of 16 source countries in our
> validation set, no public genome exists in ENA at all. The limit is a
> surveillance gap, not a technical one.

The logic chain, each link independently evidenced. **This chain is written on
the earlier [SNP/24] analysis; recast it on [cg-Licht/46] for the paper — country
10/46 = 22% (a hair above a 26% baseline, and 2/14 where a close relative exists),
region 89%. The conclusion is identical and stronger (North America now included);
only the numbers update.**

1. Country attribution fails. **0/24 [SNP/24]** / **10/46, and 2/14 where a close
   relative exists [cg-Licht/46]** under leave-group-out.
2. It is not our estimator: **region works, 22/24 = 92% [SNP/24]** / **89%
   [cg-Licht/46]**, same data, same estimator, same holdout.
3. It is not resolution: across a **584-fold** span in locus count, country never
   exceeds chance — **0/17 [MLST/17], 0/24 [SNP/24], and 10/46 = 22% against a
   26% baseline at 4,221 loci [cg-Licht/46]**; a resolution curve over a
   **2,000-fold** range holds country flat while region climbs **49.5% → 82.1%
   [REScurve]**.
4. It is not the lineage partition: the same result appears under two
   **partition-free** methods (7-locus MLST [MLST/17], cgMLST nearest-neighbour
   [cg-Licht/46]).
5. It is not fixable by sequencing more of what we already have: the failure
   tracks **absence of reference genomes for the source country**.
6. Independent confirmation from the organism itself: **ST92 spans seven
   countries** across the Americas — a single sequence type covering the entire
   region of applied interest.
7. What *does* work operationally: the **Gulf Coast cluster** is clonal at
   outbreak resolution (median 5 filtered SNPs internally, ≥486 to anything
   outside), so cluster membership is callable even where geography is not.

---

## 3. Results outline

### R1 — The panel, and the frame it is drawn from

**Table 1.** Panel composition, on the **corrected v4d panel of 2,955** (2,976
less 17 duplicate BioSamples and 4 register exclusions — `panel.corrected_v4d`).
**50 countries.** Thailand **1,753 (59.5%)**, China **295 (10.0%)**, Australia
**282 (9.6%)** — top three = **79.1%**. Three BioProjects = **46.4%** of the panel.

⚠ **Quote 2,955, not 2,976.** The uncorrected figure and every percentage
computed on it (58.9 / 9.9 / 9.5 / 78.3%) are superseded.

**Table 2.** Coverage of the public universe, **re-censused 2026-08-21 as a
union of `read_run` and `assembly`** (`GENOME_REGISTER` §2). ENA holds 9,623 read
runs and 3,546 assemblies over **9,040 unique BioSamples, 7,192 with a country**,
across 56 countries. **Our panel is 41.1% of those** (`panel.coverage_of_ena`).

⚠ **Quote 41.1%, not 44% and not 41.4%.** The 44% figure used a reads-only
denominator (6,707), which is blind to assembly-only depositions — the same error
that produced the Mexico mistake in R4; 41.4% was computed on the uncorrected
2,976. Both remaining figures are also slight over-statements, since 312 panel
genomes (10.6%) are in-house and not public at all; against the public-derived
**2,643** the figure is **36.7%**.

Not proportional: Australia under-represented **2.5×**, Cambodia **5×**, China
over **3.5×**.

**Table 3 — genomes against predicted disease burden. This is the strongest
version of the sampling argument and it needs no model.**

Burden from Limmathurotsakul et al. 2016 (*Nat Microbiol* 1:15008, PMID
26877885), Table 1; genome counts are our 2,959 region-labelled panel members.
**Recomputed 2026-08-21 against the current panel — see the warning below.**

| region | cases/yr | % burden | genomes | % of panel | genomes per 1k cases |
|---|---|---|---|---|---|
| **South Asia** | 73k | **44.2%** | **75** | **2.5%** | **1.0** |
| **East Asia & Pacific** | 65k | 39.4% | **2,717** | **91.8%** | **41.8** |
| **Sub-Saharan Africa** | 24k | **14.5%** | **30** | **1.0%** | **1.2** |
| Latin America & Caribbean | 2k | 1.2% | 79 | 2.7% | 39.5 |
| Middle East & North Africa | <1k | 0.3% | 3 | 0.1% | 6.0 |
| Europe & Central Asia | <1k | 0.0% | 12 | 0.4% | — |
| North America | <1k | 0.0% | 43 | 1.5% | — |
| **Global** | **165k** | 100% | **2,959** | 100% | 17.9 |

**East Asia & Pacific is sampled 41× more heavily per predicted case than South
Asia, and 33× more heavily than Sub-Saharan Africa.** The region predicted to
carry the largest share of disease contributes 2.5% of the genomes.

> *The country label in this collection is not measuring where the organism is.
> It is measuring where sequencing happened — and across the top of the burden
> distribution the two are inverted.*

This is the honesty anchor, and it costs nothing because the disproportion **is**
the finding. It also generalises the validation-set result in R4 from our 16
source countries to the whole species.

*Caveat to state:* roughly 15% of the global public collection is environmental
isolates from a single Thai case–control study, so this is a
clinical-plus-environmental comparison.

⚠ **Do not reuse the older regional figures.** A version of this table computed
on the 2026-08-09 NCBI census (5,515 genomes) gives 2.9% / 93.5% / 0.3% and a
36× ratio. Those are superseded and should not appear alongside these. Pick one
census and say which.

### R2 — Country attribution fails; region succeeds

**Table 4 (headline). [cg-Licht/46]** — cgMLST nearest-neighbour and modal k=20,
leave-group-out **and leave-outbreak-out**. This is the paper's headline table.

| scale | scorable | modal k=20 | nearest-neighbour | majority baseline | κ (best est.) |
|---|---|---|---|---|---|
| **country** | 46 | 7/46 (15%) | **10/46 (22%)** | **26%** | **0.193** (NN) |
| sub-national | 5 | **0%** | 0% | 0% | — |
| **region (7-way)** | 46 | **41/46 (89%)** | 37/46 (80%) | **46%** | **0.832** (modal) |

**Report the best estimator per scale and say which** — country NN, region modal.
Country's 22% sits *below* its own 26% baseline; the honest sentence is "country
attribution does not exceed chance," not "country attribution reaches 22%."

**Table 4b (core-genome cross-check). [SNP/24]** — the original unit-based result,
retained as an independent-typing-system confirmation, **not** as the headline:

| scale | scorable | modal | nearest-neighbour | majority baseline |
|---|---|---|---|---|
| country [SNP/24] | 24 | **0%** | **0%** | 0% |
| sub-national | 5 | **0%** | 0% | 0% |
| region [SNP/24] | 24 | **92%** | 67% | **54%** |

**The single most important methodological point in the paper.** Under
leave-*one*-out, country nearest-neighbour scores **29% (7/24)**. Under
leave-*group*-out it is **0/24**. All seven hits were validation genomes
predicting each other. **Never quote a leave-one-out country number**; report
the collapse itself as the result, because it quantifies how much apparent
attribution performance is circularity.

### R3 — Resolution is not the limiting factor

**Table 5.** The 584-fold ladder — country is zero at every rung:

| layer | loci | country | region |
|---|---|---|---|
| MLST **[MLST/17]** | 7 | 0/17 | 13/15 (87%) |
| **cgMLST [cg-Licht/46]** ← **use this row** | **4,221** | **10/46 (22%), baseline 26%** | **41/46 (89%), baseline 46%** |
| core-genome SNP **[SNP/24]** | whole genome | 0/24 | 22/24 (92%) |

⚠ **The [cg-Pub/29] row (4,089 loci, country 0/30, region 23/29 = 79%) is
superseded and comes out of the manuscript body.** Keep it only in the
supplement as the scheme-swap robustness check — the two schemes agree (region
93% under both at the time of the swap, cgMLST↔SNP r = 0.999), so it evidences
*scheme-independence* and nothing else.

*(Each row is a different validation set because each typing system covers
different genomes — that is inherent, not an error. The MLST row predates the
31-genome correction and is due a re-run — see §6. Note the ladder is no longer
"0 at every rung": at 4,221 loci country reaches 22% against a 26% baseline,
which is still **at or below chance** — state it that way rather than as a bare
zero, because the bare zero is now only true of the smaller [SNP/24] and
[MLST/17] sets.)*

**Figure 2. [REScurve].** The resolution curve. k loci sampled at random,
k = 2 → 4,089, 10 replicates, on the travel-reattributed validation set (**not
the cg-Licht/46 set** — the Track 0 additions are not in it, so this figure is
unchanged). Country flat at 0–7.3% across the whole range and **0.0% at the
full 4,089**; region rises **49.5% → 82.1%** against a 48% baseline and
plateaus by ~100 loci.

This figure is the paper's **built-in positive control**: the estimator
demonstrably *can* convert resolution into accuracy, so the country failure is
absence of signal, not bluntness of instrument.

**Caveat that must travel with it:** random loci are a *lower bound* for a
curated scheme. The published PBP dual-locus scheme chose its loci *because*
they carried geographic signal. The permitted claim is *"resolution alone does
not buy country-level attribution"* — not *"no two-locus scheme can work."*

### R4 — Why: the panel does not contain the source countries

**Table 6.** ⚠ **Corrected 2026-08-21 — see `GENOME_REGISTER_2026-08-21.md` §4.**
The previously circulated *"9 of 16 source countries have zero public genomes"*
was computed from a **read-run-only** ENA query, which is blind to
assembly-only depositions. Re-run as a union of `read_run` and `assembly`:

> **7 of 16 source countries have no public genome in ENA — Aruba, Costa Rica,
> El Salvador, Guatemala, Martinique, Nicaragua, and Trinidad and Tobago. All
> seven are Latin America & Caribbean.**

That is a **sharper** finding than the old one: the gap is not scattered across
the tropics, it is one region.

⚠ **Denominator updated 2026-08-23: 16, not 15.** Recomputed on the n=46
validation set — Track 0 added USA as a source country. The seven zero-genome
countries are **unchanged**, and so is the all-one-region finding; only the
denominator moves. Do not quote "7 of 15" or the old "9 of 16 / 44%".

**Two countries move out of the zero column, and this matters:**
**Mexico has 21 public genomes** (all assembly-only, 16 from the recent
`PRJNA1131791`) and **the Philippines has 1**. The claim *"we hold the only ones
in existence"* was true of the Philippines when written and is now marginal; for
Mexico it was never true. **Do not repeat it for Mexico.**

The finding survives the correction, because Mexico is the case that proves the
mechanism is not simply absence: **three Mexican genomes retained genuine
same-country references under leave-group-out — 3 in a 30-genome pool — and
attribution still failed.** Absence of references explains most of the failure;
Mexico shows it is not the whole of it.

**The reach-limit appears at three levels, and they are the same phenomenon:**

1. **Country** — fails outright where no same-country reference exists.
2. **Region** — the four cgMLST region misses are Ghana and Nigeria (panel holds
   30 Sub-Saharan African genomes) and two Guatemalan genomes dragged to a
   single Czech genome. *"Region attribution works"* must be qualified to
   *"region attribution works where the panel has reference genomes for that
   region."*
3. **Unattributable at all** — **[SNP/31] 6 of 31** validation genomes sit alone in
   singleton units with no pool. Their exposure countries are Mexico, Ghana,
   Nigeria, El Salvador, Philippines, and one *ex Africa*. **Four are the sole
   panel representative of their exposure country.**

That third level is worth its own paragraph in the Discussion: in operational
use this is a **19% no-answer rate, concentrated in exactly the cases that
prompt the question.**

⚠ **Scope this claim to the SNP/unit analysis.** "Sits alone in a singleton unit
with no pool" is a *partition* failure mode, and the headline [cg-Licht/46]
analysis is **partition-free** — cgMLST nearest-neighbour always has a pool, so it
returns an answer for 46 of 48, the 2 exclusions being non-country exposures
rather than missing pools. The right framing is therefore **not** "19% get no
answer" but the sharper W2 point: the partition-free method *always answers*, and
above d ≥ 0.30 that answer is an attractor artifact. That is what motivates the
abstention rule (D3) — a deliberate no-answer is better than a confident wrong
one. Recompute the 6/31 on the current basis before quoting it, or drop it in
favour of the distance stratification.

**And the same gap, at species scale.** R1's Table 3 shows it by region; the
country-level version closes the argument. Computed against the **current ENA
union census** (`GENOME_REGISTER` §5): **21 countries with ≥100 predicted
cases/year have zero public genomes**, together **8,939 cases/year — 5% of the
global estimate.**

**19 of those 21 are sub-Saharan African** (the exceptions are Nepal and El
Salvador). Largest: Guinea 1,372/yr, Côte d'Ivoire 1,144, Benin 919, Nepal 914,
Sierra Leone 600.

That pairs exactly with the regional table — **sub-Saharan Africa, 14.5% of
predicted burden and 1.0% of the panel** — and gives the paper a single, clean
statement of where the remaining hole is.

**Read Tables 3 and 6 together and the claim is complete:** country attribution
fails for our validation cases because their source countries have no reference
genomes, and that is not a peculiarity of our 16 countries — it is the shape of
the entire public collection relative to where the disease actually is.

⚠ **The widely-cited internal figure is wrong. Do not quote it.**

`GAP4` records ***"29 countries with >100 cases/yr have zero genomes, totalling
54,076 cases/yr = 33% of global burden."*** It was computed on the superseded
2026-08-09 NCBI census. Recomputed twice:

| | `GAP4`, 2026-08-09 NCBI | v4c panel | **ENA union, 2026-08-21** |
|---|---|---|---|
| countries ≥100 cases/yr, zero genomes | 29 | 24 | **21** |
| their share of global burden | **33%** | 7% | **5%** |

**Use the ENA column — it is the right denominator for a claim about the public
record.** The 33% collapsed because Indonesia (20,038 cases/yr), Nigeria (13,481)
and Myanmar (6,247) — the three largest contributors — have all acquired public
genomes since that census, along with Cambodia, Brazil and Colombia.

**Publishing 33% would be a factual error a reviewer could catch with one
lookup, and our own panel contradicts it.**

### R5 — Two typing systems fail in the same places (orthogonal confirmation)

- **ST92 spans seven countries** — USA 26, Brazil 3, Mexico 3, Colombia 1,
  Nicaragua 1, Guadeloupe 1, Martinique 1 — and **four distinct lineages**. Two
  known-exposure validation genomes are ST92, so this is not a deposit-country
  artefact.
- **ST58** is China 25 / Thailand 20 / Philippines 9 — one ST, three countries,
  and it is the ST of most Philippine validation genomes.
- ST homoplasy is systemic: **52 of 279 STs span more than one unit**; ST70
  spans eight.
- cgMLST allelic distance vs recombination-filtered SNP distance: **median
  Pearson r = +0.861**, 66 of 85 frozen-basis units at r ≥ 0.7. The orthogonal check both
  external reviews asked for.

**Framing:** prior work already showed MLST lacks resolution to pin geographic
origin. **The novel half is that whole-genome, recombination-corrected
clustering does not rescue it.**

### R6 — Where geographic signal does and does not exist

Fitch parsimony on the corrected tree, 1,000 permutations, with a **BioProject
control on the identical tree** — the decisive question being *is country
significant in a way study-of-origin is not?*

| scale | testable | raw p≤0.05 | survives FDR | **passes the control** |
|---|---|---|---|---|
| sub-national | 83 | 17 | 11 | **0** |
| national | 49 | 26 | 24 | **6** |
| regional | 16 | 4 | 3 | **1** |

I re-derived the **6** independently: 11 units are country-clustered with
BioProject clean, but the **vacuous-control gate removes 4** (the control never
ran) and q<0.05 removes 1. The gate does real work — it eliminates **36% of
apparent passes** — and should be described in Methods as a result in itself.

**All six are Southeast Asian. Every Americas unit fails**, including the
Mississippi unit (p = 1.0000) and `strain_4_L1_4` (country p = 0.0010 *and*
BioProject p = 0.0010 at 31/33 coverage — a well-powered negative).

**Sub-national geography is indistinguishable from study of origin: 0 of 88.**
A label like `Thailand :: Nakhon Phanom` is very nearly the name of a collection
effort.

### R7 — What is operationally usable: the Gulf Coast cluster

**Figure 3.** Distance distribution, `strain_4_L1_1`, n=22.

| | chr1 | chr2 |
|---|---|---|
| internal median (raw / filtered) | 8 / **5** | 5 / **4** |
| max to the Colombian genome (raw / filtered) | 1,136 / **494** | 1,432 / **528** |

**Operational rule: a new US case within ~20 SNPs is the Gulf Coast lineage;
500+ away is not. The call is never borderline.**

Limit stated in the same breath: because the nearest outside relative is ~490
filtered SNPs away, **the origin of the lineage cannot be stated.** The
Colombian genome is *the nearest relative in this panel*, not *a near relative*
— a statement about Americas panel sparsity, not about an introduction route.

**Context for every distance in the paper:** across 176 replicon-units the
median filtered/raw ratio is **0.090** — about **91% of raw pairwise distance
is imported DNA, not inherited mutation.** Any distance quoted without saying
which kind it is means very little.

---

## 4. Discussion arcs

**D1 — The negative result is the useful one.** Reframe from "our method
failed" to "the exposure country is not in the genome to be found, for anyone,
with any method, until the source countries are sequenced." R3 and R4 are what
license this; without the resolution curve it would read as an excuse.

**D2 — Attribution reaches exactly as far as the reference panel, and no
further.** The same boundary shows up at country scale, at region scale (Africa
and Central America), and as outright unattributability. One mechanism, three
observations. This is the paper's most generalisable claim and it applies to any
pathogen with an uneven reference panel.

**D3 — Say "I don't know."** The nearest-neighbour distance is a natural
abstention criterion and the data argue for it strongly — see §5, weak spot W2.
This is how the paper converts a negative result into a deployable tool, and I
think it is the strongest *new* idea available.

**D4 — Sampling frame as a public-health finding.** Three nested facts, each
independently evidenced: **7 of 16** validation source countries have zero public
genomes, all of them Latin American & Caribbean (R4); **21 countries** with ≥100
predicted annual cases have none in ENA, ~5% of global burden, **19 of them
sub-Saharan African** (R4); and, most robustly, **South Asia carries 44.2% of
predicted cases and 2.5% of the genomes while East Asia & Pacific carries 39.4%
and 91.8%** (R1 Table 3).

Lead the discussion with the **regional** comparison — it is the one that does
not move between censuses.

The actionable recommendation is not "sequence more" but "sequence *these*", and
the priority list is already derived: Australia ~1,311, Puerto Rico ~56, Cambodia
~487, India ~40 — explicitly **not** more Thailand. Note the tension worth naming
in the text: that list is drawn from *what is available to download*, which is
itself the biased frame. The burden table says the highest-value sequencing is in
countries where **nothing exists to download at all** — South Asia and
sub-Saharan Africa. Those are different recommendations and the paper should make
both, distinctly.

**D5 — What this means for outbreak response.** Cluster membership is callable
(R7) even where geography is not (R2). Those are different questions and the
paper should separate them cleanly, because conflating them is how "we
sequenced it" gets over-promised to an incident team.

---

## 5. Weak spots, ranked by how much damage a reviewer could do

### W1 — The validation set is far smaller than n=24 suggests ⚠ **most serious**

I computed this directly and it is not stated anywhere in the corpus. **[SNP/24]
— the pseudoreplication point holds and hardens on [cg-Licht/46], where the
Philippines is 12 of 46:**

- 24 scorable rows come from **9 exposure countries** and **3 BioProjects**.
- **The Philippines alone contributes 11 of 24 (46%)**, all correct. *(On
  [cg-Licht/46]: 12 of 46, still all correct at region — same concern, larger n.)*
- Excluding the Philippines: **11/13 (85%)** — still above baseline, but on 13
  observations.
- Five countries contribute exactly one genome each.

The 24 observations are **not independent**; pseudoreplication operates at the
study level, and the project already owns `pseudoreplication_bp.py`.

**How to strengthen.** (a) Report the by-country score as the headline —
**8 of 9 exposure countries correctly placed at region scale** — which is more
honest *and* more persuasive than 92%. (b) State the BioProject count. (c) The
incoming batch takes the set to 44 and adds Australia, Thailand and India,
which are countries where the panel *does* hold references — this is the single
highest-value pending experiment and R2 should be re-run on it before
submission. (d) The one country-level failure is Viet Nam, and it has a known
cause: its unit is USA 6 / Viet Nam 5, so deposit-country labels outvote
exposure labels. That is a metadata defect, not a genomic limit, and fixing it
is cheap.

### W2 — The Latin American region successes may be luck ⚠ **new finding**

Stratifying the region result by nearest-neighbour distance. **Corrected
2026-08-23 — the [cg-Licht/46] column previously shown here (11/14 · 6/10 ·
20/22) was the NEAREST-NEIGHBOUR stratification printed beside a modal-k=20
headline.** The estimator-matched figures are below; use the **modal k=20**
column, because 89% is a modal number.

| stratum | [cg-Pub/29] | [cg-Licht/46] **NN** | [cg-Licht/46] **modal k=20** ← use |
|---|---|---|---|
| d < 0.05 (a real relative exists) | 8/10 | 11/14 | **14/14** |
| 0.05 ≤ d < 0.30 | 4/6 | 6/10 | **8/10** |
| **d ≥ 0.30 (no real relative)** | **11/13** | 20/22 | **19/22** |

**This strengthens the paper's central claim rather than weakening it.** Region
attribution is **perfect where a close relative exists — 14/14** — against
country's **2/14 on those same 14 genomes.** That is the depth-ceiling result in
its cleanest form: same genomes, same pool, same holdout, opposite outcomes at
two geographic scales.

That bottom row still looks like a success and still is not, and the mechanism is
now confirmed directly on the current data. Of the 22 genomes at d ≥ 0.30, **nine
share a single Ecuadorian nearest neighbour** (`GCF_000959265_1_Ecuador`) and
five share one Indian reference. Eleven of the 22 are genuinely Latin American,
so "Ecuador → Latin America & Caribbean" scores correct. **Both Sub-Saharan
African genomes in the stratum are called Latin America & Caribbean under modal
k=20 and scored wrong** (`SRR35174254`, `SRR35239810`) — under NN only one of
them misses, so the headline estimator is the *less* forgiving one here. Same
mechanism, different luck.

Same mechanism, different luck. At d = 0.46, 46% of cgMLST loci differ — that
is not a relative in any meaningful sense. The method is not identifying
provenance; it is reporting *"unlike the Asian majority of the panel"*, and the
catch-all region label converts that into a correct answer for the Americas and
a confidently wrong one for Africa.

**How to strengthen.** This is W1's problem and D3's opportunity. Report region
accuracy **stratified by nearest-neighbour distance**, and propose the
**abstention rule**: above a distance threshold, return *"unattributable —
novel lineage"* rather than a region. That rule would have correctly declined
both African genomes instead of calling them Latin American. It turns the
weakness into the paper's most useful methodological contribution.

**⚠ Controlled 2026-08-22 — the concern is now precisely bounded, and it is
narrower than "region may be luck."** `DOWNSAMPLING_CONTROL_RESULT_2026-08-22.md`
rebalanced the panel and re-scored. Two distinct "attractor" mechanisms have to
be separated:

- **Majority-imbalance attractor** (genomes snap to the dominant East Asia &
  Pacific cluster, 89% of references): **refuted.** Capping East Asia & Pacific
  from 2,692 references to 30 — a 90× cut, 89% → ~15% of the pool — moves region
  modal-k20 kappa only from **0.89 to 0.81**. An artifact would collapse toward
  0. So the *bulk* of region accuracy reads the genome's regional cohort, not the
  panel's shape, and the ~0.08 erosion bounds the total imbalance contribution at
  roughly a tenth of the signal.
- **Local-cluster attractor** (the d ≥ 0.30 stratum above: LatAm cases snapping
  to one *small* Ecuadorian reference): **not addressed by rebalancing**, because
  capping does not remove a small cluster, and it should not be claimed to be.
  This is the residual W2 concern, and it is exactly the case the abstention rule
  targets.

Net: report region as a genuine capability (the majority-artifact control is the
evidence) **with** the abstention rule for the no-relative stratum (the local
attractor is the reason). Do not let the strong control be read as licensing the
d ≥ 0.30 calls — it does the opposite of that.

**Note the two methods differ here and the lineage method is sounder.** The
SNP/unit-based region calls rest on genuine co-membership — `strain_4_L1_3` is
Brazil 31 / Guatemala 2 / Aruba 2, `strain_4_L1_4` is USA 13 / Mexico 6 /
Puerto Rico 5 / Ecuador 2 / Colombia 2. Those are real pan-Americas lineages.
The cgMLST nearest-neighbour result agrees with them **for a much weaker
reason**. Say so rather than presenting the agreement as simple corroboration.

### W3 — ✅ **RESOLVED 2026-08-21.** Gate 1 recomputed in alignment units

The challenge was that the r/m headline (then **7.38**, median of 47 of 88 units
"inside the window") rested on a 47/88 split computed by converting Mash distance
to approximate SNPs (`mash × 3,805,619 bp`), while the window itself was
calibrated in `ska distance` units — a triage-grade conversion by its own
docstring, and the project had recorded sketching mis-scaling by **0.88×–91×**.

**Done, and the fix mattered.** Recomputed on alignment-derived distances the
proxy proved to **misplace 22 of 85 units**; the window is **[700, 4700] mean
pairwise core SNPs** (floor bracketed (588, 755]) and the headline is
**r/m = 7.70 across 47 of 85 units** (`rm.median_gate1`), with 1.99 outside — the
contrast that makes this a *detection* window rather than a filter.
`GATE1_ALIGNMENT_RESULT_2026-08-21.md`.

⚠ **Never quote 7.38, 7.44 or 7.26** — different partitions or the Mash proxy.
**Residual, for Paper 2 only:** `trackA_diversity` still feeds the Mash proxy, and
Gate 1's union-coverage criterion does not reproduce the calibration's 76–88%
(max band median 68%) — disclose that, per `rm.gate1_caveat`. The floor does not
depend on it.

### W4 — Gate 1's lower bound is disclosed as wide but not as inadmissible

`METHODS_DRAFT` §2.6.1 is honest that the floor is a bracket — *"(405, 1,268]
— still 3.1× wide, and rests on one cluster either side"* — and that the whole
rule is *"a construct calibrated on this dataset, not a published constant."*
Good. But the archive goes further: the bracketing observations are themselves
**mixtures**, so the floor rests on nothing admissible, and the circularity is
structural (modality is only interpretable *inside* the range whose lower bound
is being derived).

**How to strengthen.** Describe the lower bound as *"the lowest diversity at
which a unit has been observed to work"* — an operating convention — not as a
measured threshold. The draft already uses almost exactly that phrasing
elsewhere; make it consistent.

### W5 — The lineage partition changed five times

v2 → v3 → v4 → v4b → v4c. A reviewer will ask whether conclusions ride on it.

**The answer is good, and I verified it.** Unit *labels* are not stable across
versions and must never be quoted across versions. But for the validation
genomes, **v4b→v4c co-membership agreement is 198/210 pairs = 94.3%**, and the
12 disagreeing pairs are one real refinement (v4b `strain_5_L1_7` splitting into
v4c `strain_4_L1_3` + `strain_4_L1_4`). Coverage improved monotonically:
**5 → 21 → 25** validation genomes placed in analysed units.

**And the headline does not depend on the partition at all** — MLST and cgMLST
nearest-neighbour need no units and return the same answer. Put that sentence
in the Results, not the rebuttal letter.

### W6 — Stale numbers inside current documents

**Partly addressed 2026-08-23:** the attribution figures are now reconciled — see
the **Figure Provenance Key** at the top. Every attribution number carries an
analysis tag ([SNP/24], [cg-Licht/46], …) so the "same quantity, two values"
cases are now distinguishable as *different analyses*, not contradictions. The
r/m and census stale-number cases below still stand.

The corpus contains at least 15 places where the same quantity has two values.
The dangerous ones, because both versions sit in the *same* file:

| quantity | stale | correct |
|---|---|---|
| validation set | 26 → 31 → 43 | **48 registered / 46 scorable** |
| panel | 2,976 | **2,955** (`panel.corrected_v4d`) |
| ENA coverage | 44% → 41.4% | **41.1%** (`panel.coverage_of_ena`) |
| analysed units / genomes | 88 / 2,342 | **85 / 2,340** (frozen basis) |
| r/m headline | 7.38 / 7.44 / 7.26 | **7.70** (`rm.median_gate1`) |
| zero-genome source countries | 9 of 16 → 7 of 15 | **7 of 16** |
| region accuracy | 100% on 19, baseline 58% | **92% on 24 [SNP/24]; 89% on 46 [cg-Licht/46]** |
| country LOO nearest-neighbour | 37% | **29%** (7/24) |
| sub-national | *"untestable"* | **testable, and fails 0/5** |
| CFML/Gubbins offset | ≈4.9× | **2.19× / 2.45×** |

**48 vs 46 is not a discrepancy** — 48 genomes are registered, 2 carry a
non-country exposure ('Africa', 'Panama and Peru') and are unattributable, so 46
are scorable. Every `x/46` is over the scorable set (`validation.scorable`).
Never use 48 as an attribution denominator.

The sub-national one is the worst: `ATTRIBUTION_AND_DISTANCES_FINDINGS` states
both, about thirty lines apart.

**How to strengthen.** Before any drafting, do a numbers freeze: recompute every
quotable figure from the TSVs and mark the documents. The project's own rule
already covers this — *"recompute it from the artefacts; the appendix entries
were often written mid-run."*

### W7 — "Region" is a **binary** classification, not a 7-way one ⚠

I checked, and this is sharper than the corpus states anywhere. The 24 scorable
region rows carry exactly **two** labels:

| label | n |
|---|---|
| East Asia & Pacific | 13 |
| Latin America & Caribbean | 11 |

That is the whole task. The 54% majority baseline is exactly 13/24, which
confirms it. **The two Sub-Saharan African genomes are not in the scorable set
at all** — they are among the six that fall in singleton units (R4), so the one
region category that would have made this a three-way problem is precisely the
one the method cannot place.

So the headline is: **[SNP/24] 92% on a two-class problem, n=24, from 9 countries and 3
BioProjects, with 46% of rows from a single country.**

This is still the operationally right question — *did this person acquire it in
the Americas, or while travelling in Asia?* — and 92% against 54% is a real
lift. But "region-level attribution works" invites a reader to picture a 7-way
geographic assignment, and that is not what was tested.

**How to strengthen.** Call it what it is in the Results text: a
**binary Asia-vs-Americas discrimination**. Report it alongside the by-country
score (8/9, W1) and the distance stratification (W2). Three honest framings of
the same 24 observations are far more convincing than one inflated one — and
the incoming 44-genome set adds Australia, Thailand and India, which is what
would genuinely make it multi-class.

### W8 — ⚠ **HALF-RESOLVED 2026-08-23. Fixed in the frozen basis; still live in the cgMLST reference pool**

**What is fixed.** The frozen basis carries the register cross-check as a
first-class validation: `freeze_basis_bp.py` asserts *"no register-excluded
genome in the partition"* and *"no duplicate BioSample in the partition"*, and
both **PASS at 0**. Re-run directly against `FINAL_PARTITION.tsv` and
`FINAL_PANEL.tsv`: **0 of the 46 register rows appear in either.** The scenario
below — a `broken_assembly` genome inside `strain_1_L1_26` — **can no longer
happen in the reported analysis**, and the check is now automated rather than
documented.

**What is still live, and it is a real reviewer target.** The exclusion register
was never applied to the **cgMLST reference pool**. All four genomes below are
present in `cgmlst_lichtenegger/MANIFEST.tsv` and therefore in the pool that
every [cg-Licht/46] attribution call searches — including **`SRR2896271`, which
fails the *species* gate outright** (`mash_K96243 = 0.0135` against a ≤0.008
threshold; it may not be *B. pseudomallei*).

**Measured consequence, so the scope is not guesswork:** one validation genome's
nearest neighbour is an excluded assembly — `SRR33748081` → `SRR2896257`
(3,315 contigs) at **d = 0.79048**. At that distance it is not a relative in any
meaningful sense; it sits deep in the W2 attractor stratum. Its region call
scores correct, its country call does not. **So the headline does not move on
this genome — but "an excluded broken assembly is a nearest neighbour in our
attribution analysis" is a sentence we do not want a reviewer writing.**

**How to fix.** Drop the four from the cgMLST manifest and re-score. That
changes a frozen headline, so do it as a **deliberate batched refresh** (register
→ regenerate attribution → recompute strata → propagate n), never piecemeal —
`TRACK0_INTEGRATION_2026-08-23.md` is the model. Then extend the register
cross-check to cover the cgMLST manifest, not just the partition.

<details><summary>The original W8 finding, retained for the record</summary>

`PANEL_EXCLUSIONS_README` specifies its own cross-check: *"excluded samples
present in the panel → must be 0."* **I ran it. It is 4**, and one is inside an
analysed unit:

| sample | register reason | in panel | in an analysed unit |
|---|---|---|---|
| `SRR2896257` | broken_assembly | yes | **`strain_1_L1_26`** |
| `SRR2896259` | broken_assembly | yes | no |
| `ERR9980356` | broken_assembly | yes | no |
| `SRR2896271` | **wrong_species_or_divergent** | yes | no |

Two things make this worse than a bookkeeping slip.

**First, `strain_1_L1_26` is the worst possible unit for this to happen in.** It
is the largest (n=154), it is the unit the A100 split three ways, and its
pre-split **r/m of 3.10 was in-window and therefore a reportable measurement**.
`SRR2896257` is **7,452,260 bp in 3,315 contigs** — above the 7.4 Mb upper bound
and more fragmented than any assembly in the base collection.

**Second, the exclusions themselves rest on an unpopulated field.** All four
register rows read `core=na%` — the core-coverage measurement was never made —
while their gene-count ratios are **0.96, 1.14, 0.92, 0.94**, all *below* the
1.20 gate. So the stated reason ("core coverage <85% **or** ratio >1.20") is
evidenced by neither clause. `SRR2896271` is a separate matter: at
`mash_K96243 = 0.0135` it fails the ≤0.008 species gate outright, and it is in
the panel.

**Neither the exclusion nor the re-inclusion is currently evidence-based.** They
were decided on SKESA-batch measurements and the panel then used the SPAdes
re-assemblies, which were QC'd under different gates.

**How to fix.** Re-measure core coverage on the four SPAdes assemblies, then
either formally rescind the exclusions with evidence or drop them and re-derive
`strain_1_L1_26`. Then re-run the register cross-check to zero and keep it as a
CI check. This is a few hours and it removes the single most concrete thing a
reviewer could find by running your own documented check.

</details>

**The unpopulated-evidence problem above is still unresolved and still matters**,
because it governs whether the four should be dropped from the cgMLST pool or
formally re-included: all four register rows read `core=na%`, so the stated
reason ("core coverage <85% **or** ratio >1.20") is evidenced by neither clause.
Re-measure core coverage on the SPAdes assemblies before deciding either way.
`SRR2896271` is separable — it fails the species gate on mash alone and should
come out regardless.

### W9 — Submission blockers that are not science ⚠ **fix these first, they are cheap**

None of these is a weakness in the work. All of them will stop a submission.

- ~~**No ethics or consent statement exists**~~ — **RESOLVED 2026-08-21: the
  epidemiology team handled the IRB** for the 312 in-house Nakhon Phanom isolates
  (259 `IP-`, 53 `IE-`). Remaining task is text-gathering only: **get the
  approval number and approving body into the Methods.** "The epis handled it"
  is not a Methods sentence. No longer a blocker.
- **No data availability statement, and the 174 new assemblies do not appear to
  be deposited.** Needs: accession list, the new assemblies in ENA/GenBank, and
  the supporting tables (`PANEL_EXCLUSIONS.tsv`,
  `curated_L1v4c_clusters.final.tsv`, `EXPOSURE_OVERRIDES.tsv`).
- **No flow diagram.** Every number exists but the figure does not. **Updated to
  the frozen basis:** 9,040 ENA BioSamples (union of `read_run` + `assembly`;
  7,192 with a country) → **2,955** corrected panel → **2,340 genomes in 85
  analysed units** → **47 units in-window** for r/m. This should be **Figure 1**;
  it does more work than any other single display item because it makes the
  attrition auditable. ⚠ Do not reuse the old chain (8,500 → 2,976 → 2,352 →
  2,342 in 88 units): three of its five numbers are superseded.
- **The exact production command line is no longer pinned.** The 2026-08-11
  methods draft cited `branch reference-blocklist, commit f1a7d13`; the 08-19
  rewrite dropped the branch and commit and cites only the repo URL. Restore it.
- **A single stated inclusion rule.** `SAMPLING_FRAME_2026-08-21.md` §5 already
  drafts one and it is better than anything in the methods draft — promote it.

### W10 — Methods-draft contradictions that a reviewer reading the scripts will find

The methods draft is **two pipelines in one document** — a calibration track
(`ska map`, 2,802 genomes, PopPUNK K=4, IQ-TREE 2.4.0 with `-fconst`) and the
production run (**Snippy 4.6.0**, 2,976 genomes, **PopPUNK K=5**, IQ-TREE 2.2.6
with **`GTR+ASC`**). Three consequences:

1. **Every gate and threshold was calibrated under one variant caller and
   applied under another**, while the same document states that **no stable
   caller correction factor exists** (r/m shifts −15% to +76% with no consistent
   sign). This transfer is nowhere justified.
2. **Production used `+ASC`; the calibration section explicitly argues against
   it** on exactly these data, because in a 68% GC genome `+ASC` collapses base
   composition toward 25/25/25/25 while true `-fconst` counts reproduce it. The
   validation in §2.8.1 covers `-fconst`, not `+ASC`. The open item "quantify
   ASC vs `-fconst` on one unit" is still open. **Do that one unit.**
3. **§2.6.3 contradicts itself about union coverage** — it establishes that
   union is size-confounded (`r(log n, union) = +0.80`, partial +0.84) and then,
   forty lines later, states union was "found **not** to scale with unit size
   (r = 0.142)". That is stale text that was never deleted, and it is the exact
   error the project later named. **Delete it.**

Also unexplained: **PopPUNK changed from K=4/271 strains to K=5/310 clusters**
between drafts with no stated rationale, and branch support may not actually
have been enabled in production (`iqtree_support = false` is the repo default
while §2.12.8 asserts support was on). **Confirm from `pipeline_info/`.**

### W11 — Known metadata defects, quantified and mostly harmless

US Caribbean territories split across two conventions (10 genomes); `Viet Nam`
vs `Vietnam`; the compound `Panama and Peru`. Normalising all three altered
**2 of 88 units** and **changed no p-value or verdict**. Harmless, but fix
before print. Separately: `iso_a3` is not a clean substitute — it records
reporting country, so Aruba, Guatemala and Mexico rows all carry `USA`.

---

## 6. Literature positioning

### 6.1 The one-sentence frame

**Prior work reconstructs; we predict.** Seng et al. 2024 and Chewapreecha 2017
reconstruct history and score it by internal consistency. We ask whether the
origin of an *unknown* isolate can be predicted, and score on held-out cases.
Prediction is strictly harder, and that difference is why our headline is more
negative than theirs. Say this explicitly and early — it is the whole
positioning, and without it a reviewer reads our result as contradicting a
literature it does not contradict.

### 6.2 The comparison set

| work | what it showed | our relation |
|---|---|---|
| **Seng R, … Chantratita N. *Nat Commun* 2024;15:5699.** PMID 38972886 | 1,391 genomes, NE Thailand; PopPUNK→rhierbaps→per-lineage Gubbins; **per-lineage r/m 3.7 / 4.6 / 2.2**; temporal signal in only 1 of 10 sub-lineages | **Same architecture, harder question.** Our in-window r/m sits in the same range. Two deliberate differences: `-fconst` vs their `+ASC` (compositional, 68% GC), and our control is **study of origin** where theirs is **spatial density** — not substitutable, each forced by its collection design. **They are ahead on** pangenome (Panaroo, 15,237 genes) and environmental covariates. ⚠ **Cite as Seng, not "Chewapreecha 2024"** — internal docs get this wrong |
| **Chewapreecha C, et al. *Nat Microbiol* 2017;2:16263.** PMID 28112723 | 469 isolates, 30 countries; clusters almost perfectly geographic (19 of 20 ≥90% one region); African root for the Americas group | Consistent. We add the prospective test they did not attempt |
| **Viberg LT, … Currie BJ. *mBio* 2017;8(2):e00356-17.** PMID 28400528 | *"very strong phylogeographic signal that allows accurate identification of strain origin on a continental level"*; correctly assigned a CF patient to SE Asia | **A counterpoint to carry, not contradict.** Our 92%-region / 0%-country result **is the quantified version of exactly this sentence.** Frame as agreement made precise |
| **McLaughlin HP, Gulvik CA, Sue D. *PLoS NTD* 2022.** doi:10.1371/journal.pntd.0009882 | dual-locus PBP scheme for geographic origin; **no independent test set, no cross-validation**; D = 0.8512 | **The contradicting result — and not a straw man.** Frame as *"we tested prospectively what prior schemes asserted descriptively."* Never as carelessness; their aim was a cheap assay. Gentle design point: **PBP genes are β-lactam targets under selection**, so signal there may track antibiotic use and homoplasy, not descent. **They themselves documented** that four "UK" ST-1 strains are lab cultures of K96243 — the same metadata failure mode we hit |
| **Sprenger H, … Gulvik CA. *Microbiol Spectr* 2026.** doi:10.1128/spectrum.02926-25 | attributes the aromatherapy MAG to **India** — a country-level call, from CDC | ⚠ **Must not appear to contradict.** Single-strain attribution **with supply-chain corroboration** vs blind systematic prediction. CDC's own *genomics* gave **South Asia**; the country came from product provenance. State our claim narrowly |
| **Gee JE, et al. *EID* 2017;23(7)** | Western Hemisphere / ST92 framing, n=26, no recombination correction, no validation | **New ground.** ST92 spans **7 countries and 4 units** — the type is not one lineage |
| **Petras JK, … *NEJM* 2023.** doi:10.1056/NEJMoa2306448 | Mississippi Gulf Coast, 3 clinical + 3 environmental | The reference event for R7. **Open: read the published ST off the paper** |
| **Brennan T, … Gulvik CA. *EID* 2025.** doi:10.3201/eid3109.250804 | 4 Georgia cases, no travel, relatedness → shared exposure | **The published applied precedent for our ≤20-SNP rule.** Cite rather than describing the use case abstractly |
| **De Smet B, et al. *JCM* 2015;53(1):323–6** | 4 isolates showing ST105/ST849 Cambodia–Australia sharing is homoplasy; eBURST *"unreliable for inferring the geographic origin of STs"* | **Same phenomenon, we supply the denominator:** 52 of 279 STs span >1 unit; ST70 spans eight |
| **Nandi T, et al. *Genome Res* 2015;25:129–141.** PMID 25236617 | genome-wide **r/m 7.2**; **≥78% of K96243 ever recombined**; recombination higher on chr II | Consistent. The species-wide "7.2" anchor was used as a threshold and **withdrawn as a category error** — do not revive |
| **Gee JE, Gulvik CA, Castelo-Branco DSCM, Sidrim JJC, Rocha MFG, Cordeiro RA, Brilhante RSN, Bandeira TJPG, Patrício I, Alencar LP, da Costa Ribeiro AK, Sheth M, Deka MA, Hoffmaster AR, Rolim D. Genomic Diversity of *Burkholderia pseudomallei* in Ceará, Brazil. *mSphere* 2021;6(1):e01259-20.** PMID 33536328 | **59% of 31,594 core SNPs recombinant** → r/m ≈ 1.44 | Same direction, ours larger (78.5% pooled). **Not like-for-like** — r/m scales with the divergence of the set; ours are within-strain subclusters, theirs a regional collection over 14 STs. |
| **Didelot X, Parkhill J. *Phil Trans R Soc B* 2022;377:20210246** | the pipeline paper; **Figure 1 is this architecture** | The methodological citation. Key quote: at high r/m *"an alignment containing only the non-recombinant sites would contain no sites"* — the justification for building on the clonal genealogy |
| **Yu Y, Wheeler NE, Barquist L. *PLoS Biol* 2025;23:e3003539.** PMID 41401143 | 24,000 genomes, 5 pathogens; recommends *"phylogeny-aware cross-validation testing on held-out clades"*; *"increasing the training sample size fails to rescue performance"* | **Cite for the leave-group-out design** — converts a from-scratch derivation into a citation — **and** for "more sequencing won't fix this". **Never mentions BioProject/study origin**, which is what leaves 4.1 below open |
| **Blackwell GA, et al. *PLoS Biol* 2021;19(11):e3001421.** PMID 34752446 | **50% of 661,405 ENA genomes come from 50 of 23,316 projects** | Direct support for treating BioProject as the confounder |
| **Limmathurotsakul D, et al. *Nat Microbiol* 2016;1:15008.** PMID 26877885 | 165,000 cases/yr; **South Asia 44% of burden**; endemic in 45 countries, likely 34 more | The denominator for §6.4 |

### 6.3 Novelty claims — how well each is actually supported

The corpus's own rule is right and should be kept: **write "we are not aware of",
never "first."** I grepped; no unhedged "first" claim currently exists. Ranked by
strength of evidence:

1. **BioProject as a measured companion control — strongest.** Two independent
   negative searches agree, and Yu 2025 (24,000 genomes, entirely about sampling
   bias) never mentions study origin or lab batch. Still owed the systematic
   search the corpus itself lists as open.
2. **Leave-group-out attribution validation — well supported**, but cite Yu 2025
   for the principle and claim novelty only for the *B. pseudomallei*
   application.
3. **Resolution-invariance across 584-fold — weakest-evidenced.** No documented
   search backs "we are not aware of this for any bacterial pathogen." Either run
   the search or drop the novelty framing and let the result stand on its own.
4. **Two-detector concordance (Gubbins + ClonalFrameML at panel scale)** —
   plausible, hedge it. The *finding* (thresholds do not transfer) is solid.

**The governing caveat, from the corpus and worth heeding:** a claim of "no
published application of PopPUNK to *Burkholderia*" was made and **retracted** —
Seng 2024 had done it, but the paper is not indexed under the tool name. Every
"we are not aware of" here means "not found by keyword search."

### 6.4 The burden-versus-genomes comparison — **now folded into R1 (Table 3) and R4**

**Done.** Recomputed 2026-08-21 against the current v4c panel and moved into the
Results, where it belongs. See **R1 Table 3** for the regional table and **R4**
for the country-level version.

**What changed when I recomputed it, and why it matters:** the version circulating
in `GAP4` was computed on the superseded **2026-08-09 NCBI census (5,515
genomes)**. Two of its figures do not survive:

| figure | `GAP4`, on the 2026-08-09 census | recomputed on the v4c panel |
|---|---|---|
| countries ≥100 cases/yr with no genomes | **29** | **21** (ENA union, final) |
| their share of global predicted burden | **33%** (54,076 cases/yr) | **5%** (8,939 cases/yr) |
| South Asia share of genomes | 2.9% | **2.5%** |
| EAP oversampling vs South Asia | 36× | **41×** |

The 33% collapses to 7% because **seven of the 29 now hold genomes** — Cambodia
47, Brazil 32, Colombia 11, Nigeria 10, Myanmar 9, Indonesia 7, El Salvador 1 —
and those include the three largest contributors to the old total (Indonesia
20,038 cases/yr, Nigeria 13,481, Myanmar 6,247).

**Publishing "33% of global burden has zero genomes" would be a factual error a
reviewer could catch with a single lookup, and our own panel contradicts it.**

The *regional* comparison is robust and survives on either census — that is the
one to lead with. Also note the country-level headline figures **35,852-fold**
and **Australia 1,877× India** are from the same superseded census and are not
in R1/R4 for that reason; regenerate them before use.

**Done.** The ENA union census was re-run 2026-08-21 and the final figures are
**21 countries / 5%**, with **19 of the 21 sub-Saharan African**. Full working in
`GENOME_REGISTER_2026-08-21.md` §5.

### 6.5 Citation hygiene — errors already caught, do not reintroduce

**Never cite:** a pooled Chewapreecha rate of 1.03 × 10⁻⁶ (appears nowhere in
that paper); the ~772 kb divergence denominator behind "0.73–5.61%".

**Already corrected once:** Pearson 2009 is ***BMC Biology***, not BMC
Microbiology. Kalkauskas 2021 is *PLoS Comput Biol*, not Phil Trans R Soc B.
Kühnert 2016 is *Mol Biol Evol*. BETS is PMID 32895707.

**Verify before citing:** Pearson 2020's PMID (**two different values appear in
our own documents**); De Smet 2015 PMID (missing); the Ceará 2021 author list
(missing); the eLife Salmonella attribution paper (**cited as a bare URL only**);
Seng's rate-prior reference [53], which resolves to a pangenome paper with no
clock analysis.

⚠ **Which cgMLST scheme do we cite? SUPERSEDED — this section was written when
cg-Pub was the headline, and the headline has since changed. Read the correction
first.**

> ### ✅ CORRECTED 2026-08-23 — the headline scheme is Lichtenegger, and it must be cited
>
> The paper's headline analysis is **[cg-Licht/46]**, run on the **Lichtenegger
> 4,221-locus scheme**. Verified against a fetched PubMed record, not an internal
> document:
>
> **Lichtenegger S, Trinh TT, Assig K, Prior K, Harmsen D, Pesl J, Zauner A, Lipp
> M, Que TA, Mutsam B, Kleinhappl B, Steinmetz I, Wagner GE. Development and
> Validation of a *Burkholderia pseudomallei* Core Genome Multilocus Sequence
> Typing Scheme To Facilitate Molecular Surveillance. *J Clin Microbiol*
> 2021;59(8):e0009321. PMID 33980649, doi:10.1128/JCM.00093-21.**
>
> The abstract states the scheme was built by challenging K96243 with 469 genomes
> yielding **4,221 core and 1,351 accessory targets** — matching our 4,221 exactly,
> and confirming the scheme is real, published and validated (320 WGS datasets).
>
> **So the instruction below — "remove the Ashcroft and Lichtenegger citations" —
> is inverted for the current headline.** It applies only to the superseded
> [cg-Pub/29] run. Concretely:
>
> - **[cg-Licht/46] (headline)** → cite **Lichtenegger 2021, PMID 33980649**.
> - **[cg-Pub/29] (supplement, scheme-swap robustness only)** → cite the platform,
>   **Jolley 2018, PMID 30345391**, and record the snapshot; it has no scheme
>   publication.
> - **"Ashcroft 2021" is a phantom** and must never be cited — it does not exist as
>   a distinct scheme; the reference resolves to Lichtenegger.
>
> Because the headline scheme is published and versioned, the "experimental, subject
> to change" caveat below **no longer attaches to the headline** — it attaches to the
> supplementary cg-Pub run. Still record the Lichtenegger scheme version (v1.1,
> 4,221 loci) and archive the allele FASTAs.

<details><summary>The superseded 2026-08-21 determination, retained for the record</summary>

✅ **Which cgMLST scheme did we use? RESOLVED 2026-08-21.** It is **neither**
Ashcroft 2021 nor Lichtenegger 2021 — both are 4,221-target schemes. We ran
**PubMLST scheme 2, "cgMLST — *Burkholderia pseudomallei* typing", 4,090 loci,
1,154 profiles, last updated 2026-06-18, curated by Jessica Webb** (University of
Adelaide / Menzies School of Health Research). **It has no scheme publication.**

**Cite the platform:** Jolley KA, Bray JE, Maiden MCJ. *Wellcome Open Res*
2018;3:124, PMID 30345391. **Remove the Ashcroft and Lichtenegger citations
wherever they are attached to our cgMLST results.**

⚠ **The scheme is flagged "experimental in development" and "subject to
change".** So the Methods must record the exact snapshot — scheme 2, 4,090 loci,
1,154 profiles, retrieved 2026-06-18 — and state that results are reproducible
only against it. Archive the allele FASTAs with the results. This is a provenance
statement, not a weakness: the 4,089 called loci behaved well (median call rate
95.5%, cgMLST-vs-SNP concordance r = +0.861).

</details>

### 6.6 A real hole in the literature review

**Accessory-genome and tree-free source attribution was never searched.** GAP1
covers reference-free k-mer methods but records no search for accessory/unitig
attribution, ML attribution from genomes, kSNP or sourmash. The Salmonella
accessory-unitig study — the direct precedent for the highest-value open
experiment (§7 item 6) — exists in our notes **as a bare URL with no author,
year or title**. The one solid tree-free precedent on record is **Wilson DJ, et
al. *PLoS Genet* 2008;4(9):e1000203** (*Campylobacter* source attribution), and
its dependency is exactly our problem: it needs **independently sampled
reference panels per candidate source**.

**A separate literature pass is required here before the accessory experiment is
written up.**

---

## 7. What to do next, in order

**Start now, because it has the longest lead time and nothing else depends on
you:**

0. ~~Ethics/IRB~~ — **done by the epis.** Just collect the approval number and
   approving body for the Methods (W9).

**Then, in order:**

1. **Decide §1.** One sentence, written down: this is Paper A+D, and C is a
   separate paper. Everything else is downstream of that.
2. **Fix the exclusion register** (W8) and re-run its own cross-check to zero.
   Highest concreteness-to-effort ratio on this list — a reviewer running your
   documented check currently finds a `broken_assembly` genome inside the
   largest analysed unit.
3. ~~**Numbers freeze**~~ — **DONE.** `generate_numbers.py` → `NUMBERS.tsv` is
   the single source, `freeze_basis_bp.py` validates the basis (14 checks), and
   the estimator is now part of every attribution key. W6's table above records
   what moved. Remaining: the `PRIMER` is still the most quotable and most stale
   document in the workspace — regenerate it or mark it.
4. **Add the distance-stratified region table and the abstention rule** (W2/D3).
   **The table now exists** (W2, estimator-matched: 14/14 · 8/10 · 19/22) — what
   is still owed is the *abstention rule* itself: pick the threshold, score the
   rule, and report what it declines. Still the most novel thing available to
   the paper.
5. ~~**Re-run R2 on the 44-genome validation set**~~ — **DONE 2026-08-23 (Track
   0), and it landed at 46, not 44.** Portugal→Thailand plus 2 Mississippi
   autochthonous→USA, requiring leave-*outbreak*-out via an explicit register
   (`OUTBREAK_GROUPS.tsv`). North America is now testable. Region fell 93%→89%
   (κ 0.890→0.832) precisely *because* the harder case entered the set.
   `TRACK0_INTEGRATION_2026-08-23.md`.
6. ~~**Run the accessory-genome test**~~ — **DONE, and it FAILS its controls.**
   It looked positive (country 30% vs core 21%) but scores **0/13 where a close
   relative exists**, is 5× sensitive to assembly quality, and the entire margin
   rests on two Mississippi reference genomes. **Do not present it as a
   contrast**; the core result is strengthened by its failure.
   (`ACCESSORY_ATTRIBUTION_RESULT`)
7. **Score the PBP dual-locus scheme through the identical holdout.** The one
   published method that could undercut R3 — better to run it than caveat it.
8. **Delete the stale union-coverage paragraph** in `METHODS_DRAFT` §2.6.3 and
   resolve the `+ASC` vs `-fconst` question on one unit (W10).
9. **Re-run the MLST row** of Table 4 on the corrected **46**-genome set (it
   still predates the correction and is the last untagged row in R3).
10. Fix the metadata defects (W11), read the Mississippi ST off NEJM, and
    convert every "first" to "we are not aware of".
11. **Literature pass on accessory-genome / tree-free source attribution**
    (§6.6). It is unsearched, and it is the evidence base for item 6.
12. ~~Settle which cgMLST scheme paper to cite~~ — **REOPENED then RESOLVED
    2026-08-23.** The 08-21 answer (PubMLST scheme 2, drop Lichtenegger) applied
    when cg-Pub was the headline. The headline is now **[cg-Licht/46]**, so
    **cite Lichtenegger 2021, PMID 33980649** (verified against PubMed; 4,221
    core targets, matches ours) for the headline, and Jolley 2018 only for the
    supplementary cg-Pub robustness run. "Ashcroft 2021" is a phantom — never
    cite it. See the correction box in §6.5.
13. **Citation audit** (§6.5): resolve the two conflicting Pearson 2020 PMIDs,
    retrieve the Ceará 2021 and eLife Salmonella citations, and fix
    "Chewapreecha 2024" → **Seng et al. 2024** everywhere.
14. ~~Regenerate the zero-genome country list~~ — **DONE 2026-08-21.** ENA
    union census re-run; final figures **21 countries / 5%**, and the validation
    countries corrected to **7 of 16** (recomputed 2026-08-23 on the n=46 set;
    the seven countries are unchanged). See `GENOME_REGISTER_2026-08-21.md`.
15. ~~**Re-run the country-scale scoring when the assemblies land**~~ — **DONE
    2026-08-23; superseded by item 5.** Validation reached **46**. The fair test
    it promised has now been run, and country still does not clear baseline
    (10/46 = 22% vs 26%), including for well-referenced countries — which is the
    result, not a shortfall.

**New, added 2026-08-23 — apply the exclusion register to the cgMLST pool (W8).**
All four register-excluded genomes are in `cgmlst_lichtenegger/MANIFEST.tsv`,
one of them failing the species gate, and one serves as a validation genome's
nearest neighbour. Fix as a deliberate batched refresh, not piecemeal.
16. **Get the IRB approval number and approving body** from the epi team into
    the Methods (W9).

**Deliberately not doing:** re-partitioning (Phase 2). It invalidates every
unit, r/m, distance table and tree, and W5 shows the headline does not depend on
the partition anyway. If the panel is expanded, do **Phase 1 only** — assemble,
QC, cgMLST, re-score — which invalidates nothing because cgMLST needs no unit
assignment.

---

## 8. One-paragraph abstract to write toward

> *Burkholderia pseudomallei* causes melioidosis across the tropics, and cases
> increasingly present where exposure location is unknown. We assembled 2,955
> genomes — 41% of all country-labelled public isolates — partitioned them into
> recombination-aware lineages, and tested whether exposure country can be
> recovered from the genome, using 46 isolates with independently documented
> exposure country as ground truth. Under a leave-group-out and
> leave-outbreak-out design that removes same-source references, **country-level
> attribution did not exceed chance — 10/46 (22%) against a 26% majority
> baseline, κ 0.19** — at every resolution tested, from 7 MLST loci to 4,221
> cgMLST loci to whole-genome recombination-filtered SNPs, while **regional
> attribution reached 41/46 (89%) against a 46% baseline, κ 0.83**. The contrast
> is sharpest where it should be easiest: among the 14 cases with a close
> relative in the panel, region was correct **14/14** and country **2/14**.
> Randomly subsampling 2 to 4,089 loci held country accuracy flat while regional
> accuracy rose from 50% to 82%, showing the failure is absence of signal rather
> than insufficient resolution. The boundary instead tracks reference
> availability: **for 7 of 16 exposure countries in our validation set, no public
> genome exists in ENA** — all seven in Latin America and the Caribbean — and the
> collection as a whole is inverted against disease burden: **South Asia carries
> 44% of predicted global cases and 2.5% of the genomes, while East Asia and the
> Pacific carries 39% and 92%**. We
> conclude that country-level genomic attribution for melioidosis is currently
> unachievable for most source countries by any method, that regional
> attribution is achievable only where the reference panel reaches, and that
> attribution systems should abstain rather than answer when no near relative
> exists.
