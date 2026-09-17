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

## Why the panels differ: it is one line of work, not two datasets

**Corrected 2026-09-17 by the project lead.** An earlier version of this note said
the only difference was country breadth. That was incomplete.

**The initial clustering came first.** It placed the study isolates in a global
tree, and that is where the 2,773-genome framework comes from. The work then moved
on in three ways:

1. **More isolates**, added specifically to represent more countries.
2. **A refined clustering algorithm.**
3. **A determined detection window**, which is what clip 2 is about.

So the two panel sizes are two points on one progression. The later panel exists
*because* the first one had been built. They are not competing analyses and the
second does not contradict the first.

**If asked what "refined" means, the answer is specific.** The first clustering
leaned heavily on the mash distance matrix, and **every cluster was silently capped
at 200 members**. Cluster counts and memberships from that stage are artifacts of
the cap rather than properties of the collection, which is why no clip presents
them and why the algorithm was replaced.

**Nothing that matters depends on that stage.** The closeout's conclusion that
clinical and environmental isolates are drawn from one population rests on 19
shared sequence types and on environmental genomes sitting throughout the
phylogeny. Neither uses the clustering. Clip 1 act 5 corroborates the same
conclusion using our own 85 analysis units, which are a different object built on
the expanded panel with the refined algorithm.

**Why the expansion was needed at all.** The closeout asked how the Nakhon Phanom
collection sits inside global diversity, and 35 countries is ample for that. This
work asks whether a genome can be placed to the country it was acquired in, and a
country with no genomes in the panel cannot be predicted at any resolution. That
is why the growth went into countries rather than into Thailand.

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
