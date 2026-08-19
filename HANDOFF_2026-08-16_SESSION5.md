# Session handoff — 2026-08-16 (session 5)

Supersedes `HANDOFF_2026-08-15_SESSION4.md` for everything it covers. **The
analysis is COMPLETE and the results are on the external drive.** This session
finished the run, found and fixed two defects that were changing the answers,
built the deliverables, and moved global-tree generation into the pipeline.

---

## §0 READ THIS FIRST — the pattern that caught every real bug

Every defect found across sessions 4 and 5 was caught the same way: **by looking
at raw per-item numbers, not at summaries or correlations.**

| what looked true | what the raw numbers showed |
|---|---|
| "three reference genomes break Gubbins" | RAxML segfaults at a 128-character run id; the three just had long filenames |
| "r/m is deflated by a caller × reference-distance interaction" | one branch held **96%** of the signal — the external reference's |
| "the groupKey fix will shorten the run" | it redistributes work; on a saturated box it is a wash |
| "resume will reuse the previous run" | `-resume` picks the LAST session, including `-preview` ones |

**The second row is the important one.** That wrong diagnosis was written up,
nearly discarded 50 of 82 units, and was reached by a chain of reasoning that got
*stronger* at each step — restricting to same-reference units sharpened the
correlation from −0.589 to −0.823, which felt like confirmation. It wasn't. A
single `sort` on the per-branch statistics would have shown the truth before any
correlation was computed.

**Prefer the raw per-item view over the derived summary.**

---

## §1 STATE

- **Nothing running.** ~250 GB free locally; external drive TB1 has 698 GB free.
- Pipeline `~/wf-assembly-snps-mod`: branch **`reference-blocklist`** at
  **`f1a7d13`**, 5 commits ahead of `main` (`a28a96c`). **Not merged, not pushed.**
- Results: `L1_out/` (first run) and `L1_clean_out/` (cold re-run). Work dirs
  `L1_work` deleted; `L1_clean_work` retained.
- **Deliverables exported to `/media/phemarajata/TB1/snp_results_2026-08-16/`**
  — 686 files, 26 MB. Read its `README.txt` first.

### Commits this session

| commit | what |
|---|---|
| `0a58a86` | `--reference_blocklist` (mechanism kept; **list is now empty**) |
| `7515f1b` | reject unit ids that would segfault RAxML |
| `10f04b5` | retract the bad-reference claim |
| `04e8308` | `groupKey` so clusters gather as soon as mapped |
| `1916597` | A100 profile retuned from measured trace |
| `f1a7d13` | **global ML tree across units, with support, in both modes** |

---

## §2 THE RESULTS

**82 units, 2,070 genomes (73.9% of 2,802), 164/164 replicon-units Tier1, zero
failures.** Reproduced exactly by a cold re-run (§5).

- **Median pooled r/m = 6.30** (IQR 2.52–9.39, range 0.36–18.03), after excluding
  the external reference's branches. **Use `RM_RESULTS_L1_CORRECTED.tsv` column
  `rm_corrected`.** The uncorrected median is 1.85 and is a mixture artefact.
- **35 of the manual analysis's 37 units are recovered set-identically** — the
  strongest external check on the partition.
- **Geography: 42 of 82 units contain exactly one country, against 2.0 expected
  by chance (p = 0.0001)**, and only 2 of those 42 are single-BioProject, so it
  is not a sampling artefact. Among the 40 mixed units, 21 cluster significantly
  by country vs 18 by BioProject with 15 overlapping — there the two cannot be
  separated.
- **Global ML tree**: 82 tips, 79 internal nodes, **64 (81%) at UFBoot ≥ 95 and
  SH-aLRT ≥ 80**.

**Methods are written up in `METHODS_DRAFT_2026-08-11.md` §2.12**, which
describes the analysis as actually run and supersedes §2.1–2.11 where they
differ. Plain-language account in `RESULTS_NARRATIVE.md`.

---

## §3 THE TWO DEFECTS, BOTH FIXED

### 3.1 RAxML segfaults at a 128-character run id

Gubbins builds that id from the reference's FASTA defline. Long deflines →
segfault → Gubbins' bare `except` reports `Unable to fit model to data`. Settled
by holding the alignment byte-identical and varying only the filename (136 fails,
65 succeeds), then re-running all six historically-failing units against the
reference that had "broken" each: **12/12 succeeded**.

**Fix:** deflines normalised to `<accession>_<index>` before every run
(`normalize_reference_headers_bp.py`); `SPLIT_REFERENCE_REPLICONS` refuses
over-long unit ids. **24% of this run's units would have died without it.**
`reference_blocklist.txt` is now empty — the mechanism is kept, the entries were
wrong.

### 3.2 The external reference's branch inflated the clonal frame

The reference is kept as a taxon (deliberately — it keeps the alignment
full-length). Its branch is enormous because it sits outside the population, and
Gubbins scores those substitutions as *outside recombination*, so they land in
r/m's denominator. **52% of all outside-recombination SNPs came from reference
branches.**

**Fix:** `exclude_reference_branches_bp.py` drops the `Reference` leaf **and its
sibling at the root** (Gubbins' arbitrary rooting splits outgroup divergence
across both). Median r/m 1.85 → 6.30. Validated against the manual analysis: the
apparent distance dependence collapses from −0.589 to −0.137 and agreement
tightens to IQR 1.26–1.64.

**Still to do:** the workflow should exclude these branches when it pools, rather
than the correction living in a downstream script.

---

## §4 DELIVERABLES

On the drive at `/media/phemarajata/TB1/snp_results_2026-08-16/`:

| path | contents |
|---|---|
| `tables/` | assignments (99.9% metadata), r/m corrected, clusters, units, stragglers, references, alternates, medoids, phylogeography |
| `trees/per_unit/` | **328** — 164 ML with SH-aLRT/UFBoot + 164 Gubbins |
| `trees/global/` | ML tree with support, Mash NJ backbone, model report |
| `recombination/` | 164 GFFs + 164 per-branch statistics |
| `analysis/` | narrative, methods, comparison, both investigation write-ups, handoffs |
| `provenance/` | execution traces, versions, pipeline commit |

Excluded on purpose: alignments (~7 GB), work dirs, per-task logs. Regenerate
with `export_deliverables_bp.sh` after any change.

---

## §5 REPRODUCIBILITY, AND WHAT THE TIMING DOES NOT SAY

Two runs — one incremental across restarts, one **cold from an empty cache**:

| | result |
|---|---|
| per-unit r/m | **82/82 identical to 4 dp** |
| SNPs inside / outside | **1,547,423 / 422,894 — identical** |
| Gubbins trees | **164/164 byte-identical** |
| recombination GFFs | identical content; **line ordering only** differs |

Wall clock 10.5 h and 11.0 h. **Do not read the difference as a regression.** The
cold run also did 2,070 uncached input tasks and added 164 bootstrap analyses.
Its "sum of task realtimes" (140 h vs 90.6 h) is **contention, not work** —
identical mappings producing identical output took longer each because Gubbins
now runs alongside them.

That overlap is `groupKey` (`04e8308`) working as intended, and on a 20-core box
it is a wash. **It pays only where cores are spare** — i.e. the A100.

---

## §6 NEXT STEPS

1. **Interpretation** — the agreed next phase, and the reason to start a fresh
   session. See §7.
2. **Merge `reference-blocklist` into `main` and push.** Five commits, none
   pushed. The branch name is now misleading: the blocklist ended up empty and
   the real content is the RAxML gate, the A100 retune and the global tree.
3. **Move the reference-branch exclusion into the workflow** (§3.2), so r/m comes
   out of the pipeline already correct.
4. **Gate `IQTREE_FAST` on `--gubbins_skip_starting_tree`** — its output is
   discarded when that flag is set, yet it still runs (164 tasks, max 2.5 GB).
5. **Verify the global-tree tip-label fix on the next full run.** It was verified
   in isolation, not end to end (§8).

---

## §7 THE APPLIED GOAL, AND WHERE THE ANALYSIS SHOULD GO

**The purpose of the clustering work is rapid origin-of-exposure attribution**
for U.S./Americas cases with no travel history — where the genome is the only
evidence of where the organism came from.

The structure needed is present:

- **2 of 82 units are entirely Americas**, both inside `strain_9`:
  `strain_9_L1_4` (n=13: USA 6, Puerto Rico 5, Trinidad 1, Virgin Islands 1) and
  `strain_9_L1_5` (n=7: USA 5, Guadeloupe 1, Martinique 1). **20 of the 30
  Americas genomes sit in these two.**
- The other 10 are lone genomes inside Asian-dominated units — the pattern
  importation produces.
- **`strain_20_L1_1` is USA 6 / Viet Nam 5** — genuinely mixed, and the single
  most interesting unit given the documented decades-long latency in Vietnam
  veterans ("Vietnamese time bomb").

**Published work already validates the approach and the lineage.** Gee et al.
2017 (EID, [10.3201/eid2307.161978](https://doi.org/10.3201/eid2307.161978)) show
Western Hemisphere isolates form a distinct clade seeded from Africa with
region-associated subclades — **and reassigned a case presumed to be 62-year
latent SE Asian exposure to a Central/South American origin.** Hall et al. 2019
(PLoS NTD, [10.1371/journal.pntd.0007727](https://doi.org/10.1371/journal.pntd.0007727))
show Puerto Rico isolates form a monophyletic Caribbean clade nested in a
Central/South American clade. Latency case reports: Beck et al. 1984
([10.1212/wnl.34.1.105](https://doi.org/10.1212/wnl.34.1.105), 13 years),
Koponen et al. 1991 ([10.1001/archinte.151.3.605](https://doi.org/10.1001/archinte.151.3.605),
18 years). *(Retrieved from PubMed.)*

**Two concrete checks, both cheap and both unanswered:**

1. **Does `strain_9` sit apart in `L1_GLOBAL_ML_TREE.nwk`**, consistent with
   Gee's distinct Western Hemisphere clade? Independent recovery would be strong
   external validation of the partition.
2. **Within `strain_20_L1_1`, do the US and Vietnamese genomes interdigitate or
   separate?** Interdigitating → shared acquisition source. Separating → two
   populations that merely share a PopPUNK strain.

**The limit that must accompany any claim:** Americas genomes are **30 of 2,068
(1.5%)**. A match to `strain_9_L1_4`/`L1_5` is informative; a **non-match is weak
evidence of importation**, because an unsampled endemic American lineage would
also fail to match. That is fixed by more Americas genomes, not more analysis.

**Other open interpretation questions:** how our median r/m of 6.30 compares with
published *B. pseudomallei* estimates; and what distinguishes the r/m = 0.36 units
from the r/m = 18.03 ones — a 50-fold spread that is currently unexplained.

---

## §8 TRAPS — sessions 3 and 4 still apply, plus these

**`-resume` resumes the LAST session, and `-preview` counts as one.** Two
compile-check preview runs became "the last session", so the next resume
re-executed an 11-hour run instead of reusing it. **Cost me twice this session.**
Use `RESUME_SESSION=<id>` (added to `run_wf_curated_L1.sh`); find ids with
`awk -F'\t' '{print $1, $3, $6}' ~/wf-assembly-snps-mod/.nextflow/history`.
**Check what a resume will actually reuse before launching it.**

**Regenerating byte-identical inputs invalidates the cache.** Nextflow's default
hashing includes **mtime**. The runner used to rewrite its samplesheet and
normalized references on every launch, so a no-op resume invalidated everything.
Fixed with `write_if_changed_bp.py`; the runner now reports
`inputs rewritten: none (cache preserved)`. **Never use `cache = 'lenient'`.**

**A queue channel read twice SPLITS its emissions.** Reading `ch_for_alignment`
again for the medoid stage silently stole emissions from the alignment path.
Fork with `multiMap` before any consumer — the workflow already did this
everywhere else and says so in a comment.

**`find -name per_branch_statistics.csv` matches nothing.** The file is
`<unit>.per_branch_statistics.csv`. That failure looks exactly like "Gubbins never
produced it", which is a far scarier conclusion than the truth.

**Changing workflow topology re-runs downstream stages.** Not a bug — Nextflow is
conservative about provenance. Costs nothing on a fresh run; costs hours against
an existing cache.

**parsnp's own tree step can hang** long after the alignment is done. Use
`--skip-phylogeny` and take `parsnp.snps.mblocks` directly (the module does).

**IQ-TREE refuses `+ASC` if any column is invariant** and writes a
`.varsites.phy`; retry on that (the module does).

---

## §9 FILES ADDED THIS SESSION

**Analysis** — `build_L1_partition_bp.py`, `merge_L1_refs_bp.py`,
`rank_reference_alternates_bp.py`, `normalize_reference_headers_bp.py`,
`consolidate_L1_rm_bp.py`, **`exclude_reference_branches_bp.py`**,
`build_L1_assignments_bp.py`, `phylogeography_association_bp.py`,
`build_global_backbone_bp.py`, `build_global_ml_tree_bp.sh`,
`write_if_changed_bp.py`

**Operations** — `run_wf_curated_L1.sh` (idempotent, `RESUME_SESSION`),
`retry_failed_references.sh`, `monitor_L1.sh`, `archive_L1_stats.sh`,
`move_superseded.sh`, `export_deliverables_bp.sh`, `add_branch_support_bp.sh`,
`run_clean_timed.sh`

**Documents** — `RESULTS_NARRATIVE.md`, `CLEAN_RUN_COMPARISON.md`,
`L1_RESULTS_AND_THE_REFERENCE_DISTANCE_PROBLEM.md`,
`REFERENCE_FAILURE_SOLVED.md`, `METHODS_DRAFT_2026-08-11.md` §2.12

**Regeneration order** if inputs change:
```
build_L1_partition_bp.py -> pick_cluster_references_bp.py
  -> rank_reference_alternates_bp.py (no --refs)
  -> merge_L1_refs_bp.py -> rank_reference_alternates_bp.py (--refs)
  -> run_wf_curated_L1.sh -> archive_L1_stats.sh
  -> exclude_reference_branches_bp.py -> build_L1_assignments_bp.py
  -> phylogeography_association_bp.py -> export_deliverables_bp.sh
```
