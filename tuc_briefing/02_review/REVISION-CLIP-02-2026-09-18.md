# Clip 2 revision, 2026-09-18

Two asks: apply clip 3's vocabulary change, and fix a narration that was still on
the previous slide.

## The sync defect, and why nothing caught it

Reported at 1:21. At that point act 2's narration says "that makes clades behave
as functional units of genetic isolation" while the screen has moved on to the
caveat. Fourteen seconds later it reads the caveat aloud, and by then the screen
has wiped to the verdict.

Measured, not judged. `trace_onscreen_text.py` walks the scene graph and records
when each on-screen string appears and disappears; `syncheck.py` pairs that with
the narration CSV. Three lines in the shipped cut were spoken while the line they
paraphrase was **off screen**:

| clip | said at | on screen | gap |
|---|---|---|---|
| act 2 | 39.20 | 26.53 to 30.60 | 8.6 s after it was wiped |
| DetectionWindowSweep | 12.82 | 5.93 to 7.33 | 5.5 s after |
| act 2 | 35.10 | 22.73 to 30.60 | 4.5 s after |

Two more acts were out of order rather than merely late. Act 1's last two lines
were swapped against their slides. Act 5 was the worst: the picture builds the
recovery table strictly bottom up, from the lowest donor divergence to the
highest, while the narration led with the headline 91% and then went back to fill
in the rest. The viewer hears "at two in a thousand" while the screen is showing
the 0.0005 row, which is drawn eight seconds before the 0.002 row exists.

**Why the existing checks passed it.** Every one of them asks about timing: does
the line fit its gap, is the clip too silent, is there a stall. None asks what is
on screen when the line is spoken. A clip can satisfy all of them and still be a
slide behind throughout.

**Why the fix is not "shift the timings".** The first pass solved the starts
against the measured audio and pushed act 5's lines two to three seconds later,
which re-created the lag. The lines were longer than the picture's cadence, so
the words came out instead. Act 5 is now nine lines against seventeen visual
moments, each budgeted at the rate this voice actually reads numbers.

All 70 lines were re-laid against the measured on-screen timeline. Zero lines are
now spoken after their slide is wiped, and every remaining flag is a lead of
under 1.5 seconds, which is what narration should do.

## Silence

| | shipped | now |
|---|---|---|
| gaps over 2.5 s | 9 | 3 |
| longest gap | 6.25 s | 4.75 s |
| gaps over 3.5 s | 4 | 0 |

The title card was the largest remaining silence, so its hold went from 5.0 s to
3.6 s. The brief asks for 1 to 2 seconds and clip 2 is the only film with a
separate card.

## Vocabulary

Same change as clip 3. "Ceiling" meant the window's upper bound here and a limit
on achievable performance in clip 4, which is why it read as jargon. On screen
and in narration:

- "below the floor" and "above the ceiling" become **below the window** and
  **above the window**
- "floor 700, bracket 588 to 755" becomes **lower edge 700, range 588 to 755**
- "Both bounds are brackets, not points" becomes **ranges, not points**

`DetectionWindowSweep` was re-rendered for this. `NegativeControlZoom` uses
neither word. Clip 4 is deliberately untouched: its "ceiling" is the ordinary
English sense and needs no teaching.

## Two traps worth keeping

**`generate_elevenlabs.py` keeps audio by line NUMBER, not by text.** Rewriting a
line and re-running reports "kept" and leaves the old recording in place. Two
acts were rewritten and silently kept their previous audio, which showed up as
impossible overruns. Delete the clip's voice directory when its lines change.

**`build_narration.py`'s silence and overrun checks are wpm estimates.** Act 5 is
almost entirely numbers, which this voice reads at roughly 120 wpm against a
176 wpm clip median, so the estimate called it 37% silent when the real audio
measured 22.7%. Build with a widened band when the estimate and the audio
disagree, then gate on `assemble_voice.py`, which uses the real files.
