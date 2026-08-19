# Portable handoff — why do three reference genomes break Gubbins?

**Self-contained. Everything needed to continue this on another machine is listed
in §5.** Nothing here depends on the 2,802-genome run continuing.

---

## §0 THE FINDING, AND WHY IT IS WORTH CHASING

Three *B. pseudomallei* reference genomes make Gubbins fail with RAxML
**"Unable to fit model to data"** for every cluster mapped against them. Swap the
reference and the same genomes analyse fine. The three references are, by every
standard QC metric, **indistinguishable from references that work** — so whatever
is wrong is invisible to the tools normally used to vet a reference.

That is the interesting part. If a reference can silently make a whole analysis
unit unanalysable while passing QUAST, ANI and CheckM-style checks, then
reference selection needs a functional test, not just a quality gate.

### The association

| reference | clusters OK | clusters FAILED |
|---|---|---|
| `GCF_003798365_1_Thailand_Ubon_Ratchathani` | **0** | **4** |
| `GCF_026315045_1_Australia_Northern_Territory` | **0** | **1** |
| `GCF_002843645_1_Australia_Northern_Territory` | **0** | **1** |
| all 23 other references used | **28** | **0** |

p ≈ 0.001 for the 4/4 case under a null of the observed 17.6% failure rate
(≈0.026 after crude correction for 26 references tested).

### The controlled experiment (this is the strong evidence)

All six failing clusters were re-run with **only the reference changed** —
identical genomes, identical Gubbins settings (`--min-snps 3 --iterations 5`,
non-hybrid, no starting tree), identical pipeline commit.

**Result: 12/12 replicon-units succeeded. Zero failures.**

| strain | n | failed against | mean Mash | succeeded against | mean Mash |
|---|---|---|---|---|---|
| strain_14 | 31 | GCF_026315045_1 | 0.00030 | GCF_000511915_1 | **0.00589** |
| strain_15 | 30 | GCF_003798365_1 | 0.00359 | GCF_000755945_1 | 0.00361 |
| strain_21 | 13 | GCF_003798365_1 | 0.00339 | GCF_000755905_1 | 0.00353 |
| strain_23 | 12 | GCF_003798365_1 | 0.00376 | GCF_000755945_1 | 0.00390 |
| strain_33 | 7 | GCF_002843645_1 | 0.00205 | GCF_000511915_1 | **0.00548** |
| strain_34 | 7 | GCF_003798365_1 | **0.00041** | GCF_000755905_1 | 0.00357 |

**Three succeeded against a MORE DISTANT reference** — strain_14 at 20× the
distance, strain_33 at 2.7×, strain_34 at 9×. So this is not divergence. The
picker chose the *nearest* complete genome and nearest is what broke.

---

## §1 WHAT IS ALREADY RULED OUT (do not redo these)

Every one of these was measured on the three failing references against 4–23
working ones, and **none separates the two classes**:

| hypothesis | result |
|---|---|
| different species / misidentified | fastANI vs K96243: **99.349–99.504%** for all. Failing refs interleaved with working ones; `GCF_003798365_1` has the 2nd-HIGHEST ANI of those tested |
| poor assembly contiguity | all exactly **2 contigs**, N50 ~4.0 Mb, L50 = 1 |
| wrong genome size | 7.03–7.28 Mb (failing) vs 6.99–7.47 Mb (working) |
| ambiguous bases | **0 non-ACGT** in all three failing refs; some *working* refs have up to 1,000 |
| duplicated replicons | QUAST duplication ratio **1.001–1.002** (working refs 1.002–1.004) |
| misassemblies | failing **67, 72, 77**; working **77, 82, 88, 91** — failures have FEWER |
| genome fraction vs K96243 | 92.5–95.9% vs 95.0–96.3% — overlapping |
| GC content | 68.01–68.14% vs 68.05–68.16% — identical |
| atypical within collection | mean Mash to all 2,802: failing 0.00462–0.00672, working 0.00427–0.00615, collection median 0.00470 — overlapping |
| **cluster** clonality | within-cluster mean Mash: FAIL 0.00038–0.00357 vs OK 0.00008–0.00352. `strain_28` at **0.000081** (most clonal in the run) SUCCEEDED |
| **cluster** size | of five n=7 clusters, 3 succeeded and 2 failed |
| variable site count | `strain_28` OK on **91** variable sites; `strain_14` FAILED on 1,091 |
| alignment missingness | FAIL mean 0.0386 vs OK 0.0413 — failures are *cleaner* |
| invariant-site composition | e.g. strain_23 A/C/G/T = 468,183 / 1,023,694 / 1,030,368 / 469,692 — normal 68.6% GC, all non-zero |

---

## §2 HYPOTHESES STILL OPEN

Ordered by what I would try first.

1. **Repeat / low-complexity structure of the reference.** *B. pseudomallei* is
   68% GC and repeat-rich. If these three carry an unusual repeat architecture,
   snippy's alignment may produce a site pattern RAxML cannot fit even though
   summary statistics look normal. Test: `nucmer --maxmatch` self-alignment,
   count repeat fraction and longest repeat, failing vs working refs. The
   workspace already has `caller_repeat_overlap_bp.py` doing self-alignment
   repeat detection.
2. **Site-pattern pathology in the alignment.** RAxML's ASC_GTRGAMMA with
   `--asc-corr=stamatakis` fails when the pattern matrix is degenerate. Test:
   take a failing alignment (`*.core.full.aln`) and count distinct site
   patterns, singleton sites, and constant-per-base counts; compare with a
   working one of similar n. **This is the most direct route to a mechanism.**
3. **Reproduce outside the pipeline.** Run RAxML directly on the failed
   alignment with the exact Gubbins command line (recoverable from the
   diagnostics log) and read the full error, which the pipeline truncates to
   one line. Then bisect: does it fail with `-m GTRGAMMA` (no ASC)? With
   `--asc-corr=lewis` instead of `stamatakis`? That isolates whether it is the
   ascertainment correction specifically.
4. **Annotation / mobile element content.** Are these three carrying an
   unusually large prophage or ICE that maps oddly? `caller_annotation_overlap_bp.py`
   is the existing tool for this.
5. **Is it Gubbins version-specific?** Pinned to 3.4.3 (`08db3ee`). Would 3.3.5
   or a newer build behave differently? Cheap to test on one failing alignment.

---

## §3 THE DECISIVE NEXT EXPERIMENT

Hypothesis 2/3 combined, on ONE unit, no pipeline needed:

```
strain_23 + GCF_003798365_1  -> FAILS      (alignment preserved, see §5)
strain_23 + GCF_000755945_1  -> SUCCEEDS
```

Same 12 genomes, two alignments, one fails and one does not. Diff their site
patterns. Whatever differs is the mechanism. Everything else about the two runs
is identical.

---

## §4 WHY IT MATTERS BEYOND THIS PROJECT

- **6 of 34 analysis units** were being written off as unanalysable. They are
  not. Recovering them changes the analysable set from 28/34 to 34/34.
- The reference picker ranks candidates by **centrality** (mean, then max, Mash
  distance to cluster members) with completeness as a pass/fail gate. That logic
  is sound and is validated against the manual analysis (36/36 agreement on
  internal-vs-borrowed). But it has **no functional check** — it cannot tell that
  the reference it just picked will break the analysis.
- Suggested fix regardless of mechanism: a **blocklist plus fallback** — on
  Gubbins "Unable to fit model to data", retry with the next-nearest complete
  reference. That is a stated, empirically-calibrated rule with a controlled
  experiment behind it, which is defensible to a reviewer without needing the
  mechanism.

---

## §5 WHAT TO COPY TO THE OTHER MACHINE

All paths relative to `/home/phemarajata/Downloads/snp-mod-local-working`.

**Minimum for hypothesis 2/3 (a few hundred MB):**
- `reftest_work/*/*/strain_23*.core.full.aln` — the WORKING alignment
- the failing alignment: `all35_work/*/*/strain_23*.core.full.aln`
  *(if `all35_work` has been purged, regenerate with `run_wf_reftest.sh` after
  editing `reftest_refs.tsv` to point strain_23 back at `GCF_003798365_1`)*
- the six reference FASTAs named in §0, from
  `/home/phemarajata/Downloads/final_deduped_all_BP_with_locations/`
- `all35_work/*/*/*.diagnostics.log` for a failing unit — contains the exact
  RAxML command line Gubbins used

**For the full picture:**
- `pp2802_out/Summaries/` — `clusters.tsv`, `cluster_references.tsv`,
  `reference_selection.tsv` (per-cluster reference, source, mean/max Mash)
- `mash_matrix_2802.tsv` (82 MB) — all pairwise distances, expensive to recompute
- `reftest_clusters.tsv`, `reftest_refs.tsv`, `run_wf_reftest.sh` — the
  controlled experiment, rerunnable as-is
- the 12 recovered results: `reftest_out/Clusters/*/Gubbins/`

**Tooling:** pipeline at `github.com/PHemarajata/wf-assembly-snps-mod` @ `a28a96c`.
Gubbins pinned to `quay.io/biocontainers/gubbins:3.4.3--py310h5140242_0`.
fastANI lives in the local conda env `snp-phylogeny`; QUAST and BUSCO are in base
and in `bpseudo_eval`.

---

## §6 ONE CAUTION

Everything above rests on **one controlled experiment on six clusters**. It is
strong — 12/12, with the distance relationship running backwards — but it is a
single experiment. Before it becomes a methods claim, confirm the three
references fail on a *different* cluster set, and confirm a working reference
does not fail on the six clusters used here. Both are cheap with
`run_wf_reftest.sh` and a one-line edit to `reftest_refs.tsv`.
