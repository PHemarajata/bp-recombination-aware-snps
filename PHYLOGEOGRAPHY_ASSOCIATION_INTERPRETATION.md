# The phylogeny–geography association test: what it computes, and what it licenses you to say

Written 2026-08-19 from the RTX 4070 workstation. Companion to
`METHODS_DRAFT_2026-08-19.md` §2.12.9 and
`HANDOFF_PHYLOGEOGRAPHY_2026-08-19.md` §3.

This document does two things. §1–§4 explain the calculation and how to read its
output. §5–§7 report a **new analysis run for this document**: the same test
repeated at three geographic scales — sub-national, national, continental — to
establish *which* geographic unit the signal actually attaches to, rather than
assuming that a significant "country" result means the structure is national.

All results below are from the **A100 88-unit v4c partition**, 1,000
permutations, seed 20260815.

> **⚠ SUPERSEDED FOR THE REPORTED NUMBERS (banner added 2026-08-23).** Two things
> changed after this document was written.
>
> 1. **The A100 run is no longer the production run.** It is now the
>    cross-hardware **control**; the reported run is the 22-core workstation,
>    **85 units / 2,340 genomes**. Wherever this document says "production", read
>    "control".
> 2. **The association test was re-run on the frozen basis** at all three scales.
>    Quote `PHYLOGEO_FROZEN_{subnational,national,regional}_2026-08-23.tsv`, not
>    the figures below. **One claim did not survive**: sub-national is **1 of 81**
>    units, not the 0 of 88 reported here. National is 6 of 48 and regional 1 of
>    17.
>
> §1–§4 — what the test computes and how to read it — are unaffected and remain
> the reference for that. §5–§7 are superseded in their numbers.

---

## 1. What the test is for

A phylogenetic tree of a bacterial lineage carries no geography of its own. The
question is whether the geographic labels we hang on the tips are arranged
non-randomly with respect to tree structure — whether isolates from the same
place sit together.

That is a narrow question, and deliberately so. It is **not** a phylogeographic
reconstruction. It estimates no migration rates, infers no ancestral locations,
and says nothing about direction or timing of spread. `GAP4` establishes at
length why the fuller model-based machinery (DTA, the structured coalescent) is
not defensible on a collection sampled like this one; this test is the
design-based alternative that survives that critique.

---

## 2. The calculation, step by step

### 2.1 The statistic: Fitch small parsimony

For one unit's recombination-corrected tree, take the geographic label of every
tip and compute the **minimum number of label changes** that could explain the
observed tip labels on that fixed topology. This is Fitch's small-parsimony
score, computed in one post-order pass:

- At a tip, the state set is `{label}`, or "unknown" if there is no label.
- At an internal node, intersect the children's state sets. If the intersection
  is non-empty, that is the node's state set and no change is counted.
- If the intersection is empty, take the union instead and **count one change**.

The total count is the score. A low score means few changes were needed — tips
sharing a label sit together. A high score means labels are scattered across the
tree.

**Missing labels are fully ambiguous.** A tip with no label returns no state set
and is skipped in the intersection, so it can never force a change. Absent
metadata therefore *weakens* the signal rather than inventing one. This is why
the placeholder-string bug mattered: 274 genomes whose `bioproject` was the
literal string `unknown` were being treated as a genuine shared study rather than
as missing (fixed 2026-08-19; it changed the BioProject state count in 55 of 86
units).

### 2.2 The null: permute labels on the same tree

A raw parsimony score means nothing on its own — it depends on how many tips
there are, how many distinct labels, and how skewed their frequencies are. So the
score is compared against a null built by **shuffling the observed labels across
the tips of the same tree**, 1,000 times, recomputing the score each time.

This choice is the crux of the method. Shuffling only the *assignment* of labels
holds two things fixed:

- **the topology**, so tree shape is not part of what is being tested; and
- **the exact multiset of labels**, so a unit that is 90% Thai is compared
  against other 90%-Thai arrangements, never against an even mix.

That second property is what makes the test usable on a collection this skewed.
Any parametric null would have to assume a distribution over countries, and there
is no defensible one here. The permutation null sidesteps the question entirely.
This is the Slatkin–Maddison style test.

### 2.3 The p-value, and its floor

```
p = (number of permutations scoring <= observed + 1) / (1000 + 1)
```

One-sided: it asks how often chance does *as well as or better than* what we
observed. The `+1` in numerator and denominator is the standard correction that
stops a p-value of exactly zero.

**Consequence worth internalising: the smallest attainable p is 1/1001 =
0.0010.** A great many units report exactly `0.0010`. That does not mean
"p = 0.001"; it means **no permutation out of 1,000 matched the observed
arrangement**, and the true p is somewhere at or below 0.001. It is a floor, not
an estimate. Distinguishing p = 0.0009 from p = 0.000001 would need more
permutations, and nothing here depends on that distinction.

### 2.4 Units where the test cannot run

If every genome in a unit carries the same label, the parsimony score is 0 and no
permutation can do better, so p is trivially 1 and carries no information. These
are reported as `uninformative: <2 distinct values` with an **empty p-value** and
are excluded from every count of significant units. They must never be tallied as
"clustered".

> Note: `METHODS_DRAFT` previously stated that such units were "tested instead
> against the probability of drawing n genomes of one country at random from the
> collection's own country distribution". No such test was ever implemented. The
> Methods text was corrected on 2026-08-19 to describe actual behaviour. If that
> draw-probability test is wanted, it still needs writing.

### 2.5 The BioProject companion test — the part that does the real work

Every unit is tested a second time, with **BioProject** substituted for the
geographic label, on the identical tree with identical machinery.

The reasoning: a BioProject is typically one study, one laboratory, often one
outbreak investigation or one hospital. Isolates that were sequenced together are
frequently related for reasons that have nothing to do with geography — a single
outbreak, a single collection trip, a single clinical series. In this panel
"country" and "BioProject" are substantially the same variable wearing different
labels.

So the decisive comparison is not "is country significant?" but **"is country
significant in a way BioProject is not?"** A geographic signal no stronger than
the study-of-origin signal is not evidence of phylogeography; it is evidence that
related isolates get sequenced together.

---

## 3. Reading a single unit's result

Four outcomes, in decreasing strength:

| verdict | condition | what it licenses |
|---|---|---|
| **passes** | geography significant after FDR; BioProject *not* significant; BioProject control non-vacuous | geographic clustering not explained by study of origin |
| **confounded** | both geography and BioProject significant | nothing — the two explanations are indistinguishable here |
| **vacuous control** | geography significant, BioProject "not significant" but barely measured | nothing — the control did not run, it merely failed to fire |
| **untestable** | fewer than 2 distinct labels | nothing either way |

### The vacuous-control trap

This is the easiest way to fool yourself with this output, and it is not visible
from the p-value. A unit can report `p_country = 0.0010` and
`p_bioproject = 1.0000` and look like the strongest possible result, when in
truth only 7 of its 39 genomes have a BioProject recorded at all. The control did
not clear geography of confounding; it simply had no data with which to
implicate it.

**Always read `n_known` and `n_distinct` on the BioProject row before believing a
pass.** The rule used throughout this document: a BioProject control counts only
if it covers **≥70% of the unit's tips and has ≥3 distinct values**. On the Track
A control run, 4 of 12 apparent passes failed that bar.

### Multiple testing

Roughly 49 units are testable at country scale. At α = 0.05 that yields about 2.5
false positives by chance alone. All "passes" counts in this document apply
**Benjamini–Hochberg FDR control at 5%** across the testable units at that scale,
in addition to the BioProject requirement.

---

## 4. What a positive result does and does not mean

A "passes" verdict means: **tips sharing this geographic label sit closer
together on this tree than a random reassignment of the same labels would put
them, and that is not equally true of the labels recording which study sequenced
them.**

It does **not** mean, and cannot be stretched to mean:

- that the lineage *originated* in the dominant country — the test is
  directionless and the tree is undated;
- that transmission occurred between any two places;
- anything about migration rate, timing, or ancestral state;
- anything about countries absent from the panel — and 29 countries with over
  100 predicted annual cases have zero genomes;
- that the clustering is caused by transmission rather than by sampling. It
  narrows the alternatives by excluding study-of-origin; it does not exhaust
  them. Sampling one hospital, one outbreak, or one year within a country
  produces clustered labels through no epidemiological mechanism at all.

---

## 5. Which geographic unit does the signal attach to?

Everything above tests whichever label you supply. Running it with `country`
answers a question about countries — it cannot tell you whether the real
structure is finer (a province, a district) or coarser (a region, a continent),
because those labels were never presented to it.

So the test was re-run at three scales on the same 88 trees, same seed, same
permutation count. Only the label column changed.

- **Sub-national** — `country :: subregion` (e.g. `USA :: Mississippi`,
  `Thailand :: Nakhon Phanom`). 79.6% of analysed tips populated, 96 distinct.
- **National** — country, normalised (see §6). 99.8% populated, 41 distinct.
- **Regional** — World Bank regions, chosen for consistency with `GAP4`'s burden
  arithmetic. 99.8% populated, 7 distinct.

### 5.1 How much can even be asked at each scale

| scale | units testable (of 88) | single-label, untestable | median labels per unit |
|---|---|---|---|
| sub-national | **83** | 5 | 6 |
| national | **49** | 39 | 2 |
| regional | **16** | **72** | 1 |

**At continental scale the panel is close to mute, and this is a sampling fact,
not a biological one.** 93.4% of analysed genomes are East Asia & Pacific, so 72
of 88 units contain exactly one region and no test can run on them. The remaining
composition is Latin America & Caribbean 3.2%, North America 1.6%, South Asia
0.6%, Europe & Central Asia 0.5%, Sub-Saharan Africa 0.4%, Middle East & North
Africa 0.04%.

### 5.2 What survives at each scale

Applying FDR at 5% **and** requiring a non-vacuous BioProject control:

| scale | raw p ≤ 0.05 | survives FDR | **passes everything** |
|---|---|---|---|
| sub-national | 17 | 11 | **0** |
| national | 26 | 24 | **6** |
| regional | 4 | 3 | **1** |

The six that pass at national scale: `strain_11_L1_5`, `strain_14_L1_4`,
`strain_1_L1_28`, `strain_1_L1_5`, `strain_2_L1_2`, `strain_5_L1_3`. All six are
Southeast Asian.

### 5.3 Sub-national geography is indistinguishable from study of origin

Zero of 88 units pass at sub-national scale, and the reason is specific rather
than a matter of power — 83 units were testable and 17 produced raw hits. Of
those 17:

- 6 did not survive FDR;
- **11 were confounded with BioProject**;
- 0 survived.

Every single sub-national signal strong enough to clear multiple testing was
matched by the study label. That is exactly what one should expect: a label like
`Thailand :: Nakhon Phanom` or `Puerto Rico :: Arecibo` is very nearly the name
of a collection effort. At this resolution, place and study are the same variable
in this panel.

### 5.4 The national signal is genuinely national, not inherited from continent

If country-level clustering were merely a shadow of continental structure, the
same units should cluster at regional scale. They do not. For the six units that
pass at country scale:

| unit | regional-scale result | sub-national result |
|---|---|---|
| `strain_11_L1_5` | p = 1.0000 — regions **do not** cluster | p = 0.7453 |
| `strain_2_L1_2` | p = 1.0000 — regions **do not** cluster | p = 0.0769 |
| `strain_14_L1_4` | untestable (single region) | p = 0.3616 |
| `strain_1_L1_28` | untestable (single region) | p = 0.0400 |
| `strain_5_L1_3` | untestable (single region) | p = 0.9510 |
| `strain_1_L1_5` | p = 0.0020 — also passes at region | p = 1.0000 |

Two units show countries clustering while regions explicitly do not, and three
more sit entirely inside one region, so their country signal is by construction
*within*-region structure. Only `strain_1_L1_5` (Singapore 10, France 5,
Malaysia 2, Bangladesh 1) clusters at both, which is unsurprising for a unit
spanning three continents.

**The signal in this panel lives at country scale.** Finer than that it is
inseparable from study design; coarser than that it mostly cannot be asked, and
where it can, it largely disappears.

---

## 6. What the geographic labels actually are

Interpretation depends on what `country` means, and it is not simply "where the
sample was collected".

**It is an acquisition estimate, deliberately.** `origin_basis` records 2,322
genomes `as_isolated` and **20 `travel_reattributed`** — assigned to an inferred
country of exposure rather than the reporting country. Sample identifiers show
the reasoning (`GCF_002111125_1_USA_New_York_ex_Aruba` carries `country = Aruba`).
This is the right variable for origin-of-exposure attribution, but it means the
column is a curated inference for a minority of rows, not a raw observation.
`origin_resolution` flags 4 genomes `unknown` and 1 `multi_country`.

**Three labelling defects were found while preparing this document:**

1. **US Caribbean territories are split across two conventions.** Five genomes
   are `country = USA, subregion = Puerto Rico`; five others are
   `country = Puerto Rico, subregion = Arecibo`. Same territory, two states in
   the test. The same applies to the Virgin Islands (5 as `USA`, 1 as
   `Virgin Islands` — and that row's `iso_a3` is the unresolved literal string
   `VGB or VIR`, conflating the British and US territories).
2. **`Viet Nam` (43) and `Vietnam` (1)** are separate strings sharing ISO `VNM`.
3. **`Panama and Peru`** is a single compound value, flagged
   `origin_resolution = multi_country`.

Also note `iso_a3` is *not* a cleaner substitute: it records reporting country
where `country` records acquisition, so `Aruba`, `Guatemala` and `Mexico` rows
all carry `iso_a3 = USA`.

**These defects do not change any conclusion here.** Re-running the national
scale with all three normalised (territories harmonised, spelling merged,
compound value set to missing) altered the result of exactly **2 of 88 units** —
`strain_4_L1_3` (parsimony 6 → 5) and `strain_4_L1_4` (9 → 11) — and neither
changed its p-value or its verdict. They should still be fixed before the numbers
are published.

---

## 7. What can and cannot be said from these data

### Supported

- In 6 of 88 units, isolates from the same **country** are phylogenetically
  clustered to a degree not explained by which study sequenced them. All six are
  Southeast Asian.
- **Country is the resolution at which this panel carries geographic
  information.** Sub-national labels add nothing once study of origin is
  controlled; regional labels are unaskable for 82% of units.
- 39 of 88 units are single-country. That is a descriptive fact about panel
  composition and may be useful as an attribution prior, but it is not a test
  result and carries no p-value.
- The result is robust to partition version: the Track A 86-unit control run
  agrees on 6 of 7 survivors, the single discrepancy (`strain_1_L1_11`) being a
  genuine membership difference (n = 18 vs 24), not permutation noise.

### Not supported

- **No sub-national attribution.** Nothing survives at that scale. In particular
  the Mississippi unit `strain_4_L1_1` (21 USA/Mississippi + 1 Colombia) returns
  p = 1.0000 at *every* scale; with two labels in a 21-to-1 split, no permutation
  test can say anything. Its uniformity is a description of the unit, not a
  finding about geography.
- **No Americas attribution.** Every Americas-bearing unit fails, each
  differently: `strain_4_L1_4` (33 genomes, ten countries) is **confounded** at
  country p = 0.0010 *and* BioProject p = 0.0010 with 31/33 coverage — a
  well-powered negative, not a data-poor one; `strain_4_L1_3` (Brazil 31 of 39)
  has a **vacuous control** at 7/39 BioProject coverage; `strain_4_L1_2` and
  `strain_22_L1_1` show no country signal.
- **No continental claims.** Not "Australia is ancestral", not "Southeast Asia is
  the source". 72 of 88 units cannot be tested at that scale at all.
- **No direction, no dates, no rates.** The trees are substitution-scaled and
  undated, and the test is symmetric in the labels.
- **Nothing about the 29 high-burden countries with zero genomes.**

### The honest one-sentence version

> On the v4c panel, phylogenetic clustering by country that cannot be attributed
> to study of origin is demonstrable in 6 of 88 units, all Southeast Asian;
> country is the only geographic resolution at which this collection carries
> such information, and no unit relevant to Americas origin-of-exposure
> attribution survives the study-of-origin control.

---

## 8. Reproducing this

```bash
# per-unit trees from the A100 production run (176 files, 2.2 MB)
rclone copy peerah-gdrive:wfsnps-v4c-results/snp/Clusters A100_v4c_Clusters \
  --include "*/Gubbins/*.node_labelled.final_tree.tre" --transfers 8

# national scale — metadata satisfies the --assignments interface directly
python3 phylogeography_association_bp.py \
  --assignments L1v4c_MERGED_METADATA.tsv --trees A100_v4c_Clusters \
  --perms 1000 --seed 20260815 --out PHYLOGEOGRAPHY_ASSOCIATION_v4c_A100.tsv

# other scales: same command with assign_subnational.tsv / assign_country_norm.tsv
# / assign_region.tsv, which carry the scale label in the `country` column
```

Outputs: `SCALE_subnational.tsv`, `SCALE_country_norm.tsv`, `SCALE_region.tsv`,
and `SCALE_country_raw.tsv` (byte-identical to
`PHYLOGEOGRAPHY_ASSOCIATION_v4c_A100.tsv`, which confirms reproducibility).
Columns: `unit, n_tips, variable, n_known, n_distinct, parsimony_score,
top_share, p_value, verdict`, two rows per unit.
