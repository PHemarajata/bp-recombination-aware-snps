# B. pseudomallei recombination-aware SNP phylogeny — analysis code

Analysis and orchestration code for a recombination-aware SNP phylogeny of
*Burkholderia pseudomallei*, built to support **rapid origin-of-exposure
attribution for melioidosis cases without travel history**.

The pipeline itself lives in a separate repository
(`wf-assembly-snps-mod`). This repository holds the surrounding work: panel
construction, partitioning, reference selection, calibration, diagnostics, and
the run orchestration and monitoring used on both the workstation and the A100.

## No data in this repository — by design

**No isolate-level data is tracked here.** No assemblies, alignments, trees,
metadata tables, cluster memberships or samplesheets. *B. pseudomallei* is a US
Tier 1 Select Agent and the study metadata joins accession to isolation location,
collection date and exposure label, which is re-identifiable for rare cases.

`.gitignore` therefore **denies everything by default** and re-admits only source
code and documentation, at the top level, by extension. Subdirectories are not
re-admitted at all — every output, work directory and bundle lives in one.

Before any push:

```bash
git ls-files | xargs -r du -ch | tail -1   # total tracked size
git ls-files                                # read the whole list
```

`git add -f` bypasses all of it. Do not use it without checking what you are
forcing.

## Method, in one paragraph

Gubbins detects recombination as unusually SNP-dense regions against a clonal
background, so it only works on a population of the right diversity. The genomes
are therefore partitioned first — PopPUNK strains, subdivided by fastbaps, with
analysis units taken at level 1 and retained at n >= 7 — and Gubbins is run
within each unit, per replicon, never across the whole collection.

**The operating range was measured, not assumed**, because Gubbins publishes no
divergence ceiling. Outside roughly **1,270–4,671 mean pairwise core SNPs** the
r/m estimate is not a measurement: below the floor recombination cannot be
detected, above the ceiling the estimate collapses. **A low r/m is therefore a
detection failure, not a clean unit** — the single most important thing to know
when reading these results.

## Layout

- `*.py`, `*.sh` — panel construction, partitioning, reference selection,
  calibration, diagnostics, orchestration and monitoring
- `*.md` — methods drafts, handoffs, calibration and investigation records

Start with `METHODS_DRAFT_2026-08-19.md`.

## Working conventions

Two rules explain most of the code:

**Check per-item values; never infer from a summary line.** Every serious defect
in this project produced plausible output — a CRLF line terminator that made a
run report success while doing nothing, a RAxML crash that surfaced as "Unable to
fit model to data", ONT assemblies that passed every automated gate.

**A clean exit does not mean every unit succeeded.** The workflow runs with
`errorStrategy 'ignore'`. Verification compares units *requested* against units
that actually produced output, per unit, before any number is quoted.
