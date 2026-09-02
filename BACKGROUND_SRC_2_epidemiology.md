# *Burkholderia pseudomallei* / Melioidosis — Epidemiology, Global Distribution, Environmental Ecology and Transmission

Raw literature research for the Background section of a recombination-aware SNP genomics manuscript.
Compiled 2 September 2026.

**How to read this document.** Every factual claim carries a citation keyed to the table at the end. Confidence is flagged inline:

- **[V]** = Verified. I retrieved the figure from the publisher's full text, the PMC full text, or the raw Europe PMC `abstractText` field, and the PMID/DOI were independently confirmed.
- **[S]** = Secondary/snippet. The figure came from a search summary or a summarised page fetch and the underlying number has *not* been read in the primary source. Re-check before it goes into a manuscript.
- **[UNVERIFIED]** = I could not confirm this at all. The gap is stated explicitly.

**Model output vs. observation.** Section 1 figures are *model outputs*, not case counts. This distinction is flagged throughout and is the single most important caveat in this topic area — the 165,000/89,000 numbers are routinely miscited as observed data.

---

## 0. Tooling caveat affecting this research

The PubMed MCP tools (`get_article_metadata`, and most `search_articles` calls) were blocked for the whole session by a safety classifier unrelated to the content of the queries; `Bash` was likewise blocked. Verification was therefore done through WebSearch, WebFetch of PMC full texts, and **the Europe PMC REST API** (`https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:<pmid>&resultType=core&format=json`), which returns authoritative PMID/DOI/abstract records.

**This mattered.** A WebFetch of the *Journal of Travel Medicine* page returned PMID `37040739` for the Norman & Chen travel review. Europe PMC shows PMID 37040739 is *"Miniature Linguistic Systems for Individuals With Autism Spectrum Disorder"* — an unrelated paper. The correct PMID is **36971472**. Treat any PMID not in the final citation table as unconfirmed.

---

## 1. Global burden modelling

### 1.1 The anchor paper — Limmathurotsakul et al. 2016

Limmathurotsakul D, Golding N, Dance DAB, Messina JP, Pigott DM, Moyes CL, Rolim DB, Bertherat E, Day NPJ, Peacock SJ, Hay SI. *Predicted global distribution of* Burkholderia pseudomallei *and burden of melioidosis.* **Nat Microbiol 2016;1(1):15008.** PMID 26877885; DOI 10.1038/nmicrobiol.2015.8. [C1]

**Headline estimates (all are MODEL OUTPUTS for the year 2015, not observed counts):** [V]

> "We estimate there to be 165,000 (95% credible interval 68,000–412,000) human melioidosis cases per year worldwide, of which 89,000 (36,000–227,000) die."

- Cases: **165,000/yr (95% CrI 68,000–412,000)** [V]
- Deaths: **89,000/yr (95% CrI 36,000–227,000)** [V]
- Population at risk: **~3 billion** people living in areas likely to contain *B. pseudomallei* [V]
- Implied incidence: **5.0 per 100,000 people at risk per year** [V]

Note the credible intervals are very wide — the upper bound on cases (412,000) is 6× the lower bound (68,000). Any manuscript sentence citing "165,000 cases" without the interval overstates the precision.

### 1.2 IMPORTANT CORRECTION — the "45 countries" figure

The brief for this research stated "the 45 countries where it is endemic but never reported." **That conflates two distinct numbers.** The paper's actual wording, verbatim from the full text: [V]

> "The list of priority countries includes 45 countries where melioidosis is known to be endemic but is underreported and a further 34 countries where melioidosis is probably endemic but has never been reported."

And from the abstract: [V]

> "Our estimates suggest that melioidosis is severely underreported in the 45 countries in which it is known to be endemic and that melioidosis is likely endemic in a further 34 countries which have never reported the disease."

So: **45 = endemic but under-reported. 34 = probably endemic, never reported. 79 priority countries in total.** Do not write "45 countries where it is endemic but never reported."

### 1.3 The environmental suitability model — method and covariates

- Occurrence database: **22,338 geo-located records** of human cases, animal cases and environmental *B. pseudomallei*, spanning **1910 to 2014** (literature searched Jan 1 1920 – Dec 31 2014; final dataset spans 1910–2014). [V]
- Method: **boosted regression tree (BRT)** model of environmental suitability at **5 km × 5 km** resolution, then a **negative binomial regression** relating suitability to geo-positioned incidence data, and a **logistic regression** for case fatality. Ensemble of **2,500 global realisations** via bootstrap resampling and Monte Carlo simulation. [V]
- Covariates: soil characteristics (Harmonized World Soil Database), precipitation and land surface temperature (WorldClim), vegetation/moisture index (AVHRR). [V]
- Model performance: **AUC 0.81 (95% CrI 0.76–0.86).** [V]

**Environmental associations found:** [V]

> "We found that high rainfall and temperature, and anthrosol and acrisol soil types were strongly associated with the presence of [*B. pseudomallei*]... We also found that high salinity and high proportion of gravel were associated with the presence of [*B. pseudomallei*]."

**A key negative result, directly relevant to Section 6:** [V]

> "Although our model did not find an association between the presence of [*B. pseudomallei*] and soil pH reported by previous environmental studies, this could be because soil pH is generally associated with other soil factors, particularly soil salinity, reducing the capacity of our model to identify this as a geographic risk factor."

This is a genuine point of tension with the field-sampling literature (see §6.2), and worth flagging in a manuscript rather than glossing.

**Predicted distribution:** [V]

> "We predict that [*B. pseudomallei*] is ubiquitous throughout the tropics. The highest risk zones are in Southeast and South Asia, tropical Australia, Western sub-Saharan Africa and South America. Risk zones of varying sizes are also observed in Central America, Southern Africa and the Middle East."

**Regional burden split — a counterintuitive and frequently missed result:** [V]

> "We predict that only 40% of all melioidosis cases occur in the East Asia and Pacific region, where melioidosis is considered highly endemic. By contrast, South Asia is predicted to bear 44% of the overall burden, because large populations live in areas contaminated with [*B. pseudomallei*]."

**Mortality modelling:** case fatality was predicted from **under-5 mortality rate** (OR 1.88, 95% CrI 1.73–2.07 per 10× increase in infant deaths per 1,000 live births). **>99% of predicted deaths occur in low- and middle-income countries; <1% in high-income countries** (Australia, Brunei Darussalam, Singapore). [V]

**Incidence model covariates:** environmental suitability, adjusted by country income level (aIRR 0.58, 95% CrI 0.23–1.39 for high income — note this CrI crosses 1, so it is not statistically significant) and prevalence of indigenous ethnicity in Australia (aIRR 1.23, 95% CrI 1.09–1.38 per 10% increase). [V]

**Validation caveat stated by the authors:** [V]

> "Only Australia, Brunei Darussalam and Singapore have national surveillance data for melioidosis that are comparable to our estimates."

That is, the model is calibrated against — and validated by — only three countries' surveillance systems.

**Comparative framing used by the authors:** predicted global melioidosis mortality (89,000/yr) is "comparable to those due to measles (95,600 per year) and higher than that due to leptospirosis (50,000 per year) and dengue infection (9,100–12,500 per year)." [V]

### 1.4 The DALY estimate — Birnie et al. 2019

Birnie E, Virk HS, Savelkoel J, Spijker R, Bertherat E, Dance DAB, Limmathurotsakul D, Devleesschauwer B, Haagsma JA, Wiersinga WJ. *Global burden of melioidosis in 2015: a systematic review and data synthesis.* **Lancet Infect Dis 2019;19(8):892–902.** PMID 31285144; DOI 10.1016/S1473-3099(19)30157-4. [C2]

- Systematic review: **475 studies** included from 2,888 articles screened. [V]
- **Global burden 2015: 4.6 million DALYs (UI 3.2–6.6), or 84.3 per 100,000 people (57.5–120.0).** [V]
- **Years of life lost = 98.9% of total DALYs; years lived with disability = 1.1%.** [V] (i.e. the burden is almost entirely premature mortality, not chronic disability.)
- Pneumonia was the most common presentation: 3,633/10,175 patients (**35.7%, 95% UI 34.8–36.6**). [V]

**Relationship to the 2016 paper:** Birnie et al. does **not** supersede Limmathurotsakul et al. It is *built on* it — it takes the 2016 modelled incidence and mortality as input and converts them into DALYs, adding a systematic review of clinical outcomes. The two are therefore not independent estimates, and the 4.6M DALY figure inherits the 2016 model's uncertainty. Both papers share authors (Dance, Limmathurotsakul, Bertherat).

### 1.5 Is there a newer burden estimate that supersedes 2016?

**No.** As of the literature retrieved here, **the 2016 Limmathurotsakul model remains the standard global burden estimate and has not been superseded.** The 2024 *Nature Reviews Microbiology* review by the field's leading authors continues to rely on it: [V]

> "Modelled estimates of the global burden predict that melioidosis remains vastly under-reported, and a call has been made for it to be recognized as a neglected tropical disease by the World Health Organization." — Meumann et al. 2024 [C3]

Meumann EM, Limmathurotsakul D, Dunachie SJ, Wiersinga WJ, Currie BJ. *Burkholderia pseudomallei and melioidosis.* **Nat Rev Microbiol 2024;22(3):155–169.** PMID 37794173; DOI 10.1038/s41579-023-00972-5. [C3]

This is the best single umbrella citation for a Background section. Its abstract also supplies two claims directly useful here: [V]

> "Severe weather events and environmental disturbance are associated with increased case numbers, and it is anticipated that, in some regions, cases will increase in association with climate change. Genomic epidemiological investigations have confirmed B. pseudomallei endemicity in newly recognized regions, including the southern United States."

---

## 2. Recognised endemic regions

### 2.1 Northeast Thailand

Limmathurotsakul D, Wongratanacheewin S, Teerawattanasook N, Wongsuvan G, Chaisuksant S, Chetchotisakd P, Chaowagul W, Day NPJ, Peacock SJ. *Increasing incidence of human melioidosis in Northeast Thailand.* **Am J Trop Med Hyg 2010;82(6):1113–1117.** PMID 20519609; DOI 10.4269/ajtmh.2010.10-0038. [C4]

- **2,243 culture-confirmed cases**, Sappasithiprasong Hospital, Ubon Ratchathani, **1997–2006**. [V]
- **Incidence rose from 8.0/100,000 (95% CI 7.2–10.0) in 2000 to 21.3/100,000 (95% CI 19.2–23.6) in 2006.** [V]
- Average incidence for the province across the study: **12.7/100,000/yr.** [S]
- **Average mortality rate over the study period: 42.6%.** [V]
- Minimum estimated population mortality 2006: **8.63 per 100,000** — making melioidosis **the third most common cause of death from infectious disease in northeast Thailand after HIV/AIDS and tuberculosis.** [V]
- Independent risk factors: male sex, age ≥45 years, known or undiagnosed diabetes. [V]

The 2016 global model paper separately states, verbatim: "In northeast Thailand, there are around 2,000 culture-confirmed melioidosis cases per year with a case fatality rate (CFR) of 40%." [V, C1]

### 2.2 Northern Australia (Darwin / Top End) — the best-characterised endemic setting

Currie BJ, Mayo M, Ward LM, Kaestli M, Meumann EM, Webb JR, Woerle C, Baird RW, Price RN, Marshall CS, Ralph AP, Spencer E, Davies J, Huffam SE, Janson S, Lynar S, Markey P, Krause VL, Anstey NM. *The Darwin Prospective Melioidosis Study: a 30-year prospective, observational investigation.* **Lancet Infect Dis 2021;21(12):1737–1746.** PMID 34303419; DOI 10.1016/S1473-3099(21)00022-0. [C5]

All figures below are **[V]** — taken from the raw Europe PMC `abstractText`, quoted verbatim:

- Period: **1 Oct 1989 – 30 Sept 2019** (30 years), tropical Northern Territory. Melioidosis is a **laboratory-notifiable disease in the NT**.
- **1,148 culture-confirmed cases; 133 (12%) died.**
- Median age 50 (IQR 38–60); 48 (4%) children <15y; 721 (63%) male; **600 (52%) Indigenous Australians.**
- Risk factors: all but 186 (16%) had a clinical risk factor; **513 (45%) diabetes; 455 (40%) hazardous alcohol use.** Only 3 (2%) of 133 fatalities had no identified risk factor.
- Presentation: **pneumonia 595 (52%)**; bacteraemia 633/1,135 (56%); septic shock 240 (21%); mechanical ventilation 180 (16%).
- **Seasonality: "Cases correlated with rainfall, with 80% of infections occurring during the wet season (November to April)."**
- **Incidence: "Median annual incidence was 20·5 cases per 100 000 people; the highest annual incidence in Indigenous Australians was 103·6 per 100 000 in 2011–12."**
- Trend: "Over the 30 years, annual incidences increased, as did the proportion of patients with diabetes, although **mortality decreased to 17 (6%) of 278 patients over the past 5 years**."
- Genomics: "Genotyping of B pseudomallei confirmed case clusters linked to environmental sources and defined evolving and new sequence types."

The paper's own Background sentence is a useful framing quote for a manuscript introduction: [V]

> "The global distribution of melioidosis is under considerable scrutiny, with both unmasking of endemic disease in African and Pacific nations and evidence of more recent dispersal in the Americas."

Case-mix breakdown (from the 2024 narrative review, [C6]): of the 1,148 DPMS patients, **88% acute, 9% chronic, 3% reactivation**. [S]

### 2.3 Malaysia

Arushothy R, Mohd Ali MR, Zambri HF, Muthu V, Hashim R, Chieng S, Nathan S. *Assessing the national antibiotic surveillance data to identify burden for melioidosis in Malaysia.* **IJID Regions 2024;10:94–99.** PMID 38179416; DOI 10.1016/j.ijregi.2023.11.014. [C7]

- National average annual incidence **2014–2020: 3.41 per 100,000.** [V]
- **Highest state incidence: Pahang, 11.33 per 100,000.** [V] Followed by Melaka, Negeri Sembilan, Kedah, Terengganu (8.12 down to 6.27 per 100,000). [S]
- Peninsular Malaysia 3.39/100,000 vs Sabah+Sarawak 3.52/100,000. [S]
- Paediatric melioidosis in Central Sarawak: **4.1 per 100,000 children**; Kapit and Tatau districts **20.2 and 15.7 per 100,000 children** — "among the highest observed in any melioidosis endemic region." [S]
- Paediatric case-mix (Malaysia): among 34 children, **59% had an infection located on the head or neck** — a distinctive regional presentation. [S, C6]
- **Lubuk Yu outbreak** (recreational water exposure): 153 people exposed, 10 confirmed melioidosis, 4 co-infected with leptospirosis, **70% fatality** in that co-infected subgroup. [S, C6] — numbers need primary verification.

### 2.4 Singapore

- From the 2016 global model paper, verbatim: **"In Singapore, 550 melioidosis cases occurred during the last ten years, of which a fifth resulted in death."** [V, C1]
- Reported incidence range **0.6–2.4 per 100,000**. [S] — source not pinned down; **needs a primary citation before use.**
- Liu X, Pang L, Sim SH, Goh KT, Ravikumar S, Win MS, Tan G, Cook AR, Fisher D, Chai LYA. *Association of melioidosis incidence with rainfall and humidity, Singapore, 2003–2012.* **Emerg Infect Dis 2015;21(1):159–162.** PMID 25531547; DOI 10.3201/eid2101.140042. [C8] — **550 cases over the 10-year period**; rainfall and humidity associated with incidence. Notable because Singapore is highly urbanised and direct soil exposure is rare, which the authors take as suggestive of an aerosol/atmospheric route even in urban settings. [V/S]

Singapore is one of only three countries whose national surveillance the 2016 model regarded as comparable to its estimates [V, C1] — so it is an important calibration point, not just another endemic country.

### 2.5 Laos and Cambodia

Bulterys PL, Bulterys MA, Phommasone K, Luangraj M, Mayxay M, Kloprogge S, Miliya T, Vongsouvath M, Newton PN, Phetsouvanh R, French CT, Miller JF, Turner P, Dance DAB. *Climatic drivers of melioidosis in Laos and Cambodia: a 16-year case series analysis.* **Lancet Planet Health 2018;2(8):e334–e343.** PMID 30082048; DOI 10.1016/S2542-5196(18)30172-4. [C9]

- **870 patients diagnosed in Laos** (Oct 1999 – Aug 2015) and **173 in Cambodia** (Feb 2009 – Dec 2013). [S]
- "In recent years, more than 100 people have been diagnosed with melioidosis each year at Mahosot Hospital" in Vientiane, Laos — an acknowledged underestimate of true burden. [S]
- Cambodia paediatric: reported annual incidence of **28–35 cases per 100,000 children** with high case fatality. [S] — **needs primary verification; this is a strikingly high figure.**
- Cambodian paediatric case series (2009–2018), 355 children: **parotitis most frequent (27%)**; in-hospital case fatality **11.5%**. [S, C6]

Paediatric **parotitis** is a hallmark presentation in Southeast Asia (Cambodia, Thailand, Vietnam) and is rare in Australia — a useful clinical-geographic contrast.

### 2.6 Vietnam

- Paediatric retrospective study 2015–2019, 35 culture-confirmed cases: **parotitis most common (43%)**, then lung infection (29%); **case fatality 11%**. [S, C6]
- Vietnam is epidemiologically important for a *genomics* manuscript for a separate reason: the closest ST41 isolates to the autochthonous Georgia, USA strains are **from Vietnam** (see §4.4). [V, C10]

### 2.7 Myanmar

- Melioidosis is historically significant here (the disease was first described in Rangoon by Whitmore and Krishnaswami in 1912 — **[UNVERIFIED]**, I did not retrieve the primary 1912 citation).
- Modern environmental confirmation exists: *"Geographical distribution of Burkholderia pseudomallei in soil in Myanmar"*, PLoS Negl Trop Dis (DOI 10.1371/journal.pntd.0009372). [S] — **PMID not verified.** Establishes soil isolates, i.e. culture-supported endemicity rather than modelling only.

### 2.8 India — and the rising case counts

India is, per the 2016 model, part of the South Asian region predicted to carry **44% of global burden** [V, C1] — far more than its reported case counts suggest.

Reported case counts (all **[S]**, and **mutually inconsistent** — see the conflict note below):

- One systematic review of individual cases: **558 confirmed cases across 20 Indian states/UTs, 1991–2024**; Karnataka 176, Tamil Nadu 161 (together >60% of all reports), Odisha 60, Telangana 25, Pondicherry 22.
- A different source in the same search: Karnataka **499 cases** (8% mortality), Tamil Nadu **210 cases** (22% mortality), Kerala **58 cases** (10% mortality).

⚠️ **CONFLICT.** These two sets cannot both be right (Karnataka 176 vs 499; Tamil Nadu 161 vs 210). They are probably different denominators — one counting individually-reported cases in a systematic review, the other counting all cases from institutional series. **Do not cite either figure until the primary reviews are read directly.** The two candidate sources are PMC12874796 ("Melioidosis in India: A systematic review of individual cases") and PMC12030058 ("Two Decades of Melioidosis in India: A Comprehensive Epidemiological Review); neither was fetched in full here.

Better-supported qualitative claims about India:

- **Progressive increase in reported cases over time, particularly after 2008**, attributed to improved clinical recognition, diagnostic capacity and reporting from tertiary centres — i.e. **ascertainment, not necessarily true incidence.** [S] This distinction matters and should be stated explicitly in a manuscript.
- Endemicity is **culture/environment-supported, not modelling-only**: *B. pseudomallei* has been isolated from the environment in Tamil Nadu and Kerala, and seropositivity in Karnataka reported at 29%. [S]
- **Monsoon concentration: 66.9% of cases June–September.** [S]
- Reporting gap: of 8,673 primary and district health centres nationally, **only 73 have ever reported a melioidosis case, and 96% of reports come from just 30 centres in five states.** [S] — a vivid under-ascertainment statistic if verified.
- India is the **second most common country of acquisition for travel-associated melioidosis (8.8%)** after Thailand. [S, C11]

### 2.9 Sri Lanka

- Melioidosis re-emerged in the literature after a long silence; **ten confirmed cases reported in 2013, with one fatality**, following increased awareness. [S]
- Endemicity is supported by clinical isolates; environmental isolation in Sri Lanka **[UNVERIFIED]** in the sources retrieved.

### 2.10 Southern China — Hainan, Guangxi, Guangdong, Fujian

Zheng X, Xia Q, Xia L, Li W. *Endemic Melioidosis in Southern China: Past and Present.* **Trop Med Infect Dis 2019;4(1):39.** PMID 30823573; DOI 10.3390/tropicalmed4010039. [C12]

Verbatim from the abstract [V]:

> "Between the 1970s and the 1990s, the presence of B. pseudomallei causing melioidosis in humans and other animals was demonstrated in four coastal provinces in southern China: Hainan, Guangdong, Guangxi, and Fujian, although indigenous cases were rare and the disease failed to raise concern amongst local and national health authorities. In recent years, there has been a rise in the number of melioidosis cases witnessed in the region, particularly in Hainan."

And on surveillance [V]:

> "although China has established and maintained an effective communicable disease surveillance system, it has not yet been utilized for melioidosis. Thus, the overall incidence, social burden and epidemiological features of the disease in China remain unclear."

Supporting detail (**[S]**, from this review as relayed in search):
- **170 culture-confirmed cases** hospitalised in three general hospitals in Hainan, **2002–2014**, with a steady increase; pneumonia 34.1% most common; diabetes and outdoor labourers at greatest risk.
- **Cluster of 16 microbiologically confirmed cases after Typhoon Rammasun struck northern Hainan on 18 July 2014** — a good severe-weather data point (§6.4).

### 2.11 Taiwan

Ko WC, Cheung BM, Tang HJ, Shih HI, Lau YJ, Wang LR, Chuang YC. *Melioidosis outbreak after typhoon, southern Taiwan.* **Emerg Infect Dis 2007;13(6):896–898.** PMID 17553230; DOI 10.3201/eid1306.060646. [C13]

Verbatim abstract [V]:

> "From July through September 2005, shortly after a typhoon, 40 cases of Burkholderia pseudomallei infection (melioidosis) were identified in southern Taiwan. Two genotypes that had been present in 2000 were identified by pulsed-field gel electrophoresis. Such a case cluster confirms that melioidosis is endemic to Taiwan."

Note the genomic logic: the *same two genotypes* recurring from 2000 to 2005 is what establishes local endemicity rather than importation — a nice precedent for a genomics-framed argument.

Additional [S]: **782 cases reported in Taiwan over a 20-year period**, with outbreaks clustering in a specific hotspot and coinciding with severe typhoons; **11 local confirmed cases after Typhoon Kemi**, 8 of them in Kaohsiung City. There is a 2025 PLoS NTD paper, *"Geographical and climatic contributions to melioidosis hotspot formation in Southern Taiwan"* (DOI 10.1371/journal.pntd.0012958) — **PMID not verified**, worth retrieving.

---

## 3. Newly recognised and expanding areas — isolates vs modelling

**This is the section where the isolate/model distinction matters most.** The 2016 model predicts risk zones in western sub-Saharan Africa, South America, Central America, southern Africa and the Middle East [V, C1]. Predicted suitability is *not* evidence of presence. Below, each region is graded.

### 3.1 Sub-Saharan Africa — **culture-confirmed, but sparse**

Africa is the clearest example of modelled-high-burden vs almost-no-reported-cases.

Birnie E, James A, Peters F, Olajumoke M, Traore T, Bertherat E, Trinh TT, Naidoo D, Steinmetz I, Wiersinga WJ, Oladele R, Akanmu AS. *Melioidosis in Africa: Time to Raise Awareness and Build Capacity for Its Detection, Diagnosis, and Treatment.* **Am J Trop Med Hyg 2022;106(2):394–397.** PMID 35008053; DOI 10.4269/ajtmh.21-0673. [C14]

Verbatim [V]:

> "Only a few cases have been reported from African countries. However, studies on the global burden of melioidosis showed that Africa holds a significant unrecognized disease burden, with **Nigeria being at the top of the list**."

This paper reports the **first WHO African Melioidosis Workshop**, held in Lagos, Nigeria. [V]

**Culture-confirmed African evidence now exists:**

Rossouw J, Geyer HDW, Birkhead M, Wilson D, Nel J, Karstaedt AS, Haumann CE, Jonker A, Sahl JW, Wagner DM, Frean JA. *Emergence of Human and Animal Melioidosis in Southern Africa, 2018–2021.* **Trop Med Infect Dis 2026;11(2):60.** PMID 41746030; DOI 10.3390/tropicalmed11020060. [C15]

- **Three human cases (South Africa n=2, Namibia n=1) and two ovine cases in South Africa**, 2018–2021. Until this report, human melioidosis had not been reported in southern Africa. [V/S]
- Isolates characterised by **MALDI-TOF MS and whole-genome sequencing**; phylogenetic analysis showed **substantial diversity, suggesting "long-term cryptic persistence"** in the region. [V/S]

**Why this matters for a recombination-aware genomics paper:** substantial genomic *diversity* among a handful of cases is the signature of a long-established population, not a recent point-source introduction. This is the opposite inference to the Mississippi GCS2020 situation (§4.3), and the contrast is worth drawing explicitly.

Other African evidence [S]: a novel sequence type causing lethal septic shock, and *B. pseudomallei* plus *B. thailandensis* isolated from the environment in **Gabon**, via the African Melioidosis Network (Steinmetz and colleagues). A **first culture-confirmed case in Mozambique** (2026, in a 37-year-old man with advanced HIV) and a **retrospective observational study in Mali** were both identified but **not retrieved in full — PMIDs/DOIs UNVERIFIED.**

**Grade: culture-confirmed presence in South Africa, Namibia, Gabon, Mozambique (and historically Malawi, per [C1]); modelled high burden across western sub-Saharan Africa (Nigeria) with essentially no confirmatory isolates.**

### 3.2 The Americas — **culture-confirmed and ecologically established in several locations**

Per the 2016 model, "recent national additions include India, Southern China, Brazil and Malawi." [V, C1]

**Puerto Rico — environmental isolates, ecologically established but rare:**

Hall CM, Jaramillo S, Jimenez R, Stone NE, Centner H, Busch JD, Bratsch N, Roe CC, Gee JE, Hoffmaster AR, Rivera-Garcia S, Soltero F, Ryff K, Perez-Padilla J, Keim P, Sahl JW, Wagner DM. *Burkholderia pseudomallei, the causative agent of melioidosis, is rare but ecologically established and widely dispersed in the environment in Puerto Rico.* **PLoS Negl Trop Dis 2019;13(9):e0007727.** PMID 31487287; DOI 10.1371/journal.pntd.0007727. [C16]

Verbatim findings [V]:
- **600 environmental samples (500 soil, 100 water) from 60 sites.** Only **three adjacent soil samples from one site** were PCR-positive; **55 isolates** obtained from two of them.
- "The 55 B. pseudomallei isolates exhibited fine-scale variation in the core genome and contained **four novel genomic islands**."
- "Phylogenetic analyses grouped Puerto Rico B. pseudomallei isolates into a **monophyletic clade containing other Caribbean isolates, which was nested inside a larger clade containing all isolates from Central/South America**."
- "Phylogeographic patterns suggest the source of B. pseudomallei populations in Puerto Rico and elsewhere in the Caribbean **may have been Central or South America**."

Note the striking rarity: 3/600 samples positive, all from one site — yet described as "ecologically established and widely dispersed" because previous human and environmental isolates came from *eastern* Puerto Rico while this site was north-central. The "widely dispersed but rare" formulation is the authors' own and should be quoted rather than paraphrased as "widespread."

**Mexico, Central America and the Caribbean:**

Sanchez-Villamil JI, Torres AG. *Melioidosis in Mexico, Central America, and the Caribbean.* **Trop Med Infect Dis 2018;3(1):24.** PMID 29780897; DOI 10.3390/tropicalmed3010024. [C17]

- First reports date to the **late 1940s**; new endemic foci reported in **Mexico, Costa Rica, Guadeloupe, Puerto Rico**, with sporadic cases elsewhere in the Caribbean, Central and South America. [V/S]
- The review's own framing: "a lack of both diagnostic capacity and awareness of the disease has resulted in a limited number of studies that have attempted to accurately determine its prevalence and geographical distribution." [V]

**Americas-wide case tally [S]:** a prior review described **120 human cases 1947–2015, of which 95 (79%) were likely acquired in the Americas; mortality 39%.** — needs primary citation.

**South America [S]:** confirmed human cases from **Ecuador, Venezuela, Colombia, Brazil, Peru**; *B. pseudomallei* **isolated from the environment in Brazil and Peru** (so: culture-supported, not modelling-only).

**Brazil specifically [S]:**
- First documented cases **2003, Ceará state**: four siblings infected after recreational exposure at a town dam; **three died within a week.**
- By 2017, **30 cases diagnosed in Ceará.**
- Environmental isolation: ***B. pseudomallei* isolated from 26 (4.3%) of 600 samples** across dry and rainy seasons.
- A case series of **seven patients in Piauí State, 2019–2021** (J Med Case Reports, DOI 10.1186/s13256-023-04093-8; PMID **UNVERIFIED**).

**Grade for the Americas: culture-confirmed and environmentally isolated in Brazil, Peru, Puerto Rico, and now the continental USA (§4). Elsewhere in Central America/Caribbean, clinical isolates without systematic environmental confirmation.**

**Phylogeographic framing.** The Western Hemisphere isolates form a distinct clade; the standing hypothesis is derivation "from a constricted seeding event from Africa" [S], elaborated in [C10] as dispersal "from Africa to the Americas in the 17th–19th centuries, potentially implicating the transatlantic slave trade." [V]

### 3.3 The Middle East — **weakest evidence**

- The 2016 model predicts risk zones of varying size in the Middle East. [V, C1]
- Reported cases: **UAE and Oman reported imported cases (2024)** [S, C6]; sporadic case reports include **Iran** [S].
- **Grade: essentially modelling-only for autochthonous transmission.** I found no environmental isolation and no clearly autochthonous case series from the Middle East. **This is a genuine gap — state it as such rather than implying endemicity.**

### 3.4 Pacific islands and Papua New Guinea — **culture-confirmed in PNG and New Caledonia; serology-only elsewhere**

Warner JM, Currie BJ. *Melioidosis in Papua New Guinea and Oceania.* **Trop Med Infect Dis 2018;3(1):34.** PMID 30274431; DOI 10.3390/tropicalmed3010034. [C18]

Region-by-region (all **[S]** unless noted; from the PMC full text via summarised fetch):

| Location | Evidence grade | Detail |
|---|---|---|
| **PNG — Balimo, Western Province** | **Clinical + environmental isolates** | 8 culture-confirmed cases in 18 months during active case detection (1990s); *B. pseudomallei* recovered from **2.6% of 274 soil samples**; seroprevalence in some villages matching northern Australia. Childhood predilection, chronic presentation mimicking TB. 3 MLST genotypes among 13 clinical + 26 environmental isolates, **ST267** most prevalent |
| **PNG — Port Moresby** | Clinical isolates, rare | 7 culture-confirmed cases since 1975; only **2 of 2,285 blood cultures positive (0.09%, 95% CI 0.01–0.32%)** in 2000–2002 surveillance; 1 of 1,309 sputum samples from TB patients |
| **New Caledonia** | **Clinical + animal isolates** | **19 confirmed cases since 1999**; 32% chronic disease incl. skin lesions; **ST292** dominant on the endemic east coast; first confirmed animal case in a **goat** |
| **Guam** | Clinical isolates | First cases 1946, among military personnel |
| **Fiji** | **Inferred only** | Australian cases with infection acquired there, but **no confirmed culture isolates documented** |
| **East Timor** | **Serology only** | Seroprevalence evidence; **no confirmed cultures** |
| **Yap (FSM)** | Clinical | Cluster of **7 cases, all fatal, 2013–2016**; CDC investigation [S — verify] |

Key verified statement from the abstract [V]:

> "Clinical cases and environmental reservoirs documented in Balimo, Papua New Guinea and Northern Province of New Caledonia, with **incidence similar to tropical Australia**. Burkholderia pseudomallei isolates **phylogenetically linked to Australian strains**."

Authors attribute under-recognition to lack of laboratory facilities, clinical unawareness, and the **competing burden of tuberculosis** (melioidosis mimics TB) [V] — a mechanism worth stating in §8.

A biogeographic hypothesis relevant to a phylogenomics manuscript [S]: an **ice-age land bridge ~20,000 years ago** may have carried ancestral strains between Australia and Asia via PNG.

Currie BJ, Meumann EM. *Melioidosis in Asia-Pacific Nations: Expanding Boundaries but Unknowns Remain.* **Respirology 2025;30(10):917–919.** PMID 40730495; DOI 10.1111/resp.70098. [C19] — a recent editorial framing; full text was 403-blocked at Wiley, **content UNVERIFIED beyond the citation itself.**

---

## 4. The United States

This is the most consequential recent development in melioidosis geography, and it is almost entirely a **genomics** story — which makes it ideal material for this manuscript.

### 4.1 Background: prior US status

Before 2022, *B. pseudomallei* had **never been isolated from the environment in the continental United States.** [V, C21] The 2016 model had nonetheless flagged the US as suitable: [V, C1]

> "We also predict that two (USA and Japan) of the 44 countries where [*B. pseudomallei*] is considered currently absent have areas which would be suitable for [*B. pseudomallei*] establishment. These include a **geographically contiguous area covering southern parts of Florida, Louisiana and Texas** in the USA, and **Okinawa and Kagoshima prefectures in Japan**."

The model also assessed Louisiana after the **November 2014 Tulane National Primate Research Center** incident: suitability at the Center itself was **0.02**, but **0.55 in New Orleans, 35 miles south** — comparable to Saravane, Laos (0.54). [V, C1] The authors concluded establishment "would be possible... if the bacterium were to be released widely," and noted "It is also possible that [*B. pseudomallei*] is already present in the environment in USA and Japan but has never been detected." [V] **That last sentence was, in hindsight, correct** — a strong narrative hook.

### 4.2 The 2021 multistate aromatherapy spray outbreak

Gee JE, Bower WA, Kunkel A, Petras J, Gettings J, Bye M, Firestone M, Elrod MG, Liu L, Blaney DD, Zaldivar A, Raybern C, Ahmed FS, Honza H, Stonecipher S, O'Sullivan BJ, Lynfield R, Hunter M, Brennan S, Pavlick J, Gabel J, Drenzek C, Geller R, Lee C, Ritter JM, Zaki SR, Gulvik CA, Wilson WW, Beshearse E, Currie BJ, Webb JR, Weiner ZP, Negrón ME, Hoffmaster AR. *Multistate Outbreak of Melioidosis Associated with Imported Aromatherapy Spray.* **N Engl J Med 2022;386(9):861–868.** PMID 35235727; DOI 10.1056/NEJMoa2116130. [C20]

**Cases — four, in four states, all in 2021** [V]:

| Patient | State | Age/sex | Onset | Outcome |
|---|---|---|---|---|
| 1 | Kansas | 53 F | ~4–5 days before 13 Mar 2021 | **Died**, hospital day 9 |
| 2 | Texas | 4 F | fever from 31 May 2021 | Survived, **neurologic sequelae** |
| 3 | Minnesota | 53 M | altered mental status 29 May 2021 | Survived |
| 4 | Georgia | 5 M | ~9 Jul 2021 (presented 12 Jul) | **Died**, hospital day 4 |

**Two of four died; both fatalities and both paediatric cases are notable — a 4-year-old survived with severe residual neurological disability and a 5-year-old died.** [V]

**The product and the genomic link** [V]:
- *B. pseudomallei* was isolated from an aromatherapy room spray **obtained from the home of Patient 4**.
- Product: **"Better Homes and Gardens"-brand** "highly fragranced essential oil and semi-precious stone infused room spray," **"lavender and chamomile"** scent. Sold via Walmart. **Imported from India.**
- Strain designation: **ATS2021** ("aromatherapy spray 2021").
- "whole-genome sequencing analysis indicated that the isolate from the spray bottle and those from the four patients were **all the same strain**."
- "Strain ATS2021 also **clustered with samples of B. pseudomallei from South Asia that are consistent with the origin of the spray — India**."

**Route of infection.** The NEJM paper is careful and does **not** definitively assign a route, stating only that "Exposure to this bacterium typically occurs through inhalation, ingestion, or the percutaneous route." [V] Secondary sources assert inhalation was "the likely route," explaining the high morbidity [S]. **Flag this as inference, not established fact,** if used.

**Sequence type: the NEJM paper names the strain ATS2021 but I did not confirm an MLST ST number for it. [UNVERIFIED]**

Timeline detail: the spray was distributed to Walmart stores and sold online **between February and 21 October 2021** [S]; the **recall date is not stated in the retrieved text [UNVERIFIED]**. CDC issued **HAN Advisory 455 on 25 October 2021** [S].

### 4.3 The 2022 Mississippi Gulf Coast environmental finding

**CDC Health Advisory HAN-00470, distributed 27 July 2022** [C21], titled: *"Melioidosis Locally Endemic in Areas of the Mississippi Gulf Coast after Burkholderia pseudomallei Isolated in Soil and Water and Linked to Two Cases – Mississippi, 2020 and 2022."*

CDC's conclusion, verbatim [V]:

> "melioidosis is now considered to be **locally endemic in areas of the Gulf Coast region of Mississippi**."

- Two unrelated cases, **July 2020 and May 2022**, both Gulf Coast Mississippi residents with **no recent international travel**. [V]
- Environmental sampling **June 2022**, on the 2020 patient's property and nearby areas, plus household products. **Three soil and water samples positive** by PCR and culture. [V]
- "B. pseudomallei isolates from both patients and the environmental samples were **all genetically similar and were distinct from previous known isolates**, indicating bacteria from the environment was the likely source." [V]

CDC recommendations: clinicians should consider melioidosis in Gulf Coast residents **regardless of travel history**; laboratorians must verify automated identification systems (which misidentify the organism); health departments should add melioidosis to reportable disease lists; public should avoid soil/muddy water contact and protect open wounds. [V]

### 4.4 The full Mississippi investigation — three cases and strain GCS2020

Petras JK, Elrod MG, Ty MC, Dawson P, O'Laughlin K, Gee JE, et al. *Locally Acquired Melioidosis Linked to Environment — Mississippi, 2020–2023.* **N Engl J Med 2023;389(25):2355–2362.** PMID 38118023; DOI 10.1056/NEJMoa2306448. Published **21 December 2023.** [C22]

*(Author list beyond the first several is **[S]** — I confirmed the citation, journal, volume, pages, PMID and DOI, but did not capture the complete author string.)*

**Three patients, same Mississippi Gulf Coast county, over three years** [V]:

| Patient | Date | Age/sex | Risk factors | Outcome |
|---|---|---|---|---|
| 1 | July 2020 | 39 M | Type 2 diabetes, alcohol use disorder, fatty liver disease, obesity, 20 pack-years tobacco | Recovered |
| 2 | April 2022 | 62 M | Excessive alcohol use, hypertensive heart disease, prediabetes, >10 pack-years tobacco | Recovered |
| 3 | January 2023 | 64 M | Hypertension, arthritis (no metabolic risk factors) | Under investigation at publication |

**Environmental sampling** [V]:
- **188 samples total: 59 in 2020, 109 in 2022** (note: 59+109=168, not 188 — **arithmetic discrepancy in my extraction; verify sample counts against the paper's Methods before citing**). ⚠️
- **3 positive: one water puddle and two soil samples, all from Patient 1's property.** All other locations negative, including Patient 2's property.

**Strain GCS2020 ("Gulf Coast Strain 2020")** [V]:
- **Sequence type: ST92**, a Western Hemisphere ST.
- **">1000 SNPs distant from any other genome available"** — i.e. not a match to any previously encountered isolate.
- **"groups with strains associated with South America."**
- Clinical and environmental isolates were **clonal to each other (3 to 15 SNPs apart)**.

**Conclusion** [V]: *"These findings indicate that melioidosis may be endemic to the Mississippi Gulf Coast region"*, representing *"the first environmental isolation of B. pseudomallei in the continental United States."*

**Note the hedging: "may be endemic."** The NEJM authors are more cautious than the CDC HAN, which said "is now considered to be locally endemic." Worth noting the difference in register.

**The >1000 SNP distance is the key genomic argument** and is directly germane to a recombination-aware SNP paper: it is what rules out recent importation and establishes a long-resident, previously unsampled population. Contrast with ATS2021 (§4.2), which clustered tightly with South Asian genomes and was therefore attributed to import.

### 4.5 Georgia, 2024 — a second US focus, and a 41-year genomic link

Brennan S, Thompson JM, Gulvik CA, Paisie TK, Elrod MG, Gee JE, Schrodt CA, DeBord KM, Richardson BT, Drenzek C, Bower WA, Hoffmaster AR, Weiner ZP, Cossaboom CM, Gabel J. *Related Melioidosis Cases with Unknown Exposure Source, Georgia, USA, 1983–2024.* **Emerg Infect Dis 2025;31(9):1802–1806.** PMID 40835221; DOI 10.3201/eid3109.250804. [C23]

Verbatim abstract [V]:

> "We identified **4 cases of presumptive autochthonous melioidosis during 1983–2024 in Georgia, USA**. Epidemiologic investigation identified no recent international travel before illness; **all cases were geographically linked, and 3 patients became ill after a severe weather event**. Bioinformatic analyses revealed Burkholderia pseudomallei genome sequences were highly related, suggesting a shared exposure."

Detail [S/V via C10]:
- **Two human cases in September 2024, following Category 4 Hurricane Helene.** Both **ST41**.
- CDC's multidecade surveillance archive yielded **two further historical ST41 Georgia cases, 1983 and 1989, both fatal, both in the same county** as the 2024 cases.
- **All four ST41 genomes separated by <20 SNPs despite spanning four decades.** [V, C10]
- **ST41 is of Southeast Asian, not Americas, origin; the closest ST41 isolates to the Georgia strains are from Vietnam.** [V, C10]

**Hypothesis** [V, C10]: "unlike the presumptively more recent introduction of *B. pseudomallei* into Mississippi, *B. pseudomallei* may have entered Georgia decades ago with returning troops and equipment following the Vietnam War."

**<20 SNPs across 41 years is a remarkable claim about molecular clock rate / environmental dormancy** and is exactly the sort of result a recombination-aware SNP method should be able to interrogate. Strongly recommend engaging with this directly.

### 4.6 Current CDC / expert position on US endemicity

Currie BJ, Kaestli M, Meumann EM. *Global dispersal of Burkholderia pseudomallei and the evolving endemicity of melioidosis in the United States of America.* **PLoS Negl Trop Dis 2026;20(4):e0014217.** PMID 42030350; DOI 10.1371/journal.pntd.0014217. [C10]

Verbatim [V]:

> "Melioidosis should therefore now be considered **endemic in Mississippi and is likely endemic in Georgia and Texas**, although B. pseudomallei is yet to be cultured from the environment in the latter two states."

**Texas** [V]: one suspected locally acquired case (2018), no environmental confirmation. Phylogenomic analysis of that case plus two historical cases from Texas and Arizona placed all three in the **"Americas" clade**, "supporting introduction of *B. pseudomallei* to Texas from South or Central America or the Caribbean."

**Summary of US evidence grades:**

| State | Human cases | Environmental isolate | Strain | Grade |
|---|---|---|---|---|
| Mississippi | 3 (2020, 2022, 2023) | **Yes** (3 samples) | GCS2020, ST92, Americas clade | **Endemic** |
| Georgia | 4 (1983, 1989, 2024×2) | No | ST41, SE Asian origin | **Likely endemic** |
| Texas | 1 suspected (2018) + historical | No | Americas clade | **Likely endemic** |
| (Multistate 2021) | 4 | Product only, not environment | ATS2021, South Asian | **Imported, not endemic** |

Also note [V, C10]: melioidosis became a **Nationally Notifiable Disease in the US** following a favourable vote at the 2022 CSTE conference [S — verify the CSTE detail].

---

## 5. Modes of transmission — with evidence quality

### 5.1 Percutaneous inoculation — **the presumed dominant route; evidence: strong but largely indirect**

The 2016 model paper states plainly: "Skin inoculation is considered the main route of infection in agricultural workers in developing countries." [V, C1]

The strongest direct epidemiological evidence is the matched case-control study:

Limmathurotsakul D, Kanoksil M, Wuthiekanun V, Kitphati R, deStavola B, Day NPJ, Peacock SJ. *Activities of Daily Living Associated with Acquisition of Melioidosis in Northeast Thailand: A Matched Case-Control Study.* **PLoS Negl Trop Dis 2013;7(2):e2072.** PMID 23437412; DOI 10.1371/journal.pntd.0002072. [C24]

Design: prospective hospital-based **1:2 matched case-control**, **286 culture-confirmed cases and 512 controls**, matched on gender, age ±5 years and diabetes status. [S]

Conditional odds ratios (**[S] — these were read from a summarised fetch of the PMC table; verify against the published Table before citing**):

| Exposure | cOR (95% CI) | Route implicated |
|---|---|---|
| Working in a rice field | 2.1 (1.4–3.3) | Percutaneous |
| Open wound | 2.0 (1.2–3.3) | Percutaneous |
| Other soil/water exposure | 1.4 (0.8–2.6) *(NS)* | Percutaneous |
| Outdoor rain exposure | 2.1 (1.4–3.2) | Inhalation |
| Water inhalation | 2.4 (1.5–3.9) | Inhalation/aspiration |
| Drinking untreated water | 1.7 (1.1–2.6) | Ingestion |
| Eating soil/dust-contaminated food | 1.5 (1.0–2.2) | Ingestion |
| Current smoking | 1.5 (1.0–2.3) | (host factor) |
| Oral steroid use | 3.1 (1.4–6.9) | (host factor) |

Also reported: "Presence of *B. pseudomallei* in drinking water source(s) **doubled the odds** of acquiring melioidosis" (7% of cases vs 3% of controls). [S]

**Protective factors** [S]: wearing **long trousers or rubber boots**, and **washing after working in the rice field**, were each associated with decreased risk.

**Critical interpretive point:** this single study supports percutaneous, inhalational *and* ingestion routes simultaneously, with overlapping confidence intervals. It does **not** establish the relative contribution of each. Claims that percutaneous inoculation accounts for "most" cases are conventional wisdom supported by exposure epidemiology, **not** by any study that has partitioned routes quantitatively. Say so.

Prevention guidance derived from this evidence base [S]: residents, rice farmers and visitors should wear boots and gloves for soil/water contact, drink only bottled or boiled water, and avoid outdoor exposure to heavy rain or dust clouds. Adherence is poor — focus-group work found participants "not inclined to use boots and gloves while working in muddy rice fields." [S]

### 5.2 Inhalation and the severe-weather/aerosol hypothesis — **evidence: moderate-to-strong, and improving**

**The foundational clinical observation:**

Currie BJ, Jacups SP. *Intensity of rainfall and severity of melioidosis, Australia.* **Emerg Infect Dis 2003;9(12):1538–1542.** PMID 14720392; DOI 10.3201/eid0912.020750. [C25]

12-year prospective study, **318 culture-confirmed cases**, Top End NT [V/S]:
- Univariate: prior 14-day rainfall **≥125 mm** correlated with **pneumonia (OR 1.70), bacteraemia (OR 1.93), septic shock (OR 1.94), death (OR 2.50)**. [S]
- Multivariate: 14-day pre-admission rainfall was an **independent risk factor for pneumonia (p=0.023), bacteraemic pneumonia (p=0.001), septic shock (p=0.005) and death (p<0.0001)**. [S]
- Verbatim [V]: *"Median rainfall in the 14 days before admission was highest (211 mm) for those dying with melioidosis, in comparison to 110 mm for those surviving (p=0.0002)."*
- Verbatim conclusion [V]: *"Heavy monsoonal rains and winds may cause a shift towards inhalation of Burkholderia pseudomallei."*

Note this is an **association between rainfall and disease severity/phenotype**, from which inhalation is *inferred*. It is a hypothesis, well-supported but not a demonstration of aerosol transmission.

**The direct aerosol evidence — much stronger:**

Chen PS, Chen YS, Lin HH, Liu PJ, Ni WF, Hsueh PT, Liang SH, Chen C, Chen YL. *Airborne Transmission of Melioidosis to Humans from Environmental Aerosols Contaminated with B. pseudomallei.* **PLoS Negl Trop Dis 2015;9(6):e0003834.** PMID 26061639; DOI 10.1371/journal.pntd.0003834. [C26]

In an endemic area of Taiwan [V]: the bacterium primarily inhabits north-west cropped fields while cases concentrate in the densely populated south-east. Soil and aerosol samples across a **72 km²** area found *B. pseudomallei*-specific DNA well distributed during the rainy season; **DNA concentration correlated positively with disease incidence and with north-westerly winds**. **PFGE Type Ia (ST58) predominated, linking soil, aerosol and human isolates.**

**This is the single best citation for airborne transmission** — it closes the loop from soil → aerosol → patient with matched genotypes, rather than inferring from weather.

**Evidence grade: inhalation is established as a real route; its quantitative contribution remains unresolved.**

### 5.3 Ingestion of contaminated water — **evidence: moderate, strongest from water-supply outbreaks**

- Case-control: drinking untreated water cOR **1.7 (1.1–2.6)**; presence of *B. pseudomallei* in the drinking water source doubled the odds. [S, C24]
- The 2016 model paper: "Recent evidence also suggests that inhalation of [*B. pseudomallei*] during extreme weather events and **ingestion of [*B. pseudomallei*] contaminated water** are also important routes of infection." [V, C1]

**Water-supply outbreaks with genomic source attribution** — the strongest evidence, and highly relevant to this manuscript:

McRobb E, Sarovich DS, Price EP, Kaestli M, Mayo M, Keim P, Currie BJ. *Tracing melioidosis back to the source: using whole-genome sequencing to investigate an outbreak originating from a contaminated domestic water supply.* **J Clin Microbiol 2015;53(4):1144–1148.** PMID 25631791; DOI 10.1128/JCM.03453-14. [C27]

Verbatim [V]:
> "Two cases of melioidosis within a 3-month period at a residence in rural northern Australia prompted an investigation... **B. pseudomallei isolates from the property's groundwater supply matched the multilocus sequence type of the clinical isolates.** Whole-genome sequencing confirmed the water supply as the probable source of infection in both cases, with the clinical isolates **differing from the likely infecting environmental strain by just one single nucleotide polymorphism (SNP) each**."

This paper also directly anticipates the methodological concerns of a recombination-aware SNP manuscript [V]:
> "For the first time, we report a phylogenetic analysis of genomewide insertion/deletion (indel) data, an approach conventionally viewed as problematic due to high mutation rates and homoplasy. Our whole-genome indel analysis was concordant with the SNP phylogeny... Our methods and findings have important implications for outbreak source tracing of this bacterium and **other highly recombinogenic pathogens**."

**Strongly recommend citing [C27] — it is both an ecology/transmission citation and a methods precedent.**

A companion paper showing the opposite (non-clonal) pattern:

Sarovich DS, Chapple SNJ, Price EP, Mayo M, Holden MTG, Peacock SJ, Currie BJ. *Whole-genome sequencing to investigate a non-clonal melioidosis cluster on a remote Australian island.* **Microb Genom 2017;3(8):e000117.** PMID 29026657; DOI 10.1099/mgen.0.000117. [C28]

Verbatim [V]:
> "We analysed the genome-wide relatedness of the two most common multilocus sequence types (STs) involved in the outbreak, **STs 125 and 126**. This analysis showed that although these STs were closely related on a whole-genome level, they demonstrated **evidence of multiple recombination events that were unlikely to have occurred over the timeframe of the outbreak**... Our results confirm the previous hypothesis that a **single unchlorinated water source harbouring multiple B. pseudomallei strains** was linked to the outbreak, and that increased melioidosis risk in this community was associated with **Piper methysticum root (kava) consumption**."

**This is arguably the most directly relevant citation in the entire corpus for a recombination-aware SNP paper** — it is an explicit demonstration that recombination confounds outbreak-timeframe inference in *B. pseudomallei*. Flag prominently.

Other water-supply evidence [S]:
- Two clonal clusters of human melioidosis in remote Indigenous communities in northern Australia traced by molecular typing to contaminated **community water supplies**; fatalities in both. In one the water was unchlorinated; in the other the chlorination system was not adequately maintained.
- *B. pseudomallei* isolated from a **water storage tank** and from **spray formed in a pH-raising aerator unit** one year after an outbreak in a remote coastal community in north-western Australia — note this is simultaneously an ingestion *and* aerosol reservoir.
- Inglis et al., *Burkholderia pseudomallei traced to water treatment plant in Australia*, PMID 10653571 [S — not retrieved in full].
- Australian bore water: *Burkholderia pseudomallei in Unchlorinated Domestic Bore Water, Tropical Northern Australia*, EID 2011;17(7) [S — PMID/DOI **UNVERIFIED**].

**Animal parallel** [S]: an outbreak of **159 cases in intensive piggeries in Queensland** attributed to water supply contamination; a clonal outbreak in pigs near Darwin linked to *B. pseudomallei* cultured from the farm's bore water.

### 5.4 Near-drowning and aspiration — **evidence: strong for the association, based on case series**

Chierakul W, Winothai W, Wattanawaitunechai C, Wuthiekanun V, Rugtaengan T, Rattanalertnavee J, Jitpratoom P, Chaowagul W, Singhasivanon P, White NJ, Day NP, Peacock SJ. *Melioidosis in 6 tsunami survivors in southern Thailand.* **Clin Infect Dis 2005;41(7):982–990.** PMID 16142663; DOI 10.1086/432942. [C29]

Verbatim, from the raw abstract [V]:
- "Six cases of melioidosis were identified in survivors of the **26 December 2004 tsunami** who were admitted to Takuapa General Hospital in Phangnga, **a region in southern Thailand where melioidosis is not endemic. All 6 cases were associated with aspiration, and 4 were also associated with laceration.**"
- "The 6 patients (age range, 25–65 years) presented with signs and symptoms of pneumonia **3–38 days (median duration, 6.5 days) after the tsunami.**" Blood cultures positive in 3, respiratory secretions in 4. **Two required ventilation and inotropes; 1 died.**
- Comparison with 22 patients with aspiration-related melioidosis in **endemic** northeast Thailand (1987–2003): the endemic patients had a **shorter interval (median 1 day)** between aspiration and pneumonia onset, were more likely to have shock/respiratory failure/renal failure/altered consciousness (p=.03), and had **higher in-hospital mortality (64%, 14/22; p=.07).**
- **Environmental contrast, verbatim:** "Only **3 (0.8%) of 360 soil samples from Phangnga** were positive for B. pseudomallei, compared with **26 (20%) of 133 samples from northeast Thailand** (P<.0001)."
- Conclusion: "Tsunami survivors are at increased risk of melioidosis if they are injured in an environment containing B. pseudomallei."

The 25-fold difference in soil positivity between a non-endemic and an endemic region, in one paper, is a useful quantitative anchor for §6.

### 5.5 Vertical transmission and breast milk — **evidence: a small number of well-documented cases, one genotype-confirmed**

Ralph A, McBride J, Currie BJ. *Transmission of Burkholderia pseudomallei via breast milk in northern Australia.* **Pediatr Infect Dis J 2004;23(12):1169–1171.** PMID 15626961; DOI 10.1097/01.inf.0000145548.79395.da. [C30]

Verbatim abstract [V]: *"Two cases of maternal to child transmission of melioidosis are reported from Australia's tropical north. One infant died of overwhelming sepsis. Both lactating mothers had mastitis."*

Genotype confirmation [S]: in one case, *B. pseudomallei* isolated from breast milk was **identical on PFGE** to the blood and CSF isolates from the infant. **This is the key evidence — without it the association would be circumstantial.**

Abbink FC, Orendi JM, de Beaufort AJ. *Mother-to-child transmission of Burkholderia pseudomallei.* **N Engl J Med 2001;344(15):1171–1172.** PMID 11302149; DOI 10.1056/NEJM200104123441516. [C31] (Correspondence; no abstract.)

Neonatal systematic review [S]: of neonatal melioidosis cases, **3 (12%) were confirmed direct vertical transmission and 1 (4%) breast-milk transmission** — denominator not captured; **verify** (candidate source PMC12315437).

**Evidence grade: real but rare; mechanism (mastitis → breast milk) plausible and genotype-supported in at least one instance.**

### 5.6 Sexual transmission — **evidence: WEAK. Treat with explicit scepticism.**

The frequently cited report involves **an American Vietnam veteran with *B. pseudomallei*-associated prostatitis and his spouse**, but this is **supported only by serology**, with no isolate or genotype linkage. Secondary sources describe it as "speculative and unconfirmed." [S]

**I did not retrieve the primary citation for this case. [UNVERIFIED]** If the manuscript mentions sexual transmission, it should (a) cite the primary report directly, and (b) state that the evidence is serological only. Do not present it as established.

### 5.7 Person-to-person transmission — **evidence: extremely rare; one genomically confirmed event**

- Consensus position [S]: "The person-to-person route of transmission is very rare, and **only standard infection control measures** have been recommended for clinical care of patients with melioidosis."
- A preprint exists: *"Comparative genomics confirms a rare melioidosis human-to-human transmission event and reveals incorrect phylogenomic reconstruction due to polyclonality"* (bioRxiv 804344). [S] — **note the title's second clause is directly on-topic for a recombination/phylogenomics manuscript: polyclonality causing incorrect phylogenomic reconstruction.** Check whether this was subsequently published in a peer-reviewed venue; **currently UNVERIFIED as a citable reference.**

### 5.8 Nosocomial transmission — **evidence: weak/anecdotal in what I retrieved**

Reported vehicles [S]: *B. pseudomallei*-contaminated **wound irrigation fluid, antiseptics, and hand-wash detergent**.

⚠️ **CAUTION.** My searches for nosocomial melioidosis returned mostly *Burkholderia cepacia* complex outbreaks (chlorhexidine mouthwash, octenidine mouthwash, IV medications), which are a **different organism** and must not be cited as melioidosis evidence. **I found no verified primary citation for a nosocomial melioidosis outbreak. This is an open gap.**

### 5.9 Laboratory-acquired infection — **evidence: rare, documented; primary source not retrieved**

- Consensus [S]: "Laboratory-acquired infections are also rare, but can occur, especially if procedures produce aerosols."
- *B. pseudomallei* is a **CDC Tier 1 Select Agent** [V, C27] — which is why laboratory exposures trigger formal risk assessment and post-exposure prophylaxis protocols.
- The relevant US source is *"Melioidosis Cases and Selected Reports of Occupational Exposures to Burkholderia pseudomallei — United States, 2008–2013"*, MMWR Surveill Summ 2015;64(5). **The CDC page returned HTTP 403 and I could not retrieve it. Case counts, exposure numbers and outcomes are UNVERIFIED.**
- The canonical biosafety reference (Peacock et al., laboratory exposure management guidelines) was **not retrieved. [UNVERIFIED]**

### 5.10 Zoonotic and animal cases — **evidence: extensive; but animals are sentinels, not usually sources for humans**

- Susceptible species [S]: melioidosis occurs most commonly in **sheep, goats and pigs**; also cattle, buffalo, horses, mules, deer, camels, alpacas, dogs, cats, dolphins, wallabies, koalas, primates (human and non-human), birds, tropical fish and reptiles. In northern Australia, **goats, sheep, camels and alpacas** are considered particularly susceptible.
- **Direct animal-to-human zoonotic transmission is not considered an important route** — animals and humans are generally infected from the same environmental source. (Consistent across sources; **no single primary citation retrieved for this negative claim — [UNVERIFIED] as a citable statement.**)

**Importation of infected animals as a mechanism of geographic spread** — this *is* well-documented and matters for a distribution/genomics narrative:

- **Paris, 1975.** Verbatim from [C1] [V]: *"Previous importation events to non-endemic regions include an outbreak of melioidosis in 1975 in Paris, resulting in the deaths of two humans and an unknown number of animals. [B. pseudomallei] then persisted in the soil for up to six years."* The widely repeated detail that the index animal was **a panda imported from China**, and that the epidemic spread to other zoos (Mulhouse) and to equestrian clubs across France, is **[S] and not in the [C1] text** — verify before repeating.
- **Tulane National Primate Research Center, Louisiana, November 2014.** Verbatim from [C1] [V]: *"The results of a CDC investigation concluded that the organism had spread from a building where mice were being infected experimentally to primates within the facility possibly through contamination of the inner garments worn by staff. It is, however, not yet known whether [B. pseudomallei] could have contaminated and persisted in the environment in Louisiana."*
- Imported primates in Britain (PMID 1279882) and cynomolgus macaques imported to the US from Cambodia (PMC9827603). [S]
- From [C10] [V]: *"Various imported animals have been diagnosed with melioidosis, including primates from Southeast Asia and pet iguanas from Central America."* And critically: *"**in none of these other examples of imported melioidosis was there evidence of environmental persistence of B. pseudomallei**"* — i.e. importation happens often, establishment almost never. Mississippi is the exception.
- **Maryland aquarium case** [V, C10]: *"A single case of melioidosis from Maryland was traced to a freshwater home aquarium that had contained imported tropical fish, with B. pseudomallei genotyping supporting Southeast Asian origin."*
- New Caledonia: first confirmed animal case in a **goat** [S, C6/C18].
- A 2025 EID report of *B. pseudomallei* in an American Quarter Horse in Florida (PMID 40563095) [S — not retrieved].

---

## 6. Environmental ecology

### 6.1 The soil and water reservoir

*B. pseudomallei* is a free-living saprophyte of soil and surface water in tropical and subtropical regions [V, C3]. It is not an obligate pathogen and has no requirement for an animal host — the environmental reservoir *is* the reservoir.

Quantitative anchors for soil prevalence:
- **Northeast Thailand (highly endemic): 26 of 133 soil samples positive (20%).** [V, C29]
- **Phangnga, southern Thailand (non-endemic): 3 of 360 positive (0.8%).** [V, C29]
- **Lowland rice paddy, Laos: 195 of 653 samples (29.7%).** [V, C32]
- **Balimo, PNG: 2.6% of 274 soil samples.** [S, C18]
- **Puerto Rico: 3 of 600 samples (0.5%), all from a single site.** [V, C16]
- **Brazil: 26 of 600 samples (4.3%)**, across dry and rainy seasons. [S]

The 100-fold range across endemic settings is itself worth noting — "present in soil" spans two orders of magnitude of actual abundance.

### 6.2 Soil depth, type and pH

Manivanh L, Pierret A, Rattanavong S, Kounnavongsa O, Buisson Y, Elliott I, Maeght JL, Xayyathip K, Silisouk J, Vongsouvath M, Phetsouvanh R, Newton PN, Lacombe G, Ribolzi O, Rochelle-Newall E, Dance DAB. *Burkholderia pseudomallei in a lowland rice paddy: seasonal changes and influence of soil depth and physico-chemical properties.* **Sci Rep 2017;7(1):3031.** PMID 28596557; DOI 10.1038/s41598-017-02946-z. [C32]

Verbatim/near-verbatim findings [V]:
- **195/653 samples (29.7%) yielded *B. pseudomallei*.**
- **"A higher prevalence of B. pseudomallei was found at soil depths greater than the 30 cm currently recommended for B. pseudomallei environmental sampling."** Authors recommend sampling **at a soil depth of at least 60 cm**, with a **25 × 25 m grid** sufficient for detection at a given location. [V/S]
- **"B. pseudomallei was associated with a high soil water content and low total nitrogen, carbon and organic matter content."** [V]
- The study field was **relatively acidic (mean pH 4.31, range 3.38–5.58) and sandy.** [S]
- Caveat stated by the authors [S]: "Culture of B. pseudomallei in environmental samples is difficult and liable to variation, and future studies should rely on molecular approaches and address the micro-heterogeneity of soil."

**⚠️ Literature disagreement on pH — flag explicitly.** Field studies report association with **acidic** soils (mean pH 4.31 here). The global BRT model **did not** find a soil pH association, and attributed this to collinearity with soil salinity [V, C1]. These are not necessarily contradictory (a global 5 km-resolution model can miss a relationship visible in a single paddy at 60 cm depth), but a manuscript should not assert "*B. pseudomallei* is associated with acidic soils" as settled fact without noting the model's null result.

**Soil types from the global model** [V, C1]: **anthrosols** (soils profoundly modified by human activity, particularly irrigated agriculture) and **acrisols** (clay-rich tropical soils) were strongly associated with presence; also **high salinity** and **high gravel proportion**. The anthrosol association is important — it implies *B. pseudomallei* distribution is partly **anthropogenic**, and the 2016 authors explicitly predict increasing burden "fuelled by an increase in anthrosol and the marked rise in the prevalence of diabetes mellitus globally." [V]

### 6.3 Rice paddies and agricultural exposure

- Rice farming is the archetypal exposure. Working in a rice field: **cOR 2.1 (1.4–3.3)** [S, C24].
- Rice paddy soil is a documented reservoir at high prevalence (29.7%) [V, C32].
- *B. pseudomallei* has been detected in **soil and paddy rice water** in a northeast Thailand rice field **but not in air and rainwater** in that study [S] — a useful counterpoint to the aerosol hypothesis, indicating aerosolisation is not universal. (Source: PMC5805070; **PMID/DOI UNVERIFIED**.)

### 6.4 Rainfall, monsoon seasonality and severe weather

**Seasonality — the two best-quantified endemic settings:**

| Setting | Wet-season proportion | Source |
|---|---|---|
| Top End, northern Australia | **80% of infections in the wet season (November–April)** | [V, C5] |
| India | **66.9% of cases during monsoon (June–September)** | [S] |
| Northeast Thailand | Strongly seasonal, rainy-season predominant — **specific proportion UNVERIFIED** | — |

⚠️ **The brief asked for "the proportion of cases in the wet season in Australia and Thailand." I have the Australian figure verified at 80%. I did NOT find a verified equivalent percentage for Thailand.** Do not fabricate one. The Bulterys et al. Lancet Planet Health paper [C9] on climatic drivers in Laos/Cambodia is the closest regional analogue and should be read in full to supply this.

**Rainfall and severity:** see §5.2 — 14-day antecedent rainfall independently predicts pneumonia, bacteraemic pneumonia, septic shock and death [C25].

**Severe weather events:**

Merritt AJ, Inglis TJJ. *The Role of Climate in the Epidemiology of Melioidosis.* **Curr Trop Med Rep 2017;4(4):185–191.** PMID 29188170; DOI 10.1007/s40475-017-0124-4. [C33]

Key content [V/S]: high rainfall and dense cloud cover predict environmental bacterial presence and disease through soil moisture; **increased cases following storms in Taiwan and cyclones in the Australian Northern Territory**; indirect effects include bacterial output from **water seeps after heavy rain**; **Western Australia surveillance over 10 years showed cases along cyclone paths, caused by different MLST genotypes** (i.e. weather mobilises the local population rather than importing a strain).

Documented severe-weather clusters:
- **Typhoon, southern Taiwan, Jul–Sep 2005: 40 cases**, two genotypes previously present in 2000. [V, C13]
- **Typhoon Rammasun, northern Hainan, 18 July 2014: 16 confirmed cases.** [S]
- **Typhoon Kemi, Taiwan: 11 local cases**, 8 in Kaohsiung. [S]
- **Hurricane Helene (Cat 4), Georgia USA, September 2024: 2 cases**, ST41. [V, C23/C10]
- **2004 Indian Ocean tsunami, Phangnga Thailand: 6 cases** in survivors. [V, C29]

The Georgia case is notable because **3 of the 4 presumptive autochthonous cases "became ill after a severe weather event"** [V, C23] — severe weather appears to be what surfaces a cryptic environmental population.

### 6.5 The 2004 tsunami

Covered in §5.4 [C29]. The key epidemiological point: melioidosis appeared in a **non-endemic** region of Thailand because near-drowning delivered a large inoculum despite very low environmental prevalence (0.8% of soil samples). Extreme mechanical disturbance + aspiration can overcome low reservoir density.

### 6.6 Climate change projections

- **Expert consensus statement** [V, C3]: "Severe weather events and environmental disturbance are associated with increased case numbers, and it is anticipated that, in some regions, cases will increase in association with climate change."
- **Merritt & Inglis** [V/S, C33]: "Predicted temperature increases and extreme weather changes expected to alter melioidosis epidemiology."
- **Quantitative projection (animal melioidosis)** [S]: a risk-assessment modelling study reports current global animal melioidosis risk concentrated **between 30°S and 30°N**, with high-risk areas in Central America, northern South America, and eastern/southern India; under **SSP 245**, risk-expansion regions were **larger in the 2050s than in the 2070s or 2090s**; under **SSP 126**, expansion in the 2050s/2070s/2090s was comparable to current conditions. **"With future climate change, the risk regions in most countries are expected to expand, and new epidemic zones will emerge at higher northern latitudes."** Source: *"Risk Assessment of Global Animal Melioidosis Under Current and Future Climate Scenarios"*, Animals 2025;15(3):455 (PMC11815718). **PMID/DOI UNVERIFIED — retrieve before citing.**

⚠️ **Note this is a projection for *animal* melioidosis, not human, and is a model output.** I found **no** peer-reviewed quantitative projection of *human* melioidosis range expansion under climate scenarios. If the manuscript needs one, this is a genuine gap in the literature and can be stated as such — which is itself a useful Background point.

---

## 7. Travel-associated and imported cases

### 7.1 How often melioidosis appears in non-endemic countries

Norman FF, Chen LH. *Travel-associated melioidosis: a narrative review.* **J Travel Med 2023;30(3):taad039.** PMID **36971472**; DOI 10.1093/jtm/taad039. [C11]

⚠️ **PMID caution:** a WebFetch of the publisher page returned PMID 37040739, which Europe PMC shows belongs to an unrelated speech-pathology paper. **36971472 is the verified PMID.**

Findings (all **[S]** — extracted from a summarised fetch of the publisher page; **verify against the paper before citing**):
- **137 reports of travel-associated melioidosis, 2016–2022.**
- Reporting countries: **UK 55 (40%), Netherlands 28 (20%), USA 12 (9%), France 10 (7%), Qatar 7 (5%).**
- Region of exposure: **"Most patients were exposed in Asia (76.8%), mainly in Thailand (40.8%), India (8.8%), Malaysia (4.8%), Cambodia (4.8%) and Vietnam (4%)."** Americas-Caribbean 6.4%, Africa 4.8%, Oceania 1.6%.
- Outcome: **87.2% survived; 13% died.**
- Duration of travel ranged **"from 9 days among travellers to 10 years among expatriates."**

Related [S, C6]: an earlier series of **75 travel-associated cases 1982–2015** showed a similar profile with **Thailand 46%**.

**Interpretation for a Background section:** imported melioidosis is uncommon but not rare in referral centres of high-income countries, and is overwhelmingly acquired in Southeast Asia — with Thailand alone accounting for ~40–46% across two eras. The UK/Netherlands dominance in *reporting* almost certainly reflects surveillance and tropical-medicine referral infrastructure rather than true exposure distribution.

### 7.2 Latency and the exposure history — and a significant literature correction

**Timing of symptom onset relative to return** [S, C11]:
- **<1 week after return (including onset during travel): 55.4%**
- **1–12 weeks: 16.1%**
- **>12 weeks: 28.6%**

So roughly **a quarter to a third of imported cases present more than three months after return** — which is what makes the travel history easy to miss.

**The "Vietnamese time bomb" — a claim that should NOT be repeated uncritically:**

Howes M, Currie BJ. *Melioidosis and Activation from Latency: The "Time Bomb" Has Not Occurred.* **Am J Trop Med Hyg 2024;111(1):156–160.** PMID 38806042; DOI 10.4269/ajtmh.24-0007. [C34]

This paper is a direct corrective to a widely repeated Background-section trope. Findings [S — from a summarised fetch; the argument is clear but **verify exact figures**]:

- The original prediction: from serology studies of US military personnel repatriated from Southeast Asia, **"it was estimated that there were approximately 225,000 potential future melioidosis cases."**
- Actual observed rate: over the DPMS's 34 years (1989–2023), **29 of 1,148 (2.5%)** primary melioidosis diagnoses in the first 30 years were assigned as *potential* activation from latency, and only **4 of 225 (1.8%)** in the subsequent four years.
- On detailed review, three of those were reclassified as **chronic disease**, and of the remaining 25, only **20 had "strong evidence"** of genuine latency.
- **Verbatim: "activation from latency is a rare event in melioidosis, accounting in our analysis for under 3% of DPMS cases."**
- **Verbatim: "the predicted 'Vietnamese time bomb' has clearly not eventuated."**
- Many historical "reactivation" cases were actually **undiagnosed chronic melioidosis with relapsing–remitting courses**, not asymptomatic latency followed by activation.

**On the longest latent period — an important genomics point:**
- The often-quoted **62-year** latency was **"subsequently disproven by bacterial genotyping."** [S, C34]
- The longest plausible asymptomatic latency the authors accept is **29 years**, from a 1997 report of "a 50-year-old veteran who had 'enjoyed good health' for 29 years after army service in Vietnam until a diagnosis of blood culture–positive melioidosis." [S, C34]

⚠️ **CONFLICT IN THE LITERATURE — state this explicitly.** Secondary and review sources (including material surfaced in my searches) still assert *"latent periods... as long as 62 years"*. [S] **That figure has been refuted by genotyping** [C34]. A manuscript that repeats "62 years" without acknowledging [C34] would be citing a superseded claim. This is a good example of genomics overturning a long-standing epidemiological belief — thematically apt for a genomics paper.

Note also the concordant DPMS figure: **3% of the 1,148 DPMS cases were reactivation** [S, C6], matching the "<3%" of [C34].

### 7.3 Genomes used to infer where infection was acquired

This is the strongest thread for a genomics manuscript. Verified examples:

1. **ATS2021 / aromatherapy spray, USA 2021** [V, C20]. Four patient isolates and the product isolate were the same strain by WGS; the strain "clustered with samples of *B. pseudomallei* from South Asia that are consistent with the origin of the spray — India." **Genomics identified both the vehicle and the country of origin.**

2. **GCS2020 / Mississippi** [V, C22]. ST92; **>1000 SNPs from any other available genome**; groups with South American strains; clinical and environmental isolates **3–15 SNPs apart**. Genomics established (a) local acquisition, (b) a previously unsampled resident population, and (c) a probable ultimate origin in South/Central America or the Caribbean. Framed in [C10] [V] as: *"The very closely related genomes of the clinical and environmental isolates support a point-source introduction from South or Central America or the Caribbean."*

3. **ST41 / Georgia** [V, C23, C10]. Four isolates spanning **1983–2024, <20 SNPs apart**; **ST41 is of Southeast Asian origin and the closest relatives are from Vietnam**, prompting the hypothesis of introduction with returning Vietnam-War-era troops and equipment.

4. **Maryland aquarium case** [V, C10]. Traced to a freshwater home aquarium that had held imported tropical fish, "with *B. pseudomallei* genotyping supporting Southeast Asian origin." A concordant case in [C11] [S]: *"Gene sequencing of clinical isolates and aquarium samples clustered with genomes from SE Asia (Singapore and Malaysia)."*

5. **Imported iguanas** [S, C11]: *"Isolate from both iguanas matched isolate recovered from a tourist infected in Costa Rica."*

6. **The refuted 62-year latency** [S, C34] — genotyping showed the infection was not a reactivation of a decades-old exposure. Genomics used to *exclude* a claimed acquisition history.

7. **Domestic water supply, northern Australia** [V, C27] — clinical isolates 1 SNP from the environmental source strain.

**Global phylogeographic framework** [V, C10]: an **Australian origin** for *B. pseudomallei*, with "spread to Southeast Asia estimated to have occurred during the last ice age"; "from Asia to Africa estimated at two millennia ago and from Africa to the Americas in the 17th–19th centuries, potentially implicating the transatlantic slave trade." The Americas are described as **"currently the most dynamic region globally for dispersal."** Also documented: **ST562, ST46 and ST70 represent "3 separate introductions of *B. pseudomallei* from Asia to northern Australia."**

---

## 8. Under-reporting and surveillance

### 8.1 The best single quantification of under-reporting

Hantrakun V, Kongyu S, Klaytong P, Rongsumlee S, Day NPJ, Peacock SJ, Hinjoy S, Limmathurotsakul D. *Clinical Epidemiology of 7126 Melioidosis Patients in Thailand and the Implications for a National Notifiable Diseases Surveillance System.* **Open Forum Infect Dis 2019;6(12):ofz498.** PMID 32083145; DOI 10.1093/ofid/ofz498. [C35]

*(Author list beyond the first three is **[S]**.)*

Verbatim [V]:
> "A total of 7126 culture-confirmed melioidosis patients were identified from 2012 to 2015 in 60 hospitals countrywide."
> "The overall 30-day mortality was 39% (2805/7126). **Only 126 (4%) deaths were reported to the NNDSS.**"

**96% of melioidosis deaths in a country where the disease is notifiable and well-recognised went unreported to the national surveillance system.** This is the single most powerful under-reporting statistic in the corpus, and it comes from *the best-studied endemic country in the world* — which makes the implication for Nigeria, India or Laos considerably starker.

Authors' recommendation [V]: "integrating information from readily available microbiology and hospital databases could be used to generate such information, supplement NNDSS data, and support priority-setting for policy-makers in LMICs."

Corroborating [S]: a retrospective study in Songkhla and Phatthalung provinces, southern Thailand, 2014–2020, similarly found under-reporting of cases and deaths (PMC10223873; **PMID/DOI UNVERIFIED**).

### 8.2 Why case counts underestimate — mechanisms

1. **Diagnosis requires culture, and culture requires a microbiology laboratory.** In Thailand, **"more than 60% of melioidosis cases reported... are from facilities without microbiology laboratories"** [S]. Across the endemic tropics, the density of capable labs is far lower.
2. **Misidentification by automated systems.** CDC explicitly advises that "laboratorians must verify automated system identifications that may misidentify the organism" [V, C21]. *B. pseudomallei* is commonly dismissed as a contaminant or misassigned to related non-pathogenic species absent from standard diagnostic databases [S].
3. **Clinical mimicry.** Melioidosis mimics tuberculosis; in PNG and Oceania the competing burden of TB is named as a specific driver of under-recognition [V, C18].
4. **Serology is unreliable in endemic settings.** Background seropositivity from environmental exposure produces false positives [S].
5. **Reporting-system failure even when diagnosis succeeds.** The 4%-of-deaths figure above [V, C35] is a pure reporting failure, downstream of correct diagnosis.
6. **No surveillance system applied to the disease at all.** For China: "although China has established and maintained an effective communicable disease surveillance system, **it has not yet been utilized for melioidosis**. Thus, the overall incidence, social burden and epidemiological features of the disease in China remain unclear." [V, C12]
7. **Ascertainment gradients masquerade as incidence trends.** India's post-2008 rise is attributed to improved recognition and diagnostic capacity [S] — genuinely ambiguous between rising incidence and rising detection. Similarly, the 2016 model paper notes "Strengthening of microbiological laboratories and research facilities often results in the discovery of [*B. pseudomallei*] in new areas; recent national additions include India, Southern China, Brazil and Malawi." [V, C1]

### 8.3 Notifiability status by country

| Country/region | Status | Grade |
|---|---|---|
| **Australia (Northern Territory)** | **Laboratory-notifiable** | [V, C5] |
| **Thailand** | Notifiable via NNDSS — but only **4% of deaths actually reported** | [V, C35] |
| **United States** | **Nationally notifiable** following a favourable vote at the **2022 CSTE conference** | [S, C10] — CSTE detail should be verified |
| **China** | Surveillance system exists but **not applied to melioidosis** | [V, C12] |
| **India** | Not nationally notifiable; only **73 of 8,673** health centres have ever reported a case | [S] |
| Most other endemic countries | Not notifiable / status unknown | [UNVERIFIED] |

⚠️ **I could not assemble a comprehensive country-by-country notifiability table.** No such consolidated source surfaced. The rows above are what is verifiable; the brief's request for "notifiability status by country" **cannot be fully satisfied from the retrieved literature** and would require primary policy-document research per country.

### 8.4 The advocacy context

There is an active, authored campaign to have melioidosis recognised as a **WHO Neglected Tropical Disease** [V, C3]. Supporting arguments: the DALY burden exceeds that of several recognised NTDs [V, C2]; predicted mortality is comparable to measles and exceeds leptospirosis and dengue [V, C1]. Relevant advocacy papers surfaced but **not retrieved in full**: *"A call to action: time to recognise melioidosis as a neglected tropical disease"* (Lancet Infect Dis) and *"Reducing the melioidosis burden: public health, chronic disease prevention, or improved case management?"* (Lancet Infect Dis 2019) — **PMIDs/DOIs UNVERIFIED.**

---

## 9. Points where the literature disagrees — summary for the manuscript

Collected here because these are the places a Background section is most likely to go wrong.

1. **"45 countries endemic but never reported" is a conflation.** Correct: 45 endemic-but-under-reported **plus** 34 probably-endemic-never-reported. [V, C1] (§1.2)

2. **Soil pH.** Field studies find *B. pseudomallei* in acidic soils (mean pH 4.31) [C32]; the global BRT model found **no** pH association and attributed this to collinearity with salinity [C1]. Not strictly contradictory but should not be asserted as settled. (§6.2)

3. **The 62-year latency figure is refuted.** Disproven by genotyping; the defensible maximum is ~29 years, and reactivation accounts for **<3%** of cases. The "Vietnamese time bomb" (≈225,000 predicted cases) "has clearly not eventuated." [C34] Many secondary sources still repeat the 62-year claim. (§7.2)

4. **India case counts conflict** between two recent reviews (Karnataka 176 vs 499; Tamil Nadu 161 vs 210). Neither should be cited until the primaries are read. (§2.8)

5. **CDC vs NEJM register on US endemicity.** CDC HAN: melioidosis "is now considered to be locally endemic" in Gulf Coast Mississippi [C21]. NEJM authors: "may be endemic" [C22]. Currie et al. 2026 go furthest: endemic in Mississippi, "likely endemic in Georgia and Texas" despite no environmental isolates in the latter two [C10]. (§4)

6. **Route attribution is not quantitatively resolved.** Percutaneous inoculation is conventionally called the main route, but the one good case-control study supports percutaneous, inhalational and ingestion routes with overlapping CIs [C24]. No study partitions routes quantitatively. (§5.1)

7. **Birnie 2019 does not independently corroborate Limmathurotsakul 2016** — it is downstream of it and shares authors. Citing both as if they were two independent estimates overstates the evidence. (§1.4)

8. **Genomic diversity signals opposite histories in Africa vs Mississippi.** Southern Africa: high diversity among few cases → "long-term cryptic persistence" [C15]. Mississippi: 3–15 SNPs among all isolates, >1000 SNPs from anything else → recent point-source introduction of a single lineage [C22]. Same organism, opposite inferences from diversity structure.

9. **Recombination confounds *B. pseudomallei* outbreak phylogenetics.** [C28] found STs 125/126 in a single outbreak showed "multiple recombination events that were unlikely to have occurred over the timeframe of the outbreak"; the human-to-human transmission preprint reports "incorrect phylogenomic reconstruction due to polyclonality." **These are the core motivating citations for a recombination-aware SNP method.** (§5.3, §5.7)

---

## 10. Gaps and unresolved items

Items the brief asked for that I could **not** verify:

| # | Item | Status |
|---|---|---|
| 1 | **Proportion of cases in wet season in *Thailand*** | **NOT FOUND.** Australia verified at 80% [C5]; India 66.9% [S]. No verified Thai percentage. Read [C9] and Thai seasonality papers. |
| 2 | **MLST sequence type of ATS2021** (aromatherapy strain) | **NOT FOUND.** Strain name confirmed; ST not stated in retrieved text. |
| 3 | **Aromatherapy spray recall date** | **NOT FOUND.** Distribution window Feb–21 Oct 2021 [S]; recall date not in retrieved text. |
| 4 | **Mississippi environmental sample arithmetic** | **DISCREPANCY.** "188 total" vs "59 in 2020 + 109 in 2022" = 168. Verify against paper. |
| 5 | **Nosocomial melioidosis primary citation** | **NOT FOUND.** Searches returned *B. cepacia* outbreaks, a different organism. Do not conflate. |
| 6 | **Laboratory-acquired infection primary data** | **NOT RETRIEVED.** CDC MMWR Surveill Summ 2015;64(5) returned HTTP 403. Peacock et al. biosafety guidelines not retrieved. |
| 7 | **Sexual transmission primary citation** | **NOT RETRIEVED.** Only secondary description; evidence is serological only and described as speculative. |
| 8 | **Comprehensive notifiability-by-country table** | **NOT ASSEMBLABLE** from retrieved literature. Five countries documented (§8.3). |
| 9 | **Human melioidosis climate-change range projection** | **APPARENTLY DOES NOT EXIST.** Only an *animal* melioidosis SSP projection found, itself unverified. This gap is worth stating in the manuscript. |
| 10 | **India case counts** | **CONFLICTING.** Two reviews disagree; neither primary read. |
| 11 | **Middle East autochthonous transmission** | **NO EVIDENCE FOUND** beyond modelling and imported cases. |
| 12 | **Whitmore & Krishnaswami 1912 original description** | **NOT RETRIEVED.** |
| 13 | **Human-to-human transmission genomics paper** | Only a **bioRxiv preprint** (804344) found; check for peer-reviewed publication. |
| 14 | Several supporting PMIDs/DOIs | Marked UNVERIFIED inline: Myanmar soil, Taiwan hotspot 2025, Brazil Piauí series, Mozambique, Mali, bore water EID 2011, Animals 2025 climate model, NTD advocacy papers. |

---

## 11. Citation table

Verified entries had PMID and DOI confirmed via the Europe PMC REST API or the publisher/PMC full text. Entries marked ⚠ have an unverified component, specified in the notes.

| # | Role | Citation | PMID | DOI |
|---|---|---|---|---|
| C1 | **Anchor — global burden model**; 165,000 cases / 89,000 deaths; 45+34 countries; BRT suitability model; soil/climate covariates; USA & Japan suitability; Paris 1975; Tulane 2014 | Limmathurotsakul D, Golding N, Dance DAB, Messina JP, Pigott DM, Moyes CL, Rolim DB, Bertherat E, Day NPJ, Peacock SJ, Hay SI. Predicted global distribution of *Burkholderia pseudomallei* and burden of melioidosis. *Nat Microbiol.* 2016;1(1):15008. | 26877885 | 10.1038/nmicrobiol.2015.8 |
| C2 | DALY burden estimate (downstream of C1) | Birnie E, Virk HS, Savelkoel J, Spijker R, Bertherat E, Dance DAB, Limmathurotsakul D, Devleesschauwer B, Haagsma JA, Wiersinga WJ. Global burden of melioidosis in 2015: a systematic review and data synthesis. *Lancet Infect Dis.* 2019;19(8):892–902. | 31285144 | 10.1016/S1473-3099(19)30157-4 |
| C3 | **Best umbrella review**; climate change; newly recognised endemicity incl. southern USA; NTD call | Meumann EM, Limmathurotsakul D, Dunachie SJ, Wiersinga WJ, Currie BJ. *Burkholderia pseudomallei* and melioidosis. *Nat Rev Microbiol.* 2024;22(3):155–169. | 37794173 | 10.1038/s41579-023-00972-5 |
| C4 | NE Thailand incidence and trend; 3rd leading infectious cause of death | Limmathurotsakul D, Wongratanacheewin S, Teerawattanasook N, Wongsuvan G, Chaisuksant S, Chetchotisakd P, Chaowagul W, Day NPJ, Peacock SJ. Increasing incidence of human melioidosis in Northeast Thailand. *Am J Trop Med Hyg.* 2010;82(6):1113–1117. | 20519609 | 10.4269/ajtmh.2010.10-0038 |
| C5 | **Australian incidence, seasonality (80% wet season), 30-yr outcomes** | Currie BJ, Mayo M, Ward LM, et al. The Darwin Prospective Melioidosis Study: a 30-year prospective, observational investigation. *Lancet Infect Dis.* 2021;21(12):1737–1746. | 34303419 | 10.1016/S1473-3099(21)00022-0 |
| C6 | Regional case-mix roundup; travel series | Norman FF, Blair BM, Chamorro-Tojeiro S, González-Sanz M, Chen LH. The Evolving Global Epidemiology of Human Melioidosis: A Narrative Review. *Pathogens.* 2024;13(11):926. | 39599479 | 10.3390/pathogens13110926 |
| C7 | Malaysia national incidence | Arushothy R, Mohd Ali MR, Zambri HF, Muthu V, Hashim R, Chieng S, Nathan S. Assessing the national antibiotic surveillance data to identify burden for melioidosis in Malaysia. *IJID Regions.* 2024;10:94–99. | 38179416 | 10.1016/j.ijregi.2023.11.014 |
| C8 | Singapore incidence, rainfall/humidity association | Liu X, Pang L, Sim SH, Goh KT, Ravikumar S, Win MS, Tan G, Cook AR, Fisher D, Chai LYA. Association of melioidosis incidence with rainfall and humidity, Singapore, 2003–2012. *Emerg Infect Dis.* 2015;21(1):159–162. | 25531547 | 10.3201/eid2101.140042 |
| C9 | Laos/Cambodia climatic drivers | Bulterys PL, Bulterys MA, Phommasone K, et al. Climatic drivers of melioidosis in Laos and Cambodia: a 16-year case series analysis. *Lancet Planet Health.* 2018;2(8):e334–e343. | 30082048 | 10.1016/S2542-5196(18)30172-4 |
| C10 | **Global phylogeography + US endemicity synthesis**; ST41 Vietnam link; imported animals; aquarium case | Currie BJ, Kaestli M, Meumann EM. Global dispersal of *Burkholderia pseudomallei* and the evolving endemicity of melioidosis in the United States of America. *PLoS Negl Trop Dis.* 2026;20(4):e0014217. | 42030350 | 10.1371/journal.pntd.0014217 |
| C11 ⚠ | Travel-associated melioidosis review | Norman FF, Chen LH. Travel-associated melioidosis: a narrative review. *J Travel Med.* 2023;30(3):taad039. ⚠ *PMID/DOI verified; internal percentages are [S], unverified against the paper.* | 36971472 | 10.1093/jtm/taad039 |
| C12 | Southern China / Hainan / Guangxi endemicity; no surveillance applied | Zheng X, Xia Q, Xia L, Li W. Endemic Melioidosis in Southern China: Past and Present. *Trop Med Infect Dis.* 2019;4(1):39. | 30823573 | 10.3390/tropicalmed4010039 |
| C13 | Taiwan typhoon outbreak; recurring genotypes prove endemicity | Ko WC, Cheung BM, Tang HJ, Shih HI, Lau YJ, Wang LR, Chuang YC. Melioidosis outbreak after typhoon, southern Taiwan. *Emerg Infect Dis.* 2007;13(6):896–898. | 17553230 | 10.3201/eid1306.060646 |
| C14 | Africa — unrecognised burden, Nigeria top of list; WHO workshop | Birnie E, James A, Peters F, et al. Melioidosis in Africa: Time to Raise Awareness and Build Capacity for Its Detection, Diagnosis, and Treatment. *Am J Trop Med Hyg.* 2022;106(2):394–397. | 35008053 | 10.4269/ajtmh.21-0673 |
| C15 | **Southern Africa culture-confirmed cases; WGS diversity → cryptic persistence** | Rossouw J, Geyer HDW, Birkhead M, et al. Emergence of Human and Animal Melioidosis in Southern Africa, 2018–2021. *Trop Med Infect Dis.* 2026;11(2):60. | 41746030 | 10.3390/tropicalmed11020060 |
| C16 | Puerto Rico environmental isolates; Caribbean clade nested in Central/South America | Hall CM, Jaramillo S, Jimenez R, et al. *Burkholderia pseudomallei*, the causative agent of melioidosis, is rare but ecologically established and widely dispersed in the environment in Puerto Rico. *PLoS Negl Trop Dis.* 2019;13(9):e0007727. | 31487287 | 10.1371/journal.pntd.0007727 |
| C17 | Mexico / Central America / Caribbean | Sanchez-Villamil JI, Torres AG. Melioidosis in Mexico, Central America, and the Caribbean. *Trop Med Infect Dis.* 2018;3(1):24. | 29780897 | 10.3390/tropicalmed3010024 |
| C18 | PNG & Oceania; Balimo environmental isolates; New Caledonia; TB mimicry | Warner JM, Currie BJ. Melioidosis in Papua New Guinea and Oceania. *Trop Med Infect Dis.* 2018;3(1):34. | 30274431 | 10.3390/tropicalmed3010034 |
| C19 ⚠ | Asia-Pacific expanding boundaries (editorial) | Currie BJ, Meumann EM. Melioidosis in Asia-Pacific Nations: Expanding Boundaries but Unknowns Remain. *Respirology.* 2025;30(10):917–919. ⚠ *Citation verified; full text 403-blocked, content unverified.* | 40730495 | 10.1111/resp.70098 |
| C20 | **US 2021 aromatherapy outbreak; strain ATS2021; South Asian/India cluster** | Gee JE, Bower WA, Kunkel A, et al. Multistate Outbreak of Melioidosis Associated with Imported Aromatherapy Spray. *N Engl J Med.* 2022;386(9):861–868. | 35235727 | 10.1056/NEJMoa2116130 |
| C21 | **CDC conclusion on Gulf Coast Mississippi endemicity** | CDC Health Alert Network. Melioidosis Locally Endemic in Areas of the Mississippi Gulf Coast after *Burkholderia pseudomallei* Isolated in Soil and Water and Linked to Two Cases — Mississippi, 2020 and 2022. HAN Advisory 470, 27 July 2022. | n/a | n/a |
| C22 | **Mississippi 3 cases; strain GCS2020, ST92, >1000 SNPs; first continental-US environmental isolation** | Petras JK, Elrod MG, Ty MC, et al. Locally Acquired Melioidosis Linked to Environment — Mississippi, 2020–2023. *N Engl J Med.* 2023;389(25):2355–2362. | 38118023 | 10.1056/NEJMoa2306448 |
| C23 | **Georgia ST41, 1983–2024, <20 SNPs; severe weather** | Brennan S, Thompson JM, Gulvik CA, et al. Related Melioidosis Cases with Unknown Exposure Source, Georgia, USA, 1983–2024. *Emerg Infect Dis.* 2025;31(9):1802–1806. | 40835221 | 10.3201/eid3109.250804 |
| C24 ⚠ | **Route-of-exposure case-control; ORs for rice field, wounds, water, rain** | Limmathurotsakul D, Kanoksil M, Wuthiekanun V, Kitphati R, deStavola B, Day NPJ, Peacock SJ. Activities of Daily Living Associated with Acquisition of Melioidosis in Northeast Thailand: A Matched Case-Control Study. *PLoS Negl Trop Dis.* 2013;7(2):e2072. ⚠ *ORs are [S]; verify against published table.* | 23437412 | 10.1371/journal.pntd.0002072 |
| C25 | **Rainfall–severity association; inhalation hypothesis** | Currie BJ, Jacups SP. Intensity of rainfall and severity of melioidosis, Australia. *Emerg Infect Dis.* 2003;9(12):1538–1542. | 14720392 | 10.3201/eid0912.020750 |
| C26 | **Direct airborne transmission evidence; soil→aerosol→human genotype match (ST58)** | Chen PS, Chen YS, Lin HH, Liu PJ, Ni WF, Hsueh PT, Liang SH, Chen C, Chen YL. Airborne Transmission of Melioidosis to Humans from Environmental Aerosols Contaminated with *B. pseudomallei*. *PLoS Negl Trop Dis.* 2015;9(6):e0003834. | 26061639 | 10.1371/journal.pntd.0003834 |
| C27 | **WGS source attribution from domestic water supply (1 SNP); indel phylogenetics; "highly recombinogenic pathogens"** | McRobb E, Sarovich DS, Price EP, Kaestli M, Mayo M, Keim P, Currie BJ. Tracing melioidosis back to the source: using whole-genome sequencing to investigate an outbreak originating from a contaminated domestic water supply. *J Clin Microbiol.* 2015;53(4):1144–1148. | 25631791 | 10.1128/JCM.03453-14 |
| C28 | **★ Recombination confounds outbreak-timeframe inference (ST125/126); non-clonal water-source cluster** | Sarovich DS, Chapple SNJ, Price EP, Mayo M, Holden MTG, Peacock SJ, Currie BJ. Whole-genome sequencing to investigate a non-clonal melioidosis cluster on a remote Australian island. *Microb Genom.* 2017;3(8):e000117. | 29026657 | 10.1099/mgen.0.000117 |
| C29 | **2004 tsunami / near-drowning; endemic vs non-endemic soil prevalence** | Chierakul W, Winothai W, Wattanawaitunechai C, et al. Melioidosis in 6 tsunami survivors in southern Thailand. *Clin Infect Dis.* 2005;41(7):982–990. | 16142663 | 10.1086/432942 |
| C30 | **Breast-milk transmission, PFGE-confirmed** | Ralph A, McBride J, Currie BJ. Transmission of *Burkholderia pseudomallei* via breast milk in northern Australia. *Pediatr Infect Dis J.* 2004;23(12):1169–1171. | 15626961 | 10.1097/01.inf.0000145548.79395.da |
| C31 | Mother-to-child transmission | Abbink FC, Orendi JM, de Beaufort AJ. Mother-to-child transmission of *Burkholderia pseudomallei*. *N Engl J Med.* 2001;344(15):1171–1172. | 11302149 | 10.1056/NEJM200104123441516 |
| C32 | **Soil depth (>60 cm), pH 4.31, water content; rice paddy 29.7% positive** | Manivanh L, Pierret A, Rattanavong S, et al. *Burkholderia pseudomallei* in a lowland rice paddy: seasonal changes and influence of soil depth and physico-chemical properties. *Sci Rep.* 2017;7(1):3031. | 28596557 | 10.1038/s41598-017-02946-z |
| C33 | Climate role; cyclone paths, storm-associated cases | Merritt AJ, Inglis TJJ. The Role of Climate in the Epidemiology of Melioidosis. *Curr Trop Med Rep.* 2017;4(4):185–191. | 29188170 | 10.1007/s40475-017-0124-4 |
| C34 | **★ Refutes "Vietnamese time bomb"; latency <3%; 62-yr claim disproven by genotyping** | Howes M, Currie BJ. Melioidosis and Activation from Latency: The "Time Bomb" Has Not Occurred. *Am J Trop Med Hyg.* 2024;111(1):156–160. | 38806042 | 10.4269/ajtmh.24-0007 |
| C35 | **★ Under-reporting: only 4% of melioidosis deaths reached the Thai NNDSS** | Hantrakun V, Kongyu S, Klaytong P, et al. Clinical Epidemiology of 7126 Melioidosis Patients in Thailand and the Implications for a National Notifiable Diseases Surveillance System. *Open Forum Infect Dis.* 2019;6(12):ofz498. | 32083145 | 10.1093/ofid/ofz498 |
| C36 | Environmental sampling consensus methodology | Limmathurotsakul D, Dance DA, Wuthiekanun V, Kaestli M, Mayo M, Warner J, Wagner DM, Tuanyok A, Wertheim H, Yoke Cheng T, Mukhopadhyay C, Puthucheary S, Day NP, Steinmetz I, Currie BJ, Peacock SJ. Systematic review and consensus guidelines for environmental sampling of *Burkholderia pseudomallei*. *PLoS Negl Trop Dis.* 2013;7(3):e2105. | 23556010 | 10.1371/journal.pntd.0002105 |

★ = highest-value citations for a *recombination-aware SNP* manuscript specifically.

---

## 12. Suggested next retrievals

To close the gaps in §10, retrieve in full:
1. [C9] Bulterys et al. — for Thai/Lao/Cambodian wet-season proportions.
2. [C24] — verify the OR table.
3. [C11] — verify the travel percentages.
4. PMC12874796 and PMC12030058 — resolve the India case-count conflict.
5. MMWR Surveill Summ 2015;64(5) — laboratory/occupational exposures (try stacks.cdc.gov, which was reachable, rather than cdc.gov/mmwr which 403s).
6. The bioRxiv human-to-human/polyclonality preprint — check for peer-reviewed publication.
7. A primary citation for nosocomial melioidosis, and for the sexual-transmission case report.
