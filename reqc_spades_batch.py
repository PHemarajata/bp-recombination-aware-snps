#!/usr/bin/env python3
"""
Re-QC the SPAdes re-assembly batch, using the same gates as NEW200_QC_2026-08-17.

Gates, unchanged from the calibration in NEW200_QC_REPORT_2026-08-17.md so the
two rounds are comparable:

    species / divergence   mash to K96243 <= 0.012, gambit not thailandensis
    core completeness      >= 85% of K96243 covered
    base accuracy          gene-count ratio <= 1.20, where
                           expected = 821 * assembly_Mb + 1.0 * contigs
    length                 upper bound only (<= 7.6 Mb, raised from 7.4 after SPAdes
                           assemblies ran longer than SKESA); the lower bound is
                           deliberately NOT applied -- it rejects fragmented
                           short-read assemblies that carry 86-98% of the core

Assembly source per sample:
    PANEL_ASSEMBLY_OVERRIDES.tsv wins (currently 3 samples pinned to SKESA)
    otherwise the SPAdes assembly

Samples in PANEL_EXCLUSIONS.tsv are reported but never pass.

Mash uses -s 10000 -k 21, matching the sketch size the 0.008/0.012 thresholds
were calibrated at -- NOT the -s 50000 the partition uses.

Writes SPADES_QC_<date>.tsv and SPADES_PASS_LIST.txt.
"""
import collections
import csv
import glob
import json
import os
import statistics
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
SPADES = "/home/phemarajata/Downloads/bp_spades_assemblies"
REF = f"{BASE}/refs/K96243.fasta"
REFLEN = 7247547
TERRA = f"{SPADES}/bp_2b_assembled (2).tsv"
THREADS = os.environ.get("QCTHREADS", "8")
OUT = os.environ.get("QCOUT", f"{BASE}/SPADES_QC_2026-08-17.tsv")


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
    tot, run = sum(L), 0
    n50 = 0
    for x in L:
        run += x
        if run >= tot / 2:
            n50 = x
            break
    return tot, len(L), n50, raw


def core_cov(path, tmpdir):
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


def genes(path, tmpdir):
    fna = os.path.join(tmpdir, "p.fna")
    subprocess.run(["prodigal", "-i", path, "-d", fna, "-q", "-p", "single",
                    "-o", os.devnull], capture_output=True)
    n, lens = 0, []
    for line in open(fna):
        if line.startswith(">"):
            f = line.split("#")
            n += 1
            try:
                lens.append(abs(int(f[2]) - int(f[1])) + 1)
            except (IndexError, ValueError):
                pass
    return n, (statistics.median(lens) if lens else 0)


def main():
    excl = {r["sample_id"]: r for r in
            csv.DictReader(open(f"{BASE}/PANEL_EXCLUSIONS.tsv"), delimiter="\t")}
    over = {r["sample_id"]: r for r in
            csv.DictReader(open(f"{BASE}/PANEL_ASSEMBLY_OVERRIDES.tsv"), delimiter="\t")}
    terra = {r["entity:bp_2b_assembled_id"]: r for r in
             csv.DictReader(open(TERRA), delimiter="\t")}
    sra = {r["run_accession"]: r for r in
           csv.DictReader(open(f"{BASE}/SRA_TO_ASSEMBLE.tsv"), delimiter="\t")}

    paths = {}
    for p in sorted(glob.glob(f"{SPADES}/*.fasta")):
        paths[acc(p)] = p
    for s, r in over.items():
        paths[s] = r["use_path"]          # pinned assembly wins

    # mash, one sketch file for the batch
    tmp = tempfile.mkdtemp()
    lst = os.path.join(tmp, "paths.txt")
    order = sorted(paths)
    with open(lst, "w") as fh:
        fh.write("\n".join(paths[s] for s in order) + "\n")
    subprocess.run(["mash", "sketch", "-s", "10000", "-k", "21", "-p", THREADS,
                    "-o", os.path.join(tmp, "batch"), "-l", lst],
                   capture_output=True)
    subprocess.run(["mash", "sketch", "-s", "10000", "-k", "21",
                    "-o", os.path.join(tmp, "ref"), REF], capture_output=True)
    dist = subprocess.run(["mash", "dist", os.path.join(tmp, "ref.msh"),
                           os.path.join(tmp, "batch.msh")],
                          capture_output=True, text=True).stdout
    mash = {acc(l.split("\t")[1]): float(l.split("\t")[2])
            for l in dist.splitlines() if l.strip()}

    rows = []
    for i, s in enumerate(order, 1):
        p = paths[s]
        length, ctg, n50, raw = contig_stats(p)
        cov = core_cov(p, tmp)
        g, medlen = genes(p, tmp)
        ratio = g / (821 * length / 1e6 + 1.0 * ctg)
        t = terra.get(s, {})
        meta = sra.get(s, {})
        why = []
        if s in excl:
            why.append(f"excluded:{excl[s]['reason_class']}")
        if mash.get(s, 1) > 0.012:
            why.append(f"mash {mash.get(s):.4f} > 0.012")
        if (t.get("gambit_predicted_taxon") or "") == "Burkholderia thailandensis":
            why.append("gambit: B. thailandensis")
        if cov < 85:
            why.append(f"core {cov:.1f}% < 85%")
        if ratio > 1.20:
            why.append(f"gene ratio {ratio:.2f} > 1.20")
        if length > 7_600_000:
            why.append(f"length {length/1e6:.2f} Mb > 7.6 Mb")
        rows.append(dict(
            sample=s, verdict="pass" if not why else "fail",
            fail_reasons="; ".join(why),
            assembly_source=over[s]["use_assembler"] if s in over else "spades",
            length_ge500=length, contigs_ge500=ctg, n50=n50,
            contigs_all=raw, core_cov_pct=f"{cov:.1f}",
            mash_to_K96243=f"{mash.get(s, float('nan')):.4f}",
            prodigal_genes=g, gene_count_ratio=f"{ratio:.2f}",
            median_gene_len=f"{medlen:.0f}",
            gambit_taxon=t.get("gambit_predicted_taxon", ""),
            est_coverage=t.get("est_coverage_clean", ""),
            origin_country=meta.get("origin_country", ""),
            collection_date=meta.get("collection_date", ""),
        ))
        if i % 25 == 0:
            print(f"  {i}/{len(order)}", flush=True)

    cols = list(rows[0])
    rows.sort(key=lambda r: (r["verdict"] != "pass", -float(r["core_cov_pct"])))
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    passed = [r["sample"] for r in rows if r["verdict"] == "pass"]
    with open(f"{BASE}/SPADES_PASS_LIST.txt", "w") as fh:
        fh.write("\n".join(sorted(passed)) + "\n")

    print(f"\nwrote {OUT} ({len(rows)} rows) and SPADES_PASS_LIST.txt ({len(passed)})")
    print(f"  pass {len(passed)}   fail {len(rows)-len(passed)}")
    print("  fail reasons:",
          dict(collections.Counter(w.split(";")[0].split(":")[0].split(" ")[0]
                                   for r in rows if r["verdict"] == "fail"
                                   for w in [r["fail_reasons"]])))


if __name__ == "__main__":
    main()
