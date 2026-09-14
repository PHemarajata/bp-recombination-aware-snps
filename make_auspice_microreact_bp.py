#!/usr/bin/env python3
"""
Export the global tree and its metadata for Microreact and Auspice.

Writes three Newick files and one metadata TSV into AUSPICE_MICROREACT/.

WHY THREE TREES. The grafted tree splices two branch-length scales that differ by
roughly 133-fold: backbone edges are substitutions per site over the parsnp core,
within-unit edges are substitutions per site over that unit's
recombination-filtered variable sites. Every figure in this project draws it as a
cladogram for that reason. An external viewer will happily draw the raw lengths
and imply the distances are comparable, so the safe files come first and the raw
one is named to make its own warning.

  global_tree_2340_cladogram.nwk    topology only, no branch lengths.
                                    Recommended for Microreact.
  global_tree_2340_steps.nwk        every branch length 1, so depth is the number
                                    of nodes from the root. Readable in Auspice,
                                    and it is NOT divergence.
  global_tree_2340_RAW_SPLICED_LENGTHS_DO_NOT_INTERPRET.nwk
                                    the original lengths, for completeness only.

The metadata TSV loads in both tools. r/m is split across two columns so that
neither can be colored in a way that mixes a measurement with a detection
failure.

  python3 make_auspice_microreact_bp.py
"""

import csv
import json
import os
import re
import sys

B = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, B)
from make_itol_bp import parse_newick, tips_of, prune, to_newick  # noqa: E402

TREE = f"{B}/L1v4c_out/global_grafted_chr1.treefile"
PART = f"{B}/FINAL_BASIS_2026-08-22/FINAL_PARTITION.tsv"
META = f"{B}/L1v4c_MERGED_METADATA.tsv"
GATE = f"{B}/GATE1_ALIGNMENT_2026-08-21.tsv"
REGION = f"{B}/assign_region.tsv"
VMJSON = f"{B}/VM_HANDOFF_PACK/extracts/virtual_manuscript_data.json"
NUMBERS = f"{B}/NUMBERS.tsv"
OUT = f"{B}/AUSPICE_MICROREACT"

OKABE = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9", "#D55E00",
         "#B8A22E", "#8C564B", "#7570B3", "#1B9E77", "#A6761D", "#6E7B8B"]
GATECOL = {"in": "#0072B2", "below": "#D55E00", "above": "#7570B3"}
GATENAME = {"in": "In the working range",
            "below": "Below the floor",
            "above": "Above the ceiling"}

# Country display positions. The first block is lifted verbatim from MAPC in
# virtual_manuscript_data.json, which derive_vm_data.py validates against the
# frozen basis, so the published map and this export cannot disagree. The second
# block is plain country centroids added here for the 21 labels MAPC does not
# carry, together 33 genomes. THESE ARE COUNTRY CENTROIDS FOR DISPLAY. They are
# not isolate collection locations, and no isolate in this collection has a
# recorded coordinate.
EXTRA_COORDS = {
    "United Kingdom": (-2.0, 54.0),
    "Pakistan": (69.5, 30.0),
    "Myanmar": (96.0, 21.0),
    "Japan": (138.0, 36.5),
    "South Korea": (127.8, 36.5),
    "Portugal": (-8.2, 39.5),
    "Israel": (35.0, 31.5),
    "Taiwan": (121.0, 23.8),
    "New Zealand": (172.5, -41.0),
    "Vietnam": (106.0, 16.0),
    "Hong Kong": (114.2, 22.3),
    "Russia": (95.0, 60.0),
    "Czech Republic": (15.5, 49.8),
    "Trinidad and Tobago": (-61.2, 10.5),
    "Virgin Islands": (-64.8, 18.3),
    "Guadeloupe": (-61.6, 16.2),
    "Martinique": (-61.0, 14.6),
    "Costa Rica": (-84.1, 9.9),
    "Nicaragua": (-85.2, 12.9),
}
# Deliberately absent: "unknown", and "Panama and Peru", which is a two-country
# exposure string rather than a country and must not be given one position.


def strain_of(u):
    m = re.match(r"(strain_\d+)", u)
    return m.group(1) if m else u


def strip_lengths(n):
    n.length = None
    for c in n.children:
        strip_lengths(c)


def unit_lengths(n, root=True):
    n.length = None if root else 1.0
    for c in n.children:
        unit_lengths(c, root=False)


def main():
    for p in (TREE, PART, META, GATE, REGION, VMJSON, NUMBERS):
        if not os.path.isfile(p):
            sys.exit(f"FATAL: {p} not found.")
    os.makedirs(OUT, exist_ok=True)

    numbers = {r["key"]: r["value"]
               for r in csv.DictReader(open(NUMBERS), delimiter="\t")}
    exp_g = int(numbers["genomes.analysed"])
    exp_u = int(numbers["units.analysed"])

    g2u = {r["sample_id"]: r["unit"]
           for r in csv.DictReader(open(PART), delimiter="\t")}
    meta = {r["sample_id"]: r
            for r in csv.DictReader(open(META), delimiter="\t")}
    # assign_region.tsv's column named "country" holds WORLD REGION values. That
    # mislabeling is a documented trap. Real country is column 9 of the merged
    # metadata, read above.
    region = {r["sample_id"]: (r.get("country") or "")
              for r in csv.DictReader(open(REGION), delimiter="\t")}
    gate = {r["unit"]: r
            for r in csv.DictReader(open(GATE), delimiter="\t")}
    if len(gate) != exp_u:
        sys.exit(f"FATAL: Gate 1 table has {len(gate)} units, expected {exp_u}.")

    coords = {}
    for c, _n, lon, lat, _r in json.load(open(VMJSON))["MAPC"]:
        coords[c] = (lon, lat)
    n_from_map = len(coords)
    for c, ll in EXTRA_COORDS.items():
        if c in coords:
            sys.exit(f"FATAL: {c} is in MAPC already, remove it from EXTRA_COORDS.")
        coords[c] = ll

    # ---- trees ----------------------------------------------------------------
    root = parse_newick(open(TREE).read())
    all_tips = tips_of(root)
    keep = {t for t in all_tips if t in g2u}
    if len(keep) != exp_g:
        sys.exit(f"FATAL: {len(keep)} tips kept, NUMBERS.tsv says {exp_g}.")
    root = prune(root, keep)
    order = [t for t in tips_of(root) if t]
    if len(order) != exp_g:
        sys.exit("FATAL: prune did not leave the expected tip set.")
    if len(set(order)) != exp_g:
        sys.exit("FATAL: duplicate tip labels after pruning.")

    raw = to_newick(root) + ";"
    unit_lengths(root)
    steps = to_newick(root) + ";"
    strip_lengths(root)
    clado = to_newick(root) + ";"

    files = {
        "global_tree_2340_cladogram.nwk": clado,
        "global_tree_2340_steps.nwk": steps,
        "global_tree_2340_RAW_SPLICED_LENGTHS_DO_NOT_INTERPRET.nwk": raw,
    }
    for name, text in files.items():
        with open(f"{OUT}/{name}", "w") as fh:
            fh.write(text + "\n")

    # ---- metadata -------------------------------------------------------------
    strains = sorted({strain_of(u) for u in gate},
                     key=lambda s: int(s.split("_")[1]))
    scol = {s: OKABE[i % len(OKABE)] for i, s in enumerate(strains)}
    regs = sorted({region.get(t, "") or "unknown" for t in order})
    rcol = {r: OKABE[i % len(OKABE)] for i, r in enumerate(regs)}

    cols = ["id", "unit", "poppunk_strain", "gate1_class", "unit_n",
            "unit_diversity_mean_pairwise_core_snps",
            "rm_measured", "rm_reported_but_not_interpretable",
            "country", "region", "bioproject", "collection_date",
            "latitude", "longitude",
            "gate1_class__colour", "poppunk_strain__colour", "region__colour"]
    # The minimal variant drops bioproject and collection date, leaving accession
    # joined only to country. ENA already publishes that pair. Use it whenever the
    # destination is a service that stores what you upload.
    DROP = {"bioproject", "collection_date"}
    keep = [i for i, c in enumerate(cols) if c not in DROP]

    n_coord, n_in = 0, 0
    fh_min = open(f"{OUT}/global_tree_2340_metadata_minimal.tsv", "w", newline="")
    w_min = csv.writer(fh_min, delimiter="\t", lineterminator="\n")
    w_min.writerow([cols[i] for i in keep])
    with open(f"{OUT}/global_tree_2340_metadata.tsv", "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(cols)
        for t in order:
            u = g2u[t]
            g = gate[u]
            m = meta.get(t, {})
            cls = g["gate1_alignment"]
            country = (m.get("country") or "").strip()
            rg = region.get(t, "") or "unknown"
            lon, lat = coords.get(country, ("", ""))
            if lat != "":
                n_coord += 1
            if cls == "in":
                n_in += 1
            row = [
                t, u, strain_of(u), GATENAME[cls], g["n"],
                g["aln_mean_pairwise_snps"],
                g["rm_corrected"] if cls == "in" else "",
                g["rm_corrected"] if cls != "in" else "",
                country or "unknown", rg,
                m.get("bioproject") or "", m.get("collection_date") or "",
                lat, lon,
                GATECOL[cls], scol[strain_of(u)], rcol[rg],
            ]
            if len(row) != len(cols):
                sys.exit("FATAL: row width does not match the header.")
            w.writerow(row)
            w_min.writerow([row[i] for i in keep])

    fh_min.close()
    readme(n_from_map, len(EXTRA_COORDS), n_coord, exp_g, exp_u, n_in)
    print(f"wrote {OUT}/")
    for name in files:
        print(f"  {name}  {os.path.getsize(OUT + '/' + name)/1024:.0f} KB")
    print(f"  global_tree_2340_metadata.tsv          {exp_g} rows, "
          f"{len(cols)} columns")
    print(f"  global_tree_2340_metadata_minimal.tsv  {exp_g} rows, "
          f"{len(keep)} columns, no bioproject and no collection date")
    print(f"  {n_coord} of {exp_g} genomes carry a display coordinate")
    print(f"  {n_in} genomes in units inside the working range")


def readme(n_map, n_extra, n_coord, exp_g, exp_u, n_in):
    txt = f"""# Global tree for Microreact and Auspice

Generated by `make_auspice_microreact_bp.py` from the frozen basis
(`FINAL_BASIS_2026-08-22`). {exp_g} genomes, {exp_u} analysis units, 28 PopPUNK
strains, on the grafted chromosome 1 tree.

## Read this before you load anything

**Branch lengths in the source tree are not comparable.** The grafted tree
splices two scales that differ by roughly 133-fold. Backbone edges are
substitutions per site over the parsnp core. Within-unit edges are substitutions
per site over that unit's recombination-filtered variable sites. Every figure in
this project draws the tree as a cladogram for that reason, and an external
viewer will draw the raw lengths without asking.

**No rate and no date may be taken from this tree.** It is not
recombination-corrected. No dates were estimated anywhere in this work.

**r/m is a measurement only inside the working range.** Outside it, a low value
is a detection failure rather than a low recombination rate. That is why the
metadata splits r/m across two columns that cannot be colored together.

## Files

| file | what it is | use it for |
|---|---|---|
| `global_tree_2340_cladogram.nwk` | topology only, no branch lengths | Microreact |
| `global_tree_2340_steps.nwk` | every branch length 1, so depth is nodes from the root | Auspice, where a length is required. This is NOT divergence |
| `global_tree_2340_RAW_SPLICED_LENGTHS_DO_NOT_INTERPRET.nwk` | the original spliced lengths | completeness only |
| `global_tree_2340_metadata.tsv` | {exp_g} rows, one per tip | both tools, on a machine you control |
| `global_tree_2340_metadata_minimal.tsv` | the same minus bioproject and collection date | anything that uploads to a server |

## Microreact

1. Go to microreact.org and choose Upload.
2. Add `global_tree_2340_cladogram.nwk` as the tree.
3. Add `global_tree_2340_metadata.tsv` as the data file.
4. The `id` column matches the tree tip labels exactly.

The three `__colour` columns are Microreact's convention and set the palette for
`gate1_class`, `poppunk_strain` and `region` without any manual picking. The map
is driven by `latitude` and `longitude`.

## Auspice

Drag `global_tree_2340_steps.nwk` onto auspice.us, then drag
`global_tree_2340_metadata.tsv` onto the rendered tree. Auspice reads the first
column as the node name.

Set the layout to rectangular and leave the x-axis on divergence, remembering
that divergence here counts nodes rather than substitutions. Do not switch to a
time axis. There are no dates.

## Columns

| column | note |
|---|---|
| `id` | tip label, matches the Newick exactly |
| `unit` | analysis unit, {exp_u} of them |
| `poppunk_strain` | the strain the unit sits in, 28 of them |
| `gate1_class` | In the working range, Below the floor, Above the ceiling |
| `unit_n` | genomes in that unit |
| `unit_diversity_mean_pairwise_core_snps` | alignment-derived, the basis of the window [700, 4700]. Never the Mash proxy |
| `rm_measured` | populated only for units inside the window, {n_in} genomes |
| `rm_reported_but_not_interpretable` | populated only for units outside it |
| `country` | column 9 of the merged metadata |
| `region` | World Bank region |
| `bioproject`, `collection_date` | as deposited, and both are incomplete |
| `latitude`, `longitude` | COUNTRY CENTROIDS FOR DISPLAY, not collection sites |

## Which metadata file to use

`B. pseudomallei` is a US Tier 1 Select Agent, and the study metadata joins
accession to isolation location, collection date and exposure label. That
combination is re-identifiable for rare cases, which is why the repository has
never tracked isolate-level data.

**Neither file here carries an exposure label or an isolation location.** The
full file does carry accession joined to country, BioProject and collection date.
The minimal file drops the last two, leaving accession joined to country, a pair
ENA already publishes.

Auspice renders a dropped file in your own browser. Microreact uploads what you
give it to their server, so use the minimal file there unless you have decided
otherwise, and set the project to private.

## Coordinates

No isolate in this collection carries a recorded coordinate. The positions here
are country centroids, for display only. {n_map} of them come from the published
sampling map's own table, which `derive_vm_data.py` validates against the frozen
basis, so the map figure and this export cannot disagree. {n_extra} more were
added for smaller countries. {n_coord} of {exp_g} genomes carry a position, and
the rest are genomes whose country is unknown or is recorded as a two-country
exposure string.

## One metadata inconsistency to know about

The country column carries both `Viet Nam` and `Vietnam` as separate values. They
are the same country and they are not merged here, because the merged metadata is
a frozen input and silently normalizing it would put this export out of step with
every other table in the project. Group them yourself if you color by country.

## Sampling, which limits what any map can show

Thailand is 1,561 of {exp_g}, 66.7 percent. China adds 265. Two countries are
three quarters of everything analyzed. South Asia carries about 44 percent of
modelled global melioidosis burden and 2.5 percent of this panel. A map of this
collection is a map of where sequencing happened.
"""
    with open(f"{OUT}/README.md", "w") as fh:
        fh.write(txt)


if __name__ == "__main__":
    main()
