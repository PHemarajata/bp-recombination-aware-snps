# Vietnam / Georgia — resolved, and it is a result

**2026-08-23.** Open item 5 (`LEAVE_OUTBREAK_OUT_2026-08-23.md` §6). The question
was whether two USA:GA cases sharing a strain with two Vietnam-exposure cases are
*unrecorded Vietnam imports* (mislabelled references) or a *genuine trans-Pacific
lineage*. It is the second, and the epidemiology is published.

> **The Georgia cases are autochthonous, and the lineage genuinely spans Vietnam
> and the southeastern USA. The boundary between "acquired in Georgia" and
> "acquired in Vietnam" is ONE cgMLST locus in 4,221.** That is this paper's
> central claim as a single worked example, with independent published
> epidemiology on both sides of it.

## 1. The premise was wrong in two ways, both in our favour

- **It is five Georgia cases, not two** — 1983, 1989, and **three in 2024**.
- **A sixth US genome is Ohio, not Georgia** (1969), and it is a distance outlier.

Authoritative ENA metadata, requested-vs-returned verified for all eight
(`PRJNA908850`):

| run | BioSample | country | year |
|---|---|---|---|
| `SRR31608437` | SAMN45170502 | **USA: GA** | 1983 |
| `SRR31608434` | SAMN45170505 | **USA: GA** | 1989 |
| `SRR31608438` | SAMN45170501 | **USA: GA** | 2024 |
| `SRR31608439` | SAMN45170500 | **USA: GA** | 2024 |
| `SRR31608440` | SAMN45170499 | **USA: GA** | 2024 |
| `SRR31608436` | SAMN45170503 | USA: OH | 1969 |
| `SRR31608433` | SAMN45170506 | USA: CA **ex Vietnam** | 2017 |
| `SRR31608435` | SAMN45170504 | USA: CA **ex Vietnam** | 2012 |

Plus, in the same unit `strain_22_L1_1` (n=11) and from **independent**
BioProjects, three genuine **in-country Vietnamese** isolates:
`GCF_041726195_1` and `GCF_041726215_1` (2023, `PRJNA1143172`) and
`GCF_009768635_1` (2015, `PRJNA595043`).

## 2. The epidemiology is published, and it says no travel

According to PubMed:

> **Brennan S, Thompson JM, Gulvik CA, Paisie TK, Elrod MG, Gee JE, Schrodt CA,
> DeBord KM, Richardson BT, Drenzek C, Bower WA, Hoffmaster AR, Weiner ZP,
> Cossaboom CM, Gabel J. "Related Melioidosis Cases with Unknown Exposure Source,
> Georgia, USA, 1983–2024." *Emerg Infect Dis* 2025;31(9):1802–1806.**
> PMID **40835221**, [doi:10.3201/eid3109.250804](https://doi.org/10.3201/eid3109.250804)

The abstract reports 4 presumptive **autochthonous** cases in Georgia over
1983–2024; epidemiologic investigation found **no recent international travel**
before illness; all cases were **geographically linked**; and **3 patients became
ill after a severe weather event** — which matches our three 2024 genomes.

**So the "unrecorded Vietnam import" hypothesis is refuted by a CDC/state
epidemiologic investigation, not by our inference.** Our
`origin_basis = as_isolated`, `exposure_country = USA` on these five is
independently confirmed correct.

⚠ **One discrepancy to resolve before citing:** the paper reports **4 cases**;
the BioProject carries **5 Georgia genomes** (1983, 1989, 2024 × 3). Either one
case contributed two isolates, or one genome is a Georgia case outside the
published series. Confirm against the paper's own accession list before writing a
number.

## 3. The distance structure — and a one-locus boundary

cgMLST allelic distance (fraction of 4,221 loci differing, × 1000):

| comparison | min | median |
|---|---|---|
| **Georgia cluster, internal** (n=5, 1983–2024) | 3.72 | 7.57 — **max 8.67** |
| Georgia → Vietnam **travel** cases (2012, 2017) | **8.91** | 13.15 |
| Georgia → Vietnam **in-country** (2023 × 2) | 12.34 | 14.05 |
| Georgia → Ohio 1969 | 13.63 | 14.63 |
| Georgia → Vietnam 2015 | 57.25 | 57.97 |

**The nearest non-Georgia genome in the entire 3,033-genome collection is
`SRR31608433` — a Vietnam-exposure case — at 8.91, against a Georgia internal
maximum of 8.67.**

> **Separation margin = 0.25 × 10⁻³ = 1.0 locus of 4,221.**

A published, epidemiologically-investigated US autochthonous cluster is separated
from a documented Vietnam-acquired case by **one locus** more than the cluster's
own internal spread. No distance threshold can put those on opposite sides
reliably.

### It is not a BioProject artifact — the control is internal

The obvious objection is that the Georgia genomes cluster because they share a
BioProject, a lab and an assembly pipeline. **`PRJNA908850` contains both the
Georgia cases and both Vietnam-exposure cases**, and within that single project
the distances to the Georgia cluster span **8.91 to 16.47**: `SRR31608433` sits
at its edge while `SRR31608435` sits far outside it. Same lab, same pipeline,
four-fold difference in distance. The structure is biological.

### Two members do not belong to the story

- **Ohio 1969** sits 13.63–16.86 from the Georgia cluster — outside it. 1969 is
  peak Vietnam-War era and this is a plausible independent importation. It should
  not be described as part of the Georgia focus.
- **`GCF_009768635_1` (Vietnam 2015)** sits at ~58 from *everything*, including
  the other Vietnamese genomes — a **divergent member** of the kind that inflates
  unit diversity ([[rm-spread-is-divergent-members]]). It is barely in this unit.

## 4. What this is worth to the manuscript

1. **A second US autochthonous focus, alongside Mississippi.** Georgia
   (Brennan 2025, 1983–2024) and the Gulf Coast (Petras 2023 *NEJM*) are now two
   published, independently investigated US foci. R7 currently describes only
   Mississippi.
2. **The strongest single illustration of the country-attribution failure.**
   Elsewhere the paper argues country fails because source countries lack
   reference genomes. Here the opposite condition holds — *both* countries are
   represented, by independent studies, with published epidemiology — **and
   attribution still fails, by one locus.** That is a much harder case than
   absence of references, and it belongs in R2 or the Discussion.
3. **It vindicates the leave-outbreak-out design decision.** `OUTBREAK_GROUPS.tsv`
   is an explicit register precisely because an automatic same-BioProject or
   near-clone rule would have held the Georgia cases out as "same source" and
   manufactured a Viet Nam answer of 2/2. The published epidemiology now confirms
   they are **independent cases of a shared lineage, not co-deposits** — so
   holding them out would have hidden real references and faked a result. The
   counterexample that drove the design is now externally validated.
4. **A dating opportunity we are not taking.** A 41-year Georgia series (1983,
   1989, 2024 × 3) is exactly the temporal structure a molecular-clock analysis
   wants. **Do not attempt it here** — the grafted backbone mixes branch-length
   units and must not be dated ([[snp-pipeline-architecture-and-known-flaws]]),
   and r/m ≈ 7.7 means most of this distance is imported DNA, not inherited
   mutation. Name it as further work.

## 5. What is NOT claimed

- **No direction of transmission.** These data cannot say whether the lineage
  moved Vietnam → USA, USA → Vietnam, or descends from a shared ancestor in a
  third place. Sampling is far too sparse and the panel is 59.5% Thailand.
- **No date for the Georgia introduction.** See §4.4.
- **Not "the same strain" in the outbreak sense.** 8.67 × 10⁻³ across the Georgia
  cluster is ~37 loci — far above the Gulf Coast cluster's outbreak-resolution
  signature (median 5 filtered SNPs internally). This is a *lineage*, not a
  point-source event, and the published series says "shared exposure" over
  41 years, which is a different claim again.
- **The 4-vs-5 genome discrepancy is unresolved** (§2).

## 6. Actions

- Add Georgia to R7 as a second autochthonous focus; cite Brennan 2025
  (PMID 40835221) — already in the outline's §6.2 comparison table but only as
  "the published applied precedent for our ≤20-SNP rule".
- Use the one-locus margin in R2/Discussion as the sharpest instance of the
  country-attribution ceiling.
- Reconcile the 4-cases-vs-5-genomes count against the paper.
- Consider registering the Georgia cases as an outbreak group **for robustness
  only** — with the explicit note that they must NOT be held out when scoring
  Viet Nam, since they are independent cases and their removal fakes a result.
- Flag `GCF_009768635_1` as a divergent member of `strain_22_L1_1`.
