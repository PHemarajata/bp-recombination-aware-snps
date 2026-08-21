# Handoff — 2026-08-21, session end

Read this first in the next chat. Working directory
`/home/phemarajata/Downloads/snp-mod-local-working`.

---

## 1. RUNNING RIGHT NOW — check these first

**Updated 2026-08-21 17:20. Nothing is running. Both jobs are closed out.**

| job | final state | note |
|---|---|---|
| **ClonalFrameML v4c** | **DONE — 172 / 172** replicon-units, all `exit=0`, driver exited after 10h00 | no failures, no empty `cfml.em.txt`. `nu_hypothesis_bp.py` has been re-run on the full set — see §2 |
| **ENA fastq download** | **ABANDONED — 0 files.** The fetcher died leaving only a 0-byte `additions_2026-08-21/fetch.log` | superseded: pull reads with **Terra's SRA fetch workflow** instead, then assemble (§4) |
| Yuyi / A100 CFML | overlap control | if hers lands, compare — hardware-reproducibility check |

### The CFML denominator is 172, not 176 — don't re-derive it as 176

`L1v4c_out/Clusters` holds **176** directories but only **172** carry a
`.core.full.aln`, and CFML needs the full alignment. The four without one are
two units × two replicons:

- `strain_1_L1_36__GCF_030297295_1` (n=48)
- `strain_1_L1_37__GCF_003546995_3` (n=9)

Both were computed **on the A100** and only their trees and Gubbins outputs were
rclone'd back — the alignments never left that machine (`A100_v4c_Clusters`
carries `.core.full.aln` for **0** of 176 dirs, consistent with
[[a100-cluster-trees-are-on-drive]]). They are **not** in the cleanup logs, so
nothing local deleted them. They are recoverable from the A100 if you want
172→176 coverage; until then **172 is the correct, complete denominator** and
86 is the per-replicon n. The "176" in the pre-update version of this file was
a wrong denominator, not a shortfall.

CFML is resumable — a unit with `cfml.em.txt` is skipped.

---

## 2. What changed today (results, not activity)

**Validation set was wrong: 26 → 31.** Five genomes with known exposure were
never flagged. Fixed via `build_v4c_panel.py --fix-exposure-flags` +
`EXPOSURE_OVERRIDES.tsv`. Corrected numbers:

| scale | leave-group-out | baseline |
|---|---|---|
| country | **0 / 24** | 0 |
| **sub-national** | **0 / 5** (was "untestable") | 0 |
| region | **92%** | 54% |

**Resolution curve** (`RESOLUTION_CURVE_RESULT_2026-08-21.md`) — subsampled
k loci from cgMLST, k = 2 → 4,089. **Country flat at ~0 across a 2,000-fold
range; region climbs 51% → 85%.** The region curve is a built-in positive
control: the estimator demonstrably *can* use resolution, so the country failure
is absence of signal, not bluntness.

**ν hypothesis REFUTED — and this now stands on the complete 172-unit set.**
The conclusion held when the run finished, but **several supporting numbers
moved, because the earlier ones were computed mid-run on ~148 units.** Use the
full-set column and nothing else:

| quantity | quoted mid-run (~148) | **full set (172; n=86/replicon)** |
|---|---|---|
| ν vs Gubbins r/m | −0.42 / −0.49 | **−0.286** (p=0.008) / **−0.367** (p=0.0005) |
| ν vs δ (the confound) | −0.86 | **−0.791 / −0.785** (pooled −0.765, p=2e-34) |
| CFML/Gubbins r/m offset | ~4.9× | **2.2× (chr1) / 2.5× (chr2)** |
| ν of Gubbins-rejected vs rest | uniform, p=0.23 | chr1 p=**0.214**, chr2 p=**0.039** |

Still negative, still opposite to prediction, so **ν is refuted**. Cause is
unchanged: ν and δ are strongly anti-correlated because ClonalFrameML trades
them off, so **ν is not independently interpretable — never read it alone.**

Two corrections to carry forward:

1. **The offset is ~2.2–2.5×, not ~4.9×.** Anywhere the 4.9× figure appears, it
   came from the partial run. Median Gubbins r/m 5.34 vs CFML 14.09 (chr1) /
   13.85 (chr2).
2. **An argument was withdrawn, not just a number.** The old reasoning for "CFML
   does not rescue Gubbins-rejected units" was *the CFML/Gubbins ratio is no
   larger for rejected units (p=0.23), so the offset is uniform.* **That test is
   circular** — the groups are defined by low `rm_gubbins`, which is the ratio's
   own **denominator**, so selecting on it inflates the ratio mechanically. On
   the full set it now comes out strongly significant the *other* way (6.10× vs
   1.86×, p<0.001). **Neither result means anything.** Don't cite either.
3. **The no-rescue conclusion survives on better evidence.** Ask where rejected
   units sit on the CFML scale itself: they keep the significantly *lower* CFML
   r/m (median 9.99 vs 15.56 chr1, 9.85 vs 15.59 chr2; p≈4e-05 / 4e-06), sit at
   the **30th / 26th percentile** of the CFML distribution, and the two tools
   agree on rank at rho **+0.611 / +0.598**. They cross 3.0 only because the
   whole distribution shifted up — **52/53 and 53/53 accepted units clear it
   too.** A threshold that passes ~99% of units isn't discriminating. **CFML
   re-scales; it does not re-rank.**
4. **"Rejected units have no distinctive ν" can't be stated flatly any more** —
   holds on chr1 (p=0.214), but chr2 is nominally significant (p=0.039) with
   rejected ν *higher*, i.e. pointing away from the prediction.

✅ **`NU_HYPOTHESIS_RESULT_2026-08-21.md` has been REGENERATED** on the 172-unit
set (supersedes the n=81 and n≈148 versions; pre-update copies kept as
`*.partial148.bak`). Note the script rewrites only `NU_HYPOTHESIS.tsv`, **not**
the prose — so if you re-run it, hand-update the .md again or it goes stale.

**cgMLST done** — 4,089 loci, 2,976 genomes, 97.8% classified. Concordance with
filtered SNP distance median r = **+0.846**. Country 0/30, region 23/29.

**The sampling-frame answer** (`SAMPLING_FRAME_2026-08-21.md`) — see §3.

**Cleanup:** 247 GB deleted, 69 GB archived to TB1 (`TB1_ARCHIVE_MANIFEST.md`).
Disk 91 GB → 411 GB free.

---

## 3. The most important finding of the day

**For 9 of our 16 validation source countries, ENA holds ZERO genomes.**
Philippines 0 public (we hold 12), Mexico 0/8, Guatemala 0/2, Aruba 0/2,
Nicaragua, El Salvador, Costa Rica, Trinidad and Tobago, Martinique — all 0.

**We hold the only ones in existence, and they are the genomes being held out.**

So country attribution is impossible *for anyone*. This converts the limitation
into a finding about global surveillance gaps. **It is the answer to "how did
you come up with these 2,976 sequences?"**

Also, state before a reviewer does: the panel is **44% of country-labelled ENA
BioSamples** and **not proportional** — Australia is under-represented 2.5×
(we hold 283 of 1,594), Cambodia 5×, Puerto Rico we hold 5 of 61.

---

## 4. Immediate next steps

**a) Assemble the 40 runs on Terra.** Do not download locally — the local
fetcher is abandoned. Pull reads with **Terra's SRA fetch workflow**, then run
TheiaProk Illumina PE.

**Build the sample set from 40 runs, not 43.** `ENA_TARGETS_CLASSIFIED.tsv` has
43 rows: 8 A_exposure_stated + 5 B_external_evidence + 27 C_deposit_only +
**3 D_unusable**. The three D rows are the *B. thailandensis* runs
(`SRR22548210`, `SRR22548211`, `SRR22548212`) — exclude them. 43 − 3 = 40.

### TheiaProk inputs — verified against current `main`, 2026-08-21

Checked by reading the WDL and its sub-workflows, not the release notes.

**The three critical settings survived the version bump.** The call is still
`call digger_denovo.digger_denovo`, and `wf_digger_denovo.wdl` still declares
`assembler` (**default still `"skesa"`**), `assembler_options` and
`filter_contigs_min_length` (default 200) as top-level inputs — so both
`digger_denovo.*` keys still resolve and have **not** been silently orphaned
back to SKESA. `task_quast.wdl` still uses `min_contig_length = 500`, so
`filter_contigs_min_length: 500` still reconciles the delivered FASTA with the
reported metrics ([[assembly-qc-gates-recalibrated]]).

```json
{
  "theiaprok_illumina_pe.samplename": "${this.bp_2b_assembled_id}",
  "theiaprok_illumina_pe.read1": "${this.read1}",
  "theiaprok_illumina_pe.read2": "${this.read2}",
  "theiaprok_illumina_pe.genome_length": "${7247547}",
  "theiaprok_illumina_pe.expected_taxon": "${}",
  "theiaprok_illumina_pe.digger_denovo.assembler": "spades",
  "theiaprok_illumina_pe.digger_denovo.filter_contigs_min_length": "${500}",
  "theiaprok_illumina_pe.digger_denovo.assembler_options": "${}",
  "theiaprok_illumina_pe.perform_characterization": "${true}",
  "theiaprok_illumina_pe.call_kmerfinder": "${true}",
  "theiaprok_illumina_pe.call_ani": "${false}",
  "theiaprok_illumina_pe.call_plasmidfinder": "${false}",
  "theiaprok_illumina_pe.call_abricate": "${false}",
  "theiaprok_illumina_pe.call_gamma": "${false}",
  "theiaprok_illumina_pe.call_resfinder": "${false}",
  "theiaprok_illumina_pe.call_arln_stats": "${false}",
  "theiaprok_illumina_pe.merlin_magic.run_amr_search": "${false}"
}
```

**What changed from the previous input set, and why:**

- **`genome_length: 7247547`** (K96243, both replicons) — *the substantive one.*
  Left unset, `task_screen.wdl` estimates genome size by running **mash on the
  reads**; on a 7.2 Mb, ~68% GC, repeat-rich two-replicon genome that collapses
  repeats and reads low, inflating estimated coverage and making
  `min_coverage: 10` mean something other than 10×. Supplying it switches the
  screen to exact bases÷length. It also flows into **both** `cg_pipeline` calls,
  so `est_coverage_raw`/`est_coverage_clean` become comparable across samples
  instead of each being divided by its own fragmented assembly length.
- **`call_ani` → false.** Already measured useless here: the animummer DB is
  PulseNet-scoped and does not cover *Burkholderia* — 190/192 rows last batch
  said "did not surpass the 70.0 threshold".
- **`call_kmerfinder` → true.** Its bacterial DB *does* cover *Burkholderia* and
  it is the actual contamination detector. Covers the signal given up by no
  longer getting an independent mash size estimate (above).
- **`call_plasmidfinder` → false — must be set explicitly.** It now defaults to
  **`true`** in this version, so omitting it is *not* the same as disabling it.
  Its DB is Enterobacteriaceae + Gram-positive replicons; nothing for
  *Burkholderia*.
- **`call_resfinder` / `call_abricate` / `call_gamma` / `call_arln_stats` /
  `merlin_magic.run_amr_search` → false.** Cost with no return for a
  phylogeny/cgMLST panel. `wf_merlin_magic.wdl` has 18 organism dispatch blocks
  and **none is Burkholderia**; `run_amr_search`'s taxon map holds 8 species,
  none Burkholderia, behind an explicit species guard — it will **not** crash,
  it silently does nothing. Drop the `abricate.cpu` key along with abricate.

**Leave alone — checked, no action needed:**

- **`expected_taxon` stays empty.** It feeds amrfinder, resfinder, `ts_mlst` and
  `merlin_tag` via `select_first([expected_taxon, gambit...])`. Setting it would
  override GAMBIT and force the *B. pseudomallei* MLST scheme onto a
  misidentified genome — hiding exactly the *B. thailandensis* contamination
  that got caught last time (§6, tier D).
- **`trim_min_length: 75` is safe for this batch.** Across all 43 runs
  compressed bytes-per-spot is 107–150, consistent with 2×150 throughout; there
  are no 2×50 runs that a 75 bp floor would wipe out. (Worth re-checking for any
  *future* batch — a short-read run would be silently destroyed.)
- **Keep `perform_characterization: true`.** Prokka's gene count feeds the
  recalibrated gate (`expected = 821 × Mb + 1.0 × contigs`, flag ratio > 1.20).
  Switching characterization off to save money **breaks that gate**.
- Bracken defaults `true` in the read-QC sub-workflow but is gated behind
  `defined(kraken_db) && call_kraken`, both unset — it never fires.
- `call_rasusa` false, `mlst_run_secondary_scheme` false,
  `concatenate_illumina_lanes` only fires with lane2–4 inputs. BUSCO now runs
  unconditionally — free extra QC.

**After the run, confirm the `assembler` column reads `spades` before trusting
anything downstream.** Terra silently ignores a mistyped fully-qualified input
name — that is exactly how the SKESA batch happened
([[theiaprok-digger-defaults-to-skesa]]).

Then assembly QC with the recalibrated gates (core coverage ≥85% + gene-count
ratio, **not** length).

**b) Then cgMLST only — do NOT re-partition.**
chewBBACA AlleleCall against the existing prepared schema
(`cgmlst_scheme/prepared/`), incremental. Then re-run
`attribution_score_bp.py` and `cgmlst_analysis_bp.py`.

**This takes the validation set to 44** and adds **Australia, Thailand, India** —
countries where the panel *does* hold references, so country attribution finally
gets a fair test. Currently it is dominated by countries with zero references.

The 13 new ground-truth genomes are already classified in
`ENA_TARGETS_CLASSIFIED.tsv` (8 tier-A `ex`-stated, 5 tier-B aromatherapy/India)
and the aromatherapy five are already registered in `EXPOSURE_OVERRIDES.tsv`.

**c) ~~When CFML finishes — `nu_hypothesis_bp.py` on all 176.~~ DONE.**
CFML finished 172/172 and the analysis was re-run on the full set; results and
the corrected numbers are in §2. Remaining sub-task: **regenerate the stale
`NU_HYPOTHESIS_RESULT_2026-08-21.md`**, which still describes the ~148-unit run.
Optionally recover the two A100-only alignments (§1) to reach 176.

---

## 5. Expansion decision pending (user offered to pay for VMs)

~2,000 genomes available and worth adding, **in this order**: Australia
(~1,311), Puerto Rico (~56), Cambodia (~487), India (~40), then Viet
Nam/Taiwan/Mali/New Caledonia (~107). **Do NOT add more Thailand** — already
over-represented at 59%.

**Two phases, and the distinction controls all the risk:**

- **Phase 1 — attribution only:** download → assemble → QC → cgMLST → re-score.
  **Invalidates nothing**, because cgMLST needs no unit assignment.
- **Phase 2 — full integration:** re-partition + re-run SNP pipeline.
  **Invalidates every unit, r/m value, distance table and tree.**

**Recommend Phase 1 first.** It answers *does a balanced reference panel change
attribution?* for the cost of assembly alone. Phase 2 only if it does.

---

## 6. Metadata discipline — the standard now in force

Two purposes, two standards (`classify_ena_origin_bp.py`):

| tier | meaning | use |
|---|---|---|
| A_exposure_stated | ENA country reads "X **ex** Y" | ground truth |
| B_external_evidence | published investigation + `EXPOSURE_OVERRIDES.tsv` citation | ground truth |
| C_deposit_only | country recorded, travel unknown | **panel only, never ground truth** |
| D_unusable | no country, or wrong species | exclude |

D is not hypothetical — **3 *B. thailandensis* runs** were caught in the CDC
BioProjects by a study-level query with no taxon filter.

---

## 7. Key documents

| file | what |
|---|---|
| `SAMPLING_FRAME_2026-08-21.md` | the sampling-frame answer; ENA census |
| `ATTRIBUTION_AND_DISTANCES_FINDINGS_2026-08-20.md` | main results, revised for 31 |
| `RESOLUTION_CURVE_RESULT_2026-08-21.md` | resolution curve |
| `NU_HYPOTHESIS_RESULT_2026-08-21.md` | ν refuted — **regenerated on the full 172-unit set**, current. Data: `NU_HYPOTHESIS.tsv` (172 rows) |
| `MLST_FINDINGS_2026-08-20.md` | MLST + cgMLST, ST92 |
| `LITERATURE_POSITIONING_2026-08-21.md` | vs Chewapreecha/CDC/Gulvik; §6a is newest |
| `IDEAS_AND_OPEN_QUESTIONS.md` | running list of what to try |
| `PRIMER_HOW_TO_READ_THIS_WORK.md` | concepts + how to catch my errors |
| `ACQUISITION_TARGETS_US_2026-08-21.md` | US sequences worth getting |
| `A100_QUICKCARD.md` / `A100_RUNBOOK_YUYI*.md` | Yuyi's job (also on Drive) |
| `TB1_ARCHIVE_MANIFEST.md` | what was deleted/archived and why |

**Note:** rclone remote is `peerah-gdrive:` locally but the runbooks say
`gdrive_ph:` — Yuyi's machine name. Same Drive.

---

## 8. Still open

- Accessory-genome attribution — **highest-value untested idea**. PopPUNK
  accessory distances exist (`poppunk_bp/db/db.dists.npy`) but cover only 10 of
  31 validation genomes; needs the db extended with the newer batch first.
- Numbered clade nomenclature (region as annotation, never in the name).
- Two-stage placement (`poppunk_assign` → within-unit) before any UShER index;
  MAT must be built on the **masked** alignment.
- Implement the actual PBP dual-locus scheme and score it through the same holdout.
- Quantify ASC vs `-fconst` on one unit.
- Systematic check of the BioProject-control novelty claim before writing "first".
- `GCF_021083435_1_USA_Texas` (2021) sits in a 37-Thailand unit — our method
  predicts SE Asia. If CDC has travel history, that is free external validation.
