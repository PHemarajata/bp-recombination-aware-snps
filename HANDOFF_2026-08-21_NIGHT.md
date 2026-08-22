# Handoff, 2026-08-21 night — updated 2026-08-22

Read this first. Working directory
`/home/phemarajata/Downloads/snp-mod-local-working`.

> ## ⚑ THE BASIS IS FROZEN — 2026-08-22
>
> **`FINAL_BASIS_2026-08-22/` — 85 units, 2,340 genomes.** The corrected
> workstation partition. **Run `python3 freeze_basis_bp.py` before quoting any
> number** (12 checks, non-zero exit on drift).
>
> - **r/m headline is 7.70 (n=47)**, alignment-derived Gate 1. Not 7.44 (A100),
>   7.38 (A100 + Mash proxy) or 7.26 (this basis + Mash proxy).
> - The METHODS production/control designation is **flipped**: this is the
>   reported partition, the A100 88-unit run is the reproducibility control.
> - Join the panel on **`unit_membership`**, never `subcluster` — the latter
>   labels 615 non-members.
> - Never take membership by globbing `L1v4c_out/Clusters` (88 hybrid dirs) or
>   `cfml/`.
> - 66 off-basis files moved to `RETIRED_2026-08-22/` — see its README.
> - Impact of the freeze on every downstream result:
>   **`DOWNSTREAM_IMPACT_2026-08-22.md`**.

Supersedes `HANDOFF_2026-08-21_EVENING.md`, which is still correct on framing and
§3 findings but stale on §5 (five of its eight action items are now closed).

---

## 0. Nothing is running. The re-derivation finished.

All **6/6** replicon-runs completed, `rederive_2026-08-21/`, 21:22–22:02.

| unit | n (excl. Reference) | replicons |
|---|---|---|
| `strain_1_L1_8` | 89 | 2/2 OK |
| `strain_14_L1_4` | 12 | 2/2 OK |
| `strain_1_L1_26` | 153 | 2/2 OK |

**One failure was hit and fixed, and it is worth knowing about.** Both
`strain_1_L1_26` replicons first died at **rc=135, "Bus error (core dumped)"**,
in **pyjar** (joint ancestral reconstruction) — *after* RAxML had already
succeeded, so it is **not** the zero-seed bug and not a RAxML failure. Cause:
`rederive_units_bp.sh` omitted **`--shm-size=2g`**. Docker defaults `/dev/shm`
to 64 MB, pyjar allocates its reconstruction arrays in shared memory, and on a
154-taxon unit it runs off the end of the segment. The 90- and 13-taxon units
passed, which is the size threshold showing itself. `nextflow.config` sets the
same 2g for the same documented reason, so the fix is production parity, not
tuning. Fixed and both replicons then completed all 5 iterations.

**If you ever see rc=135 / SIGBUS from Gubbins after RAxML has succeeded, it is
`/dev/shm`, not memory and not the seed.**

### §5 item 2 is CLOSED

r/m recomputed through the pipeline's own `pool_recombination_stats.py`, spliced
into `L1v4c_out/Summaries/recombination_rm.tsv`, `strain_1_L1_10` dropped, and
`NUMBERS.tsv` regenerated. Full result in **`REDERIVATION_RESULT_2026-08-21.md`**.

**86 → 85 units, 2,352 → 2,340 genomes.** `strain_1_L1_26` moved r/m **3.10 →
4.47 (+44%)** because the genome removed, `SRR2896257`, was that unit's longest
surviving branch at 1,382 substitutions.

**The quotable r/m did not move:** Gate 1 median **7.26 (n=47)** and
no-divergent-member median **7.26 (n=59)**, both unchanged. Only the all-unit
median shifted (5.34 → 5.51), and that one is marked do-not-quote anyway.

⚠ **Two corrections came out of this:**

1. **The Gate 1 median: RESOLVED. 7.38 is the A100 run, 7.26 is the
   workstation run.** Both `recombination_rm.tsv` files were pulled from Drive
   (now in `rm_provenance/`); the A100 table reproduces every 08-19 figure to
   the digit (5.70 / 47:7.38 / 9:1.67 / 32:2.48). Not a hardware disagreement —
   the two runs agree to **0.46%** across the 86 shared units. The whole gap is
   that the A100 run **split `strain_1_L1_26`** into three units and the
   workstation run kept it whole. **Quote 7.26**, the unsplit partition, which
   is what `curated_L1v4c_clusters.tsv` and everything downstream uses. **Do not
   overwrite 7.38** where it sits beside "88 units" and "5.70" — label it the
   A100 variant. Full working in `REDERIVATION_RESULT_2026-08-21.md` §3.

2. **`generate_numbers.py` was reading r/m from a denormalised copy** (the
   `unit_rm` column of `L1v4c_MERGED_METADATA.tsv`) and so still reported the
   pre-re-derivation values. It now reads the pipeline's authoritative table.
   The stale copies were repaired in place too.

**W3 is now CLOSED too — and it moved the headline: r/m is 7.70, not 7.26.**
See `GATE1_ALIGNMENT_RESULT_2026-08-21.md`. The Mash proxy overstates diversity
by a median 1.30x (max 17x) and misplaces **22 of 85 units**. Gate 1's structure
survives the change of metric and is *sharper* on alignment distances (median
r/m 1.53 -> 8.59 -> 2.14 across bands); its **floor** was simply in the wrong
place, carried across unit systems untranslated. Relocated on union coverage and
tract length — **not** on r/m, which would be circular — to **[700, 4,700]**,
floor bracketed **(588, 755]**. The **ceiling translates essentially unchanged**
from 4,671, which is a real check since nothing forced the two systems to agree.
In-window 47 units, median **7.70** (IQR 5.51–9.44); outside, 38 units, median
**1.99**. Insensitive to floor placement across the whole bracket (7.70–7.78).

⚠ Two disclosures carried forward: alignment SNP counts are not *provably*
identical to `ska distance`, and **union coverage does not reproduce the
calibration's 76–88%** (max band median 68%, and it rises with diversity). The
floor does not depend on the coverage criterion, but a reviewer could press on
it. Both are in §7 of the result doc and `rm.gate1_caveat`.

---

## 1. The headline: accessory attribution was tested and it fails

Full result in **`ACCESSORY_ATTRIBUTION_RESULT_2026-08-21.md`**. This was the last
experiment that could have changed the paper's headline. It did not.

**It looked like it worked.** Country nearest-neighbour **13/43 (30%, kappa
0.263)** against core's 9/43 (21%, kappa 0.188) and a 28% baseline — the first
time country has cleared baseline in this project. `modal_k5` reached 35%.

**Four pre-registered controls, committed in `bf93d09` before the result was
computed.** Three fail:

- **Control 4, decisive: 0/13 where a genuine close relative exists**, 11/22
  where none does. Pure attractor signature, and **worse than core (1/13)** in
  the only stratum where a correct answer means anything.
- **Control 1:** country accuracy swings **26% / 23% / 5%** across contig-count
  pool tertiles.
- **Control 2:** contigs vs mean accessory distance rho **+0.156** (p=8.6e-18)
  against **+0.038** for core — the 4× ratio the control predicted.
- **Control 3 PASSES:** real accuracy sits far outside a permutation null
  shuffled within contig strata (p=0.001 both scales). There *is* non-random
  accessory structure. It is not country-attributive. Report this honestly —
  and report its limitation, that shuffling cannot separate geography from
  BioProject.

**Post hoc and decisive: dropping ONE pair of genomes** (`GCF_006542565_1_Mexico_Huasabas`,
`GCF_006542585_1_Mexico_Huasabas`) takes country from 13/43 to **8/43, below
core**, and Mexico from **5/5 to 0/5**.

Accessory is also **worse at region** (kappa 0.707 vs core's 0.761) — the scale
that actually works.

**Two things this buys the paper:**

1. **The core result is strengthened.** Accessory was the best remaining
   hypothesis for shallow geographic signal. Four representations now agree
   (cgMLST alleles, PopPUNK core, PopPUNK accessory, SNP distances). PopPUNK
   core independently reproduces the cgMLST core result (country 19% vs 21%,
   region 93% at modal k=20 in both), so **the core failure is not an artifact
   of the typing system.**
2. **A methodological finding.** Without the controls this would have been
   written up as "accessory lifts country attribution above baseline." See §3
   for how to phrase the literature claim — it is narrower than we assumed.

**Keep as a lead, labelled a hypothesis (§6 of the result doc):** those two
Mexican references share accessory content with five cases across a core gap of
d = 0.406–0.462. n=2 and n=5, so it is not a result. Cheap to test — acquire more
Mexican genomes and see whether it scales with reference count or stays pinned to
Huasabas.

**Route B is not closed.** Pangenome/unitig presence-absence is uninstalled and
untested, and it is what the Salmonella precedent actually used.

---

## 2. Also closed today

**cgMLST scheme concordance** (`SCHEME_CONCORDANCE_2026-08-21.md`). On the 30
validation genomes scored under both schemes: country 0/30 (PubMLST) vs 1/30
(Lichtenegger); **region 28/30 (93%) under BOTH** at modal k=20; NN distances
correlate at **r = +0.999**.

⚠ **The correction this forces:** the full runs read 0/30 vs 9/43 at country,
which invites "the published scheme recovered signal." **It did not.** The gain
is entirely the **13 validation genomes added in the same batch**. Scheme and
validation set changed together; always say which one moved a number.

**Citation audit** — four defects fixed, all verified against fetched PubMed
records:

- **PMID 32149236, cited as "Pearson 2020" in six files, is a materials-chemistry
  paper about formic acid adsorption onto ceramics.** Correct is **32134991**.
  It was worst in `phylogeography_diagnostics_bp.py`, where it sat in a comment,
  in a string **printed at runtime**, and in a `--help` default.
- **"Ashcroft et al. 2021" is a phantom.** No such paper. It is Lichtenegger et
  al. 2021, JCM **59(8)**:e00093-21, PMID 33980649. Stated definitively now:
  PubMed returns zero Ashcroft Bp cgMLST records and the DOI we attached to
  "Ashcroft" was Lichtenegger's.
- "Chewapreecha 2024" → **Seng et al. 2024**, Nat Commun 15:5699, PMID 38972886.
- "Ceará clade (Pearson 2021)" → **Gee et al. 2021**, mSphere 6(1):e01259-20,
  PMID 33536328; author list retrieved.

Verified correct, no change: Viberg 2017, Gee 2017, Sprenger/Gulvik 2026,
Chewapreecha 2017, Pearson 2009 (*BMC Biology*).

**Still unverified, abstract-only:** Gee 2017's n=26; McLaughlin's D=0.8512.
Neither contradicted, neither confirmed.

**The repo was committed** — 5 commits, working tree clean. See §5.

---

## 3. The literature find that reframes the whole result

`ACCESSORY_ATTRIBUTION_RESULT_2026-08-21.md` §8. Two things:

**(a) We were describing the Salmonella precedent wrongly.** Bayliss et al. 2023,
*eLife* 12:e84167, PMID 37042517 — the paper we held as a bare URL. Macro-F1
0.954/0.718/**0.661** confirmed, and the target *is* country. But:

- **It does not use accessory genes.** Features are **unitigs called from reads**;
  nothing assembled, nothing annotated.
- Its labels are **patient-reported travel destination** — the same ground-truth
  design as ours.
- **It does control data quality** (coverage floor, downsampling, unitig-length
  cap, 220 exclusions) and runs temporal + cross-institution external validation.

So **do not write "they did not run controls."** Write: *assembly-quality
confounding of gene-content features, and stratification by whether a genuine
close relative exists, are not addressed in the source-attribution literature we
could find.* Their only relatedness step is deduplication to one isolate per SNP5
cluster per country — **no leave-clade-out, no close-relative stratification**,
which is exactly our control 4.

**(b) The B. pseudomallei literature already answered this in 2007.**
**Tuanyok et al. 2007, PMID 17933898** partitions the species on a single
accessory gene cluster — **YLF vs BTFC**, Australia versus Thailand-and-elsewhere,
across 571 isolates. Duangsonk 2006 (PMID 16597858) and Chewapreecha 2017 find
the same axis. **Every accessory-geography result in this organism resolves
Australia vs Asia. None resolves country.**

That is our divergence-depth mechanism, independently, nineteen years earlier. A
reviewer asking "why didn't accessory work?" has a published answer. **Our
contribution is that we tested it prospectively at country scale and measured
where it fails.**

**(c) Citable support for the control:** Panaroo (PMID 32698896) — on
near-identical genomes where the true accessory genome is ≈0, tools reported
2,584–3,670 accessory genes, **59% of the discrepancy from assembly
fragmentation**; Panaroo's own QC flags outliers **by contig count**. Plus
Klassen 2012 (PMID 22233127), Denton 2014 (PMID 25474019), GenAPI (PMID 32690023).

⚠ **Gao et al. 2025, PMID 40644951** (*Cronobacter*, 748 assemblies, accessory
gene profiles → continent) is the **closest published analogue to our
experiment** and is **paywalled and unverified**. Get the PDF before writing
about it. Do not characterise its controls.

---

## 4. Correction to the evening handoff's §5 item 2

It lists four affected units under one heading. Verified against
`curated_L1v4c_clusters.tsv`, they come from **two separate defects**:

| cause | unit | change |
|---|---|---|
| duplicate BioSamples | `strain_1_L1_8` | 91 → 89 |
| duplicate BioSamples | `strain_14_L1_4` | 14 → 12 |
| duplicate BioSamples | `strain_1_L1_10` | 7 → 4 — **drop the unit** |
| **register-excluded genome** | `strain_1_L1_26` | 154 → 153 (`SRR2896257`) |

**No dropped duplicate is in `strain_1_L1_26`** — its shrinkage is the
`broken_assembly` exclusion, a different list. The counts in the evening handoff
are all correct; only the cause attribution was merged. The other 11 duplicate
drops sit in no analysed unit. **82 of 86 units are untouched.**

`rederive_units_bp.sh` pins parameters to the production run (same container
digest, 5 iterations, RAxML, min-snps 3, `--invariant-site-correction`, filter
25%) because r/m shifts 0.47–0.78× with settings and cannot be pooled across
them. Two deliberate deviations, both documented in the script header: an
explicit `--seed` (the pipeline passes none, and Gubbins' unseeded
`randint(0,10000)` draws 0 about 1 run in 10,001), and strictly sequential runs
in isolated working directories (Gubbins writes scratch to CWD, not `--prefix`).

---

## 5. Repo state

**5 commits on `feat/core-shrinkage-and-itol`, working tree clean, NOT pushed.**
Pushing is your call.

`c39913b` corpus + code · `bf93d09` pre-registered controls · `4e3ba08` accessory
result · `4194504` citations · `4bbb7e4` re-derivation driver
(+ concordance, + literature).

**`ACQUISITION_TARGETS_US_2026-08-21.md` was deliberately excluded** and added to
`.gitignore` §6 with the reason recorded there: its table 1 joins run + biosample
+ month date + anatomical specimen for five 2021 outbreak isolates, and the prose
below names the four patients' US states. The accessions are individually public;
the assembled join is what this repo does not track. **Reverse it if you
disagree** — it is one line in `.gitignore`.

Nothing data-shaped is tracked: 716 KB staged, all `.md`/`.py`/`.sh` at top level.

---

## 6. Still open, re-ranked

0. **REPRODUCIBILITY TEST — once Methods are frozen, before submission.**
   Re-run the analysis end to end from primary data and diff every headline
   against the documents. Not optional: the 2026-08-21/22 sessions edited many
   intermediates **in place** rather than re-running — `recombination_rm.tsv`
   spliced and one unit dropped, `unit_rm` rewritten on 259 metadata rows,
   `generate_numbers.py`'s r/m source changed twice, §2.6.1/§2.12.7/§2.12.10
   rewritten, panel and citation corrections. Every change was justified and
   committed; the collection has **not** been re-derived since. This project's
   recurring failure is a number that was right when computed and left behind by
   a later correction. Budget it as real compute (Gubbins hours; `--shm-size=2g`
   and the zero-seed trap both apply).

   **Take membership from `curated_L1v4c_clusters.tsv` (86) or
   `rm_provenance/A100_cluster_membership.tsv` (88) — never by globbing
   `L1v4c_out/Clusters`** (see §9).

1. **Finish the re-derivation** (§0) — running. Then `generate_numbers.py`.
2. ~~File the GAMBIT issue.~~ **CLOSED by decision 2026-08-21: stay on GAMBIT
   DB 2.2.0, do not adopt 3.0.0, do not file the issue.**
   `THEIAGEN_GAMBIT_ISSUE.md` stays drafted and unfiled. **kmerfinder is dropped
   too — set `call_kmerfinder: false`**, superseding the `true` in the evening
   handoff's TheiaProk block (that recommendation only existed to replace the
   contamination signal GAMBIT 3.x had broken; on 2.2.0 GAMBIT works). Species
   gating stays on **mash to K96243** either way.
3. **IRB approval number** from the epi team into Methods. Human action.
4. **Get the Gao 2025 PDF** (§3) before the literature section is written.
5. **Two method questions for Paper 2**: `+ASC` vs `-fconst` on one unit;
   recompute Gate 1 diversity from alignment distances instead of the Mash proxy.
6. **The Mexican accessory lead** (§1) — cheap, and it is the only route by which
   accessory comes back.
7. Numbered clade nomenclature; two-stage placement before any UShER index (MAT
   on the **masked** alignment); implement and score the PBP dual-locus scheme.
8. Systematic check of the BioProject-control novelty claim before writing
   "first".

**Deliberately not doing:** re-partitioning, re-running the SNP pipeline
wholesale, rewriting the corpus (`REDO_DECISION_2026-08-21.md`).

---

## 7. Rules and traps — unchanged, plus two

The evening handoff's §7 list all still stands. Two additions:

9. **Verify every PMID against a fetched PubMed record before it goes in a
   manuscript.** One in this corpus resolved to a paper about ceramics, and
   another named an author who has never written on the subject.
10. **When two things change at once, say which one moved the number.** The
    scheme swap and the validation-set expansion happened together and the
    scheme was getting the credit (§2).

---

## 9. ⚠ `L1v4c_out/Clusters` is a hybrid directory — found 2026-08-22

It holds **88 unit directories** where `curated_L1v4c_clusters.tsv` has **86**.
The extras are `strain_1_L1_36` and `strain_1_L1_37`, the A100 run's split
children of `strain_1_L1_26`, sitting beside `cluster_strain_1_L1_26` which still
contains the **unsplit 155-sequence parent**. **Those 153 genomes are present
twice.**

Any script enumerating units by globbing that directory inherits the defect. Two
outputs are known to carry it:

| file | pathology |
|---|---|
| `DISTANCES_v4c_SUMMARY.tsv` | `strain_1_L1_11` (24 vs 18), `strain_1_L1_22` (34 vs 32), `strain_1_L1_26` (154 vs 98) carry workstation membership; the rest match the A100 |
| `CGMLST_CONCORDANCE.tsv` | same, plus `strain_27_L1_1` (11 vs 10). Median concordance **0.8459** as filed, **0.8552** excluding the six ambiguous units. The quoted **+0.846** is as-filed |

Everything else audited is single-partition: `L1v4c_MERGED_METADATA`,
`PANEL_v4d`, `cluster_membership`, `cluster_sizes`, `NU_HYPOTHESIS`,
`PHYLOGEOGRAPHY_ASSOCIATION_v4c`, `trackA_diversity_*`, both `recombination_rm`
tables and the `SCALE_*` set.

**The r/m headline is unaffected** — 48 in-window, median **7.44** either way,
because the two misplaced units swap across the window and both sit below it.
**The control figure 7.70 is unaffected entirely**, since for those units the
file's membership *is* the control run's.
