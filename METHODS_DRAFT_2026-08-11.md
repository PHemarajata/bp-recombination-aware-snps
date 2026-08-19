# Methods (draft, updated 2026-08-16)

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

Units were required to fall in **≈1,270–4,671 mean pairwise core SNPs
(`ska distance` units)**.

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
Union coverage was checked and found **not** to scale with unit size
(r = 0.142 against n) or with branch count (r = −0.059), so a single cutoff is
applicable across the 20-fold size range spanned by the units. Note that union
has little dynamic range at the top of its scale and becomes uninformative
there.

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
derive. It was executed as a Nextflow workflow
(`github.com/PHemarajata/wf-assembly-snps-mod`, branch `reference-blocklist`,
commit `f1a7d13`) in **curated mode**, meaning the partition and the per-unit
mapping references were supplied rather than re-derived inside the run. Where this
section conflicts with 2.1–2.11, this section is what was done.

## 2.12.1 Partition: PopPUNK strains, fastbaps sub-clusters, analysed at level 1

The analysis unit is a **fastbaps level-1 sub-cluster within a PopPUNK strain**.
The rule was applied uniformly: no lineage was subdivided because it was large,
and none was left whole because it was small.

**Strains.** PopPUNK v2.7.6 (bgmm fit followed by boundary refinement; Seng et al.
2024 in-organism parameters, PMID 38972886) over all 2,802 assemblies. The refined
fit returned **264 clusters, of which 35 contained ≥ 7 genomes, covering 2,395
genomes**; 152 were singletons. The refine pass is not optional: bgmm alone gave a
1,723-genome cluster, which is not an analysis unit by any definition.

**Sub-clusters.** fastbaps (via PopPIPE, `levels = 3`) within each strain,
analysed at **level 1**. Levels 2 and 3 were computed but not used, so that unit
size was determined by one stated rule rather than chosen per lineage.

**Size floor.** Units with **n < 7** were excluded. Below that there are too few
informative sites for Gubbins to distinguish recombination from mutation. Seven
matches the smallest unit in the earlier manual analysis, keeping the two
comparable.

**Result: 82 units, 2,070 genomes — 73.9% of the 2,802-genome collection**
(largest unit n = 155, median n = 18). For comparison the earlier manual analysis
covered 37 units and 1,051 genomes (37.5%).

### Provenance of the fastbaps labels, and the seam

fastbaps was not re-run for this analysis. Labels were transferred from an
earlier PopPIPE execution that used a **different PopPUNK fit** of an earlier
snapshot (2,430 genomes, 42 strains). This is defensible only because the two
fits agree about membership, and that was verified rather than assumed:

- Every one of the 35 analysed strains maps onto **exactly one** archived strain —
  no splitting, no merging. Only the numbering differs (this analysis's
  `strain_12` is archived strain 13), so labels were joined **by membership,
  never by strain identifier**, and the build script aborts if any strain spans
  two archived strains.
- **35 of the earlier manual analysis's 37 units are recovered set-identically.**
  The two exceptions are understood: one unit the manual analysis subdivided a
  further level (`s1_L1_27_L2_69`, n = 45 of 150), and one that gained a single
  genome (`s9_L1_4`, 12 → 13).

**Fifteen genomes (0.6%) entered the collection after that fastbaps run and carry
no label.** Each was assigned to the sub-cluster of its nearest labelled
strain-mate by Mash distance, **subject to a containment test**: a genome joins
only if it is no further from that neighbour than the sub-cluster's labelled
members are from each other. Twelve passed. **Three were refused and excluded** —
for example a genome 0.00262 from its nearest relative in a sub-cluster whose own
members span 0.00089, three times the group's diameter. Without the test these
would have been hung as long branches off clonal units, the configuration that
most inflates r/m. One strain (n = 7, Sri Lanka) was absent from the fastbaps
input entirely and forms a single unit. All fifteen are itemised in
`curated_L1_stragglers.tsv`.

**Cost of the wider coverage, stated plainly:** 258 of the 2,070 analysed genomes
(12.5%) come from strains the manual analysis never screened for modality.

## 2.12.2 Per-unit mapping reference

Completeness is a **gate**, centrality is the **ranking**. A reference must have
≤ 2 contigs, because Gubbins cannot use a multi-contig reference and the replicon
split requires one FASTA per replicon; 90.7% of this collection is draft, so a
plain medoid is usually inadmissible. Among admissible candidates the reference is
the one minimising **mean, then maximum, Mash distance to the unit's members**.
N50 and total length are deliberately not ranking criteria: once the gate is
passed, a longer reference only adds positions other members cannot fill.

A unit with no admissible member **borrows** the nearest complete genome. The
borrow pool is **every complete genome in the 2,802-genome collection (189 after
the gate)**, not merely those inside analysed units — a distinction that matters:
restricting the pool to analysed genomes left 17 units further from their
reference than necessary, one by **5.1×** (mean Mash 0.00402 against 0.00078).

**Result: 82 units, 23 internal and 59 borrowed references, 31 distinct genomes.
Every unit lies within Mash 0.005 of its reference** — SKA2's strain boundary —
with a median of 0.00236.

### Reference FASTA headers are normalised before use

Reference deflines are rewritten to `<accession>_<replicon index>` (e.g.
`GCF_000954175_1_1`) before the run. **This is a correctness requirement, not
tidying.** The workflow names each replicon after the first token of its defline
and keys the analysis unit as `<unit>__<replicon>`; Gubbins then passes
`<unit>.core.full.iteration_N_reconstruction` to RAxML as its run identifier.
**RAxML v8 segfaults when that identifier reaches 128 characters** — measured
directly with all else held constant: 127 characters exits 0, 128 exits 139, and
the working-directory path length is irrelevant. RAxML contains a guard string for
this condition but crashes before printing it, and Gubbins wraps the call in a
bare exception handler that reports only `Unable to fit model to data`.

This collection's original deflines were the full filename plus a contig index,
up to 108 characters. **Before normalisation, 40 of 164 replicon-units (24%)
would have failed**, including one of n = 90. Normalisation reduced the longest
run identifier from 161 to 70 characters. Sequence content is verified
byte-identical; only `>` lines change. The workflow additionally refuses any unit
identifier that would exceed the bound.

This also retires an earlier finding. Three reference genomes had been recorded as
causing Gubbins failures and were excluded. They were exonerated by holding the
alignment **byte-identical** and varying only the filename — run identifier 136
fails, 65 succeeds — and then re-running all six affected units against the
reference that had "broken" each: **12 of 12 succeeded**. No reference is
excluded in this analysis.

## 2.12.3 Alignment, replicon splitting and recombination

**Replicon splitting.** Each reference is split into one FASTA per replicon and
alignment and recombination inference run **per replicon**, keyed
`<unit>__<replicon>`. Gubbins' sliding window must never scan across a contig
junction, where it would call spurious recombination, and `snp-sites` hardcodes
the chromosome field. Replicons shorter than **100 kb** are dropped: a contig-count
check cannot catch a size problem, and one reference carried two ~2.5 kb
pseudo-replicons that would otherwise each have become an analysis unit.

**Variant calling.** Snippy 4.6.0, scattered one task per (unit, genome) and
gathered with `snippy-core`. Invariant A/C/G/T columns are retained in the
alignment handed to Gubbins; feeding it a variant-only alignment would remove the
clonal background against which recombination is defined.

**Recombination.** Gubbins 3.4.3 (`quay.io/biocontainers/gubbins:3.4.3--py310h5140242_0`),
`--tree-builder raxml --iterations 5 --min-snps 3 --invariant-site-correction
--filter-percentage 25`, no starting tree. The version pin and
`--invariant-site-correction` must move together: 3.4.2 made that correction
optional and defaulted it off, so 3.4.3 without the flag would silently drop a
correction 3.3.5 always applied. RAxML is pinned as the tree builder because a
distance-based builder underestimates r/m systematically (2.8.2).

## 2.12.4 Recombination-to-mutation ratio

r/m is **pooled, not averaged**:

> r/m = Σ(SNPs inside recombinations) / Σ(SNPs outside recombinations), summed
> over branches and over both replicons of a unit.

Per-branch ratios are undefined where a branch carries no SNPs outside
recombination — **865 of 8,444 branches (10.2%)** here — and are wildly noisy on
short branches, so averaging them lets the least informative branches dominate.
Both replicons are pooled because they share one genealogy; their agreement is a
consistency check, never evidence of validity.

### The external reference's branches are excluded

The workflow retains the mapping reference as a taxon so the alignment stays
full-length and invariant-site counts remain honest. Gubbins therefore
reconstructs substitutions along the branch leading to it — and that reference
sits outside the population by construction, so the branch is enormous. In one
unit it carried **7,307 of 7,574** SNPs classed as outside recombination, against
4–52 for every real genome.

Those substitutions are population-to-outgroup divergence, not evolution within
the population, and Gubbins scores them outside recombination because they are
genome-wide rather than clustered — placing them in r/m's denominator. **Across
this analysis 52% of all outside-recombination SNPs (458,688 of 881,582) came
from reference branches.**

They are therefore excluded before pooling. Gubbins writes an unrooted tree with
an arbitrary root, and where the reference is the outgroup its divergence is
**split between the `Reference` leaf and the sibling clade at the root** (3,859.7
and 3,774.9 branch units in the worked example), so **both children of the root
are dropped** whenever one of them is the reference. Where the reference instead
nests inside the population — 40 of 82 units, median reference distance 0.00133 —
reference branches contribute **0.0%** and nothing is removed. Where it is a true
outgroup — 42 units, median 0.00297 — they contribute **90.7%**.

Effect: **median r/m 1.85 uncorrected → 6.30 corrected.**

**Validation.** Against the 36 units shared with the manual analysis (same
genomes, same Gubbins settings; different variant caller), the correction removes
an apparent dependence of r/m on reference distance — correlation of reference
distance with log(new/manual r/m) falls from **−0.589 to −0.137** — and tightens
agreement from an interquartile ratio of 0.40–1.54 to **1.26–1.64**, with 32 of 36
within two-fold. The residual **~1.34× offset is a genuine caller difference**
(snippy here, `ska map` in the manual analysis), consistent and directional, and
should be quoted as such rather than treated as noise.

## 2.12.5 Phylogenies

**Per unit.** After recombination removal, a maximum-likelihood tree from the
filtered polymorphic sites: IQ-TREE 2.2.6, GTR with ascertainment-bias correction
(model and constant-site counts taken from a per-unit preflight), **1,000 ultrafast
bootstrap replicates and 1,000 SH-aLRT replicates**. 164 replicon-unit trees.
Gubbins' own node-labelled trees are retained alongside as a second estimator.

**Across units.** One **medoid per unit** — the member minimising mean SNP
distance to the rest of its unit, computed on the recombination-filtered alignment
and excluding the reference taxon — then a parsnp core-genome alignment over those
82 medoids (**82,514 variable sites**) and IQ-TREE under GTR+ASC with the same
support settings. Tips are unit identifiers.

**This global tree is not recombination-corrected, and must not be.** Gubbins
identifies recombination as regions of unusually dense SNPs against a clonal
background; across 82 divergent lineages no shared clonal background exists, so
it would call most of the alignment recombinant — precisely the failure the
partition exists to prevent. The global tree therefore shows how units relate,
its branch lengths include recombination, and **no r/m may be derived from it**.

A neighbour-joining tree on Mash distances over the same medoids is also provided
for quick orientation. **Its branch lengths are Mash distances, not substitutions
per site**, and it must not be grafted onto the per-unit trees or dated.

## 2.12.6 Phylogeny–geography association

Per unit, the **Fitch small-parsimony score** of country labels on the
recombination-corrected topology, compared with a null from **1,000 permutations
of the labels across tips of the same tree**. Permuting holds both the topology
and the country composition fixed, so a unit that is 90% Thai is compared against
other 90%-Thai arrangements — necessary here because the marginal country
distribution is extremely uneven. Tips with unknown country are treated as fully
ambiguous, so missing metadata weakens signal rather than inventing it.

**BioProject was tested identically and reported alongside**, because a
BioProject is typically one study, one laboratory and one country, and a
geographic signal no stronger than the BioProject signal is not evidence of
phylogeography. In this collection **70.5% of genomes are from Thailand and the
top three BioProjects account for 58.4%**.

Units in which every genome shares one country yield a parsimony score of zero
that no permutation can better; they are reported separately and tested instead
against the probability of drawing n genomes of one country at random from the
collection's own country distribution.

## 2.12.7 Metadata

Country, sub-region, BioProject and collection date were joined from a curated
table of 2,804 records. The join is attempted against `sample_id`, `FASTA_name`
and `Assembly Accession` in that order — a naive exact join on `sample_id` alone
matches 73% and accession prefix alone 86%, whereas all three together reach
**99.9% (2,068 of 2,070)**. The two unmatched genomes are listed in
`L1_assignments_unmatched.txt`. Genomes without metadata are retained with empty
fields rather than dropped, so that per-unit denominators remain correct.

## 2.12.8 Reproducibility

The analysis was executed twice: once incrementally across several restarts, and
once **cold from an empty cache and a fresh work directory**. The two runs agree
exactly:

| | result |
|---|---|
| per-unit pooled r/m | **82 of 82 identical to 4 decimal places** |
| total SNPs inside / outside recombination | **1,547,423 / 422,894 in both** |
| Gubbins trees | **164 of 164 byte-identical** |
| recombination predictions | identical content |

The recombination GFFs differ byte-wise in 137 of 164 files, but **line ordering
only** — sorting both sides gives zero differing lines. Gubbins emits records
nondeterministically.

Both runs completed **164 of 164 replicon-units at the highest confidence tier
with zero failures**. Wall-clock was 10.5 h and 11.0 h respectively on a 20-core
workstation; the difference is a cold start plus the addition of branch support,
not extra work.

## 2.12.9 Software

| tool | version | role |
|---|---|---|
| Nextflow | 25.04.6 | workflow |
| PopPUNK | 2.7.6 | strain assignment |
| fastbaps (PopPIPE) | levels = 3 | within-strain sub-clustering |
| Mash | sketch 10,000, k = 21 | distances for reference choice and medoids |
| Snippy | 4.6.0 | reference-based variant calling |
| Gubbins | 3.4.3 | recombination detection |
| RAxML | 8.2.12 (in Gubbins) | tree builder inside Gubbins |
| IQ-TREE | 2.2.6 | per-unit and global ML trees |
| parsnp | 1.7.4 | core-genome alignment for the global tree |

Container digests, the exact command line and per-task resource usage are in each
run's `pipeline_info/`, archived with the results.
