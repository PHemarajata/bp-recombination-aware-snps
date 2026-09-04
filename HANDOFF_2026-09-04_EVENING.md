# Handoff, 2026-09-04 evening

Supersedes `HANDOFF_2026-09-04.md` on its five open items. Read that one first
for what closed in the morning; this covers what happened to its open list.

---

## Where everything is

| | |
|---|---|
| **Analysis repo** | `claude/citation-audit-2026-09-03` at `9f19fe5`, 44 commits ahead of `main`, pushed, CI green |
| **Open PR** | [#21](https://github.com/PHemarajata/bp-recombination-aware-snps/pull/21), base `main` |
| **Pipeline repo** | `~/wf-assembly-snps-mod`, `main` at `b8c6b85`, CI green on nine jobs |
| **Tag `v1.1.0-mod`** | still `0551e72`. **Not moved.** `main` is 3 commits past it, two of which change behaviour, so the tag no longer describes the tip |
| **Frozen basis** | unchanged: 85 units, 2,340 genomes, r/m **7.70** |

---

## The morning's five items

**1. Nextflow 26.x. Closed.** `nextflow config .` succeeds on 24.10.5, 25.04.6,
25.10.0 and 26.04.6 across all eleven profiles, 44 combinations. Six separate
things blocked it, each hidden behind the one before, so the count went up as the
work went on. `PROVENANCE.md` has the table.

Nothing any profile allocates has changed, and that was measured: seven
processes, one per label, failing twice so each ran at `task.attempt` 1, 2 and 3,
five profiles, 21 measurements each, old against new, **identical in all 105**.

**The one place it nearly went wrong is worth knowing.** `check_max()` was
replaced by the `resourceLimits` directive. Written as a plain list,
`resourceLimits` binds `params.max_*` once, when the file is parsed. `check_max()`
read them per task. So a ceiling set in a later `-c` overlay is silently ignored:
12 cpus where the overlay says 3. It passed every check first run against it,
because a command-line `--max_cpus` is honoured either way and that is what was
tested. A negative control caught it. All seven declarations are closures now and
CI asserts it.

**2. The background bibliography. Measured, not fixed, and the problem is much
larger than 34 dangling citations.**

`BP_background_section.md` carries two bibliographies with two different
numberings. The prose follows the machine-readable block in the body. The
`## References` list is the other one. They agree on `[1]`-`[40]` and diverge from
`[41]` on.

Of 277 citation marks in the prose: 102 land on the paper the sentence means,
**136 land on a different paper**, 36 land on nothing.

No dangling-and-orphan audit could have seen it. Every number in `[1]`-`[96]` has
an entry and every entry is cited, so both counts are perfect while the citations
are wrong. `verify_references_bp.py` now detects it and
`compare_bibliographies_bp.py` reports it per number.

This refutes `BACKGROUND_SCOPE_DECISION_2026-09-03.md`'s "five lookups, not
sixty-five". 120 of the 130 need resolving against a primary record. Promoting the
body block is not the shortcut it looks like: its entries pair one paper's title
with another's PMID, and eleven carry the `10.60692` fabrication signature.

Written up in `BACKGROUND_BIBLIOGRAPHY_DEFECT_2026-09-04.md`, per number in
`BACKGROUND_BIBLIO_COMPARISON.md`, and as a warning at the head of the list
itself so it cannot be quoted unaware.

**3. Manuscript citations. Closed.** 34 references, all cited, all defined, no
dangling, no orphans, no `[CONFIRM]` in the reference block. Every one retrieved
from PubMed in session.

`[17]` fastbaps is complete. `[18]`, one placeholder standing for seven tools, is
now nine entries: Nextflow, SKA2, Mash, Snippy, RAxML, IQ-TREE 2, parsnp, BUSCO,
Seq-Gen. Mash and Nextflow were not in the placeholder and were uncited entirely.
Seq-Gen is now named where the null simulation is described; it was used and
never mentioned. The last citation `[CONFIRM]`, on the two outbreak SNP figures,
is closed with Sarovich 2017 and Aziz 2017.

**`[14]` cited PMID 22163051, which is a paper about cannabidiol and
neuroinflammation.** The correct record is 22180792. The DOI beside it was
already right, which is why it survived review: a wrong PMID next to a right DOI
looks consistent unless one of them is resolved.

20 `[CONFIRM]` markers remain in the body and every one is an author decision:
word counts, deposition, funding, author roles, IRB, and two editorial calls.

**4. The reproducibility test. Run at smoke-test scale, and it passes.**

`gubbins_deterministic` governed Gubbins and never governed IQ-TREE. All five
IQ-TREE invocations ran unseeded and multi-threaded, two of which produce
reported output: `IQTREE_ASC` builds the per-unit trees and `GLOBAL_ML_TREE` the
global one. `conf/params.config` had asserted the same measurement for IQ-TREE
since that morning. Nothing acted on it. **That is the `gubbins_seed` defect a
second time.**

Measured on three real unit alignments, production invocation, treefile compared
byte for byte: unseeded at 4 threads differs, seeded at 4 threads differs,
unseeded at 1 thread differs, seeded at 1 thread is identical on all three. Both
are required, which is sharper than the Gubbins result.

Fixed: `iqtree_seed` passed always, and `deterministic` pinning both tools.
`gubbins_deterministic` still works and either turns it on. CI asserts all five
invocations.

**Then run.** Two full workflow runs over the 9-genome smoke test, sequential,
separate working directories, `--deterministic true`. Both 34 tasks, zero
non-zero exit codes, identical process sets. **All ten scientific outputs
byte-identical**, including both IQ-TREE trees. Of 58 comparable published files,
43 match exactly and the 15 that differ are timestamps, runtimes, work paths, and
two files whose rows are the same in a different order.
`DETERMINISTIC_SMOKETEST_2026-09-04.md` has the detail. The full-scale run is
still open, and so is `GLOBAL_ML_TREE`, which a single-cluster test cannot
exercise.

**5. PR #21. Ready for review, not merged.** 44 commits, mergeable, clean, and
the description now covers today's work. It was left for you rather than merged:
the morning handoff authorised a merge of a 37-commit branch, and what is on it
now is materially different, including the judgement call not to rebuild the
background's 130 references. Merge with a **merge commit, not squash**; the
commit titles are the record of which claim was corrected when.

---

## What to do next, in the order I would take it

**1. Run the reproducibility test at full scale.** The smoke-test scale is done
and passes; see item 4 above and `DETERMINISTIC_SMOKETEST_2026-09-04.md`. What is
left is whether it holds over 85 units and 2,340 genomes, and `GLOBAL_ML_TREE`,
which needs at least three medoids and so cannot run on a single-cluster test.

```bash
nextflow run . -profile bp,local_workstation,docker --deterministic true \
        --input <samplesheet> --outdir <out>
```

Two things to settle before starting it:

- **The Docker daemon is not running on this workstation** and starting it needs
  root. `apptainer` 1.5.3 is available if you would rather not.
- **Cost.** The 2026-08-24 full run took 12 h 24 m across two segments,
  non-deterministic. Determinism measured 1.28x at 8 taxa and 1.98x at 37, and
  units run to 159, so budget more than 2x. Demonstrating reproducibility needs
  two runs. Call it two days of the workstation.

Two things found while running the smoke test that will bite the full run:

- **`~/.docker/config.json` holds a Docker Hub token that expired in September
  2025.** Apptainer prefers it over anonymous access and Docker Hub answers
  "unauthorized: incorrect username or password", which reads like a rate limit
  and is not one. Anything on this host pulling from Docker Hub hits it.
- **`-profile ...,singularity` does not select singularity.** The workstation
  profile wins and resolves `docker.enabled = true`, whatever order the profiles
  are given in. A `-c` overlay at run time works. On a host with a working Docker
  daemon this would silently run under Docker and nobody would notice.

**2. Decide what the background section is for.** The three options are set out
at the end of `BACKGROUND_BIBLIOGRAPHY_DEFECT_2026-09-04.md`. Nothing else in the
citation work is blocked on it, and the manuscript is not.

**3. Move `v1.1.0-mod`, or cut `v1.2.0-mod`.** The tag is 3 commits behind
`main`. Two of them change behaviour, the 26.x config migration and the IQ-TREE
determinism control, and the third is CI only. `PROVENANCE.md` already records that the tag was moved more
than once on the day it was made, so moving it again is the worse option. A new
tag is cleaner. Resolve any tag with `git rev-list -n1 <tag>`, never from a
transcribed SHA.

**4. The 20 author-decision `[CONFIRM]` markers.** These are the critical path to
submission and none of them is a lookup.

---

## Three things worth distrusting

**A check that cannot fail is worse than no check, and I wrote three of them
today before noticing.** The IQ-TREE seed check matched an echoed error message
and missed the real `IQTREE_ASC` call, which is written as an escaped shell
variable. Tightened, it then matched `[ -s gml.iqtree ]`, where `-s` is the
shell's file test and not IQ-TREE's input flag. Both times the count guard caught
it, not reading it. **Every check added today asserts a minimum count and was
broken on purpose before being trusted.**

**A Python f-string emitting `${{` killed an entire CI run before any job
started.** GitHub evaluates that sequence as an Actions expression anywhere in a
workflow file, including inside a `run:` block it never executes. It fails in 0
seconds, with no log, no annotation beyond "workflow file issue", and
`gh run view --log-failed` returns "log not found". Nothing in the diff is wrong
as Python. The syntax job now checks for it.

**Scoping a rewrite to a heading is not optional.** Renumbering the manuscript's
references matched the submission checklist below, because that checklist is
itself a numbered list restarting at 1. Same defect the morning's handoff records
for the reference audit, met again in a second place within hours.

---

## Two things that have not changed

**The reported analysis is `v1.0.5-mod` at `79ab645` and is not
seed-reproducible.** It ran unseeded and multi-threaded through both Gubbins and
IQ-TREE. Re-running it under `--deterministic true` produces a different run
rather than validating the pinned one. This is not recoverable and belongs in the
Methods, stated once and plainly.

**Units.** Gate 1's window is `[700, 4700]` mean pairwise core SNPs on the
**alignment** basis. Quote r/m **7.70** in-window on the frozen basis, never the
all-unit median. The estimator is part of every attribution number: `nearest_nb`
is country's best and `modal_k20` is region's, and mixing them produces a figure
belonging to neither.
