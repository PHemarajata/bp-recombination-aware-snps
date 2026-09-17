# Clip 2: A ruler you can trust

Second clip of the TUC briefing series. Long-form, six acts, built as separate
renders and concatenated. Acts 3 and 4 are existing clips, each reused **with its
already-specified revision applied** (see Reused clips below).

**The claim.** Recombination detection in this organism only works over a bounded
range of population diversity, so the range was measured rather than assumed, and
the detector was then shown both to invent nothing and to recover what is really
there.

**The quantity that carries it.** Detection efficiency as a function of donor
divergence: the share of implanted recombination tracts the detector recovers,
against a false positive rate from a population where the true answer is zero. The
claim is about an instrument's operating range, so the quantity is a recovery
share across a swept parameter, never a single accuracy figure.

**Why motion.** An operating range is a property that only exists across a sweep.
Any single frame shows the detector working or failing and implies that is what it
does. The viewer has to watch the same detector, unchanged, succeed and then fail
as the population around it changes.

---

## Source and data

Measured except where noted. The two reused clips contain schematic curves that
are labeled as schematic in their own frames, and that distinction must be styled
the same way here.

| value | source |
|---|---|
| Negative control constants | `NUMBERS.tsv`; 1,519 replicates over 62 unit-replicons |
| Spike-in recovery | `TABLES.md` Table 4 |
| Window bounds and brackets | `NUMBERS.tsv` `rm.gate1_floor`, `rm.gate1_ceiling` |
| Clade barriers and partitioning rationale | `MANUSCRIPT_DRAFT_2026-09-02.md` Discussion |

**`TIER2_null.txt` is a mid-run snapshot and must not be summarized.** It reports
1,302 replicates over 54 unit-replicons. The completed run is **1,519 over 62**.
Use the constants.

---

## The six acts

One render per act. Each names its entry and exit state. Word budgets are spoken
words; runtime follows from word count at the chosen voice's measured rate.

**Continuity object: the diversity axis and the working window band on it.** The
axis is drawn in act 2 and never leaves. Every subsequent act places something on
it: the detector's behavior in act 3, the null in act 4, the recovery sweep in act
5. Both reused clips already live on this axis, which is why it is the right
object. In clip 3 the 85 units are placed on the same axis, so it carries across.

### Act 1. Why the obvious approach fails (~110 words, ~48 s)
*Entry:* clip 1's closing question. *Exit:* r/m defined, and one number refused.

Establish the process before the measurement. In this species DNA moves between
lineages, so two genomes can differ because of accumulated point mutation or
because a block arrived from elsewhere. The ratio between those two contributions
is r/m, and it is the quantity everything downstream depends on.

Then the trap. Computing one r/m for the species returns a number, and the number
is meaningless. Do not show its value here. Clip 3 shows the naive number in its
proper place, as the thing being corrected.

### Act 2. Partition first, because the biology says so (~120 words, ~54 s)
*Entry:* r/m defined. *Exit:* the diversity axis drawn, window not yet placed.

This is the act that most needs to land and is most often heard as a technicality.
It is not one. Clade-specific restriction-modification systems restrict DNA uptake
between clades, so genomic clades behave as functional units of genetic isolation.
A species-wide average would average across barriers that exist in nature.
Partitioning before measuring is therefore a biological requirement, not a
computational convenience.

State the caveat in the same breath: that result comes from 106 strains in one
restricted Asian locale, and whether it holds globally has not been tested.

### Act 3. How the detector actually works
*Lead-in ~40 words, ~17 s, then the revised* `7.03_detection_window` *(47.8 s)*
*Entry:* the diversity axis. *Exit:* three anchor units placed, window visible.

Lead-in sets up what to watch: the detector looks for a local excess of SNP
density, and whether that excess is visible depends entirely on how diverse the
background is.

### Act 4. Does it invent recombination?
*Lead-in ~40 words, ~17 s, then the revised* `7.01_negative_control` *(41.5 s)*
*Entry:* as act 3 leaves it. *Exit:* the null and the real units, separated.

Lead-in frames it as the control any laboratory would demand: run the identical
pipeline on populations simulated with zero recombination and see what comes back.
1,519 replicates over 62 unit-replicons, 20 returning any call at all.

### Act 5. Does it find what is really there? (~100 words, ~45 s)
*Entry:* the null result. *Exit:* the recovery sweep complete.

The other half of the control, and the half the earlier deliverable never had a
clip for. Implant recombination tracts of known length from donors of known
divergence, then ask how many come back:

| donor divergence | SNPs per 5 kb tract | recovered |
|---|---|---|
| 0.0005 | 2.4 | 4 of 20, 20% |
| 0.001 | 4.2 | 8 of 20, 40% |
| **0.002, the measured value** | **9.0** | **19 of 21, 91%** |
| 0.005 | 25.0 | 19 of 19, 100% |
| 0.01 | 45.0 | 19 of 21, 90% |

At the divergence this organism actually shows, recovery is 91%. Below it,
detection falls away, which is the floor of the window arriving from a second
direction.

### Act 6. What you now have (~65 words, ~29 s)
*Entry:* the sweep. *Exit:* the window with both bounds, handing off to clip 3.

Close the instrument. A detector that returns essentially nothing when there is
nothing, recovers nine tenths of what is there at the relevant divergence, and
works only between a measured floor and a measured ceiling. Both bounds are
brackets rather than points. That is a ruler, and clip 3 points it at the data.

---

## Reused acts: use the merged renders

**Both revisions are already applied.** `ANIMO_BRIEF_2026-09-09.md` section 11.2
specified them and they were rendered on 2026-09-10, so the clips are the revised
set. This brief previously said otherwise; see
`CORRECTION_CLIPS_WERE_REVISED_2026-09-17.md`.

**Use the merged renders, not the delivered clips.**

| act | file |
|---|---|
| 3 | `~/Downloads/TUC_LEGACY_MERGED_2026-09-17/DetectionWindowSweep.mp4`, 47.8 s |
| 4 | `~/Downloads/TUC_LEGACY_MERGED_2026-09-17/NegativeControlZoom.mp4`, 41.5 s |

Source: `tuc_legacy_scenes_merged.py` at the repo root. The merge is semantic
only, so both render frame-for-frame identical in length to the delivered clips.
It reserves purple for geography, reserves rust for adverse outcomes, and renames
"group" to "unit" on screen. **There is a stale copy** of both clips in the APHL
package's `legacy_mp4/`, which is the pre-revision 13:51 set. Do not use it.

**One gap to close when these are narrated.** `7.03`'s counted-as bars have no
narration line pointing at them, and the brief that promoted them calls that beat
the mechanism the whole series rests on. Its hide-the-outline beat is unnarrated
too, although the existing line "It never changes. Only the background around it
does." is the claim that beat exists to make checkable. Write lines for both.

## What would be a fabrication

- **Drawing the spike-in recovery as a smooth rising curve.** It is not monotonic:
  recovery is 100% at 0.005 and 90% at 0.01, because a tract carrying 45 SNPs can
  be split into two called blocks with neither covering half of it. A fitted curve
  through these five points asserts a relationship the data does not have.
- **Showing a species-wide r/m value in act 1.** The act's point is that the
  number should not be computed. Showing it undercuts that and pre-empts clip 3.
- **Drawing either window bound as a precise value.** Both are brackets.
- **Rendering the reused clips' schematic curves as solidly as measured values.**
  This is `7.12`'s revision 2 applied here as a house rule: schematic and measured
  must be distinguishable at a glance, the same way, in every clip.
- **Presenting the restriction-modification barrier as established globally.** The
  manuscript's own caveat is 106 strains in one restricted Asian locale.
- **Implying the window was derived from the negative control alone.** The floor is
  located by two independent lines of evidence, the spike-in sweep and the coverage
  and tract-length bands. Act 5 is the second one, not a restatement of act 4.

## Forbidden framings

- **Never present a low r/m as a low recombination rate.** Clip 3 makes this
  explicit, but acts 3 and 6 here set it up and must not contradict it.
- **Never say prior studies were wrong.** They did the right thing with what they
  had. One step was missing from all of it, including this study until it was
  added.
- **Never quote the Mash proxy against the [700, 4700] window.** The window is
  alignment-derived throughout.
- **Never claim the reported run is seed-reproducible.** It ran unseeded and
  multi-threaded.
- **Do not name cgMLST.** Excluded from this series by instruction.
- **Writing style, hard constraint, anything on screen:** no em dashes, no en
  dashes, no semicolons, no curly quotes, American spelling, median sentence
  length about 19 words.

## Number collision in this clip

**Two different 91%-shaped quantities sit two acts apart.** Act 5's headline
recovery is 91% at the measured divergence. Act 4's negative control reports 1.32%
of replicates returning any call, and its separation figures run 427-fold to
2,234-fold. None of these is a percentage of the same thing. Label each with its
denominator on screen, every time, and never place a recovery share and a false
positive rate in the same frame without both denominators visible.

## Audience

As clip 1. Technical, familiar with the project and with phylogenetics through the
closeout deck. This is the clip where the genuinely new concepts arrive:
recombination as a population-genomic process, r/m as a ratio, and detection as
something with an operating range. Define each once, carefully, and assume
nothing about population genetics beyond what a bench scientist with a genomics
background would carry. Clips 3 and 4 assume everything this clip establishes and
define none of it again.

## Production constraints

- **1920x1080, 60 fps**, matching the existing clips.
- **Six separate renders, concatenated.** Acts 3 and 4 are the revised reuses.
- **Target about 5 minutes**, roughly 470 spoken words of new narration at 168 wpm,
  plus the two reused clips at 47.8 s and 41.5 s.
- **An animated step for every sentence.**
- **Title card holds 1 to 2 seconds.**
- **The bottom eighth of the frame is reserved** for captions.
- **Narrated, not presenter-led.**
- **The visual system is inherited from clip 1 unchanged**, including the
  treatment that distinguishes schematic from measured. Do not re-invent it here.
- **Voice: ElevenLabs "Justin", `uFIXVu9mmnDZ7dTKCBTX`, at default speed**, the
  same voice across all four clips. **Measured at 168.0 words per minute** on
  act-length passages, with only a 2.5% penalty on number-dense text
  (`VOICE_MEASUREMENT_2026-09-17.md`). Every word budget below is stated at that
  measured rate with a fifth of each act silent. Re-measure if the voice, the
  model or the speed changes, because any of the three moves every runtime
  downstream.
- **Two-pass render expected.**
- **If text is rendered with manim on Linux, guard glyph spacing** by laying out
  at a larger requested size and scaling down.

## Narration conventions, settled 2026-09-17

- **Voice:** Justin `uFIXVu9mmnDZ7dTKCBTX` on `eleven_multilingual_v2` at speed
  1.0, **measured at 168.0 words per minute** on act-length text.
- **`say_as` map**, so the caption keeps the written form and the engine gets the
  spoken one: `SNPs` to `snips`, `SNP` to `snip`, `isolates` to `isolits`.
- **"unit", never "group"**, for an analysis unit. The statistical senses stay:
  grouping ladder, leave-group-out, groupings.
- **Measure every line against its own audio file.** Synthesis is not
  deterministic: the same text re-synthesized varies up to sixteen percent in
  duration. A line that fits is a fact about a file, not about a sentence, so
  never re-generate a line that already fits.

## You may refuse this brief

If the material does not support the claim or the quantity, say so and propose
what it does support. Act 2 is the specific risk: it argues that partitioning is
biological rather than computational, and it rests on a citation with a stated
caveat rather than on anything measured here. If it cannot be drawn without
looking like a measured result, say so and propose a framing that is visibly an
argument from the literature.
