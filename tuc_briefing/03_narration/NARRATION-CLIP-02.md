# TUC clip 2 narration, draft 1: text settled, placement blocked

Written 2026-09-17 against `~/Downloads/TUC_CLIP2_2026-09-17/`. **The text is
settled. The timings are provisional and cannot be finalized, because the picture
front-loads its activity and the narration cannot be placed on it.**

## The blocker, measured

Every new act ends its visible activity long before the act ends. The builder used
a `hold_to(T)` helper that pads with one long wait to hit the brief's stated
seconds, so the padding is systematic rather than accidental.

| act | duration | last visible change | longest frozen stretch | share |
|---|---|---|---|---|
| title card | 5.0 s | 2.8 s | 2.2 s | 44% |
| 1 | 48.0 s | 35.0 s | 13.0 s | 27% |
| **2** | 54.0 s | **22.1 s** | **31.9 s** | **59%** |
| 3 lead-in | 17.0 s | 11.8 s | 5.2 s | 31% |
| 4 lead-in | 17.0 s | 12.0 s | 5.0 s | 29% |
| **5** | 45.0 s | **25.5 s** | **19.5 s** | **43%** |
| **6** | 29.0 s | **14.7 s** | **14.3 s** | **49%** |

Placing the text below on those beats gives **14 line-boundary violations and four
lines that begin after the picture has stopped moving**, including act 2's closing
line, which would speak over a frozen frame for 21 seconds.

Both failures are one thing seen twice: the beats cluster in the first 40% of each
act, so consecutive beats sit 2 to 5 s apart while lines need 5 to 7, and then
nothing happens for the rest.

## Stretching the waits is not enough, and I checked before assuming

| act | stretch needed to fill | longest resulting hold |
|---|---|---|
| 1 | 1.46x | 3.8 s, acceptable |
| 3 lead-in | 1.31x | 2.4 s, acceptable |
| 4 lead-in | 1.22x | 1.7 s, acceptable |
| 2 | **3.15x** | 8.2 s |
| 5 | **4.04x** | 8.1 s |
| 6 | **3.86x** | 5.4 s |

Acts 2, 5 and 6 would need five to eight second holds on single lines. **And
shortening them instead does not work**, because the narration needs the runtime:
act 2's 120 words are 40 s of speech in a 54 s act. The act length is right and
the picture is too sparse for it.

So acts 2, 5 and 6 need **more visual beats**, not different waits. Acts 1, 3 and
4 need only the modest stretch above.

## What can be split without inventing content

Act 2 reveals several things in combined plays that can each become their own beat,
which is what fixed clip 1 act 3's pacing:

- the two clades, currently one `FadeIn` for both, and their two labels likewise
- the caveat's two lines
- the verdict's two lines
- the axis, its ticks, its labels and its caption, currently two plays for four things

Six more beats in act 2 alone, at no cost in content.

## The text

Budgets are the brief's. Rate is Justin's **measured 179 wpm on `eleven_v3`**, not
the 168 the brief assumes.


### Act1. Why the obvious approach fails

*48 s, 112 words against a 110 budget*

** 3.25** (provisional)  Start with the process, not the measurement. In this species DNA moves between lineages as well as down them.

** 8.52** (provisional)  So when two genomes differ, that difference has two possible origins: mutation accumulated over time, or a block that arrived from elsewhere.

**14.13** (provisional)  The ratio between those two contributions is r over m, and everything downstream depends on it.

**19.85** (provisional)  Now the trap. You can compute one r over m for the whole species, and it will return a number.

**27.48** (provisional)  That number is meaningless, so it is not shown here. Clip three shows it where it belongs, as the thing being corrected.

**35.07** (provisional)  The reason it is meaningless is biological, and it is the next act.


### Act2. Partition first, because the biology says so

*54 s, 105 words against a 120 budget*

** 2.60** (provisional)  The reason is a barrier that exists in the biology. Consider two clades of this organism.

** 7.40** (provisional)  Restriction-modification systems differ between clades, and they restrict which DNA a cell will accept from outside.

**13.00** (provisional)  So a block crossing from one clade to the other is often stopped before it can recombine.

**16.30** (provisional)  That makes genomic clades behave as functional units of genetic isolation, not merely as branches on a tree.

**21.10** (provisional)  The evidence comes from a hundred and six strains in one restricted Asian locale. Whether it holds globally is untested.

**26.57** (provisional)  Averaging across a barrier that exists in nature is not a shortcut. Partitioning first is a biological requirement.


### Act3Leadin. How the detector actually works (lead-in)

*17 s, 38 words against a 40 budget*

** 2.27** (provisional)  Whether an excess of density is visible depends entirely on the background it has to stand out against.

** 6.90** (provisional)  So the same imported block can be obvious, or invisible, depending only on how diverse its unit happens to be.


### Act4Leadin. Does it invent recombination? (lead-in)

*17 s, 38 words against a 40 budget*

** 2.60** (provisional)  Before trusting any of it, the detector has to be shown not to find recombination where none exists.

** 7.30** (provisional)  One thousand five hundred nineteen replicates across sixty two unit replicons, and twenty of them returned any call at all.


### Act5. Does it find what is really there?

*45 s, 95 words against a 100 budget*

** 3.00** (provisional)  The other half of the control asks the opposite question. Can it find recombination that is definitely there?

** 6.90** (provisional)  Implant tracts of known length, from donors of known divergence, then count how many come back.

**12.80** (provisional)  At a donor divergence of one in two thousand, which is what this organism actually shows, nineteen of twenty one tracts are recovered.

**17.80** (provisional)  Below that, recovery falls away: forty percent, then twenty. Above it, it stays high but does not keep climbing.

**25.57** (provisional)  So the floor of the window arrives here a second time, from a different direction than the negative control.


### Act6. What you now have

*29 s, 55 words against a 65 budget*

** 2.17** (provisional)  So here is the instrument. It returns essentially nothing when there is nothing to find.

** 6.90** (provisional)  It recovers nine tenths of what is there at the divergence this organism shows.

**10.32** (provisional)  And it works only between a measured floor and a measured ceiling.

**14.77** (provisional)  Both bounds are brackets, not points. Clip three points this ruler at the data.


---

## Not duplicating the reused clips, which was a real risk

Acts 3 and 4 hand off to `7.03` and `7.01`, and both already carry narration in
`TUC_LEGACY_MERGED_2026-09-17/narration_corrected/`. Three collisions avoided:

- `7.03` already opens "The detector looks for a local excess of SNP density", so
  the act 3 lead-in does **not** say that. It says only that whether the excess is
  visible depends on the background.
- `7.03` already says "It never changes. Only the background around it does", so a
  drafted third lead-in line saying the same thing was cut.
- `7.01` already opens on the no-template control analogy, so the act 4 lead-in
  carries the counts instead: 1,519 replicates, 62 unit-replicons, 20 returning a
  call.

**Still outstanding on the reused side**, per the brief: `7.03`'s counted-as bars
and its hide-the-outline beat have no narration line, and the brief calls the first
of those the mechanism the whole series rests on. Those lines go into `7.03`'s own
file and need its beat map.

**443 words** across the six new acts against a 475 budget. The gap closes once the
picture is re-paced and the lines can spread.
