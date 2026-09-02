# Collaborator materials — Yuyi / A100

Moved out of the immediate workspace 2026-08-22. **Not retired — parked.**

| file | what |
|---|---|
| `A100_QUICKCARD.md` | one-page operating card for the DGX A100 |
| `A100_RUNBOOK_YUYI.md` | full runbook, English |
| `A100_RUNBOOK_YUYI_TH.md` | full runbook, Thai |
| `EXPLAINER_FOR_YUYI_EN_TH.md` | conceptual explainer, EN + TH |
| `HANDOFF_A100_2026-08-19.md` | the 2026-08-19 A100 handoff |

## ⚠ Recall condition — live, not historical

**Yuyi did not finish on Friday (2026-08-21).** If her results land next week,
these documents are the operating context for interpreting them and should come
back to the top level.

**But the current analysis does not depend on them.** The frozen basis
(`FINAL_BASIS_2026-08-22/`, 85 units) is the corrected *workstation* partition;
the A100 run is the cross-hardware reproducibility control, and the comparison
that matters — 0.46% median relative r/m across the 82 shared units — is already
computed and recorded in `METHODS_DRAFT` §2.12.10 and
`rm_provenance/A100_recombination_rm.tsv`. Nothing is blocked on Yuyi's return.

**If her results do arrive**, the thing to check is *not* whether they change the
reported numbers — they cannot, the basis is frozen — but whether they extend the
reproducibility control to units it does not currently cover, and whether the two
A100-only units (`strain_1_L1_36`, `strain_1_L1_37`) finally arrive with the
`.core.full.aln` files that were never transferred. Those alignments are the one
thing that would let the A100 partition be corrected and re-derived locally, and
their absence is a stated reason the workstation partition was chosen as the
basis (`FINAL_BASIS_2026-08-22/README.md` §2).

Note the rclone remote is `peerah-gdrive:` here and `gdrive_ph:` in the runbooks —
same Drive, different machine name.
