# L1 v4b partition — 2,973 genomes, full PopPIPE — 2026-08-17

Supersedes the 2,466-genome v4 attempt in `L1V4_PARTITION_REPORT_2026-08-17.md`.
Outputs: `curated_L1v4b_{clusters,units,stragglers,merges,assignments_all}.tsv`,
panel `L1v4b_MERGED_METADATA.tsv`, samplesheet `wf_L1v4b_samplesheet.csv`.

## Panel

    2,282  v3 analysis panel
      520  v3 collection, assign-only in v3 (recovered -- v4 had wrongly dropped these)
      171  new TheiaProk (184 delivered, minus 13 already in the collection)
    2,973  total

`origin_country` present for 2,958/2,973; 15 unknown. `origin_resolution` marks
2,956 `country`, 1 `multi_country` (Panama and Peru), 1 `region` (Africa),
15 `unknown` — exclude the non-`country` rows from country statistics.

## Result

    PopPUNK 2.7.6, bgmm K=5 + refine   325 strains, network score 0.9231
                                       39 strains at n>=7 (2,475 genomes)
    Full PopPIPE fastbaps              45 strains at n>=6, all fresh labels
    L1 partition                       479 units, 95 at n >= 7, 384 assign-only
    analysed                           2,311 of 2,973 (77.7%)
    stragglers                         462, all 462 placed, 0 unassigned
    kept units                         min 7, median 17, max 164

**No label transfer remains anywhere.** Every strain at n>=6 got its own
ska + rapidnj + fastbaps run against this panel; nothing is inherited from the
2,430-genome archive. That removes the failure that sank the 2,466 attempt, where
strain_7 was 68% unlabelled and 56 genomes went unplaced.

| | v3 | v4b |
|---|---|---|
| collection partitioned | 2,802 | 2,973 |
| units | 376 | 479 |
| units at n>=7 | 91 | **95** |
| genomes analysed | 2,282 | **2,311** |
| stragglers unplaced | — | **0** |
| PopPUNK network score | 0.8894 | **0.9231** |

## Both rescue targets landed

**Mississippi: 22 genomes, all `analysis`, all in one unit `strain_5_L1_4`.**
The handoff target was n=23 from PRJNA942243; the 23rd is `SRR30648669`, dropped
as *B. thailandensis*. So 22 is the correct complete answer, not a shortfall.

**Mexico: 8 in the panel, 4 `analysis` in `strain_5_L1_7`**, 4 assign-only in
singleton PopPUNK clusters. Partial — the v3 target `strain_9_L1_8` was n=6.

## The trade: 137 gained, 108 lost

**Gained — 137 genomes newly analysed** (107 new + 30 recovered), concentrated
exactly where the panel was blind:

    Cambodia 29   USA 23   Brazil 14   Philippines 11   Ghana 11   Colombia 9
    Indonesia 6   Thailand 6   China 6   Laos 6   Malaysia 4   Mexico 4

**Lost — 108 genomes that v3 analysed are now assign-only.** By country:
Thailand 53, Malaysia 12, Australia 11, Laos 8, Sri Lanka 7, China 5.

The mechanism is unit fragmentation, not exclusion: those 108 came from **18 v3
units** and now sit in **57 v4b units**, 74 of them in units of size 1–3 and 34 in
units of size 4–6. Fresh fastbaps subdivided more finely than the archived labels
did for those strains — partly a different PopPUNK fit (K=5), partly RapidNJ
hierarchies where some archived strains had used IQ-TREE.

Net analysed +29. The composition shift is the real result: 47 Thai genomes lost
from an already 1,600-strong set, against the first Americas, African and
Philippine representation the panel has ever had.

**This is a judgment call, not a settled outcome.** Finer units are tighter, which
suits Gubbins, but a unit below n=7 cannot carry an r/m estimate. If the 108 matter
more than the granularity, the lever is `--min-size`, not a re-partition.

## Validation set

16 travel-reattributed genomes (PRJNA908850 `ex <country>` convention) carry
`validation_label`. 11 reach analysis units, 5 are assign-only:

| label | analysis | assign-only |
|---|---|---|
| Philippines | 10 | 2 |
| El Salvador | 0 | 1 |
| Ghana | 0 | 1 |
| Nicaragua | 0 | 1 |
| Nigeria | 0 | 1 |

Nine of the ten analysed Philippine genomes sit together in `strain_1_L1_8`
(n=56), which is a coherent target for leave-one-out scoring. The four singleton
labels (El Salvador, Ghana, Nicaragua, Nigeria) landed in their own PopPUNK
clusters and are assign-only, so they can be placed on a tree but not scored
inside a unit.

**Still score leave-one-out.** These 16 are in the panel; an accuracy computed
with them left in is circular.

## Marginal genomes flagged earlier

- `SRR32083527` (core 84.4%) → `strain_1_L1_8`, n=56. One marginal member of 56;
  low impact, keep.
- `SRR32459564` (core 84.2%) → `strain_1_L1_19`, **n=7, exactly at the floor**.
  This is the case predicted in the QC report: dropping it takes the unit to n=6
  and deletes the unit entirely. Keep it, and treat that unit's core alignment as
  capped by its worst member.

## Defects found and fixed during this build

1. **v4 partitioned the wrong set** — built from `L1v3_ASSIGNMENTS.tsv` (v3's
   *analysis subset*) instead of the 2,802 collection, silently dropping 521
   genomes including 4 of 5 Mississippi and 4 Mexico. Fixed by rebuilding at
   2,973.
2. **13 duplicate genomes** — `SRA_TO_ASSEMBLE.tsv` re-requested accessions
   already held; the v3 SPAdes assembly beat the new SKESA one in 13/13 pairs.
   New copies dropped; the batch adds 171, not 184.
3. **PopPUNK K=4 unstable on this set** — bgmm collapsed twice (5 then 9 clusters,
   largest 2,981/2,986), refine reaching only 0.7336, below the >=0.8 bar. K=5
   gives 233 clusters / largest 1,748 and score 0.9231. Documented deviation from
   the pipeline's K=4.
4. **fastbaps silently returns an all-1s partition** on an unrooted tree or a
   label mismatch. Caught twice by the guard in `run_poppipe_v4b.py`; PopPIPE
   avoids it via ete3 midpoint-rooting inside `run_iqtree.py`.
5. **`GCF_015714675_1_Virgin_Islands_St._John`** — PopPUNK rewrites `.` to `_`,
   so `sketchlib --subset` matched 100 of 101 names and fastbaps died on a label
   mismatch. Third failure from this one id; fixed at the source by making the
   sanitized spelling canonical everywhere. Hyphens are not rewritten — this was
   the only affected id, verified against `db/db.dists.pkl`.
6. **Mash sketch size** — the run used `-s 50000`, not the 10000 in
   `params.config`. Rebuilt to match; 2,415/2,415 shared pairs identical to
   `mash_matrix_2802.tsv`.

## Next

Regenerate references, re-run the SNP pipeline from
`wf_L1v4b_samplesheet.csv`, re-export as the next `PART`.

Pending: the SPAdes re-assembly of the new Illumina samples. When it lands, the
171 should be re-QC'd and the partition re-run — the fragmented SKESA assemblies
are the likeliest cause of any Americas unit that looks over-split here.
