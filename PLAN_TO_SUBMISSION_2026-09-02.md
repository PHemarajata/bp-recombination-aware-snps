# Plan to submission

**2026-09-02.** Five phases, ordered by what blocks what. Phase 0 is today.

---

## First: the PR #4 numbers

`+23,431 / −9,123` looks alarming. It decomposes benignly:

| type | added | deleted |
|---|---|---|
| `.md` | 15,794 | **8,898** |
| `.py` | 6,805 | 27 |
| `.sh` | 774 | 99 |
| `.config` | 0 | 99 |

**98% of the deletions are prose**, and they are the deliberate document triage:
31 superseded handoffs, an obsolete `METHODS_DRAFT_2026-08-11.md`, old finishing
plans. Nothing is lost; git history holds all of it. Code deletions total **27
lines** of Python. The bilingual explainer that shows in the deletion list was
replaced by `WHAT_THE_ANALYSES_SHOW_2026-08-20_TH.md`.

The `○ CI` badge is neutral, not failing: **this repository has no CI configured
at all.** That is itself worth fixing (Phase 4).

**The one thing that matters when merging PR #4: use a merge commit, not
squash.** All three strategies are enabled on the repo. Squashing would collapse
88 commits into one and destroy exactly the provenance chain that makes the
corrections auditable. The commit titles are the record of which claim was
corrected when.

---

## Phase 0 — land the tree (today)

1. **Merge PR #4** with a merge commit.
2. **Rebase PR #3** onto the new `main`, then renumber it from
   `PR3_CORRECTIONS_2026-09-02.md`. Keep its engineering: the v1-default removal
   closes E0, and `test_phylogeography_bp.py` is the project's first test file.
3. Re-run PR #3's own driver against the frozen basis, which is what it was built
   to do and could never do in its own container.

**Exit criterion:** `main` is current, and a fresh clone plus the untracked data
reproduces `NUMBERS.tsv`.

---

## Phase 1 — reproducibility by construction

Today the pipeline is reproducible *in practice* and not *by construction*. Close
that gap, and be precise about what it can and cannot retroactively buy.

1. **`-seed <N>` and `-T 1`** at `clonalframe_nu_bp.py:249`. `-seed` alone is
   insufficient: measured, multithreaded IQ-TREE gives a different tree every run
   at a fixed seed, and single-threaded gives one identical tree across three.
2. **E1**: `gate1_from_alignment_bp.py` defaults `--mash` to an 86-unit partition
   file. Same class as E0.
3. **E4**: `recomb_filtered_distances_bp.py` hardcodes the reported r/m table at
   line 209, so running it on any other run silently mixes bases.
4. **Then** the reproducibility test that has been waiting on a Methods freeze.

**State the limit honestly in the Methods.** The reported run is pinned at
`79ab645` and is not seed-reproducible. The claim that survives is two-part, and
**only one half is currently evidenced**: the reported run reproduces empirically
(D1: Gate 1 = 47 units, median 7.70). The second half, that the pipeline is
deterministic going forward once seeded, **cannot be asserted yet** — see below.

> **⚠ Corrected 2026-09-04.** This passage previously said the pin "predates the
> `gubbins_seed` fix". **There is no such fix.** Verified against the pipeline
> repository: no `gubbins_seed` parameter, no commit adding one on any branch, and
> the string `seed` has never appeared in a Gubbins module. PR #5, which landed on
> the date the fix was attributed to, pins CSV line terminators and drains a pipe.
>
> **Gubbins 3.4.3 does expose `--seed`, and this pipeline never passes it.** So
> the zero-seed failure is live in current code, and the seeded configuration this
> plan depends on does not exist. Phase 1 therefore gains a step 0, before
> everything else in it:
>
> **0. Add a `gubbins_seed` parameter and pass `--seed` at all three
> `run_gubbins.py` call sites in `modules/local/gubbins_cluster/main.nf`.** One
> parameter, three lines. Until it is done, steps 1 to 4 below cannot be completed
> and no determinism claim may be made.

**Cheap, high-value, and blocked on step 0:** run ten units twice under the seeded
configuration and show
byte-identical output. Hours, not days. That converts "should be deterministic"
into a measurement.

---

## Phase 2 — close the remaining uncertainty

Four open questions, none of which blocks drafting but all of which a reviewer
can reach.

1. **The four CFML pairing units.** `strain_1_L1_26`, `strain_1_L1_22`,
   `strain_1_L1_11`, `strain_27_L1_1` pair a Gubbins r/m from the control run
   against a ClonalFrameML value computed on workstation alignments. Decide:
   drop the four rows (defensible, costs two in-window units) or re-run CFML on
   the control's own alignments (correct, needs ~1.5 GB off A100 scratch and CFML
   time). **Recommend dropping**, and saying so.
2. **The Gate 1 coverage caveat.** `NUMBERS.tsv` carries
   `rm.gate1_caveat`: union coverage does not reproduce the calibration's 76–88%
   band. The floor does not depend on it, but the coverage criterion does not
   reproduce quantitatively. This must be disclosed, not resolved by argument.
3. **The geography scope decision.** The defensible claim is **6 units** passing
   the BioProject control, not 37 single-country units. This is the decision that
   determines whether Paper 2 exists in its current form. Make it before drafting.
4. **Determinism of the reported run** is not recoverable. Say so once, plainly.

---

## Phase 3 — figures and analysis presentation

Only **Figure 1 of 3** exists.

| figure | status | action |
|---|---|---|
| **1. Study flow** | ✅ `FIGURE1_STUDY_FLOW.svg` | none. `make_figure1_bp.py` reads `NUMBERS.tsv` and **exits non-zero on a missing key**, so it cannot ship with a hole |
| **2. Gate 1 window** | ❌ not built | r/m against mean pairwise core SNPs, log x, window shaded, three Gate 1 classes. **85 units, not 88** |
| **3. Global ML tree** | ❌ not built | over unit medoids. **85 medoids, not 88** |

**Extend the Figure 1 pattern to every figure and table**: read from
`NUMBERS.tsv`, fail loudly on a missing key. That is the mechanism that makes a
stale number impossible rather than merely unlikely, and it already exists and
works.

Every table in the draft should be regenerated the same way and diffed against
`NUMBERS.tsv` before it goes near a manuscript.

---

## Phase 4 — tidying against misuse and misunderstanding

The failure mode this project keeps hitting is not a wrong calculation. It is a
right calculation on the wrong basis. Four defenses, in order of value:

1. **Add CI.** There is none. Two jobs, both of which run without data:
   `test_phylogeography_bp.py` (32 checks, arrived in PR #3) and a syntax/import
   pass. Add `freeze_basis_bp.py` as a third where the data exists.
2. **Make the traps unreachable, not merely documented.** The recurring ones are
   globbing `L1v4c_out/Clusters` (hybrid, 88 dirs), joining the panel on
   `subcluster` rather than `unit_membership`, and quoting an all-unit r/m median.
   E0/E1/E4 are the same bug three times: a dangerous default. Audit every script
   for defaults that point at a partition or a run.
3. **Keep `STATE_2026-09-02.md` current**, and make it the first thing any new
   session reads. The PR #3 episode is the argument for it.
4. **`.gitignore` stays deny-by-default.** It held through this week's work: 3.3
   MB tracked, 200 files, zero data files. Do not loosen it; the verification
   commands are written into its own header.

---

## Phase 5 — build the manuscript

**Build every number from `NUMBERS.tsv`.** It already annotates itself
`QUOTE THIS` and `DO NOT QUOTE`, and those markers encode real distinctions
(7.70 in-window against 5.51 all-unit, which averages measurements with detection
failures).

The three-paper split is sound in shape:

- **Paper 1, calibration and measurement.** The operating range, the validation
  suite, both failure modes, r/m **7.70**, reproducibility. Cut geography
  entirely: the argument does not depend on sampling, so including it invites an
  attack on a 67%-Thailand frame that is otherwise irrelevant. Needs no analysis
  that has not been run. Target *Microbial Genomics*.
- **Paper 2, geographic structure.** Blocked on the Phase 2 scope decision. At
  six control-passing units it is a materially thinner paper than previously
  scoped, and that should be decided deliberately rather than discovered in
  review.
- **Paper 3, exposure-origin attribution.** Closest to the mission, furthest out.
  Needs the Mississippi and Mexico units to cross the size threshold and a
  cross-validated misclassification rate. That last is genuinely unclaimed
  territory.

**Run the non-science chain in parallel, because it is longer than the writing.**

- **C1, the IRB number.** The hardest-blocked item in the project. Start now.
- **B1 to B6**, deposition, chains off a BioProject registration. B1 is the head
  and nothing else in B moves until it lands.
- **A1**, the Zenodo archive and DOI. Include `control_pipeline_info/`, which
  exists only here and on unbacked-up A100 scratch.
- **The data availability statement is the highest-risk item in the project**,
  given Select Agent status and re-identifiable metadata. Settle it with
  biosafety and legal **before** choosing a journal, not after a desk rejection.

---

## Critical path

```
PR #4 merge ──► PR #3 rebase ──► seed fix ──► figures 2 and 3 ──► Paper 1 draft
                     │
                     └──► geography scope decision ──► Paper 2 exists or not

IRB (C1) ──────────────────────────────────────────────► submission
BioProject (B1) ──► deposition (B2-B5) ────────────────►
biosafety/legal ──► data availability ──► journal choice
```

The science is not the critical path. **C1 and the data availability statement
are.** Everything in Phases 0 to 3 is work we control and can finish; those two
depend on people outside this repository, so they should be started first even
though they appear last in the writing.
