# Clip 3 revision, 2026-09-18

Three review notes from the lab chief, and what each turned out to be.

## 1. "1:12 audio drops. check again throughout."

**Real, and worse than reported.** A full decode of the delivered film found one
12.5 second stretch with no audio at all, from 1:24.7 to 1:37.2. The reported
time was close; the gap itself was the last 11.5 seconds of act 2 plus act 3's
own lead-in.

**Cause.** Act 2's brief stated a 65 second target. The scene was padded to hit
it with a closing `self.wait(11.5)` over a still frame that nothing was said
over. This is the same failure as the APHL acts: an advisory duration became a
target and the padding went in at the end, where it is least visible.

**It was reported and ignored.** `build_narration.py` printed
`PACING C3Act2: 11.5s of held frame after the last line` on the build that
shipped, along with three shorter stalls in acts 1, 3 and 7. Those lines are
warnings, not refusals, and the tool says so: "these are builder fixes, not
script fixes. The files are still written." They were read as advisory and
nothing was done. **A pacing warning is a defect report.**

**Fixed.** Act 2's hold cut from 11.5 s to 4.5 s and a closing narration line
written for the frame that was being held. Acts 1 and 7 given the lines they
were missing. Longest silence in the film is now 3.75 seconds, down from 12.5.

| act | silence before | after |
|---|---|---|
| act 1 | 34.5% | 24.4% |
| act 2 | 29.5% | 15.3% |
| act 7 | 28.4% | 15.8% |

One 3.6 second pause is kept on purpose, at 1:53, immediately after "A low ratio
is a detection failure, not a quiet genome." lands. That is the claim the series
rests on and the beat is deliberate. Say so if it gets flagged again.

## 2. "1:45 very messy with overlaps"

**Real, ten instances across four acts.** The pointer label "above ceiling: so
much the estimate collapses" was printed across the shaded window itself, and
"Only the units inside the window are quiet or loud on purpose." was cut in half
by the window's lower edge.

**Why the checker passed it.** `check_text_collisions.py` has a text-over-marks
test that deliberately ignores any shape larger than the text, because sitting
inside a background panel is normal. The shaded window is exactly such a shape,
so a line laid across its boundary was invisible to every check. Inside is fine
and outside is fine; **straddling is the defect**, and nothing tested for it.

A sixth check was added for it. Run against the shipped source it found ten
instances: three in act 2, two in act 3, three in act 4's lead-in and two in
act 7. All ten are fixed, and all seven acts now report clean.

**The underlying arithmetic.** The band is 1.9 tall about y = 0.10, so it runs
from -0.85 to 1.05. Act 7's own comment said the gap above the axis starts at
-0.75, which is wrong by the band's half-height. Every line placed on that
assumption was cut. The file now carries `BAND_TOP`, `BAND_BOT`, `ROW_ABOVE`
and `ROW_BELOW` as named constants: exactly one text row fits above the band and
exactly one fits below it.

## 3. "act 7 a bit confusing ... every time 'ceiling' is mentioned I'm thrown off"

### The word collides with itself across the series

"Ceiling" carries two unrelated meanings four films apart:

- clips 2 and 3, the **upper diversity bound of the detection window**, our own
  coinage, and something the viewer has to be taught
- clip 4, a **limit on achievable performance**: "two ceilings", "the linkage
  ceiling", "the country ceiling", "what moves the ceiling". This is the ordinary
  English sense and needs no explanation at all

Clip 3 now uses plain description instead: **below the window**, **above the
window**, and **the lower edge** where a noun is needed. The window is drawn on
screen, so the words say what the picture shows. Clip 4's usage is left alone,
because it is the sense that already reads.

`IQR` is also gone from the screen. The band said "In-window IQR is 5.72 to
9.41"; it now says "Half of them fall between 5.72 and 9.41", which is what an
IQR is.

### Act 7's explanation was genuinely ambiguous

"Those ten would not exist as measurements at all. **Their** median r over m is
seven point seven four." reads as the median of the ten. It is the median of all
thirty four funded units. The line now names its subject, and the picture labels
both figures with their denominators: "the 34 funded units 7.74" against
"all 47 in-window units 7.70".

"Load-bearing and representative at the same time" was replaced with
**"Ten units depend on them. The number does not."**

## What is still open, for the lab chief to decide

Clip 2 uses the old vocabulary in three narration lines and on screen in its
reused act 3, which is a legacy render shared with nothing else. Clip 4's four
"ceiling" mentions are the other sense and read fine on their own, but they are
the far side of the collision. Neither was touched: changing them means
re-rendering and re-voicing films that are already in review.

Clip 3's legacy reuse was re-rendered, because `RecursiveSubdivision` is used
only by clip 3. Its pre-existing findings (axis labels in the reserved bottom
eighth, the "eighteen times lower" annotation on its arrow) are unchanged and
were verified identical to the shipped version before and after the edit.
