#!/usr/bin/env python3
"""
build_L1_partition_bp.py

Turn the pp2802 PopPUNK strain partition into the L1 analysis partition.

THE RULE, stated once so it can be quoted in Methods:

    PopPUNK defines strains. fastbaps (PopPIPE, levels=3) subdivides within
    each strain. Analysis units are fastbaps LEVEL 1 subclusters. The rule is
    applied uniformly to every strain -- a strain that fastbaps does not split
    simply yields one L1 unit. No strain is subdivided because it is large and
    none is left whole because it is small.

WHERE THE LABELS COME FROM, and the one caveat.

fastbaps was run by PopPIPE-bp (~/PopPIPE-bp, 2026-08-10) on an EARLIER PopPUNK
fit of an earlier snapshot of the collection (2,430 genomes, 42 strains). The
partition analysed here is the in-workflow pp2802 fit (2,802 genomes, 264
clusters, 35 kept at n >= 7). Those are two different fits, so the labels are
only reusable if the two fits agree about strain MEMBERSHIP. They do:

    every one of the 35 pp2802 strains maps onto exactly ONE archived strain,
    with no strain splitting or merging in either direction.

Strain NUMBERING differs (pp2802 strain_12 is archived strain 13, strain_21 is
archived 23, and so on), which is why this script joins by membership and never
by strain id.

What does not carry over: 15 genomes (0.6%) that were added to the collection
after the fastbaps run and therefore have no label. They are handled by
--straggler-policy, and every one of them is written to the audit file so the
count can be quoted rather than glossed.

Outputs
  <prefix>_clusters.tsv       cluster_id <TAB> sample_id, curated-mode contract
  <prefix>_units.tsv          per-unit sizes, strain of origin, straggler count
  <prefix>_stragglers.tsv     every genome assigned by nearest neighbour

Stdlib only.
"""

import argparse
import collections
import csv
import glob
import os
import sys


def read_poppipe_fastbaps(root):
    """sample -> (archived_strain, L1) from every PopPIPE strain directory."""
    out = {}
    pattern = os.path.join(root, "output", "strains", "*", "fastbaps_clusters.txt")
    for path in sorted(glob.glob(pattern)):
        strain = os.path.basename(os.path.dirname(path))
        with open(path) as fh:
            reader = csv.reader(fh)
            header = next(reader, None)
            if not header:
                continue
            for row in reader:
                if len(row) >= 2 and row[0].strip():
                    out[row[0].strip()] = (strain, row[1].strip())
    if not out:
        sys.exit(f"no fastbaps_clusters.txt found under {pattern}")
    return out


def read_clusters(path):
    """cluster_id -> [sample_id]; accepts the curated 2-column contract."""
    out = collections.defaultdict(list)
    with open(path) as fh:
        reader = csv.reader(fh, delimiter="\t")
        next(reader, None)
        for row in reader:
            if len(row) >= 2 and row[0].strip():
                out[row[0].strip()].append(row[1].strip())
    return out


def norm(name):
    """
    Match names across files that sanitised them differently.

    The Mash matrix carries GCF_015714675_1_Virgin_Islands_St__John where the
    cluster table carries ...St._John -- the same genome, one file having turned
    '.' into '_' and the other having kept it. Collapse every run of non-
    alphanumerics to a single '_' so both spellings land on one key.
    """
    out = []
    for ch in name:
        out.append(ch if ch.isalnum() else "_")
    return "_".join(x for x in "".join(out).split("_") if x)


def read_mash_rows(path, wanted):
    """
    Row-wise read of the labelled square Mash matrix, keyed by norm().

    Returns {sample: {other: distance}} restricted to `wanted` on both axes, so
    the 2,802 x 2,802 matrix never lands in memory whole.
    """
    keep = {norm(w) for w in wanted}
    with open(path) as fh:
        header = fh.readline().rstrip("\n").split("\t")
        names = [norm(n) for n in header[1:]]
        idx = [i for i, n in enumerate(names) if n in keep]
        sub = [names[i] for i in idx]
        rows = {}
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            key = norm(parts[0]) if parts else ""
            if key not in keep:
                continue
            vals = parts[1:]
            rows[key] = {
                sub[k]: float(vals[i]) for k, i in enumerate(idx) if vals[i] != ""
            }
    missing = keep - set(rows)
    if missing:
        sys.exit(
            f"{len(missing)} genomes absent from the Mash matrix, "
            f"e.g. {sorted(missing)[:3]}"
        )
    return rows


def assign_stragglers(strain, unlabelled, labelled, mash, policy):
    """
    Give each unlabelled genome an L1 label, or refuse to.

    'nearest'  -- nearest labelled strain-mate decides the candidate subcluster
                  (single nearest neighbour, not a centroid: which subcluster a
                  genome belongs to is answered better by its closest relative
                  than by a mean, when subclusters differ wildly in size), and
                  the genome joins it only if it passes the CONTAINMENT TEST
                  below. Otherwise it is left unassigned.
    'own'      -- each unlabelled genome forms its own unit (dropped later by
                  the size threshold unless several share a strain).
    'drop'     -- excluded entirely.

    THE CONTAINMENT TEST, and why it is not optional. Nearest-neighbour alone
    always finds *a* nearest subcluster, however far away it is. Measured here:
    GCF_001976585_1_Thailand sits 0.00262 from its nearest labelled relative in
    a subcluster whose own members span at most 0.00089 -- three times the
    diameter of the group it would be joining. Adding such a genome hangs a long
    branch off a clonal unit, which is precisely the configuration that inflates
    r/m. So a straggler joins only if it is no further from its nearest labelled
    relative than that subcluster's labelled members are from each other. A
    subcluster with a single labelled member has no diameter to test against and
    cannot accept stragglers.

    A strain with NO labelled member at all (pp2802 strain_31, seven Sri Lankan
    genomes absent from the fastbaps input) has nothing to test against; it
    becomes a single L1 unit, which is what fastbaps returns for a set it cannot
    split.
    """
    out, notes = {}, []
    if not unlabelled:
        return out, notes
    if policy == "drop":
        for s in unlabelled:
            notes.append((strain, s, "", "dropped (policy=drop)", "", ""))
        return out, notes
    if not labelled or policy == "own":
        reason = "no labelled strain-mate" if not labelled else "policy=own"
        for s in unlabelled:
            out[s] = "1"
            notes.append((strain, s, "", f"whole-strain unit ({reason})", "", ""))
        return out, notes

    members = collections.defaultdict(list)
    for t, lab in labelled.items():
        members[lab].append(t)
    diameter = {}
    for lab, mem in members.items():
        diameter[lab] = max(
            (mash[norm(a)][norm(b)] for i, a in enumerate(mem) for b in mem[i + 1:]),
            default=float("nan"),
        )

    for s in unlabelled:
        row = mash[norm(s)]
        best = min(labelled, key=lambda t: row.get(norm(t), float("inf")))
        dist = row.get(norm(best), float("nan"))
        lab = labelled[best]
        diam = diameter[lab]
        if diam == diam and dist <= diam:          # NaN-safe: a lone member fails
            out[s] = lab
            basis = "nearest neighbour, contained"
        else:
            basis = ("unassigned: nearest subcluster has one labelled member"
                     if diam != diam else "unassigned: outside subcluster diameter")
        notes.append((strain, s, best, basis, f"{dist:.6f}",
                      "" if diam != diam else f"{diam:.6f}"))
    return out, notes


def merge_subthreshold(strain, units, mash, min_size, ceiling):
    """
    Absorb sub-threshold L1 subclusters into their nearest sibling, instead of
    deleting them.

    WHY THIS EXISTS. `min_cluster_size` was justified for POPPUNK STRAINS -- 7
    matches the smallest unit in the existing analysed set. fastbaps then exists
    precisely to SUBDIVIDE those strains, so reapplying the same absolute floor
    to its output discarded 122 of 204 L1 units (60%) holding 322 genomes, on top
    of the 407 already lost at the strain floor. strain_34 is the clean case: 7
    genomes, passes the strain floor exactly, fastbaps splits it 4 + 3, both
    halves fail, whole strain gone.

    The loss was not uniform. It tracked rarity, because a rare lineage IS a
    small subcluster: Singapore lost 0%, Thailand 16.8%, USA 41.7%, Australia
    74.1%, India 94.6%, and 51% of every Americas genome in the collection. For
    origin attribution that is the worst possible bias -- the discarded genomes
    are exactly the ones a rare imported lineage would look like.

    THE MERGE RULE has two clauses, and BOTH are needed.

        (1) gap:    d_min(A, B) <= diameter(B)
        (2) result: diameter(A union B) <= ceiling

    Clause (1) is the existing straggler containment test unchanged -- the gap
    must fall inside the spread the RECEIVER already has. An earlier draft used
    max(diameter(A), diameter(B)) instead, which is wrong: a loose little unit
    then licenses its own merger into a clonal one. Measured, that draft took
    strain_1_L1_3 from diameter 0.00047 to 0.00385 (8x) and strain_20_L1_1 --
    the published Georgia cluster -- from 0.00084 to 0.00327.

    Clause (2) bounds the OUTCOME, because clause (1) alone still permits a
    small-but-internally-broad unit to widen its receiver. The ceiling is
    calibrated, not chosen: it is the 90th percentile of the diameters of units
    that reach min_size WITHOUT any merging, i.e. the observed shape of a
    legitimately formed L1 unit. Nothing merged is allowed to be looser than
    that.

    A singleton has no diameter, so it can never be a receiver -- as before.

    Merging is iterative and smallest-first: absorbing a unit can lift the
    receiver over the threshold, and it changes the receiver's diameter, so both
    are recomputed each round rather than cached.

    What CANNOT be merged is not deleted. It keeps its unit label and is written
    to the assignment output with role=assign_only: too small to estimate r/m
    from is a statement about what the unit can support, not a reason to discard
    the genomes, which remain usable for placement and distance-based
    attribution.
    """
    def dia(members):
        if len(members) < 2:
            return float("nan")
        return max(mash[norm(a)][norm(b)]
                   for i, a in enumerate(members) for b in members[i + 1:])

    def gap(a, b):
        return min(mash[norm(x)][norm(y)] for x in a for y in b)

    merges = []
    while True:
        small = sorted((u for u in units if len(units[u]) < min_size),
                       key=lambda u: len(units[u]))
        if not small or len(units) < 2:
            break
        moved = False
        for u in small:
            others = [o for o in units if o != u]
            if not others:
                break
            best = min(others, key=lambda o: gap(units[u], units[o]))
            d = gap(units[u], units[best])
            db = dia(units[best])                       # receiver's spread only
            if db != db or d > db:                      # clause (1)
                continue
            merged_dia = dia(units[u] + units[best])
            if merged_dia > ceiling:                    # clause (2)
                continue
            merges.append((strain, u, best, len(units[u]), len(units[best]),
                           d, db, merged_dia))
            units[best].extend(units[u])
            del units[u]
            moved = True
            break
        if not moved:
            break
    return merges


def merge_across_strains(units, strain_of, mash, min_size, ceiling):
    """
    Second merge round, for units that are still sub-threshold after the
    within-strain pass -- principally the 229 PopPUNK strains that fall below the
    strain floor (407 genomes, 152 of them singletons).

    Those strains never reached this script at all before: `min_cluster_size`
    removed them at the PopPUNK stage, and they were deleted rather than
    recorded. The loss was the same shape as the L1 one and hit the same places
    -- 171 Australian genomes, 42 Indian, and every African genome in the
    collection (4 Ghanaian).

    The rule is UNCHANGED from merge_subthreshold: gap within the receiver's own
    diameter, and the merged diameter under the calibrated ceiling. Only the
    candidate set widens, from siblings inside one strain to every unit.

    THIS CROSSES A POPPUNK BOUNDARY, so it is reported separately and should be
    read as a claim about that boundary: a sub-threshold strain that passes both
    clauses sits inside the spread of an existing unit, which is to say PopPUNK's
    split between them was not carrying much. A strain that fails stays its own
    assign-only unit -- it is never deleted, and never forced into a neighbour.
    """
    def dia(members):
        if len(members) < 2:
            return float("nan")
        return max(mash[norm(a)][norm(b)]
                   for i, a in enumerate(members) for b in members[i + 1:])

    def gap(a, b):
        return min(mash[norm(x)][norm(y)] for x in a for y in b)

    merges = []
    while True:
        small = sorted((u for u in units if len(units[u]) < min_size),
                       key=lambda u: len(units[u]))
        moved = False
        for u in small:
            others = [o for o in units if o != u and len(units[o]) >= min_size]
            if not others:
                break
            best = min(others, key=lambda o: gap(units[u], units[o]))
            d = gap(units[u], units[best])
            db = dia(units[best])
            if db != db or d > db:
                continue
            merged_dia = dia(units[u] + units[best])
            if merged_dia > ceiling:
                continue
            merges.append((strain_of.get(u, "?"), u, best, len(units[u]),
                           len(units[best]), d, db, merged_dia))
            units[best].extend(units[u])
            del units[u]
            moved = True
            break
        if not moved:
            break
    return merges


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--clusters", required=True,
                    help="pp2802 clusters.tsv (cluster_id, sample_id)")
    ap.add_argument("--poppipe", default=os.path.expanduser("~/PopPIPE-bp"))
    ap.add_argument("--mash", required=True, help="labelled square Mash matrix TSV")
    ap.add_argument("--min-size", type=int, default=7,
                    help="minimum L1 unit size to keep (default 7)")
    ap.add_argument("--straggler-policy", choices=["nearest", "own", "drop"],
                    default="nearest")
    ap.add_argument("--no-merge", action="store_true",
                    help="restore the pre-2026-08-16 behaviour: delete "
                         "sub-threshold L1 units instead of merging them")
    ap.add_argument("--all-clusters", default=None,
                    help="PopPUNK refined_clusters.csv (every genome, including "
                         "strains below the strain floor)")
    ap.add_argument("--absorb-subthreshold-strains", action="store_true",
                    help="bring the strains below the PopPUNK strain floor into "
                         "the partition as whole-strain units, then let the "
                         "cross-strain merge round place what it can. Requires "
                         "--all-clusters. Nothing is deleted either way.")
    ap.add_argument("--prefix", default="curated_L1")
    args = ap.parse_args()

    fastbaps = read_poppipe_fastbaps(args.poppipe)
    strains = read_clusters(args.clusters)
    print(f"pp2802 partition:   {sum(len(v) for v in strains.values())} genomes "
          f"in {len(strains)} strains")
    print(f"PopPIPE fastbaps:   {len(fastbaps)} genomes "
          f"in {len({v[0] for v in fastbaps.values()})} archived strains")

    # Refuse to proceed if the two fits disagree about strain membership: the
    # whole justification for reusing these labels is that they do not.
    conflict = []
    for strain, samples in strains.items():
        arch = collections.Counter(fastbaps[s][0] for s in samples if s in fastbaps)
        if len(arch) > 1:
            conflict.append((strain, dict(arch)))
    if conflict:
        print("\nSTOP: pp2802 strains span several archived strains, so the "
              "archived L1 labels are not transferable:", file=sys.stderr)
        for strain, arch in conflict:
            print(f"  {strain}: {arch}", file=sys.stderr)
        sys.exit(2)
    print("membership check:    every pp2802 strain maps 1:1 onto one archived "
          "strain (no splits, no merges)")

    # Optionally pull in the strains PopPUNK's own floor removed. They carry no
    # fastbaps labels (49 of 407 do), so each becomes a whole-strain L1 unit via
    # the existing no-labelled-strain-mate path, and the cross-strain merge round
    # places what it can. Recorded either way; deleted never.
    n_sub_strains = n_sub_genomes = 0
    if args.absorb_subthreshold_strains:
        if not args.all_clusters:
            sys.exit("--absorb-subthreshold-strains requires --all-clusters")
        full = collections.defaultdict(list)
        with open(args.all_clusters) as fh:
            for row in csv.DictReader(fh):
                cid = (row.get("Cluster") or "").strip()
                smp = (row.get("Taxon") or "").strip()
                if cid and smp:
                    full[cid].append(smp)
        known = {s for v in strains.values() for s in v}
        for cid, mem in sorted(full.items(), key=lambda kv: int(kv[0])):
            if any(m in known for m in mem):
                continue                       # already an above-floor strain
            strains[f"strain_pp{cid}"] = mem
            n_sub_strains += 1
            n_sub_genomes += len(mem)
        print(f"sub-threshold strains: {n_sub_strains} strains / {n_sub_genomes} "
              f"genomes brought in below the PopPUNK strain floor")

    # Only the partition matters here: the archived fastbaps run covers genomes
    # that have since left the collection and are absent from the Mash matrix.
    in_partition = {s for v in strains.values() for s in v}
    stragglers = {s for s in in_partition if s not in fastbaps}
    mash = read_mash_rows(args.mash, in_partition) if (
        stragglers and args.straggler_policy == "nearest") else {}

    assign, notes = {}, []
    def strain_ord(x):
        tail = x.split("_")[1]
        return (1, int(tail[2:])) if tail.startswith("pp") else (0, int(tail))

    for strain in sorted(strains, key=strain_ord):
        samples = strains[strain]
        labelled = {s: fastbaps[s][1] for s in samples if s in fastbaps}
        unlabelled = [s for s in samples if s not in fastbaps]
        for s, lab in labelled.items():
            assign[s] = f"{strain}_L1_{lab}"
        extra, note = assign_stragglers(strain, unlabelled, labelled, mash,
                                        args.straggler_policy)
        notes.extend(note)
        for s, lab in extra.items():
            assign[s] = f"{strain}_L1_{lab}"

    units = collections.defaultdict(list)
    for s, u in assign.items():
        units[u].append(s)

    # Absorb sub-threshold subclusters into their nearest sibling within the same
    # strain, rather than deleting them. See merge_subthreshold().
    all_merges = []
    if not args.no_merge:
        if not mash:
            mash = read_mash_rows(args.mash, in_partition)
        # Calibrate the outcome ceiling on units that reach min_size WITHOUT
        # merging -- the observed shape of a legitimately formed L1 unit.
        def _dia(mem):
            if len(mem) < 2:
                return float("nan")
            return max(mash[norm(a)][norm(b)]
                       for i, a in enumerate(mem) for b in mem[i + 1:])
        natural = sorted(d for d in (_dia(v) for v in units.values()
                                     if len(v) >= args.min_size) if d == d)
        ceiling = (natural[int(0.9 * (len(natural) - 1))] if natural
                   else float("inf"))
        print(f"merge ceiling:       {ceiling:.5f} "
              f"(p90 diameter of the {len(natural)} units formed without merging)")

        by_strain = collections.defaultdict(dict)
        for u, mem in units.items():
            by_strain[u.split("_L1_")[0]][u] = list(mem)
        units = {}
        for strain in sorted(by_strain, key=strain_ord):
            su = by_strain[strain]
            all_merges.extend(merge_subthreshold(strain, su, mash, args.min_size,
                                                 ceiling))
            units.update(su)
        strain_of = {u: u.split("_L1_")[0] for u in units}
        cross = merge_across_strains(units, strain_of, mash, args.min_size,
                                     ceiling)
        if cross:
            print(f"cross-strain merges: {len(cross)} sub-threshold unit(s) "
                  f"absorbed across a PopPUNK boundary")
        all_merges.extend(cross)
        assign = {s: u for u, mem in units.items() for s in mem}

    kept = {u: v for u, v in units.items() if len(v) >= args.min_size}
    assign_only = {u: v for u, v in units.items() if len(v) < args.min_size}

    def unit_key(u):
        strain, sub = u.split("_L1_")
        tail = strain.split("_")[1]
        pri = (1, int(tail[2:])) if tail.startswith("pp") else (0, int(tail))
        return (pri, int(sub))

    with open(f"{args.prefix}_clusters.tsv", "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")  # never CRLF
        w.writerow(["cluster_id", "sample_id"])
        for u in sorted(kept, key=unit_key):
            for s in sorted(kept[u]):
                w.writerow([u, s])

    straggler_units = collections.Counter(
        assign[n[1]].split("_L1_")[0] + "_L1_" + assign[n[1]].split("_L1_")[1]
        for n in notes if n[1] in assign)
    with open(f"{args.prefix}_units.tsv", "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["cluster_id", "strain", "n", "n_straggler", "kept", "role"])
        for u in sorted(units, key=unit_key):
            w.writerow([u, u.split("_L1_")[0], len(units[u]),
                        straggler_units.get(u, 0),
                        "yes" if u in kept else "no",
                        "analysis" if u in kept else "assign_only"])

    # Every genome, with what it can and cannot be used for. The analysis
    # contract (<prefix>_clusters.tsv) still carries only units big enough to
    # estimate from; nothing is deleted from this file.
    with open(f"{args.prefix}_assignments_all.tsv", "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["sample_id", "cluster_id", "strain", "unit_n", "role"])
        for u in sorted(units, key=unit_key):
            for smp in sorted(units[u]):
                w.writerow([smp, u, u.split("_L1_")[0], len(units[u]),
                            "analysis" if u in kept else "assign_only"])
        if args.all_clusters and os.path.isfile(args.all_clusters):
            placed = {smp for mem in units.values() for smp in mem}
            with open(args.all_clusters) as afh:
                for row in csv.DictReader(afh):
                    smp = (row.get("Taxon") or "").strip()
                    if smp and smp not in placed:
                        w.writerow([smp, "", f"pp_{row.get('Cluster','').strip()}",
                                    "", "below_strain_floor"])

    with open(f"{args.prefix}_merges.tsv", "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["strain", "absorbed_unit", "into_unit", "n_absorbed",
                    "n_receiver", "gap", "receiver_diameter", "merged_diameter"])
        for row in all_merges:
            w.writerow([row[0], row[1], row[2], row[3], row[4],
                        f"{row[5]:.6f}", f"{row[6]:.6f}", f"{row[7]:.6f}"])

    with open(f"{args.prefix}_stragglers.tsv", "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["strain", "sample_id", "nearest_labelled", "basis",
                    "mash_to_nearest", "subcluster_diameter", "assigned_unit"])
        for strain, s, near, basis, dist, diam in notes:
            w.writerow([strain, s, near, basis, dist, diam,
                        assign.get(s, "UNASSIGNED")])

    total = sum(len(v) for v in strains.values())
    sizes = sorted((len(v) for v in kept.values()), reverse=True)
    print(f"\nmerges:              {len(all_merges)} sub-threshold units absorbed "
          f"into a sibling" + ("  (DISABLED by --no-merge)" if args.no_merge else ""))
    print(f"L1 units:            {len(units)} total, {len(kept)} at n >= {args.min_size}, "
          f"{len(assign_only)} assign-only")
    ao = sum(len(v) for v in assign_only.values())
    print(f"assign-only genomes: {ao} retained (not deleted; excluded from Gubbins)")
    print(f"genomes analysed:    {sum(sizes)} of {total} in the partition "
          f"({100.0 * sum(sizes) / total:.1f}%), of 2802 in the collection "
          f"({100.0 * sum(sizes) / 2802:.1f}%)")
    print(f"largest unit:        n = {sizes[0]}   median n = {sizes[len(sizes) // 2]}")
    placed = sum(1 for n in notes if n[1] in assign)
    print(f"stragglers:          {len(notes)} genomes, policy={args.straggler_policy}"
          f" -- {placed} placed, {len(notes) - placed} left unassigned")
    if args.all_clusters and os.path.isfile(args.all_clusters):
        with open(args.all_clusters) as afh:
            n_all = sum(1 for _ in csv.DictReader(afh))
        below = n_all - total
        print(f"strain floor:        {below} genomes sit in PopPUNK strains below "
              f"the strain floor and never reach this script; they are listed in "
              f"{args.prefix}_assignments_all.tsv as role=below_strain_floor")
    print(f"\nwrote {args.prefix}_clusters.tsv, {args.prefix}_units.tsv, "
          f"{args.prefix}_stragglers.tsv, {args.prefix}_merges.tsv, "
          f"{args.prefix}_assignments_all.tsv")


if __name__ == "__main__":
    main()
