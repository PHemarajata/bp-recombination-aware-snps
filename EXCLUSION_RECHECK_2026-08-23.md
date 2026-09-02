# Exclusion re-check — four PANEL_EXCLUSIONS rows, and the cgMLST reference pool

2026-08-23. The evidence gap behind four register rows, closed by measurement.
No scorer was re-run and no attribution artifact was regenerated — see
**§6 What was deliberately not done**.

Register rows under review, all `evidence = NEW200_QC_2026-08-17.tsv`,
`decided = 2026-08-17`, `status = final`:

| sample | reason_class | register evidence string |
|---|---|---|
| `SRR2896257` | broken_assembly | core coverage <85% or ratio >1.20; mash=0.0098, **core=na%**, ratio=1.14 |
| `SRR2896259` | broken_assembly | core coverage <85% or ratio >1.20; mash=0.0097, **core=na%**, ratio=0.92 |
| `ERR9980356` | broken_assembly | core coverage <85% or ratio >1.20; mash=0.0102, **core=na%**, ratio=0.96 |
| `SRR2896271` | wrong_species_or_divergent | gambit/mash: not *B. pseudomallei* or grossly divergent; mash=0.0135, **core=na%**, ratio=0.94 |

## 1. The finding in one paragraph

**Core coverage was measured. It was never missing.** It is in
`NEW200_QC_2026-08-17.tsv` under `core_cov_unfiltered_pct` — 80.7, 81.5, 83.1
and 71.9% — while the register transcribed the *adjacent* `core_cov_filtered_pct`
column, which is empty for every row in that file. So `core=na%` is a
transcription artifact, not an unmeasured field, and on the SKESA batch **all
four genuinely fail the <85% core gate**. The exclusions were evidenced.

**But they were evidenced against an assembly nothing uses.** The panel and the
cgMLST reference pool both use the SPAdes re-assemblies, and on those, **all four
pass every gate** — core 86.2–93.3%, gene ratio 0.89–0.97, mash 0.0065–0.0093,
all inside the operative thresholds. This is not a new measurement: the SPAdes
re-QC of 2026-08-18 already recorded all four as `pass` with empty
`fail_reasons` (`SPADES_QC_2026-08-17.tsv`). That result was never reconciled
against the register.

## 2. Provenance — the register was written after the re-QC that superseded it

`reqc_spades_batch.py:162` marks any sample present in `PANEL_EXCLUSIONS.tsv`
with `excluded:<reason_class>` and forces `verdict = fail`, before any gate is
applied. That mechanism demonstrably fired: **19** register members carry an
`excluded:` string in `SPADES_QC_2026-08-17.tsv`, including
`ERR8098257`, `SRR30648669` and all 13 `duplicate` rows.

These four carry **no** `excluded:` string and `verdict = pass`. They were
therefore **not in the register when the SPAdes re-QC ran** (2026-08-18 02:52).
The register file's mtime is 2026-08-20 20:49; its rows are back-dated
`decided = 2026-08-17`. The four rows were written from the superseded SKESA
measurements after the SPAdes evidence already existed.

## 3. Method

Re-measured independently by `verify_exclusions_bp.py`, reimplementing the
gate definitions from `reqc_spades_batch.py` so both assemblers are directly
comparable:

- **core completeness** — `minimap2 -x asm10` vs `refs/K96243.fasta`, PAF
  MAPQ ≥ 10, reference intervals merged per target, divided by 7,247,547 bp.
  Gate **≥ 85%**.
- **base accuracy** — prodigal single-mode gene count ÷
  (821 × assembly_Mb + 1.0 × contigs≥500). Gate **≤ 1.20**.
- **species/divergence** — `mash -s 10000 -k 21` to K96243, the sketch size the
  0.008/0.012 thresholds were calibrated at (**not** the `-s 50000` the
  partition uses). Operative code gate **≤ 0.012**.

SPAdes assemblies were read from `additions/fasta_spades/` — the exact paths in
`cgmlst_lichtenegger/MANIFEST.tsv`. Their sequence content is byte-identical
(case-normalised, headers stripped) to the `bp_spades_assemblies/` copies the
re-QC measured, so the two runs are comparable. Excluded genomes were never
copied into `additions/fasta_new200/`, so their SKESA assemblies were read from
the raw TheiaProk delivery at `bp_new_assemblies/`.

**Controls all reproduce**, which is what licenses the target numbers:

| control | expectation | measured |
|---|---|---|
| `ERR8098257` SPAdes | register row that genuinely fails core on SPAdes, 81.3% | **81.3%** ✓ |
| `SRR30648682` SKESA | override row: "passes every gate (mash 0.0072, core 92.2%, ratio 0.96)" | **0.0073 / 92.2% / 0.95** ✓ |
| `SRR30648682` SPAdes | override row: 11.88 Mb, foreign content | **11.88 Mb, mash 0.0205, fail** ✓ |
| `SRR28096039/43` SKESA | `C_pass`, core 100.0%, mash 0.0065/0.0063 | **100.0% / 0.0065, 0.0063** ✓ |

## 4. Measurements

| sample | assembler | core % | mash | ratio | length | ctg≥500 | N50 | verdict |
|---|---|---|---|---|---|---|---|---|
| `SRR2896257` | **spades (in pool)** | **90.5** | 0.0077 | 0.89 | 7,452,260 | 3,315 | 3,160 | **pass** |
| | skesa (decided on) | 80.7 | 0.0098 | 1.14 | 5,827,429 | 4,611 | 1,431 | fail: core |
| `SRR2896259` | **spades (in pool)** | **93.3** | 0.0065 | 0.97 | 6,956,968 | 826 | 15,849 | **pass** |
| | skesa (decided on) | 81.5 | 0.0097 | 0.92 | 6,088,458 | 2,660 | 3,192 | fail: core |
| `ERR9980356` | **spades (in pool)** | **86.2** | 0.0093 | 0.90 | 6,793,904 | 2,403 | 4,219 | **pass** |
| | skesa (decided on) | 83.1 | 0.0102 | 0.96 | 6,264,441 | 2,874 | 3,014 | fail: core |
| `SRR2896271` | **spades (in pool)** | **89.1** | 0.0087 | 0.97 | 6,751,137 | 1,203 | 10,056 | **pass** |
| | skesa (decided on) | 71.9 | **0.0135** | 0.94 | 5,469,807 | 2,987 | 2,366 | fail: core + mash |

The SKESA core values reproduce `core_cov_unfiltered_pct` exactly (80.7, 81.5,
83.1, 71.9), confirming §1.

**Scale for the SPAdes numbers.** Across the 172 passing SPAdes assemblies:
core min 86.2, p05 92.5, p25 96.0, median 96.8; mash min 0.0014, median 0.0059,
p95 0.0067, max 0.0093. So all four sit in the bottom tail of a passing
distribution — `ERR9980356` **is** the minimum core and the maximum mash of the
entire passing set, and only **2 of 172** passing genomes exceed mash 0.008
(`SRR2896271` 0.0087 and `ERR9980356` 0.0093).

## 5. Verdict per genome

| sample | exclusion is | why |
|---|---|---|
| `SRR2896259` | **UNSUPPORTED** | Cleanest of the four. Core 93.3% (above p05), mash 0.0065 (batch median), ratio 0.97, 826 contigs at N50 15.8 kb. Nothing distinguishes it from a routine pass. |
| `SRR2896257` | **UNSUPPORTED, with a caveat** | Passes every gate (core 90.5%, ratio 0.89, mash 0.0077). But 3,315 contigs is the most fragmented assembly in the batch, and 7,452,260 bp exceeds the original 7.4 Mb bound — it is inside the gate only because the bound was raised to 7.6 Mb for the SPAdes round. Fragmentation is the confounder of record for accessory analysis; it is not a core-attribution gate. |
| `ERR9980356` | **AMBIGUOUS** | Passes both gates, but is simultaneously the **weakest passing assembly in the batch on both axes** — core 86.2% (rank 172/172) and mash 0.0093 (rank 172/172). A defensible gate at core ≥ 87% or mash ≤ 0.009 would exclude it and nothing else. The exclusion is not evidenced as written, but this is the one genome where re-inclusion is a judgement call rather than a correction. |
| `SRR2896271` | **UNSUPPORTED as `wrong_species_or_divergent`** | See §5.1. |

### 5.1 SRR2896271 — the species claim, checked independently

The task premise is that at `mash_K96243 = 0.0135` it fails a ≤0.008 species gate
on mash alone and should be excluded regardless of core coverage. Checked, and
**the premise does not hold for the assembly in the pool**:

1. **The 0.0135 is real and reproducible — on SKESA.** Independently re-measured
   at exactly **0.0135**. On that assembly it fails both the ≤0.012 code gate and
   the core gate (71.9%). Nothing in the register is fabricated.
2. **The pool does not contain that assembly.** `cgmlst_lichtenegger/MANIFEST.tsv`
   points to `additions/fasta_spades/SRR2896271.fasta`, which measures
   **0.0087** — below the operative **≤0.012** gate in `reqc_spades_batch.py:164`.
3. **0.008 is not the operative gate.** It appears in prose only
   (`PANEL_EXCLUSIONS_README.md`, `BATCH3_QC_REPORT_2026-08-21.md`, which calls
   it "the stricter 0.008 threshold"). The threshold enforced in code is 0.012.
   At 0.0087 the genome is over the advisory line and under the enforced one.
4. **It is not a different species.** Confirmed wrong-species genomes in this
   register sit at core 18.2–50.2% with mash 0.0222–0.0635. The one true
   *B. thailandensis* (`SRR30648669`) is core 87.5% but **mash 0.0635 — 7×
   higher**. `SRR2896271` at core 89.1% / mash 0.0087 is not in that regime: a
   non-*pseudomallei* genome does not align 89% of K96243 at `asm10`.
5. **GAMBIT agrees, on the trustworthy database.** NEW200 ran before the GAMBIT
   3.0.0 regression that calls *B. pseudomallei* as *B. mallei* 40/40; its call
   here is `Burkholderia pseudomallei` under the older 2.2.0-era database.

So the correct reading is **divergent, not wrong-species** — and the divergence
is largely a SKESA artifact, since the same isolate measures 0.0087 under SPAdes.
It remains 1 of only 2 passing genomes above the advisory 0.008. Note both
`SRR2896271` and `SRR2896259` are Papua New Guinea; elevated divergence in
PNG/Australian lineages is expected biology, but `SRR2896259` measures 0.0065,
so this is an observation, not an explanation.

## 6. What this is worth — the blast radius, measured

Scope is bounded, and it is small. In `CGMLST_LICHT_ATTRIBUTION.tsv` (46 country
+ 46 region rows), exactly **two rows** have one of the four as nearest
neighbour, both the same genome:

| genome | scale | NN | d | correct |
|---|---|---|---|---|
| `SRR33748081` | country | `SRR2896257` | 0.79048 | **0** |
| `SRR33748081` | region | `SRR2896257` | 0.79048 | 1 |

`SRR2896259`, `ERR9980356` and `SRR2896271` are **never** a nearest neighbour for
any validation genome. And **d = 0.79048 is the maximum NN distance in the entire
validation set** (n=46, min 0.00664, median 0.23182, p90 0.64119). `SRR33748081`
is the single most isolated validation genome; its "nearest neighbour" is the
furthest of all 46. At 2,520 loci compared, ~79% of loci differ — not a relative
in any meaningful sense.

Consequences if the four were dropped from the pool:

- **Country 10/46 cannot fall.** `SRR33748081`'s country call is already wrong;
  a different NN can only leave it wrong or make it right. So country is
  **10/46 or 11/46**.
- **Region 41/46 can fall by at most one.** Its region call is currently correct;
  it survives only if the replacement NN is also East Asia & Pacific. So region
  is **40/46 or 41/46**.
- `GROUPING_LADDER.tsv` holds no sample IDs and inherits whatever the attribution
  table says.

## 7. What was deliberately not done

No scorer was re-run and `CGMLST_LICHT_ATTRIBUTION.tsv` / `NUMBERS.tsv` were not
regenerated. Dropping these genomes moves a frozen headline (region 41/46,
country 10/46), and that must go through a deliberate batched refresh —
register → regenerate attribution → recompute strata → propagate n — on the
model of `TRACK0_INTEGRATION_2026-08-23.md`. Reporting and stopping here.

`freeze_basis_bp.py` was run before and after this work: **14/14 PASS** both
times. The frozen basis never contained any of the four
(`FINAL_PARTITION.tsv` and `FINAL_PANEL.tsv` both grep to 0); this was only ever
a reference-pool problem.

`EXPOSURE_OVERRIDES.tsv`, `OUTBREAK_GROUPS.tsv` and the frozen partition were not
touched. `PANEL_EXCLUSIONS.tsv` was **not** edited — the decision below is the
user's to make.

## 8. Recommendation

The evidence supports **three separate decisions, not one**:

1. **`SRR2896259` and `SRR2896257` — retire the register rows.** Both pass every
   gate on the assembly in use, and the rows rest on a superseded assembler plus
   a mis-transcribed column. Keeping them is not conservatism; it is an
   unevidenced exclusion that a reviewer can reproduce as unevidenced. If
   `SRR2896257` is dropped anyway, drop it for **fragmentation** (3,315 contigs,
   7.45 Mb), stated as such — not for core coverage.
2. **`ERR9980356` — a real judgement call.** Rewrite the row either way. It
   passes, but it is the weakest passing assembly in the batch on both axes
   simultaneously. Excluding it needs a stated gate (core ≥ 87% or mash ≤ 0.009)
   applied to the whole panel, not to this genome alone.
3. **`SRR2896271` — reclassify, do not simply delete.** `wrong_species_or_divergent`
   is wrong as written: it is *B. pseudomallei* by mash, by core alignment and by
   GAMBIT on the good database. If it is excluded, the reason is *divergence
   above the advisory 0.008 line under a SKESA assembly that is no longer used* —
   which is a weak reason, and it should be said plainly.

Whichever way each goes, two follow-ups are independent of the decision:

- **Extend the register cross-check to the cgMLST manifest**, not just the
  partition. `freeze_basis_bp.py` passes 14/14 today precisely because it never
  looks at `cgmlst_lichtenegger/MANIFEST.tsv`.
- **Fix the transcription bug at source.** Any future register row sourced from
  `NEW200_QC_2026-08-17.tsv` must read `core_cov_unfiltered_pct`;
  `core_cov_filtered_pct` is empty for every row in that file and will silently
  produce another `core=na%`.

## Files

- `verify_exclusions_bp.py` — the re-measurement, read-only.
- `EXCLUSION_RECHECK_2026-08-23.tsv` — 14 rows: 4 targets × 2 assemblers,
  plus 3 controls.
