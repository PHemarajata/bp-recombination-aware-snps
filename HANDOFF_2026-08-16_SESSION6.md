# Session handoff — 2026-08-16 (session 6)

Supersedes `HANDOFF_2026-08-16_SESSION5.md`. Session 5 finished the 82-unit run
and asked for interpretation. This session did that, found the interpretation was
resting on a partition that discarded 26% of the collection, fixed it, re-ran,
and staged a contextual-genome expansion.

---

## §0 THE PATTERN, AGAIN — five more instances

Every real defect this session produced **output that looked entirely
reasonable** and was caught only by checking raw per-item values against what
they should have been:

| what it looked like | what it was |
|---|---|
| a clean BioSample table, 1,784 records | NCBI efetch stripped the `SAMEA` prefix and returned **a human cell line** at HTTP 200; 61% of records were the wrong organism |
| `min_cluster_size = 7`, one documented rule | applied **twice** — to PopPUNK strains AND fastbaps subclusters — discarding 732 genomes |
| my merge rule, summary stats fine | inflated `strain_1_L1_3` from diameter 0.00047 to 0.00385 (8x) — visible only per-unit |
| phylogeography: "21 of 40 clustered" | `--trees` silently defaulted to **v1** output; joined v3 assignments to v1 trees |
| 23 assemblies downloaded, all sized | 5 were 7.7-8.1 Mb across 2,126-4,067 contigs — contaminated gastric-biopsy isolates |

**Diff requested against returned. Check per-item, not per-summary.**

---

## §1 STATE

- **Nothing running.** Local disk 217 GB free; TB1 698 GB free.
- Pipeline `~/wf-assembly-snps-mod`: `main` at **`79ab645`**, pushed. Two new
  commits this session (r/m in-pipeline, IQTREE_FAST gate).
- **Current results: `L1v3_out/` — 91 units, 2,282 genomes, 182/182 Tier1.**
- Exported to `/media/phemarajata/TB1/snp_archive/snp_results_2026-08-16_v3/`.
  The old 82-unit export carries `SUPERSEDED.txt`.

---

## §2 THE PARTITION WAS THE PROBLEM (§12 of INTERPRETATION, L1_PARTITION_V2.md)

`min_cluster_size = 7` was applied to PopPUNK strains **and again** to fastbaps
L1 subclusters. fastbaps exists to *subdivide* strains, so the second
application discarded **60% of L1 units by construction** — 732 of 2,802
genomes (26.1%), biased hard against rare lineages:

    Singapore 0% lost · Thailand 16.8% · USA 41.7% · Australia 74.1% · India 94.6%
    **51% of every Americas genome in the collection**

For origin attribution that is the worst possible bias: a rare imported lineage
IS a small subcluster.

**FIXED.** `build_L1_partition_bp.py` now merges sub-threshold units into their
nearest sibling under two clauses — gap <= receiver diameter, AND merged
diameter <= a ceiling calibrated as the p90 of naturally-formed units. What
cannot merge is retained as `role=assign_only`, never deleted.
`--no-merge` reproduces the old behaviour exactly (verified before changing
anything). `--absorb-subthreshold-strains` handles the PopPUNK floor too.

    v1  82 units  2,070 genomes   732 deleted
    v3  91 units  2,282 genomes     0 deleted, 517 assign-only

---

## §3 v3 IS VALIDATED — see V3_RUN_RESULTS.md

1. **61/61 unchanged units reproduce v1 r/m to within 0.01.** The in-pipeline
   `POOL_RECOMBINATION_STATS` is byte-faithful to the script it replaced.
2. **r/m 6.30 -> 4.87 is compositional**: unchanged 6.20, merged 4.44, new 1.77.
   **QUOTE THE CLEAN SUBSET, NOT THE 91-UNIT MEDIAN.**
3. **Manual validation holds** for the 50 manual-matched unchanged units.

**Coherence is the standing caveat:** 29 of 91 units carry a >=1,000-substitution
surviving branch (was 20 of 82). Merging did not fix the divergent-member
problem — filter on `max_kept_branch_len` before any biological r/m claim.

---

## §4 INTERPRETATION — INTERPRETATION_2026-08-16.md

- **strain_9 holds the longest internal branch in the tree** (0.09549, 100/100),
  independently recovering the Western Hemisphere clade. Now **three** units:
  `strain_9_L1_7` crossed the threshold in v3 and contains **four untravelled
  mainland-US cases** (TX x2, CA x2) with two Ecuadorian isolates from 1960-62.
- **The two US endemic foci are genetically distinct**: Georgia
  (`strain_20_L1_1`, Vietnam-linked, Brennan 2025 EID) vs Mississippi
  (`strain_9_L1_2`, Caribbean clade, Petras 2023 NEJM). Both recovered without
  the method seeing any geography.
- **`country` hides US territories** — 10 of 21 "USA" genomes are PR/USVI.
  Use `subregion`. `Country_Final` is ORIGIN (17/17 travel cases attributed to
  acquisition, never isolation).
- **Isolation source now known for 99.3%** (`ISOLATION_SOURCE_2026-08-16.tsv`).
  `IP-` = patient, `IE-` = environmental (Burk-Genome, Nakhon Phanom). 11 genomes
  are laboratory stock and must be excluded from country statistics.

---

## §5 ADDITIONS — STAGED, BLOCKED ON EXTERNAL ASSEMBLY

`GENOME_ADDITIONS_PROPOSAL.md`, `ADDITIONS_MANIFEST.tsv` (234 genomes).

| bucket | n | where |
|---|---|---|
| assemblies pulled, QC-passed | 18 | `additions/fasta/` (17 Mexico + 1 Philippines) |
| **need external assembly** | **205** | `SRA_accessions.txt`, `SRA_TO_ASSEMBLE.tsv` |
| quarantined (contaminated) | 5 | `additions/quarantine/` — Malaysian, 8 Mb, gastric biopsy |
| dropped (no data anywhere) | 6 | 3 Colombia, 3 Malaysia |

Platform: 192 Illumina, 5 PacBio, 5 ONT (**all 10 Ghana are long-read**; the 5
ONT need Medaka polishing), 3 unknown.

**T0 priority is Mississippi**: PRJNA942243 holds 23 samples, we have 5. The
other 18 take `strain_9_L1_2` from n=5 (assign-only) to n=23. It is the best
case-to-environment linkage in the collection — 2 clinical + 3 environmental
from the NEJM investigation, the patient's own property sampled.

**Philippines: 12 of 13 public genomes ARE the CDC validation set.** Use as a
proxy panel, NEVER as reference data — that would be circular.

### When the 205 come back
1. Merge on `origin_country` (never `ena_country` — ENA gives isolation).
   Carry platform through. Exclude the quarantined 5.
2. Re-partition, re-run, re-export (`PART=v3` -> next generation).
3. Then the CDC validation set becomes scorable — most of those 24 cases are
   themselves in the 205.

---

## §6 TRAPS ADDED THIS SESSION

- **NCBI efetch mangles SAMEA/SAMD accessions** — strips the alpha prefix,
  resolves the digits as a UID, returns a different sample at HTTP 200. **Use
  ENA** (`ebi.ac.uk/ena/browser/api/xml/`) and assert requested == returned.
- **`phylogeography_association_bp.py --trees` defaults to `L1_out/Clusters`.**
  Repoint `--assignments` AND `--trees` together or you silently mix generations.
- **`export_deliverables_bp.sh` is now `PART`-aware** (`PART=v1|v3`). Do not
  hardcode filenames into it again.
- **TB1 root is `root:root`** — new top-level dirs need sudo. Exports go to
  `snp_archive/`.
- **Editing a running bash script corrupts it** (bash re-reads by byte offset).
  The `run_wf_curated_L1.sh` resume-flag fix waited for the run to finish.

---

## §7 WHAT IS ACTUALLY LEFT

Nothing is blocked except on the external assembly. Open items:

1. **Assemble the 205** (external), then the additions round above.
2. `strain_9_L1_2` (Mississippi n=5) and `strain_9_L1_8` (Mexico n=6) stay
   assign-only until then — they are what the additions target.
3. **Score the CDC validation set** once its members are analysable.
4. The 407 below the PopPUNK strain floor are retained as
   `role=below_strain_floor` but only 17 became analysable — they are 229
   genuinely distinct lineages, mostly singletons, not recoverable data.
