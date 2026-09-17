# TUC clip 1 narration, voiced on eleven_v3

**Film: `~/Downloads/TUC_CLIP1_2026-09-17/final_v3/TUC_CLIP1_NARRATED_v3.mp4`**,
291.02 s. Justin, `eleven_v3`, seed 20260917, two-pass EBU R128 per line.

## Two defects found in review, both fixed

**Acts 3, 4 and 5 were rendered before the `Txt()` wrap fix and were never
re-rendered.** Animo repaired the helper and re-audited the source, reporting zero
wraps, but its own note says acts 3 to 5 were *carried over* from an earlier run.
The source was clean and the delivered files were stale, which is why act 5's
opening line still printed "among" on top of "patient". Re-rendered here from the
current source with the text cache cleared. Frame counts are identical, so no
timing moved.

**Act 5 implied a pairing that does not exist.** Corrected against the closeout
deck rather than from memory.

## What the closeout actually says about patient and environmental isolates

This is the part the narration had to get right, and it is sharper than it looked.

- The two sets are **not matched collections**. 259 clinical against 53
  environmental, and slide 20 says outright that the clinical-only count is
  inflated by sampling effort.
- A household pairing sub-study **does** exist: slide 22, nine nominated pairs
  from five patients, six evaluable after three B. thailandensis exclusions.
- **It found nothing.** Slide 23: "Household sampling did not recover the
  infecting strain", and none of the six linked patients fall inside the
  near-identical range. The deck calls this a useful negative result.
- Slide 21 makes the point directly: IE-0044 and IP-0196 are the closest
  environmental-patient pair in the whole collection, and **they are not from the
  same household**. "Proximity on the tree is not the same as a confirmed
  transmission event."

So an act that says "34 of 42 environmental isolates share a unit with a patient
isolate" without qualification does not merely overstate. Read quickly, it sounds
like it overturns their negative result. It does not, because a unit is coarse and
their test was for near-identity, but the narration has to say so.

Act 5 now carries an explicit line at 28.65 s:

> A unit is coarse. Sharing one means one population, not a link from patient to
> source.

and closes on "Same answer as the closeout, at a different scale: one population",
which is the deck's own conclusion 2 rather than a new claim.

## Still open, and worth a decision

**The two panels are one line of work, and act 3 now says so.** Corrected by the
project lead: there is no rival clustering to retire. The initial clustering placed
the study isolates in a global tree, which is where the 2,773-genome framework
comes from, and the work then added isolates to cover more countries, refined the
clustering algorithm, and determined the detection window. The two panel sizes are
two points on one progression.

Act 3 line 2 previously said the second panel "was expanded for a different
question", which named only one of the three changes. It now reads:

> That is one line of work, not two datasets. The panel grew to cover more
> countries, and the clustering was refined.

If anyone asks what "refined" means: the first clustering leaned heavily on the
mash distance matrix with every cluster silently capped at 200 members, so counts
and memberships from that stage are artifacts of the cap. No clip presents them,
and nothing load-bearing depends on them. Full note in
`tuc_briefing/02_review/QA-two-panels-explained.md`.

**The household negative result is already in clip 4, and has been strengthened.**
An earlier version of this note said it was in none of the four briefs. That was
wrong: `BRIEF-04` act 2 covers the nine nominated pairs and the six evaluable ones,
and act 3 reuses `7.12` as its mechanism. What it lacked was closeout slide 21,
the sharpest item in the deck: the closest environmental-to-patient pair in the
whole collection, IE-0044 and IP-0196, same sequence type and same district, is
**not** from the same household. Added.

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

** 11.15**  That is one line of work, not two datasets. The panel grew to cover more countries, and the clustering was refined.

** 19.20**  Here is how you can tell. Count the Thai genomes in each panel: seventeen hundred fifty four, and seventeen hundred fifty three.

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

** 28.65**  A unit is coarse. Sharing one means one population, not a link from patient to source.

** 35.51**  Thirty four of the forty two environmental isolates sit in one of those mixed units.

** 40.54**  Sixteen of those twenty units sit inside the measurable range.

** 45.98**  Same answer as the closeout, at a different scale: one population.


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

**611 words**, voiced on eleven_v3.
