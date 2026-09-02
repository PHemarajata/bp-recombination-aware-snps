# PR #3 review: the code is good, the numbers are from a stale tree

**2026-09-02.** Reviewed against the data, which the authoring session did not have.

---

## 1. Root cause, and it is not carelessness

`origin/main` is at `32a08a4`, dated **2026-08-19**. The working branch
`feat/core-shrinkage-and-itol` is **85 commits ahead of it**, tip dated
2026-08-28, and **26 of those commits have never been pushed anywhere**.

PR #3 was branched from `main`. In that tree:

- `FINAL_BASIS_2026-08-22/` does not exist
- `RUN_DESIGNATION_CORRECTION_2026-08-23.md` does not exist
- the A100 88-unit run is still called **production**
- r/m **7.38** is still the current number

So the manuscript's numbers are correct *for the tree the session could see*. It
reproduced the 2026-08-19 world faithfully. Every discrepancy below follows from
that one fact, and **any future session branched from `main` will reproduce them
again**.

Two consequences worth separating:

1. **`main` is two weeks stale.** Until it is updated, it is an active trap.
2. **26 commits exist only on this workstation.** That includes `402c20b`, the
   run-designation correction itself. A disk failure loses the freeze, the
   corrections, and the validation work.

---

## 2. Numbers to correct

The Gate 1 table (PR draft §3, lines 293-295). Every cell moves except the
in-window count, which coincidentally matches:

| stratum | PR draft (88-unit A100) | frozen basis (85-unit) |
|---|---|---|
| In-window | 47, r/m **7.38** | 47, r/m **7.70** |
| Below floor | 9, r/m 1.67 | **12**, r/m **1.32** |
| Above ceiling | 32, r/m 2.48 | **26**, r/m **2.14** |
| total units | 88 | **85** |

Other claims:

| PR draft says | should be |
|---|---|
| "a production run of 88 units and 2,342 genomes" | the **control**; the reported run is **85 units, 2,340 genomes** |
| "r/m 7.38" (headline, ×4 places) | **7.70** |
| "47 of 88 units" | **47 of 85** |
| "82 units of identical membership" | 82 is the shared-unit count, not the basis; the basis is **85** |
| "median absolute difference ... across 82 units" | **0.36% median relative**, membership-matched |

The frozen-basis README is explicit that 7.38 is one of the numbers *not* to
publish: "Not 7.44 (that is the A100 run), not 7.38 (A100 under the Mash proxy),
not 7.26 (this basis under the Mash proxy)."

---

## 3. The geography headline does not survive contact with the data

The draft's "42 of 82 units contain a single country where chance would give 2"
is wrong in both terms and, more importantly, **misreads what the category is**.

Computed on the frozen basis from `PHYLOGEOGRAPHY_ASSOCIATION_FROZEN_2026-08-23.tsv`:

| | |
|---|---|
| single-country units | **37 of 85**, not 42 of 82 |
| expected under a random-draw null | **0.94**, not 2 |
| exact Poisson-binomial P(X>=37) | 4.1e-64 |

But the significance is not the point, because **the 37 single-country units are
the untestable stratum**. The frozen table classifies them
`uninformative: <2 distinct values` / `untestable: single-valued`. They are units
where the association test cannot run, not units where geography was shown.

The full country breakdown of those 85 units:

| interpretation | units |
|---|---|
| untestable: single-valued | 37 |
| null | 25 |
| confounded (BioProject) | 12 |
| **geographic (control passes)** | **6** |
| vacuous control | 5 |

**The defensible geographic claim is 6 units, not 42.** Those six are
`strain_11_L1_5`, `strain_1_L1_11`, `strain_1_L1_28`, `strain_1_L1_5`,
`strain_2_L1_2`, `strain_5_L1_3`, all with full country knowledge and q < 0.03.

Two further findings, pulling in opposite directions:

- **For the single-country observation:** only **3 of 37** are also
  single-BioProject, so 34 draw on 2 to 4 independent submitters and yet contain
  one country. That is not a single-submitter artifact.
- **Against it:** **30 of 37 are Thailand** (81%), against Thailand being 67% of
  the collection. Only **7** single-country units are non-Thailand. The
  observation is largely a restatement of the sampling frame.

A random-draw null was always going to reject here, since units are defined by
genetic similarity and geography tracks phylogeny for legitimate reasons. The
BioProject control is the test that carries information, and it is already
implemented and already run.

---

## 4. What is good in the PR, and should be kept

- Removing the v1 defaults from `--assignments` and `--trees`, and the preflight
  that aborts on a basis mismatch. This closes **SUBMISSION_TODO E0**.
- The same fix in `exclude_reference_branches_bp.py`.
- `test_phylogeography_bp.py`, the project's first test file, 32 checks that run
  without data. It caught a real regression during authoring.
- `manuscript_numbers_bp.py` refusing to print an all-unit r/m median when the
  diversity input is missing.

The publication strategy is sound in shape. Paper 1 is not "80% done" at the
number level, but the correction is mechanical rather than analytical: the
analyses have all been run, on the frozen basis, and the values above are the
ones to drop in.

Note also **SUBMISSION_TODO E1** is still open and is the same class of bug:
`gate1_from_alignment_bp.py` defaults `--mash` to `trackA_diversity_86units.tsv`,
an older partition.

---

## 5. Recommended order

1. **Push the 26 local commits.** They are the only copy.
2. **Bring `main` up to date**, or the trap fires again on the next session.
3. Rebase PR #3 on the current tree and re-run its own driver against the frozen
   basis, which is what it was built to do.
4. Apply §2 and §3 to the draft.
