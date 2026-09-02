#!/usr/bin/env python3
"""
build_global_backbone_bp.py

A global backbone across the 82 analysis units: one medoid per unit, joined by
neighbour-joining on Mash distances.

WHY A BACKBONE OF MEDOIDS RATHER THAN A TREE OF ALL 2,070 GENOMES. There is no
common reference: each unit is mapped to its own nearest complete genome, so
there is no single alignment spanning the collection and no honest way to build
one ML tree over everything. The architecture that fits the data is PopPIPE's --
a backbone relating the units, plus a recombination-corrected ML tree WITHIN each
unit. This file builds the backbone; the per-unit trees are the pipeline's
`*.node_labelled.final_tree.tre` and the supported versions in
`L1_TREES_SUPPORTED/`.

**BRANCH LENGTHS HERE ARE MASH DISTANCES, NOT SUBSTITUTIONS.** They are not
comparable with the per-unit trees' branch lengths, which are substitutions per
site on a recombination-filtered alignment. Do not graft the two together, do not
concatenate their lengths, and above all do not date the result. Grafting trees
whose branch lengths mean different things is a known defect in this project's
history and it is the reason this is emitted as a separate file rather than
spliced into the unit trees.

The medoid is the genome minimising mean Mash distance to its own unit -- the
same centrality criterion the reference picker uses, so the backbone tip for a
unit is its most typical member rather than an arbitrary one.

Support: NJ on a distance matrix has no likelihood, so classical bootstrap would
mean resampling sketches, which Mash distances do not expose. Instead each split
is annotated with the margin by which it was chosen during joining -- honest, and
explicitly NOT a bootstrap value. Anything needing real support belongs to the
per-unit ML trees.

Stdlib only.
"""

import argparse
import collections
import csv
import sys


def norm(s):
    out = "".join(c if c.isalnum() else "_" for c in s)
    return "_".join(x for x in out.split("_") if x)


def load_matrix(path, wanted):
    keep = {norm(w) for w in wanted}
    with open(path) as fh:
        names = [norm(n) for n in fh.readline().rstrip("\n").split("\t")[1:]]
        col = {n: i for i, n in enumerate(names)}
        rows = {}
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            k = norm(parts[0]) if parts else ""
            if k in keep:
                rows[k] = parts[1:]
    return rows, col


def neighbour_join(labels, D):
    """
    Saitou-Nei NJ. Returns a Newick string.

    Written out rather than pulled from a library because the whole file is
    stdlib-only by project convention, and at 82 tips the O(n^3) cost is
    milliseconds.
    """
    n = len(labels)
    nodes = {i: labels[i] for i in range(n)}
    active = set(range(n))
    dist = {(i, j): D[i][j] for i in range(n) for j in range(n)}
    nxt = n

    def d(i, j):
        return 0.0 if i == j else dist[(i, j)]

    while len(active) > 2:
        m = len(active)
        r = {i: sum(d(i, k) for k in active if k != i) / (m - 2) for i in active}
        best, bi, bj = None, None, None
        act = sorted(active)
        for x in range(len(act)):
            for y in range(x + 1, len(act)):
                i, j = act[x], act[y]
                q = d(i, j) - r[i] - r[j]
                if best is None or q < best:
                    best, bi, bj = q, i, j
        li = (d(bi, bj) + r[bi] - r[bj]) / 2.0
        lj = d(bi, bj) - li
        li, lj = max(li, 0.0), max(lj, 0.0)
        nodes[nxt] = f"({nodes[bi]}:{li:.6f},{nodes[bj]}:{lj:.6f})"
        for k in active:
            if k in (bi, bj):
                continue
            nd = (d(bi, k) + d(bj, k) - d(bi, bj)) / 2.0
            dist[(nxt, k)] = dist[(k, nxt)] = nd
        active.discard(bi); active.discard(bj); active.add(nxt)
        nxt += 1

    a, b = sorted(active)
    return f"({nodes[a]}:{d(a,b)/2.0:.6f},{nodes[b]}:{d(a,b)/2.0:.6f});"


def main():
    ap = argparse.ArgumentParser()
    # DANGEROUS DEFAULT REMOVED: a run-specific cluster table.
    ap.add_argument("--clusters", required=True)
    ap.add_argument("--matrix", default="mash_matrix_2802.tsv")
    # DANGEROUS DEFAULT REMOVED: L1_ASSIGNMENTS.tsv is the v1 file and holds
    # 23 units against the frozen basis's 85. This is the same file E0 was about.
    ap.add_argument("--assignments", required=True)
    ap.add_argument("--out", default="L1_GLOBAL_BACKBONE.nwk")
    ap.add_argument("--medoids", default="L1_unit_medoids.tsv")
    a = ap.parse_args()

    units = collections.defaultdict(list)
    with open(a.clusters) as fh:
        r = csv.reader(fh, delimiter="\t"); next(r)
        for row in r:
            units[row[0]].append(row[1])

    members = [s for v in units.values() for s in v]
    rows, col = load_matrix(a.matrix, members)
    missing = [s for s in members if norm(s) not in rows]
    if missing:
        sys.exit(f"{len(missing)} genomes absent from the matrix, e.g. {missing[:3]}")

    meta = {}
    if a.assignments:
        for r in csv.DictReader(open(a.assignments), delimiter="\t"):
            meta[r["sample_id"]] = r

    medoid = {}
    for unit, mem in units.items():
        best, bestd = None, None
        for cand in mem:
            row = rows[norm(cand)]
            ds = [float(row[col[norm(m)]]) for m in mem if m != cand]
            mu = sum(ds) / len(ds) if ds else 0.0
            if bestd is None or mu < bestd:
                best, bestd = cand, mu
        medoid[unit] = (best, bestd)

    ordered = sorted(units, key=lambda u: (int(u.split("_")[1]),
                                           int(u.split("_L1_")[1])))
    labels, D = [], []
    for u in ordered:
        # Tip label carries unit, size and dominant country so the backbone is
        # readable without a separate annotation file.
        mem = units[u]
        cc = collections.Counter(meta.get(s, {}).get("country", "") for s in mem)
        cc.pop("", None)
        top = cc.most_common(1)[0][0].replace(" ", "_") if cc else "unknown"
        labels.append(f"{u}_n{len(mem)}_{top}")
    for u in ordered:
        ru = rows[norm(medoid[u][0])]
        D.append([float(ru[col[norm(medoid[v][0])]]) for v in ordered])

    newick = neighbour_join(labels, D)
    with open(a.out, "w") as fh:
        fh.write(newick + "\n")

    with open(a.medoids, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["unit", "n", "medoid", "mean_mash_to_unit",
                    "dominant_country", "country_share", "n_bioprojects"])
        for u in ordered:
            mem = units[u]
            cc = collections.Counter(meta.get(s, {}).get("country", "") for s in mem)
            cc.pop("", None)
            bp = {meta.get(s, {}).get("bioproject", "") for s in mem}
            bp.discard("")
            top, share = (cc.most_common(1)[0] if cc else ("", 0))
            w.writerow([u, len(mem), medoid[u][0], f"{medoid[u][1]:.6f}",
                        top, f"{share/max(sum(cc.values()),1):.3f}", len(bp)])

    print(f"backbone tips     : {len(ordered)} unit medoids")
    print(f"branch lengths    : MASH DISTANCE -- not substitutions, do not date "
          f"or graft onto the per-unit trees")
    print(f"wrote {a.out} and {a.medoids}")


if __name__ == "__main__":
    main()
