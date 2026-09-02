# QC report, the 2026-08-21 additions

**57 assemblies, 57 pass, zero exclusions, zero duplicates.**

Two sets, QC'd together so the within-batch rank check has a real denominator:

| set | n | source |
|---|---|---|
| `terra40` | 40 | TheiaProk 4.3.0 SPAdes assemblies (`/home/phemarajata/Downloads/bp_spades_assemblies_2`) |
| `mexico17` | 17 | NCBI GenBank assemblies, downloaded 2026-08-21 (`additions_mexico_2026-08-21/`) |

Script: `qc_batch3_2026-08-21.py`. Data: `BATCH3_QC_2026-08-21.tsv`,
`BATCH3_PASS_LIST.txt`. Terra metrics: `bp_2b_assembled_2.tsv`.

---

## 1. The headline: the assembler parameter took effect

**`assembler = spades`, `assembler_version = v4.1.0`, for all 40.** The known
trap, `digger_denovo` silently defaulting to SKESA, did not fire. This is the
first thing to check on any TheiaProk batch and it is now verified for this one.

## 2. Gate results

Gates unchanged from the 2026-08-17 calibration, so the two rounds are comparable.

| gate | threshold | terra40 | mexico17 |
|---|---|---|---|
| mash → K96243 | ≤ 0.012 | median **0.0058** (0.0041–0.0075) | median **0.0064** (0.0061–0.0077) |
| core coverage of K96243 | ≥ 85% | median **96.9%** (91.3–98.6) | median **97.0%** (93.9–97.8) |
| gene-count ratio | ≤ 1.20 | median **0.982** (0.942–0.994) | median **0.996** (0.975–1.022) |
| length | ≤ 7.6 Mb upper bound only | 6.97–7.33 Mb | 7.00–7.39 Mb |
| **verdict** | | **40/40 PASS** | **17/17 PASS** |

Nothing is close to a gate. The gene-count ratios cluster at 0.94–1.02 against a
K96243 calibration of 1.00; the assemblies that failed this gate in the previous
round sat at 1.35–1.67.

**BUSCO (burkholderiales_odb10, n=688), the 40 only:** Complete median **99.5%**,
minimum 95.1%; Fragmented median 0.4%, max 3.8%; Missing median 0.2%, max 1.1%.
For scale, the two ONT assemblies excluded in the last round had F+M of **4.9%
and 9.4%**. Clean coverage: median **82×**, range 57–164×.

## 3. ⚠ GAMBIT 3.0 calls every one of them *Burkholderia mallei*

`gambit_predicted_taxon = "Burkholderia mallei"` for **all 40**, at species rank,
and `kmerfinder_top_hit` agrees. **They are not *B. mallei*.**

- Cause: **GAMBIT 3.0.0 shipped with TheiaProk 4.3.0**, database
  `gambit-metadata-3.0.0-20260601` / `gambit-signatures-3.0.0-20260601`. The
  previous batch, on the older GAMBIT, called the same organism *B. pseudomallei*.
- *B. mallei* is a clonal derivative **of** *B. pseudomallei*, so the pair is
  genuinely hard to separate and the new database evidently resolves it the other
  way.
- **Refuted independently by mash:** every assembly sits **0.0041–0.0077** from
  K96243, a genuine *B. pseudomallei* reference. All 57 are below even the
  stricter 0.008 threshold. For contrast, `SRR2896271`, excluded in the last
  round as `wrong_species_or_divergent`, measured **0.0135**.

**CONFIRMED 2026-08-21 by a controlled re-run.** Same 40 assemblies, same tool
version, only the GAMBIT database changed:

| GAMBIT database | `gambit_predicted_taxon` |
|---|---|
| `2.2.0-20251111` | **B. pseudomallei 40/40** |
| `3.0.0-20260601` | **B. mallei 40/40** |

Verified same inputs: `assembly_length` matches the FASTAs on disk 40/40,
`assembler = spades` in both.

⚠ **Two corrections to what this report first claimed.**

1. **kmerfinder calls *B. mallei* under BOTH databases** (`kmerfinder_bacteria_20230911`,
   unchanged). So kmerfinder is independently wrong and always was; GAMBIT 3.0.0
   changed to agree with it. The earlier statement that kmerfinder "agreed" was
   right but incomplete: it agreed in both runs, so it is not corroboration.
2. **The downstream MLST effect was overstated.** Re-running with 2.2.0 gives
   `bcc` scheme for **1** sample, not 0. Only `SRR34776626` changed scheme
   (bpseudomallei → bcc), and its result did not change (`No ST predicted` under
   both). `SRR31683025` is on `bcc` under both databases, so its scheme is NOT
   driven by the GAMBIT call. `No ST predicted` is 8/40 under both. **The
   coupling is real but loose, and changed no results in this batch.**

The earlier 195-genome batch is consistent:

| batch | date | n | called *B. pseudomallei* | called *B. mallei* |
|---|---|---|---|---|
| previous | 2026-08-17 | 195 | **189** | **0** |
| this one | 2026-08-21 | 40 | **0** | **40** |

The old database also correctly called 1 *B. thailandensis* and left 4 at genus
level, so it was discriminating within the complex, not guessing.

**Can the database be pinned? Yes, but not from the workflow level.**
`tasks/taxon_id/task_gambit.wdl` declares them as task inputs:

```
String docker = "us-docker.pkg.dev/general-theiagen/staphb/gambit:1.0.0"
File gambit_db_genomes    = "gs://gambit-databases-rp/3.0.0/gambit-metadata-3.0.0-20260601.gdb"
File gambit_db_signatures = "gs://gambit-databases-rp/3.0.0/gambit-signatures-3.0.0-20260601.gs"
```

`wf_theiaprok_illumina_pe.wdl` passes only `assembly` and `samplename`, so these
are not surfaced as workflow inputs, but Terra's fully-qualified naming reaches
them the same way `digger_denovo.assembler` did:

```
theiaprok_illumina_pe.gambit.gambit_db_genomes
theiaprok_illumina_pe.gambit.gambit_db_signatures
```

⚠ **Note the version numbers refer to two different things.** The GAMBIT *tool*
is **v1.0.0** and did not change; the **database** is **3.0.0 (2026-06-01)**.
A bug report should name the database, not the tool.

**The previous database version, for rollback** (from the TheiaProk docs, which
still list it as the default, so the docs and `main` disagree, itself worth
mentioning to Theiagen):

```
theiaprok_illumina_pe.gambit.gambit_db_genomes    = "gs://gambit-databases-rp/2.2.0/gambit-metadata-2.2.0-20251111.gdb"
theiaprok_illumina_pe.gambit.gambit_db_signatures = "gs://gambit-databases-rp/2.2.0/gambit-signatures-2.2.0-20251111.gs"
```

**2.2.0 (2025-11-11) is almost certainly the database that produced the 189/195
*B. pseudomallei* calls on 2026-08-17.** Re-running the 40 against it is the
controlled experiment: same assemblies, same tool, only the database changes.

**How to apply:** on this GAMBIT version, `gambit_predicted_taxon` cannot be used
as the species gate for *B. pseudomallei*. Gate on **mash to K96243** and keep
GAMBIT only to catch grossly wrong organisms (it still separated the three
*B. thailandensis* runs at the target-selection stage). Do not let a reviewer or
a future session read "B. mallei" off the Terra table and conclude the panel is
contaminated.

## 4. Duplicate and register checks, both clean

The previous round shipped **13 duplicates** that were not caught until after
assembly. This round was checked before ingest:

| check | result |
|---|---|
| terra40 accession already a panel `sample_id` | **none** |
| terra40 accession matching a panel GCA/GCF stem | **none** |
| mexico17 GCA number matching a panel GCA/GCF | **none** |
| any new sample in `PANEL_EXCLUSIONS.tsv` | **none** |

⚠ **CORRECTED 2026-08-21: this check was accession-based and missed 2 duplicates.**
A BioSample-level check (`BIOPROJECT_AUDIT_2026-08-21.md` §3) finds **2 of 57 new
genomes duplicate an existing panel isolate under a different accession type**:
`SRR17029022` = `GCF_030010175_1_USA_Georgia` (`SAMN23424236`) and
`SRR34266633` = `GCF_051251265_1` (`SAMN49682048`).
**Deduplicate on BioSample, never on accession.**

## 5. The one to keep an eye on

**`SRR35159552`** is the weakest assembly on every axis: **1,638 contigs**
(batch median 410), N50 7,274 bp, core coverage 91.3%, BUSCO C=95.1% / F=3.8% /
M=1.1%.

It **passes every gate**, and by the recalibrated rules it should: fragmentation
is not the gate, because a fragmented short-read assembly loses repeat content
without losing core genome. Its gene-count ratio is **0.942**, the *lowest* in
the batch, so there is no frameshift signal, and 91.3% core coverage is well
clear of 85%.

**Keep it, flagged `marginal_fragmentation`.** Revisit only if it lands in a
small unit, where one fragmented member caps the core alignment for everyone
else. This mirrors the two `marginal_core_coverage` genomes already carried.

Five `mexico17` assemblies sit above the batch p90 gene-count ratio (0.999):
`GCA_056153345/385/425/445/465`, at 1.000–1.022. That is trivially above a
percentile, nowhere near the 1.20 gate, and expected of NCBI assemblies produced
by a different pipeline. **No action.**

## 6. What this adds

| | before | after |
|---|---|---|
| panel | 2,976 | **3,033** |
| validation (ground truth) | 31 | **44** |
| real source countries | 12 | **15** |
| Mexican reference genomes | 4 | **21** |

- **terra40** → 13 ground truth (India 6, Thailand 4, Australia 2, Trinidad and
  Tobago 1) + 27 deposit-only context (USA 19, Puerto Rico 6, Thailand 1,
  Bangladesh 1). The 27 are **panel context only and must never be scored as
  ground truth.**
- **mexico17** → all reference context. Takes Mexico from 4 references to 21,
  which is what makes the Mexico attribution test properly powered.

**Note the panel arithmetic:** 2,976 + 40 + 17 = **3,033**, not the 3,016 quoted
in `GENOME_REGISTER` §6, which counted the 40 but not the Mexican 17.

## 7. Next, and the constraint on it

Add all 57 to the **cgMLST reference pool and re-score attribution, Phase 1.**
cgMLST needs no unit assignment, so this invalidates nothing.

**Do not re-partition.** Putting these into the SNP/unit analysis is Phase 2 and
invalidates every unit, r/m value, distance table and tree.
