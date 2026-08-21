# Unit re-derivation — result

2026-08-21 night. Closes `HANDOFF_2026-08-21_EVENING.md` §5 item 2. The four
affected units were re-derived, r/m recomputed through the pipeline's own
pooling code, spliced in, and `NUMBERS.tsv` regenerated.

---

## 1. What changed

| unit | n | r/m corrected | longest surviving branch |
|---|---|---|---|
| `strain_1_L1_8` | 91 → 89 | 5.9568 → **6.0061** | `GCF_006385955_1` 393 → 393 |
| `strain_14_L1_4` | 14 → 12 | 3.0728 → **3.2453** | `Node_1` 1100 → **1331** |
| `strain_1_L1_26` | 154 → 153 | 3.1042 → **4.4713** | **`SRR2896257` 1382 → `GCA_015320925_1` 362** |
| `strain_1_L1_10` | 7 → 4 | 1.0723 → **dropped** | below the n≥5 floor |

**`strain_1_L1_26` is the substantive one: r/m rose 44%, from 3.10 to 4.47.**

The reason is visible in the table and it is a clean confirmation of an existing
finding. `SRR2896257` — the `broken_assembly` genome the register excluded — was
**that unit's longest surviving branch, at 1,382 substitutions.** Removing it
dropped the longest remaining branch to 362, roughly a quarter. The unit's low
r/m was a divergent member sitting in the denominator, exactly the mechanism
recorded for the r/m spread, and removing one bad assembly moved the unit out of
the "≥1000-substitution surviving branch" category entirely.

`strain_14_L1_4` went the other way on branch length (1100 → 1331) and **stays**
in that category, so its 3.25 is still depressed for a reason this correction
does not address. Do not read it as a measurement.

`strain_1_L1_8` is unchanged in substance, as expected — the two duplicates it
lost were ordinary members.

## 2. Headline figures, before and after

| figure | before | after |
|---|---|---|
| analysed units | 86 | **85** |
| analysed genomes | 2,352 | **2,340** |
| median r/m, all units | 5.34 | **5.51** |
| median r/m, Gate 1 window | 7.26 (n=47) | **7.26 (n=47)** |
| median r/m, no divergent member | 7.26 (n=59) | **7.26 (n=59)** |

**The quotable r/m did not move.** Both filtered medians are unchanged, which is
the reassuring outcome: the defect was real but bounded, and it did not touch the
number the paper actually quotes. Only the all-unit median moved, and that one is
marked "do not quote" for independent reasons.

The two filtered sets are genuinely different (59 and 47 units, overlap 43) and
land on the same median by coincidence — the same unit sits at the middle of
both. Checked, not assumed.

## 3. The Gate 1 figure: 7.26 here, 7.38 in the 2026-08-19 documents — UNRESOLVED

`generate_numbers.py` hardcoded **"quote 7.38, the median of the 47 in-window
units"**, copied from `METHODS_DRAFT` §2.6.1. Recomputed from primary data the
in-window count reproduces at **exactly 47**, but the median is **7.26** —
before the re-derivation as well as after, so the re-derivation did not cause it.

**My first explanation was that 7.38 came from an 88-unit table and this one
holds 85, i.e. a denominator difference. That explanation is wrong, and it is
recorded here rather than quietly dropped.** Checking it:

- The 88-unit table is the 86 local units plus `strain_1_L1_36` (n=47) and
  `strain_1_L1_37` (n=8) — the two units computed on the A100 whose alignments
  never came back.
- `strain_1_L1_37` is outside the Gate 1 window (229 mean SNPs), but
  **`strain_1_L1_36` is inside it** (3,374). So if it had carried an r/m value
  the 88-unit in-window count would be 48, not the documented 47.
- Both counts are 47, so **the in-window set is the same 47 units in both
  cases.** The difference is therefore **in the r/m values themselves, not in
  which units were included.**

Corroborating this: the 2026-08-19 documents pair 7.38 with an **all-unit median
of 5.70**, while the table those documents are contemporaneous with
(`L1v4c_out/Summaries/recombination_rm.tsv`, written 2026-08-19 07:59) gives
**5.34** pre-splice. Two different r/m tables existed on the same day.

**What this means practically:**

- The current, reproducible figure from the pipeline's own output is
  **7.26 (n=47, 85-unit table)**, and it is now generated
  (`rm.gate1_units`, `rm.median_gate1`) rather than restated.
- **Do NOT mass-replace 7.38 with 7.26 in the corpus.** The 7.38 figures appear
  alongside "88 units" and "5.70", an internally consistent set. Overwriting one
  number inside a consistent set is how denominators get mixed — the error this
  project keeps catching.
- **Which table is authoritative is a call for whoever knows the 08-19 run
  history.** Until then quote 7.26 with its 85-unit denominator named, and treat
  the 0.12 gap as unexplained rather than as rounding.

⚠ Still open and now surfaced as `rm.gate1_caveat`: **Gate 1 diversity is still
the Mash proxy, not alignment distances** (`HANDOFF_2026-08-21_EVENING.md` §5
item 6). Window membership inherits whatever the proxy gets wrong.

## 4. The mechanism fix

`generate_numbers.py` was reading r/m from the **`unit_rm` column of
`L1v4c_MERGED_METADATA.tsv`** — a per-genome denormalised copy of a per-unit
quantity. That is the restate-rather-than-derive pattern the project set out to
eliminate, and it failed exactly as expected: after the re-derivation it still
read 3.1042 for `strain_1_L1_26`, and still carried a value for
`strain_1_L1_10`, a unit that no longer exists.

It now reads `L1v4c_out/Summaries/recombination_rm.tsv`, the pipeline's own
`POOL_RECOMBINATION_STATS` output, and falls back to the metadata column only if
that file is missing — labelling the fallback in the `source` field when it does.

The stale copies were also repaired in place (259 genome rows updated, 7 cleared
for the dropped unit), so other consumers of that column are not left wrong.

## 5. How it was run, and the one failure

`rederive_units_bp.sh`, parameters pinned to the production run (same container
digest, 5 iterations, RAxML, min-snps 3, `--invariant-site-correction`, filter
25%), because r/m shifts 0.47–0.78× with Gubbins settings and a unit computed
under different settings cannot be pooled with the other 82.

Pooling used the pipeline's own `bin/pool_recombination_stats.py` rather than a
reimplementation, so the reference-branch exclusion is identical.

**Both `strain_1_L1_26` replicons first failed at rc=135, "Bus error (core
dumped)", inside pyjar — after RAxML had already succeeded.** Not the zero-seed
bug, not a RAxML failure, not memory. The script omitted **`--shm-size=2g`**;
Docker defaults `/dev/shm` to 64 MB and pyjar allocates its
ancestral-reconstruction arrays there. The 90- and 13-taxon units passed, which
is the size threshold showing itself. `nextflow.config` sets the same 2g for the
same documented reason.

**If Gubbins dies with SIGBUS after RAxML has succeeded, it is `/dev/shm`.**

## 6. Files

| file | what |
|---|---|
| `rederive_units_bp.sh` | the driver |
| `rederive_2026-08-21/` | Gubbins outputs, 6 replicon-runs |
| `rederive_2026-08-21/recombination_rm_rederived.tsv` | pooled r/m for the 3 units |
| `rederive_2026-08-21/curated_L1v4c_clusters_corrected.tsv` | 85 units, 2,340 assignments |
| `L1v4c_out/Summaries/recombination_rm.tsv` | spliced; `.pre-rederive-2026-08-21.bak` is the original |
| `L1v4c_MERGED_METADATA.tsv` | `unit_rm` repaired; `.pre-rederive-2026-08-21.bak` is the original |
| `NUMBERS.tsv` | regenerated |
