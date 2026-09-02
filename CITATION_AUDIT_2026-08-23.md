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
- ~~The eLife Salmonella accessory-unitig paper~~ — ✅ **FOUND**: Bayliss *et al.*
  *eLife* 2023;12:e84167, PMID **37042517**. The 0.661 figure is confirmed
  verbatim. See §5.1.
- **Sprenger 2026** (`doi:10.1128/spectrum.02926-25`) and the Mississippi ST in
  Petras 2023 — not resolvable from abstracts; need full text.

## 5. The literature pass §6.6 said had never been done

Accessory-genome and tree-free source attribution. Two directly relevant papers,
both verified, neither previously in the corpus.

### 5.1 ✅ The "bare URL" eLife paper is FOUND — and it is the 0.661 source

> **Bayliss SC, Locke RK, Jenkins C, Chattaway MA, Dallman TJ, Cowley LA. "Rapid
> geographical source attribution of *Salmonella enterica* serovar Enteritidis
> genomes using hierarchical machine learning." *eLife* 2023;12:e84167.**
> PMID **37042517**, PMC10147375,
> [doi:10.7554/eLife.84167](https://doi.org/10.7554/eLife.84167)

**This is the paper our notes carried as a bare URL with no author, year or
title, and it is the source of the "macro F1 0.661" figure** — confirmed verbatim
in its abstract. It is open access, so its full methods are readable.

- 2,313 *S.* Enteritidis genomes, UKHSA 2014–2019
- 4 continents, 11 sub-regions, **38 countries (53 classes)**
- features are **unitigs** (426,647 → 94,865 patterns → 25,000 selected), i.e.
  accessory/pan-genome k-mers — so this *is* the accessory-attribution precedent
  §6.6 was looking for
- **macro F1: continental 0.954, sub-regional 0.718, country 0.661**

### 5.2 ⚠ The holdout design, checked — and it is a random split

**This was the load-bearing question, and it is now answered from the source.**
The eLife methods state:

> *"The dataset was split into **75–25% train-test ratio stratified by the
> country** for downstream applications."*

and for model selection:

> *"…**stratified threefold cross-validation** of the input database…"*

**That is a random, class-stratified split. It is not phylogeny-aware, not
leave-one-clade-out, and not leave-group-out.** Near-identical genomes from the
same lineage, outbreak or submitting laboratory can therefore appear in both
training and test sets.

**This is exactly the design whose collapse we report.** Our own country
attribution reaches **29–37% under leave-one-out** and every hit is a validation
genome predicting another of the same country; under leave-group-out it falls
below baseline. Yu *et al.* 2025 (PMID 41401143, already cited) argues precisely
this for bacterial genomes and recommends phylogeny-aware cross-validation on
held-out clades.

The authors were partly alert to it — they state *"Sample redundancy between
validation and training datasets was removed before comparison"* — but exact
redundancy removal is not the same as removing same-source relatives, and they
report of one outbreak validation that *"six samples … were present in the
training dataset."*

### 5.2.1 Their own results reproduce our depth ceiling

The decisive point for the Discussion is not that they are wrong. It is that
**their own numbers show the same monotonic decay with geographic depth that we
report**:

| level | eLife macro F1 | our κ (modal k=20) |
|---|---|---|
| continental / Asia-vs-not | **0.954** | **1.000** |
| sub-regional / 7-way region | 0.718 | 0.832 |
| **country** | **0.661** | **0.193** |

And their discussion attributes the country-level shortfall to exactly the
mechanism we identify: *"a correlation between a lack of training data and lower
prediction accuracy"* — reference availability setting the ceiling. Their US
samples were *"consistently misclassified"*, and France and Italy scored
hF1 ≈ 0.3.

**So the honest framing is: two organisms, the same shape of result, different
positions on the same curve.** *S.* Enteritidis has dense, geographically
structured, well-referenced sampling and so retains usable country signal;
*B. pseudomallei* is recombinogenic, environmentally acquired, with
continent-spanning lineages and 7 of our 16 source countries at zero public
genomes, and so does not.

### 5.2.2 ✅ DeepSANet's evaluation, read from the authors' own code

The PDF is paywalled, but the authors publish the official implementation at
**`github.com/ShaanLiang/DeepSANet`**, and the evaluation design is legible
there. **This is stronger evidence than the paper's prose would have been.**

**First, the dataset link is now verified rather than inferred.**
`utils/dataset.py` defines `UKHSADataSetInfo` with **4 regions, 11 subregions and
38 countries**, and the country list is the UKHSA travel-associated set. That is
**exactly Bayliss 2023's "four continents, 11 sub-regions, and 38 countries"**.
DeepSANet is benchmarked on the Bayliss dataset.

**Second — and this is the finding — there is no held-out test set in the
released configuration.**

`configs/deepsanet_ukhsa.yaml`:
```yaml
TRAIN_PATH: "data/ukhsa/train"
VAL_PATH:   "data/ukhsa/val"
TEST_PATH:  "data/ukhsa/val"      # ← identical to VAL_PATH
MAX_EPOCH:  300
```
`configs/deepsanet_enterobase.yaml` does the same
(`TEST_PATH: "data/enterobase/val_s10f_0.pt"` = `VAL_PATH`; the `s10f_0` naming
indicates stratified 10-fold, fold 0).

And `trainval.py` selects the reported checkpoint **by maximising accuracy on
that same val set**, over 300 epochs:

```python
if acc_mean_val > best_acc_mean_val:          # line 206
    best_acc_mean_val = acc_mean_val
    best_acc_h1_val, best_acc_h2_val, best_acc_h3_val = ...
    torch.save(model.state_dict(), ".../best.pt")
```

then prints *"three-level acc when best val acc (mean)"* — the
region/subregion/country triple at the arg-max epoch. `test.py` loads
`best.pt` (line 81) and evaluates it on `TEST_PATH` — the same val set.

> **So the headline 91.88 / 87.05 / 80.83 are, in the released configuration, the
> maximum over 300 epochs of accuracy measured on the very set they are reported
> on.** That is selection on the evaluation set, and it inflates the numbers
> before any question of population structure arises.

**Two biases therefore stack, and they are independent:**

1. **Selection-on-test** (above) — optimistic for any dataset, any organism.
2. **A random, class-stratified split** — inherited from the Bayliss benchmark
   (75:25 stratified by country) and echoed by `s10f_0`. Not phylogeny-aware, so
   near-identical genomes of one lineage or outbreak can fall on both sides.

Plus the metric point from §5.2.1: these are **accuracies**, not macro F1.

⚠ **Two fairness caveats, and state both.** The README says *"This repository
currently includes the core components of our paper. Additional code will be
released once the paper is accepted"*, so the released configs may not be exactly
what produced the published numbers. And we have not read the paper's own methods
text. **Write this as "in the released reference implementation", not as "the
authors evaluated on their training set".** The claim is about verifiable code,
and should be phrased so it stays true even if the manuscript describes something
different.

**Net effect on our Discussion: the DeepSANet comparison is no longer a threat
that needs neutralising.** Lead with Bayliss — whose split is documented, whose
depth decay reproduces ours, and whose own discussion blames reference
availability. Cite DeepSANet as a subsequent architecture result on the same
benchmark, note the metric difference, and note that its released implementation
reports on the model-selection set. That is a factual, checkable, non-hostile
sentence, and it is the strongest available.

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
