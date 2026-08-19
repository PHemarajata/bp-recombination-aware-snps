# Gap 3: pipelines and scale

**Resolved 2026-08-09.** Companion to `SNP_STRATEGY_REVIEW_2026-08.md`, `HANDOFF_research_gaps.md`, `GAP1_reference_free_kmer_methods.md` and `GAP2_clustering_algorithms.md`.

Scope, from the handoff: whether an nf-core pipeline covers bacterial SNP phylogenetics end-to-end and is worth adopting; ascertainment-bias correction done correctly; masking practice and whether a published masked-region BED exists for K96243; multi-replicon handling given 92% drafts; and IQ-TREE 2/3 vs RAxML-NG vs VeryFastTree at ~3,000 genomes.

Sources read via PubMed/PMC, journal full text, tool repositories, and — where the documentation was wrong or silent — the tools' own source code. Arithmetic and the four runnable checks are in `pipeline_checks_bp.py`.

**Method caveat, stated up front.** Several findings below come from reading source rather than documentation, because on this topic the documentation is wrong or absent in specific, consequential places. Those are marked. Separately, a number of retrieval routes were blocked during this session — tandfonline, ASM Journals, Nature supplementary files, `docs.rs`, parts of the GitHub API, and eventually the session's web-search budget. Everything below is quoted from text that was actually read; items that could not be reached are listed together in §8 rather than softened into the body.

---

## The short version

**1. Take the nf-core modules, not the pipeline — and bactmap's own documentation is the best citation you will find for your architecture.** On `--remove_recombination`, the bactmap usage docs say it *"should only be run on sets of samples that are closely related and not for example on a set of samples that have diversity spanning that of the entire species."* That is the pipeline's own authors conceding that their global-Gubbins design is inappropriate for a species-wide collection. Use it as the published justification for cluster-then-Gubbins.

**2. bactmap is a dead end in a stronger sense than the handoff recorded.** v1.0.0 is five years old, and the in-development 2.0.0 branch **deletes Gubbins and all four tree builders** — its `CITATIONS.md` and dev parameter list contain no Gubbins, no RapidNJ, FastTree, IQ-TREE or RAxML-NG. It is being repositioned as reads → pseudogenome → SNP alignment, handing phylogenetics back to the user. Adopting it would mean forking a pipeline whose maintainers are actively removing the functionality you depend on.

**3. Every step you need exists as a maintained nf-core module, and installing modules into a non-template repo is an explicitly supported pattern.** `gubbins`, `iqtree`, `snpsites`, `snpdists`, `fasttree`, `raxmlng`, `parsnp`, `mash/sketch`, `mash/dist`, `mashtree`, `ska/*` are all present; `poppunk` is not. One caveat that lands directly on your critical path: the nf-core gubbins module pins **3.3.5**, and the fix you care about is in 3.4.3.

**4. The graft is the genuinely unprecedented step — and PopPIPE may not actually be the precedent the handoff recorded.** Two pipelines now do cluster → per-cluster recombination correction at or beyond your scale and **deliberately stop before grafting**: **ARETE** (Beiko lab, Nextflow, PopPUNK → per-lineage SKA2 → Verticall and/or Gubbins, *"benchmarked on datasets from fewer than ten to over 10,000 genomes"*) and **BigBacter** (Washington State DOH, PopPUNK → per-cluster Snippy + Gubbins + IQ-TREE, switching to RapidNJ above 500 samples per cluster). Neither has a methods publication. PopPIPE remains the only implementation with all three steps — but see finding 5. Meanwhile the graft *is* proven at massive scale in SARS-CoV-2 (COG-UK grapevine → virus-evolution/phylopipe, via `clusterfunk graft` onto an explicit user-supplied guide tree), where splits use pre-assigned Pango lineages and recombination correction is absent by design.

**4b. PopPIPE's Gubbins probably does not sit on the path that produces the grafted tree — which weakens a "settled" claim in the handoff.** Reading the Snakemake rule structure, Gubbins is on the `transmission` target, operating on `ska map` reference-based alignments, while the grafted tree comes from `ska_align` → `iq_tree` → `graft_tree`. If that reading is right, **the PopPIPE overall tree is grafted from ML subtrees that were never recombination-corrected**, and the handoff's §3 statement that "PopPIPE does exactly this graft" overstates the precedent. Flagged as inferred from the rule graph, not stated by the authors — **verify against a real run before citing it either way.** Their own disclaimer stands regardless: the grafted tree *"will not maximize the phylogenetic likelihood – it is only intended as a convenient visualization of the entire dataset."*

**5. Use `-fconst`, not `+ASC`, and the reason is specific to this organism.** They are not two spellings of the same correction: they are Leaché et al.'s *reconstituted-DNA* and *conditional-likelihood* methods respectively. `+ASC` applies a blanket correction that cannot know the base composition of the sites it is compensating for. **K96243 is 68.06% GC** — composition ≈ A 15.9% / C 34.1% / G 33.9% / T 16.0%, computed directly from the two RefSeq records. In a controlled test, `-fconst` with true counts reproduced the full-alignment base frequencies and tree length exactly, while `+ASC` and a flat `-fconst 300,300,300,300` both collapsed to ≈25/25/25/25. At this GC content, `+ASC` discards information that `-fconst` preserves.

**6. The premise that `+ASC` silently inflates branch lengths on an alignment containing constant sites is wrong — it hard-errors.** IQ-TREE writes `.varsites.phy` and then calls `outError`: *"Invalid use of +ASC because of N invariant sites in the alignment"*. **The hazard is the remedy, not the error.** The trigger is `frac_invariant_sites`, not `frac_const_sites` — so a column that is genuinely polymorphic but retains one real base plus gaps after Gubbins masking counts as "invariant (constant or ambiguous constant)", trips the error, and is then **silently deleted** when you rerun on `.varsites.phy`. That is precisely the column class recombination masking creates.

**7. Gubbins v3.4.2 silently flipped a default, and v3.4.2 is additionally broken.** Reading the source across the three releases: v3.4.1 applied invariant-site correction to its internal trees **unconditionally**; v3.4.2 added `--invariant-site-correction` with `default = False` and gated the correction behind it. So the same command line gives materially different internal branch lengths across that boundary, released under the note *"Make invariant site correction optional."* Worse, in v3.4.2 the model-selection conditional chain used `elif` where it needed `if`, so enabling the correction **dropped the `-m` model flag entirely**. v3.4.3 fixes it. **Pin ≥3.4.3 and pass `--invariant-site-correction` explicitly.** A residual inconsistency survives in 3.4.3: model selection instantiates its `IQTree` object without the flag (so correction defaults on), while tree building respects the flag (so it is off) — the model is chosen under a corrected likelihood and the tree built without it.

**8. The concatenation junction is a real, undocumented problem, and three tools in the chain create or compound it.** `snippy-core` joins reference contigs *"end to end, in input-FASTA order, with no separator"* — verified in source. Gubbins detects recombination with a **spatial scanning statistic over a sliding window of 0.1–10 kb**, so any window straddling position 4,074,542/4,074,543 spans both chromosomes at once, across a step change in polymorphism density. And `snp-sites` **hardcodes `CHROM` to the literal `"1"`** in its VCF writer, with `POS` as the alignment column index — so every chr II variant is reported on chromosome "1" at an offset of 4.07 Mb. Gubbins has no `--mask`, no BED input, and no per-contig facility; the words *contig*, *replicon*, *plasmid* and *chromosome* do not appear in its manual at all. **The only way to keep Gubbins honest on a two-replicon reference is to split the alignment yourself and run it twice.**

**9. Nobody has published a concatenated-versus-per-replicon comparison, for any organism — and the same lab has done it both ways without comment.** Chewapreecha 2017 ran BEAST per chromosome and never says why; Seng et al. 2024, with Chewapreecha as corresponding author, ran Snippy → concatenated `core.full.aln` → snp-sites → Gubbins with no split and no mention of the change. The cost of getting it wrong is visible in Chewapreecha's own numbers: the TMRCA of the American isolates is **1806 from chromosome I and 1759 from chromosome II** — a 47-year spread on the same isolates — and they handled it by reporting both with a combined HPD rather than choosing.

**10. The strongest argument for splitting is a mutation-accumulation experiment, and it points the opposite way from the obvious one.** Dillon et al. 2015, 47 MA lines of *B. cenocepacia* over >5,550 generations: base-substitution rates differ significantly across the three chromosomes (χ² = 6.77, d.f. = 2, P = 0.034), and *"are highest on Chr1, and lowest on Chr2, which is **the opposite of observed evolutionary rates on these chromosomes**."* Chromosome II mutates less per site per generation yet diverges more in nature. **The excess on chr II is therefore selection and recombination, not mutation** — which is exactly the regime a single concatenated alignment under one substitution model and one clock cannot represent. It also kills compositional binning: GC is 66.8 / 66.9 / 67.3% across the three replicons, essentially identical.

**11. There is no published masked-region BED for K96243, but the coordinates exist and are retrievable.** Holden et al. 2004 describe **16 genomic islands totalling 6.1% of the genome**; Tuanyok et al. 2008 define **71 distinct GIs across five strains including K96243**, with a tRNA-anchored nomenclature; and **IslandViewer 4 holds precomputed predictions for `NC_006350.1`**, downloadable as tab-delimited/CSV/Excel. That last one is the practical answer to the handoff's question: not a BED, but a downloadable coordinate table for your exact reference, from the standard tool.

**12. Whether to pre-mask at all is genuinely contested, and the Gubbins authors are on the "don't" side — with one precise exception.** The manual states there is *"no need to remove accessory genome loci, as the algorithm should cope with regions of missing data"*, and the 2015 paper's showcase result is Gubbins recovering a 44.7 kb prophage as a single clean event. Yet Gubbins' own alignment generator runs `ska map --repeat-mask`. **The principled line is: mask what you cannot reliably call; do not mask what you can call but expect to be recombinant.** Repeats fall on the first side, prophage and genomic islands on the second.

**13. Over-masking has two documented failure modes, one mechanical and one statistical.** Mechanically, every masked base is missing data, and `--filter-percentage` (default 25) drops taxa for gappiness — in Gubbins issue #392, SKA2 repeat-masking took 217 *M. kansasii* genomes from <10% N to >40% N and the filter ate the dataset. Croucher's documented answer is to raise it; his own group used `--filter-percentage 100.0` in Derelle et al. 2024. Statistically, Hedge & Wilson found that *"removing recombining sites can exacerbate branch length distortion caused by recombination"*, because older events are easier to detect and so masking strips substitutions preferentially from deep branches.

**14. The only organism with a rigorous, benchmarked mask got there by shrinking it 2.7-fold.** Marin et al. 2022 benchmarked *M. tuberculosis* short-read calls against long reads and replaced the conventional ~10% exclusion list with a 177,077 bp / **4.01%** refined set, finding **68% of traditionally excluded positions are accurately callable**, including 52 of 168 PE/PPE genes. Their masking-versus-tuning comparison is the number to quote: masking repetitive content bought precision 99.1% → 99.6% at a cost of recall 85.8% → **70.2%**. Fifteen points of recall for half a point of precision.

**15. The only prospective test of masking in a transmission setting recommends against it.** Gorrie et al. 2021, 1,537 genomes across 16 STs and four organisms: *"Omitting prophage regions had minimal effect; however, omitting recombination regions had a highly variable effect, often inflating the number of closely related pairs"*, concluding for *"a closely related reference genome, **without masking of prophage or recombination regions**"*.

**16. On tree inference the decisive published number is that IQ-TREE `--fast` beats FastTree on both axes at once.** Lees et al. 2018, the only bacterial-genomics benchmark: Kendall-Colijn distance from truth — RAxML 4.63, IQ-TREE full 11.2, **IQ-TREE `-fast` 11.3 in 14.6 minutes**, parsnp 14.0, FastTree 16.0 in 189 minutes. `-fast` is 48× faster than full IQ-TREE for 0.1 KC units, and simultaneously **more accurate and 13× faster than FastTree**. There is no remaining argument for an approximate method at backbone scale.

**17. VeryFastTree cannot do ascertainment-bias correction, which disqualifies it from any SNP-alignment step.** Verified three ways: the FastTree manual has no such option, the VeryFastTree manpage inherits the interface exactly, and the RedDog developers hit this and switched to RAxML for `ASC_GTRGAMMA`. It remains admissible only on full-length alignments where constant sites are retained. **Related correction: VeryFastTree does not claim to produce identical output to FastTree 2** — the v4 paper says thread level ≥2 *"may result in **different trees** with respect to the sequential execution"*, and level 3 is the default. The real claim is equal topological accuracy plus determinism, the latter being an advantage over *parallel* FastTree-2, not over sequential.

**18. IQ-TREE parallelises along the alignment, not across taxa — so reducing to SNPs destroys your threading headroom.** From the IQ-TREE FAQ: *"the parallel efficiency is only increased with longer alignments."* A snp-sites alignment of tens of thousands of sites saturates `-T AUTO` at few threads. **Run many clusters concurrently at low thread counts rather than one cluster at high.** RAxML-NG quantifies the same pattern with its coarse-grained mode: 20 searches on 16 cores went from 2,300 s at one worker to **893 s at four**.

**19. Three thousand taxa is below the documented breaking point, but not far below.** RAxML-NG *"did not converge on a 10,000-sequence dataset even after a week"* on 16 CPUs; at 50,000, IQ-TREE 2 *"fails to return a tree at all due to memory issues."* At 3,000 the risk is convergence, not crashing — budget multiple starting trees. And use **transfer bootstrap**: Lemoine et al. designed TBE precisely because at this scale *"Felsenstein's bootstrap tends to yield very low supports, especially on deep branches."* RAxML-NG computes both metrics in one run with `--bs-metric fbp,tbe`, which lets you demonstrate the collapse rather than assert it.

**20. Your grafting architecture has a name and a literature you are not citing.** Disjoint tree mergers — NJMerge, TreeMerge, and GTM — decompose taxa into disjoint subsets, build subset trees, and merge them. GTM was the pipeline that succeeded at 50,000 sequences where both RAxML-NG and IQ-TREE 2 failed. Your cluster-trees-plus-backbone design *is* a disjoint tree merger with an ad hoc merge step; GTM's merge provably minimises topological distance to the guide tree, which representative-grafting does not.

---

## 1. Community pipelines, and the adoption verdict

### 1.1 nf-core/bactmap: the handoff was right, and the situation is worse than recorded

Confirmed as stated in the handoff: no clustering step, and Gubbins is the single optional flag `--remove_recombination` applied to the whole concatenated alignment. Two things to add.

**First, the documentation argues your case for you.** From [nf-co.re/bactmap/1.0.0/docs/usage](https://nf-co.re/bactmap/1.0.0/docs/usage/):

> "remove regions likely to have been acquired by horizontal transfer and recombination and therefore perturb the true phylogeny using gubbins. **This should only be run on sets of samples that are closely related and not for example on a set of samples that have diversity spanning that of the entire species.**"

This is a first-party statement that bactmap's own recombination step is documented as inappropriate for a species-wide dataset. For 3,000–5,700 *B. pseudomallei* genomes at r/m = 7.2 it is decisive, and it is a better citation than any external critique.

**Second, bactmap 2.0.0 removes the entire phylogenetics half of the pipeline.** The `dev` branch `CITATIONS.md` lists AdapterRemoval2, BCFtools, BEDTools, Bowtie2, BWA-MEM2, Clair3, Falco, fastp, fastq-scan, Filtlong, FreeBayes, minimap2, MultiQC, nanoq, Porechop, Rasusa, SAMtools, seqtk, SNP-sites — and **no Gubbins, no RapidNJ, FastTree, IQ-TREE or RAxML-NG**. Confirmed three ways: the dev `CITATIONS.md`, the dev output docs (which end at snpsites → multiqc), and the dev parameters page (no `--remove_recombination`, no `--iqtree`).

Release state: v1.0.0 tagged 18 June, inferred 2021 (nf-co.re reports "about 5 years ago"; the Zenodo record for 0.9.1 is 10 May 2021). Newest `dev` commit 27 July 2026. Open issue #74 is titled "Updating nf-core/bactmap Pipeline", marked *help wanted*. PR #153 "Version 2.0.0 Release" has been open since 22 September 2025 without its required approvals.

On multi-replicon references, the usage doc says:

> "although the pipeline can handle multiple contigs within the reference sequence, it is recommended that plasmid records are removed leaving only the chromosomal records (usually one chromosome in most bacteria) since plasmids are often acquired horizontally and are evolving at a different rate to the chromosome."

Note the parenthetical: the pipeline's mental model does not contain multipartite genomes. The stated reason for excluding plasmids — different evolutionary rate, horizontal acquisition — is *precisely* the argument that applies to chromosome II here, and the docs offer nothing for a second chromosome. Confirmed in `bin/vcf2pseudogenome.py`: per-contig sequence lists are flattened with `''.join(...)` into a **single `SeqRecord`**.

No documented scale limit anywhere in the 1.0.0 or dev docs.

### 1.2 nf-core/pathogensurveillance: real, published, and not what you need

Releases 1.0.0 (27 Jun 2024) and 1.1.0 (13 Feb 2025). Preprint: Foster ZSL et al., *"PathogenSurveillance: an automated pipeline for population genomic analyses and pathogen identification"*, bioRxiv 2025-10-31, DOI [10.1101/2025.10.31.685798](https://doi.org/10.1101/2025.10.31.685798) — still a preprint, `published_doi: NA`.

Tools: bbmap sendsketch → sourmash → fastp → SPAdes/Flye → Bakta → PIRATE → MAFFT → IQ-TREE2 (core-gene tree) → BWA-MEM → **graphtyper** → IQ-TREE2 (SNP tree).

Three disqualifiers:
1. **Grouping is by a samplesheet column**, `report_group_ids` — *"For every unique value in this column a report will be generated."* Metadata partitioning, not data-driven clustering.
2. **No recombination correction at all.** Gubbins is absent; there is no recombination parameter.
3. **`--max_samples` defaults to 1000** — the only explicit scale knob found in any nf-core bacterial pipeline, and it sits below your dataset.

Briefly, on the rest: **nf-core/bacass** is per-isolate assembly and annotation with no comparative genomics; **nf-core/phyloplace** does EPA-NG phylogenetic *placement* into an existing tree (its GAPPA "tree grafting" is grafting of placements, not of independently inferred subtrees, so it is not a solution to your graft); **nf-core/createtaxdb** is irrelevant; **nf-core/tbanalyzer** is dev-only and MTBC-specific. There is **no microbial/pathogen special interest group** among nf-core's 13 SIGs — no organised constituency that would maintain a cluster-then-Gubbins pipeline if you contributed one.

### 1.3 The non-nf-core field, and one finding that matters for your framing

**SPANDx** — Sarovich DS & Price EP, *BMC Res Notes* 2014;7:618, PMID 25201145, DOI [10.1186/1756-0500-7-618](https://doi.org/10.1186/1756-0500-7-618) — is the *B. pseudomallei* community's own pipeline, and it is alive: master `VERSION` 4.3.1, commits dated 5 August 2026, rewritten in **Nextflow** at v4.0. Abstract claim: *"comprising one through thousands of genomes."*

**But it has no clustering step and no recombination correction whatsoever.** A case-insensitive grep of the README, `main.nf` and `nextflow.config` for `gubbins|clonalframe|recombinat|repeatmask|phage|mask` returns **zero matches** — the string "recombination" does not appear anywhere in the repository, nor in the 2014 paper. I separately confirmed the README describes no default masking, no shipped exclusion BED, and does not name K96243 as a default reference. (A web-search snippet claiming SPANDx runs Gubbins and ClonalFrameML is simply false.)

What it has instead is a **dense-SNP filter as a recombination proxy**: `gatk VariantFiltration --cluster-size 3 -window 10`, i.e. ≥3 SNPs in a 10 bp window. That will not touch a 1–50 kb recombinant import — median tract length in this organism is ~5 kb (Nandi 2015). Trees are **FastTree 2** only, with "MP" implemented as `fasttree -noml` (minimum evolution, not parsimony), no bootstrapping, no model selection, no ascertainment correction.

Two further things worth knowing before citing it. **The Nextflow rewrite has never been published or tagged** — the last release is v4.0.1 (2020-04-02) while HEAD reports 4.3.1, and `nextflow.config`, the `main.nf` header and the runtime banner disagree with each other on the version. And there is a hard scaling wall in `bin/Master_vcf.sh`: all gVCFs go onto one `gatk CombineGVCFs` command line, followed by `GenotypeGVCFs -ploidy $n` where `$n` is the **sample count**. At thousands of genomes that hits `ARG_MAX`, has no GenomicsDB backend, and is combinatorially explosive. The largest datasets actually benchmarked in the 2014 paper were 16 *E. coli* and ~20 *H. influenzae* genomes; "thousands" is an assertion, not a measurement.

**Every *B. pseudomallei* paper that runs Gubbins is bolting it on downstream of SPANDx by hand. That is the strongest framing available for your work: the community's flagship tool stops at the SNP matrix, and it stops there without recombination correction.**

**ARDaP**, the same group's AMR tool (Madden DE et al., *EBioMedicine* 2020;63:103152, PMID 33285499, DOI [10.1016/j.ebiom.2020.103152](https://doi.org/10.1016/j.ebiom.2020.103152); and *Genome Med* 2024;16:78, PMID 38849863, DOI [10.1186/s13073-024-01346-z](https://doi.org/10.1186/s13073-024-01346-z)), shares the SPANDx codebase — `configs/gatk.config` is byte-identical and `bin/Master_vcf.sh` differs by one line — so it inherits the same wall. No publication states the relationship; source it to the code. It is also still **Nextflow DSL1**, which was removed at Nextflow v22.12, so it requires a pinned legacy runtime.

**Bactopia** (Petit & Read, *mSystems* 2020;5(4):e00190-20, PMID 32753501, DOI [10.1128/mSystems.00190-20](https://doi.org/10.1128/mSystems.00190-20)) is the most actively maintained competitor — v4.1.0 released 5 August 2026 — and its `snippy` Bactopia Tool is snippy → snippy-core → **Gubbins** → **IQ-TREE** → snp-dists, demonstrated at 1,664 genomes. Architecturally identical to bactmap 1.0.0: global Gubbins, no clustering. **Note its default `--iqtree_model HKY` applied to a SNP-only alignment — no ascertainment correction at all by default**, which is a live instance of the §2 problem in the most actively maintained pipeline in this survey. (There is no Bactopia v3 or v4 paper; PubMed `"Bactopia"[Title]` returns one record, the 2020 v1 paper, which the docs still direct you to cite.)

**CSP2** (Literman et al., *PeerJ Comput Sci* 2025, PMID 40989335, DOI [10.7717/peerj-cs.2878](https://doi.org/10.7717/peerj-cs.2878)) is the one to cite for the draft-assembly problem: Nextflow, extracts SNPs **directly from assemblies** via MUMmer whole-genome alignment, validated on **>11,000 isolates across 150 clusters** — the largest verified scale in this survey. It does not cluster (users pre-group by supplying references), does not remove recombination, and builds no tree by default.

**TheiaProk `Snippy_Tree`** (WDL/Terra) runs Snippy → Gubbins (`use_gubbins` **default true**) → SNP-sites → IQ-TREE 2 → SNP-dists, with a docs warning that Gubbins *"may take many iterations … especially for phylogenies that contain large numbers of genomes."* No clustering.

**Dead or unsuitable:** Nullarbor (last commit 3 August 2020; single-node `make -j`; Illumina PE only; no Gubbins); PHEnix (last commit 2018); SnapperDB (last commit 2018 — conceptually interesting because the "SNP address" *is* hierarchical clustering, but derived from SNP distances for naming, not to partition compute, and with no recombination correction); ProkEvo (Pegasus WMS, scaled to ~23,000 genomes and produces MLST/cgMLST/BAPS structure — but **no ML trees and no Gubbins**, so it clusters and then never builds per-cluster trees); P-DOR (not a workflow manager; clusters by SNP threshold and topology; no Gubbins; 1,388 genomes in 7h50m at 4.49 GB).

### 1.4 Cluster → correct → graft at scale: the graft is the unprecedented part

McHugh MP et al., *Microbial Genomics* 2025;11(4):001404, PMID 40294103, DOI [10.1099/mgen.0.001404](https://doi.org/10.1099/mgen.0.001404). Snakemake v7.8.5. PopPUNK → pp-sketchlib → RapidNJ → SKA2 → IQ-TREE → fastbaps, with **per-cluster Gubbins v3.1.0** in transmission mode. The grafting sentence, verbatim:

> "Create an overall tree by grafting the maximum-likelihood trees for subclusters to their matching nodes, rescaling branch lengths to match the neighbour-joining tree and midpoint rooting maximum-likelihood trees."

**Demonstrated on 616 *S. pneumoniae* genomes (62 strains) and 87 *E. faecium*.** Not 1,000+. Runtimes: PopPUNK clustering 2 min on 4 threads; visualisation + phylogeny + subclusters +28 min; transmission pipeline +52 min. Of 62 strains, 28 met `min_cluster_size: 6` and were subclustered. Tool versions: PopPUNK v2.7.0, SKA2 v0.3.9, IQ-TREE v2.0.3, **Gubbins v3.1.0**, fastbaps v1.0.5, BactDating v1.1.

**But the Gubbins step is probably not on the graft path.** The rule chain is `split_strains` → `sketchlib_dists` → `generate_nj` → `ska_build` → `ska_align` → `iq_tree` → `graft_tree`, while `gubbins` sits under the separate `transmission` target and consumes `ska map` reference-based alignments. On that reading the grafted overall tree is assembled from ML subtrees that were **never recombination-corrected**, and the shorthand "PopPIPE clusters, then removes recombination, then grafts" is wrong. This is inferred from the Snakefile and the paper's ordering, not stated by the authors — **check it against a run before relying on it in either direction.** Worth noting separately that PopPIPE's `config.yml` sets `iqtree: {model: 012310+G+ASC}`, so it *does* apply ascertainment correction.

**Two pipelines do the first two steps at or beyond your scale, and stop.**

**ARETE** (Beiko lab; Nextflow DSL2 on the nf-core template but not an nf-core pipeline; v1.0.1, 2024-05-13). Its docs distinguish two uses of PopPUNK explicitly, and the second is your architecture:

> "**Recombination detection is performed within lineages identified by PopPUNK.** Note that this application of PopPUNK is different from the subsetting described above."

The recombination subworkflow runs SKA2 then **Verticall and/or Gubbins**, emitting per-cluster `cluster_*.aln` and per-cluster Gubbins directories. Scale, verbatim: *"ARETE has been benchmarked on datasets from fewer than ten to over 10,000 genomes."* Its phylogenomics subworkflow is separate and whole-dataset, producing a single tree; **there is no tree-merging module and no graft.** No methods publication.

**BigBacter** (Northwest Pathogen Genomics / Washington State DOH; Nextflow; v1.0.0, 2024-10-18). PopPUNK assign against a taxon-specific database, with automatic resolution of PopPUNK-merged clusters, then **per cluster**: Snippy + snippy-core → Gubbins → snp-dists → IQ-TREE 2 below `--max_ml` (default **500 samples**), RapidNJ above it. Maintains a persistent per-cluster database so new samples join existing clusters — *"Optimized to reduce core genome shrinkage."* **No graft**; its PopPUNK visualisation is a parallel low-resolution artefact, not a backbone. No methods publication; applied in Torres LM et al., *Emerg Infect Dis* 2025;31(13):25–34, PMID 40359067, DOI [10.3201/eid3113.241227](https://doi.org/10.3201/eid3113.241227).

**The graft itself is proven at scale — in SARS-CoV-2.** COG-UK **grapevine** (Snakemake) and its Nextflow successor **virus-evolution/phylopipe** implement exactly this shape: split by lineage → per-lineage FastTree/VeryFastTree → root → `clusterfunk graft --scions <per-lineage trees> --input <guide_tree>`. Architecturally phylopipe is *cleaner* than PopPIPE, because the backbone is an explicit user-supplied `params.guide_tree` rather than an NJ tree of everything. Two decisive differences: they split on **pre-assigned Pango nomenclature**, not de-novo genomic clustering, and they do **no recombination correction at all**. Neither has a publication.

| Pipeline | Clusters? | Per-cluster recombination? | Grafts? | Scale shown |
|---|---|---|---|---|
| PopPIPE | ✅ PopPUNK | ✅ Gubbins 3.1.0 — but likely off the graft path | ✅ | 616 |
| **ARETE** | ✅ PopPUNK | ✅ Verticall and/or Gubbins | ❌ | **>10,000** |
| **BigBacter** | ✅ PopPUNK | ✅ Gubbins | ❌ | per-cluster ML/NJ switch at 500 |
| COG-UK grapevine / phylopipe | ⚠️ pre-assigned Pango lineages | ❌ | ✅ `clusterfunk graft` | SARS-CoV-2 scale |
| CSP2 | ❌ user pre-groups | ❌ | ❌ | **11,000+** |
| ProkEvo | ✅ fastbaps, 6 levels | ❌ | ❌ | ~23,000 |
| nf-core/pathogensurveillance | ❌ metadata groups | ❌ | ❌ | `--max_samples` 1000 |
| Bactopia `snippy` | ❌ | ❌ global | ❌ | 1,664 |
| TheiaProk `Snippy_Tree` | ❌ | ❌ global | ❌ | unstated |
| nf-core/bactmap 1.0.0 | ❌ | ❌ global | ❌ | unstated |

**The claim your review can defend** is narrower and better than "nobody has done this": cluster-then-per-cluster-recombination is now established practice at 10,000-genome scale (ARETE) and in routine public-health surveillance (BigBacter), but **both stop deliberately before merging the trees**; the only bacterial implementation that grafts describes its output as a visualisation rather than a phylogeny, and may not be correcting recombination on that path at all; and the one place grafting is proven at scale assumes away recombination entirely. **The unsolved piece is specifically the merge, under recombination.**

**Why the partition-first architecture exists at all** is worth stating in one line, from the Gubbins abstract itself: it *"achieves convergence in only a few hours on alignments of **hundreds** of bacterial genome sequences"* and is *"appropriate for reconstructing the **recent** evolutionary history"*. Hundreds, and recent. That constraint forces either partitioning (PopPIPE, BigBacter, ARETE) or a new detector — which is what Verticall is, and why the field's current momentum is toward scaling the algorithm rather than stitching trees.

### 1.5 The verdict: modules, not pipeline

Installing nf-core modules into a non-template Nextflow repo is documented and supported. From [Chapter 8 of the nf-core module tutorial](https://nf-co.re/docs/tutorials/nf-core_training/writing-nf-core-modules/chapter-8-using-in-pipelines): run `nf-core modules install <tool>`, select `pipeline` when asked, accept creation of `nf-core.yaml` and `modules.json` — *"This tracks installed module versions for future updates."* A documented gotcha: if a second install returns `ERROR 'manifest.name'`, add a `nextflow.config` with a `manifest` scope carrying `name`, `description`, `version`.

| Module | Pinned version | Notes |
|---|---|---|
| **gubbins** | `bioconda::gubbins=3.3.5` | runs `run_gubbins.py --threads $task.cpus $args`; honours `ext.args`; has stub |
| **iqtree** | `bioconda::iqtree=3.1.3` | accepts partition files, constraint trees, guide trees |
| **snpsites** | — | emits `*.fas`, `*.sites.txt`, **and a constant-site count value** — exactly what `-fconst` needs |
| **snpdists**, **fasttree**, **raxmlng**, **parsnp**, **mash/sketch**, **mash/dist**, **mashtree**, **ska/fasta**, **ska/distance** | — | present and maintained |
| **poppunk** | — | **does not exist** (404) |

Cost of adoption: move inputs to the meta-map convention (`tuple val(meta), path(...)`), define `process_low/medium/high` labels, add a `modules.config` supplying `ext.args` and `publishDir`. Mechanical, bounded, and it does not touch the architecture.

**One caveat to carry into the methods:** the nf-core gubbins module pins **3.3.5** (upstream April 2023) while upstream is **3.4.3**. Given §2, that pin is on your critical path — override the container spec rather than taking it as-is.

Framework citations if you adopt: Ewels PA et al., *Nat Biotechnol* 2020;38(3):276–278, PMID 32055031, DOI [10.1038/s41587-020-0439-x](https://doi.org/10.1038/s41587-020-0439-x); Langer BE et al., *Genome Biol* 2025;26(1):228, PMID 40731283, DOI [10.1186/s13059-025-03673-9](https://doi.org/10.1186/s13059-025-03673-9) — the latter stating that *"An extensive library of modules and subworkflows enables research communities to adopt common standards progressively."* That sentence licenses exactly the module-layer adoption recommended here.

---

## 2. Ascertainment bias, and a Gubbins reproducibility hazard

### 2.1 What Gubbins actually emits, and what goes into IQ-TREE

From the manual, the outputs are `.recombination_predictions.{embl,gff}`, `.branch_base_reconstruction.embl`, `.summary_of_snp_distribution.vcf`, `.per_branch_statistics.csv`, `.filtered_polymorphic_sites.{fasta,phylip}`, `.final_tree.tre`, `.node_labelled.final_tree.tre`, `.log`, plus `.final_tree.timetree.tre` and `.lsd.out` when dates are supplied.

**Gubbins does not emit a masked alignment by default.** `.filtered_polymorphic_sites.*` is polymorphic sites only, by construction. To get a full-length masked alignment you must run the bundled post-processing script.

`mask_gubbins_aln.py` was read in source. It loads the **original input alignment**, and for each GFF record performs an in-place substring replacement, `taxon.seq[start:end+1] = args.missing_char*(end-start+1)`. **It preserves alignment length exactly** — pure character substitution, no columns added or removed, and the GFF 1-based-inclusive → 0-based coordinate arithmetic is correct. Two things to note: the default masking character is **`-` (gap), not `N`**, and masking **destroys pattern compression** (see §2.5).

```bash
mask_gubbins_aln.py \
  --aln input_full_length.aln \
  --gff out.recombination_predictions.gff \
  --out out.masked.aln \
  --missing-char N          # consider N over the default '-'
```

### 2.2 Gubbins v3.4.2 flipped a default silently, and shipped a bug

First, a correction to the handoff. The actual GitHub release notes, confirmed against the releases page and the `releases.atom` feed:

| Tag | Release note (verbatim) | Timestamp |
|---|---|---|
| v3.4.1 | "Fixes to installation, addition of veryfasttree, and improved phylogenetic model fitting." | 2025-08-22T17:14:11Z |
| v3.4.2 | > "Make invariant site correction optional." | 2025-08-27T09:14:23Z |
| v3.4.3 | > "Fixes to the invariant site calculations." | 2025-08-27T19:45:27Z |

The handoff's v3.4.2 quote, "Change invariant proportion estimation", is not the release note — though it happens to describe a change that landed in **v3.4.3**. The v3.4.3 quote and the 2025-08-27 date are correct.

**Gubbins does pass constant-site counts to its internal tree builders.** From `common.py`:

```python
constant_sites = (complete_aln_length - snp_aln_length)
constant_base_counts = [int(b*constant_sites) for b in base_frequencies]
```

dispatched per builder: IQ-TREE gets `-fconst A,C,G,T` **and** a `+I` suffix; RAxML gets `-m ASC_GTRGAMMA --asc-corr=stamatakis` plus a partition file; RAxML-NG gets `--model GTR+G+ASC_STAM{a/c/g/t}`; FastTree, VeryFastTree, rapidnj and star get **nothing** (`self.invariant_site_correction = False`). The counts are apportioned by **observed base composition** over the full-length alignment, not a flat 25% — good, though with two approximations: overall composition proxies for constant-site composition, and gaps/Ns sit in the denominator but not the numerator, so `sum(constant_base_counts) < constant_sites` whenever there is missing data.

**The default flip.** v3.4.2 added:

```python
treeGroup.add_argument('--invariant-site-correction',
                       help='Correct for invariant sites',
                       default = False, action = 'store_true')
```

In v3.4.1 the correction was unconditional; from v3.4.2 it is gated on a flag that defaults to off. **The same command line therefore produces different internal branch lengths across the 3.4.1 → 3.4.2 boundary**, with no deprecation warning.

**The bug.** In v3.4.2's `IQTree.__init__` the model-selection chain read `if invariant_site_correction: ... elif self.model == 'JC': ...`. When the correction was enabled the first branch consumed the chain and **no `-m` flag was ever appended**, leaving IQ-TREE to fall back to ModelFinder. v3.4.3 splits the conditional correctly, and in the same change replaces the fixed `+I{p}` with an estimated `+I` — which is the "change invariant proportion estimation" the handoff recorded, one release later than recorded. **Treat v3.4.2 as a broken release and skip it.**

**A residual inconsistency in v3.4.3.** `select_best_models` builds its `IQTree` object without passing the flag, so it defaults to `True`. In a default run the model is selected under a constant-site-corrected likelihood and the tree is then built without the correction. Worth flagging in print.

One further oddity: when correction is on, Gubbins hands IQ-TREE **both** `-fconst` *and* `+I` — adding constant sites back as real columns while also asking IQ-TREE to estimate a proportion of invariable sites on top. The two are strongly confounded.

### 2.3 `+ASC` versus `-fconst`, and why the answer is compositional

**IQ-TREE 3 is released and published:** Wong TKF et al., *"IQ-TREE 3: phylogenomic inference software using complex evolutionary models"*, *Mol Biol Evol* 2026;43(5):msag117, PMID 42085559, DOI [10.1093/molbev/msag117](https://doi.org/10.1093/molbev/msag117). Latest tag v3.1.3 (2026-06-19). The `+ASC`/`-fconst` semantics are identical in 2.x and 3.x.

**The error is hard, not silent.** Reproduced locally on IQ-TREE 2.4.0 with a 10-taxon, 1,500-column alignment containing 1,200 constant sites:

```
Alignment was printed to t1.varsites.phy
ERROR: For your convenience alignment with variable sites printed to t1.varsites.phy
ERROR: Invalid use of +ASC because of 1200 invariant sites in the alignment
```

matching `model/modelfactory.cpp`, which calls `outError` after writing the file. The trigger is `frac_invariant_sites` — "constant **or ambiguous constant**" — not `frac_const_sites`. **This is the Gubbins trap**: a masked column retaining one real base plus gaps is ambiguous-constant, trips the error, and is then silently dropped if you rerun on `.varsites.phy`. bqminh's position, from iqtree2 #139: *"We intentionally stopped the run, so that users are conscious of the problem in their input data."* John Lees raised the ambiguous-base behaviour in iqtree2 #164 and closed it as consistent with the docs — documented, not fixed. And the `.varsites` writer was itself buggy for roughly a year (fixes in v2.2.0.2 / v2.2.0.8 / v2.2.2.4).

**`-fconst` has no long form.** Only `-fconst` exists in `utils/tools.cpp`; there is no `--fconst`. Order is **A,C,G,T**, comma-separated, no spaces. It literally synthesises real alignment columns and appends them, then recounts — so supplying `-fconst` guarantees `frac_invariant_sites > 0`, which guarantees the `+ASC` error. **They are mutually exclusive by construction, not by convention.**

**Prefer `-fconst`.** Leaché et al. 2015 (*Syst Biol* 64(6):1032–1047, PMID 26227865, DOI [10.1093/sysbio/syv053](https://doi.org/10.1093/sysbio/syv053)) name the two methods and map them exactly: conditional likelihood ≡ `+ASC`, reconstituted DNA ≡ `-fconst`, with the latter allowing counts *"specified for each base separately (i.e., A vs. C vs. G vs. T)"*. Their numbers: *"the uncorrected model overestimates the TL over 4-fold"*; *"The conditional likelihood method overestimates branches by 100%"*; *"Branch length biases are not as severe for the reconstituted DNA correction… most branches are within 25% of the full sequences branch lengths."* Their data are ddRAD lizards with up to 84% missing data, so the mechanism transfers and the percentages do not.

**The compositional argument, which is specific to this organism.** Computed directly from the RefSeq records:

| Replicon | Accession | Length | GC% | A | C | G | T |
|---|---|---:|---:|---:|---:|---:|---:|
| Chromosome 1 | NC_006350.1 | 4,074,542 | 67.72% | 654,024 | 1,382,812 | 1,376,465 | 661,241 |
| Chromosome 2 | NC_006351.1 | 3,173,005 | 68.49% | 501,425 | 1,091,456 | 1,081,855 | 498,269 |
| **Combined** | | **7,247,547** | **68.06%** | 1,155,449 | 2,474,268 | 2,458,320 | 1,159,510 |

Composition ≈ **A 15.9% / C 34.1% / G 33.9% / T 16.0%**. A flat assumption is wrong by more than a factor of two in both directions. Demonstrated on a 10-taxon test alignment with GC-skewed constant sites (true counts `185,394,410,211`), under GTR:

| Configuration | Estimated π(A), π(C), π(G), π(T) | Tree length |
|---|---|---:|
| Full-length alignment, constant sites retained *(reference)* | 0.1707, 0.3111, 0.3241, 0.1941 | 0.6040 |
| SNP-only + `-fconst 185,394,410,211` | **0.1707, 0.3111, 0.3241, 0.1941** ✅ | **0.6040** ✅ |
| SNP-only + `-fconst 300,300,300,300` (flat) | 0.2474, 0.2484, 0.2507, 0.2535 ❌ | 0.6016 |
| SNP-only + `GTR+ASC` | 0.2370, 0.2420, 0.2537, 0.2673 ❌ | 3.7192 |
| SNP-only, uncorrected | 0.2474, 0.2484, 0.2507, 0.2535 ❌ | 3.8837 |

**Honest caveat:** the test alignment's variable sites were drawn independently rather than on a tree, so the *tree-length* column is not a fair calibration test of `+ASC` (which reports lengths conditioned on variability, a different scale). Cite Leaché for the magnitude. The **base-frequency** result is exact and scale-free, and it is the point: `-fconst` recovers the true composition, `+ASC` and flat-`fconst` both collapse to ≈25/25/25/25.

The mechanism, from Conor Meehan: *"ASC is doing a Lewis correction to the likelihood score… **It doesn't know if it is an A or C or G or T just a blanket correction.** Fconst is doing a per site addition of constant sites which are then fed into the rate matrix and frequency calculations."*

### 2.4 Computing the counts: `snp-sites -C`, and three traps in it

Confirmed from `src/main.c` of snp-sites v2.5.1 (the README omits `-C`; only `--help` and the source have it):

```
 -c     only output columns containing exclusively ACGT
 -C     only output count of constant sites (suitable for IQ-TREE -fconst) and nothing else
```

Output is `"%d,%d,%d,%d\n"` in A,C,G,T order — directly pasteable. Three traps, all read from source:

1. **`-C` must be run on the full-length alignment**, never on `filtered_polymorphic_sites.fasta`, which by construction returns `0,0,0,0`.
2. **`-C` silently ignores `-c`.** `count_constant_sites()` hardcodes `pure_mode=0`. So in the popular one-liner, the alignment is built in pure mode but the counts are not — columns that are variable *and* contain an `N` are dropped by `-c` and not added to the constant counts. They vanish from the accounting, and `len(SNP aln) + sum(fconst) < len(original aln)`.
3. **Counts are read off the FIRST sequence only.** From `alignment-file.c:201`, `is_pure(first_sequence[i])` accepts only ACGT. Wherever taxon #1 has a gap or N at an otherwise-constant column, that column is not counted. **With a Gubbins-masked alignment, constant sites are undercounted in proportion to the first taxon's masked fraction.** Order the alignment so the least-masked genome is first, or compute the counts yourself.

Note this is looser than what the IQ-TREE author requires (Cibiv/IQ-TREE #137): *"fA should only count the number of AAAAA sites, i.e. strictly with A character. And not including A-A--AA, for example."* A discrepancy between the tool and the requirement, worth stating.

### 2.5 ModelFinder, and the cost question reframed

From `main/phylotesting.cpp`: on a SNP-only DNA alignment where `frac_invariant_sites == 0`, plain `-m MFP` **already tests `+ASC`, `+ASC+G`, `+ASC+R`** and picks by BIC; `-m MFP+ASC` restricts the candidate set to ASC models only. This is independently corroborated by Seng et al.'s wording — *"Standard model selection in IQ-TREE determined the best-fit model as TVM + F + ASC + R6"* — i.e. they did not force it. **Use `-m MFP+ASC` only if you take the ASC route**, so the choice is explicit rather than contingent on BIC.

**The cost trade-off is about distinct site patterns, not megabases.** From `tree/phylotree.cpp::getMemoryRequired()`, memory and per-iteration likelihood cost scale with the number of **distinct site patterns** × states × rate categories × mixtures × 8 bytes per internal node. IQ-TREE compresses identical columns; the local test reported `1500 columns, 296 distinct patterns`.

This cuts both ways, and the second half is the important one:

- For a **clean** full-length core alignment, constant sites collapse into ~4 extra patterns, so retaining them would cost almost nothing — the "3.8 Mb is too expensive" intuition would be wrong.
- **But a Gubbins-masked alignment is not clean.** `mask_gubbins_aln.py` gives every taxon a different gap pattern, so previously identical constant columns fragment into many distinct patterns. **Masking actively destroys pattern compression, and the penalty scales with recombination load** — worst case for this organism.

Verifiable benchmarks, all below your scale: 40 MTB genomes — full alignment 2m20s, full + `-t PARS -ninit 2` 1m20s, snp-sites 58s, snp-sites tuned 48s (≈3×, not orders of magnitude). Lees et al. 2018 at 96 taxa: IQ-TREE slow 703 min / 3.2 GB, IQ-TREE fast 14.6 min / 1.1 GB, RAxML 587 min / 3.0 GB, FastTree 189 min / 10.6 GB. **No benchmark exists at ~500 taxa × 3.8 Mb.** Given the pattern-compression argument, that is cheap to measure and worth measuring — `raxml-ng --parse` reports the exact pattern count in minutes.

### 2.6 Published guidance, and what the field actually does

The most explicit published ranking of your three options is institutional grey literature (Norwegian Veterinary Institute bioinformatics docs, © 2024), and it matches the analysis above:

> **(c) SNP-only + `+ASC`:** "This is the least recommended method because it uses an algorithm to estimate a correction to be applied on branch lengths… those evolutionary models that depend on estimating the empirical frequencies in your dataset cannot do that on variable sites only, because it might introduce a strong bias in base composition."

> **(b) SNP-only + `-fconst`:** "If you want to only use the MSA with only polymorphic sites, but get a better quality phylogeny, you can use the IQ-TREE `fconst` option without the ACS option."

> **(a) masked full-length:** "you provide the multiple alignment with recombinant masked (using `N`) and let IQ-TREE find the frequency of invariant base and polymorphic sites."

It also warns: *"NOTE: Never use Gubbins to remove recombinant sequences on concatenated genes alignment, or on MSAs of only SNPs!"*

**Neither Gubbins nor snippy helps.** The Gubbins paper (PMID 25414349) never mentions ascertainment bias, constant sites, or invariant sites — zero occurrences. Its only relevant statement is that final branch lengths are in point mutations and *"can be converted to substitutions per site by dividing them by the number of sites in the input alignment."* It sidesteps the problem for its own tree and hands you nothing for yours. The canonical snippy recipe applies no correction at all:

```bash
snippy-clean_full_aln core.full.aln > clean.full.aln
run_gubbins.py -p gubbins clean.full.aln
snp-sites -c gubbins.filtered_polymorphic_sites.fasta > clean.core.aln
FastTree -gtr -nt clean.core.aln > clean.core.tree
```

**The most-copied workflow in bacterial genomics propagates uncorrected branch lengths by default.** That is a citable point.

**Bacterial-specific quantification is a genuine gap.** No bacterial paper publishes a with/without-ASC branch-length comparison with numbers. The closest is Lees et al. 2018, added at reviewer request: *"We found similar topology in both modes, and if anything more accurate branch lengths when using polymorphic sites with an ascertainment bias correction… resource use was much lower when using only variable sites – we would therefore recommend this approach over using the full alignment."* Crucially, **they did not distinguish `-fconst` from `+ASC`**, so it does not settle (b) versus (c). The supplementary table carrying the actual numbers is JS-gated and was not retrieved.

The bacterial dating community effectively all uses option (b): Duchene S et al. 2018, PMID 29914372, DOI [10.1186/s12862-018-1210-5](https://doi.org/10.1186/s12862-018-1210-5) — *"**Because our data consist of SNPs, we used ascertainment bias correction by specifying the number of constant sites from the core genome.**"*, on Gubbins-filtered datasets. That is your best precedent. Menardo et al. 2019 (PMID 31513651) rescaled ML branch lengths post hoc and gave BEAST2 explicit constant-site counts, with neither arm using `+ASC`.

Two further citations worth having: **Bertels et al. 2014** (*Mol Biol Evol* 31(5):1077–1088, PMID 24600054, DOI [10.1093/molbev/msu088](https://doi.org/10.1093/molbev/msu088)) is the bacterial counterpart to Leaché, with the section header *"Branch Lengths Are Highly Inaccurate When Using SNP Positions Only"* and the finding that *"Up to 100% of all inferred tree topologies were incorrect for some parameter sets"* on SNP-only data versus essentially none on the full alignment — but note they compared **uncorrected** SNP-only against full, so do not cite it as evidence against `+ASC`. And **Capobianco & Höhna 2025** (*Syst Biol* 74(6):952–966, PMID 40378150, DOI [10.1093/sysbio/syaf038](https://doi.org/10.1093/sysbio/syaf038)) show that with among-character rate variation there are two distinct ways to condition on variable characters, that *"tree length and amount of ACRV in the data are systematically biased when conditioning… differently from how the data were simulated"*, and urge developers to state which they implement. IQ-TREE's documentation does not — which is live for `+ASC+R6`.

**Do not conflate this with SNP *discovery* bias** (Pearson et al. 2004, *PNAS* 101(37):13536–13541, PMID 15347815) — a different problem that reviewers routinely merge with this one. One pre-emptive sentence is worth it.

### 2.7 The recommended invocation

```bash
# 1. Gubbins on the full-length per-cluster alignment (per replicon -- see 3)
run_gubbins.py --prefix cluster01_chr1 \
  --tree-builder iqtree --first-tree-builder rapidnj \
  --invariant-site-correction \        # NOT the default in >=3.4.2 -- set it explicitly
  --threads 16 cluster01_chr1.full.aln

# 2. Mask recombination, preserving full length (N, not the default '-')
mask_gubbins_aln.py \
  --aln cluster01_chr1.full.aln \
  --gff cluster01_chr1.recombination_predictions.gff \
  --out cluster01_chr1.masked.aln --missing-char N

# 3. Constant-site counts from the MASKED FULL-LENGTH alignment, never the SNP file.
#    Put the least-masked genome first: snp-sites -C reads base identity off sequence #1.
snp-sites -C cluster01_chr1.masked.aln > cluster01_chr1.fconst

# 4. SNP alignment
snp-sites -c cluster01_chr1.masked.aln > cluster01_chr1.snps.aln

# 5. ML tree: -fconst, NO +ASC (mutually exclusive)
iqtree2 -s cluster01_chr1.snps.aln \
        -fconst "$(cat cluster01_chr1.fconst)" \
        -m MFP -T 4 -B 1000 --alrt 1000 --prefix cluster01_chr1.tree
```

The arithmetic must close: `len(SNP aln) + sum(fconst) == len(masked aln)`. Any shortfall is the `-c`/`-C` accounting leak or first-taxon masking. `pipeline_checks_bp.py §A` implements this check.

### 2.8 The two *B. pseudomallei* precedents

**Seng et al. 2024** — PMID 38972886, *Nat Commun* 15:5699, DOI [10.1038/s41467-024-50067-9](https://doi.org/10.1038/s41467-024-50067-9). Confirmed verbatim from the Methods via PMC11228029:

> "Core genome SNP alignment was identified from a full genome alignment using snp-sites v.2.5.1, with genomic islands masked. Separate maximum likelihood phylogenies were constructed… using IQ-TREE v.2.0.3. **Standard model selection in IQ-TREE determined the best-fit model as TVM + F + ASC + R6 for all three phylogenies.**"

and for the per-lineage trees, which are structurally your pipeline:

> "All genome alignments were subjected to Gubbins v.3.1.3… **Maximum-likelihood phylogenies were constructed using recombination-free SNP alignment of each dominant lineage using IQ-TREE v.2.0.3 with TVM + F + ASC + R6** and 1000 replicates of bootstrap support."

Two observations. They used **Gubbins v3.1.3**, where internal invariant-site correction was unconditionally on — so their Gubbins-internal trees were corrected while their downstream IQ-TREE used `+ASC` with no constant-site counts. And "standard model selection… determined" confirms ModelFinder chose `+ASC` rather than the authors forcing it.

**Wu et al. 2026** — PMID 42377320, *Emerg Microbes Infect* 15(1):2691358, DOI [10.1080/22221751.2026.2691358](https://doi.org/10.1080/22221751.2026.2691358). The abstract confirms *"Core-genome SNP phylogenies were constructed from recombination-masked alignments"*, consistent with retaining constant sites. **The full Methods could not be retrieved** (tandfonline 403, no PMC deposit), so the specific "skipped +ASC" quotation recorded in the handoff **remains unverified by this pass.** Flagging rather than repeating it as established.

A third, minor precedent: Schully KL et al. 2024, *Front Microbiol* 15:1401259, PMID 39044950, DOI [10.3389/fmicb.2024.1401259](https://doi.org/10.3389/fmicb.2024.1401259) — *"IQ-Tree (v1.6.10)… with automatic model testing using TVM+F+ASC+G4"*, 21 isolates, no justification. Note the recurring `TVM+F+ASC+*`: this is ModelFinder's default landing spot for GC-skewed *Burkholderia* SNP alignments, not a considered choice by any of these authors.

---

## 3. Multi-replicon handling

### 3.1 What each tool does to a two-chromosome reference

| Tool | Multi-contig ref? | Alignment output | Per-replicon coordinates retained? | Mask facility |
|---|---|---|---|---|
| snippy | yes | n/a | yes, in per-sample `snps.vcf` | `--mask` BED |
| snippy-core | yes | **concatenated, no separator** | `core.vcf`/`core.tab` yes; **`core.full.aln` no** | `--mask` |
| Gubbins | alignment only | n/a | **no concept of contigs** | **none** |
| snp-sites | n/a | SNP-only FASTA | **no — `CHROM` hardcoded to `"1"`** | none |
| bactmap `vcf2pseudogenome` | yes | **single concatenated SeqRecord** | no | n/a |
| ska map | yes | `.aln` concatenated; **`.vcf` keeps `CHROM`** | **yes, via VCF** | `--repeat-mask` |

`snippy-core` builds each output sequence as `join '', map { $seq{$id}{$_} } @$chrom_list` — end to end, in input order, no separator, no N-padding, no boundary record. For K96243 that puts BX571965.1 position 4,074,542 immediately adjacent to BX571966.1 position 1. `core.txt` gives no per-contig breakdown, so you cannot even read off how much of chr II aligned per sample. Nothing in the Snippy README warns about any of this.

**Gubbins is where it bites.** The manual states recombination *"is detected using a spatial scanning statistic, which relies on a sliding window"*, with windows *"between 0.1 and 10 kb such that the expected number of base substitutions in a window would be at least 10"*. Any window overlapping the junction spans both chromosomes across a step change in polymorphism density — and chromosome II carries the higher density. The background density used for the null on each branch becomes a mixture of two regimes.

**Is this documented?** Not by Gubbins. The words *contig*, *plasmid*, *replicon*, *chromosome* and *draft* do not appear in its manual. The only related caveat is the well-known one about Roary/Panaroo core-gene concatenations — the same class of error at a different scale, and the docs do not generalise it. There is **no `--mask`, no BED/GFF input, no per-contig option** in the full option list; `mask_gubbins_aln.py` masks *output*, not input.

**But it is documented downstream, by Theiagen**, in the `Snippy_Tree_PHB` workflow docs — and this is the citation to use, because it states the incompatibility flatly:

> "**If reference genomes have multiple contigs, they are incompatible with Gubbins** to mask recombination in the phylogenetic tree."

Theiagen's docs also carry the clearest published statement of Gubbins' failure modes, worth quoting alongside it:

> "Gubbins cannot distinguish recombination from high densities of SNPs that may result from assembly or alignment errors, mutational hotspots, or regions of the genome with relaxed selection. The tool is also intended only to find recombinant regions that are short relative to the length of the genome, so large regions of recombination may not be masked."

and the precondition that your clustering step exists to satisfy:

> "If masking recombination with `Gubbins`, input data should represent whole genomes from the same strain/lineage (e.g. MLST) that share a recent common ancestor"

The situation is not rescued by Gubbins' own alignment helper: `generate_ska_alignment.py` requests the **`.aln`** output with a single `--reference`, and contains no iteration over reference contigs. So the officially recommended input pipeline produces a concatenated pseudo-alignment for a two-chromosome reference. **`ska map` preserves replicon identity in its VCF output, not its `.aln`** — the correct route is `ska map` → VCF → split by `CHROM` → two alignments.

**snp-sites compounds it.** From `src/vcf.c`, the VCF writer emits `##contig=<ID=1,length=%i>` and `fprintf(vcf_file_pointer, "1\t")` for every variant row: **`CHROM` is hardcoded to the literal `"1"`**, and `POS` is the alignment column index. So a chr II SNP is reported on chromosome "1" at an offset of 4.07 Mb, and mapping back requires you to have retained the reference contig lengths yourself. This is the single most likely place in the pipeline for a silent off-by-4.07-Mb error. `pipeline_checks_bp.py §B` implements the split and the coordinate translation.

### 3.2 The field is split, and nobody has argued the case

**Chewapreecha 2017** mapped against both replicons of K96243 and ran BEAST **per chromosome** — and never states why. There is no methodological argument in the paper. The consequence is visible in their own results: TMRCA of the American isolates *"estimated to be 1806 or 1759 based on either chromosome I or II, respectively (combined 95% highest posterior density interval of both chromosomes, 1682-1849)"*. They did not choose; they reported both and quoted a combined HPD. Their date-randomisation ranks are also reported per chromosome, from 34th (group 6 chr II) to 97th (group 8 chr II) — worst and best both on chr II. And chromosome I of group 4 failed to reach a credible ESS while chromosome II succeeded.

**Seng et al. 2024** — same lab, Chewapreecha corresponding — ran the concatenated path end to end: Snippy against both accessions, snp-sites with genomic islands masked, Gubbins v3.1.3, no split anywhere and no mention of the change in approach. They cite Nandi 2015 for the chr I/chr II recombination asymmetry in their own reference list and still run Gubbins across the junction. One incidental mitigation: masking genomic islands, which are disproportionately on chr II, partially flattens the density step — but that is not the same as handling the junction.

**No paper explicitly compares the two approaches, for any organism.** Searched across *Burkholderia*, *Vibrio*, *Brucella*, *Agrobacterium*, *Rhizobium/Sinorhizobium*, *Leptospira*, plus "multipartite genome phylogeny", "chromid", "secondary chromosome phylogeny", "replicon-specific phylogeny". What exists is (i) papers reporting incongruence without recommending a practice — *V. vulnificus* chromosome I and II reconstructions were formally tested and found **not congruent**; *S. meliloti* showed *"significant incongruence, indicating reassortment among the three replicons in natural populations"*, with pSymB genes in overall linkage equilibrium; (ii) papers doing it one way silently (everyone else); (iii) reviews noting that evolutionary and mutation rates differ across replicons without making a methods recommendation. *Brucella* is predominantly concatenated and is a near-clonal, low-recombination genus where the question barely bites. For *Agrobacterium* and *Leptospira* I found nothing at all — genuine blanks.

**This is the most valuable finding in the sub-question, and it is a ready-made contribution:** run the same panel concatenated and per-replicon, quantify topological distance, quantify Gubbins' recombination calls in the junction window, and report per-replicon clock rates.

### 3.3 Chromosome II is a chromid, and it mutates *less*

Harrison et al. 2010 defined "chromid" by three criteria: plasmid-type replication and partitioning systems; nucleotide composition close to the chromosome; and carriage of core genes that are chromosomal in other species.

**Burkholderia chromosome II qualifies.** diCenzo, Mengoni & Perrin 2019 (*Mol Biol Evol* 36(3):562, DOI [10.1093/molbev/msy248](https://doi.org/10.1093/molbev/msy248)) built their analysis *"based on the amino acid sequence of the ParB partitioning protein"* — a **plasmid-type ParAB/parS system**, not the chromosomal DnaA/oriC one — and identified 37 genes conserved across *Burkholderia* and *Paraburkholderia* chromids, **8 of them annotated essential** (*accD*, *asd*, *dnaG*, *dxs*, *folC*, *rpoD*, *sdhA*, *sdhD*). McDonald–Kreitman on ParB gave a neutrality index of 0.039 (P < 0.001). Agnoli et al. (*PLoS Genet* 12(6):e1006172) confirm the partitioning systems are replicon-specific.

Two practical consequences. **DnaA/oriC finders will find chromosome I's origin and not chromosome II's**, so origin detection is a chr I detector, not a replicon classifier. And *parS*-based classification, while conceptually diagnostic, assigns one contig per replicon out of ~101 — useless for binning a draft.

**The mutation-accumulation result is the strongest argument available.** Dillon, Sung, Lynch & Cooper 2015, *Genetics* 200(3):935–946, PMID 25971664, DOI [10.1534/genetics.115.176834](https://doi.org/10.1534/genetics.115.176834) — 47 MA lines of *B. cenocepacia*, >5,550 generations each, 282 mutations, genome-wide base-substitution rate 1.33 × 10⁻¹⁰ per bp per generation:

> "The overall base-substitution mutation rates of the three core chromosomes differ significantly based on a chi-square proportions test" (χ² = 6.77, d.f. = 2, P = 0.034)

> "Base-substitution mutation rates are **highest on Chr1, and lowest on Chr2**, which is **the opposite of observed evolutionary rates on these chromosomes**."

> "The conditional base-substitution mutation spectra were also significantly different in all pairwise chi-squared proportions tests between chromosomes."

So the elevated divergence of chromosome II is not mutational in origin — it is selection and recombination. That is a much better argument for splitting than "chr II is more divergent", and it makes the case that one substitution model and one clock across the concatenation is mis-specified.

**It also kills compositional binning:** GC is 66.8% / 66.9% / 67.3% across the three replicons, with only the small true plasmid (62.0%) compositionally distinct. This satisfies Harrison's second criterion and simultaneously removes the obvious contig-assignment heuristic.

### 3.4 Draft assemblies: mapping coordinates are not the pragmatic choice, they are the only one

**No published number exists** for what fraction of a draft *B. pseudomallei* assembly can be confidently assigned to a replicon, and no published quantification of chr I ↔ chr II paralogy or cross-replicon mismapping in this organism. Searched directly.

The assembly context, from Chewapreecha 2017:

> "The assembly pipeline gave an average total length of 7,139,337 bp (range 6,744,467 – 7,536,799) from 101 contigs (range 72 - 356) with an average contig length of 84,361 bp (range 20,098 – 192,188 bp) and an N50 of 223,075 (range 37,455 – 1,142,362)."

At ~101 contigs and N50 ~223 kb, contigs are long relative to genes and short relative to replicons. The failure mode is not unassignable contigs but repeat-collapsed ones — and *B. pseudomallei* is IS-rich with substantial paralogy.

**Every published replicon-classification tool answers "chromosome or plasmid?", and none answers "which chromosome?"**

| Tool | *Burkholderia* model? | Separates chr I from chr II? |
|---|---|---|
| **mlplasmids** (PMID via DOI [10.1099/mgen.0.000224](https://doi.org/10.1099/mgen.0.000224)) | No — only *E. faecium*, *K. pneumoniae*, *E. coli* | No. And pentamer frequency is the wrong feature given §3.3 |
| **RFPlasmid** (DOI [10.1099/mgen.0.000683](https://doi.org/10.1099/mgen.0.000683)) | Yes, *Burkholderia* is among its 17 taxa | **No, and ambiguously so** — the paper says only that "complete and identified chromosomal and plasmid sequences were downloaded from NCBI GenBank"; NCBI labels BX571966.1 "chromosome 2", so it was almost certainly folded into the chromosome class. No multi-chromosome caveat anywhere |
| **plASgraph2** (DOI [10.3389/fmicb.2023.1267695](https://doi.org/10.3389/fmicb.2023.1267695)) | No — "The training set… did not contain any data from non-ESKAPEE species" | No |
| PlasmidFinder, MOB-suite, Platon, PlaScope, PlasClass, gplas | no chromid class | No |

**A chromid is, to every one of these tools, a chromosome.** They would all correctly decline to call chr II a plasmid, and all be useless for the problem.

What the field actually does is **ABACAS**, and only to build references — Chewapreecha: *"ordered relative to its closest reference using ABACAS v2.5.1 and ACT followed by manual curation"*; Seng: *"orientated its contigs according to strain K96243 using ABACAS v.1.3.1."* Neither bins every sample's contigs. **For the 92% draft cohort, replicon assignment comes from the mapping coordinate, and the literature offers no alternative.** That is a stronger statement than it looks, because the alternatives have been published and shown not to cover this case.

### 3.5 QC thresholds: the organism's literature does not state numeric cutoffs

Chewapreecha 2017's complete QC description is Kraken for contamination, *"Contigs shorter than the insert size length were filtered out"*, and SMALT remapping as a check. **That is the only hard filter — no N50 threshold, no contig-count threshold.** The ranges quoted (72–356 contigs, N50 37 kb–1.14 Mb) are observed, not imposed. Note the worst assembly in that set would comfortably pass Verticall's criteria (N50 ≥ 15 kb, ≤1,000 contigs), so those thresholds are permissive for this organism.

Seng et al. 2024: Kraken v1.1.1, **CheckM v1.2.2**, FastANI v1.31, with the numeric cutoffs deferred to *"Supplementary Data"* — **not retrievable in this session**. A CheckM completeness/contamination threshold from a 1,391-genome *B. pseudomallei* study is exactly the citable number you want; it is Supplementary Data 1 of DOI 10.1038/s41467-024-50067-9 and needs one manual download.

### 3.6 Callable fraction by replicon: nobody has published it

| Study | Core-genome figure | Per-replicon split? |
|---|---|---|
| **Sim et al. 2008**, *PLoS Pathog* 4(10):e1000178, PMID 18927621, DOI [10.1371/journal.ppat.1000178](https://doi.org/10.1371/journal.ppat.1000178) | **86% core (4,619 genes) / 14% accessory (750 genes)** | **Almost** — *"The 750 variable genes were equally distributed between both Chromosome 1 and Chromosome 2 after normalizing for chromosome size differences"* |
| Chewapreecha 2017 (469 genomes) | 4,064 core CDS; 324,637 SNPs; divergence 0.73–5.61% | No |
| Seng 2024 (1,391 genomes) | 5,577 conserved of 15,237 pan; 77,156 core SNPs | No |
| cgMLST (2021) | 4,221 core + 1,351 accessory targets | No |
| Wu et al. 2026 | 3,805,619 bp = 52.5% of K96243 | Methods not retrievable |

**Sim et al. is the only per-replicon core statement in the literature, and it is in tension with the "10× fewer core genes on chr II" framing carried in the main review.** The two are measuring different things — Sim is array CGH gene presence/absence across 94 isolates, not mapping callability, which is depressed further on chr II by higher recombination, density filters and accessory content — but the tension should be stated explicitly rather than left for a reviewer to find.

**This is a computation you should simply do.** `core.txt` will not give it to you (§3.1), but a `ska map` VCF split by `CHROM`, or per-sample `snps.aligned.fa`, gives the callable-fraction split directly. Given the literature is silent, one number — "X% of chr I versus Y% of chr II is callable across N genomes" — is a genuine contribution. `pipeline_checks_bp.py §B` computes it.

---

## 4. Masking

### 4.1 Is there a published K96243 BED? No — but the coordinates exist

**Holden et al. 2004**, *PNAS* 101(39):14240–14245, PMID 15377794, DOI [10.1073/pnas.0403302101](https://doi.org/10.1073/pnas.0403302101). From the abstract:

> "A striking feature of the genome was the presence of **16 genomic islands (GIs) that together made up 6.1% of the genome.** Further analysis revealed these islands to be variably present in a collection of invasive and soil isolates but entirely absent from the clonally related organism *B. mallei*."

**Tuanyok et al. 2008**, *"Genomic islands from five strains of Burkholderia pseudomallei"*, *BMC Genomics* 9:566, PMID 19038032, DOI [10.1186/1471-2164-9-566](https://doi.org/10.1186/1471-2164-9-566):

> "We identified **71 distinct GIs** from the genome sequences of five reference strains of *B. pseudomallei*: **K96243**, 1710b, 1106a, MSHR668, and MSHR305. The genomic positions of these GIs are not random, as many of them are associated with tRNA gene loci… we provide a GI nomenclature that is based upon integration hotspots."

This is the most complete GI catalogue for the organism and it explicitly includes K96243. Also relevant: Tumapa et al. 2008, *BMC Genomics* 9:190, PMID 18439288, DOI [10.1186/1471-2164-9-190](https://doi.org/10.1186/1471-2164-9-190), which took five representative K96243 islands and screened 186 NE Thai isolates by multiplex PCR — GI presence ranged from **12% (GI 9, prophage-like) to 76% (GI 16, metabolic)**, cumulative GI count per isolate 0–5 (median 2). Useful for arguing that GIs are variable enough to be worth masking, and that GI 9 in particular is a prophage.

**The practical answer: IslandViewer 4 holds precomputed predictions for both K96243 replicons, and they are downloadable anonymously today.** Verified live, 2026-08-09. Citation: Bertelli C et al., *"IslandViewer 4: expanded prediction of genomic islands for larger-scale datasets"*, *Nucleic Acids Res* 2017;45(W1):W30–W35, PMID 28472413, DOI [10.1093/nar/gkx343](https://doi.org/10.1093/nar/gkx343). **Still version 4 in 2026 — there is no IslandViewer 5.**

**Use the RefSeq accessions.** `BX571965`/`BX571966` are absent from IslandViewer entirely; it is keyed on RefSeq only.

| | NC_006350.1 (chr 1) | NC_006351.1 (chr 2) |
|---|---|---|
| internal analysis id | **15999** | **16000** |
| Integrated ("predicted by at least one method") | **64** | **16** |
| IslandPath-DIMOB | 11 | 7 |
| SIGI-HMM | 19 | 6 |
| IslandPick | 30 | 2 |
| Islander | 4 | 1 |

```bash
# GI coordinates, all four methods plus integrated, TSV
curl "https://www.pathogenomics.sfu.ca/islandviewer/download/coordinates/?aid=15999&token=15999&downloadtype=coordinates&methods=integrated&methods=sigi&methods=dimob&methods=islandpick&methods=islander&format=tab" -o K96243_chr1_GIs.tsv
curl "https://www.pathogenomics.sfu.ca/islandviewer/download/coordinates/?aid=16000&token=16000&downloadtype=coordinates&methods=integrated&methods=sigi&methods=dimob&methods=islandpick&methods=islander&format=tab" -o K96243_chr2_GIs.tsv
```

TSV header: `Island start / Island end / Length / Method / Gene name / Gene ID / Locus / Gene start / Gene end / Strand / Product / External Annotations`. Formats offered are **tab-delimited, CSV, Excel** for coordinates and annotations, **GenBank or FASTA** for sequence — **no GFF and no BED anywhere** in the UI, the REST API, or the bulk datasets, so you convert from TSV yourself. Whole-database tarballs are also available at `/islandviewer/download/datasets/` (`all_gis_islandviewer_iv4.txt.tar.gz` and per-method equivalents), though the advertised bulk FASTA links 404.

Four caveats worth recording in the methods. The precomputed database was **last updated 2024-09-06** (34,184 genomes) and has not been refreshed since, despite the FAQ claiming semiannual updates. The download endpoints above are **undocumented internal endpoints** reverse-engineered from the results page — the documented REST API has no endpoint for retrieving precomputed results at all, only for your own submissions. The server is slow (tens of KB/s on large responses), so set generous timeouts. And the sister tool IslandCompare carries a banner stating it is funded *"until at least the end of August, 2026, pending funding"*, with the date rolled forward monthly in git — **mirror these files locally rather than fetching at runtime.**

One rendering trap: the static HTML of `/accession/NC_006350.1/` shows "IslandPath-DIMOB (No results found)" for every method. That is misleading template text; the real counts load by AJAX from `/islandviewer/json/gis/15999/?token=15999`. Do not scrape the HTML legend.

**What Seng et al. masked is not stated.** Their Methods say only *"with genomic islands masked"*, with no definition, no citation to a GI source, and no coordinate file. Given Holden 2004 is the K96243 genome paper and defines 16 islands, that is the likely source, but it is an inference and should be labelled as one.

Underlying IslandViewer 4 methods, if you want to run them yourself rather than download: **IslandPath-DIMOB v1.0.6** (dinucleotide bias + mobility HMMs; Bertelli & Brinkman, *Bioinformatics* 2018;34(13):2161–2167, PMID 29905770, DOI [10.1093/bioinformatics/bty095](https://doi.org/10.1093/bioinformatics/bty095); bioconda `islandpath`, GPL-3.0), **SIGI-HMM** (codon-usage HMM, Waack et al., *BMC Bioinformatics* 2006;7:142, PMID 16542435; bioconda `colombo` 4.0 — note the original Göttingen download is **404 and the Brinkman GitHub mirror is now the canonical artifact**), **IslandPick** (comparative; no standalone distribution), and **Islander** (precomputed RefSeq only). Alien_Hunter/IVOM is **not** part of IslandViewer 4. Two operational traps: IslandPath-DIMOB requires **annotated GenBank/EMBL**, not FASTA, so a Prokka/Bakta step must precede it; and **do not clone `master`** — the `master` HEAD script predates the release tag and emits only legacy TSV without GFF3. Pin `v1.0.6-conda` or the bioconda package.

Benchmark for calibration (Bertelli & Brinkman 2018, 104 genomes, 1,845 GIs): IslandPath-DIMOB v1.0.0 recall 46.9% / precision 87.4% / MCC 0.49; SIGI-HMM 26.4% / 91.9% / 0.35; MTGIpick 67.5% / 55.1% / 0.32. **These are high-precision, low-recall tools.** For masking that is the right direction, but do not expect a GI predictor to find most of what is there.

### 4.2 Prophage and IS: what to use if you mask them

If you decide to mask mobile elements (see §4.3 before you do), the current evidence supports a short list.

**Prophage.** The 2025 benchmark to cite is Gao H et al., *"Highly accurate prophage island detection with PIDE"*, *Genome Biology* 2025;26(1):254, PMID 40836306, DOI [10.1186/s13059-025-03733-0](https://doi.org/10.1186/s13059-025-03733-0) — ground truth from **induced-prophage sequencing** of 38 isolates, which is the strongest boundary ground truth available. Base-level precision/recall: PIDE 0.91/0.91, **geNomad 1.8.0 0.81/0.90**, PHASTER 0.70/0.80, **VirSorter2 0.35/0.94**. Their qualitative finding: *"VirSorter2 systematically overpredicted PI boundaries, whereas PHASTER frequently missed portions of PI regions"* — which matches VirSorter2's own README warning that boundary detection *"tends to overextend to host regions"* by design.

The complementary CDS-level benchmark across a wider tool set is Roach MJ et al., *"Philympics 2021: Prophage Predictions Perplex Programs"*, *F1000Research* 2022;10:758, DOI [10.12688/f1000research.54449.2](https://doi.org/10.12688/f1000research.54449.2) — **note there is no PMID or PMCID**, confirmed via the NCBI ID converter; cite the DOI only. On 78 manually curated genomes: PhiSpy precision 0.772 / recall 0.731 / F1 0.733; VIBRANT 0.675/0.702/0.677; Phigaro 0.748/0.566/0.611; VirSorter2 0.399/0.766/0.508; DBSCAN-SWA 0.244/0.558/0.287. Directly relevant taxonomic note: F1 was significantly **above** average for *Burkholderia*.

Practical picks: **PhiSpy 5.0.10** (MIT, bioconda, native GFF3 plus *att*-site coordinates, ~150 s and <1 GB per genome — but requires annotated GenBank) or **geNomad 1.12.0** (bioconda, nf-core modules exist, FASTA in, provirus coordinates in the `coordinates` column of `virus_summary.tsv`). **Phigaro 2.4.0** is the lowest-friction option because `-e bed` emits BED directly. **Do not use VirSorter2 alone for boundaries.**

**PHASTEST** is usable locally after all, which the handoff did not know: there is an official Dockerised distribution (`wishartlab/phastest-docker-single`, amd64 only, plus a ~3.5 GB database zip from phastest.ca), and it emits `predicted_phage_regions.json` with `region/start/stop/completeness/most_common_phage/GC`. **But it is CC BY-NC 4.0 — non-commercial only**, which is why no nf-core module exists, and the shipped `docker-compose.yml` uses a fixed `container_name` and fixed input directory that break parallel Nextflow tasks. Also note the sibling service phaster.ca has been returning HTTP 522 since roughly April 2026. Citations: Wishart DS et al., *Nucleic Acids Res* 2023;51(W1):W443–W450, PMID 37194694, DOI [10.1093/nar/gkad382](https://doi.org/10.1093/nar/gkad382).

**IS elements.** **ISEScan v1.7.3** (2025-04-08, bioconda, Apache-2.0) is the workhorse: FASTA in, GFF3 plus a CSV carrying `isBegin`/`isEnd` out, published sensitivity 92% (ISbrowser) to 100% (*E. coli* K-12) at ~20% FDR. **ISfinder should not be in the pipeline**: no API, redistribution explicitly prohibited, and as of 2026-08-09 `isfinder.biotoul.fr` has no DNS record while `www-is.biotoul.fr` serves a maintenance page — only the UNESP/TnPedia mirror works. Cite it as the nomenclature reference; do not call it at runtime. If you are reference-mapping and want *sample-specific* IS insertion sites, **panISa 0.1.7** works from BAMs. **IntegronFinder 2.0.6** has an nf-core module if you widen the mask.

### 4.3 Should you pre-mask at all? The authors say mostly no

**The Gubbins manual is explicit**, and it is the strongest statement against pre-masking:

> The input should be a **whole genome sequence alignment**; there is no need to remove accessory genome loci, as the algorithm should cope with regions of missing data.

**The 2015 paper argues the same**:

> "the algorithm's flexibility allows it to be applied to full genome alignments without the difficult process of filtering to remove accessory loci, as is recommended for ClonalFrame."

> "Gubbins is effective even in cases where recombination primarily represents the movement of MGEs, with few false positives predicted elsewhere in the genome."

Its showcase result is Gubbins recovering φSa3 cleanly: *"Another extended to almost the entire length of the 44.7 kb prophage φSa3, with its edges just 680 and 96 bp within the respective 5′ and 3′ boundaries of the annotated MGE."*

**But Gubbins' own pipeline pre-masks one thing.** `generate_ska_alignment.py` runs `ska map --repeat-mask`, added in commit `1da11b91`, 2023-06-22, *"Mask repeats with ska2"*. SKA2's documentation: *"Add `--repeat-mask` to mask any repeated split k-mers in the reference with 'N'."*

**That is the principled line: mask what you cannot call, not what you can call but expect to be recombinant.** Repeats are unresolvable split k-mers — you have no reliable base there either way. Prophage and genomic islands are callable; leaving them in is what lets Gubbins do its job.

Derelle et al. 2024 (*Genome Res* 34(10):1661–1673, PMID 39406504, DOI [10.1101/gr.279449.124](https://doi.org/10.1101/gr.279449.124)) — Croucher and Harris are co-authors — is the modern statement of practice and it does exactly this:

> "We used `ska build`, with both k = 17 and k = 63, followed by `ska map` with options to mask repeats and any ambiguous bases… We used Gubbins v3.3.1, turning off gap filtering (`--filter-percentage 100.0`)"

> "the major peaks spanning prophage φMM1-2008, the mobile element ICESpn23FST81, and the *cps* operon were all detected."

> "Filtering on repeat regions removes these false positives but increases false negatives. For a purely phylogenetic or transmission analysis, the lower recall (which drops further with more distant references) is less desirable."

Note also `--filter-percentage 100.0`: the documented workaround for masking-induced missing data, used by Croucher's own group.

**The maintainer has been asked about MGE pre-masking twice in public and has never answered.** Gubbins issue #275 asked exactly this question in 2020 and Croucher did not reply; issue #382 (2023) asked whether IS elements should be hidden before Gubbins and Croucher answered the other four questions in the thread and not that one. The substantive public answer is from Mat Beale in #275:

> "If your goal is simply to mask out the recombination for downstream phylogeny, then as far as I am aware, it's unlikely to make a big impact on gubbins' ability to detect additional blocks, unless they are in close proximity to your masked regions."

### 4.4 What the big studies actually do — three practices, routinely conflated

| Practice | Description | Exemplars |
|---|---|---|
| **(1) A-priori coordinate masking** | Fixed BED applied before the alignment exists | *S.* Typhi; *M. tuberculosis* |
| **(2) Post-hoc event filtering** | Run detection on everything, then drop *detected events* in MGE annotations from r/m statistics | Croucher 2011/2013; Chewapreecha 2014 |
| **(3) Reference choice as implicit masking** | Map to an MGE-free reference | D'Aeth 2021 |

**Pneumococcus — Croucher's own practice is (2), not (1).** Croucher 2013 (*Nat Genet*, PMID 23644493): *"Recombinations occurring in regions annotated as MGEs… were also excluded, as these may represent the transfer of autonomously mobile elements rather than homologous recombinations."* Note the grammar: **recombinations** were excluded, not regions. The alignment is not masked. Chewapreecha 2014 (PMID 24509479) says the same for r/m calculation. The GPS project's methods (Gladstone et al. 2019, PMID 31003929) contain **no masking statement of any kind**. D'Aeth 2021 (PMID 34259624) is practice (3): *"Only genes present within this mobile genetic element (MGE)-free reference are annotated."* **Prophage, *cps*, *pspA/pspC* — none pre-masked.**

***S. aureus* does exclude MGEs, but both key papers predate Gubbins.** Holden et al. 2013 (PMID 23299977): *"SNPs falling within MGEs regions were also excluded from the core genome, as well as those falling in high-density SNP regions, which could have arisen by recombination."* That high-density filter is a **manual stand-in for** Gubbins, not a complement to it. I could find no post-2015 *S. aureus* study with an explicit published mask file.

***K. pneumoniae* does not mask the K and O loci.** Wyres et al. 2019 (PMID 30986243) filter only on quality, and the K/O loci are the headline result: *"there was a major peak defining a recombination hot-spot at the capsule (K) and adjacent LPS antigen (O) biosynthesis loci."*

***S.* Typhi is the cleanest a-priori mask, and it runs no Gubbins.** Wong et al. 2015 (*Nat Genet*, PMID 25961941): *"SNPs called in phage regions, repetitive sequences (354 kb; ~7.4% of bases in the CT18 reference chromosome…) or recombinant regions (~180 kb; <4%…) were excluded."* Three named categories with sizes — but the recombinant set is a fixed published list, not a Gubbins output, and the justification is that *"The S. Typhi genome is highly stable and exhibits minimal genetic variation and virtually no recombination"*. The opposite of your situation.

### 4.5 The one benchmarked mask, and what benchmarking did to it

Marin M et al., *"Benchmarking the empirical accuracy of short-read sequencing across the M. tuberculosis genome"*, *Bioinformatics* 2022;38(7):1781–1787, PMID 35020793, DOI [10.1093/bioinformatics/btac023](https://doi.org/10.1093/bioinformatics/btac023). Cite the erratum too (PMID 36893013).

> "Approximately 10% of the Mtb reference genome (H37Rv) is regularly excluded from genomic analysis because it is purported to be more error prone and enriched for repetitive sequence content"

> "Of these genomic positions typically excluded for Mtb, **68% are accurately called** using Illumina WGS including 52/168 PE/PPE genes (34.5%)"

> "the proposed RLC regions account for **177 kb (4.0%)** of the total H37Rv genome"

Independently recomputed from the distributed BED: `RLC_Regions.H37Rv.bed` is 773 intervals, **177,077 bp, 4.01%** — reproducing the paper exactly. The legacy list it replaced is 469,501 bp / **10.64%** (168 PE/PPE + 147 MGE + 69 repetitive genes). **A 2.7-fold reduction, recovering ~292 kb.**

The accuracy trade-off is the number to quote: MQ≥40 tuning gave recall 85.8% / precision 99.1%; masking repetitive content gave recall **70.2%** / precision 99.6%. **Fifteen points of recall for half a point of precision.**

**There is no Zenodo DOI** — the repo `farhat-lab/mtb-illumina-wgs-evaluation` (MIT) has zero GitHub releases, so no archive was ever minted. Pin the commit: the file has exactly one, `ee873927159c7fe18faa836839a9603fcaa25042`. Contig is `NC_000962.3`; the TB-Profiler `tbdb/mask.bed` uses `Chromosome` for the same coordinates, and `bedtools` will silently produce nothing on a mismatch. As of commit `13b6ed45` (2025-08-05) `tbdb/mask.bed` is the interval union of Modlin's blind spots (159,659 bp) and Marin's RLC+LowPmap (276,750 bp) = 311,910 bp / 7.07%.

**The lesson from the best-worked case is that community mask lists drift toward over-conservatism, and fixing them requires orthogonal ground truth rather than consensus.** No comparable benchmarked, machine-readable mask exists for any other bacterial species.

### 4.6 The two failure modes of over-masking

**Mechanical.** Every masked base is missing data, and `--filter-percentage` (default 25.0) drops taxa for gappiness. Gubbins issue #392 is the worked example: SKA2 repeat-masking took 217 *M. kansasii* genomes from <10% N to >40% N and the filter removed them. Croucher's reply:

> "You can change the percentage missing data used by Gubbins to filter the alignment - worth removing any low quality ingroup sequences before relaxing that criterion though."

**Statistical.** Hedge J & Wilson DJ, *mBio* 2014;5(6):e02158-14, PMID 25425237, DOI [10.1128/mBio.02158-14](https://doi.org/10.1128/mBio.02158-14):

> "Surprisingly, **removing recombining sites can exacerbate branch length distortion** caused by recombination."

> "removing homoplasies actually exacerbated the spurious signal of demographic growth generated by recombination, because older recombination events were more likely to be detected as homoplasies. This led to preferential removal of substitutions from the deep branches of the tree, producing trees that appeared even more star-like."

Topology is robust (>97% accuracy, still 93% at ρ = 8%); branch lengths and demographic inference are not.

**And the one prospective test says don't.** Gorrie CL et al., *Lancet Microbe* 2021;2(11):e575–e583, PMID 35544081, DOI [10.1016/S2666-5247(21)00149-X](https://doi.org/10.1016/S2666-5247(21)00149-X) — 1,537 genomes, 16 STs, four organisms, 15 months, eight hospitals:

> "Omitting prophage regions had minimal effect; however, **omitting recombination regions had a highly variable effect, often inflating the number of closely related pairs.**"

> "We propose that the use of a closely related reference genome, **without masking of prophage or recombination regions**, and of a sliding-window approach for isolate inclusion is best for accurate and consistent MDR organism transmission inference"

(Paywalled; these are from the PubMed structured abstract, which was read directly. The Methods were not.)

Note this pulls against Lees et al. 2018, from the same institute, which lists *"whether mobile elements have been masked"* among the determinants of tree quality and says *"The best practice is to try to remove these regions before performing phylogenetic reconstruction."* **That is a genuine, citable disagreement in the literature**, and worth presenting as one rather than resolving by assertion.

### 4.7 The recipe, if you build a mask anyway

Given §4.3–4.6 the defensible minimum is repeats only. If you want a GI/prophage mask as a *sensitivity analysis* rather than a default:

1. **Repeats** — `ska map --repeat-mask` against the two-replicon reference, which is what Gubbins' own helper does and requires no external coordinate file. If you want an explicit BED instead, self-align each replicon with `nucmer --maxmatch --nosimplify`, filter self-hits, and convert; do it **per replicon**, never on the concatenation.
2. **Genomic islands** — download the IslandViewer 4 precomputed table for `NC_006350.1` and `NC_006351.1` (tab-delimited), or run IslandPath-DIMOB v1.0.6 + SIGI-HMM yourself on a Bakta-annotated GenBank. Cross-reference Holden's 16 islands and Tuanyok's 71-GI nomenclature.
3. **Prophage** — geNomad 1.12.0 or PhiSpy 5.0.10; take `coordinates` / `prophage_coordinates.tsv` and convert.
4. **IS elements** — ISEScan v1.7.3, `isBegin`/`isEnd` from the CSV.
5. **Merge per replicon**, keeping BX571965.1 and BX571966.1 as separate BED contigs, and **report the total fraction masked**. PIDE found prophage averages ~2.8% of a bacterial genome; a mask far above the ~6.1% of Holden's islands plus repeats should be treated as suspicious.
6. **Raise `--filter-percentage`** to match, and report what you set it to.

And run it both ways. Given Gorrie, Hedge & Wilson, and Marin, the masked run is the sensitivity analysis and the unmasked run is arguably the primary.

---

## 5. Tree inference at scale

### 5.1 Versions and citations

- **IQ-TREE 3** — Wong TKF et al., *Mol Biol Evol* 2026;43(5):msag117, PMID 42085559, DOI [10.1093/molbev/msag117](https://doi.org/10.1093/molbev/msag117). Latest v3.1.3. **Caveat that matters:** its headline features — mixture models, gCF/sCF concordance factors, MCMCTree integration, AliSim — are all multi-gene phylogenomic features. **For a single concatenated core-SNP alignment, IQ-TREE 3 ≈ IQ-TREE 2 plus bug fixes.** Cite it; do not claim it improves this workflow. IQ-TREE 2: Minh BQ et al., *Mol Biol Evol* 2020;37(5):1530–1534, PMID 32011700, DOI [10.1093/molbev/msaa015](https://doi.org/10.1093/molbev/msaa015). Correction to the brief: **terrace-aware inference and PoMo are IQ-TREE 2 features**, not new in 3; MixtureFinder is genuinely new.
- **RAxML-NG** — Kozlov AM et al., *Bioinformatics* 2019;35(21):4453–4455, **PMID 31070718**, DOI [10.1093/bioinformatics/btz305](https://doi.org/10.1093/bioinformatics/btz305). (Not 30931025, which is a physiotherapy paper.) Stable v1.2.x; v2.0-beta2 on Zenodo 2025-05-12, v2.0-beta3 2025-10-31.
- **VeryFastTree** — Piñeiro C, Abuín JM, Pichel JC, *Bioinformatics* 2020;36(17):4658–4659, **PMID 32573652**, DOI [10.1093/bioinformatics/btaa582](https://doi.org/10.1093/bioinformatics/btaa582); and Piñeiro C, Pichel JC, ***GigaScience*** 2024;13:giae055, PMID 39115958, DOI [10.1093/gigascience/giae055](https://doi.org/10.1093/gigascience/giae055). (GigaScience, not *Bioinformatics*.) v4.0.5, 2024-04-06.
- **FastTree 2** — Price MN, Dehal PS, Arkin AP, *PLoS ONE* 2010;5(3):e9490, PMID 20224823, DOI [10.1371/journal.pone.0009490](https://doi.org/10.1371/journal.pone.0009490).

### 5.2 The decisive benchmark

Lees JA et al., *Wellcome Open Res* 2018;3:33, PMID 29774245, DOI [10.12688/wellcomeopenres.14265.2](https://doi.org/10.12688/wellcomeopenres.14265.2). 96 simulated bacterial genomes on a *L. monocytogenes* topology with pneumococcal evolutionary parameters, plus 616 real pneumococcal core genomes. Accuracy is Kendall-Colijn at λ=0; ~286 is random.

| Rank | Method | KC distance | Runtime |
|---|---|---|---|
| 1 | RAxML + mapped-reference alignment | **4.63** | 806.5 min |
| 2= | RAxML + core gene alignment | 11.2 | 587 min |
| 2= | IQ-TREE (slow) | 11.2 | 703 min |
| 4 | **IQ-TREE `-fast`** | **11.3** | **14.6 min** |
| 5 | Parsnp | 14.0 | 42.5 min |
| 6 | FastTree | 16.0 | 189 min |
| 9 | NJ on SNP alignment | 20.5 | — |
| 11 | BIONJ + Mash distances | 51.7 | 0.75 min |

Memory 1–37 GB across ML methods. Threading: *"RAxML achieved ~100% parallel efficiency with 16 threads; FastTree limited to ~4 CPUs."*

**Two things follow.** IQ-TREE `-fast` is simultaneously **more accurate and 13× faster than FastTree** — there is no operating point at which FastTree wins. And **parsnp ranks 5th**, below IQ-TREE `-fast` by 2.7 KC units, which bears directly on your backbone.

The authors' overall conclusion is worth quoting in the review because it reframes the whole gap: *"generating a high quality input alignment is likely to be the major limiting factor of accurate tree topology."*

### 5.3 FastTree's support values are the worst-calibrated of the options

FastTree's local support is an SH test over the three NNI topologies around a single branch — *purely local*, so it cannot detect that a clade is wrong because of a distant misplacement, which is the dominant error mode at high taxon counts.

Ecker N et al., *Bioinformatics* 2024;40(Suppl 1):i208–i217, DOI [10.1093/bioinformatics/btae255](https://doi.org/10.1093/bioinformatics/btae255):

> "among the various scores examined, **the SH test employed by FastTree exhibited the lowest performance, obtaining an AUC score of 0.876**"

and its supports *"substantially deviated from the expected probabilities (ECE = 0.055)"*.

Zhou X et al., *Mol Biol Evol* 2018;35(2):486–503, PMID 29177474, DOI [10.1093/molbev/msx302](https://doi.org/10.1093/molbev/msx302) — 19 empirical datasets, 36–200 taxa: IQ-TREE found the highest likelihood in **all 17 supermatrices**; FastTree's median normalised RF from the best tree exceeded 0.33, and **many incongruent splits received high bootstrap support.** That is the sourced answer to "does FastTree get bacterial topologies wrong": yes, and it reports them confidently.

The FastTree authors' own limitation statement is the cleanest citation of all: *"**If accurate branch lengths are essential, however, then neither the CAT approximation nor the standard Γ approximation is sufficient.**"* And `-gamma` is a post-hoc rescaling, not a model used in the search — the manpage says it reports the Γ likelihood *"after the final round of optimizing branch lengths with the CAT model"*.

### 5.4 Scaling, memory and where things break

**IQ-TREE parallelises along the alignment.** From the FAQ: *"IQ-TREE parallelizes the likelihood computation along the alignment. Thus, the parallel efficiency is only increased with longer alignments."* A short SNP alignment therefore saturates `-T AUTO` at few threads and can run *slower* with more cores. **Parallelise across your 61–101 clusters, not within them.** RAxML-NG's coarse-grained mode quantifies the pattern: 20 searches on a 16-core node, 2,300 s at one worker → **893 s at four workers**.

**`raxml-ng --parse` is the tool that answers the memory and pattern-count questions empirically** and should be step zero:

```bash
raxml-ng --parse --msa cluster01.snps.aln --model GTR+G+ASC_LEWIS --prefix c01
# * Estimated memory requirements: N MB
# * Recommended number of threads / MPI processes: N
```

It also writes a compressed `.raxml.rba` that speeds up later runs, and it reports the distinct-pattern count — which is what §2.5 says actually drives cost. RAxML-NG thread efficiency on 436 taxa × 1,371 sites: 90% at 2 threads, 75% at 4, 30–60% at 8–14, and **runtime increases at 16+**. It is hybrid MPI + pthreads, with `--workers` for independent searches.

RAxML-NG's ascertainment syntax, for completeness:

```bash
raxml-ng --msa snps.aln --model GTR+G+ASC_LEWIS --prefix asc1
raxml-ng --msa snps.aln --model GTR+F+ASC_FELS{3750000} --prefix asc2
raxml-ng --msa snps.aln --model GTR+F+ASC_STAM{900000/975000/975000/900000} --prefix asc3
```

with the hard requirement from the wiki: *"**When using `+ASC` models, you have to remove all invariant sites from the MSA!**"*

**The breaking point is ~10,000 taxa, not 3,000.** Zaharias P & Warnow T, *Phil Trans R Soc B* 2022;377(1861):20210244, PMID 35989607, DOI [10.1098/rstb.2021.0244](https://doi.org/10.1098/rstb.2021.0244) — note this is in the discussion-meeting issue *"Genomic population structures of microbial pathogens"*, directly on topic:

> "RAxML-NG, using 16 CPUs, **did not converge on a 10 000-sequence dataset even after a week**."

> at 50,000 sequences "**RAxML-NG has nearly 100% false negative error** … while **IQ-TREE 2 fails to return a tree at all due to memory issues**."

At 3,000 taxa you are below that, but the risk is convergence rather than crashing — budget multiple starting trees and check the likelihood spread.

### 5.5 Support at 3,000 taxa: use TBE

Lemoine F et al., *Nature* 2018;556(7702):452–456, PMID 29670290, DOI [10.1038/s41586-018-0043-0](https://doi.org/10.1038/s41586-018-0043-0):

> "With phylogenies of this size **Felsenstein's bootstrap tends to yield very low supports, especially on deep branches.**… The resulting supports are higher and **do not induce falsely supported branches.**"

Fast implementation: Lutteropp S, Kozlov AM, Stamatakis A, *Bioinformatics* 2020;36(7):2280–2281, PMID 31755898, DOI [10.1093/bioinformatics/btz874](https://doi.org/10.1093/bioinformatics/btz874) — up to 480× faster than `booster`, 31,749 taxa scored in under 2 minutes, integrated into RAxML-NG from v0.8.1.

```bash
raxml-ng --all --msa global.raxml.rba --model GTR+G+ASC_LEWIS \
         --bs-trees autoMRE --bs-metric fbp,tbe \
         --threads auto --workers auto --prefix global_all
```

`--bs-metric fbp,tbe` gives both in one run, so you can **demonstrate** the classical-bootstrap collapse rather than assert it.

**In IQ-TREE, `--tbe` works only with standard bootstrap `-b`, not with UFBoot `-B`** — the developers' position is that *"TBE was introduced in the context of standard Felsenstein's bootstrap"* and its interpretation under UFBoot is unstudied. `-sup` also does not work with `--tbe`. So IQ-TREE's fast support and IQ-TREE's TBE are mutually exclusive, which is a further reason to run the global tree in RAxML-NG. Caveat to state plainly: TBE makes the *scoring* free, not the replicates — at 3,000 taxa you still pay for 100+ full bootstrap searches, and that is the real cost.

For per-cluster trees, UFBoot2 (Hoang DT et al., *Mol Biol Evol* 2018;35(2):518–522, PMID 29077904, DOI [10.1093/molbev/msx281](https://doi.org/10.1093/molbev/msx281)) is *"778 times (median) faster than SBS"*. Remember the threshold differs: trust a clade at **SH-aLRT ≥ 80% AND UFBoot ≥ 95%**, and do not compare UFBoot percentages to classical bootstrap percentages.

### 5.6 MAPLE is ruled out, but testably so

De Maio N et al., *Nat Genet* 2023;55(5):746–752, PMID 37038003, DOI [10.1038/s41588-023-01368-0](https://doi.org/10.1038/s41588-023-01368-0) (**Nature Genetics**, not *Nature*); CMAPLE: Ly-Trong N et al., *Mol Biol Evol* 2024;41(7):msae134, PMID 38934791, DOI [10.1093/molbev/msae134](https://doi.org/10.1093/molbev/msae134).

Performance is extraordinary — at 10,000 sequences, CMAPLE 8 min / 0.24 GB against IQ-TREE 2's 40.5 h / 12.54 GB. And the stated applicability criteria rule it out:

> "every sequence must be at most **6.7% different from the reference sequence** and… **average sequence divergence from the reference must be at most 2%**"

with the README adding *"When analysing non-closely related genomes (e.g. branch lengths >0.01) the software will be both slower and less accurate."* A species-wide *B. pseudomallei* core alignment will exceed that. **But CMAPLE ships inside IQ-TREE**, so you can measure rather than argue:

```bash
iqtree3 -s cluster01.snps.aln --pathogen -T AUTO   # self-assesses, falls back if unsuitable
```

`--pathogen` checks the criteria itself and silently reverts to standard IQ-TREE when they are violated. Running it on one cluster and reporting which branch it took converts an inference into a measured result. Note also that the CMAPLE authors implemented 40 empirical protein models *"to enable analyzing a broader spectrum of pathogen data, including bacterial genomes"* — the aspiration exists, the bacterial validation does not.

### 5.7 Your graft has a literature

- **NJMerge** — Molloy EK & Warnow T, *Algorithms Mol Biol* 2019;14:14, DOI [10.1186/s13015-019-0151-x](https://doi.org/10.1186/s13015-019-0151-x). Divides taxa into disjoint subsets, builds subset trees, merges via a distance matrix on the full taxon set. Can fail to return a tree; O(n⁵).
- **TreeMerge** — Molloy EK & Warnow T, *Bioinformatics* 2019;35(14):i417–i426. Fixes both, and *"enables both ASTRAL-III and RAxML to complete on datasets that they would otherwise fail on."*
- **GTM** — Smirnov V & Warnow T, *BMC Genomics* 2020;21:235, PMID 32299343, DOI [10.1186/s12864-020-6605-1](https://doi.org/10.1186/s12864-020-6605-1). *"adds edges to connect subset trees so as to provably minimize the topological distance to a computed guide tree."* This is the pipeline that succeeded at 50,000 sequences where RAxML-NG and IQ-TREE 2 both failed.

**Your cluster-trees-plus-backbone design is a disjoint tree merger with an ad hoc merge step.** These three papers are the principled justification for the decomposition — and GTM's merge carries a guarantee that representative-grafting does not, which is worth considering as a substitution as well as a citation.

---

## 6. What I would actually do

**Ascertainment and Gubbins**
1. **Pin Gubbins ≥ 3.4.3 and pass `--invariant-site-correction` explicitly.** Never use 3.4.2. Record the version in the methods; the 3.4.1→3.4.2 default flip is a reproducibility hazard that affects published results, not just yours.
2. **Use `-fconst`, not `+ASC`**, computed with `snp-sites -C` from the **masked full-length** alignment, with the least-masked genome ordered first. Assert `len(SNP) + sum(fconst) == len(full)` on every cluster and fail the pipeline if it does not close.
3. If you prefer consistency with Seng et al., use `-m MFP+ASC` so the choice is explicit — but say in the methods that you know the two are different corrections and why you chose.

**Replicons**
4. **Split by replicon before Gubbins.** Route through `ska map` → VCF → split on `CHROM` → two alignments, or split the concatenated `core.full.aln` at the known reference boundary. Run Gubbins twice. This is unambiguously more defensible than the concatenated path and costs nothing but a split.
5. **Report per-replicon callable fraction and per-replicon topologies.** Nobody has published either. Concordance is a free check on whether a clade is real; discordance is itself publishable, and Chewapreecha's 47-year TMRCA spread says to expect some.

**Masking**
6. **Mask repeats only, by default** — `ska map --repeat-mask`, which is what Gubbins' own helper does. Raise `--filter-percentage` to match and report the value.
7. **Treat a GI/prophage/IS mask as a sensitivity analysis, not the primary.** Build it from the IslandViewer 4 precomputed table for `NC_006350.1`/`NC_006351.1` plus geNomad and ISEScan, merged per replicon, and report the fraction masked. Run the analysis both ways. Given Gorrie 2021, Hedge & Wilson 2014, and Marin 2022, the unmasked run has the better prior.

**Trees**
8. **Replace parsnp/FastTree on the backbone with IQ-TREE 3, `-m MFP -B 1000 --alrt 1000`.** At 61–101 taxa this is minutes, and it is the single most defensible change available: backbone errors are unrecoverable downstream, and parsnp ranked 5th where IQ-TREE ranked 2nd in the only bacterial benchmark.
9. **Per-cluster: IQ-TREE with `-fconst`, `-T 4`, many clusters concurrently.** Not one cluster at `-T 64`.
10. **If you attempt a global 3,000-taxon tree, use RAxML-NG with `--parse` first and `--bs-metric fbp,tbe` for support**, and treat it as a validation exercise against the grafted tree rather than as the production object.
11. **Drop VeryFastTree from consideration on any SNP alignment.** It cannot correct ascertainment bias, full stop.

**Cheap experiments worth doing before committing**
12. `raxml-ng --parse` on one real masked cluster — reports the distinct-pattern count and settles the full-length-versus-SNP cost question in minutes (§2.5). No published benchmark exists at your scale, so this is also a contribution.
13. `iqtree3 --pathogen` on one cluster — converts the MAPLE exclusion from an inference into a measurement (§5.6).
14. Concatenated versus per-replicon on one cluster — the comparison nobody has published, for any organism (§3.2).

---

## 7. Corrections to the earlier documents

1. **The Gubbins v3.4.2 release note is misquoted in the handoff.** It reads *"Make invariant site correction optional"*, not "Change invariant proportion estimation" — the latter describes a change that landed in **v3.4.3**. The v3.4.3 note and the 2025-08-27 date are correct. More importantly, the v3.4.2 change was a **silent default flip plus a bug**, which is a materially bigger finding than the handoff recorded (§2.2).
2. **`+ASC` does not silently inflate branch lengths on an alignment containing invariant sites — IQ-TREE hard-errors.** The handoff's framing of this as a correctness risk is right, but the mechanism is the *remedy* (silent deletion of ambiguous-constant columns via `.varsites.phy`), not the error (§2.3).
3. **Wu et al. 2026's "retained constant sites, skipped +ASC" is unverified by this pass.** The abstract confirms recombination-masked alignments; the Methods could not be retrieved (tandfonline 403, no PMC deposit), and one search pass could not locate the paper in an indexed form at all. Treat the specific quotation in the handoff as provisional until the PDF is read.
4. **Sim et al. 2008 says accessory content is *equally distributed* between the two replicons after size normalisation**, which is in tension with the main review's "chromosome II has ~10× fewer core genes". Both may be true of different quantities (gene presence/absence by aCGH versus core-gene counts), but the tension should be stated rather than left latent (§3.6).
5. **VeryFastTree does not claim to reproduce FastTree 2's output.** The v4 paper states thread level ≥2 *"may result in different trees"*, and level 3 is the default. The claim is equal topological accuracy plus determinism relative to *parallel* FastTree-2 (§5.1).
6. Minor: **terrace-aware inference and PoMo are IQ-TREE 2 features**, not IQ-TREE 3 additions; the RAxML-NG PMID is **31070718**; the VeryFastTree 2020 PMID is **32573652**; and the VeryFastTree v4 paper is in **GigaScience**, not *Bioinformatics*.
7. **The Gubbins `VERSION` file reads `3.4.2` on both `master` and tag `v3.4.3`.** So `run_gubbins.py --version` may report 3.4.2 on a 3.4.3 install. Cite the release tag, and do not use `--version` output as your provenance record.
8. **The handoff's settled fact #3 — "PopPIPE does exactly this graft" — needs qualifying twice.** First, PopPIPE's Gubbins appears to sit on the `transmission` branch rather than the path feeding `graft_tree`, so the grafted tree may be built from uncorrected subtrees (§1.4; inferred, needs checking). Second, and newly established by this pass, **PopPIPE is no longer the only pipeline doing cluster-then-per-cluster-recombination** — ARETE does it at >10,000 genomes and BigBacter does it in routine surveillance, both stopping before the graft. The novelty claim should be narrowed from "the architecture" to "the merge, under recombination". The rescaling advice the handoff took from PopPIPE is unaffected and still stands.
9. **The main review's remark that no published method validates grafting is right for bacteria but not in general.** COG-UK grapevine and virus-evolution/phylopipe graft per-lineage trees onto a guide tree at SARS-CoV-2 scale via `clusterfunk graft`. Neither is peer-reviewed and neither corrects recombination, so the caveat survives — but the sentence should acknowledge the viral precedent rather than claim none exists.

---

## 8. Still open after this pass

**Retrievable with access I did not have:**
- **Wu et al. 2026 full Methods** (tandfonline 403, no PMC deposit) — the ascertainment-correction claim, the reference genome used for SNP calling, and any per-replicon breakdown of the 3,805,619 bp core alignment.
- **Chewapreecha 2017 Supplementary Table** with the per-chromosome BEAST clock rates. A demonstrated chr I ≠ chr II clock rate would be the single strongest justification for splitting, and it is one PDF download from nature.com/articles/nmicrobiol.2016.263.
- **Seng et al. 2024 Supplementary Data 1** — the numeric CheckM completeness/contamination thresholds for 1,391 *B. pseudomallei* genomes.
- **Lees et al. 2018 Supplementary Table 1** — the actual with/without-ASC KC distances and resource deltas (JS-gated).
- **Tuanyok 2008 supplementary tables** — whether the 71 GI coordinates are given per strain in machine-readable form.
- **diCenzo & Finan 2017 MMBR** *"The Divided Bacterial Genome"* (ASM login wall) — the definitive multipartite review, likely carrying the per-replicon rate synthesis.

**Genuinely unpublished, as far as this pass can establish:**
- **No head-to-head comparison of concatenated versus per-replicon phylogeny exists for any organism.** Searched extensively.
- **No bacterial paper publishes a with/without-ASC branch-length or tree-scale comparison with numbers**, and none quantifies sensitivity of the tree to perturbations in the supplied `-fconst` counts.
- **No benchmark of any tree builder at ~500 taxa × 3.8 Mb**, i.e. nothing comparing a SNP-only alignment against the equivalent full-length alignment at bacterial scale.
- **No published quantification of chr I ↔ chr II paralogy or cross-replicon mismapping in *B. pseudomallei***, and no *Burkholderia*-specific contig-to-replicon binning method.
- **No benchmarked, machine-readable mask BED for any bacterial species other than *M. tuberculosis***.
- **No published guidance on masking specific to high r/m.** Gubbins' scope statement is diversity-based (*"samples of limited diversity, sharing a recent common ancestor"*), not r/m-based, and r/m is a Gubbins *output* rather than an input to the masking decision. The honest statement is that the r/m > 5 regime is governed by the "subdivide into lineages" advice, which is what Gap 2 already resolved.
- **No post-2015 Gubbins methods paper exists.** Not in PubMed, not cited by the README, not on the docs site. Derelle et al. 2024 is the closest thing to a modern methods statement from that group.

**Unverified for other reasons:**
- **Whether PopPIPE's Gubbins output ever reaches `graft_tree`** (§1.4). This is the single most consequential unverified item in this document, because it determines whether the handoff's "published precedent" for your architecture is a precedent for the whole thing or only for the clustering half. One run, or one careful read of the Snakefile DAG, settles it.
- `parsnp` uses FastTree 2 internally — worth confirming, because if so your backbone inherits every limitation in §5.3 whether or not you invoke FastTree by name. (Parsnp v2 does offer `--partition`, but note it merges *alignments*, not *trees*, and the v2 paper drops v1's recombination-detection claims entirely.)
- UShER/matOptimize applicability; presumed excluded on the same divergence grounds as MAPLE but not confirmed.
- **Non-GitHub hosting.** The "nobody has done this" claims in §1.4 rest partly on exhaustive GitHub code search, which cannot see GitLab, Bitbucket, or institutional Git hosts. A public-health-agency GitLab pipeline would have been missed. This is the main residual risk to the novelty claim.
- Bactopia v2.x/v3.x tool inventories — the versioned `bactopia-tools/` index pages 404, so "gubbins was never a standalone Bactopia Tool" is verified for v4.1.0 only.
