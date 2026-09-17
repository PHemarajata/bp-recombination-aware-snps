# Film work: what to read, in what order

Two films are in flight and the instructions for them are spread across eight
documents. This is the entry point. It is an index, not a summary: nothing here
restates content, because a second copy of a number is a second thing to drift.

Each Animo render session starts fresh, so the documents on disk are the
continuity. Read them in this order.

## The two films

| | APHL film | TUC briefing series |
|---|---|---|
| audience | APHL Global Health all-country call, many second-language listeners | one funder, technical, has seen the closeout deck |
| length | ~4 minutes, six clips, 235.0 s | ~21 minutes, four clips |
| state | picture rendered, not frozen, no narration | briefs only, nothing built |
| voice speed | Justin on `turbo_v2_5` at 0.9, 157.8 wpm | Justin on `multilingual_v2` at 1.0, 168 wpm |

They are not competing drafts. The TUC series is the long cut and the APHL film
is the short one, and after the merge they share one codebase.

## Read in this order

**1. `FILM_SHARING_ARCHITECTURE_2026-09-17.md`**
Why there is one design system and not two, and the act library that both films
draw from. Start here or nothing else has context.

**2. `ANIMO_MERGE_SPEC_2026-09-17.md`**
The biggest single item. Merges the five legacy scenes into the house tree and
closes every pending revision in the same pass. Carries the em dash table.

**3. `ANIMO_ACT4_REVISION_2026-09-17.md`**
Rebuilds APHL Act 4, which currently reports a count the manuscript declines to
report. Replaces the act rather than patching it.

**4. `VOICE_MEASUREMENT_2026-09-17.md`**
Justin measured at 168.0 wpm. Every word budget in both films was written against
132, so this changes all of them. Poses the APHL speed problem, which document 5 resolves.

**5. `ANIMO_APHL_TIGHTEN_2026-09-17.md`**
Resolves the APHL speed decision and the picture trim that follows from it. Only
affects that film. Read straight after the voice note.

**6. `tuc_briefing/02_review/REVIEW-reused-clips.md`**
Measured beats against narration for the five legacy clips. Explains why `7.09`'s
narration has to be re-authored rather than retimed.

**7. `tuc_briefing/01_concept/`**
`SHORTLIST.md` first for the scope decision, then the four briefs. Build order is
**clip 1 first**, even though clips 3 and 4 were briefed first, because clip 1
establishes the visual system the others inherit.

## Still binding from before

**`ANIMO_BRIEF_2026-09-09.md` section 11** is the source of every pending clip
revision. The merge spec folds them in, but section 11 holds the reasoning and the
beat maps.

**Its section 6, forbidden framings, still applies to both films**, with one
change: the cgMLST exclusion continues, and the Act 4 unit count is removed by
document 3 above.

## Not yet written

Narration for either film. It comes after the picture is frozen, and the picture
is being rebuilt. `7.09` needs new lines against a new beat map; the other four
legacy clips need retiming; both films need their acts written to the refit word
budgets.

## The one thing blocking everything

Steps 1 to 4 of the architecture's work order are Animo's. **Manim is not
installed on the Mac**, so nothing can be rendered or re-rendered here. The
Franklin Gothic faces are installed, so returned renders can be audited locally
with `map_beats.py` and `audit_frames.py`, and the ElevenLabs key is set, so
narration can be generated and measured here once there are frozen pictures to
write against.
