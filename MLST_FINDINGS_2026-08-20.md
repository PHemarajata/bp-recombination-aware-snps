# Seven-locus MLST across the panel — findings

Written 2026-08-20. `mlst 2.23.0`, scheme `bpseudomallei`, all 2,976 assemblies,
6m48s, zero failures. Output: `MLST_v4c.tsv` (sample_id, ST, unit, role, country,
allele profile).

Run before committing to cgMLST, because MLST costs nothing and answers part of
the same question. It answered more of it than expected.

---

## 1. Why this matters more than its resolution suggests

Seven-locus MLST is far too coarse for outbreak work, and nothing here changes
that. But **ST is the common currency of the melioidosis literature** — twenty
years of published *B. pseudomallei* epidemiology is indexed by it. That makes it
the natural bridge between our units and everything already published, and it is
the typing a traditional reviewer will ask to see.

514 distinct STs across the panel; 210 genomes are novel or untypeable (`ST-`).

Most common: ST70 (n=203, Thailand 183), ST46 (n=98, China 57), ST670 (n=79, all
Thailand), ST51 (n=63, Singapore 43), ST58 (n=56), ST326 (n=39, Australia 36).

---

## 2. The headline: ST92 is a pan-Americas lineage

**Every one of the 22 genomes in the Mississippi unit `strain_4_L1_1` is ST92** —
including the single Colombian genome, despite it sitting ~486
recombination-filtered SNPs away from the Mississippi cluster.

Across the whole panel, ST92 spans **seven countries**:

| ST92, n = 36 | |
|---|---|
| USA | 26 |
| Brazil | 3 |
| Mexico | 3 |
| Colombia, Nicaragua, Guadeloupe, Martinique | 1 each |

Two of the known-exposure validation genomes are ST92 — one Mexico, one
Nicaragua — so this is not an artefact of deposit country.

This is consistent with the published description of the Mississippi Gulf Coast
isolates as a *"Western Hemisphere strain"* ([NEJM
2023](https://www.nejm.org/doi/full/10.1056/NEJMoa2306448)), and **ST92 is
independently documented as a Western Hemisphere marker** — a 2014 US traveller
returning from Mexico was typed ST92 with ITS type G, "consistent with an isolate
that originated in the Western Hemisphere"
([EID](https://pmc.ncbi.nlm.nih.gov/articles/PMC4593452/)). The exact ST
published for the Mississippi isolates themselves has still not been read off the
NEJM paper; worth doing before print, though the agreement above makes a conflict
unlikely.

### ST92 is four lineages, not one — and this is the clearest case for the WGS work

Those 36 ST92 genomes fall into **four distinct v4c units**:

| unit | n | composition |
|---|---|---|
| `strain_4_L1_1` | 22 | USA 21 (Mississippi), Colombia 1 |
| `strain_4_L1_4` | 9 | USA 4, Mexico 3, Guadeloupe 1, Martinique 1 |
| `strain_4_L1_3` | 4 | Brazil 3, Nicaragua 1 |
| `strain_pp192_L1_1` | 1 | USA 1 |

MLST alone would report all 36 as one Western Hemisphere type and lump the Gulf
Coast cluster together with Mexican, Brazilian and Caribbean isolates. The
whole-genome partition separates them into four groups, and the Mississippi one
is a tight clonal cluster (median 7 raw SNPs) quite distinct from the rest.

This is the documented **ST homoplasy** problem in this species ([Suspected cases
of intracontinental ST homoplasy resolved using whole-genome
sequencing](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5729916/)), and it is
systemic here rather than anecdotal: **52 of 279 STs span more than one unit**,
ST70 spanning eight.

**So the two layers do different jobs.** MLST places an isolate in the published
literature; only WGS says whether two ST92 isolates are actually related. Neither
attributes to a country — but that is a separate failure, and it is not fixed by
resolution.

Other Americas STs behave the same way: ST297 spans Trinidad and Tobago, USA,
Puerto Rico, Mexico and Brazil (n=13); ST95 spans Brazil, Mexico and the USA
(n=14).

---

## 3. Independent confirmation that country attribution cannot work

Applying the *same* leave-group-out rule used on the units, but attributing by
**ST instead of by unit**:

| scale | ST-based | unit-based (for comparison) |
|---|---|---|
| country | **0 / 17** | 0 / 19 |
| region | **13 / 15 (87%)** | 19 / 19 (100%) |

The two methods share no machinery — one is seven housekeeping genes with a
20-year-old public nomenclature, the other is whole-genome
recombination-corrected clustering. **They fail and succeed in the same places.**

The mechanism is visible directly in the ST table. The Philippine genomes are
mostly ST58, which in this panel is China 25, Thailand 20, Philippines 9. A
single ST spans all three countries, so no amount of resolution *within* the
typing system separates them.

**This is the strongest reviewer-facing evidence we have that country-level
attribution is a property of the organism's distribution and not a deficiency of
our pipeline.**

**Prior literature already says half of this.** It is established that MLST
"lacks the resolution to firmly link an isolate to a specific geographic origin"
([EID, Western Hemisphere
phylogeography](https://wwwnc.cdc.gov/eid/article/23/7/16-1978_article)). Our
contribution is the other half: **whole-genome, recombination-corrected
clustering does not rescue it either.** MLST failing was expected. WGS failing in
the same places is the finding.

---

## 4. Concordance with the v4c partition

Adjusted Rand Index between ST and unit assignment, over the 2,236 analysed
genomes with a numeric ST: **0.559** (279 STs vs 86 units).

- 65 of 86 units contain more than one ST
- 52 of 279 STs are split across more than one unit

Moderate agreement in both directions: our units are usually broader than an ST,
but sometimes cut one. That is the expected relationship between a seven-gene
scheme and whole-genome clustering, and it is the orthogonal check the reviews
asked for — two independently constructed views of population structure that
broadly agree without being redundant.

---

## 4a. cgMLST (added 2026-08-21) — resolution is not the limiting factor

Ran after this document was first written. PubMLST scheme 2, **4,089 loci**,
chewBBACA 3.5.4 over all 2,976 genomes (AlleleCall 181 min). Call rate is good:
median **95.5%** of loci called, 99.1% of genomes above 90%, comparable to the
98.4% the scheme's authors reported.

### The decisive comparison

Three typing layers spanning **584-fold** in locus count, scored under the
identical leave-group-out regime:

| layer | features | country | region |
|---|---|---|---|
| 7-locus MLST | 7 loci | **0 / 17** | 13 / 15 (87%) |
| cgMLST | 4,089 loci | **0 / 30** | 23 / 29 (79%) |
| core-genome SNP units | whole genome | **0 / 24** | 22 / 24 (92%) |

*(cgMLST and core-genome rows revised 2026-08-21 on the corrected 31-genome
validation set; the MLST row predates the correction and is due a re-run.)*

**Country-level attribution is zero at every resolution.** Going from 7 loci to
4,089 loci to the whole genome changes nothing. This kills the obvious reviewer
objection — *did you simply need more resolution?* — with a direct measurement
rather than an argument.

### Concordance is strong

cgMLST allelic distance versus our recombination-filtered core SNP distance,
per unit: **median Pearson r = +0.861** across the 85 frozen-basis units, 66 of
85 at r ≥ 0.7 (Lichtenegger scheme). The filed **+0.846** was the PubMLST scheme
over 88 hybrid units; on the frozen basis PubMLST gives **+0.865**, so the move
from 0.846 is the basis correction, not the scheme — the two schemes differ by a
median of **0.0005** per unit.
Two independently constructed views of the same population agreeing closely.
This is the orthogonal-typing check both external reviews asked for, and it
passes.

### cgMLST covers genomes our units cannot

It needs no analysable unit, so it places the six genomes that the core-genome
test had to report as *unattributable: no unit*. Three of five testable ones are
placed correctly at region scale (Mexico, El Salvador, Philippines). **That is a
real operational gain**: a new isolate falling outside every analysable unit is
not a dead end.

### Correction: "region attribution works" needs qualifying

The four region-scale misses are not random, and they change the claim:

| genome | true region | predicted |
|---|---|---|
| Ghana | Sub-Saharan Africa | Latin America & Caribbean |
| Nigeria | Sub-Saharan Africa | Latin America & Caribbean |
| Guatemala ×2 | Latin America & Caribbean | Europe & Central Asia |

Both African genomes fail, and the panel holds only **30 Sub-Saharan African**
genomes; the Guatemala pair is dragged to a **single** Czech genome out of 12
for all of Europe & Central Asia. So the honest statement is not *region
attribution works* but **region attribution works where the panel has reference
genomes for that region** — the same reference-density limit that defeats
country-level attribution, one scale up.

That refinement should be carried into the manuscript. It also means the
100% figure from the core-genome test is optimistic: it was scored on 19
genomes that all happened to sit in well-sampled regions.

---

## 5. What cgMLST turned out to be worth *(revised 2026-08-21, after running it)*

The prediction in this section was that cgMLST would add cross-lab
comparability and nothing to the attribution question. **Half right.** It added
three things that were not anticipated:

1. **It settles the resolution objection empirically** (§4a). Predicting that
   4,089 loci would behave like 7 is not the same as measuring it.
2. **It extends coverage to genomes with no analysable unit** — a real
   operational gain, not just a validation exercise.
3. **It exposed the reference-density limit at region scale**, which the
   core-genome test's 19 well-sampled genomes had hidden.

It also cost nothing but compute: **the supply risk did not materialise.** The
scheme is curated openly at **PubMLST as scheme 2** (4,090 loci, 1,154 profiles,
updated 2026-06-18) with a documented REST API, not only behind Ridom's
commercial cgMLST.org. Fetched with `fetch_cgmlst_scheme_bp.py`, 577 MB.

**Revised recommendation: keep cgMLST in the paper.** It is the layer that
turns "we could not attribute to country" from a claim into a result, by showing
the answer is invariant across a 584-fold range of resolution.

---

## 6. Caveats

- 210 of 2,976 genomes are `ST-` (novel or untypeable). Four of the six
  unattributable validation genomes are among them, so they are missing from
  both the ST and unit analyses for the same underlying reason: they are
  isolated.
- ST-based region attribution had 11 unattributable of 26, more than the
  unit-based test, because a novel ST has no pool at all.
- ARI is reported as a point estimate; no confidence interval.
