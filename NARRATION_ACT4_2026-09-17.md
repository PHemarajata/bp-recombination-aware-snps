# Act 4 narration, written and measured

For `Act4NotSeparable.mp4`, render `09ad83cd-63a7-4bdc-9adb-dc71d34fd810`. Written
2026-09-17 against the measured beat map, generated with Justin, and checked
against the real audio rather than against the arithmetic.

The generated files live beside the clip in that render directory:
`narration/` holds the CSV, SRT, VTT, TXT, the spec and the per-line MP3s, and
`Act4NotSeparable_narrated.mp4` is the muxed result. They regenerate from the spec
below, which is why this document is the tracked artifact and they are not.

## The lines

Written against the six measured moments, not the authored beat marks. Seven lines
over six moments, because the first gap carries two and one line spans the pair at
31.40 and 33.25.

| # | start | words | anchor |
|---|---|---|---|
| 1 | 1.8 s | 17 | title, then the Thailand share bar begins to draw |
| 2 | 9.0 s | 9 | the two thirds line, held |
| 3 | 13.0 s | 5 | the project grid starts filling |
| 4 | 16.1 s | 18 | the grid completes, six outlines left standing |
| 5 | 23.7 s | 18 | the association scale, held at its measured value |
| 6 | 31.4 s | 24 | the axis returns, then the five Americas groups land outside the window |
| 7 | 43.0 s | 18 | the pivot text |

> **1.** Before asking whether a genome can name a country, it is worth asking what
> this collection holds.
>
> **2.** You cannot find structure in a place nobody sampled.
>
> **3.** Now ask who sequenced them.
>
> **4.** Almost every project sampled a single country, which makes a study and a
> place very nearly one fact.
>
> **5.** So when a group of genomes looks geographic, nothing here can separate real
> geography from who collected it.
>
> **6.** And for the region this whole question was asked about, all five groups sit
> outside the detection window, so recombination cannot even be measured.
>
> **7.** None of that makes the genome uninformative. It means country is not the
> question this collection can settle.

## Measured fit, the check that mattered

Generated at `eleven_turbo_v2_5`, voice `uFIXVu9mmnDZ7dTKCBTX`, **speed 0.9**, then
every line timed with `ffprobe`.

| # | start | predicted | **actual** | ends | next starts | fit |
|---|---|---|---|---|---|---|
| 1 | 1.8 | 6.46 | 5.85 | 7.65 | 9.00 | ok |
| 2 | 9.0 | 3.42 | 3.25 | 12.25 | 13.00 | ok |
| 3 | 13.0 | 1.90 | 1.67 | 14.67 | 16.10 | ok |
| 4 | 16.1 | 6.84 | **7.38** | 23.48 | 23.70 | ok after the fix |
| 5 | 23.7 | 6.84 | 7.11 | 30.81 | 31.40 | ok |
| 6 | 31.4 | 9.13 | 9.43 | 40.83 | 43.00 | ok |
| 7 | 43.0 | 6.84 | 7.01 | 50.01 | 51.00 | ok |

**Line 4 overran on the first pass.** Predicted 6.84 s, read 7.38 s, which put it
0.08 s into line 5. Moving line 5 from 23.4 to 23.7 cleared it. Nothing was
rewritten.

That is the whole argument for measuring rather than computing. The clip-level
arithmetic was fine and would have hidden it: **109 words, 41.70 s of speech, 18.2%
silence, engine reading 156.8 wpm against a predicted 157.8**, within one percent.
The error was entirely inside one line.

## Rules this was written to

- **Density 128.2 spoken words per minute of runtime**, above the 120 floor that
  flags a clip stating conclusions instead of narrating.
- **Silence 18.2%**, inside the fifteen to twenty percent band.
- **First word at 1.8 s**, under the two second limit on opening silence.
- **No digit anywhere in the spoken text.** "Five groups", "two thirds" as words.
- **The screen carries precision, the voice carries meaning.** The narration never
  reads a number the picture already shows. The bar says 1,561 and 779; the voice
  says you cannot find structure in a place nobody sampled.
- **Written to the reviewed constraint.** The review found about three lines would
  have no visual change under them, so lines 2, 5 and 7 draw conclusions over held
  frames and none of them claims motion. That is the `7.09` failure avoided rather
  than repeated.

## Where this does not apply

**This is the APHL cut.** It is generated at turbo speed 0.9 for a room with many
second-language listeners. The TUC series uses the same voice at
`eleven_multilingual_v2` speed 1.0 and 168 wpm, so if this act is ever reused
there its lines need regenerating and re-fitting, not just re-timing.
