# Two questions: the CDC India call, and how to group isolates

Run 2026-08-21 on the Lichtenegger cgMLST profiles, 3,031 genomes, 45 validation.
Scripts `grouping_test_bp.py`, `score_cgmlst_lichtenegger.py`.

---

## 1. Would genomics alone have supported the CDC's India attribution?

**South Asia: yes, strongly. India: no.**

Taking the five 2021 aromatherapy-outbreak genomes and measuring their distance
to every region in the panel, with the outbreak itself held out:

| region | n | min d | median d | mean d |
|---|---|---|---|---|
| **South Asia** | 75 | **0.6403** | **0.7380** | **0.7362** |
| Middle East & North Africa | 3 | 0.6922 | 0.7002 | 0.7315 |
| North America | 79 | 0.6936 | 0.8088 | 0.7981 |
| East Asia & Pacific | 2,718 | 0.7301 | 0.7971 | 0.7984 |
| Sub-Saharan Africa | 30 | 0.7675 | 0.8150 | 0.8086 |
| Europe & Central Asia | 12 | 0.7858 | 0.8048 | 0.7985 |
| Latin America & Caribbean | 92 | 0.8042 | 0.8133 | 0.8133 |

South Asia leads on **all three** statistics, so this is not one lucky neighbour.

| test | result |
|---|---|
| South Asia (n=75) vs all other regions (n=2,934) | median **0.7380 vs 0.7974**, Mann-Whitney **p = 2.8e-34**, rank-biserial effect **0.82** |
| **India (n=56) vs the rest of South Asia (n=19)** | median 0.7375 vs 0.7763, **p = 0.351** |

**A large, highly significant regional signal, and nothing at country level
within that region.**

This independently reproduces the CDC's own conclusion on their own outbreak:
their genomics gave South Asia, and India came from the product supply chain. We
reach the same boundary from a different panel and a different method.

**That is a strong thing for the paper to be able to say.** It converts our
negative result from a limitation of our data into a reproduction of a published
investigation's limit.

**It also corrects something I said earlier.** I described the aromatherapy
strain's d = 0.64 nearest neighbour as "no signal". That was wrong.
**Absolute distance and discriminative signal are different things.** There is no
close relative, but the *ranking* of distances still carries strong regional
information.

## 2. How should isolates be grouped?

Raw accuracy is not comparable across groupings, because a binary split with a
90% majority class scores 90% by saying nothing. The headline statistic is
**Cohen's kappa**, which corrects for chance and therefore also neutralises the
Thailand-overrepresentation worry.

| grouping | classes | best estimator | accuracy | baseline | **kappa** |
|---|---|---|---|---|---|
| **Asia vs non-Asia** | 2 | modal k=20 | **100%** | 60% | **1.000** |
| East vs West hemisphere | 2 | modal k=20 | 95% | 65% | **0.901** |
| **region, 7-way** | 4 present | modal k=20 | 93% | 47% | **0.890** |
| SEA vs non-SEA | 2 | modal k=20 | 74% | 58% | **0.425** |
| country | 15 | nearest neighbour | 21% | 28% | **0.188** |

### Coarser is not automatically better

**SEA vs non-SEA is binary and performs worse than the 7-way region.** So the
question is not granularity. It is whether the boundary follows population
structure.

Your instinct to be suspicious of SEA was right, but the reason is more
interesting than Thailand overrepresentation: **the SEA / non-SEA line cuts
straight through the Asian clade.** India and China are non-SEA but genomically
Asian, so the split asks the data for a boundary it does not contain.

### The 7-way region is the right operating point

Asia vs non-Asia has the higher kappa, but it answers almost nothing: it is one
bit. The 7-way region is at kappa 0.890, only marginally lower, and carries far
more information per call. **Use region as the reported scale, and cite the
binary split as the floor that never fails.**

### "Western Hemisphere strain" is supportable

East vs West hemisphere reaches **kappa 0.901, 95%**. So the Gee 2017 framing
holds up as a *grouping*, even though ST92 spanning seven countries means it does
not hold up as a *country-level* claim. Those are compatible, and worth saying
explicitly since we are contradicting the country reading of the same literature.

## 3. Why the deep splits survive where country does not

Asia vs non-Asia, stratified by nearest-neighbour distance:

| stratum | Asia vs non-Asia | East vs West | region 7-way | country |
|---|---|---|---|---|
| d < 0.05, real relative | **13/13** | 13/13 | 10/13 | **1/13** |
| 0.05 to 0.30 | **8/8** | 8/8 | 6/8 | 2/8 |
| **d >= 0.30, no relative** | **22/22** | 20/22 | 20/22 | 6/22 (luck) |

**Asia vs non-Asia is perfect in every stratum, including 22/22 where no close
relative exists.** That is the *opposite* of the attractor pattern. The attractor
signature is scoring better where there is nothing to match; this scores
perfectly everywhere.

The mechanism: **at large genomic distance, what remains legible is which side of
the species' deepest divergence a genome sits on.** That split is exactly the
Asia / non-Asia one, consistent with Pearson 2009's Australasia / Southeast Asia
separation and Chewapreecha 2017's finding that clusters do not mix across it.
A 70%-divergent neighbour still tells you the right side of a split that old.

Country fails at *every* distance, including 1/13 where a genuine close relative
exists, because lineages span countries (ST92 across seven, ST58 across three).

**So the resolution ceiling is not set by how much data you have. It is set by
how deep the divergence you are asking about is.** Deep splits are readable from
distant relatives. Country is not readable even from close ones.

## 4. An idea that did not work

I expected a hybrid to win: use the modal neighbour when a close relative exists,
fall back to a group-level median-distance test when none does, since the group
test is what recovered South Asia for the aromatherapy strain.

**It lost to plain modal k=20 on every grouping** (region 67% vs 93%, SEA
37% vs 74%). The group test works for a genome with no relatives anywhere, but as
a general estimator its median-distance statistic is dominated by group size and
internal diversity. Recorded so it is not re-attempted.

## 5. What to do with this

1. **Report the granularity ladder as a result**, not a methods choice:
   country 0.19, SEA/non-SEA 0.43, region 0.89, Asia/non-Asia 1.00. The ladder
   shows where the signal stops, and it is more informative than any single
   number.
2. **Report kappa alongside accuracy everywhere.** It is what makes the
   comparison legitimate given a 60 to 65% majority class, and it pre-empts the
   Thailand-overrepresentation objection.
3. **Use the aromatherapy case as the worked example.** It is a published
   outbreak, our result matches the published investigation's own limit, and it
   demonstrates region-yes / country-no on a single strain.
4. **Re-examine the abstention rule.** Abstaining above d = 0.30 would decline 22
   of 43 calls, but those 22 are 22/22 correct on Asia vs non-Asia. **Abstention
   should be scale-dependent**: decline the country call, keep the regional one.
5. n = 43 and the perfect scores are on small numbers. State that, and re-run
   when the panel grows.
