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

## Open discrepancy, not yet resolved

**`[103]`: four patients or five?** The background prose says "four patients in
Georgia, USA, with disease episodes spanning 1983–2024". A project note records
this focus as **five** cases over the same span. The Brennan title says only
"Related Melioidosis Cases". The count must be read out of the paper itself
before either number is used. Do not quote a number for this focus until it is.

## Still to resolve

- `[100]` PubMLST, expected to be a Jolley reference for the database rather than
  for *B. pseudomallei* specifically.
- `[102]` the quoted claim of a "very strong phylogeographic signal that allows
  accurate identification of strain origin on a continental level". This is a
  direct quotation and needs its actual source; a topic search did not find it.
- `[104]`–`[111]`, the acquired-resistance block: PenA structural mutations,
  *bpss1219* PBP3 deletion, *amrR*/*bpeT* efflux regulator loss of function,
  BpeEF-OprC and trimethoprim-sulfamethoxazole, and the ARDaP tool. This block
  carries the most specific factual claims in the background and none of them
  currently has a citation that resolves.
- `[112]`–`[122]`, the climate and rainfall block, including the Townsville
  fortnightly-rainfall association, the 31.6°S temperate Western Australian
  focus, the 77.7% to 97.4% PCR positivity shift, the 5% to 82% seasonal culture
  positivity with Spearman's rho 0.905, and the 26°C wettest-quarter MaxEnt
  threshold.
- `[123]`–`[130]`: ST562 intercontinental sharing, cgMLST framing, prospective
  case-to-environment linkage, GWAS of virulence loci, PCR-HRM regional
  assignment, the African origin of South American isolates, the Australian goat
  farm, and the typhoon airborne-transmission isolate.

These are the topics handoff section 5 identified as ground the SciSpace draft
covers and our corpus does not, which is exactly why they cannot be resolved from
the corpus and need primary lookups.
