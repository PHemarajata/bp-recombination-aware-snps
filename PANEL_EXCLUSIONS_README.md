# Panel exclusion register

`PANEL_EXCLUSIONS.tsv` — every sample excluded from the analysis panel, with the
reason and the evidence that supports it. `PANEL_ASSEMBLY_OVERRIDES.tsv` — samples
that are **kept**, but where a specific assembly must be used instead of the
newest one.

Both are machine-readable and should be the single source of truth. Do not
re-derive exclusions by hand; add a row here instead.

## Columns

`PANEL_EXCLUSIONS.tsv`: `sample_id`, `batch`, `reason_class`, `reason`,
`evidence`, `decided`, `status`, `action`.

`PANEL_ASSEMBLY_OVERRIDES.tsv`: `sample_id`, `use_assembler`, `use_path`,
`reject_assembler`, `reason`, `evidence`.

## Current contents — 46 excluded samples

| reason_class | n | what it means |
|---|---|---|
| duplicate | 13 | same SRA run already held as a v3 SPAdes assembly; the v3 copy is retained |
| wrong_species_or_divergent | 7 | gambit/mash say not *B. pseudomallei*, or grossly divergent |
| no_data | 6 | no assembly and no reads in ENA or NCBI |
| assembly_failure | 5 | PacBio RS II CLR; no usable assembly is obtainable |
| contaminated | 5 | Malaysian, 7.7–8.1 Mb over 2,126–4,067 contigs; 3 gastric biopsy |
| read_screen_fail | 5 | failed TheiaProk read screening before assembly |
| broken_assembly | 4 | core coverage <85% of K96243, or gene-count ratio >1.20 |
| mixed_sample | 1 | SPAdes assembled ~12 Mb at good contiguity, and SKESA does not rescue it either |

Note these are **not** the same as `assign_only` genomes. Assign-only genomes are
in the panel and on the trees; they are simply in units below n=7 and so carry no
r/m estimate. Nothing is deleted for being assign-only — see
`curated_L1v4b_assignments_all.tsv`.

## Assembly overrides — 3 samples

`SRR28096032`, `SRR28096062` and `SRR30648682` use their **SKESA** assemblies, not SPAdes.

`SRR28096032` and `SRR28096062` are one case. SPAdes collapsed both to ~4.3 Mb
across ~5,600 contigs with a longest contig
under 2.8 kb. The SPAdes log shows the run completed normally — all four k-mer
passes, clean exit, 3.1 GB peak against a 16 GB limit — so it is not a resource
or truncation failure. The cause is in the library:

    WARN  Estimated mean insert size 145.604 is very small compared to read length 151
    WARN  Too many erroneous kmers, the estimates might be unreliable

The insert is shorter than the read, so pairs fully overlap and read through into
the adapter. That removes any pairing span beyond ~145 bp and generates the
erroneous k-mers flagged at every K. Compounding it, `digger_denovo` runs SPAdes
with `--only-assembler` (`Mode: ONLY assembling (without read error correction)`),
so BayesHammer never runs. SKESA tolerates this failure mode and produced
6.96 / 6.95 Mb at N50 7.8 / 7.5 kb.

**This is a property of the reads, not of the settings.** Do not re-run these two
with more memory or different SPAdes options.

`SRR30648682` is a different case. SPAdes assembled it at 11.88 Mb with good
contiguity (N50 18,894), exposing foreign content — but its SKESA assembly is
7,096,979 bp / 1,235 contigs and passes **every** gate (mash 0.0072, core 92.2%,
gene-count ratio 0.96), so SKESA suppressed the contaminant cleanly. The SKESA
assembly is therefore used and the sample is kept.

Its neighbour `SRR30648681` looks like the same case and is not. There SKESA gives
**7,941,716 bp — 540 kb over the 7.4 Mb upper bound — at mash 0.0099**, above the
0.008 gate and against a batch median near 0.006. The contaminant survives under
both assemblers, so no assembly of it is trustworthy and it stays excluded. The
two were separated on measurement, not on the fact that both looked inflated
under SPAdes.

## Open item: one exclusion is inside the running v4b pipeline

`SRR30648681` was accepted at v4b build time and only shown to be a mixed sample
afterwards, by the SPAdes re-assembly. It is in the panel of the run started
2026-08-17, in **`strain_5_L1_4` — the Mississippi unit** (n=23, 22 USA +
1 Colombia).

Consequences:

- The unit survives its removal at n=22, well above the floor of 7.
- **Do not quote r/m, recombination or diversity for `strain_5_L1_4` from this
  run.** One mixed-sample genome is in it, and foreign content inflates exactly
  those statistics.
- Every other unit is unaffected — the cross-check confirms this is the only
  excluded sample present in the panel.

It drops out automatically at the next re-partition, which is due anyway once
the SPAdes batch is QC'd.

## Applying the register

    python3 - <<'PY'
    import csv
    # HONOUR `status`. A row with status=retired is a RESCINDED decision kept
    # for the record, NOT an active exclusion. Reading the register without this
    # filter re-applies exclusions that were withdrawn on evidence.
    excl = {r['sample_id'] for r in csv.DictReader(open('PANEL_EXCLUSIONS.tsv'), delimiter='\t')
            if r.get('status') != 'retired'}
    over = {r['sample_id']: r['use_path']
            for r in csv.DictReader(open('PANEL_ASSEMBLY_OVERRIDES.tsv'), delimiter='\t')}
    # drop excl from any candidate set; prefer over[sid] as the assembly path
    PY

Cross-check to run before every panel build — **both lines, not just the first**:

    ACTIVE excluded samples present in the panel      ->  must be 0
    ACTIVE excluded samples in the cgMLST ref pool    ->  must be 0

⚠ **The second line was missing until 2026-08-23, and its absence hid a real
defect for weeks.** The partition was clean, so `freeze_basis_bp.py` passed every
check while all four then-active exclusions sat in
`cgmlst_lichtenegger/MANIFEST.tsv` — the pool every attribution call searches.
**A genome excluded from the analysis can still decide a call as a reference**,
and one of the four was the nearest neighbour of a validation genome. Both lines
are now enforced by `freeze_basis_bp.py`.

## `status` — the retirement mechanism (added 2026-08-23)

| status | meaning |
|---|---|
| `final` | active exclusion. Drop the sample. |
| `retired` | **rescinded.** The sample is a normal panel member. The row is kept so the register records that a decision was made *and was wrong*. |

Retire with `retire_exclusions_bp.py` (idempotent, and the replayable record —
`*.tsv` is gitignored, so a hand edit is invisible to git). Never delete a row.

Four rows are currently retired: `SRR2896257`, `SRR2896259`, `ERR9980356`,
`SRR2896271`. See `EXCLUSION_RECHECK_2026-08-23.md`.

## ⚠ Transcription trap: `core=na%` in NEW200-sourced rows

Every row whose `evidence` is `NEW200_QC_2026-08-17.tsv` reads `core=na%`. **The
core coverage was measured.** It is in `core_cov_unfiltered_pct`; the register
transcribed the adjacent `core_cov_filtered_pct`, which is **empty for every row
in that file**. Any future row sourced from that QC table must read
`core_cov_unfiltered_pct`.

This mattered: four rows were excluded citing a core gate whose value the row
did not carry, and on the SPAdes assemblies actually in use all four pass it.
One further row, `SRR28096031`, has the same empty `core` field but its exclusion
is genuinely supported by `ratio = 1.35` — only its *reason string* is imprecise.

⚠ **`0.008` is not the operative mash gate.** It appears in this README and in
`BATCH3_QC_REPORT_2026-08-21.md` as prose. The threshold enforced in code
(`reqc_spades_batch.py`) is **≤ 0.012**. Do not exclude a genome for exceeding
0.008 and describe it as failing a gate.
