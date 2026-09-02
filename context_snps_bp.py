#!/usr/bin/env python3
"""
Recombination-aware SNP distances and local context trees for the recurrence
series, matching the reported pipeline's method rather than re-inventing it.

WHY THIS EXISTS
---------------
The mash distances in C29_recurrence_pairwise_mash.csv are k-mer distances. They
separate the one reinfection from the 19 relapses cleanly, but they cannot say
how many SNPs separate two episodes, and they are inflated by recombination,
which matters here because this organism runs r/m near 7.7. Two isolates that
differ by a single imported recombinant tract look far apart by mash and are
nearly identical once the tract is removed.

The existing L1 cluster Gubbins runs already answer this for 16 of the 20 pairs,
but their context is the global panel (UK, other Thai provinces, public
assemblies). They also do not cover patients 7 and 10, whose isolates are not in
the panel at all, nor patient 9, whose two isolates sit in different clusters.
This script builds a purpose-made local analysis instead: for every recurrence
patient, the patient's own isolates plus the Nakhon Phanom genomes that are
actually close to them.

METHOD (matches the reported run: main@79ab645)
-----------------------------------------------
Per context group, exactly the chain the pipeline runs per cluster:

  snippy --ctgs        per genome, against the group medoid
  snippy-core          -> <g>.full.aln, the WHOLE-GENOME alignment
  drop Reference       our reference is a group member, so snippy-core's
                       "Reference" record would duplicate it
  run_gubbins.py       --tree-builder raxml --iterations 5 --min-snps 3
                       --invariant-site-correction --filter-percentage 25.0
  iqtree2              GTR+ASC on the recombination-filtered variant sites

The alignment handed to Gubbins keeps invariant sites. This is not optional:
Gubbins is a spatial scanning statistic over SNP density along the alignment,
and a variant-sites-only alignment silently produces nonsense. The pipeline's
own module aborts rather than substitute the SNP-only <prefix>.aln.

The column-missingness filter the pipeline applies between snippy-core and
Gubbins is skipped here because it ran as an exact no-op in the reported run
(max_column_missingness = 1.0, kept_fraction 1.000000).

DELIBERATE DEPARTURES, AND WHY
------------------------------
  --seed        The pipeline passes no seed. Gubbins then draws an unseeded
                randint(0, 10000) for RAxML's -p, and RAxML rejects -p 0, which
                is a ~1/10001 silent unit loss per call. Seeding also makes this
                reproducible. This changes nothing else.
  Reference     Dropped, because our reference is internal to the group. The
                pipeline keeps it only because its references are external.
  IQ-TREE       2.4.0 here against 2.2.6 in the reported run. No local env has
                2.2.6. Affects tree search, not the SNP distances.
  Gubbins       bp-gubbins carries 3.4.3 py310h5140242_0, byte-identical to the
                build the reported run's container wraps. Do NOT use the poppipe
                env: it is 3.4, where --invariant-site-correction behaves
                differently.

Each Gubbins call runs with its cwd set to its own directory. Gubbins writes
scratch (<basename>.start, .phylip, .snp_sites.aln) into the CWD and not into
--prefix, so concurrent runs sharing a basename delete each other's scratch and
surface as "Unable to fit model to data".
"""

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
ASSEMBLIES = "/home/phemarajata/Downloads/320_isolates"
WORK = os.environ.get("CTX_WORK", "/tmp/recurrence_ctx")
GROUPS_JSON = "/tmp/recurrence_mash_bp/context_groups.json"

SNIPPY_BIN = "/home/phemarajata/miniforge3/envs/snp-phylogeny/bin"
GUBBINS_BIN = "/home/phemarajata/miniforge3/envs/bp-gubbins/bin"

GUBBINS_ITERATIONS = 5
GUBBINS_MIN_SNPS = 3
GUBBINS_FILTER_PCT = 25.0
SEED = 42
THREADS = int(os.environ.get("CTX_THREADS", "8"))


def run(cmd, cwd=None, bin_dir=None, log=None):
    env = dict(os.environ)
    if bin_dir:
        env["PATH"] = bin_dir + ":" + env["PATH"]
    env["NUMBA_CACHE_DIR"] = os.path.join(cwd or WORK, ".numba_cache")
    os.makedirs(env["NUMBA_CACHE_DIR"], exist_ok=True)
    proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if log:
        with open(log, "w") as fh:
            fh.write(proc.stdout + "\n===STDERR===\n" + proc.stderr)
    return proc


def read_fasta(path):
    seqs, name, buf = {}, None, []
    for line in open(path):
        if line.startswith(">"):
            if name:
                seqs[name] = "".join(buf)
            name, buf = line[1:].strip().split()[0], []
        else:
            buf.append(line.strip())
    if name:
        seqs[name] = "".join(buf)
    return seqs


def write_fasta(seqs, path):
    with open(path, "w") as fh:
        for k in sorted(seqs):
            fh.write(">%s\n" % k)
            for i in range(0, len(seqs[k]), 60):
                fh.write(seqs[k][i:i + 60] + "\n")


def pick_reference(members):
    """Group medoid by mash, tie-broken by fewest contigs, as the pipeline's
    SELECT_UNIT_MEDOID does."""
    listfile = os.path.join(WORK, "medoid.txt")
    with open(listfile, "w") as fh:
        for m in members:
            fh.write(os.path.join(ASSEMBLIES, m + ".fasta") + "\n")
    sk = os.path.join(WORK, "medoid")
    subprocess.run(["mash", "sketch", "-p", str(THREADS), "-s", "50000",
                    "-o", sk, "-l", listfile], capture_output=True, check=True)
    out = subprocess.run(["mash", "dist", "-p", str(THREADS),
                          sk + ".msh", sk + ".msh"],
                         capture_output=True, text=True, check=True).stdout
    tot = {m: 0.0 for m in members}
    for line in out.splitlines():
        a, b, d = line.split("\t")[:3]
        tot[os.path.basename(a)[:-6]] += float(d)
    contigs = {m: sum(1 for line in open(os.path.join(ASSEMBLIES, m + ".fasta"))
                      if line.startswith(">")) for m in members}
    return min(members, key=lambda m: (round(tot[m], 6), contigs[m], m))


def do_group(g):
    name = g["name"]
    members = g["members"]
    gdir = os.path.join(WORK, name)
    os.makedirs(gdir, exist_ok=True)
    done = os.path.join(gdir, "DONE")
    if os.path.exists(done):
        print("[%s] already complete" % name, flush=True)
        return True

    ref = g.get("reference") or pick_reference(members)
    g["reference"] = ref
    refpath = os.path.join(gdir, "ref.fa")
    if not os.path.exists(refpath):
        shutil.copy(os.path.join(ASSEMBLIES, ref + ".fasta"), refpath)
    print("[%s] n=%d reference=%s" % (name, len(members), ref), flush=True)

    # 1. snippy per genome
    sdir = os.path.join(gdir, "snippy")
    os.makedirs(sdir, exist_ok=True)
    for i, m in enumerate(members, 1):
        outdir = os.path.join(sdir, m)
        if os.path.exists(os.path.join(outdir, "snps.aligned.fa")):
            continue
        p = run(["snippy", "--outdir", outdir, "--ref", refpath,
                 "--ctgs", os.path.join(ASSEMBLIES, m + ".fasta"),
                 "--cpus", str(THREADS), "--force"],
                cwd=gdir, bin_dir=SNIPPY_BIN,
                log=os.path.join(gdir, "snippy_%s.log" % m))
        if p.returncode != 0:
            print("[%s] snippy FAILED on %s" % (name, m), flush=True)
            return False
        print("[%s]   snippy %d/%d %s" % (name, i, len(members), m), flush=True)

    # 2. snippy-core -> whole-genome alignment
    full = os.path.join(gdir, name + ".full.aln")
    if not os.path.exists(full):
        p = run(["snippy-core", "--ref", refpath, "--prefix", name]
                + [os.path.join(sdir, m) for m in members],
                cwd=gdir, bin_dir=SNIPPY_BIN,
                log=os.path.join(gdir, "snippy_core.log"))
        if p.returncode != 0 or not os.path.exists(full):
            print("[%s] snippy-core FAILED" % name, flush=True)
            return False

    # 3. drop the duplicated Reference record
    aln = os.path.join(gdir, name + ".core.full.aln")
    if not os.path.exists(aln):
        seqs = read_fasta(full)
        seqs.pop("Reference", None)
        write_fasta(seqs, aln)
        print("[%s] alignment %d taxa x %d bp"
              % (name, len(seqs), len(next(iter(seqs.values())))), flush=True)

    # 4. Gubbins, in its own cwd
    gb = os.path.join(gdir, "gubbins")
    os.makedirs(gb, exist_ok=True)
    filt = os.path.join(gb, name + ".filtered_polymorphic_sites.fasta")
    if not os.path.exists(filt):
        local = os.path.join(gb, os.path.basename(aln))
        if not os.path.exists(local):
            shutil.copy(aln, local)
        p = run(["run_gubbins.py", "--prefix", name,
                 "--tree-builder", "raxml",
                 "--iterations", str(GUBBINS_ITERATIONS),
                 "--min-snps", str(GUBBINS_MIN_SNPS),
                 "--invariant-site-correction",
                 "--filter-percentage", str(GUBBINS_FILTER_PCT),
                 "--seed", str(SEED),
                 "--threads", str(THREADS),
                 os.path.basename(local)],
                cwd=gb, bin_dir=GUBBINS_BIN,
                log=os.path.join(gdir, "gubbins.log"))
        if not os.path.exists(filt):
            print("[%s] gubbins FAILED (rc=%d), see gubbins.log"
                  % (name, p.returncode), flush=True)
            return False

    # 5. IQ-TREE on the recombination-filtered variant sites
    tre = os.path.join(gb, name + ".final.treefile")
    if not os.path.exists(tre):
        for model in ("GTR+ASC", "GTR+G"):
            p = run(["iqtree2", "-s", os.path.basename(filt), "-st", "DNA",
                     "-m", model, "-T", str(THREADS),
                     "--prefix", name + ".final", "-bb", "1000", "-alrt",
                     "1000", "-redo"],
                    cwd=gb, bin_dir=GUBBINS_BIN,
                    log=os.path.join(gdir, "iqtree_%s.log" % model[:3]))
            if os.path.exists(tre):
                g["tree_model"] = model
                break
        if not os.path.exists(tre):
            print("[%s] iqtree FAILED" % name, flush=True)
            return False

    open(done, "w").write(ref + "\n")
    print("[%s] complete" % name, flush=True)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--groups", default="all",
                    help="comma separated group names, or 'all'")
    args = ap.parse_args()
    os.makedirs(WORK, exist_ok=True)
    state = json.load(open(GROUPS_JSON))
    groups = state["groups"]
    if args.groups != "all":
        want = set(args.groups.split(","))
        groups = [g for g in groups if g["name"] in want]
    ok = True
    for g in groups:
        if not do_group(g):
            ok = False
    json.dump(state, open(GROUPS_JSON, "w"), indent=1)
    print("finished; all groups ok" if ok else "finished WITH FAILURES")


if __name__ == "__main__":
    main()
