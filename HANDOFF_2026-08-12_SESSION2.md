# Session handoff — 2026-08-12 (session 2)

Continues `HANDOFF_2026-08-12.md`. That file is still the record for Deliverable A's
evidence base; **this file covers the workflow/pipeline work and the caller
investigation.** Read §0 first.

---

## §0 READ THIS FIRST — the one habit that produced every real finding

Every substantive result this session came from **changing one variable at a time
and measuring**, and every wrong conclusion came from inferring instead. Four
claims were made and then refuted by measurement:

| claim | how it died |
|---|---|
| "ska biases r/m low by 23–43%" | extrapolated from one cluster; refuted on a real analysed unit |
| "snippy runs ~15% lower" | looked solid after `s1_L1_19` alone; refuted by `s1_L1_9` (opposite sign) |
| "the caller gap is Gubbins parameters" | refuted by the decisive test — it was mostly the *alignment* |
| spacing ratio 0.623 | positions indexed the SNP-only alignment, not the genome |

**Session 3 added a fifth** (see §9): *"the alignment fixes in `10d1669` close the
fidelity gap"* — they closed the **alignment** half and left r/m at 0.47–0.78× of
target. End-to-end r/m was never going to match while a fourth variable (Gubbins
settings) was still free. Same failure mode as the row above it: a partial fix
read as a whole one. **Verify the settings actually took effect in the
diagnostics log before reading any number the run produces.**

**Two effects that offset each other will masquerade as agreement.** The workflow
looked ~2% from the manual baseline end-to-end while actually differing by +59%
(alignment) and −37% (Gubbins params). Do not trust an end-to-end match; decompose.

---

## §1 STATE: nothing running, 408 GB free

- No processes running (verified). All monitors ended.
- **76 GB reclaimed** in session 2 by purging superseded run dirs. Session 3 spent
  ~29 GB back on `cs_*_work` + `fid_*_work` (437 → 408 GB free). **Do not purge the
  `_work` dirs**: `per_branch_statistics.csv` lives only there, and it is the sole
  source of pooled r/m — the workflow never publishes it to `outdir`.
- Pipeline repo `~/wf-assembly-snps-mod`: **`main` is at `f4cccbc`, pushed.**
  Session 3 fast-forwarded `main` over all 5 branch commits (`6a5e018`, `4a10de4`,
  `10d1669`, `aa9357f`, `f4cccbc`) — no merge commit, history is linear. Working
  tree clean, `main` == `origin/main`. **`curated-partition-references` is deleted**
  (local and `origin`) — it was fully merged, so every commit lives on `main`.
  Section headings below still name the branch; that is now history, not state.
  *(Session 2 wrote "4 commits, NOT pushed" counting `08db3ee`, which was already
  on `main`; it was 3 unpushed at the time.)*

---

## §2 PIPELINE WORK — 4 commits on `curated-partition-references`

| commit | what |
|---|---|
| `08db3ee` | pin RAxML + Gubbins 3.4.3 + invariant-site correction *(already on `main`, pushed)* |
| `6a5e018` | **curated mode**: `--cluster_assignments` + `--cluster_references` bypass Mash clustering & medoid selection |
| `4a10de4` | **`--split_replicons`**: per-replicon alignment + Gubbins, keyed `cluster__<replicon>`; fails loudly on a draft ref (> `--max_replicons`, default 4) |
| `10d1669` | **corrected defaults**: `max_column_missingness` 0.10→**1.0**; curated mode now counts as an external reference so the `Reference` taxon is **kept** |
| `aa9357f` | **`--gubbins_skip_starting_tree`** (default false): substitutes the 0-byte `assets/NO_FILE` for `IQTREE_FAST.out.tree`, so `GUBBINS_CLUSTER`'s existing `[ -s "$starting_tree" ]` guard takes the no-starting-tree branch. The last Gubbins knob with no param behind it. *(session 3)* |

All stub-verified. Curated mode runs the per-cluster chain
(SNIPPY→GUBBINS→IQTREE_ASC→SUMMARIZE) with none of
MASH/CLUSTER_GENOMES/SELECT_CLUSTER_REPRESENTATIVE/BACKBONE/GRAFT. Replicon split
verified standalone: 2 files at 3,985,223 + 3,100,174 bp matching the source contigs
exactly.

### ✅ DONE in session 3 — see §9
Re-run under `10d1669` completed, then the fidelity check with production Gubbins
settings. **All four replicons reproduce the manual baselines.** A fifth commit
`aa9357f` adds `--gubbins_skip_starting_tree`. Targets (frozen, verified):
`s1_L1_19` chr1 **2.03** / chr2 **1.89**; `s1_L1_9` chr1 **5.11** / chr2 **6.28**.

---

## §3 THE DECOMPOSITION THAT CLOSED THE LOOP

Question: does the workflow reproduce the manual pipeline? Answered by holding
everything constant and varying one thing at a time. **s1_L1_19 chr1, identical
Gubbins flags throughout:**

| alignment | r/m | |
|---|---|---|
| manual (no filter, 35 taxa incl. Reference) | **2.03** | published baseline |
| **workflow full-length + Reference kept** | **2.00** | ← **matches** |
| workflow filtered @0.10 + Reference dropped | **3.23** | +59% |

Because 2.00 ≈ 2.03, **the snippy variant calls are equivalent between the two
pipelines** and the entire discrepancy was two workflow transforms. Both now fixed
in `10d1669`. **No bug in the curated/split code.** Nothing unexplained remains.

Separately, Gubbins flags (`--min-snps 2` vs default 3, `--iterations 3` vs 5,
starting tree, hybrid builder) move r/m the *other* way, ~−37% on the same
alignment (3.23 → 2.57). These are still at workflow values and are a **judgement
call, not a fidelity constraint** — see §6.

> **Session 3 amends this.** True that they are not a *code* fidelity constraint,
> but they are absolutely a constraint on **reproducing the baselines**: left at
> workflow values they hold r/m at 0.47–0.78× of target through the real
> workflow. §9 measures all four replicons at production settings and closes the
> loop. The −37% figure was one replicon; the real spread is wider and
> non-uniform.

### Why `max_column_missingness = 1.0` is right (three converging lines)
1. The param's own in-repo benchmark: injected 8 kb block recall **0.991 no filter**
   vs 0.921 @0.10 vs 0.508 all-ATCG.
2. **Coordinate integrity** — Gubbins is a *spatial* statistic. Dropping columns
   (148,464 of 3,100,174 = 4.8% at 0.10) renumbers positions, compressing SNP
   spacing and inflating local density. The dropped columns cluster in
   poorly-covered/repetitive regions, so the bias is not uniform. Same principle as
   splitting replicons and never feeding a SNP-only alignment.
3. Measured end-to-end, above.

---

## §4 CALLER INVESTIGATION — ska_map vs snippy (complete)

**Mechanism CONFIRMED.** SKA2 split k-mers (k=31) cannot call a variant whose flank
carries another variant. Recovery vs snippy by nearest-neighbour spacing:
**0–10 bp 0.152 | 10–31 bp 0.717 | 31–100 bp 0.984 | ≥500 bp 1.279** — depletion
stops exactly at the k=31 boundary. (`CALLER_SPACING_RESULT.txt`)

**Mismapping REFUTED as the counter-explanation**, two independent ways:
nucmer self-alignment 28/2,474 clustered SNPs in repeats even permissively;
RefSeq annotation 21/3,144 in mobile elements, **0** in rRNA. Clustered SNPs are
*depleted* in CDS (56% vs 89.6%) — the signature of recombinant tract boundaries.
(`CALLER_REPEAT_RESULT.txt`, `CALLER_ANNOTATION_RESULT.txt`)

**But r/m has NO stable sign** — measured, not inferred: cluster37 snippy
1.29–1.76× higher; `s1_L1_19` 0.851× lower; `s1_L1_9` 1.332× higher.
**Never apply a caller correction factor.**

**What IS consistent: tract length.** 4/4 paired replicons, all < 1: ska
median-of-medians **5,388 bp** vs snippy **3,553 bp** (ratio 0.64), union coverage
nearly unchanged. Same recombinant sequence, more and shorter tracts.

**Empty r/m band (2.30–4.28) HOLDS** from both edges: `s1_L1_19` 2.30→1.96 (below),
`s1_L1_9` 4.28→5.69 (above) — both move *away*. Not a caller artefact; the
26/853 coverage split stands. All written into `METHODS_DRAFT` §2.5/§2.8.2/limitation 11.

**Caller decision:** snippy going forward (sensitivity must not depend on the
quantity being estimated); **keep ska for the published paper** — switching would
invalidate the Tier 2 null (built on ska alignments) and the spike-in, with no
correction factor available. Documented as limitation 11.

---

## §5 MASH CLUSTERING CANNOT PARTITION THIS COLLECTION

The first full 2,802-genome run was **killed at ~20 min, correctly**. At
`mash_threshold = 0.028`: *one* connected component containing all 2,802, chopped
into 60 size-capped parts. **Gini 0.059, max/min 2.78** — below Wu's *deliberately
imposed* 10-way cut (0.095). An imposed partition, not a found one.

Threshold sweep on the real matrix (`MASH_THRESHOLD_SWEEP.txt`) — **no threshold
works**: fuses into one component between **0.005 and 0.007** (straddling the `bp`
profile's own suggested range), shatters into 786/1,094 singletons below.
Single-linkage chains through this collection. **This independently reproduces why
the project moved to PopPUNK/fastbaps.** Curated mode (§2) is the fix.

Matrix preserved: **`mash_matrix_2802.tsv`** (82 MB) — reuse it, don't recompute.

---

## §6 OPEN DECISIONS (yours, not blockers)

1. **Gubbins params in the workflow** — `--min-snps 2` (vs default 3),
   `--iterations 3` (vs 5), IQTREE_FAST starting tree, hybrid builder. These are the
   pipeline author's speed choices. User's framing: *"whichever gives the best
   results… not stick to the former settings."* So this is an optimization question,
   not fidelity. `gubbins_min_snps` / `gubbins_iterations` / `gubbins_use_hybrid` are
   already params; the starting tree needs a toggle (GUBBINS_CLUSTER already has a
   `has_starting_tree` guard — pass an empty sentinel to disable, no module surgery).
   **Session 3: the toggle now exists (`aa9357f`, the sentinel approach worked as
   described), and the choice is costed** — speed settings buy ~5/3 fewer
   iterations and no first-tree build, at 0.47–0.78× on r/m, non-uniformly (§9).
   Still your call, but production settings are the only ones that reproduce the
   baselines, so anything quantitative should use them.
2. ~~**Push / merge** `curated-partition-references` to `main`~~ — done in
   session 3. `main` is at `f4cccbc` and pushed; see §1.
2b. ~~**Phantom `Tier4` row in split mode**~~ — fixed in `f4cccbc` (§9).
3. **Whole-collection run** — only meaningful in curated mode with a
   PopPUNK/fastbaps partition (§5). Needs a `cluster_assignments` TSV for all 26–37
   units and a `cluster_references` TSV (complete/borrowed per unit — the manual
   analysis already decided these; 12 of 45 had a complete internal member, 33
   borrowed).
4. **`[CONFIRM]` in `METHODS_DRAFT`** — **answered in session 3, user-confirmed.**
   The 312 in-house `IP-`/`IE-` isolates: **Illumina paired-end**, assembled with
   **`bacterial-genomics/wf-paired-end-illumina-assembly` v3.1.1** (a *different*
   upstream repo from `wf-assembly-snps-mod`), **SPAdes** path. Chain: Trimmomatic
   → bbduk PhiX → FLASH overlap → SPAdes → bwa + Pilon polish. Written into
   `METHODS_DRAFT_2026-08-11.md` §2.1, replacing the placeholder.

   **One small residue, still `[CONFIRM]`:** the SPAdes *version number*. That
   workflow pins containers by digest (`staphb/spades@sha256:5df39e84…`) not by
   version tag, so it is not readable from the workflow source. Get it from the
   assembly runs' `software_versions.yml` or by inspecting the image — and the
   same for Trimmomatic / Pilon if the journal wants per-tool versions.
5. **Untested alternative** — indel-adjacent alignment artefact in snippy. Neither
   repeats nor mobile elements, so both overlap tests miss it. Doesn't affect the
   band verdict.

---

## §7 FILES

**Preserved / load-bearing**
- `MANUAL_RESULTS_FROZEN/` (162 MB) — 184 prod arms + **`snippy_baselines/`**
  (4 arms, verified reproducing 2.03 / 1.89 / 5.11 / 6.28). The comparison targets.
- `mash_matrix_2802.tsv` (82 MB) — expensive, reuse.
- `prod_*` (46 dirs) — the published manual analysis, untouched.
- Results: `CALLER_SPACING_RESULT.txt`, `CALLER_REPEAT_RESULT.txt`,
  `CALLER_ANNOTATION_RESULT.txt`, `SNIPPY_BAND_TEST_RESULT.txt`,
  `MASH_THRESHOLD_SWEEP.txt`, `FULLRUN_v1_cluster_summary_threshold0.028.txt`,
  `TRIAGE_RESULTS_2026-08-11.txt`, `SPIKEIN_RESULT.txt`,
  `TREEBUILDER_EQ_RESULT.txt`, `RAPIDNJ_EQ_RESULT.txt`.
- Runners: `run_wf_curated_split.sh`, `run_snippy_s1_L1_19.sh`,
  `run_snippy_s1_L1_9.sh`, `run_smoketest.sh`, `run_full_workflow.sh`.
- Curated inputs (built, ready): `curated_s1_L1_19_{clusters,refs}.tsv`,
  `curated_s1_L1_9_{clusters,refs}.tsv`, `wf_*_samplesheet.csv`,
  `refs_s1_L1_19_close.fa`, `refs_s1_L1_9_close.fa`, `refs_K96243.fa`.
- New analysis scripts (all self-tested): `caller_spacing_bp.py`,
  `caller_repeat_overlap_bp.py`, `caller_annotation_overlap_bp.py`,
  `mash_threshold_sweep_bp.py`.

**Stale — do not quote**
- ~~`cs_s1_L1_19_out` / `cs_s1_L1_9_out` — old defaults (chr1 2.41 / chr2 2.20;
  chr1 3.72 / chr2 3.54)~~ — **overwritten in session 3** by the `10d1669` re-run.
  They now hold *correct-alignment, workflow-Gubbins* results (§9), which are
  legitimate but are **not** the fidelity numbers. Quote `fid_*_out` for fidelity.
- v1 per-unit whole-genome workflow numbers (2.25, 4.15) — draft medoid ref, unsplit.

**Session 3 additions**
- `fid_s1_L1_19_out` / `fid_s1_L1_9_out` + `fid_*_work` — the fidelity runs (§9).
  **The `_work` dirs are load-bearing**: `per_branch_statistics.csv` is the only
  source of pooled r/m and the workflow does **not** publish it to `outdir`.
- `run_wf_fidelity.sh` — the fidelity runner, carrying the production Gubbins
  invocation in its header comment.

**Purged** (76 GB): `fullrun_{work,out}`, `wf_*_{work,out}`, `cs_*_work`,
`snippy_s1_L1_19/`, `snippy_s1_L1_9/` (stats frozen first), scratchpad test dirs.

---

## §8 ENVIRONMENT TRAPS

- **Java/Nextflow**: `~/.bashrc` had `JAVA_HOME` → a non-existent conda env, so
  Nextflow fell back to conda base's Java 11 and refused to start. User fixed it.
  Deactivating conda alone is **not** enough (`miniforge3/bin` stays ahead on PATH).
  All runner scripts set `JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64` explicitly.
- **Stale Nextflow session locks** — 23 accumulated from killed stub runs and caused
  "cannot acquire lock". Clear with `rm -rf ~/wf-assembly-snps-mod/.nextflow/cache/*`
  when nothing is running.
- **`-work-dir` must be on `/home`**, never `/tmp` — a full run's work dir hit 254 GB.
- **`pkill -f "nextflow.*run \."` matches its own shell** and kills the tool call
  (exit 143). Check `ps -eo args | awk '!/awk/'` instead of trusting `pgrep -c`.
- **Gubbins CWD collision** (from session 1, still live): scratch goes to CWD, not
  `--prefix`; the isolating property is the **basename**, not the path.

---

## §9 SESSION 3 — THE FIDELITY LOOP IS CLOSED

**§2's acceptance test passes.** Curated+split reproduces the manual snippy
pipeline on all four replicons. Two runs, one variable moved between them.

Pooled r/m — and *pooled* is the definition: `sum(SNPs inside recombinations) /
sum(SNPs outside)` over `gubbins.per_branch_statistics.csv`, which reproduces all
four frozen targets exactly (2.0342 / 1.8855 / 5.1075 / 6.2825). **Median and mean
do not** — `s1_L1_9`'s median is 0.0. Session 2 never wrote this down.

| unit | rep | manual | `cs` (workflow gubbins) | **`fid`** (production gubbins) | fid/target |
|---|---|---|---|---|---|
| `s1_L1_19` | chr1 | 2.0342 | 1.4861 | **2.0022** | 0.984 |
| | chr2 | 1.8855 | 1.4745 | **1.8707** | 0.992 |
| `s1_L1_9` | chr1 | 5.1075 | 3.8888 | **5.1235** | 1.003 |
| | chr2 | 6.2825 | 2.9772 | **6.2956** | 1.002 |

The match is not just the ratio — inside/outside and block counts land on the
manual values too (`s1_L1_9` chr2: outside 3,041 vs 3,041; blocks 841 vs 849).
`s1_L1_9` (181 branches) matches better than `s1_L1_19` (69), the right direction
for RAxML tree-search stochasticity, so read the ~1% residual as noise. Two units
only — don't over-claim.

### What `10d1669` did and did not fix
It fixed the alignment, completely and verifiably: `kept_fraction 1.000000`,
`Reference` present at `missing_fraction 0.000000`, and **total SNPs within 0.7%
of the manual arms on all four replicons** with identical branch counts. That is
the strong result — *the variant calls and the alignment are equivalent.*

It did not close the r/m gap, because Gubbins settings were still free. At the
pipeline's speed settings the same alignments give **0.731 / 0.782 / 0.761 /
0.474** of target: same variants, different partition into recombinant vs clonal,
via more and smaller blocks (1,440 vs 1,263).

### Two consequences that outlive this test
1. **No correction factor between Gubbins settings.** The spread is 0.47–0.78,
   not a constant — same conclusion §4 reached for callers. **Never pool r/m from
   different Gubbins settings into one distribution**, and never compare a run to
   the frozen baselines without first confirming settings match.
2. **The empty band is parameter-conditional.** Under speed settings both
   `s1_L1_9` replicons fall from 5.11/6.28 *into* the 2.30–4.28 band; under
   production settings they sit well above it. The band is sound as built
   (production settings throughout) but would need re-deriving, not inheriting,
   if production ever moves to the speed settings. Belongs in `METHODS_DRAFT`
   next to limitation 11.

### Reproducing it
```bash
cd /home/phemarajata/Downloads/snp-mod-local-working
bash run_wf_fidelity.sh s1_L1_19 s1_L1_9
```
Sets `--gubbins_min_snps 3 --gubbins_iterations 5 --gubbins_use_hybrid false
--gubbins_skip_starting_tree true`. `gubbins_tree_builder` /
`gubbins_first_tree_builder` are already `raxml` and `gubbins_filter_percentage`
already `25`, matching production, so they need no override.

**The production invocation these reproduce** — recovered from
`reference_sensitivity_bp.py:740`, since the `snippy_*/arms/*.sh` scripts were
purged in session 2:
```
run_gubbins.py --prefix "$OUT/gubbins" --threads "$THREADS" \
               --invariant-site-correction --filter-percentage 25 \
               "$OUT/aln.full.$REPLICON.fa"
```
No `--min-snps`, `--iterations`, `--tree-builder` or `--starting-tree` — so
production runs on Gubbins' own defaults (3, 5, raxml, none). Corroborated by the
manual `gubbins.log`: raxmlHPC-PTHREADS-AVX2 as both first- and later-iteration
tree constructor, Gubbins 3.4.3.

**ALWAYS verify the settings took effect before reading a number.** Grep each
`Gubbins/*.diagnostics.log` for `has_starting_tree=false` and
`RUN: no starting-tree + NON-HYBRID tree_builder=raxml`. Params passed ≠ params
applied, and an unverified r/m is exactly how §0's four dead claims happened.

### Phantom Tier4 row — FIXED in `f4cccbc`
Every split-mode run used to emit a **third summary row** keyed on the bare
cluster id (`s1_L1_19`, `s1_L1_9`) with `gubbins_status no_diagnostics`,
`failed_no_tree`, `Tier4_no_meaningful_tree`. `SUMMARIZE_CLUSTER_PHYLOGENY`
enumerates clusters from `ch_clusters_file` — the assignments TSV, which carries
**unsplit** ids — while every artefact is keyed `<cluster>__<replicon>`, so the
bare id matched nothing and the "include any cluster mentioned in clusters.tsv"
fallback invented a failure. Harmless per run, but anything aggregating
confidence tiers across units would have counted it.

`bin/summarize_cluster_phylogeny.py` now detects the split by asking whether any
artefact key starts with `<cluster_id>__` — anchored on known cluster ids rather
than splitting artefact keys on `__`, because a cluster id may itself contain
`__`. Split parents are dropped; **the fallback stays**, so a genuinely failed
cluster is still reported.

Replicon rows also now inherit the parent's `n_isolates` (34 / 90) instead of
falling through to the alignment record count (35 / 91, which includes the
external `Reference` — not a cluster member). `seq_count_in_alignment` still
carries the alignment's own taxon count, and `notes` gains `replicon_of=<parent>`.

Verified three ways on real `fid_s1_L1_19_out` artefacts: phantom row gone with
both replicon rows Tier1 at n_isolates=34; a synthetic artefact-less cluster
still reported Tier4; the non-split path producing an identical single row.
**The existing `cs_*_out` / `fid_*_out` summaries on disk still contain the
phantom row** — they were written before the fix. Re-run to regenerate, or
ignore that row.
