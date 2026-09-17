# TUC series: where all four clips stand

Written 2026-09-17 after Animo delivered clips 2, 3 and 4. **The whole series
picture now exists: 22.9 minutes.** Everything below was checked, not taken from
the render notes.

| clip | picture | duration | collision checks | narration |
|---|---|---|---|---|
| 1 From one province to a global question | done | 291.02 s | **clean, all four** | **voiced on v3** |
| 2 A ruler you can trust | built | 304.30 s | 7 findings, all clearance | not written |
| 3 What the ruler measured | built | 299.30 s | **completely clean** | not written |
| 4 How close is close enough | **three rival builds** | 476.83 to 476.90 s | 13 to 18 findings, all clearance | not written |

Copied out of the volatile renders directory to
`~/Downloads/TUC_CLIP2_2026-09-17/`, `~/Downloads/TUC_CLIP3_2026-09-17/` and
`~/Downloads/TUC_CLIP4_CANDIDATES_2026-09-17/{A,B,C}/`.

## No true overprints anywhere in clips 2 to 4

Every finding across all five builds is a **clearance** violation, text sitting
0.02 to 0.12 units from other text without intersecting it. Nothing is
overprinted, which is the defect that made clip 1's act 2 display a wrong number.

**Several findings are legitimate and must not be "fixed".** Clip 4 act 5's
ladder pairs a label with its value ("Country" beside "16 classes", "89% correct,
46% baseline" beside "modal k = 20"). Those are table columns and 0.09 units is
normal typography. The clearance check does not know a table from a paragraph, so
its output needs reading rather than obeying. In clip 1 the same check was
catching prose abutting the source note, which is a real defect; here it is
mostly not.

## Provenance is clean, which was worth checking

The reused clips are the right copies in every case:

- clip 2's `DetectionWindowSweep` and `NegativeControlZoom` are md5-identical to
  the merged set
- clip 3 references the merged set by absolute path
- clip 4 act 3 is the merged `OutbreakThreshold`, and act 6 is the **rebuilt**
  `Act4NotSeparable` at 51.0 s, not the superseded 46.9 s copy. Six copies of
  that file exist on disk in two versions; the right one was used.

## Clip 4 needs a decision that cannot be made mechanically

The three builds are **independent interpretations of the same brief, not
iterations of one another.** Their `scene.py` files differ throughout, and both A
and C describe independently hitting and fixing an overprint where the axis block
printed through retained text.

| | A `7567b90f` | B `4bb107a2` | C `07420c96` |
|---|---|---|---|
| duration | 476.900 s | 476.833 s | 476.900 s |
| acts on their frame target | all | **two miss by 2 frames** | all |
| clearance findings | 18 | **13** | 18 |
| acts with findings | 4 of 7 | **3 of 7** | 5 of 7 |

B has the fewest findings and the only frame drift, and the drift is 33 ms on a
45 s act, which is immaterial. **On the mechanical evidence B wins, but the
mechanical evidence cannot see whether a build explains the ladder better.** That
needs watching, and it is the project lead's call.

## CORRECTED: the budgets are fine. 168 versus 179 costs five points of silence

An earlier version of this section said clips 2 to 4 were short by about 244
words and that clip 2 at 38% silence would be refused. **That was wrong, and the
error was mine, not the briefs'.** I extracted word budgets with a pattern that
only matched `(~N words` in an act heading, which silently missed the two lead-in
budgets in clip 2 and the two in clip 3, each stated mid-paragraph as
`*Lead-in ~40 words*`. Clip 2's budget is 475, not 395; clip 3's is 535, not 475.

Measured properly, on new content only:

| clip | new content | budget | speech at 179 | silence |
|---|---|---|---|---|
| 1 | 291 s | 650 | 218 s | 25% |
| 2 | 215 s | 475 | 159 s | 26% |
| 3 | 237 s | 535 | 179 s | 24% |
| 4 | 381 s | 850 | 285 s | 25% |

**All four sit inside the 10 to 35% band at the budgets the briefs already
specify.** Nothing needs padding. The 168 against 179 difference is real but its
whole effect is about five points of silence, from a planned 20% to an actual 25%,
which is comfortable rather than a problem.

Clip 1's act 7 did need five more words, but that was one short act breaching the
ceiling on its own, not a series-wide shortfall.

**The lesson is the one this project keeps relearning:** a total assembled by a
regex over prose is a measurement with no denominator check. Count the acts the
pattern matched against the acts that exist. Here it found 4 of 6 in clip 2 and 5
of 7 in clip 3 and reported a total anyway.

## Next, in order

1. **Choose the clip 4 build.** Blocking only clip 4.
2. **Narrate clip 2** at 179 wpm with the extra words, then clip 3, then clip 4.
   The reused clips already have narration: clip 2's two are in
   `TUC_LEGACY_MERGED_2026-09-17/narration_corrected/`, and clip 3's `7.09` was
   re-authored there after its picture changed to a ratio plot.
3. Voice each on `eleven_v3` under a fixed seed, normalize per line, refit from
   the audio rather than from any nominal rate.
