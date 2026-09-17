# TUC clip 1 narration, v2: one line per visible event

**Film: `~/Downloads/TUC_CLIP1_2026-09-17/final_v3/TUC_CLIP1_NARRATED_v3.mp4`**,
279.12 s. Justin, `eleven_v3`, seed 20260917, two-pass EBU R128 per line.

## What the review found, and what was actually wrong

The note was that acts 1 and 2 were "all over the place and do not hit the beats".
Measured, the line **starts** were fine: every one sat within 1.2 s of a visible
event. The real fault was **coverage**. There were 11 events and 4 lines in act 1,
and 15 events and 6 lines in act 2, so each line ran six to nine seconds across two
or three picture changes while the screen moved on underneath it.

That is the same fault as the separate note that act 2 has on-screen text nobody
mentions. One cause, two symptoms: **too few lines, each too long.**

| | before | after |
|---|---|---|
| lines | 39 | **54** |
| act 1 | 4 lines, 11 events | 7 lines |
| act 2 | 6 lines, 15 events | 10 lines |
| act 4 | 7 lines, 13 events | 10 lines |
| act 6 | 5 lines, 10 events | 9 lines |
| **events with nothing said** | **32 of 72** | **2 of 72** |

## Two picture fixes in the same pass

**The eleven-dot row overlapped the 312-mark grid.** Its left edge sat at -3.235
and the grid's right edge is -3.167, so the first of the eleven dots was drawn on
top of the grid's last column. Moved right; it clears by 0.23 now. **The collision
checker could not see this**, because it compares text against text and this was a
shape against a shape. Third blind spot found by eye, not by tooling.

**Act 3 no longer defends itself.** At the project lead's instruction the Thailand
comparison is gone: the 1,754 against 1,753 counts, the "one genome apart" span,
and the "evidence they are one collection rather than two datasets" line. The act
now states that the panel expanded and moves on. That removed 11.9 s, so act 3 is
28.1 s rather than 40.0 and **the clip is 279.12 s rather than 291.02.**

## Rate is per-act, not per-voice

Two acts had to be rebalanced after hearing them, because the engine does not read
at one rate. Act 2 came back at **153 wpm** and act 6 at **195**, against a planned
179. Act 2's numbers are the cause: "two hundred nineteen of three hundred twelve"
costs far more time per word than prose.

At the planned rate act 2 landed at 6.8% silence, under the 10% floor, and act 6 at
36.9%, over the 35% ceiling. Fourteen words came out of act 2 and nineteen went
into act 6. **All seven acts are now inside the band**, 14.7% to 34.5%.

## Checks on the finished audio

- All 54 lines fit. No boundary under 0.29 s.
- Every line audibly present: 66% speech minimum in its own window, 94% median.
- Loudness spread 1.3 LU across all 54.
- All seven acts clean on the four collision checks after the source edits.

## Lines as heard


### Act 1. What this project built

**  0.70**  Three hundred twenty six isolates were sequenced, and three hundred twelve confirmed.

**  6.10**  Two hundred fifty nine from patients, fifty three from the environment.

** 10.90**  Three findings carried forward. The population there is extraordinarily diverse.

** 16.16**  Clinical and environmental isolates are drawn from one population.

** 20.38**  And the third, which this series is about.

** 23.08**  A shared sequence type is not enough to claim a link.

** 28.00**  Attribution needs core-genome distance. All of it from one province.


### Act 2. Resistance, asked and closed

**  0.50**  Emerging resistance was one of the things this sequencing was meant to find.

**  5.30**  No acquired resistance genes were detected.

**  8.50**  What is present is intrinsic to the species.

** 12.90**  Two hundred nineteen of three hundred twelve carry no determinant, seventy percent.

** 18.70**  First line therapy is unaffected. Ceftazidime and trimethoprim: two hundred fifty three susceptible of two hundred fifty eight.

** 26.84**  That leaves one loose end, and it is already scheduled.

** 30.35**  Eleven isolates were non-susceptible in the laboratory with no matching determinant in the genome.

** 36.09**  They get repeat testing, with MIC determination, in the next phase.

** 40.39**  Two isolates carry the only quinolone determinant found.

** 44.05**  The province has a baseline now. Resistance: asked, answered, set aside.


### Act 3. Two frameworks, one collection

**  1.00**  These genomes have been placed in a global panel twice.

**  4.65**  The closeout used two thousand seven hundred seventy three.

**  8.31**  This work uses two thousand nine hundred seventy six.

** 12.05**  The panel was expanded to cover more countries, and the clustering was refined.

** 19.18**  Of those, two thousand three hundred forty enter analysis.

** 23.24**  A unit needs a minimum size, which leaves eighty five analysis units.


### Act 4. Where the 312 went

**  2.10**  The partition already exists, built from two thousand three hundred forty genomes.

**  7.36**  Now drop the three hundred twelve into it, and watch where they land.

** 13.60**  Two hundred seventy six enter the analysed set.

** 17.89**  They land in fifty six of the eighty five units.

** 22.70**  Not a cluster, and not a corner of the tree.

** 27.40**  A provincial collection reaching across a global panel is what lets it answer questions no single province could.

** 33.73**  Thirty six did not enter.

** 36.27**  Every one has a nearest unit recorded, so none of them is lost.

** 40.36**  Their lineages are too rare in the panel for a measurable unit to form.

** 45.36**  That is a finding about the panel, not a defect in the isolates.


### Act 5. The same answer, a second time

**  2.08**  The closeout found environmental isolates scattered among patient isolates.

**  6.50**  There was no separate environmental lineage. But that was one tree, built from these three hundred twelve genomes alone.

** 16.14**  So test it again in a structure that knew nothing about which isolate came from where.

** 22.78**  Twenty of the eighty five units hold both a patient isolate and an environmental one.

** 28.65**  A unit is coarse. Sharing one means one population, not a link from patient to source.

** 35.51**  Thirty four of the forty two environmental isolates sit in one of those mixed units.

** 40.83**  Sixteen of those twenty units sit inside the measurable range.

** 45.98**  Same answer as the closeout, at a different scale: one population.


### Act 6. The question this makes askable

**  1.00**  Here is the problem this now makes it possible to ask.

**  5.20**  A patient presents with severe sepsis and no travel history at all.

**  9.69**  No exposure, no source. The genome is the only evidence of where it came from.

** 15.02**  The closeout already settled two things about that.

** 18.89**  Two isolates can share a sequence type, the same broad genetic family.

** 23.52**  Measured across the whole genome, they can still be far apart.

** 27.20**  So sharing a sequence type is not enough to answer the question.

** 31.53**  It needs distance measured across the whole core genome, not a handful of loci.

** 36.55**  So with core genomes, in a global frame, how far can you get?


### Act 7. What the rest of this takes

**  1.98**  Answering that question takes three things, in order.

**  5.80**  First, the measuring instrument has to be shown to work.

**  9.45**  Then it has to be pointed at the data.

** 13.12**  Then the answer, and just as important, the point where it stops working.


---

**619 words**, 54 lines, voiced on eleven_v3.
