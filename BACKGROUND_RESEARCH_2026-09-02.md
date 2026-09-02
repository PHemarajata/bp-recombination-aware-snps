# Background research for the *B. pseudomallei* manuscript

Written 2026-09-02. Source material for the Background and Introduction, not
finished manuscript prose. Every factual claim carries a citation with a PMID and
a DOI. Numbers that could not be traced to a primary source are marked
**UNVERIFIED** with a note on what is missing.

Scope. The methods literature is covered in `GAP1`–`GAP4` and is not repeated.
This document covers the disease, its epidemiology and ecology, the genome, and
what comparative genomics has established about relatedness and geographic
origin. Section 12 lists citation errors found in the existing project documents.

Provenance. Research ran as five parallel literature passes plus an independent
verification pass. Anchors were checked directly against PubMed records. The five
passes worked through Europe PMC and PMC full text because the PubMed programmatic
tools were blocked for them mid-session. Every load-bearing number was extracted
twice. Three fabrications were caught and discarded during that process, and they
are documented in section 12.4 because they show what the failure mode looks like.

---

## 1. The organism and the disease

*Burkholderia pseudomallei* is a Gram-negative environmental saprophyte of soil
and surface water across the tropics and subtropics, and the cause of melioidosis
(Wiersinga 2018, PMID 29388572; Meumann 2024, PMID 37794173). It is not
host-adapted. Human infection is an accident of environmental exposure, and
person-to-person transmission is exceptionally rare. That single ecological fact
is what makes the genome informative about place, because there is no transmission
chain to homogenize genotypes across geography.

Melioidosis has no characteristic presentation. Pneumonia is the commonest single
syndrome, but the disease also appears as bacteremia without a focus, skin and
soft-tissue infection, visceral abscesses in liver, spleen and prostate, septic
arthritis, osteomyelitis, parotitis in children, and neurological disease. The
Darwin Prospective Melioidosis Study has captured every culture-confirmed case in
the tropical Northern Territory of Australia since October 1989, which gives the
cleanest denominator in the literature (Currie 2021, PMID 34303419).

| Darwin Prospective Melioidosis Study, 1989–2019 | Value |
|---|---|
| Culture-confirmed cases | 1,148 |
| Deaths | 133 (12%) |
| Pneumonia at presentation | 595 (52%) |
| Bacteremia | 633 of 1,135 (56%) |
| Septic shock | 240 (21%) |
| Mechanical ventilation | 180 (16%) |
| Diabetes | 513 (45%) |
| Hazardous alcohol use | 455 (40%) |
| No identified risk factor | 186 (16%) |
| Cases in the wet season, November to April | 80% |
| Median annual incidence | 20.5 per 100,000 |

Two figures from that study carry the clinical argument. Mortality fell to 17 of
278 (6%) over the final five years, which shows what early diagnosis and intensive
care achieve. And of the 133 people who died, only three had no identified risk
factor, so melioidosis kills through comorbidity rather than at random.

Outcomes elsewhere are far worse. Limmathurotsakul and colleagues note that
treatment with an antimicrobial the organism is intrinsically resistant to "may
result in case fatality rates (CFRs) exceeding 70%" (PMID 26877885). The
Australia-versus-Thailand contrast is the one to quote, 12% in Darwin against
roughly 43% in Ubon Ratchathani. **UNVERIFIED: the 42.6% Ubon Ratchathani figure
came through a summarizing fetch rather than the primary text. Retrieve the source
before citing it.**

Diabetes is the dominant risk factor everywhere, and the global diabetes trend is
why burden is expected to rise (Wiersinga 2018, PMID 29388572). Be careful with
the effect size. The widely repeated 12- to 13-fold figure attributed to
Suputtamongkol 1999 could not be traced to any number in that paper's abstract,
and a pooled meta-analytic estimate gives relative risk 3.40 (2.92–3.87) with
I-squared of 98.2%. **UNVERIFIED: do not cite "13-fold" to Suputtamongkol without
the full text.**

### Incubation, latency, and a claim that genomics overturned

Where a discrete inoculating event can be identified, the incubation period runs
1–21 days with a mean of 9 (Currie 2000, PMID 10975006). Wiersinga and colleagues
restate this and add that a more severe form with shorter incubation follows
inhalation or aspiration of contaminated fresh water (PMID 29388572).

Latency has been badly overstated for fifty years. The "Vietnamese time bomb"
framing traces to a 1971 review and a 1987 single case report, amplified by a 1973
serological survey that projected roughly 225,000 future cases among repatriated
US personnel. Howes and Currie tested it against 30 years of Darwin data and found
that "activation from latency is a rare event in melioidosis, accounting in our
analysis for under 3% of DPMS cases," and that "the predicted 'Vietnamese time
bomb' has clearly not eventuated" (Am J Trop Med Hyg 2024, PMID 38806042, DOI
10.4269/ajtmh.24-0007). The longest plausible asymptomatic latency they accept is
29 years.

The record 62-year latency claim was overturned by phylogeography, and this is the
best single vignette available for the manuscript. Ngauy and colleagues reported
cutaneous melioidosis in a man captured by Japanese forces in March 1942 and
presenting in February 2004, resting the 62-year figure on the patient's own
account and a clinical timeline, with no genotyping (J Clin Microbiol
2005;43(2):970-972, PMID 15695721). Gee and colleagues later sequenced the
isolate, TX2004, and placed it in the Western Hemisphere clade alongside genomes
from patients with travel to Guatemala, Panama and Peru (Emerg Infect Dis
2017;23(7):1133-1138, PMID 28628442, DOI 10.3201/eid2307.161978). Their conclusion
is verbatim: "analysis suggested the isolate originated in Central or South
America."

A claim repeated for over a decade as the field record was corrected purely by
SNP-based geographic placement. That is exactly what this manuscript is about, and
it demonstrates that exposure history alone is not evidence of where an infection
was acquired.

### Recurrence, and why the answer depends on where you ask

Recurrence is common and is not always treatment failure. Genotyping is the only
way to separate relapse from reinfection, because they are clinically identical,
and the two best-studied settings give opposite answers.

In Darwin, of 679 survivors among 785 cases over 23 years, 39 (5.7%) had recurrent
disease, and MLST called 29 (74%) relapse against 10 (26%) reinfection (Sarovich
2014, PMID 24478504, DOI 10.1128/JCM.02239-13). Relapse collapsed over time, from
24 of 375 (6.4%) admitted before September 2003 to 5 of 410 (1.2%) admitted
afterward, p < 0.001. In northeast Thailand, of 116 patients with 123 recurrent
episodes, 92 (75%) were the same strain and 31 (25%) a new one, and the paper's
title states the finding plainly, that recurrence "is frequently due to reinfection
rather than relapse" (Maharjan 2005, PMID 16333094, DOI
10.1128/JCM.43.12.6032-6034.2005). Relapse accounted for 57 of 64 (89%)
recurrences inside the first year and 35 of 59 (59%) after it.

The disagreement is real and is probably about exposure intensity rather than
method. It should be reported as a disagreement.

---

## 2. Burden and global distribution

The burden estimate everyone cites is a model, and the manuscript should say so.
Limmathurotsakul and colleagues assembled 22,338 geolocated records of human
cases, animal cases and environmental detections spanning 1910 to 2014, fitted a
boosted regression tree model of environmental suitability at 5 km resolution, and
propagated it through incidence and case-fatality regressions over 2,500 global
realizations (Nat Microbiol 2016;1:15008, PMID 26877885, DOI
10.1038/nmicrobiol.2015.8). Model AUC was 0.81 (95% credible interval 0.76–0.86).

| Modeled global estimate, 2015 | Value (95% credible interval) |
|---|---|
| Human melioidosis cases per year | 165,000 (68,000–412,000) |
| Deaths per year | 89,000 (36,000–227,000) |
| Population living in likely *B. pseudomallei* areas | about 3 billion |
| Implied incidence | 5.0 per 100,000 at risk per year |

The credible intervals span roughly sixfold. Quoting 165,000 without the interval
overstates the precision, and the authors themselves note that only Australia,
Brunei Darussalam and Singapore have surveillance data comparable to their
estimates.

Two of their results matter more for this manuscript than the headline. The first
is the country count, and the project documents have been stating it wrongly. The
paper says, verbatim, that its priority list "includes 45 countries where
melioidosis is known to be endemic but is underreported and a further 34 countries
where melioidosis is probably endemic but has never been reported." Those are two
different numbers totaling 79 priority countries, not one number of 45.

The second is the regional split, which is counterintuitive and usually missed.
The model predicts "only 40% of all melioidosis cases occur in the East Asia and
Pacific region, where melioidosis is considered highly endemic," while "South Asia
is predicted to bear 44% of the overall burden." The part of the world with most
of the burden is not the part with most of the sequenced isolates.

That last point is the core argument for the manuscript's applied aim. If most
endemic countries under-report or have never reported at all, exposure history
cannot establish where an infection came from, and the organism's own genome is
the only remaining witness.

Birnie and colleagues converted the 2016 model into 4.6 million DALYs (uncertainty
interval 3.2–6.6), of which years of life lost are 98.9% (Lancet Infect Dis
2019;19(8):892-902, PMID 31285144). That paper takes the 2016 incidence and
mortality as inputs and shares authors with it, so it is downstream, not
independent corroboration. No newer estimate supersedes the 2016 model, and the
2024 review still relies on it (Meumann 2024, PMID 37794173).

---

## 3. The United States, and why attribution became urgent

The recent expansion of recognized melioidosis geography is almost entirely a
genomics story, and it supplies both failure modes that attribution has to
distinguish.

The 2016 model had already flagged the US, predicting that "two (USA and Japan) of
the 44 countries where [*B. pseudomallei*] is considered currently absent have
areas which would be suitable," naming "a geographically contiguous area covering
southern parts of Florida, Louisiana and Texas." The same paper allowed that the
organism might already be present and undetected. It was.

### Imported, not endemic

Four people in Georgia, Kansas, Minnesota and Texas developed melioidosis in 2021
with no travel to endemic areas, and records noted they had never traveled outside
the United States. Two died, including a five-year-old boy, and a four-year-old
girl survived with neurological sequelae. Whole-genome sequencing showed that "the
isolate from the spray bottle and those from the four patients were all the same
strain, which we have named ATS2021," and that the strain "clustered with samples
of *B. pseudomallei* from South Asia that are consistent with the origin of the
spray, India" (Gee 2022, N Engl J Med 2022;386(9):861-868, PMID 35235727, DOI
10.1056/NEJMoa2116130). The vehicle was an imported room spray sold through a
national retailer, and identifying it enabled a recall.

Conventional epidemiology could not have connected four unrelated patients across
four states. The genome connected them to each other, then to the product, then to
a subcontinent.

### Locally acquired, and long resident

Three patients in one Mississippi Gulf Coast county developed melioidosis between
July 2020 and January 2023, all reporting no travel outside the continental United
States (Petras 2023, N Engl J Med 2023;389(25):2355-2362, PMID 38118023, DOI
10.1056/NEJMoa2306448). Environmental sampling recovered *B. pseudomallei* from
one water puddle and two soil samples on the first patient's property, the first
environmental isolation of the organism in the continental United States.

The genomic argument is the interesting part. The strain, GCS2020, is sequence
type 92, a Western Hemisphere type, and sits more than 1,000 SNPs from any other
available genome while grouping with South American strains. Clinical and
environmental isolates were 3 to 15 SNPs apart. The large distance to everything
else rules out recent importation and establishes a long-resident, previously
unsampled population. The small distance within the cluster establishes a single
local source.

**UNVERIFIED: the environmental sample counts. One extraction gave 188 total with
59 in 2020 and 109 in 2022, which does not sum. Check the Methods before citing
any of the three numbers.**

CDC's own language went further than the paper's. Health Advisory HAN-00470 of 27
July 2022 states that "melioidosis is now considered to be locally endemic in areas
of the Gulf Coast region of Mississippi," while the NEJM paper says only that
melioidosis "may be endemic." Worth noting the difference in register.

### Forty-one years in one county

Four presumptive locally acquired cases occurred in Georgia between 1983 and 2024,
none with recent international travel, and all four *B. pseudomallei* genomes were
"highly related, suggesting a shared exposure" (Brennan 2025, Emerg Infect Dis
2025;31(9):1802-1806, PMID 40835221, DOI 10.3201/eid3109.250804). Two cases
followed Hurricane Helene in September 2024. Both were ST41, and archival
searching found two further fatal ST41 cases in the same county from 1983 and
1989. The four genomes fall within 20 SNPs of each other across 41 years, and ST41
is of Southeast Asian rather than Americas origin, with the closest relatives from
Vietnam.

**UNVERIFIED: the under-20-SNP figure and the Vietnam proximity came through a
secondary review rather than the primary paper. Retrieve Brennan 2025 in full
before quoting either.**

Twenty SNPs across four decades is a strong claim about clock rate or
environmental dormancy, and it is precisely the kind of statement a
recombination-aware method should be able to test. Currie and colleagues now hold
that "melioidosis should therefore now be considered endemic in Mississippi and is
likely endemic in Georgia and Texas," though the organism has not been cultured
from the environment in the latter two (PLoS Negl Trop Dis 2026;20(4):e0014217,
PMID 42030350, DOI 10.1371/journal.pntd.0014217).

---

## 4. Transmission and ecology

Infection follows environmental exposure by percutaneous inoculation, inhalation,
or ingestion of contaminated water. Wiersinga and colleagues state that "specific
clinical presentations and their severity vary depending on the route of bacterial
entry (skin penetration, inhalation or ingestion), host immune function and
bacterial strain and load" (PMID 29388572).

The strongest direct evidence tying patients to places is a genomics result from
Darwin. Over 20 years the group sampled the environment at 98 patient sites where
a specific location was suspected, collecting 975 samples, 742 soil and 233 water.
Genotyping matched clinical and epidemiologically linked environmental isolates
for 19 patients (19%), 11 from soil and 8 from water, and 17 of the 19 pairs
clustered on a core-genome SNP phylogeny (Webb 2022, PMID 35080450, DOI
10.1128/JCM.01648-21). Matched pairs let them infer the infecting route in
individual cases, covering percutaneous inoculation, inhalation and ingestion.

Two things in that paper deserve quoting. The authors conclude that
whole-genome sequencing and "careful genomics are required to avoid overcalling the
relatedness between clinical and environmental isolates of *B. pseudomallei*."
And they report that "pairwise genetic differences between the epidemiologically
linked isolates (n = 19) did not correlate with time," documenting zero-SNP
differences between isolates separated by 18 days and by 156 days alike.

Overcalling relatedness is a recombination problem in substance, and a molecular
clock that does not track time at this scale is what you expect when most of the
distance is imported rather than accumulated.

Seasonality is strong, with 80% of Darwin cases in the November to April wet
season (Currie 2021, PMID 34303419). Environmental associations from the global
model are high rainfall and temperature, anthrosol and acrisol soils, high salinity
and a high proportion of gravel. The model found no association with soil pH,
which conflicts with the field-sampling literature, and the authors attribute this
to pH being confounded with salinity. That tension is worth flagging rather than
smoothing over.

Seng and colleagues found that terrain slope, altitude and river direction shape
the geographic dispersal of *B. pseudomallei* in northeast Thailand, which points
at the physical environment rather than human movement as the main thing
structuring the population over short distances (PMID 38972886, DOI
10.1038/s41467-024-50067-9).

---

## 5. Genome architecture

The reference is K96243, a Thai clinical isolate (Holden 2004, Proc Natl Acad Sci
U S A 2004;101(39):14240-5, PMID 15377794, DOI 10.1073/pnas.0403302101).

| K96243 | Value |
|---|---|
| Chromosome 1 | 4,074,542 bp, 3,460 CDS, accession BX571965 |
| Chromosome 2 | 3,173,005 bp, 2,395 CDS, accession BX571966 |
| Total | 7,247,547 bp |
| Genomic islands | 16, comprising 6.1% of the genome |

**UNVERIFIED: Holden 2004 states no G+C content anywhere, not for the genome and
not per replicon. The commonly quoted 68% comes from the NCBI assembly record.
Compute per-replicon GC from the sequence rather than citing the paper for it.**

The two replicons are not interchangeable, and that governs how the analysis is
designed. Holden and colleagues describe "significant functional partitioning of
genes between them," with the large chromosome carrying "many of the core
functions associated with central metabolism and cell growth" and the small
chromosome carrying "more accessory functions associated with adaptation and
survival in different niches." They found greater gene-order conservation and more
orthologs on the large chromosome, and concluded that "the two replicons have
distinct evolutionary origins." Wu and colleagues independently confirmed that
compartmentalization two decades later on a much larger sample (PMID 42377320).

Two replicons with different functional loads and different evolutionary origins
should not be pooled under one clock or one recombination model. Chewapreecha and
colleagues ran BEAST separately per chromosome for that reason, and the
disagreement they obtained is documented in `GAP4` section 9.

Holden and colleagues found the 16 islands "variably present in a collection of
invasive and soil isolates but entirely absent from the clonally related organism
*B. mallei*," and concluded that "variable horizontal gene acquisition by
*B. pseudomallei* is an important feature of recent genetic evolution and that this
has resulted in a genetically diverse pathogenic species."

Tuanyok and colleagues extended the count across five reference genomes and found
71 distinct genomic islands (BMC Genomics 2008;9:566, PMID 19038032, DOI
10.1186/1471-2164-9-566). Island positions are not random. Many sit at tRNA loci,
and the authors propose tRNA-mediated site-specific recombination as the
integration mechanism. For a mapping pipeline that predicts where callability will
fail and where SNP density will spike for reasons unrelated to vertical descent.

A useful negative. K96243 carries only 42 insertion-sequence elements, against 171
(3.1% of the genome) in *B. mallei*, so IS-driven mismapping is a *B. mallei*
problem and not a *B. pseudomallei* one. **UNVERIFIED: both IS counts came through
a secondary extraction. Confirm against Nierman 2004 and Holden 2004 before
citing.**

---

## 6. Core and accessory genome

There is no single core-genome fraction for this organism, and the published
figures answer different questions. `GAP1` section 4 tabulates them and that table
should be reused. The point that must survive into the manuscript is provenance.

The widely quoted 86% figure is array comparative genomic hybridization across 94
South East Asian strains from 2008 (Sim 2008, PMID 18927621, DOI
10.1371/journal.ppat.1000178). It measures gene presence against a fixed probe
set, it cannot see anything absent from K96243, and it is not a base-level callable
fraction. Chewapreecha's 469-genome pangenome puts 21,748 of 25,812 CDS (84%) in
the accessory genome, with only 4,064 core at 99% presence.

**UNVERIFIED but important: `GAP1` states that Wu and colleagues obtained a
core-genome alignment of 3,805,619 bp, 52.5% of K96243. Two independent passes
failed to retrieve that figure. The publisher returns 403 and there is no PMC
deposit. Do not quote 3,805,619 bp or 52.5% until the full text is in hand.**

Spring-Pearson and colleagues analyzed 37 isolates and found the pangenome open,
with the 37th genome adding 136 new genes, and a global core of 4,568 ± 16
homologs (PLoS One 2015;10(10):e0140274). Their most useful result for this
manuscript is structural. Gene order is "highly conserved among strains, despite
the high recombination rates previously observed," and they argue that "high rates
of gene transfer and recombination are incompatible with retaining gene order
unless these processes are either highly localized to specific sites within the
genome, or are characterized by symmetrical gene gain and loss." They report a
split of roughly 96% low-recombination genome against 4% readily recombining.

Recombination in this species is localized and structured rather than uniform,
which is exactly the premise a recombination-aware method exploits.

Sim and colleagues found something else relevant to attribution. Strains from human
melioidosis "clustered on a tree based on accessory gene content, and were
significantly more likely to harbor certain GIs compared to animal and
environmental isolates." Accessory content carries a source signal, but it is a
signal about host and niche as much as about geography, and the two are confounded
in any convenience collection.

---

## 7. Determinants that vary with geography

Three loci have published genotype-to-place or genotype-to-disease associations,
and all three are variably present rather than universal.

### YLF and BTFC

Two mutually exclusive gene clusters occupy the same position on chromosome 2. YLF
is a *Yersinia*-like fimbrial cluster, BPSS0120 to BPSS0123 in K96243, and is
horizontally acquired. BTFC is a *B. thailandensis*-like flagellum and chemotaxis
cluster and is the ancestral state. Tuanyok and colleagues screened 571
*B. pseudomallei* DNA extracts from endemic regions and every strain carried one or
the other (J Bacteriol 2007;189(24):9044-9, PMID 17933898, DOI 10.1128/JB.01264-07).

| Region | n | BTFC | YLF |
|---|---|---|---|
| Australia | 231 | 204 (88%) | 27 (12%) |
| Thailand | 310 | 6 (2%) | 304 (98%) |
| Other countries | 30 | 7% | 93% |

All 77 *B. thailandensis* strains tested carried the BTFC-like region, consistent
with BTFC being ancestral. Clinical isolates are more likely to be YLF and
environmental isolates more likely to be BTFC. Chewapreecha's genome-wide
association analysis independently recovered BTFC as regionally variable across 469
genomes.

One horizontally acquired locus separates two continents at 88% against 98%. That
is encouraging for geographic signal in accessory content and cautionary at the
same time, because a locus of this kind moves between lineages without carrying the
rest of the genome with it.

### BimA and fhaB3

Sarovich and colleagues used 556 northern Australian melioidosis patients with
isolates spanning 24 years (PLoS One 2014;9(3):e91682, DOI
10.1371/journal.pone.0091682). The *B. mallei*-like allele *bimA*(Bm),
BURPS668_A2118 in MSHR668, occurs in about 12% of northern Australian strains, and
patients infected with such a strain were 14 times more likely to present with
neurological involvement, p < 0.001, 95% CI 4.7–44.6. The allele has not been
observed in Thailand, Cambodia, Laos or Vietnam, but was found in two isolates from
India. Morris and colleagues supplied the mouse phenotype, with increased
persistence in phagocytes and replication in brain and spinal cord (Emerg Infect
Dis 2017;23(5):740-749, PMID 28457226).

*fhaB3*, BPSS2053, a 9.3 kb gene, is present in 83% of the Australian isolates and
reportedly 100% of Thai strains. Patients carrying it were twice as likely to be
blood-culture positive, p = 0.028, and *fhaB3*-negative strains were four times
more likely in cutaneous melioidosis without sepsis, p = 0.001. This stratifies
presentation rather than geography, though the prevalence difference partly
confounds the two.

**Citation conflict to resolve: a direct PubMed query returned PMID 24618705 for
this paper, matching title, journal, authors and DOI. One research pass reported
PMID 24614774. Use 24618705 unless a check says otherwise.**

### LPS O-antigen

Tuanyok and colleagues genotyped 999 strains, 600 Australian, 349 Thai and 50 from
elsewhere in Southeast Asia, into four LPS types (PLoS Negl Trop Dis
2012;6(1):e1453, PMID 22235357, DOI 10.1371/journal.pntd.0001453). Genotype A was
97.7% in Southeast Asia and 85.3% in Australia, genotype B was 2.3% against 13.8%,
and all seven genotype B2 strains came from Australia (5) and Papua New Guinea (2).

The authors state their own limitation, that "we phenotyped only about 24% of the
isolates that were genotyped." The widely repeated claim that LPS type B is less
virulent is not established at the level usually implied. Prevalence is robust on
999 strains, serum resistance and serology rest on a quarter of them, and the two
claims must be kept apart.

### What does not belong on this list

T3SS3 (Bsa) and T6SS-5 are core within *B. pseudomallei* and are shared with
*B. mallei* and *B. thailandensis*. They are virulence determinants, but they are
not sources of presence-or-absence variation between strains, and listing them
beside YLF/BTFC or *bimA* would be an error. What varies in them is allelic
sequence and expression.

---

## 8. Relatives and species boundaries

*B. mallei*, the cause of glanders, is not a sister species. Godoy and colleagues
typed 147 isolates and found that *B. mallei* isolates "recovered from three
continents over a 30-year period had identical allelic profiles," that they
"clustered within the *B. pseudomallei* group," and that six of seven alleles were
also present in *B. pseudomallei* (J Clin Microbiol 2003;41(5):2068-79, PMID
12734250, DOI 10.1128/JCM.41.5.2068-2079.2003). Their conclusion is blunt, that
*B. mallei* "is a clone of *B. pseudomallei* that, on population genetics grounds,
should not be given separate species status."

*B. thailandensis* is a genuine separate species and the usual outgroup, with
average allelic divergence of 3.2% and no allele sharing. Its capsular
polysaccharide cluster shows the species boundary is porous. Sim and colleagues
found *B. thailandensis* E555 carrying a CPS cluster resembling the
*B. pseudomallei* one, conferring colony wrinkling, complement resistance and
intracellular macrophage survival, though without enhanced virulence in mice
(Genome Biol 2010;11(8):R89, PMID 20799932). A major virulence locus moves
horizontally across a species boundary.

The same 2003 paper established the MLST scheme still in use, resolving 128
*B. pseudomallei* isolates into 71 sequence types.

---

## 9. Recombination

This is the section the manuscript speaks to most directly, and the literature has
a specific trap in it.

### Three different quantities all called r/m

| Quantity | What it measures | Magnitude in *B. pseudomallei* |
|---|---|---|
| Per-site genome-wide r/m | substitutions introduced by recombination against by mutation, across a core alignment | 2.2 to 8.5 |
| Per-allele MLST r/m | probability a whole MLST allele changes by recombination against by mutation, at 7 loci | 18 to 30 |
| Per-genome or per-branch counts | number of recombination events or blocks | 2,373 events across 106 genomes (Nandi) |

A per-allele figure exceeds a per-site figure by roughly the mean number of
substitutions imported per event within a 400–500 bp locus. Reporting "r/m about
25 in *B. pseudomallei*" alongside genome-wide values from other species compares
different things, and the error is present in the published literature.

Pearson and colleagues are the source of the famous claim, that "the relative
contributions of homologous recombination versus mutation for *Burkholderia
pseudomallei* is over two times higher than for *Streptococcus pneumoniae* and is
thus the highest value yet reported in bacteria" (BMC Biol 2009;7:78, PMID
19922616, DOI 10.1186/1741-7007-7-78). That is a per-allele quantity from seven
housekeeping genes. It does not survive translation to a per-site genome-wide
scale, and the manuscript should not repeat "the highest recombination rate
reported in bacteria" without saying which quantity it refers to.

### The genome-wide estimates

Nandi and colleagues sequenced 106 clinical, animal and environmental strains from
a restricted Asian locale, 97 from Singapore and Malaysia and 9 from Thailand,
isolated 1996 to 2005 (Genome Res 2015;25(1):129-41, PMID 25236617, DOI
10.1101/gr.177543.114). They report verbatim that "the overall per site r/m ratio
was 7.2," with clade values of 4.5, 8.5 and 6.

Three details about that number are routinely misstated and all three matter.

The tool was ClonalFrame, not ClonalFrameML. Gubbins was used only to mask
recombinant sites before tree-building. A verification pass confirmed that the
string "ClonalFrameML" does not appear anywhere in the paper.

The estimate is already a within-clade estimate. ClonalFrame "was applied
separately to each Bp clade," which is the same design principle this project
adopts.

The alignment was a 5.6 Mb reduced core genome that deliberately excludes mobile
elements, surface polysaccharides, secretion systems and tandem repeats. That
excludes some of the most recombinogenic real estate, so 7.2 is conservative if
anything.

The supporting inventory is 10,314 lineage SNPs against 74,532 recombination
associated SNPs, whose ratio is 7.2, and 2,373 recombination events with tract
lengths from 3 bp to 71 kb, median about 5 kb. **Note an internal inconsistency:
another passage in the same paper gives 2,481, 821 and 334 events for clades A, B
and C, summing to 3,636. Both strings are present. Cite 2,373, the figure attached
to the r/m calculation, and do not sum the per-clade numbers.**

Seng and colleagues provide the only other genome-wide per-site estimate, and the
only one with confidence intervals, from 1,391 isolates collected at nine northeast
Thai hospitals between 2015 and 2018 (PMID 38972886). They partitioned with PopPUNK
into three dominant lineages and ran Gubbins v3.1.3 on lineage-specific alignments.

| Lineage | r/m | 95% CI | Mean pairwise core SNPs |
|---|---|---|---|
| 1 | 3.7 | 3.3–4.1 | 549 |
| 2 | 4.6 | 4.0–5.2 | 351 |
| 3 | 2.2 | 1.8–2.6 | 517 |
| whole population | not estimated | | 1,087 |

They also report that "a very high proportion of genes underwent recombination at
least once: 99.5% of genes in lineage 1, 99.9% in lineage 2, and 96.6% in lineage
3." Essentially no gene in the core genome is recombination-free over the history
of a single lineage.

The defensible range to quote for genome-wide per-site r/m in this species is
roughly 2 to 9, centered on 4 to 7, and both published estimates are within-lineage
rather than whole-species. That is methodologically correct rather than an
oversight, for reasons in the next subsection.

**UNVERIFIED and important: it could not be determined whether *B. pseudomallei*
appears among the 48 species in Vos and Didelot's ClonalFrame survey (ISME J
2009;3(2):199-208, PMID 18830278). The paper is paywalled with no PMC record. Do
not write that the species "ranks Nth" in that survey.** What is safe is that the
survey spans r/m from 0.02 to 63.6, and that the species is absent from the modern
162-species genome-based survey of Torrance and colleagues, whose median effective
r/m is 3.84 (PNAS 2024;121(18):e2316302121, PMID 38657048). Placing
*B. pseudomallei* at 2 to 9 puts it around to somewhat above that median, not at
the extreme. **A claimed "r/m = 973.8 for *B. pseudomallei* MSHR3" surfaced in
search results, could not be traced to any primary source, names a strain that does
not match standard nomenclature, and must not be cited.**

### Why the population has to be partitioned first

Nandi and colleagues supply the biological reason. They observed "clade-specific
patterns of recombination and accessory gene exchange," with recombination
happening between clade members while "interclade exchanges were rarely observed."
They identified the mechanism, in that each clade "harbored a distinct complement
of restriction-modification (RM) systems," confirmed by methylome sequencing to
give distinct methylation profiles, and showed in *E. coli* that these systems "can
inhibit uptake of non-self DNA." Their conclusion is that "genomic clades may thus
represent functional units of genetic isolation in *Bp*, modulating intraspecies
genetic diversity."

If clades are units of genetic isolation, a recombination rate estimated across
clades is not estimating a rate that exists in nature.

This also answers the question of how geographic signal survives the recombination
load. Recombination homogenizes within a geographic population while leaving
between-population structure largely intact, which is why Pearson's Phi_PT of 0.117
is significant despite MLST data that look almost panmictic. The caveat is that
Nandi's result comes from 106 strains in one restricted Asian locale, and whether
RM-mediated restriction of gene flow holds globally, and specifically across
Wallace's Line, has not been tested.

### The operating range, which nobody has published

This is where the manuscript's own contribution sits, so the absence should be
stated precisely rather than implied.

Croucher and colleagues state that Gubbins "is most effective when detecting
imports of sequence into a densely sampled collection of closely-related isolates,
where recombinations import a high density of base substitutions from divergent
donors" (Nucleic Acids Res 2015;43(3):e15, PMID 25414349, DOI
10.1093/nar/gku1196). Both failure modes are named in that paper.

Too diverse, and "the identification of recombinations as regions with elevated
densities of base substitutions is confounded by the high diversity of the
sequences in the alignment, and therefore for improved accuracy such populations
would need to be split into sets of closely-related isolates."

Too clonal, and the number is stark. Gubbins "was only able to predict 5–10% of the
actual number of recombinations," because only 35% of recombinations imported more
than the minimum detectable number of substitutions. Between 90% and 95% of real
events are missed when donor and recipient are similar.

ClonalFrameML is explicitly a within-lineage tool, designed for "a single lineage
(for example a single sequence type according to multi-locus sequence typing), with
frequent imports from other lineages" (Didelot and Wilson, PLoS Comput Biol
2015;11(2):e1004041, PMID 25675341, DOI 10.1371/journal.pcbi.1004041). Both of its
documented failure modes bias r/m downward, so published values in this species
should be read as lower bounds.

Neither paper gives a numeric divergence range. What the *B. pseudomallei*
literature has instead is three groups operationalizing the same principle without
publishing a calibration.

Chewapreecha and colleagues used hierBAPS to subdivide the population so as to
"allow the recombination detection tool (Gubbins) to operate within its best
performing range," and continued hierarchical clustering "until the diversity
observed in secondary or tertiary clusters fell within the limit of recombination
detection" (PMID 28112723). Two consequences follow. The whole-species
*B. pseudomallei* alignment is explicitly too diverse for Gubbins. And one cluster,
the Australasian group, "could not be further sub-clustered," which is a documented
species-specific failure of the standard pipeline in the most basal and most
diverse part of the population. Anything inferred about Australasian ancestry rests
on data that could not be recombination-corrected to the same standard as the rest.

Zheng and colleagues supplied the only published number. They subdivided using "a
threshold of 5000 PSDs [pairwise SNP distances], which ensured that the population
of strains was subdivided into groups with closely related genetic backgrounds and
allowed the recombination detection tool Gubbins to operate within its best
performance range," across 1,654 genomes and 325,036 SNPs on a 5.8 Mb core (Microb
Genom 2021;7(11), PMID 34762026, DOI 10.1099/mgen.0.000659). It is an empirical
rule of thumb from one study, not a validated criterion, and should be presented as
such.

Seng's lineages sat at 351 to 549 mean pairwise core SNPs, an order of magnitude
below Zheng's ceiling.

So the field has a stated principle, one unvalidated ceiling, and no floor at all.
Measuring the range in both directions is what this study adds, and the measured
window of roughly 1,270 to 4,671 mean pairwise core SNPs sits inside Zheng's
threshold while supplying the lower bound nobody has published.

### The consequence for outbreak genomics

The regime in which SNP thresholds are applied, 0 to 15 SNPs, is precisely the
regime in which the standard detectors miss 90% to 95% of recombination. One step
up in scale, recombination accounts for most of the SNP distance. Recombination is
therefore most consequential and least detectable at exactly the scale where
outbreak calls are made.

---

## 10. Population structure, phylogeography and attribution

### The two-population picture and its resolution limit

Pearson and colleagues established the split along Wallace's Line from 601
sequence types across more than 1,700 isolates, with Phi_PT = 0.117, P = 0.001, and
proposed "an Australian origin for *B. pseudomallei*, characterized by a single
introduction event into Southeast Asia during a recent glacial period" (PMID
19922616). Their sample was near-balanced and they ran anti-bias checks. They also
stated the load-bearing assumption openly, verbatim, that "the conclusions that we
draw are contingent on an Australian root to this tree and not isolate 668 in
particular." `GAP4` section 8 works through this.

Dale and colleagues then quantified the limit, and this is the most direct
engagement with the manuscript's question in the literature. Using 1,829 isolates
from 35 countries and 664 sequence types, they assigned "88.3% of STs to either
Population 1 or Population 2 with ≥95% probability," with Population 1 being 95%
Australian and Population 2 89% Southeast Asian (PLoS Negl Trop Dis
2011;5(12):e1381, DOI 10.1371/journal.pntd.0001381). **UNVERIFIED: PMID 22163051
came from a publisher page and was not confirmed against an index.**

Their framing of the problem is the sentence to quote: "high rates of recombination
within the genome of this bacterium have confounded attempts to match clinical
samples to geographically defined populations." And their limit is explicit, that
"the seven MLST genes and the current set of STs do not provide enough resolution
for further robust differentiation among subpopulations."

Eighty-eight percent assignment to one of two continents, and nothing finer that is
robust. That is where MLST stops.

### Whole genomes

Chewapreecha and colleagues used 469 isolates from 30 countries collected over 79
years, 1935 to 2013, against K96243, yielding 324,637 core-genome SNPs (PMID
28112723, DOI 10.1038/nmicrobiol.2016.263). Their data "point to Australia as an
early reservoir, with transmission to Southeast Asia followed by onward
transmission to South Asia and East Asia." They saw "repeated reintroductions"
within the Malay Peninsula and between countries on the Mekong. They dated the
arrival of *B. pseudomallei* in the Americas to between 1650 and 1850 from an
African source, "providing a temporal link with the slave trade." And they found
"geographically distinct genes/variants in Australasian or Southeast Asian isolates
alone, with virulence-associated genes being among those over-represented."

They report no species-wide TMRCA, saying instead that "dating of these deeper
evolutionary events is less reliable," so the Australia-to-Asia split is undated.
They also state their sampling caveat plainly, that "a very limited number of
isolates had been stored and were available in areas where melioidosis is either
uncommon or under-reported based on lack of microbiology infrastructure, which
resulted in an unequal geographic representation," and that the African root for
the American isolates was inferred "based on our sampling density."

Gee and colleagues resolved the Western Hemisphere clade specifically, finding that
it derives from "a constricted seeding event from Africa" and, critically, that
"subclades have been resolved that are associated with specific regions within the
Western Hemisphere and suggest that isolates might be correlated geographically
with cases of melioidosis" (PMID 28628442). That sentence is the direct
methodological justification for genomic attribution of exposure origin.

Wu and colleagues give the most recent global picture, comparing 554 southern
Chinese isolates against 3,573 public genomes and identifying 10 evolutionary
clusters, with Chinese isolates enriched in Cluster 1 alongside Thai strains and
distinct from the mostly Australian Cluster 5 (PMID 42377320).

Lichtenegger and colleagues built the cgMLST scheme by challenging K96243 with 469
genomes, retaining 4,221 core and 1,351 accessory targets, validated on 320
datasets with more than 95% good targets in 98.4% of genomes (PMID 33980649, DOI
10.1128/JCM.00093-21). It resolved 150 global isolates into 148 types, Simpson's
diversity 1.00, against 211 sequence types from 468 genomes by conventional MLST.
They used it to identify a sugarcane field as the presumed source of one case,
where environmental isolates differed from the patient strain by 3 to 5 alleles.
The scheme proposes no allele-distance threshold, and it makes no statement about
how recombination affects it, which is a notable omission for the most
recombinogenic bacterium characterized.

Norris and colleagues sequenced 47 isolates from North Central Vietnam, 35 clinical
from Ha Tinh, 10 from soil, one swine and one bear, finding 15 sequence types with
20 of 35 clinical isolates (57%) being ST41 and ST41 later recovered from soil
about a year afterward (PLoS Negl Trop Dis 2026;20(2):e0013945, PMID 41662344, DOI
10.1371/journal.pntd.0013945). Their framing matches this manuscript's, that soil
reservoir genotypes "can tell us about the propensity of *B. pseudomallei*
genotypes to transmit from soil to humans."

### What SNP thresholds do in this species

There is no consensus, validated SNP threshold for *B. pseudomallei*, and the
evidence base is thinner than its use suggests.

Webb and colleagues assemble the published numbers. Earlier Australian
investigations "have used SNP differences ranging from 0 to 5 SNPs for inferring an
environmental transmission event," and their own study "found a maximum of 15 SNPs
in the 17 case-environment isolate matches for which we inferred a causal
transmission" (PMID 35080450). The commonly cited 2 to 37 comparator range is
borrowed from other species. The 15-SNP upper bound rests on 17 informative pairs
from one study. And that study applies no recombination correction at all.

Recombination breaks threshold logic in both directions, and the published examples
are striking.

Upward, Sarovich and colleagues documented a genuine point-source outbreak spanning
1,328 SNPs between ST-125 and ST-126, of which only about 73 (5%) survived
recombination filtering, and wrote that the isolates "demonstrated evidence of
multiple recombination events that were unlikely to have occurred over the
timeframe of the outbreak."

Downward, Aziz and colleagues found same-ST isolate pairs differing by 21,211 and
20,567 genome-wide SNPs, against 404 for a genuinely clonal pair. Meumann and
colleagues found ST562 isolates from Australia, Hainan and Taiwan separated by
6,252 to 7,786 SNPs, falling to 964 to 1,453 after recombination masking, so
masking reduces but does not eliminate the problem.

**UNVERIFIED: the Sarovich 2017, Aziz 2017 and Meumann 2021 numbers came through
Europe PMC extractions with double-checking but without full citation strings.
Retrieve all three before quoting any figure.**

A pair of isolates can acquire hundreds or thousands of apparent SNPs in a single
recombination event, over a single generation. Any threshold applied to an unmasked
SNP alignment in this species is measuring recombination rather than time. Webb's
own recommendation is not a number but "a combination of epidemiology and
phylogenetic analysis including closely related local isolates for context," and
that is the defensible position to adopt.

### What attribution currently rests on

Five published instances, and the base is thinner than the field's confidence
implies.

The Darwin environmental point-source work matched 19 of 98 sampled patient sites
(PMID 35080450). The aromatherapy spray traceback linked four non-travel cases
across four US states to a product and, at continental resolution, to India (PMID
35235727). The Mississippi cluster established a local reservoir from three
patients sharing a strain with soil and water on one property (PMID 38118023). The
cgMLST work identified a sugarcane field (PMID 33980649). And the Georgia ST41
cluster linked four cases across 41 years (PMID 40835221).

Every one of these is a small-n problem where the candidate sources were already
known, or where the answer was continental. The 19% match rate in Darwin is a
candid statement of the current ceiling, achieved with systematic environmental
sampling around patients' own homes.

The gap is specific and it is the strongest justification available for this
manuscript. Whole-genome sequencing is repeatedly asserted to resolve strain
origin, but the resolution has never been quantified. There is no published
misclassification rate for assigning a genome to a country of origin, no confidence
measure accompanying any published attribution, and no cross-validated accuracy
figure at any spatial scale finer than Dale's two-population continental split,
which is MLST-based anyway. Every explicit "limits of phylogeographic inference"
statement in this literature is about MLST resolution or about SNP-distance
overcalling within a region. None addresses whole-genome attribution, and none
formally accounts for the recombination that motivates the whole exercise.

### The sampling problem, stated up front

Our own collection is about 70% Thailand, and it is worse on this axis than
Chewapreecha's. That belongs in the manuscript's framing rather than in a
limitations paragraph at the end. Note also that the burden model puts 44% of
global cases in South Asia against 40% in East Asia and Pacific, so the sampling
skew runs opposite to where the disease actually is. `GAP4` covers what can and
cannot be inferred under this skew.

---

## 11. Where this study fits

Four gaps, each addressed by the analysis.

Recombination has never been measured across the species with the population
partitioned first and the per-unit values reported as a distribution. Nandi
measured 106 genomes from one Asian locale and reported three clade values. Seng
measured three lineages in one Thai region. Chewapreecha partitioned into 19
clusters and re-mapped each to a lineage-specific reference, which is the right
design, but reported no r/m at all. Nobody has asked whether recombination rate is
a species constant, and the published values already suggest it is not, spanning
2.2 to 8.5 across five lineages in two studies.

No published guidance exists on the divergence range over which Gubbins produces a
measurement rather than a detection failure. The field has one unvalidated ceiling,
Zheng's 5,000 pairwise SNP distances, and no floor. Both method papers describe
their tools as suited to recent diversification without saying where recent stops,
and Croucher quantifies the too-clonal failure at 90% to 95% of events missed
without saying at what divergence that begins.

Reference choice has never been evaluated systematically in this organism, which
`GAP1` section 4 documents at length, even though at least four references are in
concurrent use and no work bridges their coordinate systems.

And no study has measured how much geographic structure survives recombination
correction, which is the question that decides whether attribution is feasible at
all.

---

## 12. Corrections and cautions

### 12.1 Citation errors in existing project documents

`GAP1` section 4 cites PMID 35080450 as "Localized *Burkholderia pseudomallei*
Genotype Clusters Within Darwin, Northern Territory, Australia. *J Clin Microbiol*
2022;60(2):e0164821." The authors, DOI and article number are right. The title and
issue are wrong. PubMed returns "Genomic Epidemiology Links *Burkholderia
pseudomallei* from Individual Human Cases to *B. pseudomallei* from Targeted
Environmental Sampling in Northern Australia," *J Clin Microbiol* 2022;**60(3)**.
A title search returns no paper by the cited name. The fine-scale Darwin clustering
paper the title appears to describe is Rachlin and colleagues, *Sci Rep*
2020;10:5443. **The substance quoted in `GAP1` from PMID 35080450, the
six-reference comparison and the 113 to 136 SNP shift, is not in the abstract and
must be re-checked against the full text.**

`GAP1` section 4 describes PMID 41662344 as mapping 1,468 genomes to 1026b. The
paper newly characterized 47 isolates. The 1,468 figure is the size of the global
comparison set, including those 47.

`GAP1` section 4 states that Wu and colleagues report a 3,805,619 bp core alignment,
52.5% of K96243. Two independent retrieval attempts failed to confirm it. Publisher
returns 403, no PMC deposit. Hold the number until the full text is available.

`GAP4` section 12 gives PMID 32149236 for Pearson 2020 in the dating table while
`GAP1` section 4 gives PMID 32134991 for what appears to be the same paper, *PLoS
Pathog* 2020;16(3):e1008298. One is wrong.

### 12.2 Numbers to stop quoting

The "45 countries where it is endemic but never reported" formulation merges two
distinct figures. Use 45 endemic-but-under-reported plus a further 34
probably-endemic-never-reported.

"The highest recombination rate reported in bacteria" is a per-allele MLST quantity
from Pearson 2009 and is not comparable to any genome-wide r/m.

"86% core genome" is a 2008 microarray result and is not a base-level callable
fraction.

The 12- to 13-fold diabetes risk attributed to Suputtamongkol 1999 could not be
traced to a number in that paper.

The 62-year latency record was overturned by Gee 2017 and should be cited only as
an example of a claim that genomics corrected.

### 12.3 Numbers that need retrieval before use

The Wu core alignment length. The Brennan 2025 Georgia SNP distances. The Sarovich
2017, Aziz 2017 and Meumann 2021 SNP figures with full citations. The Mississippi
environmental sample counts. The Ubon Ratchathani case fatality rate. Per-replicon
GC content, which should be computed rather than cited. The insertion-sequence
counts for K96243 and *B. mallei*. Whether *B. pseudomallei* appears in Vos and
Didelot's 48-species table. And the Sarovich 2014 PMID, where a direct PubMed query
gave 24618705 and one research pass gave 24614774.

### 12.4 Fabrications caught during this research

Three, recorded because they show the failure mode rather than to pad the list.

A PDF fetch of Chewapreecha 2017 from an institutional repository returned "1,387
isolates from Thailand, Laos and Vietnam," a "5.27 Mb core genome" and an "r/m
3–4x," all of which contradict the PMC full text of the same paper, which reports
469 isolates from 30 countries and no r/m at all. None of it was used.

A search result claimed "r/m = 973.8 for *Burkholderia pseudomallei* MSHR3." The
strain name does not match standard nomenclature and the figure is two orders of
magnitude outside every verified estimate.

A publisher page returned PMID 37040739 for a travel-medicine review, which
actually belongs to an unrelated speech-pathology paper. The correct identifier is
36971472.

The general rule this supports is the project's own. Check per-item values, never
infer from a summary line, and re-verify any figure that arrives through a
summarizing intermediary.

---

## 13. Citation table

Entries were checked against the returned record for title, journal, year, volume,
pages, PMID and DOI, except where marked.

| Role | Citation | PMID | DOI |
|---|---|---|---|
| Global burden model | Limmathurotsakul D, Golding N, Dance DAB, et al. Predicted global distribution of *Burkholderia pseudomallei* and burden of melioidosis. *Nat Microbiol* 2016;1:15008 | 26877885 | [10.1038/nmicrobiol.2015.8](https://doi.org/10.1038/nmicrobiol.2015.8) |
| Current umbrella review | Meumann EM, Limmathurotsakul D, Dunachie SJ, Wiersinga WJ, Currie BJ. *Burkholderia pseudomallei* and melioidosis. *Nat Rev Microbiol* 2024;22(3):155–169 | 37794173 | [10.1038/s41579-023-00972-5](https://doi.org/10.1038/s41579-023-00972-5) |
| Disease primer | Wiersinga WJ, Virk HS, Torres AG, et al. Melioidosis. *Nat Rev Dis Primers* 2018;4:17107 | 29388572 | [10.1038/nrdp.2017.107](https://doi.org/10.1038/nrdp.2017.107) |
| Best clinical denominator | Currie BJ, Mayo M, Ward LM, et al. The Darwin Prospective Melioidosis Study: a 30-year prospective, observational investigation. *Lancet Infect Dis* 2021;21(12):1737–1746 | 34303419 | [10.1016/S1473-3099(21)00022-0](https://doi.org/10.1016/S1473-3099(21)00022-0) |
| DALYs, downstream of the 2016 model | Birnie E, Virk HS, Savelkoel J, et al. Global burden of melioidosis in 2015. *Lancet Infect Dis* 2019;19(8):892–902 | 31285144 | [10.1016/S1473-3099(19)30157-4](https://doi.org/10.1016/S1473-3099(19)30157-4) |
| Incubation period | Currie BJ, Fisher DA, Anstey NM, Jacups SP. Melioidosis: acute and chronic disease, relapse and re-activation. *Trans R Soc Trop Med Hyg* 2000;94(3):301–304 | 10975006 | [10.1016/S0035-9203(00)90333-X](https://doi.org/10.1016/S0035-9203(00)90333-X) |
| Latency is rare; time bomb refuted | Howes M, Currie BJ. Melioidosis and Activation from Latency: The "Time Bomb" Has Not Occurred. *Am J Trop Med Hyg* 2024 | 38806042 | [10.4269/ajtmh.24-0007](https://doi.org/10.4269/ajtmh.24-0007) |
| The 62-year claim, original | Ngauy V, Lemeshev Y, Sadkowski L, Crawford G. Cutaneous melioidosis in a man who was taken as a prisoner of war by the Japanese during World War II. *J Clin Microbiol* 2005;43(2):970–972 | 15695721 | [10.1128/JCM.43.2.970-972.2005](https://doi.org/10.1128/JCM.43.2.970-972.2005) |
| The 62-year claim, overturned; Western Hemisphere clade | Gee JE, Gulvik CA, Elrod MG, et al. Phylogeography of *Burkholderia pseudomallei* Isolates, Western Hemisphere. *Emerg Infect Dis* 2017;23(7):1133–1138 | 28628442 | [10.3201/eid2307.161978](https://doi.org/10.3201/eid2307.161978) |
| Recurrence, Darwin, 74% relapse | Sarovich DS, Ward L, Price EP, et al. Recurrent melioidosis in the Darwin Prospective Melioidosis Study. *J Clin Microbiol* 2014;52(2):650–653 | 24478504 | [10.1128/JCM.02239-13](https://doi.org/10.1128/JCM.02239-13) |
| Recurrence, Thailand, 25% reinfection | Maharjan B, Chantratita N, Vesaratchavest M, et al. Recurrent melioidosis in patients in northeast Thailand is frequently due to reinfection rather than relapse. *J Clin Microbiol* 2005;43(12):6032–4 | 16333094 | [10.1128/JCM.43.12.6032-6034.2005](https://doi.org/10.1128/JCM.43.12.6032-6034.2005) |
| Product traceback, four non-travel US cases | Gee JE, Bower WA, Kunkel A, et al. Multistate Outbreak of Melioidosis Associated with Imported Aromatherapy Spray. *N Engl J Med* 2022;386(9):861–868 | 35235727 | [10.1056/NEJMoa2116130](https://doi.org/10.1056/NEJMoa2116130) |
| Local US endemicity, genomically established | Petras JK, Elrod MG, Ty MC, et al. Locally Acquired Melioidosis Linked to Environment, Mississippi, 2020–2023. *N Engl J Med* 2023;389(25):2355–2362 | 38118023 | [10.1056/NEJMoa2306448](https://doi.org/10.1056/NEJMoa2306448) |
| Georgia ST41 across 41 years | Brennan S, Thompson JM, Gulvik CA, et al. Related Melioidosis Cases with Unknown Exposure Source, Georgia, USA, 1983–2024. *Emerg Infect Dis* 2025;31(9):1802–1806 | 40835221 | [10.3201/eid3109.250804](https://doi.org/10.3201/eid3109.250804) |
| Current US endemicity position | Currie BJ, Kaestli M, Meumann EM. Global dispersal of *Burkholderia pseudomallei* and the evolving endemicity of melioidosis in the USA. *PLoS Negl Trop Dis* 2026;20(4):e0014217 | 42030350 | [10.1371/journal.pntd.0014217](https://doi.org/10.1371/journal.pntd.0014217) |
| Clinical-to-environmental genomic linkage; SNP thresholds | Webb JR, Mayo M, Rachlin A, et al. Genomic Epidemiology Links *Burkholderia pseudomallei* from Individual Human Cases to *B. pseudomallei* from Targeted Environmental Sampling in Northern Australia. *J Clin Microbiol* 2022;60(3):e0164821 | 35080450 | [10.1128/JCM.01648-21](https://doi.org/10.1128/JCM.01648-21) |
| Reference genome; two replicons; 16 GIs | Holden MTG, Titball RW, Peacock SJ, et al. Genomic plasticity of the causative agent of melioidosis, *Burkholderia pseudomallei*. *Proc Natl Acad Sci U S A* 2004;101(39):14240–5 | 15377794 | [10.1073/pnas.0403302101](https://doi.org/10.1073/pnas.0403302101) |
| 71 genomic islands; tRNA-mediated integration | Tuanyok A, Leadem BR, Auerbach RK, et al. Genomic islands from five strains of *Burkholderia pseudomallei*. *BMC Genomics* 2008;9:566 | 19038032 | [10.1186/1471-2164-9-566](https://doi.org/10.1186/1471-2164-9-566) |
| aCGH core/accessory; accessory clusters by source | Sim SH, Yu Y, Lin CH, et al. The core and accessory genomes of *Burkholderia pseudomallei*. *PLoS Pathog* 2008;4(10):e1000178 | 18927621 | [10.1371/journal.ppat.1000178](https://doi.org/10.1371/journal.ppat.1000178) |
| Open pangenome; gene order conserved despite recombination | Spring-Pearson SM, Stone JK, Doyle A, et al. Pangenome Analysis of *Burkholderia pseudomallei*: Genome Evolution Preserves Gene Order despite High Recombination Rates. *PLoS One* 2015;10(10):e0140274 | 26484663 ⚠ | [10.1371/journal.pone.0140274](https://doi.org/10.1371/journal.pone.0140274) |
| YLF/BTFC, Asia against Australia | Tuanyok A, Auerbach RK, Brettin TS, et al. A horizontal gene transfer event defines two distinct groups within *Burkholderia pseudomallei* that have dissimilar geographic distributions. *J Bacteriol* 2007;189(24):9044–9 | 17933898 | [10.1128/JB.01264-07](https://doi.org/10.1128/JB.01264-07) |
| bimA(Bm) and fhaB3 disease associations | Sarovich DS, Price EP, Webb JR, et al. Variable virulence factors in *Burkholderia pseudomallei* (melioidosis) associated with human disease. *PLoS One* 2014;9(3):e91682 | 24618705 ⚠ | [10.1371/journal.pone.0091682](https://doi.org/10.1371/journal.pone.0091682) |
| bimA(Bm) mouse phenotype | Morris JL, Fane A, Sarovich DS, et al. Increased neurotropic threat from *Burkholderia pseudomallei* strains with a *B. mallei*-like variation in the bimA motility gene, Australia. *Emerg Infect Dis* 2017;23(5):740–749 | 28457226 | [10.3201/eid2305.151417](https://doi.org/10.3201/eid2305.151417) |
| LPS genotypes A/B/B2, 999 strains | Tuanyok A, Stone JK, Mayo M, et al. The genetic and molecular basis of O-antigenic diversity in *Burkholderia pseudomallei* lipopolysaccharide. *PLoS Negl Trop Dis* 2012;6(1):e1453 | 22235357 | [10.1371/journal.pntd.0001453](https://doi.org/10.1371/journal.pntd.0001453) |
| CPS cluster crosses the species boundary | Sim BMQ, Chantratita N, Ooi WF, et al. Genomic acquisition of a capsular polysaccharide virulence cluster by non-pathogenic *Burkholderia* isolates. *Genome Biol* 2010;11(8):R89 | 20799932 | [10.1186/gb-2010-11-8-r89](https://doi.org/10.1186/gb-2010-11-8-r89) |
| MLST scheme; *B. mallei* is a Bp clone | Godoy D, Randle G, Simpson AJ, et al. Multilocus sequence typing and evolutionary relationships among the causative agents of melioidosis and glanders. *J Clin Microbiol* 2003;41(5):2068–79 | 12734250 | [10.1128/JCM.41.5.2068-2079.2003](https://doi.org/10.1128/JCM.41.5.2068-2079.2003) |
| Australian origin; per-allele MLST r/m | Pearson T, Giffard P, Beckstrom-Sternberg S, et al. Phylogeographic reconstruction of a bacterial species with high levels of lateral gene transfer. *BMC Biol* 2009;7:78 | 19922616 | [10.1186/1741-7007-7-78](https://doi.org/10.1186/1741-7007-7-78) |
| MLST resolution limit; two-population assignment | Dale J, Price EP, Hornstra H, et al. Epidemiological Tracking and Population Assignment of the Non-Clonal Bacterium, *Burkholderia pseudomallei*. *PLoS Negl Trop Dis* 2011;5(12):e1381 | 22163051 ⚠ | [10.1371/journal.pntd.0001381](https://doi.org/10.1371/journal.pntd.0001381) |
| Cross-species r/m scale (MLST/ClonalFrame) | Vos M, Didelot X. A comparison of homologous recombination rates in bacteria and archaea. *ISME J* 2009;3(2):199–208 | 18830278 | [10.1038/ismej.2008.93](https://doi.org/10.1038/ismej.2008.93) |
| Modern genome-based r/m comparator, 162 species | Torrance EL, Burton C, Diop A, Bobay L-M. Evolution of homologous recombination rates across bacteria. *PNAS* 2024;121(18):e2316302121 | 38657048 | [10.1073/pnas.2316302121](https://doi.org/10.1073/pnas.2316302121) |
| Genome-wide r/m 7.2; RM barriers; clades as isolation units | Nandi T, Holden MTG, Didelot X, et al. *Burkholderia pseudomallei* sequencing identifies genomic clades with distinct recombination, accessory, and epigenetic profiles. *Genome Res* 2015;25(1):129–41 | 25236617 | [10.1101/gr.177543.114](https://doi.org/10.1101/gr.177543.114) |
| Global phylogeography; hierBAPS to reach Gubbins' range | Chewapreecha C, Holden MTG, Vehkala M, et al. Global and regional dissemination and evolution of *Burkholderia pseudomallei*. *Nat Microbiol* 2017;2:16263 | 28112723 | [10.1038/nmicrobiol.2016.263](https://doi.org/10.1038/nmicrobiol.2016.263) |
| Per-lineage r/m with CIs; 96.6–99.9% of genes recombined | Seng R, Chomkatekaew C, Tandhavanant S, et al. Genetic diversity, determinants, and dissemination of *Burkholderia pseudomallei* lineages implicated in melioidosis in Northeast Thailand. *Nat Commun* 2024;15:5699 | 38972886 | [10.1038/s41467-024-50067-9](https://doi.org/10.1038/s41467-024-50067-9) |
| The only published operating threshold, 5,000 PSDs | Zheng H, Qin J, Chen H, et al. Genetic diversity and transmission patterns of *Burkholderia pseudomallei* on Hainan island, China. *Microb Genom* 2021;7(11) | 34762026 | [10.1099/mgen.0.000659](https://doi.org/10.1099/mgen.0.000659) |
| 554 southern China isolates; 10 global clusters | Wu H, Lei Z, Chen S, et al. Genomic landscape and phylogenetic insights of *B. pseudomallei* over two decades in southern China. *Emerg Microbes Infect* 2026;15(1):2691358 | 42377320 | [10.1080/22221751.2026.2691358](https://doi.org/10.1080/22221751.2026.2691358) |
| cgMLST scheme; sugarcane-field attribution | Lichtenegger S, Trinh TT, Assig K, et al. Development and Validation of a *Burkholderia pseudomallei* Core Genome Multilocus Sequence Typing Scheme. *J Clin Microbiol* 2021;59(8):e0009321 | 33980649 | [10.1128/JCM.00093-21](https://doi.org/10.1128/JCM.00093-21) |
| North Central Vietnam; ST41 soil to human | Norris MH, Au La TH, Metrailer MC, et al. Expanding the molecular epidemiology of melioidosis in North Central Vietnam. *PLoS Negl Trop Dis* 2026;20(2):e0013945 | 41662344 | [10.1371/journal.pntd.0013945](https://doi.org/10.1371/journal.pntd.0013945) |
| Gubbins; both failure modes named | Croucher NJ, Page AJ, Connor TR, et al. Rapid phylogenetic analysis of large samples of recombinant bacterial whole genome sequences using Gubbins. *Nucleic Acids Res* 2015;43(3):e15 | 25414349 | [10.1093/nar/gku1196](https://doi.org/10.1093/nar/gku1196) |
| ClonalFrameML; within-lineage by design | Didelot X, Wilson DJ. ClonalFrameML: efficient inference of recombination in whole bacterial genomes. *PLoS Comput Biol* 2015;11(2):e1004041 | 25675341 | [10.1371/journal.pcbi.1004041](https://doi.org/10.1371/journal.pcbi.1004041) |
| fastGEAR; needs the diverse alignment kept together | Mostowy R, Croucher NJ, Andam CP, et al. Efficient inference of recent and ancestral recombination within bacterial populations. *Mol Biol Evol* 2017;34(5):1167–1182 | 28199698 | [10.1093/molbev/msx066](https://doi.org/10.1093/molbev/msx066) |

⚠ marks a PMID taken from a publisher page rather than confirmed against an index,
or a conflict between sources. Re-verify these before submission.
