# Background research: *Burkholderia pseudomallei* genome architecture, gene content, and strain-variable molecular determinants

Prepared for the Background section of a recombination-aware SNP manuscript.
Compiled 2026-09-02. Every numeric claim below is tagged with the source it came from. Numbers I could not verify against the primary source are explicitly marked **UNVERIFIED**.

**Tooling note / caveat on provenance.** The PubMed MCP tools and shell `curl` were blocked in this session by a safety classifier, so all retrieval was done with WebSearch and WebFetch against PubMed Central, Europe PMC REST, NCBI E-utilities/Datasets APIs, and publisher sites. Verbatim quotations below were extracted by fetching the full text at the URL given; where a publisher blocked access (e.g. pnas.org returns HTTP 403) I used the PMC mirror of the same article. Quotations are reproduced as returned by the fetch of the primary text; a final proof-read against the PDFs is advisable before they go into a manuscript.

---

## 1. The reference genome K96243 (Holden et al. 2004)

**Citation:** Holden MTG, Titball RW, Peacock SJ, Cerdeño-Tárraga AM, Atkins T, Crossman LC, Pitt T, Churcher C, Mungall K, Bentley SD, Sebaihia M, Thomson NR, Bason N, Beacham IR, Brooks K, Brown KA, Brown NF, Challis GL, Cherevach I, Chillingworth T, Cronin A, Crossett B, Davis P, DeShazer D, Feltwell T, Fraser A, Hance Z, Hauser H, Holroyd S, Jagels K, Keith KE, Maddison M, Moule S, Price C, Quail MA, Rabbinowitsch E, Rutherford K, Sanders M, Simmonds M, Songsivilai S, Stevens K, Tumapa S, Vesaratchavest M, Whitehead S, Yeats C, Barrell BG, Oyston PCF, Parkhill J. *Genomic plasticity of the causative agent of melioidosis, Burkholderia pseudomallei.* Proc Natl Acad Sci USA. 2004;101(39):14240–14245. PMID 15377794. DOI 10.1073/pnas.0403302101. PMC521101.

### 1.1 Replicon structure, sizes, CDS counts, accessions

Verbatim from the paper:

> "The complete genome of *B. pseudomallei* strain K96243 consists of two circular replicons (European Molecular Biology Laboratory accession nos. BX571965 and BX571966) of 4.07 Mb and 3.17 Mb"

> "...that have been designated chromosome 1 and chromosome 2 and encode 3,460 and 2,395 coding sequences (CDSs), respectively"

Summary table (paper values, and the exact base-pair lengths from the deposited records):

| Replicon | Holden 2004 size | Exact length (NCBI) | EMBL/GenBank | RefSeq | CDSs (Holden 2004) |
|---|---|---|---|---|---|
| Chromosome 1 | 4.07 Mb | 4,074,542 bp | BX571965.1 | NC_006350.1 | 3,460 |
| Chromosome 2 | 3.17 Mb | 3,173,005 bp | BX571966.1 | NC_006351.1 | 2,395 |
| Total | 7.25 Mb | 7,247,547 bp | — | — | 5,855 (3,460 + 2,395) |

Exact replicon lengths and total assembly length are from the NCBI Datasets sequence report and assembly report for **GCF_000011545.1 (ASM1154v1)**, the RefSeq assembly of K96243, released 2004-09-16 by the Sanger Institute (https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_000011545.1/). The abstract of Holden 2004 gives the genome as "two chromosomes of 4.07 megabase pairs and 3.17 megabase pairs".

**tRNAs:** "53 are encoded on chromosome 1, and 8 are encoded on chromosome 2." (Holden 2004)

### 1.2 GC content — a caution

**Holden et al. 2004 does not state an overall or per-chromosome G+C percentage anywhere in the text.** I searched the PMC full text specifically for this. The only G+C figures in the paper are per-genomic-island values in Table 1 (range **54.5%–65.4%**), plus the statement:

> "A skew in strand-specific G/C content was seen for both chromosomes, which enabled the prediction of the origins of replication."

The genome-level figure comes from the assembly record, not from Holden:

- **GC content of GCF_000011545.1 = 68%** (NCBI Datasets assembly report; reported rounded to whole percent).
- For comparison, a modern Australian complete genome (MSHR1435) is reported at **"average GC content of 67.9%"** (Sahl et al. 2018, below).

**Per-chromosome GC for K96243 is UNVERIFIED.** Widely quoted values of ~67.7% (chr 1) and ~68.5% (chr 2) could not be traced to a primary source in this session. If you need them, compute them directly from BX571965/BX571966 rather than citing Holden.

### 1.3 Functional division between the two replicons

This is the key architectural claim for a recombination-aware analysis, because it predicts different evolutionary regimes on the two replicons. Verbatim:

> "Chromosome 1 contains a higher proportion of CDSs involved in core functions, such as macromolecule biosynthesis, amino acid metabolism, cofactor and carrier synthesis, nucleotide and protein biosynthesis, chemotaxis, and mobility."

> "Chromosome 2, by contrast, contains a greater proportion of CDSs encoding accessory functions: adaptation to atypical conditions, osmotic protection and iron acquisition, secondary metabolism, regulation, and laterally acquired DNA."

> Chromosome 2 "contains a greater proportion of CDSs with matches to hypothetical proteins or proteins that have no database matches at all."

From the abstract:

> "The large chromosome encodes many of the core functions associated with central metabolism and cell growth, whereas the small chromosome carries more accessory functions associated with adaptation and survival in different niches."

> "Genomic comparisons with closely and more distantly related bacteria revealed a greater level of gene order conservation and a greater number of orthologous genes on the large chromosome, suggesting that the two replicons have distinct evolutionary origins."

**The one hard proportion Holden gives for the replicon split** is the orthology comparison against *Ralstonia solanacearum*:

> "57% of CDSs on chromosome 1 and 25% of CDSs on chromosome 2 have matches."

**Caution for the manuscript:** the "57% vs 25%" figure is a *proportion of CDSs with orthologues in R. solanacearum*, **not** a proportion of core vs accessory genes and **not** a proportion of the *B. pseudomallei* species core. It is frequently paraphrased loosely. Quote it with its comparator attached. I found **no** table in Holden 2004 giving a percentage breakdown of functional classes per replicon; the functional-partitioning claims above are qualitative ("higher proportion", "greater proportion") in the text and are backed by a figure, not by stated percentages. Any numeric functional-class split per replicon you may have seen is **UNVERIFIED** against this paper.

### 1.4 Genomic islands in K96243

Verbatim from the abstract:

> "A striking feature of the genome was the presence of 16 genomic islands (GIs) that together made up 6.1% of the genome."

> "Further analysis revealed these islands to be variably present in a collection of invasive and soil isolates but entirely absent from the clonally related organism *B. mallei*."

> "We propose that variable horizontal gene acquisition by *B. pseudomallei* is an important feature of recent genetic evolution and that this has resulted in a genetically diverse pathogenic species."

From the body:

> "Twelve putative GIs have been identified on chromosome 1, and four have been identified on chromosome 2, each comprising ≈7.6% and ≈4.2% of the DNA of these replicons, respectively"

> "Several of the GIs ... are located next to tRNA genes and are flanked by small repeats"

> "all but one of the islands identified ... are absent in the *B. mallei* genome"

> "Horizontal acquisition of DNA appears to have been intrinsic to the evolution of this organism."

Other K96243 GI facts: at least three of the 16 GIs are prophages or prophage-like (GI 2, GI 3, GI 15); φK96243 is described as an inducible lysogenic phage; tRNA-Phe serves as a prophage attachment site. Table 1 columns are: island name, size (kb), CDS coordinates, integrases, GC (%), function notes; GI G+C ranges 54.5–65.4% against a genome background near 68%, which is the compositional evidence for recent lateral acquisition.

The multiplex-PCR survey underlying "variably present" screened **11 GIs across 40 *B. pseudomallei* isolates (20 clinical, 20 soil)**.

**Note on "6% vs 6.1%":** Holden's abstract says **6.1%**. Tumapa et al. 2008 (same group, see §4) rounds this to "approximately 6% of the genome". Both are citable; prefer 6.1% with Holden.

### 1.5 K96243 reference-sequence quality — relevant to mapping

Wagley S, Scott AE, Ireland PM, Prior JL, Atkins TP, Bancroft GJ, Studholme DJ, Titball RW. *Genome resequencing of laboratory stocks of Burkholderia pseudomallei K96243.* Microbiol Resour Announc. 2019;8(9):e01529-18. PMID 30834386. DOI 10.1128/MRA.01529-18. PMC6395871.

- Up to **42 SNVs** and up to **11 indels** per laboratory culture relative to the 2004 reference; **60 SNVs** and **19 indels** in total across four cultures, indels ranging from 1 nt to **33.7 kb**.
- "At 21 sites, the same SNV was present in all resequenced cultures, suggesting errors in the reference genome." Similarly "At 5 sites, the same indel was present in all resequenced cultures".
- One culture carried a **31.7-kb deletion**.
- Authors' conclusion: "the genetic makeups of laboratory stock cultures of *B. pseudomallei* strain K96243 are not identical", and they recommend labs sequence their own K96243 stocks.

This is a directly useful point for a mapping/SNP-calling manuscript: a small number of apparent reference errors are baked into K96243-based SNP calls.

---

## 2. Other complete reference genomes in use

| Strain | Origin / type | Replicon sizes | Accessions | Assembly | Source |
|---|---|---|---|---|---|
| **K96243** | Asian (Thailand), clinical (human melioidosis) | 4,074,542 / 3,173,005 bp | BX571965 / BX571966 | GCF_000011545.1 | Holden 2004; NCBI |
| **1026b** (UW assembly) | Asian (Thailand), clinical — blood of a patient with septicaemic melioidosis, 1993 | 4,092,668 / 3,138,747 bp (total 7,231,415 bp) | CP002833 / CP002834 (NC_017831 / NC_017832) | GCF_000260515.1 (ASM26051v1, University of Washington, 2012-04-30) | GenBank record; Hayden et al. 2012 |
| **1026b** (LANL assembly) | same strain, independently finished | total 7,237,672 bp | — | GCF_000959125.1 (ASM95912v1, Los Alamos, 2015-03-20) | NCBI; Johnson et al. 2015 |
| **MSHR1153** | **Australian**, **clinical** (human, Australia); a neurologic isolate from the Northern Territory | 4,032,226 / 3,280,677 bp (total 7,312,903 bp) | CP009271 / CP009272 (NZ_CP009271 / NZ_CP009272) | GCF_000770435.1 (ASM77043v1, Los Alamos, submitted 2014-10-31; BioSample SAMN03008919) | GenBank record; Johnson et al. 2015 |
| **MSHR1435** | **Australian**, **environmental** — water bore near the home of a chronic melioidosis patient, Northern Territory, 2002; sequence type ST131; fully virulent | 4,019,555 / 3,258,775 bp; average GC 67.9%; 6,946 coding genes, 4 complete *rrn* operons, 60 tRNAs (PGAP) | CP025264 / CP025265 | — | Sahl et al. 2018 |

**Notes and provenance detail:**

- **1026b.** The GenBank record for CP002833 defines the strain as "isolated from blood of a patient with septicemic melioidosis in Thailand, collected in 1993" and cites Hayden HS, Lim R, Brittnacher MJ, Sims EH, Ramage ER, et al. *Evolution of Burkholderia pseudomallei in recurrent melioidosis.* PLoS ONE. 2012;7(5):e36507. PMID 22615773. DOI 10.1371/journal.pone.0036507. 1026b is the workhorse strain of the Schweizer laboratory's antimicrobial-resistance genetics (see §6). Note there are **two independent complete assemblies of 1026b** with different total lengths (7,231,415 vs 7,237,672 bp) — worth stating explicitly if you map to "1026b".
- **MSHR1153.** The GenBank source qualifiers are: strain MSHR1153, isolation source "clinical isolate", host *Homo sapiens*, country Australia. The submission (Los Alamos, 2014-08-26; 269× coverage from Illumina + 454 + PacBio) carries **no linked primary publication**; the umbrella announcement is Johnson SL, et al. *Complete genome sequences for 59 Burkholderia isolates, both pathogenic and near neighbor.* Genome Announc. 2015;3(2):e00159-15. PMID 25931592. DOI 10.1128/genomeA.00159-15. PMC4417688. MSHR1153 is now the standard **Australian** mapping reference (e.g. it is the reference used for Illumina read mapping in the NT LPS-genotype work of Kaestli et al. 2019, PMID 31348781). It is described in the literature as a neurologic (CNS-disease) NT isolate; the precise clinical annotation is not in the GenBank record, so **cite a paper that uses it rather than the record itself** if you need the "neurologic" descriptor. Treat "MSHR1153 = neurologic isolate" as **partially verified** (asserted in secondary literature, not in the deposited record).
- **MSHR1435** is the correct citation for an *environmental* Australian reference: Sahl JW, Mayo M, Price EP, Sarovich DS, Kaestli M, Pearson T, Williamson CHD, Nottingham R, Sheridan K, Wagner DM, Currie BJ, Keim P. *Complete genome sequence of the environmental Burkholderia pseudomallei sequence type 131 isolate MSHR1435, associated with a chronic melioidosis infection.* Genome Announc. 2018;6(11):e00072-18. PMID 29545292. DOI 10.1128/genomeA.00072-18. PMC5854770. Its value is as the *ancestral* environmental baseline against which clinical isolates from a 17.5-year chronic infection in the same patient show "substantial mutations and deletions indicating attenuated virulence".

**Framing point for the manuscript:** the reference set spans the two main population groups — Asian (K96243, 1026b) and Australian (MSHR1153, MSHR1435) — and both clinical and environmental origins. Because the Australian and Asian populations differ in accessory content (§3, §5), reference choice systematically changes the callable fraction of the genome and biases which accessory loci are even visible.

---

## 3. The pangenome: open vs closed, gene discovery, accessory genome size

### 3.1 Chewapreecha et al. 2017 (the largest global set; the Roary numbers)

**Citation:** Chewapreecha C, Holden MTG, Vehkala M, Välimäki N, Yang Z, Harris SR, Mather AE, Tuanyok A, De Smet B, Le Hello S, Bizet C, Mayo M, Wuthiekanun V, Limmathurotsakul D, Phetsouvanh R, Spratt BG, Corander J, Keim P, Dougan G, Dance DAB, Currie BJ, Parkhill J, Peacock SJ. *Global and regional dissemination and evolution of Burkholderia pseudomallei.* Nat Microbiol. 2017;2:16263. PMID 28112723. DOI 10.1038/nmicrobiol.2016.263. PMC5300093.

Verbatim:

> "We sequenced 276 *B. pseudomallei* isolates cultured from humans with melioidosis or from the environment between 1935 and 2013. These originated from 30 countries across Australasia, Asia, Africa and Central and South America."

Total analysed = **469 isolates** (276 newly sequenced + 193 public).

> "A total of 25,812 predicted coding sequences (CDS), with 4,064 and 21,748 genes assigned to the core (present in 99% of isolates), and accessory (variably present) genome, respectively."

Method: Roary, "BLASTP and sequences clustered using a percentage identity of 92%".

Per-genome content:

> Each assembled genome averaged "5,980 predicted coding sequences" (range **5,701–6,671**), compared with K96243 at **6,332 coding sequences**.

Gene discovery / regional accessory genome:

> "the Australasian *B. pseudomallei* population had the highest rate of new gene discovery and the largest accessory genome"

SNP scale:

> "Variants were identified at 324,637 SNPs (range 5,650 to 43,221 sites per isolate)" when mapping against K96243.

Recombination handling: "Recombination fragments were called and removed from the alignment using Gubbins" prior to phylogenetic reconstruction.

Origin:

> "providing evidence for the hypothesis that Australia was an early reservoir for the current global *B. pseudomallei* population"

**Two cautions.**
1. The paper reports the rarefaction/gene-discovery result qualitatively; **it does not use the word "open" in the main text** as far as I could extract. If you want the explicit "open pangenome" claim, cite Spring-Pearson 2015 (below), which quantifies it.
2. **Per-chromosome clock rates are UNVERIFIED.** The main text says only: "the time calibrated phylogenetic trees, clock rates and time since most recent common ancestor (TMRCA) of estimated clusters are reported in Supplementary Figure 6", and "Clock rates on each chromosome for clusters estimated by BEAST is consistent with previous estimates in *Burkholderia* species". The numeric per-chromosome rates live in **Supplementary Figure 6**, which I could not retrieve. If you want to state a per-replicon clock difference from this paper you must open that supplement.

### 3.2 Spring-Pearson et al. 2015 (the explicit open-pangenome fit)

**Citation:** Spring-Pearson SM, Stone JK, Doyle A, Allender CJ, Okinaka RT, Mayo M, Broomall SM, Hill JM, Karavis MA, Hubbard KS, Insalaco JM, McNew LA, Rosenzweig CN, Gibbons HS, Currie BJ, Wagner DM, Keim P, Tuanyok A. *Pangenome analysis of Burkholderia pseudomallei: genome evolution preserves gene order despite high recombination rates.* PLoS ONE. 2015;10(10):e0140274. PMID 26484663. DOI 10.1371/journal.pone.0140274. PMC4613141.

- **37 isolates** analysed.
- Pangenome = **13,799 homologous groups**.
- Core = **4,568 ± 16** homologous groups (extended core); **2,798 ± 59** (strict core).
- **Open pangenome**, fitted as **N(n) = 809·n^−0.49**, i.e. **≈136 new genes per additional genome sequenced**.
- Genomic islands ≈ **5.8%** of individual genomes.
- Recombination/mutation ratio around **25** in *B. pseudomallei* (as discussed in that paper).
- Model D: **"96% of the genome [has] very low recombination rates but 4% of the genome recombines readily."**
- Gene order highly conserved: mean σ = **0.9765**, i.e. gene-order disruption in only **2.4%** of orthologous gene pairs.
- **"Integration of DNA sequence into the *B. pseudomallei* genome is largely mediated by site-specific recombination at tRNA repeats."**
- **No per-replicon breakdown of recombination or core/accessory content is given** in this paper (it discusses chromosome dosage effects only). **UNVERIFIED** for per-replicon claims.

**This is the single most directly relevant published statement for a recombination-aware SNP paper:** 96%/4% split into a low-recombination background and a readily recombining fraction, plus tRNA-anchored site-specific integration.

### 3.3 Nandi et al. 2015 (recombination in the core genome; clade structure)

**Citation:** Nandi T, Holden MTG, Didelot X, Mehershahi K, Boddey JA, Beacham I, Peak I, Harting J, Baybayan P, Guo Y, Wang S, How LC, Sim B, Essex-Lopresti A, Sarkar-Tyson M, Nelson M, Smither S, Ong C, Aw LT, Hoon CH, Michell S, Studholme DJ, Titball R, Chen SL, Parkhill J, Tan P. *Burkholderia pseudomallei sequencing identifies genomic clades with distinct recombination, accessory, and epigenetic profiles.* Genome Res. 2015;25(1):129–141. PMID 25236617. DOI 10.1101/gr.177543.114. PMC4317168.

- **106 strains** (97 Singapore/Malaysia, 9 Thailand).
- Core genome **5.64 Mb**; a reduced core of **5.6 Mb** excluding mobile elements was used for some analyses.
- **84,846 high-quality SNPs** total; **10,314** lineage (L-)SNPs; **74,532** recombination-associated (R-)SNPs. **≈88% of SNPs are recombination-associated.**
- **2,373 recombination events**, tract lengths **3 bp to 71 kb (median ≈5 kb)**.
- Overall **r/m = 7.2**; clade-specific **r/m = 4.5 (Clade A), 8.5 (Clade B), 6 (Clade C)**.
- **"at least 78% of the BpK96243 reference genome (≈5.67 Mb) has undergone recombination."**
- Accessory: **≈183 kb of novel accessory regions (NAE)** per strain; **at least 2,897 new non-K96243 genes**; pan-genome **"at least 8,802 genes, which is 2× the size of the Bp core genome."**
- **Per-replicon differences (important):** "L-SNPs occurred at a ≈1.2-fold higher frequency on Chr II compared to Chr I"; and "higher recombination levels were observed for Chr II than Chr I."
- Epigenetics: **six unique methylated motifs**; one (5′-CACAG-3′) shared, five strain- or clade-specific.
- Clade-specific recombination and accessory gene exchange, with rare interclade exchange — "Genomic clades may thus represent functional units of genetic isolation."

### 3.4 Sim et al. 2008 — the aCGH figure, and why it needs a health warning

**Citation:** Sim SH, Yu Y, Lin CH, Karuturi RKM, Wuthiekanun V, Tuanyok A, Chua HH, Ong C, Paramalingam SS, Tan G, Tang L, Lau G, Ooi EE, Woods D, Feil E, Peacock SJ, Tan P. *The core and accessory genomes of Burkholderia pseudomallei: implications for human melioidosis.* PLoS Pathog. 2008;4(10):e1000178. PMID 18927621. DOI 10.1371/journal.ppat.1000178. PMC2564834.

- Platform: **array comparative genomic hybridization (aCGH)** against the K96243 gene set.
- **94 strains** — "ninety-four Bp strains isolated from human patients, animals, and environmental soils".
- Core: **"86% of the Bp K96243 genes (4619)"**.
- Accessory: **"14% of the K96243 genome was variably present across the strain panel"**; **"750 out of 5369 genes (14%)"** variably present.
- **"the accessory (variably present) portion of the Bp genome corresponds to ∼14% of the whole genome content"**.

> ⚠️ **FLAG — weak/old provenance.** The "86% core / 14% accessory" figure is a **2008 microarray measurement of gene presence/absence relative to a single reference gene set (K96243), in 94 strains**. It is routinely re-quoted as if it were (a) a modern pangenome estimate, or (b) a base-level "callable fraction" of the genome for read mapping. It is **neither**.
> - It is *gene-level*, not base-level. aCGH cannot resolve partial genes, divergent alleles, small indels, or recombined-but-present sequence.
> - It is *reference-anchored*: it can only detect loss of K96243 genes, never gain of non-K96243 genes. That is why it gives 14% accessory while whole-genome-assembly pangenomics gives a far larger accessory fraction — Chewapreecha 2017 assigns **21,748 of 25,812 genes (84%) to the accessory genome** across 469 isolates, and Nandi 2015 finds **≥2,897 new non-K96243 genes** in only 106 strains.
> - It predates high-throughput sequencing of the species and its 94-strain panel is heavily Thai-weighted.
>
> **Recommendation:** cite Sim 2008 only as the historical first estimate of a large accessory genome, explicitly labelled as aCGH and reference-anchored. Use Chewapreecha 2017 / Spring-Pearson 2015 / Nandi 2015 for any quantitative pangenome statement, and derive your own callable-fraction number from your own alignments rather than reusing 86%.

### 3.5 Pangenome numbers side by side

| Study | n genomes | Method | Pangenome | Core | Accessory | Open? |
|---|---|---|---|---|---|---|
| Sim 2008 | 94 | aCGH vs K96243 | n/a (reference-anchored) | 4,619 genes (86% of K96243) | 750 genes (14%) | not addressed |
| Spring-Pearson 2015 | 37 | assembly-based homolog clustering | 13,799 groups | 4,568 ± 16 (extended); 2,798 ± 59 (strict) | remainder | **Yes**, N(n)=809n^−0.49, ≈136 new genes/genome |
| Nandi 2015 | 106 | assembly + mapping | ≥8,802 genes | 5.64 Mb core; ≈2× core = pangenome | ≥2,897 novel genes; ≈183 kb NAE/strain | implied open |
| Chewapreecha 2017 | 469 | Roary (BLASTP, 92% id) | 25,812 CDS | 4,064 (≥99% of isolates) | 21,748 | highest new-gene discovery in Australasia |

**Note the core-size discrepancy:** Chewapreecha's 4,064 (99% presence, 469 isolates) vs Spring-Pearson's 4,568 (37 isolates) vs Nandi's 5.64 Mb. These are not contradictory — core size shrinks as more, and more diverse, genomes are added, and the definitions differ (99%-presence gene clusters vs homolog groups vs megabases of alignable core). State the definition whenever you quote a core size.

---

## 4. Genomic islands, prophages, ICEs and insertion sequences

### 4.1 Tuanyok et al. 2008 — 71 GIs across five strains

**Citation:** Tuanyok A, Leadem BR, Auerbach RK, Beckstrom-Sternberg SM, Beckstrom-Sternberg JS, Mayo M, Wuthiekanun V, Brettin TS, Nierman WC, Peacock SJ, Currie BJ, Wagner DM, Keim P. *Genomic islands from five strains of Burkholderia pseudomallei.* BMC Genomics. 2008;9:566. PMID 19038032. DOI 10.1186/1471-2164-9-566. PMC2612704.

- **71 distinct GIs** identified across five reference strains: **K96243, 1710b, 1106a, MSHR668, MSHR305**.
- Per-strain counts: **17, 16, 16, 17, 21** respectively.
- **"more than half of the GIs found in that strain were unique to that particular strain."** — i.e. GI content is largely strain-private.
- **Size range: 3.91 kb (GI7.4 in MSHR305) to 107.94 kb (GI6b in 1710b).**
- **40–60% of all GIs were "located adjacent to tRNA genes"**, with associations to tRNA-Met, -Pro, -Arg, -Thr, -Ala, -Ser, -Leu, -Phe, -Cys and -Gly.
- Mechanism: integration involves "the 3′ end sequences of tRNA genes", generating direct repeats; the authors "propose the term 'tRNA-mediated site-specific recombination' (tRNA-SSR) for this mechanism".
- Compositional signal: "dinucleotide signatures 'GC' and 'CG' have the highest frequencies in all GIs regardless of the actual %G+C" — i.e. GIs are detectable by compositional anomaly as well as by structure.
- Multiple GIs are prophages or prophage-like, including GI2, GI6b, GI10.2 and GI8c.
- Conclusion: **"acquisition of GIs is one of the major sources of genomic diversity within *B. pseudomallei*."**

### 4.2 Tumapa et al. 2008 — GI presence/absence across a population, and site re-use

**Citation:** Tumapa S, Holden MTG, Vesaratchavest M, Wuthiekanun V, Limmathurotsakul D, Chierakul W, Feil EJ, Currie BJ, Day NPJ, Nierman WC, Peacock SJ. *Burkholderia pseudomallei genome plasticity associated with genomic island variation.* BMC Genomics. 2008;9:190. PMID 18439288. DOI 10.1186/1471-2164-9-190. PMC2386483.

- **10 whole-genome sequences** compared; **186 Thai isolates** screened by PCR.
- Five K96243 islands used as representatives: **GI 2, 6, 9, 11, 16**.
- **Presence frequency ranges from 12% (GI 9, a prophage-like island) to 76% (GI 16, a metabolic island)** across the 186-isolate population.
- The 16 K96243 GIs comprise **"approximately 6% of the genome."**
- tRNA anchoring, with examples: "GI 11 is inserted at an orthologous site" using an Ala tRNA; "GI 2 is integrated at an alternative tRNA gene" (tRNA-Arg vs tRNA-Phe across strains).
- **Same-site occupancy by different islands:** strain 1655 carries a GI 2-like prophage at a tRNA-Arg site where K96243 instead carries GI 12.

**That last point is the crux for mapping and masking:** the *site* is conserved, the *cargo* is not. Reads from a non-reference island at a conserved tRNA attachment site will either fail to map or will mismap to the reference island occupying the same coordinates, producing dense spurious SNP clusters exactly at tRNA loci.

### 4.3 Insertion sequences

- **K96243 contains only 42 complete or partial IS elements.** Verbatim from Nierman et al. 2004: *"In comparison, the *B. pseudomallei* K96243 genome contains only 42 and the *B. thailandensis* E264 genome contains only 46 complete or partial copies of IS elements."*
- By contrast **B. mallei ATCC 23344 has 171 complete and partial IS elements, ≈3.1% of the genome**, from five families (IS3, IS5, IS110, IS256, ISL3) — see §7.
- ISBma2 insertion into the putative *folA* transcriptional terminator is noted as frequent in *B. pseudomallei* (Podnecky et al. 2013, §6) — an example of an IS insertion with a phenotype.

**Practical implication:** *B. pseudomallei* itself is not IS-rich (42 copies in 7.25 Mb), so IS-driven mismapping is a much smaller problem in *B. pseudomallei* than in *B. mallei*. The dominant repeat/mismapping hazards in *B. pseudomallei* are (i) the tRNA-anchored GI attachment sites, (ii) prophage regions, (iii) the multiple *rrn* operons, and (iv) large paralogous families (e.g. the multiple T3SS and T6SS clusters, and the *fhaB*/filamentous haemagglutinin family). *Explicit published copy-number counts for rrn operons in K96243 are* **UNVERIFIED** *here* — MSHR1435 is annotated with "4 complete *rrn* operons" (Sahl 2018), which is the closest verified figure.

### 4.4 Integrative and conjugative elements (ICEs)

I was **unable to find a *B. pseudomallei*-specific primary paper that formally names and characterises ICEs** in this species during this session. The literature I could verify treats the mobile elements as "genomic islands" carrying integrases and, in some cases, conjugative machinery, rather than as formally designated ICEs. Statements such as "*B. pseudomallei* carries N ICEs" are **UNVERIFIED** and should not be written without a specific source. What *is* verifiable and sufficient for the Background:

- GIs carry integrases (Holden 2004, Table 1 column "Integrases").
- Integration is at tRNA 3′ ends via tRNA-SSR, generating flanking direct repeats (Tuanyok 2008).
- Site-specific recombination at tRNA repeats is the dominant route of DNA integration into the genome (Spring-Pearson 2015).
- *B. pseudomallei* is naturally competent, which provides an additional uptake route (see PLoS ONE 2017;12(12):e0189018, "Burkholderia pseudomallei natural competency and DNA catabolism" — **citation details not fully verified in this session**).

### 4.5 Implications for read mapping and masking (synthesis)

This section is a synthesis of the verified numbers above; each supporting figure carries its own citation.

1. **A large majority of core-genome SNPs are recombinant.** Nandi 2015: 74,532 of 84,846 SNPs (≈88%) were recombination-associated, across 2,373 events with a median tract of ≈5 kb; **≥78% of the K96243 reference (≈5.67 Mb) has been touched by recombination** in a 106-strain regional set. Any phylogeny or dating built from unfiltered SNPs in this species is measuring recombination, not clonal descent.
2. **But recombination is very unevenly distributed.** Spring-Pearson 2015's best model has **96% of the genome recombining at very low rates and 4% recombining readily**. That heterogeneity is what makes recombination-aware masking tractable rather than hopeless.
3. **The recombining fraction is spatially predictable.** It is concentrated in GIs (5.8–6.1% of the genome; Holden 2004, Spring-Pearson 2015) and anchored at tRNA loci (Tuanyok 2008; Spring-Pearson 2015). tRNA-adjacent windows and prophage regions are the highest-value masking targets.
4. **Accessory content is enormous and reference-dependent.** 21,748 accessory genes vs 4,064 core genes across 469 isolates (Chewapreecha 2017); ≥2,897 novel non-K96243 genes in 106 strains (Nandi 2015). Reads from accessory sequence absent from the reference have nowhere correct to map.
5. **The same genomic coordinate can hold different islands in different strains** (Tumapa 2008). This produces false SNP density peaks that look like recombination but are actually alignment artefacts, and it argues for masking by *reference coordinate interval*, not only by post-hoc SNP-density detection.
6. **Per-replicon asymmetry.** Chromosome 2 recombines more and carries more lineage SNPs than chromosome 1 (Nandi 2015: recombination higher on Chr II; L-SNPs ≈1.2-fold higher on Chr II), consistent with Holden's functional partitioning of accessory/laterally-acquired DNA onto chromosome 2. A per-replicon treatment of masking and of clock rate is therefore justified by published data.
7. **Method reference for recombination masking:** Croucher NJ, Page AJ, Connor TR, Delaney AJ, Keane JA, Bentley SD, Parkhill J, Harris SR. *Rapid phylogenetic analysis of large samples of recombinant bacterial whole genome sequences using Gubbins.* Nucleic Acids Res. 2015;43(3):e15. PMID 25414349. DOI 10.1093/nar/gku1196. PMC4330336. Gubbins is what Chewapreecha 2017 used on this species.

---

## 5. Virulence and accessory determinants that vary geographically or between strains

### 5.1 YLF vs BTFC — the flagship geographic polymorphism

**Citation:** Tuanyok A, Auerbach RK, Brettin TS, Bruce DC, Munk AC, Detter JC, Pearson T, Hornstra H, Sermswan RW, Wuthiekanun V, Peacock SJ, Currie BJ, Keim P, Wagner DM. *A horizontal gene transfer event defines two distinct groups within Burkholderia pseudomallei that have dissimilar geographic distributions.* J Bacteriol. 2007;189(24):9044–9049. PMID 17933898. DOI 10.1128/JB.01264-07. PMC2168593.

- Two mutually exclusive gene clusters occupy **the same location on chromosome 2**:
  - **YLF** — *Yersinia*-like fimbrial gene cluster, **BPSS0120 to BPSS0123** in K96243; horizontally acquired.
  - **BTFC** — *B. thailandensis*-like flagellum and chemotaxis gene cluster; the ancestral state; "genes for flagellum biosynthesis and genes for chemotaxis biosynthesis proteins".
- **571 *B. pseudomallei* DNA extracts** screened from areas of endemicity.
- **Australia (n = 231): 88% BTFC (204), 12% YLF (27).**
- **Thailand (n = 310): 2% BTFC (6), 98% YLF (304).**
- **Other countries (n = 30): 7% BTFC, 93% YLF.**
- **All 77 *B. thailandensis* strains tested carried the BTFC-like region** (consistent with BTFC being ancestral).
- ***B. mallei* and *B. cepacia* tested negative for both clusters.**

This is a clean, well-powered, single-locus Asia/Australia marker with an explicit HGT interpretation, and it sits on chromosome 2 — the accessory-enriched replicon.

Chewapreecha 2017's genome-wide association analysis independently recovered BTFC as regionally variable: "The GWAS also identified unappreciated regional variations in well and less well characterised virulence loci", naming specifically the "*Burkholderia thailandensis*-like flagellum and chemotaxis cluster (BTFC), and *Burkholderia mallei*-like *BimA* (*BmBimA*)".

### 5.2 BimA variants and neurological melioidosis

**Citation:** Sarovich DS, Price EP, Webb JR, Ward LM, Voutsinos MY, Tuanyok A, Mayo M, Kaestli M, Currie BJ. *Variable virulence factors in Burkholderia pseudomallei (melioidosis) associated with human disease.* PLoS ONE. 2014;9(3):e91682. PMID 24614774. DOI 10.1371/journal.pone.0091682.

- **556 melioidosis patients** from northern Australia, isolates spanning **24 years**.
- Loci and locus tags (verbatim from the paper):
  - ***bimA*_Bp* = **BPSS1492** in K96243.
  - ***bimA*_Bm* = **BURPS668_A2118** in MSHR668 — the *B. mallei*-like allele.
  - ***fhaB3*** = **BPSS2053** in K96243; a **9.3 kb** gene.
  - YLF marker gene = **BPSS0124**; BTFC marker gene = ***lafU***.
- **Prevalence:** *bimA*_Bm in **"approximately 12% of northern Australian strains"**; the variant **"shares 95% homology with *Burkholderia mallei*"**. *fhaB3* in **83%**. BTFC in **79%**.
- **Association:** patients infected with a *bimA*_Bm strain were **"14 times more likely to present with neurological involvement" (p < 0.001; 95% CI 4.7–44.6)**.
- **Geography:** *bimA*_Bm **"has not yet been observed"** in Thailand, Cambodia, Laos or Vietnam, but **was found in two isolates originating from India**.

**Supporting phenotype/second citation:** Morris JL, Fane A, Sarovich DS, Price EP, Rush CM, Govan BL, Parker E, Mayo M, Currie BJ, Ketheesan N. *Increased neurotropic threat from Burkholderia pseudomallei strains with a B. mallei-like variation in the bimA motility gene, Australia.* Emerg Infect Dis. 2017;23(5):740–749. PMID 28457226. DOI 10.3201/eid2305.151417.
- Compared **7 strains with *bimA*_Bm alleles vs 8 with *bimA*_Bp**, from NT clinical isolates collected October 1989 – October 2012.
- **"Correlation of virulence genes of *B. pseudomallei* with clinical presentations of melioidosis identified the *bimBm* allele as a risk factor for neurologic melioidosis."**
- **"*B. mallei*–like *bimA* variants (*bimBm*) have been identified in a subset of *B. pseudomallei* isolates from Australia and 2 *B. pseudomallei* isolates from India. This allele has not yet been identified in isolates from Southeast Asia."**
- Mouse model: *bimA*_Bm strains showed increased persistence in phagocytic cells, increased virulence, rapid systemic dissemination and replication in brain and spinal cord.

**Note on north Queensland:** a later study (Webb et al., PLoS Negl Trop Dis 2021/2022; PMC9236262) reports that north Queensland clinical isolates carry **diverse *bimA*_Bm genes** associated with CNS disease and are phylogenomically distinct from other Australian strains. I did not fetch its full citation details, so **treat that as UNVERIFIED** pending a lookup.

### 5.3 *fhaB3* and disease presentation

From Sarovich et al. 2014 (same paper, PMID 24614774; DOI 10.1371/journal.pone.0091682):

- ***fhaB3* (BPSS2053, 9.3 kb) present in 83%** of the Australian isolates; **"100% of Thai *B. pseudomallei* strains"** per that paper.
- Patients with *fhaB3*-positive strains were **"twice as likely to be blood culture-positive" (p = 0.028; 95% CI 1.1–3.4)**.
- ***fhaB3*-negative strains were "four times more likely" in cutaneous melioidosis without sepsis (p = 0.001; 95% CI 1.8–8.1)**.

So *fhaB3* stratifies **disease presentation** (bacteraemic/disseminated vs localised cutaneous) rather than geography per se, though its Australia-vs-Thailand prevalence difference (83% vs 100%) means it is partly confounded with geography.

### 5.4 Type III secretion system cluster 3 (T3SS3 / Bsa)

**Citation:** Vander Broek CW, Stevens JM. *Type III secretion in the melioidosis pathogen Burkholderia pseudomallei.* Front Cell Infect Microbiol. 2017;7:255. PMID 28664152. DOI 10.3389/fcimb.2017.00255. PMC5471309.

- *B. pseudomallei* encodes **three T3SSs — T3SS-1, T3SS-2, T3SS-3 — and "all three T3SSs [reside] on chromosome 2."**
- The **Bsa (*Burkholderia* secretion apparatus) T3SS-3 locus spans BPSS1516–BPSS1552.**
- **"T3SS-3 is required for full virulence in both murine and Syrian hamster models of infection."** It is required for efficient endosomal escape.
- **Conservation:** **"T3SS-2 and T3SS-3 are present in the genomes of *B. mallei* and *B. thailandensis*, whereas T3SS-1 is absent from both."**
- Regulatory hierarchy: *bspR* (BPSL1105) → *bprP* (BPSS1553) → *bsaN* (BPSS1546) with chaperone *bicA* (BPSS1533), controlling effectors *bopA*, *bopC*, *bopE*, chaperone *bicP* (BPSS1523) and regulators *bprB–D* (BPSS1520–1522). Needle tip protein **BipD**.

> **Important nuance for a "variable determinants" section:** T3SS3/Bsa is **core, not accessory**, within *B. pseudomallei*, and is shared with *B. mallei* and *B. thailandensis*. It is a determinant of virulence, but it is **not** a source of strain-to-strain presence/absence variation. Do not list it alongside YLF/BTFC or *bimA* as a variable marker. What varies is allelic sequence and expression, not gene content.

### 5.5 Type VI secretion system cluster 5 (T6SS-5 / *tss-5*)

**Citation:** Lennings J, West TE, Schwarz S. *The Burkholderia type VI secretion system 5: composition, regulation and role in virulence.* Front Microbiol. 2019;9:3339. PMID 30687298. DOI 10.3389/fmicb.2018.03339. PMC6335564.

- **"*B. pseudomallei* encodes six type VI secretion systems (T6SSs) and orthologs of five of them are present in *B. thailandensis*."**
- **T6SS-5 is on chromosome 2, locus tags BPSS1493–BPSS1511 in K96243** (adjacent to *bimA*_Bp at BPSS1492 — worth noting, since this is a single accessory-rich neighbourhood on chromosome 2).
- T6SS-5 is required for virulence in mammalian models across *B. pseudomallei*, *B. mallei* and *B. thailandensis*; it mediates host-cell fusion into multinucleated giant cells (MNGCs) and intercellular spread.
- T6SS-1 and T6SS-4 have distinct roles in interbacterial competition and metal-ion acquisition respectively.
- **VgrG-5** is the T6SS-5-exported spike protein required for MNGC formation and virulence; a *vgrG-5* ΔCTD mutant is avirulent in mice and cannot drive cell fusion. (Toesca IJ, French CT, Miller JF. *The type VI secretion system spike protein VgrG5 mediates membrane fusion during intercellular spread by pseudomallei group Burkholderia species.* Infect Immun. 2014;82(4):1445–1452. DOI 10.1128/IAI.01367-13. **PMID not verified in this session.**)

> Same nuance as T3SS3: **T6SS-5 is core within the *pseudomallei* group**, not a variable presence/absence marker.

### 5.6 Capsular polysaccharides

**Citation (CPS I locus):** Cuccui J, Milne TS, Harmer N, George AJ, Bustamante SV, Terentjeva M, Phillips-Jones MK, Prior JL, Beacham IR, Wren BW, Titball RW. *Characterization of the Burkholderia pseudomallei K96243 capsular polysaccharide I coding region.* Infect Immun. 2012;80(3):1209–1221. PMID 22252864. DOI 10.1128/IAI.05805-11. PMC3294636.

- **"There are at least four polysaccharide-encoding gene clusters within the two chromosomes of *B. pseudomallei* K96243."** (CPS I–IV.)
- **CPS I is a 34.5-kb locus on chromosome 1**; "Genes involved in sugar biosynthesis and transport of CPS I are found on chromosome 1"; "the CPS I cluster represents the largest known bacterial locus involved in the biosynthesis and transport of a monomeric repeating sugar unit". Example locus tags cited: BPSL2810 (*manC*), BPSL2801 (*wcbG*).
- CPS I is an unbranched manno-heptopyranose homopolymer.
- **"*Burkholderia pseudomallei* requires CPS I for full virulence, as the production of this polysaccharide contributes to the survival of *B. pseudomallei in vivo* by preventing opsonization and phagocytosis."**

**CPS III:** present in *B. pseudomallei* and *B. thailandensis* but **absent from *B. mallei*** (Reckseidler-Zenteno et al., J Med Microbiol 2010; PMID 20724509; DOI 10.1099/jmm.0.022202-0 — **DOI/PMID pairing verified from search result metadata only, not from full text; treat as needing a final check**).

**CPS as an accessory/HGT trait in near neighbours:** Sim BMQ, Chantratita N, Ooi WF, Nandi T, Tewhey R, Wuthiekanun V, Thaipadungpanit J, Tumapa S, Ariyaratne P, Sung W-K, Sem XH, Chua HH, Ramnarayanan K, Lin CH, Liu Y, Feil EJ, Glass MB, Tan G, Peacock SJ, Tan P. *Genomic acquisition of a capsular polysaccharide virulence cluster by non-pathogenic Burkholderia isolates.* Genome Biol. 2010;11(8):R89. PMID 20799932. DOI 10.1186/gb-2010-11-8-r89. PMC2945791. *B. thailandensis* strain E555 carries a CPS cluster resembling the *B. pseudomallei* one and shows "colony wrinkling, resistance to human complement binding, and intracellular macrophage survival", though **without enhanced virulence in mice**. This is a clean demonstration that a major virulence locus moves horizontally across the species boundary.

### 5.7 LPS O-antigen types A, B, B2 and rough

**Citation:** Tuanyok A, Stone JK, Mayo M, Kaestli M, Gruendike J, Georgia S, Warrington S, Mullins T, Allender CJ, Wagner DM, Chantratita N, Peacock SJ, Currie BJ, Keim P. *The genetic and molecular basis of O-antigenic diversity in Burkholderia pseudomallei lipopolysaccharide.* PLoS Negl Trop Dis. 2012;6(1):e1453. PMID 22235357. DOI 10.1371/journal.pntd.0001453. PMC3250505.

- **Four LPS types: A (typical), B (atypical), B2 (a novel derivative of the atypical type), and rough (no O-antigen ladder).**
- **999 *B. pseudomallei* strains genotyped**: Australia n = 600, Thailand n = 349, other SE Asian sources n = 50.
- **Geographic distribution:**
  - **Genotype A: 97.7% in Southeast Asia; 85.3% in Australia.**
  - **Genotype B: 2.3% in Southeast Asia; 13.8% in Australia.**
  - **Genotype B2: 7 strains total — 5 from Australia, 2 from Papua New Guinea.**
- Conserved genes across the three clusters: **"Genes *wbiGHI*, and *rmlBAC* are conserved among these three different clusters."** Cluster-distinguishing genes include *wbiE*, *wbiI*, *wbiF*, *wbiD*; *oacA* (O-antigen acetylase A, BPSL1936 homolog).
- **Phenotype:** rough-LPS strains **"were unable to grow in the presence of 30% normal human serum"**, whereas typical genotype A strains **"were able to resist the inhibitory human serum effect."**
- **Serology:** "The atypical LPS types (lanes 2 and 3) were seroreactive with the antibody from the LPS genotype B infected patient only", while rough LPS was "seronegative to both sera."
- **The authors' own limitation, quote it:** **"we phenotyped only ∼24% of the isolates that were genotyped"** — so claims about *virulence* differences between LPS types from this paper are weakly powered. Do not over-read them.

> ⚠️ **FLAG:** the widely repeated claim that "LPS type B is less virulent" is **not** established by Tuanyok 2012 at the level often implied. That paper establishes **genotype prevalence** robustly (999 strains) and **serum-resistance/serology** on a ~24% subset. Separate the two claims.

### 5.8 Other published genotype–phenotype / genotype–geography links

- **Chewapreecha 2017 GWAS** found "unappreciated regional variations in well and less well characterised virulence loci", explicitly naming **BTFC** and ***BmBimA*** — an independent, genome-wide confirmation of §5.1 and §5.2 from 469 genomes.
- **Arabinose assimilation operon** — see §7.2. Its *absence* in *B. pseudomallei* (and *B. mallei*) versus presence in *B. thailandensis* is the classic gene-loss-associated-with-virulence example, and it is also the basis of the standard biochemical Ara−/Ara+ discrimination.
- **Aminoglycoside/macrolide susceptibility in Sarawak** (§6.4) is a genotype–geography–phenotype link: an *amrB* mutation restricted to ST881/ST997 explains a regionally distinctive susceptibility phenotype.
- **Genomic islands as clinical/environmental markers:** Nandi et al. and others have proposed GI content differs between clinical and environmental isolates (see "Genomic islands as a marker to differentiate between clinical and environmental *Burkholderia pseudomallei*", PLoS ONE 2012;7(5):e37762, PMC3365882). **Full citation and numbers UNVERIFIED in this session** — fetch before citing.

---

## 6. Intrinsic antimicrobial resistance genetics

**General review:** Rhodes KA, Schweizer HP. *Antibiotic resistance in Burkholderia species.* Drug Resist Updat. 2016;28:82–90. PMID 27620956. DOI 10.1016/j.drup.2016.07.003. PMC5022785.

### 6.1 PenA (BPSS0946 / *penI*) — class A β-lactamase, chromosome 2

- **Locus identity confirmed from NCBI Gene (GeneID 3095241):** gene symbol **penI**, locus tag **BPSS0946** (RefSeq locus tag BPS_RS23870), description **"PenI family class A extended-spectrum beta-lactamase"**, organism *B. pseudomallei* K96243, **chromosome 2, NC_006351.1: 1,248,194–1,249,081**.
- Chirakul S, Norris MH, Pagdepanichkit S, Somprasong N, Randall LB, Shirley JF, Borlee BR, Lomovskaya O, Tuanyok A, Schweizer HP. *Transcriptional and post-transcriptional regulation of PenA β-lactamase in acquired Burkholderia pseudomallei β-lactam resistance.* Sci Rep. 2018;8:10652. PMID 30006637. DOI 10.1038/s41598-018-28843-7. PMC6045580.
  - Confirms **"the *penA* gene is located on chromosome 2."**
  - **Three mechanisms** of acquired β-lactam resistance via PenA: (1) **"acquired CAZ resistance (CAZ^r) by up-regulation of *penA* due to a putative promoter mutation"**; (2) ***penA* gene duplication and amplification**; (3) **"PenA amino acid substitutions that extend the enzyme's substrate spectrum."**

### 6.2 Specific ceftazidime-resistance mutations

Sarovich DS, Price EP, Von Schulze AT, Cook JM, Mayo M, Watson LM, Richardson L, Seymour ML, Tuanyok A, Engelthaler DM, Pearson T, Peacock SJ, Currie BJ, Keim P, Wagner DM. *Characterization of ceftazidime resistance mechanisms in clinical isolates of Burkholderia pseudomallei from Australia.* PLoS ONE. 2012;7(2):e30789. PMID 22359557. DOI 10.1371/journal.pone.0030789. PMC3283585.

- **Nine clinical isolates** from two Australian patients (3 from patient 21, 6 from patient 337) who developed CAZ resistance during therapy.
- Two causal SNPs identified:
  - **G→A transition at position −21 of the *penA* promoter (*penA* −21A)** → overexpression.
  - **Cysteine→tyrosine at position 69 (C69Y)**, nucleotide position 281 (*penA* 281A) → substrate-spectrum change.
- **Deleting *penA* restores susceptibility:** "All Δ*penA* strains possessed a CAZ^S phenotype, with MICs of approximately 1 µg/mL."
- **No amrAB-oprA or bpeEF-oprC involvement** in this study.

Additional reported *penA* mutations: **P167S** (reported in a separate study of CAZ resistance developing during acute infection, PMID 22977307 — **full citation not verified here**); **A172T** plus palindromic GC-rich repeats facilitating *penA* duplication/amplification (2025 work in a Thai collection, PMC12326997 — **full citation not verified here**). Gene duplication and amplification (a reversible ~33-kb GDA involving wild-type *penA*) is documented in a Thai CAZ-resistant clinical isolate (PMID 30639528 — **full citation not verified here**).

### 6.3 Gene loss / deletion as a resistance mechanism

**Citation:** Chantratita N, Rholl DA, Sim B, Wuthiekanun V, Limmathurotsakul D, Amornchai P, Thanwisai A, Chua HH, Ooi WF, Holden MTG, Day NPJ, Tan P, Schweizer HP, Peacock SJ. *Antimicrobial resistance to ceftazidime involving loss of penicillin-binding protein 3 in Burkholderia pseudomallei.* Proc Natl Acad Sci USA. 2011;108(41):17165–17170. PMID 21969582. DOI 10.1073/pnas.1111020108. PMC3193241.

Verbatim from the abstract:

> "Detailed comparisons of the initial ceftazidime-susceptible infecting isolate and subsequent ceftazidime-resistant variants from six patients led us to identify a common, large-scale genomic loss involving a minimum of 49 genes in all six resistant strains."

> "Mutational analysis of wild-type *B. pseudomallei* demonstrated that ceftazidime resistance was due to deletion of a gene encoding a penicillin-binding protein 3 (BPSS1219) present within the region of genomic loss."

> "The clinical ceftazidime-resistant variants failed to grow using commonly used laboratory culture media, including commercial blood cultures, rendering the variants almost undetectable in the diagnostic laboratory."

Related: a natural **>130 kb deletion including the *amrAB-oprA* operon** has been described in *B. pseudomallei*, i.e. loss of an efflux pump by large-scale deletion (reported in the gene-loss-as-resistance literature; PMC3712167, "Bacterial gene loss as a mechanism for gain of antimicrobial resistance" — **full citation UNVERIFIED here**).

**This is directly relevant to a mapping paper:** resistance in this species is frequently caused by *deletions of tens to hundreds of kilobases*, which are invisible to SNP-only pipelines and which also remove reference coordinates from the callable set.

### 6.4 AmrAB-OprA efflux — intrinsic aminoglycoside/macrolide resistance and its regional exception

**Citation:** Podin Y, Sarovich DS, Price EP, Kaestli M, Mayo M, Hii S, Ngian H, Wong S, Wong I, Wong J, Mohan A, Ooi M, Fam T, Wong J, Tuanyok A, Keim P, Giffard PM, Currie BJ. *Burkholderia pseudomallei isolates from Sarawak, Malaysian Borneo, are predominantly susceptible to aminoglycosides and macrolides.* Antimicrob Agents Chemother. 2014;58(1):162–166. PMID 24145517. DOI 10.1128/AAC.01842-13.

- **86% of Sarawak clinical isolates were gentamicin-susceptible** — highly unusual for a species that is intrinsically aminoglycoside-resistant via AmrAB-OprA.
- Susceptibility was **restricted to strains of ST881 or its single-locus variant ST997.**
- Cause: **a novel nonsynonymous mutation in *amrB***, encoding an essential component of the AmrAB-OprA multidrug efflux pump; confirmed by reverting the mutation to wild type.

### 6.5 BpeEF-OprC efflux and folate-pathway inhibitor (TMP-SMX / co-trimoxazole) resistance

**Citation 1:** Podnecky NL, Wuthiekanun V, Peacock SJ, Schweizer HP. *The BpeEF-OprC efflux pump is responsible for widespread trimethoprim resistance in clinical and environmental Burkholderia pseudomallei isolates.* Antimicrob Agents Chemother. 2013;57(9):4381–4386. PMID 23817379. DOI 10.1128/AAC.00660-13. PMC3754293.

Verbatim from the abstract:

> "Here, we demonstrate that trimethoprim resistance is widespread in clinical and environmental isolates from northeast Thailand and northern Australia. This resistance was shown to be due to BpeEF-OprC efflux pump expression. No dihydrofolate reductase target mutations were involved, although frequent insertion of ISBma2 was noted within the putative *folA* transcriptional terminator. All isolates tested remained susceptible to trimethoprim-sulfamethoxazole, suggesting that resistance to trimethoprim alone in these strains probably does not affect the efficacy of co-trimoxazole therapy."

**Citation 2:** Podnecky NL, Rhodes KA, Mima T, Drew HR, Chirakul S, Wuthiekanun V, Schupp JM, Sarovich DS, Currie BJ, Keim P, Schweizer HP. *Mechanisms of resistance to folate pathway inhibitors in Burkholderia pseudomallei: deviation from the norm.* mBio. 2017;8(5):e01357-17. PMID 28874476. DOI 10.1128/mBio.01357-17. PMC5587915.

- Laboratory-acquired trimethoprim resistance: constitutive **BpeEF-OprC** expression from ***bpeT*** mutations; dihydrofolate reductase target mutations are rare.
- **Co-trimoxazole** resistance: **BpeEF-OprC overexpression from *bpeS* mutations** (BpeS DNA-binding or C-terminal effector-binding domain mutations), driving efflux of both trimethoprim and sulfamethoxazole.
- Most laboratory-selected co-trimoxazole-resistant mutants **also carry *folM* mutations** (pterin reductase); both *bpeS* and *folM* mutations contribute.
- ***bpeT*, *bpeS* and *folM* mutations occur in clinical isolates**, so they are clinically significant.
- Authors' conclusion: **"Co-trimoxazole resistance in *B. pseudomallei* is a complex phenomenon, which may explain why resistance to this drug is rare in this bacterium."**

**Within-host emergence (worked examples):** Viberg LT, Sarovich DS, Kidd TJ, Geake JB, Bell SC, Currie BJ, Price EP. *Within-host evolution of Burkholderia pseudomallei during chronic infection of seven Australasian cystic fibrosis patients.* mBio. 2017;8(2):e00356-17. PMID 28400528. DOI 10.1128/mBio.00356-17. PMC5388805.
- ***penA*: C69Y mutation and ~30× duplication** in patient CF6; a **36.7-kb duplication** in CF11.
- ***bpeT*: frameshift at T314** in the later CF6 isolate.
- ***ptr1*: R18-R19-A20 duplication** (CF11), **W116R** substitution (CF9).
- **Deletions:** a **35-kb deletion on chromosome II** in CF8 (nitrate reductase, formate-hydrogen lyase); multiple deletions in CF9 including a **45.5-kb deletion encompassing *mutS*** (a hypermutator).

---

## 7. Relationship to close relatives

### 7.1 *B. mallei* — a clone / deletion derivative of *B. pseudomallei*

**Citation:** Nierman WC, DeShazer D, Kim HS, Tettelin H, Nelson KE, Feldblyum T, Ulrich RL, Ronning CM, Brinkac LM, Daugherty SC, Davidsen TD, DeBoy RT, Dimitrov G, Dodson RJ, Durkin AS, Gwinn ML, Haft DH, Khouri H, Kolonay JF, Madupu R, Mohammoud Y, Nelson WC, Radune D, Romero CM, Sarria S, Selengut J, Shamblin C, Sullivan SA, White O, Yu Y, Zafar N, Zhou L, Fraser CM. *Structural flexibility in the Burkholderia mallei genome.* Proc Natl Acad Sci USA. 2004;101(39):14246–14251. PMID 15377793. DOI 10.1073/pnas.0403306101. PMC521142.

| Metric | *B. mallei* ATCC 23344 | *B. pseudomallei* K96243 |
|---|---|---|
| Total genome | **5.8 Mb** | 7.25 Mb |
| Chromosome 1 | **3,510,148 bp**, 3,344 ORFs | 4,074,542 bp, 3,460 CDS |
| Chromosome 2 | **2,325,379 bp**, 2,091 ORFs | 3,173,005 bp, 2,395 CDS |
| Total protein-coding ORFs | **5,535** | 5,855 |
| Accessions | **CP000010, CP000011** | BX571965, BX571966 |
| IS elements | **171 complete/partial, ≈3.1% of genome** (IS3, IS5, IS110, IS256, ISL3 families) | **42 complete/partial** |

- **Genome size difference: Holden 2004 states the *B. pseudomallei* genome is "1.31 Mb larger" than *B. mallei*.**
- **"627 genes on chromosome 1 and 819 on chromosome 2 of *B. pseudomallei* are either not present or variant in *B. mallei*"** (= 1,446 genes total).
- Shared genes: **">90% identity; average, 99.1%"** over **">90% of the length (average, 99.9%)"**. This near-identity is why *B. mallei* is treated as a clone of *B. pseudomallei* rather than a separate lineage.
- **37 *B. mallei* genes contain frameshifts** relative to *B. pseudomallei* orthologues; **10 genes contain transposon insertions**.
- **15 of the 16 K96243 genomic islands are absent from *B. mallei*** (Holden 2004: "all but one of the islands identified ... are absent in the *B. mallei* genome").
- From the Nierman abstract: **"The genome contains numerous insertion sequence elements that have mediated extensive deletions and rearrangements of the genome relative to *Burkholderia pseudomallei*."** Also **">12,000" simple sequence repeats**, proposed as a mechanism of antigenic variation.
- **"IS elements account for ≈3.1% of the genome in 171 complete and partial IS elements ... In comparison, the *B. pseudomallei* K96243 genome contains only 42 and the *B. thailandensis* E264 genome contains only 46 complete or partial copies of IS elements."**
- The stepwise expansion of **ISBma1, ISBma2 and IS407A** drove deletions and rearrangements, predominantly mediated by **IS407A**. (This is stated in the paper's results/discussion; **the individual per-element copy numbers for ISBma1/ISBma2/IS407A were not recoverable as a verbatim sentence in my extraction — treat individual copy numbers as UNVERIFIED.**)

**Outgroup implication:** *B. mallei* is a *within-species* derivative clade, not an outgroup. Using it as an outgroup for *B. pseudomallei* phylogenetics is phylogenetically incorrect and will produce a rooted tree with *B. mallei* nested inside *B. pseudomallei* diversity. Its 1.4 Mb of missing/variant genes and 171 IS elements also make it a poor mapping comparator.

### 7.2 *B. thailandensis* — avirulent, arabinose-assimilating

**Citation:** Yu Y, Kim HS, Chua HH, Lin CH, Sim SH, Lin D, Derr A, Engels R, DeShazer D, Birren B, Nierman WC, Tan P. *Genomic patterns of pathogen evolution revealed by comparison of Burkholderia pseudomallei, the causative agent of melioidosis, to avirulent Burkholderia thailandensis.* BMC Microbiol. 2006;6:46. PMID 16725056. DOI 10.1186/1471-2180-6-46. PMC1508146.

- ***B. thailandensis* E264: 6.7 Mb total; chromosome 1 = 3.80 Mb / 3,282 CDS; chromosome 2 = 2.9 Mb / 2,363 CDS; 5,645 predicted ORFs.** GenBank **CP000086 and CP000085** (the fetch returned "CP0000865" for the second, which is a transcription artefact — the correct pair is **CP000085 (chr 2) and CP000086 (chr 1)**; **verify before publication**).
- Species-specific genes: *B. pseudomallei* has **484** unique genes on chromosome 1 and **370** on chromosome 2; *B. thailandensis* has **312** and **339** respectively.
- **"Of 368 known and potential virulence genes in Bp, 275 orthologs (71%) are present in Bt at an average similarity of greater than 80%."** — i.e. most *B. pseudomallei* virulence genes are also in the avirulent relative, so virulence is not simply a matter of gene presence.
- ***B. thailandensis* contains "an eight-gene arabinose assimilation operon ... that is absent in Bp."**

**Arabinose and virulence:** Moore RA, Reckseidler-Zenteno S, Kim H, Nierman W, Yu Y, Tuanyok A, Warawa J, DeShazer D, Woods DE. *Contribution of gene loss to the pathogenic evolution of Burkholderia pseudomallei and Burkholderia mallei.* Infect Immun. 2004;72(7):4172–4187. PMID 15213162. DOI 10.1128/IAI.72.7.4172-4187.2004.
- *B. thailandensis* readily uses L-arabinose as sole carbon source; *B. pseudomallei* cannot.
- The **arabinose assimilation operon comprises nine genes** in that analysis, and is **deleted from *B. pseudomallei***; **the deletion was found in all *B. pseudomallei* and *B. mallei* strains investigated.**
- **Restoring the operon in *B. pseudomallei* significantly raised the LD50 in Syrian hamsters** (i.e. made it less virulent), and **microarray showed T3SS genes were down-regulated when cells were grown in L-arabinose.**

> Note the discrepancy: Moore 2004 describes a **nine-gene** operon; Yu 2006 describes an **eight-gene** operon. Both are cited in the literature. If you state a number, attribute it to the specific paper.

### 7.3 *B. oklahomensis*

**Citation:** Glass MB, Steigerwalt AG, Jordan JG, Wilkins PP, Gee JE. *Burkholderia oklahomensis sp. nov., a Burkholderia pseudomallei-like species formerly known as the Oklahoma strain of Pseudomonas pseudomallei.* Int J Syst Evol Microbiol. 2006;56(9):2171–2176. PMID 16957116. DOI 10.1099/ijs.0.63991-0.

- Type strain **C6786^T (= LMG 23618^T = NCTC 13387^T = CCUG 51349^T)**, originally isolated **1973 from a wound infection following a farming accident in Oklahoma, USA**.
- Environmental isolates C7532 and C7533 from the Oklahoma accident site matched C6786; a further clinical isolate originally called *B. pseudomallei* was recovered from a person in Georgia, USA, after an automobile accident.
- Gram-negative, catalase- and oxidase-positive, aerobic, motile.
- It is the most divergent named member of the *B. pseudomallei* complex and is the conventional choice when a genuinely outgroup-like *pseudomallei*-complex taxon is needed. **Its exact ANI to *B. pseudomallei* was not verified in this session — UNVERIFIED.**

### 7.4 *B. humptydooensis*

**Citation:** Tuanyok A, Mayo M, Scholz H, Hall CM, Allender CJ, Kaestli M, Ginther J, Spring-Pearson S, Bollig MC, Stone JK, Settles EW, Busch JD, Sidak-Loftis L, Sahl JW, Thomas A, Kreutzer L, Georgi E, Gee JE, Bowen RA, Ladner JT, Lovett S, Koroleva G, Palacios G, Wagner DM, Currie BJ, Keim P. *Burkholderia humptydooensis sp. nov., a new species related to Burkholderia thailandensis and the fifth member of the Burkholderia pseudomallei complex.* Appl Environ Microbiol. 2017;83(5):e02802-16. PMID 27986727. DOI 10.1128/AEM.02802-16. PMC5311406.

- Type strain **MSMB43^T (= ATCC BAA-2767 = LMG 29471)**, from **an automated water bore (well) in Humpty Doo, Northern Territory, Australia, 1995**. Two further strains from a separate bore ~950 km south, 2007. MLST sequence type **ST318**. Genome ~**7.3 Mb**.
- **"The 16S rRNA gene sequence similarities of *B. humptydooensis* sp. nov. to other members of the *B. pseudomallei* complex (*B. thailandensis*, *B. mallei*, and *B. oklahomensis*) were 99%."**
- **GGDC to related species were less than 70%**, with **"the highest detected similarity being between *B. humptydooensis* sp. nov. and *B. thailandensis* (51.1% [± 3.2%])"**.
- **The *B. pseudomallei* complex thus comprises five species: *B. pseudomallei*, *B. mallei*, *B. thailandensis*, *B. oklahomensis*, *B. humptydooensis*.**

> ⚠️ **CORRECTION of a likely misreading.** The sentence *"Among the three tested B. humptydooensis sp. nov. genomes, the calculated genome-to-genome distance calculation (GGDC) and average nucleotide identity (ANI) values were in the range of 93 to 99% and 98 to 99%, respectively"* refers to comparisons **among the three B. humptydooensis genomes themselves**, NOT to *B. pseudomallei* or *B. thailandensis*. Do not write "*B. humptydooensis* shares 98–99% ANI with *B. pseudomallei*" — that is wrong. **The ANI of *B. humptydooensis* to *B. pseudomallei* / *B. thailandensis* is UNVERIFIED here** (the GGDC/DDH value to *B. thailandensis* is 51.1%, well below the 70% species threshold).

### 7.5 What this means for outgroup choice and species boundaries

- ***B. mallei* is NOT a valid outgroup** — it is a monomorphic, host-restricted, IS-expanded deletion clone nested within *B. pseudomallei* diversity (Nierman 2004; Holden 2004). Rooting a *B. pseudomallei* tree on *B. mallei* is a phylogenetic error.
- ***B. thailandensis* E264 is the standard near-neighbour outgroup**: it is a distinct species, shares 71% of *B. pseudomallei*'s known/potential virulence gene orthologues at >80% similarity (Yu 2006), and is comparably sized (6.7 Mb) with a similar two-replicon architecture and similar IS burden (46 copies).
- ***B. oklahomensis* is more divergent** and is preferable if you need a deeper root, at the cost of a smaller alignable core.
- ***B. humptydooensis* offers a fifth complex member** with GGDC <70% to all others; it is a useful additional outgroup, but published ANI values against *B. pseudomallei* need to be looked up rather than inferred.
- **Species-boundary caveat:** the CPS-cluster acquisition by *B. thailandensis* E555 (Sim BMQ 2010) and the shared BTFC cluster (Tuanyok 2007: all 77 *B. thailandensis* tested carried BTFC) show that virulence-associated loci cross the species boundary. Outgroup contamination of accessory loci is therefore a real risk in any presence/absence analysis, and is another argument for restricting SNP calling to a masked core.

---

## 8. Mutation rate estimates and per-replicon differences

| Setting | Rate | Source |
|---|---|---|
| Within-host, chronic CF infection (6 of 7 patient pairs) | **3.6 SNPs/year = 4.9 × 10⁻⁷ substitutions/site/year** | Viberg 2017, PMID 28400528 |
| Within-host, hypermutator patient CF9 (*mutS* deleted) | **12.9 SNPs/year = 1.8 × 10⁻⁶ substitutions/site/year** | Viberg 2017, PMID 28400528 |
| Within-host, single patient, >16-year chronic infection | **median 1.7 × 10⁻⁷ substitutions/site/year (95% HPD 1.3 × 10⁻⁷ – 2.1 × 10⁻⁷)** | Pearson 2020, PMID 32134991 |
| Global population, per chromosome, BEAST | **"consistent with previous estimates in *Burkholderia* species"; numeric values in Supplementary Fig. 6 only** | Chewapreecha 2017, PMID 28112723 — **numbers UNVERIFIED** |

**Composite range often quoted:** ≈**1.7 – 4.9 × 10⁻⁷ substitutions/site/year** for non-hypermutator *B. pseudomallei*, i.e. roughly **1.2–3.6 SNPs per genome per year** on a 7.25 Mb genome.

**Caveats to state explicitly:**
- These are all **within-host** estimates from chronic human infections. **The environmental (soil/water) substitution rate of *B. pseudomallei* is not known**; the organism spends most of its life cycle as a saprophyte, and there is no reason to assume the within-host clock transfers. Pearson 2020 and the review literature make this point.
- **Hypermutators exist and matter:** the *mutS*-deleted CF9 lineage ran ~3.6× faster. A single hypermutator lineage will distort a dataset-wide clock.
- **Clock-rate assumptions are violated in this species** by the very high recombination rate (r/m = 7.2 overall, up to 8.5 within a clade; ≈88% of SNPs recombination-associated — Nandi 2015). Rate estimates that do not first strip recombination are not measuring mutation.

### Per-replicon differences

**The only verified per-replicon quantitative statements I found:**

- **Nandi et al. 2015:** *"L-SNPs occurred at a ≈1.2-fold higher frequency on Chr II compared to Chr I"* and *"higher recombination levels were observed for Chr II than Chr I."* So chromosome 2 shows **both** a modestly higher lineage-SNP (i.e. mutation-derived) density **and** more recombination.
- **Holden et al. 2004** provides the architectural rationale: chromosome 2 carries the accessory functions and the laterally acquired DNA; chromosome 1 carries core metabolism and shows greater gene-order conservation and more orthologues with related genomes (57% vs 25% CDS matches to *R. solanacearum*).
- **Spring-Pearson et al. 2015** does **not** give a per-replicon recombination breakdown (**UNVERIFIED** for that claim).
- **Chewapreecha et al. 2017** estimated clock rates **per chromosome** but reports them only in Supplementary Figure 6 (**UNVERIFIED numbers**).

**Recommended sentence for the manuscript (fully supportable):** *"The two replicons are not evolutionarily equivalent: chromosome 2 carries the accessory, adaptation-associated and laterally acquired gene content (Holden et al. 2004) and shows both higher recombination and a ~1.2-fold higher lineage-SNP density than chromosome 1 (Nandi et al. 2015)."*

---

## 9. Gaps, unverified items, and provenance warnings — consolidated

**Flagged for weak or misused provenance:**
1. **Sim et al. 2008 "86% core / 14% accessory"** — a 2008 *array CGH* result, gene-level and anchored to K96243, from 94 mostly Thai strains. It is frequently re-quoted as if it were a modern pangenome estimate or a base-level callable fraction. It is neither. Chewapreecha 2017 puts 21,748 of 25,812 genes (84%) in the accessory genome across 469 isolates. See §3.4.
2. **Tuanyok 2012 LPS "virulence" differences** — only ~24% of the 999 genotyped isolates were phenotyped, and the authors say so. The prevalence figures are strong; the virulence inference is weak. See §5.7.
3. **"6% vs 6.1%" of the genome as genomic islands** — Holden 2004 says 6.1%; Tumapa 2008 says ~6%; Spring-Pearson 2015 says ~5.8% of individual genomes. Not contradictory, but pick one and attribute it.
4. **T3SS3/Bsa and T6SS-5 are core, not variable.** They are frequently listed in "variable virulence determinants" sections; they are conserved across the *pseudomallei* group. Only their alleles/expression vary.
5. **"*B. humptydooensis* shares 98–99% ANI with *B. pseudomallei*"** — a misreading of Tuanyok 2017. That range is among the three *B. humptydooensis* genomes. See §7.4.
6. **K96243 reference errors** — 21 SNV sites and 5 indel sites appear in all four resequenced lab cultures, suggesting errors in the 2004 reference (Wagley 2019). Relevant if you report absolute SNP counts against K96243.

**Explicitly UNVERIFIED — do not write without checking:**
- **Per-chromosome G+C for K96243.** Holden 2004 gives no genome or chromosome G+C at all. Only the whole-assembly value (68%, NCBI GCF_000011545.1) and MSHR1435's 67.9% are verified. Compute from BX571965/BX571966 if you need per-replicon values.
- **Any numeric per-replicon functional-class percentage from Holden 2004.** Holden's functional partitioning is stated qualitatively plus one orthology comparison (57%/25% vs *R. solanacearum*).
- **Chewapreecha 2017 per-chromosome clock rates** — Supplementary Figure 6 only; not retrieved.
- **ISBma1 / ISBma2 / IS407A individual copy numbers in *B. mallei*.** The 171 total / 3.1% figure is verified; the per-element breakdown is not.
- **Formal ICE designations in *B. pseudomallei*.** I could not find a primary paper naming *B. pseudomallei* ICEs. Use "genomic islands with integrases, integrating by tRNA-SSR" instead.
- ***B. oklahomensis* ANI to *B. pseudomallei***.
- ***B. thailandensis* E264 accession pair** — almost certainly CP000085/CP000086; the fetched text rendered one as "CP0000865". Verify.
- **rRNA operon count in K96243** (MSHR1435 has 4; K96243 not verified).
- **Secondary citations named but not fully verified:** Reckseidler-Zenteno CPS III (PMID 20724509); Toesca VgrG5 (DOI 10.1128/IAI.01367-13); Webb north Queensland *bimA*_Bm (PMC9236262); *penA* P167S (PMID 22977307); *penA* A172T / GC-rich repeats (PMC12326997); *penA* GDA (PMID 30639528); >130 kb *amrAB-oprA* deletion (PMC3712167); GI clinical/environmental marker paper (PLoS ONE 2012;7(5):e37762, PMC3365882); natural competence (PLoS ONE 2017;12(12):e0189018).

**Topics requested but thin in the retrieved literature:**
- **Prophage counts across strains.** Holden identifies ≥3 prophage/prophage-like GIs in K96243; Tuanyok 2008 identifies several prophage GIs among the 71. A dedicated, current census exists (Frontiers in Bacteriology 2024, "A comprehensive study of prophage islands in *Burkholderia pseudomallei* complex") but I did not fetch and verify it. Worth adding.
- **ICEs** (see above).
- **A modern, base-level callable-fraction figure for *B. pseudomallei* short-read mapping.** No published figure was found. This is arguably a gap your manuscript fills — and it is exactly why the Sim 2008 figure should not be pressed into that role.

---

## 10. Citation table

| Role in the Background | Citation | PMID | DOI |
|---|---|---|---|
| K96243 reference genome; replicon sizes, CDS counts, accessions BX571965/BX571966; functional partitioning; 16 GIs = 6.1% of genome | Holden MTG, et al. Genomic plasticity of the causative agent of melioidosis, *Burkholderia pseudomallei*. Proc Natl Acad Sci USA. 2004;101(39):14240–14245. | 15377794 | 10.1073/pnas.0403302101 |
| K96243 exact replicon lengths (4,074,542 / 3,173,005 bp), total 7,247,547 bp, GC 68% | NCBI Assembly GCF_000011545.1 (ASM1154v1), Sanger Institute, 2004-09-16 | — | — |
| K96243 lab-stock variation and probable reference errors | Wagley S, et al. Genome resequencing of laboratory stocks of *Burkholderia pseudomallei* K96243. Microbiol Resour Announc. 2019;8(9):e01529-18. | 30834386 | 10.1128/MRA.01529-18 |
| 1026b origin (Thai clinical, 1993); CP002833/CP002834 | Hayden HS, et al. Evolution of *Burkholderia pseudomallei* in recurrent melioidosis. PLoS ONE. 2012;7(5):e36507. | 22615773 | 10.1371/journal.pone.0036507 |
| MSHR1153 and second 1026b complete genomes (LANL panel) | Johnson SL, et al. Complete genome sequences for 59 *Burkholderia* isolates, both pathogenic and near neighbor. Genome Announc. 2015;3(2):e00159-15. | 25931592 | 10.1128/genomeA.00159-15 |
| MSHR1435 — Australian environmental ST131 reference; 4,019,555/3,258,775 bp; GC 67.9%; 6,946 genes; CP025264/CP025265 | Sahl JW, et al. Complete genome sequence of the environmental *Burkholderia pseudomallei* sequence type 131 isolate MSHR1435. Genome Announc. 2018;6(11):e00072-18. | 29545292 | 10.1128/genomeA.00072-18 |
| Global pangenome: 469 isolates, 25,812 CDS, 4,064 core / 21,748 accessory; 324,637 SNPs; Australian origin; regional virulence-locus variation | Chewapreecha C, et al. Global and regional dissemination and evolution of *Burkholderia pseudomallei*. Nat Microbiol. 2017;2:16263. | 28112723 | 10.1038/nmicrobiol.2016.263 |
| Open pangenome (N(n)=809n^−0.49; ~136 new genes/genome); core 4,568±16; GIs 5.8%; 96%/4% recombination split; gene order conserved (σ=0.9765) | Spring-Pearson SM, et al. Pangenome analysis of *Burkholderia pseudomallei*. PLoS ONE. 2015;10(10):e0140274. | 26484663 | 10.1371/journal.pone.0140274 |
| Core-genome recombination: 106 genomes, r/m 7.2, 2,373 events, ≥78% of reference recombined, 88% of SNPs recombinant; Chr II > Chr I | Nandi T, et al. *Burkholderia pseudomallei* sequencing identifies genomic clades with distinct recombination, accessory, and epigenetic profiles. Genome Res. 2015;25(1):129–141. | 25236617 | 10.1101/gr.177543.114 |
| aCGH core/accessory (86%/14%, 94 strains) — historical, flag provenance | Sim SH, et al. The core and accessory genomes of *Burkholderia pseudomallei*: implications for human melioidosis. PLoS Pathog. 2008;4(10):e1000178. | 18927621 | 10.1371/journal.ppat.1000178 |
| 71 GIs across 5 strains; 3.91–107.94 kb; 40–60% tRNA-adjacent; tRNA-SSR | Tuanyok A, et al. Genomic islands from five strains of *Burkholderia pseudomallei*. BMC Genomics. 2008;9:566. | 19038032 | 10.1186/1471-2164-9-566 |
| GI presence 12–76% across 186 Thai isolates; different islands at the same tRNA site in different strains | Tumapa S, et al. *Burkholderia pseudomallei* genome plasticity associated with genomic island variation. BMC Genomics. 2008;9:190. | 18439288 | 10.1186/1471-2164-9-190 |
| Recombination-masking method used on this species | Croucher NJ, et al. Rapid phylogenetic analysis of large samples of recombinant bacterial whole genome sequences using Gubbins. Nucleic Acids Res. 2015;43(3):e15. | 25414349 | 10.1093/nar/gku1196 |
| YLF vs BTFC; 571 isolates; Australia 88% BTFC, Thailand 98% YLF; same chr-2 locus, mutually exclusive; BPSS0120–0123 | Tuanyok A, et al. A horizontal gene transfer event defines two distinct groups within *Burkholderia pseudomallei* that have dissimilar geographic distributions. J Bacteriol. 2007;189(24):9044–9049. | 17933898 | 10.1128/JB.01264-07 |
| *bimA*_Bm (BURPS668_A2118) vs *bimA*_Bp (BPSS1492); 12% of NT strains; OR 14 for neurological disease; *fhaB3* (BPSS2053) 83%, OR 2 bacteraemia / 4 cutaneous; BTFC 79%; 556 patients | Sarovich DS, et al. Variable virulence factors in *Burkholderia pseudomallei* (melioidosis) associated with human disease. PLoS ONE. 2014;9(3):e91682. | 24614774 | 10.1371/journal.pone.0091682 |
| *bimA*_Bm neurotropism in vivo; geographic restriction to Australia (+2 Indian isolates) | Morris JL, et al. Increased neurotropic threat from *Burkholderia pseudomallei* strains with a *B. mallei*-like variation in the *bimA* motility gene, Australia. Emerg Infect Dis. 2017;23(5):740–749. | 28457226 | 10.3201/eid2305.151417 |
| LPS O-antigen genotypes A/B/B2/rough; 999 strains; A 97.7% SE Asia vs 85.3% Australia; B 2.3% vs 13.8%; B2 n=7 | Tuanyok A, et al. The genetic and molecular basis of O-antigenic diversity in *Burkholderia pseudomallei* lipopolysaccharide. PLoS Negl Trop Dis. 2012;6(1):e1453. | 22235357 | 10.1371/journal.pntd.0001453 |
| Three T3SSs, all on chromosome 2; Bsa/T3SS-3 = BPSS1516–BPSS1552; required for virulence; conserved in *B. mallei* and *B. thailandensis* | Vander Broek CW, Stevens JM. Type III secretion in the melioidosis pathogen *Burkholderia pseudomallei*. Front Cell Infect Microbiol. 2017;7:255. | 28664152 | 10.3389/fcimb.2017.00255 |
| Six T6SSs; T6SS-5 = BPSS1493–BPSS1511 on chromosome 2; MNGC formation and mammalian virulence | Lennings J, West TE, Schwarz S. The *Burkholderia* type VI secretion system 5. Front Microbiol. 2019;9:3339. | 30687298 | 10.3389/fmicb.2018.03339 |
| ≥4 CPS clusters; CPS I = 34.5 kb on chromosome 1; required for full virulence | Cuccui J, et al. Characterization of the *Burkholderia pseudomallei* K96243 capsular polysaccharide I coding region. Infect Immun. 2012;80(3):1209–1221. | 22252864 | 10.1128/IAI.05805-11 |
| CPS cluster horizontally acquired by non-pathogenic *B. thailandensis* E555 | Sim BMQ, et al. Genomic acquisition of a capsular polysaccharide virulence cluster by non-pathogenic *Burkholderia* isolates. Genome Biol. 2010;11(8):R89. | 20799932 | 10.1186/gb-2010-11-8-r89 |
| PenA regulation: promoter mutation, gene duplication/amplification, substrate-spectrum substitutions; *penA* on chromosome 2 | Chirakul S, et al. Transcriptional and post-transcriptional regulation of PenA β-lactamase in acquired *Burkholderia pseudomallei* β-lactam resistance. Sci Rep. 2018;8:10652. | 30006637 | 10.1038/s41598-018-28843-7 |
| *penA* −21A promoter SNP and C69Y; Δ*penA* restores susceptibility | Sarovich DS, et al. Characterization of ceftazidime resistance mechanisms in clinical isolates of *Burkholderia pseudomallei* from Australia. PLoS ONE. 2012;7(2):e30789. | 22359557 | 10.1371/journal.pone.0030789 |
| Gene loss as resistance: ≥49-gene deletion, PBP3 (BPSS1219) loss → ceftazidime resistance, 6 patients | Chantratita N, et al. Antimicrobial resistance to ceftazidime involving loss of penicillin-binding protein 3 in *Burkholderia pseudomallei*. Proc Natl Acad Sci USA. 2011;108(41):17165–17170. | 21969582 | 10.1073/pnas.1111020108 |
| PenA locus identity: *penI*/BPSS0946, chromosome 2, NC_006351.1:1,248,194–1,249,081 | NCBI Gene GeneID 3095241 | — | — |
| AmrAB-OprA: *amrB* mutation → 86% gentamicin susceptibility in Sarawak ST881/ST997 | Podin Y, et al. *Burkholderia pseudomallei* isolates from Sarawak, Malaysian Borneo, are predominantly susceptible to aminoglycosides and macrolides. Antimicrob Agents Chemother. 2014;58(1):162–166. | 24145517 | 10.1128/AAC.01842-13 |
| BpeEF-OprC → widespread trimethoprim resistance; ISBma2 in *folA* terminator | Podnecky NL, et al. The BpeEF-OprC efflux pump is responsible for widespread trimethoprim resistance in clinical and environmental *Burkholderia pseudomallei* isolates. Antimicrob Agents Chemother. 2013;57(9):4381–4386. | 23817379 | 10.1128/AAC.00660-13 |
| Co-trimoxazole resistance: *bpeT*, *bpeS*, *folM* mutations | Podnecky NL, et al. Mechanisms of resistance to folate pathway inhibitors in *Burkholderia pseudomallei*: deviation from the norm. mBio. 2017;8(5):e01357-17. | 28874476 | 10.1128/mBio.01357-17 |
| General AMR review for *Burkholderia* | Rhodes KA, Schweizer HP. Antibiotic resistance in *Burkholderia* species. Drug Resist Updat. 2016;28:82–90. | 27620956 | 10.1016/j.drup.2016.07.003 |
| Within-host rate 3.6 SNPs/yr (4.9×10⁻⁷ subs/site/yr); hypermutator 12.9 SNPs/yr; *penA*/*bpeT*/*ptr1* mutations; 35-kb and 45.5-kb deletions | Viberg LT, et al. Within-host evolution of *Burkholderia pseudomallei* during chronic infection of seven Australasian cystic fibrosis patients. mBio. 2017;8(2):e00356-17. | 28400528 | 10.1128/mBio.00356-17 |
| Within-host rate 1.7×10⁻⁷ subs/site/yr (95% HPD 1.3–2.1×10⁻⁷) over >16 years; seven large deletions | Pearson T, et al. Pathogen to commensal? Longitudinal within-host population dynamics, evolution, and adaptation during a chronic >16-year *Burkholderia pseudomallei* infection. PLoS Pathog. 2020;16(3):e1008298. | 32134991 | 10.1371/journal.ppat.1008298 |
| *B. mallei* as IS-expanded deletion derivative: 5.8 Mb, 171 IS elements (3.1%), K96243 has 42; 627+819 genes absent/variant; 99.1% mean identity | Nierman WC, et al. Structural flexibility in the *Burkholderia mallei* genome. Proc Natl Acad Sci USA. 2004;101(39):14246–14251. | 15377793 | 10.1073/pnas.0403306101 |
| *B. thailandensis* E264: 6.7 Mb; 71% of Bp virulence-gene orthologues present; arabinose operon absent from Bp | Yu Y, et al. Genomic patterns of pathogen evolution revealed by comparison of *Burkholderia pseudomallei* to avirulent *Burkholderia thailandensis*. BMC Microbiol. 2006;6:46. | 16725056 | 10.1186/1471-2180-6-46 |
| Arabinose assimilation operon deleted in Bp/Bm; restoration raises hamster LD50; T3SS down-regulated by arabinose | Moore RA, et al. Contribution of gene loss to the pathogenic evolution of *Burkholderia pseudomallei* and *Burkholderia mallei*. Infect Immun. 2004;72(7):4172–4187. | 15213162 | 10.1128/IAI.72.7.4172-4187.2004 |
| *B. oklahomensis* species description; type strain C6786^T | Glass MB, et al. *Burkholderia oklahomensis* sp. nov. Int J Syst Evol Microbiol. 2006;56(9):2171–2176. | 16957116 | 10.1099/ijs.0.63991-0 |
| *B. humptydooensis* — fifth member of the *B. pseudomallei* complex; MSMB43^T; GGDC <70%, 51.1% to *B. thailandensis* | Tuanyok A, et al. *Burkholderia humptydooensis* sp. nov. Appl Environ Microbiol. 2017;83(5):e02802-16. | 27986727 | 10.1128/AEM.02802-16 |
| General framing review of *B. pseudomallei* and melioidosis | Meumann EM, Limmathurotsakul D, Dunachie SJ, Wiersinga WJ, Currie BJ. *Burkholderia pseudomallei* and melioidosis. Nat Rev Microbiol. 2024;22(3):155–169. | 37794173 | 10.1038/s41579-023-00972-5 |

---

*Sources retrieved via PubMed Central, Europe PMC REST API, NCBI E-utilities and NCBI Datasets API, and publisher full-text pages, 2026-09-02.*
