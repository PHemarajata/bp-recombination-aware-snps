# Citation audit + the missing literature pass

**2026-08-23.** Every PMID and DOI in `MANUSCRIPT_OUTLINE_2026-08-21.md` and
`METHODS_DRAFT_2026-08-19.md` checked **against a fetched PubMed record**, not
against an internal document. Closes open items 11 and 13, and §6.6's
"never searched" gap.

> **Headline: the corpus's citations are in better shape than feared — 13 of 13
> verified correct — but the literature pass found a 2025 paper that reports
> 80.8% COUNTRY-level attribution for Salmonella from cgMLST. That is the exact
> task we report as failing, and the paper must address it directly.**

---

## 1. Verified correct (13)

According to PubMed. All match the corpus's journal, year, volume and first
author unless noted.

| PMID | citation as used | status |
|---|---|---|
| 25236617 | Nandi, *Genome Res* 2015;25:129–141 | ✅ vol 25(1):129-41 |
| 26877885 | Limmathurotsakul, *Nat Microbiol* 2016;1:15008 | ✅ doi nmicrobiol.2015.8 |
| 27110344 | Murray, *Methods Ecol Evol* 2016 | ✅ vol 7(1):80-89 (PubMed year 2015 = epub) |
| 28112723 | Chewapreecha, *Nat Microbiol* 2017;2:16263 | ✅ |
| 28400528 | Viberg, *mBio* 2017;8(2):e00356-17 | ✅ |
| 30345391 | Jolley, *Wellcome Open Res* 2018;3:124 | ✅ |
| 32895707 | Duchêne (BETS), *Mol Biol Evol* 2020;37:3363 | ✅ |
| 33536328 | Gee, *mSphere* 2021;6(1):e01259-20 (Ceará) | ✅ |
| 33980649 | **Lichtenegger**, *J Clin Microbiol* 2021;59(8):e0009321 | ✅ 4,221 targets, matches our scheme |
| 34752446 | Blackwell, *PLoS Biol* 2021;19(11):e3001421 | ✅ the 661,405-genome paper |
| 38972886 | Seng, *Nat Commun* 2024;15:5699 | ✅ |
| 40835221 | **Brennan**, *Emerg Infect Dis* 2025;31(9):1802–1806 | ✅ (first author was wrong — see §3) |
| 41401143 | Yu, *PLoS Biol* 2025;23:e3003539 | ✅ |

## 2. Previously unresolved — now resolved and verified (6)

The outline listed these as "verify before citing" or "PMID missing". All six are
now pinned:

| citation | **PMID** | verified title |
|---|---|---|
| De Smet, *J Clin Microbiol* 2015;53(1):323-6 | **25392354** | "…MLST types common to both Cambodia and Australia are due to homoplasy" |
| McLaughlin, *PLoS Negl Trop Dis* 2022;16(4):e0009882 | **35417451** | "In silico analyses of penicillin binding proteins…" |
| Petras, *N Engl J Med* 2023;389(25):2355–2362 | **38118023** | "Locally Acquired Melioidosis Linked to Environment — Mississippi, 2020-2023" |
| Gee, *Emerg Infect Dis* 2017;23(7):1133–1138 | **28628442** | "Phylogeography of *Burkholderia pseudomallei* Isolates, Western Hemisphere" |
| Didelot & Parkhill, *Phil Trans R Soc B* 2022;377:20210246 | **35989600** | "A scalable analytical approach from bacterial genomes to epidemiology" |
| Wilson, *PLoS Genet* 2008;4(9):e1000203 | **18818764** | "Tracing the source of campylobacteriosis" |

### 2.1 Two of them say more than the corpus records

**Gee 2017 (PMID 28628442) contains a direct precedent for the Georgia case, and
the corpus does not mention it.** Its abstract reports: *one isolate associated
with a former **World War II prisoner of war**, believed to represent illness
**62 years after exposure in Southeast Asia**, was shown by analysis to have
**originated in Central or South America** instead.*

That is the reactivation-versus-local-acquisition question decided by genomics,
in the same organism, by the same group — and it is decided **against** the
long-latency-import explanation. It directly supports the reasoning in
`VIETNAM_GEORGIA_RESULT_2026-08-23.md` and should be cited there and in R7.

**De Smet 2015 is more supportive than the corpus frames it.** The outline uses
it for "eBURST is unreliable for inferring the geographic origin of STs". True —
but the abstract also states whole-genome analysis **"correctly identified the
Asian or Australian origin"**. That is an independent published instance of
*continental*-scale attribution succeeding where ST-level attribution fails —
i.e. the depth-ceiling result, in another lab's data. Cite it for both halves.

## 3. Corrections already made this session

| was | is | how found |
|---|---|---|
| "Ashcroft 2021" as a distinct 4,221-target scheme | **phantom** — resolves to Lichtenegger | earlier session |
| "Brennan **T**, … *EID* 2025", partial title | **Brennan S** (Skyler); full title and page range | fetched record |
| §6.5 instruction to *remove* the Lichtenegger citation | **inverted** — it is the headline scheme | fetched record |

## 4. Unresolved, and to be treated as unciteable until resolved

- **"Pearson 2020"** — the outline records two conflicting PMIDs in project
  documents, and one of them was previously found to be a materials-chemistry
  paper about formic acid on ceramics. Targeted PubMed searches for a Pearson
  *B. pseudomallei* phylogeography paper returned **nothing**. **Do not cite
  "Pearson 2020" in any form until someone produces the actual reference.**
  (Pearson **2009**, *BMC Biology*, is a separate and correct citation.)
- **The eLife Salmonella accessory-unitig paper** (the "macro F1 0.661" figure in
  our notes) — **still not found.** Multiple searches failed. The 0.661 figure
  should not be quoted until the source is identified. See §5 for what the search
  *did* turn up in its place.
- **Sprenger 2026** (`doi:10.1128/spectrum.02926-25`) and the Mississippi ST in
  Petras 2023 — not resolvable from abstracts; need full text.

## 5. The literature pass §6.6 said had never been done

Accessory-genome and tree-free source attribution. Two directly relevant papers,
both verified, neither previously in the corpus.

### 5.1 ⚠ DeepSANet — a 2025 paper reporting 80.8% COUNTRY attribution

> **Liang S, Mei S, Ji J, *et al.* "DeepSANet: A deep learning approach for
> hierarchical geographical source attribution of *Salmonella*." *Food Res Int*
> 2025;221(Pt 4):117554.** PMID **41185308**,
> [doi:10.1016/j.foodres.2025.117554](https://doi.org/10.1016/j.foodres.2025.117554)

Reports hierarchical geographic attribution of *Salmonella* at **91.88% (region),
87.05% (subregion) and 80.83% (country)**, and >90% at all levels on an
EnteroBase-derived set — **using only 3,002 cgMLST loci as features**.

**This is the single most dangerous paper for our manuscript and it must be
addressed in the Discussion, not omitted.** It is the same feature type (cgMLST),
a comparable locus count (3,002 vs our 4,221), and it claims success at exactly
the scale we report as unreachable.

**Three substantive distinctions, in order of strength — each testable, none
rhetorical:**

1. **Holdout design is the decisive question, and the abstract does not state
   one.** Our country result depends entirely on it: under leave-**one**-out our
   own estimator reaches 29–37% at country scale, and *every one of those hits is
   a validation genome predicting another of the same country*. Under
   leave-**group**-out it collapses. **Yu 2025 (PMID 41401143), already cited,
   argues precisely this** — that biased sampling driven by population structure
   confounds ML on bacterial genomes, and recommends phylogeny-aware
   cross-validation on held-out clades. If DeepSANet uses random splits, its
   country figure measures population structure plus sampling, not attribution.
   **Read the methods before writing the rebuttal sentence.**
2. **Organism.** *B. pseudomallei* is environmental, highly recombinogenic
   (in-window r/m 7.70) and carries lineages that genuinely span continents — ST92
   across seven Americas countries, and the Viet Nam/Georgia lineage where a US
   autochthonous cluster and a Viet Nam-acquired case sit **one locus** apart.
   *S. enterica* Enteritidis is comparatively clonal and geographically
   structured. A method can succeed on one and fail on the other without either
   result being wrong.
3. **Reference density.** EnteroBase holds hundreds of thousands of *Salmonella*
   genomes; the entire public *B. pseudomallei* record is 9,040 BioSamples, of
   which **7 of our 16 validation source countries have zero**. Our central claim
   is that attribution reaches exactly as far as the reference panel — which
   predicts that a densely-referenced organism *should* attribute better.
   **DeepSANet is therefore consistent with our thesis rather than a refutation
   of it**, and framing it that way is stronger than treating it as a rival.

### 5.2 Munck 2020 — cgMLST + ML source attribution, but to reservoirs

> **Munck N, Njage PMK, Leekitcharoenphon P, Litrup E, Hald T. "Application of
> Whole-Genome Sequences and Machine Learning in Source Attribution of
> *Salmonella* Typhimurium." *Risk Anal* 2020;40(9):1693–1705.** PMID
> **32515055**, [doi:10.1111/risa.13510](https://doi.org/10.1111/risa.13510)

cgMLST features, logit boost, **0.933 accuracy** — but attributing to **animal
reservoir** (pigs, broilers, cattle, ducks, layers) within Denmark, a 5-class
problem in one country. Cite as the methodological precedent for cgMLST-based
attribution while noting the task is not geographic and the class count is small.

### 5.3 What the search establishes for the novelty claim

§6.3 ranks "resolution-invariance across 584-fold" as the weakest-evidenced
novelty claim, with no documented search behind it. **That search has now been
run** and returned only the two papers above plus Wilson 2008. Neither tests
resolution invariance. The claim can stand as *"we are not aware of"* with a
documented search behind it — but it must be written as a searched claim, and the
search terms recorded.

## 6. Actions

1. **Add DeepSANet (PMID 41185308) to §6.2** as the contradicting result, with
   the three distinctions above. **Read its methods for the holdout design before
   drafting the rebuttal** — that is the load-bearing point.
2. **Add Munck 2020 (PMID 32515055)** as the cgMLST-ML precedent.
3. **Cite Gee 2017's WWII POW case** in R7 and in `VIETNAM_GEORGIA_RESULT` — it
   is the published precedent for genomics overturning a long-latency-import
   assumption.
4. **Cite De Smet 2015 for both halves** — ST-level attribution fails, continental
   attribution succeeds.
5. **Insert the six newly-resolved PMIDs** into the outline's §6.2 table.
6. **Strike "Pearson 2020"** from the corpus until a real reference exists, and
   **stop quoting the 0.661 macro-F1** until its source is found.
