# The background section cites a different bibliography from the one it prints

Found while working open item 2 of `HANDOFF_2026-09-04.md`, which was to source
the 34 dangling citations in `BP_background_section.md`. The dangling citations
are real, and they are the smaller half of the problem.

**`BP_background_section.md` contains two bibliographies with two different
numberings. The prose follows one of them. The `## References` list is the other
one.** They agree on `[1]` through `[40]` and disagree on everything after.

Per-number detail is in `BACKGROUND_BIBLIO_COMPARISON.md`, one row per citation
number with what each bibliography says it is. Regenerate it, and the TSV
alongside it, with `compare_bibliographies_bp.py`.

---

## The measurement

277 citation marks in the prose, counting each occurrence.

| where the mark lands | marks | share |
|---|---|---|
| the paper the sentence means | 102 | 37% |
| **a different paper** | **136** | **49%** |
| nothing at all | 36 | 13% |
| undecidable, one side has no DOI | 3 | 1% |

By reference number rather than by mark, of the 96 entries in the printed list:

| | n |
|---|---|
| agrees with the body block | 39 |
| **disagrees** | **54** |
| undecidable, `[7]` `[57]` `[59]` | 3 |
| numbers cited with no entry in the list at all | 34 |

`verify_references_bp.py` reports 40 and 56 rather than 39 and 54 for the same
file. The difference is the three undecidable rows: the table above compares DOIs
only and abstains where one side has none, while the audit falls back to
comparing title words, which decides all three. Neither is wrong; the audit is
built to fail loudly and the table is built to be read, so the table abstains
where the evidence is a word overlap rather than an identifier.

The two numberings drift apart in steps. Matching the two bibliographies by DOI
gives an offset of 0 for block entries `[1]`-`[40]`, +1 for `[42]`-`[50]`, and
+2 for `[52]`-`[98]`. Two entries were inserted into one list and not the other,
and everything below each insertion shifted.

## Which numbering is authoritative

The prose. It was checked by reading sentences against both candidates, not by
assuming.

| the sentence citing it is about | body block says | printed list says |
|---|---|---|
| `[52]` incidence in Kenya | Population-Based Estimate of Melioidosis, Kenya | Currie and Kaestli, a global picture of melioidosis |
| `[55]` serological exposure in Nigeria | Serologic Evidence of Exposure, Nigeria | Birnie, melioidosis in Africa |
| `[56]` burden estimates from suitability modeling | Global Burden and Challenges of Melioidosis | Wiersinga, pathogenicity |
| `[59]` Tier 1 select agent status | Clinical Features and Laboratory Diagnosis of Infection with the Potential Bioterrorism Agents | Pongmala, distribution within a 300 cm soil profile |
| `[60]` two-phase ceftazidime and eradication therapy | Treatment and prophylaxis of melioidosis | Hogan, melioidosis in Trinidad and Tobago |

Five for five, the body block matches the claim and the printed list does not.
`[68]` matches neither, so the drift is not a single clean offset everywhere.

Two numbers, `[123]` and `[128]`, have block entries and no prose mark at all.
That is not a defect. Those two sentences were corrected in an earlier session
and now cite inline, as "(Meumann et al., PMID 33754984)" and "(PMID 27303718)",
which is a third citation style in the same document and the only one in it that
is currently reliable. The transatlantic slave trade clause that `[128]` could
not support was removed at the same time.

## Why no audit caught it

Because there was nothing for a dangling-and-orphan audit to see. Every number
in `[1]`-`[96]` has an entry, and every entry is cited. Dangling is 0 across that
range and orphans are 0. **The counts are perfect and the citations are wrong.**

This is a new failure mode for this project's collection. The others were a
number that could not be found, a number that was found and disagreed with
another number, or an entry that named a paper which did not exist. This one is
a number that resolves cleanly, to a real paper, that the sentence is not about.
A reviewer spot-checking three references drawn from `[1]`-`[40]` sees nothing.

`verify_references_bp.py` now checks for it. Where a document carries a second
bibliography in its body, the two are compared entry by entry and any
disagreement fails the run. It is not gated behind `--warn-only` and it is not
subject to the `--max-dangling` ratchet, because both of those exist to let an
*incomplete* list through while it is being built, and this is not incompleteness.

Verified in both directions on a synthetic pair: identical bibliographies report
0 disagreements and exit 0; changing one entry reports 1 disagreement, names the
number, and exits 1.

## What this does to the scope decision

`BACKGROUND_SCOPE_DECISION_2026-09-03.md` concluded that the remaining citation
work was "five lookups, not sixty-five", on the premise that the 96 printed
entries were sound and only the 34 dangling ones needed attention. **That premise
is false and the conclusion does not survive it.** 54 of the 96 need replacing,
not because they are low quality but because they are the wrong papers.

The section-by-section scope call in that document is unaffected. Sections 6, 7
and 8 are still the parts worth keeping, and the manuscript's Introduction is
still better sourced than the background's. What changes is the cost of using any
of it: no citation in the background above `[40]` can be quoted without checking
it first, including the ones in the sections that were kept.

## The body block is not a usable replacement either

The obvious repair is to delete the printed list and promote the body block,
since the block is what the prose means. That would trade one defect for a worse
one. The block is a SciSpace export and its entries mix correct and invented
fields within a single record:

| | title | DOI | PMID |
|---|---|---|---|
| `[99]` | a cluster-analysis paper | `10.1128/JCM.02519-20` | 33980649, which is the cgMLST scheme paper, a different work |
| `[101]` | "Locally Acquired Melioidosis, United States, 2022" | `10.1056/NEJMoa2305248` | 38118023, which is Petras, whose DOI is `10.1056/NEJMoa2306448` |
| `[103]` | correct | `10.3201/eid3107.250235` | 40835221, whose DOI is `10.3201/eid3109.250804` |

Eleven entries carry the full fabrication signature recorded in
`REFERENCES_RESOLVED_2026-09-03.md`: a `10.60692` prefix, no journal field, and a
title that paraphrases the sentence citing it. `[123]`, `[124]` and `[128]` are
among them, and all three stand in for real papers that were easy to find.

So promoting the block would produce a reference list that is aligned with the
prose and populated with identifiers that point at the wrong records. The
alignment defect would disappear from the audit while the citations stayed wrong,
which is strictly worse than the current state, where at least the defect is
visible once you look for it.

## What has to happen

**All 130 references need resolving against a primary record.** Not the 34
dangling ones, and not the five the scope decision named. There is no subset that
can be trusted without checking, because the failure is not concentrated: it
starts at `[41]` and runs to the end.

Nine are already done and verified against PubMed in
`REFERENCES_RESOLVED_2026-09-03.md`: `[99]` `[100]` `[101]` `[103]` `[123]`
`[124]` `[125]` `[127]` `[128]`. `[102]` is closed as unsupported and must not be
used. That leaves 120.

This is a real piece of work and it is not on the critical path to submission.
`PLAN_TO_SUBMISSION_2026-09-02.md` is right that the background is not what
completes the Introduction, and the manuscript's own 34 references are now
complete, verified and internally consistent. The decision this finding forces is
narrower than it looks:

1. **If the background is only ever supporting material**, mark the file as
   having no usable bibliography above `[40]` and leave it. Done below.
2. **If sections 6, 7 and 8 are to be drawn on for the Discussion**, resolve the
   references those three sections cite before quoting any of them. That is a
   bounded subset and it can be counted from the comparison table.
3. **If the standalone review is ever wanted**, all 130 have to be done.

Nothing here should be repaired by hand in place. The printed list cannot be
patched entry by entry into correctness, because the number a patch would be
applied to is itself the thing that is wrong.

## Files

| file | what it is |
|---|---|
| `BACKGROUND_BIBLIO_COMPARISON.md` | one row per citation number: prose mark count, verdict, fabrication flag, and what each bibliography says. Tracked |
| `compare_bibliographies_bp.py` | generates that table, and a TSV beside it. Exits 1 while any number disagrees |
| `verify_references_bp.py` | now detects and fails on rival-bibliography disagreement |
| `REFERENCES_RESOLVED_2026-09-03.md` | the nine that are verified, and why `[102]` is closed |

The TSV is not tracked and is not meant to be. Rule 5 of `.gitignore` excludes
`*.tsv` as belt and braces against isolate data reaching the repository, and says
in terms that a future loosening must not silently start tracking it. This table
carries citation metadata and no accessions, but the right response to a rule
written that way is to commit the generator and the Markdown, not to force-add
past it.
