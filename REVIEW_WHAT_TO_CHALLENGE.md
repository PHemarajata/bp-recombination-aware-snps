# Where I would attack this

Written by the analysis side, naming the weakest joints rather than waiting for a
reviewer to find them. Ordered by how much damage a successful challenge would do.

If you have limited time, challenges 1, 2 and 5 are the ones that would move
conclusions. The rest would force rewording.

---

## 1. The floor is the load-bearing number and it rests on three units

**The claim.** Recombination detection has a lower bound near 700 mean pairwise core
SNPs, below which a low r/m is a detection failure rather than a clonal population.
Everything downstream depends on it, because it decides which units enter the
headline median at all.

**Why it is vulnerable.** Only three units sit below the bracket. The bracket
(588, 755] is narrow, but a bound located by three observations is a bound located
by three observations. The supporting evidence is also, on its own terms,
inadmissible in a way the manuscript admits: two of the three below-floor units are
unambiguous mixtures, so their failure is attributable to structure rather than
diversity, and the third cannot be assessed because modality is only interpretable
inside the diversity range whose lower bound is the quantity being derived. That
circularity is real and was not broken.

**The defence, and judge whether it holds.** The bound was located on union
recombination coverage and median tract length, never on r/m, so it is not chosen to
maximise the result. And the answer is insensitive across the bracket: 588, 700, 755
and 840 give 7.70, 7.70, 7.74, 7.78.

**What would settle it.** A unimodal unit of n >= 25 sitting between roughly 535 and
1,265 mean pairwise SNPs. This partition does not contain one.

---

## 2. The window's second criterion does not reproduce

**The problem.** The original calibration justified the window partly on union
recombination coverage of 76-88% for in-window clusters. In this panel, coverage
never reaches that band anywhere: the maximum band median is 68%, and coverage
*rises* with diversity, peaking in the bands the gate rejects.

**Why this matters more than it looks.** Coverage was one of the two statistics that
made the window defensible as *measured* rather than *chosen*. If one of the two
criteria does not reproduce quantitatively, the claim that the window was measured is
weaker than the text implies.

**The defence.** The floor does not depend on it, being located by a 4.3% to 28.0%
jump far from the disputed range, and the tract-length criterion does reproduce.

**Push here on whether the disclosure is placed correctly.** It is currently a
disclosure. An argument can be made that it belongs in the Results as a limitation of
the calibration rather than in the Limitations as a caveat.

---

## 3. Four values of the same statistic are in circulation

r/m is 7.70, 7.26, 7.44 or 7.38 depending on partition and distance metric. Only 7.70
is reported. `GATE1_ALIGNMENT_RESULT_2026-08-21.md` section 7c tabulates all four and
they differ by less than 6%, which is exactly what makes them dangerous: a value from
the wrong cell reads as a rounding discrepancy rather than a different analysis.

**What to test.** Take any r/m in any document in `repository/` and establish which
cell it belongs to. If you find one that cannot be placed, or one placed wrongly, that
is a real finding. Several documents carry corrected banners above uncorrected bodies.

---

## 4. Attribution rests on 46 genomes, and five regions, two of which have two

Every regional error falls in the two regions with n = 2. Where a region has six or
more it is 41 of 42. The framing offered is that this is a sampling statement with a
named remedy rather than an accuracy ceiling.

**The challenge.** That framing is convenient. It is also testable: it predicts that
adding references from the Americas outside Colombia and from Africa moves those two
cells and leaves the rest alone. Until that is done, "the method works and the panel is
thin" and "the method fails outside dense regions" fit the same 46 observations.

**The strongest counter available to us** is the depth control: region is right on 19
of 22 genomes with no close relative anywhere in the panel. If sparsity alone drove
performance, that number should collapse. Judge whether it carries the weight.

---

## 5. The regional result may be partly a labelling artifact

**The uncomfortable version.** Two of the five errors are Mississippi genomes assigned
to Latin America and Caribbean. Their sequence type spans seven countries, all in the
Americas. Two more are African genomes assigned to the same region, and African and
South American isolates are published as one clade.

The manuscript reads these as the scheme cutting real lineages, which is favourable.
**A reviewer could read the same fact the other way**: if regional labels cut across
lineages, then regional accuracy is partly measuring how well the World Bank regions
happen to align with *B. pseudomallei* phylogeography, not how much geography the
genome carries. The 89% would then be a property of the label set as much as of the
data.

**This is the challenge I would most want an independent answer on.** The internal
evidence for the favourable reading is that Asia-vs-not is perfect and SEA-vs-not is
poor, which shows performance tracks phylogenetic structure rather than label
coarseness. Whether that is sufficient is a judgement call.

---

## 6. Country attribution is reported as a measured ceiling; it could be a power problem

22% against a 26% baseline over 46 genomes and 16 classes. With that many classes and
that few genomes, the confidence interval is wide.

**The defence, and it is the strongest single piece of evidence in the attribution
work:** scoring the same genomes on 7-locus MLST gives country 0 of 33 and region 17 of
33. Going to 4,221 loci moves region from marginal to 89% and leaves country below its
baseline. Three orders of magnitude more information lifts one and not the other, which
is hard to explain as a power problem.

---

## 7. The grafted global tree mixes branch-length scales

Backbone edges are substitutions per site over the parsnp core; within-unit edges are
over recombination-filtered variable sites, differing by roughly 133-fold. The tree is
used only as a topology aid, is drawn as a cladogram, and every artefact carries the
warning. **Check that no downstream claim quietly depends on its branch lengths.** No
rate or date is derived from it, and no r/m.

---

## 8. Places where the documents disagree with each other

The repository contains superseded results kept deliberately visible under correction
banners rather than deleted, which is good practice and also a hazard: a document read
top to bottom can present a superseded number before its correction.

Known instances, all in `repository/`:

- `PUBLICATION_STRATEGY_2026-09-02.md` carries a corrected banner above a header still
  describing the 88-unit basis and r/m 7.38.
- `GATE1_ALIGNMENT_RESULT_2026-08-21.md` has correct tables and a body that uses the
  pre-reversal run labels, flagged in its own reading note; its section 9 is superseded
  by its section 7b and carries a banner saying so.
- `MANUSCRIPT_COMPILED_2026-08-26.md` has no bibliography at all and predates several
  corrections. `MANUSCRIPT_DRAFT_2026-09-02.md` is the current draft.

**If you find a disagreement not on this list, that is a genuine finding.**
`REVIEW/DOCUMENT_MAP.md` gives status for all 93 documents.

---

## 9. What is not evidenced here at all

- **The pipeline repository is absent.** Variant calling and recombination inference
  run in `wf-assembly-snps-mod`. You can verify that both runs executed identical code
  via the shared Nextflow script hash, but you cannot read that code here.
- **No end-to-end rerun since the methods freeze.** Outstanding, and acknowledged.
- **Isolate-level data is withheld** under the data policy. See
  `REVIEW/DATA_GOVERNANCE.md` for what was substituted so the numbers stay checkable.
