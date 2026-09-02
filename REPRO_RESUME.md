# Paused 2026-08-24 15:47 — how to resume

The reproducibility run was **stopped cleanly** (SIGTERM, not a crash) so the
machine could be powered off. It is resumable. Nothing needs to be redone.

---

## Resume with this, exactly

```bash
cd /home/phemarajata/wf-assembly-snps-mod-79ab645 && setsid nohup bash /home/phemarajata/Downloads/snp-mod-local-working/resume_reproducibility.sh > /dev/null 2>&1 < /dev/null &
```

That wrapper re-issues the original command line verbatim with `-resume` added,
and restarts the disk watchdog. If you would rather run it by hand, the only
thing that matters is that you are **in the launch directory** and that
`-work-dir` is unchanged.

## Where it got to

| | |
|---|---|
| ran for | 5 h 46 m (10:01 → 15:47) |
| `SNIPPY_SCATTER` | **2,656 / 4,704** (56%) |
| `GUBBINS_CLUSTER` | **64 / 172** (37%) |
| `IQTREE_ASC` | 56 / 172 |
| completed task dirs cached | **5,484** |
| work dir | 140 GB |
| root free at pause | 308 GB |

**13 in-flight tasks were killed** by the stop and will simply re-run. Everything
with a recorded exit code is cached and will be skipped.

Roughly **4–5 hours** of work remains at the observed rate.

## What must survive the reboot — do not delete either of these

Resume needs **two** things, and they are in different places. This is the usual
way a resume gets lost:

1. **The work dir** — `REPRO_2026-08-24_work` (140 GB) in the working directory.
2. **The resume cache** — `.nextflow/cache/c93bd595-8aaa-4cf1-8152-728d8c408e9e/`
   (19 MB) plus `.nextflow/history`, both inside the **launch directory**
   `/home/phemarajata/wf-assembly-snps-mod-79ab645`. That is the detached git
   worktree. **Do not remove the worktree** (`git worktree remove …`) before the
   run finishes — it would delete the cache and force a full restart even though
   the 140 GB work dir is still there.

Also unchanged: `-resume` matches on the command line and inputs, so the
samplesheet, cluster and reference files must stay where they are.

## Session identity, if you ever need it explicitly

| | |
|---|---|
| run name | `soggy_gilbert` |
| session UUID | `c93bd595-8aaa-4cf1-8152-728d8c408e9e` |
| scriptId | `e09a5c4ead` |
| history status | `ERR` — **expected**, that is what a SIGTERM'd run records |

A bare `-resume` picks the last run in this launch directory, which is
unambiguous here. To be explicit: `-resume c93bd595-8aaa-4cf1-8152-728d8c408e9e`.

## Two things not to misread on restart

- **`ERR` in the history and `rc=1` in the log are the pause, not a failure.**
  Nextflow logs "Pipeline completed with errors" and "Killing running tasks (13)"
  when it is asked to stop. The analysis did not fail.
- **The per-process counts in `REPRO_2026-08-24.log` will restart from zero** in
  the *new* log, because resumed tasks are reported as cached rather than
  submitted. Judge completion from the final summary, or from
  `find REPRO_2026-08-24_work -maxdepth 3 -name .exitcode | wc -l`, not by
  grepping "Submitted" in the second log.

Everything else — the traps, the expected task totals, and the diff plan — is
unchanged in `REPRO_RUN_2026-08-24.md`.
