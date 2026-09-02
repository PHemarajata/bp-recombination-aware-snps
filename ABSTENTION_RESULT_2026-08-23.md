# The abstention rule — result

**Run 2026-08-23.** `abstention_rule_bp.py`, on `GROUPING_PREDICTIONS.tsv`
(leave-group-out **and** leave-outbreak-out, frozen basis, n=46).
Outputs: `ABSTENTION_CURVE.tsv` (198 operating points),
`ABSTENTION_OPERATING_POINTS.tsv` (54 rows). Both regenerate byte-identical.

> **Verdict.** The rule **works for region and fails for country**, and the
> failure is the more decisive of the two findings. For region it declines
> exactly the errors it was designed to catch — both Sub-Saharan African
> attractor calls — at a real but modest cost. For country the apparent gain is
> **entirely** explained by the retained subset having an easier class mix, and
> it disappears the moment that baseline is computed. Country cannot be rescued
> by abstaining.

---

## 1. What was tested

D3 proposed: above a nearest-neighbour distance threshold, return
*"unattributable — novel lineage"* rather than a region. Three candidate
confidence signals were scored, because "is anything near me" and "do the
things near me agree" are different questions:

| signal | question | direction |
|---|---|---|
| `nn_distance` | is anything near me at all | abstain **above** threshold |
| `vote_share` | how much of the 20-neighbourhood backs the call | abstain **below** |
| `margin` | how far does the winning label lead the runner-up | abstain **below** |

`vote_share` and `margin` are new columns on `GROUPING_PREDICTIONS.tsv`, added
by the same refactor. The refactor was verified to change **no prediction** —
`GROUPING_LADDER.tsv` is byte-identical before and after.

**No new pool-building code was written.** The analysis is a pure consumer of
`grouping_test_bp.py`'s output. Five scorers in this project each reimplemented
pool construction and four had to be repaired for the same leak; a sixth
implementation would have been a sixth chance to leak silently.

## 2. Two baselines, because one of them is load-bearing

A selective accuracy can rise for two very different reasons:

- **random-abstention baseline** — declining the same *number* of cases at
  random leaves the expected error rate untouched, so this baseline is just the
  answer-everything accuracy. It tests whether the *signal* carries information.
- **retained-subset majority baseline** — abstention changes the class mix, so
  the original majority baseline does not transfer. If selective accuracy merely
  tracks this, the rule has selected an **easier subset**, not a more reliable
  one.

The second one is what kills the country result. It was added specifically
because this project's standing rule is *never quote an accuracy without its
baseline and denominator* — and here the two baselines disagree.

## 3. Region — the rule works, honestly and modestly

Headline estimator (modal k=20), answer-everything **41/46 = 89.1%**.

| operating point | cov | sel. acc | random | **retained majority** | err avoided | correct lost |
|---|---|---|---|---|---|---|
| answer everything | 100% | 89.1% | — | 45.7% | 0 | 0 |
| **`nn_distance` ≤ 0.462** | **78.3%** | **94.4%** | 89.1% | **50.0%** | **3 of 5** | 7 |
| `vote_share` ≥ 0.80 | 65.2% | 93.3% | 89.1% | 60.0% | 3 of 5 | 13 |
| `margin` ≥ 0.75 | 50.0% | 100% | 89.1% | **78.3%** | 5 of 5 | 18 |

**Recommended operating point: `nn_distance` ≤ 0.462.** Out-of-sample by
leave-one-out threshold selection — the threshold is chosen on the other 45 and
applied to the held-out genome — it holds: **coverage 76.1%, selective accuracy
94.3%**, against 78.3% / 94.4% in-sample. That agreement is the point; a
threshold tuned and scored on the same 46 genomes would not be evidence.

⚠ **Do not oversell the accuracy gain.** Selective accuracy rises 89.1% → 94.4%,
but the retained majority baseline rises too, 45.7% → 50.0%. The lift over chance
therefore improves only **+43.4pp → +44.4pp**. **The value of this rule is in
error composition, not in a dramatic accuracy gain**, and the paper should say so
in those words.

⚠ **The `margin` ≥ 0.75 row is a trap.** 100% accuracy looks like the headline
and is not: it answers half the cases and the retained subset is **78.3% one
class**. Perfect accuracy on a nearly-single-class subset is close to vacuous.

### Which errors does it decline?

Ranking all 46 by abstainability (1 = most abstainable):

| genome | truth → predicted | `nn_distance` rank | declined at 0.462? |
|---|---|---|---|
| `SRR36223763` | East Asia & Pacific → South Asia | **2** | ✅ |
| `SRR35239810` | **Sub-Saharan Africa** → Latin America | **9** | ✅ |
| `SRR35174254` | **Sub-Saharan Africa** → Latin America | **10** | ✅ |
| `GCF_035776895_1_USA_Mississippi` | North America → Latin America | 26 | ❌ |
| `GCF_035776835_1_USA_Mississippi` | North America → Latin America | 27 | ❌ |

**This is the result, and the split is the interesting part.** The rule catches
**both Sub-Saharan African genomes** — the exact failure W2 identified, where a
genome with no real relative snaps to the Ecuadorian attractor and the catch-all
region label converts that into a confidently wrong answer. It also catches the
one East Asian error.

It **does not catch the two Mississippi genomes, and it cannot.** Those are the
depth-ceiling failure: they have genuine close relatives (ST92 is a real
pan-Americas lineage), high neighbourhood consensus, and are correct at the deep
splits and wrong only at the shallow one. No confidence signal based on "is
anything near me" can flag a case whose problem is that the near things are
*genuinely* near but *geographically uninformative*.

**Both failure modes are real and they are different. The abstention rule
addresses one of them. Say that, rather than presenting it as a general fix.**

## 4. Country — the rule fails its control

Headline estimator (nearest neighbour), answer-everything **10/46 = 21.7%**.

| operating point | cov | sel. acc | random | **retained majority** | verdict |
|---|---|---|---|---|---|
| answer everything | 100% | 21.7% | — | 26.1% | below baseline |
| `nn_distance` ≤ 0.642 | 93.5% | 23.3% | 21.7% | 25.6% | below baseline |
| `vote_share` ≥ 0.10 | 84.8% | 23.1% | 21.7% | 30.8% | below baseline |
| **`vote_share` ≥ 0.30** | **52.2%** | **37.5%** | 21.7% | **37.5%** | **exactly equal — no signal** |

The `vote_share` ≥ 0.30 row is the one that looks like a discovery: selective
accuracy 37.5% against an answer-everything 21.7%, a **+15.8pp** apparent lift,
and leave-one-out reproduces it exactly (52.2% / 37.5%).

**It is not a discovery.** The retained-subset majority baseline is **37.5%** —
*identical* to the selective accuracy. On the half of cases the rule chooses to
answer, always guessing the single most common exposure country scores exactly
as well as the genome does. The rule has found an easier subset, not a signal.

This is the same failure the accessory-genome experiment showed
(`ACCESSORY_ATTRIBUTION_RESULT`) and the same shape as the circular test in
`never-split-a-ratio-on-its-own-denominator`. **Country attribution is not
rescued by abstaining, and the paper should state that as a result** — it closes
the last obvious "but what if you just decline the hard ones" objection.

## 5. Positive control — the deep split

`asia_vs_not` under modal k=20 is already **46/46 = 100%**. Across all three
signals and every coverage target: selective accuracy stays 100%, **errors
avoided = 0**, and abstention buys nothing while costing up to 23 answers.

That is the correct behaviour and it is worth reporting: the rule does **not**
fire spuriously where the method already works. Combined with §3 and §4, the
three cases say the same thing the rest of the project says — **the method is
reliable at depth, unreliable at the shallow end, and abstention tracks that
boundary rather than creating it.**

## 6. What to put in the paper

1. **Report region with the rule as a secondary operating point, not the
   headline.** Headline stays 41/46 (89%). Add: *"declining the 22% of cases
   with no relative closer than 0.462 raises accuracy on the remainder to 94.4%
   (leave-one-out 94.3%) and removes both Sub-Saharan African
   misattributions."*
2. **State the honest limit in the same breath** — the retained majority
   baseline also rises, so the gain is in *which* errors remain, not in the
   lift over chance.
3. **Report the country failure as a result.** The +15.8pp lift that vanishes
   against its own retained baseline is a clean, quantified answer to the
   obvious objection.
4. **Name the two failure modes separately.** Attractor errors (catchable) and
   depth-ceiling errors (not catchable). The Mississippi pair is the worked
   example of the second, and it is the same genome pair that makes North
   America testable at all (`TRACK0_INTEGRATION_2026-08-23.md`).

## 7. Caveats

- **n=46, and 5 region errors.** Every statement in §3 rests on which of five
  genomes get declined. Leave-one-out removes *threshold*-selection
  circularity; it does **not** remove **signal**-selection circularity — three
  signals were compared on this same set, and `nn_distance` was chosen partly
  because it won. Treat the operating point as calibrated-on-46, and re-derive
  it if the validation set grows.
- **The threshold is not a species constant.** 0.462 is a cgMLST allelic
  distance under the Lichtenegger 4,221-locus scheme on this panel. It will not
  transfer to another scheme or a differently-shaped reference panel.
- **Coverage is not "no-answer rate" in the operational sense.** A declined case
  still gets the deep-split answer — `asia_vs_not` is 100% and never declines
  usefully. The deployable product is *"Asia or not: certain; region: only when
  a relative exists; country: no."*
