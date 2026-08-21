# GitHub issue, ready to paste

**Repo:** `theiagen/public_health_bioinformatics` → New issue → **Bug Report**

**Title:**

```
GAMBIT database 2.2.0 -> 3.0.0 flips B. pseudomallei to B. mallei on 40/40 identical assemblies
```

Everything below the line is the body. Follows the repo's `bug-report.md` template.

---

:bug:

### :pencil: Describe the Issue

Running the same 40 *Burkholderia pseudomallei* assemblies through TheiaProk 4.3.0 twice, changing **only** the GAMBIT database, flips the species call on every genome:

| GAMBIT database | `gambit_predicted_taxon` | rank |
|---|---|---|
| `2.2.0-20251111` | **Burkholderia pseudomallei** 40/40 | species |
| `3.0.0-20260601` | **Burkholderia mallei** 40/40 | species |

GAMBIT tool version is `staphb/gambit:1.0.0` in both runs. The assemblies are byte-identical (verified: `assembly_length` matches the FASTAs on disk 40/40, `assembler = spades` in both). The database is the only variable.

This is consistent with an earlier batch from the same lab: 195 genomes on the older database returned *B. pseudomallei* for 189, *B. mallei* for 0, and correctly identified one *B. thailandensis*.

#### Evidence these are *B. pseudomallei*

| check | result |
|---|---|
| Mash to K96243 (`-s 10000 -k 21`) | **0.0041 to 0.0077** (all 40) |
| Core coverage of K96243 (minimap2 `asm10`, MAPQ≥10) | **91.3 to 98.6%**, median 96.9% |
| BUSCO `burkholderiales_odb10` (n=688) | Complete median **99.5%**, min 95.1% |
| Distinct 7-locus STs | **22** (incl. ST92, ST70, ST297, ST369) |
| BioProjects / countries | 3 / 4 |

For calibration, a genome we previously excluded as wrong-species measured **0.0135** to K96243. Everything here is 2 to 3x closer. The 22 STs across 3 BioProjects show this is not one unusual clade. Most are CDC-deposited melioidosis case investigations.

#### kmerfinder calls *B. mallei* under both databases

`kmerfinder_top_hit = "Burkholderia mallei"` for all 40 in **both** runs, on an unchanged database (`kmerfinder_bacteria_20230911`).

So the two identifiers previously disagreed, with GAMBIT giving the answer that matches mash, ANI-style core coverage, and MLST. On 3.0.0 they now agree with each other on the call our orthogonal evidence contradicts. Whether that is coincidence or a shared reference-set issue, we can't say from our data.

#### Minor downstream effect

`ts_mlst` takes its scheme from the GAMBIT call:

```wdl
taxonomy = select_first([expected_taxon, gambit.gambit_predicted_taxon]),
```

The effect here was small and we want to be accurate about it. Comparing the two runs:

| | GAMBIT 2.2.0 | GAMBIT 3.0.0 |
|---|---|---|
| `ts_mlst_pubmlst_scheme = bpseudomallei` | 39 | 38 |
| `ts_mlst_pubmlst_scheme = bcc` | 1 | 2 |
| `No ST predicted` | 8/40 | 8/40 |

Only **one** sample (`SRR34776626`) changed scheme, from `bpseudomallei` to `bcc`, and its result did not change (`No ST predicted` either way). `SRR31683025` is assigned `bcc` under **both** databases, so its scheme selection is not driven by the GAMBIT taxon.

So the coupling exists but is loose, and in this batch it changed no results. Flagging it only because the mechanism means a taxon error *can* reach downstream typing.

#### Why we're raising it

This is a genuinely hard pair. *B. mallei* is a clonal derivative of *B. pseudomallei*, and separating them from assembly data is a real problem, not a careless one.

The reason it seems worth a look is the asymmetry of consequence for public health labs. Both organisms are HHS/USDA Tier 1 Select Agents, so **this does not move anything into or out of regulation**. But melioidosis is an expected US finding, now endemic on parts of the Gulf Coast, while glanders is essentially absent from the Western Hemisphere. A *B. mallei* call on a US isolate is an extraordinary result that would trigger a much larger and different response than melioidosis. In the other direction, a lab trusting the call would report the wrong disease.

#### Scope of what we tested

*B. pseudomallei* only, n=40. **We have not tested whether GAMBIT 3.0.0 still identifies true *B. mallei* correctly**, and we have not looked at other taxa. We cannot say whether this is specific to this species pair or broader.

#### Two smaller observations

1. **Docs and `main` disagree on the default.** The input documentation lists `gs://gambit-databases-rp/2.2.0/gambit-metadata-2.2.0-20251111.gdb` for `gambit_db_genomes`, while `tasks/taxon_id/task_gambit.wdl` on `main` has the 3.0.0 paths. That may be why the change wasn't obvious.
2. **Database inputs aren't exposed at workflow level.** `wf_theiaprok_illumina_pe.wdl` passes only `assembly` and `samplename` to the `gambit` task, so pinning requires the fully qualified `theiaprok_illumina_pe.gambit.gambit_db_genomes`. Surfacing them as workflow inputs would make rollback easier.

### :repeat: How to Reproduce

Run `theiaprok_illumina_pe` on any *B. pseudomallei* Illumina PE read set and read `gambit_predicted_taxon`. Then re-run with the 2.2.0 database pinned and compare.

Public accessions from our batch that reproduce it:

```
SRR16343583  SRR16344669  SRR17029022  SRR31682036  SRR31683025
SRR31696406  SRR31760806  SRR31976171  SRR32012546  SRR34776626
```

Database pin used for the 2.2.0 arm:

```
theiaprok_illumina_pe.gambit.gambit_db_genomes    = "gs://gambit-databases-rp/2.2.0/gambit-metadata-2.2.0-20251111.gdb"
theiaprok_illumina_pe.gambit.gambit_db_signatures = "gs://gambit-databases-rp/2.2.0/gambit-signatures-2.2.0-20251111.gs"
```

<details>
<summary>Other non-default inputs we set</summary>

```json
{
  "theiaprok_illumina_pe.genome_length": 7247547,
  "theiaprok_illumina_pe.digger_denovo.assembler": "spades",
  "theiaprok_illumina_pe.digger_denovo.filter_contigs_min_length": 500,
  "theiaprok_illumina_pe.call_kmerfinder": true,
  "theiaprok_illumina_pe.call_ani": false,
  "theiaprok_illumina_pe.call_plasmidfinder": false,
  "theiaprok_illumina_pe.call_abricate": false,
  "theiaprok_illumina_pe.call_gamma": false,
  "theiaprok_illumina_pe.call_resfinder": false,
  "theiaprok_illumina_pe.call_arln_stats": false,
  "theiaprok_illumina_pe.merlin_magic.run_amr_search": false
}
```

`expected_taxon` was deliberately left **unset**, so GAMBIT's call was not overridden.

</details>

### :computer: Version Information

| component | version |
|---|---|
| TheiaProk | **4.3.0** (`theiaprok_illumina_pe`) |
| GAMBIT tool | `staphb/gambit:1.0.0`, **identical in both runs** |
| GAMBIT database, run A | `gambit-metadata-2.2.0-20251111.gdb` / `gambit-signatures-2.2.0-20251111.gs` |
| GAMBIT database, run B | `gambit-metadata-3.0.0-20260601.gdb` / `gambit-signatures-3.0.0-20260601.gs` |
| kmerfinder database | `kmerfinder_bacteria_20230911`, identical in both runs |
| BUSCO | 5.7.1, `burkholderiales_odb10 (2024-01-08)` |
| assembler | SPAdes v4.1.0 via `digger_denovo` |
| platform | Terra |

**Only the GAMBIT database differed between the two runs.**

Happy to share the 40 assemblies or the full Terra data tables. Thanks for TheiaProk, it's been a workhorse for us.
