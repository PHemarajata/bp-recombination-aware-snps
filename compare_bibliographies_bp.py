#!/usr/bin/env python3
"""
Compare the two bibliographies in a document that carries both.

`BP_background_section.md` prints a reference list under `## References` and also
carries a machine-readable block of the same references earlier in the file. They
are not the same bibliography: they agree on `[1]`-`[40]` and disagree from `[41]`
on, because entries were inserted into one and not the other. The prose follows
the block, so the printed list names the wrong work for most of its entries.

`verify_references_bp.py` detects that condition and fails on it. This script is
the other half: it says, per number, what each side thinks the number means, so
the repair can be worked rather than merely known about.

Two outputs, because of a governance rule rather than a preference:

  --out    a TSV, which `.gitignore` excludes by design. Rule 5 of that file
           excludes `*.tsv` as belt and braces against isolate data being
           committed, and says in terms that a future loosening must not
           silently start tracking it. This table holds citation metadata and no
           accessions, but the right response to a rule like that is to write
           the generator rather than to force-add past it.
  --md     a Markdown summary, which is tracked, so a reader of the repository
           has the finding without having to run anything.

Usage:
    python3 compare_bibliographies_bp.py BP_background_section.md \\
            --out BACKGROUND_BIBLIO_COMPARISON.tsv \\
            --md  BACKGROUND_BIBLIO_COMPARISON.md
"""
import argparse
import collections
import csv
import re
import sys

# A reference entry in the body block. Two shapes occur in the same file:
#   [1]\n  authors: ...        (SciSpace export, entries 1-102)
#   [103] Brennan, B.G.; et al.\n  title: ...   (entries 103-130)
BLOCK = re.compile(r"^\[(\d+)\][ \t]*(.*)\n((?:[ \t]+\w+:.*\n)+)", re.M)
FIELD = re.compile(r"^[ \t]+(\w+):[ \t]*(.*)$", re.M)
LIST = re.compile(r"^\[(\d+)\](.*?)(?=\n\[\d+\]|\Z)", re.S | re.M)
TRAILING_DOI = re.compile(r'(10\.\d{4,9}/[^\s,"]+?)\.?$')
INLINE_DOI = re.compile(r"(?i)\bdoi:\s*(10\.\d{4,9}/\S+?)(?:[.,;]\s|$|\s)")


def block_entries(text):
    out = {}
    for m in BLOCK.finditer(text):
        fields = {k: v.strip() for k, v in FIELD.findall(m.group(3))}
        if m.group(2).strip():
            fields["authors_inline"] = m.group(2).strip()
        out[int(m.group(1))] = fields
    return out


def list_entries(text):
    return {int(m.group(1)): " ".join(m.group(2).split()) for m in LIST.finditer(text)}


def doi_of_list_entry(entry):
    m = TRAILING_DOI.search(entry.strip()) or INLINE_DOI.search(entry + " ")
    return m.group(1).rstrip(".").lower() if m else ""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("document")
    ap.add_argument("--refs-heading", default="## References")
    ap.add_argument("--block-marker",
                    default="These are the papers cited in the insights:",
                    help="line that introduces the machine-readable block")
    ap.add_argument("--out", help="write the per-number TSV here")
    ap.add_argument("--md", help="write the tracked Markdown summary here")
    ap.add_argument("--min-entries", type=int, default=50,
                    help="refuse to report if fewer than this many numbers are "
                         "found on either side. A comparison over an empty set "
                         "reports perfect agreement, which is this project's "
                         "signature false pass")
    a = ap.parse_args()

    text = open(a.document, encoding="utf-8").read()
    if a.refs_heading not in text:
        sys.exit(f"REFUSING: no '{a.refs_heading}' heading in {a.document}")
    if a.block_marker not in text:
        sys.exit(f"REFUSING: no second bibliography found in {a.document}. "
                 f"There is nothing to compare, which is not the same as "
                 f"nothing being wrong.")

    i = text.index("\n" + a.refs_heading)
    body, refs = text[:i], text[i:]
    block = block_entries(body[body.index(a.block_marker):])
    printed = list_entries(refs)
    prose = body[:body.index(a.block_marker)]

    if len(block) < a.min_entries or len(printed) < a.min_entries:
        sys.exit(f"REFUSING: parsed {len(block)} block entries and "
                 f"{len(printed)} list entries, expected at least "
                 f"{a.min_entries} of each. The parser is broken, not the file.")

    marks = collections.Counter()
    for grp in re.findall(r"\[(\d+(?:\s*,\s*\d+)*)\]", prose):
        for n in grp.split(","):
            marks[int(n.strip())] += 1

    rows = []
    for n in sorted(set(block) | set(printed)):
        b, p = block.get(n, {}), printed.get(n, "")
        bd = (b.get("doi", "") or "").lower()
        pd = doi_of_list_entry(p)
        if not p:
            verdict = "NO-LIST-ENTRY"
        elif not b:
            verdict = "NO-BLOCK-ENTRY"
        elif bd and pd:
            verdict = "AGREE" if bd == pd else "DISAGREE"
        else:
            verdict = "UNDECIDABLE"
        rows.append(dict(
            n=n,
            prose_marks=marks.get(n, 0),
            verdict=verdict,
            # 10.60692 with no journal is the fabrication signature recorded in
            # REFERENCES_RESOLVED_2026-09-03.md. The third element of it, a title
            # that paraphrases the citing sentence, is not mechanical and is not
            # tested here.
            fabrication_signature="YES" if bd.startswith("10.60692") and not b.get("journal") else "",
            block_title=b.get("title", "")[:150],
            block_doi=bd,
            block_pmid=b.get("pmid", ""),
            list_entry=p[:200],
            list_doi=pd,
        ))

    counts = collections.Counter(r["verdict"] for r in rows)
    by_mark = collections.Counter()
    for r in rows:
        by_mark[r["verdict"]] += r["prose_marks"]

    print(f"document              : {a.document}")
    print(f"block entries         : {len(block)}")
    print(f"printed list entries  : {len(printed)}")
    print(f"citation marks in prose: {sum(marks.values())}")
    print()
    print(f"{'verdict':16s} {'numbers':>8s} {'marks':>8s}")
    for v in ("AGREE", "DISAGREE", "UNDECIDABLE", "NO-LIST-ENTRY", "NO-BLOCK-ENTRY"):
        if counts[v] or by_mark[v]:
            print(f"{v:16s} {counts[v]:8d} {by_mark[v]:8d}")
    fab = sum(1 for r in rows if r["fabrication_signature"])
    print(f"\nfabrication signature : {fab}")
    dis = [r["n"] for r in rows if r["verdict"] == "DISAGREE"]
    if dis:
        print(f"first divergence at   : [{min(dis)}]")

    if a.out:
        with open(a.out, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t")
            w.writeheader()
            w.writerows(rows)
        print(f"\nwrote {a.out}")

    if a.md:
        with open(a.md, "w", encoding="utf-8") as fh:
            fh.write("# Which paper does each citation number point at?\n\n")
            fh.write(f"Generated by `compare_bibliographies_bp.py` from "
                     f"`{a.document}`. Regenerate rather than edit.\n\n")
            fh.write("`AGREE` and `DISAGREE` compare the DOI held by the body "
                     "block against the DOI in the printed reference list. The "
                     "prose follows the block, so `DISAGREE` means the printed "
                     "list names a work the citing sentence is not about.\n\n")
            fh.write("| verdict | numbers | prose marks |\n|---|---|---|\n")
            for v in ("AGREE", "DISAGREE", "UNDECIDABLE", "NO-LIST-ENTRY", "NO-BLOCK-ENTRY"):
                if counts[v] or by_mark[v]:
                    fh.write(f"| {v} | {counts[v]} | {by_mark[v]} |\n")
            fh.write(f"\nEntries carrying the `10.60692` fabrication signature: {fab}\n")
            fh.write("\n## Per number\n\n")
            fh.write("| n | marks | verdict | fab | block says | printed list says |\n")
            fh.write("|---|---|---|---|---|---|\n")
            for r in rows:
                bt = r["block_title"].replace("|", "/")[:70]
                pe = r["list_entry"].replace("|", "/")[:70]
                fh.write(f"| {r['n']} | {r['prose_marks']} | {r['verdict']} | "
                         f"{r['fabrication_signature']} | {bt} | {pe} |\n")
        print(f"wrote {a.md}")

    sys.exit(1 if counts["DISAGREE"] else 0)


if __name__ == "__main__":
    main()
