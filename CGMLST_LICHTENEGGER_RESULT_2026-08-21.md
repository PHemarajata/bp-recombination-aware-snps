# cgMLST on the published scheme, expanded panel

**This changes the paper's headline. Country attribution is no longer zero, and
the failure decomposes into three mechanisms rather than one.**

Run 2026-08-21. Scheme: *B. pseudomallei* cgMLST **v1.1, 4,221 loci**, seed
genome K96243, Lichtenegger et al. *J Clin Microbiol* 2021;59:e00093-21, PMID
33980649. Panel 3,033 genomes. Validation 44.
Scripts: `run_cgmlst_lichtenegger.sh`, `score_cgmlst_lichtenegger.py`.
Data: `cgmlst_lichtenegger/results/`, `CGMLST_LICHT_ATTRIBUTION.tsv`.

---

## 1. The scheme swap was worth doing on its own merits

| | PubMLST scheme 2 (old) | **Lichtenegger v1.1 (new)** |
|---|---|---|
| loci | 4,090 | **4,221** |
| published | **no** ("experimental in development") | **yes**, PMID 33980649 |
| hosted | PubMLST | cgMLST.org + Pathogenwatch |
| seed genome | not stated | **K96243**, the reference we already use |
| AlleleCall wall clock | 181 min | **47m 47s** |
| call rate, median | 95.5% | **96.9%** |
| genomes >= 90% called | 99.1% | **99.2%** |

12,200,529 exact matches, 155,689 inferred new alleles. Faster because Ridom
ships one seed allele per locus rather than a full allele database, so BLAST has
far less to search.

## 2. cgMLST call rate independently flags every known QC problem

Panel median call rate is 96.9%. Every genome this project has ever flagged
falls out at the bottom, without being told to:

| genome | call rate | why it was already known |
|---|---|---|
| `GCA_017356705_2` | **59.8%** | duplicated chromosome II, 10.6 Mb |
| `SRR2896257` | **60.8%** | register-excluded `broken_assembly`, **still in the panel** |
| `GCA_017356725_2` | **64.3%** | duplicated chromosome II |
| `ERR9980356` | **71.7%** | register-excluded, still in the panel |
| `SRR32459564` | **76.8%** | `marginal_core_coverage` (84.2%) |
| `SRR32083527` | **78.8%** | `marginal_core_coverage` (84.4%) |
| `SRR2896271` | **81.5%** | register-excluded, still in the panel |
| `SRR35159552` | **82.2%** | flagged today as `marginal_fragmentation` |
| `SRR28096039` | **84.1%** | excluded ONT genome |
| `SRR28096043` | **89.3%** | excluded ONT genome |

**This settles the live defect in the exclusion register.** `SRR2896257` is the
third-worst genome in a 3,033-genome panel and it sits inside `strain_1_L1_26`,
the largest analysed unit, whose pre-split r/m of 3.10 was reported as a valid
in-window measurement. The register was right; the panel was wrong. Drop the
four register-excluded genomes and re-derive that unit.

It is also an independent validation of the QC framework: a completely separate
method, using different evidence, ranks the same genomes at the bottom.

## 3. Country attribution: 4 / 42, and no longer zero

Leave-group-out, 44 validation genomes, 42 scorable.

| scale | correct | majority baseline | by exposure country |
|---|---|---|---|
| **country** | **4/42 (10%)** | 12/42 (29%) | **1/15 countries fully correct** |
| **region** | **30/42 (71%)** | 20/42 (48%) | 10/15 countries fully correct |

The four country successes are **Thailand 2/4, Australia 1/2, Nigeria 1/1** and
they are exactly what you would predict: Thailand (3,528 public genomes) and
Australia (1,616) are the two most heavily sequenced countries on earth for this
organism.

**Note the accuracy sits below the majority baseline.** Predicting "Philippines"
for every genome would score 12/42. So country attribution is not merely weak, it
is worse than a constant guess.

## 4. The decisive negative: Mexico still fails with 21 references

Mexico went from 4 reference genomes to **21** for this run. It scored **0/4**,
with nearest-neighbour distances of **0.406 to 0.462**, predicting Ecuador three
times and Nicaragua once.

**The 21 Mexican references never became the nearest neighbour.** They are a
different lineage from the Mexican-exposure cases in our validation set.

This is the single most important result of the run, because it bounds the
explanation the paper has been resting on. Absence of same-country references is
**necessary but not sufficient**. Adding references for a country does not buy
attribution if they are not close relatives. That is a genuinely harder and more
interesting claim than "we lack references", and we now have the controlled test
to support it.

## 5. The failures decompose into three mechanisms

**17 of 38 country failures have a genuinely close relative (d < 0.05) that
simply carries a different country label.** They are not one phenomenon:

### (a) A DUPLICATE LEAK, not a labeling error, n=6 (+2 uncertain)

⚠ **Revised by `BIOPROJECT_AUDIT_2026-08-21.md`.** The India cases are worse and
simpler than stated below: `GCF_030010175_1_USA_Georgia` and the held-out
`SRR17029022` are **the same BioSample** (`SAMN23424236`, the aromatherapy bottle
isolate). One copy is held out as India, the other stays in the pool as USA. The
Indian genomes were matching their own outbreak isolate. **The India row is
invalid until this is dropped and attribution re-run.**
The Viet Nam pair is downgraded to a hypothesis: their neighbours are genuine
`USA: GA` deposits with no stated travel.

| exposure | predicted | d | nearest neighbour |
|---|---|---|---|
| India x5 | USA | **0.007 to 0.009** | `GCF_030010175_1_USA_Georgia` |
| India x1 | USA | 0.023 | `SRR35159552` |
| Viet Nam x2 | USA | **0.009, 0.014** | `SRR31608437`, `SRR31608438` |

`GCF_030010175_1_USA_Georgia` is in **`PRJNA763213`, the 2021 aromatherapy
outbreak** -- the same BioProject as `SRR17029022`, the aromatherapy bottle
isolate. Its true exposure is India. It is **not flagged** `travel_reattributed`,
so leave-group-out does not hold it out, and it wins the nearest-neighbour
comparison for every Indian case.

`SRR31608437/438` are in **`PRJNA908850`**, the CDC project that supplied the two
"USA: CA ex Vietnam" genomes. **8 of its 10 panel members are unflagged.**

**The leave-group-out design is leaking.** This is the same class of error as the
26 -> 31 validation correction: exposures present in the data but never flagged.

**Correcting it will not make these succeed.** Flagging them removes the close
neighbour and forces a more distant prediction, which will probably still be
wrong. What changes is the stated *mechanism* of failure, and that matters,
because right now the paper would attribute to "no signal" a failure that is
actually "the panel's labels are diagnosis countries, not exposure countries."

### (b) Genuine cross-country lineage sharing, n=7, not fixable

Philippines to China at **d = 0.010 to 0.043**, seven times. These are real
Chinese deposits. ST58 spans China, Thailand and the Philippines, so a Philippine
case genuinely has Chinese near-relatives. This is the biology, and it is the
result the paper should lead with.

### (c) No close relative at all, n=13

Mexico, Aruba, Costa Rica, El Salvador, Nicaragua and Ghana at **d = 0.23 to
0.60**. Nothing in the panel is a relative. Not fixable by relabelling; needs
sequencing, and per §4, needs sequencing of the *right* lineage.

## 6. Region fell from 92% to 71%, and that is the fair number

The earlier 92% was scored on 24 genomes dominated by countries with no
references. The expanded set is harder and the number is more honest.

The 12 region failures: **India 0/6** (predicted North America, via the
mislabelled aromatherapy genome in 5(a)), **Viet Nam 0/2** (same cause),
**Guatemala 0/2** (a single Czech genome for all of Europe & Central Asia),
**Ghana 0/1**, **Thailand 1/4**.

So **8 of 12 region failures share a single cause with 5(a)**: unflagged
travel-associated genomes in the reference pool. Fix the flags and the region
number moves materially. It should be re-run before anything is quoted.

Distance stratification, the check from the outline's W2:

| stratum | correct |
|---|---|
| d < 0.05, close relative exists | 10/18 |
| 0.05 to 0.30 | 6/8 |
| d >= 0.30, no real relative | **14/16** |

The "no real relative" stratum still scores highest. The Ecuador-attractor
effect persists: genomes with no true relative snap to the same distant Americas
cluster, which is right for Latin American cases and wrong for African ones.
**A correct region call at d = 0.46 is not evidence of attribution.**

## 7. What this does to the paper

The clean negative is gone. What replaces it is better:

> Country-level attribution succeeds only for the two most heavily sequenced
> countries on earth, fails below a constant-guess baseline overall, and fails
> even where same-country references exist but belong to a different lineage.
> Where it appears to fail for lack of references, a substantial share is instead
> a metadata artifact: reference panels label isolates by country of diagnosis,
> and travel-associated cases are therefore labelled wrongly for this purpose.

That is three findings instead of one, and each is separately defensible.

## 8. Before anything here is quoted

1. **Audit `PRJNA763213` and `PRJNA908850` for unflagged exposures** and re-run.
   This is the highest-value fix and it affects both scales.
2. **Drop the four register-excluded genomes** and re-derive `strain_1_L1_26`.
3. **Run the PubMLST-vs-Lichtenegger concordance** so the scheme swap becomes a
   robustness result. Both profile sets now exist.
4. Re-check whether more of the 27 deposit-only additions are travel cases.
