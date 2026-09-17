# build_narration.py: two caption faults, fixed

Found while delivering the APHL film, 2026-09-17. Both were invisible in the
generated files and only appeared when the delivered HTML was opened in a
browser. `test_build_narration_captions.py` at the repo root reproduces them.

## What was wrong

**1. Cue text was emitted unwrapped.** A 110-character narration line became one
110-character caption line. Chrome does not wrap a long cue: it renders it on a
single line and clips whatever runs past the frame. The first caption of the
delivered film read "so people meet" and stopped, silently losing "it where they
live and work." No error anywhere, and the VTT was byte-perfect against source.

**2. `--vtt-line` defaulted to 94.** That pushes cues to the bottom edge, which
is exactly where the player draws its own control bar. With controls visible the
caption sits on top of the play button, the time readout, volume and fullscreen.

The second fault has an honest origin, recorded in the script's own comment: 94
was chosen to trade the source line for the data labels, which is the right trade
*against clip content*. It just collides with the player's furniture, which the
comment did not consider.

## The fix

| | before | after |
|---|---|---|
| cue wrapping | none | `wrap_caption()`, default **42 chars**, the broadcast convention |
| `--vtt-line` default | **94** | **0**, meaning omit and let the player place captions |
| new flag | | `--caption-width`, 0 disables wrapping |

Chrome already places a *wrapped* cue clear of its own controls, so once
wrapping exists the line setting stops being needed. Both `84%` and `94%`
rendered identically on the delivered film once cues wrapped.

## Test first, and it failed first

`test_build_narration_captions.py` builds a one-line spec with a 110-character
cue, renders a throwaway clip with ffmpeg, runs the script, and asserts:

- no caption line exceeds 60 characters, in **both** VTT and SRT
- wrapping preserves the words exactly, in order
- default output carries **no** `line:NN%` setting
- `--vtt-line 90` still emits `line:90%`, so the opt-in path is not broken

Before the fix it reported both faults verbatim:

```
FAULT 1 vtt: longest caption line is 109 chars, expected <= 60 (unwrapped)
FAULT 1 srt: longest caption line is 109 chars, expected <= 60
FAULT 2: default output carries a cue setting: line:94%
```

After: `ALL PASS`. Verified again on a real spec, the TUC acts 3 and 5 narration,
which now emits at most 42 characters per line and no cue settings.

## The skill is now under version control

**Resolved 2026-09-17.** `~/skills` is a git repository pushed to
`PHemarajata/skills`, **private**, seventeen tracked files and no bytecode.
Private rather than public because the skill carries no license and no stated
author, so republishing it would assert a right to redistribute that the files do
not establish.

History is two commits on purpose:

| commit | state | the test says |
|---|---|---|
| `5bace68` import as received | the skill exactly as it arrived | **RED**, both faults verbatim |
| `3d41496` the caption fix | this change | **GREEN** |

The first commit was reconstructed by reverse-applying the fix, and the test
verified the reconstruction: it reproduced both original faults with identical
messages. So the diff at `3d41496` is exactly what changed, and nothing else.

The test stays committed here rather than beside the skill because it is the
durable half across reinstalls: running
`python3 test_build_narration_captions.py` says in one line whether the bug is
back, whatever version of the skill is installed.

## Consequence for the reserved caption band

A wrapped caption is taller than an unwrapped one, so a clip that reserves a band
for captions must reserve it for the **wrapped** height. The APHL film reserves
the bottom eighth, which fits one caption line, and only 13 of its 31 cues are
short enough to be one line at any sane width. The rest now sit two lines tall
and reach above the reserved band onto axis labels.

That is not a tooling bug and this fix does not address it. It is a brief-level
assumption: the band was sized for a caption height nobody had measured. Any
future brief that reserves a caption band should say **how many lines** it
reserves, and the narration should be written to fit that many.

The narrower the wrap, the safer against clipping and the taller on screen. 42 is
the broadcast convention and the default here; the APHL film shipped at 55, which
keeps most cues to two lines. Neither is wrong, but the choice belongs to whoever
knows how much room the picture left.
