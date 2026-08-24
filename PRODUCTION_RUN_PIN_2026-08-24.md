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
and §2.12.13. **Its command line is not pinned here** — no equivalent
`pipeline_info` record for it was found in this working directory, and the
run itself lives on the A100. Pin it from that host's `.nextflow.log` before
submission, or state in the Methods that the control's exact invocation was not
retained. Do not reconstruct it from this one.

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

## 10. Reproduce

```bash
git clone https://github.com/PHemarajata/wf-assembly-snps-mod && cd wf-assembly-snps-mod && git checkout 79ab645
```

Then the §2 command line with the four §8 inputs repointed.
