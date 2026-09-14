# Risk register

Errors this project made, what produced them, what each would have cost if it had
survived, and how it is prevented now. Then the risks that are still live.

**Why this is the first document in the package.** A methods section tells you what
was done. It does not tell you how often the analysis was wrong on the way, which is
the only evidence available about how much to trust the version you are reading.
Every entry below is documented in the repository with its own record, named in the
last row, so nothing here rests on this summary.

The pattern worth noticing before the list: **almost none of these produced an error
message.** They produced a plausible number. That is why the remedies that matter are
the ones that make a class of error impossible rather than the ones that fix an
instance.

---

## Part 1 — Errors made and caught

### A. Counting before the run finished

| | |
|---|---|
| **What** | A figure was read off a denominator that was still filling, and recorded as final. |
| **Instances** | Seven, the most recent on 2026-09-04. |
| **Worst case** | The zero-recombination null was recorded as 1,302 replicates over 54 unit-replicons. The completed run is **1,519 over 62**. Separation between observed r/m and the null is 427x to 2,234x on the finished run, 434x to 2,131x on the partial one. Both support the conclusion, so the error was invisible in the verdict and visible only in the denominator. |
| **How it recurred** | The stale intermediate (`TIER2_null.txt`) is still on disk and still looks authoritative. On 2026-09-04 a figure was generated from it and reported the *manuscript* as being in error when the manuscript was right. |
| **Prevented by** | `make_figure5_bp.py` now takes the completed-run values as constants, refuses to run if their ratio stops matching 427x-2,234x, and warns that the snapshot must not be summarised. |
| **Record** | `REVISED_STRATEGY_2026-08.md` A.11ag addendum: *"THE COUNTS BELOW ARE STALE; THE VERDICT IS NOT ... do not record a count until the run that produces it has stopped."* |

### B. Two runs, and the wrong one designated as production

| | |
|---|---|
| **What** | The 88-unit A100 run was called production and the 85-unit workstation run the control. That designation was reversed. |
| **Cost if it had survived** | Every headline number moves. r/m is 7.44 on one and 7.70 on the other; the all-unit median is 5.70 against 5.51. Both are real measurements of something, which is what makes them dangerous: a value from the wrong run reads as a rounding discrepancy rather than a different analysis. |
| **Residual risk** | Documents written before the reversal may still carry old labels below a corrected banner. `GATE1_ALIGNMENT_RESULT_2026-08-21.md` carries an explicit reading note that its body uses the old labels while its tables are correct. |
| **Prevented by** | `NUMBERS.tsv` is the single source for quantities; figure and table generators read from it and fail on a missing key. |
| **Record** | `RUN_DESIGNATION_CORRECTION_2026-08-23.md`, `TRACK_A_VS_A100_COMPARISON.md` |

### C. Comparing a number in one unit system to a bound in another

| | |
|---|---|
| **What** | The Gate 1 diversity window was calibrated in `ska distance` units and applied to alignment distances without translation. |
| **Cost** | The floor was placed at 1,270 when in alignment units it is near 700. The untranslated bound reclassified 22 of 85 units, pushed units with r/m up to 12.28 below a floor whose premise is that detection fails there, and produced an in-window median of 8.05 instead of 7.70. |
| **It recurred, twice** | Table 3 of the manuscript still reported the Mash approximation against the alignment-derived floor as of 2026-09-03. And on 2026-09-04 the reviewer of that table compared 955 Mash SNPs to a 700 alignment floor and concluded a Results section had reversed, which it had not. |
| **Prevented by** | The window is stated in alignment units with its bracket in `NUMBERS.tsv`; the ska-unit bounds are recorded as the original calibration. **No mechanical check exists for this class. This is the residual risk most worth your attention.** |
| **Record** | `GATE1_ALIGNMENT_RESULT_2026-08-21.md` |

### D. Argument defaults pointing at a specific run

| | |
|---|---|
| **What** | `argparse` defaults hard-coded to a particular partition or run directory, so a script run without arguments silently analysed the wrong thing. |
| **Instances** | Six. |
| **Worst case** | One bounds pair served two different metrics, so default arguments returned 39 units at r/m 8.05 instead of 47 at 7.70. That would have gone into the manuscript. |
| **Prevented by** | `audit_defaults_bp.py`, in CI, fails the build if any `argparse` default matches a path-like pattern. The class is closed, not the six instances. |
| **Record** | `repository/audit_defaults_bp.py`; CI job *no input defaults to a specific run* |

### E. Concurrent tool runs colliding in the working directory

| | |
|---|---|
| **What** | Gubbins writes scratch to the current working directory regardless of `--prefix`. Concurrent runs overwrote each other. |
| **Cost** | Three wrong conclusions drawn before the cause was found, and the failure presented as a problem with the input rather than the invocation. |
| **Prevented by** | Every concurrent run gets its own working directory, recorded as a general pipeline rule rather than a Gubbins note. |
| **Record** | `REVISED_STRATEGY_2026-08.md` |

### F. A crash misdiagnosed as a biological property

| | |
|---|---|
| **What** | RAxML segfaults when its run identifier reaches 128 characters. Gubbins reports this as a failure to fit a model to the data. |
| **Cost** | Diagnosed for an entire investigation as "bad reference genomes" — a biological explanation for a string-length bug. It would have destroyed 42 of 172 replicon-units in this partition. |
| **Record** | `METHODS_DRAFT_2026-08-19.md`; reported in the manuscript as a finding for the field |

### G. The mapping reference left in the tree

| | |
|---|---|
| **What** | Retaining the mapping reference as a tree tip puts population-to-outgroup divergence into the denominator of r/m. |
| **Cost** | Moved a median from 1.85 to 6.30 in an earlier partition, the difference between reporting a moderately and a strongly recombinogenic organism. 52% of outside-recombination SNPs were the outgroup's branch. |
| **Found by** | Sorting per-branch values and seeing one branch hold 96% of the signal. A correlation analysis attempted first found nothing. |
| **Record** | `METHODS_DRAFT_2026-08-19.md`; reported in the manuscript |

### H. Unseeded stochastic tools

| | |
|---|---|
| **What** | Gubbins called RAxML with an unseeded `randint(0, 10000)`, which hits 0 roughly once in 10,001 and fails. IQ-TREE was likewise unseeded. |
| **Cost** | About a 16% chance of silently losing a unit per full run. The unseeded IQ-TREE call accounted for 100% of run-to-run variation between otherwise identical executions. |
| **Status, IQ-TREE** | **Fixed.** `clonalframe_nu_bp.py` sets `-seed` *and* `-T 1`; measured, `-seed` alone is insufficient because multithreaded IQ-TREE gives a different tree per run at a fixed seed. |
| **Status, Gubbins** | ⚠ **NOT fixed. See entry Q.** This row previously said the reported run "predates the seed fix" and that determinism by construction was evidenced going forward. Both were false: no Gubbins seed fix exists, and the failure is live in current code. |
| **Record** | `PRODUCTION_RUN_PIN_2026-08-24.md`, `REPRO_RUN_2026-08-24.md`, and **entry Q below** |

### I. A filter applied twice

| | |
|---|---|
| **What** | `min_cluster_size` was applied at two stages. |
| **Cost** | 26% of the collection discarded, biased hard against rare lineages: 74% of Australian and 51% of Americas genomes lost. **That bias runs in the same direction as the study's geographic question.** |
| **Prevented by** | Partition v2 onward merges rather than deletes; the current basis discards nothing at that step. |
| **Record** | `REDO_DECISION_2026-08-21.md` |

### J. Two estimators reported as one number

| | |
|---|---|
| **What** | Attribution accuracy depends on the estimator, and two tables report different ones. `CGMLST_LICHT_ATTRIBUTION.tsv` is nearest-neighbour throughout and gives region as 37/46; the reported 41/46 is the modal vote over k=20. |
| **Cost if mixed** | The two disagree on six of the 46 genomes. Quoting one figure with the other's stratification would produce a coherent-looking table that measures nothing. |
| **Prevented by** | The estimator is part of every key name in `NUMBERS.tsv`, precisely so the comparison cannot be made by accident. `make_figure_attribution_bp.py` asserts each grouping is drawn at its best estimator by kappa and exits otherwise. |
| **Record** | `NUMBERS.tsv` key `attribution.NOTE_estimator` |

### K. A directory holding two partitions at once

| | |
|---|---|
| **What** | An output directory contained unit directories from two runs, 88 where the partition has 86. |
| **Cost** | Globbing it double-counted 153 genomes and corrupted two summary tables. A related defect gives a split child its unsplit parent's diversity, 1,310 instead of its own 72, when joined by unit name. |
| **Residual** | That 72 cannot be read from any file in `evidence/` and is a documented constant in the table generator. **If you doubt one number in this package, doubt that one first.** |
| **Record** | `GATE1_ALIGNMENT_RESULT_2026-08-21.md` section 7b |

### L. Validation leaking through near-identical genomes

| | |
|---|---|
| **What** | Scoring a validation genome against its own outbreak siblings, which sit within 0.005 allelic distance. |
| **Cost** | Would have scored the Mississippi cases correct by matching them to each other, inflating attribution accuracy on exactly the cases the study is about. |
| **Prevented by** | Leave-outbreak-out, with outbreak groups as an explicit register rather than an automatic same-BioProject rule. |
| **Record** | `LEAVE_OUTBREAK_OUT_2026-08-23.md` |

### M. Controlling for a descendant of the exposure

| | |
|---|---|
| **What** | The BioProject was used as a confounder control for geographic signal. |
| **Cost** | It is not a confounder: country causes BioProject rather than the reverse, with 113 of 119 BioProjects entirely single-country. Conditioning on it is over-adjustment and removes real signal. The retained-unit count runs from 6 to 24 by specification, and no endpoint is defensible alone. |
| **Resolved by** | Reporting the range with its mechanism instead of a point estimate, and stating that country and collection history are not separable in a collection assembled this way. |
| **Record** | `BIOPROJECT_COUNTERFACTUAL_2026-09-02.md`, `CONTROL_SPECIFICATION_2026-09-02.md` |

### N. Building on a stale branch

| | |
|---|---|
| **What** | Work proceeded on a tree 89 commits and two weeks behind main, without fetching. |
| **Cost** | A manuscript whose headline r/m was correct for the visible tree and wrong for the real one. |
| **Prevented by** | Fetch before starting; current state pinned in `STATE_2026-09-02.md`. |
| **Record** | `PR3_CORRECTIONS_2026-09-02.md` |

### O. Citations that resolve and are still wrong

| | |
|---|---|
| **What** | A drafted background carried 130 citations, of which 34 pointed at entries outside the reference list, and five entries share a fabrication signature: DOI prefix `10.60692`, no journal, year 2024, and **a title that paraphrases the sentence citing it**. |
| **Worse than fabrication** | Three sentences cite real papers for claims those papers do not make. One attributes transatlantic-slave-trade timing to a study proposing Austronesian migration; one attributes a phylogeographic assignment to an author whose five relevant papers are all within-host evolution studies. **A resolving DOI and a topic-matching title are not verification.** |
| **Prevented by** | `verify_references_bp.py`, in CI, which also detects reference entries sitting outside the reference list. It cannot detect a real paper cited for the wrong claim; that pass is manual and recorded in `REFERENCES_RESOLVED_2026-09-03.md`. |
| **Record** | `HANDOFF_CITATIONS_2026-09-03.md`, `REFERENCES_RESOLVED_2026-09-03.md` |

### P. Two sessions editing one branch

| | |
|---|---|
| **What** | Two analysis sessions worked the same branch concurrently, one without access to the data. |
| **Cost** | The data-free session correctly propagated a documented correction into Results section 2 but could not check Table 3 against the partition, leaving the manuscript stating a floor of 700 in one section and marking a unit at 955 as below floor in another. Only the session with the data could catch it. |
| **Rule adopted** | The workstation owns every number; the data-free session owns citations, cross-document consistency and tooling. One branch, one writer. |
| **Record** | `HANDOFF_CITATIONS_2026-09-03.md` section 10 |

### Q. A fix recorded as done that was never made

| | |
|---|---|
| **What** | Six documents recorded a `gubbins_seed` fix as an accomplished fact dated 2026-08-19, and used it to bound a reproducibility limitation to the pinned commit. **No such fix exists**, on any branch, at any time. |
| **How it was established** | `git log --all -S'seed' -- 'modules/local/*gubbins*'` returns empty: the string has never appeared in a Gubbins module in the repository's history. `conf/params.config` defines eight `gubbins_*` parameters and none is a seed. None of the three `run_gubbins.py` call sites passes one. |
| **Where the belief came from** | Something did land on 2026-08-19: pull request #5, pinning CSV line terminators and draining a pipe. The date was right and the content was not. |
| **Cost** | The manuscript's forward-looking reproducibility claim, that the pipeline is deterministic by construction going forward, was **not true**. The zero-seed failure, roughly a 16% chance per panel of silently dropping a unit while exiting 0, is **live in current code** rather than confined to the reported run. A reproduction run on 2026-08-25 hit it and the observation was filed as evidence about an old commit. |
| **Why it is worse than an ordinary error** | Gubbins 3.4.3 **does** expose `--seed`; `gubbins/utils.py::set_seed` falls back to `str(randint(0, 10000))` only when none is given. So this was never an upstream limitation to be lived with. It was a one-parameter omission, reported as closed for weeks. |
| **Status** | **Closed 2026-09-04.** Documentation corrected in all six places, mechanism text left intact because it was always right. The code fix is `gubbins_seed` (PR #6), and measuring it produced a second correction: **`--seed` alone is not determinism.** Ten units, two runs each, gave 5/10 byte-identical with a seed against 4/10 without, and 10/10 only at `--threads 1`. So `gubbins_deterministic` (PR #7) exists as well, and both Gubbins paths are wired (PR #8), including the classic one that produced no reported result. Released as `v1.1.0-mod`. |
| **Not correctable** | The annotated tag `v1.0.5-mod` carries the false claim in its own message. Retagging a published release to fix prose is worse than leaving it; `DATA_AVAILABILITY_2026-08-24.md` now holds the correction of record. |
| **Record** | `METHODS_DRAFT_2026-08-19.md` §2.12, `STATE_2026-09-02.md`, `PLAN_TO_SUBMISSION_2026-09-02.md` Phase 1 |

**Read this entry as the one that most limits what the rest of the register can
promise.** Every other entry describes an error found by checking a number against
data. This one was found by checking a *claim about the code* against the code, and
it had survived six documents and several weeks. Nothing in the tooling would have
caught it: the pipeline repository had no CI at all, and no check anywhere verified
that a documented fix existed.

**That gap is now closed, and the closing is worth auditing too.** The pipeline
repository has CI as of `v1.1.0-mod`, and one job asserts that no `run_gubbins.py`
call site omits a seed. The check was written wrong twice before it was right, and
**both wrong versions passed the positive test**: the first used a line window wide
enough to see an adjacent call site's seed, and the second matched a single trailing
backslash where the Groovy script block emits two, so it found zero call sites and
passed over an empty set. It is now scoped to the command block and asserts a
minimum count, because an assertion over an empty set is not an assertion. It was
verified by deleting a seed and confirming the job fails. A reviewer should treat
"we added a check" with the same suspicion as "we made a fix", and this entry is the
reason why.

---

## Part 2 — Live risks, not resolved

Disclosed in the manuscript, and where an independent assessment is most useful.

**1. The Gate 1 floor rests on a bracket, and on a criterion that does not fully
reproduce.** The window was located on union recombination coverage and median tract
length rather than on r/m, deliberately, so the bounds are not chosen to flatter the
result. But union coverage never reaches the original calibration's stated 76-88%
band anywhere in this panel: the maximum band median is 68%, and coverage *rises*
with diversity, peaking in the bands the gate rejects. The floor does not depend on
that criterion, being located by a 4.3% to 28.0% jump far from the range in question.
The discrepancy is nonetheless unexplained. Treat the window as calibrated on one
dataset and re-verifiable, not as a species constant.

**2. The floor is insensitive but not determined.** Putting it at 588, 700, 755 or 840
gives in-window medians of 7.70, 7.70, 7.74 and 7.78, so the answer does not depend on
the judgement call. The bracket is still a bracket, and only three units sit below it:
the evidence for the floor is thinner than the evidence for the ceiling.

**3. Attribution rests on 46 genomes and five regions, two with n = 2.** All five
regional errors fall in those two. That is a sampling statement with a named remedy,
not an accuracy ceiling, but the regional estimate is well determined for three
regions and barely constrained for the others.

**4. The modal estimator collapses the output space.** It emits only three of the seven
regions. North America and Sub-Saharan Africa are unreachable rather than merely wrong,
and a confusion matrix restricted to observed columns hides this entirely.

**5. Abstention cannot reach the errors that matter.** Confidence does not separate
errors from successes: correct calls have a median vote share of 0.85 and the errors
reach 0.85. Distance-based abstention declines three of five errors and cannot decline
the two with a genuine close relative.

**6. The panel is roughly two thirds one country.** Thailand is 66.7% of the analysed
set. The country baseline of 26% and the regional baseline of 46% are each set by a
single dominant class. No amount of analysis repairs a sampling frame.

**7. RESOLVED 2026-09-04. The Gubbins zero-seed failure is fixed, and the
reproducibility claim is now two clauses rather than one.** See H and Q. `--seed` is
passed at every call site as of `v1.1.0-mod`, so new runs no longer carry the ~16%
per-panel chance of silently dropping a unit. What remains true, and must be stated
in the Methods rather than quietly dropped:

  - **The reported analysis is still not seed-reproducible.** It is pinned at
    `v1.0.5-mod` / `79ab645`, which predates both parameters. Re-running it under
    them produces a different run, not a validation of the pinned one. This is not
    recoverable.
  - **A seed alone would not have bought determinism anyway.** Measured: 5/10
    byte-identical with a seed at 4 threads against 4/10 without, and 10/10 only at
    `--threads 1`. The five that agreed under a seed are the same five that agreed
    without one. Thread count dominates, so determinism is opt-in via
    `gubbins_deterministic` and costs roughly 2x. Assume any threaded tree builder
    in this stack is non-deterministic regardless of seed unless measured; the same
    was independently true of IQ-TREE.

**9. The pipeline config does not parse on Nextflow 26.x.** Found by CI on its first
run: 26.x ships a strict config parser that rejects the `check_max` function
definition in `nextflow.config`, so `nextflow config .` fails outright. `check_max`
is the nf-core resource-capping helper used throughout the profile blocks, so
removing it changes how every profile computes its resource ceilings, and those
ceilings are already known to be sized for small units (see the profile-ceiling
note). Nothing has been run on 26.x and nothing should be until this is fixed.
Verified working on 24.10.5, 25.04.6 and 25.10.0; CI tests the latter two, which are
the versions behind the reported run and the cross-hardware control.

**8. A reproducibility test after the methods freeze has not been run.** Too many
intermediates were edited in place on 2026-08-21 and 22 for an end-to-end rerun to be
meaningful before the freeze. It remains outstanding.

---

## Part 3 — What the pattern says

Seventeen entries, in three shapes.

**Silent wrong answers, not crashes.** Only two of the sixteen produced an error
message. The rest produced a number that looked reasonable. Any remedy relying on
someone noticing that something looks odd has already failed for this class.

**One entry is not like the others.** Q is not a wrong number; it is a claim about the code that was false, and it survived six documents because nothing checks documentation against the thing it describes. Weigh the other sixteen accordingly: they were caught because numbers can be recomputed.

**Denominator and unit-system confusion is the dominant mode.** A, B, C, I, J and K are
the same shape: two things that are legitimately different were treated as the same, or
one was silently substituted for the other. This is why so much of the tooling exists to
make a quantity carry its basis, its units and its estimator in its own name.

**The remedies that held closed a class.** The three that have not recurred are the ones
turned into a mechanical check: `audit_defaults_bp.py`, `verify_references_bp.py`, and
generators that fail on a missing `NUMBERS.tsv` key. The ones that recurred — C most
notably, twice — are the ones where the remedy was a document saying to be careful.
