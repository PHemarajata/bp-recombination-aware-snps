# TUC clip 2 narration, voiced

**Film: `~/Downloads/TUC_CLIP2_2026-09-17/final/TUC_CLIP2_NARRATED.mp4`**,
304.32 s. Justin, `eleven_v3`, seed 20260917, two-pass EBU R128 per line.

## The pacing revision was accepted, and verified independently

Animo's revision passes the brief's own acceptance test, re-run here rather than
taken on trust. **Act 2 went from 59% frozen frame to 10%**, act 5 from 43% to 8%,
act 6 from 49% to 13%. No freeze over 6 s anywhere, every last visible change
within 4 s of its act's end.

It also got something right that the brief got wrong. **The brief's 0.05 threshold
did not say which scale it was on.** Animo worked out it was 0 to 255 rather than
0 to 1, and proved it by reproducing the brief's own baseline table to within a
frame. On a 0 to 1 scale nothing on a white slide exceeds 0.012, so the test would
have detected nothing at all.

Everything the brief constrained held: frame counts exact on all seven parts,
304.300 s total, one pixel format, and no content drift. The only string changes
are three two-line reveals split into six single-line ones, which is the requested
fix rather than new content.

## The reused clips are voiced too, and two gaps closed

`7.03` and `7.01` carry 89 s of the 304 s. Leaving them silent would have been a
third of the clip. Both are now voiced from the corrected text in
`TUC_LEGACY_MERGED_2026-09-17/narration_corrected/`, and the two gaps the clip 2
brief flagged are closed:

- **the counted-as bars**, which the brief calls the mechanism the whole series
  rests on, now have a line: "The bars show what counts as recombination, and what
  as mutation."
- **the hide-the-outline beat** now has one: "The outline is hidden. Look for the
  tract and you cannot."

Seven existing lines were lengthened slightly to bring `7.01` inside the silence
band, which it missed at 39%. No claim changed.

## Checks

- **68 lines**, all fit. One boundary at exactly 0.290 s, which is the floor, not
  under it.
- Every line audibly present: 73% speech minimum in its own window, 94% median.
- Loudness spread 2.1 LU across the 46 new lines.
- Real silence 20.9 to 31.3% across the nine parts, all inside the 10 to 35 band.

## Lines as heard


### title card

*silent, 5 s*

### 1. Why the obvious approach fails

**  1.10**  Start with the process, not the measurement.

**  4.59**  In this species DNA moves between lineages as well as down them.

**  8.98**  So when two genomes differ, that difference has two possible origins.

** 13.28**  Mutation accumulated over time.

** 15.58**  Or a block that arrived from somewhere else.

** 18.20**  The ratio between those two contributions is r over m.

** 23.30**  It is the quantity everything downstream depends on.

** 28.20**  Now the trap. You can compute one r over m for the whole species.

** 34.70**  It will return a number, and the number is meaningless.

** 39.10**  It is not shown here. Clip three shows it where it belongs.

** 43.90**  The reason is biological, and it is the next act.


### 2. Partition first, because the biology says so

**  0.80**  The reason is a barrier that exists in the biology.

**  4.45**  Consider two clades of this organism.

**  7.80**  Restriction-modification systems differ between them.

** 11.70**  They restrict which DNA a cell will accept from outside.

** 15.35**  So a block crossing between them is often stopped.

** 22.30**  It never gets the chance to recombine.

** 26.10**  That makes clades behave as functional units of genetic isolation.

** 30.60**  Not merely branches on a tree.

** 35.10**  The evidence is a hundred and six strains in one Asian locale.

** 39.20**  Whether it holds globally has not been tested.

** 42.06**  Averaging across a real barrier is not a shortcut.

** 45.96**  Partitioning first is a biological requirement, not a computational convenience.

** 50.82**  So measure r over m within each unit.


### 3. How the detector actually works (lead-in)

**  2.10**  Whether an excess of density is visible depends entirely on the background it stands out against.

**  7.76**  So the same imported block can be obvious, or invisible.

** 12.40**  It depends only on how diverse its unit happens to be.


### 3. 7.03 detection window (reused)

**  1.28**  The detector looks for a local excess of SNP density.

**  5.15**  One imported piece sits in this stretch.

**  8.19**  The bars show what counts as recombination, and what as mutation.

** 12.82**  It never changes. Only the background around it does.

** 16.48**  Below the floor there are almost no SNPs.

** 19.26**  This is a real unit from the collection. Nothing gets marked.

** 23.00**  Inside the window the piece is clearly denser, so it is found.

** 27.17**  Above the ceiling, SNPs are dense everywhere.

** 33.40**  The outline is hidden. Look for the tract and you cannot.

** 37.38**  Now it looks ordinary, and is missed.

** 40.03**  Too similar and too different both read low.

** 43.53**  Only inside the window does it mean anything.


### 4. Does it invent recombination? (lead-in)

**  1.20**  Before trusting any of it, the detector has to be shown not to find recombination where none exists.

**  9.03**  One thousand five hundred nineteen replicates across sixty two unit replicons.

** 14.13**  Twenty of them returned any call at all.


### 4. 7.01 negative control (reused)

**  1.28**  Every laboratory runs a no-template control on its assays.

**  4.93**  We ran the same idea on the recombination detector.

**  8.11**  Simulate genomes with zero recombination. Run the identical pipeline.

** 13.46**  Almost nothing came back from any of them.

** 16.00**  The largest value returned across the whole run was vanishingly small.

** 20.54**  Now watch the scale. It stays linear the whole way.

** 23.64**  It widens until the real analysis units appear.

** 26.90**  These are real units of genomes from the collection.

** 31.00**  The separation between them is over four hundred fold.

** 34.65**  So the tool is not inventing recombination where there is none.


### 5. Does it find what is really there?

**  0.90**  The other half of the control asks the opposite question.

**  4.55**  Can it find recombination that is definitely there?

**  7.57**  Implant recombination tracts of known length, taken from donors of known divergence.

** 12.99**  Then count how many come back.

** 14.90**  At a donor divergence of two in a thousand, which is what this organism actually shows, nineteen of twenty one come back.

** 22.64**  Ninety one percent.

** 24.60**  Below that, recovery falls away sharply: forty percent, and then only twenty.

** 32.10**  Above it, it stays high but does not keep climbing.

** 36.79**  So the floor of the window arrives here a second time, from a completely different direction.


### 6. What you now have

**  1.00**  So here is the finished instrument.

**  4.00**  It returns essentially nothing when there is nothing to find.

**  7.65**  It recovers nine tenths of what is really there, at the divergence this organism shows.

** 13.90**  And it works only between a measured floor and a measured ceiling.

** 18.22**  Both bounds are brackets, not points.

** 21.00**  That is what makes it a ruler.

** 24.80**  Clip three points that ruler at the data.


---

**655 words**, 68 lines, voiced on eleven_v3.
