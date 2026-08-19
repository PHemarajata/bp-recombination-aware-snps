# Three findings from the workstation, 2026-08-19

Closes the two open items in `READ_ME_FIRST_2026-08-19.md` §6 (the `SRR28096043`
tip check and the `maxForks` change), and reports a third finding that emerged
from doing them: **the r/m values in this run are only interpretable for 47 of
the 88 units**, and two of the interpretations in `READ_ME_FIRST` §3 are inverted
by the project's own calibration.

Companion to `TRACK_A_VS_A100_COMPARISON.md`. All numbers measured here, not
carried over.

---

## 1. `SRR28096043` — the tip-branch check says drop it

Track A is the better tree for this because it still contains **both** ONT
genomes. `strain_27_L1_1` is a near-controlled experiment: 10 isolates, all Ghana
Ashanti environmental soil, same batch, same reference — 8 Illumina, 2 ONT.

Terminal branch lengths from `<unit>.final.treefile`:

| tip | replicon 1 | replicon 2 |
|---|---|---|
| `SRR28096039` (ONT, gene-ratio 1.08) | 0.11838 | 0.15568 |
| **`SRR28096043` (ONT, gene-ratio 1.06)** | **0.05415** | **0.08450** |
| longest Illumina tip in the same unit | 0.00142 | 0.00144 |
| Illumina median | 0.00056 | 0.00077 |

`SRR28096043`'s terminal branch is **38–59x the longest Illumina tip** in its own
unit and **97–109x the unit median**. Every Illumina member falls between 0.4x
and 2.5x the median. The criterion in `READ_ME_FIRST` §6.3 is met without
ambiguity: **drop it** (n falls to 9, still above the n>=7 gate).

This independently confirms the A100's BUSCO result (`SRR28096043` 654 complete /
22 fragmented / 12 missing, against 688/0/0 for contiguity-matched complete
genomes) by a completely different route — tree geometry rather than gene content.
Two lines of evidence, same conclusion.

**Two consequences beyond this genome:**

- **The gene-count ratio works as a screen.** The only two isolates in the unit
  with ratio > 1.0 are exactly the two with catastrophic terminal branches; the
  eight at 0.90–0.97 all produced normal ones.
- **The <=1.20 gate is too loose.** A ratio of **1.06** was enough to produce a
  40–60x inflated branch. The gate was calibrated on PacBio CLR failures at
  >=1.35. These two isolates were the top 2 of 171 in their batch (median 0.97,
  p90 0.99), so the discriminating signal was their **rank within the batch**, not
  their absolute value. Recommend an outlier test against the batch, as
  `METHODS_DELTA` §3 already proposes via BUSCO for <=5-contig assemblies.

## 2. `maxForks` 40 -> 59 — diagnosis confirmed, but 59 is too aggressive

Measured from the A100 execution trace (`execution_trace_2026-08-19_11-49-18.txt`,
8,174 tasks):

| process | tasks | max concurrency | mean parallelism |
|---|---|---|---|
| **SNIPPY_SCATTER** | 4,684 | **40 (= its maxForks)** | **38.9** |
| GUBBINS_CLUSTER | 176 | 13 | 3.6 |
| IQTREE_ASC | 176 | 5 | 0.4 |

**Confirmed: SNIPPY_SCATTER was fork-bound, not CPU-bound** — it sat at 38.9 of
its 40 slots for essentially the whole stage. It is also the only stage whose
maxForks binds before the executor budget:

| process | cpus | maxForks | cpu when saturated | of 118 |
|---|---|---|---|---|
| **SNIPPY_SCATTER** | 2 | 40 | **80** | leaves 38 idle |
| GUBBINS_CLUSTER | 8 | 14 | 112 | ~budget |
| IQTREE_ASC | 8 | 10 | 80 | — |

**Where 59 comes from: 118 / 2 = 59** — snippy alone consuming the entire
executor budget. That matches the config's stated philosophy ("maxForks
generously; the executor budget is the real cap"), and snippy is the one stage
violating it.

**The problem with 59:** GUBBINS ran at mean parallelism 3.6 of 14 — input-starved,
waiting on mapping, but still overlapping. At 59 forks snippy leaves **0 cores**
for an 8-cpu Gubbins task while saturated, converting a pipelined run into a
phased one and starving the superlinear stage you most want overlapped.

| forks | snippy cpu | left | concurrent Gubbins | snippy wall |
|---|---|---|---|---|
| 40 (current) | 80 | 38 | 4 | 2.84 h |
| **48 (suggested)** | 96 | 22 | 2 | 2.30 h |
| 59 | 118 | 0 | **0** | 1.87 h |

Total CPU is ~305 core-hours, so the floor at 118 cores is **2.59 h** against
3.31 h observed — only ~0.7 h is available to win regardless.

**Recommend 48.** It captures most of the mapping speedup while keeping two
Gubbins slots always live. Then check `GUBBINS_CLUSTER` mean parallelism on the
next run: if it holds at ~3.6 or better, push higher; if it drops, the crowding
is real and you have measured it. Change it **between** runs — editing the config
mid-run invalidates the task hashes and the resume cache.

---

## 3. The finding that matters most: r/m is valid for only 47 of the 88 units

`METHODS_DELTA_2026-08-19.md` opens by noting "the methods document is not on the
A100 or in any Drive bundle; it is on the workstation." That document
(`METHODS_DRAFT_2026-08-11.md`, §2.6) contains this project's **calibrated
operating range for Gubbins**, and it was therefore not available when the unit
refinement was designed. Applying it now changes how several numbers should be
read.

**Gate 1 (§2.6.1): units must fall in ~1,270–4,671 mean pairwise core SNPs.**
Outside it, r/m is not a measurement. Below the floor Gubbins cannot detect
recombination at all; above the ceiling the estimate collapses (the draft records
r/m 0.16–1.73 for above-ceiling clusters).

Running the project's own `cluster_diversity_bp.py` on the final 88 units against
`mash_named.phylip`:

| Gate 1 class | units | median r/m |
|---|---|---|
| **in-window** | **47** | **7.38** |
| below floor | 9 | 1.67 |
| above ceiling | 32 | 2.48 |

The calibration reproduces exactly: **r/m is high only inside the window and
collapses at both extremes.** So:

> **Quote the in-window median, 7.38 (n = 47).** Not the all-unit median (5.70),
> and not the raw range. **A low r/m is a detection failure, not a clean unit.**

### This inverts two readings in `READ_ME_FIRST` §3

That section cites `strain_1_L1_35` (r/m 1.31) and `strain_4_L1_3` (r/m 0.75) as
evidence that declining to split them was correct — "among the lowest in the run".
Measured:

| unit | ~mean pairwise SNPs | vs ceiling | r/m |
|---|---|---|---|
| `strain_1_L1_35` | 9,042 | **1.9x above** | 1.31 |
| `strain_4_L1_3` | 13,099 | **2.8x above** | 0.75 |

Their low r/m is the documented above-ceiling collapse (0.16–1.73), not a clean
signal. **Leaving them unsplit may well still be right** — they are unimodal, and
that is a sound structural reason — but not for the reason given, and their r/m
values should not be quoted at all.

### The `strain_1_L1_26` split, measured against Gate 1

| | n | ~mean pairwise SNPs | r/m | Gate 1 |
|---|---|---|---|---|
| **before** | 154 | 3,421 | 3.10 | **in-window — valid** |
| after `strain_1_L1_26` | 98 | **955** | 1.07 | **below floor — invalid** |
| after `strain_1_L1_36` | 47 | 3,374 | **6.68** | **in-window — valid** |
| after `strain_1_L1_37` | 8 | **229** | 2.63 | **below floor — invalid** |

One in-window unit became one in-window unit plus two unmeasurable ones; 106 of
153 genomes moved out of the measurable set, and the in-window unit *count* was
unchanged (47 before, 47 after). This also explains the Track A comparison result
in `TRACK_A_VS_A100_COMPARISON.md`: the pre-split parent was not "elevated"
because it was a valid in-window measurement all along.

The draft predicted this. §2.6.2 states the gate order is load-bearing —
**diversity first, modality second** — and offers the working hypothesis that
"`gap/mean` high indicates a tight core plus a few outliers and subdivision is
futile". `strain_1_L1_26` was among the tightest units in the panel (median
pairwise 0.00060). §2.6.2 also states that **below n = 25 modality is
undecidable**, and `strain_1_L1_37` is n = 8.

### But the split is still defensible — if reported correctly

The draft already contains this exact precedent (§2.6.2): a 150-genome unit split
into "a usable 45-genome in-range unit plus a 95-genome clonal expansion at mean
140 SNPs (far below the floor, unusable for recombination inference, but of
independent interest as a probable outbreak or heavily-sampled sublineage)."

v4c's 154 -> 47 in-window + 98 + 8 is the **same shape**. So report it the same
way:

- `strain_1_L1_36` (n=47, r/m **6.68**) — the recombination result from this split;
- `strain_1_L1_26` (n=98) and `strain_1_L1_37` (n=8) — identified clonal
  expansions, of epidemiological interest, **reported with no r/m**.

That framing is defensible, consistent with the project's own precedent, and does
not require redoing the run.

---

## What to change

1. **`METHODS_DELTA` §5** — replace the r/m-inflation rationale with the modality
   +Gate 1 framing above, and state the gate order (diversity first).
2. **Do not quote** all-unit r/m medians or the values for out-of-window units.
   Report **7.38 (n=47, in-window)**.
3. **Drop `SRR28096043`** — n falls to 9.
4. **`maxForks` 48**, not 59, and only between runs.
5. Run Gate 1 **before** Gate 2 on any future partition.
