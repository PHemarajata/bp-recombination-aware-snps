# What moved to TB1, and what was deleted — 2026-08-21

Local disk was at **95% (91 GB free)**. After this pass: **~404 GB free**.
TB1 (`/media/phemarajata/TB1`, 916 GB) went from 172 GB used to ~241 GB.

Every archive step copied, verified **both** the file list and the total byte
count, and only then removed the local copy — see `archive_to_tb1.sh`. Nothing
was moved with `mv`, which across filesystems is a non-atomic copy-then-delete
and can lose data if interrupted.

---

## Deleted outright (not archived)

| what | size | why it was safe |
|---|---|---|
| `L1v4c_work/` | **232 GB** | Nextflow work dir of the completed v4c Track A run. Checked before deleting: run ended 8,178 tasks COMPLETED / 0 FAILED; every published output in `L1v4c_out/` is a **real file, not a symlink** (0 symlinks among 1,928 files); no process held it open; no Nextflow session state pointed at it. |
| `L1_clean_out/` | 15 GB | Already on TB1 at `snp_archive/L1_clean_out`. The archived copy was missing 12 files (global tree outputs + `pipeline_info` run records); those were synced first, then verified byte-for-byte identical (15,982,054,841 bytes both sides) before the local copy was removed. |
| `__pycache__/` | 1 MB | regenerable |

**The symlink check on `L1v4c_work` was the one that mattered.** Nextflow's
`publishDir` frequently publishes by symlinking into the work directory; had it
done so here, deleting the work dir would have destroyed the published results
rather than freeing space.

---

## Archived to `TB1/snp_superseded/`

Superseded partition generations. Kept because they are the provenance for
figures and numbers already quoted in the drafts.

| directory | bytes verified |
|---|---|
| `L1v3_out/` | 17,610,007,837 |
| `L1v4b_out/` | 17,840,912,263 |
| `L1v4b_partition/` | 12,049,841,319 |
| `L1v4_partition/` | 2,129,469,504 |

Joins the existing `all35_out/` and `pp2802_out/` already there.

## Archived to `TB1/snp_archive/`

Completed sensitivity experiments — run, reported, not expected to be re-run.

| directory | bytes verified |
|---|---|
| `null_sim/` | 11,111,753,103 |
| `fconst_sensitivity/` | 7,030,888,739 |
| `spikein/` | 1,898,804,315 |
| `refsens_cluster37/` | 3,380,463,030 |

Joins the existing `L1_clean_out/` and `snp_results_2026-08-16_v3/`.

**Scripts referencing these paths will no longer resolve** —
`null_simulation_bp.py`, `spikein_sensitivity_bp.py`,
`reference_sensitivity_bp.py`, `constant_sites_sensitivity_bp.py` and a few
others. They are re-pointable at
`/media/phemarajata/TB1/snp_archive/<dir>` if any needs re-running.

---

## Considered and deliberately KEPT

| what | size | why |
|---|---|---|
| `v4c_local/fasta/` | 21 GB | Looks like a pure duplicate — 2,970 of 2,976 files match a copy elsewhere by size. **It is not.** All 86 reference paths in `curated_L1v4c_refs.tsv` point into it, and **6 files exist nowhere else**: `GCF_015714675_1_Virgin_Islands_St__John`, `SRR28096032`, `SRR28096039`, `SRR28096043`, `SRR28096062`, `SRR30648682` — three of which are the SKESA-override assemblies from `PANEL_ASSEMBLY_OVERRIDES.tsv`. |
| `L1_out/` | 15 GB | Referenced by 8 scripts, and it is the generation the root-level `RM_RESULTS_L1*.tsv` files describe. |
| `prod_*/arms/` | ~10 GB | The alignments behind the published 46-unit Gubbins-vs-ClonalFrameML concordance result. `clonalframe_nu_bp.py --layout arms` still reads them. |
| `a100_stage/` | 6.4 GB | Staging bundle; small, and re-staging is more work than the space is worth. |
| `additions/fasta_spades/` | 2.7 GB | Live input — the cgMLST genome symlinks resolve here. |
| `cgmlst_scheme/`, `cgmlst_results/` | ~11 GB | Active work. |
| `*.bak` from 2026-08-20 | <1 MB | Rollback for that day's metadata and association-table edits. |

---

## Restoring anything

```bash
rsync -a /media/phemarajata/TB1/snp_superseded/L1v4b_out/ ./L1v4b_out/
```

TB1 is the **only** copy of everything listed above. It is not backed up
elsewhere.
