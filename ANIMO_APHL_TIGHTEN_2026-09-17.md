# APHL film: the speed decision, and the picture trim that follows

Resolves the open item in `VOICE_MEASUREMENT_2026-09-17.md` §"What this does to
each film". Read that first.

## The problem, stated exactly

The APHL room has many second-language listeners, so Justin at his default 168
words per minute is too fast for it. But slowing him created a second problem: at
131.7 wpm the film could not carry enough narration to stay dense.

That turned out to be arithmetic, not judgement. Narration density is
`rate x (1 - silence)`, so at 131.7 wpm with a normal 18% silence the ceiling is
**108 spoken words per minute of runtime**, below the 120 floor that flags a clip
stating conclusions rather than narrating. Reaching 120 at that rate would need
silence down at 8.9%, below the 10% floor. **The two floors are mutually
unsatisfiable below about 146 wpm.** No amount of rewriting fixes that.

## The decision: a different model, not a different voice

| model | speed | measured | density at 18% silence |
|---|---|---|---|
| `eleven_multilingual_v2` | 1.0 | 155 to 168 | 127 to 138 |
| `eleven_multilingual_v2` | 0.9 | **ignored**, 154.8 | 127 |
| `eleven_multilingual_v2` | 0.8 | 131.7 | 108, too sparse |
| `eleven_turbo_v2_5` | 0.9 | **157.8** | **129** |
| `eleven_turbo_v2_5` | 0.8 | 136.5 | 112, too sparse |

**Use `eleven_turbo_v2_5` at speed 0.9**, same Justin voice
(`uFIXVu9mmnDZ7dTKCBTX`), giving **157.8 wpm**.

That is meaningfully slower than 168 for the room, and it clears the density floor
with healthy silence. It has to be the turbo model because **`multilingual_v2`
ignores speed 0.9**, returning 154.8 against 155.1 at 1.0, and then jumps
straight to 131.7 at 0.8. There is no intermediate setting on that model.

The TUC series is unaffected and stays on `multilingual_v2` at 1.0. One fluent
viewer watching alone does not need the slower read.

## The trim

Target runtimes derived from each act's word budget at 157.8 wpm and 18% silence,
not chosen by eye.

| act | words | now | target | trim | largest measured gap |
|---|---|---|---|---|---|
| FilmTitleCard | — | 6.8 s | 6.8 s | none | 3.8 s |
| Act 1 The Question | 85 | 40.1 s | 39.4 s | **0.7 s** | 9.9 s |
| Act 2 Fair Comparison | 90 | 49.4 s | 41.7 s | **7.7 s** | 10.3 s |
| Act 3 The Window | 80 | 46.2 s | 37.1 s | **9.1 s** | 11.0 s |
| Act 4 Geography | 110 | 45.9 s | 51.0 s | **grows 5.1 s** | rebuild |
| Act 5 The Ceiling | 80 | 46.6 s | 37.1 s | **9.5 s** | 9.5 s |
| **total** | **445** | **235.0 s** | **213.1 s** | **21.9 s** | |

Resulting density **125.3** words per minute of runtime, above the 120 floor.
Silence **18.0%** across the narrated acts, 169.2 s of speech in 206.3 s of
picture.

**Every trim is smaller than a measured still stretch inside its own act**, so the
time is available without touching anything that moves. Act 1 already fits and
needs essentially nothing.

**Act 5 is the one to watch.** Its trim of 9.5 s equals its largest single gap
exactly, so taking it all from one place would remove that hold entirely. Spread
it across the 9.50 s and 7.82 s gaps instead.

**Act 4 gets longer, not shorter.** It is being rebuilt to
`ANIMO_ACT4_REVISION_2026-09-17.md` with three beats and a pivot, which is more
than the old act carried. 51.0 s is its target.

## How to take the time out

Cut held frames, not animation. The gaps above are stretches where the frame
difference trace detects no change, so they are holds rather than motion. A hold
is legitimate when narration is explaining something, and these acts have no
narration yet, so nothing is being explained during them.

Do not compress animations to save time. That changes the pacing of the thing
being taught, and at 60 fps it also risks the quantization drift that makes a
preview and a delivery render different lengths.

## What this does not change

- **Every accuracy guard still binds.**
- **The word budgets are the spine's original ones**, 85 / 90 / 80 / 80, plus 110
  for the rebuilt Act 4. Nothing has to be cut from the script. The fifteen
  percent overshoot reported earlier was an artifact of the assumed rate.
- **Frame audit and beat map must be re-run** on every trimmed act. Trimming moves
  every subsequent beat, so the current beat map is void the moment an act is
  re-rendered.
- **Narration comes after**, written to these word budgets against the new beat
  maps, then generated at turbo 0.9 and measured before the delivery re-render.
