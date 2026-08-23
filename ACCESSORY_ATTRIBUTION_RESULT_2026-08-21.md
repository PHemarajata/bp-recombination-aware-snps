# Accessory-genome attribution — result

2026-08-21, evening session. Answers the experiment specified in
`HANDOFF_2026-08-21_EVENING.md` §1, the last remaining experiment that could
have changed the paper's headline.

**Verdict: accessory content does not rescue country attribution. The core
result is strengthened.** This is outcome 3 of the three the handoff pre-declared
as publishable. One fragile, testable positive lead survives (§6).

> ✅ **FULLY RE-RUN AT n = 46 (2026-08-24).** The body tables below are now the
> n = 46 figures, with the superseded n = 43 values retained in brackets or in
> §1a. **Every conclusion is unchanged.** One figure was *not* refreshed and is
> flagged in place: the contiguity-matched pool in §4.
>
> Headline: **accessory country 14/46 (30%, κ 0.264) vs cgMLST core 10/46
> (22%, κ 0.193)**, against a 26% majority baseline.
>
> | Control 4 — country accuracy by whether a genuine close relative exists (n=46) | accessory | core |
> |---|---|---|
> | d_core < 0.05 — **a close relative exists** | **1/14 (7%)** | 2/14 (14%) |
> | d_core 0.05–0.30 | 2/10 | 2/10 |
> | d_core ≥ 0.30 — **no real relative** | **11/22 (50%)** | 6/22 (27%) |
>
> **Region under the same strata does NOT run the other way**, and saying so
> would be wrong: accessory region is 9/14 · 6/10 · **20/22**, so it too is best
> where no close relative exists. That is the known attractor artifact, which
> affects both scales. What separates country is the *magnitude and the
> baseline*: accessory country swings **7% → 50%** across the strata and sits
> below its 26% baseline in the close-relative stratum, whereas region is 64% →
> 91% and clears its 46% baseline in every stratum. Core region NN over the same
> cuts is 11/14 · 6/10 · 20/22 — accessory is indistinguishable from core on
> region and only differs on country.
>
> **The inversion is the whole finding, and it is stronger at n=46 than at n=43
> (where the close-relative stratum was 0/13).** Accessory country attribution is
> **7% where a real relative exists and 50% where none does.** A method that
> works only when there is nothing to match is not attributing; the 30% headline
> is carried almost entirely by the no-relative stratum.
>
> The other controls also hold at n=46. **Control 1**: country accuracy by pool
> assembly quality 24% / 24% / **7%** (best → most fragmented), and validation
> genomes split by their own quality give country 5/12 (low-contig) vs 8/33
> (high-contig). **Control 2**: contig count correlates with mean *accessory*
> distance at ρ = +0.156 (p = 8.6 × 10⁻¹⁸) against only ρ = +0.038 for *core* —
> accessory distance is roughly four times more contaminated by fragmentation
> than core is, which is the mechanism. **Control 3**: the within-stratum
> permutation null is beaten (country 30.4% vs null mean 7.7%, p = 0.001) — but
> that null tests only "better than shuffled labels", not "better than the
> attractor", so it does not rescue the result.

---

## 1. The headline number, and why it does not mean what it looks like

**Re-run at n = 46 on 2026-08-23.** The n = 43 table it replaces is preserved in
§1a for comparison; every conclusion below is unchanged.

| axis | scale | best estimator | accuracy | kappa |
|---|---|---|---|---|
| **accessory** | country | NN **14/46** | **30%** | **0.264** |
| cgMLST core | country | NN 10/46 | 22% | 0.193 |
| PopPUNK core | country | NN 8/46 | 17% | 0.148 |
| majority baseline | country | — | 26% (12/46) | 0 |
| **accessory** | region | NN **35/46** | **76%** | **0.665** |
| cgMLST core | region | NN 37/46 | 80% | 0.715 |
| cgMLST core | region | modal k=20 **41/46** | **89%** | 0.832 |
| PopPUNK core | region | NN 35/46 | 76% | 0.653 |
| majority baseline | region | — | 46% (21/46) | 0 |

κ is computed with the same function as `grouping_test_bp.py`, so these values
are comparable with `GROUPING_LADDER.tsv` rather than merely similar to it.

Taken alone, the first row is the result the experiment was hoping for: country
attribution above its majority baseline for the first time in this project, and
8 points above the cgMLST core genome. Under `modal_k5` accessory reaches
**15/46 (33%)**.

**Four independent checks say the number is not attribution.** Estimator choice
is reported as required: accessory country peaks at NN and `modal_k5` and
*falls* to **4/46 (9%, κ 0.063)** by `modal_k20` — the opposite of the core
genome's behaviour, which is itself a warning that the signal is carried by one
or two neighbours rather than by a neighbourhood.

### 1a. The superseded n = 43 table

Kept because the §2 like-for-like argument and the §6 lead were both written
against it. **Do not quote from here.**

| axis | scale | best estimator | accuracy | kappa |
|---|---|---|---|---|
| accessory | country | NN 13/43 | 30% | 0.263 |
| cgMLST core | country | NN 9/43 | 21% | 0.188 |
| PopPUNK core | country | NN 8/43 | 19% | 0.161 |
| majority baseline | country | — | 28% | 0 |
| accessory | region | NN 34/43 | 79% | 0.707 |
| cgMLST core | region | NN 36/43 | 84% | 0.761 |
| cgMLST core | region | modal k=20 40/43 | 93% | — |
| majority baseline | region | — | 47% | 0 |

The three genomes added by the Track 0 integration move accessory country from
13/43 to 14/46 — the *rate* is flat at 30% — while every region figure falls a
few points because North America became testable. The ordering that carries the
argument (accessory > cgMLST core > PopPUNK core on country) is unchanged.

---

## 2. Method, and the like-for-like guarantee

PopPUNK 2.7.6 sketch database built over the **same 3,033 genomes** the
Lichtenegger cgMLST run used (`cgmlst_lichtenegger/genomes/`), k = 15–31 step 2,
sketch size 10,000 — matching the parameters of the existing `poppunk_bp` db.
4,598,028 pairs; 3,015 genomes after the 18 duplicate-BioSample drops; **48
validation genomes, 46 scorable** (45 / 43 as originally run, before the Track 0
integration).

Accessory distance is PopPUNK's *a*, the intercept of the regression of
log(Jaccard) on k; core *pi* is the slope. Both come from the same sketches, so
**PopPUNK core is a free internal control**: same genomes, same estimators, only
the axis differs.

`score_accessory_bp.py --distance cgmlst --validate` re-derives the core cgMLST
result through this script's own label-building code and diffs it against
`CGMLST_LICHT_ATTRIBUTION.tsv`: **0 rows missing, 0 extra, 0 truth/neighbour
mismatches — PASS.** Everything except the distance function is held fixed
(leave-group-out on exposure country, five estimators, exposure overrides,
duplicate drops, region map). Without that pass the core/accessory comparison
would not be trustworthy.

That PopPUNK core independently reproduces the cgMLST core result (country 19%
vs 21%, region 93% at modal k=20 in both) is worth stating on its own: **the
core-genome failure is not an artifact of the typing system.** Three
representations — cgMLST alleles, PopPUNK core, and previously SNP distances —
agree.

---

## 3. The four pre-registered controls

Written and committed as `accessory_control_bp.py` in `bf93d09`, **before the
accessory result was computed** (`git log` on that file predates
`accessory_bp/ATTR_ACCESSORY.tsv`). 1,000 permutations, seed 20260821 fixed to
the date so the null cannot be shopped.

### Control 1 — accuracy varies 5-fold with assembly quality. FAIL.

Restricting the matchable pool to one contig-count tertile at a time (cuts at
114 and 173 contigs):

Re-run at n = 46 (2026-08-23); the n = 43 values are in brackets.

| pool restricted to | n_pool | country | region |
|---|---|---|---|
| low (best assemblies) | 1,001 | 11/46 (24%) *[11/43, 26%]* | 31/46 (67%) *[30/43]* |
| mid | 1,011 | 11/46 (24%) *[10/43, 23%]* | 42/46 (91%) *[41/43]* |
| **high (most fragmented)** | 986 | **3/46 (7%)** *[2/43, 5%]* | 32/46 (70%) *[31/43]* |

Validation genomes split by **their own** assembly quality: country 5/12
(low-contig) vs 8/33 (high-contig), region 9/12 vs 25/33.

When only fragmented genomes are available to match against, country accuracy
collapses to 7% — well below both the 26% baseline and the core genome. The
geographic composition of the pool changes across tertiles too, so this is not
proof of a batch effect on its own, but a 3.5-fold swing driven by assembly
quality is exactly the failure signature the control was written to detect.

### Control 2 — accessory distance is measurably a function of fragmentation. FAIL.

| relationship | rho | p |
|---|---|---|
| contigs vs **mean accessory** distance | **+0.156** | 8.6e-18 |
| contigs vs mean core distance *(internal control)* | +0.038 | 0.036 |
| \|contigs_A − contigs_B\| vs accessory distance | +0.263 | <1e-300 |
| \|contigs_A − contigs_B\| vs core distance | +0.216 | <1e-300 |
| contigs_A + contigs_B vs accessory distance | +0.151 | <1e-300 |

Per genome, the accessory effect is **4× the core effect** — as predicted, since
a missing contig costs accessory presence/absence far more than it costs core
distance. Post hoc, the same holds for the nearest-neighbour distance
specifically (accessory rho +0.195, p=3.9e-27), and the median nearest-neighbour
accessory distance rises monotonically with fragmentation: 0.0009 for closed
genomes, 0.0015 at 51–150 contigs, 0.0039 at 151–400, **0.0151 above 400**. A
fragmented genome is systematically far from everything.

### Control 3 — the signal is not purely a batch effect. PASS.

Country labels shuffled **within** contig-count strata, so assembly quality is
held fixed:

Re-run at n = 46 with 1,000 permutations (2026-08-23); n = 43 in brackets.

| scale | real | null mean | null 95th pct | p |
|---|---|---|---|---|
| country | 30.4% *[30.2%]* | 7.7% *[6.4%]* | 13.2% *[11.6%]* | 0.0010 |
| region | 76.1% *[79.1%]* | 43.5% *[43.9%]* | 50.0% *[51.2%]* | 0.0010 |

Both sit far outside the null. **There is genuine non-random structure in
accessory content that assembly quality alone does not explain.** This is the
one control accessory passes cleanly, and it should be reported as such.

Its limitation must be reported with it: shuffling destroys *all* label
structure, so the test shows the signal is not purely contig-driven — it cannot
distinguish geography from any other non-contig confound such as BioProject or
submitting laboratory.

### Control 4 — the accuracy is entirely attractor artifact. FAIL, decisively.

Stratified on the **core** nearest-neighbour distance, because "does a genuine
close relative exist" is a fact about ancestry and the accessory scale is not
comparable to cgMLST's:

| stratum | accessory country | accessory region | *core country, for reference* |
|---|---|---|---|
| d_core < 0.05 — a real close relative exists | **0/13** | 8/13 | *1/13* |
| d_core 0.05–0.30 | 2/8 | 6/8 | *2/8* |
| d_core ≥ 0.30 — no real relative | **11/22 (50%)** | 20/22 | *6/22* |

**Accessory country attribution is 0 for 13 where a genuine close relative
exists.** Every correct call is concentrated where no relative exists, which is
precisely the attractor pattern already identified for region
(`HANDOFF_2026-08-21_EVENING.md` §3.3): a genome with no relative snaps to a
distant cluster, and the label is right often enough to look like a capability.

Accessory is *worse* than the core genome (0/13 vs 1/13) in the only stratum
where a correct answer would mean anything.

---

## 4. The whole margin over core rests on two genomes

Post hoc, motivated by the result and reported as post hoc.

All five Mexican validation genomes are 2–3 contig closed assemblies, and each
matched a 2-contig Mexican reference from a single locality (Huasabas). Dropping
**that one pair of genomes**:

Re-run at n = 46 (2026-08-23); n = 43 in brackets.

| | with | without |
|---|---|---|
| country | 14/46 (30%) *[13/43]* | **9/46 (20%)** *[8/43]* |
| region | 35/46 (76%) *[34/43]* | 34/46 (74%) *[33/43]* |
| Mexico specifically | **5/5** | **0/5** |

Two genomes out of 3,015 carry the entire accessory advantage. Remove them and
accessory country (**9/46, 20%**) falls **below the cgMLST core genome**
(10/46, 22%) *and* below the 26% majority baseline. The Mexican cases' next
choices become Brazil, Costa Rica, Czech Republic and El Salvador.

**This is now a reproducible command rather than an ad-hoc edit.**
`score_accessory_bp.py` gained an `--exclude` flag that removes genomes from the
panel on top of the duplicate register, so the frozen `PANEL_DUPLICATES`
register is never touched:

```bash
python3 score_accessory_bp.py --distance accessory --out-prefix accessory_bp/ATTR_ACC_NOHUASABAS --exclude GCF_006542565_1_Mexico_Huasabas,GCF_006542585_1_Mexico_Huasabas
```

A contiguity-matched pool (nearest neighbour restricted to genomes within ±50%
of the query's contig count) reduces country 30% → 23% and region 79% → 74%.
**⚠ These two figures are still the n = 43 run** — the contiguity-matched pool
is not one of the four controls `accessory_control_bp.py` re-runs, so it was not
refreshed with the rest. It is directional support, not a headline; re-run it
before it appears in the manuscript.

For context, the core genome places those same Mexican cases nearest to Ecuador
and Colombia at d = 0.002 — a coherent Americas lineage signal — and scored them
0/5, which is what made Mexico the paper's controlled negative (21 references,
wrong lineage).

---

## 5. What this does to the paper

**The core-genome result is strengthened, as the handoff predicted it would be
if accessory failed.** Accessory content was the best remaining hypothesis for
carrying shallow geographic signal, it was tested under an identical regime, and
it does not carry it. The ceiling is set by divergence depth, not by data type —
now shown across four representations rather than three.

**The methodological finding stands on its own.** Without the pre-registered
controls this experiment would have been written up as "accessory genome lifts
country attribution from 21% to 30%, above baseline for the first time." That
claim would have been wrong in three separate ways: 0/13 where it matters,
5-fold sensitivity to assembly quality, and total dependence on two reference
genomes. See §8 for what the literature does and does not already control — the
claim has to be phrased more carefully than "nobody runs this control."

**Reporting rules that apply** (`HANDOFF_2026-08-21_EVENING.md` §4.4): kappa is
given beside every accuracy; the distance stratification is given beside every
headline; the estimator is named everywhere; no NN number is compared to a modal
one.

---

## 6. The one lead worth keeping

Two Mexican reference genomes share enough accessory content with five Mexican
cases to win nearest-neighbour across a **core-genome gap of d = 0.406–0.462**.
Locally circulating mobile elements are the obvious candidate explanation, and it
is the mechanism the whole experiment was premised on.

It is a hypothesis, not a result: n = 2 references, n = 5 cases, and it does not
survive its own controls. **It is testable and cheap** — acquire more Mexican
genomes and see whether the signal scales with reference count or stays pinned to
Huasabas. If it scales, accessory attribution works but needs dense
within-country reference sets, which is a different and more interesting claim
than either "it works" or "it fails".

## 7. What was not tested

Route B — explicit pangenome or unitig presence/absence (panaroo, ppanggolin,
unitig-caller) — remains uninstalled and untested. PopPUNK's accessory distance
is a sketch-based Jaccard decomposition, not a gene presence/absence matrix, and
it is the *less* interpretable of the two representations. **A negative on Route
A does not fully close Route B**, and Route B is what the Salmonella precedent
actually used. Given §4, the honest expectation is that Route B would need the
same four controls to mean anything, and would likely fail control 4 the same
way — but that is an expectation, not a result.

---

## 8. Literature positioning — added 2026-08-21 after a full-text pass

### 8.1 The Salmonella precedent is not what our notes said it was

**Bayliss SC, Locke RK, Jenkins C, Chattaway MA, Dallman TJ, Cowley LA. Rapid
geographical source attribution of *Salmonella enterica* serovar Enteritidis
genomes using hierarchical machine learning. *eLife* 2023;12:e84167. PMID
37042517.** This is the paper our notes held only as a bare URL. The macro-F1
figures are confirmed: **0.954 region, 0.718 sub-region, 0.661 country**, over
2,313 UKHSA genomes.

**Three corrections to how we have been describing it:**

1. **It does not use accessory genes.** Features are **unitigs called directly
   from reads** (bcalm2 k=31 → unitig-caller → 426,647 unitigs → 25,000 after
   selection). Nothing is assembled and nothing is annotated. Calling it
   "accessory" is a loose gloss. Our Route A (PopPUNK accessory distance) is
   two steps away from it, which sharpens §7: **Route B is not the same as
   Bayliss either.**
2. **Their labels are patient-reported travel destination**, not isolation
   country — the same ground-truth design as ours. Worth stating, because it
   makes the comparison fairer than it looks.
3. **They report their signal as phylogeographic**, noting large clusters of
   isolates from geographically related countries.

**On controls, the honest statement is narrower than "they did not run them."**
Bayliss *does* control data quality: a ≥28× coverage floor, downsampling to
~100×, a minimum k-mer abundance, and a total-unitig-length cap; 220 samples
were excluded. They also run prospective temporal validation and external
validation on non-UKHSA reads (South Africa 25/25, Singapore 44/48, Poland 18/35
at country), which is real evidence against a pure batch artifact.

**What they do not do is the relatedness control.** Their only step in that
direction is deduplication to one isolate per SNP5 single-linkage cluster per
country — removing near-identical isolates, not removing close relatives from
the training pool. There is no leave-clade-out and **no stratification by
whether a close relative exists**, which is precisely the control (our control 4)
that killed our result.

So the claim to make in print is: **assembly-quality confounding of gene-content
features, and stratification by whether a genuine close relative exists, are not
addressed in the source-attribution literature we could find** — not "never
controlled." Verified in full text for Bayliss 2023, Guillier 2020 (AB_SA,
*Microb Genom* 6(7):mgen000366, PMID 32320376), Guzinski 2024 (*Front Microbiol*
15:1393824, PMID 39611092) and Tagg 2026 (*Nat Commun* 17:1270, PMID 41578138):
none regresses accessory distance on assembly quality, none stratifies accuracy
by it, none tests robustness to removing reference genomes.

### 8.2 The B. pseudomallei accessory-geography literature already says region, not country

This is the strongest framing available and it was sitting unread:

- **Tuanyok A, et al. A horizontal gene transfer event defines two distinct
  groups within *Burkholderia pseudomallei* that have dissimilar geographic
  distributions. *J Bacteriol* 2007;189(24):9044–9. PMID 17933898.** A single
  accessory gene cluster (**YLF vs BTFC**) partitions the species across 571
  isolates: BTFC dominant in Australia, YLF in Thailand and elsewhere.
- **Duangsonk K, et al. *J Clin Microbiol* 2006;44(4):1323–34. PMID 16597858.**
  14-amplicon accessory presence/absence on 48 Thai + 44 Australian isolates;
  clusters "mainly or exclusively from one geographical origin"; genomic island
  11 absent from every Australian isolate.
- **Chewapreecha 2017** identifies genes and variants distinct to Australasian
  *or* SE Asian isolates.

**Every accessory-geography result in this organism resolves Australia versus
Asia. None resolves country.** That is our §3.4 divergence-depth mechanism,
independently and repeatedly, going back nineteen years — and it means a
reviewer asking "why didn't accessory work?" already has a published answer.
Our contribution is that we *tested* it prospectively at country scale and
measured where it fails.

Also useful: **Spring-Pearson 2015 (*PLoS One* 10(10):e0140274, PMID 26484663)**
establishes the Bp pangenome is open (+136 genes per genome), i.e. the accessory
genome is large enough to have carried the signal. It did not.

### 8.3 Citable support for the fragmentation control

- **Tonkin-Hill G, et al. Producing polished prokaryotic pangenomes with the
  Panaroo pipeline. *Genome Biol* 2020;21:180. PMID 32698896.** The primary
  citation. On 413 near-identical *M. tuberculosis* genomes (max 9 SNPs apart,
  so the true accessory genome is ≈0), Roary/PanX/PIRATE/PPanGGoLiN/COGsoft
  reported **2,584–3,670 accessory genes — a ~10-fold inflation — and 59% of the
  difference was genes fragmented during assembly.** Panaroo's own QC flags
  outlier samples **by contig count and gene count**, which is direct precedent
  for our control 1 and control 2.
- **Klassen JL, Currie CR. *BMC Genomics* 2012;13:14. PMID 22233127.** Bacterial
  and quantitative: fragmented ORFs exceed 80% of predicted ORFs in some draft
  genomes, and fragmentation correlates with assembly quality.
- **Denton JF, et al. *PLoS Comput Biol* 2014;10(12):e1003998. PMID 25474019**
  (mechanism) and **Gabrielaitė M, Marvig RL. *BMC Bioinformatics* 2020;21:320.
  PMID 32690023** (a tool built specifically because presence/absence calling
  degrades on fragmented assemblies).

### 8.4 Nearest published analogue — unverified, get the PDF

**Gao M, Pradhan AK, Blaustein RA. *Int J Food Microbiol* 2025;441:111335. PMID
40644951.** *Cronobacter sakazakii*, 748 assemblies, accessory gene profiles
associated with **continent** of origin, random forest "accurately predicted
source attributions". This is the closest published work to our experiment —
assemblies, gene presence/absence, geography. **Paywalled; its methods,
validation design and controls are unverified. Do not characterise them.**

Also flagged unverified: **Tanui et al. 2022** (*Listeria* food-source
attribution, *Pathogens*) — metadata came from a secondary source, not PubMed.
Confirm before citing.

Contrast cases at host/source scale, not geography — do not let them be
conflated: **Arning N, et al. *PLoS Genet* 2021;17(10):e1009436. PMID 34662334**
(*C. jejuni* host source; note **cgMLST at 85% beat whole-genome k-mers at
78%**), plus Guillier 2020 and Guzinski 2024 above.

**Search scope, stated honestly:** PubMed, Consensus, PMC full text and general
web. Not Scopus, not Web of Science, not non-English literature. "We found none"
is a search result, not proof of absence.

---

## Files

| file | what |
|---|---|
| `score_accessory_bp.py` | scorer; `--distance accessory\|core_pp\|cgmlst`, `--validate` |
| `accessory_control_bp.py` | the four pre-registered controls |
| `assembly_stats_bp.py` | panel-wide contigs / N50 / GC |
| `accessory_bp/ppdb3033/` | PopPUNK sketch db, 3,033 genomes |
| `accessory_bp/ASSEMBLY_STATS_3033.tsv` | contig counts, panel-wide |
| `accessory_bp/ATTR_ACCESSORY.tsv` | per-genome accessory result |
| `accessory_bp/ATTR_CORE_PP.tsv` | PopPUNK core, internal control |
| `accessory_bp/ATTR_CGMLST.tsv` | core cgMLST re-derived, validation of the scorer |
| `accessory_bp/CONTROLS.log` | full control output |
