# Gate 1 recomputed from alignment distances — W3

2026-08-21. Closes weak spot **W3** of `MANUSCRIPT_OUTLINE_2026-08-21.md`.

> **⚠ THIS BOX WAS REVERSED. Which number goes in the paper: 7.70 (n = 47).**
>
> As originally written this box said 7.44, because `METHODS_DRAFT` §2.12 then
> designated the **88-unit A100 run** as production. **That designation has since
> been reversed.** The reported run is the **22-core workstation, 85 units, 2,340
> genomes**, and on it the alignment-derived Gate 1 gives **47 in-window units,
> median r/m 7.70** (below floor 12 / 1.32, above ceiling 26 / 2.14). The
> **7.44 (n = 48)** derived below is the **A100 cross-hardware control**.
>
> Both are computed the same way and differ only in which run's r/m table they
> score. **Do not mix them** — that is the error this whole line of work exists to
> prevent. Their closeness (7.70 vs 7.44, 3.5%) is a comparability result, not a
> discrepancy. See §7c for all four circulating values tabulated.

**Headline on the reported run: 7.70, not 7.26.** The window's *structure* is
confirmed and is sharper than the Mash proxy showed. Its *floor* was in the wrong
place — carried across unit systems without translation.

> **Reading note.** Below this point the body still says "control run" where it
> means the workstation run that is now *reported*, and vice versa. The
> derivations and every number are correct; only the two run labels were swapped
> by the later redesignation. §7b and §7c are written in the current designation.

---

## 1. Why this mattered

Gate 1 (`METHODS_DRAFT` §2.6.1) admits units in **≈1,270–4,671 mean pairwise core
SNPs, calibrated in `ska distance` units**. But membership was decided from
`approx_mean_snps = mash × 3,805,619` — a conversion whose own docstring calls
itself triage-grade, in a different unit system from the calibration.

That gate decides which units enter the headline r/m median at all, and it had
already moved that number once: the entire 7.38-vs-7.26 discrepancy resolved
earlier the same day came down to **one unit's position relative to this window**.

`DISTANCES_v4c_SUMMARY.tsv` carries `raw_mean` — mean pairwise SNP distance
computed directly on each unit's core alignment, per replicon. Summed across
replicons (one genome, two parts; the `ska distance` calibration was
whole-genome) that is a SNP count, the same *kind* of quantity the window is
calibrated in.

`raw_mean` is used rather than `filt_*` deliberately: Gate 1 is applied **before**
trusting Gubbins, so conditioning it on the recombination-filtered distance would
mean validating Gubbins with its own output.

## 2. The proxy is badly wrong

| | |
|---|---|
| ratio mash / alignment | min **0.66**, median **1.30**, max **17.20** |
| units where the proxy is >2× off | **17 of 85** |

The proxy systematically **overstates** diversity, and does so unevenly. Applying
the unchanged ska-unit bounds to alignment distances reclassifies **22 of 85
units** — a quarter of the panel.

## 3. The first answer was wrong, and why

Applying the **old bounds** to the **new distances** gives in-window n=39, median
r/m 8.05. That result is incoherent and must not be quoted: it pushes 15 units
below the floor, several with *high* r/m (12.28, 8.27, 7.60, 7.26, 6.80), and the
below-floor group's median rises to 3.78. Gate 1's whole premise is that below
the floor detection fails and r/m collapses. A below-floor group with r/m up to
12 falsifies that.

It is also unstable: combining replicons by mean or chr1 instead of sum gives a
median of **3.56** and puts **no unit** above the ceiling at all.

**Transplanting bounds between unit systems is the same error the gate already
had.** The bounds have to be relocated, not reused.

## 4. The window structure is real — and sharper than Mash showed

Median r/m by diversity band, alignment distances, equal-count bins:

| diversity (aln) | n | median r/m | |
|---|---|---|---|
| 15–797 | 14 | **1.53** | detection failure |
| 840–1,574 | 14 | 7.25 | |
| 1,596–2,449 | 14 | 8.39 | |
| 2,739–4,247 | 14 | **8.59** | peak |
| 4,463–6,365 | 14 | 3.68 | |
| 6,387–8,757 | 14 | **2.14** | collapse |

Cleanly unimodal, rising 1.53 → 8.59 and falling back to 2.14. **Gate 1's premise
survives the change of metric.** The Mash version of the same table is flatter at
the bottom (3.78 in its lowest band), i.e. the proxy was *blurring* the very
signal the gate depends on.

## 5. Relocating the bounds — without selecting on r/m

Choosing bounds to maximise in-window r/m would be circular. The original
calibration used **independent** criteria — union recombination coverage and
median tract length against a literature ~5 kb — and both are in
`DISTANCES_v4c_SUMMARY.tsv` (`masked_fraction`, `masked_bp / n_recomb_intervals`).
Located on those alone:

| diversity (aln) | n | union coverage | tract kb | *(r/m, not used)* |
|---|---|---|---|---|
| 15–588 | 12 | **4.3%** | **1.12** | *1.32* |
| 755–1,349 | 12 | 28.0% | 3.37 | *6.30* |
| 1,355–2,010 | 12 | 35.7% | **4.08** | *8.81* |
| 2,015–3,375 | 12 | 51.2% | 3.63 | *9.11* |
| 3,403–4,732 | 12 | 46.8% | 3.77 | *6.08* |
| 4,750–6,532 | 12 | 68.1% | **2.69** | *2.96* |
| 6,629–8,757 | 12 | 67.7% | 2.22 | *2.14* |

**The bottom band reproduces the original calibration's failure signature
almost exactly.** The draft records "a cluster at 405 gave union 0.7% and an
abnormal 1,002 bp median tract"; here the 15–588 band gives **4.3% coverage and a
1.12 kb tract**. Independent confirmation that the floor is real — and that it
sits far below 1,270.

**Floor: bracketed (588, 755]**, where coverage jumps 4.3% → 28.0% and tract
1.12 → 3.37 kb. **Not 1,270.**

**Ceiling: ≈4,700**, where tract falls 3.77 → 2.69 kb, between the 3,403–4,732 and
4,750–6,532 bands. **The ceiling translates essentially unchanged from 4,671** —
which is a genuine check on the whole exercise, since nothing forced the two unit
systems to agree at the top.

## 6. The result

Relocated window **[700, 4,700]** in alignment units:

| | n | median r/m |
|---|---|---|
| **in-window** | **47** | **7.70** (IQR 5.51–9.44) |
| outside | 38 | **1.99** |

**Insensitive to where in the bracket the floor is put** — 588 → 7.70, 700 →
7.70, 755 → 7.74, 840 → 7.78. The answer does not depend on the judgement call.

The in/out separation is **3.9×**, cleaner than the Mash gate's (7.26 in, 2.04
below / 2.48 above).

| | figure |
|---|---|
| Mash proxy, ska-unit bounds *(what was quoted)* | 7.26 (n=47) |
| old bounds on alignment distances *(incoherent — do not quote)* | 8.05 (n=39) |
| **alignment distances, relocated bounds** | **7.70 (n=47)** |

That the relocated window admits **47 units, the same count as before**, is
coincidence — the membership differs.

## 7. What this settles, and what it does not

**Settled.** The r/m headline no longer rests on a triage-grade sketch
conversion. Gate 1's premise is independently confirmed, on criteria that are not
r/m, and it is confirmed *more* strongly than the proxy suggested. **Quote 7.70
(n=47, alignment-derived Gate 1).**

**Not settled, and both should be disclosed:**

1. **Alignment SNP counts are not provably identical to `ska distance`.** SKA
   counts SNPs from split k-mers over whole assemblies; this counts them on a
   reference-mapped core alignment. Much closer than Mash, not proven equal. The
   ceiling agreeing to within 1% across the two systems is reassuring but is one
   data point.
2. **⚠ Union coverage never reaches the calibration's stated 76–88% anywhere in
   this panel — the maximum band median is 68%, and coverage *rises* with
   diversity, peaking in the bands the gate rejects.** The original calibration
   reports 76–88% for its in-window clusters. That discrepancy is unexplained. It
   does not affect the floor (which is located by the 4.3%→28% jump, far from
   this range) but it means the coverage criterion is **not** reproducing
   quantitatively, and a reviewer could press on it.

**The floor bracket (588, 755] is 1.28× wide**, against the ska-unit floor's
(405, 1,268] at 3.1×. Tighter, on more units, in the units actually used.

## 7b. ⚠ A defect in `DISTANCES_v4c_SUMMARY.tsv` found 2026-08-22

> **⚠ LABELS CORRECTED 2026-08-23.** This section was written when the **A100 /
> 88-unit** run was designated *production* and the **workstation / 85-unit** run
> was the *control*. **That designation has since been reversed**: the reported
> run is the 22-core workstation (85 units, 2,340 genomes) and the A100 run is the
> cross-hardware control. Every "production"/"control" below has been rewritten to
> the current designation. **No number changed** — only which run each belongs to.
> The inverted text had already propagated into `METHODS_DRAFT` §2.12.10, where it
> was corrected the same day. If you are reading an older copy of this section,
> distrust its run labels and trust the table.

The file is **keyed to two different partitions at once.** Eighty-five of its 88
rows carry membership the two runs agree on, but **`strain_1_L1_11` (24 vs 18),
`strain_1_L1_22` (34 vs 32) and `strain_1_L1_26` (154 vs 98) carry the
*reported* run's**, and it simultaneously holds
`strain_1_L1_36`/`strain_1_L1_37`, which are **control-only** children of
`strain_1_L1_26`. Those 153 genomes are therefore counted twice, and the file's
88 unit names are not any one run's partition.

**Consequence.** Joining it to the **control** r/m table by unit name gives the
n = 98 child the unsplit parent's diversity, **1,310**, when its own members sit
at **72**. Recomputed on control membership from `core.tab`:

| unit | control n | true diversity | as filed | effect |
|---|---|---|---|---|
| `strain_1_L1_11` | 18 | 3,424 | 5,819 | above ceiling → **in-window** |
| `strain_1_L1_22` | 32 | 3,672 | 4,525 | no change |
| `strain_1_L1_26` | 98 | **72** | 1,310 | in-window → **below floor** |

**The control's figures are unaffected: 48 in-window, median r/m 7.44, either
way** — the two misplaced units swap in and out and both sit below the median.
The *composition* changes, and that is what matters for §2.12.10.

**The reported figure (7.70, 47 units) is not affected at all**, because for
those three units the file's membership *is* the reported run's.
`generate_numbers.py`, which joins to the reported r/m table, is correct as
written — and is doubly safe, because that table carries only the 85 reported
units, so the control-only rows drop out on the join.

**Rule: do not join `DISTANCES_v4c_SUMMARY.tsv` to the *control* partition by
unit name.** Recompute diversity on control membership first.

### 7c. The four r/m values, tabulated

Partition × basis. Verified 2026-08-23 by recomputing all four cells:

| median r/m (n in-window) | Mash proxy | alignment-derived |
|---|---|---|
| **reported run** (workstation, 85 units) | 7.26 (47) | **7.70 (47)** |
| control run (A100, 88 units) | 7.38 (47) | 7.44 (48) |

Quote **7.70**. The other three are real measurements of something else, which is
what makes them dangerous: a value from the wrong cell reads as a rounding
discrepancy rather than a different analysis.

## 8. Reproduce

```bash
python3 gate1_from_alignment_bp.py --floor 700 --ceiling 4700
```

Sensitivity: `--combine {sum,mean,chr1}`; bounds via `--floor`/`--ceiling`.
Per-unit output in `GATE1_ALIGNMENT_2026-08-21.tsv`.

## 9. Consequences for the documents

> **⚠ TWO CLAIMS IN THIS SECTION ARE SUPERSEDED. Do not act on it as written.**
>
> **1. The run labels are inverted**, as the header box at the top of this file
> warns for everything below §7a. The reported run is the **workstation, 85 units,
> 7.70 (n = 47)**; the A100 88-unit run at **7.44 (n = 48)** is the cross-hardware
> control. The bullet below says the opposite.
>
> **2. The `strain_1_L1_26` reading is wrong, and §7b supersedes it.** The bullet
> below calls the n = 98 child **in-window** and concludes refinement increased
> the measurable set by one. That reads the **as-filed** diversity of 1,310, which
> §7b shows is the unsplit parent's value inherited through a join on unit name.
> Recomputed on its own membership the child sits at **72**, which is **below the
> floor**. §7b was written a day later and is the correct reading.
>
> The in-window count does go 47 → 48 between the two bases, so that half of the
> bullet is accidentally right, but the extra unit is **`strain_1_L1_11`**
> (above ceiling → in-window at its true 3,424) and not this split, which is
> net-neutral. Confirmed 2026-09-03 against `GATE1_ALIGNMENT_2026-08-21.tsv` and
> the control's own gate file.
>
> This matters beyond bookkeeping: comparing the child's Mash figure of 955 to the
> alignment-derived floor of 700 is exactly the cross-unit-system error this whole
> document exists to correct, and it reached Table 3 of the manuscript.

- **`METHODS_DRAFT` §2.6.1** should state the window in alignment units,
  **[700, 4,700]** with the floor bracketed **(588, 755]**, and record the
  ska-unit bounds as the original calibration.
- **The production-run figure is 7.44 (n=48)**; 7.70 (n=47) is the control run.
  `METHODS_DRAFT` was updated 2026-08-21: §2.6.1 now states the window in
  alignment units, §2.12.7 reports 7.44/48, and §2.12.10 carries a flag —
  under the alignment gate `strain_1_L1_26` (n=98) is **in-window**, not below
  floor, so refinement *did* increase the measurable set by one and the
  paragraph's earlier reading no longer holds.
- **7.38 still must not be overwritten** — it is the A100/88-unit variant and is
  internally consistent with "88 units" and "5.70".
- `generate_numbers.py` still emits `rm.median_gate1` from the Mash-based
  window. **It should be switched to the alignment metric**, which is the
  remaining mechanical task.
