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

## Decisions taken

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

## Open

- ~~The voice is not chosen.~~ **Settled.** ElevenLabs Justin
  `uFIXVu9mmnDZ7dTKCBTX` on `eleven_multilingual_v2` at speed 1.0,
  **measured at 168.0 words per minute** on act-length text. Every budget in
  these briefs is stated at that rate. See `VOICE_MEASUREMENT_2026-09-17.md`.
  The APHL film runs the same voice on `eleven_turbo_v2_5` at 0.9, so anything
  shared between the films regenerates rather than re-times.
- ~~The narration source for the existing clips is unsettled.~~ **Settled by the
  merge.** The reused acts are narrated fresh at the TUC settings against the
  merged renders. `7.09` is already done. The other four have corrected text in
  `~/Downloads/TUC_LEGACY_MERGED_2026-09-17/narration_corrected/`, with "unit"
  applied, ready to be voiced. The four rival versions are superseded and
  `voice/` remains the oldest of them.
