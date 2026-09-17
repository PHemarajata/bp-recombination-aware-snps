# Clip 3: What the ruler measured

Third clip of the TUC briefing series. Long-form, seven acts, built as separate
renders and concatenated. Acts 4 and 5 are existing clips, each reused **with its
already-specified revision applied** (see Reused clips below).

**The claim.** Applying the measured window turns one uninterpretable average into
a measurement and a diagnosis: inside the window the recombination-to-mutation
ratio is 7.70, outside it is 1.99, and that contrast means a low ratio is the
detector failing rather than the genome being quiet.

**The quantity that carries it.** The median r/m of a set of units, recomputed as
the set is redefined. The argument is one number moving as the population it is
computed over changes, so the quantity is a conditional median and its contrast
across classes, never a raw r/m value on its own.

Secondary quantity, act 6: the same median recomputed at four different window
floors, which is a sensitivity, not a result.

**Why motion.** The naive number and the correct number are the same arithmetic on
different sets. A still can show 5.51 or it can show 7.70, but only motion shows
that the second came out of the first by removing units where the instrument was
out of range. The viewer has to watch the set change to believe the number did.

---

## Source and data

All measured. Nothing in this clip is illustrative except the two reused clips'
schematic curves, which are labeled as such in their own frames.

| value | source |
|---|---|
| Unit counts, class medians, IQR | `TABLES.md` Table 2; `NUMBERS.tsv` `rm.*` |
| Window bounds and their brackets | `NUMBERS.tsv` `rm.gate1_floor`, `rm.gate1_ceiling` |
| Floor sensitivity | `NUMBERS.tsv` `rm.floor_sensitivity` |
| Subdivision example | `TABLES.md` Table 3 |
| Tree-builder comparison | `TABLES.md` Table 5; `TREEBUILDER_EQ_RESULT.txt`, `RAPIDNJ_EQ_RESULT.txt`, twelve rows each |
| Funded isolate accounting | `FINAL_BASIS_2026-08-22/` joined to `GATE1_ALIGNMENT_2026-08-21.tsv` |

---

## The seven acts

One render per act. Each names its entry and exit state; the exit of act N is the
entry of act N+1. Word budgets are spoken words; runtime follows from word count
at the chosen voice's measured rate, not from the seconds below, which assume 132
words per minute with a fifth of the act silent.

**Continuity object: the 85 analysis units.** They arrive in act 1 as 85
undifferentiated marks and stay on screen, in the same style, for the whole clip.
Act 2 classifies them, act 3 reads the classes back, acts 4 and 5 show two ways a
mark can move without anyone noticing, act 6 jitters the boundary, and act 7
lights up the ones the funded isolates built. In clip 4 the continuity object
changes to the 46 validation genomes; the visual system carries across, the object
does not.

### Act 1. Eighty-five units, one ruler (~55 words, ~31 s)
*Entry:* black. *Exit:* 85 marks placed on the diversity axis, unclassified.

Recall the instrument from clip 2 in one sentence, then point it. Eighty-five
analysis units, 2,340 genomes. Each unit has a diversity and each has an r/m.
Establish that the window is about to be applied to them and that the window was
measured before any of these numbers were looked at, which is what makes this a
test rather than a selection.

### Act 2. The split, and the contrast (~115 words, ~65 s)
*Entry:* 85 unclassified marks. *Exit:* three classes, each with its median.

The central act. Show the naive number first and name it as the thing being
corrected: pooled across all 85 units the median is **5.51**, which blends real
measurements with detection failures and is not a result. Then apply the window:

| class | units | median r/m | genomes |
|---|---|---|---|
| In-window | **47** | **7.70** | 1,388 |
| Below floor | 12 | 1.32 | 349 |
| Above ceiling | 26 | 2.14 | 603 |

In-window IQR is **5.72 to 9.41**. Pooled outside the window, 38 units, the median
is **1.99**. The contrast between 7.70 and 1.99 is the whole act.

### Act 3. The reversal (~85 words, ~48 s)
*Entry:* three classes. *Exit:* the same three classes, re-read.

Nothing new appears. The same picture is read the other way round, and this is the
single most important idea in the series. A unit below the floor does not have
little recombination. It has too little diversity for the detector to find any, so
the detector returns a small number and the small number means nothing. A unit
above the ceiling has so much that the estimate collapses. **A low r/m is a
detection failure, not a quiet genome.** Say it plainly and let it sit.

### Act 4. First silent failure: a correct split that costs the measurement
*Lead-in ~25 words, ~14 s, then the revised* `7.07_recursive_subdivision` *(~35.7 s)*
*Entry:* the three classes. *Exit:* as the reused clip leaves it.

Lead-in frames why this is coming: the classes are not permanent, and a decision
taken for good reasons elsewhere in the pipeline can move a unit out of the
measurable set without anyone noticing.

### Act 5. Second silent failure: the tree builder underneath
*Lead-in ~25 words, ~14 s, then the revised* `7.09_tree_builder_paired` *(~26.6 s)*
*Entry:* as act 4 leaves it. *Exit:* the twelve comparisons resolved.

Lead-in frames the question: r/m is estimated on a tree, so does the choice of
tree builder change the answer? Maximum-likelihood builders agree with each other,
median ratio 0.988, sign test p = 0.77. The distance-based default does not:
median ratio 0.922, eleven of twelve below parity, p = 0.0063.

### Act 6. Is the window itself arbitrary? (~50 words, ~28 s)
*Entry:* twelve comparisons. *Exit:* 7.70 restated, now with its bracket.

Anticipate the obvious objection. Both bounds are brackets, not points: the floor
is bracketed to (588, 755]. Recompute the in-window median at four candidate
floors, 588, 700, 755 and 840, and it reads **7.70, 7.70, 7.74, 7.78**. The
headline does not depend on where in the bracket the floor is placed.

### Act 7. Whose measurement this is (~65 words, ~37 s)
*Entry:* 85 marks, classified. *Exit:* the funded isolates lit within them, handing
off to clip 4.

The continuity object pays off. Of the 47 in-window units, **34 contain isolates
this project sequenced**. Six of those 34 fall below the minimum analysis size
without them and would not exist as measurements at all. Their median r/m is
**7.74** against **7.70** for all in-window units, which is the point: load-bearing
and representative at the same time, not a biased corner.

---

## Reused clips: apply the pending revisions first

`7.07`, `7.09` and `7.12` all carry revisions specified in `ANIMO_BRIEF_2026-09-09.md`
section 11 on 2026-09-10, each costed as a re-render, none of which was executed.
The delivered files are the pre-revision versions. Do not drop them into a
technical briefing unrevised. Two of the three defects are exactly the kind this
audience will notice.

**`7.09`, section 11.1, the largest payoff.** It plots absolute r/m for both
builders and connects the pairs. Seven of twelve comparisons sit below r/m 5, so
the lines are short, overlapping and nearly flat, and **the finding is carried
entirely by the text caption. The picture does not show it.** Plot the ratio
instead: one dot per comparison, one reference line at 1.0, eleven dots below it
and one above. The worst case becomes the lowest dot rather than a label. Keep
both panels and the sign test annotations. Per-comparison values are on disk in
`TREEBUILDER_EQ_RESULT.txt` and `RAPIDNJ_EQ_RESULT.txt`.

**`7.07`, section 11.2.** Two fixes. The bar and the plot are two views of the same
three objects with nothing linking them until a color flip at 27 s, so drop each
bar segment onto its position on the diversity axis. And the eighteen-fold drop
from the parent at 1,310 to its own child at 72 is not drawn: on a log axis it
reads as a small step, and it is the trap this project keeps hitting. Annotate it
explicitly.

---

## What would be a fabrication

- **Presenting a below-floor or above-ceiling r/m as a low recombination rate.**
  The single forbidden reading, and act 3 exists to prevent it. Any frame showing
  1.32 or 2.14 without the reason beside it is this error.
- **Quoting 5.51 as a result.** It appears once, in act 2, labeled as the number
  being corrected, and never again.
- **Using the IQR 5.51 to 9.44.** The correct in-window IQR is 5.72 to 9.41.
- **Drawing the tree-builder comparison as two series of absolute values.** That is
  the defect being fixed. The quantity is the ratio against parity, and the claim
  is a count below a reference line.
- **Presenting the subdivision example as part of the reported basis.** Table 3's
  split comes from the cross-hardware control run. The reported basis keeps
  `strain_1_L1_26` unsplit. The clip may use it as a worked demonstration and must
  not imply the reported 85 units contain it.
- **Drawing either window bound as a precise value.** Both are brackets. Act 6
  depends on the floor being drawn as a band.
- **Implying the window was chosen after seeing the r/m values.** It was measured
  first. If the animation orders it the other way it inverts the argument.

## Two number collisions in this clip

Both are real and both would read as errors on screen.

- **7.74 appears twice for unrelated reasons.** In act 6 it is the in-window median
  at a floor of 755, a sensitivity value. In act 7 it is the median of the units
  containing funded isolates. Acts 6 and 7 are adjacent. Separate them: act 6 can
  show its four values as deviations from 7.70 rather than as absolutes.
- **47 is both a unit count and a genome count.** 47 in-window units in act 2, and
  in Table 3 the middle child of the subdivision has n = 47 in act 4. Label units
  and genomes distinctly wherever both are on screen.

## Forbidden framings

- **Never say prior studies were wrong.** One step was missing from all of it,
  including this study until it was added.
- **Never quote an r/m for a unit outside the window** as though it meant
  something.
- **Never quote the Mash proxy against the [700, 4700] window.** Different units.
  The window is alignment-derived throughout.
- **Never claim the reported run is seed-reproducible.** It ran unseeded and
  multi-threaded. The pipeline is byte-reproducible under `--deterministic true`,
  which produces a different run rather than validating the pinned one.
- **No recommended SNP threshold.** That belongs to clip 4 and is refused there
  too.
- **Writing style, hard constraint, anything on screen:** no em dashes, no en
  dashes, no semicolons, no curly quotes, American spelling, median sentence
  length about 19 words.

## Audience

As clip 4. One primary viewer, the TUC laboratory chief who funded the sequencing,
technical and familiar with the project through the Kawang closeout deck.
Phylogenetics and sequence typing are known ground. Recombination as a
population-genomic process, and r/m as a quantity, are not: clip 2 introduces
them and this clip assumes only what clip 2 established. Define nothing twice.

## Production constraints

- **1920x1080, 60 fps**, matching the existing clips. Deliver at these settings,
  not preview quality.
- **Seven separate renders, concatenated.** Acts 4 and 5 are the revised reuses.
- **Target about 5 minutes**, roughly 420 spoken words of new narration plus the
  two reused clips at 35.7 s and 26.6 s.
- **An animated step for every sentence.** Act 3 is the exception and is
  deliberately still: it re-reads act 2's picture without adding to it, and that
  stillness is the point. Budget it as narration over a held frame.
- **Title card holds 1 to 2 seconds.**
- **The bottom eighth of the frame is reserved** for captions. No axis labels, no
  legend, no source line there.
- **Narrated, not presenter-led.** Every caveat lives in the visual.
- **Voice: ElevenLabs "Justin", voice ID `uFIXVu9mmnDZ7dTKCBTX`**, the same voice
  across all four clips. Every word budget here assumes 132 words per minute,
  which is the rate the earlier narration pack was timed at and **not a measured
  property of this voice**. Measure Justin's real rate on a sample first, then
  re-derive each act's seconds from its own word count. A faster voice buys more
  words at the same length; it does not shorten the clip.
- **Two-pass render expected.** Silent preview accepted on content and layout
  only, then narration, then one timing-only lengthen note per act, then the
  delivery re-render.
- **If text is rendered with manim on Linux, guard glyph spacing** by laying out
  at a larger requested size and scaling down.

## You may refuse this brief

If the material does not support the claim or the quantity, say so and propose
what it does support. In particular, act 6 is a sensitivity analysis wearing the
clothes of a result. If it cannot be drawn so that a viewer sees "the answer does
not depend on this choice" rather than "here are four more numbers", say so and
propose something simpler, or cut it.
