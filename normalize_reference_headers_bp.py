#!/usr/bin/env python3
"""
normalize_reference_headers_bp.py

Rewrite the deflines of the mapping references to short, stable replicon ids.

WHY THIS EXISTS — it is a correctness fix, not tidying.

`SPLIT_REFERENCE_REPLICONS` names each replicon after the sanitised first token
of its defline, and the workflow then keys the analysis unit as
`<cluster_id>__<replicon id>`. Gubbins passes `<unit>.core.full.iteration_N` and
`<unit>.core.full.iteration_N_reconstruction` to RAxML as the `-n` run id.

**RAxML v8 segfaults (exit 139) on a `-n` run id of 128 characters or more.**
Measured directly: identical inputs, only the `-n` length varied --
127 chars exits 0, 128 chars exits 139, and the `-w` working-directory path
length makes no difference. RAxML even contains the string "Error: run id after
\\"-n\\" is too long" but crashes before printing it, so the operator sees
nothing. Gubbins wraps the call in a bare `except` and reports only
"Unable to fit model to data", which is why this looked like a model-fitting
problem for an entire investigation.

This collection's deflines are the whole filename plus a contig index, e.g.
`Burkholderia_pseudomallei_vgh07_GCF_000954175.1_Taiwan_Kaohsiung_Veterans_General_Hospital_Kaohsiung.fasta_1`
(108 characters). With `strain_1_L1_18__` in front and Gubbins' 37-character
suffix behind, the run id reaches 161 -- and that unit dies. Measured on the L1
partition before this fix: **40 of 164 replicon-units (24%) were over the
limit**, including `strain_1_L1_9` (n=90).

THE NEW DEFLINE is `<accession>_<index>`, e.g. `GCF_000954175_1_1`. The
accession alone identifies the reference unambiguously, the index distinguishes
replicons, and the result is ~17 characters instead of ~108. The location label
is not lost -- `curated_L1_reference_audit.tsv` maps every unit to its full
reference name.

SEQUENCE DATA IS NOT TOUCHED. Only `>` lines change, and the script verifies
that the residue stream of every output is byte-identical to its input before
writing anything.
"""

import argparse
import csv
import hashlib
import os
import re
import sys

from write_if_changed_bp import write_if_changed


ACCESSION = re.compile(r'(GC[AF]_\d+[._]\d+)')

# Gubbins appends ".core.full.iteration_N_reconstruction" to the unit name
# before handing it to RAxML as -n. Measured: unit of 99 chars -> run id of 136.
GUBBINS_SUFFIX = len(".core.full.iteration_1_reconstruction")
RAXML_LIMIT = 127


def accession_of(stem):
    """
    The accession is the stable identifier; everything else in these filenames
    is a location label that varies in length from 'unknown' to
    'Taiwan_Kaohsiung_Veterans_General_Hospital_Kaohsiung'.
    """
    m = ACCESSION.search(stem)
    if m:
        return m.group(1).replace(".", "_")
    # No accession in the name (e.g. a CP0184xx chromosome record). Fall back to
    # a truncated stem plus a hash, so the id stays short AND unique.
    safe = re.sub(r'[^A-Za-z0-9]', '_', stem)[:24].strip("_")
    return f"{safe}_{hashlib.md5(stem.encode()).hexdigest()[:6]}"


def residues(path):
    """Sequence bytes only, deflines excluded, for the equality check."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for line in fh:
            if not line.startswith(b">"):
                h.update(line.strip())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refs", required=True, help="TSV: cluster_id, reference_path")
    ap.add_argument("--outdir", default="refs_normalized")
    ap.add_argument("--out-refs", default="curated_L1_refs_normalized.tsv")
    a = ap.parse_args()

    os.makedirs(a.outdir, exist_ok=True)

    rows = list(csv.DictReader(open(a.refs), delimiter="\t"))
    originals = {}
    for r in rows:
        originals[r["reference_path"]] = None

    written, ids_seen = {}, {}
    n_written = 0
    for src in sorted(originals):
        stem = os.path.basename(src).rsplit(".", 1)[0]
        acc = accession_of(stem)
        dst = os.path.join(a.outdir, f"{acc}.fasta")

        n = 0
        out = []
        with open(src) as fin:
            for line in fin:
                if line.startswith(">"):
                    n += 1
                    rid = f"{acc}_{n}"
                    if ids_seen.setdefault(rid, src) != src:
                        sys.exit(f"ERROR: replicon id {rid} collides between "
                                 f"{ids_seen[rid]} and {src}")
                    out.append(f">{rid}\n")
                else:
                    out.append(line)

        # Write ONLY if the content differs. Nextflow's default cache hashing
        # includes mtime, so rewriting a byte-identical reference invalidates
        # every task that consumed it -- and this script runs on every launch of
        # the runner, including plain `-resume`.
        rewrote = write_if_changed(dst, "".join(out))
        if rewrote:
            n_written += 1

        if residues(src) != residues(dst):
            sys.exit(f"ERROR: sequence content changed for {src} -- refusing")
        written[src] = dst

    import io
    buf = io.StringIO()
    w = csv.writer(buf, delimiter="\t", lineterminator="\n")
    w.writerow(["cluster_id", "reference_path"])
    for r in rows:
        w.writerow([r["cluster_id"], os.path.abspath(written[r["reference_path"]])])
    write_if_changed(a.out_refs, buf.getvalue())

    # Prove the fix: recompute what the longest RAxML run id will now be.
    worst = []
    for r in rows:
        dst = written[r["reference_path"]]
        acc = os.path.basename(dst).rsplit(".", 1)[0]
        n_rep = sum(1 for line in open(dst) if line.startswith(">"))
        for i in range(1, n_rep + 1):
            unit = f"{r['cluster_id']}__{acc}_{i}"
            worst.append((len(unit) + GUBBINS_SUFFIX, unit))
    worst.sort(reverse=True)
    over = [w for w in worst if w[0] > RAXML_LIMIT]

    print(f"references normalized : {len(written)} -> {a.outdir}/  ({n_written} rewritten, {len(written)-n_written} unchanged)")
    print(f"sequence content      : verified identical for all {len(written)}")
    print(f"longest RAxML run id  : {worst[0][0]} chars (limit {RAXML_LIMIT})")
    print(f"  from unit           : {worst[0][1]}")
    print(f"replicon-units over   : {len(over)} of {len(worst)}")
    if over:
        for n, u in over[:5]:
            print(f"    STILL TOO LONG {n}: {u}")
        sys.exit(2)
    print(f"\nwrote {a.out_refs}")


if __name__ == "__main__":
    main()
