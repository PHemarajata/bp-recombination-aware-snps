# Session handoff — 2026-08-10

Companion to `HANDOFF_research_gaps.md` (the research state) and
`REVISED_STRATEGY_2026-08.md` (the strategy, whose **Appendix A** holds
everything measured in this session). This file is the operational state: what
was run, what was found, what is in flight, and what to do next.

**Read `REVISED_STRATEGY_2026-08.md` Appendix A first.** It is the durable
record; this file is the pointer.

---

## 0. WHERE WE ARE (2026-08-11) — read this, then A.11 and A.11b–A.11f

### The method and parameters are SETTLED

| Step | Setting | Basis |
|---|---|---|
| Reference | per-cluster **constrained medoid**, complete (≤2 contigs) | avoids ~87% false calls; A.3b/c |
| Caller | **reference-free `ska_map`** for SNPs, r/m, union **and slopes** | mapping caller adds ~9,000 phantom positions and inflates slopes; A.3c, A.11e |
| k-mer | `--k 31` (never the helper's 17) | 59% → 3.5% masking; A.3a |
| `-fconst` | from the **full** alignment | SNP-only file returns `0,0,0,0`; A.3a |
| Replicons | split **before** Gubbins | forced by tooling; A.4 |
| Gubbins | ≥3.4.3, `--invariant-site-correction` explicit | A.4 |
| Diversity | **`ska distance --min-freq 0.0`**, never Mash | ±13% on 4 anchors; Mash spans 0.88×–91×; A.7/A.8 |
| Modality | **n ≥ 25; mixture if gap/mean > 1.0 OR empty_bins > 0.45.** Apply AFTER the diversity gate | calibrated by subsampling; A.11f |
| Operating range | **~1,270 – 4,671** ska units | A.11, A.11b |
| Detection gate | **union ≥ 47%** (insensitive: 20–58% identical) | 41-point empty band; A.11c |
| Dating | refuse above **4,700** ska; judge on \|slope\| **magnitude** only | coincides with r/m ceiling; A.11e |
| Partition | **fastbaps L1** — not L3, and do **not** raise `levels` to 5 | L3 shatters strains into pairs; A.11b |
| Tree support | **NOT a gate.** Report it, then **collapse** branches below support into polytomies | headline moved 5.3× on the threshold, and 70 is the wrong scale for UFBoot; **A.11y** |
| Acceptance | **pooled r/m is the ONLY gate.** union, tract and support are diagnostics | A.11r, A.11y |
| Reference borrow | bound is an **assumption**, not a measurement; quality declines with borrow distance (r/m r = −0.38) | **A.11y**, Tier 0.4 |

**Evidence base:** 6 full 12-arm runs + 13 reduced 4-arm runs + 2 L1 sub-cluster
runs; 91 clusters measured for diversity, 56 + 47 + 49 + 46 screened for modality.

### What is NOT settled

1. **Floor bracketed to (405, 1,268]** — 3.1×. Needs one continuous cluster near ~700.
2. **Ceiling bracketed to (4,671, 6,342]** — 1.36×, but **`cluster_0` (ska 9,617, continuous) has a sound slope**, the only one of seven above the ceiling. Unexplained; the ceiling is a tendency with a counter-example, not a law.
3. **The 5e-06 slope-soundness cutoff is a chosen round number**, and `cluster_10` (5.02e-06) only just exceeds it — so the two clusters bracketing the ceiling are the two nearest that cutoff.
4. **Only 29.6% of the collection (828/2,802) is analysable.** The largest recoverable block is the in-range BIMODAL sub-clusters (N1a) — `s1_L1_27` alone is 150 genomes.
5. **25 sub-clusters / 360 genomes are UNDECIDABLE** (in range but n < 25). Recovering them needs a statistic that works at small n — `gap/mean` and `empty_bins` both fail there (A.11f). A.10's 800–2,500 band claim used the old n≥30/0.09 rule and still needs re-checking.
6. **Circularity:** thresholds were measured on size-capped fragments, half of them bridged. They must be re-verified on any new partition.
7. **BioProject ICC** unmeasured — effective *n* still spans 672→35 on that one number.
8. **The subtree merge under recombination** — unsolved, needs simulation not clusters.

> ## ⚠ SUPERSEDED 2026-08-11 by the completed production run — see **A.11t**.
> **N1, N2 and N3 are DONE.** All 45 units ran (180 arms, zero failures) and were
> triaged. **The measured coverage is 933 genomes / 30 units = 33.3%**, not 44.0%
> — the 1,233 figure counted units that had not yet been tested.
> **The union screen is size-confounded** (r(log n, union) = +0.81, A.11r) and
> must not be applied as a fixed cutoff; judge small units on r/m. Read
> **A.11r and A.11t first**, then A.11j–A.11s. Everything below this line is the
> pre-run plan, retained as the record of what was expected.

### THE ANALYSABLE SET IS BUILT — 1,233 genomes, 45 units, 44.0%

| source | units | genomes | modality-screened |
|---|---|---|---|
| L1 sub-clusters, n ≥ 25 | 11 | 660 | yes |
| L1 sub-clusters, n < 25 | 25 | 360 | **NO — accepted unscreened** |
| PopPUNK strains already in range | 9 | 213 | n/a |
| **TOTAL** | **45** | **1,233** | **44.0% of 2,802** |

**Files (all in the working dir):**
- `analysable_units.tsv` — the production target list, with a `screened` column
- `inputs/analysable_membership.tsv` — unit → genome
- `analysable_references_final.tsv` — **12 internal medoids + 33 borrowed**, every
  borrow within Mash 0.005 (median 0.00355, max 0.00479) vs K96243's 0.0073 floor
- `analysable_refs_runner.tsv`, `analysable_modality.tsv` — runner-format copies
- `refs/analysable/` — 14 distinct reference FASTAs staged, all ≤2 contigs

**THE DELIBERATE COMPROMISE, and it must be stated in any write-up.** 360 genomes
in 25 units enter the pipeline **without a modality check**, because both
statistics fail below n=25 (A.11f). Some are probably bridged. The safety net is
r/m — bridged clusters give 0.94–1.49 — but it fires *after* the Gubbins run, not
before. Expect wasted runs and treat r/m as the flag. A quarter of the analysable
set was not screened for the property the rest was screened on.

### WHAT'S NEXT, in order

**N1. ✅ DONE 2026-08-11 — the borrowed reference PASSES.** `prod_s2_L1_2`
(n=75, ska 2,460, borrow `GCF_009741295_1_Viet_Nam` at Mash 0.00137) gives
**union 85.8%, pooled r/m 7.23, tract 5,928** — mid-range on all three, and
within a few points of its K96243 contrast arm on every statistic. 4/4 arms, no
failures. **Full result and caveats: A.11g.** The other 32 borrows are licensed
by analogy only (every borrow is closer than the K96243 arm that already works);
re-examine any that turns up RM-LOW.

**N2. ▶ IN FLIGHT since 13:06, 2026-08-11 — the remaining 44 units.**

```
python3 -u reduced_refsens_bp.py --clusters "<44 units, comma-separated>" \
  --threads 4 --reserve-cores 4 \
  --membership inputs/analysable_membership.tsv \
  --references analysable_refs_runner.tsv \
  --modality analysable_modality.tsv --outdir-prefix prod_ > N2_run.log 2>&1
```

**`--clusters` IS REQUIRED** — the earlier form of this command omitted it and
exits instantly with "nothing to run" (A.11h). Build the list with
`awk -F'\t' 'NR>1 && $1!="s2_L1_2"{print $1}' analysable_units.tsv | paste -sd,`.
22 cores → 4 arms × 4 threads, 6 free. All 44 passed a `--dry-run` preflight
(every reference resolves, 2 contigs, n matches). Progress: `tail -f N2_run.log`;
resumable — completed arms are skipped, so re-issuing the same command is safe.

**N3. Triage the results on union AND r/m** (A.11, A.11c). Tool:
**`python3 triage_analysable_bp.py`** (self-tested; reproduces the published
A.11 rows from disk). Units failing r/m are the unscreened bridged ones —
expected, not a pipeline fault. **The two cutoffs are not equally evidenced:**
union ≥ 47% sits in a 41-point empty band and is insensitive over 0.20–0.58,
whereas the r/m ≥ 3.0 line rests on ONE in-range point either side
(`s1_L1_27` bridged at 2.57, `cluster_15` working at 3.38 — a 1.3× bracket).
Treat RM-LOW as "re-examine", never as a verdict.

> ## ⚠ COVERAGE SUPERSEDED 2026-08-11 — see **A.11ac**. The figure is **30.4%**
> (26 units / 853 genomes), or **35.1%** against the 2,430 genomes that were ever
> eligible. The 9 PopPUNK-strain units are **WITHDRAWN**: completing the fastbaps
> partition across all 42 strains showed their apparent diversity was mixture
> structure (`strain_8`, apparent ska 1,265, is a 36-genome clonal core at **55**
> SNPs, gap/mean 8.697). One replacement unit was recovered — `s13_L1_1` (n=31),
> pooled r/m **12.89** against `strain_13`'s 2.89. **Always quote the denominator:
> 372 genomes sit in strains too small to partition and were never candidates.**

**N3 ✅ DONE 2026-08-11 — see A.11t.** 30 units / 933 genomes usable (**33.3%**)
under the size-corrected reading; 12 units / 662 genomes (23.6%) if the union
screen is applied strictly, which is **not** recommended (A.11r). Worst block was
the **PopPUNK strains** (56%), not the unscreened sub-clusters (64%).

**N4 ✅ PER-UNIT STAGE ALREADY COMPLETE — no new compute needed (A.11v).** Its
specified content (replicon split, Gubbins ≥3.4.3 with explicit
`--invariant-site-correction`, `-fconst` from full alignments, trees) is exactly
what the `prod_` runs executed. **90 trees exist** (45 units × 2 replicons,
close reference); all 30 usable units verified — tip counts equal n, models are
the expected K3Pu/HKY family.

**But two things came out of verifying them:**

- ⚠ ~~**UFBoot ≥ 70 ADOPTED as a third criterion (A.11v).**~~ **WITHDRAWN
  2026-08-11 (Tier 0.1, A.11y). FINAL COVERAGE IS 33.3% — 30 units / 933
  genomes.** Two reasons. (1) **Wrong scale:** 70 is the *standard*-bootstrap
  convention; UFBoot's own is **95**, so applying 70 to UFBoot values was more
  permissive than the convention cited for it, not more conservative. (2)
  **Coverage moves 5.3×** across defensible thresholds (33.3% no gate → 25.3% at
  70 → 6.3% at 95), so the headline was reporting a convention.
  **What replaces it:** keep every unit; collapse branches below support into
  polytomies with **`python3 collapse_unsupported_bp.py --support 95`** (58% of
  internal branches collapse at 95, 34% at 70) and carry the uncertainty
  downstream. `s1_L1_9` (n=90) and `s16_L1_3` (r/m 10.43) are **restored**.
  A.11v's underlying measurement stands and is still reported: resolution is
  orthogonal to r/m (−0.010) and only weakly size-dependent (+0.171). It is a
  diagnostic, not a gate. **Every downstream method must tolerate polytomies.**
- **The merge is the blocker and was NOT attempted (A.11w).** Combining units —
  or even the two replicons *within* a unit — is the documented-unsolved step.
  **Corrected 2026-08-11 (Tier 0.2):** the reason is **not** that branch-length
  units are incommensurable — with `-fconst` from the full alignment they are
  already in substitutions per full-alignment site. The real residues are
  **differing denominators** (each unit aligned to a different reference, so
  "core site" denotes a different position set) and **independent per-unit
  correction**. Practical guidance unchanged: **do not date a grafted tree.**
  **No per-unit consensus tree exists and none can be made without settling
  this.** Next step is simulation (SimBac), not more cluster runs.
**Two decisions taken 2026-08-11; two remain.**

1. ✅ **Coverage reading: 33.3% size-corrected, ADOPTED.** Judge units on pooled
   r/m; do not apply union as a fixed cutoff (A.11r). 30 units / 933 genomes
   enter N4. The 44.0% figure is a *candidate* count and must not be quoted as
   coverage.
2. ✅ **Strains re-screened (A.11u).** Caught `strain_8` — `gap/mean` **2.695**,
   the second-highest ever measured, and the largest strain at n=46 — which had
   been admitted with no screening at all. **Zero false positives, but only 1 of
   5 failures caught.** Adopt the screen (it is cheap and safe) but do not treat
   it as fixing the block.
3. ⚠ **The floor CANNOT currently be derived — attempted and failed (A.11x).**
   UFBoot does not work for it (`cluster_53` at ska 535 has UFBoot 94.5; UFBoot
   tracks phylogenetic signal, which keeps rising into the regime where
   detection has collapsed — `cluster_2` at 13,826 scores 98). Detection does not
   work either: **all three units below ska 1,268 are disqualified** — two are
   mixtures (`cluster_53` 1.549, `strain_8` 2.695, and A.11e forbids mixtures
   setting diversity thresholds) and `cluster_62`'s modality is formally
   undefined because it sits below the very gate being derived. **The bracket
   stays (405, 1,268] and rests on nothing admissible.** Do not quote ~1,270 as
   measured — it is only the lowest diversity at which a unit has been observed
   to work. **Settling it needs a CONTINUOUS unit with n ≥ 25 in ska 535–1,265,
   which the current partition does not contain.**
4. ⬜ **The r/m failures no upstream statistic predicts** — the ska 3,956–4,088
   dip (`s1_L1_19`, `s3_L1_10`, `s1_L1_13`, A.11l), plus 4 of 5 strain failures
   (A.11u). **SEVEN hypotheses now refuted**, including the two best ones:
   callable-fraction variance (A.11aa) and **low ν** (A.11ab — ν ratio 1.00,
   and ν varies more between replicons than between units, so it is a constant
   of the organism). **This is still the largest open problem in the method.**
5. 🔴 **NEW, and it outranks Tier 2: is pooled r/m tool-dependent?** (A.11ab)
   ClonalFrameML does not reproduce Gubbins' ordering of the same six units —
   Gubbins' lowest-r/m unit is CFML's second-highest; Spearman **+0.31**;
   CFML/Gubbins ratio median 4.3×. r/m is the **sole** acceptance gate, so this
   bears on every unit-level verdict. **n = 6 has no power — settle it by running
   `clonalframe_nu_bp.py` across all 45 units** (tooling written, hours of
   compute) **before the Tier 2 simulation**, which would otherwise calibrate a
   null against an unsettled criterion.

**Still open, needing no more clusters:** floor bracket (405, 1,268]; the
`cluster_0` ceiling anomaly; BioProject ICC; the subtree merge; the
K96243/1026b bridge from cluster_37 (publishable alone, §2.4).

**Subdivision is exhausted** — both in-range bimodal units are done. `s1_L1_27`
recovered 45 of 150 (the other 95 are a clonal expansion at mean 140 SNPs);
`s1_L1_32` recovered nothing (its 2,378 was manufactured by 4 outliers; the
33-genome core measures 485). **Triage rule from those two cases:** `empty_bins`
high with `gap/mean` LOW → real modes, worth splitting. `gap/mean` HIGH → tight
core plus outliers, splitting is futile.

### Performance note

Arms are independent. `reduced_refsens_bp.py --threads 4 --reserve-cores 4` runs
**4 arms × 4 threads, 4 cores free**, a **measured 1.7×** speedup over
1 arm × 16 threads — IQ-TREE does not scale past ~6 threads (656% CPU on 16).
6 cores are left idle deliberately: this laptop froze once mid-run with no OOM
evidence. Cloud burst is ~$2–5 for the remaining threshold work but ~1–2 h of
setup, so it only pays off from N1 onward; check the Thai data-sharing agreement
before staging anything non-public.

---

## 1. The headline results, measured this session

> ## ⇒ READ `REVISED_STRATEGY_2026-08.md` **APPENDIX A.11** FIRST.
> It is the final synthesis over **17 clusters** and supersedes A.6/A.7/A.9/A.10
> and **§2.3** wherever they conflict. **The stopping rule is now measured:**
> **(1) DIVERSITY FIRST** — measured mean pairwise core SNPs in **~1,270–4,671**
> (calibrated `ska distance`, never Mash). **(2) THEN modality**, at n ≥ 25:
> mixture if `gap/mean > 1.0` OR `empty_bins > 0.45` (A.11f). The order matters —
> gap/mean divides by the mean, so it is unstable on very tight clusters.
> **(3) Screen both union coverage and pooled r/m** — neither detects both
> failure modes. The derived ~1,000 cap sits **below the floor, in a zone where
> Gubbins detects ~0.7% of recombination.** Rows below marked WITHDRAWN or
> superseded are kept as a record of what was tested and rejected.

| Finding | Where |
|---|---|
| **FINAL RULE: diversity 1,270–4,671 FIRST, then modality at n≥25 (gap>1.0 OR empty>0.45); screen union AND r/m** | **A.11, A.11f** |
| **Operating range ~1,270–4,671 (ska units); 7 consecutive clusters 6,342–13,826 collapse** | **A.11, A.11b** |
| **fastbaps L1 supplies the partition: 10 sub-clusters, 615 genomes. Use L1, NOT L3 — do NOT raise levels to 5** | **A.11b, A.11f** |
| **COLLECTION-WIDE ANALYSABLE: 1,233 / 2,802 = 44.0%** across 45 units, after accepting 25 unscreened units (n<25) | **A.11f, §0** |
| **All 45 units have a reference: 12 internal medoids + 33 BORROWED**, every borrow within Mash 0.005 | **§0** |
| **s1_L1_27's bimodality = a 95-genome CLONAL EXPANSION at mean 140 SNPs** (unusable for Gubbins; of interest for outbreak analysis) | **A.11f** |
| **Modality needs TWO statistics** — gap/mean catches tight-core+outliers, empty_bins catches wide multimodal (cluster_48: gap 0.128 MISSES, empty 0.60 catches) | **A.11f** |
| Modality is size-dependent: **undecidable below n=25**, both classes overlap at every threshold | **A.11f** |
| Diversity has TWO scales: alignment-derived runs ~10% above ska. **Apply the rule in ska units only** | **A.11** |
| **Two failure modes, two detectors: below the floor union → ~1%; above the ceiling union stays NORMAL while r/m → 0.66–1.74** | **A.11** |
| **The derived ~1,000 cap is below the measured floor — it would drive subdivision into a blind zone** | **A.11** |
| Reference bias in *B. pseudomallei*, quantified and replicated | A.3b, A.3c |
| Clusters are size-capped, not lineages — **measured: 70.3% of clusters / 88.1% of genomes** exceed the derived ceiling (proxy said 79.1%/94.3%) | A.1, A.3d, **A.8** |
| Per-cluster references are 93% solvable today | A.3e |
| Six defects in tooling, three of which fail **silently** | A.3a |
| **The Mash→SNP proxy overestimates 1.36–4.23×; A.3d's validation had the sign backwards** | **A.5** |
| **The dating and r/m ceilings COINCIDE at (4,671, 6,342] ska. `DATING_MAX`=4,700** | **A.11e** |
| Read SLOPES from the reference-free caller — the mapping caller inflates them (1.8e-05 vs 3.7e-06 on cluster_0) | **A.11e** |
| **Never use a MIXTURE to set a diversity threshold** — it cost two wrong `DATING_MAX` values | **A.11e** |
| Dating diagnosed on \|slope\| MAGNITUDE only — sign is noise (A.10 retracts A.9's sign criterion) | A.9, A.10 |
| **Union cutoff CALIBRATED: 47%, and insensitive — a 41-point empty band spans 20–58%** | **A.11c** |
| **REFUTED: union does NOT gate dating. Highest union (86.5%) has an inflated slope; lowest (18%) a sound one** | **A.11c** |
| **R² does not flag it — screen measured diversity + slope sign/magnitude instead** | **A.9** |
| **Clusters are multi-modal MIXTURES — a cap on the mean is the wrong parameterisation** | **A.9** |
| ~~Under-detection at low diversity is real~~ → **REINSTATED on clean evidence**: cluster_62 (405, *continuous*) gives 0.7% union, r/m 0.07 | **A.11** |
| **STRUCTURE × DIVERSITY: bridged clusters give r/m 0.94–1.49 regardless of diversity; only CONTINUOUS clusters track it** | **A.10** |
| **Recovery REPRODUCES (cluster_37 r/m 3.81/4.75) — cluster_16 is not merely atypical** | **A.10** |
| **Half of all clusters (28/28) are bridged mixtures; NO continuous cluster exists in 800–2,500** | **A.10** |
| ~~r/m "envelope"/optimum at 3,600~~ — **WITHDRAWN**, rests on 1 of 5 clusters; r/m anchor was a category error | **A.9** |
| **The Mash proxy distorts diversity SPACING (57% implied vs 2% true) — unusable for targeting** | **A.7** |
| **`ska distance` calibrated as the replacement: every anchor within 13%** | **A.7** |
| **All 91 clusters measured — `cluster_diversity_measured.tsv` supersedes the proxy table** | **A.8** |
| Loosening the cap raises the usable fraction substantially, but recompute against the **measured** range 2,690–4,671 and only for UNIMODAL clusters — A.8's 11.9%→39.4% assumed a cap since superseded | A.8, **A.11** |

**The single most actionable number:** mapping a *tight* cluster to K96243
instead of a within-cluster reference makes **~87% of SNP calls false**
(+630% chr1, +715% chr2), and two independent reference-free callers prove it
is mismapping rather than real divergence. **Corrected 2026-08-10:** the effect
does *not* scale inversely with cluster diversity — cluster_16 carries 7×
cluster_53's diversity and shows nearly the same inflation (+580%/+637%). The
spurious count is roughly constant at ~9,000 positions, so inflation tracks the
**post-Gubbins** SNP count, i.e. the size of the clonal frame, not raw
diversity (A.6). It is worst wherever the clonal frame is small.

**Dating is answered negatively, six-for-six.** Clusters below the ceiling give
small plausible slopes (~3e-07 subs/site/yr); those above give 1.8e-05–4.5e-05,
a 6-fold empty gap. **Refuse to date any cluster above the measured ceiling
(~4,700 ska units).** Diagnose on |slope| **MAGNITUDE only** — sign is noise
(cluster_37 is negative on both replicons and perfectly well-behaved; A.10
retracts A.9's sign criterion). **R² is useless as the flag** three ways over:
0.08 with a negative slope (c48), 0.02 with an inflated one (c0), 0.124 on the
worst-behaved (c8). This inverts §2.12/§6.5 — screen diversity first, temporal
signal second.

---

## 2. PROBE RESULT — fastbaps sub-clustering WORKS, partially

**COMPLETE.** Strains 1/2/3 (1,590 genomes), NJ trees, fastbaps 3 levels.
Scored on the same Mash matrix:

| | PopPUNK strains | **fastbaps L3** |
|---|---|---|
| Clusters | 3 | **319** |
| Median diversity | 8,981 | **1,707** |
| Mean diversity | 9,869 | **2,253** |
| Max diversity | 33,946 | **13,527** |
| Clusters in cap | 0 (0.0%) | **60 (35.1%)** |
| **Genomes in cap** | **0 (0.0%)** | **441 (27.7%)** |

**This is the first method all session to move "genomes in cap" materially.**
Every prior attempt sat at 4–6% (Mash 5.6%, refined PopPUNK 4.2%, single
linkage never held the bound). Sub-clustering cuts median diversity 5.3-fold
and drops max diversity 33,946 → 13,527, so it is breaking the deep bridged
groups, not just shaving small ones off.

**But 72% of genomes remain in sub-clusters too diverse for Gubbins**
(median 1,707 vs a ~1,000 target and Seng's 351–549). The two-level design is
**necessary but not sufficient**.

> **⚠ Requalified 2026-08-10 — this whole table is in proxy units.** Every
> figure above is Mash-derived, and the proxy is now measured to **overestimate
> true mean pairwise SNPs by 1.36×–4.23×**, worse the tighter the cluster
> (Appendix A.5). The L3 median of 1,707 is therefore plausibly in the high
> hundreds in real units — i.e. possibly **already at Seng's band**. The
> "necessary but not sufficient" verdict is *unproven in either direction*, and
> so is 27.7%. Do not re-derive it from a Mash matrix; the only way to settle it
> is to measure mean pairwise distance on an actual sub-cluster alignment.
>
> **And the target itself moved — now settled (A.11).** The measured working
> range is **2,690–4,671 ska units**, not ~1,000. The L3 median of 1,707 proxy
> corrects to roughly 1,250 measured, which is **BELOW the measured floor** — so
> sub-clustering at L3 may already be too fine, and **raising fastbaps levels
> from 3 to 5 would likely make things worse, not better.** Measure the
> sub-clusters directly (`measure_diversity_bp.py`, then `--screen-all` for
> modality) before committing the 42-strain run. Do not raise levels on the
> strength of the proxy median.

### Verdict — REVISED 2026-08-11, and item 2 is now known to be HARMFUL

1. **Enable IQ-TREE** (`config.bp2802.yml`). The probe used NJ trees; fastbaps
   partitions whatever hierarchy it is given, so ML trees should partition
   better. Cost: the 913-genome strain is the long pole, likely overnight.
   **Still stands.**
2. ~~**Raise `fastbaps: levels` from 3 to 5.**~~ **DO NOT.** Measured (A.11b):
   usable coverage runs **L1 14.2% → L2 11.5% → L3 11.5%**, and L3 already
   shatters strains into pairs (median sub-cluster size 2; 206 of 319 are
   singletons or pairs). Going finer moves genomes *out* of the operating range.
   **Use L1.** The 1,707 median that motivated raising levels was a proxy figure
   averaged over mostly-pairs.
3. **NEW — the probe only covered strains 1–3 (1,590 of 2,802 genomes).** Every
   threshold in §0 is calibrated on those three. Running fastbaps on the other 39
   is the gating item (§0 N1).

Re-score after with `compare_partitions_bp.py`; the target is "genomes in cap"
materially above 27.7%.

**What this does NOT change:** Gubbins is still not wired to sub-clusters,
still needs per-sub-cluster medoid references, still needs the version pin and
replicon split (§4). The probe validates the *partition strategy*, not the
pipeline.

Artefacts: `/home/phemarajata/PopPIPE-bp/output/strains/{1,2,3}/fastbaps_clusters.txt`,
membership at `_fastbaps.tsv`. The expensive per-strain products
(`split_kmers.skf`, `align_variants.aln`, `njtree.nwk`, distance matrices) are
cached and will be reused by the full run.

---

## 2b. Nothing is in flight

**PopPIPE probe** — `/home/phemarajata/PopPIPE-bp`, log `probe.log`.
Runs fastbaps sub-clustering on PopPUNK strains 1, 2, 3 (913 + 416 + 261 =
1,590 genomes), IQ-TREE disabled so the RapidNJ tree passes through.
21 jobs. Launched via `run_probe.sh`.

**The question it answers:** does fastbaps sub-clustering bring the largest
strains under the ~1,000 mean-pairwise-SNP cap Gubbins needs?

- **If yes** → commit to the full 42-strain run *with* IQ-TREE enabled
  (`config.bp2802.yml`), then re-key Gubbins to sub-clusters (§4 below).
- **If no** → six methods will have failed the same way. Conclude that a
  diversity-bounded partition may not exist at r/m 7.2, state it as a finding,
  and redirect to sub-national Thailand (§5).

**To check it:**
```
tail -30 /home/phemarajata/PopPIPE-bp/probe.log
ls /home/phemarajata/PopPIPE-bp/output/strains/{1,2,3}/fastbaps_clusters.txt
```

**To score the result** (this is the decisive step):
```
cd /home/phemarajata/Downloads/snp-mod-local-working
# build a membership TSV from the fastbaps outputs, then:
python3 compare_partitions_bp.py \
  --phylip /home/phemarajata/wf-assembly-snps-mod/results_all_2802/Clustering/mash_distances.phylip \
  --partition "poppunk_refined=_ppr.csv:Taxon:Cluster" \
  --partition "fastbaps=<new>.tsv:sample:subcluster"
```
Look at **"genomes in cap"** — currently 4.2% for refined PopPUNK, 5.6% for the
Mash partition. Sub-clustering has to move that materially or it has not worked.

---

## 3. Clustering: five methods, same failure

| Method | Outcome |
|---|---|
| Mash + `max_cluster_size=50` | Size cap, not diversity. 79% over cap, 29 clusters at exactly 50 |
| Single-linkage sweep | **Chained.** Max diversity 2.6–3.5× threshold at every setting |
| PopPUNK (archived, 3,592) | 69% of clusters over cap |
| PopPUNK BGMM (fresh) | **Giant component** — 61% of genomes in one cluster |
| PopPUNK refine (fresh) | Best so far. Score **0.8894** (Seng: 0.8961), largest 913 (32.6%) |

All five fail through **recombinant bridging**, which is what r/m 7.2 predicts
and what Hennart 2022 documented in a *less* recombinogenic organism. The
consistency is itself evidence the difficulty is biological, not tooling.

**Current best partition:** `poppunk_bp/refined/refined_clusters.csv`
(2,802 genomes, 271 clusters, network score 0.8894, density 0.0480,
transitivity 0.9343). 42 strains have ≥6 members, covering 2,430 genomes.

---

## 4. Wiring Gubbins in — what it actually takes

The `gubbins` rule exists (`Snakefile:184`) but is **off the default target
path** (confirmed: it does not appear in the 295-job DAG). This validates
GAP3's inference that PopPIPE's Gubbins sits on the `transmission` branch.

Requesting `output/strains/{strain}/gubbins.final_tree.tre` would run it — but
**do not**, because it is keyed on PopPUNK *strains*, and only 31.9% of those
meet the diversity cap.

**The correct restructure:**
1. Re-key the wildcard from `{strain}` to sub-cluster.
2. `ska map` per sub-cluster (PopPIPE correctly feeds Gubbins
   `map_variants.aln`, not `align_variants.aln` — the coordinate guard holds).
3. **Per-sub-cluster reference**, constrained medoid — re-run
   `pick_cluster_references_bp.py` on the sub-cluster partition.
4. Add the flags PopPIPE lacks: pin Gubbins **≥3.4.3**, pass
   `--invariant-site-correction` explicitly, split by replicon.

---

## 5. If clustering does not converge: the redirect

Decided on **populated metadata fields**, not hope
(`metadata_opportunities_bp.py`):

| Option | Verdict |
|---|---|
| Source attribution | **Dead.** 8 real environmental–clinical links, 6 cases. Wilson 2008 used 1,231 |
| Travel-acquisition inference | **Too thin** — 17 imported cases (0.6%) |
| Travel-acquisition as *validation* | **Useful.** 17 known-origin isolates to test continental assignment; Viberg validated on 1 |
| **Sub-national Thailand** | **The real asset.** 100% have `Subregion`; Thailand = 26 subregions, 1,684 dated genomes, 1965–2025 |

Sub-national Thailand is deeper and broader than Chewapreecha's entire global
study (469 isolates, 30 countries). Country is a bad unit here — 42 labels
collapse to **2.40 effective countries** — but subregion within one country
sidesteps most of that, and Seng 2024 is a direct in-organism precedent
(n=15 per province). **Caveat:** well-powered for *spatial* structure, not
temporal (68% of dated Thai genomes are Seng's 4-year window; 8.20 effective
years overall).

---

## 6. Dating: downgrade, do not drop

Do **not** run BETS on 150 clusters. Run the cheap screen everywhere
(root-to-tip slope, Mantel r/p, tree length — code exists in
`reference_sensitivity_bp.py`), then **BETS on ~12 clusters** spanning the
diversity and time-span range plus negative controls. Same publishable claim,
~5% of the compute.

Outcomes: log BF ≤ −3 = positive evidence of *no* clock (expected; publish the
pass/fail table on the Menardo 2019 template). ≥ +3 = real signal, date it but
check against Tay 2024's tree-extension false positives. Between = inconclusive.

---

## 7. Tools written this session

All stdlib-only, all in `/home/phemarajata/Downloads/snp-mod-local-working`.

| Tool | Purpose |
|---|---|
| `reference_sensitivity_bp.py` | The reference experiment. `plan` / `analyse` / `demo` / `selftest` / `checkaln`. **56 self-tests** |
| `cluster_metadata_join_bp.py` | Join clusters to metadata; cap detection; candidate selection; emits genome list + dates |
| `cluster_diversity_bp.py` | Within-cluster diversity from the Mash matrix (GAP1 §11 Step 0) |
| `pick_cluster_references_bp.py` | Constrained-medoid reference per cluster, with borrow fallback |
| `compare_partitions_bp.py` | Score any partitions on a common genome set |
| `repartition_sweep_bp.py` | Diversity-threshold sweep (documents the chaining failure) |
| `metadata_opportunities_bp.py` | What the metadata supports besides dating |
| `calibrate_mash_snp_bp.py` | True mean pairwise SNPs from existing alignments; calibrates the Mash proxy. **7 self-tests** (added 2026-08-10) |
| `cap_location_bp.py` | Locates the Gubbins diversity cap: union coverage, pooled r/m and tract length per cluster, by caller. **7 self-tests** (added 2026-08-10) |
| `measure_diversity_bp.py` | TRUE core-SNP diversity via `ska build`+`ska distance`, plus `--screen-all` modality screening. **CALIBRATED: `--min-freq 0.0`; mixture if gap/mean>1.0 OR empty_bins>0.45, n≥25. 24 self-tests** |
| `validate_modality_bp.py` | Calibrates the modality thresholds by subsampling clusters of known structure. **3 self-tests** (added 2026-08-11) |
| `reduced_refsens_bp.py` | 4-arm reference-sensitivity (ska_map only). Partition-agnostic (`--membership/--references/--modality`); **parallel arms** (`--threads 4 --reserve-cores 6` → 4×4, measured 1.7× speedup); refuses mixtures. 18 self-tests |
| `fastbaps_L1_references.tsv` | Constrained-medoid references for L1 sub-clusters (n≥30) — closes §4 step 3 |
| `tier0_evidence_bp.py` | **Regenerates every Tier 0 number from disk** — UFBoot sweep, marginal + partial correlations, borrowed-vs-internal reference analysis, shared-bin counts. Emits `tier0_units.tsv`. **13 self-tests** (added 2026-08-11) |
| `collapse_unsupported_bp.py` | **Collapses branches below support into polytomies** — what replaces the withdrawn UFBoot gate. Preserves root-to-tip distances additively; never touches a tip. **18 self-tests** (added 2026-08-11) |
| `pseudoreplication_bp.py` | Metadata concentration (BioProject/year/subregion) per unit vs clonal groups; **`assert_columns()` guards the positional indices**. **12 self-tests** (added 2026-08-11) |
| `mge_hotspot_audit_bp.py` | **Tier 1.2** — shared recombinant-bin enrichment against an independence null, with a lineage control and size-matched subsampling. **10 self-tests** (added 2026-08-11) |
| `callable_variance_bp.py` | **Tier 1.4** — per-genome callable fraction from the full alignments; regresses r/m on its variance. **10 self-tests** (added 2026-08-11) |
| `clonalframe_nu_bp.py` | **Tier 1.3** — ClonalFrameML R/θ, δ, ν decomposition vs diversity-matched controls, plus the Gubbins-vs-CFML concordance check. Rebuilds **uncorrected** starting trees. **17 self-tests** (added 2026-08-11). Env: `cfml` |

**Run `python3 reference_sensitivity_bp.py selftest` after any edit.**
**Run `python3 calibrate_mash_snp_bp.py --selftest` after editing that one.**

Key data products: `cluster_references.tsv`, `cluster_diversity.tsv`,
`cluster_metadata_per_cluster.tsv`, `refsens_cluster0/RESULTS.txt`,
`refsens_cluster53/RESULTS.txt`, `poppunk_bp/refined/refined_clusters.csv`.

---

## 8. Traps that cost real time — do not rediscover these

1. **conda + `set -u`.** `eval "$(conda shell.bash hook)"` activates *base*,
   whose `activate.d/activate-gcc_linux-64.sh` dereferences an unbound
   `SYS_SYSROOT`. Wrap **both** the hook and the activate in `set +u`.
2. **`pgrep -f <script>` matches your own command line.** It falsely reported a
   dead runner as alive twice. Use `ps -eo pid,args` and check for the real
   process.
3. **`generate_ska_alignment.py` defaults to `--k 17`** and always applies
   `--repeat-mask`. On this organism that masked **59%** of chromosome 2 and
   killed Gubbins. Pass `--k 31` (3.5%).
4. **`snp-sites -C` on Gubbins' `filtered_polymorphic_sites.fasta` returns
   `0,0,0,0`.** IQ-TREE accepts `-fconst 0,0,0,0` silently and models nothing.
   Read counts from the **full** alignment.
5. **PopPUNK sanitises `.` → `_` in sample names.** Any name containing a dot
   breaks the rfile↔clusters join. This is what the `_1` suffixes in the old
   PopPIPE `KeyError` actually were.
6. **PopPUNK crashes on multi-component `--output`** — it builds
   `os.path.join(prefix, prefix + '.png')`. Use flat names, run from inside the
   directory.
7. **Independent jobs must not share `set -e`.** One failing arm aborted eleven
   others. Log and continue; make runners resumable.
8. **`snakemake -q` takes an argument** in 7.32 and will swallow the next
   positional target.
9. **`--config key='{"a": false}'` passes `false` as a string** and fails PopPIPE's
   JSON schema. Use a config file.
10. **"Mean pairwise distance" and "count of polymorphic sites" are not the same
    number** and differ by roughly the Watterson factor (≈4.5 at n=50). Validating
    one against the other is what put A.3d's proxy check off by a factor of ~1.9
    *and* inverted its sign. Whenever comparing two diversity figures, check they
    are the same statistic, over the same replicons, before reading the ratio.
11. **`conda` is not on PATH in a non-login shell, and the failure looks like a
    completed run.** The arm scripts call `eval "$(conda shell.bash hook)"`,
    which needs conda already on PATH — true in a login shell, false after a
    reboot or a bare background launch. Every arm then dies with exit 127 in
    about a second, and because the runner logs-and-continues by design (trap 7)
    the whole 12-arm run "finishes" instantly with every arm FAILED. Checking
    only that the runner exited will mislead you. Fix: source
    `<conda>/etc/profile.d/conda.sh` explicitly and verify `command -v conda`
    before handing off — see `refsens_cluster16/resume.sh`, which also
    pre-checks that both envs exist so a missing env fails once, loudly.
12. **The curated metadata TSV has TWO `sample_id` columns** (indices 0 and 16)
    plus a `FASTA_name` column (17), and `csv.DictReader` silently keeps only the
    last. Joining on the DictReader key drops roughly half the collection with no
    error — cluster_53 reports 23 dated / 25-year span instead of the true 41 /
    62. Index by raw column position and join on **all three** key columns,
    stripping the `.fasta` suffix. Source:
    `final_deduped_all_BP_with_locations/megamix_bestshot_cleaned_dropGCF_on_Fdups_APPENDED.tsv`,
    date field `final_collection_dates`. `cluster_metadata_join_bp.py` already
    does this correctly; hand-rolled joins are what break.
13. **Gubbins' per-branch `r/m` median is meaningless in tight clusters.** 43% of
    cluster_53's branches carry r/m exactly 0 — too few SNPs to assign any — so
    the median reports 0.27 while the pooled value is 2.09, which **reverses the
    ordering against cluster_0**. Report pooled r/m, or the median with the
    zero-branch fraction attached. Same caution for block counts: half of
    cluster_53's 299 "recombination blocks" are 3–76 bp. Those are a **mapping-
    caller artefact**: the reference-free caller on the same cluster and
    reference gives 4,604 bp median tracts, and 4,600–5,900 bp at every
    diversity level tested (A.6). Tract length is a property of the caller.
14. **mean ≈ median does NOT mean a cluster is homogeneous.** cluster_48 has
    mean 4,562 and median 4,581 and is a **three-sub-lineage mixture** (pairs at
    ~300/~2,700/~5,400, largest gap 842 SNPs). It was selected on that criterion
    and the criterion was worthless. Screen on the full pairwise distribution —
    largest gap over mean, and count of near-empty histogram bins (A.9 Finding 3).
15. **Summing Gubbins' per-branch masked bases is not "fraction of the genome
    recombined."** It counts shared sites once per branch, so over ~97 branches
    it exceeds 1.0 routinely and reads as false saturation. Take the **union** of
    recombinant intervals across branches — `cap_location_bp.py:union_coverage`.

---

## 9. Why PopPIPE-bp was abandoned (resolved)

Two independent faults, which is why it was hard to diagnose:

1. `combined_rfile.txt` had been **overwritten by a single-genome test run**
   (1 line) while `combined_clusters.csv` still held 3,592 taxa, so
   `Snakefile:25`'s `.loc` dumped every unmatched name into a `KeyError`.
2. **PopPUNK's dot-to-underscore sanitisation** genuinely did mangle names, so
   the naming theory was not wrong — just not the whole story.

Fixed: `config.bp2802.yml` + `rfile.sanitised.txt`, validated by
`check_inputs.py` (reproduces `Snakefile:25` before committing compute).
**Run `bash check_inputs.sh` before any PopPIPE run.**

---

## 10. EVERYTHING WORTH TRYING — ranked backlog

Consolidated from the whole session. Ordering matters where noted. Items marked
**[free]** need no new compute; **[B]** belongs to the methods paper.

### Tier 1 — do these, evidence largely in hand

0. **DONE 2026-08-10 — `cluster_16` ran, 12/12 arms, and it changed the cap.**
   Measured 3,639 whole-genome mean pairwise SNPs. It reproduces all three
   published recombination anchors (r/m 7.2, 78% ever-recombined, ~5 kb tracts)
   on both replicons under two independent callers, while cluster_53 (535)
   under-detects and cluster_0 (9,433) loses contrast. **The derived ~1,000 cap
   sits inside the under-detection regime**; the honest operating point is nearer
   3,000–4,000. Full result and its limits in Appendix A.6.

0. **All 2026-08-10/11 threshold work is COMPLETE — see §0 for the settled
   parameters and the ordered next steps.** Runs: cluster_8, cluster_48,
   cluster_37, cluster_16 (full); 13 reduced; s1_L1_9 and s1_L1_27 (L1
   sub-clusters). Diversity measured for all 91 clusters; modality screened for
   the 2,802-genome partition and for fastbaps L1/L2/L3. **The gating item is now
   N1 in §0: fastbaps has only ever been run on strains 1–3.**

1. **Apply per-cluster references to the pipeline.** `cluster_references.tsv`
   gives a medoid for all 91 multi-genome clusters (57 internal, 28 borrowed
   within Mash 0.005, 6 need ABACAS). The code change is to stop conflating two
   objects: *representative* = centrality only; *reference* = completeness gate,
   then centrality. **Do this BEFORE re-clustering** — a diversity-based
   re-partition turns most of the collection into tight clusters, which is the
   regime where a distant reference makes 87% of calls false. Re-clustering
   first would amplify the artefact rather than confine it.
2. **Audit the Nextflow pipeline for the two silent defects** (§8.3, §8.4):
   does it pass `-k` to `generate_ska_alignment.py`, and where does it read
   `-fconst` counts from? Both fail silently and produce plausible wrong
   numbers. This is independent of everything else and should happen regardless.
3. **Measure the BioProject ICC.** Effective *n* currently spans 672→35
   depending on this one unmeasured number. Compute the fraction of core-SNP
   variance between vs within BioProjects. Days, not months. **Searched for and
   not found: any bacterial-genomics paper treating BioProject as a random
   effect** — this is a genuine Tier 1 contribution, and it generalises well
   beyond this organism.
4. **Tip-state-swap permutation null** — permute country labels across tips,
   hold the tree fixed, re-run `make.simmap`, compare observed transition counts
   and root state against the null. **Then repeat permuting BioProject labels.**
   Needs no new software and is the only handle anyone has on the
   study-of-origin confounder.
5. **Cheap dating screen everywhere + BETS on ~12.** See §6.

### Tier 2 — cheap, novel, take them

6. **[free] Balanced-subsample re-clustering with ARI.** Re-cluster a
   country-balanced and separately a BioProject-balanced subsample; report ARI
   against the full-data partition as a *distribution*. **No bacterial
   precedent exists.** Cite PopPUNK for the ARI machinery, Meirmans 2018 for
   motivation. Hours of work.
7. **Concatenated vs per-replicon phylogeny, compared explicitly.** Never done
   **for any organism**. You are forced into the replicon split by the tooling
   anyway, so the comparison is nearly free. Dillon 2015 supplies the mechanism
   (chromid: lowest mutation rate, highest evolutionary rate).
8. **[free] Publish a K96243 masked-region BED.** None exists. Coordinates do:
   Holden 2004 (16 GIs, 6.1%), Tuanyok 2008 (71 GIs), IslandViewer 4 for both
   replicons. Mirror them — the database froze 2024-09-06 on month-to-month
   funding, so the mirror has independent value. An afternoon.
9. ~~**Third cluster of INTERMEDIATE diversity** for reference sensitivity.~~
   **Promoted to Tier 1 item 0** — it turned out to be the only way to locate
   the diversity cap, not just a dose–response nicety.
10. **Reference-selection alternative: 1-center (minimax)** rather than medoid —
    minimise the *worst* member's distance, since that member is what trips
    `--filter-percentage 25` and is silently dropped. Both columns are already
    in `cluster_references.tsv`; switching criteria needs no recomputation.
11. **Verticall distance as a second recombination arm**, per cluster. Recovered
    temporal signal in 63/83 *K. pneumoniae* lineages vs Gubbins' 42/83. Still a
    preprint, so treat as robustness check, not primary. **Never use Verticall
    *alignment* for anything dated** (dated PMEN1's root to 1701 vs ~1972).
12. **[free] Re-run the genome audit retaining `bioproject_accession`.** The
    original script dropped it, which is why the third dominant Thai BioProject
    stayed unidentified. Cheap and makes the audit reproducible.

### Tier 3 — real but bigger, or blocked

13. **SimBac benchmarking [B].** Nobody has benchmarked any of these tools at
    *B. pseudomallei* parameters on a two-replicon 7.2 Mbp genome. **One
    simulation answers two open questions**: whether the subtree merge is valid
    under recombination, and whether BAPS-family/PopPUNK clusters track clonal
    descent at r/m 7.2. That second question is a documented absence.
14. **The subtree merge under recombination [B].** The genuinely unsolved piece.
    Cite what you currently do not: NJMerge, TreeMerge, and especially **GTM**
    (Smirnov & Warnow 2020, PMID 32299343), whose merge *provably minimises
    topological distance to the guide tree*. **GTM's guarantee is topological
    only** — it fixes "which edges" and leaves the branch-length-unit problem
    untouched. That residual is the actual contribution.
15. **badMIXTURE / bottleneck-vs-admixture test** for the Australian-origin
    question. Chewapreecha names the alternative ("repeated population
    bottlenecks outside Australia, but not within it") and does not exclude it;
    Lawson 2018 shows the two histories are indistinguishable from a bar plot.
    **Searched for and not found: any paper re-examining the Australian-origin
    hypothesis on sampling-bias grounds.** Real opening, real work.
16. **ChromoPainter/fineSTRUCTURE on *Burkholderia*** — absent, feasible
    (4,067 *H. pylori* precedent; van Hal 2022 at 1,128 *E. faecium* is the
    template). Take it **only** if the question is direction and quantity of
    gene flow, which trees structurally cannot answer. It cannot date anything
    and is itself sampling-bias sensitive.

### Do NOT chase these

- **Structured coalescent applied to *B. pseudomallei*** — absent because it is
  a bad idea here and would not run (>15 demes infeasible; you have ~37).
  Filling this gap would be a mistake presented as novelty.
- **ARG methods on bacteria** — ceiling is 23 taxa × 53 loci at ~a week per
  chain. Two orders of magnitude short.
- **Pangenome graphs** — Pandora loses ~11% recall at core SNPs with a 20–30×
  higher error rate; pggb's bacterial ceiling is 500 *complete* genomes.
  The item most likely to look attractive and cost months.
- **Environmental source attribution from THIS dataset** — 8 real links (§5).
  Worth doing only as new sampling.
- **A phylogenetic ESS for discrete traits / inverse-probability tip
  weighting** — genuine statistical holes, but separate statistics projects.
  Name them as future work; label the Kish calculation ad hoc, which it is.

### Reporting — non-negotiable if any of this is published

**STROME-ID items 6.1, 9.1, 12.1, 12.2 and especially 13.2** (sampling fraction
+ cluster-size distribution for cluster-based studies). Compliance across 114 TB
genomic-epidemiology papers averaged **50%** and did not improve after
publication, so reporting them puts the paper in a small minority. Full
checklist in `REVISED_STRATEGY_2026-08.md` §6, including the per-cluster,
per-replicon dating table and the phylogeography items (report the **full ARD
rate matrix** — Chewapreecha reports none, so this is a strict improvement at
no methodological risk).

**And the claims list in §4 of the strategy is the thing to re-read before
writing any abstract.** The most dangerous available conclusion is "lineages
moved from Southeast Asia into Australia" — SAASI shows that is precisely what
the sampling bias manufactures.

---

## 11. SECURITY — RESOLVED (2026-08-10)

A live Microreact API JWT had been committed to the public repo
`github.com/PHemarajata/PopPIPE-bp` in 8 files. **The user reports the token
issue is handled.** Nothing outstanding here; do not re-raise it.

Left on record because it dictates a habit, not a task: the working-tree scrub
never fixed the exposure — only server-side invalidation did. If a credential
is ever committed again, revoke first and rewrite history second.
