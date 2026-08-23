# Acquisition scope — validation power, not reference density

2026-08-22. Scopes the alternative to Phase 1: acquiring genomes that add
**held-out ground truth**, after the downsampling control
(`DOWNSAMPLING_CONTROL_RESULT_2026-08-22.md`) showed reference density is already
saturated where it can be bought.

**One-line recommendation: pursue the free half (metadata mining) now; gate the
paid half (targeted sequencing) on whether a specific stratum needs tightening,
because neither can change the headline — the ceiling is established three ways —
and both only narrow confidence intervals and strengthen worked examples.**

---

## 1. Why validation power, not references

The downsampling control settled the reference question: country attribution does
not lift off baseline under any panel balance, and region survives a 90×
rebalancing (κ 0.89 → 0.81). So more references buy nothing. **The limiting axis
is the validation set** — the held-out cases with independently known origin that
the method is scored against. It is small (n = 43 scorable) and thin exactly
where the paper's claims are sharpest.

## 2. What we have, by stratum

**By region** (n = 43):

| region | n | note |
|---|---|---|
| East Asia & Pacific | 20 | Thailand, Australia, Viet Nam, Philippines |
| Latin America & Caribbean | 15 | the interesting failures — Mexico, Aruba, Guatemala… |
| South Asia | 6 | India (incl. the aromatherapy 5) |
| Sub-Saharan Africa | **2** | Nigeria, Ghana — the "snap to Ecuador, scored wrong" cases |
| North America / Europe / MENA | **0** | no imported-case validation at all |

**By country-scale distance stratum:**

| stratum | n | current result |
|---|---|---|
| d < 0.05 (a close relative exists) | **13→14** | **1/13 → 2/14** post-Track-0 — still the strongest anti-country result |
| 0.05 ≤ d < 0.30 | 8 | 2/8 |
| d ≥ 0.30 (no relative) | 22 | 6/22, all attractor hits |

The two most load-bearing strata for the paper — "country fails *even with* a
close relative" (1/13) and "the region far-distance successes are attractor
artifacts" (the 2 African genomes are the clean counter-examples) — rest on
**n = 13** and **n = 2** respectively. That is what acquisition can strengthen.

## 3. What counts as validation power, and what does not

Only tiers **A** (`ENA "X ex Y"`) and **B** (`external evidence +
EXPOSURE_OVERRIDES`) are ground truth (`classify_ena_origin_bp.py`). Two traps:

- **Endemic-country `as_isolated` genomes are references, not validation.** An
  Australian genome collected in Australia is trivially "correct" by co-location
  and tests nothing about prediction. This is why the obtainable ~1,300
  Australian public genomes are worthless for validation despite topping the
  Phase-1 volume list.
- **Tier-C deposit-only genomes are not validation** unless an investigation
  attaches an exposure country — which is exactly what Track 0 does.

## 4. Two tracks

### Track 0 — metadata mining (free, do first)

**Turn panel genomes we already hold into validation genomes by attaching
published exposure evidence.** Zero sequencing. Every hit is `+1` to
`EXPOSURE_OVERRIDES.tsv` (currently **11 rows**) and `+1` validation genome.

The model is already recorded: `GCF_021083435_1_USA_Texas` (2021) sits in a
37-Thailand unit; if CDC holds travel history for it, that is a free tier-B
validation genome, and one in the d < 0.05 stratum (it has a close Thai relative)
— the most valuable kind. The panel holds ~52 USA genomes and a handful of
European ones; the deposit-only, non-endemic-country subset is the candidate pool.

**Method:** for each tier-C panel genome from a non-endemic country (US, Europe,
Gulf states — places where a *B. pseudomallei* case is almost always imported),
search the BioProject's publications and CDC/ProMED records for a stated
exposure. Register hits in `EXPOSURE_OVERRIDES.tsv` with the citation.

**Yield:** unknown until run, but the ceiling is the ~52 US + European panel
genomes, and non-endemic diagnosis makes many of them investigated cases.
Plausibly 5–15 conversions. **Cost: literature time only.**

### Track 1 — targeted sequencing (cheap, gated)

Acquire travel-attributed cases **not already in the panel**, via Terra (the
local fetcher is abandoned). Prioritise by **boundary novelty**, not volume:

1. **Americas and African imported cases** — the validation-thin regions that are
   also where the failure/attractor story lives. Highest value.
2. **Close-relative (d < 0.05) cases in any region** — they enlarge the 1/13
   stratum, the paper's strongest claim. Hard to target deliberately (you cannot
   know d before sequencing), but Caribbean/Latin-American imports into the US
   are the best bet given the ST92 pan-Americas lineage.
3. **Not: more Asia imports.** India/Thailand/Australia are already the bulk of
   the set (n = 12 of 13 in the last batch) and test region we already resolve.

**First action is a census, not a download:** an ENA `"* ex *"` query **unioning
`read_run` with `result=assembly`** (the read-run-only census undercounts — it
produced the Mexico "0 genomes" error), minus what is already in the panel,
classified through `classify_ena_origin_bp.py`.

**Cost model, from the batch already done:** 40 Terra runs yielded 13 tier-A/B
validation genomes (a 33% ground-truth rate; the rest were deposit-only
references). So ~20 new validation genomes ≈ ~60 runs assembled — a few hundred
dollars of Terra compute, against Phase 1's ~2,000-genome assembly bill for zero
validation gain.

## 5. The honest ceiling

**Acquisition cannot change the headline.** The divergence-depth ceiling is
established by the Mexico controlled negative, the resolution curve, and now the
downsampling control. Doubling the validation set will not make country work; it
will show country failing on n ≈ 85 instead of 43, more tightly.

What it *does* buy, concretely:

- **Tighter CIs on the two thin, load-bearing strata** (1/13 country-with-relative;
  the 2 African attractor counter-examples).
- **A stronger CDC aromatherapy worked example** if more cases from that or
  similar published outbreaks are added (§3.5 of the attribution findings).
- **Nothing for the Philippines** — 12 held-out genomes, zero obtainable
  references anywhere on earth. No acquisition of any kind helps them; that
  absence is itself the surveillance-gap finding and should be reported as a
  result, not a gap to be closed.

## 6. Decision gate

- **Track 0 is free and strictly positive.** Recommend running it regardless: it
  grows the validation set at zero cost and only improves every stratum.
- **Track 1 is worth its few-hundred-dollar cost only if** the reviewer response
  or the paper's framing needs a thicker n in the Americas/Africa strata. If the
  current n = 43 with its stratification is judged sufficient — and it may be,
  given kappa and the three independent ceiling controls — Track 1 can be
  declined without weakening the result.

**Recommendation: run Track 0; hold Track 1 pending the Methods/response draft,
which is where it becomes clear whether any stratum reads as too thin to defend.**

Per-isolate target lists, when Track 1 is scoped, go in a gitignored file (isolate
data), not here.
