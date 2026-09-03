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

**`[123]`, ST562.** ⚠ **Correction to an earlier version of this entry.** It said
the background claimed ST562 "in both Australia and Southeast Asia" and that the
region was therefore wrong. **That was my error, not the background's.** The
sentence says "Australia and **southern China**", which is right: Meumann 2021
reports ST562 from Hainan Province. I read a truncated context ending "Australia
and so..." and expanded it to the wrong phrase instead of checking the full
sentence, which is the same shortcut this handoff documents elsewhere.

What is genuinely missing is the qualification the background leaves out. Those isolates
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

## The fabricated entries have a signature, and it is mechanical

Found while fixing the two sentences above, and it is the most useful audit
result here.

**The entries for `[103]`–`[130]` exist, but they sit in the document body rather
than under `## References`.** That is why both tools reported them as dangling:
`verify_references_bp.py` splits on the `## References` heading, so this block
counts as prose, its `[n]` labels are counted as citation marks, and nothing in
it is counted as a definition. The 34 dangling and the 409 marks are both partly
artifacts of where the block sits. `[97]`–`[102]` have **no entry anywhere**,
which is why `[102]` could not be sourced: there was never anything to source.

Within that block, five entries share a signature:

| ref | title as given | tell |
|---|---|---|
| `[123]` | "ST562 Identified in Both Australia and Southern China: Intercontinental Sharing of a *B. pseudomallei* Sequence Type" | title restates the claim sentence |
| `[124]` | "Formal Development and Validation of the 4,221-Locus Core-Genome MLST Scheme for *B. pseudomallei*" | title restates the claim sentence |
| `[126]` | virulence GWAS | out of scope |
| `[128]` | African origin | out of scope for sourcing, in scope for the sentence |
| `[130]` | typhoon airborne transmission | out of scope |

All five carry the **`10.60692` prefix** and **no journal field**, and four are
dated **2024**. `[123]`'s DOI is `10.60692/x9erj-5ns21`, which is the exact
identifier the handoff traced to a repository rather than a journal.

**Three of the five have real papers, which I found independently before noticing
the pattern:** `[123]` is Meumann 2021, `[124]` is Lichtenegger 2021, `[128]` is
Sarovich 2016. So these are not merely bad identifiers attached to real work.
They are entries whose titles were written to match the sentence citing them,
standing in for real papers that already existed and were easy to find.

That makes the signature worth encoding rather than remembering: **`10.60692`
prefix, plus no journal, plus a title that paraphrases the citing sentence.** The
first two are mechanical and already flagged by `verify_references_bp.py` as
UNKNOWN-PREFIX and NO-METADATA. The third is the one that identifies fabrication
rather than sloppiness, and it is checkable by comparing entry title against the
text of the sentences citing it.

## `[102]` cannot be substantiated, and the attribution is checkable

The sentence names its author, which makes this decidable rather than merely
unfound: "**Viberg et al.** used whole-genome phylogenetics to correctly assign
the isolate of a cystic fibrosis patient to Southeast Asia based solely on its
position in the global *B. pseudomallei* tree, confirming the established
principle that the organism carries a 'very strong phylogeographic signal that
allows accurate identification of strain origin on a continental level'".

**All five Viberg *Burkholderia* papers in PubMed were retrieved and checked.**

| PMID | first author | what it is |
|---|---|---|
| 25883282 | **Viberg LT** | Genome announcement, five Australian CF isolates |
| 28400528 | **Viberg LT** | Within-host evolution, seven Australasian CF patients (mBio) |
| 29394337 | Sarovich DS | Meropenem susceptibility and efflux regulators |
| 29989529 | Price EP | Transcriptomics of longitudinal CF isolates |
| 25339397 | Price EP | Polyclonal infection with the same ST |

Only two have Viberg as first author, and both are about **within-host evolution
and antibiotic resistance in Australian CF patients**. Neither assigns an isolate
to Southeast Asia, neither is a phylogeographic study, and a one-paragraph genome
announcement is not a plausible source for a quoted "established principle". The
quotation itself was not found by four separate searches.

**Verdict: unsupported. Do not use `[102]`, and do not carry the quotation.** The
underlying idea, that continental-scale assignment works, is true and is now
sourced properly in the manuscript to Sarovich 2016 and Gasqué 2024. It does not
need this sentence.

The caveat on this verdict, stated so it can be overturned: only titles and
abstracts were read, not full texts. If someone produces the sentence from a real
paper, this entry is wrong. Nobody should quote it until they have.

## `[97]`: no intended source found, and the claim splits in two

"The limited resolution of MLST ... means that it cannot capture the full genomic
diversity of *B. pseudomallei* **or reliably distinguish between isolates from
different geographic regions at the country level** [95], [97]."

No source was found that makes the whole claim. The two halves need different
treatment.

- **Resolution.** Directly demonstrated by Price 2015 (PMID 25339397): twelve
  isolates from one patient, identical ST, polyclonal on whole-genome data. That
  is now manuscript reference `[24]`.
- **Country-level discrimination.** This is *this paper's own finding*, and it
  should not be imported from a background citation at all. Citing someone else
  for the paper's own result would be circular in the direction that flatters it.
  Rachlin 2019 (PMID 31433287) was checked as a candidate and argues the
  opposite, reporting "limited geographical dispersal amongst sequence types",
  though it does document one suspected case of ST homoplasy.

**Verdict: split the sentence.** Keep the resolution half on Price. Drop the
country-level half or replace it with a forward reference to the paper's own
Results section 8.

## Still to resolve, in scope

Scope is fixed by `BACKGROUND_SCOPE_DECISION_2026-09-03.md`: sections 6, 7 and 8
enter the manuscript, plus 5.1 for Methods. That left 11 in-scope dangling
citations. **All 11 are now closed:** nine resolved to a verified source, and two
closed as unusable, `[102]` unsupported and `[97]` split. Nothing in scope is
outstanding.

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
