#!/usr/bin/env python3
"""Generate iTOL annotation files for the grafted all-sample tree.

Produces four drag-and-drop files:

  itol_collapse.txt        collapse all 86 unit clades -> every visible edge is a
                           BACKBONE edge, so the displayed tree is on one scale
  itol_unit_labels.txt     label each collapsed clade "unit (n, dominant country)"
  itol_unit_ranges.txt     shade each unit clade by its dominant country
  itol_country_strip.txt   per-leaf country colour, for when a unit is expanded

Why collapsing matters: the grafted tree mixes two branch-length scales. Backbone
edges are substitutions/site over the parsnp core (median 0.033); within-unit
edges are substitutions/site over that unit's recombination-filtered variable
sites (median 0.00025) -- a 133x difference. Collapsing removes the within-unit
edges from the layout, so what remains is internally comparable.

USA is split into mainland and territories: 10 of the 47 USA genomes here are
Puerto Rico or the US Virgin Islands, and collapsing them into "USA" hides that.
"""
import csv, collections, sys
from Bio import Phylo

TREE   = "L1v4c_out/global_grafted_chr1.treefile"
CLUST  = "curated_L1v4c_clusters.tsv"
META   = "L1v4c_MERGED_METADATA.tsv"

TERRITORIES = {"Puerto Rico", "Virgin Islands", "Guam", "American Samoa",
               "Northern Mariana Islands"}

# Okabe-Ito derived; distinguishable in common colour-vision deficiencies.
PALETTE = {
    "Thailand":          "#0072B2",
    "China":             "#D55E00",
    "Australia":         "#009E73",
    "Singapore":         "#CC79A7",
    "Malaysia":          "#E69F00",
    "USA (mainland)":    "#B22222",
    "USA (territories)": "#F0A3A3",
    "Laos":              "#56B4E9",
    "Viet Nam":          "#8C6BB1",
    "Brazil":            "#7F3B08",
    "Cambodia":          "#4D9221",
    "Micronesia":        "#00CED1",
    "Philippines":       "#FFD700",
    "India":             "#A6761D",
    "other/unknown":     "#BBBBBB",
}
OTHER = "other/unknown"


def country_of(sample, meta):
    c, sub = meta.get(sample, ("", ""))
    c = (c or "").strip()
    if c == "USA":
        return "USA (territories)" if sub.strip() in TERRITORIES else "USA (mainland)"
    return c if c in PALETTE else (OTHER if c else OTHER)


def main():
    meta = {r["sample_id"]: ((r.get("country") or ""), (r.get("subregion") or ""))
            for r in csv.DictReader(open(META), delimiter="\t")}
    units = collections.defaultdict(list)
    for i, l in enumerate(open(CLUST)):
        if i == 0:
            continue
        f = l.rstrip("\r\n").split("\t")
        if len(f) >= 2:
            units[f[0]].append(f[1])

    tree = Phylo.read(TREE, "newick")
    leaves = {t.name for t in tree.get_terminals()}

    collapse, labels, ranges = [], [], []
    non_mono, missing = [], []

    for unit, members in sorted(units.items()):
        present = [m for m in members if m in leaves]
        if len(present) < len(members):
            missing.append((unit, len(members) - len(present)))
        if len(present) < 2:
            continue
        mrca = tree.common_ancestor(present)
        got = {t.name for t in mrca.get_terminals()}
        if got != set(present):
            # Monophyly is required: collapsing a non-monophyletic clade would
            # silently swallow genomes from other units into the triangle.
            non_mono.append((unit, len(got - set(present))))
            continue
        span = mrca.get_terminals()
        node = f"{span[0].name}|{span[-1].name}"

        cs = collections.Counter(country_of(m, meta) for m in present)
        top, n_top = cs.most_common(1)[0]
        pct = round(100 * n_top / len(present))
        colour = PALETTE.get(top, PALETTE[OTHER])

        collapse.append(node)
        labels.append(f"{node}\t{unit} (n={len(present)}, {top} {pct}%)")
        ranges.append(f"{node}\trange\t{colour}\t{unit}")

    with open("itol_collapse.txt", "w") as fh:
        fh.write("COLLAPSE\nDATA\n" + "\n".join(collapse) + "\n")
    with open("itol_unit_labels.txt", "w") as fh:
        fh.write("LABELS\nSEPARATOR TAB\nDATA\n" + "\n".join(labels) + "\n")
    with open("itol_unit_ranges.txt", "w") as fh:
        fh.write("TREE_COLORS\nSEPARATOR TAB\nDATA\n" + "\n".join(ranges) + "\n")

    used = [c for c in PALETTE if any(country_of(m, meta) == c
                                      for ms in units.values() for m in ms)]
    with open("itol_country_strip.txt", "w") as fh:
        fh.write("DATASET_COLORSTRIP\nSEPARATOR TAB\n")
        fh.write("DATASET_LABEL\tCountry\nCOLOR\t#0072B2\n")
        fh.write("STRIP_WIDTH\t28\nMARGIN\t4\nBORDER_WIDTH\t0\n")
        fh.write("LEGEND_TITLE\tCountry\n")
        fh.write("LEGEND_SHAPES\t" + "\t".join("1" for _ in used) + "\n")
        fh.write("LEGEND_COLORS\t" + "\t".join(PALETTE[c] for c in used) + "\n")
        fh.write("LEGEND_LABELS\t" + "\t".join(used) + "\n")
        fh.write("DATA\n")
        for ms in units.values():
            for m in ms:
                if m in leaves:
                    c = country_of(m, meta)
                    fh.write(f"{m}\t{PALETTE[c]}\t{c}\n")

    print(f"  units collapsed        : {len(collapse)} / {len(units)}")
    print(f"  leaves annotated       : {sum(1 for ms in units.values() for m in ms if m in leaves)}")
    print(f"  countries in legend    : {len(used)}")
    if non_mono:
        print(f"  !! NOT monophyletic, not collapsed: {len(non_mono)}")
        for u, extra in non_mono[:5]:
            print(f"       {u} (+{extra} foreign leaves)")
    else:
        print("  every unit is monophyletic in the grafted tree")
    if missing:
        print(f"  !! members absent from tree: {missing[:5]}")


if __name__ == "__main__":
    main()
