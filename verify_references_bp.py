#!/usr/bin/env python3
"""
verify_references_bp.py

Check a numbered reference list against the citations that use it, and against
what the identifiers actually resolve to.

WHY THIS EXISTS. `citation_audit_report.md` reported "130/130 refs cited and
defined, 0 orphans" for `BP_background_section.md`. The file as delivered cites
[1]-[130] in prose and defines [1]-[96]. Thirty-four citations point at nothing.
The audit checked internal consistency of the part it had built and then asserted
a whole-file verification it had not run, which is the same failure this project
keeps hitting: a plausible status line standing in for a measurement.

WHAT IT CHECKS, in the order the failures matter:

  1. DANGLING     cited in prose, absent from the reference list.
  2. ORPHAN       in the reference list, never cited.
  3. UNRESOLVABLE the DOI does not resolve at doi.org.
  4. NON-JOURNAL  the DOI resolves outside a publisher namespace. Seven entries
                  in the background carry the prefix 10.60692, which resolves to
                  a repository (gresis.osc.int) rather than a journal, and at
                  least four of those are real papers from 2008-2019 re-dated to
                  "July 2024". A real paper behind a wrong identifier and a wrong
                  year is harder to catch than an invented one.
  5. PREPRINT     cited as literature when a published version may exist.
  6. NO-METADATA  no journal volume, so the entry cannot be located by hand.
  7. NO-ID        neither DOI nor PMID.

WHAT IT DOES NOT CHECK. Whether the cited paper supports the sentence citing it.
No tool does that. This narrows the manual pass to the entries that survive, it
does not remove it.

Offline by default. Pass --online to resolve DOIs and query Crossref, which needs
network access and is the only part that is slow.

Stdlib only.
"""

import argparse
import collections
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.request

# Publisher prefixes seen in legitimate biomedical citation. Not exhaustive, and
# deliberately not used to reject: an unknown prefix is reported, not failed.
KNOWN_PUBLISHER = {
    "10.1038": "Nature Portfolio", "10.1371": "PLOS", "10.1128": "ASM",
    "10.1093": "Oxford UP", "10.1016": "Elsevier", "10.1099": "Microbiology Soc",
    "10.1073": "PNAS", "10.1101": "CSHL (Genome Res / bioRxiv)",
    "10.1155": "Hindawi", "10.3201": "CDC EID", "10.4269": "ASTMH",
    "10.1186": "BMC", "10.3389": "Frontiers", "10.1111": "Wiley",
    "10.1056": "NEJM", "10.1080": "Taylor & Francis", "10.1017": "Cambridge UP",
    "10.1136": "BMJ", "10.3390": "MDPI", "10.1265": "J-Stage",
    "10.1097": "Wolters Kluwer", "10.1002": "Wiley", "10.1126": "AAAS",
    "10.1534": "Genetics Soc", "10.7717": "PeerJ", "10.1146": "Annual Reviews",
    "10.1089": "Mary Ann Liebert", "10.1099": "Microbiology Society",
}
PREPRINT_MARKERS = re.compile(
    r"(?i)\bbiorxiv\b|\bmedrxiv\b|\bpreprint\b|10\.20944/preprints|"
    r"\bresearch\s*square\b|10\.21203")
ABSTRACT_MARKERS = re.compile(r"(?i)supplement(_|\s)|^\s*[A-Z]-\d+\.|\bposter\b")


def read_text(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    # Drive's markdown export backslash-escapes punctuation. Undo it.
    for a, b in [("\\#", "#"), ("\\*", "*"), ("\\[", "["), ("\\]", "]"),
                 ("\\`", "`"), ("\\_", "_"), ("\\-", "-"), ("\\(", "("),
                 ("\\)", ")"), ("\\>", ">"), ("\\.", ".")]:
        raw = raw.replace(a, b)
    return raw


def split_document(text, heading):
    i = text.find(heading)
    if i < 0:
        return text, ""
    return text[:i], text[i:]


def parse_entries(refs):
    """
    Return {number: entry_text} for a reference list.

    Two styles occur in this project and both must parse, because the audit is
    only worth having if it can be pointed at the manuscript as well as at the
    background. The background numbers entries '[1] Author ...'; the manuscript
    numbers them '1. Author ...'. Whichever style yields more entries wins, so
    no caller has to declare it.
    """
    bracket, numbered = {}, {}
    for m in re.finditer(r"^\s*\[(\d+)\]\s*(.*?)(?=^\s*\[\d+\]|\Z)",
                         refs, flags=re.M | re.S):
        bracket[int(m.group(1))] = " ".join(m.group(2).split())
    for m in re.finditer(r"^\s*(\d{1,3})\.\s+(.*?)(?=^\s*\d{1,3}\.\s|\Z)",
                         refs, flags=re.M | re.S):
        numbered[int(m.group(1))] = " ".join(m.group(2).split())
    return bracket if len(bracket) >= len(numbered) else numbered


def cited_numbers(body):
    """
    Every citation number appearing in prose, including grouped markers.

    '[1]' and '[1,2]' and '[1, 2]' all cite. Matching only '\\[(\\d+)\\]' silently
    drops every grouped marker, which in the manuscript means missing the very
    first citation in the Introduction.
    """
    out = collections.Counter()
    for grp in re.findall(r"\[(\d+(?:\s*,\s*\d+)*)\]", body):
        for n in grp.split(","):
            out[int(n.strip())] += 1
    return out


def doi_of(entry):
    m = re.search(r"(?i)\bdoi:\s*(10\.\d{4,9}/\S+?)(?:[.,;]\s|$|\s)", entry + " ")
    return m.group(1).rstrip(".,;") if m else None


def pmid_of(entry):
    m = re.search(r"(?i)\bPMID:?\s*(\d{6,9})", entry)
    return m.group(1) if m else None


def resolve_doi(doi, timeout=12):
    """Return (ok, target_url). Uses the handle API, which is fast and stable."""
    url = "https://doi.org/api/handles/" + urllib.parse.quote(doi, safe="/.")
    try:
        with urllib.request.urlopen(url, timeout=timeout) as fh:
            d = json.load(fh)
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, f"{type(e).__name__}"
    if d.get("responseCode") != 1:
        return False, f"responseCode {d.get('responseCode')}"
    for v in d.get("values", []):
        if v.get("type") == "URL":
            return True, v["data"]["value"]
    return True, "(resolved, no URL value)"


def main():
    ap = argparse.ArgumentParser(
        description="Audit a numbered reference list for dangling citations, "
                    "orphans, and identifiers that do not resolve to a journal.")
    ap.add_argument("document", help="markdown file containing prose + references")
    ap.add_argument("--refs-heading", default="## References",
                    help="heading that starts the reference list")
    ap.add_argument("--online", action="store_true",
                    help="resolve every DOI at doi.org (needs network)")
    ap.add_argument("--sleep", type=float, default=0.1,
                    help="delay between online lookups")
    ap.add_argument("--out", help="write a per-reference TSV here")
    ap.add_argument("--max-dangling", type=int, default=0, metavar="N",
                    help="tolerate at most N dangling citations before failing. "
                         "A ratchet: set it to the current count so the number "
                         "can only go down, rather than demanding a clean sheet "
                         "before the audit may run in CI at all")
    ap.add_argument("--warn-only", action="store_true",
                    help="report entry-level flags but do not fail on them. "
                         "Dangling citations still fail, because a citation "
                         "pointing at nothing is a defect and a thesis-repository "
                         "DOI is a judgement call")
    a = ap.parse_args()

    text = read_text(a.document)
    body, refs = split_document(text, a.refs_heading)
    if not refs:
        print(f"ABORT: no '{a.refs_heading}' heading found. "
              f"The file has no reference list at all.", file=sys.stderr)
        sys.exit(2)

    cited = cited_numbers(body)
    entries = parse_entries(refs)

    dangling = sorted(n for n in cited if n not in entries)
    orphan = sorted(n for n in entries if n not in cited)

    print("=" * 74)
    print(f"REFERENCE AUDIT  {a.document}")
    print("=" * 74)
    print(f"  citation marks in prose      : {sum(cited.values())}")
    print(f"  distinct numbers cited       : {len(cited)}"
          f"  (range {min(cited)}-{max(cited)})" if cited else "")
    print(f"  entries in the reference list: {len(entries)}"
          f"  (range {min(entries)}-{max(entries)})" if entries else "")
    print()
    print(f"  DANGLING (cited, undefined)  : {len(dangling)}")
    if dangling:
        print(f"     {dangling}")
        print("     Every one of these citation marks points at nothing.")
    print(f"  ORPHAN (defined, uncited)    : {len(orphan)}")
    if orphan:
        print(f"     {orphan}")

    rows = []
    counts = collections.Counter()
    for n in sorted(entries):
        e = entries[n]
        doi, pmid = doi_of(e), pmid_of(e)
        flags = []
        if not doi and not pmid:
            flags.append("NO-ID")
        if "vol." not in e:
            flags.append("NO-METADATA")
        if PREPRINT_MARKERS.search(e) and not re.search(r"10\.1101/gr\.", e):
            flags.append("PREPRINT")
        if ABSTRACT_MARKERS.search(e):
            flags.append("ABSTRACT")
        prefix = doi.split("/")[0] if doi else None
        if prefix and prefix not in KNOWN_PUBLISHER:
            flags.append(f"UNKNOWN-PREFIX:{prefix}")
        target = ""
        if a.online and doi:
            ok, target = resolve_doi(doi)
            if not ok:
                flags.append(f"UNRESOLVABLE:{target}")
            elif not re.search(r"(?i)doi\.org|link\.springer|nature\.com|"
                               r"journals\.plos|asm\.org|academic\.oup|"
                               r"sciencedirect|ncbi\.nlm\.nih\.gov|wiley|"
                               r"tandfonline|frontiersin|biomedcentral|"
                               r"cambridge\.org|bmj\.com|mdpi\.com|nejm\.org|"
                               r"cdc\.gov|ajtmh\.org|microbiologyresearch|"
                               r"genome\.cshlp|pnas\.org|peerj|liebertpub|"
                               r"lww\.com|jstage|hindawi|annualreviews|"
                               r"science\.org|genetics\.org", target):
                flags.append("NON-JOURNAL-TARGET")
            time.sleep(a.sleep)
        for f in flags:
            counts[f.split(":")[0]] += 1
        rows.append({"ref": n, "cited_times": cited.get(n, 0), "doi": doi or "",
                     "pmid": pmid or "", "resolves_to": target,
                     "flags": ";".join(flags), "entry": e[:300]})

    print()
    print("  entry-level flags")
    for k, v in counts.most_common():
        print(f"     {k:22} {v}")
    if not counts:
        print("     none")

    worst = [r for r in rows if r["flags"]]
    if worst:
        print()
        print(f"  {len(worst)} entries carry at least one flag. First 15:")
        for r in worst[:15]:
            print(f"     [{r['ref']:>3}] {r['flags']}")
            print(f"           {r['entry'][:110]}")

    if a.out:
        with open(a.out, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()),
                               delimiter="\t", lineterminator="\n")
            w.writeheader()
            for r in rows:
                w.writerow(r)
        print(f"\n  wrote {a.out}")

    print()
    print("  NOTE: this checks that a citation points at a real, locatable,")
    print("  published thing. It does NOT check that the paper supports the")
    print("  sentence citing it. That pass is still manual.")

    over = len(dangling) - a.max_dangling
    if over > 0:
        print(f"\n  FAIL: {len(dangling)} dangling citations, "
              f"{a.max_dangling} tolerated ({over} over).")
        sys.exit(1)
    if dangling:
        print(f"\n  {len(dangling)} dangling, within the tolerated "
              f"{a.max_dangling}. Ratchet this down as they are fixed.")
    if counts and not a.warn_only:
        print("\n  FAIL: entry-level flags present.")
        sys.exit(1)
    print("\n  PASS")
    sys.exit(0)


if __name__ == "__main__":
    import urllib.parse
    main()
