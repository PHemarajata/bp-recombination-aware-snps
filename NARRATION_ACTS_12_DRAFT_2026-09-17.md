# Acts 1 and 2 narration, drafted and measured. Start times provisional.

Drafted 2026-09-17, ahead of the trim renders, because the words do not depend on
the trim and the line durations do not either. **Only the start times are
provisional.** When the trimmed acts arrive, re-map the beats and re-anchor. Do
not re-author and do not re-generate: the audio is already correct.

Both acts audit clean today, and their trims are small and come out of a single
still stretch each, which is what makes drafting ahead safe here. I would not do
this for acts 3 or 5.

## Act 1, The Question. Target 39.4 s, 88 words.

| # | start | words | measured | anchor |
|---|---|---|---|---|
| 1 | 1.90 | 20 | 6.64 s | the organism, soil and water across the tropics |
| 2 | 9.60 | 23 | 8.78 s | the case with no travel history, and the question |
| 3 | 19.80 | 12 | 4.46 s | the genome offered as the answer |
| 4 | 25.30 | 12 | 4.04 s | the three steps, sequence, relatives, source |
| 5 | 29.80 | 21 | 7.99 s | the turn into act 2 |

> **1.** This organism lives in soil and surface water across the tropics, so people
> meet it where they live and work.
>
> **2.** When a case appears in someone who never travelled, the question is where
> they met it, and classical case investigation often cannot say.
>
> **3.** A genome ought to settle that. Find where its closest relatives live.
>
> **4.** Read the origin off the tree. That, at least, is the promise.
>
> **5.** Except that comparing these genomes runs into something most pathogens do
> not do, and nothing downstream works until it is handled.

**31.90 s of speech, 19.0% silence, density 134.0 spoken words per minute of
runtime.** All lines fit.

The first draft came in at 80 words and **26.9% silence**, above the fifteen to
twenty band, with density at 121.8 and only just over the floor. Lines two and
four carried the extra words because they had the slack; nothing was restructured.

## Act 2, Fair Comparison. Target 41.7 s, 87 words.

| # | start | words | measured | anchor |
|---|---|---|---|---|
| 1 | 1.95 | 16 | 5.67 s | two isolates, genomes aligned |
| 2 | 8.70 | 13 | 5.20 s | related here, distant there |
| 3 | 15.60 | 10 | 3.44 s | the whole collection as one pile |
| 4 | 19.60 | 12 | 5.06 s | the collection cut into comparable pieces |
| 5 | 25.25 | 17 | 7.38 s | the counts land |
| 6 | 33.30 | 19 | 7.01 s | the turn into act 3 |

> **1.** Take two isolates and line their genomes up. In one stretch they look like
> close relatives.
>
> **2.** In another they look like strangers. One pair of genomes, two different
> answers.
>
> **3.** Do that across thousands of genomes and the signal blurs.
>
> **4.** So cut the collection first, into groups where a comparison means something.
>
> **5.** Nearly three thousand assemblies become eighty five groups, and nothing is
> compared across a boundary that matters.
>
> **6.** Now each group can be asked how much recombination it carries. That
> measurement turns out to have a catch.

**33.76 s of speech, 19.0% silence, density 125.2.** All lines fit.

## How the start times were predicted

Each act's trim comes out of its largest still stretch, so beats before the cut
hold and beats after shift earlier by the trim.

| act | cut taken from | beats that hold | beats that shift |
|---|---|---|---|
| Act 1 | 10.57 to 20.50, 9.93 s | 2.12, 9.58, 10.10, 10.57 | 20.50, 23.62, 25.95, 30.50, less 0.7 s |
| Act 2 | 15.60 to 25.85, 10.25 s | 1.95, 8.70, 15.60 | 25.85, 27.28, 32.95, 41.00, less 7.7 s |

**If the builder spreads a cut differently, every start time after it is wrong.**
That is the one thing to re-check, and `map_beats.py` on the delivered act answers
it in seconds.

Act 1's beats at 9.58, 10.10 and 10.57 are half a second apart and are treated as
one moment. Three lines cannot be placed there; the earlier refit put their
per-gap ceilings at under one word each.

## A finding that extends the voice measurement

**These two acts read at materially different rates.** Act 1 came back at 165.5
words per minute and act 2 at 154.6, a spread of seven percent on the same voice,
model and speed.

That is much larger than the 2.5% prose-against-numbers penalty measured on
purpose-built samples in `VOICE_MEASUREMENT_2026-09-17.md`, and it means **an act's
word budget cannot be set from another act's measured rate.** Budget from the
film-level figure, then measure each act and adjust its own start times. Act 4
behaved the same way: predicted 157.8, read 156.8 overall, and still hid a line
that ran 0.54 s long.

## What to do when the renders land

1. `map_beats.py` on the delivered act.
2. Compare against the predicted beats above. If the cut came from the expected
   stretch, only the shifted starts move and by a known amount.
3. Re-anchor the existing lines. **Do not re-author, do not re-generate.** The
   audio in the session scratchpad is final unless a line is rewritten.
4. Re-run the fit check. Every act so far has needed at least one start nudged.
