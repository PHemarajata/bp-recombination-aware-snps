# A primer: how to read, question, and defend this work

Written for someone with genomic-epi and phylogenetics training who wants to
judge the *reasoning* rather than take it on trust. Every concept below is
anchored to a real decision in this project, with the real numbers.

Not a statistics course. It is the set of ideas you need to (a) follow why we
did what we did, (b) catch it when a method is being misapplied, and (c) push
back on me when I am wrong — which has happened repeatedly in this project and
will happen again.

**Read Part 1 and Part 5 if you read nothing else.** Part 1 is the conceptual
core; Part 5 is how to catch errors, including mine.

---

# Part 1 — The five ideas that do most of the work

## 1.1 Recombination breaks the assumption a phylogenetic tree is built on

A phylogenetic tree assumes **vertical inheritance**: differences between two
genomes accumulated as mutations since their common ancestor. That's what lets
you read a tree as a history, and it's what lets branch length mean "time" or
"evolutionary distance."

Homologous recombination violates this. A bacterium swaps a chunk of chromosome
with a relative. The swapped chunk arrives carrying *someone else's* mutations,
all at once. Two genomes can now look distant because of one import event that
happened yesterday, not because they diverged long ago.

**Concretely, in our data:** the Colombian genome and the Mississippi genomes
differ by ~1,130 SNPs raw. Strip out the imported tracts and it's ~490. **Over
half the apparent divergence arrived in chunks, not by descent.** Across our
whole collection the median is worse — roughly 90% of pairwise differences are
imported rather than inherited.

**Why this drives everything else:** if you don't remove recombination, your
tree is partly a map of who-swapped-with-whom rather than who-descends-from-whom.
Branch lengths are inflated, topology can be actively wrong, and any molecular
clock is meaningless. That is why the whole pipeline exists: find the imported
tracts, mask them, rebuild the tree on the remainder (the "clonal frame").

**The question to ask about any distance number:** *is that raw or
recombination-filtered?* If someone can't tell you, the number means very little.

## 1.2 Ratios behave; cumulative counts lie

This is the single most transferable statistical idea in the project, and it is
not obvious.

Some statistics **accumulate as you add samples**, and some don't.

**Union coverage** — "what fraction of the genome has been recombinant on at
least one branch?" — sounds like a property of the population. It isn't. More
genomes means more branches means more chances for any given site to be flagged
*somewhere*. It only ever goes up. In our data, log(unit size) vs union coverage
correlates at **+0.81** — it is mostly measuring how many genomes you had.

**r/m** — SNPs inside recombinant tracts ÷ SNPs outside — is a **ratio**. Both
numerator and denominator grow together, so it doesn't systematically inflate
with sample size. Correlation with log(size) is +0.37, much weaker.

The clean demonstration from our own data — two units:

| unit | n | union coverage | r/m |
|---|---|---|---|
| A | 49 | 18.0% | 1.25 |
| B | **7** | **17.9%** | **9.11** |

Identical union coverage. Unit A is a genuine detection failure; unit B is one of
the healthiest we measured. **Any threshold on union coverage treats these
identically and would be wrong.**

**The general lesson:** before you threshold *any* statistic, ask whether it
grows with sample size. If it does, you're partly thresholding on how much data
you happened to have.

## 1.3 Confounding — the thing that looks like your answer but isn't

This is the most important idea in the geographic part of the project.

Suppose genomes from Brazil cluster together on the tree. Tempting conclusion:
Brazilian isolates are genetically related, so there's a Brazilian lineage.

But **who sequenced them?** If all the Brazilian genomes came from one study, in
one lab, from one hospital, in one year — then "clusters by country" and
"clusters by study" are the same observation. You cannot tell whether you're
seeing biology or seeing a sampling artifact.

**Two variables are confounded when they vary together, so an effect
attributable to one is equally attributable to the other.** No amount of
statistical cleverness separates them after the fact. You need data where they
*don't* move together.

**What we did about it:** for every unit, we ran the identical clustering test
twice — once on country, once on BioProject (a proxy for "which study"). Then:

- Country clusters, BioProject doesn't → **geographic signal is real**
- Both cluster equally → **confounded**, uninterpretable
- BioProject data too sparse to test → **vacuous control**, unknown

Result across the reported **85 units**: **6 genuinely geographic, 12
confounded**, 5 vacuous, 25 null, 37 untestable. So when someone shows you a map
that agrees with a phylogeny, the relevant number is 6, not 85.

*(Corrected 2026-08-26. This previously read "across 88 units: 6, 13, 5, 25, 39",
which is the A100 control partition rather than the reported one. The pass count,
6, is the same on both.)*

**One refinement, because "confounded" is doing more work than it should.** In
this panel 95% of BioProjects are entirely single-country, so a real within-country
clonal expansion deposited by one study makes *both* variables fire on the same
clade, and "confounded" is the automatic verdict whether or not anything
artefactual is present. Asking the study-effect question directly, holding country
fixed, splits the discarded units into **8 with batch structure at nominal p (only
2 surviving FDR), 4 with none at all, and 2 untestable**. So batch structure is
real in aggregate but confirmed in only two units. "Confounded" honestly means
*we cannot separate these two explanations here*, which is weaker than *this is an
artefact* and stronger than *this is geography*.

**The question to ask about any geographic claim:** *did you check whether the
same pattern is explained by who did the sequencing?* Based on my searches,
almost nobody in this literature does. That's why it's one of our contributions.

## 1.4 Circularity — grading your own homework

We have 46 genomes where we *know* the true country of exposure (travel
histories), from 45 patients. Perfect for testing whether our method can predict origin.

Except those genomes are **in the reference panel**. So when we ask "can we
attribute this Philippine genome?", the method's nearest neighbours include the
*other* Philippine validation genomes. It's predicting Philippines because we
told it those are Philippine. That is circular.

**Two ways to hold data out, answering different questions:**

- **Leave-one-out** — remove just the target genome. Asks: *given that reference
  genomes for this country exist, can we attribute?*
- **Leave-group-out** — remove every validation genome from that country. Asks:
  *can we attribute to a country with no reference representation?*

**What it did to our numbers, on the 26-genome SNP analysis where we first caught
it:** nearest-neighbour country attribution scored **37%** under leave-one-out.
Under leave-group-out it scored **0%**. All seven apparent successes were
validation genomes predicting each other.

**If we had published the 37%, it would have been entirely artifact.** Not
optimistic, artifact.

The effect did not go away when the set grew. On the current cgMLST basis, with
46 scorable genomes and every figure computed under leave-group-out, country
attribution is **10 of 46 (22%)** against a **26% majority baseline**, that is,
still not above chance. The holdout is now stricter again: it removes not only
every validation genome from the target's country but the target's whole outbreak
group, because same-country was not sufficient once we found that outbreak
siblings leak across country labels.

**The question to ask about any accuracy figure:** *what exactly was held out,
and could the answer have leaked in through a back door?*

## 1.5 A number without a baseline is not a result

We can predict world region with 89% accuracy. Impressive?

Our collection is **91.8% East Asia & Pacific**. A method that ignores the genome
entirely and always answers "East Asia & Pacific" scores **46%** on our validation
set. So the honest framing is **41/46 = 89% against a 46% floor**, κ 0.832: real
signal, but roughly half the apparent performance is free.

The same discipline flatters and then deflates the binary version. Asia versus
elsewhere scores **46/46, a perfect 100%**, but on a set that is overwhelmingly
Asian to begin with, which is why the 7-way region split is the honest operating
point rather than the binary one.

*(Updated 2026-08-26. This section previously quoted "100% against a 58% floor",
which was the older and much smaller validation set.)*

This is the **majority-class baseline** (sometimes "no-information rate"). Any
classification accuracy must be reported next to it.

**The question to ask:** *what would a stupid method score on this same test?*

---

# Part 2 — The statistics, in the order they show up in our outputs

## 2.1 Correlation: Pearson vs Spearman, and what rho means

**Pearson r** measures how well a *straight line* fits the raw values. Sensitive
to outliers and to skew — one extreme point can create or destroy it.

**Spearman rho** converts everything to ranks first (1st, 2nd, 3rd…) and
measures whether they move together in order. Immune to outliers and to
non-linear-but-consistent relationships.

**Why we mostly use Spearman for r/m comparisons:** r/m values are skewed with
long tails (0.04 to 12.9 in one comparison). Pearson would be dominated by the
extremes; Spearman asks the question we actually care about — *do the two tools
rank units in the same order?*

Rough reading of magnitude, for biological data:

| \|rho\| | reading |
|---|---|
| 0.0–0.2 | no useful relationship |
| 0.2–0.4 | weak; real only with decent n |
| 0.4–0.6 | moderate; a genuine tendency, poor prediction |
| 0.6–0.8 | strong |
| 0.8–1.0 | very strong |

Sign matters as much as magnitude. **+** means they rise together, **−** means
one rises as the other falls.

**Real examples from this project:**

- Gubbins r/m vs ClonalFrameML r/m: **rho +0.59**. Moderate. The two tools
  broadly agree on ordering but are not interchangeable — which is exactly the
  finding.
- cgMLST allelic distance vs our filtered SNP distance: **median r +0.85** per
  unit. Strong. Two independent methods measuring the same thing.
- ν vs Gubbins r/m: **rho −0.42**. Moderate, and *negative* — the opposite of
  what we predicted. That refuted a hypothesis.

## 2.2 The trap that killed our ν hypothesis: shared terms and confounded predictors

Worth its own section because it's subtle and I fell into it.

We predicted: units where imported DNA is very similar to the recipient (low
**ν**) should look like detection failures, because imports carrying few SNPs
don't register as "unusually dense."

Two things went wrong.

**First, a shared-term problem.** ClonalFrameML computes r/m as
(R/θ) × δ × ν. So ν is *inside* the thing we wanted to correlate it against.
Testing ν against a ratio containing ν guarantees a relationship that's
arithmetic, not biology. The fix: test ν against **Gubbins'** r/m instead —
Gubbins never sees ν, so any relationship there is real.

**Second, and worse: ν and δ (tract length) are anti-correlated at rho −0.86.**
ClonalFrameML trades them off when fitting the model — a unit fitted with long
tracts gets low per-site divergence, and vice versa. Both describe the same
amount of imported sequence.

**Consequence: ν is not independently interpretable.** Any apparent ν effect is
mostly δ in disguise. When I first looked at two units and saw low ν with big
disagreement, I was actually looking at long δ. With 81 units, δ turned out to be
the real correlate (+0.55, correctly signed) and ν's apparent effect reversed.

**The generalisable lesson:** when two predictors are strongly correlated with
each other, you cannot attribute an effect to one of them from a simple
correlation. This is *collinearity*, and it's the same reason you can't tell
whether it's the smoking or the drinking without data where they come apart.

**The question to ask:** *is your predictor correlated with something else that
could explain this just as well?*

## 2.3 p-values: what they do and don't mean

A p-value answers exactly one question: **if there were no real effect, how
often would I see a pattern this strong by chance?**

p = 0.001 means: one time in a thousand. p = 0.20 means: one time in five, which
is often enough that you've learned nothing.

**What it does *not* mean:**
- It is not the probability the hypothesis is true
- It is not a measure of effect size — a tiny, useless effect gets a tiny p-value
  with enough samples
- p > 0.05 is not proof of no effect; it may just mean too few samples

**Practically:** always read the p-value next to the *n* and the effect size. Our
"rho −0.42, p = 0.007, n = 41" is worth more than a p-value alone, because you
can see the relationship is moderate and the sample is reasonable.

## 2.4 Permutation tests — how our geographic test actually works

Most statistical tests assume your data follows some standard distribution.
Phylogenies don't. So we build the null distribution empirically instead.

Our test, step by step:

1. Take the real tree and the real country labels. Count the minimum number of
   country "changes" needed to explain the labels on that tree (a **parsimony
   score**). Fewer changes = more geographically clustered.
2. Now **shuffle the labels randomly among the tips**, keeping the tree fixed and
   keeping the same *number* of each country. Score again.
3. Do that 1,000 times. You now have 1,000 scores from trees where geography is
   random by construction.
4. p = the fraction of shuffles that scored as well as or better than reality.

**Why shuffling matters so much here:** it holds composition fixed. A unit that's
90% Thai is compared against *other 90%-Thai arrangements* — not against some
imaginary evenly-sampled world. Given that our sampling varies 35,000-fold
between countries, that's the only defensible comparison.

**Where the floor comes from:** with 1,000 shuffles, the smallest possible
p-value is 1/1001 ≈ 0.001. That's why so many of our results read exactly
`0.0010` — it means "better than all 1,000 shuffles," not "p equals precisely
0.001."

## 2.5 Multiple testing and FDR

Test one thing at p < 0.05 and you accept a 1-in-20 false-positive risk. Test 49
things and you should *expect* about 2.5 false positives even if nothing is real.

**Benjamini–Hochberg FDR** controls the expected *proportion* of your
"significant" findings that are false. At 5% FDR, roughly 5% of the things you
call significant are expected to be wrong.

It works by sorting p-values and requiring smaller ones from the more marginal
results. In our data, 26 units passed raw p ≤ 0.05 but only **24 survived FDR**.

**A subtlety worth knowing:** the size of the correction depends on how many
tests you count as a family. We correct within one geographic scale, treating
country tests as the hypotheses and BioProject tests as controls rather than
hypotheses. Folding the controls in would dilute the very comparison they exist
to make. Choices like that are judgement calls and should be stated explicitly —
not buried.

## 2.6 Regression coefficients, briefly

We ran: log(Gubbins r/m) ~ log(R/θ) + log(δ) + log(ν).

A regression asks: *holding the others constant, how much does the outcome move
when this predictor moves?* The coefficients came out near **+0.5** each, with
**R² ≈ 0.35**.

- If Gubbins simply measured (R/θ) × δ × ν, every coefficient would be ~+1.0.
  They're ~0.5, so Gubbins recovers only about half the log-scale effect of each
  component.
- **R² = 0.35** means the three predictors together explain 35% of the variance —
  two thirds is unexplained. That's a substantial admission and worth carrying
  into the write-up rather than hiding.

Note the caveat from §2.2: because ν and δ are collinear, individual coefficients
in this model are unstable. The overall R² is more trustworthy than any single
coefficient.

---

# Part 3 — The bioinformatics, conceptually

## 3.1 The pipeline, in one pass

```
assemblies → pick a reference → align everything to it
   → find variant sites → detect & mask recombinant tracts
   → build tree on what's left → measure
```

**Assembly** — reads stitched into contigs. Not the true chromosome; a
reconstruction with errors and gaps.

**Alignment to a reference** — line every genome up against one chosen genome so
"position 1,439" means the same thing in all of them. Everything downstream
depends on this shared coordinate system.

**Variant sites** — positions where genomes differ. The interesting 0.1%.

**Recombination detection** — find windows with implausibly dense SNPs and flag
them as imports. This is Gubbins' whole idea.

**Tree building** — maximum likelihood, on the non-recombinant remainder.

## 3.2 Reference bias — why the choice of reference matters

You align everything to one genome. Anything absent from that reference is
invisible; anything very divergent aligns poorly. So **your choice of reference
shapes what you can see**, and lineages far from it lose callable genome.

Our pipeline picks a *close* reference per unit to reduce this. The cost is that
each unit ends up measured in a slightly different coordinate system, which is
part of why merging per-unit trees is hard. That tradeoff is real and there's no
free answer — the honest move is to state which one you took.

## 3.3 Constant sites — a subtle trap worth understanding

You build the tree from variant sites only, for speed. But branch lengths are
supposed to be "substitutions per site" — and if you only show the tree the
variable sites, it thinks *every* site varies, and inflates every branch.

The fix: tell the tree-builder how many invariant A, C, G, T sites existed in the
full alignment. Get this wrong — pass zeros — and the branch lengths are wrong by
a large factor, **with no error message.** Our pipeline explicitly refuses an
all-zero vector for this reason.

This is a good example of a class of bioinformatics bug: **silent, plausible-
looking, and only detectable if you know to check.**

## 3.4 Clustering, and why we partition before analysing

Recombination-detection tools assume limited diversity within the sample. Across
a whole species, mutation density and import density become indistinguishable and
detection degrades. Runtime is also quadratic in sample count.

So: split the collection into strain-like **units** first, then correct each
independently. In many species this also matches biology — bacteria exchange DNA
readily within a lineage and rarely between lineages.

**Terminology, because these get conflated constantly:**

| term | what it means | our scale |
|---|---|---|
| **unit / cluster** | a group we analyse together | 85 units, n=7 to 159 |
| **ST (sequence type)** | 7-gene type; the field's shared vocabulary | 514 in our panel |
| **cgMLST profile** | ~4,000-gene allele profile | 4,089 loci |
| **clonal cluster** | genomes so close they're plausibly one transmission chain | our Mississippi 21, ≤20 SNPs |

They are *not* interchangeable. Our ST92 spans **four different units and seven
countries** — the same ST, genomically distinct groups. That's called ST
homoplasy, and it's why 7-gene typing can't do fine-scale work.

---

# Part 4 — The specific numbers you'll be asked about

| number | what it is | what it means |
|---|---|---|
| **85 units** | analysis groups | 2,340 genomes analysed of 2,959 |
| **~90%** | share of pairwise differences from recombination | why raw SNP distances mislead |
| **6 of 85** | units with real geographic signal after control | the honest count for any map claim |
| **12 of 85** | units not separable from study | geography inseparable from who sequenced; only 2 have FDR-confirmed batch structure |
| **10 / 46 (22%)** | country attribution, cgMLST, vs a 26% baseline | still not above chance; earlier runs on smaller sets scored 0 across a 584-fold resolution range |
| **46%** | majority-class baseline at region scale | the floor any region accuracy must beat (was 58% on the older, smaller set) |
| **41 / 46 (89%)** | region attribution, cgMLST modal k=20, κ 0.832 | works *where the panel has references* |
| **median 7 SNPs** | within the Mississippi cluster | tight enough for an operational rule |
| **~490 vs ~1,130** | Colombia–Mississippi, filtered vs raw | over half was imported |
| **rho +0.59** | Gubbins vs ClonalFrameML r/m ranking | moderate; tools not interchangeable |
| **rho −0.86** | ν vs δ | why ν can't be read alone |
| **46** | genomes with known exposure country, from **45 patients** | the entire validation set, still small |

**The most important limitation to be able to state out loud:** our conclusions
about attribution rest on **46 scorable genomes from 45 patients, spread across
16 source countries, most with one or two genomes each, and with the Philippines
alone contributing 12.** The regional
result is consistent and survives the strict test, but "well-supported" is the
right phrase, not "established."

---

# Part 5 — Being a responsible AI user: how to catch me

You asked how to be a better AI user. The honest answer is that I make confident,
fluent errors, and fluency is not accuracy. Here are **real mistakes I made in
this project**, what caused them, and the question that would have caught each.

### Mistake 1 — I gave you a confident result from two data points

Mid-run I reported that low ν tracked with tool disagreement, "exactly as the
hypothesis predicted." I had **two units.** With 81 units the relationship
reversed sign and the hypothesis was refuted.

→ **Ask: "how many data points is that based on?"** Anything under ~20 in
biology is a hint, not a result. I should have said so unprompted.

### Mistake 2 — I diagnosed from pattern-matching instead of testing

I told you the Mississippi unit's low r/m looked like a "bridged unit" whose
remedy is to split it. The pattern fit. When we actually re-ran it, splitting
made every statistic **worse** — it was the opposite diagnosis (under-detection
at low diversity).

→ **Ask: "did you test that, or infer it from a pattern?"** A pattern that fits a
catalogue entry is a hypothesis, not a finding.

### Mistake 3 — I treated an old note as current fact

A memory note said a contaminated sample was inside the running Mississippi unit.
I repeated it. It was about the **previous** pipeline version; the current one
had already excluded it. That nearly cost an unnecessary A100 re-run.

→ **Ask: "is that still true, and which version is it about?"** Anything I recall
from earlier work needs re-verifying against current files.

### Mistake 4 — I overstated a problem's severity

I called a metadata inconsistency a "label collision" affecting published
results. On checking, the analysis script never read that column — the published
results were fine. The problem was real but narrower than I first said.

→ **Ask: "what specifically breaks, and has it actually affected anything?"**

### Mistake 5 — I nearly deleted something I'd verified only shallowly

I checked that a 21 GB directory was a duplicate by comparing file sizes. It
looked disposable. On closer inspection, 6 files existed nowhere else and 86
reference paths pointed into it.

→ **Ask: "how exactly did you verify that?"** "Sizes match" is much weaker than
"byte counts match and I checked what references it."

### The general questions worth asking me, always

1. **"How many samples is that based on?"**
2. **"Did you measure that or infer it?"**
3. **"What's the baseline / what would a naive method get?"**
4. **"What was held out, and could the answer have leaked in?"**
5. **"Is there something else that would explain this equally well?"**
6. **"How did you verify that?"**
7. **"What would change your mind?"**
8. **"What's the weakest part of this?"** — I will usually tell you honestly, but
   often only if asked.

### The pattern behind all five mistakes

Every one was me being **fluent about something under-verified**. Not fabrication
— plausible reasoning that happened to be wrong, delivered in the same confident
register as the things that were right. **You cannot tell my correct claims from
my incorrect ones by tone.** The only reliable filter is whether a claim is
attached to a measurement you could check.

So the highest-value habit: when I state something that matters, ask what it
would take to check it — and prefer conclusions with a file, a count, or a test
behind them.

---

## What this primer does not cover

- Model selection in ML tree-building (GTR+F+I and friends)
- Bayesian methods and molecular dating — deliberately ruled out for this
  collection, since our data fails the clock-signal test
- Pangenome and accessory-genome methods, beyond the note that they may attribute
  geography where the core genome cannot
- Anything organism-specific

For any of these, or for a real statistical review before submission, a
statistician looking at the actual numbers is worth more than any amount of
primer.
