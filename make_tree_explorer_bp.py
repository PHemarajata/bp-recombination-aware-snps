#!/usr/bin/env python3
"""
Assemble TREE_EXPLORER.html from the template and the generated data payload.

Single self-contained file, no external requests, so it opens offline on the same
terms as VIRTUAL_MANUSCRIPT.html. The data is inlined rather than fetched because
a file:// fetch is blocked by every browser's origin rules.

  python3 make_tree_explorer_data_bp.py     # first, writes the JSON
  python3 make_tree_explorer_bp.py          # then, writes the HTML

Refuses to write if the payload's counts disagree with NUMBERS.tsv, so the viewer
cannot drift away from the frozen basis the way a hand-edited file would.
"""

import csv
import json
import os
import sys

B = os.path.dirname(os.path.abspath(__file__))
TPL = f"{B}/tree_explorer_template.html"
DATA = f"{B}/TREE_EXPLORER_DATA.json"
NUMBERS = f"{B}/NUMBERS.tsv"
OUT = f"{B}/TREE_EXPLORER.html"
MARK = "/*__DATA__*/"


def main():
    for p in (TPL, DATA, NUMBERS):
        if not os.path.isfile(p):
            sys.exit(f"FATAL: {p} not found. Run make_tree_explorer_data_bp.py first.")

    numbers = {r["key"]: r["value"]
               for r in csv.DictReader(open(NUMBERS), delimiter="\t")}
    raw = open(DATA).read()
    d = json.loads(raw)

    checks = [
        ("n_tips", d["n_tips"], int(numbers["genomes.analysed"])),
        ("n_units", d["n_units"], int(numbers["units.analysed"])),
        ("tip_name", len(d["tip_name"]), int(numbers["genomes.analysed"])),
        ("unit_blocks", len(d["unit_blocks"]), int(numbers["units.analysed"])),
    ]
    for name, got, want in checks:
        if got != want:
            sys.exit(f"FATAL: {name} is {got}, NUMBERS.tsv says {want}.")

    shaded = sum(1 for b in d["strain_blocks"] if b["clade"])
    if (shaded, len(d["strain_blocks"])) != (29, 30):
        sys.exit(f"FATAL: strain blocks {shaded} of {len(d['strain_blocks'])}, "
                 "expected 29 of 30 as in make_figure6_bp.py.")

    # An empty check is worse than no check. Assert the payload is populated.
    for k in ("parent", "x", "y", "istip", "tip_idx", "tip_unit", "units"):
        if not d.get(k):
            sys.exit(f"FATAL: payload key {k} is empty.")

    tpl = open(TPL).read()
    if MARK not in tpl:
        sys.exit(f"FATAL: {TPL} has no {MARK} placeholder.")
    html = tpl.replace(MARK, raw)
    if MARK in html:
        sys.exit("FATAL: placeholder survived substitution.")

    with open(OUT, "w") as fh:
        fh.write(html)
    print(f"wrote {OUT}  {os.path.getsize(OUT)/1024:.0f} KB")
    print(f"  {d['n_tips']} genomes, {d['n_units']} units, "
          f"{shaded} of {len(d['strain_blocks'])} strain blocks are real clades")


if __name__ == "__main__":
    main()
