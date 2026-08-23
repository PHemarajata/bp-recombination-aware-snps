# Downsampling control — is region attribution a panel-imbalance artifact?

2026-08-22. Addresses weak spot **W2** ("the region successes may be luck") and
settles the **Phase 1 expansion** question without any download.

**Verdict: region attribution is real, not an attractor artifact. It survives a
90× reduction of the dominant region with kappa falling only 0.83 → 0.77.
Country attribution stays at baseline under every panel configuration. A balanced
reference panel neither rescues country nor breaks region — so Phase 1 would
confirm what this free control already shows.**

---

## 1. The concern

The panel is imbalanced two ways: **58% Thailand** at the country level, and
**89% East Asia & Pacific (2,692 of 3,015 references)** at the region level. The
attractor hypothesis (HANDOFF 2026-08-21 §3.3): region scores 89% partly because
a genome with no close relative snaps to the dominant cluster, and coarse 7-way
region labels make that "correct" often enough to look like a capability. If so,
balancing the panel should collapse region accuracy toward chance.

## 2. Design

cgMLST Lichtenegger distance (partition-independent — this is why the control
costs nothing), leave-group-out on exposure country, identical to the scored
attribution. The non-validation reference pool is capped and the panel re-scored;
validation genomes always remain (they are references for each other and are held
out per group). 20 seeded replicate draws per cap. **Primary metric is Cohen's
kappa** — chance-corrected, so immune to the majority-baseline objection that is
the whole point of the test. NN and modal k=20 reported separately; modal k is
the estimator most exposed to pool composition.

## 3. Result — country-level capping (Thailand 1,754 → 25)

| cap/country | Thai n | pool | region NN (κ) | region k20 (κ) | country NN (κ) |
|---|---|---|---|---|---|
| full | 1,754 | 3,004 | +0.72 | **+0.83** | +0.19 |
| 500 | 500 | 1,750 | +0.69 | +0.83 | +0.16 |
| 200 | 200 | 1,273 | +0.69 | +0.83 | +0.15 |
| 100 | 100 | 973 | +0.69 | +0.83 | +0.13 |
| 50 | 50 | 732 | +0.70 | +0.83 | +0.13 |
| 25 | 25 | 483 | +0.72 | **+0.83** | +0.11 |

Region modal-k20 kappa is **flat at +0.83 (±0.00)** across a 70× cut of the
dominant country. But per-country capping leaves East Asia & Pacific dominant as
a *region* (it is many countries), so this is not yet the decisive test.

## 4. Result — region-level equalization (East Asia & Pacific 2,692 → 30)

| cap/region | EAP n | pool | region NN (κ) | region k20 (κ) |
|---|---|---|---|---|
| 200 | 200 | 512 | +0.67 ±0.02 | +0.82 ±0.01 |
| 100 | 100 | 412 | +0.65 ±0.02 | +0.76 ±0.03 |
| 50 | 50 | 290 | +0.64 ±0.04 | +0.76 ±0.04 |
| 30 | 30 | 210 | +0.64 ±0.04 | **+0.77 ±0.06** |

**EAP drops from 89% of the pool to ~15% — a 90× cut — and region modal-k20 kappa
falls only from 0.83 to 0.77.** An attractor artifact would collapse toward 0;
this does not. Region attribution genuinely reads the genome's regional cohort,
not the panel's shape.

The **modest, honest** decline (0.83 → 0.77, and NN 0.72 → 0.64) says a small
part of the headline accuracy — on the order of 10% of the kappa — was
imbalance-assisted. At the most extreme balancing the pool is only 208 genomes,
so the ±0.06 spread means 0.77 is within sampling noise of the full-panel value.
Either way it is a slight erosion, not a collapse.

## 5. Country: not rescued by balance

Country NN kappa runs +0.19 → +0.13 as the panel balances — near the chance line
throughout, and drifting *down* slightly because balancing removes the very
attractor near-hits that produced country's few nominal successes. **No panel
configuration lifts country off baseline.** This is the third independent
confirmation of the divergence-depth ceiling, alongside the Mexico controlled
negative and the resolution curve.

## 6. What this means for Phase 1

Phase 1 was scoped as "*does a balanced reference panel change attribution?* for
the cost of assembly." **This control answers that question directly and for
free:**

- **Country: no.** Balancing cannot rescue it; the ceiling is divergence depth,
  not reference count.
- **Region: barely.** Balancing erodes region kappa by ~0.06 at the extreme, well
  within noise — the signal is not a panel artifact.

So a blanket Phase 1 expansion — download, assemble and QC ~2,000 genomes to
balance the panel — would spend real assembly compute to reproduce a result
already in hand. The expansion's own arithmetic reinforces this: the additions
would land overwhelmingly in East Asia & Pacific (where obtainable public genomes
are), the region that is *already* 89% of the panel and that this control just
shrank 90× with no benefit. The countries whose validation genomes could actually
move — Philippines (12 held-out genomes, zero obtainable references anywhere) —
cannot be helped by any expansion, because the references do not exist.

**Recommendation: do not run Phase 1 as a panel-balancing exercise.** If genomes
are acquired at all, acquire for **validation power** — travel-attributed / ex-
stated imported cases that add held-out ground truth — not for reference density,
which this shows is already saturated where it can be bought.

## 7. Reproduce

```bash
python3 downsample_control_bp.py
```

Deterministic under seed 20260822. ~2 minutes; caches each validation genome's
distance row once, so only the pool selection varies across caps.
