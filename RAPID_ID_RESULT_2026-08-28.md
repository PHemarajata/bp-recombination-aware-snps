# Rapid species ID across all 3,033 assemblies

**2026-08-28.** Prompted by the GAMBIT 3.0 misidentification
(theiagen/public_health_bioinformatics#1127). Ran a species check over the whole
collection rather than the 40 genomes in that report.

> **Result: all 3,033 assemblies are *Burkholderia pseudomallei*.** Every one
> passes the project's mash gate to K96243, and **none is within 700 kb of
> *B. mallei*'s genome size**. The smallest assembly here is 1.12x the size of
> *B. mallei*; the median is 1.22x. This refutes the v3.0.0 *B. mallei* call at
> n = 3,033 rather than n = 40.
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

## 5. What this run did find: two duplicated assemblies

| sample_id | total_bp | vs K96243 | contigs | mash | cgMLST call rate |
|---|---|---|---|---|---|
| `GCA_017356725_2` | 10,628,399 | **1.47x** | **2** | 0.00605 | **0.653** |
| `GCA_017356705_2` | 10,601,007 | **1.46x** | **2** | 0.00605 | **0.608** |

Both are India, `role=assign_only`, in `strain_pp85_L1_1`.

**10.6 Mb in two contigs is not contamination and not a real genome.** A mixed
sample fragments; these are near-perfectly contiguous. The signature is
haplotype duplication: the assembly carries two near-identical copies of the same
genome. That also explains why mash is blind to it. Mash compares sets of distinct
k-mers, and duplicating a genome adds almost no new distinct k-mers, so the
distance stays at the panel median while the assembly is half as long again.

The damage is visible in the allele calls. Panel median cgMLST call rate is
**0.955** (p05 0.941); these two are **0.653 and 0.608**, the two worst genomes in
the entire 2,976-genome pool, presumably because duplicated loci call as ambiguous.

**Impact on reported numbers: none.** Neither genome is in the analysed partition,
neither is a validation genome, and neither wins a nearest-neighbour comparison in
`ATTR_CGMLST.tsv` or `ATTR_ACCESSORY.tsv`. India is represented by 56 genomes in
the pool, so these two are not load-bearing. They are, however, **not in
`PANEL_EXCLUSIONS.tsv`**, and 18 further genomes above 7.60 Mb are also unflagged.

The register already contains the analogous case: `SRR30648681` was excluded as
`mixed_sample` on "SPAdes assembled 12.00 Mb ... at good contiguity". These two
match that pattern and were missed.

**Recommendation:** add an upper genome-size bound to the assembly QC gate. The
existing gates are mash distance and core coverage, and this run demonstrates that
**neither catches a duplicated assembly**. A bound at roughly 7.6 Mb flags 20
genomes for review; a bound at 8.0 Mb flags only the two clear cases. This is a
gate the collection currently lacks, not a re-litigation of the exclusion register.

## 6. What this does not establish

- It does not distinguish *B. pseudomallei* from *B. mallei* by sequence identity,
  because nothing can. The argument is gene content, via size.
- It does not screen for *B. thailandensis*, *B. oklahomensis* or
  *B. humptydooensis*, which are genuinely distinct species within the complex. All
  three would sit further from K96243 than anything observed here, so the
  ≤ 0.012 result argues against their presence, but no member of the complex was
  sketched as a reference. Adding those references would make this a positive
  identification rather than a one-sided distance check. They are not on disk and
  the sandbox has no network access, so that was not done.
- It says nothing about within-species assignment, lineage or ST.

## 7. Artifacts

| file | contents |
|---|---|
| `rapid_id_2026-08-28/RAPID_ID_3033.tsv` | per-genome: mash to K96243, shared hashes, contigs, total_bp, GC. Sorted by descending distance |
| `rapid_id_2026-08-28/dist_raw.tsv` | raw `mash dist` output |
| `rapid_id_2026-08-28/panel3033.msh` | sketch of all 3,033 at `-s 10000 -k 21`, 232 MB. Reusable; rebuilding takes about a minute |
| `rapid_id_2026-08-28/K96243.msh` | reference sketch |
