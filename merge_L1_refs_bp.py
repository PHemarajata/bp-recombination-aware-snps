#!/usr/bin/env python3
"""
merge_L1_refs_bp.py

Combine the two halves of the reference decision into the one file the pipeline
consumes: cluster_id <TAB> reference_path.

An internal reference is a cluster member chosen for centrality; a borrowed one
is the nearest complete genome from outside a cluster that has no complete
member of its own. Curated mode does not care about the distinction, so they are
merged here, with the source recorded in the audit file so it stays quotable.

WHERE THE BORROWED REFERENCE COMES FROM, and why not from the picker.
pick_cluster_references_bp.py builds its borrow pool out of genomes it has
already read while scoring cluster members -- which means it can only borrow
from inside the analysed partition. That is 2,070 genomes, not the 2,802 in the
collection, and it costs real distance: measured across the 82 L1 units, 17
borrowed references were further from their unit than the best complete genome
in the collection, strain_13_L1_3 by 5.1x (mean Mash 0.00402 against 0.00078).
Given this project's own measurement that a distant reference inflates SNP calls
by up to 630% in a tight cluster, that is not a rounding error. So borrowed
references are taken from rank_reference_alternates_bp.py, which ranks all 189
complete genomes in the collection by the SAME criterion the picker uses.

Internal picks still win where they exist. A complete member is inside its own
cluster by definition, and the three units where an outsider ranked above the
internal pick differ by 1.00-1.05x -- nothing worth trading away the property
that makes an internal reference the right default.

Two things this deliberately re-checks rather than trusts:

  * BLOCKLIST. The picker filters it, but the blocklist is the whole reason the
    six previously-failing units are analysable at all, so it is enforced again
    on the merged result. A blocked reference reaching the run is a hard error,
    not a warning.
  * PATHS. cluster_references.tsv from an in-workflow run records the path the
    reference was staged at INSIDE the task directory, which dies with the work
    dir. Everything here resolves by basename against the live collection, and
    a reference that does not resolve is a hard error.
"""

import argparse
import csv
import os
import sys


def load_blocklist(path):
    out = []
    if path:
        with open(path) as fh:
            for line in fh:
                line = line.split("#", 1)[0].strip()
                if line:
                    out.append(line)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selection", required=True,
                    help="curated_L1_reference_selection.tsv")
    ap.add_argument("--alternates", required=True,
                    help="curated_L1_ref_alternates.tsv; rank 1 supplies the "
                         "reference for every unit with no complete member")
    ap.add_argument("--fasta-dir", required=True)
    ap.add_argument("--blocklist", default=None)
    ap.add_argument("--out", default="curated_L1_refs.tsv")
    ap.add_argument("--audit", default="curated_L1_reference_audit.tsv")
    a = ap.parse_args()

    blocked = load_blocklist(a.blocklist)

    listing = {}
    for fn in os.listdir(a.fasta_dir):
        if fn.endswith((".fasta", ".fa", ".fna")):
            listing[fn.rsplit(".", 1)[0]] = os.path.join(a.fasta_dir, fn)

    chosen = {}
    with open(a.selection) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r["status"] == "ready" and r["reference"]:
                chosen[r["cluster_id"]] = (r["reference"], "internal", r["n"],
                                           r.get("ref_mean_mash", ""),
                                           r.get("ref_max_mash", ""))
    n_internal = len(chosen)

    best = {}
    with open(a.alternates) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r["rank"] == "1":
                best[r["cluster_id"]] = r
    for cid, r in best.items():
        if cid in chosen:
            continue              # an internal pick always wins
        chosen[cid] = (r["reference"], "borrowed", "", r["mean_mash"],
                       r["max_mash"])

    errors = []
    rows = []
    for cid in sorted(chosen, key=lambda c: (int(c.split("_")[1]),
                                             int(c.split("_L1_")[1]))):
        ref, source, n, mean_d, max_d = chosen[cid]
        if any(ref.startswith(p) for p in blocked):
            errors.append(f"{cid}: blocked reference {ref} survived selection")
            continue
        path = listing.get(ref)
        if path is None:
            for stem, q in listing.items():
                if stem.startswith(ref):
                    path = q
                    break
        if path is None:
            errors.append(f"{cid}: reference {ref} not found in {a.fasta_dir}")
            continue
        rows.append((cid, path, ref, source, n, mean_d, max_d))

    if errors:
        print("REFUSING TO WRITE -- %d unresolved:" % len(errors), file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        sys.exit(2)

    with open(a.out, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")   # never CRLF
        w.writerow(["cluster_id", "reference_path"])
        for cid, path, _, _, _, _, _ in rows:
            w.writerow([cid, path])

    with open(a.audit, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["cluster_id", "reference", "source", "n",
                    "mean_mash", "max_mash"])
        for cid, _, ref, source, n, mean_d, max_d in rows:
            w.writerow([cid, ref, source, n, mean_d, max_d])

    distinct = len({r[2] for r in rows})
    print(f"units with a reference : {len(rows)} "
          f"({n_internal} internal, {len(rows) - n_internal} borrowed)")
    print(f"distinct references    : {distinct}")
    print(f"blocklist enforced     : {len(blocked)} prefixes, 0 survivors")
    print(f"\nwrote {a.out} and {a.audit}")


if __name__ == "__main__":
    main()
