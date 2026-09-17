# Review: TUC clip 3, "What the ruler measured"

Render `1db0803b-26cb-436b-95e4-2a14c006b591`, silent picture, `TUC_CLIP3.mp4`,
299.300 s, 17,958 frames, 1920x1080 60/1.

**Verdict: revise. One structural blocker and three content blockers.** The
numbers are the best of any clip so far: every figure on screen reproduces from
source, including the three in act 7 that are registered nowhere, which I
re-derived independently. The problem is the picture, not the facts.

## The numbers are right, including the ones I doubted

Act 7's three figures appear nowhere in `NUMBERS.tsv`, so I recomputed them from
`GATE1_ALIGNMENT_2026-08-21.tsv` joined to the frozen basis. Taking "isolates
this project sequenced" as the `IP-`/`IE-` identifiers:

| act 7 draws | recomputed | match |
|---|---|---|
| 47 in-window units | 47 | yes |
| all in-window median 7.70 | 7.6988 | yes |
| 34 of them contain this project's isolates | 34 | yes |
| their median 7.74 | 7.7394 | yes |
| ten fall below the seven-member floor without them | 10 | yes |

The `IP-`/`IE-` reading is the right one: those are this project's own
unpublished Nakhon Phanom isolates, held in no public archive, so the identifier
is the metadata. The claim that the funded units are load-bearing and
representative at once is supported exactly as stated.

Table 2 also reconciles to the frozen basis: 47 + 12 + 26 = 85 units and
1,388 + 349 + 603 = 2,340 genomes, with medians 7.70, 1.32 and 2.14 and the
in-window IQR 5.72 to 9.41. The retired 5.51 to 9.44 does not appear. 5.51 is
drawn once, in act 2, labelled the number being corrected, which is the correct
handling of a constant `NUMBERS.tsv` marks **DO NOT QUOTE**. The floor
sensitivity is drawn as deviations from a flat 7.70, which is both the right
encoding for a sensitivity and what keeps 7.74 from colliding with act 7.

Also clean: 17,958 frames is exactly 299.3 x 60, one pixel format across all
nine parts, and no content clipped by the frame in any act.

## Blocker 1. This is a slide deck with fades, not an animation

**476 of the brief's 535 words, 89%, would be spoken over a frame that has
already been still for three seconds or more.** 238.9 s of the 299.3 s film sits
in a hold of three seconds or more.

I checked this against a fair threshold rather than a convenient one, because
the first pass looked implausible. Sweeping the change threshold down to where
it registers slow fades:

| part | origin | moving | longest single animation |
|---|---|---|---|
| C3Act3 | new | 5.07 s of 48.0 s (10.6%) | 0.60 s |
| C3Act7 | new | 6.28 s of 37.0 s (17.0%) | 1.17 s |
| RecursiveSubdivision | reused | 16.70 s of 35.7 s (46.8%) | 3.12 s |

So the new acts do animate. They animate about a third as much as the reused
clip that carries the same house style, in bursts a third as long, and the
magnitude of change is smaller by more than a decade: act 3's 99th-percentile
frame difference is 0.065 against 1.004 for `RecursiveSubdivision`. A reveal
here is a half-second fade of one text line, followed by four to five seconds of
nothing.

Act 3 is the clearest case. Its holds run 4.17, 4.87, 4.48, 4.87, 4.17, 4.97,
4.50, 4.17 and 3.83 seconds, separated by reveals of a frame or two. That is a
metronome, and 92 of its 110 words land on a held frame.

Act 1 is the same shape at a larger scale. Between 5.05 s and 19.98 s, nearly
half the act, exactly one thing happens: a single-frame change at 12.47 s. Two
consecutive holds of 7.43 s and 7.52 s sit either side of it.

Two acts are worse than the average:

- **`C3Act5Lead` is a still.** 14.0 s long, one change at 0.43 s, then 13.57 s
  frozen. All 30 of its words play over a frozen frame.
- **`C3Act4Lead`** spends 13.8 of its 14.0 s in long holds, 99%.

Per-act detail:

| act | runtime | last change | held tail | in holds >= 3 s | words on a held frame |
|---|---|---|---|---|---|
| C3Act1 | 31.0 s | 24.48 s | 6.52 s | 81% | 57 of 70 |
| C3Act2 | 65.0 s | 52.60 s | 12.40 s | 92% | 133 of 145 |
| C3Act3 | 48.0 s | 44.17 s | 3.83 s | 83% | 92 of 110 |
| C3Act4Lead | 14.0 s | 7.60 s | 6.40 s | 99% | 30 of 30 |
| C3Act5Lead | 14.0 s | 0.43 s | **13.57 s** | 97% | 29 of 30 |
| C3Act6 | 28.0 s | 24.00 s | 4.00 s | 89% | 58 of 65 |
| C3Act7 | 37.0 s | 33.97 s | 3.03 s | 92% | 78 of 85 |

**The runtimes themselves are defensible, so do not shorten the acts.** 535
words over 237 s is 135 wpm of runtime, which is what the briefs intend, and
close to what clip 1 actually realized. The fix is more animated steps inside
the existing runtime, one per sentence, which is what the skill asks for and
what the reused clips already do.

## Blocker 2. Act 3 writes its conclusion across the measured data

The 85-unit strip is the series continuity object, and the NOTE is right to
insist its marks are measured rather than schematic. Act 3 then drops the strip
to 0.28 opacity and writes the payoff sentence, "A low ratio is a detection
failure, not a quiet genome.", straight across it, with two more lines below and
two class labels above. The dots show through the glyphs and read as texture
behind a caption.

This is what act 3's 19 overlap flags are, including one at 98% of the smaller
element's box held for 14.5 s and four above 76% held for 9.5 s. The frame audit
is right to fire here even though it fires on benign nesting elsewhere.

Either the strip carries this act, in which case the conclusion belongs in the
clear band above it and the dots come back to full strength, or the act does not
need the strip and it should leave. Dimming measured evidence to make room for a
sentence about it is the one thing this series has been careful not to do.

## Blocker 3. Act 3's source note is stage direction

It reads **"Nothing new appears. The same picture, read the other way"**, in the
slot every other act uses for provenance: "85 analysis units, 2,340 genomes.
Diversity is measured", "Table 2, Gate 1 classification", "Worked demonstration.
Not part of the reported 85 units", "Floor sensitivity", and so on.

By act 3 the audience has learned that line means "here is where this came
from". Instead it gets a note about the construction of the film, whose content
is an admission that the act adds no picture. Give it a real source or drop it.

## Blocker 4. Act 7 draws two absolutes where the claim is agreement

The act ends on **"funded units 7.74"** and **"all in-window 7.70"** side by
side in 32-point type. The claim those numbers exist to support is that the two
are the *same*: load-bearing and representative, not a biased corner. Two large
absolutes 0.04 apart invite the viewer to look for the difference, which is the
opposite reading.

Act 6 solves this exact problem correctly one act earlier, by drawing its four
sensitivity medians as deviations from a flat 7.70 line so the flatness is the
picture. Act 7 should do the same: show the gap, or show both against a common
reference, not two numbers.

**The placement makes it worse.** Both readouts sit in a band immediately above
the log diversity axis, at fixed scene x of -3.30 and +1.55. The axis directly
below them runs 10 to 10,000 mean pairwise core SNPs, so the labels read as
positions on it, and "funded units 7.74" lands above the below-floor region,
over the red marks in the zone act 2 has just taught means the detector failed.
An r/m value should not be placed on a diversity axis at all.

## Minor

- **"funded units" is a second name for the same thing.** The frame's own
  sentence says "isolates this project sequenced", which is the brief's wording;
  the legend says "funded units" and the source note says "Funded units joined
  to Gate 1". It also reintroduces a framing the series dropped on purpose:
  clip 1's narration draft 2 removed the funding opening so the work carries it
  (commit `8b63767`). Two strings to change, and the underlying fact is correct
  either way.
- **Act 5's lead-in says the same thing twice.** Body line: "Every ratio was
  estimated on a tree." Source note: "r/m is estimated on a tree".
- **Act 5's schematic tree uses the measured colour.** Its three tips are the
  teal act 2 established for measured units, on an obviously schematic
  three-tip tree. The house rule is that schematic and measured must be
  distinguishable at a glance.
- **Digits are inconsistent across acts.** Act 2 uses digits (47, 7.70, 1,388);
  act 7 spells the same class of number out (Forty-seven, Thirty-four, Ten). The
  screen should carry the precision and let the voice spell things.
- **Act 2 has a 2 px text line held from 24.0 to 30.5 s.** Almost certainly a
  thin graphic the audit read as text rather than real unreadable type, but it
  is the one finding in act 2 and worth one look.
- **The strip's vertical axis has no meaning and no label.** Vertical position
  is jitter to separate marks. Nothing tells the viewer that.

## What the NOTE claims that does not hold

The NOTE reports "zero text overlaps, zero right-margin violations, zero
caption-band intrusions across all 60 holds" and "zero
stroked-geometry-through-text". The margin and caption-band claims hold up, and
so does the stroked-geometry claim, which is a genuine improvement over clip 2.
The zero-overlap claim does not: act 3 holds text over the unit marks for most
of the act, and the pixel audit finds it in every act but two.

The NOTE also plans narration on `eleven_multilingual_v2` at 168 wpm. Clip 1 was
voiced on **`eleven_v3`**, and 168 was refit downward from clip 1's own audio.
See the plan note; this is a series-level problem, not clip 3's fault.
