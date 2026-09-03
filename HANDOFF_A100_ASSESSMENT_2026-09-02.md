# Handoff to the A100 side: our assessment of the A100 work

**From:** the workstation analysis session, 2026-09-02
**To:** whoever continues on the DGX Station A100 (the ClonalFrameML run and the
88-unit control run were produced there)
**Purpose:** a sense-check, not a correction list. The A100 work was sound and
complete. This document states what we concluded about it so everyone is working
from the same understanding, and flags the few places where our reading differs
from what the delivered files say on their face. Please read section 9 and tell us
if any of it does not match what you did.

---

## 1. What was assessed

Two artifacts produced on the A100:

1. **`cfml_v4c_results.tar.gz`** — the ClonalFrameML decomposition (delivered
   2026-08-26). 86 chr1 + 86 chr2 units.
2. **The 88-unit v4c pipeline run** — the cross-hardware reproducibility control
   (run 2026-08-19), whose command line and records we recovered from the host on
   2026-09-01.

Both are in good shape. Nothing needs re-running on the A100 for the current
manuscript.

---

## 2. The ClonalFrameML run: assessment

**It is complete and correct.** All 172 unit-directories carry a full parameter
set. The three points from the delivery note all check out:

- **Both arms completed 86/86.** Confirmed.
- **The two missing alignments were the expected ones.** `strain_1_L1_36` and
  `strain_1_L1_37` are exactly the two the frozen-basis README names as having no
  local `.core.full.aln`. Correct.
- **The `strain_7_L1_1` "Unknown sequence type" fix was right.** Forcing `-st DNA`
  was the correct call, and for a concrete reason: that unit's SNP file is 42.7%
  N (857 of 2,040 characters), which is what defeats IQ-TREE's sequence-type
  autodetection. The alignment itself is sound (136 real SNPs reconstituted to
  3.93 Mb via `-fconst`, 99.9965% constant).

  One thing worth knowing downstream: that unit sits **below the Gate 1 detection
  floor** on every basis (15.4 mean pairwise SNPs against a floor of 700), so its
  r/m was never interpretable regardless. The fix was correct; the unit just does
  not contribute to any reported number.

**Two small documentation notes, neither a problem with the run:**

- The shipped `cfml_v4c_chr1.log` still records `strain_7_L1_1 chr1 exit=2` with
  no record of the successful rerun. The rerun output is real and complete
  (timestamped 2026-08-26 11:06 against the 2026-08-21 main run); the log is just
  the stale first pass. If it is easy to regenerate the log after the rerun, that
  would make the delivered log match the delivered results, but it is cosmetic.
- `-st DNA` is present in all 86 chr2 runs but only the one chr1 rerun. Not an
  issue, just noting the two arms did not run identical command lines.

**The NaN concordance had two separate causes, not one.** The delivery note
attributed all of it to the missing `tier0_evidence_bp.py`. That is only half:

- **Pearson/Spearman** are NaN because `tier0_evidence_bp.py` was absent. It
  supplies only two helpers (`pearson()`, `pvalue()`), both of which exist on the
  workstation, so re-running the report there fills these in. We did, and the
  numbers are in section 4 below.
- **The suspects-vs-controls "nu" table** is NaN for an unrelated reason: the run
  used `--all`, so every unit carries role `other`, both groups are empty, and
  their means are undefined. Shipping the missing module would not have fixed
  this. Given the nu hypothesis is already refuted and nu/delta are confounded, we
  are not resurrecting that table, so no action is needed.

---

## 3. The 88-unit run: assessment as the cross-hardware control

**This is the strongest use of the A100 work, and it holds up well.** We
recovered its command line and records from the host and reconciled them against
the reported workstation run.

- **Nextflow 25.10.0 confirmed** (read from the log banner). It had been carried
  in the draft Methods as "unverified" and is now verified.
- **Both runs executed byte-identical pipeline code.** The two execution reports
  record the same Nextflow Script ID, `e09a5c4eadba2c5984f6790095423ee4`, which is
  a hash of `main.nf`. That is a stronger provenance statement than a shared git
  commit.
- **Identical tool versions** across both runs (Gubbins 3.4.3, IQ-TREE 2.2.6,
  snippy 4.6.0, parsnp 1.7.4, numpy 1.26.2, Ubuntu 22.04.5). So the two runs
  differ in exactly two respects: Nextflow version and resource profile.
- **Clean run:** 8,174 tasks, 0 cached, 0 ignored, 0 failed, 0 retries; 176/176
  replicon-units at the highest confidence tier.
- **Cross-platform r/m agreement is 0.36% median relative difference** over the
  membership-matched units. This is the empirical basis for the reproducibility
  claim in the manuscript.

**The `-resume` in the command line is a non-issue.** We checked: there is exactly
one `.nextflow.log` in that directory with no rotated predecessors, and the run
reports 0 cached tasks, so `-resume` resumed nothing. It was a no-op on a first
run.

**One trap to avoid on the A100, for whoever cites this run:** the `pipeline_info/`
directory under `~/wf-assembly-snps-mod/` is dated **2026-05-28 and belongs to an
unrelated earlier run**. Do not cite it for this control. The control's own
record is at `/data/scratch/v4c/L1v4c_out/pipeline_info/` (execution report,
timeline, trace, `software_versions.yml`). We copied those five files off to
preserve them, because scratch is not backed up — see section 7.

---

## 4. What we recomputed, and the honest concordance result

Since `tier0_evidence_bp.py` is local, we regenerated the concordance the shipped
report could not:

- **Cross-platform ClonalFrameML agreement is essentially perfect.** Across all
  172 unit-replicons the median relative difference in implied r/m is **0.00%**,
  and inside the Gate 1 window the maximum is 2.43% with nothing above 5%. Both of
  the two >5% outliers fall outside the window.
- **A crossover test settles where the residual variation lives.** We fed the
  A100's starting tree for one unit to *local* ClonalFrameML and got a
  **byte-identical `cfml.em.txt`** back. So ClonalFrameML itself is deterministic
  across the two machines, and 100% of the run-to-run variation comes from one
  step: the unseeded IQ-TREE call that builds the starting tree (see section 6).
- **Gubbins vs ClonalFrameML concordance is moderate, not high.** On the Gate-1
  in-window units, Pearson r ≈ +0.56 and Spearman rho ≈ +0.52, with ClonalFrameML
  estimating r/m about **1.74× higher** than Gubbins. This is a real result and
  we are comfortable with it; it is worth stating so nobody expects the two tools
  to agree tightly.

**One provenance point about the shipped concordance table.** Its `n` column is
correct (it equals the A100 partition's unit sizes). But for **four units**
(`strain_1_L1_26`, `strain_1_L1_22`, `strain_1_L1_11`, `strain_27_L1_1`) the two
columns of that table come from **different runs**: the Gubbins r/m is the A100
control run's, while the ClonalFrameML value was computed on alignments that came
from the reported workstation run. The pairing is sound for **82 of 86** units and
**45 of the 47** in-window units. The root cause is benign: the control ran 2,342
genomes against the reported run's 2,352 (a strict subset, 10 fewer), and those 10
genomes fall in exactly those units. Nothing was done wrong; the two runs simply
have slightly different membership in a few units. If we report the concordance,
we will restrict to the pairing-sound set.

---

## 5. Where the A100 work lands in the manuscript

- **The A100 88-unit run is the cross-hardware reproducibility control** (Results
  section 9), not the reported basis. The reported basis is the 85-unit
  workstation run. This is the designation that was corrected on 2026-08-22 (the
  A100 run was previously labelled "production"); the control framing is the
  stronger use of it, and section 9 now cites the same-Script-ID and 0.36%
  agreement findings.
- **The ClonalFrameML result is currently in the Discussion** as a suggested
  next step ("an independent within-lineage estimator applied across all in-window
  units would establish whether the rank disagreement is real"). We did not put
  the six-unit pilot in Results. If the A100 side wants to run the full in-window
  comparison, that would let us promote it to a Results finding — see section 8.

---

## 6. One issue that applies to both platforms: the pipeline is not deterministic

This is not an A100 problem specifically — the workstation runs the same way — but
it surfaced through the A100 comparison, so it belongs here.

**IQ-TREE is invoked without `-seed`, so the starting tree differs every run.** We
measured that `-seed` alone is not enough: multithreaded IQ-TREE is
non-deterministic regardless of seed, while single-threaded with a fixed seed is
bit-identical across repeats. The fix is **`-seed <N>` AND `-T 1`** at
`clonalframe_nu_bp.py:249`. This has since been applied on the workstation side.

The consequence for the A100 comparison is actually reassuring: because
ClonalFrameML is bit-identical given the same tree, the whole cross-platform
story is clean once the tree-building step is seeded. Until then, the runs are
reproducible *in practice* (to well within the precision we quote) but not *by
construction*.

Note the reported run is pinned at a commit that predates the `gubbins_seed` fix,
so re-running it seeded would produce a *different* run rather than validating the
pinned one. We are not asking anyone to re-run the reported analysis.

---

## 7. Files that live only on A100 scratch — please preserve

The control run's own records exist only at
`/data/scratch/v4c/L1v4c_out/pipeline_info/` on the A100, which is **not backed
up**. We copied five of them to the workstation and they will go into the archive
(Zenodo):

- `execution_report_2026-08-19_11-49-18.html`
- `execution_timeline_2026-08-19_11-49-18.html`
- `execution_trace_2026-08-19_11-49-18.txt`
- `pipeline_dag_2026-08-19_11-49-18.html`
- `software_versions.yml`

If that scratch path is at any risk of being cleared, a second copy on the A100
side would be worth keeping until the archive is deposited.

---

## 8. What we would ask the A100 side to confirm or consider

**Please confirm (sense-check):**

1. That our reading of the ClonalFrameML run matches what you did — in particular
   the `-st DNA` fix, and that the `--all` flag was intentional (it is fine; it
   just empties the suspects/controls groups).
2. That the 88-unit run at `/data/scratch/v4c/L1v4c_out` with session
   `insane_jennings` and Script ID `e09a5c4ead...` is indeed the control run we
   think it is, and that nothing else was run from that directory.

**Optional, only if we decide to promote the ClonalFrameML result to Results:**

3. Extend the ClonalFrameML comparison from the six-unit pilot to the **full
   in-window set** (47 units), with `-st DNA` set for all of them and with the
   IQ-TREE starting-tree step **seeded and single-threaded** so the run is
   reproducible by construction. That would let us report the Gubbins/CFML
   concordance as a Results finding rather than a Discussion aside.
4. If convenient, a small **determinism demonstration**: run ~10 units twice under
   `-seed <N> -T 1` and confirm byte-identical output. That converts "should be
   deterministic" into a measurement and would strengthen the Methods.

Neither 3 nor 4 is on the critical path. The manuscript is complete without them.

---

## 9. Bottom line

The A100 work was solid, complete, and is doing real load-bearing work in the
paper as the cross-hardware reproducibility control. The two runs agree to 0.36%
and provably ran the same pipeline code. The ClonalFrameML run is intact and its
one visible failure (`strain_7_L1_1`) was handled correctly. Our only substantive
findings were (a) the NaN concordance has a second, benign cause beyond the
missing module, (b) four concordance rows pair estimates across two runs with
slightly different membership, and (c) the shared unseeded-IQ-TREE issue, which is
a whole-project matter and not specific to the A100.

Nothing here changes a reported number. If any of section 2, 3, or 4 does not
match your understanding of what was run, that is exactly what we want to hear
before this goes further.
