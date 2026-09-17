# Salvage: the died Animo run built all of TUC clip 1

`~/.agi/renders/df1eb4b1-f5db-4ad5-b453-7ac91efc28d4`, examined 2026-09-17.

**Everything is salvageable.** The run did not die early. It built the complete
picture for clip 1, audited it, mapped its beats, and died at the narration step
with the spec written but every `text` field empty. That is the exact point where
this project takes over anyway, because narration is written and voiced here.

## What is there

| act | title | duration | frames |
|---|---|---|---|
| 1 | What this project built | 34.0 s | 2040 |
| 2 | Resistance, asked and closed | 51.0 s | 3060 |
| 3 | Two frameworks, one collection | 40.0 s | 2400 |
| 4 | Where the 312 went | 54.0 s | 3240 |
| 5 | The same answer, a second time | 51.0 s | 3060 |
| 6 | The question this makes askable | 43.0 s | 2580 |
| 7 | What the rest of this takes | 18.0 s | 1080 |

All seven complete, 1920x1080 at 60 fps, 291 s total. Plus `scene.py` (45 KB,
self-contained), contact sheets, a frame audit and a beat map.

Durations match the brief's advisory seconds exactly. Act titles match the brief,
except act 3, which the brief calls "Two frameworks, reconciled" and the build
titles "Two frameworks, one collection".

## The house rules hold

- **Zero em or en dashes.** All 37 `group` hits are Manim's own `VGroup`; zero
  on-screen "group".
- **Numbers verify.** 2,976 panel and 50 countries against `NUMBERS.tsv`
  `panel.v4c` and `panel.countries`; 2,340 in 85 units against
  `FINAL_PARTITION.tsv`; Thailand 1,753 against `phylo.thailand_share_panel`.
  `scene.py`'s header cites a source per figure.
- **The n >= 5 trap is avoided.** Act 3 says "a unit needs a minimum size before
  it can be measured at all" and puts no number on screen. `TABLES.md` line 25
  still carries the wrong `n >= 5`; the build did not inherit it.

## The frame audit is a false positive, and it missed the real defect

Act 2's three persistent "small-text" faults are the 312-dot grid scaled to 0.58
in the left margin. A row-based detector reads a row of dots as a text line. The
dots are legible. Every other fault in `audit.json` is a single transient sample
during a scale animation.

**What the audit did not catch is a hard overprint in act 4.** `p2` is placed
with `.next_to(p1, DOWN)` and flows down to about y = -2.55; `p3` is placed
absolutely at y = -2.42. They collide, both are illegible, and it is the final
held state of the act for 22.7 seconds:

> Their lineages are too rare in the global panel for a
> measurable unit to form around them.

overprinted with

> That is a finding about the panel, not a defect in the isolates.

`scene.py:578-583`. The audit checks small text and clipping, not collision. This
is the second time a collision has survived an audit on this project; the first
was the APHL act 3 label collision.

## The pacing defect is systematic, and it is in the authoring, not the render

The beat map under-reports by two to four times, so it should not be trusted on
its own. A direct frame-difference sweep at 10 Hz gives the real numbers:

| act | last visible change | longest still stretch | share of act |
|---|---|---|---|
| 1 | 28.0 s | 6.0 s | 18% |
| 2 | 43.5 s | 7.5 s | 15% |
| 3 | 26.9 s | 13.1 s | 33% |
| 4 | 35.4 s | 18.6 s | 34% |
| 5 | 32.2 s | 18.8 s | 37% |
| 6 | 37.9 s | 5.1 s | 12% |
| 7 | 13.1 s | 4.9 s | 27% |

Every one of acts 1 to 5 ends with a single long `self.wait`: 10.1, 11.6, 12.8,
**22.7** and **22.9** seconds. The brief said runtime follows from word count and
that its seconds were advisory. The builder treated them as a target and hit them
by padding the end rather than by pacing the content across the duration.

At the brief's budgets and Justin's measured 168 wpm the narration is 232 s
against 291 s of picture, so about 59 s of the film is slack and most of it is
piled into two terminal holds.

**Acts 1, 2, 6 and 7 are fine as they stand.** Acts 3, 4 and 5 need the tail
redistributed.

## Why this is the cheapest possible moment to have found it

Narration does not exist yet, so there is no timing to preserve. Re-pacing acts
3, 4 and 5 costs nothing downstream, where the same change against written
narration would force a refit.

Manim 0.21.0 is live in the venv at `/tmp/manimenv` and `TucC1Act7` re-rendered
from this `scene.py` here, so the fix does not need Animo.

## What this changes about the Animo plan

**Clip 1 does not need to go back to Animo.** The classifier failure on
`BRIEF-01` is now moot for the picture: it is built. `BRIEF-01-ALT-derisked.md`
stays useful only if clip 1 ever has to be rebuilt from scratch.

Animo's remaining work is clips 2, 3 and 4.
