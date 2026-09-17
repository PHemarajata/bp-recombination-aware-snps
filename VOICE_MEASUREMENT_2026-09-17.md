# Justin, measured

ElevenLabs voice `uFIXVu9mmnDZ7dTKCBTX`. Measured 2026-09-17 on this Mac, by
synthesizing real narration text and timing the audio with `ffprobe`. Every word
budget in both films was written against an assumed 132 words per minute, which
is the rate the earlier narration pack was timed at and was never a property of
this voice.

## The headline

**168.0 words per minute at default speed, on act-length passages.**

174 words over 62.14 seconds, across two samples written in house style:

| sample | words | seconds | wpm |
|---|---|---|---|
| prose, the reversal act | 82 | 28.89 | 170.3 |
| number-dense, the class split | 92 | 33.25 | 166.0 |
| **pooled** | **174** | **62.14** | **168.0** |

**The number-density penalty is small**, 2.5% between prose and a passage that
spells out eleven figures as words. That was the main worry and it is not one.

## Measure on act-length text, not on lines

Per-line rates are not usable for budgeting. Six single lines of six to fifteen
words scattered from **138 to 195 wpm**, and a 58-word paragraph read at 155.1.
The same voice on 82 and 92-word passages reads at 170.3 and 166.0.

Short samples are dominated by onset padding and phrase-final lengthening. Since
the unit we budget is the act, **168.0 is the figure to use**, and the per-line
scatter is a reason to re-check fit after synthesis rather than to trust any
single line's arithmetic.

## Speed control works, and it lands on the old design

| model | speed | wpm |
|---|---|---|
| `eleven_multilingual_v2` | 1.0 | 155.1 |
| `eleven_multilingual_v2` | 0.9 | 154.8 |
| `eleven_multilingual_v2` | **0.8** | **131.7** |
| `eleven_turbo_v2_5` | 1.0 | 176.3 |
| `eleven_turbo_v2_5` | 0.9 | 157.8 |
| `eleven_turbo_v2_5` | 0.8 | 136.5 |

Measured on one 58-word paragraph, so these are comparable to each other but not
to the 168.0 act-length figure.

Two things to know. **`multilingual_v2` ignores 0.9**, returning 154.8 against
155.1, then responds at 0.8. `turbo_v2_5` responds smoothly across all three, so
it is the model to use if a rate between the two is ever wanted. And **0.8 lands
at 131.7 wpm**, which is within half a percent of the 132 the packs were designed
around.

## What this does to each film

### TUC briefing series: budgets rise about 28%

Runtimes are a choice here because nothing is built. Holding the intended
runtimes at 168 wpm with a fifth of each clip silent:

| clip | reused | target | old budget | that would now run | new budget |
|---|---|---|---|---|---|
| Clip 1 | — | 300 s | 510 | 228 s | **672** |
| Clip 2 | 89.3 s | 300 s | 370 | 254 s | **472** |
| Clip 3 | 62.3 s | 300 s | 420 | 250 s | **532** |
| Clip 4 | 44.9 s | 420 s | 660 | 340 s | **840** |
| total | | | 1,960 | | **2,517** |

A faster voice buys more words at the same length. It does not shorten the clip.

**Run TUC at speed 1.0.** One fluent technical viewer, watching alone, who can
rewind. 168 wpm is brisk and appropriate.

### APHL film: the fifteen percent overshoot problem is gone

Runtimes there are fixed by a rendered picture, so the words move instead. At 168
wpm the original stated budgets stop being a problem: 425 words is 152 seconds of
speech against 235.3 seconds of picture.

| act | runtime | stated | old refit | fits at 168 wpm, 18% silence |
|---|---|---|---|---|
| Act 1 The Question | 40.1 s | 85 | 71 | **92** |
| Act 2 Fair Comparison | 49.4 s | 90 | 82 | **113** |
| Act 3 The Window | 46.2 s | 80 | 69 | **106** |
| Act 4 Geography, rebuilt | ~53 s | 90 | 75 | **122** |
| Act 5 The Ceiling | 46.6 s | 80 | 71 | **107** |

`NOTES.md` was right that the budgets did not fit, and right about why: they were
set against a rate measured on different content. **The defect was the assumed
rate, not the budgets.** Nothing has to come out. There is room for more.

**The APHL speed is a real decision, and it is not the same as TUC's.** That film
goes to the APHL Global Health all-country call, where many listeners are working
in a second language. 168 wpm is fast for that room. Speed 0.8 gives 131.7 wpm,
which is the pace the film was designed for.

The cost of slowing it: at 132 wpm the film carries about 425 words over 235.3
seconds of picture, which is **108 spoken words per minute of runtime**, below the
120 floor that flags a clip stating conclusions rather than narrating. At speed
1.0 and 540 words it reaches 138 and clears the floor comfortably, but reads fast.

So the honest position is that **this film's picture is slightly longer than its
script at any comfortable pace.** Three ways out, in the order I would try them:

1. **Add words at speed 0.8.** 471 words reaches the 120 floor at 9% silence.
   Tight but legal, and it keeps the pace the audience needs.
2. **Tighten the picture in the re-render.** Acts 3 and 4 are being re-rendered
   anyway. Trimming held frames is the structural fix rather than a compromise.
3. **Accept 108 and speed 0.8.** Defensible for a film with deliberate pauses on
   a number-dense subject, but it will read as sparse.

## How this was measured

`ffprobe` on the returned MP3, words counted by whitespace split. Sample text was
narration prose carrying no accession, location, date or exposure label, so
nothing restricted left the machine. Scripts are in the session scratchpad; the
method is three lines and is quicker to redo than to archive.

Re-measure if the voice, the model or the speed changes. Any of the three moves
the rate, and the rate sets every runtime downstream.
