# Handoff, 2026-08-21 evening

Read this first. Working directory
`/home/phemarajata/Downloads/snp-mod-local-working`.

**Nothing is running.** No background jobs, no monitors. The session ended clean.

This supersedes `HANDOFF_2026-08-21_SESSION_END.md` (17:28), which is now stale on
almost every number.

---

## 0. The one-paragraph state of play

The attribution paper's evidence is essentially complete and was re-run today
end-to-end on a published cgMLST scheme, an expanded and de-duplicated panel, and
an enlarged validation set. The headline changed: **country attribution does not
merely fail, it fails in a way that has a demonstrated mechanism**, and
**regional attribution is strong but partly an artifact that has to be reported
honestly**. One experiment remains that could turn the paper from a negative into
a contrast: **accessory-genome attribution**, described in §1. Everything else is
cleanup, and a deliberate decision was made not to redo the project (§6).

---

## 1. THE IMMEDIATE TASK: accessory attribution with a contig-count control

### 1.1 Why it matters

Today established that **signal legibility tracks divergence depth, not data
volume** (§3.4). The core genome only reads deep splits, so it can separate Asia
from non-Asia perfectly and cannot separate countries at all.

**Accessory content is the one data type that could carry the shallow signal.**
Phage, plasmids and ICEs are acquired locally and circulate in a place, so
accessory presence/absence may tag geography in a way vertical descent does not.
The Salmonella precedent reached country-level macro **F1 0.661** on accessory
unitigs where core SNPs give zero.

If it works, the paper becomes *core fails, accessory works, here is why*, which
is far stronger than a negative result.

### 1.2 The obstacle that must be controlled, or the result is worthless

**Assembly fragmentation causes apparent gene absence.** Measured today on the
57 QC'd genomes:

```
contigs vs cgMLST call rate:        rho = -0.642,  p = 7.5e-08
core coverage vs cgMLST call rate:  rho = +0.455,  p = 3.7e-04
```

A gene that is present but unassembled looks absent. For core genes this costs a
few points of call rate and is survivable. **For accessory presence/absence,
absence is the signal, so this is fatal if uncontrolled.**

The confound is directional in the worst way: assembly quality correlates with
sequencing center, which correlates with country. **An uncontrolled accessory
analysis risks recovering a signal about who did the sequencing and reporting it
as geography.** This is the first thing a reviewer will ask.

### 1.3 Protocol

**Step 0, decide the accessory representation.** Two routes:

- **Route A, PopPUNK accessory distances.** Cheapest. But
  `poppunk_bp/db/db.dists.npy` covers **2,802 genomes and only 16 of the 45
  validation genomes** (verified today). It must be extended before use. The
  `poppipe` conda env exists; there is no standalone `poppunk` env, so check
  `~/miniforge3/envs/poppipe/bin/`.
- **Route B, unitig or pangenome presence/absence.** Closer to the Salmonella
  precedent and more interpretable. **No tool is installed**: no panaroo, roary,
  ppanggolin, unitig-caller or bifrost. Needs an install.

Recommendation: **Route A first** because extending an existing sketch database
is cheaper than a pangenome build over 3,000 genomes, and it answers the
yes/no question. Go to Route B only if Route A shows signal.

**Step 1, score attribution.** Use `score_cgmlst_lichtenegger.py` as the
template. It already implements leave-group-out, the five estimators, the
distance stratification, and the exposure-override logic. Swap the distance
function for the accessory distance and keep everything else identical, so the
comparison to core is like-for-like.

**Step 2, THE CONTROL. Do not skip and do not run it after the fact.**

Pre-register these before looking at the accessory result:

1. **Stratify by contig count.** Split the panel into tertiles by contig count
   and score attribution *within* each stratum. If accessory accuracy tracks
   assembly quality rather than geography, it shows up immediately as accuracy
   varying across strata while the geographic composition is held fixed.
2. **Regress accessory distance on contig-count difference.** For each pair,
   does |contigs_A - contigs_B| predict accessory distance? If yes, the distance
   is partly measuring assembly quality.
3. **Permutation null on assembly quality.** Shuffle country labels within
   contig-count strata. If accuracy survives, the signal is geographic; if it
   collapses, it was a batch effect.
4. **Report the same distance stratification as for core** (d < 0.05,
   0.05-0.30, >= 0.30). If accessory scores *better* where no close relative
   exists, it is the same attractor artifact and not attribution (§3.3).

**Step 3, the honest outcomes.** All three are publishable:

- Accessory works and survives the control: the paper's headline changes.
- Accessory works but dies in the control: **a methodological finding worth
  publishing on its own**, because the Salmonella precedent did not run this
  control either.
- Accessory does not work: the core result is strengthened, since accessory was
  the best remaining hypothesis.

### 1.4 Inputs

| item | path | note |
|---|---|---|
| corrected panel | `PANEL_v4d_2026-08-21.tsv` | 2,955 genomes, use this |
| new genomes | `cgmlst_lichtenegger/MANIFEST.tsv` | 57 additions with role and exposure |
| assemblies | `cgmlst_lichtenegger/genomes/` | symlinks named by sample_id, 3,033 |
| contig counts | `BATCH3_QC_2026-08-21.tsv` | the 57 only; panel-wide needs recomputing |
| ground truth | `EXPOSURE_OVERRIDES.tsv` + `origin_basis` | 45 validation genomes |
| scoring template | `score_cgmlst_lichtenegger.py` | leave-group-out, 5 estimators |
| core comparison | `CGMLST_LICHT_ATTRIBUTION.tsv` | what accessory must beat |

**Contig counts are not available panel-wide.** Compute them from
`cgmlst_lichtenegger/genomes/` before the control can run.

---

## 2. What was done today

| | |
|---|---|
| ClonalFrameML v4c | finished 172/172, all exit 0. ν re-analyzed on the full set |
| 40 Terra assemblies | QC'd, 40/40 pass |
| 17 Mexican references | downloaded from NCBI, QC'd, 17/17 pass |
| cgMLST | re-run on the **published Lichtenegger scheme**, 3,033 genomes, 47m47s |
| attribution | re-scored, 45 validation genomes, 5 estimators |
| BioProject audit | found a leave-group-out leak and 16 duplicate isolates |
| panel | corrected 2,976 to **2,955** |
| GAMBIT bug | found, confirmed by controlled re-run, GitHub issue drafted |
| redo decision | **do not redo**, reasoning recorded |

---

## 3. The findings, in the order they matter

### 3.1 Country attribution: 1 genuine success in 43

Best estimator (nearest neighbour) gives 9/43, **below the 28% majority
baseline**. Stratified by distance:

| stratum | country | region |
|---|---|---|
| d < 0.05, real relative exists | **1/13** | 10/13 |
| 0.05 to 0.30 | 2/8 | 6/8 |
| d >= 0.30, no relative | 6/22 | 20/22 |

**Country is 1/13 where a genuine close relative exists.** Six of the nine
"successes" are attractor hits at d = 0.59 to 0.64. The honest number is **1
genuine success in 43** (Thailand, d = 0.0066).

### 3.2 Mexico is the controlled negative, and it is the paper's best result

Mexico went from **4 reference genomes to 21** and still scored **0/5**, nearest
neighbours at d = 0.406 to 0.462. The new Mexican references never became the
nearest neighbour; they are a different lineage.

**Absence of same-country references is necessary but not sufficient.** Adding
references for the right country does not buy attribution if they are the wrong
lineage. This is a harder and more interesting claim than "we lack references",
and it is now supported by a controlled test.

### 3.3 Region is 93%, and the number needs a caveat attached

**Region was never down.** The earlier "71%" compared a nearest-neighbour number
to a modal one. Original core-genome result: **modal 92%, NN 67%**. Today:

| estimator | country | region |
|---|---|---|
| nearest neighbour | **9/43 (21%)** | 36/43 (84%) |
| **modal k=20** | 6/43 (14%) | **40/43 (93%)** |
| baseline | 12/43 (28%) | 20/43 (47%) |

**93% on 43 genomes from 15 countries, versus 92% on 24.** Better, on a harder
set.

**But region scores highest where no relative exists** (91% at d >= 0.30 vs 77%
at d < 0.05). That is the attractor effect: a genome with no relative snaps to a
distant cluster, and coarse region labels make that "correct" often enough to
look like a capability. **Always report the stratification beside the 93%.**

**Estimator choice is scale-dependent.** Country does best under nearest
neighbour, region under modal k=20. **Never compare an NN number to a modal
one**, that mistake is what created the false 92%-to-71% regression.

### 3.4 The unifying mechanism: legibility tracks divergence depth

Granularity ladder, by Cohen's kappa (accuracy is not comparable across
groupings; kappa corrects for chance and neutralizes the Thailand-baseline
objection):

| grouping | acc | baseline | **kappa** |
|---|---|---|---|
| **Asia vs non-Asia** | **100%** | 60% | **1.000** |
| East vs West hemisphere | 95% | 65% | 0.901 |
| **region, 7-way** | 93% | 47% | **0.890** |
| SEA vs non-SEA | 74% | 58% | 0.425 |
| country | 21% | 28% | 0.188 |

Asia vs non-Asia is **13/13, 8/8, 22/22** across distance strata: perfect even
with no close relative, the *opposite* of the attractor pattern.

**At large genomic distance what stays legible is which side of the species'
deepest divergence a genome sits on**, and that split is Asia / non-Asia
(consistent with Pearson 2009 and Chewapreecha 2017). Country is unreadable at
every distance because lineages span countries.

**So the ceiling is set by the depth of the divergence being asked about, not by
data volume. More sequencing will not buy country resolution.**

Two consequences:
- **Coarser is not automatically better.** SEA/non-SEA is binary and beats only
  country, because that line cuts through the Asian clade (India and China are
  non-SEA but genomically Asian).
- **Region 7-way is the right operating point**: kappa within 0.11 of the binary
  split while carrying far more information.
- **"Western Hemisphere strain" (Gee 2017) survives as a grouping** (kappa
  0.901) even though ST92 across seven countries kills it as a country claim.

### 3.5 The CDC aromatherapy case, reproduced independently

Five 2021 aromatherapy genomes, outbreak held out:

| test | result |
|---|---|
| South Asia (n=75) vs all other regions (n=2,934) | median 0.7380 vs 0.7974, **p = 2.8e-34**, effect **0.82** |
| India (n=56) vs rest of South Asia (n=19) | **p = 0.351** |

**Genomics supports South Asia and not India**, exactly the boundary CDC hit;
their country call came from product supply chain.

**Use this as the paper's worked example.** A published outbreak where our method
reaches the same limit the published investigation did.

⚠ **Note the correction embedded here.** Absolute distance and discriminative
signal are different things. There is no close relative (d ~ 0.74), yet the
*ranking* of distances carries strong regional information. Do not repeat the
claim that d = 0.64 means "no signal".

### 3.6 A leave-group-out leak, and 16 duplicate isolates

`GCF_030010175_1_USA_Georgia` and `SRR17029022` are **the same BioSample**
(`SAMN23424236`, the aromatherapy bottle isolate). One copy held out as India,
one left in the pool as USA. It was the nearest neighbour for 5 of 6 Indian cases
at d = 0.007. Dropping it moved India from 0/6 to 6/6 at region.

Panel-wide, **16 BioSamples were represented twice** (mostly Laos pairs: a RefSeq
assembly plus our own SPAdes assembly of the same reads). Seven pairs had both
copies inside the same analyzed unit.

**Rule: deduplicate on BioSample, never on accession.** Accession-level checking
is what let this through twice.

### 3.7 cgMLST call rate independently validates the QC framework

Panel median 96.9%. Every genome the project had ever flagged fell to the bottom
without being told to: the two duplicated-chromosome-II assemblies (59.8%,
64.3%), the register-excluded `SRR2896257` (60.8%), both
`marginal_core_coverage` genomes (76.8%, 78.8%), both excluded ONT genomes.

This settled the exclusion-register defect with independent evidence and is worth
a sentence in the paper as orthogonal validation.

### 3.8 GAMBIT 3.0.0 misidentifies B. pseudomallei as B. mallei

Controlled re-run, same assemblies, same tool v1.0.0, only the database changed:
**DB 2.2.0 gives B. pseudomallei 40/40; DB 3.0.0 gives B. mallei 40/40.**
Refuted by mash: all 57 sit 0.0041 to 0.0077 from K96243.

GitHub issue drafted at `THEIAGEN_GAMBIT_ISSUE.md`, formatted to the repo's
the repo's Bug Report template template. **Not yet filed.**

Do **not** use `gambit_predicted_taxon` as the species gate on GAMBIT 3.x. Gate
on mash to K96243.

---

## 4. Paper framing

### 4.1 Two papers, decided

- **Paper 1 = limits + capability, fused.** The limit *is* the capability
  statement. Evidence complete.
- **Paper 2 = the Gubbins r/m operating envelope.** Complete but unwritten.
- Paper 3 (recombination-aware subtree merging) stays deferred.

### 4.2 The spine of Paper 1

> Country attribution fails at every resolution and, critically, fails even where
> same-country references exist (Mexico, 21 references, 0/5) and even where a
> genuine close relative exists (1/13). Regional attribution succeeds at 93%, but
> largely because coarse labels convert "unlike the panel majority" into a
> correct answer. What is actually legible from the genome is the species'
> deepest divergence, and that ceiling is set by divergence depth rather than
> data volume.

### 4.3 Positioning

- **Prior work reconstructs; we predict.** Seng 2024 and Chewapreecha 2017 score
  by internal consistency; we score on held-out cases. State this early or the
  result reads as contradicting a literature it does not contradict.
- **Viberg 2017** ("strong phylogeographic signal at continental level") is our
  result quantified, not a contradiction.
- **McLaughlin/Gulvik 2022** (PBP dual-locus, no held-out validation) is the
  contradicting result. Frame as *"we tested prospectively what prior schemes
  asserted descriptively"*, never as carelessness.
- **Sprenger/Gulvik 2026** attributes the aromatherapy MAG to India. Our §3.5
  reproduces their genomics limit exactly. Do not appear to contradict them.
- **cgMLST citation: Lichtenegger et al. 2021, JCM 59:e00093-21, PMID 33980649.**
  "Ashcroft et al. 2021" is a **phantom citation** in our documents; it is the
  same paper, misattributed. We now use the published 4,221-locus scheme.

### 4.4 Reporting rules that must survive into print

1. **Report kappa alongside accuracy** for every grouping.
2. **Report the distance stratification beside every headline accuracy.**
3. **Name the estimator.** Never compare NN to modal.
4. **Quote 41.1% panel coverage, not 44%.** The 44% used a read-run-only
   denominator.
5. **Do not quote the all-unit r/m median.** Use 7.38, the median of the 47
   in-window units.
6. **Propose scale-dependent abstention**: decline the country call above
   d = 0.30, keep the regional one, since those 22 calls are 22/22 correct on
   Asia vs non-Asia.

---

## 5. Action items, ranked

**Done today:** Tier 1 data fixes, `NUMBERS.tsv`, duplicate register, corrected
panel, cgMLST re-run, attribution re-score, BioProject audit, GAMBIT issue draft.

**Next:**

1. **The accessory experiment with its control** (§1). The only remaining
   experiment that could change the headline.
2. **Re-derive the 4 affected units.** `strain_1_L1_26` (154 to 153),
   `strain_1_L1_8` (91 to 89), `strain_14_L1_4` (14 to 12), and
   **`strain_1_L1_10` which falls from 7 to 4 and must be dropped as a unit.**
   Only 4 of 86 units are affected; 82 are untouched.
3. **File the GAMBIT issue** (`THEIAGEN_GAMBIT_ISSUE.md`).
4. **Get the IRB approval number** from the epi team into the Methods. The epis
   handled the approval; only the text is missing.
5. **PubMLST vs Lichtenegger scheme concordance.** Both profile sets exist. Turns
   the scheme swap into a robustness result.
6. **Two method questions for Paper 2**: quantify `+ASC` vs `-fconst` on one
   unit, and recompute Gate 1 diversity from alignment distances instead of the
   Mash proxy.
7. **Citation audit**: fix "Chewapreecha 2024" to **Seng et al. 2024**, resolve
   the two conflicting Pearson 2020 PMIDs, retrieve the Ceará 2021 and eLife
   Salmonella citations.
8. **Literature pass on accessory-genome attribution.** Unsearched. The Salmonella
   precedent exists in our notes as a bare URL.

**Deliberately not doing:** re-partitioning, re-running the SNP pipeline
wholesale, rewriting the corpus. Reasoning in `REDO_DECISION_2026-08-21.md`.

---

## 6. Why we are not redoing the project

Short version, for defending the decision:

- **The analyses were independently reproduced; the documents were not.** Two
  runs on different hardware agree to **0.38%** median relative r/m across 82
  units. The attribution result holds across three typing systems, two of which
  use no partition, and across two independent cgMLST schemes.
- **The defects were bounded and enumerated:** 4 of 86 units, 266 of 2,352
  genomes. 82 units untouched.
- **We fixed the mechanism, not the instances.** Numbers are now generated
  (`generate_numbers.py` to `NUMBERS.tsv`) rather than restated in prose;
  deduplication is at BioSample level.
- **Re-running carried its own risk.** Every re-partition in this project
  introduced new defects (v4 silently dropped 521 genomes; v4b lost 108; v4c
  produced the `strain_4` label collision), and Gubbins' zero-seed bug gives
  ~16% chance per run of silently losing a unit.

Framing: **we localized the damage rather than hiding it under a fresh run.**

---

## 7. Rules and traps

1. **Run `python3 generate_numbers.py` before quoting any figure.** It regenerates
   36 headline numbers from primary data into `NUMBERS.tsv`, with warnings
   attached to the dangerous ones. **Documents cite that file; they do not restate
   values.** Of six headline numbers checked today, four were wrong in at least
   one circulating document, and the code was right every time.
2. **Every ENA census must union `read_run` with `result=assembly`.** A read-run
   query is blind to assembly-only depositions and produced two wrong claims
   (Mexico "0 genomes" when it has 21).
3. **Deduplicate on BioSample, never accession.**
4. **Never compare a nearest-neighbour number to a modal one.**
5. **Never quote an accuracy without its baseline and its denominator.**
6. **Never test a ratio by splitting on its own denominator.**
7. **Do not record a count until the run producing it has stopped.** Seven
   instances in this project, every one flattering the result.
8. **On GAMBIT 3.x, gate species on mash to K96243, not
   `gambit_predicted_taxon`.**

---

## 8. Key files

| file | what |
|---|---|
| **`NUMBERS.tsv`** | **every quotable figure, regenerated. Start here** |
| `generate_numbers.py` | regenerates the above |
| `PANEL_v4d_2026-08-21.tsv` | the corrected panel, 2,955 genomes |
| `PANEL_DUPLICATES_2026-08-21.tsv` | 18 duplicate drops with justification |
| `GENOME_REGISTER_2026-08-21.md` | panel / validation / census reconciliation |
| `MANUSCRIPT_OUTLINE_2026-08-21.md` | full outline, results, weak spots W1-W11 |
| `ATTRIBUTION_FINAL_2026-08-21.md` | the final attribution result |
| `GROUPING_AND_CDC_2026-08-21.md` | granularity ladder and the CDC reproduction |
| `BIOPROJECT_AUDIT_2026-08-21.md` | the leak and the 16 duplicates |
| `CGMLST_LICHTENEGGER_RESULT_2026-08-21.md` | the cgMLST re-run |
| `BATCH3_QC_REPORT_2026-08-21.md` | QC of the 57 additions |
| `REDO_DECISION_2026-08-21.md` | why we are not redoing |
| `THEIAGEN_GAMBIT_ISSUE.md` | GitHub issue, ready to file |
| `score_cgmlst_lichtenegger.py` | **the scoring template for §1** |
| `grouping_test_bp.py` | granularity ladder with kappa |

**Superseded:** `HANDOFF_2026-08-21_SESSION_END.md`, and every figure in
`SAMPLING_FRAME_2026-08-21.md` §3 and `GAP4` §1/§12.
