# Recombination-aware phylogenomics in recombining bacteria — a methods handoff

**Scope.** How to build recombination-corrected phylogenies for a bacterial
species with substantial homologous recombination, from assemblies, at the scale
of a few thousand genomes. Organism-agnostic. Everything here was learned by
measurement on a real collection; the numbers are given as illustrations, but the
**rules** are what transfer.

**Who this is for.** Anyone standing up a Gubbins/ClonalFrameML-style pipeline on
*Streptococcus pneumoniae*, *Campylobacter*, *Helicobacter*, *Neisseria*,
*Burkholderia*, *Escherichia*, or any other species where r/m is appreciably
above zero.

**The single most useful thing in this document** is §5 — the distinction
between *cumulative* and *ratio* statistics. It is the error that cost us the
most, it is not discussed in the tool documentation, and it will silently corrupt
any acceptance criterion built on the wrong kind of statistic.

---

## 1. The decision that comes first: partition, then correct

**Do not run recombination correction on the whole collection.** Every tool in
this class assumes *limited diversity within a sample sharing a recent common
ancestor*. Detection degrades as point-mutation density approaches
recombination-import density — precisely the deeply-divergent case — and runtime
is quadratic in sample count.

Three consequences:

1. **Partition into strain-like units first**, then correct each independently.
2. **Never feed a concatenated core-gene alignment** to a recombination-detection
   tool. The methods use physical distance between sites; concatenation destroys
   it.
3. **In many species recombination is clade-specific** — restriction–modification
   systems block non-self DNA uptake, so exchange is frequent within clades and
   rare between them. Partitioning is therefore not just a tooling workaround; it
   matches the biology.

**Choosing the partitioner.** Use an assembly-based method that separates core
from accessory divergence (k-mer-based lineage assignment), then sub-partition
with a phylogeny-conditioned BAPS-family method. Two practical findings:

- **Do not sub-partition deeper than you must.** Going one level deeper reduced
  our usable fraction and shattered strains into pairs (median sub-cluster size 2;
  two-thirds of units were singletons or pairs). More levels is not more signal.
- **Distance-only clustering (e.g. Mash-style sketching) is not adequate for
  defining these units.** Benchmarked against alignment-derived pairwise SNP
  distances, it mis-scaled by 0.88×–91× depending on the cluster, because it
  conflates core divergence with gene content. Use it for coarse triage only.

---

## 2. The per-unit pipeline, and the nine traps

This is the settled configuration. Each numbered trap cost us real time; several
fail **silently**, which is why they are listed as traps rather than steps.

### The chain

```
reference selection  →  split by replicon/contig  →  reference-free variant call
   →  ALIGNMENT SANITY CHECK  →  recombination correction (full-length input)
   →  variant-site extraction  →  ML tree with constant-site correction
```

### The traps

**T1 — Use the coordinate-carrying mapping mode of your k-mer caller, not the
alignment mode.** Split k-mer tools typically offer both. Only one emits columns
at true genomic positions; the other emits them in hash-table order. The
recombination tool consumes the latter **without error** and produces
meaningless output. Check that your caller's output is coordinate-ordered.

**T2 — The k-mer length default may be catastrophic, and the failure is
silent-ish.** A default of k=17 gives a split k-mer of 2×8+1 bases, which is far
from unique in a high-GC, repeat-rich genome. On our data the repeat mask removed
**59% of one replicon** at k=17 versus **3.5% at k=31**, and the resulting
alignment tripped the correction tool's taxon filter and dropped nearly every
sample. **Always compare the masked fraction against a conventional mapping
caller on the same reference and samples** — if the k-mer caller loses far more,
it is a k-mer artefact, not divergence.

**T3 — Split by replicon/contig *before* correction.** Sliding-window detection
will scan straight across a chromosome I / chromosome II junction, and common
variant-site tools hardcode the chromosome field. Multi-replicon organisms must
be split; single-chromosome organisms should still ensure a single-contig
reference.

**T4 — Feed FULL-LENGTH pseudogenome alignments, never variant-site
alignments.** The distance between variant sites is an *input* to these methods.
This is the most commonly violated rule in published pipelines.

**T5 — Extract variant sites AFTER correction, never before.** Corollary of T4.

**T6 — Take constant-site counts from the FULL alignment.** Running a
constant-site counter on the tool's filtered-polymorphic-sites output returns
`0,0,0,0` by construction, and passing that to the tree builder silently defeats
the very correction it is meant to supply. **Make the pipeline refuse an all-zero
vector** rather than trusting the operator to notice.

**T7 — Use true constant-site counts, not ascertainment-bias correction, in
composition-skewed genomes.** With true counts the tree builder reproduces
full-alignment base frequencies exactly; ascertainment correction and flat counts
both collapse composition toward 25/25/25/25, which is badly wrong at 68% GC.

**T8 — Assert the alignment is rectangular before correction.** Pipelines often
contain fallback paths that copy raw concatenated sequence into a file the next
tool treats as an alignment. The result is enormous branch lengths with no
recombination involved, and it is expensive to diagnose three steps later. One
line of checking; do it every run.

**T9 — Pin the correction tool version, and verify it from package metadata.**
A minor release made the invariant-site correction *optional and off by default*.
Worse, the bundled VERSION file can report the previous release even on a correct
install, so `--version` is not authoritative. **Pass the correction flag
explicitly rather than relying on the default**, whatever version you believe you
have.

### A limitation worth measuring rather than declaring

Constant-site counts taken from the alignment *as it entered* correction include
constant positions inside masked recombinant tracts. This is widely declared as
unavoidable. **It is measurable, and in our data it is immaterial.**

If your correction tool ships a masking helper, use it: mask recombinant sequence
**per taxon**, recount constant sites, rebuild the tree with each vector, and
compare. Across 62 unit-replicons the constant-site count moved by **0.0%
(median; −0.5% to +1.1%)** and total tree length by **0.1% (median; at most
1.1%)**, with split-matched branch correlations of 0.9988 or better. Both ends of
the bracket give the same tree at the same scale, so the caveat can be closed
with a measurement instead of carried forever.

**Two traps in doing this, and we fell into both.**

**Do not bound it by excluding every column recombinant on *any* branch.** That
sounds conservative and is actually a restatement of union coverage — in our data
r = **+0.997** between the two — so it inherits the whole size confound of §5.1.
It made the limitation look material (tree lengths up to **105×**) on the largest
units purely because they have the most branches. **Recombination is a property
of a branch, not of a column.**

**Do not compare branch lengths positionally.** Two runs of the same tree search
need not emit branches in the same order, so an element-wise correlation of two
Newick files is meaningless. Key each branch by the **split** it induces — the set
of tips below it, canonicalised against its complement — and compare shared
splits. Positional comparison gave us correlations near zero and nearly a
spurious finding; split-matched comparison gave 0.9988.

---

## 3. Choosing a per-unit reference

**Completeness is a GATE, not a ranking term.** Recombination-correction tools
cannot use a multi-contig reference at all. Set a hard maximum (one contig per
replicon) and treat it as pass/fail. An unconstrained medoid selection will
happily return a 135-contig draft.

**Then pick the constrained medoid** — the genome closest to the unit centroid
*among those passing the gate* — with assembly contiguity as a tie-break.

**Borrowing a reference from another unit is acceptable, and "validate it once"
is not enough.** *(Rewritten — the original text validated on a single unit,
which is exactly the failure §6.1 warns against. We had 33 borrows on disk and
had only ever looked at one of them.)*

Many units will contain no complete assembly. We borrowed for **33 of 45 units**
and set a sketch-distance bound well inside the distance to the universal
reference. Measured across all of them:

**The class comparison finds nothing.** Borrowed (33 units) versus internal
medoid (12 units), median values:

| statistic | borrowed | internal | Mann–Whitney p |
|---|---|---|---|
| union coverage | 41.4% | 45.1% | 0.45 |
| pooled r/m | 5.29 | 6.80 | 0.14 |
| tract length | 5,414 | 5,789 | 0.39 |
| median support | 80.5 | 89.0 | 0.43 |

**But the dose–response does not.** Within the borrows, regressing each statistic
on the borrow distance actually used (range 0.0008–0.0048):

| | r | p |
|---|---|---|
| borrow distance vs **pooled r/m** | **−0.38** | **0.028** |
| borrow distance vs median support | −0.34 | 0.057 |
| borrow distance vs tract length | −0.32 | 0.068 |
| borrow distance vs union coverage | −0.31 | 0.083 |

Borrow distance is uncorrelated with unit size (−0.17, p = 0.35) and with
diversity (+0.07, p = 0.71), so this is not a size or divergence artefact;
controlling for either leaves r/m at −0.40. **All four statistics decline with
borrow distance, and they decline *inside* the bound we set.**

**Three lessons, and the third is the transferable one:**

1. **A pass/fail comparison of "borrowed vs not" is the wrong test.** It asks
   whether borrowing is categorically broken, which it is not. The question that
   matters is whether quality degrades *with distance*, and that requires
   regressing on the distance rather than splitting on the label.
2. **Our bound was never validated — it was assumed.** The single-unit check
   confirmed that *one* borrow at *one* distance worked. It could not have
   detected a gradient, because a gradient needs a range. State such a bound as
   **an assumption with a recorded value**, not as a measurement, unless you have
   varied the thing being bounded.
3. **Effects that a threshold hides are still there.** Everything here sits
   within a bound we had told ourselves was safe, and nothing crosses a
   significance line except r/m. The honest report is a measured gradient with
   its uncertainty, not "borrowing is fine" and not "borrowing is broken".

**What to do.** Borrow when you must; record every borrow distance; **report the
dose–response rather than the class comparison**; and prefer the nearest
admissible reference even when a more distant one is inside your bound, because
the cost of distance is continuous rather than a cliff.

**Keep a universal-reference contrast arm** for at least a subset of units. It
costs little and it is what tells you whether a borrowed reference is behaving.

**Keep a universal-reference contrast arm** for at least a subset of units. It
costs little and it is what tells you whether a borrowed reference is behaving.

**Reference choice matters more than people expect.** In our hands a poorly
chosen reference inflated false calls substantially. If you have the budget,
measure reference sensitivity explicitly on a handful of units (two references ×
two replicons is enough) before committing.

---

## 4. Acceptance criteria: what to measure per unit

After correction you have, per unit and per replicon:

| statistic | what it tells you | use it as an acceptance gate? |
|---|---|---|
| **pooled r/m** (SNPs in recombination / SNPs outside) | whether SNPs are being assigned to detected tracts | **yes** — ratio, size-robust |
| **median tract length** | whether detected tracts are biologically plausible | **yes** — compare to the literature value for your species |
| **median bootstrap support** | whether the resulting tree is resolved | **NO — report it, then collapse; see §5.3** |
| **union coverage** (fraction of replicon recombinant on ≥1 branch) | how much of the genome has ever recombined | **NO — size-confounded, see §5** |

**Only one of these four is a defensible gate.** That is a genuinely
uncomfortable finding and it took us three attempts to accept: two of the four
statistics measure sample size or convention as much as biology, so gating on
them filters your collection on something other than what you meant.

**Measure all four anyway.** They fail in different directions and the *pattern*
across them is what identifies the failure mode (§7). Our acceptance criterion is
**pooled r/m**; tract length is a sanity check on it; union coverage and bootstrap
support are **diagnostics that are reported, never thresholded**.

**Bootstrap support is genuinely independent information** — its correlation with
r/m across our units was **−0.01**, so r/m cannot stand in for it. That is exactly
why we first adopted it as a second gate, and exactly why doing so was wrong: the
information is real, but a threshold is the wrong instrument for it. See §5.3.

---

## 5. THE transferable lesson: cumulative vs ratio statistics

**This is the section to read if you read only one.**

Some per-unit statistics **accumulate with sample size** and some do not. Mixing
them into one acceptance rule, or comparing them across units of different size,
produces confident nonsense.

### 5.1 Union coverage is a cumulative statistic — do not threshold it

"Fraction of the genome recombinant on **at least one** branch" sounds like a
property of the population. It is not. More genomes means more branches means
more chances for any given site to be flagged *somewhere*. It only ever goes up.

Measured across 45 units spanning n = 7–155:

| correlate | r | p |
|---|---|---|
| **log(unit size) vs union coverage** | **+0.80** | 4e-11 |
| diversity vs union coverage | +0.28 | 0.062 |
| **log(unit size) vs diversity** — the putative confounder | **−0.01** | 0.95 |
| **partial: log(size) vs union, controlling diversity** | **+0.84** | 2e-12 |
| **partial: diversity vs union, controlling log(size)** | **+0.48** | 0.0009 |

Mean union coverage was **75% for units with n ≥ 45** and **44% for n < 25** —
i.e. the small-unit group sat *below* the cutoff we had been applying, as a
group, for reasons that had nothing to do with biology.

**Run the partial correlation, even when you are confident.** We were challenged
to show the size effect was not really a diversity effect in disguise, and the
test was worth running for two reasons — neither of which was the one we
expected:

- **The confound did not exist.** Size and diversity are uncorrelated here
  (−0.01), so there was nothing to control for, and the size effect *strengthens*
  to +0.84 once diversity is held constant. We could not have known that without
  looking; "these are probably independent" is a hypothesis, not a result.
- **It surfaced an effect we had understated.** Diversity has a genuine
  independent contribution of **+0.48** (p = 0.0009), roughly double what its
  marginal +0.28 suggested — because the marginal is diluted by the much larger
  size effect. We had been treating diversity as a non-driver on the strength of
  that marginal. It is a real second driver, and we would have missed it.

The general point: a marginal correlation answers "does X track Y", which is
rarely the question. The partial answers "does X contribute anything Z does not",
which usually is — and it can revise your estimate **upward** as easily as
explain it away.

**How badly this misleads, in one comparison.** Two units in our set:

| unit | n | union coverage | pooled r/m |
|---|---|---|---|
| A | 49 | 18.0% | 1.25 |
| B | **7** | **17.9%** | **9.11** |

Unit A is a genuine detection failure. Unit B has a pooled r/m among the
healthiest we measured and a normal tract length. **Their union coverage is
identical to one decimal place.** Any threshold on unnormalised union coverage
treats these two identically, and it should not.

**The same defect afflicts empty-bin counts** used for modality screening. A
20-bin histogram of pairwise distances is sparse when a unit has 7 genomes (21
pairs) for reasons of sampling alone. In our data every false rejection produced
by the modality screen at small n traced to the empty-bin term.

### 5.2 Ratio statistics are size-robust — build your criteria on these

- **pooled r/m** — SNPs inside tracts over SNPs outside. Correlation with log(n):
  **+0.37**, and with tree resolution **−0.01**. This is the workhorse.
- **largest-gap-over-mean** — for modality. A ratio; far more stable at small n
  than bin occupancy.

**If you must use union coverage, normalise it** — per branch, or against a
permutation expectation at that sample size — or restrict comparisons to units of
comparable n. Do not apply a fixed cutoff across a 20-fold size range.

**The same warning applies to literature anchors.** A published "X% of the genome
has ever recombined" figure is computed on one genome, species-wide. A per-unit
union coverage inside a shallow cluster is a *different quantity*. We had a unit
exceed the species-wide anchor by 20 points, which is not a contradiction — the
two numbers are not commensurable. Cite such anchors as context, never as a value
your data should reproduce.

### 5.3 Tree resolution is a third, independent axis — and it must not be a gate

Median bootstrap support is uncorrelated with r/m (−0.01) and only weakly related
to size (+0.21). A unit can have **r/m 10.4 and median bootstrap 43** — detection
worked perfectly, the tree is barely resolved. **Measure it explicitly**; nothing
else catches it.

**Do not use it to gate diversity.** Bootstrap support tracks *phylogenetic
signal*, which keeps rising into the high-divergence regime where recombination
detection has already collapsed. In our data a unit whose r/m had collapsed to
0.16 — a total analytical failure — had median bootstrap **98**. It is a useless
floor statistic.

**And do not use it to gate acceptance either.** We adopted a median-support
threshold as a third criterion and **withdrew it**. Two independent reasons, and
the second is the general one:

**(a) The scales are not interchangeable.** IQ-TREE's *ultrafast* bootstrap
(UFBoot) is not on the standard nonparametric scale. UFBoot ≥ 95 is roughly the
conventional SBS ≥ 70. We applied **UFBoot ≥ 70** believing it conservative; it
is **far more permissive** than the convention we cited. If your support values
come from an approximate method, find out what scale they are on before you
threshold them — and say which convention you used, because a reader cannot tell
from the number alone.

**(b) The headline moved 5.3× across defensible choices.** Coverage of our
collection, varying only the support threshold:

| threshold | units | genomes | coverage |
|---|---|---|---|
| **no support gate** | **30** | **933** | **33.3%** |
| UFBoot ≥ 70 (what we first adopted) | 22 | 708 | 25.3% |
| UFBoot ≥ 80 | 17 | 632 | 22.6% |
| UFBoot ≥ 90 | 10 | 437 | 15.6% |
| UFBoot ≥ 95 (UFBoot's own convention) | 7 | 176 | 6.3% |

**A headline that moves 5.3× on a convention is not a measurement.** No reader
can evaluate 25.3% without knowing that 6.3% and 33.3% were equally available.

**What to do instead — collapse, do not discard.** An unsupported branch is not a
broken unit; it is an identifiable piece of a tree that the data do not resolve.
Delete that *edge*, reattach its children to the parent, and the node becomes a
**polytomy** — the tree then asserts exactly what is supported and no more.
Preserve branch lengths additively so root-to-tip distances are unchanged, and
never collapse a terminal branch (a tip carries no support and removing one
deletes a genome).

Reporting the collapse is more informative than reporting a pass rate. On our 180
trees:

| collapse threshold | internal branches removed |
|---|---|
| UFBoot ≥ 70 | 34% |
| UFBoot ≥ 80 | 41% |
| UFBoot ≥ 95 | **58%** |

That 58% is a far more honest description of how resolved these trees are than
"22 of 30 units passed". **Every downstream method should then be one that
tolerates polytomies**, which is the real cost, and it is a cost worth paying to
avoid selecting your collection on a convention.

**The general rule.** When a quality statistic is continuous, identifiable per
branch or per site, and *localised*, prefer collapsing or masking the bad part
over discarding the whole unit. Reserve pass/fail for failures that are
properties of the unit as a whole — which, of our four statistics, only r/m is.

---

## 6. Deriving thresholds without fooling yourself

We derived, withdrew and re-derived several thresholds. The failures were more
instructive than the successes, and they follow a small number of patterns.

**6.1 — Never set a threshold from one observation either side.** Our diversity
floor rested on a single unit. When we finally measured into the gap beneath it,
it moved by more than a factor of two. A threshold with one point either side is
a guess with a decimal point.

**6.2 — Never set a *diversity* threshold using a structurally heterogeneous
unit.** If a unit is bimodal/bridged, its failure is attributable to structure,
not divergence. We made this error, corrected it, then nearly made the mirror
error later — two units that appeared to tighten our floor turned out to be
mixtures, which disqualified both.

**6.3 — An "empty band" in a small calibration set is not a property of the
world.** We justified a cutoff on the grounds that 19 units left a 41-point gap
around it, so any value in a wide range classified identically. Production runs
populated the band, and the cutoff became sensitive to a decision we had told
ourselves did not matter.

**6.4 — Before concluding "no effect", check your predictor has variance.** We
tested union coverage against unit size early, found r = 0.14, and concluded size
did not matter. That test ran on a calibration set that was almost entirely one
size. When production data supplied a 20-fold size range, the same test returned
**r = 0.81**. Absence of spread in the predictor was mistaken for absence of
effect, and the wrong conclusion stood for hours and shaped other decisions.

**6.5 — Cross-sectional and paired analyses answer different questions.** The
same size effect was invisible across units (between-unit biology swamps it) and
obvious within a lineage: subdividing one unit cut its branch count 3.4× and
dropped union coverage 10 points on *both* replicons. When a between-group
comparison comes back null, try a paired one before believing it.

**6.6 — Pre-register predictions, and write the confounds down first.** We
predicted an effect, listed in advance which test units were confounded, and the
prediction failed — but because the confounds were recorded beforehand, the
failure was interpretable rather than arguable. Two of our threshold proposals
were refuted within minutes of being written, by the next unit to finish; the
overfitting caveats attached at the time are what made that legible instead of
embarrassing.

**6.7 — Keep withdrawn versions, marked, with the reason.** A methods appendix
containing only surviving conclusions is a document that will repeat its own
mistakes. Ours retains every superseded threshold with a note on what killed it.
This is the cheapest quality practice in the whole project.

**6.8 — Beware round numbers presented as measurements.** Our final acceptance
threshold was a conventional value borrowed from the literature, and one unit
failed it by half a point. Conventions are fine — but report them as conventions,
with the unfiltered figure alongside.

---

## 7. Failure-mode catalogue

Five distinguishable ways a unit goes wrong. Learn the signatures: they tell you
what to *do*, which a single pass/fail verdict does not.

| mode | union | r/m | tract | bootstrap | action |
|---|---|---|---|---|---|
| **Genuine under-detection** | collapses | collapses | **short** | any | drop — below the analysable range |
| **Bridged / mixed unit** | often normal | ~1–2 | normal | any | **subdivide** — it recovers |
| **Above-ceiling collapse** | normal | collapses | normal | often high | drop — too divergent to correct |
| **Size artefact** | low | **healthy** | normal | any | **keep** — judge on r/m, not union |
| **Unresolved tree** | any | healthy | normal | **low** | **keep and collapse** — detection worked; make the unsupported nodes polytomies (§5.3) |

**Two signatures worth memorising.** Genuine detection failure collapses union
*and* r/m *together*, usually with an abnormally short tract length; that joint
signature is reliable. A low union with healthy r/m and a normal tract is almost
always a small unit, not a broken one.

**Bridging is repairable, and we demonstrated it.** Splitting a bimodal unit into
its modes nearly doubled r/m (2.57 → 4.94) — right diagnosis, working remedy.
**But the same split cut union coverage from 59.5% to 49.5%**, because the child
has a third of the branches. **The prescribed remedy degrades the size-confounded
statistic.** If your acceptance rule uses union coverage, deeper partitioning
will appear to make things worse while actually making them better.

---

## 8. Modality screening, and its size limit

You need to know a unit is unimodal before trusting any diversity-based verdict
on it.

- **Use two statistics at moderate size.** A largest-gap-over-mean ratio catches
  a tight core plus outliers; a histogram-occupancy measure catches several
  clumps spread over a wide range. Neither catches both — one of our units was
  demonstrably four-modal while scoring 0.13 on the gap ratio.
- **Below roughly 25 genomes both degrade**, and the occupancy measure degrades
  *badly*, for the cumulative-statistic reason in §5.1: 7 genomes give 21
  pairwise distances to fill 20 bins, so bins are empty from sparsity alone.
- **Do not discard small units' modality scores entirely.** We treated
  sub-threshold units as "undecidable" and admitted them unscreened; several were
  glaring mixtures, including one scoring 2.7 on a scale where 1.0 is already a
  mixture. **Apply the gap ratio one-sided** — reject on a strong signal, stay
  silent otherwise. In our data the conventional threshold applied this way
  produced **zero** false rejections and would have avoided most of the wasted
  compute.
- **Apply the diversity gate BEFORE the modality gate.** A gap-over-mean ratio
  divides by the mean, so on a very tight cluster one divergent genome produces
  an enormous ratio. Calibrating modality on out-of-range units fails
  characteristically: the "continuous" percentile *rises* with sample size, which
  is impossible for sampling noise and is diagnostic of a mis-composed panel.

---

## 9. What we could NOT solve — and you probably cannot either

**9.1 — Merging per-unit trees is hard under recombination, but not for the
reason we first gave.** *(Rewritten — the original claim contradicted this
document's own T6/T7 and was wrong.)*

We previously wrote that the branch-length units are **incommensurable** — a
backbone in substitutions per core-genome site versus subtrees in substitutions
per *variable* site. **That is not true of a pipeline that follows T6/T7.** If
true constant-site counts from the full alignment are supplied to the tree
builder, the resulting branch lengths are already in substitutions per site of
the **full** alignment, not per variable site. The incommensurability claim was
inherited from an earlier configuration of our pipeline — one that did *not* pass
constant sites correctly — and should not have survived into a document that
prescribes T6/T7 four sections earlier. If you find yourself with genuinely
per-variable-site branch lengths, the bug is upstream: fix T6, do not try to
reconcile the trees.

**What actually remains, which is smaller but real:**

- **Different denominators.** Each unit was aligned against a *different*
  reference, so "per site of the full alignment" denotes a different position set
  in each unit. The lengths are in the same *units* but are not measurements of
  quite the same *thing*. This is a bounded, quantifiable discrepancy — you can
  measure the pairwise overlap of the reference position sets — not an unsolved
  problem.
- **Correction was independent per unit.** Each subtree had recombination removed
  against its own clonal frame, so what counts as "vertical" differs slightly
  between units. This has no standard solution and is the genuine residue.
- **The topological merge itself is solved** and we should have cited it: GTM
  (Smirnov & Warnow 2020) provably minimises topological distance to the guide
  tree. **Its guarantee is topological only** — it decides which edges, and says
  nothing about lengths. That gap is precisely the contribution available here.

**Practical guidance is unchanged even though the diagnosis changed.** Treat a
grafted tree's lengths as approximate and **do not date it**. But state the
reason correctly: the obstacle is heterogeneous denominators and per-unit
correction, not a unit mismatch — and if your write-up claims the latter while
also prescribing T6/T7, a reader is entitled to notice that both cannot be true.

**One thing that dissolves most of this**, if you are willing to pay for it: call
variants for the whole collection against a **single** reference, then partition
and correct. Every unit then shares one denominator and only the
independent-correction residue survives. We did not do this because it means
re-calling every genome and invalidating completed runs — and because, for a
claim about *method behaviour*, the merge is not needed at all. Decide whether
you actually need one collection-wide tree before paying for it; in our case, we
did not.

**9.2 — The same problem recurs one level down.** If you split by replicon (T3),
each unit now has two trees. Merging *those* is the same unsolved problem in
miniature, and accessory-rich secondary replicons make topological discordance
expected rather than exceptional.

**9.3 — The lower bound of the analysable range may not be derivable.** Ours is
bracketed to a 3.1× interval, and every observation supporting it proved
inadmissible: two were mixtures (disqualified by 6.2), and the third could not be
assessed because modality is only interpretable *inside* the diversity range
whose lower bound is the quantity being derived. **That circularity is
structural, not an artefact of our data.** Expect to hit it.

**9.4 — Some failures have no upstream predictor.** A tight cluster of our units
— clean modality, adequate size, healthy union coverage — returned uniformly
depressed r/m. **Seven hypotheses have now been tested and refuted.** Budget for
a residue of unexplained failures instead of assuming a predictor exists.

Two of the seven are worth naming, because they are the ones a reviewer will
propose and both are cheap to test:

- **Callable-fraction variance.** If genomes within a unit differ widely in how
  much of the reference they call, the shared core is small and patchy. Measured:
  r = −0.18 (p = 0.23) against pooled r/m, and our suspect units had *lower*
  variance than the rest — the opposite of the prediction.
- **Low ν — recombination from donors too close to detect.** This is the good
  hypothesis, because r/m conflates three separable quantities (R/θ × δ × ν) and
  a unit importing near-identical DNA would look non-recombining to any
  density-based detector while recombining normally. **Decompose r/m with a
  model-based tool rather than assuming.** In our data ν was **identical** between
  suspect and healthy units (ratio 1.00 on both replicons) and varied *more
  between replicons* (+7 to +13%) than between units (≤8%) — i.e. ν was a
  constant of the organism, not a variable, and could not explain a 4.5× spread
  in r/m.

**The transferable point is the decomposition itself, not our negative result.**
If your acceptance criterion is r/m, you are thresholding a product of three
parameters, and a unit can fail on any one of them for reasons that demand
different responses. Measure them separately at least once before believing that
a low r/m means what you think it means.

**9.4a — And check whether your criterion is tool-dependent.** Running a second,
model-based recombination estimator on the same alignments gave us r/m values
**1.7–8.0× higher** than the first tool (median 4.3×) and, more importantly, a
**different ordering** of the same units — the lowest-r/m unit under one tool was
the second-highest under the other (Spearman +0.31 on six units). A systematic
offset between two estimators is expected and harmless; a *reordering* is not,
because a threshold acts on order.

We report this as an open flag rather than a result — six units has almost no
power, and bridged population structure is a competing explanation — but the
lesson is cheap to act on: **if a single statistic is your only gate, estimate it
twice with independent tools before trusting which units it rejects.**

**9.5 — Effective sample size is smaller than n.** Public collections are
dominated by a few large studies; ours had 81% of one country's genomes from
three projects. Pseudo-replication operates at the study level, so report
per-study effective sample size beside any population-level claim, and treat
geographic weighting as part of the analysis rather than preprocessing.

---

## 10. A minimal reproducible protocol

For each unit, per replicon:

1. Select a reference: completeness as a **gate**, then constrained medoid.
2. Split the reference by replicon; index it.
3. Call variants reference-free, in **coordinate-carrying mode**, with a k-mer
   length validated against a mapping caller on the same data.
4. **Assert the alignment is rectangular.**
5. Correct recombination on the **full-length** alignment, with the
   invariant-site correction passed **explicitly**, on a **pinned** version.
6. Extract variant sites **after** correction.
7. Take constant-site counts from the **full** alignment; **refuse an all-zero
   vector**.
8. Build the ML tree with true constant-site counts (not ascertainment
   correction) and bootstrap support.

Then score each unit on **pooled r/m**, **median tract length**, **median
bootstrap support**, and — only if normalised or size-matched — union coverage.

**Report per unit, not just per collection.** A single coverage percentage hides
which units failed and why.

---

## 11. What generalises, and what does not

**Transfers to any recombining bacterium:**

- Partition before correction; never feed concatenated core-gene alignments.
- Full-length alignments in, variant sites out afterwards.
- Constant-site counts from the full alignment, with an all-zero guard.
- Completeness of the reference as a gate.
- Cumulative vs ratio statistics (§5) — this is a property of the statistics, not
  of any organism.
- The threshold-derivation discipline in §6.
- The failure-mode signatures in §7.
- The merge being unsolved (§9.1).

**Needs re-measuring for your organism:**

- **The analysable diversity range.** Ours spanned roughly 1,300–4,700 mean
  pairwise core SNPs. That number is a function of your species' r/m, tract
  length and genome size, and **must not be transferred**.
- **k-mer length.** Ours was driven by 68% GC and repeat content. Validate
  against a mapping caller rather than assuming.
- **Whether recombination is clade-specific.** Determines how much partitioning
  buys you.
- **Expected r/m and tract length.** Use them as sanity anchors, not thresholds.
- **Whether a secondary replicon exists** and how discordant it is.

**A caution about literature anchors generally.** Published species-wide values
(r/m, "% ever recombined") are computed on different quantities from your
per-unit measurements. They are useful for spotting order-of-magnitude errors and
useless as acceptance thresholds. We twice built a criterion on such an anchor and
twice had to withdraw it.

---

## 12. Expected yield, and why to measure it early

Nominating units for analysis is not the same as having analysable units, and
**neither is the same as having tried.** Our final figures, which moved three
times:

| figure | value | what it is |
|---|---|---|
| nominated | 44.0% | units submitted for analysis — **never a result** |
| survived, first reported | 33.3% | before the composite units were caught |
| **survived, corrected** | **30.4%** | of the whole collection |
| **survived, eligible denominator** | **35.1%** | of the genomes that could ever have been partitioned |

**Report the denominator with the number, always.** 13% of our collection sat in
groups too small to partition at all. Those genomes are not analytical failures —
they were never candidates — but a single "X% analysable" figure silently counts
them as failures. The gap between 30.4% and 35.1% is entirely a choice about what
counts as having been attempted, and a reader cannot recover it from either
number alone.

The blocks performed very differently:

| block | yield |
|---|---|
| units screened for modality (n ≥ 25) | 82% pass detection |
| units admitted unscreened (n < 25) | 64% |
| units exempted from screening by category | **56%** |

**The worst-performing block was the one exempted on the weakest grounds** —
admitted because of what it *was* (a lineage-level cluster rather than a
sub-cluster) rather than because it had been measured. Category-based exemptions
from screening do not survive contact with data.

**We later withdrew that block entirely, and the reason generalises.** When those
units were finally sub-partitioned, their apparent diversity turned out to be
manufactured by mixture structure rather than by within-lineage divergence. One
sat at an apparent 1,265 mean pairwise SNPs — inside our operating range, right
at the floor — and resolved into a 36-genome clonal core at **55** SNPs plus
outliers. It had never been a unit at all.

**A bridged unit's diversity is a property of its bridging.** This is why §6.2
forbids setting a diversity threshold from a structurally heterogeneous unit, and
it is a stronger statement than we first made: such a unit does not merely give
an unreliable diversity estimate, it gives one that is *mostly structure*. Screen
for modality before you believe a diversity value, not after.

**The counterpart finding is more encouraging.** In the one case where the
composite did contain a genuine in-range core, splitting it off raised pooled r/m
from 2.89 to **12.89** — from barely usable to the top of our whole study — by
removing five genomes from thirty-six. Subdivision genuinely repairs r/m. It
fails only when the core that remains falls below the diversity floor, which is
what happened in the other eight cases.

**Report the measured yield, never the nominated count.** And run a handful of
units end-to-end *before* committing to a partition — our yield estimate moved by
19 percentage points once real results arrived, in both directions at different
points during the analysis.

---

## Appendix: a checklist you can paste into a protocol

- [ ] Partition first; units are strain-like, not size-capped
- [ ] Reference: ≤1 contig per replicon (**gate**), constrained medoid
- [ ] Reference borrowing bounded by a recorded distance, and the **dose–response
      on that distance measured** across all borrows — not validated on one
- [ ] Split by replicon before correction
- [ ] Coordinate-carrying caller mode
- [ ] k-mer length validated against a mapping caller (report masked %)
- [ ] Alignment asserted rectangular
- [ ] Correction on full-length alignment, invariant-site flag **explicit**
- [ ] Correction tool version pinned **and verified from package metadata**
- [ ] Variant sites extracted after correction
- [ ] Constant sites from full alignment; all-zero vector refused
- [ ] True constant-site counts, not ascertainment correction
- [ ] Scored on r/m + tract + bootstrap + union; **only r/m used as a gate**
- [ ] Support values checked for **which bootstrap scale** they are on before any
      comparison to a published threshold
- [ ] Unsupported branches **collapsed into polytomies**, not used to drop units;
      collapsed fraction reported
- [ ] Downstream methods verified to tolerate polytomies
- [ ] Modality screened, one-sided below the size limit
- [ ] Diversity gate applied **before** modality gate
- [ ] Mixtures excluded from any threshold derivation
- [ ] Every threshold reported with its bracket and the number of supporting points
- [ ] **Any headline number re-computed across the range of defensible thresholds,
      and the spread reported** — if it moves several-fold, it is a convention
- [ ] Withdrawn thresholds retained in the record with reasons
- [ ] Per-unit results reported, not just a collection-level percentage
- [ ] Merge treated as an open problem **for the right reason** (§9.1), not a
      pipeline step


---

## Appendix B: prompt scaffold for a fresh model session

Paste this document as context, then open with the block below, filling the five
bracketed fields. It is written to state the task in the register it actually
occupies — building and validating a standard comparative-genomics pipeline —
because a request phrased as construction gets a cleaner, faster response than the
same work phrased as adversarial ("break", "attack", "evade").

### B.1 The opening prompt

> I am building a recombination-aware phylogenomics pipeline for **[SPECIES]**, a
> bacterium with substantial homologous recombination. I have **[N]** public
> genome assemblies. My goal is a set of validated, recombination-corrected
> per-lineage phylogenies suitable for downstream population-genetic analysis.
>
> The attached methods handoff is a hard-won protocol from the same class of
> problem in a different organism. Treat its **rules** as settled and its
> **numbers** as illustrative only — the diversity range, k-mer length and r/m
> anchors must be re-measured for **[SPECIES]**.
>
> Organism parameters I already know:
> - approximate genome size and replicon structure: **[e.g. ~2.2 Mbp, single
>   chromosome / ~7 Mbp, two replicons]**
> - GC content: **[X%]**
> - published r/m and mean tract length, if any: **[values or "unknown"]**
>
> Please start by proposing (a) the partitioning strategy, (b) the per-unit
> pipeline with the nine traps from §2 addressed for this organism, and (c) which
> of the handoff's numbers I must re-measure versus can adopt. Do not run
> anything yet — I want to agree the design first.

### B.2 Why this framing works

- **It names the deliverable, not a target to defeat.** "Validated per-lineage
  phylogenies" is the actual goal. Phrasings like "find where the method breaks"
  or "attack the pipeline" describe the *same* validation work but read as
  adversarial and invite a more guarded response. Say what you are building.
- **It scopes the model's first move to design, not execution** ("do not run
  anything yet"). This surfaces disagreements about the plan before compute is
  spent, and keeps the first exchange in analysis rather than action.
- **It marks what is settled versus open**, so the model spends its effort on the
  organism-specific unknowns rather than re-deriving the parts you have already
  paid for.

### B.3 Follow-up prompts, in order

Use these once the design is agreed. Each is self-contained and constructive.

**State the falsification target with each one.** This is the single most
valuable change we made to how we work, and it is what actually produced §5 and
§6. A step phrased as "measure X" gets you a number and no way to tell whether it
is any good. A step phrased as "measure X; **this is what would show the answer
is wrong; this is the threshold; this is what I do in that case**" gets you a
number you can act on — and, in our experience, refutes about a third of what you
expected. Two of our threshold proposals were refuted within minutes of being
written, by the next unit to finish, and that was cheap only because the refuting
observation had been named in advance.

The pattern is: **name the statistic, name the value that would refute the
claim, and name the consequence.**

1. **Partition.** "Run the partitioner we agreed. Report the number of units, the
   size distribution, and the diversity distribution in calibrated pairwise-SNP
   units. Flag any unit that is multi-modal.
   > *Falsification:* if the median unit falls outside the diversity range we
   > agreed, or if more than half of units are singletons or pairs, the partition
   > is at the wrong depth — **report that and stop**, rather than proceeding to
   > per-unit runs that cannot succeed."
2. **Calibrate the diversity range.** "Run the reduced protocol (§2, ska_map arm
   only, both replicons, close + universal reference) on **[6–10]** units chosen
   to span the diversity range. Report r/m, tract length, union coverage and
   bootstrap per unit. We are locating the analysable floor and ceiling — do not
   assume the handoff's values.
   > *Falsification:* the floor is only established if a unit **below** it fails
   > and a unit **above** it works, with neither being a mixture (§6.2). If every
   > supporting observation is a mixture, or the bracket rests on one point either
   > side, **report the bracket as underdetermined** — do not report a number."
3. **Screen and triage.** "Apply the acceptance criterion from §4–§5. Report the
   measured yield by block, and list every unit that fails with its failure mode
   from the §7 catalogue.
   > *Falsification:* recompute the headline yield across the full range of
   > defensible thresholds for **every** screen. If it moves more than ~2× on any
   > of them, that screen is reporting a convention rather than a measurement —
   > **drop it as a gate and report the diagnostic instead** (this is exactly what
   > happened to our bootstrap gate, §5.3)."
4. **Check the size confound before believing any correlate.** "For each per-unit
   statistic, report its correlation with log(unit size) and with diversity, and
   the **partial** correlation of each controlling the other.
   > *Falsification:* any statistic correlating with log(n) above ~0.5 is
   > cumulative and **must not be thresholded** (§5.1). And before concluding *no*
   > effect, report the spread of the predictor — a null on a set with no variance
   > in the predictor is not evidence of anything (§6.4)."
5. **Report.** "Draft a methods section covering everything settled, with a
   limitations subsection. Quote measured yield, never nominated counts. Keep any
   threshold you could not derive as an explicit open item, **with its bracket and
   the number of admissible supporting observations**, and keep withdrawn
   thresholds in the record with the reason each was withdrawn."

### B.3a A prompt that is worth its own step: attack the finished result

Once you have a result, ask for it to be argued against, **with the cost of each
proposed remedy stated**:

> Here is the pipeline, the acceptance criteria and the measured yield. Identify
> the claims that are least supported by the evidence given. For each one, say
> what observation would settle it, and **estimate what that observation costs**
> in compute and in invalidated prior work. Rank by (value of settling it) /
> (cost), and say plainly which ones are not worth settling.

The cost clause matters. A critique written without having run the pipeline will
identify real design debt accurately and **systematically underestimate what it
costs to repay** — in our case the central recommendation would have discarded 45
completed runs to fix problems that four cheap checks closed. Ask for both halves
and you get a usable plan instead of a rebuild.

### B.4 If a session still stalls

The work in this handoff is routine authorised comparative genomics on public
data. If a session hesitates, the fix is almost always to **re-anchor on the
deliverable**: restate that you are building and validating a pipeline for
published assemblies, name the intended downstream analysis, and ask for the
specific analytical step you need. Do not escalate the framing toward
adversarial language to force progress — that is what triggers caution, not what
resolves it. State the constructive goal plainly and the request goes through.
