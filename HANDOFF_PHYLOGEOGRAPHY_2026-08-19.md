# Handoff — phylogeographic analysis of the v4c panel

Written 2026-08-19 from the RTX 4070 workstation, at the end of the session that
finished the v4c SNP runs. For a new chat picking up phylogeography.

**Revised 2026-08-19 after an independent re-verification pass against disk.**
Corrected in that pass: all GAP4 cross-references (they cited short-version
points using body-section notation, and two pointed at sections that do not
exist); the grafted tree's two-scale ratio (52×, not 133×); the Thailand share
and its denominator; and the claim that a `--assignments` file needs building.
Two fixes were also made outside this document: Methods §2.12.9 no longer
describes a single-country test the code never implemented, and
`phylogeography_association_bp.py` no longer scores 274 genomes whose
`bioproject` is the literal string `unknown` as one shared study (§3). Figures
below were recomputed from the trees and metadata, not carried over.

**Second revision, same day.** The claim that the A100's `Clusters/` were never
uploaded was **wrong** — they are on Drive and take seconds to pull (§7). The
association test has now been run on the real 88-unit production partition;
results are in §3.

Working directory: `/home/phemarajata/Downloads/snp-mod-local-working`

---

## 1. Read these first, in this order

| # | file | why |
|---|---|---|
| 1 | **`GAP4_phylogeography_biased_sampling.md`** | 160 KB methodological review, already done. **It largely decides what you may and may not do.** Its 16-point "short version" is the summary; read at minimum that. |
| 2 | **`PHYLOGEOGRAPHY_ASSOCIATION_INTERPRETATION.md`** | what the association test computes, how to read it, and the multi-scale result: the signal is **national** — sub-national is inseparable from study design, continental is unaskable for 82% of units |
| 3 | `METHODS_DRAFT_2026-08-19.md` §2.12.9 | the association test as already specified and run |
| 4 | `START_HERE.md` (Drive bundle) | read order for the v4c results and what supersedes what |
| 5 | memory files (below) | the traps |

> **GAP4 has two independent numbering schemes and they collide.** The "short
> version" is 16 numbered *points*; the body is 12 numbered *sections* (§1–§12,
> with subsections). They do not correspond — there is no §15 or §16. Every
> citation below gives the short-version **point** first and the body **section**
> second.

**Do not re-derive GAP4's conclusions.** It cost a lot of work and it is the
strongest asset here. It is a *literature and design* review, not an analysis of
this panel — so its conclusions are inputs to your analysis, not results.

---

## 2. The single most important constraint

**Discrete trait analysis (DTA) is not defensible on this collection, and neither
is the structured coalescent.** GAP4 short-version points 2–5 establish this
(body §2 for DTA, §3 for the structured coalescent), with citations:

- DTA treats relative sampling intensity as data informative about migration,
  *before any sequence is analysed*. This panel is **66.4% Thailand** with the
  two largest BioProjects alone at 43% (§6); sampling intensity spans
  **35,852-fold** across countries, and at the top of the burden distribution
  sampling and true burden are **inverted** (South Asia: 44.2% of predicted
  global cases, 2.9% of genomes).
- BASTA/MASCOT are not the escape hatch — they were biased even on *unbiased*
  samples in the only head-to-head benchmark, and their specific failure mode
  (inflating migration rates *to* under-represented demes) would declare this
  panel's singleton countries the drivers of global spread.
- They would not run anyway: O(N·S³), and the literature caps usable analyses at
  ~15 demes. This panel has 43+ countries.
- MASCOT-GLM rescued inference in the benchmark by using case-count time series.
  **Melioidosis has none.**

So: **no BEAST-family phylogeography.** If you conclude otherwise, you are
disagreeing with a documented review — say so explicitly and give the reason.

### What IS defensible

1. **The permutation-based association test already implemented** (§3 below).
2. **Tip-state-swap permutation nulls**, including permuting **BioProject** —
   the only handle on the study-of-origin confounder (GAP4 point 7, body §4.1a).
3. **Sampling-corrected root prior**: `pi = (n_i/s_i)/Σ(n_j/s_j)`, with `s_i`
   from the burden estimates in `phylogeography_diagnostics_bp.py §F`
   (GAP4 point 7, body §4.1a).
4. **Balanced subsampling** — but as a *trade*, stratified on country × BioProject
   × year, reporting what it costs. At n=15/country it retains 4.1% of the
   collection; n=100 is the better operating point (8 countries, 14.5%). Do not
   claim it removes the bias (GAP4 points 6 and 8, body §4.1).
   **Both percentages are on GAP4's 5,515-genome denominator, not this panel's**
   (2,976 metadata rows / 2,352 analysed). Recompute before quoting either for
   v4c.
5. **`make.simmap` transition counts and directions** — these survive an undated
   tree. **Occupancy times do not** (they become substitutions on a
   substitution-scaled tree). Note phytools' documented root-prior sampling bug
   in ≤1.0-1; the root state *is* the Australian-origin claim, so re-run rather
   than assume (GAP4 point 16, body §10).

---

## 3. What has already been run, and what needs redoing for v4c

`phylogeography_association_bp.py` implements the test in Methods §2.12.9:

> Fitch small-parsimony score of country labels on the recombination-corrected
> topology, against a null of **1,000 permutations of labels across tips of the
> same tree**. Permuting holds topology *and* country composition fixed, so a
> 90%-Thai unit is compared against other 90%-Thai arrangements. Unknown-country
> tips are fully ambiguous, so missing metadata weakens signal rather than
> inventing it. **BioProject is tested identically and reported alongside** —
> a geographic signal no stronger than the BioProject signal is not evidence of
> phylogeography.

```
python3 phylogeography_association_bp.py \
  --assignments <sample_id -> country/bioproject TSV> \
  --trees L1v4c_out/Clusters \
  --perms 1000 --seed 20260815 \
  --out PHYLOGEOGRAPHY_ASSOCIATION_v4c.tsv
```

Output columns: `unit, n_tips, variable, n_known, n_distinct, parsimony_score,
top_share, p_value, verdict` — two rows per unit (`country`, `bioproject`).

**Status: run and done — see "Results" below.** The old
`PHYLOGEOGRAPHY_ASSOCIATION.tsv` (164 rows, 82 units) is v3-era; all 82 of its
unit names match `L1v3_out` membership, and 55 of them *also* exist in v4c with
different membership, so it looks partly current and is not. Do not use it.

The trees are at `L1v4c_out/Clusters` (172 replicon-unit dirs, Track A; the
script uses the 86 replicon-1 trees and skips replicon 2). All 86 units clear the
script's 4-tip floor, so all 86 are testable.

**No `--assignments` file needs building.** The script reads the TSV with
`csv.DictReader` and touches only `sample_id`, `country` and `bioproject`, so
`L1v4c_MERGED_METADATA.tsv` satisfies the interface as-is (cols 1, 9, 12; plus
`subregion` 10, `collection_date` 13, `validation_label` 17). Verified: all 2,352
tips across the 86 trees join to `sample_id` **exactly, 100%** — no prefix
matching or relabelling needed. Pass the metadata file directly.

**Two corrections were made to the test itself on 2026-08-19. Both change what a
v4c re-run produces, so do not compare against pre-2026-08-19 output.**

*Single-country units.* Methods §2.12.9 used to say these were "tested instead
against the probability of drawing n genomes of one country at random from the
collection's own country distribution." The script never implemented that. Rather
than build a test nobody had validated, Methods was corrected to describe the
actual behaviour: such units emit `verdict = "uninformative: <2 distinct values"`
with an empty `p_value` and are excluded from the significant count. Under v4c
that is 38 of 86 units for `country` and 7 of 86 for `bioproject`. **If you want
the draw-probability test, it still needs writing** — it is a real gap, just no
longer a misdescribed one.

*The `unknown` BioProject bucket — this one mattered.* The metadata encodes
missing values inconsistently: `country` uses an empty cell, but `bioproject`
uses the **literal string `unknown` for 274 of the 2,352 analysed tips**. The
script's `or None` idiom only caught empty strings, so those 274 were scored as
one shared 274-member "study". That mis-measures the exact confounder this test
exists to detect, and measurement error in a confounder *understates* it —
biasing toward concluding the geographic signal is real. The script now
normalises a `MISSING` set to `None` for both fields. **This changes the
BioProject state count in 55 of 86 units (64%)**, so it is not a corner case.

### Results, run 2026-08-19

Both runs done at 1,000 permutations, seed 20260815, metadata passed directly:

| | A100 88 units (**use this**) | Track A 86 units (control) |
|---|---|---|
| output | `PHYLOGEOGRAPHY_ASSOCIATION_v4c_A100.tsv` | `PHYLOGEOGRAPHY_ASSOCIATION_v4c.tsv` |
| country testable / clustered | 49 / 26 | 48 / 26 |
| surviving BH-FDR 5% | 24 | 24 |
| **confounded (BioProject clusters too)** | **15** | 14 |
| single-country, untestable | 39 | 38 |

**The headline: 6 of 88 units carry a geographic signal that survives both
multiple-testing correction and a non-vacuous BioProject control** —
`strain_11_L1_5`, `strain_14_L1_4`, `strain_1_L1_28`, `strain_1_L1_5`,
`strain_2_L1_2`, `strain_5_L1_3`. All six are Southeast Asian. The two runs agree
on 6 of 7; the single discrepancy, `strain_1_L1_11`, is a genuine partition
difference (n=18 on the A100 vs 24 on Track A), not permutation noise.

**Every Americas unit fails, and this is the finding that bears on the applied
goal.** Do not read any of these as attribution evidence:

| unit | n | composition | verdict |
|---|---|---|---|
| `strain_4_L1_4` | 33 | all Americas, 10 countries (USA 13, Mexico 6, PR 5, …) | **confounded** — country p=0.0010 *and* BioProject p=0.0010 at 31/33 coverage, so this is well-powered, not data-poor |
| `strain_4_L1_3` | 39 | Brazil 31, Aruba 2, Guatemala 2 | **vacuous control** — country p=0.0010 but only 7/39 have a BioProject, so p_bp=1.0000 means nothing |
| `strain_4_L1_1` | 22 | USA 21 (all Mississippi), Colombia 1 | **untestable** — country p=1.0000, BioProject single-valued; descriptive only |
| `strain_4_L1_2` | 10 | Colombia 8, USA 2 | no country signal (p=0.0749) |
| `strain_22_L1_1` | 11 | USA 6, Viet Nam 5 | no country signal (p=0.0589) |

**Read `n_known` before trusting any "BioProject not clustered" verdict** — on
Track A, 4 of the 12 apparent passes had under 70% BioProject coverage or fewer
than 3 distinct values. A vacuous control is not a pass.

One metadata defect surfaced: a genome in `strain_4_L1_3` has the compound
country value `Panama and Peru`, which Fitch scores as its own distinct state.

---

## 4. Which tree to use — this matters and is easy to get wrong

| artifact | what it is | use for phylogeography? |
|---|---|---|
| `L1v4c_out/Clusters/*/Gubbins/*.node_labelled.final_tree.tre` | per-unit, recombination-corrected | **YES** — this is what the association test consumes |
| `L1v4c_out/global_ml_tree.treefile` | 86 tips = unit medoids, parsnp core | for context only; tips are units, not genomes |
| `L1v4c_out/global_grafted_chr1.treefile` | **2,352 tips = every analysed genome** | topology/membership only — see below |

**The grafted tree's branch lengths mix two scales** — measured on the tree
itself: backbone median **0.0325** over 170 edges (the parsnp core), within-unit
median **0.00063** over 4,455 edges (each unit's filtered variable sites), so the
two scales are **~52× apart**. Taking the median of the 86 per-unit medians
instead gives 44×. It is a topology and membership object. **Do not date it,
and do not read rates or cross-unit distances from it.** For display, collapse the
units in iTOL (package on Drive at `itol_grafted_chr1/`) so every visible edge is
a backbone edge on one scale.

All 86 units are monophyletic in the grafted tree — verified.

---

## 5. Two results already in hand that bear directly on this

**Australia is basal, and it is not an input.** The two longest terminal backbone
branches of 86 are the only two majority-Australia units:

    strain_9_L1_1   n=40, 92% Australia,  0.1494  rank 1/86
    strain_15_L1_1  n=31, 100% Australia, 0.1447  rank 2/86

This is consistent with an Australian origin with SE Asian populations derived,
and it reproduces an earlier independent observation. **But** GAP4 point 15
(body §8) is the essential counterweight: the Australian-origin hypothesis is
better supported than a naive bias critique implies *and still not established*
— Pearson 2009's conclusion is explicitly "contingent on an Australian root,"
and Chewapreecha's un-excluded alternative is repeated bottlenecks outside
Australia. GAP4 notes **no paper has re-examined this on sampling-bias grounds —
a genuine opening.**

**r/m is only valid inside the Gate 1 diversity window** (47 of 88 units, median
7.38). This does not constrain phylogeography — being outside the Gubbins window
is not disqualifying for trees or geography — but do not import r/m values into a
phylogeographic argument without checking the unit is in-window.

---

## 6. Metadata traps that will bite

- **`country` conflates US territories with the mainland.** Of 47 USA genomes in
  the analysed set: Mississippi 21, Texas 5, Georgia 5, **Puerto Rico 5, Virgin
  Islands 5**, Ohio 2, California 2, Arizona 1 (labelled `Arizona, Phoenix`),
  unknown 1. Any US-origin claim must disaggregate. Use `subregion` — but note
  that column is not purely a place: at least one row in the full metadata reads
  `Illinois ex Mexico`, i.e. it encodes exposure history. Parse it, don't group
  on it blindly.
- **Thailand share — quote the analysed set, and say which denominator.**
  Measured: **66.4% of the analysed 2,352** are Thailand; it is 58.9% of the
  2,976-row metadata file. Three documents used to disagree — this handoff's old
  "~60%", the script docstring's 70.5%, and GAP4's 59.6%. The first two are now
  corrected to 66.4%; **GAP4's 59.6% is left alone deliberately**, because GAP4
  is scoped to a different (5,515-genome) collection and is not wrong on its own
  terms. Concentration by study is real but smaller than "three BioProjects"
  implies: the top three account for **54.6%** of the analysed set, and the third
  is the literal string `unknown` (274 genomes), not a study — see §3, where that
  string turned out to be a live defect. The two genuine leaders are
  `PRJEB25606` (543) and `PRJEB35787` (468). This is still why BioProject must be
  tested alongside country, every time.
- **The CDC BioProject is a labelled validation set** — genomes with known
  exposure country. `validation_label` in the metadata. Score attribution
  **leave-one-out**; those genomes are in the panel, so naive scoring is circular.
- **Philippine genomes — resolved, no longer an open question.** The v4c panel
  has **12 Philippine genomes in the metadata and 11 in the analysed set**. The
  older "zero Philippine genomes against 11 Philippine cases" accounting is
  superseded. Beware the coincidence: 11 analysed genomes against 11 cases are
  different quantities that happen to share a number.
- `isolation_location` is populated for **681 of 2,976 metadata rows, but only
  168 of the 2,352 analysed (7.1%)** — the analysed-set figure is the one that
  governs any tree-based use. `IP-`/`IE-` prefixes are the internal Nakhon Phanom
  patient collection (not public).

---

## 7. Which run to analyse

**Use the A100 88-unit run for results** (`snp/Summaries/` in the Drive bundle
`wfsnps-v4c-results`): 88 units, 2,342 genomes, 176/176 replicon-units Tier1,
zero failures.

**Track A (86 units, 2,352 genomes) is the control**, and it is what is on this
workstation at `L1v4c_out/`.

**The A100 per-unit trees ARE on Drive** — an earlier version of this handoff said
they were not, and that was wrong. They are at
`wfsnps-v4c-results/snp/Clusters/`, one directory per replicon-unit, each with a
`Gubbins/` subdirectory. Pull just the trees with `rclone` (the `peerah-gdrive:`
remote is already configured on this workstation):

```
rclone copy peerah-gdrive:wfsnps-v4c-results/snp/Clusters A100_v4c_Clusters \
  --include "*/Gubbins/*.node_labelled.final_tree.tre" --transfers 8
```

That is 176 files, 2.2 MB, a few seconds. Verified on arrival: 88 unit-1 trees,
2,342 tips, 100% join to `sample_id`, 82 units membership-identical to Track A,
and the two extra unit names are `strain_1_L1_36` and `strain_1_L1_37`. The
directory layout is identical to `L1v4c_out/Clusters`, so
`--trees A100_v4c_Clusters` is a drop-in substitution.

The two runs agree to a median 0.38% on r/m across the 82 shared units, so Track A
is a legitimate basis for method development — but final numbers should come from
the 88-unit run.

---

## 8. Standing rules that have each already cost this project

- **A clean exit does not mean every unit succeeded.** `errorStrategy 'ignore'`.
  Compare units *requested* against units that produced output, every time.
- **Never compute a percentage against "seen so far."** Six appendix figures were
  once wrong this way.
- **Strain labels are not comparable between partition versions.** v4b `strain_4`
  (n=261) and v4c `strain_4` (n=104) share zero members — and that is not the
  exception: of the 27 strain labels present in both partitions, **24 share zero
  members**. Compare by *membership*, never label.
- **Check per-item values; never infer from a summary line.** Every serious defect
  in this project produced plausible output.
- **The grafted tree must not be dated** (§4).

---

## 9. Memory files to load

`crlf-refs-file-kills-snp-run-silently`, `rm-only-valid-inside-gate1-window`,
`v4c-workstation-run-validated`, `gubbins-zero-seed-raxml-failure`,
`parsnp-core-alignment-memory-ceiling`, `origin-attribution-is-the-applied-goal`,
`public-bp-genome-sampling-bias`, `country-column-hides-us-territories`,
`cdc-bioproject-is-a-labelled-validation-set`,
`v4-merge-puts-the-validation-set-in-the-panel`,
`global-tree-recovers-known-biogeography`,
`single-cluster-conclusions-are-provisional`, `partial-denominator-error`,
`l1v4b-partition-is-the-current-result`,
`gap4-has-two-colliding-numbering-schemes`

**Caution on `l1v4b-partition-is-the-current-result`:** its title no longer holds
— v4c supersedes v4b as the current partition. Load it for the *reasoning* about
how the partition was built, not for its claim of currency.

Located at
`~/.claude/projects/-home-phemarajata-Downloads-snp-mod-local-working/memory/`
(`MEMORY.md` is the index).

---

## 10. Suggested first moves

1. Read GAP4's "short version" (16 points) and Methods §2.12.9.
2. Pass `L1v4c_MERGED_METADATA.tsv` straight to `--assignments` — it already
   satisfies the script's interface and joins to every tip (§3). Build a derived
   file only if you want `subregion` substituted for `country` in the US split.
3. The association test is **already run** (§3, "Results") on both the A100 88
   units and Track A. Read those before re-running anything.
4. Only then consider `simmap` transition counts, with the sampling-corrected
   root prior and the phytools version caveat — and scope it to the 6 units that
   survived, not the 26 that merely have a significant country p-value.

The applied goal throughout is **origin-of-exposure attribution for US/Americas
cases without travel history** — not a global migration history. Keep claims
scoped to that, and to what the sampling can carry.
