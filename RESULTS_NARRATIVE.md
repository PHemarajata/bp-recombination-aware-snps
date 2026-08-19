# What we did, what we found, and what it means

*B. pseudomallei* recombination-aware phylogenomics, 2,802-genome collection.
Written 2026-08-15, updated 2026-08-16 after the cold re-run and after the global
ML tree was moved into the pipeline. Plain language first, numbers attached,
caveats not buried.

**Full methods: `METHODS_DRAFT_2026-08-11.md` section 2.12**, which describes the
analysis as actually run and supersedes the earlier sections where they differ.

---

## 1. The short version

We split 2,802 *B. pseudomallei* genomes into **82 analysis units** covering
**2,070 genomes (74% of the collection)**, built a recombination-corrected
phylogeny for each, and measured how much of the genetic variation comes from
**recombination** versus **point mutation**.

Three things came out of it:

1. **Recombination dominates.** Across the 82 units the median r/m is **6.3** —
   for every SNP introduced by mutation, roughly six arrive by recombination.
   This is a highly recombinogenic organism and any analysis that ignores it
   will produce wrong trees.
2. **The population is strongly geographically structured.** **42 of 82 units
   contain genomes from a single country**, where chance would give **2**. That
   is not a sampling artefact: 40 of those 42 span multiple independent
   sequencing projects.
3. **Two software defects were corrupting the results**, both found by checking
   raw numbers rather than trusting summaries. Both are fixed, and one of them
   had been misdiagnosed for an entire prior investigation.

---

## 2. How the collection was divided, and why it matters

You cannot measure recombination across a whole species at once. Gubbins looks
for regions where SNPs are unusually dense; if you feed it several unrelated
lineages, the differences *between* lineages look exactly like dense SNP patches
and get called as recombination. The estimate comes out precise and wrong.

So the collection is divided twice:

- **PopPUNK** finds 35 "strains" — deep lineages — covering 2,395 genomes.
- **fastbaps** subdivides within each strain into **level-1 subclusters**.
- Units with fewer than 7 genomes are dropped: below that there is not enough
  signal to detect recombination at all.

That leaves **82 units, 2,070 genomes**. The rule is applied uniformly — no
strain was split because it was awkward and none left whole because it was
small. That matters because subdividing only the inconvenient lineages is
exactly the post-hoc choice a reviewer would attack.

**This is a large improvement in coverage.** The previous manual analysis
covered 37 units and 1,051 genomes (37% of the collection). We now cover 74%.

**A sanity check that matters:** 35 of the manual analysis's 37 units come out
**exactly identical** here — same genomes, same groupings. The two exceptions
are understood (one unit the manual analysis subdivided one level further, and
one where a single genome was added). That agreement is the strongest evidence
that the partition is right.

**Cost of the extra coverage, stated plainly.** 258 of the 2,070 genomes (12.5%)
come from lineages the manual analysis never screened for data quality. Broader
coverage, slightly less vetting.

---

## 3. The main result: recombination dominates

**Median r/m = 6.3** across 82 units (middle half: 2.5–9.4; full range
0.36–18.0).

r/m is the ratio of SNPs brought in by recombination to those arising by
mutation. At 6.3, recombination introduces about six times more variation than
mutation does. For context, many bacterial pathogens sit well below 1.

**The practical consequence:** a tree built from raw SNPs in this organism is
mostly describing recombination history, not descent. Every unit tree in this
analysis is built *after* removing the recombinant regions.

**Variation between lineages is real and large** — from 0.36 (a unit evolving
almost clonally) to 18.0. That spread is itself a finding: recombination rate is
not a species constant.

**Cross-check:** for the 36 units we can compare against the earlier manual
analysis — different variant caller, same everything else — the two agree within
a median factor of 1.34, and 32 of 36 agree within 2×. The residual ~1.34×
offset is a genuine, consistent difference between the two variant callers, not
noise.

---

## 4. The geography result

**Question:** do genomes from the same country sit together on the tree?

**Answer: strongly yes, and not because of how the data were collected.**

| finding | number |
|---|---|
| units containing exactly one country | **42 of 82** |
| expected by chance | **2.0** (p = 0.0001) |
| of those 42, how many span >1 sequencing project | **40** |
| single-country units spanning ≥3 projects | **33** |

The confounder had to be taken seriously. **70.5% of this collection is from
Thailand**, and the **top 3 sequencing projects are 58.4% of everything.** A
single project usually means one lab, one country, often one outbreak — so
"country" and "project" could easily be the same variable in disguise.

The test that separates them: **only 2 of the 42 single-country units come from a
single project.** The rest pool genomes from several independent studies that
nonetheless all come from the same country. Geographic structure survives.

For the 40 units that *do* contain multiple countries, we tested whether country
labels cluster on the tree more than chance (permutation test, 1,000 shuffles,
holding topology and country composition fixed). **21 of 40 show significant
clustering by country**, versus 18 of 40 by sequencing project — and 15 units
are significant for both. So *within* mixed units the two signals cannot be
cleanly separated. The clean evidence is the single-country result above.

**What this does NOT show.** Nothing here reconstructs direction of spread,
dates, or migration rates. This collection's sampling — 70% one country, more
than half from three projects — cannot support that, and no amount of analysis
will fix it.

---

## 5. Two defects that were changing the answers

### 5.1 A crash that looked like biology

Six analysis units failed with Gubbins reporting *"Unable to fit model to data"*.
The prior investigation ruled out species misidentification, assembly quality,
contiguity, GC content, ambiguous bases, cluster size and clonality — none
explained it — and concluded that three particular reference genomes were
somehow toxic, so they were blacklisted and 6 of 34 units written off.

The real cause: **RAxML crashes (segfault) when its run-identifier reaches 128
characters.** Gubbins builds that identifier from the reference genome's FASTA
header. The three "bad" references simply had long filenames. Gubbins caught the
crash in a catch-all and reported it as a model-fitting failure.

Settled by holding the alignment **byte-identical** and changing only the
filename: run-id 136 fails, run-id 65 succeeds. Repeated over all six units:
**12/12 now succeed against the reference that had "broken" them.** The blacklist
is empty; no reference is bad.

This was not academic. **40 of 164 replicon-units in this very run (24%) would
have crashed**, including one of the largest, before the headers were normalized.

### 5.2 An outgroup inflating the clonal signal

The pipeline keeps the mapping reference in the tree as an extra tip. Because
that reference sits outside the population, its branch is enormous — in one unit
it carried **7,307 of 7,574** SNPs assigned to "not recombination". Those are
differences between the population and an outsider, not evolution within it, and
they were landing in the denominator of r/m.

Across the run, **52% of all non-recombinant SNPs came from those reference
branches.** Excluding them moves the median r/m from **1.85 to 6.30**.

The correction is validated against the manual analysis: the disagreement that
looked like a reference-distance effect (correlation −0.589) drops to −0.137,
and agreement tightens from a 0.40–1.54 spread to 1.26–1.64.

**Honest note on how this was found.** The first diagnosis was wrong. It looked
like an interaction between the variant caller and reference distance, and 50 of
82 units were nearly discarded on that basis. The correlation was real; the
explanation was not. What broke it open was the cheapest possible check — sorting
the per-branch numbers, where a single branch held 96% of the signal. That check
should have come before any correlation was computed.

---

## 6. What you can hand to someone

| file | what it is |
|---|---|
| `L1_ASSIGNMENTS.tsv` | every analysed genome: strain, subcluster, unit r/m, reference, country, project, date. 99.9% metadata coverage |
| `RM_RESULTS_L1_CORRECTED.tsv` | per-unit r/m, corrected. **Use `rm_corrected`, not the uncorrected column** |
| `L1_TREES_SUPPORTED/` | 164 recombination-corrected ML trees with SH-aLRT and UFBoot support |
| pipeline stages | the global ML tree is now generated by the workflow itself (`--global_ml_tree`, commit `f1a7d13`); it was built by hand for this run and the two agree exactly — 82 tips, 79 internal nodes, 64 (81%) at UFBoot >= 95 |
| `L1_out/Clusters/*/Gubbins/` | per-unit recombination predictions and Gubbins trees |
| `L1_GLOBAL_ML_TREE.nwk` | **global ML tree over the 82 units with SH-aLRT + UFBoot** — parsnp core alignment (82,514 variable sites), GTR+ASC. 64 of 79 internal nodes (81%) at UFBoot >= 95 and SH-aLRT >= 80 |
| `L1_GLOBAL_BACKBONE.nwk` | quick Mash-distance NJ backbone over the same 82 medoids. No support values; superseded by the ML tree above for anything quantitative |
| `L1_unit_medoids.tsv` | per-unit medoid, dominant country, project count |
| `PHYLOGEOGRAPHY_ASSOCIATION.tsv` | per-unit country and project clustering tests |
| `RUN_STATS_ARCHIVE/L1/` | the raw per-branch statistics r/m is computed from |

**Two warnings about the global trees.**

`L1_GLOBAL_BACKBONE.nwk` has branch lengths in Mash distance, while the per-unit
trees are substitutions per site. Different units — do not graft them together
and do not date the result. The ML tree does not have this problem.

`L1_GLOBAL_ML_TREE.nwk` is **not recombination-corrected, and must not be.**
Gubbins finds recombination as regions of unusually dense SNPs against a clonal
background; across 82 divergent lineages there is no shared clonal background, so
it would call most of the alignment recombinant. That is exactly the failure the
partition exists to prevent. The global tree therefore shows how the units
relate, with branch lengths that include recombination, and **no r/m may be
computed from it.** r/m comes only from within-unit analysis.

---

## 7. The run itself

82 units, 2,070 genomes, **164/164 replicon-units completed at the highest
confidence tier, zero failures.** 10.5 hours on a 20-core workstation, of which
89% was read mapping. The analysis was then re-run cold from an empty cache and a
fresh work directory in 11.0 hours; the two runs agree exactly — 82 of 82 r/m
values identical to 4 decimal places and 164 of 164 Gubbins trees byte-identical
(see `CLEAN_RUN_COMPARISON.md`). Retuned for a 128-core machine, the mapping stage
projects to under an hour.

Large lineages are still subdivided even on big hardware, and the reason is
worth stating: Gubbins on one unit is **one task**. Its runtime grows sharply
past ~155 genomes — a 917-genome unit was still inside its first of five
iterations after 10.5 hours. No number of cores shortens a single task. Cores
buy throughput across units; only subdivision shortens the longest job.
