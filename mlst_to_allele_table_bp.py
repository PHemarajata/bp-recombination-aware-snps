#!/usr/bin/env python3
"""Reshape MLST_v4c.tsv into the wide allele table score_cgmlst_lichtenegger.py eats.

Table 5's MLST row predates the validation-set correction and is due a re-run on
the current n = 46 set. The obvious way to do that is a fifth scorer; the
handoff's tech-debt item explicitly says not to write one, because the four that
exist each rebuild the reference pool and each re-implement leave-outbreak-out,
and that is where they drift apart.

So this does not score anything. It only converts the 7-locus MLST profile into
the same wide `FILE + one column per locus` shape as
`cgmlst_lichtenegger/results/results_alleles.tsv`, after which the existing
cgMLST scorer runs over it unchanged and the MLST row is produced by *the same
code path* as the cgMLST row -- pool construction, exposure overrides,
leave-group-out and leave-outbreak-out all included. That is the point: the two
rows of Table 5 become comparable by construction rather than by inspection.

  python3 mlst_to_allele_table_bp.py
  python3 score_cgmlst_lichtenegger.py \
      --profiles MLST_ALLELES_WIDE.tsv \
      --out-prefix MLST_ATTRIBUTION \
      --estimator nearest_neighbour
"""
import csv
import os
import re
import sys

B = os.path.dirname(os.path.abspath(__file__))
SRC = f"{B}/MLST_v4c.tsv"
OUT = f"{B}/MLST_ALLELES_WIDE.tsv"

TOKEN = re.compile(r"^([A-Za-z0-9_]+)\(([^)]*)\)$")

rows = list(csv.DictReader(open(SRC), delimiter="\t"))
if not rows:
    sys.exit(f"FATAL: {SRC} is empty")

# Establish the locus order from the first row that parses cleanly, then require
# every other row to match it. A silently reordered profile would scramble the
# allele columns and still produce a plausible-looking distance matrix.
loci = None
out, skipped = [], []
for r in rows:
    prof = (r.get("profile") or "").strip()
    if not prof:
        skipped.append((r["sample_id"], "empty profile"))
        continue
    pairs = []
    ok = True
    for tok in prof.split("\t"):
        tok = tok.strip()
        if not tok:
            continue
        m = TOKEN.match(tok)
        if not m:
            ok = False
            break
        pairs.append((m.group(1), m.group(2)))
    if not ok or not pairs:
        skipped.append((r["sample_id"], f"unparseable: {prof[:40]!r}"))
        continue
    names = [p[0] for p in pairs]
    if loci is None:
        loci = names
    elif names != loci:
        skipped.append((r["sample_id"], f"locus order differs: {names}"))
        continue
    out.append((r["sample_id"], [p[1] for p in pairs]))

if loci is None:
    sys.exit("FATAL: no parseable MLST profile found")

# The scorer treats '-', '0' and '' as missing and strips a leading '*' or
# 'INF-'. MLST novel/absent alleles come through as '-' or '~', so normalise the
# tilde form to something it already understands rather than teaching it a new
# sentinel.
with open(OUT, "w", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["FILE"] + loci)
    for sid, alleles in out:
        w.writerow([sid] + [("-" if a in ("", "~", "-", "0") else a)
                            for a in alleles])

print(f"wrote {OUT}")
print(f"  {len(out)} genomes x {len(loci)} loci: {', '.join(loci)}")
if skipped:
    print(f"  skipped {len(skipped)}:")
    for sid, why in skipped[:10]:
        print(f"    {sid}\t{why}")
    if len(skipped) > 10:
        print(f"    ... and {len(skipped) - 10} more")
