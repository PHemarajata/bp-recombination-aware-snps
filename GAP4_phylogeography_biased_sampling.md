# Gap 4: phylogeography under biased sampling

**Resolved 2026-08-09.** Companion to `SNP_STRATEGY_REVIEW_2026-08.md`, `HANDOFF_research_gaps.md`, `GAP1_reference_free_kmer_methods.md`, `GAP2_clustering_algorithms.md` and `GAP3_pipelines_and_scale.md`. Runnable diagnostics in `phylogeography_diagnostics_bp.py`.

Scope, from the handoff: discrete trait analysis versus structured coalescent under biased sampling and the De Maio / Kühnert / Lemey critiques; non-clock alternatives when date-randomisation fails; BactDating and TreeTime practice on recombination-corrected trees; population-genetic alternatives to trees (ChromoPainter/fineSTRUCTURE, DAPC, ADMIXTURE); and the per-replicon clock rates that the Gap 3 pass left unretrieved.

Sources read via PubMed Central, Europe PMC, journal full text, ENA and NCBI E-utilities, and the tools' own repositories, up to 2026-08-09.

**Method caveat, stated up front.** Several retrieval routes were blocked or throttled during this pass — PMC's direct supplementary-file endpoint returned an interstitial rather than the PDF, Europe PMC's supplementary-files endpoint returned an empty archive, bioRxiv returned HTTP 429 on two preprints, and the permission classifier intermittently blocked shell and subagent calls. Everything below is quoted from text that was actually read. Items that could not be reached by any route are listed together in §11 and are marked as unverified rather than as absent.

---

## The short version

**1. The strongest argument in this gap needs no model at all, and it is a comparison nobody in the *B. pseudomallei* literature has made.** Against Limmathurotsakul et al.'s burden model: **South Asia carries 44.2% of predicted global cases and holds 2.9% of the genomes; East Asia & Pacific carries 39.4% and holds 93.5%.** At country level it is far starker. Sampling intensity spans **35,852-fold**; **Australia is sequenced 1,877× more heavily per predicted case than India**; India carries the world's largest national burden (52,506 cases/yr) with 110 genomes; and **29 countries with over 100 predicted cases a year have zero genomes, together accounting for 33% of global predicted burden** — including Indonesia (20,038/yr, second in the world) and Nigeria (13,481/yr, third). "Country" here is not measuring where the organism is; it is measuring where sequencing happened, and across the top of the burden distribution the two are *inverted*. Arithmetic in `phylogeography_diagnostics_bp.py §F` and `§F2`.

**2. DTA is not defensible here, and the reason is structural rather than a matter of degree.** De Maio et al. state the mechanism exactly: in discrete trait analysis "**the relative sampling intensities of the demes are treated as data, informative about the migration parameters, even before any sequence data is analysed**," because the model assumes individuals are "sampled at random from demes **in proportion to their relative size**." So the test is not "how skewed is the sample?" — it is "**is the sample-count vector interpretable as an estimate of the relative population-size vector?**" For this collection the answer is unambiguously no. Their no-data experiment is the cleanest demonstration: given only sampling locations and **zero sequence data**, DTA returned a posterior migration log-ratio of **1.7 (SD 0.94)** against a prior mean of 0.0, while the structured coalescent methods correctly returned the prior.

**3. But the structured coalescent is not the alternative, and this is the finding that most changes the review's position.** Layan et al. 2023 is the only head-to-head DTA/BASTA/MASCOT/MASCOT-GLM benchmark across a graded bias ladder, and it does not endorse the structured coalescent: "**BASTA and MASCOT reconstructions were also biased when employing unbiased samples**," and "**CTMC outperforms BASTA and MASCOT when the sampling is representative**." Worse, the specific failure mode maps onto this dataset exactly: "BASTA and MASCOT **compensate for location under-representation by estimating high backward-in-time migration rates to the under-represented location**." With ~30 countries, most of them singletons or near-singletons, the structured coalescent would declare the singleton countries to be the drivers of global *B. pseudomallei* migration. That is a worse error than DTA's and much less likely to be caught by a reader.

**4. And it would not run anyway.** BASTA's likelihood is **O(N·S³)** for transition matrices and **O(N²·S²)** for partial likelihoods — cubic in demes, quadratic in sequences. Layan et al.'s verdict is quotable and decisive: "**More research and development are needed for datasets with a large number of locations (>15), and it currently seems unlikely that such analyses are possible at all with BASTA and MASCOT.**" Exact methods cap at "three or four" states. The largest true geographic structured-coalescent analysis in *any* bacterium is **260 *Vibrio cholerae* genomes across 11 demes**.

**5. The one intervention that did rescue inference under high bias is unavailable for this organism.** MASCOT-GLM won Layan's benchmark by informing deme sizes with **case-count time series**. Melioidosis has none — it is endemic, environmentally acquired and massively under-reported. Belman et al. hit precisely this wall for pneumococcus and abandoned the entire Bayesian phylogeographic family in response: "**Informing coalescent models with true case count data can reduce the impact of geographic sampling bias, but for an endemic, often asymptomatic pathogen this remains difficult.**"

**6. The defensible course is design-based — but balanced subsampling is a trade, not a free correction, and at this level of bias the trade may be bad.** Layan et al. endorse it, and Chewapreecha used it five years earlier: "**opt for an even sampling strategy across geographical locations** … or **compare the inferences over multiple subsamples**." But their endorsement is regime-qualified ("at intermediate sampling bias"), and the SAASI authors — who benchmarked `ace` and `simmap` directly — found that once you count the internal nodes downsampling deletes, "**the accuracy drops dramatically, and is substantially lower than reconstructions on the full tree**." Their breakpoint sits between 4× and 10× imbalance; this collection is at or past it. So subsample, stratify on **country × BioProject × year**, and report what the subsampling costs — but do not claim it removed the problem.

**7. Two corrections are cheap, implementable today, and better targeted than subsampling.** First, a **tip-state-swap permutation null** (the mechanism behind Gámbaro et al.'s adjusted Bayes factor): permute country labels across tips holding the tree fixed, re-run the mapping, and compare observed transition counts and root states against that null — then do it again permuting **BioProject** labels, which is the only handle anyone has on the study-of-origin confounder. Second, a **sampling-corrected root prior**: SAASI's own `simmap` baseline used `pi = (n_i/s_i)/Σ(n_j/s_j)` rather than the flat default, and §1's burden estimates supply the s_i. That is a one-line change targeting the exact failure mode that carries the Australian-origin claim.

**8. The price of that design on this collection is severe and should be stated in print.** At Chewapreecha's own n = 15 per country, the rule retains **225 of 5,515 genomes — 4.1% of the collection**, uses **0.4% of the Thai genomes**, and discards 22 countries entirely, including Papua New Guinea, Ghana, Madagascar and every South American country. A threshold of n = 100 is the better operating point on this collection: 8 countries, 800 genomes, 14.5%. Sweep in `phylogeography_diagnostics_bp.py §C`.

**9. Dateability cannot be triaged from cluster metadata, and this is a measured negative result rather than an impression.** Scoring Chewapreecha's own 20 clusters against their published dated/not-dated outcome, **every candidate predictor sits near AUC 0.5**: cluster size 0.35, ST count 0.35, sampling span 0.37, country count 0.45, isolates per year 0.47. Group 4 (span 8 years) and Group 7 (span 9) were dated; Group 3 (span 70), Group 1 (span 46) and the bin cluster (span 64) were not. Sampling window is if anything *anti*-correlated with success. Plan to test every cluster formally and expect most to fail — 5 of 19 in Chewapreecha, 1 of 10 sub-lineages in Seng. Arithmetic in `§D` and `§E`.

**10. The date-randomisation test is anticonservative under exactly this data structure, and the arithmetic lands on the documented failure threshold.** Murray et al. showed that where temporal and genetic structure are confounded — closely related sequences sampled at similar times, which is what an assembled multi-study collection guarantees — "over a third of the simulated data sets showed a high correlation between sampling date and root-to-tip distance" while giving a tMRCA of **51 years against a true 10,000**. They locate the danger zone at "fewer than **7** nucleotide substitutions per genome … during this entire sampling period." At the Pearson rate over the Wu core alignment this collection accumulates **0.647 substitutions per genome per year**, and §A's *effective* temporal span is **11.05 independent-year-equivalents** rather than the nominal 90 — giving **7.1 expected substitutions across the whole sampling window**. The collection sits on Murray's boundary, computed from metadata alone. Use **BETS** as the primary test instead: it is the only one that can *positively* support the absence of temporal signal, which is the finding this study is most likely to have.

**11. The reference study's own dating is materially weaker than the handoff records, and both corrections needed retrieving from figure panels.** The paper has **no supplementary tables at all** — the clock rates sit inside Supplementary Figure 6f and the date-randomisation ranks inside Supplementary Figure 5b, which is why earlier passes could not find them. Two corrections follow. The ranks are **percentiles**, so "34th" means the true R² fell *below 66% of randomised replicates* — a failure, not the p ≈ 0.03 the handoff assumed; **only Group 8 (92nd, 97th) approaches an acceptable result**, and Group 6 was dated on an R² of 0.0189. And the dated fraction is **59 of 469 isolates (12.6%), not 68 (14.5%)**, because only 9 of Group 19's 18 members were dated. The defensible summary is that **there is currently no well-supported molecular clock estimate for this organism outside chronic within-host infection.**

**12. Both *B. pseudomallei* dating precedents are thinner than they appear, and one contains a broken citation.** Seng et al. dated **17 isolates out of 1,391** (1.2%); their rate and TMRCA appear only inside a supplementary figure panel, and their 100-permutation date-randomisation test result **is never reported anywhere** — established by exhaustive search of the main text, the 12-page SI and the Peer Review File. Their stated rate prior cites reference [53], which resolves to **Spring-Pearson et al. 2015, a pangenome paper containing no clock analysis** (zero occurrences of "mutation rate", "molecular clock", "BEAST" or "per site per year"). Cite Pearson 2020 directly for the number; cite Seng only for the practice of importing one.

**13. The two in-organism rate sources disagree by 4–10×, and the epidemiological middle of the range is empty.** Chewapreecha's per-cluster rates run **6.26 × 10⁻⁷ to 1.81 × 10⁻⁶**; Pearson's within-host median is **1.7 × 10⁻⁷**. The ordering is not even monotonic in timescale. The deepest figure in the literature is not an estimate at all but a borrowed *E. coli* per-generation rate. And the two long-window outbreak studies most likely to supply an epidemiological rate — Chapple 2016 over 25 years and Webb 2020 over 51 — both report *absence* of temporal signal and decline to fit a clock. Any imported prior must therefore span better than an order of magnitude, and every date reported under it inherits that width.

**14. Tree-free methods are a complement, never a substitute, and each is degraded by this imbalance in a different, nameable way.** ChromoPainter/fineSTRUCTURE does scale to bacterial cohort size — **4,067 *H. pylori* genomes** in one published run, and **1,128 *Enterococcus faecium* genomes** in the best available template — and it recovers direction of gene flow that a tree structurally cannot. But Yahara's own caveat is the load-bearing one: "**Sampling bias will have strong effect on inference of population structure and admixtures.**" ADMIXTURE is worse: Lawson, van Dorp and Falush show unbalanced sampling changes both which group appears unadmixed and the inferred K, and that "**the problem is fundamental to any approach based on equally weighing samples**." And fastGEAR carries a silent trap — it cannot identify the direction of ancestral recombination and resolves ties by "always mark the lineage with fewer strains as the recipient," which on a 59.6%-Thailand dataset will mechanically declare Australia the recipient.

**15. The Australian-origin hypothesis is better supported than a naive sampling-bias critique implies, and still not established.** Pearson 2009 ran STRUCTURE on 601 STs from a near-balanced sample (**45% Australasia, 47% Southeast Asia**) and applied two explicit anti-bias checks. But the conclusion is, in their own words, "**contingent on an Australian root to this tree**," and Chewapreecha names an alternative she does not exclude: "**An alternative explanation is that there have been repeated population bottlenecks outside Australia, but not within it.**" That is exactly the recent-bottleneck-versus-admixture confound that Lawson et al. show is indistinguishable in a bar plot. **Searched for and not found: any paper that re-examines the Australian-origin hypothesis on sampling-bias grounds.** That is a genuine opening.

**16. Stochastic character mapping survives a dating failure, but one of its two outputs does not.** `make.simmap` requires only a `phylo` object — no ultrametric or time-calibrated tree — so it runs fine on a Gubbins-corrected substitution-scaled tree. But its `maps` and `mapped.edge` elements record "the **times** spent in each state" *in the tree's own branch-length units*. Chewapreecha reported both "the transitions between different geographical characters" and "the total time spent in each geographical character." **Transition counts and directions survive an undated tree; occupancy times do not** — on a substitution-scaled tree they become substitutions, confounding residence with lineage-specific rate. Separately, phytools is now **2.5-2** against Chewapreecha's **0.5-10**, its default model is `SYM` (their `ARD` was a deliberate override), and its documentation records a **root-node sampling error affecting user-supplied `pi` priors in "phytools 1.0-1 and probably prior recent versions."** Since the root state *is* the Australian-origin claim and the paper never reports `pi`, that warrants one re-run rather than an assumption.

---

## 1. The denominator — what "country" is actually measuring

This section is the one place in Gap 4 where the argument is settled by arithmetic rather than by weighing methods, and it should lead the write-up.

> Limmathurotsakul D, Golding N, Dance DAB, Messina JP, Pigott DM, Moyes CL, Rolim DB, Bertherat E, Day NPJ, Peacock SJ, Hay SI. "Predicted global distribution of *Burkholderia pseudomallei* and burden of melioidosis." *Nat Microbiol.* 2016;1:15008. PMID 26877885. [10.1038/nmicrobiol.2015.8](https://doi.org/10.1038/nmicrobiol.2015.8)

Read in full. The headline, verbatim from the abstract:

> "We estimate there to be 165,000 (95% credible interval 68,000–412,000) human melioidosis cases per year worldwide, of which 89,000 (36,000–227,000) die. Our estimates suggest that melioidosis is severely underreported in the 45 countries in which it is known to be endemic and that melioidosis is likely endemic in a further 34 countries which have never reported the disease."

And from the Results, the sentence that does the work:

> "We predict that only 40% of all melioidosis cases occur in the East Asia and Pacific region, where melioidosis is considered highly endemic. By contrast, South Asia is predicted to bear 44% of the overall burden, because large populations live in areas contaminated with *B. pseudomallei*."

Their Table 1, reproduced, against the genome audit mapped to the same World Bank regions:

| Region | Predicted cases/yr (thousands) | % of burden | Genomes | % of genomes | Genomes per 1,000 predicted cases |
|---|---|---|---|---|---|
| South Asia | 73 (31–171) | 44.2% | 162 | 2.9% | **2.2** |
| East Asia & Pacific | 65 (28–161) | 39.4% | 5,154 | 93.5% | **79.3** |
| Sub-Saharan Africa | 24 (8–72) | 14.5% | 17 | 0.3% | **0.7** |
| Latin America & Caribbean | 2 (1–7) | 1.2% | 61 | 1.1% | 30.5 |
| Middle East & North Africa | <1 | 0.3% | 6 | 0.1% | 12.0 |
| Europe & Central Asia | 0 | 0% | 28 | 0.5% | — |
| North America | 0 | 0% | 87 | 1.6% | — |
| **Global** | **165 (68–412)** | 100% | **5,515** | 100% | 33.4 |

Population at risk is **3,280 million (2,862–3,624)** and predicted deaths **89,000 (36,000–227,000)**, of which ">99% of all deaths due to melioidosis occur in low- and middle-income countries, and <1% in high-income countries including Australia, Brunei Darussalam and Singapore."

**Sampling intensity spans 112-fold across regions.** The region predicted to carry the largest single share of disease contributes 2.9% of the genomes; the region carrying 14.5% contributes 0.3%.

Two further points from the same paper that bear on how confidently this can be asserted. First, the model's own validation was reasonable — "high predictive performance of the BRT ensemble model with an area under the receiver operating characteristic curve of **0.81 (95% CrI 0.76–0.86)**" — and it was fitted to **22,338 geo-located occurrence records** spanning 1910–2014. Second, the authors state directly that reported case counts are not a usable denominator either: "Only Australia, Brunei Darussalam and Singapore have national surveillance data for melioidosis that are comparable to our estimates. Our estimates for other countries where melioidosis is known to be endemic were higher than reported."

**What this licenses in the write-up.** Not "the sampling is biased" — everyone says that. Rather: *the country label in this dataset is a proxy for national sequencing capacity, and it is anti-correlated with predicted disease burden across the two largest endemic regions.* Any model that reads country frequencies as informative about population sizes is therefore fitting the wrong latent variable, and the direction of the error is known in advance. That is a much stronger claim, and it is the premise §2 needs.

**One caveat, and it is not the one I first wrote.** The burden model predicts *human clinical cases*, so a clean comparison needs the genome side to be clinical too. **It is not.** §4.2a establishes that at least **856 genomes — about 15% of the entire global collection — are environmental isolates, all from a single Thai case-control study.** Removing them leaves roughly 2,558 clinical Thai genomes against 73,000 predicted South Asian cases represented by 162 genomes, so the direction and rough magnitude of the mismatch survive; but the comparison must be stated as clinical-plus-environmental, not as clinical.

That correction cuts in an interesting direction. A phylogeography of a soil saprophyte would ideally sample the *environmental* population, and this collection does contain the largest environmental panel available — but it is from one country, one study, and 93.6% of it is undated. So the collection is not a clinical sample with an environmental fringe; it is a clinical sample plus one large, geographically unreplicated environmental block. §7.6's recommendation to build **balanced regional environmental panels** follows directly: the Thai half of that comparison already exists.

### 1.1 The same comparison at country level, and it is far worse

Supplementary Information Table 1 was retrieved (publisher supplement `MOESM367_ESM`, page 11: "Predicted incidence and mortality of melioidosis in 2015, by countries"). *(A note for anyone retracing this: the NIH author-manuscript version of the supplement contains figures only. The table exists solely in the publisher version.)* Running it against the genome audit turns the regional argument into a much sharper one.

| Country | Genomes | Predicted cases/yr | Genomes per 1,000 cases | |
|---|---|---|---|---|
| Australia | 586 | 149 | **3,932.9** | |
| Hong Kong | 122 | 67 | 1,820.9 | * |
| Singapore | 184 | 276 | 666.7 | |
| **Thailand** | **3,414** | **7,572** | **450.9** | * |
| Malaysia | 161 | 1,752 | 91.9 | * |
| China | 403 | 7,174 | 56.2 | * |
| Vietnam | 158 | 10,430 | 15.1 | * |
| Sri Lanka | 18 | 1,881 | 9.6 | * |
| Madagascar | 4 | 880 | 4.5 | * |
| **India** | **110** | **52,506** | **2.1** | * |
| Bangladesh | 28 | 16,931 | 1.7 | * |
| **Philippines** | **1** | **9,116** | **0.1** | * |

*(\* = "endemic but under reported", the table's own footnote.)*

**Sampling intensity spans 35,852-fold across countries.** Per predicted case, **Australia is sampled 1,877× more heavily than India**, and Thailand 215× more heavily. India carries the largest predicted national burden on earth — **52,506 cases per year (95% CrI 22,335–124,652)** — and contributes 110 genomes.

**And the countries that are simply absent are the decisive part.** Twenty-nine countries with more than 100 predicted cases per year have **zero genomes** in the collection. Ranked by burden, the top of that list is:

| Country | Predicted cases/yr (95% CrI) | |
|---|---|---|
| **Indonesia** | **20,038 (7,859–52,812)** | * |
| **Nigeria** | **13,481 (4,839–38,348)** | * |
| Myanmar | 6,247 (2,513–15,400) | * |
| Cambodia | 2,083 (850–5,451) | * |
| Guinea | 1,372 (472–3,810) | † |
| Côte d'Ivoire | 1,144 (414–3,368) | * |
| Benin | 919 (348–2,580) | † |
| Nepal | 914 (317–2,354) | † |
| Brazil | 872 (273–2,905) | * |

*(† = "predicted to be endemic but never reported".)*

**Summed across every country with no genomes, the missing predicted burden is 54,076 cases per year — 33% of the global estimate.** Indonesia is the second-highest-burden country in the world for this organism and contributes nothing at all. So does Nigeria, third.

Two consequences the review should state plainly.

**First, this is not a bias that a model can absorb.** A discrete-trait state space in which the highest-burden states are *absent* and the lowest-burden states are *saturated* does not contain comparable observations. §2's mechanism — DTA reading state counts as relative deme sizes — is not merely mis-calibrated here; the mapping is inverted across the top of the burden distribution.

**Second, it sets a hard ceiling on what any phylogeographic claim from this collection can mean.** With a third of the world's predicted burden unrepresented, an inferred "origin" or "migration route" is a statement about the sampled subset, and every unsampled country is a candidate ghost deme in De Maio's sense (§2.4). Worth noting in passing that **Cambodia has zero genomes here yet was one of the six countries in Chewapreecha's n = 15 balanced design** — the sampling frame has not simply grown since 2017, it has shifted.

---

## 2. Discrete trait analysis under this skew

### 2.1 The mechanism, which is what to lead with

> De Maio N, Wu C-H, O'Reilly KM, Wilson D. "New routes to phylogeography: a Bayesian structured coalescent approximation." *PLoS Genet.* 2015;11(8):e1005421. PMID 26267488. [10.1371/journal.pgen.1005421](https://doi.org/10.1371/journal.pgen.1005421)

Read in full. The load-bearing passage:

> "There are some unusual consequences of the DTA modelling assumptions: (i) Demes can be lost, and they can be resurrected. (ii) **The relative sampling intensities of the demes are treated as data, informative about the migration parameters, even before any sequence data is analysed.** (iii) It is unclear what the relationship is between the effective population size parameter of the DTA and the vector of effective population sizes of the structured coalescent, hindering interpretation."

The model assumption behind (ii), verbatim: "Individuals are sampled at random from demes **in proportion to their relative size**." Contrast the structured coalescent: "Within demes, individuals are sampled at random. **However, no assumptions are made about the total sample size nor the relative sample sizes per deme.**"

And the authors' own statement of when DTA is and is not appropriate:

> "the DTA model inherits a set of assumptions appropriate for the independent mutation of loci within lineages, but **profoundly at odds with classical population genetics models of migration**"

> "the assumptions of DTA are well motivated when employed to analyse randomly sampled alleles or discrete phenotypes which evolve independently across individuals. But they are questionable when employed to analyse the migration of individuals between subpopulations, whose relative frequencies are maintained by external forces such as resource availability, and **for which the sampling frame might not be related to the relative sizes of the subpopulations**."

**The criterion this gives you is sharper than a skew threshold.** It is not "how unbalanced is the sample?" but "is the sample-count vector interpretable as an estimate of the relative population-size vector?" §1 answers that question definitively for this dataset: the counts are anti-correlated with predicted burden across the two largest endemic regions.

### 2.2 The no-data experiment

The cleanest result in the paper. Datasets containing **only the 200 sampling locations, with no genetic information at all**, were analysed. A method robust to sampling must return the prior.

> "We found that for DTA the posterior distribution was substantially different to the prior, exhibiting a bias that depended on sampling, and a reduction in parameter uncertainty, unlike the structured coalescent methods (MTT and BASTA). Particularly with high migration rates DTA posteriors showed large biases (**posterior median of rates log-ratio 1.7 with standard deviation 0.94**), indicating that the sampling strategy significantly influenced the result. The posterior distributions for MTT and BASTA were unbiased, centred on the prior mean of 0.0."

A prior mean of 0.0 becoming a posterior median of 1.7 is a ~5.5-fold spurious migration asymmetry inferred from sample counts alone.

There is a second consequence that matters at ~30 countries:

> "Even when migration rates were low DTA substantially over-estimated them… the DTA model expects that, at low migration rates, one subpopulation will drift to high frequency, and that samples are collected proportionally to subpopulation size, so a random sample would be unlikely to capture multiple locations. The presence of multiple locations therefore suggests to DTA an appreciable migration rate."

So DTA on this collection will infer non-trivial inter-country migration **merely because thirty-odd countries appear in the tip labels**, before a single SNP is read.

### 2.3 What the simulations actually show — and a correction to how they are usually cited

This needs stating carefully, because the paper is routinely over-claimed.

**Only one biased ratio was tested**: 10 / 190 (1:19) in a two-deme model. There is **no dose–response curve over sampling skew in De Maio 2015**. Table 1, fixed tree, 100 replicates:

| Sampling | Rate | Method | Calibration (target 0.95) | Correlation | RMSE |
|---|---|---|---|---|---|
| Even (100/100) | Fast | DTA | 0.56 | 0.58 | 1.83 |
| | | BASTA | 0.95 | 0.83 | 1.51 |
| Uneven (10/190) | Fast | DTA | 0.68 | **0.33** | 1.79 |
| | | MTT | 0.80 | 0.46 | **2.50** |
| | | BASTA | 0.84 | 0.70 | 2.08 |
| Uneven (10/190) | Slow | DTA | 0.80 | **0.39** | 1.73 |
| | | BASTA | 0.88 | 0.51 | 2.29 |

> "The 95% credibility intervals were not well calibrated, including the true parameter between **56%–81%** of the time, compared to **80%–96%** for MTT, **84%–97%** for BASTA, and the theoretical target of 95%."

Root-state accuracy under **even** sampling: "**54% for DTA**, compared to **68% for MTT** and **77% for BASTA**."

**Read the table carefully before quoting it.** Uneven sampling degrades all three methods, and under uneven sampling MTT and BASTA have *higher* RMSE than DTA (2.50 and 2.08 versus 1.79). What skew destroys specifically is DTA's **correlation** with truth — 0.58 → 0.33 fast, 0.64 → 0.39 slow — i.e. its ability to rank migration rates, while its intervals stay spuriously narrow. The honest claim is "under 1:19 skew DTA's point estimates become nearly uninformative about the true rate ordering while remaining over-confident." The honest claim is **not** "DTA's error blows up while the structured coalescent stays accurate."

### 2.4 Over-confidence in ancestral states, and the Ebola case

On real data (avian influenza, 5–10 host classes; TYLCV, 8 locations):

> "DTA reported posterior probabilities above 90% for ancestral reconstruction of most subpopulations (**135 out of 145** internal nodes … and **all 132** …), even deep within the tree. In contrast, BASTA placed high confidence … only for internal nodes close to samples (**63 out of 145** … and **61 out of 132**)."

The Ebola analysis is the most-cited result and deserves its caveat. With the animal reservoir as an unsampled ghost deme, BASTA inferred the human outbreaks were seeded by zoonosis with the MRCA in the reservoir at 100% posterior; DTA inferred **no zoonotic transmission at all**, also at 100% posterior probability, implying four decades of undetected human-to-human persistence.

> "They demonstrate the possibility of obtaining implausible results with DTA, which may be accompanied by high posterior probabilities… it demonstrates the potential to produce highly misleading inference **when independent epidemiological understanding is scarce**."

**Caveat:** this is a 100%-versus-0% ghost-deme scenario, not graded skew, and ghost demes are a known weakness of the structured coalescent too. Cite it for the *shape* of the failure — confident attribution of persistence to the densely sampled compartment rather than the unsampled reservoir — not as a general performance comparison. That shape does map onto *B. pseudomallei* uncomfortably well: a clinical collection with a genuinely unsampled environmental compartment, and Nandi's estimate that ~7% of every genome arrives from an unsampled source.

### 2.5 Does the GLM extension rescue DTA? Searched for, and unanswered

> Lemey P, Rambaut A, Bedford T, Faria N, Bielejec F, Baele G, Russell CA, Smith DJ, Pybus OG, Brockmann D, Suchard MA. "Unifying viral genetics and human transportation data to predict the global transmission dynamics of human influenza H3N2." *PLoS Pathog.* 2014;10(2):e1003932. PMID 24586153. [10.1371/journal.ppat.1003932](https://doi.org/10.1371/journal.ppat.1003932)

The GLM extension parameterises the **migration rate matrix** as a log-linear function of covariates such as air passenger flow. It **does not change the DTA likelihood's treatment of tip locations**. The structural defect De Maio identifies is untouched.

Note also a practice worth flagging: sample size per location is commonly included as a GLM predictor precisely to absorb sampling-intensity effects. That is nuisance-covariate mitigation, not a correction of the generative model, and it competes for signal with the substantive predictors.

**A controlled benchmark of GLM-DTA under sampling bias was searched for and not found.** Layan et al. benchmarked MASCOT-**GLM**, which is the structured-coalescent side; they say explicitly of the CTMC analogue, "a similar approach is available under the CTMC framework, but **we did not test it here**." Report as unanswered. Do not claim the GLM extension fixes it.

The travel-history extension (Lemey et al. 2020) is better evidenced but requires individual travel records, which do not exist for an environmentally acquired organism.

---

## 3. The structured coalescent is not the alternative

This is the section that most changes the review's position, because the obvious move after §2 — "so use MASCOT or BASTA" — is not supported.

### 3.1 The decisive benchmark

> Layan M, Müller NF, Dellicour S, De Maio N, Bourhy H, Cauchemez S, Baele G. "Impact and mitigation of sampling bias to determine viral spread: Evaluating discrete phylogeography through CTMC modeling and structured coalescent model approximations." *Virus Evol.* 2023;9(1):vead010. PMID 36860641. [10.1093/ve/vead010](https://doi.org/10.1093/ve/vead010)

Read in full. This is the only head-to-head DTA / BASTA / MASCOT / MASCOT-GLM comparison across a graded bias ladder, and it uses an epidemiologically realistic simulator (a stochastic metapopulation model of dog rabies in Morocco) rather than simulating under the inference model. 50 simulated epidemics, 3- and 7-deme frameworks, 150 or 500 sequences, over-sampling weights of **2.5, 5, 10, 20 and 50**; 8,800 XML files, ~1,500 CPU-hours.

From the abstract:

> "**While the reconstructed spatiotemporal histories were impacted by sampling bias for the three approaches, BASTA and MASCOT reconstructions were also biased when employing unbiased samples.**"

> "Overall, **CTMC outperforms BASTA and MASCOT when the sampling is representative** of the true underlying transmission process, as BASTA and MASCOT only recover the location of the ancestral nodes and not individual migration events."

DTA's failure mode is over-confidence rather than inaccuracy: "the **correlation and the calibration drop rapidly with increasing levels of sampling bias**… Nevertheless, the WIS and the MRB remain smaller than those of BASTA and MASCOT, even at high levels of bias. Consequently, CTMC leads to median estimates that are closer to the true values **but with 95 per cent HPDs that are too narrow**." BASTA and MASCOT are "less confident with an average **95 per cent HPD width that is ten to thirty times higher**."

### 3.2 The failure mode that lands directly on this dataset

> "As we have set equal deme sizes in BASTA and MASCOT, but a single tip is sampled for Oriental Mindoro in the RABV dataset and for Africa in the SARS-CoV-2 dataset, **BASTA and MASCOT compensate for location under-representation by estimating high backward-in-time migration rates to the under-represented location**."

> "we show on real datasets that **singletons may be inferred as drivers of the migration process in an unparsimonious way by structured coalescent model approximations**."

> "although the structured coalescent model, in principle, allows us to mitigate sampling biases, **it can itself be highly biased when wrong population dynamics are assumed**."

The audit contains Guadeloupe (1), Philippines (1), Ecuador (4), Madagascar (4), Japan (4), New Zealand (4), South Africa (4), and a long tail at 2. A structured-coalescent run over country demes on this collection is predicted, by the best available benchmark, to make those the migration hubs. That is a worse error than DTA's, and a reader is far less likely to catch it.

### 3.3 The deme ceiling and the scaling

Layan et al., verbatim, and this is the sentence to quote:

> "It is difficult to generalize our results in regard to the number of demes… While a scenario with three demes was doable, the one with seven demes turned out to be difficult to analyze, notably due to computational burden. **More research and development are needed for datasets with a large number of locations (>15), and it currently seems unlikely that such analyses are possible at all with BASTA and MASCOT.**"

Supporting detail from the same paper: "**BASTA unfortunately proved impractical** to infer such histories from large samples of 500 sequences in the seven demes framework as a result of **extremely high calculation times**"; "we removed **26 per cent of the MASCOT chains** on the large samples of 500 sequences in the seven demes framework **due to convergence issues**"; and "all demes were set to have an equal size due to numerical issues, leading to a computational time of **over 70 hours per million iterations**."

The exact complexity, from the BEAGLE parallelisation work (Shao Y, Suchard MA, Rambaut A, Ji X, Lemey P, Vasylyeva TI, Baele G, bioRxiv 2025, [10.1101/2025.09.22.677844](https://doi.org/10.1101/2025.09.22.677844), PMID 41040339):

> "The BASTA likelihood scales **cubically with deme count and quadratically with sequence count** due to matrix exponentiation and pairwise coalescent probability calculations."

> "the computation of the transition matrices operates at 𝒪(N·S³), the evaluation of the partial likelihood vectors … is 𝒪(N²·S²)"

For exact methods the ceiling is lower still. The MASCOT authors: "As the number of different states is increased, convergence of the MCMC chains becomes a severe issue… **This essentially limits the number of different states that can be accounted for to three or four.**"

Parameter counts alone make the point. For *d* demes there are *d*(*d*−1) asymmetric migration rates plus *d* population sizes: at 10 countries that is 100 free parameters, at 30 countries **900**.

### 3.4 Bacteria: a near-absence

Searched hard. The complete list found:

| Study | Organism | Method | n | Demes | Deme meaning |
|---|---|---|---|---|---|
| Roberts, Everitt, Koskela, Didelot 2025 (PLoS Comput Biol 21(4):e1012995, PMID 40258093) | *S. aureus* ST239 | exact structured coalescent | 58 | 5 | continents |
| same | *V. cholerae* 7th pandemic | exact structured coalescent | **260** | **11** | locations |
| Duault et al. 2022 (Vet Res 53:28, PMID 35366933) | *M. bovis* SB0821 | MASCOT | 167 | 2 | **host species** |
| De Maio et al. 2016 (SCOTTI, PMID 27681228) | *K. pneumoniae* | structured coalescent | outbreak | tens | **individual hosts** |
| Pečerska et al. 2021 (PMID 34256273) | *M. tuberculosis* L4 | MTBD | — | 2 | **drug resistance** |

The largest true *geographic* bacterial application is 260 genomes across 11 demes. Roberts et al. state their own ceiling: "We appear to be **approaching the performance limit of our method with 48 hours of run time and phylogenies consisting of 1000 samples around 7 demes**."

**Searched for and not found: any application of the structured coalescent (MASCOT, BASTA, MultiTypeTree, SCOTTI, bdmm) to *B. pseudomallei*.**

### 3.5 The most telling precedent — what large bacterial phylogeography actually does

> Belman S, Pesonen H, Croucher NJ, Bentley SD, Corander J. "Estimating between-country migration in pneumococcal populations." *G3.* 2024;14(6):jkae058. PMID 38507601. [10.1093/g3journal/jkae058](https://doi.org/10.1093/g3journal/jkae058)

The closest published analogue to the target study: a large, multi-country, recombinogenic bacterial dataset asking a between-country migration question. 12,582 genomes reduced to 2,746 across 6 GPSC lineages and 4 African countries; Gubbins-masked; **cluster-first, analyse-per-lineage — the same architecture as this pipeline.**

They used **neither DTA nor the structured coalescent**. They used Approximate Bayesian Computation with Bayesian Optimization for Likelihood-Free Inference over `msprime` simulations. Their reasoning, verbatim:

> "**Variable sampling strategies between countries, poor approximation of between-country mobility, and the large time scales of between-country pathogen spread can hinder definitive estimates.**"

> "**Informing coalescent models with true case count data can reduce the impact of geographic sampling bias, but for an endemic, often asymptomatic pathogen this remains difficult.**"

> "Due to the lack of direct observations of between-country migration, **we are unable to use typical Bayesian techniques.**"

That middle quote is what closes off MASCOT-GLM for *B. pseudomallei*. MASCOT-GLM was Layan's winning intervention precisely because reliable case counts inform deme sizes; §1 establishes that melioidosis case counts are not merely unreliable but anti-correlated with sampling. Belman et al. hit the identical wall for a better-surveilled organism and abandoned the family.

### 3.6 Multi-type birth–death, for completeness

> Kühnert D, Stadler T, Vaughan TG, Drummond AJ. "Phylodynamics with migration: a computational framework to quantify population structure from genomic data." *Mol Biol Evol.* 2016;33(8):2102–2116. PMID 27189573

*(The handoff's guess of* J R Soc Interface *is wrong; it is MBE 2016.)*

MTBD is theoretically the most attractive of the three families because it is the only one with an **explicit, type-specific, time-varying sampling parameter** (ψᵢ,ₖ and ρᵢ) in the generative model — it does not assume sampling proportional to deme size. Four reasons it is nonetheless not an option:

1. **Deme ceiling is the worst of the three.** Verbatim: "at least for small numbers (**two or three**) of subpopulations and medium-sized samples."
2. **Tip ceiling.** Originally "up to approximately **250** genetic samples"; after Scire et al. 2022 (Viruses 14(8):1648, PMID 36016270), demonstrated at **500**.
3. **Identifiability.** Sampling proportion, removal rate and birth rate are jointly identifiable only under constraints, so ρᵢ must be fixed per deme from external knowledge. For an environmental organism with no per-country incidence denominator, there is no defensible way to fix ρ_Thailand versus ρ_Australia — the same wall as MASCOT-GLM.
4. **Model mismatch.** Birth = transmission, death = recovery. Melioidosis is acquired from soil, not transmitted person to person. The parameterisation has no epidemiological interpretation at country scale.

### 3.7 One sampling-aware method that would actually run

> Song Y, Gill I, MacPherson A, Colijn C. "SAASI: Sampling Aware Ancestral State Inference." *Nat Commun.* 2026;17(1). PMID 42115598. [10.1038/s41467-026-72851-5](https://doi.org/10.1038/s41467-026-72851-5)

> "In phylogeography, ancestral state inference methods are used to identify the geographic or host species origin of **viral or bacterial lineages**… However, **differences in sampling among states can bias these inference methods.** Here, we introduce sampling-aware ancestral state inference (SAASI), a method that accounts for sampling differences."

> "SAASI infers past viral locations/host species **considerably more accurately than standard methods when sampling bias exists**, is computationally feasible for large datasets, and **scales to trees with 100,000 tips.**"

This is the only method found that explicitly corrects for per-state sampling differences, is validated at this tip count, and is framed as applying to bacteria. It operates on a **fixed tree**, which fits a cluster-then-Gubbins-then-per-cluster-tree design well. Worth evaluating; note it is new, and no bacterial application beyond the authors' framing was found.

---

## 4. What is actually defensible

Ranked by strength of evidence.

**A caveat that must come before the ranked list, because it cuts against the obvious recommendation.** Balanced subsampling is well evidenced *for discrete-trait migration-count estimands at intermediate bias*, and it is **not** a free correction for ancestral-state reconstruction at high bias. The SAASI authors benchmarked `ace` and `simmap` directly against known sampling bias and found:

> "Supplementary Fig. and Supplementary Table explore the practice of downsampling data to obtain approximately uniform sampling. Under high sampling bias, downsampling achieves high accuracy when evaluated only on preserved nodes… However, **if we account for a lack of inference on all internal nodes that are removed…, the accuracy drops dramatically, and is substantially lower than reconstructions on the full tree**… Similar patterns arise under moderate sampling bias…, where downsampling reduces accuracy when missing transition events are considered."

So equal-*n* subsampling buys unbiased inference on the nodes you keep at the cost of no inference at all on the nodes you delete, and the net can be worse than not subsampling. Note too that Layan's own endorsement is regime-qualified — "alternative sampling strategies that maximize the spatiotemporal coverage greatly improved the inference **at intermediate sampling bias**."

**Where this collection sits.** SAASI's simulations put the breakpoint between 4× and 10×: "Under high sampling bias (= 10 …) … ace incorrectly infers approximately half of the internal node states (≈ 0.5) and **misidentifies the root state as** [the over-sampled state]", whereas at 4× "all methods have high accuracy." Thailand:Australia is ≈5.8×, but the study-level imbalance inside Thailand is far larger — one nine-hospital study is 37% of Thai genomes. **This collection is at or past the regime where `ace` and `simmap` fail on root state.**

And the direction of the failure is specific: "if state [i] is far less sampled than state [j], ace **overestimates the transition rates from other states to state [i]** and underestimates transition rates from state [i] to other states." Australia is the under-sampled state here, so **transition rates *into* Australia will be inflated and rates *out of* Australia deflated.** Any conclusion of the form "lineages moved from Southeast Asia into Australia" is precisely what this bias manufactures — which is the mirror image of the Australian-origin claim and needs saying in §8's terms.

So the list below stands, but read "subsample" as "subsample, report the loss, and do not treat it as having removed the problem."

**1. Balanced subsampling across strata, repeated, reported as a distribution over resamples.** Still the best-evidenced intervention *for migration counts at intermediate bias*, with the caveat above.

- Layan 2023: "subsampling strategies that **maximize the spatial or spatiotemporal coverage considerably improve** the inference of the geographical spread by the CTMC"; and the bottom line, "Whenever possible, we would advise to **opt for an even sampling strategy across geographical locations**, compare the inferences of the different approaches, or **compare the inferences over multiple subsamples** when analyzing real datasets."
- Kalkauskas A, Perron U, Sun Y, Goldman N, Baele G, Guindon S, De Maio N. "Sampling bias and model choice in continuous phylogeography: getting lost on a random walk." *PLoS Comput Biol.* 2021;17(1):e1008561. PMID 33406072. *(Note: the handoff's guess of* Phil Trans R Soc B *is wrong.)* This contains the only published dose–response curve for sampling bias in phylogeography: "at **75% bias intensity already a large part of the inference bias already disappears**." Catastrophe is concentrated at ~100% one-sided sampling, and even modest admixture of under-sampled regions recovers most of the inference.
- Layan 2023 again, on cost: "inference accuracy **rapidly plateaus when using up to 25–50 per cent of the sequence data available**." Subsampling is cheap in information terms.

**This is exactly what Chewapreecha et al. did in 2017**, five years before Layan validated it. Reframe it as endorsed rather than pragmatic. Their Methods, verbatim:

> "To avoid sampling bias, we sub-sampled the phylogeny so that there were **equal numbers of isolates from Thailand, Laos, Cambodia, Vietnam, Malaysia and Singapore (n = 15 for each country), and resampled 1,000 times.** Countries containing less than 15 isolates were excluded… For each sub-sampled tree, we used stochastic character mapping … under an asymmetric model of character change for 1,000 simulations."

Note the scope honestly: that subsampling covered **6 countries at n = 15**, not all 30, and it was applied to the stochastic mapping only — not to the root-position argument, which was read off branch lengths and tree topology.

**2. Stratify by BioProject and year, not by country alone.** Nothing in the literature addresses within-country study-block clustering directly — searched for and not found. The closest analogue is Kalkauskas et al.'s yellow-fever result, where capping per-location counts at 2 **moved the inferred outbreak origin**: "after downsampling, the origin of the outbreak is not inferred anymore to be solely nearby Teófilo Otoni, but also possibly south, close to another cluster of samples near Caratinga." Given that ~37% of Thai genomes come from one nine-hospital study over four years, this is the same hazard one level down.

**3. Report a sampling-aware method alongside.** Layan: "compare the inferences of the different approaches." SAASI (§3.7) is the candidate that runs at this scale.

**4. Report an adjusted Bayes factor if reporting DTA support.** Gámbaro F, Layan M, Baele G, Vrancken B, Dellicour S. "Navigating sampling bias in discrete phylogeographic analysis: assessing the performance of an adjusted Bayes factor." *Mol Biol Evol.* 2025;42(11):msaf253. [10.1093/molbev/msaf253](https://doi.org/10.1093/molbev/msaf253). BF_adj "incorporates information on the relative abundance of samples by location… without requiring additional data." With the authors' own caveats: it "results in less FP but also fewer TP and more FN," and at the highest bias weight the true positives detected "**drops substantially**."

**5. Do not claim GLM-DTA fixes it** (§2.5). **Do not present MASCOT/BASTA as the rigorous alternative at this scale** (§3.1–3.4).

### 4.1 The price of the design, measured

`phylogeography_diagnostics_bp.py §C` sweeps Chewapreecha's rule across this collection:

| n per country | Countries kept | Genomes used | % of collection | % of Thai genomes used |
|---|---|---|---|---|
| 5 | 23 | 115 | 2.09% | 0.15% |
| 10 | 19 | 190 | 3.45% | 0.29% |
| **15** (Chewapreecha) | **15** | **225** | **4.08%** | **0.44%** |
| 20 | 14 | 280 | 5.08% | 0.59% |
| 50 | 9 | 450 | 8.16% | 1.46% |
| **100** | **8** | **800** | **14.51%** | **2.93%** |
| 150 | 6 | 900 | 16.32% | 4.39% |
| 200 | 3 | 600 | 10.88% | 5.86% |

At n = 15 the rule discards 22 countries entirely — 107 genomes including Papua New Guinea (14), Ghana (9), Madagascar (4), South Africa (4), Ecuador (4) and every remaining South American entry. **The design buys an unbiased comparison among the survivors at the price of saying nothing at all about anywhere else, and the write-up must say so rather than letting a map imply global coverage.**

**n = 100 is the better operating point on this collection**: 8 countries, 800 genomes, 14.5% of the collection, and it keeps India and the USA in. It is a departure from Chewapreecha's number, so justify it as a sample-size-driven choice rather than citing her for it.

### 4.1a Two cheap corrections that are directly implementable, and one contraindication

**The permutation null — the single most implementable recommendation in this document.** Gámbaro et al.'s BF_adj works by replacing the fixed combinatorial prior with an empirical, abundance-aware one derived from a **tip-state-swap null**: permute the observed tip locations, holding topology and branch lengths fixed, and measure how much apparent transition support arises from sampling composition alone. Their standard prior, verbatim, "does not account for their relative abundances (i.e. their sampling intensity)."

That null is portable straight into a non-Bayesian phytools pipeline and costs nothing but compute. Permute country labels across tips, re-run `make.simmap`, and compare observed transition counts and root-state frequencies against the permutation distribution. **Permute BioProject labels the same way**, which is the only handle found anywhere on the study-of-origin confounder (§4.4). This answers "is this phylogeographic signal distinguishable from the sampling composition?" using tools already in the pipeline.

**A sampling-corrected root prior.** SAASI's own `simmap` baseline was not run with the default flat prior — verbatim, they set "the root prior to π_i = (n_i/s_i)/∑(n_j/s_j)", where n_i is the number of taxa in state *i* and s_i its relative sampling intensity. That is a one-line change in phytools: pass `pi = normalise(n_i / s_i)` instead of `pi="equal"`. It needs an external estimate of s_i — and **§1 supplies exactly that**, in the form of predicted burden per region. It does not fix the transition-rate bias, but it targets the root-state failure mode directly, which is the one that carries the Australian-origin claim.

**A contraindication: do not use Treemmer for the phylogeographic subsample.** Treemmer prunes to maximise retained relative tree length, and its authors state the limitation plainly:

> "it should not be considered as a random unbiased sample: **the number of leaves belonging to different clades in the reduced dataset depends on the genetic diversity of the different clades and not on the abundance of different clades in nature**; highly diverse clades will be represented by more leaves than less diverse ones, irrespectively of the frequency of such clades in natural populations."

A discrete-trait reconstruction is a frequency-based inference — the Mk likelihood is driven by tip-state counts — so a diversity-proportional sample substitutes one wrong sampling model for another. Treemmer remains appropriate for making a tree computationally tractable and for the Verticall use case recorded in the handoff; it is not a phylogeographic sampling fix, and the Treemmer authors say so. *(Its `-lm`/`-pm` metadata options are, however, the only tool-level hook found for constraining pruning by study of origin.)*

### 4.2 The effective sampling frame, measured

`§A` computes Hill numbers on the country distribution. **37 distinct country labels collapse to 4.83 effective countries at q = 1 and 2.48 at q = 2** (Pielou evenness 0.436). A phylogeographic model given 37 discrete states would be estimating on the order of 1,332 pairwise migration rates from what is effectively a 2.5-state dataset.

On years: 3,539 dated genomes (61.8%), 48 distinct years, but **18.34 effective years at q = 1 and 11.05 at q = 2** against a nominal span of 90 years. Root-to-tip regression is driven by the effective span, not the nominal one.

On BioProject pseudo-replication, the Kish design effect with the Seng collection treated as one cluster against singleton remainder — a deliberately conservative floor:

| Assumed ICC | Design effect | Effective n | % of nominal |
|---|---|---|---|
| 0.01 | 3.89 | 1,416 | 25.7% |
| 0.05 | 15.47 | 356 | 6.5% |
| 0.10 | 29.95 | 184 | 3.3% |
| 0.25 | 73.37 | 75 | 1.4% |

The intra-cluster correlation is not measurable from the audit table, but it **is** measurable from your own data as the fraction of core-SNP variance falling between rather than within BioProjects. Until it is measured, quote the range. Even the most generous value cuts the effective sample size by a factor of four.

### 4.2a The three dominant BioProjects, resolved — and the largest is a case-control study

The handoff recorded "81% of Thai genomes from three BioProjects" with only two identified. **All three are now identified.** The reason it stayed open is mundane: the original audit script never retained `assembly_info.bioproject_accession`. Re-running the same NCBI Datasets query with that field kept, on the same 5,728 assemblies:

| BioProject | Assemblies | % of Thai | % of collection |
|---|---|---|---|
| **PRJEB3409** | **1,506** | **44.1%** | **26.3%** |
| PRJEB25606 | 682 | 20.0% | 11.9% |
| PRJEB35787 | 582 | 17.0% | 10.2% |
| **Three combined** | **2,770** | **81.1%** | — |

The 81% figure reproduces exactly. **The missing project, PRJEB3409, is the single largest contributor to the entire global collection** — bigger than both Seng projects together. Its ENA record reads "**Burkholderia_pseudomallei___case_control_study_**", Wellcome Sanger Institute, first public 2014-11-26.

Three properties make it more consequential than a large block of genomes would ordinarily be:

- **It is a case-control design.** Isolates were selected by outcome, not sampled at random from a population. That is a stronger and more specific form of ascertainment bias than the convenience sampling the review has been arguing about, and STROME-ID item 9.1 asks about it by name.
- **It is majority environmental.** Host is `environmental` for 760 and `environment` for 96 — **856 of 1,506 (56.9%)** — against 650 (43.2%) `Homo sapiens`. So the case-control axis is clinical versus environmental, and ~15% of the whole global collection is environmental isolates from this one study.
- **It is 93.6% undated.** 1,410 of 1,506 have no collection date; the 96 that do run 2010–2012. **It alone supplies 1,410 of the 1,554 undated Thai genomes — 91% of them.** ENA records its date as the placeholder range "1800/2014", which is worth knowing because a naive `date[:4]` parse would silently read that as the year 1800.

**The consequence for dating is sharper than the raw percentages suggest.** Of the 3,414 Thai genomes, 1,554 are undated, leaving 1,860 dated — and **1,264 of those 1,860 (68%) are Seng et al., nine hospitals over four years.** So the dated Thai signal is essentially one hospital network in one window. That is textbook confounding of temporal and genetic structure in Murray et al.'s sense (§6.2), and it is the concrete mechanism behind §A's finding that the effective temporal span is 11 years rather than the nominal 90.

`phylogeography_diagnostics_bp.py §A` now uses PRJEB3409 as the dominant cluster in the design-effect calculation. That raises the design effect relative to the earlier Seng-based figure: at ICC 0.05 the effective *n* is **256, or 4.6% of nominal**, and at ICC 0.10 it is 131.

### 4.2b Study of origin is the dominant unaddressed confounder, and the field has no machinery for it

**Searched for and not found: any bacterial-genomics paper that models study of origin or BioProject accession as a random effect, a blocking factor, or a stratification variable in a phylogeographic analysis.** Multiple query formulations across PubMed and web search. In this literature the unit of non-independence is always the clade or the species — never the deposition batch.

That absence is worth stating because the problem is documented even though the correction is not:

- **Blackwell GA, et al. 2021** (*PLoS Biol* 19(11):e3001421, PMID 34752446), across 661,405 ENA genomes: "**50% of the data originating from 50 sequencing projects**" out of 23,316, and "**the enormous contribution of just a few projects shows that even the drive and focus of individual groups has influenced our view of recent bacterial diversity**." The over-represented species "tend to be acute/common human pathogens, aligning with research priorities."
- **Yu Y, Wheeler NE, Barquist L 2025** (*PLoS Biol* 23:e3003539, PMID 41401143): "bacterial populations are highly structured, and **sampling is biased towards human disease isolates, violating ML assumptions of independence between samples**… we show the resulting ML models perform poorly and that **increasing the training sample size fails to rescue performance**." Their proposed remedy — clade-held-out cross-validation and "lineage-aware algorithms that explicitly model the hierarchical structure" — is the closest analogue, but keyed to clade rather than to study.

**The two handles that do exist**, both noted above: the tip-state-swap permutation applied to BioProject labels (§4.1a), and Treemmer's `-lm`/`-pm` metadata options for constraining pruning by study or geography (§4.1a). Nothing else was found.

**On effective sample size, the concept has not been ported to this field.** Phylogenetic effective sample size is formalised for **continuous** traits under Brownian-motion and Ornstein–Uhlenbeck models (Ané 2008, *Ann Appl Stat* 2(3):1078–1102; Bartoszek 2016, *J Theor Biol*, PMID 27343033), and bacterial GWAS has an effective number of independent *tests* via pyseer's unique-variant-pattern count (Lees et al. 2018, PMID 30535304) — the right idea on the wrong axis. **Searched for and not found: any phylogenetic effective sample size for a discrete trait under an Mk/CTMC model; any "effective number of independent isolates" for a clustered pathogen collection; any application of design effect or intraclass correlation to pathogen genomic data; and any published justification for the near-universal one-isolate-per-patient deduplication convention.** §4.2's Kish calculation is therefore an ad hoc descriptive statistic and must be labelled as one — which the script does.

### 4.2c Reporting standards, and the sanity check that has no precedent

**STROME-ID is the only reporting guideline that bites here** (Field N, Cohen T, Struelens MJ, et al., *Lancet Infect Dis* 2014;14(4):341–352, PMID 24631223). Five items apply directly, verbatim:

| Item | Text |
|---|---|
| **6.1** | "state the source of participants and clinical specimens, and **clearly describe sampling frame and strategy**" |
| **9.1** | "describe any efforts made to address **discovery or ascertainment bias**" |
| **12.1** | "state how the study took account of the **non-independence of sample data**, if appropriate" |
| **12.2** | "state how the study dealt with **missing data**" |
| **13.2** | "if the study investigates groups of genetically indistinguishable pathogens (molecular clusters), state the **sampling fraction**, the distribution of cluster sizes, and the study population turnover, if known" |

**Item 13.2 is the one that bites hardest.** A per-cluster analysis of 61–101 clusters is exactly "a study [that] investigates groups of genetically indistinguishable pathogens," and it demands the sampling fraction and the cluster-size distribution — the very numbers that expose a 1,265-isolate hospital-network study. `cluster_diagnostics_bp.py` from Gap 2 already computes the size distribution, and §4.2 here supplies the fraction.

Compliance is poor and did not improve after publication: across 114 tuberculosis genomic-epidemiology papers, "the proportion of applicable STROME-ID criteria fulfilled … ranged from 16% to 75% (mean 50% [SD 12])" and "was similar before and after STROME-ID publication (51% … 46%, p=0.26)" (Cheng B, et al., *Lancet Microbe* 2021;2(3):e115–e129, PMID 33842904). **Reporting these items explicitly would put the paper in a small minority.**

**And the field says the protocol this review wants does not exist.** Two authoritative reviews, four years apart. Featherstone LA, et al. 2022 (*Virus Evol* 8(1):veac045, PMID 35775026): "**protocols are required to address when and how to subsample from a large database. Methods are emerging to meet this need, but many questions remain**… **How should one subsample sequences from individual countries to infer travel-associated transmission rates?**" Attwood SW, et al. 2022 (*Nat Rev Genet* 23(9):547–562, PMID 35459859): "**there is a need for standard definitions of sampling schemes to minimize bias in large-scale analyses**," and "**analytical methods for a priori estimation of appropriate sampling intensity, sizes and strategy … are urgently required but not well developed.**"

**The balanced-subsample re-clustering check has no bacterial precedent either — but it is trivially constructible.** Searched for and not found: any paper that re-runs population-structure clustering on a geographically or study-balanced subsample and quantifies partition agreement against the full-data partition. The machinery exists and is citable: **PopPUNK uses the Adjusted Rand Index** for a structurally similar stability check — "the adjusted Rand index can be used to compare the clustering results. This ranges from zero (different clusters) to one (the same clusters) while adjusting for chance cluster overlap" — perturbing batch order and reference choice rather than sampling balance. fastbaps uses Fowlkes–Mallows, and bootstraps over *sites* rather than isolates, which is orthogonal to this question.

So: report ARI between the full-data partition and each of B balanced-subsample partitions (balanced on country, and separately on BioProject), restricted to the intersection of retained genomes, as a **distribution** rather than a point estimate. Cite PopPUNK for the statistic and Meirmans 2018 for the motivation, and state that no bacterial precedent exists — that statement is itself a contribution.

**One contemporary negative example worth naming.** Wu et al. 2026 (*Emerg Microbes Infect*, PMID 42377320) make exactly this kind of phylogeographic claim from 3,573 unbalanced public *B. pseudomallei* genomes with no bias correction of any kind. Gap 2 already establishes their ten clusters were imposed by `fcluster(t=10)` rather than inferred.

### 4.3 A demonstration that the root-state answer follows the sampling

`§B` implements the closed form. Under an equal-rates Mk model on a star tree, the root conditional likelihood for state *i* is a product over tips, so it depends on the data **only through the state counts**. Running it on the observed country counts puts posterior **1.0000 on Thailand with a log10 Bayes factor in the hundreds** against the runner-up, at every value of q·t tested from 0.001 to 0.5. Running it on the n = 15 balanced design gives an exactly flat posterior of 1/15, by construction.

A star tree is the extreme case, and the script says so. Real tree structure dilutes the effect because correlated tips stop counting as independent observations; it does not remove it, because the tip counts enter the likelihood the same way on any topology. The point of the demonstration is that a root-state posterior from an unbalanced run **carries no information the sample-size table does not already carry**, and must not be reported as a result.

---

## 5. Dating tooling on recombination-corrected trees

### 5.0 The pipeline paper, retrieved — and it settles the architecture question outright

> Didelot X, Parkhill J. "A scalable analytical approach from bacterial genomes to epidemiology." *Phil Trans R Soc B.* 2022;377(1861):20210246. [10.1098/rstb.2021.0246](https://doi.org/10.1098/rstb.2021.0246)

Read in full. This is the step-by-step guidance paper from the BactDating author, and it is the reference the review's whole architecture should be citing. Their Figure 1 is exactly the pipeline in question: **whole-genome alignment → (Gubbins, ClonalFrameML) → recombination-corrected phylogeny → (BactDating, LSD, treedater, TreeTime) → dated phylogeny → (phylodyn, skygrowth, treestructure, TransPhylo, phydyn) → epidemiological interpretation.**

**The decisive passage settles handoff fact #2 with a concrete demonstration rather than an argument.** Verbatim:

> "A method often used is to extract from the genomic alignment the sites that have not been affected by recombination and to build a phylogeny using these sites only. Both Gubbins and ClonalFrameML are often used in this way, to create a recombination-free alignment which is then passed on to BEAST. **However, this method works only if relatively few recombination events happened throughout the tree.**"

And the simulation that makes it concrete — a modest dataset of 20 sequences at r/2 = 0.001 per site:

> "**In this simulated dataset, there was not a single site that was not affected by recombination on at least one of the branches.** On the other hand, every branch had some sites unaffected by recombination."

> "ClonalFrameML correctly inferred that there was not a single site unaffected by recombination on at least one of the branches. **Therefore an alignment containing only the non-recombinant sites would contain no sites, and could not be used as a starting point for further analysis.** On the other hand, the inferred clonal genealogy … can be used in our proposed step-by-step approach."

For *B. pseudomallei* — r/m = 7.2, at least 78% of K96243 ever recombined (Gap 5) — this is not a hypothetical. **The masked-alignment route degrades toward an empty or near-empty alignment precisely in this organism's regime, while the clonal genealogy remains usable.** That is the strongest available justification for the existing design, and it was previously supported only by Hedge & Wilson's branch-length argument.

A second sentence closes the Gap 3 loop on `snp-sites` ordering: alignments of variant sites "cannot be used for recombination-aware phylogenetics since the **genomic distance between variant sites becomes an important factor**."

**Four further things this paper supplies that the review needs.**

**Missing dates are a solved problem, and the fix is native.** In their worked example, "the isolation dates were unknown for 36 of the 521 genomes. **BactDating can accommodate this by treating the missing dates as additional parameters that are inferred simultaneously as the dates of the common ancestors.**" With 38.2% of this collection undated — and §4.2a showing that 1,410 of those come from a single project — this is the route to take rather than dropping tips. Note that BactDating's `clusteredTest()` does *not* respect it (§6.5).

**The date-randomisation floor is 20, not 100.** Verbatim: the test "involves making sure that the inferred substitution rate is larger when using the correct dates for the genomes than when the dates are permuted in **at least 20 randomized datasets**," and they note the step-by-step design makes this cheap "which is achieved in our step-by-step method by separating the phylogenetic inference from the dating." Their own example used 100 replicates with the CR2 criterion.

**Rooting is a dating decision.** "The root of the phylogeny is typically estimated during the dating step, since the trees generated by standard phylogenetic tools are not rooted whereas dated trees are always rooted by definition." If the root is already fixed by outgroups, feed in a rooted tree without the outgroups and **turn off root estimation**; if it is not, dating gives you rooting for free. This matters for §8, where the Australian-origin claim is a root claim.

**Prior misspecification is more forgiving than expected.** Their Figure 3 simulates under an epidemic model and dates under a coalescent constant-size prior — "in good agreement with the 'true' dated phylogeny … **despite the complete difference between the epidemic model used for simulation and the coalescent model used for inference**." And Figure 4 shows uncertainty in the dated phylogeny propagates weakly into transmission-tree interpretation. That is reassuring for the tree prior specifically; it says nothing about the *rate* prior, which §5.5 shows spans an order of magnitude.

**Their own scale check, for calibration.** 521 *S. aureus* ST239 genomes: ClonalFrameML ~2 days, Gubbins ~1 day ("this step currently represents a clear bottleneck"), BactDating v1.1 with the **additive relaxed clock** ~3 h for 10⁶ iterations. They note that "for very large datasets, it can be useful to divide them into lineages which can be analysed separately and in parallel" — i.e. the cluster-then-analyse design, endorsed in passing.

### 5.1 BactDating — three things the handoff did not record

> Didelot X, Croucher NJ, Bentley SD, Harris SR, Wilson DJ. "Bayesian inference of ancestral dates on bacterial phylogenetic trees." *Nucleic Acids Res.* 2018;46(22):e134. PMID 30184106. [10.1093/nar/gky783](https://doi.org/10.1093/nar/gky783)

**The default clock model is now `arc`, not strict.** Verified in v1.1.4 source (dated 2025-07-07): `bactdate(..., model="arc", useRec=F, nbIts=10000)`. Eight models exist, including an undocumented `mixedcarc`.

The justification matters more than the default:

> Didelot X, Siveroni I, Volz EM. "Additive uncorrelated relaxed clock models for the dating of genomic epidemiology phylogenies." *Mol Biol Evol.* 2021;38(1):307–317. PMID 32722797. [10.1093/molbev/msaa193](https://doi.org/10.1093/molbev/msaa193)

Standard uncorrelated relaxed clocks have excess variance proportional to *l*², violating additivity, so **estimates shift when genomes are added or removed**. In a study where cluster membership is *itself inferred* — and Gap 2 establishes the partition is neither unique nor validated — a non-additive clock means the dates move when the clustering moves. That is a direct threat, and `arc`/`carc` is the fix.

**`useRec=T` is not the default.** The Gubbins per-branch recombination information is discarded unless explicitly requested. This is easy to miss.

**`loadGubbins()` can fail silently.** Reverse-engineered from source: it reads `.final_tree.tre`, `.node_labelled[.final_tree].tre` and `.per_branch_statistics.csv` (tab-separated), calls `unroot()`, and computes a per-branch `unrec` fraction. **Column indexing branches on `ncol == 11` or `13`; anything else falls through to a different formula with no warning.** Assert per cluster: `ncol(per_branch_statistics) %in% c(11, 13)` and `all(tree$unrec > 0 & tree$unrec <= 1)`. Note also that branch lengths must be in substitutions, not per site — `main.R` warns only if total tree length < 5.

**Seng et al. 2024 used v1.1.1 with a strict clock.** That is now doubly superseded: superseded on the clock model by the additivity argument, and superseded again by §6.4 below, which shows strict clocks carry the *highest* type-I error in temporal-signal classification.

### 5.2 TreeTime, LSD2, treedater

> Sagulenko P, Puller V, Neher RA. "TreeTime: maximum-likelihood phylodynamic analysis." *Virus Evol.* 2018;4(1):vex042. PMID 29340210

Current version 0.12.1. Its strongest feature for this dataset is native handling of **missing dates**, which matters when 38.2% of the collection has no collection year. But: **searched for and not found — any native TreeTime support for Gubbins output, or any TreeTime analogue of per-branch recombination down-weighting.** For a post-Gubbins workflow BactDating is the better fit, because it is the only one of these tools that consumes the recombination correction rather than ignoring it.

LSD2 (To TH, Jung M, Lycett S, Gascuel O, *Syst Biol* 2016;65(1):82–97, and via IQ-TREE's `--date`) and treedater (Volz & Frost, *Virus Evol* 2017;3(2):vex025) are fast least-squares and relaxed-clock alternatives. Useful as cheap cross-checks; neither handles recombination weighting.

### 5.3 The substitution rate to use, and what it is worth

| Rate (subs/site/yr) | Interval | Basis | Source |
|---|---|---|---|
| **1.7 × 10⁻⁷** | **95% HPD 1.3–2.1 × 10⁻⁷** | median across a >16-year chronic within-host infection | **Pearson et al. 2020**, *PLoS Pathog* 16(3):e1008298, PMID 32149236 |
| 4.9 × 10⁻⁷ | no CI given | average within-patient rate | cited as ref [14] in Pearson 2020 |
| 3.3 / 3.6 × 10⁻⁷ | — | *B. dolosa* / *B. multivorans*, for context | refs [80]/[82] in Pearson 2020 |
| **6.26 × 10⁻⁷ – 1.81 × 10⁻⁶** | see per-cluster table below | **BEAST, per cluster, per replicon** | **Chewapreecha 2017, Supplementary Figure 6f — RETRIEVED 2026-08-09** |

Verbatim from Pearson: "The median evolutionary rate across the entire genomic dataset was **1.7 × 10⁻⁷ substitutions/site/year (95% HPD 1.3 × 10⁻⁷–2.1 × 10⁻⁷)**."

**Seng et al. 2024 imported a Pearson rate as their prior, but which one cannot be established from the paper.** Their Methods say "prior mutation rate derived from Pearson and colleagues," citing reference [53]. Pearson et al. 2020 is the only Pearson *B. pseudomallei* rate paper with a credible interval, so it is the natural reading. **But reference [53] as published resolves to Spring-Pearson et al. 2015 (*PLoS ONE*), a pangenome paper containing no clock analysis at all** — verified independently via Crossref key `50067_CR53` and PMC. So the citation as printed does not support the rate.

Two things follow. There *is* a *Nature Communications*-published precedent for importing an external rate prior into a *B. pseudomallei* BactDating analysis, which answers the handoff's "is this defensible?" with a qualified yes. But **do not cite Seng as precedent for the specific value 1.7 × 10⁻⁷**, because the paper's own reference does not establish it. Cite Pearson 2020 directly for the number, and Seng only for the practice.

**Four caveats that must travel with the number.** It is a **within-host** rate from chronic infection, and this organism spends most of its existence as a soil saprophyte; short-timescale rates systematically exceed long-timescale ones, so the two biases compound in the same direction and node ages derived from it skew **young**. BactDating's μ is per genome per year, so per-replicon analysis requires multiplying by the replicon length actually in the alignment, not the 7.2 Mb total. And these rates were not estimated on Gubbins-corrected trees.

### 5.4 Chewapreecha's per-chromosome clock rates — retrieved, and they disagree with Pearson by 4–10×

The Gap 3 pass recorded these as sitting "in a supplementary table that has still not been retrieved." **The reason they could not be found is that there is no such table. The paper has no supplementary tables at all** — the SI front matter lists only "Supplementary Figures 1-12, Supplementary note and Supplementary References," plus Supplementary Data 1–5 as separate files. **The rates are printed inside panel (f) of Supplementary Figure 6**, and the date-randomisation ranks are annotations inside Supplementary Figure 5.

Supplementary Figure 6f, transcribed:

| Group | Rate chr I (95% HPD) | Rate chr II (95% HPD) | TMRCA chr I | TMRCA chr II |
|---|---|---|---|---|
| Group 4 — SEA (Singapore–Malaysia) | **N/A** (ESS failure) | 6.26 × 10⁻⁷ (4.22–8.37 × 10⁻⁷) | N/A | 1918 (1883–1942) |
| Group 6 — SEA (Thailand–Laos) | 9.22 × 10⁻⁷ (6.90 × 10⁻⁷–1.14 × 10⁻⁶) | 6.71 × 10⁻⁷ (4.05–9.37 × 10⁻⁷) | 1940 (1920–1955) | 1938 (1901–1961) |
| Group 7 — SEA (Singapore–Malaysia) | 6.96 × 10⁻⁷ (3.53 × 10⁻⁷–1.14 × 10⁻⁶) | 1.59 × 10⁻⁶ (1.22–2.00 × 10⁻⁶) | 1981 (1968–1988) | **1991 (1968–1988)** ⚠ |
| Group 8 — SEA (Singapore–Malaysia) | 1.12 × 10⁻⁶ (7.05 × 10⁻⁷–1.45 × 10⁻⁶) | 1.26 × 10⁻⁶ (6.70 × 10⁻⁷–1.72 × 10⁻⁶) | 1976 (1970–1977) | 1976 (1966–1977) |
| Group 19 — American isolates only | 1.80 × 10⁻⁶ (1.36–2.26 × 10⁻⁶) | 1.81 × 10⁻⁶ (1.29–2.28 × 10⁻⁶) | 1806 (1756–1849) | 1759 (1682–1815) |

⚠ **A published erratum worth noting:** Group 7 chromosome II reads "1991 (1968 to 1988)" — the point estimate lies outside its own stated HPD. Verified against a page render; this is what the figure says.

**Three things follow that the review needs.**

**First, the two in-organism rate sources disagree by 4–10×.** Chewapreecha's range is 6.26 × 10⁻⁷ to 1.81 × 10⁻⁶; Pearson's is 1.7 × 10⁻⁷. Since §6.7's fallback is "impose a literature rate range and report a broad conservative interval," which literature rate you import swings node ages by roughly an order of magnitude. **The honest move is to impose the union — roughly 1.3 × 10⁻⁷ to 2.3 × 10⁻⁶ — and report how far the answer moves across it**, rather than picking one and quoting a tight interval. This is exactly the prior-sensitivity analysis Tay et al. require.

**Second, Chewapreecha's own external validation is weaker than it reads.** The SI caption pins "consistent with the previous estimate in *Burkholderia* species" to **Lieberman et al. 2011, *Nat Genet* 43:1275** — which is *B. dolosa* within cystic-fibrosis patients. A different species, on a within-host timescale. So the reference study's rate sanity-check is against the same class of short-timescale within-host estimate that §5.3 flags as biased fast.

**Third, the combined American HPD is not a combination.** Verbatim: "The most recent common ancestor for the American isolates was estimated to be 1806 or 1759 based on either chromosome I or II, respectively (combined 95% highest posterior density (HPD) interval of both chromosomes, 1682-1849)." The two chromosomes were analysed as fully independent BEAST runs and the "combined" interval is simply the **outer envelope** of the two — 1682 is chromosome II's lower bound, 1849 is chromosome I's upper bound. There is no weighting, no joint analysis, and no test of whether two estimates 47 years apart are compatible. *(Note also that the abstract's "between 1650 and 1850" is the historical slave-trade window, not the HPD.)*

**A unit warning.** The rates are reported in substitutions per site per year only; the paper reports SNPs per genome per year nowhere. And because the core-genome alignment length is never stated (§11), **those rates cannot be converted to per-genome units by any reader**. Any conversion requires assuming a denominator the paper does not license.

**Do not cite a pooled Chewapreecha rate of 1.03 × 10⁻⁶.** That figure circulates second-hand but appears nowhere in the paper or its Supplementary Information; the only rates given are the nine per-cluster, per-chromosome values above. If a single figure is needed, quote the range.

### 5.5 The rate landscape is not a clean time-dependent gradient, and its middle is empty

Ordering every *B. pseudomallei* estimate by timescale:

| Timescale | Source | Rate (subs/site/yr) |
|---|---|---|
| Within-host, hypermutator (defective MutS) | Viberg et al. 2017, *mBio* 8(2):e00356-17, PMID 28400528, patient CF9 | **1.8 × 10⁻⁶** ✅ verified |
| Within-host, normal, months–years | Viberg et al. 2017 | **4.9 × 10⁻⁷** ✅ verified |
| Within-host, 16-year chronic carriage | Pearson et al. 2020 | **1.7 × 10⁻⁷** (95% HPD 1.3–2.1 × 10⁻⁷) |
| Epidemiological, one NE Thai sub-lineage, ~3.5-yr window | **Seng et al. 2024**, Supplementary Fig 3c | **3.20 × 10⁻⁷** (95% HPD 8.11 × 10⁻⁸ – 5.36 × 10⁻⁷) |
| Epidemiological clusters, decades–2 centuries | **Chewapreecha 2017** | **6.26 × 10⁻⁷ – 1.81 × 10⁻⁶** |
| Long-term phylogeographic, millennia | Pearson et al. 2009 | ~1.4 × 10⁻⁸ – 1.6 × 10⁻⁷ — **assumed, not estimated** |

*(Note the authorship correction: the 4.9 × 10⁻⁷ within-host figure is* **Viberg** *LT et al. 2017, not Price. And Pearson 2009 is* BMC Biology*, not BMC Microbiology.)*

Three things are wrong with treating this as a time-dependent rate gradient.

**It is not monotonic.** Pearson's 16-year *within-host* estimate (1.7 × 10⁻⁷) is *lower* than Chewapreecha's decadal-to-bicentennial *between-host* cluster rates (up to 1.81 × 10⁻⁶) — the opposite of the naive expectation, and the opposite direction from the caveat in §5.3. The within-host estimates alone span an order of magnitude, driven largely by mutator status.

**Seng's own posterior is the only other between-host estimate, and it is nearly circular.** 3.20 × 10⁻⁷ with a 95% HPD of 8.11 × 10⁻⁸ – 5.36 × 10⁻⁷, reported only in Supplementary Figure 3c and never in the main text, for a single sub-lineage over a ~3.5-year window. It overlaps Pearson but excludes most of Chewapreecha's range. Since it was estimated *under an imported Pearson prior* on a window far too short to identify a rate independently (§6, and the whole point of §5.3), it should be read as largely reproducing its prior rather than as independent corroboration.

**The deepest point is not an estimate.** Pearson 2009's millennial figure is an *E. coli*/*B. anthracis* per-generation rate multiplied by an assumed 100–300 generations per year. **There is currently no empirically estimated long-timescale *B. pseudomallei* substitution rate.**

**And the epidemiological middle is essentially empty.** The two investigations most likely to supply one report no rate at all and explicitly report *absence* of temporal signal over long windows: Chapple et al. 2016 (*Microb Genom* 2:e000067, PMID 28348862; Western Australian Avon Valley point source, 1966–1991, 11 isolates, 1–268 SNPs, no temporal correlation) and Webb et al. 2020 (*mSystems* 5:e00726-20, PMID 33172968; a 51-year ST-284 focus, 22 genomes, 532 SNPs, "limited evidence of a correlation between mutation patterns and time" — clock deliberately not applied). The 2021 US aromatherapy-spray outbreak (Gee, Bower et al. 2022, *NEJM* 386:861, PMID 35235727) reports no SNP count between patient and product isolates and no rate.

**The practical consequence** is that "impose a literature rate range" (§6.8) has to span **1.3 × 10⁻⁷ to 2.3 × 10⁻⁶** — better than an order of magnitude — and that any date reported under it inherits that width. Say so rather than picking the convenient end.

**Viberg verified from the primary source**, and it supplies per-genome units the other estimates lack. Verbatim: "Six (CF1, CF6, CF7, CF8, CF10, and CF11) of the seven pairs accrued mutations at a mean rate of 6.4 mutations/year… Examining only SNPs, this rate was **3.6 SNPs/year (4.9 × 10⁻⁷ substitutions/site/year)**, similar to those determined previously for *B. dolosa* at 2.1 SNPs/year (**3.3 × 10⁻⁷**…) and for *B. multivorans* at 2.4 SNPs/year (**3.6 × 10⁻⁷**…). In contrast, the CF9 pair was a clear outlier, with 24.9 mutations/year and **12.9 SNPs/year (1.8 × 10⁻⁶ substitutions/site/year)**." The implied denominator, 3.6 ÷ 4.9 × 10⁻⁷ ≈ 7.35 Mb, is consistent with the genome size, so the conversion is internally coherent.

**A counterpoint from the same paper that the review should carry, because it cuts the other way.** Viberg et al. state that *B. pseudomallei* "demonstrates a **very strong phylogeographic signal that allows accurate identification of strain origin on a continental level**," and they used it successfully: "our analysis revealed that patient CF11 was infected while traveling in Southeast Asia, **consistent with the reported travel history for this patient**, whereas all other patients in our study acquired their *B. pseudomallei* infections in Australia."

That is a genuine, independently corroborated validation of continental-scale assignment — Asia versus Australia — in a case where the answer was known from travel history. It does not rescue dating, fine-scale migration rates, or root-state inference, all of which fail for the reasons in §2–§6. But it does mean the review should not overreach into "nothing can be said about geography." **The defensible line is that continental-level strain origin is well supported and independently validated, while dated, directional, between-country migration inference is not.**

*(Confidence note: Chewapreecha's values in §5.4 and Viberg's above are verified from primary sources. Lieberman 2011's 3.3 × 10⁻⁷ is quoted here at one remove via Viberg's citation of it; Croucher 2011, Harris 2010 and Young 2012 remain unverified. Check before citing.)*

---

## 6. Testing temporal signal — the standard test is broken here

This is the most consequential technical section in Gap 4, because the review currently recommends date-randomisation and that recommendation needs qualifying.

### 6.1 Two PMID corrections before anything is cited

The handoff's PMIDs for two key papers are wrong, and both wrong numbers resolve to unrelated clinical articles. **Duchêne 2015 date-randomisation is PMID 25771196** (not 26069215, a congenital-heart-defect cost study). **BETS is PMID 32895707** (not 32895713, a deep-brain-stimulation meta-analysis). Fix before citing.

### 6.2 The date-randomisation test is anticonservative under exactly this data structure

> Murray GGR, Wang F, Harrison EM, Paterson GK, Mather AE, Harris SR, Holmes MA, Rambaut A, Welch JJ. "The effect of genetic structure on molecular dating and tests for temporal signal." *Methods Ecol Evol.* 2016;7(1):80–89. PMID 27110344. [10.1111/2041-210X.12466](https://doi.org/10.1111/2041-210X.12466)

> "all of the standard tests of temporal signal are seriously misleading for data where temporal and genetic structures are confounded (i.e. where closely related sequences are more likely to have been sampled at similar times)"

The quantitative result is severe. In the confounded, low-temporal-structure scenario, "**over a third of the simulated data sets showed a high correlation between sampling date and root-to-tip distance**" while "yielding a wildly inaccurate estimate of the tMRCA: **51 ybp, as opposed to the true value of 10,000 ybp**." A ~200-fold error, in more than a third of replicates, passing the standard tests. With balanced sampling, "none of the 1000 data sets gave high r-values."

Their MRSA ST22 example locates the danger zone numerically: for a 3-year sampling window where "**fewer than 7 nucleotide substitutions per genome would be expected during this entire sampling period**," "the standard tests failed for the confounded subsample, **resulting in false confidence**."

Their recommendation: "we recommend the use of '**clustered permutation**' for all analyses" — permuting dates **among but not within** monophyletic clades that share a sampling era — plus "use a Mantel test, comparing genetic distance and difference in sampling dates, to identify data sets where confounding is present."

**A *B. pseudomallei* collection assembled from published studies across four decades and six regions is a textbook confounded design: geography ⇒ clade ⇒ sampling era.** And the arithmetic lands exactly on Murray's threshold. `phylogeography_diagnostics_bp.py §E`, at the Pearson rate over the Wu core alignment, gives **0.647 substitutions per genome per year**; against §A's **effective** temporal span of **11.05 independent-year-equivalents**, that is **7.1 expected substitutions across the entire sampling window**. The collection as a whole sits on the boundary of the regime Murray et al. showed produces false confidence — a number computed from metadata alone, before any alignment exists.

**The consequence for the reference study is direct and worth stating in print.** Chewapreecha's date-randomisation ranks were 34th to 97th of 1,000, i.e. empirical p ≈ 0.03–0.10 — marginal **even under the anticonservative test**. Under a clustered permutation those five clusters would plausibly not survive. Both melioidosis precedents used an unclustered test (Chewapreecha 1,000 permutations; Seng 100) and both used a strict clock. By current standards both choices are superseded, and that gap is itself a legitimate contribution.

Two further cautions on root-to-tip regression, which the review should stop treating as a test:
- Duchêne 2015: root-to-tip distances "**do not represent statistically independent samples**."
- Rieux A, Balloux F, *Mol Ecol* 2016;25(9):1911–1924, PMID 26880113: "**extensive pseudoreplication between samples. Indeed, the same branches in the phylogeny will contribute to multiple root-to-tip distances**," and "the nonindependence between distances cannot be completely controlled for." Their headline: "highly recommend performing the **clustered** date-randomization test using the most stringent criterion prior to any study." And the warning to quote when declining to date: "**in the absence of a temporal signal in the data, the result will be driven by the prior, and is thus likely to be misleading.**"

If a date-randomisation test is run at all, use Duchêne's **CR2**: "there is no overlap between the 95% credible interval of the original rate estimate and any of those from the date-randomized data sets," with at least 20 randomisations.

### 6.3 BETS is the only decision-capable test, and that asymmetry is the argument for it

> Duchene S, Lemey P, Stadler T, Ho SYW, Duchene DA, Dhanasekaran V, Baele G. "Bayesian evaluation of temporal signal in measurably evolving populations." *Mol Biol Evol.* 2020;37(11):3363–3379. PMID 32895707. [10.1093/molbev/msaa163](https://doi.org/10.1093/molbev/msaa163)

BETS compares the marginal likelihood of a **heterochronous** model (real sampling times) against an **isochronous** one (samples constrained contemporaneous), via generalized stepping-stone in BEAST 1.10 or nested sampling in BEAST 2.5. Thresholds on the Kass–Raftery scale: log BF ≥ 5 "very strong," ≥ 3 "strong," ≥ 1 positive.

**The critical property for a study whose expected outcome is negative: log BF ≤ −3 positively supports the *absence* of temporal signal. The date-randomisation test can only fail to reject.** For a review that expects most clusters to be undateable, that asymmetry is the single strongest methodological argument.

Their verdict on the alternatives is blunt. On the DRT: "an inconsistent mixture of statistical frameworks when Bayesian phylogenetic methods are used," and "such an approach is **not a formal test** of temporal signal in the data because the permutations do not necessarily constitute an appropriate null model." On root-to-tip: "the absence of appropriate statistics means that there is **no clear objective way** of determining whether the data contain temporal information," and — describing this dataset almost exactly — "the root-to-tip regression is uninformative when the data have been sampled over a **narrow time window** and there is some **rate variation among lineages**."

Their bacterial exemplar is instructive as a contrast. *Bordetella pertussis*, 150 samples over **89 years**, gave log BF 47.40 for heterochronous over isochronous and a rate of 1.65 × 10⁻⁷ — essentially identical to the *B. pseudomallei* rate. **An 89-year window at the same rate still needed a relaxed clock.** That is why *B. pseudomallei* clusters, with effective windows near 11 years, fail.

### 6.4 BETS is not free either

> Tay JH, Kocher A, Duchene S. "Assessing the effect of model specification and prior sensitivity on Bayesian tests of temporal signal." *PLoS Comput Biol.* 2024;20(11):e1012371. PMID 39502105

The failure mode is **"tree extension"**: when data lack temporal signal but priors favour implausibly old roots, "the incorrect inclusion of sampling times produces a dramatic overestimation of the height of the tree," the sampling times become negligible against root height, and **BETS falsely detects temporal signal**. Prior sensitivity is severe — log-normal versus exponential priors gave mean root heights of **772 versus 2.9** units in simulation.

Critically: with Gamma and log-normal priors on isochronous simulations, BETS produced false positives in **most replicates under strict clock models**, and "analyses under the relaxed clock tended to have fewer type I classification errors than the strict clock." **Seng et al.'s choice of a strict clock "to prevent parameter over-fitting" is precisely the setting with the highest type-I error for this purpose.** Flag it.

Their four requirements, all of which should be adopted: prior predictive simulation on root height and rate; prior sensitivity analysis across at least Gamma, log-normal and exponential priors; preference for relaxed clocks; and hard bounds on root height from biology, which "eliminated false positives in simulations even when set five-fold higher than true values."

### 6.5 `clusteredTest()` exists in BactDating and is not what it sounds like

Undocumented in README and vignettes, present in `R/clustered.R`, labelled "Experimental." Read the source before using it: it **drops all undated tips**, runs `vegan::mantel(genetic distance, temporal distance)`, and if the Mantel test is significant it **thins tips** — greedily removing isolates whose dates fall within an expanding window of an already-retained isolate — looping until the Mantel test goes non-significant, then runs the **ordinary, uniformly-permuted `roottotip()`** on what remains.

So it removes confounding by *deleting data until the confounding is undetectable*, then applies the standard test to the residue. That is defensible but it is **not** Murray's clustered permutation. It is stochastic with no exposed seed, so it is not reproducible run to run, and the final non-significant Mantel result is a failure to reject rather than evidence of absence.

**Use its Mantel component as the diagnostic Murray prescribes — report Mantel *r* and *p* per cluster — and do not rely on the thinned p-value as the temporal-signal test.**

Note also that `roottotip()`'s own permutation is `sample(date, n, replace=F)`: a uniform, unclustered permutation, i.e. exactly the test Murray showed is anticonservative.

### 6.6 The protocol this implies

Per cluster, per replicon:

0. **Screen, don't test.** Record n tips, n dated tips, sampling window, tree length in substitutions, and the **Mantel r/p** between cophenetic genetic distance and temporal distance. Clusters with significant Mantel correlation are confounded, and no unclustered test may be applied to them. Duchêne et al. 2016 found "data sets with sampling times spanning **less than 10 years** were largely unreliable" — a prima facie exclusion.
1. **Root-to-tip as a figure, never as a test.** Report the slope, which is an interpretable rate. Do not report R² as a test statistic and do not report the built-in permutation p-value.
2. **Clustered date-randomisation with CR2** where feasible, reporting the number of unique permutations available (it collapses fast, and where it is small the test is underpowered).
3. **BETS as the primary test**, with the Tay et al. diligence attached. It is a BEAST analysis and does not scale to 61–101 clusters × 2 replicons × 4 models, so run steps 0–2 on everything and BETS on the survivors plus a random negative-control subset.
4. **Cheap analogue where BETS is infeasible:** `bactdate()` with real dates versus all-dates-equal, compared with `modelcompare()` on BactDating's hard-coded DIC scale (ΔDIC > 10 "definitely better," 5–10 "slightly," < 5 "not significant"). Report as a DIC approximation and cite Duchene 2020's preference for marginal likelihoods.
5. **Exploit the two replicons as an internal replicate.** Chewapreecha's filter — accept only clusters with "consistent clock-like behaviour across both chromosomes" — is a principled concordance criterion that single-replicon organisms do not afford.
6. **Post-hoc diagnostics on every dated tree reported.** DiagnoDating (Didelot X, Carson J, Ribeca P, Volz E, *Mol Biol Evol* 2026;43(4):msag093) runs posterior predictive checks on branch-length moments and stemminess plus Anderson–Darling tests on per-branch residuals, and is designed to detect "the distorting effect of recombination" that survives Gubbins. The authors advocate it "for all microbial population genetic studies that involve the reconstruction of a dated phylogeny."

### 6.7 The reference study's own numbers are weaker than the handoff recorded — two corrections

Both corrections come from Supplementary Figures 5 and 6, retrieved and transcribed 2026-08-09. Both make the "dating failure is the base case" argument stronger, and both need fixing before anything is cited.

**Correction 1 — the ranks are PERCENTILES, and that inverts their meaning.** The handoff reads the "34th to 97th of 1,000 permutations" as empirical p ≈ 0.03–0.10, i.e. marginal but passing. That is wrong. The Supplementary Figure 5 caption states, verbatim, that "**a percentile rank of R² from the true signal against 1,000 randomised signals is documented underneath its R²**." A percentile rank of 34 means the true R² fell **below 66% of the randomised replicates** — an outright failure of temporal signal, not a marginal pass.

The full per-cluster, per-chromosome table read off Supplementary Figure 5b:

| Group | chr I R² | chr I rank | chr II R² | chr II rank |
|---|---|---|---|---|
| Group 4 | 0.201 | 73rd | 0.224 | 86th |
| Group 5 (n=4, not dated) | 0.879 | — | 0.938 | — |
| Group 6 | **0.0189** | **45th** | **0.0122** | **34th** |
| Group 7 | 0.253 | 88th | 0.0657 | 69th |
| Group 8 | 0.842 | 92nd | 0.976 | 97th |
| Group 19 — America only | 0.123 | 65th | 0.134 | 66th |

**Only Group 8 (92nd, 97th) approaches a conventionally acceptable result.** Group 6 was dated on an R² of 0.0189 and 0.0122 — essentially no root-to-tip signal at all — at percentile ranks of 45 and 34, meaning its true signal was *worse than random* on one chromosome and indistinguishable on the other. The authors acknowledge this only obliquely ("suggesting that noise had an effect on a small dataset") and then defend the results by comparing rates to other species rather than by the test.

For context, Supplementary Figure 5a reports the whole-dataset root-to-tip regression at **R² = 0.00323**, with the caption stating: "**The plot rejects the influence of sampling time over the amount of root-to-tip diversity in the whole dataset.**"

**A further wrinkle:** their permutation is the inverse of the conventional test. Verbatim: "we performed **1,000 permutations with the true date, but randomised root-to-tip distance**." Conventional date-randomisation permutes tip dates. They permuted the response variable instead — which tests a different null and is not the Duchêne/Murray procedure they cite.

**Correction 2 — the dated fraction is 59 of 469, not 68.** Verbatim: "American isolates within group 19: 9 isolates, group 4: 11 isolates, group 6: 24 isolates, group 7: 9 isolates, and group 8: 6 isolates." That sums to **59 isolates, 12.6% of the collection**, not the 68 / 14.5% the handoff records. The discrepancy is Group 19: it has 18 members, but **only its 9 American isolates were dated** — the cluster as a whole never was.

Note also the geographic concentration of what did work: three of the five dated clusters are the same Singapore–Malaysia sub-region, one is Mekong, one is American. Nothing Australasian, nothing Thai-dominated.

**Correction 3 — the second precedent is thinner still, and its test result was never published.** Seng et al. 2024 sequenced 1,391 genomes and dated **one sub-lineage of 17 isolates** — confirmed twice, from the 17 tips in Supplementary Figure 3c and from Supplementary Data 1's `sub_dominant_lineage` column. That is **1.2% of the collection**, against Chewapreecha's 12.6%. Their rate (3.20 × 10⁻⁷) and TMRCA (2011) appear **only inside that figure panel** and nowhere in the main text.

And the test itself is unreported. The Methods describe "a date-randomisation test, consisting of 100 permutations… to assess the robustness of the temporal signal," but **no p-value, rank or percentile appears anywhere** — not in the main text, not in the 12-page Supplementary Information, not in the Peer Review File. The SI contains zero occurrences of "randomis\*", "root-to-tip", "BactDating", "temporal" or "clock", and there is no root-to-tip regression figure and no temporal-signal figure at all. This is a definitive non-report, established by exhaustive text search, not a retrieval failure.

**What this does to the review's position.** The handoff already treats dating failure as the base case. These numbers say the base case is worse than that. The one global *B. pseudomallei* dating analysis dated five clusters, **four of which fail their own temporal-signal test** on the conventional reading of their own statistic. The one large regional analysis dated **17 isolates out of 1,391** and **never published its test result**. Neither applied any sampling-bias correction to the dating itself — Chewapreecha's n = 15 subsampling was applied only to the ancestral-state reconstruction.

Combined with §6.2 — that the standard test is anticonservative under exactly this data structure, and that Chewapreecha used an unconventional variant of it — the defensible summary is that **there is currently no well-supported between-host molecular clock estimate for this organism.** That is a strong, citable, and previously unstated claim, and it reframes a negative dating result from this pipeline as the expected finding rather than a shortfall.

### 6.8 Publishing the negative result — the base rate and the template

Dating failure is the modal outcome in bacterial genomics and is routinely published as a finding.

- **Duchêne S, Holt KE, Weill F-X, et al.** "Genome-scale rates of evolutionary change in bacteria." *Microb Genom.* 2016;2(11):e000094. PMID 28348834. Across 36 datasets from 16 species, "the date-randomization test suggested that 28 data sets had strong to moderate temporal signal" — **8 of 36 (22%) lacked usable signal, reported in the main result.** Also: "Nearly all bacterial species investigated here displayed genome evolution that was measurable over a period of 10–100 years. **Data sets with sampling times spanning less than 10 years were largely unreliable.**"
- **Menardo F, Duchêne S, Brites D, Gagneux S.** "The molecular clock of *Mycobacterium tuberculosis*." *PLoS Pathog.* 2019;15(9):e1008067. **This is the best template for the paper.** 31 datasets, **13 failed** the date-randomisation test. The pass/fail table is a primary result. And the citable fallback prescription, verbatim:

  > "Alternatively, for data with no temporal structure, our estimates can be used to calibrate the clock rate at 10⁻⁸–5×10⁻⁷ nucleotide changes per site per year, thus obtaining a **broad (conservative) time estimate** for the age of the tree and of its nodes."

  Note the emphasis on *broad* and *conservative*: the imported prior should be a wide range, not a point value.
- **Both melioidosis precedents simply reported the failures.** Chewapreecha left 14 of 19 clusters undated. Seng reported dates for one sub-lineage of ten and offered no alternative analysis for the other nine — in *Nature Communications*.

**This answers the handoff's "non-clock alternatives" question, and the answer is mostly negative.** Searched for and not found: a bacterial paper publishing a **relative-time (substitution-scaled) tree as the headline deliverable** with the stated rationale that temporal signal was absent. The observed norm is either (a) report the failure and give no dates, or (b) report the failure and give a deliberately broad range under an imported literature rate. Relative-time-constraint dating and Bernabeu et al. 2025 ("Probabilistic modelling improves relative dating from gene phylogenies," *Methods Ecol Evol*, [10.1111/2041-210X.70127](https://doi.org/10.1111/2041-210X.70127)) are live but not standard; neither was read in full.

**The honest formulation for the paper:** dates obtained under an imported rate prior are *conditional projections of that prior*, not independent estimates. Report them as ranges, state the prior, and show a prior-sensitivity analysis demonstrating how far the answer moves when the prior moves.

---

## 7. Tree-free and population-genetic alternatives

### 7.1 ChromoPainter / fineSTRUCTURE — the scaling premise was wrong

The handoff assumed this family might not reach bacterial cohort scale. It does.

| Study | Organism | n genomes |
|---|---|---|
| Zhu M, et al. *Helicobacter* 2025;30(2):e70025, PMID 40059062 | *H. pylori* | **4,067** (fineSTRUCTURE + ADMIXTURE + DAPC on the same data) |
| Guevara-Tique AA, et al. *Virulence* 2022;13(1):1146–60, PMID 35838227 | *H. pylori* | 1,245 |
| **van Hal SJ, et al. *Lancet Microbe* 2022;3(2):e133–41, PMID 35146465** | ***E. faecium*** | **1,128** |
| Tomonari K, et al. *Microb Genom* 2025;11(6), PMID 40493491 | *H. pylori* | 438 |
| Yahara K, et al. *Mol Biol Evol* 2013;30(6):1454–64, PMID 23505045 | *H. pylori* | 29 (the original in-silico painting paper) |

**van Hal 2022 is the best template**, because it is non-*Helicobacter*, at 1,128 genomes, and its justification is this review's own argument in someone else's words: recombination-masking "excluded on average 2·5 Mb, or 85% of B genomes, distorting the inferred relationships," whereas painting "provides a coherent view of genetic exchange." Their pipeline — ChromoPainter in 10 kb windows for co-ancestry and hybrid detection (>30% admixture cutoff), then fastGEAR on highly-admixed regions purely for directionality — is adoptable more or less as-is.

Two practical facts that remove the obvious objections: bacterial haploidy eliminates the phasing problem entirely, and Yahara found linked ≈ unlinked painting in *H. pylori* (median chunk 14 bp), meaning a flat recombination map suffices.

**But the caveat is the load-bearing part**, verbatim from Yahara 2013:

> "Sampling bias will have strong effect on inference of population structure and admixtures… inference of admixture will sensibly depend on bias of donor genomes in the data set."

And on what painting cannot do: "there is currently no way to infer the date of admixture based on the co-ancestry matrix." If the question is *when* *B. pseudomallei* crossed Wallace's Line, painting cannot answer it. If the question is *which direction and how much*, it can.

**Searched for and not found: any application of ChromoPainter, fineSTRUCTURE, fastGEAR, ADMIXTURE, STRUCTURE or DAPC to *Burkholderia* whole genomes.** The only exception is STRUCTURE on 7-locus MLST in Pearson 2009.

### 7.2 ADMIXTURE — the decisive citation is fatal here

> Lawson DJ, van Dorp L, Falush D. "A tutorial on how not to over-interpret STRUCTURE and ADMIXTURE bar plots." *Nat Commun.* 2018;9:3258. PMID 30108219. [10.1038/s41467-018-05257-7](https://doi.org/10.1038/s41467-018-05257-7)

Unbalanced sampling changes **which group is inferred to be unadmixed** and changes the inferred **K**; sub-Saharan Africans lose the K = 2 split "because [they] constitute only a small proportion of the sample"; and the general statement, "**the problem is fundamental to any approach based on equally weighing samples**."

The most important part for this review is §3.2 of that paper: a **Recent-Bottleneck** history and an **Admixture** history produce *indistinguishable* bar plots. That is not an abstract concern here — Chewapreecha names exactly that alternative in her own paper (§8 below).

Their constructive remedy, **badMIXTURE**, works on unlinked data and does not need a recombination map: rather than reading the bar plot, compare the co-ancestry residuals implied by the fitted model against the observed ones, and see whether the admixture model actually explains the data.

### 7.3 DAPC — descriptive only

> Jombart T, Devillard S, Balloux F. *BMC Genet.* 2010;11:94. PMID 20950446

Two cautions with concrete numbers:

- Miller JM, Cullingham CI, Peery RM. "The influence of a priori grouping on inference of genetic clusters." *Heredity.* 2020;125(5):269–80. PMID 32753664. DAPC fails to recover clusters de novo at F_ST < 0.1 (in 100% of SNP replicates), and **a priori groups always separate — even under simulated panmixia**. 52.3% of surveyed studies omitted run parameters.
- Thia JA. "Guidelines for standardizing the application of DAPC to genotype data." *Mol Ecol Resour.* 2023;23(3):523–38. PMID 36039574. The concrete rule: retain **p_axes ≤ k − 1** discriminant axes, *not* the commonly used proportional-variance criterion.

Given Pearson's Φ_PT of 0.117 between the Australasian and Southeast Asian populations — just above the 0.1 line — DAPC on this organism sits exactly where Miller et al. say de novo inference fails. Use it to visualise a partition you already have; never to define one.

### 7.4 fastGEAR — right shape, silent trap

> Mostowy R, Croucher NJ, Andam CP, Corander J, Hanage WP, Marttinen P. "Efficient inference of recent and ancestral recombination within bacterial populations." *Mol Biol Evol.* 2017;34(5):1167–82. PMID 28199698

It scales to thousands, and it has an explicit **unsampled-origin state** — which matches Nandi's estimate that ~7% of each genome arrives from an unsampled source. That makes it the best-shaped tool in this section.

**The trap:** it cannot identify the direction of *ancestral* recombination, and resolves this by **always marking the lineage with fewer strains as the recipient**. On a 59.6%-Thailand collection that heuristic will mechanically declare Australia the recipient of Thai gene flow. If fastGEAR is used, restrict it to *recent* events where direction is identifiable, exactly as van Hal did, and state the constraint.

### 7.5 ARG methods are two orders of magnitude short

> Vaughan TG, Welch D, Drummond AJ, Biggs PJ, George T, French NP. "Inferring ancestral recombination graphs from bacterial genomic data." *Genetics.* 2017;205(2):857–70. PMID 28007885

This verifies and quantifies the review's existing claim. **bacter** was demonstrated at **23 taxa × 53 rMLST loci, roughly one week per chain**, and validated at 5–10 leaves; the authors describe the problem as "not in any way solved," and note the crossover-coalescent formulation is inappropriate for bacteria.

**Searched for and not found**, each as a separate query: tsinfer/tskit on bacterial genomes; ARGweaver on bacteria; Relate on bacteria; SINGER on bacteria; TreeMix on bacterial genomes; f3/f4/D-statistics/qpAdm on bacterial genomes. This closes the handoff's open question with a documented absence.

### 7.6 The existence proof for tree-free source attribution

> Wilson DJ, Gabriel E, Leatherbarrow AJH, Cheesbrough J, Gee S, Bolton E, Fox A, Fearnhead P, Hart CA, Diggle PJ. "Tracing the source of campylobacteriosis." *PLoS Genet.* 2008;4(9):e1000203. PMID 18818764

> "We use multilocus sequence typing to genotype **1,231 cases of *C. jejuni***… **By modeling the DNA sequence evolution and zoonotic transmission of *C. jejuni* between host species and the environment, we assign human cases probabilistically to source populations.**"

A probabilistic, tree-free assignment of individual isolates to source populations in a highly recombinogenic bacterium, at n > 1,200, producing an actionable directional answer.

**Its dependency is the whole point, and it is also the review's best concrete recommendation.** Source attribution requires **reference panels from each candidate source, sampled independently of the cases**. The Campylobacter work had chicken, cattle, sheep, swine, wild bird and environmental panels. The *B. pseudomallei* analogue would be **geographically balanced environmental reference panels** — an Australian soil panel and a Thai soil panel at comparable depth. The current 59.6/10.2 clinical imbalance is precisely the wrong shape. Building those panels is a higher-value investment than any modelling choice in this document.

---

## 8. The Australian-origin hypothesis

Worth a section because it is the phylogeographic claim this pipeline would be re-testing, and because the sampling critique cuts less deeply than expected.

**Pillar 1 — Pearson 2009**, and note it was already partly tree-free:

> Pearson T, Giffard P, Beckstrom-Sternberg S, et al. "Phylogeographic reconstruction of a bacterial species with high levels of lateral gene transfer." *BMC Biol.* 2009;7:78. PMID 19922616

STRUCTURE 2.2 on **601 STs × 7 MLST loci from >1,700 isolates**, plus Φ_PT and eBURST, alongside a Bayesian tree from >14,000 orthologous SNPs across 43 genomes. The population split: "**Φ_PT = 0.117; P = 0.001**"; divergence from an estimated ancestral population "**F_ST = 0.03 and 0.21 for the Australasian and Southeast Asian populations, respectively**."

**The sample was near-balanced** — "approximately **47% of STs are from Southeast Asia, 45% are from Australasia**, and 8% are from other geographic regions" — and they ran two explicit anti-bias checks:

> "**Increasing the value of K retained the two major populations but with further subdivision in both, indicating that the coherence of either population is not merely an artefact of intensive sampling in a single geographic region.**"

> "STs from *B. mallei* did not form a separate population even as K was increased… **again suggesting that the observed patterns are not the result of uneven geographic sampling**."

But they state the load-bearing assumption plainly: "**The conclusions that we draw are contingent on an Australian root to this tree**," and call it a "provisional hypothesis."

*(One unit caution for the review: Pearson's "18 to 30 times more likely to change by recombination rather than mutation" is a* per-allele MLST *ratio and must not be merged with Nandi's genome-wide r/m = 7.2. Gap 5 already flags the analogous error for the "more than twice* S. pneumoniae*" claim.)*

**Pillar 2 — Chewapreecha 2017**, including the alternative she does not exclude:

> "Isolates from Australasia had longer phylogenetic branches compared to isolates from other regions, indicative of greater genetic diversity. This was also observed from the pan-genome analysis, which confirmed that the Australasian [*B. pseudomallei*] population had the **highest rate of new gene discovery and the largest accessory genome**. Examination of data distribution confirmed that this finding was not related to different sampling periods or sequencing platforms."

> "**These observations provide evidence for the hypothesis that Australia was an early reservoir… An alternative explanation is that there have been repeated population bottlenecks outside Australia, but not within it.**"

That second sentence is the most important quotation in this section. A recent bottleneck outside Australia and an Australian origin are exactly the two histories Lawson et al. 2018 show are indistinguishable from an admixture bar plot, and neither PCA nor an F_ST tree separates them either.

Her own sampling admission is also quotable:

> "**A very limited number of isolates had been stored and were available in areas where melioidosis is either uncommon or under-reported based on lack of microbiology infrastructure, which resulted in an unequal geographic representation.**"

> "The phylogenies also highlighted an African root for this group (100% bootstrap support), **implying an African origin of the American isolates based on our sampling density**."

**Where this leaves the claim.** Better supported than a naive critique implies, because Pearson's sample was balanced and he checked. Not established, because the root is contingent on outgroup choice, the bottleneck alternative is untested, and De Maio's result specifically concerns "migration rates **and root locations**" under biased sampling.

**A reporting gap in the directional claim itself, found while retrieving the SI.** Chewapreecha's stochastic character mapping ran phytools v0.5-10 under an asymmetric (ARD) model, 1,000 simulations across 1,000 subsampled trees. **But the paper reports no transition rate matrix, no per-transition directional rates, and no per-transition support.** The only inferential statistics given for the geography analysis are two aggregate Mann–Whitney p-values, both stated as "<2.2 × 10⁻¹⁶" — which is R's floor, not a computed value. So the headline directional conclusions ("Australia as early reservoir, onward transmission to Southeast then South and East Asia") are not accompanied by the quantities that would let a reader assess them, and cannot be reproduced or compared against from the paper as published.

That is worth stating plainly, because it is the specific thing this pipeline could do better at no methodological risk: **report the full ARD rate matrix with its uncertainty across resamples.** Section 4 already establishes that the between-replicate spread over subsamples *is* the sampling-uncertainty estimate; publishing it is a strict improvement on the reference study.

**Searched for and not found: any paper that critiques or re-examines the *B. pseudomallei* Australian-origin hypothesis on sampling-bias grounds.** The strongest existing statement is Chewapreecha's own one sentence. Testing the bottleneck alternative — with badMIXTURE residuals, or with a demographic model fitted per region — is an available and currently unclaimed contribution.

---

## 9. Replicon choice is a dating decision, not just an alignment decision

Carried forward from the Gap 3 pass and completed here, because it changes how a dating result must be reported.

Chewapreecha ran BEAST separately on chromosome I and chromosome II for every cluster. The spread that produced is not a rounding difference. On the American isolates the TMRCA is **1806 from chromosome I and 1759 from chromosome II** — 47 years apart on the same isolates — and their handling was to report both with a combined HPD rather than choose. Chromosome I of group 4 failed to reach a credible ESS while chromosome II succeeded. Their date-randomisation ranks are reported per chromosome, and both the best and the worst (34th and 97th of 1,000) fall on chromosome II.

Two details retrieved this pass sharpen that. The Group 4 chromosome I run is the one that failed ESS — "the estimation for group 4 chromosome I did not reach a credible ESS and was excluded from the analysis" — so that cluster is dated on chromosome II alone. And the "combined" American HPD is not a combination at all but the outer envelope of two independent runs (§5.4).

The mechanistic argument for keeping them separate is stronger than the observation that they disagree:

> Dillon MM, Sung W, Lynch M, Cooper VS. "The rate and molecular spectrum of spontaneous mutations in the GC-rich multichromosome genome of *Burkholderia cenocepacia*." *Genetics.* 2015;200(3):935–946. PMID 25971664

In *B. cenocepacia* the chromid has the **lowest spontaneous mutation rate of the three replicons yet the highest observed evolutionary rate**. So per-replicon rate differences in nature are selection and recombination, not mutation. A single clock across a concatenation of chromosome I and chromosome II is therefore not merely imprecise — it is averaging over two replicons known to be under different regimes, in a genus where that has been measured.

This compounds with Gap 3's finding that Gubbins cannot handle multi-contig references at all and that `snp-sites` hardcodes `CHROM` to `"1"`. The replicon split is forced on you by the tooling; treat the dating consequence as a benefit rather than an inconvenience, and **report per-replicon estimates separately with their disagreement visible**, following Chewapreecha. Concordance between replicons is a free check that a date is real; discordance of the 1759-versus-1806 kind is itself a publishable result about the limits of the method.

---

## 10. Stochastic character mapping — what changed since 2017, and what happens if dating fails

Read from the current phytools reference manual, **version 2.5-2, dated 2025-09-18**. Chewapreecha used **v0.5-10**. That is eight years and a major version, and four things follow.

**The default model is `SYM`, not `ARD`.** Usage is `make.simmap(tree, x, model="SYM", nsim=1, ...)`. Chewapreecha's asymmetric model was therefore a deliberate override, not the default — worth saying, because an asymmetric model is the right choice for directional geographic claims and it should be justified rather than inherited.

**The root prior is where sampling frequency leaks in, and it is an argument you must set explicitly.** Verbatim: "`pi` gives the prior distribution on the root node of the tree. Acceptable values for `pi` are `"equal"`, `"estimated"`, or a vector with the frequencies. **If `pi="estimated"` then the stationary distribution is estimated by numerically solving pi\*Q=0 for pi, and this is used as a prior on the root.** … The function defaults to `pi="equal"` which results in the root node being sampled from the conditional scaled likelihood distribution at the root."

That is the §4.3 problem in the ancestral-state setting: `pi="estimated"` derives the root prior from the fitted rate matrix, which was itself fitted to tip states whose frequencies are the sampling distribution. **Use `pi="equal"` and say so**, or report both and show the difference.

**There is a documented root-node sampling bug in the version era Chewapreecha used, and the paper does not report `pi`.** Verbatim: "Giorgio Bianchini pointed out that in **phytools 1.0-1 (and probably prior recent versions) there was an error sampling the state at the root node of the tree based on the input prior (`pi`) supplied by a user** – except for `pi="equal"` (a flat prior, the default) or for a prior distribution in which one or another state was known to be the global root state. All of these issues should be fixed in the current and all later versions."

So: if Chewapreecha left `pi` at its default, the result stands. If they supplied a custom root prior, the root-state sampling in v0.5-10 falls inside the flagged range. **The paper does not state which.** Since the root state is precisely the "Australia as early reservoir" claim, this is worth one re-run on current phytools rather than an assumption. *(Two earlier bugs — an ARD-specific bug between 0.2-26 and 0.2-36, and a root conditional-likelihood error between 0.2-33 and 0.2-47 — both predate v0.5-10 and do not apply.)*

**And the answer to the handoff's question: yes, stochastic mapping still runs if dating fails — but the units of the answer change, and one of Chewapreecha's two reported quantities stops being meaningful.** `make.simmap` takes "a phylogenetic tree as an object of class `phylo`"; **no ultrametric or time-calibrated requirement appears anywhere in the documentation**, and the likelihood is computed by Felsenstein pruning adapted from ape's `ace`, which needs only branch lengths. So a Gubbins-corrected, substitution-scaled tree is valid input.

But look at what comes back. The `maps` element is "a list of named vectors containing the **times spent in each state** on each branch," and `mapped.edge` is "a matrix containing the total **time** spent in each state along each edge." Those "times" are in **the tree's own branch-length units**. On a substitution-scaled tree they are *substitutions*, not years.

Chewapreecha reported two things from simmap: "**the transitions between different geographical characters** and **the total time spent in each geographical character**." The first survives an undated tree unchanged — a count of transitions is a count of transitions. **The second does not.** On an undated tree "total time spent in Thailand" becomes "total substitutions accumulated in Thailand," which confounds residence time with lineage-specific rate — and §9 establishes that rate varies between replicons for reasons of selection and recombination. **Report transition counts and directions from undated trees; do not report occupancy times unless the tree is dated.**

**One upgrade worth taking.** The `Q` argument accepts `"empirical"` (the default — fit a single most-likely Q and simulate under it), `"mcmc"` (sample `nsim` values of Q from its posterior via Bayesian MCMC, then simulate one map per sampled Q), or a fixed matrix. Given how small the effective sample is here (§4.2), `Q="mcmc"` is the better choice: it propagates uncertainty in the rate matrix instead of conditioning on a point estimate.

**Independent confirmation of the tree-requirement finding.** Direct inspection of the current CRAN sources finds **zero occurrences of `ultrametric` in either `make.simmap.R` or `fitMk.R`** — no `is.ultrametric()` guard, no `force.ultrametric()` call, no warning. Branch lengths appear only as a scalar multiplying Q inside a matrix exponential: `P[[i]]<-expm(Q*tt$edge.length[i])`. So the documentation reading above is confirmed at the level of the code. One further consequence to state precisely: on a phylogram, **Q has units of expected geographic transitions per substitution per site**, which means *comparing Q across clusters whose substitution rates differ silently conflates the molecular clock with the geographic process*. Given §5.5, those rates do differ. Report Q per cluster; do not pool or compare it across clusters unless the trees are dated.

There is also a hard asymmetry worth stating once: **stochastic mapping survives the loss of dating; birth–death sampling models do not.** BDSky and MTBD are defined in per-calendar-time rates by construction, and **searched for and not found: any BDSky/MTBD variant defined on a non-dated or substitution-scaled tree.** So for the clusters that fail dating, the sampling-proportion-as-parameter route (§3.6) is closed outright, while simmap remains available.

### 10.1 Model choice needs reporting, and ARD is expensive here

phytools defers model definitions to ape's `ace`: ER has 1 rate, SYM has *k*(*k*−1)/2, ARD has *k*(*k*−1). **For Chewapreecha's six-country trait that is ER = 1, SYM = 15, ARD = 30 free rate parameters estimated from 90 tips** — a 3:1 tip-to-parameter ratio. That number should be reported.

Revell's own worked example in the phytools 2.0 paper does not declare a winner; it fits competing models, reports AIC and Akaike weights, and ends with two models near-tied. Boyko 2026 (*Syst Biol*, PMID 41746276) goes further, showing that model-set choice **moves the ancestral reconstruction itself** and warning of "the dangers of an over-reliance on default model sets." And Beaulieu, O'Meara & Donoghue 2013 (PMID 23676760) note that "with trees comprised of larger, older, and globally distributed clades, it is likely that the lability of a binary character will differ significantly among lineages, which could lead to errors in estimating transition rates and the associated inference of ancestral states."

**And a simulation study argues specifically against ARD here, while also undercutting the obvious "just use AIC" fix.** "What is the best method for estimating ancestral states from discrete characters?" (bioRxiv 2023, [10.1101/2023.08.31.555762](https://doi.org/10.1101/2023.08.31.555762); 500 characters, 15 Markov generating models, 8–256 tips, three topologies) reports, verbatim:

> "**The ER model frequently outperforms the ARD model, even when data are simulated using unequal rates.** … These results suggest that **ARD models may be overparameterized when character data is limited.**"

> "Surprisingly, difference in error between likelihood models is a poor predictor of difference in model fitness; **better fitting models are not necessarily more accurate.**"

> "However, there is a strong correlation between model uncertainty and model error; **likelihood models with more certain ancestral state estimates are typically more accurate.**"

> "Using empirical morphological datasets, I demonstrate that **applying different methods often results in substantively different ancestral state estimates.**"

The second quote is the awkward one, because it says model selection by fit — the Revell/Boyko workflow — is not a reliable route to accuracy. Taken together with the parameter count above, the position shifts:

**Defensible position: default to ER, not ARD.** Fit ER, SYM and ARD per cluster and report ΔAIC and Akaike weights for transparency, but do not treat an ARD win on AIC as licence to use it — at 30 free parameters from 90 tips this is exactly the "character data is limited" regime where ARD is reported to lose to ER even when the truth is asymmetric. Where an asymmetric model is genuinely needed for the scientific question (directional migration is asymmetric by nature), report both ER and ARD results and show that the conclusion does not depend on the choice. And **report estimate certainty per node**, since that — not model fit — is what tracks accuracy.

This also reframes Chewapreecha's choice. Their ARD was a deliberate override of the `SYM` default, appropriate to a directional question, but with 30 parameters from 90 tips and no reported rate matrix (§8) there is no way for a reader to judge whether it was over-parameterised. Reporting the matrix and an ER comparison is a cheap, strict improvement.

### 10.2 Pooling across resampled trees is not well defined — a real hole

This qualifies §4's resampling recommendation at the implementation level, and it is a documented absence rather than an oversight.

Every phytools summarisation facility — `describe.simmap`/`summary.multiSimmap`, `densityMap`, `countSimmap`'s multiSimmap branch — is built around trees that **share a topology and tip set**; the `check.equal` and `check` arguments exist precisely to enforce that. **Searched for and not found: any phytools facility or published methodological guidance for pooling stochastic-map output across trees with *different tip sets*.** That is exactly what a Chewapreecha-style "subsample, re-run, repeat 1,000 times" design produces.

What follows practically:

- **Node-level posteriors cannot be pooled across replicates**, because the internal nodes are not the same nodes. Any figure captioned "posterior probability at node X" summed over differently-subsampled trees is not well defined.
- **Only tree-level scalars are poolable**: the count of *i*→*j* transitions from `countSimmap`, and the root state. And they pool as a **distribution over replicates** — a bootstrap-style interval — **not as a Bayesian posterior.**

State this explicitly in the methods, and restrict the summary to those two quantities reported as intervals across resamples. On the number of simulations, Revell's guidance is that 100–1,000 is the conventional range and 1,000 is defensible; no numeric convergence diagnostic for transition counts is specified anywhere.

### 10.3 The prior literature on ASR under biased tips, in one place

- **Goldberg EE, Igić B 2008** (*Evolution* 62(11):2727–2741, PMID 18764918) identify "two major causes of errors: **incorrect assignment of root state frequencies**, and neglect of the effect of the character state on rates of speciation and extinction," and go as far as "we demonstrate devastating flaws in the methods that are the foundation of all such studies." Root-state frequency assignment is precisely what unbalanced tips corrupt, and precisely what the `pi` argument controls (§10).
- **Wright AM, et al. 2015** (*J Exp Zool B* 324(6):504–516, PMID 26227660) report the counter-intuitive result that "**a method that is designed to account for biases in taxon sampling actually accentuates, rather than lessens, those biases** with respect to ancestral state reconstructions."
- **Maddison & FitzJohn 2015** (*Syst Biol* 64(1):127–136, PMID 25209222) show that apparent correlated evolution is often spurious "particularly when the dependent relationship stems from a **single replicate deep in time**" — which is the exact shape of one hospital-network study contributing a single deep clade of 1,265 isolates.
- *(Citation caution carried forward: Litsios & Salamin 2012 is* Syst Biol *61(3):533–538, PMID 22223447, **not** BMC Evol Biol. And Salisbury & Kim 2001 could not be located in PubMed under any tried combination — do not cite without independent confirmation.)*

---

## 11. Verification status

The distinction between "the paper does not report this" and "I could not retrieve it" matters for what can be claimed, so they are separated.

### 11.1 Genuine non-reports — these are findings, not gaps

**Two papers cite a "Supplementary Table 1" that does not exist.** Chewapreecha 2017 and Limmathurotsakul 2016 both reference supplementary tables in their main text; both Supplementary Information files were retrieved in full and both contain **only figures and methods**. In Chewapreecha's case the clock rates turned out to be inside a figure *panel* (§5.4). In Limmathurotsakul's, the country-level burden numbers appear only as binned cartogram legends (§1). Worth knowing as a general retrieval lesson: in this literature, "supplementary table" is not a reliable signal that a table exists.

**Chewapreecha's core-genome alignment length is never reported. This closes the item Gap 1 left open.** The full 27-page Supplementary Information was retrieved and text-extracted, then searched for `core genome`, `alignment`, `K96243`, `bp`, `Mb`, `kb`, `base pair` and every 6–9-digit numeric token. No alignment length appears anywhere — not total, not per chromosome, in neither main text nor SI.

**The ~772 kb divergence denominator is unverifiable and the underlying quantity is undefined.** The two reported figures are internally consistent with ≈772 kb (5,650 SNPs ÷ 0.0073 = 774,000; 43,221 ÷ 0.0561 = 770,428), so the pairing is almost certainly right. But 772 kb is only **10.7% of K96243's 7,247,547 bp**, which is implausibly small for anything called a core genome of this organism; and the alternative decimal reading implies ~7.72 Mb, which *exceeds* the reference and is impossible. **Neither reading reconciles.** "Genetic divergence compared with the K96243 core genome" is not defined anywhere in the paper. Stop propagating the 772 kb figure; flag the ambiguity instead.

Also genuine non-reports in Chewapreecha: **no ESS values** anywhere, only the >200 pass/fail threshold; **no per-cluster marginal likelihoods**, despite running stepping-stone and path sampling; **no rates in SNPs per genome per year**; and **no transition rate matrix or per-transition support** for the stochastic character mapping (§8).

**Seng et al. 2024's date-randomisation result is never reported.** The Methods describe 100 permutations; no p-value, rank or percentile appears in the main text, the 12-page Supplementary Information, or the Peer Review File. The SI has zero occurrences of "randomis\*", "root-to-tip", "BactDating", "temporal" or "clock", and contains no temporal-signal figure. Established by exhaustive text search of retrieved files.

**Seng's reference [53] is a mis-citation.** The sentence "The prior mutation rate derived from Pearson and colleagues[53] was used" points unambiguously (`xref rid="CR53"` → `ref id="CR53"`, labelled "53.") to **Spring-Pearson SM, et al. "Pangenome analysis of *Burkholderia pseudomallei*…" *PLoS ONE* 2015;10:e0140274, PMID 26484663** — a pangenome and gene-order paper. Term counts in its full text: "mutation rate" 0, "per site per year" 0, "molecular clock" 0, "clock" 0, "BEAST" 0, "dating" 0. Note also that the first author is Spring-Pearson SM, not Pearson T. Confirmed by two independent routes.

On the software side: there is no published minimum-tips or minimum-dated-tips threshold for BactDating, no BactDating guidance on multi-replicon analysis, and `clusteredTest()` is documented nowhere outside its source file.

### 11.2 Searched-for absences — each is a defensible claim of novelty

Each of the following was searched for specifically and not found:

- Any controlled benchmark of **GLM-extended DTA under sampling bias**. Layan et al. tested MASCOT-GLM, not the CTMC analogue, and say so.
- Any application of the **structured coalescent to *B. pseudomallei*** (MASCOT, BASTA, MultiTypeTree, SCOTTI, bdmm).
- Any assessment of whether **DTA or the structured coalescent is more robust to residual recombination** in bacteria.
- Any application of **ChromoPainter, fineSTRUCTURE, fastGEAR, ADMIXTURE, STRUCTURE or DAPC to *Burkholderia* whole genomes** (Pearson 2009's STRUCTURE on 7-locus MLST is the sole exception).
- **tsinfer/tskit, ARGweaver, Relate, SINGER, TreeMix, or f3/f4/D-statistics/qpAdm applied to bacterial genomes** — each queried separately.
- Any paper **re-examining the *B. pseudomallei* Australian-origin hypothesis on sampling-bias grounds**.
- Any bacterial paper publishing a **relative-time (substitution-scaled) tree as the headline deliverable** because temporal signal was absent.
- Any treatment of **within-country study-block clustering** (BioProject, hospital network) as a phylogeographic confounder.

### 11.3 Retrieval failures — get these manually

**Resolved after the first draft**, when the source PDFs were supplied and the audit query was re-run:

| Item | Outcome |
|---|---|
| **Didelot & Parkhill 2022, *Phil Trans R Soc B* 20210246** | **Obtained and read in full — see §5.0.** It settles the masked-alignment-versus-clonal-genealogy question outright and supplies the missing-dates, rooting and randomisation-count guidance. |
| **The third large Thai BioProject** | **Resolved: PRJEB3409** — see §4.2a. A Wellcome Sanger case-control study, 1,506 assemblies, 56.9% environmental, 93.6% undated. |
| Viberg et al. 2017 within-host rates | **Verified from the primary source** — §5.5. |
| Limmathurotsakul 2016 **Supplementary Table 1** | **Does not exist.** The SI was retrieved in full and contains only Supplementary Figures 1–9 plus Methods; there are no supplementary tables, despite the main text citing "Supplementary Information Table 1". Figure 8's binned cartogram is the usable substitute (§1). |
| Müller, Rasmussen & Stadler 2017 *MBE* | PDF supplied; the deme-limit claims in §3.3 remain quoted from the 2018 restatement, which is the stronger and more explicit statement anyway. |

**Still outstanding:**

| Item | Why it matters | What blocked it |
|---|---|---|
| beast.community **BETS tutorial** | GSS path-step counts and XML settings for §6.6 step 3 | classifier-blocked; a PDF was supplied but not yet mined |
| Roberts et al. 2025 full *V. cholerae* results | Whether they discuss recombination validity — it is one of §11.2's claimed absences and I would rather it be a checked absence | publisher HTML truncated |
| Wilson et al. 2008 full text | Verbatim methods for source attribution | PMC ID lookup returned the wrong article |
| "A simple correction to DTA sampling biases" ([10.1101/2023.11.21.568020](https://doi.org/10.1101/2023.11.21.568020)) | Unread entirely; may or may not be relevant to §4 | bioRxiv HTTP 429 |
| Croucher 2011, Harris 2010, Young 2012 rate values | Comparator rows in §5.5 | not yet checked against primary sources |

### 11.4 Additional documented absences from the subsampling and ASR pass

Beyond §11.2, each of the following was searched for and not found, and each is a legitimate finding:

- A head-to-head benchmark of **random vs stratified vs diversity-preserving vs temporal subsampling** measured against phylogeographic conclusions. Both Featherstone 2022 and Attwood 2022 state the protocol does not exist.
- **Inverse-probability or importance weighting of tips inside a phylogenetic likelihood.** Nothing assigns tips a weight *w* = 1/π from an estimated sampling probability. The field only adds observations, removes them, imports external covariates, or reweights the null.
- Any phytools facility or published guidance for **pooling stochastic maps across trees with different tip sets** (§10.2).
- A **phylogenetic effective sample size for a discrete trait** under an Mk/CTMC model; an **"effective number of independent isolates"**; any application of **design effect or ICC** to pathogen genomic data (§4.2b).
- Published justification for the near-universal **one-isolate-per-patient deduplication** convention.
- **Study of origin / BioProject as a random effect** in bacterial genomics (§4.2b).
- **Balanced-subsample re-clustering with a partition-agreement statistic**, in bacteria (§4.2c).
- A **non-dated variant of BDSky or MTBD** usable when dating fails (§10).
- A **phytools NEWS/ChangeLog** — none exists; version history lives only in `.Rd` Note sections and a blog.
- **Per-field metadata-completeness statistics** for public bacterial genome archives. Blackwell et al. quantify project- and species-level skew but not the fraction missing country or collection date.

### 11.5 Confidence flags

The Chewapreecha values in §5.4 and §6.7 were read directly from the retrieved Supplementary Information and are **verified**. The comparator rates in §5.5 (Viberg 2017, Lieberman 2011, Croucher 2011, Harris 2010, Young 2012) were assembled at one remove and are **not** independently verified — check each against its primary source before citing. And one figure that circulates second-hand, a pooled Chewapreecha rate of **1.03 × 10⁻⁶**, appears nowhere in the paper or SI and **must not be cited**.

---

## 12. Citation table

Corrections to identifiers used in earlier passes are marked **⚠**.

### Sampling bias and phylogeographic model choice

| Role | Citation | PMID | DOI |
|---|---|---|---|
| **Burden denominator — the §1 argument** | Limmathurotsakul D, Golding N, Dance DAB, et al. Predicted global distribution of *Burkholderia pseudomallei* and burden of melioidosis. *Nat Microbiol* 2016;1:15008 | 26877885 | [10.1038/nmicrobiol.2015.8](https://doi.org/10.1038/nmicrobiol.2015.8) |
| **DTA critique; BASTA** | De Maio N, Wu C-H, O'Reilly KM, Wilson D. New routes to phylogeography: a Bayesian structured coalescent approximation. *PLoS Genet* 2015;11(8):e1005421 | 26267488 | [10.1371/journal.pgen.1005421](https://doi.org/10.1371/journal.pgen.1005421) |
| **The decisive benchmark** | Layan M, Müller NF, Dellicour S, De Maio N, Bourhy H, Cauchemez S, Baele G. Impact and mitigation of sampling bias… *Virus Evol* 2023;9(1):vead010 | 36860641 | [10.1093/ve/vead010](https://doi.org/10.1093/ve/vead010) |
| Dose–response curve for sampling bias ⚠ *not Phil Trans R Soc B* | Kalkauskas A, Perron U, Sun Y, Goldman N, Baele G, Guindon S, De Maio N. Sampling bias and model choice in continuous phylogeography. *PLoS Comput Biol* 2021;17(1):e1008561 | 33406072 | [10.1371/journal.pcbi.1008561](https://doi.org/10.1371/journal.pcbi.1008561) |
| Detection vs survey sampling schemes | Guindon S, De Maio N. Accounting for spatial sampling patterns in Bayesian phylogeography. *PNAS* 2021;118(52):e2105273118 | 34930835 | [10.1073/pnas.2105273118](https://doi.org/10.1073/pnas.2105273118) |
| MASCOT | Müller NF, Rasmussen D, Stadler T. MASCOT… *Bioinformatics* 2018;34(22):3843–3848 | 29790921 | [10.1093/bioinformatics/bty406](https://doi.org/10.1093/bioinformatics/bty406) |
| Structured coalescent approximations (theory) | Müller NF, Rasmussen DA, Stadler T. The structured coalescent and its approximations. *Mol Biol Evol* 2017;34(11):2970–2981 | 28666382 | [10.1093/molbev/msx186](https://doi.org/10.1093/molbev/msx186) |
| O(N·S³)/O(N²·S²) complexity | Shao Y, Suchard MA, Rambaut A, Ji X, Lemey P, Vasylyeva TI, Baele G. Parallel algorithms for phylogenetic inference under a structured coalescent approximation. bioRxiv 2025 | 41040339 | [10.1101/2025.09.22.677844](https://doi.org/10.1101/2025.09.22.677844) |
| MTBD ⚠ *MBE 2016, not J R Soc Interface* | Kühnert D, Stadler T, Vaughan TG, Drummond AJ. Phylodynamics with migration… *Mol Biol Evol* 2016;33(8):2102–2116 | 27189573 | [10.1093/molbev/msw064](https://doi.org/10.1093/molbev/msw064) |
| MTBD tip ceiling 250→500 | Scire J, Barido-Sottani J, Kühnert D, Vaughan TG, Stadler T. *Viruses* 2022;14(8):1648 | 36016270 | [10.3390/v14081648](https://doi.org/10.3390/v14081648) |
| Exact SC on bacteria (*S. aureus*, *V. cholerae*) | Roberts I, Everitt RG, Koskela J, Didelot X. *PLoS Comput Biol* 2025;21(4):e1012995 | 40258093 | [10.1371/journal.pcbi.1012995](https://doi.org/10.1371/journal.pcbi.1012995) |
| **Large bacterial phylogeography declines this method family** | Belman S, Pesonen H, Croucher NJ, Bentley SD, Corander J. Estimating between-country migration in pneumococcal populations. *G3* 2024;14(6):jkae058 | 38507601 | [10.1093/g3journal/jkae058](https://doi.org/10.1093/g3journal/jkae058) |
| Sampling-aware ASR at 10⁵ tips | Song Y, Gill I, MacPherson A, Colijn C. SAASI: sampling aware ancestral state inference. *Nat Commun* 2026;17(1) | 42115598 | [10.1038/s41467-026-72851-5](https://doi.org/10.1038/s41467-026-72851-5) |
| Adjusted Bayes factor for DTA | Gámbaro F, Layan M, Baele G, Vrancken B, Dellicour S. *Mol Biol Evol* 2025;42(11):msaf253 | — | [10.1093/molbev/msaf253](https://doi.org/10.1093/molbev/msaf253) |
| GLM-extended DTA | Lemey P, Rambaut A, Bedford T, et al. *PLoS Pathog* 2014;10(2):e1003932 | 24586153 | [10.1371/journal.ppat.1003932](https://doi.org/10.1371/journal.ppat.1003932) |
| Unbalanced sampling → spurious K=2 | Meirmans PG. *Heredity* 2018;122(3):276–287 | — | — |

### Dating and temporal signal

| Role | Citation | PMID | DOI |
|---|---|---|---|
| BactDating | Didelot X, Croucher NJ, Bentley SD, Harris SR, Wilson DJ. *Nucleic Acids Res* 2018;46(22):e134 | 30184106 | [10.1093/nar/gky783](https://doi.org/10.1093/nar/gky783) |
| ARC/CARC — the additivity argument | Didelot X, Siveroni I, Volz EM. *Mol Biol Evol* 2021;38(1):307–317 | 32722797 | [10.1093/molbev/msaa193](https://doi.org/10.1093/molbev/msaa193) |
| TreeTime | Sagulenko P, Puller V, Neher RA. *Virus Evol* 2018;4(1):vex042 | 29340210 | [10.1093/ve/vex042](https://doi.org/10.1093/ve/vex042) |
| DRT criteria CR1/CR2 ⚠ **PMID was wrong in the handoff** | Duchêne S, Duchêne D, Holmes EC, Ho SYW. *Mol Biol Evol* 2015;32(7):1895–1906 | **25771196** (not 26069215) | [10.1093/molbev/msv056](https://doi.org/10.1093/molbev/msv056) |
| **DRT anticonservative under structure; clustered permutation** | Murray GGR, Wang F, Harrison EM, et al. *Methods Ecol Evol* 2016;7(1):80–89 | 27110344 | [10.1111/2041-210X.12466](https://doi.org/10.1111/2041-210X.12466) |
| **BETS** ⚠ **PMID was wrong in the handoff** | Duchene S, Lemey P, Stadler T, Ho SYW, Duchene DA, Dhanasekaran V, Baele G. *Mol Biol Evol* 2020;37(11):3363–3379 | **32895707** (not 32895713) | [10.1093/molbev/msaa163](https://doi.org/10.1093/molbev/msaa163) |
| BETS prior sensitivity / tree extension | Tay JH, Kocher A, Duchene S. *PLoS Comput Biol* 2024;20(11):e1012371 | 39502105 | [10.1371/journal.pcbi.1012371](https://doi.org/10.1371/journal.pcbi.1012371) |
| Root-to-tip pseudoreplication | Rieux A, Balloux F. *Mol Ecol* 2016;25(9):1911–1924 | 26880113 | [10.1111/mec.13586](https://doi.org/10.1111/mec.13586) |
| Field-wide failure base rate (8/36) | Duchêne S, Holt KE, Weill F-X, et al. *Microb Genom* 2016;2(11):e000094 | 28348834 | [10.1099/mgen.0.000094](https://doi.org/10.1099/mgen.0.000094) |
| **Negative-result template (13/31 failed)** | Menardo F, Duchêne S, Brites D, Gagneux S. *PLoS Pathog* 2019;15(9):e1008067 | — | [10.1371/journal.ppat.1008067](https://doi.org/10.1371/journal.ppat.1008067) |
| Post-hoc dated-tree diagnostics | Didelot X, Carson J, Ribeca P, Volz E. DiagnoDating. *Mol Biol Evol* 2026;43(4):msag093 | — | [10.1093/molbev/msag093](https://doi.org/10.1093/molbev/msag093) |
| **Rate prior (the one Seng used)** | Pearson T, Sahl JW, Hepp CM, et al. *PLoS Pathog* 2020;16(3):e1008298 | 32149236 | [10.1371/journal.ppat.1008298](https://doi.org/10.1371/journal.ppat.1008298) |
| Within-host rate ⚠ *first author Viberg, not Price* | Viberg LT, Sarovich DS, Kidd TJ, et al. *mBio* 2017;8(2):e00356-17 | 28400528 | [10.1128/mBio.00356-17](https://doi.org/10.1128/mBio.00356-17) |
| Chewapreecha's rate benchmark — *B. dolosa*, not *B. pseudomallei* | Lieberman TD, et al. *Nat Genet* 2011;43(12):1275–80 | 22081229 | [10.1038/ng.997](https://doi.org/10.1038/ng.997) |
| No temporal signal over 25 yr | Chapple SNJ, et al. *Microb Genom* 2016;2:e000067 | 28348862 | — |
| No temporal signal over 51 yr | Webb JR, et al. *mSystems* 2020;5:e00726-20 | 33172968 | — |

### Tree-free / population-genetic

| Role | Citation | PMID | DOI |
|---|---|---|---|
| **ADMIXTURE — the decisive warning** | Lawson DJ, van Dorp L, Falush D. A tutorial on how not to over-interpret STRUCTURE and ADMIXTURE bar plots. *Nat Commun* 2018;9:3258 | 30108219 | [10.1038/s41467-018-05257-7](https://doi.org/10.1038/s41467-018-05257-7) |
| ChromoPainter / fineSTRUCTURE | Lawson DJ, Hellenthal G, Myers S, Falush D. *PLoS Genet* 2012;8(1):e1002453 | 22291602 | [10.1371/journal.pgen.1002453](https://doi.org/10.1371/journal.pgen.1002453) |
| Painting in bacteria; the sampling caveat | Yahara K, Furuta Y, Oshima K, et al. *Mol Biol Evol* 2013;30(6):1454–64 | 23505045 | [10.1093/molbev/mst055](https://doi.org/10.1093/molbev/mst055) |
| **Best >1,000-genome bacterial template** | van Hal SJ, et al. *Lancet Microbe* 2022;3(2):e133–41 | 35146465 | [10.1016/S2666-5247(21)00236-6](https://doi.org/10.1016/S2666-5247(21)00236-6) |
| Largest painting run (4,067 genomes) | Zhu M, et al. *Helicobacter* 2025;30(2):e70025 | 40059062 | [10.1111/hel.70025](https://doi.org/10.1111/hel.70025) |
| fastGEAR | Mostowy R, Croucher NJ, Andam CP, Corander J, Hanage WP, Marttinen P. *Mol Biol Evol* 2017;34(5):1167–82 | 28199698 | [10.1093/molbev/msx066](https://doi.org/10.1093/molbev/msx066) |
| ARG methods in bacteria — the ceiling | Vaughan TG, Welch D, Drummond AJ, Biggs PJ, George T, French NP. *Genetics* 2017;205(2):857–70 | 28007885 | [10.1534/genetics.116.193425](https://doi.org/10.1534/genetics.116.193425) |
| DAPC | Jombart T, Devillard S, Balloux F. *BMC Genet* 2010;11:94 | 20950446 | [10.1186/1471-2156-11-94](https://doi.org/10.1186/1471-2156-11-94) |
| DAPC fails de novo at F_ST < 0.1 | Miller JM, Cullingham CI, Peery RM. *Heredity* 2020;125(5):269–80 | 32753664 | [10.1038/s41437-020-0348-2](https://doi.org/10.1038/s41437-020-0348-2) |
| DAPC PC-retention rule | Thia JA. *Mol Ecol Resour* 2023;23(3):523–38 | 36039574 | [10.1111/1755-0998.13706](https://doi.org/10.1111/1755-0998.13706) |
| **Tree-free source attribution existence proof** | Wilson DJ, Gabriel E, Leatherbarrow AJH, et al. Tracing the source of campylobacteriosis. *PLoS Genet* 2008;4(9):e1000203 | 18818764 | [10.1371/journal.pgen.1000203](https://doi.org/10.1371/journal.pgen.1000203) |

### Ancestral state reconstruction

| Role | Citation | PMID | DOI |
|---|---|---|---|
| Stochastic character mapping | Huelsenbeck JP, Nielsen R, Bollback JP. Stochastic mapping of morphological characters. *Syst Biol* 2003;52(2):131–138 | — | — |
| **phytools reference manual — §10 is read from this** | Revell LJ. Package 'phytools' **version 2.5-2, dated 2025-09-18** (CRAN, published 2025-09-19). `make.simmap` documentation, pp. 132–134 | — | [CRAN](https://cran.r-project.org/web/packages/phytools/) |
| phytools 2.0 | Revell LJ. phytools 2.0: an updated R ecosystem for phylogenetic comparative methods (and other things). *PeerJ* 2024;12:e16505 | — | [10.7717/peerj.16505](https://doi.org/10.7717/peerj.16505) |
| Root prior option cited in the manual | FitzJohn RG, Maddison WP, Otto SP. *Syst Biol* 2009;58:595–611 | — | — |
| **Root-state frequency assignment as a major error source** | Goldberg EE, Igić B. *Evolution* 2008;62(11):2727–2741 | 18764918 | [10.1111/j.1558-5646.2008.00505.x](https://doi.org/10.1111/j.1558-5646.2008.00505.x) |
| Bias-correcting methods can accentuate bias in ASR | Wright AM, Lyons KM, Brandley MC, Hillis DM. *J Exp Zool B* 2015;324(6):504–516 | 26227660 | [10.1002/jez.b.22642](https://doi.org/10.1002/jez.b.22642) |
| "Single replicate deep in time" | Maddison WP, FitzJohn RG. *Syst Biol* 2015;64(1):127–136 | 25209222 | [10.1093/sysbio/syu070](https://doi.org/10.1093/sysbio/syu070) |
| Model-set choice moves the reconstruction | Boyko JD. *Syst Biol* 2026 | 41746276 | [10.1093/sysbio/syag018](https://doi.org/10.1093/sysbio/syag018) |
| Rate lability across large clades | Beaulieu JM, O'Meara BC, Donoghue MJ. *Syst Biol* 2013;62:725–737 | 23676760 | [10.1093/sysbio/syt034](https://doi.org/10.1093/sysbio/syt034) |
| **ER often beats ARD; model fit ≠ accuracy** | "What is the best method for estimating ancestral states from discrete characters?" bioRxiv, posted 2023-09-01 *(author not shown on the retrieved title page — check before citing)* | — | [10.1101/2023.08.31.555762](https://doi.org/10.1101/2023.08.31.555762) |
| **The pipeline paper** | Didelot X, Parkhill J. A scalable analytical approach from bacterial genomes to epidemiology. *Phil Trans R Soc B* 2022;377(1861):20210246 | — | [10.1098/rstb.2021.0246](https://doi.org/10.1098/rstb.2021.0246) |
| **Within-host rates, verified; continental-signal counterpoint** | Viberg LT, Sarovich DS, Kidd TJ, Geake JB, Bell SC, Currie BJ, Price EP. *mBio* 2017;8(2):e00356-17 | 28400528 | [10.1128/mBio.00356-17](https://doi.org/10.1128/mBio.00356-17) |

### Sampling frame, reporting and study-of-origin

| Role | Citation | PMID | DOI |
|---|---|---|---|
| **Treemmer, and its contraindication for phylogeography** | Menardo F, Loiseau C, Brites D, et al. Treemmer: a tool to reduce large phylogenetic datasets with minimal loss of diversity. *BMC Bioinformatics* 2018;19(1):164 | 29716518 | [10.1186/s12859-018-2164-8](https://doi.org/10.1186/s12859-018-2164-8) |
| **STROME-ID reporting checklist** | Field N, Cohen T, Struelens MJ, et al. *Lancet Infect Dis* 2014;14(4):341–352 | 24631223 | [10.1016/S1473-3099(13)70324-4](https://doi.org/10.1016/S1473-3099(13)70324-4) |
| STROME-ID compliance ~50%, no post-publication improvement | Cheng B, Behr MA, Howden BP, Cohen T, Lee RS. *Lancet Microbe* 2021;2(3):e115–e129 | 33842904 | [10.1016/s2666-5247(20)30201-9](https://doi.org/10.1016/s2666-5247(20)30201-9) |
| "Protocols are required… many questions remain" | Featherstone LA, Zhang JM, Vaughan TG, Duchêne S. *Virus Evol* 2022;8(1):veac045 | 35775026 | [10.1093/ve/veac045](https://doi.org/10.1093/ve/veac045) |
| "Urgently required but not well developed" | Attwood SW, Hill SC, Aanensen DM, Connor TR, Pybus OG. *Nat Rev Genet* 2022;23(9):547–562 | 35459859 | [10.1038/s41576-022-00483-8](https://doi.org/10.1038/s41576-022-00483-8) |
| **50% of ENA data from 50 projects** | Blackwell GA, Hunt M, Malone KM, et al. *PLoS Biol* 2021;19(11):e3001421 | 34752446 | [10.1371/journal.pbio.3001421](https://doi.org/10.1371/journal.pbio.3001421) |
| Sampling bias violates independence; more data does not rescue | Yu Y, Wheeler NE, Barquist L. *PLoS Biol* 2025;23:e3003539 | 41401143 | [10.1371/journal.pbio.3003539](https://doi.org/10.1371/journal.pbio.3003539) |
| Adjusted Rand Index for partition stability | Lees JA, Harris SR, Tonkin-Hill G, et al. PopPUNK. *Genome Res* 2019;29(2):304–316 | 30679308 | [10.1101/gr.241455.118](https://doi.org/10.1101/gr.241455.118) |
| GLM-DTA susceptible to sampling bias | Magee D, Suchard MA, Scotch M. *PLoS Comput Biol* 2017;13(2):e1005389 | 28170397 | [10.1371/journal.pcbi.1005389](https://doi.org/10.1371/journal.pcbi.1005389) |
| DTA could not be fit without travel metadata | Porter AF, Featherstone L, Lane CR, et al. *Microb Genom* 2023;9(8) | 37650865 | [10.1099/mgen.0.001099](https://doi.org/10.1099/mgen.0.001099) |

### *B. pseudomallei* primary literature

| Role | Citation | PMID | DOI |
|---|---|---|---|
| **The reference study** | Chewapreecha C, Holden MTG, Vehkala M, et al. *Nat Microbiol* 2017;2:16263 | 28112723 | [10.1038/nmicrobiol.2016.263](https://doi.org/10.1038/nmicrobiol.2016.263) |
| 1,391-genome NE Thailand study | Seng R, Chomkatekaew C, Tandhavanant S, et al. *Nat Commun* 2024;15:5699 | 38972886 | [10.1038/s41467-024-50067-9](https://doi.org/10.1038/s41467-024-50067-9) |
| Australian-origin pillar ⚠ *BMC Biology, not BMC Microbiology* | Pearson T, Giffard P, Beckstrom-Sternberg S, et al. *BMC Biol* 2009;7:78 | 19922616 | [10.1186/1741-7007-7-78](https://doi.org/10.1186/1741-7007-7-78) |
| r/m = 7.2; RM barriers | Nandi T, Holden MTG, Didelot X, et al. *Genome Res* 2015;25(1):129–41 | 25236617 | [10.1101/gr.177543.114](https://doi.org/10.1101/gr.177543.114) |
| Per-replicon rate ≠ per-replicon mutation | Dillon MM, Sung W, Lynch M, Cooper VS. *Genetics* 2015;200(3):935–946 | 25971664 | — |

---
