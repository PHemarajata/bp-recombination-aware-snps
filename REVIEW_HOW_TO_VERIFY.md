# How to verify the headline numbers yourself

Every command below runs against `evidence/` with Python 3 and no third-party
packages. Run them from the package root. Each prints the number the manuscript
claims, so a mismatch is immediately visible.

The point is not that you should trust these commands. It is that the headline
figures are recomputable from small tables, so you can check the reasoning without
taking the pipeline on trust.

---

## 1. The reported basis: 85 units, and the r/m headline of 7.70

```bash
python3 - <<'PY'
import csv, statistics as st
g=[r for r in csv.DictReader(open('evidence/GATE1_ALIGNMENT_2026-08-21.tsv'),delimiter='\t')]
print("units:", len(g))
for cls in ("in","below","above"):
    v=[float(r['rm_corrected']) for r in g if r['gate1_alignment']==cls]
    print(f"  {cls:6} n={len(v):3}  median r/m {st.median(v):.2f}")
allv=[float(r['rm_corrected']) for r in g]
print(f"  all-unit median (NOT reported): {st.median(allv):.2f}")
PY
```

Expect **85 units**, in 47 / 7.70, below 12 / 1.32, above 26 / 2.14, and an all-unit
median of **5.51**. The manuscript reports 7.70 and explicitly declines to report
5.51, on the grounds that it averages measurements with detection failures.

## 2. The Gate 1 window, and that it was not chosen to flatter the result

```bash
python3 - <<'PY'
import csv, statistics as st
g=[r for r in csv.DictReader(open('evidence/GATE1_ALIGNMENT_2026-08-21.tsv'),delimiter='\t')]
d=lambda r: float(r['aln_mean_pairwise_snps'])
inw=sorted(d(r) for r in g if r['gate1_alignment']=='in')
bel=sorted(d(r) for r in g if r['gate1_alignment']=='below')
abv=sorted(d(r) for r in g if r['gate1_alignment']=='above')
print(f"floor bracket: ({max(bel):.1f}, {inw[0]:.1f}]   ceiling ~ ({inw[-1]:.1f}, {min(abv):.1f}]")
for f in (588,700,755,840):
    v=[float(r['rm_corrected']) for r in g if f<=d(r)<=4700]
    print(f"  floor at {f}: n={len(v)}  median r/m {st.median(v):.2f}")
PY
```

Expect a floor bracket of **(587.6, 754.8]** and medians of **7.70, 7.70, 7.74, 7.78**.
The insensitivity is the defence of the judgement call. Challenge 1 in
`WHAT_TO_CHALLENGE.md` is about what it does not defend.

## 3. The Mash proxy really does misplace a quarter of the panel

```bash
python3 -c "
import csv
g=[r for r in csv.DictReader(open('evidence/GATE1_ALIGNMENT_2026-08-21.tsv'),delimiter='\t')]
print('reclassified between metrics:', sum(1 for r in g if r['gate1_alignment']!=r['gate1_mash']), 'of', len(g))
for m in ('gate1_alignment','gate1_mash'):
    from collections import Counter; print(' ',m, dict(Counter(r[m] for r in g)))
"
```

Expect **22 of 85** reclassified, alignment giving 47/12/26 and Mash 47/6/32. This is
error C in the risk register, and the reason the manuscript's Table 3 was wrong until
2026-09-03.

## 4. The attribution ladder

```bash
column -t -s$'\t' evidence/GROUPING_LADDER.tsv
```

Read the `estimator` column, and read it twice. Country is reported at
`nearest_nb` and everything else at `modal_k20`, each being that grouping's best by
kappa. Mixing them is error J. Expect country **10/46** against a 26% baseline, region
**41/46** against 46%, kappa 0.193 and 0.832.

## 5. Where the 46 landed, and the depth control

```bash
cat evidence/DEIDENTIFIED_AGGREGATES.md
```

The per-genome source table is withheld under the data policy; this file carries the
counts every figure is built from. Expect the confusion matrix to show 41 on the
diagonal, all five errors in the two regions with n = 2, only **three of seven regions
ever emitted**, and the depth strata 14/14, 8/10, 19/22 for region against 2/14, 2/10,
6/22 for country.

**The depth strata are the control that matters.** Region holds where no close relative
exists; country improves with distance, which is the signature of falling back on the
modal class rather than reading the genome.

## 6. The null, and the separation

```bash
head -20 evidence/TIER2_null.txt
```

**This file is a mid-run snapshot and must not be summarised.** It shows 1,302
replicates over 54 unit-replicons. The completed run is **1,519 over 62**, recorded in
`repository/REVISED_STRATEGY_2026-08.md` A.11ag, with a maximum null r/m of 0.00668
against observed values of 2.85 to 14.92, i.e. 427x to 2,234x. This is error A, and the
file is included precisely so you can see the trap rather than be protected from it.

## 7. Spike-in recovery and the tree-builder comparison

```bash
head -18 evidence/SPIKEIN_RESULT.txt
head -20 evidence/TREEBUILDER_EQ_RESULT.txt
head -20 evidence/RAPIDNJ_EQ_RESULT.txt
```

Spike-in: 91% recovery at the measured donor divergence of 0.002. Note the rates cannot
be recomputed from the printed integers, because the nu = 0.002 and nu = 0.01 rows show
identical counts and different rates; the counts are rounded summaries across
replicates.

Tree builders: IQ-TREE against RAxML median ratio 0.988 with 7 of 12 below 1.0, against
rapidnj at 0.922 with 11 of 12 below and a two-sided sign test p = 0.0063. The
distance-based builder underestimates r/m systematically. All reported numbers come
from the RAxML arm.

## 8. Regenerate every figure and table

From `repository/`, with the full data present on the analysis workstation:

```bash
python3 make_figure1_bp.py          # study flow, from NUMBERS.tsv
python3 make_figure2_bp.py          # the operating range
python3 make_figure3_bp.py          # global ML tree over unit medoids
python3 make_figure4_bp.py          # the confounder control
python3 make_figure5_bp.py          # detection bounds
python3 make_figure6_bp.py          # genome-level tree by strain
python3 make_figure_attribution_bp.py
python3 make_tables_bp.py           # Tables 1-5, cross-checked against the manuscript
python3 make_itol_bp.py             # iTOL package for figure 3
python3 make_itol_grafted_bp.py     # iTOL package for figure 6
```

Several of these **refuse to run** rather than emit a stale figure: the tree scripts
exit if the pruned tip count disagrees with `NUMBERS.tsv`; `make_tables_bp.py` exits if
any value disagrees with the manuscript; `make_figure_attribution_bp.py` exits if a
grouping is not drawn at its best estimator. Those guards are worth reading as part of
the methods.

## 9. The CI checks

```bash
cd repository && cat .github/workflows/checks.yml
python3 test_phylogeography_bp.py   # unit tests, no data required
python3 audit_defaults_bp.py        # no argparse default points at a specific run
python3 verify_references_bp.py MANUSCRIPT_DRAFT_2026-09-02.md --warn-only
```

Five CI jobs. The last two exist because of errors D and O in the register, and each
closes a class rather than an instance.
