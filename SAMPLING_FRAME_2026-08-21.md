# The sampling frame — how the panel was assembled, and how it compares to what exists

Written 2026-08-21 to answer the question a reviewer will certainly ask:
**"how did you arrive at these 2,976 sequences?"**

Census taken 2026-08-21 from the ENA Portal API, *B. pseudomallei* (taxid
28450). Reproducible — the query is at the bottom.

---

## 1. The universe

| | count |
|---|---|
| ENA read runs | **9,623** |
| unique BioSamples | **8,500** |
| BioSamples with a recorded country | **6,695** |
| ENA assemblies | 3,546 |
| **our panel** | **2,976** (2,961 with a country) |
| **our coverage of country-labelled BioSamples** | **44%** |

So we hold roughly two fifths of the country-labelled public collection. That is
a real number and it should be stated, not hidden.

---

## 2. The honest weakness: our panel is not proportional to what exists

| country | ENA share | our share | verdict |
|---|---|---|---|
| Thailand | 51.6% | **59.2%** | over-represented |
| Australia | **23.8%** | **9.6%** | **under by 2.5×** |
| Cambodia | 8.0% | **1.6%** | **under by 5×** |
| China | 2.8% | **10.0%** | over by 3.5× |
| USA | 1.7% | 1.8% | proportional |
| India | 1.4% | 1.9% | proportional |

**Australia is the serious gap.** It is one of the two major endemic regions,
it sits basal in our own global tree, and we hold **283 of 1,594** available
genomes — 18%.

| country | in ENA | ours | we have | available to add |
|---|---|---|---|---|
| Thailand | 3,462 | 1,753 | 51% | 1,709 |
| **Australia** | **1,594** | **283** | **18%** | **1,311** |
| **Cambodia** | 534 | 47 | **9%** | 487 |
| **Puerto Rico** | 61 | 5 | **8%** | 56 |
| Taiwan | 38 | 3 | 8% | 35 |
| India | 96 | 56 | 58% | 40 |
| USA | 117 | 53 | 45% | 64 |
| Viet Nam | 83 | 60 | 72% | 23 |
| Mali | 31 | 0 | 0% | 31 |
| New Caledonia | 18 | 0 | 0% | 18 |

---

## 3. The finding that reframes the whole limitation

**For most of the countries our validation genomes came from, there is NO public
data at all — not for us, not for anyone.**

| exposure country | genomes in ENA | genomes we hold |
|---|---|---|
| **Philippines** | **0** | **12** |
| **Mexico** | **0** | 8 |
| **Guatemala** | **0** | 2 |
| **Aruba** | **0** | 2 |
| **Nicaragua** | **0** | 1 |
| **El Salvador** | **0** | 1 |
| **Costa Rica** | **0** | 1 |
| **Trinidad and Tobago** | **0** | 1 |
| **Martinique** | **0** | 1 |
| Nigeria | 9 | 10 |

**Nine of our sixteen validation source countries have zero public reference
genomes.** We hold the only ones in existence, and they are the very genomes
being held out.

This transforms the limitation from an admission into a finding:

> Country-level attribution is not achievable for most melioidosis source
> countries **because the reference genomes do not exist**, in any public
> database, for anyone. It is not a shortcoming of this panel or this method.
> More sequencing of the *same* countries will not fix it; sequencing the
> *unrepresented* ones would.

**That is the answer to the reviewer.** It is stronger than a defence, because
it identifies a concrete gap in global surveillance and quantifies it.

---

## 4. Two different metadata standards, for two different jobs

The panel serves two purposes with different evidence requirements, and
conflating them is the error to avoid.

| use | what the country field must mean | standard |
|---|---|---|
| **reference population** | where the organism was found | **deposit country is appropriate** — that is where it lives |
| **validation ground truth** | where the patient acquired it | **exposure country required** — deposit is not evidence of origin |

A US clinical isolate with no travel field could be domestic or an unrecorded
import. Counting it as "USA origin" would inject the exact error we are trying
to measure. `classify_ena_origin_bp.py` enforces this with four tiers:

| tier | meaning | use |
|---|---|---|
| **A_exposure_stated** | ENA country reads "X **ex** Y" | ground truth |
| **B_external_evidence** | origin from published investigation, registered in `EXPOSURE_OVERRIDES.tsv` with a citation | ground truth |
| **C_deposit_only** | a country, but nothing distinguishes local acquisition from unrecorded travel | **panel only** |
| **D_unusable** | no country, or wrong species | exclude |

**D is not hypothetical.** The first pass on three CDC BioProjects caught **3
*B. thailandensis* runs** that a study-level query would have silently pulled in.

---

## 5. The stated inclusion rule, for the methods section

> Genomes were drawn from public repositories and retained where (i) they were
> *B. pseudomallei* by taxonomic assignment, (ii) they passed assembly QC
> (contamination, ANI, size, gene-count ratio), and (iii) they were not
> duplicates of a retained genome. Exclusions are enumerated with reasons in
> `PANEL_EXCLUSIONS.tsv` (n = 46). Origin metadata was classified into four
> tiers of evidential strength; only tiers A and B were used as attribution
> ground truth, tier C for reference population only.
>
> The panel represents 44% of country-labelled *B. pseudomallei* BioSamples in
> ENA as of 2026-08-21, and is **not proportional** to that collection:
> Thailand and China are over-represented and Australia and Cambodia
> under-represented relative to public availability. Neither the panel nor the
> public collection is proportional to melioidosis burden.

Stating the disproportion explicitly is much stronger than being caught on it.

---

## 6. Expansion priorities, given compute is available

**Do not add more Thailand.** We hold 1,753 and it is already 59% of the panel;
adding more worsens the imbalance that matters.

| priority | target | n | why |
|---|---|---|---|
| **1** | **Australia** | ~1,311 | Largest gap, major endemic region, basal in our tree, and we now hold **2 Australian exposure genomes** to test against |
| **2** | **Puerto Rico** | ~56 | We hold 8%. Directly relevant to the Americas/US question, and cheap |
| **3** | **Cambodia** | ~487 | Under by 5×; balances SE Asia |
| **4** | **India** | ~40 | We now hold **6 India exposure genomes** (1 stated + 5 aromatherapy) |
| **5** | **Viet Nam, Taiwan, Mali, New Caledonia** | ~107 | Fill zeros and near-zeros |

**~2,000 genomes.**

### The staging decision that controls cost and risk

**Adding genomes to the reference panel does not require re-running the SNP
pipeline — unless you want them in units.**

| phase | what it needs | what it costs | what it invalidates |
|---|---|---|---|
| **Phase 1: attribution only** | download → assemble → QC → cgMLST allele call → re-score | assembly is the only heavy step; cgMLST is incremental against the existing prepared schema | **nothing** |
| **Phase 2: full integration** | re-partition (PopPUNK + fastbaps) → re-run SNP pipeline → Gubbins → distances | the whole analysis again | **every unit, r/m, distance table and tree** |

**Recommend Phase 1 first.** It answers the scientific question — *does a
properly balanced reference panel change attribution?* — without invalidating
the 88-unit analysis, the r/m work, or the ClonalFrameML run. If attribution
improves materially with Australian and Puerto Rican references, Phase 2 becomes
justified. If it does not, we have the answer for the cost of assembly alone.

**Phase 2 is a genuine re-analysis**, not an increment. Every number in the
current write-ups would need regenerating. Worth doing deliberately, not by
drift.

---

## 7. Reproducing this census

```bash
curl -s "https://www.ebi.ac.uk/ena/portal/api/search?result=read_run\
&query=tax_eq(28450)\
&fields=run_accession,sample_accession,study_accession,country,collection_date\
&format=tsv&limit=0" -o ena_all_runs.tsv
```

Deduplicate to BioSample, split `country` on `:` to drop the sub-national part,
and count. Assemblies: same URL with `result=assembly`.
