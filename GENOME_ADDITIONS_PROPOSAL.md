# Contextual genome additions — proposal (2026-08-16)

Prepared while the v3 partition run is in progress. **No download is recommended
until that run completes and its r/m / coherence checks pass** — adding data now
would confound the partition change with the dataset change, which is the exact
trap the v3 run is designed to avoid.

Counts are ENA `sample` records for *B. pseudomallei* (taxid 28450) by country,
split into what the collection already holds (matched on BioSample/assembly
accession) and what is genuinely new. Held/new matching is by accession prefix,
so "new" is an upper bound; some are re-releases under a second accession.

## The reframing this rests on

The v3 partition retains every genome, but 517 sit in units too small for
Gubbins. **38 of those units (177 genomes) are within 1–3 genomes of the n=7
analysis threshold.** So an addition does two jobs at once: it adds the new
lineage, and it can *rescue* genomes already in hand by giving an orphan unit
enough members to cross the threshold. That rescue effect is what makes small,
targeted downloads worth more than their raw count.

## Tier 1 — highest value, small, and rescues held data (~90 genomes)

| country | new available | rescues a near-threshold unit? | why |
|---|---|---|---|
| **Mexico** | 17 | yes (1 unit, `strain_9_L1_8`, n=6) | 9 held + 17 new ≈ 26; a defensible Americas lineage instead of an orphan sextet. Serves origin attribution directly. |
| **Ghana** | 17 | no | The **only African data in the collection** (5 held). 22 total moves the Gee/Chewapreecha African-origin question from *untestable* to *visible*. Highest intellectual value per genome. |
| **Brazil** | 37 | no | Ceará clade (Gee et al. 2021, *mSphere* 6(1):e01259-20, PMID 33536328). Anchors the South American end of `strain_9` and tests whether it is one Western-Hemisphere clade or several. |
| **Colombia** | 14 | no | Fills the northern–South-America gap between the Caribbean and Brazil. |
| **Nigeria** | 10 | no | Second African country; pairs with Ghana to make "West Africa" more than one point. |

Tier 1 is ~90 genomes, every one from a country currently at 0–9 in the
analysis, and none large enough to disturb the PopPUNK fit.

## Tier 2 — rescues held data, modest new lineages (~50 genomes, optional)

Countries where the collection already holds a near-threshold unit and a few new
genomes would convert it to analysable: **Myanmar** (0 held in analysis, 16 new,
1 unit at n=4), **Papua New Guinea** (9 new, 1 unit), **Laos** (32 new, 3 units),
**Malaysia** (97 new, 1 unit). Take only enough to lift each target unit over 7,
not the whole country — 3–4 genomes apiece.

## Tier 3 — the singletons (~6 genomes, free)

Nicaragua 1, El Salvador 1, Indonesia 7. Each converts a guaranteed
non-match into a possible correct match. State explicitly in any writeup that
n=1 supports only "this lineage exists here," nothing about frequency.

## Explicitly deferred

- **Cambodia (540 new).** A 19% expansion of the collection. It *will* reshape
  the PopPUNK fit and every unit downstream — that is a collection redesign, not
  an addition, and must be scheduled on its own, after v3 is settled. If wanted
  sooner, sample 50–100 spanning its ST diversity rather than taking all 540.
- **Australia (1,487 new) / India (100) / China (68).** The collection already
  holds far more of these than it can analyse (Australia 282 held, 84 analysed).
  The bottleneck is not sampling — it is that these are deep, diverse lineages
  that fragment into small units. More Australian genomes would rescue some of
  the 13 near-threshold Australian units, but at the cost of pulling the fit
  toward Australasia. Revisit only with a specific question.
- **Philippines (13 new).** **Do not add to the reference panel.** 12 of the 13
  are the CDC travel-associated US cases that constitute the *validation set*;
  adding them to the panel and then testing against them is circular. Only 1
  genome was truly isolated in the Philippines. Use the 12 as a **proxy-panel
  experiment** instead (see below), not as reference data.

## The proxy-panel idea (method, not a download)

For countries with travel cases but no endemic sampling — the Philippines being
the extreme case — test whether the CDC `ex <country>` travel isolates
themselves form a country-specific cluster that can serve as a proxy reference.
Validate where ground truth exists (Vietnam, Thailand have both travel cases and
real genomes) before trusting it where it does not. If it holds, it is a genuine
contribution: attribution for countries that will never be sampled endemically.

## Metadata standard for anything pulled

A **reference** genome needs provenance (country + ideally year/source); a
**test** genome needs exposure history. Country-only metadata is adequate for a
reference and should not disqualify a Tier-1/2 download. Pull via ENA, never
NCBI efetch for SAMEA/SAMD accessions, and diff requested-vs-returned accessions
on every batch (the efetch prefix-stripping bug returned a human cell line for a
*B. pseudomallei* accession earlier in this project).

## FINAL MANIFEST (built 2026-08-16) — `ADDITIONS_MANIFEST.tsv`, 234 genomes

| tier | target | take | available | already held |
|---|---|---|---|---|
| **T0** | **Mississippi (PRJNA942243)** | **18** | 18 | 5 |
| T1 | Brazil | 37 | 37 | 0 |
| T1 | Ghana | 17 | 17 | 5 |
| T1 | Mexico | 17 | 17 | 9 |
| T1 | Colombia | 14 | 14 | 0 |
| T1 | Nigeria | 10 | 10 | 0 |
| T2 | Myanmar | 16 | 16 | 0 |
| T2 | Laos | **12** | 32 | 16 |
| T2 | Malaysia | **12** | 97 | 63 |
| T2 | Papua New Guinea | 9 | 9 | 1 |
| T3 | Indonesia / Nicaragua / El Salvador | 9 | 9 | 0 |
| T4 | Cambodia (stratified by year) | 50 | 540 | 0 |
| T5 | Philippines (**proxy panel only**) | 13 | 13 | 0 |

**Tier 2 sizing rule.** Take everything where the country currently has **zero**
analysed genomes — there every genome is new lineage coverage (Myanmar, PNG).
Cap at roughly 4x the measured shortfall where the country is already well
represented and the only gain is rescuing one unit: Laos has 46 analysed and a
7-genome shortfall across 3 units, Malaysia has 61 analysed and a 3-genome
shortfall in 1 unit. Taking all 97 Malaysian genomes would buy almost nothing
the 61 already held do not. This drops Tier 2 from 154 to 49.

Cambodia is sampled stratified across collection year (10 per year, 2020-2024)
rather than taken whole, so the 50 span the country's diversity instead of one
study.

## T0 — Mississippi is now the first priority

`strain_9_L1_2` holds 5 genomes from the Petras et al. *NEJM* 2023 investigation
([10.1056/NEJMoa2306448](https://doi.org/10.1056/NEJMoa2306448)) — 2 clinical
(blood, 2020 and 2022) and 3 environmental (2 soil, 1 water), the first
documented environmental establishment of *B. pseudomallei* in the continental
United States. Our geography-blind partition placed them in `strain_9`, the
Western Hemisphere clade, independently reproducing CDC's own call.

**PRJNA942243 holds 23 samples; we have 5.** The other 18 include 2023 clinical
cases and further soil/water isolates. Pulling them takes the unit from n=5
(assign-only, unanalysable) to n=23 — comfortably an analysis unit, and the best
case-to-environment linkage in the entire collection.

## Origin ambiguity — 2 genomes, handle with a field not a fudge

Exactly two genomes have an origin that is not a single country:
`GCF_002111305_1` (**"Panama and Peru"** — a Georgia case whose travel history
covered both) and `GCF_002113945_1` (**"Africa"** — Maryland ex Africa,
continent-level only).

Do **not** force either to one country, and do **not** leave them as pseudo-
countries: "Panama and Peru" is currently a country of n=1 that can never match
anything and inflates any country tally. Add an `origin_resolution` column —
`country` / `multi_country` / `region` / `unknown` — and exclude anything that
is not `country` from country-level statistics, including the 42-of-82
single-country phylogeography test.

Keep both in the tree and the panel, because they are **constrained test cases**,
not noise: if the Panama-and-Peru genome clusters with Panamanian genomes the
ambiguity resolves itself, and the Africa genome against the 5 Ghanaian ones is
the same experiment. The Colombia and Central American additions in T1/T3 give
the first one a realistic chance of resolving.

## Bottom line

If exactly one thing is added: **Ghana + Brazil + Mexico + Colombia + Nigeria
(~90 genomes)**, after the v3 run. It is small enough not to destabilise the
fit, it triples Americas representation, it creates the first testable African
signal, and Mexico rescues held data on top. Everything else is deferrable
without regret.
