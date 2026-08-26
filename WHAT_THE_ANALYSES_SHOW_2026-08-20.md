# What the analyses show — plain language

Written 2026-08-20. A non-technical companion to
`ATTRIBUTION_AND_DISTANCES_FINDINGS_2026-08-20.md`, which holds the numbers,
methods and file paths. This one is for explaining the work to a collaborator, a
CDC contact, or a reviewer's first read.

---

## The headline

**We can say which part of the world a case came from. We cannot say which
country.**

That reads like a limitation, but it matches the question people ask first. For a
US patient with no travel history the operational question is *did they acquire
this domestically or abroad, and if abroad, roughly where* — and that we can
answer. "Which country" we cannot, under any method tried.

On the 19 genomes where the true exposure country is known, regional attribution
was correct every time, against 58% from always guessing the most common region.
Country-level attribution was correct **zero** times.

---

## The result that is immediately usable

The Mississippi cluster is genuinely tight: 21 genomes all within about 20
mutations of one another, and the nearest other thing in the entire collection is
roughly 500 mutations away. There is no ambiguous middle ground.

That gives a clean operational test. **A new Gulf Coast isolate either falls
inside that cluster or it does not, and the call is never borderline.** This is
probably the most directly actionable output of the project so far.

The flip side: because the nearest outside relative is ~500 mutations away, we
cannot say where the Gulf Coast lineage originally came from. The Colombian
genome is the closest relative we have, not a close relative.

---

## Why country-level attribution fails

Two separate reasons, and the distinction matters.

**Missing reference genomes.** We hold no Philippine genomes except the
ground-truth ones themselves. You cannot match a sample to a country you have no
samples from.

**The lineages do not respect borders — and this is the more important one.**
Attribution failed *even where we did have the country.* Three Mexican cases had
genuine Mexican reference genomes sitting in their own cluster and the method
still guessed wrong. A single Americas lineage spans Mexico, Puerto Rico, Brazil
and the Caribbean. So this is not purely a sampling gap that more sequencing
fixes; it is partly how the organism is actually distributed.

---

## An independent check that says the same thing

We also typed every genome with the standard seven-gene scheme the melioidosis
field has used for twenty years — a completely different method, with no shared
machinery. It reaches the same conclusion: attributing to a **region** works
(13 of 15), attributing to a **country** does not (0 of 17).

You can see why directly. The Mississippi lineage is **ST92**, and ST92 turns up
in the USA, Brazil, Mexico, Colombia, Nicaragua, Guadeloupe and Martinique —
seven countries. The Philippine cases are mostly **ST58**, which is also found in
China and Thailand. These types simply span continents.

That is the strongest thing we can say to a sceptical reviewer: **the failure to
name a country is a fact about where the organism lives, not a shortcoming of our
pipeline.**

## The trap worth remembering

**The countries you most need to identify are the ones least likely to work.**

Six of the 26 ground-truth genomes could not be placed at all, because they fell
into clusters too small to analyse. Four of those six were the *only* genome from
their country in the whole collection. Rare origin means small cluster means
unanalysable — and it bites hardest on exactly the imported cases that matter
most. The effect is self-reinforcing and will not go away on its own.

---

## Two cautions for anyone interpreting this

**Most apparent geography cannot be separated from study batch.** Of 85 clusters,
only 6 show geographic clustering that survives asking "or is this just because
one lab sequenced all of these together?" Twelve cannot be separated from study
of origin. When a map appears to agree with the genomics, 6 is the number to hold
in mind.

*(Updated 2026-08-26. Previously "of 88 clusters ... thirteen are outright
confounded", which used the A100 control partition and overstated the verdict.
Of the twelve, only 2 have batch structure confirmed after multiple-testing
correction and 4 show none at all, so "outright confounded" was too strong; the
honest reading is that the two explanations cannot be told apart in this panel.)*

**Raw mutation counts are badly misleading in this organism.** About 90% of the
differences between any two genomes are imported DNA rather than inherited
mutation. The Colombia-to-Mississippi comparison falls from ~1,130 differences to
~490 once that is stripped out. Any distance quoted without saying which kind it
is means very little.

---

## How confident to be

**Nineteen scorable genomes is not many.** The regional result is clean and
consistent and it does not degrade under the stricter test, but it rests on a
small validation set in which four of the five source countries are represented
by one or two genomes. Describe it as *well-supported*, not *established*.

One methodological question is still open and should be settled before any claim
about analysis quality: **which clusters count as "good enough to analyse" turns
out to depend on which recombination tool you ask** — about 17% of them change
verdict. That is what the A100 job is for.

---

## One-paragraph version

Across ~2,900 genomes we can place a *Burkholderia pseudomallei* case to a world
region but not to a country, because the lineages span whole continents and
because most countries are thinly sampled. Regional placement was correct on all
19 cases with known exposure, against a 58% baseline. The Gulf Coast (Mississippi)
lineage is tight and unambiguous enough to serve as a direct operational test for
new US cases. Most apparent geographic structure elsewhere is confounded with
which laboratory did the sequencing, and roughly 90% of the genetic differences
between any two isolates come from recombination rather than inheritance, so
uncorrected genetic distances should not be used.
