# The production/control redesignation was applied in three places out of six

2026-08-23, evening session. **No reported number changes.** What changes is
which run several documents attribute a number to — and in one case, which number
a reader is told to put in the paper.

---

## 1. What happened

At some point the two runs swapped roles:

| | run | designation **before** | designation **now** |
|---|---|---|---|
| 22-core workstation, 62 GB | 85 units, 2,340 genomes | control | **reported** |
| NVIDIA DGX Station A100 | 88 units, 2,342 genomes | production | **control** |

The flip was applied to the `METHODS_DRAFT` §2.12 preamble, to §2.12.13, and to
`FINAL_BASIS_2026-08-22/README.md`. **It was not applied to the documents those
sections depend on**, so four artifacts continued to describe the A100 run as
production. Because both runs are real and their numbers are close, the stale
labels do not read as errors — they read as slightly different measurements.

This is the same failure mode as the partial-denominator and hybrid-directory
traps already on record: a correction applied at the point of use rather than at
the source, leaving the source to re-infect the next reader.

## 2. The worst instance

`GATE1_ALIGNMENT_RESULT_2026-08-21.md` opened with a callout box reading, in
bold, **"Which number goes in the paper: 7.44."** That is the control run's
figure. The frozen headline is **7.70**. A reader following that document
top-down would have taken the wrong r/m into the manuscript, and the two are
close enough (3.5%) that nothing downstream would have flagged it.

## 3. The four r/m values, verified

All four recomputed from the frozen artifacts on 2026-08-23. They are the two
partitions crossed with the two ways of measuring unit diversity:

| median r/m (n in-window) | Mash proxy | alignment-derived |
|---|---|---|
| **reported run** (workstation, 85 units) | 7.26 (47) | **7.70 (47)** |
| control run (A100, 88 units) | 7.38 (47) | 7.44 (48) |

Sources: reported from `DISTANCES_v4c_SUMMARY.tsv` joined to
`L1v4c_out/Summaries/recombination_rm.tsv`; control from
`RETIRED_2026-08-22/a100_control/GATE1_ALIGNMENT_A100_2026-08-21.tsv`, whose
`gate1_alignment` and `gate1_mash` columns give the two bases directly. Window
[700, 4700] mean pairwise core SNPs in both cases.

**`generate_numbers.py` was right all along** and needs no change. It joins
`DISTANCES_v4c_SUMMARY.tsv` by unit name, which §7b warned against — but that
warning was aimed at the *control* partition under the old labels. The reported
r/m table carries only the 85 reported units, so the three control-only rows
(`strain_1_L1_10`, `_36`, `_37`) drop out on the join and the remaining rows
carry reported membership. Confirmed by recomputing with the universe restricted
to `FINAL_PARTITION.tsv`: 47 units, median 7.70, identical.

## 4. Two further errors found in the same paragraph

`METHODS_DRAFT` §2.12.10, while being relabelled:

- **The unsplit `strain_1_L1_26` was given r/m 3.10. Its value is 4.47.**
  3.1042 is the stale denormalised `unit_rm` copy from
  `L1v4c_MERGED_METADATA.tsv` — the exact value `generate_numbers.py` names in
  its own source comment as the reason not to read that column. The authoritative
  `recombination_rm.tsv` gives **4.4713** for n = 153.
- **`strain_1_L1_36`'s mean pairwise distance was given as 1,126.** That figure
  appears nowhere else in the corpus and is not reproducible from any artifact.
  On the alignment basis — the same basis as the Gate 1 floor it is being
  compared against — it is **1,477** (756.2 + 720.8 across replicons). Corrected.

Neither changes the argument: the n = 98 child is still a clonal expansion an
order of magnitude below the floor, and `_36` is still comfortably in-window.

## 5. Files corrected

| file | change |
|---|---|
| `METHODS_DRAFT_2026-08-19.md` §2.12.10 | run labels reversed; r/m 3.10 → **4.47**; `_36` diversity 1,126 → **1,477**; the join warning re-aimed at the control |
| `METHODS_DRAFT_2026-08-19.md` §2.12.7 | "three r/m values" → the **2×2 table**; panel 2,976 → 2,959 in the revision note |
| `METHODS_DRAFT_2026-08-19.md` header | revision note rewritten onto the frozen basis |
| `GATE1_ALIGNMENT_RESULT_2026-08-21.md` | opening box reversed (**7.44 → 7.70**); §7b relabelled; **§7c added** with the 2×2 |
| `PHYLOGEOGRAPHY_ASSOCIATION_INTERPRETATION.md` | superseded-banner: A100 is the control, and R6 was re-run on the frozen basis (sub-national **1 of 81**) |
| `GENOME_REGISTER_2026-08-21.md` | analysed-subsets table gains a reported row; A100 relabelled control; 2,352 marked a pre-correction intermediate |

`HANDOFF_2026-08-23.md` (morning) also carries the old labels and is left alone:
it is superseded by the evening handoff and is dated as such.

## 6. Rule to carry forward

**When a designation flips, grep the corpus for the old one before considering it
done.** The flip touched three files; six needed it. The tell is that a stale
run label produces a *plausible* number rather than an absurd one, so none of the
existing consistency checks — `freeze_basis_bp.py` included — can catch it.
`freeze_basis_bp.py` validates the basis, not the prose that describes it.

## 7. Reproduce

```bash
python3 generate_numbers.py && python3 freeze_basis_bp.py
```

Both unchanged by this correction: 15/15 checks pass, `rm.gate1_units` 47,
`rm.median_gate1` 7.70.
