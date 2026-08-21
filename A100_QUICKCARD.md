# A100 quick card — ClonalFrameML v4c

Copy-paste, top to bottom. Stop at any **CHECK** that doesn't match.
Full explanations: `A100_RUNBOOK_YUYI.md`. Thai: `A100_RUNBOOK_YUYI_TH.md`.

Total: ~20 min of your attention, then 3–4 h unattended.

---

## 0. Confirm your rclone remote is called `gdrive_ph`

```bash
rclone listremotes
```

**CHECK →** `gdrive_ph:` is listed.

If it has a different name, either use that name everywhere below, or rename it
in `rclone config`. Remote names are local aliases — they differ per machine.

---

## 1. Install (once, ~2 min)

```bash
mamba create -y -n cfml-v4c -c bioconda -c conda-forge clonalframeml snp-sites iqtree
```

```bash
conda run -n cfml-v4c bash -c 'for t in ClonalFrameML snp-sites iqtree iqtree2; do printf "%-14s " $t; command -v $t || echo MISSING; done'
conda run -n cfml-v4c iqtree --version 2>/dev/null | head -1
```

**CHECK →** `ClonalFrameML` and `snp-sites` both found; **at least one** of
`iqtree`/`iqtree2` found; version line says **2.x** (not 1.x).

---

## 2. Configure (every new terminal)

```bash
export CFML_CONDA_SH=$HOME/miniforge3/etc/profile.d/conda.sh
export CFML_ENV_CFML=cfml-v4c
export CFML_ENV_TREE=cfml-v4c
export CFML_ENV_SNP=cfml-v4c
```

**CHECK →**

```bash
ls $CFML_CONDA_SH
```

prints the path (no "No such file"). If it errors, find yours with
`ls ~/*conda*/etc/profile.d/conda.sh` and re-export.

> Skip re-typing these later: `cat >> ~/.bashrc` and paste the four lines.

---

## 3. Get the data

```bash
mkdir -p ~/v4c_cfml && cd ~/v4c_cfml
```

**3a. Do you already have the alignments locally?**

```bash
find ~ -name "*.core.full.aln" -path "*Clusters*" 2>/dev/null | head
```

- **Lists files** → note that directory, skip 3c, symlink it as
  `~/v4c_cfml/L1v4c_out/Clusters`
- **Empty** → do 3c

**3b. Small files (always):**

```bash
cd ~/v4c_cfml
rclone copy gdrive_ph:wfsnps-v4c-results/snp/Clusters ./L1v4c_out/Clusters -P --exclude "*.core.full.aln"
rclone copy gdrive_ph:wfsnps-v4c-results/snp/Summaries ./L1v4c_out/Summaries -P
rclone copy gdrive_ph:wfsnps-v4c-results/clonalframe_nu_bp.py . -P
```

**3c. Alignments — only if 3a was empty (17 GB, slow, resumable):**

```bash
rclone copy gdrive_ph:wfsnps-v4c-results/snp/Clusters ./L1v4c_out/Clusters -P --include "*.core.full.aln"
```

---

## 4. Verify before running

```bash
cd ~/v4c_cfml
ls L1v4c_out/Clusters | wc -l                       # expect 176
ls L1v4c_out/Clusters/*/*.core.full.aln | wc -l     # expect 172 (or 176)
wc -l < L1v4c_out/Summaries/recombination_rm.tsv    # expect 89
grep -c CFML_CONDA_SH clonalframe_nu_bp.py          # expect 1 or more, NOT 0
```

**CHECK →** all four match.

- **176 dirs, 172 alignments, 89 summary lines is CORRECT.** Two pipeline runs
  exist: the summary is the A100 version (88 units), the alignments are the
  workstation set (86 units). Nothing is missing.
- **176 alignments** → you found the A100's own copies; even better, you'll get
  88 jobs.
- **Last one prints `0`** → you have the old script:
  `rm clonalframe_nu_bp.py` then re-run the third command in 3b.

---

## 5. Dry run (writes nothing)

```bash
python3 clonalframe_nu_bp.py --layout v4c --plan --replicon chr1
```

**CHECK →** last line reads `86 job(s); 4 concurrent x 4 threads`
(or `88 job(s)` if you have the A100's own alignments)

| you see | means |
|---|---|
| `86 job(s)` | correct — alignments from Drive |
| `88 job(s)` | correct, better — A100's own alignments |
| `MISSING alignment: strain_1_L1_36/37` | **expected at 86, ignore** |
| `6 job(s)` | `--layout v4c` was dropped — about to run the wrong dataset |
| `0 job(s)` | alignments not where expected — check you're in `~/v4c_cfml` |

---

## 6. Run chr1

```bash
cd ~/v4c_cfml
nohup python3 clonalframe_nu_bp.py --layout v4c --run --replicon chr1 --jobs 12 --threads 8 > cfml_v4c_chr1.log 2>&1 &
```

Do not exceed `--jobs 16`.

---

## 7. Monitor

```bash
ls cfml/*__chr1/cfml.em.txt 2>/dev/null | wc -l     # units FINISHED
ls -d cfml/*__chr1 2>/dev/null | wc -l              # units started
```

**After 1 hour: message Peera the finished count.** That's the single most
useful thing to send.

**If fewer than 3 finished after 2 hours — stop and say so.** Don't let it run
for days.

Resumable: finished units are skipped on restart, so killing it loses only
in-flight work.

---

## 8. Then chr2 (only after chr1 finishes)

```bash
nohup python3 clonalframe_nu_bp.py --layout v4c --run --replicon chr2 --jobs 12 --threads 8 > cfml_v4c_chr2.log 2>&1 &
```

---

## 9. Send results back

```bash
cd ~/v4c_cfml
python3 clonalframe_nu_bp.py --layout v4c --report --replicon chr1 > TIER1_3_clonalframe_v4c.txt
tar -czf cfml_v4c_results.tar.gz cfml/ TIER1_3_clonalframe_v4c.txt cfml_v4c_chr*.log
rclone copy cfml_v4c_results.tar.gz gdrive_ph:wfsnps-v4c-results/ -P
```

Plus a short note: **how many finished**, **how many failed and their names**,
**total wall-clock**.

---

## If something breaks

```bash
tail -30 cfml/<unit>__chr1/run.log
```

Re-run one unit:

```bash
rm -rf cfml/<unit>__chr1
python3 clonalframe_nu_bp.py --layout v4c --run --replicon chr1 --jobs 1 --threads 16
```

| symptom | cause | fix |
|---|---|---|
| exit 141, **0-byte log** | CRLF line endings in an input | `sed -i 's/\r$//' <file>` |
| `conda activate` fails | §2 exports not set in this shell | re-run §2 |
| `neither iqtree2 nor iqtree found` | env not active / bad install | re-run §1 |
| `-fconst` unrecognised | IQ-TREE 1.x installed | `mamba install -n cfml-v4c "iqtree>=2"` |
| *"Unable to fit model to data"* | RAxML 128-char path limit | keep paths short, stay in `~/v4c_cfml` |
| one unit fails, neighbours fine | random seed hit 0 (~1 in 10,000) | just re-run that unit |
| OOM, retries fail identically | fixed memory ceiling | don't retry — report it |

**Wrong numbers with no error** = two copies of the driver running from the same
directory. Scratch files collide. Never run two at once from one folder.

A few failed units is normal. **Record which and why** — a unit that can't be
estimated is itself a result. Don't drop it silently.
