# Session handoff — 2026-08-15 (session 3)

Continues `HANDOFF_2026-08-12_SESSION2.md`. That file's §9 is still the record
for the fidelity work; **this file covers the PopPUNK front end, the
whole-collection attempts, and the reference finding.** Read §0 and §1 first.

---

## §0 READ THIS FIRST — the habit still holds, and it caught me out repeatedly

Session 2's rule was *change one variable and measure*. Session 3 confirms it in
the negative: **every wrong call this session came from asserting a mechanism I
had not tested.** Four times:

| I claimed | what measurement showed |
|---|---|
| "strain_1's Gubbins OOMed" | it was IQTREE_FAST; I had stripped the process name with `sed` before reading it |
| "small n + distant reference explains the Gubbins failures" | refuted: strain_14 (n=31, *internal* ref at 0.0003) failed; strain_20 succeeded at 0.0047 |
| "clonality explains it" | refuted: strain_28 at mash 0.000081 — the most clonal unit — SUCCEEDED |
| "cache 'lenient' will protect the resume" | it invalidated the ENTIRE cache; 0 tasks cached |

The one claim that survived is the one I ran a controlled experiment for (§4).
**Prefer the cheap decisive experiment over the plausible explanation.**

---

## §1 STATE

- **Nothing running.** 101 GB free — *tight*, see §7.
- Pipeline repo `~/wf-assembly-snps-mod`: `main` at **`a28a96c`**, clean, pushed.
  Branch `curated-partition-references` merged and deleted.
- Five commits added this session:

| commit | what |
|---|---|
| `aa9357f` | `--gubbins_skip_starting_tree` (closes the fidelity loop, session 2 §9) |
| `f4cccbc` | no phantom Tier4 row for replicon-split clusters |
| `51b7c4f` | **PopPUNK clustering front end + complete-reference selection** |
| `a28a96c` | `--min_replicon_length` (drops sub-threshold pseudo-replicons) |

---

## §2 WHAT WAS BUILT

**`--clustering_method poppunk`** — `POPPUNK_CLUSTER` runs create-db → bgmm →
refine (Seng et al. 2024 params, PMID 38972886), pinned to PopPUNK **2.7.6**, and
emits the same `cluster_id<TAB>sample_id` contract curated mode already accepts,
so everything downstream is the already-validated path.

**`--pick_complete_references`** — `PICK_CLUSTER_REFERENCES` chooses the *mapping*
reference separately from the backbone medoid: completeness is a **gate**,
centrality (mean then max Mash to members) is the **ranking**, and a cluster with
no complete member **borrows** the nearest complete genome. Validated against the
manual analysis's own decisions: **36/36** agreement on internal-vs-borrowed,
**29/36** identical reference given the same 14-reference shortlist.

**`--min_replicon_length`** (default 100 kb) — `strain_12`'s reference has 4
contigs: 3.95 Mb, 3.09 Mb, **2,595 bp, 2,533 bp**. `max_replicons` is a COUNT
check and let it through; each pseudo-replicon then became its own analysis unit
with 37 snippy jobs. Only reference in the set affected; nothing legitimate is
dropped.

---

## §3 RESULTS THAT EXIST ON DISK

| output | contents | status |
|---|---|---|
| `pp2802_out/Summaries/` | **the PopPUNK partition** — `clusters.tsv` (35 strains, 2,395 genomes), `cluster_references.tsv`, `reference_selection.tsv` | **load-bearing, keep** |
| `all35_out/Clusters/` | 56 Gubbins results, un-subdivided partition | superseded if §5 is adopted, keep as comparison |
| `reftest_out/Clusters/` | **12 recovered units** (the 6 previously-failing strains) | keep |
| `pp2802_out/Clusters/` | 7 Gubbins results from the PopPUNK-mode run | keep |

**PopPUNK partition, in-workflow:** 264 clusters over all 2,802 genomes,
**35 kept at n ≥ 7 covering 2,395 genomes**, 152 singletons. Compared with the
archived `poppunk_bp/` fit: 30/35 strains set-identical, 4 differing slightly.
**The fit is stochastic** (264 vs 271 clusters on identical input) and **strain
numbering is NOT stable across runs** — `strain_12` here is archived strain 13.
*Join by membership, never by strain id.*

**r/m from the un-subdivided run:** 53 replicon-units, range **0.159–12.15**,
median 1.48. Two replicons of the same strain usually agree tightly (strain_2:
10.3090 vs 10.3064) — but see §5 before quoting any of it.

---

## §4 THE REFERENCE FINDING — the substantive result of this session

Six clusters failed Gubbins with RAxML *"Unable to fit model to data"*. The
failures are explained by **which reference was used**, and by nothing else:
three references account for all six (`GCF_003798365_1` alone for four, 0/4),
while 23 other references gave 28/28 successes.

**Controlled experiment: all six re-run with only the reference changed →
12/12 replicon-units succeeded, zero failures.** Three succeeded against a
reference *more distant* than the one they failed on (strain_14 at 20×).

Ruled out with data: species ID (fastANI 99.35–99.50% vs K96243), assembly
contiguity, misassemblies, duplication ratio, ambiguous bases, GC, genome
fraction, collection typicality, cluster clonality, cluster size, variable-site
count, alignment missingness, invariant-site composition.

**Consequence: the analysable set is 34/34 strains, not 28/34.** The failures
were a tooling artefact of reference choice, not unanalysable populations.

**Full detail and the plan for chasing the mechanism:
`HANDOFF_REFERENCE_FAILURE_INVESTIGATION.md`** — written to be portable to
another machine.

---

## §5 THE OPEN DECISION — partition granularity (blocking)

User's framing: *"I want this to be reviewer-proof."*

The three largest PopPUNK strains each swallow many of the previous analysis's
units:

| strain | n | prior analysed units it absorbs |
|---|---|---|
| strain_1 | 917 | **12** |
| strain_2 | 416 | **9** |
| strain_3 | 261 | **5** |

`strain_2`'s r/m came out at **10.31** — far above anything in the manual
analysis (max 6.28) — with both replicons agreeing to 4 s.f. That concordance
shows the estimate is *precise*, not that it is *valid*: high r/m is exactly the
signature of inferring recombination across nine lumped populations.

**Agreed direction (2026-08-15): subdivide uniformly, do not special-case
strain_1.** Subdividing only the inconvenient one is a post-hoc size-based cut
and is precisely what a reviewer would attack. The project already has the rule
and it is encoded in the unit names — **PopPUNK for strains, fastbaps within
strains, analyse at L1** (`s1_L1_19` = strain 1, fastbaps L1 subcluster 19).
That is PopPIPE's design and what the manual analysis did.

**Consequence:** results for strain_1–5 are superseded under the new rule; the
~25 small strains mapping to 0–1 prior units are unaffected.

**Not yet built:** the fastbaps subdivision step. `_fastbaps.tsv` holds L3
labels for 1,590 genomes (strains 1+2+3 = 913+416+261, which is exactly why
those three were subdivided before).

---

## §6 IMMEDIATE NEXT STEPS

1. **Build the fastbaps subdivision** for oversized strains and regenerate
   `cluster_assignments` at L1 granularity. Then one run at final granularity.
2. **Add the reference fallback** — on Gubbins "Unable to fit model to data",
   retry with the next-nearest complete reference. §4 makes this defensible
   without needing the mechanism. Blocklist the three known-bad references
   meanwhile.
3. **Re-run** with 1+2 in place. Use **curated mode** (§7).
4. Optional: `strain_1` at full resources — but see §5; under uniform
   subdivision it stops being a single unit, which is both faster and more
   defensible than throwing 20 cores at a 917-taxon Gubbins.

---

## §7 TRAPS — all measured this session, all expensive

**Use curated mode for anything long.** In PopPUNK mode, `MASH_SKETCH_BATCH`
misses cache on *every* restart (batches come from `.collate()` over an unordered
channel); default cache hashing includes file **timestamps**, so `MASH_TRIANGLE`
rewrites a byte-identical matrix with a new mtime and everything downstream
rehashes. **Measured three times: the snippy stage was invalidated on every
restart — ~6.5 h, then ~27 h, then ~27 h.** With no Mash/PopPUNK upstream there
is nothing to rehash: the curated resume preserved **3,668 of 3,685 snippy tasks**.

**`errorStrategy` closures need an attempt guard.** This is wrong:
```groovy
{ task.exitStatus in [71,104,134,137,139,140,143,255] ? 'retry' : 'ignore' }
```
137 (OOM) is in the list, so it always returns `'retry'`; when `maxRetries` is
exhausted the strategy still says retry, none remain, and **the pipeline
terminates**. `'ignore'` is unreachable for exactly the codes that exhaust
retries. This killed a 28-hour run. Correct form:
```groovy
{ (task.exitStatus in [...] && task.attempt <= 2) ? 'retry' : 'ignore' }
```

**Never change `cache` mode mid-project.** `cache = 'lenient'` was tried to
survive regenerated intermediates; it changes how hashes are computed and
invalidated **the entire cache** (0 cached, restart from task one). Resource and
`errorStrategy` directives are NOT part of the hash and can be changed freely.

**Profile ceilings are sized for n ≤ 155** and several are FIXED, not
attempt-scaled — so an OOM retries at the same memory and fails identically.
`KEEP_INVARIANT_ATCG` is pinned at 4 GB; strain_3 (n=261) passed, strain_2
(n=416) and strain_1 (n=917) OOMed. At 20 GB all pass. Gubbins itself is
compute-bound, not memory-bound: peak RSS only **3.7 GB at n=416**.

**`PICK_CLUSTER_REFERENCES` records staged paths.** `cluster_references.tsv`
contains the path the reference was staged at *inside the task dir*, which dies
with the work dir. Resolve references back to the collection by basename —
`run_wf_curated_all35.sh` does this.

**`csv.writer` defaults to CRLF.** Generated TSVs got `\r\n`; `splitCsv` then
carries a trailing `\r` into `reference_path` and `checkIfExists` fails. Always
pass `lineterminator="\n"`.

**`IQTREE_FAST` runs even when its output is discarded.** With
`--gubbins_skip_starting_tree true` Gubbins builds its own first tree, but the
process still runs — and OOMed twice on strain_1 at 917 taxa. Should be gated on
the skip flag.

**Gubbins runtime is superlinear:** n=90 ~13 min, n=261 ~62 min, n=416 ~177 min
per replicon (5 iterations). strain_1 (n=917) was still inside **iteration 1
after 10.5 h** and was stopped.

---

## §8 FILES ADDED THIS SESSION

**Runners** (all with the corrected errorStrategy and scaled resources):
- `run_wf_curated_all35.sh` — 35 strains, curated mode, `EXCLUDE_STRAINS` env var
- `run_wf_reftest.sh` — **the controlled reference experiment**, rerunnable
- `run_wf_poppunk_2802.sh` — FASTA-only PopPUNK-mode run (see §7 before reusing)
- `run_wf_bigstrains.sh` — big-strain follow-up, `BIG_STRAINS` env var

**Inputs:** `curated_all35_{clusters,refs}.tsv`, `wf_all35_samplesheet.csv`,
`reftest_{clusters,refs}.tsv`, `wf_reftest_samplesheet.csv`,
`wf_2802_samplesheet.csv`, `curated_analysed37_{clusters,refs}.tsv`

**Archive:** `RUN_STATS_ARCHIVE/` — `per_branch_statistics.csv` (the ONLY source
of pooled r/m; the workflow never publishes it) for the cs/fid runs and one
PopPUNK-run unit.

**Disk:** `all35_work` is **283 GB** and `reftest_work` 13 GB, against **101 GB
free**. `all35_work` is disposable *if* §5 is adopted — but extract any
`per_branch_statistics.csv` first, and note `publish_dir_mode = 'copy'` so
published outputs survive work-dir deletion (verified: link count 1).

---

## §9 ANSWERS TO TWO QUESTIONS FROM THE FOLLOW-ON CHAT (2026-08-15)

### Q1: was `inputs/fastbaps_membership_L1_all.tsv` (14 of 42 strains) a deliberate screen?

**No evidence of a quality screen. It looks structure-driven — but the file is
NOT authoritative for what is analysable.**

Measured from `~/PopPIPE-bp/output/strains` (42 strain dirs) against the
workspace file (14 strains, 133 L1 units, 2,006 genomes):

- **fastbaps ran on all 42.** Every strain dir has fastbaps output, so the 14 is
  not "the ones that could be run".
- **Not a size threshold — the sizes interleave:** s8 (n=46) excluded vs s9
  (n=45) included; s10 (40) excluded vs s11 (39) included; s28 (9) excluded vs
  s29 (9) included; s31/s33/s34 (n=7) excluded vs s32 (n=7) included.
- **Every included strain contributed >= 3 L1 units**, with a clean break — none
  has 1 or 2:
  s1:43, s3:11, s2:10, s4:9, s6:9, s9:8, s11:8, s5:7, s16:7, s7:6, s25:5,
  s29:4, s18:3, s32:3.
  If the file were simply "strains fastbaps ran on", singletons would appear.

Most consistent reading: it carried strains where fastbaps **found substructure**
and omitted those returning essentially one cluster. **This is inference, not
established** — the archived `fastbaps_clusters.txt` did not parse with the
assumed format, so it was never confirmed.

**The caveat that matters:** `s13` is NOT in the 14-strain file, yet `s13_L1_1`
(n=31) IS in `analysable_units.tsv`, and `METHODS_DRAFT` §2.7 lists it as
"L1 sub-cluster **recovered from** strain 13", contributing 1 unit / 31 genomes
to the analysed set. So at least one excluded strain yielded a usable unit that
entered by a separate route.

=> Reusing all 42 does **not** resurrect units dropped for cause. It will pick
up strains where subdivision is uninformative (they reduce to the strain
itself) — harmless, not wrong.

**To close it:** parse the 42 archived `fastbaps_clusters.txt` and count distinct
L1 labels per strain. If every excluded strain has exactly 1, the inference is
confirmed and the rule can be stated explicitly.

### Q2: was re-running fastbaps on the pp2802 partition considered and rejected?

**Neither — it was never reached.** The decision to subdivide uniformly was taken
at the very end of session 3; §5 records the fastbaps step as "Not yet built".

Relevant measurements for the provenance seam:

- The in-workflow pp2802 PopPUNK fit gives **264 clusters**; the archived fit
  gives **271** on identical input. **The fit is stochastic.**
- **30 of 35 strains are set-identical; 4 differ** — strain_1 913→917
  (Jaccard 0.996), strain_9 0.915, strain_12 0.973, strain_21 0.923.
- **Strain numbering is NOT stable across fits** — `strain_12` here is archived
  strain 13. Any label transfer must be by **membership**, never by id.

So a clean 1:1 strain mapping is real but incomplete: for those 4 strains the
transferred labels land on genomes that were not in the archived strain when
fastbaps was run. The ~15 unlabelled genomes are almost certainly exactly those
membership differences.

=> Transfer is defensible for the 30 identical strains and hard to defend for
the 4 that differ — and those include **strain_1**, the largest. Re-running
fastbaps on the pp2802 fit removes the seam entirely and is cheap relative to
the Gubbins work downstream.
