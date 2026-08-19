# Critique and proposed redesign

**Companion to** `RECOMBINATION_AWARE_PHYLOGENOMICS_HANDOFF.md`. Assessed against
that document only; no pipeline code was read.

**Verdict.** The handoff is a strong account of a pipeline whose hardest chapters
are self-inflicted. §5 (cumulative vs ratio statistics) and §6 (threshold
discipline) are genuinely transferable and I would change nothing in them. But
three chapters — the nine traps, the threshold agony of §6, and the "unsolved"
merge of §9.1 — are not properties of recombination-aware phylogenomics. They
follow from three upstream choices: **per-unit references and per-unit
alignments**, **a partitioner chosen independently of the pipeline's operating
range**, and **empirical threshold derivation where a null simulation was
available**. Fix those and roughly half the document becomes unnecessary.

The most serious problem is not any error the document confesses to. It is that
a 25% yield produced by a size- and divergence-dependent filter is a non-random
exclusion of three quarters of the collection, and §12 treats honest reporting of
that as the remedy.

Claims below marked **[verified]** were checked against tool documentation during
this review; the rest are argument.

---

## Part 1 — Errors of design, ordered by what they cost

### 1.1 Per-unit references manufacture the merge problem that §9.1 calls unsolvable

§9.1 states the backbone is in substitutions per core-genome site and subtrees in
substitutions per *variable* site, so lengths cannot be stitched. This
contradicts §2's own T6/T7: supplying true constant-site counts to the tree
builder is precisely what puts branch lengths in substitutions per site of the
full alignment. If T6 and T7 were followed, the subtrees are already in
per-core-site units and there is no unit mismatch.

What actually differs is the **denominator**. Each unit was aligned to a
different reference, so "core site" denotes a different position set with a
different masked and callable fraction. That is real, but far smaller than
"unsolved research problem", and it exists only because of the per-unit
reference design.

**Align once.** Build one collection-wide, full-length pseudo-alignment per
replicon against a single reference, then define units by **subsetting rows**
rather than re-aligning. Every unit then shares one coordinate system and one
denominator. Consequences:

- §3 disappears entirely — no completeness gate, no constrained medoid, no
  reference borrowing, no distance bound, no universal-reference contrast arm.
- Masks become combinable across units, because an interval means the same
  coordinates everywhere.
- "Reference choice inflated false calls substantially" becomes one controlled
  decision instead of a hazard replicated per unit.

The handoff's own data supports this: the borrowed reference tracked the
universal-reference arm "to within a few points on every statistic." That is a
measurement showing the expensive per-unit machinery bought very little.

The cost is reference bias — divergent lineages lose callable fraction. Measure
and report it per lineage. If it bites, use a small reference panel with a shared
coordinate mapping, not one reference per unit.

**Caveat, and an important one.** Aligning once does *not* mean *correcting*
once. §1's argument — detection degrades as point-mutation density approaches
import density, and runtime is quadratic in n — is correct and survives. Run
correction per unit, on row-subsets of the shared alignment. What is shared is
the coordinate system, not the Gubbins run.

**[verified]** Gubbins ships `generate_files_for_clade_analysis.py`, which
extracts a clade's tree, masked alignment and recombination predictions from a
whole-collection run, noting that "the recombinations will include recombinations
shared by all taxa in the clade, but the masking only corresponds to
recombinations occurring within the clade." This is not a substitute for per-unit
correction at this scale, but it is an excellent **cross-check arm**: run
correction on a moderate backbone subsample, extract clades, and compare against
the independent per-unit runs. Divergence between the two is diagnostic.

### 1.2 Three of the nine traps are artefacts of an avoidable tool choice

T1 (hash-order vs coordinate-carrying output), T2 (the k-mer length that masked
59% of a replicon) and T8 (alignment not rectangular) are specific to split-k-mer
calling. They are well described, and T2's instinct — validate masked fraction
against a mapping caller — is right. The unasked question is why a split-k-mer
caller was primary for a high-GC, repeat-rich, accessory-rich genome. It was
tried, it failed characteristically, and three checks were built around it.

For assemblies, a contig-mapping pipeline (`snippy --ctgs`, or a
minimap2/nucmer-based pseudogenome builder) emits a full-length
reference-coordinate pseudo-alignment directly: coordinate-carrying by
construction, rectangular by construction, no k-mer length to tune. T1, T2 and T8
cease to exist. It is also what most of the published Gubbins literature uses,
which matters for reviewability. Keep the k-mer caller as a triage arm where its
speed is the point.

### 1.3 The partitioner is chosen independently of the operating range, then 75% is filtered out for being outside it

The document's sequence is: lineage-assign, sub-partition, discover one level
deeper shatters strains into pairs, apply a diversity gate, apply a modality
gate, arrive at 25%. Every gate asks "is this unit inside the analysable range?"
— a question the partitioner could answer directly.

The range is known in calibrated pairwise-SNP units (§11: roughly 1,300–4,700
mean pairwise core SNPs). So **define the partition by that range**: build one
collection-wide backbone from SNP-calibrated distances, cut at the depth
producing units inside the range, and split recursively until each unit is both
in range and unimodal. One monotone auditable parameter replaces an opaque level
selection plus two post-hoc screens.

Two consequences. Most of the lost yield returns, because the diversity gate
becomes a construction constraint rather than a filter. And units become clades
by construction, so §7's failure mode 2 ("bridged / mixed unit") largely stops
occurring — and with it most of §8. The modality apparatus exists to detect
structural heterogeneity the partitioner is introducing.

Keep §1's finding that sketch distances mis-scale by 0.88×–91× and are unfit for
defining units. It is correct and it constrains which distance the backbone may
use.

### 1.4 §6's entire problem is solved by simulation, not by more careful empiricism

This is the largest missed opportunity. §6 records thresholds derived, withdrawn
and re-derived; a diversity floor resting on one observation that moved >2× when
measured into the gap; a null at r = 0.14 that became r = 0.81 once the predictor
had variance; a 41-point "empty band" that production data populated. §5.2
explicitly wishes for "a permutation expectation at that sample size" and then
does not build one.

Build it. Details in Part 4. It dissolves §5.1's size confound, most of §6,
§5.2's normalisation problem, and gives §9.3's circularity an exit: the lower
bound of the analysable range is the divergence at which observed r/m becomes
indistinguishable from a no-recombination null — measurable without needing
admissible real units either side of it.

### 1.5 Single-detector output is being treated as measurement

Every acceptance statistic in §4 comes from one tool's spatial scan. The standard
robustness move — a second detector with different assumptions, requiring
concordance — is absent.

**[verified]** ClonalFrameML estimates **R/θ** (rate of recombination relative to
mutation), **1/δ** (inverse mean tract length) and **ν** (divergence of imported
DNA), with per-branch estimation available via `-embranch` /
`-embranch_dispersion`, and `r/m = (R/θ) × δ × ν`.

That decomposition matters more than the concordance check. **Pooled r/m
conflates three parameters, and the three fail differently.** A unit whose r/m is
depressed because ν is low is in a completely different situation from one where
R/θ is low: low ν means imported DNA is too similar to the recipient to leave a
detectable SNP-density signature — real recombination, invisible by construction.
Low R/θ means little recombination. The handoff's single ratio cannot tell these
apart, and its failure-mode catalogue therefore cannot either.

**This is a live sixth hypothesis for §9.4.** A tight cluster of units with clean
modality, adequate size and healthy union coverage returning uniformly depressed
r/m is exactly the signature of predominantly *within-cluster* exchange: donors
and recipients are close relatives, ν is low, tracts carry too few SNPs to call.
Five hypotheses were tested and refuted; this one is directly measurable as ν and
was not, apparently, among them. If ν is low in that cluster and normal
elsewhere, the "unexplained residue" is explained and is not a pipeline failure
at all.

**[verified]** Gubbins exposes `--converge-method`
(`weighted_robinson_foulds` | `robinson_foulds` | `recombination`) and halts on
identical trees across iterations or on hitting the iteration cap. So
**convergence is a free per-unit statistic** and it is not being collected. A
unit that hit the cap without converging has untrustworthy r/m and union
coverage, because detection is conditioned on a tree still in motion. Record
iterations-to-convergence and whether the cap was hit; this is a second candidate
explanation for §9.4.

A third: within-unit heterogeneity in callable fraction. Long N-runs in a subset
of genomes prevent tract calls and depress pooled r/m with no unit-level
signature. Regress per-unit r/m on the **variance** of per-genome callable
fraction, not the mean.

### 1.6 Pass/fail gating biases the analysis it feeds

§7 prescribes "drop" for three of five modes, including "unresolved tree —
detection worked, tree unusable." Dropping on median bootstrap discards real data
for having short internal branches, which in a low-diversity clade is a property
of the truth. And the filter is not random: it preferentially removes small and
divergent units. Any population-genetic quantity estimated on the survivors is
estimated on a sample thinned along axes correlated with the estimand. §9.5
worries about study-level pseudo-replication while a larger selection effect
passes unremarked.

**Propagate instead of exclude.** Collapse unsupported nodes into polytomies and
keep the unit. Carry a set of bootstrap or posterior trees forward so downstream
analyses integrate over topological uncertainty. Reserve exclusion for units
where detection is demonstrably indistinguishable from the null — a statement
Part 4 lets you make quantitatively.

Also pin down §6.8's borrowed bootstrap convention: ultrafast and standard
nonparametric bootstrap are not on the same scale (roughly, 95 in one ≈ 70 in the
other). A unit failing by half a point on an unstated flavour is a decision made
by a citation.

### 1.7 Omissions from the "minimal reproducible protocol"

Three absences cause exactly the failure modes §7 catalogues:

- **No assembly QC gate** — no contamination screen, species-identity/ANI check,
  or assembly size/N50 bound. One contaminated or mixed assembly can dominate a
  unit's recombination output and presents as a "bridged / mixed unit."
- **No pre-masking of mobile elements** — prophage, ICEs, IS elements, rRNA
  operons. These generate false tracts. **[verified]** Gubbins has no `--mask`
  flag for this, so it must be done by editing the input alignment (replace the
  intervals with N) before correction — worth stating explicitly in the protocol
  because there is no flag to remind you.
- **No handling of imports from outside the species.** Introgression from a
  sister species presents as long, unusually divergent tracts and *inflates* r/m
  for a reason the acceptance criteria will read as health. With ClonalFrameML
  this is visible as anomalously high ν.

---

## Part 2 — Internal inconsistencies

**2.1** §3 sets a reference-borrowing distance bound validated on **one** unit.
§6.1 states a threshold with one point either side is a guess with a decimal
point. Both cannot stand.

**2.2** §5.1 reports log(n) vs union coverage at +0.81 and diversity vs union
coverage at +0.26 as two marginal correlations, concluding size is the driver.
Cluster size and cluster diversity are themselves correlated in real collections,
so this needs a partial correlation or a two-predictor regression. The conclusion
is very likely right but is asserted at a lower standard than §6 demands
elsewhere.

**2.3** §9.1's unit mismatch contradicts T6/T7, as set out in 1.1.

**2.4** The §2 "known limitation" is not unavoidable. **[verified]** Gubbins
ships `mask_gubbins_aln.py --aln in.aln --gff out.recombination_predictions.gff
--out out.masked.aln`, which produces a recombination-masked alignment (the
clonal frame). The genuine subtlety is that masking is per-branch, so "the masked
alignment" is not uniquely defined — the honest handling is to count constant
sites **twice**, excluding sites masked on ≥1 branch (conservative) and excluding
none (permissive), and report that branch lengths are insensitive to the choice.
That converts a declared limitation into a two-line sensitivity check.

---

## Part 3 — The redesign

Same tools, different order. Target: near-total inclusion and one commensurable
output.

**Phase 0 — QC and masking.** Contamination and species-identity screen, assembly
bounds. Mask known MGEs, prophage, ICEs, IS elements, rRNA operons by editing the
alignment. Record per-genome callable fraction; it becomes a covariate.

**Phase 1 — align once.** One collection-wide full-length pseudo-alignment per
replicon in one reference coordinate system, built by contig mapping. Assert
rectangularity once. Report per-lineage callable fraction so reference bias is
measured, not assumed.

**Phase 2 — partition into the operating range.** One collection-wide backbone
from SNP-calibrated distances (not sketch distances). Cut at the depth landing
units inside the analysable range; split recursively until each unit is in range
and unimodal. Units are clades sharing one coordinate system; form them by
subsetting rows, never by re-aligning.

**Phase 3 — correct, twice, per unit.** Both a spatial-scan detector and a
model-based one on full-length per-unit alignments, invariant-site correction
passed explicitly on pinned versions. Require tract concordance. Record R/θ, δ
and ν separately — not just pooled r/m — and record iterations-to-convergence and
whether the cap was hit. Cross-check a subsample against clade extraction from a
backbone run.

**Phase 4 — calibrate against simulation.** Part 4 below. Thresholds become
per-unit p-values.

**Phase 5 — trees, with uncertainty retained.** True constant-site counts from
the mask-aware alignment, computed both conservatively and permissively. Collapse
unsupported nodes rather than dropping units. Carry a tree set, not a point tree.

**Phase 6 — merge in one denominator.** Because every unit shares one alignment
and one coordinate system, build the collection-wide tree on the collection-wide
alignment with the union of per-unit masks applied, constraining within-unit
topology to the per-unit corrected trees. All lengths are then substitutions per
core site of the same alignment. This is not a general solution to §9.1 and
should not be sold as one — but it is commensurable and defensible, which is
strictly more than "graft and do not date," and it restores the option of a
date-randomisation test that the current design rules out a priori. The same
construction handles §9.2, with per-replicon trees under a shared mask and
topological discordance reported as a finding rather than a merge failure.

**Phase 7 — downstream honesty.** Study-level weighting and per-study effective
sample size as part of the analysis, not preprocessing. Report measured yield —
but with this design the number should be far closer to the nominated count,
because inclusion no longer depends on passing a filter correlated with size and
divergence.

---

## Part 4 — The simulation calibration, concretely

This is the recommendation that does the most work. It replaces §5's
normalisation problem, most of §6, and §8's size limit.

**The null arm.** For each unit, take its inferred tree, its θ, its alignment
length, its base composition and — critically — its observed missing-data pattern
(the per-genome N mask, applied verbatim). Simulate sequence evolution along that
tree under the fitted substitution model with **no recombination** (Seq-Gen,
pyvolve, or equivalent). Run the identical pipeline end to end, including the
same detector settings and the same reference. Repeat ~100×.

You now have, per unit, the null distribution of union coverage, pooled r/m,
tract length and median bootstrap **at that unit's own n, θ and missing-data
pattern**. Union coverage stops being a statistic you must not threshold and
becomes one you threshold against its own null. Every §6 threshold becomes a
per-unit p-value rather than a global cutoff or a borrowed convention.

**The power arm.** **[verified]** SimBac (PMID 27713837) simulates whole
bacterial genomes with within- and between-species homologous recombination.
Simulate at a grid of R/θ, δ and ν spanning the plausible range for the organism,
at each unit's n and θ, and run the identical pipeline. This gives per-unit
sensitivity and false-discovery rate, and — most valuable — the **detectability
surface in ν**, which tells you directly how low ν can go before r/m collapses.
That surface is what converts §9.4's unexplained residue into either an explained
result or a bounded one.

**What it buys, mapped to the handoff:**

| handoff problem | resolved by |
|---|---|
| §5.1 union coverage is size-confounded | null at matched n |
| §5.2 "normalise against a permutation expectation" | that *is* the null arm |
| §6.1 threshold from one observation | null gives a continuous expectation |
| §6.3 "empty band" in a small calibration set | null populates the band |
| §6.8 round number borrowed from literature | replaced by a p-value |
| §8 modality degrades below n≈25 | null at n=7 gives the sparsity expectation |
| §9.3 lower bound not derivable (circularity) | floor = where r/m meets the null |
| §9.4 unexplained depressed r/m | detectability surface in ν |

The cost is one extra pipeline run per replicate. It is embarrassingly parallel
and cheaper than the hours §6 records losing to withdrawn thresholds.

---

## Part 5 — Keep unchanged

§5 entire — the cumulative/ratio distinction is correct, transferable, and the
unit A / unit B comparison (identical union coverage, r/m 1.25 vs 9.11) is the
most persuasive thing in the document. §6.1–§6.7 as discipline, especially 6.4
(check the predictor has variance before concluding no effect) and 6.7 (retain
withdrawn thresholds with reasons). §7's two memorable joint signatures. §8's
one-sided gap ratio and the diversity-before-modality ordering — the latter is
correct and non-obvious, since gap-over-mean explodes on tight clusters. §12's
insistence on measured rather than nominated yield. T3, T4, T5, T6, T7 and T9,
which are the substance of the method.

---

## Part 6 — On Appendix B

§B.2 and §B.4 advise framing the work as construction rather than validation, on
the theory that "find where this breaks" reads as adversarial and invites a
guarded response. As a description of how to get good analysis this is backwards.
The document's two best sections are products of exactly the adversarial
self-testing B.2 discourages — measuring into the gap beneath a threshold,
checking whether a predictor had variance, pre-registering a prediction that then
failed. Asking a collaborator to attack the pipeline is the request that produces
§5; asking for help building it produces agreement.

There is nothing sensitive about validating a comparative-genomics pipeline on
public assemblies, and no reason to phrase the request as anything other than
what it is. Replace B.2/B.4 with an instruction to state the falsification target
explicitly: name the statistic, the threshold, and what observation would refute
it.

---

## Sources checked during this review

- [Gubbins manual](https://github.com/nickjcroucher/gubbins/blob/master/docs/gubbins_manual.md)
  — `mask_gubbins_aln.py`, `generate_files_for_clade_analysis.py`,
  `--converge-method`, absence of a pre-masking flag
- [ClonalFrameML wiki](https://github.com/xavierdidelot/ClonalFrameML/wiki) and
  [r/m derivation discussion](https://github.com/xavierdidelot/ClonalFrameML/issues/119)
  — R/θ, 1/δ, ν, `-embranch`, `r/m = (R/θ) × δ × ν`
- SimBac, PMID 27713837 — whole-genome bacterial simulation with recombination
- [maskrc-svg](https://github.com/kwongj/maskrc-svg) — masks output from either
  detector, supporting a shared downstream for the dual-detector arm
