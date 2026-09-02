# Should we redo everything from scratch?

**No. Recommendation: fix 4 units, answer 2 methodological questions, and build
one generated numbers file. Do not re-partition, do not re-run the SNP pipeline,
do not rewrite the corpus.**

The reasoning, with the evidence.

---

## 1. "Inconsistency" is three different problems wearing one name

Separating them is most of the decision.

### A. Documentation drift, ~90% of what we hit

"9 of 16" vs "7 of 15". 44% vs 41.4%. 33% vs 5%. Mexico +13 vs +17. 26 vs 31 vs
44 vs 45 validation genomes. 4.9x vs 2.2x. 92% vs 71%. Panel 2,976 vs 3,016 vs
3,033. The phantom "Ashcroft" citation.

**Every one of these is a number recorded once, copied between documents, and
never re-derived.** None is two analyses disagreeing. In each case, when I
recomputed from the primary table, there was one right answer and the code had
been right all along.

**A rewrite does not fix this.** The mechanism that produced it (write a figure
into prose, copy it onward, never regenerate) survives any rewrite, and the drift
reaccumulates. This is the single most important point in the memo.

### B. Real data defects, small and now enumerated

Four register-excluded genomes in the panel. Two BioSample duplicates in the new
batch, one causing a leave-group-out leak. Sixteen intra-panel duplicate
BioSamples. One unflagged Mexico exposure.

These are real and worth fixing. **They are also bounded, and we now know
exactly how bounded** (§3).

### C. Genuine methodological questions, two of them

1. **Every gate was calibrated under `ska map` and applied to Snippy data**,
   while the project's own measurement says there is no stable caller correction
   factor (r/m shifts -15% to +76% with no consistent sign).
2. **Production used `GTR+ASC`; the calibration section argues against it** on
   these data, because in a 68% GC genome ASC collapses base composition toward
   25/25/25/25 while true `-fconst` counts reproduce it.

**Only category C could justify re-running anything, and only for r/m.**

## 2. Where analyses have actually been repeated, they agree

This is the evidence a redo would be redundant, and it is strong:

| test | result |
|---|---|
| Track A (workstation) vs A100, 82 identical-membership units | median \|Δr/m\| **0.0145 (0.38% relative)**, max 1.32 |
| clean run vs incrementally resumed | **82/82 units identical to 4 d.p.**, **164/164 Gubbins trees byte-identical** |
| accidental repeat of one n=90 unit | r/m **4.54 vs 4.55**, tract 5,684 vs 5,694 bp |
| phylogeography survivors, 86-unit vs 88-unit partition | agree on **6 of 7** |
| validation-genome co-membership, v4b vs v4c | **94.3%** (198/210 pairs) |
| headline attribution, across MLST / cgMLST / core-SNP units | same answer, and **two of the three use no partition at all** |
| cgMLST across two independent schemes (PubMLST 4,090, Lichtenegger 4,221) | same conclusions |

**The redo has effectively already been run, several times, and it passed.**
Today added another: a completely independent method (cgMLST call rate on a new
scheme) ranked every previously-flagged genome at the bottom of a 3,031-genome
panel without being told to.

## 3. The real contamination is 4 units out of 86

I traced every known data defect to the units it touches:

| unit | n | defect |
|---|---|---|
| `strain_1_L1_26` | 154 | register-excluded `SRR2896257` (60.8% cgMLST call rate) |
| `strain_1_L1_8` | 91 | 2 duplicated BioSamples |
| `strain_14_L1_4` | 14 | 2 duplicated BioSamples |
| `strain_1_L1_10` | 7 | **3 duplicated BioSamples** |

**4 of 86 units. 266 of 2,352 genomes. 82 units and 2,086 genomes are
untouched.**

`strain_1_L1_10` deserves attention: n=7 with 3 duplicate pairs means **4 distinct
isolates**. It sits exactly at the n>=7 analysis floor, so it should not exist as
a unit at all. That is a real result, not just a cleanup.

**A full redo would re-derive 82 clean units to fix 4 dirty ones.**

## 4. Redoing has a real chance of making things worse

The project's own history is the argument. Every re-partition introduced new
defects:

- **v4 was broken**: built from v3's *analysis subset*, silently dropping 521
  genomes including 4 of 5 Mississippi. The headline numbers looked healthy.
- **v4b** lost 108 genomes that v3 had analysed, to finer subdivision.
- **v4c** needed its own debugging, and produced the `strain_4` label collision
  where the same name means two disjoint genome sets in two files.

Plus the standing hazards: Gubbins' unseeded `randint(0, 10000)` gives a
**~16% chance per full run** of silently losing a unit; `errorStrategy 'ignore'`
means a clean exit does not establish that every unit succeeded.

**A redo is not a return to a known-good state. It is a new run with its own new
errors, and the base rate for this pipeline is not low.**

## 5. What the two papers actually depend on

This is what finally settles it.

**Paper 1 (attribution) barely touches any of this.** Its evidence is cgMLST
(no units), MLST (no units), the validation set, and the sampling frame. Today it
was re-run end to end on a fresh published scheme, an expanded panel, with
duplicates dropped and the leak closed. **Paper 1 has already been redone.**

**Paper 2 (the r/m operating envelope) is where category C bites.** The gates
were calibrated under one caller and applied under another, and `+ASC` vs
`-fconst` is unresolved. That is a real, scoped problem, and it does not require
re-partitioning to address.

## 6. What I would do, in order

**Tier 1: data fixes. Hours, no pipeline re-run.**

1. Drop the 4 register-excluded genomes and the 2 new-batch duplicates.
2. Resolve the 16 intra-panel duplicate BioSamples, keeping one copy each.
3. **Re-derive only the 4 affected units.** Not 86.
4. Re-check whether `strain_1_L1_10` still clears the n>=7 floor. It probably
   does not.
5. Add a **BioSample-level** duplicate check to ingest. Accession-level checking
   is what let this through, twice.

**Tier 2: the numbers freeze. Half a day, highest value per hour spent.**

Write one script that recomputes every quotable figure from the primary tables
and emits a single `NUMBERS.tsv`. Every document cites that file instead of
restating a value. `GENOME_REGISTER_2026-08-21.md` is the right idea but it is
still prose, so it will drift like everything else.

**This is the only item that prevents recurrence.** Without it, a full redo
produces a fresh set of documents that start drifting the next day.

**Tier 3: the two real methodological questions. Days, scoped to Paper 2.**

6. Quantify `+ASC` vs `-fconst` on one unit. The methods draft already lists this
   as an open item.
7. Recompute Gate 1 diversity from alignment-derived distances instead of the
   Mash proxy the project itself retired for exactly this use.
8. Either justify the ska-calibrated gates on Snippy data, or restate every
   ska-derived threshold as provisional in print. **Restating is honest, cheap,
   and probably sufficient.**

**Do not do:** re-partition (Phase 2), re-run the SNP pipeline wholesale, or
rewrite the corpus.

## 7. The honest counter-argument

If Paper 2 is going to make strong quantitative claims about r/m in this species,
then a re-run under a single caller with gates calibrated on that caller is the
defensible thing to do, and item 8 above is a mitigation rather than a fix.

**My answer: scope Paper 2 to what survives.** The transferable contributions do
not depend on the absolute r/m value:

- union coverage is size-confounded (r = +0.80 with log n)
- the reference-taxon artifact (52% of outside-recombination SNPs)
- tree-builder equivalence is per-class, not universal
- Gubbins vs ClonalFrameML re-scales but does not re-rank
- nu and delta are anti-correlated at -0.79, so nu is never interpretable alone
- the matched null (1.32% false positives) and spike-in (91% recovery)

**Every one of those is a statement about method behavior, and none needs the
absolute r/m number to be exactly right.** Lead with those, report r/m with its
bracket and its caller caveat, and the caller question stops being load-bearing.

## 8. One sentence

The analyses are consistent and have been independently reproduced; the
*documents* are not, and the fix for that is a generated numbers file plus four
re-derived units, not a rewrite that would reaccumulate the same drift while
risking the new-run errors this pipeline reliably produces.
