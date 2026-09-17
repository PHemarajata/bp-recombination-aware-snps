# Clip 4: How close is close enough?

Fourth and final clip of the TUC briefing series. Long-form, seven acts, built as
separate renders and concatenated. Act 3 is an existing accepted clip dropped in
whole.

**The claim.** One property of this organism, its recombination load, sets the
resolution limit on every question we ask of a genome: it erases the fine scale,
where linkage and country live, and leaves the coarse scale, where region lives,
intact. So region-level origin is answerable and country-level origin is not, and
that is a measured boundary rather than a shortfall.

**The quantity that carries it.** Cohen's kappa for each rung of the grouping
ladder, read against that rung's own baseline. Kappa is the load-bearing quantity
because raw accuracy is not comparable across groupings: a two-class split with a
59% majority scores 59% while saying nothing. Every rung must show its own
baseline next to it or the comparison is meaningless.

Secondary quantity, act 5: trait association index by the scale of the trait,
which is the mechanism read directly off a phylogeny.

**Why motion.** The whole argument is a quantity changing as the question changes
scale, and the viewer has to hold the previous rung in mind to see the next one
move. A static table of five kappas invites reading the largest number and
stopping. It also lets the non-monotonic rung hide, and that rung is the honesty
of the result.

---

## Source and data

All measured. No illustrative or simulated values anywhere in this clip.

| value | source |
|---|---|
| Every attribution and ladder number | `NUMBERS.tsv` keys `attribution.*`, `ladder.*`, `validation.*`, `abstention.*` |
| Validation denominator, 46 scorable | `NUMBERS.tsv` `validation.scorable` |
| Funded isolate accounting | `FINAL_BASIS_2026-08-22/FINAL_PANEL.tsv` joined to `FINAL_PARTITION.tsv` |
| Gate 1 classes | `GATE1_ALIGNMENT_2026-08-21.tsv` |
| Association index by trait | Kawang closeout deck, slide 25, computed on the 2,773-genome framework |
| Household pair result | Kawang closeout deck, slide 23 |

**Two framework sizes appear in this series and they are different panels.**
Kawang's is 2,773 genomes and 35 countries; ours is a 2,976-genome panel of which
2,340 enter analysis across 85 units, 50 countries. Clip 1 carries the
reconciliation beat. In this clip, any value taken from the Kawang deck must be
labeled with its own framework on screen. Do not present the two as one dataset.

---

## The seven acts

Build one render per act. Each act names its entry and exit state; the exit of act
N is the entry of act N+1. Word budgets are spoken words, and each act's runtime
follows from its word count at the chosen voice's measured rate, not from the
seconds below, which are stated at Justin's measured 168 words per minute with a
fifth of the act silent.

**Continuity object: the 46 scorable validation genomes.** They appear in act 2
as an undifferentiated set and are re-asked at every scale that follows. The same
46 marks, the same style, every act. In act 7 they hand off to the 312 funded
isolates. This is the thread that makes seven renders one film.

### Act 1. Two questions, one shape (~90 words, ~40 s)
*Entry:* black. *Exit:* the two questions side by side, both unanswered.

A genome arrives and two questions get asked of it. Did this patient and this soil
sample share a source? Where was this infection acquired? They look like different
questions and they are the same question: how close is close enough to claim a
link? Establish that both will be answered, and that the answers differ.

### Act 2. The linkage scale, set up (~50 words, ~23 s)
*Entry:* the two questions. *Exit:* the near-identical distance band, empty, ready
for act 3.

The project already asked the linkage question in the field. Nine nominated
patient and environment pairs, six evaluable after the *B. thailandensis*
exclusions. None of the six linked patients fell inside the near-identical range
that genuine matches elsewhere in the collection occupy. State it as a finding,
not a disappointment.

### Act 3. Existing clip `7.12_outbreak_threshold`, revised then dropped in whole (44.9 s)
*Entry and exit as built.* Narration as delivered, do not re-author.

Explains why act 2's result was predictable: recombination is least detectable and
most consequential at exactly the tight SNP distances where linkage claims are
made. This is the mechanistic answer to the household result, and placing it
immediately after act 2 is the whole point of the reuse.

**Apply its two pending revisions first.** `ANIMO_BRIEF_2026-09-09.md` section 11.2
specified both on 2026-09-10, costed each as a re-render, and neither was
executed. The delivered file is the pre-revision version.

1. **The decision band reads as an edge case.** Zero to fifteen SNPs is where every
   outbreak call happens, and on a log axis it is a sliver at the far left. Invert
   the emphasis by dimming outside the band, or add a second panel zoomed to it.
2. **The most visually dominant object is the least real one.** The field between
   the two curves fills the frame and both curves are schematic, while the four
   published anchor points are the only measured values in the clip and arrive as
   thin dashed verticals in the last third. Render the schematic curves in a
   visibly sketchy style, reserve solid rendering for the anchors, and make the
   anchors the spine.

Do not fix the second by making the curves look more like data. They are schematic
and must stay schematic, and the on-screen label saying so stays. This is the same
rule act 6 is held to below, which is why the two acts must be styled
consistently: schematic and measured have to be distinguishable the same way in
both.

### Act 4. The geography scale, set up (~120 words, ~54 s)
*Entry:* the 46 marks arrive. *Exit:* 46 marks, each with a true exposure label.

Forty-six genomes whose exposure country is independently known, out of 48
registered: two carry a non-country exposure and cannot be scored. Explain
leave-group-out plainly: the whole outbreak or submission group is held out, not
just the one genome, because sibling isolates from the same event would otherwise
hand the answer back. State what counts as correct before any score appears.

### Act 5. The ladder (~190 words, ~85 s)
*Entry:* 46 labeled marks. *Exit:* five rungs, each with its kappa and baseline.

The core act. Five rungs, each scored on the same 46 genomes:

| rung | accuracy | baseline | kappa | estimator |
|---|---|---|---|---|
| Country, 16 classes | 22% | 26% | **0.193** | nearest neighbour |
| SEA vs non-SEA | 76% | 59% | **0.461** | modal k=20 |
| Region, 5 classes | 89% | 46% | **0.832** | modal k=20 |
| East vs West hemisphere | 96% | 63% | **0.909** | modal k=20 |
| Asia vs non-Asia | 100% | 59% | **1.000** | modal k=20 |

Three things this act must land, in order. Country scores **below its own
baseline**, so it is not a weak answer, it is no answer. Region reaches 0.832 and
Asia versus non-Asia is perfect on this set. And **the ladder does not climb
monotonically**: SEA versus non-SEA is a two-class question that scores 0.461,
well below the five-class region question. Coarser is not automatically better.

### Act 6. One mechanism, both ceilings (~170 words, ~77 s)
*Entry:* the five rungs. *Exit:* the rungs re-read as an erosion gradient.

The payoff. Recombination moves DNA between lineages within a population while
leaving between-population structure largely intact. Fine scale erased, coarse
scale preserved. One cause explains both the linkage ceiling from act 3 and the
country ceiling from act 5.

Corroboration from the Kawang framework, labeled as such: association index by
trait, region 0.193 and country 0.236 are strongly structured, while collection
decade 0.581, isolation source 0.710 and Thai province 0.721 are well mixed. Lower
means more structured. A different panel and a different method, pointing the same
way.

### Act 7. The accounting (~90 words, ~40 s)
*Entry:* the 46 marks. *Exit:* the 312, and one line about what to fund.

The continuity object hands off. 312 confirmed genomes sequenced by this project,
276 entering the analysed set, landing in 56 of 85 units and 34 of the 47
in-window units, with 10 in-window units existing only because of them and a median
r/m of 7.74 against 7.70 overall. Then the 36 that did not enter: their lineages
are too rare in the global panel for a measurable unit to form. Close on what
moves the ceiling, which is references in the right lineages, not more sequencing
volume.

Abstention belongs here, compressed to two sentences: the region rule declines
what it cannot answer and holds 94.3% selective accuracy out of sample at 76.1%
coverage. It is the difference between a method that guesses and one that knows
its own edge.

---

## What would be a fabrication

- **A monotonic staircase.** The single most likely wrong picture. Sorting the
  rungs by kappa, or drawing them as a smooth climb from country to Asia, deletes
  the SEA rung's dip, which is the result's own internal honesty check. The rungs
  are ordered by the scale of the question, never by their score.
- **Comparing a country number to a region number without both estimators
  visible.** Country's best estimator is nearest neighbour; region's is modal
  k=20. They are different estimators and the comparison is invalid without both
  named on screen. This is the trap this project guards hardest against.
- **Any accuracy shown without its baseline.** 22% against a 26% baseline is the
  finding. 22% alone reads as a weak positive.
- **A stratification shown against a different estimator than its headline.** The
  distance-stratified breakdowns exist for both estimators and must never be
  crossed.
- **Drawing the mechanism as measured.** We measured r/m. The within-versus-between
  erosion is the cited explanation for the pattern, not something this study
  quantified. Render it as an explanatory schematic and never as solidly as the
  measured rungs beside it.
- **Implying the two frameworks are one panel**, or carrying a Kawang value
  without its framework label.

## Forbidden framings

- **No country attribution is supported anywhere in this work.** The clip may
  state that country cannot be done. It may never show a worked country call as if
  it were usable.
- **No dates and no direction of spread.** Neither is supported.
- **Never say prior studies were wrong.** They did the right thing with what they
  had.
- **Never present a low r/m as a low recombination rate.** It is a detection
  failure. That reversal is act 3's premise and clip 3's conclusion.
- **Do not claim abstention rescues country.** It does not: selective accuracy
  equals the retained-majority baseline exactly, so the rule found an easier
  subset rather than a signal. If country's abstention appears at all, it appears
  as a failure.
- **Do not overclaim the restriction-modification barrier.** The manuscript's own
  caveat is that it rests on 106 strains from one restricted Asian locale and has
  not been tested globally. If act 6 names the barrier, it names the caveat.
- **Writing style, hard constraint, anything on screen:** no em dashes, no en
  dashes, no semicolons, no curly quotes, American spelling, median sentence
  length about 19 words.

## Audience

One primary viewer: the TUC laboratory chief who funded the sequencing of the 312
isolates. Technical, and familiar with this project through the Kawang closeout
deck, so *B. pseudomallei* biology, MLST, phylogenetic trees and AST are known
ground. Population genomics and recombination are not assumed. Pitch at a
scientist who will interrogate a claim rather than a general audience: define
kappa and leave-group-out, but do not explain what a phylogeny is. Assume the
Kawang deck has been seen.

## Production constraints

- **1920x1080, 60 fps**, matching the five existing clips exactly. Deliver at
  these settings, not at preview quality.
- **Seven separate renders, concatenated.** Act 3 is the existing
  `7.12_outbreak_threshold.mp4` inserted unchanged.
- **Target about 7 minutes**, roughly 840 spoken words of new narration at 168 wpm,
  plus act 3's existing 44.9 seconds. Runtime follows the narration, not the reverse.
- **An animated step for every sentence.** Not one reveal per paragraph. This is
  what keeps seven minutes honest rather than padded.
- **Title card holds 1 to 2 seconds.** Not five.
- **The bottom eighth of the frame is reserved.** No axis labels, no legend, no
  source line there. Captions are drawn in that band.
- **Narrated, not presenter-led.** It must stand alone, so every caveat lives in
  the visual.
- **Voice: ElevenLabs "Justin", `uFIXVu9mmnDZ7dTKCBTX`, at default speed**, the
  same voice across all four clips. **Measured at 168.0 words per minute** on
  act-length passages, with only a 2.5% penalty on number-dense text
  (`VOICE_MEASUREMENT_2026-09-17.md`). Every word budget below is stated at that
  measured rate with a fifth of each act silent. Re-measure if the voice, the
  model or the speed changes, because any of the three moves every runtime
  downstream.
- **Two-pass render expected.** Silent preview at reading pace first, accepted on
  content and layout only. Narration written to each act's word budget, voice
  generated and measured, then one timing-only lengthen note per act, then the
  delivery re-render.
- **If text is rendered with manim on Linux, guard glyph spacing** by laying out
  at a larger requested size and scaling down.

## You may refuse this brief

If the material does not support the claim or the quantity, say so and propose
what it does support. In particular: if act 6's mechanism cannot be drawn without
implying we measured the erosion, say so and propose a weaker framing. An honest
schematic labeled as one is better than a picture that quietly promotes a citation
to a result.
