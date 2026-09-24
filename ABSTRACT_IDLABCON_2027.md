# ID Lab Con 2027 abstract, draft 2026-09-24

APHL ID Lab Con 2027, Hyatt Regency Atlanta, March 15-18, 2027. The call for
abstracts is open and **closes October 2, 2026**, confirmed against the APHL
event page on 2026-09-24. Three submission types (plenary, roundtable, poster)
and seven tracks. This one fits **Pathogen Genomics**, with **Biosafety and
Biosecurity** as a plausible second given the Tier 1 select agent framing.

The word limit and any required headings are still unconfirmed, see open item 1.

**Scope note.** This abstract covers the *global attribution* work tracked in
this repository: 2,959 genomes, 85 recombination-aware analysis units, and
accuracy measured against 46 documented-exposure cases. It is **not** the
Nakhon Phanom paired human and residential isolate study. That dataset does not
appear anywhere in this repository, and the two should not be conflated.

Source of every number: `ABSTRACT_DRAFT_2026-08-23.md`, which draws from
`NUMBERS.tsv` on the frozen basis `FINAL_BASIS_2026-08-22/`. `NUMBERS.tsv` is
not in this repo (it is generated, and the working copy moved to the Mac on
2026-09-14). Revalidate before submission with `freeze_basis_bp.py` and
`generate_numbers.py`.

---

## Title

**When genomics cannot tell you where a melioidosis patient was exposed: a
measured accuracy floor for country attribution, and what to report instead**

Alternate, shorter: **Country attribution of melioidosis exposure does not
exceed chance, and regional attribution does**

## Authors

[AUTHORS]. Association of Public Health Laboratories, [AFFILIATION LINE].

## Submission type

**Plenary or oral.** The finding is a single measured result that changes what a
laboratory reports, which is what that format is for, and a negative result needs
the speaking time to establish that the instrument works before the absence lands.
Poster is the fallback if the plenary slots go elsewhere. Roundtable is the wrong
fit here, because the abstract answers a question rather than opening one.

---

## Version A, structured, 323 words

**Background.** *Burkholderia pseudomallei* causes melioidosis across the
tropics and is a Tier 1 select agent. Locally acquired cases on the Mississippi
Gulf Coast and a presumptive focus in Georgia have made exposure origin a
domestic question for US laboratories. When a patient has no travel history,
clinicians ask the laboratory to name the place of exposure from the genome. No
published study reports how often that answer is right, at any geographic scale.

**Methods.** We assembled 2,959 *B. pseudomallei* genomes, 41% of publicly
archived isolates carrying a recorded country, and partitioned them into
recombination-aware analysis units. Accuracy was measured against 46 cases from
45 individuals with independently documented exposure, under a holdout removing
both same-country reference genomes and same-source outbreak isolates.

**Results.** Country attribution did not exceed chance, at 10 of 46 (22%)
against a 26% majority baseline, kappa 0.19. Regional attribution reached 41 of
46 (89%) against a 46% baseline, kappa 0.83, and the Asia versus elsewhere split
was recovered without error. Among the 14 cases with a close relative in the
panel, region was correct 14 of 14 and country 2 of 14. Country accuracy stayed
flat across a 584-fold range of genomic resolution, from 7 MLST loci to
whole-genome recombination-filtered SNPs, while regional accuracy rose from 50%
to 82%. The same pipeline separated 19 relapses from one reinfection across 20
recurrence pairs (1 to 14 versus 1,102 SNPs), so the limit is not the assay.
Seven of 16 exposure countries have no public genome, all of them in Latin
America and the Caribbean, and some lineages span continents. A published US
autochthonous cluster differs from a Viet Nam-acquired case by one cgMLST locus
in 4,221.

**Conclusions.** Report exposure attribution by geographic scale, with region
stated and country withheld. A laboratory can say a case is consistent with
acquisition in South Asia. It cannot yet say which country. Closing the
reference gap in the Americas is a prerequisite for anything finer.

---

## Version B, structured, 192 words (if the limit is tighter)

**Background.** Melioidosis increasingly presents without a travel history,
including locally acquired cases in the continental United States, and
laboratories are asked to name the place of exposure from the genome. No
published study reports how often that answer is right.

**Methods.** We assembled 2,959 *Burkholderia pseudomallei* genomes and scored
attribution against 46 cases from 45 individuals with documented exposure, under
a holdout removing same-country and same-source reference isolates.

**Results.** Country attribution did not exceed chance, at 10 of 46 (22%)
against a 26% baseline, kappa 0.19. Regional attribution reached 89% (kappa
0.83), and the Asia versus elsewhere split was recovered without error. Among
the 14 cases with a close relative available, region was correct 14 of 14 and
country 2 of 14. Country accuracy was flat across a 584-fold range of genomic
resolution, which points to absent signal rather than insufficient resolution.
Seven of 16 exposure countries have no public genome, all of them in Latin
America and the Caribbean, and some lineages span continents.

**Conclusions.** Report exposure attribution by geographic scale. Region is
defensible today, country is not, and the reference gap in the Americas has to
close before that changes.

---

## Why these numbers and not others

**Baselines stay in, every time.** "22%" on its own reads as partial success.
"22% against a 26% baseline" is the finding. The same holds for 89% against 46%.

**45 individuals, not just 46 cases.** Two isolates come from one patient. It
costs four words and answers the question before it is asked.

**The recurrence clause earns its space.** The first objection to any negative
result is that a better method would have worked. The relapse and reinfection
separation answers it with the pipeline's own output rather than with an
argument. It is the sentence to protect if the word limit bites.

**The one-locus US and Viet Nam clause.** Without it the work reads as "we did
not have enough reference genomes", which is only half the story and the weaker
half. With it, the ceiling is a property of the organism as well as of the
collection.

**Left out on purpose.** The recombination operating range and r/m 7.70 are
load-bearing for the methods paper, not for this audience. The abstention rule
(region 94% on 76% of cases at an allelic distance of 0.462) is a good slide and
a poor abstract sentence, because it needs the threshold explained. The South
Asia burden inversion (2.5% of genomes, 44% of predicted cases) is a strong
closing slide for the same reason.

---

## Open items before submission

1. **Call for abstracts.** The deadline (October 2, 2026), dates, submission
   types and tracks are confirmed above. The **word limit and any required
   headings are not**, and the APHL submission portal is the place to check.
   Both versions above assume Background, Methods, Results, Conclusions.
2. **Author list and order.** Not drafted. [AUTHORS] is a placeholder.
3. **Revalidate every number** against `NUMBERS.tsv` on the current frozen
   basis. The panel figure in particular: 2,959 is the deduplicated panel and
   2,976 is the count of assemblies considered, and the two are not
   interchangeable.
4. **"41% of publicly archived isolates with a recorded country"** is the
   careful phrasing. Read as "41% of all public *B. pseudomallei* genomes" it is
   wrong, and the correct figure there is 36.8%.
5. **Select agent and metadata clearance.** `PUBLICATION_STRATEGY_2026-09-02.md`
   flags data availability as the highest-risk item across all three papers,
   because the metadata joins accession to location, date and exposure label.
   A conference abstract is lower stakes than a manuscript, but this is an APHL
   meeting and internal clearance should happen before submission, not after.

   The lift here is lighter than for a partner-isolate abstract, and that is
   the main practical argument for this submission over the Nakhon Phanom one
   with eight days left. Per `METHODS_DRAFT_2026-08-19.md` §2.12.11a.2, the 48
   exposure-labelled genomes (46 scorable) are CDC submissions carrying an
   explicit `ex <country>` label, older assemblies with the exposure country in
   the assembly name, and cases documented in the published literature. No
   partner institution has to release unpublished isolates for this abstract to
   go out.
6. **Relationship to the manuscripts.** This is the attribution work, listed as
   Paper 3 in the publication strategy and the least finished of the three. The
   abstract cites calibration work that is still unpublished. That is normal for
   a conference, but the talk needs one slide on why the recombination
   correction is trustworthy.
