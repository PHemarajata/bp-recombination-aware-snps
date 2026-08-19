#!/usr/bin/env python3
"""Reduced reference-sensitivity protocol: 4 arms instead of 12, for threshold-finding.

WHY REDUCED. The full 12-arm protocol (3 callers x 2 references x 2 replicons)
exists to test REFERENCE SENSITIVITY. That question is settled -- per-cluster
constrained-medoid references, replicated across five clusters, avoiding up to
+630% false calls (A.3b/A.3c/A.6/A.7/A.9). Re-testing it on every new cluster
is waste: the snippy arms cost 11-21 min each, the ska arms ~2 min.

This runs only `ska_map` (the reference-free arbiter) against both references
and both replicons = 4 arms, ~10 min per cluster instead of ~2 h. That is
sufficient for the two thresholds still open (A.9):

  under-detection : union coverage collapses at low diversity. Bracketed only
                    to (535, 3,639) -- a 6.8x gap with NOTHING measured inside.
  dating          : root-to-tip slope becomes large-magnitude nonsense (one
                    cluster negative on both replicons). Bracketed to
                    (3,639, 5,362).

It also reports pooled r/m, which bears on A.9 Finding 2 (unresolved: narrow
detection window vs cluster_16 being an atypical lineage).

WHAT IT DOES NOT DO. No snippy/`existing` arm, so it cannot measure the
reference-bias INFLATION of the mapping caller, and no `ska_lo`, so there is no
third-caller concordance check. Use the full protocol if either is the question.

MODALITY SCREEN IS MANDATORY. A multi-modal cluster's Gubbins result reflects
the bridging, not the diversity, so it cannot serve as a threshold test case --
cluster_48 was selected on mean ~= median (4,562 vs 4,581), is three
sub-lineages, and produced an uninterpretable result. This script REFUSES a
cluster flagged as a mixture unless --allow-mixture is passed.

Usage:
    python3 reduced_refsens_bp.py --clusters cluster_34,cluster_27
    python3 reduced_refsens_bp.py --auto-select 6 --band 800,3600
    python3 reduced_refsens_bp.py --selftest
"""

import argparse
import csv
import glob
import os
import re
import subprocess
import sys

SELF = os.path.dirname(os.path.abspath(__file__))
# Local canonical copy. The pipeline output tree this originally pointed at
# (results_all_2802/) VANISHED mid-sweep on 2026-08-10, skipping 4 clusters.
# Recovered from the Nextflow work dir (exact match: 2,802 genomes, 153
# clusters, same 91 multi-genome clusters). Never depend on a path outside
# this working directory again.
MEMBERSHIP = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "inputs", "cluster_membership_2802.tsv")
FASTA_DIR = "/home/phemarajata/Downloads/final_deduped_all_BP_with_locations"
METADATA = os.path.join(FASTA_DIR,
                        "megamix_bestshot_cleaned_dropGCF_on_Fdups_APPENDED.tsv")
CONDA_SH = "/home/phemarajata/miniforge3/etc/profile.d/conda.sh"
OUTDIR_PREFIX = "reduced_"
JOBS = 1
THREADS_PER_ARM = 4
K96243 = "K96243=refs/K96243.fasta#NC_006350.1,NC_006351.1"


def members(cluster):
    out = []
    with open(MEMBERSHIP) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r["cluster_id"] == cluster:
                out.append(r["sample_id"])
    return out


REF_TABLE = "cluster_references.tsv"
MOD_TABLE = "cluster_modality.tsv"


def ref_row(cluster):
    with open(os.path.join(SELF, REF_TABLE)) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r["cluster_id"] == cluster:
                return r
    return None


def modality_row(cluster):
    p = os.path.join(SELF, MOD_TABLE)
    if not os.path.exists(p):
        return None
    with open(p) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r["cluster_id"] == cluster:
                return r
    return None


def load_dates():
    """genome -> year. Joins on ALL key columns: the TSV has two `sample_id`
    columns plus `FASTA_name`, and DictReader silently keeps only the last,
    which drops ~half the collection (handoff trap 12)."""
    rd = csv.reader(open(METADATA, newline=""), delimiter="\t")
    hdr = next(rd)
    idx = {}
    for i, h in enumerate(hdr):
        idx.setdefault(h, []).append(i)
    keys = idx["sample_id"] + idx.get("FASTA_name", [])
    dcol = idx["final_collection_dates"][0]
    out = {}
    for row in rd:
        if len(row) <= dcol:
            continue
        for c in keys:
            k = re.sub(r"\.fasta$", "", row[c].strip())
            if k:
                out.setdefault(k, row[dcol].strip())
    return out


def year_of(datestr):
    if not datestr or datestr.startswith("1800/"):
        return None
    m = re.search(r"(19|20)\d{2}", datestr)
    return int(m.group(0)) if m else None


def contig_names(fasta):
    names = []
    with open(fasta) as fh:
        for line in fh:
            if line.startswith(">"):
                names.append(line[1:].split()[0])
    return names


def bash(script, check=True):
    full = ("set +u; . %s; conda activate bp-gubbins; set -u\n" % CONDA_SH) + script
    p = subprocess.run(["bash", "-c", full], capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError("failed (%d): %s" % (p.returncode, p.stderr[-1500:]))
    return p



def plan_concurrency(threads_per_arm, reserve_cores):
    """How many arms to run at once, leaving cores free for the desktop.

    IQ-TREE does NOT scale to high thread counts on these alignments -- measured
    at 656% CPU when given 16 threads, i.e. ~41% efficiency, with the machine
    43% idle overall. It also warns "Number of threads seems too high for short
    alignments". The generated run_all.sh header says the same thing: prefer
    many arms at low thread counts over few at high.

    reserve_cores is deliberate headroom. This laptop froze once mid-run on
    2026-08-10 with no OOM evidence, so leave the desktop room to breathe rather
    than saturating every core.
    """
    try:
        ncpu = len(os.sched_getaffinity(0))
    except AttributeError:
        ncpu = os.cpu_count() or 4
    usable = max(1, ncpu - reserve_cores)
    return max(1, usable // max(1, threads_per_arm)), ncpu


def run_arms_parallel(outdir, jobs):
    """Run arm scripts concurrently, preserving run_all.sh's two guarantees:
    completed arms are SKIPPED (resumable), and a failing arm is logged and
    does not abort the others (handoff trap 7).
    """
    arms = sorted(glob.glob(os.path.join(outdir, "arms", "*.sh")))
    todo = []
    for a in arms:
        name = os.path.basename(a)[:-3]
        tf = os.path.join(outdir, "arms", name, "tree.treefile")
        if os.path.exists(tf) and os.path.getsize(tf) > 0:
            continue
        todo.append(a)
    if not todo:
        return 0, 0
    listfile = os.path.join(outdir, ".arms_todo")
    with open(listfile, "w") as fh:
        fh.write("\n".join(todo) + "\n")
    # xargs -P gives us the concurrency cap; `|| true` per arm isolates failures
    bash("xargs -P {j} -I{{}} bash -c 'bash \"$1\" >> \"{log}\" 2>&1 || "
         "echo \"ARM $1 FAILED\" >> \"{log}\"' _ {{}} < {lst}"
         .format(j=jobs, log=os.path.join(outdir, "run_all.log"), lst=listfile),
         check=False)
    done = sum(1 for a in todo
               if os.path.exists(os.path.join(outdir, "arms",
                                              os.path.basename(a)[:-3], "tree.treefile")))
    return len(todo), len(todo) - done


def prepare(cluster, allow_mixture):
    """Returns (list_file, dates_file, ref_fasta, chr1, chr2) or raises."""
    r = ref_row(cluster)
    if not r:
        raise RuntimeError("%s not in cluster_references.tsv" % cluster)
    if r.get("status") != "ready":
        raise RuntimeError("%s status=%s (needs a complete internal reference)"
                           % (cluster, r.get("status")))
    m = modality_row(cluster)
    if m is None:
        raise RuntimeError("%s not in cluster_modality.tsv -- run "
                           "`measure_diversity_bp.py --screen-all` first (table: %s)"
                           % (cluster, MOD_TABLE))
    if m["structure"] == "mixture" and not allow_mixture:
        raise RuntimeError("%s is a MIXTURE (gap/mean %s); a bridged cluster cannot "
                           "serve as a threshold test case (A.9 Finding 3). "
                           "Pass --allow-mixture to override."
                           % (cluster, m["gap_over_mean"]))

    ids = members(cluster)
    lst = os.path.join(SELF, "cluster_metadata_%s_genomes.tsv" % cluster)
    n = 0
    with open(lst, "w") as fh:
        for s in ids:
            fa = os.path.join(FASTA_DIR, s + ".fasta")
            if os.path.exists(fa):
                fh.write("%s\t%s\n" % (s, fa))
                n += 1
    if n < 6:
        raise RuntimeError("%s: only %d FASTAs found" % (cluster, n))

    dates = load_dates()
    dfile = os.path.join(SELF, "cluster_metadata_%s_dates.csv" % cluster)
    nd = 0
    with open(dfile, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["genome", "year"])
        for s in ids:
            y = year_of(dates.get(s, ""))
            if y:
                w.writerow([s, y])
                nd += 1

    src = os.path.join(FASTA_DIR, r["reference"] + ".fasta")
    dst = os.path.join(SELF, "refs", "%s_close.fasta" % cluster)
    if not os.path.exists(dst):
        bash("cp '%s' '%s'" % (src, dst))
    cn = contig_names(dst)
    if len(cn) != 2:
        raise RuntimeError("%s reference has %d contigs, need 2" % (cluster, len(cn)))
    print("  %s: n=%d, dated=%d, ref=%s, structure=%s (gap/mean %s)"
          % (cluster, n, nd, r["reference"], m["structure"], m["gap_over_mean"]))
    return lst, dfile, dst, cn[0], cn[1]


def run_one(cluster, allow_mixture, threads):
    outdir = os.path.join(SELF, "%s%s" % (OUTDIR_PREFIX, cluster))
    lst, dfile, ref, c1, c2 = prepare(cluster, allow_mixture)
    done = os.path.join(outdir, "RESULTS.txt")
    if os.path.exists(done) and os.path.getsize(done) > 0:
        print("  %s: already complete, skipping" % cluster)
        return outdir

    plan = ("python3 %s plan --cluster-list %s "
            "--ref 'close=%s#%s,%s' --ref '%s' --outdir %s "
            "--callers ska_map --env-caller snp-phylogeny --env-recomb bp-gubbins "
            "--threads %d" % (os.path.join(SELF, "reference_sensitivity_bp.py"),
                              lst, ref, c1, c2, K96243, outdir, threads))
    bash(plan)
    n, failed = run_arms_parallel(outdir, JOBS)
    print("  %s: ran %d arms at %d-way concurrency (%d threads each)%s"
          % (cluster, n, JOBS, THREADS_PER_ARM,
             ", %d FAILED" % failed if failed else ""))
    bash("python3 %s analyse --outdir %s --dates %s --close-ref close "
         "> %s/RESULTS.txt 2>&1 || true"
         % (os.path.join(SELF, "reference_sensitivity_bp.py"), outdir, dfile, outdir),
         check=False)
    fails = bash("grep -c 'FAILED' %s/run_all.log || true" % outdir, check=False)
    print("  %s: done (%s FAILED lines in log)" % (cluster, fails.stdout.strip() or "0"))
    return outdir


def auto_select(count, band, exclude):
    lo, hi = band
    p = os.path.join(SELF, MOD_TABLE)
    if not os.path.exists(p):
        raise RuntimeError("run `measure_diversity_bp.py --screen-all` first")
    rows = []
    with open(p) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r["usable_testcase"] != "yes":
                continue
            if r["cluster_id"] in exclude:
                continue
            mn = float(r["mean_snps"])
            if lo <= mn <= hi:
                rows.append((mn, r["cluster_id"], int(r["n"])))
    rows.sort()
    if not rows:
        return []
    # spread the picks evenly across the band rather than clustering them
    if count >= len(rows):
        return [c for _, c, _ in rows]
    step = (len(rows) - 1) / (count - 1) if count > 1 else 0
    return [rows[int(round(i * step))][1] for i in range(count)]


def selftest():
    fails = []
    # the --ref spec must be NAME=PATH[#REP1,REP2]; a missing NAME= prefix made
    # every run abort at plan time (caught by running it, not by reading it)
    if not re.match(r"^[A-Za-z0-9_]+=.+#[^,]+,[^,]+$", K96243):
        fails.append("K96243 ref spec malformed: %r" % K96243)
    if year_of("1800/2014") is not None:
        fails.append("PRJEB3409 placeholder must be dropped")
    if year_of("2017-05-01") != 2017:
        fails.append("ISO date parse")
    if year_of("") is not None or year_of(None) is not None:
        fails.append("empty date must be None")
    if year_of("1965") != 1965:
        fails.append("bare year parse")
    # auto_select must spread picks, not bunch them
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "cluster_modality.tsv")
        with open(p, "w") as fh:
            fh.write("cluster_id\tn\tref_status\tmean_snps\tmedian_snps\tmax_snps\t"
                     "gap\tgap_over_mean\tempty_bins\tstructure\tusable_testcase\n")
            for i, mn in enumerate([900, 1200, 1800, 2400, 3000, 3400]):
                fh.write("c%d\t40\tready\t%d\t%d\t9\t9\t0.02\t4\tcontinuous\tyes\n"
                         % (i, mn, mn))
            fh.write("bad\t40\tready\t2000\t2000\t9\t9\t0.5\t4\tmixture\tno\n")
        global SELF
        old = SELF
        SELF = td
        try:
            got = auto_select(3, (800, 3600), set())
            if len(got) != 3:
                fails.append("auto_select count: got %r" % got)
            if "bad" in got:
                fails.append("auto_select must never return a mixture")
            if got != ["c0", "c2", "c5"]:
                fails.append("auto_select should spread across the band: got %r" % got)
            if auto_select(2, (800, 1000), set()) != ["c0"]:
                fails.append("narrow band should return the single match")
        finally:
            SELF = old
    # concurrency must always leave the reserve free and never return 0
    import unittest.mock as _m
    with _m.patch.object(os, "sched_getaffinity", lambda _: set(range(22))):
        j, n = plan_concurrency(4, 6)
        if n != 22: fails.append("core count: %r" % n)
        if j != 4: fails.append("22 cores, reserve 6, 4 threads -> expected 4 jobs, got %r" % j)
        if j * 4 > 22 - 6: fails.append("concurrency exceeds the usable budget")
        if plan_concurrency(64, 6)[0] != 1: fails.append("must never return 0 jobs")
        if plan_concurrency(4, 100)[0] != 1: fails.append("over-reserving must still allow 1 job")

    # module-level table names must be overridable (sub-cluster partitions)
    for nm in ("REF_TABLE", "MOD_TABLE", "MEMBERSHIP", "OUTDIR_PREFIX"):
        if nm not in globals():
            fails.append("%s must exist as a module global for --override to work" % nm)

    if fails:
        print("SELFTEST FAILED (%d)" % len(fails))
        for f in fails:
            print("  " + f)
        return 1
    print("selftest: 18/18 checks passed")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--clusters", default="", help="comma-separated cluster ids")
    ap.add_argument("--auto-select", type=int, default=0,
                    help="pick N usable clusters spread across --band")
    ap.add_argument("--band", default="800,3600", help="lo,hi measured mean pairwise SNPs")
    ap.add_argument("--allow-mixture", action="store_true")
    ap.add_argument("--threads", type=int, default=4,
                    help="threads PER ARM (default 4; IQ-TREE does not scale past ~6)")
    ap.add_argument("--reserve-cores", type=int, default=6,
                    help="cores left free for the OS/desktop (default 6)")
    ap.add_argument("--jobs", type=int, default=0,
                    help="arms in flight at once; 0 = auto from cores minus reserve")
    ap.add_argument("--membership", default=None,
                    help="override the membership TSV (e.g. a sub-cluster partition)")
    ap.add_argument("--references", default=None,
                    help="override cluster_references.tsv")
    ap.add_argument("--modality", default=None,
                    help="override cluster_modality.tsv")
    ap.add_argument("--outdir-prefix", default="reduced_")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()

    global MEMBERSHIP, REF_TABLE, MOD_TABLE, OUTDIR_PREFIX
    if args.membership: MEMBERSHIP = args.membership
    if args.references: REF_TABLE = args.references
    if args.modality:   MOD_TABLE = args.modality
    OUTDIR_PREFIX = args.outdir_prefix
    global JOBS, THREADS_PER_ARM
    THREADS_PER_ARM = args.threads
    auto, ncpu = plan_concurrency(args.threads, args.reserve_cores)
    JOBS = args.jobs if args.jobs > 0 else auto
    print("cores %d, reserving %d -> %d arms in flight x %d threads = %d busy, %d free\n"
          % (ncpu, args.reserve_cores, JOBS, THREADS_PER_ARM,
             JOBS * THREADS_PER_ARM, ncpu - JOBS * THREADS_PER_ARM))

    already = {"cluster_53", "cluster_16", "cluster_48", "cluster_8", "cluster_0", "cluster_37"}
    if args.auto_select:
        lo, hi = [float(x) for x in args.band.split(",")]
        clusters = auto_select(args.auto_select, (lo, hi), already)
        print("auto-selected %d clusters in band %g-%g: %s\n"
              % (len(clusters), lo, hi, ", ".join(clusters) or "(none usable)"))
    else:
        clusters = [c.strip() for c in args.clusters.split(",") if c.strip()]
    if not clusters:
        ap.error("nothing to run")

    for c in clusters:
        try:
            if args.dry_run:
                prepare(c, args.allow_mixture)
            else:
                run_one(c, args.allow_mixture, args.threads)
        except Exception as exc:
            print("  %s: SKIPPED -- %s" % (c, exc))
    return 0


if __name__ == "__main__":
    sys.exit(main())
