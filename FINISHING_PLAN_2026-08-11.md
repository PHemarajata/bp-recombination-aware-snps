# Plan to finish — assessed against the Fable critique

---

> # ✅ DELIVERABLE A COMMITTED — TIER 0 COMPLETE, TIER 1.2 COMPLETE (2026-08-11)
>
> **Tier 0 (all five items) is done**, and **Tier 1.2 — the item flagged as the
> one that could force a re-run — is done and came back negative.**
>
> | item | status | outcome |
> |---|---|---|
> | 0.1 drop the UFBoot gate | ✅ | Coverage restored to **33.3% (30 units, 933 genomes)**. Gate removed from `triage_analysable_bp.py`; `collapse_unsupported_bp.py` added; 180 trees collapsed. |
> | 0.2 rewrite §9.1 | ✅ | Incommensurable-units claim withdrawn in all four documents; replaced with differing-denominators + independent-correction. |
> | 0.3 partial correlation | ✅ | Reproduced on 45 units with p-values. A.11r survives (+0.837); diversity's independent effect **+0.482, p = 0.0009**, was understated. |
> | 0.4 reference borrowing | ✅ | **Upgraded from n=1 to n=33.** Classes indistinguishable, but a **dose–response on borrow distance** exists (r/m r = −0.38, p = 0.028) *inside* the bound. Bound restated as an assumption. |
> | 0.5 revise Appendix B | ✅ | Falsification target stated per step; new §B.3a (attack-the-result prompt with cost clause). |
> | **1.2 MGE / hotspot audit** | ✅ | **THE ALARM IS REFUTED — see below.** |
> | 1.4 callable-fraction variance | ✅ | Not supported (r = −0.18, p = 0.23); sixth candidate excluded. |
> | 1.5 capture convergence | ✅ | Wired into the runner for future runs; 4 new self-tests. |
> | **1.3 ClonalFrameML / ν** | ✅ | **THE ν HYPOTHESIS IS REFUTED (ratio 1.00). See below.** |
>
> ### Tier 1.2 refutes §1.4 of this plan, and §1.4 should be read as superseded
>
> §1.4 below concluded the shared-bin signal was "VALIDATED, and it is
> actionable". **It is neither.** The finding had no null and used a statistic
> that is not comparable across group sizes.
>
> - Each unit *individually* flags **35–97%** of 10-kb bins as recombinant. At
>   those marginal rates, "54 bins recombinant in all 8 units" and "only 1 bin
>   lineage-specific" are **arithmetic**, not signal.
> - Against an independence null, enrichment is **1.1×** — near chance.
> - "Recombinant in ≥80% of units" means ≥7 of 8 in one group but **all 4** of 4
>   in another, so the 46%-vs-3% contrast compared two different questions.
> - The lineage control §1.4 asked for **was already on disk**: two of four
>   reference groups are cross-lineage (one spans seven lineages). Cross-lineage
>   enrichment is **1.1×**, indistinguishable from same-lineage.
>
> **No masked re-run is indicated.** Stated conservatively: enrichment rises at
> finer bins (1.4× at 500 bp) and is higher in same-lineage groups, so this
> **bounds** a fixed-coordinate artefact at a small factor rather than excluding
> one. MGE masking stays worth doing; it is no longer a correction to results
> already reported.
>
> **The meta-lesson, and it is §5.1's lesson again:** "only 1 bin in 403 is
> lineage-specific" is a cumulative statistic dressed as a rate. We made the same
> class of error twice, four days apart.
>
> **Durable record:** `REVISED_STRATEGY_2026-08.md` **A.11y** (gate withdrawal +
> partials) and **A.11z** (hotspot audit). Reproduce with `tier0_evidence_bp.py`
> and `mge_hotspot_audit_bp.py`.
>
 ### Also done: Tier 1.4 and Tier 1.5
>
> **1.4 — callable-fraction variance does NOT explain the r/m residue (A.11aa).**
> sd of per-genome callable fraction vs pooled r/m: **−0.183, p = 0.23**
> (−0.188 controlling size and diversity). The three named §9.4 units have
> **lower** variance than the rest (0.0033 vs 0.0047); the hypothesis predicts
> higher. **Sixth candidate excluded**; the residue stands.
>
> **Two incidental results from that run matter more than the test:**
> - **r(log n, pooled r/m) = +0.024 (p = 0.88)** over 45 units, against +0.373 on
>   19. r/m is essentially size-independent — which **strengthens** making it the
>   sole gate, since the two screens we withdrew both tracked size or convention.
> - **r(diversity, pooled r/m) = −0.470 (p = 0.0011)**. A.11l proposed this
>   gradient and withdrew it on four points; over 45 it is solid. **But this
>   reinstates the phenomenon, not the interpretation** — a smooth decline is
>   exactly what makes a threshold arbitrary, so **r/m ≥ 3.0 is a point on a
>   continuum**, not a boundary between regimes. Anything resting on a clean
>   in-range/above-ceiling dichotomy needs re-reading.
>
> **1.5 — convergence capture is wired in.** Gubbins stdout now goes to
> `gubbins.progress.log` with a `gubbins.convergence.txt` extract, per arm, and
> the redirect propagates a non-zero exit rather than swallowing it. Four new
> self-tests in `reference_sensitivity_bp.py` (now 60, all passing). **Applies to
> future runs only** — it cannot be recovered retrospectively.
>
 ### Tier 1.3 — ClonalFrameML installed and run; the ν hypothesis is REFUTED
>
> ClonalFrameML 1.20 in conda env `cfml`; 12 runs (6 units × 2 replicons), all
> exit 0. Suspects vs **diversity-matched** healthy controls (matching was
> required — r/m declines with diversity, A.11aa). Starting trees rebuilt
> **uncorrected**, since every tree on disk is post-Gubbins.
>
> | | suspects | controls | ratio |
> |---|---|---|---|
> | R/θ | 1.203 / 1.123 | 1.310 / 1.257 | 0.92 / 0.89 |
> | δ | 5,063 / 4,981 | 6,329 / 6,274 | 0.80 / 0.79 |
> | **ν** | **0.00211 / 0.00222** | **0.00210 / 0.00222** | **1.00 / 1.00** |
>
> **§1.5 of this plan called low ν "the single most publishable thing to come out
> of the critique". It is not there.** Both replicons independently give ν ratio
> **1.00**, and the decomposition is decisive: ν varies **more between replicons
> within a unit** (+6.7% to +13.3%) **than between units within a replicon**
> (≤8%). It is a constant of the organism, and an ≤8% spread cannot explain a
> **4.5×** spread in Gubbins r/m. R/θ and δ do not explain it either.
> **Seventh candidate excluded; the §9.4 residue stands.**
>
> ### The one thing that now outranks Tier 2
>
> ClonalFrameML does not reproduce Gubbins' **ordering**: Gubbins' lowest-r/m
> unit (`s3_L1_10`, 2.03) is CFML's second-highest (16.31). Spearman **+0.31**;
> CFML/Gubbins ratio median 4.3× (1.7–8.0×). Since pooled r/m is now the **sole**
> acceptance gate, a real ordering disagreement would mean the gate is
> tool-dependent.
>
> **This is a flag, not a finding** — n = 6 has almost no power; the two are not
> the same estimator (which explains the offset but not a reordering); and
> bridged structure is a competing explanation.
>
> **→ Run ClonalFrameML across all 45 units and correlate against Gubbins r/m.**
> Hours of compute, tooling already written, and it tests the criterion that
> every remaining conclusion rests on. **Do this before the Tier 2 overnight
> run** — if the gate is tool-dependent, Tier 2 would be calibrating a null
> against a criterion that is itself unsettled.
>
> **Still open in Tier 1:** 1.1 (mask-aware constant sites — tooling present, a
> few hours of compute).
>
> ### PARTITION COMPLETED AND COVERAGE CORRECTED (A.11ac)
>
> fastbaps now run on **all 42 strains** (196 jobs, 0 errors), closing gating item
> N1. The 28 previously-skipped strains yielded 100 sub-clusters but **median size
> 2, 61% singletons/pairs**, and only **1** unit both in range and unimodal.
>
> **The 9 PopPUNK-strain units are withdrawn** — their apparent diversity was
> mixture structure, not divergence. **`s13_L1_1` (n=31) recovered and passes:
> pooled r/m 12.89 vs `strain_13`'s 2.89 — a 4.5× lift from removing 5 genomes.**
>
> **Coverage: 30.4%** (26 units / 853 genomes) of 2,802, or **35.1%** of the 2,430
> eligible. 372 genomes were never partitionable and must not be counted as
> failures.

---

**Inputs:** `RECOMBINATION_AWARE_PHYLOGENOMICS_HANDOFF.md` (ours),
`RECOMBINATION_HANDOFF_CRITIQUE_AND_REDESIGN.md` (Fable), the 45 completed
production runs, and four verification tests run today (below).

**Bottom line.** The critique is largely correct and three of its points are
consequential enough to change what we report. But its headline recommendation —
re-architect around a single collection-wide alignment — is the *most* expensive
item on the list and the *least* likely to change any scientific conclusion.
**Do not start over. Do four cheap things, one overnight thing, then stop.**

---

## Part 1 — Verdict on the critique, tested rather than argued

I checked four claims against the data and the install rather than accepting or
rejecting them on argument.

### 1.1 CONCEDED, and it is the biggest one: bootstrap gating is indefensible

Fable is right that IQ-TREE's ultrafast bootstrap is not on the standard
nonparametric scale (UFBoot ≥95 ≈ SBS ≥70). We applied **UFBoot ≥70**, which is
*far more permissive* than the convention we cited, not more conservative.

Measured consequence:

| threshold | units | genomes | coverage |
|---|---|---|---|
| detection only, no bootstrap gate | 30 | 933 | **33.3%** |
| median UFBoot ≥ 70 (what we adopted) | 22 | 708 | 25.3% |
| median UFBoot ≥ 80 | 17 | 632 | 22.6% |
| median UFBoot ≥ 90 | 10 | 437 | 15.6% |
| median UFBoot ≥ 95 (the actual convention) | **7** | **176** | **6.3%** |

**A headline number that moves from 25.3% to 6.3% on a convention choice is not
a result.** This settles the argument in favour of Fable's §1.6: stop gating on
support, collapse unsupported nodes into polytomies, and carry the uncertainty
forward. **ACTION: drop the UFBoot gate. Coverage returns to 33.3% (30 units,
933 genomes), and tree uncertainty is represented rather than thresholded.**

### 1.2 CONCEDED: §9.1 overstated the merge problem

Fable caught a real internal contradiction. If T6/T7 are followed — true
constant-site counts supplied to the tree builder — branch lengths are already in
substitutions per site of the *full* alignment, not per variable site. The
"incommensurable units" claim was inherited from the pipeline's earlier
configuration and should not have survived into a document that also prescribes
T6/T7.

What actually differs between units is the **denominator** (each unit aligned to
a different reference, so "core site" denotes a different position set). That is
real but much smaller than "unsolved research problem". §9.1 needs rewriting.

### 1.3 RAISED CORRECTLY, but the conclusion survives: the size confound is real

Fable asked for a partial correlation before accepting that size drives union
coverage. Run today:

| | r |
|---|---|
| marginal r(log n, union) | +0.800 |
| marginal r(diversity, union) | +0.281 |
| **r(log n, diversity)** — the putative confounder | **−0.010** |
| **partial r(log n, union \| diversity)** | **+0.837** |
| **partial r(diversity, union \| log n)** | **+0.482** |

Size and diversity are **uncorrelated** in this collection (−0.010), so there was
no confound to control for; the size effect *strengthens* to +0.837 when
diversity is held constant. **A.11r survives.** But the partial also shows
diversity has a genuine independent effect (+0.482) that the marginal +0.281
understated — worth adding, and we would not have seen it without running the
test Fable asked for.

### 1.4 VALIDATED, and it is actionable: the missing MGE mask leaves a large signature

Fable's §1.7 flags the absence of prophage/IS/ICE/rRNA masking. Tested by asking
whether recombination tracts pile up at the *same reference coordinates* across
units that were analysed independently. Eight units share one reference:

| 10-kb bins | count |
|---|---|
| recombinant in **all 8** units | **54** |
| recombinant in ≥80% of units | **185** (46% of all recombinant bins) |
| recombinant in exactly **one** unit | **1** |
| total bins with any recombination | 403 |

**Only one bin in 403 is lineage-specific.** If recombination were independent
per lineage this distribution would be far flatter. Something is generating
tracts at fixed coordinates — mobile elements, repeats, or mapping artefact.

**Caveat, stated because it matters:** seven of the eight units are sub-clusters
of the same lineage, so shared *ancestral* recombination is a competing
explanation. The test needs repeating across units from different lineages
sharing a reference before the artefact reading is secure. But the near-total
absence of lineage-specific signal is hard to explain by inheritance alone, and
the fix (mask MGEs before correction) is cheap and standard either way.

### 1.5 BLOCKED retrospectively: convergence was not captured

Fable's best free-diagnostic suggestion — record iterations-to-convergence, since
a unit that hit the cap has untrustworthy r/m by construction — cannot be
recovered from our runs. Gubbins' progress output went to stdout and was drowned
by IQ-TREE's. `gubbins.log` is a citation manifest, not a progress log.
**ACTION: capture it on every future run** (separate the streams); it costs
nothing and is a live candidate explanation for the §9.4 residue.

### 1.6 AVAILABLE: the tooling claims check out

- `mask_gubbins_aln.py` and `generate_files_for_clade_analysis.py` **are
  installed** in our environment. The §2 "unavoidable limitation" on constant-site
  counts is therefore fixable as Fable describes — count twice (conservative:
  exclude sites masked on ≥1 branch; permissive: exclude none) and show branch
  lengths are insensitive.
- **ClonalFrameML is NOT installed** anywhere. Needed for the ν test (below).
- **SimBac and seq-gen are NOT installed.** Needed for the simulation arm.

### 1.7 Where I do NOT follow the critique

**Do not switch to contig mapping (critique §1.2).** Fable argues T1/T2/T8 are
artefacts of split-k-mer calling and recommends `snippy --ctgs`. The reasoning is
sound in the abstract, but we have direct measurement Fable did not have: on six
full 12-arm runs, the mapping caller added **~9,000 phantom positions** and
inflated root-to-tip slopes relative to the reference-free caller, which is
*why* the reference-free arm became the arbiter. Switching would reintroduce a
bias we measured and rejected. T1/T2/T8 are already solved and guarded. **Keep
the current caller; retain the mapping arm as the concordance check it already
is.**

**Treat "align once" as a Tier 3 option, not a prerequisite.** Fable is right
that it dissolves §3 and makes the merge a shared-denominator problem. But it
requires re-calling all 2,802 genomes and invalidates all 45 completed runs, and
— critically — **it changes no scientific conclusion we are currently able to
draw.** See Part 2.

---

## Part 2 — The strategic fork, which decides how much more work is justified

There are two possible deliverables here and they have very different
requirements. **Choose before doing more compute.**

### Deliverable A — a methods contribution

*"How to build and validate recombination-aware phylogenies in a recombining
bacterium, and the ways the standard acceptance statistics mislead."*

The evidence for this is **already collected**. Its core findings — cumulative
vs ratio statistics, the size confound with partial correlation, the
threshold-derivation failure modes, the failure-mode catalogue, the demonstration
that a coverage headline moves 4× on a bootstrap convention — are complete and
unusually well documented. Tier 0 and Tier 1 below finish it.

**No re-architecture required.** The merge is not needed, because the claim is
about method behaviour, not about the population.

### Deliverable B — a population-genetic or phylogeographic result

*"What this collection says about the population."*

This **does** need the redesign — and it is capped regardless by something no
re-architecture fixes. The collection is ~60% one country, with 81% of that
country's genomes from three studies. §9.5's point stands: effective sample size
is far below n, and discrete-trait or mugration analysis on the unweighted
collection measures sequencing effort, not biogeography.

**So the honest sequence for B is:** fix the sampling frame first (weighting,
per-study effective sample size, balanced subsampling), and only then decide
whether the merge is worth building. **Re-architecting to enable a
collection-wide tree, and then dating it on a collection that cannot support
dating, is effort spent in the wrong order.**

**Recommendation: commit to A now, and treat B as a separate project with the
sampling frame as its first task, not its last.**

---

## Part 3 — The plan

### Tier 0 — Corrections, today, zero compute

| # | action | why |
|---|---|---|
| 0.1 | **Drop the UFBoot gate.** Collapse branches below support into polytomies; keep the unit. Report **33.3% (30 units, 933 genomes)**. | The gate moves the headline 4× on a convention (1.1). Gating is not defensible; representing uncertainty is. |
| 0.2 | **Rewrite §9.1.** The units are commensurable under T6/T7; the residual problem is differing denominators. | Conceded internal contradiction (1.2). |
| 0.3 | **Add the partial correlation to A.11r**, including the independent diversity effect (+0.482). | Strengthens the finding and answers the critique (1.3). |
| 0.4 | **Fix the reference-borrowing inconsistency.** Either validate the bound on more units or restate it as an assumption, not a measurement. | §3 vs §6.1 (critique 2.1) — both cannot stand. |
| 0.5 | **Revise Appendix B** to Fable's version: state the falsification target — name the statistic, the threshold, and what observation would refute it. | Better advice than ours, and it is what actually produced §5 and §6. |

### Tier 1 — Cheap diagnostics on existing data (1–2 days, no re-runs)

| # | action | cost | what it decides |
|---|---|---|---|
| 1.1 | **Mask-aware constant sites.** Run `mask_gubbins_aln.py` on each accepted unit; recount constant sites conservatively and permissively; show branch lengths are insensitive. | hours | Converts a declared limitation into a two-line sensitivity check. |
| 1.2 | **MGE / hotspot audit.** Repeat today's shared-bin test across units from *different* lineages sharing a reference. Annotate the top shared bins (prophage, IS, rRNA, repeats). | hours | Decides whether the 46%-shared-bin signal is artefact or ancestry. **If artefact, it affects every r/m we report.** |
| 1.3 | **Install ClonalFrameML; run on the §9.4 units** (`s1_L1_19`, `s3_L1_10`, `s1_L1_13`) plus 3 healthy controls. Read off R/θ, δ, **ν** separately. | hours | Tests Fable's best hypothesis: is the unexplained r/m dip **low ν** — real recombination from donors too close to detect? If yes, the residue is biology, not failure. |
| 1.4 | **Callable-fraction variance vs r/m.** Regress per-unit r/m on the *variance* of per-genome non-N fraction. | ~1 hour | Fable's third §9.4 candidate. Cheap to exclude. |
| 1.5 | **Capture convergence on all future runs.** Separate Gubbins stdout from the tree builder's. | minutes | Free per-unit diagnostic we currently lack (1.5). |

### Tier 2 — The simulation calibration (one overnight run)

**This is the highest-value remaining action and it is feasible on this machine.**

Per unit: take its inferred tree, fitted model, alignment length, base
composition and **observed per-genome N pattern applied verbatim**; simulate
**zero-recombination** replicates (seq-gen/pyvolve) along that tree; run the
identical pipeline; record union coverage, r/m, tract length and support.

- **50–100 replicates × 30 units** at ~2 min per replicate ≈ 50–150 CPU-hours.
  At 16-way concurrency that is **4–9 hours — one overnight run.**
- Use `--threads 4 --reserve-cores 4` as before; the machine has frozen once, so
  do not saturate it.

**What it buys, in our own terms:**

| our open problem | resolved by the null |
|---|---|
| union coverage is size-confounded and unusable | thresholded against its own null at matched n → **usable again** |
| every threshold in §6 is a round number or a one-point bracket | replaced by **per-unit p-values** |
| the floor is not derivable (A.11x circularity) | floor = divergence at which observed r/m meets the null — **no admissible real units needed either side** |
| modality undecidable below n≈25 | null at n=7 gives the sparsity expectation directly |
| bootstrap threshold is convention-dependent (1.1) | null gives expected support at that n and θ |

**Add the power arm only if Tier 1.3 is inconclusive.** SimBac across a grid of
R/θ, δ and ν gives the detectability surface in ν — but if ClonalFrameML already
shows low ν in the anomalous units, the cheap test has answered the question and
the grid is unnecessary.

### Tier 3 — Only if a Tier 1–2 result demands it

- **Align once** (Fable §1.1). Justified *only* if you commit to Deliverable B
  and the merge becomes load-bearing. Cost: re-call 2,802 genomes, invalidate 45
  runs. Do not start this to fix a problem Tier 0–2 has already closed.
- **Re-partition into the operating range** (Fable §1.3). Attractive, but our own
  subdivision data shows clades can jump from too-divergent to too-tight with
  nothing in range between — one split produced a 95-genome clonal group at 140
  SNPs and a 45-genome unit at 1,487. Recursive cutting does not
  guarantee a unit lands in range, so the yield recovery Fable projects is an
  upper bound, not a forecast.

---

## Part 4 — Sequencing, and what "finished" means

**Week 1.** Tier 0 today (documentation only, no compute). Then Tier 1.1–1.4 in
parallel — they are independent and none needs the machine for long. Launch
Tier 2 as an overnight run at the end of the week.

**Week 2.** Read the null distributions. Re-express every acceptance threshold as
a per-unit p-value. Re-derive the floor as the divergence at which observed r/m
becomes indistinguishable from no-recombination. Rewrite the methods section
against p-values instead of round numbers.

**Then stop.** At that point the methods contribution is complete and defensible,
and every remaining open item is either (a) a known limitation stated honestly,
or (b) Deliverable B, which is a separate project.

### The three results that would change the plan

1. **Tier 1.2 shows the shared-bin signal is artefact, not ancestry.** Then MGEs
   are inflating r/m across every unit, the acceptance criteria have been reading
   artefact as health, and units must be re-run with masked input. **This is the
   one Tier 1 result that can force a re-run** — which is why it is worth doing
   first.
2. **Tier 1.3 shows low ν in the anomalous units.** Then §9.4's "unexplained
   residue" is explained, is real biology, and the failure-mode catalogue gains a
   sixth entry: *recombination present but undetectable because donors are too
   close*. This would be the single most publishable thing to come out of the
   critique.
3. **Tier 2's null shows our accepted units are indistinguishable from
   no-recombination.** Unlikely given r/m of 5–12, but it is the test that would
   invalidate the whole analysis, and it should be run precisely because it
   could.

### What "finished" looks like

- 30 units / 933 genomes (33.3%), no bootstrap gate, unsupported nodes collapsed
- every threshold expressed as a per-unit p-value against a matched null
- the r/m residue either explained by ν or bounded by the null
- MGE exposure measured, and masked if the audit says so
- constant-site sensitivity shown both ways
- the merge documented as out of scope for the claim being made, not as a failure

**Explicitly NOT in scope:** a collection-wide dated tree. The sampling frame
cannot support dating and the merge cannot support commensurable lengths. Saying
so plainly is a stronger paper than attempting either.

---

## Part 5 — What we owe the critique

Fable was right on the points that mattered most, and two of them we could not
have found ourselves without the prompt: the bootstrap-scale error (which moved
our headline 4×) and the ν decomposition (which is a live explanation for the one
thing we could not explain). The partial-correlation challenge was correct
practice even though our conclusion survived it, and the MGE gap is real and
measurable.

Where the critique is weaker is in cost-awareness: its central recommendation
requires discarding 45 completed runs and days of compute to fix problems that
Tier 0–2 close for a fraction of the effort, and one of its tooling
recommendations would reintroduce a bias we had already measured and rejected.

**That asymmetry is the lesson, not a complaint.** A critique that has not run
the pipeline will correctly identify design debt and systematically underestimate
what it costs to repay. Both halves need weighing, which is what Part 3 does.
