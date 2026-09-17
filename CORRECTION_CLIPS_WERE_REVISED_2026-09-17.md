# Correction: the delivered clips were revised. I said they were not.

Established 2026-09-17, while starting the legacy merge. **This supersedes the
claim, made in several documents and in project memory, that all five delivered
clips are pre-revision.** They are not. The section 11 revisions were applied to
the source and rendered the same day the brief was written.

## What is actually true

There are **two sets** of the five legacy clips, and they are different files.

| set | location | timestamp | state |
|---|---|---|---|
| A | `~/Downloads/ANIMO_DELIVERABLES_2026-09-09/video/` | 2026-09-10 **16:36** | **revised** |
| B | `~/.agi/renders/36e4638f-.../legacy_mp4/` | 2026-09-10 **13:51** | pre-revision |

`~/Downloads/ANIMO_DELIVERABLES_2026-09-09/source/scene.py` is timestamped 16:36,
the same minute as set A, and every one of its five scene sections carries a
`REVISED` header listing exactly the section 11 fixes.

Evidence, not inference:

- **7.09 plots the ratio.** One dot per comparison, a reference line at 1.0, both
  panels, the sign test annotated. That *is* section 11.1's fix, on screen.
- **Rendering `TreeBuilderPaired` from that source here** produced 1596 frames at
  26.600 s, matching set A exactly. Set B is 1608 frames at 26.800 s.
- **7.03, 7.07 and 7.09 differ in frame count** between the sets.
- **7.01 and 7.12 match in frame count but differ in content**, mean pixel
  difference 3 to 10 across four sampled timestamps each. A revision that adds an
  inset or restyles a curve changes the picture without changing the timing,
  which is exactly what those two were asked to do.

## How I got it wrong

I read `ANIMO_BRIEF_2026-09-09.md` section 11, saw each revision specified and
costed as a re-render, and concluded that none had been executed. I never checked
whether the source or the clips had moved **after** that brief was written. They
had, within hours.

The confirming evidence I cited was real but misattributed. The beat map showing
`7.09` with three moments and 78% of its runtime still is a property of the
*revised* clip too: the ratio plot draws quickly and then holds. I read a true
measurement as proof of a false claim.

**This is the failure this project names in its own README:** never infer from a
summary line, check per-item values. A brief describing what should be fixed is
not evidence about what was fixed.

## What survives, and it is worse than I described

The `7.09` defect is real and still live, with a different cause.

**The picture was revised. The narration was not.** The delivered narration says:

> Lines scatter both ways. No directional bias.
> Almost every line falls. That is systematic.

The delivered picture shows **dots against a reference line**. There are no lines
to scatter and none to fall. Someone re-rendered the clip and did not update the
script, so the shipped narration is factually wrong about its own picture.

That is a harder failure than "the revision was never applied", because nothing
flags it: the clip renders, the narration builds, the fit check passes, and the
words describe a picture that no longer exists.

The other four need checking for the same class of gap rather than contradiction,
for example whether `7.03`'s new hide-the-outline beat has a line pointing at it.

## What this changes

**The legacy merge is much smaller than specified.** `ANIMO_MERGE_SPEC_2026-09-17.md`
section 4, "fold in the pending section 11 revisions", is **already done** for all
five clips. What remains of the merge is the part that was always separate:

- the four semantic divergences, purple, rust, axis and nomenclature
- the em dash sweep
- adopting `aphl_common.py` as the single token module

**Use set A, never set B.** The APHL package's `legacy_mp4/` is the superseded
copy and it is the one sitting inside the film package, which is how it would get
picked up by accident.

**Documents to distrust on this point** until corrected: the four TUC briefs'
"Reused clips: apply the pending revisions first" sections,
`ANIMO_MERGE_SPEC` section 4, `tuc_briefing/02_review/REVIEW-reused-clips.md`,
`FILM_SHARING_ARCHITECTURE` section 5, and `ANIMO_ACT4_REVISION` on `7.12`.
The memory entry has been rewritten.

## One thing the merge inherits

The legacy scenes seed their randomness locally, `random.Random(11)`,
`random.Random(20260909)` and `random.Random(7)`, so renders are reproducible.
Worth preserving through the merge rather than rediscovering, given this
project's history with unseeded generators.
