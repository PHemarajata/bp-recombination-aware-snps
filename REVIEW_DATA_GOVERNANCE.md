# What was withheld, what was substituted, and how to get the rest

## The constraint

*Burkholderia pseudomallei* is a US Tier 1 Select Agent. The study metadata joins
accession to isolation location, collection date and exposure label, and for rare
cases that combination is re-identifiable. The repository has therefore never tracked
isolate-level data: `.gitignore` denies everything by default and re-admits only source
code and documentation, at the top level, by extension.

That policy governs this package too. Applying it consistently mattered, because
several tables a reviewer would naturally want are exactly the join the policy exists
to prevent.

## What is included

**Aggregate and per-unit tables**, which carry no genome identifiers and are sufficient
to recheck the headline numbers:

| file | what it supports |
|---|---|
| `NUMBERS.tsv` | every canonical quantity, with its source and its do-not-quote annotations |
| `GATE1_ALIGNMENT_2026-08-21.tsv` | per-unit diversity and Gate 1 class on both metrics |
| `recombination_rm.tsv` | per-unit r/m, corrected and uncorrected |
| `DISTANCES_v4c_SUMMARY.tsv` | per-unit-replicon diversity, masking, tract statistics |
| `GROUPING_LADDER.tsv` | the attribution ladder, all groupings and all estimators |
| `ABSTENTION_*.tsv` | abstention curve and operating points |
| `MLST_ATTRIBUTION_SUMMARY.tsv` | the 7-locus comparison |
| `TIER2_null.txt`, `SPIKEIN_RESULT.txt` | the null and the sensitivity bound |
| `TREEBUILDER_EQ_RESULT.txt`, `RAPIDNJ_EQ_RESULT.txt` | per-comparison tree-builder results |

`recombination_rm.tsv` contains accessions in its `max_kept_branch` column, naming
which taxon carried the longest surviving branch. Accessions alone are public records
in ENA and NCBI; it is the join to exposure that is restricted, and that column carries
no such join.

## What is withheld

Four tables, all of which join a genome identifier to geography or exposure:

| file | why |
|---|---|
| `L1v4c_MERGED_METADATA.tsv` | accession joined to country, subregion, collection date, isolation location, exposure label and validation status. The full re-identification surface. |
| `CGMLST_LICHT_ATTRIBUTION.tsv` | accession joined to exposure country, plus the identity of its nearest neighbour |
| `GROUPING_PREDICTIONS.tsv` | accession joined to true and predicted geography at every grouping |
| `FINAL_PARTITION.tsv` | accession to analysis unit. Lower risk, since accessions are public and unit assignment is derived, but it enumerates the study membership. |

## What was substituted so the numbers stay checkable

`evidence/DEIDENTIFIED_AGGREGATES.md` is generated from `GROUPING_PREDICTIONS.tsv` and
carries every count the attribution figures and claims are built from, with no genome
identifiers:

- the region confusion matrix, in full, including the rows for regions never predicted
- accuracy stratified by distance to nearest panel genome, for both region and country
- the vote-share distributions for correct and incorrect calls
- the five regional errors, described by true region, predicted region, distance and
  vote share, with no sample identifiers

That is enough to reconstruct panels B, C and D of the attribution figure and to test
the depth control independently. It is not enough to re-derive the predictions from the
distances, which would require the withheld tables.

## The honest limitation

You cannot audit the attribution result end to end from this package. You can check
that the reported counts are internally consistent, that the stratification supports the
claim made from it, and that the estimator is used consistently. You cannot check that
a given genome's exposure label is correct, or that the nearest-neighbour computation
was done correctly, because both require the identifiable tables.

If that gap matters for your assessment, say so and request them. They exist, they are
small, and releasing them is a decision about data governance rather than a technical
obstacle. The likely routes are a data use agreement, or review conducted on the
analysis workstation rather than on a copy.

## What no route can provide

Raw reads and assemblies run to roughly 300 GB and are not transferable in any
practical sense. Recomputation from raw inputs is not available to an external reviewer
under any arrangement contemplated here, which is a real limit on what this review can
establish and should be stated as such in any report.
