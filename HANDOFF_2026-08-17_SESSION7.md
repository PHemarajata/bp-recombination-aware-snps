# Session handoff — 2026-08-17 (session 7)

Supersedes `HANDOFF_2026-08-16_SESSION6.md` for the additions work; session 6's
partition/run content still stands. This session: validated v3 end to end,
re-exported deliverables, and triaged the contextual-genome additions down to
runnable per-sample settings.

---

## §0 THE PATTERN — now seven instances

Every real defect across sessions 6-7 produced **plausible output from a silent
mismatch**, and was caught only by checking raw per-item values:

| looked fine | actually |
|---|---|
| 1,784 BioSample records | NCBI efetch stripped `SAMEA` prefix, returned **a human cell line**; 61% wrong organism |
| one documented size rule | `min_cluster_size` applied **twice**, discarding 732 genomes |
| my merge rule, summary stats fine | inflated a clonal unit's diameter 8x — visible only per-unit |
| phylogeography "21 of 40 clustered" | `--trees` silently defaulted to **v1** output |
| 23 assemblies, all downloaded | 5 were 7.7-8.1 Mb / 4,067 contigs — contaminated |
| "genome length 21-66 Mb" | oversequencing artefact at 200-1200x, **not** contamination |
| "read file is empty" | nanoq Q10 filter deleting 100% of PacBio CLR reads |

**Diff requested vs returned. Check per-item, not per-summary.**

---

## §1 STATE

- **Nothing running.** Local disk ~217 GB free; TB1 698 GB free.
- Pipeline `~/wf-assembly-snps-mod`: `main` at **`79ab645`**, pushed.
- **Current results: `L1v3_out/` — 91 units, 2,282 genomes, 182/182 Tier1.**
- Exported: `/media/phemarajata/TB1/snp_archive/snp_results_2026-08-16_v3/`
  (763 files, 30 MB). Old 82-unit export carries `SUPERSEDED.txt`.
- `export_deliverables_bp.sh` is now **`PART`-aware**: `PART=v3 ./export...`
  (`PART=v1` still reproduces the original).

## §2 v3 IS VALIDATED — `V3_RUN_RESULTS.md`

1. **61/61 unchanged units reproduce v1 r/m to within 0.01.** In-pipeline
   `POOL_RECOMBINATION_STATS` is byte-faithful to the script it replaced.
2. **r/m 6.30 -> 4.87 is compositional:** unchanged 6.20, merged 4.44, new 1.77.
   **QUOTE THE CLEAN SUBSET, NOT THE 91-UNIT MEDIAN.**
3. **Manual validation holds** for the 50 manual-matched unchanged units.

**Standing caveat:** 29 of 91 units carry a >=1,000-substitution surviving
branch. Filter on `max_kept_branch_len` before any biological r/m claim.

**Global tree:** strain_9 still holds the **longest internal branch**
(0.09549, 100/100) and now has **three** units — `strain_9_L1_7` crossed the
threshold and contains **four untravelled mainland-US cases** (TX x2, CA x2)
with two Ecuadorian isolates from 1960-62. Mainland-US genomes 11 -> 15.
`strain_9_L1_4`, `strain_9_L1_5`, `strain_20_L1_1` are byte-identical to v1.

---

## §3 THE ADDITIONS — 234 genomes, fully triaged

`GENOME_ADDITIONS_PROPOSAL.md` · `ADDITIONS_MANIFEST.tsv`

| bucket | n | location / state |
|---|---|---|
| assemblies pulled, QC-passed | 18 | `additions/fasta/` (17 Mexico + 1 Philippines) |
| **need assembly (external)** | **205** | `SRA_TO_ASSEMBLE.tsv`, `SRA_accessions.txt` |
| quarantined (contaminated) | 5 | `additions/quarantine/` — Malaysian, 8 Mb, gastric biopsy |
| dropped (no data anywhere) | 6 | 3 Colombia, 3 Malaysia |

### `SRA_TO_ASSEMBLE.tsv` is now fully annotated (205 rows)

Columns include measured `read_count`, `base_count_Mb`, `coverage_7.2Mb`,
`verdict`, `rescue_note`, plus `origin_country` / `origin_basis` and platform.

| verdict | n | meaning |
|---|---|---|
| `ok` | 131 | assemble at defaults |
| `ok_downsample` | 65 | >150x — rasusa first (`RASUSA_JOBS.tsv`) |
| `assemble_pacbio` | 5 | PacBio CLR — special settings |
| `marginal` | 1 | `SRR28096031` 6.1x — QC hard |
| `drop` | 3 | `SRR28096040` 1.5x, `SRR28096047` 3.6x, `SRR32459445` 4.2x |

Platform: **192 Illumina, 5 PacBio RS II (CLR), 5 ONT, 3 CDC MiSeq** (the last
resolved via NCBI; ENA has not mirrored them).

**All 25 of the Terra failures are within these 205** — none are outside samples.

---

## §4 WHY THE TERRA ASSEMBLIES FAILED — all diagnosed, see `THEIAPROK_SETTINGS.md`

Five classes, **23 of 25 rescuable**, none contamination:

1. **"genome length 21-66 Mb too large" (16)** — all **Illumina at 200-1200x**.
   The mash k-mer estimator inflates with error k-mers at extreme depth. The
   deepest-sequenced samples, rejected for being too good.
2. **PacBio CLR wiped by read cleaning (5)** — `nanoq_min_read_qual` defaults to
   **10** (Q10 = 90%); RS II CLR is ~85-88% (Q8-9), so **every read is deleted**.
   Raw PASS, clean FAIL "empty read file".
3. **R1/R2 imbalance 66/34 (2)** — harmless; R1 longer than R2.
4. **Marginal coverage 9 vs 10 (1)** — `SRR2896258`.
5. **Genuinely too shallow (2)** — drop.

### Two corrections to earlier advice (from the real Terra input table)

- **ONT already skips the genome-length screen** (`skip_mash = true`,
  `max_genome_length`/`min_genome_length`/`min_coverage` all "skipped by
  default"). Only `min_reads` (5000) and `min_basepairs` are live there.
  `max_genome_length = 75000000` applies to **Illumina_PE only**.
- **The assembler task is `flye_denovo`, not `flye`**, and its
  `polisher` defaults to **medaka** — ONT-specific. For PacBio use **racon**.

### PacBio: do NOT use hifiasm

The Broad `PBAssembleWithHifiasm` requires **HiFi (CCS) >99% accuracy**. These
are **RS II CLR** — confirmed by instrument model, `WGS/RANDOM` library, variable
read lengths (5.4-17.7 kb), and by the fact that a Q10 filter removed 100% of
reads. Use Flye `--pacbio-raw` (TheiaProk_ONT with the settings in
`THEIAPROK_SETTINGS.md`, or standalone `flye --pacbio-raw --genome-size 7.2m`).

---

## §5 ORIGIN ATTRIBUTION — the rule for merging anything new

`Country_Final` in the curated metadata is **country of probable ORIGIN**, not
isolation: all 17 travel cases attribute to acquisition (`USA: TX ex Nigeria` ->
Nigeria), never to the diagnosing country. **ENA's `country` is ISOLATION.**

`SRA_TO_ASSEMBLE.tsv` carries both: `ena_country` as retrieved and
`origin_country` with any `ex <country>` already parsed. **Merge on
`origin_country`.** 16 of the 205 are travel-reattributed.

Two genomes have non-single-country origin — `GCF_002111305_1`
("Panama and Peru") and `GCF_002113945_1` ("Africa"). Add an
`origin_resolution` column (`country` / `multi_country` / `region` / `unknown`)
and exclude non-`country` from country statistics. Keep them in the tree — they
are constrained test cases whose placement may resolve the ambiguity.

Also: 11 genomes are **laboratory stock** (`ISOLATION_SOURCE_2026-08-16.tsv`) —
their "country" is where the lab sits. Exclude from country statistics.

---

## §6 WHEN THE ASSEMBLIES COME BACK

1. QC every assembly: **7.0-7.4 Mb**, sane contig count. This is the control that
   works — it caught the 5 contaminated Malaysian genomes.
2. Merge on `origin_country`; carry platform through; exclude the quarantined 5.
3. Re-partition (`build_L1_partition_bp.py`, merge-not-delete is now default),
   regenerate references, re-run, re-export as the next `PART`.
4. Targets: `strain_9_L1_2` (Mississippi, n=5) and `strain_9_L1_8` (Mexico, n=6)
   are assign-only and are what the additions are meant to rescue. **T0 priority
   is the 18 Mississippi** — PRJNA942243 holds 23, we have 5; the rest take that
   unit to n=23. It is the best case-to-environment linkage in the collection
   (2 clinical + 3 environmental from the Petras 2023 NEJM investigation).
5. Only then is the **CDC validation set** scorable — most of those 24
   ground-truth `ex <country>` cases are themselves among the 205.

---

## §7 TRAPS (cumulative)

- **NCBI efetch mangles SAMEA/SAMD** — use ENA; assert requested == returned.
- **`phylogeography_association_bp.py --trees` defaults to `L1_out/Clusters`** —
  repoint `--assignments` AND `--trees` together.
- **`export_deliverables_bp.sh` is `PART`-aware** — do not hardcode filenames again.
- **TB1 root is `root:root`** — new top-level dirs need sudo; exports go to
  `snp_archive/`.
- **Editing a running bash script corrupts it** (bash re-reads by byte offset).
- **`-resume` bug FIXED** in `run_wf_curated_L1.sh` (was duplicating the session id).
- **Terra: a mistyped input prefix is silently ignored.** Verify
  `flye_denovo.` / `read_QC_trim.` names against what Terra displays.

---

## §8 KEY FILES

| file | what |
|---|---|
| `V3_RUN_RESULTS.md` | v3 validation, the three checks |
| `L1_PARTITION_V2.md` | the double-size-filter fix, merge rule |
| `INTERPRETATION_2026-08-16.md` | strain_9, Georgia vs Mississippi, r/m, isolation source |
| `THEIAPROK_SETTINGS.md` | **per-platform Terra settings** |
| `READ_SCREEN_RESCUE.md` | the 25 failures, by class |
| `SRA_TO_ASSEMBLE.tsv` | 205 accessions, annotated with verdicts |
| `RASUSA_JOBS.tsv` | the 65 needing downsampling |
| `ADDITIONS_MANIFEST.tsv` | all 234 |
| `curated_L1v3_*` | the v3 partition |
