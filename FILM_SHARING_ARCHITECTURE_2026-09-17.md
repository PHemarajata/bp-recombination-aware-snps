# How the two films share material

Written 2026-09-17, from the source of both. The short version: **it is one design
system with two vintages, not two systems.** The sharing problem is smaller than it
looks, and the answer is one act library with two cuts.

## 1. The palettes are not similar. They are identical.

| token | legacy `scene.py` | APHL `aphl_common.py` |
|---|---|---|
| teal, marks | `TEAL` `#00A0AF` | `TEAL` `#00A0AF` |
| teal, text-safe | `TEAL_D` `#006E79` | `TEAL_TXT` `#006E79` |
| teal, deepest | `TEAL_X` `#005057` | `TEAL_DK` `#005057` |
| purple | `PURPLE` `#9960A7` | `PURPLE` `#9960A7` |
| rust | `RUST` `#B42E34` | `RUST` `#B42E34` |
| ink | `INK` `#404040` | `INK` `#404040` |
| rule / gridline | `RULE` `#E2E9EC` | `GRIDGRAY` `#E2E9EC` |
| gray | `GRAY` `#6E6E6E` | `SRCGRAY` / `GRAYOUT` `#6E6E6E` |

Same values, same names in three cases. Fonts match exactly too, Franklin Gothic
Medium for titles and Book for body, on a white background, in both.

The APHL build is the later vintage: it kept every value, renamed a few, added
`TEAL_LT`, `AMBER` and `ORANGE`, and **assigned each color a fixed meaning**. The
legacy clips predate that assignment.

## 2. So the divergence is semantic, and it is four specific things

**Purple means two different things.** APHL: geography and place. Legacy `7.03`:
the *mutation* bar in the counted-as pair. Run them in succession and purple is
mutation in one act and country in the next.

**Rust is used for the subject, not a failure.** APHL reserves rust for "a limit or
a failure, adverse outcome only". Legacy `7.03` uses it for "one imported piece",
which is the thing being detected, and for "measured r/m 1.25", which is a
measurement. Under the APHL rule both should be teal.

**The diversity axis is log in legacy and linear in APHL.** Same quantity, same
window `[700, 4700]`. This one is already a known defect: section 11.2's complaint
about `7.07` is that the eighteen-fold drop from 1,310 to 72 "reads as a small step"
on a log axis. **APHL Act 3 already solved it by going linear.** Adopting the APHL
axis fixes a listed revision for free.

**Nomenclature.** Legacy says "group" (`group diversity`, `85 analysis groups`).
APHL says "unit" and its build guide requires one name per concept across the film.

None of these is a rebuild. They are color assignments, an axis, and a word.

## 3. Both source trees exist and are editable

| what | where | size |
|---|---|---|
| Legacy five clips | `~/Downloads/ANIMO_DELIVERABLES_2026-09-09/source/scene.py` | 931 lines, 5 scene classes |
| APHL film | `~/.agi/renders/36e4638f-.../src/` + `scenes/` | 7 body files, 6 scenes |
| Shared tokens | `~/.agi/renders/36e4638f-.../src/aphl_common.py` | 3.5 KB |

This is the fact that settles the question. Earlier planning assumed the legacy
clips could only be reused as finished MP4s. They can be edited, so "apply the
pending section 11 revisions" and "bring them into the house semantics" are the
same pass over the same file.

`aphl_common.py` is the reusable layer, and it is small: the tokens, `Txt()`
carrying the Pango glyph-spacing fix, `Title()`, `Body()`, `source_note()`,
`schematic_tag()`, `case_mark()`, `small_dot()`, `genome_strip()`. Nothing in it is
specific to either film.

## 4. The architecture: one act library, two cuts

Build acts, not films. Each act is a separate render with a declared entry and exit
state, in the shared system. A film is then a concatenation order plus a narration
track. The APHL film is the short cut; the TUC briefing is the long one.

| act | content | APHL | TUC |
|---|---|---|---|
| A The question | a case, no travel history | Act 1, 40.1 s | Clip 1 act 6 |
| B Fair comparison | recombination, why partition, 85 units | Act 2, 49.4 s | Clip 2 acts 1 to 2 |
| C The window | r/m, the window, failure at both edges | Act 3, 46.2 s | Clip 2 act 3, Clip 3 acts 1 to 3 |
| D Not separable | sampling, the confound, the Americas | Act 4, rebuilt | **new to TUC** |
| E The ceiling | region yes, country no, ST92 | Act 5, 46.6 s | Clip 4 acts 5 to 6 |
| F Negative control | `7.01` | — | Clip 2 act 4 |
| G Spike-in recovery | Table 4 | — | Clip 2 act 5 |
| H Subdivision | `7.07` | — | Clip 3 act 4 |
| I Tree builder | `7.09` | — | Clip 3 act 5 |
| J Outbreak threshold | `7.12` | — | Clip 4 act 3 |
| K The 312 | the funded isolates | — | Clip 1 acts 1, 4, 5; Clip 3 act 7; Clip 4 act 7 |
| L Resistance | the AMR closeout | — | Clip 1 act 2 |

**Five acts serve both films** (A to E), at two depths. **Five are legacy scenes**
(F to J) that the TUC cut needs and the APHL cut does not, but which become
available to APHL once they are in the same system. **Two are TUC-only** (K, L).

A and D can likely be the *same render* in both films. B, C and E need a short and
a long variant, which is a parameter on one scene rather than two scenes: the APHL
cut states the result, the TUC cut walks the derivation.

## 5. What this changes about the TUC briefs

**Two corrections to the four briefs in `tuc_briefing/01_concept/`.**

First, they say "reuse `7.xx` with its pending revision applied", which implied
dropping a finished MP4 into a new series. Replace that with: rebuild the scene
from `scene.py` in the shared system, applying the section 11 revision and the
semantic realignment in one pass. Same work, better result, and it is the only way
`7.09` can be done at all since its fix changes the encoding.

Second, and this is the substantive one: **the TUC series has no confound
material.** None of the four briefs covers the fact that country and collection
history are not separable in this collection, which is the manuscript's actual
reported geographic conclusion. The APHL Act 4 being rebuilt right now covers
exactly that. It should be adopted into the TUC series, most naturally as an act in
Clip 4 before the ladder: the collection cannot settle the country question, and
then separately, neither could a better one, because of ST92.

That ordering is stronger than either film has on its own. It separates the
practical limit from the structural one.

## 6. Housekeeping found on the way

**Twenty on-screen strings in the APHL source carry an em dash**, including the
title card. The project's writing style forbids them in anything on screen, and the
APHL style guide never inherited that rule: it mentions em dashes only as a `t2s`
italic bug. Affected files: `act5_body.py` 6, `act3_body.py` 4, `act4_body.py` 4,
`act1_body.py` 3, `aphl_common.py` 3 (including `schematic_tag`), `title_body.py`
2, `act2_body.py` 1. Replacements change text width, so fold this into the acts
already being re-rendered rather than doing it as its own pass.

## 7. Order of work

1. **Rebuild APHL Act 4** to `ANIMO_ACT4_REVISION_2026-09-17.md`. Already specified.
2. **Fix the Act 3 label collision.** Layout only, no beat moves. Four elements
   overprint for about 24 seconds on the act carrying the mechanism.
3. **Sweep the em dashes** across all acts being re-rendered.
4. **Merge `scene.py` into the shared system.** Adopt `aphl_common.py` tokens, fix
   the four semantic divergences, apply the section 11 revisions to all five legacy
   scenes in the same pass. This is the biggest single item and it unblocks the TUC
   series entirely.
5. **Measure the voice.** Blocked on an ElevenLabs credential for both films.
   Nothing downstream can be timed without it, and per `long-form.md` the voice is
   measured before the delivery re-render, not after.
6. **Then narration**, per film, against measured beats on the re-rendered acts.

Steps 1 to 3 are the APHL film's critical path. Step 4 serves both and is what
makes the TUC series buildable at all. Step 5 gates both.
