# Are we ready to draft? — assessment, 2026-08-23

Scope: can Paper 1 (A+D fused — the limits/capability paper) be drafted now,
Methods and Results in particular. Assessed by reading the artifacts, not the
summaries.

> **Verdict: draft the Results now. Do not draft the Methods yet.**
>
> The Results outline is in good shape — internally consistent, every figure
> tied to a regenerable key, all major weak spots resolved or bounded.
> **`METHODS_DRAFT_2026-08-19.md` is not**: its "production analysis" section
> describes a partition that is not the reported one, and its attribution
> section describes an analysis that has been superseded twice. Drafting Results
> against it would import those errors into prose, which is exactly how this
> project accumulated the stale-number problem in the first place.

---

## 1. Results — ready, with four small gaps

`MANUSCRIPT_OUTLINE_2026-08-21.md` is now the mature document. As of today:

- Every attribution figure carries a provenance tag and cites a `NUMBERS.tsv`
  key; **[cg-Licht/46] is the single cgMLST headline** and cg-Pub/29 has left the
  body.
- The estimator is explicit everywhere (country NN, region modal k=20), so the
  forbidden NN-vs-modal comparison cannot be made silently.
- **W2 resolved** — strata are estimator-matched (14/14 · 8/10 · 19/22), the
  attractor mechanism is confirmed on current data, and the abstention rule is
  built, scored and validated out-of-sample.
- **W3 resolved** (r/m 7.70, alignment-derived). **W8 resolved** (exclusions
  retired; register now reaches the cgMLST pool).
- **W8b added** — the assembler effect, quantified.
- Table 1, Table 2, Table 3 and the abstract all recomputed on the current panel.

**Remaining Results gaps, all small:**

| gap | effort | blocking? |
|---|---|---|
| MLST row of Table 5 predates the correction — re-run on n=46 | small | no, tag it |
| Accessory control sub-numbers still n=43 (headline already corrected) | small | no |
| R7 needs Georgia added as a second autochthonous focus (below) | small | no |
| Flow diagram (Figure 1) does not exist; all five numbers now do | small | no |

None of these blocks writing. Three are "re-run a script and update a row".

## 2. Methods — not ready. Three distinct problems

### 2.1 §2.12 describes the wrong partition ⚠ **the main blocker**

The preamble is **correct**: it states the reported partition is the corrected
workstation run, **85 units / 2,340 genomes**, with the A100 88-unit run as the
cross-hardware reproducibility control (lines 1183–1189).

**The body was never rewritten to match.** Eight subsections still report the
88-unit A100 partition as the analysis:

| section | stale content |
|---|---|
| 2.12.1 Genome panel | "**2,976** assemblies" (now 2,959) |
| 2.12.4 Partition | "86 units, 2,352 genomes"; sketch over "all 2,976" |
| 2.12.5 Unit refinement | "**Final partition: 88 units, 2,342 genomes**" |
| 2.12.6 Reference selection | "served the **88 units**" |
| 2.12.7 Alignment / r/m | "misplaces 15 of these **88 units**" |
| 2.12.8 Phylogenies | "over those **88 medoids**"; "across **88** divergent lineages" |
| 2.12.9 Phylogeny–geography | "**2,352** analysed genomes"; "**56 of 88** units" |

§2.12 spans lines 1173–1671 — **about 30% of the draft.** A reader following the
Methods would reconstruct a different analysis from the one reported.

### 2.2 §2.12.11a describes a superseded attribution analysis ⚠ **worst, because it is the central result**

The attribution Methods section describes the **n=26, SNP-unit, modal-label**
analysis from mid-August:

> *"Twenty-six genomes … three estimators … the unit's modal label, its nearest
> neighbour by recombination-filtered SNP distance … correct for 19 of 19
> scorable genomes against a 58% baseline."*

Every element is superseded. The current headline is **cgMLST (Lichtenegger,
4,221 loci), 46 scorable, region modal k=20 41/46 (89%) against a 46% baseline,
κ 0.832**. Grep counts across the whole draft:

| term | mentions |
|---|---|
| Lichtenegger · modal k=20 · kappa · abstention · GROUPING_LADDER | **0 each** |
| leave-outbreak-out · retired | **0 each** |

So the Methods contain **no description of**: the cgMLST scheme actually used,
the modal-k20 estimator, Cohen's κ as the headline statistic, leave-**outbreak**-out
(as distinct from leave-group-out), the abstention rule, or the exclusion-register
retirement mechanism.

### 2.3 Two live self-contradictions

1. **§2.6.3, union coverage** — W10 flagged this and it is **still present**.
   Line 432 establishes union *is* size-confounded (`r(log n, union) = +0.80`,
   p = 4×10⁻¹¹); line 480 states it was "found **not** to scale with unit size
   (r = 0.142)". Both in the same section, 48 lines apart. Delete the second.
2. **§2.12.13 vs the §2.12 preamble** — line 1658 still reads *"The **production
   run** used an NVIDIA DGX Station A100 …; the **control run** a 22-core
   workstation"*, directly contradicting the preamble's flip 470 lines earlier.
   The designation was corrected in one place only.

## 3. What is genuinely ready in the Methods

Worth stating, because the rewrite is smaller than §2 suggests:

- **§2.1–§2.11 (calibration track) is in good shape.** The r/m headline is
  already **7.70** on the alignment-derived Gate 1 (lines 10, 1407, 1419), and
  the Gate 1 window is described in alignment units.
- **§2.8 method validation** (constant sites, tree-builder equivalence,
  zero-recombination null, spike-in recovery) is self-contained and unaffected by
  the partition question.
- **§2.9 "analyses deliberately not performed"** and **§2.11 known limitations**
  are the right shape and mostly survive.
- The **§2.12 preamble** already states the correct basis and the correct reason
  for it — it is the model for what the body should say.

## 4. Recommended order

1. **Draft Results now**, from the outline, citing `NUMBERS.tsv` keys. It is the
   mature document and drafting will surface any remaining prose gaps cheaply.
2. **Rewrite §2.12 onto the frozen basis** — mechanical, and every number needed
   is already in `NUMBERS.tsv` and `FINAL_BASIS_2026-08-22/`. Fix §2.12.13's
   designation while there.
3. **Write §2.12.11a from scratch.** This is new writing, not editing: cgMLST
   scheme + snapshot, the estimator per scale and why, κ as the headline
   statistic, leave-group-out **and** leave-outbreak-out with the Vietnam/Georgia
   counterexample as the justification, the distance stratification, and the
   abstention rule with both baselines.
4. **Delete the stale union paragraph** in §2.6.3 (one paragraph, already
   identified).
5. **Then** the cheap Results gaps (MLST row, accessory sub-numbers, Figure 1).
6. **Then** the non-science blockers: IRB number, data availability + deposition,
   pinned production command line.

**The reproducibility test (open item 1) should come after step 3, not before.**
Re-deriving the collection against a Methods section that describes a different
partition would produce a diff nobody can interpret.

## 5. Honest risk register for drafting

- **The Methods rewrite is where stale numbers will try to re-enter.** Every
  figure in §2.12 must come from `NUMBERS.tsv` or `FINAL_PARTITION.tsv` at the
  moment of writing, not from the existing prose.
- **Two partitions will remain in the paper** (85 reported, 88 control). That is
  correct and defensible, but §2.12.10 must make the roles unmistakable, because
  this is the single most confusing thing in the corpus.
- **n=46 is small** and the paper's honesty depends on saying so three ways
  (W1 pseudoreplication, W7 the effective class count, and the new batch-
  enrichment check). Those are drafted; keep them.
- **The abstention threshold is calibrated on 46 genomes** and its signal was
  chosen after seeing which won. Disclosed in `ABSTENTION_RESULT` §7 — carry that
  caveat into the paper verbatim rather than softening it.
