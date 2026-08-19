# Single-shot clean run vs the incremental run

Clean run: **2026-08-15 23:55:38 → 2026-08-16 10:57:05, 11 h 01 m**, fresh work
directory, cache cleared, every fix in place. 82 units, 2,070 genomes,
**164/164 Tier1_high_confidence, zero failures.**

---

## 1. Are the results different? No — they are identical.

| comparison | result |
|---|---|
| per-unit corrected r/m | **82 / 82 identical to 4 dp** |
| total SNPs in recombination | 1,547,423 vs 1,547,423 — **identical** |
| total SNPs outside recombination | 422,894 vs 422,894 — **identical** |
| Gubbins trees | **164 / 164 byte-identical** |
| recombination predictions (GFF) | identical content; see below |

The GFFs differ byte-wise in 137 of 164 files, but that is **line ordering
only** — sorting both sides gives zero differing lines, same 180 entries per
file. Gubbins emits the records in a nondeterministic order. Nothing about the
calls changes.

**So the pipeline is deterministic in substance.** Two independent runs, one
built up incrementally through several restarts and one cold from scratch,
produce the same trees, the same recombination calls, and the same r/m.

---

## 2. How long, and why the naive comparison misleads

| | baseline (incremental) | clean (single shot) |
|---|---|---|
| wall clock | 10.51 h | **11.02 h** |
| sum of task realtimes | 90.6 h | **140.0 h** |
| tasks served from cache | 2,070 | **0** |
| branch support computed | no | **yes (UFBoot + SH-aLRT, 164 trees)** |

Taken at face value the clean run looks 5% slower and 54% more expensive. Both
impressions are wrong, for different reasons.

**The 140 h is not more work — it is contention.** "Sum of task realtimes"
measures elapsed time per task, and elapsed time inflates when tasks compete.
SNIPPY_SCATTER shows 127.6 h against the baseline's 81.4 h for *the same 4,140
mappings on the same inputs producing byte-identical output*. The tasks did not
do more; they each waited longer because Gubbins was running alongside them.

**That contention is the `groupKey` fix working as designed.** In the baseline,
`SNIPPY_CORE_GATHER` could not fire until the entire mapping stage drained, so
Gubbins ran afterwards in a separate ~2 h block. In the clean run units gathered
as soon as their own mappings finished — Gubbins reached 40/164 before mapping
was half done, and 89% before mapping finished. The work was interleaved rather
than queued.

**On this machine that is a wash, and it was always going to be.** A 20-core box
is saturated either way; rescheduling *when* work happens cannot reduce *how
much* there is. The 0.5 h difference is the cold start (2,070 input tasks the
baseline had cached) plus the added bootstrap (IQTREE_ASC 0.4 h → 1.0 h).

**Corrected like-for-like: the two runs are the same speed**, and the clean run
delivers branch support the baseline did not have.

---

## 3. Where the fixes actually pay

The overlap fix pays only where cores are spare. On the retuned A100 profile:

- `SNIPPY_SCATTER` at 96 forks instead of 12 — it is 89% of the workload and
  measures 108% cpu, so it is one core per task and only concurrency helps.
  ~4,140 × 70 s ÷ 96 ≈ **50 min** against ~7 h here.
- Gubbins at 24 forks × 4 cores overlaps that mapping window instead of
  following it, which is exactly the idle-tail capacity `groupKey` unlocks.

Projected A100 wall clock: **1.5–2 h**, against 11 h on the workstation. That
projection is arithmetic from measured per-task costs, not a measurement — it
should be checked on the first real A100 run.

---

## 4. What the clean run also confirms

- **The RAxML run-id fix holds.** Zero "Unable to fit model to data" across
  164 units. Before header normalization, 40 of those 164 (24%) would have
  segfaulted.
- **The empty blocklist is safe.** All three formerly blacklisted references
  were in use; none failed.
- **The runner is now idempotent.** `inputs rewritten: none (cache preserved)` on
  a repeat invocation — the defect that invalidated a resume mid-session and
  nearly cost 7 h of re-mapping.
- **Resource ceilings hold at this scale.** No OOM, no retry, including
  `KEEP_INVARIANT_ATCG`, whose real peak (3.60 GB) is triple what its profile
  comment claimed.
