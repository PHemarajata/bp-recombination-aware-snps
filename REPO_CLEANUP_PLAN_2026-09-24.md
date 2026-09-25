# Repository cleanup: survey and plan

**2026-09-24.** Read-only survey first. Nothing below has been executed except
the warning already pushed to `MAC_VERIFICATION_REQUEST_2026-09-24.md`.

---

## 0. The finding that changes the priority

**`main` carries a `generate_numbers.py` that destroys data, and the fix has
never been merged.**

On `main` the script opens `NUMBERS.tsv` with `"w"` and writes only the keys it
computes. A branch recorded on 2026-09-17 that the file held **101 figures while
the script built 66**, so a plain run **silently deleted 35**, including every
`controls.*` constant and the six `rm.*` keys carrying the Gate 1 window, its
brackets, the in-window IQR and the floor sensitivity.

The fix rewrites the write as a merge and prints which figures were carried
rather than recomputed. It lives only on `origin/worktree-clip2-review`.

This is the single highest-value thing in the cleanup, and it is a correctness
fix rather than tidying.

---

## 1. Branch survey

| branch | ahead | behind | unique files | verdict |
|---|---|---|---|---|
| `chore/track-a100-stage-scripts` | 0 | 126 | 0 | **fully merged, safe to delete** |
| `claude/citation-audit-2026-09-03` | 0 | 86 | 0 | **fully merged, safe to delete** |
| `fix/manuscript-tooling-on-frozen-basis` | 0 | 95 | 0 | **fully merged, safe to delete** |
| `docs/film-work-2026-09` | 33 | 0 | 26 | contained in **both** branches below, redundant |
| `worktree-clip2-review` | 47 | 0 | 35 | **carries the `generate_numbers.py` fix** |
| `feat/room-tone-bed` | 86 | 0 | 53 | most film work, **diverged** from clip2-review |
| `claude/bp-genomics-research-t1b68u` | 3 | 123 | 31 | old handoffs, 2026-08-10 to 08-19 |
| `feat/core-shrinkage-and-itol` | 2 | 56 | 2 | a reading copy and an A100 assessment |
| `claude/gracious-cannon-8d6z53` | 15 | 0 | 4 | this work, PR #28, open |

Only **PR #28** is open. Every other branch was pushed and never proposed.

**The divergence that needs a human decision.** `worktree-clip2-review` and
`feat/room-tone-bed` both contain `docs/film-work-2026-09`, but neither contains
the other. **41 paths differ between them**, including `TABLES.md`,
`make_tables_bp.py`, `.gitignore`, and four `tuc_briefing/` files that exist only
on clip2-review. Merging one and deleting the other loses work.

---

## 2. Plan, ordered by risk

### Phase 1 — land the `generate_numbers.py` fix. Do this first.

Cherry-pick the merge-write change onto a branch off current `main`, open a PR,
land it. It is self-contained and touches one file. Until this is on `main`,
anyone following the documented workflow can destroy 35 figures.

*Risk: low. Benefit: prevents silent data loss.*

### Phase 2 — delete the three fully merged branches.

`chore/track-a100-stage-scripts`, `claude/citation-audit-2026-09-03`,
`fix/manuscript-tooling-on-frozen-basis`. Each has **zero** commits `main` does
not already contain, verified by `git rev-list --count origin/main..<branch>`.

*Risk: none. Nothing is lost, because nothing is unique.*

### Phase 3 — the film branches. **Needs your decision.**

Three options, and I cannot pick between them from the repository alone:

- **(a)** Merge `feat/room-tone-bed` into `main`, then merge
  `worktree-clip2-review` on top and resolve the 41 differing paths.
- **(b)** Merge `feat/room-tone-bed` only, and cherry-pick the
  `generate_numbers.py` fix and the four `tuc_briefing/` files from
  clip2-review.
- **(c)** Leave both as branches and land only Phase 1.

Which film cut is current is a question about the films, not about git.

### Phase 4 — the two stale branches with unique files. **Needs your decision.**

`feat/core-shrinkage-and-itol` holds `MANUSCRIPT_READING_COPY_2026-09-02.md` and
`HANDOFF_A100_ASSESSMENT_2026-09-02.md`. Both look like things worth keeping,
and both are two commits from a branch 56 behind.

`claude/bp-genomics-research-t1b68u` holds 31 files, nearly all handoffs dated
2026-08-10 to 2026-08-19 plus `METHODS_DRAFT_2026-08-11.md`. Superseded by
what is on `main`, but they are the only record of that period.

Landing either means merging a branch that is 56 or 123 commits behind, which
will conflict. Cherry-picking the files is cleaner.

### Phase 5 — root-level sprawl. **My recommendation: do not move files.**

`main` tracks **267 files**, of which **105 are root-level markdown**, 104 are
`.py` and 48 are `.sh`. It is genuinely hard to navigate.

**But moving them is more dangerous than it looks.** The CI `citations` job
reads `MANUSCRIPT_DRAFT_2026-09-02.md` and `BP_background_section.md` by literal
path. `generate_numbers.py` and its siblings read a dozen data files by literal
name. The Mac bundle in `MIGRATION_TO_MAC_2026-09-14.md` is built by grepping
filenames out of `*.py`, so a moved file silently drops out of the next bundle.
`STATE_2026-09-02.md` §8 references documents by name as the project index.

A rename breaks all four, and the breakage is silent in three of them.

**Instead: add one index and leave the tree alone.** `STATE_2026-09-02.md` §8
already does this for the 2026-09-02 documents. Extending that into a single
current `INDEX.md` that says, for each live question, which file is
authoritative and which are superseded, gets the navigability without the blast
radius.

---

## 3. What I will not do without you saying so

- Delete any branch that has unique commits.
- Force-push or rewrite history anywhere.
- Move or rename any tracked file.
- Merge the diverged film branches.
