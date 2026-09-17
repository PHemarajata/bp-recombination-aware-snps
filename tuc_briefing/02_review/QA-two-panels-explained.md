# Q&A: why there are two panel sizes, and what actually differs

Not for the clip. This is for answering the question if it comes up.

## The short answer

They are the same collection, counted at two different times, for two different
questions. The closeout placed the Nakhon Phanom isolates in a **2,773-genome,
35-country** framework. This work uses a **2,976-genome, 50-country** panel. The
second is the first, later and wider.

## What is identical

**The isolates at the center.** All 312 confirmed isolates are in our panel:
259 IP and 53 IE, verified by sample prefix in `L1v4c_MERGED_METADATA.tsv`. Both
frameworks are built around the same sequencing.

**The Thai component.** Thailand is 1,754 genomes in the closeout framework and
1,753 in ours. **One genome.** That is the number to lead with if anyone doubts
they are the same collection: two panels assembled independently from the public
archives would not agree to within one genome out of seventeen hundred.

## What differs, and by how much

| | closeout | this work | difference |
|---|---|---|---|
| genomes | 2,773 | 2,976 | **+203** |
| countries | 35 | 50 | **+15** |
| Thailand | 1,754 | 1,753 | -1 |

**The growth went into countries, not into Thailand.** 203 more genomes bought 15
more countries. Our panel is 19 Asian countries holding 2,483 genomes, and 31
non-Asian countries holding 478.

## Why the panels differ: the two questions need different things

The closeout asked **how the Nakhon Phanom collection sits inside global
diversity**. For that you need enough global diversity to place things against,
and 35 countries is ample. Adding a fifteenth country in the Americas would not
change the answer.

This work asks **whether a genome can be placed to the country it was acquired
in**. For that the panel must actually contain the candidate country. A country
with no genomes in the panel cannot be predicted at any resolution, no matter how
good the method is. So the panel had to be widened, specifically into the places
a US or European case might have been exposed.

That is the whole difference: **breadth of countries, added because attribution
needs references and diversity assessment does not.**

## The honest limit, and it is worth volunteering

The expansion bought breadth, not depth. **28 of the 50 countries are represented
by five genomes or fewer, and together those 28 countries hold 53 genomes**, under
2% of the panel. That is exactly why the defensible result is region rather than
country, and it is better to say so first than to be asked.

## What cannot be answered from here

**Which 203 genomes.** The genome list behind the closeout's 2,773 is not in this
repository; that figure comes from the closeout deck, slides 25 and 26. The +203
and +15 above are differences of totals, not a reconciled membership diff. If the
exact set difference is ever needed, it needs that list.

## One trap to expect

Our own panel has **three legitimate counts at different stages**, and a reader
who has seen another document may quote a different one:

| count | what it is |
|---|---|
| **2,976** | assemblies as submitted to PopPUNK. **This is what the clip says**, and it is what the partition was run on |
| 2,959 | after removing 17 duplicate BioSamples (`PANEL_DUPLICATES_2026-08-21.tsv`) |
| 2,955 | a 2026-08-21 snapshot taken while four later-retired exclusions were still active. Superseded; do not quote |

`NUMBERS.tsv` says to quote 2,959 as the corrected panel figure. The clip says
2,976 because that is the number the 85 units were actually built from. Both are
right for what they describe. If challenged: **2,976 went in, 2,959 are unique
BioSamples, 2,340 were large enough to analyse.**
