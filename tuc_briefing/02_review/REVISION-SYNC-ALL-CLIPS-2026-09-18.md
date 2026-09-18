# The narration was behind the picture in all four films

Found while fixing clip 2's reported "narration still on its slide while the
presentation has already moved on". It was not confined to clip 2.

## How it was measured

`trace_onscreen_text.py` walks a Manim scene and records when each on-screen
string appears and disappears. `syncheck.py` pairs that with the narration CSV
and flags any line spoken while the string it paraphrases is off screen.

Neither existed before. Every check in the toolchain asks about **timing**: does
the line fit its gap, is the act too silent, is there a stall. None asks about
**content**, so a film can satisfy all of them and be a slide behind throughout.

## What it found, and what was done

| film | lines spoken after their slide was wiped | worst | now |
|---|---|---|---|
| 1 | 3 | 6.3 s | 0 |
| 2 | 3 | 8.6 s | 0 |
| 3 | 3 | 15.8 s | 0 |
| 4 | 1 | 8.0 s | 0 |

Clip 3's three were found **after** it had been re-delivered once. The first pass
fixed its dead air and never checked what was on screen, and one of the three was
introduced by that pass: clearing the two pointer labels early left the line that
names them with nothing to point at.

## One root cause, four films

The pictures reveal faster than anyone can narrate, and then hold. Clip 1's act 1
put four findings on screen in seven seconds, held 2.2 s, wiped, then held 10.1 s
on the next frame. Clip 1's act 2 put five strings up in twelve seconds and held
seventeen. Clip 3's act 2 drew three class rows and a spread, then wiped 3.4 s
later. Clip 4's act 7 closed on 8.8 s of held frame.

The narration was written to fill the total runtime, so it stretched across the
wipe and arrived late. **Moving the narration does not fix this.** Solving clip
2's start times against the measured audio pushed act 5 two to three seconds
later and re-created the lag, because the lines were longer than the picture's
cadence. Either the words come out, or the hold moves from the end of the act to
the middle where the content is. Both were used.

Runtime changes: clip 1 act 1 keeps 34.0 s with 5 s moved from its closing hold
into the findings block; clip 1 act 2 51.5 to 57.0 s; clip 3 act 2 58 to 63 s;
clip 4 act 7 77.0 to 72.7 s.

## Silence, after

| film | runtime | silent 10 s windows | longest gap |
|---|---|---|---|
| 1 | 285.3 s | 0 | 4.75 s |
| 2 | 302.9 s | 0 | 4.75 s |
| 3 | 299.1 s | 0 | 3.00 s |
| 4 | 472.8 s | 0 | 6.50 s |

Clip 4's 6.50 s sits at the seam between act 5 and the reused separability clip,
and clip 1's 4.75 s at the act 6 to act 7 seam. Both are scene transitions in
acts that were not otherwise touched.

## Two cautions for anyone re-running this

**`syncheck.py` produces false positives on number-dense text.** It matches on
shared content words, and this material repeats "units", "median", "seven" and
"point" constantly. Five of the six flags on the corrected clip 3 were spurious
pairings across unrelated sentences. Read every flag against the interleaved
timeline before acting on it; a lead of under about 1.5 s is correct and wanted.

**Manim returns `Text.text` with the spaces stripped.** Tokenizing it finds
nothing, which is why the first version of the check reported zero defects on a
film with known ones. Match by substring.

## Pronunciation and a misread number, 2026-09-18 (second pass)

Three review notes, all acted on.

**pseudomallei and Nakhon Phanom.** The engine read both wrong in clip 1. The
say_as map now carries `pseudomallei` to `su-do-MA-lee-eye` and `Nakhon Phanom`
to `Na-kon Pa-nom`. The spec text holds the respelling, so the engine says it and
the captions still print the real spelling.

**SNP spelled out, not "snip".** Ten lines in clip 2 and, for series
consistency, the two in clip 4's reused outbreak clip. `SNP` now goes to
"ess enn pee" and `SNPs` to "ess enn peez". Clip 4's change was not asked for;
reverse it if "snip" is wanted there. One knock-on: "a SNP threshold" became
"an SNP threshold", because the article follows how the abbreviation is said.

**The floor-sensitivity beat read as an error.** The line recited the four
absolute medians, "seven point seven, seven point seven, seven point seven four,
seven point seven eight", while the screen plotted DEVIATIONS from 7.70. Hearing
7.7 twice sounded like a stutter and invited the reading that 588 was a value of
the same quantity.

It is not. **588, 700, 755 and 840 are candidate positions for the window's
lower edge, in mean pairwise core SNPs. 7.70, 7.70, 7.74 and 7.78 are the
in-window median r/m recomputed at each of them.** Two being identical is the
result: moving the edge from 588 to 700 changes the median by nothing.

The line now says what is drawn: "Against seven point seven zero: nothing,
nothing, four hundredths, eight hundredths." Act 6 went 28.0 to 30.0 s to give
it room; it had been the least silent act in the clip at 9.4%.
