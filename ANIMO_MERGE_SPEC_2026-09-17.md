# Merge specification: one codebase, two films

Step 4 of `FILM_SHARING_ARCHITECTURE_2026-09-17.md`. This is the item that
unblocks the TUC briefing series and it also closes every pending revision on the
five legacy clips, because they are the same pass over the same file.

**For the builder.** Manim is not installed on the Mac, so this is a
specification, not a change set. The Franklin Gothic faces are installed here, so
layout can be checked locally once renders come back.

## 1. What is being merged

| source | where | contains |
|---|---|---|
| legacy | `~/Downloads/ANIMO_DELIVERABLES_2026-09-09/source/scene.py` | 931 lines, 5 scene classes |
| house | `~/.agi/renders/36e4638f-.../src/` | `aphl_common.py` plus 6 act bodies |

The two already share a palette. Identical hex values for teal, purple, rust and
ink, identical Franklin Gothic faces, identical white background. `aphl_common.py`
is the later vintage: it kept every value, renamed a few, and **assigned each color
a fixed meaning**. The legacy scenes predate that assignment.

**Target:** the five legacy scenes become act bodies in the house tree, importing
`aphl_common.py` for tokens and helpers. One token module, one `Txt()` glyph fix,
one set of color meanings, for both films.

## 2. Token mapping, mechanical

| legacy | house | note |
|---|---|---|
| `TEAL_D` | `TEAL_TXT` | same value `#006E79` |
| `TEAL` | `TEAL` | same `#00A0AF` |
| `TEAL_X` | `TEAL_DK` | same `#005057` |
| `RUST` | `RUST` | same `#B42E34`, but see §3 |
| `PURPLE` | `PURPLE` | same `#9960A7`, but see §3 |
| `INK` | `INK` | same `#404040` |
| `RULE` | `GRIDGRAY` | same `#E2E9EC` |
| `GRAY` | `SRCGRAY` or `GRAYOUT` | same `#6E6E6E`, pick by role |
| `F_TITLE` / `F_BODY` | `FONT_TITLE` / `FONT_BODY` | identical faces |
| `F_EMPH` | none | house has no Demi token. Add one rather than inlining the string. |

Legacy `L(...)` should become the house `Txt()` / `Body()` / `Title()`, which is
what carries the Pango glyph-spacing fix. Do not keep two text constructors.

## 3. The four semantic divergences

These are the only real work in the merge. Everything else is renaming.

### 3.1 Purple is geography, and eight legacy uses are not geography

| scene | lines | current meaning |
|---|---|---|
| `DetectionWindowSweep` (7.03) | 385, 401, 403 | the **mutation** bar, its label and its percentage |
| `OutbreakThreshold` (7.12) | 879, 880, 881, 900, 903 | the **detection-efficiency** curve, label, dot and caption |

Neither is a place. Both must move off purple, because in a series where these
play alongside the APHL acts, purple means country in one act and mutation in the
next.

**Pick replacements from the unassigned ramp** (`TEAL_LT`, `AMBER`, `ORANGE`) or
from a second teal step. I am deliberately not choosing: 7.03's pair is a
two-way share of one measured quantity and 7.12's pair is two schematic curves,
and those want different treatments. Name the constraint, not the swatch.

The constraint: **purple and rust are both unavailable**, and in 7.03 the two bars
must stay distinguishable at the moment they flip 0/100 to 43/57 and back, because
that flip is the mechanism the whole series rests on.

### 3.2 Rust is for adverse outcomes, and the imported tract is not one

In `DetectionWindowSweep`, most rust is correct: `NOT MARKED` (370), the
out-of-window dots (422), the not-in-window branch (436), the below-floor and
above-ceiling medians (473, 475).

**Wrong:** lines 339, 340, 342 and 356 color the imported tract and its label
"one imported piece". That tract is the subject being detected, not a failure.
Under the house rule it is either the measured signal (teal) or, if it is drawn
schematically, a neutral marked as schematic.

Audit the other four scenes' rust uses against the same rule. I have not read all
35 and most are likely correct.

### 3.3 The diversity axis is log in legacy and linear in the house system

Same quantity, same window `[700, 4700]`. **Adopt the house linear axis.**

This is not only consistency. Section 11.2's complaint about `7.07` is that the
eighteen-fold drop from 1,310 to 72 "reads as a small step" on a log axis.
**Switching to the house axis closes that revision for free**, so do 3.3 before
attempting the `7.07` annotation fix and then re-check whether the annotation is
still needed.

### 3.4 Nomenclature

Legacy says "group": `group diversity`, `mean pairwise core SNPs in the group`,
`85 analysis groups`. The house build guide requires one name per concept.
**"Unit" throughout.** This is a string sweep, but check it does not overflow any
label box, since "unit" is shorter than "group" in some places and the layouts
were spaced for the longer word.

## 4. Fold in the pending section 11 revisions

All five legacy clips are pre-revision. Doing these during the merge costs one
render each instead of two.

- **`7.09`**, the largest payoff. Replace paired absolute r/m with one dot per
  comparison against a reference line at 1.0. Eleven dots below, one above. Per-
  comparison values are in `TREEBUILDER_EQ_RESULT.txt` and
  `RAPIDNJ_EQ_RESULT.txt`, twelve rows each. **This also fixes a measured defect:
  the clip has three detected moments in 26.6 s, the last at 5.80 s, so 78% of its
  runtime is a still frame.** Its narration must be re-authored, not retimed, and
  that is specified in `tuc_briefing/02_review/REVIEW-reused-clips.md`.
- **`7.03`**, three fixes: promote the counted-as bars to co-star with the genome
  track, dwell on the three anchors at 243, 1,284 and 5,819 rather than ticking
  through 44 values, and hide the tract outline at the above-ceiling state so the
  viewer tries to find it and fails.
- **`7.07`**, two fixes: link the bar segments to their positions on the diversity
  axis, and annotate the eighteen-fold drop. Re-check the second after 3.3.
- **`7.12`**, two fixes: invert the emphasis so the 0 to 15 SNP band is not a
  sliver, and render the schematic curves sketchily while the four published
  anchors become the solid spine. **Do not fix this by making the curves look more
  like data.**
- **`7.01`**, three fixes: cut the seven seconds of empty zoom from 20 to 27 s,
  keep an inset showing the null at its own scale at the moment 427-fold is
  claimed, and settle on one name for the control.

## 5. Em dash sweep, twenty strings

The house style forbids em dashes in anything on screen. The APHL style guide
never inherited the rule and mentions em dashes only as a `t2s` italic bug.

| file | line | replacement |
|---|---|---|
| `act1_body.py` | 30 | `across the tropics, soil and water` |
| `act1_body.py` | 57 | `a case, no travel history` |
| `act2_body.py` | 113 | trailing dash, two-part reveal. Restructure. |
| `act3_body.py` | 39 | `Each unit carries a diversity, how different its genomes are.` |
| `act3_body.py` | 65 | `r / m, how much difference came from recombination, not mutation.` |
| `act3_body.py` | 90 | `r/m reads falsely low, a detection failure, not biology.` |
| `act3_body.py` | 135 | `So some units, and some places, cannot be read at all.` |
| `act4_body.py` | 42 | `one sequencing project is often one country, batch can mimic geography` |
| `act4_body.py` | 74 | `Schematic map, regions, not to scale` |
| `act4_body.py` | 98 | `all outside the window, recombination cannot even be measured` |
| `act4_body.py` | 105 | `The honest reason is sampling, most public genomes come from a few...` |
| `act5_body.py` | 17 | `back to the case, no travel history` |
| `act5_body.py` | 37 | `41 of 46, 89%` |
| `act5_body.py` | 38 | `10 of 46, 22%` |
| `act5_body.py` | 50 | **content fix too**, see below |
| `act5_body.py` | 64 | `one lineage: ST92` |
| `act5_body.py` | 88 | trailing dash, two-part reveal. Restructure. |
| `aphl_common.py` | 63 | `Schematic, illustrative` |
| `title_body.py` | 10 | `Placing a melioidosis case, the region, not the country` |
| `title_body.py` | 13 | leading dash on a subtitle fragment. Restructure. |

Three need judgement rather than substitution: the two trailing dashes are
two-part reveals where the second half arrives later, and the title fragment is a
subtitle.

**`act5_body.py` line 50 is a content fix, not a punctuation one.** It reads
"fails — barely above chance". Country attribution is 22% against a 26% baseline,
so it is at or below chance. **"fails: no better than chance"** is accurate and is
the stronger line.

Replacements change text width, so fold this sweep into acts already being
re-rendered rather than running it as its own pass.

## 6. What must not change

- **Every accuracy guard in `BUILD-GUIDE.md` and `SPINE.md` still binds**, except
  the Act 4 count, which `ANIMO_ACT4_REVISION_2026-09-17.md` removes.
- **The palette values.** This merge renames tokens and reassigns two colors'
  meanings. It changes no hex value.
- **`7.12`'s schematic curves stay schematic.**
- **The bottom eighth stays reserved** in every act, legacy included. The frame
  audit found no caption-band intrusion in the APHL acts and that must survive.
- **Every `run_time` stays a multiple of 0.1 s.**
- **The `Txt()` K-scaling glyph fix applies to every text object**, including all
  legacy text once `L()` is retired.

## 7. Verification, in order

1. `python3 audit_frames.py` on each re-render. **`clipped` is a hard failure.**
   Run it at the render's own resolution, not on an upscaled preview.
2. `python3 map_beats.py` on each re-render. Expect `7.09`'s three moments to
   become many; if it still shows a long dead tail, the encoding change did not
   land.
3. **Grep the built scenes for `—`. Expect zero.**
4. **Grep for `PURPLE`. Every surviving use must be geography.**
5. Confirm no scene prints a count of geographically structured units.
6. Only then narration, per `VOICE_MEASUREMENT_2026-09-17.md`: Justin at 168.0
   wpm for the TUC cut, and a speed decision for the APHL cut, whose room is
   second-language heavy.

## 8. You may refuse any part of this

If a semantic reassignment cannot be made without damaging the picture, say so and
propose the alternative. Section 3.1 in particular hands you a constraint rather
than a swatch, and if the unassigned ramp cannot carry 7.03's two bars legibly at
the flip, that is worth knowing before five scenes are rebuilt around it.
