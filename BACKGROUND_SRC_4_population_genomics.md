# *Burkholderia pseudomallei*: Population Structure, Phylogeography and Comparative Genomics

Literature research for the Background section of a recombination-aware SNP genomics manuscript.

**Compiled:** 2026-09-02
**Verification method:** All metadata (PMID / PMCID / DOI / volume / pages) cross-checked against the Europe PMC REST API (`resultType=core`). Full-text claims were extracted from PMC / publisher HTML. Where a number could not be retrieved from a primary source it is marked **UNVERIFIED** with a statement of exactly what is missing.

**Important tooling caveat for the reader:** the PubMed MCP tools were unavailable in this session (blocked by a safety classifier), as was outbound `curl`. All retrieval was via WebFetch/WebSearch. Full-text extraction therefore passed through a summarising model; every load-bearing number below was either (a) obtained as an explicit verbatim quote, and in several cases re-fetched independently, or (b) flagged as unverified. Two hallucinated values were caught and corrected during this process (see §10, "Errors caught during verification").

---

## 0. Three corrections to premises supplied in the research brief

Before the substantive review, three factual corrections. Each matters because the brief's version would put a wrong number into the manuscript.

**(a) PMID 41662344 is not a 1,468-genome study.** The brief describes "the 2026 North Central Vietnam study (PMID 41662344, 1,468 genomes)". The paper is Norris MH *et al.*, *PLoS Negl Trop Dis* 2026;20(2):e0013945 (PMCID PMC12900444, DOI 10.1371/journal.pntd.0013945). It **newly characterised 47 isolates** from Ha Tinh province — "35 clinical *B. pseudomallei* isolates, ten from soil, one from swine, and one from a bear" — yielding 15 STs, four of them novel. The number 1,468 is the size of the **global comparison set**, not the study's own sequencing effort: "Whole genome SNP analysis of 1,468 *B. pseudomallei* strains from Australia and Southeast Asia, **including the 47 from this work**." Citing it as a 1,468-genome Vietnamese study would be wrong.

**(b) PMID 35080450 (Webb *et al.* 2022) is not primarily about localised genotype clusters within Darwin.** Its actual title is "Genomic Epidemiology Links *Burkholderia pseudomallei* from Individual Human Cases to *B. pseudomallei* from Targeted Environmental Sampling in Northern Australia" (*J Clin Microbiol* 2022;60(3):e0164821, DOI 10.1128/jcm.01648-21). It is a case-to-environment source-attribution study. The paper that establishes **localised, fine-scale genotype clustering within urban Darwin** is a different one: Rachlin A, Mayo M, Webb JR, Kleinecke M, Rigas V, Harrington G, Currie BJ, Kaestli M, *Sci Rep* 2020;10:5443 (DOI 10.1038/s41598-020-62300-8, PMID 32214186). Both are covered below; they should not be conflated.

**(c) PMID 42377320 (Wu *et al.* 2026) reports 554 culture-confirmed melioidosis *cases*, and the "3,805,619 bp core alignment" could not be verified.** See §4.2. The publisher site (Taylor & Francis) returned HTTP 403 and there is no PMC deposit, so only the abstract was obtainable.

---

## 1. MLST-era population structure

### 1.1 The scheme (Godoy *et al.* 2003)

The 7-locus MLST scheme for the *B. pseudomallei* complex was published by Godoy D, Randle G, Simpson AJ, Aanensen DM, Pitt TL, Kinoshita R, Spratt BG. *J Clin Microbiol* 2003;41(5):2068–2079 (PMCID PMC154742, DOI 10.1128/jcm.41.5.2068-2079.2003, PMID 12734250).

- Loci: ***ace, gltB, gmhD, lepA, lipA, narK, ndh*** — confirmed independently against the live PubMLST scheme definition (see §1.2).
- The original collection comprised **147 isolates** of *B. pseudomallei*, *B. mallei* and *B. thailandensis*, of which **128 *B. pseudomallei*** isolates were resolved into **71 sequence types**; the full 147-isolate collection yielded **81 distinct allelic profiles**.
- Allele counts per locus among the 128 *B. pseudomallei*: reported in the range **4–15 alleles per locus, mean 8.6**. *(Retrieved via full-text extraction; the paper's exact sentence was not returned verbatim, so treat the 8.6 mean as SECOND-ORDER — verify against the PDF before printing it.)*
- **NOT PRESENT in Godoy 2003:** any numeric recombination-to-mutation ratio, and any eBURST/clonal-complex analysis. Repeated targeted searches of the full text returned "NOT PRESENT" for both. Do **not** attribute the well-known per-allele r/m figure to this paper — it belongs to Pearson 2009 (§2.2).

### 1.2 PubMLST database size (live figures, as accessed 2026-09-02)

Retrieved from the PubMLST organism page and the BIGSdb REST API (`rest.pubmlst.org/db/pubmlst_bpseudomallei_seqdef/schemes/1`):

| Quantity | Value | "Last updated" as shown |
|---|---|---|
| ST profiles (MLST scheme, `records`) | **2,628** | 2026-08-25 |
| Isolates in the typing database | **7,697** | 2026-08-14 |
| Allele sequences | **650,966** | — |
| Genomes in the genome collection | **1,175** | 2026-06-17 |
| Loci in the MLST scheme | **7** (*ace, gltB, gmhD, lepA, lipA, narK, ndh*) | — |

Caveat for the manuscript: these are live counts and will drift. State the access date. Note also that the public REST API returned "you are currently restricted to accessing data that was submitted on or prior to 2024-12-31" for the *isolates* database, so the 7,697 figure (from the web front page) and the 2,628 figure (from the seqdef REST endpoint) come from two different access paths.

### 1.3 The Australia / Asia split in MLST data

Two papers establish this and they are the ones to cite:

**Vesaratchavest M, Tumapa S, Day NPJ, Wuthiekanun V, Chierakul W, Holden MTG, White NJ, Currie BJ, Spratt BG, Feil EJ, Peacock SJ.** "Nonrandom distribution of *Burkholderia pseudomallei* clones in relation to geographical location and virulence." *J Clin Microbiol* 2006;44(7):2553–2557 (PMCID PMC1489466, DOI 10.1128/jcm.00629-06, PMID 16825379). Verbatim from the abstract:

> "A total of 266 Thai *B. pseudomallei* isolates were characterized (83 soil and 183 invasive). These corresponded to 123 sequence types (STs), the most abundant being ST70 (n=21), ST167 (n=15), ST54 (n=12), and ST58 (n=11)."

> "MLST profiles for 158 isolates from Australia (mainly disease associated) contained a number of STs (96) similar to that seen with the Thai invasive isolates, but **no ST was found in both populations**. There were also differences in diversity and allele frequency distribution between the two populations. This analysis reveals strong genetic differentiation on the basis of geographical isolation and a significant differentiation on the basis of virulence potential."

**Currie BJ, Thomas AD, Godoy D, Dance DAB, Cheng AC, Ward L, Mayo M, Pitt TL, Spratt BG.** "Australian and Thai isolates of *Burkholderia pseudomallei* are distinct by multilocus sequence typing." *J Clin Microbiol* 2007;45(11):3828–3829 (PMCID PMC2168502, DOI 10.1128/jcm.01590-07, PMID 17898162). Verbatim:

> "At present, there are **178 STs from Australia and 224 STs from Thailand** represented in the database"

> "there is **no ST common to isolates verified as obtained from Australia or from Thailand**"

> "**complete separation of Australian and Thai STs** among those isolates whose origins are verifiable from original sources"

This 2007 note is important methodologically: the apparent Australia–Thailand ST overlap that existed in the database at the time turned out to be a database curation artefact (the original Australian ST60 isolates were not *B. pseudomallei* and likely originated from Thailand — "a case of mistaken identity"). It is an early, explicit demonstration that database provenance metadata, not just the genotype, drives phylogeographic conclusions.

### 1.4 eBURST clonal complexes

From Vesaratchavest 2006 (verbatim):

> "Two clusters of related STs (clonal complexes) were identified; the larger clonal complex (**CC48**) did not conform to a simple pattern of radial expansion from an assumed ancestor, while a second (**CC70**) corresponded to a simple radial expansion from ST70."

Note the asymmetry the same paper reports: Australian isolates show markedly greater eBURST-visible diversity than Thai isolates, consistent with the Australia-as-ancestral-reservoir hypothesis (§2, §3).

Malaysian veterinary/environmental isolates have been assigned to **CC48**, described as "found in Southeast Asia" — but this comes from a secondary summary rather than a verbatim quote and I did not obtain the primary paper, so treat as **UNVERIFIED**; if used, retrieve the Malaysian veterinary isolate paper directly.

### 1.5 ST562 — the exemplar geographically restricted ST, and the exemplar of why ST identity ≠ geographic identity

**Meumann EM, Kaestli M, Mayo M, Ward L, Rachlin A, Webb JR, Kleinecke M, Price EP, Currie BJ.** "Emergence of *Burkholderia pseudomallei* Sequence Type 562, Northern Australia." *Emerg Infect Dis* 2021;27(4):1057–1067 (PMCID PMC8007296, DOI 10.3201/eid2704.202716, PMID **33754984**). Abstract, verbatim:

> "Since 2005, the range of *Burkholderia pseudomallei* sequence type 562 (ST562) has expanded in northern Australia. During 2005–2019, ST562 caused melioidosis in 61 humans and 3 animals. Cases initially occurred in suburbs surrounding a creek before spreading across urban Darwin, Australia and a nearby island community. In urban Darwin, ST562 caused 12% (53/440) of melioidosis cases, a proportion that increased during the study period. We analyzed 2 clusters of cases with epidemiologic links and used genomic analysis to identify previously unassociated cases. We found that ST562 isolates from Hainan Province, China, and Pingtung County, Taiwan, were distantly related to ST562 strains from Australia. Temporal genomic analysis suggested a single ST562 introduction into the Darwin region in ≈1988. The origin and transmission mode of ST562 into Australia remain uncertain."

Key quantitative results (from full text; the SNP figures are load-bearing and worth re-checking against the PDF before final submission):
- Isolates sequenced: 71 Australian (61 human incl. 3 recurrent, 3 animal, 4 environmental), plus 5 from Hainan and 1 from Pingtung County, Taiwan.
- Estimated single introduction into the Darwin region: **≈1988 (95% HPD 1961–2001)**.
- **Hainan/Taiwan ST562 vs Australian ST562: 6,252–7,786 SNPs; 964–1,453 SNPs after excluding recombinogenic regions.**

That last line is the single most useful number in this whole review for a recombination-aware SNP manuscript. Two isolates with an **identical 7-locus ST**, from opposite ends of the species range, are separated by thousands of raw SNPs; masking recombination reduces the distance by roughly 5–8×, but still leaves ~1,000 SNPs. The ST is uninformative about geography here; the recombination-masked core SNP distance is decisive.

### 1.6 ST-based clustering: the documented failure modes

Three papers give explicit, quantified demonstrations that shared ST does not imply relatedness or shared origin.

**(i) Intercontinental ST homoplasy.** De Smet B, Sarovich DS, Price EP, Mayo M, Theobald V, Kham C, Heng S, Thong P, Holden MTG, Parkhill J, Peacock SJ, Spratt BG, Jacobs JA, Vandamme P, Currie BJ. "Whole-genome sequencing confirms that *Burkholderia pseudomallei* multilocus sequence types common to both Cambodia and Australia are due to homoplasy." *J Clin Microbiol* 2015;53(1):323–326 (PMCID PMC4290968, DOI 10.1128/jcm.02574-14, PMID 25392354). Abstract, verbatim:

> "*Burkholderia pseudomallei* isolates with shared multilocus sequence types (STs) have not been isolated from different continents. We identified two STs shared between Australia and Cambodia. Whole-genome analysis revealed substantial diversity within STs, **correctly identified the Asian or Australian origin**, and confirmed that these shared STs were due to homoplasy."

Note both halves: MLST failed, WGS succeeded in assigning continent.

**(ii) Intracontinental ST homoplasy.** Aziz A, Sarovich DS, Harris TM, Kaestli M, McRobb E, Mayo M, Currie BJ, Price EP. "Suspected cases of intracontinental *Burkholderia pseudomallei* sequence type homoplasy resolved using whole-genome sequencing." *Microb Genom* 2017;3(11):e000139 (PMCID PMC5729916, DOI 10.1099/mgen.0.000139, PMID 29208140). Verbatim:

> "we used whole-genome sequencing to identify the first reported instances of intracontinental ST homoplasy, which involved ST-722 and ST-804 *B. pseudomallei* isolates separated by large geographical distances."

> "MLST can occasionally lead to **erroneous conclusions about isolate origin and disease attribution**. In cases where a shared ST is identified between geographically distant locales, whole-genome sequencing should be used to resolve strain origin."

SNP distances between same-ST, geographically distant pairs:
- ST-722: MSHR0052 vs MSHR9076 — **21,211 SNPs** (≈300 km apart)
- ST-804: MSHR3528 vs MSHR4608 — **20,567 SNPs** (≈1,000 km apart)

**(iii) The converse — non-clonal outbreaks where distinct STs are actually one epidemiological event.** Sarovich DS, Chapple SNJ, Price EP, Mayo M, Holden MTG, Peacock SJ, Currie BJ. "Whole-genome sequencing to investigate a non-clonal melioidosis cluster on a remote Australian island." *Microb Genom* 2017;3(8):e000117 (PMCID PMC5610713, DOI 10.1099/mgen.0.000117, PMID 29026657). Verbatim:

> "We analysed the genome-wide relatedness of the two most common multilocus sequence types (STs) involved in the outbreak, STs 125 and 126. This analysis showed that although these STs were closely related on a whole-genome level, they demonstrated **evidence of multiple recombination events that were unlikely to have occurred over the timeframe of the outbreak**."

> "**ST-125 and ST-126 isolates are separated by 1328 SNPs or 1482 SNP-indel variants.**"

> "Despite PFGE being unable to discriminate between ST-125 and ST-126, these STs differ by at least 1328 SNPs and 154 indels on the whole-genome level."

> "Given the genetic diversity of infecting isolates, this case cluster was likely caused by a **polyclonal *B. pseudomallei* population** that had contaminated the unchlorinated community water supply."

This paper cuts both ways and should be cited carefully: it is simultaneously (a) evidence that a single point source can seed a polyclonal outbreak, so genomic non-identity does not exclude a common source, and (b) an explicit statement that recombination generates SNP differences on timescales far shorter than a naive molecular clock would imply.

**(iv) A directly relevant EID statement on MLST resolution** (from Gee 2017, §4.5), verbatim:

> "Although MLST is the most common method to subtype isolates of *B. pseudomallei*, over time it has become recognized that **it lacks the resolution to firmly link an isolate to a specific geographic origin**"

---

## 2. Pearson *et al.* 2009 (BMC Biol 7:78)

**Full citation:** Pearson T, Giffard P, Beckstrom-Sternberg S, Auerbach R, Hornstra H, Tuanyok A, Price EP, Glass MB, Leadem B, Beckstrom-Sternberg JS, Allan GJ, Foster JT, Wagner DM, Okinaka RT, Sim SH, Pearson O, Wu Z, Chang J, Kaul R, Hoffmaster AR, Brettin TS, Robison RA, Mayo M, Gee JE, Tan P, Currie BJ, Keim P. "Phylogeographic reconstruction of a bacterial species with high levels of lateral gene transfer." *BMC Biol* 2009;7:78. PMID **19922616**, PMCID **PMC2784454**, DOI **10.1186/1741-7007-7-78**.

### 2.1 Data

- **43 whole genome sequences** of *B. pseudomallei* and near neighbours (23 *B. pseudomallei*, 10 *B. mallei*, 5 *B. thailandensis*, 5 other near neighbours).
- **14,544 orthologous shared SNPs** (the abstract says ">14,000"). Verbatim: *"Bayesian phylogenetic analyses of >14,000 single nucleotide polymorphisms yielded completely resolved trees for these 43 strains with high levels of statistical support."*
- MLST layer: verbatim — *"We therefore analyzed MLST data from >1,700 isolates of B. thailandensis, B. pseudomallei, and B. mallei from an online database http://bpseudomallei.mlst.net **downloaded on July 28, 2008**."* Approximate composition: 47% Southeast Asia, 45% Australasia, 8% other.

### 2.2 The r/m ratio — **PER-ALLELE, MLST LOCI ONLY**

Verbatim:

> "In contrast to *H. pylori*, recombination in *B. pseudomallei* is **between 18 and 30 times more likely to generate new alleles than mutation**, a result consistent with previous analyses."

And from the abstract:

> "A comparison of recombination levels and diversity at **seven housekeeping genes** for eleven bacterial species... shows that the relative contributions of homologous recombination versus mutation for *Burkholderia pseudomallei* is **over two times higher than for *Streptococcus pneumoniae*** and is thus the **highest value yet reported in bacteria**."

**Explicit warning for the manuscript:** this 18–30× figure is a **per-allele ratio at the seven MLST housekeeping loci** (ρ/θ-type, "how much more likely is a new *allele* to arise by recombination than by point mutation"). It is **not** a genome-wide r/m (the ratio of *nucleotide substitutions* introduced by recombination versus mutation). The two quantities differ by roughly an order of magnitude in interpretation and must never be merged, averaged, or presented as interchangeable. The genome-wide, Gubbins-derived r/m values published for this species are **2.2–4.6** (Seng 2024, §4.1) — an order of magnitude smaller than 18–30 and measuring a different thing. A Background section that writes "r/m for *B. pseudomallei* is 18–30, the highest reported in bacteria" without the per-allele qualifier is making an error that a reviewer with population-genetics training will catch.

### 2.3 STRUCTURE analysis

- K tested from 1 to 5 across 10 iterations. **K = 2 was supported**: one population largely Australian, one largely Southeast Asian.
- Increasing K retained the two major populations but subdivided both.
- STs from other regions (Africa, the Americas, South Asia) clustered with one or other of the two, i.e. no separate third global population was resolved by MLST.

### 2.4 Φ_PT and F_ST

Verbatim:

> "The extant *B. pseudomallei* form two populations: one composed largely of Australian isolates and one composed largely of Southeast Asian isolates (**Φ_PT = 0.117; P = 0.001**; Figure 3)."

The paper's own interpretation: this "statistically significant Φ_PT value suggests that these two populations are sexually isolated from each other."

Verbatim on F_ST:

> "The low divergence of the Australasian population and high divergence of the Southeast Asian population is expected, given our phylogenetic analyses which show that the Australasian population is paraphyletic and ancestral to the monophyletic Southeast Asian population (**F_ST = 0.03 and 0.21 for the Australasian and Southeast Asian populations, respectively**)."

Note these two F_ST values are each population's divergence from the *inferred ancestral* population, not a pairwise F_ST between the two extant populations. Φ_PT = 0.117 is the between-population differentiation statistic. Do not present F_ST = 0.03/0.21 as a pairwise Australia-vs-Asia F_ST.

Interpretively, Φ_PT = 0.117 is a **modest** differentiation coefficient. It says roughly 12% of the variance partitions between the two continental populations and ~88% within them. This is the quantitative core of the "geographic signal exists but is weak at MLST resolution" argument.

### 2.5 The Australian-origin hypothesis and its stated contingency on the root

Verbatim from the abstract:

> "Our results suggest that despite an almost panmictic population, we can detect two distinct populations of *B. pseudomallei* that conform to biogeographic patterns found in many plant and animal species. That is, **separation along Wallace's Line**, a biogeographic boundary between Southeast Asia and Australia."

> "We describe an **Australian origin** for *B. pseudomallei*, characterized by a **single introduction event into Southeast Asia during a recent glacial period**, and variable levels of lateral gene transfer within populations."

And in the body:

> "*B. pseudomallei* is subdivided into two distinct subpopulations with distinct geographic distributions that are separated by Wallace's Line."

> "It is likely that the most recent common ancestor to *B. pseudomallei* existed on the Australian continent."

**The contingency statement, verbatim:**

> "**The conclusions that we draw are contingent on an Australian root to this tree and not isolate 668 in particular.**"

This is the sentence to quote. The entire Australian-origin edifice — which is then inherited by Sarovich 2016, Chewapreecha 2017, and every review since — rests on where the root is placed on a tree built from 43 genomes. The authors said so themselves in 2009 and, to their credit, said it plainly.

---

## 3. Chewapreecha *et al.* 2017 (Nat Microbiol 2:16263)

**Full citation:** Chewapreecha C, Holden MTG, Vehkala M, Välimäki N, Yang Z, Harris SR, Mather AE, Tuanyok A, De Smet B, Le Hello S, Bizet C, Mayo M, Wuthiekanun V, Limmathurotsakul D, Phetsouvanh R, Spratt BG, Corander J, Keim P, Dougan G, Dance DAB, Currie BJ, Parkhill J, Peacock SJ. "Global and regional dissemination and evolution of *Burkholderia pseudomallei*." *Nat Microbiol* 2017;2:16263. PMID **28112723**, PMCID **PMC5300093**, DOI **10.1038/nmicrobiol.2016.263**.

### 3.1 Abstract (verbatim, in full)

> "The environmental bacterium *Burkholderia pseudomallei* causes an estimated 165,000 cases of human melioidosis per year worldwide, and is also classified as a biothreat agent. We used whole genome sequences of **469 *B. pseudomallei* isolates from 30 countries collected over 79 years** to explore its geographic transmission. Our data point to **Australia as an early reservoir, with transmission to Southeast Asia followed by onward transmission to South Asia, and East Asia.** Repeated reintroduction was observed within the Malay Peninsula, and between countries bordered by the Mekong river. Our data support an **African origin of the Central and South American isolates with introduction of *B. pseudomallei* into the Americas between 1650 and 1850**, providing a temporal link with the slave trade. We also identified geographically distinct genes/variants in Australasian or Southeast Asian isolates alone, with virulence-associated genes being among those overrepresented. This provides a potential explanation for clinical manifestations of melioidosis that are geographically restricted."

### 3.2 SNPs and core genome

Verbatim:

> "variants were identified at **324,637 SNPs** (range 5,650 to 43,221 sites per isolate)"

Mapping reference: the two chromosomes of *B. pseudomallei* K96243 (7.2 Mb, 6,332 predicted CDS in the reference).

Recombination handling, verbatim: *"Recombination fragments were called and removed from the alignment using Gubbins."* **No r/m ratio and no percentage-of-genome-recombinant figure is reported in the main text** — repeated targeted queries returned nothing quantitative. If the manuscript needs a genome-wide recombination statistic for this dataset, it is not in this paper; use Seng 2024 (§4.1) or Nandi 2015 (§9.2) instead and say so.

### 3.3 The 19 clusters

Verbatim:

> "This resulted in **19 groups** for subsequent lineage-specific analyses"

> "We then estimated a timeline... by identifying and analysing **19 separate Bayesian clusters**"

Method, verbatim:

> "Except for the Australasian cluster (Group 1), which contained the highest amount of diversity for each isolate and could not be further sub-clustered, we continued the hierarchical clustering until the diversity observed in secondary or tertiary clusters **fell within the limit of recombination detection**."

That last clause is worth flagging: the cluster definition is explicitly bounded by the resolution of recombination detection, i.e. the clustering granularity is set by a methodological limit, not by a biological one. Clustering method: hierarchical Bayesian clustering (hierBAPS).

### 3.4 Direction of spread

Australia → Southeast Asia → (South Asia, East Asia). Also: repeated reintroduction within the Malay Peninsula, and between Mekong-bordering countries. **No numeric statistical support (e.g. posterior probability, BF) for the directionality was recoverable from the accessible text** — mark **UNVERIFIED** if the manuscript wants to state a support value.

### 3.5 African root of the American isolates, and dating

Verbatim:

> "The most recent common ancestor for the American isolates was estimated to be **1806 or 1759 based on either chromosome I or II, respectively (combined 95% highest posterior density (HPD) interval of both chromosomes, 1682–1849)**."

> "Dating of Asian clusters showed that recent common ancestors could be defined for **three Malaysian-Singaporean clusters and one Thai–Laos cluster, all of which dated to the 20th century**."

**The species-wide TMRCA is NOT reported.** Verbatim explanation:

> "The most recent common ancestor of other Asian and Australasian clusters is very likely to pre-date these estimates, but **dating of these deeper evolutionary events is less reliable**."

This is a material limitation and directly relevant to any manuscript claim about the depth of the geographic signal: the Australia→Asia split itself is **undated** in the definitive global study.

**Substitution / clock rate: UNVERIFIED.** The only accessible statement is the qualitative one:

> "our clock rate on each chromosome for the clusters estimated by BEAST is consistent with previous estimates in *Burkholderia* species"

Three independent targeted extractions failed to return a numeric substitutions-per-site-per-year value with HPD for chromosome I or chromosome II. **What is missing:** the numeric clock rate (per chromosome, with 95% HPD) — most likely present in the Supplementary Information or a Methods table not in the PMC author-manuscript HTML. If the manuscript needs it, obtain the Nature Microbiology PDF + Supplementary directly.

Also verbatim, on model selection: *"Stepping-stone and path-sampling analyses did not show appreciable differences between clock models."*

### 3.6 Accessory genome and gene discovery in Australasia

Verbatim:

> "We identified a total of **25,812 predicted coding sequences (CDS)**, with **4,064 and 21,748 genes assigned to the core (present in 99% of isolates), and accessory (variably present) genome**, respectively"

> "Isolates from Australasia had longer phylogenetic branches compared to isolates from other regions, indicative of greater genetic diversity"

> "This was also observed from the pan-genome analysis, which confirmed that the **Australasian *B. pseudomallei* population had the highest rate of new gene discovery** [and the largest accessory genome]"

Region-specific loci, verbatim:

> "**468 and 14 loci that were specific to the Australasian and Southeast Asian population, respectively**"

Functional enrichment, verbatim:

> "Functional enrichment analyses highlighted elevated frequencies of the terms... and 'defense mechanisms' among region-specific genes compared to random expectation from a reference genome (one-sided Fisher test p-value < 2.2 × 10⁻¹⁶, < 2.2 × 10⁻¹⁶, 1.86 × 10⁻¹⁰ and 9.07 × 10⁻¹⁰ respectively"

**The numeric gene-discovery rate (new genes per additional genome) for Australasia vs Southeast Asia is NOT stated in the accessible text — UNVERIFIED.** What is missing: the fitted Heaps'-law exponent or a "N new genes per genome" figure per region. The qualitative claim ("highest rate of new gene discovery" in Australasia) and the 468 vs 14 region-specific loci asymmetry are both solid and quotable; the rate itself is not.

For context, a species-level (not region-level) gene-discovery rate does exist in the literature: Spring-Pearson 2015 (§9.3) reports "**On average, the addition of the 37th genome added 136 genes to the pangenome**." Do not present that as Chewapreecha's Australasian figure — different paper, different quantity, different sample.

### 3.7 The authors' own sampling caveats

Verbatim:

> "A very limited number of isolates had been stored and were available in areas where melioidosis is either uncommon or under-reported based on lack of microbiology infrastructure, which resulted in an **unequal geographic representation**."

> "Due to a small sample size used for each estimated cluster... Ranks of the true signals ranged from 34th... to 97th..., suggesting that **noise had an effect on a small dataset**."

This is the single most important caveat to carry into a Background section arguing for recombination-aware, sampling-aware inference. The canonical global phylogeography of this species rests on 469 genomes with acknowledged unequal geographic representation, an undated deep split, and an explicit note that noise affected small per-cluster datasets.

---

## 4. Later large-scale studies

### 4.1 Seng *et al.* 2024 — northeast Thailand, 1,391 genomes

**Full citation:** Seng R, Chomkatekaew C, Tandhavanant S, Saiprom N, Phunpang R, Thaipadungpanit J, Batty EM, Day NPJ, Chantratita W, West TE, Thomson NR, Parkhill J, Chewapreecha C, Chantratita N. "Genetic diversity, determinants, and dissemination of *Burkholderia pseudomallei* lineages implicated in melioidosis in Northeast Thailand." *Nat Commun* 2024;15:5699. PMID **38972886**, PMCID **PMC11228029**, DOI **10.1038/s41467-024-50067-9**.

Abstract, verbatim (key sentence):

> "we conduct a comprehensive genomic analysis of **1,391 *B. pseudomallei* isolates collected from nine hospitals in northeast Thailand between 2015 and 2018**, and contemporaneous isolates from neighbouring countries, representing the **most densely sampled collection to date**. Our study identifies **three dominant lineages**, each with unique gene sets potentially enhancing bacterial fitness in the environment. We find that **recombination drives lineage-specific gene flow**."

Quantitative results:
- Composition: 1,265 clinical isolates from NE Thailand (July 2015 – December 2018) plus 15 clinical and 111 environmental isolates from neighbouring regions.
- Dominant lineages: **Lineage 1 (n = 312), Lineage 2 (n = 297), Lineage 3 (n = 125)** — together **52.8%** of the studied population.
- Core-genome SNP alignment: **77,156 SNPs**.
- **Genome-wide r/m (Gubbins-based): 3.7 (lineage 1), 4.6 (lineage 2), 2.2 (lineage 3).**
- Proportion of genes showing evidence of recombination: **99.5% (lineage 1), 99.9% (lineage 2), 96.6% (lineage 3)**.
- Dating: sub-lineage 1.3 emerged **around 2011 (95% HPD 2000–2014)**.
- Dissemination: consistent dissemination patterns in **14 of 28 provincial pairs**; 8 pairs correlated with terrain-altitude slope between provinces or natural river flow; 3 patterns aligned with northeast monsoon winds.

Authors' caveat, verbatim:

> "anthropogenic activities such as human migration between provinces may also contribute to the observed pattern. However, without access to comprehensive human movement data, this aspect remains challenging to investigate."

**These r/m values (2.2–4.6) are genome-wide, lineage-specific, and Gubbins-derived.** They are the correct comparator for any genome-wide recombination statement, and they are the ones to contrast explicitly with Pearson's per-allele 18–30 (§2.2). The near-universal per-gene recombination (96.6–99.9% of genes) is arguably the more striking figure for a recombination-aware SNP paper: essentially every gene in the core genome carries recombination signal within a lineage.

### 4.2 Wu *et al.* 2026 — southern China / Hainan

**Full citation:** Wu H, Lei Z, Chen S, Wang X, Huang H, Xiang D, Tan W, Chen J, Chen C, Qin M, Wen Q, Lu B. "Genomic landscape and phylogenetic insights of *Burkholderia pseudomallei* over two decades in southern China and its global surveillance." *Emerg Microbes Infect* 2026;15(1):2691358. PMID **42377320**, DOI **10.1080/22221751.2026.2691358**. **No PMCID.**

Abstract, verbatim (relevant portions):

> "Herein, performed a retrospective analysis of **554 culture-confirmed melioidosis cases in southern China from 2003 to 2022**. Genomic characteristics and their relationship with antimicrobial susceptibility and clinical characteristics were analyzed *via* whole genome sequencing. **Core-genome SNP phylogenies were constructed from recombination-masked alignments** and compared them with **3,573 publicly available global *B. pseudomallei* genomes** to define their population structure and phylogeographic patterns."

> "Furthermore, global phylogenomic analysis identified **10 evolutionary clusters**; Chinese isolates were significantly **enriched in Cluster 1, a clade shared with Thai strains**, and were phylogenetically **distinct from Cluster 5, as predominantly composed of Australian isolates**."

> "The genomic analysis highlighted substantial regional and global genetic diversity, and **phylogeographic structuring** of *B. pseudomallei*, underscoring the importance of continued genomic surveillance."

Clinical figures from the abstract: male predominance 86.8% (481/554); 57.7% aged 45–64; bacteraemia OR = 5.91 (p < 0.001), diabetes OR = 2.27 (p = 0.008), pulmonary infection OR = 2.26 (p = 0.005) as mortality risk factors; imipenem susceptibility 100%, ceftazidime 99.6%.

**UNVERIFIED — core genome alignment length of 3,805,619 bp.** The number does not appear in the abstract and I could not reach the full text: `tandfonline.com` returned HTTP 403 and there is no PMC deposit. **What is missing:** access to the full text (or supplementary) to confirm the core alignment length, the total SNP count, the number of STs, and whether all 554 cases yielded sequenced genomes (the abstract says 554 *cases*, and does not state a genome count). Do not print 3,805,619 bp without obtaining the PDF.

Note this paper explicitly uses **recombination-masked** core-genome SNP phylogenies — directly supportive of the manuscript's methodological premise.

### 4.3 Norris *et al.* 2026 — North Central Vietnam

**Full citation:** Norris MH, Au La TH, Metrailer MC, Viet Nguyen H, Thi Le Tran Q, Jiranantasak T, Minh Luong T, Bluhm AP, Ngoc Do B, Thu Ha Hoang T, Hoa Luong M, Hai Pham T, Nguyen Hai Bui L, Thi Thu Nguyen H, Thi Pham H, Thanh Trinh T, Blackburn JK. "Expanding the molecular epidemiology of melioidosis in North Central Vietnam." *PLoS Negl Trop Dis* 2026;20(2):e0013945. PMID **41662344**, PMCID **PMC12900444**, DOI **10.1371/journal.pntd.0013945**.

- **47 isolates** newly characterised from Ha Tinh province: 35 clinical, 10 soil, 1 swine, 1 bear. Clinical isolates from 2020; environmental samples from 2016 and 2022.
- **15 STs**, four of them novel among the clinical isolates.
- Global context set: **1,468 *B. pseudomallei* strains from Australia and Southeast Asia, including the 47 from this work** — verbatim: *"Whole genome SNP analysis of 1,468 B. pseudomallei strains from Australia and Southeast Asia, including the 47 from this work"*. **See §0(a): 1,468 is the comparison set, not the study's own sequencing.**
- Fine-scale phylogeography, verbatim: a cgMLST minimum spanning tree *"showed a phylogeographic correlation among genetically related strains and their geographic location of isolation from the southeast to the northwest of the study area"*.
- ST41 dominant; recovered from soil ~1 year after the clinical isolates, evidencing environmental persistence.

This is a useful supporting citation for **within-country, sub-provincial phylogeographic correlation** — but note it rests on a single study with 47 isolates from one province.

### 4.4 Darwin Prospective Melioidosis Study (DPMS)

**Full citation:** Currie BJ, Mayo M, Ward LM, Kaestli M, Meumann EM, Webb JR, Woerle C, Baird RW, Price RN, Marshall CS, Ralph AP, Spencer E, Davies J, Huffam SE, Janson S, Lynar S, Markey P, Krause VL, Anstey NM. "The Darwin Prospective Melioidosis Study: a 30-year prospective, observational investigation." *Lancet Infect Dis* 2021;21(12):1737–1746. PMID **34303419**, DOI **10.1016/s1473-3099(21)00022-0**. **No PMCID (paywalled).**

Verbatim from the abstract:

> "There were **1148 individuals with culture-confirmed melioidosis**, of whom 133 (12%) died."

> "Median annual incidence was **20·5 cases per 100 000 people**; the highest annual incidence in Indigenous Australians was **103·6 per 100 000 in 2011–12**."

> "**Genotyping of *B pseudomallei* confirmed case clusters linked to environmental sources and defined evolving and new sequence types.**"

> "**Genotyping of *B pseudomallei* informs evolving local and global epidemiology.**"

Also: 80% of infections in the wet season (November–April); mortality fell to 6% (17/278) over the final 5 years; 45% of patients had diabetes.

DPMS is the platform behind Meumann 2021 (ST562, §1.5), Webb 2022 (§5.2), Rachlin 2020 (§4.5) and Rachlin 2019 (§5.4). Cite it as the cohort, and cite the individual genomic papers for the genomic claims.

The most-cited review synthesising this body of work is Meumann EM, Limmathurotsakul D, Dunachie SJ, Wiersinga WJ, Currie BJ. "*Burkholderia pseudomallei* and melioidosis." *Nat Rev Microbiol* 2024;22:155–169. PMID **37794173**, DOI **10.1038/s41579-023-00972-5**. **No PMCID; paywalled — I could not retrieve any verbatim text.** Cite for framing only; do not attribute quotes to it without obtaining the PDF.

### 4.5 Fine-scale structure within urban Darwin (the "localised clusters" paper)

**Full citation:** Rachlin A, Mayo M, Webb JR, Kleinecke M, Rigas V, Harrington G, Currie BJ, Kaestli M. "Whole-genome sequencing of *Burkholderia pseudomallei* from an urban melioidosis hot spot reveals a fine-scale population structure and localised spatial clustering in the environment." *Sci Rep* 2020;10:5443. PMID **32214186**, PMCID **PMC7096523**, DOI **10.1038/s41598-020-62300-8**.

Abstract, verbatim:

> "While there is a considerable degree of genetic diversity amongst isolates, *B. pseudomallei* has a **robust global biogeographic structure and genetic populations are spatially clustered in the environment**. We examined the distribution and local spread of *B. pseudomallei* in Darwin, Northern Territory, Australia, which has the highest recorded urban incidence of melioidosis globally. We sampled soil and land runoff throughout the city centre and performed whole-genome sequencing (WGS) on *B. pseudomallei* isolates. By combining phylogenetic analyses, Bayesian clustering and spatial hot spot analysis our results demonstrate that **some sequence types (STs) are widespread in the urban Darwin environment, while others are highly spatially clustered over a small geographic scale. This clustering matches the spatial distribution of clinical cases for one ST.**"

- Sampling: **135 environmental soil and water isolates** sequenced, from **42 drains and 45 public park areas** across urban Darwin (12.5°S).
- Verbatim: *"unique genetic populations of *B. pseudomallei* exist on an exceptionally small scale in the environment"*; clustering "over a remarkably restricted geographical area"; three of four common STs showed significant localised clustering by urban region.
- Source-attribution relevance, verbatim: *"Environmental ST-553 clustering around the north-eastern suburbs (Region 3) matched the residence of clinical cases with ST-553"*, suggesting infection occurred "at or near their residential address".

**Important nuance for the manuscript:** the paper's own finding is heterogeneous — *some* STs are geographically restricted at sub-city scale, *others* are widespread across the city. Any general claim that "genotype predicts exposure location at fine scale" is not supported; the honest statement is that fine-scale spatial clustering exists for a subset of lineages.

### 4.6 North Queensland, Australia

**Full citation:** Gassiep I, Chatfield MD, Permana B, *et al.* "The Genomic Epidemiology of Clinical *Burkholderia pseudomallei* Isolates in North Queensland, Australia." *Pathogens* 2024;13(7):584. PMID **39057811**, PMCID **PMC11279585**, DOI **10.3390/pathogens13070584**.

Verbatim from the abstract:

> "*Burkholderia pseudomallei*, the causative agent of melioidosis, is **highly genetically recombinant, resulting in significant genomic diversity**."

> "**Fifty-nine distinct sequence types (STs) were identified from the 128 clinical isolates.** Six STs comprised 64/128 (50%) isolates. **Novel STs accounted for 38/59 (64%) STs**, with ST TSV-13 as the most prevalent (n = 7), and were less likely to possess an LPS A genotype or YLF gene cluster (*p* < 0.001). These isolates were **most likely to be found outside the inner city (aOR: 4.0, 95% CI: 1.7–9.0, *p* = 0.001)**. ST TSV-13 was associated with increased mortality (aOR: 6.1, 95% CI: 1.2–30.9, *p* = 0.03)."

> "An emerging novel ST appears to have an **association with geographic location and mortality**."

Note: 64% novel STs in a well-studied endemic country is itself a strong statement about how far MLST is from saturation.

### 4.7 Hainan island population genomics (earlier study)

**Full citation:** Zheng H, *et al.* "Genetic diversity and transmission patterns of *Burkholderia pseudomallei* on Hainan island, China, revealed by a population genomics analysis." *Microb Genom* 2021;7(11). PMID **34762026**, PMCID **PMC8743561**, DOI **10.1099/mgen.0.000659**.
**122 genomes** from Hainan (2002–2018), **nine phylogenetic groups**, evidence of **multiple importation events from Southeast Asia** and recent between-city transmission on the island. *(Abstract-level extraction; not independently verbatim-verified beyond the abstract.)*

### 4.8 Malaysia, Singapore, South Asia, Africa, the Americas

**Malaysia.** ST data show limited overlap between Peninsular Malaysia and Malaysian Borneo, with region-restricted STs (e.g. ST658 in Sarawak; ST289 across six Peninsular states). **This came from a search-result synthesis, not a verbatim primary-source extraction — mark UNVERIFIED and retrieve the primary Malaysian MLST/genomics papers before citing.** The relevant primary candidates are the *Microb Genom* whole-genome comparative analysis of Malaysian clinical isolates (DOI 10.1099/mgen.0.000527) and *PLoS Negl Trop Dis* 2020 MLST study (DOI 10.1371/journal.pntd.0008979).

**Singapore / restricted Asian locale.** Nandi *et al.* 2015 (§9.2) sequenced 106 clinical, animal and environmental strains "from a restricted Asian locale" — the deepest single-locale genomic study of recombination structure in the species.

**Bangladesh / South Asia.** Jilani MSA, Farook S, Bhattacharjee A, Barai L, Ahsan CR, Haq JA, Tuanyok A. "Phylogeographic characterization of *Burkholderia pseudomallei* isolated from Bangladesh." *PLoS Negl Trop Dis* 2023;17(12):e0011823. DOI 10.1371/journal.pntd.0011823. **22 isolates** (20 clinical, 2 soil), **12 STs** including four novel. Verbatim: *"STs 1005, 1007 and 56 were the most widespread STs frequently isolated in Bangladesh."* Predominant Bangladeshi STs *"share more genetic similarities with Southeast Asian strains rather than South Asian isolates."* Authors' own caveat, verbatim: *"MLST is not very much efficient in detecting relatedness among *B. pseudomallei* ST due to high levels of lateral gene transfer"*, recommending whole-genome SNP typing instead. **PMID not confirmed — UNVERIFIED.**

**Sri Lanka.** A *PLoS Negl Trop Dis* 2021 study (PMID 34851950) reports **43 STs including 22 novel**, eBURST yielding four groups, a large clonal group with 46 STs plus 17 singletons, STs shared with India/Bangladesh/Cambodia, and describes Sri Lankan isolates as intermediate between Southeast Asia and Oceania. **Extracted from search-result synthesis only — UNVERIFIED; retrieve the primary paper before citing any of these numbers.**

**Africa.** Two primary sources:

*(i)* Sarovich DS, Garin B, De Smet B, Kaestli M, Mayo M, Vandamme P, Jacobs J, Lompo P, Tahita MC, Tinto H, Djaomalaza I, Currie BJ, Renaud F. "Phylogenomic Analysis Reveals an Asian Origin for African *Burkholderia pseudomallei* and Further Supports Melioidosis Endemicity in Africa." *mSphere* 2016;1(2):e00089-15. PMID **27303718**, PMCID **PMC4863585**, DOI **10.1128/msphere.00089-15**. Abstract, verbatim:

> "***B. pseudomallei* first emerged in Australia, with subsequent rare dissemination event(s) to Southeast Asia**; however, its dispersal to other regions is not yet well understood. We used large-scale comparative genomics to investigate the origins of **three *B. pseudomallei* isolates from Madagascar and two from Burkina Faso**. Phylogenomic reconstruction demonstrates that these African *B. pseudomallei* isolates **group into a single novel clade that resides within the more ancestral Asian clade**. Intriguingly, **South American strains reside within the African clade**, suggesting more recent dissemination from West Africa to the Americas. Anthropogenic factors likely assisted in *B. pseudomallei* dissemination to Africa, possibly during **migration of the Austronesian peoples from Indonesian Borneo to Madagascar ~2,000 years ago**, with subsequent genetic diversity driven by mutation and recombination."

*(ii)* Schully KL, Voegtly LJ, Rice GK, *et al.* "Phylogenetic and phenotypic characterization of *Burkholderia pseudomallei* isolates from Ghana reveals a novel sequence type and common phenotypes." *Front Microbiol* 2024;15:1401259. DOI 10.3389/fmicb.2024.1401259. **PMID not confirmed — UNVERIFIED.** Verbatim: *"Twenty-one isolates were subjected to whole genome sequencing and found to represent three discrete sequence types (ST), one of which was novel, and designated ST2058."* Ghanaian isolates grouped within "a clade associated with isolates from the Americas" and in "a sub-clade that includes isolates from Ghana-neighboring Burkina Faso."

**The Americas.** Gee JE, Gulvik CA, Elrod MG, Batra D, Rowe LA, Sheth M, Hoffmaster AR. "Phylogeography of *Burkholderia pseudomallei* Isolates, Western Hemisphere." *Emerg Infect Dis* 2017;23(7):1133–1138. PMID **28628442**, PMCID **PMC5512505**, DOI **10.3201/eid2307.161978**. Abstract, verbatim:

> "Analysis indicated that isolates from the Western Hemisphere form a **distinct clade**, which supports the hypothesis that these isolates were derived from a **constricted seeding event from Africa**. **Subclades have been resolved that are associated with specific regions within the Western Hemisphere and suggest that isolates might be correlated geographically with cases of melioidosis.** One isolate associated with a former World War II prisoner of war was believed to represent illness 62 years after exposure in Southeast Asia. However, **analysis suggested the isolate originated in Central or South America**."

### 4.9 Where the literature disagrees

The Australia-origin narrative is consistent across Pearson 2009, Sarovich 2016 and Chewapreecha 2017 — but that consistency is partly inheritance rather than independent replication: Pearson 2009 supplied the Australian root, and Pearson 2009 itself states the conclusion is contingent on that root (§2.5).

On the **route into Africa and the Americas** the two primary papers give different mechanisms and different timescales, and this is a genuine, citable disagreement:

| | Sarovich 2016 (mSphere) | Chewapreecha 2017 (Nat Microbiol) |
|---|---|---|
| Asia → Africa mechanism | Austronesian migration, Borneo → Madagascar | not specified |
| Timing of Asia → Africa | ~2,000 years ago | not dated |
| Africa → Americas | "more recent dissemination from West Africa to the Americas" | introduction **1650–1850** (95% HPD both chromosomes 1682–1849) |
| Africa → Americas mechanism | anthropogenic, unspecified | "temporal link with the **slave trade**" |
| Sample from Africa | **5 isolates** (3 Madagascar, 2 Burkina Faso) | part of the 469-genome global set |

Both agree on the topological claim (African clade nested in Asian clade; American isolates nested in/derived from African). Gee 2017 independently supports "constricted seeding event from Africa" for the Western Hemisphere. But the Africa branch of the story rests, in Sarovich 2016, on **five genomes from two countries** — an extremely thin basis for a continental origin claim, and worth saying so.

---

## 5. Origin-of-exposure attribution: the published use cases

This is the section where the manuscript's motivating use case has actual precedent. Six documented instances, ordered by how much the genome actually resolved.

### 5.1 US multistate aromatherapy spray outbreak, 2021 — product traceback + continental origin inference

**Full citation:** Gee JE, Bower WA, Kunkel A, Petras J, Gettings J, Bye M, Firestone M, Elrod MG, Liu L, Blaney DD, Zaldivar A, Raybern C, Ahmed FS, Honza H, Stonecipher S, O'Sullivan BJ, Lynfield R, Hunter M, Brennan S, Pavlick J, Gabel J, Drenzek C, Geller R, Lee C, Ritter JM, Zaki SR, Gulvik CA, Wilson WW, Beshearse E, Currie BJ, Webb JR, Weiner ZP, Negrón ME, Hoffmaster AR. "Multistate Outbreak of Melioidosis Associated with Imported Aromatherapy Spray." *N Engl J Med* 2022;386(9):861–868. PMID **35235727**, PMCID **PMC10243137**, DOI **10.1056/nejmoa2116130**.

Four geographically dispersed cases (Georgia, Kansas, Minnesota, Texas), none with endemic travel history; two deaths, one a 5-year-old child.

**What the genome gave — two distinct resolutions:**

*(a) Case-to-product linkage (high resolution).* Verbatim:

> "The results of subsequent whole-genome sequencing analysis indicated that the isolate from the spray bottle and those from the four patients were all the **same strain**, which we have named **ATS2021** (i.e., aromatherapy spray 2021)."

*(b) Geographic origin of the strain (low resolution — continental/subcontinental only).* Verbatim:

> "Strain ATS2021 also **clustered with samples of *B. pseudomallei* from South Asia** that are consistent with the origin of the spray — India."

The spray was "imported from India to the United States."

**Critical reading for the manuscript:** the genome resolved the *product* link decisively, but the *geographic* inference was "clusters with South Asian isolates" — a clade-membership statement, not a point estimate of origin, and it was **corroborated by, not independent of, the known import record**. The paper reports **no SNP distances** between the patient isolates and the spray isolate in the main text, and contains **no explicit statement about the resolution limits of the genomic inference**. So this celebrated case study actually demonstrates the ceiling: WGS gave subcontinent-level attribution that was consistent with — and confirmed by — non-genomic supply-chain evidence.

Follow-on: Gee JE, *et al.* "Virulence of *Burkholderia pseudomallei* ATS2021 Unintentionally Imported to United States in Aromatherapy Spray." *Emerg Infect Dis* 2024;30(10). PMID **39320153**, PMCID PMC11431913. *(Metadata from search results — DOI not independently confirmed, UNVERIFIED.)*

### 5.2 Individual human cases linked to targeted environmental sampling, Darwin

**Full citation:** Webb JR, Rachlin A, Rigas V, Mayo M, Currie BJ, Kaestli M. "Genomic Epidemiology Links *Burkholderia pseudomallei* from Individual Human Cases to *B. pseudomallei* from Targeted Environmental Sampling in Northern Australia." *J Clin Microbiol* 2022;60(3):e0164821. PMID **35080450**, PMCID **PMC8925902**, DOI **10.1128/jcm.01648-21**.

Design: environments of **98 melioidosis patients** sampled; **975 environmental samples** (742 soil, 233 water); *B. pseudomallei* recovered at **50 patient sites**; genotype matches between clinical and environmental isolates for **19 patients (19%)** — 11 soil-linked, 8 water-linked.

**What the genome gave:** for **17 of 19** patients the clinical and environmental isolates clustered on a Darwin core-genome SNP phylogeny, separated by **0 to 15 SNPs, median 4 SNPs**. Two patients were excluded by large distances (**1,294** and **152 SNPs**).

Verbatim: *"For this study we found a maximum of 15 SNPs in the 17 case-environment isolate matches for which we inferred a causal transmission."*

So: for ~19% of cases, targeted sampling plus WGS placed the exposure at a specific residential site. For the remaining ~81%, no environmental match was recoverable at all.

### 5.3 Inhalational exposure attributed to air sampling at a residence

**Full citation:** Currie BJ, Price EP, Mayo M, Kaestli M, Theobald V, Harrington I, Harrington G, Sarovich DS. "Use of Whole-Genome Sequencing to Link *Burkholderia pseudomallei* from Air Sampling to Mediastinal Melioidosis, Australia." *Emerg Infect Dis* 2015;21(11):2052–2054. PMID **26488732**, PMCID **PMC4622230**, DOI **10.3201/eid2111.141802**.

Verbatim:

> "Multilocus-sequence typing, completed by using standard methods, confirmed that 2 isolates from each of the positive air and soil samples and the isolate from the patient's blood culture were all **sequence type (ST) 562**."

> "the air isolate (added to the MLST database as MSHR46817) and the 2 soil isolates (MSHR4681 and MSHR4682) obtained from the environment outside the residence of patient 692 were **identical by whole-genome sequencing and differed from the blood culture isolate of patient 692 (MSHR4515) by only 3 SNPs**."

> "These data provide evidence of aerosolization of *Burkholderia pseudomallei* during stormy conditions in an endemic location and **strong circumstantial evidence for inhalation** of *B. pseudomallei*."

**Resolution achieved: 3 SNPs, single residence, and a route-of-infection inference.** This is the highest-resolution published attribution in the species.

### 5.4 Zoo / captive-animal outbreak traceback

**Full citation:** Rachlin A, Shilton C, Webb JR, Mayo M, Kaestli M, Kleinecke M, Rigas V, Benedict S, Gurry I, Currie BJ. "Melioidosis fatalities in captive slender-tailed meerkats (*Suricata suricatta*): combining epidemiology, pathology and whole-genome sequencing supports variable mechanisms of transmission with one health implications." *BMC Vet Res* 2019;15:458. DOI **10.1186/s12917-019-2198-9**. **PMID 31856823 — reported by the fetched page but NOT independently confirmed against Europe PMC; UNVERIFIED.**

Eight fatal melioidosis cases in captive meerkats at a wildlife park in the Darwin region, March 2015 – October 2016. **Two STs involved: ST-36 (seven meerkats) and ST-562 (one)**; environmental soil samples yielded ST-132. The seven ST-36 isolates were near-identical — **"only 22 total orthologous SNP and InDel variants identified"** across all seven, with two cases differing by a single variant and two October cases by five variants.

**What the genome gave:** it resolved the outbreak into two independent introductions plus within-enclosure transmission, but it **did not establish a geographic origin or import source**. This is the honest answer for animal-import tracebacks: the published example resolves transmission structure, not provenance.

### 5.5 Environmental source attribution by cgMLST — the sugarcane field

From Lichtenegger *et al.* 2021 (§8). Verbatim:

> "cgMLST analysis of the clinical isolate and epidemiologically linked environmental strains revealed **seven environmental isolates, which differed from the patient strain in just 3 to 5 alleles**, pinpointing the **sugarcane field** of the patient as the source of infection."

> "Within the patient cluster, we observed environmental isolates that **differed in only 3 to 5 alleles** from the clinical strains, categorizing the sugarcane field as the presumed exposure site."

**Resolution achieved: a specific field, via 3–5 cgMLST allele differences.** Note this is an allele distance in a 4,221-target scheme, not a SNP distance; the two are not interconvertible.

### 5.6 Reassignment of a presumed exposure history — the WWII prisoner-of-war case

From Gee *et al.* 2017 (§4.8). Isolate TX2004, from a Texas resident who had been a prisoner of war in Southeast Asia during WWII, had been interpreted as melioidosis with a **62-year latency** after Pacific-theatre exposure. Verbatim:

> "TX2004 was obtained from a resident of Texas, USA, who had spent time in Southeast Asia during World War II as a prisoner of war"

> "This finding, and the fact that TX2004 is ITS type G, suggests that **TX2004 might not have been acquired by the patient in the Pacific theater during World War II**."

Genomic analysis placed TX2004 in the Western Hemisphere clade. **This is the cleanest published instance of WGS overturning a clinically assumed exposure geography** — precisely the manuscript's use case — and it should probably be the anchor example. But note the resolution: it excluded a hemisphere and assigned a clade; it did not name a country.

### 5.7 Imported / travel-associated case genomics (Europe)

Henczkó J, Tóth Á, Knausz M, Gartner B, Reményi Á, Bíró E, Létay E, Rókusz L, Tóth S, Pályi B, Mag T, Erdősi T, Deézsi-Magyar N, Molnár Z, Kis Z. "Whole Genome Sequencing and Comparative Genomics of the Emerging Pathogen *Burkholderia pseudomallei* Isolated from Two Travel-Related Infections in Hungary." *Pathogens* 2025;14(11):1108. DOI **10.3390/pathogens14111108**. **PMID 41305346 reported by the fetched page — UNVERIFIED against Europe PMC.**

Case 1 (2008, travel to **India**): novel **ST1643**. Case 2 (2019, travel to **Thailand**): **ST1051**. Verbatim: *"Both isolates clustered within the **Asian clade**, confirming an imported origin."*

**Resolution: clade membership (Asian vs Australasian) only.** No SNP distances to nearest references were reported. Again, the ceiling: genomics confirmed "not autochthonous, Asian in origin", which the travel history had already told them.

### 5.8 Summary of what genomes actually deliver for origin attribution

| Use case | Resolution achieved | Independent of prior epi info? |
|---|---|---|
| Air/soil at residence (Currie 2015) | **3 SNPs**, one address, route of infection | Yes — genomics was decisive |
| Sugarcane field (Lichtenegger 2021) | **3–5 cgMLST alleles**, one field | Partly — epi identified candidate sites |
| Case–environment matching (Webb 2022) | **0–15 SNPs (median 4)**, one residential site, for 19% of cases | Partly — targeted sampling was epi-guided |
| Meerkat outbreak (Rachlin 2019) | transmission structure; **no** geographic origin | n/a |
| Aromatherapy spray (Gee 2022) | strain identity across 4 patients + product; **subcontinent** for origin | No — import record supplied "India" |
| Travel cases, Hungary (2025) | **clade** (Asian) only | No — travel history already known |
| POW case TX2004 (Gee 2017) | **hemisphere/clade reassignment**, overturning assumed exposure | **Yes** — genomics contradicted the history |
| Cambodia/Australia homoplasy (De Smet 2015) | **continent correctly identified** where MLST failed | Yes |

The pattern: within an endemic region with dense local environmental sampling, genomes resolve to a specific site at single-digit SNP distances. Across regions, in the absence of local reference panels, genomes resolve to a **clade or continent**, not a country or site. No published study demonstrates country-level origin attribution for a case with no exposure history and no candidate source isolate.

---

## 6. Within-host evolution and relapse versus reinfection

### 6.1 Relapse versus reinfection: the epidemiological baseline

**Full citation:** Maharjan B, Chantratita N, Vesaratchavest M, Cheng A, Wuthiekanun V, Chierakul W, Chaowagul W, Day NPJ, Peacock SJ. "Recurrent melioidosis in patients in northeast Thailand is frequently due to reinfection rather than relapse." *J Clin Microbiol* 2005;43(12):6032–6034. PMID **16333094**, PMCID **PMC1317219**, DOI 10.1128/jcm.43.12.6032-6034.2005 *(DOI inferred from the JCM URL pattern — UNVERIFIED against Europe PMC).*

Abstract, verbatim:

> "Human melioidosis is associated with a high rate of recurrent disease, despite adequate antimicrobial treatment. Here, we define the rate of relapse versus the rate of reinfection in **116 patients with 123 episodes of recurrent melioidosis** who were treated at Sappasithiprasong Hospital in Northeast Thailand between 1986 and 2005."

- Typing: **PFGE with MLST confirmation** (pre-genomic).
- **92 episodes (75%) relapse; 31 episodes (25%) reinfection.**
- **Median time to relapse 228 days (IQR 99.5–608); median time to reinfection 823 days (IQR 453–1,211); P = 0.0001.**
- Within the first year, relapse accounted for **89% (57/64)** of recurrences; after 2 years, only **53% (20/38)**.

This gives the time-based prior that any SNP threshold has to be interpreted against.

### 6.2 Genomic relapse pairs

**Full citation:** Hayden HS, Lim R, Brittnacher MJ, Sims EH, Ramage ER, Fong C, Wu Z, Crist E, Chang J, Zhou Y, Radey M, Rohmer L, Haugen E, Gillett W, Wuthiekanun V, Peacock SJ, Kaul R, Miller SI, Manoil C, Jacobs MA. "Evolution of *Burkholderia pseudomallei* in Recurrent Melioidosis." *PLoS One* 2012;7(5):e36507. DOI **10.1371/journal.pone.0036507**. **PMID 22666360 reported by the publisher page — UNVERIFIED against Europe PMC.**

Abstract, verbatim:

> "we conducted whole-genome comparisons of **clonal primary and relapse *B. pseudomallei* isolates recovered six months to six years apart from four adult Thai patients**. We found differences within each of the four pairs, and some, including a **330 Kb deletion**, affected substantial portions of the genome. Many of the changes were associated with increased antibiotic resistance."

- SNP differences between paired primary/relapse isolates ranged **from zero to eight** point mutations *(the reported "fifteen SNPs identified in the 1710, 1106 and 354 pairs" is a total across three pairs; the internal accounting here was not fully reconciled from the extraction — **treat these SNP figures as needing verification against the PDF**)*.
- Authors' reasoning on excluding reinfection, verbatim: *"It is unlikely that these observed variations were due to reinfection of patients with strains of different genotypes. The paired isolates are unambiguously clonal, and **the chance is very low of infection months or years later by the same clone given the vast diversity of strains found in the environment.**"*

That last sentence is the actual published logic for relapse-versus-reinfection discrimination in this species: **it is not a SNP threshold; it is an argument from environmental strain diversity.** Because the environmental population is so diverse, re-encountering the same clone is improbable, so clonality itself — not a specific SNP cut-off — is the evidence for relapse. This is worth stating explicitly in the manuscript, because it is often mis-cited as if a threshold existed.

### 6.3 Within-host mutation accumulation rates

**(a) Viberg LT, Sarovich DS, Kidd TJ, Geake JB, Bell SC, Currie BJ, Price EP.** "Within-Host Evolution of *Burkholderia pseudomallei* during Chronic Infection of Seven Australasian Cystic Fibrosis Patients." *mBio* 2017;8(2):e00356-17. PMID **28400528**, PMCID **PMC5388805**, DOI **10.1128/mbio.00356-17**.

- **Seven CF patients**, paired isolates collected **~4 to 55 months apart**.
- **The headline rate, verbatim:**

> "Examining only SNPs, this rate was **3.6 SNPs/year (4.9 × 10⁻⁷ substitutions/site/year)**, similar to those determined previously for *B. dolosa* at **2.1 SNPs/year (3.3 × 10⁻⁷ substitutions/site/year)** and for *B. multivorans* at **2.4 SNPs/year (3.6 × 10⁻⁷ substitutions/site/year)**."

- Including all mutation types, the mean across six patients was **6.4 mutations/year**, with patient CF9 an outlier at **24.9 mutations/year**.
- Per-patient totals: CF9 accumulated **112 mutational events over 55 months**; CF8 only **12 mutations over 46 months**.

**This ~50-fold spread between patients (12 vs 112 events over comparable periods; 6.4 vs 24.9 mutations/year) is the strongest single argument against a fixed within-host SNP threshold in this species.** The paper does **not** itself address relapse-versus-reinfection discrimination.

**(b) Price EP, Sarovich DS, Mayo M, Tuanyok A, Drees KP, Kaestli M, Beckstrom-Sternberg SM, Babic-Sternberg JS, Kidd TJ, Bell SC, Keim P, Pearson T, Currie BJ.** "Within-host evolution of *Burkholderia pseudomallei* over a twelve-year chronic carriage infection." *mBio* 2013;4(4):e00388-13. PMID **23860767**, PMCID **PMC3735121**, DOI **10.1128/mbio.00388-13**.

- Three isolates from a single patient (P314): MSHR1043 (July 2000), MSHR1655 (**+37 months**), MSHR6686 (**+139 months**, January 2012).
- Over the 139-month carriage period: **23 SNPs, 14 small indels, and four large chromosomal deletions totalling 285 kb removing 221 genes**.
- Selection signature, verbatim: *"Of 23 point mutations, **78% were nonsynonymous and 43% were predicted to be deleterious to gene function**, demonstrating a strong propensity for positive selection."*
- **No explicit per-year mutation rate is calculated in this paper.** (23 SNPs / 11.6 years ≈ 2 SNPs/year, but that arithmetic is mine, not the paper's — do not attribute it to the authors.)
- Relapse relevance, verbatim: *"In general, there was a better correlation between mutations observed in MSHR6686 and those from chronic infections with other pathogenic species... than from relapsed *B. pseudomallei* infections."*

**(c) Chronic carriage in cystic fibrosis** is documented in both (a) and (b) above; Viberg 2017 is the CF-specific study, reporting antibiotic resistance emergence, genome reduction, and deleterious mutations in genes for virulence, metabolism, environmental survival and cell wall components. Note that (b), the 12-year carriage case, is a **single patient** — a widely cited but n = 1 result.

### 6.4 What this means for the manuscript

Combining §6.1–6.3, the honest summary is:
- Within-host SNP accumulation is roughly **2–7 SNPs/year on average, but varies ~4–10× between patients**, and one CF patient reached 24.9 mutations/year.
- Relapse pairs separated by months to years show **0–8 SNPs**, overlapping completely with the **0–15 SNP** range Webb 2022 used to infer case-to-environment transmission.
- Therefore the same SNP distance is compatible with (i) relapse from a within-host reservoir, (ii) direct acquisition from a matched environmental source, and (iii) two independent acquisitions from a locally clonal environmental population. **A SNP distance alone cannot discriminate these.**
- The published discrimination logic for relapse vs reinfection is **clonality plus environmental diversity plus time-since-primary**, not a threshold.

---

## 7. SNP thresholds and relatedness cut-offs

### 7.1 The published numbers

All from Webb *et al.* 2022 (§5.2), which is the only paper that assembles them explicitly. Verbatim:

> "Previous epidemiological investigations on Australian melioidosis animal and human clusters have used SNP differences ranging from **0 to 5 SNPs for inferring an environmental transmission event**"

(and, per the same passage, **0 SNPs** for identifying human case clusters presumed to share a source where no environmental isolate is available to confirm transmission)

> "For this study we found a **maximum of 15 SNPs** in the 17 case-environment isolate matches for which we inferred a causal transmission."

> "This is concordant with SNP cutoffs established for other clinically relevant bacteria, with **2 to 37 SNP differences** being reported."

Supporting data points from elsewhere in this review:
- **3 SNPs** — patient blood isolate vs air and soil isolates at the same residence (Currie 2015, §5.3).
- **0–15 SNPs, median 4** — the 17 case-environment matches (Webb 2022).
- **152 and 1,294 SNPs** — the two pairs Webb 2022 *excluded* as non-causal.
- **≤22 orthologous SNP+indel variants** across seven meerkats in one ST-36 outbreak (Rachlin 2019, §5.4).
- **1,328 SNPs** between ST-125 and ST-126 in a single point-source outbreak (Sarovich 2017, §1.6iii) — i.e. **a genuine common-source outbreak spanning >1,300 SNPs**.

### 7.2 The explicit warnings

**(a) Webb 2022, verbatim:**

> "However, **WGS and careful genomics are required to avoid overcalling the relatedness** between clinical and environmental isolates of *B. pseudomallei*."

> "**Pairwise genetic differences between the epidemiologically linked isolates (n = 19) did not correlate with time.**"

The paper documents zero-SNP differences in isolate pairs separated by both **18 days and 156 days** — i.e. the molecular clock provides no usable signal at this scale.

**(b) Sarovich 2017, verbatim** — the strongest published caution against reading SNP distance as time:

> "although these STs were closely related on a whole-genome level, they demonstrated **evidence of multiple recombination events that were unlikely to have occurred over the timeframe of the outbreak**"

Recombination imports blocks of divergent sequence in single events. A pair of isolates can acquire hundreds or thousands of apparent SNPs in one recombination event, on a timescale of a single generation. **Any threshold applied to an unmasked SNP alignment in this species is measuring recombination, not time.**

**(c) Aziz 2017, verbatim:** *"MLST can occasionally lead to erroneous conclusions about isolate origin and disease attribution."*

### 7.3 Assessment for the manuscript

- **There is no consensus, validated SNP threshold for *B. pseudomallei*.** The published range spans **0 to 15 SNPs** for "epidemiologically linked", with 0–5 being the earlier convention and 15 the upper bound from the largest systematic study (n = 17 linked pairs). The 2–37 range is borrowed from *other species*, not derived for *B. pseudomallei*.
- **The evidence base is thin.** The 15-SNP upper bound rests on a single study with 17 informative pairs.
- **Recombination breaks threshold logic in both directions.** Upward: recombination inflates distances between genuinely linked isolates (Sarovich 2017 — 1,328 SNPs in one outbreak). Downward: recombination causes ST/PFGE-identical isolates to be tens of thousands of SNPs apart (Aziz 2017 — 21,211 SNPs; Meumann 2021 — 6,252–7,786 SNPs for identical ST562). Recombination masking reduces but does not eliminate this (Meumann 2021: 6,252–7,786 → 964–1,453 SNPs, still ~1,000).
- **No paper in this review states a fixed threshold is appropriate.** Webb 2022 comes closest to an explicit warning ("avoid overcalling"), and its stated requirement is *"a combination of epidemiology and phylogenetic analysis including closely related local isolates for context"* — i.e. a **local reference panel**, not a number. That is the defensible position to adopt.

---

## 8. cgMLST and other typing schemes

**Full citation:** Lichtenegger S, Trinh TT, Assig K, Prior K, Harmsen D, Pesl J, Zauner A, Lipp M, Que TA, Mutsam B, Kleinhappl B, Steinmetz I, Wagner GE. "Development and Validation of a *Burkholderia pseudomallei* Core Genome Multilocus Sequence Typing Scheme To Facilitate Molecular Surveillance." *J Clin Microbiol* 2021;59(8):e0009321. PMID **33980649**, PMCID **PMC8373231**, DOI **10.1128/jcm.00093-21**.

Abstract, verbatim (key portions):

> "A soft defined core genome was obtained by **challenging the *B. pseudomallei* reference genome K96243 with 469 environmental and clinical genomes, resulting in 4,221 core and 1,351 accessory targets**. The scheme was **validated with 320 WGS data sets**. We compared our novel typing scheme with single nucleotide polymorphism-based approaches investigating closely and distantly related strains. Finally, we applied our scheme for **tracking the environmental source of a recent infection**. The validation of the scheme detected **>95% good cgMLST target genes in 98.4% of the genomes**. Comparison with existing typing methods revealed very good concordance. Our scheme proved to be applicable to investigating not only closely related strains but also **the global *B. pseudomallei* population structure**. We successfully utilized our scheme to identify a **sugarcane field** as the presumable source of a recent melioidosis case."

Scheme construction details:
- Seed genome: **K96243**.
- Core threshold: genes present in **>97%** of the challenge genomes retained as core.
- **4,221 core targets + 1,351 accessory targets.**
- Note the challenge set size — **469 genomes** — is the same number as Chewapreecha 2017's collection; the schemes are built on essentially the global public collection of that era.

Resolution vs 7-locus MLST:
- 468 genomes yielded **211 STs** by conventional MLST.
- 150 global isolates resolved into **148 cgMLST types (Simpson's diversity index 1.00)**.

Geographic signal, verbatim:

> "The cgMLST-based UPGMA tree shows **clustering of global isolates similar to that of a previously constructed global SNP phylogeny** and provides high resolution for closely related isolates on a global level"

Application (also §5.5): environmental isolates differing from the patient strain by **3 to 5 alleles** identified a sugarcane field as the exposure site; the patient's three isolates including a relapse isolate (NA18, blood, relapse) **shared identical allelic profiles** with the primary isolates.

**Two gaps to flag explicitly:**
1. **No allele-distance threshold is proposed.** Targeted searching of the full text for "threshold", "cluster cut-off", "allele difference" returned no numeric cluster definition. The 3–5 allele figure is a *reported observation in one case*, not a validated cut-off. Anyone using "≤5 alleles = linked" is extrapolating beyond what the paper claims.
2. **No explicit statement about recombination's effect on the scheme.** This is a notable omission for the most recombinogenic bacterium yet characterised — allele-based schemes count a recombined gene as one allelic difference regardless of how many nucleotides changed, which arguably *dampens* recombination's distorting effect relative to raw SNP counting. But the paper does not make or test that argument, so it must not be attributed to them.

**Other typing schemes** worth a line: Price EP, *et al.* "Improved multilocus sequence typing of *Burkholderia pseudomallei* and closely related species." *J Med Microbiol* 2016;65:992–997. PMID 27412128, DOI 10.1099/jmm.0.000312 — improved MLST primers. And the ITS type (A/B/G) and YLF/BTFC gene-cluster markers appear throughout the phylogeography literature as coarse geographic markers (e.g. Gee 2017 uses "ITS type G" as corroborating evidence for the Western Hemisphere assignment of TX2004; Gassiep 2024 reports YLF prevalence of 68% in North Queensland vs 79% BTFC in the NT and 98% YLF in Thailand — **these three comparative percentages come from a full-text extraction that was not returned as verbatim quotes; UNVERIFIED**).

---

## 9. How much geographic signal survives recombination — and the published limits of phylogeographic inference

### 9.1 The explicit statement of the problem

**Dale J, Price EP, Hornstra H, Busch JD, Mayo M, Godoy D, Wuthiekanun V, Baker A, Foster JT, Wagner DM, Tuanyok A, Warner J, Spratt BG, Peacock SJ, Currie BJ, Keim P, Pearson T.** "Epidemiological Tracking and Population Assignment of the Non-Clonal Bacterium, *Burkholderia pseudomallei*." *PLoS Negl Trop Dis* 2011;5(12):e1381. DOI **10.1371/journal.pntd.0001381**. **PMID 22163051 reported by the publisher page — UNVERIFIED against Europe PMC.**

This paper is the most direct engagement with the manuscript's core question. Verbatim:

> "**High rates of recombination within the genome of this bacterium have confounded attempts to match clinical samples to geographically defined populations.**"

Abstract, verbatim:

> "Rapid assignment of bacterial pathogens into predefined populations is an important first step for epidemiological tracking. For clonal species, a single allele can theoretically define a population. **For non-clonal species such as *Burkholderia pseudomallei*, however, shared allelic states between distantly related isolates make it more difficult to identify population defining characteristics.**"

Data and results:
- **1,829 isolates from 35 countries**; **664 *B. pseudomallei* STs**; seven MLST loci.
- **"88.3% of STs [were assigned] to either Population 1 or Population 2 with ≥95% probability of assignment."**
- Population 1: **95% Australian** isolates. Population 2: **89% Southeast Asian** isolates.

**The explicit limit, verbatim:**

> "**The seven MLST genes and the current set of STs do not provide enough resolution for further robust differentiation among subpopulations.**"

This is the key quantitative answer to "how much geographic signal survives recombination at MLST resolution": **~88% of STs assign to one of two continental populations with ≥95% confidence, and nothing finer than that two-population split is robustly resolvable from MLST.**

### 9.2 Why geographic signal survives at all — the mechanistic argument

Two mechanisms are proposed in the literature.

**(a) Ecology.** Because melioidosis is acquired from soil or surface water and human-to-human transmission is exceptionally rare, each infection is an independent sample of the local environmental population — there is no transmission chain to homogenise genotypes across geography. *(This framing appears in the Dale 2011 / Rachlin 2020 literature; I did not obtain it as a single verbatim sentence from a primary source, so **treat the specific wording as UNVERIFIED** and re-derive it from Rachlin 2020's "robust global biogeographic structure and genetic populations are spatially clustered in the environment", which IS verbatim.)*

**(b) Restricted gene flow between clades.** Nandi T, Holden MTG, Didelot X, Mehershahi K, Boddey JA, Beacham I, Peak I, Harting J, Baybayan P, Guo Y, Wang S, How LC, Sim B, Essex-Lopresti A, Sarkar-Tyson M, Nelson M, Smither S, Ong C, Aw LT, Hoon CH, Michell S, Studholme DJ, Titball R, Chen SL, Parkhill J, Tan P. "*Burkholderia pseudomallei* sequencing identifies genomic clades with distinct recombination, accessory, and epigenetic profiles." *Genome Res* 2015;25(1):129–141. PMID **25236617**, PMCID **PMC4317168**, DOI **10.1101/gr.177543.114**.

Abstract, verbatim:

> "we performed whole-genome sequencing (WGS) on **106 clinical, animal, and environmental strains from a restricted Asian locale**. Whole-genome phylogenies **resolved multiple genomic clades of Bp, largely congruent with multilocus sequence typing (MLST)**. We discovered **widespread recombination in the Bp core genome, involving hundreds of regions associated with multiple haplotypes**. Highly recombinant regions exhibited functional enrichments that may contribute to virulence. We observed **clade-specific patterns of recombination and accessory gene exchange**, and provide evidence that this is likely due to ongoing recombination between clade members. **Reciprocally, interclade exchanges were rarely observed, suggesting mechanisms restricting gene flow between clades.**"

> "each clade harbored a distinct complement of **restriction-modification (RM) systems**, predicted to cause clade-specific patterns of DNA methylation... **Genomic clades may thus represent functional units of genetic isolation in Bp, modulating intraspecies genetic diversity.**"

This is the mechanistic answer to "how does phylogeographic signal survive the highest r/m in bacteria": **recombination is predominantly intra-clade, and RM systems restrict inter-clade DNA uptake.** Recombination therefore homogenises *within* a geographic population while leaving *between*-population structure largely intact — which is exactly why Φ_PT = 0.117 is significant despite "almost panmictic" MLST data (Pearson 2009).

Caveat on generalising Nandi 2015: 106 strains from a **single restricted Asian locale**. Whether RM-mediated gene-flow restriction holds globally, and specifically across the Wallace's Line divide, has not to my knowledge been tested. This is a single-study result carrying a lot of interpretive weight.

### 9.3 Recombination and genome architecture

Spring-Pearson SM, Stone JK, Doyle A, Allender CJ, Okinaka RT, Mayo M, Broomall SM, Hill JM, Karavis MA, Hubbard KS, Insalaco JM, McNew LA, Rosenzweig CN, Gibbons HS, Currie BJ, Wagner DM, Keim P, Tuanyok A. "Pangenome Analysis of *Burkholderia pseudomallei*: Genome Evolution Preserves Gene Order despite High Recombination Rates." *PLoS One* 2015;10(10):e0140274. DOI **10.1371/journal.pone.0140274**. **PMID 26484663 reported by the publisher page — UNVERIFIED against Europe PMC.**

- **37 isolates** analysed.
- **"the global core genome consists of 4568±16 homologs"**
- **"On average, the addition of the 37th genome added 136 genes to the pangenome"** — i.e. an open pangenome.
- Genomic islands: **~5.8%** of an average genome.
- Verbatim: *"gene order was highly conserved among strains, despite the high recombination rates previously observed"* and *"High rates of gene transfer and recombination are incompatible with retaining gene order unless these processes are either highly localized to specific sites within the genome, or are characterized by symmetrical gene gain and loss"*

The relevance: recombination in this species is **localised and structured**, not uniformly distributed — which is precisely the premise a recombination-aware SNP method exploits.

### 9.4 Published statements on the limits of phylogeographic inference — consolidated

Direct quotes, in descending order of usefulness:

1. Dale 2011: *"High rates of recombination within the genome of this bacterium have confounded attempts to match clinical samples to geographically defined populations."*
2. Dale 2011: *"The seven MLST genes and the current set of STs do not provide enough resolution for further robust differentiation among subpopulations."*
3. Gee 2017: *"Although MLST is the most common method to subtype isolates of B. pseudomallei, over time it has become recognized that it lacks the resolution to firmly link an isolate to a specific geographic origin."*
4. Aziz 2017: *"MLST can occasionally lead to erroneous conclusions about isolate origin and disease attribution. In cases where a shared ST is identified between geographically distant locales, whole-genome sequencing should be used to resolve strain origin."*
5. Pearson 2009: *"The conclusions that we draw are contingent on an Australian root to this tree and not isolate 668 in particular."*
6. Chewapreecha 2017: *"...which resulted in an unequal geographic representation."* and *"...dating of these deeper evolutionary events is less reliable."*
7. Webb 2022: *"WGS and careful genomics are required to avoid overcalling the relatedness between clinical and environmental isolates of B. pseudomallei."*
8. Jilani 2023: *"MLST is not very much efficient in detecting relatedness among B. pseudomallei ST due to high levels of lateral gene transfer."*
9. Sarovich 2017: *"...evidence of multiple recombination events that were unlikely to have occurred over the timeframe of the outbreak."*

**Note the shape of this list:** every explicit "limits of phylogeographic inference" statement in the literature is about **MLST** resolution, or about **SNP-distance overcalling within a region**. I found **no published statement that quantifies the residual uncertainty of whole-genome-based geographic attribution** — e.g. no published misclassification rate for assigning a genome to a country of origin, and no cross-validated accuracy figure at any spatial scale finer than the two-population continental split of Dale 2011 (88.3% of STs at ≥95% probability, which is MLST-based anyway).

**This is a genuine gap in the literature and is likely the strongest justification available for the present manuscript.** State it as such: WGS is repeatedly asserted to "resolve strain origin" (De Smet 2015, Aziz 2017), but the resolution has never been quantified, no confidence measure accompanies published attributions, and the recombination that motivates the whole exercise has never been formally accounted for in an attribution framework.

---

## 10. Errors caught during verification (methodological note)

Recording these because they indicate the failure modes of the retrieval path used here, and because two of them nearly entered this document as facts.

1. **Hallucinated PMID.** A WebFetch of the EID page for Gee 2017 returned "PMID: 28628439". The correct PMID, from the Europe PMC API, is **28628442**. Publisher-page extractions produced a plausible-looking but wrong identifier.
2. **Wrong PMC article returned.** A fetch of PMC4279066, guessed as Nandi 2015, returned a *Pediatrics* paper on neonatal weight loss. The correct PMCID is **PMC4317168**. Never guess PMCIDs.
3. **Conflated studies in a search summary.** A WebSearch response merged Maharjan 2005 (JCM, relapse vs reinfection) with Limmathurotsakul 2006 (CID, risk factors for recurrent melioidosis), attributing the 116-patient/123-episode figures to a single paper. The figures do belong to Maharjan 2005 (confirmed against PMC1317219), but the merge was only detectable by fetching the primary source.
4. **Brief's premises wrong on two counts.** See §0(a) and §0(b).

Consequence: **every PMID/DOI in the citation table below that is marked "verified" was confirmed against the Europe PMC REST API**, not against a publisher page. Those marked UNVERIFIED were taken from publisher pages only and should be re-checked.

---

## 11. Where the literature rests on a single study

Flagging these because the manuscript should not present them as settled:

| Claim | Sole/primary source | Sample size |
|---|---|---|
| Australian origin of *B. pseudomallei* | Pearson 2009 (root-contingent, by its own statement) | 43 genomes |
| African clade nested within Asian clade | Sarovich 2016 | **5 African genomes** (3 Madagascar, 2 Burkina Faso) |
| Introduction to Americas 1650–1850 / slave trade | Chewapreecha 2017 | subset of 469 |
| RM-mediated restriction of interclade gene flow | Nandi 2015 | 106 strains, one Asian locale |
| Upper bound of 15 SNPs for case–environment linkage | Webb 2022 | 17 informative pairs |
| 12-year chronic carriage evolution | Price 2013 | **1 patient**, 3 isolates |
| ST562 introduced to Darwin ≈1988 | Meumann 2021 | 71 Australian + 6 Asian isolates |
| Fine-scale (sub-city) genotype clustering | Rachlin 2020 | 135 environmental isolates, one city |
| cgMLST 3–5 allele environmental source attribution | Lichtenegger 2021 | **1 case** |

---

## 12. Citation table

| Role in the manuscript | Citation | PMID | DOI |
|---|---|---|---|
| MLST scheme origin (7 loci; 128 isolates → 71 STs) | Godoy D, Randle G, Simpson AJ, Aanensen DM, Pitt TL, Kinoshita R, Spratt BG. *J Clin Microbiol* 2003;41(5):2068–2079 | 12734250 ✓ | 10.1128/jcm.41.5.2003.2068-2079 *(as returned: 10.1128/jcm.41.5.2068-2079.2003)* ✓ |
| Australia/Asia split; eBURST CC48 & CC70; no shared ST | Vesaratchavest M, *et al.* *J Clin Microbiol* 2006;44(7):2553–2557 | 16825379 ✓ | 10.1128/jcm.00629-06 ✓ |
| Complete Australia/Thailand ST separation; database provenance artefact | Currie BJ, *et al.* *J Clin Microbiol* 2007;45(11):3828–3829 | 17898162 ✓ | 10.1128/jcm.01590-07 ✓ |
| Φ_PT = 0.117; F_ST 0.03/0.21; per-allele r/m 18–30×; Australian origin & root contingency | Pearson T, *et al.* *BMC Biol* 2009;7:78 | 19922616 ✓ | 10.1186/1741-7007-7-78 ✓ |
| MLST population assignment; recombination confounds geographic matching; 88.3% assignment; resolution limit | Dale J, *et al.* *PLoS Negl Trop Dis* 2011;5(12):e1381 | 22163051 ⚠ | 10.1371/journal.pntd.0001381 ✓ |
| Relapse vs reinfection baseline (75%/25%; 228 vs 823 days) | Maharjan B, *et al.* *J Clin Microbiol* 2005;43(12):6032–6034 | 16333094 ✓ | 10.1128/jcm.43.12.6032-6034.2005 ⚠ |
| Relapse pair genomics (0–8 SNPs; 330 kb deletion); clonality-not-threshold logic | Hayden HS, *et al.* *PLoS One* 2012;7(5):e36507 | 22666360 ⚠ | 10.1371/journal.pone.0036507 ✓ |
| 12-year chronic carriage; 23 SNPs/14 indels/285 kb deleted | Price EP, *et al.* *mBio* 2013;4(4):e00388-13 | 23860767 ✓ | 10.1128/mbio.00388-13 ✓ |
| Within-host rate 3.6 SNPs/yr (4.9×10⁻⁷ subs/site/yr); 6.4 vs 24.9 mut/yr between patients; CF chronic carriage | Viberg LT, *et al.* *mBio* 2017;8(2):e00356-17 | 28400528 ✓ | 10.1128/mbio.00356-17 ✓ |
| Intercontinental ST homoplasy; WGS correctly identified continent | De Smet B, *et al.* *J Clin Microbiol* 2015;53(1):323–326 | 25392354 ✓ | 10.1128/jcm.02574-14 ✓ |
| Intracontinental ST homoplasy; 21,211 and 20,567 SNPs within shared STs | Aziz A, *et al.* *Microb Genom* 2017;3(11):e000139 | 29208140 ✓ | 10.1099/mgen.0.000139 ✓ |
| Non-clonal point-source outbreak; 1,328 SNPs between ST-125/126; recombination outpaces outbreak timeframe | Sarovich DS, *et al.* *Microb Genom* 2017;3(8):e000117 | 29026657 ✓ | 10.1099/mgen.0.000117 ✓ |
| Clade-specific recombination; RM systems restrict interclade gene flow | Nandi T, *et al.* *Genome Res* 2015;25(1):129–141 | 25236617 ✓ | 10.1101/gr.177543.114 ✓ |
| Pangenome; core 4568±16; +136 genes per genome; gene order conserved despite recombination | Spring-Pearson SM, *et al.* *PLoS One* 2015;10(10):e0140274 | 26484663 ⚠ | 10.1371/journal.pone.0140274 ✓ |
| Global phylogeography: 469 genomes, 324,637 SNPs, 19 clusters, Australia→Asia, Americas 1650–1850, sampling caveat | Chewapreecha C, *et al.* *Nat Microbiol* 2017;2:16263 | 28112723 ✓ | 10.1038/nmicrobiol.2016.263 ✓ |
| Asian origin of African isolates; South American strains within African clade; Austronesian route | Sarovich DS, *et al.* *mSphere* 2016;1(2):e00089-15 | 27303718 ✓ | 10.1128/msphere.00089-15 ✓ |
| Western Hemisphere clade; MLST lacks resolution for geographic origin; TX2004 POW reassignment | Gee JE, *et al.* *Emerg Infect Dis* 2017;23(7):1133–1138 | 28628442 ✓ | 10.3201/eid2307.161978 ✓ |
| Aromatherapy spray outbreak; ATS2021; South Asia/India clustering | Gee JE, *et al.* *N Engl J Med* 2022;386(9):861–868 | 35235727 ✓ | 10.1056/nejmoa2116130 ✓ |
| Air sampling → mediastinal melioidosis; 3 SNPs; ST562 | Currie BJ, *et al.* *Emerg Infect Dis* 2015;21(11):2052–2054 | 26488732 ✓ | 10.3201/eid2111.141802 ✓ |
| Case-to-environment linkage; 0–15 SNPs median 4; SNP threshold discussion; "avoid overcalling" | Webb JR, *et al.* *J Clin Microbiol* 2022;60(3):e0164821 | 35080450 ✓ | 10.1128/jcm.01648-21 ✓ |
| Fine-scale spatial clustering in urban Darwin; ST-553 matches case residences | Rachlin A, *et al.* *Sci Rep* 2020;10:5443 | 32214186 ⚠ | 10.1038/s41598-020-62300-8 ✓ |
| Zoo/captive-animal outbreak traceback (meerkats); ≤22 variants across 7 isolates; no geographic origin resolved | Rachlin A, *et al.* *BMC Vet Res* 2019;15:458 | 31856823 ⚠ | 10.1186/s12917-019-2198-9 ⚠ |
| ST562 emergence in Darwin; ≈1988 (95% HPD 1961–2001); 6,252–7,786 SNPs (964–1,453 recombination-masked) to Hainan/Taiwan ST562 | Meumann EM, *et al.* *Emerg Infect Dis* 2021;27(4):1057–1067 | 33754984 ✓ | 10.3201/eid2704.202716 ✓ |
| cgMLST scheme: 4,221 core + 1,351 accessory targets; 469-genome challenge set; sugarcane field attribution at 3–5 alleles | Lichtenegger S, *et al.* *J Clin Microbiol* 2021;59(8):e0009321 | 33980649 ✓ | 10.1128/jcm.00093-21 ✓ |
| DPMS 30-year cohort; 1,148 cases; genotyping informs local and global epidemiology | Currie BJ, *et al.* *Lancet Infect Dis* 2021;21(12):1737–1746 | 34303419 ✓ | 10.1016/s1473-3099(21)00022-0 ✓ |
| Hainan population genomics; 122 genomes; 9 groups; multiple SE Asian importations | Zheng H, *et al.* *Microb Genom* 2021;7(11) | 34762026 ✓ | 10.1099/mgen.0.000659 ✓ |
| NE Thailand 1,391 genomes; 3 dominant lineages; **genome-wide r/m 2.2–4.6**; 77,156 core SNPs; 96.6–99.9% of genes recombinant | Seng R, *et al.* *Nat Commun* 2024;15:5699 | 38972886 ✓ | 10.1038/s41467-024-50067-9 ✓ |
| North Queensland; 128 isolates, 59 STs, 64% novel; geographic association of novel ST | Gassiep I, *et al.* *Pathogens* 2024;13(7):584 | 39057811 ✓ | 10.3390/pathogens13070584 ✓ |
| Southern China 2003–2022; 554 cases; recombination-masked core SNP phylogeny vs 3,573 global genomes; 10 clusters | Wu H, *et al.* *Emerg Microbes Infect* 2026;15(1):2691358 | 42377320 ✓ | 10.1080/22221751.2026.2691358 ✓ |
| North Central Vietnam; **47 new isolates**, 15 STs; 1,468-genome global comparison set; sub-provincial phylogeographic correlation | Norris MH, *et al.* *PLoS Negl Trop Dis* 2026;20(2):e0013945 | 41662344 ✓ | 10.1371/journal.pntd.0013945 ✓ |
| Bangladesh phylogeography; 22 isolates, 12 STs; MLST inefficient due to LGT | Jilani MSA, *et al.* *PLoS Negl Trop Dis* 2023;17(12):e0011823 | ⚠ not confirmed | 10.1371/journal.pntd.0011823 ✓ |
| Ghana; 21 isolates, 3 STs incl. novel ST2058; clusters with Americas/Burkina Faso clade | Schully KL, *et al.* *Front Microbiol* 2024;15:1401259 | ⚠ not confirmed | 10.3389/fmicb.2024.1401259 ⚠ |
| Travel-related imported cases, Hungary; ST1643/ST1051; "clustered within the Asian clade" | Henczkó J, *et al.* *Pathogens* 2025;14(11):1108 | 41305346 ⚠ | 10.3390/pathogens14111108 ✓ |
| General review / framing (paywalled; no verbatim text obtained) | Meumann EM, Limmathurotsakul D, Dunachie SJ, Wiersinga WJ, Currie BJ. *Nat Rev Microbiol* 2024;22:155–169 | 37794173 ✓ | 10.1038/s41579-023-00972-5 ✓ |
| Improved MLST primers | Price EP, *et al.* *J Med Microbiol* 2016;65:992–997 | 27412128 ✓ | 10.1099/jmm.0.000312 ✓ |
| PubMLST *B. pseudomallei* database (2,628 STs; 7,697 isolates; 1,175 genomes; 650,966 alleles) | pubmlst.org/organisms/burkholderia-pseudomallei and rest.pubmlst.org, accessed 2026-09-02 | n/a | n/a |

✓ = PMID/DOI confirmed against the Europe PMC REST API in this session.
⚠ = taken from a publisher page or search result only; **re-verify before submission.**

---

## 13. Outstanding gaps — what still needs to be retrieved

1. **Chewapreecha 2017 clock rate.** Numeric substitutions/site/year with 95% HPD for chromosome I and II. Not in the PMC author manuscript text I could reach. Requires the Nature Microbiology PDF + Supplementary Information.
2. **Chewapreecha 2017 gene-discovery rate.** The numeric rate (new genes per additional genome, or Heaps' α) for Australasian vs Southeast Asian populations. Only the qualitative claim and the 468-vs-14 region-specific loci figure were recoverable.
3. **Wu 2026 core alignment length (3,805,619 bp) and genome count.** Publisher returned HTTP 403; no PMC deposit. Also unconfirmed: total SNP count, number of STs, and whether all 554 cases were sequenced.
4. **Godoy 2003 allele-per-locus statistics.** The "4–15 alleles per locus, mean 8.6" figure was returned by a summarising extraction, not as a verbatim quote. Verify against the PDF.
5. **Hayden 2012 SNP accounting.** The "zero to eight" per-pair range and the "fifteen SNPs identified in the 1710, 1106 and 354 pairs" were not fully reconciled. Verify against the PDF before quoting any specific number.
6. **Malaysia and Sri Lanka population genomics.** All figures in §4.8 for these two countries came from search-result synthesis, not primary extraction. Primary papers to retrieve: *Microb Genom* DOI 10.1099/mgen.0.000527 (Malaysian clinical WGS); *PLoS Negl Trop Dis* DOI 10.1371/journal.pntd.0008979 (Malaysian MLST); PMID 34851950 (Sri Lanka biogeography).
7. **Nat Rev Microbiol 2024 review** — paywalled, no PMC. Needed if the manuscript wants an authoritative synthesis quote on the limits of phylogeographic inference.
8. **YLF/BTFC comparative percentages** (68% NQ / 79% NT / 98% Thailand) from Gassiep 2024 — not returned verbatim.
9. **A quantified accuracy figure for whole-genome geographic attribution.** I could not find one in the literature at any scale finer than Dale 2011's MLST-based two-population assignment. If this genuinely does not exist, it is the manuscript's strongest motivating gap — but the negative claim should be checked with a systematic search before being asserted in print.
