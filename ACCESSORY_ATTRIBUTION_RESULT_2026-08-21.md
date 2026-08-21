# Accessory-genome attribution — result

2026-08-21, evening session. Answers the experiment specified in
`HANDOFF_2026-08-21_EVENING.md` §1, the last remaining experiment that could
have changed the paper's headline.

**Verdict: accessory content does not rescue country attribution. The core
result is strengthened.** This is outcome 3 of the three the handoff pre-declared
as publishable. One fragile, testable positive lead survives (§6).

---

## 1. The headline number, and why it does not mean what it looks like

| axis | scale | best estimator | accuracy | kappa |
|---|---|---|---|---|
| **accessory** | country | NN 13/43 | **30%** | **0.263** |
| cgMLST core | country | NN 9/43 | 21% | 0.188 |
| PopPUNK core | country | NN 8/43 | 19% | 0.161 |
| majority baseline | country | — | 28% | 0 |
| **accessory** | region | NN 34/43 | **79%** | **0.707** |
| cgMLST core | region | NN 36/43 | 84% | 0.761 |
| cgMLST core | region | modal k=20 40/43 | 93% | — |
| majority baseline | region | — | 47% | 0 |

Taken alone, the first row is the result the experiment was hoping for: country
attribution above its majority baseline for the first time in this project, and
9 points above the core genome. Under `modal_k5` accessory reaches 15/43 (35%).

**Four independent checks say the number is not attribution.** Estimator choice
is reported as required: accessory country peaks at NN and `modal_k5` and
*falls* to 4/43 by `modal_k20`, the opposite of the core genome's behaviour,
which is itself a warning that the signal is carried by one or two neighbours
rather than by a neighbourhood.

---

## 2. Method, and the like-for-like guarantee

PopPUNK 2.7.6 sketch database built over the **same 3,033 genomes** the
Lichtenegger cgMLST run used (`cgmlst_lichtenegger/genomes/`), k = 15–31 step 2,
sketch size 10,000 — matching the parameters of the existing `poppunk_bp` db.
4,598,028 pairs; 3,015 genomes after the 18 duplicate-BioSample drops; 45
validation genomes, 43 scorable.

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

| pool restricted to | n_pool | country | region |
|---|---|---|---|
| low (best assemblies) | 1,001 | 11/43 (26%) | 30/43 (70%) |
| mid | 1,011 | 10/43 (23%) | 41/43 (95%) |
| **high (most fragmented)** | 986 | **2/43 (5%)** | 31/43 (72%) |

When only fragmented genomes are available to match against, country accuracy
collapses to 5% — well below both the 28% baseline and the core genome. The
geographic composition of the pool changes across tertiles too, so this is not
proof of a batch effect on its own, but a 5-fold swing driven by assembly
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

| scale | real | null mean | null 95th pct | p |
|---|---|---|---|---|
| country | 30.2% | 6.4% | 11.6% | 0.0010 |
| region | 79.1% | 43.9% | 51.2% | 0.0010 |

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

| | with | without |
|---|---|---|
| country | 13/43 | **8/43** |
| region | 34/43 | 33/43 |
| Mexico specifically | **5/5** | **0/5** |

Two genomes out of 3,015 carry the entire accessory advantage. Remove them and
accessory country (8/43) falls **below the core genome** (9/43). The Mexican
cases' next choices become Costa Rica, Czech Republic and El Salvador.

A contiguity-matched pool (nearest neighbour restricted to genomes within ±50%
of the query's contig count) reduces country 30% → 23% and region 79% → 74%.

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
genomes. **The Salmonella precedent that motivated this experiment (country
macro-F1 0.661 on accessory unitigs) did not run these controls.** That is worth
reporting whether or not our own result had been positive.

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
