#!/usr/bin/env python3
"""Re-measure the QC evidence behind four PANEL_EXCLUSIONS.tsv rows.

The four rows -- SRR2896257, SRR2896259, ERR9980356 (broken_assembly) and
SRR2896271 (wrong_species_or_divergent) -- all read `core=na%`, and all four
gene-count ratios are below the 1.20 gate, so the stated reason ("core coverage
<85% OR frameshift ratio >1.20") is evidenced by neither clause. The decisions
were taken on the SKESA batch; the panel and the cgMLST reference pool then used
the SPAdes re-assemblies.

This script measures both assemblies of each genome under the *same* gate
definitions used by reqc_spades_batch.py, so the two assemblers are directly
comparable:

    core completeness   minimap2 -x asm10 vs K96243, MAPQ >= 10, merged
                        reference intervals / 7,247,547 bp; gate >= 85%
    base accuracy       prodigal single-mode gene count /
                        (821 * assembly_Mb + 1.0 * contigs_ge500); gate <= 1.20
    species/divergence  mash -s 10000 -k 21 to K96243 (the sketch size the
                        0.008/0.012 thresholds were calibrated at)

Controls are measured alongside the targets so the numbers have a scale:
ERR8098257 is a register row from the same batch that genuinely fails the core
gate on SPAdes (81.3%), and the clean panel controls anchor the passing range.

Read-only. Writes EXCLUSION_RECHECK_<date>.tsv and prints a summary.
"""
import collections
import csv
import os
import statistics
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
REF = f"{BASE}/refs/K96243.fasta"
REFLEN = 7247547
THREADS = os.environ.get("QCTHREADS", "8")
OUT = os.environ.get("QCOUT", f"{BASE}/EXCLUSION_RECHECK_2026-08-23.tsv")

# what the cgMLST pool and the panel actually use
SPADES_DIRS = [f"{BASE}/additions/fasta_spades",
               "/home/phemarajata/Downloads/bp_spades_assemblies"]
# what the exclusion decisions were taken on. Excluded genomes were never
# copied into additions/fasta_new200, so the raw TheiaProk delivery is the
# only place their SKESA assembly survives.
SKESA_DIRS = [f"{BASE}/additions/fasta_new200",
              "/home/phemarajata/Downloads/bp_new_assemblies"]
SUFFIXES = [".fasta", "_filtered_contigs.fasta"]

TARGETS = ["SRR2896257", "SRR2896259", "ERR9980356", "SRR2896271"]
# same-batch register row that genuinely fails the core gate on SPAdes
NEG_CONTROL = ["ERR8098257"]
# clean panel genomes, for the passing range
POS_CONTROL = ["SRR28096039", "SRR28096043", "SRR30648682"]


def contig_stats(path, cutoff=500):
    """Length and contig count over the >=500 bp set, as the gate defines them."""
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
    """Percent of K96243 covered by MAPQ>=10 asm10 alignments, intervals merged.

    Identical to reqc_spades_batch.py: PAF field 11 is MAPQ, 5 is the target
    name, 7/8 the target start/end.
    """
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


def mash_dists(paths, tmpdir):
    """mash at the calibration sketch size, -s 10000 -k 21."""
    lst = os.path.join(tmpdir, "paths.txt")
    with open(lst, "w") as fh:
        fh.write("\n".join(paths) + "\n")
    subprocess.run(["mash", "sketch", "-s", "10000", "-k", "21", "-p", THREADS,
                    "-o", os.path.join(tmpdir, "batch"), "-l", lst],
                   capture_output=True)
    subprocess.run(["mash", "sketch", "-s", "10000", "-k", "21",
                    "-o", os.path.join(tmpdir, "ref"), REF], capture_output=True)
    dist = subprocess.run(["mash", "dist", os.path.join(tmpdir, "ref.msh"),
                           os.path.join(tmpdir, "batch.msh")],
                          capture_output=True, text=True).stdout
    return {l.split("\t")[1]: float(l.split("\t")[2])
            for l in dist.splitlines() if l.strip()}


def resolve(sample, dirs):
    for d in dirs:
        for suf in SUFFIXES:
            p = os.path.join(d, f"{sample}{suf}")
            if os.path.exists(p):
                return p
    return None


def main():
    jobs = []   # (sample, role, assembler, path)
    for group, role in ((TARGETS, "target"), (NEG_CONTROL, "neg_control"),
                        (POS_CONTROL, "pos_control")):
        for s in group:
            for asm, dirs in (("spades", SPADES_DIRS), ("skesa", SKESA_DIRS)):
                p = resolve(s, dirs)
                if p:
                    jobs.append((s, role, asm, p))
                else:
                    print(f"  WARNING: no {asm} assembly for {s}",
                          file=sys.stderr)

    tmp = tempfile.mkdtemp()
    mash = mash_dists([j[3] for j in jobs], tmp)

    rows = []
    for i, (s, role, asm, p) in enumerate(jobs, 1):
        length, ctg, n50, raw = contig_stats(p)
        cov = core_cov(p)
        g, medlen = genes(p, tmp)
        ratio = g / (821 * length / 1e6 + 1.0 * ctg)
        d = mash.get(p, float("nan"))
        why = []
        if cov < 85:
            why.append(f"core {cov:.1f}% < 85%")
        if ratio > 1.20:
            why.append(f"gene ratio {ratio:.2f} > 1.20")
        if d > 0.012:
            why.append(f"mash {d:.4f} > 0.012")
        if length > 7_600_000:
            why.append(f"length {length/1e6:.2f} Mb > 7.6 Mb")
        rows.append(dict(
            sample=s, role=role, assembler=asm,
            verdict="pass" if not why else "fail",
            fail_reasons="; ".join(why),
            core_cov_pct=f"{cov:.1f}", mash_to_K96243=f"{d:.4f}",
            gene_count_ratio=f"{ratio:.2f}", prodigal_genes=g,
            length_ge500=length, contigs_ge500=ctg, n50=n50, contigs_all=raw,
            median_gene_len=f"{medlen:.0f}", path=p))
        print(f"  [{i}/{len(jobs)}] {s:<12} {asm:<7} core={cov:5.1f}%  "
              f"mash={d:.4f}  ratio={ratio:.2f}  {'PASS' if not why else 'FAIL'}",
              flush=True)

    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    print(f"\nwrote {OUT} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
