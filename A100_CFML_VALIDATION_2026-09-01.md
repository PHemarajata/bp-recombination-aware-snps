# A100 ClonalFrameML run: reproducibility and concordance assessment

**Date:** 2026-09-01
**Artifact assessed:** `cfml_v4c_results.tar.gz` (71.7 MiB), delivered to
`gdrive_ph:wfsnps-v4c-results/` 2026-08-26 15:18
**Comparator:** the independent local ClonalFrameML run in `cfml/` (172 directories
dated 2026-08-21)
**Derived table:** `A100_CFML_CONCORDANCE_CORRECTED.tsv` (86 units)

---

## Bottom line

**The A100 reproduced the local run on every unit where our r/m estimates are
interpretable.** Across the 47 Gate 1 in-window units the two runs agree on
implied r/m to a median relative difference of **0.00%**, with a maximum of
**2.43%** and **nothing above 5%**. All 172 unit-replicons were run on identical
taxon sets.

The agreement is stronger than a like-for-like rerun would have been, because it
survives a change of tree-builder major version, thread count, and hardware
simultaneously.

A controlled experiment (§3.1) pins the residual variation precisely.
**ClonalFrameML given the same starting tree produces byte-identical output on
the two machines.** Every difference between the runs traces to one step: the
unseeded, multithreaded IQ-TREE call that builds the starting tree. Fix that call
and the whole pipeline becomes deterministic.

Two qualifications, neither of which moves a reported number:

1. **The pipeline is not deterministic by construction.** What we have is
   reproducibility demonstrated in practice, not guaranteed by the code. See §3.
2. **The shipped report has defects**: a wrong `n` column for four units, and
   NaN statistics arising from two separate causes. The CFML outputs themselves
   are unaffected. See §4.

---

## 1. What was delivered, and what was verified

86 chr1 and 86 chr2 unit directories, all carrying complete ClonalFrameML output
(`cfml.em.txt`, `cfml.importation_status.txt`, `cfml.labelled_tree.newick`,
`cfml.ML_sequence.fasta`, `cfml.position_cross_reference.txt`). Nothing needs
rerunning on the A100.

Three claims from the delivery note were checked:

The control run's own record was recovered from the A100 on 2026-09-01
(`PRODUCTION_RUN_PIN_2026-08-24.md` §7). Its execution trace shows **8,174 tasks,
every one `COMPLETED` at exit 0**, covering 88 units, 176/176 replicon-units and
2,342 genomes, against the reported run's 8,178 tasks, 86 units, 172/172 and
2,352 genomes. **Both runs used identical tool versions** (Gubbins 3.4.3, IQ-TREE
2.2.6, snippy 4.6.0, parsnp 1.7.4, numpy 1.26.2, Ubuntu 22.04.5), so Nextflow
(25.04.6 against 25.10.0) is the only software difference between them. The
control's 2,342 genomes are a strict **subset** of the reported run's 2,352.

| Claim | Verdict |
|---|---|
| Both arms completed 86/86 | **Confirmed.** All 172 directories are complete. |
| The two missing alignments were the expected ones | **Confirmed.** `strain_1_L1_36` and `strain_1_L1_37` are exactly the two the frozen-basis README names as having no local `.core.full.aln`. |
| `strain_7_L1_1` was fixed by forcing `-st DNA` | **Confirmed, and the fix is correct.** See §6. |

One documentation defect: the shipped `cfml_v4c_chr1.log` still records
`strain_7_L1_1 chr1 exit=2` and contains no record of the successful rerun. The
rerun output is real and complete (timestamped 2026-08-26 11:06 against the
2026-08-21 14:58 main run). The log is stale, not the result.

---

## 2. Platform reproducibility: the main result

Unit-level implied r/m, averaged over both replicons, local run versus A100 run,
stratified by Gate 1:

| Gate 1 stratum | units | median rel. diff | max | above 5% |
|---|---|---|---|---|
| **in-window** | 47 | **0.00%** | **2.43%** | **0** |
| above window | 26 | 0.00% | 3.65% | 0 |
| below window | 12 | 0.40% | 19.09% | 1 |
| not gated (`strain_1_L1_10`) | 1 | 0.28% | 0.28% | 0 |

At the finer per-unit-replicon level (172 comparisons), the median relative
difference is 0.00% for R/theta, delta, nu, and implied r/m alike; the 90th
percentile is about 1%; 16 of 172 exceed 1% and only 2 exceed 5%.

**Both of the >5% cases fall outside the Gate 1 window**: `strain_8_L1_1__chr2`
(below window, 27.4% at replicon level and 19.09% at unit level) and
`strain_3_L1_10__chr2` (above window, 7.6%).

This is worth stating explicitly as a finding in its own right. Gate 1 was
derived from alignment SNP density and had nothing to do with ClonalFrameML, yet
it independently predicts where ClonalFrameML is numerically stable. That is a
second, independent vindication of the window.

The Gubbins r/m from the two machines likewise agree to **0.36% median relative
difference** across the membership-matched units, consistent with the 0.46%
figure recorded in the frozen-basis README.

### What the comparison spans

| | local | A100 |
|---|---|---|
| IQ-TREE | 2.4.0 (all 172) | **3.1.3 (all 172)** |
| threads | `-T 4` (170), `-T 8` (2) | `-T 8` (171), `-T 16` (1) |
| `-st DNA` | none | all 86 chr2, plus the one chr1 rerun |
| random seed | unseeded, auto-generated | unseeded, auto-generated |

The estimate is robust to the whole toolchain, not merely to the hardware.

---

## 3. The determinism defect

The driver at `clonalframe_nu_bp.py:249` invokes IQ-TREE without `-seed`:

```
"$IQ" -s "$WD/snps.fasta" -fconst "$FCONST" \
    -m GTR+F+I -T {threads} --prefix "$WD/start" -redo
```

Consequently the starting tree differs on **all 172** unit-replicons, and the two
runs land in different EM optima. On `strain_8_L1_1__chr2` the maximum
log-likelihood was -79520.2 locally against -79005.2 on the A100. That single
unit accounts for the largest disagreement in the whole comparison.

### The starting tree accounts for all of it

To separate the tree-building step from ClonalFrameML itself, the A100's starting
tree for `strain_8_L1_1__chr2` was rerun through **local** ClonalFrameML on the
local alignment. If the machines themselves contributed anything, the result would
land somewhere between the two originals.

| run | R/theta | delta | nu | implied r/m |
|---|---|---|---|---|
| local (local tree, IQ-TREE 2.4.0) | 0.91837 | 329.1 | 0.010427 | 3.152 |
| A100 (A100 tree, IQ-TREE 3.1.3) | 0.97950 | 479.4 | 0.008844 | 4.153 |
| **crossover (A100 tree, run locally)** | **0.97950** | **479.4** | **0.008844** | **4.153** |

The crossover reproduces the A100 exactly: **0.00% on all four parameters, and the
entire `cfml.em.txt` is byte-identical**, including per-branch estimates and
posterior variances. Against the local run it differs by the full original 27.42%.

Two conclusions follow, and they are worth stating separately:

- **ClonalFrameML is exactly reproducible across the two machines.** Not "agrees
  within tolerance" but bit-identical, given the same tree and alignment.
- **The unseeded IQ-TREE call is the sole source of run-to-run variation in the
  pipeline.** It accounts for 100% of the observed discrepancy, not merely most
  of it.

That is why the fix below is worth making. It is not a marginal tightening; it
converts the pipeline from reproducible-in-practice to deterministic.

### Adding `-seed` alone does not fix it

**Adding `-seed` alone does not fix this.** Measured directly on that unit's SNP
alignment with IQ-TREE 2.4.0:

| configuration | runs | distinct trees | best log-likelihood |
|---|---|---|---|
| `-seed 12345 -T 4` | 2 | **2** | varies |
| `-seed 999 -T 4` | 2 | **2** | -4283096.162 / -4283096.233 |
| `-seed 12345 -T 1` | 3 | **1** | -4283083.774 (identical) |

Multithreaded IQ-TREE is non-deterministic regardless of seed. **The fix is
`-seed <N>` together with `-T 1`.** Single-threading also happened to find a
better likelihood here than any multithreaded run, though that is a single unit
and not a general claim.

Until that lands, the honest formulation is: the run is reproducible in practice
to well within the precision at which we quote r/m, but it is not reproducible by
construction, and a rerun on the same machine would also differ.

---

## 4. Corrections to the shipped report

### 4.1 A provenance mismatch in four units

> **Corrected 2026-09-01.** This section previously said the report's `n` column
> was wrong for four units. **It is not wrong.** Checked against the control
> run's own execution trace and membership table, `n` equals the A100 control
> partition's unit size in **all 86 cases**. The defect is real but it is not
> where I first placed it.

The two columns of the concordance table come from **different runs**. The
Gubbins r/m and `n` are the A100 control run's, drawn from
`rm_provenance/A100_recombination_rm.tsv` (86 of 86 exact match). The
ClonalFrameML values were computed on alignments that, for four units, came from
the **reported workstation run** instead:

| unit | CFML alignment | control partition | frozen basis | Gate 1 |
|---|---|---|---|---|
| `strain_1_L1_26` | 154 | 98 | 153 | in |
| `strain_1_L1_22` | 34 | 32 | 34 | in |
| `strain_1_L1_11` | 24 | 18 | 24 | above |
| `strain_27_L1_1` | 11 | 10 | 11 | below |

For three of them the alignment matches the frozen basis **exactly**, which is
what identifies the workstation run as its source. The proof is direct: the
control run's trace shows it never processed the six genomes
(`GCA_963562295_1`, `GCA_963562875_1`, `GCF_002900605_1_Malaysia`,
`GCF_002900625_1_Malaysia`, `GCF_028621545_1_missing`, `GCF_041028405_1`) that
separate `strain_1_L1_11` at 24 from the same unit at 18, yet all six are present
in that unit's ClonalFrameML alignment.

So for these four units the shipped table compares a Gubbins estimate and a
ClonalFrameML estimate **computed on different genome sets**. For
`strain_1_L1_26` that is 98 against 154.

**Effect on the concordance.** The pairing is sound for **82 of 86** units, and
for **45 of the 47** in-window units (`strain_1_L1_22` and `strain_1_L1_26` are
the exceptions). Restricted to the sound pairs:

| set | n | Pearson r | Spearman rho | CFML/Gubbins |
|---|---|---|---|---|
| all 86, as shipped | 86 | +0.592 | +0.611 | 2.33x |
| pairing-sound | 82 | +0.571 | +0.586 | 2.32x |
| in-window, as shipped | 47 | +0.558 | +0.516 | 1.74x |
| **in-window and pairing-sound** | **45** | **+0.514** | **+0.481** | **1.74x** |

Dropping the four rows is the cheap and defensible repair. Repairing them
properly would mean re-running ClonalFrameML on the control's own alignments for
those units, which live only on the A100's unbacked-up scratch.

### 4.2 The NaNs have two distinct causes

- **Pearson and Spearman**: caused by the missing `tier0_evidence_bp.py`, which
  supplies only two helpers, `pearson()` and `pvalue()`. Both exist locally, so
  re-running the report here resolves these.
- **The suspects-versus-controls "nu" table**: *not* caused by the missing
  module. The run used `--all`, so every unit carries role `other`, both groups
  are empty, and their means are NaN. Shipping the module would not have fixed
  it. Given that the nu hypothesis is already refuted and that nu and delta are
  confounded at -0.86, this table is not worth resurrecting.

---

## 5. Basis alignment against the frozen 85

The ClonalFrameML alignments match frozen-basis membership for **82 of 86**
units. The exceptions are small:

| unit | CFML genomes | frozen | note |
|---|---|---|---|
| `strain_1_L1_26` | 154 | 153 | +1 |
| `strain_1_L1_8` | 91 | 89 | +2 |
| `strain_14_L1_4` | 14 | 12 | +2 |
| `strain_1_L1_10` | 7 | n/a | not in the frozen basis at all |

Of the 47 Gate 1 in-window units, **45 are membership-clean**; the exceptions are
`strain_1_L1_26` and `strain_1_L1_8`. Note that `strain_8_L1_1` and
`strain_1_L1_8` are different units and are easy to confuse.

---

## 6. `strain_7_L1_1`, the unit that failed and was rerun

The "Unknown sequence type" error had a real cause. That unit's SNP file is
**42.7% N** (857 of 2,040 characters), which defeats IQ-TREE's sequence-type
autodetection. The alignment is otherwise sound: 136 genuinely polymorphic
columns across 15 taxa, reconstituted to 3,931,555 sites via `-fconst`, and
99.9965% constant. Forcing `-st DNA` is the correct response.

It does not follow that the unit's r/m is usable. `strain_7_L1_1` is a
hyper-clonal Micronesia/Yap cluster at **15.4 mean pairwise SNPs** against a Gate
1 floor of 700, and is flagged `below` on both the alignment and the Mash bases.
Its r/m was never interpretable, so the rerun changes nothing downstream.

---

## 7. Tool concordance is a separate question, and the answer is weaker

Platform reproducibility (§2) and agreement between Gubbins and ClonalFrameML are
different questions. The second is the weaker result.

Gubbins r/m on the frozen basis against ClonalFrameML implied r/m from the A100:

| set | n | Pearson r | Spearman rho |
|---|---|---|---|
| all 86 units | 85 | +0.594 | +0.613 |
| Gate 1 in-window | 47 | +0.538 | +0.521 |
| in-window and membership-clean | 45 | **+0.521** | **+0.498** |

ClonalFrameML runs systematically higher than Gubbins: median **1.83x** on the
clean in-window set, range 1.03x to 10.64x.

Two cautions for anyone quoting these. Restricting to the window *weakens* the
correlation, so the all-86 figure is range-inflated by units where the estimator
is known to fail. And the report's claim that "12 units change verdict" is
internally valid on the A100 basis but does not transfer wholesale to the
reported basis, since three of those twelve (`strain_1_L1_22`, `strain_1_L1_8`,
`strain_1_L1_10`) are affected by the membership issues in §5.

---

## 8. What can and cannot be claimed

**Supported:**

- The A100 reproduced the local ClonalFrameML result on all 47 Gate 1 in-window
  units, to a median of 0.00% and a maximum of 2.43% relative difference in r/m.
- That reproduction survives a tree-builder major version change, differing
  thread counts, and differing hardware.
- Gubbins r/m reproduces cross-platform to 0.36% median relative difference.
- Every numerical disagreement above 5% lies outside the Gate 1 window.
- **ClonalFrameML itself is exactly reproducible across the two machines**:
  given the same starting tree and alignment it returns byte-identical output.
  The unseeded IQ-TREE call is the sole source of run-to-run variation.

**Not supported, and should not be written:**

- That "all results were concordant and reproducible" without qualification.
  Twelve below-window and 26 above-window units were also compared, and one
  below-window unit disagrees by 19%.
- That the pipeline is reproducible by construction. It is not, until `-seed`
  and `-T 1` are set.
- That Gubbins and ClonalFrameML agree about which units are recombinant. At
  r = +0.52 in-window, with a systematic 1.83x offset, they do not.

---

## 9. Recommended actions

1. **Set `-seed <N>` and `-T 1`** in the IQ-TREE call at
   `clonalframe_nu_bp.py:249`. This is the only change that affects future
   results, and it is a precondition for the reproducibility test already on the
   TODO list.
2. **Re-run the report locally** so the Pearson and Spearman cells populate, and
   drop or fix the suspects/controls block rather than shipping NaNs.
3. **Correct the `n` column** from the alignments, and re-pair the four affected
   concordance rows.
4. **Use `A100_CFML_CONCORDANCE_CORRECTED.tsv`** as the source for any downstream
   table, and take membership from it rather than from the report.
5. Ask that the chr1 log be regenerated after the rerun, so the delivered log
   matches the delivered results.
