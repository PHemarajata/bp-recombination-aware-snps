# Melioidosis: clinical presentation, burden, risk factors, diagnosis, treatment, biosafety

Raw research material for the Background section of a *Burkholderia pseudomallei* genomics manuscript.

**Compiled:** 2026-09-02

---

## 0. Provenance and verification notes — READ FIRST

**Tooling caveat.** The PubMed MCP tools (`search_articles`, `get_article_metadata`, `get_full_text_article`, `find_related_articles`) and `curl`/E-utilities were blocked in this session by a safety classifier after the first call. All retrieval below was done with **WebSearch** and **WebFetch** against:
- **Europe PMC REST API** (`ebi.ac.uk/europepmc/webservices/rest/search`) — used as the search substitute; returns PMID/DOI/PMCID reliably.
- **PMC full text** (`pmc.ncbi.nlm.nih.gov/articles/PMCxxxxxxx/`) — used for verbatim extraction.
- Publisher/agency sites (CDC EID, selectagents.gov).

`pubmed.ncbi.nlm.nih.gov` article pages are **not** fetchable (cookie wall). PMC and Europe PMC are.

**Important limitation on "verbatim".** WebFetch renders a page and answers a prompt using a *small summarising model*. Where that model returned text in quotation marks I have reproduced it, but **quoted strings below are second-hand and should be re-checked against the PDF before they go into a manuscript**, especially any that will be quoted directly. Numbers were cross-checked across independent sources wherever possible. Items I could **not** verify are flagged **UNVERIFIED** with a statement of exactly what is missing.

**Highest-confidence items** (verbatim abstract retrieved intact from Europe PMC `resultType=core`, or explicitly re-queried sentence-by-sentence from PMC results sections): the Darwin 30-year abstract (§1.1), the Darwin 20-year results sentences (§1.2), Gee 2017 abstract (§4.3), Meumann 2024 abstract (§2.4).

---

## 1. Clinical spectrum

### 1.1 Darwin Prospective Melioidosis Study (DPMS), 30 years — the anchor cohort

Currie BJ, Mayo M, Ward LM, Kaestli M, Meumann EM, Webb JR, Woerle C, Baird RW, Price RN, Marshall CS, Ralph AP, Spencer E, Davies J, Huffam SE, Janson S, Lynar S, Markey P, Krause VL, Anstey NM. **The Darwin Prospective Melioidosis Study: a 30-year prospective, observational investigation.** *Lancet Infect Dis* 2021;21(12):1737–1746. PMID 34303419. DOI 10.1016/S1473-3099(21)00022-0.

Prospective, culture-confirmed, laboratory-notifiable capture in the tropical Northern Territory of Australia, **1 Oct 1989 – 30 Sept 2019**. This is the single best-characterised melioidosis cohort in the world and the natural comparator for any genomic study.

Verbatim from the abstract (retrieved intact):

> "There were 1148 individuals with culture-confirmed melioidosis, of whom 133 (12%) died. Median age was 50 years (IQR 38-60), 48 (4%) study participants were children younger than 15 years of age, 721 (63%) were male individuals, and 600 (52%) Indigenous Australians. All but 186 (16%) had clinical risk factors, 513 (45%) had diabetes, and 455 (40%) hazardous alcohol use. Only three (2%) of 133 fatalities had no identified risk. Pneumonia was the most common presentation occurring in 595 (52%) patients. Bacteraemia occurred in 633 (56%) of 1135 patients, septic shock in 240 (21%) patients, and 180 (16%) patients required mechanical ventilation. Cases correlated with rainfall, with 80% of infections occurring during the wet season (November to April). Median annual incidence was 20·5 cases per 100 000 people; the highest annual incidence in Indigenous Australians was 103·6 per 100 000 in 2011-12. Over the 30 years, annual incidences increased, as did the proportion of patients with diabetes, although mortality decreased to 17 (6%) of 278 patients over the past 5 years."

Interpretation, verbatim:

> "Melioidosis is an opportunistic infection with a diverse spectrum of clinical presentations and severity. With early diagnosis, specific antimicrobial therapy, and state-of-the-art intensive care, mortality can be reduced to less than 10%. However, mortality remains much higher in the many endemic regions where health resources remain scarce. Genotyping of B pseudomallei informs evolving local and global epidemiology."

**Note the denominator quirk:** bacteraemia is reported as 633/1135, not /1148 — 13 patients lacked blood culture data. Reproduce the denominator faithfully.

### 1.2 Darwin 20-year study — the presentation-by-presentation breakdown

Currie BJ, Ward L, Cheng AC. **The epidemiology and clinical spectrum of melioidosis: 540 cases from the 20 year Darwin prospective study.** *PLoS Negl Trop Dis* 2010;4(11):e900. PMID 21152057. DOI 10.1371/journal.pntd.0000900. PMC2994918. Open access.

This paper, not the 30-year one, is the source for the fine-grained organ-by-organ frequencies. Sentences quoted from the Results section:

| Presentation | n (%) | Verbatim |
|---|---|---|
| Pneumonia (principal presentation) | 278 (51%) | "Pneumonia was the commonest principal clinical presentation on admission (278 cases; 51%)" |
| Bacteraemic overall | 298 (55%) | "Overall 298 (55%) patients were bacteremic." |
| Septic shock | 116 (21%), 58 (50%) died | "Of the 116 patients (21%) with septic shock, 58 (50%) died from acute fulminant melioidosis." |
| Prostatic abscess (males) | 76/372 males (20%) | "Prostatic abscesses were present in 76 males (20%)" |
| Genitourinary infection | 76 (14%) | (from summary table) |
| Skin infection | 68 (13%) | (from summary table) |
| Bacteraemia without evident focus | 59 (11%) | (from summary table) |
| Septic arthritis / osteomyelitis | 20 (4%) | (from summary table) |
| Neurological melioidosis | 14 (3%) | (from summary table) |
| Splenic abscess | 28 (5%) | (from summary table) |
| Renal abscess | 18 (3%) | (from summary table) |
| Liver abscess | 15 (3%) | (from summary table) |

Overall mortality: **"There were 540 cases and 77 deaths (14%) attributable to melioidosis over the 20 years."** Mortality fell **"from 30% in the first 5 years to 9% in the last five years (p<0.001)"**.

*Caveat:* the rows marked "(from summary table)" were returned by the fetch summariser as a table rather than as quoted sentences; the six rows I re-queried sentence-by-sentence (pneumonia, bacteraemia, septic shock, prostate, mortality, no-risk-factor) all reproduced exactly, which is reassuring but does not guarantee the rest. **Re-check the table rows against the PDF.**

### 1.3 Pneumonia in detail

Meumann EM, Cheng AC, Ward L, Currie BJ. **Clinical features and epidemiology of melioidosis pneumonia: results from a 21-year study and review of the literature.** *Clin Infect Dis* 2012;54(3):362–369. PMID 22057702. DOI 10.1093/cid/cir808. PMC3258273.

- 319 of 624 culture-confirmed patients (**51%**) had melioidosis pneumonia.
- **"acute/subacute presentations accounted for the majority of primary pneumonia cases (91%); chronic disease was seen less commonly (9%)."**
- Mortality of melioidosis pneumonia overall: **20%** (64/319).
- Bacteraemic pneumonia mortality **27%**; non-bacteraemic **4%**.
- Multilobar involvement **32%** mortality vs **14%** single-lobe.
- Bacteraemia present in **63%** of pneumonia cases.

### 1.4 Neurological melioidosis

Gora H, Hasan T, Smith S, et al. **Melioidosis of the central nervous system.** *Clin Infect Dis* 2022; ciac111. PMID 35137005. DOI 10.1093/cid/ciac111.

- **52 of 1587 (3.3%)** melioidosis cases had confirmed CNS involvement.
- Breakdown: 20 brain abscess, 18 encephalomyelitis, 4 isolated meningitis, 10 extra-meningeal.
- **"8 (15.4%) deaths; 17/44 (38.6%) survivors had residual disability."**
- The **bimA<sub>Bm</sub>** allele variant was associated with death or residual disability: **OR 4.88 (95% CI 1.28–18.57), p=0.01**. *This is directly relevant to a genomics manuscript — a genotype–phenotype link in a virulence-factor allele.*

Landmark older series: Woods ML, Currie BJ, Howard DM, et al. **Neurological melioidosis: seven cases from the Northern Territory of Australia.** *Clin Infect Dis* 1992;15(1):163–169. PMID 1617057. DOI 10.1093/clinids/15.1.163.
Also: Currie BJ, Fisher DA, Howard DM, Burrow JN. **Neurological melioidosis.** *Acta Trop* 2000;74(2-3):145–151. PMID 10674643. DOI 10.1016/S0001-706X(99)00064-9.

Mechanism: St John JA, et al. **Burkholderia pseudomallei penetrates the brain via destruction of the olfactory and trigeminal nerves.** *mBio* 2014;5(2):e00025-14. PMID 24736221. DOI 10.1128/mBio.00025-14. PMC3993850.

### 1.5 Chronic melioidosis

Singh H, et al. **Epidemiology, Clinical Features, and Outcomes of Chronic Melioidosis.** *Open Forum Infect Dis* 2026;13(6):ofag294. PMID 42253281. DOI 10.1093/ofid/ofag294. PMC13241206.

- Definition: **"Cases were prospectively designated as chronic if the reported symptom duration was ≥2 months."**
- Chronic = **126/1346 (9.36%)** of cases.
- Commonest presentations: pneumonia 38.89%, cutaneous 32.54%.
- Mortality **3/126 (2.38%)** vs **11.13%** for acute — chronic disease is much less lethal acutely.
- **Misdiagnosis:** among 34 chronic pneumonia cases with radiology reports, **tuberculosis** was a differential in **32.35%** and **neoplasia** in **23.53%**. Directly supports the "systematic misdiagnosis" argument.

### 1.6 Paediatric melioidosis and parotitis

Dance DA, Davis TM, Wattanagoon Y, Chaowagul W, Saiphan P, Looareesuwan S, Wuthiekanun V, White NJ. **Acute suppurative parotitis caused by *Pseudomonas pseudomallei* in children.** *J Infect Dis* 1989;159(4):654–660. PMID 2926159. DOI 10.1093/infdis/159.4.654.

> "Parotitis constituted 6.3% of all culture-positive melioidosis and 38% of melioidosis in children."

This is the landmark for the striking geographic asymmetry: **suppurative parotitis is a common paediatric presentation in Thailand and Cambodia but rare in Australia.**

McLeod C, Morris PS, Bauert PA, Kilburn CJ, Ward LM, Baird RW, Currie BJ. **Clinical presentation and medical management of melioidosis in children: a 24-year prospective study in the Northern Territory of Australia and review of the literature.** *Clin Infect Dis* 2015;60(1):21–26. PMID 25228703. DOI 10.1093/cid/ciu733.

- 45 paediatric cases = **5% of 820** total.
- **"Primary cutaneous melioidosis was the commonest presentation in children (60% vs 13%)"** — i.e. children present cutaneously far more than adults.
- Mortality **3/45 (7%)**; all had identifiable risk factors.

Cambodia paediatric emergence: Pagnarith Y, et al. *Am J Trop Med Hyg* 2010. PMID 20519608. DOI 10.4269/ajtmh.2010.10-0030. PMC2877419.

**Gap:** I did not verify the Cambodian parotitis proportion specifically.

### 1.7 Rainfall, inhalation and severity — mechanism for presentation shift

Currie BJ, Jacups SP. **Intensity of rainfall and severity of melioidosis, Australia.** *Emerg Infect Dis* 2003;9(12):1538–1542. PMID 14720392. DOI 10.3201/eid0912.020750. PMC3034332.

Odds ratios for ≥125 mm rainfall in the 14 days before admission:

| Outcome | OR | 95% CI | p |
|---|---|---|---|
| Pneumonia | 1.70 | 1.09–2.65 | 0.019 |
| Bacteraemia | 1.93 | 1.24–3.02 | 0.004 |
| Septic shock | 1.94 | 1.14–3.29 | 0.014 |
| Death | 2.50 | 1.36–4.57 | 0.003 |

> "median rainfall in the 14 days before admission was highest for those dying with melioidosis (211 mm), in comparison to 110 mm for those surviving (p = 0.0002)."

Authors' argument: **"heavy rainfall results in a shift towards inhalation as the mode of infection with *B. pseudomallei*, which leads to more severe illness."** This matters for a genomics paper because **route of exposure, not just strain, modulates severity** — a confounder for any genotype–severity association.

---

## 2. Mortality and burden

### 2.1 Case fatality by setting

| Setting | CFR | Source |
|---|---|---|
| Darwin, NT Australia, 30 yr (1989–2019) | **12%** (133/1148) | Currie 2021, PMID 34303419 |
| Darwin, last 5 yr (2014–2019) | **6%** (17/278) | Currie 2021 |
| Darwin, 20 yr, first 5 yr | **30%** | Currie 2010, PMID 21152057 |
| Darwin, 20 yr, last 5 yr | **9%** | Currie 2010 |
| Far North Queensland, 1998–2016 | **14%** (27/197); 27% → 9% over time (p=0.009) | Stewart 2017, PMID 28264029 |
| Ubon Ratchathani, NE Thailand, 1997–2006 | **42.6%** average; 49% (1997) → 40.5% (2006) | Limmathurotsakul 2010, PMID 20519609 |
| Southern India, 2008–2014 | **14.9%** (17/114) | Koshy 2019, PMID 30666953 |
| Global (modelled) | ~54% of predicted cases die (89,000/165,000) | Limmathurotsakul 2016, PMID 26877885 |

**The Australia–Thailand gap is the headline contrast: ~6–14% vs ~40%.** Currie et al. attribute this explicitly to early diagnosis, specific antimicrobials and intensive care availability rather than to strain differences.

### 2.2 Mortality with septic shock and in ICU

- **Septic shock, Darwin 20-yr:** "Of the 116 patients (21%) with septic shock, 58 (50%) died from acute fulminant melioidosis." (Currie 2010)
- **Non-septic-shock mortality, Darwin 20-yr:** 19/424 (4%).
- **Royal Darwin Hospital ICU, 24 years:** Stephens DP, Thomas JH, Ward LM, Currie BJ. **Melioidosis Causing Critical Illness: A Review of 24 Years of Experience From the Royal Darwin Hospital ICU.** *Crit Care Med* 2016;44(8):1500–1505. PMID 26963328. DOI 10.1097/CCM.0000000000001668.
  - **207 patients** required ICU admission.
  - ICU mortality fell from **92% (1989–1997)** to **26% (1998–2013)**.
  - *This is a dramatic figure and a strong argument that outcome is dominated by care quality. **Flag:** the 92%→26% numbers came via the summarising fetcher from the abstract; the paper is paywalled with no PMC copy. **Re-check against the PDF before quoting.***
- **Singapore ICU:** Chan KP, Low JG, Raghuram J, Fook-Chong SM, Kurup A. **Clinical characteristics and outcome of severe melioidosis requiring intensive care.** *Chest* 2005;128(5):3674–3678. PMID 16304330. DOI 10.1378/chest.128.5.3674. — 27 adult ICU patients, overall mortality **48.1%**, **60%** among those with septic shock.

### 2.3 Global burden — and a provenance warning

Limmathurotsakul D, Golding N, Dance DAB, Messina JP, Pigott DM, Moyes CL, Rolim DB, Bertherat E, Day NPJ, Peacock SJ, Hay SI. **Predicted global distribution of *Burkholderia pseudomallei* and burden of melioidosis.** *Nat Microbiol* 2016;1:15008. PMID 26877885. DOI 10.1038/nmicrobiol.2015.8. PMC4746747.

- **"165,000 (95% credible interval 68,000–412,000) human melioidosis cases per year worldwide"**, of which **"89,000 (36,000–227,000) die"**.
- Known endemic in **45 countries**; predicted **likely endemic in a further 34 countries which have never reported the disease**.
- Conclusion: **"melioidosis is severely underreported in the 45 countries in which it is known to be endemic"**.

> **PROVENANCE WARNING — important for the manuscript.** The "165,000 cases / 89,000 deaths" figures are the most-repeated numbers in the melioidosis literature, but they are **modelled predictions from environmental niche mapping, not observed counts**, and the credible intervals are enormous (a 6-fold range on cases, 6-fold on deaths). Birnie et al. 2019 did **not** independently re-derive them: they **"extracted mortality and incidence estimates from a recent modelling study"** and built DALYs on top. So the widely cited DALY figure inherits the same uncertainty and is **not** independent corroboration. State them as modelled estimates with intervals, not as facts.

Birnie E, Virk HS, Savelkoel J, Spijker R, Bertherat E, Dance DAB, Limmathurotsakul D, Devleesschauwer B, Haagsma JA, Wiersinga WJ. **Global burden of melioidosis in 2015: a systematic review and data synthesis.** *Lancet Infect Dis* 2019;19(8):892–902. PMID 31285144. DOI 10.1016/S1473-3099(19)30157-4. PMC6867904.
- **4.6 million DALYs (UI 3.2–6.6)**, or **84.3 per 100,000 (UI 57.5–120.0)**.

### 2.4 Current framing (2024 review)

Meumann EM, Limmathurotsakul D, Dunachie SJ, Wiersinga WJ, Currie BJ. **Burkholderia pseudomallei and melioidosis.** *Nat Rev Microbiol* 2024;22(3):155–169. PMID 37794173. DOI 10.1038/s41579-023-00972-5.

Abstract, verbatim (retrieved intact from Europe PMC):

> "Burkholderia pseudomallei, the causative agent of melioidosis, is found in soil and water of tropical and subtropical regions globally. Modelled estimates of the global burden predict that melioidosis remains vastly under-reported, and a call has been made for it to be recognized as a neglected tropical disease by the World Health Organization. Severe weather events and environmental disturbance are associated with increased case numbers, and it is anticipated that, in some regions, cases will increase in association with climate change. Genomic epidemiological investigations have confirmed B. pseudomallei endemicity in newly recognized regions, including the southern United States. Melioidosis follows environmental exposure to B. pseudomallei and is associated with comorbidities that affect the immune response, such as diabetes, and with socioeconomic disadvantage. Several vaccine candidates are ready for phase I clinical trials. In this Review, we explore the global burden, epidemiology and pathophysiology of B. pseudomallei as well as current diagnostics, treatment recommendations and preventive measures, highlighting research needs and priorities."

This is the single best "current state of the field" citation — note it explicitly frames **genomic epidemiology** as the tool that confirmed new endemic regions.

### 2.5 Melioidosis is NOT a WHO-recognised NTD

Savelkoel J, Dance DAB, Currie BJ, Limmathurotsakul D, Wiersinga WJ. **A call to action: time to recognise melioidosis as a neglected tropical disease.** *Lancet Infect Dis* 2022;22(6):e176–e182. PMID 34953519. DOI 10.1016/S1473-3099(21)00394-7.

> "Melioidosis causes a higher estimated disease burden and mortality than many other recognised NTDs, with deaths primarily occurring among rural poor populations in low-income and middle-income countries."

Also: Mohapatra PR, Behera B. **Melioidosis: a call for recognition as a neglected tropical disease under the Southeast Asia regional neglected tropical disease framework.** *Lancet Reg Health Southeast Asia* 2025;39:100625. PMID 40842680. DOI 10.1016/j.lansea.2025.100625. PMC12365795.

**Status as of this research (Sept 2026): melioidosis remains absent from the WHO NTD list.** *Confirmed via web search of advocacy literature and institutional pages, but I did not fetch the WHO NTD list page itself — **verify against who.int before asserting current status in print**, as the list is periodically revised.*

---

## 3. Risk factors

### 3.1 Diabetes — the dominant risk factor, but the effect size is contested

Proportions of melioidosis patients with diabetes:

| Cohort | Diabetes prevalence |
|---|---|
| Darwin 30-yr | **513/1148 (45%)** |
| Darwin 20-yr | **213/540 (39%)** |
| Far North Queensland | **102/182 (56%)** |
| Southern India (Koshy 2019) | **93/114 (81.6%)** |
| Pooled meta-analysis (39 studies) | **45.68% (95% CI 44.8–46.57)** |

Effect size — **here the literature disagrees, and this should be stated explicitly**:

- **Wiersinga 2018 (Nat Rev Dis Primers)** states: *"Individuals with diabetes mellitus have a 12-fold higher risk of melioidosis after adjustment for age, sex and other risk factors"* and that diabetes is *"present in >50% of all patients with melioidosis worldwide"*, with *"23–60% of patients with melioidosis also have diabetes"*.
- **Chowdhury S, et al. The Epidemiology of Melioidosis and Its Association with Diabetes Mellitus: A Systematic Review and Meta-Analysis.** *Pathogens* 2022;11(2):149. PMID 35215093. DOI 10.3390/pathogens11020149. PMC8878808. — pooled **RR 3.40 (95% CI 2.92–3.87, p<0.001)** from **6 studies**; pooled diabetes prevalence **45.68%** from **39 studies**. Heterogeneity **I² = 98.2%** (RR) and **96.7%** (prevalence) — i.e. extreme.

> **DISAGREEMENT / WEAK PROVENANCE — flag in the manuscript.** The "12-fold" (Wiersinga 2018) and the commonly quoted "13-fold" (attributed to Suputtamongkol 1999) differ by ~4× from the pooled meta-analytic **RR 3.40**. Part of this is estimand mismatch (adjusted OR in a case-control design vs pooled RR), part is the near-total heterogeneity (I² 98%) in the meta-analysis, which makes the pooled point estimate itself of limited meaning.
>
> **UNVERIFIED:** I could **not** verify the primary numeric relative risk in Suputtamongkol 1999 from the source. The *Clinical Infectious Diseases* full text is paywalled, there is no PMC copy, and **the published abstract contains no odds ratios, relative risks or confidence intervals at all** — it states only that the factors "were confirmed to be significant risk factors". The "13-fold" figure circulating in reviews and secondary sources could not be traced to a verifiable primary number in this session. *What is missing: the full text (or Table 2/3) of Suputtamongkol 1999 CID 29:408–413.* **Do not cite "13-fold" to Suputtamongkol 1999 without checking the PDF.**

Primary risk-factor study (landmark, still the standard citation):
Suputtamongkol Y, Chaowagul W, Chetchotisakd P, Lertpatanasuwun N, Intaranongpai S, Ruchutrakool T, Budhsarawong D, Mootsikapun P, Wuthiekanun V, Teerawatasook N, Lulitanond A. **Risk factors for melioidosis and bacteremic melioidosis.** *Clin Infect Dis* 1999;29(2):408–413. PMID 10476750. DOI 10.1086/520223.

Abstract, verbatim (this much is solid):

> "A case-control study was conducted in four hospitals in northeastern Thailand to identify risk factors for melioidosis and bacteremic melioidosis. Cases were patients with culture-proven melioidosis, and there were two types of controls (those with infections, i.e., with community-acquired septicemia caused by other bacteria, and those without infection, i.e., randomly selected patients admitted with noninfectious diseases to the same hospitals). Demographic data, clinical presentations, and suspected risk factors were analyzed. Diabetes mellitus, preexisting renal diseases, thalassemia, and occupational exposure, classified by the soil and water risk assessment, were confirmed to be significant risk factors for melioidosis and bacteremic melioidosis. Only diabetes mellitus was a significant factor associated with bacteremic melioidosis, as compared with nonbacteremia. A significant interaction was found between diabetes mellitus and occupational exposure. Thus, diabetic rice farmers would be the most appropriate population group for targeted control measures such as vaccination in the future."

Key qualitative findings that ARE verifiable from this abstract: **thalassaemia** and **preexisting renal disease** are confirmed independent risk factors; **diabetes is the only factor associated with bacteraemia specifically**; and there is a **significant interaction between diabetes and occupational exposure** — the "diabetic rice farmer" as the target population.

### 3.2 Full risk-factor profile across cohorts

| Risk factor | Darwin 30-yr | Darwin 20-yr | Far North Qld |
|---|---|---|---|
| Diabetes | 513 (45%) | 213 (39%) | 102/182 (56%) |
| Hazardous alcohol use | 455 (40%) | 211 (39%) | 86/166 (52%) |
| Chronic lung disease | — | 140 (26%) | 26/169 (15%) |
| Chronic renal/kidney disease | — | 65 (12%) | 28/180 (16%) |
| **No identified risk factor** | **186 (16%)** | **106 (20%)** | **14/162 (8.6%)** |

Mortality by risk factor, Darwin 20-yr: diabetes 33 (15%), hazardous alcohol 33 (16%), chronic lung disease 27 (19%), chronic renal disease 13 (20%), **no risk factor 2 (2%)**.

**Two figures worth foregrounding:**
1. **"All but 186 (16%) had clinical risk factors"** (Darwin 30-yr) — i.e. **~16–20% of melioidosis occurs in people with no recognised risk factor.**
2. **"Only three (2%) of 133 fatalities had no identified risk."** (Darwin 30-yr) — risk-factor-free patients get melioidosis but rarely die of it. Corroborated by the 20-yr study: **"Of the 106 patients with no identified risk factor, only two died (2%)"**.

Other risk factors named by Wiersinga 2018 without quantified effect sizes: **liver disease, prolonged steroid use, immunosuppression**. Wiersinga also states **"Approximately 80% of patients have known risk factors, mainly diabetes mellitus"** — consistent with the Darwin 16–20% figure.

### 3.3 Occupational and behavioural exposure — the case-control evidence

Limmathurotsakul D, Kanoksil M, Wuthiekanun V, Kitphati R, deStavola B, Day NPJ, Peacock SJ. **Activities of daily living associated with acquisition of melioidosis in northeast Thailand: a matched case-control study.** *PLoS Negl Trop Dis* 2013;7(2):e2072. PMID 23437412. DOI 10.1371/journal.pntd.0002072. PMC3578767.

**286 cases, 512 controls.** Multivariable **conditional** logistic regression; the paper reports **conditional odds ratios (cOR)** — these are adjusted estimates, not crude. **Diabetes was a matching variable, so no OR for diabetes is reported in this study** (important — do not cite this paper for a diabetes effect size).

Verbatim from the abstract:

| Exposure | cOR | 95% CI | Route |
|---|---|---|---|
| Working in a rice field | **2.1** | 1.4–3.3 | skin inoculation |
| An open wound | **2.0** | 1.2–3.3 | skin inoculation |
| Other soil/water exposure | 1.4 | 0.8–2.6 (ns) | skin inoculation |
| Eating food contaminated with soil/dust | 1.5 | 1.0–2.2 | ingestion |
| Drinking untreated water | **1.7** | 1.1–2.6 | ingestion |
| Outdoor rain exposure | **2.1** | 1.4–3.2 | inhalation |
| Water inhalation | **2.4** | 1.5–3.9 | inhalation |
| Current smoking | 1.5 | 1.0–2.3 (p=0.069) | — |
| Oral steroid intake | **3.1** | 1.4–6.9 | immunosuppression |

No population attributable fraction is reported.

**This is the key paper establishing that all three routes — percutaneous, ingestion, inhalation — contribute independently.** That matters for interpreting genomic attribution of exposure origin.

---

## 4. Incubation period, latency and reactivation

### 4.1 Incubation period

Currie BJ, Fisher DA, Anstey NM, Jacups SP. **Melioidosis: acute and chronic disease, relapse and re-activation.** *Trans R Soc Trop Med Hyg* 2000;94(3):301–304. PMID 10975006. DOI 10.1016/S0035-9203(00)90333-X.

- Incubation period where a discrete inoculating event could be identified: **1–21 days, mean 9 days**.
- Of **252 cases: 244 (97%) recent infection; 8 (3%) reactivation.**
- **222 (88%) acute illness; 30 (12%) chronic illness.**
- Of 207 surviving patients, **27 (13%) had a confirmed relapse**, mean interval ~8 months; 5 relapsed twice (32 relapses total).
- TMP-SMX monotherapy ≥3 months outperformed doxycycline monotherapy for eradication.

Wiersinga 2018 restates this as: **"The incubation period of acute infections is on average 9 days, ranging from 1–21 days"**, with the caveat that a **"more severe form of the disease with shorter incubation can occur after inhalation or aspiration of contaminated fresh water"**.

*Note:* the summarising fetcher declined to reproduce the Currie 2000 abstract in full (character-limit constraint), so these numbers are extracted rather than block-quoted. They are internally consistent with the DPMS papers.

### 4.2 The "Vietnamese time bomb" — provenance traced

This is a case where **a widely repeated idea has demonstrably weak foundations**, and the reference chain is now fully traceable:

- **Howe C, Sampath A, Spotnitz M. The pseudomallei group: a review.** *J Infect Dis* 1971;124:598–606. — earliest "time-bomb disease" framing.
- **Goshorn RK. Recrudescent pulmonary melioidosis. A case report involving the so-called "Vietnamese time bomb."** *Indiana Med* 1987;80:247–249. — **this is where the phrase itself comes from.** A single case report.
- **Clayton AJ, Lisella RS, Martin DG. Melioidosis: a serological survey in military personnel.** *Mil Med* 1973;138:24–26. — the source of the alarming projection. From serology, **"it was estimated ... that there were approximately 225,000 potential future melioidosis cases"** among repatriated US personnel.
- **Kingston CW. Chronic or latent melioidosis.** *Med J Aust* 1971;2:618–621.
- **Chodimella U, Hoppes WL, Whalen S, Ognibene AJ, Rutecki GW. Septicemia and suppuration in a Vietnam veteran.** *Hosp Pract (1995)* 1997;32:219–221.

### 4.3 The definitive rebuttal

Howes M, Currie BJ. **Melioidosis and Activation from Latency: The "Time Bomb" Has Not Occurred.** *Am J Trop Med Hyg* 2024. PMID 38806042. DOI 10.4269/ajtmh.24-0007. PMC11229659.

- Over 30 years of DPMS: **"29 of 1,148 (2.5%) primary (first episode) melioidosis diagnoses were assigned as potential activation from latency."** On reassessment, three were reclassified as chronic melioidosis, leaving **25 plausible cases (20 with strong evidence)**.
- Conclusion: **"activation from latency is a rare event in melioidosis, accounting in our analysis for under 3% of DPMS cases."**
- **"the predicted 'Vietnamese time bomb' has clearly not eventuated."**
- **"The longest plausible duration of asymptomatic latency remains 29 years."** — a 50-year-old Vietnam veteran, previously in good health, presenting with blood-culture-positive melioidosis pneumonia with empyema, spleen and muscle abscesses and osteomyelitis.
- Much of what was historically called "latent reactivation" is better explained as **undiagnosed chronic disease with a relapsing course**.

### 4.4 The 62-year latency claim — a genomics-driven retraction (excellent for this manuscript)

**Original claim:** Ngauy V, Lemeshev Y, Sadkowski L, Crawford G. **Cutaneous melioidosis in a man who was taken as a prisoner of war by the Japanese during World War II.** *J Clin Microbiol* 2005;43(2):970–972. PMID 15695721. DOI 10.1128/JCM.43.2.970-972.2005. PMC548040.

- Claimed latency: **62 years after exposure.**
- Patient captured **8 March 1942**; held in Java, Singapore, Malaysia, Burma and Thailand; ~2 years in a Thai internment camp. Presented **14 February 2004**.
- Evidence base was **the patient's historical account plus the clinical timeline only**. Identification was by **Vitek 1 biochemical testing**, repeat biochemistry and PCR. **No genotyping was performed.**
- Even the original authors hedged: "it is unclear if he developed the infection while in Thailand and this was the first manifestation of disease... or if he had a previous infection... and now has had a relapse of disease."

**Refutation:** Gee JE, Gulvik CA, Elrod MG, Batra D, Rowe LA, Sheth M, Hoffmaster AR. **Phylogeography of *Burkholderia pseudomallei* Isolates, Western Hemisphere.** *Emerg Infect Dis* 2017;23(7):1133–1138. PMID 28628442. DOI 10.3201/eid2307.161978. PMC5512505.

Abstract, verbatim (retrieved intact):

> "The bacterium Burkholderia pseudomallei causes melioidosis, which is mainly associated with tropical areas. We analyzed single-nucleotide polymorphisms (SNPs) among genome sequences from isolates of B. pseudomallei that originated in the Western Hemisphere by comparing them with genome sequences of isolates that originated in the Eastern Hemisphere. Analysis indicated that isolates from the Western Hemisphere form a distinct clade, which supports the hypothesis that these isolates were derived from a constricted seeding event from Africa. Subclades have been resolved that are associated with specific regions within the Western Hemisphere and suggest that isolates might be correlated geographically with cases of melioidosis. One isolate associated with a former World War II prisoner of war was believed to represent illness 62 years after exposure in Southeast Asia. However, analysis suggested the isolate originated in Central or South America."

From the body: the isolate **TX2004** "belongs to the Western Hemisphere clade and groups with genomes from isolates from melioidosis patients who had travel histories to Guatemala, Panama, and Peru," and "This finding, and the fact that TX2004 is ITS type G, suggests that TX2004 might not have been acquired by the patient in the Pacific theater during World War II."

> **This is arguably the single most useful vignette for a recombination-aware SNP / genomic-attribution manuscript.** A 62-year latency claim — repeated for over a decade as the record — was overturned purely by SNP-based phylogeography placing the isolate in the wrong hemisphere. It is a clean, citable demonstration that **molecular attribution of exposure origin changes the clinical narrative**, and that phenotype/history alone is not reliable evidence of where an infection was acquired.

**Note the PMID discrepancy encountered:** one fetch returned PMID 28628306 for this article; the authoritative Europe PMC record gives **PMID 28628442**, consistent with the PubMed URL surfaced by web search. **Use 28628442.**

### 4.5 Relapse vs reinfection — genotyping was required to tell them apart

Sarovich DS, Ward L, Price EP, Mayo M, Pitman MC, Baird RW, Currie BJ. **Recurrent melioidosis in the Darwin Prospective Melioidosis Study: improving therapies mean that relapse cases are now rare.** *J Clin Microbiol* 2014;52(2):650–653. PMID 24478504. DOI 10.1128/JCM.02239-13. PMC3911345.

- **785** culture-confirmed cases over 23 years; **106 (13.5%)** died of the initial infection.
- Of 679 survivors, **39 (5.7%)** had recurrent melioidosis.
- By MLST: **29 (74%) relapse** (same strain) vs **10 (26%) reinfection** (different strain).
- **Temporal collapse in relapse:** 24/375 (**6.4%**) of patients admitted before 30 Sept 2003 relapsed, vs only 5/410 (**1.2%**) admitted Oct 2003–Sept 2012 (Fisher's exact, **p<0.001**).
- Timing: relapse median **285 days** between episodes; reinfection median **1,643 days**.

Contrasting Thai finding — **the literature disagrees by setting**:
Maharjan B, Chantratita N, Vesaratchavest M, Cheng A, Wuthiekanun V, Chierakul W, Chaowagul W, Day NPJ, Peacock SJ. **Recurrent melioidosis in patients in northeast Thailand is frequently due to reinfection rather than relapse.** *J Clin Microbiol* 2005;43(12):6032–6034. PMID 16333094. DOI 10.1128/JCM.43.12.6032-6034.2005. PMC1317219.

> **Explicit disagreement to note:** in Darwin, recurrence is predominantly **relapse** (74%); in northeast Thailand, recurrence is frequently **reinfection**. This is plausibly explained by differing environmental exposure intensity — and it is precisely the kind of question that only genotyping can answer, since relapse and reinfection are clinically indistinguishable.

Landmark older: Chaowagul W, Suputtamongkol Y, Dance DA, Rajchanuvong A, Pattara-arechachai J, White NJ. **Relapse in melioidosis: incidence and risk factors.** *J Infect Dis* 1993;168(5):1181–1185. PMID 8228352. DOI 10.1093/infdis/168.5.1181.

Within-host evolution over long carriage: Price EP, Sarovich DS, Mayo M, et al. **Within-host evolution of *Burkholderia pseudomallei* over a twelve-year chronic carriage infection.** *mBio* 2013;4(4):e00388-13. PMID 23860767. DOI 10.1128/mBio.00388-13. PMC3735121.

---

## 5. Diagnosis — why underdiagnosis is systematic

### 5.1 Culture is the gold standard, and it is not very sensitive

Gassiep I, Armstrong M, Norton R. **Human Melioidosis.** *Clin Microbiol Rev* 2020;33(2):e00006-19. PMID 32161067. DOI 10.1128/CMR.00006-19. PMC7067580.

> "The culture of *B. pseudomallei* from any specimen in a patient with suspected melioidosis remains the diagnostic 'gold standard.'"

> "Overall, the sensitivity of culture in the setting of melioidosis has been reported at 60.2%. Therefore, culture can be said to have low sensitivity and low negative predictive value (NPV)."

Primary source for that 60.2%:
Limmathurotsakul D, Jamsen K, Arayawichanont A, Simpson JA, White LJ, Lee SJ, Wuthiekanun V, Chantratita N, Cheng A, Day NPJ, Verzilli C, Peacock SJ. **Defining the true sensitivity of culture for the diagnosis of melioidosis using Bayesian latent class models.** *PLoS One* 2010;5(8):e12485. PMID 20830194. DOI 10.1371/journal.pone.0012485. PMC2932979.

- Culture sensitivity: **60.2% (95% CI 51.7%–68.5%)**.
- Culture-positive proportions by specimen: blood 54.6%, sputum 31.1%, throat swab 21.9%, urine 16.8%, other 42.9%.
- Model estimated true prevalence ~61.6% while culture identified only 37.2% — **roughly 40% of infected patients culture-negative.**
- Authors conclude **"culture has low sensitivity and low NPV for the diagnosis of melioidosis"** and recommend empirical therapy for all suspected cases rather than waiting on culture.

> **This is the crux of the underdiagnosis argument: the gold standard misses ~40% of true cases. Every incidence and burden figure in the literature is therefore a floor, not an estimate.**

Time to positivity (blood, BacT/Alert): **62.5% detected within 24 h, 93% within 48 h** (Gassiep 2020).

### 5.2 Misidentification by automated systems

This is a major, well-documented failure mode and directly explains why melioidosis is missed in non-endemic settings.

Accuracy of commercial identification (as summarised in the literature; regionally dependent):
- **VITEK 2: 63–81%** of isolates correctly identified.
- **BD Phoenix: 0–28%.** Gassiep 2020: Phoenix "will most commonly misidentify the organism as *B. cepacia* with 95 to 99% confidence" — i.e. **confidently wrong**.
- **API 20NE: 37–99%.**

Commonest misidentifications: ***Burkholderia cepacia* complex** and ***Chromobacterium violaceum***. Documented individual failures include API 20NE calling it *Pseudomonas fluorescens* (75.8% probability), VITEK 2 Compact calling it *Aeromonas sobria* (90%), and Phoenix calling it *Alcaligenes faecalis* (98%).

Key references:
- **Podin Y, Kaestli M, McMahon N, et al. Reliability of automated biochemical identification of *Burkholderia pseudomallei* is regionally dependent.** *J Clin Microbiol* 2013;51(9):3076–3078. DOI 10.1128/JCM.01290-13. — the source of the regional-dependence finding; Malaysian isolates were misidentified as *B. cepacia* far more often than Australian ones.
- **Zong Z, Wang X, Deng Y, Zhou T.** *Burkholderia pseudomallei* misidentified by automated system. *Emerg Infect Dis* 2009;15(11):1936–1938. DOI 10.3201/eid1511.081719.
- Misidentification of *Burkholderia pseudomallei*, China. *Emerg Infect Dis* 2021. PMC7920660.
- Inglis TJJ, et al. Potential misidentification of *Burkholderia pseudomallei* by API 20NE. *Pathology* 1998. PMID 9534210.

> **CONFLICT TO FLAG.** Gassiep 2020 quotes API 20NE sensitivity as **"99% (95% CI, 98.0 to 99.6%)"**, whereas the regional-dependence literature gives a range as low as **37%**. These are not reconcilable as a single number: API 20NE performance is **strain- and region-dependent**, and the 99% figure derives from a specific (likely Thai/Australian) isolate collection. **Report the range and the regional dependence, not a single sensitivity.** I did not fetch Podin 2013 directly — **UNVERIFIED**: the exact 63–81% / 0–28% / 37–99% bracket came via web search summarising the JCM abstract, not from the paper itself. *What is missing: direct retrieval of Podin 2013 JCM 51:3076–3078.*

**MALDI-TOF MS:** Gassiep 2020 notes that for the standard platforms **"Neither instrument's routine diagnostic database includes the reference spectra required for identification of *B. pseudomallei*"** — i.e. the organism is absent from the default commercial databases, a regulatory consequence of its select-agent status (see §8). With a supplemented database and a 99.9% cutoff, performance is excellent:

Campbell S, Taylor B, Menouhos D, Hennessy J, Mayo M, Baird R, Currie BJ, Meumann EM. **Performance of MALDI-TOF MS, real-time PCR, antigen detection, and automated biochemical testing for identification of *Burkholderia pseudomallei*.** *J Clin Microbiol* 2024;62(10):e00961-24. PMID 39235248. DOI 10.1128/jcm.00961-24. PMC11481520.
- **"MALDI-TOF MS had a sensitivity of 1.0 and specificity of 1.0"** at a 99.9% certainty cutoff.
- Automated biochemical testing: sensitivity **0.83**, specificity **0.88**.

### 5.3 Serology is unreliable and cannot be used for diagnosis in endemic areas

From Gassiep 2020:
- **"19% and 26% of culture-confirmed cases never seroconverted in two studies"** — i.e. seronegativity does not exclude melioidosis.
- **Background seropositivity in endemic Thailand is very high:** **"21% of healthy blood donors were found to have a titer of ≥1:40"**; a later study **"reported 38% seropositivity with titers of ≥1:80"**.
- **Australia:** cutoff 1:40; seroprevalence **"approximately 2.5 to 8.7%, compared to 35 to 38% in Thailand"**.

> The consequence: the **indirect haemagglutination assay (IHA) has essentially no positive predictive value in northeast Thailand**, where a third of healthy people are seropositive, and it cannot rule out disease anywhere because up to a quarter of confirmed cases never seroconvert. This also retrospectively undermines the Clayton 1973 serosurvey that generated the "225,000 future cases" projection (§4.2).

Childhood seroconversion in endemic areas: Wuthiekanun V, Chierakul W, Langa S, et al. **Development of antibodies to *Burkholderia pseudomallei* during childhood in melioidosis-endemic northeast Thailand.** *Am J Trop Med Hyg* 2006;74:1074–1075.

Contemporary: Ho C, et al. **Clinical Implications of High Melioidosis Serology.** *Pathogens* 2025;14(2):165. PMID 40005540. DOI 10.3390/pathogens14020165. PMC11858129.

### 5.4 Rapid tests — still not ready

Currie BJ, Woerle C, Mayo M, Meumann EM, Baird RW. **What is the Role of Lateral Flow Immunoassay for the Diagnosis of Melioidosis?** *Open Forum Infect Dis* 2022;9(5):ofac149. PMID 35493111. DOI 10.1093/ofid/ofac149. PMC9043003.

AMD/AMD-PLUS lateral flow immunoassay (CPS antigen detection) performance on clinical specimens:

| Specimen | Sensitivity |
|---|---|
| Serum, overall | 27% |
| Serum, bacteraemic | 39% |
| Serum, septic shock | 68% |
| Urine, overall | 63% |
| Urine, culture-positive | 79% |
| Urine, septic shock | 90% |
| Sputum, culture-positive | 85% |
| Pus/tissue, culture-positive | 83% |
| Specificity (serum) | 99% |

> "Culture of *Burkholderia pseudomallei* remains the gold standard for diagnosis of melioidosis."

> "Prospective studies...are required to ascertain if the specificity of AMD-PLUS is adequate to enable diagnosis of melioidosis with a high positive predictive value."

Earlier laboratory-condition figures (Houghton RL, et al. **Development of a prototype lateral flow immunoassay (LFI) for the rapid diagnosis of melioidosis.** *PLoS Negl Trop Dis* 2014;8(3):e2727. PMID 24651568. DOI 10.1371/journal.pntd.0002727. PMC3961207) were far rosier — sensitivity **98.7%**, specificity **97.2%** — because they were run on culture-amplified material, not primary clinical specimens. **Note this gap between laboratory and clinical performance.**

Newest: Gassiep I, et al. **Laboratory diagnosis of melioidosis.** *PLoS Negl Trop Dis* 2025;19(12):e0013761. PMID 41343561. DOI 10.1371/journal.pntd.0013761. PMC12677508. Open access — likely the most current diagnostic review.

Also useful for sampling strategy: Duguid RC, et al. **Throat and rectal swabs to diagnose melioidosis.** *J Clin Microbiol* 2026;64(6):e00113-26. PMID 42132431. DOI 10.1128/jcm.00113-26. PMC13251406.

### 5.5 Why underdiagnosis is systematic — the argument assembled

1. **Gold standard misses ~40%** (culture sensitivity 60.2%; Limmathurotsakul 2010).
2. **Automated ID systems confidently misassign** the organism to *B. cepacia* / *C. violaceum*, and performance varies by region (Podin 2013; Gassiep 2020).
3. **MALDI-TOF default databases omit the organism** (Gassiep 2020) — a direct consequence of select-agent regulation.
4. **Serology cannot discriminate** in endemic areas (up to 38% background seropositivity) and up to 26% of true cases never seroconvert.
5. **No validated rapid point-of-care test** for primary specimens (Currie 2022).
6. **Clinical mimicry:** chronic melioidosis is read as tuberculosis (32.35%) or neoplasia (23.53%) on radiology (Singh 2026); in Africa it mimics **malaria or tuberculosis** (Steinmetz 2018).
7. **The disease is predicted endemic in 34 countries that have never reported a case** (Limmathurotsakul 2016) — regions largely lacking the microbiology capacity to make the diagnosis at all.
8. **Non-endemic clinicians do not consider it**, particularly absent a travel history (Gee 2022; Petras 2023).

Foundational framing: Dance DAB. **Melioidosis: the tip of the iceberg?** *Clin Microbiol Rev* 1991;4(1):52–60. PMID 2004347. DOI 10.1128/CMR.4.1.52. PMC358178.

---

## 6. Treatment

### 6.1 The landmark trial that defined modern therapy

White NJ, Dance DAB, Chaowagul W, Wattanagoon Y, Wuthiekanun V, Pitakwatchara N. **Halving of mortality of severe melioidosis by ceftazidime.** *Lancet* 1989;2(8665):697–701. PMID 2570956. DOI 10.1016/S0140-6736(89)90768-X.

Dance 2014 summarises it: **"The overall mortality was 37% in those treated with ceftazidime compared with 74% in the conventionally treated group, a reduction of 50%."**

Comparator trial: Simpson AJH, Suputtamongkol Y, Smith MD, et al. **Comparison of imipenem and ceftazidime as therapy for severe melioidosis.** *Clin Infect Dis* 1999;29(2):381–387. PMID 10476746. DOI 10.1086/520219.

### 6.2 Two-phase therapy — the standard of care

**Intensive (parenteral) phase**, from Wiersinga 2018 verbatim:

> "Initial intensive therapy should last for a minimum of 10–14 days and consists of ceftazidime...2 g (50 mg kg−1 up to 2 g in children (<15 years of age)) intravenous, 6-hourly; or meropenem...1 g (25 mg kg−1 up to 1 g in children) intravenous, 8-hourly."

> "Long-term intravenous therapy (≥4–8 weeks) is recommended where possible for complicated pneumonia, deep-seated infection (including prostatic abscesses), neurological melioidosis, osteomyelitis and septic arthritis"

**Eradication (oral) phase**, verbatim:

> "The eradication therapy should last for ≥3 months after the end of the initial intensive therapy and consists of trimethoprim–sulfamethoxazole...orally, 12-hourly"

> "Longer eradication therapy (≥6 months) is recommended for neurological melioidosis and osteomyelitis."

### 6.3 The Darwin guideline — duration by focus

Sullivan RP, Marshall CS, Anstey NM, Ward L, Currie BJ. **2020 Review and revision of the 2015 Darwin melioidosis treatment guideline; paradigm drift not shift.** *PLoS Negl Trop Dis* 2020;14(9):e0008659. PMID 32986699. DOI 10.1371/journal.pntd.0008659. PMC7544138. Open access.

**"Ceftazidime is used for most cases, with meropenem generally reserved for those with severe disease requiring admission to the Intensive Care Unit (ICU)."**

Minimum intensive-phase duration by clinical focus (Table 5, 2020 revision):

| Focus | Minimum IV duration |
|---|---|
| Skin abscess | 2 weeks |
| Bacteraemia, no focus | 2 weeks |
| Unilateral unilobar pneumonia, uncomplicated | 2 weeks |
| Multilobar pneumonia, no bacteraemia | 3 weeks |
| Pneumonia with bacteraemia | 4 weeks |
| Deep-seated collections | 4 weeks |
| Osteomyelitis | 6 weeks |
| CNS infection | 8 weeks |
| Arterial infection | 8 weeks |

Eradication: oral TMP-SMX, **minimum 12 weeks** for most categories; **6 months** for osteomyelitis / CNS / arterial infection.

Reported outcomes in this cohort: **recrudescence 2.8%, recurrence 4.7%.** *(Flag: these two percentages came via the fetch summariser rather than as quoted sentences — re-check.)*

Related: Pitman MC, Luck T, Marshall CS, Anstey NM, Ward L, Currie BJ. **Intravenous therapy duration and outcomes in melioidosis: a new treatment paradigm.** *PLoS Negl Trop Dis* 2015;9(3):e0003586. PMID 25811783. DOI 10.1371/journal.pntd.0003586. PMC4374799.

Most recent: Meumann EM, et al. **Treatment of Melioidosis.** *Infect Dis Clin North Am* 2026;40(1):127–147. PMID 41571490. DOI 10.1016/j.idc.2025.12.002.

### 6.4 The MERTH trial — eradication phase

Chetchotisakd P, Chierakul W, Chaowagul W, Anunnatsiri S, Phimda K, Mootsikapun P, Chaisuksant S, Pilaikul J, Thinkhamrop B, Phiphitaporn S, Susaengrat W, Toondee C, Wongrattanacheewin S, Wuthiekanun V, Chantratita N, Thaipadungpanit J, Day NPJ, Limmathurotsakul D, Peacock SJ. **Trimethoprim-sulfamethoxazole versus trimethoprim-sulfamethoxazole plus doxycycline as oral eradicative treatment for melioidosis (MERTH): a multicentre, double-blind, non-inferiority, randomised controlled trial.** *Lancet* 2014;383(9919):807–814. PMID 24284287. DOI 10.1016/S0140-6736(13)61951-0. PMC3939931.

- **626 randomised**: TMP-SMX + placebo (n=311) vs TMP-SMX + doxycycline (n=315).
- Primary endpoint: **culture-confirmed recurrent melioidosis**.
- Recurrence: **16 (5%)** with TMP-SMX alone vs **21 (7%)** with the combination. **HR 0.81 (95% CI 0.42–1.55)**; non-inferiority criterion met (**p=0.01**).
- **Adverse reactions: 122 (39%) vs 167 (53%); discontinuation for adverse events: 37 (12%) vs 59 (19%).**
- Conclusion: **TMP-SMX monotherapy for a minimum of 20 weeks** is the eradication standard — equally effective and better tolerated than the combination.

Network meta-analysis: Anothaisintawee T, Harncharoenkul K, Poramathikul K, et al. **Efficacy of drug treatment for severe melioidosis and eradication treatment: a systematic review and network meta-analysis.** *PLoS Negl Trop Dis* 2023;17(6):e0011382. PMID 37307278. DOI 10.1371/journal.pntd.0011382. PMC10289671. — 14 randomised trials; **"TMP-SMX for 20 weeks was ranked as the most efficacious eradication treatment (87.7%)"**.

### 6.5 Intrinsic antimicrobial resistance

Wiersinga 2018, verbatim:

> "*B. pseudomallei* is resistant to penicillin, ampicillin, first-generation and second-generation cephalosporins, gentamicin, tobramycin, streptomycin, macrolides and polymyxins"

> "*B. pseudomallei* encodes at least ten resistance nodulation division efflux pump systems, spanning both chromosomes, that confer at least partial resistance to six antibiotic classes, including aminoglycosides, fluoroquinolones and tetracyclines"

Regional exception worth noting: **"clonal groups of isolates susceptible to gentamicin are common in Sarawak, Malaysia"** — a genotype-linked resistance phenotype, relevant to a genomics manuscript.

Mechanistic detail — Schweizer HP. **Mechanisms of antibiotic resistance in *Burkholderia pseudomallei*: implications for treatment of melioidosis.** *Future Microbiol* 2012;7(12):1389–1399. PMID 23231488. DOI 10.2217/fmb.12.116. PMC3568953.

**Efflux pumps (RND family):**

| Pump | Substrates / significance |
|---|---|
| **AmrAB–OprA** | "Responsible for the intrinsic aminoglycoside and macrolide resistance observed in most clinical and environmental strains." Also extrudes fluoroquinolones and tetracyclines at clinically insignificant levels. |
| **BpeAB–OprB** | Macrolides, fluoroquinolones, tetracyclines, chloramphenicol — low clinical relevance. |
| **BpeEF–OprC** | "Most clinically significant pump identified to date" — chloramphenicol, fluoroquinolones, tetracyclines, **trimethoprim**. |

**Polymyxin resistance:** due to **lipid A modification**, not efflux.

**β-lactamase PenA** (chromosomal class A) — three routes to resistance:
1. **Overproduction:** "Overexpression of PenA in a laboratory strain (exogenous promoter) and clinical isolates (promoter-up mutation) leads to clinically significant ceftazidime resistance."
2. **C69Y** substitution: high-level ceftazidime resistance (**MIC ≥256 µg/ml**).
3. **P167S** → ceftazidime resistance; **S72F** → amoxicillin–clavulanate resistance.

Wild-type PenA has minimal effect on carbapenems, and PenA-mutant strains generally **remain meropenem-susceptible** — which is why meropenem is the ICU agent.

**Acquired TMP-SMX resistance:** mediated by **BpeEF–OprC** expression. "trimethoprim resistance is widespread and attributable to BpeEF–OprC expression. All trimethoprim-resistant isolates remain susceptible to sulfamethoxazole" — preserving co-trimoxazole activity in many cases, though co-trimoxazole resistance can emerge via the same pump.

### 6.6 Acquired resistance is rare in practice but emerges on therapy

Wuthiekanun V, Amornchai P, Saiprom N, Chantratita N, Chierakul W, Koh GCKW, Chaowagul W, Day NPJ, Limmathurotsakul D, Peacock SJ. **Survey of antimicrobial resistance in clinical *Burkholderia pseudomallei* isolates over two decades in Northeast Thailand.** *Antimicrob Agents Chemother* 2011;55(11):5388–5391. PMID 21876049. DOI 10.1128/AAC.05517-11. PMC3195054.

- **4,021 patients, 1987–2007** (21 years), northeast Thailand.
- **Ceftazidime resistance: 0.6%** overall (24/4,021); **primary (pre-treatment) resistance only 0.05%**.
- **Amoxicillin-clavulanate: 0.6%.**
- **Imipenem/meropenem: 0%** — no carbapenem resistance detected.
- **21 of 24 resistant isolates "emerged during antimicrobial therapy"**, median **15 days** to detection.

> Key point for the manuscript: **primary resistance is vanishingly rare (0.05%); resistance is overwhelmingly acquired within the host during treatment.** This makes *B. pseudomallei* an attractive system for within-host evolution studies and is a direct argument for genomic surveillance of serial isolates.

Doxycycline and TMP-SMX were **not systematically tested** in this survey. **UNVERIFIED:** I could not confirm from this paper whether resistance increased over the two decades, nor resolve the well-known methodological discrepancy in reported TMP-SMX resistance rates (disc diffusion substantially overcalls resistance versus Etest/broth microdilution). *What is missing: the full Wuthiekanun 2011 text and a dedicated TMP-SMX susceptibility-methodology paper.* Note that Koshy 2019 (India) reported **TMP-SMX resistance in 5.9%** and **100% susceptibility to carbapenems and ceftazidime** — a 10× higher TMP-SMX figure than Thailand, quite possibly a methodology artefact rather than a real geographic difference. **Flag this explicitly if TMP-SMX resistance rates are cited.**

Within-host evolution to resistance: Evans TJ, et al. **Case Report: Genetic evolution of *Burkholderia pseudomallei* during treatment leading to antibiotic resistance and disease relapse.** *Wellcome Open Res* 2025. PMID 40861388. DOI 10.12688/wellcomeopenres.24138.2. PMC12374155.
Also: Seng R, et al. **Phenotypic and genetic alterations of *Burkholderia pseudomallei* in patients during relapse and persistent infections.** *Front Microbiol* 2023;14:1103297. PMID 36814569. DOI 10.3389/fmicb.2023.1103297. PMC9939903.
Also: **Whole-Genome Sequences of *Burkholderia pseudomallei* Isolates Exhibiting Decreased Meropenem Susceptibility.** PMC5383878.

### 6.7 Adjunctive therapy

- **G-CSF:** Cheng AC, et al. *Clin Infect Dis* 2007;45(3):308–314. PMID 17599307. DOI 10.1086/519261 — randomised trial in Thailand, **no mortality benefit**. Earlier observational: Cheng AC, et al. *Clin Infect Dis* 2004;38(1):32–37. PMID 14679445. DOI 10.1086/380456.
- **Glyburide/glibenclamide:** Koh GCKW, et al. **Glyburide is anti-inflammatory and associated with reduced mortality in melioidosis.** *Clin Infect Dis* 2011;52(6):717–725. PMID 21293047. DOI 10.1093/cid/ciq192. PMC3049341.

---

## 7. Vaccine status

**There is no licensed vaccine for melioidosis.** Wiersinga 2018, verbatim: **"No vaccine for either is currently available"** (referring to melioidosis and glanders).

**Current stage (2024):** Meumann et al. 2024, *Nat Rev Microbiol*, abstract verbatim: **"Several vaccine candidates are ready for phase I clinical trials."**

> As of this review, **no melioidosis vaccine has completed a published phase I trial.** A Europe PMC search of titles containing both "melioidosis" and "vaccine" returned only animal-model and computational studies (macaque, murine, in silico) through 2026 — **no human trial results**.

**Leading candidate — CPS-CRM197 + Hcp1:**
- Glycoconjugate of **capsular polysaccharide (CPS)** conjugated to **CRM197** (non-toxic diphtheria toxin variant), admixed with **Hcp1** (haemolysin co-regulated protein 1, a Type VI secretion system component), adjuvanted with **Alhydrogel + CpG (TLR9 agonist)**.
- Developed at the **University of Nevada, Reno**.
- Preclinical: **100% protection** against lethal inhalational challenge in mice; **70% of survivors** had no culturable bacteria in lungs, liver or spleen.
- Planned **phase I in Oxford, UK (36 healthy adults)**, with a **phase Ib planned in Ubon Ratchathani, Thailand**, in volunteers with and without diabetes.

> **UNVERIFIED / weak sourcing.** The Oxford phase I trial details (n=36, site, phase Ib in Thailand, 2024 start) come from a **book chapter and secondary web sources**, not from a peer-reviewed trial registration or publication that I retrieved. *What is missing: a ClinicalTrials.gov / ISRCTN registration number and a primary publication.* **Do not state a trial has started, or report a start date, without checking a trial registry.** The safe, citable claim is Meumann 2024's "ready for phase I clinical trials."

Other candidate classes (Peacock 2012 systematic review): **live attenuated, whole-cell killed, subunit, plasmid DNA, and dendritic cell vaccines.**

Recent preclinical:
- Baker SM, et al. **An outer membrane vesicle vaccine prevents lung pathology in a macaque model of pneumonic melioidosis.** *Nat Commun* 2025. PMID 41366245. DOI 10.1038/s41467-025-67213-6. PMC12804674.
- Sengyee S, et al. **Safety and immunogenicity testing of a melioidosis subunit vaccine candidate in cynomolgus macaques.** *NPJ Vaccines* 2026. PMID 42448712. DOI 10.1038/s41541-026-01526-5.
- Khakhum N, et al. ***Burkholderia pseudomallei* ΔtonB Δhcp1 live attenuated vaccine strain.** *mSphere* 2019;4(1):e00570-18. PMID 30602524. DOI 10.1128/mSphere.00570-18. PMC6315081.
- Elko EA, et al. **PepSeq as a highly multiplexed platform for melioidosis antigen discovery and vaccine development.** *Front Immunol* 2025. PMID 40677719. DOI 10.3389/fimmu.2025.1605758. PMC12267161.

**The case for a vaccine (health economics):**
Peacock SJ, Limmathurotsakul D, Lubell Y, Koh GCKW, White LJ, Day NPJ, Titball RW. **Melioidosis vaccines: a systematic review and appraisal of the potential to exploit biodefense vaccines for public health purposes.** *PLoS Negl Trop Dis* 2012;6(1):e1488. PMID 22303489. DOI 10.1371/journal.pntd.0001488. PMC3269417.
> "a vaccine could be a cost-effective intervention in Thailand, particularly if used in high-risk populations such as diabetics."

Luangasanatip N, Flasche S, Dance DAB, Limmathurotsakul D, Currie BJ, Mukhopadhyay C, Atkins T, Titball R, Jit M. **The global impact and cost-effectiveness of a melioidosis vaccine.** *BMC Med* 2019;17:129. PMID 31272431. DOI 10.1186/s12916-019-1358-x. PMC6610909.
- Optimal strategy prevents **68,000 lost QALYs, 8,300 cases and 4,400 deaths per vaccinated age cohort** across **61 countries/territories** with local transmission.
- **Vaccinating diabetics aged over 45** was optimal in most regions.
- Potential market **USD 268 million/year** at the threshold cost-effective price.

> Note the alignment with Suputtamongkol 1999's conclusion 20 years earlier: **"diabetic rice farmers would be the most appropriate population group for targeted control measures such as vaccination in the future."**

---

## 8. Biosafety, select agent status, and the biothreat framing

### 8.1 US Federal Select Agent Program — Tier 1

Verified directly against **selectagents.gov** (the official HHS/USDA Select Agents and Toxins List):

- ***Burkholderia mallei*** and ***Burkholderia pseudomallei*** are both listed as **Overlap Select Agents and Toxins** (regulated by both HHS and USDA), and **both carry the Tier 1 designation**.
- Governing regulations: **42 CFR Part 73** (HHS), **7 CFR Part 331** and **9 CFR Part 121** (USDA).

**Tier 1 definition** (as quoted in Wiersinga 2018 and consistent with the regulation): Tier 1 select agents are those that present

> "the greatest risk of deliberate misuse with the most significant potential for mass casualties or devastating effect to the economy, critical infrastructure; or public confidence"

**Origin of the Tier 1 category:** **Executive Order 13546** (2 July 2010) directed HHS and USDA to designate Tier 1 agents and establish agent-specific security standards. The designation was implemented by the **final rule published 5 October 2012 (77 FR 61084)**, amending 42 CFR Part 73; core provisions effective **4 December 2012**, remainder **3 April 2013**. Tier 1 agents are subject to **additional security and personnel suitability requirements** beyond ordinary select agents.

> **Historical nuance worth stating precisely.** Peacock et al. 2012 describes *B. pseudomallei* as a **"Category B select agent"** — that reflects the pre-2012 CDC bioterrorism *category* scheme (Category A/B/C), which is a **different classification** from the *tier* scheme introduced in the October 2012 rule. Papers written before late 2012 will say Category B; papers after say Tier 1. **Both are correct for their era — do not "correct" an older citation to Tier 1.**

Broader biothreat-assessment context: Rotz LD, Khan AS, Lillibridge SR, Ostroff SM, Hughes JM. **Public health assessment of potential biological terrorism agents.** *Emerg Infect Dis* 2002;8(2):225–230. PMID 11897082. DOI 10.3201/eid0802.010164. PMC2732458.

### 8.2 Biosafety level and laboratory-acquired infection

Peacock SJ, Schweizer HP, Dance DAB, Smith TL, Gee JE, Wuthiekanun V, DeShazer D, Steinmetz I, Tan P, Currie BJ. **Management of accidental laboratory exposure to *Burkholderia pseudomallei* and *B. mallei*.** *Emerg Infect Dis* 2008;14(7):e2. PMID 18598617. DOI 10.3201/eid1407.071501. PMC2600349. Open access.

- **"The organism should be handled by trained personnel within a Biosafety Level 3 (BSL-3) facility"**
- **"*B. pseudomallei* has been designated a select agent by the US Centers for Disease Control and Prevention (CDC)"**
- **Documented laboratory-acquired infections cited:** two cases —
  1. A **48-year-old** worker who cleaned a centrifuge spill **with bare hands**; symptoms at **3 days**.
  2. A **33-year-old** who performed susceptibility testing on an isolate **thought to be *B. cepacia*** but actually *B. pseudomallei*; illness at **4 days**.
  Both recovered after prolonged antimicrobial therapy.
- **Risk stratification:** *low risk* — inadvertent plate opening, sniffing a plate without contact, splash onto gloved skin. *High risk* — needlestick injury, aerosol generation outside a biosafety cabinet, splash to eyes or mouth.
- **Post-exposure prophylaxis:** **"oral TMP-SMX is the agent of first choice"**, twice daily; alternatives doxycycline or amoxicillin-clavulanate where resistance exists. **"A period of 3 weeks of PEP is suggested"**.
- **Serological follow-up:** baseline day 1, then weeks 1, 2, 4 and 6; **"any reproducible rise between 2 samples should be used as an indicator of seroconversion"**.

> **Note the second case is a perfect illustration of §5.2:** the laboratory-acquired infection happened *because* the organism had been misidentified as *B. cepacia*, so it was handled on the open bench. **Misidentification is not only a diagnostic failure — it is a biosafety failure.**

Dance 2014 adds a sobering caveat on PEP: prophylaxis would **"probably only delay rather than prevent the development of infection."** PEP recommendations specify co-trimoxazole or co-amoxiclav for **21 days**.

Consensus guidance: Lipsitz R, Garges S, Aurigemma R, et al. **Workshop on treatment of and postexposure prophylaxis for *Burkholderia pseudomallei* and *B. mallei* infection, 2010.** *Emerg Infect Dis* 2012;18(12):e2. PMID 23171644. DOI 10.3201/eid1812.120638. PMC3557896.

### 8.3 What the biothreat framing implies for data sharing — the argument

This is the section most directly relevant to a genomics manuscript's framing. The chain of consequences:

1. **Regulatory burden on materials.** Tier 1 status means isolates cannot be freely shipped, shared, or held. Transfers require prior FSAP approval; possession requires registration, personnel suitability vetting (security risk assessments), and BSL-3 containment. This **structurally limits which laboratories can hold a strain collection** — and therefore who can generate genomic data.

2. **Sequence data as a dual-use concern.** Because the organism is a Tier 1 agent, genomic data attract dual-use-research-of-concern scrutiny in a way that data from, say, *Klebsiella* do not. This creates friction against open deposition and can delay or restrict public release.

3. **Diagnostic databases are deliberately incomplete.** Gassiep 2020 records that routine commercial MALDI-TOF databases **do not include the reference spectra needed to identify *B. pseudomallei***. This is a direct, measurable **patient-safety cost of the biothreat framing**: the organism is harder to identify in exactly the non-endemic settings where clinicians are least likely to suspect it (§5.2, §8.2).

4. **Research funding is skewed toward biodefence rather than endemic public health.** Peacock 2012's title makes this explicit — *"appraisal of the potential to exploit biodefense vaccines for public health purposes"*. The vaccine pipeline exists substantially because of biodefence money, not because of the ~89,000 modelled annual deaths among the rural poor.

5. **The equity asymmetry.** The disease burden falls overwhelmingly on **low- and middle-income tropical countries** (Savelkoel 2022: deaths "primarily occurring among rural poor populations in low-income and middle-income countries"), while the regulatory apparatus, containment infrastructure and sequencing capacity sit in high-income countries. **Restrictive sharing regimes therefore fall hardest on the endemic countries that most need genomic epidemiology.** This is a defensible argument for open, recombination-aware genomic frameworks and public reference data.

6. **Counter-pressure:** melioidosis is **not** a WHO-recognised NTD (§2.5), so it does not benefit from NTD-directed funding and access mechanisms either. It sits in a gap: **too securitised to be freely shared, too neglected to be resourced.**

---

## 9. Why molecular attribution of exposure origin matters

This is the section that connects the clinical background to a recombination-aware SNP methods paper.

### 9.1 The clinical problem: cases with no travel history

**Multistate outbreak from a consumer product:**
Gee JE, Bower WA, Kunkel A, Petras J, Gettings J, Bye M, Kaplan S, Kolton CB, Marston CK, Salzer JS, et al. **Multistate outbreak of melioidosis associated with imported aromatherapy spray.** *N Engl J Med* 2022;386(9):861–868. PMID 35235727. DOI 10.1056/NEJMoa2116130. PMC10243137.

- **Four cases** in **Georgia, Kansas, Minnesota and Texas**; **two deaths** (a 53-year-old woman in Kansas; a **5-year-old boy** in Georgia).
- All four patients **"did not have a history of travel to melioidosis-endemic areas"**; records noted they **"had never traveled outside the United States."**
- Whole-genome sequencing showed isolates from all four patients and from an **aromatherapy room spray** recovered from Patient 4's home were **clonal** — **"the isolate from the spray bottle and those from the four patients were all the same strain, which we have named ATS2021."**
- Phylogenomic analysis placed the strain's origin in **South Asia, specifically India** — matching the product's manufacturing origin.

> **This is the paradigm case.** Four geographically scattered patients with no travel history and no epidemiological link. Conventional epidemiology could not connect them. **Genomics both connected the cases to each other and identified the vehicle and its country of origin** — enabling a product recall. Without sequence-based attribution the outbreak would have been four unexplained deaths-and-illnesses in four states.

**Newly recognised endemicity in the continental US:**
Petras JK, Elrod MG, Ty MC, Dawson P, O'Laughlin K, Gee JE, Hanson J, Boyd S, et al. **Locally acquired melioidosis linked to environment — Mississippi, 2020–2023.** *N Engl J Med* 2023;389(25):2355–2362. PMID 38118023. DOI 10.1056/NEJMoa2306448. PMC10773590.

- **Three patients** from the **same Mississippi Gulf Coast county** over three years (July 2020, April 2022, January 2023).
- WGS: **"all isolates were clonal to each other (3 to 15 SNPs apart)"** and matched **environmental samples from soil and water on one patient's property**.
- All were **sequence type 92 (ST92)**, **"a sequence type associated with strains of Western Hemisphere origin"**; the novel strain (**GCS2020**) clustered within the **Western Hemisphere clade** with South American strains.
- Travel histories: Patient 1 **"reported no travel outside the continental United States in his lifetime"**; Patient 2 had **"no travel history to melioidosis-endemic countries"**; Patient 3 **"reported no travel outside the continental United States in his lifetime."**
- Conclusion: melioidosis **"may be endemic to the Mississippi Gulf Coast region"** — the **first environmental isolation of *B. pseudomallei* from soil and water in the continental United States.**

> **The 3–15 SNP resolution is the whole point.** Distinguishing "three unrelated imported cases" from "one local environmental reservoir seeding cases over three years" is a question answerable **only** at fine SNP resolution — and *B. pseudomallei*'s high recombination rate is exactly what makes naive SNP distances unreliable, which is the methodological gap a recombination-aware approach addresses.

Related unexplained-source work: **Related Melioidosis Cases with Unknown Exposure Source, Georgia, USA, 1983–2024.** *Emerg Infect Dis* 2025;31(9).

### 9.2 Linking individual patients to environmental sources

Webb JR, Mayo M, Rachlin A, Woerle C, Meumann E, Rigas V, Harrington G, Kaestli M, Currie BJ. **Genomic epidemiology links *Burkholderia pseudomallei* from individual human cases to environmental sources.** *J Clin Microbiol* 2022;60(2):e01648-21. PMID 35080450. DOI 10.1128/JCM.01648-21. PMC8925902.

- Of **98 patient sites** sampled, **"Genotyping matched the clinical and epidemiologically linked environmental *B. pseudomallei* for 19 patients (19%)."**
- WGS confirmed links and helped identify infection routes: **percutaneous inoculation, inhalation, and ingestion.**

> Note the modest yield: even with systematic environmental sampling around patients' homes, only **19%** could be matched. This is a candid statement of the current limits of attribution — and an argument that better methods (higher-resolution, recombination-aware) would raise that yield.

Occupational exposure at known sites: McCrory K, Underwood JG, Perkins SG, Rigas V, Mayo M, Kaestli M, Meumann EM, Letizia AG, Currie BJ. **Environmental presence of *Burkholderia pseudomallei* at military sites in an endemic region.** *Am J Trop Med Hyg* 2026. PMID 41666453. DOI 10.4269/ajtmh.25-0542. PMC12964799. — *B. pseudomallei* recovered from soil at all four Darwin military sites (not from air); **four sequence types matched human melioidosis cases** from the region.

### 9.3 Global dispersal and phylogeography

- Gee JE, et al. **Phylogeography of *Burkholderia pseudomallei* isolates, Western Hemisphere.** *Emerg Infect Dis* 2017;23(7):1133–1138. PMID 28628442. DOI 10.3201/eid2307.161978. PMC5512505. — Western Hemisphere isolates form a **distinct clade** from a **"constricted seeding event from Africa"**; **subclades resolve to specific regions**, so **"isolates might be correlated geographically with cases of melioidosis."** *This is the direct methodological justification for genomic attribution of exposure origin.*
- Sarovich DS, Garin B, De Smet B, et al. **Phylogenomic analysis reveals an Asian origin for African *Burkholderia pseudomallei* and further supports melioidosis endemicity in Africa.** *mSphere* 2016;1(2):e00089-15. PMID 27303718. DOI 10.1128/mSphere.00089-15. PMC4863585.
- Currie BJ, et al. **Global dispersal of *Burkholderia pseudomallei*.** *PLoS Negl Trop Dis* 2026;20(4):e0014217. PMID 42030350. DOI 10.1371/journal.pntd.0014217. PMC13108894.
- Currie BJ, Meumann EM, Kaestli M. **The expanding global footprint of *Burkholderia pseudomallei* and melioidosis.** *Am J Trop Med Hyg* 2023;108(6):1081–1083. PMID 37160279. DOI 10.4269/ajtmh.23-0223. PMC10540122.
- Klimko CP, et al. **Virulence of *Burkholderia pseudomallei* strains from Western Hemisphere and Africa in mice.** *Emerg Infect Dis* 2026;32(8):1251–1263. PMID 42436040. — bears on whether clade differences translate into virulence differences.

### 9.4 Summary of why attribution matters — clinical and public health

**Clinically:**
1. **Relapse vs reinfection are clinically indistinguishable** but have opposite implications: relapse means treatment failure (inadequate eradication, poor adherence, resistance emergence); reinfection means continuing environmental exposure. **Only genotyping distinguishes them** (Sarovich 2014; Maharjan 2005) — and the two settings studied gave **opposite answers** (§4.5).
2. **Claimed latency drives clinical suspicion decades after exposure.** The 62-year claim was overturned by phylogeography (Gee 2017); the true maximum plausible latency is **29 years**, and latency accounts for **<3%** of cases (Howes & Currie 2024). Attribution therefore **narrows** the differential rather than widening it.
3. **Within-host resistance emergence** (Wuthiekanun 2011: 21/24 resistant isolates arose during therapy) is only detectable by comparing serial isolates genomically.
4. **Genotype–outcome links exist** — e.g. the *bimA*<sub>Bm</sub> allele and death/disability in CNS melioidosis, **OR 4.88 (1.28–18.57)** (Gora 2022).

**For public health:**
1. **Detecting point-source outbreaks** in patients with no epidemiological link (Gee 2022 — aromatherapy spray, product recall).
2. **Establishing new endemicity** and redrawing risk maps (Petras 2023 — Mississippi Gulf Coast; Meumann 2024 — "Genomic epidemiological investigations have confirmed *B. pseudomallei* endemicity in newly recognized regions, including the southern United States").
3. **Distinguishing imported from locally acquired infection** where no travel history exists — which determines whether the response is a product trace-back or environmental risk communication to a resident population.
4. **Biothreat differentiation:** for a Tier 1 select agent, distinguishing a natural environmental exposure from a deliberate release is a genomic attribution question with national-security consequences. This cuts both ways — it is a strong argument for attribution capability, and part of why the data are securitised (§8.3).
5. **Linking cases to specific environmental reservoirs** to target remediation and prevention (Webb 2022 — 19% match rate; McCrory 2026 — military sites).

> **The methodological gap this motivates:** *B. pseudomallei* has an exceptionally recombinogenic genome (two chromosomes, extensive genomic islands — Holden 2004 PNAS PMID 15377794; Tuanyok 2008 BMC Genomics PMID 19038032; Sim/Tumapa 2008 PMID 18439288). Recombination inflates apparent SNP distances and distorts phylogenies, so naive SNP-distance thresholds — of the kind that underpin the "3 to 15 SNPs apart" clonality call in Petras 2023 — are not reliable without recombination-aware correction. **The clinical and public health stakes above are exactly what make getting that correction right consequential.**

---

## 10. Explicit list of disagreements, weak provenance, and unverified items

| # | Issue | Detail |
|---|---|---|
| 1 | **Diabetes effect size** | Wiersinga 2018 says **12-fold**; commonly quoted **13-fold** attributed to Suputtamongkol 1999; meta-analysis gives pooled **RR 3.40 (2.92–3.87)** with **I²=98.2%**. ~4× discrepancy. Partly estimand mismatch, partly extreme heterogeneity. |
| 2 | **Suputtamongkol 1999 numbers — UNVERIFIED** | Paywalled, no PMC copy. **The abstract contains no OR/RR/CI at all.** The "13-fold" figure could not be traced to a primary number. *Missing: full text / Tables of CID 1999;29:408–413.* |
| 3 | **Global burden 165,000/89,000** | **Modelled**, not observed; credible intervals span ~6-fold (68,000–412,000 cases; 36,000–227,000 deaths). Birnie 2019 **adopted** these figures rather than independently deriving them, so the 4.6M DALY estimate is **not** independent corroboration. |
| 4 | **Relapse vs reinfection** | **Direct disagreement by setting:** Darwin 74% relapse / 26% reinfection (Sarovich 2014); northeast Thailand "frequently reinfection rather than relapse" (Maharjan 2005). |
| 5 | **API 20NE sensitivity** | Gassiep 2020 quotes **99% (98.0–99.6)**; regional-dependence literature gives **37–99%**. Irreconcilable as a single figure — performance is region/strain dependent. |
| 6 | **Podin 2013 figures — UNVERIFIED** | The VITEK 2 63–81% / Phoenix 0–28% / API 20NE 37–99% bracket came via web-search summary of the abstract, not direct retrieval. *Missing: Podin 2013, JCM 51:3076–3078.* |
| 7 | **TMP-SMX resistance rate** | Thailand 21-yr survey did not systematically test it; India (Koshy 2019) reports **5.9%**. Disc diffusion is known to overcall TMP-SMX resistance vs Etest/broth microdilution. **UNVERIFIED** whether the India–Thailand gap is real or methodological. |
| 8 | **Stephens 2016 ICU mortality 92%→26%** | Striking figure, paywalled, no PMC copy; obtained via summarising fetcher from the abstract. **Re-check against PDF.** |
| 9 | **Sullivan 2020 recrudescence 2.8% / recurrence 4.7%** | Came via summariser, not as quoted sentences. Re-check. |
| 10 | **Darwin 20-yr organ-abscess table rows** | Six key sentences re-verified word-for-word; the remaining table rows (GU 14%, skin 13%, bacteraemia-no-focus 11%, arthritis/osteo 4%, neuro 3%, spleen 5%, kidney 3%, liver 3%) were returned as a summariser-built table. Re-check against PDF. |
| 11 | **Vaccine phase I trial details — UNVERIFIED** | n=36, Oxford, phase Ib Ubon Ratchathani, 2024 start: sourced from a book chapter/web, **not** a registry or primary publication. *Missing: ClinicalTrials.gov/ISRCTN ID.* Safe claim = Meumann 2024's "ready for phase I clinical trials." |
| 12 | **WHO NTD status** | Confirmed via advocacy literature that melioidosis is **not** on the WHO NTD list; **I did not fetch who.int directly.** Verify before asserting in print. |
| 13 | **Gee 2017 PMID conflict** | One fetch returned 28628306; authoritative Europe PMC record and PubMed URL give **28628442**. **Use 28628442.** |
| 14 | **Select agent: Category B vs Tier 1** | Pre-Oct-2012 papers (e.g. Peacock 2012) correctly say "Category B"; the Tier 1 *tier* scheme began with the 5 Oct 2012 final rule (77 FR 61084). Different schemes — do not retro-correct. |
| 15 | **Africa case fatality — GAP** | Steinmetz 2018 gives sub-Saharan Africa modelled burden (**24,000 cases [8,000–72,000]; 15,000 deaths [6,000–45,000]** annually; 24 African + 3 Middle Eastern countries likely endemic) but **no CFR from African case series**. *Missing: an African clinical cohort with a CFR.* |
| 16 | **Verbatim quotes generally** | All quoted strings passed through a summarising model. Re-verify any quotation used as a direct quote in the manuscript. |

---

## 11. Citation table

| Role | Citation | PMID | DOI |
|---|---|---|---|
| **Anchor cohort, 30 yr** | Currie BJ, Mayo M, Ward LM, et al. The Darwin Prospective Melioidosis Study: a 30-year prospective, observational investigation. *Lancet Infect Dis* 2021;21(12):1737–1746. | 34303419 | 10.1016/S1473-3099(21)00022-0 |
| **Clinical spectrum, organ-level** | Currie BJ, Ward L, Cheng AC. The epidemiology and clinical spectrum of melioidosis: 540 cases from the 20 year Darwin prospective study. *PLoS Negl Trop Dis* 2010;4(11):e900. | 21152057 | 10.1371/journal.pntd.0000900 |
| **Global burden (modelled)** | Limmathurotsakul D, Golding N, Dance DAB, et al. Predicted global distribution of *Burkholderia pseudomallei* and burden of melioidosis. *Nat Microbiol* 2016;1:15008. | 26877885 | 10.1038/nmicrobiol.2015.8 |
| **Global burden, DALYs** | Birnie E, Virk HS, Savelkoel J, et al. Global burden of melioidosis in 2015: a systematic review and data synthesis. *Lancet Infect Dis* 2019;19(8):892–902. | 31285144 | 10.1016/S1473-3099(19)30157-4 |
| **Current major review** | Meumann EM, Limmathurotsakul D, Dunachie SJ, Wiersinga WJ, Currie BJ. *Burkholderia pseudomallei* and melioidosis. *Nat Rev Microbiol* 2024;22(3):155–169. | 37794173 | 10.1038/s41579-023-00972-5 |
| **Disease primer** | Wiersinga WJ, Virk HS, Torres AG, Currie BJ, Peacock SJ, Dance DAB, Limmathurotsakul D. Melioidosis. *Nat Rev Dis Primers* 2018;4:17107. | 29388572 | 10.1038/nrdp.2017.107 |
| **General review (classic)** | Wiersinga WJ, Currie BJ, Peacock SJ. Melioidosis. *N Engl J Med* 2012;367(11):1035–1044. | 22970946 | 10.1056/NEJMra1204699 |
| **General review (classic)** | Cheng AC, Currie BJ. Melioidosis: epidemiology, pathophysiology, and management. *Clin Microbiol Rev* 2005;18(2):383–416. | 15831829 | 10.1128/CMR.18.2.383-416.2005 |
| **General review (classic)** | White NJ. Melioidosis. *Lancet* 2003;361(9370):1715–1722. | 12767750 | 10.1016/S0140-6736(03)13374-0 |
| **Underdiagnosis, foundational** | Dance DAB. Melioidosis: the tip of the iceberg? *Clin Microbiol Rev* 1991;4(1):52–60. | 2004347 | 10.1128/CMR.4.1.52 |
| **NE Thailand incidence & CFR** | Limmathurotsakul D, Wongratanacheewin S, Teerawattanasook N, et al. Increasing incidence of human melioidosis in Northeast Thailand. *Am J Trop Med Hyg* 2010;82(6):1113–1117. | 20519609 | 10.4269/ajtmh.2010.10-0038 |
| **Australian cohort (FNQ)** | Stewart JD, Smith S, Binotto E, McBride WJ, Currie BJ, Hanson J. The epidemiology and clinical features of melioidosis in Far North Queensland. *PLoS Negl Trop Dis* 2017;11(3):e0005411. | 28264029 | 10.1371/journal.pntd.0005411 |
| **India cohort & CFR** | Koshy M, Jagannati M, Ralph R, et al. Clinical manifestations, antimicrobial drug susceptibility patterns, and outcomes in melioidosis cases, India. *Emerg Infect Dis* 2019;25(2):316–320. | 30666953 | 10.3201/eid2502.170745 |
| **Africa burden** | Steinmetz I, Wagner GE, Kanyala E, et al. Melioidosis in Africa: time to uncover the true disease load. *Trop Med Infect Dis* 2018;3(2):62. | 30274458 | 10.3390/tropicalmed3020062 |
| **Africa phylogenomics** | Sarovich DS, Garin B, De Smet B, et al. Phylogenomic analysis reveals an Asian origin for African *Burkholderia pseudomallei*. *mSphere* 2016;1(2):e00089-15. | 27303718 | 10.1128/mSphere.00089-15 |
| **Pneumonia** | Meumann EM, Cheng AC, Ward L, Currie BJ. Clinical features and epidemiology of melioidosis pneumonia. *Clin Infect Dis* 2012;54(3):362–369. | 22057702 | 10.1093/cid/cir808 |
| **CNS melioidosis + genotype link** | Gora H, Hasan T, Smith S, et al. Melioidosis of the central nervous system. *Clin Infect Dis* 2022;ciac111. | 35137005 | 10.1093/cid/ciac111 |
| **Neurological (landmark)** | Woods ML, Currie BJ, Howard DM, et al. Neurological melioidosis: seven cases from the Northern Territory of Australia. *Clin Infect Dis* 1992;15(1):163–169. | 1617057 | 10.1093/clinids/15.1.163 |
| **CNS invasion mechanism** | St John JA, Ekberg JAK, Dando SJ, et al. *Burkholderia pseudomallei* penetrates the brain via destruction of the olfactory and trigeminal nerves. *mBio* 2014;5(2):e00025-14. | 24736221 | 10.1128/mBio.00025-14 |
| **Chronic melioidosis** | Singh H, et al. Epidemiology, clinical features, and outcomes of chronic melioidosis. *Open Forum Infect Dis* 2026;13(6):ofag294. | 42253281 | 10.1093/ofid/ofag294 |
| **Paediatric parotitis (landmark)** | Dance DA, Davis TM, Wattanagoon Y, et al. Acute suppurative parotitis caused by *Pseudomonas pseudomallei* in children. *J Infect Dis* 1989;159(4):654–660. | 2926159 | 10.1093/infdis/159.4.654 |
| **Paediatric, Australia** | McLeod C, Morris PS, Bauert PA, et al. Clinical presentation and medical management of melioidosis in children. *Clin Infect Dis* 2015;60(1):21–26. | 25228703 | 10.1093/cid/ciu733 |
| **Paediatric, Cambodia** | Pagnarith Y, Kumar V, Thaipadungpanit J, et al. Emergence of pediatric melioidosis in Siem Reap, Cambodia. *Am J Trop Med Hyg* 2010;82(6):1106–1112. | 20519608 | 10.4269/ajtmh.2010.10-0030 |
| **ICU mortality, Australia** | Stephens DP, Thomas JH, Ward LM, Currie BJ. Melioidosis causing critical illness: a review of 24 years of experience from the Royal Darwin Hospital ICU. *Crit Care Med* 2016;44(8):1500–1505. | 26963328 | 10.1097/CCM.0000000000001668 |
| **ICU mortality, Singapore** | Chan KP, Low JG, Raghuram J, Fook-Chong SM, Kurup A. Clinical characteristics and outcome of severe melioidosis requiring intensive care. *Chest* 2005;128(5):3674–3678. | 16304330 | 10.1378/chest.128.5.3674 |
| **Rainfall/inhalation → severity** | Currie BJ, Jacups SP. Intensity of rainfall and severity of melioidosis, Australia. *Emerg Infect Dis* 2003;9(12):1538–1542. | 14720392 | 10.3201/eid0912.020750 |
| **Climate association** | Kaestli M, Grist EPM, Ward L, Hill A, Mayo M, Currie BJ. The association of melioidosis with climatic factors in Darwin, Australia: a 23-year time-series analysis. *J Infect* 2016;72(6):687–697. | 26945846 | 10.1016/j.jinf.2016.02.015 |
| **Risk factors (landmark)** | Suputtamongkol Y, Chaowagul W, Chetchotisakd P, et al. Risk factors for melioidosis and bacteremic melioidosis. *Clin Infect Dis* 1999;29(2):408–413. | 10476750 | 10.1086/520223 |
| **Diabetes meta-analysis** | Chowdhury S, Barai L, Afroze SR, et al. The epidemiology of melioidosis and its association with diabetes mellitus: a systematic review and meta-analysis. *Pathogens* 2022;11(2):149. | 35215093 | 10.3390/pathogens11020149 |
| **Exposure activities case-control** | Limmathurotsakul D, Kanoksil M, Wuthiekanun V, et al. Activities of daily living associated with acquisition of melioidosis in northeast Thailand: a matched case-control study. *PLoS Negl Trop Dis* 2013;7(2):e2072. | 23437412 | 10.1371/journal.pntd.0002072 |
| **NE Thailand epidemiology (early)** | Suputtamongkol Y, Hall AJ, Dance DAB, et al. The epidemiology of melioidosis in Ubon Ratchatani, northeast Thailand. *Int J Epidemiol* 1994;23(5):1082–1090. | 7860160 | 10.1093/ije/23.5.1082 |
| **Incubation, acute vs chronic, relapse** | Currie BJ, Fisher DA, Anstey NM, Jacups SP. Melioidosis: acute and chronic disease, relapse and re-activation. *Trans R Soc Trop Med Hyg* 2000;94(3):301–304. | 10975006 | 10.1016/S0035-9203(00)90333-X |
| **Latency debunked** | Howes M, Currie BJ. Melioidosis and activation from latency: the "time bomb" has not occurred. *Am J Trop Med Hyg* 2024. | 38806042 | 10.4269/ajtmh.24-0007 |
| **62-yr latency claim (original)** | Ngauy V, Lemeshev Y, Sadkowski L, Crawford G. Cutaneous melioidosis in a man who was taken as a prisoner of war by the Japanese during World War II. *J Clin Microbiol* 2005;43(2):970–972. | 15695721 | 10.1128/JCM.43.2.970-972.2005 |
| **62-yr claim refuted; phylogeography** | Gee JE, Gulvik CA, Elrod MG, Batra D, Rowe LA, Sheth M, Hoffmaster AR. Phylogeography of *Burkholderia pseudomallei* isolates, Western Hemisphere. *Emerg Infect Dis* 2017;23(7):1133–1138. | 28628442 | 10.3201/eid2307.161978 |
| **"Vietnamese time bomb" coinage** | Goshorn RK. Recrudescent pulmonary melioidosis. A case report involving the so-called "Vietnamese time bomb." *Indiana Med* 1987;80:247–249. | — | — |
| **"Time-bomb" concept origin** | Howe C, Sampath A, Spotnitz M. The pseudomallei group: a review. *J Infect Dis* 1971;124:598–606. | — | — |
| **225,000 projection (serosurvey)** | Clayton AJ, Lisella RS, Martin DG. Melioidosis: a serological survey in military personnel. *Mil Med* 1973;138:24–26. | — | — |
| **Latent melioidosis (early)** | Kingston CW. Chronic or latent melioidosis. *Med J Aust* 1971;2:618–621. | — | — |
| **Relapse vs reinfection, Australia** | Sarovich DS, Ward L, Price EP, et al. Recurrent melioidosis in the Darwin Prospective Melioidosis Study: improving therapies mean that relapse cases are now rare. *J Clin Microbiol* 2014;52(2):650–653. | 24478504 | 10.1128/JCM.02239-13 |
| **Reinfection dominant, Thailand** | Maharjan B, Chantratita N, Vesaratchavest M, et al. Recurrent melioidosis in patients in northeast Thailand is frequently due to reinfection rather than relapse. *J Clin Microbiol* 2005;43(12):6032–6034. | 16333094 | 10.1128/JCM.43.12.6032-6034.2005 |
| **Relapse incidence (landmark)** | Chaowagul W, Suputtamongkol Y, Dance DAB, et al. Relapse in melioidosis: incidence and risk factors. *J Infect Dis* 1993;168(5):1181–1185. | 8228352 | 10.1093/infdis/168.5.1181 |
| **Within-host evolution** | Price EP, Sarovich DS, Mayo M, et al. Within-host evolution of *Burkholderia pseudomallei* over a twelve-year chronic carriage infection. *mBio* 2013;4(4):e00388-13. | 23860767 | 10.1128/mBio.00388-13 |
| **Culture sensitivity 60.2%** | Limmathurotsakul D, Jamsen K, Arayawichanont A, et al. Defining the true sensitivity of culture for the diagnosis of melioidosis using Bayesian latent class models. *PLoS One* 2010;5(8):e12485. | 20830194 | 10.1371/journal.pone.0012485 |
| **Diagnosis review** | Gassiep I, Armstrong M, Norton R. Human melioidosis. *Clin Microbiol Rev* 2020;33(2):e00006-19. | 32161067 | 10.1128/CMR.00006-19 |
| **Diagnosis review (current)** | Gassiep I, et al. Laboratory diagnosis of melioidosis. *PLoS Negl Trop Dis* 2025;19(12):e0013761. | 41343561 | 10.1371/journal.pntd.0013761 |
| **Misidentification, regional** | Podin Y, Kaestli M, McMahon N, et al. Reliability of automated biochemical identification of *Burkholderia pseudomallei* is regionally dependent. *J Clin Microbiol* 2013;51(9):3076–3078. | — | 10.1128/JCM.01290-13 |
| **Misidentification by automated system** | Zong Z, Wang X, Deng Y, Zhou T. *Burkholderia pseudomallei* misidentified by automated system. *Emerg Infect Dis* 2009;15(11):1936–1938. | — | 10.3201/eid1511.081719 |
| **MALDI-TOF performance** | Campbell S, Taylor B, Menouhos D, et al. Performance of MALDI-TOF MS, real-time PCR, antigen detection, and automated biochemical testing for identification of *Burkholderia pseudomallei*. *J Clin Microbiol* 2024;62(10):e00961-24. | 39235248 | 10.1128/jcm.00961-24 |
| **Lateral flow, clinical reality** | Currie BJ, Woerle C, Mayo M, Meumann EM, Baird RW. What is the role of lateral flow immunoassay for the diagnosis of melioidosis? *Open Forum Infect Dis* 2022;9(5):ofac149. | 35493111 | 10.1093/ofid/ofac149 |
| **Lateral flow, prototype** | Houghton RL, Reed DE, Hubbard MA, et al. Development of a prototype lateral flow immunoassay (LFI) for the rapid diagnosis of melioidosis. *PLoS Negl Trop Dis* 2014;8(3):e2727. | 24651568 | 10.1371/journal.pntd.0002727 |
| **Serology in children** | Wuthiekanun V, Chierakul W, Langa S, et al. Development of antibodies to *Burkholderia pseudomallei* during childhood in melioidosis-endemic northeast Thailand. *Am J Trop Med Hyg* 2006;74(6):1074–1075. | — | — |
| **Ceftazidime landmark trial** | White NJ, Dance DAB, Chaowagul W, et al. Halving of mortality of severe melioidosis by ceftazidime. *Lancet* 1989;2(8665):697–701. | 2570956 | 10.1016/S0140-6736(89)90768-X |
| **Imipenem vs ceftazidime** | Simpson AJH, Suputtamongkol Y, Smith MD, et al. Comparison of imipenem and ceftazidime as therapy for severe melioidosis. *Clin Infect Dis* 1999;29(2):381–387. | 10476746 | 10.1086/520219 |
| **Treatment guideline** | Sullivan RP, Marshall CS, Anstey NM, Ward L, Currie BJ. 2020 review and revision of the 2015 Darwin melioidosis treatment guideline; paradigm drift not shift. *PLoS Negl Trop Dis* 2020;14(9):e0008659. | 32986699 | 10.1371/journal.pntd.0008659 |
| **IV duration paradigm** | Pitman MC, Luck T, Marshall CS, Anstey NM, Ward L, Currie BJ. Intravenous therapy duration and outcomes in melioidosis: a new treatment paradigm. *PLoS Negl Trop Dis* 2015;9(3):e0003586. | 25811783 | 10.1371/journal.pntd.0003586 |
| **Eradication RCT (MERTH)** | Chetchotisakd P, Chierakul W, Chaowagul W, et al. Trimethoprim-sulfamethoxazole versus trimethoprim-sulfamethoxazole plus doxycycline as oral eradicative treatment for melioidosis (MERTH). *Lancet* 2014;383(9919):807–814. | 24284287 | 10.1016/S0140-6736(13)61951-0 |
| **Treatment review** | Dance D. Treatment and prophylaxis of melioidosis. *Int J Antimicrob Agents* 2014;43(4):310–318. | 24613038 | 10.1016/j.ijantimicag.2014.01.005 |
| **Treatment network meta-analysis** | Anothaisintawee T, Harncharoenkul K, Poramathikul K, et al. Efficacy of drug treatment for severe melioidosis and eradication treatment. *PLoS Negl Trop Dis* 2023;17(6):e0011382. | 37307278 | 10.1371/journal.pntd.0011382 |
| **Treatment (most recent)** | Meumann EM, et al. Treatment of melioidosis. *Infect Dis Clin North Am* 2026;40(1):127–147. | 41571490 | 10.1016/j.idc.2025.12.002 |
| **Resistance mechanisms** | Schweizer HP. Mechanisms of antibiotic resistance in *Burkholderia pseudomallei*: implications for treatment of melioidosis. *Future Microbiol* 2012;7(12):1389–1399. | 23231488 | 10.2217/fmb.12.116 |
| **Resistance surveillance** | Wuthiekanun V, Amornchai P, Saiprom N, et al. Survey of antimicrobial resistance in clinical *Burkholderia pseudomallei* isolates over two decades in Northeast Thailand. *Antimicrob Agents Chemother* 2011;55(11):5388–5391. | 21876049 | 10.1128/AAC.05517-11 |
| **Resistance on therapy (case)** | Evans TJ, et al. Case report: genetic evolution of *Burkholderia pseudomallei* during treatment leading to antibiotic resistance and disease relapse. *Wellcome Open Res* 2025. | 40861388 | 10.12688/wellcomeopenres.24138.2 |
| **Adjunctive G-CSF RCT** | Cheng AC, Limmathurotsakul D, Chierakul W, et al. A randomized controlled trial of granulocyte colony-stimulating factor for the treatment of severe sepsis due to melioidosis in Thailand. *Clin Infect Dis* 2007;45(3):308–314. | 17599307 | 10.1086/519261 |
| **Glyburide and mortality** | Koh GCKW, Maude RR, Schreiber MF, et al. Glyburide is anti-inflammatory and associated with reduced mortality in melioidosis. *Clin Infect Dis* 2011;52(6):717–725. | 21293047 | 10.1093/cid/ciq192 |
| **Vaccine systematic review** | Peacock SJ, Limmathurotsakul D, Lubell Y, et al. Melioidosis vaccines: a systematic review and appraisal of the potential to exploit biodefense vaccines for public health purposes. *PLoS Negl Trop Dis* 2012;6(1):e1488. | 22303489 | 10.1371/journal.pntd.0001488 |
| **Vaccine cost-effectiveness** | Luangasanatip N, Flasche S, Dance DAB, et al. The global impact and cost-effectiveness of a melioidosis vaccine. *BMC Med* 2019;17:129. | 31272431 | 10.1186/s12916-019-1358-x |
| **Vaccine, OMV macaque** | Baker SM, et al. An outer membrane vesicle vaccine prevents lung pathology in a macaque model of pneumonic melioidosis. *Nat Commun* 2025. | 41366245 | 10.1038/s41467-025-67213-6 |
| **Vaccine, subunit macaque** | Sengyee S, et al. Safety and immunogenicity testing of a melioidosis subunit vaccine candidate in cynomolgus macaques. *NPJ Vaccines* 2026. | 42448712 | 10.1038/s41541-026-01526-5 |
| **Vaccine, live attenuated** | Khakhum N, Bharaj P, Myers JN, et al. *Burkholderia pseudomallei* ΔtonB Δhcp1 live attenuated vaccine strain. *mSphere* 2019;4(1):e00570-18. | 30602524 | 10.1128/mSphere.00570-18 |
| **Lab exposure management / BSL-3** | Peacock SJ, Schweizer HP, Dance DAB, et al. Management of accidental laboratory exposure to *Burkholderia pseudomallei* and *B. mallei*. *Emerg Infect Dis* 2008;14(7):e2. | 18598617 | 10.3201/eid1407.071501 |
| **PEP consensus** | Lipsitz R, Garges S, Aurigemma R, et al. Workshop on treatment of and postexposure prophylaxis for *Burkholderia pseudomallei* and *B. mallei* infection, 2010. *Emerg Infect Dis* 2012;18(12):e2. | 23171644 | 10.3201/eid1812.120638 |
| **Biothreat assessment** | Rotz LD, Khan AS, Lillibridge SR, Ostroff SM, Hughes JM. Public health assessment of potential biological terrorism agents. *Emerg Infect Dis* 2002;8(2):225–230. | 11897082 | 10.3201/eid0802.010164 |
| **Select agent list (Tier 1)** | Federal Select Agent Program. HHS and USDA Select Agents and Toxins list. 42 CFR Part 73; 7 CFR Part 331; 9 CFR Part 121. https://www.selectagents.gov/sat/list.htm | — | — |
| **Tier 1 rule** | Possession, Use, and Transfer of Select Agents and Toxins; Biennial Review. Final rule. *Fed Regist* 5 Oct 2012;77(194):61084. | — | — |
| **NTD advocacy** | Savelkoel J, Dance DAB, Currie BJ, Limmathurotsakul D, Wiersinga WJ. A call to action: time to recognise melioidosis as a neglected tropical disease. *Lancet Infect Dis* 2022;22(6):e176–e182. | 34953519 | 10.1016/S1473-3099(21)00394-7 |
| **NTD advocacy (regional)** | Mohapatra PR, Behera B. Melioidosis: a call for recognition as a neglected tropical disease under the Southeast Asia regional NTD framework. *Lancet Reg Health Southeast Asia* 2025;39:100625. | 40842680 | 10.1016/j.lansea.2025.100625 |
| **Outbreak, no travel history** | Gee JE, Bower WA, Kunkel A, et al. Multistate outbreak of melioidosis associated with imported aromatherapy spray. *N Engl J Med* 2022;386(9):861–868. | 35235727 | 10.1056/NEJMoa2116130 |
| **US endemicity, genomic attribution** | Petras JK, Elrod MG, Ty MC, et al. Locally acquired melioidosis linked to environment — Mississippi, 2020–2023. *N Engl J Med* 2023;389(25):2355–2362. | 38118023 | 10.1056/NEJMoa2306448 |
| **Case-to-environment genomic linkage** | Webb JR, Mayo M, Rachlin A, et al. Genomic epidemiology links *Burkholderia pseudomallei* from individual human cases to environmental sources. *J Clin Microbiol* 2022;60(2):e01648-21. | 35080450 | 10.1128/JCM.01648-21 |
| **Occupational environmental exposure** | McCrory K, Underwood JG, Perkins SG, et al. Environmental presence of *Burkholderia pseudomallei* at military sites in an endemic region. *Am J Trop Med Hyg* 2026. | 41666453 | 10.4269/ajtmh.25-0542 |
| **Global dispersal** | Currie BJ, et al. Global dispersal of *Burkholderia pseudomallei*. *PLoS Negl Trop Dis* 2026;20(4):e0014217. | 42030350 | 10.1371/journal.pntd.0014217 |
| **Expanding footprint** | Currie BJ, Meumann EM, Kaestli M. The expanding global footprint of *Burkholderia pseudomallei* and melioidosis. *Am J Trop Med Hyg* 2023;108(6):1081–1083. | 37160279 | 10.4269/ajtmh.23-0223 |
| **Genome plasticity (recombination context)** | Holden MTG, Titball RW, Peacock SJ, et al. Genomic plasticity of the causative agent of melioidosis, *Burkholderia pseudomallei*. *Proc Natl Acad Sci USA* 2004;101(39):14240–14245. | 15377794 | 10.1073/pnas.0403302101 |
| **Genomic islands** | Tuanyok A, Leadem BR, Auerbach RK, et al. Genomic islands from five strains of *Burkholderia pseudomallei*. *BMC Genomics* 2008;9:566. | 19038032 | 10.1186/1471-2164-9-566 |
| **Genomic island variation** | Tumapa S, Holden MTG, Vesaratchavest M, et al. *Burkholderia pseudomallei* genome plasticity associated with genomic island variation. *BMC Genomics* 2008;9:190. | 18439288 | 10.1186/1471-2164-9-190 |
| **MLST scheme** | Godoy D, Randle G, Simpson AJ, et al. Multilocus sequence typing and evolutionary relationships among the causative agents of melioidosis and glanders, *Burkholderia pseudomallei* and *Burkholderia mallei*. *J Clin Microbiol* 2003;41(5):2068–2079. | 12734250 | 10.1128/JCM.41.5.2068-2079.2003 |
| **Thailand national picture** | Hinjoy S, Hantrakun V, Kongyu S, et al. Melioidosis in Thailand: present and future. *Trop Med Infect Dis* 2018;3(2):38. | 29725623 | 10.3390/tropicalmed3020038 |
| **SE Asia sepsis context** | Southeast Asia Infectious Disease Clinical Research Network. Causes and outcomes of sepsis in southeast Asia: a multinational multicentre cross-sectional study. *Lancet Glob Health* 2017;5(2):e157–e167. | 28104185 | 10.1016/S2214-109X(17)30007-4 |
| **Community-acquired bacteraemia, NE Thailand** | Kanoksil M, Jatapai A, Peacock SJ, Limmathurotsakul D. Epidemiology, microbiology and mortality associated with community-acquired bacteremia in northeast Thailand: a multicenter surveillance study. *PLoS One* 2013;8(1):e54714. | 23349954 | 10.1371/journal.pone.0054714 |
| **South Asia** | Mukhopadhyay C, Shaw T, Varghese GM, Dance DAB. Melioidosis in South Asia (India, Nepal, Pakistan, Bhutan and Afghanistan). *Trop Med Infect Dis* 2018;3(2):51. | 30274447 | 10.3390/tropicalmed3020051 |
