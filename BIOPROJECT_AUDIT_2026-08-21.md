# BioProject audit: unflagged exposures and duplicate isolates

Run 2026-08-21 against the full ENA census (9,623 read runs + 3,546 assemblies,
unioned and deduplicated to BioSample).

**Headline: the India attribution failure is not a labeling error. It is the same
physical isolate appearing in the reference pool twice under two accessions, one
held out and one not.**

---

## 1. The explicit "ex" convention is well covered

Scanned every ENA record for a travel-exposure country string.

- **37 BioSamples** carry an `ex <country>` record, all from two studies:
  `PRJNA908850` (23) and `PRJNA352974` (14).
- **All 37 are in our panel.**
- **36 of 37 are already flagged** `travel_reattributed` or arrive as ground
  truth in the new batch.

**One miss:**

| sample | ENA country | current flag |
|---|---|---|
| `GCF_002111285_1` | **"USA: Illinois ex Mexico"** | `as_isolated`, country USA |

It is **not** in an analysed unit, so it never affected a unit-level result. But
it is a fifth Mexican-exposure genome and belongs in the validation set.
**Validation becomes 45, and Mexico becomes 5.**

## 2. The critical finding: a held-out isolate is still in the pool

`SAMN23424236` carries **both** a run and an assembly:

| accession | in | label | flag |
|---|---|---|---|
| `SRR17029022` | the new batch (terra40) | **India** | ground truth, **held out** |
| `GCA_030010175` = `GCF_030010175_1_USA_Georgia` | the v4c panel | **USA** | `as_isolated`, **stays in pool** |

**This is one isolate: ATS2021, the aromatherapy bottle isolate from the 2021
outbreak (`PRJNA763213`, PMID 35235727).**

Under leave-group-out, every India-exposure genome is held out, including
`SRR17029022`. Its own duplicate remains in the pool labeled USA and wins the
nearest-neighbour comparison for **5 of the 6 Indian validation genomes, at
d = 0.007 to 0.009**.

So the Indian cases were matching *their own outbreak's isolate*, under the wrong
country. That is not a metadata subtlety. It is a straightforward leak, and it
invalidates the India row of the attribution table.

`PRJNA763213` has 5 BioSamples total (Georgia x2, Kansas, Texas, Minnesota).
`SAMN21441754` (Georgia, `SRR16344671`, GA2021a) is correctly flagged; the second
Georgia record is the bottle isolate above.

## 3. A second new-batch duplicate

| new genome | BioSample | already in panel as | role |
|---|---|---|---|
| `SRR17029022` | `SAMN23424236` | `GCF_030010175_1_USA_Georgia` | ground truth |
| `SRR34266633` | `SAMN49682048` | `GCF_051251265_1` | context |

**This corrects `BATCH3_QC_REPORT_2026-08-21.md` §4, which reported zero
duplicates.** That check compared accession strings and stems, so it could not
see two accession *types* pointing at one BioSample. **2 of 57 new genomes
duplicate an existing panel isolate.**

**Rule going forward: deduplicate on BioSample, never on accession.**

## 4. 16 isolates are in the panel twice, and 7 pairs are inside the same unit

Panel-wide check: 2,542 genomes map to 2,526 BioSamples.

**16 BioSamples are represented by two panel genomes each**, so 32 genomes are
really 16 isolates. Fourteen are Laos pairs from `SAMN141197xx`, one is
Australian, all of the same shape: a RefSeq assembly plus our own SPAdes
assembly of the same isolate's reads.

| | count |
|---|---|
| duplicate BioSamples | **16** |
| **both copies inside the same analysed unit** | **7** |
| only one copy analysed | 0 |
| neither analysed | 9 |

Examples: `GCF_014712835_1_Laos` and `SRR11097784_SPAdes` are both in
`strain_1_L1_8`. `GCF_014712825_1_Laos` and `SRR11097781_SPAdes` are both in
`strain_1_L1_10`.

**Seven units contain the same isolate twice.** That is pseudoreplication inside
the unit: a duplicated tip inflates n, contributes zero-distance pairs to the
distance matrices, and adds a zero-length branch that Gubbins and ClonalFrameML
both see. The effect on r/m is probably small but it is not zero, and it is the
kind of thing a reviewer finds by accident.

## 5. What does NOT need fixing

`PRJNA908850` has 54 BioSamples in ENA, 10 in our panel. Eight are unflagged, but
their ENA countries are plain `USA: GA`, `USA: OH`, `USA: WA` with **no stated
travel**. Under the project's own tier rules they are `C_deposit_only`: a
recorded country, travel unknown. Leaving them unflagged is correct.

Worth noting as a hypothesis rather than a defect: `SRR31608437` and
`SRR31608438` (both `USA: GA`) are the nearest neighbours of the two Vietnamese
validation genomes at **d = 0.009 and 0.014**. Either those Georgia cases share a
lineage with Vietnamese exposure, or they are unstated travel cases. We have no
evidence either way, so they stay tier C.

## 6. Actions, in order

1. **Flag `GCF_030010175_1_USA_Georgia` as India exposure, or drop it as a
   duplicate of `SRR17029022`.** Dropping is cleaner: it is the same isolate and
   the read-derived copy is the one with the documented provenance. **Then re-run
   attribution.** The India row will change and the region number will move.
2. **Drop `SRR34266633`** as a duplicate of `GCF_051251265_1`, or vice versa.
3. **Add `GCF_002111285_1` to `EXPOSURE_OVERRIDES.tsv`** as Mexico exposure.
   Validation goes to 45; Mexico to 5.
4. **Resolve the 16 intra-panel duplicate pairs**, keeping one copy each. Seven
   affect analysed units and should be resolved before any r/m or distance figure
   is quoted from those units.
5. **Add a BioSample-level duplicate check to the ingest path**, so this class of
   error cannot recur.

## 7. What this does to the cgMLST result

`CGMLST_LICHTENEGGER_RESULT_2026-08-21.md` §5(a) attributed 8 country failures to
"deposit-label error in the reference panel." That was half right:

- **India (6 of the 8): a duplicate leak, not a labeling error.** The finding is
  stronger and simpler than stated. Re-run required.
- **Viet Nam (2 of the 8): stands, but downgraded to a hypothesis.** Their
  nearest neighbours are genuine `USA: GA` deposits with no stated travel. They
  may be lineage sharing rather than mislabeling.

The other two mechanisms are untouched:
**§4 (Mexico still 0/4 with 21 references)** and **§5(b) (Philippines to China at
d = 0.01, genuine cross-country lineage sharing)** both stand.
