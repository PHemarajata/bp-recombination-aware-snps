# Session handoff — 2026-08-15 (session 4)

Continues `HANDOFF_2026-08-15_SESSION3.md`. That file's §4 and
`HANDOFF_REFERENCE_FAILURE_INVESTIGATION.md` remain the record for the reference
finding. **This file covers the L1 partition, the reference selection at L1, and
the blocklist feature.** Read §0 and §1 first.

---

## §0a THE HEADLINE — the reference failure is solved, and it is not biological

**`raxmlHPC` v8 segfaults (exit 139) when its `-n` run id is ≥ 128 characters.**
Gubbins builds that run id from the analysis unit name, which is built from the
reference's **FASTA defline**. Long-named references overflow it; short-named
ones do not. Gubbins' bare `except` reports the SIGSEGV as
`Unable to fit model to data`.

Perfect separation in the archived logs: **12 failures at run id 135–136, 56
successes at 109–126**, zero overlap. Direct measurement with everything else
held identical: 127 exits 0, 128 exits 139.

This retires "three reference genomes break Gubbins", the functional-reference-
test idea, and the claim that 6 of 34 units were unanalysable. It also explains
why every genome quality metric was correctly ruled out — **none of them is a
function of a filename** — and why units succeeded against a *more distant*
reference: the substitute simply had a shorter name.

**Full write-up: `REFERENCE_FAILURE_SOLVED.md`** (also copied to the shared
notes folder, as the reply to `PROMPT_FOR_LINUX_SESSION.md` — do not build that
bundle, and do not re-run `run_wf_reftest.sh`).

**It was not academic.** The L1 run had already started when this surfaced:
**40 of 164 replicon-units (24%) would have segfaulted**, including
`strain_1_L1_9` (n=90). The run was stopped, deflines normalized
(`normalize_reference_headers_bp.py`, longest run id **161 → 70**, sequence
content verified byte-identical), and relaunched. `SPLIT_REFERENCE_REPLICONS`
now rejects over-long unit ids loudly (pipeline `7515f1b`).

**Open item:** `reference_blocklist.txt` is now a workaround for a bug that is
fixed. Its three entries should be re-tested with normalized deflines and the
list probably emptied. Measured cost of leaving it on: **3 units of 82 would get
a closer reference, by 1.03–1.05×** — negligible, which is why the current run
was left alone rather than restarted again.

---

## §0 READ THIS FIRST — two claims from session 3 did not survive measurement

Session 3's rule was *prefer the cheap decisive experiment over the plausible
explanation*. It held again, twice, in the negative:

| the claim | what measurement showed |
|---|---|
| the 14-strain fastbaps file held "strains where fastbaps found substructure (≥3 L1 units)" | **refuted.** 34 of 42 archived strains have ≥3 L1 units; only 14 are in the file. ≥3 is necessary, not sufficient, and no structural rule reproduces the 14 |
| nearest-neighbour is enough to place the genomes fastbaps never labelled | **refuted.** It placed `GCF_001976585_1_Thailand` into a subcluster whose own members span 0.00089, at a distance of 0.00262 — 3× the diameter. Two more like it. A containment test now refuses them |

Both were caught by checking rather than reasoning, and both had already been
written down as settled. **A claim that arrives labelled "confirmed" still needs
the one-line check.**

---

## §1 STATE

- **Nothing running.** 395 GB free — `all35_work` (283 GB) and `reftest_work`
  were purged; published outputs survived (`publish_dir_mode = 'copy'`).
- Pipeline repo `~/wf-assembly-snps-mod`: branch **`reference-blocklist`** at
  `0a58a86`, one commit ahead of `main` (`a28a96c`). **Not merged, not pushed.**
- **The L1 run is built and validated but NOT LAUNCHED.** Every input exists and
  passes `DRY_RUN=1`. Launching is §6 step 1.

---

## §2 WHAT WAS BUILT — the L1 partition

Session 3 §5 agreed the direction (*subdivide uniformly, PopPUNK for strains,
fastbaps within strains, analyse at L1*) but left the step unbuilt. It is built.

**The rule, stated for Methods:** PopPUNK defines strains; fastbaps (PopPIPE,
levels = 3) subdivides within each strain; analysis units are fastbaps **level 1**
subclusters kept at n ≥ 7. A strain fastbaps does not split yields one L1 unit.
No strain is subdivided because it is large and none is left whole because it is
small.

**Result: 82 units, 2,070 genomes.**

| | units | genomes | % of 2,802 | largest |
|---|---|---|---|---|
| manual analysis | 37 | 1,051 | 37.5% | 155 |
| all35 run (session 3) | 35 | 2,395 | 85.5% | **917** |
| **this partition** | **82** | **2,070** | **73.9%** | **155** |

Session 3 feared subdividing would be expensive. It is the opposite. Gubbins
scales superlinearly — measured n=90 ~13 min, n=261 ~62 min, n=416 ~177 min per
replicon; n=917 was still inside iteration 1 after 10.5 h. Fitting those points
gives t ≈ 0.006·n^1.71 min, so **the whole Gubbins stage is ~6 h serial, ~2 h at
maxForks 3.** Mapping dominates now (~2,070 snippy jobs), not Gubbins.

### Where the labels come from, and why not a fresh fastbaps run

Labels are transferred from the archived PopPIPE-bp run (2026-08-10, an earlier
PopPUNK fit) onto the pp2802 fit. Three measurements justify it:

1. **Every one of the 35 pp2802 strains maps onto exactly one archived strain** —
   no splits, no merges. Numbering shifts (`strain_12` is archived 13, `strain_21`
   is archived 23), which is why the build joins by membership and refuses to run
   if any strain spans two archived strains.
2. **35 of the manual analysis's 37 units come out set-identical.** The two
   exceptions are understood: `s1_L1_27_L2_69` (the manual analysis alone went to
   L2 there, 45 of 150) and `s9_L1_4` (13 vs 12, one straggler).
3. **The seam is exactly 15 genomes** — collection additions postdating the
   fastbaps run, itemised in `curated_L1_stragglers.tsv`.

Re-running fastbaps was the intuitive "cleaner provenance" choice and was
**rejected on evidence**: it renumbers every L1 subcluster, destroying the
unit-by-unit comparison with the manual analysis in (2) — the best external
check available — and it is stochastic, so it would perturb the partition
everywhere to fix a seam measuring 15 genomes. It also needs the pp2802 PopPUNK
h5, which died with the work dir.

### The 15 stragglers

Placed by nearest labelled neighbour **subject to a containment test**: a
straggler joins only if it is no further from its nearest labelled relative than
that subcluster's labelled members are from each other. Without the test, three
genomes were being hung as long branches off clonal units — the exact
configuration that inflates r/m.

- **12 placed**, all geography-consistent (Virgin Islands → Puerto Rico, Mexico → Mexico)
- **3 refused** and excluded: `GCF_001976585_1_Thailand`, `GCA_963563995_1`, `IE-0046`
- `strain_31` (7 Sri Lanka Batticaloa genomes) is absent from the archived fit
  entirely and becomes one whole L1 unit

---

## §3 THE 14-STRAIN FILE — settled, and it is not a quality screen

Session 3 reused `inputs/fastbaps_membership_L1_all.tsv` (14 of 42 archived
strains). The open worry was whether the other 28 had been dropped for cause.
They were not:

- fastbaps ran successfully on **all 42**; every `fastbaps_clusters.txt` parses.
- Not size: strain 8 (n=46) out, strain 9 (n=45) in.
- Not substructure — see §0.
- **What it actually is:** `analysable_units.tsv` holds 37 units, **36 of them
  from those same 14 strains**. The file is the manual analysis's *scope*. The
  lone exception, `s13_L1_1`, was recovered separately, so absence never meant
  "judged unanalysable".

**Consequence, and it must be quoted rather than glossed:** using all 42 raises
unscreened content. **258 of the 2,070 analysed genomes (12.5%) come from strains
outside the 14 and have never been modality-screened.** That is a widening of the
known gap, not a new flaw, but it is the number a reviewer will ask for.

---

## §4 REFERENCES AT L1

Selection is unchanged in principle — completeness is a gate, centrality (mean
then max Mash to members) is the ranking — but three things are new.

**All 82 units have a reference within Mash 0.005** (SKA2's strain boundary),
median 0.00236. 23 internal, 59 borrowed, 31 distinct references.

**A defect was found and fixed in the workspace picker.** Its borrow pool was
built from genomes it had already read while scoring members, so it could only
borrow from inside the analysed partition — 2,070 genomes, not the collection's
2,802. Measured cost: 17 borrowed references were further from their unit than
the best complete genome available, `strain_13_L1_3` by **5.1×** (mean Mash
0.00402 against 0.00078). Borrowed references now come from
`rank_reference_alternates_bp.py`, which ranks all 189 complete genomes by the
same criterion. **The pipeline's own `bin/pick_cluster_references.py` never had
this bug** — only the workspace analysis copy did.

**18 of the 31 references in use have never been exercised in a successful run**,
covering ~975 genomes. At the observed 3-in-26 bad-reference rate, expect roughly
**two more bad references to surface in this run.** Do not read a Gubbins
model-fit failure as a property of the population until the alternate reference
has been tried — that mistake previously wrote off 6 of 34 units.

---

## §5 THE BLOCKLIST — now a pipeline feature

`--reference_blocklist` (branch `reference-blocklist`, `0a58a86`) excludes
accession prefixes from **both** selection paths. Filtering only the internal
path would have missed four of the six known failures, which borrowed their bad
reference.

Verified on the six known-bad units: **without the list 5 of 6 select a blocked
reference; with it none do** — and the substitutes it picks are the same ones the
manual re-run validated 12/12 (`strain_21` → `GCF_000755905_1`, `strain_23` →
`GCF_000755945_1`, `strain_34` → `GCF_000755905_1`). That is an independent
reproduction of the session-3 experiment from a different code path.

The list is **staged as a file** so its contents join the task hash: adding a
newly identified bad reference invalidates the cached selection instead of
silently reusing a pick made without it.

`retry_failed_references.sh` closes the loop: it scans diagnostics logs for the
`Unable to fit model to data` signature **only**, promotes each affected unit to
its next-ranked alternate, and re-drives just those units into their own outdir.
It deliberately does **not** promote OOM, timeout, or too-few-sequence failures —
swapping the reference there would hide a real problem. Two promotions maximum;
a unit still failing after that is a finding about the unit.

---

## §6 IMMEDIATE NEXT STEPS

1. **Launch the run.** `./run_wf_curated_L1.sh` — validated with `DRY_RUN=1`;
   82 units, 2,070 genomes, all paths resolve, no CRLF. Curated mode, so it
   resumes properly.
2. **When it finishes**, count Tier1 units in
   `Summaries/cluster_phylogeny_summary.csv`. `errorStrategy 'ignore'` means a
   zero exit does **not** mean every unit succeeded.
3. **Run `./retry_failed_references.sh`** for any model-fit failures, then add
   whatever it identifies to `reference_blocklist.txt`.
4. **Extract `per_branch_statistics.csv`** into `RUN_STATS_ARCHIVE/` before
   deleting `L1_work` — it is the only source of pooled r/m and the workflow
   never publishes it.
5. **Recompute every quoted figure from the completed run**, not from a partial
   one. Six appendix numbers in this project were once computed mid-run.
6. Merge `reference-blocklist` into `main` once the run has exercised it.

**Sensitivity check worth doing:** `strain_1_L1_27` stays whole at n=150 under
the uniform rule where the manual analysis cut it to L2 (`s1_L1_27_L2_69`,
n=45). Comparing their r/m is the cheapest available test of whether L1 is the
right granularity — which is the assumption the whole partition rests on.

---

## §7 TRAPS — session 3's all still hold, plus two

Session 3 §7 is unchanged and still load-bearing: curated mode for anything
long, the `task.attempt <= 2` guard on `errorStrategy`, never change `cache`
mode, fixed profile ceilings, staged reference paths, `csv.writer` CRLF,
`IQTREE_FAST` running when discarded, superlinear Gubbins runtime. New:

**Sample-name sanitisation differs between files.** `mash_matrix_2802.tsv` has
`GCF_015714675_1_Virgin_Islands_St__John` where `clusters.tsv` has
`...St._John`. A naive join silently drops the genome — here it surfaced as a
hard error only because the lookup was made mandatory. Every script added this
session normalises non-alphanumerics to `_` before joining.

**Nearest-neighbour assignment needs a containment test.** See §0. Nearest
neighbour always finds *a* nearest subcluster, however far away it is.

---

## §8 FILES ADDED THIS SESSION

**Partition and references** (all regenerate from scratch, stdlib only):
- `build_L1_partition_bp.py` → `curated_L1_{clusters,units,stragglers}.tsv`
- `rank_reference_alternates_bp.py` → `curated_L1_ref_alternates.tsv` (5 ranked
  alternates per unit; also the whole-collection borrow pool)
- `merge_L1_refs_bp.py` → `curated_L1_refs.tsv`, `curated_L1_reference_audit.tsv`
- `reference_blocklist.txt` — the three bad references, with their record
- `pick_cluster_references_bp.py` — gained `--blocklist`

**Runners:**
- `run_wf_curated_L1.sh` — the L1 run; `DRY_RUN`, `EXCLUDE_UNITS`,
  `CLUSTERS`/`REFS`/`OUTDIR`/`WORKDIR` overridable
- `retry_failed_references.sh` — the reference fallback pass

**Regeneration order**, if any input changes:
```
build_L1_partition_bp.py  ->  pick_cluster_references_bp.py
  ->  rank_reference_alternates_bp.py (no --refs)
  ->  merge_L1_refs_bp.py  ->  rank_reference_alternates_bp.py (--refs, marks IN_USE)
```
