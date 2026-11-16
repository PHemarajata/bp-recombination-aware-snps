# Index: what is authoritative, and what is superseded

**Written 2026-09-24.** The repository tracks 267 files, 105 of them root-level
markdown. This says which one to read for each live question, and which look
current but are not.

Files are **not** moved or renamed. Scripts, the CI citations job, the Mac
bundle builder and `STATE`'s own document map all reference documents by literal
name, and three of those four break silently on a rename. This index is the
navigability fix; the tree stays as it is.

---

## Read these first, in this order

| | file | why |
|---|---|---|
| 1 | **`STATE_2026-09-02.md`** | the canonical snapshot. It says in its own words that it and `NUMBERS.tsv` win when documents disagree. Its §8 is a document map for the 2026-09-02 work and its §3 lists the numbers that are easy to get wrong |
| 2 | `MIGRATION_TO_MAC_2026-09-14.md` | the working copy moved to the Mac on 2026-09-14. This repository is code and documentation only |
| 3 | `SUBMISSION_TODO.md` | the open items, with the reasoning behind each |
| 4 | `HANDOFF_2026-09-04_EVENING.md` | the latest manuscript-side handoff |
| 5 | `HANDOFF_VIRTUAL_MANUSCRIPT_2026-09-08.md` | the latest video-side handoff |

`README.md` still says to start with `METHODS_DRAFT_2026-08-19.md`. That is a
138 KB methods document and a poor entry point. Start with `STATE`.

---

## By question

### The recombination rate and the operating range

**`MANUSCRIPT_DRAFT_2026-09-02.md`** is the current manuscript, on the reported
85-unit basis throughout. Its nine Results sections are the partition, the
operating range, r/m, subdivision, detection bounds, tree-builder robustness, two
silent failure modes, country-versus-collection-history, and reproducibility.

**r/m is 7.70.** Not 7.44 (the A100 run), not 7.38 (A100 under the Mash proxy),
not 7.26 (this basis under the Mash proxy), and never the all-unit median 5.51,
which mixes measurements with detection failures. `STATE` §3 has the table.

### Attribution of exposure origin

**`ATTRIBUTION_SPECIFICATION_CURVE_2026-09-02.md`** is authoritative, and it
revises the August framing. Country fails against the majority-class baseline,
region works under `modal_k20` and not under nearest neighbour, and the estimator
is part of every number.

⚠ **`RESULTS_DRAFT_2026-08-23.md` §R2 and `ABSTRACT_DRAFT_2026-08-23.md` predate
it.** Both read as current and are partially superseded. Specifically: the
close-relative strata (2/14, 14/14) must not be quoted without each stratum's own
baseline, and the resolution curve spans 7 MLST loci to 4,089 cgMLST loci on a
26 or 31 genome denominator, not whole-genome SNPs on 46.
`ABSTRACT_IDLABCON_REVIEW_2026-09-24.md` has the full list.

`MANUSCRIPT_COMPILED_2026-08-26.md` is an August compilation and carries the same
superseded attribution framing.

### Geographic structure

**Paper 2 is superseded and must not be written.**
`PUBLICATION_STRATEGY_2026-09-02.md` carries the retraction inline: 26 of 85
units cluster by country, 6 survive the BioProject control, and the control
removes 77% of the apparent signal. The finding moved into Paper 1 as Results
section 8. `CONTROL_SPECIFICATION_2026-09-02.md` is the headline conclusion,
with `BIOPROJECT_COUNTERFACTUAL`, `BIOPROJECT_CHARACTERIZATION` and
`BATCH_PROXY_AUDIT` as its supporting tier.

### The background literature

⚠ **`BP_background_section.md` carries two bibliographies with two numberings.**
Of 277 citation marks, 102 land on the paper the sentence means, **136 land on a
different paper**, and 36 land on nothing. It is not quotable until resolved.
`BACKGROUND_BIBLIOGRAPHY_DEFECT_2026-09-04.md` measures it and
`BACKGROUND_BIBLIO_COMPARISON.md` reports per number. The manuscript's own 34
references are clean and separate.

### The ID Lab Con 2027 abstract

Three files, **all of which arrive with PR #28 and are not on `main` yet**:
`ABSTRACT_IDLABCON_2027.md` is the submission text,
`ABSTRACT_IDLABCON_REVIEW_2026-09-24.md` is what was wrong in its first draft,
and `MAC_VERIFICATION_REQUEST_2026-09-24.md` is what still needs checking on the
Mac.

---

## Traps that have already cost time

**Numbers go stale between the tree and the session.**
`PR3_CORRECTIONS_2026-09-02.md` documents a session that branched from a stale
`main` and faithfully reproduced a two-week-old world, and predicts the failure
will recur. It did recur, on 2026-09-24, in the first draft of the ID Lab Con
abstract. Check document dates against `STATE` before quoting.

**`generate_numbers.py` used to truncate `NUMBERS.tsv`.** It opened the file with
`"w"` and wrote only the keys it computed, deleting 35 hand-computed figures on a
file of 101. **Fixed on `main` 2026-09-24** in PR #29. The fix had sat unmerged
on `origin/worktree-clip2-review` since 2026-09-17 while `main` kept the
destructive version, so **any checkout not pulled since then still destroys
those figures**.

**No `.tsv` is in this repository.** `.gitignore` carries a blanket `*.tsv` and
the `no-data-tracked` CI job enforces it. `NUMBERS.tsv` and every other data file
live only on the Mac, and reached it in the curated bundle rather than through a
clone.

**A low r/m is a detection failure, not a clonal unit.** The single most
important thing to know when reading any result here.

---

## Branches, as of 2026-09-24

`main` is current. `claude/gracious-cannon-8d6z53` is PR #28.
`docs/film-work-2026-09`, `worktree-clip2-review` and `feat/room-tone-bed` hold
film work and are deliberately left alone: the last two have **diverged**, both
containing the first but neither containing the other, with 41 differing paths.
`REPO_CLEANUP_PLAN_2026-09-24.md` has the branch-by-branch survey, and arrives
with PR #28 rather than with this change.
