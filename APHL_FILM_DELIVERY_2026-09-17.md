# The APHL film is built

Assembled 2026-09-17. Deliverables sit in
`~/.agi/renders/4f9166a4-fdba-4191-ad20-8abae769dea8/film/`.

| file | size | what |
|---|---|---|
| `APHL_FILM.html` | 19.3 MB | **the deliverable.** One self-contained file, opens offline, no external URLs |
| `APHL_FILM.mp4` | 14.4 MB | the film alone, for anyone who wants the video |
| `APHL_FILM.vtt` / `.srt` | 4 KB | the caption track, 31 cues |

## What it is

**213.12 seconds**, 1920x1080 at 60 fps, h264 and aac, six segments concatenated
without re-encoding.

| segment | runtime | narration |
|---|---|---|
| Film title card | 6.8 s | silent, by design |
| Act 1 The Question | 39.4 s | 88 words, 5 lines |
| Act 2 Fair Comparison | 41.7 s | 88 words, 6 lines |
| Act 3 The Window | 37.1 s | 79 words, 6 lines |
| Act 4 Not Separable | 51.0 s | 109 words, 7 lines |
| Act 5 The Ceiling | 37.1 s | 81 words, 7 lines |

445 spoken words, 31 caption cues, every line fit-checked against its own audio
file. Voice is Justin `uFIXVu9mmnDZ7dTKCBTX` on `eleven_turbo_v2_5` at speed 0.9.

The title card needed silent audio at 48 kHz mono to concatenate with the acts,
which were 48 kHz mono against its original 44.1 kHz stereo. Without that the
concat would have produced broken audio rather than an error.

## The caption defect, which only the rendered page showed

`build_narration.py` writes `line:94%` on every cue. On the rendered page that
put the caption **straight through the player's control bar**, overlapping the
play button, the time readout, volume and fullscreen. Worse, the cue text was a
single unwrapped line of up to 147 characters, so Chrome **truncated it**: the
first caption read "so people meet" and stopped, losing "it where they live and
work."

Neither fault is visible in the markup. The VTT was correct, byte-identical to
source, 31 cues, every one carrying its setting. The skill's instruction to check
captions on the rendered page rather than in the file is the only reason this was
caught, and the truncation is the more serious of the two: it silently drops
words from a deliverable meant for second-language listeners.

**Fixed** by wrapping every cue to 55 characters per line. Text is now complete
and legible, and Chrome clamps a two-line cue clear of the controls by itself, so
the line setting stops mattering: 84% and 94% render identically once the cue
wraps.

## One trade left open, and it needs your call

A two-line caption is taller than the bottom eighth the film reserves for it, so
it now covers the axis label, for example "mean pairwise core SNPs (diversity)" in
Act 3. Axis numbers stay visible; the explanatory label does not.

**Captions are currently on by default**, so every viewer sees this unless they
turn them off.

| | cues at one line | two | three |
|---|---|---|---|
| wrapped at 55 chars | 6 | 21 | 4 |
| wrapped at 62 | 10 | 18 | 3 |
| wrapped at 70 | 12 | 18 | 1 |

Only 13 of 31 cues are short enough to fit one line at any sane width, so
wrapping alone cannot solve it. Four options:

1. **Leave it.** Captions on, axis labels covered when they are. Defensible: the
   numbers stay readable and the room needs captions more than it needs that
   label.
2. **Default captions off**, opt-in through the CC control, which is what the
   page's own hint already tells viewers to do. Protects the picture and hurts
   the audience the captions exist for. I would not.
3. **Split the long cues** into more, shorter ones. Fits the reserved band, and
   costs a retime of every act.
4. **Re-render with a taller reserved band**, two caption lines instead of one.
   The structural fix, and it costs a render of all six acts.

My preference is 1 now and 4 if there is another render pass anyway, because the
reserved band was sized for a single caption line and that assumption is the
actual defect.

## Still outstanding

- `build_narration.py` emits unwrapped cues and a `line:94%` default. Both bit
  here. Worth fixing at source before the TUC series reaches delivery.
- The TUC series is untouched by this and still waits on the legacy merge.
