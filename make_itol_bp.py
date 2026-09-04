#!/usr/bin/env python3
"""
make_itol_bp.py -- iTOL components for the global maximum-likelihood tree.

Figure 3 is a static rendering of the global tree over unit medoids. This emits
the same tree and the same annotations as iTOL upload files, so the figure can be
explored, re-styled and re-exported without re-running a plotting script, and so
a reviewer can be handed the tree rather than a picture of it.

WHAT IT WRITES, into itol/ :

  global_ml_tree_frozen85.nwk   the tree, PRUNED to the frozen basis
  itol_labels.txt               LABELS            readable tip labels
  itol_gate1_class.txt          DATASET_COLORSTRIP  Gate 1 class
  itol_country.txt              DATASET_COLORSTRIP  dominant country
  itol_rm.txt                   DATASET_SIMPLEBAR   r/m per unit
  itol_diversity.txt            DATASET_SIMPLEBAR   mean pairwise core SNPs
  itol_unit_size.txt            DATASET_SIMPLEBAR   genomes per unit
  README.md                     how to load them, and what not to claim

THE PRUNING IS THE POINT, and it is why this is a script rather than a manual
export. `global_ml_tree.treefile` carries 86 tips; the frozen reported basis is
85 units. Uploading the raw treefile would put a unit in the figure that is not
in the analysis, which is exactly the class of error this repository keeps
finding. This refuses to write anything if the pruned tip count disagrees with
`units.analysed` in NUMBERS.tsv.

THE TREE IS UNROOTED and is NOT recombination-corrected. Its branch lengths
include recombination and no r/m may be derived from it. The README says so, and
so must any figure legend built from these files.

Stdlib only.
"""

import collections
import csv
import os
import re
import sys

B = os.path.dirname(os.path.abspath(__file__))
TREE = f"{B}/L1v4c_out/global_ml_tree.treefile"
PANEL = f"{B}/FINAL_BASIS_2026-08-22/FINAL_PANEL.tsv"
GATE1 = f"{B}/GATE1_ALIGNMENT_2026-08-21.tsv"
NUMBERS = f"{B}/NUMBERS.tsv"
OUTDIR = f"{B}/itol"

# Colour-blind safe, and deliberately the same roles as Figure 3: in-window is
# the one the paper reports, so it gets the strong colour.
GATE_COLOR = {"in": "#1b9e77", "below": "#d95f02", "above": "#7570b3"}
GATE_LABEL = {"in": "in-window", "below": "below floor", "above": "above ceiling"}
COUNTRY_PALETTE = ["#4477aa", "#ee6677", "#228833", "#ccbb44", "#66ccee",
                   "#aa3377", "#bbbbbb", "#ee8866", "#77aadd", "#44bb99"]
OTHER_COLOR = "#dddddd"


# ---------------------------------------------------------------- newick ----
class Node:
    __slots__ = ("name", "length", "children")

    def __init__(self):
        self.name, self.length, self.children = "", None, []


def parse_newick(s):
    """Minimal Newick reader. Enough for an IQ-TREE treefile with supports."""
    s = s.strip()
    i = 0

    def node():
        nonlocal i
        n = Node()
        if s[i] == "(":
            i += 1
            while True:
                n.children.append(node())
                if s[i] == ",":
                    i += 1
                    continue
                if s[i] == ")":
                    i += 1
                    break
                raise ValueError(f"bad newick at {i}: {s[i:i+30]!r}")
        m = re.match(r"[^,\)\(:;]*", s[i:])
        n.name = m.group(0).strip().strip("'\"")
        i += len(m.group(0))
        if i < len(s) and s[i] == ":":
            i += 1
            m = re.match(r"-?[\d.eE+-]+", s[i:])
            n.length = float(m.group(0))
            i += len(m.group(0))
        return n

    root = node()
    return root


def tips_of(n):
    if not n.children:
        return [n.name] if n.name else []
    out = []
    for c in n.children:
        out += tips_of(c)
    return out


def prune(n, keep):
    """
    Return a copy containing only tips in `keep`, or None if nothing survives.

    Unary nodes left behind are collapsed and their branch lengths added, so
    distances between surviving tips are unchanged. Getting that wrong would
    silently redraw the tree.
    """
    if not n.children:
        return n if n.name in keep else None
    kids = [k for k in (prune(c, keep) for c in n.children) if k is not None]
    if not kids:
        return None
    if len(kids) == 1:
        only = kids[0]
        if n.length is not None:
            only.length = (only.length or 0.0) + n.length
        return only
    out = Node()
    out.name, out.length, out.children = n.name, n.length, kids
    return out


def to_newick(n):
    if n.children:
        inner = ",".join(to_newick(c) for c in n.children)
        s = f"({inner}){n.name}"
    else:
        s = n.name
    if n.length is not None:
        s += f":{n.length:.10g}"
    return s


# ------------------------------------------------------------------ main ----
def header(kind, label, color, extra=()):
    out = [kind, "SEPARATOR TAB", f"DATASET_LABEL\t{label}", f"COLOR\t{color}"]
    out += list(extra)
    out.append("DATA")
    return out


def main():
    for p in (TREE, PANEL, GATE1, NUMBERS):
        if not os.path.isfile(p):
            sys.exit(f"FATAL: {p} not found.")

    numbers = {r["key"]: r["value"]
               for r in csv.DictReader(open(NUMBERS), delimiter="\t")}
    if "units.analysed" not in numbers:
        sys.exit("FATAL: NUMBERS.tsv has no units.analysed key.")
    expected = int(numbers["units.analysed"])

    members = collections.defaultdict(list)
    for r in csv.DictReader(open(PANEL), delimiter="\t"):
        if r.get("basis_role") == "analysis" and r.get("unit_membership"):
            members[r["unit_membership"]].append((r.get("country") or "").strip())
    basis = set(members)

    dominant, share = {}, {}
    for u, cs in members.items():
        known = [c for c in cs if c and c.lower() not in ("na", "unknown")]
        if known:
            c, k = collections.Counter(known).most_common(1)[0]
            dominant[u], share[u] = c, k / len(known)
        else:
            dominant[u], share[u] = "unknown", 0.0

    g = {r["unit"]: r for r in csv.DictReader(open(GATE1), delimiter="\t")}

    root = parse_newick(open(TREE).read())
    all_tips = [t for t in tips_of(root) if t]
    keep = {t for t in all_tips if t in basis}
    dropped = sorted(t for t in all_tips if t not in basis)

    print(f"tree tips {len(all_tips)}   frozen basis {len(basis)}   keeping {len(keep)}")
    if dropped:
        print(f"  pruning {len(dropped)} tip(s) not in the frozen basis: "
              f"{', '.join(dropped)}")
    if len(keep) != expected:
        sys.exit(f"FATAL: {len(keep)} tips after pruning but NUMBERS.tsv says "
                 f"units.analysed = {expected}. Refusing to write a tree that is "
                 f"not the reported basis.")

    pruned = prune(root, keep)
    os.makedirs(OUTDIR, exist_ok=True)

    nwk = f"{OUTDIR}/global_ml_tree_frozen85.nwk"
    with open(nwk, "w") as fh:
        fh.write(to_newick(pruned) + ";\n")

    # LABELS
    with open(f"{OUTDIR}/itol_labels.txt", "w") as fh:
        fh.write("LABELS\nSEPARATOR TAB\nDATA\n")
        for t in sorted(keep):
            fh.write(f"{t}\t{t} | {dominant[t]} ({share[t]*100:.0f}%)\n")

    # Gate 1 colorstrip
    order = ["in", "below", "above"]
    with open(f"{OUTDIR}/itol_gate1_class.txt", "w") as fh:
        fh.write("\n".join(header(
            "DATASET_COLORSTRIP", "Gate 1 class", "#1b9e77",
            ["STRIP_WIDTH\t40", "MARGIN\t4", "BORDER_WIDTH\t0.5",
             "LEGEND_TITLE\tGate 1 class",
             "LEGEND_SHAPES\t" + "\t".join("1" for _ in order),
             "LEGEND_COLORS\t" + "\t".join(GATE_COLOR[k] for k in order),
             "LEGEND_LABELS\t" + "\t".join(GATE_LABEL[k] for k in order)])) + "\n")
        for t in sorted(keep):
            cls = g.get(t, {}).get("gate1_alignment", "")
            if cls in GATE_COLOR:
                fh.write(f"{t}\t{GATE_COLOR[cls]}\t{GATE_LABEL[cls]}\n")

    # Country colorstrip: top N by unit count, rest "other"
    counts = collections.Counter(dominant[t] for t in keep)
    top = [c for c, _ in counts.most_common(len(COUNTRY_PALETTE))]
    cmap = {c: COUNTRY_PALETTE[i] for i, c in enumerate(top)}
    legend = top + ["other"]
    with open(f"{OUTDIR}/itol_country.txt", "w") as fh:
        fh.write("\n".join(header(
            "DATASET_COLORSTRIP", "Dominant country", "#4477aa",
            ["STRIP_WIDTH\t40", "MARGIN\t4", "BORDER_WIDTH\t0.5",
             "LEGEND_TITLE\tDominant country (of known-country members)",
             "LEGEND_SHAPES\t" + "\t".join("1" for _ in legend),
             "LEGEND_COLORS\t" + "\t".join(
                 [cmap[c] for c in top] + [OTHER_COLOR]),
             "LEGEND_LABELS\t" + "\t".join(legend)])) + "\n")
        for t in sorted(keep):
            c = dominant[t]
            fh.write(f"{t}\t{cmap.get(c, OTHER_COLOR)}\t{c}\n")

    # Simple bars
    def bars(fname, label, color, field, cast, scale):
        with open(f"{OUTDIR}/{fname}", "w") as fh:
            fh.write("\n".join(header(
                "DATASET_SIMPLEBAR", label, color,
                ["WIDTH\t220", "MARGIN\t8", f"DATASET_SCALE\t{scale}"])) + "\n")
            for t in sorted(keep):
                v = g.get(t, {}).get(field, "")
                if v not in ("", "NA"):
                    fh.write(f"{t}\t{cast(v)}\n")

    bars("itol_rm.txt", "r/m (Gubbins, corrected)", "#4575b4",
         "rm_corrected", lambda v: f"{float(v):.4f}", "2,5,10,15")
    bars("itol_diversity.txt", "mean pairwise core SNPs (alignment)", "#b2182b",
         "aln_mean_pairwise_snps", lambda v: f"{float(v):.1f}",
         "700,2000,4700,8000")
    bars("itol_unit_size.txt", "genomes in unit", "#5aae61",
         "n", lambda v: str(int(float(v))), "25,50,100,150")

    readme(nwk, len(keep), dropped, counts, top)

    print(f"wrote {OUTDIR}/ :")
    for f in sorted(os.listdir(OUTDIR)):
        print(f"  {f}")
    print(f"\n  {len(keep)} tips, matching NUMBERS.tsv units.analysed = {expected}")
    ing = sum(1 for t in keep if g.get(t, {}).get("gate1_alignment") == "in")
    print(f"  {ing} in-window")


def readme(nwk, n, dropped, counts, top):
    with open(f"{OUTDIR}/README.md", "w") as fh:
        fh.write(f"""# iTOL components for the global ML tree

Generated by `make_itol_bp.py`. Do not edit by hand; regenerate.

## Load order

1. Upload **`{os.path.basename(nwk)}`** to iTOL (Upload → Tree file).
2. Drag the `itol_*.txt` files onto the tree, or use Datasets → Upload. Each is a
   standalone iTOL dataset and they can be toggled independently.

| file | dataset | shows |
|---|---|---|
| `itol_labels.txt` | LABELS | `unit \\| dominant country (share)` |
| `itol_gate1_class.txt` | COLORSTRIP | Gate 1 class, in-window / below floor / above ceiling |
| `itol_country.txt` | COLORSTRIP | dominant country of the unit's known-country members |
| `itol_rm.txt` | SIMPLEBAR | r/m per unit |
| `itol_diversity.txt` | SIMPLEBAR | mean pairwise core SNPs, alignment-derived |
| `itol_unit_size.txt` | SIMPLEBAR | genomes per unit |

## The basis

**{n} tips, one per analysis unit**, matching `units.analysed` in `NUMBERS.tsv`.
The source treefile carries {n + len(dropped)} tips; {len(dropped)} was pruned as
not being in the frozen basis{': ' + ', '.join(dropped) if dropped else ''}.
The generator refuses to write anything if the pruned count disagrees with
`NUMBERS.tsv`, because a tree carrying a unit that is not in the analysis is the
same class of error as a stale number in a table.

Pruning collapses the unary nodes it leaves behind and adds their branch lengths
to the surviving child, so distances between remaining tips are unchanged.

## What this tree does not support

**It is unrooted.** Any apparent basal position is an artifact of display. Do not
describe a unit as ancestral, early-diverging or a root from this tree.

**It is not recombination-corrected, and must not be.** Across {n} divergent
lineages there is no shared clonal background, so Gubbins would call most of the
alignment recombinant. Branch lengths therefore include recombination and **no
r/m may be derived from this tree**. The per-unit r/m in `itol_rm.txt` is
computed within units, not from this tree.

**Geography was never an input.** PopPUNK, fastbaps and IQ-TREE saw no country
label at any stage, which is what makes the recovery of known biogeography a
result rather than an assumption. That also means the country strip is an
annotation laid over the tree afterwards, not something the tree was fitted to.

**Dominant country is a summary and hides mixture.** It is the modal country
among members whose country is known, and the share is printed beside it in
`itol_labels.txt`. A unit at 55% is not a country's unit. Read the share.

## Composition

Units by dominant country, of {n}:

""")
        for c, k in counts.most_common():
            mark = "" if c in top else "  (grouped as 'other' in the strip)"
            fh.write(f"- {c}: {k}{mark}\n")


if __name__ == "__main__":
    main()
