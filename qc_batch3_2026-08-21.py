#!/usr/bin/env python3
"""
QC the 2026-08-21 additions, using the gates calibrated in
NEW200_QC_REPORT_2026-08-17.md so this round is comparable with the last.

Two input sets, QC'd together so the within-batch rank check has a denominator:
  A. 40 SPAdes assemblies from Terra   (/home/phemarajata/Downloads/bp_spades_assemblies_2)
  B. 17 Mexican reference genomes      (additions_mexico_2026-08-21/fasta)

Gates, unchanged from the 08-17 calibration:
    species / divergence   mash to K96243 <= 0.012   (sketch -s 10000 -k 21,
                           the size the threshold was calibrated at, NOT the
                           -s 50000 the partition uses)
    core completeness      >= 85% of K96243 covered (minimap2 -x asm10, MAPQ>=10)
    base accuracy          gene-count ratio <= 1.20, where
                           expected = 821 * assembly_Mb + 1.0 * contigs
    length                 UPPER bound only (<= 7.6 Mb). The lower bound is
                           deliberately not applied: it rejects fragmented
                           short-read assemblies carrying 86-98% of the core.

Plus the lesson from the ONT genomes (NEW200 §2.12.3): the gene-count ratio has
little discriminating power on near-complete assemblies, and what actually
separated the bad ones was RANK WITHIN BATCH, not the absolute value. So the
batch p90 is reported and anything above it is flagged for a look even if it
passes the absolute gate.

Writes BATCH3_QC_2026-08-21.tsv and BATCH3_PASS_LIST.txt.
"""
import collections
import concurrent.futures as cf
import csv
import glob
import os
import re
import statistics
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
REF = f"{BASE}/refs/K96243.fasta"
REFLEN = 7247547
SETS = [
    ("terra40", "/home/phemarajata/Downloads/bp_spades_assemblies_2/*.fasta"),
    ("mexico17", f"{BASE}/additions_mexico_2026-08-21/fasta/*.fasta"),
]
THREADS = os.environ.get("QCTHREADS", "4")
WORKERS = int(os.environ.get("QCWORKERS", "6"))
OUT = f"{BASE}/BATCH3_QC_2026-08-21.tsv"

MASH_MAX = 0.012
CORE_MIN = 85.0
RATIO_MAX = 1.20
LEN_MAX = 7_600_000


def acc(p):
    b = os.path.basename(p)
    for s in ("_filtered_contigs.fasta", "_reoriented.fasta", ".fasta"):
        b = b.replace(s, "")
    return b


def contig_stats(path, cutoff=500):
    L, c = [], 0
    for line in open(path):
        if line.startswith(">"):
            if c:
                L.append(c)
            c = 0
        else:
            c += len(line.strip())
    if c:
        L.append(c)
    raw = len(L)
    L = sorted([x for x in L if x >= cutoff], reverse=True)
    tot, run, n50 = sum(L), 0, 0
    for x in L:
        run += x
        if run >= tot / 2:
            n50 = x
            break
    return tot, len(L), n50, raw


def core_cov(path):
    out = subprocess.run(
        ["minimap2", "-x", "asm10", "-t", THREADS, REF, path],
        capture_output=True, text=True).stdout
    iv = collections.defaultdict(list)
    for line in out.splitlines():
        f = line.split("\t")
        if len(f) > 11 and int(f[11]) >= 10:
            iv[f[5]].append((int(f[7]), int(f[8])))
    tot = 0
    for v in iv.values():
        v.sort()
        cs = ce = None
        for s, e in v:
            if cs is None:
                cs, ce = s, e
            elif s <= ce:
                ce = max(ce, e)
            else:
                tot += ce - cs
                cs, ce = s, e
        if cs is not None:
            tot += ce - cs
    return tot * 100 / REFLEN


def genes(path):
    with tempfile.TemporaryDirectory() as td:
        fna = os.path.join(td, "p.fna")
        subprocess.run(["prodigal", "-i", path, "-d", fna, "-q", "-p", "single",
                        "-o", os.devnull], capture_output=True)
        n, lens = 0, []
        if os.path.exists(fna):
            for line in open(fna):
                if line.startswith(">"):
                    f = line.split("#")
                    n += 1
                    try:
                        lens.append(abs(int(f[2]) - int(f[1])) + 1)
                    except (IndexError, ValueError):
                        pass
    return n, (statistics.median(lens) if lens else 0)


def mash_dist(paths, order):
    with tempfile.TemporaryDirectory() as td:
        lst = os.path.join(td, "p.txt")
        with open(lst, "w") as fh:
            fh.write("\n".join(paths[s] for s in order) + "\n")
        subprocess.run(["mash", "sketch", "-s", "10000", "-k", "21",
                        "-o", os.path.join(td, "b"), "-l", lst],
                       capture_output=True)
        out = subprocess.run(["mash", "dist", REF, os.path.join(td, "b.msh")],
                             capture_output=True, text=True).stdout
    d = {}
    for line in out.splitlines():
        f = line.split("\t")
        if len(f) >= 3:
            d[acc(f[1])] = float(f[2])
    return d


def one(item):
    s, p, setname = item
    tot, n, n50, raw = contig_stats(p)
    cov = core_cov(p)
    ng, gl = genes(p)
    exp = 821 * (tot / 1e6) + 1.0 * n
    return dict(sample_id=s, set=setname, path=p, length=tot, contigs=n,
                n50=n50, raw_contigs=raw, core_cov=round(cov, 2),
                genes=ng, median_gene_len=gl,
                expected_genes=round(exp, 1),
                ratio=round(ng / exp, 3) if exp else 0)


def main():
    paths, setof = {}, {}
    for name, pat in SETS:
        for p in sorted(glob.glob(pat)):
            paths[acc(p)] = p
            setof[acc(p)] = name
    order = sorted(paths)
    print(f"QC on {len(order)} assemblies "
          f"({sum(1 for s in order if setof[s]=='terra40')} terra40, "
          f"{sum(1 for s in order if setof[s]=='mexico17')} mexico17)",
          file=sys.stderr, flush=True)

    print("  mash ...", file=sys.stderr, flush=True)
    md = mash_dist(paths, order)

    rows = []
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for i, r in enumerate(ex.map(one, [(s, paths[s], setof[s]) for s in order]), 1):
            r["mash_K96243"] = md.get(r["sample_id"], float("nan"))
            rows.append(r)
            print(f"  [{i}/{len(order)}] {r['sample_id']}", file=sys.stderr, flush=True)

    ratios = [r["ratio"] for r in rows]
    p90 = statistics.quantiles(ratios, n=10)[8] if len(ratios) >= 10 else max(ratios)

    for r in rows:
        fail = []
        if r["mash_K96243"] > MASH_MAX:
            fail.append(f"mash>{MASH_MAX}")
        if r["core_cov"] < CORE_MIN:
            fail.append(f"core<{CORE_MIN}%")
        if r["ratio"] > RATIO_MAX:
            fail.append(f"ratio>{RATIO_MAX}")
        if r["length"] > LEN_MAX:
            fail.append("length>7.6Mb")
        r["batch_p90_ratio"] = round(p90, 3)
        r["rank_flag"] = "above_batch_p90" if r["ratio"] > p90 else ""
        r["verdict"] = "PASS" if not fail else "FAIL"
        r["reason"] = ";".join(fail)

    cols = ["sample_id", "set", "verdict", "reason", "length", "contigs", "n50",
            "raw_contigs", "core_cov", "mash_K96243", "genes", "expected_genes",
            "ratio", "batch_p90_ratio", "rank_flag", "median_gene_len", "path"]
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        for r in sorted(rows, key=lambda x: (x["set"], x["sample_id"])):
            w.writerow({c: r[c] for c in cols})
    with open(f"{BASE}/BATCH3_PASS_LIST.txt", "w") as fh:
        for r in sorted(rows, key=lambda x: x["sample_id"]):
            if r["verdict"] == "PASS":
                fh.write(r["sample_id"] + "\n")
    npass = sum(1 for r in rows if r["verdict"] == "PASS")
    print(f"\nwrote {OUT}\n  PASS {npass} / {len(rows)}", file=sys.stderr)


if __name__ == "__main__":
    main()
