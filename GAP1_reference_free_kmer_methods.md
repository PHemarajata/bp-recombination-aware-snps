# Gap 1: reference-free and k-mer methods

**Resolved 2026-08-09.** Companion to `SNP_STRATEGY_REVIEW_2026-08.md` and `HANDOFF_research_gaps.md`.

Scope, from the handoff: SKA2 and `ska lo`; PopPUNK/PopPIPE; core-genome fraction and reference choice in *B. pseudomallei*; pangenome tooling.

Sources were read via PubMed Central up to 2026-08-09, then supplemented with PDFs supplied directly that day — Wu et al. 2026, the Verticall preprint, Nandi et al. 2015, Spring-Pearson et al. 2015, De Smet et al. 2015, Chewapreecha et al. 2017, Seng et al. 2024, and the published pggb paper. Those direct reads corrected several conclusions drawn from search alone; each correction is flagged in place and listed at the end. **The pattern is worth noting before relying on anything here: every one of the corrections went from a search-derived claim to a Methods-derived fact, and two of them reversed the original conclusion.**

---

## The short version

**1. PopPIPE is the pipeline you hand-rolled, and it grafts too — but it rescales the graft and refuses to interpret it.**
This is the most consequential finding, and it amends §4 of the main review. That section concluded there was *no published precedent* for grafting subtrees onto a backbone. There is. PopPIPE does exactly this, as a named step, in a peer-reviewed *Microbial Genomics* paper from the Lees/Croucher group. Two things differ from your implementation, and both are the interesting part: PopPIPE **rescales subtree branch lengths onto a single global distance scale** before grafting, which dissolves the unit-mismatch objection; and the authors explicitly state the product "will not maximize the phylogenetic likelihood — it is only intended as a convenient visualization." So the precedent exists, it solves your unit problem, and it comes with the authors' own instruction not to treat the result as inference.

**2. SKA2 is usable for *B. pseudomallei*, but only inside clusters — and the numbers say your clusters are the right size.**
Both SKA papers state plainly that the tools are for within-strain use. Placing *B. pseudomallei* on SKA2's published recall curve (my arithmetic, from Chewapreecha's 324,637 SNPs across 469 genomes) puts species-wide diversity at π ≈ 0.0067 SNPs/site — about 1.3× SKA2's "strain" boundary where recall is ~90%, and roughly **7× below** the species regime where recall collapses to 10–50%. That is a better answer than expected: SKA is not out of range for this organism, it is merely out of range *species-wide*. Per cluster it should be comfortably accurate. Memory arithmetic reaches the same conclusion independently.

**3. `ska map` feeds Gubbins as a first-class, officially supported path — and it is ~190× faster than Snippy.**
Gubbins ships `generate_ska_alignment.py` and bundles SKA2 in its conda package. This is the answer to "does its output feed Gubbins cleanly?" — yes, by design, with real chromosomal coordinates. It also handles multiple replicons, which matters for chromosomes I and II.

**4. Reference choice measurably degrades recombination-corrected results, and there is now a clean quantification of it.**
The `ska lo` paper contains the experiment the handoff asked for, in *S. pneumoniae*: swapping to a reference at 98.52% OrthoANI inflated Snippy's post-Gubbins SNP count by 42%, made the tree "deviate greatly," and collapsed the temporal signal from R = 0.46 to R = 0.25. The reference-free callers barely moved. This is not a *B. pseudomallei* result, but it is a within-species reference swap, and it is the strongest evidence available that reference choice propagates all the way through Gubbins into dating.

**5. Pangenome tooling is a parallel track, not a substitute — and graph references are measured to be *worse* at the one thing you need.**
No gene-cluster pangenome tool can feed Gubbins, because Gubbins needs spatial distribution and their outputs are concatenations without a shared coordinate frame. Keep them for the accessory genome, GWAS and genomic islands, run alongside the phylogeny — exactly what Wu et al. did on the closest comparable dataset. On graph references the evidence is quantitative rather than merely absent: the only head-to-head core-genome comparison, from the tool purpose-built for bacterial pangenome graphs, reports an **~11% loss of recall at core SNPs** and a 20–30× higher error rate than snippy. Graphs win on rare and accessory variants and lose on core SNPs — and core SNPs under a clock are the entire basis of your phylogeny. For pggb specifically, the published benchmark is **500 complete *E. coli* at 41.4 hours and 211 GB**, with sparsification already on, and its data appendix confirms only "assemblies that completely resolved the genome" were used.

**6. The "86% of K96243 is core" figure in the main review is a 2008 microarray result, not a sequencing-era callable fraction.**
It traces to array comparative genomic hybridisation across 94 South East Asian strains. Sequencing-era equivalents land 10–14 points lower — about 76% of the K96243 gene set survives being challenged with 469 genomes — and the fraction erodes further as sample size grows. The review should not leave that number where a reader will take it for a mapping statistic.

**7. Reference bias is the largest controllable error source in mapping-based SNP calling, and *B. pseudomallei* sits in the worst part of the range.**
Across 209 pipelines and ten species, distance-to-reference predicts recall at ρ = −0.94, and the effect is worst for recombinogenic species. A 0.82% divergent within-species reference inflated false-positive SNPs a hundredfold in *Listeria*; *B. pseudomallei* spans **0.73–5.61% divergence from K96243**. Worse, recombination inference is itself reference-dependent — Gubbins-style peaks appear and disappear with the reference. Only one small *B. pseudomallei* study has ever varied the reference, and the field is split between K96243 and 1026b with no bridge. Run against two references and report concordance; that is the published minimum and nobody in this field does it.

**8. Gap 5 is closed.** Nandi et al. 2015 gives an overall per-site **r/m of 7.2** (4.5 / 8.5 / 6 across the three clades, θ/ρ ≈ 1), and confirms that **at least 78% of the K96243 reference (~5.67 Mb) has undergone recombination** — but describes that as "comparable to *S. pneumoniae*," not exceeding it, which is a correction to how the claim usually travels. At r/m = 7.2, *B. pseudomallei* is roughly 26× the *S. aureus* ST239 value the main review quotes.

**9. PopPUNK has already been fitted to 1,391 *B. pseudomallei* genomes**, with published parameters and quality scores (Seng et al. 2024) — retracting an earlier claim in this document that no such application existed. That removes the main practical obstacle to adopting the PopPUNK-based design. The same paper found temporal signal in **only 1 of 10 sub-lineages** despite dense 2015–2018 sampling, and its two ENA accessions turn out to be the second- and third-largest BioProjects in the entire public collection — so roughly 37% of all public Thai genomes are this one nine-hospital study.

**10. Verticall is two tools and only one is safe.** Its distance workflow recovered temporal signal in **76% of 83 real *K. pneumoniae* lineages against Gubbins' 51%** — directly relevant to Gap 4's weak-clock problem — but is O(n²) and timed out at 4,857 genomes. Its alignment workflow scales but under-filters so badly it dated a well-characterised pneumococcal lineage to **1701 instead of 1972**. Use distance per cluster; never use alignment for dating.

---

## 1. PopPUNK and PopPIPE

> McHugh MP, Horsfield ST, von Wachsmann J, Toussaint J, Pettigrew KA, Czarniak E, Evans TJ, Leanord A, Tysall L, Gillespie SH, Templeton KE, Holden MTG, Croucher NJ, Lees JA. Integrated population clustering and genomic epidemiology with PopPIPE. *Microb Genom.* 2025;11(4). PMID 40294103. [10.1099/mgen.0.001404](https://doi.org/10.1099/mgen.0.001404)

> Lees JA, Harris SR, Tonkin-Hill G, Gladstone RA, Lo SW, Weiser JN, Corander J, Bentley SD, Croucher NJ. Fast and flexible bacterial genomic epidemiology with PopPUNK. *Genome Res.* 2019;29(2):304–316. PMID 30679308. [10.1101/gr.241455.118](https://doi.org/10.1101/gr.241455.118)

### The architecture is yours, formalised

PopPIPE v1.1.0 is a Snakemake pipeline. Its default sub-clustering path, in order:

1. Partition assemblies into **PopPUNK** strains. Steps 2–6 then run in parallel per strain.
2. **pp-sketchlib** core and accessory distances within each strain.
3. **RapidNJ** neighbour-joining tree from the core distances.
4. **SKA2** reference-free alignment (`ska align`).
5. **IQ-TREE** maximum-likelihood phylogeny, using the NJ tree as a starting point.
6. **fastbaps** subclusters, in the mode where subclusters are constrained to be partitions of the phylogeny — which by construction eliminates polyphyletic clusters.

The transmission path adds: `ska map` against a within-strain reference → **Gubbins** → **BactDating** → **TransPhylo**.

This is cluster-then-recombination-correct, exactly as you have it, with the clustering done by sketching rather than Mash-plus-judgement and the alignment done reference-free. Their framing of the design logic is worth quoting in substance: partition the population until transmission between clusters is implausible *and* a recent common ancestor exists, then detect recombination inside each partition. That is the same argument Chewapreecha made, arrived at from the tooling side.

### The graft — this changes §4 of the main review

PopPIPE's step 7 is:

> "Create an overall tree by grafting the maximum-likelihood trees for subclusters to their matching nodes, rescaling branch lengths to match the neighbour-joining tree and midpoint rooting maximum-likelihood trees. We note that this tree will not maximize the phylogenetic likelihood — it is only intended as a convenient visualization of the entire dataset, which is compatible with existing tools."

Three things follow.

**The design is published and peer-reviewed.** The main review's §4 statement that no published precedent exists should be corrected. It exists, from the group that wrote PopPUNK, SKA and much of the surrounding literature.

**It solves your unit-mismatch problem, and tells you how.** Your objection — that the backbone and the subtrees carry branch lengths in different units — is real, and PopPIPE's answer is to **rescale the ML subtree branch lengths onto the neighbour-joining core-distance tree**. Every part of the final object then lives on one scale, the pp-sketchlib core distance. Your pipeline grafts recombination-masked ML subtrees onto an unmasked parsnp/FastTree backbone with no rescaling step at all. That is the specific missing piece, and it is a bounded change rather than a redesign.

**The authors still refuse to interpret it.** Even having rescaled, they call it a visualization and note it does not maximise likelihood. So the main review's second recommendation — document the grafted tree as topology-only — is now backed by a published pipeline that builds the same object and applies the same caveat to it. That recommendation gets stronger, not weaker.

### What PopPIPE was actually demonstrated on

616 *S. pneumoniae* genomes. PopPUNK clustering took 2 minutes on four threads; sub-clustering plus visualization a further 28 minutes; the transmission path another 52 minutes. Of 62 inferred strains, **28 had ≥6 members and so were large enough to subcluster**, yielding 101 first-level and 157 second-level subclusters.

Note the scale. 616 genomes at 2.1 Mb is roughly a fiftieth of the sequence volume of 3,000 *B. pseudomallei* at 7.2 Mb. **PopPIPE has not been demonstrated at your scale**, and the paper's own timing shows half the sub-clustering wall-clock went to ML tree inference on the single largest strain (98 samples). With clusters in the hundreds, that step dominates.

### The finding that spills into Gap 2

PopPUNK returned **62 strains** on the same 616 genomes where the original published analysis using BAPS returned **16 sequence clusters** — a roughly fourfold finer partition, from the sketch-based method. Mutual information between the two was 2.49 against 0.53 for a random shuffle, so they agree in structure; PopPUNK simply splits harder.

That is the same shape as your open Gap 2 discrepancy: your Mash clustering gives 61–76 clusters where Wu et al. report 10 and Chewapreecha 19. Sketch-distance clustering splitting several-fold finer than BAPS is **expected behaviour, not evidence of a bug**. It does not make 61–76 correct, but it removes the presumption that it is wrong, and it means comparing your partition against a BAPS/fastbaps partition on the same genomes will show a systematic offset that needs interpreting rather than fixing.

Also relevant to Gap 2: PopPIPE reports that first-level subclusters corresponded more closely to MLST than the top-level strains did (mutual information 3.38 with sequence clusters, 3.74 with sequence types), and that fastbaps run in phylogeny-partition mode eliminates polyphyletic clusters by construction. That last property is worth having and your Mash approach does not guarantee it.

The fastbaps mode PopPIPE uses is worth noting on its own, because it carries a criterion:

> Tonkin-Hill G, Lees JA, Bentley SD, Frost SDW, Corander J. Fast hierarchical Bayesian analysis of population structure. *Nucleic Acids Res.* 2019;47(11):5539–5549. PMID 31076776. [10.1093/nar/gkz361](https://doi.org/10.1093/nar/gkz361)

fastbaps fits an approximate Dirichlet process mixture model, and provides "a method for rapidly partitioning an existing hierarchy in order to maximize the DPM model marginal likelihood, allowing us to split phylogenetic trees into clades and subclades using a population genomic model." That is a **model-based stopping rule for how far to subdivide** — marginal likelihood, not a distance threshold — and it is the second principled answer (alongside iterative-PopPUNK) to the criterion problem your Mash clustering lacks. It clusters datasets 10–100× larger than earlier model-based methods. Full evaluation belongs to Gap 2, but it should not be researched from scratch there.

### iterative-PopPUNK: a principled answer to "how many clusters?"

> Zhao B, Lees JA, Wu H, Yang C, Falush D. Genealogical inference and more flexible sequence clustering using iterative-PopPUNK. *Genome Res.* 2023;33(6):988–998. PMID 37253539. [10.1101/gr.277395.122](https://doi.org/10.1101/gr.277395.122)

This extends PopPUNK to produce **multiple consistent cluster assignments across a range of sequence identities**, building a partially resolved genealogical tree with respect to those clusters so a user can pick the resolution they need. On *E. coli* and *S. pneumoniae* it spans resolutions from phylogroup down to sequence type. Validated on simulated data and seven bacterial species; ships as `PopPUNK_iterate`.

This is a direct, tooled answer to the criterion problem the main review raised — your Mash clustering has no principled size criterion. Chewapreecha's rule (subdivide until within-cluster diversity falls inside Gubbins' detection range) is a *stopping condition*; iterative-PopPUNK is the *machinery* for sweeping resolutions so you can apply that condition rather than guess. The two compose. I have read the abstract and metadata only, not the full text — the resolution-selection details should be checked before relying on them.

### Direct answer to the handoff's question: adopt the design, not the software

The handoff asked whether to adopt PopPIPE wholesale rather than maintain a bespoke Nextflow pipeline. **No — converge on its design instead.** Four reasons, in descending weight:

1. **PopPIPE is Snakemake (v7.8.5), yours is Nextflow.** Adopting wholesale means changing workflow managers, which is a large migration that buys nothing scientific. The scientific content is in the tool choices and their ordering, and that transfers to Nextflow directly.
2. **No pre-built PopPUNK database exists for *Burkholderia*** (below), so the one step that most needs to be defensible is the one you would have to build yourself anyway.
3. **It has not been demonstrated near your scale** — 616 genomes at 2.1 Mb.
4. **It pins Gubbins v3.1.0 and IQ-TREE v2.0.3**, which collides with Gap 3.

What is worth taking wholesale is the sequence of decisions: sketch-based strain partitioning, `ska align` for within-strain phylogeny, `ska map` against a *within-strain* reference for anything needing coordinates, fastbaps constrained to partition the phylogeny, and branch-length rescaling onto a single global scale before any grafting.

### Two blockers on adopting PopPIPE wholesale

**There is no pre-built PopPUNK database for *Burkholderia* — but there is now a published model fit.** Seng et al. 2024 ran PopPUNK v2.6.0 on 1,391 *B. pseudomallei* genomes with `--min-k 15 --max-kmer 31 --max-a-dist 0.53 --K 4 --k-step 2`, reporting density 0.028, transitivity 0.992 and network score 0.8961 (§9b). That is a validated starting point for the one step that most needed judgement, and it substantially lowers the cost of adoption estimated below. The remaining obstacle is only that you must fit and host the database yourself. For the record, the bacpop listing offers 25 species — *Acinetobacter baumannii*, *Bordetella pertussis*, *Campylobacter jejuni*, *Enterococcus faecalis* and *faecium*, *E. coli*, *H. influenzae*, *H. pylori*, *K. pneumoniae*, *L. pneumophila*, *L. monocytogenes*, *M. abscessus*, *M. tuberculosis*, *N. gonorrhoeae*, *N. meningitidis*, *P. aeruginosa*, *S. aureus*, *S. maltophilia*, and seven *Streptococcus* species — and **no *Burkholderia* at all**. You would have to fit your own model, and the PopPIPE paper is explicit that everything downstream depends on the quality of that primary clustering: "we recommend checking the quality of these strain designations before running PopPIPE." Model fitting is the step that needs judgement, and it is exactly the step the pre-built databases normally remove. This is not disqualifying — it is a bounded piece of work — but it is the real cost of adoption and it lands on the part of the pipeline you most want to be defensible.

**A Python-version clash caps the workflow manager, and the published versions are old.** Two separate things here, and it is worth keeping them apart.

The *paper* reports the versions used in the published analysis: Gubbins v3.1.0, IQ-TREE v2.0.3, SKA2 v0.3.9, PopPUNK v2.7.0, fastbaps v1.0.5, Snakemake v7.8.5. The *repository* is looser — `environment.yml` specifies minimums, not hard pins (`gubbins >=3.1.0`, `iqtree >=2.0.3`, `ska2 >=0.4.0`, `poppunk >=2.3.0`, `r-fastbaps >=1.0.5`). So a fresh install resolves to current versions, and my earlier reading that PopPIPE would lock you to an old Gubbins was wrong.

The real constraint is a dependency conflict the file documents in its own comments: **Gubbins caps Python at 3.10, which in turn caps Snakemake at 7.x** ("snakemake 8 would be preferred, requires python 3.11 (clashes with gubbins)"). That is a live maintenance smell rather than a correctness problem.

What survives for Gap 3: because the constraints are minimums, whichever Gubbins you get is whatever conda resolves *today*, which will be on the far side of the v3.4.2/v3.4.3 invariant-site change. So the ascertainment-bias question does not go away by adopting PopPIPE — it just gets answered by the solver instead of by you. Pin it deliberately once Gap 3 concludes.

---

## 2. SKA2 — what it can and cannot do at this divergence

> Derelle R, von Wachsmann J, Mäklin T, Hellewell J, Russell T, Lalvani A, Chindelevitch L, Croucher NJ, Harris SR, Lees JA. Seamless, rapid, and accurate analyses of outbreak genomic data using split-mer analysis. *Genome Res.* 2024;34(10):1661–1673. PMID 39406504. [10.1101/gr.279449.124](https://doi.org/10.1101/gr.279449.124)

### The divergence envelope, which is the whole question

SKA2 splits odd-length k-mers into two flanks around a variable middle base. Matching flanks between samples establishes homology; differing middle bases are SNPs. No alignment, so no soft reference bias (the tendency to call the reference allele at low coverage) and no hard reference bias (SNPs missed in regions absent from the reference).

The cost is that **SNPs closer together than the k-mer length break the flank match and are missed**, and that failure mode worsens with divergence. The authors' measured recall, from simulation on an *S. pneumoniae* backbone:

| Regime | Divergence | Recall |
|---|---|---|
| Within a lineage (clone) | ≲ 0.0005 SNPs/site | **> 99%** |
| Within a strain | ≲ 0.005 SNPs/site | **~ 90%** |
| Across a species | ≳ 0.05 SNPs/site | **10–50%** |

Their recommendation is unambiguous: "we recommend that SKA2 is used only within bacterial strains and, for this purpose, with a short k-mer length."

### Where *B. pseudomallei* falls — my arithmetic, not a published figure

The handoff asks whether SKA2 can handle *B. pseudomallei*-level divergence. No one has published that number, so I derived it. Reproducible in `ska_feasibility_bp.py`.

Chewapreecha et al. mapped 469 globally distributed isolates to K96243 (chromosomes I + II, 7,247,547 bp) and found 324,637 SNPs. That is a segregating-site density of 0.0448 per site. Converting to average pairwise divergence via Watterson's estimator (a₄₆₉ = 6.727):

**π ≈ 0.0067 SNPs/site, or about 99.33% ANI — roughly 48,000 SNPs between two randomly chosen genomes.**

Against the SKA2 landmarks, species-wide *B. pseudomallei* is **1.3× the strain boundary** (~90% recall) and **7.5× below the species regime** where recall collapses. Assuming only 80–90% of the reference is callable moves π to 0.0074–0.0083, which does not change the conclusion.

Three caveats, and they matter:

- Watterson's θ assumes neutrality and panmixia. *B. pseudomallei* has strong clade structure (Nandi et al. 2015, restriction-modification-mediated genetic isolation), and structure typically pushes pairwise π *above* θ_W. **Treat 0.0067 as a lower bound.** Even a generous 0.01 stays 5× below the collapse regime.
- The 469 isolates were deliberately globally balanced across 30 countries, which makes this a fair species-wide estimate — arguably the best available — and specifically *not* subject to the Thailand-dominance problem in the public collection.
- This is an estimate from a published SNP count, not a measurement. See "the cheap experiment" below.

One point in favour of the estimate: those 324,637 SNPs are pre-Gubbins — Chewapreecha ran recombination correction *after* hierBAPS partitioning — so they include recombination-imported differences. For most purposes that would inflate apparent diversity, but for this purpose it is exactly right. What breaks a split-mer match is observed sequence divergence from any cause, not clonal-frame divergence. The unmasked count is the correct input.

**The practical reading.** Species-wide `ska align` on *B. pseudomallei* would be degraded but not destroyed — somewhere in the 80–90% recall band, extrapolating. Per cluster, where within-cluster diversity is one to two orders of magnitude lower, SKA2 sits in the >99% regime. Partitioning first is what makes SKA2 accurate here, and you already partition.

### Memory says the same thing, independently

The `ska align` merged dictionary holds one byte of middle base per sample per split-mer, and the authors note that "the entire intersection of split-mers must always be kept, which leads to large memory use with diverse samples." Extrapolating from their published 240-genome / 3.6 GB figure (calibration factor ≈ 5× over naive byte-counting, in `ska_feasibility_bp.py`):

| Genomes | Est. peak RAM, species-wide | Est. peak RAM, within-cluster |
|---|---|---|
| 100 | ~8 GB | ~4 GB |
| 200 | ~16 GB | ~9 GB |
| 500 | ~43 GB | ~22 GB |
| 1,000 | ~91 GB | — |
| 3,000 | ~300 GB | — |
| 5,728 | ~590 GB | — |

Order-of-magnitude only. But the shape is robust: species-wide `ska align` on the full public collection is not viable on ordinary hardware, per-cluster runs are cheap, and resource arithmetic reproduces the accuracy-based advice. Note that `ska map` avoids this by processing samples one at a time against a reference — the paper flags this as the scalable option for large, diverse sample sets, at the cost of somewhat lower recall.

### `ska map` into Gubbins: supported, validated, and very fast

This is the specific integration question from the handoff, and the answer is clean.

The Gubbins manual ships a helper script and bundles the tool:

> "the alignment can be generated using the Gubbins script `generate_ska_alignment.py`, which creates an alignment using SKA2, which can be installed through `conda install -c bioconda ska2`"

Usage is `generate_ska_alignment.py --reference seq_X.fa --input input.list --out out.aln`.

The SKA2 paper validates the path on 240 *S. pneumoniae* PMEN1 assemblies against the Spn23F reference: alignment built in **56 seconds using 3.6 GB RAM, about 190× faster than running Snippy on all samples (178 minutes)**. Gubbins on that alignment recovered the same major recombination signals as the original short-read-mapping analysis, including the φMM1-2008 prophage and the ICE*Spn*23FST81 mobile element. Exactly one major locus was missed: a gene composed largely of short serine-containing amino-acid repeats. Because that low-complexity repeat runs longer than 63 bases, no split-mer can span it even at the maximum k = 63.

That single miss is the generalisable warning. Split-mer methods have a **structural blind spot at low-complexity repeats longer than k**, and it is not fixable by parameter tuning — 63 is the hard ceiling. Before adopting this path, check whether any *B. pseudomallei* locus you care about has that character. The obvious candidates are the large surface-protein and adhesin genes; *B. pseudomallei* is known for repeat-rich surface antigens, so this deserves a look rather than an assumption.

Two details that matter for you specifically:

- **`ska align` output has no coordinate system.** Its columns are in hash-table order and "do not represent a physical position in the chromosome." It therefore **cannot** go into Gubbins. Only `ska map` output can. This is the same class of error as feeding Gubbins a snp-sites alignment, and it would fail silently — the window scan would run on meaningless spacing. Guard it.
- **Multiple replicons are handled.** The `ska map` implementation includes logic to "keep track of multiple chromosomes." PopPIPE's own description notes SKA2 maps against a reference "so SNPs form correct windows on the physical chromosome." Chromosomes I and II should come through with correct per-replicon coordinates, which is what the main review's sixth recommendation (analyse replicons separately) needs.

### Operational details worth carrying over

- **k-mer size trades off with divergence.** Longer k is more specific and spans more repeats (repeat resolution ~95% → ~98%); shorter k is more sensitive to closely spaced SNPs. The authors recommend short k within strains. Max k is 63. In simulation, SNP recovery was flat from k = 21 to k = 51 and dropped sharply at k = 61.
- **Coverage floor.** At 20× coverage with default settings, sensitivity collapsed (0.93 → 0.43 for *S. pneumoniae*). Running `ska cov` to fit the k-mer coverage model and lowering the minimum count from 5 to 3 restored it to 0.89. If any of your inputs are low-coverage, this is mandatory. Moot for assembly input.
- **Assemblies work directly**, and are ~190× faster than reads. Given 92% of the public collection is draft assemblies, this suits you — though the draft median contig N50 of 133 kb means contig ends will lose split-mers.
- **Incremental addition works.** Filtering split-mers on frequency (`--min-freq 0.8`) preserved SNP counts almost exactly across 288 *S. enterica* genomes added in batches (max difference 13 SNPs out of 16,905) while shrinking files 2–6.4×. Filtering on SNP presence/absence instead **biases pairwise distances downward** and should not be used for anything but final fixed sets. Relevant if you plan to keep adding public genomes.
- **Versions.** The SKA2 paper used v0.3.5; the PopPIPE paper reports v0.3.9 while its `environment.yml` requires `>=0.4.0`; the `ska lo` paper used v0.4. Current bioconda `ska2` is **0.5.1**. Actively maintained, Rust, Apache 2.0. Note that `ska lo` did not exist at v0.3.x, so anything pinned below 0.4 cannot use it.

---

## 3. `ska lo` — worth using, for a reason the handoff did not anticipate

> Derelle R, Madon K, Hellewell J, Rodríguez-Bouza V, Arinaminpathy N, Lalvani A, Croucher NJ, Harris SR, Lees JA, Chindelevitch L. Reference-free variant calling with local graph construction with `ska lo` (SKA). *Mol Biol Evol.* 2025;42(4). PMID 40171940. [10.1093/molbev/msaf077](https://doi.org/10.1093/molbev/msaf077)

`ska lo` ("SKA left over") converts the split-mer file into a coloured De Bruijn graph and traverses it to build "variant groups" — all variant paths between a given entry and exit node. Because its detection span is 2k−1 nucleotides rather than k, it recovers SNPs that split-mers lose to multi-nucleotide polymorphisms and to overlapping variants in dense regions. It also calls indels, which `ska align`/`ska map` cannot, up to at least 5 kb, with **zero false-positive indels** in benchmarking where Snippy's false positives grew with reference distance.

**It does not extend the divergence range.** Stated directly: "ska lo remains unsuitable for the analysis of highly divergent genomes (i.e. at the species level), with sensitivity still lower than that of Snippy and high computational costs associated with large graphs." Their recommendation is to partition first "using MLST schemes or PopPunk," and they point at PopPIPE for doing so. So `ska lo` is a better within-cluster caller, not a route to species-wide analysis.

### The reference-choice experiment — the most transferable result in Gap 1

170 *S. pneumoniae* PMEN2 isolates, called three ways, each put through Gubbins, then root-to-tip dated.

With a **close** reference (670-6B):

| Caller | Raw SNPs | Post-Gubbins SNPs | Root-to-tip R |
|---|---|---|---|
| Snippy | 23,469 | 2,320 | 0.46–0.50 |
| `ska map` | 11,950 | 2,234 | 0.61–0.62 |
| `ska lo` | 17,548 | 2,280 | **0.66** |

1,990 polymorphic positions were shared by all three. Now swap to a **more distant** reference (ATCC 700669, OrthoANI 98.52% against 670-6B — still the same species, a different strain):

| Caller | Post-Gubbins SNPs | Root-to-tip R |
|---|---|---|
| Snippy | **3,291** (+42%) | **0.25–0.29** |
| `ska map` | 2,082 | 0.45 |
| `ska lo` | 2,040 | 0.58 |

Shared positions fell from 1,990 to 1,537. Snippy's tree "deviated greatly" from the close-reference result; the reference-free callers' trees stayed nearly identical across the two references. The authors attribute Snippy's inflation to misalignment against the distant reference — false SNPs that survive Gubbins and then destroy the clock signal.

**Why this should change what you do.** This is the failure mode your pipeline is exposed to. K96243 is a single Thai clinical isolate. Your collection is 54% Thailand but also spans Australia, China, Africa and the Americas, and Nandi et al. showed *B. pseudomallei* clades are genetically isolated by clade-specific restriction-modification systems — so the between-clade distance from K96243 is real, structured, and largest for exactly the Australian genomes that carry the phylogeographic signal you care about. A 98.52% OrthoANI reference swap in *S. pneumoniae* was enough to inflate post-Gubbins SNPs 42% and halve the temporal signal. *B. pseudomallei* species-wide divergence (π ≈ 0.0067, ~99.33% ANI, above) is of the same order.

This is a *S. pneumoniae* result and I am extrapolating; it is not proof about *B. pseudomallei*. But it is a within-species reference swap, it propagates all the way through Gubbins into dating, and Gap 4 already flags weak temporal signal as your likely failure point. Reference bias is a plausible contributor to that, and it is testable cheaply.

### Caveats on `ska lo`

- The missing-data parameter must stay **below 0.5**; above that it emits duplicate/spurious SNPs from high-polymorphism regions. Default is 0.1; the PMEN2 analysis used 0.4.
- SNP positioning accuracy on the reference degrades with variant density, from 100% down to 97.6%. The authors judge this "adequate for analyzing SNP distribution across the genome (e.g. detecting recombination events)" but explicitly recommend **against** using `ska lo` positions to test specific known variants such as resistance SNPs.
- Confident inference is limited to the core genome, as a consequence of the missing-data filter.
- Efficiency on 170 genomes: `ska lo` 34 s / 2.4 GB versus `ska map` 17 s / 7.6 GB. Slower but substantially lighter on memory.

---

## 4. Core-genome fraction and reference choice in *B. pseudomallei*

### The headline: the main review's "86% core" figure is a 2008 microarray result

The main review states, in §3, that "86% of K96243 is core to all strains, 14% variable." That number is real and correctly quoted, but its provenance needs to be in the document, because it is not what a reader will assume it is.

> Sim SH, Yu Y, Lin CH, et al. The core and accessory genomes of *Burkholderia pseudomallei*: implications for human melioidosis. *PLoS Pathog.* 2008;4(10):e1000178. PMID 18927621. [10.1371/journal.ppat.1000178](https://doi.org/10.1371/journal.ppat.1000178)

It is **array comparative genomic hybridisation across 94 South East Asian strains, published in 2008**: 4,619 of 5,369 genes core (86.0%), 750 accessory (14%), with 30.8% of accessory genes falling in genomic islands. Three consequences follow. It measures **gene presence/absence against a fixed probe set**, not base-level callability. It **cannot detect anything absent from K96243**, so it is structurally incapable of seeing the hard reference bias that matters here. And the strain panel is regionally narrow, from a period long predating the current collection.

Citing it as "86% of K96243 is callable when you map a modern collection" would be a category error, and the review is currently one careless sentence away from that reading. The sequencing-era equivalents land **10–14 percentage points lower**.

### The modern numbers, and why they disagree

There is no single core-genome fraction for this organism. The published figures answer different questions and are routinely conflated:

| Source | Figure | What it actually measures |
|---|---|---|
| Sim 2008 (PMID 18927621) | **86%** of K96243 | Gene presence by aCGH, 94 SE Asian strains |
| Lichtenegger 2021 (PMID 33980649) | **75.6%** of K96243 gene set | 4,221 cgMLST targets retained from 5,580 candidates, challenged with 469 genomes |
| **Wu 2026 (PMID 42377320)** | **52.5% of K96243** | **Core-genome alignment of 3,805,619 bp across 554 isolates — an actual base-level callable fraction** |
| Nandi 2015 (PMID 25236617) | **77.8%** of K96243 | Bp core genome estimated at 5.64 Mb, regions common to all Bp strains, 106 strains |
| Spring-Pearson 2015 (PMID 26484663) | **82%** of an average strain | Extended core homolog groups per genome |
| Spring-Pearson 2015 | **~24%** | Strict core (3,278 observed) as a fraction of 13,799 homolog groups |
| Chewapreecha 2017 (PMID 28112723) | **15.7%** | 4,064 core CDS (≥99% presence) of a 25,812-CDS pangenome across 469 isolates |

**The Wu figure is the one to use, and it is much lower than the review currently assumes.** Their Snippy/snippy-core pipeline produced a core-genome alignment of **3,805,619 bp** — 52.5% of the 7,247,547 bp K96243 reference — across 554 isolates. That is a genuine base-level callable fraction from a modern mapping pipeline, which is exactly what was missing, and it is **33 points below the 86% aCGH figure** the review currently cites.

Two things make it more alarming rather than less. Those 554 isolates are from a single region (99.3% from Hainan), so this is a *narrow* collection — a global set of 4,127 would be expected to yield less, not more, and Wu never report the alignment length for their global tree. And it means **roughly half of every genome is invisible to the phylogeny.** Whatever recombination, accessory content or geographic signal lives in the other 47.5% is not being analysed at all.

For calibration, Lichtenegger's cgMLST retained 4,221 of 5,580 candidate targets when challenged with 469 genomes — 75.6% of the candidate set, 72.1% of Holden's 5,855 CDS. That derived percentage is my arithmetic from their counts. Gene-level retention sitting well above base-level callability is expected, since a gene survives if most of it is callable.

**The fraction also erodes as you sample more deeply**, which is directly relevant to a 3,000-genome run:

> Sahl JW, Vazquez AJ, Hall CM, et al. The effects of signal erosion and core genome reduction on the identification of diagnostic markers. *mBio.* 2016;7(5):e00846-16. PMID 27651357. [10.1128/mBio.00846-16](https://doi.org/10.1128/mBio.00846-16)

Against K96243: 298 public genomes gave 2,570 core CDS; 392 *B. pseudomallei* gave **2,339**; adding *B. mallei* to reach 416 genomes dropped it to **1,684**. Species-specific diagnostic markers collapsed from 63 to 22 over the same progression. Expect your core to be smaller than any published figure simply because your n is larger, and report the core alignment length you actually obtain rather than citing someone else's.

### The number that most improves §2 — and it corroborates my estimate

Chewapreecha et al. report per-isolate SNP counts against the K96243 core genome ranging **5,650 to 43,221**. Over the 7,247,547 bp reference that is **0.078% to 0.596% divergence**.

That is a valuable independent check on §2. My Watterson-derived species-wide π was **0.666%**; the maximum observed single-isolate divergence from K96243 is **0.596%**. Those are different quantities — average pairwise diversity versus maximum distance to one particular reference — but they are the same magnitude and mutually consistent, which is about as much corroboration as an estimate of this kind can get.

Placed on SKA2's scale (lineage 0.05%, strain 0.5%, species 5%): **even the single most divergent isolate in a deliberately global 469-genome panel sits at 0.6%, just past the strain boundary and roughly eightfold below the species regime.** Section 2's conclusion holds, now with a published number underneath it rather than only an estimate.

**RESOLVED — the "0.73% to 5.61%" figure is not genome-wide SNP divergence, and §2 stands.**

The paper states that "genetic divergence compared with the K96243 core genome ranged from 0.73 to 5.61%." That upper bound cannot be genome-wide SNP divergence: 43,221 SNPs over 7.25 Mb is 0.596%, an order of magnitude smaller. Reversing the arithmetic to ask what denominator would make the published range self-consistent:

| Endpoint | SNPs | Stated divergence | Implied denominator |
|---|---|---|---|
| Minimum | 5,650 | 0.73% | 773,973 bp |
| Maximum | 43,221 | 5.61% | 770,428 bp |

**Both ends independently imply the same denominator, ~772 kb, agreeing to within 0.5%.** Two unrelated endpoints landing on the same figure is not coincidence, so the divergence percentages are per-isolate SNP counts divided by roughly 772 kb — about 10.7% of K96243, and far too small to be a core genome in the usual sense (Wu's core alignment over 554 isolates is 3.81 Mb). Whatever that 772 kb subset is, the figure is **not** a genome-wide divergence and cannot be compared with SKA2's landmarks.

The number relevant to SKA feasibility is the unambiguous one: **43,221 SNPs over the 7,247,547 bp reference is 0.596% maximum per-isolate divergence.** Section 2's conclusion holds without qualification. What remains genuinely unknown is the length of the core alignment Chewapreecha actually used, which they never report.

Separately, the *lower* bound is worth keeping in view for a different reason: even at 0.73%, the closest isolate to K96243 in a global panel already exceeds the 0.82%-ish threshold at which Pightling measured hundredfold false-positive inflation in *Listeria*.

### Reference choice: the general evidence is damning, and *B. pseudomallei* sits in the danger zone

This is the part of Gap 1 with the largest practical consequence, so it is worth setting out properly.

**The general bacterial literature is unambiguous, and reference divergence is the dominant term.**

> Bush SJ, Foster D, Eyre DW, et al. Genomic diversity affects the accuracy of bacterial single-nucleotide polymorphism-calling pipelines. *GigaScience.* 2020;9(2):giaa007. PMID 32025702. [10.1093/gigascience/giaa007](https://doi.org/10.1093/gigascience/giaa007)

209 SNP-calling pipelines across 254 strains from ten species. Distance-to-reference correlated with **recall at Spearman ρ = −0.94** and with F-score at ρ = −0.72 (simulated) and ρ = −0.83 (real data). The best pipeline against a genome's *own* reference achieved 0.944 errors per Mb; against a divergent reference the best achieved 2.627 errors per Mb — **roughly a 2.8-fold increase in error rate purely from the reference**. Pipeline choice is a second-order effect next to this.

Two of their conclusions transfer directly. The loss is driven by **recall, not precision** — false negatives, sites that simply cannot be called, and "some will be found only within genes unique to the original genome," which is hard reference bias by another name. And the effect is species-dependent in a way that places your organism badly: "especially pronounced for diverse, recombinogenic bacteria such as *Escherichia coli* but less dominant for clonal species such as *Mycobacterium tuberculosis*." For clonal species reference choice has "negligible influence." *B. pseudomallei* is at the recombinogenic extreme of that spectrum, so the *E. coli* regime is the relevant one.

> Valiente-Mullor C, Beamud B, Ansari I, et al. One is not enough: on the effects of reference genome for the mapping and subsequent analyses of short-reads. *PLoS Comput Biol.* 2021;17(1):e1008678. PMID 33503026. [10.1371/journal.pcbi.1008678](https://doi.org/10.1371/journal.pcbi.1008678)

Five species, each mapped against multiple within-species references. Three findings, each worse than the last:

- **Coverage.** The outbreak-matched reference gave 96.7% mapped reads and 97.7% genome coverage; the other references gave median values below 89%. **An eight-point loss of callable genome from a within-species reference swap.**
- **SNP counts.** Against the most distant references of *K. pneumoniae*, *L. pneumophila* and *P. aeruginosa*, SNP counts were "one order of magnitude larger" than against closer ones.
- **Topology.** Normalised Robinson-Foulds distances between trees from different references averaged 6.5–12.4 depending on species, and individual isolates were "placed in different clades" depending on which reference was used.

And the one that should worry this project most: **recombination inference is itself reference-dependent.** In *N. gonorrhoeae*, alignments built against two references "showed at least two clearly observable peaks that were absent when FA 1090 was the reference." That is the Gubbins step changing its answer based on a choice made upstream of it. Their recommendation is explicit — map against multiple references and report whether conclusions are robust to the choice.

> Pightling AW, Petronella N, Pagotto F. Choice of reference sequence and assembler for alignment of *Listeria monocytogenes* short-read sequence data greatly influences rates of error in SNP analyses. *PLoS One.* 2014;9(8):e104579. PMID 25144537. [10.1371/journal.pone.0104579](https://doi.org/10.1371/journal.pone.0104579)

The sharpest single number in this literature. Two real *Listeria* references: one near-identical (~0.000096% distant) and one at **0.82%** — still the same species. False-positive SNPs went from an average of 3.3–3.8 to **218.8–1,477.2**. Two to three orders of magnitude, from a 0.82% divergent within-species reference.

**Now place *B. pseudomallei* on that scale.** Chewapreecha report divergence from the K96243 core genome ranging **0.73% to 5.61%** across their global panel. The *lower bound* of that range is already at Pightling's catastrophic 0.82% threshold, and the upper bound is nearly seven times it. Given the Thailand-versus-Australia structure documented in the main review's sampling audit, the genomes furthest from a Thai clinical reference are precisely the Australian ones that carry the phylogeographic signal the project exists to recover.

### The one *B. pseudomallei* study — and it is smaller than the question deserves

I initially concluded no such study existed. One does, and it is worth reading:

> Webb JR, Mayo M, Rachlin A, Woerle C, Meumann EM, Rigas V, Harrington G, Kaestli M, Currie BJ. Localized *Burkholderia pseudomallei* Genotype Clusters Within Darwin, Northern Territory, Australia. *J Clin Microbiol.* 2022;60(2):e0164821. PMID 35080450. [10.1128/JCM.01648-21](https://doi.org/10.1128/JCM.01648-21)

From the Menzies group. They deliberately varied the reference, with the stated rationale that "a more closely related reference genome would reduce the chance of mismapping and increase the regions in the reference genome against which reads would be mapped." One distant global reference (MSHR1153) versus five sequence-type-matched close references.

The measured effect, on two clinical–environmental pairs: **113 → 136 SNPs** and **0 → 3 SNPs** when moving from the distant to the ST-matched reference. Direction is as predicted — **the distant reference under-calls**, losing roughly 20% of differences at the ~100-SNP scale.

Three caveats keep this from settling the question. It reports no callable fraction, no total SNP counts per alignment, and no tree distances between the six phylogenies. And the authors' own conclusion was that it did not change their epidemiological call: the single-ST approach "did not provide higher genetic resolution" than the Darwin-wide phylogeny. So it establishes direction and rough magnitude at outbreak scale, not the callable-fraction curve you would need for a 3,000-genome phylogeographic study.

### Chewapreecha already used per-cluster references — and the current pipeline apparently does not

The full text was supplied on 2026-08-09. Its Methods contain the single strongest endorsement of the per-cluster-reference recommendation, verbatim:

> "Evolutionary parameters and date of most recent common ancestors were determined for 19 clusters. **For each cluster, closely related reference genomes were chosen for mapping to increase variant calling sensitivity.** Where closely related reference genomes were not available as complete chromosomal contigs, draft reference genomes were created from *de novo* assemblies. One isolate within each of these clusters was selected, assembled and ordered relative to its closest reference using ABACAS v2.5.1 and ACT followed by manual curation. Short reads from all members of each cluster were then mapped against this **lineage-specific reference** using SMALT 0.7.4."

So the field-standard study maps to K96243 only for the *global* tree and population structure, then **re-maps each of its 19 clusters against its own lineage-specific reference** before Gubbins and dating — with the stated rationale being exactly the sensitivity argument in §4. Combined with Verticall's 83 *K. pneumoniae* sublineages (each mapped to its own reference) and Webb 2022, that is three independent groups converging on the same design.

This reframes the recommendation. Using a per-cluster reference is not an improvement to propose — it is **standard practice that the current pipeline appears to omit**. If per-cluster Gubbins is running on alignments mapped to K96243, that is a deviation from the reference study, not an extension of it.

**The core alignment length is confirmed absent.** Having now read the Methods directly: they state only that reads were "mapped against the core genome of *B. pseudomallei* strain K96243 (accession numbers BX571965 and BX571966)" with bases called per Harris et al. and Page et al., that "genetic divergence compared with the K96243 core genome ranged from 0.73 to 5.61%," and that "variants were identified at 324,637 SNPs (range 5,650 to 43,221 sites per isolate)." **No length in bp appears anywhere in the Methods.** The ~772 kb denominator implied by the divergence range therefore remains unexplained, and this is a genuine reporting gap in the paper rather than a retrieval failure.

Two further numbers worth having. Their pan-genome (Roary, 92% BLASTP identity) gave **25,812 CDS with 4,064 core at 99% presence and 21,748 accessory**. And with *B. thailandensis* E264 as outgroup, of 127,421 SNPs across 1,605 shared single-copy core genes, 69,473 (54.5%) separated the two species, **leaving 57,948 to resolve *B. pseudomallei* population structure**.

### What is actually missing

**No study systematically compares K96243 against Australian references across a global collection and reports callable fraction, SNP counts and topology distances.** Two further facts make that gap sharper:

**The field does not agree on a reference — there are at least four in active use.** Chewapreecha 2017 maps 469 genomes to **K96243**; a 2026 North Central Vietnam study (PMID 41662344, [10.1371/journal.pntd.0013945](https://doi.org/10.1371/journal.pntd.0013945)) maps 1,468 genomes to **1026b**; Webb et al. 2022 use **MSHR1153** plus five ST-matched references; Pearson et al. (*PLoS Pathog.* 2020;16(3):e1008298. PMID 32134991. [10.1371/journal.ppat.1008298](https://doi.org/10.1371/journal.ppat.1008298)) use **MSHR1435** for a 130-genome within-host study. No published work bridges these coordinate systems, so SNP counts and distances are not comparable across the literature — which is worth remembering when the review compares your cluster count to Wu's ten or Chewapreecha's nineteen.

**The field's own pipeline paper is silent.** SPANDx (Sarovich & Price, *BMC Res Notes.* 2014;7:618. PMID 25201145. [10.1186/1756-0500-7-618](https://doi.org/10.1186/1756-0500-7-618)) contains no discussion of reference bias and no *Burkholderia* worked example; its benchmarks are *E. coli* and *H. influenzae*. Closest-relative reference selection is widely *practised* in this field — Meumann et al. 2020 switch reference by analysis scope without comment — but it has never been *validated* here.

So: strong general evidence, an organism sitting in the worst part of the range, a well-motivated practice nobody has quantified, and a cheap experiment (§11) that would close it. Valiente-Mullor's recommendation — run against at least two references spanning the diversity of the set and report concordance — is the defensible minimum, and it is what I would adopt regardless of whether the fuller experiment gets done.

### Pan-reference and graph references

Covered in §5. The short answer is no — not recommended and not demonstrated at this scale for bacterial SNP phylogenetics, and no *Burkholderia* graph-reference work exists.

---

## 5. Pangenome tooling

### The answer: complementary, not substitutive

The handoff asked for current status of Panaroo, PPanGGOLiN and pggb. The load-bearing conclusion is a negative one, and it is firm: **no gene-cluster pangenome tool can substitute for reference mapping in recombination-aware SNP phylogenetics**, because the recombination step is the binding constraint and Gubbins explicitly forbids that input. From the Gubbins manual, verbatim:

> "Gubbins will not produce a sensible alignment on concatenations of core genes output by software such as Roary or Panaroo, because it requires information on the spatial distribution of polymorphisms across the genome."

The manual recommends exactly two input routes: Snippy mapping, or `generate_ska_alignment.py` with SKA2. That is the same pair §2 arrived at from the SKA side. Pangenome tooling belongs in a parallel track — accessory genome, gene presence/absence, GWAS, genomic islands — not in the phylogeny path.

The reason is coordinates. Panaroo's `gene_data.csv` carries a scaffold name but **no start/stop/strand**, and `core_gene_alignment.aln` is a concatenation that destroys spatial signal. PPanGGOLiN's `write_genomes --gff` does emit true contig/start/stop/strand for genes, regions of genome plasticity and modules, but it produces no multiple-sequence alignment at all. Neither can feed Gubbins.

**Searching for published evidence that a pangenome or graph approach improves recombination-aware SNP phylogenetics returned nothing peer-reviewed.** The claim appears only as an aspirational clause in the pggb abstract and in two sources that should not be cited: an arXiv preprint (2505.07919, not peer reviewed) and an unfetchable MDPI review. One of those snippets describes PanSN-spec — a sequence *naming convention* — as a recombination-inference tool, which is a good measure of its reliability.

### Current status of the three tools

**Panaroo** — Tonkin-Hill G, et al. Producing polished prokaryotic pangenomes with the Panaroo pipeline. *Genome Biol.* 2020;21:180. PMID 32698896. [10.1186/s13059-020-02090-4](https://doi.org/10.1186/s13059-020-02090-4). Currently **v1.8.0 (2026-07-02)**, actively maintained with four releases in the past year, no algorithmic overhaul since 2020.

Its relevance to you is specific: Panaroo's graph cleaning targets **spurious gene calls at contig ends in fragmented assemblies**, and in the paper's simulations fragmentation was the single largest error source for every competing tool but not for Panaroo. With 92% drafts at median N50 133 kb, that is the failure mode your corpus has. Benchmark anchors: on 413 clonal *M. tuberculosis* genomes competitors inflated the accessory genome ~10×; on 328 *K. pneumoniae* Panaroo recovered 3,372 core genes against Roary's 1,800.

But note what Panaroo's own merge documentation says:

> "The Panaroo algorithm assumes that a dataset is not overly diverse and thus results can be improved by running the algorithm on separate clusters of genomes independently before merging the resulting graphs."

For the organism with the highest reported r/m in bacteria, that is a first-order caveat — and it is the **fourth independent tool in this document telling you to partition first**. Scaling: the paper's largest run is 1,054 genomes; an independent benchmark (PanTA, Le et al., *Genome Biol.* 2024;25:209, PMID 39107817, [10.1186/s13059-024-03362-z](https://doi.org/10.1186/s13059-024-03362-z)) puts Panaroo at ~2.1 h and 11.8 GB for 1,500 *K. pneumoniae*, and users report OOM kills at larger scales. **3,000+ genomes in one run is not demonstrated anywhere.** Panaroo has no replicon concept — graph edges are contig adjacency — so for drafts the chromosome I/II distinction is simply lost.

**PPanGGOLiN** — Gautreau G, et al. PPanGGOLiN: Depicting microbial diversity via a partitioned pangenome graph. *PLoS Comput Biol.* 2020;16(3):e1007732. PMID 32191703. [10.1371/journal.pcbi.1007732](https://doi.org/10.1371/journal.pcbi.1007732) (correction PMID 34890406). Currently **v2.3.0 (2026-03-30)**, pushed 2026-08-07 — the most actively maintained of the three.

Three things make it the better choice than Panaroo *for your specific complementary questions*:

1. **Scale.** Documented at 1,000 strains in 45 min / 14 GB and **20,656 genomes in ~1 day / 120 GB** — an order of magnitude beyond anything shown for Panaroo. Treat the 20k figure cautiously: the independent PanTA benchmark had PPanGGOLiN as the *heaviest* tool at 1,500 genomes (26.3 GB, with OOM at a 32 GB cap), so the two are not reconcilable without matching flags.
2. **`panRGP`** (Bazin A, et al. *Bioinformatics.* 2020;36(Suppl_2):i651–i658. PMID 33381850. [10.1093/bioinformatics/btaa792](https://doi.org/10.1093/bioinformatics/btaa792)) predicts Regions of Genome Plasticity and their insertion spots. Given that ~6% of K96243 is genomic islands and those are the recombination hotspots, this is the single most relevant capability of any tool in this section. Note `panModule` is **preprint only** (bioRxiv 2021, DOI 10.1101/2021.12.06.471380) — cite accordingly.
3. **Replicon handling is sane for complete genomes.** The neighbour graph is built strictly per-contig and contigs carry an `is_circular` attribute, so for the 6.8% of genomes that are complete, chromosomes I and II are never spuriously joined. For drafts, replicon identity is lost as with Panaroo.

There is no PPanGGOLiN V2 journal paper — "PPanGGOLiN V2" exists only as a HAL deposit (hal-04371316, Jan 2024), grey literature. The better 2026 citation for the framework at scale is **Panorama** (Arnoux et al., *PLoS Comput Biol.* 2026;22(7):e1013856, [10.1371/journal.pcbi.1013856](https://doi.org/10.1371/journal.pcbi.1013856)), which applies it across >6,000 genomes including 3,083 *E. coli*.

**pggb** — Garrison E, Guarracino A, Heumos S, et al. Building pangenome graphs. *Nat Methods.* 2024;21(11):2008–2012. PMID 39433878. [10.1038/s41592-024-02430-3](https://doi.org/10.1038/s41592-024-02430-3). The stack is actively developed. Two components have their own papers — **seqwish** (Garrison E, Guarracino A. Unbiased pangenome graphs. *Bioinformatics.* 2023;39(1):btac743. PMID 36448683. [10.1093/bioinformatics/btac743](https://doi.org/10.1093/bioinformatics/btac743)) and **odgi** (PMID 35552372) — while **wfmash has no peer-reviewed paper at all** (cite Zenodo 10.5281/zenodo.6949373; it has also moved to `waveygang/wfmash`) and **smoothxg has neither a paper nor a citation section**.

I went into this expecting the answer to be "promising but unproven." It is worse than that for your specific corpus, and the reasons are concrete enough to state.

**A correction on sourcing before the numbers.** An earlier draft of this section cited figures that came from the **v1 preprint (April 2023)**, not the published paper. The two differ substantially, and the file circulating as `Building_pangenome_graphs.pdf` is in fact v1. Everything below is from the version of record (bioRxiv v2, matching *Nat Methods* 2024;21(11):2008–2012 — abstract and author list confirmed against the PubMed record). Where a number changed, both are shown.

**The paper's own scale claim is "hundreds," not thousands.** The published text says pggb "has proven to be accurate and scalable to hundreds of genomes," and that "even for hundreds of small genomes, PGGB can provide a variation graph within hours." The largest bacterial set benchmarked is **500 *E. coli***, and the published cost is **41.39 hours and 210.87 GB peak RAM** on a 48-thread AMD EPYC 7402P with 378 GB — **with Erdős–Rényi sparsification already enabled** (Table 1 marks that row with an asterisk). That is 1.7 days consuming 56% of a 378 GB machine, which sits awkwardly next to "within hours."

Both cost axes are worse than the v1 numbers I originally quoted (30.3 h and 134.6 GB): runtime is 37% higher and memory 57% higher. The project *documentation* separately suggests "a few thousand bacterial genomes `pggb -x auto [-n 2000]`" — considerably more optimistic than the published benchmark supports.

**Every benchmarked bacterial genome was complete, and this is now explicitly citable.** Published Appendix A.2, verbatim:

> "We downloaded the assemblies from Genbank, considering those that completely resolved the genome. From these, we randomly selected 500 and 50 assemblies."

The same appendix filters *A. thaliana* to five-contig assemblies and *M. musculus* to chromosome-level. Arithmetic confirms it: 2,562,798,947 bp / 500 = 5.13 Mb per genome, a closed *E. coli* genome. **Against a corpus that is 92% drafts, this is the single most disqualifying fact in this section** — and note it appears only in the published version; the v1 preprint has no data appendix at all. It is an inclusion criterion rather than an explicit exclusion, since the paper is silent on draft assemblies either way, but it means the largest bacterial benchmark used 100% closed genomes.

It is compounded by three things from the issue tracker:

- Garrison, on fragmented bacterial input: "**Sequences shorter than the segment size are not multi mapped. They get only the best mapping.**" At the default `-s 5000`, wfmash keeps mappings ≥5×`-s` = 25 kb. Your *median contig N50* of 133 kb clears that, but the long tail of short contigs does not.
- On overlapping contigs from Illumina drafts: "**In PGGB, there is no such method to merge overlapping contigs**" — the reporter got subgraphs floating free of the main graph, and no solution was offered.
- With drafts you also cannot do the `circlator`-style origin rotation that the one real bacterial application (below) performed, and contig order within a genome is unknown, so path structure encodes assembly artefact rather than biology.

**The largest published bacterial graph took 10 days, and pggb itself could not finish it.** nf-core/pangenome (Heumos S, et al. *Bioinformatics.* 2024;40(11):btae609. PMID 39400346. [10.1093/bioinformatics/btae609](https://doi.org/10.1093/bioinformatics/btae609)) built a graph from **2,146 *E. coli*** sequences in **10 days**, noting that "PGGB could not finish within 30 days due to cluster time restrictions." The only downstream analysis was a pangenome growth curve; there was no variant calling, no phylogeny, no recombination analysis. The softcore stayed at ~3 Mb, under 10% of the total pangenome, and the authors attribute part of the remainder to sequencing error and contamination. It reimplements pggb in Nextflow and distributes wfmash across nodes — genuinely relevant to your infrastructure — but it is a compute demonstration, not a population-genetics result.

**The only real bacterial population-genomics application is 130 genomes of a 2.2 Mb organism.** Yang Z, Guarracino A, Biggs PJ, et al. *Front Genet.* 2023;14:1225248. PMID 37636268. [10.3389/fgene.2023.1225248](https://doi.org/10.3389/fgene.2023.1225248) — *N. meningitidis*, another high-recombination species. Useful numbers: 130 genomes cost **73 h and 38.6 GB** (2,787 min and 21.9 GB with `-x auto`, producing an identical graph); the resulting graph was 4.75 Mb across 629,349 nodes, **more than twice a single genome**; and a phylogeny derived from graph similarity recovered clonal complexes but was *less* resolved than a k-mer SNP tree and disagreed with it on two complexes.

That gives an honest extrapolation. Their 130 × 2.2 Mb = 286 Mb of input took 73 h. Your 3,000–5,700 × 7.2 Mb is 21.6–41 Gb — **75 to 140× more sequence, against an all-versus-all alignment that is quadratic in sequence count**. No published work approaches this for any bacterium, and an independent 2026 paper (PanTax, *Genome Res.* 36(2):405–420, PMID 41535070) caps pggb at **10–100 genomes per species** explicitly to manage resources.

**A subtle one that matters more than it looks: `-x auto` assumes panmixia.** Garrison, in the pull request that introduced the sparsification heuristic, notes it "comes with the assumption that the genomes are in something like panmixia. Less sparsification can be tolerated if there is greater population or species structure in the input genomes." *B. pseudomallei* is strongly lineage-structured with restriction-modification-enforced clade boundaries — about as far from panmictic as a bacterial species gets. So the one mechanism that makes pggb tractable at your scale is the mechanism whose stated assumption your organism most clearly violates. This is never flagged as bacterial guidance anywhere.

For accuracy on the mechanism itself: the **published** version uses an Erdős–Rényi **full-connectivity** criterion, P_connected > (1+ε)·lnN/N, implemented as `P_sparse = min(10·ln(n)/n, 1)`, and reports that "10× increase in the number of genomes requires only **44×** increase in runtime—rather than 100×." The giant-component threshold of 1/(N−1) and the "20×" figure were the **v1** formulation and should not be cited. The 44× figure is consistent with the published table's own 0.93 h → 41.39 h.

There is also an **unreconciled contradiction in the maintainers' own advice**. For ~99% ANI bacteria producing "braided" under-aligned graphs, the fix given is to *increase* mappings per sequence, with the warning that otherwise "it will be very difficult to get a meaningful VCF file out of this." For scale, the fix given is `-x auto`, which *decreases* them. Nobody says where the balance sits for a within-species bacterial set.

**Replicon partitioning — a real advantage, with a real cost.** `partition-before-pggb` splits input into communities "which usually correspond to the different chromosomes of the genomes." For a bipartite genome that should cleanly separate chromosomes I and II and split off plasmids, and it is a genuine advantage over Panaroo and PPanGGOLiN. But the documentation's own caveat bites here: partitioning hides rearrangements between communities. In an organism where inter-replicon exchange is a live question, that is a biological signal you would be discarding to gain tractability. `odgi squeeze` can rejoin partitioned graphs if needed.

### The open avenue, and why I would not take it yet

Coordinate-anchored output is real and is a first-class feature, so this is not blocked on principle. `pggb -V 'K96243:1000'` runs `vg deconstruct` against a named reference path (then `vcfbub` to pop nested bubbles and `vcfwave` to decompose complex alleles) and emits **a VCF in that path's coordinate system**. Include K96243 with its two replicons as named paths and you get true chromosome I and II coordinates — exactly what a recombination scanner needs.

Four things stop me recommending it:

1. **Accessory sequence has no reference coordinate.** Anything the reference path does not traverse can only appear as an insertion allele anchored to a flanking reference base — a 30 kb genomic island collapses to a single VCF record at a single position. For *B. pseudomallei*, where the genomic islands *are* the recombination hotspots, the graph's advantage evaporates in exactly the region of interest.
2. **An accuracy floor around 0.97 — weaker than I first argued, but still a floor.** I originally cited SNV F-scores of 0.947 and 0.937 against MUMmer4. Those are the **v1 preprint** values. The **published** figures are **0.977863 (50 *E. coli*) and 0.967453 (500 *E. coli*)**, so the discordance is roughly 2–3%, not 5–6%. That materially weakens this particular objection and I am flagging it rather than quietly restating it. It does not eliminate it: a few percent discordance still propagates into recombination inference, and recombination detectors are specifically sensitive to *clustered* false positives, which is exactly the error mode local mis-alignment in repeat-rich regions produces. But if this were the only objection, it would not carry the argument. The resource and assembly-quality points do.
3. **You would end up rebuilding the same object.** Gubbins needs a full-length alignment with invariant sites. Reconstituting that from a decomposed VCF plus the reference path gets you approximately the core-genome SNP alignment that reference mapping hands you directly, at two to three orders of magnitude more compute.
4. **Known normalisation bugs.** The pggb script itself carries a `#TODO: remove "bcftools annotate" when vcfwave will be bug-free` with workarounds for missing `TYPE` fields and variants lacking ALT alleles.

**No published source says pggb is unsuitable for bacteria** — the maintainers' position is the opposite, and I looked. The negative case above has to be argued from scaling arithmetic, the complete-genomes-only benchmark, and the issue tracker, not cited to an authority. But it is strong enough that I would not spend the compute. If a graph approach is wanted for the *accessory* questions, `odgi untangle` and `odgi position` offer reference-relative segmentation without going through VCF at all, and may fit better than the variant-calling route.

Worth noting for completeness: **Minigraph-Cactus is reference-based**, needing a backbone assembly, which is why at least one user with fragmented input reported preferring it to pggb (Hickey G, et al. *Nat Biotechnol.* 2024;42(4):663–673. PMID 37165083. [10.1038/s41587-023-01793-w](https://doi.org/10.1038/s41587-023-01793-w)). It has no published bacterial application — the paper covers 90 human haplotypes and *Drosophila*.

### Graph references as a replacement for K96243: no, and there is now a number

The handoff's third question was whether a pan-reference or graph reference is now recommended. The answer is no, and unusually for this document the negative is backed by a direct measurement rather than only by absence.

**The one head-to-head core-genome SNP comparison shows the graph losing.**

> Colquhoun RM, Hall MB, Lima L, Roberts LW, Malone KM, Hunt M, Letcher B, Hawkey J, George S, Pankhurst L, Iqbal Z. Pandora: nucleotide-resolution bacterial pan-genomics with reference graphs. *Genome Biol.* 2021;22:267. PMID 34521456. [10.1186/s13059-021-02473-1](https://doi.org/10.1186/s13059-021-02473-1)

Pandora is the tool purpose-built for exactly this — a bacterial pangenome reference graph with nucleotide-resolution genotyping, built from 578 *E. coli* genomes. Its advantage is real but specific: for rare variants present in 2–5 of 20 isolates it recovered 7,200–24,500 more SNPs than snippy, SAMtools, medaka and nanopolish, with pan-variant recall 7–15 points higher, and its recall stayed near 90% across phylogroups where single references showed phylogroup bias.

But the paper reports an **~11% loss of recall at core SNPs**, and Pandora's error rate is 0.2–0.3% against snippy's 0.01%. Core SNPs under a molecular clock are exactly and only what your phylogeny is built from. **The one thing a graph reference is measured to do worse is the one thing you need it for.** Note also that only 20 isolates were genotyped, so this is not a population-scale demonstration either.

**The largest bacterial graph reference ever published did not use it for phylogeny.** Canalda-Baltrons et al. (*Nat Commun.* 2025. PMID 41315227. [10.1038/s41467-025-65779-9](https://doi.org/10.1038/s41467-025-65779-9)) built a minigraph reference from 859 long-read *M. tuberculosis* assemblies and genotyped 41,134 Illumina isolates against it — genuinely population scale. Their phylogenetic SNPs were nonetheless called by mapping to H37Rv, a single linear reference. Their advocacy is scoped to structural variant detection, and even there graph recall was *lower* than short-read manta (0.34 versus 0.42).

**The authoritative reviews decline to make the claim.** Eizenga et al. (*Annu Rev Genomics Hum Genet.* 2020. PMID 32453966. [10.1146/annurev-genom-120219-080406](https://doi.org/10.1146/annurev-genom-120219-080406)) say of graphs that "it is unclear if they will replace linear reference genomes," and all their variant-calling accuracy evidence is human. Sherman & Salzberg (*Nat Rev Genet.* 2020. PMID 32034321. [10.1038/s41576-020-0210-7](https://doi.org/10.1038/s41576-020-0210-7)) document graph *harms*, with accuracy declining once more than roughly 8–12% of known variants are incorporated.

**Public-health guidance does not mention graph references at all.** The PulseNet International vision paper (Nadon C, et al. *Euro Surveill.* 2017;22(23):30544. PMID 28662764. [10.2807/1560-7917.ES.2017.22.23.30544](https://doi.org/10.2807/1560-7917.ES.2017.22.23.30544)) explicitly names the problem — "the SNP approach is highly discriminatory but sensitive to the selection of the reference" — and resolves it by standardising on wgMLST, not graphs. For a methods review, that is arguably the strongest single data point: the community that most needs reference-independence went to allele calling instead.

**And the enthusiasm rests on human numbers that do not transfer.** The Human Pangenome Reference Consortium draft (Liao WW, et al. *Nature.* 2023;617:312–324. PMID 37165242. [10.1038/s41586-023-05896-x](https://doi.org/10.1038/s41586-023-05896-x)) reduced small-variant discovery errors by 34% and doubled structural variant detection from 47 phased diploid assemblies. Those are the figures everyone cites. They come from a diploid, low-diversity, recombining genome with a consortium, a versioned citable reference, a stable coordinate system and held-out truth sets. **No bacterial species has any of those four things.** *B. pseudomallei* is haploid, bipartite, at the recombinogenic extreme, with an open pangenome roughly three times its core — a materially harder case that nobody has attempted.

There is **no graph or pan-reference work anywhere in the genus *Burkholderia***, and no benchmark anywhere comparing graph against single-reference on bacterial *tree topology* accuracy.

### *Burkholderia*-specific pangenome numbers

> Spring-Pearson SM, Stone JK, Doyle A, et al. Pangenome analysis of *Burkholderia pseudomallei*: genome evolution preserves gene order despite high recombination rates. *PLoS One.* 2015;10(10):e0140274. PMID 26484663. [10.1371/journal.pone.0140274](https://doi.org/10.1371/journal.pone.0140274)

From 37 isolates: the pangenome is **open**, adding ~**136 new genes per additional genome** against a total of 13,799 homolog groups and ~5,726 per strain; ~**5.8% of the genome is genomic islands**. The model fit is the interesting part — **96% of the genome recombines at very low rates and 4% recombines readily**. That is a strong, quantitative version of the "recombination is spatially localised" claim, and it explains the paper's central paradox that gene order stays conserved despite the highest r/m in bacteria.

**The core-genome discrepancy is resolved.** The paper reports both observed and extrapolated values, and earlier automated reads conflated them. Verbatim: "After sequencing 37 genomes, the extended core consisted of 4,736 HGs and the strict core genome consisted of 3,278 HGs." Those are the **observed** counts. The 2,798 ± 59 and 4,568 ± 16 figures are **asymptotic estimates** from 100 permutations of sequencing order, following Tettelin's method — what the core is projected to converge to as more genomes are added. Both are correct answers to different questions. Use the observed counts when describing these 37 genomes and the asymptotes when projecting; never mix them.

That 96/4 split is worth carrying into Gap 3's masking discussion. It implies a well-defined minority of the genome drives the recombination signal, which is exactly the premise of a masked-region BED.

> Holden MTG, Titball RW, Peacock SJ, et al. Genomic plasticity of the causative agent of melioidosis, *Burkholderia pseudomallei*. *Proc Natl Acad Sci USA.* 2004;101(39):14240–5. PMID 15377794. [10.1073/pnas.0403302101](https://doi.org/10.1073/pnas.0403302101)

The original K96243 paper, and the primary source for replicon compartmentalisation: chromosome I (4.07 Mb) carries core metabolism and cell growth; chromosome II (3.17 Mb) carries accessory adaptation and survival functions; the large chromosome has greater gene-order conservation and more orthologues, indicating **distinct evolutionary origins** for the two replicons. 16 genomic islands, 6.1% of the genome, variably present and entirely absent from clonal *B. mallei*. This is the citation the main review's §3 "Chromosome I and II are not interchangeable" subsection was missing.

Also new, and it should be added to the main review's dataset comparisons:

> Seng R, Chomkatekaew C, Tandhavanant S, Saiprom N, Phunpang R, Thaipadungpanit J, Batty EM, Day NPJ, Chantratita W, West TE, Thomson NR, Parkhill J, Chewapreecha C, Chantratita N. Genetic diversity, determinants, and dissemination of *Burkholderia pseudomallei* lineages implicated in melioidosis in Northeast Thailand. *Nat Commun.* 2024;15(1):5699. PMID 38972886. [10.1038/s41467-024-50067-9](https://doi.org/10.1038/s41467-024-50067-9)

**1,391 isolates from nine hospitals, 2015–2018 — "the most densely sampled collection to date."** Three dominant lineages, each with a unique gene set, and the finding that **recombination drives lineage-specific gene flow**, with lineage-specific genes upregulated under environmental conditions in two of three lineages. Author list overlaps heavily with Chewapreecha 2017 (Chewapreecha, Parkhill, Thomson).

Three reasons this matters beyond the pangenome question. It is **independent corroboration of Nandi's clade-specific recombination** from a sample three times larger. It reports environmental drivers of dispersal — terrain slope, altitude, river direction — which is a non-phylogenetic source of geographic signal worth knowing about before Gap 4. And it is almost certainly a large component of the 2015–2019 Thai peak documented in the main review's sampling audit, which means the audit's pseudo-replication concern and this paper's sampling are the same phenomenon viewed from two sides. Methods software unverified; full text not retrieved.

### Precedent for the complementary architecture

Wu et al. 2026 (PMID 42377320), the closest published comparator at ~4,127 genomes, did exactly what this section recommends: core-genome SNP phylogenies **from recombination-masked alignments** for the tree, and **separately** a pan-genome analysis that "confirmed chromosomal functional compartmentalization of the bipartite genome" plus a gene presence/absence GWAS. Mapping-plus-masking for phylogeny, pangenome for the accessory layer, run in parallel rather than substituted. Their specific software is unverified — the full text is paywalled — but the architecture is visible from the abstract, and it is the one to copy.

---

## 6. Verticall — benchmarks now read, and the recommendation needs splitting in two

The preprint was supplied in full on 2026-08-09. The main review recommends evaluating Verticall on the strength of its abstract, which says it "showed comparable or superior performance to the established tools Gubbins and ClonalFrameML." The per-dataset results tell a sharper story: **Verticall is two tools, they fail in opposite regimes, and only one of them should go near a dating analysis.**

Version described is **v0.4.2** (Zenodo 10.5281/zenodo.19687935); the alignment-tree benchmarks used v0.4.1. Comparators were Snippy v4.6.0 pseudoalignments, IQ-TREE v2.3.6, Gubbins v3.4 with `--filter-percentage 100`, ClonalFrameML v1.13. Every program got 32 threads, 375 GB RAM and one week.

### What completed and what did not

| Dataset | ClonalFrameML | Gubbins | Verticall alignment | Verticall distance |
|---|---|---|---|---|
| *S. pneumoniae* PMEN1, n=154 | 4.5 GB / 1.79 h | 0.7 GB / 0.09 h | 0.3 GB / 0.01 h | 0.3 GB / 1.09 h |
| *S. enterica* Typhi H58, n=4,857 | **OOM >375 GB** | 73.5 GB / 69.73 h | 0.5 GB / 0.44 h | **timeout >168 h** |
| *E. coli* species-wide, n=193 | 20.4 GB / 13.96 h | 5.2 GB / 1.52 h | 1.0 GB / 0.02 h | 0.9 GB / 3.09 h |
| *Klebsiella* genus-wide, n=511 | 153.8 GB / 34.6 h | **timeout >168 h** | 1.0 GB / 0.07 h | 1.3 GB / 26.38 h |

Two failures matter for you. **Verticall's distance workflow is O(n²) and timed out at 4,857 genomes.** And for the genus-wide *Klebsiella* set, tree-building on the Verticall-alignment output also timed out, so only unfiltered, ClonalFrameML and Verticall-distance produced trees there. Verticall is not immune to scale — it just fails somewhere different from Gubbins.

### The accuracy result that should govern the decision

**Verticall alignment systematically under-filters.** On PMEN1 it masked only 560 blocks across 154 genomes (median 2 per genome) where Gubbins predicted 2,601 events (median 17) and ClonalFrameML 2,569. Significant residual recombination remained in its output (PHI *p* = 0, χ² *p* = 0), whereas Gubbins' output showed none (PHI *p* = 0.27, χ² *p* = 0.058).

That propagates straight into dating, and the consequence is severe:

| Method (PMEN1) | Root-to-tip R² | Substitution rate (per year) | Root date |
|---|---|---|---|
| Unfiltered | 0.15 | — | — |
| ClonalFrameML | 0.43 | — | — |
| Gubbins | 0.51 | 2.63 [2.25–2.99] | 1974 [1970–1977] |
| **Verticall distance** | **0.51** | 1.96 [1.65–2.30] | **1970 [1964–1975]** |
| **Verticall alignment** | **0.17** | 1.05 [0.71–1.49] | **1701 [1186–1915]** |

The published reference value (Didelot et al. via Gubbins) is 3.09 substitutions/year with a root of 1972. Verticall distance lands on 1970 — excellent agreement. **Verticall alignment returns a root date of 1701, off by nearly 270 years**, and recovers no more temporal signal than doing no filtering at all. The authors attribute this to "insufficient filtering."

### The result that makes it genuinely attractive for you

Across **83 real *K. pneumoniae* clonal sublineages of 19–838 genomes each** — the closest published analogue to per-cluster *B. pseudomallei* work — BactDating convergence rates were:

| Workflow | Sublineages with recovered temporal signal |
|---|---|
| **Verticall distance** | **63 / 83 (75.9%)** |
| Gubbins | 42 / 83 (50.6%) |
| Verticall alignment | 39 / 83 (47.0%) |

**Verticall distance recovered temporal signal in three-quarters of lineages where Gubbins managed half.** Agreement with Gubbins where both worked was good for substitution rates (ICC 0.87) and moderate for root dates (ICC 0.51). And counter-intuitively, *more* genomes helped: larger sublineages had significantly higher odds of convergence (OR = 10, 95% CI 1.71–58.31, *p* = 0.0105), while nucleotide divergence was not a significant predictor in any model.

Given that Gap 4 expects weak temporal signal from this collection — half the calibration mass in 2015–2019 — a method that raises dating convergence from 51% to 76% on real lineages is the most directly relevant result in this document.

### The authors' own verdict

> "While we consider Gubbins the gold-standard for detection of recombination within clonal lineages, for large datasets of thousands of genomes (where Gubbins fails to complete in a reasonable time frame), or analyses that extend beyond a single lineage such as species-wide or genus-wide variation, Verticall provides a useful solution… the distance-based workflow (Verticall distance) showed superior performance… and is therefore **recommended in most cases**. However, for large datasets, the pairwise distance-tree approach becomes inefficient… and Verticall's alignment-based approach is needed. **Results with Verticall alignment are generally not as reliable as Verticall distance.**"

### What I would actually do

**Use Verticall distance per cluster, alongside Gubbins, and judge on dating convergence.** At your cluster sizes (roughly 100–500) it is affordable — 511 *Klebsiella* took 26.4 h and 1.3 GB — and it is the exact use case where it beat Gubbins 76% to 51%. Fold it into the §11 experiment as a fourth arm.

**Do not use Verticall alignment for anything you intend to date.** A 270-year root-date error on a well-characterised dataset is disqualifying, and the under-filtering that causes it will be worse, not better, in an organism with r/m = 7.2.

**Do not expect either to solve the backbone.** The distance workflow won't reach 3,000+ genomes, and the alignment workflow's tree-building timed out on the one genus-wide dataset tested. The main review's hope that Verticall might rescue the between-cluster level is not supported.

Two incidental findings worth stealing. Their QC thresholds for a comparable task were **N50 ≥ 15 kb, ≤ 1,000 contigs, ≤ 100 assembly-graph dead ends** — usefully permissive next to your median N50 of 133 kb. And for lineages above 200 genomes they downsampled with **Treemmer v0.3**, constrained to keep ≥200 samples plus at least one per unique combination of K locus, O locus, country and year. That is a concrete, citable subsampling protocol for Gap 4, where the equivalent constraint would be country and collection year.

Most usefully of all: they mapped **each sublineage to its own reference genome**, chosen per lineage (34 from a hybrid-assembled collection, the rest picked from RefSeq with Bactinspector v0.1.3). That is the per-cluster-reference design §4 and §11 recommend, applied at scale across 83 lineages by an independent group.

---

## 7. How this interacts with the rest of the toolkit

Gap 1 does not compete with the Verticall recommendation, because the two operate at different pipeline stages:

- **SKA replaces the variant-calling step** (mapping to K96243 → `ska map`), feeding a recombination detector downstream.
- **Verticall replaces the recombination-detection step** (Gubbins → Verticall), consuming assemblies directly.

They are composable in principle but not in the obvious way. Verticall's alignment-tree workflow does its own all-versus-reference comparison and masks horizontal regions itself, so it does not want a SKA pseudo-alignment as input — it wants assemblies. So the realistic choices are `ska map` → Gubbins (validated, supported, fast) *or* Verticall on assemblies (broader diversity range, preprint-stage, developer-run benchmarks only).

The relevant contrast: SKA's constraint is *divergence* and Verticall's selling point is *tolerating divergence*. Since §2 puts *B. pseudomallei* only modestly past SKA2's strain boundary, and since you already partition, the divergence argument for Verticall is weaker inside clusters than it looks species-wide. I had expected Verticall's advantage to show up on the **backbone**, at the between-cluster level where Gubbins is documented to fail — but §6 shows that hope is not supported: the distance workflow will not reach 3,000+ genomes and the alignment workflow's tree-building timed out on the only genus-wide dataset tested. Verticall's real advantage is *within* clusters, on dating convergence.

One shared constraint worth noting: Verticall needs assemblies with reasonable N50, and so does SKA when run on assemblies. With 92% drafts at median contig N50 133 kb, both lose split-mers or alignment blocks at contig ends, and both are affected the same way. That makes assembly quality a shared upstream filter rather than a discriminator between them.

---

## 8. Wu et al. 2026 methods, now read — and they settle two questions in other gaps

The full text arrived after the rest of this document was written. It is worth its own section because two lines in its Methods resolve open items the review had flagged as substantive puzzles.

**Their pipeline, for the record.** Illumina NovaSeq 6000; assembly by SOAPdenovo2 v2.04 / SPAdes / AbySS integrated with CISA, gap-filled with GapCloser v1.12, contigs <500 bp discarded (50–173 contigs, N50 101.6–455.0 kb). SNP calling by **Snippy v3.2-dev in contig mode** on SPAdes assemblies, then **snippy-core**, then **Gubbins v2.4.1**. Tree by **RAxML v8.2.12 under GTRGAMMA**, 100 rapid bootstraps. Variant thresholds: minimum coverage 10, minimum variant fraction 0.9, minimum variant quality 100. Pangenome by **Prokka v1.13 + Roary v3.12.0** at 95% BLASTP, core defined as ≥99% presence. GWAS by **Scoary v1.6.16**, re-run with **pyseer** using a phylogeny-aware linear mixed model and kinship matrix. Genomes at BioProject **PRJNA1059167**.

### The ten clusters were imposed, not discovered — Gap 2's central puzzle dissolves

The main review treats "10 clusters versus your 61–76" as a discrepancy large enough to need explaining. It does not need explaining. Verbatim from their Methods:

> "pairwise SNP distances were calculated from the Gubbins-filtered recombination-masked core-genome alignment, and agglomerative hierarchical clustering was performed in SciPy using average linkage (UPGMA); flat clusters were defined with fcluster (criterion = "maxclust", t = 10), and cluster stability was assessed by 100 bootstrap resamplings of SNP sites."

`fcluster(criterion="maxclust", t=10)` means **"return exactly ten clusters."** The number ten is a parameter the authors chose, not a result the data produced. There is no model selection, no stopping rule, no marginal likelihood — just UPGMA on a distance matrix cut at a preset height.

The cluster sizes confirm it. Their ten clusters run 285, 309, 311, 337, 395, 396, 424, 429, 496 and 583 — a **maximum-to-minimum ratio of 2.0×**. Real bacterial population structure is strongly skewed, with a few large lineages and a long tail of small ones; PopPUNK on 616 pneumococci gave 62 strains of wildly unequal size, and Chewapreecha's hierBAPS gave 19. A ten-way split with every cluster within a factor of two of every other is the signature of a fixed-*k* cut through a dendrogram, not of biology.

**So the review's third recommendation should be restated.** It currently says to compare your partition against "the 10 clusters reported by Wu et al." That comparison is close to meaningless: Wu's ten clusters and your 61–76 are not competing estimates of the same quantity, because Wu never estimated it. The genuine comparators are Chewapreecha's 19 hierBAPS groups and whatever fastbaps or iterative-PopPUNK produce on your data. Wu's clusters remain useful as *labels* for describing global structure — Cluster 1 shared between China and Thailand, Cluster 5 predominantly Australian — but not as a target cluster count.

### They kept constant sites and skipped ascertainment correction — Gap 3 has its precedent

Also verbatim:

> "The input alignment was the Gubbins-filtered recombination-masked core-genome alignment retaining constant sites, and therefore SNP-only ascertainment-bias correction was not applied."

Gap 3 flags IQ-TREE `+ASC` on a SNP alignment as a live correctness risk. This is the published precedent for the clean way out: **feed the tree builder the full-length masked alignment with invariant sites retained, and the ascertainment problem does not arise.** No constant-site counts to supply, no version-dependent Gubbins invariant-site handling to get right, no `+ASC` at all. It costs alignment size and tree-building time; it buys the elimination of an entire class of error. Gap 3 should evaluate this against the `+ASC`-with-correct-counts route rather than assuming the latter.

### Three caveats on the paper itself

**The reference genome for SNP calling is never stated.** Snippy requires one, but the Methods name K96243 (given as GCF_000959285.1) only for pangenome and GWAS gene mapping. The phylogeny's reference is left to inference. Given §4, that omission is not a small one — and the accession cited is not K96243's usual one (GCA/GCF_000011545.1), which is worth checking if you intend to reproduce their coordinates.

**Their tool versions are old.** Gubbins v2.4.1 against a current v3.4.3, and Snippy v3.2-dev against a current v4.6.0. Roary rather than Panaroo, which matters given §5 on fragmented-assembly error. Their genomes are drafts of 50–173 contigs, exactly the case Panaroo was built for.

**They acknowledge the sampling problem the review identified independently**, which is worth citing as corroboration: "public databases are heavily skewed towards Australia and Thailand. Thus, this sampling bias can artificially inflate the apparent clustering and ST distribution, and the inferred global landscape should be interpreted cautiously." They also note the post-2018 submission surge reflects sequencing capacity, not incidence. That is the same argument as the review's §1, from the authors of the largest comparable dataset.

---

## 9. Gap 5 is closed — r/m = 7.2, and the 78% claim is confirmed

Nandi et al. 2015 was supplied in full on 2026-08-09. **Page 132 contains both numbers Gap 5 was chasing**, from a primary source, and they are quotable.

> Nandi T, Holden MTG, Didelot X, Mehershahi K, Boddey JA, Beacham I, Peak I, Harting J, Baybayan P, Guo Y, Wang S, How LC, Sim B, Essex-Lopresti A, Sarkar-Tyson M, Nelson M, Smither S, Ong C, Aw LT, Hoon CH, Michell S, Studholme DJ, Titball R, Chen SL, Parkhill J, Tan P. *Burkholderia pseudomallei* sequencing identifies genomic clades with distinct recombination, accessory, and epigenetic profiles. *Genome Res.* 2015;25(1):129–141. PMID 25236617. [10.1101/gr.177543.114](https://doi.org/10.1101/gr.177543.114)

### The r/m value

Verbatim from page 132:

> "We computed recombination/mutation (r/m) values, corresponding to the ratio of rates at which substitutions are introduced by recombination and mutation, across the entire population. **The overall per site r/m ratio was 7.2.**"

And per clade, from ClonalFrame on a reduced 5.6 Mb core genome with mobile elements excluded:

> "For all three clades, the ratio of mutation rate (theta) to recombination rate (rho) was close to one, suggesting that recombination and mutation both happen at approximately the same rates. Recombination was also found to introduce more substitutions than mutation (**r/m = 4.5 in Clade A, r/m = 8.5 in Clade B, and r/m = 6 in Clade C**), with the highest impact observed in Clade B."

| Quantity | Value |
|---|---|
| **Overall per-site r/m, whole population** | **7.2** |
| Clade A r/m | 4.5 |
| Clade B r/m | 8.5 |
| Clade C r/m | 6 |
| θ/ρ, all three clades | ≈ 1 |

This is a genuine genome-wide r/m from ClonalFrame, and it is directly comparable with the figures the main review quotes from Didelot & Parkhill — where *S. aureus* ST239 had **r/m = 0.28**. ***B. pseudomallei* at r/m = 7.2 is roughly 26× that.** That comparison is now legitimate to make, where the Pearson 2009 seven-locus ratio never was.

### The 78% claim is confirmed — and so is a core-genome size

Also verbatim from page 132:

> "Based upon these data, we estimate that **at least 78% of the BpK96243 reference genome (~5.67 Mb) has undergone recombination**, a level comparable to *S. pneumoniae*, a highly recombinogenic species (74K/85K R-SNPs for Bp; 50K/57K R-SNPs for *S. pneumoniae*)."

The handoff's unverified claim is therefore **correct as stated**, with one important correction to how it is usually paraphrased. Nandi describe this as **"a level comparable to *S. pneumoniae*"**, not as exceeding it. The "more than twice *S. pneumoniae*" claim comes from Pearson 2009 and is a seven-locus MLST ratio. **The two should not be merged.** At the whole-genome level *B. pseudomallei* looks comparable to pneumococcus; at MLST loci it looks much worse. If the review states both, state them as what they are.

Page 130 also gives another core-genome figure for §4's table: the Bp core genome, defined as regions common to all Bp strains, has an **estimated size of 5.64 Mb** — 77.8% of K96243, and reassuringly close to the Lichtenegger cgMLST retention of 75.6%.

### This also resolves the tension with Spring-Pearson

I flagged Nandi's 78% as being in apparent conflict with Spring-Pearson's model of 96% of the genome recombining rarely and 4% readily. **They are compatible, and together they are more informative than either alone.** Nandi measure how much of the reference has *ever* been inside a recombination tract across a population — 78%. Spring-Pearson model the *rate* at which each part recombines — nearly all of it rarely, a small fraction constantly. Most of the genome has been hit at some point; a small minority is hit continually. Nandi's own tract statistics support this: 2,373 events with tract lengths from 3 bp to 71 kb, median ~5 kb, concentrated in 1,630 identifiable high-recombination protein-coding genes (897 on chromosome I, 733 on chromosome II).

**For Gap 3's masking question that combination is the useful one.** A masked-region BED should target the 4% that recombines readily — and Nandi hand you a candidate list of 1,630 genes plus the enriched loci they name (the TTSS3 Type III secretion cluster, the TFP8 Type IVB pilus cluster).

### Two more findings worth carrying

**Recombination is significantly higher on chromosome II than chromosome I** (P < 2.2 × 10⁻¹⁶, Mann-Whitney U), matching the direction of their lineage-SNP density result. That is independent quantitative support for the main review's sixth recommendation to analyse the replicons separately.

**Inter-clade gene flow is small but non-zero.** "On average, ~5% of each genome from a given clade was found to have originated from another clade and approximately another 7% from a source not present in our data set." So clade isolation is strong but leaky, and roughly 7% of each genome comes from somewhere unsampled entirely — which is worth remembering before any strong claim about clade boundaries.

---

### The older MLST-locus framing, and why it is a different number

> Pearson T, Giffard P, Beckstrom-Sternberg S, Auerbach R, Hornstra H, Tuanyok A, Price EP, et al. Phylogeographic reconstruction of a bacterial species with high levels of lateral gene transfer. *BMC Biol.* 2009;7:78. PMID 19922616. [10.1186/1741-7007-7-78](https://doi.org/10.1186/1741-7007-7-78)

Verified against the primary record: the relative contribution of homologous recombination versus mutation in *B. pseudomallei* is **more than twice that of *S. pneumoniae***, and is **"the highest value yet reported in bacteria."**

**This is not the same quantity as Nandi's r/m = 7.2, and the two must not be merged.** It is a comparison "at seven housekeeping genes for eleven bacterial species" — an MLST-locus ratio, computed in 2009, not a genome-wide r/m from a recombination-aware method. It is a real, citable primary source for the *qualitative* claim that *B. pseudomallei* recombines heavily. It is **not** the figure to set against the *S. aureus* ST239 value of r/m = 0.28 that the main review quotes from Didelot & Parkhill — Nandi's 7.2 is.

Note too that the two primary sources differ in emphasis. Pearson says *B. pseudomallei* exceeds *S. pneumoniae* by more than twofold **at MLST loci**; Nandi call the **genome-wide** level "comparable to" *S. pneumoniae*. Both are defensible; report each with its scope attached rather than picking the more dramatic one.

Two other things in that paper are worth pulling into the main review, because both predate Chewapreecha and neither is currently cited. Pearson et al. proposed **an Australian origin with a single introduction into Southeast Asia during a recent glacial period**, and found population separation along **Wallace's Line** — the same biogeographic boundary seen in plants and animals. That is an independent, earlier line of evidence for the conclusion the main review attributes to Chewapreecha 2017, derived from >1,700 isolates at seven loci plus 43 whole genomes and >14,000 SNPs. Two independent methods reaching the same answer is a stronger footing for the Australian-reservoir hypothesis than the review currently reflects.

A second, more directly operational figure:

> *Genomic diversity of Burkholderia pseudomallei in Ceará, Brazil.* **mSphere.** 2021;6(1):e01259-20. PMID 33536328. [10.1128/mSphere.01259-20](https://doi.org/10.1128/mSphere.01259-20)

Of 31,594 core SNPs identified, **59% were attributed to recombination**. That is the sharpest single number available for how much of the SNP signal masking removes in this organism.

### The *J Clin Microbiol* homoplasy paper — read, with two corrections

> De Smet B, Sarovich DS, Price EP, Mayo M, Theobald V, Kham C, Heng S, Thong P, Holden MTG, Parkhill J, Peacock SJ, Spratt BG, Jacobs JA, Vandamme P, Currie BJ. Whole-genome sequencing confirms that *Burkholderia pseudomallei* multilocus sequence types common to both Cambodia and Australia are due to homoplasy. *J Clin Microbiol.* 2015;53(1):323–326. [10.1128/JCM.02574-14](https://doi.org/10.1128/JCM.02574-14)

**Correction 1: it did not run Gubbins on individual monophyletic groups.** The handoff describes it that way; the paper does not. It is a **four-isolate** study — two Cambodian (CAM41, SHCH2430) and two Australian (MSHR282, MSHR4004) sharing ST105 and ST849 — analysed with SPANDx v2.3 against **K96243**, with additional reference genomes brought in as simulated Illumina reads via ART. It identified **84,839 core genome SNPs** and ran Gubbins once, with default parameters.

**Correction 2: the 13.5% figure is internally inconsistent in the paper.** Verbatim: "GATK filtering or gubbins analysis removed 37,213 (44%) or 24,216 (13.5%) SNPs, respectively." The first pair checks out — 37,213 / 84,839 = 43.9%. The second does not: **24,216 / 84,839 = 28.5%, not 13.5%.** One of the two values in that parenthesis is wrong and the paper gives no way to tell which. **Cite the count, not the percentage**, and note the discrepancy if it matters.

What the paper does establish cleanly is more useful anyway. Neither filtering approach "alter[ed] geographic attribution of strains or tree topology" — with only four isolates that is weak evidence, but it points the same way as Webb 2022: recombination filtering and reference choice moved the numbers without moving the conclusion. And its substantive finding is a caution for Gap 2: shared sequence types between continents were **homoplasy**, arising from "both mutation and multiple recombination events over considerable evolutionary time rather than from recent recombination," with eBURST judged "unreliable for inferring the geographic origin of STs" because of high recombination. Any clustering built on MLST-scale similarity in this organism will make that mistake.

---

## 9b. Seng et al. 2024 — PopPUNK *has* been run on *B. pseudomallei*, and I was wrong

> Seng R, Chomkatekaew C, Tandhavanant S, Saiprom N, Phunpang R, Thaipadungpanit J, Batty EM, Day NPJ, Chantratita W, West TE, Thomson NR, Parkhill J, Chewapreecha C, Chantratita N. Genetic diversity, determinants, and dissemination of *Burkholderia pseudomallei* lineages implicated in melioidosis in Northeast Thailand. *Nat Commun.* 2024;15:5699. PMID 38972886. [10.1038/s41467-024-50067-9](https://doi.org/10.1038/s41467-024-50067-9)

**Correction to this document.** Section 2 and the caveats list both state that there is no published application of PopPUNK to *Burkholderia*. **That is wrong.** Seng et al. ran **PopPUNK v2.6.0 on 1,391 *B. pseudomallei* genomes**, and published the fitted model parameters. My PubMed searches missed it because the paper is not indexed under the tool name; it took reading the Methods to find. Treat the earlier statement as retracted — and treat it as a caution about how much weight to put on any "no published application of X" claim in this document.

### The PopPUNK recipe, which you can reuse directly

Verbatim from their Methods:

> "PopPUNK v.2.6.0 was run on 1391 assembled genomes. To define the core and accessory distance between each pair of isolates, the assemblies were hashed at different k-mers. Several kmer comparison options (--k-step) and model fit options (--K) were tested to identify the parameters with the optimal fit based on density, transitivity and network scores. The optimal population model was fit using command line `poppunk --fit-model ---output <database> --min-k 15 --max-kmer 31 --max-a-dist 0.53 --K 4 --k-step 2`. **The model had a density of 0.028, a transitivity of 0.992, and a network score of 0.8961.**"

That removes the main obstacle §1 identified to adopting the PopPUNK/PopPIPE design — there is no pre-built *Burkholderia* database, but there is now a published, parameterised model fit with reported quality scores to start from. A transitivity of 0.992 is high, meaning the strain network is close to cleanly separable.

### Their pipeline, which is the closest published match to yours

| Step | Tool |
|---|---|
| QC | Kraken v1.1.1, CheckM v1.12.2, FastANI v1.31 |
| Assembly | Velvet v1.2.10 + scaffolding |
| Mapping | **Snippy v4.6.0**, min 10 reads and frequency ≥ 0.9 |
| Population-wide reference | **K96243** (BX571965, BX571966) |
| Population structure | **PopPUNK v2.6.0** |
| Core SNP alignment | **snp-sites v2.5.1, genomic islands masked** |
| Trees | **IQ-TREE v2.0.3**, best-fit **TVM + F + ASC + R6**, 1,000 bootstraps |
| Sub-lineages | **rhierbaps v1.1.4** |
| Recombination | **Gubbins v3.3.1** |
| Dating | **BactDating v1.1.1**, strict clock, 3 chains ≥ 10⁸ iterations |
| Pan-genome | Prokka v1.14.5 + **Panaroo v1.3.3**, sensitive mode, 92% identity |
| Ancestral states | phytools v1.9.16 `make.simmap` |

Their stated reason for K96243 is worth quoting because it is the opposite of a bias-aware choice: it was selected "due to its origin in northeast Thailand, aligning with the geographical focus of our study." Sensible for a Thai study; the reverse of what §4 implies you need for a globally distributed collection.

### Three findings that change other gaps

**They used `+ASC`, where Wu retained constant sites.** Their best-fit model was TVM + F + **ASC** + R6 on a snp-sites alignment; Wu explicitly kept invariant sites and skipped ascertainment correction. **Gap 3 therefore has two published precedents in the same organism doing opposite things**, both from credible groups. That makes the choice a real methodological decision to argue rather than a bug to fix — and it means whichever route you take, there is a citation for it.

**Per-lineage references again, and they built one from scratch.** For lineage 1 they used K96243; for **lineage 2** they picked representative isolate 27035_8#57, ran **MinION long-read sequencing**, and built a **Unicycler v0.4.8 hybrid assembly** to serve as the mapping reference; for **lineage 3** they took the best de novo assembly and ordered its contigs against K96243 with **ABACAS v1.3.1**. This is the fourth independent group doing per-cluster references, and the first to sequence a new long-read reference specifically to get one. Note the escalation: they judged it worth generating new data rather than mapping lineage 2 to K96243.

**The temporal-signal result is the most sobering number I have found for Gap 4.** Verbatim:

> "Notably, the temporal signals were discernable at the sub-lineage level rather than the broader lineage level. Among the 10 sub-lineages, **only one sub-lineage (lineage 1.3) exhibited a positive correlation in their clock signals.**"

This is 1,391 genomes, densely sampled from nine hospitals over a tight 2015–2018 window, with recombination removed and date-randomisation applied — and **one sub-lineage in ten yielded usable temporal signal.** Set alongside Chewapreecha dating only five of 19 clusters with marginal date-randomisation, and Verticall's 51% Gubbins convergence across 83 *Klebsiella* lineages, the pattern is consistent: dating *B. pseudomallei* mostly fails, and it fails at the lineage level while occasionally working one level down. Gap 4's instruction to "be prepared for the answer to be no" should be upgraded from a caution to the base case.

### And a direct link to the sampling audit

Their data availability statement gives ENA study accessions **PRJEB25606 and PRJEB35787**. Those are **the second- and third-largest BioProjects in the entire public collection** per the main review's audit — 682 and 582 genomes, 1,264 together, matching their 1,265 clinical isolates almost exactly.

So the audit's pseudo-replication concern now has a name. Roughly **37% of all Thai genomes in the public collection come from this single nine-hospital study covering 2015–2018 in northeast Thailand** — which also explains the 2015–2019 spike holding half the dated collection. When the review says effective independent sampling is far below *n*, this is the largest single reason. It also means any analysis treating those 1,264 genomes as independent draws from "Thailand" is really analysing one hospital network over four years.

Two smaller findings worth carrying. They compared tree topologies across core-genome SNP, cgMLST, MLST and PopPUNK using **treespace v1.14.3**, and found core SNP and cgMLST bootstrap trees clustered together while **MLST trees dispersed widely** — independent support for the main review's scepticism about MLST-scale resolution, and consistent with De Smet's homoplasy result. And their subsampling for ancestral state reconstruction used **n = 15 isolates per province, permuted 1,000 times**, with provinces below that threshold excluded — the identical design Chewapreecha used at country level, now applied at province level.

---

## 9c. The 19 hierBAPS clusters, tabulated — and a diagnostic you can run today

Chewapreecha's Supplementary Data 1 gives per-isolate cluster assignments for all 469 genomes. I have tabulated it as `chewapreecha_hierbaps_clusters_2026-08-09.csv`. It answers the Gap 2 question more directly than any argument in this document.

### What a real partition looks like

| | Chewapreecha hierBAPS | Wu `fcluster(t=10)` |
|---|---|---|
| Clusters | 19 named + a 34-isolate "bin" | 10 |
| Size range | **4 – 137** | 285 – 583 |
| Median | 17 | ~397 |
| **Max / min ratio** | **34.2×** | **2.0×** |
| Unassigned | 7.2% binned | none |

**A model-based partition of this organism produces a 34-fold size range and throws 7% of isolates into a bin.** An imposed ten-way cut produces clusters all within a factor of two of each other and assigns everything. That is the difference between finding structure and imposing it, and it confirms §8's reading of Wu from the opposite direction.

**The diagnostic follows immediately.** Compute the size distribution of your own 61–76 Mash clusters. If they are roughly even, your clustering is imposing structure regardless of how the count compares to anyone else's. If they are strongly skewed — a few large clusters, a long tail of small ones, some isolates hard to place — you are finding it. **That check costs one line of code and is more informative than comparing your cluster count to 19 or to 10.**

### Clusters are almost perfectly geographic — and that has consequences

Nineteen of the twenty labels are **≥90% one geographic region**. Group 1 is **100% Australasia** (Australia 129, PNG 4, Fiji 2); every other named group is **100% Asia** except Group 19, which is the Africa/Americas cluster (Chad, Puerto Rico, Brazil) behind the slave-trade inference. There is **no Asia/Australasia mixing at cluster level at all** — Wallace's Line appears in the clustering itself, not just in the phylogeography built on top of it.

Two consequences. Geographic subsampling and cluster-stratified subsampling are close to the same operation in this organism, so doing both is not double-counting but nor is it double protection. And since the public collection is 54% Thai, the Thailand-dominated clusters (Groups 6, 9, 10, 11, 14–18) are exactly the ones that will inflate, while Group 1 and Group 19 stay comparatively fixed.

### Group 1 is the problem child, and it is the one you care about

Group 1 holds **137 isolates, 29% of the entire collection**, spans 1966–2012, contains **98 distinct sequence types**, and is 100% Australasian. The paper states it "contained the highest amount of diversity for each isolate and **could not be further sub-clustered**." It was also **not among the clusters that could be dated**.

So the largest cluster is simultaneously the one that resisted subdivision, the one that failed to date, and the one carrying the Australian-reservoir signal the whole phylogeographic argument depends on. In your collection Australia is 586 genomes. Expect the same behaviour at four times the size, and plan for it: this is where a partition-then-Gubbins design is most likely to break, and where Verticall distance (§6) is most worth trying, since its advantage is precisely at diversity levels where Gubbins struggles.

### Only 14.5% of the collection was actually dateable

Clock-like behaviour across both chromosomes was found in Groups 4, 5, 6, 7, 8 and the American subset of Group 19. Group 5 (n=4) was dropped. That leaves **five clusters and 68 isolates — 14.5% of 469** — underpinning every date in the reference study.

The clusters that failed include the largest (Group 1, n=137), the deepest-sampled Singapore group (Group 3, n=38, spanning 1935–2005), and the Thailand-heavy Groups 10, 17 and 18. Note what *did* work: small clusters with tight temporal windows, plus the Americas group. This is a third independent confirmation of the §9b pattern — dating this organism mostly fails, and it fails on the big, diverse, epidemiologically interesting clusters.

### MLST holds up better than expected, except where it matters

Only **14 of 211 sequence types (6.6%) appear in more than one population cluster**, and the largest offender is the placeholder "STunknown". Excluding that, thirteen real STs cross cluster boundaries. So MLST is not broadly misleading about population structure here — which sits awkwardly against Seng's `treespace` result that MLST trees disperse widely, and is worth stating as a nuance rather than a contradiction: MLST assigns clusters tolerably but resolves *topology* poorly.

The exceptions are precise and instructive. **ST105 appears in both Group 1 (Australasia) and Group 15 (Thailand/Cambodia/Vietnam)** — which is exactly the intercontinental homoplasy case De Smet et al. sequenced four genomes to demonstrate (§9). Chewapreecha's clustering shows the same thing independently. ST51 spans three clusters; ST46, ST163, ST205, ST211 and ST422 each span two. If any of those STs are used as a grouping variable anywhere in your pipeline, they are pooling genuinely distinct lineages.

One last figure for calibration: **95.5% of these 469 isolates have a collection year**, against 61.8% of the public collection. The reference study's temporal analyses ran on far better-annotated data than you have, and still dated only five clusters.

---

## 10. A through-line worth noticing

Five independent tools and pipelines, developed by different groups for different purposes, all arrive at the same instruction:

| Source | What it says |
|---|---|
| Gubbins manual | "populations be subdivided into smaller groups of less diverse samples" |
| SKA2 (Derelle 2024) | "used only within bacterial strains" |
| `ska lo` (Derelle 2025) | "partitioning WGS datasets into low-genomic-diversity groups" |
| Panaroo merge docs | "running the algorithm on separate clusters of genomes independently before merging" |
| PopPIPE (McHugh 2025) | the entire pipeline architecture |

Plus Chewapreecha's hierBAPS-then-Gubbins design, and Lees' rebuttal to Sakoparnig quoted in the main review. **Partition-first is not a workaround for tool limitations; it is the consensus design of the field.** The main review's third recommendation — replace ad-hoc Mash clustering with a criterion tied to the next tool — is therefore the highest-leverage change available, because every downstream tool's validity depends on it. Gap 1's contribution is to supply two published mechanisms for setting that criterion (iterative-PopPUNK's resolution sweep and fastbaps' DPM marginal likelihood) where previously there was only Chewapreecha's stopping rule and no tooling for it.

---

## 11. The cheap experiment that closes most of this

Everything above is literature plus arithmetic. One run on one existing cluster converts most of it into measurement, and it answers questions from Gaps 2, 3 and 4 at the same time. Pick a mid-sized cluster you already have — 100–300 genomes, ideally one with both Thai and non-Thai members.

**Step 0, free, do it first.** Read the maximum within-cluster Mash distance off the distance matrix you already computed. Mash distance approximates 1 − ANI, which is the same quantity as π. If your within-cluster maximum is below 0.005, you are inside SKA2's ~90%-recall strain regime and everything below is expected to work. If it is above 0.01, your clusters are too coarse for SKA regardless of anything else. **You already own this measurement and it decides whether the rest is worth running.**

**Step 1 — calibrate resources.** `ska build` then `ska align` on the cluster; record peak RSS and wall-clock. That single number replaces the whole estimated memory table in §2 and tells you whether species-wide is as far out of reach as I think it is.

**Step 2 — compare callers on a close reference.** Build the same cluster three ways: your existing mapping pipeline, `ska map`, and `ska lo`, all against a *within-cluster* representative. Run each through Gubbins. Compare post-Gubbins SNP counts, the number of polymorphic positions shared by all three, tree distance, and root-to-tip R².

**Step 3 — the reference-swap test, which is the one that matters.** Repeat step 2 against K96243 instead. You now have the `ska lo` PMEN2 experiment replicated on your own organism. If your mapping pipeline's post-Gubbins SNP count inflates and its root-to-tip R² drops when you move from a within-cluster reference to K96243, while the reference-free callers hold steady, then reference bias is contributing to the weak temporal signal Gap 4 anticipates — and the fix is a per-cluster reference, which is cheap.

That third step is the highest-value single run in this document. It is a direct test of a specific, plausible failure in the current pipeline, it uses data you already have, and either outcome is informative: a null result retires reference bias as a concern and strengthens everything you conclude afterwards. It also fills a genuine hole in the literature — per §4, **nobody has ever quantified reference bias in this organism.**

**Step 4, optional but strategically valuable — add 1026b as a third reference.** The field is split between K96243 (Chewapreecha and most of the Thai literature) and 1026b (the 2026 Vietnam study, 1,468 genomes), with no published bridge. Running the same cluster against both would let you state how much of the difference between those two literatures is reference artefact. That is a small addition to a run you are doing anyway and it is publishable on its own.

Two guards while doing this. `ska align` output must never reach Gubbins — only `ska map` carries coordinates, and the failure would be silent. And pin the Gubbins version deliberately once Gap 3 resolves, rather than letting the conda solver choose across runs and quietly change your ascertainment-bias handling mid-project.

---

## What I would change

Ordered by expected value, and scoped to Gap 1 — these slot into the main review's §5 list rather than replacing it.

**First, read the within-cluster Mash distances you already have.** Free, immediate, and it decides whether any of the SKA work is worth doing. Below 0.005 you are in the safe regime; above 0.01 your clusters are too coarse for split-mer methods regardless.

**Second, make three corrections to the main review.** (a) §4's claim that the backbone-plus-grafted-subtrees design has no published precedent is wrong — PopPIPE is that precedent, and it supplies the missing piece: rescale subtree branch lengths onto a single global distance scale before grafting. Adopt the rescaling; keep the topology-only caveat, which PopPIPE's authors apply to their own equivalent output. (b) §3's "86% of K96243 is core" needs its provenance attached — it is 2008 array CGH on 94 SE Asian strains, and sequencing-era figures are 10–14 points lower. (c) Add that Chewapreecha 2017 never reports its callable fraction, thresholds, masking, or post-Gubbins alignment length, which means their core alignment is not reproducible from the paper.

**Third, adopt "at least two references, report concordance" as standing practice, then run the reference-swap test (§11, step 3).** The standing practice is Valiente-Mullor's explicit recommendation and costs one extra mapping run; nobody in the *B. pseudomallei* field currently does it. The test itself — one cluster, two or three references, three callers, Gubbins on each, compare root-to-tip R² — is the highest-value single experiment in Gap 1. Reference divergence is the largest controllable error term in this kind of analysis, *B. pseudomallei* spans a range where the effect is documented to be severe in other species, and recombination inference is itself reference-sensitive, which puts the Gubbins step directly downstream of an unvalidated choice. A null result is as useful as a positive one.

**Fourth, switch per-cluster alignment generation to `generate_ska_alignment.py`.** It is the officially supported Gubbins input path, roughly two orders of magnitude faster than mapping, removes reference bias from the variant-calling step, and handles both replicons. The guard is absolute: `ska map`, never `ska align`, into Gubbins. Use `ska lo` instead of `ska map` if the reference-swap test shows it gives a stronger clock signal, as it did on PMEN2.

**Fifth, treat PopPIPE as a specification to converge on rather than software to adopt wholesale.** The architecture is validated and matches yours; the obstacles are real but bounded — no *Burkholderia* PopPUNK database exists, it has only been demonstrated at 616 genomes of a 2.1 Mb organism, and it pins Gubbins v3.1.0 and IQ-TREE v2.0.3. Take the design decisions (sketch-based partitioning, phylogeny-constrained fastbaps subclustering, branch-length rescaling before grafting, `ska map` into Gubbins) without inheriting the pins.

**Sixth, hand iterative-PopPUNK and fastbaps to Gap 2 rather than re-deriving them.** Both supply a principled criterion for how far to subdivide — a resolution sweep and a DPM marginal-likelihood partition of an existing hierarchy respectively — which is precisely what the current Mash clustering lacks. And note the calibration point: PopPUNK split 616 pneumococcal genomes into 62 strains where BAPS gave 16, so sketch-based methods splitting several-fold finer than BAPS is expected. That partly defuses the 61–76 versus 10 discrepancy before Gap 2 starts.

**Seventh, keep pangenome analysis but move it out of the phylogeny path.** Run it as a parallel track answering different questions — accessory content, replicon compartmentalisation, gene presence/absence GWAS, genomic islands via `panRGP` — exactly as Wu et al. did on the closest comparable dataset. Do not attempt to feed any of it to Gubbins. For tool choice: PPanGGOLiN for scale and RGP detection, Panaroo if annotation-error correction on fragmented drafts is the priority; they are complementary rather than competing.

**Eighth, do not spend compute on a pangenome graph or a graph reference.** This is the one place I would spend a recommendation on *not* doing something, because it is the item on the Gap 1 list most likely to look attractive and cost months. The decisive number is Pandora's ~11% loss of recall at core SNPs: graph references demonstrably help with rare and accessory variants and demonstrably hurt on the core SNPs your clock runs on. Around that sit the practical obstacles — the published pggb bacterial ceiling of **500 complete *E. coli* at 41.4 h and 211 GB with sparsification already enabled** (and 2,146 in a Nextflow reimplementation that took ten days while pggb itself timed out at thirty), a data appendix confirming only completely-resolved assemblies were used, and sparsification that assumes panmixia this organism violates. Your 3,000–5,700 target is six to eleven times beyond the largest published bacterial benchmark, extrapolating a 44×-per-10× scaling law well past any tested point. Note also that PulseNet's answer to reference sensitivity was wgMLST, not graphs, and that pggb performs no recombination analysis anywhere in the paper — the abstract's claim that graphs let you "detect recombination events" is delegated entirely to a citation. Revisit if a *Burkholderia* pan-reference consortium and truth set appear, or if the long-read fraction rises well above today's 9%.

**Eighth, add Spring-Pearson's 96%/4% recombination model to Gap 3's masking work.** If 96% of the genome recombines at very low rates and 4% recombines readily, then a masked-region BED is tractable in principle and the genomic islands are the place to start. Gap 3 asks whether a published masked-region BED exists for K96243; this is the quantitative argument for building one if it does not.

---

## What could not be verified

- **No *B. pseudomallei* π or ANI figure from a primary source.** The π ≈ 0.0067 SNPs/site figure central to §2 is **my arithmetic** from Chewapreecha's published SNP count via Watterson's estimator, not a published measurement. The neutrality and panmixia assumptions are both violated by this organism. It is a lower bound and should be replaced by a direct measurement from the existing Mash matrix.
- ~~No published application of SKA, PopPUNK or PopPIPE to *Burkholderia*.~~ **WRONG, retracted 2026-08-09.** Seng et al. 2024 ran **PopPUNK v2.6.0 on 1,391 *B. pseudomallei* genomes** and published the fitted model parameters (§9b). My PubMed searches missed it because the paper is not indexed under the tool name — it took reading the Methods. **This is the most instructive error in the document**: a keyword search for "tool X + organism Y" will not find tool use buried in a Methods section, so every remaining "no published application of X" claim here should be read as "no application found by keyword search," which is a much weaker statement. SKA and PopPIPE specifically remain unlocated for *Burkholderia*, with that caveat attached.
- **Chewapreecha 2017 does not report its callable fraction of K96243.** This was confirmed absent from the Methods, not merely unretrieved. The single most-cited *B. pseudomallei* population-genomic study does not publish what proportion of the reference it retained as core, its coverage or mapping-quality thresholds, its repeat masking, or its post-Gubbins SNP count and alignment length. That is worth stating plainly in the main review, because it means nobody can reproduce their core alignment.
- **Chewapreecha 2017 never reports the length of its core alignment.** The "0.73–5.61% divergence" figures reverse-engineer to a consistent ~772 kb denominator (§4), which is too small to be a core genome as normally defined and conflicts with Wu's 3.81 Mb. So the *ratio* is internally consistent but what it is a ratio *of* is still unidentified. This does not affect §2, which uses the unambiguous per-isolate SNP counts, but it does mean their core alignment cannot be reconstructed.
- **The reference-bias evidence base is strong but not *B. pseudomallei*.** Bush 2020, Valiente-Mullor 2021, Pightling 2014 and Yoshimura 2019 are all solid, peer-reviewed and directly on point, but none covers this organism. The one *B. pseudomallei* study that varied the reference (Webb 2022) is a two-pair, outbreak-scale comparison reporting neither callable fraction nor tree distances. Transferring the magnitude of the effect is inference.
- **Some benchmark figures cited here were read from tables via automated extraction**, which is the weakest link in the retrieval chain — specifically Webb's per-pair SNP counts, Valiente-Mullor's Robinson-Foulds values, and Yoshimura's precision figures. Verify these against the papers before they go into a manuscript.
- ~~Wu et al. 2026 methods remain unread.~~ **Resolved** — PDF supplied 2026-08-09 and read in full; see §8. Their core alignment is 3,805,619 bp (52.5% of K96243), their ten clusters were imposed via `fcluster(t=10)`, and they retained constant sites rather than applying ascertainment correction. The one thing still missing from their paper is the reference genome used for SNP calling, which they never state.
- **Tooling was partially blocked during this research.** A permission classifier denied several PubMed MCP metadata and full-text calls and some PMC/Europe PMC fetches during the background searches, and PubMed began serving CAPTCHAs. Q2 and Q3 of the core-genome research were therefore searched less exhaustively than intended. The "no *B. pseudomallei* reference-comparison study exists" conclusion is a negative from a bounded search, not an exhaustive proof.
- **PopPIPE has not been demonstrated at this scale.** 616 genomes of a 2.1 Mb organism, versus ~3,000 genomes at 7.2 Mb. The published timings do not extrapolate safely, and the paper itself notes ML tree inference on the largest single strain consumed half the sub-clustering wall-clock.
- **SKA2's own documentation gives no quantitative divergence guidance.** The recall-versus-divergence numbers exist only in the paper's Figure 2; the docs say only that smaller k is more sensitive and less specific. Anyone reading the docs alone would not learn the strain-level limit.
- **iterative-PopPUNK read at abstract and metadata level only**, not full text. The resolution-selection mechanism should be checked before it is relied on.
- **The memory table in §2 is extrapolation**, calibrated against a single published data point (240 genomes / 3.6 GB) with a crude ~5× correction factor. Order-of-magnitude only.
- **The reference-bias quantification is *S. pneumoniae*, not *B. pseudomallei*.** The 98.52% OrthoANI swap that inflated post-Gubbins SNPs 42% and halved the temporal signal is a real, well-controlled result, but transferring it to *B. pseudomallei* is inference, not evidence. The reference-swap experiment is how to settle it.
- **A genome-wide r/m for *B. pseudomallei* is still not located.** Pearson 2009 is verified but is a seven-locus MLST ratio, not comparable to modern genome-wide r/m estimates. Gap 5 should stay open on this point.
- **The ≥78%-of-K96243-recombined claim remains unverified**, and is in apparent tension with Spring-Pearson's 96%/4% model. Do not cite either as settled until they are reconciled.
- **No benchmark comparing Panaroo, Roary, PIRATE and PEPPAN on high-diversity or highly recombinant species appears to exist.** Searched by title, keyword and field tags. The nearest items compare clustering *criteria* across 125 pangenomes (Manzano-Morales et al., *Genome Biol.* 2023;24:250, PMID 37904249) or measure resources only (PanTA). This is a genuine gap in the literature, not a gap in the search.
- **No published application of any pangenome or graph tool to recombination-aware SNP phylogenetics in bacteria.** The only supporting claims trace to a non-peer-reviewed arXiv preprint and an unfetchable review, one of which misdescribes a naming convention as a recombination tool. The pggb `-V` → coordinate-anchored VCF → recombination-scan route is coherent but unproven, and the objection that all-versus-all alignment over ~700,000 draft contigs is impractical is **my reasoning, not a citation** — no published source addresses it either way.
- **No bacterial pggb build above 2,146 genomes** is confirmed in a peer-reviewed paper, and **no benchmark anywhere** compares graph against single-reference on bacterial *tree topology* accuracy. Pandora's ~11% core-SNP recall penalty is the closest available proxy and comes from a 20-isolate genotyping run, not a population-scale phylogeny.
- ~~Spring-Pearson's core-genome counts are ambiguous.~~ **Resolved 2026-08-09.** 3,278 strict / 4,736 extended are the observed counts across 37 genomes; 2,798 ± 59 and 4,568 ± 16 are asymptotic estimates from 100 permutations. Both correct, different questions.
- **I cited the wrong version of the pggb paper throughout the first draft.** The file circulating as `Building_pangenome_graphs.pdf` is the April 2023 v1 preprint, not the published paper, and its Table 1 differs in every value. Corrected in §5. One correction went **against** my argument: published SNV F-scores are 0.978 and 0.967, not the 0.947 and 0.937 I first quoted, so the accuracy objection to pggb is weaker than stated in the first draft. The resource and assembly-quality objections got stronger. This is a caution about the whole document: automated extraction from a PDF cannot tell you which *version* of a paper you are holding.
- **Table 1 of the pggb paper was read from the bioRxiv v2 author manuscript**, not the typeset *Nature Methods* PDF. Abstract and author list match the PubMed record exactly, so I am confident it is the published table, but confirm against the journal HTML before these numbers go into a manuscript.
- **Methods sections of both large recent *B. pseudomallei* papers are unread** — Wu et al. 2026 (paywalled) and Seng et al. 2024 (not retrieved). Their specific SNP-calling, masking and pangenome software is unverified; only abstract-level claims are used above.
- **PPanGGOLiN's 20,656-genome / 120 GB figure comes from project documentation**, not a peer-reviewed benchmark, and conflicts with an independent benchmark where it was the heaviest tool at 1,500 genomes. Do not present it as a guaranteed operating point.
- **PIRATE, PEPPAN and Roary are effectively frozen** (last releases 2022, 2020 and 2019 respectively) — relevant if Gap 3 or a reviewer asks why they were not considered.
