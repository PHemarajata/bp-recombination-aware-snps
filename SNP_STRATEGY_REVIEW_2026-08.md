# SNP, clustering and phylogeography strategy for *Burkholderia pseudomallei*

**A literature and data review, August 2026.**
Prepared against the existing pipeline: Mash clustering → per-cluster Gubbins + IQ-TREE → subtrees grafted onto a parsnp/FastTree backbone.

---

## The short version

Three things came out of this review, in descending order of how much they should change what you do.

**1. Your biggest problem is not recombination. It is sampling.**
I audited every public *B. pseudomallei* assembly in NCBI (n = 5,728, queried 2026-08-09). Thailand is 59.6% of the collection and Australia is 10.2%. Restrict to genomes with a usable country *and* collection year and it gets worse for inference, not better: Thailand 52.7%, Australia 7.9%. Worse still, 81% of the Thai genomes come from just three BioProjects. No choice of recombination tool, clustering algorithm, or tree method repairs this. Any statement your pipeline makes about geographic origin or directionality is, by default, a statement about where sequencing was funded.

**2. The masked alignment is the wrong output to build on; the corrected *tree* is the right one.**
This is a specific, well-evidenced methodological point that maps directly onto the branch-length problem already found in your backbone. Recombination masking reliably recovers *topology* but badly distorts *branch lengths* — and Hedge & Wilson showed masking can make branch-length distortion **worse**, not better. Didelot & Parkhill showed that at high recombination the non-recombinant-sites alignment can collapse to literally zero sites, while the ML clonal genealogy from the same tool stays accurate (weighted Robinson-Foulds 0.005 for ClonalFrameML, 0.03 for Gubbins).

**3. Your cluster-then-Gubbins design is right, and is the field standard — the graft is the part without precedent.**
Chewapreecha et al.'s global *B. pseudomallei* study did exactly this: hierBAPS partitioning, Gubbins within lineages, per-cluster dating. What they did *not* do is stitch the pieces into one global tree and interpret it. They dated per cluster and did geography by stochastic character mapping on subsampled trees. I could find no published method that validates grafting recombination-masked subtrees onto an unmasked backbone with different branch-length units.

---

## 1. The sampling audit

Queried the NCBI Datasets API for taxid 28450 on 2026-08-09. All 5,728 assemblies, with BioSample attributes.

### Metadata completeness

| Field | n | % |
|---|---|---|
| Total assemblies | 5,728 | 100% |
| Usable country | 5,516 | 96.3% |
| Usable collection year | 3,539 | 61.8% |
| **Both country and year** | **3,527** | **61.6%** |

Tip-dating discards roughly 38% of the collection before you start.

### Geography

| Country | All (n=5,728) | Dated + located (n=3,527) |
|---|---|---|
| Thailand | 3,414 (59.6%) | 52.7% |
| Australia | 586 (10.2%) | 7.9% |
| China | 403 (7.0%) | 10.2% |
| Singapore | 184 (3.2%) | 4.8% |
| Malaysia | 161 (2.8%) | 3.5% |
| Viet Nam | 158 (2.8%) | 4.4% |
| Hong Kong | 122 (2.1%) | 3.5% |
| India | 110 (1.9%) | 3.1% |
| USA | 87 (1.5%) | 2.4% |

Africa is essentially absent (Ghana 9, Madagascar 4). The Americas are represented almost entirely by Mexico (42) and the USA.

### The Thai majority is three studies, not a country sample

Of 3,414 Thai assemblies, the top three BioProjects account for **2,770 (81%)**: PRJEB3409 (1,506), PRJEB25606 (682), PRJEB35787 (582). Where sub-national labels exist they point at Ubon Ratchathani (186) and Nakhon Si Thammarat (108) — the known northeastern hotspot — but 3,104 of 3,414 carry no locality beyond "Thailand". The five largest BioProjects overall, all Thailand-dominated, are 61% of the entire public collection.

The practical consequence is pseudo-replication at the study level. Effective independent sampling is far below n.

### Temporal structure

Dated genomes span 1935–2025, median 2017, but the mass is concentrated:

| Period | n | % of dated |
|---|---|---|
| < 1990 | 53 | 1.5% |
| 1990–1999 | 188 | 5.3% |
| 2000–2009 | 571 | 16.1% |
| 2010–2014 | 422 | 11.9% |
| **2015–2019** | **1,792** | **50.6%** |
| 2020–2025 | 513 | 14.5% |

Half the calibration mass sits in a five-year window, and only 6.8% predates 2000. Expect weak temporal signal. Date-randomisation testing is mandatory here, not a nicety.

### Assembly quality

| Metric | Value |
|---|---|
| Contig N50 | median 133,172 (Q1 92,132; Q3 195,688) |
| Contig count | median 123 (Q1 88; Q3 177) |
| Total length | median 7,127,124; range 5,759,349 – 10,628,399 |
| Complete genomes | 389 (6.8%) |
| Any long-read platform | 518 (9.0%) |

The length tails are suspect — short assemblies are incomplete, long ones likely contaminated or mixed. Filter on total length.

Only 9% have long reads, so assembly-based SNP calling is not available for the bulk of the collection; reference mapping stays necessary. And because 92% are drafts, per-replicon analysis has to come from mapping coordinates against K96243 chromosomes I and II, not from the assemblies themselves.

### Analysable N

Requiring country + collection year + contig N50 ≥ 20 kb + total length 6.5–7.9 Mb leaves **3,436 genomes (60.0%)** — still 54.1% Thailand, 9.7% China, 8.1% Australia.

### What follows from this

- Any discrete-trait or mugration analysis run on the unweighted collection will be dominated by Thailand. Chewapreecha et al. inferred Australia as the early reservoir from a deliberately balanced 469-genome, 30-country set; today's public data inverts that ratio roughly sevenfold.
- Geographic subsampling is not optional preprocessing, it is the analysis. Chewapreecha et al. ran stochastic character mapping on *subsampled* phylogenies for exactly this reason.
- Report effective sample size per country and per BioProject alongside any phylogeographic claim.

---

## 2. Recombination: what the evidence actually supports

### Gubbins is being used outside its validated envelope if applied species-wide

Current release is **v3.4.3**. There is no separate v3 publication; the v3 changes are documented only in the repository. The validated behaviour comes from the original paper:

> Croucher NJ, Page AJ, Connor TR, et al. Rapid phylogenetic analysis of large samples of recombinant bacterial whole genome sequences using Gubbins. *Nucleic Acids Res.* 2015;43(3):e15. PMID 25414349. [10.1093/nar/gku1196](https://doi.org/10.1093/nar/gku1196)

The manual states the tool is for "samples of limited diversity, sharing a recent common ancestor" — strain or lineage level, not species-wide — and recommends subdividing populations when branches are long. For cross-species diversity it points users to fastGEAR instead.

The authors' own stated breakdown condition is precise and worth quoting in substance: detection fails as the expected density of point mutations rises toward the density at which substitutions are imported by recombination. That is exactly the deeply-divergent, within-species-donor case. They add that inaccuracies from high divergence "can be overcome by denser sampling or subdivision of the population prior to analysis."

Simulation performance, for calibration: recombination-event sensitivity ≈ 83%, PPV for recombination-imported substitutions > 99.5%, final branch-length correlation with truth median R = 0.996. But this envelope was established on simulated pneumococcal-parameterised data with divergent external donors, at recombination rates up to ρ = 0.75. **No published simulation extends this to a two-replicon 7.2 Mbp genome or to species-level sampling.** Runtime scales quadratically in sample number.

The manual also states explicitly: **do not run Gubbins on concatenated core-gene alignments** from Roary or Panaroo. The sliding-window scan needs true genomic coordinates.

### The three critiques that matter

**Branch lengths are the casualty, and masking can worsen them.**

> Hedge J, Wilson DJ. Bacterial phylogenetic reconstruction from whole genomes is robust to recombination but demographic inference is not. *mBio.* 2014;5(6):e02158-14. PMID 25425237. [10.1128/mBio.02158-14](https://doi.org/10.1128/mBio.02158-14)

Their finding: whole-genome tree topologies robustly reconstruct the clonal frame, but branch lengths are badly skewed — and *removing* recombining sites can exacerbate the distortion. Older recombination events are easier to detect than young ones, so masking removes evidence asymmetrically across the tree.

This is directly relevant to the implausible backbone branch lengths already measured in your pipeline. It says the topology is the robust product and the branch lengths are not — which is the same conclusion reached from the unit-mismatch argument, arrived at independently.

**At high recombination the masked alignment can vanish entirely — but the corrected tree survives.**

> Didelot X, Parkhill J. A scalable analytical approach from bacterial genomes to epidemiology. *Philos Trans R Soc Lond B Biol Sci.* 2022;377(1861):20210246. PMID 35989600. [10.1098/rstb.2021.0246](https://doi.org/10.1098/rstb.2021.0246)

This is the single most actionable paper found. Their demonstration: 20 sequences × 100 kb under a coalescent with ρ/2 = 0.001/site, δ = 1500 bp, donor distance ν = 0.05. Result — not a single site escaped recombination on at least one branch. An alignment of only non-recombinant sites would contain **no sites at all**.

But the inferred *clonal genealogy* from the same run had the same topology as truth and very similar branch lengths: weighted Robinson-Foulds 0.005 for ClonalFrameML, 0.03 for Gubbins with RAxML.

They add a hard constraint that is easy to violate accidentally: **alignments of variant sites cannot be used for recombination-aware phylogenetics**, because the genomic distance between variant sites is itself an input to the method. Gubbins and ClonalFrameML need the full-length pseudogenome, and snp-sites belongs *after* the recombination step, not before.

Their worked example (*S. aureus* ST239, 521 genomes vs TW20) gives useful runtime expectations: PhyML ~3 h, ClonalFrameML ~2 days, Gubbins v2.4.1 ~1 day. R/θ = 0.144, δ = 619 bp, ν = 0.31%, r/m = 0.28. Recombination correction made the temporal signal clearer, not weaker (root-to-tip R² = 0.57).

**The deeper challenge: there may be no clonal frame to recover.**

> Sakoparnig T, Field C, van Nimwegen E. Whole genome phylogenies reflect the distributions of recombination rates for many bacterial species. *eLife.* 2021;10:e65366. PMID 33416498. [10.7554/eLife.65366](https://doi.org/10.7554/eLife.65366)

For *E. coli*, only 27.4% of SNPs support the core-tree topology; the phylogeny changes roughly every 5–10 SNP columns (~50–100 nt), tens of thousands of times along the genome; each position has been overwritten by recombination at least 190 times; 78% of strain pairs are fully recombined. Cross-species C/M: *H. pylori* 0.3, *E. coli* / *B. subtilis* / *S. enterica* ~0.12–0.15, *S. aureus* ~0.10, *M. tuberculosis* 0.08.

Their direct critique of Gubbins and ClonalFrameML is that both assume the whole-genome reference tree represents clonal ancestry and then call deviations recombination — a premise they argue has no rigorous justification. They also argue that describing a species by a single ρ/μ is misleading, because recombination rates between lineages vary over several orders of magnitude.

The strongest counter-argument, from John Lees, is that this attacks a straw man: practitioners already partition into strains before recombination detection, and few would infer clonal ancestry from a whole-species tree. His proposed pipeline — PopPUNK strain partitioning → Gubbins/ClonalFrameML within strain → per-strain phylogeny — is compatible with Sakoparnig's findings. That is, notably, the architecture you already have, minus the graft.

### Why clusters are biologically real in this organism

> Nandi T, Holden MTG, Didelot X, et al. *Burkholderia pseudomallei* sequencing identifies genomic clades with distinct recombination, accessory, and epigenetic profiles. *Genome Res.* 2015;25(1):129–41. PMID 25236617. [10.1101/gr.177543.114](https://doi.org/10.1101/gr.177543.114)

Recombination in *B. pseudomallei* is **clade-specific**: ongoing within clades, rarely observed between them. The mechanism is that each clade carries a distinct complement of restriction-modification systems, producing clade-specific methylation, and those RM systems block uptake of non-self DNA. The authors conclude that genomic clades "may represent functional units of genetic isolation."

This matters for your design. It means partitioning first and running Gubbins within partitions is not merely a computational convenience to stay inside Gubbins' envelope — it matches where recombination actually happens in this organism. It also implies deep, between-clade branches carry proportionally *less* recombination than the species-wide rate suggests, which is a testable prediction against your backbone.

### Alternatives to detect-and-mask

**fastGEAR** is the only tool found with published evidence of detecting *ancestral*, deep-branch recombination.

> Mostowy R, Croucher NJ, Andam CP, et al. Efficient inference of recent and ancestral recombination within bacterial populations. *Mol Biol Evol.* 2017;34(5):1167–1182. PMID 28199698. [10.1093/molbev/msx066](https://doi.org/10.1093/molbev/msx066)

In their simulations of ancestral recombination, fastGEAR detected events that Gubbins, ClonalFrameML, BRATNextGen and STRUCTURE all missed entirely. Caveat: distributed as MATLAB/MCR code from a personal URL; current maintenance status was not verified.

**Verticall** is the newest attempt at the scale-and-diversity ceiling.

> Odih EE, Wick RR, Holt KE (London School of Hygiene & Tropical Medicine). Verticall: A fast and robust tool for recombination detection in large-scale bacterial genomic datasets. *bioRxiv*, posted 2026-04-24, v1. [10.64898/2026.04.21.719734](https://doi.org/10.64898/2026.04.21.719734). **Preprint, not peer reviewed and not yet journal-published.** Current version 0.4.3. Code: https://github.com/rrwick/Verticall

Metadata and abstract verified directly against bioRxiv. It works on pairwise assembly comparisons and assigns genomic regions as horizontally or vertically related non-parametrically, from the distribution of pairwise genetic distances between genomes. Two workflows: a **distance-tree** approach (pairwise distance matrix from vertical-only regions) and an **alignment-tree** approach (all genomes compared to a reference, horizontal regions masked in a pseudo-alignment).

Benchmarks cover four public datasets of **154–4,857 genomes**, from within-lineage to genus-wide diversity. Across all four, Verticall reported "comparable or superior performance to the established tools Gubbins and ClonalFrameML in terms of computational efficiency, plausibility of inferred phylogenetic trees, and recovery of temporal signal for molecular dating." Per-dataset detail could not be retrieved, and the benchmarks are developer-run with no independent evaluation. Analysis code and data are posted (figshare 10.6084/m9.figshare.31930821; github.com/erkison/verticall_paper), so the claims are at least checkable.

The impact statement makes the positioning explicit: existing tools "are not suitable for datasets with very high diversity or thousands of genomes," and Verticall "produces comparable results to existing software for smaller more clonal datasets, but also performs well on datasets that the existing packages cannot handle." That is your dataset's shape.

The authors' own caveat is worth heeding: "if your dataset is suitable for Gubbins (i.e. a small and closely related group of genomes), then it will probably give you better results." It also needs assemblies with reasonable N50 — which, given 92% of public genomes are drafts with median N50 133 kb, is a real but probably surmountable constraint.

Real uptake exists: Verticall v0.4.2 was used for recombination filtering ahead of BactDating in a 2025 *Genome Medicine* One Health study of *Klebsiella pneumoniae* (PMID 40296028).

**Chromosome painting** (ChromoPainter/fineSTRUCTURE) is what the *H. pylori* community — the highest-recombination species tested by Sakoparnig — uses instead of detect-and-mask (Yahara et al., *Mol Biol Evol.* 2013;30(6):1454–64, PMID 23505045).

**SimBac** deserves a mention because it addresses the honest gap here: nobody has benchmarked any of these tools at *B. pseudomallei* recombination levels on a two-replicon 7.2 Mbp genome. You could (Brown T, Didelot X, Wilson DJ, De Maio N. *Microb Genom.* 2016;2(1). PMID 27713837).

**RCandy** lets you inspect what Gubbins actually masked rather than trusting it (Chaguza C, et al. *Bioinformatics.* 2022;38(5):1450–1451. PMID 34864895).

### What could not be verified

The web-search budget for this session was exhausted, leaving real gaps:

- **No verified r/m figure for *B. pseudomallei*.** Search summaries suggested a recombination-to-mutation ratio more than twice that of *S. pneumoniae*, and that ≥78% of the K96243 reference has undergone recombination, but the source papers were not retrieved. Treat both as unconfirmed.
- No published r/m threshold at which the standard approach is demonstrated to break down. The evidence is qualitative.
- Nothing verified on ARG-aware methods in bacteria (ARGweaver, tsinfer/tskit, Relate, bacter). Silence here is not evidence either way. What *was* verified: ClonalOrigin has been integrated into BEAST2 but is too computationally intense for whole-genome datasets.
- Maintenance status of ClonalFrameML, fastGEAR and BRATNextGen.
- No independent 2023–2026 benchmark comparing recombination-detection tools was found.
- Three of the five research streams commissioned for this review (reference-free/k-mer methods, clustering algorithms, and pipeline/scale questions) did not return before the search budget ran out. So this document is thin on SKA2, PopPUNK/PopPIPE, fastbaps versus hierBAPS, TreeCluster, nf-core pipelines, and ascertainment-bias handling in IQ-TREE. Those affect *how* you implement the recommendations below, not *whether* they hold.

---

## 3. The field standard for *B. pseudomallei* phylogeography

> Chewapreecha C, Holden MTG, Vehkala M, Välimäki N, Yang Z, Harris SR, Mather AE, Tuanyok A, De Smet B, Le Hello S, Bizet C, Mayo M, Wuthiekanun V, Limmathurotsakul D, Phetsouvanh R, Spratt BG, Corander J, Keim P, Dougan G, Dance DAB, Currie BJ, Parkhill J, Peacock SJ. Global and regional dissemination and evolution of *Burkholderia pseudomallei*. *Nat Microbiol.* 2017;2:16263. PMID 28112723. [10.1038/nmicrobiol.2016.263](https://doi.org/10.1038/nmicrobiol.2016.263)

469 isolates, 30 countries, 79 years. The method, in order:

1. Map to **K96243**, chromosomes I and II, with SMALT v0.7.4. 324,637 SNPs.
2. **hierBAPS** partitioning into 19 groups, with an explicit stopping criterion: keep subdividing until within-cluster diversity falls **within Gubbins' recombination-detection limit**.
3. **Gubbins within lineages**, not globally.
4. **BEAST per cluster, and separately per chromosome** (I vs II) to validate temporal signal. Strict clock, chosen over relaxed by model comparison; Bayesian skyline tree prior.
5. Temporal signal checked by root-to-tip regression (Path-O-Gen) **and date-randomisation with 1,000 permutations**.
6. Geography by **stochastic character mapping** (phytools, asymmetric ARD model, 1,000 simulations) on **subsampled** phylogenies — not BEAST discrete trait analysis.

Their conclusions: Australia as early reservoir, onward transmission to Southeast then South and East Asia; repeated reintroductions within the Malay Peninsula and among Mekong-bordering countries; African origin for Central/South American isolates, introduced 1650–1850, temporally consistent with the slave trade.

**The design lesson is what they did not do.** There is no single global dated tree. Dating happens per cluster. Geography happens by ancestral state reconstruction on subsampled trees. The step your pipeline adds — grafting the subtrees onto a backbone and treating the result as one object — has no counterpart in the reference study.

That stopping criterion in step 2 is also worth stealing outright. Your Mash clustering produces 61–76 clusters with no principled size criterion; theirs subdivides until each partition is inside the range where the next tool is valid. That is a defensible rule, and it is testable.

### The largest current dataset

> Wu H, Lei Z, Chen S, et al. Genomic landscape and phylogenetic insights of *Burkholderia pseudomallei* over two decades in southern China and its global surveillance. *Emerg Microbes Infect.* 2026;15(1):2691358. PMID 42377320. [10.1080/22221751.2026.2691358](https://doi.org/10.1080/22221751.2026.2691358)

554 southern-China isolates plus 3,573 public global genomes (~4,127 total), core-genome SNP phylogenies from recombination-masked alignments, resolving **10 evolutionary clusters**. Chinese isolates enriched in Cluster 1 (shared with Thai strains) and distinct from Cluster 5 (predominantly Australian). Pan-genome analysis confirmed functional compartmentalisation between the two replicons. Paywalled; methods detail could not be retrieved.

This is the closest published comparator to your ~2,800-genome run, and 10 clusters versus your 61–76 is a large enough discrepancy to be worth understanding.

### Chromosome I and II are not interchangeable

Chromosome 2 is the more divergent replicon, accessory-rich, with roughly ten-fold fewer core genes than chromosome 1. Published trees from the two replicons contain the same clades but contradict each other on strain placement, attributed to clade-specific recombination and accessory exchange. Chewapreecha et al. ran BEAST separately per chromosome for precisely this reason.

For K96243 specifically: 16 genomic islands, ~6% of the genome; 71 genomic islands identified across five reference strains; 86% of K96243 is core to all strains, 14% variable.

### The allele-based alternative

> Lichtenegger S, Trinh TT, Assig K, Prior K, Harmsen D, Pesl J, Zauner A, Lipp M, Que TA, Mutsam B, Kleinhappl B, Steinmetz I, Wagner GE. Development and validation of a *Burkholderia pseudomallei* core genome multilocus sequence typing scheme to facilitate molecular surveillance. *J Clin Microbiol.* 2021;59(8):e0009321. PMID 33980649. [10.1128/JCM.00093-21](https://doi.org/10.1128/JCM.00093-21)

A "soft defined" core genome, obtained by challenging K96243 with 469 environmental and clinical genomes: **4,221 core plus 1,351 accessory targets**, then validated on 320 further datasets. More than 95% of targets called well in 98.4% of genomes. Hosted in Ridom SeqSphere+ and at cgMLST.org, indexed by Pathogenwatch. The cgMLST UPGMA tree clustered global isolates similarly to the published global SNP phylogeny and detected homoplasy concordantly; five SNPs corresponded to two allele differences in a transmission pair. The authors report it works "not only for closely related strains but also the global *B. pseudomallei* population structure."

Two honest limitations: the authors do **not** claim recombination robustness, and they recommend **no** allele-difference clustering thresholds. Resolution was slightly below SNP+indel methods for very closely related environmental isolates.

Worth running as an independent check on cluster assignment, not as a replacement.

---

## 4. On the graft specifically

I searched for published precedent for the backbone-plus-grafted-subtrees design and found none that fits.

- **uDance** (*Nat Biotechnol.* 2023, [10.1038/s41587-023-01868-8](https://doi.org/10.1038/s41587-023-01868-8)) does updatable divide-and-conquer at ~200,000 genomes, but on 387 marker genes at cross-domain scale — not within-species SNP work.
- **NJMerge** and supertree methods are statistically consistent for combining subset trees, but they combine trees built the same way, not recombination-masked subtrees onto an unmasked backbone.
- **GTDB-Tk v2** uses backbone-then-subtree placement, but for taxonomic classification, not within-species phylogeny.

Nothing validates joining trees whose branch lengths are in different units. That remains the structural objection, and it is independent of the recombination question.

---

## 5. What I would change

Ordered by expected value.

**First, settle the backbone diagnostic that is already outstanding.** Before attributing the inflated backbone branch lengths to recombination, verify that `backbone_alignment.fa` contains records of equal length. The module has fallback paths that copy raw concatenated representatives, and if a fallback fired, FastTree was handed unaligned sequence — which would explain 25× inflation with no recombination involved. This is cheap and it is a prerequisite for interpreting anything else. Publish that file so the check is repeatable.

**Second, stop treating the grafted tree as a distance object.** Hedge & Wilson give you the citation: topology is robust, branch lengths are not, and masking can worsen them. Document the grafted tree as topology-only. This costs nothing and is defensible.

**Third, replace ad-hoc Mash clustering with a criterion tied to the next tool.** Chewapreecha's rule — subdivide until within-cluster diversity falls inside Gubbins' detection range — is principled, published, and gives you a stopping condition you can defend. Compare the resulting partition against hierBAPS or fastbaps, and against the 10 clusters reported by Wu et al.

**Fourth, use the recombination-corrected clonal genealogy, not the masked alignment.** This is the Didelot & Parkhill result. It also removes the per-variable-site denominator that creates half your unit mismatch. Related and easy to get wrong: Gubbins must receive full-length pseudogenomes, never a SNP-only alignment, and snp-sites belongs after Gubbins.

**Fifth, weight or subsample by geography before any phylogeographic claim.** Given 54% Thailand and 8% Australia in the analysable set, and 81% of Thai genomes from three BioProjects, this determines whether your conclusions mean anything. Follow Chewapreecha in running ancestral state reconstruction over repeated subsamples rather than once on everything.

**Sixth, analyse the two chromosomes separately, at least as a validation.** Concordance between replicon trees is a free check on whether a clade is real or a recombination artefact, and discordance is itself publishable. Since 92% of genomes are drafts, replicon assignment has to come from K96243 mapping coordinates.

**Seventh, if you intend to date anything, run date-randomisation first and be prepared for the answer to be no.** Half the calibration mass is in 2015–2019 and only 6.8% predates 2000.

**Worth evaluating, not adopting blind:** Verticall v0.4.3 on the full collection, head-to-head against per-cluster Gubbins; fastGEAR for deep-branch recombination that Gubbins is documented to miss; and SimBac to benchmark your own pipeline at *B. pseudomallei*-like parameters, since nobody else has.

---

## Sources

Primary literature is cited inline above with PMIDs and DOIs; article metadata was retrieved from PubMed. The sampling audit is original analysis of the NCBI Datasets API (taxid 28450), queried 2026-08-09; the summary table is saved alongside this document as `bp_public_genome_audit_2026-08-09.csv`.

Gaps are stated explicitly in §2. The web-search budget for the session was exhausted before the r/m literature for *B. pseudomallei* and the ARG-aware methods literature could be checked.
