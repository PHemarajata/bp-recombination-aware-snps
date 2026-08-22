# Leave-outbreak-out

2026-08-23. Implements the leak control the Track 0 pass required
(`TRACK0_MINING_RESULT_2026-08-23.md` §3): a validation genome from an
outbreak/cluster with multiple deposited isolates leaks through leave-group-out,
because a near-identical same-source sibling in the reference pool wins
nearest-neighbour at ~0 distance and hands over the true label.

**Mechanism: an explicit same-source register (`OUTBREAK_GROUPS.tsv`), held out
as a unit. Not automatic — the automatic version was tried and is wrong.** No-op
on the current validation set; verified. The scorer change is in
`score_cgmlst_lichtenegger.py` and mirrored in `score_accessory_bp.py`
(`--validate` PASS).

---

## 1. Why not automatic — the Vietnam/Georgia counterexample

The obvious automatic rule is "hold out any pool genome that shares the query's
BioProject and is a near-clone." It is wrong, and the data says so.

Applied to the current set it "corrects" the two `USA: CA ex Vietnam` validation
genomes (`SRR31608433/435`) from country 0/2 to 2/2 — by holding out
`SRR31608437/438`, which sit ~0.01 away in the same BioProject. But those two are
**`USA: GA` clinical cases from 1983 and 2024** — *independent* cases of a lineage
that spans Vietnam and the United States, not co-deposits of one source. (The 1983
Georgia case is very plausibly a Vietnam-war veteran — melioidosis reactivating
decades after exposure, the classic "Vietnamese time bomb.")

Holding them out would **fake** a Viet Nam answer by hiding real references — the
opposite of what a leak control should do. The automatic rule cannot tell
"same source, co-deposited" (a leak) from "independent cases of a shared lineage"
(the paper's core finding). Only verified provenance can, so the register is
explicit.

## 2. The mechanism

`OUTBREAK_GROUPS.tsv` (gitignored — isolate data): `group_id, sample_id, basis`.
When scoring a validation genome that belongs to a group, every member of that
group is added to the leave-group-out hold-out set. An empty or absent register
is an exact no-op — confirmed by diffing the attribution result before and after
the code change (identical).

## 3. The one registered group: Mississippi Gulf Coast

`MS_gulf_coast_2020`, **21 isolates.** The Mississippi autochthonous source — one
Western Hemisphere strain, one investigation, confirmed by an environmental
source on the patient's property (Petras 2023 *NEJM* PMID 38118023).

The group was built by taking every panel isolate within d < 0.05 of the two
Mississippi clinical cases, then **verifying provenance**: all 21 are USA /
Mississippi by both `country` and `isolation_location` — none is an independent
Latin-American relative that the Western-Hemisphere strain merely resembles. The
first 5-isolate attempt leaked anyway (the cluster is deposited under both GCF
assembly and SRR run accessions); the distance-plus-provenance sweep caught all
21.

## 4. Demonstrated behaviour

Temporarily registering the two Mississippi clinical cases as validation genomes:

| genome | without leave-outbreak-out | with it |
|---|---|---|
| MS2020a / MS2022a — country | USA ✓ **(leak, NN a sibling at d≈0.005)** | **Colombia ✗** (NN a genuine Colombian genome at d≈0.15) |
| MS2020a / MS2022a — region | North America ✓ (leak) | **Latin America ✗** |
| Viet Nam `SRR31608433/435` | USA ✗ | **USA ✗ (unchanged)** |

The leak is removed, and the honest result is **informative and strengthens the
paper**: a US-origin autochthonous genome misattributes to Latin America because
the Mississippi strain is a Western Hemisphere lineage — country and region fail
even for a genome whose true origin is certain. Vietnam/Georgia is correctly left
alone.

## 5. State

- Code: `score_cgmlst_lichtenegger.py` + `score_accessory_bp.py`, both updated;
  `--validate` PASS; `freeze_basis` PASS; `generate_numbers` 40 keys; current
  attribution unchanged (9/43, 36/43) — no-op as intended.
- `OUTBREAK_GROUPS.tsv`: the Mississippi group, **staged**. It fires only when a
  Mississippi genome is a validation genome, which will happen at the batched
  Track 0 integration, not now.

## 6. Two follow-ups this surfaced

1. **The Vietnam/Georgia cases deserve a metadata look.** `SRR31608437` (Georgia
   1983) and `SRR31608438` (Georgia 2024) are the same strain as two Vietnam-
   exposure cases. If the Georgia cases are unrecorded Vietnam imports (the 1983
   one especially), they are mislabelled references; if they are genuinely US
   cases, they are a clean genomic example of the melioidosis-reactivation
   "Vietnamese time bomb" and a lineage that spans continents. Either way it is a
   result, not noise — but it is not for the automatic scorer to assume.
2. **The aromatherapy series** is already covered (all exposure=India, mutually
   held out; the one stray same-strain USA deposit was removed in the BioProject
   audit) but could be registered as a group for robustness when integrated.
