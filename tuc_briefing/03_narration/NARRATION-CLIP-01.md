# TUC clip 1 narration, voiced

Voiced 2026-09-17. Film: `~/Downloads/TUC_CLIP1_2026-09-17/final/TUC_CLIP1_NARRATED.mp4`,
291.02 s, 1920x1080 60 fps, AAC 48 kHz. Captions in `narration_final/`.

Justin (`uFIXVu9mmnDZ7dTKCBTX`), `eleven_multilingual_v2`, **seed 20260917**, then
two-pass EBU R128 per line at I -20, TP -1.5, LRA 11.

## The nominal rate was wrong, and it matters for clips 2 to 4

The briefs budget words at **168 wpm**. The engine actually read this script at
**141 to 157 wpm per act**, mean about 148, with a per-line spread of **106 to 206
wpm**. Spelled-out numbers are the cause: "two thousand nine hundred seventy six"
costs far more time per word than prose, and this script is full of them.

Fifteen of the 39 lines overran their slot as a result. They were not rewritten;
the schedule was refitted to the audio with `retime_from_audio.py`, which exists
for exactly this. Only one line was rewritten, act 1 line 3, because refitting it
alone would have pushed the next line past the picture it describes.

**Clips 2 to 4 should budget at about 148 wpm, not 168**, roughly 12% fewer words
for the same runtime.

## Checks that ran on the finished audio

- **All 39 lines fit**, measured from the audio rather than predicted.
- **Real silence 12.6 to 22.7% per act**, measured, against 26% predicted.
- **Every line is audibly present at its cue.** Minimum 65% speech inside its own
  window, median 82%. An earlier version of this check asked whether the midpoint
  was silent and flagged five lines; that was wrong, because any line with a
  sentence break has a pause in the middle.
- **Loudness spread 7.4 LU to 0.9 LU**, and no line changed duration by a
  millisecond.
- **Twelve line boundaries sit at exactly the 0.30 s floor.** That is the retimer
  packing to the minimum we set, not a fault, but the schedule is tight.

## Lines as heard, with final timings


### Act 1. What this project built

**  2.20**  Three hundred twenty six isolates were sequenced for this project, and three hundred twelve were confirmed.

**  9.10**  Two hundred fifty nine came from patients. Fifty three came from soil and water.

** 15.29**  The first two describe the population: extraordinarily diverse, and a single population.

** 22.28**  And the third, which is why this series exists. A shared sequence type is not enough to claim a link.


### Act 2. Resistance, asked and closed

**  2.20**  Emerging resistance was one of the things this sequencing was meant to find. There was none.

**  9.13**  Seventy percent carry no predicted determinant, and what is present is intrinsic to the species.

** 16.39**  First line therapy is unaffected. Ceftazidime and trimethoprim were each tested on two hundred fifty eight patient isolates, two hundred fifty three susceptible.

** 27.19**  One loose end. Eleven isolates were non-susceptible in the laboratory with nothing in the genome to explain it.

** 34.36**  Those get repeat testing, with MIC determination, in the next phase. The closeout recommended it and it is scheduled.

** 44.41**  The province has a baseline now, so a future change will be visible against it.


### Act 3. Two frameworks, one collection

**  2.10**  These genomes have been placed in a global panel twice, and the two panels are different sizes.

** 10.00**  That is one collection curated twice, not two collections. The second is larger because it was expanded for a different question.

** 18.71**  Here is how you can tell. Count the Thai genomes in each panel: seventeen hundred fifty four, and seventeen hundred fifty three.

** 27.83**  Two separately built datasets would never agree that closely.

** 32.08**  Of those, two thousand three hundred forty enter analysis, because a unit needs a minimum size. That gives eighty five units.


### Act 4. Where the 312 went

**  2.00**  The partition already exists, built from two thousand three hundred forty genomes.

**  8.52**  Now drop the three hundred twelve into it, and watch where they land.

** 13.60**  Two hundred seventy six enter the analysed set.

** 18.03**  They land in fifty six of the eighty five units. Not a cluster, and not a corner of the tree.

** 27.45**  A provincial collection reaching across a global panel is what lets it answer questions no single province could.

** 34.90**  Thirty six did not enter. Every one has a nearest unit recorded, so none of them is lost.

** 44.20**  Their lineages are too rare in the panel for a measurable unit to form. That is a finding about the panel.


### Act 5. The same answer, a second time

**  2.08**  The closeout found environmental isolates scattered among patient isolates.

**  7.48**  There was no separate environmental lineage. But that was one tree, built from these three hundred twelve genomes alone.

** 16.61**  So test it again in a structure that knew nothing about which isolate came from where.

** 22.78**  Twenty of the eighty five units hold both a patient isolate and an environmental one.

** 30.27**  So count the environmental isolates that share a unit with a patient isolate.

** 35.78**  Thirty four of the forty two in the analysed set.

** 40.50**  Sixteen of those twenty mixed units sit inside the measurable range.

** 45.96**  The same answer, from a different instrument, at eight times the scale.


### Act 6. The question this makes askable

**  2.29**  Here is the problem this now makes it possible to ask, and it is the applied one.

** 10.00**  A patient presents with no travel history. No exposure, no source. The genome is the only evidence of where the infection was acquired.

** 21.07**  The closeout already settled two things about that, and both still hold.

** 26.80**  Sharing a sequence type will not answer it. The question needs distance measured across the whole core genome, not a handful of loci.

** 36.07**  So, with core genomes and a global frame, the question becomes how far you can actually get.


### Act 7. What the rest of this takes

**  1.47**  Answering that question takes three things, in order.

**  5.90**  First, the instrument has to be shown to work.

**  9.83**  Then it has to be pointed at the data.

** 13.38**  Then the answer, and just as important, where it stops.


---

**601 words.** Voiced and assembled.
