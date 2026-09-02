# What lives on TB1, and how it got there

External disk **TB1** — `/dev/sda1`, ext4, label `TB1`, mounted at
`/media/phemarajata/TB1`. 916 GB total.

**For everything listed here, TB1 holds the only copy.** Nothing below exists on
the workstation any more. Treat the disk accordingly.

---

## Moved 2026-08-24 → `TB1/snp_superseded/`

Moved to buy disk headroom for the running reproducibility job
(`REPRO_RUN_2026-08-24.md`), which was projected to finish with an
uncomfortably thin margin. Script: `archive_to_tb1_2026-08-24.sh`.
Log: `ARCHIVE_TB1_2026-08-24.log`.

| directory | size | files | what it was | why it was safe to move |
|---|---|---|---|---|
| `v4c_local` | 21 GB | 2,976 | staging copy of the v4c assembly set (`v4c_local/fasta`) | **2,970 of its 2,976 files also exist** in `final_deduped_all_BP_with_locations` (2,801) or `additions/fasta_spades` (169); an 80-file checksum sample found **zero** content differences. Moved **wholesale rather than deduplicated**, so the 6 genuinely unique files travel with it |
| `L1_out` | 15 GB | 8,194 | output of the **v1** run — the original 82-unit analysis | superseded twice over. The reported basis is the v4c workstation run; see the caveat below |
| `a100_stage` | 6.4 GB | 20 | transfer bundle built for upload to the A100 (`fasta_spades_overlay.tar.zst` and friends) | a one-way transfer artifact, already consumed. The A100 run completed and its outputs are on Drive and in `A100_v4c_Clusters` |
| `a100_v4c_partition` | 6.2 GB | 76 | A100 partition staging | no script references it |
| `prod_s2_L1_6` | 2.2 GB | 110 | single-unit exploratory run | no script references it |
| `fbL1_s1_L1_27` | 2.1 GB | 106 | single-unit fastbaps exploration | no script or document references it at all |

**Total: 53 GB, 11,482 files.** Root free went **367 GB → 417 GB**; TB1 free
**630 GB → 578 GB**.

### How each move was verified

TB1 becomes the only copy, so nothing was deleted on a size or file-count match.
Per directory: `rsync -a` to copy, then **`rsync -ain --checksum`**, which
re-reads and checksums both sides and must report **zero** differing files, then
`rm -rf` on the source — and only then. A source whose verification reported
anything would have been left in place and marked `FAILED`. All six report
`verified clean` in the log, with file counts matching exactly
(2,976 / 8,194 / 20 / 76 / 110 / 106).

Copies ran under `nice -n 19 ionice -c3` so as not to starve the live Gubbins
and Snippy tasks. The reproducibility run stayed up throughout.

### ⚠ One known consequence

`phylogeography_association_bp.py` still defaults `--trees` to `L1_out/Clusters`,
which no longer exists. **Running it with no arguments will now fail loudly
instead of silently scoring the v1 trees** — which is an improvement, but it is a
change. The frozen R6 results were produced with `--trees` passed explicitly and
are unaffected. This belongs with the same class of stale default as
`SUBMISSION_TODO` E1 (`gate1_from_alignment_bp.py --mash`).

Restore with:

```bash
rsync -a /media/phemarajata/TB1/snp_superseded/L1_out/ /home/phemarajata/Downloads/snp-mod-local-working/L1_out/
```

## Deliberately NOT moved

Recorded so the reasoning does not have to be reconstructed next time the disk
is tight:

| kept | size | why |
|---|---|---|
| `L1v4c_out` | 17 GB | **the reported run's output** and the source of the frozen tables — `Summaries/recombination_rm.tsv` is what the reproducibility diff compares against. Never archive this while the paper is open |
| `REPRO_2026-08-24_{out,work}` | growing | the live run |
| `additions/` | 2.7 GB | **the live run reads 126 assemblies from it** (121 `fasta_spades` + 5 `fasta_new200`) |
| `cgmlst_lichtenegger/` | 5.7 GB | the live cgMLST scorers read it, and it is on the Zenodo archive list |
| `cgmlst_results/` | 3.3 GB | `concordance_frozen_bp.py` and `resolution_curve_bp.py` (Figure 2) both read it |
| `cfml/` | 2.1 GB | small, and the withdrawn nu hypothesis is kept on purpose |
| `A100_v4c_Clusters/`, `RETIRED_2026-08-22/a100_control/` | small | supply the A100 **control** figures quoted in Methods §2.12.10 |

## Earlier arrivals

| directory | when | note |
|---|---|---|
| `snp_superseded/pp2802_out`, `snp_superseded/all35_out` | 2026-08-15 | earlier superseded runs; TB1 is likewise the only copy |
| `snp_superseded/L1v3_out`, `L1v4b_out`, `L1v4_partition`, `L1v4b_partition` | 2026-08-16 → 18 | superseded partitions |
| `snp_archive/` (113 GB), `snp_results_2026-08-16/` | various | results archive |
| `bp-megamix`, `new_megamix`, `good_CDC_assemblies`, `ILM_ONT_comparison` | various | assembly collections, predate this work |
