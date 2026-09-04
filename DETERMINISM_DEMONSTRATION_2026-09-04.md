# Determinism demonstration: what the seed buys, and what it does not

2026-09-04. Closes Phase 1 item 4 of `PLAN_TO_SUBMISSION_2026-09-02.md`, and
corrects the claim that item was written to support.

**Headline.** `--seed` alone does **not** make Gubbins reproducible. Determinism
requires `--seed` **and** a single thread, and costs roughly 2x. The seed is still
required for a different reason: it removes the draw that silently loses a unit.

---

## Design

Ten units from the frozen basis, 8 to 9 taxa, whole-genome alignments of 31 to
36 MB. Each configuration run twice on the **same alignment** with the **same
pipeline code**, every run in its **own working directory** because Gubbins
writes scratch to the working directory regardless of `--prefix` and concurrent
runs sharing one collide.

Invocation matches production: `--first-tree-builder raxml --tree-builder raxml
--iterations 3 --min-snps 2 --invariant-site-correction --filter-percentage 25`,
Gubbins 3.4.3 from the pinned build.

A pair counts as identical only if **all four** scientific outputs match byte for
byte: `per_branch_statistics.csv` (the numerator and denominator of r/m),
`recombination_predictions.gff` (the called tracts),
`node_labelled.final_tree.tre`, and `filtered_polymorphic_sites.fasta`. Logs are
excluded; they carry timestamps.

## Result

| configuration | identical pairs |
|---|---|
| no seed, `--threads 4` | **4 / 10** |
| `--seed 20260904`, `--threads 4` | **5 / 10** |
| `--seed 20260904`, `--threads 1` | **10 / 10** |

**The seed on its own is worth one unit out of ten**, which is within noise of
doing nothing. The five units that agreed under a seed are the same five that
agreed without one: they are stable regardless, having little enough structure
that the search lands in the same place every time. Every unit that actually
varies run to run still varied with the seed set.

Single-threading closes it completely. The three units re-tested first were
chosen precisely because they had differed at four threads, and all three became
identical; extending to all ten gave 10 of 10.

### The per-unit digests, deterministic configuration

Ten distinct values across ten units, which is the sanity check that matters: an
earlier version of this experiment reported 10 of 10 identical because twenty
runs had failed and the comparison was hashing absent files, and the tell was the
*same* digest appearing for different units.

| unit | taxa | run A | run B |
|---|---|---|---|
| `strain_17_L1_2` | 8 | `81e5e07cc47f7c02` | `81e5e07cc47f7c02` |
| `strain_18_L1_2` | 9 | `2796cfc9f60c0a47` | `2796cfc9f60c0a47` |
| `strain_19_L1_3` | 9 | `aaadbc45519514bd` | `aaadbc45519514bd` |
| `strain_1_L1_14` | 9 | `f128163ca63fca65` | `f128163ca63fca65` |
| `strain_1_L1_31` | 8 | `ff9365911fbd1270` | `ff9365911fbd1270` |
| `strain_1_L1_4` | 8 | `e3b9146c711d5caf` | `e3b9146c711d5caf` |
| `strain_20_L1_1` | 8 | `1b1fb6b96eef9092` | `1b1fb6b96eef9092` |
| `strain_20_L1_2` | 9 | `cf3aed884ecae6b3` | `cf3aed884ecae6b3` |
| `strain_5_L1_1` | 8 | `c2abc0dfc26b569d` | `c2abc0dfc26b569d` |
| `strain_5_L1_4` | 8 | `656bceb45dca98d2` | `656bceb45dca98d2` |

All 40 runs in the first experiment and all 20 here exited 0.

## Cost

| taxa | 4 threads | 1 thread | ratio |
|---|---|---|---|
| 8 | 18 s | 23 s | 1.28x |
| 37 | 44 s | 87 s | 1.98x |

Units in this collection reach 159 taxa, so the ratio should be expected to grow
beyond 2x. The reported run took 6 h 37 m, so a fully deterministic re-run is
plausibly most of a day rather than a week. That is affordable for a
demonstration or a final archival run, and it is not something to impose on every
exploratory run.

## Why the seed is still mandatory

Determinism is not what the seed was added for. Without `--seed`, Gubbins takes
`gubbins/utils.py::set_seed` -> `str(randint(0, 10000))` and passes it to RAxML
as `-p`. That draw is 0 about 1 time in 10,001; RAxML rejects a non-positive
parsimony seed; and Gubbins reports the failure only as "Unable to fit model to
data". With `errorStrategy 'ignore'` the unit is dropped and the run still exits
0. Across a panel the chance of losing at least one unit is about 16%, and it was
observed on 2026-08-25 (`strain_1_L1_30`, iteration 5, `-p 0`; 171 units where
172 were expected).

So the two settings do different jobs, and both are needed:

- **`gubbins_seed`** removes a silent unit loss. Required always. Default set.
- **`gubbins_deterministic`** gives byte-reproducibility. Costs ~2x. Default off.

## This is the same finding as the IQ-TREE one

`A100_CFML_VALIDATION_2026-09-01.md` measured exactly this shape for IQ-TREE:
`-seed 12345 -T 4` twice gave two different trees, `-seed 999 -T 4` twice gave two
different trees, and `-seed 12345 -T 1` three times gave one identical tree. The
conclusion there was "`-seed` alone does not fix it; the fix is `-seed <N>`
together with `-T 1`".

The same is now measured for Gubbins and RAxML. **Multithreaded tree search in
this stack is non-deterministic regardless of seed**, because the parallel search
does not impose a deterministic reduction order. It should be assumed to hold for
any threaded tree builder here unless measured otherwise.

## What the manuscript may now claim

Not "deterministic by construction going forward". That was asserted before it
was measured, on the strength of a fix that did not exist, and it is false as
stated even now that the fix does exist.

What is supported:

1. The reported run reproduces **empirically**: Gate 1 = 47 units, median r/m
   7.70 (D1, `REPRO_RESULT_2026-08-26.md`).
2. ~~The pipeline is **deterministic when run single-threaded**, demonstrated at
   10 of 10 on real alignments, at a cost of roughly 2x.~~
   **Corrected later the same day. That was true of Gubbins and not of the
   pipeline.** `gubbins_deterministic` pinned Gubbins and nothing else. Every
   IQ-TREE call ran unseeded and multi-threaded, including the two that produce
   reported output. See the correction below. It is true now.
3. The reported run itself remains **not** seed-reproducible: it predates both
   parameters, and re-running produces a different run rather than validating the
   pinned one.

Three sentences, each measured. The previous single sentence implied more than
any of them.

## Reproduce

Harnesses are `seedtest/run.sh` (the 40-run seeded/unseeded comparison) and
`seedtest/det.sh` (the 20-run deterministic demonstration), both retained with
the scratch outputs. Pipeline support is
`wf-assembly-snps-mod@0543892` (`gubbins_seed`) and `@4fd7b22`
(`gubbins_deterministic`), PRs #6 and #7.

---

# Correction, later on 2026-09-04: the flag did not cover IQ-TREE

The section above ends by observing that multithreaded tree search in this stack
is non-deterministic regardless of seed, and that it "should be assumed to hold
for any threaded tree builder here unless measured otherwise". IQ-TREE is a
threaded tree builder here. It was measured, in the earlier work that section
cites. And `gubbins_deterministic` did not touch it.

So the demonstration above is a demonstration about Gubbins, and claim 2 read it
as a demonstration about the pipeline.

## What was actually running

Five IQ-TREE invocations, none seeded, all multi-threaded:

| module | what it produces |
|---|---|
| `IQTREE_ASC` | the per-unit final ML trees |
| `GLOBAL_ML_TREE` | the reported global ML tree, two invocations |
| `IQTREE_FAST` | the Gubbins starting tree |
| `BUILD_INTEGRATED_TREE` | integrated mode, `-nt AUTO`, sized to the host |

Two of those are reported output.

## Measured

Three real unit alignments, 24 to 34 taxa, two runs per configuration, the
production invocation (`GTR`, `-bb 1000 -alrt 1000`), treefile compared byte for
byte:

| configuration | result |
|---|---|
| no seed, `-T 4` (production) | differs on all three |
| `-seed`, `-T 4` | differs |
| no seed, `-T 1` | differs |
| **`-seed`, `-T 1`** | **identical on all three** |

Both are needed. That is a sharper result than Gubbins gave, where a seed at four
threads still matched on the units that were stable without one. Under `-seed`
with `-T 1` the only difference left anywhere is the `.iqtree` report's own
timestamp and its two runtime lines.

## Fixed

`wf-assembly-snps-mod` gains `iqtree_seed`, passed to every invocation always,
and `deterministic`, which pins Gubbins and IQ-TREE both.
`gubbins_deterministic` still works and either turns determinism on, so nothing
already written down breaks. CI asserts all five invocations are seeded and
thread-controlled and refuses if it finds fewer than five, which caught two
faulty versions of the check itself before either was trusted.

## What claim 2 should say

**The pipeline is deterministic under `--deterministic true`, which pins both
Gubbins and IQ-TREE to one thread and seeds both.** Gubbins was demonstrated at
10 of 10 units and IQ-TREE at 3 of 3 alignments. Neither was demonstrated
end to end through the workflow, and that test has not been run.

## Why this matters for the reproducibility test

Open item 4 of `HANDOFF_2026-09-04.md` was to run the end-to-end reproducibility
test, on the grounds that it was "now unblocked: the seeded, single-threaded
configuration exists". It did not exist. It exists now.

Had the test been run this morning it would have failed, and it would have failed
on the per-unit and global trees while Gubbins reproduced perfectly, which is a
confusing place to start debugging from. The cheap check came first for that
reason: four call sites, read in a few minutes, against a run measured in days.
