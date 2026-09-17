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

---

# Both defects fixed, 2026-09-17

Source: `tuc_clip1_scenes.py` at the repo root. Complete set in
`~/Downloads/TUC_CLIP1_SALVAGE_2026-09-17/clips_fixed/`, 291.000 s, all
1920x1080 at 60 fps. Acts 1, 2, 6 and 7 are the delivered files unchanged; 3, 4
and 5 are re-rendered here.

## The durations were right; only the distribution was wrong

Checked before cutting anything: at the brief's word budgets and Justin's
measured 168 wpm, every act's runtime is already correct at about 20% silence
(75 w in 34 s, 120 w in 54 s, and so on). So the terminal waits were redistributed
into the body rather than trimmed, and all three acts land on their original
duration to the frame.

| act | longest still, before | after | duration |
|---|---|---|---|
| 3 | 13.1 s, 33% | **4.0 s, 10%** | 40.000 s, 2400 frames |
| 4 | 18.6 s, 34% | **4.5 s, 8%** | 54.000 s, 3240 frames |
| 5 | 18.8 s, 37% | **5.6 s, 11%** | 51.000 s, 3060 frames |

No new content was written. The existing reveals were spread out, act 3's
two-line explanation now lands a line at a time, and act 3 clears that
explanation at the end so the 2,976 / 2,340 / 85 summary stands alone.

## The act 4 overprint

`p2` flowed down from `p1` while `p3` was placed at an absolute y inside it. The
stack is now relative throughout and raised to y = -1.05, which is the lowest
position that clears both the source note (y -2.61 to -2.83) and the reserved
bottom eighth. Verified by rendering, not by arithmetic.

## A render trap that cost most of the time here

Midway through, the fixed act 4 started rendering with `p2` wrapped and
overlapping itself. It was not the edit. **The same file renders clean from one
directory and wrapped from another**, and clearing `media/texts` fixes it:

| where | `media/texts` | p2 |
|---|---|---|
| repo, after my probe scripts had run | 187 svg | **wrapped** |
| scratchpad | 51 svg | clean |
| repo, after `rm -rf media/texts` | rebuilt | clean |

Manim caches rendered text as SVG keyed by a hash. The probe scripts I used to
measure the layout constructed the same strings at other sizes and keyword
combinations into the same media directory, and afterwards the real render picked
up geometry that was not its own. It is silent, it is deterministic once poisoned,
and it changes text metrics, so a render can be wrong without anything in the
source being wrong.

**Clear `media/texts` before any render whose output will be delivered, and keep
measurement scripts out of the media directory a film renders into.** The three
acts above were rendered from a cleared cache.

## The audit gap is now closed

`check_text_collisions.py` at the repo root walks the live scene graph at every
animation boundary and reports overlapping text and anything crossing into the
reserved bottom eighth. It works on the scene graph rather than on pixels, which
is why it does not mistake a grid of filled squares for a line of text, as a
density test does.

Validated against the known defect, then run over everything:

| act | original | fixed |
|---|---|---|
| 1, 2, 3, 5, 6, 7 | clean | not re-rendered / clean |
| 4 | **overlap 61%, t 31.6 to 54.3 s** | clean |

Act 4 was the only collision in the clip, so acts 1, 2, 6 and 7 are safe to ship
as delivered.

## Still open

Narration for all seven acts. The beat map in `beats/` was measured against the
old acts 3, 4 and 5 and must be re-run on `clips_fixed/` before narration is
written against it.

---

# Superseded the same evening: Animo delivered a better clip 1

Render `340a15a4`, continued from `88f4dbee`, not from the run that died. It is
the clip 1 to use. Copied to `~/Downloads/TUC_CLIP1_2026-09-17/`, and
`tuc_clip1_scenes.py` at the repo root is now its `scene.py`.

Seven acts plus `TUC_CLIP1.mp4`, **291.000 s**, every act on its brief target to
the frame, `h264 1920x1080 60/1 yuv420p` throughout, concat verified by stream
copy.

## The work above was duplicated, and then some

Its acts 3, 4 and 5 were carried from `88f4dbee`, which had **already** made both
fixes recorded above: `p3` is placed relative to `p2`, and the source carries the
comment "1.6 -> 3.6, tail redistributed". Measured still stretches are 3.8 / 4.5
/ 4.8 s against the 4.0 / 4.5 / 5.6 s reached here independently.

It then fixed five defects this session missed. The one that matters:

**Act 2's opening line was overprinted in the set assembled above**, with
"sequencing" printed on top of "was meant". Verified by cropping t = 2 s from both
copies. Three more were geometry in acts 1 and 2: a line sitting 0.003 units clear
of the dot grid, two lines running over the grid, and a band border running through
its own text.

## The Txt() helper had a real bug

The K-scaling wrap detector compared only height. A wrap that reflows into the
**same line box** holds height constant, measured at a ratio of 0.9998, which
passes the 1.3 test, while width collapses from 8.360 to 6.520 scene units, 78%
of the K=1 layout. Width is the reliable signal because a wrap always reflows
narrower:

```python
if m.height / K <= base_h * 1.3 and m.width / K >= base_w * 0.95:
```

Re-auditing all 59 distinct strings with the corrected helper reports zero wraps.
**This belongs in `aphl_common.py` before the next clip is built.**

This is the same failure class as the `media/texts` trap recorded above, reached
from the other end: there a poisoned cache made a correct string wrap, here a
blind detector let a wrapping string through.

## The collision checker's blind spot, stated

`check_text_collisions.py` compares bounding boxes **between** Text objects, so a
wrap **inside** one object is invisible to it. That is exactly why it passed act 2
as clean. The `Txt()` width guard catches that class at the source. The two are
complementary and both are needed: the checker reports Animo's build clean across
all seven acts, which is how that build was verified here.

## Beat map, re-run

`~/Downloads/TUC_CLIP1_2026-09-17/beats/`, at `--floor 0.05`.

| act | dur | beats | largest gap | words | lines at ~19 w |
|---|---|---|---|---|---|
| 1 | 34.0 s | 12 | 5.9 s | 75 | 4 |
| 2 | 51.0 s | 19 | 7.4 s | 115 | 6 |
| 3 | 40.0 s | 12 | 4.6 s | 90 | 5 |
| 4 | 54.0 s | 15 | 5.9 s | 120 | 6 |
| 5 | 51.0 s | 18 | 5.9 s | 115 | 6 |
| 6 | 43.0 s | 13 | 4.7 s | 95 | 5 |
| 7 | 18.0 s | 5 | 4.4 s | 40 | 2 |

94 moments against 41 from the delivered map, because `map_beats.py` clamped its
threshold with a hardcoded `max(thr, 0.25)` that no `--sensitivity` value could
reach. Fixed in the skill with a `--floor` option, default unchanged. Every act is
anchored throughout, so no narration line has to land on a still frame.

**650 words is 232 s of speech at Justin's 168 wpm into 291 s of picture, 20%
silence.** The brief's budgets fit the delivered picture without adjustment.

## Still open

Narration. Its note records that the brief was not on that disk, so its on-screen
figures were carried from the previous pass's header rather than re-verified. That
gap is covered: the figures were checked against `NUMBERS.tsv` earlier in this
document.
