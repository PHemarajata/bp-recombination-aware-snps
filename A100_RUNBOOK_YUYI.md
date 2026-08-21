# A100 runbook — ClonalFrameML on the v4c units

> ## STATUS 2026-08-21 — Job 1 is WORTH DOING if you have time. Job 2 is done.
>
> **Job 1 (ClonalFrameML) is also running on the workstation right now**, but
> slowly: 22 cores, ~16 replicon-units per hour, so ~10 hours for all 176. The
> A100 has ~3× the cores and should finish in 3–4 hours. **If you have time,
> please run it — we will use whichever finishes first.**
>
> There is **no collision risk**: your outputs land on the A100, the local ones
> stay here. Where the two overlap they become a hardware-reproducibility
> control, which is a result in its own right — same inputs, different machine,
> do R/θ, δ and ν agree?
>
> **Please message Peera when you start**, so the local run can be stopped and
> the cores freed.
>
> **Job 2 (two missing units) — DONE, skip it.** `strain_1_L1_36` and
> `strain_1_L1_37` were recovered from Drive on 2026-08-21. Their `.core.tab`
> and Gubbins GFFs were there all along; only the 90 MB alignments were missing,
> and the distance work does not use those.
>
> ### If you already downloaded anything, RE-PULL THESE TWO FILES
>
> Both were fixed on 2026-08-21 **after** the first version went out. The data
> files (alignments, Clusters, Summaries) are unchanged — do not re-download
> those.
>
> ```bash
> cd ~/v4c_cfml
> rclone copy gdrive_ph:wfsnps-v4c-results/clonalframe_nu_bp.py . -P
> rclone copy gdrive_ph:wfsnps-v4c-results/A100_RUNBOOK_YUYI.md . -P
> ```
>
> Confirm you have the new driver — this must print a line, and prints nothing
> for the old one:
>
> ```bash
> grep -c CFML_CONDA_SH clonalframe_nu_bp.py     # expect 1 or more, NOT 0
> ```
>
> If it prints `0`, rclone kept the stale copy: `rm clonalframe_nu_bp.py` and
> re-run the copy.
>
> ### What changed, and why the old version could not have worked
>
> 1. **Conda paths and env names were hardcoded to the originating workstation**
>    (`/home/phemarajata/miniforge3`, envs `cfml` / `bp-gubbins` /
>    `snp-phylogeny`). None exist on the A100, so every unit would have died at
>    `conda activate` no matter what you installed. Now overridable — see §1.2.
> 2. **The driver called `iqtree2` specifically**, and the A100's iqtree env
>    provides only `iqtree`. That failed *after* snp-sites had already run. It
>    now resolves whichever name exists.
> 3. **A v4c layout bug** — it silently resolved the *old* partition's file paths
>    under `--layout v4c`, i.e. ran the wrong data without erroring.
> 4. **The alignments were not on Drive** when this document first went out, so
>    §2.1 could not have completed. All 172 are uploaded and verified now.
>    **Still check §2.1 step 0 first** — the A100 may hold its own copies, which
>    saves the 17 GB download entirely.

**For:** Yuyi. **Written:** 2026-08-20. **Contact:** Peera (away until ~2026-08-27).

Self-contained: you do not need any history with this project. **One job** —
§2. Read §0 and the trap table in §4 before starting; several of the failure
modes here look like success, or like a different problem than they are.

---

## 0. What you are doing and why it matters

We split ~2,900 *Burkholderia pseudomallei* genomes into 86 "units" and ran
Gubbins on each to strip recombination before building trees. Gubbins reports one
number per unit, **r/m**, and that number is currently the *sole* gate deciding
which units are usable.

On an **older** partition we ran a second tool, ClonalFrameML, over 46 units and
compared. The two tools **disagree about which units are good**: rank correlation
+0.30, and **8 of 46 units flip accept/reject** depending on which tool you ask.
If that holds, the acceptance gate is tool-dependent — a finding about the
method, not about those units.

**Job 1 is to find out whether it holds on the current (v4c) partition.** Those
older units have different names and different membership, so the existing result
does not transfer.

**Job 1 is the only job.** (Job 2 in §3 was completed on 2026-08-21 — that
section is kept only as a record.)

> **A previously-planned third job has been cancelled.** It was to re-run the
> Mississippi unit to remove a contaminated sample (`SRR30648681`). That sample
> was verified on 2026-08-20 to be already absent from the v4c panel. Do not
> re-run it. If anyone asks you to, point them at this paragraph.

---

## 1. Prerequisites

The box is a DGX Station A100: 64 physical cores (128 logical), ~480 GB RAM.
**The GPU accelerates nothing here** — every stage is CPU. Don't tune for it.

You need rclone configured for `gdrive_ph:` and **~200 GB free**
(`df -h .`). Everything else is installed below.

### 1.1 Create the conda environment

Checked on the A100 2026-08-21: `iqtree` and `snp-sites` exist in separate envs,
**ClonalFrameML is missing entirely**. Rather than wire three envs together,
put all three tools in one:

```bash
mamba create -y -n cfml-v4c -c bioconda -c conda-forge clonalframeml snp-sites iqtree
```

Verify — `ClonalFrameML`, `snp-sites`, and **at least one** of
`iqtree`/`iqtree2` must resolve:

```bash
conda run -n cfml-v4c bash -c 'for t in ClonalFrameML snp-sites iqtree iqtree2; do printf "%-14s " $t; command -v $t || echo MISSING; done'
```

It is fine if only one of the two iqtree names appears — the driver detects
which at run time. It must be **IQ-TREE 2**, though; version 1.x does not accept
the `-fconst` flag this pipeline depends on. Check with
`conda run -n cfml-v4c iqtree --version | head -1`.

### 1.2 Point the driver at YOUR conda, not the originating workstation's

The driver's defaults are the machine it was written on
(`/home/phemarajata/miniforge3`, envs `cfml` / `bp-gubbins` / `snp-phylogeny`).
None of those exist here, so **without these four exports every unit fails at
`conda activate`**:

```bash
export CFML_CONDA_SH=$HOME/miniforge3/etc/profile.d/conda.sh
export CFML_ENV_CFML=cfml-v4c
export CFML_ENV_TREE=cfml-v4c
export CFML_ENV_SNP=cfml-v4c
```

**These must be set in the same shell you launch from.** A new terminal needs
them again — put them in `~/.bashrc` if you would rather not think about it.

---

## 2. Job 1 — ClonalFrameML across the 86 v4c units

### 2.1 Get the inputs

ClonalFrameML needs the full per-unit alignments (`*.core.full.aln`, ~17 GB
total). Everything else is small.

**Step 0 — look for them on the A100 first.** The A100 ran this pipeline
originally, so it may still hold them, which saves a 17 GB download:

```bash
find ~ -name "*.core.full.aln" -path "*Clusters*" 2>/dev/null | head
```

If that lists files, note the directory holding the `cluster_*` folders and use
it as `L1v4c_out/Clusters` below (a symlink is fine). **Skip the alignment
download.**

**Step 1 — the small files, always needed:**

```bash
mkdir -p ~/v4c_cfml && cd ~/v4c_cfml
rclone copy gdrive_ph:wfsnps-v4c-results/snp/Clusters ./L1v4c_out/Clusters -P \
  --exclude "*.core.full.aln"
rclone copy gdrive_ph:wfsnps-v4c-results/snp/Summaries ./L1v4c_out/Summaries -P
rclone copy gdrive_ph:wfsnps-v4c-results/clonalframe_nu_bp.py . -P
```

**Step 2 — the alignments, only if step 0 found nothing:**

```bash
rclone copy gdrive_ph:wfsnps-v4c-results/snp/Clusters ./L1v4c_out/Clusters -P \
  --include "*.core.full.aln"
```

All 172 were uploaded and verified present on Drive on 2026-08-21. This is
~17 GB and takes a while; rclone resumes, so re-run it if interrupted.

**Checkpoint — do not proceed until all three print what is shown:**

```bash
ls L1v4c_out/Clusters | wc -l                      # expect 176
wc -l < L1v4c_out/Summaries/recombination_rm.tsv   # expect 89  (88 units + header)
ls L1v4c_out/Clusters/*/*.core.full.aln | wc -l    # expect 172
```

**The mismatched numbers are all correct — none of them is a failed download.**
*(Corrected 2026-08-21 after Yuyi found the summary has 88 units, not 87 lines.)*

There were **two runs** of this pipeline: the A100 production run produced **88
units**, and a workstation control run produced **86**, missing
`strain_1_L1_36` and `strain_1_L1_37`. The files on Drive are a mixture — the
**summary is the A100 version (88 units)**, but the **alignments are the
workstation set (86 units × 2 replicons = 172)**.

So the driver reads 88 units, finds alignments for 86, and prints:

```
MISSING alignment: strain_1_L1_36 chr1
MISSING alignment: strain_1_L1_37 chr1
```

**Those two warnings are expected. Ignore them.** They are not errors and
nothing is broken.

If the alignment count is **below 172**, the rclone genuinely did not finish.
If it is **176**, you found the A100's own copies in step 0 — even better, you
will get 88 jobs instead of 86.

### 2.2 Dry run first — this writes nothing

```bash
python3 clonalframe_nu_bp.py --layout v4c --plan --replicon chr1
```

**Expect the last line to read `86 job(s); 4 concurrent x 4 threads`** — or
`88 job(s)` if step 0 found the A100's own alignments.

| you see | means |
|---|---|
| **`86 job(s)`** | correct — alignments came from Drive |
| **`88 job(s)`** | correct and better — you have the A100's own alignments for all units |
| `6 job(s)` | `--layout v4c` was dropped; about to run the **old partition** |
| `0 job(s)` | alignments not where expected — check you are in `~/v4c_cfml` and `L1v4c_out/Clusters` sits directly beneath it |

A couple of `MISSING alignment:` lines above the count are expected at 86 — see
the checkpoint note in §2.1.

### 2.3 Run chr1

Start with chr1 only. It is half the work and tells us the timing before we
commit to the rest.

```bash
cd ~/v4c_cfml
nohup python3 clonalframe_nu_bp.py --layout v4c --run --replicon chr1 \
      --jobs 12 --threads 8 > cfml_v4c_chr1.log 2>&1 &
```

`--jobs 12 --threads 8` is 96 of 128 logical cores, leaving headroom. Do not go
above `--jobs 16`; see trap T2.

**Timing is genuinely uncertain** — ClonalFrameML runtime scales with both taxon
count and alignment length, and these units range from 7 to 159 genomes. Check
after the first hour:

```bash
ls -d cfml/*__chr1 2>/dev/null | wc -l                 # dirs created
ls cfml/*__chr1/cfml.em.txt 2>/dev/null | wc -l        # units FINISHED
```

Extrapolate from that. **Message Peera with the number finished after one hour**
— that is the single most useful thing you can send. If fewer than 3 have
finished after two hours, stop and say so rather than letting it run for days.

The run is **resumable**: a unit with `cfml.em.txt` present is skipped. Killing
and restarting loses only in-flight units.

### 2.4 Then chr2

Only after chr1 completes:

```bash
nohup python3 clonalframe_nu_bp.py --layout v4c --run --replicon chr2 \
      --jobs 12 --threads 8 > cfml_v4c_chr2.log 2>&1 &
```

### 2.5 Report and send back

```bash
python3 clonalframe_nu_bp.py --layout v4c --report --replicon chr1 > TIER1_3_clonalframe_v4c.txt
tar -czf cfml_v4c_results.tar.gz cfml/ TIER1_3_clonalframe_v4c.txt cfml_v4c_chr*.log
rclone copy cfml_v4c_results.tar.gz gdrive_ph:wfsnps-v4c-results/ -P
```

The section to look at in that report is **CONCORDANCE**. The number that
matters is the Spearman rho and the count of units that change verdict.

---

## 3. Job 2 — DONE 2026-08-21, no action needed

*Kept as a record only.* `strain_1_L1_36` and `strain_1_L1_37` were missing from
the workstation's distance table. They were recovered directly from Drive — the
`.core.tab` variant tables and Gubbins GFFs had been there all along, and the
only missing pieces were the 90 MB alignments, which that analysis does not use.
The distance table now covers all 88 units / 176 replicon-units.

---

## 4. Traps — read this before you debug anything

Every one of these has cost this project real time, and most do not look like
what they are.

| trap | what you will see | what to do |
|---|---|---|
| **CRLF in an input file** | exit code 141 and a **0-byte log**. Looks like the run failed instantly. It didn't — a pipe died. | `file <input>` — if it says CRLF, run `sed -i 's/\r$//' <file>` |
| **Concurrent Gubbins/CFML collision** | Wrong numbers, **no error at all**. Scratch files go to the *current working directory*, not the output prefix, so parallel jobs overwrite each other. | The driver script already gives each unit its own dir. **Do not run two copies of the driver from the same directory.** |
| **Long run identifiers** | RAxML segfaults; the wrapper reports it as *"Unable to fit model to data"*, which sounds like a data problem. | It is a **128-character limit** on the run id. Keep paths short — stay in `~/v4c_cfml`, don't nest deeper. |
| **Zero random seed** | One unit fails where its neighbours succeed, reproducibly on re-run. | An unseeded `randint(0,10000)` hits 0 about 1 in 10,001 times. Just re-run that unit; it is not a real failure. |
| **Out-of-memory retry loop** | A stage OOMs, retries, and fails **identically** every time. | Some memory ceilings are fixed, not scaled per attempt. Retrying will never work — report it instead. |
| **Nextflow resume** | Only relevant if you end up in Job 2's re-run path. | **Never change the cache mode mid-run.** If you must resume, resume exactly as launched. |

### If a unit fails

Failure of a few units is normal and not a crisis. Check its log:

```bash
tail -30 cfml/<unit>__chr1/run.log
```

Then re-run just that unit by deleting its directory and re-invoking the driver
(finished units are skipped, so it only redoes the missing one):

```bash
rm -rf cfml/<unit>__chr1
python3 clonalframe_nu_bp.py --layout v4c --run --replicon chr1 --jobs 1 --threads 16
```

**Record which units failed and why.** A unit that cannot be estimated is itself
a result — do not quietly drop it.

---

## 5. What to send back

1. `cfml_v4c_results.tar.gz` (§2.5)
2. A short note with: **how many units finished**, **how many failed and their
   names**, **total wall-clock**, and anything from §4 that you hit

That note is more useful than the tarball. Please send it even if everything
worked.
