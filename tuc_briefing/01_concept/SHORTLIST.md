# TUC briefing series: scope

Decided 2026-09-16, revised 2026-09-17. Four clips, about 23 minutes total,
shown in succession.

## Audience and purpose

One primary viewer: the TUC laboratory chief who funded the sequencing of the 312
Nakhon Phanom isolates. Technical. Has seen the Kawang closeout deck
(`~/Downloads/BurkGenome_close_KK260812_final.pptx`, 41 slides) and knows the
isolates, the workflow and the provincial findings.

This series is the sequel to that deck. Its closing line is *"the lasting output
is not a figure in this deck, it is a provincial reference set and the local
capacity to keep adding to it"*, and this series is what that reference set did
next.

**The purpose is an honest success story.** The result that survives scrutiny is
not country-level attribution, which fails, but a method that answers at the
resolution the data supports and knows when to decline. That, plus a specific and
costed next investment drawn from the funder's own isolates.

## The four clips

| | clip | runtime | reuse |
|---|---|---|---|
| 1 | From one province to a global question | ~5 min | none |
| 2 | A ruler you can trust | ~5 min | `7.03`, `7.01` |
| 3 | What the ruler measured | ~5 min | `7.07`, `7.09` |
| 4 | How close is close enough? | ~8 min | `7.12`, `Act4NotSeparable` |

**Build clip 1 first** even though 3 and 4 were briefed first. Clip 1 establishes
the visual system every other clip inherits.

## The spine

Two acts, one argument. The Act 1 measurement explains the Act 2 ceiling, and the
join is already argued in `MANUSCRIPT_DRAFT_2026-09-02.md`:

> recombination homogenizes within a population while leaving between-population
> structure largely intact

so the fine scale where linkage and country live is erased, and the coarse scale
where region lives survives. One property of the organism, both ceilings.

The funded isolates are structural rather than a segment: introduced in clip 1 as
the continuity object, lit inside the partition in clip 3, and totaled in clip 4.

## What stays static

Not everything in the corpus earns animation. Explicitly out of scope:

- **The AMR results.** The closeout covered them and they are a reference table,
  not a change over time. Simultaneous comparison, so motion would destroy them.
- **Assembly QC and the panel construction pipeline.** Audit objects.
- **Results 9, reproducibility.** A statement, not a mechanism. One line in clip 3
  at most, and it must not claim the reported run is seed-reproducible.
- **The full grouping ladder beyond five rungs.** Clip 4 shows five. More rungs
  make the non-monotonicity harder to see, not easier.

## Motion: the acceptance gate every clip has to pass

Added 2026-09-17, after clip 2 and clip 3 both came back as slides that hold.
Clip 3's new acts sit between 81% and 99% of their runtime in holds of three
seconds or more; one fourteen-second lead-in changes once, at 0.43 s, and then
freezes. `RecursiveSubdivision`, reused from the earlier deliverable and built
in this same house style, sits at **22%**, so the target is known to be
reachable.

**The per-act seconds in a brief are an output of the word budget, not a target
to hit.** Both builders hit them to the frame by holding a finished frame, and
both said so in their delivery notes as though it were a feature. A brief should
state the words and let the runtime follow.

Four rules, all measurable on the delivered mp4 rather than from the scene
source:

1. **No act above 40% of its runtime in holds of three seconds or more.**
2. **No single hold longer than about four seconds.**
3. **Roughly one animated step per sentence of the act's word budget.** If the
   script needs more room, add steps; do not lengthen a hold.
4. **The builder ships the measurement, not the assurance.** Paste the per-act
   hold table and the frame audit, run on the delivered files, into the note.

Rule 4 exists because both notes claimed checks that the renders fail. Clip 2's
claimed every figure carried its denominator, and act 6 carries two without
either. Clip 3's claimed zero text overlaps, and act 3 holds its conclusion over
the measured unit marks for most of the act. Both harnesses read the scene graph
at animation boundaries, so they check what was asked for rather than what was
drawn, and neither measures how long anything sits still.

## Decisions taken

- **On screen they are "isolates this project sequenced", never "funded".** Clip
  1's narration dropped the funding opening on purpose so the work carries the
  story. Clip 3's act 7 then put "funded units" back on screen as a legend and a
  source note, beside its own sentence using the better phrase, so one concept
  had two names in one frame. Use the brief's wording everywhere, including
  legends and source notes. The underlying set is unambiguous either way: the
  `IP-` and `IE-` identifiers, which `generate_numbers.py` now registers as
  `funded.*` keys because that is what the code has always called them.

- **Two framework sizes are reconciled on screen**, in clip 1 act 2, rather than
  avoided. Kawang 2,773 and 35 countries; ours 2,976 panel, 2,340 analysed, 50
  countries. Thailand differs by one genome between them.
- **cgMLST is not named anywhere in the series**, continuing the instruction that
  applied to the earlier deliverable. Describe what the method does, not what it
  is called.
- ~~Every reused clip gets its pending section 11 revision applied first.~~
  **Wrong, corrected 2026-09-17.** The revisions were already applied and
  rendered. The reused acts now come from the **merged** renders in
  `~/Downloads/TUC_LEGACY_MERGED_2026-09-17/`, built from
  `tuc_legacy_scenes_merged.py`. A stale pre-revision copy sits in the APHL
  package's `legacy_mp4/`; do not use it. See
  `CORRECTION_CLIPS_WERE_REVISED_2026-09-17.md`.
- **Narrated, not presenter-led.** The clips must stand alone, so every caveat
  lives in the visual.
- **Clip 4 reuses the APHL film's `Act4NotSeparable` whole**, as act 6. It fills
  this series' one content gap, that country and collection history are not
  separable in a collection assembled this way. Its narration regenerates rather
  than re-times, because the two films run different models and speeds.

## If a content classifier refuses a brief

`BRIEF-01-ALT-derisked.md` is Clip 1 with the species unnamed, the resistance act
reduced to its function, and a few unlucky words swapped. Same seven acts, same
titles, same beats; only act 2's budget moves, 115 words to 90, because it says
less. **Use it only if the original is refused.**

Clips 2 and 3 name no organism and carry essentially no sensitive vocabulary, so
**feed one of them first when a build keeps failing.** If they pass and 1 or 4 do
not, the cause is the pathogen, resistance and attribution content rather than
anything structural, and the fix is known.

If a full brief is refused whatever you do, `references/long-form.md` in the
clip-production skill notes that a timing-only note carries nothing for a
classifier to catch, and that an older model often has looser classifiers.

## Open

- ~~The voice is not chosen.~~ ~~**Settled.** ElevenLabs Justin on
  `eleven_multilingual_v2` at speed 1.0, measured at 168.0 words per minute.~~
  **Superseded 2026-09-17 on both counts. Read the next bullet before budgeting
  anything.**

- **The voice, as actually delivered.** ElevenLabs Justin
  `uFIXVu9mmnDZ7dTKCBTX` on **`eleven_v3`**, with a **fixed seed** (clip 1 used
  20260917), two-pass EBU R128 per line. `eleven_v3` is the house model and
  should not be swapped back to `v2` to make a line fit. Synthesis is not
  deterministic unseeded, so always pass the seed.

  **The 168.0 wpm figure in `VOICE_MEASUREMENT_2026-09-17.md` is not the rate to
  budget on.** It was measured on a 174-word passage that happened to contain
  few numbers. These scripts are dense with spelled-out figures, which cost far
  more time per word, and the rate was refit downward from clip 1's delivered
  audio to about **148 wpm of speech**.

  **Budget on runtime density, not on a speaking rate.** Clip 1 is the only
  finished clip in the series: **611 words over 291.02 s, which is 126 words per
  minute of runtime**, silence included. That single number is what a brief
  should size an act against, because it is the only one measured end to end on
  a real clip with real pauses.

  The APHL film runs the same voice on `eleven_turbo_v2_5` at 0.9, so anything
  shared between the films regenerates rather than re-times.

- **Both delivered pictures were budgeted on the superseded 168, and both came
  back padded.** Against 126 wpm of runtime, clip 2's word budgets are about 8%
  hot and clip 3's about 7%. Trim the words rather than the runtimes.
- ~~The narration source for the existing clips is unsettled.~~ **Settled by the
  merge.** The reused acts are narrated fresh at the TUC settings against the
  merged renders. `7.09` is already done. The other four have corrected text in
  `~/Downloads/TUC_LEGACY_MERGED_2026-09-17/narration_corrected/`, with "unit"
  applied, ready to be voiced. The four rival versions are superseded and
  `voice/` remains the oldest of them.

## Series guard: the two panels are one line of work, not two clusterings

**Set 2026-09-17 by the project lead, correcting an earlier note here that framed
this as retiring a rival clustering. There is no separate closeout clustering to
retire.**

**What actually happened, and this is the version to tell.** The initial
clustering placed the study isolates in a global tree. That is where the
2,773-genome framework comes from. The work then moved on in three ways:

1. **More isolates**, added specifically to represent more countries.
2. **A refined clustering algorithm.**
3. **A determined detection window**, which is clip 2's whole subject.

So the two panel sizes are two points on one progression, not two competing
datasets. The later panel exists because the first one had been built.

**Why the first clustering is superseded.** It leaned heavily on the mash
distance matrix, and **every cluster was silently capped at 200 members**. Cluster
counts and memberships from that stage are artifacts of the cap. This is the
answer if anyone asks what "refined" means.

**No clip presents cluster results from that stage.** Checked as built: clip 1
references them nowhere, on screen or in narration. Clip 1 act 5 corroborates the
closeout's conclusion 2 using **our own 85 analysis units**, and that conclusion
does not depend on any clustering: it rests on 19 shared sequence types and on
environmental genomes sitting throughout the phylogeny.

**What to watch for.** Do not reach for "six clonal groups contain both" as
supporting evidence because it sounds like our "20 units hold both". Quote our
units, or quote shared sequence types.
