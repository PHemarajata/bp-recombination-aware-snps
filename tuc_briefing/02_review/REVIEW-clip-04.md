# Review: TUC clip 4, "How close is close enough?"

Render **`7567b90f-ca23-49df-a89d-457b90b8aead`**, silent picture,
`TUC_CLIP4.mp4`, 476.900 s (7.95 min), 28,614 frames, 1920x1080 60/1, nine acts.

**Verdict: revise, but this is the best clip in the series by a wide margin.**
Every number on screen reproduces, including five I had to verify against the
closeout deck itself. Three findings, one of which is a genuine trap that the
delivery note walks into as well.

## Which of the three candidates this is, and why

Three clip 4 renders exist. All three are 1920x1080 60/1 and frame-exact.

| | held share, new acts | longest hold | concat | note |
|---|---|---|---|---|
| **`7567b90f`** | **37%** | 10.35 s | absolute paths, 9 parts, plus `verify.sh` | 12.5 kB |
| `07420c96` | 44% | 10.35 s | relative paths, 9 parts | 7.7 kB |
| `4bb107a2` | 83% | **31.17 s** | none recorded | 9.7 kB |

`7567b90f` wins on the metric that matters. It is a later revision of the same
work as `07420c96`: acts 2 and 8 are byte-identical between them, act 5 measures
the same, and acts 4, 7 and 9 are improved (act 7 from 43% held to 26%, act 9
from 47% to 21%). `4bb107a2` is a different, worse line of work, with a
**31-second frozen frame** in its act 9 and no concat recipe, and should be
discarded.

All three use byte-identical reused acts, and act 3 checksums identical to
`OutbreakThreshold.mp4` in `TUC_LEGACY_MERGED_2026-09-17/`, so the merged
revision was used and not the stale APHL copy.

## The numbers are the best of the series

Everything drawn reproduces. I checked the ones the note claimed and the ones it
did not.

**The ladder, all five rungs exact**, against `NUMBERS.tsv` `ladder.*`: country
0.193 (16 classes, nearest neighbour), region 0.832 (five, modal k=20),
Southeast Asia 0.461 (two, modal), East or West 0.909 (two, modal), Asia 1.000
(two, modal). Every accuracy-against-baseline pair matches too, including
country's 22% against a 26% baseline, which is the honest reason its kappa is
0.193.

**The ordering avoids the brief's single most likely fabrication.** Sorted by
kappa the rungs would climb smoothly, which is exactly the false picture the
brief warns about. Act 5 orders them by **number of classes** (16, five, two,
two, two), so Southeast Asia at 0.461 sits visibly below region at 0.832 and the
dip reads as a dip. The class counts are on screen, so the ordering principle is
legible rather than asserted.

**The estimators are never crossed.** `NUMBERS.tsv` says "NEVER compare an NN
number to a modal one". Act 5 prints the estimator under every rung name, and
the distance strata keep the same discipline: region read on modal k=20
(14/14, 8/10, 19/22, summing to the 41/46 headline), country on nearest
neighbour (2/14, 2/10, 6/22, summing to 10/46), denominators 14+10+22 = 46.

**Act 8 uses the defensible number, not the flattering one.** It draws the
out-of-sample 94.3% at 76.1% coverage, which `NUMBERS.tsv` marks as "this is the
defensible number", rather than the in-sample 94.4% at 78.3%. 35 answered, 33
correct, two wrong, 11 declined is internally consistent, and its "eight correct
answers given up" reconciles exactly with the registered `errors_avoided` of
3 of 5: of the 11 declined, eight would have been right and three wrong, and
33 + 8 = 41, 2 + 3 = 5. The threshold value is deliberately not drawn, because
it is a scheme- and panel-specific allelic distance, which is what the source
note demands.

**Act 9, recomputed independently from the frozen basis:**

| drawn | recomputed |
|---|---|
| 312 confirmed, 259 patient, 53 environment | 312 / 259 / 53 |
| 276 enter the analysed set, 36 did not | 276 / 36 |
| landing in 56 of the 85 units | 56 of 85 |
| 34 of the 47 in-window units | 34 of 47 |
| each of the 36 has a nearest unit | all 36 carry `nearest_unit` |
| median r/m 7.74 against 7.70 | 7.7394 against 7.6988 |

**Act 4's denominator is stated correctly.** "Validation set, n = 46 scorable of
48 registered" matches `validation.total` 48 and `validation.scorable` 46, and
act 5's "16 classes" matches `validation.source_countries`. The act also states
the scoring rule before any score appears, which is the right order.

**The five Kawang association indices are cited correctly.** They are registered
nowhere in the repo, so I read the closeout deck: slide 25 gives geographic
region 0.193, country 0.236, collection decade 0.581, isolation source 0.710,
Thai province 0.721, on 2,773 genomes and 35 countries, with "lower means more
strongly structured". Act 7 transcribes all of it, carries "A different panel
from ours." beside the bars, and tags the mechanism "Recombination is the cited
explanation, not a quantity this study measured."

**Layout is clean.** All seven new acts return no clipping, no overlap and no
caption-band intrusion. The rule-through-glyph class that clip 2's act 1 failed
on is absent: zero candidates across 33 sampled frames. The bottom eighth is
empty throughout.

## Finding 1. 0.193 means two different things, two acts apart, with the labels crossed

- **Act 5** draws **Country, 0.193** as a kappa. It is the clip's headline
  failure: country is not answerable.
- **Act 7** draws **Region, 0.193** as a Kawang association index, bracketed
  "strongly structured".

Both are correct and correctly sourced. That is what makes it dangerous. A
viewer who carries "0.193" out of act 5 as *the number for country, and it
fails* meets it two acts later attached to *region, and it is strongly
structured*. The labels are crossed and the valence is inverted.

The delivery note shows the confusion is live for the author too. Its act 7
rationale reads "country is strongly structured on the Kawang panel and still
scored 0.193 on ours" — putting 0.193 next to country in a sentence about the
panel where 0.193 belongs to region.

Both clip 2 and clip 3 have a written number-collision rule; clip 4's brief
should have one, and this is the collision. **Fix:** act 7's argument needs
country's 0.236, not region's 0.193, so the cleanest repair is to drop region's
bar or to move it out of the strongly-structured bracket's headline position. If
both bars must stay, print the index to a precision that does not collide.

## Finding 2. The hold claim is not true as delivered

The note says defect 1 was fixed and that "every hold is now 1.6 to 4.2 s". That
holds only for the **final** hold of each act, which is what its table reports,
and those are genuinely fixed: 1.58 to 4.50 s, down from a first pass that held
117.6 s of dead final frames across six acts. Real progress.

The interior holds were not addressed. Measured across all nine acts,
**21 holds run longer than 4.5 s**:

| act | held share | longest hold | where |
|---|---|---|---|
| 1 Questions | 58% | 6.98 s | 32.32 - 39.30 |
| 2 Linkage | 44% | 4.93 s | 18.00 - 22.93 |
| 3 Outbreak threshold, reused | 57% | 6.00 s | 32.30 - 38.30 |
| 4 Geography | 47% | **10.35 s** | 39.38 - 49.73 |
| 5 Ladder | 37% | 6.92 s | 14.70 - 21.62 |
| 6 Not separable, reused | 63% | 9.60 s | 3.40 - 13.00 |
| 7 Mechanism | 26% | 7.10 s | 67.32 - 74.42 |
| 8 Abstention | 30% | 5.27 s | 8.70 - 13.97 |
| 9 Accounting | **21%** | 4.17 s | passes both rules |

Against the gate now in `SHORTLIST.md`, the new acts sit at **37% overall, which
passes the 40% share rule**, and four of seven acts pass individually. Only act 9
passes both rules. Clip 3's new acts ran 81% to 99%, so this is a different
league, and act 9 shows the target is reachable in this style.

Act 4's 10.35 s hold is the most defensible long one, since it carries four
lines of text and the 46 marks and a viewer needs reading time. Act 1's three
holds over 4.5 s in a 45 s act are the least defensible.

## Finding 3. Act 9's grid encodes a different split from the text beneath it

The 312-dot grid is filled for the 259 patient isolates and hollow for the 53
environmental ones. That is keyed, correctly, for **1.8 s** near the start:
"259 from patients", "53 from the environment". Then the key fades and never
returns.

For the remaining ~30 s the grid does not change, while the text below it moves
through a different partition of the same 312: "276 enter the analysed set",
"landing in 56 of the 85 units", "34 of the 47 units inside the detection
window", and finally "36 did not enter."

So at the moment the act says **36 did not enter**, the screen shows **53 hollow
marks** and no key. The natural reading, that hollow means did not enter, is
wrong and off by seventeen. I counted the marks from the delivered frame to be
sure: 312 exactly, 259 filled and 53 hollow.

The consequence is that every quantity in the act — 276, 36, 56 of 85, 34 of 47,
and the inferred 10 — is carried by text, while the only picture on screen
encodes something else. **Fix:** re-encode the grid when the text moves on, so
the 36 are the marked ones, or keep the key up as long as the grid is.

## Minor

- **Titles are inconsistent within the film.** The new acts left-align per the
  style spec; the reused act 6 centres its own, and clip 1 centres too. One film
  currently contains both. The builder flagged it and it is a one-line change,
  but it should be settled for the series, not per clip.
- **No title card**, though the brief mentions a 1 to 2 s card. Flagged by the
  builder; the runtime arithmetic closes without it.
- **The five association indices should be registered.** They are verified
  against slide 25 now, so they are quotable, but they live only in a deck.
- **Word budgets are about 6% hot.** 850 words across the seven new acts over
  381 s is 134 words per minute of runtime, against the 126 clip 1 actually
  realized. Same direction and size as clips 2 and 3.
- **The note still plans pass 2 on `eleven_multilingual_v2` at 168 wpm.** Third
  clip in a row. `SHORTLIST.md` has been corrected, so the next brief out will
  not carry it.
- **Act 7 drops the deck's "(all p < 0.01)"** from the association indices.
  Arguably cleaner without it; noting it because the qualifier is in the source.
- **The closing investment is directional, not costed.** Act 9 ends on "What
  moves the ceiling is references in the right lineages, not more sequencing
  volume", which is the right and honest conclusion and matches what the
  reference-sensitivity work found. `SHORTLIST.md` asks for a "specific and
  costed next investment", and there is no cost on screen.
- **Act 6 is the holdiest part of the film** at 63%, with a 9.60 s hold. It is
  reused whole and pre-existing, so it is not clip 4's doing, but it is in the
  film.

## What the note got right that is worth keeping

This note is the model for the other two builders. It flagged its own inference
(the 10-unit figure, and the size floor it had to choose to get there, which I
reproduced), surfaced a series inconsistency it could have ignored (clip 1's
header carries 2,976 where `NUMBERS.tsv` says quote 2,959), disclosed that act
3's revisions were not re-verified, recorded nine defects it found and fixed
with the measurements that found them, and used `freezedetect` rather than
guessing. Rule 4 of the new motion gate asks builders to ship measurements
instead of assurances; this note nearly does it already.
