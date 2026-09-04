# Independent review package

*Burkholderia pseudomallei* recombination-aware SNP phylogeny, and genomic source
attribution. Staged 2026-09-04 for independent methodological review.

**What is being asked of you.** Vet the methodology and the reasoning, and assess
risk. Not to confirm the numbers are arithmetically right, though you can check
most of them here, but to judge whether the analyses answer the questions they
claim to, whether the controls rule out what they are supposed to rule out, and
where the argument would break under pressure.

---

## Start here, in this order

| | | |
|---|---|---|
| 1 | `REVIEW/RISK_REGISTER.md` | **Read this first.** Sixteen errors this project made and caught, each with what produced it, what it would have cost, and how it is now prevented. It is the honest account of how reliable the rest is. |
| 2 | `repository/PRIMER_HOW_TO_READ_THIS_WORK.md` | Written before this review was contemplated, for someone judging the reasoning rather than taking it on trust. Its Part 5 is about how to catch errors, including the authors'. |
| 3 | `REVIEW/WHAT_TO_CHALLENGE.md` | Where I would attack this if it were not mine. The weakest joints, named. |
| 4 | `REVIEW/HOW_TO_VERIFY.md` | Re-derive the headline numbers yourself from `evidence/`, with the commands. |
| 5 | `REVIEW/DOCUMENT_MAP.md` | All 93 documents, what each is for, and which are superseded. |

Then the science: `repository/METHODS_DRAFT_2026-08-19.md` for what was done,
`repository/MANUSCRIPT_DRAFT_2026-09-02.md` for what is claimed, and
`repository/DISCUSSION_ATTRIBUTION_2026-09-04.md` for the attribution argument.

---

## What is in the package

```
README.md            this file
REVIEW/              the review layer, written for this handover
repository/          the complete tracked repository, 240 files, nothing omitted
                     or reorganised. 93 documents, 90 Python, 48 shell.
pipeline/            the Nextflow workflow that produced the results, at
                     v1.1.0-mod, 164 files
evidence/            derived tables sufficient to recheck the headline numbers
figures/             generated figures and tables, light and dark variants
```

**The repository is copied intact.** Nothing has been curated out of it. Working
notes, superseded results and abandoned lines are all present, because for a
review of reasoning the discarded branches are evidence too. `REVIEW/DOCUMENT_MAP.md`
tells you which is which so you are not misled by a stale document, but it hides
nothing.

---

## Two things this package cannot give you, and why

**The isolate data is not here.** The organism is a US Tier 1 Select Agent, and
the study metadata joins accession to isolation location, collection date and
exposure label, which is re-identifiable for rare cases. The repository has
therefore never tracked isolate-level data, by an explicit policy that denies
everything by default. Raw inputs and intermediates run to roughly 300 GB and live
on the analysis workstation.

What that costs you: you cannot recompute from reads or assemblies. What it does
not cost you: `evidence/` carries the per-unit and aggregate tables, so r/m, the
Gate 1 classification, the attribution ladder, the null, the spike-in and the
tree-builder comparison are all recheckable. See `REVIEW/DATA_GOVERNANCE.md` for
exactly what was withheld, what was substituted, and how to request the rest.

**The pipeline is a separate repository, included here as `pipeline/`.** Panel
construction, partitioning, calibration and orchestration are in `repository/`;
the Nextflow workflow that executes variant calling and recombination inference
is `wf-assembly-snps-mod`, copied in at tag `v1.1.0-mod`. Start with
`pipeline/PROVENANCE.md`, which maps the reported analysis to the code that
produced it and is the one document that tells you which release corresponds to
which number.

Two things there are worth a reviewer's attention. **The reported analysis is
`v1.0.5-mod`, not the tag shipped here**, and it is not seed-reproducible;
`v1.1.0-mod` adds the determinism controls but re-running under them produces a
different run rather than validating the pinned one. And the `v1.0.5-mod` tag
message is itself wrong about why, which `PROVENANCE.md` records because a
published tag cannot be corrected.

Both reported runs record the same
Nextflow script identifier `e09a5c4eadba2c5984f6790095423ee4`, a hash of
`main.nf`, so the two executions provably ran byte-identical pipeline code; that
is a stronger claim than a shared commit and it is checkable from the run records
in `repository/PRODUCTION_RUN_PIN_2026-08-24.md`.

---

## The reported basis, so you can spot a number that is off it

Everything quantitative should be on one frozen basis. If you meet a figure that
is not, it is either superseded or wrong, and the risk register explains why that
distinction has mattered here more than once.

| | |
|---|---|
| panel | 2,976 assemblies submitted, 2,959 after duplicate removal |
| **analysed** | **85 units, 2,340 genomes** (`FINAL_BASIS_2026-08-22`) |
| headline r/m | **7.70**, median of 47 in-window units |
| Gate 1 window | **[700, 4700]** mean pairwise core SNPs, alignment-derived, floor bracketed (588, 755] |
| attribution | region **41/46**, country **10/46** over 46 scorable validation genomes |
| cross-hardware control | 88 units, 2,342 genomes, A100. **Not** the reported run |

Four numbers in this project are the same statistic on different bases and are
easy to confuse: r/m is 7.70 or 7.26 or 7.44 or 7.38 depending on partition and
distance metric. `repository/GATE1_ALIGNMENT_RESULT_2026-08-21.md` section 7c
tabulates all four. Only 7.70 is reported.

---

## What the work claims, in four sentences

Recombination detection in this species has a bounded operating range, and that
range had never been measured; outside it a low r/m is a detection failure rather
than a clonal population. On the frozen basis the median r/m among units inside
the window is 7.70, against 1.99 outside, and the all-unit median of 5.51 mixes
measurements with failures and is not reported. Separately, genomic source
attribution resolves the **region** of exposure at 89% and does not resolve the
**country** at all, scoring 22% against a 26% majority baseline. Both results are
accompanied by the controls that would have exposed them as artifacts, and those
controls are the part most worth your attention.
