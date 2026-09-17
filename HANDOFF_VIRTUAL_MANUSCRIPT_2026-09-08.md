# Handoff: the virtual manuscript, and a brief for a specialist animation agent

Written 2026-09-08. Read this whole file before touching anything. It exists so a
specialist scientific-animation agent (Manim, anime.js, D3, GSAP) can rebuild or
extend the visual explanation of this project without re-deriving the science and
without introducing numbers that the frozen analysis does not support.

The current deliverable, `VIRTUAL_MANUSCRIPT.html`, is a working artifact, not a
ceiling. Treat every visual specification below as a statement of *what has to be
communicated and why*, not as a design to copy.

---

## 0. The one-paragraph version

*Burkholderia pseudomallei* causes melioidosis, is acquired from soil and water,
and swaps large pieces of DNA between lineages so freely that most of the
difference between any two genomes arrived by swapping rather than by
inheritance. Standard software strips that swapped DNA out before any
evolutionary comparison. **That software only works inside a range of genetic
diversity, and outside the range it does not fail loudly. It returns a clean,
believable, wrong number.** Nobody had measured where the range lies. We measured
it, on 2,340 genomes in 85 analysis groups, and the corrected recombination rate
inside the range is **r/m 7.70**, against **1.99** outside it. We then asked
whether these genomes can tell you where a patient was infected. **Region works.
Country does not**, and we can show exactly why.

---

## 1. Audience and purpose of the visual deliverable

The presentation target is the **APHL Global Health all-country call**:
departmental leadership plus laboratory colleagues, mostly technologists, across
every country with an APHL office. Many are second-language English speakers.
Many are bench scientists rather than bioinformaticians.

Three consequences that drive every design decision:

1. **The presenter has to be able to narrate it live, cold, 100% of the time.**
   If a visual needs a caveat to avoid being misread, the caveat belongs *in* the
   visual, not in the speaker's memory.
2. **Abstract statistical machinery is the failure point.** The presenter has
   said explicitly that the permutation tests, the negative control, and the
   "above ceiling" collapse were the parts they could not explain. Those are the
   places where animation earns its cost.
3. **No PowerPoint.** The deliverable is a single self-contained HTML file that
   opens offline in any browser. Any replacement must keep that property.

---

## 2. Where everything is

| | |
|---|---|
| **Analysis repo** | `/home/phemarajata/Downloads/snp-mod-local-working`, branch `claude/citation-audit-2026-09-03` |
| **Pipeline repo** | `~/wf-assembly-snps-mod`, tag `v1.2.0-mod` |
| **Reported analysis run** | pipeline `v1.0.5-mod` at commit `79ab645`. **Not seed-reproducible**, see §8 |
| **Frozen basis** | `FINAL_BASIS_2026-08-22/` — 85 units, 2,340 genomes |
| **Single source of numeric truth** | `NUMBERS.tsv` — every headline in the paper is a key in this file |
| **Manuscript** | `MANUSCRIPT_DRAFT_2026-09-02.md`, 34 references, all PubMed-verified |
| **Generated tables** | `TABLES.md`, Tables 1 to 5, rebuilt by `make_tables_bp.py` |
| **Generated figures** | `FIGURE1..6*.svg`, each from `make_figureN_bp.py` |
| **Current deliverable** | `VIRTUAL_MANUSCRIPT.html`, 1.72 MB, 14 sections, 11 generated SVGs plus one embedded tree |
| **This handoff's data pack** | `VM_HANDOFF_PACK/` |

### The data pack

```
VM_HANDOFF_PACK/
  VIRTUAL_MANUSCRIPT.html              the current deliverable
  data/                                every frozen input a figure reads
    NUMBERS.tsv                        source of truth for all headline numbers
    GATE1_ALIGNMENT_2026-08-21.tsv     85 units: n, diversity, r/m, Gate 1 class
    PHYLOGEOGRAPHY_ASSOCIATION_FROZEN_2026-08-23.tsv   170 rows, the geography tests
    SPIKEIN_RESULT.txt                 positive control, raw
    TIER2_null.txt                     negative control, raw (see the trap in §8)
    GROUPING_LADDER.tsv                attribution accuracy at 5 geographic scales
    CGMLST_LICHT_ATTRIBUTION.tsv       per-genome attribution calls
    RM_RESULTS_L1_CORRECTED.tsv        per-unit r/m with the outgroup correction
    cluster_diversity_measured.tsv     per-unit diversity, measured
    FINAL_PARTITION.tsv                2,340 rows: genome -> unit
    FINAL_PANEL.tsv                    the panel before partitioning
    L1_GLOBAL_ML_TREE.nwk              86-tip unit-medoid tree (prune 1, see §8)
    L1_GLOBAL_BACKBONE.nwk             strain-level backbone
  figures/   FIGURE1..6 and FIGURE_ATTRIBUTION_CEILING, light variants
  text/      MANUSCRIPT_DRAFT, TABLES.md, GATE1_ALIGNMENT_RESULT, STATE,
             P-writing-prompt.md (style is a hard constraint), AGENT_PROMPT_VIRTUAL_MANUSCRIPT_v2.md
  extracts/
    virtual_manuscript_data.json       every array embedded in the HTML, with a schema
    derive_vm_data.py                  re-derives all of it from source and asserts it matches
```

**Run the derivation check first.** It takes two seconds and tells you the basis
is intact:

```bash
python3 VM_HANDOFF_PACK/extracts/derive_vm_data.py
```

Expected output ends `OK: every embedded dataset reproduces from the frozen basis`.
If it fails, stop and report, because it means a source file moved under the
deliverable.

---

## 3. The manuscript, and how it got here

The paper is **"A measured operating range for recombination detection in
*Burkholderia pseudomallei*, and what it changes about the reported recombination
rate."** Structure: Abstract, Importance, Introduction, Results (6 sections),
Discussion, Methods, then figures, tables and references.

Effort worth knowing about, because it shapes what the visuals may claim:

- **Everything is generated, nothing is drawn.** All five manuscript figures and
  all five tables are produced by scripts that read the frozen basis and **fail
  rather than emit a stale number**. `make_figure2_bp.py` cross-checks its own
  medians against `NUMBERS.tsv` before writing. This is a deliberate response to
  a project history of numbers drifting between documents.
- **The basis was frozen on 2026-08-22** precisely because intermediates had been
  edited in place. `freeze_basis_bp.py` validates it. Quote nothing that
  `NUMBERS.tsv` does not carry.
- **The citation audit.** 34 manuscript references, every one retrieved from
  PubMed in session. One reference had a PMID pointing at a paper on cannabidiol
  and neuroinflammation while its adjacent DOI was correct, which is how it
  survived earlier review.
- **A separate background section (`BP_background_section.md`) is known broken and
  is not part of the paper.** It carries two rival bibliographies; of 277 citation
  marks, 136 resolve to the wrong paper. Do not mine it for facts. See
  `BACKGROUND_BIBLIOGRAPHY_DEFECT_2026-09-04.md`.
- **20 `[CONFIRM]` markers remain in the manuscript body.** All are author
  decisions (word counts, funding, IRB, authorship), none is a missing fact.

### Manuscript figures, and how they map to the presentation

| MS figure | What it is | Presentation status |
|---|---|---|
| **Fig 1** Study flow | CONSORT-style, 2,959 panel genomes to 85 units / 2,340 genomes to 47 in-window units to 46 scorable validation genomes | Not used directly. The numbers appear in the hero stat bar |
| **Fig 2** The operating range | **The paper's central figure.** Pooled r/m against mean pairwise core SNPs, all 85 units, log x, window shaded, Gate 1 classes coloured | Reproduced as the interactive `chart` |
| **Fig 3** Global ML tree | 85 unit medoids, one tip per unit, annotated by dominant country and Gate 1 class | Not used. Superseded for this audience by Fig 6 |
| **Fig 4** Confounder control | Country permutation p against BioProject permutation p, log-log. Only the upper-left is geography | **Section 11's weakest point.** See §5.11 |
| **Fig 5** Detection bounds | Panel A observed r/m against a matched zero-recombination null; Panel B spike-in recovery against donor divergence | Split into two separate animations, `negSvg` and `posSvg` |
| **Fig 6** Global strain tree | All 2,340 genomes, 85 units in 28 strains, circular cladogram, strains shaded | **Embedded inline and themed**, see §5.10 |

---

## 4. The numbers that must never drift

These are the load-bearing values. Every one is in `NUMBERS.tsv` or
`GATE1_ALIGNMENT_2026-08-21.tsv`. A visual that contradicts one of these is a
defect regardless of how good it looks.

**Scale and partition**
- Panel 2,976 assemblies; 2,959 after removing 17 duplicate BioSamples
- **85 analysis units, 2,340 genomes** (this is the analysed basis)
- 43 countries in the analysed set; 50 in the panel
- Unit size median 18, range 7 to 159

**The detection window** — all diversities are **alignment-derived mean pairwise
core SNPs**, never the Mash proxy
- Window **[700, 4700]**, floor bracketed **(588, 755]**, ceiling ≈ **4,700**
- **47 in-window, median r/m 7.70**, IQR 5.72 to 9.41, 1,388 genomes
- **12 below floor, median r/m 1.32**, IQR 1.04 to 2.38, 349 genomes
- **26 above ceiling, median r/m 2.14**, IQR 1.30 to 3.49, 603 genomes
- Median r/m outside the window **1.99**. In/out separation **3.9x**
- Median across all 85 units is **5.51** and is *not* the headline

**How the floor was located, without touching r/m** (this matters, it is the
answer to "isn't that circular?")
- Diversity band 15 to 588: union recombination coverage **4.3%**, median tract **1.12 kb**
- Diversity band 755 to 1,349: union coverage **28.0%**, median tract **3.37 kb**
- Nothing in the collection sits between **588 and 755**, so the floor is a
  bracket and 700 is a round number chosen inside an empty gap
- Insensitive to placement: floor at 588 → 7.70, 700 → 7.70, 755 → 7.74, 840 → 7.78

**Controls**
- Negative: **1,519 simulated no-recombination replicates over 62 unit-replicons.**
  20 replicates (**1.32%**) produced any call. Maximum null r/m ever seen **0.00668**.
  Lowest real observed value **2.85**, highest **14.92**. Separation **427x to 2,234x**
- Positive: 21 implanted 5 kb tracts at the measured donor divergence nu = 0.002,
  **19 recovered, 91%**. Recovery 90 to 100% for any donor more distant

**Tree builder**
- IQ-TREE against RAxML: median ratio 0.988, sign test **p = 0.77**, agreement
- rapidnj against RAxML: median ratio **0.922**, worst 45.5%, 11 of 12 below 1.0,
  **p = 0.0063**. rapidnj systematically underestimates r/m
- 6 units x 2 replicons = 12 comparisons

**Geography and attribution** (validation set = **46 scorable** genomes)
- Country, best estimator `nearest_nb`: **10/46 (22%)**, kappa **0.193**
- Region 7-way, best estimator `modal_k20`: **41/46 (89%)**, kappa **0.832**
- Asia vs not, `modal_k20`: **46/46 (100%)**, kappa **1.000**
- **The estimator is part of the number.** Country's best is `nearest_nb`,
  region's best is `modal_k20`. Mixing them produces a figure belonging to neither
- Per-unit phylogeography over 85 units: **6 geographic (control passes)**,
  12 confounded, 25 null, 5 vacuous control, **37 untestable because single-country**

**Sampling**
- Thailand **1,561 of 2,340 = 66.7%**; China 265; the two together are three quarters
- USA 47, of which **21 sit in one unit** (`strain_4_L1_1`, plus 1 Colombia)
- South Asia carries ~44% of modelled global melioidosis burden and **2.5%** of this panel

---

## 5. Per-visual specification

For each: **the finding**, **why this visual form**, **what exists now**, and
**what a specialist agent should do better**. Section numbers are the deliverable's
own (`data-name` attributes, 14 sections, `a0` to `a12` plus `forward`).

---

### 5.1 `paramSvg` — the parameter chain (section 1, "Why this organism is difficult")

**The finding.** The analysis is a chain of nine steps, and every step's output is
the next step's input: assemblies → Mash distances → PopPUNK strains → fastbaps
level-1 subclusters → analysis units → per-unit reference → core alignment →
Gubbins → r/m. A choice made early propagates all the way down. This is the
structural reason the study exists: nobody had asked what the *measurement step*
requires of the *partitioning step*.

**Why a node-and-edge diagram.** The audience needs to hold the pipeline in mind
for the rest of the talk. A static chain with labelled arrows is the right form
because the claim is about dependency, not about magnitude.

**What exists.** 9 nodes, 8 edges, 640x478. A side module beside it lists every
node and every arrow with its exact label, and selecting an entry isolates it in
the diagram. Data in `extracts/virtual_manuscript_data.json` as `PARAM_NODES`
and `PARAM_EDGES`.

**What to do better.** This is the one place where a *build* animation would help
more than interactivity: reveal the chain one step at a time as the presenter
speaks, then flash the two steps whose relationship the paper measures
(partitioning and Gubbins). Manim's `Create` / `TransformMatchingShapes` on a
directed graph is a natural fit. Keep the side module, because it is what lets the
presenter answer "what was that box again?" without scrolling.

---

### 5.2 The prior-work comparison (section 2, unnamed SVG, 1000x320)

**The finding.** Three prior studies and this one all do the same two things:
divide the population, then remove recombination before measuring. They differ in
what they divide by and how far they divide. **None of them measured whether the
measurement step still works on the pieces they produced.** That single missing
step is the contribution.

The presenter has flagged this as the section they struggled to explain to a
colleague. The difficulty is that the studies are *mostly the same*, and the
audience keeps hearing "they were wrong", which is not the claim.

**Why a shared-spine comparison.** The visual has to make similarity obvious
first and difference obvious second. A four-column table makes everything look
equally different. A shared horizontal spine with per-study annotations makes the
common workflow the figure's subject and the divergence a local deviation.

**What to do better.** This is the highest-value target in the whole deliverable.
Suggested treatment: animate one workflow spine, run all four studies down it
simultaneously as coloured tokens, and let three of them exit at the same point
while this study continues into a "measure the measurable range" step. The
emotional beat is *we did not do something different, we did one more thing*.
A Manim scene with a common track and staggered token movement would land this
far better than the current static panel.

---

### 5.3 `winSvg` — the detection window mechanism (section 3, three states)

**The finding, and the mechanism.** Gubbins finds recombination by looking for a
*local excess of SNP density* against the genome-wide background. That is the
whole trick, and everything follows from it.

- **Below the floor**, the genomes are nearly identical. There are almost no SNPs
  anywhere, including inside the imported piece, so no patch is dense enough to
  stand out. The tool marks nothing. r/m collapses toward zero.
- **Inside the range**, the background carries a moderate scatter and the imported
  piece carries far more, packed into one stretch. The contrast is visible, the
  piece is marked, and its SNPs go into the numerator. **This is the only regime
  where r/m means what it says.**
- **Above the ceiling**, the genomes have been apart so long that SNPs are dense
  *everywhere*. The imported piece is still physically there, but it no longer
  looks unusual, so it is not marked and its SNPs are counted as ordinary
  mutation. That moves recombination from the numerator into the denominator, and
  the ratio falls.

**The collapse is symmetric.** Too similar and too different both produce a low
number, and the number alone cannot tell you which you have, nor separate either
from a group that genuinely recombines less.

**Why this visual form.** The presenter reported the above-ceiling case as the
hardest thing in the talk. The insight is that *the imported piece never changes*
— only the background does. So the visual holds one stretch of genome fixed,
holds the imported segment fixed and highlighted, and varies only the background
SNP density across three states. What the eye is asked to do is judge contrast,
which is exactly what the algorithm does.

**What exists.** A SNP-density track, 1000x300, with three buttons (Too similar /
In the range / Too different) plus Replay. Each state redraws tick marks at a
different background density and prints the verdict: "Not marked. These
differences are counted as ordinary mutation" versus "Marked as recombination.
Counted in the numerator."

**What to do better.** Three things.
1. **Make it continuous.** A slider or a smooth tween across the diversity axis,
   with the r/m readout updating live, would convert three snapshots into one
   mechanism. The audience would see the ratio rise then fall.
2. **Show the numerator and denominator as a physical quantity** — two accumulating
   bars beside the track — so "moves into the denominator" becomes visible rather
   than asserted.
3. **Anchor it to the real axis.** Right now the three states are illustrative.
   Tie state positions to actual diversity values (say 100, 1,500 and 8,000 mean
   pairwise core SNPs) and label them, so the mechanism panel and the data panel
   in §5.4 share a coordinate system.

---

### 5.4 `chart` — all 85 units (section 4, "What the range does to the answer")

**The finding.** Pooled r/m against mean pairwise core SNPs, log x-axis, one point
per unit, 85 points. The in-window band is shaded. Median inside is 7.70, median
outside is 1.99. **This is MS Figure 2 and it is intended to carry the argument
alone.**

**Why a scatter with a shaded band.** The claim is a window, and a window is
literally a region of a one-dimensional axis. There is no better encoding.

**What exists.** 900x470, 85 dots, three toggles: working range on/off, colour by
Gate 1 class on/off, median line on/off. Data is `UNITS` in the JSON extract, five
fields per unit.

**What to do better.** The toggles are good pedagogy and should survive. Two
additions worth making: a **hover readout** naming the unit (currently absent
here though present in other panels), and an animated **"what happens if you move
the floor"** control that sweeps the floor across the bracket and shows the
headline median barely moving (7.70 → 7.70 → 7.74 → 7.78). That last one answers
the sharpest question a statistician in the audience will ask, and the answer is
already computed.

---

### 5.5 `floorSvg` — the twelve groups below the floor (section 5)

**The finding.** All twelve below-floor units, plotted by diversity against
reported r/m. **Ten of the twelve report r/m below 2.5**, against 7.70 for
in-window units. The two exceptions sit closest to the floor, at 535.0 and 587.6
mean pairwise core SNPs, and report 7.598 and 5.867. That is exactly why the floor
is published as a bracket rather than a line.

Named examples, all verified against `GATE1_ALIGNMENT_2026-08-21.tsv`:

| unit | n | mean pairwise core SNPs | r/m |
|---|---|---|---|
| `strain_7_L1_1` | 14 | 15.4 | 0.979 |
| `strain_1_L1_3` | 79 | 40.6 | 1.057 |
| `strain_8_L1_1` | 36 | 42.8 | 1.675 |
| `strain_15_L1_1` | 31 | 113.9 | 2.365 |
| `strain_19_L1_3` | 8 | 121.5 | 2.409 |
| `strain_22_L1_1` | 11 | 211.0 | 1.380 |
| **`strain_4_L1_1`** | **22** | **243.3** | **1.252** |
| `strain_27_L1_1` | 11 | 285.6 | 0.334 |
| `strain_9_L1_1` | 40 | 405.0 | 0.613 |
| `strain_1_L1_7` | 48 | 511.2 | 1.112 |
| `strain_21_L1_1` | 16 | 535.0 | **7.598** |
| `strain_13_L1_1` | 33 | 587.6 | **5.867** |

**`strain_4_L1_1` is the one to lead with for this audience.** It holds 21 of the
47 United States genomes in the analysed set (plus one from Colombia, verified by
joining `curated_L1v4c_clusters.tsv` to `L1v4c_MERGED_METADATA.tsv`). The group a
public health audience most wants a number for is a group where the number is a
detection failure.

**Why this visual form.** Section 5's argument is that a low r/m is the easiest
result in the output to misread. Showing every below-floor unit at once, rather
than two cherry-picked ones, is what makes it an argument instead of an anecdote,
and showing the two that *do not* collapse is what keeps it honest.

**What exists.** 1000x390 scatter, log x from 10 to 1,000, floor line at 700,
a reference line at 7.70, the sub-2.5 zone shaded, four units labelled, hover
tooltips, and an annotation calling out the two exceptions. Data is `BELOW` in the
JSON extract.

**What to do better.** Consider a small-multiple: for three or four of these
units, show the actual SNP-density track from §5.3 at that unit's real diversity,
so the reader connects "this dot is at 15 SNPs" to "here is what 15 SNPs looks
like along a genome". That closes the loop between mechanism and data, which is
currently left to the reader.

---

### 5.6 `splitSvg` — what subdivision costs (section 6)

**The finding, with real numbers.** `strain_1_L1_26` is 153 genomes at 1,310 mean
pairwise core SNPs, r/m 4.47, comfortably in the window. The evidence that it held
two populations was unambiguous, so it was divided. The three children:

| child | n | mean pairwise core SNPs | r/m | Gate 1 |
|---|---|---|---|---|
| `strain_1_L1_26` | 98 | **72** | 1.07 | below floor |
| `strain_1_L1_36` | 47 | 1,477 | 6.68 | in window |
| `strain_1_L1_37` | 8 | 123 | 2.63 | below floor |

**Two of the three landed below the floor.** The division was correct. The cost
was invisible until the floor had been measured.

**Why an animated split.** The point is causal and temporal: one thing becomes
three, and two of them fall out of a region. Animation is doing real work here,
not decoration.

**What to do better.** Two upgrades. First, show the *parent* dissolving into
children rather than boxes sliding, so conservation of genomes is visible
(153 = 98 + 47 + 8). Second, and more valuable, generalise: the standard response
to a diverse group is to keep dividing, so run the recursion two or three levels
and show the in-window population draining away. That is the argument Results
section 4 makes, and no current visual makes it.

**A trap you must not fall into.** The n = 98 child's diversity is **72**,
recomputed on its own membership. The distances file will hand you **1,310**,
which is the unsplit parent's value arriving through a join on unit name. Using it
is wrong by a factor of eighteen and flips that row's Gate 1 class. This is
documented in `GATE1_ALIGNMENT_RESULT_2026-08-21.md` section 7b and it is a named
constant in `make_tables_bp.py` for exactly this reason.

---

### 5.7 `negSvg` and `posSvg` — the two controls (section 7)

**This is the section the presenter said "doesn't work at all. I cannot
successfully explain any of the tests."** The current version is a rewrite that
reframes both as assay controls, which is the audience's native vocabulary.

**The negative control.** Simulate genomes with **zero recombination** using
Seq-Gen, run them through the identical pipeline with identical settings, and see
what the tool reports anyway. Across **1,519 replicates over 62 unit-replicons**,
only **20 replicates (1.32%)** produced any call, and the largest value ever
reported was **0.00668**. Real units sit between **2.85 and 14.92**, so they are
**427x to 2,234x** higher than anything clean input could produce. The tool is not
manufacturing recombination.

**The positive control.** A spike-in. Plant **21 pieces of DNA, 5,000 bases each**,
into real genomes, copied from a donor at **nu = 0.002**, the divergence actually
observed between strains in this collection. **19 of 21 recovered, 90%.** Recovery
stays between 90 and 100% for any donor more distant.

**Why this framing.** Every laboratory technologist in the audience runs a
negative and a positive control every day. The analogy is exact and it is not a
simplification: a no-template control that comes up clean, and a known-positive
that comes back at the expected level. Reframing a permutation-flavoured
simulation as "the no-template control" is the single highest-leverage move in
the deliverable.

**What exists.** `negSvg` (1000x250) shows the input condition, then on button
press draws the distribution of null values against a scale bar with the maximum
marked at 0.00668 and the real range marked separately. `posSvg` (1000x292) shows
21 tiles that resolve to 19 checks and 2 crosses.

**What to do better.** The negative control is still the weakest visual in the
file, because 0.00668 against 2.85 is a 427-fold gap that cannot be drawn to scale
on a linear axis and reads as "one dot near zero" on a log axis. Options worth
trying: a **broken axis with an explicit break marker**; or an animated **zoom-out**
that starts at the null distribution's own scale, then pulls back until the real
data enters the frame, so the audience *feels* the 427x rather than reading it.
The zoom-out is the sort of thing Manim does well and HTML/SVG does badly, and it
is probably the single best argument for bringing in a specialist agent.

For the spike-in, consider showing one implanted tract on the genome track from
§5.3 and letting the detector sweep across it, so "recovered" has a visible
meaning rather than being a tile turning green.

---

### 5.8 The tree-builder comparison (section 8)

**The finding.** Six units by two replicons, 12 comparisons, on the same real
alignments, spanning r/m 1.81 to 14.13. IQ-TREE and RAxML agree (median ratio
0.988, sign test p = 0.77). **rapidnj systematically underestimates r/m** (median
ratio 0.922, worst 45.5%, 11 of 12 ratios below 1.0, p = 0.0063). The third
comparison holds the model fitter constant to isolate the constructor alone.

**Why it matters.** rapidnj is the fast default in several pipelines. A study that
uses it will report a lower recombination rate for a reason that has nothing to do
with biology.

**What exists.** A table only. No custom visual.

**What to do better.** This is under-served. A paired-comparison plot — 12 lines
connecting each unit-replicon's r/m under two builders, with the sign test result
as an annotation — would be more persuasive than the table and takes very little
space. It is a standard form and a specialist agent should just produce it.

---

### 5.9 `mapSvg` — where the genomes come from (section 10)

**The finding.** The collection is severely unbalanced, and the imbalance is the
main limit on what any geographic claim can be. **Thailand is 1,561 of 2,340
(66.7%)**. China adds 265, so two countries are three quarters of everything
analysed. **South Asia carries about 44% of modelled global melioidosis burden and
2.5% of this panel.** 43 countries are represented at all.

**Why a map.** The presenter asked for this directly. Sampling imbalance is
inherently spatial, and a bar chart of country counts hides the fact that entire
high-burden regions are near-empty.

**What exists.** An equirectangular plot, 1000x470, with hand-authored coarse
coastlines (14 polygons in lon/lat, projected by the same `px`/`py` functions),
proportional circles by genome count, region colouring, and hover tooltips. 23 of
27 country circles sit on drawn land; the other four are genuine island nations
(Micronesia, Puerto Rico, Sri Lanka, Aruba). Data is `MAPC`, and a second small
SVG (880x210) carries the burden-versus-sampling comparison.

**What to do better.** The coastlines are hand-drawn and coarse by necessity,
since the artifact cannot fetch external assets. A specialist agent with an
offline projection library could produce a proper equal-area projection with real
boundaries, embedded as inline path data. Beyond fidelity, the strongest upgrade
would be an animated **burden-versus-sampling morph**: draw the map with circles
sized by genome count, then tween the same circles to sizes proportional to
estimated burden. South Asia inflating and Thailand collapsing in one motion makes
the argument in about two seconds.

---

### 5.10 `treeFig` and `amerSvg` — geography (section 11)

**This section carries the applied finding and the presenter has said it is the
one they most need to land.**

#### The tree

`FIGURE6_GLOBAL_STRAIN_TREE.svg` is embedded inline: all 2,340 analysed genomes,
85 units in 28 PopPUNK strains, drawn as a circular cladogram with strains shaded.
It was made themeable by substituting `#555555` → `var(--treeink)` (8,343 refs)
and `#1a1a1a` → `var(--treeink2)` (17 refs), and by neutralising a full-canvas
white background path that otherwise painted a white slab in dark theme.

**Two caveats are structural and must survive any redesign.** Branch lengths are
**not drawn**, because the grafted tree splices two scales that differ by about
133-fold (backbone substitutions per site over the parsnp core, against within-unit
substitutions per site over recombination-filtered sites). And a slice is shaded
only where it is a **real clade**, checked against its MRCA's leaf set, which is
why `strain_1` occupies three separate blocks and one of them is outlined rather
than filled. 29 of 30 blocks are shaded.

**Why it earns its place.** Geography was never an input to PopPUNK, fastbaps or
IQ-TREE, so the recovery of known biogeography is a result rather than an
assumption. The tree is the evidence that the collection has real structure.

#### The Americas panel

**The finding, and it is the best teaching object in the project.** Ten units
contain at least one genome from the Americas, and they fall into two clean kinds:

*Pattern 1, an American genome among its regional relatives* — four units that are
92 to 100% Americas, spanning the US, Colombia, Brazil, Mexico, Puerto Rico,
Ecuador and the Caribbean. `strain_22_L1_1` sits between the patterns at 55%
Americas (6 USA, 5 Viet Nam).

*Pattern 2, an American genome inside an Asian lineage* — five units dominated by
Thailand, Singapore or China, **each carrying exactly one United States genome.**
That is the signature of travel-associated acquisition, and **you can see it
without running any test.**

Full composition is in `AMER_UNITS` in the JSON extract. Worth noting for the
narrative: every Americas-dominated unit falls **outside** the working range, so
r/m is not interpretable for any of them.

**Why this visual form.** The presenter's instruction was explicit: show all ten,
be as visual as possible, and do not make too many points in one table. Composition
bars with a two-colour encoding (Americas / everywhere else) let the two patterns
separate on sight, with no reading required.

**What exists.** 1000x554, ten rows, filterable to either pattern, hover tooltips
per country segment, a dashed separator between patterns, and a right-hand column
carrying Gate 1 class and diversity.

**What to do better.** The strongest possible version connects the bars to the
tree: select a unit and have its clade light up on the circular tree, so "this US
genome sits inside a Thai lineage" is shown topologically rather than as a colour
proportion. That is a linked-view interaction, and it is the thing that would make
the travel-versus-local distinction unforgettable.

#### Why country attribution fails

Region 7-way reaches **41/46 (89%)**, kappa **0.832**. Asia versus not reaches
**46/46**, kappa **1.000**. Country reaches **10/46 (22%)**, kappa **0.193**.

The per-unit phylogeography test over 85 units returns **6 geographic**, 12
confounded, 25 null, 5 vacuous, and **37 untestable because the unit holds only
one country**. That last number is the story: more than a third of the panel
cannot be tested at all, and it is a sampling artifact.

**What to do better.** The presenter said section 7's tests could not be explained;
the same risk applies here. The grouping ladder in `GROUPING_LADDER.tsv` is an
under-used asset: it shows accuracy and kappa at five nested geographic scales for
four estimators. A visual that walks *down* the ladder — country, region, SEA vs
not, Asia vs not, hemisphere — and shows kappa climbing as the question gets
coarser would explain the finding better than any single number. **Use kappa, not
raw accuracy**, because the baselines differ per scale, and label the estimator on
every point.

---

### 5.11 The confounder control (section 11, currently prose only)

**The finding.** BioProject is nested inside country: 95% of BioProjects are
single-country. So a test that controls for BioProject partly controls for the
thing it is trying to detect. Depending on which imperfect control you use, the
count of units with real geographic signal runs from **6 to 24**, and neither
endpoint is defensible. **The range is the finding, not a failure to get an
answer.**

**What exists.** Prose and a callout. MS Figure 4 (country p against BioProject p,
log-log) exists as an SVG but is not used in the deliverable.

**What to do better.** This is abstract and important and currently has no visual.
A specification-curve animation would suit it: show the estimate moving as each
analytical choice is toggled, with the 6-to-24 envelope drawn as a band. That is a
known form in the literature and it communicates "the answer depends on a defensible
choice" better than any prose. Source data is
`PHYLOGEOGRAPHY_ASSOCIATION_FROZEN_2026-08-23.tsv` plus
`BATCH_PROXY_AUDIT_2026-09-02.md` and `CONTROL_SPECIFICATION_2026-09-02.md`.

---

### 5.12 Sections 12 to 14 — reproducibility, contribution, and what more samples would answer

**Reproducibility (section 12).** The pipeline is now byte-reproducible end to end
under `--deterministic true` at smoke-test scale, demonstrated on two full runs
with all ten scientific outputs byte-identical. **Determinism is thread count, not
just seed**: IQ-TREE needs both a seed and one thread; Gubbins is dominated by
threads. Currently a light section. A specialist agent probably should not spend
effort here.

**Contribution (section 13).** The presenter asked for more work on *what was there
versus what is new*. Honest framing: the organism was known to recombine heavily,
the software was known to have limits, and dividing the population before measuring
was already standard practice. **What is new is measuring where the measurement
works, and what that does to the reported rate.** A before/after visual — the
literature's reported r/m range against this study's in-window and out-of-window
values — would make the contribution concrete. Not yet built.

**What more samples would answer (section 14).** The presenter asked to "really
make a point what more samples could answer." The strongest available argument is
quantitative rather than rhetorical: 37 of 85 units are untestable because they
hold a single country, and South Asia carries 44% of burden against 2.5% of the
panel. A visual that shows how many units *become testable* under a modelled
sampling expansion would turn a wish into a plan. The data to model it is in
`FINAL_PARTITION.tsv` joined to metadata. Not yet built, and it is the most
valuable unbuilt thing in the deliverable.

---

## 6. What the current HTML does technically

Worth knowing if you extend rather than replace it.

- Single file, 1.72 MB, no external requests. Fonts fall back to system stacks.
- 14 `<section class="act">` elements with a fixed left rail; `ArrowLeft`/`ArrowRight`
  and `PageUp`/`PageDown` move between sections, so presenter remotes work.
- **Smooth scrolling is off** in all three places it was set (CSS on `html`, and
  two `scrollIntoView` calls), so remote clicks do not queue.
- Theming is token-based across three states: bare `:root` (light),
  `@media (prefers-color-scheme: dark)` guarded by `:root:not([data-theme="light"])`,
  and `:root[data-theme="dark"]`. The embedded tree participates through
  `--treeink` / `--treeink2`.
- Every animation is button-triggered and replayable, and respects
  `prefers-reduced-motion` through a `reduced()` helper.
- All SVGs are hand-authored via a small `E(tag, attrs, text)` helper. No library.
- Verified: no console errors, no horizontal overflow at 375 px, no element
  outside its `viewBox`, no label collisions in the generated panels.

**Writing style is a hard constraint** (`VM_HANDOFF_PACK/text/P-writing-prompt.md`): no em dashes, no
en dashes, no semicolons, no curly quotes, American spelling, median sentence
length ~19 words with 18 to 20% of sentences at 10 words or fewer, and prose that
does not read as AI-assisted. The current file measures median 19, mean 19.2, 18%
short, zero on every prohibited character. **cgMLST is deliberately absent from the
deliverable** at the presenter's instruction, even though it is the manuscript's
attribution basis.

---

## 7. Suggested priority for a specialist agent

Ranked by audience value per unit of effort:

1. **The negative control zoom-out** (§5.7). Biggest comprehension win, and the
   clearest case where Manim beats hand-authored SVG.
2. **The prior-work shared spine** (§5.2). The presenter named this as a failure
   in live explanation.
3. **The continuous detection window** (§5.3), replacing three states with one
   sweep, with numerator and denominator drawn as accumulating quantities.
4. **The grouping ladder** (§5.10), showing kappa climbing as the question coarsens.
5. **Linked tree-and-composition views** for the Americas panel (§5.10).
6. **The burden-versus-sampling morph** on the map (§5.9).
7. **Recursive subdivision** draining the in-window population (§5.6).
8. **The specification curve** for the confounder control (§5.11).
9. **The paired tree-builder plot** (§5.8). Small, standard, currently missing.

---

## 8. Traps that have already cost this project real time

Each of these has bitten at least once. They are in `NUMBERS.tsv` notes, in the
result documents, or in the memory index, but they are worth restating here
because they are exactly the kind of thing a fresh agent reproduces.

- **Two diversity bases exist and they are not interchangeable.** Alignment-derived
  mean pairwise core SNPs is the basis of the window. The Mash proxy overstates
  diversity unevenly (median ratio 1.30, max 17.20) and misplaces 22 of 85 units.
  Quoting a Mash value against the `[700, 4700]` window is the project's signature
  error and it was found in the deliverable's own section 5 table on 2026-09-08.
- **Pairwise means all member pairs, not reference against member.** The reference
  genome only supplies a shared coordinate system. A group of 10 gives 45 pairs;
  40 gives 780. Computed with `np.triu_indices(d.shape[0], 1)`.
- **`TIER2_null.txt` is a mid-run snapshot.** It gives 1,302 replicates over 54
  unit-replicons. The completed run is **1,519 over 62**. Do not summarise the
  file; use the constants. This was the project's seventh instance of reading a
  count off a denominator that was still filling.
- **`L1_GLOBAL_ML_TREE.nwk` carries 86 tips and the frozen basis has 85.** Prune
  the one that is not in the basis, and refuse to draw if the remainder disagrees.
- **The `country` column in `assign_region.tsv` holds region values.** Real country
  is column 9 of `L1v4c_MERGED_METADATA.tsv`.
- **`L1v4c_out/Clusters` is a hybrid directory** holding 88 subdirectories against
  86 units. Globbing it double-counts 153 genomes.
- **The reported analysis run is not seed-reproducible.** It ran unseeded and
  multi-threaded through both Gubbins and IQ-TREE. Re-running under
  `--deterministic true` produces a *different* run rather than validating the
  pinned one. This is stated in the Methods and must not be presented as resolved.
- **Never split a ratio on its own denominator.** A circular test built this way
  produced a false null that survived into two write-ups.
- **A check that passes over an empty set is worse than no check.** Three such
  checks were written in one day before being caught. Every check added since
  asserts a minimum count and was broken on purpose before being trusted.

---

## 9. First actions for the next session

```bash
cd /home/phemarajata/Downloads/snp-mod-local-working
python3 VM_HANDOFF_PACK/extracts/derive_vm_data.py     # must print OK
python3 -m http.server 8731                            # then open VIRTUAL_MANUSCRIPT.html
```

Read `VM_HANDOFF_PACK/text/TABLES.md` and `NUMBERS.tsv` before writing any number
into a visual. If a value you want is not in one of those two files, it is not
established, and the right move is to say so rather than to compute it fresh.
