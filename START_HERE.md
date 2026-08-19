# START HERE — read order for this folder

Last updated 2026-08-19 17:10 +07, from the workstation.

This folder accumulated documents from three sessions across two machines on the
same day. **Several supersede each other, and two contain conclusions that later
measurement refuted.** Read in this order; the supersession table below says
which parts of the older documents no longer stand.

---

## Read in this order

| # | document | what it is |
|---|---|---|
| 1 | **`READ_ME_FIRST_2026-08-19.md`** | what the A100 did and what state it left things in. **Read §3 with the correction in #3 below.** |
| 2 | **`FINDINGS_2026-08-19_workstation.md`** | the two open items closed (ONT drop, maxForks), **plus the diversity-window finding that changes how every r/m number reads** |
| 3 | **`TRACK_A_VS_A100_COMPARISON.md`** | the two runs compared; what refinement actually did |
| 4 | **`METHODS_DRAFT_2026-08-19.md`** | **the current methods document.** §2.12 rewritten in full. This is what goes to the manuscript |
| 5 | `EXPLAINER_FOR_YUYI_EN_TH.md` | the whole project start-to-finish, EN + TH, non-specialist |
| 6 | `SESSION_NARRATIVE_2026-08-19.md`, `A100_SESSION_2026-08-19.md` | the A100 session's reasoning, for provenance |

Data: `snp/Summaries/` (A100 production, 88 units) and
`trackA_workstation/Summaries/` (workstation control, 86 units).

---

## Superseded — do not act on these

| document | status |
|---|---|
| **`METHODS_DELTA_2026-08-19.md`** | **fully merged into `METHODS_DRAFT_2026-08-19.md`.** Do not merge it again. Its §5 rationale ("a unit that fuses two sub-populations inflates its r/m") **was not supported** when tested — see #2/#3 above |
| **`a100_handoff_2026-08-19/HANDOFF_A100_2026-08-19.md`** | its central recommendation — **re-fit PopPUNK** — **was wrong and was correctly rejected on the A100.** See the banner inside that file |
| `HANDOVER.md` | pre-dates the run; kept for provenance only |
| `L1V4C_RESULTS_SUMMARY.txt` | written by the collector before it was fixed; trust `snp/Summaries/` instead |
| `fix_and_run_v4c.sh` | its job is done — the CRLF and SIGPIPE bugs are fixed in the repo (PR #5) |

---

## The three things that changed after those documents were written

**1. r/m is valid for only 47 of the 88 units — quote 7.38, not 5.70.**
Gubbins only measures recombination inside a diversity window
(≈1,270–4,671 mean pairwise core SNPs). Outside it, in **either** direction, the
estimate is a detection failure rather than a measurement:

| Gate 1 class | units | median r/m |
|---|---|---|
| **in-window** | **47** | **7.38** |
| below floor | 9 | 1.67 |
| above ceiling | 32 | 2.48 |

**A low r/m is not a clean unit.** `READ_ME_FIRST` §3 reads `strain_1_L1_35`
(1.31) and `strain_4_L1_3` (0.75) as evidence the decision not to split them was
right; they are in fact **1.9× and 2.8× above the ceiling**. Leaving them intact
was still correct — they are unimodal — but not for that reason, and those
values should not be quoted.

**2. The split did not do what it was expected to do.** The pre-split
`strain_1_L1_26` measured **3.10 and was in-window** — a valid measurement, not
an inflated one. Its children: 1.07 (below floor), **6.68 (in-window)**, 2.63
(below floor). Report `strain_1_L1_36` as the recombination result and the other
two as identified clonal expansions **with no r/m**. The split is defensible on
population structure; the r/m argument for it is not.

**3. Both ONT genomes are out.** `SRR28096043`'s terminal branch is **38–59×
the longest Illumina branch in its own unit** — same soil, same batch, same
reference, only the platform differs. BUSCO agreed independently. `n` falls to 9,
still above the gate.

---

## Still open — your call

- **`maxForks` 40 → 48**, not 59. 59 consumes the entire 118-cpu budget and
  leaves zero cores for an 8-cpu Gubbins task. Change it **between** runs.
- **PR #5** on `wf-assembly-snps-mod` — the CRLF and SIGPIPE fixes. One task
  re-runs on resume (~7 min); nothing touches snippy, Gubbins or IQ-TREE.
- **Analysis code is now on GitHub**, private:
  `PHemarajata/bp-recombination-aware-snps`. No isolate data is tracked.

---

## The rule that produced all three corrections

**Check per-item values; never infer from a summary line.** Every defect here
produced plausible output — a CRLF terminator that made a run report success
while doing nothing, a RAxML crash surfacing as "Unable to fit model to data",
ONT assemblies passing every automated gate, and a low r/m that reads as a clean
result and usually means the measurement failed.
