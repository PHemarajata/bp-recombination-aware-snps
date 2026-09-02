# Rapid species ID across all 3,033 assemblies

**2026-08-28.** Prompted by the GAMBIT 3.0 misidentification
(theiagen/public_health_bioinformatics#1127). Ran a species check over the whole
collection rather than the 40 genomes in that report.

> **Result: all 3,033 assemblies are *Burkholderia pseudomallei*.** Every one is
> nearer a *B. pseudomallei* reference than to *B. mallei*, *B. thailandensis*,
> *B. oklahomensis* or *B. humptydooensis*, and **none is within 700 kb of
> *B. mallei*'s genome size**. The smallest assembly here is 1.12x the size of
> *B. mallei*; the median is 1.22x. This refutes the v3.0.0 *B. mallei* call at
> n = 3,033 rather than n = 40.
>
> **Updated 2026-08-28** with the four complex references downloaded from RefSeq,
> which turns §6's one-sided distance check into a positive identification and
> produces a result that matters on its own: **mash to K96243 cannot exclude
> *B. mallei***, because the two species' references are only 0.0101 apart, inside
> the project's 0.012 gate. Genome size is doing the work, not mash.
>
> **Separately, it found a real QC defect**: two India genomes are duplicated
> assemblies that mash cannot detect. No reported number changes.

`rapid_id_2026-08-28/RAPID_ID_3033.tsv` has the per-genome table.

---

## 1. Why not kmerfinder or GAMBIT

Neither answers the question, and it is worth being explicit about why.

**kmerfinder already calls these *B. mallei*.** Issue #1127 records
`kmerfinder_top_hit = "Burkholderia mallei"` for all 40 genomes under an
*unchanged* database, in both arms. Running it across 3,033 would reproduce that,
not test it.

**GAMBIT 3.0 calls them *B. mallei* by construction.** GTDB collapses
*B. mallei* and *B. pseudomallei* into one species cluster at ~99% ANI, and the
merged cluster carries the older name. There is no database state in which
GAMBIT v3.0.0 distinguishes them.

**No ANI-based or k-mer-based tool can separate these two taxa.** They sit at
about 99.3% ANI, far above the 95% species boundary; that is precisely why GTDB
merged them. fastANI, skani, sourmash and mash would all agree they are one
species, and all would be right. The question "is this *B. pseudomallei* or
*B. mallei*?" is not answerable by any distance-to-reference method.

**What does separate them is gene content, and the cheapest proxy is genome
size.** *B. mallei* is a host-restricted, genome-reduced clone that arose from
within *B. pseudomallei* diversity: ATCC 23344 is **5,835,527 bp** against
K96243's **7,247,547 bp**, a loss of roughly 1.4 Mb through deletion and IS-element
expansion. That difference is large, stable, and visible in any assembly.

So the check run here is mash for species membership plus genome size for the
*mallei*-versus-*pseudomallei* question, which is the discriminating axis.

## 2. What was run

```bash
mash sketch -p 20 -s 10000 -k 21 -o K96243 refs/K96243.fasta
mash sketch -p 20 -s 10000 -k 21 -l paths.txt -o panel3033
mash dist  -p 20 K96243.msh panel3033.msh
```

Sketch size and k are matched to issue #1127 so the numbers are comparable.
Genome sizes were taken from the existing `accessory_bp/ASSEMBLY_STATS_3033.tsv`,
joined on `sample_id`. All 3,033 manifest paths resolve.

⚠ Two traps hit while doing this, both previously recorded and both still live:

- `cgmlst_lichtenegger/MANIFEST.tsv` is **CRLF**, so `awk '{print $NF}'` yields
  paths with a trailing `\r` and every file appears to be missing. Strip `\r`.
- **`sort -n` does not parse scientific notation.** Two mash distances are
  returned as `5e-05`, and `sort -n` ranks them as `5`, i.e. as the largest values
  in the file. The first distance summary computed this way reported a maximum
  *smaller than the minimum*. Compute these percentiles in awk or Python.

## 3. Species membership: all 3,033 pass

Mash distance to K96243:

| | value |
|---|---|
| minimum | 0.000002 |
| median | 0.004899 |
| p90 | 0.006139 |
| p99 | 0.007178 |
| **maximum** | **0.009278** |

| gate | n |
|---|---|
| **≤ 0.012** (the operative code gate) | **3,033** |
| 0.012 to 0.0135 | 0 |
| > 0.0135 (the value of a genome previously excluded as wrong-species) | **0** |

The whole collection sits below the gate with room to spare. The furthest ten
from K96243 are dominated by Australian genomes, which is expected rather than
alarming: Australia is the basal, most divergent part of the species, and the
global tree recovers that independently.

Two of the furthest are `ERR9980356` (0.00928) and `SRR2896271` (0.00871), which
are two of the four **retired** exclusions. Their values here match those recorded
when the exclusions were retired (0.0093 and 0.0087), independently confirming
that decision: they are divergent but comfortably inside the species.

## 4. The *B. mallei* question: not close

| | bp |
|---|---|
| *B. mallei* ATCC 23344 | 5,835,527 |
| *B. pseudomallei* K96243 | 7,247,547 |
| **this collection, minimum** | **6,553,321** |
| this collection, p05 | 7,005,841 |
| this collection, median | 7,133,920 |
| this collection, p95 | 7,325,318 |

- Assemblies within *B. mallei*'s size range, taken generously as anything below
  6.30 Mb: **0 of 3,033**.
- Assemblies at 6.80 Mb or above, i.e. squarely *B. pseudomallei*: **3,023 of
  3,033**.
- Smallest assembly in the collection relative to *B. mallei*: **1.12x**. Median:
  **1.22x**.

For a genome to be *B. mallei* it would have to be missing roughly 1.4 Mb that
every genome here has. None is. The ten below 6.80 Mb are ordinary draft
assemblies with incomplete recovery, not reduced genomes, and all pass the mash
gate.

## 5. What this run did find: two redundant assemblies

| sample_id | total_bp | vs K96243 | contigs | mash | NIPHEM | cgMLST call rate |
|---|---|---|---|---|---|---|
| `GCA_017356725_2` | 10,628,399 | **1.47x** | **2** | 0.00605 | **1,395** | 0.653 |
| `GCA_017356705_2` | 10,601,007 | **1.46x** | **2** | 0.00605 | **1,444** | 0.608 |

Both are India, `role=assign_only`, in `strain_pp85_L1_1`.

> ⚠ **Corrected 2026-08-28.** This section first read that these were haplotype
> duplications, "two near-identical copies of the same genome". That was wrong,
> and BUSCO is what disproved it: a whole-genome duplication would push the
> duplicated-BUSCO score toward 100%, and it is **4.1%**, against **4.3%** for an
> ordinary panel genome. The actual defect is narrower and is set out below.

**Chromosome 2 is deposited twice.** The assemblies have two records:

| record | length | label |
|---|---|---|
| `CP071526.1` | 7,387,707 | "chromosome, complete" |
| `CP076289.1` | 3,240,692 | "chromosome 2, complete" |

*B. pseudomallei* chromosome 1 is ~4.07 Mb, so a 7.39 Mb "chromosome" is not
chromosome 1: it is the **whole genome**. Twenty 200 bp probes drawn at random
from record 2 were all found verbatim in record 1 (**20/20**), while record 1
shows no self-containment above background (1/20). So record 1 is the complete
genome and record 2 repeats chromosome 2. 7.39 + 3.24 = 10.63 Mb.

That explains every observation at once:

- **mash is normal** (0.0060) because repeating existing sequence adds almost no
  new distinct k-mers.
- **BUSCO misses it** because *B. pseudomallei*'s core BUSCOs sit on chromosome 1,
  and it is chromosome 2 that is duplicated.
- **cgMLST call rate collapses** to 0.61 and 0.65, and the mechanism is visible in
  the classification: **NIPHEM** (locus found in multiple *exact* copies) is
  **1,395 and 1,444**, against 116 for a normal genome, while **LNF is normal**
  (44 and 45 against 36). Nothing is missing. About 1,400 loci are present twice.

### 5.1 NIPHEM is the right detector, and it is free

Screening the existing `results_alleles.tsv` across all 3,033:

| NIPHEM | value |
|---|---|
| panel median | 29 |
| p90 | 32 |
| p99 | 41 |
| highest legitimate genome | 131 |
| **the two defective genomes** | **1,395 and 1,444** |

Thirty-five times the p99, with an order-of-magnitude gap between 131 and 1,395.
Exactly **two** genomes exceed 500. Compare the genome-size bound, which flags
**20** genomes of which 18 are ordinary large assemblies. NIPHEM is the specific
test; size is the blunt one.

**Impact on reported numbers: none.** Neither genome is in the analysed partition,
neither is a validation genome, and neither wins a nearest-neighbour comparison in
`ATTR_CGMLST.tsv` or `ATTR_ACCESSORY.tsv`. India is represented by 56 genomes in
the pool. Both are, however, **not in `PANEL_EXCLUSIONS.tsv`**.

Note this is a defect in the **public GenBank deposit** (`GCA_017356725.2` and
`GCA_017356705.2`, strain VBM399), not in anything built here.

**Recommendation:** add `NIPHEM <= 300` to the QC gate. It is computed from output
the pipeline already produces, costs nothing, and is far more specific than a size
bound. Implemented as criterion 4 in `species_id_bp.py`.

## 6. Positive identification against the complex

**Added 2026-08-28.** §6 previously recorded that only K96243 had been sketched,
making the result a one-sided distance check. The four missing references were
downloaded from RefSeq and the panel sketch re-used.

| accession | organism | bp | level |
|---|---|---|---|
| `GCF_033956065.1` | *B. mallei* | 5,834,748 | Complete |
| `GCF_000012365.1` | *B. thailandensis* E264 | 6,723,972 | Complete |
| `GCF_030297255.1` | *B. pseudomallei* (current RefSeq reference) | 7,081,111 | Complete |
| `GCF_000959365.1` | *B. oklahomensis* C6786 | 7,135,022 | Complete |
| `GCF_000011545.1` | *B. pseudomallei* K96243 | 7,247,547 | Complete |
| `GCF_001513745.1` | *B. humptydooensis* | 7,287,809 | Complete |

Requested and returned accessions were diffed: six requested, six returned, no
substitutions. `GCF_000011545.1` is 7,247,547 bp, matching the local
`refs/K96243.fasta` exactly, which confirms the local reference is the canonical
K96243 assembly. Note NCBI's current *B. pseudomallei* reference is **not**
K96243; both are included.

### 6.1 The references calibrate the gate, and the news is not good for mash

| pair | mash |
|---|---|
| *B. pseudomallei* K96243 vs *B. pseudomallei* ref | 0.0048 |
| **_B. mallei_ vs _B. pseudomallei_ ref** | **0.0096** |
| **_B. mallei_ vs _B. pseudomallei_ K96243** | **0.0101** |
| *B. humptydooensis* vs *B. thailandensis* | 0.0587 |
| *B. thailandensis* vs *B. pseudomallei* K96243 | 0.0639 |
| *B. humptydooensis* vs *B. pseudomallei* K96243 | 0.0657 |
| *B. oklahomensis* vs *B. pseudomallei* K96243 | 0.0811 |

**The *B. mallei* reference sits at 0.0101 from K96243, inside the project's
≤ 0.012 gate.** A genuine *B. mallei* genome would pass the mash gate. This is the
same fact that defeats GAMBIT, arriving by a different route, and it means the
mash-to-K96243 gate is a *B. pseudomallei complex* filter rather than a
*B. pseudomallei* filter. §4's genome-size argument is not a convenience; it is the
only part of this analysis that actually discriminates *mallei* from
*pseudomallei*.

The other three species sit at 0.062 to 0.081, roughly seven times the
collection's maximum distance of 0.0093, so they are excluded with a wide margin.

### 6.2 Every genome is *B. pseudomallei*

Nearest reference across all 3,033:

| nearest reference | n |
|---|---|
| *B. pseudomallei* (current RefSeq ref) | 2,395 |
| *B. pseudomallei* K96243 | 638 |
| *B. mallei* / *thailandensis* / *oklahomensis* / *humptydooensis* | **0** |

Margin, defined as distance to *B. mallei* minus distance to the nearer
*B. pseudomallei* reference, is **positive for every genome**: minimum +0.0029,
median +0.0056, maximum +0.0101. **Zero genomes are closer to *B. mallei*.**

Closest approach to each non-*pseudomallei* species anywhere in the collection:
*B. thailandensis* 0.0624, *B. humptydooensis* 0.0648, *B. oklahomensis* 0.0793.
Nothing comes near.

Per-genome distances to all six references are in
`rapid_id_2026-08-28/RAPID_ID_BPC_3033.tsv`, sorted by ascending *mallei* margin
so the least clear-cut genomes are at the top.

## 7. What this does not establish

- It does not distinguish *B. pseudomallei* from *B. mallei* **by sequence
  identity**, because nothing can, and §6.1 now quantifies that: the two references
  are closer to each other than the project's own species gate. The discriminating
  evidence is gene content, via genome size.
- It says nothing about within-species assignment, lineage or ST.
- The four downloaded references are single representatives. A genome that was
  genuinely intermediate would need more than one reference per species to place
  confidently. Nothing here is intermediate, so this does not arise.


## 8. Recommended species-ID method

**Added 2026-08-28**, replacing the mash-only gate. Implemented as
`species_id_bp.py`; results in `SPECIES_ID_2026-08-28.tsv`.

The problem to solve is narrow: *B. mallei* passes any similarity-based gate,
because it is a clone nested inside *B. pseudomallei* diversity. What separates
them is **gene content**: *B. mallei* deleted ~1.4 Mb. So the test has to ask
whether the *B. pseudomallei*-specific genes are present, not how similar the
genome is.

### 8.1 The test: three criteria

| # | criterion | threshold | excludes |
|---|---|---|---|
| 1 | mash to K96243 | ≤ 0.012 | *thailandensis* (0.064), *humptydooensis* (0.066), *oklahomensis* (0.081). **Not *mallei*** |
| 2 | **fraction of 540 diagnostic cgMLST loci called** | **≥ 0.50** | ***B. mallei*** |
| 3 | assembly size | 6.3 to 7.6 Mb | reduced genomes, and duplicated assemblies that 1 and 2 both pass |

Criterion 2 does the work nothing else does. Criteria 1 and 3 are nearly free and
catch different failure modes.

### 8.2 How the 540 loci were chosen

Ran chewBBACA `AlleleCall` against the project's own Lichtenegger schema (4,221
loci) for both *B. pseudomallei* references and **eight complete *B. mallei*
genomes** spanning 5.23 to 5.91 Mb, then kept loci **called in both
*B. pseudomallei* and `LNF` in all eight *B. mallei***. That yields **540 loci**.

The gene loss is visible directly in the `LNF` column: *B. pseudomallei* 33 and
34, against *B. mallei* 614 to 980.

Nothing new has to be run for genomes already in the pipeline. The score is
computed from the existing `results_alleles.tsv`.

### 8.3 Held-out validation, because defining the set on *B. mallei* is circular

Define the locus set on **4** *B. mallei* genomes, score the **other 4**, across
all 70 splits (280 held-out evaluations):

| | score |
|---|---|
| held-out *B. mallei*, median | **0.000** |
| held-out *B. mallei*, **worst case** | **0.061** |
| 3,033 real *B. pseudomallei*, **worst case** | **0.685** |
| 3,033 real *B. pseudomallei*, median | 0.998 |

**A 62-point gap separates the worst *B. pseudomallei* from the worst-case
*B. mallei*.** The 0.50 threshold sits in the middle of it with better than
tenfold margin either way. This is the non-circular evidence: the set generalises
to *B. mallei* strains it was not built from.

The other complex members score 0.71 to 0.80, so they retain most of these loci.
The set is specific to *mallei*'s deletions rather than being a generic
"hard-to-call loci" list, which is also why criterion 1 is still needed.

### 8.4 Result on this collection

| verdict | n |
|---|---|
| ***B. pseudomallei*** | **3,013** |
| `SIZE_OUT_OF_RANGE:high`, all otherwise passing | 20 |
| failing the *B. mallei* test | **0** |

The lowest diagnostic score in the entire collection is **0.685**
(`SRR2896257`), eleven times the worst-case *B. mallei*. The 20 size flags are
the oversized tail of §5, including the two duplicated India assemblies; all 20
score 0.96 or above on criterion 2 and are *B. pseudomallei* by species, so the
flag is an assembly-quality flag, not a species call.

**Every isolate in this collection is documented as *B. pseudomallei* by positive
evidence**: it carries the *B. pseudomallei*-specific gene content that
*B. mallei* lacks, rather than merely resembling a *B. pseudomallei* reference.

### 8.5 For the Methods

> Species identity was confirmed for all 3,033 assemblies by three criteria: mash
> distance to *B. pseudomallei* K96243 ≤ 0.012, which excludes *B. thailandensis*,
> *B. oklahomensis* and *B. humptydooensis*; assembly size between 6.3 and 7.6 Mb;
> and presence of at least 50% of 540 cgMLST loci that are present in
> *B. pseudomallei* reference genomes and absent from all eight complete
> *B. mallei* genomes examined. The third criterion is required because
> *B. mallei* is a genome-reduced clone within *B. pseudomallei* diversity and is
> not separable from it by sequence similarity: the *B. mallei* reference lies
> 0.0101 from K96243, inside the mash gate. Held-out validation over all 70 four-
> versus-four splits of the *B. mallei* panel gave a worst-case held-out
> *B. mallei* score of 0.061 against a worst-case *B. pseudomallei* score of 0.685.
> All 3,033 assemblies satisfied all three criteria except 20 that exceeded the
> upper size bound and were retained after review as *B. pseudomallei*.

### 8.6 Limits

- The 540 loci are defined against **this** cgMLST schema. If the schema changes,
  re-derive them; `species_id_bp.py` errors out rather than scoring on a mismatch.
- Eight *B. mallei* genomes is a small panel, though 70 complete genomes are
  available and the held-out margin is wide. Re-deriving on more would tighten it.
- Criterion 2 tests *absence of B. mallei's deletions*, so it would not flag a
  novel *B. pseudomallei*-complex organism with intact gene content. Criterion 1
  covers the described complex members; something undescribed would need a tree.
- These are draft assemblies; a genuinely fragmented genome loses diagnostic loci
  for reasons unrelated to species, which is why the threshold is 0.50 and not 0.9.

## 9. Artifacts

| file | contents |
|---|---|
| `rapid_id_2026-08-28/RAPID_ID_3033.tsv` | per-genome: mash to K96243, shared hashes, contigs, total_bp, GC. Sorted by descending distance |
| `rapid_id_2026-08-28/dist_raw.tsv` | raw `mash dist` output |
| `rapid_id_2026-08-28/panel3033.msh` | sketch of all 3,033 at `-s 10000 -k 21`, 232 MB. Reusable; rebuilding takes about a minute |
| `rapid_id_2026-08-28/K96243.msh` | reference sketch |
| `rapid_id_2026-08-28/RAPID_ID_BPC_3033.tsv` | per-genome distance to all six complex references, plus the *mallei* margin, contigs, size and GC. Sorted by ascending margin |
| `rapid_id_2026-08-28/dist_bpc.tsv` | raw `mash dist` output, six references x 3,033 |
| `refs_bpc/fasta/` | the six RefSeq reference genomes, named by species |
| `refs_bpc/bpc_refs.msh` | sketch of the six references |
| `refs_bpc/mallei_fasta/` | eight complete *B. mallei* genomes used to derive the diagnostic loci |
| `rapid_id_2026-08-28/BP_DIAGNOSTIC_LOCI.txt` | the 540 diagnostic locus names |
| `species_id_bp.py` | the three-criterion test |
| `SPECIES_ID_2026-08-28.tsv` | per-genome verdict for all 3,033 |
