# Methods (draft, updated 2026-08-19)

> **Revision note.** Sections 1–2.11 (method development, calibration and
> validation) are unchanged from the 2026-08-11 draft. **Section 2.12 has been
> replaced in full**: it now describes the 88-unit v4c production run of
> 2026-08-19 and its 86-unit control, superseding the earlier 82-unit run.
> The substantive changes are: the panel (2,976 assemblies), assembler selection
> and the recalibrated assembly-QC gate (2.12.1–2.12.3); unit refinement and the
> Gate 1 / Gate 2 order that governs it (2.12.5); **r/m reported only for the 47
> in-window units, median 7.70** (2.12.7), on an alignment-derived Gate 1
> (2.6.1); and the reproducibility control (2.12.10).

> **Status.** Sections 2.1–2.11 describe the exploratory and calibration work,
> written while the production run was still pending. **Section 2.12 describes
> the analysis that was actually run and from which all reported results come**,
> and where the two disagree, 2.12 supersedes.
>
> Items marked **[CONFIRM]** are placeholders where the exact value could not be
> recovered from the run artefacts and must be filled from the lab record before
> submission. Section 2.7 was written as a plan and its projected yield is
> superseded by the measured yield in 2.12.2.

## 2.1 Genome collection and quality control

Analyses were performed on **2,802 *Burkholderia pseudomallei* assemblies**, a
deduplicated, location-filtered collection assembled for this work. **It is not a
subset of the public audit reported below**, and the two must not be conflated:

| source | n | share |
|---|---|---|
| GenBank assemblies (`GCA_`) | 1,398 | 49.9% |
| RefSeq assemblies (`GCF_`) | 1,035 | 36.9% |
| **NCBI-derived subtotal** | **2,433** | **86.8%** |
| in-house isolates (`IP-`) | 259 | 9.2% |
| in-house isolates (`IE-`) | 53 | 1.9% |
| SRA/ENA read sets assembled locally (`SRR`, `ERR`) | 57 | 2.0% |
| **non-public subtotal** | **369** | **13.2%** |

**369 genomes (13.2%) are not present in the public audit at all.** Inclusion
required deduplication and the presence of usable location metadata; the
resulting set is the input directory `final_deduped_all_BP_with_locations`, which
is the recorded `--input` of the production run.

**Quality control, stated plainly: no assembly-quality screen was applied to this
collection.** This is reported rather than glossed, because a reader will
reasonably assume otherwise.

The only per-assembly QC threshold anywhere in the recorded pipeline is a
**minimum input file size of 45 kB**, enforced once at input handling. Against a
7.2 Mbp genome it is non-binding by roughly two orders of magnitude: the smallest
assembly in the collection is **6.42 MB**, the median 6.92 MB and the largest
10.26 MB, so no assembly was within a factor of 140 of the threshold and none was
excluded by it. All 2,795 assemblies in the archived production run recorded
`PASS`. No assembly-quality metric — contig count, N50, genome size,
completeness or contamination — was computed or filtered on at any stage; no
QUAST, CheckM or BUSCO output exists for this collection.

What the two curation steps in the directory name actually mean is narrower than
"QC":

- **Deduplication** was performed at accession level, dropping the RefSeq (`GCF_`)
  copy wherever a GenBank (`GCA_`) duplicate of the same assembly existed. This is
  verifiable in the result: no two entries in the 2,802 share a numeric assembly
  accession. A second, manual axis recorded patient-case linkage, but it is
  annotated for only **53 of 2,796** manifest rows (45 "none", 7 "single/direct",
  1 "co-equal"), so it is a partial annotation rather than a systematic
  one-isolate-per-patient rule.
- **Location filtering** means the presence of curated country-level metadata in
  the accompanying manifest, not a quality criterion.

**The consequence, which belongs in the limitations.** The collection therefore
contains assemblies that a conventional QC step would have flagged: contig counts
run from 1 to **3,097** (median 139, p95 331), with **45 assemblies above 500
contigs** and **9 above 1,000**. Only **192 of 2,802** are effectively complete
(≤ 2 contigs), which is the pool from which per-unit references were drawn
(Section 2.4). None of this was screened.

**Two assemblies carry a duplicated replicon, and were identified by this size
check.** `GCA_017356725_2` (strain VBM399) and `GCA_017356705_2` (strain VBM364)
total 10.63 and 10.60 Mbp against an expected 7.25 Mbp — 47% oversized, and
separated from the rest of the collection by a 1 MB gap with no assembly between
8.0 and 9.0 MB. Both are two-contig records in which the **first contig alone
(7.39 Mbp) is the size of a complete genome** and the second (3.21–3.24 Mbp)
matches chromosome II (reference 3.17 Mbp), so **chromosome II is represented
twice**. The contig accessions come from two different submission ranges
(`CP0715xx` and `CP0762xx`), consistent with an assembly-version merge that
retained a redundant replicon rather than with biological contamination.

**Their effect on the results is nil, which we verified rather than assumed.**
Neither appears in any analysed unit — both sit in PopPUNK `cluster_40`, which was
never a candidate — and neither was selected as a per-unit reference, despite
being *eligible* under the ≤ 2-contig admissibility rule that a duplicated-replicon
assembly satisfies for the wrong reason. Their only footprint is on the PopPUNK
fit and the collection-level counts. **The near-miss is worth reporting: a
contig-count criterion for reference admissibility does not detect this failure
mode, and a total-length check would have.** We recommend the latter alongside any
contig-count rule.

The 312 in-house `IP-`/`IE-` isolates were sequenced on **Illumina** (paired-end)
and assembled with **`bacterial-genomics/wf-paired-end-illumina-assembly`
v3.1.1**, using its **SPAdes** assembler path. That workflow trims with
Trimmomatic, removes PhiX with bbduk, overlaps read pairs with FLASH, assembles
with SPAdes, and polishes with bwa + Pilon; all process containers are pinned by
SHA256 digest. Their file provenance is resolved — all 312, together with 8 `SRR`
assemblies, come from the `320_isolates` directory, and all 320 are present in
the 2,802.

**[CONFIRM — minor, lab record only: the SPAdes version *number*. The workflow
pins its container by digest (`staphb/spades@sha256:5df39e84…`) rather than by
version tag, so the release number is not readable from the workflow source. Take
it from the assembly runs' `software_versions.yml`, or by inspecting that image.
Same for Trimmomatic and Pilon if the journal requires per-tool versions.]**

*A minor discrepancy to reconcile before submission:* the archived production run
(`results_all_2795`) processed **2,795** genomes from this same input directory,
seven fewer than the 2,802 the PopPUNK fit used. The direction and cause should be
established rather than assumed.

For context on sampling structure — and as an external reference point rather
than as the sampling frame for this collection — all public *B. pseudomallei*
assemblies were audited via the NCBI Datasets API (taxid 28450, queried
2026-08-09; n = 5,728).
The collection is dominated by Thailand (59.6%), followed by Australia (10.2%)
and China (7.0%), with Africa nearly absent. **81% of Thai genomes derive from
three BioProjects** (PRJEB3409, n = 1,506; PRJEB25606, n = 682; PRJEB35787,
n = 582), and the five largest BioProjects account for 61% of the collection, so
pseudo-replication operates at the study level and the effective independent
sample size is substantially below n. Metadata completeness was 96.3% for country
and 61.8% for collection year. Applying country, year, contig N50 ≥ 20 kb and
total length 6.5–7.9 Mb filters retained 3,436 genomes (60%), still 54.1%
Thailand against 8.1% Australia.

This imbalance is reported here because it bounds the phylogeographic
interpretation rather than the recombination analysis: the published inference of
an Australian ancestral reservoir rests on a deliberately balanced 469-genome,
30-country design, whereas the public collection inverts that ratio roughly
sevenfold. Discrete-trait or mugration analysis run on the unweighted collection
would measure sequencing effort rather than biogeography, and no clustering
algorithm or recombination correction repairs this.

## 2.2 Population structure: strains and sub-clusters

Clustering by Mash distance was abandoned. Mash conflates core divergence with
gene content, which is material in this organism — K96243 carries 16 genomic
islands (~6% of the genome) and accessory profiles are clade-specific — and, when
benchmarked against alignment-derived pairwise SNP distances, Mash mis-scaled by
between 0.88× and 91× depending on cluster (Section 2.3).

Strains were instead defined with **PopPUNK 2.7.6** (sketchlib backend v2.1.5)
using parameters previously fitted to this organism by Seng et al. 2024
(PMID 38972886): database construction with `--min-k 15 --max-k 31 --k-step 2`,
then a BGMM fit with `--K 4 --max-a-dist 0.53`. *(Note for the record: the
protocol as written intended v2.6.0; the run log resolves to the `poppipe`
environment, which carries 2.7.6, so 2.7.6 is what executed.)* A boundary-refined
fit was used in preference to the initial model fit; the refined fit assigned all
2,802 genomes to **271 strains** (initial fit: 208).

Strains were sub-partitioned with **fastbaps 1.0.8** (`r-fastbaps`) in
phylogeny-conditioned mode (`best_baps_partition(sparse.data, tree)`, multi-level
via `multi_res_baps()`). This mode was selected because it cannot emit a
polyphyletic cluster — monophyly holds by construction — and because it scales:
the BAPS-family alternative did not complete in a week at comparable scale.
Sub-clustering yielded **64 level-1 (L1) sub-clusters over 1,590 samples**.

**Level 1 was used, and deeper levels were rejected on measurement.** Descending
L1 → L2 → L3 moved the usable fraction of the collection from 14.2% to 11.5% to
11.5%, and L3 shattered strains into pairs (median sub-cluster size 2; 206 of 319
sub-clusters were singletons or pairs). Raising the number of fastbaps levels
would therefore make coverage strictly worse.

## 2.3 Diversity measurement and its calibration

Cluster diversity was measured as **mean pairwise core SNP distance using
`ska distance` (SKA2 v0.5.0) with `--min-freq 0.0`**, which requires neither a
reference nor an alignment.

The `--min-freq` setting was calibrated against four clusters for which
alignment-derived mean pairwise distances were available. At `--min-freq 0.0`
every anchor fell within 13% of its alignment-derived value with rank order
preserved; other settings were uniformly worse. Mash distances on the same
anchors spanned 0.88×–91× of the true value and were discarded as a diversity
statistic.

**Two diversity scales exist and must not be mixed.** Alignment-derived means run
approximately 10% above `ska distance` values for the same cluster (e.g. 3,193
versus 2,894). **All thresholds in this work are expressed and applied in
`ska distance` units.**

## 2.4 Selection of a per-unit reference

Gubbins cannot use a multi-contig reference — its 0.1–10 kb sliding window would
scan across the chromosome I / chromosome II junction — so **completeness was
treated as a pass/fail gate, not a ranking term**: a candidate was admissible only
at **≤ 2 contigs**. Among admissible candidates, the genome closest to the cluster
centroid was chosen (a *constrained medoid*), with contig N50 and total length as
tie-breaks. An unconstrained medoid is not adequate: for one cluster it selected a
135-contig draft.

Twelve of the 45 analysable units contained an admissible internal member. The
remaining **33 units borrowed a complete reference from another unit**, in every
case within **Mash 0.005** of the borrowing unit (median 0.00355, maximum
0.00479) — closer than *B. pseudomallei* K96243, which sits at 0.0073 from these
units and is used as the universal contrast reference (Section 2.6).
Borrow distances were computed with **Mash 2.3** at a **sketch size of 10,000, a
k-mer size of 21, and a minimum k-mer copy number of 1** (`mash sketch -s 10000
-k 21 -m 1`). These were resolved from the upstream Nextflow pipeline
(`wf-assembly-snps-mod`), whose `MASH_SKETCH` module takes them from
`conf/params.config`, together with the production run's recorded command line.

**One caveat should be stated in the paper rather than buried.** The pipeline
ships a *B. pseudomallei*-specific profile (`conf/profiles/bp.config`) that raises
the sketch size to **50,000**, on the explicit grounds that "default 10k is
undersized for 300+ BP genomes". The archived production run was invoked as
`-profile local_workstation_rtx4070,docker` — **without the `bp` profile** —
although the pipeline's own documentation gives the intended invocation as
`-profile bp,local_workstation_rtx4070,docker`. Several of that profile's
settings were supplied manually on the command line (`--max_cluster_size 50`,
`--recombination_aware_mode true`) but the sketch size was not, so it fell through
to 10,000.

The consequence is bounded and should be described as such. Mash-based clustering
was **abandoned** in favour of PopPUNK (Section 2.2), so the sketch size does not
affect the partition on which any result rests. It affects only the precision of
the borrow distances quoted in this section, which are used to rank candidate
references rather than to define units, and which are corroborated by the SKA and
SNP-level agreement reported alongside them.

## 2.5 Variant calling, recombination correction and phylogenetics

Each unit was processed per replicon. The reference was split with
`samtools faidx` **before** any downstream step, because Gubbins cannot handle a
multi-contig reference and `snp-sites` hardcodes `CHROM` to `1`.

**Variant calling.** Reference-free calling used **`ska map` (SKA2 v0.5.0)** via
`generate_ska_alignment.py` with **`--k 31`**. `ska map` was used rather than
`ska align` because only `ska map` carries genomic coordinates; `ska align` emits
columns in hash-table order, which does not correspond to physical position and
which Gubbins consumes **silently**. The k-mer length is not the tool default and
is not optional: at the default k = 17 a split k-mer spans 2×8+1 bases, which in a
68% GC, repeat-rich 7.2 Mb genome is far from unique, and the repeat mask removed
59% of chromosome 2 — enough to trip Gubbins' `--filter-percentage 25` and drop
nearly every taxon. At k = 31 the same data masked 3.5%, against 2.6–4.3%
unaligned for a mapping caller on the identical reference and genomes, confirming
the loss was a k-mer artefact rather than divergence.

**Alignment guard.** Every alignment was asserted rectangular (all records equal
length) before Gubbins. This is a prophylactic check: a fallback path that copies
raw concatenated sequence into a file the next tool treats as an alignment
produces very large branch lengths with no recombination involved, and is
expensive to diagnose downstream.

**Recombination correction.** **Gubbins v3.4.3** was run on the **full-length
pseudogenome alignment** — never a variant-site alignment, since the genomic
distance between variant sites is an input to the method — with
**`--invariant-site-correction` passed explicitly** and `--filter-percentage 25`.
The explicit flag matters because v3.4.2 made this correction optional and
defaulted it off, and the bundled `VERSION` file reads `3.4.2` even on tag
v3.4.3, so `--version` can misreport a correct install; package metadata was
checked in addition. Gubbins invokes RAxML v8.2.13 internally.

Partitioning before Gubbins is not merely a tooling constraint. *B. pseudomallei*
recombination is clade-specific — frequent within clades and rare between them,
because clade-specific restriction–modification systems block non-self DNA uptake
— so per-unit correction matches the organism's biology. Gubbins is documented for
samples of limited diversity sharing a recent common ancestor, and its detection
degrades as point-mutation density approaches recombination-import density.

**Variant-site extraction.** `snp-sites` was run **after** Gubbins, on the
filtered polymorphic sites, and nowhere earlier.

**Constant-site counts.** Counts were taken with `snp-sites -C` from the **full**
alignment, not from Gubbins' `filtered_polymorphic_sites.fasta`. The latter is
SNP-only by construction and returns `0,0,0,0`, which would silently defeat the
correction it is meant to supply; the pipeline refuses an all-zero vector rather
than building a tree from it. Measured counts on the full alignment
(467202,1026217,1020414,465056) correspond to 68.7% GC, matching K96243's 68.06%.
**Stated limitation:** this counts constant sites over the alignment *as it
entered* Gubbins, so constant positions inside masked recombinant tracts are
included; Gubbins does not emit a masked full-length alignment by default.

**Phylogenetics.** Trees were inferred with **IQ-TREE v2.4.0** on the
Gubbins-filtered polymorphic sites, with model selection (`-m MFP`), 1,000
ultrafast bootstrap replicates (`-B 1000`), and **`-fconst`** supplied from the
constant-site counts above. Ascertainment-bias correction (`+ASC`) was not used:
`-fconst` with true counts reproduces full-alignment base frequencies exactly,
whereas `+ASC` and flat counts both collapse composition toward 25/25/25/25 in a
genome of 68% GC.

## 2.6 The stopping rule, and how it was calibrated

The field's stated rule — subdivide "until the diversity observed fell within the
limit of recombination detection" — **cannot be implemented as written, because
Gubbins publishes no divergence ceiling.** Its absence was confirmed against the
primary publication, manual, documentation site and manpage. Existing pipelines
hard-code a *size* gate rather than a diversity gate. **We therefore measured the
operating range directly, and we state plainly that the resulting rule is a
construct calibrated on this dataset, not a published constant.**

Calibration used a **reduced 4-arm protocol** per unit — two references (the
unit's constrained medoid, and K96243 as a universal contrast) × two replicons —
validated to reproduce the full 12-arm protocol. All reported statistics are read
from the **reference-free `ska_map` caller against the unit's own close
reference**; a mapping caller adds roughly 9,000 phantom positions and inflates
root-to-tip slopes. The evidence base is 6 full 12-arm runs, 13 reduced 4-arm
runs and 2 L1 sub-cluster runs, with 91 clusters measured for diversity.

Per unit, the headline union coverage, pooled r/m and median tract length are the
**mean of the two `close` arms** (chromosome 1 and chromosome 2).

### 2.6.1 Gate 1 — diversity

Units were required to fall in **≈1,270–4,671 mean pairwise core SNPs**. The
calibration below was performed in **`ska distance` units**; the window applied
to this collection is its translation into **alignment-derived** mean pairwise
core SNPs, **[700, 4,700]**, with the floor bracketed **(588, 755]**.

**The two bounds translate very differently, and the reason the translation was
necessary is instructive.** Membership had been decided from a Mash-to-SNP
conversion (`mash × 3,805,619`) whose own documentation describes it as
triage-grade, and which is in neither unit system. Against distances computed
directly on each unit's core alignment it overstates diversity by a median
**1.30×**, by up to **17.20×**, and is more than 2× off for **17 of 85 units**.
Applying the unchanged bounds to alignment distances **reclassifies 22 of 85
units** — a quarter of the panel.

The **ceiling translates essentially unchanged** (4,671 → ≈4,700), located where
median recombination tract length falls from 3.77 kb to 2.69 kb. The **floor does
not**: it sits near 700, not 1,270. It was located on the same independent
criteria used in the original calibration — union recombination coverage and
median tract length, **not** r/m, which would be circular — and the lowest
diversity band reproduces the original failure signature closely: **union
coverage 4.3% and a 1.12 kb tract**, against the 0.7% and 1,002 bp recorded below
for a cluster at 405. The relocated floor bracket is **1.28× wide**, against
3.1× for the `ska`-unit floor.

The window's structure is unaffected by the change of metric and is in fact
sharper in alignment units: median r/m across equal-count diversity bands runs
1.53 → 7.25 → 8.39 → **8.59** → 3.68 → 2.14. The in-window median is insensitive
to floor placement across the whole bracket (7.70–7.78).

Two limitations are disclosed. Alignment SNP counts are not *provably* identical
to `ska distance` — SKA counts split k-mers over whole assemblies, this counts
SNPs on a reference-mapped core alignment — though the ceiling agreeing to within
1% across the two systems is a point in favour. And **union coverage does not
reproduce the calibrated 76–88% anywhere in this panel**: the highest band median
is 68%, and coverage *rises* with diversity, peaking in bands the gate rejects.
The floor does not depend on that criterion, but it does not reproduce
quantitatively.

Six consecutive clusters spanning 2,690–4,671 behaved consistently across 12
replicon measurements: union coverage 76–88%, pooled r/m 3.4–12.1, and median
tract 4.7–7.1 kb against a literature tract length of ~5 kb. Seven consecutive
clusters from 6,342 to 13,826 collapsed, with r/m 0.16–1.73 on both replicons.
Below the floor, recombination detection failed outright: a cluster at 405 gave
union 0.7% and an abnormal 1,002 bp median tract.

**Both bounds are brackets, and are reported as such.** The floor is bracketed to
**(405, 1,268]** — still 3.1× wide — and rests on one cluster either side; it
moved by more than a factor of two when the gap beneath it was first measured.
The ceiling is bracketed to **(4,671, 6,342]**, a 1.36× interval, and **has a
counter-example**: one continuous cluster at 9,617 has a sound root-to-tip slope,
the only one of seven above the ceiling to do so. The ceiling is therefore a
strong tendency, not a law, and the gate refuses that cluster on diversity as the
conservative choice.

### 2.6.2 Gate 2 — modality, applied second

Units passing the diversity gate were screened for multimodality. **The order is
load-bearing:** `gap/mean` divides by the mean, so on very tight clusters a
single divergent genome produces an enormous ratio. A calibration attempt that
included out-of-range clusters failed at every sample size, with the continuous
p95 *rising* with n — impossible for sampling noise, and the signature of a
mis-composed panel.

Thresholds were calibrated by **subsampling clusters whose structure is
unambiguous at full size** (7 continuous, 3 mixture, all in-range) down to smaller
n, 25 replicates per size; subsampling preserves the ground-truth label, so any
change is a pure size effect. The adopted rule is:

> **At n ≥ 25, classify a unit as a mixture if `gap/mean` > 1.0 OR
> `empty_bins` > 0.45.**

This catches 100% of known mixtures from n = 25 upward at a 15–21% false-mixture
rate. The asymmetry is deliberate: a mixture that slips through is caught
downstream by r/m, whereas a continuous unit wrongly rejected is a silent loss.

**Two statistics are required because they detect different mixture shapes.**
`gap/mean` catches a tight core plus outliers (one large gap over a small mean);
`empty_bins` catches several clumps over a wide range, where each gap is small
relative to a large mean. One cluster that is demonstrably 4-modal on its
histogram scores `gap/mean` = 0.128 and is missed entirely, while `empty_bins`
= 0.60 flags it.

**Below n = 25 modality is undecidable.** Both statistics overlap between classes
at every threshold tested; this is a limit of the data, not of tuning.

**Which statistic fires predicts whether subdivision will help** — offered as a
working hypothesis from two cases rather than a result. `empty_bins` high with
`gap/mean` low indicates several substantial modes and subdivision is worthwhile:
one 150-genome unit split into a usable 45-genome in-range unit plus a
95-genome clonal expansion at mean 140 SNPs (far below the floor, unusable for
recombination inference, but of independent interest as a probable outbreak or
heavily-sampled sublineage). `gap/mean` high indicates a tight core plus a few
outliers and subdivision is futile: a second unit's apparent mean of 2,378 was
manufactured almost entirely by 4 divergent genomes, and its 33-genome core
measured 485.

### 2.6.3 Post-hoc screens — union coverage and pooled r/m

**Neither statistic detects both failure modes**, which is why single-statistic
approaches failed: below the floor union collapses toward ~1% while above the
ceiling **union stays normal** and only r/m collapses.

**Union coverage** is the fraction of the replicon flagged recombinant on at
least one branch, computed as a merged interval union rather than a per-branch
sum. A threshold of **≥ 47%** was applied during calibration.

> **⚠ THIS SCREEN DID NOT SURVIVE THE PRODUCTION RUN AND MUST NOT BE APPLIED AS
> A FIXED CUTOFF. See "Union is size-confounded" below.** The subsections
> immediately following describe the calibration as performed; the limitation
> supersedes them.

The cutoff was originally justified as insensitive: sorted union across the 19
calibration units left a 41.4-point empty band between 18.0% and 59.5%, so any
threshold in 0.20–0.58 classified them identically. **Both halves of that
justification have since failed** — production units populated the band, and the
underlying statistic turned out to depend on sample size.

#### Union is size-confounded and is not comparable across units

**Union coverage is substantially a function of the number of genomes in a
unit.** Across all 45 units, spanning n = 7–155 — a range the calibration set
lacked, being almost entirely n ≈ 50 — union correlates with size at
**r(log n, union) = +0.80** (p = 4×10⁻¹¹), against **+0.28** with diversity
(p = 0.062). Mean union is **74.9%** for units with n ≥ 45 and **43.9%** for
n < 25, the latter falling below the cutoff as a group.

**The size effect is not a proxy for diversity.** Unit size and diversity are
uncorrelated in this collection (r = −0.01, p = 0.95), so there is no confound to
control; holding diversity constant *strengthens* the size effect to a partial
**r = +0.84** (p = 2×10⁻¹²). The partial analysis also revises a secondary
conclusion: diversity has a genuine independent association with union coverage
of **+0.48** (p = 0.0009), roughly double its marginal +0.28, which is diluted by
the much larger size effect. An earlier reading of the marginal correlation as
indicating that diversity is not a driver was therefore understated.

The mechanism is structural rather than biological: union counts sites
recombinant on **at least one** branch, so a larger unit has more branches and
more opportunity for any given site to be flagged somewhere. It is a cumulative
statistic and cannot be compared across sample sizes without normalisation. A
paired within-lineage test confirms this directly — subdividing one unit reduced
branch count 3.4× (299 → 89) and lowered union from 59.5% to 49.5%, consistently
on both replicons, while pooled r/m simultaneously *rose* from 2.57 to 4.94.

**Consequences, all of which apply to the results reported here:**

1. **A fixed union threshold acts as a size filter.** Seven units returned union
   below 47% while carrying pooled r/m of 5.90–10.61 — including one (n = 17)
   with the highest r/m in the entire study (10.61) and a union of 42.1%. These
   are very likely false rejections.
2. **Genuine under-detection remains detectable**, because it collapses **both**
   statistics simultaneously (union 0.7–41.4% with r/m 0.07–2.19). It is
   union-only failures that are unreliable.
3. **Small units should be judged on r/m rather than union.** This inverts the
   original assumption that union was the better-evidenced detector.
4. **The 47% cutoff and the 78% literature anchor were both established on
   n ≈ 50 units** and do not transfer to other sizes.
5. **Any diversity threshold derived from union is confounded**, because unit
   size and diversity are not independent in this partition.

**The cutoff is deliberately not anchored to the literature.** An earlier
derivation set it at 0.6 × 78%, where 78% is the published fraction of K96243
ever recombined; that derivation was abandoned in favour of the empty band, which
is internal to the measured data. This matters because the two quantities are not
commensurable: 78% is a **species-wide** figure for one genome, whereas union as
measured here is the fraction of a replicon recombinant on ≥ 1 branch **within a
shallow unit**. One unit measured 98.0% union — exceeding the species-wide figure
by 20 points — with correspondingly high pooled r/m (9.99) and per-branch
recombination burden (5.4–6.2 versus 2.0–2.7 elsewhere) and entirely normal block
sizes, i.e. genuinely recombination-rich rather than over-called. The 78% figure
is therefore cited as context only, not as a value the data should reproduce.
⚠ **A stale paragraph stood here and has been deleted (2026-08-23).** It read:
*"Union coverage was checked and found **not** to scale with unit size
(r = 0.142 against n) or with branch count (r = −0.059), so a single cutoff is
applicable across the 20-fold size range spanned by the units."* **That directly
contradicts this same section**, which establishes above that union coverage
**is** size-confounded — `r(log n, union) = +0.80` (p = 4 × 10⁻¹¹), partial +0.84
— and it is the earlier, superseded measurement. A single union cutoff is
therefore **not** applicable across the size range, which is why union is used as
a disclosed post-hoc screen rather than as a gate. Note also that union has
little dynamic range at the top of its scale and becomes uninformative there.

Independent corroboration comes from tract length —
every unit above 18% union has a median tract of 4.3–7.1 kb, and the single unit
with an abnormal tract (1,002 bp) is the only case where detection is *broken*
rather than merely sparse.

**Tract length is a property of the variant caller as much as of the biology, and
must be read that way.** All values here come from `ska map`. Two analysed units
(`s1_L1_19`, n = 34; `s1_L1_9`, n = 90) were re-called with snippy against the
same reference under identical Gubbins and tree-builder settings, so that only
the caller differs. Across all four paired replicons the median tract falls from
**5,388 bp under `ska map` (range 5,256–5,867) to 3,553 bp under snippy (range
2,717–3,879)** — a ratio of 0.64, with every measurement below one — while union
coverage is essentially unchanged (68.4→68.8% on `s1_L1_9` chr1). The callers
partition the *same* recombinant sequence into a larger number of shorter tracts
rather than rescaling one another. The mechanism is understood: SKA2's split k-mers cannot
call a variant whose flanking window carries another variant, so recovery of SNPs
within 10 bp of a neighbour is ~15% of snippy's, ~72% at 10–31 bp, and
indistinguishable beyond the k = 31 boundary (Section 2.11). **A reader using a
mapping-based caller should expect tract lengths near half those reported here.**

Two things this does *not* undermine. **Pooled r/m does not shift in a consistent
direction, and the two units move opposite ways**: `s1_L1_19` returned 1.96 under
snippy against `ska map`'s 2.30 (15% lower), while `s1_L1_9` returned 5.69
against 4.28 (33% higher). Neither matches what the SNP-recovery deficit alone
would predict, because losing clustered SNPs changes which tracts Gubbins
resolves as well as how SNPs are apportioned between recombination and mutation.
No caller correction factor should be inferred from either unit. Critically, the
two units sit on opposite edges of the empty r/m band and both move *away* from
it, so the band — and the coverage split that rests on it (Section 2.7) — is not
an artefact of the variant caller. And the clustered SNPs snippy recovers are not mapping
artefacts: they are not enriched in self-aligning repeats (28 of 2,474 under
permissive detection) nor in mobile elements or rRNA (21 of 3,144; zero in rRNA),
and are *depleted* in coding sequence (56% vs 89.6% for isolated SNPs, against an
85% coding genome) — the distribution expected of recombinant tract boundaries,
not of mismapping.

**Pooled r/m is reported as a continuous covariate. No r/m threshold is applied,
and the r/m ≥ 3.0 acceptance gate used in earlier drafts is withdrawn.** Three
independent findings made the gate indefensible, and we report the withdrawal
because each is easy to repeat.

First, **the cutoff's entire empirical support has been removed from the study.**
The value 3.0 was chosen to sit in a local gap, resting on one unit either side —
`strain_13` at r/m 2.89 and `strain_12` at 3.77. Both are PopPUNK strain units,
and the whole nine-unit strain block was subsequently withdrawn as composite
(Section 2.7). Nothing in the current unit set supports the number.

Second, **the null cannot calibrate any boundary in this region** (Section 2.8.3):
its entire support is [0, 0.00668] against a nominal boundary of 3.0, so a
p-value cannot distinguish r/m 2.03 from 12.89.

Third, **the spike-in shows detection is comparably reliable on both sides of it**
(Section 2.8.4): recovery is 91% at the ν measured in every unit, so a low r/m is
not evidence that detection failed.

**What the data show instead of a threshold.** Across the 37 analysed units
pooled r/m runs from 0.04 to 12.89, and the distribution is not uniform: there is
an **empty band 1.98 units wide, from 2.30 to 4.28, containing no unit at all**.
Eleven units (198 genomes) fall below it and twenty-six (853 genomes) above it.
The grouping is therefore a property of the data rather than of a chosen number,
and **any cutoff placed anywhere within that band yields the identical
partition** — which is why withdrawing the 3.0 convention changes no coverage
figure in Section 2.7.

Two honest qualifications. **The 1.98 band is not the largest gap in the
distribution** — a 2.25-wide gap sits higher up, between 10.61 and 12.86, and it
separates nothing meaningful. Gap width alone is not evidence of a class boundary;
what distinguishes the lower band is that it coincides with the point where union
coverage independently agrees (below). And the band is empty **partly because the
two units that occupied it were withdrawn for unrelated reasons**; had the strain
block survived, the region would be populated and no band would exist.

**A retracted claim that must not survive into the manuscript.** Earlier text
argued that because every analysable unit sits inside the diversity range, the
above-ceiling branch of the r/m failure mode is "excluded by construction", so a
low r/m must indicate bridging. **That does not hold.** The r/m decline appears to
begin *below* the nominal 4,671 ceiling — the four highest-diversity in-range
units average r/m 3.05 against 7.19 for the twelve below ska 3,900. A low r/m on a
high-diversity unit is therefore **ambiguous between bridging and ceiling onset**,
and the ambiguity is the finding. The evidence is four points and non-monotone, so
no gradient should be claimed from it either.

**This bears directly on the compromise described in Section 2.7**, since r/m is
the only post-hoc check on the 360 unscreened genomes. That check is a continuous
covariate, not a categorical test, and is reported as one.

One screened unit (n = 34, diversity 3,956) returned r/m 2.30 with entirely
normal union (78.1%) and tract length (5,261 bp). Three candidate explanations —
a near-threshold `empty_bins` score, high within-unit distance spread, and
elevated `gap/mean` — were each tested against the other completed units and each
refuted, in every case by a unit sharing the same value of the putative predictor
while returning a high r/m. The observation is reported as unexplained.

**A tempting screen that was tested and refuted, and should not be revived.** The
hypothesis that residual undetected recombination (78% − union) drives slope
inflation predicts that a stricter union threshold would identify datable units.
It does not: the unit with the **highest** union (86.5%) has an inflated slope,
and the unit with the **lowest** (18.0%) has a sound one. **Union predicts whether
recombination was found; diversity predicts whether a unit can be dated.** No
union requirement is imposed on dating.

**Dating.** Dating is refused above **4,700 `ska` units**, a bound that coincides
with the r/m collapse bracket. Root-to-tip slopes are judged on **magnitude
only**, read from the reference-free caller.

## 2.7 The analysable set: candidates, and the measured yield

**A distinction that must be preserved in reporting.** Applying the two gates to
the 2,802-genome collection nominated **1,233 genomes across 45 units (44.0%)** as
*candidates*. That figure is not a coverage result — it counts units that had not
yet been analysed. Every candidate was subsequently run, and the analysed set is
**1,051 genomes across 37 units**, of which **853 genomes across 26 units** sit
above the empty r/m band described in Section 2.6.3.

| Source | Candidate units | Candidate genomes | Modality-screened | **Above the r/m band** |
|---|---|---|---|---|
| L1 sub-clusters, n ≥ 25 | 11 | 660 | yes | **9 / 598** |
| L1 sub-clusters, n < 25 | 25 | 360 | **no** | **16 / 224** |
| ~~PopPUNK strains~~ **withdrawn** | 9 | 213 | **no (exempted)** | **0 / 0** |
| L1 sub-cluster recovered from strain 13 | 1 | 31 | yes | **1 / 31** |
| **Total** | **37** | **1,051** | | **26 / 853** |

**The final column is descriptive, not a filter.** Since no r/m threshold is
applied (Section 2.6.3), every one of the 37 analysed units is reported with its
measured r/m, and downstream users may draw the line wherever they judge
appropriate — or nowhere. The 26/853 figure is given because the 2.30–4.28 band is
empty, so *any* cutoff inside it produces this same split; it is a statement about
the shape of the distribution, not a decision imposed on the reader.

**The eleven units below the band are not a homogeneous class, and should not be
reported as one.** They carry r/m from 0.04 to 2.30, but union coverage — an
independent statistic — agrees with the low r/m in only **eight** of them, where
union runs from 0.4% to 41.4% and both measures point at genuine under-detection.
The remaining **three have entirely normal union coverage**: `s3_L1_10` (62.8%),
`s1_L1_13` (54.5%) and `s1_L1_19` (78.1%). In those three, Gubbins located
recombinant tracts perfectly well and simply assigned few SNPs to them, which is
the pattern expected from either a bridged unit or the onset of the diversity
ceiling — and, per Section 2.6.3, those two causes cannot be told apart here. They
are reported individually rather than pooled into a failure category.

**Coverage is 30.4% of the 2,802-genome collection, or 35.1% of the 2,430
genomes that were ever eligible for sub-partitioning.** Both figures are given
because the difference is entirely a matter of what counts as having been
attempted: 372 genomes lie in PopPUNK strains with fewer than six members and
were never candidates for any analysis. A coverage percentage quoted without its
denominator is not interpretable.

**The deliberate compromise, and how it actually performed.** 360 genomes in 25
units entered without a modality screen, because both screening statistics are
undecidable below n = 25 (Section 2.6.2); the safety net was pooled r/m, which
fires only *after* recombination correction, so some wasted analysis was
anticipated. The measured yield of that block was **64%** — lower than the
screened block's 82%, but substantially better than the pre-run concern implied.

**The worst-performing block was the one exempted from screening on the weakest
grounds.** The nine PopPUNK strains were admitted without modality screening
because they are strains rather than sub-clusters, an exemption never supported by
measurement. They returned the lowest yield of any block (56%), including two
units failing both detection screens. Being a strain rather than a sub-cluster
confers no protection against a bridged distribution, and the exemption should not
be repeated.

**Tree resolution was measured but deliberately not used as an acceptance
criterion.** Median ultrafast-bootstrap support is genuinely independent
information: across the 26 units above the r/m band it is essentially uncorrelated
with pooled r/m (r = −0.164) and only weakly related to unit size (+0.148), while
correlating with diversity (+0.552). One unit returned pooled r/m of 10.43 — among the
highest measured — with a median UFBoot of 43, i.e. recombination assigned well
and a tree that resolves little.

We initially adopted a **median UFBoot ≥ 70** gate on the worse replicon and
subsequently withdrew it, for two reasons that we report because both are easy to
repeat. First, the threshold was **on the wrong scale**: IQ-TREE's ultrafast
bootstrap is not the standard nonparametric bootstrap, whose ≥ 70 convention we
had cited; UFBoot's own "supported" line is ≥ 95, so our gate was substantially
*more* permissive than the convention invoked to justify it. Second, and
decisively, the resulting coverage figure is **almost entirely a function of that
choice**:

| Support threshold | Units | Genomes | Coverage |
|---|---|---|---|
| **none (reported)** | **26** | **853** | **30.4%** |
| UFBoot ≥ 70 | 19 | 652 | 23.3% |
| UFBoot ≥ 80 | 15 | 583 | 20.8% |
| UFBoot ≥ 90 | 9 | 425 | 15.2% |
| UFBoot ≥ 95 | 6 | 164 | 5.9% |

A headline that moves **5.2-fold** across the range of defensible conventions
describes the convention rather than the collection. *(Computed on the 26 units
above the r/m band and on the current unit set; an earlier version of this table
was computed before the strain block was withdrawn and reported 30 units / 933
genomes / 33.3% at the top row.)*

**Poorly supported branches were therefore collapsed rather than used to exclude
units.** For each tree, internal edges with support below the collapse threshold
were deleted and their children reattached to the parent, converting unresolved
nodes into polytomies; branch lengths were preserved additively so root-to-tip
distances are unchanged, and terminal branches were never collapsed. At the
UFBoot ≥ 95 convention this removes **58%** of internal branches across the 180
trees (34% at ≥ 70, 41% at ≥ 80). That figure is reported as the primary
description of tree resolution, in preference to a pass rate. **All downstream
analyses must therefore accommodate polytomies.**

**The nine whole-strain units were withdrawn after sub-partitioning showed them
to be composites.** They had been admitted without modality screening on the
grounds that they were PopPUNK strains rather than sub-clusters — a category
exemption never supported by measurement. Completing the fastbaps partition
across all 42 strains showed that their apparent diversity was produced by
mixture structure: `strain_8`, at an apparent 1,265 mean pairwise SNPs, resolves
into a 36-genome clonal core at **55** SNPs plus outliers (gap/mean 8.697);
`strain_12` (3,210) resolves to a core at 873; `strain_17` (3,252) to cores at
846 and 112. Only `strain_13` contained a core inside the analysable range, and
that core (`s13_L1_1`, n = 31) returned pooled r/m **12.89** against the whole
strain's 2.89 — a 4.5-fold increase from removing five genomes.

**Reporting rule.** Quote **30.4% (853 genomes, 26 units)** of the collection,
with **35.1%** of the eligible 2,430 alongside. The 44.0% candidate count should
appear only as the size of the set submitted for analysis, never as a result.

**Validation of the borrowed-reference configuration.** 33 of 45 units ran
against a borrowed reference, every borrow within Mash 0.005 (median 0.00355,
maximum 0.00479). Borrowed and internal-medoid units are **statistically
indistinguishable as classes** (medians, borrowed vs internal: union 41.4% vs
45.1%; pooled r/m 5.29 vs 6.80; tract 5,414 vs 5,789 bp; median support 80.5 vs
89.0; Mann–Whitney *p* = 0.14–0.45).

**A class comparison is, however, the wrong test, and it conceals a
dose–response.** Regressing each statistic on the borrow distance actually used
(range 0.0008–0.0048) gives a consistent decline with distance: pooled r/m
**r = −0.38 (p = 0.028)**, median support −0.34 (p = 0.057), tract length −0.32
(p = 0.068), union coverage −0.31 (p = 0.083). Borrow distance is uncorrelated
with unit size (−0.17, p = 0.35) and with diversity (+0.07, p = 0.71), and
controlling for either leaves the r/m coefficient at −0.40. The effect is
therefore not a size or divergence artefact, and it operates **within** the
distance bound we imposed.

We report this rather than the class comparison alone because the bound itself
was never validated: it was set *a priori* and confirmed on a single unit, and a
single observation at a single distance cannot detect a gradient. **The Mash
0.005 bound should be read as a recorded assumption, not a measured safe limit**,
and the nearest admissible reference should be preferred even where a more
distant one falls inside it.

All 45 units were analysed (180 arms, no failures).

**How the completed runs are reported.** **No unit is excluded by a threshold on
either statistic.** All 37 analysed units are reported with their measured union
coverage, pooled r/m, median tract length and median UFBoot, and the two
detection statistics are read together rather than as gates:

| pattern | units | genomes | reading |
|---|---|---|---|
| union and r/m both high | 26 | 853 | recombination detected and assigned; no caveat |
| union and r/m both low | 8 | 112 | genuine under-detection — two independent measures agree |
| r/m low, union normal | 3 | 86 | tracts found but few SNPs assigned; **ambiguous** between bridging and ceiling onset (Section 2.6.3) |

Union coverage is **not** applied as an independent criterion, because it is
size-confounded: 17 units return union below the nominal 47% while carrying r/m of
5.29–12.86, and union correlates with log unit size at r = +0.81. Treating those
as failures would have been a false rejection driven by *n*, not by biology. The
conjunction in row two is meaningful precisely because the two statistics are
confounded in different directions — union by size, r/m by diversity — so their
agreement is harder to explain as an artefact of either.

## 2.8 Method validation

Five experiments bound the behaviour of the pipeline itself rather than of the
collection. Two close limitations previously carried as open; two bound the false
-positive and false-negative rates of recombination detection; one excludes three
alternative explanations for the unexplained low-r/m residue.

### 2.8.1 Constant-site handling does not affect any relative quantity

Constant-site counts supplied to IQ-TREE via `-fconst` can be taken permissively
(all constant positions) or conservatively (excluding constant positions inside
masked recombinant tracts). The two were computed across **62 unit-replicons**
and compared.

Conservative counting removes a median of **0.0%** of constant sites
(range −0.5% to 1.1%). Total tree length moves by a median ratio of **1.001**
(range 0.994–1.011), and per-branch lengths matched on shared splits correlate at
a median **r = 1.0000**, minimum **0.9988**.

**Branch lengths are near-perfectly correlated, so the choice does not change
which tree is recovered — only its scale, and by at most 1.1%.** The limitation
is closed for any topological or relative-branch use. We report the permissive
count and state the bracket. One caveat is worth stating explicitly: topology
agreement measured as shared splits is a median of 100% but falls to **69.1%** in
the worst unit, so the invariance claim is about branch-length scale, not about
identity of every split in every unit.

### 2.8.2 The recombination estimate is robust to the ML tree builder, but not to a distance-based one

Production runs Gubbins under its default RAxML builder; the simulation arms use
IQ-TREE. Because a builder effect would confound any comparison between them, the
two were run on the same real alignments — **6 units × 2 replicons = 12
comparisons**, chosen to span the r/m range from 1.81 to 14.13. A third builder,
**rapidnj**, was measured on the identical design because the upstream Nextflow
pipeline was invoked with it (Section 2.10); its result is reported below and is
materially different.

| quantity | agreement |
|---|---|
| r/m ratio (IQ-TREE / RAxML) | median **0.988**, range 0.850–1.126 |
| r/m deviation | median **2.3%**, worst 15.0% |
| union coverage, absolute difference | median **0.3 pts**, maximum 1.5 pts |
| correlation of r/m across builders | **r = +0.9890** |
| units changing side of the empty r/m band | **0 of 6** |

**The builder choice does not relocate any unit within the r/m distribution.**
Taking unit-level means across both replicons, the six units sit at 2.03, 2.30,
3.77, 5.80, 9.15 and 12.89 under RAxML and at 1.98, 2.30, 3.81, 5.81, 8.88 and
12.11 under IQ-TREE: none crosses the empty 2.30–4.28 band, and `s1_L1_19` returns
2.30 — the band's lower edge — under both. (`strain_12`, at 3.77/3.81, is the one
unit sitting inside the band under either builder; it belongs to the withdrawn
strain block and is not part of the analysed set.)

The result is reported as a gradient rather than a pass/fail, and deliberately so:
an earlier version of this test returned a binary on whether the worst deviation
exceeded 15%, and it came out at **15.004%** — a verdict decided by four
thousandths of a point. That is the same round-number failure documented three
times elsewhere in this work, and it is now the second reason this section reports
numbers instead of verdicts; the first is that the acceptance gate those verdicts
referred to has since been withdrawn entirely (Section 2.6.3).

**rapidnj is NOT equivalent, and the difference is directional.** Run on the same
12 alignments, the distance-based builder **systematically underestimates r/m**:

| comparison | median ratio | median \|deviation\| | worst | ratios below 1.0 | sign test |
|---|---|---|---|---|---|
| IQ-TREE vs RAxML | 0.988 | **2.3%** | 15.0% | 7 of 12 | p = 0.77 |
| **rapidnj vs RAxML** | **0.922** | **7.8%** | **45.5%** | **11 of 12** | **p = 0.0063** |
| rapidnj vs IQ-TREE | 0.938 | 6.2% | 51.6% | 10 of 12 | p = 0.039 |

The two maximum-likelihood builders agree with no directional bias — the 7-of-12
split is exactly what chance predicts. rapidnj departs from both, in one
direction, at a magnitude three to four times larger, and the bias is significant
by a two-sided sign test.

**The bias belongs to the tree construction, not to the model fitting.** Passing
`--tree-builder rapidnj` does not produce a pure rapidnj run: Gubbins delegates
model fitting to IQ-TREE, because a distance-based method cannot fit a
substitution model. The citation manifests confirm this — the rapidnj arm records
`Model fitter → iqtree` with `Tree constructor → rapidnj`, against `iqtree` for
both in the IQ-TREE arm and `raxmlHPC-PTHREADS-AVX2` for both in production. The
third row of the table therefore holds the model fitter constant and isolates the
tree constructor alone, and the underestimation persists there (p = 0.039). It is
the neighbour-joining topology, not the model, that loses recombination signal.

**It also moves a unit across the empty band.** At unit level `s1_L1_19` falls
from 2.30 to 2.12, and `s2_L1_8` from 5.80 to 4.46 — the latter still above the
band but close to its 4.28 edge, where RAxML placed it comfortably clear.

**Consequence for reproducibility.** Every number reported in this work comes from
the RAxML production arm, so no result is affected. But a pipeline configured with
rapidnj would not reproduce them, and would report r/m values biased low by a
median of 8% and by as much as 46% in individual replicons. **We therefore pin the
tree builder to RAxML and recommend against distance-based builders for
recombination inference at this scale.** The finding also argues that
tree-builder equivalence should be verified per builder class rather than assumed
from a single comparison: agreement between two ML builders carried no
information about a distance-based one.

### 2.8.3 False positives: a matched zero-recombination null

**1,519 replicates across 62 unit-replicons.** Each replicate inherits, from the
real unit it matches, its tree, fitted substitution model, alignment length, base
composition and **per-genome missing-data pattern applied verbatim**; sequences
were simulated under that model with seq-gen 1.3.5 and passed through the
identical Gubbins invocation used in production. By construction the truth is
zero recombination.

**20 of 1,519 replicates (1.32%) produced any false-positive block**, one block
each. The maximum pooled r/m the null ever reached is **0.00668**; the median is
**0.000**. Observed values in the real units range from **2.85 to 14.92**, i.e.
**427× to 2,234× the null maximum**. Every accepted unit's recombination signal is
real and is not an artefact of tree shape, alignment length, base composition or
missing-data structure.

**The null cannot calibrate the acceptance threshold, and no number of extra
replicates would change that.** Its entire support is [0, 0.00668] against a
boundary of 3.0 — three orders of magnitude away, with no overlap. Consequently
every unit with any detected recombination receives the same minimum p-value,
1/(k+1) = 0.0385 at 25 replicates; 59 of 62 unit-replicons clear p ≤ 0.05, and
the three that do not are limited by replicate count rather than by signal. **A
p-value cannot distinguish r/m 2.03 from r/m 12.89**, because both sit hundreds of
times above anything the null produces. Units at the bottom of the r/m
distribution are as significant against this null as units at the top — **the
low-r/m units are not units in which recombination went undetected; they are units
with abundant real recombination and simply less of it relative to mutation.**
This is one of the three findings that led us to withdraw the r/m acceptance gate
altogether and report r/m as a continuous covariate (Section 2.6.3): a boundary
that no available null can calibrate, and on both sides of which detection is
comparably reliable, is not a boundary worth imposing on a reader.

The null carries one tree and no population structure, so it calibrates the
**recombination** role of pooled r/m only; its second role as a structure
detector is not calibrated here.

### 2.8.4 False negatives: spike-in of known tracts into real data

Sensitivity was measured by implanting recombinant tracts of known length and
known divergence into a real unit (`s13_L1_1`, chromosome 1), leaving every other
property of real data intact. Tracts are 5,000 bp; an implant counts as
**recovered** if a Gubbins block covers ≥ 50% of it *for that recipient taxon* in
the spiked run and not in the unspiked control. Implants landing where the control
already detected recombination cannot be attributed to the implant and are
excluded from the denominator rather than scored. Three replicates per divergence,
24 implants per cell.

| donor divergence ν | SNPs per 5 kb tract | recovered |
|---|---|---|
| 0.0005 | 2.4 | 4/20 = **20%** |
| 0.001 | 4.2 | 8/20 = **40%** |
| **0.002 — our measured value** | **9.0** | **19/21 = 91%** |
| 0.005 | 25.0 | 19/19 = **100%** |
| 0.01 | 45.0 | 19/21 = **90%** |

**At the ν measured in every unit (0.0021–0.0024), Gubbins recovers 91% of the
recombination that is really present.** Detection becomes reliable somewhere
between 4 and 9 SNPs per 5 kb tract, and the collection sits above that
threshold. **Our r/m values are therefore not systematically deflated by donor
similarity.**

Recovery **plateaus at roughly 90–100%** above ν = 0.002 rather than saturating
cleanly at 100% — the highest cell returns 90%. On three replicates and ~20
scorable implants per cell, 90% versus 100% is about two implants and is within
sampling noise, so the honest statement is a plateau rather than a ceiling. The
low-ν cells at 20% and 40% are what establish that the scoring rule is not
spuriously generous: a lenient criterion would have inflated those too.

Caveats: one base unit and one replicon; implants are terminal-branch imports
into a single recipient rather than clade-level events; the tree builder is
IQ-TREE, for which equivalence to production RAxML is quantified in Section 2.8.2.

### 2.8.5 Three alternative explanations for the low-r/m residue, all excluded

| hypothesis | test | result |
|---|---|---|
| Detected recombination is concentrated in mobile-element hotspots, so sharing reflects MGE content rather than genuine exchange | matched enrichment of shared blocks, cross-lineage versus inheritance-explicable pairs | **1.1× in both** — no excess where inheritance cannot explain sharing |
| Units differ in donor divergence ν, so r/m differences reflect detectability | ClonalFrameML decomposition (R/θ, δ, ν) on six units | **ν ratio 1.00**; ν varies more between replicons than between units |
| Units differ in callable fraction, so r/m tracks alignment quality | correlation of r/m against the standard deviation of callable fraction | **r = −0.183, p = 0.23** (Spearman −0.188) |
| Units differ in assembly fragmentation, so both detection statistics track assembly quality rather than biology | per-unit median contig count against union coverage and pooled r/m, 36 units | **union r = −0.216, p = 0.21; r/m r = +0.262, p = 0.12** (Spearman −0.212 and +0.165) |

None survives. Together with Section 2.8.3's exclusion of under-detection — the
residue units exceed the null maximum by more than 300× and therefore contain
abundant real recombination — the unexplained residue points at biology or at
residual population structure rather than at the method.

## 2.9 Analyses deliberately not performed

**The grafted whole-collection tree was not dated and its branch lengths are not
interpreted as distances.** Two residues prevent it, and we state them precisely
because an earlier draft of this section stated them wrongly. It is **not** the
case that the subtrees are expressed in substitutions per *variable* site: with
`-fconst` supplied from the full alignment (Section 2.5), the per-unit branch
lengths are already in substitutions per site of the full alignment, so the
scales are commensurable. What remains is (i) each unit was aligned against a
**different reference**, so "per site of the full alignment" denotes a different
set of positions in each unit, and (ii) recombination was corrected
**independently within each unit**, so the clonal frame from which vertical
substitutions are counted differs between them. The first is bounded and could be
quantified as the pairwise overlap of reference position sets; the second has no
standard solution. Correcting the backbone would not resolve either.

**Recombination correction was not applied to the backbone.** Gubbins assumes
limited diversity with a recent common ancestor, whereas the backbone
representatives are maximally spread by construction — precisely the regime in
which its calls stop being interpretable.

**An independent estimate of r/m was obtained for a subset, and it does not fully
agree.** Because pooled r/m is the principal covariate on which units are
characterised, ClonalFrameML 1.20
was run on six units — the three with unexplained low r/m and three
diversity-matched controls — on both replicons, with starting trees rebuilt
without recombination correction. Its decomposition of r/m into R/θ, δ and ν
shows **no difference in ν** between the two groups (ratio 1.00 on both
replicons), excluding the hypothesis that the depressed r/m reflects
recombination from donors too close to detect; ν varied more between replicons
within a unit (+6.7% to +13.3%) than between units within a replicon (≤8.1%).

ClonalFrameML's implied r/m was systematically higher than Gubbins' pooled value
(median 4.3×, range 1.7–8.0×) and **ranked the units differently** (Spearman
+0.31): the unit with the lowest Gubbins r/m had the second-highest
ClonalFrameML estimate. A systematic offset between two differently-defined
estimators is expected; a difference in ordering is not, since the acceptance
criterion is a threshold. **This is reported as an unresolved caveat rather than
a result** — six units provide almost no power to estimate a rank correlation,
and differential sensitivity to bridged population structure is an equally
consistent explanation. Extending the comparison to all 45 units is identified as
the highest-priority outstanding validation.

**Date-randomisation was not used to validate temporal signal**, being
anticonservative where temporal and genetic structure are confounded, as they are
here (Murray 2016, PMID 27110344).

**BETS (Bayesian Evaluation of Temporal Signal; PMID 32895707) was not run, and
is not merely unreported.** No BEAST XML, state, `.trees` or posterior log file
exists anywhere in the project, and no TreeTime or TempEst output does either;
the only BETS artefact present is a copy of the BEAST documentation, i.e. reading
material. It remains **planned rather than performed**, and is deliberately
deferred: no dating is attempted anywhere in this work, the grafted
whole-collection tree must not be dated for the reasons given above, and temporal
inference belongs to the separate analysis whose first requirement is a defensible
sampling frame rather than a merge.

## 2.10 Software and reproducibility

| Tool | Version | Provenance | Role |
|---|---|---|---|
| PopPUNK | 2.7.6 | env | strain definition (271 refined strains) |
| fastbaps | 1.0.8 (`r-fastbaps`) | env | phylogeny-conditioned sub-clustering (64 L1 units) |
| SKA2 | 0.5.0 | env | `ska distance` (diversity); `ska map` (reference-free calling, k = 31) |
| samtools | 1.17 | env | replicon splitting |
| Gubbins | 3.4.3 | **artefact** | recombination correction (`--invariant-site-correction`) |
| RAxML | 8.2.12 | **artefact** | invoked internally by Gubbins (`raxmlHPC-PTHREADS-AVX2`, GTRGAMMA) |
| pyjar | 1.0 | **artefact** | ancestral sequence reconstruction within Gubbins |
| snp-sites | 2.5.1 | env | variant-site extraction and constant-site counts |
| IQ-TREE | 2.4.0 | **artefact** | ML phylogenetics (`-m MFP -B 1000 -fconst`) |
| Mash | 2.3 | **artefact** | reference-borrow distances only (`-s 10000 -k 21 -m 1`; Section 2.4) |
| ClonalFrameML | 1.20 | env | independent r/m decomposition (R/θ, δ, ν) on six units |

**Provenance is stated per tool because the two sources are not equally strong.**
*artefact* means the version was read from the run output itself and is therefore
what actually executed: Gubbins 3.4.3 and IQ-TREE 2.4.0 each agree across all
184 production arms, and RAxML 8.2.12 across all 1,686 model-fitting and
tree-construction entries in the Gubbins citation manifests (`gubbins.log`).
*env* means the version was resolved from conda package metadata for the
environment the run demonstrably used, which pins the package but not the
timestamp — an environment rebuilt after the runs would not be detected this way.

Two version strings do not self-report consistently and are given as observed.
Gubbins' `VERSION` file reads 3.4.2 even on tag v3.4.3, so `--version` understates
it; the citation manifest is authoritative and reports 3.4.3. Conversely the
conda package is `raxml 8.2.13` while the binary self-reports 8.2.12 in every
manifest entry; 8.2.12 is what ran and is what is quoted above.

PopPUNK was run as BGMM fit followed by boundary refinement (`--fit-model bgmm`
then `refine`), backend sketchlib v2.1.5, yielding 271 network components — the
271 refined strains used throughout.

The toolchain spans three conda environments (`snp-phylogeny`, `bp-gubbins`,
`poppipe`) because Gubbins caps Python at 3.10; each pipeline step activates the
environment owning its tool. Per-unit runs are resumable at arm granularity.
Scoring is reproducible from the on-disk run directories via
`triage_analysable_bp.py`, whose self-tests assert the published union, r/m and
tract values for three reference clusters.

Every quantitative claim in Sections 2.6–2.7 is regenerated from the run
directories by `tier0_evidence_bp.py` (correlations, partial correlations, the
support-threshold sweep and the reference-borrowing analysis; 13 self-tests),
`mge_hotspot_audit_bp.py` (the shared-tract audit and its independence null; 10
self-tests) and `collapse_unsupported_bp.py` (branch collapsing; 18 self-tests).
Per-unit values are tabulated in `tier0_units.tsv`.

**Run-to-run reproducibility** was measured by chance, when one unit (n = 90) was
processed end-to-end twice against the same reference in independent invocations.
Union coverage was identical on all four arms (66.3 / 77.6 / 68.4 / 79.1%), and
pooled r/m and median tract agreed to within 0.2% (4.54 versus 4.55; 5,684 versus
5,694 bp). Residual variation is attributable to stochasticity in the Gubbins /
RAxML tree search. Reported statistics are therefore stable well below the
between-unit differences they are used to distinguish.

**Every concurrent invocation of Gubbins is given its own working directory, and
this is a correctness requirement rather than tidiness.** Gubbins writes several
intermediates — `<basename>.start`, `<basename>.phylip`, `<basename>.snp_sites.aln`
— into the *current working directory*, not into the path given by `--prefix`.
Concurrent runs whose input alignments share a **basename** therefore overwrite
and delete one another's scratch, regardless of how far apart their inputs and
outputs sit in the filesystem. The isolating property is the basename, not the
path: in this project only 30 distinct basenames occur across 184 production
arms, because every unit's arm against the common reference is named for that
reference's contigs.

The failure mode deserves reporting because of how it presents. It is invisible
in single-run testing, appears only under concurrency, and surfaces as
`FileNotFoundError` on a missing intermediate or as a model-fitting error that
points at the input rather than at the collision. In our own use it destroyed
roughly two-thirds of one simulation sweep at a rate **flat across a 250-fold
range of the parameter under study**, and was twice mistaken for a scientific
finding about that parameter before the cause was identified. A failure rate
independent of the variable being varied is diagnostic of the harness rather than
of the biology, and we recommend it as a standing check. Orphaned scratch
directories are the physical signature: Gubbins removes its per-iteration
temporary directories on a clean exit, so an accumulation of them counts runs
that died mid-iteration.

## 2.11 Known limitations

1. **The diversity floor is not established and could not be derived.** It is
   bracketed to (405, 1,268], a 3.1× interval, and **every observation supporting
   it is inadmissible**. Only three units fall below the bound; two are
   unambiguous mixtures (largest within-distribution gap over the mean of 1.55
   and 2.70), so their failures are attributable to population structure rather
   than diversity, and the third cannot be assessed because modality is only
   interpretable inside the diversity range whose lower bound is the quantity
   being derived — a circularity. Tree resolution was tested as an alternative
   basis and rejected: one unit at a mean pairwise distance of 535 returns a
   median bootstrap of 94.5, and resolution continues to rise into the
   high-divergence regime where recombination detection has already failed, so it
   measures phylogenetic signal rather than analysability. **The reported value
   should therefore be described as the lowest diversity at which a unit has been
   observed to work, not as a measured threshold.** Resolving it requires a
   unimodal unit of n ≥ 25 between 535 and 1,265, which the present partition
   does not contain.
2. **A quarter of the analysable set (360 genomes, 25 units) is unscreened for
   modality**, and the r/m safety net acts only post hoc (Section 2.7).
3. **The ceiling has an unexplained counter-example** — one continuous cluster at
   9,617 dates soundly (Section 2.6.1).
4. ~~**The r/m bridging cutoff rests on one point either side.**~~ **RESOLVED by
   withdrawal** (Section 2.6.3). No r/m cutoff is applied. The two points that
   were its only support, `strain_13` (2.89) and `strain_12` (3.77), both belong
   to the withdrawn strain block, so the cutoff had ceased to rest on anything at
   all. Units are now reported with continuous r/m.
5. **Thresholds were calibrated on size-capped fragments, roughly half of them
   bridged**, and must be re-verified against any new partition.
6. **Within-BioProject correlation is unmeasured**, leaving effective sample size
   uncertain across a wide range.
7. ~~**Constant-site counts include constant positions inside masked recombinant
   tracts.**~~ **CLOSED** (Section 2.8.1). Across 62 unit-replicons the two
   counting conventions move total tree length by a median ratio of 1.001 and
   correlate per-branch at r ≥ 0.9988, so the choice changes scale by at most
   1.1% and changes no relative or topological quantity. Residual caveat:
   shared-split agreement falls to 69.1% in the worst unit, so the invariance is
   demonstrated for branch-length scale, not for every split in every unit.
8. **No published benchmark exists for these tools on a two-replicon 7.2 Mbp
   genome**, and the behaviour of the subtree merge under recombination remains
   unresolved. **Partly addressed** in Section 2.8: detection is now bounded from
   both sides *on this genome* — false positives at 1.32% of 1,519
   zero-recombination replicates with a null maximum 427× below the lowest
   observed value, and sensitivity at 91% recovery at the measured ν — and the
   estimate is shown not to depend on the tree builder. **The subtree merge is
   still not validated**, and the sensitivity bound rests on one unit and one
   replicon with terminal-branch implants only, so it does not speak to
   clade-level imports.
9. **The grouping of units into "above" and "below" the empty r/m band is an
   observation about the present unit set, not a calibrated threshold**
   (Sections 2.6.3, 2.7). The 2.30–4.28 band is empty, so the 26/853 split is
   invariant to where a cutoff is placed within it — but the band is empty in part
   because the two units that occupied it were withdrawn for unrelated reasons,
   and a wider or differently partitioned collection may populate it. The band
   width (1.98) is also not the largest gap in the distribution; a 2.25-wide gap
   at 10.61–12.86 separates nothing meaningful. **Readers should treat r/m as the
   continuous covariate it is** and should not infer that units below the band
   failed detection — Section 2.8.3 shows they exceed the zero-recombination null
   by more than 300×.
10. **Three of the eleven low-r/m units are ambiguous between bridging and
    diversity-ceiling onset and cannot be resolved with the present evidence**
    (Sections 2.6.3, 2.7). `s3_L1_10`, `s1_L1_13` and `s1_L1_19` carry normal
    union coverage (54.5–78.1%) with low r/m. The claim in earlier drafts that the
    ceiling branch is "excluded by construction" for in-range units is withdrawn.
11. **Variant calling was done with `ska map`, whose split k-mers under-recover
    clustered SNPs** (Sections 2.5, 2.8.5). Measured against snippy on paired
    arms: ~15% recovery of SNPs within 10 bp of a neighbour, ~72% at 10–31 bp,
    parity beyond the k = 31 boundary. The consequence is **not** a uniform bias.
    Median tract length is materially affected — roughly halved under snippy — so
    the ~5 kb figure reported here is caller-dependent. Pooled r/m is not shifted
    in a consistent direction: on `refsens_cluster37` snippy ran 29–76% *higher*,
    on `s1_L1_19` 15% *lower*, and on `s1_L1_9` 33% *higher*. **No stable caller
    correction factor exists**, and none should be applied. The empty r/m band was
    tested from **both** edges and holds: `s1_L1_19` (lower edge, 2.30) moves to
    1.96 and `s1_L1_9` (upper edge, 4.28) moves to 5.69 — both *away* from the
    band, in opposite directions — so the band is not an artefact of the caller.
    The surviving untested alternative is indel-adjacent alignment artefact in
    snippy, which neither the repeat nor the annotation test covers.
12. **No assembly-quality screen was applied to the collection** (Section 2.1).
    The sole threshold is a 45 kB minimum file size that is non-binding by a
    factor of ~140, and no contig-count, N50, completeness or contamination metric
    was ever computed. The collection consequently retains 45 assemblies above 500
    contigs, 9 above 1,000 (maximum 3,097), and two assemblies ~48% larger than
    the median genome. **The effect on the reported statistics was tested and is
    not detectable** (Section 2.8.5): across 36 units with membership and contig
    counts, per-unit median contig count correlates with union coverage at
    r = −0.216 (p = 0.21) and with pooled r/m at r = +0.262 (p = 0.12), neither
    significant — and the r/m association runs *positive*, the opposite of the
    direction fragmentation would be expected to produce. The two oversized
    assemblies were inspected individually and diagnosed as duplicated
    chromosome II; neither enters any analysed unit nor was used as a reference,
    so the measured impact is nil (Section 2.1). **The residual risk is that the
    screen which found them was ad hoc.** No total-length or completeness check
    runs in the pipeline, so an equivalent artefact in a future collection would
    pass unnoticed — and the ≤ 2-contig reference-admissibility rule would treat
    it as a high-quality candidate. A total-length bound belongs in the pipeline
    alongside the contig-count rule.

---

# 2.12 The production analysis, as run

Everything in this section describes the analysis from which all reported results
derive. It supersedes the earlier 82-unit run described in previous drafts.
It was executed as a Nextflow workflow
(`github.com/PHemarajata/wf-assembly-snps-mod`) in **curated mode**, meaning the
partition and the per-unit mapping references were supplied rather than
re-derived inside the run. Where this section conflicts with 2.1–2.11, this
section is what was done.

Two runs are reported. The **reported partition** is the 22-core workstation
run, corrected: **85 units, 2,340 genomes** after the duplicate-BioSample and
register exclusions of 2026-08-21 (`FINAL_BASIS_2026-08-22/`). A second run
(88 units, which refines `strain_1_L1_26` into three) was executed on an NVIDIA
DGX Station A100 and serves as the **cross-hardware reproducibility control**;
2.12.10 uses it to establish comparability and to measure the effect of
refinement. Both completed with zero task failures.

**The reported partition is the corrected one.** Both runs carry the same seven
duplicate BioSamples; only this one has had them removed, and correcting the
A100 run would require re-deriving it, which was ruled out. Every alignment for
this partition is also local, whereas the A100's two refinement children have no
core alignment here and their r/m cannot be re-derived. The refinement is not
lost by this choice: 2.12.10 reports what it showed.

## 2.12.1 Genome panel

**2,976** *B. pseudomallei* assemblies were assembled and considered: **2,802**
from the established curated collection and **174** newly added isolates. Of the
additions, **169** are on SPAdes paths — **165 assembler swaps plus 4 isolates
rescued into the panel by re-assembly** — and 5 were retained from other
assemblers (2.12.2).

**Seventeen assemblies were then removed as duplicate BioSamples**, leaving an
analysed panel of **2,959**. Deduplication is on BioSample, not run accession: a
BioSample re-sequenced or re-deposited under several run accessions is one
isolate and would otherwise contribute repeated observations of the same
geography. Panel membership, exclusions and per-isolate assembler overrides are
recorded in `PANEL_EXCLUSIONS.tsv`, `PANEL_ASSEMBLY_OVERRIDES.tsv` and
`PANEL_RESCUES_2026-08-18.tsv`.

Of 188 SPAdes assemblies produced, 19 were not admitted: 13 duplicates of runs
already in the collection, 5 not *B. pseudomallei* or grossly divergent, and 1
mixed sample (`SRR30648681`, which SPAdes revealed as 12.00 Mb of foreign content
and which SKESA did not rescue). Every exclusion carries a recorded reason and
evidence.

**The exclusion register is versioned, and four rows were rescinded.** Rows carry
a `status` field; `status = retired` marks a decision that was withdrawn on
evidence and is retained for the record rather than deleted. Four rows
(`SRR2896257`, `SRR2896259`, `ERR9980356`, `SRR2896271`) were retired on
2026-08-23: each had been excluded for core-genome coverage below 85%, measured
on the SKESA assemblies, but the panel uses the SPAdes re-assemblies and on those
all four pass every gate (core 86.2–93.3%, gene-count ratio 0.89–0.97, mash to
K96243 0.0065–0.0093). The register's `core = na%` on those rows was a
transcription error rather than an unmeasured field — the value is in
`core_cov_unfiltered_pct` and the adjacent `core_cov_filtered_pct`, which was
read instead, is empty for every row in that QC table. **There are consequently
no active register exclusions in the analysed panel**, and the four are panel
members that fall in no analysis unit (2.12.5).

## 2.12.2 Assembly and assembler selection

Short-read isolates were assembled with SPAdes (TheiaProk `digger_denovo`,
`assembler=spades`; **the pipeline default of SKESA was overridden explicitly**).
Three isolates retained their SKESA assembly because SPAdes failed on them, each
for a documented reason: for `SRR28096032` and `SRR28096062` the library insert
(145 bp) was shorter than the read length (151 bp), so read pairs overlapped
fully and read through into adapter, and `--only-assembler` bypassed BayesHammer
error correction — SPAdes collapsed to 4.3 Mb against SKESA's 6.96 Mb. For
`SRR30648682` SPAdes assembled 11.88 Mb, revealing foreign content that SKESA had
suppressed. Two further isolates (`SRR28096039`, `SRR28096043`) were Oxford
Nanopore assemblies with no short-read counterpart.

## 2.12.3 Assembly QC, and a gate that had to be recalibrated

Assemblies were gated on **core-genome coverage and gene-count ratio** rather
than on length or contiguity.

**The gene-count-ratio threshold (≤ 1.20) was calibrated on PacBio CLR failures
at ≥ 1.35 and has no discriminating power on near-complete assemblies**, where
contiguity cannot mask residual indel error. The two ONT assemblies were
therefore re-screened with BUSCO v5.8.2 (`burkholderiales_odb10`, n = 688)
against contiguity-matched complete genomes. Three complete two-contig genomes
(`K96243`, `GCF_000763555.1`, `GCF_030297255.1`) each returned **688 complete, 0
fragmented, 0 missing**. `SRR28096043` (2 contigs) returned **654/22/12** and
`SRR28096039` (2 contigs) returned **623/44/21** — the latter worse than a
1,388-contig SKESA draft. Because contiguity cannot explain a fragmented BUSCO in
a two-contig assembly, the deficit is attributed to frameshifts from residual
indels. Prodigal gene calls agreed: `SRR28096039` predicted 6,474 CDS at a mean
length of 308 aa with 11.8% under 100 aa, against 5,765–5,967 CDS at 343 aa and
8.0–8.6% for the complete genomes.

**Tree geometry independently confirmed this.** Both ONT isolates fell in
`strain_27_L1_1`, a unit of 10 isolates from one Ghanaian batch (8 Illumina, 2
ONT) — a near-controlled contrast, since provenance, batch and reference are
shared and only the platform differs. Terminal branch lengths:

| tip | replicon 1 | replicon 2 |
|---|---|---|
| `SRR28096039` (ONT) | 0.11838 | 0.15568 |
| `SRR28096043` (ONT) | 0.05415 | 0.08450 |
| longest Illumina tip | 0.00142 | 0.00144 |
| Illumina median | 0.00056 | 0.00077 |

`SRR28096043`'s terminal branch is **38–59× the longest Illumina tip in its own
unit**; every Illumina member falls within 0.4–2.5× the unit median. **Both ONT
isolates were therefore excluded from analysis.** The discriminating signal was
their **rank within their batch** (the top 2 of 171; batch median 0.97, p90 0.99),
not their absolute ratio.

> **Recommended gate going forward:** for assemblies at ≤ 5 contigs, screen on
> BUSCO fragmented + missing against a complete-genome baseline of zero, and
> treat gene-count ratio as a within-batch outlier test rather than an absolute
> threshold.

## 2.12.4 Partition: PopPUNK strains, fastbaps sub-clusters, analysed at level 1

The analysis unit is a **fastbaps level-1 sub-cluster within a PopPUNK strain**,
retained at **n ≥ 7**. The rule was applied uniformly: no lineage was subdivided
because it was large, and none was left whole because it was small.

**Strains.** PopPUNK v2.7.6. A sketch database was built over all **2,976**
assemblies as sequenced (k = 15–31, step 2) — the partition was derived before
BioSample deduplication, so the sketch covers the pre-deduplication set — and
fitted with a Gaussian mixture (`bgmm`, K = 5) followed by boundary refinement,
yielding **310 clusters of which the largest held 901 genomes**.

**Sub-clusters.** Within each strain, PopPIPE built a split-k-mer alignment
(SKA v0.4.0), a neighbour-joining guide tree and a fastbaps hierarchical
partition (`levels = 3`), analysed at **level 1**. Levels 2 and 3 were computed
but not used, so unit size was determined by one stated rule rather than chosen
per lineage.

**Result before refinement: 86 units, 2,352 genomes**, largest n = 159,
median n = 18. That is **79.0%** of the 2,976 assemblies the partition was
derived over, or **79.5%** of the 2,959-genome deduplicated panel; quote whichever
denominator is in use and say which.

> **PopPUNK `bgmm` at fixed K is deterministic per input and exposes no seed**, so
> cluster boundaries are a property of the panel, not of the run. It follows that
> **strain labels are not comparable between fits on different panels.** This is
> not a technicality: the strain numbered 4 in the previous panel and the strain
> numbered 4 here share **zero** members, and all 261 genomes of the former fall
> inside strain 1 here. Comparisons across fits must be made by membership, never
> by label.

## 2.12.5 Unit refinement, and the gate order that governs it

Gubbins infers recombination against a clonal background, so a unit fusing two
well-separated clonal groups can misattribute the divergence between them. Units
were therefore screened for internal population structure before analysis, using
the pairwise core distances already present in the PopPUNK database (all
C(2976,2) = 4,426,800 pairs).

Overall diversity was **not** diagnostic: units drawn from more than one
prior-partition unit were ~4× more internally diverse (median-of-medians 0.00221
vs 0.00054), but the most diverse single-provenance unit (max 0.00538) exceeded
every one of them. **Modality was diagnostic.** `strain_1_L1_26` (n = 154, median
pairwise distance 0.00060 — among the tightest units in the panel) held three
clonal groups at 0.00007 internal against 0.00088 and 0.00134 separation, and
this screen proposed splitting it into 98, 47 and 8; the screen also proposed
removing divergent members from `strain_1_L1_11` (24 → 18) and `strain_1_L1_22`
(34 → 32). Units that were diverse but unimodal were left intact.

### The refinement was applied in the control run, not the reported one

**This is the single point at which the two runs differ, and it must not be read
past.** The refinement above was executed in the A100 run, giving **88 units,
2,342 genomes, 176 replicon-units**. **The reported partition is the
workstation run, which is unrefined**: `strain_1_L1_26` is retained whole,
`strain_1_L1_11` and `strain_1_L1_22` keep their divergent members, and the
largest unit is `strain_2_L1_6` (n = 159) rather than a child of
`strain_1_L1_26`.

The reported partition was then **corrected**, which the A100 partition was not
and could not be without re-deriving it:

| step | units | genomes |
|---|---|---|
| after the n ≥ 7 rule | 86 | 2,352 |
| − `strain_1_L1_10`: 3 of its 7 members are duplicate BioSamples, leaving 4, below the floor, so the whole unit is dropped | **85** | 2,345 |
| − 4 further duplicate BioSamples in other units | 85 | 2,341 |
| − `SRR2896257`, then a register exclusion | **85** | **2,340** |

**Reported partition: 85 units, 2,340 genomes, 170 replicon-units**
(`FINAL_BASIS_2026-08-22/FINAL_PARTITION.tsv`), unit size min 7, median 18,
max 159, drawn from 28 distinct PopPUNK strains.

⚠ **One genome is a known, deliberate inconsistency, and it is disclosed rather
than repaired.** `SRR2896257` was removed from `strain_1_L1_26` (154 → 153)
under a register exclusion that was **subsequently retired as unevidenced**
(2.12.1). It was not re-added: doing so would require re-deriving that unit's
alignment, recombination inference and r/m, changing a frozen analysis basis for
a single genome. It is retained as a panel member assigned to no unit. **The
reported `strain_1_L1_26` is therefore n = 153 where the current registers would
support 154.**

Why the unrefined partition is the reported one, in order of weight:

1. **It is the only one that is corrected.** Both runs carry the same duplicate
   BioSamples; only this one has had them removed.
2. **Every alignment is local.** The A100's two refinement children of
   `strain_1_L1_26` have no core alignment in this workspace, so their r/m cannot
   be re-derived here.
3. **The refinement buys nothing measurable.** Its n = 98 child is a clonal
   expansion at 72 mean pairwise SNPs — an order of magnitude below the Gate 1
   floor — and refinement did not increase the in-window set (2.12.10).

### The gate order is load-bearing, and refinement must be read through it

Section 2.6 establishes that **the diversity gate is applied first and the
modality gate second** (2.6.2), and that **below n = 25 modality is undecidable**.
Refinement in this run was designed from the modality evidence before the
diversity gate had been applied to the resulting units. Applying Gate 1
retrospectively (2.6.1; usable window ≈ 1,270–4,671 mean pairwise core SNPs,
computed with `cluster_diversity_bp.py` over the Mash matrix) gives:

| | n | ~mean pairwise core SNPs | Gate 1 |
|---|---|---|---|
| **before** `strain_1_L1_26` | 154 | 3,421 | **in-window** |
| after `strain_1_L1_26` | 98 | **955** | below floor |
| after `strain_1_L1_36` | 47 | 3,374 | **in-window** |
| after `strain_1_L1_37` | 8 | **229** | below floor (and n < 25) |

The split therefore converted one measurable unit into one measurable unit plus
two clonal expansions that lie **below the floor at which Gubbins can detect
recombination at all**. This is the outcome 2.6.2 anticipates for a tight core
("`gap/mean` high indicates a tight core plus a few outliers and subdivision is
futile"), and it matches the precedent already recorded there: a 150-genome unit
splitting into "a usable 45-genome in-range unit plus a 95-genome clonal
expansion … unusable for recombination inference, but of independent interest as
a probable outbreak or heavily-sampled sublineage."

**The split is reported on that basis.** `strain_1_L1_36` (n = 47) is the
recombination result arising from it. `strain_1_L1_26` (n = 98) and
`strain_1_L1_37` (n = 8) are reported as **identified clonal expansions of
epidemiological interest, with no r/m** (2.12.7).

## 2.12.6 Per-unit mapping reference

Per-unit references were chosen by a completeness gate (≤ 2 contigs) and
centrality ranking within the unit, with empirically poor references blocklisted;
units containing no complete genome borrow the nearest one from outside. **34
distinct references** served the 85 reported units
(`curated_L1v4c_refs.tsv`, restricted to `FINAL_PARTITION.tsv`).

**Reference deflines were normalised before analysis.** Gubbins passes
`<unit>__<replicon>.core.full.iteration_N_reconstruction` to RAxML as its `-n`
run id, and RAxML v8 **segfaults at a run id of ≥ 128 characters**. In the run
where this was diagnosed, **42 of 172 replicon-units (24.4%) would have exceeded
the limit** (longest 161 characters); after normalisation the longest was **70**.
⚠ *That count is from the control run's replicon set and has not been recomputed
on the 170 reported replicon-units; the failure mode and the fix are independent
of which partition is used, but recompute the count before quoting it.* Sequence
content was verified byte-identical — only `>` lines were rewritten. This failure
mode is silent in the sense that matters: Gubbins reports it as "Unable to fit
model to data", which is indistinguishable from a genuinely bad reference.

## 2.12.7 Alignment, replicon splitting, recombination and r/m

Within each unit, reference-based variant calling was performed with Snippy
against the unit reference, with **replicons split** (`--split_replicons`) and
replicons below **100 kb** discarded, so that no alignment spans a contig
junction. Recombination was removed per unit with Gubbins at **5 iterations,
minimum 3 SNPs per recombination block, hybrid tree builder disabled, starting
tree skipped**; maximum unit size was capped at 1,000.

> These parameters are **pinned rather than left at defaults** because Gubbins
> settings shift r/m by **0.47–0.78× non-uniformly, with no correction factor**;
> estimates from different settings cannot be pooled. The repository defaults
> (3 iterations, minimum 2 SNPs, hybrid enabled) would not be comparable with the
> calibration in 2.6 or with the control run.

r/m is **pooled, not averaged**: Σ(SNPs inside recombinations) / Σ(SNPs outside),
summed over branches and over both replicons of a unit. Per-branch ratios are
undefined where a branch carries no SNPs outside recombination and are wildly
noisy on short branches, so averaging lets the least informative branches
dominate. Both replicons are pooled because they share one genealogy; their
agreement is a consistency check, never evidence of validity.

**The external reference's branches are excluded** before pooling, as in previous
drafts: the reference sits outside the population by construction, so its branch
carries population-to-outgroup divergence that Gubbins scores outside
recombination and which would otherwise enter r/m's denominator. Where the
reference is a true outgroup its divergence is split between the `Reference` leaf
and the sibling clade at the root, so **both children of the root are dropped**
whenever one is the reference; where the reference nests inside the population,
nothing is removed. The per-unit record of which branches were dropped is in
`Summaries/recombination_rm.tsv`.

### r/m is reported only for units inside the diversity window

This is the single most important qualification on the recombination results.
Section 2.6.1 establishes that outside the diversity window r/m is **not a
measurement**: below the floor Gubbins cannot detect recombination, and above the
ceiling the estimate collapses (0.16–1.73 in calibration). Classifying the 85
units of the reported partition on **alignment-derived distances** against the
window as relocated into those units (**[700, 4,700]**, 2.6.1) reproduces the
calibration:

| Gate 1 class | units | median r/m |
|---|---|---|
| **in-window** | **47** | **7.70** |
| below floor | 12 | 1.32 |
| above ceiling | 26 | 2.14 |

Membership was previously taken from a Mash-to-SNP proxy in a different unit
system from the calibration; that proxy overstates diversity by a median
**1.30×**, by up to **17.20×**, and **reclassifies 22 of these 85 units**. It
gave 47 units and a median of **7.26** — close in aggregate, but with a
below-floor group whose composition did not hold up. The alignment-derived
classification is the one reported.

⚠ **Three r/m values are in circulation and only one is this analysis.** **7.70**
is the reported figure (alignment-derived Gate 1, 85 units). **7.26** is the same
partition scored through the Mash proxy. **7.38** is the A100 88-unit control.
They differ by basis and by proxy, not by biology; none is a correction of
another.

**The reported recombination result for this collection is therefore
r/m = 7.70 (median of 47 in-window units).** The all-unit median (5.51) mixes
measurements with detection failures and is not reported. A **low r/m is a
detection failure, not a clean unit** — a reading error that is easy to make in
both directions, since the collapse is symmetric.

Out-of-window units remain in the analysis for phylogeny and phylogeography,
where diversity outside the Gubbins window is not disqualifying; only their r/m
is withheld.

## 2.12.8 Phylogenies

**Per unit.** After recombination removal, a maximum-likelihood tree from the
filtered polymorphic sites: IQ-TREE under **`GTR+ASC`**, one tree per
replicon-unit (**170** on the reported partition). Gubbins' own node-labelled
trees are retained alongside as a second estimator.

> ⚠ **Two corrections to what this section previously claimed, both verified
> against the pipeline configuration (`conf/params.config`) rather than against
> prose.**
>
> **1. Production used `+ASC`, not `-fconst`.** `iqtree_model` and
> `iqtree_asc_model` are both `GTR+ASC` and **`iqtree_fconst = null`**. Where the
> filtered alignment contains constant columns — which makes `+ASC` abort —
> `iqtree_asc_fallback = "varsites"` strips those columns and **keeps `+ASC`**;
> the config notes that `+ASC` and `-fconst` are mutually exclusive and that the
> two alternative fallbacks alter branch lengths.
>
> **This contradicts §2.5**, which argues `-fconst` with true counts is
> preferable here because it reproduces full-alignment base composition exactly
> whereas `+ASC` collapses composition toward 25/25/25/25 in a 68% GC genome.
> **The contradiction is real and is not resolved by this draft.** The
> calibration track used `-fconst`; the production run used `+ASC`. Quantifying
> the difference on one unit is an open method question and must be done before
> submission — either the production choice is defended or the trees are
> recomputed. Do not describe the two as equivalent.
>
> **2. Branch support was NOT enabled in the production run.**
> `iqtree_support = false`, which the config itself flags as altering scientific
> output (no UFBoot or SH-aLRT values on the tree). Support values were added
> **post-hoc** by `add_branch_support_bp.sh`, which re-runs IQ-TREE on the
> published alignments adding `-bb 1000 -alrt 1000`
> (`L1_TREES_SUPPORTED/`, `SUPPORT_TREES.log`, 2026-08-15). ⚠ That run covered
> **164 replicon-units** and predates the current partition, so it does not
> correspond one-to-one with the 170 reported here. **Re-run it on the reported
> partition, or state plainly which trees carry support and which do not.**
> The earlier claim that all trees were "at the highest confidence tier" is not
> supported and has been removed.

**Across units.** One **medoid per unit** — the member minimising mean SNP
distance to the rest of its unit, computed on the recombination-filtered
alignment and excluding the reference taxon — then a parsnp core-genome alignment
over those **85** medoids and IQ-TREE under `GTR+ASC`. Tips are unit identifiers.

**This global tree is not recombination-corrected, and must not be.** Gubbins
identifies recombination as regions of unusually dense SNPs against a clonal
background; across **85** divergent lineages no shared clonal background exists, so
it would call most of the alignment recombinant — precisely the failure the
partition exists to prevent. The global tree shows how units relate, its branch
lengths include recombination, and **no r/m may be derived from it**.

**The grafted global tree must not be dated.** Per-unit trees grafted onto the
parsnp backbone mix branch-length units between the backbone and the grafts; the
result is a topology aid, not a time-calibrated or rate-comparable object.

## 2.12.9 Phylogeny–geography association

Per unit, the **Fitch small-parsimony score** of country labels on the
recombination-corrected topology, compared with a null from **1,000 permutations
of the labels across tips of the same tree**. Permuting holds both topology and
country composition fixed, so a unit that is 90% Thai is compared against other
90%-Thai arrangements — necessary because the marginal country distribution is
extremely uneven. Tips with unknown country are treated as fully ambiguous, so
missing metadata weakens signal rather than inventing it.

**BioProject was tested identically and is reported alongside**, because a
BioProject is typically one study, one laboratory and one country, and a
geographic signal no stronger than the BioProject signal is not evidence of
phylogeography. Units in which every genome shares one country yield a parsimony
score of zero that no permutation can better; these carry no information and are
reported as uninformative, with no p-value, rather than counted as significant.

Missing metadata is encoded inconsistently in the source table — `country` uses
an empty cell, but `bioproject` uses the literal string "unknown" for 274 of the
**2,340** analysed genomes — so both fields are normalised to a missing state before
scoring. Left unnormalised, those 274 genomes would be scored as one shared
274-member study, mis-measuring the confounder in the direction that favours a
geographic result. A genome whose origin resolves to more than one country
(one record, "Panama and Peru") is likewise treated as missing at country scale,
keyed on its `multi_country` resolution rather than on string-matching, since
"Trinidad and Tobago" is a single country.

**Multiple testing and the control gate are applied in code**, not by hand:
Benjamini–Hochberg FDR at 5% across the testable country tests of a single scale,
and a BioProject control counted as informative only where it covers ≥70% of the
unit's tips across ≥3 distinct projects. Each unit receives one of five
interpretations — *untestable (single-valued)*, *null*, *vacuous control*,
*confounded*, or *geographic (control passes)*. At national scale: 39, 25, 5, 13
and 6 units respectively.

**A draw-probability test was considered and deliberately not implemented.** An
earlier draft proposed testing near-homogeneous units — for example the
22-genome Mississippi unit, 21 of one country — against the hypergeometric
probability of drawing that composition at random from the collection. We reject
it. Its null is that the unit is a random draw from the collection, but units are
clades, and clades are geographically concentrated by descent, so rejecting that
null demonstrates only that the partitioner works. In the analysed set **54 of 85
units are ≥90% single-country and 37 are 100%**, so the test fires on almost all of
them, at a magnitude set by how rare the country happens to be in the collection
rather than by any property of the unit. The decisive comparison is internal:
`strain_3_L1_8` (n=22, top share 0.955, 21 Thailand) and `strain_4_L1_1` (n=22,
top share 0.955, 21 USA) are identical in every tested quantity and both return
p = 1.0000 under the permutation test — correctly, since each is a clade plus one
stray. A hypergeometric would separate them by many orders of magnitude solely
because Thailand is **66.8% of the analysed set** and the USA ~2%. ⚠ *Quote that
denominator explicitly: Thailand is 66.8% of the 2,340 analysed genomes but
**59.5% of the 2,959-genome panel**. Both figures are correct and they are not
interchangeable.* Such units are reported as
**descriptive composition, without a p-value**.

## 2.12.10 The control run, and what it establishes

The 86-unit partition (2.12.4, before refinement) was run to completion
independently on a 22-core workstation: 8,178 tasks, **zero failures**, 172/172
replicon-units completed at the highest confidence tier. This is not a duplicate;
it is the control that makes the effect of refinement measurable.

**Comparability.** 82 units have identical membership in both runs. Across those,
r/m agrees to a **median absolute difference of 0.0145 (0.38% relative)**,
maximum 1.32. Two runs on different hardware, under different resource
configurations, agreeing to ~0.4% on the median unit — this is the empirical
basis for treating the two partitions as comparable, rather than assuming it from
the configuration.

**Effect of refinement.** The pre-split `strain_1_L1_26` measured r/m 3.10 and was
**in-window**; its three children measured 1.07, 6.68 and 2.63.

**The n=98 child is a clonal expansion, and the gate is right to exclude it.**
Computed directly from its own `core.tab` sites over its 98 members, its mean
pairwise distance is **72 SNPs** (median 72, max 235) and Gate 2 scores it
**continuous** (gap/mean 0.014, 8/20 empty bins). Ninety-eight genomes within 235
SNPs of one another, unimodally distributed, is a recent clonal expansion; at 72
SNPs it sits an order of magnitude below the Gate 1 floor, which is precisely
where r/m is not a measurement. Its r/m of 1.07 is a detection floor, not a
biological estimate. `strain_1_L1_36` by contrast has mean pairwise distance
1,126 and is in-window with r/m 6.68.

**So refinement did not increase the measurable set**, as stated below: the
unsplit parent was one in-window unit and the split yields one in-window child.

Two bookkeeping corrections apply to the counts, neither affecting that reading.
Under the alignment-derived Gate 1 the in-window count is **48 in the production
run and 47 in the control**, not 47 in both — but the additional unit is
`strain_1_L1_11`, reclassified from above-ceiling, not a refinement child.
And **`DISTANCES_v4c_SUMMARY.tsv` must not be joined to the production
partition by unit name**: three of its rows (`strain_1_L1_11`,
`strain_1_L1_22`, `strain_1_L1_26`) carry the *control* run's membership while
the rest match production, so it reports the unsplit parent's diversity (1,310)
against the production run's n=98 child (72). Diversity for those three must be
recomputed on production membership, as it was here. The in-window median is
unaffected either way — **7.44** — because the two units this misplaces both sit
below it.

The comparability argument above is unaffected, and is if anything strengthened:
the two runs' in-window medians are **7.44 and 7.70**, agreeing to 3.5%.
Refinement therefore did not increase the measurable set; its contribution is
that it separates a genuine clonal expansion from the in-window population that
surrounds it, and surfaces heterogeneity (1.07 to 6.68) that the combined unit
averaged away.

**Two-genome trims are not neutral.** `strain_1_L1_22` moved from r/m 4.12 (n=34)
to 7.21 (n=32) on the removal of two isolates — the unit sits at ~4,762 mean
pairwise SNPs, immediately above the Gate 1 ceiling, where the estimate is
unstable. Trims of this size near the window boundary should be reported with
that caveat or not performed.

## 2.12.11 Metadata

Country, sub-region, BioProject and collection date were joined from a curated
table. The join is attempted against `sample_id`, `FASTA_name` and
`Assembly Accession` in that order — a naive exact join on `sample_id` alone
matches 73% and accession prefix alone 86%, whereas all three together reach
99.9%. Genomes without metadata are retained with empty fields rather than
dropped, so that per-unit denominators remain correct.

**Country strings require care.** The country column conflates US territories
with the mainland: of 21 genomes labelled "USA", 10 are Puerto Rico or the US
Virgin Islands, leaving 11 from the mainland. Analyses of US origin must
disaggregate these.

## 2.12.11a Origin attribution, scored against known exposures

**Rewritten 2026-08-23.** The previous version of this section described an
earlier analysis — 26 genomes, unit-modal labels over recombination-filtered SNP
distances — that has been superseded twice. It is retained in the project archive
as `[SNP/24]`, where it serves as an independent-typing-system cross-check on a
different validation set. The analysis below is the reported one.

### 2.12.11a.1 Typing scheme

Attribution is scored on **core-genome MLST**, not on the SNP units, so that the
result does not depend on the partition. The scheme is **Lichtenegger *et al.*,
4,221 core targets** (Lichtenegger S, Trinh TT, Assig K, *et al.* *J Clin
Microbiol* 2021;59(8):e0009321; PMID 33980649; doi:10.1128/JCM.00093-21), built by
challenging K96243 with 469 genomes and validated on 320 WGS datasets. Alleles
were called with chewBBACA (`PrepExternalSchema` then `AlleleCall`) over
**3,033** genomes; median call rate **96.9%** of 4,221 loci, with **99.2%** of
genomes above 90%.

Distance between two genomes is the **fraction of commonly-called loci at which
their alleles differ**, computed pairwise on the loci called in both; loci
missing in either genome are excluded from that pair rather than imputed. This
makes the denominator pair-specific, and it is reported alongside every
attribution call (`n_loci_compared`, median 4,039 of 4,221, range 2,520–4,083).

> A second scheme (PubMLST scheme 2, 4,089 loci) was run in full as a
> scheme-swap robustness check and is reported in the supplement. The two agree:
> region accuracy was identical and cgMLST-vs-SNP concordance correlated at
> r = 0.999 between schemes. **The scheme is not what determines the result.**

### 2.12.11a.2 Validation set

**48 genomes carry an independently documented exposure country** rather than
merely a country of deposit — CDC submissions with an explicit `ex <country>`
label, older assemblies whose exposure country is recorded in the assembly name,
and cases whose exposure is documented in the published literature. The register
of exposure assignments is `EXPOSURE_OVERRIDES.tsv`; it is a **frozen input**,
changed only by a deliberate batched refresh, never edited mid-analysis.

**Two of the 48 carry a non-country exposure** ("Africa"; "Panama and Peru") and
are unattributable at country scale by construction. **The scorable set is
therefore 46**, drawn from **16 exposure countries**. Every `x/46` in this paper
is over that set. ⚠ **48 is not an attribution denominator.**

### 2.12.11a.3 Estimators, and why the choice is reported per scale

Four estimators were computed for every held-out genome against the same pool:

| estimator | rule |
|---|---|
| **nearest neighbour** | the label of the single closest genome |
| **modal k = 20** | the commonest label among the 20 closest |
| group test | the group whose *median* distance to the target is lowest |
| hybrid | modal k=20 when a relative closer than 0.30 exists, else the group test |

**The best estimator differs by scale, and both are reported with the estimator
named.** Country is best under **nearest neighbour**; region is best under
**modal k = 20**:

| scale | estimator | correct | accuracy | majority baseline | **κ** |
|---|---|---|---|---|---|
| country | **nearest neighbour** | 10/46 | 21.7% | **26.1%** | **0.193** |
| country | modal k = 20 | 7/46 | 15.2% | 26.1% | 0.132 |
| region (7-way) | nearest neighbour | 37/46 | 80.4% | 45.7% | 0.715 |
| region (7-way) | **modal k = 20** | **41/46** | **89.1%** | **45.7%** | **0.832** |

⚠ **A nearest-neighbour number and a modal number are different analyses and must
never be compared with each other.** Region under nearest neighbour is 37/46
(80%); that is not a correction to 89% and must not be reported as one. The
per-estimator results are written to `GROUPING_LADDER.tsv` and surfaced with the
estimator in the key (`attribution.region.modal_k20`,
`attribution.country.nearest_neighbour`).

**Cohen's κ is the headline statistic, not accuracy.** Accuracy is not comparable
across groupings: a binary split with a 90% majority class scores 90% by saying
nothing, and East Asia & Pacific is 66.8% of the analysed set. κ corrects for
chance agreement and therefore also neutralises the Thailand over-representation.

**Country attribution does not exceed chance.** 21.7% against a 26.1% majority
baseline. It is reported as a failure to clear baseline, not as "22% accuracy".

### 2.12.11a.4 Holdout: leave-group-out AND leave-outbreak-out

Two holdout rules are applied together.

**Leave-group-out.** Every *other validation genome sharing the target's exposure
country* is removed from the pool. Without it, validation genomes predict one
another and country accuracy is inflated by circularity rather than by signal:
under leave-*one*-out the same estimator reaches 37% at country scale and **all
of those hits are validation genomes of the same country predicting each other**.
The collapse under leave-group-out is reported as a result in its own right,
because it quantifies how much apparent attribution performance is circular.

**Leave-outbreak-out.** Isolates that are the *same epidemiological source* —
one investigation, one strain, one place — are not independent observations of
geography and are held out together whenever any member is scored. The register
is `OUTBREAK_GROUPS.tsv`, also a frozen input.

> **This register is explicit, not automatic, and the reason is a measured
> counterexample that has since been externally confirmed.** An automatic
> same-BioProject or near-clone rule would hold out the Georgia, USA cases that
> sit ~0.01 from two Viet Nam-exposure cases in the same BioProject, "correcting"
> Viet Nam from 0/2 to 2/2. Those Georgia cases are **not** co-deposits: a CDC
> and state epidemiologic investigation found no recent international travel and
> reported them as presumptive autochthonous cases spanning 1983–2024 (Brennan S,
> *et al.* *Emerg Infect Dis* 2025;31(9):1802–1806; PMID 40835221). They are
> independent cases of a lineage that genuinely spans Viet Nam and the
> southeastern United States, and removing them would hide real references and
> manufacture an answer. **An automatic rule would have produced a false positive
> here; only an explicit register avoids it.**

### 2.12.11a.5 Stratification by nearest-neighbour distance

Every accuracy is reported stratified by the distance to the closest available
relative, because the two regimes are different problems:

| stratum | country (NN) | region (modal k = 20) |
|---|---|---|
| d < 0.05 — a close relative exists | **2/14** | **14/14** |
| 0.05 ≤ d < 0.30 | 2/10 | 8/10 |
| d ≥ 0.30 — no real relative | 6/22 | 19/22 |

⚠ **A stratification must use the same estimator as the headline it accompanies.**
The region strata above are modal k=20 because 89% is a modal number; the
nearest-neighbour region strata (11/14 · 6/10 · 20/22) belong with the 80% figure.

**The d ≥ 0.30 row is not the success it appears to be.** At that distance ~30–79%
of loci differ and there is no relative in any meaningful sense. Nine of those 22
genomes share a single Ecuadorian nearest neighbour; because most are Latin
American, "Ecuador → Latin America & Caribbean" scores correct, while **both
Sub-Saharan African genomes in the stratum are confidently assigned to Latin
America and scored wrong**. The estimator is reporting *"unlike the Asian
majority of the panel"*, and a catch-all region label converts that into a
correct answer for one continent and a wrong one for another.

**A control for the obvious alternative explanation.** Genomes with fewer
commonly-called loci could have inflated distances, which would make the far
stratum an assembly-quality artefact. It is not: across the 46, `n_loci_compared`
against nearest-neighbour distance gives Spearman ρ = **−0.247** (n = 46, not
significant), and median loci compared is flat across the three strata
(**4,042 / 4,040 / 4,024**).

### 2.12.11a.6 The abstention rule

Because the d ≥ 0.30 stratum answers confidently without evidence, the estimator
is paired with an **abstention rule**: where no relative closer than a threshold
exists, return *"unattributable — novel lineage"* rather than a region.

The threshold is **nearest-neighbour distance ≤ 0.462**, and it is reported
**out-of-sample**: the threshold is selected on the other 45 genomes and applied
to the held-out one, so the figure is not the circular result of tuning and
scoring on the same set.

| | in-sample | leave-one-out |
|---|---|---|
| coverage | 78.3% (36/46) | **76.1%** |
| selective accuracy | 94.4% | **94.3%** |

**Both baselines are required and they disagree**, which is the point. Declining
cases *at random* leaves the expected error rate unchanged, so the
random-abstention baseline is simply the answer-everything accuracy (89.1%). But
abstention also changes the class mix, so the **majority share of the retained
subset** must be reported too: it rises from 45.7% to 50.0%. The rule therefore
improves lift over chance only from +43.4 to +44.4 points. **Its value is in
*which* errors remain, not in the accuracy number**, and the paper states it that
way.

The rule declines **3 of the 5 region errors**, including **both** Sub-Saharan
African misassignments, at a cost of 7 correct answers. It **cannot** decline the
two Georgia/Mississippi-type errors, which have genuine close relatives and high
neighbourhood agreement — **two distinct failure modes, and this rule addresses
one of them.**

⚠ **The same rule fails at country scale, and that is reported as a result.** Its
best operating point reaches 37.5% selective accuracy against an answer-everything
21.7% — an apparent +15.8 points, reproduced exactly under leave-one-out. But the
**retained-subset majority baseline is also exactly 37.5%**: on the half of cases
the rule elects to answer, always guessing the commonest exposure country scores
identically. **Country attribution is not rescued by abstaining.**

### 2.12.11a.7 Scales not claimed

**Sub-national attribution fails and is reported as failing**: 0 of 5 scorable
genomes, under every estimator.

**The granularity ladder shows where the ceiling lies.** The same data, the same
holdout, coarser groupings (modal k = 20):

| grouping | classes | accuracy | baseline | **κ** |
|---|---|---|---|---|
| Asia vs non-Asia | 2 | **100%** | 58.7% | **1.000** |
| Eastern vs Western hemisphere | 2 | 95.7% | 63.0% | **0.909** |
| region, 7-way | 5 present | 89.1% | 45.7% | **0.832** |
| SEA vs non-SEA | 2 | 76.1% | 58.7% | 0.461 |
| country | 16 | 21.7% | 26.1% | **0.193** (NN) |

**We therefore claim regional attribution and an essentially perfect deep split,
and we do not claim country-level attribution.** The limit is depth of signal,
not volume of data: the deep splits are recovered without error while the
shallow ones are not, on the same genomes and the same pool.

### 2.12.11a.8 Software

Attribution is scored by `score_cgmlst_lichtenegger.py` (per-genome calls) and
`grouping_test_bp.py` (the estimator × grouping ladder and κ), the abstention
rule by `abstention_rule_bp.py`. The two scorers construct their candidate pools
independently and are cross-checked against each other for agreement on the
nearest-neighbour calls and on the scorable denominator, as part of the frozen
basis validator (2.12.12).

## 2.12.12 Reproducibility

Analysis-unit membership and per-unit references are provided as
`curated_L1v4c_clusters.final.tsv` and `curated_L1v4c_refs.final.tsv`. The
workflow was driven in **curated mode**, in which the partition and references
are taken as given and no in-workflow clustering is performed; Mash clustering,
medoid selection and tree grafting are skipped on this path.

A clean exit does **not** establish that every unit succeeded: the workflow uses
`errorStrategy 'ignore'`, so units can fail and the run still exit zero.
Verification is therefore per-unit, comparing units **requested** against units
that actually produced Gubbins output, and reading `gubbins_status`,
`gubbins_exit_code`, `iqtree_status` and `confidence_tier` from
`Summaries/cluster_phylogeny_summary.csv`. Both runs reported here were verified
this way: **176/176 and 172/172 replicon-units complete, exit 0, highest
confidence tier, zero task failures in either execution trace.**

## 2.12.13 Software and compute

| tool | version | role |
|---|---|---|
| Nextflow | 25.10.0 (production) / 25.04.6 (control) | workflow |
| PopPUNK | 2.7.6 | strain assignment |
| SKA | 0.4.0 | split-k-mer alignment within strains |
| fastbaps (PopPIPE) | levels = 3 | within-strain sub-clustering |
| Mash | **sketch size 50,000**, k = 21 | distances for reference choice and medoids |
| Snippy | 4.6.0 | reference-based variant calling |
| Gubbins | 3.4.3 | recombination detection |
| RAxML | 8.2.12 (in Gubbins) | tree builder inside Gubbins |
| IQ-TREE | 2.2.6 | per-unit and global ML trees |
| parsnp | 1.7.4 | core-genome alignment for the global tree |
| BUSCO | 5.8.2 (`burkholderiales_odb10`) | assembly base-accuracy screening |

The Mash sketch size is **50,000**, not the 10,000 named in the repository's
`params.config`; the sketch header is authoritative.

**Compute.** ⚠ **Note the designation, which was inverted in an earlier draft.**
The **reported** run is the 22-core, 62 GB workstation (85 units, 2,340 genomes);
the NVIDIA DGX Station A100 (128 cores, 503 GB RAM) executed the **control** run
(88 units), per the §2.12 preamble. **No stage is
GPU-accelerated** — Gubbins, Snippy, IQ-TREE and RAxML are all CPU-bound. The
hardware requirement is memory, and it falls on partitioning rather than on the
SNP analysis: `ska build` on the 901-genome strain requires ~500–600 GB when
built monolithically, which exceeds the workstation. It was executed instead in
**8 batches of 113 (peak 12.8–14.2 GB each) followed by `ska merge`**;
equivalence was verified rather than assumed — on a 60-genome subset, monolithic
and batched builds produced the same taxa and identical alignment column
multisets, differing only in column order, which `ska align` does not define and
fastbaps' site-independent model does not use.

Container digests, the exact command line and per-task resource usage are in each
run's `pipeline_info/`, archived with the results.
