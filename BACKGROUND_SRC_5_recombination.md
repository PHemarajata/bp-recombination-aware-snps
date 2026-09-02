# Recombination and lateral gene transfer in *Burkholderia pseudomallei*, and its consequences for phylogenetic and epidemiological inference

Literature research for the Background section of a genomics manuscript.
Compiled 2026-09-02. All numbers traced to a retrievable source; every unverified item is explicitly flagged **UNVERIFIED**.

---

## 0. Provenance and verification note (read this first)

**Tooling constraint.** The PubMed MCP tools and networked Bash were blocked in this session by a safety
classifier reacting to earlier conversation content. All retrieval below was done with WebSearch and
WebFetch. WebFetch summarises pages through a small model, so **every load-bearing number in this
document was extracted at least twice** — usually via a second, verification-style pass over the same
Europe PMC `fullTextXML` endpoint asking for exact sentences and "NOT FOUND" where absent. Where two
passes disagreed, or a number appeared only once, it is flagged in-line.

**One fetch was discarded as unreliable.** A PDF fetch of Chewapreecha 2017 from the Imperial College
Spiral repository returned content ("1,387 isolates from Thailand, Laos and Vietnam", "5.27 Mb core
genome", "r/m 3–4×") that directly contradicts the PMC full text of the same paper (469 isolates,
30 countries, no r/m reported). **None of that content is used here.** Treat any such figures seen
elsewhere as fabricated unless independently confirmed.

**A critical distinction used throughout this document.** Three different quantities are routinely
called "r/m" in this literature and are *not* interchangeable:

| Quantity | Meaning | Typical magnitude in *B. pseudomallei* |
|---|---|---|
| **per-site genome-wide r/m** | ratio of *nucleotide substitutions* introduced by recombination vs by point mutation, across a core-genome alignment | **2.2 – 8.5** |
| **per-allele MLST r/m** | probability that a *whole MLST allele* changes by recombination vs by mutation, at 7 housekeeping loci | **18 – 30** |
| **per-genome / per-branch counts** | number of recombination *events* or *blocks* per genome or per tree branch | 2,373 events / 106 genomes (Nandi); 36–39 blocks (Sarovich) |

A per-allele figure is inflated relative to a per-site figure roughly by the mean number of substitutions
imported per recombination event within a ~400–500 bp locus. Reporting "r/m ≈ 25 in *B. pseudomallei*"
(a per-allele MLST number) alongside genome-wide r/m values from other species is an apples-to-oranges
comparison. **This exact error is present in the published literature** — see §2.3.

---

## 1. Genome-wide (per-site) recombination-to-mutation ratio in *B. pseudomallei*

### 1.1 Nandi et al. 2015 — the primary genome-wide estimate

**Citation.** Nandi T, Holden MTG, Didelot X, Mehershahi K, Boddey JA, Beacham I, Peak I, Harting J,
Baybayan P, Guo Y, Wang S, How LC, Sim B, Essex-Lopresti A, Sarkar-Tyson M, Nelson M, Smither S, Ong C,
Aw LT, Hoon CH, Michell S, Studholme DJ, Titball R, Chen SL, Parkhill J, Tan P. *Burkholderia
pseudomallei* sequencing identifies genomic clades with distinct recombination, accessory, and
epigenetic profiles. **Genome Res. 2015;25(1):129–141.** PMID **25236617**; PMCID **PMC4317168**;
DOI **10.1101/gr.177543.114**.

**The headline number.**

> "We computed recombination/mutation (r/m) values, corresponding to the ratio of rates at which
> substitutions are introduced by recombination and mutation, across the entire population."

> **"The overall per site r/m ratio was 7.2."**

> "Recombination was also found to introduce more substitutions than mutation (r/m = 4.5 in Clade A,
> r/m = 8.5 in Clade B, and r/m = 6 in Clade C)"

- **No confidence intervals are reported** for 7.2, 4.5, 8.5 or 6. Verified by a second targeted pass.
- The quantity is explicitly **per site**, and explicitly defined as the ratio of *rates at which
  substitutions are introduced* by the two processes. This is the quantity directly comparable to
  cross-species genome-wide r/m surveys.

**Which method produced it — this matters and is commonly misreported.**

Nandi 2015 used **two different tools for two different purposes**:

1. **Gubbins** — used only to *mask* recombinant sites before tree-building:
   > "SNPs predicted to have arisen by homologous recombination were identified using Gubbins and
   > excluded from phylogenetic reconstruction"
   (The paper cites Croucher et al. 2011 at this point, i.e. the *S. pneumoniae* Science paper in which
   the approach was introduced, not the 2015 Gubbins software paper.)

2. **ClonalFrame** (Didelot & Falush 2007) — the tool that produced the **r/m values**:
   > "To measure clade-specific recombination rates, ClonalFrame (Didelot and Falush 2007) was applied
   > **separately to each Bp clade**. To reduce mapping artifacts, we focused on the 5.6-Mb portion of the
   > core genome that excludes mobile genetic elements and other potentially biased regions such as
   > surface polysaccharides, secretion systems, and tandem repeats."

- **It is ClonalFrame, not ClonalFrameML.** A verification pass confirmed the string "ClonalFrameML"
  **does not appear** anywhere in the paper. (ClonalFrameML was published in Feb 2015, essentially
  simultaneously with this paper.)
- **BratNextGen does not appear** anywhere in the paper. Verified.
- No ClonalFrame iteration/burn-in counts are given in the Methods.

**On what genomes and over what alignment.**

- **106 *B. pseudomallei* strains**: "97 strains from Singapore and Malaysia (87/10) and nine strains
  from Thailand", "isolated from various clinical, animal, and environmental sources over a 10 yr period
  (1996–2005)".
- **Alignment: a 5.6-Mb reduced core genome**, explicitly excluding mobile genetic elements, surface
  polysaccharide loci, secretion systems and tandem repeats. Note this is *smaller* than the ~7.2 Mb
  *B. pseudomallei* genome and deliberately excludes some of the most recombinogenic real estate — so
  7.2 is if anything a **conservative** genome-wide figure.
- **Three genomic clades (A, B, C)** among the Singapore/Malaysia strains. Representative STs given as
  Clade A (ST51, ST422, ST414, ST169); Clade B (ST423, ST84, ST289); Clade C (ST46, ST50). Per-clade
  strain counts are not tabulated in the text I could retrieve — **UNVERIFIED: n per clade.**

**SNP and recombination-event inventory.**

- **10,314 L-SNPs** ("lineage SNPs"):
  > "We excluded SNPs associated with regions of recombination as previously described, resulting in a
  > set of 10,314 SNPs representing mutations inherited by vertical descent along different lineages
  > ('lineage SNPs' [L-SNPs])."
- **74,532 R-SNPs** (recombination-associated SNPs):
  > "From 74,532 R-SNPs, we identified **2373 recombination events** across the three genomic clades,
  > with **recombination tract lengths ranging from 3 bp to 71 kb (median ~5 kb)**."
- Note the raw R-SNP : L-SNP ratio is 74,532 / 10,314 ≈ **7.2** — which is exactly the reported per-site
  r/m. This is a useful sanity check and tells you the quantity is essentially "recombined substitutions
  per clonal substitution".

**⚠ An internal tension in the paper, flagged.** A separate passage reads:
> "Of **2481, 821, and 334** recombination events detected within genomic Clades A, B, and C,
> respectively, we could assign sources ('matches') for ~60% of recombination events"

2481 + 821 + 334 = 3,636, which does not equal the 2,373 quoted above. Both strings were confirmed
present in the document by a verification pass. The most likely explanation is that the two figures come
from different analysis stages (e.g. events per clade before vs after merging/filtering), but **the paper
as retrieved does not reconcile them.** If you cite an event count, cite **2,373 across the three clades**
(the figure attached to the r/m calculation) and do not sum the per-clade numbers.

### 1.2 Seng et al. 2024 — the second genome-wide per-site r/m estimate, with confidence intervals

**Citation.** Seng R, et al. (Chewapreecha C, Limmathurotsakul D and colleagues). Genetic diversity,
determinants, and dissemination of *Burkholderia pseudomallei* lineages implicated in melioidosis in
Northeast Thailand. **Nat Commun. 2024;15:5699** (article number as indexed).
PMID **38972886**; PMCID **PMC11228029**; DOI **10.1038/s41467-024-50067-9**.

This is, as far as I can find, **the only other published genome-wide per-site r/m estimate for this
species**, and unlike Nandi it reports confidence intervals.

- **Design:** "1,391 *B. pseudomallei* isolates collected from nine hospitals in northeast Thailand
  between 2015 and 2018", plus additional regional isolates. Core-genome alignment: **77,156 SNPs**
  (cgMLST used 46,945 SNPs; MLST used 31 SNPs).
- **Population partition:** **PopPUNK** on genome assemblies; **three dominant lineages**.
- **Recombination detection:** **Gubbins v3.1.3**, run on **lineage-specific alignments** — i.e. within
  lineages, not across the species.
- **r/m values (per-site, per-lineage):**

  | Lineage | r/m | 95% CI |
  |---|---|---|
  | 1 | **3.7** | 3.3 – 4.1 |
  | 2 | **4.6** | 4.0 – 5.2 |
  | 3 | **2.2** | 1.8 – 2.6 |

  > "The ratio of polymorphisms introduced through recombination compared to those introduced by mutation
  > (r/m) was 3.7, 4.6 and 2.2 for lineages 1, 2, and 3 respectively"

  Table 1 is titled "Recombination in dominant lineages by coding sequences (CDS)" and its r/m column is
  defined as "Average r/m (number of SNPs introduced by recombination / SNPs introduced by
  substitutions)", broken out by **Internal nodes**, **Terminal nodes**, and **Average** with 95% CIs.
  This is the standard Gubbins per-branch r/m summary.

  **⚠ UNVERIFIED:** the Methods section, as retrieved, **does not explicitly name the software that
  computed the r/m values**. A verification pass returned NOT FOUND for that specific sentence. The
  Table 1 column definition and the internal/terminal-node breakdown are strongly diagnostic of Gubbins'
  own r/m output, but if you need to state the tool in the manuscript, confirm against the published
  Methods/Supplementary.

- **Near-universal recombination across the core genome:**
  > "A very high proportion of genes underwent recombination at least once: **99.5% of genes in lineage 1,
  > 99.9% in lineage 2, and 96.6% in lineage 3**."

  This is a striking and quotable result: **essentially no gene in the *B. pseudomallei* core genome is
  recombination-free** over the history of a single lineage.

- **Within-lineage vs whole-population diversity:** average pairwise core SNP distances were
  **549, 351 and 517 SNPs** for lineages 1, 2 and 3 respectively, versus **1,087 SNPs** across the total
  population.

### 1.3 Reconciling the two estimates

| Study | Estimate | Quantity | Method | Scale of analysis |
|---|---|---|---|---|
| Nandi 2015 | **7.2** overall; **4.5 / 8.5 / 6** by clade | per-site, per-substitution | **ClonalFrame** | within each of 3 clades; 5.6 Mb reduced core; 106 genomes, SG/MY/TH |
| Seng 2024 | **3.7 / 4.6 / 2.2** (with 95% CIs) | per-site, per-substitution | **Gubbins** (tool for r/m not explicitly named) | within each of 3 lineages; 1,391 genomes, NE Thailand |

Both are *within-lineage/within-clade* estimates. Neither is a whole-species estimate — and that is
methodologically correct, not an oversight (see §6 and §8). The **defensible range to quote for
*B. pseudomallei* genome-wide per-site r/m is roughly 2–9, centred around 4–7**, depending on lineage and
method. Nandi's values run higher than Seng's; plausible contributors are the different tools
(ClonalFrame vs Gubbins), the different geographic sampling, and the deliberate exclusion of
polysaccharide/secretion/tandem-repeat regions from Nandi's 5.6 Mb alignment.

### 1.4 Where *B. pseudomallei* sits relative to other bacteria

**Vos & Didelot 2009.** Vos M, Didelot X. A comparison of homologous recombination rates in bacteria and
archaea. **ISME J. 2009;3(2):199–208.** PMID **18830278**; DOI **10.1038/ismej.2008.93**.
**No PMCID — the article is not in PubMed Central.**

Abstract (verbatim, via Europe PMC):
> "It is a standard practice to test for the signature of homologous recombination in studies examining
> the genetic diversity of bacterial populations. Although it has emerged that homologous recombination
> rates can vary widely between species, comparing the results from different studies is made difficult
> by the diversity of estimation methods used. Here, Multi Locus Sequence Typing (MLST) datasets from a
> wide variety of bacteria and archaea are analyzed using the ClonalFrame method. This enables a direct
> comparison between species and allows for a first exploration of the question whether phylogeny or
> ecology is the primary determinant of homologous recombination rate."

**Scope and range of that survey**, as characterised in a recent peer-reviewed source (Torrance et al.
2024 PNAS, see below), which I use because I could not obtain Table 1 of the ISME J paper itself:
> "In their 2009 study, Vos & Didelot used ClonalFrame to estimate recombination rates using MLST data
> across **48 species**. This study found r/m rates to vary by over three orders of magnitude:
> from **r/m = 0.02 (*Leptospira interrogans*) to r/m = 63.6 (*Flavobacterium psychrophilum*)**."

> **⚠ UNVERIFIED — IMPORTANT GAP.** I was **unable to determine whether *B. pseudomallei* is one of the
> 48 species in Vos & Didelot 2009.** The paper is paywalled, has no PMC record, and the ResearchGate
> and ISME/OUP copies returned 403 / wrong-article. **Do not write that *B. pseudomallei* "ranks Nth in
> the Vos and Didelot survey" or "is among the most recombinogenic species in Vos and Didelot"
> without checking Table 1 of the original.**
>
> What you *can* safely write: Vos & Didelot's ClonalFrame/MLST survey of 48 species spans
> r/m = 0.02 to 63.6, and *B. pseudomallei*'s genome-wide per-site r/m of ~2–9 (Nandi 2015; Seng 2024)
> places it in the upper part of that distribution but well below the extreme. Note the further
> caveat that Vos & Didelot's values are **ClonalFrame-on-MLST** estimates, so they are not
> methodologically identical to a genome-wide alignment estimate either.

**A modern genome-based comparator.** Torrance EL, Burton C, Diop A, Bobay L-M. Evolution of homologous
recombination rates across bacteria. **PNAS. 2024;121(18):e2316302121.** PMID **38657048**;
PMCID **PMC11067023**; DOI **10.1073/pnas.2316302121**.

- **162 bacterial species and one archaeon; 7,541 genomes**; Approximate Bayesian Computation with
  forward simulation (CoreSimul).
- Effective **r/m ranged from 0.003 (*Staphylococcus saprophyticus*) to 32.18 (*Vibrio splendidus*);
  median 3.84; mean 5.98 ± 5.89.**
- **⚠ *B. pseudomallei* is NOT included in this study.** So there is no directly comparable
  genome-based r/m ranking for the species.
- Useful framing for the manuscript: *B. pseudomallei*'s within-lineage per-site r/m of ~2–9 sits
  **around to somewhat above the median (3.84) of 162 genome-surveyed bacteria**, not at the extreme.
  This is a much more defensible statement than "the highest recombination rate reported in bacteria",
  which derives from the per-allele MLST quantity (§2) and does not survive translation to a per-site
  genome-wide scale.

**⚠ A number to avoid.** An early web search surfaced a claim of "r/m = 973.8 for *Burkholderia
pseudomallei* MSHR3" attributed to a González-Torres multispecies analysis. **I could not verify this
against any primary source, the strain name "MSHR3" does not match standard *B. pseudomallei* strain
nomenclature (MSHR305, MSHR668 etc.), and the figure is wildly out of line with every verified estimate.
Treat as UNVERIFIED and do not cite.**

---

## 2. The MLST per-allele estimates — and why they are NOT genome-wide r/m

### 2.1 Pearson et al. 2009 — the "18 to 30 times" figure

**Citation.** Pearson T, Giffard P, Beckstrom-Sternberg S, Auerbach R, Hornstra H, Tuanyok A, Price EP,
Glass MB, Leadem B, Beckstrom-Sternberg JS, Allan GJ, Foster JT, Wagner DM, Okinaka RT, Sim SH,
Pearson O, Wu Z, Chang J, Kaul R, Hoffmaster AR, Brettin TS, Robison RA, Mayo M, Gee JE, Tan P,
Currie BJ, Keim P. Phylogeographic reconstruction of a bacterial species with high levels of lateral
gene transfer. **BMC Biol. 2009;7:78.** PMID **19922616**; PMCID **PMC2784454**;
DOI **10.1186/1741-7007-7-78**.

**The exact statement, verbatim:**
> **"The per-allele recombination to mutation parameter (r/m allele) suggests that *B. pseudomallei*
> alleles are between 18 and 30 times more likely to change by recombination rather than mutation."**

and, in the same paper:
> "recombination in *B. pseudomallei* is between 18 and 30 times more likely to generate new alleles
> than mutation"

and the widely-quoted comparative claim, from the abstract:
> "the relative contributions of homologous recombination versus mutation for *Burkholderia pseudomallei*
> is **over two times higher than for *Streptococcus pneumoniae*** and is thus **the highest value yet
> reported in bacteria**."

**Method that produced it — NOT ClonalFrame.** Verified: the string "ClonalFrame" **does not appear** in
Pearson 2009. The Methods state:
> "To calculate the relative contribution of recombination and mutation on allelic variation, we used the
> methods described elsewhere [39] except we used the program eBURST [35] to identify the most likely
> ancestral ST for each clonal complex."

This is the classic **Feil/Spratt-style single-locus-variant counting within clonal complexes**: identify
the founder ST of each clonal complex with eBURST, enumerate its single-locus variants, and classify each
as arising by point mutation (one nucleotide difference) or by recombination (multiple nucleotide
differences). The output is a **per-allele** ratio.

> **⚠ UNVERIFIED:** reference [39] of Pearson 2009 (the source of the counting method) was not resolved
> in this session. If the manuscript needs to name the method's origin precisely, resolve [39] from the
> paper's reference list. It is almost certainly a Feil/Spratt-lineage paper but I have not confirmed it.

**Other Pearson 2009 numbers.**
- Whole-genome genotyping identified **>14,000 SNPs** (**14,544 shared SNPs** in the
  *B. pseudomallei*/*B. mallei* phylogeny), yielding trees for **43 strains**.
- **>1,700 isolates** analysed by MLST; **641 sequence types**.
- Comparison of recombination and diversity **at seven housekeeping genes across eleven bacterial
  species** (Figure 7). **⚠ UNVERIFIED:** the per-species numeric values in that figure could not be
  extracted as text; a verification pass confirmed they appear only in the figure. Do not quote the
  comparator species' values without reading the figure.
- **Geographic structuring of recombination rate:**
  > "As might be expected by the greater interconnection of Southeast Asian STs compared to Australian
  > STs (Figures 4 and 6), the recombination to mutation ratio for the **Southeast Asian population is
  > approximately 1.7 times higher than in the Australian population**."
- Phylogeography: two subpopulations separated by **Wallace's Line**; "an Australian origin for
  *B. pseudomallei*, characterized by a single introduction event into Southeast Asia during a recent
  glacial period".

### 2.2 Why 18–30 is not comparable to 7.2

These are different denominators and different units:

- **Pearson's 18–30** counts *whole 400–500 bp MLST alleles* that changed. One recombination event that
  imports a divergent allele changes the allele once, regardless of how many nucleotides it carries. One
  point mutation also changes the allele once. So the ratio measures **events per locus**.
- **Nandi's 7.2 / Seng's 2.2–4.6** count *nucleotide substitutions*. One recombination event importing a
  5 kb tract with (say) 40 substitutions contributes 40 to the numerator.

Because the two quantities scale differently with tract length and donor divergence, **the numeric
values cannot be placed on a common axis.** In particular:

- **Pearson's "highest value yet reported in bacteria" claim is a statement about the per-allele MLST
  quantity, benchmarked against per-allele MLST quantities in ten other species.** It is not a claim
  that *B. pseudomallei* has the highest genome-wide per-site r/m of any bacterium, and the genome-wide
  data (Nandi 7.2; Seng 2.2–4.6; cf. Torrance median 3.84 across 162 species) do not support that
  stronger reading.

**Suggested manuscript wording** (safe, precise):
> Early MLST-based analysis estimated that *B. pseudomallei* MLST alleles are 18–30 times more likely to
> change by recombination than by mutation (Pearson et al. 2009) — a **per-allele** quantity derived from
> single-locus-variant counting within eBURST-defined clonal complexes, and not directly comparable to
> genome-wide per-site estimates. Whole-genome analyses subsequently placed the **per-site**
> recombination-to-mutation ratio at 7.2 across a Southeast Asian population (Nandi et al. 2015,
> ClonalFrame) and at 2.2–4.6 within three Northeast Thai lineages (Seng et al. 2024, 95% CIs 1.8–5.2).

### 2.3 The conflation is already in the literature — a worked example

**Spring-Pearson SM, et al. Pangenome Analysis of *Burkholderia pseudomallei*: Genome Evolution Preserves
Gene Order despite High Recombination Rates. PLoS One. 2015;10(10):e0140274.** PMID **26484663**;
PMCID **PMC4613141**; DOI **10.1371/journal.pone.0140274**.

This paper cites **"r/m values ~ 25 in *B. pseudomallei*"** attributed to Pearson et al., and compares it
against r/m values in other species. **~25 is the midpoint of Pearson's per-allele 18–30 range**, being
used in a comparison where the other values are (or read as) general recombination rates. This is a clean,
citable illustration for the Background that the per-allele / per-site distinction has been lost in
practice — and a good motivation for a recombination-aware SNP method.

Other useful content from this paper (verified):
- **37 *B. pseudomallei* genomes** (10 finished, 3 drafted into 2 chromosomes, 24 unfinished).
- Pangenome is **open**: "approximately 136 new genes identified with each new genome sequenced";
  **global core genome 4,568 ± 16 homologs**; strict core 3,278 HGs; total pangenome 13,799 homologous
  groups.
- **~5.8% of the genome consists of genomic islands** ("5 strains … average total length of 417.93 kbp
  of genomic islands and an average genome size of 7.23 Mbp"); "80% of GIs containing at least one
  transposase".
- **The two-compartment model** (their Model D), which is directly relevant to §4:
  > "**96% of the genome being a relatively rigid core with a low rate of exchange with the environment,
  > and the remaining 4% of the genome exchanging DNA very freely.**"
- **Gene order is nonetheless conserved:** mean synteny σ = **0.9765 (range 0.9089–0.9980)**; "gene order
  of adjacent genes is disrupted in only **2.4%** of orthologous gene pairs".
  > "High rates of gene transfer and recombination are incompatible with retaining gene order unless
  > these processes are either highly localized to specific sites within the genome, or are characterized
  > by symmetrical gene gain and loss."

### 2.4 MLST homoplasy — the empirical consequence of per-allele recombination

Two papers demonstrate directly that shared *B. pseudomallei* STs can be **convergent, not clonal**:

**De Smet B, Sarovich DS, Price EP, Mayo M, Theobald V, Kham C, Heng S, Thong P, Holden MTG, Parkhill J,
Peacock SJ, Spratt BG, Jacobs JA, Vandamme P, Currie BJ. Whole-genome sequencing confirms that
*Burkholderia pseudomallei* multilocus sequence types common to both Cambodia and Australia are due to
homoplasy. J Clin Microbiol. 2015;53(1):323–326.** PMID **25392354**; PMCID **PMC4290968**;
DOI **10.1128/JCM.02574-14**.
*(Note: often mis-cited as "Sarovich 2014". First author is **De Smet**; the issue is Jan 2015.)*

- **ST105 and ST849** were each found in both Australia and Cambodia. Four genomes: MSHR282 (Australia,
  ST105, 1994), CAM41 (Cambodia, ST105, 2008), MSHR4004 (Australia, ST849, 2010, soil), SHCH2430
  (Cambodia, ST849, 2010, clinical).
- **84,839 core genome SNPs** identified with SPANDx default settings. "GATK filtering or gubbins
  analysis removed 37,213 (44%) or 24,216 (13.5%) SNPs, respectively."
  > **⚠ Arithmetic inconsistency flagged:** 37,213/84,839 = 43.9% ✓, but 24,216/84,839 = **28.5%**, not
  > 13.5%. Either the percentage or the denominator differs in the original. **Verify against the
  > published text before quoting the 13.5% figure.** The absolute counts (37,213 and 24,216) were
  > returned consistently.
- Conclusions, verbatim:
  > "Our findings rule out recent *B. pseudomallei* transmission between these regions and demonstrate
  > **some limitations of MLST for source attribution of highly recombinogenic species**."
  > "Thus, **MLST of *B. pseudomallei* can, in rare cases, be confounded by ST homoplasy**."
  > "Overall, these findings suggest that both ST105 and ST849 convergence was a consequence of **both
  > mutation and multiple recombination events over considerable evolutionary time** rather than from
  > recent recombination involving the MLST loci."
- Earlier framing in the same paper: "the inherently high recombination rate of this bacterium and
  greater sampling efforts were predicted to inevitably reveal shared sequence types".

**Aziz A, Sarovich DS, Harris TM, Kaestli M, McRobb E, Mayo M, Currie BJ, Price EP. Suspected cases of
intracontinental *Burkholderia pseudomallei* sequence type homoplasy resolved using whole-genome
sequencing. Microb Genom. 2017;3(11):e000139.** PMID **29208140**; PMCID **PMC5729916**;
DOI **10.1099/mgen.0.000139**.
*(Author list beyond the first author is **UNVERIFIED** — confirm before citing in full.)*

This is the most quantitatively striking result on MLST homoplasy in the species:

| ST | Isolate pair | Genome-wide SNP difference |
|---|---|---|
| **ST-722** | MSHR0052 vs MSHR9076 | **21,211 SNPs** |
| **ST-804** | MSHR3528 vs MSHR4608 | **20,567 SNPs** |
| ST-149 (control, genuinely clonal) | MSHR0503 vs MSHR4300 | **404 SNPs** (divergence ~1984) |

> "High rates of genetic recombination, coupled with genetic drift over large timescales, can lead to
> occasional instances where *B. pseudomallei* strains have converged on the same ST by chance rather
> than by sharing a recent common ancestor."

> "In cases where a shared ST is identified between geographically distant locales, whole-genome
> sequencing should be used to resolve strain origin."

- Recombination method: **Gubbins v2.2.0**, default parameters, to identify recombinogenic SNPs for
  filtering prior to phylogenetic reconstruction.
- **The headline for the Background:** two isolates that are *identical at all seven MLST loci* differ by
  **>20,000 genome-wide SNPs**. This is a ~50-fold larger distance than a genuinely clonal same-ST pair
  (404 SNPs). No stronger single illustration exists of what per-allele recombination does to
  MLST-based epidemiological inference in this species.

---

## 3. Restriction–modification systems as barriers to recombination; structuring by lineage and geography

### 3.1 Nandi 2015 — RM systems as clade-specific gene-flow barriers

This is the central result of Nandi 2015 and the reason the paper matters beyond its r/m number.

**Abstract, verbatim (relevant portion):**
> "We observed clade-specific patterns of recombination and accessory gene exchange, and provide evidence
> that this is likely due to ongoing recombination between clade members. Reciprocally, **interclade
> exchanges were rarely observed, suggesting mechanisms restricting gene flow between clades**.
> Interrogation of accessory elements revealed that **each clade harbored a distinct complement of
> restriction-modification (RM) systems, predicted to cause clade-specific patterns of DNA methylation**.
> Using methylome sequencing, we confirmed that representative strains from separate clades indeed exhibit
> distinct methylation profiles. Finally, using an *E. coli* system, we demonstrate that **Bp RM systems
> can inhibit uptake of non-self DNA**. Our data suggest that **RM systems borne on mobile elements,
> besides preventing foreign DNA invasion, may also contribute to limiting exchanges of genetic material
> between individuals of the same species. Genomic clades may thus represent functional units of genetic
> isolation in Bp, modulating intraspecies genetic diversity.**"

**Supporting quantitative findings:**

- **RM system inventory:**
  > "By interrogating genes in the Bp accessory genome and mobile genetic elements, we identified
  > **four different Bp RM systems (I, II, III, and IV)**"

  Clade-associated distribution as extracted: ST51 strains carried RM Type IIGC genes; ST422 strains
  carried RM Type IIGC and Type IC; Clade B (ST423/ST84/ST289) was dominated by RM Type IC and Type IBC,
  with type III RM genes in ST84. **⚠ These per-ST assignments were extracted in a single pass and
  should be checked against the paper's figure/table before being restated in the manuscript.**

- **Functional demonstration (E. coli efficiency-of-transformation assay):**
  > "unmethylated reporter plasmids carrying one or two recognition sites exhibited a **>100-fold decrease
  > in EOT** compared to reporter plasmids with no recognition sites"

  Methylated plasmids showed "no significant EOT differences", confirming the effect is
  methylation-dependent restriction rather than a sequence artefact.

- **Methylome (SMRT) sequencing:** two representative strains; **six unique methylated motifs** total,
  including one shared motif **5′-CACAG-3′**, a Type II motif **5′-GTAWAC-3′** and a Type I motif
  **5′-GTCATN₅TGG-3′**.
  > **⚠ Inconsistency flagged:** across two extraction passes the strain-to-clade assignments came back
  > inconsistently (one pass: "Bp35 (Clade A) and Bp33 (Clade B)"; another: "Type I RM system specific to
  > Clade A (Bp33)"). Also, the Type I recognition motif was returned once as
  > `5′-GTACATN₅TGG-3′` and once as `5′-GTCATN₅TGG-3′`. **Do not quote specific strain-clade pairings or
  > the exact Type I motif without re-reading the paper.** The qualitative finding — two strains from
  > different clades have distinct methylomes — is solid.

- **Quantifying the barrier:**
  > "On average, **~5% of each genome from a given clade was found to have originated from another clade**
  > and approximately another **7% from a source not present in our data set**"

- **Recombination is ongoing, not historical:**
  > "recombined regions in the core genome had uniformly lower sequence divergence than nonrecombined
  > regions, suggesting that **recombination is active and ongoing within clades**"

- Source assignment: "we could assign sources ('matches') for ~60% of recombination events".

### 3.2 Recombination structured by geography

Three independent lines of evidence:

1. **Pearson 2009:** "the recombination to mutation ratio for the Southeast Asian population is
   approximately **1.7 times higher** than in the Australian population" — attributed to "the greater
   interconnection of Southeast Asian STs compared to Australian STs".

2. **Tuanyok A, Auerbach RK, Brettin TS, Bruce DC, Munk AC, Detter JC, Pearson T, Hornstra H,
   Sermswan RW, Wuthiekanun V, Peacock SJ, Currie BJ, Keim P, Wagner DM. A horizontal gene transfer event
   defines two distinct groups within *Burkholderia pseudomallei* that have dissimilar geographic
   distributions. J Bacteriol. 2007;189(24):9044–9049.** PMID **17933898**; DOI **10.1128/JB.01264-07**.
   The two mutually exclusive gene clusters at this locus are conventionally referred to as **YLF**
   (*Y*ersinia-*l*ike *f*imbrial) and **BTFC** (*B. thailandensis*-*l*ike *f*lagellum and *c*hemotaxis),
   with YLF predominating in Southeast Asia and BTFC in Australia.
   > **⚠ UNVERIFIED:** I could not retrieve the abstract or the exact geographic percentages —
   > Europe PMC returned 503/504 on repeated attempts and both ASM and PubMed returned 403 / cookie
   > walls. **The citation metadata above (authors, journal, volume, issue, pages, year, PMID, DOI) is
   > verified via search-result metadata; the YLF/BTFC naming and the direction of the geographic skew
   > are from secondary sources and the title. Confirm the percentages and the cluster names against the
   > original before citing any number.** This is a single-HGT-event marker that is geographically
   > structured — exactly the kind of locus that will behave badly in a naive SNP phylogeny.

3. **Chewapreecha 2017 (below):** the global population is geographically structured, with the
   Australasian cluster carrying the deepest diversity; recombination correction had to be done
   cluster-by-cluster because the between-cluster divergence exceeded the detectors' range.

### 3.3 Recombination structured by lineage

- **Nandi 2015:** clade-specific recombination and accessory gene exchange; RM systems as the proposed
  mechanism; "Genomic clades may thus represent functional units of genetic isolation".
- **Seng 2024:** materially different r/m per lineage (**3.7 vs 4.6 vs 2.2**, non-overlapping 95% CIs
  between lineages 2 and 3), i.e. **recombination intensity is a lineage-level property, not a species
  constant**. This is a direct argument against applying a single species-wide recombination correction
  or a single SNP threshold.
- **Nandi 2015:** clade-level r/m also varied nearly two-fold (4.5 / 8.5 / 6).

---

## 4. Recombination hotspots and cold spots; chromosome I vs chromosome II; genomic islands

### 4.1 Chromosome I vs chromosome II — chromosome II recombines more

**Nandi 2015**, verified verbatim:

> "L-SNPs occurred at a **~1.2-fold higher frequency on Chr II compared to Chr I**
> (**6.1 × 10⁻³ SNPs per site for Chr I versus 7.5 × 10⁻³ for Chr II**)"

> "Similar to L-SNPs, **higher recombination levels were observed for Chr II than Chr I**
> (**P < 2.2 × 10⁻¹⁶, Mann-Whitney U test**)"

So **both** the clonal mutation rate and the recombination rate are elevated on the smaller, secondary
chromosome. This is the standard multi-replicon bacterial pattern (chromid carrying accessory/niche
functions under relaxed constraint), and it means a uniform genome-wide recombination model is misspecified
across the two replicons.

### 4.2 Hotspot definition and map

**Nandi 2015** is the **published recombination map** for this species.

- **Hotspot definition:**
  > "Genome-wide median recombination frequencies (RFs) were computed to identify genomic regions
  > exhibiting elevated recombination rates and multiple recombination events. We identified **1630
  > protein-coding genes (Chr I: 897 genes; Chr II: 733)** associated with regions of high recombination
  > (**RF > RF_median + 3MAD**, median absolute deviation)."

  1,630 genes is roughly a quarter of the ~5,800-gene *B. pseudomallei* core — i.e. **hotspots are not a
  small fringe of the genome**.

- **Functional enrichment:**
  > "Genes experiencing high recombination frequencies were significantly enriched in **intracellular
  > trafficking and secretion pathways (corrected P = 0.0006, binomial test)**, whereas genes involved in
  > **protein translation were underrepresented (corrected P = 0.012, binomial test)**"

  The translation-machinery depletion is the closest thing to a published **cold spot** signal in this
  species — housekeeping/translational genes recombine less than expected. See the caveat below.

- **Named hotspot loci (with locus tags):**
  > "Examples of genomic regions exhibiting elevated recombination included a **Type III secretion cluster
  > (TTSS3; BPSS1520–BPSS1537)** previously linked to mammalian virulence, and a **Type IVB pilus cluster
  > (TFP8, Chr II: BPSS2185–BPSS2198)**"

  Both are on chromosome II and both are virulence-associated (see §9).

- **The map figure:** the paper presents K96243 genomic tracks for Chr I and Chr II showing
  "Row 1: Genomic locations of recombined regions (red). Row 2: Genomic locations of **16 known Bp
  genomic islands** (gray)", alongside sequence features of nonrecombined regions (NR), recombined
  regions (R) and accessory elements (AE). **This is the figure to cite as the published recombination
  map.** The 16 K96243 genomic islands trace to the reference genome paper: Holden MTG, et al. Genomic
  plasticity of the causative agent of melioidosis, *Burkholderia pseudomallei*. PNAS.
  2004;101(39):14240–14245. PMID **15377794**; PMCID **PMC521101**; DOI **10.1073/pnas.0403302101**.

- > **⚠ UNVERIFIED / GAP:** a targeted verification pass returned **NOT FOUND** for any explicit
  > discussion of recombination **cold spots** in Nandi 2015, and I found **no published cold-spot map
  > for *B. pseudomallei* in any paper**. The only cold-spot-adjacent published result is the
  > under-representation of translation genes among hotspots (corrected P = 0.012). If the manuscript
  > wants to claim cold spots exist, that claim is currently **unsupported by a dedicated published
  > analysis** — which may itself be a gap worth stating as motivation.

### 4.3 Genomic islands as site-specific recombination hotspots

**Tuanyok A, Leadem BR, Auerbach RK, Beckstrom-Sternberg SM, Beckstrom-Sternberg JS, Mayo M, Wuthiekanun V,
Brettin TS, Nierman WC, Peacock SJ, Currie BJ, Wagner DM, Keim P. Genomic islands from five strains of
*Burkholderia pseudomallei*. BMC Genomics. 2008;9:566.** PMID **19038032**; PMCID **PMC2612704**;
DOI **10.1186/1471-2164-9-566**.
*(Full author list is **UNVERIFIED** — confirm before citing in full.)*

- **71 distinct genomic islands** identified across five reference strains:
  K96243 (17 GIs, 12 unique), 1710b (16, 10 unique), 1106a (16, 9 unique), MSHR668 (17, 13 unique),
  MSHR305 (21, 17 unique).
- **GI sizes: 3.91 kb to 107.94 kb.**
- **40–60% of all GIs** associate with tRNA genes.
- **Mechanism — tRNA-mediated site-specific recombination (tRNA-SSR):**
  > "Recombination at tRNA loci is initiated at the 3′ end of tRNA genes. This process creates a short,
  > direct repeat sequence."
  Direct repeats ranged from a **14 bp repeat (tRNA-Ser; GI13)** to a **56 bp repeat (tRNA-Leu; GI5)**.
  tRNAs involved: Phe, Met, Leu, Pro, Arg, Cys, Ser, Gly, Thr, Ala.
- **The hotspot statement, verbatim:**
  > "**recombination events at tRNA-Met, Pro, Thr, Ala, and Arg are common across the genomes, suggesting
  > that these sites serve as 'genomic hotspots' for GI insertion in *B. pseudomallei* genomes**"
- GIs contain "transposase, integrase, conjugal plasmid protein, recombinase, invertase, and resolvase
  genes", with different IS elements across strains suggesting "GIs in *B. pseudomallei* originated from
  different sources".

### 4.4 Synthesis for §4

There are **two distinct recombination regimes** in this genome, and they need different treatment:

1. **Site-specific, integrase/tRNA-mediated acquisition of genomic islands** — localised to a small number
   of tRNA attachment sites, accounting for ~5.8% of the genome (Spring-Pearson 2015), producing
   **accessory-genome presence/absence variation**. These regions are usually excluded from core-genome
   SNP analysis anyway.
2. **Widespread homologous recombination in the core genome** — 1,630 hotspot genes across both
   chromosomes (Nandi 2015), 96.6–99.9% of genes recombined at least once per lineage (Seng 2024),
   elevated on chromosome II. **This is the regime that corrupts core-genome SNP distances and
   phylogenies, and it is not solved by masking mobile elements.**

Spring-Pearson's Model D — "96% of the genome … relatively rigid core with a low rate of exchange …
remaining 4% … exchanging DNA very freely" — is a useful shorthand, but note it was fitted to
**gene presence/absence frequency spectra**, not to homologous substitution data, and it sits in some
tension with Seng 2024's finding that ~99% of core genes show homologous recombination at least once.
The two are reconcilable (rare homologous replacement of nearly every gene vs frequent turnover of a few),
but do not present them as measuring the same thing.

---

## 5. Lateral gene transfer with *B. thailandensis* and other *Burkholderia*; natural competence

### 5.1 Natural competence and transformation in the genus

*B. pseudomallei* and *B. thailandensis* are **naturally transformable**, which supplies a direct mechanism
for the homologous recombination measured in §1.

**Thongdee M, Gallagher LA, Schell M, Dharakul T, Songsivilai S, Manoil C. Targeted mutagenesis of
*Burkholderia thailandensis* and *Burkholderia pseudomallei* through natural transformation of PCR
fragments. Appl Environ Microbiol. 2008;74(10):2985–2989.** PMID **18310423**; PMCID **PMC2394929**;
DOI **10.1128/AEM.00030-08**.
*(Author list and page range **UNVERIFIED** beyond first author — confirm before citing in full.)*
Establishes that both species take up and recombine exogenous linear DNA efficiently enough for routine
targeted mutagenesis with PCR products.

**Kang Y, Norris MH, Barrett AR, Wilcox BA, Hoang TT. Knockout and pullout recombineering for naturally
transformable *Burkholderia thailandensis* and *Burkholderia pseudomallei*. Nat Protoc.
2011;6(8):1085–1104.** PMID **21738123**; PMCID **PMC3564556**; DOI **10.1038/nprot.2011.346**.
*(Author list **UNVERIFIED**.)*

**Norris MH, Schweizer HP, Tuanyok A. *Burkholderia pseudomallei* natural competency and DNA catabolism:
Identification and characterization of relevant genes from a constructed fosmid library. PLoS One.
2017;12(12):e0189018.** PMID **29253888**; PMCID **PMC5734746**;
DOI **10.1371/journal.pone.0189018**. *(Author list **UNVERIFIED**.)*
Links natural transformation to DNA catabolism: *B. pseudomallei* 1026b, K96243 and *B. thailandensis*
E264 can use DNA as a sole carbon source, but only 1026b and E264 are naturally transformable —
i.e. **competence is strain-variable within *B. pseudomallei***.

**Heacock-Kang Y, et al. The heritable natural competency trait of *Burkholderia pseudomallei* in other
*Burkholderia* species through *comE* and *crp*. Sci Rep. 2018;8:12422 (article number **UNVERIFIED**).**
PMID **30127446**; PMCID **PMC6102250**; DOI **10.1038/s41598-018-30853-4**.

- **Naturally competent:** *B. pseudomallei* **1026b** (**75.7%** GFP uptake), *B. thailandensis* **E264**
  (**63.7%**).
- **Not naturally competent:** *B. pseudomallei* **K96243**, *B. mallei* **ATCC23344**,
  *B. cenocepacia* **K56-2**.
- **"~50% of Bp strains"** are naturally transformable.
- **comE** (competence protein, "56% amino acid similarity and 38% identity" to *N. meningitidis* ComEA)
  and **crp** (Crp/Fnr-family regulator) are sufficient to confer competence on non-competent
  *Burkholderia*, raising GFP uptake to **39.7%–73%**.
  > **⚠ All numeric values in this bullet list were extracted in a single pass. Verify before quoting.**

**Interpretive point for the Background:** competence is present in roughly half of strains and is
transferable between species via two genes. That is consistent with (a) high but heterogeneous
recombination rates, and (b) recombination intensity being a **lineage-level trait** (§3.3) rather than a
species constant — a competence-negative lineage should recombine less.

### 5.2 *B. pseudomallei* ↔ *B. thailandensis* gene exchange

**Sim BM, Chantratita N, Ooi WF, Nandi T, Tewhey R, Wuthiekanun V, Thaipadungpanit J, Tumapa S,
Ariyaratne P, Sung WK, Sem XH, Chua HH, Ramnarayanan K, Lin CH, Liu Y, Feil EJ, Glass MB, Tan G,
Peacock SJ, Tan P. Genomic acquisition of a capsular polysaccharide virulence cluster by non-pathogenic
*Burkholderia* isolates. Genome Biol. 2010;11(8):R89.** PMID **20799932**; PMCID **PMC2945791**;
DOI **10.1186/gb-2010-11-8-r89**.

- 50 *B. thailandensis* isolates profiled; **39 variable genomic regions** identified.
- > "Variant *B. thailandensis* isolates exhibited isolated acquisition of a **capsular polysaccharide
  > biosynthesis gene cluster**" resembling that of *B. pseudomallei*; confirmed by whole-genome
  > sequencing of strain **E555**.
- > "Both whole-genome microarray and multi-locus sequence typing analysis revealed that the variant
  > strains formed part of a phylogenetic subgroup distinct from the ancestral *B. thailandensis*
  > population."
- Functionally, E555 "did not exhibit enhanced virulence relative to other *B. thailandensis* strains",
  indicating capsule acquisition alone is not sufficient for mammalian pathogenicity.
- These are the isolates now generally called the ***B. thailandensis* capsular variant (BTCV)**.
  *(The "BTCV" abbreviation itself is from later literature, not this paper.)*

**This is the cleanest published case of a *B. pseudomallei* virulence determinant crossing a species
boundary into a near-neighbour by lateral transfer.**

### 5.3 Transfer to more distant *Burkholderia*

**Patarapuwadol S, et al. Whole-genome sequencing of *Burkholderia glumae* strains from Thailand reveals
potential horizontal gene transfer with *Burkholderia pseudomallei*. PLoS One. 2025;20(12):e0340071
(volume/issue **UNVERIFIED**).** PMID **41474711**; PMCID **PMC12755741**;
DOI **10.1371/journal.pone.0340071**.

- *B. glumae* strains 60BGCRMSO3-9 and 60BGCRMSO3-11 carry a **~41.7 kb horizontally acquired region on
  chromosome 1 (positions 122,026–163,756)** with **90–100% amino acid identity** to a genomic region in
  *B. pseudomallei* strain 8400.
- Two genes specifically attributed to *B. pseudomallei* origin: a **putative nuclease
  (WP_038743760.1)** and a **PAAR domain-containing protein (WP_004535952.1)**. (PAAR proteins are Type
  VI secretion spike components — i.e. a competition/virulence-associated function.)
- Detection methods: HGT-DB and NCBI nr BLAST, **Alien Hunter v1.3.0**, comparative alignment with
  PyGenomeViz. **These are compositional/BLAST-based HGT predictors, not homologous-recombination
  detectors — this is evidence of gene acquisition, not of homologous replacement.**
- Ecological rationale, verbatim:
  > "Both species exhibit higher prevalence during periods of increased rainfall and humidity, which lead
  > to simultaneous population peaks during the rice-growing season. These seasonal conditions create
  > dense, metabolically active microbial communities in waterlogged paddy soils, enhancing the frequency
  > of cell-to-cell contact."

**Also relevant:** *Burkholderia cepacia* strains expressing a *B. pseudomallei*-like capsular
polysaccharide have been reported (Microbiol Spectr, 2024; **full citation UNVERIFIED — I located the
article title and journal only**). Do not cite without resolving.

---

## 6. Homologous-recombination detection methods applied to *B. pseudomallei*

### 6.1 Inventory of what has actually been run on this species

| Study | Tool(s) | Population scale | Run within lineages or across the species? | What they concluded |
|---|---|---|---|---|
| **Nandi 2015** (n=106, SG/MY/TH) | **Gubbins** (masking) + **ClonalFrame** (rate estimation) | 106 genomes, 3 clades, 5.6 Mb reduced core | **Within clades** — "ClonalFrame … was applied **separately to each Bp clade**" | Per-site r/m 7.2 overall; 4.5/8.5/6 by clade; RM systems restrict interclade flow |
| **Seng 2024** (n=1,391, NE Thailand) | **Gubbins v3.1.3** | 3 PopPUNK lineages | **Within lineages** (lineage-specific alignments) | r/m 3.7 / 4.6 / 2.2 (95% CIs); 96.6–99.9% of genes recombined ≥once |
| **Chewapreecha 2017** (n=469, 30 countries, 79 yr) | **Gubbins**, after **hierBAPS** partitioning | Global | **Within hierBAPS clusters**, explicitly to stay inside Gubbins' working range | Australia an early reservoir; single transmission out of Australasia; American MRCA 1806/1759 |
| **Chewapreecha 2019** (n=1,010, Thailand+Australia GWAS) | **Gubbins** | Monophyletic groups | **Within** — "we ran Gubbins on individual monophyletic group" | Recombination comparable in clinical and environmental isolates; 47 genes / 26 loci associated |
| **Zheng 2021** (Hainan, n=1,654 total) | **Gubbins** | Groups defined by a **5,000 pairwise-SNP-distance** threshold | **Within groups**, explicitly to keep Gubbins in range | 9 phylogenetic groups; 21 between-city transmission events |
| **Aziz 2017** (ST homoplasy) | **Gubbins v2.2.0**, default | Small comparative sets | Within comparison sets | ST-722 and ST-804 homoplasy; >20,000 SNPs between same-ST isolates |
| **De Smet 2015** (ST homoplasy) | **Gubbins** (+ GATK filtering) | 4 genomes + refs | Within comparison set | ST105/ST849 homoplasy; MLST limits for source attribution |
| **Sarovich 2017** (island cluster) | **Gubbins v1.4.1 AND ClonalFrameML** | 2 STs from one outbreak investigation | Within outbreak set | Gubbins: 36 blocks / ~339 kb; ClonalFrameML: 39 blocks / ~333 kb; 73 SNPs (~5%) remained |

### 6.2 The key methodological observation

**Every published *B. pseudomallei* recombination analysis I could find ran the detector *within* a
lineage, clade, or pre-clustered group — never across the whole species.** Three of them state the reason
explicitly (§8). This is not incidental: it reflects a documented limitation of the detectors, and it means
that **no published estimate of species-wide recombination in *B. pseudomallei* exists**, only a set of
within-lineage estimates that differ from one another by more than two-fold.

**BratNextGen and fastGEAR: no application found.** A Europe PMC search for
`("Burkholderia pseudomallei") AND ("fastGEAR" OR "BratNextGen" OR "ClonalFrameML")` returned only
Sarovich 2017 among *B. pseudomallei* primary studies (which used ClonalFrameML), plus method papers and
unrelated species. **I found no published application of BratNextGen or fastGEAR to *B. pseudomallei*.**
Given that fastGEAR is specifically designed to detect *ancestral* (whole-lineage) recombination and to
work across diverse alignments where Gubbins cannot (§8), **this is a real and citable gap** — arguably a
strong motivation for the manuscript.

### 6.3 Sarovich 2017 — the one head-to-head comparison in this species

**Sarovich DS, Chapple SNJ, Price EP, Mayo M, Holden MTG, Peacock SJ, Currie BJ. Whole-genome sequencing
to investigate a non-clonal melioidosis cluster on a remote Australian island. Microb Genom.
2017;3(8):e000117.** PMID **29026657**; PMCID **PMC5610713**; DOI **10.1099/mgen.0.000117**.
*(Author list **UNVERIFIED** beyond first author.)*

- **Gubbins v1.4.1: 36 discrete recombination blocks totalling ~339 kb.**
- **ClonalFrameML: 39 discrete recombination blocks totalling ~333 kb.**
- The two tools agree closely on total recombinant sequence (~1.6% difference in total length,
  ~8% difference in block count) — **useful evidence that the choice between them is not the dominant
  source of uncertainty at this scale.**
- **The epidemiologically important number:** ST-125 and ST-126 differed by **1,328 SNPs and 154 indels**
  before correction; after excluding recombinogenic regions, **"73 SNPs (~5 % total) still separated the
  ST-125 and ST-126 strains"**.
  **~95% of the apparent SNP distance between these two lineages was recombination, not clonal
  divergence.** This is the single most directly relevant published number in this species for a
  recombination-aware SNP method.
- Within-lineage clonal diversity was minute by comparison: "entire ST-125 population differed by only
  **2 SNPs and 11 indels**"; "one SNP differentiated MSHR0435 from the other ST-126 isolates".
- > "*B. pseudomallei* is a highly recombinogenic species and substantial genetic differentiation can
  > arise due to recombination events … [which] can confound evolutionary signal."

---

## 7. Methodological consequences: what recombination does to phylogenetic and epidemiological inference

### 7.1 General bacterial-genomics evidence

**(a) Croucher et al. 2015 — the Gubbins paper**

Croucher NJ, Page AJ, Connor TR, Delaney AJ, Keane JA, Bentley SD, Parkhill J, Harris SR. Rapid
phylogenetic analysis of large samples of recombinant bacterial whole genome sequences using Gubbins.
**Nucleic Acids Res. 2015;43(3):e15.** PMID **25414349**; PMCID **PMC4330336**;
DOI **10.1093/nar/gku1196**.

Mechanism of distortion:
> "The substantial lengths of sequence transferred via different recombination mechanisms can influence
> genome-wide measures of sequence similarity to a **far greater extent than the vertically-inherited
> point mutations that are the signal of shared common ancestry**"

Topological distortion via homoplasy:
> such acquisitions "can affect tree topology if convergence arises by similar sequences being acquired at
> the same genomic location in parallel on different branches"

Performance (simulations):
- Sensitivity for recombination detection **~83%**, stable across recombination rates (linear relationship
  between simulated and detected recombinations, **R² = 0.999**).
- PPVs for identifying recombination-introduced base substitutions **>99.5%**.
- Ancestral base-substitution reconstruction: "all PPVs above 90% and all FDRs and FNRs below 10%".
- PPVs for point mutations "around two-thirds or greater even at p_rec values of 0.75, despite all 10
  simulations using this parameterization having **at least 35-fold more base substitutions introduced
  through recombination than occurring by point mutation**."
- **Branch-length recovery:** correlation with true branch lengths improved from a median **R² = 0.714**
  for the naïve initial ML tree to a final median **R² = 0.996** after Gubbins iteration.

**(b) Didelot & Wilson 2015 — the ClonalFrameML paper**

Didelot X, Wilson DJ. ClonalFrameML: efficient inference of recombination in whole bacterial genomes.
**PLoS Comput Biol. 2015;11(2):e1004041.** PMID **25675341**; PMCID **PMC4326465**;
DOI **10.1371/journal.pcbi.1004041**.

- Parameters inferred: **R/θ** (relative rate of recombination to mutation), **δ** (mean import tract
  length, bp), **ν** (mean divergence of imported sequence). And crucially the definition:
  > **r/m = (R/θ) × δ × ν**

  This formula is worth stating in the manuscript: it makes explicit that r/m is a **composite** of rate,
  tract length and donor divergence. Two populations with identical r/m can have entirely different
  recombination processes, and only one of the three components (donor divergence, ν) controls how badly
  a SNP distance is inflated per event.

- **Topology is robust; branch lengths are not:**
  > "Recombination is therefore informative about the tree topology in exactly the same way as mutation"
  > "**The scale of branch lengths in the reconstructed phylogeny was 2.1 times greater than in the true
  > tree**, because the latter accounts only for the substitutions introduced by mutation whereas the
  > former also includes the differences imported by recombination."
  > "The most noticeable difference concerned some of the **shortest terminal branches** in the true
  > clonal genealogy, which had lengths **several times longer** in the reconstructed phylogeny."

- **The direct statement about outbreak/transmission inference — the single best quote for §7:**
  > "This distortion **could have important consequences, for example it could mislead one into excluding
  > the possibility of direct transmission between two infected individuals in a genomic epidemiology
  > study**."

  Note the *direction*: recombination makes closely related isolates look **further apart**, causing
  **false exclusion** of transmission links — i.e. false negatives in outbreak calling, not false
  positives.

- **Downstream inference:** large recombination events produce homoplasy "mirrored on the branch leading
  to the sister clade", contributing to
  > "well-recognized **distortion of branch lengths leading to spurious inference of demography, selection
  > and molecular clocks**."

- Accuracy: 213 of 248 (**86%**) simulated recombination events correctly detected; 95% CIs contained the
  true value in **82%, 85% and 74%** of simulations for R/θ, δ and ν respectively (when δR < 1).
  **Branch score** between true and uncorrected ML trees **7.47 × 10⁻³** vs **9.72 × 10⁻⁵** between true
  and ClonalFrameML trees — a **~77-fold improvement**.
- Speed vs ClonalFrame: ~15 minutes vs ~42 hours on one simulated dataset (>100×).

**(c) Hedge & Wilson 2014 — the paradox resolved, and a warning about naive filtering**

Hedge J, Wilson DJ. Bacterial phylogenetic reconstruction from whole genomes is robust to recombination
but demographic inference is not. **mBio. 2014;5(6):e02158-14.** PMID **25425237**; PMCID **PMC4251999**;
DOI **10.1128/mBio.02158-14**.
*(Note: PMID verified as 25425237. This paper is sometimes mis-cited with PMID 25370495.)*

**Abstract, verbatim (this is the citation to lead with):**
> "Phylogenetic inference in bacterial genomics is fundamental to understanding problems such as
> population history, antimicrobial resistance, and transmission dynamics. The field has been plagued by
> an apparent state of contradiction since the distorting effects of recombination on phylogeny were
> discovered more than a decade ago. Researchers persist with detailed phylogenetic analyses while
> simultaneously acknowledging that recombination seriously misleads inference of population dynamics and
> selection. Here we resolve this paradox by showing that **phylogenetic tree topologies based on whole
> genomes robustly reconstruct the clonal frame topology but that branch lengths are badly skewed.
> Surprisingly, removing recombining sites can exacerbate branch length distortion caused by
> recombination.**"

Supporting detail (extracted from the full text; **single-pass extraction — verify the specific simulation
parameters before quoting them numerically**):
- Simulations of **1,000 populations of 100 bacterial genomes, each 1 Mb**, under ρ = 1%, 0.1% and 0%.
- Topological accuracy: "clonal frame topology was reconstructed remarkably accurately even when
  recombination was present (**>97%**)"; at ρ = 8% "topological accuracy remained high (**93%**)".
- **The counter-intuitive result, and the most important one for a recombination-aware SNP method:**
  removing homoplasies "**actually exacerbated the spurious signal of demographic growth generated by
  recombination**", because "**older recombination events were more likely to be detected as
  homoplasies … preferential removal of substitutions from the deep branches**". The resulting trees
  "appeared even more star-like", with "95% confidence intervals that excluded the true growth rate".
- Demographic inference: "recombination gave rise to a spurious or inflated signal of demographic growth
  when we fitted a model of exponential growth using BEAST"; growth rates "systematically overestimated,
  even though tree topology remained accurate".

**Synthesis of (a)–(c) for the Background:**
1. **Topology survives** recombination reasonably well (Hedge & Wilson: >97%; Didelot & Wilson: "informative
   about the tree topology in exactly the same way as mutation").
2. **Branch lengths do not** (2.1× inflation in ClonalFrameML simulations; "badly skewed" in Hedge &
   Wilson), and the distortion is **worst on the shortest terminal branches** — exactly the branches that
   outbreak investigation depends on.
3. **Naive filtering can make things worse**, because recombination detectors preferentially strip deep
   branches, further star-ifying the tree and worsening demographic and dating inference (Hedge & Wilson).
   This is the strongest published argument that "run Gubbins and move on" is not a sufficient answer.

### 7.2 *Burkholderia*-specific evidence

**(a) The magnitude of SNP-distance inflation.** Sarovich 2017: of the **1,328 SNPs** separating ST-125
from ST-126, only **73 (~5%)** survived recombination filtering. **~95% of the raw core-genome SNP
distance was recombinant.**

**(b) MLST-scale homoplasy.** Aziz 2017: same-ST isolate pairs differing by **21,211** and **20,567**
genome-wide SNPs, versus **404** for a genuinely clonal same-ST pair. De Smet 2015: ST105 and ST849 shared
across continents by convergence, "demonstrat[ing] some limitations of MLST for source attribution of
highly recombinogenic species".

**(c) Dating inference.** Chewapreecha 2017 performed BEAST dating **only after** removing recombination
within hierBAPS clusters, and reported the American-isolate MRCA as **1806 (chromosome I) or 1759
(chromosome II)**, with a **combined 95% HPD across both chromosomes of 1682–1849**, noted as overlapping
the height of the slave trade (1650–1850). Two points worth making:
- The **~47-year discrepancy between the two chromosomes' point estimates** from the same isolates is
  itself an indication of how sensitive dating is to which sites are analysed — and chromosome II is the
  more recombinogenic replicon (Nandi 2015, §4.1).
- The very wide HPD (167 years) is characteristic of dating a recombining organism.

**(d) SNP thresholds for outbreak calling — the concrete gap.**

Webb JR, Mayo M, Rachlin A, Woerle C, Meumann E, Rigas V, Harrington G, Kaestli M, Currie BJ. Genomic
Epidemiology Links *Burkholderia pseudomallei* from Individual Human Cases to *B. pseudomallei* from
Targeted Environmental Sampling in Northern Australia. **J Clin Microbiol. 2022;60(3):e01648-21.**
PMID **35080450**; DOI **10.1128/jcm.01648-21**; PMCID **PMC8925902**.

> "Previous epidemiological investigations on Australian melioidosis animal and human clusters have used
> SNP differences ranging from **0 to 5 SNPs** for inferring an environmental transmission event"

> "For this study we found a **maximum of 15 SNPs** in the 17 case-environment isolate matches for which
> we inferred a causal transmission."

> "For example, **≤37 SNPs** has been used as the cutoff for inferring transmission of *Pseudomonas
> aeruginosa*"

**Critically: a verification pass confirmed this paper describes SNP calling with SPANDx v3.2 and
mentions NO recombination detection method — no Gubbins, no ClonalFrameML — and contains no discussion of
whether recombination affects SNP distances or outbreak inference.**

Set this against Sarovich 2017's finding that **~95% of the SNP distance between two co-circulating
lineages was recombinant**, and the problem is immediate: a **0–5 SNP** or **15 SNP** threshold applied to
uncorrected core-genome SNP distances in a species with per-site r/m of 2–9 is measuring a quantity whose
composition is unknown. A single ~5 kb import from a divergent donor can, by itself, exceed any of these
thresholds. **This is the sharpest published motivation for a recombination-aware SNP-distance method in
this species.**

> **⚠ GAP.** I found **no published study that directly quantifies how recombination corrupts SNP-distance
> thresholds in *B. pseudomallei*** — i.e. no paper that computes outbreak-calling sensitivity/specificity
> with and without recombination correction in this species. The argument above is assembled from
> Sarovich 2017 (magnitude of inflation) + Webb 2022 (thresholds in use, uncorrected) + Didelot & Wilson
> 2015 (mechanism and direction of the error). **State it as an inference, not as a published finding.**

**(e) Population-partitioning thresholds also assume a recombination model.** Zheng 2021 (Hainan) used a
**5,000 pairwise-SNP-distance** threshold specifically to make Gubbins tractable (§8) — note this is
~340× the 15-SNP transmission threshold, illustrating the enormous dynamic range of SNP distances over
which different inferential questions are asked in this species, and that different questions are
answered on differently-corrected data.

---

## 8. The divergence range over which recombination detection actually works

### 8.1 What the method papers say

**Gubbins (Croucher 2015):**
> "The algorithm is **most effective when detecting imports of sequence into a densely sampled collection
> of closely-related isolates**, where recombinations import a high density of base substitutions from
> **divergent donors**."

**Too diverse — the failure mode and the prescribed remedy:**
> "In such datasets, the identification of recombinations as regions with elevated densities of base
> substitutions is **confounded by the high diversity of the sequences in the alignment**, and therefore
> for improved accuracy **such populations would need to be split into sets of closely-related isolates**."

**Too clonal / donors too similar — the other failure mode, with a hard number:**
> "**Gubbins was only able to predict 5–10% of the actual number of recombinations**, largely as a
> consequence of only **35% of the recombinations importing more than s_min base substitutions**."

  That is, when donor and recipient are similar, imports carry too few substitutions to register as a
  density anomaly and **~90–95% of real recombination events are missed**. Gubbins detects
  *substitution-dense* imports, not recombination *per se*.

Also: "The PPVs for the reconstruction of base substitutions were above 95% across all simulations,
**increasing as samples became more closely related**"; and lower accuracy was "associated with
simulations using extreme p_rec and low p_birth values" (i.e. more divergent sequences).

**ClonalFrameML (Didelot & Wilson 2015):**
- Designed for a **"single lineage (for example a single sequence type according to multi-locus sequence
  typing), with frequent imports from other lineages"** — i.e. an explicitly within-lineage tool, whose
  model assumes imports come from *outside* the sampled set and are recognisable by a "high number of
  substitutions which are not seen elsewhere in the dataset".
- **Failure mode 1 (too much recombination):** when **δR > 1**, "estimates of δ and ν remain in good
  alignment … but the relative rate **R/θ is sometimes underestimated**", because the model permits at
  most one recombination event per position per branch.
- **Failure mode 2 (recombination from within the sample):** with intra-population recombination,
  "R/θ was also correlated with the correct values, but **almost always underestimated**", especially
  with short tracts.
  **Both failure modes bias r/m downward.** So published *B. pseudomallei* r/m values should be read as
  **lower bounds**, not point estimates — a useful and defensible statement.

**fastGEAR (Mostowy 2017):**
Mostowy R, Croucher NJ, Andam CP, Corander J, Hanage WP, Marttinen P. Efficient inference of recent and
ancestral recombination within bacterial populations. **Mol Biol Evol. 2017;34(5):1167–1182.**
PMID **28199698**; PMCID **PMC5400400**; DOI **10.1093/molbev/msx066**.

- Benchmarked against **STRUCTURE, Gubbins and ClonalFrameML**, varying **between-population distance
  (parameter T, from 1.0 × 10³ to 2.0 × 10⁴)**.
- "The false positive rate stayed very low with all methods."
- "fastGEAR had similar sensitivity to detect recent and intermediate recombinations to the other methods,
  and **no method was systematically the best**."
- "fastGEAR detected **ancestral** recombinations equally well to recent and intermediate ones. This is
  particularly encouraging as **none of the other methods could detect ancestral recombinations**."
- **The explicit divergence dependence:**
  > "the proportion of detected recombinations was **highly dependent on the between-lineage distance** …
  > **in the absence of clear population genetic structure, populations are relatively closely related and
  > there are too few polymorphisms to signal the presence of a recombination**."
  > "As expected, performance of fastGEAR depends on the strength of the underlying population genetic
  > structure."
  > "a higher **within-lineage** distance often affected the inference of ancestral recombinations as it
  > generated the intra-lineage population genetic structure."
- **Scale guidance:** "fastGEAR is at its strongest when applied to investigate **between-lineage or
  between-species** bacterial data." And: "When run in a lineage-by-lineage manner, fastGEAR had **clearly
  lower sensitivity** than with the full alignment, and the lengths of the external recombinations were
  often overestimated".
- The paper gives **no explicit numeric minimum or maximum divergence thresholds** — only that performance
  rises with population-structure strength.

**Note the direct opposition, which is the crux of §8:** Gubbins and ClonalFrameML require you to
**subdivide** a diverse sample into closely-related sets; fastGEAR requires you to **keep** the diverse
alignment together, because it draws its power from seeing the donor lineages. Running the wrong tool at
the wrong scale fails in opposite directions. **There is no single scale at which all three work.**

### 8.2 What *B. pseudomallei* studies say — this species is where the guidance was operationalised

**Chewapreecha 2017** — the clearest statement in the *B. pseudomallei* literature:

Chewapreecha C, Holden MTG, Vehkala M, Välimäki N, Yang Z, Harris SR, Mather AE, Tuanyok A, De Smet B,
Le Hello S, Bizet C, Mayo M, Wuthiekanun V, Limmathurotsakul D, Phetsouvanh R, Spratt BG, Corander J,
Keim P, Dougan G, Dance DAB, Currie BJ, Parkhill J, Peacock SJ. Global and regional dissemination and
evolution of *Burkholderia pseudomallei*. **Nat Microbiol. 2017;2:16263.** PMID **28112723**;
PMCID **PMC5300093**; DOI **10.1038/nmicrobiol.2016.263**.
*(Full author list is **UNVERIFIED** — confirm before citing in full.)*

> "A tree-independent hierarchical Bayesian clustering with **hierBAPS** … was employed to determine the
> population structure generated from the core genome mapping alignment. This method allows the population
> to be sub-divided into groups with closely related genetic backgrounds and **allows the recombination
> detection tool (Gubbins) to operate within its best performing range**."

> "Except for the Australasian cluster (Group 1), which contained the highest amount of diversity for each
> isolate and **could not be further sub-clustered**, we continued the hierarchical clustering **until the
> diversity observed in secondary or tertiary clusters fell within the limit of recombination
> detection**."

> "Recombination fragments were called and removed from the alignment using Gubbins. A **lineage-specific
> phylogeny** was reconstructed using the remaining variants."

Study scale: **469 isolates from 30 countries over 79 years (1935–2013)**; 276 newly sequenced, 193 public;
reference K96243; **324,637 core-genome SNPs**; pan-genome of **25,812 CDS** with **4,064 core (present in
99% of isolates) and 21,748 accessory**. **No r/m value is reported** (verified: NOT FOUND).

Two things worth drawing out for the manuscript:
1. **The whole-species *B. pseudomallei* alignment is explicitly too diverse for Gubbins.** The authors had
   to iterate hierarchical clustering until diversity dropped "within the limit of recombination
   detection".
2. **One cluster — the Australasian group — was too diverse even after clustering and could not be
   resolved further.** That is a documented, named, species-specific failure of the standard pipeline, in
   the most basal and most diverse part of the *B. pseudomallei* population. Anything inferred about
   Australasian ancestry rests on data that could not be recombination-corrected to the same standard as
   the rest.

**Zheng H, Qin J, Chen H, Hu H, Zhang X, Yang C, Wu Y, Li Y, Li S, Kuang H, Zhou H, Shen D, Song K, Song Y,
Zhao T, Yang R, Tan Y, Cui Y. Genetic diversity and transmission patterns of *Burkholderia pseudomallei*
on Hainan island, China, revealed by a population genomics analysis. Microb Genom. 2021;7(11).**
PMID **34762026**; PMCID **PMC8743561**; DOI **10.1099/mgen.0.000659**.

Operationalises the same guidance with an explicit numeric threshold:
> "… based on **a threshold of 5000 PSDs [pairwise SNP distances]**, which ensured that the population of
> strains was subdivided into groups with closely related genetic backgrounds and **allowed the
> recombination detection tool Gubbins to operate within its best performance range**"

Scale: 122 newly sequenced Hainan strains (2002–2018) plus 1,532 published genomes (**1,654 total**);
**325,036 SNPs across a 5.8 Mb core genome**. Groups were subdivided into 4–56 subgroups each. No r/m
reported.

**This 5,000-PSD figure appears to be the only published numeric operating threshold for recombination
detection in *B. pseudomallei*.** It is an empirical rule of thumb from one study, not a validated
criterion — present it as such.

**Seng 2024** applied Gubbins v3.1.3 to lineage-specific alignments, within lineages whose average
pairwise core SNP distances were **549, 351 and 517 SNPs** (vs 1,087 across the whole population) — i.e.
an order of magnitude below Zheng's 5,000-PSD ceiling.

### 8.3 Summary of the working range, as best it can be stated from the literature

| Regime | What happens | Evidence |
|---|---|---|
| **Too diverse** (whole-species *B. pseudomallei* alignment) | Elevated-SNP-density signal is swamped by background diversity; recombination cannot be distinguished from divergence. Remedy: subdivide. | Croucher 2015 ("confounded by the high diversity … would need to be split"); Chewapreecha 2017 (hierBAPS to reach "best performing range"; Australasian cluster unresolvable); Zheng 2021 (5,000-PSD threshold) |
| **In range** (within lineage/clade; ~350–5,000 pairwise SNPs in this species) | Gubbins ~83% sensitivity, >99.5% PPV for recombinant substitutions; ClonalFrameML ~86% event detection; ~77-fold branch-score improvement | Croucher 2015; Didelot & Wilson 2015; Seng 2024; Nandi 2015 |
| **Too clonal / donors too similar** (outbreak-scale, near-identical isolates) | **~90–95% of real recombination events missed**; r/m underestimated | Croucher 2015 ("only able to predict 5–10% of the actual number"); Didelot & Wilson 2015 (R/θ "almost always underestimated" with intra-population recombination); Mostowy 2017 ("too few polymorphisms to signal the presence of a recombination") |

**The problem this creates for outbreak genomics specifically:** the regime in which SNP thresholds are
applied (0–15 SNPs, Webb 2022) is precisely the "too clonal" regime in which the standard detectors are
least able to find recombination — while, at the lineage scale immediately above it, recombination
accounts for ~95% of SNP distance (Sarovich 2017). **Recombination is most consequential and least
detectable at exactly the scale where outbreak calls are made.** This is, in my reading, the single
strongest framing available for the manuscript's Background.

---

## 9. Selection and adaptation: recombination importing virulence and resistance determinants

### 9.1 Virulence

**Nandi 2015 — recombination hotspots are enriched for virulence-associated functions:**
> "Genes experiencing high recombination frequencies were **significantly enriched in intracellular
> trafficking and secretion pathways (corrected P = 0.0006, binomial test)**"

> "Examples of genomic regions exhibiting elevated recombination included a **Type III secretion cluster
> (TTSS3; BPSS1520–BPSS1537) previously linked to mammalian virulence**, and a **Type IVB pilus cluster
> (TFP8, Chr II: BPSS2185–BPSS2198)**"

and from the abstract:
> "**Highly recombinant regions exhibited functional enrichments that may contribute to virulence.**"

**Note the careful hedge in the authors' own wording — "may contribute to virulence". Nandi 2015 shows
recombination is *enriched in* virulence loci; it does not demonstrate that recombination *caused* a
virulence phenotype.** Preserve that hedge.

**Sim 2010 — a virulence cluster crossing species by lateral transfer:** *B. thailandensis* variants
acquired a *B. pseudomallei*-like **capsular polysaccharide biosynthesis gene cluster** (capsule being an
established *B. pseudomallei* virulence determinant). Importantly, the recipients "**did not exhibit
enhanced virulence relative to other *B. thailandensis* strains**" — so acquisition of a virulence gene
cluster was **not sufficient** for a virulence phenotype. This is a useful counterweight to
over-interpretation.

**Chewapreecha 2019 — GWAS evidence of mobile, selected, disease-associated loci:**
Chewapreecha C, Mather AE, Harris SR, Hunt M, Holden MTG, Chaichana C, Wuthiekanun V, Dougan G, Day NPJ,
Limmathurotsakul D, Parkhill J, Peacock SJ. Genetic variation associated with infection and the environment
in the accidental pathogen *Burkholderia pseudomallei*. **Commun Biol. 2019;2:428.** PMID **31799430**;
PMCID **PMC6874650**; DOI **10.1038/s42003-019-0678-x**.

- **1,010 genomes** from Northeast Thailand and Australia. **47 genes from 26 distinct loci** associated
  with clinical vs environmental origin in Thailand; **12 replicated** in the Australian cohort.
- **A large, mobile, disease-associated toxin locus:** *tcdB*, *tcdA*, *tccC*, *fhaC*, spanning
  **69.7 kb**, "flanked … by several integrases and transposases families including IS2, IS3/911, IS4,
  IS66, IS166, IS407, IS111A/IS1328/IS1533 and IS1478, **indicative of a mobile genetic element origin**".
  Homologues occur "in diverse bacterial species including *Pseudomonas*, *Yersinia* and *Photorhabdus*".
- **8 of the 26 loci** "consisted of IS, transposons and integrase".
- **Turnover under selection:** "**38/47 genes showed a preference for net gain**, 4/47 net loss, 5/47
  ambiguous". In one monophyletic group, the toxin locus was "acquired and lost **10 and 9 times**,
  respectively … suggesting not only a selective advantage but also a fitness cost".
- **Selection:** mean dN/dS below 1 for both groups, but "significantly higher for environmental-associated
  compared with disease-associated genes and accessory genes", i.e. "reduced purifying selection, or
  elevated diversifying selection" on environment-associated genes.
- **Methodologically relevant:** Gubbins was run "on individual monophyletic group[s]"; GWAS controlled for
  population structure using "the first three principal components calculated from metric dimensional
  scaling"; and "Similar numbers of recent recombination events … were identified in both clinical and
  environmental isolates", so recombination was not systematically confounded with the phenotype.
  > **⚠** The paper states "The contribution of recombination to the overall diversity was estimated by
  > ratio of recombination events to the number of mutations (r/m)" but **no numeric r/m value appears in
  > the main text** (verified).

### 9.2 Antimicrobial resistance — a genuine negative result, and it is important

**Madden DE, Webb JR, Steinig EJ, Currie BJ, Price EP, Sarovich DS. Taking the next-gen step: comprehensive
antimicrobial resistance detection from *Burkholderia pseudomallei*. EBioMedicine. 2021;63:103152.**
PMID **33285499**; PMCID **PMC7724162**; DOI **10.1016/j.ebiom.2020.103152**.

From the abstract, verbatim:
> "*B. pseudomallei* was chosen due to limited treatment options, high fatality rate, and **AMR caused
> exclusively by chromosomal mutation (i.e. single-nucleotide polymorphisms [SNPs], insertions-deletions
> [indels], copy-number variations [CNVs], inversions, and functional gene loss)**."

> "CARD, ResFinder, and AMRFinderPlus **failed to identify any clinically-relevant AMR in
> *B. pseudomallei***; ARIBA identified AMR encoded by SNPs and indels that were manually added to its
> database."

**This is a clean, citable statement that — unlike virulence determinants — AMR in *B. pseudomallei* is
not imported by lateral transfer.** It is a useful asymmetry for the Background: recombination reshapes
the virulence-associated and accessory genome of this species, but resistance arises by chromosomal
mutation. (Note that a mutation-derived resistance allele could still be *spread* between lineages by
homologous recombination even if the determinant is not an acquired gene — I found **no published
*B. pseudomallei* study testing that**, so do not assert it.)

**Genus-level comparator for recombination and AMR:**
Diaz Caballero J, Clark ST, Wang PW, Donaldson SL, Coburn B, Tullis DE, Yau YCW, Waters VJ, Hwang DM,
Guttman DS. A genome-wide association analysis reveals a potential role for recombination in the
evolution of antimicrobial resistance in *Burkholderia multivorans*. **PLoS Pathog.
2018;14(12):e1007453.** PMID **30532201**; PMCID **PMC6300292**; DOI **10.1371/journal.ppat.1007453**.
*(Author list **UNVERIFIED** beyond first author.)*

> "we identified a minimum of **14 recombination events**, and observed that **loci carrying putative
> parallel pathoadaptations and polymorphisms statistically associated with β-lactam resistance were
> over-represented in these recombinogenic regions**."

- Resistance-associated loci: ***ampD*** (β-lactams), an ***araC*** transcriptional regulator
  (aminoglycosides, quinolones), and ***BMUL_3342*** outer-membrane porin (aminoglycosides, quinolones).
- Recombination detection: **DnaSP Hudson–Kaplan four-gamete test** (not Gubbins/ClonalFrameML).
- No r/m estimate for *B. multivorans*.
- This is a **within-host, single-patient** study in a different species — use it as suggestive
  genus-level context only, not as evidence about *B. pseudomallei*.

---

## 10. Consolidated gaps and cautions

**Numbers I could not verify (do not use without checking the primary source):**
1. **Whether *B. pseudomallei* appears in Vos & Didelot 2009's 48-species table, and at what rank.**
   Paywalled, no PMC record, ResearchGate/OUP inaccessible. The survey's *range* (0.02–63.6) is verified
   via Torrance 2024 PNAS.
2. **Tuanyok 2007 (YLF/BTFC) abstract and geographic percentages.** Citation metadata verified;
   content not retrieved (repeated 403/503/504).
3. **Pearson 2009 reference [39]** — the origin of the per-allele counting method.
4. **Pearson 2009 Figure 7** per-species values for the 11-species comparison (figure-only data).
5. **De Smet 2015's "13.5%"** — arithmetically inconsistent with 24,216/84,839 = 28.5%.
6. **Nandi 2015: 2,373 vs 2,481+821+334 recombination events** — both strings verified present, not
   reconciled in the retrievable text.
7. **Nandi 2015 strain-to-clade assignments (Bp33/Bp35) and the exact Type I recognition motif** —
   returned inconsistently across passes.
8. **Nandi 2015 per-clade strain counts.**
9. **Seng 2024: which software computed the r/m values** — Methods returned NOT FOUND on a targeted pass.
10. **Full author lists** for Aziz 2017, Tuanyok 2008, Sarovich 2017, Chewapreecha 2017,
    Diaz Caballero 2018, Thongdee 2008, Kang 2011, Norris 2017, Heacock-Kang 2018, Patarapuwadol 2025.
11. **Heacock-Kang 2018 numeric values** (75.7%, 63.7%, ~50%, 39.7–73%) — single-pass extraction.
12. **Hedge & Wilson 2014 simulation specifics** (1,000 populations × 100 genomes × 1 Mb; ρ values; >97%,
    93%) — single-pass extraction. The abstract is fully verified.
13. **The "r/m = 973.8 for *B. pseudomallei* MSHR3"** claim seen in a web search — **almost certainly
    spurious; do not cite.**
14. **"Identification of *Burkholderia cepacia* strains that express a *B. pseudomallei*-like capsular
    polysaccharide" (Microbiol Spectr)** — title and journal only.

**Substantive gaps in the published literature itself (i.e. genuine motivation for the manuscript):**
- **No whole-species recombination analysis of *B. pseudomallei* exists.** Every study partitions first.
- **No published application of BratNextGen or fastGEAR to *B. pseudomallei*** — notable given fastGEAR is
  the one tool designed for the between-lineage/ancestral recombination that this species clearly has.
- **No published recombination cold-spot map for *B. pseudomallei*.** Only the translation-gene
  under-representation in Nandi 2015 (corrected P = 0.012).
- **No study quantifies how recombination corrupts SNP-distance thresholds in *B. pseudomallei*.**
  Outbreak thresholds in current use (0–5 SNPs; max 15 SNPs, Webb 2022) are applied to **uncorrected**
  distances, in a species where recombination accounted for ~95% of the SNP distance between two
  co-circulating lineages (Sarovich 2017).
- **No numeric, validated operating range for recombination detection in this species.** Zheng 2021's
  5,000-PSD threshold is the only published number and is an empirical rule of thumb from a single study.
- **Chewapreecha 2017's Australasian cluster could not be recombination-corrected** to the standard applied
  to the rest of the global population — a documented failure in the most basal part of the species.

---

## 11. Citation table

| Role | Citation | PMID | DOI |
|---|---|---|---|
| **Primary genome-wide r/m (7.2); RM barriers; hotspot map; Chr I vs II** | Nandi T, Holden MTG, Didelot X, Mehershahi K, Boddey JA, Beacham I, Peak I, Harting J, Baybayan P, Guo Y, Wang S, How LC, Sim B, Essex-Lopresti A, Sarkar-Tyson M, Nelson M, Smither S, Ong C, Aw LT, Hoon CH, Michell S, Studholme DJ, Titball R, Chen SL, Parkhill J, Tan P. *Burkholderia pseudomallei* sequencing identifies genomic clades with distinct recombination, accessory, and epigenetic profiles. Genome Res. 2015;25(1):129–141. | 25236617 | 10.1101/gr.177543.114 |
| **Second genome-wide r/m with 95% CIs (3.7/4.6/2.2); ~99% of genes recombined** | Seng R, et al. Genetic diversity, determinants, and dissemination of *Burkholderia pseudomallei* lineages implicated in melioidosis in Northeast Thailand. Nat Commun. 2024;15:5699. | 38972886 | 10.1038/s41467-024-50067-9 |
| **Per-allele MLST r/m (18–30×); Wallace's Line; SE Asia 1.7× Australia** | Pearson T, Giffard P, Beckstrom-Sternberg S, Auerbach R, Hornstra H, Tuanyok A, Price EP, Glass MB, Leadem B, Beckstrom-Sternberg JS, Allan GJ, Foster JT, Wagner DM, Okinaka RT, Sim SH, Pearson O, Wu Z, Chang J, Kaul R, Hoffmaster AR, Brettin TS, Robison RA, Mayo M, Gee JE, Tan P, Currie BJ, Keim P. Phylogeographic reconstruction of a bacterial species with high levels of lateral gene transfer. BMC Biol. 2009;7:78. | 19922616 | 10.1186/1741-7007-7-78 |
| **Cross-species r/m survey (48 spp., MLST/ClonalFrame, 0.02–63.6)** | Vos M, Didelot X. A comparison of homologous recombination rates in bacteria and archaea. ISME J. 2009;3(2):199–208. *(no PMCID)* | 18830278 | 10.1038/ismej.2008.93 |
| **Modern genome-based cross-species r/m (162 spp.; median 3.84); characterises Vos & Didelot** | Torrance EL, Burton C, Diop A, Bobay L-M. Evolution of homologous recombination rates across bacteria. PNAS. 2024;121(18):e2316302121. | 38657048 | 10.1073/pnas.2316302121 |
| **Global phylogeography; hierBAPS + Gubbins "best performing range"; dating** | Chewapreecha C, Holden MTG, Vehkala M, Välimäki N, Yang Z, Harris SR, Mather AE, Tuanyok A, De Smet B, Le Hello S, Bizet C, Mayo M, Wuthiekanun V, Limmathurotsakul D, Phetsouvanh R, Spratt BG, Corander J, Keim P, Dougan G, Dance DAB, Currie BJ, Parkhill J, Peacock SJ. Global and regional dissemination and evolution of *Burkholderia pseudomallei*. Nat Microbiol. 2017;2:16263. | 28112723 | 10.1038/nmicrobiol.2016.263 |
| **Gubbins + ClonalFrameML head-to-head in this species; ~95% of SNP distance recombinant** | Sarovich DS, et al. Whole-genome sequencing to investigate a non-clonal melioidosis cluster on a remote Australian island. Microb Genom. 2017;3(8):e000117. | 29026657 | 10.1099/mgen.0.000117 |
| **MLST homoplasy: >20,000 SNPs between same-ST isolates** | Aziz A, et al. Suspected cases of intracontinental *Burkholderia pseudomallei* sequence type homoplasy resolved using whole-genome sequencing. Microb Genom. 2017;3(11):e000139. | 29208140 | 10.1099/mgen.0.000139 |
| **MLST homoplasy across continents; limits of MLST for source attribution** | De Smet B, Sarovich DS, Price EP, Mayo M, Theobald V, Kham C, Heng S, Thong P, Holden MTG, Parkhill J, Peacock SJ, Spratt BG, Jacobs JA, Vandamme P, Currie BJ. Whole-genome sequencing confirms that *Burkholderia pseudomallei* multilocus sequence types common to both Cambodia and Australia are due to homoplasy. J Clin Microbiol. 2015;53(1):323–326. | 25392354 | 10.1128/JCM.02574-14 |
| **SNP thresholds in use for outbreak calling (0–5, max 15); no recombination correction** | Webb JR, Mayo M, Rachlin A, Woerle C, Meumann E, Rigas V, Harrington G, Kaestli M, Currie BJ. Genomic epidemiology links *Burkholderia pseudomallei* from individual human cases to *B. pseudomallei* from targeted environmental sampling in northern Australia. J Clin Microbiol. 2022;60(3):e01648-21. | 35080450 | 10.1128/jcm.01648-21 |
| **5,000-PSD threshold to keep Gubbins in range** | Zheng H, Qin J, Chen H, Hu H, Zhang X, Yang C, Wu Y, Li Y, Li S, Kuang H, Zhou H, Shen D, Song K, Song Y, Zhao T, Yang R, Tan Y, Cui Y. Genetic diversity and transmission patterns of *Burkholderia pseudomallei* on Hainan island, China, revealed by a population genomics analysis. Microb Genom. 2021;7(11). | 34762026 | 10.1099/mgen.0.000659 |
| **Pangenome; 5.8% genomic islands; 96%/4% model; gene order conserved; per-allele/per-site conflation example** | Spring-Pearson SM, et al. Pangenome analysis of *Burkholderia pseudomallei*: genome evolution preserves gene order despite high recombination rates. PLoS One. 2015;10(10):e0140274. | 26484663 | 10.1371/journal.pone.0140274 |
| **71 genomic islands; tRNA-mediated site-specific recombination hotspots** | Tuanyok A, et al. Genomic islands from five strains of *Burkholderia pseudomallei*. BMC Genomics. 2008;9:566. | 19038032 | 10.1186/1471-2164-9-566 |
| **K96243 reference genome; genomic plasticity; the 16 genomic islands** | Holden MTG, et al. Genomic plasticity of the causative agent of melioidosis, *Burkholderia pseudomallei*. PNAS. 2004;101(39):14240–14245. | 15377794 | 10.1073/pnas.0403302101 |
| **Geographically structured HGT event (YLF vs BTFC)** *(content UNVERIFIED)* | Tuanyok A, Auerbach RK, Brettin TS, Bruce DC, Munk AC, Detter JC, Pearson T, Hornstra H, Sermswan RW, Wuthiekanun V, Peacock SJ, Currie BJ, Keim P, Wagner DM. A horizontal gene transfer event defines two distinct groups within *Burkholderia pseudomallei* that have dissimilar geographic distributions. J Bacteriol. 2007;189(24):9044–9049. | 17933898 | 10.1128/JB.01264-07 |
| **Gubbins method paper; divergence range; performance** | Croucher NJ, Page AJ, Connor TR, Delaney AJ, Keane JA, Bentley SD, Parkhill J, Harris SR. Rapid phylogenetic analysis of large samples of recombinant bacterial whole genome sequences using Gubbins. Nucleic Acids Res. 2015;43(3):e15. | 25414349 | 10.1093/nar/gku1196 |
| **ClonalFrameML method paper; r/m = (R/θ)×δ×ν; branch-length inflation; transmission-exclusion warning** | Didelot X, Wilson DJ. ClonalFrameML: efficient inference of recombination in whole bacterial genomes. PLoS Comput Biol. 2015;11(2):e1004041. | 25675341 | 10.1371/journal.pcbi.1004041 |
| **Topology robust, branch lengths skewed; removing sites can make it worse** | Hedge J, Wilson DJ. Bacterial phylogenetic reconstruction from whole genomes is robust to recombination but demographic inference is not. mBio. 2014;5(6):e02158-14. | 25425237 | 10.1128/mBio.02158-14 |
| **fastGEAR; benchmark vs Gubbins/ClonalFrameML/STRUCTURE across divergence** | Mostowy R, Croucher NJ, Andam CP, Corander J, Hanage WP, Marttinen P. Efficient inference of recent and ancestral recombination within bacterial populations. Mol Biol Evol. 2017;34(5):1167–1182. | 28199698 | 10.1093/molbev/msx066 |
| **Natural transformation of *B. pseudomallei* and *B. thailandensis*** | Thongdee M, et al. Targeted mutagenesis of *Burkholderia thailandensis* and *Burkholderia pseudomallei* through natural transformation of PCR fragments. Appl Environ Microbiol. 2008;74(10):2985–2989. | 18310423 | 10.1128/AEM.00030-08 |
| **Recombineering in naturally transformable *Burkholderia*** | Kang Y, et al. Knockout and pullout recombineering for naturally transformable *Burkholderia thailandensis* and *Burkholderia pseudomallei*. Nat Protoc. 2011;6(8):1085–1104. | 21738123 | 10.1038/nprot.2011.346 |
| **Competence genes; DNA catabolism; strain-variable competence** | Norris MH, et al. *Burkholderia pseudomallei* natural competency and DNA catabolism: identification and characterization of relevant genes from a constructed fosmid library. PLoS One. 2017;12(12):e0189018. | 29253888 | 10.1371/journal.pone.0189018 |
| **comE/crp confer competence; ~50% of Bp strains transformable** | Heacock-Kang Y, et al. The heritable natural competency trait of *Burkholderia pseudomallei* in other *Burkholderia* species through *comE* and *crp*. Sci Rep. 2018;8. | 30127446 | 10.1038/s41598-018-30853-4 |
| **Capsule virulence cluster transferred to *B. thailandensis* (BTCV)** | Sim BM, Chantratita N, Ooi WF, Nandi T, Tewhey R, Wuthiekanun V, Thaipadungpanit J, Tumapa S, Ariyaratne P, Sung WK, Sem XH, Chua HH, Ramnarayanan K, Lin CH, Liu Y, Feil EJ, Glass MB, Tan G, Peacock SJ, Tan P. Genomic acquisition of a capsular polysaccharide virulence cluster by non-pathogenic *Burkholderia* isolates. Genome Biol. 2010;11(8):R89. | 20799932 | 10.1186/gb-2010-11-8-r89 |
| **HGT from *B. pseudomallei* into *B. glumae* (~41.7 kb region)** | Patarapuwadol S, et al. Whole-genome sequencing of *Burkholderia glumae* strains from Thailand reveals potential horizontal gene transfer with *Burkholderia pseudomallei*. PLoS One. 2025. | 41474711 | 10.1371/journal.pone.0340071 |
| **GWAS: mobile disease-associated loci; dN/dS; gene gain/loss** | Chewapreecha C, Mather AE, Harris SR, Hunt M, Holden MTG, Chaichana C, Wuthiekanun V, Dougan G, Day NPJ, Limmathurotsakul D, Parkhill J, Peacock SJ. Genetic variation associated with infection and the environment in the accidental pathogen *Burkholderia pseudomallei*. Commun Biol. 2019;2:428. | 31799430 | 10.1038/s42003-019-0678-x |
| **AMR in *B. pseudomallei* is exclusively chromosomal, not acquired** | Madden DE, Webb JR, Steinig EJ, Currie BJ, Price EP, Sarovich DS. Taking the next-gen step: comprehensive antimicrobial resistance detection from *Burkholderia pseudomallei*. EBioMedicine. 2021;63:103152. | 33285499 | 10.1016/j.ebiom.2020.103152 |
| **Genus-level: recombination and AMR evolution in *B. multivorans*** | Diaz Caballero J, et al. A genome-wide association analysis reveals a potential role for recombination in the evolution of antimicrobial resistance in *Burkholderia multivorans*. PLoS Pathog. 2018;14(12):e1007453. | 30532201 | 10.1371/journal.ppat.1007453 |
