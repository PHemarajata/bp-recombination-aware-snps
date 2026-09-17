# Revision: clip 2's pacing. One defect, three acts, no content change

For the builder. Self-contained. **Clips 1, 3 and 4 are finished or fine and must
not be touched.** Measured 2026-09-17.

Source: `~/Downloads/TUC_CLIP2_2026-09-17/scene.py`, renders beside it.

## What is wrong

Every new act in clip 2 stops moving well before it ends. `Clock.hold_to(T)` pads
with one long wait to reach the brief's stated seconds, so the act hits its target
duration by freezing rather than by filling.

| act | duration | last visible change | longest frozen stretch | share |
|---|---|---|---|---|
| title card | 5.0 s | 2.8 s | 2.2 s | 44% |
| 1 | 48.0 s | 35.0 s | 13.0 s | 27% |
| **2** | 54.0 s | **22.1 s** | **31.9 s** | **59%** |
| 3 lead-in | 17.0 s | 11.8 s | 5.2 s | 31% |
| 4 lead-in | 17.0 s | 12.0 s | 5.0 s | 29% |
| **5** | 45.0 s | **25.5 s** | **19.5 s** | **43%** |
| **6** | 29.0 s | **14.7 s** | **14.3 s** | **49%** |

The narration is written and cannot be placed on this. It produces 14 line
boundary violations and four lines that begin after the picture has stopped,
including act 2's closing line speaking over a frozen frame for 21 seconds.

**Clips 3 and 4 do not have this problem**, at 8 to 24%. This is clip 2 only.

## Two fixes that do not work, checked so you do not repeat them

**Stretching the waits.** It works for acts 1, 3 and 4 at 1.2 to 1.5x. Acts 2, 5
and 6 would need 3.1x, 4.0x and 3.9x, which puts five to eight second holds on
single lines of text.

**Shortening the acts to match their content.** The narration needs the runtime.
Act 2's 120 words are 40 s of speech in a 54 s act, so the act length is correct
and the picture is too sparse for it. Shortening breaks the word budget instead.

**Acts 2, 5 and 6 need more visual beats.** That is the whole ask.

## What to change

**Acts 1, 3 lead-in and 4 lead-in:** stretch the intermediate waits by about 1.4x,
1.3x and 1.2x so content reaches within about 4 s of the end. Nothing else.

**Acts 2, 5 and 6:** add beats by splitting reveals that are currently combined.
This adds no content and states nothing new. In act 2 there are at least six:

- the two clades arrive in one `FadeIn`; give each its own
- their two labels likewise
- the caveat is one two-line `Body`; reveal the lines separately
- the verdict is one two-line `Body`; likewise
- the axis, its ticks, its labels and its caption are four things in two plays;
  give each its own beat

Apply the same treatment in acts 5 and 6. Act 5's five table rows are the obvious
candidates; act 6's three instrument properties are another.

## Hard constraints

- **Durations do not change.** 5, 48, 54, 17, 17, 45, 29 s, on target to the
  frame, because the narration word budgets depend on them.
- **The total stays 304.300 s** and the nine parts must still concatenate by
  stream copy in one pixel format.
- **No content changes, no new claims, no new numbers.** Splitting a reveal is
  allowed; inventing a thing to reveal is not.
- **Every guard in the clip 2 brief still binds**, including no species-wide r/m
  value in act 1, the 106-strain caveat in act 2, both window bounds as brackets,
  and every denominator labelled.
- **The diversity axis is the continuity object.** It is drawn in act 2 and never
  leaves. Do not disturb it.
- **The two reused clips are correct and final.** `DetectionWindowSweep` and
  `NegativeControlZoom` in `~/Downloads/TUC_LEGACY_MERGED_2026-09-17/` are the
  merged renders and are md5-identical to what is already in the clip. Leave them.

## What the picture has to support, per act

The narration exists. Give each act at least one beat per line, and prefer two.

| act | narration lines | words |
|---|---|---|
| 1 | 6 | 112 |
| 2 | 6 | 105 |
| 3 lead-in | 2 | 38 |
| 4 lead-in | 2 | 38 |
| 5 | 5 | 95 |
| 6 | 4 | 55 |

## Acceptance test, which you can run yourself

Decode each act at 10 fps, grayscale, downscaled to 192x108, and take the mean
absolute difference between consecutive frames. Treat any value above **0.05** as
a visible change.

1. **No frozen stretch longer than 6 s**, anywhere in any act.
2. **Last visible change within 4 s of the act's end.**
3. **No 6 s window in the first 90% of an act without a visible change.**
4. Frame counts exactly 60x the target seconds, and one pixel format across all
   nine parts.

## One thing not to over-fix

A collision check over clip 2 returns seven findings, all of them text sitting
0.02 to 0.12 units from other text without intersecting it. **Some are probably
legitimate.** A table label beside its value at 0.09 units is normal typography.
Two are worth a look because they are prose rather than table: act 2's
`Fromtheliterature,notmeasuredinthisstudy` against the R-M line, and act 6's
`Worksonlybetweenameasuredfloorandceiling` against `Bothboundsarebrackets`. Use
judgement; do not space out a table to satisfy a checker.
