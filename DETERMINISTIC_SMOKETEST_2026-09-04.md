# The workflow is byte-reproducible end to end under `--deterministic true`

**2026-09-04.** Closes the "not demonstrated end to end through the workflow"
gap left by `DETERMINISM_DEMONSTRATION_2026-09-04.md`. The earlier work measured
Gubbins on alignments and IQ-TREE on alignments, each outside the pipeline. This
runs the whole workflow twice and compares everything it published.

> **Result: all ten scientific outputs are byte-identical across two runs.**
> **45 of 58** comparable published files match exactly, after the ordering fix
> below. The 13 that differ are timestamps, runtimes and work-directory paths.

---

## 1. What was run

| | |
|---|---|
| pipeline | `wf-assembly-snps-mod` `main@b8c6b85` |
| Nextflow | 25.04.6 |
| containers | apptainer 1.5.3 |
| input | 9 real *B. pseudomallei* genomes, unit `s4_L1_5`, `smoketest_s4_L1_5_samplesheet.csv` |
| profile | `bp,local_workstation_rtx4070,singularity` plus a run-time overlay |
| parameters | `--deterministic true --global_ml_tree false` |
| runs | two, **sequential**, each with its own `--outdir` and `-work-dir` |
| duration | 2 m 56 s and 2 m 46 s |

Sequential and separately-rooted is not incidental. Gubbins writes scratch to the
working directory regardless of `--prefix`, and concurrent runs sharing one
collide. That failure is invisible in single-run testing and has already cost
this project three wrong conclusions.

**The determinism flags demonstrably took effect**, read back from the generated
task scripts rather than assumed from the parameter:

| flag | occurrences |
|---|---|
| `--seed 20260904` (Gubbins) | 3 |
| `--threads 1` (Gubbins) | 3 |
| `-seed 20260904` (IQ-TREE) | 2 |
| `-T 1` (IQ-TREE) | 3 |

Both IQ-TREE stages are covered: `IQTREE_FAST`, which builds the Gubbins starting
tree, and `IQTREE_ASC`, which builds the per-unit final tree. Those are the calls
that ran unseeded and multi-threaded until this morning.

## 2. Exit code 0 is not the check

Both runs exited 0. So did the run that lost a unit in August. The check is
per-task:

| | run A | run B |
|---|---|---|
| processes submitted | 34 | 34 |
| tasks carrying an exit code | 34 | 34 |
| **non-zero exit codes** | **0** | **0** |
| process sets identical | yes | yes |

## 3. The comparison

Every published file outside `work/`, hashed with SHA-256.

| | files |
|---|---|
| present in both | 58 |
| **identical** | **45** |
| differing | 13 |
| present in only one | 0, outside `pipeline_info` |

### The scientific outputs, all identical

| output | |
|---|---|
| `cluster_0.per_branch_statistics.csv` | the numerator and denominator of r/m |
| `cluster_0.recombination_predictions.gff` | the called recombination tracts |
| `cluster_0.node_labelled.final_tree.tre` | the Gubbins tree |
| `cluster_0.filtered_polymorphic_sites.fasta` | the filtered alignment |
| `cluster_0.final.treefile` | **IQ-TREE ASC, the per-unit final tree** |
| `cluster_0.treefile` | **IQ-TREE fast, the starting tree** |
| `backbone.treefile` | the backbone |
| `global_grafted.treefile` | the grafted tree |
| `recombination_rm.tsv` | pooled r/m |
| `cluster_phylogeny_summary.csv` | the per-unit summary the audit reads |

### The 13 that differ, and why each one does

| files | what differs |
|---|---|
| 9 × `process_logs/*.command.err` | log timestamps |
| 2 × `*.iqtree` | IQ-TREE's own "Date and time" line and its two runtime lines |
| 1 × `backbone_report.txt` | a UTC timestamp |
| 1 × `Gubbins/cluster_0.diagnostics.log` | work-directory paths, and 20 lines that differ only in a timing float |

`Summary.QC_File_Checks.tsv` and `software_versions.yml` were a fifteenth and
sixteenth entry here until the ordering fix in section 4. They are identical
now.

The Gubbins log was the one worth checking properly rather than waving through.
After masking work-directory paths, 20 line pairs differ. Every one of them
differs in a timing number and nothing else: no text differs, and no likelihood
moves. Both log-likelihood values, `-9645778.005072` and `-9645929.937335`,
appear identically in both runs.

## 4. One real nondeterminism, since fixed

`Summaries/Summary.QC_File_Checks.tsv` and `pipeline_info/software_versions.yml`
held **the same rows in a different order** on every run. Nextflow's collection
order, not a tool's output, so it touched no number and no tree. Fixed anyway,
because a diff of two agreeing runs should be empty, and a reviewer who diffs
these two files and sees noise learns to skip them.

The QC summary used `collectFile(sort: 'index')`, which is the order chunks
arrived on the channel, that is, task completion order. Measured over 3 runs of
an 8-task harness with randomised completion times:

| `sort:` | run 1 vs 2 | run 1 vs 3 |
|---|---|---|
| default | differs | differs |
| `'index'` | differs | differs |
| `true` | differs | differs |
| **`{ it.name }`** | **same** | **same** |

The versions file had no `sort` at all, and sorting by name would not have helped
because every chunk is named `versions.yml`, so the key ties. It sorts by content
now. Both files carry the same rows and the same count as before; only the order
changed. **Verified over two further full runs: both are byte-identical.**

### The fix surfaced a second defect in the same file

`software_versions.yml` also carried a stray line, `    END_VERSIONS`. `<<-`
strips leading **tabs** only, so a space-indented terminator is not recognised.
Bash closed the heredoc at end-of-file with a warning and wrote the terminator
into the file as content.

It bites only where Nextflow does not dedent the script block, and Nextflow
dedents by the block's **minimum** indentation, so one wrapped error message
starting at column 0 silently arms every heredoc in that process. 57 of 58 sites
in the repository worked for that reason alone. All 58 terminators are at column
0 now, which is recognised either way, and CI asserts it. The stray line and the
bash warning are both gone, confirmed over a full run.

### One thing that is still not reproducible, correctly

`cluster_phylogeny_summary.csv` carries an `iqtree_log_size_bytes` column, which
is the byte size of a log containing timestamps and runtimes. It moves by a byte
or two between runs: 4220 against 4221 in one pair, equal in two others. That is
luck, not determinism. It is a diagnostic column rather than a result, and the
earlier claim here that the file was identical held only because the byte counts
happened to agree.

### Noted and not fixed

`software_versions.yml` does not parse as YAML, before or after this change.
Module script blocks dedent by different amounts, so some entries are emitted at
column 0 and others at four spaces. Making it valid means normalising every
heredoc body, which changes the published file's shape, so it is left for a
decision.

## 5. What this does not show

**Scale.** Nine genomes, one cluster, one replicon-unit, three minutes. The
frozen basis is 85 units and 2,340 genomes. Determinism at this size does not
prove it at that size, and the cost multiplier grows with taxa: measured 1.28x at
8 taxa and 1.98x at 37.

**`GLOBAL_ML_TREE` is not exercised.** Nine genomes form one cluster, so
`GLOBAL_CORE_ALIGNMENT` receives one medoid and refuses, correctly, because a
global tree needs at least three. It is disabled here with
`--global_ml_tree false`.

That refusal is instructive on its own. Left enabled, it races the rest of the
graph: the first attempt had run A already submitting `IQTREE_ASC` when the
failure hit and run B not, so the two runs completed **different task sets**, 11
processes against 9. Nothing was wrong with either run's determinism. The
comparison was simply between two different pipelines, and a per-process count is
what caught it rather than the diff.

**The reported analysis is still not reproducible.** It predates every one of
these parameters and ran unseeded and multi-threaded through both tools.
Re-running it under `--deterministic true` produces a different run rather than
validating the pinned one.

## 6. Two things that got in the way, both worth knowing

**`~/.docker/config.json` holds a Docker Hub access token that expired in
September 2025.** Apptainer reads that file, prefers the stale credential over
anonymous access, and Docker Hub answers `unauthorized: incorrect username or
password`. That reads exactly like a rate limit and is not one; it also fails
intermittently, because only the Docker Hub images are affected and quay.io is
most of them. Pointing `DOCKER_CONFIG` at an empty directory for the run makes
the pulls anonymous and they succeed. The credential file was not modified. It is
worth refreshing or removing, because anything on this host that pulls from
Docker Hub is hitting the same wall.

**Selecting the singularity profile does not select singularity.**
`-profile bp,local_workstation_rtx4070,singularity` resolves to
`docker.enabled = true` and `singularity.enabled = false`, and so does every
other ordering of those three tried, including putting singularity last where
Nextflow's documented left-to-right precedence should make it win. `-profile
singularity` and `-profile bp,singularity` both resolve correctly, so it is the
workstation profile that wins over a later selection. A `-c` overlay at run time
does work.

This is the profile-ordering hazard already documented in
`conf/profiles/low_spec.config`, in a place that comment does not cover: not
which science parameters win, but which **container engine** runs. A run launched
with `-profile ...,singularity` on a host with a working Docker daemon would
silently use Docker and nobody would see it.

## 7. Reproduce

```bash
nextflow run . -profile bp,local_workstation_rtx4070,singularity \
  -c <overlay forcing singularity> \
  --input smoketest_s4_L1_5_samplesheet.csv \
  --outdir <out> --deterministic true --global_ml_tree false \
  -work-dir <out>/work -ansi-log false
```

Outputs are under `DET_SMOKETEST/run_a` and `DET_SMOKETEST/run_b`. Compare with
SHA-256 over every published file, excluding `work/`.
