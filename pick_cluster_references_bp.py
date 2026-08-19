#!/usr/bin/env python3
"""
pick_cluster_references_bp.py

Choose a per-cluster mapping reference, and report how many clusters can
actually get a usable one.

Why this exists. The measured reference effect (Appendix A.3b/A.3c) is +28% in
a diffuse cluster and +630% in a tight one, with ~87% of calls false in the
latter. The fix is a within-cluster reference. But there are two hard
constraints the current pipeline does not respect:

  1. Gubbins cannot use a multi-contig reference at all. A draft with 135
     contigs -- which is what the pipeline picked for cluster_0 -- is unusable
     even though it is a perfectly good cluster representative for other
     purposes.
  2. The reference must be a member of (or very close to) its own cluster,
     which is the whole point.

So the representative used for the BACKBONE and the reference used for MAPPING
are different objects with different requirements, and conflating them is what
produced the 135-contig choice.

SELECTION LOGIC, and the distinction matters:
  * Completeness (<= --max-contigs) is a GATE, not a ranking. Gubbins cannot
    use a multi-contig reference at all, so this is pass/fail.
  * Among genomes that pass the gate, rank by CENTRALITY -- mean, then max,
    Mash distance to cluster members. Distance to members is what drives
    mismapping (measured at +630% SNPs / ~87% false calls against a distant
    reference) and callable fraction.
  * N50 and total length are NOT ranking criteria once the gate is passed. A
    longer reference simply adds positions other members cannot fill, raising
    missing data and risking --filter-percentage exclusions. "Most core SNPs"
    is likewise not a target: a reference does not carry SNPs, it determines
    where you are able to look.

A cluster is "reference-ready" if any member passes the completeness gate.

Stdlib only. Reads assembly FASTAs once to count contigs and compute N50.
"""

import argparse
import csv
import os
import sys
from collections import defaultdict

from cluster_diversity_bp import read_phylip


def contig_stats(path):
    """(n_contigs, n50, total_len) in one pass, sequences not retained."""
    lens = []
    cur = 0
    try:
        with open(path) as fh:
            for line in fh:
                if line.startswith(">"):
                    if cur:
                        lens.append(cur)
                    cur = 0
                else:
                    cur += len(line.strip())
        if cur:
            lens.append(cur)
    except OSError:
        return None
    if not lens:
        return None
    total = sum(lens)
    lens.sort(reverse=True)
    acc = 0
    n50 = lens[-1]
    for L in lens:
        acc += L
        if acc >= total / 2:
            n50 = L
            break
    return (len(lens), n50, total)


def load_blocklist(path):
    """
    Accession prefixes that must never be chosen as a mapping reference.

    Why a blocklist exists at all. Three references made Gubbins fail with
    RAxML "Unable to fit model to data" for every cluster mapped against them
    (GCF_003798365_1 alone for four of six failures, 0/4), while 23 other
    references gave 28/28 successes. Re-running all six with ONLY the reference
    changed recovered 12/12 replicon-units -- three of them against a reference
    MORE distant than the one they failed on. So the effect is real, is a
    property of the reference, and is invisible to every quality metric tested
    (fastANI, contiguity, N50, ambiguous bases, GC, duplication, misassemblies).
    The mechanism is not yet known, which is exactly why the rule is an explicit
    empirical blocklist rather than a quality threshold that would not catch it.

    Matching is by accession prefix, because the collection's filenames carry a
    location suffix (GCF_003798365_1_Thailand_Ubon_Ratchathani) that the
    accession alone does not.
    """
    out = []
    with open(path) as fh:
        for line in fh:
            line = line.split("#", 1)[0].strip()
            if line:
                out.append(line)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--membership", required=True)
    ap.add_argument("--fasta-dir", required=True)
    ap.add_argument("--id-col", default="sample_id")
    ap.add_argument("--cluster-col", default="cluster_id")
    ap.add_argument("--max-contigs", type=int, default=2,
                    help="a reference with more contigs than this is not "
                         "usable by Gubbins (default: %(default)s)")
    ap.add_argument("--min-size", type=int, default=2,
                    help="ignore clusters smaller than this")
    ap.add_argument("--phylip", default=None,
                    help="Mash distance matrix, used to find a borrowable "
                         "complete genome for clusters that lack one")
    ap.add_argument("--blocklist", default=None,
                    help="file of accession prefixes never to use as a mapping "
                         "reference, one per line, '#' comments allowed")
    ap.add_argument("--out", default="cluster_references.tsv")
    a = ap.parse_args()

    blocked = load_blocklist(a.blocklist) if a.blocklist else []

    def is_blocked(sid):
        return any(sid.startswith(p) for p in blocked)

    if blocked:
        print("reference blocklist: %d accession prefixes -- %s\n"
              % (len(blocked), ", ".join(blocked)))

    with open(a.membership, newline="") as fh:
        head = fh.readline()
        fh.seek(0)
        d = "\t" if "\t" in head else ","
        mem = list(csv.DictReader(fh, delimiter=d))
    clusters = defaultdict(list)
    for r in mem:
        cid = (r.get(a.cluster_col) or "").strip()
        sid = (r.get(a.id_col) or "").strip()
        if cid and sid:
            clusters[cid].append(sid)

    listing = {}
    for fn in os.listdir(a.fasta_dir):
        if fn.endswith((".fasta", ".fa", ".fna")):
            listing[fn.rsplit(".", 1)[0]] = os.path.join(a.fasta_dir, fn)

    # ---- centrality machinery (needs the Mash matrix) ---------------------
    cent = None
    _names = _rows_d = _idx = None
    if a.phylip:
        _names, _rows_d, _idx = read_phylip(a.phylip)

        def _d(i, j):
            if i == j:
                return 0.0
            if j < len(_rows_d[i]):
                return _rows_d[i][j]
            if i < len(_rows_d[j]):
                return _rows_d[j][i]
            return None

        def cent(cid, cand):
            """(mean, max) Mash distance from cand to all members of cid."""
            if cand not in _idx:
                return None
            ds = []
            for m in clusters[cid]:
                if m in _idx:
                    v = _d(_idx[cand], _idx[m])
                    if v is not None:
                        ds.append(v)
            if not ds:
                return None
            return (sum(ds) / len(ds), max(ds))

    cache = {}

    def stats(sid):
        if sid in cache:
            return cache[sid]
        p = listing.get(sid)
        if p is None:
            for stem, q in listing.items():
                if stem.startswith(sid):
                    p = q
                    break
        v = contig_stats(p) if p else None
        cache[sid] = (v, p)
        return cache[sid]

    rows = []
    for cid, sids in sorted(clusters.items()):
        if len(sids) < a.min_size:
            continue
        scored = []
        for s in sids:
            if is_blocked(s):
                continue
            v, p = stats(s)
            if v:
                scored.append((v[0], -v[1], -v[2], s, p))
        if not scored:
            rows.append((cid, len(sids), None, None, None, None, "NO_FASTA", None, None))
            continue
        n_complete = sum(1 for t in scored if t[0] <= a.max_contigs)
        complete_here = [t for t in scored if t[0] <= a.max_contigs]

        if complete_here and cent is not None:
            # Among COMPLETE members, rank by CENTRALITY, not by N50 or length.
            # Completeness is a gate (Gubbins cannot use a multi-contig
            # reference); centrality is the criterion, because distance to
            # members drives both mismapping and callable fraction. N50 and
            # total length are irrelevant once the gate is passed -- a longer
            # reference merely adds positions other members cannot fill.
            ranked = []
            for nc_, negn50_, negtot_, sid_, path_ in complete_here:
                c = cent(cid, sid_)
                if c is not None:
                    ranked.append((c[0], c[1], nc_, -negn50_, sid_))
            if ranked:
                ranked.sort()          # mean distance, then max distance
                mean_d, max_d, nc, n50, sid = ranked[0]
                rows.append((cid, len(sids), sid, nc, n50, n_complete,
                             "ready", mean_d, max_d))
                continue

        scored.sort()
        nc, negn50, negtot, sid, path = scored[0]
        status = "ready" if nc <= a.max_contigs else "NO_COMPLETE_MEMBER"
        rows.append((cid, len(sids), sid, nc, -negn50, n_complete, status,
                     None, None))

    ready = [r for r in rows if r[6] == "ready"]
    notready = [r for r in rows if r[6] == "NO_COMPLETE_MEMBER"]

    print("=" * 74)
    print("PER-CLUSTER REFERENCE AVAILABILITY  (<= %d contigs required)"
          % a.max_contigs)
    print("=" * 74)
    print("clusters considered (n >= %d)   : %d" % (a.min_size, len(rows)))
    print("reference-ready                 : %d  (%.1f%%)"
          % (len(ready), 100.0 * len(ready) / max(len(rows), 1)))
    print("no complete member              : %d" % len(notready))
    gr = sum(r[1] for r in ready)
    gn = sum(r[1] for r in notready)
    print("genomes in ready clusters       : %d" % gr)
    print("genomes in not-ready clusters   : %d" % gn)

    # ---- can not-ready clusters BORROW a complete genome? ------------------
    # Building an ABACAS pseudo-reference per cluster is real work. Before
    # committing to it, check whether a complete genome elsewhere in the
    # collection is close enough to serve. Uses the existing Mash matrix.
    borrowed = {}
    if a.phylip and notready:
        names, rows_d, idx = read_phylip(a.phylip)

        def dist(i, j):
            if i == j:
                return 0.0
            if j < len(rows_d[i]):
                return rows_d[i][j]
            if i < len(rows_d[j]):
                return rows_d[j][i]
            return None

        # The blocklist has to apply here too, not only to internal picks: four
        # of the six known failures were clusters that BORROWED a blocked
        # reference, so filtering only the internal path would leave the main
        # route to a bad reference wide open.
        complete = [s for s in cache
                    if cache[s][0] and cache[s][0][0] <= a.max_contigs
                    and not is_blocked(s)]
        for cid, n, sid, nc, n50, ncomp, st, md, xd in notready:
            members = [m for m in clusters[cid] if m in idx]
            if not members:
                continue
            best, bestd = None, None
            for cand in complete:
                if cand not in idx:
                    continue
                ds = [dist(idx[cand], idx[m]) for m in members]
                ds = [x for x in ds if x is not None]
                if not ds:
                    continue
                md = sum(ds) / len(ds)
                if bestd is None or md < bestd:
                    best, bestd = cand, md
            if best:
                borrowed[cid] = (best, bestd)

    # Write the borrow assignment to a companion TSV. Printing only the top 10
    # meant the other 23 were invisible to anything downstream, and a pipeline
    # cannot consume stdout.
    if borrowed:
        bpath = (a.out or "cluster_references.tsv").replace(".tsv", "") + ".borrowed.tsv"
        with open(bpath, "w") as bh:
            bh.write("cluster_id\tborrowed_reference\tmean_mash\n")
            for cid, (b, d) in sorted(borrowed.items(), key=lambda kv: kv[1][1]):
                bh.write("%s\t%s\t%.5f\n" % (cid, b, d))
        print("\nWrote %s (%d borrow assignments)" % (bpath, len(borrowed)))

    if borrowed:
        print("\nNearest COMPLETE genome available to borrow, per not-ready "
              "cluster:")
        print("  %-14s %-34s %10s" % ("cluster", "borrowable reference",
                                      "mean_mash"))
        vals = sorted(borrowed.items(), key=lambda kv: kv[1][1])
        for cid, (b, d) in vals[:10]:
            print("  %-14s %-34s %10.5f" % (cid, b[:34], d))
        ds = [d for _, (_, d) in borrowed.items()]
        near = sum(1 for d in ds if d <= 0.005)
        print("  ... %d clusters total; %d have a complete genome within "
              "Mash 0.005" % (len(borrowed), near))
        print("  (0.005 is SKA2's strain boundary and a reasonable proxy for")
        print("   'close enough to map against without the A.3c effect')")

    if notready:
        print("\nClusters with NO complete member (best available shown):")
        print("  %-14s %5s %-34s %8s" % ("cluster", "n", "best member", "contigs"))
        for cid, n, sid, nc, n50, ncomp, st, md, xd in sorted(
                notready, key=lambda r: -r[1])[:15]:
            print("  %-14s %5d %-34s %8s" % (cid, n, (sid or "-")[:34], nc))
        print("\n  For these, a lineage-specific pseudo-reference must be")
        print("  BUILT by ordering the best draft against a complete genome")
        print("  (ABACAS, as Chewapreecha and Seng both did), or the cluster")
        print("  must borrow the nearest complete genome from outside itself.")

    with open(a.out, "w") as fh:
        fh.write("cluster_id\tn\treference\tref_contigs\tref_n50\t"
                 "n_complete_members\tstatus\tref_mean_mash\tref_max_mash\n")
        for cid, n, sid, nc, n50, ncomp, st, md, xd in rows:
            fh.write("%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"
                     % (cid, n, sid or "", nc if nc is not None else "",
                        n50 if n50 is not None else "",
                        ncomp if ncomp is not None else "", st,
                        "" if md is None else "%.6f" % md,
                        "" if xd is None else "%.6f" % xd))
    print("\nWrote %s" % a.out)


if __name__ == "__main__":
    sys.exit(main())
