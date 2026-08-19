# Gap 2: clustering algorithms

**Resolved 2026-08-09.** Companion to `SNP_STRATEGY_REVIEW_2026-08.md`, `HANDOFF_research_gaps.md` and `GAP1_reference_free_kmer_methods.md`.

Scope, from the handoff: fastbaps vs rhierbaps vs hierBAPS and their behaviour under high recombination; whether Chewapreecha's stopping rule exists in software; TreeCluster and SNP-threshold selection; cluster validation; UMAP/t-SNE cautions.

Sources read via PubMed Central, journal full text, and the tools' own repositories and documentation up to 2026-08-09. Arithmetic and the cluster-size diagnostic are in `cluster_diagnostics_bp.py`.

**Method caveat, stated up front because it affects what "could not verify" means here.** Several retrieval routes were blocked during this session's research passes — `raw.githubusercontent.com`, the GitHub API, Europe PMC's REST endpoint, CRAN, and a handful of publisher domains. Everything below was obtained through alternative routes and is quoted from text that was actually read, but a small number of items are marked as unconfirmed specifically because the direct route was unavailable rather than because the source does not exist. Those are listed together at the end.

---

## The short version

**1. The question "are my 61–76 clusters too many?" has the answer backwards.** The only published PopPUNK run on this organism — Seng et al. 2024, 1,391 *B. pseudomallei* genomes — produced **101 lineages**. Your 61–76 clusters over roughly twice as many genomes is *coarser* than the one in-species precedent, not finer. Combined with the calibration already in the handoff (PopPUNK split 616 pneumococci into 62 strains where BAPS gave 16), nothing in the literature supports the worry that 61–76 is too fragmented. The open question is whether the clusters are *right*, not whether there are too many.

**2. Use fastbaps, and the decisive number is a runtime, not an accuracy figure.** On 3,156 pneumococcal genomes × 392,524 sites — almost exactly your scale — rhierbaps **did not finish within a week**, while fastbaps took 795 seconds with the fixed BAPS prior and 3,822 seconds with the optimised one. The MATLAB hierBAPS is functionally superseded; rhierbaps' own README points users to fastbaps. This retires the handoff's question about which is current.

**3. The only BAPS mode that cannot emit a polyphyletic cluster is the phylogeny-conditioned one, and it is the mode PopPIPE uses.** `best_baps_partition()` cuts a pre-computed tree to maximise the Dirichlet-process-mixture marginal likelihood, runs in linear time in the number of nodes, and the authors state it gives "a solution similar to that found using the optimized BAPS prior." Unconstrained hierBAPS and fastbaps both demonstrably produce polyphyletic clusters — and Chewapreecha's own *B. pseudomallei* run produced two non-monophyletic units out of nineteen.

**4. Nobody has ever tested whether BAPS-family clusters track clonal descent under high recombination.** Both models are products of independent per-site multinomial–Dirichlet likelihoods with no coalescent, no clonal frame and no recombination process. The one simulation in the fastbaps paper that varies recombination scores clusters against *deme membership*, not against a known clonal genealogy — and finds higher recombination makes the problem *easier*, which is exactly what you would expect when recombination homogenises demes into recoverable blobs. iterative-PopPUNK's benchmark reports the same "high recombination is easier" result and measures the same kind of thing. **Neither result licenses the inference that clustering is safe at r/m = 7.2 for the purpose you need it for.** This is a genuine hole in the literature and is worth saying so in print.

**5. Chewapreecha's stopping rule cannot be implemented as written, because Gubbins publishes no numeric divergence ceiling.** Confirmed absent from the 2015 paper, the manual, the docs site and the Debian manpage. The guidance is uniformly qualitative — "limited diversity", "sharing a recent common ancestor", "not appropriate for looking at recombination across species-wide diversity". The only hard number in the tool is `--min-snps 3`, which is a *lower* bound.

**6. But the rule is derivable, and it lands in a defensible place.** Gubbins calls recombination as a local excess of substitutions over a branch's background density, so the quantity that must stay large is the ratio of imported-substitution density to background density. Working that out with numbers already established in Gap 1 and Gap 5: species-wide the contrast is ~0.7×, i.e. gone — the *H. pylori* regime the Gubbins authors name as their failure case. At Seng's observed within-lineage diversity it is **35–54×**. A cap of roughly **1,000 mean pairwise core SNPs per cluster** keeps you at ≥20× contrast against a 0.5%-divergent donor, and Seng's three lineages (351, 517, 549) sit comfortably inside it. Arithmetic in `cluster_diagnostics_bp.py §B`.

**7. The single most useful number found for this gap is an empirical calibration point in your organism.** Seng et al. ran PopPUNK → per-lineage Gubbins v3.1.3 — your architecture — on lineages whose mean within-lineage pairwise core-SNP distances were **351, 517 and 549**, with per-lineage r/m of 4.6, 2.2 and 3.7. That is what a Gubbins-tractable *B. pseudomallei* cluster looks like, measured, in the published literature. Target it directly rather than reasoning from Gubbins' silence.

**8. Fixed SNP thresholds are not merely imprecise here, they are measuring the wrong thing — and there is an in-organism number proving it.** Sarovich et al. 2017 compared two *B. pseudomallei* STs: 1,328 raw SNPs, 36 recombination blocks totalling ~339 kb, and **73 SNPs (~5%) remaining after masking**. Roughly 95% of that pairwise distance was imported, not inherited — an ~18-fold inflation. Separately, Webb et al. 2022 state in terms that no *B. pseudomallei* SNP threshold has ever been established. And Hennart et al. 2022 demonstrated in *K. pneumoniae* that recombinant genomes act as bridges that fuse distinct groups under single-linkage clustering. A Mash-distance cut with no principled criterion is exposed to all three.

**9. There is a validation stack that is fully citable, and one piece of it you can run today.** PopPUNK's network score with a documented "at least 0.8" bar — Seng's published *B. pseudomallei* fit scored **0.8961**, so it passes; directional adjusted Wallace against the Lichtenegger cgMLST scheme, which tells you refinement from disagreement in a way ARI cannot; treespace/Kendall-Colijn comparison using within-scheme bootstrap dispersion as the null, following Seng's design; core-versus-accessory refit congruence; and per-cluster bootstrap Jaccard stability with Hennig's published thresholds. The cluster-size distribution check the handoff asked for is implemented and ready.

**10. Embeddings may visualise your clusters; they may never define them.** The strongest evidence is bacterial and comes from the authors of the bacterial tool: HDBSCAN on a mandrake embedding of 20,047 pneumococcal genomes recovered PopPUNK's GPSCs with an **AMI of 0.085**, and in their own coalescent simulations "the UMAP embedding rarely reflected the underlying simulated population structure." Chari and Pachter's decisive general point is narrower and sharper than the headline dispute: when the embedding is built from the same k-nearest-neighbour graph as the clustering, it "is then not an independent assessment of clustering results."

---

## 1. The BAPS family

### Provenance and current status

| Tool | Citation | PMID / DOI |
|---|---|---|
| BAPS | Corander J, Waldmann P, Sillanpää MJ. *Genetics* 2003;163(1):367–74 | PMID 12586722 |
| BAPS 5 | Corander J, Marttinen P, Sirén J, Tang J. *BMC Bioinformatics* 2008;9:539 | PMID 19087322 |
| **hierBAPS** | Cheng L, Connor TR, Sirén J, Aanensen DM, Corander J. Hierarchical and spatially explicit clustering of DNA sequences with BAPS software. *Mol Biol Evol* 2013;30(5):1224–8 | PMID 23408797 · [10.1093/molbev/mst028](https://doi.org/10.1093/molbev/mst028) |
| **rhierbaps** | Tonkin-Hill G, Lees JA, Bentley SD, Frost SDW, Corander J. *Wellcome Open Res* 2018;3:93 | PMID 30345380 · [10.12688/wellcomeopenres.14694.1](https://doi.org/10.12688/wellcomeopenres.14694.1) |
| **fastbaps** | Tonkin-Hill G, Lees JA, Bentley SD, Frost SDW, Corander J. Fast hierarchical Bayesian analysis of population structure. *Nucleic Acids Res* 2019;47(11):5539–49 | PMID 31076776 · [10.1093/nar/gkz361](https://doi.org/10.1093/nar/gkz361) |

The authors' own steer is in the rhierbaps README, verbatim: *"We have recently developed a faster verion of the BAPs clustering method. It can be found [here](https://github.com/gtonkinhill/fastbaps)."* There is no reciprocal pointer back. Both repositories are in maintenance mode — fastbaps' last release is **v1.0.8, 18 September 2022**, and everything since is continuous-integration housekeeping. "Maintained" is accurate; "actively developed" would not be.

No formal deprecation notice for the MATLAB hierBAPS was found. Treat it as superseded on the evidence of the ecosystem rather than on an announcement: PopPIPE, the current Lees/Croucher pipeline, uses **fastbaps v1.0.5**.

### The number that decides it at your scale

fastbaps Table 1, total CPU seconds, with the pneumococcal row at almost exactly your dataset size:

| Dataset | n | sites | fastbaps (BAPS prior) | fastbaps (optimise.baps) | rhierbaps |
|---|---|---|---|---|---|
| *S. pneumoniae* | **3,156** | **392,524** | **795 s** | **3,822 s** | **did not finish** |
| *E. coli* | 1,508 | 241,750 | 283 s | 1,210 s | 515,914 s |
| *N. meningitidis* | 882 | 87,730 | 78 s | 279 s | 110,312 s |

Table footnote, verbatim: *"Only fastbaps was able to run in a week for the Pneumococcal and HIV datasets."* rhierbaps at 1,508 genomes took **six days**. Extrapolating its scaling to 3,000 *B. pseudomallei* genomes on a core alignment several times longer than 392 kb is not a close call.

Complexity, verbatim: *"its complexity is still tied to the initial hierarchy generation and thus is O(n²)… After the initial hierarchy is generated, the remaining BHC is of the order O(lm²)."*

### The phylogeny-conditioned mode, which is the one to use

From the fastbaps paper, verbatim:

> "Given a pre-computed hierarchy or phylogeny, we can use the recursion method described previously to decide when merging sub-clades of the tree is justified according to the DPM model… It allows us to identify a partition of the tree into clades that maximizes the marginal likelihood of a DPM model given a hierarchy. As the hierarchy is pre-calculated, the approach is highly efficient and has a linear computational complexity in the number of nodes in the hierarchy."

> "The phylogeny conditioned mode can be seen to scale linearly, while the full fastbaps mode scales quadratically with the number of samples."

> "In both of these datasets the partition of the phylogeny using fastbaps provided a solution similar to that found using the optimized BAPS prior indicating it is an appropriate choice if a user's goal is to simply partition a pre-calculated phylogeny."

API: `best_baps_partition(sparse.data, tree)`; multiple levels via `multi_res_baps()`. This is a **model-based, threshold-free replacement for a tree cut** — it is what you would use instead of TreeCluster if you decide to keep cutting a tree rather than move to k-mer space.

Prior options, from `R/optimise_prior.R`: `"optimise.symmetric"`, `"symmetric"`, `"optimise.baps"`, `"baps"`, `"hc"`, defaulting to `optimise.baps`. Note a real inconsistency worth knowing before you script it: the README spells these with British `optimised.`, the argument strings are `optimise.`. The paper contains no sentence recommending a prior; `optimise.baps` is the code default and won both the simulations and five of six real datasets. Practical caveat, verbatim: *"Depending on the dataset, the prior optimization step in fastbaps can take longer than running the complete algorithm."*

### Site independence, and the thing nobody has tested

Neither paper states an independence assumption in those words; it is visible in the model form. fastbaps, verbatim: *"The merged hypothesis, which we denote [H1], is that all data in [D] were generated identically and independently from the same probabilistic model."* hierBAPS, verbatim: *"hierBAPS uses the standard multinomial likelihood for each single-nucleotide polymorphism site in each cluster and a conjugate Dirichlet prior distribution for the frequencies of the distinct variants detected at the sequence site in question."*

Both marginal likelihoods are products over loci. The consequence — stated here as inference, not as a published claim — is that a co-inherited recombinant block counts as many independent pieces of evidence rather than one event, so the likelihood ratio favouring a split is inflated roughly in proportion to block length, and isolates sharing an imported haplotype can be pulled together irrespective of clonal ancestry. At Nandi's median tract of ~5 kb this is not a small correction.

**No benchmark exists, anywhere, that varies r/m and scores BAPS-family clusters against a known clonal genealogy.** That is a searched-for absence, not an unsearched one, and it is a legitimate finding for the review.

### What the recombination simulations actually measured

This matters because the available results superficially say "recombination is fine", and they do not.

fastbaps, verbatim: *"a lower recombination rate leads to lower accuracy, which is likely due to the algorithms identifying additional population structure within each simulated deme."* Truth in those simulations is **deme membership**. Higher within-deme recombination homogenises demes, making them easier to recover. It says nothing about clonal descent.

iterative-PopPUNK (Zhao B, Lees JA, Wu H, Yang C, Falush D. *Genome Res* 2023;33(6):988–998, PMID 37253539) reports the same shape of result, verbatim: *"the accuracy between different data sets varies, with higher average accuracy of clusters in data sets with high recombination rates"* — again scoring cluster-versus-simulated-tree-node matching.

The authors of fastbaps are themselves careful where it counts. On HIV, verbatim: *"As HIV is highly recombinant, comparing the clustering of such a large global dataset to a phylogeny is unlikely to be informative."* And on the one dataset they lost: *"the outlying result … could rather be due to inaccuracies in the Fasttree phylogeny, since [it] has a high recombination rate."*

Cheng's 2013 hierBAPS simulation is often cited as the high-recombination validation. Verbatim: *"Sequence data were simulated to mimic characteristics of real MLST data under a metapopulation model with no migration between patches and no patch turnover while having high recombination to mutation rate locally within each patch (r/m = 10)."* Note the design — **r/m = 10 locally with zero migration between demes**. That is a model of recombination strictly *within* clusters. *B. pseudomallei* is closer to that than most species, because of Nandi's restriction-modification barriers, but Nandi still measured ~5% of each genome arriving from another clade. The simulation does not cover the part that hurts.

### hierBAPS over-splits demonstrably clonal lineages

The cleanest published evidence, from the GPSC paper (Gladstone RA, Lo SW, Lees JA, et al. *EBioMedicine* 2019;43:338–346, PMID 31003929, [10.1016/j.ebiom.2019.04.021](https://doi.org/10.1016/j.ebiom.2019.04.021)), on 20,027 pneumococcal genomes:

> "HierBAPS supported the clustering of 28/35 (80%) dominant-GPSCs… HierBAPS supported half of those clusters with >500 SNP distances, but GPSC18, GPSC23, GPSC37 and GPSC41 were split into two sub-clusters. Conversely GPSC1, the clonal serotype one lineage GPSC2 and GPSC16 were split by HierBAPS into two sub-clusters even when the maximum SNP distances were <500."

Splitting a lineage the same sentence calls "clonal", at maximum pairwise distances under 500 SNPs, is the behaviour to expect from a model that counts every site as independent evidence. For your purposes this is reassuring in one direction and cautionary in another: it means a high cluster count from a BAPS-family or sketch-based method is *normal*, and it means cluster boundaries at the fine end should not be over-interpreted as biology.

### Monophyly

fastbaps paper, verbatim: *"Both the hierBAPS and snapclust solutions included polyphyletic clusters while the BHC population mean based prior gave a similar result to the optimized BAPS solution."*

None of the three tools enforces monophyly except the phylogeny-conditioned fastbaps mode, which enforces it by construction — figure legend, verbatim: *"the final clustering indicates a partition of the Fasttree phylogeny using the fastbaps algorithm and thus is constrained to be consistent with the phylogeny."*

Chewapreecha's *B. pseudomallei* run confirms the general problem in your organism. Methods, verbatim: *"Except for Group 15 and a bin cluster (35 isolates), Group 1 - 14 and 16 - 19 each formed a monophyletic group in the phylogeny."* A figure legend adds: *"Apart from Group 15, which is paraphyletic and marked by two black arrows, other groups each form a monophyletic branch."* Their handling was to note it and proceed.

### PopPUNK versus RhierBAPS, since the comparison keeps getting asked for

From the PopPUNK paper (Lees JA, Harris SR, Tonkin-Hill G, et al. *Genome Res* 2019;29(2):304–316, PMID 30679308), verbatim:

> "PopPUNK used 15- to 74-fold less memory and ran between 10- and 100-fold faster than RhierBAPS."
> "Based on the Silhouette distance calculated from the π and [accessory] distances, the clustering identified by PopPUNK was typically of similar, or better, quality than that of RhierBAPS."
> "In general, both the PopPUNK and RhierBAPS clusterings corresponded to clades in the phylogenies, indicating PopPUNK strains are typically related by common descent."
> "Notably, RhierBAPS produced a superior clustering for [*N. gonorrhoeae* and *M. tuberculosis*], which lack the assumed strain structure."

A mean adjusted Rand index of **0.852** between PopPUNK and RhierBAPS was reported from that paper's supplementary material; the per-species breakdown could not be retrieved. No three-way fastbaps / hierBAPS / PopPUNK comparison on a common dataset exists.

The last quoted sentence is the one that matters for *B. pseudomallei*. PopPUNK's advantage is contingent on the species having strain structure. Nandi's restriction-modification result — clade-specific gene-flow barriers, clades as "functional units of genetic isolation" — is a direct argument that this organism does. Seng's fitted network score of 0.8961 (below) is the empirical confirmation.

---

## 2. Chewapreecha's stopping rule

### It cannot be implemented as written

The rule, verbatim from their Methods:

> "This method allows the population to be sub-divided into groups with closely related genetic backgrounds and allows the recombination detection tool (Gubbins) to operate within its best performing range… we continued the hierarchical clustering until the diversity observed in secondary or tertiary clusters fell within the limit of recombination detection."

**There is no such published limit.** No maximum divergence, no maximum branch length, no maximum pairwise SNP distance appears in Croucher et al. 2015, the Gubbins manual, the documentation site, or the manpage. What exists is qualitative, and consistent across all four:

> "samples of limited diversity, sharing a recent common ancestor - a [strain or lineage]" — manual
> "It is therefore not appropriate for looking at recombination across species-wide diversity" — manual
> "Such false positives are more likely to arise on longer branches within a phylogeny; it is recommended that populations be subdivided into smaller groups of less diverse samples that can each be independently analysed with Gubbins. This can be achieved with software such as PopPUNK or fastBAPS." — manual
> "Inaccuracies that may arise as a consequence of high levels of divergence between isolates in an alignment can be overcome by denser sampling or subdivision of the population prior to analysis." — Croucher et al. 2015
> on *H. pylori*: "in such datasets, the identification of recombinations as regions with elevated densities of base substitutions is confounded by the high diversity of the sequences in the alignment" — Croucher et al. 2015

The only hard numbers in the tool are a *lower* bound and a window rule. `--min-snps` defaults to 3: *"the minimum number of base substitutions required to infer a recombination (s_min; set to three by default)"*, with the consequence, verbatim, that *"Eleven per cent of the recombinations could not be identified because they caused two or fewer base substitutions."* And the window scan: *"The value of w is altered between 0.1 and 10 kb such that the expected number of base substitutions in a window would be at least 10."*

One more thing worth knowing before you rely on Gubbins' own filtering: **`--filter-percentage` is a missing-data filter, not a divergence filter.** Verbatim: *"Filter out taxa with more than this percentage of gaps (default: 25.0)."* A hyper-divergent isolate that aligns cleanly passes straight through and degrades the run silently.

Current release is **v3.4.3, tagged 27 August 2025**; the v3.4.2/v3.4.3 release notes concern invariant-site calculations, which is the change Gap 3 already flags.

### Nobody implements the rule

- **PopPIPE** (McHugh MP, Horsfield ST, von Wachsmann J, et al. *Microb Genom* 2025;11(4), PMID 40294103) quotes the constraint in its introduction — *"Methods exist to remove these recombination events (e.g. gubbins and ClonalFrameML) but are only applicable within populations of limited diversity sharing a recent common ancestor"* — and then hard-codes **two fastbaps levels** and `min_cluster_size: 6` in `config.yml`. The only gate is cluster *size*, never cluster *diversity*.
- **iterative-PopPUNK** sweeps the decision boundary across **1% to 99% of maximum average core distance at 30 equally spaced positions**, yielding roughly sixfold more clusters than base PopPUNK, and hands the user the resolution ladder. It supplies no criterion for choosing a rung. This is nonetheless the right machinery: it gives you the sweep, you supply the stopping rule it lacks.
- **rPinecone** (Wailan AM, Coll F, Heinz E, et al. *Microb Genom* 2019;5(4):e000264, PMID 30920366 — note **2019**, not 2020) does subdivide hierarchically by root-to-tip SNV depth, but it is the wrong tool at both ends. It targets *"low-variant (LV) populations"* with *"at least a median SNV distance of 2"* — your within-lineage means are 351–549 — and it runs **downstream** of Gubbins, not upstream: *"Chromosomal recombination regions were identified using Gubbins. SNVs found within these regions of the chromosome were excluded from the SNV alignment."*
- **nf-core/bactmap** has no clustering step at all; Gubbins is an optional post-alignment flag (`--remove_recombination`) applied to the whole alignment.
- Gubbins' own helper scripts slice output rather than qualify input. `generate_files_for_clade_analysis.py` will extract a clade's tree and alignment given an isolate list — the mechanics of subdividing are supported; *which* clade is entirely the user's call.

### The derivation that replaces it

Gubbins detects recombination as a **local excess of substitutions over a branch's background density**. So the quantity that must stay large is the ratio of imported-substitution density to background density, and that is computable from figures already established in Gap 1 and Gap 5. Full arithmetic in `cluster_diagnostics_bp.py`; the results:

**The window rule is not the binding constraint, which rules out the obvious proxy.** Gubbins picks `w = 10 / (branch SNP density)`, clamped to [100 bp, 10 kb]. Over K96243's 7.25 Mb, the 10 kb ceiling binds for every branch carrying fewer than ~7,240 SNPs and the 100 bp floor only above ~724,000. Every realistic *B. pseudomallei* branch — within-cluster or backbone — sits pinned at the ceiling, so the window rule never discriminates. I had expected this to be the mechanism-matched criterion; it is not.

**The contrast ratio does bind.** Taking background as mean within-cluster pairwise core SNPs over Wu's 3,805,619 bp core, and a recombination donor at 0.5% divergence:

| Partition | mean pairwise core SNPs | background | contrast |
|---|---|---|---|
| Seng lineage 2 — Gubbins ran on this | 351 | 9.2 × 10⁻⁵ | **54×** |
| Seng lineage 3 — Gubbins ran on this | 517 | 1.4 × 10⁻⁴ | **37×** |
| Seng lineage 1 — Gubbins ran on this | 549 | 1.4 × 10⁻⁴ | **35×** |
| a hypothetical 2,000-SNP cluster | 2,000 | 5.3 × 10⁻⁴ | 9.5× |
| a hypothetical 10,000-SNP cluster | 10,000 | 2.6 × 10⁻³ | 1.9× |
| **species-wide** (π = 0.0067) | 25,498 | 6.7 × 10⁻³ | **0.7×** |

Species-wide the contrast is gone. That is a quantitative statement of why cluster-then-Gubbins is not merely convenient in this organism but necessary, and it is derived from your own numbers rather than borrowed from pneumococcus.

**Sensitivity floor at the other end.** A tract must import ≥3 substitutions to be callable, so at Nandi's median tract length of ~5 kb, imports from donors below **0.06% divergence** are invisible no matter how you cluster. Within-cluster donors in this organism are frequently that close. This is a floor on what any per-cluster Gubbins run can see, and it belongs in the methods section as a stated limitation rather than being discovered later.

### The empirical calibration point, which is better than the derivation

Seng R, et al. *Nat Commun* 2024;15:5699, PMID 38972886, [10.1038/s41467-024-50067-9](https://doi.org/10.1038/s41467-024-50067-9) ran **PopPUNK v2.6.0 → per-lineage Gubbins v3.1.3** on 1,391 *B. pseudomallei* genomes — your architecture, your organism. Their three dominant lineages:

> "The average pairwise core SNP distance within each dominant lineage was 549, 351, and 517 SNPs"
> "The ratio of polymorphisms introduced through recombination compared to those introduced by mutation (r/m) was 3.7, 4.6 and 2.2 for lineages 1, 2, and 3 respectively"
> "99.5% of genes in lineage 1, 99.9% in lineage 2, and 96.6% in lineage 3" underwent recombination at least once

That last line is worth pausing on: within a single successfully-processed lineage, essentially every gene had recombined at least once, and Gubbins still worked. The constraint is not "has recombination happened" but "is the imported density still distinguishable from the background".

### The rule I would adopt

**Subdivide until each cluster's mean pairwise core-SNP distance is at or below ~1,000, and report the distribution of that statistic across clusters alongside the partition.** Two independent supports: it keeps contrast at ≥20× against a 0.5%-divergent donor by the derivation above, and it sits within a factor of two to three of the only published in-organism precedent where the same tool chain demonstrably worked. Report per-cluster r/m and masked-base fraction from Gubbins' `.per_branch_statistics.csv` afterwards as a post-hoc check — those columns exist, no published threshold on them does, so report them as a distribution and justify the cut empirically.

State plainly in the methods that this is a construct. The honest sentence is that Gubbins publishes no divergence ceiling, that the field's practice is to subdivide by PopPUNK or fastbaps and not measure the result, and that you calibrated against Seng.

A secondary red flag worth carrying: ClonalFrameML's δR — the compound of recombination rate, mean import length and branch length — where the authors state that *"when δR is greater than one, there is a significant chance that recombination happened more than once at any genomic position for the longer branches of the phylogeny, but this is not accounted for."* It is not a divergence rule, but it is the closest thing either tool offers to a quantitative alarm.

---

## 3. TreeCluster, and why fixed thresholds are dangerous here

### TreeCluster

> Balaban M, Moshiri N, Mai U, Jia X, Mirarab S. TreeCluster: Clustering biological sequences using phylogenetic trees. *PLoS One* 2019;14(8):e0221068. PMID 31437182. [10.1371/journal.pone.0221068](https://doi.org/10.1371/journal.pone.0221068)

It reframes clustering as **min-cut partitioning**: given a tree and threshold *t*, return the minimum number of clusters such that every cluster satisfies a stated constraint, in linear time. The implementation exposes fifteen methods, not the three in the paper — `max`, `max_clade` (the default), `sum_branch`, `sum_branch_clade`, `avg_clade`, `med_clade`, `single_linkage`, `single_linkage_cut`, `single_linkage_union`, `length`, `length_clade`, `root_dist`, `leaf_dist_max`, `leaf_dist_min`, `leaf_dist_avg`. Branch lengths are required; the `*_clade` and `*_dist` methods need a rooted tree. It scales trivially — 203,452 Greengenes leaves in 30 seconds.

Three things disqualify it as a primary partitioner for you and one thing keeps it in the toolkit.

**It was built and validated for viral and 16S data.** The benchmarks are Greengenes OTUs, HIV transmission clustering on FAVITES simulations, and MSA subset decomposition. The repository describes it as *"Efficient phylogenetic clustering of viral sequences."* No bacterial whole-genome phylogeny appears in the paper.

**It has no principled automatic threshold.** The only automatic mode, `-tf argmax_clusters`, *"choose[s] the threshold that maximizes the number of non-singleton clusters"* — a heuristic maximising a count, with no biological justification and no validation in the paper. On your data it will over-split. The paper's actual advice is to scan: *"the high speed of TreeCluster makes it possible to quickly scan through a set of α thresholds."*

**Its one bacterial application is a cautionary tale.** Menardo F. *eLife* 2022;11:e76780, PMID 35762734, used TreeCluster v1.0.3 with `method max` across thresholds 0–50 SNPs on *M. tuberculosis* ML phylogenies. Findings, verbatim: *"the optimal SNP threshold is the one that maximizes sensitivity and specificity… this threshold depends strongly on the epidemiological conditions and on the sample size: across all scenarios… 95% sensitivity threshold ranged between 3 and 11 SNPs"*; *"sub-populations with different epidemiological characteristics should not be analyzed with the same threshold"*; *"clustering results and TBL depend on many factors that have nothing to do with transmission."* That is a **monomorphic, effectively non-recombining** organism, and the optimal threshold still moved by nearly fourfold on sampling and epidemiology alone.

**What keeps it usable:** ReporTree (Mixão V, Pinto M, Sobral D, Di Pasquale A, Gomes JP, Borges V. ReporTree: a surveillance-oriented tool to strengthen the linkage between pathogen genetic clusters and epidemiological data. *Genome Med* 2023;15:43, PMID 37322495, [10.1186/s13073-023-01196-1](https://doi.org/10.1186/s13073-023-01196-1)) wraps TreeCluster and computes clustering at *all* thresholds, then uses the **neighbourhood adjusted Wallace coefficient** between consecutive partitions to *"ultimately determine regions of cluster stability."* Its software defaults call a region stable at adjusted Wallace ≥ 0.99 across at least five consecutive thresholds — both tunable, and both taken from the repository README rather than the paper, so cite them as defaults. It was benchmarked at 3,791 *N. gonorrhoeae* genomes, which is your scale.

That is the published, objective way to pick a threshold from your own data instead of importing one. One honesty caveat if you cite it as bacterial precedent for TreeCluster specifically: ReporTree's own TreeCluster demonstration is on SARS-CoV-2, and its bacterial datasets went through the cgMLST/goeBURST or hierarchical-clustering routes. It establishes TreeCluster as a sanctioned option in a mainstream bacterial surveillance pipeline, not as a published bacterial TreeCluster result. The paper never mentions recombination.

### Why fixed thresholds fail here specifically — with the in-organism number

The general argument is well made in the literature. Duval A, Opatowski L, Brisse S. *Lancet Microbe* 2023;4(5):e349–e357, PMID 37003286, is the single best citation:

> "All these parameters considered, a threshold for one outbreak is unlikely to be applicable to another outbreak, even if they involve the same pathogen."

Their derived per-outbreak thresholds are ranges, not constants — *Listeria* 1–13 SNPs across nine outbreaks against a fixed 7-allele convention. And their stated limitation makes the range a floor for your purposes: *"we only modelled mutation, neglecting other evolutionary processes such as genetic recombination."*

Stimson J, Gardy J, Mathema B, et al. *Mol Biol Evol* 2019;36(3):587–603, PMID 30690464, adds: *"By itself, the number of SNP differences between genomes does not directly imply a probability of recent transmission"*, with a compiled table of published TB thresholds spanning ≤2 to >1,000 SNPs. PopPUNK's version of the same point is quantitative: *"Calculating the within-strain SNP distances… varied by more than two orders of magnitude between species."*

But the argument that should actually go in your review is in your own organism:

> Sarovich DS, Chapple SNJ, Price EP, Mayo M, Holden MTG, Peacock SJ, Currie BJ. *Microb Genom* 2017;3(8):e000117.

ST-125 and ST-126 *"differ by at least 1328 SNPs and 154 indels on the whole-genome level"*; Gubbins found *"36 discrete recombination blocks totalling ~339 kb"*; and *"following removal of recombinogenic regions, 73 SNPs (~5 % total) still separated the ST-125 and ST-126 strains."*

**About 95% of an observed pairwise SNP distance between two *B. pseudomallei* isolates was imported rather than inherited — an ~18-fold inflation.** A raw pairwise SNP distance in this organism is mostly a measure of recombination history. Thresholding on it partitions by import load.

The mechanism is arithmetic: ClonalFrameML's decomposition **r/m = (R/θ) × δ × ν** means a single import of length δ from a donor at divergence ν contributes δ × ν SNPs *simultaneously*. At Nandi's median tract of ~5 kb and a 1% donor, that is 50 SNPs from one event; at the 71 kb maximum, several hundred.

And Hedge & Wilson supply the licence for what to do instead: topology survives recombination (*">97%"* clonal-frame topology recovery) while *"branch lengths are badly skewed"*. Recombination wrecks precisely the quantity a distance threshold consumes, and largely spares the quantity a topology-based or model-based partition consumes.

### There is no *B. pseudomallei* threshold, and the field says so

> Webb JR, Mayo M, Rachlin A, et al. *J Clin Microbiol* 2022;60(3):e01648-21, PMID 35080450.

Verbatim: **"A SNP cutoff or distance threshold for inferring transmission of *B. pseudomallei* from environment to human has not been established."** They observed 0–15 SNPs (median 4) across 17 matched case-environment pairs, with non-matches at 113 and 989, and explicitly preferred *"a combination of epidemiology and phylogenetic analysis including closely related local isolates for context."*

A correction to the handoff's framing on cgMLST: Lichtenegger et al. 2021 (PMID 33980649) does not *refuse* to recommend a threshold — it simply never proposes one. The word "recommend" does not appear, and the only use of "threshold" concerns scheme construction. **Phrase it as a documented absence, not a refusal.** What the paper does say is more useful: *"a certain number of SNP-indel mutations does not translate to a certain number of allele alterations"*, with worked examples putting the conversion at roughly one allele per six SNPs in their data. The paper does not discuss recombination at all, which is a fair criticism to make of a cgMLST scheme for an r/m ≈ 7 organism.

### Single-linkage chaining, and why it is the specific hazard for a Mash cut

> Hennart M, Guglielmini J, Bridel S, et al. *Mol Biol Evol* 2022;39(7):msac135. [10.1093/molbev/msac135](https://doi.org/10.1093/molbev/msac135)

Verbatim: *"Single linkage clustering may result in the fusion of preexisting groups as additional genomes are introduced, due to the possibility of new genomes being less distant than the threshold, from two distinct groups. This approach thus suffers from instability."*

They detected large recombination events in 1.9% of 7,198 *K. pneumoniae* genomes and intra-gene recombination in 50.6% of loci, then showed that these recombinant hybrids *"would cause the fusion of phylogroup partitions upon single linkage clustering."* This is the clearest published demonstration that recombinant genomes act as bridges collapsing threshold-defined clusters — the exact hazard for 3,000 *B. pseudomallei* genomes at r/m 7.2.

Their threshold-selection framework is worth copying wholesale: silhouette *S_t* for consistency, adjusted Wallace *W_t* for stability under subsampling, Rand *R_t* for concordance with existing nomenclature, computed across all *t*, with thresholds placed at local optima of *S_t* and *W_t* coinciding with discontinuities in the pairwise-distance distribution. Note that even after doing all that, they added stable LIN codes because single-linkage thresholds remained unstable.

PopPUNK makes the same point about its own network step: *"Only a few spurious connections can have a dramatic effect on strain definitions, as previously observed for MLST clonal complexes. For strain definitions to be robust, networks should have a nonoverlapping community structure"* — which is why the network score exists.

### Mash distance specifically

Two problems, both documented by Mash's own authors.

**Sketch size.** Ondov et al. *Genome Biol* 2016;17:132, Table 1, error bounds at k=21 and D=0.05: **s=1,000 → ±0.0068; s=10,000 → ±0.0020; s=100,000 → ±0.0006.** At the default sketch size the ±0.0068 error on a distance of 0.05 is ~14% relative — over a 7.25 Mb genome, tens of thousands of SNPs of uncertainty. Default sketches are not adequate for within-species lineage work; you need s ≥ 10⁴–10⁵. **Check what your pipeline used.**

**And raising the sketch size does not rescue it at close range.** The fastANI paper (Jain C, Rodriguez-R LM, Phillippy AM, Konstantinidis KT, Aluru S. *Nat Commun* 2018;9:5114, PMID 30504855) benchmarks Mash against alignment-based ANI on five datasets, one of which — 464 *Bacillus anthracis* genomes, described as *"challenging because its constituent genomes are closely related strains… with ANIb > 99.9 for all the pairs"* — is the closest analogue to within-species work. Pearson correlation with true ANI on that dataset: **Mash 0.594/0.932/0.935 → −0.040, 0.003, 0.010** at sketch sizes 10³, 10⁴, 10⁵ respectively, against 0.995 and better on the more divergent datasets. **At very high identity, Mash distance carries essentially no information about true divergence even at a 100,000-hash sketch.** fastANI itself drops to 0.681 there. *B. pseudomallei* is not as tight as *B. anthracis*, so this is the extreme rather than your case — but it establishes the direction of the failure, and it is the strongest available argument that a Mash-distance cut is the wrong primitive for sub-lineage structure regardless of sketch size.

**Conflation.** Mash returns one number mixing core divergence and gene content. The authors' own disclaimer: *"Mash is not explicitly designed for phylogeny reconstruction, especially for genomes with high divergence or large size differences."* PopPUNK exists to fix exactly this — regressing k-mer match probability against k under `p_match,k = (1−a)(1−π)^k` to separate core π from accessory *a*. Given that *B. pseudomallei* carries 16 genomic islands in K96243 and Nandi found clade-specific accessory profiles, conflating the two axes is not a theoretical concern here.

The PopPUNK warning that applies most directly to your organism: *"When the indel rate was fixed at 0.05, the distributions of both a and π converged toward a single mode as the rate of exchange through recombination was increased"*, and *"Neither the 2D GMM or HDBSCAN methods alone could satisfactorily resolve the recombinogenic populations into strains, primarily due to the diffuse nature of the within-strain distribution."* Recombination erodes the bimodality any distance-based partition depends on. The mitigations are PopPUNK's boundary-refinement step and — in this organism specifically — Nandi's restriction-modification barriers, which preserve more structure than a panmictic recombinogenic species would have. Seng's fitted network score of 0.8961 says the bimodality does survive in *B. pseudomallei*.

### The other tools, briefly

- **HierCC** (Zhou Z, Charlesworth J, Achtman M. *Bioinformatics* 2021;37(20):3645–3650) — single-linkage cgMLST at fixed levels, but the levels were chosen by **normalised mutual information stability blocks plus silhouette**, not by outbreak epidemiology. The *procedure* is the right template; the levels are Enterobacteriaceae-calibrated and must not be transplanted.
- **GrapeTree / MSTree V2** (Zhou et al. *Genome Res* 2018;28(9):1395–1404, PMID 30049790) — robust to missing data, demonstrated at 99,722 genomes, but a visualisation and topology tool that inherits whatever distortion recombination puts into the allelic distance. Their own caveat: *"phylogenetic topologies and branch lengths are more accurately depicted by NJ trees."* And the disqualifying detail: the accuracy simulations were run *"without homologous recombination and assuming a constant population size"*, so MSTree V2 has never been validated under the conditions you have. It also needs a cgMLST scheme, and there is no *B. pseudomallei* scheme in EnteroBase — the Lichtenegger scheme lives in Ridom SeqSphere+ and cgMLST.org instead.
- **PopPUNK `--fit-model threshold`** — a documented **fallback**, not a recommendation: *"This can be useful if `refine` cannot find a boundary due to a poorly performing network score, but one can clearly be seen from the plot."* Do not reach for it first.
- **PopPUNK `--fit-model lineage`** — nearest-neighbour joining at multiple ranks, the highest resolution PopPUNK offers directly, intended for sub-strain structure or for species without strain structure. Caveat, verbatim: *"these are not necessarily expected to be transitive, so network scores are not as informative of the optimum."*

---

## 4. Cluster validation

### PopPUNK's network score — and Seng's fit already passes

The definition, from the PopPUNK paper: `ns = transitivity × (1 − density)`, with the model chosen by maximising it. The documentation supplies the interpretation and the bar:

> **Density**: "the proportion of distances assigned as 'within-strain'. Generally smaller is better as this gives more specific clusters, but too close to zero may be an over-specific model."
> **Transitivity**: "measures whether every member of each strain is connected to every other member. Closer to 1 is better, but this can be achieved with very loose fits."
> **"This is a bad network score -- a value of at least 0.8 would be expected for a good fit."**

A structural weakness worth stating in a methods section: in the documentation's own worked example, the *bad* two-component fit has transitivity 1.0000. Transitivity alone is degenerate — a fit lumping everything into two giant cliques scores 1 — and it is the `(1 − density)` term doing the discriminating. Newer PopPUNK versions add betweenness-penalised variants (`score_1`, `score_2`) that penalise components with high node betweenness, "creating more conservative boundaries", which targets exactly the bridging failure Hennart demonstrated.

**Seng's published *B. pseudomallei* fit — density 0.028, transitivity 0.992, network score 0.8961 — clears the 0.8 bar.** The handoff already records those parameters; what is new is that there is a documented bar to read them against, and that they pass it. Use those settings as the starting point, report your own three numbers, and report the betweenness-penalised variants too given the recombination.

### Directional adjusted Wallace, which is what you want instead of ARI

> Severiano A, Pinto FR, Ramirez M, Carriço JA. Adjusted Wallace coefficient as a measure of congruence between typing methods. *J Clin Microbiol* 2011;49(11):3997–4000. PMID 21918028. [10.1128/JCM.00624-11](https://doi.org/10.1128/JCM.00624-11)
> Carriço JA, Silva-Costa C, Melo-Cristino J, et al. *J Clin Microbiol* 2006;44(7):2524–32. PMID 16825375.

Verbatim: *"W(A→B) is the probability that, for a given data set, two individuals are classified together using method B if they have been classified together using method A."* Adjusted form **AW(A→B) = [W(A→B) − Wi(A→B)] / [1 − Wi(A→B)]**, with a confidence interval that depends on Simpson's index of diversity of the reference partition.

The point: **ARI is symmetric and will hide the asymmetry that is the actual result.** AW(your clusters → cgMLST) ≠ AW(cgMLST → your clusters), and the difference is how you demonstrate that one scheme is a strict refinement of the other rather than merely disagreeing with it. Given §1's evidence that sketch and BAPS methods split finer than lineage-level schemes, refinement is the hypothesis you are actually testing.

Neither foundational paper sets a cutoff; both report point estimates with confidence intervals, deliberately. Do the same. The `comparingpartitions.info` tool from the same group computes SID, Wallace, adjusted Wallace and ARI with intervals.

Congruence targets in this organism: the Lichtenegger cgMLST scheme (4,221 core + 1,351 accessory targets, PMID 33980649, hosted at cgMLST.org and in Pathogenwatch), and the core-SNP phylogeny. **Do not use MLST as ground truth** — the handoff already records ST105 spanning two clusters and ST51 spanning three, and Seng's treespace analysis independently found MLST trees to be the dispersed outlier.

### treespace, following Seng's design

> Jombart T, Kendall M, Almagro-Garcia J, Colijn C. treespace: Statistical exploration of landscapes of phylogenetic trees. *Mol Ecol Resour* 2017;17(6):1385–1392. PMID 28374552.
> Kendall M, Colijn C. Mapping phylogenetic trees to reveal distinct patterns of evolution. *Mol Biol Evol* 2016;33(10):2735–2743. PMID 27343287.

The Kendall–Colijn metric records, for each pair of tips, the distance from their MRCA to the root both as an edge count *m* and as a path length *M*, combined as **v_λ(T) = (1−λ)m(T) + λM(T)**, where λ *"determines how much the topology of the tree only (λ = 0), versus the tree with branch lengths (λ = 1), contributes."* Given Hedge & Wilson, λ = 0 is the defensible choice here — you are comparing schemes whose branch lengths are not in comparable units, and branch lengths are the part recombination ruins.

Seng's design is the part to steal. Verbatim from their Methods: *"we used the R package treespace v. 1.1.4.3 to explore the tree tip distributions"* — note the version string is printed **v. 1.1.4.3**, not v1.14.3 as the handoff has it. They computed pairwise distances **within the first 100 bootstrap trees of each alignment category and across categories**, with two PCs accounting for >90% of variability. Result, verbatim: *"a close clustering of bootstrap trees from core genome SNP and cgMLST, while the bootstrap trees from MLST alignment showed greater dispersion."*

**Using within-scheme bootstrap dispersion as the null yardstick is the methodological point.** If cross-scheme distances fall inside the within-scheme bootstrap cloud, the schemes are congruent to within phylogenetic uncertainty — a far stronger statement than a bare adjusted Rand index. Seng did not state λ; state yours.

### Core versus accessory congruence

PopPUNK proposes this directly, and it is free once you have the distances. Verbatim: *"PopPUNK allows for models to be refined separately for the π and a distances… using this approach to analyze both the *S. pneumoniae* multidrug-resistant lineage PMEN14 and *N. gonorrhoeae* found these core and accessory clusterings to be highly discrepant"* — attributed in the first case to frequent phage infection and in the second to the Gonococcal Genomic Island.

**Expect discordance in *B. pseudomallei* and report its magnitude rather than treating it as a failure.** Nandi found clade-specific accessory and epigenetic profiles; K96243 carries 16 genomic islands at ~6% of the genome; Wu's pan-genome analysis found functional compartmentalisation between the replicons. Discordance here is a measurement of the decoupling between clonal descent and gene-content evolution, and it is publishable in its own right.

### Cluster-size distribution — the diagnostic, now runnable

`cluster_diagnostics_bp.py` implements the check the handoff asked for. Run it against your cluster assignments:

```bash
python3 cluster_diagnostics_bp.py --clusters your_clusters.csv --cluster-col cluster
```

Reference partitions, computed:

| Partition | genomes | clusters | largest | smallest | max/min | Gini |
|---|---|---|---|---|---|---|
| Chewapreecha hierBAPS | 469 | 20 | 137 | 4 | **34.2** | **0.456** |
| Wu imposed ten-way cut* | ~4,127 | 10 | 583 | 285 | **2.0** | **0.095** |

\* Wu's individual sizes are not published; the row uses a reconstruction reproducing the reported range, count and total. The shape statistics are the point, not the values.

The benchmark for what real structure looks like at scale, from the GPSC paper: **407 of 621 clusters (66%) hold 1,043 of 20,027 genomes (5%), while 35 clusters (5.6%) hold 62% of the GPS subset.** A few large lineages and a long tail. Feil's eBURST paper states the general expectation, verbatim: *"a considerable proportion of a population belongs to a limited number of clusters of closely related genotypes."*

**A Gini near 0 with a max/min ratio near 1 means the partition was imposed.** That contrast — skewed means inferred, even means imposed — is an argument supported by the data above rather than a claim anyone has published as such; present it that way.

One observation worth carrying, offered as a pattern rather than a law: **Chewapreecha's unassigned "bin" was 34/469 = 7.2%, and Seng's PopPUNK left 97/1,391 = 7.0% unassigned.** Two independent studies, different methods, different sampling frames, similar remainders. There is no published expectation for the unassigned fraction in bacterial clustering — that absence was searched for and confirmed — so if your partition leaves a comparable remainder, this is the closest thing to a sanity check available.

### Per-cluster stability, which is nearly unprecedented in this field

> Hennig C. Cluster-wise assessment of cluster stability. *Comput Stat Data Anal* 2007;52(1):258–271. [10.1016/j.csda.2006.11.025](https://doi.org/10.1016/j.csda.2006.11.025)

Thresholds, verbatim from the `fpc::clusterboot` documentation:

> "There is some theoretical justification to consider a Jaccard similarity value smaller or equal to 0.5 as an indication of a 'dissolved cluster'"
> "a valid, stable cluster should yield a mean Jaccard similarity value of 0.75 or more. Between 0.6 and 0.75, clusters may be considered as indicating patterns in the data, but which points exactly should belong to these clusters is highly doubtful. Below average Jaccard values of 0.6, clusters should not be trusted."
> "'Highly stable' clusters should yield average Jaccard similarities of 0.85 and above."

These are **per-cluster**, which is exactly right for a skewed size distribution where a single global statistic is dominated by the large lineages. Exactly one bacterial-genomics application was found (a 2023 *Salmonella* paper whose own reported figure appears to contradict its stated criterion — verify before citing). Applying per-cluster Jaccard stability to a 3,000-genome *B. pseudomallei* partition would be close to novel in this field, and it directly addresses the pseudo-replication problem the sampling audit identified: a cluster that dissolves under resampling is a cluster built from one BioProject.

### Batch stability and balanced subsampling

PopPUNK's claim is about **label persistence under append-only assignment**, not partition invariance. Verbatim: *"the Rand indices were all above 0.9997"* when population batches were added in different orders, with *"the median Rand index still greater than 0.99"* across different starting reference populations, tested on 4,107 draft pneumococcal genomes. But merges are permitted and are the designed response to newly sampled intermediates — the docs are candid: *"maintaining stable nomenclature in a dynamic population is not possible (for any nomenclature)"*, and merged clusters are renamed with underscores (`23_38`). Their yearly-batch *E. coli* design is a good template for a temporal stability experiment on your collection.

On sampling bias, the directly transferable citation is Meirmans PG. *Heredity* 2018;122(3):276–287 (PMC6460757): *"ten out of the 12 species showed an optimal value of K = 2 clusters"* under unbalanced sampling, while balanced subsamples gave different and more biologically sensible answers. Given 59.6% Thailand and 81% of Thai genomes from three BioProjects, **re-running the clustering on a geographically and BioProject-balanced subsample and comparing partitions is not optional diligence — it is a direct test of whether your clusters are population structure or sampling structure.**

### What is absent, and worth saying

- **The three canonical internal indices — Calinski-Harabasz, Davies-Bouldin, gap statistic — are essentially absent from bacterial population genomics.** Targeted searching found no primary source reporting values for any of them on real bacterial genomes. The field converged instead on PopPUNK's network score, marginal-likelihood model selection in the BAPS family, and external congruence. Silhouette appears, but mostly comparatively — PopPUNK uses it only to rank itself against RhierBAPS, reporting no absolute values; HierCC uses it jointly with NMI stability blocks, never alone.
- **No bacterial-genomics paper states the convexity assumption underlying silhouette and its relatives**, or warns that it misleads on high-dimensional sparse SNP data. The general result exists outside the field. The closest in-field evidence is PopPUNK's empirical demonstration of the same phenomenon: elongated within-strain distance distributions that a Gaussian mixture handles badly — and elongation is a recombination signature.
- **No published numeric divergence threshold for Gubbins or ClonalFrameML input**, despite universal qualitative guidance to split first. Confirmed absent from both tool papers and the current documentation.

---

## 5. UMAP and t-SNE

### The single-cell dispute, and what survives it

> Chari T, Pachter L. The specious art of single-cell genomics. *PLoS Comput Biol* 2023;19(8):e1011288. PMID 37590228. [10.1371/journal.pcbi.1011288](https://doi.org/10.1371/journal.pcbi.1011288)
> Lause J, Berens P, Kobak D. The art of seeing the elephant in the room: 2D embeddings of single-cell data do make sense. *PLoS Comput Biol* 2024;20(10):e1012403. PMID 39356722. [10.1371/journal.pcbi.1012403](https://doi.org/10.1371/journal.pcbi.1012403)

Chari and Pachter's measurements: 30-nearest-neighbour Jaccard distance to ambient space *"consistently above 0.7"*; global neighbour-ranking correlations *"≤ 0.4"*; and **4- to 200-fold inflation of max/min pairwise distance ratios**. Their theoretical claim is that distortion is unavoidable — the Johnson–Lindenstrauss bound implies *"preservation of pairwise distances with a margin of error of at most 20% for a modestly sized dataset of 10,000 cells would require at least 1,842 dimensions."* Their demonstration is "Picasso", an autoencoder that forces data into an arbitrary shape (a von Neumann elephant) while scoring comparably to t-SNE and UMAP on distance-preservation metrics.

Lause, Berens and Kobak rebut **only the Picasso equivalence claim**, and rebut it convincingly: kNN accuracy >90% for t-SNE/UMAP versus <62% for Picasso and 2D PCA; on simulated data with ground truth, *"only t-SNE and UMAP could separate the true classes, while Picasso and 2D PCA failed at that."* Verbatim: *"Claiming that Picasso and t-SNE/UMAP are 'quantitatively similar in terms of fidelity to the data in ambient dimension' is wrong."*

**What both sides agree on is the operative rule.** Lause et al., verbatim: *"we agree that 2D embeddings necessarily distort high-dimensional distances between data points"*; *"we do not recommend to use 2D embeddings for quantitative downstream analysis"*; *"any generated insight should then be validated in the high-dimensional data by other means."* The only stated disagreement is whether embeddings are useful for exploration.

The argument that transfers most directly to your pipeline is not the headline dispute at all. It is Chari and Pachter's observation that standard workflows pass **the same kNN graph** to both the clustering algorithm and the embedding, so *"the embedding is then not an independent assessment of clustering results and is likely to form clusters that resemble the kNN graph even if that graph does not represent the 'original' underlying manifold."* An embedding cannot validate the clustering it was derived from.

Also relevant if anyone proposes tuning: Kobak D, Linderman GC. *Nat Biotechnol* 2021;39:156–157, PMID 33526945 — *"the alleged superiority of UMAP over t-SNE can be entirely attributed to different choices of initialization."*

### The bacterial evidence, from the authors of the bacterial tool

> Lees JA, Tonkin-Hill G, Yang Z, Corander J. Mandrake: visualizing microbial population structure by embedding millions of genomes into a low-dimensional representation. *Philos Trans R Soc Lond B Biol Sci* 2022;377(1861):20210237. PMID 35989601. [10.1098/rstb.2021.0237](https://doi.org/10.1098/rstb.2021.0237)

Mandrake is stochastic cluster embedding, not t-SNE or UMAP — a generalisation of t-SNE with a scaling parameter that increases repulsion. Worth knowing before you read anything into how clustered its output looks: **the scale factor was chosen by a human perception study, not by a statistical criterion.**

Their three caveats, verbatim:

> 1. "Cluster sizes in the embedding space do not relate to the number of points in the cluster, or its genetic diversity."
> 2. "Distances between clusters do not correspond to their genetic distances. Two well-separated clusters, close together, are not necessarily more genetically similar than two well-separated clusters at opposite ends of the plot."
> 3. "Perplexity can greatly affect results, and runs at a few different perplexities should typically be attempted."

And the warning against inference, verbatim: *"clusters formed by these plots are generally not expected to be competitive with species-specific schemes, which have usually been curated and optimized to find useful clusters."*

Two numbers from that paper settle the question for bacteria:

- HDBSCAN on a mandrake embedding of 20,047 pneumococcal genomes recovered PopPUNK's GPSCs with a Rand index of 0.987 and an **AMI of 0.085**. The Rand index is inflated by the many-small-clusters structure; the AMI is the honest number, and it is very poor. Their own headline validation shows embedding-derived clustering does not recover the reference scheme.
- In their coalescent simulations across five scenarios, *"we found that the UMAP embedding rarely reflected the underlying simulated population structure"*, with mandrake and PCA the most accurate and UMAP the worst.

PopPUNK itself never clusters from an embedding: assignments come from the 2D core–accessory plane and the network, both directly interpretable. Its Microreact output does include an embedding — historically t-SNE of accessory distances, now mandrake — but purely as a display panel. **Perplexity changes the picture and never changes the assignment.**

### Population genetics, briefly, and one citation to handle carefully

Elhaik E. Principal Component Analyses (PCA)-based findings in population genetic studies are highly biased and must be reevaluated. *Sci Rep* 2022;12(1):14683, PMID 36038559. **Note the title — the version circulating as "Why most Principal Component Analyses (PCA) in population genetic studies are wrong" is the preprint title.** The sound and uncontroversial part is that PCA output is sample-composition dependent; the inference that ~10⁵ studies require reevaluation is not accepted, no formal published rebuttal was found, and the author's follow-up applying the same argument in physical anthropology was retracted in 2025. Cite the sample-composition point; do not lean on the paper's framing.

Diaz-Papkovich et al.'s best-practice review (*J Hum Genet* 2021;66(1):85–91, PMID 33057159) is the more useful citation, and its advice is directly transferable: run multiple parametrisations, combine with PCA and model-based methods, and *"resist the tendency to assign a demographic explanation to each cluster without careful analysis"* — they show HLA-region technical artefacts producing spurious clusters.

### The rule

**Embeddings may be used to display externally-derived cluster labels, and never to define them.** If you show one: state the algorithm, the neighbour or perplexity parameter, the initialisation, and show at least two parameter settings; state in the legend that areas and between-cluster distances are not interpretable; never compute a statistic on 2D coordinates; and regenerate rather than reuse the embedding whenever the dataset changes.

No publication applying UMAP, t-SNE or mandrake to *B. pseudomallei* population structure was found — PubMed returns nothing for any of the three. And no peer-reviewed bacterial paper defining named lineages from embedding coordinates was found either, though that is a negative result and should be hedged.

---

## 6. What I would actually do

Ordered by expected value, and deliberately compatible with what Gap 1 already concluded.

**1. Run the size-distribution diagnostic today.** `cluster_diagnostics_bp.py --clusters …`. If the Gini is near 0.1 and max/min near 2, the Mash cut is imposing structure and everything downstream inherits that. If it looks like Chewapreecha's 0.46 and 34× with a long tail, the clustering is finding something and the argument shifts to which method finds it best. This costs minutes and changes what the rest of the work means.

**2. Check the Mash sketch size that produced the current clusters.** At the default s=1,000 the distance error at within-species range is ~14% relative. If the pipeline used defaults, the 61–76 clusters are partly noise and no amount of downstream validation repairs that.

**3. Refit with PopPUNK using Seng's published parameters** (`--min-k 15 --max-kmer 31 --max-a-dist 0.53 --K 4 --k-step 2`, v2.6.0), report density, transitivity and network score against the documented ≥0.8 bar, and report the betweenness-penalised variants as well. This is the one configuration with an in-organism precedent that demonstrably fed Gubbins successfully.

**4. Adopt the diversity criterion, since the literature has none.** Cap mean within-cluster pairwise core-SNP distance at ~1,000, calibrated against Seng's 351–549 and supported by the ≥20× contrast derivation. Report the distribution across clusters, plus per-cluster r/m and masked fraction from Gubbins afterwards. Say in print that no published threshold exists and that this is a construct.

**5. Use fastbaps in phylogeny-conditioned mode for sub-clustering**, not rhierbaps and not unconstrained fastbaps. It is monophyly-safe by construction, linear-time, is what PopPIPE uses, and rhierbaps will not finish at your scale.

**6. Validate with directional adjusted Wallace against the Lichtenegger cgMLST scheme**, not with ARI alone, and report confidence intervals. Add a treespace/Kendall-Colijn comparison at λ=0 following Seng's within-scheme-bootstrap-as-null design.

**7. Re-cluster a geographically and BioProject-balanced subsample and compare partitions.** Given 81% of Thai genomes from three BioProjects, this is a direct test of whether the clusters are biology or sequencing history, and it uses machinery the sampling audit already justifies.

**8. Add per-cluster bootstrap Jaccard stability** with Hennig's thresholds. Nearly unprecedented in bacterial genomics, cheap, and it isolates exactly the clusters that are artefacts of one over-sampled study.

**9. Do not adopt a SNP threshold, and say why.** The Sarovich 1,328→73 number is in your organism and makes the argument in one sentence. If a reviewer asks for a threshold, Webb 2022's sentence is the citation for its absence.

**10. If you keep any tree cut, drive the threshold with ReporTree's stability regions or a Hennart-style silhouette-plus-adjusted-Wallace scan on your own data.** Report the plateau, never a borrowed constant.

---

## 7. Corrections to the earlier documents

- **`treespace v1.14.3`** in the handoff's Gap 2 section should be **`treespace v. 1.1.4.3`**, as printed in Seng's Methods.
- **rPinecone is Wailan et al. 2019** (*Microb Genom* 5(4):e000264, PMID 30920366), not 2020 — and more importantly it is a **post-Gubbins** tool for low-variant populations, so it is not a candidate for the pre-Gubbins partition at all.
- **Lichtenegger et al. 2021 does not "refuse" to recommend a threshold** — as the main review's §3 has it — it simply never proposes one. Restate as a documented absence.
- **The handoff's Gap 2 framing — "is 61–76 wrong?" — should be inverted.** Seng's PopPUNK produced 101 lineages from 1,391 genomes of this species. Your count is coarser than the in-species precedent, not finer.
- **PopPIPE's fastbaps step is fixed at two levels with `min_cluster_size: 6`.** The handoff correctly notes it constrains subclusters to partitions of the phylogeny; it should also note that PopPIPE quotes the Gubbins diversity constraint in its introduction and then does not operationalise it. That gap is citable.

---

## 8. Still open after this pass

- **Whether BAPS-family or PopPUNK clusters track clonal descent under high r/m.** No benchmark exists. The two results that look reassuring both score against deme membership or simulated tree nodes rather than a known clonal genealogy. This is the same shape of gap as the SimBac benchmark the main review recommends, and the same simulation could answer both.
- **The length of Chewapreecha's core alignment**, still unreported, still leaving the ~772 kb divergence denominator unidentified. Carried over from Gap 1.
- **The per-species adjusted Rand indices behind PopPUNK's mean of 0.852** — supplementary table not retrieved.
- **Whether `--stable` (PopPUNK v2.7.0+) behaves acceptably on a recombinogenic species**; the documented behaviour is nearest-neighbour assignment with novel clusters flagged NA, but no benchmark on a species like this was found.
- **CRAN's current rhierbaps version** (GitHub `DESCRIPTION` says 1.1.3; a search result indicated 1.1.4 checked 2025-11-30). Immaterial given the runtime finding, but unresolved.
- **The full Gubbins CHANGELOG**, which could not be retrieved directly. Nothing in the visible release notes addresses divergence, filtering behaviour or preclustering, but the check was partial.
- **Two numbers flagged by the research passes as needing verification before citing**: the *Salmonella* clusterboot paper's internally inconsistent 0.515 figure, and McNally et al.'s 13%/86% core-versus-accessory incongruence percentages. Neither is load-bearing above.
