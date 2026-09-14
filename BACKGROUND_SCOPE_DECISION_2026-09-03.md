# Which of the background actually enters the manuscript

Step 6 of `HANDOFF_CITATIONS_2026-09-03.md` section 11, taken before the rest of
step 2 rather than after it. The order was swapped deliberately: step 2 was about
to spend roughly 130 PubMed lookups sourcing 65 references, and sourcing a claim
that is then cut is wasted work. Sourcing it *badly* in order to keep it is
worse.

## The finding that drives everything else

**The manuscript's Introduction is already complete, and the background is not
what completes it.**

`MANUSCRIPT_DRAFT_2026-09-02.md` Introduction is seven paragraphs carrying about
fourteen references, all from the PubMed-verified corpus. It already argues, in
order: the organism's ecology is what makes its genome informative about place;
the burden is large and unevenly observed; exposure history is unreliable and
genomics has repeatedly supplied what history could not; those results are all
SNP-distance arguments and SNP distances here are dominated by recombination;
within-clade restriction-modification makes partitioning a biological requirement
rather than a convenience; every published analysis therefore subdivides; and the
rule cannot be implemented because no operating limit has ever been published.

That is the paper's argument, and it is tighter than the background's.

Two specific checks make the point. Handoff section 3 lists two content errors in
the background, the per-allele conflation and the 45-countries conflation. **The
manuscript already has both right.** Its Introduction states the 45 endemic and
under-reported countries against a further 34 that have never reported, and it
states the per-allele MLST figure as 18 to 30 while saying outright that it "is
not comparable to any per-site genome-wide estimate and should not be placed
beside one". The background needed those corrections. The manuscript did not.

So the background is not the Introduction's source. Whatever it is for, it is not
that.

## Section-by-section

| Background section | Verdict | Why |
|---|---|---|
| 1. Introduction | **out** | The manuscript has its own, and it is better |
| 2.1–2.4 Disease overview, clinical spectrum, risk factors, diagnosis and treatment | **out** | Clinical management is not what a method-calibration paper motivates from. The treatment material is the acquired-resistance block, on which see below |
| 3.1 Estimated global burden | **already in** | Introduction paragraph 2, with the credible intervals and the South Asia burden-against-sequencing asymmetry the background does not have |
| 3.2 Endemic regions | **out** | Not load-bearing for any claim in the paper |
| 3.3 Emerging and under-recognised regions | **partial** | The Mississippi and Georgia autochthonous foci are relevant to attribution, and Mississippi is already cited in the Introduction |
| 3.4 Travel-associated melioidosis | **partial** | This is the paper's applied motivation, but Introduction paragraph 3 already carries it through three worked cases |
| 4.1 Soil and water reservoirs | **partial** | One clause of Introduction paragraph 1 already does this work |
| 4.2 Routes of infection | **out** | |
| 4.3 Seasonality, 4.4 Climate change and range expansion | **out** | Range expansion is a real topic and a different paper. Nothing in this manuscript's argument turns on it |
| 5.1 Bipartite chromosome | **keep, for Methods** | The two-replicon structure is why r/m is computed per replicon and summed. Methods needs this, the Introduction does not |
| 5.2 Genomic islands, 5.3 pan-genome | **out** | |
| 5.4 Recombination as a dominant force | **already in** | Introduction paragraph 4, better sourced, with the per-allele trap named explicitly |
| 5.5 Virulence genomics | **out** | Virulence is not this paper's subject |
| 6.1 Global population structure and biogeographic separation | **keep** | Directly supports the secondary aim, that geographic structure survives recombination correction |
| 6.2 Australian origin and dispersal | **keep, hedged** | Only with the root-contingency caveat applied on 2026-09-03. Discussion already notes the global tree recovers known biogeography |
| 6.3 Regional and fine-scale structure, 6.4 genomic clades | **keep** | Relevant to what resolution is achievable, which is Results 8 and the Discussion |
| 7.1 MLST, 7.2 homoplasy and recombination | **keep** | 7.2 is direct support for the country-level negative result: homoplasy is a mechanism for why shared ST does not mean shared origin |
| 7.3 WGS and cgMLST | **keep** | This is the attribution method the paper uses |
| 7.4 Source attribution and outbreak investigation by WGS | **keep** | Closest prior art to what the paper does |
| 8. The challenge of geographic attribution | **keep, the most valuable section** | Handoff section 5 calls it a good qualitative survey, and it is the qualitative frame for Results 8. It still lacks the paper's strongest point, that no attribution accuracy or misclassification rate has ever been published |
| 9. Conclusion | **out** | |

## What this means for the citation work

The in-scope sections are **6, 7 and 8**, plus 5.1 for Methods and fragments of 3
that the Introduction already covers. Mapping the 34 dangling citations onto
that:

**In scope, and needed (11):** `[97]` `[99]` `[100]` `[101]` `[102]` `[103]`
`[123]` `[124]` `[125]` `[127]` `[128]`. Six of these are already resolved:
`[99]` `[101]` `[103]` `[127]` `[128]`, and `[101]`/`[103]` are arguably already
covered by the Introduction's existing citations.

**Out of scope, do not source (23):** `[98]` soil heterogeneity; `[104]`–`[111]`
the entire acquired-resistance block, eight references on ceftazidime and
meropenem mechanisms, PenA structural mutations, *bpss1219*, efflux regulators
and ARDaP; `[112]`–`[122]` the climate and rainfall block, eleven references;
`[126]` virulence GWAS; `[129]` the goat farm; `[130]` typhoon airborne
transmission.

**So the remaining work is five lookups, not sixty-five:** `[97]` `[100]` `[102]`
`[123]` `[124]` `[125]`, less those already done.

## What the background is actually for

Not the Introduction. Two honest uses remain, and they are different
deliverables:

1. **Sections 6, 7 and 8 as supporting material for Results 8 and the
   Discussion**, where the paper argues about what spatial resolution is
   achievable. Section 8 in particular is the qualitative frame that the
   manuscript currently states only in its own terms.
2. **A standalone review**, if that is ever wanted. In that case the whole
   bibliography does need rebuilding and the 23 out-of-scope references come back
   into play. That is a separate decision and a separate piece of work, and it
   should not be done on the way to submitting this paper.

`PLAN_TO_SUBMISSION` is right that the background is not on the critical path.
This decision keeps it off.
