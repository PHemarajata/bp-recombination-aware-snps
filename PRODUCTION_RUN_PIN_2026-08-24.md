# The reported run, pinned

2026-08-24. Closes open item 2 of the evening handoff: *"pin the production
command line (branch + commit)."* Everything below is read out of the run's own
artifacts, not reconstructed from memory or from prose.

---

## 1. The pin

| | |
|---|---|
| **Pipeline** | `wf-assembly-snps-mod` — https://github.com/PHemarajata/wf-assembly-snps-mod |
| **Branch** | `main` |
| **Commit** | **`79ab645`** — *perf(gubbins): skip IQTREE_FAST entirely under `--gubbins_skip_starting_tree`*, 2026-08-16 15:17:30 +0700 |
| **Nextflow** | 25.04.6, build 5954 |
| **Nextflow scriptId** | `e09a5c4ead` (hash of `main.nf`; **not** a git SHA — see §3) |
| **Run name / session** | `agitated_coulomb` / `c90e1105-5b12-455e-9b31-4ecde888d559` |
| **Started / finished** | 2026-08-18 19:52:00 → 2026-08-19 08:07 (+07) |
| **Host** | 22 CPUs, 62.3 GB RAM (the 22-core workstation — the **reported** run) |
| **Record** | `L1v4c_out/pipeline_info/`, `~/wf-assembly-snps-mod/.nextflow.log` |

## 2. The command line, verbatim

Read from `.nextflow.log` line 1 and confirmed against
`L1v4c_out/pipeline_info/execution_report_2026-08-18_19-52-00.html`:

```bash
nextflow run . \
  -profile bp,local_workstation_rtx4070,docker \
  -c        /home/phemarajata/Downloads/snp-mod-local-working/curated_L1_overrides.config \
  --input   /home/phemarajata/Downloads/snp-mod-local-working/wf_L1v4c_run_samplesheet.csv \
  --cluster_assignments /home/phemarajata/Downloads/snp-mod-local-working/.L1_run_clusters.tsv \
  --cluster_references  /home/phemarajata/Downloads/snp-mod-local-working/.L1_run_refs_normalized.tsv \
  --split_replicons true \
  --max_cluster_size 1000 \
  --min_replicon_length 100000 \
  --gubbins_min_snps 3 \
  --gubbins_iterations 5 \
  --gubbins_use_hybrid false \
  --gubbins_skip_starting_tree true \
  --iqtree_support true \
  --outdir    /home/phemarajata/Downloads/snp-mod-local-working/L1v4c_out \
  -work-dir   /home/phemarajata/Downloads/snp-mod-local-working/L1v4c_work \
  -ansi-log false
```

**This run DID use the `bp` profile.** That matters, because §2.6 of the Methods
records that *the archived calibration run* was invoked **without** it, and the
`bp` profile is what raises the Mash sketch size to 50,000. The two statements
are about different runs and must not be collapsed. Read the sketch header, not
`params.config`.

## 3. How the commit was established, and what is *not* proven

`nextflow run .` runs a **local directory**, so Nextflow records a `scriptId`
(a content hash of `main.nf`) rather than a git commit. `e09a5c4ead` is that
hash — `git cat-file -t e09a5c4ead` fails, and anyone treating it as a SHA will
waste an afternoon. The commit was therefore established by bracketing:

- The run started **2026-08-18 19:52** and finished **2026-08-19 08:07**.
- The last commit in the repository *before* the run is **`79ab645`**
  (2026-08-16 15:17), on `main`.
- The next two commits, `f1167f4` and `19d764c`, are both dated **2026-08-19
  16:56** — nearly nine hours *after* the run finished.
- Neither of those commits touches `main.nf`
  (`git diff --stat 79ab645..19d764c -- main.nf` is empty), which is consistent
  with the recorded scriptId but does not by itself discriminate between them.

> **⚠ What this does not prove.** Because the run was launched from a working
> directory rather than a revision, **the working tree could have carried
> uncommitted edits at launch and there is no artifact that would show it.** The
> tree is clean at `19d764c` today, but that is a statement about today. The
> honest form for the paper is *"the pipeline at commit `79ab645`"*, with this
> caveat carried, and the end-to-end reproducibility run (open item 1) is what
> would actually close it. A reproduction that diffs clean against the reported
> figures retires the caveat; nothing short of that does.
>
> ✅ **That run has since happened (2026-08-25) and diffs clean.** Gate 1 = 47
> units, median r/m **7.70**, matching; per-unit r/m identical in value and raw
> SNP counts for 81 of 84 comparable units; per-unit alignment distances identical
> for 85 of 86 units. `REPRO_RESULT_2026-08-26.md`. The caveat about uncommitted
> edits is therefore retired as far as the reported figures are concerned.

## 4. What the reported run does *not* contain

The two post-run commits fix the CRLF/SIGPIPE failure recorded in the project's
own trap list — `f1167f4` pins `lineterminator="\n"` on every CSV writer and
`19d764c` drains the pipe instead of `| head -1`. **Those fixes are not in the
reported run.** The run was not hit by the bug: it completed 8,178 tasks with
**zero failures, 172/172 replicon-units** at the highest confidence tier.

This creates a real choice for the reproducibility run, which should be made
deliberately rather than by default:

- **Reproduce at `79ab645`** — tests what was actually reported, and is the
  correct choice for a reproducibility claim.
- **Reproduce at `19d764c`** — tests what a reader would get today if they
  cloned `main`. If this diverges, that is a finding about the pipeline, not
  about the analysis.

Do the first. Report the second if it differs.

## 5. Resource overrides in force

`curated_L1_overrides.config` (in this working directory, and part of the pin)
caps the local executor at 20 CPUs / 52 GB and sets per-process resources for
`SNIPPY_CORE_GATHER`, `KEEP_INVARIANT_ATCG`, `IQTREE_FAST`, `ASC_PREFLIGHT`,
`GUBBINS_CLUSTER` and `IQTREE_ASC`.

⚠ Every one of those processes carries the errorStrategy shape already on the
project's trap list:

```groovy
errorStrategy = { (task.exitStatus in [71,104,134,137,139,140,143,255] && task.attempt <= 2) ? 'retry' : 'ignore' }
maxRetries    = 2
```

A task exiting with one of those codes on attempt 3 falls through to `'ignore'`
— it is dropped, not failed. **This run lost nothing to it** (zero failures),
but a reproduction on different hardware could silently drop a unit here, and
the unit count is the first thing to check if one does.

> ⚠ **Confirmed 2026-08-25, and the cause is not hardware.** The reproducibility
> run did drop exactly one unit this way, on the *same* workstation. Gubbins at
> this commit draws RAxML's parsimony seed from an unseeded `randint(0, 10000)`;
> `strain_1_L1_30__GCF_000755905_1_2` drew `-p 0` at iteration 5, RAxML rejected
> it, and `'ignore'` dropped the unit while the run exited 0. Roughly a 16% chance
> per full panel. **Check the per-process task counts, not the exit code.**

## 6. Tool versions, from the run's own `software_versions.yml`

| tool | version |
|---|---|
| Nextflow | 25.04.6 (build 5954) |
| Parsnp | 1.7.4 |
| Gubbins | 3.4.3 |
| IQ-TREE | 2.2.6 (COVID-edition) |
| Snippy | 4.6.0 |
| Python | 3.8.20 / 3.9.5 / 3.10.2 / 3.12.0 (per-container) |
| NumPy | 1.26.2 |
| Base image | Ubuntu 22.04.5 LTS |

Containers are declared per module in the pipeline repository and are pinned by
digest where the module declares one; the authoritative list is the repository
at `79ab645`, not this table.

## 7. The control run

The A100 88-unit cross-hardware control is described in `METHODS_DRAFT` §2.12.10
and §2.12.13. **Recovered 2026-09-01** by reading the A100 host's
`~/wf-assembly-snps-mod/.nextflow.log` directly. Not reconstructed.

| | |
|---|---|
| **Nextflow** | **25.10.0** — verified, was previously carried as "unverified" |
| **Started / finished** | 2026-08-19 11:49:16 → ~15:11 (+07), ≈3 h 22 m |
| **Host** | DGX Station A100 (`cdcadmin@cdcadmin`) |
| **Record** | `/home/cdcadmin/wf-assembly-snps-mod/.nextflow.log` **and** `/data/scratch/v4c/L1v4c_out/pipeline_info/` |

Command line, verbatim from the log's `$>` line:

```bash
nextflow run . \
  -profile bp,dgx_station_a100_updated,docker \
  -c        /home/cdcadmin/v4c_partition/curated_L1_overrides.config \
  --input   /home/cdcadmin/v4c_partition/wf_L1v4c_run_samplesheet.csv \
  --cluster_assignments /home/cdcadmin/v4c_partition/.L1_run_clusters.tsv \
  --cluster_references  /home/cdcadmin/v4c_partition/.L1_run_refs_normalized.tsv \
  --split_replicons true \
  --max_cluster_size 1000 \
  --min_replicon_length 100000 \
  --gubbins_min_snps 3 \
  --gubbins_iterations 5 \
  --gubbins_use_hybrid false \
  --gubbins_skip_starting_tree true \
  --iqtree_support true \
  --outdir    /data/scratch/v4c/L1v4c_out \
  -work-dir   /data/scratch/v4c/L1v4c_work \
  -ansi-log false \
  -resume
```

### 7.1 What differs from the reported run

Compared against §2 line by line, **every analysis parameter is identical**:
`--split_replicons`, `--max_cluster_size`, `--min_replicon_length`,
`--gubbins_min_snps`, `--gubbins_iterations`, `--gubbins_use_hybrid`,
`--gubbins_skip_starting_tree` and `--iqtree_support` all match. The differences
are four, and only the first is analysis-relevant:

1. **Resource profile**: `dgx_station_a100_updated` against the reported run's
   `local_workstation_rtx4070`. This is the one substantive difference between
   the two runs and should be stated as such in the Methods, rather than
   describing them as differing only in hardware.
2. Paths, including an `/data/scratch` outdir rather than the working directory.
3. `-ansi-log false`, cosmetic.
4. **`-resume`**, discussed below.

**Both runs used the `bp` profile.** That resolves the same question §2.1 raises
for the reported run: the Mash sketch size of 50,000 applies to the control too,
so the two are comparable on that axis.

### 7.2 The `-resume` flag, and why it does not weaken the pin

The invocation carries `-resume`, which raised the question of whether the
Aug-19 11:49 session was the control's first or a continuation of an earlier one
with a possibly different command line.

**Checked 2026-09-01 and resolved.** Globbing `~/wf-assembly-snps-mod/.nextflow.log*`
on the A100 returns **exactly one file**. Nextflow rotates a previous session's
log to `.nextflow.log.1`, `.log.2` and so on, so the absence of any rotated log
means **no earlier session was ever launched from that working directory**. The
command line in §7 is therefore the only recorded invocation, not merely the last
one, and it can be cited as the control's invocation without qualification.

`-resume` was passed with nothing in that directory to resume from. Nextflow
accepts the flag whether or not a prior session exists, and a defensively-added
`-resume` on a first run is a no-op. The residual possibility is that an earlier
session ran from a *different* directory and this one resumed its cache; that
would be visible in `.nextflow/history`, which records one row per session with
its ID, run name and timestamp. Worth reading if the scratch tree still exists,
but it does not affect what is pinned above.

### 7.3 Two-source verification, matching the reported run

The `pipeline_info` directory under `~/wf-assembly-snps-mod/` is dated
**2026-05-28 and belongs to an unrelated earlier run**. Do not cite it for the
control.

**The control's own record survives** at `/data/scratch/v4c/L1v4c_out/pipeline_info/`,
confirmed 2026-09-01:

| file | size |
|---|---|
| `execution_report_2026-08-19_11-49-18.html` | 27.8 MB |
| `execution_timeline_2026-08-19_11-49-18.html` | 3.3 MB |
| `execution_trace_2026-08-19_11-49-18.txt` | 1.6 MB |
| `pipeline_dag_2026-08-19_11-49-18.html` | 3.8 KB |
| `software_versions.yml` | 231 KB |
| `process_logs/`, `qc_file_checks/` | directories |

**The command line was re-read out of `execution_report_...html` and matches the
`.nextflow.log` verbatim.** The control is therefore verified from two
independent sources, the same standard §2 sets for the reported run, and the
single-source asymmetry noted earlier does not apply.

### 7.4 The two runs, side by side

Both records read from their own `execution_report`:

| | reported | control |
|---|---|---|
| run name | `agitated_coulomb` | `insane_jennings` |
| session | `c90e1105-5b12-455e-9b31-4ecde888d559` | `13721732-3288-434b-bd23-4cab6f54dd6d` |
| **Script ID** | **`e09a5c4eadba2c5984f6790095423ee4`** | **`e09a5c4eadba2c5984f6790095423ee4`** |
| Nextflow | 25.04.6, build 5954 | 25.10.0, build 10289 |
| profile | `bp,local_workstation_rtx4070,docker` | `bp,dgx_station_a100_updated,docker` |
| started → finished | 18-Aug 19:52:00 → 19-Aug 08:07:38 | 19-Aug 11:49:18 → 15:11:52 |
| duration | 12 h 15 m 38 s | 3 h 22 m 33 s |
| CPU-hours | 200.3 | 320.5 |
| tasks | 8,178 succeeded | 8,174 succeeded |
| cached / ignored / failed / retries | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| work dir | `…/L1v4c_work` | `/data/scratch/v4c/L1v4c_work` |
| units / replicon-units / genomes | 86 / 172 / 2,352 | 88 / 176 / 2,342 |

Three things follow, and they are worth stating separately.

**1. The two runs executed byte-identical pipeline code.** The `Script ID` is
Nextflow's hash of `main.nf`, and it is the same string in both reports. This is
a stronger provenance claim than citing a shared git commit, because it is a
direct hash of what actually ran rather than of what was checked out. Combined
with `software_versions.yml`, where **every containerised tool version matches**
(Gubbins 3.4.3, IQ-TREE 2.2.6, snippy 4.6.0, parsnp 1.7.4, numpy 1.26.2, Ubuntu
22.04.5), the runs differ in exactly **two** respects: the Nextflow version and
the resource profile.

**2. `-resume` provably did nothing.** The control reports **0 cached** tasks.
Had it resumed anything, cached tasks would be non-zero. This replaces the
inference in §7.2 (drawn from the absence of rotated logs) with direct evidence.

**3. Neither run hid a failure.** Both report **0 ignored** and **0 failed** with
0 retries. That matters because an `errorStrategy`-ignored failure is precisely
what made `rc=0` misleading in the D1 re-execution. Here the reports are
explicit, so both runs completed on every task.

**Caveat on the genome counts.** The control ran 2,342 genomes to the reported
run's 2,352, and the control's set is a strict **subset**. The 10 absent genomes
are `GCA_001320065_2`, `GCA_963562295_1`, `GCA_963562875_1`,
`GCF_002900605_1_Malaysia`, `GCF_002900625_1_Malaysia`, `GCF_006381895_1`,
`GCF_028621545_1_missing`, `GCF_041028405_1`, `SRR28096039` and `SRR2896257`.
Nine fall in three frozen-basis units (`strain_1_L1_11` ×6, `strain_1_L1_22` ×2,
`strain_27_L1_1` ×1) and `SRR2896257` is not in the frozen basis. This is the
root cause of the concordance-pairing defect documented in
`A100_CFML_VALIDATION_2026-09-01.md` §4.1.

## 8. The four input files — and the one that was lost

A command line pins nothing unless its inputs travel with it. All four must be
published as supplementary material:

| file | state | contents |
|---|---|---|
| `curated_L1_overrides.config` | ✅ present | 49 lines, §5 |
| `.L1_run_clusters.tsv` | ✅ present | **2,352 genomes in 86 units** |
| `.L1_run_refs_normalized.tsv` | ✅ present | 86 references, one per unit |
| `wf_L1v4c_run_samplesheet.csv` | ❌ **LOST** | reconstructed — see below |

**The `--input` samplesheet was not retained.** It is a `.csv` in a directory
whose `.csv`/`.tsv` are gitignored, and unlike every sibling run's samplesheet
(`wf_L1v4b_samplesheet.csv`, `wf_2802_samplesheet.csv`, …) it is simply gone.

`reconstruct_v4c_samplesheet_bp.py` rebuilds it as
`wf_L1v4c_run_samplesheet.RECONSTRUCTED.csv`. The reconstruction is sound on the
things that matter and the script says where it stops:

- The **sample set** is not inferred. `.L1_run_clusters.tsv` holds exactly 2,352
  unique ids, and the run's own trace records `INFILE_HANDLING_UNIX` executing
  exactly **2,352** times — one task per staged genome. Two independent
  artifacts, same number; the script aborts if they ever disagree.
- The **paths** are not inferred: all 2,352 carry an `assembly_path` in
  `L1v4c_MERGED_METADATA.tsv` and all 2,352 resolve on disk, across three
  directories (2,226 + 121 + 5).
- **Not proven:** row order, and that the original used these exact absolute
  paths. Neither can affect the result — Nextflow stages by content and the
  pipeline groups by `--cluster_assignments`, not by samplesheet order — but the
  filename says RECONSTRUCTED because that is what it is.

## 9. What the run was given vs what is reported

Worth stating plainly, because the two differ and the difference is deliberate:

| | units | genomes | replicon-units |
|---|---|---|---|
| **given to the pipeline** | 86 | 2,352 | 172 |
| **reported basis** | **85** | **2,340** | **170** |

The trace corroborates the input side exactly: 86 `SPLIT_REFERENCE_REPLICONS`,
172 `GUBBINS_CLUSTER`, 172 `IQTREE_ASC`, 2,352 `INFILE_HANDLING_UNIX`. The
reported basis is a **post-hoc correction of this run's output**, not a
re-execution — `strain_1_L1_10` dropped below the floor after deduplication,
plus five further duplicate/excluded genomes (`METHODS_DRAFT` §2.12.5). A
reproduction will therefore reproduce **86/2,352/172** and must then be put
through the same correction to land on 85/2,340/170.

> **Tested 2026-08-25: it reproduced 86 / 2,352 / *171*.** Units and genomes were
> exact; replicon-units came up one short because of the unseeded-seed drop in §5.
> Expect 171 about one run in six. The lost unit must be excluded rather than
> carried, because Gate 1 sums per-replicon divergence and a unit missing a
> replicon can be pulled into the window that its full self falls outside.

## 10. Reproduce

```bash
git clone https://github.com/PHemarajata/wf-assembly-snps-mod && cd wf-assembly-snps-mod && git checkout v1.0.5-mod
```

Then the §2 command line with the four §8 inputs repointed. `v1.0.5-mod` is the
release tag at `79ab645`, created 2026-08-26. Note the manifest at that commit
self-reports `v1.0.3-mod`, which is a different and older commit, so the run log
will print that string. Verify completion from the per-process task counts, not
the exit code, for the reason in §5.
