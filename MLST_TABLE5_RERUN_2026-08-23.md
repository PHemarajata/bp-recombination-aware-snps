# Table 5, MLST row: re-run on the current validation set — and it is not a number

2026-08-23 evening. The MLST row of Table 5 predated the validation-set
correction and was due a re-run on n = 46. Re-running it produced a result the
old row could not have shown: **at MLST resolution, nearest-neighbour is not a
well-defined estimator**, and the row should not report a bare accuracy.

---

## 1. How it was re-run — no fifth scorer

The handoff's tech-debt item says not to add a fifth scorer, because the four
that exist each rebuild the reference pool and each re-implement
leave-outbreak-out, and that is where they drift. So nothing new was written to
*score* anything. Instead:

- `mlst_to_allele_table_bp.py` reshapes `MLST_v4c.tsv`'s 7-locus profile into
  the same wide `FILE + one column per locus` table the cgMLST scorer already
  eats (`MLST_ALLELES_WIDE.tsv`, 2,976 genomes × 7 loci: ace, gltB, gmhD, lepA,
  lipA, narK, ndh).
- `score_cgmlst_lichtenegger.py` and `grouping_test_bp.py` then run over it
  unchanged, via a new `--profiles` / `--out-prefix` pair.

`grouping_test_bp.py` previously hardcoded its input and output paths. It now
takes both as arguments, **with defaults that reproduce the frozen cgMLST ladder
byte-for-byte** — verified by md5 before and after
(`GROUPING_LADDER.tsv` `2993f4f9…`, `GROUPING_PREDICTIONS.tsv` `e9ef4669…`).

The MLST and cgMLST rows of Table 5 are therefore produced by the *same code
path*, including pool construction, exposure overrides, leave-group-out and
leave-outbreak-out. They are comparable by construction rather than by
inspection.

## 2. What came out — and the disagreement that mattered

MLST covers **33 scorable** validation genomes (35 with a profile, less the two
non-country exposures), against cgMLST's 46.

The two code paths **agreed exactly on cgMLST and disagreed on 21 of 33 MLST
country calls.** That disagreement is the finding, not a bug in either.

| | MLST, 7 loci | cgMLST, 4,221 loci |
|---|---|---|
| validation genomes | 33 | 38 † |
| **queries with a UNIQUE nearest neighbour** | **3 of 33** | **38 of 38** |
| tied-for-nearest set size | median **21**, max 52 | median **1**, max 1 |
| true country somewhere in the tied set | 8 of 33 | 7 of 38 |

† the tie diagnostic is a standalone script and its denominator does not match
the frozen 46; it reconstructs the pool approximately. The tie-set contrast —
median 1 against median 21 — is far too large to be an artifact of that, but do
not quote 38 as a validation denominator.

**At 7 loci the "nearest neighbour" is an arbitrary pick from a median of 21
equidistant genomes.** `np.argsort` breaks the tie by index order, so the answer
depends on how the candidate pool happened to be enumerated — which is exactly
why two faithful implementations disagreed 21 times.

## 3. What the row should say

Not "0/33" and not "4/33". Both are real draws from an arbitrary tie-break, and
reporting either as a measurement would be the same category error this project
keeps catching elsewhere.

The defensible statement is a **bound**:

> At MLST resolution the nearest neighbour is not unique for 30 of 33
> validation genomes (median tied set 21). The true country appears anywhere in
> the tied set for **8 of 33**, so *no* tie-breaking rule can score above
> **8/33 (24%)**, and an adversarial one scores 0. **The majority baseline is
> 12/33 (36%).** Even an oracle tie-break therefore fails to reach chance.

That is stronger than the old "0/17", and it does not depend on a tie-break.

**Region, modal k = 20** — the estimator Table 5's region column uses — is far
less tie-sensitive because it aggregates 20 neighbours rather than one:
**19/33 (57.6%), baseline 15/33 (45.5%), κ 0.343** (`MLST_GROUPING_LADDER.tsv`).
It is still drawn partly from tied sets and should carry that caveat.

## 4. The corrected Table 5

| layer | loci | country | region |
|---|---|---|---|
| MLST **[MLST/33]** | 7 | **≤ 8/33 (24%)**, baseline 36% — NN not unique for 30 of 33 | 19/33 (58%), baseline 46%, κ 0.343 |
| **cgMLST [cg-Licht/46]** ← use this row | 4,221 | **10/46 (22%)**, baseline 26%, κ 0.193 | **41/46 (89%)**, baseline 46%, κ 0.832 |
| core-genome SNP **[SNP/24]** | whole genome | 0/24 | 22/24 (92%) |

**This strengthens R3 rather than complicating it.** The old row's region figure
was 13/15 (87%), which sat awkwardly close to cgMLST's 89% and quietly undercut
the claim that resolution buys region-level accuracy. On the corrected
validation set the region ladder is **monotonic in loci — 58% → 89% → 92%** —
while country stays at or below its baseline at every rung. The resolution curve
(Figure 2) and this table now say the same thing.

## 5. Caveats to carry

- **Denominators differ by row** (33 / 46 / 24) because each typing system
  covers a different set of genomes. Already disclosed in the outline; keep it.
- **The MLST region number is not tie-free either**, only tie-*tolerant*. If a
  reviewer presses, the honest answer is that modal k = 20 aggregates over a
  neighbourhood that is itself partly arbitrary at this resolution.
- **Do not compare the MLST NN bound to the cgMLST NN accuracy as like for
  like.** One is a bound over all tie-breaks, the other a point estimate with a
  unique neighbour. Say so wherever both appear.

## 6. Reproduce

```bash
python3 mlst_to_allele_table_bp.py
python3 score_cgmlst_lichtenegger.py --profiles MLST_ALLELES_WIDE.tsv --out-prefix MLST_ATTRIBUTION --estimator nearest_neighbour
python3 grouping_test_bp.py --profiles MLST_ALLELES_WIDE.tsv --out-prefix MLST_GROUPING
```

Outputs: `MLST_ATTRIBUTION_{ATTRIBUTION,SUMMARY}.tsv`,
`MLST_GROUPING_{LADDER,PREDICTIONS}.tsv`.
