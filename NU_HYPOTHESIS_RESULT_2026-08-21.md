# The nu hypothesis is refuted — and why it looked right

**Final, on the FROZEN BASIS: 170 replicon-units (chr1 n=85, chr2 n=85).**
2026-08-21, after the ClonalFrameML job finished 172/172 with every unit
`exit=0`. Both replicons agree throughout. Script: `nu_hypothesis_bp.py`.
Data: `NU_HYPOTHESIS.tsv` (170 rows), regenerated 2026-08-22 on
`FINAL_BASIS_2026-08-22/` — 85 units, 2,340 genomes. The earlier 172-row
version (86 units) is kept as `NU_HYPOTHESIS.tsv.pre-frozen-basis.bak`.

> **This supersedes two earlier versions of this document** written mid-run at
> n=81 and n≈148. The conclusion held, but **most of the supporting numbers
> moved, and one secondary conclusion had to be re-argued from scratch** — see
> *Corrections to the record*. The denominator is **172, not 176**: four of the
> 176 v4c cluster directories have no `.core.full.aln` (units `strain_1_L1_36`
> n=48 and `strain_1_L1_37` n=9, both replicons) because they ran on the A100 and
> only trees and Gubbins output were copied back.

---

## What was predicted

Gubbins detects recombination as regions of unusually **dense** SNPs. An import
only looks dense if the donor differed from the recipient — the divergence
ClonalFrameML estimates as **nu**. So where nu is low, imports should carry too
few SNPs to register, Gubbins should report a low r/m, and the unit should look
like a detection failure while recombination is actually happening.

**Prediction: low nu → low Gubbins r/m.** This was to be the explanation for the
depressed-r/m residue that six earlier candidate explanations had failed to
account for.

## What the data says

**The relationship runs the other way.**

| test | chr1 (n=85) | chr2 (n=85) |
|---|---|---|
| nu vs Gubbins r/m *(predicted +)* | **rho −0.274**, p=0.011 | **rho −0.346**, p=0.0012 |
| Gubbins-rejected units have lower nu? | p=0.244, **no** | p=0.059, *not significant, and the wrong direction* |

Units with *low* nu have *higher* Gubbins r/m. The hypothesis is refuted on its
own clean test — the one where Gubbins never sees nu, so no shared arithmetic can
manufacture a correlation.

**A caveat that appeared on the 86-unit set and has now gone away.** At n=81 the
rejected units had no distinctive nu on either replicon (p=0.22 / 0.17). On the
86-unit set chr2 crossed into nominal significance (p=0.039), which forced the
qualification that *"rejected units have no distinctive nu"* could no longer be
stated flatly. **On the frozen basis it does not reach significance on either
replicon — chr1 p=0.244, chr2 p=0.059** — with rejected units' nu marginally
*higher* (median 0.0040 vs 0.0039), i.e. pointing away from the prediction
regardless.

**So the flat statement is restored**, with the history recorded rather than
erased: the effect was never more than one-replicon, marginal, and
wrong-signed, and it moved back across p=0.05 when a single uninformative unit
was dropped. That fragility is itself the reason not to lean on it in either
direction.

Distributions for reference:

| | chr1 | chr2 |
|---|---|---|
| nu | median 0.0036 (0.0030–0.0908) | median 0.0039 (0.0032–0.0759) |
| delta | median 2,551 bp (27–5,204) | median 2,540 bp (32–4,900) |
| R/theta | median 1.351 (0.147–2.464) | median 1.300 (0.233–2.228) |
| r/m Gubbins | median 5.51 | median 5.51 |
| r/m CFML | median 14.09 | median 13.85 |

## Why it looked right at first

**nu and delta are strongly anti-correlated: rho −0.786 (chr1), −0.778 (chr2)**
— pooled −0.758, p=5e-33.

ClonalFrameML trades the two off when fitting: a unit fitted with long tracts
gets low per-site divergence, and one fitted with short tracts gets high
divergence. Both describe the same amount of imported sequence. **nu is therefore
not independently interpretable** — any apparent nu effect is mostly delta
wearing a disguise.

That is what the n=2 early read picked up. Both units are still in the set with
the same values: `strain_9_L1_1` has nu 0.0041 *and* delta 3,609 bp;
`strain_27_L1_1` has nu 0.064 *and* delta 27 bp. Attributing the difference to nu
rather than delta was a coin flip, and it came down wrong.

**This is a caution about ClonalFrameML output generally, not just about us:**
nu and delta should be read as a pair, never singly.

## What actually correlates with Gubbins r/m

**Tract length, correctly signed and stronger than nu:**

| | chr1 | chr2 |
|---|---|---|
| **delta vs Gubbins r/m** | **+0.615** | **+0.723** |
| delta × nu (expected SNPs per tract) vs Gubbins r/m | +0.650 | +0.781 |
| R/theta vs Gubbins r/m | +0.169 (p=0.12, n.s.) | +0.068 (p=0.53, n.s.) |

Short tracts depress Gubbins' r/m. That is mechanistically sensible — a short
tract carries few SNPs regardless of how divergent its donor was. Note that
**R/theta, the actual recombination rate parameter, does not predict Gubbins r/m
at all** on either replicon.

**But the obvious mechanism is still not the explanation.** Gubbins runs with
`min_snps=3`, so a tract expected to carry fewer than 3 SNPs is invisible by
construction. Only **3 of 86** (chr1) and **4 of 86** (chr2) units fall below that
floor; the median unit expects **9.6 / 9.9 SNPs per tract**. The `min_snps` floor
does not account for the bulk of low-r/m units. Whatever depresses them is not
simply the detection threshold.

---

## The other claim this kills: ClonalFrameML does not "rescue" rejected units

25 of 33 (chr1) and 28 of 33 (chr2) Gubbins-rejected units have CFML r/m ≥ 3.0,
which invites the reading that CFML recovers them. **It does not — but the
argument for that has changed completely, and the old one was wrong.**

### The old argument is withdrawn as invalid

Earlier versions argued: *the CFML/Gubbins ratio is not larger for rejected units
(p = 0.23 / 0.28), so the offset is a uniform multiplier and nothing unit-specific
is happening.* On the full set that test now comes out **strongly significant in
the opposite direction** — rejected units have a median ratio of 6.10× vs 1.86×
for accepted (chr1), 5.95× vs 1.95× (chr2), both p < 0.001.

**Neither result should be used, because the test is circular.** The groups are
defined by low `rm_gubbins`, and `rm_gubbins` is the *denominator* of the ratio.
Selecting on the denominator inflates the ratio mechanically. The test cannot
support "uniform offset" or "unit-specific rescue"; it is uninformative in both
directions and was uninformative at n=81 too. The old p=0.23 was a null result
from an invalid test, which is not evidence of anything.

### The valid argument, which reaches the same conclusion

Ask instead where the rejected units sit **on the CFML scale itself**, with no
shared denominator:

| | chr1 | chr2 |
|---|---|---|
| CFML r/m, Gubbins-rejected (n=32) | median **9.98** | median **9.45** |
| CFML r/m, Gubbins-accepted (n=53) | median **15.56** | median **15.59** |
| Mann-Whitney | p = 3.6e-05 | p = 3.7e-06 |
| rejected units' median percentile in the CFML distribution | **30th** | **26th** |
| Gubbins vs CFML rank agreement | rho **+0.612** | rho **+0.599** |

**CFML agrees with Gubbins about which units are the low-recombination ones.**
Rejected units keep significantly the lower CFML r/m and sit in the bottom third
of the CFML distribution. The two tools rank units consistently (rho ≈ +0.60).

They cross 3.0 only because **the entire distribution sits 2.19× (chr1) / 2.45×
(chr2) higher** — pooled 2.43×, IQR 1.6–4.8× — so essentially everything clears a
fixed 3.0 line: **52 of 53** accepted units on chr1 and **53 of 53** on chr2 do
too. A threshold that passes 99% of units is not discriminating; the 8 and 5
units that still fail are the signal, not the 25 and 28 that pass.

**Do not report CFML as rescuing units Gubbins rejected.** CFML re-scales; it
does not re-rank.

## What this does to the gate-dependence concern

It makes it smaller and more precise. The earlier 46-unit result — 8 units
flipping accept/reject between tools — is better read as **rank noise between two
noisy estimators on a common scale** than as one tool systematically missing a
class of unit. Rank agreement on the frozen basis is rho +0.612 (chr1) / +0.599
(chr2), up from +0.30 on the old partition.

The defensible statement becomes: *pooled r/m is estimator-dependent in absolute
value (≈2.5–2.6×) and only moderately consistent in rank (rho ≈ 0.6), so a
threshold calibrated on one tool does not transfer to the other* — rather than
*the gate systematically rejects a recoverable class of unit*.

---

## Corrections to the record

**Refuted hypotheses:**

1. **`RECOMBINATION_HANDOFF_CRITIQUE_AND_REDESIGN.md` §1.5** proposed low nu as
   "a live sixth hypothesis" for the depressed-r/m residue. **Refuted.**
2. **`ATTRIBUTION_AND_DISTANCES_FINDINGS_2026-08-20.md` §6** repeated it.
   **Refuted.**
3. The n=2 early read reported mid-run. **Withdrawn** — it could not distinguish
   nu from delta, and delta was the real correlate.

**Numbers withdrawn from the two earlier versions of this document,** all of
which were computed on an unfinished run and every one of which moved:

| quantity | n=81 | n≈148 | n=172 (86u) | **frozen n=170 (85u)** |
|---|---|---|---|
| nu vs Gubbins r/m | −0.417 / −0.487 | −0.42 / −0.49 | −0.286 / −0.367 | **−0.274 / −0.346** |
| nu vs delta | −0.809 / −0.864 | −0.86 | −0.791 / −0.785 | **−0.786 / −0.778** |
| CFML/Gubbins offset | **≈4.9×** | ≈4.9× | **2.19× / 2.45×** |
| delta vs Gubbins r/m | +0.529 / +0.578 | — | **+0.615 / +0.723** |
| rank agreement (chr1) | +0.59 | — | +0.611 | **+0.612** |
| rejected-unit nu, chr2 | p=0.17 | p=0.23 | p=0.039 | **p=0.059** |

**The ≈4.9× offset figure is wrong wherever it appears.** It is 2.5–2.6× on the
frozen basis (2.2–2.5× as reported on the 86-unit set).

**One argument withdrawn, not just a number:** the "uniform offset, p=0.23"
reasoning in the rescue section is invalid as described above. The conclusion it
supported survives on different evidence.

This is the **seventh** instance in this project of a figure recorded from a
denominator that was still filling. Contributing factors worth generalising:
`nu_hypothesis_bp.py` rewrites only `NU_HYPOTHESIS.tsv` and **not this prose
file**, so a stale write-up kept circulating the old numbers after the data was
corrected; and the assumed denominator (176) was itself wrong.

The residue of depressed-r/m units remains **unexplained**, now with a seventh
candidate excluded. That is the honest state, and it matches the original
handoff's own warning to budget for a residue of unexplained failures rather than
assume a predictor exists.

## Still open

- delta explains part of it (rho +0.62 / +0.72) but `min_snps` is not the
  mechanism. What sets delta per unit, and is short delta itself an artefact of
  fitting? The nu/delta trade-off at −0.79 makes this hard to answer from CFML
  output alone.
- **R/theta does not predict Gubbins r/m at all** (+0.169 / +0.068, both n.s.),
  yet it is the parameter that ought to. That is now the more interesting
  anomaly than nu.
- Log-log regression of Gubbins r/m on R/theta, delta and nu gives coefficients
  far from the +1 expected if Gubbins simply measured their product — chr1
  +0.450 / +1.210 / +1.428, R²=0.411; chr2 +0.163 / +1.873 / +2.688, R²=0.618.
  Gubbins over-weights delta and nu and under-weights R/theta, and a third to a
  half of the variance is unexplained.
- Recover the two A100-only alignments (`strain_1_L1_36`, `strain_1_L1_37`) to
  close the set at 176. Given both replicons agree at n=86, this will not change
  anything material — but the *last* three times that was asserted mid-run, the
  numbers moved.
