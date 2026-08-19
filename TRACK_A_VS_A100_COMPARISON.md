# Track A (workstation) vs A100 — v4c run comparison

Written 2026-08-19 from the RTX 4070 workstation. Companion to
`READ_ME_FIRST_2026-08-19.md`, `SESSION_NARRATIVE_2026-08-19.md` and
`METHODS_DELTA_2026-08-19.md` in this folder.

This answers item 1 of "What needs you": Track A's summaries are now on Drive
under `trackA_workstation/Summaries/`, and this note reports the comparison they
make possible.

---

## The two runs

| | Track A (workstation) | A100 |
|---|---|---|
| partition | `curated_L1v4c_refs.tsv` (86 units) | `curated_L1v4c_refs.final.tsv` (88 units) |
| analysed genomes | 2,352 | 2,342 |
| replicon-units | 172 | 176 |
| started / finished | 2026-08-18 19:52 → 2026-08-19 07:59 (13h07m) | → 2026-08-19 15:11:55 |
| nextflow session | `c90e1105-5b12-455e-9b31-4ecde888d559` | `13721732-3288-434b-bd23-4cab6f54dd6d` |
| hardware | RTX 4070 workstation, 22 cores / 62 GB | A100 box, 128 cores / 503 GB |

**Both completed clean.** Track A: 8,178 tasks COMPLETED, 0 failures, 172/172
replicon-units `gubbins_status=completed` / `exit 0` / `Tier1_high_confidence`.
A100: 88/88 units, 176/176 replicon-units, same all-Tier1 result. Neither run had
a single bad-reference or model-fit failure — the v4b-era expectation that ~2
untested references would fail did not materialise in either.

---

## The comparison is valid — 82 untouched units prove it

82 units have identical membership in both runs. Across those:

    median |Δ r/m|  = 0.0145   (0.38% relative)
    max    |Δ r/m|  = 1.32     (strain_5_L1_6, n=16: 7.35 vs 6.03)

Two independent runs, different hardware, different overrides config, agreeing to
~0.4% on the median unit. This is the empirical answer to the concern raised in
the A100 handoff that unpinned Gubbins parameters would make the two runs
non-comparable (memory `gubbins-params-shift-rm-nonuniformly`): **they are
comparable.** Differences in the changed units below are signal, not noise.

The two units the A100 deliberately left alone as controls reproduce almost
exactly: `strain_1_L1_35` 1.32 vs 1.31, `strain_4_L1_3` 0.75 vs 0.75.

---

## The decisive test — the r/m rationale for splitting is not supported

`READ_ME_FIRST` §3 states the test: "The decisive comparison is still Track A's
r/m for the *unsplit* `strain_1_L1_26`", with the prediction that the pre-split
lump should show **elevated** r/m. Track A's value:

| | n | r/m (corrected) |
|---|---|---|
| **unsplit parent — Track A** | 154 | **3.10** |
| child `strain_1_L1_26` — A100 | 98 | 1.07 |
| child `strain_1_L1_36` — A100 | 47 | **6.68** |
| child `strain_1_L1_37` — A100 | 8 | 2.63 |

**3.10 is not elevated.** Track A's median is 5.34 (p25 2.03, p75 8.27), so the
lump sits *below* the median, around the 40th percentile. And:

- the n-weighted mean of the three children is **2.87** — only **7% below** the
  parent's 3.10, not the step change un-lumping predicts;
- one child (`strain_1_L1_36`, n=47) is **2.2x the parent**.

Two other interventions point the same way, and one supports it:

| unit | Track A | A100 | direction |
|---|---|---|---|
| `strain_1_L1_22` | n=34, r/m 4.12 | n=32, r/m **7.21** | trimming 2 genomes nearly doubled r/m |
| `strain_1_L1_11` | n=24, r/m 2.04 | n=18, r/m 1.60 | as intended |
| `strain_27_L1_1` | n=11, r/m 0.33 | n=10, r/m 0.21 | as intended (ONT drop) |
| overall median | 5.34 (86 units) | 5.70 (88 units) | rose, not fell |

**What this does and does not mean.** It does **not** show the split was wrong.
The modality evidence is structural and independent of r/m — three clonal groups
at 0.00007 internal separation against 0.00088/0.00134 between them is a real
population-structure finding, and analysing genuinely separate populations as one
unit is objectionable whatever r/m does. The split also *revealed* 6.2x
heterogeneity among the children (1.07 to 6.68) that the lump was averaging away;
surfacing that is a substantive gain.

What it means is narrower and specific: **the r/m-inflation argument should not be
used to justify the split in the write-up**, because the numbers do not carry it.
`METHODS_DELTA_2026-08-19.md` should be revised accordingly before merging — the
defensible claim is modality/population structure, not recombination inflation.

Relatedly, `READ_ME_FIRST` §3 says "Every unit the distance analysis pointed at
came back at or below the 25th percentile." That holds among the A100's own
post-split values, but it is not evidence the split helped: against the Track A
baseline, `strain_1_L1_22` moved the wrong way and the parent of the main split
was already below median.

---

## Genome accounting — fully reconciled

Track A 2,352 → A100 2,342 analysed genomes, difference −10:

    −1   SRR28096039 dropped from strain_27_L1_1 (ONT, gene-count ratio 1.08)
    −6   strain_1_L1_11 trimmed 24 → 18
    −2   strain_1_L1_22 trimmed 34 → 32
    −1   strain_1_L1_26 split 154 → 98 + 47 + 8 = 153
    ---
    −10

On the ONT pair: `SRR28096039` (ratio 1.08, the batch maximum) was dropped;
`SRR28096043` (1.06) was kept and flagged. Both sat in `strain_27_L1_1`. The
outstanding check in `READ_ME_FIRST` §6.3 — tip branch length for `SRR28096043`,
dropping to n=9 if long — is still open and unaffected by this comparison.

---

## Correction: the re-fit premise in my A100 handoff was wrong

`HANDOFF_A100_2026-08-19.md` argued for a fresh PopPUNK re-fit on the grounds
that "strain_4 collapsed 14 → 4". The A100 session rejected that, and it was
right. Verified here against the membership files:

    v4b strain_4 : 261 genomes
    v4c strain_4 : 104 genomes
    overlap      : 0
    all 261 v4b strain_4 genomes are in v4c strain_1

The strain labels name **different populations** across two different fits, so
there was no "14" to recover — the comparison was invalid. This is precisely the
trap memory `l1-label-transfer-is-validated` exists to prevent, and the handoff
did not apply it. The A100's other two grounds also hold: v4c's fit was computed
on the v4c panel (2,976 genomes, `refined_clusters_reconciled.csv`), not carried
over from v4b; and PopPUNK bgmm at fixed K is deterministic per input with no
exposed seed, so re-running it on the same database reproduces the same partition
exactly. **The re-fit would have consumed the day and changed nothing.**
Substituting the modality analysis was the better experiment.

---

## Which run to use

**The A100 run (88 units) is the better result** and should be the one carried
forward: it is built on the same verified 2,976-genome panel, it removes a
genuine ONT quality risk, and its unit boundaries respect population structure
that Track A's do not. Track A's value now is as the **control** — it is what
makes the numbers above measurable, and it should be retained, not discarded.

Two things to fix in the write-up before it goes further:

1. drop the r/m-inflation justification for the splits (use modality);
2. `strain_1_L1_22` went 4.12 → 7.21 on a 2-genome trim — worth understanding
   before that trim is defended in print.

Standing caveats unchanged: the parsnp backbone graft mixes branch-length units,
so the grafted global tree must not be dated; and r/m at the high end is
dominated by units with borrowed distant references (`Reference` in
`dropped_branches` for all of the top eight), per `rm-is-deflated-beyond-mash-0002`.

---

## Files pushed alongside this note

`trackA_workstation/Summaries/` — from the workstation's `L1v4c_out/`:

    cluster_phylogeny_summary.csv   172 rows, per replicon-unit status + tier
    recombination_rm.tsv             86 rows, rm_corrected / rm_uncorrected
    cluster_sizes.tsv
    cluster_membership.tsv
    Summary.QC_File_Checks.tsv

`trackA_workstation/pipeline_info/execution_trace_*.txt` — the full task ledger
(8,178 rows) the completion claims above are verified from.

---

## Addendum 2026-08-19 — why the parent was not "elevated"

`FINDINGS_2026-08-19_workstation.md` §3 resolves the open question above. Applying
the draft's Gate 1 (§2.6.1, usable window 1,270-4,671 mean pairwise core SNPs) to
both partitions:

    before  strain_1_L1_26  n=154  ~3,421 SNPs  r/m 3.10   IN-WINDOW  (valid)
    after   strain_1_L1_26  n= 98  ~  955 SNPs  r/m 1.07   below floor (invalid)
            strain_1_L1_36  n= 47  ~3,374 SNPs  r/m 6.68   in-window  (valid)
            strain_1_L1_37  n=  8  ~  229 SNPs  r/m 2.63   below floor (invalid)

The pre-split parent was not elevated because it was a **valid in-window
measurement all along**. Only 47 of the 88 final units are in-window; the
defensible summary statistic is the **in-window median r/m = 7.38**, not 5.70.
A low r/m is a detection failure, not a clean unit.
