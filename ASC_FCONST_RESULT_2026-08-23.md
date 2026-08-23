# `+ASC` vs `-fconst` — resolved on two units

**2026-08-23.** The standing method question (outline W10 item 2; handoff open
item 9): production built per-unit trees under **`GTR+ASC`** with
`iqtree_fconst = null`, while §2.5 of the Methods argues **`-fconst` with true
constant-site counts** is preferable in a 68% GC genome. Quantified here.

> **Two conclusions, and they point in different directions.**
>
> **1. §2.5's argument is correct, and the effect is large.** `+ASC` drives
> estimated GC from a true 68.1% down to **54.5–58.9%**; `-fconst` reproduces it
> at **67.8–68.0%**. Topologies also differ.
>
> **2. It changes no reported number.** Every quantity in this paper derives from
> **Gubbins** outputs — `per_branch_statistics.csv` and
> `node_labelled.final_tree.tre` — not from the IQ-TREE `+ASC` tree, which is
> consumed only by archival and export scripts. **The question is real, and it is
> immaterial to the results.**

---

## 1. What was compared

The final per-unit tree is built on the Gubbins **variant-sites-only** alignment
(`filtered_polymorphic_sites.fasta`). Every one of the 176 ASC preflights records
`N_CONSTANT_COLS=0`, `IQ_MODEL=GTR+ASC`, `IQ_FCONST=` (empty) — so ascertainment
correction is being applied to an alignment that genuinely has no constant
columns, which is a legitimate treatment. `-fconst` is the alternative
legitimate treatment: supply the true constant-site counts instead.

Both were run on the **identical alignment**, same IQ-TREE build
(`iqtree 2.2.6`), same seed (20260823), same threads. Constant-site counts were
tallied permissively from each unit's `.core.full.aln`, which is what §2.5
specifies.

Two units, chosen to separate a model effect from an under-determined tree:

| | `strain_4_L1_1` | `strain_1_L1_28` |
|---|---|---|
| character | Gulf Coast, **clonal** | **Gate 1 in-window** |
| taxa | 23 | 57 |
| variant sites | 3,770 | 15,139 |
| mean pairwise (core SNPs) | ~8 raw / 5 filtered | 1,572 |

## 2. Base composition — §2.5 is right

| | true (full alignment) | `+ASC` estimate | `-fconst` estimate |
|---|---|---|---|
| **`strain_4_L1_1`** | A .1590 C .3413 G .3394 T .1604 | A .2204 C .2819 G .2635 T .2343 | A .1601 C .3402 G .3382 T .1616 |
| GC | **68.1%** | **54.5%** | **67.8%** |
| **`strain_1_L1_28`** | — | A .2151 C .2921 G .2965 T .1962 | A .1594 C .3411 G .3388 T .1607 |
| GC | **68.1%** | **58.9%** | **68.0%** |

**`+ASC` collapses composition toward equal base frequencies exactly as §2.5
predicts** — 13.6 and 9.2 percentage points of GC lost — while `-fconst`
reproduces the full-alignment composition to within 0.3 points. The argument in
the calibration section is confirmed, not merely asserted.

## 3. Tree length — different units, and not a simple rescaling

| | `+ASC` | `-fconst` | ratio |
|---|---|---|---|
| `strain_4_L1_1` | 0.1914 | 0.00095 | 202× |
| `strain_1_L1_28` | 0.5389 | 0.0013 | 415× |

This is expected in direction: `+ASC` lengths are per *variable* site,
`-fconst` lengths are per site over the whole ~4.05 Mb alignment. **But it is not
a pure rescaling.** Naively rescaling the `+ASC` length by (variant sites / full
length) gives 0.000178 for `strain_4_L1_1`, against an observed `-fconst` length
of 0.00095 — a five-fold discrepancy. The two models are fitting different
processes, not the same process in different units. **Branch lengths are
therefore not interconvertible between the two settings**, and no correction
factor should be offered.

## 4. Topology — differs, and the difference is signal-dependent

| unit | internal bipartitions | shared | RF (symmetric difference) | normalised |
|---|---|---|---|---|
| `strain_4_L1_1` (clonal) | 20 / 20 | 7 | **26** | **0.650** |
| `strain_1_L1_28` (Gate 1) | 54 / 54 | **48** | **12** | **0.111** |

**The clonal unit reshuffles; the high-signal unit largely does not.** On
`strain_4_L1_1` — median 5 filtered SNPs between members — 65% of bipartitions
differ, but that tree was never well determined, and any perturbation would move
it. On `strain_1_L1_28`, with 15,139 variant sites, **89% of bipartitions are
identical** under the two models.

So the honest statement is: **the model choice perturbs topology where the data
barely constrain it, and largely does not where they do.** That is a
reassuring pattern rather than an alarming one, but it does mean the two settings
are not interchangeable for display trees of clonal units.

## 5. Why it changes no reported result

Traced through every consumer:

| reported quantity | tree/statistic it reads | affected by `+ASC`? |
|---|---|---|
| **r/m** (`consolidate_L1_rm_bp.py`) | Gubbins `per_branch_statistics.csv` | **no** |
| **r/m reference correction** (`exclude_reference_branches_bp.py`) | Gubbins `node_labelled.final_tree.tre` + per-branch stats | **no** |
| **R6 phylogeography** (`phylogeography_association_bp.py`) | Gubbins `node_labelled.final_tree.tre` | **no** |
| **Global backbone** (`build_global_backbone_bp.py`) | Gubbins `node_labelled.final_tree.tre` | **no** |
| **Reference sensitivity** | Gubbins trees + per-branch stats | **no** |
| per-unit `.final.treefile` | — | **yes**, but consumed only by `archive_L1_stats.sh` and `export_deliverables_bp.sh` |

**The `+ASC` tree is a deliverable, not an input.** Gubbins re-estimates its own
tree at every iteration and reports recombination against that; the IQ-TREE step
runs afterwards and nothing downstream of it feeds a number in this paper.

Note also that R6 is a **Fitch parsimony** test, which reads topology only — so
even if it had used the IQ-TREE trees, branch-length differences would not have
touched it, and on high-signal units the topology is 89% shared.

## 6. What to do

1. **No result needs recomputing.** State in Methods that the choice was audited
   and is immaterial to every reported quantity, with the consumer table above as
   the evidence. This closes the open item.
2. **Fix the inconsistency in the text, not the analysis.** §2.5 argues for
   `-fconst` and §2.12.8 reports `+ASC`; both are now accurate descriptions of
   two different tracks, and the draft should say so explicitly rather than
   leaving a reader to find the contradiction.
3. ⚠ **If per-unit trees are published as supplementary files, rebuild them with
   `-fconst`.** A published tree whose estimated base composition is 54–59% GC in
   a 68% GC organism is hard to defend, and its branch lengths are per-variable-
   site rather than per-site. That includes the branch-support trees generated on
   2026-08-23 (`L1v4c_TREES_SUPPORTED/`), which inherited `GTR+ASC` from the
   preflight. **The support values are topology-based and largely unaffected; the
   branch lengths and composition are not.**
4. **Do not offer a conversion factor** between the two branch-length scales
   (§3).

## Reproduce

```
# counts from the unit's .core.full.aln, then on the SAME variant alignment:
iqtree2 -s aln.fasta -st DNA -m GTR+ASC                       -T 4 -seed 20260823 --prefix asc
iqtree2 -s aln.fasta -st DNA -m GTR -fconst <A>,<C>,<G>,<T>   -T 4 -seed 20260823 --prefix fconst
```
