# Genome register — the single source of truth

**Created 2026-08-21.** Every number here was computed today from primary data,
not copied from another document. Where it disagrees with an older document,
**this file is correct and the older document is superseded.**

Purpose: after dozens of sessions of adding and removing genomes, this is the one
place that says what is in the panel, what is ground truth, what is incoming, and
what is excluded — with the arithmetic shown.

---

## 1. Headline corrections to previously circulated numbers

| claim in circulation | where from | status |
|---|---|---|
| "9 of **16** validation source countries have zero public genomes" | `SAMPLING_FRAME_2026-08-21.md` §3 | **Both halves wrong.** There are **15** real source countries after the incoming batch (12 before it), and **7** have zero. See §4 |
| "Mexico 0/8 public genomes" | same | **Wrong. Mexico has 21** public genomes in ENA |
| "Philippines 0 public genomes" | same | **Wrong. Philippines has 1** |
| "panel is 44% of country-labelled ENA BioSamples" | same | Right on a reads-only denominator; **41.4%** on the correct one |
| "29 countries ≥100 cases/yr have zero genomes = 33% of global burden" | `GAP4` | **Wrong, on a superseded census.** Correct: **21 countries, 5%.** See §5 |
| "cgMLST scheme = Ashcroft 2021 **or** Lichtenegger 2021" (cited as two schemes) | `LITERATURE_POSITIONING`, `GAP1`, `GAP2` | **They are the same paper — "Ashcroft" is a phantom.** And we used *neither*: we ran an unpublished PubMLST scheme. See §7 |

### The single root cause of the first four

**`SAMPLING_FRAME`'s ENA census queried `result=read_run` only.** Groups that
deposit an assembly without submitting raw reads are invisible to that query.
Mexico is the clearest case: **all 21 Mexican genomes are assembly-only** — 16 of
them from one recent BioProject, `PRJNA1131791` (Mexico City, Sonora, Morelos,
Baja California Sur) — and not one appears in a read-run search.

**Any ENA census for this paper must union `result=read_run` with
`result=assembly`.** This is not a rounding difference: it moves the paper's
central claim about Mexico from "no reference genomes exist" to "21 exist."

---

## 2. The ENA census, re-run 2026-08-21

Queries (both needed):

```bash
curl -s "https://www.ebi.ac.uk/ena/portal/api/search?result=read_run&query=tax_eq(28450)&fields=run_accession,sample_accession,study_accession,country,collection_date&format=tsv&limit=0" -o ena_all_runs.tsv
curl -s "https://www.ebi.ac.uk/ena/portal/api/search?result=assembly&query=tax_eq(28450)&fields=accession,sample_accession,study_accession,country&format=tsv&limit=0" -o ena_all_asm.tsv
```

Deduplicate to BioSample; split `country` on `:` and keep the first field.

| | records | unique BioSamples | with a country |
|---|---|---|---|
| read runs | 9,623 | 8,500 | 6,707 |
| assemblies | 3,546 | 3,423 | 3,337 |
| **union** | — | **9,040** | **7,192** |

**56 distinct countries.** Top: Thailand 3,528, Australia 1,616, Cambodia 534,
China 304, India 150, Malaysia 146, Viet Nam 137, USA 118, Singapore 95,
Hong Kong 75, Puerto Rico 61, Laos 48, Taiwan 41, Brazil 37, Bangladesh 32.

*(Read-run figures reproduce `SAMPLING_FRAME` exactly except 6,707 vs 6,695 — 12
BioSamples deposited since that census. The assembly arm is entirely new.)*

---

## 3. The panel as it stands

**2,976 genomes, 50 countries** (`L1v4c_MERGED_METADATA.tsv`).

| provenance | n | % |
|---|---|---|
| GenBank (`GCA_`) | 1,398 | 47.0% |
| RefSeq (`GCF_`) | 1,035 | 34.8% |
| in-house patient (`IP-`) | 259 | 8.7% |
| assembled from public reads | 231 | 7.8% |
| in-house environmental (`IE-`) | 53 | 1.8% |
| **non-public subtotal** | **312** | **10.5%** |

**Coverage of the public universe: 2,976 / 7,192 = 41.4%** of country-labelled
ENA BioSamples. **Quote 41.4%, not 44%** — the 44% used a reads-only
denominator. (Both are slight over-statements, since 312 panel genomes are not
public at all; against the public-derived 2,664 the figure is 37.0%.)

Analysed subsets, which are **not** the panel and must never be conflated:

| set | n | file |
|---|---|---|
| **analysed — REPORTED** | **2,340 in 85 units** | `FINAL_BASIS_2026-08-22/FINAL_PARTITION.tsv` |
| panel, corrected | 2,959 | `PANEL_v4d_2026-08-21.tsv` |
| panel, before deduplication | 2,976 | `L1v4c_MERGED_METADATA.tsv` |
| analysed, A100 (**control**) | 2,342 in 88 units | A100 `curated_L1v4c_refs.final.tsv` |
| intermediate, pre-correction | 2,352 in 86 units | `curated_L1v4c_clusters.tsv` — **not an analysed set** |
| distance / ClonalFrameML tables | 86 of 88 units, 172 of 176 replicon-units | two units are A100-only |

> **⚠ Corrected 2026-08-23.** This table previously labelled the A100 run
> "production" and gave no row for the reported basis. The reported analysis is
> the **85-unit / 2,340-genome workstation run**; the A100 88-unit run is the
> cross-hardware control. `curated_L1v4c_clusters.tsv` (2,352) is a
> pre-correction intermediate that still lists `SRR2896257` — never subtract your
> way from it to the analysed set; read `FINAL_PARTITION.tsv`.

---

## 4. Ground truth: the validation set

**Definition of record: `origin_basis == "travel_reattributed"` in
`L1v4c_MERGED_METADATA.tsv`.** Count today: **31.** Five were added
2026-08-21 via `EXPOSURE_OVERRIDES.tsv` (10 rows, 5 of which land in the
validation set).

Exposure countries, current 31 and after the incoming batch:

| source country | val now | + batch | val after | ENA reads-only | **ENA reads+asm** | status |
|---|---|---|---|---|---|---|
| Philippines | 12 | 0 | 12 | 0 | **1** | **assembly-only** |
| Mexico | 4 | 0 | 4 | 0 | **21** | **assembly-only** |
| Aruba | 2 | 0 | 2 | 0 | **0** | zero |
| Guatemala | 2 | 0 | 2 | 0 | **0** | zero |
| Viet Nam | 2 | 0 | 2 | 83 | 137 | |
| Costa Rica | 1 | 0 | 1 | 0 | **0** | zero |
| El Salvador | 1 | 0 | 1 | 0 | **0** | zero |
| Ghana | 1 | 0 | 1 | 21 | 21 | |
| Martinique | 1 | 0 | 1 | 0 | **0** | zero |
| Nicaragua | 1 | 0 | 1 | 0 | **0** | zero |
| Nigeria | 1 | 0 | 1 | 9 | 9 | |
| Trinidad and Tobago | 1 | 1 | 2 | 0 | **0** | zero |
| **India** | 0 | **6** | **6** | 96 | **150** | *new* |
| **Thailand** | 0 | **4** | **4** | 3,462 | **3,528** | *new* |
| **Australia** | 0 | **2** | **2** | 1,594 | **1,616** | *new* |
| *Africa* (region, not a country) | 1 | 0 | 1 | — | — | not scorable |
| *Panama and Peru* (compound) | 1 | 0 | 1 | — | — | not scorable |
| **TOTAL genomes** | **31** | **13** | **44** | | | |

**Real source countries: 12 now, 15 after the batch** (excluding *Africa* and
*Panama and Peru*, neither of which is a country).

### The corrected headline

> **7 of 15 source countries — Aruba, Costa Rica, El Salvador, Guatemala,
> Martinique, Nicaragua and Trinidad and Tobago — have no public genome in ENA,
> in either reads or assemblies.**

All seven are Latin America & Caribbean. That is a **sharper** finding than the
old one, not a weaker one: the gap is not scattered, it is one region.

**Do not write "9 of 16".** The 9 came from a reads-only query that missed Mexico
and the Philippines; the 16 was never the number of source countries.

### What the incoming batch does to the test

The three new source countries — **India (150 ENA genomes), Thailand (3,528),
Australia (1,616)** — are the best-represented countries in the entire
collection. Until now, country attribution was tested almost exclusively on
countries with zero or near-zero references, which is the most attackable
feature of the negative result. **The batch is what converts it into a fair
test.** Re-run the country-scale scoring the moment those assemblies land.

---

## 5. Zero-genome countries against predicted burden

Burden: Limmathurotsakul et al. 2016, *Nat Microbiol* 1:15008, PMID 26877885,
SI Table 1. Genome counts: the ENA union census in §2.

- **21 countries with ≥100 predicted cases/year have zero public genomes.**
- Their combined burden: **8,939 cases/year = 5% of the 165,000 global estimate.**
- All 54 zero-genome burden countries: 9,981 cases/year = 6%.

**19 of the 21 are sub-Saharan African.** The two exceptions are Nepal (914) and
El Salvador (114).

Guinea 1,372 · Côte d'Ivoire 1,144 · Benin 919 · Nepal 914 · Sierra Leone 600 ·
Cameroon 540 · Liberia 445 · Chad 401 · Niger 368 · Tanzania 307 · Congo Rep. 262 ·
Ethiopia 261 · Mozambique 238 · Congo Dem. Rep. 222 · Malawi 221 · Togo 157 ·
Central African Republic 142 · El Salvador 114 · Zambia 112 · Guinea-Bissau 100 ·
Kenya 100.

### Why this differs so much from the circulating figure

| | `GAP4` (2026-08-09 NCBI census) | v4c panel | **ENA union, today** |
|---|---|---|---|
| countries ≥100 cases/yr, zero genomes | 29 | 24 | **21** |
| their share of global burden | **33%** | 7% | **5%** |

Indonesia, Nigeria, Myanmar, Cambodia, Brazil and Colombia have all acquired
public genomes since the 2026-08-09 census, and they were the largest
contributors to the old 54,076 cases/year total.

**Publishing "33% of global burden" would be a factual error.** The correct
figure is 5%, and the correct framing is that **the residual gap is now
essentially sub-Saharan Africa**, which pairs exactly with the regional table
(sub-Saharan Africa: 14.5% of burden, 1.0% of the panel).

**The regional comparison is the robust one and should lead** — it barely moves
between censuses, whereas these country totals move by 6-fold.

---

## 6. The incoming batch: 43 rows, 40 to assemble

`ENA_TARGETS_CLASSIFIED.tsv`.

| tier | n | use |
|---|---|---|
| A_exposure_stated | 8 | **ground truth** |
| B_external_evidence | 5 | **ground truth** |
| C_deposit_only | 27 | **panel context only — never ground truth** |
| D_unusable | 3 | **exclude** |

**Build the Terra sample set from the 40 non-D rows. 43 − 3 = 40.**

The three D rows are **not** *B. pseudomallei*: `SRR22548210`, `SRR22548211`,
`SRR22548212`, all `tax_id 57975` = ***Burkholderia thailandensis***. They were
caught by a taxon check on a study-level query. Do not assemble them.

The 13 ground-truth additions: **India 6, Thailand 4, Australia 2, Trinidad and
Tobago 1.** The 27 context-only additions are deposited USA 19, Puerto Rico 6,
Thailand 1, Bangladesh 1 — they enlarge the reference panel, and **none of them
may be scored as ground truth**, because a deposit country cannot distinguish
local acquisition from unrecorded travel.

**After assembly: panel 2,976 → 3,016; validation 31 → 44.**

---

## 7. The cgMLST scheme — resolved

Read from the scheme's own PubMLST page and from
`cgmlst_scheme/scheme_meta.json`:

| field | value |
|---|---|
| database | `pubmlst_bpseudomallei_seqdef` |
| scheme id | **2** |
| name | cgMLST — *Burkholderia pseudomallei* typing |
| loci | **4,090** (we called **4,089**) |
| profiles | 1,154 |
| primary key | cgST |
| last updated | 2026-06-18 |
| curator | **Jessica Webb** (University of Adelaide; Menzies School of Health Research, Darwin) |
| **status** | ⚠ **"experimental in development"; "under development and is subject to change"** |
| **scheme publication** | **none** |

### The field standard is a different scheme — and we are not using it

**Lichtenegger S, Trinh TT, Assig K, Prior K, Harmsen D, Pesl J, Zauner A, Lipp
M, Que TA, Mutsam B, Kleinhappl B, Steinmetz I, Wagner GE. *J Clin Microbiol*
2021;59:e00093-21. PMID 33980649. doi:10.1128/JCM.00093-21** — **4,221 core +
1,351 accessory targets**, K96243 challenged with 468 genomes from 30 countries
over 79 years, validated on 320 WGS sets. Hosted free on **cgMLST.org (Ridom)**
and **Pathogenwatch**.

⚠ **"Ashcroft et al. 2021" is a phantom citation.** Our documents cite Ashcroft
and Lichtenegger as two different 4,221-target schemes. **They are the same
paper.** There is exactly one published *B. pseudomallei* cgMLST scheme.

### But this does NOT affect any ST we report

Two separate things, and only one is exposed:

- **7-locus MLST is completely standard.** `mlst 2.23.0`, scheme
  `bpseudomallei` = PubMLST scheme 1, the universal one. **ST92 means the same
  thing to us, to Gee 2017, and to the NEJM Mississippi paper.** Every ST in the
  manuscript — ST92, ST70, ST58, ST297 — is directly comparable to the
  literature. The ST92-spans-seven-countries finding is safe.
- **We never assign or report a cgST.** `cgmlst_analysis_bp.py` computes only
  **normalised allelic distance over co-called loci**; there is no cgST column in
  any output. The scheme is used as a fixed measuring stick, not as a
  nomenclature. So "our cgST would not match anyone else's" is not a defect in
  anything we publish — because we publish no cgST.

**The residual exposure is narrower but real:** our cgMLST *distances* are over a
different locus set from everyone else's, so they are not directly comparable to
published cgMLST distances, and a reviewer in this field will ask why the
published scheme was not used.

### Recommendation: re-run on the Lichtenegger scheme

`AlleleCall` took **181 minutes** for 2,976 genomes. This is a ~3-hour job, and
it removes the objection entirely. **Better: run both and report the
concordance** — that converts a defensive footnote into a robustness result
("the attribution outcome is invariant to the cgMLST scheme"), which is worth
more than either run alone. The original reason for choosing PubMLST — Ridom's
allele definitions may not be redistributable — is a concern about *republishing
the scheme*, not about *using* it, and it does not require us to avoid it.

**Two things the Methods must state**Two things the Methods must state, because the scheme is unstable:**

1. It is flagged experimental and subject to change, so **record the exact
   download: scheme 2, 4,090 loci, 1,154 profiles, retrieved 2026-06-18** (we
   have this) and archive the allele FASTAs alongside the results.
2. Our results are reproducible only against that snapshot. Say so.

This is not a weakness in the analysis — the 4,089 loci behaved well (median
call rate 95.5%, cgMLST-vs-SNP concordance r = +0.861). It is a provenance
statement a reviewer will want.

---

## 7b. Should we add the newly-uncovered genomes?

Public genomes that exist and we do not hold, for **source countries only**:

| source country | val genomes | in ENA | in panel | **addable** | verdict |
|---|---|---|---|---|---|
| **Mexico** | 4 | 21 | 8 | **+13** | **DO THIS** |
| Viet Nam | 2 | 137 | 60 | +77 | worthwhile |
| India | 6 (incoming) | 150 | 56 | +94 | low marginal value |
| Australia | 2 (incoming) | 1,616 | 283 | +1,333 | low for attribution |
| Thailand | 4 (incoming) | 3,528 | 1,753 | +1,775 | **no** — already 59% of panel |
| Ghana | 1 | 21 | 18 | +3 | negligible |
| Nigeria | 1 | 9 | 10 | 0 | — |
| Philippines | 12 | 1 | 12 | 0 | — |
| **Aruba, Costa Rica, El Salvador, Guatemala, Martinique, Nicaragua, Trinidad** | 9 | **0** | 9 | **0** | **nothing exists to add** |

**Mexico is the one that changes a result.** It is the only source country where
adding materially raises reference density *for genomes already in the validation
set*, and it is already the most informative case in the paper: **three Mexican
genomes retained genuine same-country references under leave-group-out and
attribution still failed.** That test currently rests on 3 references in a
30-genome pool. Taking Mexico to 21 makes it properly powered, and the result is
decisive either way:

- **Still fails at 21 references** → the "no references" explanation is bounded,
  and the finding becomes much stronger: country signal is absent even when the
  panel is adequate.
- **Succeeds at 21 references** → the explanation is confirmed, the paper gains a
  positive result, and the recommendation sharpens to a specific reference-density
  threshold.

**India, Thailand and Australia are low marginal value for attribution**, because
the incoming batch's validation genomes for those countries already have ample
in-panel references (56 / 1,753 / 283). Adding Australia has a *separate*
justification — it is under-represented 2.5× and sits basal in the global tree —
but that is a population-structure argument, not an attribution one, and it costs
a Phase 2 re-run to exploit.

**The seven zero-reference countries have literally nothing to add.** That is the
surveillance gap, and no amount of downloading fixes it. Worth saying plainly in
the Discussion: we checked.

### The constraint that governs all of this

**Add for cgMLST scoring only — Phase 1.** cgMLST needs no unit assignment, so
new genomes enter the reference pool without touching the partition:
**invalidates nothing.** Putting them into the SNP/unit analysis is **Phase 2** —
re-partition plus full pipeline re-run — which **invalidates every unit, r/m
value, distance table and tree.** Do not let a good idea about Mexico turn into a
re-partition by drift.

---

## 8. Ethics / IRB

**Handled by the epidemiology team** (confirmed by the user 2026-08-21) for the
312 in-house Nakhon Phanom isolates (259 `IP-` patient, 53 `IE-` environmental).

**Still to do before submission:** obtain the approval number and approving body
and put them in the Methods. "The epis handled it" is not a Methods sentence.
This is no longer a blocker, only a text-gathering task.

---

## 9. Rules that keep this straight

1. **Every ENA census unions `read_run` and `assembly`.** A reads-only query
   silently omits assembly-only depositions and already produced two wrong
   claims.
2. **Ground truth is tier A or B only.** A deposit country is panel context. The
   distinction is the reason the leave-group-out result is trustworthy.
3. **Quote a denominator with every percentage.** Panel coverage is 41.4%
   (union), 44.4% (reads-only) or 37.0% (public-derived only) — all three are
   defensible and they are not interchangeable.
4. **Never carry a unit label across partition versions.** v4b `strain_4` and
   v4c `strain_4` share zero members.
5. **Re-derive, do not copy.** Of the six headline numbers checked today, four
   were wrong in at least one circulating document.
6. **Country counts change under you.** Six countries went from zero to non-zero
   between 2026-08-09 and today. Date-stamp every census and re-run it
   immediately before submission.

---

## 10. Documents superseded by this file

| document | what is now wrong in it |
|---|---|
| `SAMPLING_FRAME_2026-08-21.md` §3 | the 9-of-16 claim; Mexico 0; Philippines 0; the 44% denominator |
| `GAP4_phylogeography_biased_sampling.md` §1, §12 | 29 countries / 54,076 cases / 33% of burden |
| `LITERATURE_POSITIONING_2026-08-21.md` row E | the cgMLST scheme citation |
| `GAP1` / `GAP2` | the Lichtenegger scheme attribution |
| `MANUSCRIPT_OUTLINE_2026-08-21.md` R4, §6.4 | superseded by §4 and §5 here (outline updated 2026-08-21) |
