# Ideas and open questions — running list

Started 2026-08-21. Things raised in discussion that should reach the analysis
plan or the manuscript. Each entry says what to do, not just what was said.

---

## 1. BioProject-as-control appears to be novel — verify before claiming it

**Status: promising, needs a proper literature check before any novelty claim.**

Searched 2026-08-21. Found **no example** of study-of-origin used as a measured
companion variable in a phylogeographic association test.

- [Salmonella Enteritidis source attribution](https://elifesciences.org/articles/84167)
  (eLife) — the closest prior art to our applied goal. Acknowledges sampling bias
  qualitatively ("the countries to which UK residents commonly travel") but its
  only structural control is deduplication: one random isolate per clone per
  country. No study covariate.
- [Biased sampling confounds ML prediction of AMR](https://journals.plos.org/plosbiology/article?id=10.1371%2Fjournal.pbio.3003539)
  (PLOS Biology) — 24,000 genomes, five pathogens, entirely about sampling bias,
  and **does not mention BioProject, study origin or laboratory batch at all**.

The recognised confounder in this literature is *phylogenetic population
structure*, not *who did the sequencing*. That is the gap our BioProject control
fills.

**To do:** systematic search before print. Write it as "we are not aware of",
never "first".

## 2. Cite PLOS Biology for the leave-group-out design

The same paper independently reaches two of our conclusions and gives us a
citation instead of a from-scratch derivation:

- models confounded with population structure fail to generalise;
- **"increasing the training sample size fails to rescue performance"** — more
  data does not fix it;
- recommended remedy is **"phylogeny-aware cross-validation testing on held-out
  clades"**, which is essentially our leave-group-out regime.

**To do:** cite in the attribution methods section as prior support for the
holdout design, and in the limitations for the "more sequencing won't fix this"
point.

---

## 3. Clade nomenclature — number them, do not put geography in the name

**Decision: propose numbered clades with region as an annotation.**

A geographic clade name is a claim that is hard to retract. Our own data already
breaks it: **ST92 is the documented "Western Hemisphere" type yet spans four v4c
units and seven countries.** Name something "Americas-1" and the first Thai
isolate to land in it makes the label wrong.

Precedent, all pointing the same way: WHO abandoned country names for SARS-CoV-2
variants; GPSC for pneumococcus is numbered; the *M. tuberculosis* "Beijing"
lineage is now global.

**Proposed form:**

```
BpC-14 — predominantly Latin America & Caribbean (82% of n=45, BioProject control passes)
```

Number is the identifier; region, its share, and the **control status** travel
with it as annotation. Units that are `confounded` or `vacuous control` get no
region annotation at all — only composition.

## 4. Fast placement for region prediction — two objections and a cheaper route

The goal (place a new isolate in seconds, return a region) is right. Three
things to settle first.

**UShER assumes inherited mutations.** It places by parsimony on a
mutation-annotated tree — fine for SARS-CoV-2 and TB, but here ~90% of pairwise
differences are imported DNA, so raw-SNP placement would place queries largely by
*recombination*. **The MAT must be built on the recombination-masked alignment**
so placement uses clonal-frame sites only. Non-optional.

**UShER needs one tree, which we do not have.** Per-unit trees are not mergeable
in interpretable units, so a global index implicitly requires a collection-wide
masked alignment and tree first.

**Cheaper route that avoids both, and matches the two-scale architecture:**

1. `poppunk_assign` — place the query into a strain/unit. Seconds, already in our
   stack, no new tooling.
2. Fine placement **within** that unit — masked SNP distance, or a per-unit
   UShER index if that proves insufficient.

**To do:** benchmark the two-stage version before building a global UShER index.
Validate whatever is built **leave-group-out on the 26 known-exposure genomes**,
same regime as the current attribution scoring — propose method and validation
together.

---

## 5. Accessory genome for attribution — the most promising untested idea

The Salmonella study reached country-level macro **F1 0.661** where our
core-genome approach reaches **zero**. The difference is not only organism: they
trained on **unitig presence–absence** — accessory/pangenome content, not core
SNPs.

Accessory gene pools are locally structured (local phage, plasmids, ICEs), so
they may carry geographic signal the core genome does not — **precisely because
they are not inherited clonally.** Everything that makes recombination a problem
for core-genome attribution may make accessory content informative.

Their scale gradient also matches ours qualitatively: continental 0.954,
sub-regional 0.718, country 0.661.

**We can test this almost for free — PopPUNK already computes accessory
distances.** Score accessory-distance attribution against core-genome attribution
under the identical leave-group-out regime.

**If accessory content attributes where core does not, that is a substantially
stronger paper**, and it reframes the negative core-genome result as one half of
a contrast rather than a dead end.

**To do:** run it. This is the highest-value open experiment on the list.

---

## 6. From the Gulvik DLST paper and two newer CDC studies (added 2026-08-21)

Full detail in `LITERATURE_POSITIONING_2026-08-21.md` §6a.

- **Extend the resolution ladder to 2 loci.** The PBP dual-locus scheme
  ([10.1371/journal.pntd.0009882](https://doi.org/10.1371/journal.pntd.0009882))
  would give **2 → 7 → 4,089 → whole genome**. Cheap; strengthens the
  resolution-invariance result.
- **Cite their UK/K96243 example** — four "UK" strains that are lab cultures of a
  Thai strain. Independent published documentation of our own metadata failure
  mode.
- **Cite the Georgia 2025 paper**
  ([10.3201/eid3109.250804](https://doi.org/10.3201/eid3109.250804)) as the
  *published applied use case* for the Mississippi cluster rule: cases with
  unknown exposure source, shared exposure inferred from relatedness.
- **Pre-empt the "CDC already attributes to country" objection.** The
  aromatherapy MAG paper
  ([10.1128/spectrum.02926-25](https://doi.org/10.1128/spectrum.02926-25))
  attributes a strain to India. That is single-strain attribution with
  corroborating supply-chain evidence — a different and easier task than blind
  systematic prediction. **State our claim narrowly.**
- **One sentence on why we avoided selected loci.** PBP genes are β-lactam
  targets, so geographic signal there may track antibiotic-use patterns and
  selection-driven homoplasy rather than descent. Design rationale, not
  criticism.

## Caveat carried from the Salmonella paper

Their Polish egg outbreak was "correctly" attributed to Southern Europe because
the food was imported — the ground truth itself was ambiguous. Our travel-
attributed genomes have the same exposure: `acquired_from` is where the patient
travelled, not necessarily where the organism came from. Worth stating in
limitations.
