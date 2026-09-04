#!/usr/bin/env python3
"""
build_bibliography_bp.py

Match every reference in a numbered bibliography against this project's
PubMed-verified citation corpus, and say for each one what should happen to it.

WHY THIS EXISTS. `verify_references_bp.py` says which entries in
`BP_background_section.md` are unusable: 34 citations point at nothing, and 46 of
the 96 that exist carry a flag offline, 64 once DOIs are resolved. It does not
say what to put in their place. Repairing 96 entries in situ is more work than
rebuilding, and it ends with a bibliography nobody can inspect. This tool does
the mechanical half of the rebuild: it finds, for each background reference, the
corresponding entry in `BACKGROUND_RESEARCH_*.md` and `BACKGROUND_SRC_*.md`,
where citations carry PMIDs and DOIs that were checked against PubMed by hand and
where UNVERIFIED is marked in place.

WHAT IT DOES NOT DO. It does not decide whether the cited paper supports the
sentence citing it, and it does not write the new bibliography. It produces the
triage table a human works from, so the manual pass is spent on the entries that
actually need judgement rather than on the 60-odd that resolve mechanically.

THE MERGE RULE it enforces, from the handoff section 5: no 10.60692, no Zenodo,
no thesis repository, no conference abstract, and no repository copy of a paper
that has a publisher DOI. An entry matching one of those is never KEEP, even when
its identifier resolves.

Verdicts, in the order they are assigned:

  DANGLING        cited in prose, no entry at all. Needs a source or the claim
                  must go. These are [97]-[130].
  REPLACE         entry is flagged AND a verified corpus record matches. The
                  mechanical win: swap in the corpus citation.
  LOOKUP          entry is flagged and nothing matches. Needs a PubMed lookup or
                  the claim must be re-sourced. This is the real backlog.
  KEEP            entry is unflagged and a corpus record confirms it.
  KEEP-UNMATCHED  entry is unflagged but absent from the corpus. Probably fine,
                  it has a publisher DOI, but it is uncorroborated here.

Matching is by DOI, then PMID, then title similarity, and the column says which
was used so a title match can be eyeballed. Stdlib only.
"""

import argparse
import csv
import difflib
import re
import sys

# Reuse the audit's notion of what is wrong with an entry, so the two tools
# cannot drift apart on the definition of "flagged".
from verify_references_bp import (
    KNOWN_PUBLISHER, PREPRINT_MARKERS, ABSTRACT_MARKERS,
    read_text, split_document, parse_entries, doi_of, pmid_of,
)

# Prefixes the merge rule refuses outright, whatever they resolve to.
REFUSED_PREFIX = {
    "10.60692": "repository, not a journal",
    "10.5281": "Zenodo deposit",
    "10.25913": "thesis repository",
    "10.17863": "institutional repository copy",
    "10.6084": "figshare deposit",
    "10.20944": "Preprints.org",
    "10.21203": "Research Square preprint",
}

DOI_RE = re.compile(r"10\.\d{4,9}/[^\s)\]|,;\"']+")
PMID_RE = re.compile(r"(?:PMID:?|pmid:?)\s*\**\s*(\d{7,8})")


def norm_doi(d):
    return d.rstrip(".,;)]").lower() if d else ""


def norm_title(s):
    """Lowercase, drop markdown and punctuation, collapse space."""
    s = re.sub(r"[*_`$]|\\textit|\{|\}", " ", s or "")
    s = re.sub(r"[^a-z0-9 ]+", " ", s.lower())
    return " ".join(s.split())


def bg_title(entry):
    """The title of a background entry: the text inside curly or plain quotes."""
    m = re.search(r"[“\"](.+?)[”\"]", entry)
    return m.group(1) if m else entry


# Words too common in this literature to carry any evidence of a match. Every
# citation in the corpus is about this organism, so these are noise.
STOP = {
    "burkholderia", "pseudomallei", "melioidosis", "with", "from", "that",
    "this", "into", "their", "there", "which", "using", "based", "study",
    "analysis", "human", "clinical", "infection", "disease", "bacterial",
}


def distinctive(s):
    return {w for w in s.split() if len(w) >= 4 and w not in STOP}


def sim(tn, cn):
    """
    How well a background title sits inside a corpus citation.

    Two measures, and both must agree.

    Plain ratio() is wrong alone, because the strings are different kinds of
    object: a bare title against a full citation carrying twelve authors, a
    journal and three identifiers. The title is a short island in a long string,
    so ratio() is diluted by everything around it. Character containment fixes
    that but overshoots in the other direction: with every citation in the corpus
    sharing "melioidosis" and "burkholderia pseudomallei", scattered matches on
    common vocabulary inflate the score. At a 0.72 cutoff that paired a Zenodo
    deposit with a Mohapatra review, a conference abstract with Currie, and
    Chantratita with Seng, all on shared words alone.

    So take the weaker of character containment and distinctive-token overlap. A
    real match scores high on both; a vocabulary coincidence scores high on
    characters and low on tokens, and min() throws it out.
    """
    if not tn or not cn:
        return 0.0
    sm = difflib.SequenceMatcher(None, tn, cn)
    matched = sum(b.size for b in sm.get_matching_blocks())
    char = max(sm.ratio(), matched / len(tn))
    tt = distinctive(tn)
    # A title with one or two distinctive words cannot be matched on words: the
    # overlap is trivially 1.0 and carries no evidence. "Paediatric melioidosis"
    # reduces to {paediatric} and on that basis matched a Cambodia study by a
    # different author in a different journal fourteen years apart. Such titles
    # need a DOI or a PMID, not a guess.
    if len(tt) < 3:
        return 0.0
    tok = len(tt & distinctive(cn)) / len(tt)
    return min(char, tok)


def blocks_of(text):
    """
    Yield citation-sized chunks. Table rows stand alone; everything else is
    grouped into paragraphs, because inline citations wrap across lines and a
    line-wise reader sees only a fragment of the title. That fragment then fails
    to match, which is how [87] Chewapreecha 2019 was missed on the first pass
    despite sitting in BACKGROUND_SRC_5 with a PMID.
    """
    buf = []
    for ln in text.splitlines():
        if ln.lstrip().startswith("|"):
            if buf:
                yield " ".join(buf)
                buf = []
            yield ln
        elif not ln.strip():
            if buf:
                yield " ".join(buf)
                buf = []
        else:
            buf.append(ln.strip())
    if buf:
        yield " ".join(buf)


def load_corpus(paths):
    """
    Pull every citation carrying a PMID or a DOI out of the corpus files.

    Two shapes appear: markdown table rows '| topic | citation | PMID | DOI |',
    and prose '**Citation:** Authors. Title. Journal. year. PMID nnnn.' blocks
    that may wrap over several lines.
    """
    out, seen = [], set()
    for path in paths:
        try:
            text = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for block in blocks_of(text):
            pm = PMID_RE.search(block)
            dm = DOI_RE.search(block)
            if not pm and not dm:
                continue
            if block.lstrip().startswith("|"):
                cells = [c.strip() for c in block.strip().strip("|").split("|")]
                cells = [c for c in cells if not re.fullmatch(r"[-: ]*", c)]
                if len(cells) < 2:
                    continue
                citation = max(cells, key=len)
                # In these tables the PMID is a bare number in its own column,
                # with no "PMID" prefix for PMID_RE to find. Those rows are the
                # bulk of the corpus and the ones carrying identifiers, so
                # missing them empties the very column this tool exists to fill.
                if not pm:
                    for c in cells:
                        bare = re.fullmatch(r"\**\s*(\d{7,8})\s*\**\s*[⚠✓?]*", c)
                        if bare:
                            pm = bare
                            break
            else:
                citation = re.sub(r"(?i)\**(full )?citation:?\**", " ", block)
                citation = citation.lstrip("->*# ").strip()
            citation = re.sub(r"\s+", " ", citation)
            if len(citation) < 25:
                continue
            pmid = pm.group(1) if pm else ""
            doi = norm_doi(dm.group(0)) if dm else ""
            key = (pmid, doi, citation[:80])
            if key in seen:
                continue
            seen.add(key)
            out.append({"pmid": pmid, "doi": doi, "citation": citation[:400],
                        "source": path,
                        "unverified": bool(re.search(r"(?i)UNVERIFIED|⚠", block)),
                        "tnorm": norm_title(citation)})
    return out


def flags_for(entry):
    """Same rules as verify_references_bp, minus the online checks."""
    doi, pmid = doi_of(entry), pmid_of(entry)
    f = []
    if not doi and not pmid:
        f.append("NO-ID")
    if "vol." not in entry:
        f.append("NO-METADATA")
    if PREPRINT_MARKERS.search(entry) and not re.search(r"10\.1101/gr\.", entry):
        f.append("PREPRINT")
    if ABSTRACT_MARKERS.search(entry):
        f.append("ABSTRACT")
    prefix = doi.split("/")[0] if doi else None
    if prefix and prefix not in KNOWN_PUBLISHER:
        f.append(f"UNKNOWN-PREFIX:{prefix}")
    if prefix in REFUSED_PREFIX:
        f.append(f"REFUSED:{REFUSED_PREFIX[prefix]}")
    return f, doi, pmid


def richness(c):
    """
    How useful a corpus record is as a replacement. The same paper is often
    described several times across the corpus, and only some of those mentions
    carry the identifiers. Picking the first match returns a citation with no
    PMID, which defeats the point of the rebuild.
    """
    return (bool(c["pmid"]), bool(c["doi"]), not c["unverified"], len(c["citation"]))


def best_of(cands):
    return max(cands, key=richness) if cands else None


def match(entry_doi, entry_pmid, title, corpus, cutoff):
    if entry_doi:
        nd = norm_doi(entry_doi)
        hit = best_of([c for c in corpus if c["doi"] and c["doi"] == nd])
        if hit:
            return hit, "doi"
    if entry_pmid:
        hit = best_of([c for c in corpus if c["pmid"] and c["pmid"] == entry_pmid])
        if hit:
            return hit, "pmid"
    tn = norm_title(title)
    if len(tn) >= 20:
        scored = []
        for c in corpus:
            if not c["tnorm"]:
                continue
            s = sim(tn, c["tnorm"])
            if s >= cutoff:
                scored.append((s, c))
        if scored:
            top = max(s for s, _ in scored)
            # Among near-ties, take the record carrying the most identifiers.
            hit = best_of([c for s, c in scored if s >= top - 0.02])
            return hit, f"title:{top:.2f}"
    return None, ""


def main():
    ap = argparse.ArgumentParser(
        description="Triage a bibliography against the verified citation corpus.")
    ap.add_argument("document", help="markdown file with prose + references")
    ap.add_argument("corpus", nargs="+", help="verified corpus markdown files")
    ap.add_argument("--refs-heading", default="## References")
    ap.add_argument("--title-cutoff", type=float, default=0.72,
                    help="minimum title similarity to accept a match")
    ap.add_argument("--out", help="write the triage TSV here")
    a = ap.parse_args()

    text = read_text(a.document)
    body, refs = split_document(text, a.refs_heading)
    if not refs:
        print(f"ABORT: no '{a.refs_heading}' heading in {a.document}.",
              file=sys.stderr)
        sys.exit(2)

    cited = {}
    for m in re.findall(r"\[(\d+)\]", body):
        cited[int(m)] = cited.get(int(m), 0) + 1
    entries = parse_entries(refs)
    corpus = load_corpus(a.corpus)

    rows, tally = [], {}
    for n in sorted(set(entries) | set(cited)):
        if n not in entries:
            v = "DANGLING"
            row = {"ref": n, "cited_times": cited.get(n, 0), "verdict": v,
                   "flags": "", "match_by": "", "bg_doi": "", "bg_pmid": "",
                   "corpus_pmid": "", "corpus_doi": "", "corpus_unverified": "",
                   "corpus_citation": "", "bg_entry": ""}
        else:
            e = entries[n]
            fl, doi, pmid = flags_for(e)
            c, how = match(doi, pmid, bg_title(e), corpus, a.title_cutoff)
            refused = any(x.startswith("REFUSED") for x in fl)
            if c and fl:
                v = "REPLACE"
            elif c:
                v = "KEEP"
            elif fl:
                v = "LOOKUP"
            else:
                v = "KEEP-UNMATCHED"
            if refused and not c:
                v = "LOOKUP"
            row = {"ref": n, "cited_times": cited.get(n, 0), "verdict": v,
                   "flags": ";".join(fl), "match_by": how,
                   "bg_doi": doi or "", "bg_pmid": pmid or "",
                   "corpus_pmid": c["pmid"] if c else "",
                   "corpus_doi": c["doi"] if c else "",
                   "corpus_unverified": "yes" if (c and c["unverified"]) else "",
                   "corpus_citation": c["citation"] if c else "",
                   "bg_entry": e[:300]}
        tally[row["verdict"]] = tally.get(row["verdict"], 0) + 1
        rows.append(row)

    print("=" * 74)
    print(f"BIBLIOGRAPHY REBUILD TRIAGE  {a.document}")
    print("=" * 74)
    print(f"  verified corpus records loaded : {len(corpus)}"
          f"  (from {len(a.corpus)} files)")
    print(f"  reference numbers in play      : {len(rows)}")
    print()
    order = ["DANGLING", "LOOKUP", "REPLACE", "KEEP", "KEEP-UNMATCHED"]
    for k in order:
        if k in tally:
            print(f"    {k:16} {tally[k]:4}")
    print()
    mech = tally.get("REPLACE", 0) + tally.get("KEEP", 0)
    manual = tally.get("DANGLING", 0) + tally.get("LOOKUP", 0)
    print(f"  resolves mechanically : {mech}")
    print(f"  needs a human         : {manual}")

    if a.out:
        with open(a.out, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()),
                               delimiter="\t", lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        print(f"\n  wrote {a.out}")

    print()
    print("  NOTE: a match means the identifier or title lines up with a corpus")
    print("  record. It does NOT mean the paper supports the sentence citing it.")
    sys.exit(1 if manual else 0)


if __name__ == "__main__":
    main()
