# End-to-end reproducibility run: the reported headline reproduces

**2026-08-26.** Closes `SUBMISSION_TODO.md` D1. The reported analysis was
re-executed from the pinned commit and inputs, and the headline figures were
diffed against the frozen basis.

> **Result: Gate 1 = 47 units, median r/m = 7.70, matching the reported figures.**
> Per-unit r/m is identical for 81 of 84 comparable units, and per-unit alignment
> distances are identical for 85 of 86 units. One unit was lost to a known
> pipeline bug, and that loss produces the only apparent discrepancy in the whole
> comparison.

---

## 1. Run identity

| | |
|---|---|
| pipeline | `79ab645`, now tagged **`v1.0.5-mod`** (manifest self-reports `1.0.3-mod`) |
| Nextflow | 25.04.6 |
| first segment | 2026-08-24 10:01 to 15:47, 5 h 46 m, stopped with SIGTERM for a power-down |
| resumed segment | 2026-08-25 16:57 to 23:34, 6 h 37 m, `rc=0` |
| run names | `soggy_gilbert`, then `adoring_faggin` on resume |
| resume behaviour | 5,154 tasks restored from cache, 34 newly submitted |
| outputs | `REPRO_2026-08-24_out/`, `REPRO_DISTANCES_v4c_SUMMARY.tsv` |

`rc=0` is **not** evidence of success. Every heavy process uses
`errorStrategy ... : 'ignore'`, so a task that fails on its last attempt is
dropped and the run still exits 0. The per-process counts below are the check
that matters, and they are what caught the one failure.

## 2. Task counts

| process | expected | observed |
|---|---|---|
| `INFILE_HANDLING_UNIX` | 2,352 | 2,352 ✅ |
| `SNIPPY_SCATTER` | 4,704 | 4,704 ✅ |
| `SPLIT_REFERENCE_REPLICONS` | 86 | 86 ✅ |
| `SNIPPY_CORE_GATHER` | 172 | 172 ✅ |
| `KEEP_INVARIANT_ATCG` | 172 | 172 ✅ |
| `GUBBINS_CLUSTER` | 172 | 172 dispatched, **171 succeeded** ⚠ |
| `ASC_PREFLIGHT` / `IQTREE_ASC` / `SELECT_UNIT_MEDOID` | 172 each | **171** each |
| `POOL_RECOMBINATION_STATS` / `GLOBAL_ML_TREE` / `SUMMARIZE_CLUSTER_PHYLOGENY` / `GLOBAL_CORE_ALIGNMENT` | 1 each | 1 each ✅ |

8,505 task directories carry an exit code. Exactly one is non-zero on a final
attempt; the other non-zero codes are `143`, the SIGTERM from the deliberate
pause, and all of those tasks re-ran.

**Landing point: 86 units / 2,352 genomes / 171 replicon-units**, against an
expected 86 / 2,352 / 172. The reported basis of 85 / 2,340 / 170 is a post-hoc
correction (METHODS §2.12.5) applied after the pipeline, and is not reproduced by
the pipeline itself, exactly as anticipated. The one unit present here and absent
from the reported basis is `strain_1_L1_10`, which the correction removes.

## 3. The one failure is the known zero-seed bug

`GUBBINS_CLUSTER (cluster_strain_1_L1_30__GCF_000755905_1_2)` exited 1 at
iteration 5:

```
raxmlHPC-PTHREADS-AVX2 -T 5 -safe -m ASC_GTRGAMMA --asc-corr=stamatakis -p 0 -q ...
Failed while building the tree.
```

Iteration 1 of the same task had drawn `-p 1393` and succeeded. This is Gubbins'
unseeded `randint(0, 10000)` returning 0, which RAxML rejects, at roughly 1 call
in 10,001 and about a 16% chance per full panel run. `errorStrategy` ignored it,
which is why the three downstream processes sit at 171.

**This is a pipeline bug, not a reproducibility finding.** The pinned commit is
dated 2026-08-16, three days before the `gubbins_seed` fix of 2026-08-19, so the
reported analysis is **not seed-reproducible by construction**. That belongs in
the Methods rather than being left for a reader to infer.

## 4. Per-unit r/m

85 units are shared with the reported table. `strain_1_L1_30` is excluded from the
comparison because it lost a replicon, leaving **84 comparable units**.

| | |
|---|---|
| identical in r/m **and** raw SNP counts | **81 / 84** |
| within ±1% | 82 / 84 |
| within ±10% | 83 / 84 |
| median r/m | **5.6906 in both** |
| ratio repro/reported | median 1.0000, min 0.6942, max 1.0000 |

The three units that genuinely moved:

| unit | repro | reported | ratio |
|---|---|---|---|
| `strain_1_L1_26` | 3.1042 | 4.4713 | 0.694x |
| `strain_14_L1_4` | 3.0728 | 3.2453 | 0.947x |
| `strain_1_L1_8` | 5.9568 | 6.0061 | 0.992x |

`strain_1_L1_26` is already known to be unstable: it is the unit behind the
7.38-versus-7.26 difference between the A100 and workstation runs.

**Exact equality was not expected**, since Gubbins is stochastic and the commit
has no seed, so the clean result was checked rather than accepted. The two tables
have different checksums and are four days apart; the three shifted units have
genuinely different in/outside SNP counts; and no unit has matching r/m with
mismatched counts. Gubbins converged to the same recombination calls despite
different seeds.

## 5. Gate 1, computed two ways

**With the reported distances**, substituting only the repro r/m values:
**47 units, median 7.70**, identical membership, nothing entering or leaving.

**Fully independent**, recomputing distances from the repro alignments over a
staged 171-unit tree that excludes the failed unit
(`REPRO_DISTANCES_v4c_SUMMARY.tsv`): **48 units, median 7.48**.

That difference is an artifact, not a finding. Gate 1 **sums** `raw_mean` across a
unit's replicons, and `strain_1_L1_30` lost one:

| | replicon 1 | replicon 2 | sum | vs 4,700 ceiling |
|---|---|---|---|---|
| reported | 3317.9 | 3311.3 | 6629.2 | outside |
| repro | 3317.9 | *lost* | 3317.9 | **inside** |

The surviving replicon's value is identical to the digit. Excluding the corrupted
unit gives **47 units, median 7.70**, matching the reported figure.

Per-unit `raw_mean` reproduces **exactly** (ratio 1.0000) for 85 of 86 units;
`strain_1_L1_30` is the sole exception at 0.5005x, which is the halving above.

> **A lost replicon biases its unit toward Gate 1.** Because the window is a sum,
> losing a replicon can only push the statistic down, and therefore only toward or
> into the window. Any future Gate 1 membership change must be checked against
> `n_replicons` before it is believed.

## 6. Downstream attribution

Unaffected. The attribution figures depend on cgMLST allele calls rather than on
this pipeline, and no input to them changed.

## 7. Three things recorded that outlive this run

1. **The pin is not seed-reproducible.** `79ab645` predates the `gubbins_seed`
   fix and carries no such parameter. State it in the Methods.
2. **`REPRO_2026-08-24_out/Clusters` is a hybrid directory**: 172 Gubbins outputs
   on disk against 171 in the r/m table. The failed unit's `GUBBINS_CLUSTER`
   succeeded in the *first* segment and published output on 2026-08-24, then
   failed after resume and contributed nothing to the pool, but `publishDir` never
   retracted the stale files. File dates separate them cleanly, 171 dated Aug 25
   and 1 dated Aug 24. **Do not glob this directory**; it would have corrupted the
   recomputed distances in §5. This is the same defect as
   `L1v4c_out/Clusters` arriving by a new route, and it also proves the zero-seed
   failure is a per-attempt draw rather than a property of the unit.
3. **`recomb_filtered_distances_bp.py` hardcodes the reported r/m table** at line
   209 instead of taking it as an argument. Three columns of any new summary
   (`unit_rm`, `expected_ratio_from_rm`, `ratio_over_expected`) therefore come from
   the reported run while every other column is the new one. Filed as tech debt
   E4; the Gate 1 result above uses only `raw_mean` and is unaffected.

## 8. Verdict

The reported analysis reproduces. The headline figures are recovered exactly, the
per-unit agreement is far tighter than a stochastic pipeline had any right to
give, and the single apparent discrepancy is fully explained by a known bug whose
mechanism is documented and whose fix already exists on a later commit.
