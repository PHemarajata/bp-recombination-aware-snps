# cgMLST scheme concordance — the swap changed nothing

2026-08-21. Closes `HANDOFF_2026-08-21_EVENING.md` §5 item 5. Turns the mid-project
scheme swap from a loose end into a robustness result.

**Both profile sets were scored through the same validated scorer**
(`score_accessory_bp.py --distance cgmlst`, which reproduces
`CGMLST_LICHT_ATTRIBUTION.tsv` with 0 mismatches), so nothing but the scheme
differs.

| | PubMLST scheme 2 | Lichtenegger v1.1 |
|---|---|---|
| status | unpublished, "subject to change" | published, JCM 2021 |
| loci | 4,089 | 4,221 |
| genomes profiled | 2,976 | 3,033 |

---

## The comparison, restricted to the 30 validation genomes scored under both

| scale | estimator | PubMLST | Lichtenegger |
|---|---|---|---|
| country | nearest neighbour | 0/30 | 1/30 |
| country | modal k=5 / k=10 / k=20 | 0/30 | 0/30 |
| **region** | nearest neighbour | 23/30 | 25/30 |
| **region** | **modal k=20** | **28/30 (93%)** | **28/30 (93%)** |

- Nearest-neighbour distances correlate between schemes at **Pearson r = +0.999**.
- The two schemes pick the **same nearest-neighbour genome** for 20/30.
- They give the **same predicted label** for 25/30 at country, 28/30 at region.

**Country fails identically under both. Region is 93% under both, to the
genome.** Two independently constructed schemes differing by 132 loci give the
same answer, which is about as direct a robustness check as this project can run.

---

## The correction this forces

The full Lichtenegger run scores country **10/46 (22%, nearest neighbour)** while
the PubMLST run scored **0/30**. That gap is easy to misread as the new scheme
recovering signal. It does not.

**On the shared 30 genomes the two schemes give 1/30 and 0/30.** The entire
apparent improvement comes from the **13 validation genomes added in the same
batch** (India 6, Thailand 4, Australia 2, Trinidad and Tobago 1) — the first
validation genomes from countries where the panel actually holds references.

So the honest attribution of the change is: **the validation set expansion moved
the number; the scheme swap did not.** Anywhere the two runs are compared, say
which of the two changed. They were changed at the same time, which is exactly
the confound this note exists to unpick.

This also means the earlier PubMLST-scheme results are not superseded in
substance — they agree. Cite Lichtenegger because it is published and pinned,
not because it performed better.

---

## Reproduce

```bash
python3 score_accessory_bp.py --distance cgmlst --profiles cgmlst_results/results_alleles.tsv --out-prefix accessory_bp/ATTR_PUBMLST
```

Outputs: `accessory_bp/ATTR_PUBMLST.tsv` (60 rows), against
`accessory_bp/ATTR_CGMLST.tsv` (86 rows) for the Lichtenegger scheme.
