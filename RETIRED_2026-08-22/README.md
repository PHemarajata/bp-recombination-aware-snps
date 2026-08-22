# Retired 2026-08-22

Files moved out of the immediate workspace because they are **not on the frozen
analysis basis** (`FINAL_BASIS_2026-08-22/`, 85 units, 2,340 genomes) and could
be picked up by accident.

**Nothing here is deleted and nothing here is wrong.** Most of it was correct for
the partition it was computed on. It is retired because quoting it against the
frozen basis would mix partitions — the failure mode that caused the repeated
corrections this freeze exists to stop.

66 files. Read `DOWNSTREAM_IMPACT_2026-08-22.md` before resurrecting any of them.

---

## `a100_control/` — 7 files

The A100 88-unit run's outputs: `PHYLOGEOGRAPHY_ASSOCIATION_v4c_A100.tsv`, the
four `SCALE_*.tsv`, `trackA_diversity_88units.tsv`,
`GATE1_ALIGNMENT_A100_2026-08-21.tsv`.

**These are still live evidence, just for a different purpose.** The A100 run is
the **cross-hardware reproducibility control** (0.46% median relative r/m across
the 82 shared units), and `METHODS_DRAFT` §2.12.10 depends on it. Retired only so
that no result is computed *on* them by accident.

✅ Checked: `grouping_test_bp.py` does **not** read any `SCALE_*` file, and the
granularity ladder reproduces exactly after retirement (Asia/non-Asia κ=1.000,
hemisphere κ=0.901, region κ=0.890, SEA κ=0.425). The ladder is
partition-independent and safe.

## `superseded_partitions/` — 32 files

`curated_L1_*`, `curated_L1v2_*`, `curated_L1v3_*`, `curated_L1v4_*`,
`curated_L1v4b_*`, and the v3/v4 metadata tables.

Five partition generations preceding v4c. **Unit labels collide across
generations** — `strain_1_L1_36` denotes different genome sets in different
generations — so joining any of these by unit name to current results silently
produces nonsense.

## `superseded_rm/` — 2 files

`RM_RESULTS_CONSOLIDATED.tsv` and `RM_RESULTS_L1_CLEAN_CORRECTED.tsv`. Pre-v4c
r/m tables. The frozen-basis r/m is
`L1v4c_out/Summaries/recombination_rm.tsv` (85 units).

## `superseded_handoffs/` — 3 files

`HANDOFF_2026-08-21_SESSION_END.md`, `HANDOFF_PHYLOGEOGRAPHY_2026-08-19.md`,
`HANDOFF_research_gaps.md`. Superseded by `HANDOFF_2026-08-21_NIGHT.md`.

## `backups/` — 22 files

`*.bak`, `*.pre-*`, `*.orig` snapshots taken before in-place edits. Kept because
several are the only record of a pre-correction state — e.g.
`recombination_rm.tsv.pre-rederive-2026-08-21.bak` and
`NU_HYPOTHESIS.tsv.pre-frozen-basis.bak`.

---

## Left in the workspace deliberately — 16 files

These are superseded **but still referenced by a script that is still present**,
so moving them would break it. They are listed here so their status is not
mistaken:

`curated_L1_clusters.tsv`, `curated_L1_overrides.config`,
`curated_L1_ref_alternates.tsv`, `curated_L1_reference_audit.tsv`,
`curated_L1_reference_selection.tsv`, `curated_L1_refs.tsv`,
`curated_L1_refs_normalized.tsv`, `curated_L1v4b_clusters.tsv`,
`curated_L1v4b_refs.tsv`, `L1v3_ASSIGNMENTS.tsv`,
`L1v3_PHYLOGEOGRAPHY_ASSOCIATION.tsv`, `L1v4b_MERGED_METADATA.tsv`,
`RM_RESULTS_L1.tsv`, `RM_RESULTS_L1_CORRECTED.tsv`,
`HANDOFF_2026-08-21_EVENING.md`, `REVISED_STRATEGY_2026-08.md`.

Their referencing scripts (`build_v4c_panel.py`, `merge_L1_refs_bp.py`,
`consolidate_L1_rm_bp.py`, `export_deliverables_bp.sh`,
`run_wf_curated_L1v4c.sh` and others) are provenance for how the current basis
was built. **Retiring the scripts and their inputs together is a second pass, not
this one** — `run_wf_curated_L1v4c.sh` in particular is the production command
line the Methods must pin.

`RM_RESULTS_L1_CORRECTED.tsv` deserves a specific warning: it is an **82-unit
pre-v4c table** whose `strain_1_L1_10` has n=21 against the frozen basis's
dropped 7. It is not the v4c r/m table and must never be read as one.

---

## Verified after retirement

`freeze_basis_bp.py` (12/12 PASS), `generate_numbers.py` (units 85, r/m 7.70),
`score_accessory_bp.py --validate` (PASS), `nu_hypothesis_bp.py` (170
replicon-units). Nothing in the current analysis path depends on a retired file.

---

## `run_logs/` (59) and `intermediates/` (86) — added in the stage-1 tidy

Unreachable `.log`, `.csv` and `.txt` files: not referenced by any script in the
deliverable closure, and not cited by any document in the workspace.

**Method, and why it is a whitelist.** The keep-set was derived from the
deliverable-producing scripts (`generate_numbers.py`, `freeze_basis_bp.py`, the
scorers, the validators) by transitive file-reference closure, then anything
outside it moved. A blacklist — hunting for dead files — fails open: whatever you
fail to prove dead stays, and the clutter returns. A whitelist fails closed, and
since nothing is deleted a wrong call costs one `mv`.

**Three files were held back** because a document cites them even though no
script does: `N2_run.log`, `SRA_accessions.txt`, `V4C_STATUS.txt`.

**Verified after the move**, which is the actual guarantee — not the dependency
graph: `freeze_basis_bp.py` BASIS IS CONSISTENT, `generate_numbers.py` 40 keys,
`score_accessory_bp.py --validate` PASS, `concordance_frozen_bp.py` +0.8614
unchanged.

⚠ **Reachability does not work for prose.** Scripts never cite documents, so
every current write-up — `DOWNSTREAM_IMPACT_2026-08-22.md`,
`HANDOFF_2026-08-21_NIGHT.md`, the result docs — is "unreachable" and must never
be moved on that basis. Document triage is editorial and separate.

---

## `legacy_tables/` (92) — the stage-2 tidy

Unreachable `.tsv`: outside the deliverable closure and cited by no document.
Nine candidates were held back because a document cites them.

### ⚠ A near-miss, recorded because the rule it produced matters

Stage 2 initially moved **15 scripts** as well, and every one of them was
**tracked by git**. Among them: `run_wf_curated_L1v4c.sh` — the production
command line this very README says must be kept so the Methods can pin it — plus
`core_shrinkage_test.sh` and `make_itol_annotations.py`, which are the named
feature of the branch this work sits on. They were caught by reading `git status`
before committing, and all 15 were restored.

**The rule that follows, and it is not negotiable: never retire a git-tracked
file on the strength of a reachability test.**

The reasoning is that this repo's `.gitignore` is **deny-by-default** — a file is
tracked only because someone explicitly admitted it. Tracked status *is* a
recorded keep decision, made by a human, and it outranks any graph I can compute.
The closure test answers "does the analysis chain read this?", which is simply a
different question from "is this worth keeping": launcher scripts, run drivers
and provenance are deliverables that no analysis script ever reads.

`legacy_scripts/` is empty and left in place as a marker.

**Verified by execution afterwards — every current analysis script re-run:**

| script | result |
|---|---|
| `freeze_basis_bp.py` | BASIS IS CONSISTENT |
| `generate_numbers.py` | `rm.median_gate1` 7.70 |
| `score_accessory_bp.py --validate` | PASS — scorers like-for-like |
| `concordance_frozen_bp.py` | +0.8614 |
| `nu_hypothesis_bp.py` | 170 replicon-units |
| `grouping_test_bp.py` | Asia vs non-Asia 100% |
| `gate1_from_alignment_bp.py` | 85 units |

Every headline number reproduces unchanged. **That, not the dependency graph, is
the evidence the keep-set is sufficient** — the closure test matches literal
filenames and would miss an input reached by glob, which is exactly how
`DISTANCES_v4c_SUMMARY.tsv` came to be built from a hybrid directory.

**Kept deliberately:** `GAP1`–`GAP4` stay at top level — still live input to the
paper's positioning, and `GAP4` carries part of the citation-audit trail.

## Not here: `collaborator/`

The Yuyi / A100 materials were moved to **`collaborator/`**, not retired. They
carry a **live recall condition** — Yuyi did not finish on 2026-08-21 and results
may land next week. See `collaborator/README.md`. Nothing in the current analysis
is blocked on them.
