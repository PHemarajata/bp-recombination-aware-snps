# L1 run: results, and the reference-branch correction

Run completed 2026-08-15. **82 units, 2,070 genomes, 164/164 replicon-units
`Tier1_high_confidence`, zero failures.**

> **This file replaces an earlier version that reached the wrong conclusion.**
> That version reported "r/m is deflated beyond Mash 0.002, a caller x
> reference-distance interaction" and recommended discarding 50 of 82 units. The
> distance correlation was real; the explanation was not. The cause is the
> external Reference taxon's branch. Nothing needs discarding and nothing needs
> re-running. The wrong version is preserved in git history and in §5 below,
> because the way it failed is instructive.

---

## §1 HEADLINE

**Median pooled r/m = 6.30** across 82 units (IQR 2.52–9.39, range 0.36–18.03),
after excluding the external reference's branches.

Use **`RM_RESULTS_L1_CORRECTED.tsv`**, column `rm_corrected`. Do not use
`RM_RESULTS_L1.tsv`, whose `rm_pooled` is uncorrected (median 1.85).

---

## §2 THE CORRECTION

The pipeline keeps the mapping reference as a taxon in the Gubbins input. This is
deliberate — it keeps the alignment full-length and the invariant-site counts
honest. But Gubbins then reconstructs substitutions along the branch leading to
that reference, and the reference is outside the population by construction, so
that branch is enormous. `strain_18_L1_1`, replicon 1:

```
(Reference:3859.691,( ...7 real genomes... )Node_6:3774.899)Node_7:0.000
```

Every real genome sits on a branch of 4–52. `Node_6` alone carried **7,307 of
7,574** SNPs outside recombination — 96%.

Those substitutions are divergence between the population and an outgroup, not
evolution within the population. Gubbins scores them "outside recombination"
because they are genome-wide rather than clustered, so they land in r/m's
denominator and crush the ratio:

| `strain_18_L1_1` | r/m |
|---|---|
| with reference branches | 0.42 |
| **without** | **8.73** |
| manual analysis, 7 taxa, ska_map | 9.14 |

**Which branches.** Gubbins emits an unrooted tree written with an arbitrary
root. Where the reference is the outgroup, its divergence is *split* between the
`Reference` leaf and the sibling clade at the root — 3859.7 and 3774.9, two
halves of one quantity. Excluding only the leaf leaves half the inflation
behind, so `exclude_reference_branches_bp.py` drops both children of the root
whenever one of them is `Reference`.

**Scale.** Across the run, **52% of all outside-recombination SNPs (458,688 of
881,582) came from reference branches.** The effect is sharply bimodal and
self-diagnosing:

| | units | median ref Mash | share of outside-SNPs from reference branches |
|---|---|---|---|
| `Reference` nests inside the population | 40 | 0.00133 | **0.0%** |
| `Reference` is a true outgroup | 42 | 0.00297 | **90.7%** |

---

## §3 VALIDATION AGAINST THE MANUAL ANALYSIS

35 of the manual analysis's 37 units are set-identical to units here, and the
Gubbins parameters match on both sides (the manual arms ran
`--invariant-site-correction --filter-percentage 25` with Gubbins' defaults —
5 iterations, min-snps 3, raxml — which is what this pipeline passes explicitly).
The remaining differences are the caller (`ska_map` vs `snippy`) and, for some
units, the reference.

| | corr(ref distance, log(new/manual r/m)) | IQR of new/manual | within 2× |
|---|---|---|---|
| before correction | **−0.589** | 0.40–1.54 | 22/36 |
| **after correction** | **−0.137** | **1.26–1.64** | **32/36** |

The apparent distance effect essentially vanishes, and agreement tightens into a
narrow band. The residual **~1.34× median offset is the real caller difference**
— consistent, directional, and small, which is what a caller effect should look
like. It is not noise and should be stated when comparing to the manual numbers.

---

## §4 WHAT THIS MEANS

- **All 82 units are usable.** The earlier recommendation to discard 50 was
  wrong.
- **Reference distance is no longer the dominant term.** After correction the
  split by distance is 7.74 (n=32, <0.002) vs 5.34 (n=50, ≥0.002) — a 1.45×
  difference, against 6.2× before. What remains is plausibly lineage biology
  plus the caller offset, not an artefact.
- **r/m is high in this organism**, on both methods, in nearly every unit.
- **The pipeline should be fixed** so this does not have to be corrected
  downstream every time. `drop_reference_taxon` exists as a param but dropping
  the taxon would lose the full-length alignment the reference provides. The
  right fix is for the summary stage to exclude reference-associated branches
  when it pools — i.e. do what `exclude_reference_branches_bp.py` does, inside
  the workflow.

---

## §5 HOW THE WRONG VERSION HAPPENED

Worth recording, because the reasoning looked sound at every step.

1. Compared against the manual analysis, found r/m disagreed badly on some units.
2. Found the disagreement correlated with reference distance (r = −0.589).
3. Controlled for reference identity — restricted to 19 units using the *same*
   reference — and the correlation **sharpened** to −0.823. That felt like
   confirmation.
4. Concluded: a caller x reference-distance interaction; 50 units unusable.

Step 3 is where it went wrong. Restricting to same-reference units *did* isolate
the caller as the only difference in the alignment — but it did not isolate the
only difference in the **Gubbins input**, which also included an extra taxon.
The correlation sharpened because the same-reference subset happened to span a
wider distance range, not because the caller hypothesis gained support.

The check that broke it open was the cheapest one available and should have come
first: **look at the per-branch numbers instead of the pooled ratio.** One
branch held 96% of the signal. A single `sort` on the per-branch statistics
would have shown that before any correlation was computed.

Prefer looking at the raw per-branch data over correlating derived summaries.
