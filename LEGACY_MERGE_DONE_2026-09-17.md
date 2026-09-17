# The legacy merge is done, and 7.09's narration is rewritten

Executed 2026-09-17 rather than specified, because Manim 0.21.0 installs and
renders on this Mac at the exact version the package was built with.

Source: `tuc_legacy_scenes_merged.py` at the repo root.
Renders and narration: `~/Downloads/TUC_LEGACY_MERGED_2026-09-17/`.

## The merge changed 40 lines and no timing

| scene | frames, merged | frames, delivered | same |
|---|---|---|---|
| NegativeControlZoom, 7.01 | 2490 | 2490 | yes |
| DetectionWindowSweep, 7.03 | 2868 | 2868 | yes |
| RecursiveSubdivision, 7.07 | 2142 | 2142 | yes |
| TreeBuilderPaired, 7.09 | 1596 | 1596 | yes |
| OutbreakThreshold, 7.12 | 2694 | 2694 | yes |

Frame-for-frame identical in length, so **every existing narration timing
survives**. The merge is semantic only.

**Purple is reserved for geography.** Eight legacy uses were not: 7.03's mutation
bar, label and percentage, and 7.12's detection curve, label, dot and caption.
Both are a second measured or schematic quantity paired with a teal first, so
both take the second teal step `#005057`. Sampled at 7.03's flip, the two bars
read `#01A0AF` against `#005057` at different lengths, which was the one
constraint set on this change. `PURPLE` now survives only as an unused token
definition.

**Rust is reserved for an adverse outcome.** The imported tract is the subject
being detected, so its fill, stroke, label and reveal toggle move to teal. Rust
stays on `NOT MARKED`, the out-of-window dots, the below-floor and above-ceiling
medians and the measured r/m verdict.

**"group" became "unit"**, eight on-screen strings.

## Two corrections to my own spec, both from reading the source

**Divergence 3.3, adopt the house linear axis, is withdrawn.** It would have
damaged the scenes. 7.07 plots 72, 123, 1,310 and 1,477, and on a linear axis 72
and 123 collapse together at the left edge, while showing three children at those
values is the clip's entire subject. 7.12 spans four orders of magnitude. The
revision that drew the eighteen-fold drop had already weighed this and said so in
a comment I had not read: "on a log axis that reads as a small step, so it is
annotated explicitly." Annotating was right; rescaling was mine and it was wrong.

**The em dash sweep does not apply on this side.** The legacy source carries zero
em or en dashes on screen. That was only ever an APHL-side job.

## 7.09's narration, rewritten

This was the live defect: the picture was revised to a ratio plot and the
narration was not, so the shipped lines described dots as "lines" that "scatter"
and "fall".

`map_beats` finds only three moments, all before 5.8 s, because the annotation
reveals are small text that does not spike the difference trace. A half-second
sweep of frame differences found the real content timeline:

| ~time | what appears |
|---|---|
| 1.7 s | title |
| 3.1 s | subtitle |
| 5.8 s | both panels' dots draw |
| 12 to 15 s | left panel verdict, median 0.988, seven of twelve, p = 0.77 |
| 21 to 22 s | right panel verdict, median 0.922, eleven of twelve, p = 0.0063 |

The new lines, written against that:

> Does the tree underneath the estimate change the number you get?
>
> Anything below the line means that builder found less recombination than the
> same alignments gave RAxML.
>
> The two maximum likelihood builders sit astride the line, seven of twelve
> below, which is what chance looks like rather than bias.
>
> The fast distance builder sits below almost every time. That is systematic,
> not noise.

63 words, 21.87 s of speech in 26.6 s, **17.8% silence, density 142.1**, all four
lines fit. Voiced at the TUC settings, Justin on `eleven_multilingual_v2` at speed
1.0, measured at 172.8 wpm on this content.

The first draft came in at 56 words and 27.7% silence, above the band. Lines one
to three took the extra words because they had the slack. **Line four was not
re-synthesized**, because it did not change and a regenerated line comes back a
different length.

## What this does not resolve

**The shipped narration in `ANIMO_DELIVERABLES_2026-09-09/narration/` for 7.09 is
still the wrong one.** It has not been overwritten, because that pack is the
APHL-flavored delivery and this rewrite is voiced for TUC. Anyone using that pack
for 7.09 is using narration that describes a superseded picture.

## The check on the other four, done

No contradictions. Their narration is not wrong about its picture. But two things
came out of it, and the first is mine.

### The merge broke four narration lines, and it is the same class of fault

Renaming "group" to "unit" on screen desynchronised the narration, which still
says "group" four times:

| clip | line |
|---|---|
| 7.01 | "It widens until the real analysis **groups** appear." |
| 7.01 | "These are real **groups** of genomes from the collection." |
| 7.03 | "This is a real **group** from the collection. Nothing gets marked." |
| 7.07 | "This **group** sat comfortably inside the working window." |

**The delivered pack is still internally consistent**, because its clips and its
narration both say "group". The hazard is pairing the **merged** clips with the
**delivered** narration, which is exactly the accident this session keeps finding.

For the TUC series this costs nothing, since those clips get narrated fresh at
168 wpm and the new lines simply say "unit". **It is a constraint on that
narration, not a repair.** Anyone reusing the existing audio with the merged
picture has to re-record those four lines, and per the non-determinism finding a
re-recorded line comes back a different length and needs re-fitting.

### Two gaps, pre-existing, worth closing in the TUC narration

**7.03's counted-as bars have no line pointing at them.** Revision 1 promoted
them to co-star because they are recombination moving out of the numerator and
into the denominator, made visible, and the brief calls that the mechanism the
whole series rests on. The narration never mentions them. Its "hide the outline"
beat is also unnarrated, although the line "It never changes. Only the background
around it does." is the claim that beat exists to make checkable.

**7.07's eighteen-fold drop annotation has no line.** The narration says "Two of
the three fall below the floor", which is true but does not name the size of the
fall, which is the thing the revision drew.

Neither is a defect in the delivered clip. Both are lines worth writing when
these scenes are narrated for TUC.

**What remains of the merge is cosmetic**: splitting the file into the house
layout and importing `aphl_common.py` rather than carrying its own token block.
That buys consistency, not behavior.
