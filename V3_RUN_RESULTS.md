# v3 partition run — results and validation (2026-08-16)

`L1v3_out/`, 91 units, 2,282 genomes. Completed clean: **182/182 replicon-units
Tier1, zero failures**, r/m produced in-pipeline for the first time
(`Summaries/recombination_rm.tsv`). Wall clock ~3.7 h (resumed against the clean
run's cache; SNIPPY mappings reused, all 182 Gubbins re-run because the module
changed).

## The three validation checks — all pass

**1. Unchanged units reproduce v1 exactly.** Of the 61 units whose membership is
identical between the 82-unit v1 partition and v3, **all 61 reproduce their v1
r/m to within 0.01 — zero exceptions.** The in-pipeline `POOL_RECOMBINATION_STATS`
is byte-faithful to the downstream script it replaces. This is the load-bearing
check: the pipeline did not shift under the parts that did not change.

**2. The r/m median moved, and it is explained, not a regression.**

| | median r/m | n |
|---|---|---|
| v1 (82 units) | 6.30 | 82 |
| **v3 (91 units)** | **4.87** | 91 |
| — unchanged units | 6.20 | 61 |
| — merged units | 4.44 | 21 |
| — new units (crossed the threshold) | 1.77 | 9 |

The drop is entirely compositional: the 30 added/changed units are genuinely
more diverse (a rare lineage newly made analysable has more internal divergence
and so a lower r/m). The clean core is unmoved. **Quote r/m on the unchanged /
clean subset (6.20), never the diluted 91-unit median.**

**3. Manual validation holds.** 50 of the 65 manual-matched units are unchanged
in v3 and reproduce v1 exactly; v1's r/m carried the manual-analysis validation
(agreement IQR 1.26-1.64). So that validation transfers to those 50 transitively.
The 15 manual-matched units that v3 merged are no longer the same objects the
manual analysis measured (documented in `L1_PARTITION_V2.md`); r/m comparisons
against manual values must be restricted to the 50.

## Coherence: the honest part

**29 of 91 units carry a >=1,000-substitution surviving branch, up from 20 of
82.** Merging did not fix the divergent-member problem — that was never its job —
and the newly-analysable small units are inherently more divergent, so the count
rose. Breakdown of the 29: 13 unchanged (pre-existing), 12 merged, 4 new.

This is not a v3 defect; it is the same partition-coherence issue
(`rm-spread-is-divergent-members`) seen at higher coverage. The consequence is
unchanged: **restrict biological r/m claims to units without a large surviving
branch**, using the `max_kept_branch_len` column. v3 makes that filter more
necessary, not less, because it analyses more marginal units — which is the
correct trade for not discarding 26% of the collection.

## Verdict

**v3 is sound to build the additions round on.** The clean core is byte-identical
to the validated v1; the median shift is compositional and understood; coherence
is controlled by an existing column rather than by deletion. Nothing here argues
for reverting to v1's delete-the-small-units behaviour.

## Downstream regenerated on v3

`L1v3_ASSIGNMENTS.tsv` — 2,282 genomes in 91 units, country known for 99.9%,
31 countries. Thailand is 70.2% of known-country genomes (was 70.4% at v1), so
the collection's dominant bias is unchanged by the fix.

`L1v3_PHYLOGEOGRAPHY_ASSOCIATION.tsv` — 91 units tested. Country: 43 testable,
**23 clustered at p<=0.05 (53%)**. BioProject: 88 testable, 24 clustered (27%).
The country signal is not weakened by the added units.

**A near-miss worth recording.** The first run of the phylogeography script
reported "units tested: 82" against a 91-unit partition. `--assignments` was
passed, but `--trees` silently defaulted to `L1_out/Clusters` — the **v1**
output — so it joined v3 assignments to v1 trees and produced entirely plausible
numbers (21 of 40 clustered, close to the real 23 of 43). Caught only by noticing
the unit count. **Both `--assignments` and `--trees` must be repointed together;
the default is v1.**

## Global tree on 91 units — the headline survives and strengthens

**strain_9 still holds the longest internal branch in the tree** at 0.09549,
support 100/100, against 0.07838 for the runner-up (strain_19). The stem is
shorter than v1's 0.11790 because the clade now has **three** members, not two:
`strain_9_L1_7` crossed the threshold in v3 and joined. A shared stem shortens as
more diversity sits inside it; the gap to the runner-up is still decisive.

The three load-bearing units are byte-identical in membership to v1 —
`strain_9_L1_4` (n=13), `strain_9_L1_5` (n=7), `strain_20_L1_1` (n=11) — so every
interpretation built on them carries over unchanged.

### strain_9_L1_7 — a third Americas unit that v1 could not see

n=7, deleted by the double size filter in v1, analysable in v3:

| genome | origin | subregion | year |
|---|---|---|---|
| GCF_000959265 | Ecuador | — | 1962 |
| GCF_002111085 | Ecuador | — | 1960 |
| GCF_002110925 | USA | Texas | 2004 |
| GCF_002111105 | USA | California | 2007 |
| GCF_002111205 | USA | California | 2013 |
| GCF_013265695 | USA | Texas | 2018 |
| GCF_002111145 | Costa Rica | Arizona ex Costa Rica | 2009 |

**Four mainland-US cases with no recorded travel** (Texas x2, California x2)
clustering with two Ecuadorian isolates from 1960-62 and one Costa Rica travel
case. Either these are US-acquired from a Western Hemisphere lineage, or their
travel histories were never captured — and it was unanalysable until the size
filter was fixed. Mainland-US genomes in the analysis rise from 11 to 15.

Note `max_kept_branch_len` = 1595 for this unit, so its r/m (1.38) is depressed by
a divergent member and should not be read as a biological rate.

## What still needs doing

1. Re-export deliverables marked as superseding the 82-unit set.
2. Merge the 18 staged assemblies + the 205 externally-assembled genomes, then
   re-partition (the additions round).
3. `strain_9_L1_2` (Mississippi, n=5) and `strain_9_L1_8` (Mexico, n=6) remain
   assign-only — they still need the additions to cross the threshold.
