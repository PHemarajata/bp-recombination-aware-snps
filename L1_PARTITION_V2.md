# L1 partition v2 — the double size filter, fixed

`build_L1_partition_bp.py`, 2026-08-16. Old behaviour is still available with
`--no-merge`, and it reproduces the published partition exactly (204 units, 82
kept, 2,070 genomes, 15 stragglers with 12 placed) — verified before any change
was made.

## The defect

`min_cluster_size = 7` was applied **twice, to two different kinds of thing**:

| filter | applied to | in | out | discarded |
|---|---|---|---|---|
| PopPUNK strain floor | 264 strains | 2,802 | 2,395 | 407 |
| fastbaps L1 unit floor | 204 units | 2,395 | **2,070** | **322 (122 of 204 units)** |

The floor was justified for *strains* (7 = the smallest unit in the existing
analysed set). fastbaps exists to *subdivide* strains, so reapplying the same
absolute floor to its output discarded 60% of L1 units by construction, and the
loss tracked rarity — Singapore 0%, Thailand 16.8%, USA 41.7%, Australia 74.1%,
India 94.6%, and 51% of every Americas genome in the collection.

## The fix

Sub-threshold L1 units are **absorbed into their nearest sibling within the same
strain** instead of deleted. A merge needs two clauses:

1. **gap** — `d_min(A,B) <= diameter(B)`. The existing straggler containment
   test, unchanged: the gap must fall inside the spread the *receiver* already
   has.
2. **result** — `diameter(A ∪ B) <= ceiling`, where the ceiling is the **90th
   percentile of the diameters of units reaching min_size without any merging**
   (0.00378 here). Calibrated from the data, not chosen.

Clause 1 alone is not enough, and clause 2 exists because of a measured failure:
a first draft used `max(diameter(A), diameter(B))` as the bound, which lets a
loose little unit license its own merger into a clonal one. That draft took
`strain_1_L1_3` from diameter 0.00047 to 0.00385 (8×) and widened
`strain_20_L1_1` — the published Georgia cluster — from 0.00084 to 0.00327.

What still cannot merge is **not deleted**. It keeps its unit label and appears
in `curated_L1v2_assignments_all.tsv` with `role=assign_only`: too small to
estimate r/m from is a statement about what the unit supports, not a reason to
discard genomes that remain usable for placement and distance-based attribution.

## Result

| | before | after |
|---|---|---|
| analysis units | 82 | **91** |
| genomes analysed | 2,070 | **2,265** (+195) |
| of the partition | 86.4% | **94.6%** |
| of the 2,802 collection | 73.9% | **80.8%** |
| genomes deleted outright | 322 | **0** |
| assign-only (retained) | — | 127 |

**Coherence held.** Unit-diameter p90 0.00380 → 0.00378, max unchanged at
0.00541, median 0.00198 → 0.00222. Six units grew more than 1.5×, all inside the
ceiling. **All 82 original units survive as subsets — none was broken up** — and
the two units carrying published or load-bearing results are untouched:
`strain_20_L1_1` (Georgia) and `strain_9_L1_4` (Puerto Rico) are identical in
membership and diameter.

**Recovered:** Burk-Genome study genomes 257 → **278** of 312 (IP 218→234,
IE 39→44). Americas 30 → **38**. India 3 → **12**. Australia 73 → 82.
Laos 36 → 46. Malaysia 50 → 61. Thailand 1,458 → 1,590.

## The cost: the manual-analysis cross-check shrinks

Merging changes what an analysis unit *is*, and the manual fastbaps analysis —
the strongest external validation this project has — was performed on the
**unmerged** subclusters. Units that were size-identical to a manual unit:

| | size-identical to the manual analysis |
|---|---|
| v1 (82 units) | **65 of 67** |
| v2 (91 units) | **50 of 67** |

Fifteen manual-matched units absorbed a sibling, e.g. `strain_5_L1_4` 15 -> 29,
`strain_16_L1_3` 8 -> 22, `strain_7_L1_3` 13 -> 22.

**This does not invalidate the label transfer.** v2 changes no fastbaps label; it
only groups them, so "every pp2802 strain maps 1:1 onto one archived strain"
still holds and the 35-of-37 set-identity result stands as a statement about
*labels*. What changes is that 15 analysis **units** are no longer the same
objects the manual analysis measured, so any r/m comparison against manual values
— including the one used to validate the reference-branch correction (agreement
tightened to IQR 1.26-1.64) — must be restricted to the 50 unchanged units or
re-derived on the unmerged subclusters.

That is the trade in one line: **+195 genomes and 0 deletions, against 15 fewer
units directly comparable to the manual analysis.** Both partitions are on disk
so the comparison can be run either way.

## What is still lost, and what it would take

**407 genomes sit in PopPUNK strains below the strain floor** and never reach
this script. They are now listed as `role=below_strain_floor` rather than
vanishing silently. Recovering them is a separate change at the PopPUNK stage —
those strains genuinely cannot support Gubbins, so the honest fix is the same
one applied here: retain them for assignment, exclude them from estimation.

## Adopting it

`curated_L1v2_*` is written alongside the existing `curated_L1_*`, which is left
untouched because every published deliverable refers to it. To adopt:

```bash
build_L1_partition_bp.py -> pick_cluster_references_bp.py
  -> rank_reference_alternates_bp.py (no --refs)
  -> merge_L1_refs_bp.py -> rank_reference_alternates_bp.py (--refs)
  -> run_wf_curated_L1.sh   # ~11 h, 91 units instead of 82
```

Every r/m figure, tree and phylogeography result in the current deliverables is
computed on the 82-unit partition and would need recomputing against the 91.

---

# v3 — the strain floor, fixed the same way (2026-08-16)

`--absorb-subthreshold-strains` brings the 229 PopPUNK strains below the strain
floor (407 genomes, 152 of them singletons) into the partition as whole-strain
units, then runs a **cross-strain merge round** under the identical two-clause
rule. Outputs: `curated_L1v3_*`.

| | v1 | v2 | **v3** |
|---|---|---|---|
| analysis units | 82 | 91 | **91** |
| genomes analysed | 2,070 | 2,265 | **2,282** |
| assign-only (retained) | — | 127 | **517** |
| **deleted outright** | **732** | **407** | **0** |
| unit diameter, median | 0.00198 | 0.00222 | 0.00223 |
| unit diameter, p90 / max | 0.00380 / 0.00541 | 0.00378 / 0.00541 | **0.00378 / 0.00541** |

**Coherence is untouched** — p90 and max identical to v2, median moved by
0.00001. Six units changed, all inside the ceiling. `strain_20_L1_1` (Georgia)
and `strain_9_L1_4` (Puerto Rico) are unchanged, and all 82 original units
survive as subsets.

## What this does and does not buy

**Every genome in the collection is now accounted for.** 2,282 analysis + 517
assign-only + 3 unassigned = 2,802. Nothing vanishes silently, which was the
actual defect.

**But only 12 units (17 genomes) crossed into analysis.** The strain floor was
NOT holding back analysable data, and an earlier claim in this document that
fixing it would recover 171 Australian and 42 Indian genomes *for analysis* was
wrong. Those genomes are 229 distinct lineages, 152 represented by a single
genome. Gubbins has nothing to compare them against; the correct outcome is to
retain them for assignment, which is now what happens.

## The finding that matters: 177 genomes are within 1-3 of being analysable

The 517 assign-only genomes sit in units of these sizes:

| unit size | genomes | units |
|---|---|---|
| 1 | 180 | 180 |
| 2 | 82 | 41 |
| 3 | 78 | 26 |
| **4** | **76** | 19 |
| **5** | **65** | 13 |
| **6** | **36** | 6 |

**38 units holding 177 genomes need only 1-3 more relatives to cross the
threshold.** By country: Australia 59, Thailand 59, Laos 10, India 9, China 9,
Mexico 6, Viet Nam 5, USA 5, Myanmar 4, Malaysia 4, PNG 3.

This reframes the add-more-genomes question. Targeted additions do not merely
add data — **they rescue data already in hand** by giving orphan lineages
relatives. Mexico is the clean case: 9 genomes held, 6 of them in units of 4-6,
and 27 more available publicly. A download of 27 would likely convert a
currently unanalysable Mexican lineage into an analysis unit. The same logic
applies to Australia and India, where the collection already holds far more than
it can analyse.
