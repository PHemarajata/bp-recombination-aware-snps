# The APHL film, resynthesized under a fixed seed

Rebuilt 2026-09-17 after review found audible variation between acts.
Deliverables: `~/.agi/renders/4f9166a4-.../film_reseeded/`.

## What changed

**Every line resynthesized with `seed: 20260917`.** Same voice, same model, same
speed, so the pace decision is untouched. 31 lines across five acts.

**Six lines said "group" where the picture says "unit".** Mine, in the new
narration, and the same desync I had just finished correcting in the legacy
narration. It would have shipped. Act 2 lines 4 to 6, Act 3 line 6, Act 4 lines 5
and 6. Zero remain.

**Act 3 line 6 overran the clip end by 0.11 s** and was shortened in the same
pass, from "So one question remains. Where do those groups sit?" to "One question
remains. Where do those units sit?"

**Captions are wrapped now.** `build_narration.py` was fixed earlier today, so
this build emits 42-character lines and no `line:` cue setting. The previous
delivery had 55-character lines and `line:84%` applied by hand.

| | |
|---|---|
| runtime | 213.121354 s, unchanged |
| cues | 31, longest caption line 42 chars, zero `line:` settings |
| rate across acts | 156.6 to 173.6 wpm, mean 162.7, spread 10% |
| fit | all 31 lines, no overruns |

## What was tested and rejected first

Three approaches to the variation, all measured before choosing:

| approach | between-line rate spread |
|---|---|
| independent calls, no seed, the old build | 12 to 18% |
| **request stitching**, `previous_text` and `next_text` | **41%** |
| **stability raised** 0.5 to 0.85 | **21%** |
| whole act in one generation, split on silence | unusable |

Stitching conditions prosody on neighbours, which helps continuity and
destabilises pacing: one line fell to 108 wpm. The single-generation approach
detected eleven silences for five lines, splitting mid-sentence, so the threshold
would need hand-tuning per act.

**The seed is the one that worked**, and for a reason worth recording separately.

## The seed finding, which supersedes an earlier one

**A fixed seed makes durations exactly reproducible.** Four lines regenerated with
the same seed returned identical to the millisecond: 8.359/8.359, 4.505/4.505,
8.452/8.452, 6.966/6.966. The audio is not byte-identical, but the timing is.

This overturns `elevenlabs-synthesis-is-not-deterministic`, which was measured
without a seed and is correct only in that case. **With a seed, a line can be
regenerated safely**, which is what made this resynthesis a mechanical operation
rather than a gamble.

## What is still unverified

**Whether this fixes what the reviewer heard.** I measured that the seed fixes
duration and that rate spread is 10%. I cannot hear the output, so whether the
*timbre* variation is gone is not something I can check.

If it still sounds uneven, the next lever is the model rather than more parameter
tuning. `eleven_turbo_v2_5` was chosen for its rate, 157.5 wpm at speed 0.9, and
the reviewer separately noticed a turbo sample sounding lower quality than a
multilingual one. `eleven_multilingual_v2` at speed 1.0 measures 170 wpm on the
same lines, which is 8% faster and the wrong direction for a second-language
room, but the quality trade may be worth it. Samples of both on identical lines
are in `~/Downloads/PRONUNCIATION_TEST_2026-09-17/` as `turbo_0.9_*` and
`multi_1.0_*`.

## Pronunciation, settled

`isolits` and `snips` were confirmed correct on review, against a reference
recording of "aggregates" in the same sentence frame. Both are carried as
`say_as` entries, so the captions read "isolates" and "SNPs" while the engine
gets the respellings.
