# SOLVED: the three references do not break Gubbins. Their *names* do.

**Reply to `PROMPT_FOR_LINUX_SESSION.md`. Do not build the bundle as specified —
the site-pattern diff it is designed to enable cannot find the cause, because
the cause is not in the alignments.**

---

## The mechanism

`raxmlHPC` v8 **segfaults (exit 139) when its `-n` run id is 128 characters or
longer.**

Gubbins builds that run id as `<analysis unit>.core.full.iteration_N_reconstruction`
— 37 characters more than the unit name. The unit name is
`<cluster_id>__<replicon id>`, and the replicon id is the sanitised **first token
of the reference's FASTA defline**. In this collection deflines are the entire
filename plus a contig index:

```
>Burkholderia_pseudomallei_vgh07_GCF_000954175.1_Taiwan_Kaohsiung_Veterans_General_Hospital_Kaohsiung.fasta_1
```

That is 108 characters. Long-named references therefore push the run id past 128
and RAxML dies. Short-named ones do not.

Gubbins wraps the call in a bare `except`:

```python
try:
    subprocess.check_call(model_fitting_command, shell = True)
except:
    sys.exit("Unable to fit model to data")
```
`gubbins/common.py:444` (3.4.3)

So a SIGSEGV is reported as a model-fitting failure. RAxML actually *contains* a
guard string — `Error: run id after "-n" is too long, it has %d characters
please use a shorter one` — but at 128 it crashes before printing it. Nothing
reaches any log.

## The evidence

**1. Direct measurement of the limit.** Same alignment, same tree, same model,
only `-n` length varied:

| `-n` length | exit |
|---|---|
| 100, 120, 125, 126, **127** | **0** |
| **128**, 129, 130, 135, 136 | **139 (SIGSEGV)** |

The `-w` path length is irrelevant — tested at 122 and 214 characters, same
result. It is the run id alone.

**2. Perfect separation across the real runs.** Every archived
`*.diagnostics.log` from the all35 run, run id length vs outcome:

| outcome | n | run id length |
|---|---|---|
| FAILED | 12 | **135–136** |
| ok | 56 | **109–126** |

Zero overlap. The three "bad" references are simply the ones with long names:
`GCF_003798365_1_Thailand_Ubon_Ratchathani`,
`GCF_026315045_1_Australia_Northern_Territory`,
`GCF_002843645_1_Australia_Northern_Territory`.

**3. It explains the detail that made no sense.** The diagnostics log shows
RAxML being called *twice*. The first call succeeds in 2.13 s; the second fails
instantly. They differ only in the run id — the second appends
`_reconstruction`, 15 more characters:

```
-f d ... -n <base>.iteration_1                    -> 121 chars, "...done. Run time: 2.13 s"
-f e ... -n <base>.iteration_1_reconstruction     -> 136 chars, "Unable to fit model to data"
```

A biological explanation cannot produce that. A 15-character suffix can.

## Why every hypothesis in §1 was correctly ruled out

fastANI, contiguity, N50, genome size, ambiguous bases, GC, duplication ratio,
misassemblies, collection typicality, cluster clonality, cluster size, variable
site count, alignment missingness, invariant-site composition — all measured,
none separated the two classes. **They never could.** None of them is a function
of the filename.

The same applies to the paradox in §0 of the investigation handoff: three units
succeeded against a *more distant* reference. Distance was never relevant; the
substitute references just had shorter names.

## What this means for the bundle request

| item | status |
|---|---|
| Tier A.1–2 (failed task dirs, `all35_work`) | **`all35_work` was purged.** But the complete `*.diagnostics.log` files survive in `RUN_STATS_ARCHIVE/all35/` — 68 of them, unabridged, and they contain the exact RAxML command lines. That is what solved this. |
| Tier B.7–8 (the alignment pair) | **Do not diff these.** Both alignments are fine. `REFTEST_ALIGNMENTS/{failing,succeeding}/` already holds gzipped `.core.full.aln` for all six units, both replicons, if you still want them. |
| Tier B.9 / C.12 (reference FASTAs as consumed) | Relevant now, but for the **deflines**, not the sequence. |
| "regenerating means re-running `run_wf_reftest.sh`" | **Not needed.** Do not spend the compute. |

## The fix, applied

1. **`normalize_reference_headers_bp.py`** rewrites deflines to
   `<accession>_<replicon index>` (e.g. `GCF_000954175_1_1`). Sequence content is
   verified byte-identical; only `>` lines change. Longest run id on the current
   82-unit partition drops from **161 to 70**.
2. **`SPLIT_REFERENCE_REPLICONS` now rejects** any unit id that would exceed the
   bound, naming the offender and the fix (pipeline `7515f1b`). It fails loudly
   rather than truncating — silently shortening a unit id would change analysis
   identities nobody asked to change.

**This was not academic.** The L1 run had already started when this was found:
**40 of 164 replicon-units (24%) would have segfaulted**, including
`strain_1_L1_9` (n=90), one of the manual analysis's own validated units. The
run was stopped, the deflines normalized, and it was relaunched.

## The blocklist is retired — tested, not assumed

The three references were re-tested rather than argued about, by the tightest
experiment available: **hold the alignment bytes identical and vary only the
filename.**

```
strain_23 / GCF_003798365_1, md5 64b8b34a..., run id 136  -> exit 1, "Unable to fit model to data"
strain_23 / GCF_003798365_1, md5 64b8b34a..., run id  65  -> exit 0, SUCCESS
```

Then repeated across all six previously-failing units, both replicons, each
against **the reference that had "broken" it**:

**12 / 12 succeeded.** `reference_blocklist.txt` is now empty.

This is stronger than session 3's original experiment, which changed the
reference and so could not distinguish "the reference was bad" from "the name
was long". Holding the alignment constant removes that ambiguity entirely.

## Consequences worth carrying

- **"6 of 34 units are unanalysable" was never true.** Nor was the softer
  version, "these populations need a functional reference test."
- **The six reftest r/m values were produced against substitute references** —
  references the selection rule would not have chosen, forced by a filename bug.
  They are flagged `superseded` in `RM_RESULTS_CONSOLIDATED.tsv`.
- **Their provenance columns were also wrong.** All 12 rows recorded the
  metadata of the reference that *failed* rather than the one that produced the
  r/m — `strain_14` was labelled `internal / 0.000301` when the run actually used
  a borrowed reference at **0.00589**, a 20× error, and `strain_34` `internal /
  0.000407` against an actual **0.00357**. Corrected in place; the original is
  kept as `RM_RESULTS_CONSOLIDATED_uncorrected.tsv.bak`. Anyone who had read r/m
  against reference distance off that table was reading a corrupted relationship.
- Any pipeline naming an artefact after a defline can hit this. The bound is
  RAxML's, but the exposure is ours.
