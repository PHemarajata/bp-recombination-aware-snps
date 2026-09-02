# Attribution, final run: duplicates dropped, all estimators

Run 2026-08-21 after the BioProject audit. Panel 3,031 (2 duplicate BioSamples
dropped). Validation **45** (adds `GCF_002111285_1`, "USA: Illinois ex Mexico").
Scheme: Lichtenegger cgMLST v1.1, 4,221 loci.
Script `score_cgmlst_lichtenegger.py`, data `CGMLST_LICHT_ATTRIBUTION.tsv`.

---

## 1. The regional number was never down

The 71% I reported earlier was an artifact of two things, both now fixed:
I had implemented **only the nearest-neighbour estimator**, and the duplicate
leak was still in the pool.

| estimator | country | **region** |
|---|---|---|
| nearest neighbour | **10/46 (22%)** | 37/46 (80%) |
| modal, k=5 | 6/46 (13%) | 39/46 (85%) |
| modal, k=10 | 6/46 (13%) | 39/46 (85%) |
| **modal, k=20** | 7/46 (15%) | **41/46 (89%)** |
| enrichment, k=20 | 0/46 (0%) | 31/46 (67%) |
| majority baseline | 12/46 (26%) | 21/46 (46%) |

> **Updated 2026-08-23, Track 0 integration** (was n=43: country NN 9/43, region
> modal 40/43 = 93%). Validation set 43 → 46: +Portugal→Thailand (a correct
> close-relative country hit) and +2 Mississippi autochthonous cases → **North
> America, previously untested**. The Mississippi lineage misattributes to Latin
> America, which is why region falls 93% → 89% — a gain, not a regression (see
> `TRACK0_INTEGRATION_2026-08-23.md`).

**Region is 93% on 43 genomes from 15 countries, against 92% on 24 genomes
previously.** The result got slightly better on a set nearly twice the size and
considerably harder.

This matters for the earlier comparison too. The original core-genome result was
**modal 92%, nearest-neighbour 67%** on the same data. My cgMLST scorer only had
nearest-neighbour, so 71% was never comparable to 92%. It was comparable to 67%,
and it beat it.

**Estimator choice is scale-dependent, and worth a sentence in the paper.**
Country does best under nearest-neighbour (22% vs 15%): averaging over neighbours
dilutes a signal that only the single closest genome carries. Region does best
under modal k=20 (89% vs 80%): averaging suppresses noise in a coarse label.
Enrichment is the worst at both, which is the opposite of what it did on the
core-genome units.

Region by exposure country, modal k=20: **12 of 15 fully correct.** Philippines
12/12, India 6/6, Mexico 5/5, Viet Nam 2/2, Guatemala 2/2, Aruba 2/2, Australia
2/2, Trinidad 2/2, plus Costa Rica, Martinique, El Salvador, Nicaragua at 1/1.
Failures: Thailand 1/4, Nigeria 0/1, Ghana 0/1.

## 2. Dropping the duplicate fixed the India rows exactly as predicted

Before, with `GCF_030010175_1_USA_Georgia` leaking into the pool: India 0/6 at
both scales. After dropping it: **India 6/6 at region.** Viet Nam went 0/2 to
2/2, Guatemala 0/2 to 2/2.

## 3. But the country result does not survive a distance check

Stratifying by nearest-neighbour distance, which asks whether a "correct" answer
was backed by an actual relative:

| stratum | n | **country** | **region** |
|---|---|---|---|
| **d < 0.05**, a real relative exists | 14 | **2/14 (14%)** | 11/14 (79%) |
| 0.05 to 0.30, distant | 10 | 2/10 (20%) | 6/10 (60%) |
| **d >= 0.30**, no real relative | 22 | **6/22 (27%)** | **20/22 (91%)** |

**Country attribution is 2/14 where a genuine close relative exists, and 6/22
where none does.** The one added success (Portugal, an imported case whose Thai
strain has a real Thai relative at d=0.020) is a genuine country hit and softens
the "1/13" to "2/14" — but the pattern stands: country scores no better, and
often *better*, when there is nothing real to match. That is not attribution.

The nine "correct" country calls, by distance:

| exposure | d | what it is |
|---|---|---|
| Thailand | **0.0066** | **the only genuine success in 43** |
| Australia | 0.0537 | distant |
| Thailand | 0.0827 | distant |
| Nigeria | 0.5880 | attractor |
| India x5 | **0.638 to 0.642** | **attractor** |

The five Indian "successes" in §2 are at **d = 0.64**, meaning 64% of cgMLST loci
differ. Their nearest neighbour is `GCF_017653105_1_India`, a genuine Indian
deposit that is nonetheless unrelated. The aromatherapy strain has no close
relative anywhere in the panel, so it snaps to the nearest distant thing, which
happens to be Indian and therefore scores correct.

**The honest country result is 1 genuine success out of 43.**

## 4. The same effect inflates the region number

Region also scores **highest where no relative exists**: 91% at d >= 0.30 versus
77% at d < 0.05.

This is the Ecuador-attractor effect from the earlier analysis, confirmed on a
larger set. A genome with no true relative snaps to a distant cluster, and
because regions are coarse catch-alls, that is usually the right region. It is
right for Latin American and Indian cases and wrong for African ones (Nigeria
0/1, Ghana 0/1, both at d > 0.58).

**So the 93% is real as a number and misleading as a claim.** The method is not
identifying provenance for most of these genomes. It is reporting "unlike the
Asian majority of the panel," and the region label converts that into a correct
answer often enough to look like attribution.

## 5. What to actually claim

1. **Country-level attribution fails, and now for a demonstrated reason rather
   than an absence.** Where a genuine close relative exists it is **1/13**. It is
   not that we lack references; it is that having them does not help.
2. **Mexico is the controlled case.** 4 references to 21, still 0/5 at country,
   nearest neighbours at d = 0.41 to 0.46. References for the right country do
   not help if they are the wrong lineage.
3. **Regional attribution is 93%, and the distance stratification must be
   reported beside it.** Without it the number implies a capability the method
   does not have.
4. **Report the nearest-neighbour distance with every call, and abstain above a
   threshold.** At d >= 0.30 the method has no relative to reason from. An
   abstention rule would decline 22 of 43 calls and would have avoided the two
   confident African errors, at the cost of the six lucky country hits, which
   were never real.

## 6. Fixes applied in this run

- Dropped `GCF_030010175_1_USA_Georgia` and `SRR34266633`
  (`PANEL_DUPLICATES_2026-08-21.tsv`).
- Added `GCF_002111285_1` to `EXPOSURE_OVERRIDES.tsv` as Mexico exposure.
  Validation 44 to **45**, Mexico 4 to **5**.
- Scorer now applies `EXPOSURE_OVERRIDES.tsv` directly and reports five
  estimators.

## 7. Still open

- **16 intra-panel duplicate BioSamples**, 7 with both copies inside the same
  analysed unit. Does not affect this cgMLST result, does affect r/m and
  distances. See `BIOPROJECT_AUDIT_2026-08-21.md` §4.
- **`SRR35004689` (India exposure) matches `SRR35159552` at d = 0.023**, a tier-C
  deposit-only USA genome from the new batch. Either a shared lineage or another
  unstated exposure. No evidence either way; left as tier C.
- PubMLST vs Lichtenegger scheme concordance, both profile sets now exist.
