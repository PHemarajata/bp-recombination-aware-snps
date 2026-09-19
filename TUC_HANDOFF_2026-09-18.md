# TUC briefing series: handoff

Everything a new session needs to pick up the four-film TUC briefing. Written
2026-09-18, after the films were finished, voiced and corrected across four
review rounds. **Next task: transitions between clips, and aesthetics.**

---

## 1. What this is

Four narrated films for Suzanne, the TUC lab chief who funded a
*B. pseudomallei* recombination-aware SNP and origin-attribution study. Audience
is technical: familiar with the project and with phylogenetics through the
closeout deck, but not population genomics.

| # | title | runtime | file |
|---|---|---|---|
| 1 | From one province to a global question | 285.1 s | `1_From_one_province_to_a_global_question.mp4` |
| 2 | A ruler you can trust | 302.9 s | `2_A_ruler_you_can_trust.mp4` |
| 3 | What the ruler measured | 300.8 s | `3_What_the_ruler_measured.mp4` |
| 4 | How close is close enough | 472.6 s | `4_How_close_is_close_enough.mp4` |

**Delivery folder: `~/Downloads/TUC_FILMS_2026-09-18/`.** 22.7 minutes total.
These are the current cut. Anything else on disk named like a film is older.

The arc: clip 1 says what the project built and poses the question; clip 2
builds the instrument (the recombination detection window) and shows it invents
nothing and finds what is there; clip 3 points the instrument at the data; clip 4
asks what the resulting ruler can and cannot place.

---

## 2. Where everything lives

### Repo (git, branch `docs/film-work-2026-09`)
`/Users/peerahemarajata/bp-recombination-aware-snps`

| path | what |
|---|---|
| `tuc_clip1_scenes.py` … `tuc_clip4_scenes.py` | Manim sources, one per film |
| `tuc_legacy_scenes_merged.py` | the four reused legacy scenes (see §3) |
| `check_text_collisions.py` | six text-layout checks |
| `trace_onscreen_text.py` | records when each on-screen string appears/disappears |
| `check_narration_sync.py` | flags narration spoken while its slide is gone |
| `check_beat_coverage.py` | interleaves visual beats with narration starts |
| `tuc_briefing/01_concept/BRIEF-0*.md` | the four briefs: claim, quantity, acts, forbidden framings |
| `tuc_briefing/02_review/REVISION-*.md` | what was wrong and what was done, per round |
| `tuc_briefing/03_narration/NARRATION-CLIP-0*.md` | the delivered caption text per film |

### Build directories (NOT in git, they hold audio and renders)
`~/Downloads/TUC_CLIP{1,2,3,4}_2026-09-18/`

| subdir | what |
|---|---|
| `beats/spec_v2.json` | **the source of truth for narration**: every line, its start, its anchor |
| `narration/` | generated CSV, TXT (spoken form), SRT and VTT (written form) |
| `voice/<Part>/NN.mp3` | one file per line, ElevenLabs |
| `parts/` | silent Manim renders, 1920x1080 60fps |
| `final/` | narrated parts + `concat.txt` + `TUC_CLIP<N>_NARRATED.mp4` |

Older dated folders (`..._2026-09-17`) are superseded. Clip 1's `narration_final`
there is stale and does **not** match the delivered film; `narration_v3` was the
last good one before this round.

### Toolchain
- Manim Community **v0.21.0**, a user-site install for the python.org framework
  Python 3.13.7. **Not a venv, and not in `/tmp`.**
  - interpreter `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`
  - CLI `~/Library/Python/3.13/bin/manim`
  - manimpango 0.6.1. SoX is absent, so Manim prints a warning on every
    invocation. It is noise; all our audio goes through ffmpeg.
  - **An earlier version of this handoff said `/tmp/manimenv`. That directory was
    cleared on reboot 2026-09-19 and never held the only copy.** Do not recreate
    a toolchain under `/tmp`.
  - **Animo has its own, and it is not interchangeable.** `~/.agi/venvs/manimvtk`
    holds `manimvtk 0.19.0.post6`, a VTK fork at a different version. Rendering
    our scenes through it risks silent layout drift. Use the paths above.
- Pipeline scripts: `~/skills/narrated-clip-production/scripts/` —
  `map_beats.py`, `build_narration.py`, `generate_elevenlabs.py`,
  `assemble_voice.py`, `retime_from_audio.py`, `audit_frames.py`, `deliver.py`.
- `ELEVENLABS_API_KEY` is in the environment.

---

## 3. Film structure, part by part

Every film is a concatenation of independently rendered parts. **These seams are
where transitions would go.**

**Clip 1** (7 parts): TucC1Act1 34.0 · Act2 57.0 · Act3 28.1 · Act4 54.0 ·
Act5 51.0 · Act6 43.0 · Act7 18.0

**Clip 2** (9 parts): Clip2TitleCard 3.6 · Act1 48.0 · Act2 54.0 ·
Act3Leadin 17.0 · **DetectionWindowSweep 47.8** · Act4Leadin 17.0 ·
**NegativeControlZoom 41.5** · Act5 45.0 · Act6 29.0

**Clip 3** (9 parts): C3Act1 31.0 · Act2 63.0 · Act3 48.0 · Act4Lead 14.0 ·
**RecursiveSubdivision 35.7** · Act5Lead 14.0 · **TreeBuilderPaired 26.6** ·
Act6 30.0 · Act7 38.5

**Clip 4** (9 parts): C4Act1 45.0 · Act2 31.0 · **OutbreakThreshold 44.9** ·
Act4 58.0 · Act5 85.0 · **Act4NotSeparable 51.0** · Act7 72.7 · Act8 45.0 ·
Act9 40.0

**Bold parts are reused legacy renders** from `tuc_legacy_scenes_merged.py`.
They have their own visual conventions (axis labels sit lower, a source line in
the bottom eighth) that differ slightly from the newer acts. `DetectionWindowSweep`
and `NegativeControlZoom` belong to clip 2; `RecursiveSubdivision` and
`TreeBuilderPaired` to clip 3; `OutbreakThreshold` and `Act4NotSeparable` to
clip 4. **Editing one in that shared file affects only the clip that renders it,
but check which before you touch it.**

### Continuity objects (matters for transitions)
- **The diversity axis** (unit diversity, mean pairwise core SNPs, log scale) is
  drawn at the end of clip 2 act 2 and carries through clips 2 and 3.
- **The 85 analysis units** as marks on that axis are clip 3's continuity object.
- **The shaded window band** appears in clip 2 and persists into clip 3.
- Clip 1 act 7 hands off to clip 2; clip 3 act 7's last line is "Clip four asks
  what this ruler can place, and what it cannot."

---

## 4. How to rebuild

Render one scene (always clear the text cache first — see §7):

```bash
cd ~/bp-recombination-aware-snps
rm -rf media/texts
~/Library/Python/3.13/bin/manim -qh --fps 60 -r 1920,1080 --disable_caching \
    tuc_clip3_scenes.py C3Act2
cp media/videos/tuc_clip3_scenes/1080p60/C3Act2.mp4 \
   ~/Downloads/TUC_CLIP3_2026-09-18/parts/
```

Then rebuild narration and film:

```bash
cd ~/Downloads/TUC_CLIP3_2026-09-18
S=~/skills/narrated-clip-production/scripts
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 $S/build_narration.py beats/spec_v2.json \
    --out narration --max-silence 45
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 $S/generate_elevenlabs.py --csv narration --out voice \
    --voice-id uFIXVu9mmnDZ7dTKCBTX --model eleven_v3 --seed 20260917
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 $S/assemble_voice.py --csv narration --voice voice \
    --video parts --out final --force
cd final && ffmpeg -y -v error -f concat -safe 0 -i concat.txt -c copy \
    TUC_CLIP3_NARRATED.mp4
cp TUC_CLIP3_NARRATED.mp4 ~/Downloads/TUC_FILMS_2026-09-18/3_What_the_ruler_measured.mp4
```

**Voice, fixed:** ElevenLabs "Justin" `uFIXVu9mmnDZ7dTKCBTX`, model `eleven_v3`,
**seed 20260917**. With the seed fixed, identical text regenerates
bit-identically, so re-synthesis costs credits but never changes a fit.
Do not substitute v2; v3 also rejects neighbour conditioning.

**say_as map** (in each `spec_v2.json`). Keys are the WRITTEN form, values the
SPOKEN form. **The spec's `text` field carries the SPOKEN form**; the caption
writer inverts the map to restore spelling in the SRT and VTT.

```
isolates→isolits, isolate→isolit, SNPs→ess enn peez, SNP→ess enn pee,
RAxML→racks M L, pseudomallei→su-do-MA-lee-eye, Nakhon Phanom→Na-kon Pa-nom
```

---

## 5. The visual system

White background, never dark. Franklin Gothic Medium (titles) / Book (body),
default size 28. Identical across all four scene files.

```
TEAL     #00A0AF  measured signal, fills and marks
TEAL_TXT #006E79  text-safe teal (any teal carrying a glyph)
TEAL_DK  #005057  SERIES: the funded isolates
TEAL_LT  #A3CCCC  background / unclassified
PURPLE   #9960A7  geography ONLY (regions, countries)
RUST     #B42E34  a limit or an adverse outcome ONLY
ORANGE   #E37C1D  above-window class only
INK      #404040  default ink
GRIDGRAY #E2E9EC  gridlines and shaded zones (the window band)
SRCGRAY  #6E6E6E  source lines
```

**Colour semantics are load-bearing.** Purple means geography and nothing else;
using it for "same sequence type" in clip 3 would have made it mean two things
in one series. Rust is adverse outcomes only.

**Layout constants**, in clip 3 and worth copying elsewhere:
```
SUB_TOP  = -3.0   bottom eighth reserved for captions
MARGIN   = 0.82   content inside +/- 6.29
BAND_TOP =  1.05  the shaded window band's top
BAND_BOT = -0.85  its bottom
ROW_ABOVE=  1.36  the ONE text row that fits above the band
ROW_BELOW= -1.18  the ONE text row that fits between band and axis
```

`Txt()` in each scene file is a wrap guard: it lays text out at a larger size and
scales down, because Pango wraps silently on Linux. Do not call `Text()` directly.

**Captions are not burned in.** The films are video + audio only. SRT and VTT
exist per part in `narration/` but have never been muxed or rendered. The bottom
eighth is reserved for them and currently holds only source lines.

---

## 6. Content rules (hard)

From the briefs and from the lab chief directly. Breaking these is a factual or
political error, not a style choice.

- **A low r/m is a detection failure, not a quiet genome.** The central reversal.
  Never present a low r/m as a low recombination rate.
- **Vocabulary**: the window's bounds are **"below the window" / "above the
  window" / "the lower edge" / "the upper edge"**. Not floor and ceiling — that
  word meant the window bound in clips 2 and 3 and a performance limit in clip 4,
  and the collision is why it was changed. Clip 4's "ceiling" (the linkage
  ceiling, the country ceiling) is the ordinary English sense and stays.
- **"unit", never "group"** for an analysis unit. Statistical senses stay
  (grouping ladder, leave-group-out).
- **Do not name cgMLST.** Excluded from this series by instruction.
- **Do not present the closeout's clustering.** Its clusters were silently capped
  at 200 on the mash distance matrix. Its *association indices* in clip 4 act 7
  are explicitly allowed by BRIEF-04 and are not the retired clustering.
- **Clip 4 says "fifty six of eighty five", never "two thirds".**
- **Never quote the Mash proxy against the [700, 4700] window.** The window is
  alignment-derived throughout.
- **Never claim the reported run is seed-reproducible.** It ran unseeded and
  multi-threaded.
- **Never say prior studies were wrong.** One step was missing from all of it,
  including this study until it was added.
- **On screen**: no em dashes, no en dashes, no semicolons, no curly quotes,
  American spelling, median sentence about 19 words.
- **Prose must not read as AI-assisted.** This is checked before anything is
  handed over.

### Key numbers (frozen basis: 85 units / 2,340 genomes, `FINAL_BASIS_2026-08-22`)
- in-window median r/m **7.70**, 47 units, 1,388 genomes, spread 5.72 to 9.41
- below the window 12 units, 1.32, 349 genomes; above 26 units, 2.14, 603 genomes
- pooled outside 38 units, **1.99**; naive pooled across all 85, **5.51**
- window **[700, 4700]** mean pairwise core SNPs; lower edge bracket 588 to 755,
  upper 4,632 to 4,732
- negative control 1,519 replicates over 62 unit-replicons, 20 returning any call
- spike-in recovery **91%** at the measured divergence (0.002)
- attribution: 46 scorable, region 89% / kappa 0.832, country 22% against a 26%
  baseline, Asia-vs-non-Asia kappa 1.000

**The lower-edge sensitivity is a common misreading.** 588, 700, 755, 840 are
candidate *positions for the lower edge, in SNPs*. 7.70, 7.70, 7.74, 7.78 are the
*median r/m recomputed at each*. Two being identical is the result. The screen
plots deviations (+0.00 +0.00 +0.04 +0.08); the narration must match that, not
recite absolutes.

---

## 7. Checks, and the traps they exist because of

Run all of these before delivering anything.

### Text layout
```bash
rm -rf media/texts
CLIP_SOURCE=tuc_clip3_scenes.py ~/Library/Python/3.13/bin/manim -ql \
    --disable_caching check_text_collisions.py C3Act2
```
Six checks: text-on-text overlap, near-miss clearance (0.12), white text off its
fill, reserved bottom eighth, text over marks, and **text cut by the edge of a
shaded zone**. The last one was added 2026-09-18 and immediately found ten
defects: the marks check deliberately ignores shapes larger than the text, and
the window band is exactly such a shape, so a line straddling its edge was
invisible to everything.

### Narration against the picture
```bash
rm -rf media/texts
TRACE_OUT=/tmp/trace.json CLIP_SOURCE=tuc_clip3_scenes.py \
  ~/Library/Python/3.13/bin/manim -ql --disable_caching trace_onscreen_text.py C3Act2
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 check_narration_sync.py /tmp/trace.json \
  ~/Downloads/TUC_CLIP3_2026-09-18/narration
```
Flags any line spoken while the on-screen string it paraphrases is gone. **Every
other check in the toolchain asks about timing; this is the only one that asks
about content.** All four films were a slide behind before it existed.

Two cautions: it produces **false positives on number-dense text** (this material
repeats "units", "median", "seven", "point" — five of six flags on a corrected
clip were spurious), so read each against the interleaved timeline. And Manim
returns `Text.text` with spaces stripped, so it matches by substring.

A **lead** of under ~1.5 s is correct and wanted. A line spoken **after** its
string is wiped is always a defect.

### Audio
Verify by **full decode**, never `ebur128`:
```bash
ffmpeg -v error -i FILM.mp4 -map 0:a:0 -f s16le -acodec pcm_s16le \
    -ar 16000 -ac 1 - | <rms per window>
```
A decoder-based loudness check passed a film that played silent, because ffmpeg's
tolerant decoder fixes up a container that lies about its own contents.

### The traps that silently produce wrong output

1. **Manim's text cache poisons renders.** The same source renders wrapped in one
   directory and clean in another. `--disable_caching` does not cover it.
   **`rm -rf media/texts` before every delivered render.**
2. **`generate_elevenlabs.py` keeps audio by line NUMBER, not by text.** Rewrite a
   line, re-run, and it prints "kept" while leaving the old recording in place.
   Delete the clip's voice directory when its lines change.
3. **`build_narration.py` writes nothing when it refuses.** The next step then
   runs against the *previous* CSV and regenerates the old text. Always confirm
   it printed `wrote narration/` before generating.
4. **`build_narration.py`'s silence and overrun checks are wpm estimates.** This
   voice reads number-dense text at roughly 120 wpm against a ~176 wpm median, so
   an all-numbers act was called 37% silent when the audio measured 22.7%. Build
   with a widened `--max-silence` and gate on `assemble_voice.py`, which reads the
   real files.
5. **Its PACING warnings are defect reports, not advice.** All four stalls it
   printed shipped once, including a 12.5 s dropout.
6. **Concat with `-c copy` takes the FIRST stream's parameters.** A stereo title
   card made a whole film play silent while every measurement said it was fine.
   **Every part must be `aac, 48000 Hz, 1 channel, mono`** — check before every
   concat. A part with no audio stream at all (a silent title card that never went
   through `assemble_voice`) is the same bug in a different shape.

---

## 8. State as delivered

All four: **0 silent ten-second windows, 0 lines spoken after their slide was
wiped, all seven/nine acts clean on the collision checker.**

| film | longest silent gap | where |
|---|---|---|
| 1 | 4.75 s | act 6 to act 7 seam |
| 2 | 4.75 s | title card open |
| 3 | 3.00 s | TreeBuilderPaired to act 6 seam |
| 4 | 6.50 s | act 5 to Act4NotSeparable seam |

**Every one of the largest remaining gaps is a seam.** That is directly relevant
to the transitions task: a transition placed there would be filling silence that
already exists, not adding to runtime.

### The room tone bed, applied 2026-09-19

Those gaps were not quiet, they were **digital zero**. Measured in half-second
windows by full decode, the delivered films spent this much of their runtime
below -60 dBFS:

| film | before | after |
|---|---|---|
| 1 | 18.2% | 0.0% |
| 2 | 15.2% | 0.0% |
| 3 | 14.6% | 0.0% |
| 4 | 20.5% | 0.0% |

Two reference films in the same genre (Harvard/Broad, US Pathogen Genomics
Centers of Excellence) measured 0.3% and 2.9%. They never go silent because a
low bed runs underneath throughout. That dropout, not the cutting, is most of
why a concatenation reads as a slideshow.

`add_room_tone.py` lays band-limited pink noise under a **finished** film:

```bash
python3 add_room_tone.py --in FILM.mp4 --out OUT.mp4          # default -45 dBFS
python3 add_room_tone.py --in FILM.mp4 --check                # measure only
```

Defaults are -45 dBFS RMS, highpass 80 Hz, lowpass 4000 Hz. The lowpass matters:
speech intelligibility lives at 1 to 4 kHz, so a bed that stops below it can
never eat a consonant. There is deliberately **no sidechain ducking**, because at
23 dB of headroom it is unnecessary and it pumps at every line boundary, which is
the same artifact being removed. The level is reached by generating a probe and
measuring it, so changing the filters cannot silently move the level.

**Why this is safe.** It is mixed under the concatenated film, so no part is
re-rendered, no narration line moves, and the video stream is copied bit for bit.
The script verifies all three plus the aac/48000/mono rule and fails loudly.

Measured effect at clip 4's worst seam (dead air 259.63 to 266.05 s):

| | before | after |
|---|---|---|
| inside the seam | -330.31 dBFS | **-45.0 dBFS** |
| mid-narration control | -20.13 dBFS | -20.13 dBFS |

Output: **`~/Downloads/TUC_FILMS_2026-09-19_BED/`**. The 2026-09-18 folder is
untouched, so the bed is revertible by swapping folders.

This is room tone, not music, on purpose. The series' central finding is that a
low number is a detection failure, and a bed with a mood would editorialize a
deliberately unglamorous result. Music can layer on top later without redoing
this.

### Using a supplied music bed instead

`--bed FILE` loops an audio file in place of the synthesized noise. A supplied
mix normally needs all three of these, so they are options rather than defaults:

```bash
python3 add_room_tone.py --in FILM.mp4 --out OUT.mp4 \
    --bed "Softer Background Mix.mp3" \
    --bed-trim-head 3.5 --bed-trim-tail 8.0 --bed-xfade 5 --compress
```

- **Trim the fades.** A music bed fades in and out. Those fades are the loudest
  argument against looping it, so the faded ends are cut and only full-level
  material is looped. Find the fade lengths by measuring, not by guessing.
- **Crossfade the loop.** Copies are placed every (body minus crossfade) seconds
  and summed, so each fade out lands on the next fade in. Butt-joining leaves a
  hole at every loop point, which is the defect this tool exists to remove.
  The **first** copy has nothing before it to sum with, so the bed is built one
  crossfade longer and that opening fade is trimmed off. Without that, t=0 sat
  19.7 dB under the median.
- **Compress.** `Softer Background Mix.mp3` had an 11.06 dB working range
  (p10 to p90), which surges and recedes under narration. `--compress` took it
  to 2.18 dB.

**Check any supplied bed for these before using it**, because they decide whether
it can work at all:

| what to measure | why | `Softer Background Mix.mp3` |
|---|---|---|
| energy in 1 to 4 kHz vs the full mix | that is the speech band; a bed with energy there eats consonants | **-17.4 dB**, good |
| working range p10 to p90 | a wide range surges under narration | 11.06 dB, needed compression |
| envelope autocorrelation | a beat sets up an expectation our seams cannot meet | **0.73 at 107 BPM, it has a beat** |
| level at the first and last second | decides whether it can loop | fades at both ends, so trim |

The beat is a real editorial choice, not a neutral one. Act seams fall at times
set by animation length, not by music, so every hard cut lands mid bar. That is
a reason to prefer a sustained texture, not a reason the file cannot be used.

### Stereo finals

`--stereo` keeps a supplied bed's width and centers the mono narration.

**This does not break trap 6.** That rule binds the parts feeding the concat,
which must all be `aac, 48000 Hz, 1 channel`. This tool runs after the concat,
so the final can be stereo while every part stays mono.

**The trap inside the trap.** Do not reach a stereo final with
`aformat=channel_layouts=stereo` on a mono narration. ffmpeg converts mono to
stereo by attenuating each channel 3 dB to hold total power constant, so the
voice comes out 3 dB quieter than the mono build of the same film and nothing
announces it. Use `pan=stereo|c0=c0|c1=c0`, which duplicates at unity. The first
stereo build of clip 3 measured a median of -24.84 dB against the mono build's
-21.84 and **passed every check**, because the level test only looked for the
level rising. It now tests both directions.

Measured on clip 3, stereo against mono: median identical to 0.00 dB, duration
held, video bit-identical, 0.0 percent below -60 dBFS.

Width survives the loop, compress and level chain. Measured as side minus mid:

| | side minus mid |
|---|---|
| `Softer Background Mix.mp3`, source | -9.78 dB |
| stereo build, inside a narration gap | -9.65 dB |
| stereo build, inside another gap | -11.11 dB |

The voice images dead center, and the clean way to show it is that the **side
signal sits at about -54 dB whether or not anyone is speaking**. Voice
contributes to mid only, so its side contribution is zero.

Known, accepted, documented:
- One deliberate 3.6 s pause in clip 3 act 3, right after "A low ratio is a
  detection failure, not a quiet genome." Do not "fix" it.
- Clip 3's `RecursiveSubdivision` has pre-existing findings (axis labels in the
  reserved bottom eighth, the "eighteen times lower" annotation crossing the
  band). Verified identical before and after this round's edits.
- Clip 1 acts 4 and 7, clip 3 act 4 lead-in and `RecursiveSubdivision` sit
  slightly over the 25% silence guideline. Their gaps are all under 3 s.

---

## 9. Next task: transitions and aesthetics

**First settle what "between clips" means.** Between the four *films*
(1→2→3→4), or between the *acts inside* each film? Both are currently hard cuts.
The seams in §3 are the act boundaries.

### The constraint that governs everything here

The films are assembled with `ffmpeg -f concat -c copy`, which cannot crossfade.
A crossfade (`xfade` / `acrossfade`) requires re-encoding and, more importantly,
**overlapping two parts shortens the film**. Every narration line is timed
against its own part's timeline, so any overlapping transition desyncs everything
downstream of it unless the narration is re-laid.

Three approaches that do not break the build, in order of safety:

1. **Do it in Manim.** Add the fade in and out to the scene itself, inside the
   part's existing runtime. Costs a re-render, keeps every duration, needs no
   narration change. This is the only approach that also lets a transition carry
   a continuity object (the diversity axis persisting across a seam).
2. **Additive transition parts.** Render a short standalone transition clip, give
   it a mono 48 kHz silent audio track exactly as §7 trap 6 requires, and insert
   it into `concat.txt`. Total runtime grows, nothing desyncs. Good for
   film-to-film transitions, where there is no narration to preserve.
3. **Re-encode the whole film with xfade.** Only if 1 and 2 cannot give the look,
   and only with the narration re-laid afterwards and `check_narration_sync.py`
   re-run.

Do **not** trim a part to make room for an overlap. That is how the narration
ends up a slide behind, which took three rounds to find and fix.

### Aesthetic notes worth acting on

- The four films open inconsistently: clip 2 has a standalone title card (3.6 s),
  the other three open with a title inside act 1. A series-consistent opening and
  closing is probably the single highest-value change.
- Clip 1 and clip 4 have no end card; clip 3 ends on "Clip four asks what this
  ruler can place".
- The reused legacy parts sit slightly off the newer visual system (lower axis
  labels, a source line in the reserved bottom eighth). Harmonising them is a
  real improvement but means re-rendering from `tuc_legacy_scenes_merged.py` and
  re-checking which clip each belongs to.
- Captions exist as SRT and VTT and have never been used. If they are wanted
  burned in, the bottom eighth is already reserved and the written forms are
  already correct.

### Before touching anything

Read `tuc_briefing/01_concept/BRIEF-0*.md` for the film you are changing. Each
brief carries a "What would be a fabrication" and a "Forbidden framings" section
that constrain the *picture*, not just the words. Several of them forbid specific
visual treatments (for example: never draw the spike-in recovery as a smooth
rising curve, because it is not monotonic).

---

## 10. Data handling

*B. pseudomallei* is a **US Tier 1 Select Agent** and this repo has a public
GitHub remote.

- `.gitignore` **denies by default** and re-admits named files. To track a new
  file, add a `!path` line. **`git add -f` must never be used.**
- Restricted and must not leave the machine or go to Drive/rclone:
  `FINAL_PANEL.tsv`, `CGMLST_LICHT_ATTRIBUTION.tsv`, `VM_HANDOFF_PACK/`.
- `ANIMO_PACK/` is the cleared subset for external animation work.
- The films themselves carry no restricted table content and are fine to share.
