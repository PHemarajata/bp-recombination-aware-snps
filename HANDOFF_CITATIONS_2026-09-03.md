# Handoff: the background section, the citation audit, and what the workstation needs to run

**From:** the web session, 2026-09-03
**To:** the Linux workstation session (it has the data and the corpus files)
**Subject:** `BP_background_section.md`, `citation_audit_report.md`, and the
number discrepancies between the Drive folder and the repository

Measured, not inferred. Every count below came from running
`verify_references_bp.py` (new, in this repo) against the Drive copy of
`BP_background_section.md`, or from a direct PubMed lookup. Nothing was read off
a summary line.

---

## 1. The headline

**The audit report states "final consistency check passed, 130/130 refs cited
and defined, 0 orphans." That is false.** The file cites `[1]`–`[130]` in prose
and defines `[1]`–`[96]`. **Thirty-four citations point at nothing**, including
every fix and addition the audit itself claims to have applied.

```
citation marks in prose      : 409
distinct numbers cited       : 130   (range 1-130)
entries in the reference list:  96   (range 1-96)
DANGLING (cited, undefined)  :  34   [97 ... 130]
ORPHAN (defined, uncited)    :   0
```

The orphan count of 0 is real and is what the audit actually measured. It checked
the internal consistency of `[1]`–`[96]`, then asserted a whole-file verification
covering `[97]`–`[130]` that it had not run. That is this project's signature
failure in a new place: a plausible status line standing in for a measurement.

Every one of the audit's own deliverables is in the dangling set. `[99]`
Lichtenegger, `[100]` Jolley, `[101]` Petras, `[102]` Viberg, `[103]` Brennan,
and all 27 of `[104]`–`[130]`. The prose was edited to cite them. The reference
list was not.

---

## 2. Source quality in the 96 entries that do exist

46 of 96 carry at least one flag.

| Flag | Count | What it means |
|---|---|---|
| NO-METADATA | 31 | no journal volume, so the entry cannot be located by hand |
| UNKNOWN-PREFIX | 26 | DOI prefix outside the usual publisher namespaces |
| PREPRINT | 3 | cited as literature where a published version may exist |
| NO-ID | 2 | neither DOI nor PMID |
| ABSTRACT | 1 | a conference poster abstract, cited as `[1]` |

**Seven entries carry the prefix `10.60692`.** It resolves, but not to a journal.
`10.60692/x9erj-5ns21` returns `https://gresis.osc.int//doi/...`, a repository,
and Crossref returns 404 for the prefix. The pattern matters more than the
prefix: several of these are **real papers given a wrong date and a wrong
identifier**.

- `[84]` "Sim et al., The Core and Accessory Genomes of *Burkholderia
  pseudomallei*, **July 2024**". The real paper is *PLoS Pathog*
  2008;4(10):e1000178, PMID 18927621, doi 10.1371/journal.ppat.1000178.
- `[76]` Tumapa, genomic island variation, dated **July 2024**. Real paper is
  2008.
- `[88]` Chantratita, environmental microevolution, dated **July 2024**. Real
  paper is 2008.
- `[87]` Chewapreecha, accidental pathogen, dated **July 2024**. Real paper is
  *Commun Biol* 2019.

A real paper behind a wrong identifier and a wrong year is harder to catch than
an invented one, and it will survive a reviewer's spot-check of the *title* while
failing any check of the *year*.

Three more worth naming individually.

- `[30]` is Chewapreecha 2017, the single most important citation in the
  background, cited through the **Cambridge institutional repository**
  (`10.17863`) with the first author rendered **"H. Mtg"**. That is Holden MTG
  parsed as a surname. The title also carries a raw LaTeX artifact,
  `$\textit{Burkholderia pseudomallei}$`.
- `[11]` is a **Zenodo deposit** with no author listed.
- `[25]` is a **thesis repository** entry (`10.25913`) with no journal.

---

## 3. Two errors the audit did not look for, both still present

The audit was an internal-consistency and completeness audit. It never checked
whether a claim matches its source. Both errors `BACKGROUND_RESEARCH_2026-09-02.md`
section 12.2 documented as "stop quoting" are still in the file.

**The per-allele conflation.** §5.4 still says *B. pseudomallei* has "a ratio of
recombination to mutation (r/m) that is more than twice that of *Streptococcus
pneumoniae* and the highest value yet reported for any bacterium." That is
Pearson 2009's **per-allele MLST** quantity from seven housekeeping genes. It sits
in the same section as genome-wide r/m 7.2. The string "per-allele" appears
nowhere in the document. Left alone, this paper's own headline of **7.70** reads
as roughly three times lower than "the highest ever reported," and a reviewer
will ask why.

**The 45-countries conflation.** §3.1 still says "the predicted geographic range
of *B. pseudomallei* encompasses 45 countries, many of which have never reported
a confirmed case." Wrong twice. The 45 are countries where it **is** known to be
endemic but under-reported. A separate **34** have never reported it. The
predicted range is much larger than either. The string "34 countr" does not
appear in the file.

A third, which is an overclaim rather than a documented error: the background
states that comparative genomics "has revealed the Australian origin of the
species." Pearson 2009 says verbatim that his conclusions are "contingent on an
Australian root to this tree" and calls it provisional. Chewapreecha offers a
bottleneck alternative she does not exclude. Neither caveat appears.

---

## 4. Errors inside the audit report itself

**The Seng DOI "fix" introduces a wrong DOI.** The audit instructs updating `[80]`
to `doi:10.1038/s41467-024-49939-3`. PubMed gives PMID 38972886, doi
**10.1038/s41467-024-50067-9**. Applying the audit as written replaces a preprint
citation with a broken published one.

**The Lichtenegger roles are inverted.** §7.3 proposes a "Lichtenegger 2024:
formal development and validation of the 4,221-locus cgMLST scheme (distinct from
Lichtenegger 2021 `[99]` which describes application)." Lichtenegger **2021** is
titled *"Development and Validation of a Burkholderia pseudomallei Core Genome
Multilocus Sequence Typing Scheme To Facilitate Molecular Surveillance"* (PMID
33980649). It **is** the development-and-validation paper. The proposed 2024
"validation" paper carries a `10.60692` identifier and could not be found in
PubMed.

**Author initials are wrong in at least two proposed entries.** "Petras AMB" is
Petras **JK**. "Brennan BG" is Brennan **S**. Both verified against PubMed.

**One proposed source is a figshare deposit** (`10.6084/m9.figshare.22730058`,
Wu 2023, Hong Kong typhoon airborne transmission), cited as a study.

The audit's own good finds should not be lost in this. The Lichtenegger-miscited-
as-`[7]` catch is real and important, the orphan resolution was correct work, and
the targeted searches surfaced genuinely useful recent papers, notably Gassiep
2023 on the Queensland flooding outbreak and Webb 2020 on the temperate Western
Australian focus.

---

## 5. What to take from the SciSpace background against ours

They fail in opposite directions, which makes them complementary rather than
competing.

**Take from SciSpace: structure and topic coverage.** Its section plan is better
than mine and should be the outline. It covers ground my corpus does not, in
particular acquired antimicrobial resistance, climate and flooding as range
drivers, PCR-HRM rapid geographic typing, and the Indian, Malaysian and Sri
Lankan clinical literature. 130 citations against my roughly 40. §8, on the
challenge of geographic attribution, is a good qualitative survey.

**Do not take its citations.** As delivered, 34 point at nothing and 46 of the
remaining 96 are flagged. It is not an inspectable bibliography.

**Take from ours: the citation basis and the argument.** `BACKGROUND_RESEARCH_2026-09-02.md`
plus the five `BACKGROUND_SRC_*` files carry PubMed-verified PMIDs and DOIs with
UNVERIFIED marked in place, and they document three caught fabrications. More
importantly they carry the four things that motivate **this** paper and are
absent from the SciSpace background entirely:

- Seng's per-lineage r/m of 3.7, 4.6 and 2.2, the direct comparator for 7.70
- Croucher's 5 to 10 percent detection in the too-clonal regime
- the operating-range concept and Zheng's 5,000-PSD threshold, the only published
  operating number in this species
- Dale 2011's 88.3 percent two-population ceiling, and the fact that **no study
  has ever published an attribution accuracy or misclassification rate**

That last absence is the paper's strongest justification and the SciSpace §8 does
not state it.

**The merge rule.** SciSpace supplies the outline and the topic list. Every
sentence that survives gets its citation re-derived from our corpus or from a
fresh PubMed lookup. No `10.60692`, no Zenodo, no thesis repository, no
conference abstract, and no repository copy of a paper that has a publisher DOI.

---

## 6. Number discrepancies to settle on the workstation

Three, all checkable against `NUMBERS.tsv`, and all currently inconsistent
between the Drive documents and the repository.

| Quantity | Manuscript draft | Plan / `NUMBERS.tsv` | Note |
|---|---|---|---|
| all-unit r/m median | **5.70** (×3: Abstract, Results 3, Discussion) | **5.51** | 5.51 also appears in the draft one paragraph later as the in-window IQR lower bound. Check whether one was copied into the other. |
| Thailand share | "about **70%** one country" | **67%** | Discussion |
| Gate 1 floor | **1,270** | A100 handoff says "a floor of **700**" | Table 3 marks a unit at 955 as below floor, consistent with 1,270. One document is on a stale basis. |

The floor is the number a reviewer will push hardest on, so it should be
unambiguous before anything circulates.

Also unfixed from the last review: the draft's reference list has 20 entries,
in-text markers run `[3]`–`[15]`, and `[1]` and `[2]` are never cited. Probably a
docx conversion artifact, but it must be resolved.

And the strongest reproducibility statement in the project is still not in the
manuscript. Both runs record the same Nextflow Script ID
`e09a5c4eadba2c5984f6790095423ee4`, a hash of `main.nf`. That is stronger than a
shared git commit and belongs in Results 9 or Methods.

---

## 7. What the workstation should run

`verify_references_bp.py` is new in this repo and needs no data.

`BP_background_section.md` is **not** tracked in the repo, so the checkout does
not bring it. Run these from a directory that also holds the Drive copy, or pass
a path to it.

```bash
# 1. Offline structural audit, on whatever copy is current locally.
python3 verify_references_bp.py BP_background_section.md \
        --out REF_AUDIT_background.tsv

# 2. Online pass. Resolves every DOI and flags non-journal targets.
python3 verify_references_bp.py BP_background_section.md --online \
        --out REF_AUDIT_background_online.tsv
```

**Correction to an earlier version of this section.** It listed a third command,
the same audit against `MANUSCRIPT_COMPILED_2026-08-26.md`. That command aborts
with exit 2, and correctly so. Checked directly against the tracked copy on this
branch, the compiled manuscript contains no `## References` heading, no `[n]`
citation marks, no author-year citations and no DOI strings anywhere in its
53 KB. It carries no bibliography at all, so there is nothing yet to audit.

That is worth knowing before step 2 rather than after. For the manuscript the
choice is not between repairing entries and rebuilding, because no entries
exist. The verified corpus goes in as the first bibliography rather than as a
replacement for a broken one, which makes rebuilding from verified sources the
cheaper path by a wide margin, not merely the safer one.

Exit code is non-zero when anything is flagged, so it can go straight into the CI
that Phase 4 of `PLAN_TO_SUBMISSION` calls for, alongside
`test_phylogeography_bp.py`.

Then resolve the three numbers above from `NUMBERS.tsv` and correct the draft.

---

## 8. What I need back from the workstation

Nothing here requires isolate data.

**Correction to an earlier version of this section.** It asked for seven
artifacts as if none were reachable. Six of them are tracked in this repository
and were readable all along: `MANUSCRIPT_COMPILED_2026-08-26.md`,
`RESULTS_DRAFT_2026-08-23.md`, `DISCUSSION_DRAFT_2026-08-23.md`,
`MANUSCRIPT_OUTLINE_2026-08-21.md`, `STATE_2026-09-02.md` and
`PR3_CORRECTIONS_2026-09-02.md`. The list was written from the Drive folder's
contents without checking `git ls-files`, which is the same failure mode this
handoff documents elsewhere. Do not spend time sending those.

What is genuinely absent is every `.tsv`, because no TSV is tracked in this
repository at all.

**Still needed, blocking the number reconciliation:**

1. `NUMBERS.tsv`. The canonical source, with its `QUOTE THIS` / `DO NOT QUOTE`
   annotations. Everything in section 6 resolves from this one file, and it is
   the only blocking item left.
2. Whatever output fixes the Gate 1 floor, most likely the calibration table or
   `gate1_from_alignment_bp.py` output for the reported basis.

**Still needed, not blocking:**

3. The current local `BP_background_section.md`, if it differs from the Drive
   copy. The Drive copy is what section 1 above measured.
4. `PHYLOGEOGRAPHY_ASSOCIATION_FROZEN_2026-08-23.tsv`, to check the 26 / 6 / 37
   stratification quoted in Results 8.

Item 7 of the old list, the manuscript's reference list as markdown, is answered
and withdrawn. There is no reference list. See the correction in section 7.

---

## 9. Feedback on the workstation analysis itself

Asked for, and separable from the citation work above. This is my read of the
analysis as it stands in the A100 handoff, the plan, and the current draft.

**What is being done well, specifically.**

The basis correction is the most important call anyone made this week.
Recognizing that the reported basis is the 85-unit workstation run, and
re-designating the 88-unit A100 run as the cross-hardware control rather than as
production, converted a labelling problem into an asset. The control framing is
the stronger use of that run, and the supporting evidence is better than most
papers manage.

The Script ID finding deserves more weight than it is currently getting. Both
runs record the same Nextflow Script ID, a hash of `main.nf`. That lets you
assert byte-identical pipeline code rather than a shared commit, which is a
stronger claim than the reproducibility statements in most methods sections. It
is still not in the manuscript.

The supersession discipline is unusual and correct. Keeping the wrong Paper 2
claim visible under a banner, rather than deleting it, is what makes the
correction record auditable. Same for `PR3_CORRECTIONS`. Most projects quietly
overwrite and lose the ability to show a reviewer how a number moved.

`NUMBERS.tsv` plus a figure script that exits non-zero on a missing key is the
right structural answer, and it is the single highest-value thing in the plan.
Extending it to every figure and table is what makes a stale number impossible
rather than merely unlikely. Note that the reference audit in section 7 above is
the same pattern applied to citations, and it should join the same CI job.

**Results 8 is the best analytical work in the folder.** Moving from "6 units
survive the BioProject control" to "the confounder is mis-specified, and here is
why" is a real advance rather than a retreat. The argument that submission
accession cannot be a confounder because it is a descendant of country rather
than a common cause, evidenced by 113 of 119 BioProjects being entirely
single-country, is correct, and it generalizes. Controlling for a descendant of
the exposure removes real signal. Reframing the section as country and collection
history not being separable in this collection is more honest and more
interesting than either the original claim or the six-unit version, and it sits
naturally beside the detection window because both say the same thing: an
apparent signal is not a measurement until you have shown what else could produce
it.

**Where I would push back or press harder.**

*The Gate 1 union-coverage caveat is being handled as a disclosure when it is
closer to a limitation of the calibration.* `NUMBERS.tsv` carries
`rm.gate1_caveat` because union coverage does not reproduce the calibration's 76
to 88 percent band. The plan is right that the floor does not depend on it. But
the coverage criterion was one of the two statistics that made the window
defensible in the first place, and a criterion that does not reproduce
quantitatively weakens the claim that the window was measured rather than
chosen. Lead with it in the Results rather than placing it in Limitations, and
say plainly which parts of the window rest on which evidence.

*The floor discrepancy is not cosmetic.* 1,270 against 700 is nearly a factor of
two on the number a reviewer will attack first. Resolve it before drafting
further, and if the two figures are different quantities in different units, say
so explicitly in Methods rather than letting a reader discover it.

*The ClonalFrameML result is computed and unused.* Cross-platform agreement at a
0.00 percent median relative difference, a byte-identical crossover test, and a
Gubbins-versus-ClonalFrameML concordance of Pearson around +0.56 with
ClonalFrameML about 1.74 times higher. None of it appears in the draft. The
concordance number in particular is worth reporting, because a moderate rather
than high correlation between two accepted estimators is a real finding and
stating it pre-empts the reviewer who assumes they should agree tightly. Decide
whether it is a Results finding or a Discussion aside, but do not leave it in a
handoff only.

*Dropping the four pairing units is the right call, and it should be visible.*
Two in-window units is a cheap price for a clean statement, and the alternative
costs A100 scratch retrieval plus compute. Say in the text that four rows were
dropped because the two columns came from runs with slightly different
membership. A reader who later finds 45 where they expected 47 should not have to
reconstruct why.

*E0, E1 and E4 are one bug three times, and the fix should not be an audit.* The
plan proposes auditing every script for defaults that point at a partition or a
run. That is the right diagnosis and the wrong remedy, because an audit is a
one-time act and the bug is generative. Make it a test: a CI check that fails if
any `argparse` default in the repository matches a path-like pattern. Then the
class is closed rather than the three known instances. **See section 12: this is
already done on `main` as `audit_defaults_bp.py`.**

*The determinism framing is right and should be stated exactly as the plan has
it.* The reported run is pinned to a commit predating the seed fix, so re-running
it seeded produces a different run rather than validating the pinned one. The
two-part claim, empirical reproduction now and determinism by construction going
forward, is defensible and both halves are evidenced. Resist any temptation to
soften it into a single sentence that implies more than that.

**One thing I would not do.** The plan lists a ten-unit seeded determinism
demonstration as cheap and high value. It is cheap. But it demonstrates a
property of the fixed pipeline, not of the reported analysis, and a reviewer
could read it as implying the reported run was deterministic. If you run it,
label it unambiguously as a forward-looking check on the corrected configuration.

---

## 10. What this session is and is not useful for

Worth stating explicitly, because the division of labor has already gone wrong
once in a way that cost a pull request.

**This session has no data, by design.** No isolates, no alignments, no trees, no
`NUMBERS.tsv`. I cannot verify that a number is correct. I can only verify that
it is *consistent* across the documents I can see, which is a much weaker claim
and should never be reported as the stronger one. Every number I have commented
on in this handoff is a cross-document consistency finding, not a measurement.

**What it is genuinely good for.**

Literature and citation verification, which is what section 1 to 4 above are.
PubMed, Crossref and DOI resolution are available here and the checks are
mechanical, repetitive and exactly the kind of thing that degrades when done by
hand at volume.

Adversarial reading of claims against sources. The per-allele conflation, the
45-countries conflation and the Lichtenegger inversion were all found by
comparing an assertion against a primary record, not by domain intuition.

Cross-document consistency. Four documents in the Drive folder disagree about the
all-unit median, the Thailand share and the Gate 1 floor. Nobody reading one
document at a time would see it.

Writing tools that run without data. `verify_references_bp.py` and
`test_phylogeography_bp.py` were both built and validated here on synthetic
input, then handed over to run against the real thing.

Drafting and restructuring prose, and arguing about what a paper should claim.

**What it is bad for, and the failure that proves it.** Earlier in this project I
built on a tree 89 commits and two weeks behind `main`, never fetched to check,
and produced a manuscript whose headline r/m was correct for the tree I could see
and wrong for the real one. The lesson is not that I should try harder. It is
that **this session cannot detect that its inputs are stale**, so staleness has to
be prevented on the input side.

A second instance of the same failure, found while correcting this handoff.
Section 8 originally asked the workstation to send seven text artifacts. Six of
them were tracked in this repository and readable at any point. That list was
written from the Drive folder's contents without running `git ls-files`. The
pattern is identical: an inventory taken from the nearest visible surface and
then reported as the whole picture.

**The division of labor that follows.**

The workstation owns every number. Anything quantitative should originate in
`NUMBERS.tsv` and flow outward. If I quote a figure that did not come from a file
someone handed me in this session, treat it as unverified regardless of how
confident it sounds.

This session owns the citation basis, cross-document consistency, adversarial
review, and data-free tooling.

**What that requires from your side, every time.** Pin what I read. Give me
`NUMBERS.tsv` and the current versions of whatever documents matter, and say
which commit or which basis they are on. A dated filename is not enough, because
`PUBLICATION_STRATEGY_2026-09-02.md` currently carries a corrected Paper 2 banner
above a header still describing the 88-unit basis, 2,342 genomes, r/m 7.38 and 70
percent Thailand. Anyone reading it top to bottom, including me, meets the
superseded numbers first.

---

## 11. Recommended order

1. Run the two `verify_references_bp.py` commands in section 7. Minutes.
2. Decide the background's fate. My recommendation is to **keep its outline and
   rebuild its bibliography**, rather than repair 34 dangling and 46 flagged
   entries in place. Rebuilding from our verified corpus is less work than
   auditing someone else's, and it ends with a bibliography that can be
   inspected.
3. Fix the three content errors in section 3. They are three sentences.
4. Reconcile the three numbers in section 6 from `NUMBERS.tsv`.
5. Add the Script ID to Methods.
6. Then, and only then, merge background prose into the manuscript.

Separately, and not blocked by any of the above: resolve the Gate 1 floor, report
the ClonalFrameML concordance somewhere in the paper rather than only in a
handoff, and read section 12 before acting on the E0/E1/E4 default audit, which
an earlier draft of this list asked for and which already exists on `main` as
`audit_defaults_bp.py`, wired into CI.

The background is not on the critical path. `PLAN_TO_SUBMISSION` is right that
IRB and the data availability statement are, and neither depends on any of this.

---

## 12. Three findings from reading current `main`, added after the sections above

I rebased this session onto `origin/main` at `27da6cc` before writing anything to
the repository, having previously worked from `32a08a4`. That changed three
things in the sections above and surfaced one live defect.

**A. The caterpillar test passes on `main`, but for an incidental reason, and one
docstring is wrong.**

**Correction.** An earlier version of this section claimed the test suite on
`main` was failing. It is not. CI on `main` runs `test_phylogeography_bp.py` and
reports ALL PASS, including *"caterpillar depth 20000 does not overflow"*. I
inferred the failure from reading the code rather than running it, and the
inference was wrong. Also worth recording: CI now exists on this repository, four
jobs, so Phase 4 item 1 of `PLAN_TO_SUBMISSION` is already done.

What is actually true is smaller and still worth fixing.

PR 5 correctly ported E0, the preflight and the exact single-country enrichment,
all three confirmed present. It did not port the parser and scorer rewrite, so
`parse_newick` and `fitch_score` on `main` both still recurse, one frame per
level of nesting.

The 20,000-tip caterpillar check survives that only because of a side effect.
`fitch_score` calls `sys.setrecursionlimit(100000)` at line 148. `test_fitch()`
runs its small `fitch_score` checks before it builds the caterpillar, so the
process-wide limit is already raised to 100,000 by the time the recursive parser
is asked to descend 20,000 levels. **The test passes because an unrelated
function raised a global limit first.** Reorder the checks, or make `fitch_score`
iterative without carrying the `setrecursionlimit` call across, and it breaks.
That is how I hit it locally against the PR 3 versions, where the iterative
`fitch_score` never raised the limit and the parser then died at the default
depth of 1,000.

Two small things follow. `fitch_score`'s docstring opens *"Fitch small parsimony,
iterative post-order to avoid recursion limits"* directly above `def rec(node)`,
which describes code that is not there and should be corrected either way. And
the caterpillar check is currently a test of the recursion limit rather than of
the parser, so if the iterative versions are ever ported, port both together.

None of this is a correctness risk to any reported number. At real unit sizes,
the largest being 159 tips, recursion depth is never close to binding.

**B. The Thailand share depends on which set is being described, and three
different figures are in circulation.** `phylogeography_association_bp.py` on
`main` documents **66.4%** for the v4c analysed set of 2,352 genomes over 86
units. `PLAN_TO_SUBMISSION` says **67%**. The manuscript Discussion says **about
70%**. These are probably all correct for different denominators, which is worse
than a simple error because each looks right in isolation. Pick the reported
basis, state its denominator in the text, and make it a `NUMBERS.tsv` key.

**C. The geography result on `main` is better than the version I was reviewing,
and section 5 above understates it.** The manuscript banner reports 26 units
clustering by country with no control, **18 to 24** retained under the correctly
specified control, and **6** under the submission-accession discriminant, with
the observation that the discriminant over-adjusts because country causes
BioProject rather than the reverse. Reporting the range with its mechanism is the
right call and is stronger than any point estimate would have been. My earlier
framing of "6 units surviving the control" was reading the conservative end as
the answer.

The associated code improvements are also on `main` and were not in what I
reviewed: Benjamini-Hochberg q-values across the country family only, an explicit
`control_status` of ok, vacuous or absent, and normalization of the literal
`"unknown"` bioproject across 274 tips that would otherwise have formed one
spurious 274-member study. That last one matters in the direction that is easy to
get wrong: measurement error in a confounder understates it, which biases toward
a false positive for geography. Catching it strengthens the negative result.

**Where to get this.** Sections 1 to 11 were written against the Drive copies and
the repository as of `27da6cc`.

Both new files are on branch **`claude/citation-audit-2026-09-03`**, open as
**PR #21**, based on current `main` and independent of #5. A fresh branch was
used rather than `claude/bp-genomics-research-t1b68u`, because that branch still
points at the closed #3 commits and rebasing them forward would have
reintroduced exactly what #5 deliberately avoided.

```bash
git fetch origin claude/citation-audit-2026-09-03
git checkout claude/citation-audit-2026-09-03
```

CI is green on the head commit, all four jobs. Nothing is pending on my side.

One further note on section 9. It recommends turning the E0/E1/E4 dangerous-default
problem into a CI check rather than a one-time audit. **That already exists on
`main` as `audit_defaults_bp.py`**, and its own comment makes the case better
than mine did: six instances of the bug found in this repository, every one
producing a plausible wrong number rather than an error, all six found by
accident, and the worst would have written r/m 8.05 into the manuscript instead
of 7.70. So that recommendation is already implemented and the class is closed.
`verify_references_bp.py` is intended to sit alongside it as a fifth job.
