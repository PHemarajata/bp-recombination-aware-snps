# Resolved references for the background rebuild

Step 2 of `HANDOFF_CITATIONS_2026-09-03.md` section 11. This is the running
register of citations resolved against a primary record, built as the rebuild
proceeds. `BIBLIOGRAPHY_TRIAGE.tsv` says what needs resolving;
this file says what each one resolved *to*, and how it was checked.

**Rule.** Nothing enters this file from the handoff, from
`citation_audit_report.md`, or from the SciSpace draft. Every row was verified
against PubMed in this session, and the verification is named. The merge rule
from handoff section 5 applies: no `10.60692`, no Zenodo, no thesis repository,
no conference abstract, and no repository copy of a paper that has a publisher
DOI.

## Status

`build_bibliography_bp.py` over 486 corpus records, on the tracked background:

| verdict | n | meaning |
|---|---|---|
| DANGLING | 34 | cited in prose, no entry at all (`[97]`–`[130]`) |
| LOOKUP | 36 | flagged, nothing in the verified corpus matches |
| REPLACE | 10 | flagged, and a verified record matches |
| KEEP | 24 | unflagged, and a verified record confirms it |
| KEEP-UNMATCHED | 26 | unflagged but uncorroborated here |

34 resolve mechanically from the corpus with a PMID attached. 70 need a human,
and this file is where those land as they are done.

## Resolved against PubMed, 2026-09-03

| ref | citation | PMID | DOI | how checked |
|---|---|---|---|---|
| `[99]` | Lichtenegger S, Trinh TT, Assig K, et al. Development and Validation of a *Burkholderia pseudomallei* Core Genome Multilocus Sequence Typing Scheme To Facilitate Molecular Surveillance. *J Clin Microbiol* 2021;59(8):e0009321 | 33980649 | 10.1128/JCM.00093-21 | PubMed record retrieved; abstract states 4,221 core and 1,351 accessory targets from K96243 challenged with 469 genomes, which is the scheme this project uses |
| `[101]` | Petras JK, Elrod MG, Ty MC, et al. Locally Acquired Melioidosis Linked to Environment — Mississippi, 2020-2023. *N Engl J Med* 2023;389(25):2355-2362 | 38118023 | 10.1056/NEJMoa2306448 | PubMed record retrieved; three patients in one Gulf Coast county, same Western Hemisphere strain recovered from three environmental samples |
| `[103]` | Brennan S, et al. Related Melioidosis Cases with Unknown Exposure Source, Georgia, USA, 1983-2024. *Emerg Infect Dis* 2025;31(9):1802-1806 | 40835221 | 10.3201/eid3109.250804 | PubMed record retrieved; title carries the 1983–2024 span and the unknown-exposure framing |
| `[127]` | Gasqué M, Guernier-Cambert V, Girault G, et al. Rapid confirmation of autochthonous origin in suspected cases of melioidosis from French overseas departments in the Caribbean and the Indian Ocean by PCR-high resolution melting (HRM) analysis. *Infect Genet Evol* 2024;127:105711 | 39732273 | 10.1016/j.meegid.2024.105711 | PubMed record retrieved; abstract matches the claim exactly, three region-specific SNP markers for the Indian Ocean, the Americas and Martinique |
| `[128]` | Sarovich DS, Garin B, De Smet B, et al. Phylogenomic Analysis Reveals an Asian Origin for African *Burkholderia pseudomallei* and Further Supports Melioidosis Endemicity in Africa. *mSphere* 2016;1(2):e00089-15 | 27303718 | 10.1128/mSphere.00089-15 | PubMed record retrieved. **Supports only half the sentence citing it — see below** |
| `[100]` | Godoy D, Randle G, Simpson AJ, et al. Multilocus sequence typing and evolutionary relationships among the causative agents of melioidosis and glanders. *J Clin Microbiol* 2003;41(5):2068–79 | 12734250 | 10.1128/JCM.41.5.2068-2079.2003 | Already in the verified corpus (`BACKGROUND_RESEARCH` reference table); this is the seven-locus scheme itself |
| `[123]` | Meumann EM, Kaestli M, Mayo M, et al. Emergence of *Burkholderia pseudomallei* Sequence Type 562, Northern Australia. *Emerg Infect Dis* 2021;27(4):1057-1067 | 33754984 | 10.3201/eid2704.202716 | PubMed record retrieved. **Correct the sentence when using it — see below** |
| `[124]` | Lichtenegger S, et al., as `[99]` | 33980649 | 10.1128/JCM.00093-21 | Same paper as `[99]`. The two markers cite one source and should be merged on renumbering |
| `[125]` | Webb JR, Mayo M, Rachlin A, et al. Genomic Epidemiology Links *Burkholderia pseudomallei* from Individual Human Cases to *B. pseudomallei* from Targeted Environmental Sampling in Northern Australia. *J Clin Microbiol* 2022;60(3):e0164821 | 35080450 | 10.1128/JCM.01648-21 | PubMed record retrieved; 98 patient sites, 975 environmental samples, genotype match for 19 patients (19%). Exact match for the claim |

### Two audit corrections confirmed independently

Handoff section 4 reported both from its own PubMed lookups. Both are confirmed
here against the retrieved records rather than taken on trust.

- **"Petras AMB" is Petras JK.** The author is Julia K. Petras.
- **"Brennan BG" is Brennan S.**

### The Lichtenegger inversion, confirmed

`citation_audit_report.md` section 7.3 proposed a "Lichtenegger 2024" as the
formal development-and-validation paper, distinct from a 2021 paper describing
application. That is backwards. **Lichtenegger 2021 (PMID 33980649) is itself
titled "Development and Validation of..."**, and its abstract describes building
and validating the scheme. The proposed 2024 paper carries a `10.60692`
identifier and was not found in PubMed. Do not cite it.

## A claim that its own source does not support

**`[128]`, the transatlantic slave trade.** The background says the African and
South American populations share a common origin, "with phylogenomic evidence
supporting an African origin for Central and South American isolates and a
temporal link with the transatlantic slave trade".

Sarovich 2016 supports the first half and contradicts the framing of the second.
Verbatim from the abstract: "South American strains reside within the African
clade, suggesting more recent dissemination from West Africa to the Americas",
so African origin for South American isolates is sound. But the paper's proposed
mechanism is **Austronesian migration from Indonesian Borneo to Madagascar around
2,000 years ago**, and its headline finding is an **Asian** origin for the
African isolates. The transatlantic slave trade appears nowhere in it.

So the slave-trade link is either sourced from a different paper or is not
sourced at all. **Do not carry that clause on this citation.** Either find the
paper that makes the claim, or cut the clause and keep the part Sarovich
supports. This is the failure mode the audit never checked for: not a broken
identifier, but a real paper cited for something it does not say.

Note also for the paper's own argument: this study found "distinct
geography-specific clades for Africa, the Americas, Asia and Australasia", which
is regional structure, consistent with our own region-level result.

## A second sentence to correct, and it helps the paper

**`[123]`, ST562 "in both Australia and Southeast Asia".** Meumann 2021 places
ST562 in northern Australia and reports ST562 isolates from **Hainan Province,
China, and Pingtung County, Taiwan**. That is East Asia, not Southeast Asia, so
the region is wrong as written.

The more useful correction is the one the background leaves out. Those isolates
were **"distantly related to ST562 strains from Australia"**, and the paper says
"the origin and transmission mode of ST562 into Australia remain uncertain". So
this is not clean evidence of intercontinental sharing of a lineage. It is
evidence that **the same sequence type occurs on two continents in genomes that
are not closely related**, which is the homoplasy argument, and it is direct
external support for this manuscript's finding that country-level attribution
fails while regional attribution holds. Cited correctly it strengthens Results 8
instead of being a stray fact in a background.

Related, and worth using the same way: `[125]` Webb 2022 warns that "WGS and
careful genomics are required to avoid overcalling the relatedness between
clinical and environmental isolates".

## Open discrepancy, not yet resolved

**`[103]`: four patients or five?** The background prose says "four patients in
Georgia, USA, with disease episodes spanning 1983–2024". A project note records
this focus as **five** cases over the same span. The Brennan title says only
"Related Melioidosis Cases". The count must be read out of the paper itself
before either number is used. Do not quote a number for this focus until it is.

## Still to resolve, in scope

Scope is now fixed by `BACKGROUND_SCOPE_DECISION_2026-09-03.md`: sections 6, 7
and 8 enter the manuscript, plus 5.1 for Methods. That leaves 11 in-scope
dangling citations, of which **9 are resolved above**. Two remain.

- `[97]` the claim that typing cannot "reliably distinguish between isolates from
  different geographic regions at the country level". This is the background's
  version of this paper's own central negative result, so it needs a real source
  rather than a plausible one. `[95]` is cited alongside it and is defined, so
  start there.
- `[102]` the quotation "very strong phylogeographic signal that allows accurate
  identification of strain origin on a continental level". Three topic searches
  did not find it. Because it is presented as a **direct quotation**, it either
  has a specific source or it is fabricated, and the second possibility has
  precedent here: the corpus already documents three caught fabrications, and
  this background re-dated four real papers to July 2024. Treat as unverified
  until the sentence is found in a real paper. **Do not carry a quotation whose
  source cannot be produced.**

## Deliberately not resolved, out of scope

23 dangling citations are out of scope per the scope decision and are **not**
being sourced: `[98]`; `[104]`–`[111]`, the eight-reference acquired-resistance
block; `[112]`–`[122]`, the eleven-reference climate and rainfall block; `[126]`
virulence GWAS; `[129]` the goat farm; and `[130]` typhoon airborne
transmission.

These are real topics and several carry specific, checkable claims. They are not
being sourced because the sections containing them do not enter this manuscript,
and sourcing a sentence that is about to be cut is wasted work. If the background
is ever finished as a standalone review, they come back into play, and this list
is where that work starts.
