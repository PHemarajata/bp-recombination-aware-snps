#!/usr/bin/env python3
"""
test_phylogeography_bp.py

Self-test for phylogeography_association_bp.py, using synthetic trees and
metadata only. No isolate data is required or used, so this runs anywhere,
including in a checkout that (by design) contains no data at all.

It exists because the geographic result is the one most exposed to a silent
join between mismatched partitions, and because the single-country enrichment
test was previously described in the methods but implemented nowhere. Both are
now checked against hand-computed answers.

Run:  python3 test_phylogeography_bp.py
"""

import csv
import math
import os
import shutil
import subprocess
import sys
import tempfile

import phylogeography_association_bp as P

FAILED = []


def check(name, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {name}: got {got!r}, want {want!r}")
    if not ok:
        FAILED.append(name)


def check_close(name, got, want, tol=1e-9):
    ok = abs(got - want) <= tol
    print(f"  {'PASS' if ok else 'FAIL'}  {name}: got {got!r}, want {want!r}")
    if not ok:
        FAILED.append(name)


# ---------------------------------------------------------------------------
def test_fitch():
    """
    Hand-computable cases. Fitch counts the minimum number of state changes.
    """
    print("\nfitch_score")
    # ((A,A),(B,B)) : one change on the internal split.
    t = P.parse_newick("((a,b),(c,d));")
    check("perfectly sorted, 2 states", 
          P.fitch_score(t, {"a": "A", "b": "A", "c": "B", "d": "B"}), 1)
    # ((A,B),(A,B)) : maximally interleaved, needs two changes.
    check("interleaved, 2 states",
          P.fitch_score(t, {"a": "A", "b": "B", "c": "A", "d": "B"}), 2)
    # All one state: no changes.
    check("single state",
          P.fitch_score(t, {"a": "A", "b": "A", "c": "A", "d": "A"}), 0)
    # Unknown tips are fully ambiguous and must never force a change.
    check("unknown tip does not force a change",
          P.fitch_score(t, {"a": "A", "b": "A", "c": "A"}), 0)
    check("all unknown",
          P.fitch_score(t, {}), 0)
    # Deep caterpillar: the explicit stack must not blow up where recursion would.
    n = 20000
    nwk = "a0"
    for i in range(1, n):
        nwk = f"({nwk},a{i})"
    deep = P.parse_newick(nwk + ";")
    states = {f"a{i}": ("A" if i < n // 2 else "B") for i in range(n)}
    check(f"caterpillar depth {n} does not overflow",
          P.fitch_score(deep, states) >= 1, True)


def test_single_country_math():
    """
    P(all one country) and the Poisson-binomial tail, against hand arithmetic.
    """
    print("\nsingle-country null")
    # 10 genomes, 6 of country X and 4 of Y. Draw 3 without replacement.
    # P(all same) = [C(6,3) + C(4,3)] / C(10,3) = (20 + 4) / 120 = 0.2
    cc = {"X": 6, "Y": 4}
    check_close("p_all_one_country, n=3 of 10 (6/4)",
                P.p_all_one_country(3, cc, 10), 24 / 120)
    # Draw 5: only X can supply 5. C(6,5)/C(10,5) = 6/252
    check_close("p_all_one_country, n=5 of 10 (6/4)",
                P.p_all_one_country(5, cc, 10), 6 / 252)
    # n larger than any single country: impossible.
    check_close("p_all_one_country, n=7 impossible",
                P.p_all_one_country(7, cc, 10), 0.0)
    # n < 2 is not a meaningful 'single country' claim.
    check_close("p_all_one_country, n=1 returns 0",
                P.p_all_one_country(1, cc, 10), 0.0)

    # Poisson-binomial: three independent trials at p=0.5.
    # P(X>=0)=1, P(X>=2)=4/8=0.5, P(X>=3)=1/8
    check_close("poisson_binomial_tail k=0", P.poisson_binomial_tail([.5] * 3, 0), 1.0)
    check_close("poisson_binomial_tail k=2", P.poisson_binomial_tail([.5] * 3, 2), 0.5)
    check_close("poisson_binomial_tail k=3", P.poisson_binomial_tail([.5] * 3, 3), 0.125)
    check_close("poisson_binomial_tail k>n", P.poisson_binomial_tail([.5] * 3, 4), 0.0)
    # Unequal probabilities: P(X>=2) for p = 0.1, 0.2, 0.3
    # = p1p2(1-p3)+p1p3(1-p2)+p2p3(1-p1)+p1p2p3
    p1, p2, p3 = .1, .2, .3
    want = (p1*p2*(1-p3) + p1*p3*(1-p2) + p2*p3*(1-p1) + p1*p2*p3)
    check_close("poisson_binomial_tail unequal p, k=2",
                P.poisson_binomial_tail([p1, p2, p3], 2), want)


# ---------------------------------------------------------------------------
def write_fixture(root, units, meta_rows, unit_col="unit"):
    """Build a Clusters/ directory and an assignments TSV."""
    trees = os.path.join(root, "Clusters")
    for unit, reps in units.items():
        d = os.path.join(trees, unit, "Gubbins")
        os.makedirs(d, exist_ok=True)
        for rep, nwk in reps.items():
            fn = f"{unit}__ref_{rep}.node_labelled.final_tree.tre"
            open(os.path.join(d, fn), "w").write(nwk)
    ass = os.path.join(root, "assignments.tsv")
    with open(ass, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["sample_id", "country",
                                           "bioproject", unit_col],
                           delimiter="\t", lineterminator="\n")
        w.writeheader()
        for r in meta_rows:
            w.writerow(r)
    return ass, trees


def run(ass, trees, out, extra=()):
    cmd = [sys.executable, "phylogeography_association_bp.py",
           "--assignments", ass, "--trees", trees, "--out", out,
           "--perms", "200", *extra]
    return subprocess.run(cmd, capture_output=True, text=True)


def test_preflight_aborts():
    """
    The defect this guards against: assignments from one partition joined to
    trees from another, producing plausible numbers nobody questions.
    """
    print("\npreflight")
    root = tempfile.mkdtemp()
    try:
        # Trees hold unit_A. Assignments name unit_B. They must not join.
        units = {"unit_A": {"1": "((s1,s2),(s3,s4));"}}
        meta = [{"sample_id": f"s{i}", "country": "Thailand",
                 "bioproject": "P1", "unit": "unit_B"} for i in range(1, 5)]
        ass, trees = write_fixture(root, units, meta)
        r = run(ass, trees, os.path.join(root, "o.tsv"))
        check("aborts on partition mismatch", r.returncode, 2)
        check("says why", "different partitions" in r.stderr, True)

        # --allow-partial proceeds, but on the intersection (which is empty).
        r2 = run(ass, trees, os.path.join(root, "o2.tsv"), ("--allow-partial",))
        check("--allow-partial does not abort", r2.returncode, 0)

        # Matching partitions run clean.
        meta_ok = [dict(m, unit="unit_A") for m in meta]
        ass2, _ = write_fixture(root, units, meta_ok)
        r3 = run(ass2, trees, os.path.join(root, "o3.tsv"))
        check("matching partitions run clean", r3.returncode, 0)

        # A missing unit column is caught rather than silently producing zero units.
        ass3 = os.path.join(root, "bad.tsv")
        open(ass3, "w").write("sample_id\tcountry\tbioproject\n s1\tThailand\tP1\n")
        r4 = run(ass3, trees, os.path.join(root, "o4.tsv"))
        check("missing unit column aborts", r4.returncode, 2)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_signal_and_single_country():
    """
    End to end: a clustered unit, an interleaved unit, and single-country units
    that must be excluded from the permutation count and counted in the
    enrichment test instead.
    """
    print("\nend to end")
    root = tempfile.mkdtemp()
    try:
        units, meta = {}, []

        # clustered: 8 tips, 4 Thailand then 4 Australia, perfectly sorted.
        units["u_clustered"] = {
            "1": "(((t1,t2),(t3,t4)),((a1,a2),(a3,a4)));",
            "2": "(((t1,t2),(t3,t4)),((a1,a2),(a3,a4)));",
        }
        for s in ("t1", "t2", "t3", "t4"):
            meta.append({"sample_id": s, "country": "Thailand",
                         "bioproject": "P1", "unit": "u_clustered"})
        for s in ("a1", "a2", "a3", "a4"):
            meta.append({"sample_id": s, "country": "Australia",
                         "bioproject": "P2", "unit": "u_clustered"})

        # interleaved: same topology, labels alternating.
        units["u_mixed"] = {"1": "(((m1,m2),(m3,m4)),((m5,m6),(m7,m8)));"}
        for i, s in enumerate(["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8"]):
            meta.append({"sample_id": s,
                         "country": "Thailand" if i % 2 == 0 else "Australia",
                         "bioproject": "P3", "unit": "u_mixed"})

        # two single-country units, which must NOT be counted as clustered.
        for k in (1, 2):
            u = f"u_single{k}"
            units[u] = {"1": f"((x{k}1,x{k}2),(x{k}3,x{k}4));"}
            for j in range(1, 5):
                meta.append({"sample_id": f"x{k}{j}", "country": "Thailand",
                             "bioproject": f"P{k}", "unit": u})

        ass, trees = write_fixture(root, units, meta)
        out = os.path.join(root, "out.tsv")
        r = run(ass, trees, out)
        if r.returncode != 0:
            print(r.stdout, r.stderr)
        check("exit 0", r.returncode, 0)

        rows = list(csv.DictReader(open(out), delimiter="\t"))
        by = {(x["unit"], x["variable"]): x for x in rows}

        # Perfectly sorted labels give the minimum possible parsimony score.
        check("clustered unit parsimony == 1",
              by[("u_clustered", "country")]["parsimony_score"], "1")
        check("clustered unit is called clustered",
              by[("u_clustered", "country")]["verdict"], "clustered")
        # Interleaved labels cannot beat chance.
        check("interleaved unit not called clustered",
              by[("u_mixed", "country")]["verdict"] != "clustered", True)
        # Single-country units are uninformative for the permutation test.
        check("single-country unit has no p-value",
              by[("u_single1", "country")]["p_value"], "")
        check("single-country unit marked uninformative",
              by[("u_single1", "country")]["verdict"].startswith("uninformative"),
              True)
        # DEFERRED, not dropped. The second-replicon agreement check is a real
        # internal replication and these assertions are kept verbatim for when
        # it lands. It is not carried yet because it adds columns to the output
        # schema, and PHYLOGEOGRAPHY_ASSOCIATION_FROZEN_2026-08-23.tsv is a
        # frozen artifact that downstream tables read; adding columns means
        # regenerating it, which is a basis decision rather than a code change.
        # The reported script scores one replicon per unit on the stated grounds
        # that the two replicons share a genealogy. Re-enable together.
        if "replicon2_p_value" in (by[("u_clustered", "country")] or {}):
            check("replicon 2 checked when present",
                  by[("u_clustered", "country")]["replicon2_p_value"] != "", True)
            check("replicon 2 blank when absent",
                  by[("u_mixed", "country")]["replicon2_p_value"], "")
        else:
            print("  SKIP  replicon 2 checks: feature deferred, see comment")
        # The enrichment test ran and reported an exact tail.
        check("single-country section printed",
              "SINGLE-COUNTRY UNITS" in r.stdout, True)
        check("observed count is 2", "observed              : 2" in r.stdout, True)
        check("exact tail reported", "P(X >= observed)" in r.stdout, True)

        # Unknown countries must weaken, never fabricate, signal.
        meta_unk = [dict(m) for m in meta]
        for m in meta_unk:
            if m["unit"] == "u_clustered":
                m["country"] = ""
        ass2 = os.path.join(root, "unk.tsv")
        with open(ass2, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["sample_id", "country",
                                               "bioproject", "unit"],
                               delimiter="\t", lineterminator="\n")
            w.writeheader()
            for m in meta_unk:
                w.writerow(m)
        r2 = run(ass2, trees, os.path.join(root, "unk_out.tsv"))
        rows2 = list(csv.DictReader(open(os.path.join(root, "unk_out.tsv")),
                                    delimiter="\t"))
        by2 = {(x["unit"], x["variable"]): x for x in rows2}
        check("all-unknown country is uninformative, not significant",
              by2[("u_clustered", "country")]["p_value"], "")
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    test_fitch()
    test_single_country_math()
    test_preflight_aborts()
    test_signal_and_single_country()
    print("\n" + ("ALL PASS" if not FAILED
                  else f"{len(FAILED)} FAILED: {', '.join(FAILED)}"))
    sys.exit(1 if FAILED else 0)
