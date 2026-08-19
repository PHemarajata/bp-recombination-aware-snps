# L1 v4 re-partition from `wf_L1v4_samplesheet.csv` — 2026-08-17

Outputs: `curated_L1v4_{clusters,units,stragglers,merges,assignments_all}.tsv`.
Working files in `L1v4_partition/`.

## Result

    PopPUNK (2.7.6)   2,466 genomes -> 94 strains, network score 0.9107
                      36 strains at n >= 7 (2,381 genomes), 58 sub-threshold (85)
    L1 partition      139 units, 91 at n >= 7, 48 assign-only
    analysed          2,346 of 2,466 (95.1%)

    v3:  91 units, 2,282 analysed of 2,802 collection
    v4:  91 units, 2,346 analysed of 2,466 merged

The membership guard passed — every v4 PopPUNK strain maps 1:1 onto one archived
fastbaps strain, so the label transfer is legitimate *at the strain level*.

## But the Americas is the part that failed

Of the 184 new genomes, only **82 reach an analysis unit**:

| role | new | v3 panel |
|---|---|---|
| analysis | 82 | 2,264 |
| assign_only | 46 | 18 |
| unplaced | 56 | 0 |

The 56 unplaced are recorded in `curated_L1v4_assignments_all.tsv` with
`role=below_strain_floor`. **That label is a misnomer** — the script writes it
for any genome in `--all-clusters` that never landed in an L1 unit, and the log
line "0 genomes sit in PopPUNK strains below the strain floor" is the accurate
statement. These 56 are the stragglers the nearest-neighbour policy could not
place (`stragglers: 197, 141 placed, 56 left unassigned`).

Their origins:

    USA 17   Brazil 17   Cambodia 9   Colombia 9   Myanmar 2   Nicaragua 1   Philippines 1

**All 17 Mississippi genomes are unplaced** — the exact genomes the additions
were meant to use to rescue the Mississippi unit.

## Why: fastbaps label coverage is fine everywhere except the new geography

Per PopPUNK strain, share of members carrying an archived fastbaps L1 label:

| strain | n | labelled | unlabelled | top countries |
|---|---|---|---|---|
| strain_1 | 422 | 416 | 6 | Thailand 337 |
| strain_2 | 378 | 365 | 13 | Thailand 216, China 108 |
| strain_3 | 264 | 261 | 3 | Thailand 255 |
| strain_4 | 190 | 185 | 5 | Singapore 54, China 46 |
| strain_5 | 171 | 160 | 11 | Thailand 75, China 69 |
| strain_6 | 99 | 90 | 9 | Thailand 88 |
| **strain_7** | **84** | **27** | **57** | **USA 32, Brazil 28, Colombia 11** |
| strain_9 | 64 | 59 | 5 | Thailand 57 |
| **strain_33** | **10** | **0** | **10** | **Ghana 10** |

The Asian strains are 96–99% labelled and transfer cleanly. **strain_7 — the
Americas clade — is 68% unlabelled**, and strain_33 (Ghana) has no labels at all.

Nearest-neighbour straggler assignment needs a *labelled strain-mate* to attach
to. In strain_7 the labelled minority is the 27 v3 Americas genomes, and it was
not enough to absorb the 57 new ones; 56 fell out. strain_33 has no labelled
member at all, so it became a single whole-strain unit of 10 with no subdivision.

Overall unlabelled share: **196 of 2,466 = 7.9%**, against the **15 genomes
(0.7%)** the label-transfer approach was validated on.

## What did form in the Americas

| unit | n | composition |
|---|---|---|
| strain_7_L1_4 | 13 | USA 6, Puerto Rico 5, Trinidad and Tobago 1, Virgin Islands 1 |
| strain_7_L1_5 | 7 | USA 5, Guadeloupe 1, Martinique 1 |
| strain_7_L1_7 | 19 | Brazil 12, Ecuador 2, USA 2, Colombia 2, Costa Rica 1 |
| strain_33_L1_1 | 10 | Ghana 10 |

Three Americas units out of 84 available genomes, and 17 Mississippi sitting
outside all of them.

## Two things fixed during the run, both silent-failure class

**1. Mash matrix parameter.** `conf/params.config` declares
`mash_sketch_size = 10000`, but `mash info` on the archived sketches
(`pp2802_out/Clustering/Sketches/combined.msh`) reports **Target min-hashes per
sketch: 50000** — the run overrode the config. Matrices built at `-s 1000` and
`-s 10000` disagreed with `mash_matrix_2802.tsv` on 1,767 of 1,770 sampled pairs
(worst 0.00137 and 0.00037 respectively). Rebuilt at `-s 50000 -k 21`:
**3,160 of 3,160 sampled shared pairs now match exactly, worst diff 0.**

Since the merge ceiling here is 0.00422, a 0.0014 error is a third of the
ceiling — it would have changed merge decisions without changing anything
visible in the output.

Also note `mash sketch -m 1` (which the module passes) silently switches mash to
reads mode; combined with `-l`, it produced a single 38 Mb sketch of all 2,466
genomes concatenated instead of 2,466 sketches. Harmless in the pipeline because
it sketches one sample per invocation, fatal in a batch call.

**2. Name reconciliation on `--all-clusters`.** PopPUNK rewrites
`GCF_015714675_1_Virgin_Islands_St._John` to `...St__John`.
`poppunk_clusters_to_tsv.py` reconciles it for `--clusters`, but the raw
`refined_clusters.csv` passed to `--all-clusters` does not, so that genome
entered the partition **twice** under two spellings — 2,467 rows for 2,466
genomes, one copy in an analysis unit and one as unplaced. Fixed by writing
`L1v4_partition/refined_clusters_reconciled.csv` and re-running.
`assignments_all` is now exactly 2,466 unique ids matching the metadata.

## Recommendation: re-run fastbaps, at least on strain_7 and strain_33

The transfer is sound for the Asian strains and demonstrably not sound for the
Americas and Ghana. Reusing labels was the right call at a 15-genome seam in
well-labelled strains; it is the wrong call for a clade that is 68% unlabelled
and is the clade the origin-attribution goal depends on.

Nearest-neighbour assignment can only place a new genome into a pre-existing
subcluster — it can never let 57 new Americas genomes *define* their own
structure. That is precisely what is needed here.

Options, cheapest first:

1. **Run PopPIPE/fastbaps on strain_7 and strain_33 only**, then re-run
   `build_L1_partition_bp.py` with the augmented label set. Smallest change,
   fixes the failure exactly where it is. Both are small (84 and 10 genomes).
2. **Run PopPIPE on the full v4 set.** Cleanest and internally consistent, but
   re-derives labels for all 43 strains, so every unit id changes and the v3/v4
   comparison stops being like-for-like.

`~/PopPIPE-bp` is present with 42 strain directories, and the `poppipe` conda
env has PopPUNK 2.7.6 and the PopPIPE toolchain.

**Not recommended:** shipping the current v4 partition. It looks healthy — 91
units, 95.1% analysed, same unit count as v3 — and the headline numbers hide the
fact that the Americas additions largely did not land. This is the same shape as
the seven prior defects: plausible summary, wrong per-item values.

## Reproduce

    cd L1v4_partition
    poppunk --create-db --r-files rfile.txt --output db --min-k 15 --max-k 31 --k-step 2 --threads 8
    poppunk --fit-model bgmm --ref-db db --output fit --K 4 --max-a-dist 0.53 --threads 8
    poppunk --fit-model refine --ref-db db --model-dir fit --output refined --threads 8
    mash sketch -s 50000 -k 21 -p 8 -o combined -l paths.txt      # NOT -m, NOT -s 10000
    mash triangle -p 8 combined.msh > mash_distances.phylip
    python3 ~/wf-assembly-snps-mod/bin/mash_phylip_to_matrix.py mash_distances.phylip mash_matrix_2466.tsv
    python3 ~/wf-assembly-snps-mod/bin/poppunk_clusters_to_tsv.py \
        --clusters refined/refined_clusters.csv --rfile rfile.txt \
        --min-cluster-size 7 --prefix strain_ --out clusters.tsv --excluded poppunk_excluded.tsv
    # reconcile names in refined_clusters.csv -> refined_clusters_reconciled.csv, then:
    python3 ../build_L1_partition_bp.py --clusters clusters.tsv \
        --all-clusters refined_clusters_reconciled.csv --absorb-subthreshold-strains \
        --mash mash_matrix_2466.tsv --poppipe ~/PopPIPE-bp --min-size 7 --prefix curated_L1v4

---

# Update: targeted fastbaps on strain_7 and strain_33 — 2026-08-17

## It worked, and it exposed a scoping error upstream

### The fastbaps run

Reproduced the archived procedure exactly from `config.bp2802.yml` — `ska build
-k 31 --min-qual 20 --min-count 4`, `ska align --filter no-const
--no-gap-only-sites`, IQ-TREE `GTR+F+R6`, midpoint-root, `run_fastbaps.R`
levels=3. Alignments: strain_7 84 seqs / 38,092 variant sites; strain_33 10 seqs
/ 1,236 sites.

**A silent failure first time round.** `multi_level_best_baps_partition` requires
a rooted tree; IQ-TREE emits an unrooted one. `run_fastbaps.R` catches the error
and its fallback writes an **all-1s null partition** — a valid-looking file
saying "no subdivision". PopPIPE avoids this because `run_iqtree.py`
midpoint-roots with ete3 between IQ-TREE and fastbaps; running the rule's shell
command alone skips that. The tell was in the log:

    <simpleError ...: phylo object must be rooted>
    Problem loading fasta file – not generating subclusters

Audited the archive for the same fallback: strains 10 (n=40) and 14 (n=31) have a
single L1 cluster, but their `logs/fastbaps_*.log` are empty, and `print(e)`
writes to stdout which the Snakefile captures — so those are genuine tight
strains, not fallbacks. **The archive is clean.**

After midpoint-rooting: strain_7 → **10 L1 clusters**, strain_33 → 2.

### Label coverage and the rebuilt partition

Archived strain `9` supplies labels to v4 `strain_7` and nothing else, so it was
dropped wholesale and replaced by `v4s7` (all 84 genomes) rather than left to
collide. `assemble_label_root.py` enforces that no genome is labelled under two
directories. Unlabelled share over `clusters.tsv`: **7.9% → 2.9%** (68 genomes).

| | before | after |
|---|---|---|
| L1 units | 139 (91 at n>=7) | **145 (93 at n>=7)** |
| analysed | 2,346 (95.1%) | **2,375 (96.3%)** |
| stragglers | 197: 141 placed, **56 unplaced** | 129: 117 placed, **12 unplaced** |
| new genomes reaching analysis | 82 | **122** |

The Americas subdivision is geographically coherent, which is the real check:

| unit | n | new | composition |
|---|---|---|---|
| strain_7_L1_2 | 18 | 18 | **USA 17 (all Mississippi)**, Colombia 1 |
| strain_7_L1_6 | 20 | 20 | Brazil 20 |
| strain_7_L1_5 | 12 | 0 | USA 6, Puerto Rico 5, Trinidad and Tobago 1 |
| strain_7_L1_3 | 10 | 8 | Colombia 8, USA 2 |
| strain_7_L1_4 | 8 | 8 | Brazil 8 |
| strain_33_L1_1 | 10 | 10 | Ghana 10 |

Brazil separates from Mississippi separates from the Caribbean, and the 17
Mississippi genomes form one unit. **All 17 reach `role=analysis`.** The 12
remaining unplaced are Cambodia 9, Myanmar 2, Philippines 1 (`SRR32012547`, a
validation-labelled genome).

## The scoping error

The handoff expects the Mississippi unit to reach n=23 by adding the new genomes
to the existing 5. It reached n=18, because **the existing 5 are not in the panel
at all.**

I built `L1v4_MERGED_METADATA.tsv` from `L1v3_ASSIGNMENTS.tsv` (2,282 rows), which
is v3's **analysis subset**. The full v3 collection is
`curated_L1v3_assignments_all.tsv` (2,802). What v3 actually did:

    PopPUNK + partition on 2,802 (the whole collection)
      -> 91 analysis units covering 2,282
      -> wf_L1_samplesheet.csv with those 2,282 fed to the SNP pipeline

I partitioned on **2,466 = v3's output + 184**, so the partition input was
pre-filtered by a previous partition's discard. That re-applies exactly the
double-discard that the merge-not-delete work was built to remove.

**521 genomes dropped** (517 `assign_only`, 4 `below_strain_floor`); 520 of 521
have assemblies on disk in `final_deduped_all_BP_with_locations/`.

    Australia 181   India 38   Thailand 22   USA 18   Malaysia 10   Mexico 4
    (+248 whose country is not encoded in the sample name)

Including **4 of the 5 Mississippi genomes** and 4 Mexico genomes — the latter
being the other rescue target, `strain_9_L1_8`. The Australian loss of 181 is the
same shape as the documented 74% Australia dropout, and Australia is basal in the
global tree.

**Correct partition input is 2,802 + 184 = 2,986, not 2,466.**

## What a redo costs

PopPUNK ~7 min, mash `-s 50000` ~5 min, fastbaps on affected strains ~15 min,
partition seconds. Cheap in compute.

The consequence that matters: adding 521 genomes **changes strain membership**,
so `v4s7` would have to be recomputed against a different strain_7 — and other
strains would newly cross the n>=7 floor. Patching two strains again would be
guesswork about which two. This is the point at which running PopPIPE/fastbaps
over the whole set stops being the expensive option and becomes the cheap one.

**Recommendation:** rebuild the panel at 2,986, re-run PopPUNK, then run PopPIPE
on the full v4 set. The current 2,466 partition should not be carried forward.
