# TUC clip 1 narration, voiced on eleven_v3

**Film: `~/Downloads/TUC_CLIP1_2026-09-17/final_v3/TUC_CLIP1_NARRATED_v3.mp4`**,
291.02 s, 1920x1080 60 fps. Captions in `narration_v3/`.

Justin (`uFIXVu9mmnDZ7dTKCBTX`), **`eleven_v3`**, seed 20260917, then two-pass EBU
R128 per line at I -20, TP -1.5, LRA 11.

## Why there is also a v2 cut, and why it is not the one to use

The first pass went out on `eleven_multilingual_v2`. That was a bad call, made on
the reasoning that the word budgets were fitted at a rate measured on v2 and the
models read at different speeds. The reasoning collapsed on contact with the
audio: the 168 wpm the fit was built on was wrong anyway, and once the schedule is
refitted from measured audio the model's rate stops mattering to the fit at all.
v3 was the stated preference and it should not have been quietly overridden.

The v2 cut survives at `final/` for comparison. It is not the deliverable.

## Measured, both models, same script and seed

| | v2 | v3 |
|---|---|---|
| rate, mean | 151 wpm | **179 wpm** |
| rate, per line | 106 to 206 | 127 to 293 |
| lines overrunning their slot | 14 of 39 | **3 of 39** |
| loudness spread, before normalization | 7.4 LU | **5.2 LU** |
| loudness spread, after | 0.9 LU | 1.2 LU |
| lines held on their written beat | 25 of 39 | **33 of 39** |
| real silence, whole film | **17%** | 28% |
| speech present in each line's window | 65% min, 82% median | **70% min, 91% median** |

**v3 is better on everything except silence**, and it holds far more lines on the
beat they were written for, which is what keeps the words matched to the picture.

**Its one real cost is dead air.** v3 reads about 19% faster, so the same script
leaves about eleven more points of the runtime empty. **The fix for that is more
words, not a different model.** Act 7 breached the toolchain's 35% ceiling at
37.3% and was given five more words rather than having the gate relaxed.

## The nominal rate was wrong, and it matters for clips 2 to 4

The briefs budget at 168 wpm. Neither model reads that: v2 came in at 151 and v3
at 179, with spelled-out numbers the main cause. "Two thousand nine hundred
seventy six" costs far more time per word than prose, and this script is full of
them.

**Budget clips 2 to 4 at about 179 wpm for v3**, roughly 6% more words than 168
gives for the same runtime, and expect to refit from the audio regardless.

## Checks on the finished v3 audio

- **All 39 lines fit**, measured from the audio.
- **No line boundary under 0.29 s.**
- **Every line audibly present at its cue**: 70% speech minimum inside its own
  window, 91% median, none under 30%.
- **Loudness spread 1.2 LU**, and normalization changed no duration.
- Real silence 17.6 to 33.5% per act, all inside the 10 to 35 gate.

## Lines as heard


### Act 1. What this project built

**  2.20**  Three hundred twenty six isolates were sequenced for this project, and three hundred twelve were confirmed.

**  9.10**  Two hundred fifty nine came from patients. Fifty three came from soil and water.

** 14.84**  The first two describe the population: extraordinarily diverse, and a single population.

** 21.60**  And the third, which is why this series exists. A shared sequence type is not enough to claim a link.


### Act 2. Resistance, asked and closed

**  2.20**  Emerging resistance was one of the things this sequencing was meant to find. There was none.

**  9.13**  Seventy percent carry no predicted determinant, and what is present is intrinsic to the species.

** 15.47**  First line therapy is unaffected. Ceftazidime and trimethoprim were each tested on two hundred fifty eight patient isolates, two hundred fifty three susceptible.

** 25.07**  One loose end. Eleven isolates were non-susceptible in the laboratory with nothing in the genome to explain it.

** 34.29**  Those get repeat testing, with MIC determination, in the next phase. The closeout recommended it and it is scheduled.

** 43.57**  The province has a baseline now, so a future change will be visible against it.


### Act 3. Two frameworks, one collection

**  2.10**  These genomes have been placed in a global panel twice, and the two panels are different sizes.

** 10.95**  That is one collection curated twice, not two collections. The second is larger because it was expanded for a different question.

** 19.41**  Here is how you can tell. Count the Thai genomes in each panel: seventeen hundred fifty four, and seventeen hundred fifty three.

** 27.55**  Two separately built datasets would never agree that closely.

** 31.13**  Of those, two thousand three hundred forty enter analysis, because a unit needs a minimum size. That gives eighty five units.


### Act 4. Where the 312 went

**  2.00**  The partition already exists, built from two thousand three hundred forty genomes.

**  7.77**  Now drop the three hundred twelve into it, and watch where they land.

** 13.60**  Two hundred seventy six enter the analysed set.

** 18.03**  They land in fifty six of the eighty five units. Not a cluster, and not a corner of the tree.

** 27.45**  A provincial collection reaching across a global panel is what lets it answer questions no single province could.

** 34.79**  Thirty six did not enter. Every one has a nearest unit recorded, so none of them is lost.

** 44.20**  Their lineages are too rare in the panel for a measurable unit to form. That is a finding about the panel.


### Act 5. The same answer, a second time

**  2.08**  The closeout found environmental isolates scattered among patient isolates.

**  6.50**  There was no separate environmental lineage. But that was one tree, built from these three hundred twelve genomes alone.

** 16.14**  So test it again in a structure that knew nothing about which isolate came from where.

** 22.78**  Twenty of the eighty five units hold both a patient isolate and an environmental one.

** 30.27**  So count the environmental isolates that share a unit with a patient isolate.

** 35.78**  Thirty four of the forty two in the analysed set.

** 40.54**  Sixteen of those twenty mixed units sit inside the measurable range.

** 46.28**  The same answer, from a different instrument, at eight times the scale.


### Act 6. The question this makes askable

**  2.29**  Here is the problem this now makes it possible to ask, and it is the applied one.

** 10.00**  A patient presents with no travel history. No exposure, no source. The genome is the only evidence of where the infection was acquired.

** 19.32**  The closeout already settled two things about that, and both still hold.

** 24.60**  Sharing a sequence type will not answer it. The question needs distance measured across the whole core genome, not a handful of loci.

** 33.36**  So, with core genomes and a global frame, the question becomes how far you can actually get.


### Act 7. What the rest of this takes

**  1.98**  Answering that question takes three things, in order.

**  5.80**  First, the measuring instrument has to be shown to work.

**  9.42**  Then it has to be pointed at the data.

** 13.12**  Then the answer, and just as important, the point where it stops working.


---

**605 words**, voiced on eleven_v3.
