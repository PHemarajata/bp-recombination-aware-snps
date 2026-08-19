# A100 staging bundle — v4b panel

Everything needed to run the recombination-aware SNP workflow on the DGX Station
A100. Target: minimum hands-on time. Four commands, then it runs.

## What the box is

The `dgx_station_a100_updated` profile declares **120 cores / 480 GB**, which is
128 / 512 minus overhead — confirmed in the profile header. Note 128 is
**logical**: a DGX Station A100 is a 64-core EPYC with SMT, so Gubbins, RAxML and
IQ-TREE see ~64 real cores. `run_a100.sh` prints physical and logical counts and
warns if the box is smaller than the config assumes, before it commits.

**The GPU accelerates nothing here.** Every heavy stage is CPU. The win is cores
and RAM: the workstation ran on a 20-core / 52 GB executor budget, this is
118 / 460.

## 1. Upload from the workstation (run there, today)

    cd /home/phemarajata/Downloads/snp-mod-local-working
    rclone copy a100_stage peerah-gdrive:wfsnps-a100-v4b -P --exclude '.build/**'

**6.1 GB total** (21.58 GB of assemblies, zstd -3). Start this before you need it.

## 2. Pull on the A100

    mkdir -p ~/v4b_stage && cd ~/v4b_stage
    rclone copy peerah-gdrive:wfsnps-a100-v4b . -P
    sha256sum -c fasta.tar.zst.sha256          # must print OK
    tar -I zstd -xf fasta.tar.zst              # -> fasta/ , 2973 files, needs 22 GB free
    ls fasta | wc -l                           # must print 2973

## 3. Get the workflow repo

    cd ~ && git clone https://github.com/PHemarajata/wf-assembly-snps-mod.git
    # already cloned? make sure it is current:
    cd ~/wf-assembly-snps-mod && git pull

## 4. Run

    cd ~/v4b_stage
    DRY_RUN=1 ./run_a100.sh      # validates inputs, writes nothing heavy. ~1 min.
    ./run_a100.sh                # the real thing

Override anything via the environment if the layout differs:

    NFDIR=~/code/wf-assembly-snps-mod NFENV=nf CONDA_SH=~/miniconda3/etc/profile.d/conda.sh ./run_a100.sh

## What is in here

| path | what |
|---|---|
| `fasta.tar.zst` | all 2,973 panel assemblies, flat, named `<sample_id>.fasta`. 6.1 GB packed, 21.58 GB extracted |
| `fasta.tar.zst.sha256` | checksum, verify before extracting |
| `inputs/wf_L1v4b_samplesheet.csv` | 2,973 rows, paths as `__A100_BASE__/fasta/...` |
| `inputs/curated_L1v4b_clusters.tsv` | the 95-unit partition |
| `inputs/curated_L1v4b_refs.tsv` | 95 references, same placeholder scheme |
| `inputs/curated_L1v4b_units.tsv`, `..._assignments_all.tsv` | unit sizes, per-genome roles |
| `inputs/L1v4b_MERGED_METADATA.tsv` | panel metadata (country, origin_basis, validation_label) |
| `inputs/PANEL_EXCLUSIONS.tsv`, `PANEL_ASSEMBLY_OVERRIDES.tsv` | the exclusion register |
| `curated_L1_overrides_a100.config` | resource overrides sized for this box |
| `bin/run_wf_curated_L1.sh` | the run script, unchanged from the workstation |
| `bin/normalize_reference_headers_bp.py` | RAxML 128-char run-id guard — load-bearing |
| `bin/write_if_changed_bp.py` | keeps Nextflow's cache from being invalidated |
| `run_a100.sh` | preflight + path resolution + launch |
| `build_bundle.sh` | how `fasta.tar.zst` was made, for rebuilding |

`__A100_BASE__` is resolved in place by `run_a100.sh`, idempotently — the bundle
does not care where you extract it.

## Sizing notes

`maxForks` is deliberately generous. The executor budget (118 cores / 460 GB) is
the real cap, so a high `maxForks` lets the scheduler fill the box with whatever
mix of stages is ready. That is exactly what throttled the workstation: Gubbins
at `maxForks 3` could not use cores snippy had finished with.

Memory will bind before cores on the heavy stages — Gubbins at 24 GB × 14 forks
is 336 GB against a 460 GB budget — which is intended. Nextflow enforces it.

Expect **3–5x wall-clock**, not 6x. The floor is the critical path of the single
largest unit (n=164): its snippy → gather → Gubbins → IQ-TREE chain is serial and
no amount of forks shortens it.

## What this bundle runs: v4b minus one genome

**2,972 genomes, 95 units.** This is the panel of the workstation run in progress
with `SRR30648681` removed — a mixed sample identified after that run started
(see `inputs/PANEL_EXCLUSIONS.tsv`). Its only unit effect:

    strain_5_L1_4 (Mississippi)   23 -> 22 genomes

No unit falls below the n=7 floor, and all 95 still have a reference. So unlike
the workstation run, **every unit here is quotable, including Mississippi**.

`fasta/` holds 2,973 files; 2,972 are referenced. `SRR30648681.fasta` is present
but not in the samplesheet — harmless, and it saves rebuilding a 6.1 GB archive
to remove one file.

One thing still carries over: **`errorStrategy 'ignore'` means exit 0 does not
mean every unit succeeded.** Run `collect_L1_results.sh` before quoting any
number.

## If v4c lands first

`fasta_spades_overlay.tar.zst` (0.36 GB) holds the **165 SPAdes re-assemblies**
that would replace their SKESA counterparts — 191 delivered, minus the 3 pinned
to SKESA by `PANEL_ASSEMBLY_OVERRIDES.tsv` and the 23 excluded. Extracting it
over `fasta/` swaps them in by filename, no path changes:

    sha256sum -c fasta_spades_overlay.tar.zst.sha256
    tar -I zstd -xf fasta_spades_overlay.tar.zst     # overwrites 165 files in fasta/

Then replace three files from the v4c partition —
`inputs/curated_L1v4b_clusters.tsv`, `inputs/curated_L1v4b_refs.tsv`,
`inputs/wf_L1v4b_samplesheet.csv` — and re-run. Nothing else in the bundle is
panel-specific.

**Do not extract the overlay unless you are also swapping in a v4c partition.**
The v4b partition was built from the SKESA assemblies; mixing v4b units with
SPAdes assemblies is not a combination anything has been validated on.
