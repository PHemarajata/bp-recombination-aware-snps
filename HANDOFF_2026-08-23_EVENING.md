# Handoff — 2026-08-23 evening

**Read this first.** Working directory `/home/phemarajata/Downloads/snp-mod-local-working`.
Supersedes `HANDOFF_2026-08-23.md` (morning), which remains accurate for the
frozen foundations but predates 26 commits. **Nothing is running.** Branch
`feat/core-shrinkage-and-itol`, clean, pushed.

**Every number below was recomputed 2026-08-23.** Run `git status -sb` rather
than trusting any push-state sentence in a file.

---

## 0. Before you quote anything

```bash
python3 generate_numbers.py    # regenerates NUMBERS.tsv (65 figures)
python3 freeze_basis_bp.py     # 15 checks, non-zero exit on drift
```

**Three frozen foundations:**

1. **The analysis basis** — `FINAL_BASIS_2026-08-22/`, **85 units, 2,340
   genomes**. Take unit membership only from `FINAL_PARTITION.tsv`. Join the
   panel on `unit_membership`, never `subcluster`.
2. **The validation set** — **48 registered, 46 scorable, 45 individuals** (two
   isolates are one patient). `EXPOSURE_OVERRIDES.tsv` and `OUTBREAK_GROUPS.tsv`
   are frozen inputs; changing either triggers a deliberate batched refresh.
3. **The exclusion register is versioned** — `PANEL_EXCLUSIONS.tsv` rows carry
   `status`; **`status=retired` is NOT an active exclusion** and every reader
   must filter it (five do). Retire via `retire_exclusions_bp.py`, never by hand:
   `*.tsv` is gitignored, so manual edits are invisible to git.

## 1. Headline numbers

| quantity | value | `NUMBERS.tsv` key |
|---|---|---|
| panel, corrected | **2,959** | `panel.corrected_v4d` |
| panel, region-labelled | **2,946** | `panel.region_labelled` |
| analysed units / genomes | **85 / 2,340** | `units.analysed`, `genomes.analysed` |
| ENA coverage | **41.1%** | `panel.coverage_of_ena` |
| r/m (Gate 1 in-window) | **7.70** (n=47 of 85) | `rm.median_gate1` |
| validation, scorable | **46** (48 registered, **45 individuals**) | `validation.scorable` |
| country, NN | **10/46 (21.7%)**, baseline **26.1%**, κ 0.193 | `attribution.country.nearest_neighbour` |
| country, close relative | **2/14** | `…nearest_neighbour.d_lt_0.05` |
| region, modal k=20 | **41/46 (89.1%)**, baseline 45.7%, κ 0.832 | `attribution.region.modal_k20` |
| region, close relative | **14/14** | `attribution.region.modal_k20.d_lt_0.05` |
| Asia vs non-Asia κ | **1.000** | `ladder.asia_vs_not.kappa` |
| abstention (region) | **94.3%** on 76.1% coverage, LOO | `abstention.region.loo_selective_accuracy` |
| cgMLST↔SNP concordance | **+0.861**, 66 of 85 at r≥0.7 | `CGMLST_CONCORDANCE_FROZEN.tsv` |

**Country does not exceed chance** — write it that way, never "reaches 22%".

**The estimator is part of every number.** Country's best is NN; region's is
modal k=20. `CGMLST_LICHT_ATTRIBUTION.tsv` holds **only NN**; modal and κ come
from `GROUPING_LADDER.tsv`.

**Never quote:** r/m 7.38/7.44/7.26 · region 93% (n=43) or 37/46 as the headline
· concordance 0.846 or 0.864 (pooled schemes) · panel 2,976 or 2,955 · coverage
44% or 41.4% · "7 of 15" source countries (now **7 of 16**) · downsampling
κ 0.89→0.81 (now **0.83→0.77**) · 48 as an attribution denominator · sub-national
association "0 of 88" (now **1 of 81**) · ST92 "four lineages" (now **three**).

## 2. Manuscript status — drafted

| section | file | state |
|---|---|---|
| Abstract | `ABSTRACT_DRAFT_2026-08-23.md` | 285 w + 146 w, verified |
| Results R1–R8 | `RESULTS_DRAFT_2026-08-23.md` | **every figure regenerable** |
| Discussion | `DISCUSSION_DRAFT_2026-08-23.md` | ~2,500 w, conclusion softened |
| Methods §2.1–2.11 | `METHODS_DRAFT_2026-08-19.md` | good shape |
| Methods §2.12 | same | rewritten on the frozen basis |
| Methods §2.12.11a | same | **written from scratch** |

`DRAFT_READINESS_2026-08-23.md` has the status table.

## 3. What this session established

**Results-bearing findings:**

- **Georgia is a second US autochthonous focus.** Five genomes, four patients,
  1983–2024, published as autochthonous with no travel (Brennan, PMID 40835221).
  **The Georgia cluster's internal max is 8.67×10⁻³ and its nearest non-Georgia
  neighbour is a Viet Nam case at 8.91×10⁻³ — one locus in 4,221.** Both
  countries represented, published epidemiology on both sides, attribution still
  fails. `VIETNAM_GEORGIA_RESULT_2026-08-23.md`
- **The two "independent" Viet Nam validation genomes are ONE patient.** Scoring
  does not leak (leave-group-out already held them apart) but the denominator is
  pseudoreplicated: 46 genomes, 45 individuals.
- **The estimator worked example.** Both Viet Nam genomes are wrong under NN at
  *every* scale including the deep split — their closest relative is a Georgia
  case — and modal k=20 recovers both. They are 2 of only 3 deep-split NN errors.
- **Abstention works for region, fails for country.** d ≤ 0.462 → 94.3% on 76.1%
  (LOO). Country's apparent +15.8pp is *exactly* cancelled by its retained-subset
  baseline. Two failure modes: attractor errors (catchable) vs depth-ceiling
  (not). `ABSTENTION_RESULT_2026-08-23.md`
- **The literature comparators corroborate rather than contradict.** Bayliss
  (PMID 37042517) — **this is the bare-URL eLife citation, and the source of our
  0.661** — shows the same monotonic decay with depth (0.954/0.718/0.661) and
  blames reference scarcity in its own discussion. Its split is a random
  country-stratified 75:25. DeepSANet (PMID 41185308) reports 80.8% country, but
  its released code sets `TEST_PATH == VAL_PATH` and picks the checkpoint by max
  val accuracy — **phrase as "in the released reference implementation"**, and
  note accuracy ≠ macro F1. `CITATION_AUDIT_2026-08-23.md`

**Corrections found by re-deriving on the frozen basis** — four figure sets were
re-run and **three contained wrong numbers**:

- R6 was entirely on the A100 88-unit control run. Re-run at all three scales:
  sub-national **1 of 81** (was 0 of 88 — does *not* survive), national 6 of 48,
  regional 1 of 17.
- R5 ST counts: ST92 spans **three** lineages not four; ST58 spans **five**
  countries not three; denominator **278** not 279.
- Four exclusions were **unevidenced** and are retired; the register never
  reached the cgMLST pool.
- `generate_numbers.py` was one register-edit away from reporting 2,341 analysed
  genomes; it now reads `FINAL_PARTITION.tsv`.

**Method questions closed:**

- **`+ASC` vs `-fconst` — RESOLVED.** §2.5 is right (`+ASC` estimates 41.9–72.1%
  GC, median 56.3%, against a true 68.1%; `-fconst` gives 67.6–68.7%, median
  68.1%) **but it changes no reported number** — every quantity derives from
  Gubbins outputs. `ASC_FCONST_RESULT_2026-08-23.md`
- **Support trees rebuilt with `-fconst`**: `L1v4c_TREES_SUPPORTED_FCONST/`,
  **170/170, 0 failures**. **Publish this set, not `L1v4c_TREES_SUPPORTED/`**
  (the `+ASC` set, retained for comparison).

## 4. Open items, ranked

1. **The reproducibility test** — re-run the collection end-to-end from primary
   data and diff every headline. Real compute (Gubbins hours; `--shm-size=2g`,
   the zero-seed trap). **Do it before submission**: of four figure sets
   re-derived today, three had at least one wrong number.
2. **Non-science submission blockers** — IRB approval number into Methods; data
   availability statement + **deposit the new assemblies**; pin the production
   command line (branch + commit).
3. **Figure 1 flow diagram** — every number exists, the figure does not:
   9,040 ENA BioSamples → 2,959 panel → 2,340 genomes in 85 units → 47 in-window.
4. **Batched refresh, when convenient** — register the same-patient Viet Nam pair
   in `OUTBREAK_GROUPS.tsv` (a no-op for current numbers, which is why it should
   be deliberate), and decide whether to drop the four retired genomes from the
   cgMLST pool.
5. **Obtain the DeepSANet PDF** and read its splitting section — paywalled, no
   lawful free copy found; corresponding authors are in
   `CITATION_AUDIT_2026-08-23.md` §5.2.3.
6. **Tech debt** — four scorers each build their own pool and all four apply
   leave-outbreak-out. `abstention_rule_bp.py` is the precedent for *not* adding
   a fifth: it consumes `GROUPING_PREDICTIONS.tsv` instead.
7. **`gate1_from_alignment_bp.py`** still defaults `--mash` to
   `trackA_diversity_86units.tsv` (note **86**, an older partition).
8. **Unciteable until resolved** — "Pearson 2020" (two conflicting PMIDs, one a
   materials-chemistry paper; searches return nothing).

**Decisions on record — do not relitigate:** don't redo the project; GAMBIT stays
on DB 2.2.0; Phase 1 expansion declined; workstation partition is reported, A100
is the control; the four retired exclusions stay retired; `ERR9980356` kept
knowingly despite ranking 172/172 on both QC axes.

## 5. Traps

**Carried forward:** Run `generate_numbers.py` before quoting. Deduplicate on
BioSample, never accession. Never compare an NN number to a modal one. Never
quote an accuracy without its baseline and denominator. Every ENA census unions
`read_run` with `result=assembly`. **Verify every PMID against a fetched record.**
On GAMBIT 3.x gate species on mash to K96243. Don't record a count until the run
producing it has stopped.

**Added today:**

- **The estimator is in the key.** `CGMLST_LICHT_ATTRIBUTION.tsv` is NN-only.
- **Honour `status=retired`** in `PANEL_EXCLUSIONS.tsv`.
- **`units.analysed` / `genomes.analysed` come from `FINAL_PARTITION.tsv`**,
  never from `curated_L1v4c_clusters.tsv` minus the registers — that file is
  pre-correction (2,352 rows) and still lists `SRR2896257`.
- **`CGMLST_CONCORDANCE_FROZEN.tsv` holds BOTH schemes** (170 rows = 85 × 2).
  Restrict before taking a median: Lichtenegger 0.861, pooled 0.864.
- **`L1v4c_out/Clusters` is hybrid: 176 dirs = 88 units × 2 replicons**, against
  a frozen 85. Never glob it for membership.
- **Globbing `<unit>__*` matches BOTH replicons in arbitrary order.** This bit me
  twice today. Construct replicon-unit paths exactly.
- **A selective accuracy needs TWO baselines** — random-abstention *and* the
  majority share of the *retained* subset.
- **A QC gate is assembler-dependent.** SKESA→SPAdes moves core +10.8pp and mash
  −27% per genome; no global correction factor.
- **`0.008` is not the operative mash gate** — prose only; code enforces ≤0.012.
- **Beware rounding when validating against stored values.** The region baseline
  is stored 4-dp as `0.4565`; the true 21/46 = 45.652% rounds to **45.7%**, but
  `round(45.65,1)` in Python gives 45.6.

## 6. Key documents

| file | what |
|---|---|
| **`NUMBERS.tsv`** | every quotable figure. Start here |
| `ABSTRACT_DRAFT` / `RESULTS_DRAFT` / `DISCUSSION_DRAFT` `_2026-08-23.md` | the manuscript |
| `DRAFT_READINESS_2026-08-23.md` | what is and is not ready |
| `VIETNAM_GEORGIA_RESULT_2026-08-23.md` | the trans-Pacific lineage, one-locus boundary |
| `ABSTENTION_RESULT_2026-08-23.md` | the abstention rule, both baselines |
| `ASC_FCONST_RESULT_2026-08-23.md` | +ASC vs -fconst, resolved |
| `CITATION_AUDIT_2026-08-23.md` | 13 verified, 6 resolved, the comparators |
| `EXCLUSION_RECHECK_2026-08-23.md` | the four exclusions re-measured |
| `FINAL_BASIS_2026-08-22/README.md` | the frozen basis and its rules |
| `PANEL_EXCLUSIONS_README.md` | register spec: `status`, the `core=na%` trap |
| `GROUPING_LADDER.tsv` / `GROUPING_PREDICTIONS.tsv` | κ ladder; per-genome calls + confidence |
| `PHYLOGEO_FROZEN_{subnational,national,regional}_2026-08-23.tsv` | R6, all scales |
| `L1v4c_TREES_SUPPORTED_FCONST/` | **publish these** (170 trees) |
