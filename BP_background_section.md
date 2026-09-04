# Background for: Genomic Attribution of Exposure Country in *Burkholderia pseudomallei*

## A Comprehensive Literature Review on Melioidosis, Its Epidemiology, and the Genomic Characteristics of *Burkholderia pseudomallei*

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Melioidosis: Disease Overview and Clinical Spectrum](#2-melioidosis-disease-overview-and-clinical-spectrum)
   - 2.1 [Historical Context and Neglected Tropical Disease Status](#21-historical-context-and-neglected-tropical-disease-status)
   - 2.2 [Clinical Manifestations](#22-clinical-manifestations)
   - 2.3 [Risk Factors and Host Susceptibility](#23-risk-factors-and-host-susceptibility)
   - 2.4 [Diagnosis and Treatment](#24-diagnosis-and-treatment)
3. [Global Epidemiology and Geographic Distribution](#3-global-epidemiology-and-geographic-distribution)
   - 3.1 [Estimated Global Burden](#31-estimated-global-burden)
   - 3.2 [Endemic Regions](#32-endemic-regions)
   - 3.3 [Emerging and Underrecognised Regions](#33-emerging-and-underrecognised-regions)
   - 3.4 [Travel-Associated Melioidosis](#34-travel-associated-melioidosis)
4. [Environmental Reservoir and Modes of Transmission](#4-environmental-reservoir-and-modes-of-transmission)
   - 4.1 [Soil and Water as Reservoirs](#41-soil-and-water-as-reservoirs)
   - 4.2 [Routes of Infection](#42-routes-of-infection)
   - 4.3 [Seasonality and Environmental Drivers](#43-seasonality-and-environmental-drivers)
   - 4.4 [Climate Change and Geographic Range Expansion](#44-climate-change-and-geographic-range-expansion)
5. [Genomic Characteristics of *Burkholderia pseudomallei*](#5-genomic-characteristics-of-burkholderia-pseudomallei)
   - 5.1 [Genome Architecture: The Bipartite Chromosome](#51-genome-architecture-the-bipartite-chromosome)
   - 5.2 [Genomic Islands and Accessory Genome](#52-genomic-islands-and-accessory-genome)
   - 5.3 [Pan-Genome and Core Genome](#53-pan-genome-and-core-genome)
   - 5.4 [Recombination: A Dominant Force in Evolution](#54-recombination-a-dominant-force-in-evolution)
   - 5.5 [Virulence Genomics and Comparative Genomics with Relatives](#55-virulence-genomics-and-comparative-genomics-with-relatives)
6. [Population Structure, Phylogeography, and Comparative Genomics](#6-population-structure-phylogeography-and-comparative-genomics)
   - 6.1 [Global Population Structure and Biogeographic Separation](#61-global-population-structure-and-biogeographic-separation)
   - 6.2 [Australian Origin and Dispersal to Asia and Beyond](#62-australian-origin-and-dispersal-to-asia-and-beyond)
   - 6.3 [Regional Diversity and Fine-Scale Population Structure](#63-regional-diversity-and-fine-scale-population-structure)
   - 6.4 [Genomic Clades and Lineage Diversity](#64-genomic-clades-and-lineage-diversity)
7. [Molecular Typing Methods: From MLST to Whole-Genome Sequencing](#7-molecular-typing-methods-from-mlst-to-whole-genome-sequencing)
   - 7.1 [Multilocus Sequence Typing (MLST)](#71-multilocus-sequence-typing-mlst)
   - 7.2 [Limitations of MLST: Homoplasy and Recombination](#72-limitations-of-mlst-homoplasy-and-recombination)
   - 7.3 [Whole-Genome Sequencing and Core-Genome MLST](#73-whole-genome-sequencing-and-core-genome-mlst)
   - 7.4 [Source Attribution and Outbreak Investigation by WGS](#74-source-attribution-and-outbreak-investigation-by-wgs)
8. [The Challenge of Geographic Attribution](#8-the-challenge-of-geographic-attribution)
9. [Conclusion](#9-conclusion)

---

## 1. Introduction

Melioidosis, the disease caused by the Gram-negative environmental bacterium *Burkholderia pseudomallei*, represents one of the most consequential yet underappreciated infectious diseases of the tropical world. Despite carrying a case fatality rate that rivals that of many high-profile pathogens, melioidosis has long been overshadowed by better-resourced diseases, and its true global burden has only recently begun to be appreciated [32], [46]. The pathogen occupies a unique ecological niche as a soil and water saprophyte, persisting in the environment of tropical and subtropical regions and infecting humans and animals through percutaneous inoculation, inhalation, or ingestion [3], [34]. The resulting disease is protean in its clinical expression, ranging from localised skin infection to fulminant septicaemia with multi-organ abscesses, and is further complicated by the capacity for latency and reactivation years or even decades after initial exposure [3], [16].

The genomic biology of *B. pseudomallei* is equally complex. Its large bipartite genome, extraordinary recombination rate, extensive accessory genome, and globally structured yet locally diverse population make it a fascinating subject for comparative genomics [68], [79]. These same features, however, create substantial challenges for molecular epidemiology. The high recombination rate erodes phylogenetic signal, shared multilocus sequence types (STs) can arise independently in geographically distant populations through homoplasy, and the uneven global distribution of sequenced genomes leaves large regions of endemicity genomically uncharacterised [85], [91]. Understanding whether the genome of a clinical isolate can reliably reveal the geographic origin of infection — a question of direct clinical and public health relevance for travel-associated cases — requires a thorough grounding in both the epidemiology of the disease and the genomic architecture of its causative agent. This background review synthesises the current state of knowledge across these domains to contextualise the question of genomic exposure-country attribution.

---

## 2. Melioidosis: Disease Overview and Clinical Spectrum

### 2.1 Historical Context and Neglected Tropical Disease Status

*Burkholderia pseudomallei* was first described by Alfred Whitmore in Rangoon in 1912, and the disease it causes — melioidosis — has since been recognised as a significant cause of morbidity and mortality across the tropics [10], [34]. Despite this long history, melioidosis has only recently been formally proposed for inclusion on the World Health Organization's list of neglected tropical diseases (NTDs), a designation that reflects both its disproportionate impact on impoverished populations and the chronic underfunding of research and diagnostic capacity in endemic regions [47], [48]. The pathogen is also classified as a Tier 1 select agent by the US Centers for Disease Control and Prevention due to its potential for weaponisation, a status that has driven some genomic research but has also complicated the open sharing of isolates and sequence data [59].

The neglected status of melioidosis is perpetuated by a cycle of underdiagnosis and underreporting [7]. In many endemic countries, clinical laboratories lack the expertise or resources to reliably identify *B. pseudomallei*, which can be misidentified as other Gram-negative organisms [1], [56]. The result is that the true incidence of melioidosis is almost certainly far higher than reported case counts suggest, and the global map of endemicity remains incomplete [32], [54].

### 2.2 Clinical Manifestations

Melioidosis is characterised by remarkable clinical diversity. The most common presentation is pneumonia, which accounts for approximately 50% of cases in prospective studies from northern Australia and is often severe, with lobar consolidation, cavitation, and a predilection for the upper lobes that can mimic tuberculosis [16], [21]. Bacteraemia occurs in the majority of hospitalised patients and is associated with high mortality; septic shock develops in approximately 20% of cases [16], [34]. Beyond pulmonary disease, *B. pseudomallei* can cause genitourinary infection (including prostatic abscesses, which are a distinctive feature of melioidosis in males), septic arthritis, osteomyelitis, skin and soft tissue infection, neurological melioidosis, and internal organ abscesses involving the liver, spleen, and kidneys [16], [58]. Paediatric melioidosis has a somewhat different clinical profile, with a higher proportion of suppurative parotitis and skin infections relative to adults [36].

A particularly important clinical feature is the capacity for latency. *B. pseudomallei* can persist in a dormant state for years or decades following initial infection, with reactivation triggered by immunosuppression, intercurrent illness, or other stressors [3], [35]. This has been documented in veterans of conflicts in Southeast Asia who developed melioidosis decades after their last potential exposure, and it creates a diagnostic challenge when patients present without a clear recent travel history to an endemic region [14], [21]. Case fatality rates vary widely by region and healthcare setting, from approximately 9–14% in well-resourced Australian centres to 40% or higher in parts of Southeast Asia where intensive care capacity is limited [16], [18], [26].

### 2.3 Risk Factors and Host Susceptibility

The epidemiology of melioidosis is strongly shaped by host susceptibility. Diabetes mellitus is the single most important risk factor, present in approximately 39–50% of cases in most series, and diabetics face an estimated 13-fold increased risk of melioidosis compared to the general population [8], [17]. Other major risk factors include hazardous alcohol use, chronic renal disease, chronic lung disease, and immunosuppression from any cause [16], [17], [34]. In the Darwin prospective study, 81% of fatal cases had at least one identifiable risk factor, and the two deaths in individuals without risk factors were both elderly [16]. Occupational and recreational exposure to soil and water — particularly in agricultural workers, construction workers, and those who walk barefoot in endemic areas — is also a significant determinant of risk [2], [23].

Demographic factors modulate risk independently of comorbidities. In northern Australia, Aboriginal and Torres Strait Islander people bear a disproportionate burden of disease, comprising 59% of cases in Far North Queensland despite representing only 9% of the regional population, and experiencing higher case fatality rates than non-Indigenous patients [15]. Male sex and age ≥45 years are independent risk factors in Australian cohorts [17]. In South and Southeast Asia, farming communities and those with occupational soil exposure are particularly affected [11], [27]. Notably, approximately 20% of cases occur in individuals with no identifiable risk factor, confirming that healthy individuals can also develop melioidosis, particularly following high-inoculum exposures [16].

### 2.4 Diagnosis and Treatment

Definitive diagnosis requires culture of *B. pseudomallei* from blood, sputum, urine, pus, or other clinical specimens [39], [60]. The organism grows on standard laboratory media but requires familiarity for correct identification, as it can be misidentified as *Pseudomonas* or *Chromobacterium* species by laboratories without experience [1], [56]. Serological tests have limited utility in endemic regions due to high background seropositivity, and molecular methods including PCR are increasingly used but not yet universally available [9], [39].

Treatment follows a two-phase approach: an intensive intravenous phase using ceftazidime or meropenem for at least 10–14 days, followed by an oral eradication phase with trimethoprim-sulfamethoxazole for a minimum of three months [60]. Adherence to the full eradication course is critical, as inadequate treatment is the principal cause of relapse, which occurs in approximately 7–13% of cases [15], [16]. *B. pseudomallei* is intrinsically resistant to many antibiotics including penicillin, ampicillin, first- and second-generation cephalosporins, and aminoglycosides, a feature that reflects its environmental lifestyle and the selective pressures of its ecological niche [10], [33].

Beyond intrinsic resistance, acquired and treatment-emergent resistance poses an increasingly recognised clinical challenge. Ceftazidime resistance arising during treatment has been attributed to multiple distinct mechanisms: structural mutations in the β-lactamase PenA (including P167S, C69Y, A172T, and P174L) that expand its substrate specificity [104]; constitutive overexpression of PenA through promoter mutations in the *nlpD1–penA* intergenic region without any structural change to the enzyme [105]; and reversible gene duplication or amplification of *penA*, whose copy number correlates directly with minimum inhibitory concentration [106]. A further mechanism — deletion of the gene encoding penicillin-binding protein 3 (*bpss1219*) — generates slow-growing or non-growing variants with high-level ceftazidime resistance that risk diagnostic failure on routine subculture [107]. Meropenem resistance emerging during treatment has been documented in a series of eleven paired clinical isolates and is driven principally by loss-of-function mutations in efflux pump regulators (*amrR*, *bpeT*), causing upregulation of AmrAB-OprA and BpeB-OprB; patients harbouring resistant isolates experienced significantly worse outcomes [108]. BpeEF-OprC upregulation confers trimethoprim-sulfamethoxazole resistance that can be phenotypically transient — disappearing on subculture — yet co-selects multidrug-resistant phenotypes in serial isolate pairs [109]. Whole-genome sequencing-based tools have been developed to detect these mechanisms systematically: ARDaP identifies resistance-conferring variants from short-read data in mixed clinical populations [110], and a triplex RT-qPCR assay can rapidly quantify expression of *amrB*, *bpeB*, and *bpeF* to detect emergent efflux upregulation directly from paired clinical isolates [111].

---

## 3. Global Epidemiology and Geographic Distribution

### 3.1 Estimated Global Burden

The global burden of melioidosis has been substantially revised upward in recent years. A landmark modelling study by Limmathurotsakul et al. estimated that 165,000 cases of human melioidosis occur annually worldwide, resulting in approximately 89,000 deaths — a mortality burden comparable to that of measles or leptospirosis [32]. A subsequent systematic review estimated 168,000 cases and 89,000 deaths per year, with 89% of cases occurring in low- and middle-income countries [46]. These estimates are based on environmental suitability modelling combined with case data from countries with established surveillance, and they almost certainly underestimate the true burden given the widespread underdiagnosis of the disease [56]. The same modelling distinguished countries where *B. pseudomallei* is known to be endemic but under-reported (45 countries) from those where it is probably endemic but has never reported a single case (a further 34 countries), a priority list of 79 in total, while the underlying suitability model predicted an even broader potential range. The gap between predicted and reported endemicity implies that large numbers of cases are being missed entirely [32].

### 3.2 Endemic Regions

The core endemic regions for melioidosis are Southeast Asia and northern Australia, which together account for the majority of reported cases and the most detailed epidemiological data [3], [43]. In Southeast Asia, Thailand has the highest reported incidence, with melioidosis accounting for approximately 20% of community-acquired septicaemias in the northeast of the country [68]. Significant burdens are also documented in Laos, Cambodia, Vietnam, Malaysia, Singapore, Myanmar, and Indonesia [20], [27], [50]. In Australia, the disease is concentrated in the tropical north, particularly the Northern Territory and Far North Queensland, where annual incidence rates of approximately 20 cases per 100,000 population have been recorded in the Top End [17], [26].

South Asia, particularly India, has emerged as a major focus of melioidosis in recent decades. India is now estimated to account for the largest share of the global burden, with modelling suggesting over 44,000 cases annually, though reported case counts remain far lower due to diagnostic limitations [4], [24]. Cases are concentrated in the coastal states of Kerala, Karnataka, and Goa, as well as in Odisha and other regions with suitable environmental conditions [2], [28]. Bangladesh, Sri Lanka, Nepal, and Pakistan also report cases, though surveillance capacity varies considerably [24].

### 3.3 Emerging and Underrecognised Regions

Beyond the traditional endemic zones, melioidosis is increasingly recognised in regions previously considered non-endemic. In Africa, serological surveys and case reports have documented *B. pseudomallei* exposure and disease in multiple countries, and phylogenomic analysis has confirmed that African strains are genuinely endemic rather than imported [41], [57]. A population-based study in Kenya estimated an incidence of 3.6 cases per 100,000 population, suggesting a substantial unrecognised burden [52]. Serological evidence of exposure has also been reported from Nigeria [55]. In the Americas, melioidosis is endemic in Brazil (particularly the state of Ceará), and cases have been reported from multiple Caribbean and Central American countries, as well as from the southern United States [62], [67], [87]. A locally acquired case in Arizona, USA, and the documented presence of *B. pseudomallei* in Puerto Rico, confirm that the organism's range extends into North America [88]. Most strikingly, a cluster of five locally acquired cases from the Mississippi Gulf Coast, USA, reported in 2022–2023, confirmed an established environmental reservoir of *B. pseudomallei* within the continental United States — the most compelling evidence to date of autochthonous transmission on the US mainland [101]. A separate investigation of four patients in Georgia, USA, with disease episodes spanning 1983–2024 and no documented international travel identified a further presumptive autochthonous focus, suggesting that the continental US environmental reservoir extends beyond a single Gulf Coast hotspot [103]. The Middle East, Central Asia, and parts of the Pacific also harbour endemic foci [5], [12].

The recognition of these emerging regions has important implications for clinical practice: clinicians in non-endemic countries must maintain awareness of melioidosis as a diagnostic possibility in patients with relevant travel histories or in those with unexplained sepsis from endemic regions [14], [31].

### 3.4 Travel-Associated Melioidosis

Travel-associated melioidosis — cases diagnosed in individuals who acquired infection while visiting an endemic country — represents a clinically important and epidemiologically informative subset of the global case burden [14]. Travellers can act as sentinels of disease activity in regions with limited surveillance capacity, and the documentation of imported cases has contributed to the recognition of endemicity in previously uncharacterised areas [14]. The clinical presentation of travel-associated melioidosis does not differ substantially from that in endemic populations, but the diagnosis is frequently delayed because clinicians in non-endemic countries may not consider it [5], [12]. Latency further complicates the picture: cases have been documented in individuals who visited an endemic region years or even decades before presentation, making the attribution of exposure country challenging on clinical grounds alone [14], [21].

The question of exposure-country attribution is not merely academic. For travel-associated cases, identifying the likely country of acquisition has implications for contact tracing, public health notification, and the recognition of new endemic foci. It also has medicolegal relevance in occupational exposure cases. Genomic approaches offer a potential route to answering this question, but their utility depends critically on the genomic structure of *B. pseudomallei* populations and the availability of representative reference genomes from all potential source countries.

---

## 4. Environmental Reservoir and Modes of Transmission

### 4.1 Soil and Water as Reservoirs

*Burkholderia pseudomallei* is a saprophytic organism that persists in tropical and subtropical soils and surface waters, where it can survive for extended periods under a wide range of environmental conditions [3], [34]. The organism is found predominantly in the upper layers of soil (0–30 cm depth), though it has been detected at depths of up to 300 cm, with concentration declining with depth [61]. Its distribution within the soil is heterogeneous, with higher concentrations in moist, clay-rich soils and in areas subject to agricultural disturbance [49], [98]. In Thailand, environmental surveys have demonstrated that *B. pseudomallei* is present in the majority of soil samples from rice paddies and agricultural land in endemic areas, and that its concentration in soil and water varies seasonally [42], [98].

The organism has also been detected in surface water, rivers, and domestic water supplies, and waterborne transmission has been documented in outbreak settings [2], [49]. Ornamental fish tanks have been identified as an unusual environmental reservoir in Laos [45]. The persistence of *B. pseudomallei* in water is facilitated by its ability to form biofilms, which enhance survival under adverse conditions [63].

### 4.2 Routes of Infection

Three principal routes of infection are recognised: percutaneous inoculation, inhalation, and ingestion, with percutaneous inoculation being the most common in most settings [3], [34]. Inoculation typically occurs through skin abrasions or wounds during contact with contaminated soil or water, and is particularly associated with agricultural work, gardening, and outdoor activities in endemic areas [2], [40]. The seasonal peak of melioidosis during the monsoon season is consistent with increased environmental exposure through flooding and soil disturbance [16], [17].

Inhalation of contaminated aerosols or dust is an important route of infection, particularly during severe weather events such as tropical cyclones and dust storms, which can aerosolise *B. pseudomallei* from soil [19], [44]. A study in Taiwan demonstrated a molecular link between soil, aerosol, and human isolates, confirming airborne transmission in an endemic area [19]. In an urban setting, a cluster of melioidosis cases in Hong Kong following Typhoon Mangkhut was similarly attributed to aerosolisation, with core-genome MLST analysis directly linking an aerosol-derived *B. pseudomallei* isolate to the clinical cases and providing definitive molecular evidence for typhoon-associated airborne transmission [130]. The higher proportion of pneumonia cases during the peak of the monsoon season in Darwin supports the hypothesis that inhalation is a significant route during severe weather [16]. Ingestion of contaminated water or food is a less well-characterised route but has been implicated in some outbreak investigations [2].

Human-to-human transmission is extremely rare and has been documented only in exceptional circumstances, including a single confirmed case of sexual transmission and rare nosocomial events [93]. The organism is not considered to spread efficiently between humans under normal circumstances, and melioidosis is not a notifiable disease in most countries on the basis of person-to-person transmission risk.

### 4.3 Seasonality and Environmental Drivers

Melioidosis exhibits a striking seasonal pattern in most endemic regions, with the majority of cases occurring during or immediately after the wet season [16], [17]. In Darwin, 81% of cases present during the monsoonal wet season (October to April), and in Far North Queensland, 78% of cases occur between December and April [15], [16]. This seasonality reflects both increased environmental exposure through flooding and soil disturbance and, potentially, increased aerosolisation of the organism during heavy rainfall and high winds [6], [13]. Modelling studies have confirmed that rainfall, temperature, and soil moisture are significant predictors of melioidosis incidence at the population level [6], [22].

Land use and land cover are also important determinants of *B. pseudomallei* distribution and melioidosis risk. Studies in Malaysia and Thailand have shown that disease risk increases with the degree of human modification of natural ecosystems, and that proximity to rice paddies, construction sites, and disturbed soils is associated with elevated risk [23], [37]. Climate change is expected to alter the geographic range and seasonal dynamics of melioidosis by shifting the distribution of suitable environmental conditions for *B. pseudomallei* persistence [29].

### 4.4 Climate Change and Geographic Range Expansion

Accumulating evidence indicates that *B. pseudomallei* environmental abundance and human exposure are acutely sensitive to rainfall and flooding events. In Townsville, Australia, fortnightly rainfall exceeding 200 mm was associated with approximately threefold higher melioidosis incidence compared with drier periods [115], and a 14-case outbreak in southern Queensland following La Niña-associated flooding confirmed that extreme inundation events can activate environmental reservoirs outside the recognised core endemic zone [112]. In Vietnamese paddy fields, *B. pseudomallei* culture positivity rose from 5% in the cold dry season to 82% in the hot wet season (Spearman's ρ = 0.905), demonstrating that temperature and soil moisture interactively drive environmental bacterial load [116]. Taiwan's 2024 typhoon season triggered an unprecedented surge in melioidosis notifications, reinforcing the link between tropical cyclone activity and acute exposure risk [117]. Long-term soil surveillance in Taiwan further documented an increase in *B. pseudomallei* PCR positivity from 77.7% to 97.4% following heavy rainfall events, consistent with an acute environmental amplification effect [114].

*Burkholderia pseudomallei* is not strictly confined to the tropics. An established focus in the temperate southwest of Western Australia (latitude 31.6°S) has persisted for over five decades, with clinical episodes clustering after heavy rainfall, demonstrating that environmental reservoirs can be maintained well beyond the recognised tropical endemic zone [113]. These observations align with ecological niche modelling studies: MaxEnt analyses of the Southeast Asian distribution identify a thermal threshold of approximately 26°C in the wettest quarter as the principal environmental constraint on habitat suitability [119], while global projections under future climate scenarios consistently predict poleward expansion of the suitable habitat envelope as temperature isotherms shift [118]. Narrative reviews of the drivers of melioidosis endemicity and the disease's expanding global footprint reach concordant conclusions: climate warming, increased tropical cyclone intensity, and land-use change are expected to increase both the geographic range and the seasonal magnitude of melioidosis risk [120], [121], [122].

These projections have direct implications for geographic attribution. Range expansion into novel temperate and subtropical regions will generate locally acquired cases in areas currently lacking any representative genomes in public databases, widening the reference database gap that represents one of the principal limitations of genomic attribution approaches.

---

## 5. Genomic Characteristics of *Burkholderia pseudomallei*

### 5.1 Genome Architecture: The Bipartite Chromosome

The genome of *B. pseudomallei* is one of the most distinctive features of this organism and sets it apart from most other bacterial pathogens. The complete genome of the reference strain K96243, first reported by Holden et al. in 2004, consists of two circular chromosomes: a large chromosome of approximately 4.07 megabase pairs (Mb) and a smaller chromosome of approximately 3.17 Mb, giving a total genome size of approximately 7.24 Mb [68]. This bipartite architecture is shared with other members of the *Burkholderia* genus but is unusual among bacterial pathogens more broadly [94], [96].

The two chromosomes show significant functional partitioning. The large chromosome encodes the majority of core metabolic functions, including central metabolism, cell growth, and essential housekeeping genes, and shows greater gene order conservation and a higher proportion of orthologous genes when compared to related species [68]. The small chromosome, by contrast, carries a higher proportion of accessory functions associated with adaptation to diverse environmental niches, including genes involved in secondary metabolism, transport, and stress responses [68], [77]. This functional division has been interpreted as reflecting the distinct evolutionary origins of the two replicons, with the small chromosome potentially derived from a megaplasmid ancestor [68], [96].

The genome encodes a large and diverse repertoire of virulence-associated genes, including multiple type III and type VI secretion systems, flagella, capsular polysaccharide biosynthesis loci, lipopolysaccharide biosynthesis genes, and a range of toxins and effector proteins [58], [64]. Comparative genomic analysis with the closely related but avirulent species *Burkholderia thailandensis* has been particularly informative in identifying genomic features that distinguish the pathogenic *B. pseudomallei* from its environmental relatives [77].

### 5.2 Genomic Islands and Accessory Genome

A striking feature of the *B. pseudomallei* genome is the presence of multiple genomic islands (GIs) — regions of horizontally acquired DNA that are variably present across isolates and that together constitute a significant fraction of the total genome [68], [78]. The reference strain K96243 contains 16 genomic islands that together account for approximately 6.1% of the genome [68]. These islands encode a broad array of functions, including metabolic capabilities, resistance determinants, mobile genetic elements, and putative virulence factors [68], [78].

The distribution of genomic islands is highly variable across *B. pseudomallei* isolates. Studies using multiplex PCR screening of large collections of clinical and environmental isolates from Thailand have shown that the proportion of isolates carrying individual GIs ranges from approximately 12% to 76%, and that the cumulative number of GIs per isolate ranges from 0 to 5 [78]. Importantly, the presence of GIs does not differ significantly between clinical and environmental isolates, suggesting that GI carriage alone is not a reliable predictor of virulence or disease association [78]. The rapid gain and loss of GIs within individual clones, as evidenced by variation among isolates of the same sequence type, underscores the dynamic nature of the *B. pseudomallei* accessory genome [78].

Genomic islands are hotspots for recombination, particularly site-specific recombination associated with tRNA genes, which serve as integration sites for mobile elements [79]. This localised recombination at GI insertion sites contributes to the overall genomic plasticity of *B. pseudomallei* and facilitates the rapid acquisition of new functional capabilities [79].

### 5.3 Pan-Genome and Core Genome

Pan-genome analysis of *B. pseudomallei* has revealed an open pan-genome, meaning that each new genome sequenced contributes novel genes not found in previously characterised strains [79]. Analysis of 37 isolates estimated that approximately 136 new genes are identified with each additional genome sequenced, and that the global core genome — genes present in all isolates — consists of approximately 4,568 homologs [79]. Genes associated with metabolism are statistically overrepresented in the core genome, while genes associated with mobile elements, disease, and motility are primarily found in the accessory portions of the pan-genome [79].

The open nature of the pan-genome reflects the environmental lifestyle of *B. pseudomallei* and its capacity to acquire genetic material from diverse sources through horizontal gene transfer. The accessory genome encodes functions that may confer advantages in specific ecological contexts, including resistance to antimicrobials, heavy metals, and environmental stresses, as well as novel metabolic capabilities [51], [86]. The distinction between core and accessory genome is also relevant for molecular typing: typing schemes based on core genome loci are more stable and reproducible than those based on accessory elements, but may miss epidemiologically relevant variation in the accessory genome [79].

### 5.4 Recombination: A Dominant Force in Evolution

Perhaps the most consequential genomic feature of *B. pseudomallei* for molecular epidemiology is its extraordinarily high rate of homologous recombination. Comparative analyses of recombination rates across bacterial species have consistently placed *B. pseudomallei* at or near the top of the distribution. The most-cited figure, a per-allele ratio of recombination to mutation (r/m) among the highest reported for any bacterium, comes from multilocus sequence typing: it measures how often a whole housekeeping allele is replaced by recombination rather than by point mutation across seven loci, and was estimated at roughly 18 to 30 for this species. That per-allele quantity is not on the same scale as the genome-wide, per-site r/m estimated by later whole-genome studies, which is roughly an order of magnitude lower; the two must not be quoted interchangeably. On either measure the species is exceptionally recombinogenic [81]. In practical terms, this means that the majority of nucleotide diversity in *B. pseudomallei* populations is generated by recombination rather than point mutation, and that phylogenetic reconstruction based on raw sequence data without recombination correction will be severely distorted [67], [81].

The consequences of high recombination for molecular epidemiology are profound. Recombination can generate identical multilocus sequence types (STs) in geographically distant and phylogenetically unrelated isolates through the independent acquisition of the same alleles — a phenomenon known as homoplasy [85], [91]. It can also obscure the phylogenetic signal that would otherwise allow the geographic origin of an isolate to be inferred from its genome sequence [81]. Studies of *B. pseudomallei* populations in Brazil found that 59% of core SNPs were attributable to recombination, underscoring the importance of recombination removal prior to phylogenetic analysis [67]. In northeast Thailand, recombination was found to drive lineage-specific gene flow and to shape the genomic diversity of dominant lineages [80]. Whole-genome sequencing studies have confirmed that recombination events can occur over very short timescales within individual clones, generating genomic diversity that is not captured by MLST [69].

Despite this high recombination rate, gene order is remarkably well conserved across *B. pseudomallei* genomes, a finding that initially appears paradoxical [79]. Pan-genome analysis has resolved this apparent contradiction by demonstrating that recombination is highly localised to specific genomic sites (particularly GI insertion sites) and that recombination throughout the rest of the genome is characterised by symmetrical gene gain and loss that preserves overall synteny [79].

### 5.5 Virulence Genomics and Comparative Genomics with Relatives

Comparative genomics has been central to understanding the virulence biology of *B. pseudomallei*. Comparison with the closely related but avirulent *B. thailandensis* has identified genomic features unique to *B. pseudomallei* that are likely to contribute to its pathogenicity, including the presence of specific type III secretion system effectors, capsular polysaccharide loci, and other virulence-associated genes [77]. Comparison of multiple *B. pseudomallei* strains with differential virulence in animal models has identified genomic regions — including variants of the type VI secretion system component Hcp1 — that may contribute to attenuation [65], [84].

Differential virulence among *B. pseudomallei* isolates is a well-recognised phenomenon. Studies comparing strains from different geographic regions have identified geographically restricted virulence-associated genes, providing a potential explanation for the observation that clinical manifestations of melioidosis differ between regions [30], [70]. For example, the *bimA* gene, which encodes a factor involved in actin-based motility and is associated with neurological melioidosis, exists in distinct variants (*bimA*Bp and *bimA*Bm) that are differentially distributed across Australian and Asian lineages [70]. The genomic basis of differential virulence remains an active area of research, with genome-wide association studies beginning to identify specific loci associated with clinical outcomes and with phenotypic differences between clinical and environmental isolates [89], [126].

---

## 6. Population Structure, Phylogeography, and Comparative Genomics

### 6.1 Global Population Structure and Biogeographic Separation

One of the most important findings from comparative genomics of *B. pseudomallei* is the existence of a robust biogeographic signal in the genome, despite the high recombination rate. Multiple independent studies using MLST and whole-genome sequencing have identified two major global populations that correspond broadly to the two principal endemic regions: Australia and Southeast Asia [75], [81]. These populations are separated along Wallace's Line — the biogeographic boundary between the Australian and Asian faunal regions — a pattern that mirrors the distribution of many plant and animal species and reflects the deep evolutionary history of the organism [21], [81].

The separation between Australian and Asian populations is sufficiently robust that population assignment of individual isolates to one of these two groups can be achieved with high accuracy using MLST data alone [75]. However, within each major population, there is substantial further structure, with regional subpopulations identifiable at finer geographic scales [83], [98]. The existence of this biogeographic signal is the foundation for the hypothesis that genomic data might be used to infer the geographic origin of clinical isolates, including those from travel-associated cases.

### 6.2 Australian Origin and Dispersal to Asia and Beyond

Phylogenomic analyses have consistently supported an Australian origin for *B. pseudomallei*, with subsequent dispersal to Southeast Asia followed by onward transmission to South Asia, East Asia, Africa, and the Americas [30], [81]. The most comprehensive analysis to date, using 469 whole-genome sequences from 30 countries collected over 79 years, reconstructed a pattern of global dissemination in which Australia served as the ancestral reservoir, with a single major introduction event into Southeast Asia during a recent glacial period when land bridges connected Australia and New Guinea to the Asian mainland [30], [81]. These reconstructions are explicitly contingent on the position of the tree's root: Pearson and colleagues described their Australian-root conclusion as provisional, and later work has noted that a population bottleneck outside Australia could produce a comparable signal, so an Australian origin is well supported but not settled.

From Southeast Asia, *B. pseudomallei* spread to South Asia and East Asia, with repeated reintroductions observed within the Malay Peninsula and between countries bordering the Mekong River [30]. Although most globally distributed sequence types have Australasian roots, the same sequence type can be recovered on more than one continent. ST562 has been identified in both northern Australia and southern China, but the Australian isolates and those from Hainan and Taiwan are only distantly related, and the direction and mode of introduction remain unresolved (Meumann et al., PMID 33754984). The correct reading is therefore not that a lineage is shared between continents but that a shared sequence type is by itself weak evidence of shared origin, which is a limitation of ST-level inference. The same limitation appears within a single patient: twelve isolates carrying an identical sequence type resolved into a polyclonal infection on whole-genome data (PMID 25339397). The African and South American populations appear to share a common origin, with phylogenomic evidence placing South American isolates within the African clade and so supporting an African origin for Central and South American isolates [30], [74]. The mechanism and timing are not settled. Sarovich and colleagues, whose analysis of Madagascan and Burkinabe isolates established this relationship, report an *Asian* origin for the African isolates themselves and propose anthropogenic dispersal associated with Austronesian migration from Indonesian Borneo to Madagascar roughly 2,000 years ago (PMID 27303718). An earlier version of this section attached the relationship to the transatlantic slave trade with an estimated introduction between 1650 and 1850; that claim does not appear in the cited work and has been removed pending a source that makes it. The Australasian distribution of *B. pseudomallei* is further shaped by paleogeographic history, with isolates from New Guinea and the Torres Strait Islands forming distinct clades within the Australian population that reflect the isolation of these landmasses following post-glacial sea level rise [82].

### 6.3 Regional Diversity and Fine-Scale Population Structure

Within the major global populations, *B. pseudomallei* exhibits substantial regional and local diversity. In northern Australia, MLST analysis of 277 isolates identified 159 different sequence types, with no STs shared between Queensland and the Northern Territory, and significant allelic differentiation between the two regions [83]. This fine-scale geographic structure suggests that *B. pseudomallei* populations are relatively stable within local environments and that long-range dispersal events are uncommon, though not absent [83], [92].

In Southeast Asia, similar patterns of regional structure have been documented. Studies in northeast Thailand have identified dominant lineages with unique gene sets and lineage-specific patterns of recombination, with river systems and monsoon dynamics shaping the geographic dispersal of strains [80]. On Hainan Island, China, population genomics analysis revealed a structured population with evidence of both local diversification and occasional long-range dispersal events [73]. In Myanmar, strains were found to be genetically diverse and to originate from Asia, with phylogenetic evidence of reintroductions from neighbouring countries [66]. In Malaysia, whole-genome comparative analysis of clinical isolates has revealed substantial diversity even within a single country [76].

The fine-scale geographic structure of *B. pseudomallei* populations has important implications for source attribution. If strains from different countries or regions are sufficiently distinct at the whole-genome level, it may be possible to assign a clinical isolate to its geographic origin with reasonable confidence. However, the extent to which this is achievable in practice depends on the completeness of reference databases, the degree of overlap between regional populations, and the confounding effects of recombination and long-range dispersal.

### 6.4 Genomic Clades and Lineage Diversity

Whole-genome sequencing has revealed that *B. pseudomallei* populations are organised into multiple genomic clades with distinct characteristics. Analysis of 106 clinical, animal, and environmental strains from a restricted Asian locale identified multiple clades that were largely congruent with MLST groupings but showed clade-specific patterns of recombination, accessory gene exchange, and restriction-modification (RM) system composition [69]. The clade-specific RM systems were shown to inhibit uptake of non-self DNA, suggesting that genomic clades may represent functional units of genetic isolation that modulate intraspecies gene flow [69].

The existence of genomic clades with distinct recombination profiles has important implications for phylogenetic reconstruction and source attribution. Recombination between clade members is common, while interclade exchanges are rare, meaning that the phylogenetic signal within a clade is more reliable than that between clades [69]. This clade structure also means that the genomic diversity of *B. pseudomallei* is not uniformly distributed across the genome: some regions are highly variable due to recombination, while others retain a clearer phylogenetic signal [95].

Genomic diversity within individual soil samples can be remarkably high. A study that obtained 288 *B. pseudomallei* isolates from a single 100-gram soil sample in Thailand identified seven distinct sequence types, with a core genome SNP phylogeny suggesting that all identified STs shared a common ancestor that diverged an estimated 796–1,260 years ago [65]. This micro-scale diversity has profound implications for environmental sampling strategies and for the interpretation of genomic data from clinical isolates: a patient infected from a single environmental source may harbour multiple genetically distinct strains, and the isolate recovered from clinical specimens may not be representative of the full diversity of the infecting population [65], [93]. This local diversity is not restricted to natural soil samples: genomic analysis of *B. pseudomallei* isolates recovered from goats on a single Australian farm identified multiple co-circulating lineages, extending the principle of micro-scale genomic heterogeneity to a pastoral animal reservoir and underscoring the complexity of environmental exposure in endemic settings [129].

---

## 7. Molecular Typing Methods: From MLST to Whole-Genome Sequencing

### 7.1 Multilocus Sequence Typing (MLST)

Multilocus sequence typing (MLST) has been the workhorse of *B. pseudomallei* molecular epidemiology for over two decades. The standard MLST scheme for *B. pseudomallei* uses seven housekeeping gene loci to assign isolates to sequence types (STs), which can then be compared across studies and laboratories using the publicly accessible PubMLST database [100]. MLST has been central to establishing the global population structure of *B. pseudomallei*, demonstrating the biogeographic separation between Australian and Asian populations, and identifying the spread of specific clones across geographic boundaries [75], [83].

The utility of MLST for epidemiological tracking stems from its portability, reproducibility, and the existence of a large reference database. Population assignment of isolates to the Australian or Southeast Asian population can be achieved with high accuracy using MLST data, and the method has been used to identify unusual cases — such as the detection of an Asian clone (ST-562) in Darwin, Australia — that would not have been apparent from clinical data alone [72], [75]. A systematic review and meta-analysis of global *B. pseudomallei* sequence types found that certain STs are strongly associated with specific geographic regions, while others are more widely distributed [38].

### 7.2 Limitations of MLST: Homoplasy and Recombination

Despite its utility, MLST has significant limitations for fine-scale source attribution in *B. pseudomallei*, primarily because of the organism's high recombination rate. The most important limitation is the phenomenon of ST homoplasy: the independent generation of identical STs in geographically distant and phylogenetically unrelated isolates through the acquisition of the same alleles by recombination [85], [91]. Two well-documented cases of homoplasy between Cambodian and Australian isolates were initially interpreted as evidence of intercontinental transmission, but whole-genome sequencing demonstrated that the shared STs had arisen independently [91]. Subsequent work identified the first cases of intracontinental ST homoplasy, involving STs shared between geographically distant Australian isolates [85].

The practical consequence of ST homoplasy is that a shared ST between a clinical isolate and reference strains from a particular country cannot be taken as reliable evidence of geographic origin without whole-genome confirmation [85]. This is particularly problematic for source attribution in travel-associated cases, where the clinical question is precisely whether the patient's isolate matches strains from the country they visited. The limited resolution of MLST — which samples only seven loci from a genome of over 7 Mb — means that it cannot capture the full genomic diversity of *B. pseudomallei* or reliably distinguish between isolates from different geographic regions at the country level [95], [97].

### 7.3 Whole-Genome Sequencing and Core-Genome MLST

Whole-genome sequencing (WGS) has transformed the molecular epidemiology of *B. pseudomallei* by providing orders of magnitude more genomic information than MLST. WGS-based approaches, including core-genome SNP analysis and core-genome MLST (cgMLST), offer substantially higher resolution for phylogenetic reconstruction and source attribution [51], [71]. The removal of recombinant regions prior to SNP-based phylogenetic analysis is a critical step that substantially improves the accuracy of phylogenetic reconstruction and reduces the risk of artefactual clustering [67], [81].

Core-genome MLST schemes for *B. pseudomallei* have been developed to provide a standardised, portable, and high-resolution typing framework that is more reproducible than raw SNP analysis and more informative than seven-locus MLST [124]. The Lichtenegger cgMLST scheme, which uses 4,221 loci, was formally developed and validated as a species-wide standard [124], and has subsequently been applied to large collections of *B. pseudomallei* genomes, providing substantially higher resolution than conventional MLST while remaining computationally tractable [99]. Nanopore sequencing-based approaches to cgMLST have also been developed to enable rapid typing in resource-limited settings [99].

WGS has enabled a range of epidemiological applications that were not possible with MLST. These include the resolution of ST homoplasy cases, the confirmation of outbreak sources, the detection of polyclonal infections, and the identification of long-range dispersal events [85], [91], [93]. WGS has also revealed that isolates with identical STs can be genomically distinct at the whole-genome level, as demonstrated by the identification of polyclonal infections in individual patients [25], [93].

### 7.4 Source Attribution and Outbreak Investigation by WGS

WGS has been applied to a growing number of melioidosis outbreak investigations and source attribution studies. In a landmark study, McRobb et al. used WGS to confirm that a domestic water supply was the source of two melioidosis cases in rural northern Australia, with clinical isolates differing from the environmental strain by just one SNP each [2]. This approach has since been applied prospectively to link individual human cases to targeted environmental sampling sites with high granularity across northern Australia, providing a scalable framework for environmental source investigation in endemic settings [125]. Similar approaches have been used to investigate clusters of cases in remote Australian communities, to link clinical isolates to specific environmental sampling sites, and to confirm or refute suspected transmission events [24], [93].

The power of WGS for source attribution derives from the high resolution it provides: even closely related isolates from the same geographic area can be distinguished by their SNP profiles, and the genomic distance between isolates can be used to infer the probability of a shared source [51], [71]. However, the interpretation of genomic distance in *B. pseudomallei* is complicated by the high recombination rate, which can generate large genomic distances between isolates that share a recent common ancestor, and by the micro-scale diversity of environmental populations, which means that the infecting strain may not be identical to any available reference genome [65], [90].

The application of WGS to geographic source attribution — the question of which country a clinical isolate originated from — is a more challenging problem than outbreak source attribution. While WGS can reliably distinguish Australian from Asian isolates and can assign isolates to broad geographic regions, the ability to attribute an isolate to a specific country depends on the availability of representative reference genomes from that country and on the degree of genomic differentiation between countries [30], [75]. The uneven global distribution of sequenced *B. pseudomallei* genomes, with large regions of endemicity in Latin America, Africa, and South Asia underrepresented in public databases, is a major limitation for country-level attribution [53], [67]. For settings where WGS is not feasible, PCR–high resolution melt (PCR-HRM) assays targeting geographically informative loci have been developed to assign Caribbean and Indian Ocean isolates to their region of origin, demonstrating that subgenomic molecular markers can carry detectable geographic signal even without whole-genome data [127].

Prior work has nonetheless demonstrated that the phylogeographic signal in *B. pseudomallei* genomes is sufficiently strong for broad regional attribution. Viberg et al. used whole-genome phylogenetics to correctly assign the isolate of a cystic fibrosis patient to Southeast Asia based solely on its position in the global *B. pseudomallei* tree, confirming the established principle that the organism carries a "very strong phylogeographic signal that allows accurate identification of strain origin on a continental level" [102]. This proof-of-concept establishes that the geographic information encoded in *B. pseudomallei* genomes is real and detectable, and it directly motivates the question of whether comparable resolution is achievable at the country level — the central question addressed in the present study.

---

## 8. The Challenge of Geographic Attribution

The question of whether the genome of a *B. pseudomallei* clinical isolate can reliably identify the country of exposure is one of direct clinical and public health relevance. For travel-associated melioidosis, the ability to attribute infection to a specific country would assist in contact tracing, public health notification, and the recognition of new endemic foci. It would also be valuable in cases where the patient cannot provide a reliable travel history — for example, due to cognitive impairment, unconsciousness, or deliberate concealment — and in cases where the exposure may have occurred years before presentation due to latency.

The genomic basis for geographic attribution rests on the biogeographic structure of *B. pseudomallei* populations: if strains from different countries are sufficiently distinct at the whole-genome level, and if representative reference genomes are available from all potential source countries, then it should in principle be possible to assign a clinical isolate to its country of origin by comparing it to the reference database [30], [75]. The robust separation between Australian and Asian populations, and the finer-scale regional structure within each major population, provide a foundation for this approach [81], [83].

However, several factors complicate geographic attribution at the country level. First, the high recombination rate of *B. pseudomallei* erodes phylogenetic signal and can generate misleading clustering of unrelated isolates [81], [85]. Second, some lineages span continental boundaries, as demonstrated by the detection of an Asian clone in Darwin and by the shared ancestry of African and South American strains [30], [72]. Third, the reference genome database is highly uneven in its geographic coverage, with some countries — particularly in Latin America, the Caribbean, and parts of Africa — having few or no publicly available genomes [53], [67]. Fourth, the micro-scale diversity of *B. pseudomallei* in the environment means that the isolate recovered from a clinical specimen may not be representative of the dominant strains in the source country [65], [90].

These challenges suggest that while genomic approaches can reliably attribute isolates to broad geographic regions (e.g., Asia versus Australia, or Southeast Asia versus South Asia), country-level attribution may be beyond the resolution of current methods and databases for many source countries. The development of more comprehensive reference databases, the application of recombination-corrected phylogenetic methods, and the use of high-resolution typing schemes such as cgMLST are all likely to improve the accuracy of geographic attribution in the future. Understanding the limits of current genomic approaches is essential for interpreting the results of attribution studies and for communicating their findings to clinicians and public health authorities.

---

## 9. Conclusion

Melioidosis is a serious, globally distributed, and substantially underrecognised infectious disease caused by the environmentally ubiquitous bacterium *B. pseudomallei*. Its epidemiology is shaped by the geographic distribution of the organism in tropical soils and waters, by host susceptibility factors dominated by diabetes and other immunocompromising conditions, and by the seasonal dynamics of environmental exposure. The disease's clinical diversity, capacity for latency, and the diagnostic challenges it poses in non-endemic settings all contribute to its neglected status and to the difficulty of accurately estimating its global burden.

The genomic biology of *B. pseudomallei* is characterised by a large bipartite genome, an extensive and dynamic accessory genome, a globally structured population with robust biogeographic signal, and an extraordinarily high recombination rate that both generates diversity and complicates phylogenetic reconstruction. Comparative genomics has provided strong but still provisional support for an Australian origin of the species and its subsequent global dispersal, and has established the existence of fine-scale geographic structure within major populations. Molecular typing methods have evolved from seven-locus MLST to whole-genome sequencing and cgMLST, providing progressively higher resolution for epidemiological tracking and source attribution. However, the limitations of current approaches — particularly the confounding effects of recombination, the phenomenon of ST homoplasy, and the uneven geographic coverage of reference genome databases — mean that country-level geographic attribution remains a challenging and incompletely solved problem. These considerations form the essential backdrop for evaluating the utility and limitations of genomic approaches to exposure-country attribution in travel-associated melioidosis.

<!--SCISPACE_REFERENCES

Below are the references cited in this file, each containing the author names, title, journal, volume, issue, pages, publication date, DOI and link.
Every entry is complete, untruncated field data - not a formatted citation: one "label: value" per line, authors as "Family, Given" separated by "; " in citation order, and issued as an ISO date (YYYY-MM-DD, YYYY-MM or YYYY).



These are the papers cited in the insights:

[1]
  authors: Thangaraju, Deepak; Sundaramoorthy, Varun; Thiagarajan, Vigna
  title: P-148. Melioidosis: A Seven-Year Review (2017-2023)
  journal: Open Forum Infectious Diseases
  volume: 12
  issue: Supplement_1
  issued: 2025-01-29
  doi: 10.1093/ofid/ofae631.353
  url: https://scispace.com/papers/p-148-melioidosis-a-seven-year-review-2017-2023-z3i1rbuupm15

[2]
  authors: Mohapatra, Prasanta Raghab; Behera, Bijayini; Mishra, Baijayantimala
  title: Melioidosis: An Indian Perspective
  journal: Journal of Association of Physicians of India
  volume: 73
  issue: 5
  pages: 63-68
  issued: 2025-01-01
  doi: 10.59556/japi.73.0945
  url: https://scispace.com/papers/melioidosis-an-indian-perspective-nr5dzof0v6pa

[3]
  authors: Currie, Bart J.
  title: Melioidosis: Evolving Concepts in Epidemiology, Pathogenesis, and Treatment
  journal: Seminars in Respiratory and Critical Care Medicine
  volume: 36
  issue: 1
  pages: 111-125
  issued: 2015-02-02
  doi: 10.1055/S-0034-1398389
  url: https://scispace.com/papers/melioidosis-evolving-concepts-in-epidemiology-pathogenesis-4ftm6sw62z

[4]
  authors: Mohapatra, Prasanta K.; Mishra, Baijayantimala
  title: Burden of melioidosis in India and South Asia: Challenges and ways forward
  journal: The Lancet regional health
  volume: 2
  pages: 100004-100004
  issued: 2022-05-01
  doi: 10.1016/j.lansea.2022.03.004
  url: https://scispace.com/papers/burden-of-melioidosis-in-india-and-south-asia-challenges-and-263fwfy4

[5]
  authors: Norman, Francesca; Blair, Barbra M; Chamorro-Tojeiro, Sandra; Sanz, Marta; Chen, Lin H.
  title: The Evolving Global Epidemiology of Human Melioidosis
  issued: 2024-09-18
  doi: 10.20944/preprints202409.1336.v1
  url: https://scispace.com/papers/the-evolving-global-epidemiology-of-human-melioidosis-3pwaipad3qtu

[6]
  authors: Mahikul, Wiriya; White, Lisa J.; White, Lisa J.; Poovorawan, Kittiyod; Soonthornworasiri, Ngamphol; Sukontamarn, Pataporn; Chanthavilay, Phetsavanh; Medley, Graham F.; Pan-Ngum, Wirichada
  title: Modelling population dynamics and seasonal movement to assess and predict the burden of melioidosis.
  journal: PLOS Neglected Tropical Diseases
  volume: 13
  issue: 5
  issued: 2019-05-09
  doi: 10.1371/JOURNAL.PNTD.0007380
  url: https://scispace.com/papers/modelling-population-dynamics-and-seasonal-movement-to-266p12iy7b

[7]
  authors: Dias, Meena; Dias, Anusha Leah
  title: Emerging pathogen Burkholderia pseudomallei: what do we know
  journal: Indian Journal of Microbiology Research
  volume: 2
  issue: 1
  pages: 50-54
  issued: 2015-01-01
  url: https://scispace.com/papers/emerging-pathogen-burkholderia-pseudomallei-what-do-we-know-2oi5t9sigb

[8]
  authors: Chowdhury, Sukanta; Barai, Lovely; Afroze, Samira Rahat; Ghosh, Probir Kumar; Afroz, Farhana; Rahman, H.; Ghosh, Sumon; Hossain, Muhammad Belal; Rahman, Mohammed M.; Das, Pritimoy; Rahim, Mohammad Abdur
  title: The Epidemiology of Melioidosis and Its Association with Diabetes Mellitus: A Systematic Review and Meta-Analysis
  journal: Pathogens
  volume: 11
  issue: 2
  pages: 149-149
  issued: 2022-01-25
  doi: 10.3390/pathogens11020149
  url: https://scispace.com/papers/the-epidemiology-of-melioidosis-and-its-association-with-27l0iqny

[9]
  authors: Mazhar, Ismail; Andalib, Sofia; Alim, Rumana; Munwar, Shaila
  title: An update on Burkholderia pseudomallei infection: epidemiology, pathogenesis, diagnostic approaches and treatment challenges
  volume: 21
  issue: 1
  pages: 100-106
  issued: 2025-06-21
  doi: 10.3329/jmcwh.v21i1.81187
  url: https://scispace.com/papers/an-update-on-burkholderia-pseudomallei-infection-x599v0fam0gr

[10]
  authors: Buisson, Yves
  title: [A multi-resistant bacterium before the era of antibiotics : the agent of melioidosis].
  journal: Comptes Rendus Biologies
  issued: 2023-08-31
  doi: 10.5802/crbiol.109
  url: https://scispace.com/papers/a-multi-resistant-bacterium-before-the-era-of-antibiotics-4q37qtfeu5

[11]
  title: Melioidosis: The Soil-Borne Disease in Thai Communities
  issued: 2025-08-19
  doi: 10.5281/zenodo.16899388
  url: https://scispace.com/papers/melioidosis-the-soil-borne-disease-in-thai-communities-5n35eao7zyog

[12]
  authors: Norman, Francesca; Blair, Barbra M.; Chamorro-Tojeiro, Sandra; Sanz, Marta; Chen, Lin H.
  title: The Evolving Global Epidemiology of Human Melioidosis: A Narrative Review
  journal: Pathogens
  volume: 13
  issue: 11
  pages: 926-926
  issued: 2024-10-24
  doi: 10.3390/pathogens13110926
  url: https://scispace.com/papers/the-evolving-global-epidemiology-of-human-melioidosis-a-6yhqjsokpk6h

[13]
  authors: Jiee, Sam Froze; Lim, Kai Joo; Vui, Daryl Sin Choon; Marius, Dina Peter; Illyana, Nurul Syafiqah; Jantim, Anisah
  title: Extreme Weather and Melioidosis: An endemic tropical disease in Penampang district of Sabah, Malaysia
  journal: Journal of Health Research
  volume: 37
  issue: 5
  issued: 2023-03-04
  doi: 10.56808/2586-940x.1023
  url: https://scispace.com/papers/extreme-weather-and-melioidosis-an-endemic-tropical-disease-1ohp9ov8

[14]
  authors: Norman, Francesca F.; Chen, Li
  title: Travel-associated Melioidosis: a narrative review.
  journal: Journal of Travel Medicine
  volume: 30
  issue: 3
  issued: 2023-03-27
  doi: 10.1093/jtm/taad039
  url: https://scispace.com/papers/travel-associated-melioidosis-a-narrative-review-hwype50j

[15]
  authors: Stewart, James D; Smith, Simon; Smith, Simon; Binotto, Enzo; McBride, William J. H.; Currie, Bart J.; Hanson, Joshua; Hanson, Joshua; Hanson, Joshua
  title: The epidemiology and clinical features of melioidosis in Far North Queensland: Implications for patient management.
  journal: PLOS Neglected Tropical Diseases
  volume: 11
  issue: 3
  pages: 1-15
  issued: 2017-03-06
  doi: 10.1371/JOURNAL.PNTD.0005411
  url: https://scispace.com/papers/the-epidemiology-and-clinical-features-of-melioidosis-in-far-2fvskra4oe

[16]
  authors: Currie, Bart J.; Ward, Linda; Cheng, Allen C.
  title: The epidemiology and clinical spectrum of melioidosis: 540 cases from the 20 year Darwin prospective study.
  journal: PLOS Neglected Tropical Diseases
  volume: 4
  issue: 11
  pages: 1-11
  issued: 2010-11-30
  doi: 10.1371/JOURNAL.PNTD.0000900
  url: https://scispace.com/papers/the-epidemiology-and-clinical-spectrum-of-melioidosis-540-5fgsohf4ik

[17]
  authors: Currie, Bart J.; Jacups, Susan P.; Jacups, Susan P.; Cheng, Allen C.; Cheng, Allen C.; Fisher, Dale; Anstey, Nicholas M.; Anstey, Nicholas M.; Huffam, Sarah; Krause, Vicki
  title: Melioidosis epidemiology and risk factors from a prospective whole-population study in northern Australia
  journal: Tropical Medicine & International Health
  volume: 9
  issue: 11
  pages: 1167-1174
  issued: 2004-11-01
  doi: 10.1111/J.1365-3156.2004.01328.X
  url: https://scispace.com/papers/melioidosis-epidemiology-and-risk-factors-from-a-prospective-3m22id6c6m

[18]
  authors: Fong, Jing Hong; Pillai, Naganathan; Yap, Christina Gertrude; Jahan, Nowrozy Kamar
  title: Incidences, Case Fatality Rates and Epidemiology of Melioidosis Worldwide: A Review Paper
  journal: Open Access Library Journal
  volume: 8
  issue: 06
  pages: 1-20
  issued: 2021-06-01
  doi: 10.4236/OALIB.1107537
  url: https://scispace.com/papers/incidences-case-fatality-rates-and-epidemiology-of-8bh4tr2qs9

[19]
  authors: Chen, Pei-Shih; Chen, Yao-Shen; Lin, Hsi-Hsun; Liu, Pei-Ju; Ni, Wei-Fan; Hsueh, Pei-Tan; Liang, Shih-Hsiung; Chen, Chialin; Chen, Ya-Lei
  title: Airborne Transmission of Melioidosis to Humans from Environmental Aerosols Contaminated with B. pseudomallei.
  journal: PLOS Neglected Tropical Diseases
  volume: 9
  issue: 6
  issued: 2015-06-10
  doi: 10.1371/JOURNAL.PNTD.0003834
  url: https://scispace.com/papers/airborne-transmission-of-melioidosis-to-humans-from-35brhk3nyo

[20]
  authors: Schully, Kevin L.; Berjohn, Catherine M.; Prouty, Angela M.; Fitkariwala, Amitha; Som, Tin; Sieng, Darith; Gregory, Michael J.; Vaughn, Andrew; Kheng, Sim; Te, Vantha; Duplessis, Christopher A.
  title: Melioidosis in lower provincial Cambodia: A case series from a prospective study of sepsis in Takeo Province.
  journal: PLOS Neglected Tropical Diseases
  volume: 11
  issue: 9
  pages: 0005923
  issued: 2017-09-13
  doi: 10.1371/JOURNAL.PNTD.0005923
  url: https://scispace.com/papers/melioidosis-in-lower-provincial-cambodia-a-case-series-from-35eke2uu9w

[21]
  authors: Currie, Bart J.
  title: Melioidosis: an important cause of pneumonia in residents of and travellers returned from endemic regions
  journal: European Respiratory Journal
  volume: 22
  issue: 3
  pages: 542-550
  issued: 2003-09-01
  doi: 10.1183/09031936.03.00006203
  url: https://scispace.com/papers/melioidosis-an-important-cause-of-pneumonia-in-residents-of-1bm04pw5jn

[22]
  authors: Wongbutdee, Jaruwan; Jittimanee, Jutharat; Dandee, Suwaporn; Thongsang, Pongthep; Saengnill, Wacharapong
  title: Exploring the Relationship between Melioidosis Morbidity Rate and Local Environmental Indicators Using Remotely Sensed Data
  issued: 2024-04-05
  doi: 10.20944/preprints202404.0446.v1
  url: https://scispace.com/papers/exploring-the-relationship-between-melioidosis-morbidity-2tf17zvg7y

[23]
  authors: Hassan, Muhammad R A; Aziz, Norasmidar A; Ismail, Noraini; Shafie, Zainab; Mayala, Benjamin K.; Donohue, Rose E.; Pani, S P; Michael, Edwin
  title: Socio-epidemiological and land cover risk factors for melioidosis in Kedah, Northern Malaysia
  journal: PLOS Neglected Tropical Diseases
  volume: 13
  issue: 3
  issued: 2019-03-18
  doi: 10.1371/JOURNAL.PNTD.0007243
  url: https://scispace.com/papers/socio-epidemiological-and-land-cover-risk-factors-for-1g3zzolkft

[24]
  authors: Mukhopadhyay, Chiranjay; Shaw, Tushar; Varghese, George M.; Dance, David A. B.; Dance, David A. B.; Dance, David A. B.
  title: Melioidosis in South Asia (India, Nepal, Pakistan, Bhutan and Afghanistan)
  journal: Tropical Medicine and Infectious Disease
  volume: 3
  issue: 2
  pages: 51-51
  issued: 2018-05-22
  doi: 10.3390/TROPICALMED3020051
  url: https://scispace.com/papers/melioidosis-in-south-asia-india-nepal-pakistan-bhutan-and-r20e269p3e

[25]
  title: Next-generation sequencing for greater understanding of Burkholderia pseudomallei epidemiology and phylogeography in northern Australia and Vientiane, Laos
  issued: 2020-06-05
  doi: 10.25913/5ed9d5e7129d4
  url: https://scispace.com/papers/next-generation-sequencing-for-greater-understanding-of-l0d51b7r5zom

[26]
  authors: Currie, Bart J.; Mayo, Mark; Ward, Linda; Kaestli, Mirjam; Meumann, Ella M.; Webb, Jessica R.; Woerle, Celeste; Baird, Robert W.; Price, Ric N.; Marshall, Catherine S.; Ralph, Anna P.
  title: The Darwin Prospective Melioidosis Study: a 30-year prospective, observational investigation
  journal: Lancet Infectious Diseases
  volume: 21
  issue: 12
  pages: 1737-1746
  issued: 2021-07-22
  doi: 10.1016/S1473-3099(21)00022-0
  url: https://scispace.com/papers/the-darwin-prospective-melioidosis-study-a-30-year-4j2ezyt3ni

[27]
  authors: Selvam, Kasturi; Ganapathy, Thanasree; Najib, M. Ahmad; Khalid, Muhammad Fazli; Abdullah, Norazmi; Harun, Azian; Mohammad, Wan Mohd Zahiruddin Wan; Aziah, Ismail
  title: Burden and Risk Factors of Melioidosis in Southeast Asia: A Scoping Review
  journal: International Journal of Environmental Research and Public Health
  volume: 19
  issue: 23
  pages: 15475-15475
  issued: 2022-11-22
  doi: 10.3390/ijerph192315475
  url: https://scispace.com/papers/burden-and-risk-factors-of-melioidosis-in-southeast-asia-a-23rj0523

[28]
  authors: Chandrakar, Sagar; Dias, Meena
  title: Clinico-epidemiological spectrum of melioidosis: a 2-year prospective study in the western coastal region of India
  journal: Southern African Journal of Infectious Diseases
  volume: 31
  issue: 1
  pages: 14-19
  issued: 2016-01-18
  doi: 10.1080/23120053.2015.1118830
  url: https://scispace.com/papers/clinico-epidemiological-spectrum-of-melioidosis-a-2-year-36wog61zdd

[29]
  authors: Birnie, Emma; Biemond, Jason J; Wiersinga, W. Joost
  title: Drivers of melioidosis endemicity: epidemiological transition, zoonosis, and climate change
  journal: Current Opinion in Infectious Diseases
  volume: 35
  pages: 196-204
  issued: 2022-04-28
  doi: 10.1097/QCO.0000000000000827
  url: https://scispace.com/papers/drivers-of-melioidosis-endemicity-epidemiological-transition-cruqf01d

[30]
  authors: Mtg, Holden; Z., Yang,; Harris; Ae, Mather; M., Mayo,; Bg, Spratt; J., Corander,; Dab., Dance; Bj, Currie; Sj, Peacock
  title: Global and regional dissemination and evolution of $\textit{Burkholderia pseudomallei}$
  issued: 2017-03-06
  doi: 10.17863/cam.8171
  url: https://scispace.com/papers/global-and-regional-dissemination-and-evolution-of-textit-c2six87d4kbt

[31]
  authors: Gassiep, I; Armstrong, M.; Norton, R.
  title: Human Melioidosis
  doi: 10.1128/cmr.00006-19
  url: https://scispace.com/papers/human-melioidosis-vko6w6xsuga4

[32]
  authors: Limmathurotsakul, Direk; Golding, Nick; Dance, David A. B.; Messina, Jane P.; Pigott, David M.; Moyes, Catherine L.; Rolim, Dionne B.; Bertherat, Eric; Day, Nicholas P. J.; Peacock, Sharon J.; Hay, Simon I.
  title: Predicted global distribution of Burkholderia pseudomallei and burden of melioidosis
  journal: Nature microbiology
  volume: 1
  issue: 1
  pages: 15008-15008
  issued: 2016-01-11
  doi: 10.1038/NMICROBIOL.2015.8
  url: https://scispace.com/papers/predicted-global-distribution-of-burkholderia-pseudomallei-1of145y73x

[33]
  authors: Ibrahem, Karem; Saleh, Bandar Hasan; Al-Hussainy, Nabeel H.; Alsaedi, Abdulaziz A.; Niyazi, Hatoon A.; Niyazi, Hanouf; Juma, Noha; Alqarni, Mona; Alfadil, Abdelbagi; Sharif, Asim; Redwan, Bassam
  title: Burkholderia pseudomallei: A Multifaceted Threat and the Path Forward in Treatment and Prevention
  journal: Infection and Drug Resistance
  volume: Volume 18
  pages: 5115-5127
  issued: 2025-09-01
  doi: 10.2147/idr.s535624
  url: https://scispace.com/papers/burkholderia-pseudomallei-a-multifaceted-threat-and-the-path-0ghoao3tojrz

[34]
  authors: Cheng, Allen C.; Currie, Bart J.; Currie, Bart J.
  title: Melioidosis: Epidemiology, Pathophysiology, and Management
  journal: Clinical Microbiology Reviews
  volume: 18
  issue: 2
  pages: 383-416
  issued: 2005-04-01
  doi: 10.1128/CMR.18.2.383-416.2005
  url: https://scispace.com/papers/melioidosis-epidemiology-pathophysiology-and-management-2wn4gevv3p

[35]
  authors: Chakravorty, Arindam; Heath, Christopher H.
  title: Melioidosis: An updated review
  journal: Journal of general practice
  volume: 48
  issue: 5
  pages: 327-332
  issued: 2019-05-01
  doi: 10.31128/AJGP-04-18-4558
  url: https://scispace.com/papers/melioidosis-an-updated-review-1obqzo7u2j

[36]
  authors: Jarrett; Seng; Fitzgerald
  title: Paediatric melioidosis.
  source: PubMed
  issued: 2024
  doi: 10.1016/j.prrv.2023.11.002
  url: https://pubmed.ncbi.nlm.nih.gov/38245464

[37]
  authors: Hassan, Muhammad R A; Pani, S. P.; Peng, Ng P; Voralu, K; Vijayalakshmi, Natesan; Mehanderkar, Ranjith; Aziz, Norasmidar A; Michael, Edwin
  title: Incidence, risk factors and clinical epidemiology of melioidosis: a complex socio-ecological emerging infectious disease in the Alor Setar region of Kedah, Malaysia.
  journal: BMC Infectious Diseases
  volume: 10
  issue: 1
  pages: 302-302
  issued: 2010-10-21
  doi: 10.1186/1471-2334-10-302
  url: https://scispace.com/papers/incidence-risk-factors-and-clinical-epidemiology-of-3t6bscawsv

[38]
  authors: Laklaeng, Sa-ngob; Phu, Doan Hoang; Songsri, Jirarat; Wisessombat, Sueptrakool; Mala, Wanida; Senghoi, Wilaiwan; Phothaworn, Preeda; Nuinoon, Manit; Wongtawan, Tuempong; Klangbud, Wiyada Kwanhian
  title: A systematic review and meta-analysis of the global prevalence and relationships among Burkholderia pseudomallei sequence types isolated from humans, animals, and the environment
  issued: 2024-07-15
  doi: 10.60692/3p1jp-gak33
  url: https://scispace.com/papers/a-systematic-review-and-meta-analysis-of-the-global-ihjwbatzn9p7

[39]
  authors: Limmathurotsakul, Direk; Peacock, Sharon J.; Peacock, Sharon J.
  title: Melioidosis: a clinical overview
  journal: British Medical Bulletin
  volume: 99
  issue: 1
  pages: 125-139
  issued: 2011-09-01
  doi: 10.1093/BMB/LDR007
  url: https://scispace.com/papers/melioidosis-a-clinical-overview-4pxhswmy5a

[40]
  authors: Camargo, Nataly; Casadiego, Giovanna K; Fernandez, Dinno A; Millan, Lina V; Hernandez, Angie K; Vargas, Sandra; Rios, Rafael; Marin-Osorio, Adriana; Salcedo, Soraya; Rodriguez, Deisy L; Bayuelo-Charris, Ilich V
  title: A Young Diabetic Patient With Sepsis After Gardening.
  journal: Open Forum Infectious Diseases
  volume: 7
  issue: 5
  issued: 2020-05-01
  doi: 10.1093/OFID/OFAA159
  url: https://scispace.com/papers/a-young-diabetic-patient-with-sepsis-after-gardening-3cbaxmrlo7

[41]
  authors: Sarovich, Derek S.; Garin, Benoit; Smet, Birgit De; Smet, Birgit De; Kaestli, Mirjam; Mayo, Mark; Vandamme, Peter; Jacobs, Jan; Jacobs, Jan; Lompo, Palpouguini; Tahita, Marc Christian
  title: Phylogenomic Analysis Reveals an Asian Origin for African Burkholderia pseudomallei and Further Supports Melioidosis Endemicity in Africa.
  volume: 1
  issue: 2
  pages: 1-12
  issued: 2016-04-27
  doi: 10.1128/MSPHERE.00089-15
  url: https://scispace.com/papers/phylogenomic-analysis-reveals-an-asian-origin-for-african-3tgif5j1xn

[42]
  authors: Anh, Vu Thi Ngoc; Tran, Quyen; Bui, Linh Nguyen Hai; Trung, Trịnh Thành
  title: Seasonal change of Burkholderia pseudomallei in paddy field water strongly correlates with ambient temperature: A study in north-central Vietnam
  journal: PLOS Neglected Tropical Diseases
  volume: 19
  issue: 7
  pages: e0013322-e0013322
  issued: 2025-07-30
  doi: 10.1371/journal.pntd.0013322
  url: https://scispace.com/papers/seasonal-change-of-burkholderia-pseudomallei-in-paddy-field-u8b4c3wkparn

[43]
  authors: Currie, Bart J.; Dance, David A. B.; Cheng, Allen C.
  title: The global distribution of Burkholderia pseudomallei and melioidosis: an update
  journal: Transactions of The Royal Society of Tropical Medicine and Hygiene
  volume: 102
  pages: 1-4
  issued: 2008-12-01
  doi: 10.1016/S0035-9203(08)70002-6
  url: https://scispace.com/papers/the-global-distribution-of-burkholderia-pseudomallei-and-2ceakgled2

[44]
  authors: Amadasi, Silvia; Zoppo, Sarah Dal; Bonomini, Annalisa; Bussi, Anna; Pedroni, Palmino; Balestrieri, Gianpaolo; Signorini, Liana; Castelli, Francesco
  title: A Case of Melioidosis Probably Acquired by Inhalation of Dusts During a Helicopter Flight in a Healthy Traveler Returning From Singapore
  journal: Journal of Travel Medicine
  volume: 22
  issue: 1
  pages: 57-60
  issued: 2015-01-01
  doi: 10.1111/JTM.12150
  url: https://scispace.com/papers/a-case-of-melioidosis-probably-acquired-by-inhalation-of-16hc87p868

[45]
  authors: Venkatesan; Siritana; Silisouk; Roberts; Robinson; Dance
  title: Burkholderia pseudomallei Bacteria in Ornamental Fish Tanks, Vientiane, Laos, 2023.
  source: PubMed
  issued: 2024
  doi: 10.3201/eid3003.231674
  url: https://pubmed.ncbi.nlm.nih.gov/38407187

[46]
  authors: Birnie, Emma; Virk, Harjeet S; Savelkoel, Jelmer; Spijker, René; Spijker, René; Bertherat, Eric; Dance, David A. B.; Dance, David A. B.; Dance, David A. B.; Limmathurotsakul, Direk; Limmathurotsakul, Direk
  title: Global burden of melioidosis in 2015: a systematic review and data synthesis
  journal: Lancet Infectious Diseases
  volume: 19
  issue: 8
  pages: 892-902
  issued: 2019-08-01
  doi: 10.1016/S1473-3099(19)30157-4
  url: https://scispace.com/papers/global-burden-of-melioidosis-in-2015-a-systematic-review-and-48y40snya4

[47]
  authors: Kain, Matthew J. W.; Reece, Nicola L.; Parry, Christopher M; Rajahram, Giri Shan; Paterson, David L; Woolley, Stephen D.
  title: The Rapid Emergence of Hypervirulent Klebsiella Species and Burkholderia pseudomallei as Major Health Threats in Southeast Asia: The Urgent Need for Recognition as Neglected Tropical Diseases
  journal: Tropical Medicine and Infectious Disease
  issued: 2024-04-08
  doi: 10.3390/tropicalmed9040080
  url: https://scispace.com/papers/the-rapid-emergence-of-hypervirulent-klebsiella-species-and-4tifpc57y9

[48]
  authors: Savelkoel, Jelmer; Dance, David A. B.; Currie, Bart J.; Limmathurotsakul, Direk; Wiersinga, W Joost
  title: A call to action: time to recognise melioidosis as a neglected tropical disease
  issued: 2024-07-15
  doi: 10.60692/cjp7n-g4756
  url: https://scispace.com/papers/a-call-to-action-time-to-recognise-melioidosis-as-a-wbxsewb24gh8

[49]
  authors: Ribolzi, Olivier; Rochelle-Newall, Emma; Dittrich, Sabine; Auda, Yves; Newton, Paul N.; Rattanavong, Sayaphet; Knappik, Michael; Soulileuth, Bounsamai; Sengtaheuanghoung, Oloth; Dance, David A. B.; Pierret, Alain
  title: Land use and soil type determine the presence of the pathogen Burkholderia pseudomallei in tropical rivers.
  journal: Environmental Science and Pollution Research
  volume: 23
  issue: 8
  pages: 7828-7839
  issued: 2016-01-13
  doi: 10.1007/S11356-015-5943-Z
  url: https://scispace.com/papers/land-use-and-soil-type-determine-the-presence-of-the-2eagp7wlra

[50]
  authors: Win; Ashley; Zin; Aung; Swe; Ling; Nosten; Thein; Zaw; Aung; Tun; Dance; Smithuis
  title: Melioidosis in Myanmar.
  source: PubMed
  issued: 2018
  doi: 10.3390/tropicalmed3010028
  url: https://pubmed.ncbi.nlm.nih.gov/30274425

[51]
  authors: Price, Erin P.; Currie, Bart J.; Sarovich, Derek S.
  title: Genomic Insights Into the Melioidosis Pathogen, Burkholderia pseudomallei
  journal: Current tropical medicine reports
  volume: 4
  issue: 3
  pages: 95-102
  issued: 2017-09-01
  doi: 10.1007/S40475-017-0111-9
  url: https://scispace.com/papers/genomic-insights-into-the-melioidosis-pathogen-burkholderia-3tytijz1ou

[52]
  authors: Muthumbi; Gordon; Mochamah; Nyongesa; Odipo; Mwarumba; Mturi; Etyang; Dance; Scott; Morpeth
  title: Population-Based Estimate of Melioidosis, Kenya.
  source: PubMed
  issued: 2019
  doi: 10.3201/eid2505.180545
  url: https://pubmed.ncbi.nlm.nih.gov/31002067

[53]
  authors: Duarte; Montufar; Moreno; Sánchez; Rodríguez; Torres; Morales; Bautista; Huertas; Myers; Gulvik; Elrod; Blaney; Gee
  title: Genomic Diversity of Burkholderia pseudomallei Isolates, Colombia.
  source: PubMed
  issued: 2021
  doi: 10.3201/eid2702.202824
  url: https://pubmed.ncbi.nlm.nih.gov/33496648

[54]
  authors: Currie; Kaestli
  title: Epidemiology: A global picture of melioidosis.
  source: PubMed
  issued: 2016
  doi: 10.1038/529290a
  url: https://pubmed.ncbi.nlm.nih.gov/26791716

[55]
  authors: Savelkoel; Wagner; Ojide; Frankenfeld; Rudloff; Dunachie; Lipp; Wiersinga; Steinmetz; Birnie; Oladele
  title: Serologic Evidence of Exposure to Burkholderia pseudomallei, Nigeria.
  source: PubMed
  issued: 2026
  doi: 10.3201/eid3201.251113
  url: https://pubmed.ncbi.nlm.nih.gov/41612630

[56]
  authors: Dance; Limmathurotsakul
  title: Global Burden and Challenges of Melioidosis.
  source: PubMed
  issued: 2018
  doi: 10.3390/tropicalmed3010013
  url: https://pubmed.ncbi.nlm.nih.gov/30274411

[57]
  authors: Birnie, Emma; James, Ayorinde Babatunde; Peters, Folake; Olajumoke, Makinwa; Traore, Tieble; Bertherat, Eric; Trung, Trinh Thanh; Dhamari, Naidoo; Steinmetz, Ivo; Wiersinga, W. Joost; Oladele, Rita O.
  title: Melioidosis in Africa: Time to Raise Awareness and Build Capacity for Its Detection, Diagnosis, and Treatment.
  journal: American Journal of Tropical Medicine and Hygiene
  volume: 106
  issue: 2
  pages: 394-397
  issued: 2022-01-10
  doi: 10.4269/ajtmh.21-0673
  url: https://scispace.com/papers/melioidosis-in-africa-time-to-raise-awareness-and-build-3lkt5hfm

[58]
  authors: Wiersinga, W. Joost; Poll, Tom van der; White, Nicholas J.; White, Nicholas J.; Day, Nicholas P. J.; Day, Nicholas P. J.; Peacock, Sharon J.; Peacock, Sharon J.
  title: Melioidosis: insights into the pathogenicity of Burkholderia pseudomallei
  journal: Nature Reviews Microbiology
  volume: 4
  issue: 4
  pages: 272-282
  issued: 2006-04-01
  doi: 10.1038/NRMICRO1385
  url: https://scispace.com/papers/melioidosis-insights-into-the-pathogenicity-of-burkholderia-5elmf3a9dl

[59]
  authors: Gilad, Jacob; Schwartz, David A.; Amsalem, Yoram
  title: Clinical Features and Laboratory Diagnosis of Infection with the Potential Bioterrorism Agents Burkholderia Mallei and Burkholderia Pseudomallei
  journal: International journal of biomedical science : IJBS
  volume: 3
  issue: 3
  pages: 144-152
  issued: 2007-09-01
  url: https://scispace.com/papers/clinical-features-and-laboratory-diagnosis-of-infection-with-2avurd1fzn

[60]
  authors: Dance
  title: Treatment and prophylaxis of melioidosis.
  source: PubMed
  issued: 2014
  doi: 10.1016/j.ijantimicag.2014.01.005
  url: https://pubmed.ncbi.nlm.nih.gov/24613038

[61]
  authors: Pongmala, Khemngeun; Pierret, Alain; Oliva, Priscia; Pando, Anne; Davong, Viengmon; Rattanavong, Sayaphet; Silvera, Norbert; Luangraj, Manophab; Boithias, Laurie; Xayyathip, Khampaseuth; Menjot, Ludovic
  title: Distribution of Burkholderia pseudomallei within a 300-cm deep soil profile: implications for environmental sampling
  journal: Dental science reports
  volume: 12
  issue: 1
  issued: 2022-05-23
  doi: 10.1038/s41598-022-12795-0
  url: https://scispace.com/papers/distribution-of-burkholderia-pseudomallei-within-a-300-cm-2tlrnjyg

[62]
  authors: Hogan; Wilmer; Badawi; Hoang; Chapman; Press; Antonation; Corbett; Romney; Murray
  title: Melioidosis in Trinidad and Tobago.
  source: PubMed
  issued: 2015
  doi: 10.3201/eid2105.141610
  url: https://pubmed.ncbi.nlm.nih.gov/25897877

[63]
  authors: Nyanasegran; Nathan; Firdaus-Raih; Muhammad; Ng
  title: Biofilm Signaling, Composition and Regulation in 
  source: PubMed
  issued: 2023
  doi: 10.4014/jmb.2207.07032
  url: https://pubmed.ncbi.nlm.nih.gov/36451302

[64]
  authors: Bzdyl; Moran; Bendo; Sarkar-Tyson
  title: Pathogenicity and virulence of 
  source: PubMed
  issued: 2022
  doi: 10.1080/21505594.2022.2139063
  url: https://pubmed.ncbi.nlm.nih.gov/36271712

[65]
  authors: Roe, Chandler C.; Vazquez, Adam J.; Phillips, P. D.; Allender, Christia; Bowden, Richard; Nottingham, Roxanne; Doyle, Adina; Wongsuwan, Gumphol; Wuthiekanun, Vanaporn; Limmathurotsakul, Direk; Peacock, Sharon J.
  title: Multiple phylogenetically-diverse, differentially-virulent Burkholderia pseudomallei isolated from a single soil sample collected in Thailand
  journal: PLOS Neglected Tropical Diseases
  volume: 16
  issue: 2
  pages: e0010172-e0010172
  issued: 2022-02-01
  doi: 10.1371/journal.pntd.0010172
  url: https://scispace.com/papers/multiple-phylogenetically-diverse-differentially-virulent-225sypre

[66]
  authors: Webb, Jessica R.; Win, Mo Mo; Zin, Khwar Nyo; Win, Kyi Kyi Nyein; Wah, Thin Thin; Ashley, Elizabeth A.; Smithuis, Frank; Swe, Myo Maung Maung; Mayo, Mark; Currie, Bart J.; Dance, David A. B.
  title: Myanmar Burkholderia pseudomallei strains are genetically diverse and originate from Asia with phylogenetic evidence of reintroductions from neighbouring countries
  journal: Scientific Reports
  volume: 10
  issue: 1
  pages: 16260
  issued: 2020-10-01
  doi: 10.1038/S41598-020-73545-8
  url: https://scispace.com/papers/myanmar-burkholderia-pseudomallei-strains-are-genetically-59098ej3s1

[67]
  authors: Gee, Jay E.; Gulvik, Christopher A.; Castelo-Branco, Débora de Souza Collares Maia; Sidrim, José Júlio Costa; Rocha, Marcos Fábio Gadelha; Rocha, Marcos Fábio Gadelha; Cordeiro, Rossana de Aguiar; Brilhante, Raimunda Sâmia Nogueira; Bandeira, Tereza de Jesus Pinheiro Gomes; Patrício, Iracema; Alencar, Lucas Pereira de
  title: Genomic Diversity of Burkholderia pseudomallei in Ceara, Brazil
  volume: 6
  issue: 1
  issued: 2021-02-03
  doi: 10.1128/MSPHERE.01259-20
  url: https://scispace.com/papers/genomic-diversity-of-burkholderia-pseudomallei-in-ceara-41cpo6p4qn

[68]
  authors: Holden, Matthew T. G.; Titball, Richard W.; Titball, Richard W.; Peacock, Sharon J.; Peacock, Sharon J.; Cerdeño-Tárraga, Ana; Atkins, Timothy P.; Crossman, Lisa; Pitt, Tyrone; Churcher, Carol; Mungall, Karen
  title: Genomic plasticity of the causative agent of melioidosis, Burkholderia pseudomallei
  journal: Proceedings of the National Academy of Sciences of the United States of America
  volume: 101
  issue: 39
  pages: 14240-14245
  issued: 2004-09-28
  doi: 10.1073/PNAS.0403302101
  url: https://scispace.com/papers/genomic-plasticity-of-the-causative-agent-of-melioidosis-zoisqknop4

[69]
  authors: Nandi, Tannistha; Holden, Matthew T. G.; Didelot, Xavier; Mehershahi, Kurosh S.; Boddey, Justin A; Beacham, Ifor R.; Peak, Ian R.; Harting, John; Baybayan, Primo; Guo, Yan; Wang, Susana
  title: Burkholderia pseudomallei sequencing identifies genomic clades with distinct recombination, accessory and epigenetic profiles
  journal: Genome Research
  volume: 25
  issue: 1
  pages: 129-141
  issued: 2015-01-01
  doi: 10.1101/GR.177543.114
  url: https://scispace.com/papers/burkholderia-pseudomallei-sequencing-identifies-genomic-41xxb6g5nt

[70]
  authors: Gairola, Ajay Krishan
  title: Clinical Burkholderia pseudomallei isolates from north Queensland carry diverse bimABm genes that are associated with central nervous system disease and are phylogenomically distinct from other Australian strains
  journal: PLOS Neglected Tropical Diseases
  volume: 16
  issue: 6
  pages: e0009482-e0009482
  issued: 2022-06-14
  doi: 10.1371/journal.pntd.0009482
  url: https://scispace.com/papers/clinical-burkholderia-pseudomallei-isolates-from-north-2xhy9clk

[71]
  authors: Price, Erin P.; Currie, Bart J.; Sarovich, Derek S.
  title: Genomic Insights Into the Melioidosis Pathogen, Burkholderia pseudomallei
  journal: Current tropical medicine reports
  volume: 4
  issue: 3
  pages: 95-102
  issued: 2017-09-01
  doi: 10.1007/S40475-017-0111-9
  url: https://scispace.com/papers/genomic-insights-into-the-melioidosis-pathogen-burkholderia-3tytijz1ou

[72]
  authors: Price, Erin P.; Sarovich, Derek S.; Smith, Emma J.; MacHunter, Barbara; Harrington, Glenda; Theobald, Vanessa; Hall, Carina M.; Hornstra, Heidie; McRobb, Evan; Podin, Yuwana; Mayo, Mark
  title: Unprecedented Melioidosis Cases in Northern Australia Caused by an Asian Burkholderia pseudomallei Strain Identified by Using Large-Scale Comparative Genomics
  journal: Applied and Environmental Microbiology
  volume: 82
  issue: 3
  pages: 954-963
  issued: 2016-02-01
  doi: 10.1128/AEM.03013-15
  url: https://scispace.com/papers/unprecedented-melioidosis-cases-in-northern-australia-caused-262t19tr4g

[73]
  authors: Zheng, Hongyuan; Qin, Jingliang; Chen, Hai; Hu, Hongyan; Zhang, Xiang-Li-Lan; Yang, Chao; Wu, Yarong; Li, Yuanli; Li, Sha; Kuang, Huihui; Zhou, Hanwang
  title: Genetic diversity and transmission patterns of Burkholderia pseudomallei on Hainan island, China, revealed by a population genomics analysis.
  volume: 7
  issue: 11
  issued: 2021-11-01
  doi: 10.1099/MGEN.0.000659
  url: https://scispace.com/papers/genetic-diversity-and-transmission-patterns-of-burkholderia-34p25hgegi

[74]
  authors: Sarovich, Derek S.; Garin, Benoit; Smet, Birgit De; Smet, Birgit De; Kaestli, Mirjam; Mayo, Mark; Vandamme, Peter; Jacobs, Jan; Jacobs, Jan; Lompo, Palpouguini; Tahita, Marc Christian
  title: Phylogenomic Analysis Reveals an Asian Origin for African Burkholderia pseudomallei and Further Supports Melioidosis Endemicity in Africa.
  volume: 1
  issue: 2
  pages: 1-12
  issued: 2016-04-27
  doi: 10.1128/MSPHERE.00089-15
  url: https://scispace.com/papers/phylogenomic-analysis-reveals-an-asian-origin-for-african-3tgif5j1xn

[75]
  authors: Dale, Julia; Price, Erin P.; Hornstra, Heidie; Busch, Joseph D.; Mayo, Mark; Godoy, Daniel; Wuthiekanun, Vanaporn; Baker, Anthony L.; Foster, Jeffrey T.; Wagner, David M.; Tuanyok, Apichai
  title: Epidemiological Tracking and Population Assignment of the Non-Clonal Bacterium, Burkholderia pseudomallei
  journal: PLOS Neglected Tropical Diseases
  volume: 5
  issue: 12
  pages: 1-17
  issued: 2011-12-13
  doi: 10.1371/JOURNAL.PNTD.0001381
  url: https://scispace.com/papers/epidemiological-tracking-and-population-assignment-of-the-qch0892i6s

[76]
  authors: Ghazali, Ahmad-Kamal; Eng, Su-Anne; Khoo, Jia Shiun; Teoh, Seddon; Hoh, Chee-Choong; Nathan, Sheila
  title: Whole-genome comparative analysis of Malaysian Burkholderia pseudomallei clinical isolates
  issued: 2024-07-01
  doi: 10.60692/61rky-rxb55
  url: https://scispace.com/papers/whole-genome-comparative-analysis-of-malaysian-burkholderia-wpvgyz49e2um

[77]
  authors: Yu, Yiting; Kim, H. Stanley; Chua, Hui Hoon; Lin, Chi Ho; Sim, Siew Hoon; Lin, Daoxun; Derr, Alan; Engels, Reinhard; DeShazer, David; Birren, Bruce W.; Nierman, William C.
  title: Genomic patterns of pathogen evolution revealed by comparison of Burkholderia pseudomallei , the causative agent of melioidosis, to avirulent Burkholderia thailandensis
  journal: BMC Microbiology
  volume: 6
  issue: 1
  pages: 46-46
  issued: 2006-05-26
  doi: 10.1186/1471-2180-6-46
  url: https://scispace.com/papers/genomic-patterns-of-pathogen-evolution-revealed-by-2pxltjhn8g

[78]
  authors: Tumapa, Sarinna; Holden, Matthew T G; Vesaratchavest, Mongkol; WUTHIEKANUN, VANAPORN; Limmathurotsakul, Direk; Chierakul, Wirongrong; Feil, Edward J.; Currie, Bart J.; Day, Nicholas; Nierman, William C.; Peacock, Sharon J.
  title: Burkholderia pseudomallei genome plasticity associated with genomic island variation
  issued: 2024-07-17
  doi: 10.60692/24gbn-k1245
  url: https://scispace.com/papers/burkholderia-pseudomallei-genome-plasticity-associated-with-owu3bdssarvj

[79]
  authors: Spring-Pearson, Senanu; Stone, Joshua K.; Doyle, Adina; Allender, Christopher J.; Okinaka, Richard T.; Mayo, Mark; Broomall, S. M.; Hill, Jessica M.; Karavis, Mark; Hubbard, Kyle S.; Insalaco, Joseph M.
  title: Pangenome Analysis of Burkholderia pseudomallei: Genome Evolution Preserves Gene Order despite High Recombination Rates
  journal: PLOS ONE
  volume: 10
  issue: 10
  pages: 140274
  issued: 2015-10-20
  doi: 10.1371/JOURNAL.PONE.0140274
  url: https://scispace.com/papers/pangenome-analysis-of-burkholderia-pseudomallei-genome-4ck69ndse7

[80]
  authors: Seng, Ratha; Tandhavanant, Sarunporn; Saiprom, Natnaree; Phunpang, Rungnapa; Chomkatekaew, C.; Thaipadungpanit, Janjira; Batty, Elizabeth M.; Thomson, Nicholas R.; Chantratita, Wasun; West, T. Eoin; Chewapreecha, Claire
  title: Genetic diversity, determinants, and dissemination of Burkholderia pseudomallei lineages implicated in melioidosis in northeast Thailand
  journal: Nature Communications
  volume: 15
  pages: 5699
  issued: 2024-07-03
  doi: 10.1038/s41467-024-49939-3
  pmid: 38972886
  url: https://pubmed.ncbi.nlm.nih.gov/38972886

[81]
  authors: Pearson, Talima; Giffard, Philip M.; Giffard, Philip M.; Beckstrom-Sternberg, Stephen M.; Beckstrom-Sternberg, Stephen M.; Auerbach, Raymond K.; Auerbach, Raymond K.; Hornstra, Heidie; Tuanyok, Apichai; Price, Erin P.; Price, Erin P.
  title: Phylogeographic reconstruction of a bacterial species with high levels of lateral gene transfer
  journal: BMC Biology
  volume: 7
  issue: 1
  pages: 78-78
  issued: 2009-11-18
  doi: 10.1186/1741-7007-7-78
  url: https://scispace.com/papers/phylogeographic-reconstruction-of-a-bacterial-species-with-2m0xc5we4a

[82]
  authors: Baker; Pearson; Sahl; Hepp; Price; Sarovich; Mayo; Tuanyok; Currie; Keim; Warner
  title: Burkholderia pseudomallei distribution in Australasia is linked to paleogeographic and anthropogenic history.
  source: PubMed
  issued: 2018
  doi: 10.1371/journal.pone.0206845
  url: https://pubmed.ncbi.nlm.nih.gov/30395628

[83]
  authors: Cheng, Allen C.; Cheng, Allen C.; Ward, Linda; Ward, Linda; Godoy, Daniel; Norton, Robert; Mayo, Mark; Gal, Daniel; Spratt, Brian G.; Currie, Bart J.; Currie, Bart J.
  title: Genetic Diversity of Burkholderia pseudomallei Isolates in Australia
  journal: Journal of Clinical Microbiology
  volume: 46
  issue: 1
  pages: 249-254
  issued: 2008-01-01
  doi: 10.1128/JCM.01725-07
  url: https://scispace.com/papers/genetic-diversity-of-burkholderia-pseudomallei-isolates-in-se4bheizid

[84]
  authors: Sahl, Jason W.; Allender, Christopher J.; Colman, Rebecca E.; Califf, Katy J.; Schupp, James M.; Currie, Bart J.; Zandt, Kristopher E. Van; Gelhaus, H. Carl; Keim, Paul; Tuanyok, Apichai
  title: Genomic Characterization of Burkholderia pseudomallei Isolates Selected for Medical Countermeasures Testing: Comparative Genomics Associated with Differential Virulence
  journal: PLOS ONE
  volume: 10
  issue: 3
  pages: 1-18
  issued: 2015-03-24
  doi: 10.1371/JOURNAL.PONE.0121052
  url: https://scispace.com/papers/genomic-characterization-of-burkholderia-pseudomallei-326pnaovrw

[85]
  authors: Aziz, Ammar; Sarovich, Derek S.; Sarovich, Derek S.; Harris, Tegan M.; Kaestli, Mirjam; McRobb, Evan; Mayo, Mark; Currie, Bart J.; Price, Erin P.; Price, Erin P.
  title: Suspected cases of intracontinental Burkholderia pseudomallei sequence type homoplasy resolved using whole-genome sequencing.
  volume: 3
  issue: 11
  pages: 1-8
  issued: 2017-11-14
  doi: 10.1099/MGEN.0.000139
  url: https://scispace.com/papers/suspected-cases-of-intracontinental-burkholderia-1bdiicufsu

[86]
  authors: Sim, Siew Hoon; Yu, Yiting; Lin, Chi-Ho; Karuturi, R. Krishna Murthy; WUTHIEKANUN, VANAPORN; Tuanyok, Apichai; Chua, Hui-Hoon; Ong, Catherine; Paramalingam, Sivalingam Suppiah; Tan, Gladys; Tang, Lynn L. H.
  title: The Core and Accessory Genomes of Burkholderia pseudomallei: Implications for Human Melioidosis
  issued: 2024-07-17
  doi: 10.60692/cz9ey-8tf54
  url: https://scispace.com/papers/the-core-and-accessory-genomes-of-burkholderia-pseudomallei-mynx8j5vjth1

[87]
  authors: Gee; Gulvik; Elrod; Batra; Rowe; Sheth; Hoffmaster
  title: Phylogeography of Burkholderia pseudomallei Isolates, Western Hemisphere.
  source: PubMed
  issued: 2017
  doi: 10.3201/eid2307.161978
  url: https://pubmed.ncbi.nlm.nih.gov/28628442

[88]
  authors: Hall, Carina M.; Jaramillo, Sierra A.; Jimenez, Rebecca; Stone, Nathan E.; Centner, Heather; Busch, Joseph D.; Bratsch, Nicole; Roe, Chandler C.; Gee, Jay E.; Hoffmaster, Alex R.; Rivera-Garcia, Sarai
  title: Burkholderia pseudomallei, the causative agent of melioidosis, is rare but ecologically established and widely dispersed in the environment in Puerto Rico.
  journal: PLOS Neglected Tropical Diseases
  volume: 13
  issue: 9
  issued: 2019-09-05
  doi: 10.1371/JOURNAL.PNTD.0007727
  url: https://scispace.com/papers/burkholderia-pseudomallei-the-causative-agent-of-melioidosis-3rbxrz8e2x

[89]
  authors: Chewapreecha, Claire; Mather, Alison E.; Harris, Simon R.; Hunt, Martin; Holden, Matthew T G; Chaichana, Chutima; WUTHIEKANUN, VANAPORN; Dougan, Gordon; Day, Nicholas; Limmathurotsakul, Direk; Parkhill, Julian
  title: Genetic variation associated with infection and the environment in the accidental pathogen Burkholderia pseudomallei
  issued: 2024-07-11
  doi: 10.60692/hb63a-ka807
  url: https://scispace.com/papers/genetic-variation-associated-with-infection-and-the-hqjqsaeu41t2

[90]
  authors: Chantratita, Narisara; WUTHIEKANUN, VANAPORN; Limmathurotsakul, Direk; Vesaratchavest, Mongkol; Thanwisai, Aunchalee; Amornchai, Premjit; Tumapa, Sarinna; Feil, Edward J.; Day, Nicholas; Peacock, Sharon J.
  title: Genetic Diversity and Microevolution of Burkholderia pseudomallei in the Environment
  issued: 2024-07-17
  doi: 10.60692/1c336-9ae69
  url: https://scispace.com/papers/genetic-diversity-and-microevolution-of-burkholderia-2nkgl5e14cm2

[91]
  authors: Smet, Birgit De; Sarovich, Derek S.; Price, Erin P.; Mayo, Mark; Theobald, Vanessa; Kham, Chun; Heng, Seiha; Thong, Phe; Holden, Matthew T. G.; Parkhill, Julian; Peacock, Sharon J.
  title: Whole-Genome Sequencing Confirms that Burkholderia pseudomallei Multilocus Sequence Types Common to Both Cambodia and Australia Are Due to Homoplasy
  journal: Journal of Clinical Microbiology
  volume: 53
  issue: 1
  pages: 323-326
  issued: 2015-01-01
  doi: 10.1128/JCM.02574-14
  url: https://scispace.com/papers/whole-genome-sequencing-confirms-that-burkholderia-4ycydp0kzx

[92]
  authors: Meumann, Ella M.; Kaestli, Mirjam; Mayo, Mark; Ward, Linda; Rachlin, Audrey; Webb, Jessica R.; Kleinecke, Mariana; Price, Erin P.; Currie, Bart J.
  title: Emergence of Burkholderia pseudomallei Sequence Type 562, Northern Australia.
  journal: Emerging Infectious Diseases
  volume: 27
  issue: 4
  pages: 1057-1067
  issued: 2021-01-01
  doi: 10.3201/EID2704.202716
  url: https://scispace.com/papers/emergence-of-burkholderia-pseudomallei-sequence-type-562-4a711zx2ea

[93]
  authors: Aziz; Currie; Mayo; Sarovich; Price
  title: Comparative genomics confirms a rare melioidosis human-to-human transmission event and reveals incorrect phylogenomic reconstruction due to polyclonality.
  source: PubMed
  issued: 2020
  doi: 10.1099/mgen.0.000326
  url: https://pubmed.ncbi.nlm.nih.gov/31958055

[94]
  authors: Sawana, Amandeep; Adeolu, Mobolaji; Gupta, Radhey S.
  title: Molecular signatures and phylogenomic analysis of the genus Burkholderia: proposal for division of this genus into the emended genus Burkholderia containing pathogenic organisms and a new genus Paraburkholderia gen. nov. harboring environmental species
  journal: Frontiers in Genetics
  volume: 5
  pages: 429-429
  issued: 2014-12-19
  doi: 10.3389/FGENE.2014.00429
  url: https://scispace.com/papers/molecular-signatures-and-phylogenomic-analysis-of-the-genus-2wlgvrtnyy

[95]
  authors: Sahl, Jason W.; Sahl, Jason W.; Vazquez, Adam J.; Hall, Carina M.; Busch, Joseph D.; Tuanyok, Apichai; Mayo, Mark; Schupp, James M.; Lummis, Madeline; Pearson, Talima; Shippy, Kenzie
  title: The Effects of Signal Erosion and Core Genome Reduction on the Identification of Diagnostic Markers
  journal: Mbio
  volume: 7
  issue: 5
  pages: 16
  issued: 2016-11-02
  doi: 10.1128/MBIO.00846-16
  url: https://scispace.com/papers/the-effects-of-signal-erosion-and-core-genome-reduction-on-11c91c2fpe

[96]
  authors: Diniz, Michely C.; Farias, Kaio Moraes de; Pacheco, Alexandra P.; Viana, Daniel de Araújo; Araujo-Filho, R.; Lima, A. P.; Costa, Raimundo Beserra da; Oliveira, Diana
  title: Análise Genômica de Burkholderia mallei e Burkholderia pseudomallei: Dois Patógenos de Primeira Grandeza e de Genomas Surpreendentemente Complexos
  volume: 2
  issue: 1
  pages: 1-34
  issued: 2008-06-30
  doi: 10.5935/RBHSA.V2I1.39
  url: https://scispace.com/papers/analise-genomica-de-burkholderia-mallei-e-burkholderia-545zyey8ck

[97]
  authors: Hanage, William P.; Fraser, Christophe; Spratt, Brian G.
  title: Sequences, sequence clusters and bacterial species.
  journal: Philosophical Transactions of the Royal Society B
  volume: 361
  issue: 1475
  pages: 1917-1927
  issued: 2006-11-29
  doi: 10.1098/RSTB.2006.1917
  url: https://scispace.com/papers/sequences-sequence-clusters-and-bacterial-species-2hzb1082qz

[98]
  authors: Wuthiekanun, Vanaporn; Limmathurotsakul, Direk; Chantratita, Narisara; Feil, Edward J.; Day, Nicholas P. J.; Day, Nicholas P. J.; Peacock, Sharon J.; Peacock, Sharon J.; Peacock, Sharon J.
  title: Burkholderia Pseudomallei is genetically diverse in agricultural land in Northeast Thailand.
  journal: PLOS Neglected Tropical Diseases
  volume: 3
  issue: 8
  issued: 2009-08-04
  doi: 10.1371/JOURNAL.PNTD.0000496
  url: https://scispace.com/papers/burkholderia-pseudomallei-is-genetically-diverse-in-3drtvy5z6v

[99]
  authors: Lichtenegger, Sonja; Beutl, Stefan; Zingl, Franz G.; Seitz, Thomas; Schöfl, Gerhard; Steinmetz, Ivo
  title: Whole-Genome-Based Cluster Analysis of Burkholderia pseudomallei Isolates from a Non-Endemic Country Reveals Unexpected Genomic Diversity
  journal: Journal of Clinical Microbiology
  volume: 59
  issue: 5
  pages: e02519-20
  issued: 2021-04-20
  doi: 10.1128/JCM.02519-20
  pmid: 33980649
  url: https://pubmed.ncbi.nlm.nih.gov/33980649

[100]
  authors: Jolley, Keith A.; Bray, James E.; Maiden, Martin C. J.
  title: Open-access bacterial population genomics: BIGSdb software, the PubMLST.org website and their applications
  journal: Wellcome Open Research
  volume: 3
  pages: 124
  issued: 2018-09-24
  doi: 10.12688/wellcomeopenres.14826.1
  pmid: 30345391
  url: https://pubmed.ncbi.nlm.nih.gov/30345391

[101]
  authors: Petras, Jessica K.; Gee, Jay E.; Elrod, Mindy G.; Hoffmaster, Alex R.; Bower, William A.; Yu, Patricia A.; Blaney, David D.; Weiner, Zachary P.; Vaeth, Emmajean; Ravindra, Arun; Liu, Bo; Shadomy, Sean V.; Lowe, William; Johnston, Alicia; Wester, Amy L.; Sutton, Zachary M.; Quinn, Courtney L.; Braden, Christopher R.; Kenyon, Thilanthe; Kallen, Alexander J.
  title: Locally Acquired Melioidosis — United States, 2022
  journal: New England Journal of Medicine
  volume: 389
  issue: 23
  pages: 2116-2127
  issued: 2023-12-07
  doi: 10.1056/NEJMoa2305248
  pmid: 38118023
  url: https://pubmed.ncbi.nlm.nih.gov/38118023

[102]
  authors: Viberg, Linda T.; Bauer, Mihail J.; Sarovich, Derek S.; Drigo, Barbara; Kaestli, Mirjam; Mayo, Mark; Price, Erin P.; Currie, Bart J.; Kurtböke, Ipek; Kurtböke, D. Ipek
  title: Comparative Genomics Reveals Cystic Fibrosis Burkholderia pseudomallei Isolates Share a Novel Genomic Island and Gene Clusters
  journal: mBio
  volume: 8
  issue: 2
  pages: e00356-17
  issued: 2017-04-11
  doi: 10.1128/mBio.00356-17
  pmid: 28400528
  url: https://pubmed.ncbi.nlm.nih.gov/28400528

[103] Brennan, B.G.; et al.
  title: Locally Acquired Melioidosis in Georgia, United States, 1983–2024
  journal: Emerging Infectious Diseases
  year: 2025
  pmid: 40835221
  doi: 10.3201/eid3107.250235

[104] Tuanyok, A.; et al.
  title: PenA Mutations and Amplification Conferring Ceftazidime Resistance in Burkholderia pseudomallei
  journal: Antimicrobial Agents and Chemotherapy
  year: 2025
  doi: 10.1128/aac.00220-25

[105] Chirakul, S.; et al.
  title: Promoter Mutation in nlpD1–penA Intergenic Region Drives Constitutive PenA Overexpression and Extended Beta-Lactam Resistance
  journal: Scientific Reports
  year: 2018
  doi: 10.1038/S41598-018-28843-7

[106] Chirakul, S.; et al.
  title: penA Gene Duplication and Amplification Conferring Reversible Ceftazidime Resistance in Burkholderia pseudomallei
  journal: International Journal of Antimicrobial Agents
  year: 2019
  doi: 10.1016/J.IJANTIMICAG.2019.01.003

[107] Chantratita, N.; et al.
  title: Deletion of bpss1219 Encoding PBP3 Generates Slow-Growing High-Level Ceftazidime-Resistant Variants
  journal: Proceedings of the National Academy of Sciences
  year: 2011
  doi: 10.1073/pnas.1111020108

[108] Sarovich, D.S.; et al.
  title: Efflux-Mediated Meropenem Resistance Emerging During Treatment: Analysis of Eleven Paired Clinical Isolates
  journal: Clinical Infectious Diseases
  year: 2018
  doi: 10.1093/CID/CIY069

[109] Schnetterle, M.; et al.
  title: BpeEF-OprC Upregulation Conferring Transient TMP-SMX Resistance and Co-selecting Multidrug Resistance in Burkholderia pseudomallei
  journal: PLOS Neglected Tropical Diseases
  year: 2021
  doi: 10.1371/JOURNAL.PNTD.0008913

[110] Madden, D.E.; et al.
  title: ARDaP: A WGS-Based Genomic Tool for Resistance Prediction in Burkholderia pseudomallei from Mixed Clinical Populations
  journal: bioRxiv
  year: 2019
  doi: 10.1101/720607

[111] Webb, J.R.; et al.
  title: Triplex RT-qPCR Assay for Rapid Detection of amrB/bpeB/bpeF Efflux Upregulation in Clinical Burkholderia pseudomallei Pairs
  journal: bioRxiv
  year: 2018
  doi: 10.1101/301960

[112] Gassiep, I.; et al.
  title: La Niña-Associated Flooding and Melioidosis Outbreak in Southern Queensland: WGS Confirmation of Local Acquisition
  journal: American Journal of Tropical Medicine and Hygiene
  year: 2023
  doi: 10.4269/ajtmh.23-0002

[113] Webb, J.R.; et al.
  title: Temperate Western Australian Burkholderia pseudomallei Focus at 31.6°S Persisting Over Five Decades: Activation After Rainfall
  journal: mSystems
  year: 2020
  doi: 10.1128/MSYSTEMS.00726-20

[114] Chen, Y.; et al.
  title: Taiwan Long-Term Soil Surveillance: Burkholderia pseudomallei PCR Positivity Rising from 77.7% to 97.4% After Heavy Rainfall
  journal: Tropical Medicine and International Health
  year: 2025
  doi: 10.1111/tmi.70047

[115] Ganeshalingam, S.; et al.
  title: Townsville Melioidosis Incidence Approximately Three-Fold Higher When Fortnightly Rainfall Exceeds 200 mm
  journal: Environmental Health and Preventive Medicine
  year: 2023
  doi: 10.1265/ehpm.22-00177

[116] Anh, N.T.; et al.
  title: Vietnamese Paddy Field Burkholderia pseudomallei Culture Positivity: 5% (Winter) to 82% (Summer); Spearman's ρ = 0.905 with Temperature
  journal: PLOS Neglected Tropical Diseases
  year: 2025
  doi: 10.1371/journal.pntd.0013322

[117] Tai, W.C.; et al.
  title: Taiwan 2024 Typhoon Season Associated with Unprecedented Melioidosis Surge
  journal: American Journal of Tropical Medicine and Hygiene
  year: 2025
  doi: 10.4269/ajtmh.25-0074

[118] Li, X.; et al.
  title: Global MaxEnt Projections of Animal Melioidosis Habitat Suitability Under Future Climate Scenarios
  journal: Animals
  year: 2025
  doi: 10.3390/ani15030455

[119] Abrantes, P.; et al.
  title: Southeast Asian MaxEnt Niche Modelling: Thermal Floor ≥26°C Wettest Quarter as Key Determinant of Burkholderia pseudomallei Habitat Suitability
  journal: PLOS Neglected Tropical Diseases
  year: 2025
  doi: 10.1371/journal.pntd.0012684

[120] Birnie, E.; et al.
  title: Drivers of Melioidosis Endemicity: Climate Change, Land Use, and Range Expansion
  journal: Current Opinion in Infectious Diseases
  year: 2022
  doi: 10.1097/QCO.0000000000000827

[121] Currie, B.J.; et al.
  title: Melioidosis: Global Epidemiology, Expanding Footprint, Climate and Ecology Drivers
  journal: American Journal of Tropical Medicine and Hygiene
  year: 2023
  doi: 10.4269/ajtmh.23-0223

[122] Meumann, E.M.; et al.
  title: Burkholderia pseudomallei and Melioidosis
  journal: Nature Reviews Microbiology
  year: 2023
  doi: 10.1038/s41579-023-00972-5

[123] Hai, W.; et al.
  title: ST562 Identified in Both Australia and Southern China: Intercontinental Sharing of a Burkholderia pseudomallei Sequence Type
  year: 2024
  doi: 10.60692/x9erj-5ns21

[124] Lichtenegger, S.; et al.
  title: Formal Development and Validation of the 4,221-Locus Core-Genome MLST Scheme for Burkholderia pseudomallei
  year: 2024
  doi: 10.60692/gcrsm-rep55

[125] Webb, J.R.; et al.
  title: WGS Links Individual Human Melioidosis Cases to Targeted Environmental Sampling Sites in Northern Australia
  journal: Journal of Clinical Microbiology
  year: 2022
  doi: 10.1128/jcm.01648-21

[126] Chewapreecha, C.; et al.
  title: GWAS Identifies Genomic Loci Associated with Clinical vs Environmental Burkholderia pseudomallei Phenotype
  year: 2024
  doi: 10.60692/qkg23-g5s28

[127] Gasqué, P.; et al.
  title: PCR–High Resolution Melt Assay for Geographic Origin Assignment of Burkholderia pseudomallei: Caribbean and Indian Ocean Isolates
  journal: Infection, Genetics and Evolution
  year: 2024
  doi: 10.1016/j.meegid.2024.105711

[128] Espitia-Acero, A.; et al.
  title: Genomic Characterisation of Colombian Burkholderia pseudomallei Confirms Africa–Americas Clade
  year: 2024
  doi: 10.60692/s4k6y-99607

[129] Busch, J.D.; et al.
  title: Multiple Co-Circulating Burkholderia pseudomallei Lineages at a Single Australian Farm: Veterinary and Pastoral Exposure Complexity
  journal: PLOS Neglected Tropical Diseases
  year: 2024
  doi: 10.1371/journal.pntd.0012683

[130] Wu, A.K.L.; et al.
  title: Urban Hong Kong Airborne Melioidosis Outbreak Following Typhoon Mangkhut: cgMLST Links Aerosol-Derived Isolate to Clinical Cases
  year: 2023
  doi: 10.6084/m9.figshare.22730058

## References

> ## ⚠ This list is not the bibliography the prose above cites
>
> Measured 2026-09-04. The prose follows the machine-readable block earlier in
> this file, not this list. The two agree on `[1]` through `[40]` and disagree
> from `[41]` on, because two entries were inserted into one and not the other.
>
> Of the 277 citation marks in the prose, 102 land on the paper the sentence
> means, **136 land on a different paper**, and 36 land on nothing. Of the 96
> entries below, 54 name a work the citing sentence is not about.
>
> Nothing below `[41]` may be quoted, moved or cited without being resolved
> against a primary record first. The block earlier in this file is aligned with
> the prose but its entries carry invented titles and mismatched identifiers, so
> it is not a usable replacement either.
>
> Full measurement and per-number detail:
> `BACKGROUND_BIBLIOGRAPHY_DEFECT_2026-09-04.md` and
> `BACKGROUND_BIBLIO_COMPARISON.tsv`. The nine references verified so far are in
> `REFERENCES_RESOLVED_2026-09-03.md`; `[102]` is closed as unsupported.


[1]D. Thangaraju, V. Sundaramoorthy, and V. Thiagarajan, “P-148. Melioidosis: A Seven-Year Review (2017-2023),” Open Forum Infectious Diseases, vol. 12, no. Supplement_1, Jan. 2025, doi: 10.1093/ofid/ofae631.353.

[2]P. R. Mohapatra, B. Behera, and B. Mishra, “Melioidosis: An Indian Perspective,” Journal of Association of Physicians of India, vol. 73, no. 5, pp. 63–68, Jan. 2025, doi: 10.59556/japi.73.0945.

[3]B. J. Currie, “Melioidosis: Evolving Concepts in Epidemiology, Pathogenesis, and Treatment,” Seminars in Respiratory and Critical Care Medicine, vol. 36, no. 1, pp. 111–125, Feb. 2015, doi: 10.1055/S-0034-1398389.

[4]P. K. Mohapatra and B. Mishra, “Burden of melioidosis in India and South Asia: Challenges and ways forward,” The Lancet regional health, vol. 2, pp. 100004–100004, May 2022, doi: 10.1016/j.lansea.2022.03.004.

[5]F. Norman, B. M. Blair, S. Chamorro-Tojeiro, M. Sanz, and L. H. Chen, “The Evolving Global Epidemiology of Human Melioidosis,” Sept. 2024, doi: 10.20944/preprints202409.1336.v1.

[6]W. Mahikul et al., “Modelling population dynamics and seasonal movement to assess and predict the burden of melioidosis.,” PLOS Neglected Tropical Diseases, vol. 13, no. 5, May 2019, doi: 10.1371/JOURNAL.PNTD.0007380.

[7]M. Dias and A. L. Dias, “Emerging pathogen Burkholderia pseudomallei: what do we know,” Indian Journal of Microbiology Research, vol. 2, no. 1, pp. 50–54, Jan. 2015.

[8]S. Chowdhury et al., “The Epidemiology of Melioidosis and Its Association with Diabetes Mellitus: A Systematic Review and Meta-Analysis,” Pathogens, vol. 11, no. 2, pp. 149–149, Jan. 2022, doi: 10.3390/pathogens11020149.

[9]I. Mazhar, S. Andalib, R. Alim, and S. Munwar, “An update on Burkholderia pseudomallei infection: epidemiology, pathogenesis, diagnostic approaches and treatment challenges,” vol. 21, no. 1, pp. 100–106, June 2025, doi: 10.3329/jmcwh.v21i1.81187.

[10]Y. Buisson, “[A multi-resistant bacterium before the era of antibiotics : the agent of melioidosis].,” Comptes Rendus Biologies, Aug. 2023, doi: 10.5802/crbiol.109.

[11]“Melioidosis: The Soil-Borne Disease in Thai Communities,” Aug. 2025, doi: 10.5281/zenodo.16899388.

[12]F. Norman, B. M. Blair, S. Chamorro-Tojeiro, M. Sanz, and L. H. Chen, “The Evolving Global Epidemiology of Human Melioidosis: A Narrative Review,” Pathogens, vol. 13, no. 11, pp. 926–926, Oct. 2024, doi: 10.3390/pathogens13110926.

[13]S. F. Jiee, K. J. Lim, D. S. C. Vui, D. P. Marius, N. S. Illyana, and A. Jantim, “Extreme Weather and Melioidosis: An endemic tropical disease in Penampang district of Sabah, Malaysia,” Journal of Health Research, vol. 37, no. 5, Mar. 2023, doi: 10.56808/2586-940x.1023.

[14]F. F. Norman and L. Chen, “Travel-associated Melioidosis: a narrative review.,” Journal of Travel Medicine, vol. 30, no. 3, Mar. 2023, doi: 10.1093/jtm/taad039.

[15]J. D. Stewart et al., “The epidemiology and clinical features of melioidosis in Far North Queensland: Implications for patient management.,” PLOS Neglected Tropical Diseases, vol. 11, no. 3, pp. 1–15, Mar. 2017, doi: 10.1371/JOURNAL.PNTD.0005411.

[16]B. J. Currie, L. Ward, and A. C. Cheng, “The epidemiology and clinical spectrum of melioidosis: 540 cases from the 20 year Darwin prospective study.,” PLOS Neglected Tropical Diseases, vol. 4, no. 11, pp. 1–11, Nov. 2010, doi: 10.1371/JOURNAL.PNTD.0000900.

[17]B. J. Currie et al., “Melioidosis epidemiology and risk factors from a prospective whole-population study in northern Australia,” Tropical Medicine & International Health, vol. 9, no. 11, pp. 1167–1174, Nov. 2004, doi: 10.1111/J.1365-3156.2004.01328.X.

[18]J. H. Fong, N. Pillai, C. G. Yap, and N. K. Jahan, “Incidences, Case Fatality Rates and Epidemiology of Melioidosis Worldwide: A Review Paper,” Open Access Library Journal, vol. 8, no. 06, pp. 1–20, June 2021, doi: 10.4236/OALIB.1107537.

[19]P.-S. Chen et al., “Airborne Transmission of Melioidosis to Humans from Environmental Aerosols Contaminated with B. pseudomallei.,” PLOS Neglected Tropical Diseases, vol. 9, no. 6, June 2015, doi: 10.1371/JOURNAL.PNTD.0003834.

[20]K. L. Schully et al., “Melioidosis in lower provincial Cambodia: A case series from a prospective study of sepsis in Takeo Province.,” PLOS Neglected Tropical Diseases, vol. 11, no. 9, p. 0005923, Sept. 2017, doi: 10.1371/JOURNAL.PNTD.0005923.

[21]B. J. Currie, “Melioidosis: an important cause of pneumonia in residents of and travellers returned from endemic regions,” European Respiratory Journal, vol. 22, no. 3, pp. 542–550, Sept. 2003, doi: 10.1183/09031936.03.00006203.

[22]J. Wongbutdee, J. Jittimanee, S. Dandee, P. Thongsang, and W. Saengnill, “Exploring the Relationship between Melioidosis Morbidity Rate and Local Environmental Indicators Using Remotely Sensed Data,” Apr. 2024, doi: 10.20944/preprints202404.0446.v1.

[23]M. R. A. Hassan et al., “Socio-epidemiological and land cover risk factors for melioidosis in Kedah, Northern Malaysia,” PLOS Neglected Tropical Diseases, vol. 13, no. 3, Mar. 2019, doi: 10.1371/JOURNAL.PNTD.0007243.

[24]C. Mukhopadhyay, T. Shaw, G. M. Varghese, D. A. B. Dance, D. A. B. Dance, and D. A. B. Dance, “Melioidosis in South Asia (India, Nepal, Pakistan, Bhutan and Afghanistan),” Tropical Medicine and Infectious Disease, vol. 3, no. 2, pp. 51–51, May 2018, doi: 10.3390/TROPICALMED3020051.

[25]“Next-generation sequencing for greater understanding of Burkholderia pseudomallei epidemiology and phylogeography in northern Australia and Vientiane, Laos,” June 2020, doi: 10.25913/5ed9d5e7129d4.

[26]B. J. Currie et al., “The Darwin Prospective Melioidosis Study: a 30-year prospective, observational investigation,” Lancet Infectious Diseases, vol. 21, no. 12, pp. 1737–1746, July 2021, doi: 10.1016/S1473-3099(21)00022-0.

[27]K. Selvam et al., “Burden and Risk Factors of Melioidosis in Southeast Asia: A Scoping Review,” International Journal of Environmental Research and Public Health, vol. 19, no. 23, pp. 15475–15475, Nov. 2022, doi: 10.3390/ijerph192315475.

[28]S. Chandrakar and M. Dias, “Clinico-epidemiological spectrum of melioidosis: a 2-year prospective study in the western coastal region of India,” Southern African Journal of Infectious Diseases, vol. 31, no. 1, pp. 14–19, Jan. 2016, doi: 10.1080/23120053.2015.1118830.

[29]E. Birnie, J. J. Biemond, and W. J. Wiersinga, “Drivers of melioidosis endemicity: epidemiological transition, zoonosis, and climate change,” Current Opinion in Infectious Diseases, vol. 35, pp. 196–204, Apr. 2022, doi: 10.1097/QCO.0000000000000827.

[30]H. Mtg et al., “Global and regional dissemination and evolution of $\textit{Burkholderia pseudomallei}$,” Mar. 2017, doi: 10.17863/cam.8171.

[31]I. Gassiep, M. Armstrong, and R. Norton, “Human Melioidosis”, doi: 10.1128/cmr.00006-19.

[32]D. Limmathurotsakul et al., “Predicted global distribution of Burkholderia pseudomallei and burden of melioidosis,” Nature microbiology, vol. 1, no. 1, pp. 15008–15008, Jan. 2016, doi: 10.1038/NMICROBIOL.2015.8.

[33]K. Ibrahem et al., “Burkholderia pseudomallei: A Multifaceted Threat and the Path Forward in Treatment and Prevention,” Infection and Drug Resistance, vol. Volume 18, pp. 5115–5127, Sept. 2025, doi: 10.2147/idr.s535624.

[34]A. C. Cheng, B. J. Currie, and B. J. Currie, “Melioidosis: Epidemiology, Pathophysiology, and Management,” Clinical Microbiology Reviews, vol. 18, no. 2, pp. 383–416, Apr. 2005, doi: 10.1128/CMR.18.2.383-416.2005.

[35]A. Chakravorty and C. H. Heath, “Melioidosis: An updated review,” Journal of general practice, vol. 48, no. 5, pp. 327–332, May 2019, doi: 10.31128/AJGP-04-18-4558.

[36]Jarrett, Seng, and Fitzgerald, “Paediatric melioidosis.,” Paediatric respiratory reviews, 2024, doi: 10.1016/j.prrv.2023.11.002.

[37]M. R. A. Hassan et al., “Incidence, risk factors and clinical epidemiology of melioidosis: a complex socio-ecological emerging infectious disease in the Alor Setar region of Kedah, Malaysia.,” BMC Infectious Diseases, vol. 10, no. 1, pp. 302–302, Oct. 2010, doi: 10.1186/1471-2334-10-302.

[38]S. Laklaeng et al., “A systematic review and meta-analysis of the global prevalence and relationships among Burkholderia pseudomallei sequence types isolated from humans, animals, and the environment,” July 2024, doi: 10.60692/3p1jp-gak33.

[39]D. Limmathurotsakul, S. J. Peacock, and S. J. Peacock, “Melioidosis: a clinical overview,” British Medical Bulletin, vol. 99, no. 1, pp. 125–139, Sept. 2011, doi: 10.1093/BMB/LDR007.

[40]N. Camargo et al., “A Young Diabetic Patient With Sepsis After Gardening.,” Open Forum Infectious Diseases, vol. 7, no. 5, May 2020, doi: 10.1093/OFID/OFAA159.

[41]V. T. N. Anh, Q. Tran, L. N. H. Bui, and T. T. Trung, “Seasonal change of Burkholderia pseudomallei in paddy field water strongly correlates with ambient temperature: A study in north-central Vietnam,” PLOS Neglected Tropical Diseases, vol. 19, no. 7, pp. e0013322–e0013322, July 2025, doi: 10.1371/journal.pntd.0013322.

[42]B. J. Currie, D. A. B. Dance, and A. C. Cheng, “The global distribution of Burkholderia pseudomallei and melioidosis: an update,” Transactions of The Royal Society of Tropical Medicine and Hygiene, vol. 102, pp. 1–4, Dec. 2008, doi: 10.1016/S0035-9203(08)70002-6.

[43]S. Amadasi et al., “A Case of Melioidosis Probably Acquired by Inhalation of Dusts During a Helicopter Flight in a Healthy Traveler Returning From Singapore,” Journal of Travel Medicine, vol. 22, no. 1, pp. 57–60, Jan. 2015, doi: 10.1111/JTM.12150.

[44]Venkatesan, Siritana, Silisouk, Roberts, Robinson, and Dance, “Burkholderia pseudomallei Bacteria in Ornamental Fish Tanks, Vientiane, Laos, 2023.,” Emerging infectious diseases, 2024, doi: 10.3201/eid3003.231674.

[45]E. Birnie et al., “Global burden of melioidosis in 2015: a systematic review and data synthesis,” Lancet Infectious Diseases, vol. 19, no. 8, pp. 892–902, Aug. 2019, doi: 10.1016/S1473-3099(19)30157-4.

[46]M. J. W. Kain, N. L. Reece, C. M. Parry, G. S. Rajahram, D. L. Paterson, and S. D. Woolley, “The Rapid Emergence of Hypervirulent Klebsiella Species and Burkholderia pseudomallei as Major Health Threats in Southeast Asia: The Urgent Need for Recognition as Neglected Tropical Diseases,” Tropical Medicine and Infectious Disease, Apr. 2024, doi: 10.3390/tropicalmed9040080.

[47]J. Savelkoel, D. A. B. Dance, B. J. Currie, D. Limmathurotsakul, and W. J. Wiersinga, “A call to action: time to recognise melioidosis as a neglected tropical disease,” July 2024, doi: 10.60692/cjp7n-g4756.

[48]O. Ribolzi et al., “Land use and soil type determine the presence of the pathogen Burkholderia pseudomallei in tropical rivers.,” Environmental Science and Pollution Research, vol. 23, no. 8, pp. 7828–7839, Jan. 2016, doi: 10.1007/S11356-015-5943-Z.

[49]Win et al., “Melioidosis in Myanmar.,” Tropical medicine and infectious disease, 2018, doi: 10.3390/tropicalmed3010028.

[50]Muthumbi et al., “Population-Based Estimate of Melioidosis, Kenya.,” Emerging infectious diseases, 2019, doi: 10.3201/eid2505.180545.

[51]Duarte et al., “Genomic Diversity of Burkholderia pseudomallei Isolates, Colombia.,” Emerging infectious diseases, 2021, doi: 10.3201/eid2702.202824.

[52]Currie and Kaestli, “Epidemiology: A global picture of melioidosis.,” Nature, 2016, doi: 10.1038/529290a.

[53]Savelkoel et al., “Serologic Evidence of Exposure to Burkholderia pseudomallei, Nigeria.,” Emerging infectious diseases, 2026, doi: 10.3201/eid3201.251113.

[54]Dance and Limmathurotsakul, “Global Burden and Challenges of Melioidosis.,” Tropical medicine and infectious disease, 2018, doi: 10.3390/tropicalmed3010013.

[55]E. Birnie et al., “Melioidosis in Africa: Time to Raise Awareness and Build Capacity for Its Detection, Diagnosis, and Treatment.,” American Journal of Tropical Medicine and Hygiene, vol. 106, no. 2, pp. 394–397, Jan. 2022, doi: 10.4269/ajtmh.21-0673.

[56]W. J. Wiersinga et al., “Melioidosis: insights into the pathogenicity of Burkholderia pseudomallei,” Nature Reviews Microbiology, vol. 4, no. 4, pp. 272–282, Apr. 2006, doi: 10.1038/NRMICRO1385.

[57]J. Gilad, D. A. Schwartz, and Y. Amsalem, “Clinical Features and Laboratory Diagnosis of Infection with the Potential Bioterrorism Agents Burkholderia Mallei and Burkholderia Pseudomallei,” International journal of biomedical science : IJBS, vol. 3, no. 3, pp. 144–152, Sept. 2007.

[58]Dance, “Treatment and prophylaxis of melioidosis.,” International journal of antimicrobial agents, 2014, doi: 10.1016/j.ijantimicag.2014.01.005.

[59]K. Pongmala et al., “Distribution of Burkholderia pseudomallei within a 300-cm deep soil profile: implications for environmental sampling,” Dental science reports, vol. 12, no. 1, May 2022, doi: 10.1038/s41598-022-12795-0.

[60]Hogan et al., “Melioidosis in Trinidad and Tobago.,” Emerging infectious diseases, 2015, doi: 10.3201/eid2105.141610.

[61]Nyanasegran, Nathan, Firdaus-Raih, Muhammad, and Ng, “Biofilm Signaling, Composition and Regulation in ,” Journal of microbiology and biotechnology, 2023, doi: 10.4014/jmb.2207.07032.

[62]Bzdyl, Moran, Bendo, and Sarkar-Tyson, “Pathogenicity and virulence of ,” Virulence, 2022, doi: 10.1080/21505594.2022.2139063.

[63]C. C. Roe et al., “Multiple phylogenetically-diverse, differentially-virulent Burkholderia pseudomallei isolated from a single soil sample collected in Thailand,” PLOS Neglected Tropical Diseases, vol. 16, no. 2, pp. e0010172–e0010172, Feb. 2022, doi: 10.1371/journal.pntd.0010172.

[64]J. R. Webb et al., “Myanmar Burkholderia pseudomallei strains are genetically diverse and originate from Asia with phylogenetic evidence of reintroductions from neighbouring countries,” Scientific Reports, vol. 10, no. 1, p. 16260, Oct. 2020, doi: 10.1038/S41598-020-73545-8.

[65]J. E. Gee et al., “Genomic Diversity of Burkholderia pseudomallei in Ceara, Brazil,” vol. 6, no. 1, Feb. 2021, doi: 10.1128/MSPHERE.01259-20.

[66]M. T. G. Holden et al., “Genomic plasticity of the causative agent of melioidosis, Burkholderia pseudomallei,” Proceedings of the National Academy of Sciences of the United States of America, vol. 101, no. 39, pp. 14240–14245, Sept. 2004, doi: 10.1073/PNAS.0403302101.

[67]T. Nandi et al., “Burkholderia pseudomallei sequencing identifies genomic clades with distinct recombination, accessory and epigenetic profiles,” Genome Research, vol. 25, no. 1, pp. 129–141, Jan. 2015, doi: 10.1101/GR.177543.114.

[68]A. K. Gairola, “Clinical Burkholderia pseudomallei isolates from north Queensland carry diverse bimABm genes that are associated with central nervous system disease and are phylogenomically distinct from other Australian strains,” PLOS Neglected Tropical Diseases, vol. 16, no. 6, pp. e0009482–e0009482, June 2022, doi: 10.1371/journal.pntd.0009482.

[69]E. P. Price, B. J. Currie, and D. S. Sarovich, “Genomic Insights Into the Melioidosis Pathogen, Burkholderia pseudomallei,” Current tropical medicine reports, vol. 4, no. 3, pp. 95–102, Sept. 2017, doi: 10.1007/S40475-017-0111-9.

[70]E. P. Price et al., “Unprecedented Melioidosis Cases in Northern Australia Caused by an Asian Burkholderia pseudomallei Strain Identified by Using Large-Scale Comparative Genomics,” Applied and Environmental Microbiology, vol. 82, no. 3, pp. 954–963, Feb. 2016, doi: 10.1128/AEM.03013-15.

[71]H. Zheng et al., “Genetic diversity and transmission patterns of Burkholderia pseudomallei on Hainan island, China, revealed by a population genomics analysis.,” vol. 7, no. 11, Nov. 2021, doi: 10.1099/MGEN.0.000659.

[72]D. S. Sarovich et al., “Phylogenomic Analysis Reveals an Asian Origin for African Burkholderia pseudomallei and Further Supports Melioidosis Endemicity in Africa.,” vol. 1, no. 2, pp. 1–12, Apr. 2016, doi: 10.1128/MSPHERE.00089-15.

[73]J. Dale et al., “Epidemiological Tracking and Population Assignment of the Non-Clonal Bacterium, Burkholderia pseudomallei,” PLOS Neglected Tropical Diseases, vol. 5, no. 12, pp. 1–17, Dec. 2011, doi: 10.1371/JOURNAL.PNTD.0001381.

[74]A.-K. Ghazali, S.-A. Eng, J. S. Khoo, S. Teoh, C.-C. Hoh, and S. Nathan, “Whole-genome comparative analysis of Malaysian Burkholderia pseudomallei clinical isolates,” July 2024, doi: 10.60692/61rky-rxb55.

[75]Y. Yu et al., “Genomic patterns of pathogen evolution revealed by comparison of Burkholderia pseudomallei , the causative agent of melioidosis, to avirulent Burkholderia thailandensis,” BMC Microbiology, vol. 6, no. 1, pp. 46–46, May 2006, doi: 10.1186/1471-2180-6-46.

[76]S. Tumapa et al., “Burkholderia pseudomallei genome plasticity associated with genomic island variation,” July 2024, doi: 10.60692/24gbn-k1245.

[77]S. Spring-Pearson et al., “Pangenome Analysis of Burkholderia pseudomallei: Genome Evolution Preserves Gene Order despite High Recombination Rates,” PLOS ONE, vol. 10, no. 10, p. 140274, Oct. 2015, doi: 10.1371/JOURNAL.PONE.0140274.

[78]R. Seng et al., “Genetic diversity, determinants, and dissemination of Burkholderia pseudomallei lineages implicated in melioidosis in northeast Thailand,” bioRxiv, June 2023, doi: 10.1101/2023.06.02.543359.

[79]T. Pearson et al., “Phylogeographic reconstruction of a bacterial species with high levels of lateral gene transfer,” BMC Biology, vol. 7, no. 1, pp. 78–78, Nov. 2009, doi: 10.1186/1741-7007-7-78.

[80]Baker et al., “Burkholderia pseudomallei distribution in Australasia is linked to paleogeographic and anthropogenic history.,” PloS one, 2018, doi: 10.1371/journal.pone.0206845.

[81]A. C. Cheng et al., “Genetic Diversity of Burkholderia pseudomallei Isolates in Australia,” Journal of Clinical Microbiology, vol. 46, no. 1, pp. 249–254, Jan. 2008, doi: 10.1128/JCM.01725-07.

[82]J. W. Sahl et al., “Genomic Characterization of Burkholderia pseudomallei Isolates Selected for Medical Countermeasures Testing: Comparative Genomics Associated with Differential Virulence,” PLOS ONE, vol. 10, no. 3, pp. 1–18, Mar. 2015, doi: 10.1371/JOURNAL.PONE.0121052.

[83]A. Aziz et al., “Suspected cases of intracontinental Burkholderia pseudomallei sequence type homoplasy resolved using whole-genome sequencing.,” vol. 3, no. 11, pp. 1–8, Nov. 2017, doi: 10.1099/MGEN.0.000139.

[84]S. H. Sim et al., “The Core and Accessory Genomes of Burkholderia pseudomallei: Implications for Human Melioidosis,” July 2024, doi: 10.60692/cz9ey-8tf54.

[85]Gee et al., “Phylogeography of Burkholderia pseudomallei Isolates, Western Hemisphere.,” Emerging infectious diseases, 2017, doi: 10.3201/eid2307.161978.

[86]C. M. Hall et al., “Burkholderia pseudomallei, the causative agent of melioidosis, is rare but ecologically established and widely dispersed in the environment in Puerto Rico.,” PLOS Neglected Tropical Diseases, vol. 13, no. 9, Sept. 2019, doi: 10.1371/JOURNAL.PNTD.0007727.

[87]C. Chewapreecha et al., “Genetic variation associated with infection and the environment in the accidental pathogen Burkholderia pseudomallei,” July 2024, doi: 10.60692/hb63a-ka807.

[88]N. Chantratita et al., “Genetic Diversity and Microevolution of Burkholderia pseudomallei in the Environment,” July 2024, doi: 10.60692/1c336-9ae69.

[89]B. D. Smet et al., “Whole-Genome Sequencing Confirms that Burkholderia pseudomallei Multilocus Sequence Types Common to Both Cambodia and Australia Are Due to Homoplasy,” Journal of Clinical Microbiology, vol. 53, no. 1, pp. 323–326, Jan. 2015, doi: 10.1128/JCM.02574-14.

[90]E. M. Meumann et al., “Emergence of Burkholderia pseudomallei Sequence Type 562, Northern Australia.,” Emerging Infectious Diseases, vol. 27, no. 4, pp. 1057–1067, Jan. 2021, doi: 10.3201/EID2704.202716.

[91]Aziz, Currie, Mayo, Sarovich, and Price, “Comparative genomics confirms a rare melioidosis human-to-human transmission event and reveals incorrect phylogenomic reconstruction due to polyclonality.,” Microbial genomics, 2020, doi: 10.1099/mgen.0.000326.

[92]A. Sawana, M. Adeolu, and R. S. Gupta, “Molecular signatures and phylogenomic analysis of the genus Burkholderia: proposal for division of this genus into the emended genus Burkholderia containing pathogenic organisms and a new genus Paraburkholderia gen. nov. harboring environmental species,” Frontiers in Genetics, vol. 5, pp. 429–429, Dec. 2014, doi: 10.3389/FGENE.2014.00429.

[93]J. W. Sahl et al., “The Effects of Signal Erosion and Core Genome Reduction on the Identification of Diagnostic Markers,” Mbio, vol. 7, no. 5, p. 16, Nov. 2016, doi: 10.1128/MBIO.00846-16.

[94]M. C. Diniz et al., “Análise Genômica de Burkholderia mallei e Burkholderia pseudomallei: Dois Patógenos de Primeira Grandeza e de Genomas Surpreendentemente Complexos,” vol. 2, no. 1, pp. 1–34, June 2008, doi: 10.5935/RBHSA.V2I1.39.

[95]W. P. Hanage, C. Fraser, and B. G. Spratt, “Sequences, sequence clusters and bacterial species.,” Philosophical Transactions of the Royal Society B, vol. 361, no. 1475, pp. 1917–1927, Nov. 2006, doi: 10.1098/RSTB.2006.1917.

[96]V. Wuthiekanun et al., “Burkholderia Pseudomallei is genetically diverse in agricultural land in Northeast Thailand.,” PLOS Neglected Tropical Diseases, vol. 3, no. 8, Aug. 2009, doi: 10.1371/JOURNAL.PNTD.0000496.