# Review: TUC clip 2, "A ruler you can trust"

Render `19ac9526-d514-4dd0-a7a8-89207e202b78`, silent pass-one preview,
`TUC_CLIP2.mp4`, 304.300 s, 18,258 frames, 1920x1080 60/1.

**Verdict: revise. The visual is not frozen.** Four blockers. Two are content
errors that put a wrong number on screen, one is a layout collision, one is
structural. Everything measured below came from the delivered mp4 files, not
from `scene.py` and not from the builder's own audit.

## What the builder got right, confirmed independently

- **The assembly is what it claims.** All nine parts share codec, resolution,
  frame rate and pixel format. 18,258 frames is exactly 304.3 x 60, so the
  stream-copy concat is frame-exact.
- **Every constant reproduces.** Checked against `NUMBERS.tsv` and
  `SPIKEIN_RESULT.txt` directly: 1,519 replicates over 62 unit-replicons, 20
  returning any call at 1.32%, floor 700 with bracket (588, 755], ceiling 4,700
  with bracket (4631.8, 4731.6], recovery curve 20 / 40 / 91 / 100 / 90. The
  mid-run `TIER2_null.txt` snapshot was correctly not used.
- **Bracket placement is accurate.** The floor mark centers on x=1116, which
  reads 665 on the log axis against a true geometric mean of 666. The ceiling
  mark reads 4,685 against 4,681.
- **Fabrication guards honored.** Recovery is five discrete bars, not a fitted
  curve, and the non-monotonic top is kept as measured. No species-wide r/m
  value appears anywhere in act 1; the refusal is drawn instead, as a gray box
  reading "r/m, species-wide" over a rust "not computed here". The
  restriction-modification claim sits inside an outlined panel tagged "From the
  literature, not measured in this study", and that tag no longer collides with
  the sentence beneath it.
- **Character constraint clean.** All 41 on-screen string literals: zero em
  dashes, en dashes, semicolons or curly quotes, and no British spellings.
- **Nothing is clipped by the frame.** `audit_frames.py` returns no `clipped`
  fault in any of the seven new acts.
- **The three `overlap` flags are false alarms.** Act 5's persistent flag is the
  "0%" tick label against the axis line; act 6's two are the "10" and "10,000"
  end labels against their own ticks. All benign.

## Blocker 1. The same measurement is drawn as two different bars

Act 5 draws the fraction **"19 of 21" twice**, once labelled **91%** and once
labelled **90%**, and draws them at two different heights.

Measured from the delivered frame, with the axis calibrated off the 20% and
100% bars (which land at 20.00% and 100.00%, so the axis is linear and correct):

| donor divergence | label | fraction on screen | bar top | height reads |
|---|---|---|---|---|
| 0.002 | 91% | 19 of 21 | y=371 | 91.09% |
| 0.01 | 90% | 19 of 21 | y=376 | 89.94% |

The two bars differ by exactly **5 px, 1.14 percentage points**. 19/21 is
90.48%, so neither 91% nor a taller bar is supportable, and the picture asserts
a difference between two identical measurements.

This is inherited, not invented. `SPIKEIN_RESULT.txt` prints rate 0.91 for
nu=0.002 and 0.90 for nu=0.01 from **identical inputs**: 24 implants, 3
pre-detected, 19 recovered in both rows. The cause is in
`spikein_sensitivity_bp.py`: the count columns are summed across the three
replicates, but the rate column is `statistics.mean` of the three
**per-replicate** rates. So the percentage is a mean of ratios while the
fraction beside it is a ratio of sums. They are different estimators, and
pairing them in one label makes a claim that does not follow from its own
numerator and denominator.

**Fix on screen:** either label both bars 90% and draw them at the same height,
or keep 91% and remove the pooled fraction from that bar, naming it as the mean
across three replicates. Do not leave "19 of 21" next to "91%".

**Fix upstream, separately:** `TABLES.md` Table 4 and `NUMBERS.tsv`
`controls.spikein_recovery` carry the same pairing. Clip 3 and the manuscript
will quote it.

## Blocker 2. Act 6 breaks the brief's number-collision rule

The brief is explicit: label each figure with its denominator on screen every
time, and never place a recovery share and a false positive rate in the same
frame without both denominators visible.

Act 6's frame carries both, and neither has a denominator:

- "Returns essentially nothing when nothing is there.  **1.32%**"
- "Recovers nine tenths at the relevant divergence.  **91%**"

The NOTE states that "act 5's 91% recovery and act 4's 1.32% false-positive
never share a frame, and each carries its denominator on screen." That is not
what the render does.

Second problem in the same line: **"nine tenths" and "91%" contradict each
other**, in one sentence, and nine tenths is the figure the data supports.

## Blocker 3. Forty percent of the narration has no picture to sit on

The film is **233.9 s static out of 304.3 s, 77%**. Every new act finishes
moving in its first half to two thirds, then holds a single frame to the end.
Verified frame by frame, and for act 2 verified at full resolution: across its
27 s tail only 2 pixels of 2,073,600 vary at all, by 10 grey levels, which is
compression noise.

| act | runtime | last change | held tail | change events | brief words | words landing on the held frame |
|---|---|---|---|---|---|---|
| Act 1 | 48.0 s | 35.07 s | 12.93 s | 10 | 110 | 30 |
| Act 2 | 54.0 s | 26.57 s | **27.43 s** | 16 | 120 | **61** |
| Act 3 lead-in | 17.0 s | 11.87 s | 5.13 s | 6 | 40 | 12 |
| Act 4 lead-in | 17.0 s | 12.07 s | 4.93 s | 8 | 40 | 12 |
| Act 5 | 45.0 s | 25.57 s | **19.43 s** | 18 | 100 | **43** |
| Act 6 | 29.0 s | 14.77 s | **14.23 s** | 7 | 65 | **32** |

84 s of held frames, and **189 of 475 narration words, 40%, would be spoken
after the picture stops**. Act 2 is the worst: half the act is one frame, and
it is the act the brief calls the one that most needs to land.

The brief says "runtime follows from word count at the chosen voice's measured
rate." The per-act seconds were advisory outputs of that calculation, not
targets. The NOTE confirms they were used as targets: "this preview is held at
the stated per-act seconds so the narration has its room." Padding to a target
is the recurring failure on this project and it recurred here.

The arithmetic does not support the runtimes either way. 475 words at Justin's
measured 148 wpm is 193 s against 210 s built; at eleven_v3's ~179 wpm it is
159 s. The brief's own seconds imply 136 wpm, which is not any measured rate.

**Fix:** add animated steps inside the tails, or shorten the acts. The tails are
the only affected region, so this is not a rebuild. Acts 1, 2 and the act 4
lead-in also leave the lower third to half of the frame empty while they hold,
which is where the added steps belong.

## Blocker 4. Act 1 has a real text collision

The r/m fraction's denominator rule runs **36 px through the sentence** "Now
compute one r/m for the whole species.", underlining the "N" and part of the
"o". The rule sits at y=324-325 spanning x=487 to 594; the sentence begins at
x=558.

Cause, in `scene.py` around line 280: the r/m group is scaled to 0.62 and
centered at `[-4.1, 1.7, 0]`, which puts its right edge near x=-2.74 in scene
units, while `trap` is centered at `[0.4, 1.75, 0]` and starts near x=-3.11.
Moving the group to about x=-4.8, or the sentence to x=0.9, clears it.

`audit_frames.py` reported act 1 **clean**, and the builder's nine-frame contact
sheet missed it too. A 2 px rule crossing a glyph is invisible at thumbnail
scale. Worth remembering that the frame audit does not catch this class.

## All four text checks, run separately

`check_text_collisions.py` could not be run: manim is not installed on this
machine, since these renders come from the external animation agent. The four
checks were done on pixels from the delivered files instead. Three are clean and
the one failure is blocker 4 above.

| class | result |
|---|---|
| text intersects text | **one defect**, act 1's fraction rule through "Now" (blocker 4). A rule-crossing sweep over all nine parts at 33 sample points returned 42 candidates; 41 are axes, box edges and bars sitting on their baseline. |
| text abuts text | **marginal in one place.** Act 6's two bracket label lines sit 15 px apart against a 16 px floor (0.12 scene units). Readable, worth one nudge while act 6 is open anyway. Other candidates were artifacts of row-profile scanning, which ignores x: act 5's "100%" and "91%" bar labels share rows but are 174 px apart horizontally. |
| text leaves its own fill | **clean.** All five of act 5's white "N of M" bar labels sit wholly inside their bars, with margins of 25 to 42 px on every side, checked at three times. This is the class that put a wrong number on screen in clip 1, so it was checked directly rather than by sampling. |
| a wrap inside one Text | **no wrapping seen** in the title card, act 1 at two times, act 2 at two times, both lead-ins, act 5 and act 6. The NOTE says clip 1's corrected `Txt()` wrap guard is carried over verbatim. Since the text cache has poisoned renders before, confirm `media/texts` was cleared before the revision render rather than trusting this preview. |

## Minor, not blocking

- **Act 6's axis has no unit.** Act 2 labels the continuity axis "mean pairwise
  core SNPs in the unit"; act 6 places 700 and 4,700 on a bare 10 to 10,000
  axis. Given how often the ska and alignment bases have been confused in this
  corpus, the handoff frame should name the unit.
- **Act 6's ceiling bracket is drawn 6.4x too wide.** `bracket()` applies a
  minimum half-width of 0.09 units. At 486 px per decade the floor bracket's
  true width is 52.8 px and it is drawn 57 px, but the ceiling's true width is
  4.5 px and it is drawn 29 px. The two read as 2:1 when the truth is 11.7:1, so
  the picture understates how much more tightly the ceiling is pinned. The NOTE
  discloses this, the error is in the conservative direction, and the labels
  carry the true numbers, so this is acceptable if deliberate. Say so in the
  NOTE rather than leaving it to be rediscovered.
- **Act 5 leaves the diversity axis.** Its x-axis is donor divergence, which is
  the right quantity for the claim, but it means the continuity object does not
  in fact persist through every act as the brief describes.

## For the record: the NOTE's narration conventions are stale

The NOTE plans narration on "Justin, `eleven_multilingual_v2`, 168 wpm". The
house model is **eleven_v3**, v2 should not be substituted for fit reasons, and
Justin measures **~148 wpm** on these scripts, not 168. Settle the rate before
any narration is timed, since every act's runtime depends on it.

## Note on the beat map

`map_beats.py` under-reports on this material, consistent with past runs. It
found 4 moments in act 2 where full-frame differencing finds 16 change events,
and 7 in act 5 where there are 18. The per-act change event lists below are the
ones to narrate against. `03_beats/` holds the script's output; treat its
moment counts as a floor.

### Change events per act, measured (seconds)

```
Act 1   0.92-1.08  9.42-9.45  9.68-9.70  12.28-12.80  16.70-16.88  19.70-20.30
        20.70-20.72  22.63-22.77  27.47-27.48  35.05-35.07   then held to 48.00

Act 2   1.00-1.08  2.88-2.90  3.38-3.40  5.87-5.93  6.18-6.20  7.38-7.40
        8.18-8.20  8.58-8.60  10.98-11.00  13.37-13.42  13.68-13.70  16.28-16.87
        17.30-17.80  21.42-21.43  21.68-21.70  26.55-26.57  then held to 54.00

Act 3 lead-in   1.58-1.78  1.98-2.00  4.53-4.90  7.18-7.20  7.43-7.70
                11.85-11.87   then held to 17.00

Act 4 lead-in   0.75-1.20  2.78-3.10  3.30-3.42  3.78-4.10  6.08-6.10
                7.62-7.65  7.88-7.90  12.05-12.07   then held to 17.00

Act 5   0.72-1.20  3.25-3.35  3.58-3.60  4.65-5.00  5.38-5.40  7.12-7.50
        7.88-7.90  9.58-10.00  10.38-10.40  12.98-13.40  13.78-13.80
        15.28-15.90  16.28-16.30  17.78-18.20  18.78-18.80  20.78-20.80
        21.38-21.40  25.55-25.57   then held to 45.00

Act 6   0.48-0.50  2.05-2.25  3.75-3.93  5.45-5.80  7.48-7.50  8.48-8.50
        14.75-14.77   then held to 29.00
```

The two reused clips are fine on this measure. `DetectionWindowSweep` changes
until 47.18 s of 47.8 s and `NegativeControlZoom` until 38.05 s of 41.5 s, both
with dwells rather than one long tail.
