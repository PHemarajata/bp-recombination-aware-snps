# Attribution scoring and filtered distances — findings

Written 2026-08-20, Tier 1 of the tiered plan. Everything below was computed
locally from files already on disk; no pipeline was re-run.

New scripts: `attribution_score_bp.py`, `recomb_filtered_distances_bp.py`.
Modified: `phylogeography_association_bp.py`, `build_v4c_panel.py`.
New outputs: `ATTRIBUTION_SCORES.tsv`, `ATTRIBUTION_SUMMARY.tsv`,
`DISTANCES_v4c_SUMMARY.tsv`, `DISTANCES_v4c/` (344 matrices).

---

## 1. Headline: attribution works at region scale and fails at country scale

> **REVISED 2026-08-21 — validation set corrected from 26 to 31.** Five genomes
> with a known exposure country were not flagged `travel_reattributed` and were
> therefore invisible to the scorer: three carrying the `_ex_` naming convention
> (Trinidad and Tobago, Martinique, Costa Rica) and two CDC genomes recorded in
> ENA as "USA: CA ex Vietnam". A 19% undercount, and the only Vietnamese
> exposures in the collection. Fixed via
> `build_v4c_panel.py --fix-exposure-flags` plus `EXPOSURE_OVERRIDES.tsv`.
> **All numbers below are the corrected ones.** The conclusions are unchanged
> and now rest on more genomes.

Scored against the 31 genomes with a known exposure country
(`origin_basis == 'travel_reattributed'`). Accuracy is meaningless without the
no-information baseline, because East Asia & Pacific dominates the panel, so
both are reported.

| scale | regime | scorable | modal | nearest-neighbour | enrichment | majority baseline |
|---|---|---|---|---|---|---|
| country | leave-one-out | 24 | 0% | **29%** | 0% | 0% |
| country | leave-group-out | 24 | 0% | **0%** | 0% | 0% |
| **sub-national** | leave-one-out | **5** | 0% | 0% | 0% | 0% |
| **sub-national** | leave-group-out | **5** | **0%** | **0%** | **0%** | 0% |
| region | leave-one-out | 24 | 92% | 75% | 92% | 54% |
| region | leave-group-out | 24 | **92%** | 67% | **92%** | **54%** |

**Region-scale attribution is real signal**: 92% against a 54% baseline, and it
does not degrade under leave-group-out. **Country-scale attribution is zero**
under every estimator once circularity is removed.

**Sub-national is now testable and also fails.** It was previously reported as
untestable because no validation genome carried a sub-national label; the five
newly flagged genomes do, and all five are wrong under both regimes. A small
denominator, but it closes what had been an open gap.

**The corrected numbers are slightly lower and considerably more trustworthy.**
Region fell from 100% to 92% because the added genomes include harder cases —
and 24 scorable is a better footing than 19.

### The 37% is entirely circularity, and it is now counted

All 7 leave-one-out country hits are same-country *validation* genomes
predicting each other — Guatemala ×2, Aruba ×2, Philippines ×3. Leave-group-out
removes them and accuracy goes to 0/19. The `same_truth_refs_in_pool` column
makes this auditable per row: 16 of 19 scorable rows retain a same-country
reference under leave-one-out, 3 under leave-group-out.

**This is why any accuracy quoted with the validation genomes left in is not
just optimistic but wholly artefactual.**

### It is not only panel composition

Three Mexico genomes kept a *genuine* same-country reference under
leave-group-out — 3 Mexican genomes in a 30-genome pool — and attribution still
failed (modal → Puerto Rico, NN → USA / Martinique). So the country-scale
failure is not merely "the Philippines has no reference genomes". Inside
`strain_4_L1_4`, exposure country is not recoverable even when same-country
references are present at 10% of the unit. That is consistent with the
association test, which returns **confounded** for that unit.

### Sub-national is untestable, not failed

All 26 validation genomes have a blank sub-national label — `build_v4c_panel.py`
sets `subregion="unknown"` for the new batch. No sub-national claim can be
supported or refuted on this validation set.

### The countries most needing attribution are least likely to be analysable

6 of 26 validation genomes are unattributable because they sit in `n=1`
`assign_only` units below the analysis floor: Ghana, Nigeria, El Salvador, one
Philippines, one Mexico, and the `ex_Africa` genome. **Four are the sole panel
representative of their exposure country.** Under-sampled source countries land
in units too small to analyse — a structural bias against exactly the cases the
method exists to serve.

A seventh, the `Panama and Peru` genome, is correctly excluded as multi-country.

---

## 2. Raw vs recombination-filtered distances

`DISTANCES_v4c_SUMMARY.tsv`, 172 replicon-units, plus per-unit matrices.
Computed from `.core.tab` + the Gubbins GFF rather than by masking alignments —
370 KB against 94 MB per unit, so the whole set runs in 11 seconds and touches
no disk. The three coordinate spaces were verified to coincide.

Two filtered distances are reported, because Gubbins masks per branch:
**per-taxon** (a site is dropped for a pair only if one of that pair's taxa was
called recombinant) and **global** (any site recombinant on ≥1 branch dropped
for everybody).

### It validates independently against r/m

A pair's distance loses the SNPs recombination brought in, so filtered/raw
should track `1/(1+r/m)`. It does — **rank correlation +0.750** across the 86
units. Two computations from different files agreeing this closely is good
evidence both are right.

Observed sits ~1.75× below predicted (median 0.090 vs 0.158) because per-taxon
masking drops a site when *either* member of a pair is masked, which is more
aggressive than r/m's per-branch accounting. Expected, not a defect.

**The residual is the useful diagnostic, not the raw ratio.** A threshold on
filtered/raw alone flags 136 of 172 replicon-units — i.e. the normal state.
`ratio_over_expected` separates two real regimes: >1 means recombination is
concentrated on few branches and most pairs are spared (`strain_21_L1_1`, 6.8×);
<1 means masking hits most pairs harder than the branch count implies
(`strain_1_L1_5`, 0.17×).

### Scale of masking

Median masked fraction is **46.8%**, maximum **99.5%** (`strain_2_L1_6`, n=159 —
essentially the whole replicon called recombinant on at least one branch). This
is the size-confounded union-coverage effect showing up directly: the largest
unit has near-total union coverage.

---

## 3. The Mississippi unit

`strain_4_L1_1`, n=22 — **21 USA/Mississippi plus one Colombian genome**
(`SRR11974618`, Santander).

| | raw | filtered |
|---|---|---|
| Mississippi internal (median, range) | 7 (0–19) | 5 (0–15) |
| Colombia → Mississippi (median) | **1,128** | **486** |

Two things follow.

**The Gulf Coast cluster is clonal at outbreak resolution.** 21 genomes within
0–19 raw SNPs. That gives a clean operational rule for a new US case: inside
this cluster at <20 SNPs is the Gulf Coast lineage; 500+ SNPs away is not.

**The unit's r/m of 1.2522 is not contamination.** The mixed sample
`SRR30648681` that contaminated the *v4b* Mississippi unit is gone from v4c —
verified absent from both the metadata and the partition.

### Tested: should the unit be split on the Colombian genome? No.

An r/m of 1–2 is the "bridged/mixed unit" band, whose prescribed remedy is to
subdivide — the catalogue's worked example recovers 2.57 → 4.94. We tested it
directly by re-running Gubbins on the 21 Mississippi genomes alone, same
parameters (`iterations=5, raxml, min_snps=3, filter_percentage=25.0`), seeded,
both replicons. The correction reproduces the published 1.2522 exactly, so the
comparison is on the right scale.

| | inside | outside | pooled r/m |
|---|---|---|---|
| current unit, n=22 with Colombia | 2,160 | 1,725 | **1.2522** |
| re-run, n=21 without Colombia | 452 | 441 | **1.0249** (0.82×) |

**Splitting makes it worse**, the opposite of the bridged-unit prediction. So
this is not a bridged unit.

The mechanism is in the totals: removing one genome removes **77% of the usable
SNPs** (3,885 → 893). The Colombian genome, outlier though it is, was supplying
most of the substitution signal Gubbins had to work with. What remains is 21
genomes at a median of 5–7 pairwise SNPs — almost nothing to partition into
"recombinant" versus "clonal".

**Diagnosis: genuine under-detection at the low-diversity extreme.** All three
markers collapse together, which the catalogue calls a reliable joint signature —
r/m 1.25, union coverage 7.2% / 9.7%, and a median tract of **694 bp**, short
against the kilobase-scale tracts expected for this species.

**Consequence.** This unit is **below the analysable range for recombination**,
and no partitioning fixes that. But that is a statement about one analysis, not
about the unit: it remains excellent for the outbreak-style question, where its
tightness is the whole point. Report it as a clonal cluster with pairwise SNP
distances; **do not quote r/m, union coverage or tract length for it at all.**

Over half the Colombia–Mississippi divergence (1,128 → 486) is imported
sequence. But 486 filtered SNPs is far outside outbreak range, so this genome is
the nearest relative *in this panel* rather than a near relative — a statement
about panel sparsity in the Americas, not about the introduction route.

---

## 4. Reproducibility repairs

**BH-FDR and the vacuous-control gate are now scripted.** Both were applied by
hand and existed only as prose; nothing in the repo reproduced either. The
scripted versions reproduce the hand-computed numbers exactly:

| scale | testable | surviving BH 5% | geographic (control passes) |
|---|---|---|---|
| national | 49 | **24** | **6** |
| sub-national | 83 | **11** | **0** |
| regional | 16 | **3** | **1** |

matching `PHYLOGEOGRAPHY_ASSOCIATION_INTERPRETATION.md` (26→24→6, →11→0, 4→3→1).
New columns: `q_value`, `control_status`, `interpretation`. The national
breakdown is 39 untestable, 25 null, 13 confounded, 6 geographic, 5 vacuous.

**Unit labels in the metadata were badly stale.** `strain`, `subcluster`,
`unit_n`, `unit_rm`, `reference`, `ref_source`, `ref_mean_mash` were inherited
verbatim from v4b and never recomputed: 694 rows blank and **65.8% of populated
`subcluster` values disagreed** with the v4c partition — 2,197 of 2,976 rows
wrong or missing. Repaired via a new `build_v4c_panel.py --relabel-units` mode;
all 2,352 analysed genomes now resolve consistently. The published association
results were **not** affected, because that script derives units from tree tips.

**Exclusion register promoted** to the 46-row copy (root had 42, missing
`ERR9980356`, `SRR2896257`, `SRR2896259`, `SRR2896271`) and normalised to LF —
it was CRLF, the class of defect that has silently killed runs here.

**Compound country handled.** `Panama and Peru` was being scored as its own
Fitch state. Now treated as missing at country scale, keyed on
`origin_resolution == "multi_country"` rather than string-matching, since
"Trinidad and Tobago" is one country. Effect is surgical: exactly one row
changed (`strain_4_L1_3`, n_known 39→38, distinct 7→6), no p-value moved.

---

## 5. What this means for the write-up

1. **Claim regional attribution, not country attribution.** 100% vs a 58%
   baseline at region scale; zero at country scale under honest holdout.
2. **Never quote leave-one-out country accuracy.** It is 37% and all of it is
   circularity.
3. **Report the analysability bias.** Four of six unattributable genomes are the
   only panel representative of their exposure country.
4. **The draw-probability test stays unimplemented** — see the Methods note.

---

## 6. Already on disk and under-used: the two tools disagree about the gate

> **UPDATE 2026-08-21 — the ν explanation below has been TESTED AND REFUTED.**
> See `NU_HYPOTHESIS_RESULT_2026-08-21.md`. On 81 v4c replicon-units, ν vs
> Gubbins r/m is **negative** (rho −0.42 / −0.49), the opposite of the
> prediction, and Gubbins-rejected units have no distinctive ν (p = 0.22 / 0.17).
> ν and δ are anti-correlated at rho −0.81 / −0.86, so ν is not independently
> interpretable — the apparent signal was δ. The residue remains unexplained,
> with a seventh candidate now excluded. The text below is kept as the record of
> what was predicted.

`clonalframe_nu_bp.py` is not a stub — it is a 620-line driver that has **already
been run on 46 units**, and it independently articulates the ν-decomposition
argument (r/m ≈ (R/θ) × δ × ν, so a low r/m can mean rare recombination, short
tracts, *or* donors so close the imports are invisible). Six candidate
explanations for the depressed-r/m residue were tested and refuted before it.

`TIER1_3_clonalframe_all.txt` contains the all-units comparison that the earlier
six-unit report said was needed, and it is a stronger result than the flag it was
raised as:

- Spearman rho (Gubbins r/m vs ClonalFrameML implied r/m) = **+0.297**, p = 0.045, n = 46
- CFML/Gubbins ratio median 2.3×, range 1.1–349.5×
- Taking the top 30 units under each tool, **22 of 30 overlap — 8 units change
  accept/reject verdict depending on which tool estimates r/m**

**Pooled r/m is the sole acceptance gate.** If this holds, the gate is
tool-dependent for roughly 17% of units. That is a finding about the method, not
about those units.

**Caveat that keeps it from being conclusive:** those 46 units come from the
older s-prefix partition, with different names and membership from v4c. The
result does not transfer automatically. Re-running it on v4c is now
possible — `clonalframe_nu_bp.py --layout v4c` was added and resolves all 86
units — and is the priority job in `A100_RUNBOOK_YUYI.md`.

---

## 7. Open items

- **ClonalFrameML on the v4c units** — the highest-value open question; runbook
  written, awaiting A100 time.
- cgMLST orthogonal layer (Tier 2, GCP) — not started, needs spend go-ahead.
- `strain_1_L1_36` / `strain_1_L1_37` exist only in the A100 run, so the distance
  table covers **86 of 88 units**. Gap-fill is Job 2 of the runbook.
- Whether `strain_4_L1_1` should be split on the Colombia genome before its r/m
  is quoted anywhere.
- Sub-national attribution cannot be tested until validation genomes acquire
  sub-national labels.
