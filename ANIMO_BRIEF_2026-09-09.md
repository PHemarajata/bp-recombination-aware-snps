# Animation brief for the virtual manuscript

Written 2026-09-09. This is the continuity artifact between render sessions.
It supersedes the per-visual specifications in
`HANDOFF_VIRTUAL_MANUSCRIPT_2026-09-08.md`, which remains the reference for the
science, the traps and the file's technical construction. **Three of that file's
claims are corrected in section 3 below. Read those before anything else.**

**Treat every visual specification here as a statement of what has to be
communicated and why, not as a design to copy. If the data does not support a
described shape, say so and propose what it does support.** That instruction is
in writing because it is what produced the honest version of the tree-builder
section rather than a fabricated one.

Keep this file updated as builds land. It is the only thing that carries context
between sessions.

**If you are here to revise the five delivered clips, go straight to section 11.**
It is self-contained: the real beat map of every clip read off the rendered MP4s,
what to change, what not to touch, and the order to work in. The narration is
already re-timed in `narration_v2/` and must not be re-derived.

---

## 0. How to work with this

**Paths, not pastes.** Everything is on disk in this repository, and the working
copy of the deliverable is 1.72 MB. Do not paste it into a message. Extract the
script block, grep it, screenshot sections in headless Chrome.

```
repo         /home/phemarajata/Downloads/snp-mod-local-working
deliverable  VIRTUAL_MANUSCRIPT.html
brief        ANIMO_BRIEF_2026-09-09.md            (this file)
reference    HANDOFF_VIRTUAL_MANUSCRIPT_2026-09-08.md
pack         VM_HANDOFF_PACK/                      data, text, figures, extracts
```

**If this session is not running on that machine, you have `ANIMO_PACK/`
instead.** It is the same pack minus four data files and the derivation script,
and its README says exactly what was removed and why. Nothing in section 7 needs
any of them. `VIRTUAL_MANUSCRIPT.html` is in it and is unchanged, because the
deliverable itself carries no genome identifiers.

*Burkholderia pseudomallei* is a US Tier 1 Select Agent and the study metadata
joins accession to isolation location, collection date and exposure label, which
is re-identifiable for rare cases. The repository has never tracked isolate-level
data. **If a visual seems to need a per-genome table, stop and ask rather than
looking for a way around it.** The answer is usually an aggregate that carries
the same information without the join.

**Batch the audit, serialize the builds.** One pass over everything to rank what
is broken and what is buildable, then build one at a time. Feedback comes after
the first build, because the palette and idiom decisions there should propagate.

**Refusal is a valid answer.** If a described visual is not supported by the
data, the correct output is a short note saying so plus a proposal for what the
data does support. That is worth more than a built figure that overstates.

**Division of labor, as agreed.** Claude Code takes HTML surgery, the shared
JavaScript layer, the verification harness, prose and style constraints, and
anything repository-shaped. Animo takes the motion, and the judgment about
whether motion is the answer at all. Reserve Manim for what HTML does badly,
meaning continuous zoom across orders of magnitude, camera moves, morphing
between coordinate systems, and 3D. Everything else stays native SVG and
JavaScript, because native is what keeps theming, the replay button, presenter
remote keys, reduced motion and the file size.

**Motion is often not the answer, and one proven alternative is already in
hand.** The strongest idiom found so far is not an animation. It is a toggle that
hides an annotation so the audience tries and fails to find the imported piece
themselves. Reuse that pattern wherever a figure's real job is to make a reader
experience a difficulty rather than watch one.

**Run this before touching anything.** It takes two seconds and confirms the
basis is intact.

```bash
python3 VM_HANDOFF_PACK/extracts/derive_vm_data.py
```

It must end `OK: every embedded dataset reproduces from the frozen basis`. If it
fails, stop and report, because a source file has moved under the deliverable.

---

## 1. The one-paragraph version

*Burkholderia pseudomallei* causes melioidosis, is acquired from soil and water,
and swaps large pieces of DNA between lineages so freely that most of the
difference between any two genomes arrived by swapping rather than by
inheritance. Standard software strips that swapped DNA out before any
evolutionary comparison. That software only works inside a range of genetic
diversity, and outside the range it does not fail loudly. It returns a clean,
believable, wrong number. Nobody had measured where the range lies. We measured
it, on 2,340 genomes in 85 analysis groups, and the corrected recombination rate
inside the range is r/m 7.70, against 1.99 outside it. We then asked whether
these genomes can tell you where a patient was infected. Region works. Country
does not, and we can show exactly why.

---

## 2. Audience

The presentation target is the APHL Global Health all-country call. Departmental
leadership plus laboratory colleagues, mostly technologists, across every country
with an APHL office. Many are second-language English speakers. Many are bench
scientists rather than bioinformaticians.

Three consequences that drive every design decision:

1. **The presenter has to narrate it live, cold, every time.** If a visual needs
   a caveat to avoid being misread, the caveat belongs in the visual.
2. **Abstract statistical machinery is the failure point.** The presenter has
   said explicitly that the permutation tests, the negative control and the above
   ceiling collapse were the parts they could not explain. Those are where
   animation earns its cost.
3. **No PowerPoint.** A single self-contained HTML file that opens offline in any
   browser. Any replacement must keep that property.

---

## 3. Corrections to the 2026-09-08 handoff

Two of these came out of the first render session's audit. All three are
confirmed against source in this repository.

### 3.1 The grouping ladder does not climb monotonically. The old brief said it did.

Section 7 item 4 of the previous handoff asked for a visual "showing kappa
climbing as the question coarsens". **It does not climb.** Verified in
`GROUPING_LADDER.tsv`, 20 rows, all checked:

| grouping | classes present | best estimator | kappa | accuracy | baseline |
|---|---|---|---|---|---|
| country | 16 | nearest neighbor | 0.193 | 22% | 26% |
| region | 5 | majority of 20 nearest | **0.832** | 89% | 46% |
| Southeast Asia versus not | 2 | majority of 20 nearest | **0.461** | 76% | 59% |
| Asia versus not | 2 | majority of 20 nearest | 1.000 | 100% | 59% |
| East versus West hemisphere | 2 | majority of 20 nearest | 0.909 | 96% | 63% |

A two-class question scores below a five-class one. **The non-monotonicity is the
finding, not noise.** Coarser is not automatically easier. What matters is whether
the boundary is one the data actually draws, and the Southeast Asian boundary is
not. Any visual that animates a rising curve here is animating something false.

Two labeling traps live in this table. The region scheme is seven-way, but only
**five** of the seven regions appear in the 46-genome validation set, which is why
`NUMBERS.tsv` records five classes against a label that says seven. And **country
and region have different best estimators**, so a country number and a region
number must never be compared unless both carry their estimator on screen.

### 3.2 The tree-builder comparison data does exist. It was missing from the pack, not from the project.

The first audit reported that the 12 per-comparison values were unavailable and
only summary statistics existed. That was correct about
`VM_HANDOFF_PACK/data/` and wrong about the project. Both files are complete and
have now been copied into the pack:

```
VM_HANDOFF_PACK/data/TREEBUILDER_EQ_RESULT.txt   RAxML against IQ-TREE, 12 rows
VM_HANDOFF_PACK/data/RAPIDNJ_EQ_RESULT.txt       RAxML against rapidnj, 12 rows
```

Each carries unit, replicon, both r/m values, the ratio, both union coverage
percentages and a tract length delta, for all 12 comparisons. The paired plot
described in section 7.9 is buildable exactly as specified.

This is a packaging failure and the lesson generalizes. When a described visual
looks unbuildable, check whether the file is absent from the pack rather than
absent from the project, and ask.

### 3.3 The embedded tree costs 684 KB in one duplicated attribute, and that is Claude Code's job

`VIRTUAL_MANUSCRIPT.html` is 1,720,664 bytes. **8,343 elements carry the
identical 74-character inline style attribute** `fill: none; stroke:
var(--treeink); stroke-opacity: 0.9; stroke-width: 0.3`. That is 684,126 bytes,
or 40 percent of the file, expressible as one CSS rule.

Not yet applied to the working copy. It is repository surgery and belongs to
Claude Code, and it is queued. Do not spend a render session on it. It is
recorded here so the file size is not mistaken for irreducible.

### 3.4 Resolutions from the 2026-09-09 audit. Read this if you ran the audit before.

Your first audit raised three questions and found one real defect. All four are
resolved. You are cleared to build, starting at 7.1.

- **Q1, 7.16 cited a withheld file.** Confirmed stale citation, not a blocked
  visual. Source 7.16 from `PHYLOGEOGRAPHY_ASSOCIATION_FROZEN_2026-08-23.tsv`,
  where `interpretation == "untestable: single-valued"` gives 37 exactly. The
  brief's 7.16 Data line is corrected. Do not ask for the partition.
- **Q2, the two shipped newicks were the wrong run.** Confirmed. `L1_GLOBAL_ML_TREE.nwk`
  and `L1_GLOBAL_BACKBONE.nwk` were the 88-unit A100 control run. Both removed
  from the pack. The reported-basis tree is now shipped as
  `data/global_ml_tree_86tip.treefile`, 86 tips, all 85 basis units plus 1 to
  prune, no accessions. The section 9 trap is rewritten.
- **Q3, the explorer and export were not in the pack.** They live at the repo
  root and are read in place, paths in section 4. The 7.5 event contract is now
  in section 4, verbatim. The figures shipped are the light renders, and the dark
  ones are not a missing set, see section 4.
- **The 7.16 section 14 defect you found.** Confirmed and this was the real one.
  The deliverable claimed no group sits "between 535 and 1,265," which is false,
  ten units sit there. The range was stale ska units relabeled as alignment. Fixed
  to the true alignment bracket **(588, 755]** in the deliverable and in the
  manuscript, methods and strategy documents. The analysis never depended on it
  and did not move. Build the static current counts only, 37 of 85 untestable,
  and do not draw the sampling-expansion projection, which was never computed.

Two small drifts you flagged, both real, both author-owned and not blocking:
the rapidnj-versus-IQ-TREE worst case reads 51.8 in `TABLES.md` and 51.6 in the
manuscript, reconciled in that table's own note. And "up to 46 percent" rounds
45.5 in section 13. Pick one of each for any figure. The headline rapidnj number,
45.5 percent against RAxML, is not in doubt.

Your judgments were adopted. Hidden annotation on section 5 yes, on the Americas
and the tree builder no, and your section 3 candidate is a good one. The map morph
is refused as you proposed, replaced by the two-region opposed bars on the panel
denominator with a static locator kept separate. Motion earns its cost in four
visuals, 7.1, 7.12, 7.3 and the short 7.7 morph, plus the 7.13 camera move.

---

## 4. Where everything is

| | |
|---|---|
| Analysis repo | `/home/phemarajata/Downloads/snp-mod-local-working`, branch `claude/citation-audit-2026-09-03` |
| Pipeline repo | `~/wf-assembly-snps-mod`, tag `v1.2.0-mod` |
| Reported run | pipeline `v1.0.5-mod` at commit `79ab645`. Not seed-reproducible, see section 9 |
| Frozen basis | `FINAL_BASIS_2026-08-22/`, 85 units, 2,340 genomes |
| Single source of numeric truth | `NUMBERS.tsv`. Every headline is a key in this file |
| Manuscript | `MANUSCRIPT_DRAFT_2026-09-02.md`, 34 references, all PubMed-verified |
| Generated tables | `TABLES.md`, Tables 1 to 5, from `make_tables_bp.py` |
| Generated figures | `FIGURE1..6*.svg`, each from `make_figureN_bp.py` |
| Deliverable | `VIRTUAL_MANUSCRIPT.html`, 14 sections, 11 generated SVGs plus one embedded tree |

### The pack, as of today

```
VM_HANDOFF_PACK/
  VIRTUAL_MANUSCRIPT.html
  data/
    NUMBERS.tsv                       source of truth for all headline numbers
    GATE1_ALIGNMENT_2026-08-21.tsv    85 units: n, diversity, r/m, Gate 1 class
    PHYLOGEOGRAPHY_ASSOCIATION_FROZEN_2026-08-23.tsv   the geography tests
    SPIKEIN_RESULT.txt                positive control, raw
    TIER2_null.txt                    negative control, raw. See the trap in 9
    GROUPING_LADDER.tsv               attribution at 5 geographic scales
    CGMLST_LICHT_ATTRIBUTION.tsv      NOT SHIPPED. exposure join
    RM_RESULTS_L1_CORRECTED.tsv       NOT SHIPPED. accession plus country.
                                      Per-unit r/m is in GATE1_ALIGNMENT instead
    cluster_diversity_measured.tsv    per-unit diversity, measured
    FINAL_PARTITION.tsv               NOT SHIPPED. genome to unit
    FINAL_PANEL.tsv                   NOT SHIPPED. the re-identification surface
    global_ml_tree_86tip.treefile     NEW 2026-09-09. The reported-basis unit
                                      tree, 86 tips, all 85 basis units plus 1 to
                                      prune. This replaces the two files below,
                                      which were the wrong run. See the trap in 9
    L1_GLOBAL_ML_TREE.nwk             REMOVED 2026-09-09. Was the A100 control run
    L1_GLOBAL_BACKBONE.nwk            REMOVED 2026-09-09. Was the A100 control run
    TREEBUILDER_EQ_RESULT.txt         NEW. 12 RAxML against IQ-TREE comparisons
    RAPIDNJ_EQ_RESULT.txt             NEW. 12 RAxML against rapidnj comparisons
  figures/    FIGURE1..6 and FIGURE_ATTRIBUTION_CEILING. These are the light
              renders. Dark renders come from make_figureN_bp.py --dark and are
              not shipped, because the deliverable themes through CSS tokens
              rather than by swapping SVG files. Not a missing set
  text/       MANUSCRIPT_DRAFT, TABLES.md, GATE1_ALIGNMENT_RESULT, STATE,
              P-writing-prompt.md (style is a hard constraint),
              AGENT_PROMPT_VIRTUAL_MANUSCRIPT_v2.md,
              CONTROL_SPECIFICATION_2026-09-02.md    NEW
              BATCH_PROXY_AUDIT_2026-09-02.md        NEW
  extracts/
    virtual_manuscript_data.json      every array embedded in the HTML, schemed
    derive_vm_data.py                 NOT SHIPPED. reads two withheld tables
```

**Four data files and one script are marked NOT SHIPPED above.** They join a
genome accession to geography or exposure, and `ANIMO_PACK/README.md` says why.
No entry in section 7 needs one. `L1v4c_MERGED_METADATA.tsv` and
`assign_region.tsv` are named later in this file for provenance only and are not
shipped either. **If a visual seems to need one of them, stop and ask.** The
answer is usually an aggregate that carries the same information without the
join, which is how the reviewer package handled the same problem.

One file the deliverable needs and the pack does not carry, because it is 100 KB
and only the tree work wants it:

```
L1v4c_out/global_grafted_chr1.treefile   2,352 tips. Prune to the 2,340 in the basis
```

### Built 2026-09-09, at the repo root, NOT in this pack

```
TREE_EXPLORER.html          the interactive global tree, see 7.13
AUSPICE_MICROREACT/         the same tree for Microreact and Auspice, plus a
                            2,340-row metadata TSV and a README carrying the
                            branch-length and r/m caveats
```

**These are not in the pack on purpose.** They carry 2,064 genome accessions
joined to country, BioProject and collection date, no exposure and no isolation
location, and the pack is kept clean enough to leave the machine. **Do not copy
them into the pack.** If this session is running on the analysis machine, read
them in place at their absolute paths:

```
/home/phemarajata/Downloads/snp-mod-local-working/TREE_EXPLORER.html
/home/phemarajata/Downloads/snp-mod-local-working/AUSPICE_MICROREACT/
```

Both are generated and both refuse to write on a count that disagrees with
`NUMBERS.tsv`. The Microreact export splits r/m across two mutually exclusive
columns, `rm_measured` and `rm_reported_but_not_interpretable`, so an external
viewer cannot color a measurement and a detection failure on one scale.

### Video edition, built 2026-09-09

Animo delivered five rendered animations (7.1, 7.3, 7.7, 7.9, 7.12) as 1080p60
MP4s, verified against the frozen basis. They are embedded in a separate file,
`VIRTUAL_MANUSCRIPT_VIDEO.html`, about 22 MB, which is the interactive deliverable
plus the five videos as base64 data URIs, each using its still as the poster so
every section shows a complete final frame before play. The lean interactive
`VIRTUAL_MANUSCRIPT.html` is unchanged and stays the primary file. The videos sit
alongside the existing interactive visuals, and 7.9 and 7.12 gain a visual they
did not have. Animo source and stills are in
`~/Downloads/ANIMO_DELIVERABLES_2026-09-09/`. The video edition is regenerated by `make_virtual_manuscript_video_bp.py`, which rebuilds it byte-for-byte and fails rather than dropping or misplacing a video. The interactive `VIRTUAL_MANUSCRIPT.html` is hand-authored source and has no generator.

**The event contract for 7.5 linkage, verbatim from `TREE_EXPLORER.html`.** On
selecting a unit it dispatches on `document`:

```js
document.dispatchEvent(new CustomEvent("unitselect", {detail: u}));   // u is the unit name string, e.g. "strain_4_L1_1"
```

It listens on `document` for the reverse, and highlights plus zooms to the unit:

```js
document.addEventListener("unithighlight", e => { /* e.detail is the unit name string */ });
```

So the Americas panel in 7.5 highlights a clade by dispatching `unithighlight`
with the unit name, and learns what the user clicked in the tree by listening for
`unitselect`. The unit name is the only payload, and it matches the `unit` column
everywhere in the data.

---

## 5. The numbers that must not drift

Every one is in `NUMBERS.tsv` or `GATE1_ALIGNMENT_2026-08-21.tsv`. A visual that
contradicts one of these is a defect regardless of how good it looks.

**Scale and partition**
- Panel 2,976 assemblies, 2,959 after removing 17 duplicate BioSamples
- **85 analysis units, 2,340 genomes.** This is the analyzed basis
- 43 countries in the analyzed set, 50 in the panel
- Unit size median 18, range 7 to 159

**The detection window.** All diversities are alignment-derived mean pairwise core
SNPs, never the Mash proxy.
- Window **[700, 4700]**, floor bracketed (588, 755], ceiling about 4,700
- **47 in-window, median r/m 7.70**, IQR 5.72 to 9.41, 1,388 genomes
- **12 below floor, median r/m 1.32**, IQR 1.04 to 2.38, 349 genomes
- **26 above ceiling, median r/m 2.14**, IQR 1.30 to 3.49, 603 genomes
- Median outside the window **1.99**. Separation **3.9x**
- Median across all 85 units is 5.51 and is **not** the headline

**How the floor was located without touching r/m.** This is the answer to "isn't
that circular?"
- Diversity band 15 to 588: union recombination coverage 4.3%, median tract 1.12 kb
- Diversity band 755 to 1,349: union coverage 28.0%, median tract 3.37 kb
- Nothing sits between 588 and 755, so the floor is a bracket and 700 is a round
  number chosen inside an empty gap
- Insensitive to placement: floor 588 gives 7.70, 700 gives 7.70, 755 gives 7.74,
  840 gives 7.78

**Controls**
- Negative: **1,519 simulated no-recombination replicates over 62 unit-replicons.**
  20 replicates (**1.32%**) produced any call. Maximum null r/m ever seen
  **0.00668**. Lowest real value **2.85**, highest **14.92**. Separation
  **427x to 2,234x**
- Positive: 21 implanted 5 kb tracts at the measured donor divergence nu = 0.002,
  **19 recovered, 91%**. Recovery 90 to 100% for any more distant donor

**Tree builder.** 6 units by 2 replicons, 12 comparisons, spanning r/m 1.81 to 14.13.
- IQ-TREE against RAxML: median ratio 0.988, 7 of 12 below 1.0, sign test p = 0.77
- rapidnj against RAxML: median ratio **0.922**, worst 45.5%, 11 of 12 below 1.0,
  **p = 0.0063**
- rapidnj against IQ-TREE: median 0.938, worst 51.6%, 10 of 12 below, p = 0.039

**Geography and attribution.** Validation set is 46 scorable genomes.
- Country, best estimator nearest neighbor: **10/46 (22%)**, kappa 0.193
- Region, best estimator majority of 20 nearest: **41/46 (89%)**, kappa 0.832
- Asia versus not, majority of 20: **46/46 (100%)**, kappa 1.000
- **The estimator is part of the number.** Never mix them
- Per-unit phylogeography over 85 units: 6 geographic, 12 confounded, 25 null,
  5 vacuous control, **37 untestable because single-country**

**Sampling**
- Thailand **1,561 of 2,340 = 66.7%**. China 265. Together three quarters
- USA 47, of which **21 sit in one unit**, `strain_4_L1_1`, plus 1 Colombia
- South Asia carries about 44% of modelled global burden and **2.5%** of this panel

---

## 6. Framings that are forbidden

These are not stylistic preferences. Each one has been argued through and each
has a reason.

- **Never say or imply that prior studies were wrong.** They did the right thing
  with what they had. The claim is that one step was missing from all of it,
  including this study until it was added.
- **Never present a low r/m as a low recombination rate** outside the window. It
  is a detection failure. That reversal is the paper.
- **Never quote an r/m for a group outside the window** as though it meant
  something, including the Americas groups.
- **Never compare a country number to a region number** without both estimators
  on screen.
- **Never quote the Mash proxy against the [700, 4700] window.** Different units.
- **Never claim the reported run is reproducible.** It ran unseeded and
  multi-threaded. The pipeline is now byte-reproducible under `--deterministic
  true`, which produces a different run rather than validating the pinned one.
- **No dates, no direction of spread, no country attribution** are supported
  anywhere in this work.
- **cgMLST is deliberately absent from the deliverable** at the presenter's
  instruction, even though it is the manuscript's attribution basis. The
  attribution numbers stay. The method name does not appear.
- **Writing style is a hard constraint** on anything that appears on screen. No em
  dashes, no en dashes, no semicolons, no curly quotes, American spelling, median
  sentence length about 19 words. Full rules in
  `VM_HANDOFF_PACK/text/P-writing-prompt.md`.

---

## 7. The visuals

Each entry gives the finding, where the data lives, what the data will and will
not support, and a judgment on whether motion is the answer. **None of these is a
storyboard.** Section numbers are the deliverable's own `data-name` sections.

Format of each entry:
**Finding** what has to land. **Data** the file, by path. **Supports** what can
honestly be drawn. **Motion** whether it earns its cost, and where.
**Wrong** the specific failure to avoid.

### Part A. Agreed before today

#### 7.1 The negative control, section 7

**Finding.** Simulate genomes with zero recombination, run the identical pipeline,
and see what the tool reports anyway. Across 1,519 replicates over 62
unit-replicons, 20 replicates (1.32%) produced any call and the largest value ever
returned was 0.00668. Real units sit between 2.85 and 14.92. The tool is not
manufacturing recombination.

The framing that works for this audience is the no-template control. Every
technologist in the room runs one daily, and the analogy is exact rather than a
simplification. This reframing is the highest-leverage move in the deliverable.

**Data.** `data/TIER2_null.txt` for the raw distribution, but **the file is a
mid-run snapshot giving 1,302 replicates over 54 unit-replicons.** Use the
completed-run constants above and do not summarize the file.

**Supports.** The four constants, the 20 null calls, the 2.85 to 14.92 real range,
and the 427x to 2,234x ratio. Nothing else.

**Motion.** Yes, and this is the clearest case for Manim in the whole project. The
gap cannot be drawn to scale on a linear axis and reads as one dot near zero on a
log axis. A continuous zoom out from the null distribution's own scale until the
real data enters the frame lets the audience travel the distance rather than read
it. Ranked first.

**Wrong.** A broken axis, a log axis, or any number taken from the snapshot file.

#### 7.2 Prior work, section 2

**Finding.** Three prior studies and this one all divide the population and then
remove recombination before measuring. They differ in what they divide by and how
far. None measured whether the measurement step still works on the pieces they
produced. That single missing step is the contribution.

Nandi 2015, 106 genomes, divided by clade, removed recombination with ClonalFrame.
Chewapreecha 2017, divided repeatedly, Gubbins, and **the study states in print
that the limit exists**. Seng 2024, 1,391 genomes, divided by lineage, Gubbins.
This work, 2,976 genomes, divided the same way, and then checked the groups
against a measured range.

Chewapreecha deserves credit rather than criticism. They knew the tool had limits,
said so, and kept dividing until the numbers settled. They also report that the
Australasian group could not be divided far enough to come inside the limit, which
is a published failure of the standard approach in the oldest part of the
population. Nobody could resolve it, because there was no measured boundary.

**Data.** Section 2 of the deliverable carries the study table already.

**Supports.** The four rows above, and the stated reasons quoted in the
deliverable. It does not support any claim about what those studies would have
found under this window.

**Motion.** Probably yes, but the requirement is specific. The visual has to make
similarity obvious first and difference obvious second. A four-column table makes
everything look equally different, which is the current failure. A shared spine
with the four studies running down it, three exiting at the same station and one
continuing, is the shape. The presenter has named this as the section they could
not explain to a colleague, so ranked second.

**Wrong.** Four parallel rows. Any word implying error.

#### 7.3 The detection window mechanism, section 3

**Finding.** Gubbins finds recombination by looking for a local excess of SNP
density against the genome-wide background. That is the whole trick. Below the
floor there are almost no SNPs anywhere, including inside the imported piece, so
nothing stands out and nothing is marked. Above the ceiling, SNPs are dense
everywhere, the imported piece no longer looks unusual, it is not marked, and its
SNPs are counted as ordinary mutation. That moves recombination out of the
numerator and into the denominator.

**The collapse is symmetric, and that is the point.** Too similar and too
different both give a low number, and the number alone cannot tell you which you
have, nor separate either from a group that genuinely recombines less.

The design insight worth keeping is that **the imported piece never changes. Only
the background does.** The eye is asked to judge contrast, which is what the
algorithm does.

**Data.** Real anchor values from `data/GATE1_ALIGNMENT_2026-08-21.tsv`. Anchoring
to three real units beats illustrative values, and the units are there.

**Supports.** The mechanism, the window bounds, and the r/m by class. It does not
support a smooth analytic curve of r/m against diversity, because 85 points are
not a function.

**Motion.** Yes. Three button states should become one continuous sweep, with the
numerator and the denominator drawn as accumulating quantities so that "moves into
the denominator" is seen rather than asserted. Ranked third.

**Wrong.** Moving or resizing the imported piece. Drawing a fitted curve through
the 85 units as though r/m were a deterministic function of diversity.

#### 7.4 The grouping ladder, section 11

**Finding.** See correction 3.1. The answer does not simply improve as the
question coarsens. Region reaches kappa 0.832 at five classes, and Southeast Asia
versus not reaches only 0.461 at two. What matters is whether the boundary is one
the data draws.

**Data.** `data/GROUPING_LADDER.tsv`, 20 rows, five groupings by four estimators.

**Supports.** All 20 rows. Kappa is the right measure because the chance baseline
changes at every rung, and both the accuracy and the baseline are in the file.
Every rung must carry its estimator label.

**Motion.** Weakly. This is close to a static figure that reveals in order. The
value is in the ordering and the labels, not in movement. Do not spend a Manim
session on it.

**Wrong.** Sorting the rungs by kappa, which manufactures the monotonic climb the
old brief wrongly predicted. Mixing estimators. Drawing accuracy as the primary
bar. Naming the underlying typing method.

#### 7.5 The Americas, section 11

**Finding.** Ten units hold at least one Americas genome and they fall into two
clean kinds. Four units are 92 to 100 percent Americas, spanning the US, Colombia,
Brazil, Mexico, Puerto Rico, Ecuador and the Caribbean, and `strain_22_L1_1` sits
between the patterns at 55 percent. Five units are dominated by Thailand,
Singapore or China and **each carries exactly one United States genome.** That is
the signature of travel-associated acquisition and you can see it without running
a test.

Every Americas-dominated unit falls outside the working range, so no r/m is
interpretable for any of them.

**Data.** `AMER_UNITS` in `extracts/virtual_manuscript_data.json`, ten rows with
full country composition.

**Supports.** The composition bars and the two-pattern split. It does not support
calling any individual genome travel-associated, because exposure history is not
in this table.

**Motion.** Not much. The strongest upgrade is **linkage, not animation**: select a
unit and have its clade light up on the tree, so "this US genome sits inside a
Thai lineage" is shown topologically. Claude Code is building the interactive tree
that receives that selection, see 7.13. What Animo can usefully add is the
transition that carries the eye from a bar to its clade.

**Wrong.** Printing an r/m for an Americas-dominated unit as though it meant
something. A third color.

#### 7.6 Burden against sampling, section 10

**Finding.** The collection is severely unbalanced and the imbalance is the main
limit on any geographic claim. Thailand is 1,561 of 2,340, 66.7 percent. China
adds 265. South Asia carries about 44 percent of modelled global melioidosis
burden and 2.5 percent of this panel. East Asia and Pacific carries 40 percent of
burden and 91.8 percent of the collection. 43 countries appear at all.

**Data.** `MAPC` in the JSON extract, 27 countries with counts and coordinates.
The burden shares are in section 14 of the deliverable.

**Supports.** Counts per country and the two regional burden shares. **It does not
support a per-country burden estimate**, so a morph must be regional, not
national.

**Motion.** Yes, one motion, and it is worth about two seconds of the talk. Draw
the map with circles sized by genome count, then tween the same circles to sizes
proportional to regional burden. South Asia inflating while Thailand collapses
makes the argument without a sentence.

The current coastlines are hand-drawn, 14 polygons, because the artifact cannot
fetch external assets. A proper equal-area projection with real boundaries
embedded as inline path data would be a genuine improvement if it can be produced
offline.

**Wrong.** Sizing any single country by burden. Adding a country not in `MAPC`.

#### 7.7 Recursive subdivision, section 6

**Finding.** `strain_1_L1_26` is 153 genomes at 1,310 mean pairwise core SNPs,
r/m 4.47, comfortably in the window. The evidence that it held two populations was
unambiguous, so it was divided. Two of the three children landed below the floor.

| child | n | mean pairwise core SNPs | r/m | Gate 1 |
|---|---|---|---|---|
| `strain_1_L1_26` | 98 | **72** | 1.07 | below floor |
| `strain_1_L1_36` | 47 | 1,477 | 6.68 | in window |
| `strain_1_L1_37` | 8 | 123 | 2.63 | below floor |

The division was correct. The cost was invisible until the floor had been
measured. Conservation matters visually: 153 equals 98 plus 47 plus 8.

**Data.** `text/TABLES.md` Table 3, and `text/GATE1_ALIGNMENT_RESULT_2026-08-21.md`
section 7b for the recomputed 72.

**Supports.** One level of subdivision, on real data. **It does not support a
second or third level.** The old brief asked for the recursion run two or three
levels to show the in-window population draining away. Those deeper splits were
never run. If that shape is built it must be labeled as an illustration of the
mechanism and must carry no numbers.

**Motion.** Yes for the one real level, showing the parent dissolving into
children rather than boxes sliding.

**Wrong.** The n = 98 child's diversity is **72**, recomputed on its own
membership. The distances file will hand you **1,310**, which is the unsplit
parent's value arriving through a join on unit name. Using it is wrong by a factor
of eighteen and flips that row's Gate 1 class.

#### 7.8 The confounder specification curve, section 11

**Finding.** BioProject is nested inside country. 95 percent of BioProjects are
single-country, Cramer's V against country is 0.857. So a test that controls for
BioProject partly controls for the thing it is trying to detect. **The count of
units with real geographic signal depends on which imperfect control you choose,
and the range is the finding.**

| control rule | units retained |
|---|---|
| no control at all | 26 |
| discount only if the within-country batch effect is FDR-confirmed | **24** |
| discount if any nominal within-country batch effect | 18 |
| BioProject discriminant, what is currently reported | **6** |
| BioProject plus collection period | 2 |

The reported envelope is **6 to 24, and neither endpoint is defensible.**

**Data.** `text/CONTROL_SPECIFICATION_2026-09-02.md` and
`text/BATCH_PROXY_AUDIT_2026-09-02.md`, both now in the pack.
`data/PHYLOGEOGRAPHY_ASSOCIATION_FROZEN_2026-08-23.tsv` carries the per-unit tests.

**Supports.** The five specification points and the 6 to 24 band. It does not
support naming a preferred value inside the band.

**Motion.** Modest. A specification curve is a known static form and reveals well
in order. The animation would be the estimate moving as each choice is toggled.
Worth building because there is currently no visual at all, but it is not a Manim
job.

**Wrong.** Presenting the range as a failure to get an answer. Presenting 6 as the
answer and the rest as sensitivity.

#### 7.9 The paired tree-builder plot, section 8

**Finding.** Six units by two replicons, 12 comparisons, on the same real
alignments, spanning r/m 1.81 to 14.13. IQ-TREE and RAxML agree with no
directional bias. rapidnj underestimates r/m systematically, median ratio 0.922,
worst 45.5 percent, 11 of 12 ratios below 1.0, sign test p = 0.0063. rapidnj is
the fast default in several pipelines, so a study using it will report a lower
recombination rate for a reason that has nothing to do with biology.

**Data.** **Now available**, see correction 3.2.
`data/TREEBUILDER_EQ_RESULT.txt` and `data/RAPIDNJ_EQ_RESULT.txt`, all 12 rows
each, with both r/m values per comparison.

**Supports.** A paired-line plot, 12 lines, each connecting one unit-replicon's
r/m under two builders, with the sign test as an annotation. Both panels.

**Motion.** No. This is a standard static form and it is currently missing
entirely. Build it plain and build it fast.

**Wrong.** Averaging the two replicons of a unit. Dropping the IQ-TREE panel,
which is what makes the rapidnj panel mean something.

#### 7.10 The positive control, section 7

**Finding.** Plant 21 pieces of DNA, 5,000 bases each, into real genomes, copied
from a donor at nu = 0.002, the divergence actually observed between strains in
this collection. 19 of 21 recovered, 90 percent. Recovery stays between 90 and 100
percent for any more distant donor.

**Data.** `data/SPIKEIN_RESULT.txt`, five divergence levels with counts and rates.
**Take the rates from the file rather than recomputing**, because the printed
counts are rounded summaries. The nu = 0.002 and nu = 0.01 rows show identical
integers and different rates, so recomputing turns the reported 91 percent into
90 percent.

**Supports.** The five rows and the non-monotonic top, which is real. A tract
carrying 45 SNPs can be split into two called blocks, neither covering half of it.

**Motion.** Modest. The upgrade worth making is to show one implanted tract on the
genome track from 7.3 and let the detector sweep across it, so "recovered" has a
visible meaning rather than being a tile turning green. Sharing the track with 7.3
is most of the value.

**Wrong.** Recomputing the rates. Hiding the non-monotonicity, which is
explainable and honest.

#### 7.11 The parameter chain, section 1

**Finding.** The analysis is a chain of nine steps and every step's output is the
next step's input. Assemblies, Mash distances, PopPUNK strains, fastbaps level-1
subclusters, analysis units, per-unit reference, core alignment, Gubbins, r/m. A
choice made early propagates all the way down. This is the structural reason the
study exists. Nobody had asked what the measurement step requires of the
partitioning step.

**Data.** `PARAM_NODES` and `PARAM_EDGES` in the JSON extract, 9 nodes and 8
edges, each with its explanatory text.

**Supports.** The chain as drawn. It does not support any quantitative claim about
how much a choice propagates.

**Motion.** A build animation would help more than interactivity here. Reveal the
chain one step at a time as the presenter speaks, then flash the two steps whose
relationship the paper measures, partitioning and Gubbins. Keep the side module,
because it is what lets the presenter answer "what was that box again" without
scrolling.

**Wrong.** Removing the side module.

### Part B. New requests

#### 7.12 Why this reaches the outbreak call, section 13. Highest new value.

**Finding, and it is the most directly useful thing in the paper for this
audience.** In an outbreak investigation a SNP threshold says that two genomes
fewer than N SNPs apart probably share a source. Published thresholds for this
organism run from 0 to 5, with an upper bound of 15 taken from 17 informative
pairs in a single study that applied no recombination correction. **That regime is
precisely where Gubbins detects only 5 to 10 percent of real recombination.** One
step further out, recombination is most of the distance.

So recombination matters most, and is detected least, exactly where outbreak
decisions get made.

The published record shows it from both directions. A point-source outbreak traced
to one unchlorinated water supply spanned 1,328 SNPs between its two commonest
sequence types, of which only about 5 percent survived recombination filtering. In
the other direction, isolates sharing a sequence type have been reported 21,211
and 20,567 SNPs apart, against 404 SNPs for a genuinely clonal same-sequence-type
pair in the same study.

**Data.** `text/MANUSCRIPT_DRAFT_2026-09-02.md` Discussion, the paragraph
beginning "The consequence for outbreak and attribution genomics". Citations 11,
15, 33 and 34 there. All four values verified in place.

**Supports.** A single diversity axis carrying the threshold band 0 to 15, the
detection efficiency curve behind it, and the four published anchor points. It
does not support a recommended threshold, and it must not propose one.

**Motion.** Yes, and this is the one new visual worth a full session. The shape is
two curves crossing on one axis: how much of the distance is recombination, rising
with diversity, against how much of it the tool detects. The outbreak decision
band sits where the first is already material and the second is near zero.

**Wrong.** Proposing a corrected threshold. This work does not license one.

#### 7.13 The interactive global tree. Built 2026-09-09.

**Delivered.** `TREE_EXPLORER.html`, 199 KB, self-contained, opens offline. All
2,340 analyzed genomes, 85 units in 28 PopPUNK strains, on the grafted chr1 tree.

```
make_tree_explorer_data_bp.py   prunes 2,352 tips to the 2,340 of the basis,
                                lays out the cladogram, writes 175 KB of JSON
tree_explorer_template.html     the viewer, one /*__DATA__*/ placeholder
make_tree_explorer_bp.py        inlines the JSON, refuses to write on any
                                count that disagrees with NUMBERS.tsv
```

It renders on canvas rather than SVG, because 2,340 tips in SVG is exactly what
produced the 684 KB problem in correction 3.3. Pan, zoom, search across genome,
unit, country and region, hover readout, click to select a unit, color by strain,
detection class, region or country.

**Three things in it are load-bearing and should not be redesigned away.**

The r/m readout **refuses to print a value for a unit outside the working range**
and says so in words instead. That is the paper's central claim enforced in the
interface.

**Zoom is anisotropic.** The depth axis is 40 steps wide and wants to stay fit
while 2,340 tips need heavy vertical expansion. A single shared zoom scalar
pushed every selected clade off screen, which is the bug the first build had.

**The tree is not ladderized.** `make_figure6_bp.py` draws the pruned tree in its
natural tip order, and the 29-of-30 monophyly result is a property of that order.
Reordering children changes which strain blocks are contiguous. The generator
asserts 29 of 30 and refuses to write otherwise, so the explorer and the
published figure cannot disagree.

**It speaks the two events in 7.5.** It dispatches `unitselect` on selection and
listens for `unithighlight`, so the Americas composition panel can drive it.

Two caveats are structural and must survive any treatment. **Branch lengths are
not drawn**, because the grafted tree splices two scales differing by about
133-fold, backbone substitutions per site over the parsnp core against within-unit
substitutions per site over recombination-filtered sites. And **a slice is shaded
only where it is a real clade**, checked against its MRCA's leaf set, which is why
`strain_1` occupies three separate blocks and one of them is outlined rather than
filled. 29 of 30 blocks are shaded.

Why it earns its place: geography was never an input to PopPUNK, fastbaps or
IQ-TREE, so the recovery of known biogeography is a result rather than an
assumption.

**Nothing for Animo here except one companion camera move worth considering**, a
flight from the whole tree down into one Thai-dominated clade to find the single
US genome inside it. That would pair with 7.5 and it is the kind of continuous
zoom HTML does badly.

#### 7.14 The hidden-annotation idiom, everywhere it applies

The strongest thing found in the first render session was not an animation. It was
a toggle that hides the annotation so the audience tries and fails to find the
imported piece themselves.

**Request: identify every other place in the deliverable where that idiom
applies, and apply it.** Three candidates worth testing.

- Section 5, the twelve below-floor units. Hide the Gate 1 coloring and ask which
  of these twelve is a real low rate. Nobody can tell, which is the finding.
- Section 11, the Americas panel. Hide the pattern labels and ask which units hold
  a traveler. The two patterns are visible enough that people will get it, which
  makes the reveal a confirmation rather than a defeat.
- Section 8, the tree builder. Hide which builder produced which line.

This is a judgment request rather than a build request. Say which of these
actually works and which is a gimmick.

#### 7.15 Contribution, before and after, section 13

**Finding.** The organism was known to recombine heavily, published repeatedly at
around r/m 7.2 overall and 3.7 to 4.6 per lineage. The software was known to have
limits, stated in print but never located. Dividing before measuring was already
standard. **What is new is measuring where the measurement works, and what that
does to the reported rate.**

**Data.** Section 13 of the deliverable carries the seven-row comparison table.

**Supports.** A before and after strip: the literature's reported range against
this study's 7.70 in-window and 1.99 out-of-window. It does not support a claim
that prior values were wrong, because they were computed on unchecked groups and
this study cannot say which of those groups were in window.

**Motion.** Light. The table mostly works. What would help is one strip showing
the reversal in "what does a low r/m mean", from "a more clonal group" to "most
often a detection failure".

**Wrong.** Any framing where prior published rates are corrected by this work.

#### 7.16 What more genomes would answer, section 14

**Finding.** The presenter asked to really make a point of this and it is the most
valuable unbuilt thing in the deliverable. The strongest argument is quantitative
rather than rhetorical. **37 of 85 units are untestable because they hold a single
country.** South Asia carries 44 percent of burden against 2.5 percent of the
panel. No group in this collection sits in the diversity gap where the floor must
be, so the floor stays a bracket.

**Data.** `data/PHYLOGEOGRAPHY_ASSOCIATION_FROZEN_2026-08-23.tsv`, where
`interpretation == "untestable: single-valued"` gives the 37 single-country
units exactly, plus the four-row table already in section 14. Corrected
2026-09-09: an earlier draft cited `FINAL_PARTITION.tsv`, which is withheld and
is not needed for this number.

**Supports.** The current counts. **A modelled sampling expansion is a new
computation and nobody has run it.** If a visual shows units becoming testable
under added sampling, that model has to be built and checked first. Flag it and
Claude Code will run it, rather than drawing an illustrative curve.

**Motion.** Yes if the model exists. No if it does not.

**Wrong.** Drawing a projection that was never computed.

**Defect found and fixed 2026-09-09.** The deliverable's section 14 claimed "no
group sits in the gap between 535 and 1,265 where the boundary must be." That is
false on the alignment basis: ten units sit in [535, 1265], three with n >= 25.
The range is stale. 535 began as a ska distance for cluster_53 in
`REVISED_STRATEGY_2026-08.md`, and 1,265 is the ska floor bracket's upper bound,
1,268, both relabeled as "mean pairwise SNPs." The true empty bracket on the
alignment basis is **(588, 755]**, which is what the deliverable's own section 5
and the manuscript's own Results already use. The deliverable was corrected in
both places. **The analysis is untouched**, because r/m never depended on this
claim and is insensitive to floor placement across the bracket. The manuscript
Discussion still carries the stale range and is author-owned. See section 9.

#### 7.17 Study flow, manuscript Figure 1. Lowest priority.

CONSORT-style accounting from 2,959 panel genomes to 85 units and 2,340 genomes,
to 47 in-window units, to 46 scorable validation genomes. Exists as a static SVG
from `make_figure1_bp.py`. Currently not used in the deliverable, where the
numbers appear in the hero stat bar instead. Animate it only if a session is
otherwise free.

---

## 8. Priority

Ranked by audience value per unit of effort. Items marked CC are Claude Code's
and are listed so the sequence is legible, not as render work.

1. **The negative control zoom-out** (7.1). Biggest comprehension win, clearest
   case for Manim.
2. **The prior-work shared spine** (7.2). Named as a live-explanation failure.
3. **The outbreak threshold crossing** (7.12). New. The most directly useful thing
   in the paper for a laboratory audience.
4. **The continuous detection window** (7.3), replacing three states with one
   sweep, numerator and denominator drawn as quantities.
5. **The paired tree-builder plot** (7.9). Small, standard, missing, and now
   unblocked.
6. **The hidden-annotation audit** (7.14). Judgment, not build. Cheap.
7. **The burden-versus-sampling morph** (7.6).
8. **CC. The interactive tree** (7.13). Done. It unblocks 7.5's linkage.
9. **The grouping ladder** (7.4), built honestly, non-monotonic.
10. **Recursive subdivision** (7.7), one real level only.
11. **The specification curve** (7.8).
12. **The spike-in detector sweep** (7.10), sharing the track from 7.3.
13. **CC. The 684 KB style fix** (3.3).
14. Parameter chain build (7.11), contribution strip (7.15), study flow (7.17).

---

## 9. Traps that have already cost this project real time

Each has bitten at least once.

- **Two diversity bases exist and they are not interchangeable.** Alignment-derived
  mean pairwise core SNPs is the basis of the window. The Mash proxy overstates
  diversity unevenly, median ratio 1.30, max 17.20, and misplaces 22 of 85 units.
  Quoting a Mash value against the window is the project's signature error and it
  was found in the deliverable's own section 5 table on 2026-09-08.
- **Pairwise means all member pairs, not reference against member.** The reference
  genome only supplies a shared coordinate system. A group of 10 gives 45 pairs.
- **`TIER2_null.txt` is a mid-run snapshot** giving 1,302 replicates over 54
  unit-replicons. The completed run is 1,519 over 62. Do not summarize the file.
  This was the project's seventh instance of reading a count off a denominator
  that was still filling.
- **There are two unit-medoid trees and only one is the reported run. This trap
  was miswritten until 2026-09-09.** The reported-basis tree is
  `global_ml_tree_86tip.treefile` (source `L1v4c_out/global_ml_tree.treefile`),
  86 tips, all 85 basis units plus 1 to prune, and it is what `make_figure3_bp.py`
  uses. The files named `L1_GLOBAL_ML_TREE.nwk` and `L1_GLOBAL_BACKBONE.nwk` are a
  different run: 82 tips, only 54 basis units present, and carrying units the
  reported basis excludes on purpose, including `strain_1_L1_10` and the split
  children `strain_1_L1_36` and `strain_1_L1_37`, while missing `strain_1_L1_26`
  which the basis keeps. That is the 88-unit A100 cross-hardware control run.
  Pruning it cannot reach the basis, because it is a subset, not a superset. Those
  two files have been removed from the pack. When drawing any unit tree, prune the
  one extra tip and refuse to draw if the remainder is not exactly the 85 basis
  units. The grafted genome tree carries 2,352 against 2,340 and needs the same
  treatment.
- **The `country` column in `assign_region.tsv` holds region values.** Real country
  is column 9 of `L1v4c_MERGED_METADATA.tsv`.
- **`L1v4c_out/Clusters` is a hybrid directory** holding 88 subdirectories against
  86 units. Globbing it double-counts 153 genomes.
- **The reported analysis run is not seed-reproducible.** It ran unseeded and
  multi-threaded through both Gubbins and IQ-TREE. Re-running under
  `--deterministic true` produces a different run rather than validating the
  pinned one. This is in the Methods and must not be presented as resolved.
- **Never split a ratio on its own denominator.** A circular test built that way
  produced a false null that survived into two write-ups.
- **A check that passes over an empty set is worse than no check.** Every check
  added since asserts a minimum count and was broken on purpose before being
  trusted.
- **Never quote a phylogeography p without its q and its `control_status`.**
  `strain_22_L1_1` reads p = 0.0430, which looks like a surviving country signal.
  Its q is 0.0826 and its own `interpretation` column reads `null`. The frozen
  table carries all three columns and the raw p is the trap. Of the five
  Americas-dominated units, none survives both FDR and the control.
- **`PHYLOGEOGRAPHY_ASSOCIATION_INTERPRETATION.md` sections 5 to 7 are
  superseded, and the file says so at line 16.** They are on the A100 control
  partition, from before that run stopped being production. Quote
  `PHYLOGEOGRAPHY_ASSOCIATION_FROZEN_2026-08-23.tsv` instead. Reading past the
  banner on 2026-09-10 produced two wrong numbers in a review: the country FDR
  count as 24 rather than 23, and `strain_14_L1_4` in the list of six passing
  units rather than `strain_1_L1_11`. On the frozen basis `strain_14_L1_4` has
  q = 0.1284 and interpretation `null`. The six are also **not** all Southeast
  Asian, which that section claims.
- **New, from 3.1.** A described shape can be false. The old brief predicted a
  monotonic climb that the data does not show. Check the shape against the file
  before animating it, and say so when it does not hold.

---

## 10. Session prompts

Two short prompts. Everything else lives in this file, which is why they are
short.

**Prompt A, once, to open the audit pass.**

```
Repo is at /home/phemarajata/Downloads/snp-mod-local-working. Read ANIMO_BRIEF_2026-09-09.md first, then VIRTUAL_MANUSCRIPT.html and the files under VM_HANDOFF_PACK/. Do not paste the HTML anywhere, extract and grep it.

Run: python3 VM_HANDOFF_PACK/extracts/derive_vm_data.py
It must print OK before you go further.

Do one audit pass over section 7 of the brief. For each of the 17 visuals, tell me: is the data actually there, does the described shape hold against the file, and is motion the right answer or is a static or interactive form better. Rank what is broken and what is buildable. Refuse anything the data does not support and propose what it does support instead.

Return the audit only. Do not build anything yet.
```

**Prompt B, once per build. Fill in the two blanks.**

```
Repo is at /home/phemarajata/Downloads/snp-mod-local-working. Read ANIMO_BRIEF_2026-09-09.md, then build section 7.__ only.

Data files are on disk, listed in that entry. Use the numbers in the brief, do not recompute any statistic, and do not introduce a number that is not in the brief or in the named data file.

Output one self-contained file I can paste into VIRTUAL_MANUSCRIPT.html. No libraries, no external requests, because the deliverable has to open offline. Theme through the CSS custom properties the file already defines: --ink, --muted, --panel, --rule, --signal, --cold, --hot. One button labeled Replay. Under prefers-reduced-motion, draw the final frame.

On-screen text: no em dashes, no en dashes, no semicolons, no curly quotes, American spelling, short sentences.

If the data does not support what the entry describes, stop and tell me, and propose what it does support.

Notes from the last build: ______
```

Keep the notes line filled in from here on. It is how the palette and idiom
decisions propagate between sessions that start fresh.

---

## 11. Clip revisions, 2026-09-10. Feed this section directly.

Five clips were delivered on 2026-09-09 and reviewed frame by frame on 2026-09-10
by sampling each MP4 at one second. **This section is self-contained. It carries
the real beat map of every clip, what to change, and what not to touch.**

Two things were found. The narration was mistimed against the animation, worst in
7.01, and that is **already fixed** in `narration_v2/`. The visuals have specific
weaknesses that are worth a revision pass, listed per clip below.

**Rules that still bind.** Every number stays as delivered. All five clips were
checked against the frozen basis and their figures are correct, so a revision
changes how something reads, never what it says. Section 5 holds the numbers,
section 6 holds the forbidden framings.

### 11.0 The narration is already re-timed. Do not re-derive it.

`narration_v2/<clip>.{csv,srt,txt}` and `narration_v2/all_clips.csv`, 44 lines
across five clips. `start_s` is where a line begins. The gaps between lines are
engineered, so never stretch a line to fill one. Still 132 words per minute, still
no digits anywhere. If a revision moves a beat, the affected line's `start_s`
moves with it and the fit is re-checked with
`python3 make_narrated_videos_bp.py --check`.

### 11.1 The change with the largest payoff: 7.09 should plot the ratio

7.09 plots absolute r/m for both builders and connects the pairs. Seven of the
twelve comparisons sit below r/m 5, so those lines are short, overlapping and
nearly flat. **The finding, eleven of twelve falling, is carried entirely by the
text caption. The picture does not show it.**

Plot the ratio instead. One dot per comparison, one horizontal reference line at
1.0. Eleven dots below it and one above is legible without reading. The worst case
becomes the lowest dot rather than a label.

Per-comparison values are on disk and nothing blocks this:
`TREEBUILDER_EQ_RESULT.txt` and `RAPIDNJ_EQ_RESULT.txt`, twelve rows each.
Keep both panels. Keep the sign test annotations.

**Effort: re-render.**

### 11.2 Per clip: beat map, what is wrong, what to change

Beat times are seconds from the start of the MP4, read off the rendered file.

#### 7.01 negative control, 41.5 s

```
 0  title "The no-template control" types in
 1  lab analogy paragraph, solid by 2
 4  "We ran the same idea" plus "Simulate genomes with zero recombination"
 6  title changes to "The negative control", axis begins to draw
 8  axis with ticks, 0.000 to 0.008
 8.5 "1,519 replicates over 62 unit-replicons"
10  "20 of them returned any call at all, which is 1.32%"
12  "The largest value ever returned was 0.00668"
14.5 "Now hold the axis linear and widen it until the real groups appear."
19  readout "full width of this axis, r/m 0 to 0.008"
20  zoom begins
27  the real band enters, readout 4.72
31  zoom completes, readout 16.00
33  "everything the null ever produced, 0 to 0.00668"
34  "Separation of 427x to 2,234x"
35  "real analysis groups, 2.85 to 14.92"
36  "The tool is not manufacturing recombination."
```

**Wrong, in order of cost.**

1. **Seven seconds of empty zoom.** From 20 to 27 only a corner readout changes.
   In a 41 second clip that is the most expensive stretch and it carries no
   information. Cut it, or slide a marker in from the right edge so something is
   visibly approaching.
2. **The null disappears exactly when it is needed.** By 26 the teal cluster is a
   hairline at zero, so at the moment the clip claims 427-fold, one of the two
   compared objects is no longer visible. Keep an inset showing the null at its
   own scale, so both remain on screen at the comparison.
3. **Two names for one thing in the first six seconds**, "the no-template
   control" then "the negative control". Much of this audience is working in a
   second language. Pick one, or show the equivalence once and deliberately.

**Effort: 1 and 3 are re-renders. 2 is a small re-conception.**

#### 7.03 detection window, 47.7 s

```
 0  title "How the detector actually works"
 2  "It looks for a local excess of SNP density. That is the whole trick."
 4  title changes to "The detection window", the genome track appears
 5  "one imported piece"
 6  "The imported piece never changes. Only the background does."
 8  "NOT MARKED", almost no SNPs anywhere
 9  counted-as bars, 0% recombination and 100% mutation
11  "the working window, 700 to 4,700" band on the diversity axis
13-16 diversity readout climbs 15 to 243
17  strain_4_L1_1, 243 SNPs, below the floor, measured r/m 1.25
22  verdict flips to "MARKED as imported", bars 43% and 57%
24  strain_1_L1_23, 1,284 SNPs, in the window, measured r/m 7.70
29  verdict flips back to "NOT MARKED", bars 0% and 100%
31  strain_1_L1_11, 5,819 SNPs, above the ceiling, measured r/m 2.04
38  "Too similar and too different both give a low number."
42  the three class medians
44  "The number alone cannot tell you which one you have."
```

**This clip has the best idea in the set and buries it.** The counted-as bars
going 0/100, then 43/57, then back to 0/100 are recombination moving out of the
numerator and into the denominator, made visible. That is the mechanism the whole
paper rests on, and it is rendered as a small low-contrast footnote in the middle
of the frame. **Promote those bars to co-star with the genome track.**

Second, the diversity readout climbs through about 44 values when only three
matter, the three real anchor groups at 243, 1,284 and 5,819. Continuous ticking
trains the eye to ignore the number. **Dwell on the three anchors and move fast
between them.**

Third, the clip asserts that the imported piece never changes, but the viewer
cannot check it because the background redraws every frame. This is the place for
the hidden-annotation idiom already proven elsewhere: at the above-ceiling state,
hide the outline and let the audience try to find the piece and fail. That is the
finding, experienced rather than watched.

**Effort: the bars and the dwell are re-renders. The hide-the-outline beat is a
re-conception and is worth it.**

#### 7.07 recursive subdivision, 35.2 s

```
 0  title, subtitle by 2
 4  parent bar, "strain_1_L1_26 before the division", 153 genomes,
    1,310 mean pairwise core SNPs, r/m 4.47, in window
 7  "The evidence that it held two populations was unambiguous, so it was divided."
 9-11 the bar splits
12  "three children after the division", 98 | 47 | 8
14  "153 = 98 + 47 + 8"
16-18 plot area, "below the floor", "floor 700"
20  the parent plotted at 1,310, r/m 4.47, in window
22-25 the children plotted at 72, 1,477 and 123
27  the two below-floor segments turn red
30  "Two of the three children landed below the floor."
32  "The division was correct. The cost was invisible until the floor had been measured."
```

**Wrong.**

1. **The bar and the plot are two views of the same three objects and nothing
   links them** until the color flip at 27. Drop each bar segment onto its
   position on the diversity axis so the identity is shown rather than inferred.
2. **The eighteen-fold drop is not drawn.** The parent at 1,310 against its own
   n = 98 child at 72 is the trap this project keeps hitting, and on a log axis it
   reads as a small step. Annotate it explicitly.

**Effort: both are re-renders.**

#### 7.09 tree builder, 26.8 s

```
 0  title, subtitle by 2
 4  axis with r/m gridlines
 5.5 "IQ-TREE against RAxML" header and column labels
 7-8 the RAxML dots appear
 9-11 lines are drawn across to IQ-TREE
12.5 "median ratio 0.988, 7 of 12 fell below 1.0, sign test p = 0.77,
     no directional bias"
14  "rapidnj against RAxML" header
15-19 the second panel's dots and lines
21  "median ratio 0.922, 11 of 12 fell below 1.0, sign test p = 0.0063"
22  "a systematic underestimate"
23  "worst case, 45.5% low"
```

**The timing here is sound and needs no change.** The one defect was the last
narration line running past the final frame, and that is fixed in `narration_v2/`.

The visual change is the ratio plot in section 11.1, which is the highest-value
item in this whole section. One further note if you rebuild it: the two panels are
constructed sequentially, so the comparison the clip exists to make is only
available for its last six seconds. Draw both skeletons first, then populate them,
so the eye can compare throughout.

#### 7.12 outbreak threshold, 44.9 s

```
 0  title, premise by 2
 5-6 axes
 8  "outbreak calls are made here, 0 to 15 SNPs"
10  "The upper bound of 15 comes from 17 informative pairs in a single study
    that applied no recombination correction."
13-16 the recombination curve draws, labeled at 15
17-19 the detection curve draws, labeled at 18
20-22 the field between the curves fills, labeled at 21
25  "at the edge of the band, recombination is already material,
    detection is 5% to 10%"
28  404 SNPs marker, "a genuinely clonal pair sharing a sequence type"
32  1,328 SNPs marker, "one point source outbreak, about 5% survived filtering"
35  21,211 and 20,567 SNPs markers, "two isolates that share a sequence type"
39  "Recombination matters most, and is detected least, at exactly the scale
    where outbreak calls are made."
42  "This does not tell you what threshold to use. None is proposed here."
```

**Wrong.**

1. **The decision band reads as an edge case.** Zero to fifteen SNPs is where
   every outbreak call happens, and on a log axis it is a sliver at the far left.
   Invert the emphasis by dimming outside the band, or add a second panel zoomed
   to it.
2. **The most visually dominant object is the least real one.** The pink field
   between the curves fills the frame, and both curves are schematic. The four
   published anchors are the only measured values in the clip and they arrive as
   thin dashed verticals in the last third. **Render the schematic curves in a
   visibly sketchy style and reserve solid rendering for the anchors.** Make the
   anchors the spine.

**Do not fix this by making the curves look more like data.** They are schematic
and must stay schematic. The on-screen label saying so stays.

**Effort: both are re-renders.**

### 11.3 The pattern underneath, worth applying anywhere

- **Show the derived quantity, not the inputs.** Ratios, differences and shares
  are what the claims are about. 7.09 is the clearest case and 7.07's eighteen-fold
  drop is the same idea.
- **Dwell on anchors, sprint between them.** 7.01 and 7.03 both spend their most
  expensive seconds on continuous motion carrying no information.
- **Keep both compared objects on screen at the moment of comparison.** 7.01
  loses the null exactly when it makes its claim about the null.
- **Reserve solid rendering for measured values.** Anything schematic should look
  schematic. 7.12 is the live case.

### 11.4 What not to change

These survived review and are the reason the set works at all.

- The laboratory control framing in 7.01. Every technologist in the room runs a
  no-template control, and the analogy is exact rather than a simplification.
- The fixed-piece, changing-background construction in 7.03. The imported piece
  must never move or resize.
- 7.12 proposing no threshold, and saying so on screen.
- The editorial rule that the screen carries precision and the voice carries
  meaning. It is why the narration has room to explain rather than read figures.
- Every figure in all five clips. They were checked against the frozen basis and
  they are correct, including the 72 rather than 1,310 in 7.07 and the window at
  700 to 4,700 in 7.03.

### 11.5 Order to work in

1. **7.09 ratio plot.** Largest gain, self-contained, data already on disk.
2. **7.03 promote the counted-as bars and dwell on the three anchors.** The
   mechanism the paper rests on, currently a footnote.
3. **7.01 cut the empty zoom and keep the null visible in an inset.**
4. **7.12 sketch the schematic curves, make the four anchors the spine.**
5. **7.07 link the bar to the plot and annotate the eighteen-fold drop.**
6. **7.03 hide-the-outline beat.** The only genuine re-conception in the list,
   and the one most likely to be remembered.

After any re-render, re-check the narration fit, because moving a beat moves the
line that was timed to it:

```bash
python3 make_captions_bp.py
python3 make_narrated_videos_bp.py --check
```
