# Revised analysis strategy — *B. pseudomallei* SNP and phylogenetics

**Written 2026-08-09**, against `HANDOFF_research_gaps.md` and `GAP1`–`GAP4`. Supersedes `SNP_STRATEGY_REVIEW_2026-08.md` throughout. Section references of the form `GAP4 §5.0` point into those documents.

---

## 0. The decision that has to come first

There are two different papers latent in this pipeline, and they need different work. Deciding between them is the highest-leverage choice in this document, because it determines whether the subtree merge is a side-quest or the contribution.

**Paper A — "What the public *B. pseudomallei* genome collection can and cannot support."** An analysis-and-limits paper. Its evidence is largely already in hand: the burden-versus-sampling arithmetic (`GAP4 §1`, `§1.1`), the effective-sampling-frame measurements (`§4.2`), a systematic dateability assessment across all clusters, and a constrained set of geographic claims. Its headline findings are negative and defensible, and no competitor is positioned to publish them because nobody else has assembled the burden comparison.

**Paper B — "Recombination-aware subtree merging for large bacterial phylogenies."** A methods paper. The merge is genuinely unsolved (§3, Tier 1 item 4), but it needs SimBac benchmarking, a competing-method comparison, and a demonstration that the merged tree supports an inference the per-cluster trees cannot. That work does not exist yet and is several months of compute and development.

**Recommendation: write A first, and treat B as a distinct follow-up rather than a section of A.** Three reasons.

1. **A's evidence is already collected; B's is not.** The gap documents closed A. B requires SimBac work nobody has done.
2. **A does not need the merge at all.** Chewapreecha never merged; she dated per cluster and did geography by stochastic mapping on subsampled trees. Every conclusion A can defend is reachable from per-cluster trees plus a directly-built global backbone. The merge is currently load-bearing in your pipeline for conclusions that the sampling frame will not support anyway.
3. **Bundling them weakens both.** A methods contribution buried in an epidemiology paper gets reviewed by epidemiologists, and a novel merge presented without a simulation benchmark reads as an unvalidated shortcut — which is exactly how PopPIPE's authors characterise their own graft ("will not maximize the phylogenetic likelihood").

The protocol in §2 is written for A, with the hooks B needs marked **[B]**.

**The pushback this implies, stated plainly.** You describe the subtree merge as the unsolved methodological piece, and it is. But "unsolved" and "worth solving for this dataset" are different claims. Ask what the merged tree buys that per-cluster trees plus a backbone do not. The honest answers are: a figure, and a root. The figure does not need branch lengths to be correct. The root is a real scientific need — the Australian-origin claim is a root claim — but a root is recoverable from a directly-built global backbone with outgroups, which is what Chewapreecha and Pearson both did, and which does not require the merge to be statistically valid. That leaves the merge as a methods problem worth solving on its own terms, not a prerequisite for the biology.

---

## 1. What the sampling frame permits

This section constrains everything downstream, so it comes before any tooling. The full argument is `GAP4 §1` and `§1.1`; what follows is the operative summary and the consequences.

### 1.1 The frame, in numbers

| Quantity | Value | Source |
|---|---|---|
| Public assemblies (taxid 28450, 2026-08-09) | 5,728 | audit CSV |
| With usable country | 5,516 (96.3%) | audit |
| With country **and** year | 3,527 (61.6%) | audit |
| Thailand share | 59.6% | audit |
| Thai genomes from three BioProjects | 81.1% | `GAP4 §4.2a` |
| **Effective countries** (Hill *q*=2) | **2.48** of 37 labels | `GAP4 §4.2` |
| **Effective years** (Hill *q*=2) | **11.05** of a nominal 90 | `GAP4 §4.2` |
| Effective *n* at ICC 0.05 | 256 (4.6% of nominal) | `GAP4 §4.2a` |
| Sampling intensity range across countries | **35,852-fold** | `GAP4 §1.1` |
| Australia vs India, per predicted case | **1,877×** | `GAP4 §1.1` |
| Countries >100 predicted cases/yr with **zero** genomes | 29, totalling **33% of global burden** | `GAP4 §1.1` |

The two facts that do the most work: **South Asia carries 44.2% of predicted burden and holds 2.9% of genomes, while East Asia & Pacific carries 39.4% and holds 93.5%** (Limmathurotsakul 2016, PMID 26877885); and **Indonesia and Nigeria, second and third in the world by burden, contribute nothing at all.**

### 1.2 What that does to the inference

The mapping between sampling and biology is not merely noisy — it is **inverted across the top of the burden distribution**. This is what rules out the entire model-based phylogeographic family rather than merely degrading it:

- **DTA reads state counts as relative deme sizes** before seeing any sequence (De Maio 2015, PMID 26267488). The criterion is not "how skewed?" but "is the count vector an estimate of the population-size vector?" Here it is anti-correlated with it.
- **The structured coalescent is not the fallback.** Layan 2023 (PMID 36860641) found BASTA and MASCOT biased *even on unbiased samples*, and they "compensate for location under-representation by estimating high backward-in-time migration rates to the under-represented location" — which on this collection would make Guadeloupe (*n*=1) and the Philippines (*n*=1) the inferred migration hubs. They also would not run: ">15 locations … it currently seems unlikely that such analyses are possible at all."
- **MASCOT-GLM, the one intervention that worked under high bias, needs per-country case counts.** Melioidosis has none; Belman 2024 (PMID 38507601) hit the same wall for pneumococcus and abandoned the family.

### 1.3 The one geographic claim that survives, and why

Viberg 2017 (PMID 28400528) states that this organism "demonstrates a very strong phylogeographic signal that allows accurate identification of strain origin **on a continental level**," and validated it against known travel history for a CF patient assigned to Southeast Asia. That is independent corroboration of **continental-scale assignment** — Asia versus Australia — in a case where the answer was known.

**The defensible line, and it should be stated in exactly these terms: continental-level strain origin is well supported and independently validated; dated, directional, between-country migration inference is not.** §4 lists what falls on the wrong side of that line.

---

## 2. The revised protocol

Format for each decision: **what**, **why + citation**, **differs from your pipeline**, **differs from Chewapreecha 2017 / Seng 2024**. Steps are marked **[G]** global or **[C]** per-cluster.

A note on the shape of the whole thing. Your current architecture — partition, correct recombination within partitions, build trees per partition — is **right, and is the consensus design of the field**, supported independently by the Gubbins manual, the SKA2 authors, the `ska lo` authors, the Panaroo merge documentation, PopPIPE's architecture, Chewapreecha's design, and Lees' rebuttal to Sakoparnig. Nothing below changes that. What changes is the clustering primitive, the reference strategy, the ordering guarantees, and what you do at the end.

---

### 2.0 [G] Input QC and the analysable set

**What.** Filter to: contig N50 ≥ 20 kb, total length 6.5–7.9 Mb, and — adopting the Verticall benchmark's thresholds — ≤ 1,000 contigs. Retain `bioproject_accession`, `geo_loc_name`, `collection_date` and host for every genome. Parse ENA dates defensively: **PRJEB3409 stores the placeholder range "1800/2014", which a naive `date[:4]` reads as the year 1800.**

**Why.** The length tails are contamination and incompleteness (median 7,127,124; range 5,759,349–10,628,399). The Verticall QC thresholds (N50 ≥ 15 kb, ≤1,000 contigs) are permissive against your median N50 of 133 kb, so they cost almost nothing and are citable. The metadata retention is not optional bookkeeping — **BioProject is a primary analysis variable in this design** (§3, item 2), and the original audit script dropped it, which is why the third dominant Thai BioProject stayed unidentified for so long.

**Differs from your pipeline:** you currently do not retain BioProject. **Differs from both precedents:** neither treats study of origin as a variable at all.

**Expected analysable N:** ~3,436 (60.0%), still 54.1% Thailand.

---

### 2.1 [G] Replace Mash as the clustering primitive

**What.** Stop clustering on Mash distances. Refit with **PopPUNK v2.6.0** using the parameters already fitted to this organism by Seng: `--min-k 15 --max-kmer 31 --max-a-dist 0.53 --K 4 --k-step 2`. Report density, transitivity and network score against the documented ≥0.8 bar, plus the betweenness-penalised `score_1`/`score_2` variants.

**Why.** Three reasons, in descending force.

1. **Mash is the wrong primitive at this resolution, and sketch size does not save it.** Jain 2018 (PMID 30504855) on 464 *B. anthracis* genomes at ANI > 99.9%: Mash's Pearson correlation with true ANI collapses to **−0.040, 0.003, 0.010** at sketch sizes 10³, 10⁴, 10⁵, against 0.995+ on more divergent sets. *B. pseudomallei* is not as tight as *B. anthracis*, so this is the extreme rather than your exact case — but the direction is unambiguous.
2. **The default sketch is inadequate regardless.** At Ondov's s = 1,000, the error bound at k=21, D=0.05 is ±0.0068 — roughly **14% relative** at within-species range, tens of thousands of SNPs of uncertainty over 7.25 Mb. **Check what sketch size produced the current 61–76 clusters. If it was the default, that partition is partly noise, and no downstream validation repairs it.** This is the cheapest high-value check in the document.
3. **Mash conflates core divergence with gene content.** K96243 carries 16 genomic islands (~6% of the genome) and Nandi found clade-specific accessory profiles, so the conflation is material here. PopPUNK separates them by construction, regressing k-mer match probability against k under p_match,k = (1−a)(1−π)^k, and gives you core and accessory distances as separate axes.

**Invert the framing while you are here.** Seng's PopPUNK run on 1,391 *B. pseudomallei* genomes produced **101 lineages**. Your 61–76 over roughly twice as many genomes is **coarser than the only in-species precedent**, not finer. Stop treating the cluster count as the problem — and note that Wu's ten clusters are not a comparator at all, because `fcluster(criterion="maxclust", t=10)` means "return exactly ten." The real comparators are Chewapreecha's 19 hierBAPS groups and whatever PopPUNK/fastbaps give on your data.

**Differs from your pipeline:** replaces the clustering primitive entirely. **Differs from Chewapreecha:** she used hierBAPS on a core-genome mapping alignment; PopPUNK is assembly-based and scales. **Same as Seng**, deliberately — this is the one configuration with an in-organism precedent that demonstrably fed Gubbins successfully.

---

### 2.2 [G] Sub-cluster with fastbaps in phylogeny-conditioned mode

**What.** `best_baps_partition(sparse.data, tree)` — fastbaps constrained to partition an existing phylogeny. Multi-level via `multi_res_baps()`.

**Why.** It is the only BAPS-family mode that **cannot emit a polyphyletic cluster** (monophyly holds by construction), it runs in linear time in tree nodes rather than quadratic, and it is what PopPIPE uses. The alternative is disqualified on runtime alone: **rhierbaps did not finish in a week on 3,156 genomes × 392 kb** — almost exactly your scale — where fastbaps took 795 s.

**Two implementation traps.** The README spells the prior options with British `optimised.`; the actual argument strings are `optimise.`. And prior optimisation can take longer than the whole algorithm.

**Differs from your pipeline:** you have no model-based sub-clustering step. **Differs from Chewapreecha:** rhierbaps/hierBAPS, which will not run at your scale. **Differs from Seng:** they used rhierbaps v1.1.4 at 1,391 genomes; you have roughly twice that.

---

### 2.3 [C] The stopping rule — now MEASURED (see A.11); the derivation below is kept only as a record

> **⚠ SUPERSEDED BY APPENDIX A.11 (2026-08-11), measured on 17 clusters.**
> The ~1,000-SNP cap derived below is **wrong, and wrong in the dangerous
> direction**: it sits *below* the measured detection floor, where Gubbins finds
> essentially no recombination at all (cluster_62, measured 405: union coverage
> **0.7%** against ~78% expected). Applying it would have driven subdivision into
> a blind zone. Seng's 351–549 band is lower still.
>
> **The measured rule:**
> 1. **Subdivide until each cluster is UNIMODAL** — largest within-distribution
>    gap / mean ≤ **0.09** (`measure_diversity_bp.py --screen-all`). Bridged
>    clusters flatten r/m at *any* diversity, so this comes first.
> 2. **Then require measured mean pairwise core SNPs in ~2,700–4,700**, in
>    calibrated `ska distance` units — **never Mash**, which mis-scales by
>    0.88×–91×.
> 3. **Screen BOTH union coverage AND pooled r/m.** Below the floor union
>    collapses to ~1%; above the ceiling union stays *normal* at 79–87% while
>    r/m falls to 0.66–1.74. Neither statistic detects both failures.
>
> Floor bracketed to (405, 2,690]; ceiling to (4,671, 6,342]. Closing the floor
> needs the fastbaps sub-clusters — no continuous cluster exists between 405 and
> 2,690 in the current partition.

**What (superseded).** Subdivide until each cluster's **mean pairwise core-SNP distance is at or below ~1,000**. Report the distribution of that statistic across clusters alongside the partition. Post-hoc, report per-cluster r/m and masked-base fraction from Gubbins' `.per_branch_statistics.csv`.

**Why.** Chewapreecha's rule — "continue until the diversity observed in secondary or tertiary clusters fell within the limit of recombination detection" — **cannot be implemented as written, because Gubbins has never published a divergence ceiling.** Confirmed absent from Croucher 2015, the manual, the docs site and the manpage. Nobody implements it: PopPIPE hard-codes two fastbaps levels and `min_cluster_size: 6` (a *size* gate, never a *diversity* gate); iterative-PopPUNK gives you a 30-point sweep across 1–99% of maximum average core distance but no criterion for choosing a rung.

The rule above is derived from the mechanism Gubbins actually uses — detecting a local excess of substitutions over a branch's background density — so the binding quantity is a **contrast ratio** of imported-substitution density to background density. Against a 0.5%-divergent donor over Wu's 3,805,619 bp core alignment:

| Partition | mean pairwise core SNPs | contrast |
|---|---|---|
| Seng lineage 2 — Gubbins ran successfully | 351 | **54×** |
| Seng lineage 3 — Gubbins ran successfully | 517 | **37×** |
| Seng lineage 1 — Gubbins ran successfully | 549 | **35×** |
| hypothetical 2,000-SNP cluster | 2,000 | 9.5× |
| **species-wide** (π = 0.0067) | 25,498 | **0.7×** |

**That last row is the quantitative statement of why cluster-then-Gubbins is necessary rather than merely convenient in this organism** — species-wide, the contrast is gone, which is the *H. pylori* regime the Gubbins authors name as their failure case. A cap of ~1,000 gives ≥20× contrast against a 0.5% donor and sits within a factor of 2–3 of the only in-organism precedent.

**One thing that surprised the derivation and is worth knowing.** The obvious mechanism-matched proxy — Gubbins' own window-sizing rule — **does not bind at any realistic *B. pseudomallei* branch length.** The 10 kb ceiling applies to every branch carrying fewer than ~7,240 SNPs, so every realistic branch sits pinned at the ceiling and the rule never discriminates.

**A sensitivity floor to state as a limitation, not discover later.** With `--min-snps` at its default of 3 and Nandi's median tract length of ~5 kb, **imports from donors below 0.06% divergence are invisible to Gubbins no matter how you cluster.** Within-cluster donors in this organism are frequently that close.

**Say in print that this is a construct.** The honest sentence is: Gubbins publishes no divergence ceiling; the field's practice is to subdivide by PopPUNK or fastbaps and not measure the result; we calibrated against Seng.

**Differs from your pipeline:** you have no principled criterion. **Differs from Chewapreecha:** implements her intent with a number she never supplied. **Differs from Seng:** they subdivided and did not measure it.

---

### 2.4 [C] Per-cluster references, and the reference-sensitivity experiment

**What.** Map each cluster against a **within-cluster representative reference**, not species-wide K96243. Run **≥2 references per cluster and report concordance**.

**Why.** This is the largest controllable error source in the pipeline and *B. pseudomallei* sits in the worst part of the range.

- Across 209 pipelines and ten species, **distance-to-reference predicts recall at ρ = −0.94**, and the effect is "especially pronounced for diverse, recombinogenic bacteria" (Bush 2020, PMID 32025702). The best pipeline went from 0.944 to 2.627 errors/Mb — **2.8× — purely from the reference**.
- A 0.82%-divergent within-species reference inflated false-positive SNPs from 3.3–3.8 to 218.8–1,477.2 in *Listeria* (Pightling 2014, PMID 25144537). *B. pseudomallei* spans **0.73–5.61% from K96243**.
- **Recombination inference is itself reference-dependent** (Valiente-Mullor 2021, PMID 33503026), which puts your Gubbins step downstream of an unvalidated choice.
- In this organism specifically, Webb 2022 found a distant reference under-called by ~20% at outbreak scale — and that is the *only* study that has ever varied the reference here.

**This is not an improvement to propose; it is standard practice the current pipeline appears to omit.** Chewapreecha built lineage-specific references (ABACAS v2.5.1 + ACT + manual curation, then SMALT 0.7.4); Seng used per-lineage references for lineages 2 and 3; the Verticall benchmark used a separate reference for each of 83 sublineages. **If per-cluster Gubbins is currently running on alignments mapped to K96243, that is a deviation from the reference study, not an extension of it.**

**The experiment that closes this, and it is the highest-value single run available** (work-plan item 6). Take one mid-sized cluster (100–300 genomes, ideally with both Thai and non-Thai members) and build it three ways — your existing pipeline, `ska map`, and `ska lo` — against a within-cluster representative; run each through Gubbins; compare post-Gubbins SNP counts, positions shared by all three, tree distance, and root-to-tip R². **Then repeat against K96243.** If your pipeline's SNP count inflates and root-to-tip R² drops on the distant reference while the reference-free callers hold steady, reference bias is contributing to the weak temporal signal — and the fix is cheap. This replicates the `ska lo` PMEN2 experiment on your own organism, where moving to a reference at 98.52% OrthoANI took Snippy from 2,320 to 3,291 post-Gubbins SNPs (+42%) and root-to-tip R from 0.46–0.50 down to 0.25–0.29, while the reference-free callers barely moved.

**Either outcome is informative**, which is what makes it worth running: a null result retires reference bias as a concern and strengthens everything downstream. Optionally add **1026b** as a third reference — the field is split between K96243 (Chewapreecha and the Thai literature) and 1026b (the 2026 Vietnam study, 1,468 genomes) **with no published bridge**, and quantifying how much of the difference between those two literatures is reference artefact is publishable on its own.

---

### 2.5 [C] Alignment: `ska map` into Gubbins

**What.** Use `generate_ska_alignment.py --reference <within-cluster ref> --input input.list --out out.aln` — the officially supported Gubbins helper, which bundles SKA2.

**Why.** ~190× faster than Snippy (56 s vs 178 min on 240 pneumococcal genomes), correct multi-replicon coordinate handling, and no soft or hard reference bias. On divergence, *B. pseudomallei* is inside SKA2's usable range **at cluster level**: species-wide π ≈ 0.0067 puts it 1.3× past the strain boundary (~90% recall) and roughly 7× below the collapse regime, corroborated by Chewapreecha's per-isolate maximum of 0.596% divergence from K96243.

**Three guards, the first absolute.**

- **`ska align` output must never reach Gubbins.** Only `ska map` carries genomic coordinates; `ska align` columns are in hash-table order and "do not represent a physical position in the chromosome." Gubbins' sliding-window scan would run on meaningless spacing and **the failure would be silent.** This is the same class of error as feeding Gubbins a snp-sites alignment.
- **snp-sites goes *after* Gubbins, never before.** Didelot & Parkhill: variant-site alignments "cannot be used for recombination-aware phylogenetics since the genomic distance between variant sites becomes an important factor."
- **Never feed Gubbins a concatenated core-gene alignment** from Roary or Panaroo. The manual is explicit.

**Memory, so you can plan:** species-wide `ska align` is not viable (estimated ~300 GB at 3,000 genomes, ~590 GB at 5,728); per-cluster is cheap (~4/9/22 GB at 100/200/500 genomes). Replace these estimates with a measurement — one `ska build` + `ska align` run on an existing cluster, recording peak RSS, calibrates the whole table.

**One structural blind spot to check rather than assume:** split-mer methods cannot span low-complexity repeats longer than k, and k = 63 is a hard ceiling. Check whether any *B. pseudomallei* locus you care about has that character — the candidates are the large surface-protein and adhesin genes.

**Differs from your pipeline:** replaces the mapping step. **Differs from both precedents:** Chewapreecha used SMALT, Seng and Wu used Snippy. SKA is a speed and reference-bias improvement, not a correctness fix — so if the §2.4 experiment shows your existing caller is fine against a close reference, keeping it is defensible.

---

### 2.6 [C] Recombination: Gubbins, pinned, plus Verticall distance as a second arm

**What.** Gubbins **pinned at ≥3.4.3** with `--invariant-site-correction` passed explicitly. Run **Verticall distance** (v0.4.2) in parallel per cluster and judge on dating convergence.

**Why pin.** v3.4.2's release note is "Make invariant site correction optional" — it **silently flipped the internal correction to OFF** and shipped a broken model-selection chain; v3.4.3 (tagged 2025-08-27) is "Fixes to the invariant site calculations." Letting conda resolve the version across runs quietly changes your ascertainment-bias handling mid-project.

**Why the second arm.** Across **83 real *K. pneumoniae* clonal sublineages of 19–838 genomes** — the closest published analogue to per-cluster *B. pseudomallei* work — Verticall distance recovered temporal signal in **63/83 (75.9%)** against Gubbins' **42/83 (50.6%)**. Given that weak temporal signal is the expected outcome here (§4.3), a method that raises dating convergence from 51% to 76% on real lineages is directly on point. Agreement with Gubbins where both worked: ICC 0.87 for substitution rates. On PMEN1 it matched Gubbins on root-to-tip R² (0.51 each) and dated the root to 1970 against Gubbins' 1974 and the published 1972.

**Two hard limits on Verticall.** It is **O(n²) and timed out at 4,857 genomes** — fine per cluster, useless species-wide, and it will not rescue the backbone. And **Verticall *alignment* must never be used for anything you intend to date**: it under-filters badly (median 2 recombination blocks per genome against Gubbins' 17 on PMEN1), recovered no more temporal signal than no filtering at all (R² 0.17 vs 0.15 unfiltered), and dated PMEN1's root to **1701 [1186–1915] instead of ~1972**. It is still a preprint (bioRxiv 2026-04-24), so treat it as a second arm and a robustness check, not as the primary.

**Do not spend compute on pangenome graphs.** This is the item on the list most likely to look attractive and cost months. Pandora — the tool purpose-built for bacterial pangenome graphs — reports **~11% loss of recall at core SNPs** and a 20–30× higher error rate than snippy, winning only on rare and accessory variants. pggb's published bacterial ceiling is 500 complete *E. coli* at 41.4 h and 210.9 GB; drafts have never been benchmarked; and `-x auto` — the one mechanism that makes it tractable at your scale — assumes something like panmixia, which is the assumption a restriction-modification-structured organism most clearly violates. There is no graph work anywhere in *Burkholderia*, and PulseNet's answer to reference sensitivity was wgMLST, not graphs.

**Differs from your pipeline:** pins the version and adds a second arm. **Differs from Seng:** Gubbins v3.1.3. **Differs from Wu:** Gubbins v2.4.1, four major versions behind.

---

### 2.7 [C] Split by replicon before Gubbins — forced by the tooling, useful for the science

**What.** Split the alignment into chromosome I (columns 1–4,074,542) and chromosome II (4,074,543–7,247,547) **before** Gubbins, and run Gubbins twice. Preferred route: `ska map` → VCF → split on `CHROM` → two alignments. `pipeline_checks_bp.py split` implements the split and **refuses to run unless `aln_len == sum(replicon lengths)`**.

**Why — this is not a preference, it is three independent breakages.**

1. **`snippy-core` concatenates with no separator.** Verified in source: it joins per-contig sequences end to end in reference order, so **K96243 position 4,074,542 sits immediately adjacent to chromosome II position 1**. `core.txt` gives no per-contig breakdown. Nothing in the Snippy README warns about this.
2. **Gubbins scans with a 0.1–10 kb sliding window and has no concept of contigs.** Any window overlapping the junction spans both chromosomes across a step change in polymorphism density — and chromosome II carries the higher density, so the background used for the null becomes a mixture of two regimes. The words *contig*, *plasmid*, *replicon*, *chromosome* and *draft* do not appear in the Gubbins manual, and it has **no `--mask`, no BED input, no per-contig option**. Theiagen's docs state the incompatibility flatly: *"If reference genomes have multiple contigs, they are incompatible with Gubbins."*
3. **`snp-sites` hardcodes VCF `CHROM` to the literal `"1"`** and reports `POS` as the alignment column index. A chromosome II SNP is therefore reported on chromosome "1" at an offset of 4.07 Mb. **This is the single most likely place in the pipeline for a silent off-by-4.07-Mb error.**

**Why it is also good science, not just damage control.** The mechanistic case is stronger than "chromosome II is more divergent." Dillon 2015 (PMID 25971664), 47 mutation-accumulation lines of *B. cenocepacia* over >5,550 generations: base-substitution rates differ significantly across the three replicons (χ² = 6.77, d.f. = 2, P = 0.034), and are **highest on chromosome I and lowest on chromosome II — the opposite of the observed evolutionary rates.** So chromosome II's elevated divergence is selection and recombination, not mutation. One clock and one substitution model across a concatenation is therefore **mis-specified**, not merely imprecise.

**Run `pipeline_checks_bp.py junction` on the Gubbins GFF regardless.** A recombination block that *spans* a junction cannot be a real event — it is an artefact by construction, and its presence proves Gubbins was run on a concatenation.

**Differs from your pipeline:** adds a mandatory split. **Same as Chewapreecha**, who split and ran BEAST per chromosome — though she never states why; there is no methodological argument in the paper. **Differs from Seng**, who ran the concatenated path end to end, from the same lab, with no mention of the change. **Nobody has published a concatenated-versus-per-replicon comparison for any organism** (§3, item 6), so running both on one cluster is nearly free and is a contribution.

---

### 2.8 [G] Masking: repeats only, by default

**What.** Mask **repeats only** as the primary analysis, via `ska map --repeat-mask`. Build a genomic-island / prophage / IS mask and run it as a **sensitivity analysis**, not as the primary. Use `mask_gubbins_aln.py --missing-char N` (the default is `-`, a gap).

**Why.** The line is: **mask what you cannot reliably call; do not mask what you can call but expect to be recombinant.** Repeats fall on the first side; prophage and genomic islands on the second.

- **Gubbins' authors say pre-masking is unnecessary**: "there is no need to remove accessory genome loci, as the algorithm should cope with regions of missing data," and their showcase result is a recombination detected across almost the entire 44.7 kb φSa3 prophage, with edges 680 and 96 bp inside the annotated boundaries. Yet **their own helper script runs `ska map --repeat-mask`** — which is exactly the repeats/MGE distinction above.
- **Over-masking fails mechanically.** Gubbins issue #392: SKA2 repeat-masking took 217 *M. kansasii* genomes from <10% N to >40% N, and `--filter-percentage` (default 25) silently dropped them. Croucher's own group's answer is `--filter-percentage 100.0`.
- **Over-masking fails statistically.** Hedge & Wilson: "removing recombining sites can **exacerbate** branch length distortion," because older events are easier to detect, so masking preferentially strips substitutions from deep branches and makes trees look more star-like.
- **The only benchmarked bacterial mask shrank 2.7-fold under scrutiny.** Marin 2022 (PMID 35020793) found **68% of the positions routinely excluded from H37Rv are accurately called**, and replaced a 469,501 bp (10.64%) legacy mask with 177,077 bp (4.01%). The trade-off number to quote: masking repetitive content cost **15 points of recall for half a point of precision**.
- **The one prospective test recommends no masking at all.** Gorrie 2021 (PMID 35544081), 1,537 genomes across four organisms and eight hospitals: "Omitting prophage regions had minimal effect; however, **omitting recombination regions had a highly variable effect, often inflating the number of closely related pairs**," concluding for a closely related reference "without masking of prophage or recombination regions."

**There is a citable disagreement here** — Lees 2018, from the same institute as Gubbins, says "the best practice is to try to remove these regions before performing phylogenetic reconstruction." Present it as a disagreement and run it both ways rather than resolving it by assertion. **Given Gorrie, Hedge & Wilson and Marin, the unmasked run has the better prior and should be the primary.**

**If you build the mask anyway**, the coordinates exist and **there is no published K96243 BED** (§3, item 9). IslandViewer 4 holds precomputed predictions keyed on **RefSeq accessions only** — `NC_006350.1` (analysis id 15999, 64 integrated GIs) and `NC_006351.1` (id 16000, 16); the EMBL accessions `BX571965`/`BX571966` are absent from the database entirely. Cross-reference Holden 2004's 16 islands (6.1% of the genome) and Tuanyok 2008's 71-GI nomenclature. Add prophage from geNomad or PhiSpy — not VirSorter2 alone, which systematically overextends boundaries into host regions — and IS elements from ISEScan. **Mirror the IslandViewer files locally**: the database has not been refreshed since 2024-09-06, the download endpoints are undocumented internals, and the sister tool's funding notice reads "until at least the end of August, 2026." Report the total fraction masked, and treat anything far above ~6% plus repeats as suspicious.

**Differs from your pipeline:** makes the masking policy explicit and inverts which run is primary. **Differs from Seng**, who masked "genomic islands" with no definition, citation or coordinate file.

---

### 2.9 Ascertainment bias: `-fconst`, never `+ASC`

**What.** Per cluster, per replicon:

```bash
# constant-site counts from the MASKED FULL-LENGTH alignment, never the SNP file.
# put the least-masked genome first: snp-sites -C reads base identity off sequence #1
snp-sites -C cluster01_chr1.masked.aln > cluster01_chr1.fconst
snp-sites -c cluster01_chr1.masked.aln > cluster01_chr1.snps.aln

iqtree2 -s cluster01_chr1.snps.aln \
        -fconst "$(cat cluster01_chr1.fconst)" \
        -m MFP -T 4 -B 1000 --alrt 1000 --prefix cluster01_chr1.tree
```

**Assert `len(SNP aln) + sum(fconst) == len(masked aln)`, and fail the pipeline if it does not close.** `pipeline_checks_bp.py fconst` implements this.

**Why, and the reason is compositional rather than procedural.** These are Leaché's two distinct corrections: `+ASC` is the conditional-likelihood method, `-fconst` the reconstituted-DNA method, and only the latter lets you specify counts per base. **K96243 is 68.06% GC — A 15.9 / C 34.1 / G 33.9 / T 16.0.** A flat assumption is wrong by more than a factor of two in both directions. In a controlled test, `-fconst` with true counts reproduced the full-alignment base frequencies and tree length **exactly**, while `+ASC` and flat counts both collapsed to ≈25/25/25/25. Leaché's magnitudes: uncorrected overestimates tree length "over 4-fold," conditional likelihood "overestimates branches by 100%," reconstituted DNA keeps "most branches within 25%."

**Three traps that will bite silently.**

- **`+ASC` does not inflate branch lengths quietly — it hard-errors**, and the hazard *is* the remedy. The trigger is `frac_invariant_sites`, meaning "constant *or ambiguous constant*." A Gubbins-masked column retaining one real base plus gaps is ambiguous-constant, trips the error, and IQ-TREE helpfully writes a `.varsites.phy`. **Rerunning on that file silently deletes exactly those columns.**
- **`-fconst` and `+ASC` are mutually exclusive by construction, not by convention.** `-fconst` literally synthesises constant columns and appends them, which guarantees `frac_invariant_sites > 0`, which guarantees the `+ASC` error. Note there is no long form: only `-fconst`, comma-separated A,C,G,T, no spaces.
- **`snp-sites -C` has three failure modes.** It returns `0,0,0,0` on a polymorphic-sites file, so it must run on the full-length alignment; it silently ignores `-c`; and **it reads base identity off the first sequence only**, so with a masked alignment constant sites are undercounted in proportion to the first taxon's masked fraction. Order the least-masked genome first, or compute the counts yourself — `pipeline_checks_bp.py fconst --recount` does.

**A note on the alternative, because it is defensible.** Retaining constant sites and skipping correction entirely (Wu's route) removes an entire error class at the cost of alignment size — and the cost may be smaller than it looks, because in a clean full-length alignment constant sites collapse into ~4 extra site patterns. **But Gubbins masking destroys pattern compression** — every taxon gets a different gap pattern — and the penalty scales with recombination load, which is the worst case for this organism. Measure it: `raxml-ng --parse` on one real masked cluster reports the distinct-pattern count and settles this in minutes. **No benchmark exists at ~500 taxa × 3.8 Mb**, so measuring it is itself a small contribution.

**Differs from your pipeline:** makes the correction explicit and adds the closure assertion. **Differs from Seng**, who used `TVM+F+ASC+R6` on a snp-sites alignment with no constant-site counts. **Differs from Wu**, who retained constant sites and applied no correction. Both are credible groups doing opposite things, so **this is a choice to argue, not a bug to fix** — but the GC composition argues for `-fconst`.

---

### 2.10 Tree building

| Scale | Tool and invocation | Why |
|---|---|---|
| **Backbone, 61–101 taxa [G]** | **IQ-TREE 3**, `-m MFP -B 1000 --alrt 1000` | Replaces parsnp/FastTree. Minutes at this taxon count, and **backbone errors are unrecoverable downstream**. In the only bacterial benchmark, parsnp ranked 5th where IQ-TREE ranked 2nd. |
| **Per cluster, ≲500 taxa [C]** | **IQ-TREE**, `-fconst …`, `-m MFP -T 4 -B 1000 --alrt 1000`, **many clusters concurrently** | IQ-TREE parallelises *along the alignment*, so a short SNP alignment saturates at few threads and can run **slower** with more cores. Parallelise across clusters, not within them. |
| **Global ~3,000 taxa [G]** | **RAxML-NG**, `--parse` first, then `--all --bs-metric fbp,tbe --threads auto --workers auto` | Treat as a validation exercise against the grafted tree, not the production object. |
| **Any SNP alignment** | **Never VeryFastTree** | It **cannot do ascertainment correction at all** — disqualifying. |

**The benchmark behind this** (Lees 2018, PMID 29774245; Kendall–Colijn at λ=0, where ~286 is random): RAxML 4.63 in 806 min; IQ-TREE slow 11.2 in 703 min; **IQ-TREE `-fast` 11.3 in 14.6 min**; parsnp 14.0; **FastTree 16.0 in 189 min**. So `-fast` is 48× faster than full IQ-TREE for 0.1 KC units, and is both more accurate and 13× faster than FastTree.

**Two things to know about FastTree if the backbone stays on it.** Its support values are an SH test over the three NNI topologies around a single branch — **purely local**, so it cannot detect that a clade is wrong because of a distant misplacement, which is the dominant error mode at high taxon counts. It scored the lowest AUC (0.876) of any support measure tested, with calibration error 0.055. And across 19 empirical datasets IQ-TREE found the higher likelihood in all 17 supermatrices, while FastTree's median normalised RF from the best tree exceeded 0.33 with "many incongruent splits receiving high bootstrap support." **Also worth confirming: `parsnp` appears to use FastTree 2 internally, which would mean your backbone inherits all of this whether or not you invoke FastTree by name.**

**Support at ~3,000 taxa: use TBE, and report both.** Felsenstein's bootstrap "tends to yield very low supports, especially on deep branches" at this size (Lemoine 2018, PMID 29670290). `--bs-metric fbp,tbe` gives both in one RAxML-NG run, so you can *demonstrate* the classical-bootstrap collapse rather than assert it. Note that IQ-TREE's `--tbe` works only with standard bootstrap `-b`, not UFBoot `-B` — a further reason to run the global tree in RAxML-NG. Per cluster, use UFBoot2 and trust a clade at **SH-aLRT ≥ 80% AND UFBoot ≥ 95%**; never compare UFBoot percentages to classical bootstrap percentages.

**Differs from your pipeline:** replaces parsnp/FastTree on the backbone. This is the single most defensible cheap change available.

---

### 2.11 [G] The merge — and what to do about it now **[B]**

**What, for Paper A.** Build the global backbone **directly** with IQ-TREE 3 on cluster representatives. Keep the grafted tree if you want it, but **label it topology-only, with branch lengths explicitly not interpretable**, and cite PopPIPE including its authors' own disclaimer. Adopt PopPIPE's **branch-length rescaling onto a single global distance scale before grafting** — that is the step your implementation is missing entirely.

**What, for Paper B.** Replace representative-grafting with **GTM** (Smirnov & Warnow 2020, PMID 32299343), whose merge **provably minimises topological distance to the guide tree** — a guarantee representative-grafting does not have, and the method that succeeded at 50,000 sequences where RAxML-NG and IQ-TREE 2 both failed. Benchmark against SimBac at *B. pseudomallei* parameters (work-plan item 19). The related literature you are also not citing is NJMerge (can fail to return a tree; O(n⁵)) and TreeMerge (fixes both).

**Why the claim narrows and improves.** ARETE does cluster-then-per-cluster-recombination at **>10,000 genomes** and BigBacter does it in routine public-health surveillance — **both stop deliberately before merging the trees.** PopPIPE is the only bacterial pipeline that grafts, and it calls the output a visualisation that "will not maximize the phylogenetic likelihood." The graft is proven at scale only in SARS-CoV-2 (COG-UK grapevine, `virus-evolution/phylopipe` via `clusterfunk graft`), where recombination is assumed away and neither implementation is published. **So the unsolved piece is specifically the merge, under recombination.**

**One thing to check before citing PopPIPE as precedent for your whole architecture.** Its rule chain reads `split_strains → sketchlib_dists → generate_nj → ska_build → ska_align → iq_tree → graft_tree`, while `gubbins` sits under a separate `transmission` target consuming `ska map` alignments. On that reading, **PopPIPE's grafted tree is assembled from subtrees that were never recombination-corrected.** This is inferred from the Snakefile rule graph, not stated by the authors, and it decides whether PopPIPE is a precedent for the whole design or only the clustering half. **One run settles it** — work-plan item 7.

**Note what GTM does and does not fix.** Its guarantee is **topological**. It solves "which edges connect the subtrees" and leaves the branch-length-unit problem — masked subtree lengths against an unmasked backbone — completely untouched. That residual is the actual open problem, and framing it that way is both more honest and more interesting than "we grafted trees."

**And name the residual risk to the novelty claim honestly:** the "nobody has done this" statements rest partly on exhaustive GitHub code search, which cannot see GitLab, Bitbucket or institutional Git hosts. A public-health-agency pipeline on a private host would have been missed.

**Differs from your pipeline:** demotes the graft from analysis substrate to labelled visualisation, adds rescaling, and names GTM as the principled replacement. **Differs from Chewapreecha and Seng:** neither grafted at all.

---

### 2.12 [C] Dating: test everything, expect failure, report it as a result

**What, per cluster per replicon, in order.**

0. **Screen, don't test.** Record *n* tips, *n* dated tips, sampling window, tree length in substitutions, and **Mantel r/p** between cophenetic genetic distance and temporal distance. Clusters with significant Mantel correlation are confounded, and no unclustered test may be applied to them. Sampling windows under 10 years are a prima facie exclusion (Duchêne 2016).
1. **Root-to-tip as a figure with a slope, never as a test.** Do not report R² as a test statistic and do not report the built-in permutation p-value.
2. **Clustered date-randomisation with CR2** where feasible, reporting the number of unique permutations available.
3. **BETS as the primary test**, with Tay 2024's diligence. It does not scale to 61–101 clusters × 2 replicons × 4 models, so run steps 0–2 on everything and BETS on the survivors plus a random negative-control subset.
4. **Where BETS is infeasible**, `bactdate()` with real dates versus all-dates-equal, compared with `modelcompare()` on the DIC scale, reported as an approximation.
5. **Use the two replicons as an internal replicate** — Chewapreecha's "consistent clock-like behaviour across both chromosomes" is a principled concordance criterion that single-replicon organisms do not afford.
6. **Post-hoc diagnostics on every dated tree reported** (DiagnoDating).

**Why BETS rather than date-randomisation, and this is the key methodological choice.** **BETS can positively support the *absence* of temporal signal; the date-randomisation test can only fail to reject.** For a study whose expected outcome is negative, that asymmetry is decisive. And the standard test is specifically broken here: Murray 2016 showed that where temporal and genetic structure are confounded — which an assembled multi-study collection guarantees — over a third of replicates passed while giving a tMRCA of 51 years against a true 10,000. Their danger zone is "fewer than 7 substitutions per genome" across the window; **this collection computes to 7.1**, from metadata alone.

**BactDating settings that are not the defaults.**
- **`model="arc"` or `"carc"`**, not strict. Standard uncorrelated relaxed clocks have excess variance proportional to *l*², violating additivity, so **estimates shift when genomes are added or removed** — and here cluster membership is itself inferred, so a non-additive clock means the dates move when the clustering moves. Seng used v1.1.1 with a strict clock, which is doubly superseded: by additivity, and by Tay 2024's finding that **strict clocks carry the highest type-I error** in temporal-signal classification.
- **`useRec=T` is not the default** — without it the Gubbins per-branch recombination information is silently discarded.
- **Missing dates are inferred natively**, so do not drop the 38.2% undated. Assert `ncol(per_branch_statistics) %in% c(11, 13)` per cluster: `loadGubbins()` branches on that and otherwise falls through to a different formula with no warning.
- **`clusteredTest()` is not what it sounds like.** It deletes data until the confounding is undetectable, then applies the ordinary uniformly-permuted test to the residue, with no exposed seed. **Use its Mantel component as the diagnostic; do not rely on its p-value.**

**The rate prior.** Impose the **union of the two in-organism sources, ~1.3 × 10⁻⁷ to 2.3 × 10⁻⁶**, and report how far the answer moves across it. Cite Pearson 2020 directly for 1.7 × 10⁻⁷ (95% HPD 1.3–2.1 × 10⁻⁷). Remember BactDating's μ is per genome per year, so **per-replicon analysis requires multiplying by the replicon length actually in the alignment, not the 7.2 Mb total.**

**Differs from your pipeline:** replaces date-randomisation-as-gatekeeper with a screen-then-BETS protocol. **Differs from Chewapreecha:** she used an unconventional permutation (randomising root-to-tip distance rather than dates), a strict clock, and reported percentile ranks that four of five clusters fail. **Differs from Seng:** strict clock, BactDating v1.1.1, and a date-randomisation result never published.

---

### 2.13 [C+G] Phylogeography: stochastic mapping, permutation-tested

**What.**

1. **Subsample balanced on country × BioProject × year**, at **n = 100 per country** rather than Chewapreecha's 15 — 8 countries, 800 genomes, 14.5% of the collection, and it keeps India and the USA in. Justify it as a sample-size-driven choice, not by citing her for the number.
2. **`make.simmap` on the substitution-scaled per-cluster trees.** No dated tree is required — `make.simmap` needs only a `phylo` object, confirmed at code level (zero occurrences of `ultrametric` in `make.simmap.R` or `fitMk.R`).
3. **Fit ER, SYM and ARD; default to ER.** Report ΔAIC and Akaike weights for transparency but **do not treat an ARD win on AIC as licence** — at 30 free parameters from ~90 tips this is exactly the "character data is limited" regime where ER is reported to outperform ARD even when the truth is asymmetric, and better-fitting models are documented not to be more accurate. Where the question genuinely needs asymmetry, report both and show the conclusion does not depend on it.
4. **`Q="mcmc"`**, not the `"empirical"` default, so rate-matrix uncertainty propagates rather than conditioning on a point estimate.
5. **`pi="equal"`, stated explicitly** — or report both flat and the sampling-corrected `pi = (n_i/s_i)/Σ(n_j/s_j)`, with s_i from the burden estimates, and show the difference. **Never `pi="estimated"`**, which derives the root prior from a rate matrix fitted to tip states whose frequencies *are* the sampling distribution.
6. **Tip-state-swap permutation null.** Permute country labels across tips holding topology and branch lengths fixed, re-run, and compare observed transition counts and root-state frequencies against the null. **Then repeat permuting BioProject labels.**
7. **Report the full rate matrix with its uncertainty across resamples** — Chewapreecha reports none, and this is a strict improvement at no methodological risk.
8. **Report SAASI alongside** as the one sampling-aware method that runs at this scale (fixed tree, validated to 100,000 tips).

**Why the permutation null is the highest-value item here.** It is the mechanism behind Gámbaro 2025's adjusted Bayes factor, it needs no new software, and applied to BioProject labels it is **the only handle anyone has found on the study-of-origin confounder**. It answers the question a reviewer will actually ask: is this signal distinguishable from the sampling composition?

**What you must not report from this.** Occupancy times on an undated tree (§4.2). Node-level posteriors pooled across resamples (§4.2). And note that on a phylogram **Q has units of expected geographic transitions per substitution per site**, so comparing Q across clusters whose substitution rates differ silently conflates the molecular clock with the geographic process — report Q per cluster, and do not pool it.

**Differs from your pipeline:** adds the permutation null, the BioProject stratum, explicit `pi`, `Q="mcmc"`, and the ER default. **Differs from Chewapreecha:** phytools 2.5-2 against her 0.5-10, ER rather than an unexplained ARD override, a reported rate matrix, and a permutation null she did not run. **Differs from Seng:** they subsampled by province at n=15, the same design one level down.

---

## 3. Novelty and contribution, ranked

The gap documents flag roughly two dozen documented absences. Most are absences because nobody needed the thing; a few are absences because the thing is hard and load-bearing. This section sorts them, and states what evidence each needs to survive review.

**The sorting criterion is not "has anyone done this?" but "would a competent reader change what they believe?"** An absence that nobody has noticed is only a contribution if filling it moves a conclusion.

### Tier 1 — real contributions, evidence largely in hand

**1. The sampling frame is inverted against disease burden, and nobody in this literature has said so.**
This is the strongest item in the whole set, and it is the one to lead with. It needs no model, no simulation and no new data: it is Limmathurotsakul's burden estimates joined to a genome audit. The claim is not "sampling is biased" — everyone says that — but that **the country label is a proxy for national sequencing capacity and is anti-correlated with predicted burden across the two largest endemic regions**, with 33% of global burden at zero genomes.
*Evidence needed:* the region- and country-level tables (in hand), plus the honest caveat that the genome side is clinical-plus-environmental (`GAP4 §1`). Reproduce the audit with `bioproject_accession` retained so the numbers are checkable.
*Risk:* low. The main failure mode is over-claiming — a reviewer will accept "the sampling frame cannot support inference X" and reject "therefore the true history is Y."

**2. Study of origin (BioProject) as a phylogeographic confounder, with the first worked handle on it.**
Searched for and not found: any bacterial-genomics paper treating BioProject as a random effect, blocking factor or stratification variable. The problem is documented — Blackwell 2021 (PMID 34752446) found **50% of 661,405 ENA genomes come from 50 of 23,316 projects** — but the correction is not. You can supply two things nobody has: **the measured intra-cluster correlation** of core-SNP variance between versus within BioProjects, and a **tip-state-swap permutation null on BioProject labels**.
*Evidence needed:* work-plan item 5 (the ICC measurement) and item 17 (the permutation null). Both are days, not months.
*Why it is a real contribution rather than a curiosity:* it converts "effective sample size is somewhere between 5,515 and 27" into a number, and it generalises — every large public-data reanalysis in bacterial genomics has this problem and none of them addresses it.

**3. There is no well-supported between-host molecular clock for *B. pseudomallei*, established systematically rather than anecdotally.**
Both existing precedents are thinner than they appear: four of Chewapreecha's five dated clusters fail their own test once the percentile ranks are read correctly, and Seng dated 17 of 1,391 isolates and never published their test result. A systematic BETS assessment across all clusters — with the pass/fail table as a primary result, on the Menardo 2019 template — makes this a measured finding rather than a reading of two papers.
*Evidence needed:* the per-cluster screening protocol in §2, with BETS on survivors plus a random negative-control subset. The critical design choice is **BETS rather than date-randomisation, because BETS can positively support the absence of signal** while date-randomisation can only fail to reject.
*Risk:* this is the headline negative result, and it is publishable — but only if every cluster is tested and the failures are reported as data. Testing a few and reporting the failures as a limitation is not the same paper.

**4. The subtree merge under recombination.** **[B]**
The honest form of the claim is narrower and stronger than "the graft has no precedent." ARETE does cluster-then-per-cluster-recombination at >10,000 genomes and BigBacter does it in routine surveillance, both **stopping deliberately before the graft**. PopPIPE grafts, but rescales onto one global distance scale first and its authors call the product a visualisation that "will not maximize the phylogenetic likelihood" — and its Gubbins appears to sit off the path feeding `graft_tree`. The graft is proven at scale only in SARS-CoV-2, where recombination is assumed away. **So the unsolved piece is specifically the merge, under recombination, with branch lengths in reconcilable units.**
*Evidence needed:* SimBac benchmarking at *B. pseudomallei* parameters on a two-replicon 7.2 Mbp genome (work-plan item 19), a comparison against the existing merge literature you are currently not citing (NJMerge, TreeMerge, and especially **GTM**, Smirnov & Warnow 2020, PMID 32299343, whose merge *provably minimises topological distance to the guide tree*), and a demonstration that the merged tree supports an inference per-cluster trees cannot.
*The caveat that matters:* GTM's guarantee is **topological only**. Adopting it fixes the "which edges" problem and leaves the branch-length-unit problem untouched. That residual is the actual contribution, and it should be framed that way rather than as "we grafted trees."

### Tier 2 — real but narrower; cheap, so take them

**5. Balanced-subsample re-clustering with a partition-agreement statistic.**
No bacterial precedent, and it directly answers "is my population structure biology or sequencing history?" Report ARI between the full-data partition and *B* balanced-subsample partitions (balanced on country, and separately on BioProject) as a distribution. Cite PopPUNK for the ARI machinery and Meirmans 2018 for the motivation — she found unbalanced sampling drove 10 of 12 species to a spurious *K*=2 that balanced subsampling dissolved. *Cost: hours.*

**6. Concatenated versus per-replicon phylogeny, compared explicitly.**
Nobody has done this **for any organism**, and this lab has done it both ways without comment (Chewapreecha split, Seng concatenated). You are forced into the split by the tooling anyway, so the comparison is nearly free. The mechanistic argument makes it more than bookkeeping: Dillon 2015 showed the *B. cenocepacia* chromid has the **lowest** spontaneous mutation rate of the three replicons yet the **highest** observed evolutionary rate, so a single clock across a concatenation averages over two replicons under different regimes. *Cost: low, given the split is already required.*

**7. Whether clustering tracks clonal descent under high r/m.**
Nobody has tested whether BAPS-family or PopPUNK clusters recover clonal descent at these recombination levels; the two reassuring results both score against deme membership or simulated tree nodes, from models with no recombination process. **The same SimBac run that benchmarks the merge answers this**, so two contributions come out of one simulation. *Cost: shared with item 4.*

**8. Reference-choice sensitivity in *B. pseudomallei*.**
Distance-to-reference predicts recall at ρ = −0.94 across 209 pipelines and ten species (Bush 2020), worst for recombinogenic organisms; this organism spans 0.73–5.61% from K96243; and **recombination inference is itself reference-dependent**, which puts Gubbins downstream of an unvalidated choice. Only one small study has ever varied the reference in this organism (Webb 2022). Running ≥2 references and reporting concordance is standing good practice that here doubles as a result. *Cost: doubles the mapping step.*

**9. A published masked-region BED for K96243.**
None exists, but the coordinates do — Holden 2004 (16 GIs, 6.1% of the genome), Tuanyok 2008 (71 GIs across five strains), and IslandViewer 4's precomputed predictions for both replicons. Mirroring and publishing these is a small, genuine community contribution, and the IslandViewer database froze 2024-09-06 on month-to-month funding, so the mirror has independent value. *Cost: an afternoon.*

### Tier 3 — absences nobody cared about, or that exist for good reasons. Do not chase these.

- **Structured coalescent applied to *B. pseudomallei*.** Absent because it is a bad idea here (§4.1) and would not run. Filling this gap would be a mistake presented as novelty.
- **ARG methods on bacteria** (tsinfer/tskit, ARGweaver, Relate, SINGER, TreeMix, f3/f4/qpAdm). Absent because the bacterial ARG ceiling is 23 taxa × 53 loci at ~a week per chain, and the authors call the problem "not in any way solved." Two orders of magnitude short; not your problem.
- **GLM-extended DTA benchmarked under sampling bias.** A real absence, but it is a virology methods paper, not this one.
- **A phylogenetic effective sample size for a discrete trait**, and **inverse-probability tip weighting inside a phylogenetic likelihood.** Both are genuine, interesting statistical holes. Both are separate statistics projects. **Name them as future work and label your Kish calculation an ad hoc descriptive statistic** — which is the honest move and costs nothing.
- **Published justification for one-isolate-per-patient deduplication**, **per-field metadata-completeness statistics for public archives**, **a non-dated BDSky/MTBD variant**, **a phytools facility for pooling maps across different tip sets.** All real absences; none changes anyone's conclusions. The last is worth one methods sentence as a caveat, not a contribution.
- **ChromoPainter/fineSTRUCTURE on *Burkholderia*.** Genuinely absent and technically feasible (4,067 *H. pylori* genomes in one published run; van Hal 2022 at 1,128 *E. faecium* is an adoptable template). It sits on the Tier 2/3 boundary. **Take it only if the question is direction and quantity of gene flow, which trees structurally cannot answer.** Do not take it expecting it to rescue the sampling problem — Yahara's own caveat is that "sampling bias will have strong effect on inference of population structure and admixtures," and painting cannot date anything.

### The one Tier-1-shaped opening that needs more than you have

**Re-examining the Australian-origin hypothesis on sampling-bias grounds.** Searched for and not found — nobody has done it, and it is the most interesting question in the set. But the sampling critique cuts *less* deeply here than elsewhere, which is what makes it hard rather than easy: Pearson 2009 ran STRUCTURE on a **near-balanced** sample (45% Australasia, 47% Southeast Asia) with two explicit anti-bias checks. So the naive critique fails.

What is actually open is the alternative Chewapreecha names and does not exclude: "**there have been repeated population bottlenecks outside Australia, but not within it.**" That is precisely the recent-bottleneck-versus-admixture pair that Lawson 2018 shows is indistinguishable from a bar plot — and neither PCA nor an F_ST tree separates them either.
*Evidence needed to make this a contribution rather than a complaint:* **badMIXTURE-style co-ancestry residuals**, or a demographic model fitted per region, testing whether an admixture history explains the data better than a bottleneck history. That is real work and it is not in the current plan. **Add it only if you want this to be the paper's scientific punchline; otherwise state the alternative, cite Lawson, and leave it open.**

---

## 4. Claims we cannot make

Stated plainly, because the risk is building the paper around one of these and discovering the problem at review. Each entry gives the claim, why it fails, and what — if anything — is salvageable.

### 4.1 Hard exclusions — do not attempt these analyses at all

**"Lineages moved from Southeast Asia into Australia" (or any directional between-country migration rate).**
This is the single most dangerous available conclusion, because it is *manufactured by the bias*. SAASI's benchmark (Song 2026, PMID 42115598): "if state *i* is far less sampled than state *j*, `ace` **overestimates the transition rates from other states to state *i*** and underestimates transition rates from state *i* to other states." Australia is the under-sampled state relative to Thailand. A result of this shape is indistinguishable from the artefact and will be read as such. Not salvageable by subsampling — see 4.2.

**Any BEAST discrete trait analysis (mugration) on the unweighted collection.**
De Maio's no-data experiment returned a posterior migration log-ratio of 1.7 from sampling counts alone with zero sequence data. `GAP4 §4.3` shows the closed form: under an equal-rates Mk model the root conditional likelihood depends on the data only through state counts, and on the observed country counts it puts posterior **1.0000 on Thailand with a log₁₀ Bayes factor in the hundreds**. That number carries no information the sample-size table does not already carry. Do not report it.

**MASCOT, BASTA, MultiTypeTree, SCOTTI or bdmm over country demes.**
Two independent disqualifications. They are biased in the direction that makes singleton countries the migration hubs (Layan 2023), and they will not run: BASTA is O(N·S³)/O(N²·S²), the largest true geographic structured-coalescent analysis in *any* bacterium is 260 *V. cholerae* genomes across 11 demes, and MASCOT's own authors cap the usable state count at "three or four." You have ~37 country labels.

**Multi-type birth–death (MTBD/BDSky) for the geographic question.**
Beyond the deme ceiling of two or three, the model mismatch is fatal: birth = transmission, death = recovery. Melioidosis is acquired from soil, not transmitted person to person. The parameterisation has no epidemiological interpretation at country scale. And `GAP4 §10` records a further hard asymmetry — these models are defined in per-calendar-time rates, so unlike stochastic mapping they do **not** survive a dating failure.

**A single global dated tree.**
Nothing in the evidence supports one. Chewapreecha did not build one; she dated per cluster, per replicon. §4.3 below explains why dating at all is doubtful.

**ADMIXTURE or STRUCTURE on the full collection.**
Lawson, van Dorp & Falush 2018 (PMID 30108219): unbalanced sampling changes both which group appears unadmixed and the inferred *K*, and "the problem is fundamental to any approach based on equally weighing samples." Worse for this specific question, their §3.2 shows a **Recent-Bottleneck** history and an **Admixture** history produce indistinguishable bar plots — and the recent-bottleneck alternative is exactly the one Chewapreecha names and does not exclude.

### 4.2 Claims that survive the analysis but not the interpretation

**"Balanced subsampling corrected for the bias."**
It does not, and at this bias level it may make things worse. The SAASI authors benchmarked `ace` and `simmap` directly: once you count the internal nodes downsampling deletes, "the accuracy drops dramatically, and is substantially lower than reconstructions on the full tree." Their breakpoint sits between 4× and 10×; Thailand:Australia is ≈5.8× and the within-Thailand study-level imbalance is far worse. Layan's endorsement of subsampling is explicitly regime-qualified to "intermediate sampling bias." **Subsample, report what it cost, and never describe it as having removed the problem.** At Chewapreecha's own *n*=15 the rule retains 225 of 5,515 genomes (4.1%) and discards 22 countries entirely.

**A map, or any figure implying global coverage.**
At *n*=15 the design says nothing about Papua New Guinea, Ghana, Madagascar, South Africa, Ecuador or any South American country, and the collection says nothing about Indonesia, Nigeria, Myanmar or Cambodia at any *n*. A choropleth invites the reader to interpolate across the 29 zero-genome countries that carry a third of global burden. If a map appears, it must show sampling intensity, not inferred ancestry.

**"Thailand" as a population.**
It is three BioProjects, and the largest — PRJEB3409, 26.3% of the entire global collection — is a **case-control study, 56.9% environmental, 93.6% undated**. Isolates were selected by outcome, not sampled from a population. Any statement about "Thai *B. pseudomallei*" is a statement about that study design. Note the knock-on: ~15% of the whole global collection is environmental isolates from one Thai study, so every burden comparison is clinical-plus-environmental, not clinical.

**Occupancy times from stochastic character mapping ("total time spent in Australia").**
`make.simmap` runs fine on an undated, substitution-scaled tree — but `maps`/`mapped.edge` record times *in the tree's own branch-length units*. On a substitution-scaled tree "time spent in Thailand" becomes "substitutions accumulated in Thailand," confounding residence with lineage-specific rate. Chewapreecha reported both transition counts and occupancy times; **only the first survives an undated tree.**

**Node-level posterior probabilities pooled across resampled trees.**
`GAP4 §10.2`: every phytools summarisation facility assumes a shared topology and tip set, and a Chewapreecha-style "subsample, re-run, repeat 1,000 times" design produces neither. Internal nodes are not the same nodes across replicates. Only tree-level scalars — transition counts and root state — are poolable, and they pool as a **distribution over replicates**, not a Bayesian posterior. Say so in the methods.

### 4.3 Dating — plan for the negative result

**There is currently no well-supported between-host molecular clock estimate for this organism.** That is the finding, and it should be stated as one.

- Chewapreecha dated 5 of 19 clusters, **59 of 469 isolates (12.6%)**. Read correctly as percentiles, **four of those five fail their own date-randomisation test**; only Group 8 (92nd, 97th) approaches acceptable. Group 6 was dated on an R² of 0.0189. The whole-dataset root-to-tip regression was R² = 0.00323, with the authors' own caption stating it "rejects the influence of sampling time."
- Seng dated **17 isolates of 1,391 (1.2%)**, reported rate and TMRCA only inside a supplementary figure panel, and **never published their date-randomisation result at all** — established by exhaustive search of main text, SI and Peer Review File.
- The two in-organism rate sources **disagree by 4–10×** (Chewapreecha 6.26 × 10⁻⁷ – 1.81 × 10⁻⁶; Pearson 2020 1.7 × 10⁻⁷), the ordering is not monotonic in timescale, and the epidemiological middle of the range is empty — the two long-window outbreak studies most likely to fill it (Chapple 2016 over 25 years, Webb 2020 over 51) both report *absence* of temporal signal and decline to fit a clock.
- The standard test is **anticonservative under exactly this data structure**. Murray 2016 (PMID 27110344) showed that where temporal and genetic structure are confounded, over a third of replicates passed while giving a tMRCA of 51 years against a true 10,000. Their danger zone is "fewer than 7 substitutions per genome" across the sampling window; this collection computes to **7.1**, from metadata alone.

**So: any date reported must be labelled a conditional projection of an imported prior, not an estimate.** The prior must span the union of the two in-organism sources — roughly **1.3 × 10⁻⁷ to 2.3 × 10⁻⁶**, better than an order of magnitude — and the paper must show how far the answer moves across it (Menardo 2019's "broad (conservative) time estimate"). Reporting a tight HPD from one end of that range is the failure mode to avoid.

### 4.4 Two citation traps to avoid propagating

- **Do not cite a pooled Chewapreecha rate of 1.03 × 10⁻⁶.** It circulates second-hand and appears nowhere in the paper or its SI.
- **Do not cite Seng for the value 1.7 × 10⁻⁷.** Their reference [53] resolves to Spring-Pearson 2015, a pangenome paper with no clock analysis. Cite Pearson 2020 (PMID 32149236) for the number and Seng only for the practice of importing one.
- **Do not propagate Chewapreecha's ~772 kb divergence denominator.** It reconciles with nothing — 10.7% of K96243, implausibly small for a core genome, and the alternative decimal reading exceeds the reference. The core-alignment length is a definitive non-report.

---

## 5. Work plan, ordered

Ordered by a mix of expected value and dependency. Items 1–6 are days each and several are hours; they are grouped first because **each one can invalidate work downstream of it**, and because between them they convert most of the review's remaining hand-waves into numbers.

### Phase 0 — diagnostics that gate everything else (do these first, in this order)

**1. The backbone fallback check.** ⏱ *hours*
`build_backbone_tree/main.nf` has paths that `cp` raw concatenated representatives into `backbone_alignment.fa`. **If a fallback fired, FastTree received unaligned sequence — which alone would explain the 25× branch inflation, with no recombination involved.** Verify equal record lengths before attributing anything to recombination; `pipeline_checks_bp.py`'s `load_alignment()` exits with exactly this diagnosis on failure. **Publish the file** — it currently exists only in `work/`.
*Why first:* it is the cheapest item on the list and it can retire the entire premise that motivated the branch-length investigation.

**2. Read the Mash sketch size off the existing run.** ⏱ *minutes*
At the default s = 1,000 the distance error at within-species range is ~14% relative. **If the 61–76 clusters were produced at default sketch size, that partition is partly noise, and no downstream validation repairs it.** This is a one-line check that determines whether the clustering needs redoing before anything else runs.

**3. Cluster size distribution.** ⏱ *minutes*
`python3 cluster_diagnostics_bp.py --clusters your_clusters.csv --cluster-col cluster`, with one row per genome. Gini near 0 and max/min near 1 means the partition was **imposed**; a skewed distribution with a long tail means it was **found**. Reference points: Chewapreecha Gini 0.456, max/min 34.2; Wu's imposed ten-way cut Gini 0.095, max/min 2.0. This is more diagnostic than comparing your cluster count against 19 or 10, and it is also STROME-ID item 13.2.

**4. Maximum within-cluster Mash distance.** ⏱ *free, from the matrix you already have*
Below 0.005 puts you inside SKA2's ~90%-recall strain regime; above 0.01 means the clusters are too coarse for SKA regardless of anything else.

### Phase 1 — the measurements that become results

**5. Measure the BioProject intra-cluster correlation.** ⏱ *an afternoon* — **highest value on the list**
Compute the fraction of core-SNP variance falling between rather than within BioProjects. **`GAP4 §4.2` shows the effective sample size falls from 5,515 to somewhere between 1,416 and 75 depending on this one unmeasured number** (at ICC 0.05 with PRJEB3409 as the dominant cluster it is 256, or 4.6% of nominal). This converts the review's largest hand-wave into a number, and it is Tier-1 novelty (§3, item 2) because nobody in bacterial genomics has done it.

**6. The reference-sensitivity experiment.** ⏱ *days* — **highest-value single run**
One mid-sized cluster (100–300 genomes, mixed Thai and non-Thai), three callers (existing pipeline, `ska map`, `ska lo`), two references (within-cluster representative, then K96243), Gubbins on each; compare post-Gubbins SNP counts, shared positions, tree distance, root-to-tip R². Add **Verticall distance as a fourth arm**. Optionally add 1026b as a third reference. Full design in §2.4. **Either outcome is informative**, which is what makes it worth running.

**7. Settle whether PopPIPE's Gubbins reaches `graft_tree`.** ⏱ *one run, or one careful read of the Snakefile DAG*
This decides whether PopPIPE is a precedent for your whole architecture or only its clustering half — which directly sizes the novelty claim in §3 item 4.

**8. Concatenated versus per-replicon, on one cluster.** ⏱ *low, given the split is required anyway*
Quantify topological distance, count Gubbins recombination calls in the junction window (`pipeline_checks_bp.py junction`), and report per-replicon clock rates. **Nobody has published this comparison for any organism.**

**9. Per-replicon callable fraction.** ⏱ *free with item 8* — `pipeline_checks_bp.py split` computes it. "X% of chromosome I versus Y% of chromosome II is callable across N genomes" is a number nobody has published for this organism.

**10. Cost measurement: `raxml-ng --parse` on one real masked cluster.** ⏱ *minutes*
Reports the distinct-pattern count, which settles the full-length-versus-SNP-alignment question. No benchmark exists at ~500 taxa × 3.8 Mb.

### Phase 2 — rebuild

**11. Refit clustering** with PopPUNK (Seng's parameters) → fastbaps phylogeny-conditioned, with the ~1,000 mean-pairwise-SNP cap (§2.1–2.3).
**12. Run the validation stack**: PopPUNK network score against the ≥0.8 bar; directional adjusted Wallace against the Lichtenegger cgMLST scheme with confidence intervals; treespace/Kendall–Colijn at λ=0 with within-scheme bootstrap dispersion as the null; core-versus-accessory refit congruence; per-cluster bootstrap Jaccard against Hennig's thresholds (≥0.75 valid, <0.60 not trusted).
**13. Balanced-subsample re-clustering with ARI**, balanced on country and separately on BioProject, reported as a distribution (§3, item 5).
**14. Rebuild the per-cluster pipeline** with the pinned Gubbins, the replicon split, `-fconst` with the closure assertion, and IQ-TREE per cluster (§2.5–2.10).
**15. Rebuild the backbone** with IQ-TREE 3 rather than parsnp/FastTree.

### Phase 3 — inference

**16. The dateability screen across every cluster** (§2.12 steps 0–2), then **BETS on survivors plus negative controls**. The pass/fail table is a primary result.
**17. Stochastic character mapping with the tip-state-swap permutation null**, on country labels and then on BioProject labels (§2.13). ⏱ *cheap; needs no new software.*
**18. SAASI as the sampling-aware comparator.**

### Phase 4 — the methods paper **[B]**

**19. SimBac benchmarking** at *B. pseudomallei*-like parameters (r/m = 7.2, median tract ~5 kb, two-replicon 7.2 Mbp genome). Nobody has done this, which is why every tool recommendation in the gap documents carries a caveat. **Design it to answer two questions at once**: whether the merge recovers the true topology, and whether PopPUNK/fastbaps clusters track clonal descent at this r/m (§3, item 7).
**20. GTM against representative-grafting**, scored on the SimBac ground truth.

### Deliberately not scheduled

Pangenome graphs (§2.6). Structured coalescent (§4.1). ARG methods (§3, Tier 3). A single global dated tree (§4.1). Treemmer for the phylogeographic subsample (§4.2 contraindication). Developing a phylogenetic effective sample size for discrete traits — name it as future work and label the Kish calculation what it is.

### Retrievals still outstanding

Four items the gap documents could not reach, none blocking: the *J Clin Microbiol* 2015 MLST-homoplasy paper; the beast.community BETS tutorial (GSS path-step counts and XML settings for §2.12 step 3); Roberts 2025's full *V. cholerae* results, to convert a claimed absence into a checked one; and Wilson 2008's full text. Also verify Croucher 2011, Harris 2010 and Young 2012 before citing — they were assembled at one remove.

---

## 6. Reporting checklist

What must appear in methods and results for this to survive review. Items marked **[STROME-ID]** are formal requirements from Field 2014 (PMID 24631223); compliance across 114 TB genomic-epidemiology papers averaged 50% and did not improve after publication (Cheng 2021, PMID 33842904), so reporting them explicitly puts the paper in a small minority.

### 6.1 Sampling frame — the section that must come first

- [ ] **[STROME-ID 6.1]** Source of participants and specimens; sampling frame and strategy stated explicitly. For a public-data reanalysis this means: the collection is an assembly of deposited studies, not a sample of a population.
- [ ] **[STROME-ID 9.1]** Efforts made to address discovery or ascertainment bias. Name PRJEB3409 as a **case-control** design (1,506 assemblies, 26.3% of the collection, 56.9% environmental, 93.6% undated).
- [ ] **[STROME-ID 12.1]** How the study took account of **non-independence** of sample data. This is the BioProject ICC (work-plan item 5) plus the Kish design-effect table.
- [ ] **[STROME-ID 12.2]** How missing data were handled — 38.2% undated, 3.7% no country. State that BactDating infers missing dates natively rather than dropping tips (Didelot & Parkhill 2022).
- [ ] **[STROME-ID 13.2]** **Sampling fraction and the cluster-size distribution.** This is the item that bites hardest for a 61–101-cluster design, and `cluster_diagnostics_bp.py` already computes the distribution.
- [ ] Burden-versus-sampling table at region **and** country level, with the 29 zero-genome countries and their 33% of global burden named.
- [ ] Effective sampling frame: Hill numbers on country (*q*=1 and *q*=2) and on year, alongside the nominal counts. Label the Kish calculation an ad hoc descriptive statistic — no phylogenetic effective sample size for a discrete trait exists (`GAP4 §4.2b`).
- [ ] Explicit statement that the comparison is clinical-plus-environmental, not clinical.

### 6.2 Clustering

- [ ] Cluster count, **size distribution**, and max/min ratio, against the two published comparators: Chewapreecha's 19 hierBAPS groups (4–137 isolates, median 17, ratio 34.2×, plus a 7.2% unassigned bin) and Wu's ten clusters (ratio 2.0×, imposed by `fcluster(t=10)` — state that they were imposed, not inferred).
- [ ] The stopping rule actually used, with its numeric criterion, and the note that Chewapreecha's rule as published cannot be implemented because Gubbins has never published a divergence ceiling.
- [ ] Cluster validation statistics with their thresholds and citations (see §2).
- [ ] **Balanced-subsample re-clustering**: ARI between the full-data partition and *B* balanced-subsample partitions (balanced on country, and separately on BioProject), reported as a distribution. State that no bacterial precedent exists for this check.
- [ ] Number of non-monophyletic clusters, if any — Chewapreecha had two.

### 6.3 Alignment and recombination

- [ ] Reference genome(s), and **concordance across at least two references**. Distance-to-reference predicts recall at ρ = −0.94 across 209 pipelines (Bush 2020, PMID 32025702), *B. pseudomallei* spans 0.73–5.61% from K96243, and recombination inference is itself reference-dependent (PMID 33503026).
- [ ] Callable/core fraction per replicon, reported per cluster. Do not reuse the "86% of K96243" figure — it is a 2008 microarray number; sequencing-era equivalents are ~76% and erode with sample size.
- [ ] Gubbins version **pinned ≥3.4.3** with `--invariant-site-correction` passed explicitly, and the reason (v3.4.2 made the correction optional and defaulted it off).
- [ ] Replicon split stated, with the reason: Gubbins cannot handle multi-contig references, `snp-sites` hardcodes `CHROM` to `"1"`, and Gubbins' 0.1–10 kb sliding window would scan across a concatenation junction.
- [ ] Masking policy, and what was **not** masked. Mask what you cannot call, not what you can call but expect to be recombinant — Hedge & Wilson show masking *worsens* branch-length distortion, and `--filter-percentage` (default 25) silently drops taxa for gappiness.
- [ ] r/m = 7.2 cited to Nandi 2015 as a genome-wide figure, kept distinct from Pearson 2009's seven-locus MLST ratio.

### 6.4 Trees and the merge

- [ ] Ascertainment-bias handling: `-fconst` with true constant-site counts, or constant sites retained. State which, and note that both routes have an in-organism precedent doing opposite things (Wu retained constant sites; Seng used `+ASC`).
- [ ] The grafted tree, if shown, labelled **topology-only** with branch lengths explicitly not interpretable, and the PopPIPE precedent cited including its authors' own caveat that it "will not maximize the phylogenetic likelihood."
- [ ] Branch-length rescaling procedure, if applied, stated in full.

### 6.5 Dating

- [ ] Per cluster, per replicon: *n* tips, *n* dated tips, sampling window, tree length in substitutions, and **Mantel r/p** between cophenetic genetic distance and temporal distance (Murray's confounding diagnostic).
- [ ] Root-to-tip regression reported as a **figure with a slope**, never as a test. Do not report R² as a test statistic.
- [ ] **BETS log Bayes factors** as the primary temporal-signal test, with Tay 2024's diligence attached: prior predictive simulation on root height and rate, prior sensitivity across Gamma/log-normal/exponential, relaxed rather than strict clocks, and hard biological bounds on root height.
- [ ] Every cluster tested, and the **pass/fail table published as a primary result** (Menardo 2019 is the template — 31 datasets, 13 failed, table as headline).
- [ ] Clock model: `arc`/`carc` in BactDating, with the additivity justification (Didelot 2021, PMID 32722797 — non-additive clocks shift when genomes are added or removed, and cluster membership here is itself inferred).
- [ ] `useRec=T` stated explicitly — it is **not** the default, and without it the Gubbins per-branch information is discarded.
- [ ] Imported rate prior given as the **union range 1.3 × 10⁻⁷ – 2.3 × 10⁻⁶** with a prior-sensitivity analysis.
- [ ] Per-replicon estimates reported **separately with their disagreement visible** (Chewapreecha's American isolates: 1806 from chr I, 1759 from chr II).
- [ ] Post-hoc diagnostics on every dated tree reported (DiagnoDating).

### 6.6 Phylogeography

- [ ] Model choice among ER / SYM / ARD with ΔAIC and Akaike weights, **plus the parameter count against tip count**. For a six-state trait ARD is 30 free parameters; Chewapreecha estimated that from 90 tips and reported no rate matrix.
- [ ] **The full transition rate matrix with its uncertainty across resamples.** Chewapreecha reports none — this is a strict improvement at no methodological risk.
- [ ] `pi` reported explicitly. Use `pi="equal"` and say so, or report both flat and sampling-corrected `pi = (n_i/s_i)/Σ(n_j/s_j)` and show the difference.
- [ ] `Q="mcmc"` rather than the `"empirical"` default, so rate-matrix uncertainty propagates.
- [ ] **Tip-state-swap permutation null** results: observed transition counts and root-state frequencies against the permutation distribution, for country labels **and separately for BioProject labels**.
- [ ] Subsampling design and its cost: countries kept, genomes used, countries discarded by name.
- [ ] Per-node estimate certainty, since certainty — not model fit — is what tracks accuracy.
- [ ] Explicit statement that pooling across resampled trees yields a distribution over replicates, not a posterior, and is restricted to transition counts and root state.

### 6.7 Software and reproducibility

- [ ] Versions pinned for every tool, with Gubbins, phytools and BactDating called out specifically (all three have version-dependent behaviour that changes results).
- [ ] phytools version stated — 2.5-2 current against Chewapreecha's 0.5-10, and the documented root-node `pi` sampling bug in "1.0-1 and probably prior recent versions."
- [ ] `backbone_alignment.fa` and the per-cluster alignments published, not left in `work/`.
- [ ] **Gubbins version cited from the release tag, not `--version` output.** The `VERSION` file reads `3.4.2` on both `master` and tag `v3.4.3`, so `run_gubbins.py --version` may report the wrong release on a correct install.
- [ ] One residual Gubbins inconsistency worth flagging in print: in v3.4.3, `select_best_models` builds its IQ-TREE object without passing the correction flag, so in a default run **the model is selected under a constant-site-corrected likelihood and the tree is then built without the correction.**

---

## Appendix A: measured findings from the 2,802-genome run (2026-08-09)

These are measurements on your own data and installation, not literature. Each
changes a specific recommendation above.

### A.1 The clusters are size-capped, not inferred

`conf/profiles/bp.config` sets `max_cluster_size = 50` with
`cluster_split_method = 'similarity'`. Measured on `cluster_membership.tsv`
(2,802 genomes, 153 clusters):

| Quantity | Value |
|---|---|
| Clusters at **exactly** 50 | **29** |
| Clusters within 3 of the cap | 41 |
| Genomes in those clusters | **2,028 (72.4%)** |
| Clusters **above** the cap | **0** |
| Singletons | 62 |
| Gini | 0.599 |

A hard wall at a round number with nothing above it is a cap, not biology.
**These clusters are fragments of larger connected components**, so "cluster"
cannot be read as "lineage" in any downstream claim — per-cluster r/m, dating,
or the graft.

**The cap is not computationally necessary.** Seng ran Gubbins successfully on
*B. pseudomallei* lineages of **312, 297 and 125** genomes at 351–549 mean
pairwise core SNPs. Cap on **diversity** (§2.3's ~1,000 mean pairwise core SNP
rule), not on count.

**A correction to §2.3's own diagnostic.** The Gini here is 0.599 — *higher*
than Chewapreecha's 0.456 — which the "skewed ⇒ inferred structure" heuristic
reads as a good sign. It is not: the Gini is inflated because the singleton
tail is uncapped while the top is truncated. **Check for a wall before reading
the Gini.** `cluster_metadata_join_bp.py` now does this automatically.

### A.2 Composition, measured against the curated metadata

2,800 of 2,802 genomes joined (2 unmatched: `IP-0009-1-R`, `IP-0194-1-R`).

| Quantity | Value |
|---|---|
| Thailand / China / Australia | 62.6% / 10.5% / 10.1% |
| Country labels → **effective** (Hill q=2) | 42 → **2.40** |
| BioProjects → **effective** (Hill q=2) | 296 → **8.86** |
| Dated | **86.8%**, 1960–2025 |
| Years → **effective** (Hill q=2) | 66 → **8.20** |
| Effective *n* at ICC 0.05 (Kish) | **167 of 2,800** |

Dating completeness is far better than the public audit implied (86.8% vs
61.8%), but the **effective** temporal span is 8.2 years, so §4.3's conclusion
is unchanged.

### A.3 Three defects found by running, not by reading

All three fail silently or waste a full run, and all three are worth checking
in the Nextflow pipeline itself.

1. **`set -u` aborts conda activation.** Conda's
   `activate.d/activate-gcc_linux-64.sh` dereferences an unbound `SYS_SYSROOT`.
   Any script using `set -euo pipefail` dies at its first `conda activate`.

2. **`generate_ska_alignment.py` defaults to `--k 17` and always runs
   `ska map --repeat-mask`.** Measured on cluster_0 chromosome 2:

   | k | Masked (N) |
   |---|---|
   | 17 (helper default) | **59.0%** |
   | 31 | **3.5%** |

   At k=17 Gubbins' `--filter-percentage 25` then drops nearly every taxon
   ("Not enough sequences are left after removing duplicates"). Snippy on the
   identical reference and genomes leaves only **2.6–4.3%** unaligned, which
   proves the loss is a k-mer artefact and **not divergence** — cluster_0 is
   not too diverse for SKA. `params.config` already sets `ska_kmer = 31`;
   confirm the pipeline passes it through rather than relying on the default.

3. **`snp-sites -C` on Gubbins' `filtered_polymorphic_sites.fasta` returns
   `0,0,0,0`** — that file is SNP-only by construction. IQ-TREE accepts
   `-fconst 0,0,0,0` silently and models nothing, so the correction *appears*
   applied while doing nothing. Counts must come from the **full** alignment.
   Measured: `467202,1026217,1020414,465056` (chr2) and
   `642961,1377452,1365540,650474` (chr1) — both **68.0–68.7% GC**, matching
   K96243's 68.06% and confirming §2.9's compositional argument for `-fconst`
   over `+ASC`.

   *Methods caveat:* these counts are over the alignment as it **entered**
   Gubbins, so constants inside masked recombinant tracts are included. Gubbins
   emits no masked full alignment by default. State this rather than leave it
   implicit.

### A.3b RESULT: reference bias measured in *B. pseudomallei* (cluster_0)

The §2.4 experiment, run on cluster_0 (50 genomes, 11 countries, 24
BioProjects, 42 dated over 28 years). Close reference = `GCF_003547015_1`
(strain R15, complete, within-cluster); distant = K96243.

**Complete: 12/12 arms, 3 callers × 2 references × 2 replicons, 0 failures.**

**Post-Gubbins SNP count, close → K96243:**

| Replicon | mapping caller (snippy) | `ska map` | `ska lo` |
|---|---|---|---|
| chr1 | **+27.8%** | −1.5% | −0.5% |
| chr2 | **+30.7%** | +1.8% | −1.2% |

**Caller concordance (Jaccard on polymorphic positions) — the decisive panel:**

| Pair | chr1 close | chr1 K96243 | chr2 close | chr2 K96243 |
|---|---|---|---|---|
| existing vs `ska map` | 0.931 | **0.718** | 0.903 | **0.703** |
| existing vs `ska lo` | 0.992 | **0.773** | 0.981 | **0.771** |
| **`ska map` vs `ska lo`** | 0.938 | **0.929** | 0.885 | **0.912** |

**Read the third row.** On the distant reference the two reference-free callers
still agree with *each other* at 0.929 / 0.912 — essentially unchanged from the
close reference — while both diverge from the mapping caller, dropping from
0.98–0.99 to 0.70–0.77. So the distant reference does not degrade everything
in common; **the mapping caller alone moves, and the two independent
reference-free callers jointly define the position set it departs from.** That
is a far stronger form of the result than the SNP count alone, because it
identifies *which* caller is wrong rather than merely showing disagreement.

**Three things follow, and the second is the mechanism.**

1. **The effect is caller-specific, not a general property of reference
   distance.** The reference-free caller is unmoved (−1.5%, +1.8%) while the
   mapping caller gains 28–31%. Replicated independently on both replicons.
   This is the PMEN2 pattern (Snippy +42% post-Gubbins SNPs on a 98.52%-ANI
   reference) reproduced in this organism.
2. **The spurious calls survive Gubbins and reach the tree.** Recombination bp
   barely moves (−0.8%, +1.6%) while SNP count rises ~30%, so the extra
   positions are not being absorbed as recombination. On K96243 the union grows
   to 20,704 (chr1) / 19,935 (chr2) positions, of which ~5,800–5,900 are called
   by the mapping caller alone.
3. **Apparent r/m is reference-dependent** in the predicted direction: chr1 r/m
   falls 2.25 → 1.31 on K96243 as the point-mutation denominator inflates.
   **Report r/m with the reference and caller attached**, never as a property
   of the cluster alone.

**What this does NOT show.** Root-to-tip R² is ~0.02 on *both* references, so
the temporal-signal arm of the test could not fire — the clock is **absent**,
not degraded, and no claim may be made that reference bias harms dating here.
Usefully, Mantel is non-significant (r ≈ 0.03–0.05, p ≈ 0.41–0.60), so temporal
and genetic structure are **not** confounded in Murray's sense: the absence of
clock signal is genuine rather than an artefact of confounded sampling.

**Scope.** One cluster. Repeat on a second cluster of different diversity
before generalising — `cluster_53` (49 genomes, 8 countries, 22 BioProjects,
41 dated over a **62-year** span) is the natural candidate, because its longer
temporal window tests the dating conclusion rather than re-testing the
reference conclusion.

**Interpretive caveat that cuts across all of it:** cluster_0 carries ~16,000
post-Gubbins SNPs, roughly an order of magnitude above the ~1,000 mean pairwise
core-SNP ceiling §2.3 derives and well above Seng's 351–549 lineages. Per A.1
these clusters are size-capped fragments, so this is reference bias measured on
a partition that is not a lineage. The effect is real; the unit it was measured
on should be fixed.

### A.3c RESULT: the effect is far worse in a TIGHT cluster (cluster_53)

Second cluster, chosen for a **62-year** sampling span (49 genomes, 8 countries,
22 BioProjects, 41 dated). Close reference = `GCF_003546995_3_Malaysia`
(strain H10, complete, within-cluster).

**Post-Gubbins SNP counts, chr1:**

| Arm | SNPs |
|---|---|
| `existing` vs close | 1,435 |
| **`ska map` vs K96243** | **1,151** |
| **`existing` vs K96243** | **10,480** |

**The control settles the interpretation.** A ~7–8× rise could mean either
mismapping or genuine divergence from K96243. The reference-free caller mapped
against K96243 recovers 1,151 SNPs — consistent with the close-reference truth
(1,435), not with 10,480. Had the divergence been real, `ska map` would have
found it. **≈87% of the calls the mapping caller makes against K96243 are
false.**

**Complete: 12/12 arms, 3 callers × 2 references × 2 replicons, 0 failures.**

| Replicon | `existing` | `ska map` | `ska lo` |
|---|---|---|---|
| chr1 | **+630.3%** | −12.9% | −7.8% |
| chr2 | **+715.4%** | −14.5% | −7.1% |

The control calls slightly *fewer* SNPs against the distant reference — the
mild recall loss expected of split k-mers — which is correct behaviour and
makes the contrast sharper.

**Caller concordance (Jaccard), and this is the definitive panel:**

| Pair | chr1 close | chr1 K96243 | chr2 close | chr2 K96243 |
|---|---|---|---|---|
| existing vs `ska map` | 0.921 | **0.110** | 0.882 | **0.092** |
| existing vs `ska lo` | 0.964 | **0.122** | 0.974 | **0.111** |
| **`ska map` vs `ska lo`** | 0.955 | **0.902** | 0.905 | **0.834** |

Agreement between the mapping caller and the reference-free callers collapses
from ~0.92 to ~0.10, while the two reference-free callers **still agree with
each other at 0.902**. The arithmetic is exact: `ska map` calls 1,151
positions, *all* inside the mapping caller's 10,480, union 10,480
(1,151/10,480 = 0.110). **The mapping caller's set is the reference-free set
plus ~9,300 positions no independent method sees.** That is pure addition, not
disagreement — which is what a false-positive process looks like.

**Effect size scales inversely with cluster diversity, and that inverts the
risk.** The absolute artefact is comparable in both clusters (~4,500 spurious
positions in cluster_0, ~9,000 in cluster_53); what differs is the true signal
it sits on.

| Cluster | true SNPs (close) | inflation on K96243 |
|---|---|---|
| cluster_0 (diffuse, 16k SNPs) | 16,197 | +28% |
| cluster_53 (tight, 1.4k SNPs) | 1,435 | **+630%** |

**So reference bias is worst exactly where the analysis is most likely to be
believed** — tight, low-diversity clusters are the ones anyone would date, call
transmission on, or read a small SNP distance from. Diffuse clusters, where one
is already cautious, look comparatively fine. Cluster_0 alone would have
understated this as "real but modest."

*Comparator:* Pightling 2014 (PMID 25144537) measured false positives rising
from 3.3–3.8 to 218.8–1,477.2 in *Listeria* off a 0.82%-divergent reference.
This is the same failure at a scale that would invalidate downstream analysis.

**Dating: the 62-year test.** Root-to-tip R² on the close reference is 0.033
(chr1) and 0.051 (chr2) — still flat across a 62-year window in a tight cluster
with 41 dated genomes. This was the specific test cluster_0 could not provide:
its 28-year window could be dismissed as too short (Duchêne 2016 calls <10
years "largely unreliable"). At 62 years there is still no usable temporal
signal, which moves the "no well-supported between-host clock" claim from a
single-cluster observation toward a property of this collection.

### A.3d How many clusters are actually low-diversity? 79% are not

`cluster_diversity_bp.py` reads within-cluster diversity straight off the
existing Mash matrix (GAP1 §11 "Step 0" — no new compute). Approximate pairwise
SNPs = Mash distance × 3,805,619 bp.

| Quantity | Value |
|---|---|
| Multi-genome clusters scored | 91 |
| **Above the derived ~1,000-SNP cap** | **72 (79.1%), holding 94.3% of genomes** |
| Above Seng's largest lineage (549) | 75 |
| Max Mash > 0.010 (too coarse for SKA) | **0** |
| Max Mash ≤ 0.005 (SKA strain regime) | 71 |

*Validation of the proxy:* cluster_0 estimates at ~12,800 approximate SNPs
against 16,197 measured post-Gubbins — right order, adequate for triage.
**⚠ This validation was wrong in both magnitude and sign. See A.5, which
supersedes it and requalifies every number in this subsection.**

**Three consequences.**

1. **The size cap does not produce low-diversity partitions.** Four-fifths of
   multi-genome clusters sit above the ceiling the Gubbins-contrast rule
   derives, so Gubbins is running outside its useful contrast envelope for
   94.3% of clustered genomes. This is A.1's argument, now quantified.
2. **But SKA is fine everywhere.** Not one cluster exceeds the 0.010 coarseness
   bound, and 71 sit inside the ≤0.005 strain regime. So `ska map` is viable at
   cluster level across the whole collection — the split-k-mer route is not the
   constraint; the recombination-correction contrast is.
3. **cluster_53 being tight was luck, and that matters for A.3c.** It is one of
   the ~19 clusters inside the cap. The 630% reference-bias result therefore
   applies to the *minority* of current clusters — but that minority is exactly
   the set anyone would date or call transmission on, and a diversity-based
   re-partition would turn most of the collection into clusters of that kind.
   **Re-partitioning would make the reference problem more widespread, not
   less.** Fix the reference first.

### A.3e The reference fix is 93% solvable today

`pick_cluster_references_bp.py`. Gubbins cannot use a multi-contig reference,
so a per-cluster reference must be complete (≤2 contigs).

| Route | Clusters | Genomes |
|---|---|---|
| Complete member **inside** the cluster | **57 (62.6%)** | 1,574 |
| No complete member, but one **borrowable** within Mash 0.005 | **28** | — |
| **Total solvable with no assembly work** | **85 / 91 (93.4%)** | — |
| Need an ABACAS pseudo-reference built | **6** | — |

Borrow distances are very small — 0.00026, 0.00029, 0.00125 for the closest
cases — i.e. orders of magnitude nearer than K96243, which is what produced the
+630% / 87%-false-call effect in A.3c.

**The conflation to fix in the pipeline.** The *backbone representative* and
the *mapping reference* are different objects with different requirements, and
treating them as one is what produced cluster_0's 135-contig "reference." A
representative only has to be typical; a reference must additionally be
complete. Select them separately: representative by centrality, reference by
`min(contigs)` then `max(N50)`, falling back to the nearest complete genome
elsewhere in the collection.

**How to choose the reference: constrained MEDOID, not centroid, not N50.**

- A *centroid* is the mean point in a vector space; it need not be a real data
  point, and in sequence space it is not constructible — you cannot map against
  an average genome.
- A *medoid* is the actual member minimising mean distance to all others. That
  is the right object, and here it is a **constrained medoid**: the most
  central genome *among those passing the completeness gate*.
- **N50 and total length are not ranking criteria** once the gate is passed, and
  "most core SNPs" is not a target — a reference does not carry SNPs, it
  determines where you can look. Extra unique content only adds positions other
  members cannot fill, raising missing data and `--filter-percentage` risk.
- Ranking by centrality rather than N50 **changed 27 of 57 picks (47%)**, so
  this is not a cosmetic distinction. Median medoid distance to members is
  Mash 0.00094 (max 0.00504) — all inside SKA's strain regime.
- A defensible alternative is the **1-center (minimax)**: minimise the *worst*
  member's distance rather than the mean, on the grounds that the worst-mapped
  member is what trips `--filter-percentage 25` and is silently dropped. Both
  columns are emitted in `cluster_references.tsv`.

**The fix is already validated, so it need not be re-run.** cluster_53's medoid
is `GCF_003546995_3_Malaysia`, which is exactly the reference its "close" arm
used. That arm gave 1,435 SNPs against K96243's 10,480 — so **+630% is the
measure of what applying per-cluster references buys**, already in hand.
(cluster_0's experiment used `GCF_003547015_1` rather than its medoid
`GCF_027856615_2_China_Hong_Kong`; both are complete in-cluster genomes, so the
+28% stands, but it was not the optimal choice.)

**Ordering consequence, which reverses the obvious plan.** Re-partitioning on
diversity turns most of the collection into tight, cluster_53-like groups —
precisely the regime where a distant reference makes ~87% of calls false
(A.3c/A.3d). **So fix the reference BEFORE re-clustering, not after**, or the
re-partition will amplify the reference artefact across the whole dataset
rather than confining it to the ~19 clusters that are currently tight.

### A.4 Practical constraints discovered

- **The pipeline's cluster representative can be unusable as a reference.**
  cluster_0's representative, `GCF_028621445_1_missing`, is a **135-contig
  draft**, and Gubbins cannot use a multi-contig reference at all. Four
  *complete* (2-contig) genomes exist inside cluster_0. **Representative
  selection should prefer least-fragmented genomes.**
- **Replicon IDs are per-reference.** K96243 uses `NC_006350.1/NC_006351.1`;
  R15 uses `CP025304.1_…/CP025305.1_…`. Any per-replicon workflow must map
  slots by position and verify by length (chr1 ≈ 4.07 Mb, chr2 ≈ 3.11–3.17 Mb).
- **The toolchain spans two conda envs** (`snp-phylogeny`: samtools, snippy,
  snp-sites; `bp-gubbins`: ska, Gubbins, IQ-TREE) and they cannot simply be
  merged — Gubbins caps Python at 3.10.
- Gubbins is **3.4.3** (confirmed from conda metadata, not the VERSION file,
  which reads 3.4.2 even on tag v3.4.3), ska **0.5.0**, snippy **4.6.0**,
  snp-sites **2.5.1**.

### A.5 The Mash→SNP proxy is biased upward, non-linearly, and A.3d's validation had the sign backwards (2026-08-10)

`calibrate_mash_snp_bp.py` (stdlib, 7 self-tests) computes the **actual mean
pairwise SNP distance** from the alignments the A.3b/A.3c runs already
produced, so the proxy can finally be checked against the quantity it claims
to estimate. Pairwise deletion; only columns where both taxa carry an
unambiguous base are counted, rescaled to full alignment length.

**A.3d compared two different statistics.** The proxy's `approx_mean_snps` is a
**mean pairwise distance**. The 16,197 it was checked against is a **count of
polymorphic sites**, on **chr1 only**. Those differ by roughly the Watterson
factor (≈4.5 at n=50) and by a factor of two for the missing replicon. Scored
like-for-like, whole genome:

| Cluster | mean Mash | proxy | **measured mean pairwise** (pre-Gubbins) | proxy bias | measured (post-Gubbins) |
|---|---|---|---|---|---|
| cluster_0 | 0.003368 | 12,818 | **9,433** | **1.36× high** | 7,588 |
| cluster_53 | 0.000595 | 2,263 | **535** | **4.23× high** | 238 |

So the proxy **overestimates**, where A.3d read it as a 21% underestimate, and
the bias is not a constant — it grows sharply as clusters get tighter. The
mechanism is straightforward: Mash distance responds to whole-genome k-mer
divergence including **accessory gene content**, while core-SNP distance does
not. In a tight cluster, accessory variation is most of what Mash is seeing,
so the proxy is measuring largely the wrong thing exactly where the cap
decision is made.

**Three things this breaks.**

1. **cluster_53 is not "over cap" — it is a textbook in-cap cluster.**
   `cluster_diversity.tsv` flags it `over_derived_cap = yes` at 2,263. Its
   measured mean pairwise distance is **535**, sitting inside Seng's 351–549
   band, the only empirical anchor that exists. A.3c's statement that cluster_53
   is "one of the ~19 clusters inside the cap" was right by luck and wrong by
   the table it cited.
2. **"79% over cap / 94.3% of genomes" is not a stable number.** Propagating the
   two measured bias factors against caps of 1,000 and 2,000:

   | Effective proxy threshold | Basis | Clusters in cap | Genomes in cap |
   |---|---|---|---|
   | 1,000 | as published | 19 (20.9%) | 156 (5.7%) |
   | 1,360 | cap 1,000 × cluster_0 bias | 22 (24.2%) | 248 (9.1%) |
   | 2,000 | cap 2,000, uncorrected | 25 (27.5%) | 313 (11.4%) |
   | 2,720 | cap 2,000 × cluster_0 bias | 30 (33.0%) | 471 (17.2%) |
   | 4,230 | cap 1,000 × cluster_53 bias | 42 (46.2%) | 972 (35.5%) |
   | 8,460 | cap 2,000 × cluster_53 bias | 65 (71.4%) | 1,844 (67.3%) |

   The two uncertainties — proxy bias and cap value — **compound in the same
   direction**, and between them the headline swings from 5.7% to 67.3% of
   genomes in cap. **Quote no "genomes in cap" figure without stating which row
   of this table it assumes.** That includes the fastbaps probe's 27.7%.
3. **The re-partition target may be much closer than it looks.** The probe's L3
   median sub-cluster diversity of 1,707 is a proxy figure. At the bias
   measured in that Mash range it corresponds to something in the high
   hundreds — i.e. plausibly already at Seng's band.

**What the cap evidence actually supports, and it is less than claimed.** The
useful diagnostic is not r/m but **clonal frame retained** — cumulative
recombination bases over genome length:

| Cluster | measured mean pairwise | median block bp | cumulative rec / genome | verdict |
|---|---|---|---|---|
| cluster_53 | 535 | 76 (q1 11, q3 3,278) | 0.20 | see A.6 |
| cluster_0 | 9,433 | 3,243 (q1 881, q3 6,875) | 2.70 | see A.6 |

**⚠ The "cumulative rec / genome" column above is the WRONG statistic and the
"saturated" reading drawn from it was wrong. A.6 supersedes this paragraph.**
It sums per-branch masked bases over ~97 branches, so it exceeds 1.0 whenever
branch count × per-branch masking does, which says nothing about saturation.
The correct statistic is the **union** of recombinant intervals across branches.

**The `r/m` column in `RESULTS.txt` is a per-branch median, and it inverts the
ordering.** cluster_53 shows 0.27 against cluster_0's 2.25 — but **43% of
cluster_53's branches have r/m exactly 0** (too few SNPs to assign any), which
drags the median to near zero. Pooled over branches the ordering reverses:
**2.09 (cluster_53) vs 1.63 (cluster_0)**. Report pooled r/m, or report the
median with the zero-branch fraction attached. Any argument built on the
per-branch median in a low-diversity cluster is an argument about the
statistic, not the biology.

### A.6 RESULT: two Gubbins failure modes, and evidence the derived ~1,000 cap is too tight (2026-08-10)

> **⚠ CONCLUSIONS REVISED BY A.9.** The measurements below stand. Two
> interpretations drawn from them do not: that cluster_16 marks a diversity
> *optimum* at ~3,600, and that low r/m constitutes a "contrast loss" failure.
> A fifth cluster (A.9) showed the r/m anchor was a category error and that
> recovery rests on cluster_16 alone. **Read A.9 before citing anything here.**

Third reference-sensitivity run, `cluster_16`, **12/12 arms, 0 failures**
(`make_refsens_cluster16.sh`, `refsens_cluster16/RESULTS.txt`). n = 48, 4
countries, 11 BioProjects, 30 dated over **60 years** (1965–2025); close
reference = `GCF_003547055_1_Malaysia` (strain PMC2000), the constrained medoid,
complete at 2 contigs. Scored by `cap_location_bp.py` (7 self-tests).

**Measured whole-genome mean pairwise: 3,639** (post-Gubbins 406 — Gubbins
removes **89%** of the diversity as recombinant, against the 88% that r/m 7.2
implies arithmetically).

| Cluster | proxy | measured | bias | union map/free | r/m map/free | tract map/free | verdict |
|---|---|---|---|---|---|---|---|
| cluster_53 | 2,263 | 535 | 4.23× | 19% / 18% | 2.2 / 1.2 | 118 / 4,604 | **under-detection** |
| **cluster_16** | 4,903 | **3,639** | **1.35×** | 77% / 75% | 9.8 / **7.5** | 4,820 / 5,906 | **RECOVERS published values** |
| cluster_0 | 12,818 | 9,433 | 1.36× | 90% / 86% | 1.6 / 1.0 | 3,095 / 4,909 | **contrast loss** |

`map` = mapping caller (snippy); `free` = `ska_map`, reference-free, **the
arbiter** — it has no mapping step so it cannot manufacture the false positives
A.3c exposed. Anchors: 78% of K96243 ever recombined; Nandi r/m 7.2 genome-wide;
median tract ~5 kb.

**cluster_16 reproduces all three published anchors simultaneously, on both
replicons independently, under two independent callers.** Reference-free r/m
6.25 (chr1) and 8.66 (chr2) against Nandi's 7.2; union 73.2% / 77.4% against
78%; median tract 5,587 / 6,225 bp against ~5 kb. Nothing was tuned toward these.

**There are two distinct failure modes, and the r/m column alone cannot tell
them apart.** This is why the earlier single-diagnostic framing failed:

- **Under-detection (cluster_53, 535 SNPs).** Union 18% against an expected 78%
  — four-fifths of the recombination is simply missed — and r/m 1.2 against 7.2.
  This is §2.3's own sensitivity floor biting: within-cluster donors are below
  the ~0.06% divergence at which `--min-snps 3` can see an import.
- **Contrast loss (cluster_0, 9,433 SNPs).** Union 86%, i.e. *at or above* the
  literature value — tracts are found — yet r/m still collapses to 1.0. Gubbins
  is flagging tracts and assigning almost no SNPs to them. This is the
  contrast-ratio failure §2.3 predicts, now measured rather than derived.

**Consequence for §2.3 — the part that survives A.9.** cluster_53, at 535 and
*inside Seng's 351–549 band*, flags only 17–19% of its genome as ever
recombined against a literature expectation near 78%. That is a genuine
**under-detection** failure, it rests on union coverage rather than on r/m, and
it is unaffected by A.9's corrections. So a cap at ~1,000 or at Seng's band
does push clusters into a regime where recombination is missed, and Seng's
lineages were called successful because Gubbins *ran*, not because recombination
was recovered correctly.

**What A.9 withdraws:** the claim that ~3,600 is a measured *optimum*. That
rested on cluster_16 being the interior point of an envelope, and with five
clusters cluster_16 is instead the sole outlier on r/m. Do not quote "3.6× the
derived cap" as a calibrated operating point.

**The limit of this claim.** Three clusters cannot separate "diversity detection
envelope" from "cluster_16 is a more recombinogenic lineage." What favours the
envelope is that r/m recovers to *the published genome-wide value specifically
at the intermediate point* — a merely more recombinogenic lineage had no reason
to land on 7.2 rather than overshoot. That is an argument, not proof. A fourth
point settles it: **`cluster_8`**, predicted ≈4,500, `status = ready`, 49-year
span, 11 BioProjects.

**Reference bias does NOT scale smoothly with diversity — the dose–response
premise of §3 Tier 2 item 9 is falsified.** Inflation on K96243:

| Cluster | measured | post-Gubbins SNPs (close, chr1) | spurious added | inflation chr1 / chr2 |
|---|---|---|---|---|
| cluster_53 | 535 | 1,435 | ~9,045 | +630% / +715% |
| cluster_16 | 3,639 | 1,576 | ~9,144 | **+580% / +637%** |
| cluster_0 | 9,433 | 16,197 | ~4,507 | +28% / +31% |

cluster_16 carries **7× cluster_53's diversity yet nearly the same inflation**.
The mechanism is the denominator: the spurious count is roughly constant at
~9,000 positions, so inflation tracks the **post-Gubbins** SNP count, not raw
cluster diversity. cluster_16 and cluster_53 have similar post-Gubbins counts
(1,576 vs 1,435) *because* Gubbins removes 89% of cluster_16's diversity.
**Report reference bias against post-recombination-filtering SNP count**, which
also means the tight-cluster warning in A.3d/A.3e applies to any cluster with a
small clonal frame, not merely to low-diversity ones.

Concordance replicates A.3c exactly. On K96243 the mapping caller agrees with
the reference-free callers at Jaccard **0.117–0.139** while the two
reference-free callers agree with each other at **0.910–0.945**; on the close
reference every pair sits at 0.903–0.995. Pure addition of ~9,100 positions no
independent method sees.

**Two corrections this run forced, beyond the union/sum error above.**

1. **Sub-100 bp "blocks" are a MAPPING-CALLER artefact, not a low-diversity
   scan-statistic artefact.** cluster_53's mapping caller gives a 76 bp median
   tract; the reference-free caller on the *same cluster and same reference*
   gives **4,604 bp**. Reference-free median tracts are 4,600–5,900 bp at every
   diversity level tested, so tract length is a property of the caller, not of
   diversity. The A.5 bullet asserting otherwise is withdrawn.
2. **The proxy bias is not monotone in diversity.** cluster_16 measures 1.35×
   against cluster_0's 1.36× — effectively identical — while cluster_53 sits at
   4.23×. So the bias is a stable ~1.35× above a few thousand measured SNPs and
   blows up only in the tight regime; cluster_53 is the outlier, not the trend.
   This partly rehabilitates `cluster_diversity.tsv` for the diffuse majority.
   It also means the two-point power law used to *target* cluster_16 has no
   support: it predicted ≈1,900 and the answer was 3,639, a 1.9× miss.

**Dating: the third independent negative.** Every close-reference arm has
root-to-tip R² < 0.10 (max 0.087) across a **60-year** window with n = 30, all
30 dated genomes joining the alignment cleanly. With cluster_0 (28 years) and
cluster_53 (62 years) this is the third cluster, third span, same answer. §4.3
stands and is now three-for-three.

### A.7 RESULT: cluster_8 — and the finding that high-diversity clusters yield nonsense substitution rates (2026-08-10)

> **⚠ PARTIALLY REFRAMED BY A.9.** The rate finding here survives and got
> *stronger*. The label "contrast loss" does not: judging within-cluster r/m
> against Nandi's **species-wide, genome-wide** 7.2 was a category error, since
> shallow clusters should show lower r/m regardless. Nine of ten measurements
> across five clusters sit at 0.94–1.49, so that is the norm, not a failure.

Fourth reference-sensitivity run, **12/12 arms, 0 failures**
(`make_refsens_cluster8.sh`, `refsens_cluster8/RESULTS.txt`). n = 50, 44 dated
over **49 years** (1976–2025); close reference = `GCF_000755945_1_Australia`
(MSHR5858), constrained medoid, complete at 2 contigs.

**Measured whole-genome mean pairwise: 9,252** — a near-replicate of cluster_0's
9,433, *not* the ≈4,500 intended. See the targeting failure below.

**Contrast loss replicates in an independent lineage.** Reference-free
(`ska_map`), close reference, chr1:

| Cluster | measured | union | r/m | tract | mode |
|---|---|---|---|---|---|
| cluster_53 | 535 | 17.3% | 1.12 | 4,678 | under-detection |
| **cluster_16** | 3,639 | 73.2% | **6.25** | 5,587 | **recovers** |
| cluster_8 | 9,252 | 76.5% | 1.10 | 4,758 | contrast loss |
| cluster_0 | 9,433 | 84.8% | 1.02 | 4,755 | contrast loss |

cluster_8 and cluster_0 are unrelated lineages at nearly identical diversity and
give **identical** r/m (1.10 vs 1.02) with union coverage at the literature
value.

**How A.9 changes the reading of this.** At the time this looked like replicated
failure, weakening the "cluster_16 is merely a recombinogenic lineage"
alternative. With cluster_48 added, r/m ≈ 1.0–1.5 turns out to be what **four of
five** clusters do across a 17-fold diversity range, so these two are the norm
rather than a replicated failure, and the alternative is **not** weakened. The
union coverage here (76–86%, against 78% expected) is normal, so nothing about
these clusters' recombination *detection* is anomalous.

**THE IMPORTANT FINDING (survives A.9, restated there with five clusters):
high-diversity clusters yield nonsense substitution rates, and R² does not warn
you.** Root-to-tip on the close-reference `existing` arm:

| Cluster | mode | slope (subs/site/yr) | R² | Mantel p |
|---|---|---|---|---|
| cluster_53 | under-detection | 2.8–4.3e-07 | 0.033–0.051 | 0.83, 0.98 |
| cluster_16 | **recovers** | 2.8–3.3e-07 | 0.032–0.033 | 0.22, 0.72 |
| cluster_8 | contrast loss | **1.1–1.9e-05** | 0.124–0.125 | 0.19, **0.070** |
| cluster_0 | contrast loss | **1.7–1.8e-05** | 0.017–0.020 | 0.41, 0.59 |

The two clusters where recombination removal works give ~3e-07, inside the
plausible bacterial range. The two contrast-loss clusters give 1.1–1.9e-05 —
**~50× faster and not biologically credible**. The mechanism is direct: r/m
collapses to ~1.0 against a true ~7, so unremoved recombination stays in the
alignment and inflates branch lengths, hence the rate.

**R² is not a usable flag for this.** cluster_0 pairs an inflated rate with
R² = 0.017 — it presents as the reassuring "no temporal signal" case while its
rate is wrong by nearly two orders of magnitude. cluster_8 pairs the inflated
rate with the *highest* R² of the four (0.124) and the only Mantel values
approaching significance (p = 0.070 on the close arm; 0.006–0.052 on several
distant-reference and `ska_lo` arms) — i.e. the one cluster that looks most
datable is the one Murray's diagnostic says you cannot apply an unclustered
date-randomisation test to.

**This inverts the order of operations in §2.12 and §6.5**, and A.9 sharpens the
screen. Standard practice screens temporal signal to decide whether to date.
Instead: **screen the cluster's measured diversity and the slope's sign and
magnitude first**, and refuse to date any cluster above ~4,000–5,000 measured
mean pairwise SNPs regardless of how its temporal diagnostics look. (A.9 shows
the discriminator is diversity, not r/m — cluster_53 has r/m 1.12 and a perfectly
plausible slope.) Report the rate with the diversity and recombination
diagnostics attached, never alone.

*Consistent with §4.3, not against it:* every plausible-rate cluster still has
R² ≤ 0.051, so the no-clock conclusion holds four-for-four. What A.7 adds is that
the two clusters which *appear* to have more signal are the two whose alignments
are known to be contaminated with residual recombination.

**The inflation mechanism from A.6 is confirmed at four points**, monotone in
post-Gubbins SNP count — not in raw diversity:

| post-Gubbins SNPs (close, chr1) | 1,435 | 1,576 | 9,106 | 16,197 |
|---|---|---|---|---|
| inflation on K96243 | +630% | +580% | **+52%** | +28% |

**THE MASH PROXY MUST BE RETIRED FOR TARGETING — it distorts spacing badly.**

| cluster | mean Mash | proxy | measured | bias |
|---|---|---|---|---|
| cluster_53 | 0.000595 | 2,263 | 535 | 4.23× |
| cluster_16 | 0.001288 | 4,903 | 3,639 | 1.35× |
| cluster_8 | 0.002147 | 8,172 | 9,252 | **0.88×** |
| cluster_0 | 0.003368 | 12,818 | 9,433 | 1.36× |

cluster_8 and cluster_0 differ **1.6-fold in Mash distance and have essentially
the same true diversity**, and the bias spans 0.88×–4.23× with no monotone
relationship to anything.

**Correction, 2026-08-10 (this section first overstated the fault).** The proxy
does **not** mis-*rank* these four — its rank order matches truth exactly
(`cluster_53 < cluster_16 < cluster_8 < cluster_0`). What it destroys is
**spacing**. On the pair that broke cluster selection it implies cluster_0 is
**57%** more diverse than cluster_8 when the true difference is **2%**. So
`cluster_diversity.tsv` remains usable for coarse ordering, and A.3d's ~79% is
weakened by the 0.88×–4.23× scale error rather than by rank failure. What the
proxy cannot do is **target a wanted diversity band**, which is exactly what
both cluster selections needed. Four points cannot establish that rank order
generally holds, so treat the ordering as indicative, not reliable.

**It also explains both cluster-selection failures.** cluster_16 was targeted at
≈1,900 and measured 3,639 (1.9× miss); cluster_8 was targeted at ≈4,500 and
measured 9,252 (2.1× miss). The second used the same two-point power law already
declared unsupported in A.5 — a process error, not bad luck. **Do not select a
cluster by Mash distance again.**

**The replacement, now CALIBRATED: `measure_diversity_bp.py`.** `ska build` +
`ska distance` gives pairwise SNP distances with no reference, no alignment and
no Gubbins — minutes per cluster against ~90 minutes for a 12-arm run, so all 91
multi-genome clusters are affordable. Calibration sweep against the four anchors:

| min-freq | c53 | c16 | c8 | c0 | worst deviation |
|---|---|---|---|---|---|
| **0.0** | 1.05 | 0.90 | 0.87 | 1.02 | **13%** |
| 0.5 | 1.05 | 0.90 | 0.86 | 1.01 | 14% |
| 0.9 | 1.02 | 0.88 | 0.82 | 0.95 | 18% |
| 0.95 | 0.99 | 0.87 | 0.78 | 0.91 | 22% |
| 1.0 | 0.86 | 0.79 | 0.72 | 0.73 | 28% |

**Adopt `--min-freq 0.0`:** every anchor within 13%, rank order correct, and the
residuals scatter (1.05, 0.90, 0.87, 1.02) rather than drifting monotonically
with cluster size — so there is no size-dependent bias, just residual noise.
Spacing is far better than Mash's: on the c8/c0 pair it implies a 20% gap
against Mash's 57%, where truth is 2%. Still imperfect, so **treat a ±15% band
as the resolution limit** and do not try to target a diversity window narrower
than that.

*A criterion error worth not repeating:* the sweep was first scored on **spread**
(max/min ratio), which chose min-freq 1.0 — the worst setting, uniformly
underestimating every anchor by 14–28% while scoring "tightest" because its bias
was consistent. Score on **worst deviation from 1.0**. A tight but off-centre
calibration is a bias, not a fit.

### A.8 RESULT: all 91 clusters measured — the proxy ranks well but scales terribly, and the corrected cap triples the usable collection (2026-08-10)

`measure_diversity_bp.py --all --min-freq 0.0` over every multi-genome cluster:
**91/91 succeeded**, ~30 s each, ~35 min total. Output
`cluster_diversity_measured.tsv`. This **supersedes `cluster_diversity.tsv` as
the triage table.** The four anchors reproduce the calibration exactly (1.05,
0.90, 0.87, 1.02), so the sweep is internally consistent with A.7.

**The proxy's fault is confirmed as scale, not rank — now on 91 points, not 4.**

| Statistic | Value |
|---|---|
| Spearman rank correlation, proxy vs measured | **0.978** |
| proxy/measured ratio: min / q1 / median / q3 / max | 0.90 / 1.10 / **1.36** / 2.28 / **91.0** |

So A.7's correction holds and generalises: Mash is a serviceable **ordinal**
statistic and a bad **cardinal** one. `cluster_diversity.tsv`'s ordering was
broadly right; its magnitudes were not, and the median 1.36× overestimate is
exactly the cluster_0/cluster_16 figure. **The worst failures are all tiny
clusters**, where sketch resolution dominates:

| Cluster | n | proxy | measured | ratio |
|---|---|---|---|---|
| cluster_74 | 2 | 91 | **1.0** | 91× |
| cluster_72 | 4 | 1,811 | 31.0 | 58× |
| cluster_56 | 10 | 2,443 | 87.2 | 28× |

Any per-cluster diversity claim about an n < 10 cluster taken from Mash is
worthless. This is a *new* limit: A.5–A.7 measured only n ≈ 48–50 clusters and
could not have seen it.

**The headline figures, finally in measured units.**

| Cap | Basis | Clusters in cap | Genomes in cap |
|---|---|---|---|
| 549 | Seng's largest lineage | 23 (25.3%) | 212 (7.7%) |
| 1,000 | derived cap — **wrong regime (A.6)** | 27 (29.7%) | 325 (11.9%) |
| **3,600** | **measured optimum (A.6/A.7)** | **45 (49.5%)** | **1,078 (39.4%)** |

Two things follow. A.3d's proxy-based "79.1% of clusters and 94.3% of genomes
over cap" was a **modest overestimate**: measured, it is 70.3% and 88.1% — the
direction and the argument stand, the magnitudes were inflated. And more
practically, **moving from the derived cap to the measured optimum takes the
usable fraction of the collection from 11.9% to 39.4% of genomes, a 3.3×
increase**, without any change to clustering. That is the concrete cost of
having calibrated on a derived number.

**Mean and median diverge sharply in some clusters, and the cap must not be
applied blindly to the mean.** cluster_38 has mean 4,112 against median **73**
(56× skew) — a tight core plus a few divergent members, not an
intermediate-diversity cluster. Capping on the mean would send it into the
Gubbins regime that suits neither part of it. **Report both, and treat
high-skew clusters as candidates for further subdivision rather than for
Gubbins as-is.**

**The fifth cluster is now a lookup, not a guess: `cluster_48`.** Measured mean
**4,562**, median 4,581 (skew 1.00, i.e. homogeneous), n = 50, `status = ready`
with a complete 2-contig internal reference, 3 countries, 10 BioProjects, 48
dated over 22 years. It sits between cluster_16 (3,639, recovers) and cluster_8
(9,252, contrast loss), which is precisely the unmeasured interval. Every other
candidate in the 4,000–6,000 measured band is `NO_COMPLETE_MEMBER` and would
need a borrowed or ABACAS reference first, so cluster_48 is uniquely suitable
and should be the next run.

---

### A.9 SYNTHESIS over five clusters: the dating threshold, and "mean pairwise diversity" is the wrong parameter (2026-08-10)

> **⚠ SUPERSEDED IN PART BY A.10.** Three changes: (1) the r/m "envelope" IS
> real — recovery reproduced in cluster_37 — but only once STRUCTURE is
> conditioned on; (2) slope **sign** is retracted as a diagnostic, magnitude
> stands; (3) the under-detection claim is **withdrawn** — cluster_53 is a
> mixture, so that bound is confounded. Read A.10.

Fifth reference-sensitivity run, `cluster_48`, **12/12 arms, 0 failures**
(`make_refsens_cluster48.sh`). Measured whole-genome mean pairwise **5,362** —
the first cluster selected from calibrated `ska distance` rather than Mash
(predicted 4,562, ratio 0.85, i.e. right at the ±15% limit A.8 set). **This
section is authoritative over A.6 and A.7 wherever they disagree.**

#### The five-cluster table (reference-free `ska_map`, close reference)

| Cluster | measured | union chr1/chr2 | r/m chr1/chr2 | slope chr1/chr2 | R² |
|---|---|---|---|---|---|
| cluster_53 | 535 | 17.3% / 18.7% | 1.12 / 1.38 | +2.8e-07 / +4.3e-07 | 0.033–0.051 |
| cluster_16 | 3,639 | 73.2% / 77.4% | **6.25 / 8.66** | +3.3e-07 / +2.8e-07 | 0.032–0.033 |
| cluster_48 | 5,362 | 73.3% / 72.8% | 1.49 / 0.94 | **−1.8e-05 / −4.5e-05** | 0.076–0.083 |
| cluster_8 | 9,252 | 76.5% / 80.3% | 1.10 / 0.94 | +1.1e-05 / +1.9e-05 | 0.124–0.125 |
| cluster_0 | 9,433 | 84.8% / 88.1% | 1.02 / 0.97 | +1.7e-05 / +1.8e-05 | 0.017–0.020 |

#### FINDING 1 (strong, 5/5): a dating threshold near 4,000–5,000, diagnosed by slope sign and magnitude

The two clusters below ~4,000 give small positive slopes (~3e-07 subs/site/yr),
inside the plausible bacterial range. The three above give magnitudes of
**1e-05 to 4.5e-05**, and **cluster_48's are NEGATIVE on both replicons** —
older isolates further from the root than newer ones, which is impossible for a
clock. A negative slope of −4.5e-05 cannot be described as an inflated rate; it
is a large-amplitude fit to noise, and it makes the pathology unambiguous in a
way cluster_8 and cluster_0 alone did not.

**This separates all five clusters cleanly, and on DIVERSITY — not on r/m.**
cluster_53 has r/m 1.12 (low) and a perfectly plausible slope, so the earlier
attempt to route this through r/m was wrong. **Refuse to date any cluster above
~4,000–5,000 measured mean pairwise SNPs.** *(A.10: still 6/6 with cluster_37
added, but diagnose on |slope| MAGNITUDE only — sign is noise.)*

**R² remains useless as the flag**, now three ways: cluster_48 pairs a nonsense
negative slope with R² = 0.08, cluster_0 pairs an inflated slope with R² = 0.02,
and cluster_8 — the worst-behaved on Mantel — has the *highest* R² at 0.124.
Screen on measured diversity and on the slope's sign and magnitude.

*Two mechanisms, probably.* Large magnitude tracks diversity (all three
high-diversity clusters). The **sign flip** is most likely mixture structure:
cluster_48 is the three-sub-lineage cluster (Finding 3), and a mixture's root
sits between sub-lineages, where tip dates carry no information about distance
from it.

#### FINDING 2 (weak, 1/5): the r/m "envelope" is unresolved, and the anchor was a category error

Nine of ten measurements across five clusters and a 17-fold diversity range sit
at **0.94–1.49**. cluster_16 alone gives 6.25 / 8.66.

**The anchor was wrong.** A.6/A.7 judged within-cluster r/m against Nandi's
**7.2**, which is a *species-wide, genome-wide* figure. Within a shallow cluster
r/m should be lower regardless — donors are closer and fewer imports have
accumulated. So r/m ≈ 1.0–1.5 is plausibly just what a normal *B. pseudomallei*
cluster looks like, and **cluster_16 is the anomaly requiring explanation, not
the target.** The label "contrast loss" should not be used for these clusters.

**Two hypotheses remain undistinguished:**

- **(a) a NARROW detection window**, upper bound between 3,639 and 5,362. This
  predicts exactly the observed pattern — one cluster inside, everything else
  outside — so the "flat baseline with one spike" shape is *not* evidence
  against it.
- **(b) cluster_16 is an atypical, more-recombinogenic lineage.**

Three candidate confounders were tested and **none explains cluster_16**:

| Hypothesis | Killed by |
|---|---|
| Sampling imbalance | cluster_0 is the best-sampled cluster (11 countries, 24 BioProjects, top BioProject 10%) and has the **lowest** r/m, 1.02 |
| Clonal-replicate content | cluster_16 has **more** near-identical pairs (11.8%) than cluster_53/8/0 (7.3–8.3%) |
| Bridged mixture | cluster_0 is as coherent as cluster_16 (gap/mean 0.045 vs 0.050, both 5/20 empty bins) yet gives 1.02 |

The only clean difference between cluster_16 and cluster_0 is diversity
(3,639 vs 9,433). **The decisive experiment is a cluster INSIDE the window**
(measured ~2,500–4,000), screened for modality first: `cluster_5` (3,623),
`cluster_37` (2,894), `cluster_34` (2,690), `cluster_27` (2,776) — all `ready`
with complete internal references. cluster_48 at 5,362 was the *wrong* test: it
sat outside the candidate window, so its failure was uninformative between (a)
and (b). **Do not rebuild the pipeline around a cap justified by r/m until this
is run.**

#### FINDING 3 (new): these clusters are multi-modal mixtures, so a cap on the MEAN is the wrong parameterisation

Prompted by the question of whether imbalanced sampling drives all of this. It
does not drive r/m (table above), but it exposed something more consequential.
Pairwise-distance distributions, chr1:

| Cluster | mean | gap/mean | empty bins | structure |
|---|---|---|---|---|
| cluster_16 | 3,639 | 0.050 | 5/20 | continuous |
| cluster_0 | 9,433 | 0.045 | 5/20 | continuous |
| cluster_8 | 9,252 | 0.173 | 10/20 | mixture |
| cluster_48 | 5,362 | 0.328 | 9/20 | **three sub-lineages** |
| cluster_53 | 535 | 1.853 | 15/20 | tight core + outliers |

`gap/mean` is the largest gap within the middle 90% of the distribution, over
the mean; `empty bins` counts 20-bin histogram bins holding <2% of pairs.

**cluster_48's pairs sit at ~300, ~2,700 and ~5,400 with near-empty gaps
between** (4 pairs in the 1,339–2,008 bin; largest gap 842 SNPs). **Its mean of
5,362 describes no actual pair in it.** cluster_53 is worse structurally
(gap/mean 1.853): a tight core plus outliers.

**This invalidates the selection criterion used to pick cluster_48.** It was
chosen because mean ≈ median (4,562 vs 4,581) read as "homogeneous" — but a
multi-modal mixture can have mean ≈ median and be nothing of the kind. A.8's
mean/median skew check is therefore **insufficient**; it catches cluster_38
(mean 4,112, median 73) and misses cluster_48 entirely.

**Consequences.**

1. **Screen candidate clusters on the full distance distribution** — `gap/mean`
   and empty-bin count — never on mean, median, or their ratio.
2. **A diversity cap on the mean is the wrong parameterisation.** The stopping
   rule should plausibly be a **modality condition** — subdivide until each
   cluster is unimodal — with the diversity threshold applied afterwards. This
   also connects directly to §3's documented failure: all five clustering
   methods failed through *recombinant bridging*, and bridging is exactly what
   produces these mixtures. The clusters are not lineages (A.1), and their
   distance distributions say so directly.
3. It follows that A.8's measured-unit "over cap" figures, while correct
   arithmetic on the mean, describe a statistic that is not meaningful for
   roughly half these clusters. Quote them with that caveat.

### A.10 SYNTHESIS over six clusters: recovery reproduces, and STRUCTURE is a confounder that must be conditioned on (2026-08-10)

Sixth run, `cluster_37`, **12/12 arms, 0 failures**. Measured whole-genome
**3,193** (ska-screen predicted 2,894, ratio 0.91 — second consecutive on-target
selection since Mash was abandoned). n = 49, **100% Thailand**, 8 BioProjects,
46 dated over 32 years. Continuous by modality screen (gap/mean 0.060).
**This section is authoritative over A.6, A.7 and A.9 wherever they conflict.**

#### FINDING 1: recovery REPRODUCES — A.9 Finding 2 resolves

Reference-free r/m **3.81 (chr1) / 4.75 (chr2)** against cluster_16's 6.25 /
8.66, with matching union coverage (76–77% vs 73–77%) and ~5 kb tracts. Every
other cluster measured sits at 0.94–1.49. Two unrelated clusters — one 100%
Thai, one Singapore-dominated — both elevated. **"cluster_16 is merely an
atypical lineage" is no longer tenable as the whole explanation.**

#### FINDING 2 (the key one): a two-factor model — STRUCTURE × DIVERSITY

| Cluster | measured | structure | r/m chr1 / chr2 |
|---|---|---|---|
| cluster_53 | 535 | mixture | 1.12 / 1.38 |
| cluster_37 | 3,193 | **continuous** | **3.81 / 4.75** |
| cluster_16 | 3,639 | **continuous** | **6.25 / 8.66** |
| cluster_48 | 5,362 | mixture | 1.49 / 0.94 |
| cluster_8 | 9,252 | mixture | 1.10 / 0.94 |
| cluster_0 | 9,433 | **continuous** | 1.02 / 0.97 |

- **All six mixture measurements fall in 0.94–1.49**, at 535, 5,362 and 9,252 —
  a 17-fold diversity range with no effect. **Bridging flattens r/m regardless
  of diversity.**
- **Continuous clusters track diversity**: elevated at 3,193 and 3,639,
  collapsed at 9,433.

Replicated on both replicons independently. This is why every single-factor
analysis in A.6–A.9 failed: structure was an unmeasured confounder.

#### FINDING 3: conditioning on structure leaves only THREE clean clusters, and two earlier "bounds" are confounded

This *weakens* the intervals A.6/A.7/A.9 quoted, and the weakening is the
honest result:

- **`cluster_48`'s negative slope and low r/m are confounded** — it is a
  mixture, so it cannot bound the window's upper edge. Flagged before that run
  and now confirmed.
- **`cluster_53`'s under-detection (union 17.3%) is ALSO confounded** — it is a
  mixture (gap/mean 1.549). Whether its 17% union reflects low diversity or
  tight-core-plus-outliers structure is **unresolved**. A.6 and A.9 called this
  finding "solid"; on one confounded cluster it is not. **Withdraw the claim
  that under-detection at low diversity is established.**
- Among continuous clusters the r/m collapse point is bracketed only to
  **(3,639, 9,433]** — a 2.6× range.
- **There is no continuous cluster below 3,193 in this partition at all**, so
  the under-detection threshold has zero clean data.

#### FINDING 4 (correction): slope SIGN is not a diagnostic; MAGNITUDE is

A.9 promoted "sign and magnitude." **Sign is retracted.** cluster_37 is negative
on both replicons (−3.1e-06, −5.0e-07) yet sits in the well-behaved group;
cluster_48 is negative and large. When there is no clock the sign is noise.

**Magnitude separates 6/6**, with a 6-fold empty gap:

| |slope| range | clusters | measured |
|---|---|---|---|
| 3.3e-07 – 3.1e-06 | c53, c16, c37 | 535 – 3,639 |
| 1.8e-05 – 4.5e-05 | c48, c8, c0 | 5,362 – 9,433 |

So the dating threshold near **4,000–5,000** survives, diagnosed on magnitude
alone. Dating is negative **six-for-six** (R² ≤ 0.125). cluster_37's chr1 Mantel
is 0.056 — borderline, worth reporting.

#### FINDING 5: the modality screen over 56 clusters — half are bridged, and the low band is empty

`measure_diversity_bp.py --screen-all`, all clusters with n ≥ 20:
**28 continuous, 28 mixture.** Continuous *and* reference-ready by band:

| band | continuous | also ref-ready |
|---|---|---|
| <800 | 3 | 1 |
| 800–1,500 | **0** | **0** |
| 1,500–2,500 | 1 | 0 |
| 2,500–3,600 | 5 | 4 |
| 3,600–5,400 | 5 | 2 |
| >5,400 | 14 | 7 |

**Every ref-ready cluster in 800–2,500 is a mixture** — cluster_20 (0.141),
cluster_49 (0.156), cluster_3 (0.699), cluster_4 (2.066), cluster_78 (5.238).
The mechanism: in this partition a cluster achieves a low *mean* by holding many
near-identical pairs plus a few divergent members, which is the
tight-core-plus-outliers shape the 50-genome size cap forces. **"Low mean
diversity" and "coherent tight population" are different things here**, which is
further evidence for the modality stopping rule (A.9 Finding 3) and for §3's
recombinant-bridging diagnosis.

**Consequence: the under-detection threshold cannot be measured on this
partition.** The fastbaps L3 sub-clusters are the natural source — 319 of them,
proxy median 1,707 (≈1,250 measured), i.e. exactly the empty band.
`_fastbaps.tsv` holds 1,590 samples. That requires re-running
`pick_cluster_references_bp.py` on the sub-cluster partition (a Tier-1 item
already), then modality-screening it.

#### BY-PRODUCT: the K96243 / 1026b bridge

cluster_37's constrained medoid **is 1026b** (`GCF_000260515.1`). The field is
split between K96243 (Chewapreecha, the Thai literature) and 1026b (the 2026
Vietnam study, 1,468 genomes) with **no published bridge** (§2.4). Because the
close arm is 1026b and the distant arm K96243, this run quantifies that
difference directly on 49 genomes, three callers, both replicons. Unplanned,
and publishable on its own per §2.4.

---

### A.11 FINAL SYNTHESIS: the stopping rule, measured on 17 clusters (2026-08-11)

**This section supersedes A.6, A.7, A.9 and A.10 wherever they conflict, and is
the section to read if you read only one.** It replaces §2.3's derived
~1,000-SNP cap with two measured conditions.

Evidence base: 6 full 12-arm runs + 11 reduced 4-arm runs
(`reduced_refsens_bp.py`, validated to reproduce the full protocol exactly),
all scored on the reference-free `ska_map` caller against each cluster's own
constrained-medoid reference. Diversity in **measured** mean pairwise core SNPs
from calibrated `ska distance` (`--min-freq 0.0`, ±13% on four
alignment-derived anchors — A.7/A.8), never from Mash.

#### The rule

> **1. Subdivide until each cluster is UNIMODAL** — largest within-distribution
> gap over the mean ≤ **0.09**, **and only judge this on clusters of n ≥ 30**
> (`measure_diversity_bp.py --screen-all`). The statistic is size-dependent:
> at n = 7–14 the median gap/mean is 0.64 and *nothing* passes, purely because
> ~21 pairwise distances leave large gaps by chance. Below n ≈ 30 the screen
> reports mixtures that are not there.
> **2. Then require measured mean pairwise core SNPs in ~1,300–4,700.**
> **3. Screen BOTH union coverage AND pooled r/m. Neither alone suffices.**

*Floor revised down from 2,700 on 2026-08-11* — see A.11b. It had rested on a
single cluster at 405 with a 6.6× unmeasured gap beneath it, and measuring into
that gap moved it by more than a factor of two.

#### The curve, continuous clusters only

All diversity values below are **ska-derived** (`cluster_diversity_measured.tsv`),
the units the rule is actually applied in. *An earlier draft of this table mixed
scales:* three full-run clusters were quoted from their alignments, which run
~10% above ska for the same cluster (cluster_37 3,193→2,894; cluster_16
3,639→3,291; cluster_8 9,252→8,172). The brackets are set by reduced-run
clusters, which were always ska, so **the brackets did not move** — but never
mix the two scales when applying the rule.

| measured (ska) | cluster | union | pooled r/m | tract | verdict |
|---|---|---|---|---|---|
| 405 | cluster_62 | **0.7%** | **0.07** | 1,002 | **under-detect** |
| 2,690 | cluster_34 | 88.4% | 12.12 | 7,118 | works |
| 2,776 | cluster_27 | 75.8% | 6.55 | 5,580 | works |
| 2,894 | cluster_37 | 76.4% | 4.28 | 5,478 | works |
| 3,291 | cluster_16 | 75.3% | 7.46 | 5,906 | works |
| 3,833 | cluster_26 | 77.0% | 7.41 | 6,104 | works |
| 4,671 | cluster_15 | 83.2% | 3.38 | 4,687 | works |
| 6,342 | cluster_10 | 83.5% | **1.73** | 4,943 | **r/m collapsed** |
| 8,872 | cluster_11 | 78.8% | **0.66** | 4,857 | **r/m collapsed** |
| 9,411 | cluster_51 | 84.9% | **0.57** | 4,280 | **r/m collapsed** |
| 9,617 | cluster_0 | 86.5% | **1.00** | 4,909 | **r/m collapsed** |
| 9,635 | cluster_31 | 86.7% | **0.67** | 5,541 | **r/m collapsed** |
| 10,018 | cluster_41 | 86.8% | **0.66** | 5,068 | **r/m collapsed** |
| 13,826 | cluster_2 | **69.0%** | **0.16** | 4,941 | **r/m collapsed** |

Full table in `threshold_curve.tsv`. **Six consecutive clusters from 2,690 to
4,671 work** — 12 replicon measurements, union 76–88% against the literature's
78% ever-recombined, r/m 3.4–12.1 bracketing Nandi's 7.2, tracts 4.7–7.1 kb
against ~5 kb. **Seven consecutive clusters from 6,342 to 13,826 collapse**, r/m
0.16–1.73, every one on both replicons.

- **Floor bracketed to (405, 2,690].**
- **Ceiling bracketed to (4,671, 6,342]** — a 1.36× interval.

**One trend worth noting at the extreme.** Union coverage is flat at 79–87%
across 6,342–10,018 but drops to **69.0%** at 13,826, with r/m at its lowest
(0.16). So at very high diversity *both* statistics finally degrade — the
alignment itself starts to fail, not just the SNP assignment. One cluster only,
so treat it as a hint rather than a third regime.

#### A.11b The floor is ~1,270, not ~2,700 — and fastbaps L1 DOES supply a usable partition (2026-08-11)

The floor rested on one cluster (cluster_62, 405, union 0.7%) with the next
measured point at 2,690 — a 6.6× gap flagged as the most likely thing to be
wrong. Two fastbaps **L1 sub-clusters** were run into it with the reduced
protocol, using medoid references from the new `fastbaps_L1_references.tsv`:

| measured | unit | n | union c1/c2 | r/m c1/c2 | tract | verdict |
|---|---|---|---|---|---|---|
| 405 | cluster_62 | 40 | 0.8% / 0.5% | 0.09 / 0.05 | 1,002 | under-detect |
| **1,268** | **s1_L1_9** | 90 | **68.4% / 79.1%** | **3.91 / 4.65** | 5,689 | **works** |
| 1,698 | s1_L1_27 | 150 | 56.5% / 62.5% | 2.56 / 2.58 | 4,965 | works (marginal) |
| 2,690 | cluster_34 | 50 | 88.7% / 88.1% | 11.20 / 13.05 | 7,118 | works |

**Floor bracket: (405, 1,268]**, down from (405, 2,690].

**Consequence — the earlier "sub-clustering cannot supply the partition"
conclusion is WITHDRAWN.** At L1, restricted to n ≥ 30 and continuous:

| floor | usable sub-clusters | genomes | % of 1,590 |
|---|---|---|---|
| 2,690 (old) | 2 | 225 | 14.2% |
| **1,268 (measured)** | **6** | **595** | **37.4%** |

The usable L1 units: `s2_L1_6` (n=155, 3,050), `s1_L1_27` (150, 1,698),
`s1_L1_9` (90, 1,268), `s2_L1_2` (75, 2,460), `s2_L1_10` (70, 4,400),
`s1_L1_28` (55, 2,452). **Use L1, not L3** — L1→L2→L3 moves the usable fraction
14.2% → 11.5% → 11.5% at the old floor, and L3 shatters strains into pairs
(median sub-cluster size 2, 206 of 319 are singletons or pairs). **Raising
`fastbaps: levels` from 3 to 5 would make this strictly worse**, contradicting
the §2 recommendation.

**Two cautions.**

1. **`s1_L1_27` is the weakest working unit measured** — union 57–63%, r/m 2.57,
   and it sits alone in a sparse region of the union distribution. It **passes**
   the calibrated cutoff (A.11c) and stays in the usable partition, but it is the
   first thing to re-examine if anything downstream looks wrong.
2. **Do not re-lower the floor on one point.** 1,268 works, 405 does not, and
   405–1,268 is still unmeasured. The same one-point reasoning is what just cost
   a factor of two.

#### A.11c The union cutoff, CALIBRATED — and why there is no second union cutoff for dating (2026-08-11)

The detection cutoff had been set at 0.6 × 78% ≈ 47% with nothing behind it.
Calibrating it against all 19 measured units (reference-free, close reference):

```
0.7% ············· 18.0% ································· 59.5%  69.0 73.0 73.8 75.3 ... 88.4%
     gap 17.4 pts             gap 41.4 pts                        densely packed, gaps 0.1-9.5
```

**The cutoff is insensitive: nothing lies between 18.0% and 59.5%.** Any value in
**20–58%** classifies identically — 17 of 19 pass, excluding only `cluster_62`
(0.7%) and `cluster_53` (18.0%), the two genuine detection failures. **Keep
47%, but state it as "anywhere in 20–58%; no measured unit falls in that band",
not as a derived quantity.** Excluding `s1_L1_27` would require a cutoff in
60–68%, a 9.5-point gap containing one unit — a line drawn through sparse data to
remove a single observation.

**Independent corroboration from tract length.** Every unit above 18% union has a
median tract of 4.3–7.1 kb, matching Nandi's ~5 kb. Only `cluster_62` also has an
abnormal tract (1,002 bp), so it is the sole case where detection is *broken*
rather than merely sparse — `cluster_53` finds correctly-sized tracts, just far
too few of them.

**AND A HYPOTHESIS THAT PROVED FALSE — do not revive it.** The obvious next move
was a stricter union threshold for dating, reasoning that residual contamination
(78% − union) is what inflated slopes ~50×. **The data refutes it:**

| unit | measured | union | max abs slope | plausible? |
|---|---|---|---|---|
| cluster_53 | 535 | **18.0%** | 4.3e-07 | **yes** |
| cluster_37 | 2,894 | 76.4% | 3.1e-06 | yes |
| cluster_16 | 3,291 | 75.3% | 3.3e-07 | yes |
| cluster_48 | 4,902 | 73.0% | 4.5e-05 | no |
| cluster_8 | 8,172 | 78.4% | 1.9e-05 | no |
| cluster_0 | 9,617 | **86.5%** | 1.8e-05 | **no** |

The **highest** union in the set has an inflated slope; the **lowest** has a
sound one. **Union predicts whether recombination was found; DIVERSITY predicts
whether the cluster can be dated.** Use the ~4,700 ceiling for dating and impose
no union requirement on it. This is the same species of error as anchoring
within-cluster r/m to Nandi's species-wide 7.2: a mechanism that sounds right and
does not hold.

#### A.11d ~~TWO ceilings, not one — the dating ceiling is ~3,300 ska~~ — **WITHDRAWN, see A.11e** (2026-08-11)

> **⚠ THIS SECTION'S CONCLUSION IS WRONG.** The two ceilings COINCIDE at
> (4,671, 6,342], and `DATING_MAX` is 4,700, not 3,300. The reasoning below
> failed twice: it used a MIXTURE (cluster_48) to set a diversity threshold,
> and it read slopes off the MAPPING caller. A.11e supersedes it. The tables
> below are retained only as a record of the error.

Setting the calibrated constants exposed a conflation running through A.9–A.11.
**There are two different ceilings and they were sharing one number.**

| ceiling | what fails | bracket (ska units) | width |
|---|---|---|---|
| **r/m collapse** | Gubbins finds tracts but stops assigning SNPs to them | **(4,671, 6,342]** | 1.36× |
| **dating** | root-to-tip returns large-magnitude nonsense | **(3,291, 9,617]** | **2.9×** |

The error surfaced because `cluster_48` sits at **ska 4,562 — below the old
DATING_MAX of 4,700 — yet has a slope of −4.5e-05**, the worst in the set. The
dating evidence, re-expressed in ska units:

| unit | ska | structure | max abs slope | datable |
|---|---|---|---|---|
| cluster_53 | 562 | mixture | 4.3e-07 | yes |
| cluster_37 | 2,894 | continuous | 3.1e-06 | yes |
| cluster_16 | **3,291** | continuous | 3.3e-07 | **yes — highest confirmed** |
| cluster_48 | 4,562 | mixture | 4.5e-05 | no |
| cluster_8 | 8,012 | mixture | 1.9e-05 | no |
| cluster_0 | 9,617 | continuous | 1.8e-05 | no |

**`DATING_MAX` is now 3,300** — deliberately conservative, sitting just above the
highest cluster with a *confirmed* sound slope. It is NOT a measured boundary:
the bracket above it spans to 9,617 because `cluster_48` and `cluster_8`, the
only failures below 9,617, are **mixtures**, so their failures are confounded by
structure (A.10) and cannot tighten it. **Raising it requires a CONTINUOUS
cluster between 3,291 and 9,617 with a sound slope.** Dating wrongly is worse
than declining to date, so the constant errs low.

*Also fixed:* two scale defects in `cap_location_bp.py`. It compared `DATING_MAX`
(ska) against an alignment-derived diversity that runs ~10% higher, and it
silently dropped requested clusters whose run directory did not exist (reduced
runs live under `reduced_*`/`fbL1_*`, not `refsens_*`). It now judges on ska,
displays both scales side by side, and warns on missing directories. The
self-tests assert every one of the six verdicts above against its measured slope
— which is what caught a stale fixture still using alignment units.

#### A.11e The dating ceiling COINCIDES with the r/m ceiling at (4,671, 6,342] (2026-08-11)

A.11d claimed two separate ceilings. It was wrong, and no new compute was needed
to show it — the evidence was already in the reduced runs, on the caller that
matters. **Root-to-tip on the REFERENCE-FREE caller (`ska_map`, close ref),
CONTINUOUS clusters only:**

| ska | cluster | max abs slope | sound |
|---|---|---|---|
| 2,894 | cluster_37 | 3.88e-06 | yes |
| 3,291 | cluster_16 | 5.43e-07 | yes |
| 3,833 | cluster_26 | 1.52e-06 | yes |
| **4,671** | **cluster_15** | **3.30e-06** | **yes** |
| **6,342** | **cluster_10** | **5.02e-06** | **no** |
| 8,872 | cluster_11 | 3.09e-05 | no |
| 9,411 | cluster_51 | 9.48e-06 | no |
| 9,617 | cluster_0 | 3.73e-06 | **yes — ANOMALY** |
| 9,635 | cluster_31 | 1.41e-05 | no |
| 10,018 | cluster_41 | 1.99e-05 | no |
| 13,826 | cluster_2 | 4.82e-05 | no |

**Dating ceiling: (4,671, 6,342] — identical to the r/m collapse bracket.**
`DATING_MAX = 4700`. Ten of eleven continuous clusters follow the pattern.

**TWO ERRORS in A.11d, both recorded so they are not repeated.**

1. **A MIXTURE was used to set a diversity threshold.** `cluster_48` fails at ska
   4,562, which is what drove the ceiling down to 3,300 — but cluster_48 is a
   mixture, and A.10 had already established that mixtures cannot set diversity
   thresholds because their failures are confounded by structure. **Both**
   failures below 6,342 (cluster_48, cluster_8) are mixtures. Structure is
   screened upstream by modality; the diversity gate must not double-count it.
2. **Slopes were read off the MAPPING caller.** It inflates them through false
   positives — 1.82e-05 for cluster_0 where `ska_map` gives 3.73e-06. Union and
   r/m were already read from `ska_map`; slopes must be too. The two callers agree
   on 5 of 6 full runs and disagree precisely on the cluster that set the bound.

**The remaining anomaly.** `cluster_0` at ska 9,617 is continuous with a sound
reference-free slope (3.73e-06), the only one of seven above the ceiling to be so.
Unexplained. The gate still refuses it on diversity, which is the conservative
call, but it means the ceiling is a *tendency* with one counter-example, not a law.
Note also `cluster_10` at 5.02e-06 barely exceeds the 5e-06 soundness cutoff,
which is itself a chosen round number — the two clusters bracketing the ceiling
are the two closest to that cutoff.

#### A.11f The modality screen, CALIBRATED by subsampling — two statistics, n ≥ 25 (2026-08-11)

A.11b found gap/mean rejects everything below n≈30 and set the rule to "n ≥ 30,
gap ≤ 0.09". Both numbers were wrong. Calibrated by **subsampling clusters whose
structure is unambiguous at full size** down to smaller n — subsampling preserves
the ground-truth label, so any change is pure size effect.

**Panel: 7 continuous + 3 mixture, ALL inside the operating range**, 25 reps per
size. The range restriction is essential — see the failure below.

| n | gap/mean cont p95 / mix p5 | empty_bins cont p95 / mix p5 |
|---|---|---|
| 16 | 1.33 / 0.52 — overlap | 0.65 / 0.50 — overlap |
| 20 | 1.04 / 1.12 — **separable ~1.08** | 0.60 / 0.55 — overlap |
| 25 | 0.81 / 1.46 — separable ~1.13 | 0.60 / 0.70 — **separable ~0.65** |
| 30 | 0.56 / 1.31 — separable ~0.93 | 0.60 / 0.70 — separable ~0.65 |
| 40 | 0.41 / 1.69 — separable ~1.05 | 0.55 / 0.70 — separable ~0.62 |

**TWO statistics are required — the same pattern as union-vs-r/m.** They detect
different mixture shapes and neither alone suffices:

- **`gap/mean`** catches a **tight core plus outliers**: one large gap over a
  *small* mean. cluster_53 = 1.55, s1_L1_5 = 6.71.
- **`empty_bins`** catches **several clumps over a wide range**: each gap is
  small relative to a *large* mean, so gap/mean misses it entirely.
  **`cluster_48` is demonstrably 4-modal on its ska histogram** (clumps at
  ~7–584, ~1,737–2,314, ~4,044, ~8,658–9,811) **yet scores only gap/mean 0.128**,
  while empty_bins gives 0.60 and flags it.

A.11b dropped `empty_bins` as non-discriminating. **That was wrong**, and it was
wrong for the same reason as the first calibration attempt: an out-of-range panel.

**Measured operating points** (OR rule: flag if either fires):

| thresholds | n=20 | n=25 | n=30 | n=40 |
|---|---|---|---|---|
| gap>1.0 **or** empty>0.45 | 20% false / 99% caught | 21% / **100%** | **15% / 100%** | **15% / 100%** |
| gap>1.0 or empty>0.40 | 24% / 99% | 23% / 100% | 24% / 100% | 23% / 100% |
| gap>0.6 or empty>0.35 | 34% / 99% | 29% / 100% | 31% / 100% | 31% / 100% |

**Adopt: n ≥ 25, flag as mixture if `gap/mean > 1.0` OR `empty_bins > 0.45`.**
100% of mixtures caught from n=25 up, at a ~15–21% false-mixture rate.

**Why tolerate 15–21% false rejections?** The asymmetry runs the other way from
intuition. A mixture that slips through is **caught downstream by r/m** (bridged
clusters give 0.94–1.49 across six measurements). A continuous cluster wrongly
rejected is a **silent loss** with no second chance. Prefer the rule that catches
every mixture, and treat rejected-but-borderline clusters as re-examinable.

**THE ORDER OF THE TWO GATES IS THE REVERSE OF WHAT A.11 SAYS.** A.11's rule
reads "subdivide until unimodal, THEN require diversity in range". It must be
**diversity first, modality second**: `gap/mean` divides by the mean, so at
ska 62 a single divergent genome produces an enormous ratio. A first calibration
attempt including out-of-range clusters failed at every size, with continuous p95
*rising* from 0.43 (n=16) to 5.80 (n=30) — impossible for sampling noise, and the
signature of a mis-composed panel. **Only evaluate modality on clusters already
inside the diversity range.**

**The rule was then tested on the case most likely to expose it.** `s1_L1_27`
(n=150, ska 1,698) is rejected on `empty_bins` (12/20) despite gap/mean of 0.038
— the largest single unit at stake, and a plausible false positive. Inspecting its
histogram: **41% of its 11,175 pairs fall below 300 SNPs** (a large clonal
subgroup), with a thin scatter bridging to a diverse main body at 2,000–4,000.
It is genuinely bimodal. `gap/mean` misses it *because* that scatter prevents any
single large gap, while `empty_bins` fires because the bridging bins each hold
under 2% of pairs. The control `s2_L1_6` is textbook unimodal with its 6 empty
bins all in the upper tail. **A true positive — `empty_bins` earned its place.**

**A constructive consequence.** An in-range cluster flagged as bimodal should be
**SUBDIVIDED FURTHER**, not discarded. `s1_L1_27` is in the diversity range and
holds 150 genomes; splitting it (L2/L3 within that sub-cluster) should yield a
usable clonal unit plus a usable diverse one. Its clonal subgroup is also of
interest in itself — 41% of pairs under 300 SNPs looks like an outbreak or a
heavily-sampled sublineage.

**Coverage under the calibrated rule: 828 / 2,802 = 29.6%** (615 from sub-clusters
+ 213 from in-range strains), against 28.8% under the old n≥30/0.09 rule. The gain
is small because five small sub-clusters were added while `s1_L1_27` was correctly
removed. A further **25 sub-clusters / 360 genomes are now labelled UNDECIDABLE**
(n < 25) rather than rejected — no better for coverage, but an honest description.

**RESULT of acting on that: `s1_L1_27` subdivided (2026-08-11).** fastbaps had
already computed L2/L3 within strain 1, so no new inference was needed — only
measurement. Its L2 split:

| unit | n | ska mean | gap/mean | empty | verdict |
|---|---|---|---|---|---|
| `s1_L1_27_L2_66` | 95 | **140** | 0.007 | 10/20 | below floor — unusable |
| **`s1_L1_27_L2_69`** | **45** | **1,487** | 0.223 | 8/20 | **continuous, in range — USABLE** |
| `s1_L1_27_L2_67` | 8 | 76 | 0.079 | 5/20 | below floor |
| (fourth) | 2 | — | — | — | too small |

**The bimodality resolves exactly as the histogram predicted.** The 41% of
near-identical pairs are a **95-genome clonal expansion at mean 140 SNPs** —
deep in the under-detection zone, where Gubbins finds essentially nothing. The
other 45 genomes form a clean in-range unit.

**So subdividing recovers 45 of 150 genomes, not all of them.** Coverage
**828 → 873 / 2,802 = 31.2%**. L3 would not help: it splits the 95-genome clonal
group into 75+17+3, each tighter still.

*Worth recording independently of the pipeline:* a 95-genome clonal group at mean
140 core SNPs inside PopPUNK strain 1 is an outbreak or a heavily-sampled
sublineage. Useless for recombination inference, but exactly the kind of unit a
transmission or outbreak analysis would want — and it is invisible in any
summary that reports only the parent cluster's mean of 1,698.

**AND `s1_L1_32` subdivided — no recovery, which is the informative case.**
L2 peels off 4 singletons/pairs, leaving a 33-genome core at **mean 485** — below
the floor. The parent's apparent 2,378 was almost entirely manufactured by those
4 divergent genomes; removing them drops the mean **5-fold**. Neither part is
usable: the core is too tight, the outliers are singletons. Coverage unchanged.

**WHICH STATISTIC FIRES PREDICTS WHETHER SUBDIVISION WILL HELP.** Two cases, and
the mechanism is clear enough to state as a working rule:

| | gap/mean | empty_bins | structure | subdivision |
|---|---|---|---|---|
| `s1_L1_27` | **0.038** (low) | **12/20** (high) | two substantial modes (95 + 45) | **recovers 45 genomes** |
| `s1_L1_32` | **2.92** (high) | 15/20 | tight core + 4 outliers | **recovers nothing** |

- **`empty_bins` high with `gap/mean` LOW** → several substantial modes.
  Subdividing splits real groups and is worth doing.
- **`gap/mean` HIGH** → a tight core plus a few extreme outliers. Subdividing
  removes a handful of genomes and leaves a core that was always too tight.
  **Do not bother.**

So the two statistics do more than jointly detect mixtures: they *triage* them.
Only two cases, so treat this as a hypothesis — but it follows directly from what
each statistic measures, and it would save running the futile splits.

**Limits.** Three mixture clusters, all in-range; the panel cannot speak to
mixture shapes absent from it. Below n=25 the two classes overlap on both
statistics at every threshold tested — that is a real limit, not a tuning
problem. Tool: `validate_modality_bp.py` (3 self-tests, fixtures asserted on
cluster_48's real measured values).

**Method note — the modality statistic is size-dependent.** Median gap/mean by
size: n 7–14 → 0.641 (0/12 pass), n 15–29 → 0.261 (0/19 pass), n ≥ 30 → 0.045
(9/15 pass). The 0.09 threshold was calibrated on n ≈ 50 clusters with 1,000+
pairs and rejects everything smaller outright. **Restrict modality verdicts to
n ≥ 30**, or normalise the gap against its expectation at that pair count.
Verdicts already written for small clusters — including A.10's 800–2,500 band
claim — are unreliable and should be re-checked.

#### TWO failure modes, needing TWO different detectors

This is the most transferable result here, and it is why every single-statistic
attempt in A.6–A.10 failed:

| | union coverage | pooled r/m | what breaks |
|---|---|---|---|
| **below the floor** | **collapses to ~1%** | meaningless (0.07) | nothing detected, so nothing masked |
| **within range** | 72–89% | 3.2–13.1 | — |
| **above the ceiling** | **stays normal, 79–87%** | **falls to 0.66–1.74** | tracts found, but almost no SNPs assigned |

**The upper failure is the dangerous one**: every statistic except r/m looks
healthy. Union catches only the lower failure; r/m catches only the upper.
Report both, always.

#### STRUCTURE is a confounder and must be conditioned on first

All six mixture measurements — cluster_53 (535), cluster_48 (5,362), cluster_8
(9,252) — give r/m **0.94–1.49** across a 17-fold diversity range. **Bridging
flattens r/m at any diversity.** Two consequences:

1. **Screen modality BEFORE diversity.** A bridged cluster's Gubbins output
   reflects the bridging, not the diversity, so it cannot be judged against
   either threshold.
2. **Half this collection is bridged** — the 56-cluster screen split exactly
   28 continuous / 28 mixture, and **every ref-ready cluster in 800–2,500 is a
   mixture** (gap/mean 0.141–5.238). In this partition a low *mean* is achieved
   by many near-identical pairs plus a few divergent members — the shape the
   50-genome size cap forces. "Low mean diversity" ≠ "coherent tight
   population". This is §3's recombinant bridging, measured.

#### Consequences for §2.3, and they are large

- **The derived ~1,000 cap sits BELOW the measured floor**, inside the region
  where detection is essentially zero (cluster_62: 0.7% union at 405). It would
  have driven subdivision into a blind zone. **Seng's 351–549 band is further
  below still** — those lineages were called successful because Gubbins *ran*.
- **Every intermediate figure this session proposed was wrong**: ~3,600 as an
  "optimum" (A.6, one cluster in range), the r/m envelope framed against a
  species-wide anchor (A.7/A.9, a category error), and slope *sign* as a
  diagnostic (A.9, retracted in A.10 — magnitude only).
- **Dating**: refuse to date above ~4,700 measured. Root-to-tip |slope| runs
  3.3e-07–3.1e-06 below the ceiling and 1.8e-05–4.5e-05 above it, a 6-fold
  empty gap. **R² does not flag this** — 0.02 with an inflated slope (c0), 0.08
  with a negative one (c48), 0.124 on the worst-behaved (c8). Dating is negative
  **6/6** on the full runs.
- **Mash is retired for triage.** ρ = 0.978 for rank but the ratio spans
  0.88×–91×, worst in small clusters (cluster_74, n=2: proxy 91, measured 1.0).
  Use `cluster_diversity_measured.tsv`.

#### What is NOT settled

1. **The floor is bracketed only to (405, 2,690]** — 6.6×. No continuous cluster
   exists between them *in this partition*, so closing it requires the
   **fastbaps sub-clusters** (319 at L3, ≈1,250 measured median — exactly the
   empty band). Re-run `pick_cluster_references_bp.py` on `_fastbaps.tsv`,
   modality-screen, then sweep. **This is the blocking item.**
2. **Circularity.** These thresholds were measured on size-capped fragments, half
   of them bridged. Re-partitioning changes the cluster population, so the
   thresholds must be re-verified on the new partition — cheap now that the
   reduced runner exists.
3. **Whether a modality condition is achievable** at all by fastbaps
   sub-clustering is untested; the sub-clusters may themselves be bridged.
4. **The subtree merge under recombination**, and the **BioProject ICC**
   (effective *n* spans 672→35 on that one unmeasured number). Neither needs
   more clusters.

#### By-product worth banking

`cluster_37`'s medoid **is 1026b**, so that run quantifies the
**K96243-vs-1026b** difference directly on 49 genomes, three callers, both
replicons. The field is split between those two references with no published
bridge (§2.4), which makes this publishable on its own.

#### A.11g The BORROWED reference is validated — N1 passes (2026-08-11)

33 of the 45 analysable units have no internal complete medoid and run against a
**borrowed** reference from another unit (§0). That was the one untested part of
the configuration. `prod_s2_L1_2` (n=75, ska 2,460) is the first unit ever run
this way, borrowing `GCF_009741295_1_Viet_Nam` at Mash 0.00137.

**It behaves like a normal close reference.** Mean of the two `close__ska_map`
arms, the same convention every A.11 row uses:

| arm | union | pooled r/m | median tract |
|---|---|---|---|
| borrowed (close) chr1 | 83.9% | 7.43 | 5,750 |
| borrowed (close) chr2 | 87.8% | 7.03 | 6,107 |
| **borrowed, unit headline** | **85.8%** | **7.23** | **5,928** |
| K96243 chr1 (contrast) | 81.1% | 7.74 | 5,767 |
| K96243 chr2 (contrast) | 89.0% | 7.48 | 5,829 |

All three statistics land mid-range for a working unit: union 85.8% against the
76–88% of the six anchor clusters, r/m 7.23 essentially on Nandi's 7.2, tract
5.9 kb against ~5 kb. **The borrow does not degrade anything** — it tracks the
K96243 arm to within a few points on every statistic, and the borrowed-vs-K96243
difference is smaller than the chr1-vs-chr2 difference within either reference.
Since K96243 sits *further* from this unit (0.0073) than any borrow does (max
0.00479), that is the expected direction.

**One unit, so this licenses the other 32 borrows only by analogy** — but the
analogy is strong, because every borrow is closer than the K96243 contrast arm
that already works. Re-examine if a borrowed unit turns up RM-LOW in N3.

**Scoring reproducibility.** `triage_analysable_bp.py` (self-tested) recomputes
the published A.11 rows for `cluster_34`, `cluster_15` and `cluster_10` from the
on-disk runs to the last decimal, which is what establishes that the headline
convention is *the mean of the two close arms* rather than any other pooling.

#### A.11h Two operational defects in the §0 handoff, both corrected (2026-08-11)

Found while executing N1→N2. Neither changes a measurement; both would have cost
a session.

1. **The N2 command as written could not run.** `reduced_refsens_bp.py` requires
   `--clusters` or `--auto-select` (`if not clusters: ap.error("nothing to run")`).
   The handoff's N2 invocation passes neither and exits immediately. It must
   carry an explicit comma-separated unit list.
2. **`analysable_modality.tsv` is a STUB.** For all 45 units `gap`,
   `gap_over_mean` and `empty_bins` are `0` and `structure` is hardcoded
   `continuous`; only `mean_snps` is real. The runner's mixture gate therefore
   **cannot reject anything** in the production run. This is intentional — the
   real screening happened upstream when the analysable set was built — but it
   means the runner offers no second line of defence, and **N3 triage must read
   `screened` from `analysable_units.tsv`**, which is the only file that
   distinguishes the 11 screened units from the 25 unscreened ones.

#### A.11i Union does NOT scale with unit size — and the 78% anchor is the wrong comparator (2026-08-11)

`prod_s2_L1_6` (n=155, ska 3,050) returned **union 98.0%**, the highest ever
measured here — 10 points above the previous maximum (88.4%) and 20 above the
literature's 78%. It is also the largest unit yet run, so the obvious worry was
that union is size-dependent and the 47% cutoff is not comparable across units
spanning n = 7–155.

**Two hypotheses were tested and BOTH are refuted.** Recorded because the
outcome licenses applying one cutoff across a 20-fold size range, which the N3
triage depends on — 25 of the 45 units have n < 25.

| hypothesis | test | result |
|---|---|---|
| union rises with n | Pearson r(n, union), 22 units | **r = 0.142** — refuted |
| union saturates with branch count | r(log branches, union), 20 passing units | **r = −0.059**, slope −0.9 pts/doubling — refuted |

The two largest units bracket the entire observed range — `s1_L1_27` (299
branches) gives the **lowest** passing union at 59.5% and `s2_L1_6` (309
branches) the **highest** at 98.0% — which is what kills the size explanation.
Between-unit biology dominates; size contributes nothing detectable.

**Nor is it Gubbins over-calling.** Block sizes are indistinguishable from normal
units (median 6,017 bp, q1 2,626, q3 12,303, sub-100 bp 0.3%, against 5,750 /
2,473 / 11,832 / 0.3% for `s2_L1_2`). What is elevated is the per-branch burden:
`rec_over_genome` 5.40–6.22 against 2.03–2.73 elsewhere. High union, high r/m
(9.99, second only to cluster_34) and high per-branch burden all agree:
**`s2_L1_6` is genuinely recombination-rich.** Verdict OK.

**THE ANCHOR, NOT THE MEASUREMENT, IS WHAT NEEDS RESTATING.** 78% is "the
fraction of *K96243* ever recombined, species-wide". Union as measured here is
the fraction of a replicon recombinant on ≥1 branch **within a shallow unit**.
These are different quantities, and a within-unit value exceeding the species-wide
one is not a contradiction. **This is the same category error already recorded for
r/m** — anchoring a within-cluster statistic to Nandi's genome-wide 7.2 (A.9).

**Nothing downstream changes**, and the reason is worth stating: the 47% cutoff
does **not** rest on the 78% anchor. The original `0.6 × 78% ≈ 47%` derivation was
abandoned in A.11c and replaced by the 41-point empty band, which is internal to
the measured data. Had the cutoff still been pinned to the anchor, this
observation would have moved it. **Stop describing 78% as a target the data
should match; use it as loose context only.**

**One consequence to carry into N3.** At 98% union the statistic is near its
ceiling and has no dynamic range left, so it cannot discriminate for this unit —
r/m is doing all the work. Expect union to be uninformative at the top end.

#### A.11j `s1_L1_19` flags on r/m and is UNEXPLAINED — and r/m looks like a continuum, not two classes (2026-08-11)

**The first production flag is the kind that was not supposed to occur.**
`s1_L1_19` (n=34, ska 3,956, **screened** continuous) returned **pooled r/m
2.30**, below the working band, with **union 78.1% and tract 5,261 — both
entirely normal**. §0 predicted r/m failures would be the *unscreened* n < 25
units. This one passed the modality screen.

**Three explanations were tested against the units already completed. All three
are refuted.** Recorded in full because each is the obvious next guess.

| hypothesis | test | verdict |
|---|---|---|
| `empty_bins` just under the 0.45 cutoff (8/20 = 0.40) marks a missed mixture | `s1_L1_28` has the **same** 8/20 and r/m **9.88**, the second-highest measured | **refuted** |
| high within-unit spread (max/mean = 3.00) depresses r/m | r(max/mean, r/m) = **−0.193**; `s1_L1_28` and `s3_L1_5` sit at 3.01 with r/m 9.88 and 6.79; the highest spread (`s1_L1_9`, 5.42) gives a healthy 4.28 | **refuted** |
| elevated `gap/mean` (0.1312) marks residual structure | `s2_L1_5` has a **higher** gap/mean (0.1881) and r/m **7.71** | **refuted** |

Note the stale-label trap encountered on the way: `fastbaps_L1_measured.tsv`
records `structure = mixture` for `s1_L1_19`, but that column was written under
the **old** n≥30 / gap ≤ 0.09 rule, which its gap/mean of 0.1312 exceeds. Under
the calibrated A.11f rule it is continuous (gap 0.1312 < 1.0; empty 8/20 = 0.40
< 0.45), which is why it entered the analysable set as screened. **The
`structure` column in the `fastbaps_L1_*measured.tsv` files is stale — recompute
from `gap_over_mean` and `empty_bins`, never read the label.**

**No upstream statistic on file predicts this unit's r/m.** Treat it as
re-examinable, not as a failure, and do not subdivide on this evidence.

**THE LARGER POINT, and it weakens the r/m screen itself.** With the production
units included, in-range pooled r/m now reads:

```
2.30  2.57  3.38  4.28  4.28  4.44  6.55  6.79  7.23  7.41  7.46  7.71  9.88  9.99  12.12
```

**This is a continuum, not two classes.** The largest gap below 4 is 2.57→3.38
(0.81), which is where the 3.0 line sits — but there is nothing resembling
union's 41-point empty band, and the apparent separation in the calibration set
was a small-sample artefact. `s1_L1_19` at 2.30 is simply the low tail, adjacent
to the known-bridged `s1_L1_27` at 2.57 — **suggestive, not diagnostic.**

**Consequence: r/m cannot bear the weight §0 places on it.** It is the sole
safety net for the 360 unscreened genomes, and it does not cleanly separate
bridged from working units. Any write-up should say that the unscreened
compromise is backstopped by a **continuous, weakly-separating** statistic, not
by a categorical test.

#### A.11k THE UNION EMPTY BAND IS GONE — the cutoff is no longer insensitive (2026-08-11)

**A.11c's central claim is falsified by the production runs.** It held that
sorted union leaves a **41.4-point empty band between 18.0% and 59.5%**, so any
cutoff in 20–58% "classifies identically" and 47% is therefore insensitive. That
was true of the 19 calibration units. It is not true now.

**Three production units land inside the band:**

| unit | union | pooled r/m | verdict |
|---|---|---|---|
| `s3_L1_5` | **47.9%** | 6.79 | healthy r/m — **0.9 pts above the cutoff** |
| `s2_L1_5` | **53.8%** | 7.71 | healthy r/m |
| `s1_L1_13` | **54.5%** | 2.07 | low on **both** |

The band's largest remaining gap is 29.9 points (18.0 → 47.9), and the cutoff now
has a unit sitting **0.9 points above it**. Values in 20–58% no longer classify
identically: 47%, 48%, 55% and 58% give four different partitions of these three
units (108 genomes). **The insensitivity argument is dead — do not repeat it.**

**The cutoff itself should NOT move, but its justification must change.** Raising
it to 55% would reject `s3_L1_5` and `s2_L1_5`, whose r/m of 6.79 and 7.71 are
squarely mid-band healthy — i.e. the second detector says recombination is being
assigned normally in both. The defensible statement is now:

> 47% is retained because the units immediately above it have healthy pooled
> r/m, so the two detectors agree they are sound. It is **not** retained because
> the cutoff is insensitive; it no longer is.

Note this is exactly the cross-check the two-detector design was built for
(A.11), now doing real work rather than illustrating a principle. `s1_L1_13`,
low on both, is the only in-band unit either detector condemns.

**BOTH SCREENS WEAKENED ON THE SAME DAY.** r/m turned out to be a continuum
rather than two classes (A.11j), and union's empty band has been populated. The
triage rests on two soft cutoffs that agree with each other, not on two sharp
ones. Any write-up must say so.

#### A.11l r/m may decline BEFORE the ceiling — the in-range/above-range split is not clean

Both r/m flags are the two highest-diversity units below the ceiling, which
suggests the collapse is a **gradient, not a step**:

| ska band | n | mean pooled r/m | values |
|---|---|---|---|
| < 3,900 | 12 | **7.19** | — |
| ≥ 3,900 (still in range) | 4 | **3.05** | 2.07, 2.30, 3.38, 4.44 |

Overall r(ska, r/m) = −0.194 across 16 in-range units, i.e. weak and non-monotone
— `s2_L1_10` at 4,400 gives a healthy 4.44 — so this is **suggestive on 4 points,
not established**. But it has a direct consequence:

**`triage_analysable_bp.py`'s scoping note was wrong and has been corrected.** It
claimed that because every analysable unit is inside the diversity range, the
above-ceiling branch of the r/m failure mode is "excluded by construction", so a
low r/m must indicate bridging. If the decline begins below 4,671, then an
RM-LOW flag on a high-diversity in-range unit is **ambiguous between bridging and
ceiling onset**, and `s1_L1_19` and `s1_L1_13` (ska 3,956 and 4,088) are exactly
where that ambiguity bites. Neither should be called bridged on this evidence.

**Testable, cheaply:** if it is ceiling onset, subdividing them will not raise
r/m; if it is bridging, it will. *(A.11n ran this test on a different unit and
found subdivision DOES repair bridging-induced low r/m, so the test discriminates.)*

**UPDATE — it is a NARROW BAND, not a gradient, and it is unexplained.** A third
unit flagged, and the three cluster far too tightly for a monotone ceiling
effect:

| unit | ska | r/m | screened | reference |
|---|---|---|---|---|
| `s1_L1_19` | 3,956 | 2.30 | yes | borrowed, Mash 0.00346 |
| `s3_L1_10` | 4,011 | 2.03 | **no** (n=24) | borrowed, Mash 0.00195 |
| `s1_L1_13` | 4,088 | 2.07 | yes | borrowed, Mash 0.00355 |

**Every in-range unit in 3,956–4,088 is depressed to r/m 2.03–2.30, while both
neighbours ABOVE them are healthier** — `s2_L1_10` at 4,400 gives 4.44 and
`cluster_15` at 4,671 gives 3.38. A ceiling gradient cannot produce that shape.
**A.11l's gradient reading is therefore withdrawn**; what the data shows is a
localised dip.

**FOUR hypotheses now refuted for this dip**, each by a unit sharing the putative
predictor while returning healthy r/m: `empty_bins` near threshold, within-unit
spread, `gap/mean`, and — new — **reference divergence** (`s1_L1_28` borrows at
Mash 0.00354, indistinguishable from the two flagged borrows, and gives r/m
9.88; r = −0.278 across 7 borrowed units). Nor is it a strain effect:
`s1_L1_19`, `s1_L1_13`, `s1_L1_9` and `s1_L1_28` are all strain-1 sub-clusters
and split 2 low / 2 healthy.

**Note the mislabel this produces.** `triage_analysable_bp.py` calls
`s3_L1_10`'s flag "the expected catch" because it is unscreened — but it sits in
the middle of the dip with a near-identical r/m to two *screened* units, so the
unscreened attribution is probably wrong. **The r/m safety net cannot currently
distinguish "unscreened and bridged" from whatever this band is**, which further
undercuts §0's account of what that net is doing.

> **PRE-REGISTERED PREDICTION (2026-08-11, before the runs completed).** If the
> band is real, the three pending units inside or adjacent to it — **`s2_L1_9`
> (ska 3,909), `s1_L1_16` (4,129), `s1_L1_10` (4,185)** — should return
> **r/m ≈ 2.0–2.5**. If they come back in the healthy 4–10 range, the band is
> three-unit coincidence and should be dropped. Recorded in advance so the
> outcome cannot be rationalised either way.
>
> **CONFOUND, noted before the results arrive rather than after.** Two of the
> three test units are **not clean tests**: `s1_L1_16` (gap/mean 1.35, empty
> 14/20) and `s1_L1_10` (0.84, 13/20) both score as mixtures on the modality
> statistics, so a low r/m from either is attributable to bridging and cannot be
> credited to the band. `s2_L1_9` (0.55, 9/20) sits right at the empty_bins
> threshold and is only semi-clean. **The pre-registered test is therefore
> weaker than it looked when registered**, and a confirmatory result should be
> discounted accordingly. A clean test needs an in-band unit with low modality
> scores, and none is pending.
>
> **OUTCOME — THE PREDICTION FAILED. All three came in BELOW the predicted range.**
>
> | unit | ska | predicted r/m | measured r/m | verdict |
> |---|---|---|---|---|
> | `s2_L1_9` | 3,909 | 2.0–2.5 | **1.94** | marginally below |
> | `s1_L1_10` | 4,185 | 2.0–2.5 | **1.31** | clearly below |
> | `s1_L1_16` | 4,129 | 2.0–2.5 | **0.82** | far below |
>
> The registered falsification criterion ("healthy 4–10 range → coincidence, drop
> it") was **not** met either — they did not come back healthy, they came back
> *worse*. So the test discriminates neither way, exactly as the pre-flagged
> confound warned. All three are small (n = 10–21) and all three carry
> mixture-ish modality scores, so their low r/m has at least two other available
> causes.
>
> **BUT THE BAND IS NOT EXPLAINED AWAY, AND THE CONTRAST IS SHARPER THAN BEFORE.**
> The three original band units have **clean** modality and healthy union:
>
> | unit | ska | n | gap/mean | empty | union | r/m |
> |---|---|---|---|---|---|---|
> | `s1_L1_19` | 3,956 | 34 | 0.13 | 8/20 | 78.1% | 2.30 |
> | `s3_L1_10` | 4,011 | 24 | 0.28 | 6/20 | 62.8% | 2.03 |
> | `s1_L1_13` | 4,088 | 28 | 0.30 | 8/20 | 54.5% | 2.07 |
>
> None is a mixture, none is tiny, all have union well above the cutoff — yet all
> three sit at r/m ≈ 2.1. That is a different phenotype from the test units
> (dirty modality, tiny n, r/m 0.8–1.9) and from ordinary bridging. **The band
> remains a genuine unexplained anomaly after five refuted hypotheses**
> (`empty_bins`, spread, `gap/mean`, reference divergence, and now
> diversity-band-predicts-r/m). It needs a clean in-band unit with n ≥ 25 and low
> modality scores to test properly, and **no such unit exists in the analysable
> set** — so this cannot be resolved without new partitioning.

#### A.11p MODALITY STATISTICS RETAIN SIGNAL BELOW n=25 — the first unscreened failure says so (2026-08-11)

`s1_L1_31` (n=22, ska 3,745, **unscreened**) is the first production unit
condemned by **both** detectors: union **26.2%**, pooled r/m **0.79**, tract
**3,460** — short, the signature A.11c identifies as detection genuinely *broken*
rather than merely sparse. Both agree, so unlike A.11m's cases there is no
ambiguity.

**It was predictable, and the prediction was thrown away.** Its measured modality
statistics are **gap/mean 1.18 and empty_bins 13/20 (0.65)** — *both* above the
A.11f mixture thresholds, comfortably. It entered the analysable set only because
n = 22 < 25 put it in the "undecidable" bucket, where the statistics are
discarded rather than consulted.

**This challenges A.11f's `n ≥ 25` rule.** That rule rests on subsampling showing
the two classes *overlap* below n=25 — true, but overlap at the p95/p5 level does
not mean the statistics are uninformative for an individual unit scoring far
outside the overlap. `s1_L1_31` at gap 1.18 / empty 0.65 is not a marginal call.
**Discarding a strong signal because a weak one would be unreliable is the wrong
trade**, and it cost a wasted run plus 22 genomes admitted on false pretences.

> **SECOND PRE-REGISTERED PREDICTION.** Nine further unscreened units score as
> mixtures on the discarded statistics: **`s1_L1_10`** (0.84, 13/20),
> **`s1_L1_4`** (0.52, 12/20), **`s9_L1_4`** (0.66, 12/20), **`s1_L1_7`** (0.45,
> 12/20), **`s1_L1_16`** (1.35, 14/20), **`s1_L1_30`** (1.43, 15/20),
> **`s1_L1_11`** (3.94, 18/20), **`s18_L1_1`** (0.68, 11/20), **`s4_L1_4`**
> (0.53, 10/20). If the statistics retain signal below n=25, these should be
> **enriched for union and/or r/m failures** relative to the unscreened units
> scoring low on both (`s3_L1_8` 0.12/5, `s2_L1_4` 0.16/5, `s2_L1_8` 0.10/5,
> `s4_L1_6` 0.19/5, `s4_L1_5` 0.38/5). **Both groups are pending, so this is a
> genuine out-of-sample test** — and unlike the band prediction above it is not
> confounded, because the comparison is internal to the unscreened set.
>
> If it holds, the practical fix is cheap: **apply the modality rule below n=25
> as a one-sided screen — reject on a strong signal, stay silent otherwise** —
> rather than discarding the statistics wholesale.

**INTERIM RESULT: 7/8 — and the ONE MISS is the informative part.**

| group | n | r/m values |
|---|---|---|
| predicted **mixture**, failed as predicted | 18–22 | 0.79, 0.94, 1.31, **2.19** |
| predicted **mixture**, PASSED — a miss | 11 | **12.86** (`s1_L1_7`) |
| predicted **control**, passed as predicted | 15–22 | 5.80, 9.15, 10.22 |

**`s1_L1_7` returned the highest pooled r/m in the entire study (12.86)** while
having been predicted to fail. It is not a random miss: **its `gap/mean` of 0.45
is the LOWEST of the ten predicted mixtures** (the others run 0.52–3.94), and it
was flagged on `empty_bins` alone (12/20). **The prediction failed on its
weakest member**, which is the expected shape if the statistics carry a
dose-response rather than a categorical signal.

**This refines rather than refutes the recommendation, and tightens it.** A
one-sided screen below n=25 must fire only on a **strong** signal, and
`gap/mean` 0.45 with `empty_bins` 0.60 is evidently not strong enough. The four
true positives all carry `gap/mean` ≥ 0.52; the miss sits just below. **Do not
set the one-sided threshold at the standard `empty_bins > 0.45` — on this
evidence it needs `gap/mean` support as well**, i.e. an AND rather than the
OR used at n ≥ 25.

**Caveat on the miss itself:** at n = 11 there are ~20 branches, so pooled r/m is
computed from few terminal branches and may be unstable. A value of 12.86,
higher than any large unit, is as likely to reflect small-sample noise as
genuine recombination intensity. **r/m is not obviously trustworthy at n ≈ 10**,
which cuts against relying on it as the safety net for the smallest units — the
very units the unscreened block is made of.

**A.11f's "undecidable below n=25" should be narrowed.** The subsampling that
produced it showed the two classes *overlap* at small n, which is true and means
**marginal** calls are unreliable there. It does not follow that a unit scoring
gap/mean 3.94 with 18/20 empty bins is undecidable. Conflating "the marginal
region is wide" with "the statistic is uninformative" discarded usable
information and admitted a block that is failing at high rate (A.11q).

**Recommended rule, pending the remaining six:** below n = 25, apply the modality
screen **one-sided** — reject on a strong signal, remain silent otherwise. This
keeps the honest "undecidable" treatment for marginal units while refusing the
ones that are plainly mixtures. On the data so far it would have prevented **4
wasted production runs** and retained every unit that passed.

#### A.11m THE TWO DETECTORS CONTRADICT EACH OTHER — a case A.11 did not anticipate (2026-08-11)

A.11's two-detector design assumes union and r/m are **complementary**: each
catches a failure mode the other misses, so screening both is strictly safer than
either. The production runs show a third possibility the design has no rule for —
**they can disagree about the same unit.**

| unit | union | pooled r/m | tract | reading |
|---|---|---|---|---|
| `cluster_62` | 0.7% | 0.07 | 1,002 | both collapse — genuine failure |
| `cluster_53` | 18.0% | 1.25 | normal | both low — genuine, sparse |
| **`s5_L1_2`** | **42.3%** | **8.54** | **6,930** | **union condemns it, r/m exonerates it** |
| **`s1_L1_19`** | **78.1%** | **2.30** | 5,261 | **union exonerates it, r/m condemns it** |

**`s5_L1_2` is the sharper case.** Its r/m of 8.54 is among the highest ever
measured here and its tract is normal-to-large, which is not what
under-detected recombination looks like — under-detection collapses r/m, as
`cluster_62` and `cluster_53` both show. Yet the union rule drops it and its 28
genomes. **This is very likely a false rejection.**

**Two of ten production units so far show a detector disagreement.** The rule as
written ("fail if either fails") silently resolves every disagreement against the
unit, which was never calibrated and is not obviously right.

**`triage_analysable_bp.py` now reports `DISAGREE` as its own category** rather
than folding it into `UNDER-DETECT`, so these surface for a decision instead of
vanishing into the reject pile. **The tie-break rule is an open question and
should be decided deliberately, not by the accident of which test runs first.**

Options, none yet adopted: require both to fail before rejecting; treat
disagreement as "re-examine"; or weight by which statistic is better evidenced
for that failure mode — noting that after A.11j and A.11k, **neither is
well-evidenced any more**.

#### A.11n SUBDIVISION REPAIRS r/m BUT DEGRADES UNION — a paired within-lineage test (2026-08-11)

`s1_L1_27_L2_69` is the unit recovered by subdividing the known-bimodal
`s1_L1_27` (A.11f), so parent and child are the **same genetic material at two
partition depths** — a paired comparison, far stronger than the cross-sectional
correlations available elsewhere.

| | n | branches | ska | union | pooled r/m | tract |
|---|---|---|---|---|---|---|
| parent `s1_L1_27` | 150 | 299 | 1,698 | **59.5%** | **2.57** | 4,965 |
| child `s1_L1_27_L2_69` | 45 | 89 | 1,487 | **49.5%** | **4.94** | 5,844 |

**Result 1 — a positive control for bridging.** Removing the 95-genome clonal
group **nearly doubled r/m, 2.57 → 4.94**, into the healthy band. So the bridging
diagnosis was right, and **subdivision does repair r/m**. This is the test
proposed in A.11l, now run: where a low r/m is caused by bridging, splitting
fixes it.

**Result 2 — and it is a trap. Union moved the OTHER WAY, 59.5% → 49.5%**,
consistently on **both replicons** (56.5→46.2 and 62.5→52.7, ~10 points each).
Branch count fell 3.4× (299 → 89). **The child's chr1 arm alone, at 46.2%, is
BELOW the 47% cutoff**; only the two-arm mean (49.5%) keeps the unit.

**This partially revives a hypothesis refuted in A.11i, in a properly evidenced
form.** A.11i found union does *not* correlate with branch count **across** units
(r = −0.059) — correct, because between-unit biology swamps the effect. **Within
a lineage the effect is real and visible**, because the paired design removes that
variation. Cross-sectional and paired analyses answer different questions here;
neither result contradicts the other.

**THE METHODOLOGICAL CONSEQUENCE IS SERIOUS.** Subdivision is the method's own
prescribed remedy for a bimodal unit. Applying it **moves the two detectors in
opposite directions**: r/m improves, union degrades toward the rejection
threshold. Subdivide far enough and a genuinely sound unit fails the union screen
purely for having fewer branches. Combined with A.11k (the cutoff is no longer
insensitive) and A.11m (the detectors already contradict each other), **union
cannot currently be applied to subdivided units on the same footing as
undivided ones.** Any recovery-by-subdivision figure computed against a fixed
union cutoff is biased downward, and the bias grows with subdivision depth.

#### A.11o THE FLOOR'S ANCHOR IS AN OUTLIER — union is depressed across 1,268–1,709 (2026-08-11)

**This is the most consequential production finding, and it goes straight at the
floor.** A.11b set the floor bracket to (405, 1,268] on the strength of ONE unit,
`s1_L1_9` (ska 1,268, union 73.8%, r/m 4.28), and flagged the reliance on a
single point as the thing most likely to be wrong. Six further units have now
been measured in and just above that band.

| unit | ska | union | pooled r/m |
|---|---|---|---|
| **`s1_L1_9`** | **1,268** | **73.8%** | 4.28 |
| **`s3_L1_6`** | **1,288** | **40.2%** | 6.82 |
| `s2_L1_1` | 1,319 | **43.0%** | 7.53 |
| `s1_L1_27_L2_69` | 1,487 | 49.5% | 4.94 |
| `s5_L1_2` | 1,687 | **42.3%** | 8.54 |
| `s1_L1_27` | 1,698 | 59.5% | 2.57 |
| `s2_L1_5` | 1,701 | 53.8% | 7.71 |
| `s3_L1_5` | 1,709 | 47.9% | 6.79 |

**Banded means, in-range units only:**

| ska band | n | mean union | mean r/m |
|---|---|---|---|
| 1,200–1,800 | 8 | **51.3%** | 6.15 |
| 1,800–3,900 | 8 | **82.0%** | 8.11 |

**`s1_L1_9` sits 22 points above its own band's mean**, and every other unit
between 1,268 and 1,709 returns union 40.2–59.5%, straddling the 47% cutoff, with
three below it. **The floor was anchored to the single most favourable unit in
its band** — the precise failure mode A.11b warned about, now realised.

**THE DECISIVE PAIR.** `s3_L1_6` (ska **1,288**) sits **20 ska units** from
`s1_L1_9` (**1,268**) — indistinguishable diversity — and returns union
**40.2% against 73.8%, a 33.6-point gap**, while both have healthy r/m (6.82,
4.28). **At the floor, union varies by 34 points between units of the same
diversity.** No threshold placed on union can be a diversity floor when the
statistic scatters that widely at fixed diversity, and no floor derived from a
single unit at 1,268 can be trusted — `s1_L1_9` and `s3_L1_6` would have licensed
floors 34 points apart on the same reasoning.

**Union tracks diversity strongly at the low end** (52.8% → 82.0% across the
band boundary), which means the union screen is substantially acting as a
**second, implicit diversity floor** rather than as an independent detection
test. The two screens are not independent, contrary to the A.11 framing.

**The two detectors give opposite verdicts on this whole band.** Union says
1,268–1,709 is marginal-to-failing; r/m says it is healthy (mean 6.05, and every
unit except the bridged `s1_L1_27` lies in 4.28–8.54). A.11's own logic assigns
union the job of detecting the below-floor failure mode — so on A.11's terms the
detector is doing its job and **the floor should be higher than 1,270**.

**THE DECISION IS A COVERAGE CALL AND SHOULD BE MADE EXPLICITLY, NOT INHERITED.**

- **Raise the floor to ~1,800** (union's verdict, self-consistent with A.11's
  assignment of roles). Cost: all 7 units in the band leave the analysable set —
  `s1_L1_9` (90), `s3_L1_5` (51), `s1_L1_27_L2_69` (45), `s2_L1_5` (29),
  `s5_L1_2` (28), `s2_L1_1` (23) ≈ **266 genomes**, roughly a fifth of the
  analysable set.
- **Keep the floor at ~1,270** (r/m's verdict). Requires accepting that the union
  cutoff misclassifies low-diversity units, which A.11m already documents as a
  live problem in both directions.

**Do not split the difference silently.** Whichever is chosen, the write-up must
state that the floor's original anchor is a within-band outlier and that the two
screens disagree across the entire band beneath ~1,800.

#### A.11q THE UNSCREENED UNITS ARE FAILING AT 5× THE SCREENED RATE — 44.0% will not survive (2026-08-11, INTERIM)

**Interim, 18 of 45 units scored. The effect is large enough to report now
because it changes the headline coverage figure.**

| group | units scored | OK | pass rate | genomes OK / scored |
|---|---|---|---|---|
| **screened** (n ≥ 25) | 11 | 8 | **73%** | 570 / 660 |
| **unscreened** (n < 25) | 7 | 1 | **14%** | 22 / 151 |

The only unscreened unit to pass cleanly is `s3_L1_8`, which scores low on both
modality statistics (gap 0.12, empty 5/20) — i.e. the one that would have passed
the screen had the screen been applied.

**Naive projection, and it should be treated as indicative only** (7 of 25
unscreened units in, no PopPUNK strains scored yet): at these rates the analysable
set lands near **~775 genomes ≈ 28%**, not 1,233 ≈ 44.0%. The screened block holds
up (570 of 660 genomes); the unscreened block largely evaporates, contributing
perhaps 50 genomes rather than 360.

**What this vindicates, and what it does not.** The r/m safety net **is** doing
its job — the bridged unscreened units are being caught, exactly as §0 said they
would be. What fails is the **coverage claim built on top of it**: admitting 360
genomes that mostly cannot be used is not 44.0% coverage, it is 29.6% coverage
plus a queue of wasted runs. §0's framing — "expect wasted runs and treat r/m as
the flag" — understated this: it is not a minority of wasted runs but the
majority of that block.

**Consequences.**

1. **Stop quoting 44.0%.** Quote the screened-only figure (29.6%) as the
   defensible one, with the unscreened block reported as a measured yield rather
   than an assumed one.
2. **A.11p's one-sided screen would have recovered most of the wasted compute.**
   Of the 6 failing unscreened units, at least 3 (`s1_L1_31`, `s1_L1_10`,
   `s1_L1_4`) score as mixtures on the discarded statistics and were predictable
   before running. See the A.11p prediction, now **4 for 4**.
3. **The `n < 25` "undecidable" bucket is not neutral.** It was adopted as "an
   honest description" rather than a rejection, but in practice it admitted a
   block that fails at 86% and inflated the coverage headline by 14 points.

#### A.11r ★ UNION IS A SIZE STATISTIC — r(log n, union) = +0.81. This supersedes A.11i, A.11o and A.11q (2026-08-11)

**The single most important production finding, and it invalidates the union
screen as currently applied.** Over the 19 production units, which span
**n = 18–155** — a spread the calibration set never had, being almost entirely
n ≈ 50:

| correlate | Pearson r | reading |
|---|---|---|
| **log(unit size n) vs union** | **+0.810** | **union is largely a function of how many genomes are in the unit** |
| ska diversity vs union | +0.260 | weak; diversity is **not** the driver |
| log(n) vs pooled r/m | +0.373 | r/m is far less size-sensitive |

| group | mean union |
|---|---|
| n ≥ 45 (7 units) | **74.9%** |
| n < 25 (8 units) | **43.9%** |

**The n < 25 group averages BELOW the 47% cutoff.** A fixed union threshold
applied across n = 7–155 is therefore substantially a **size filter**, rejecting
small units irrespective of their biology.

**THREE OF MY OWN CONCLUSIONS FROM TODAY ARE WRONG. Corrections, in order.**

1. **A.11i — "union does not scale with n (r = 0.142)" — WITHDRAWN.** The test
   was run on a set dominated by n ≈ 50 calibration clusters, i.e. with almost no
   variance in the predictor. Absence of spread was mistaken for absence of
   effect. A.11n's paired within-lineage test (299 → 89 branches, union
   59.5 → 49.5%) was the first correct signal and should have prompted this
   re-test immediately rather than being filed as a curiosity.

2. **A.11o's causal reading — WITHDRAWN; its description stands.** The
   "decisive pair" is real but misattributed: `s1_L1_9` (union 73.8%) and
   `s3_L1_6` (40.2%) sit 20 ska units apart, **but differ 4.3× in size (n = 90
   vs 21)**. The 33.6-point gap is a size effect, not diversity scatter. The
   low-union band at ska 1,200–1,800 is likewise confounded — that band simply
   holds most of the small units. **The floor's anchor is still an outlier and
   the floor is still not established**, but union cannot be used to relocate it.

3. **A.11q's projection — TOO PESSIMISTIC, revised.** The unscreened block is
   n < 25 *by definition*, so it absorbs the full force of the size bias. Its
   apparent 86% failure rate is substantially an artefact of the screen.

**Corrected pass rates:**

| group | union AND r/m (current rule) | r/m only (size-corrected) |
|---|---|---|
| screened | 8/11 = 73% (570 genomes) | 9/11 = **82%** (598 genomes) |
| unscreened | 1/8 = 12% (22 genomes) | 4/8 = **50%** (84 genomes) |

Four units are low on union with healthy r/m (5.90–8.54) and are very likely
**false rejections**: `s2_L1_7` (n=18), `s3_L1_6` (21), `s2_L1_1` (23),
`s5_L1_2` (28). Every one is small. This is the mechanism behind **all four
A.11m DISAGREE cases** — small unit → depressed union (artefact) → healthy r/m
(biology) → detectors contradict. The disagreement was never mysterious.

**WHAT TO DO — the union screen cannot be applied as-is.**

- **Do not apply a fixed union cutoff across units of differing size.** At
  minimum, restrict comparisons to comparable n, or size-normalise. The
  literature-anchored 78% and the 47% cutoff were both established on n ≈ 50
  units and transfer to no other size.
- **Until then, weight r/m over union for small units**, exactly inverting
  A.11's assumption that union is the better-evidenced detector.
- **Genuine under-detection is still detectable** — it collapses **both**
  statistics (`cluster_62`, `s1_L1_31`, `s1_L1_10`, `s1_L1_4`). It is the
  union-only failures that are suspect.
- **Re-derive the floor.** A.11b's floor rests on `s1_L1_9`, whose union is now
  explained by its n = 90 rather than by its diversity.

**Mechanism, stated plainly:** union counts sites recombinant on **at least one**
branch. More genomes means more branches means more opportunity for any given
site to be flagged somewhere. It is a **cumulative** statistic and cannot be
compared across sample sizes without normalisation — the same reason A.11c's
"78% of K96243 ever recombined" was never the right anchor (A.11i).

**THE DECISIVE ILLUSTRATION — two units, the same union, opposite biology.**

| unit | n | union | pooled r/m | tract | A.11c verdict on union alone |
|---|---|---|---|---|---|
| `cluster_53` | 49 | **18.0%** | **1.25** | normal | genuine detection failure |
| `s18_L1_1` | **7** | **17.9%** | **9.11** | 6,574 | *identical union* — yet r/m is **7× higher** |

`cluster_53` is the canonical "recombination genuinely missed" case that helped
set the union cutoff. `s18_L1_1` sits **0.1 points away from it on union** and
returns a pooled r/m of 9.11, among the healthiest in the entire study, with a
normal 6.6 kb tract. **Union at 18% therefore cannot distinguish a genuine
detection failure from a healthy 7-genome unit.** No threshold on an
unnormalised union can, because the statistic is measuring sample size as much
as biology at this end of the range.

#### A.11s AT n < 25, `gap/mean` ALONE BEATS THE CALIBRATED RULE — and `empty_bins` hurts (2026-08-11)

Scoring all three candidate screens against measured outcome (`bad` = pooled
r/m < 3.0) over the **20 small units** now run:

> **⚠ THIS SECTION WAS WRITTEN AT 20 UNITS AND CORRECTED AT 22, ~4 MINUTES
> LATER, WHEN `s16_L1_3` LANDED. The overfitting caveat below fired almost
> immediately. Both versions are kept; the corrected scoring is the one to use.**

**Corrected scoring over 22 small units** (`bad` = pooled r/m < 3.0):

| rule | correct | errors |
|---|---|---|
| **A.11f OR-rule** (`gap>1.0` OR `empty>0.45`) | **19/22** | FP `s1_L1_7` (12.86); FN `s3_L1_10` (2.03), `s2_L1_9` (1.94) |
| **`gap/mean ≥ 0.52` alone** | **20/22** | FN `s3_L1_10` (2.03); **FP `s16_L1_3` (10.43)** |
| `gap ≥ 0.70` alone | 18/22 | 4 FN |
| `gap > 1.0` alone | 17/22 | 5 FN |

*(Superseded first pass, at 20 units: 19/20 for `gap≥0.52` against 17/20 for the
OR-rule — a 2-unit margin that has since narrowed to 1.)*

**THE DECISIVE OBSERVATION, AND IT LIMITS EVERY THRESHOLD ON THIS STATISTIC.**
`s16_L1_3` and `s9_L1_4` have **identical `gap/mean` of 0.66 and opposite
outcomes** — r/m **10.43** versus **0.94**. **No cutoff on `gap/mean` can
classify both correctly**, so the "clean separation" visible at 20 units was an
artefact of which units had finished. The best achievable with this statistic
alone is 21/22, and the realised figure is 20/22.

**What survives and what does not.**

- **Does not survive:** the claim of near-perfect separation, and the specific
  0.52 threshold. The margin over the calibrated rule is now **one unit** — not
  a sound basis for replacing a rule calibrated by subsampling.
- **Partly survives:** `empty_bins` still causes the OR-rule's only false
  positive (`s1_L1_7`, the highest r/m in the study). But it also *correctly*
  spares `s16_L1_3`, which scores exactly 9/20 = 0.45 and so is not flagged.
  **So `empty_bins` both helps and hurts at small n**; the earlier "it only adds
  noise" verdict was too strong.
- **Survives intact:** at n < 25 **neither statistic is reliable**, and both the
  A.11f rule and every `gap/mean` variant misclassify 2–5 of 22 units.

**`empty_bins` does not merely fail to help below n=25; it causes the only false
positive.** The OR-rule discards `s1_L1_7` on `empty_bins` 12/20 despite
`gap/mean` 0.45, and that unit returned **the highest pooled r/m in the entire
study (12.86)**. Adding `empty_bins` as an AND instead costs a true positive.
Either way it degrades the screen at small n.

**This does NOT contradict A.11f, which was calibrated at n ≥ 25.** There
`empty_bins` demonstrably earned its place, catching a 4-modal cluster that
`gap/mean` scored at 0.128. The two statistics simply behave differently at
different sizes: `empty_bins` is a 20-bin histogram occupancy measure, and with
fewer than ~25 genomes the pairwise-distance histogram is sparse for reasons of
sample size alone — the same cumulative-statistic problem that afflicts union
(A.11r). **`gap/mean` is a ratio and is far less size-sensitive.**

> **⚠ OVERFITTING CAVEAT — read before adopting.** The 0.52 threshold was read
> off these 20 units *post hoc*. Treat it as unvalidated.

##### FINAL ANALYSIS on the COMPLETE n<25 set (all 25 units, 2026-08-11)

**First, the headline: 16 of the 25 unscreened units PASS on r/m (64%).** The
block is mostly sound. The 12–14% pass rates reported earlier in A.11q were an
artefact of judging small units on union (A.11r), not a property of the units.

| rule | correct | FP (good unit wasted) | FN (bad unit run) |
|---|---|---|---|
| **`gap/mean > 1.0` alone** | 20/25 | **0** | 5 |
| `gap/mean ≥ 0.52` | 21/25 | 3 | 1 |
| A.11f OR-rule | 20/25 | 3 | 2 |
| `empty_bins > 0.45` alone | 20/25 | 3 | 2 |
| accept all (status quo) | 16/25 | 0 | 9 |
| reject all n<25 | 9/25 | **16** | 0 |

**`gap/mean > 1.0` — A.11f's OWN threshold — is the right one-sided screen, and
my 0.52 proposal was wrong.** It has the highest raw accuracy only on a tie, but
it is the **only rule that never rejects a good unit**: the largest `gap/mean`
among the 16 passing units is 0.68, and all four units above 1.0 fail. The
asymmetry decides it — a false positive is a **silent permanent loss** of a
usable unit, a false negative is one **recoverable wasted run**. On this data
`gap/mean > 1.0` saves 4 of the 9 wasted runs at **zero** cost.

**`empty_bins` must NOT be applied below n = 25.** Every false positive in every
rule tested traces to it — `s1_L1_7` (12/20, r/m **12.86**), `s18_L1_1` (11/20,
9.11), `s4_L1_4` (10/20, 6.06). This is the size confound again: `empty_bins`
counts occupancy of a 20-bin histogram, and a 7–12 genome unit has 21–66 pairwise
distances to fill 20 bins, so bins are empty from sparsity alone. **It is a
cumulative-sampling statistic, exactly like union (A.11r), and fails the same
way.** At n ≥ 25 it remains justified (A.11f).

**So the corrected recommendation is conservative, not novel:** keep A.11f's
`gap/mean > 1.0`, apply it **one-sided** below n = 25, and **drop the
`empty_bins` clause there**. No new constant is introduced, and nothing is fitted
post hoc.

**`s3_L1_10` remains the one failure no rule catches** (gap 0.28, empty 6/20,
r/m 2.03) — the A.11l band anomaly, still unexplained.

#### A.11t ★ N2/N3 COMPLETE — final coverage is 33.3%, not 44.0% (2026-08-11)

**All 45 analysable units run, 180 arms, zero arm failures.** Scored with
`triage_analysable_bp.py`.

| verdict | units | genomes |
|---|---|---|
| `OK` (passes both screens) | 12 | 662 |
| `UNION-SIZE` (low union, healthy r/m, small n — likely false rejections) | 17 | 235 |
| `RM-MARGINAL` (r/m inside the cutoff's own support bracket) | 1 | 36 |
| `RM-LOW` | 4 | 116 |
| `UNDER-DETECT` (both screens agree) | 11 | 184 |
| **total** | **45** | **1,233** |

**COVERAGE, and the choice of reading matters more than anything else measured
today:**

| reading | units | genomes | % of 2,802 |
|---|---|---|---|
| claimed before the run | 45 | 1,233 | **44.0%** |
| **size-corrected** (judge small units on r/m, per A.11r) | **30** | **933** | **33.3%** |
| strict (union AND r/m, as A.11 specifies) | 12 | 662 | **23.6%** |

**The recommended figure is 33.3%.** The strict reading discards 17 units whose
low union is an artefact of their size (A.11r) while their r/m is healthy —
5.29–12.86, i.e. mid-to-high band. Reporting 23.6% would understate the usable
set as badly as 44.0% overstates it.

**PASS RATES BY PROVENANCE — and the surprise is which block did worst.**

| block | units | genomes | note |
|---|---|---|---|
| screened sub-clusters (n ≥ 25) | 9/11 = **82%** | 598/660 | held up, as expected |
| unscreened sub-clusters (n < 25) | 16/25 = **64%** | 224/360 | **far better than A.11q feared** |
| **PopPUNK strains** | **5/9 = 56%** | **111/213** | **the WORST block** |

**The strains were the block nobody worried about.** They entered the analysable
set as "PopPUNK strains already in range", exempt from modality screening
(`screened = n/a`) on the grounds that they are not sub-clusters. They failed at
the highest rate of any group, including `strain_8` (n=46, ska 1,265, union
36.2%, r/m 1.46 — both screens agree) and `strain_15` (n=30, ska 4,442, r/m
1.15). **Being a PopPUNK strain rather than a fastbaps sub-cluster confers no
protection against bridging**, and the exemption was never justified by
measurement. If any block deserved the scrutiny the n<25 units received, it was
this one.

**A.11q is superseded.** Its interim projection (~28%, unscreened block
"evaporating") was distorted by the union confound it predated. The unscreened
block delivers 224 genomes at a 64% unit pass rate — the deliberate compromise
was **more defensible than it looked**, though the honest figure is still 64%
yield, not the 100% the 44.0% headline assumed.

**Where the losses actually are:** 11 units / 184 genomes fail both screens and
are genuine, and 4 units / 116 genomes are `RM-LOW`. Of the 11 genuine failures,
**8 carry `gap/mean` or `empty_bins` scores that flagged them in advance** and
9 of 11 have n < 25 — so A.11s's one-sided `gap/mean > 1.0` screen would have
avoided a substantial share of the wasted compute.

**DECISIONS TAKEN 2026-08-11:** the user adopted **33.3%** as the reported
coverage figure, and directed that the PopPUNK strains be re-screened — see
A.11u.

#### A.11u THE STRAINS RE-SCREENED — one glaring mixture found, but screening does NOT fix the block (2026-08-11)

The 9 PopPUNK strains were modality-screened for the first time
(`measure_diversity_bp.py --screen-all --min-n 7`, 24/24 self-tests passing).
Because their outcomes were already measured, this is a **clean retrospective
test** of what screening them would have bought. Units with n ≥ 25 are judged on
the full A.11f rule; those below on A.11s's one-sided `gap/mean > 1.0`.

| strain | n | gap/mean | empty | screen verdict | measured r/m | outcome | screen right? |
|---|---|---|---|---|---|---|---|
| `strain_8` | 46 | **2.695** | 12/20 | **MIXTURE** | 1.46 | FAIL | **✔ caught** |
| `strain_12` | 37 | 0.093 | 4/20 | pass | 3.77 | pass | ✔ |
| `strain_13` | 36 | 0.262 | 8/20 | pass | 2.89 | marginal | ✘ |
| `strain_15` | 30 | 0.610 | 9/20 | pass | 1.15 | FAIL | ✘ missed |
| `strain_17` | 19 | 0.467 | 10/20 | pass (one-sided) | 5.29 | pass | ✔ |
| `strain_20` | 14 | 0.516 | 15/20 | pass (one-sided) | 0.56 | FAIL | ✘ missed |
| `strain_23` | 12 | 0.909 | 10/20 | pass (one-sided) | 1.13 | FAIL | ✘ missed |
| `strain_24` | 12 | 0.183 | 8/20 | pass (one-sided) | 4.64 | pass | ✔ |
| `strain_33` | 7 | 0.378 | 11/20 | pass (one-sided) | 7.74 | pass | ✔ |

**Caught 1 of 5 failures. Correctly passed 4 of 4 successes. ZERO false
positives.**

**The single catch is nonetheless damning for the exemption.** `strain_8` scores
`gap/mean` **2.695** — the second-highest value ever measured on this project,
behind only `s1_L1_11`'s 3.94 — and it is the **largest strain (n = 46)**. A
blatant mixture was admitted to the analysable set purely because PopPUNK strains
were exempted from screening **by category rather than by measurement**. It then
failed both detection screens (union 36.2%, r/m 1.46). Screening costs minutes
and would have removed 46 genomes of wasted analysis up front.

**But it does not rescue the block, and the reason matters.** The other four
strain failures carry `gap/mean` of 0.262, 0.516, 0.610 and 0.909 — all below any
defensible mixture threshold. `strain_15` (r/m 1.15) is a clear failure sitting at
`empty_bins` exactly 9/20 = 0.45, flagged by neither statistic. **The strains fail
predominantly for reasons modality does not capture**, and no diversity pattern
separates them either: failures span ska 1,265–4,442 and successes 1,700–3,252,
interleaved.

**RECOMMENDATION — adopt the screen, but on the correct grounds.** Apply modality
screening to PopPUNK strains: it is cheap, has **zero false positives** here, and
catches the worst offender. Do **not** claim it fixes the strain block — measured
sensitivity is 1 in 5. **The strains' 56% yield remains substantially
unexplained**, placing them alongside `s3_L1_10` and the ska 3,956–4,088 dip
(A.11l) in the category of r/m failures that no upstream statistic predicts.
**That category is now the single largest open problem in the method.**

**Files:** `strain_modality_measured.tsv`, `inputs/strain_membership.tsv`,
`strain_screen.log`.

#### A.11v ★ N4's PER-UNIT STAGE WAS ALREADY COMPLETE — and tree resolution is a THIRD, INDEPENDENT quality axis (2026-08-11)

**N4 as specified requires no new computation.** Its stated content — per-unit
replicon split, pinned Gubbins ≥ 3.4.3 with explicit `--invariant-site-correction`,
`-fconst` from full alignments, trees — is *exactly* the configuration the
`prod_` runs already executed. **90 trees exist (45 units × 2 replicons) against
each unit's close reference.** Verified for all 30 usable units: tip counts equal
n in every case, models are the expected K3Pu+F+I / HKY+F+I family for a 68% GC
genome. Re-running would have reproduced them.

**What had never been checked is whether the trees are RESOLVED.** Median
ultrafast-bootstrap support per unit, over the 30 usable units:

| correlate | Pearson r |
|---|---|
| ska diversity vs median UFBoot | **+0.501** |
| log(n) vs median UFBoot | +0.171 |
| **pooled r/m vs median UFBoot** | **−0.010** |

| ska band | units | mean median-UFBoot |
|---|---|---|
| < 2,000 | 14 | **79** |
| ≥ 3,000 | 9 | **93** |

**Tree resolution is orthogonal to r/m (r = −0.010).** This matters because
**r/m is now the sole adopted criterion** (A.11t): a unit can pass it and still
yield a tree too poorly supported to use. Union does not capture it either,
being size-confounded (A.11r), and resolution is only weakly size-dependent
(+0.171) — so it is genuinely a **third axis**, not a restatement of either
screen.

**Six usable units have mean median-UFBoot below 75:**

| unit | n | ska | UFBoot | pooled r/m |
|---|---|---|---|---|
| **`s1_L1_9`** | 90 | **1,268** | **66** | 4.28 |
| `s3_L1_6` | 21 | 1,288 | **53** | 6.82 |
| `s16_L1_3` | 8 | 1,752 | 58 | 10.43 |
| `s5_L1_4` | 15 | 2,089 | 66 | 6.12 |
| `strain_13` | 36 | 2,634 | 69 | 2.89 |
| `s4_L1_4` | 7 | 2,706 | 61 | 6.06 |

**AND THIS BEARS ON THE FLOOR — but see A.11x, which tested it and found UFBoot
CANNOT re-derive the floor.**
`s1_L1_9` — the unit the entire floor rests on (A.11b) — produces the
**second-worst-resolved tree in the usable set** (median UFBoot 66, and only
**50** on chromosome 2). `s3_L1_6` at ska 1,288 is worse still at 53 despite a
healthy r/m of 6.82. **At the floor, Gubbins assigns recombination normally but
there is not enough signal left to resolve a tree.**

The floor's anchor has now failed three separate tests: its union is explained by
its size (A.11r), a unit at the same diversity fails outright (`strain_8`,
A.11t), and its tree is among the least resolved measured here. **Union was
size-confounded and r/m is resolution-blind; UFBoot is neither.** It is the
best-suited statistic yet identified for re-deriving the floor.

~~**RECOMMENDATION.** Add **median UFBoot ≥ 70** as a third acceptance criterion
alongside pooled r/m.~~ **— WITHDRAWN, see the banner immediately below and
A.11y. Report resolution; collapse unsupported branches; do not gate on it.**

##### ~~ADOPTED 2026-08-11 — final coverage is 25.3%~~ — **WITHDRAWN 2026-08-11, see A.11y**

> ## ⚠ THIS ADOPTION IS WITHDRAWN. The UFBoot gate is not defensible.
> **Two reasons, in A.11y.** (1) 70 is the STANDARD-bootstrap convention;
> UFBoot's own is 95, so applying 70 to UFBoot was *more permissive* than the
> convention cited to justify it, not more conservative. (2) Coverage moves
> **5.3×** (33.3% → 6.3%) across the range of thresholds a reasonable person
> might pick, so the headline was reporting a convention.
> **The observation below is sound and is retained** — tree resolution really is
> a third axis, orthogonal to r/m (−0.010). What is withdrawn is using it as a
> GATE. Unsupported branches are now collapsed into polytomies
> (`collapse_unsupported_bp.py`) and every unit is kept.
> **FINAL COVERAGE IS 33.3% (30 units, 933 genomes).** The 25.3% figure below is
> retained as the record of what was adopted and why it did not survive.

The filter was applied on the **worse of the two replicons** (a unit whose
chromosome 2 tree is unresolved is not rescued by chromosome 1; both are needed).
Implemented in `triage_analysable_bp.py` as the `UNRESOLVED` verdict, applied
**only to units that already pass detection**, so it cannot relabel a genuine
failure.

| criterion set | units | genomes | % of 2,802 |
|---|---|---|---|
| detection only (union/r/m) | 30 | 933 | 33.3% |
| **+ UFBoot ≥ 70 (ADOPTED)** | **22** | **708** | **25.3%** |
| cost of the filter | −8 | −225 | −8.0 pts |

**The eight units removed, every one of which passed detection:**

| unit | n | ska | pooled r/m | UFBoot |
|---|---|---|---|---|
| **`s1_L1_9`** | **90** | **1,268** | 4.28 | **50.0** |
| `strain_13` | 36 | 2,634 | 2.89 | 61.0 |
| `s2_L1_5` | 29 | 1,701 | 7.71 | **69.5** |
| `s3_L1_6` | 21 | 1,288 | 6.82 | **34.5** |
| `strain_17` | 19 | 3,252 | 5.29 | 68.0 |
| `s5_L1_4` | 15 | 2,089 | 6.12 | 60.0 |
| `s16_L1_3` | 8 | 1,752 | 10.43 | 43.0 |
| `s4_L1_4` | 7 | 2,706 | 6.06 | 59.0 |

**Note `s16_L1_3`: pooled r/m 10.43 — near the top of the whole study — with a
median UFBoot of 43.** That single row is the argument for the criterion: r/m
says recombination was assigned excellently, and the tree is still barely
resolved. The two statistics are measuring different things, and only one of
them bears on whether a tree can be used.

**`s1_L1_9` — the floor anchor — is removed**, and it is the largest casualty at
90 genomes. Its exclusion is not a marginal call: median UFBoot 50 on chromosome
2. The floor now rests on **no** surviving unit at its own diversity.

> **⚠ The suggestion below — that UFBoot is the best statistic for re-deriving
> the floor — was TESTED AND IS WITHDRAWN. See A.11x.** `cluster_53` at ska 535
> has median UFBoot 94.5, so UFBoot places no boundary at the low end; it tracks
> phylogenetic signal, which keeps rising into the regime where recombination
> detection has already collapsed. It is a sound acceptance criterion and a
> useless floor statistic.

**By block:**

| block | detection only | + UFBoot |
|---|---|---|
| screened (n ≥ 25) | 9 units / 598 | **7 units / 479** |
| unscreened (n < 25) | 16 units / 224 | **12 units / 173** |
| PopPUNK strains | 5 units / 111 | **3 units / 56** |

The strains lose proportionally most again (56% → 33% of their units), extending
A.11u's finding.

**The accepted set spans ska 1,290–4,400 (median 2,456)** — it still populates
the low-diversity end, so the filter has not silently become a diversity gate.

> **The 70 threshold is a CONVENTION, not a measurement.** It is the standard
> ultrafast-bootstrap "supported" cutoff, in the same class as the 5e-06 slope
> cutoff (A.11e). `s2_L1_5` fails at **69.5** — half a point — so the boundary
> decides real units and 225 genomes ride on a round number. Anyone reporting
> 25.3% should say the criterion is conventional and give the 33.3%
> detection-only figure alongside.

#### A.11x ★ THE FLOOR CANNOT BE RE-DERIVED FROM UFBoot — and it now rests on NO valid evidence (2026-08-11)

Attempted per A.11v's recommendation, over **63 units with trees and known
diversity** (run precedence `prod_` > `reduced_` > `fbL1_` > `refsens_`).
**The attempt fails, and A.11v's recommendation is WITHDRAWN.**

##### 1. UFBoot does not locate a floor

| unit | ska | n | median UFBoot |
|---|---|---|---|
| `cluster_62` | 405 | 40 | 45.0 |
| **`cluster_53`** | **535** | 49 | **94.5** |
| `strain_8` | 1,265 | 46 | 37.0 |
| `s1_L1_9` | 1,268 | 90 | 50.0 |
| `s3_L1_6` | 1,288 | 21 | 34.5 |
| **`s18_L1_1`** | **1,290** | 7 | **80.5** |
| `s2_L1_4` | 1,372 | 17 | 84.0 |

**`cluster_53` at ska 535 — far below any proposed floor — returns median UFBoot
94.5, among the best-resolved trees in the study.** Within the 25-unit window
1,265–1,290, UFBoot spans **34.5 to 80.5**. The correlation with diversity is
real (+0.476 overall, +0.421 in-range) but the scatter is far too wide to place
a boundary anywhere.

**Worse, UFBoot rises into the regime where the analysis is worthless.**
`cluster_2` at ska 13,826, where recombination detection has completely collapsed
(r/m 0.16), has **UFBoot 98**. **UFBoot measures phylogenetic signal, not
recombination-detection viability** — more divergence gives better-resolved trees
whether or not Gubbins can still work. It is a valid *acceptance* criterion
(A.11v) and a useless *floor* statistic. Those are different jobs and A.11v
conflated them.

##### 2. Nor can the floor be derived from detection — the evidence is disqualified

Only **three** units sit below ska 1,268, and all three fail detection, which
looks like clean support for a floor there. It is not:

| unit | ska | pooled r/m | gap/mean | empty_bins | admissible as floor evidence? |
|---|---|---|---|---|---|
| `cluster_62` | 405 | 0.07 | 0.007 | **18/20 = 0.90** | **no — see below** |
| `cluster_53` | 535 | 1.25 | **1.549** | 15/20 | **no — MIXTURE** |
| `strain_8` | 1,265 | 1.46 | **2.695** | 12/20 | **no — MIXTURE** |

**A.11e's own rule disqualifies two of them outright:** *"a MIXTURE was used to
set a diversity threshold… mixtures cannot set diversity thresholds because
their failures are confounded by structure."* `cluster_53` (gap/mean 1.549) and
`strain_8` (2.695) are unambiguous mixtures, so their failures are attributable
to bridging, not to diversity. That was exactly the error A.11d made with
`cluster_48`, and it is repeated here in the opposite direction.

**And `cluster_62` cannot be assessed at all — this is circular.** Its
`empty_bins` of **18/20 = 0.90** far exceeds the 0.45 mixture threshold, so under
the calibrated A.11f rule it *would* be a mixture. But A.11f also requires the
**diversity gate to be applied first**, and `cluster_62` at ska 405 sits below
that gate, so its modality is formally undefined. **To know whether its failure
is diversity-driven or structural we would need a modality verdict, and the rule
forbids issuing one outside a range whose lower bound is the very thing being
derived.**

##### 3. Consequence: the floor bracket is (405, 1,268] and rests on nothing admissible

Nothing measured today moved it, and its supporting evidence is now known to be
confounded (two mixtures) or uninterpretable (one circular case). Its former
anchor `s1_L1_9` has separately been removed from the accepted set by the UFBoot
criterion (A.11v).

**The strong statement the data supports is uncomfortable: there is no
demonstrated diversity floor.** Every observed failure below 1,268 has an
available structural explanation, and above 1,268 diversity has little
predictive power over detection — failures scatter across 1,698, 1,787, 1,975,
2,452, 2,634, 2,700, 3,024, 3,745 and upward, interleaved with passes.

**What would settle it:** a **continuous** (non-mixture) unit with n ≥ 25 in the
band **535–1,265**. None exists in the current partition. This is the same
missing observation A.11l needs for the r/m dip, and it cannot be obtained by
re-running — it requires a partition that produces low-diversity *unimodal*
units, which fastbaps L1 does not.

**Do not quote ~1,270 as a measured floor.** It is the lowest diversity at which
a unit has been *observed to work*, which is a different and much weaker claim.

#### A.11w WHAT ACTUALLY REMAINS AFTER N4 — the merge, and it is the documented blocker (2026-08-11)

With the per-unit stage complete (A.11v), the next step is combining 30 units ×
2 replicons into a collection-level phylogeny. **That step is the one this
project has repeatedly documented as unsolved, and it was not attempted.**

1. **The merge under recombination is unsolved.** Listed as open in §0 ("needs
   simulation not clusters") and in Appendix B, where the claim narrowed to
   exactly this: grafting *per se* has precedent, **the merge under
   recombination does not**.
2. ~~**Branch-length units are incommensurable.** The backbone is substitutions
   per core-genome site; the per-unit subtrees are substitutions per *variable*
   site.~~ **WITHDRAWN 2026-08-11 (Tier 0.2) — this was wrong, and it
   contradicted our own settled configuration.** With `-fconst` taken from the
   **full** alignment (§0, T6/T7 — which every `prod_` run did), the per-unit
   branch lengths are **already** in substitutions per site of the full
   alignment, not per variable site. The claim was inherited from the pipeline's
   pre-`-fconst` configuration and should not have survived into a document that
   also prescribes `-fconst` from the full alignment. Anyone reading both at once
   is entitled to notice that both cannot be true.
   **What actually remains is smaller but real:** (a) each unit was aligned to a
   **different reference**, so "per site of the full alignment" denotes a
   different position set per unit — same units, not quite the same quantity, and
   the discrepancy is *measurable* as the pairwise overlap of those position
   sets; (b) recombination was corrected independently per unit, so what counts
   as vertical differs slightly between them, and that has no standard solution.
   **The practical guidance is unchanged — do not date a grafted tree — but the
   stated reason must be corrected.**
3. **A new instance of the same problem, one level down.** Each unit now has
   **two** trees (chr1, chr2), because Gubbins forced a replicon split. Merging
   those is the same unsolved problem in miniature, and chromosome 2 is
   accessory-rich, so topological discordance between them is expected rather
   than exceptional. **No per-unit consensus tree exists, and none can be
   produced without deciding this.**

**Nothing further should be run until the merge question is settled** — the
compute is cheap but every product built on an unjustified merge inherits the
flaw. The recommended next step remains **simulation** (SimBac at
*B. pseudomallei*-like parameters: r/m 7.2, tract ~5 kb, two-replicon 7.2 Mbp),
which §3 already identifies and which answers the merge and the
does-clustering-track-clonal-descent question from one run.

---

#### A.11y ★ THE UFBoot GATE IS WITHDRAWN — the headline moved 5.3× on a convention (2026-08-11, TIER 0.1/0.3)

**This supersedes A.11v's adoption and restores the coverage figure to 33.3%.**
Reproduce with `python3 tier0_evidence_bp.py`.

**1. The threshold was on the wrong scale.** IQ-TREE's ultrafast bootstrap is not
the standard nonparametric bootstrap. The conventional "supported" line for
UFBoot is **≥ 95**, which corresponds roughly to SBS ≥ 70. A.11v applied
**UFBoot ≥ 70** while citing the ≥ 70 convention — importing a number from the
scale it does not belong to. The gate we believed was conservative was
substantially **more permissive** than the convention we cited.

**2. And the choice decides the headline.** Units and genomes surviving
detection, varying only the support threshold:

| threshold | units | genomes | coverage |
|---|---|---|---|
| **detection only, no gate** | **30** | **933** | **33.3%** |
| UFBoot ≥ 70 (adopted in A.11v) | 22 | 708 | 25.3% |
| UFBoot ≥ 80 | 17 | 632 | 22.6% |
| UFBoot ≥ 90 | 10 | 437 | 15.6% |
| UFBoot ≥ 95 (UFBoot's own convention) | 7 | 176 | 6.3% |

**33.3% → 6.3% is 5.3×.** A number that moves 5.3× across defensible conventions
is not a result, and 25.3% cannot be quoted without 6.3% and 33.3% beside it.
This is A.11e's 5e-06 problem and §6.8's round-number problem in a more expensive
form: there, a round number decided one unit; here it decides **225 genomes**.

**3. What replaces it: collapse, do not discard.** An unsupported branch is
identifiable and local. Deleting the *edge* and reattaching its children makes the
node a polytomy, so the tree asserts only what is supported and the uncertainty
travels downstream instead of being converted into a pass/fail verdict.
`collapse_unsupported_bp.py` does this, preserving root-to-tip distances additively
and never touching a terminal branch (18 self-tests).

Collapsed fraction over all 180 trees:

| collapse line | internal branches removed |
|---|---|
| UFBoot ≥ 70 | 34% |
| UFBoot ≥ 80 | 41% |
| **UFBoot ≥ 95 (default)** | **58%** |

**That 58% is the honest description of how resolved these trees are**, and it is
far more informative than "22 of 30 units passed". Two small units (`s16_L1_3`,
`s4_L1_4`) collapse to near-stars at 95 — which is the correct representation of
8 and 7 genomes at this diversity, not a reason to delete them.

**4. Consequences for other conclusions.**

- **`s1_L1_9` is restored** (n=90, the largest casualty). The floor anchor is back
  in the accepted set — but note this does **not** re-establish the floor, which
  A.11x disqualified on independent grounds. It stays bracketed at (405, 1,268].
- **`s16_L1_3` is restored** — r/m 10.43, among the highest measured, with median
  UFBoot 43. A.11v read that row as the argument *for* the criterion. It is better
  read as the argument against: a unit with excellent recombination assignment and
  an unresolved tree should have its tree collapsed, not be deleted.
- **A.11v's underlying measurement stands.** Resolution is orthogonal to r/m
  (−0.010) and only weakly size-dependent (+0.171). It is genuine third-axis
  information and is still reported per unit — as a diagnostic, not a gate.

**5. THE PARTIAL CORRELATIONS (Tier 0.3), which A.11r asserted without testing.**
Over all 45 units — A.11r ran on 19:

| correlate | r | p |
|---|---|---|
| marginal r(log n, union) | **+0.800** | 4.3e-11 |
| marginal r(diversity, union) | +0.281 | 0.062 |
| **r(log n, diversity)** — the putative confounder | **−0.010** | 0.95 |
| **partial r(log n, union \| diversity)** | **+0.837** | 1.5e-12 |
| **partial r(diversity, union \| log n)** | **+0.482** | 0.00093 |

**A.11r survives, and is strengthened.** Size and diversity are uncorrelated in
this collection, so there was no confound to control for, and the size effect
*rises* to +0.837 with diversity held constant.

> **Updated to 46 units** after `s13_L1_1` was recovered (A.11ac): marginal
> +0.801, diversity +0.255, confounder −0.022, partial **+0.835**, diversity
> partial **+0.456** (p = 0.0017). Every conclusion is unchanged. The measurement
> set retains all 46 units *including the 9 withdrawn composites* — they are
> withdrawn from the ACCEPTED set but remain valid observations of how these
> statistics behave, and dropping them would narrow the size range that made the
> confound visible. **Accepted set (26 units) and measurement set (46 units) are
> different objects; do not conflate them.**

**But the test was still worth running, for a reason we did not anticipate.**
Diversity has a genuine independent effect of **+0.482** (p = 0.0009) — roughly
double its marginal +0.281, which was diluted by the much larger size effect.
A.11r read the marginal +0.26 as "diversity is **not** the driver" and treated it
as a non-factor. It is a real second driver. **A partial correlation can revise an
estimate upward as easily as explain it away**, which is the argument for running
it even when you are confident of the answer.

#### A.11z ★ THE MGE / HOTSPOT ALARM IS REFUTED — shared tract positioning is what chance predicts (2026-08-11, TIER 1.2)

**This closes the one open item that could have forced a re-run of every unit.**
Reproduce with `python3 mge_hotspot_audit_bp.py` (10 self-tests).

**The alarm.** Across the 8 units sharing the Viet Nam reference, 10-kb bins that
are recombinant in **all 8** numbered 54, bins recombinant in ≥80% of units
numbered 185 (46% of all recombinant bins), and **exactly one bin in 403 was
lineage-specific.** Read directly, that says tracts are being generated at fixed
reference coordinates — mobile elements, repeats, or mismapping — which would mean
MGEs inflate r/m in every unit and the acceptance criteria have been reading
artefact as health.

**Two defects in that reading, both fatal.**

1. **NO NULL.** Each unit individually flags **35–97%** of 10-kb bins as
   recombinant somewhere. When single units each mark most of the genome,
   near-total agreement between them is *arithmetic*. Against an independence
   null — P(all k units flag a bin) = Πpᵢ — the observed sharing is **1.2×**
   expected, not the order-of-magnitude excess the raw counts suggest.
2. **THE STATISTIC WAS NOT COMPARABLE ACROSS GROUPS.** "Recombinant in ≥80% of
   units" means ≥7 of 8 in one group and **all 4** of 4 in another. Comparing 46%
   against 3% and reading a lineage effect compared two different questions.

**Corrected test, with the lineage control the critique asked for.** Enrichment
over an independence null, evaluated at a matched k=4 for every group:

| reference group | k | lineages | kind | matched enrichment |
|---|---|---|---|---|
| Viet Nam | 8 | 2 | mostly-1-lineage | 1.1× |
| Ubon Ratchathani | 7 | **7** | **cross-lineage** | 0.9–1.1× |
| Hong Kong | 7 | **4** | **cross-lineage** | 1.1–1.2× |
| Thailand (GCF_000756125) | 4 | 2 | mostly-1-lineage | 1.1–1.5× |

Two of the four groups are genuinely cross-lineage — including one containing
seven distinct lineages — so this **is** the "different lineages sharing a
reference" test the plan specified, and it was available on disk at zero compute.

| | median matched enrichment (k=4) |
|---|---|
| cross-lineage — inheritance CANNOT explain sharing | **1.1×** |
| same / mostly-one-lineage — inheritance CAN | **1.1×** |

**Verdict: no re-run is indicated.** Shared positioning is within ~10% of chance,
and units that cannot share recombination ancestrally agree no more than chance
predicts.

**Stated conservatively, because this bounds rather than excludes.** Enrichment
rises as bins get finer — cross-lineage 1.1× at 10 kb, 1.3× at 1 kb, 1.4× at
500 bp — which is the signature of *localised* shared hotspots rather than none,
and one cross-lineage group reaches 1.9× at 500 bp on chr1. Same-lineage groups
run higher than cross-lineage at fine resolution (1.7× vs 1.4×), the direction
ancestry predicts. **The correct claim is that a fixed-coordinate artefact is
bounded at a small factor, not that it is absent.** Masking MGEs remains cheap
and standard and is still worth doing; what has changed is that it is no longer
a correction to results already reported.

**The transferable lesson, and it is the same one as §5.1.** "Only 1 bin in 403
is lineage-specific" is a **cumulative** statistic dressed as a rate. It was
alarming for exactly the reason union coverage was misleading: the quantity grows
with how much of the genome is flagged and with how many units are compared, so
it must be read against a null at matched size. We made this error twice, in two
different sections, four days apart.

#### A.11aa CALLABLE-FRACTION VARIANCE DOES NOT EXPLAIN THE r/m RESIDUE — and two incidental correlations that matter more (2026-08-11, TIER 1.4)

Reproduce with `python3 callable_variance_bp.py` (10 self-tests); per-unit values
in `callable_variance.tsv`.

**The hypothesis.** If genomes within a unit differ widely in how much of the
reference they actually call, the shared core is small and patchy and detection
could degrade for non-biological reasons. Measured on the full-length alignments
that entered Gubbins, across all 45 units:

| predictor of pooled r/m | r | p | controlling n and diversity |
|---|---|---|---|
| **sd of callable fraction** | **−0.183** | 0.23 | −0.188 |
| cv of callable fraction | −0.188 | 0.22 | −0.193 |
| mean callable fraction | +0.115 | 0.45 | +0.187 |
| worst genome's callable fraction | −0.007 | 0.96 | +0.139 |

**Not supported, and the direct check is worse for the hypothesis than the
regression.** The three named §9.4 units have **lower** callable-fraction
variance than the rest (0.0033 vs 0.0047) — the hypothesis predicts *higher*.
Their callable fractions are unremarkable (0.930–0.957 mean, 0.906–0.949 worst).

**This is the sixth candidate excluded.** The §9.4 residue stands unexplained,
and the remaining live hypothesis is A.11l/ν — recombination present but
undetectable because donors are too close — which needs ClonalFrameML
(**not installed**; Tier 1.3).

**TWO INCIDENTAL RESULTS FROM THE SAME RUN, both more consequential than the
test itself.** Both are over 45 units; earlier values were over 19.

**1. Pooled r/m is even more size-robust than claimed: r(log n, r/m) = +0.024
(p = 0.88).** A.11r measured +0.373 on 19 units. Over the full set the size
dependence is **essentially zero**. This materially strengthens the decision to
make r/m the sole acceptance gate (A.11y): the one statistic we threshold is the
one that does not track sample size, while the two we withdrew (union, support)
both do or depend on convention.

**2. r/m declines with diversity across the whole range: r = −0.470
(p = 0.0011).** A.11l proposed exactly this gradient and **withdrew it** as
resting on four non-monotone points. Over 45 units it is a clear, well-powered
correlation.

**Read this carefully — it is a reinstatement of the phenomenon, not of A.11l's
interpretation.** What is established is that r/m declines *continuously* with
diversity rather than falling off a cliff at a ceiling. What is **not**
established is where, or whether, a usable boundary sits on that continuum: a
smooth decline is precisely the shape that makes a threshold arbitrary, which is
the same problem A.11y found with the support gate. **The r/m ≥ 3.0 cutoff should
now be understood as a point on a continuum**, with its 2.57–3.38 bracket, and
not as a boundary between two regimes. Anything resting on a clean in-range /
above-ceiling dichotomy needs re-reading in that light.

#### A.11ab ★ THE LOW-ν HYPOTHESIS IS REFUTED — ν is a constant here, not a variable (2026-08-11, TIER 1.3)

ClonalFrameML 1.20 installed (conda env `cfml`); 12 runs (6 units × 2 replicons),
all exit 0. Reproduce with `python3 clonalframe_nu_bp.py --report`; raw output in
`TIER1_3_clonalframe.txt`, per-run products under `cfml/`.

**The hypothesis.** Gubbins reports r/m as one number conflating three separable
quantities: how *often* recombination happens (R/θ), how *long* tracts are (δ),
and how *divergent* imported DNA is (ν), with r/m ≈ R/θ × δ × ν. A unit could
show low r/m because it recombines with donors so close that imports introduce
almost no SNPs — real recombination, nearly invisible to any density-based
detector. That would have made the §9.4 residue biology rather than failure.

**Design.** Three suspects (`s1_L1_19`, `s3_L1_10`, `s1_L1_13`) against three
**diversity-matched** healthy controls. Matching was essential, not cosmetic:
r/m declines with diversity across the collection (−0.470, A.11aa), and all three
suspects sit high in the range, so controls chosen on healthy r/m alone would
have differed in diversity too. Controls bracket the suspects (ska 3,357 / 4,332
/ 4,400 against 3,956–4,088). **Starting trees were rebuilt uncorrected** — every
tree on disk is post-Gubbins, and seeding ClonalFrameML with a
recombination-corrected tree would bias every parameter it reports.

| | suspects | controls | ratio |
|---|---|---|---|
| R/θ (chr1 / chr2) | 1.203 / 1.123 | 1.310 / 1.257 | 0.92 / 0.89 |
| δ (chr1 / chr2) | 5,063 / 4,981 | 6,329 / 6,274 | 0.80 / 0.79 |
| **ν (chr1 / chr2)** | **0.00211 / 0.00222** | **0.00210 / 0.00222** | **1.00 / 1.00** |

**REFUTED, and not marginally.** Both replicons independently give a ν ratio of
**1.00**. The decisive framing is the variance decomposition:

- **Between units, within a replicon:** ν spans 0.00207–0.00213 on chr1 (2.9%)
  and 0.00222–0.00240 on chr2 (8.1%).
- **Between replicons, within a unit:** ν rises **+6.7% to +13.3%** from chr1 to
  chr2, consistently in all six units.

**ν varies more between replicons than between units.** It behaves as a constant
of the organism, not as a unit-level variable, and a quantity with an ≤8% spread
cannot explain a **4.5×** spread in Gubbins r/m (2.03 → 9.15). R/θ (0.89–0.92)
and δ (0.79–0.80) do not explain it either.

**The §9.4 residue therefore stands unexplained, with a seventh candidate
excluded.** Plan §1.5 called this "the single most publishable thing to come out
of the critique". It is not there. Recording it because a refuted best hypothesis
is worth more in the record than an untested one.

##### The unanticipated observation, recorded as a FLAG rather than a finding

ClonalFrameML does not reproduce Gubbins' ordering of the same six units:

| unit | role | Gubbins r/m | rank | CFML implied r/m | rank | ratio |
|---|---|---|---|---|---|---|
| `s3_L1_10` | suspect | 2.03 | **1** | **16.31** | **5** | 8.0× |
| `s1_L1_13` | suspect | 2.07 | 2 | 10.05 | 1 | 4.9× |
| `s1_L1_19` | suspect | 2.30 | 3 | 10.56 | 2 | 4.6× |
| `s2_L1_10` | control | 4.44 | 4 | 13.20 | 3 | 3.0× |
| `s2_L1_8` | control | 5.80 | 5 | 22.69 | 6 | 3.9× |
| `s3_L1_8` | control | 9.15 | 6 | 15.82 | 4 | 1.7× |

Pearson +0.489, Spearman **+0.314**, CFML/Gubbins ratio median 4.3× (1.7–8.0×).
Gubbins' lowest-r/m unit is ClonalFrameML's second-highest. Because pooled r/m is
now the **sole** acceptance gate (A.11y), a genuine ordering disagreement would
be a finding about the gate.

**It is not established, and three caveats apply — the first alone is
disqualifying for any strong claim:**

1. **n = 6.** A Spearman rho on six points has almost no power. **Settling this
   requires running the comparison across all 45 units**, which is now cheap: the
   tooling exists and each unit costs minutes.
2. **The two are not the same estimator.** Gubbins takes an empirical SNP-count
   ratio against its own inferred clonal frame; ClonalFrameML forms R/θ × δ × ν
   under an explicit model. This explains the systematic ~4× offset — but an
   offset cannot **reorder** units, and order is what a threshold acts on.
3. **A competing explanation fits equally well.** If the suspects are bridged
   mixtures, the two tools may absorb population structure differently, making
   the disagreement informative about **the units** rather than the gate.

**Note also that every CFML implied r/m (10.1–22.7) sits above the published
species-wide anchor of ~7.2, while Gubbins' controls (4.4–9.2) bracket it.**
Consistent with §5.2's warning: literature anchors are useful for spotting
order-of-magnitude errors and useless as acceptance thresholds — and which side
of the anchor you land on is partly a choice of tool.

**RECOMMENDED NEXT ACTION, and it now outranks Tier 2.** Run ClonalFrameML across
all 45 units and correlate against Gubbins pooled r/m. If the rank disagreement
survives at n = 45, the sole acceptance criterion is tool-dependent and the
triage needs re-deriving. If it does not survive, this is noise on six points and
the matter closes. Either way it is hours of compute against a criterion
everything else now rests on.

#### A.11aj ★★ SENSITIVITY ANSWERED — spike-in on REAL data; 91% recovery at our nu (2026-08-12)

**The question A.11ab opened and the nu-slice could not answer.** nu was measured
at 0.0021-0.0024 in every unit; nobody knew whether that sits inside Gubbins'
detection regime or near its edge. Answered by implanting recombination of KNOWN
divergence into a REAL alignment -- no simulator involved.

**Design.** Base = `s13_L1_1` `close__ska_map__chr1` (31 genomes, 3.97 Mbp, real
GC, real N-masking, real phylogeny). 12 genomes x 2 implants x 5,000 bp per
replicate. The donor is EXACT by construction: the recipient's own sequence over
the tract, each callable site mutated with probability nu, so imported DNA is
exactly nu-divergent. Scored against an UNSPIKED CONTROL of the same alignment;
an implant counts as recovered only if a Gubbins block covers >=50% of it FOR
THAT TAXON in the spiked run and not in the control (the GFF carries `taxa=`).
Implants landing on pre-existing detections are excluded from the denominator.

| nu | SNPs/tract | recovery |
|---|---|---|
| 0.0005 | 2.4 | **20%** |
| 0.001 | 4.2 | **40%** |
| **0.002 (ours)** | **9.0** | **91%** |
| 0.005 | 25.0 | **100%** |
| 0.01 | 45.0 | **90%** |

**COMPLETE: 15 of 15 runs, 3 replicates per nu, ZERO failures.**

**READING.** Detection is comfortable
at our operating point: **our r/m values are NOT systematically deflated by donor
similarity.** The gradient 20% -> 40% -> 91% across 2.4 -> 4.2 -> 9.0 SNPs per
tract is a real detectability limit -- roughly **5-10 SNPs in a 5 kb tract** is
where Gubbins becomes reliable -- and our units sit just above it. This is the
cliff the nu-slice was built to find and could not, because of the working-
directory defect in A.11ai.

**The curve rises steeply and then PLATEAUS at ~90-100%** (91%, 100%, 90% at
nu = 0.002, 0.005, 0.01). It does NOT saturate cleanly at 100%: the top cell came
in at 90%, and the 100% at nu = 0.005 sits between two 90% values. On 3
replicates and ~19-21 scorable implants per cell, 90% vs 100% is roughly two
implants and well within sampling noise, so the honest statement is a **plateau
near 90-100%**, not a ceiling at 100%.

*(An earlier version of this entry claimed clean saturation at 100%. That was
written when nu = 0.005 was the highest resolved cell and nu = 0.01 had not
landed — the fifth time in this session a conclusion was drawn from an
incomplete final cell. Corrected on the full grid.)*

What the plateau does still establish is that the scoring rule is not spuriously
generous: a lenient criterion would have inflated the low-nu cells too, and those
sit at 20% and 40%.

**CAVEATS.** One base unit, one replicon. Implants are terminal-branch imports
(single recipient), not clade-level. The 0.002 row is one replicate at the time
of writing. Tree builder is IQ-TREE (equivalence measured: median 2.3% r/m
deviation, 0 of 12 verdict changes).

**TO RESUME:** `python3 spikein_sensitivity_bp.py --report`; re-run with
`--run --replicates 3`. Outputs in `spikein/`, control preserved in
`spikein/control` (494 s, reusable).

#### A.11ai ⚠ WITHDRAWN AND REWRITTEN — the nu-slice "failure" was MY HARNESS, not the simulator (2026-08-12)

> **THE ORIGINAL VERSION OF THIS ENTRY WAS WRONG AND IS RETAINED BELOW ONLY AS
> THE RECORD OF WHAT WAS CONCLUDED AND WHY IT DID NOT SURVIVE.** It reported the
> nu-slice as a negative result and diagnosed "simulated data does not resemble
> real data". Both the result and the diagnosis were artefacts of a defect in the
> runner I wrote.

**THE ACTUAL CAUSE: CONCURRENT GUBBINS RUNS SHARING A WORKING DIRECTORY.**
Gubbins writes intermediates -- `<basename>.start`, `<basename>.phylip`,
`<basename>.snp_sites.aln` -- into the **current working directory**, NOT into
`--prefix`. All 80 nu-slice replicates used the alignment basename `aln.fa` and
ran concurrently from the project root, so they overwrote and deleted one
another's intermediates. The symptom is
`FileNotFoundError: '<basename>.start'` in one run because another finished and
cleaned up.

**THE EVIDENCE IS A CLEAN NATURAL EXPERIMENT ACROSS FIVE RUNS:**

| run | alignment basename | concurrency | outcome |
|---|---|---|---|
| nu-slice, 80 replicates | all `aln.fa` | 12 | ~60-70% failed, **independent of nu** |
| single manual test in `/tmp` | isolated dir | 1 | **succeeded** |
| spike-in v1/v2, 15 replicates | all `spiked.fa` | 4 | 0-1 of 15 succeeded |
| unspiked control | unique real filename | shared | **succeeded, both builders** |
| tree-builder equivalence, 12 runs | distinct real paths | 3 | **12/12 succeeded** |

**AND THE DIRECT TEST.** Four nu-slice replicates that FAILED in the original run
were re-run from their original `sim.fa`, with nothing changed except an isolated
working directory: **4 of 4 succeeded.** Spike-in nu=0.0005 went from 0/3 (RAxML)
and 1/3 (IQ-TREE) to **3/3** on the same fix.

*Caveat, because the two conditions are not identical in every respect:* the
re-checks ran at 4-way concurrency against the original 12, so contention is not
fully excluded as a contributing factor. The filename mechanism is directly
observed in the error messages, so it is the cause; contention may modulate how
often the collision bites.

**WHAT THIS RETRACTS.**

1. **The nu-slice negative result is withdrawn.** The 18-of-80 completion rate
   and the absence of any nu relationship (r = +0.389, p = 0.34) measured my
   runner, not Gubbins' sensitivity. The experiment was recoverable throughout.
2. **"Simulated data does not resemble real data" is withdrawn.** The identical
   failure occurs on REAL alignments the moment two runs share a basename.
3. **The masking-depletion hypothesis is withdrawn.** Proposed when the same
   error appeared on spiked real data; also wrong.
4. **The nu-independence of the failure rate was the clue and I misread it
   three times.** A failure mode that is flat across a 250-fold range of the
   variable under study is almost never about that variable. I instead read it
   as evidence for a tooling/biology story twice over.

**WHAT STANDS.** The tree-builder equivalence result (A.11ae context, 12/12,
median 2.3% r/m deviation, 0 verdict changes) is unaffected -- those runs used
distinct alignment paths and never collided. The Tier 2 null (A.11ag) is
unaffected: its replicates were named `rep000.fa` .. within per-unit
directories, and it ran to completion — **1,519 replicates across 62
unit-replicons** on the finished run (the "1,302 of ~1,302" originally written
here was a mid-run count; see the addendum to A.11ag).

**THE TRANSFERABLE LESSON, and it is a pipeline rule, not a curiosity.**
**Give every concurrent run of a tool its own working directory.** Do not rely on
`--prefix`, `--outdir` or equivalent to isolate a tool's temporary files; many
tools write scratch to CWD regardless. The failure is invisible in single-run
testing, appears only under concurrency, produces misleading errors that point at
the input rather than the collision, and — as here — can be mistaken for a
scientific result. Add it to the trap list beside T8.

**ADDENDUM 2026-08-12 (later same day) — the escape criterion above is stated
wrongly, and two runners were never actually fixed.**

The natural-experiment table credits the surviving runs to **"distinct real
paths"**. That is the wrong invariant. Scratch is written to CWD as
`<basename>.*`, so what protects a run is a distinct **basename**; two runs in
different directories whose alignments share a filename still collide. Stating it
as "paths" makes the pipeline rule sound satisfied by ordinary directory
hygiene, which it is not.

Re-auditing all five scripts that launch Gubbins found the `cd` present in
`nu_slice_bp.py`, `spikein_sensitivity_bp.py` and `null_simulation_bp.py`, and
**absent from the two that touch real data** — `treebuilder_equivalence_bp.py`
and the production runner `reference_sensitivity_bp.py`. The handoff's claim
that "all runners now `cd` into a per-run directory" was therefore false when
written. Both have now been fixed (`cd "{wd}"`, and a `( cd "${OUT}" && ... )`
subshell in production so the surrounding arm script keeps its own CWD;
`reference_sensitivity_bp.py selftest` passes, including its
"still propagates a Gubbins failure" assertion).

**Neither escape was by design.**

- *Tree-builder equivalence:* survived because its six units happened to borrow
  six different close references, giving 12 distinct basenames. `strain_12`
  shares `PHLS_112` with `s18_L1_1`/`s18_L1_2`, so extending `UNITS` would have
  collided; and `ARMS` is close-arms only, so adding the K96243 arms — the
  obvious extension of a reference-choice test — would have given all 12 runs
  the identical basename.
- *Production:* survived because the generated `run_all.sh` runs arms
  sequentially **within** a unit. That file nonetheless advises the opposite:
  *"Arms are independent; submit them in parallel if you have a scheduler."*
  Across the 184 production arms there are only **30 distinct basenames**, and
  `aln.full.NC_006350.1.fa` / `NC_006351.1.fa` are each shared by **46 arms** —
  every unit's K96243 arm. Running two units' `run_all.sh` concurrently, the
  natural way to process 42 units, would have collided.

No completed result is affected: the 12/12 equivalence runs and all 184
production arms did run clean. The point is that they were protected by
circumstance, and the record said otherwise.

**Physical residue, which is also how to detect this after the fact.** The
project root holds **298 orphaned `tmp*` directories totalling 29 GB** — Gubbins'
internal per-iteration RAxML scratch (`RAxML_bestTree.<tag>.iteration_N`,
`invariant_sites.<tag>.iteration_N.partition`), 296 of them dated 2026-08-12.
Gubbins removes these on a clean exit, so an accumulation of them **is** the
signature of runs dying mid-iteration. Counting orphaned scratch directories is
a cheap standing check for this failure mode.

---

**RETAINED FOR THE RECORD — the original, withdrawn entry:**


**Reported as a negative result because it is one.** 80 replicates (8 nu values x
10), paired design, IQ-TREE builder, calibrated parameters. **18 succeeded, 56
failed, 6 unresolved.** `TIER2B_nuslice_RESULT.txt`.

| nu | ok | fail | rate |
|---|---|---|---|
| 0.0002 | 2 | 6 | 75% |
| 0.0005 | 4 | 6 | 60% |
| 0.001 | 2 | 8 | 80% |
| **0.002 (ours)** | 1 | 8 | **88%** |
| 0.005 | 4 | 5 | 55% |
| 0.01 | 4 | 6 | 60% |
| 0.02 | 1 | 8 | 88% |
| **0.05** | **0** | **9** | **100%** |

**r(log nu, failure rate) = +0.389, p = 0.34.** No trend, and the sign is
POSITIVE — failures rise slightly with divergence. At nu = 0.05, **24x our
measured value**, where imports carry ~250 SNPs per 5 kb tract and detection
should be trivial, **every replicate failed.**

**Therefore the failures are NOT a detectability cliff.** They are a
simulation-to-pipeline incompatibility: Gubbins cannot reliably process SimBac
output at any divergence. Under its default RAxML builder it failed on 79 of 80;
under IQ-TREE it fails on ~70%. The residual differences across nu are noise on
9-10 replicates.

**WHAT WAS THEREFORE NOT LEARNED.** A.11ab measured nu at 0.0021-0.0024 in every
unit and could not say whether that sits comfortably inside Gubbins' detection
regime or near its edge. **That question is still open.** The Tier 2 null
(A.11ag) bounds FALSE POSITIVES at ~0; nothing in this project bounds
SENSITIVITY. Any claim that our r/m values are not systematically deflated by
donor similarity remains unsupported.

**FOUR WRONG READINGS OF THIS RUN, MINE, ALL FROM PARTIAL DATA.** Recorded
because the failure mode is procedural and worth not repeating:

| reported | actual |
|---|---|
| "1-3 of 10 failing, intermittent" | universal — 79 of 80 |
| "monotone decline 60/50/25%" | flat ~60% |
| "zero failures at our nu" | 88% |
| "cliff between 0.001 and 0.002" | no cliff at all |

Every one read a rate off a denominator that was still filling, and **every one
flattered the result.** The monitor counted a replicate as "attempted" the moment
its log file appeared, so slow outcomes were invisible. **"Attempted" without an
in-flight count is not a denominator.** The monitor was rebuilt to report
ok/fail/in-flight per cell and to print a rate ONLY when all 10 replicates in
that cell have resolved.

**WHAT WOULD ACTUALLY ANSWER THE SENSITIVITY QUESTION.** In rough order of cost:

1. **Make simulated data resemble real data.** The plausible cause is that
   SimBac output has uniform base composition, no missing data and no repeat
   structure, against 68% GC and heavily structured N patterns in ours. Post-
   processing simulated alignments to carry a real unit's base composition and N
   mask — as the Tier 2 null already does for missing data — is the cheapest
   test, and the null's success under exactly that treatment is direct evidence
   it may be sufficient.
2. **A different simulator.** msprime + a recombination-aware mutation layer, or
   SimBac output passed through the real variant-calling pipeline rather than
   fed to Gubbins directly.
3. **Spike-in on real data.** Take a real unit, implant tracts of known length
   and divergence from a known donor, and measure recovery. This keeps every
   real-data property intact and is the most faithful design, but it needs
   careful construction to avoid implanting detectable artefacts.

**Option 3 is the one I would recommend** — it removes the simulator from the
problem entirely, and the whole failure here was the simulator's output being
unlike real data.

#### A.11ah SIMULATION INFRASTRUCTURE — what broke, and the checks that caught it (2026-08-12, TIER 2B, IN PROGRESS)

**Status: the nu-slice is parameterised and gated on a tree-builder equivalence
test that is still running. Verdict pending. Recorded now because the
infrastructure findings stand regardless of the outcome.**

**1. GUBBINS' DEFAULT RAxML STEP FAILS ON SIMULATED DATA, UNIVERSALLY.**
`raxmlHPC-AVX2 -m ASC_GTRGAMMA --asc-corr=stamatakis` reports *"Unable to fit
model to data"* at iteration 1 on every SimBac alignment tested: **1 of 80
replicates produced output.** The same invocation works on all 46 real units. The
difference is in the data, not the tool — simulated alignments have uniform base
composition and no missing data, against 68% GC and structured N patterns in
real ones. `--tree-builder iqtree` completes on identical input.

**Two things make this hard to see.** Gubbins' own error handler is broken —
`print("Gubbins failed: " + e.output)` with `e.output = None` raises
`TypeError`, so the traceback shown is not the error that occurred. And the
replicates that avoid that path exit *silently*, producing neither an artefact
nor an error.

**2. THREE PARAMETERISATION ERRORS IN THE nu-SLICE, none of which stopped it
running.**

- **Saturation.** `R_EXTERNAL` was set to 5e-4 with a comment claiming it was
  calibrated. It was not. True recombinant union coverage came out at **99.9%**
  against 64-70% in our real units — a regime we do not occupy. Calibrated to
  **6e-5** (measured: 2e-5→22%, 5e-5→75%, 7e-5→66%).
- **Circular genome.** SimBac simulates a circular chromosome, so a tract
  crossing the origin is recorded with **start > end**. `union_fraction` swapped
  the endpoints, converting an 8 kb wrap-around tract into its 992 kb
  **complement**. Every coverage figure containing a wrap was inflated. **The
  selftest asserted the swapping behaviour**, so the bug was encoded as correct.
  Caught only by a **negative mean tract length** (−4,325) in calibration output.
- **Numeric taxon names.** SimBac names taxa `0`..`29`. Gubbins accepts the
  input, filters it, calls SNPs, then dies at iteration 1 with *"Sequences must
  all be the same length"* — an error about its own intermediate file. The input
  is perfectly rectangular (verified: 30 records, all 1,000,000). Renaming to
  `taxon_N` fixes it outright. **Handoff T8's rectangularity assert was never
  applied to simulated input**; had it been, it would have passed immediately and
  redirected the search from shape to names in seconds rather than hours.

**3. AN INDEPENDENT VALIDATION FELL OUT OF THE RECALIBRATION.** Mean simulated
tract length is **4,715-5,290 bp** against our measured ~5,000 — from a
parameter set from our data rather than fitted to it.

**THE PATTERN, AND IT IS THE SAME ONE AS §5.1 AND A.11z.** Every one of these
produced a plausible-looking result while running cleanly. Not one was caught by
an exception. They were caught by comparing a simulated quantity against a known
observed value: SNP counts against the real alignment (A.11ag), tract length and
union coverage against our measurements, artefact counts stage by stage. **Build
the "does the simulation reproduce the observed data?" check before trusting any
simulation output**, and treat a clean exit as no evidence at all.

#### A.11ag ★★ THE NULL IS RUN — every detection is real, and the threshold CANNOT be calibrated from it (2026-08-12, TIER 2)

> **ADDENDUM 2026-08-12 (later same day) — THE COUNTS BELOW ARE STALE; THE
> VERDICT IS NOT.** This entry was written while the null was still filling.
> On the completed run the figures are **1,519 replicates across 62
> unit-replicons** (not 1,302 / 54), **20 replicates with any false-positive
> block, 1.32%** (not 16 / 1.2%), and **59 of 62 unit-replicons clear p ≤ 0.05**
> (not 50 of 54). The **maximum null r/m is unchanged at 0.00668**, so the
> separation is unchanged: the lowest per-replicon observed value is
> `strain_13` chr2 at 2.85, i.e. **427× the null maximum**, and the largest is
> 14.92 at 2,234×. Every conclusion below stands; only the denominators move.
> Recomputed directly from the 1,519 per-replicate statistics files.
>
> **This is the sixth time in this project that a number was read off a
> denominator that was still filling** — the same shape as the four wrong
> readings catalogued in the withdrawn half of A.11ai and the incomplete final
> cell in A.11aj. The lesson has now cost more than any other single error class
> here: *do not record a count until the run that produces it has stopped.*
> Quote the completed figures, not these, in the paper.

**1,302 zero-recombination replicates across 54 unit-replicons.** Per unit: its
own tree, fitted model, alignment length, base composition and **per-genome
missing-data pattern applied verbatim**; seq-gen 1.3.5; then the identical
Gubbins invocation. Reproduce with `null_simulation_bp.py --report`;
`TIER2_null.txt`.

**WHAT THE NULL DELIVERS — and it is decisive.**

| | value |
|---|---|
| replicates producing **any** false-positive recombination | **16 of 1,302 (1.2%)**, one block each |
| **maximum null r/m ever observed** | **0.00668** |
| median / mean null r/m | 0.000 / 0.00004 |
| lowest accepted unit (`strain_13`, 2.89) vs null max | **433×** |
| the three §9.4 "failures" (2.03–2.30) vs null max | **304–344×** |

**PLAN §3's THIRD DECISIVE TEST IS EXCLUDED.** The plan listed "Tier 2's null
shows our accepted units are indistinguishable from no-recombination" as the
result that "would invalidate the whole analysis, and it should be run precisely
because it could." It is now excluded by a factor of **433**. Every accepted
unit's recombination is real and not an artefact of tree shape, alignment length,
base composition or missing-data structure.

**AND IT REFINES §9.4 — an eighth explanation excluded.** The three unexplained
low-r/m units exceed the null maximum by **304–344×**. They are therefore **not
under-detection in the sense of "no signal"**: there is abundant real
recombination in them, simply less of it relative to mutation. "Detection failed"
is eliminated as an account of the residue, which now points at biology or at
structure (A.11ae) rather than at the method.

**WHAT THE NULL DOES *NOT* DELIVER, and the reason is structural.**

Tier 2's stated purpose was to "replace every threshold with a per-unit p-value".
**That half is not delivered, and no amount of extra replicates would deliver
it.** The null's entire support is **[0, 0.00668]** while the acceptance boundary
is **3.0** — three orders of magnitude away, with no overlap. Consequently:

- Every unit with any detected recombination gets the same minimum p-value,
  1/(k+1) = **0.0385** at 25 replicates. 50 of 54 unit-replicons clear p ≤ 0.05,
  and the four that do not are limited by replicate count, not by signal.
- **A p-value cannot distinguish r/m 2.03 from r/m 12.89**, because both are
  hundreds of times above anything the null produces. The units we *reject* are
  as significant against the null as the ones we accept.

**The two questions were never the same.** The null answers *"is this more
recombination than chance?"* — yes, universally. The threshold asks *"how much
recombination does a unit need before its corrected tree is trustworthy
downstream?"* — a question about **sufficiency**, which no zero-recombination
null can address. A.11x concluded the floor could not be derived from the data;
this shows the ceiling-side threshold cannot be derived from a null either.

**CONSEQUENCE FOR REPORTING. The r/m ≥ 3.0 acceptance threshold remains a stated
convention with its 2.57–3.38 bracket, and must be reported as such.** What has
changed is that we can now say precisely what it is *not*: it is not a
detectability boundary. Everything on both sides of it is detected far beyond
chance. It is a usability judgement, and it should be described as one.

**This raises the value of the SimBac arm**, which simulates *with* recombination
at known parameters and can therefore speak to sensitivity — the axis this null
structurally cannot reach.

> **⚠ FIVE BUGS ON THE WAY TO THIS NULL, three of them silent.** Recorded because
> the null would have produced confident nonsense under any of them.
> **(1)** seq-gen rejects IQ-TREE's Newick (internal support labels), reporting
> the misleading "Closing bracket missing".
> **(2)** **Strict PHYLIP.** seq-gen's default `-op` truncates taxon names to 10
> characters and omits the separating space when the name fills the field
> (`GCA_963563ACGCCTG...`). A `split(None, 1)` then drops the line: **31 taxa in,
> 7 records out.** Truncation also collides names, breaking the mask join. Fixed
> with `-or`; `phy2fa` now validates the record count against the header and
> refuses duplicates.
> **(3)** The per-branch file is **TAB-separated despite its `.csv` extension**,
> and the columns are `Number of SNPs ...`, not `Num of SNPs ...`. Both wrong
> gave `inside = outside = 0` → `r/m = nan` for every replicate, which the report
> then discarded as "incomplete" — a null that yields no data rather than an
> error.
> **(4) and (5)** Two *confident wrong diagnoses of my own*: exponent notation in
> branch lengths, and `-i` double-counting invariable sites. Both were
> plausible, both were wrong, and both were settled only by a **controlled test
> against a known answer** — two taxa, branch length 0.001, 1 Mbp, expected 2,000
> differences, observed 1,972. seq-gen had been correct throughout.
>
> **The design-level lesson: the SNP-count validation is what caught the real
> bug.** Without it the run would have completed cleanly on 7 of 31 genomes and
> every unit would have looked overwhelmingly significant. Build the "does the
> simulation reproduce the observed data?" check *before* trusting any null.

#### A.11af ★ THE CONSTANT-SITE LIMITATION IS CLOSED — and the naive bound was union coverage in disguise (2026-08-12, TIER 1.1)

Reproduce with `constant_sites_sensitivity_bp.py --report`;
`TIER1_1_constant_sites.txt`. 62 unit-replicons, 124 IQ-TREE runs, 0 failures.

**The limitation** (methods handoff §2): constant-site counts are taken from the
alignment *as it entered* Gubbins, so they include constant positions inside
masked recombinant tracts. It was declared as unavoidable. `mask_gubbins_aln.py`
is installed, so it is measurable instead.

**Result — the choice is immaterial:**

| | median | range |
|---|---|---|
| constant sites removed by per-taxon masking | **0.0%** | −0.5% to +1.1% |
| total tree length ratio (masked / permissive) | **1.001** | 0.994–1.011 |
| per-branch correlation, matched on splits | **1.0000** | min 0.9988 |

**Both ends of the bracket agree to within 1.1%.** The limitation is CLOSED for
topological and relative-branch use. Report the permissive count with the
bracket; it does not need to be carried as an open caveat.

Note the sign: the drop is sometimes **negative** — masking a recombinant taxon
to N converts columns that were variable *only because of that taxon* into
constant ones, partly offsetting the loss.

> **⚠ TWO ERRORS ON THE WAY TO THIS, both mine, both instructive.**
>
> **(1) The bound was union coverage in disguise.** The first implementation
> excluded every column recombinant on **any** branch, rather than masking
> per-taxon as the plan specified. Measured against that bound the limitation
> looked *material*: median tree-length ratio 1.89×, up to **105×**. But
> r(union coverage, fraction of constant sites removed) = **+0.997** (p = 1e-70)
> and r(log n, same) = +0.842 — because "exclude every column recombinant on ≥1
> branch" **is the definition of union coverage**. The bound reproduced a
> cumulative statistic (§5.1, A.11r) and inherited its size confound entire. On a
> 155-genome unit at 98% union it stripped 99.2% of constant sites.
> **This is the third time a cumulative statistic has produced a plausible wrong
> answer in this project** — union coverage itself, the MGE shared-bin alarm
> (A.11z), and now this. Recombination is a property of a BRANCH, not of a
> column, and any bound that forgets it measures sample size.
>
> **(2) The per-branch comparison was invalid.** Branch lengths were correlated
> as *positional lists* from two independently-estimated trees, which is only
> valid if both emit branches in the same order — IQ-TREE need not. It produced
> correlations near **zero** on three units, which was nearly reported as "the
> constant-site choice changes tree shape". Branches are now keyed by the
> **split** they induce (canonicalised against the complement, so an unrooted
> edge read from either side maps to one key). Corrected minimum correlation:
> **0.9988**. The apparent finding was entirely an artefact of the comparison.

**AN INDEPENDENT VALIDATION OF THE POLYTOMY DECISION, which fell out of this.**
Topology agreement between the two runs (identical input, only `-fconst`
differing) is median 100% but as low as 69%. That variation is not caused by
`-fconst` — it cannot change topology — it is IQ-TREE's tree search landing
differently where the data barely constrain it. And it tracks resolution:

| | arms | mean median-UFBoot |
|---|---|---|
| ≥99% split agreement | 40 | **85.1** |
| <99% | 22 | **78.8** |

**r(split agreement, median UFBoot) = +0.470, p = 0.00012.** The units whose
topology wobbles between runs of the *same data* are the poorly-supported ones —
`s3_L1_6` (UFBoot 34.5, 69% agreement), `s1_L1_9` chr2 (50.0, 71.8%). That is
direct evidence for A.11y's remedy: those branches should be **collapsed into
polytomies**, because they are not merely unsupported, they are not reproducible.
Gating the units away would have discarded them; collapsing represents them
honestly.

#### A.11ae ★ THE GATE IS NOT TOOL-DEPENDENT — the Gubbins/ClonalFrameML disagreement is STRUCTURE, and it vindicates pooled r/m (2026-08-11, TIER 1.3 EXTENDED)

**A.11ab raised this as a flag on 6 units and said it could only be settled at
scale. Settled: ClonalFrameML run on all 46 units × 2 replicons (92 runs, zero
errors, ~2h35m). Reproduce with `clonalframe_nu_bp.py --report --all`;
`TIER1_3_clonalframe_all.txt`.**

**The disagreement is real and survives full power:**

| | value |
|---|---|
| Pearson r(Gubbins r/m, CFML implied r/m) | **+0.345** (p = 0.019, n = 46) |
| Spearman rho | **+0.297** (p = 0.045) |
| CFML/Gubbins ratio | median **2.3×**, range 1.1–349.5× |
| top-30 overlap (threshold-free) | **22 of 30 — 8 units change verdict** |

**BUT THE DISAGREEING UNITS ARE NOT A RANDOM SUBSET.** Comparing the eight units
each tool accepts and the other rejects, on `gap/mean` — the structure statistic:

| | median gap/mean | mean | max | exceed the >1.0 mixture line |
|---|---|---|---|---|
| accepted by **Gubbins** only | 0.176 | **0.168** | 0.378 | **0 of 8** |
| accepted by **CFML** only | 0.760 | **1.334** | 3.937 | **3 of 8** |

**Mann–Whitney p = 0.0003; a 7.9× difference in mean.** The units ClonalFrameML
accepts and Gubbins rejects are systematically the structurally heterogeneous
ones — including `strain_8` (gap/mean 2.695), `s1_L1_11` (3.937) and four of the
nine withdrawn composites (A.11ac).

**MECHANISM.** Gubbins infers a clonal frame iteratively and masks against it; in
a bridged unit that frame is polluted, SNPs fall outside the detected tracts, and
pooled r/m collapses. ClonalFrameML fits a **homogeneous** model on a fixed tree,
so deep divergence between two sub-lineages reads as frequent divergent imports —
high R/θ, high implied r/m. `s1_L1_11` is the extreme: Gubbins r/m **0.04** with
union 0.4% (total under-detection), CFML implied r/m **14.85** — a 349× ratio on
a unit whose gap/mean of 3.937 says it is a mixture, not a population.

**CONSEQUENCE, and it is the opposite of the worry that prompted the test.**

**The gate survives, and is vindicated.** Gubbins' low r/m on a structured unit is
*desirable* behaviour. Pooled r/m is doing **double duty** — a recombination
statistic *and* a structure detector — which is precisely why it works as the
post-hoc safety net for units that could not be modality-screened (§0's
"bridged clusters give r/m 0.94–1.49"). Substituting ClonalFrameML would **lose**
that: CFML will happily accept a mixture.

**But the interpretation sharpens, and this changes what a flag means.** A low
pooled r/m means **"re-examine for structure"**, not "recombination is low". Do
not read it as a pure recombination-intensity measure. This also explains
A.11aa's r(diversity, r/m) = −0.470 more economically than a smooth biological
gradient would: higher-diversity units are likelier to contain structure, and r/m
responds to structure.

**IMPLICATION FOR TIER 2, and it is a design change.** The planned null simulates
**one tree, no recombination, no structure**. It can therefore calibrate only
*one* of pooled r/m's two jobs. A p-value from that null answers "is this more
recombination than chance?" and says nothing about the structure-detection role
that is doing much of the work at the low end. **Calibrate against Gubbins alone
— not both estimators**, since CFML is demonstrably absorbing structure as
recombination and calibrating against it would import that behaviour. State
explicitly that the null covers the recombination role only.

#### A.11ac ★ THE PARTITION IS NOW COMPLETE — and the PopPUNK-strain block was not merely unscreened, it was WRONG (2026-08-11)

**The provenance gap, found by tracing rather than by assuming.** The analysable
set was built from 14 sub-partitioned strains plus 9 whole strains. The 9 were
admitted because sub-partitioning **never reached them** — not for any positive
reason. fastbaps has now been run on all 42 strains with ≥6 members (196 jobs,
zero errors), closing the gating item N1 that had been open since the probe.

**The chain, stated once, with numbers:**

| step | result |
|---|---|
| collection | 2,802 genomes |
| PopPUNK refined | 271 strains |
| strains with ≥6 members | 42 strains / 2,430 genomes |
| **strains with <6 members** | **229 strains / 372 genomes — never eligible for anything** |
| fastbaps L1 previously run on | 14 strains / 2,006 genomes (71.6%) |
| **fastbaps L1 gap, now closed** | **28 strains / 424 genomes** |

**What sub-partitioning the 28 recovered: almost nothing.** 100 new L1
sub-clusters, **median size 2**, and **61% singletons or pairs** — the same
shattering documented for L3 on the large strains (A.11b). Only 16 have n ≥ 6,
covering 263 of 424 genomes. Measured against the operating range:

| | count |
|---|---|
| in range **and** unimodal | **1** (`s13_L1_1`) |
| in range but n too small to screen | 2 |
| **out of the analysable range** | **11** |

The out-of-range means are 55, 94, 112, 174, 240, 405, 450, 574, 846, 873, 1,208
— overwhelmingly **below** the 1,270 floor.

**THE DIAGNOSTIC FINDING, and it condemns the strain block retrospectively.**
Compare each whole strain against its own dominant sub-cluster:

| whole strain | measured ska | its core sub-cluster |
|---|---|---|
| `strain_8` | 1,265 | **55** (n=36), gap/mean **8.697** |
| `strain_17` | 3,252 | 846 (n=7), 112 (n=8) |
| `strain_12` | 3,210 | 873 (n=25) |
| `strain_13` | 2,634 | **1,719 (n=31)** |

**The whole-strain diversity that placed these inside the operating range was
manufactured by mixture structure, not by within-lineage divergence.** Split the
structure away and what remains is clonal. `strain_8` — which sat at ska 1,265,
right at the floor, and was one of the observations A.11x had to disqualify — is
a 36-genome clonal expansion at **55 mean SNPs** plus outliers, with a gap/mean of
8.697, three times the highest value previously recorded. It was never a unit.

This reproduces `s1_L1_27`'s pattern ("its 2,378 was manufactured by 4 outliers;
the 33-genome core measures 485") in five further units. **Apparent diversity in
a bridged unit is a property of the bridging.**

**`s13_L1_1` — the one recovery, and it validates the whole diagnosis.** Run
end-to-end through the production pipeline (4 arms, 0 failures):

| | n | union | pooled r/m | tract |
|---|---|---|---|---|
| `strain_13` (whole) | 36 | 72.1% | **2.89** — RM-MARGINAL | 5,224 |
| **`s13_L1_1` (core)** | **31** | 64.2 / 69.6% | **12.89** | 5,002 / 6,196 |

**Removing 5 genomes raised pooled r/m 4.5×**, from barely-usable to the top of
the study. Subdivision repairs r/m when a genuine in-range core exists (A.11n
saw 2.57 → 4.94; this is 2.89 → 12.89). It fails for the other 8 strains because
their cores fall **below the floor**, not because subdivision does not work.

**Coverage must be restated, and it goes DOWN:**

| reading | units | genomes | % |
|---|---|---|---|
| as previously reported | 30 | 933 | 33.3% |
| minus the 5 composite strain units | 25 | 822 | 29.3% |
| **plus `s13_L1_1` (measured, passes)** | **26** | **853** | **30.4%** |

**And the denominator itself is misleading.** 2,802 includes 372 genomes in
strains too small to partition at all. Against the 2,430 genomes that were ever
eligible, the honest figure is **853 / 2,430 = 35.1%**. Report both, and never
quote a coverage percentage without saying which denominator it uses — the
difference between 30.4% and 35.1% is entirely a choice about what counts as
having been attempted.

**A COUPLING WORTH STATING.** The strains left out of sub-partitioning were left
out because they are small; small strains split into fragments below the
analysable floor. The units that were never processed were, in the main, the
units that could not have survived processing. That is reassuring for the
existing results and is **not** an argument for having skipped them — it could
only be known by doing it, and doing it also produced `s13_L1_1`.

#### A.11ad METADATA AND SUBSAMPLING — clonal groups are moderately, not overwhelmingly, study-driven (2026-08-11)

Reproduce with `python3 pseudoreplication_bp.py`; output in
`PSEUDOREP_2026-08-11.txt`.

**Question.** Should the collection be subsampled — using metadata, the Mash
matrix or the PopPUNK strains — *before* clustering?

**Measured, over 12 clonal groups (mean pairwise < 1,270) against 37 in-range
units:**

| | clonal | in range | gap |
|---|---|---|---|
| mean top-BioProject share | **63%** | 49% | +14 pts |
| mean top-year share | **57%** | 42% | +14 pts |
| mean top-subregion share | **59%** | 39% | +20 pts |
| mean distinct BioProjects | 3.3 | 4.8 | |

All three axes agree in direction. The typical clonal group draws about
two-thirds of its genomes from one study, in one place, in one year — that is
substantial pseudo-replication. But a third to a half of each group is genuinely
multi-study, so these are **not** pure sequencing artefacts, and collapsing them
entirely would discard real local-clone signal.

> **⚠ TWO ERRORS IN THIS ANALYSIS, both caught and both instructive.**
> **(1) Wrong columns, silently.** The first run used metadata column 11 for
> BioProject — that is the **BioSample** accession, which is unique per genome,
> so every concentration measure came out at ≈1/n and the analysis appeared to
> show clonal groups were *not* study-driven. Column 13 was read as the date; it
> is the submitter, so no year ever parsed and that row was silently `nan`. The
> table looked entirely plausible. `assert_columns()` now verifies that each
> index *contains what it should* (BioProjects start with PRJ, dates parse to a
> year) and the script refuses to run otherwise. This is trap 12's lesson again:
> **a positional index into a wide TSV is exactly the thing that is wrong without
> complaining.**
> **(2) A round-number verdict.** The script called the result on whether the gap
> exceeded 15 points. It was 14, so it printed "not markedly" and reversed the
> conclusion on an arbitrary cutoff — the identical error to the UFBoot gate
> (A.11y) and the 5e-06 slope cutoff (A.11e), committed while documenting them.
> It now reports the gradient and no verdict.

---

## Appendix B: what changed against `SNP_STRATEGY_REVIEW_2026-08.md`

The original review's three headline conclusions survive in substance. What changed is their strength and their consequences.

| Original review said | Now |
|---|---|
| "Your biggest problem is sampling" | **Unchanged and much stronger** — it is now an arithmetic argument against a burden model, not an observation about proportions. |
| "Build on the corrected tree, not the masked alignment" | **Upgraded from argument to demonstration.** Didelot & Parkhill's simulation had *no* site unaffected by recombination on some branch, so the masked alignment would contain zero sites while the clonal genealogy stayed usable. At r/m = 7.2 with 78% of K96243 ever recombined, that is this organism's regime. |
| "The graft has no published precedent" | **Superseded.** PopPIPE grafts; ARETE and BigBacter cluster-then-correct at scale and stop before grafting; COG-UK grafts at SARS-CoV-2 scale without recombination. The claim narrows to **the merge, under recombination** — which is stronger, because it is defensible. |
| §3 step 5: date-randomisation validates temporal signal | **Wrong for this data structure.** The test is anticonservative where temporal and genetic structure are confounded, and this collection computes to 7.1 expected substitutions across the window — Murray's boundary. Use BETS. |
| §5 rec. 7: "run date-randomisation first and be prepared for the answer to be no" | **"Run BETS, and expect the answer to be no."** |
| "Compare your partition against Wu's 10 clusters" | **Close to meaningless** — Wu's ten were imposed by `fcluster(t=10)`, not inferred. Compare against Chewapreecha's 19 and against PopPUNK/fastbaps on your own data. |
| "61–76 clusters may be too many" | **Framing inverted.** Seng's PopPUNK gave 101 lineages from 1,391 genomes. Yours is *coarser* than the in-species precedent. |
| r/m and the 78% figure "unconfirmed" | **Both verified.** r/m = 7.2 genome-wide (Nandi 2015), 78% of K96243 ever recombined. Keep distinct from Pearson 2009's seven-locus MLST ratio. |
| Verticall "worth evaluating on the full collection" | **Per cluster only, distance workflow only.** O(n²), timed out at 4,857 genomes; the alignment workflow dated PMEN1's root to 1701. |

---
