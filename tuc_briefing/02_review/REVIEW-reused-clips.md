# Review: the five reused clips, beats against narration

Measured 2026-09-17 with `map_beats.py`, which decodes every frame of the
delivered MP4s and reports where visible change spikes. Narration line starts are
the cue starts in the delivered SRTs. Times are measured, not estimated.

A line is called **orphaned** when no detected moment falls within 2.5 seconds of
it: the voice is describing something happening while the picture is still.

## Summary

| clip | dur | lines | moments | last moment | dead tail | orphaned | verdict |
|---|---|---|---|---|---|---|---|
| `7.01` negative control | 41.5 s | 10 | 16 | 37.83 s | 3.7 s | **0 of 10** | accept, retime L1 |
| `7.03` detection window | 47.8 s | 10 | 21 | 46.30 s | 1.5 s | 2 of 10 | revise, then retime |
| `7.07` recursive subdivision | 35.7 s | 9 | 14 | 32.82 s | 2.9 s | **0 of 9** | accept, retime L1 |
| `7.09` tree builder | 26.6 s | 6 | **3** | **5.80 s** | **20.8 s** | **4 of 6** | **re-author, not retime** |
| `7.12` outbreak threshold | 44.9 s | 11 | 7 | 42.88 s | 2.0 s | 5 of 11 | revise, then retime |

## `7.09` is not a clip with a timing problem

Three detected moments in 26.6 seconds, the last at **5.80 s**. Nothing visible
changes for the final **20.8 seconds, which is 78% of the runtime**. Four of six
lines are orphaned and the worst sits **18.4 seconds** from any moment.

```
  L3  11.60 s   nearest moment 5.80   +5.80   "Lines scatter both ways. No directional bias."
  L4  15.20 s   nearest moment 5.80   +9.40   "Now rapid N J, against that same baseline."
  L5  20.80 s   nearest moment 5.80  +15.00   "Almost every line falls. That is systematic."
  L6  24.20 s   nearest moment 5.80  +18.40   "A fast default lowers the answer."
```

This independently confirms `ANIMO_BRIEF` section 11.1 from a direction that note
did not use. Section 11.1 said the finding is carried by the caption rather than
the picture. The frame difference trace says the picture is not carrying anything
at all after the sixth second: the clip is effectively a still image with a
voiceover, and every line claiming motion is describing something the viewer
cannot see.

**Its narration cannot be retimed, it has to be re-authored.** The specified fix
changes the encoding from paired absolute values to one dot per comparison against
a parity line. After that change the words "lines", "scatter" and "falls" describe
objects that no longer exist. Four of the six lines become factually wrong about
their own picture.

This is the one place in the series where the rule "do not re-author existing
narration, ask before changing wording" is overridden, and it is overridden
because the visual it was anchored to is being replaced. Write the new lines
against the new beat map, not against the old script.

## `7.12`: the measured anchors land on nothing

Five of eleven orphaned, and they are the wrong five. Lines 8, 9 and 10 carry the
four published anchor points, which are the only measured values in a clip whose
two curves are schematic.

```
  L7  25.60 s   nearest moment 22.35   +3.25   "At the edge of the band, detection is close to nothing."
  L8  31.80 s   nearest moment 22.35   +9.45   "One published outbreak spanned a thousand SNPs."
  L9  35.20 s   nearest moment 42.88   -7.68   "Almost none of it survived recombination filtering."
  L10 38.80 s   nearest moment 42.88   -4.08   "It matters most where it is detected least."
```

There is a **20.5 second gap** between the moments at 22.35 s and 42.88 s, and the
entire evidential payload of the clip is spoken inside it. Section 11.2 already
said the anchors "arrive as thin dashed verticals in the last third" and asked for
them to become the spine. The measurement says they are not even arriving as
moments: whatever the dashed verticals do, it is below the detector's threshold
for visible change.

Applying revision 2 should create a moment per anchor. Re-map after the re-render
and move L8 to L10 onto them.

## `7.03`: the two orphans are the mechanism

```
  L5  17.20 s   nearest moment 14.58   +2.62   "This is a real group from the collection. Nothing gets marked."
  L6  24.20 s   nearest moment 21.37   +2.83   "Inside the window the piece is clearly denser than the background."
```

Both sit just past the 2.5 s bound, so this is milder than the two above. But L6 is
the in-window state, which is the single idea the clip exists to convey, and it is
the line furthest from its own moment. Consistent with section 11.2's verdict that
the clip "has the best idea in the set and buries it": the counted-as bars are not
generating enough visible change to register as moments.

Promoting the bars, as revision 1 requires, should fix the timing as a side effect.

## `7.01` and `7.07` are clean

Zero orphans in both. Every line sits within 2 seconds of a detected moment and
most within 1. Their pending revisions are real but they are about legibility and
pacing, not about narration alignment. After re-render, re-map and retime, but
expect small adjustments rather than rewriting.

Note `7.01`'s revision 1 cuts seven seconds of empty zoom between 20 s and 27 s.
That will pull every line after L6 earlier by about seven seconds. The retime is
mechanical but it is not optional.

## One systematic finding across all five

Every clip's first line starts at **0.60 s** while the first detected moment is at
**1.70 to 1.78 s**. The narration consistently begins about 1.15 seconds before
the title card resolves.

It is small, it is in all five, and it is the cheapest fix in this document: move
L1 to land on the title beat rather than ahead of it. The brief template's rule
that a title card holds one to two seconds is what produced the 1.7 s beat, so the
pack was built correctly and the narration was written to a different assumption.

## The Justin voice fits all five

Measured against the delivered cue spacing, the slowest a voice can read and still
fit every line before the next one starts:

| clip | tightest line | slowest voice that fits |
|---|---|---|
| `7.07` | L1, 8 words in 6.00 s | 80 wpm |
| `7.01` | L4 | 86 wpm |
| `7.09` | L4 | 86 wpm |
| `7.03` | L5 | 94 wpm |
| `7.12` | L1 | 106 wpm |

ElevenLabs voices typically read between 130 and 170 wpm, so **Justin
(`uFIXVu9mmnDZ7dTKCBTX`) has comfortable headroom in all five**, with at least
0.98 s of slack on the tightest line in the set. The voice choice does not
constrain the reuse.

This says nothing about the four new clips, whose word budgets assume 132 wpm and
must be re-derived from Justin's measured rate.

## What to do, in order

1. Apply the pending section 11 revisions to all five clips.
2. Re-run `map_beats.py` on the revised renders. **Every time in this document is
   measured against the pre-revision files and will move.**
3. Re-author `7.09`'s narration against its new beat map. Retime the other four.
4. Move L1 onto the title beat in all five.
5. Measure Justin's rate, then re-derive the new clips' act budgets.

## Method note

`map_beats.py` reports a moment where frame-to-frame difference spikes, split into
a beat (discrete change) and a span (continuous motion). It measures visible
change, not meaning: a moment is not automatically worth a line, and a line does
not always need a moment. A held frame under a line that is drawing a conclusion
is legitimate. Four of six lines with no moment for eighteen seconds is not.
