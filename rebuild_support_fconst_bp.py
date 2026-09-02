#!/usr/bin/env python3
"""
Rebuild the per-unit support trees with `-fconst` instead of `GTR+ASC`.

WHY. Production built the final per-unit trees under `GTR+ASC`
(`conf/params.config`: `iqtree_model = "GTR+ASC"`, `iqtree_fconst = null`), and
the support trees generated on 2026-08-23 inherited that from each unit's ASC
preflight. Measured on two units (`ASC_FCONST_RESULT_2026-08-23.md`), `+ASC`
estimates base composition at **54.5-58.9% GC against a true 68.1%**, while
`-fconst` with true counts returns 67.8-68.0%. Branch lengths are also per
VARIABLE site under `+ASC` rather than per site.

Neither affects a reported number -- every quantity in the paper derives from
Gubbins outputs, and the IQ-TREE tree is read only by archive/export scripts --
but a published supplementary tree estimating 55% GC in a 68% GC organism is
indefensible, so the deliverable is rebuilt.

CONSTANT-SITE COUNTS are tallied PERMISSIVELY from each replicon-unit's own
`.core.full.aln`: a column counts as constant if the A/C/G/T characters present
are all one base, ignoring N and gaps. This is the definition Methods 2.5
specifies ("-fconst supplied from the full alignment") and the one the
calibration track used. `constant_sites_sensitivity_bp.py` shows the per-taxon
MASKED count is arguably more honest but not material for relative quantities;
the union count is a documented trap and is not used.

⚠ TWO TRAPS THIS SCRIPT AVOIDS, both of which bit during development:

  1. `L1v4c_out/Clusters` is HYBRID -- 176 dirs = 88 units x 2 replicons, of
     which only 85 units / 170 replicon-units are in the frozen basis. Membership
     is taken from FINAL_PARTITION.tsv and the script refuses to run otherwise.
  2. Globbing `<unit>__*.core.full.aln` matches BOTH replicons and returns them
     in arbitrary order. Constant counts must come from the SAME replicon-unit as
     the alignment being fitted. Paths here are constructed exactly, never
     globbed by unit alone.

  ./rebuild_support_fconst_bp.py
  FORKS=4 THREADS=4 ./rebuild_support_fconst_bp.py
"""
import csv
import glob
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor

import numpy as np

B = os.path.dirname(os.path.abspath(__file__))
CLUSTERS = f"{B}/L1v4c_out/Clusters"
PARTITION = f"{B}/FINAL_BASIS_2026-08-22/FINAL_PARTITION.tsv"
OUT = os.environ.get("OUT", f"{B}/L1v4c_TREES_SUPPORTED_FCONST")
IMG = "quay.io/biocontainers/iqtree:2.2.6--h21ec9f0_0"
UFBOOT = int(os.environ.get("UFBOOT", 1000))
ALRT = int(os.environ.get("ALRT", 1000))
FORKS = int(os.environ.get("FORKS", 4))
THREADS = int(os.environ.get("THREADS", 4))
SEED = int(os.environ.get("SEED", 20260823))
LOG = f"{B}/SUPPORT_TREES_FCONST.log"


def constant_counts(path):
    """Permissive constant-site tally: A,C,G,T. Ignores N and gaps."""
    seqs, cur = [], []
    with open(path, "rb") as fh:
        for line in fh:
            if line.startswith(b">"):
                if cur:
                    seqs.append(b"".join(cur))
                    cur = []
            else:
                cur.append(line.strip().upper())
    if cur:
        seqs.append(b"".join(cur))
    M = np.frombuffer(b"".join(seqs), dtype=np.uint8).reshape(len(seqs), -1)
    has = {b: (M == b).any(axis=0) for b in b"ACGT"}
    mono = sum(has[b].astype(np.int8) for b in b"ACGT") == 1
    return [int((mono & has[b]).sum()) for b in b"ACGT"], M.shape


def run_one(args):
    d, unit = args
    aln = f"{d}/Gubbins/{unit}.filtered_polymorphic_sites.fasta"
    full = f"{d}/{unit}.core.full.aln"
    if not (os.path.getsize(aln) if os.path.exists(aln) else 0):
        return f"SKIP {unit}: no filtered alignment"
    if not os.path.exists(full):
        return f"SKIP {unit}: no core.full.aln (cannot derive -fconst)"

    # taxon count from the preflight guard used by the ASC run
    pre = f"{d}/{unit}.asc_preflight.txt"
    ntax = 0
    if os.path.exists(pre):
        for line in open(pre):
            if line.startswith("N_TAXA="):
                ntax = int(line.strip().split("=")[1] or 0)
    if ntax and ntax < 4:
        return f"SKIP {unit}: N_TAXA={ntax} (<4, no supportable topology)"

    try:
        counts, shape = constant_counts(full)
    except Exception as e:
        return f"FAIL {unit}: constant-count error {e}"
    if sum(counts) == 0:
        return f"SKIP {unit}: zero constant sites in the full alignment"

    work = f"{OUT}/{unit}"
    os.makedirs(work, exist_ok=True)
    subprocess.run(["cp", aln, f"{work}/aln.fasta"], check=True)
    cmd = ["docker", "run", "--rm", "-v", f"{work}:/d", "-w", "/d",
           "-u", f"{os.getuid()}:{os.getgid()}", IMG,
           "iqtree2", "-s", "aln.fasta", "-st", "DNA",
           "-m", "GTR", "-fconst", ",".join(map(str, counts)),
           "-T", str(THREADS), "-seed", str(SEED),
           "--prefix", "supported", "-bb", str(UFBOOT), "-alrt", str(ALRT)]
    with open(f"{work}/iqtree.stdout", "w") as fh:
        rc = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT).returncode
    tre = f"{work}/supported.treefile"
    if rc == 0 and os.path.exists(tre) and os.path.getsize(tre):
        subprocess.run(["cp", tre, f"{OUT}/{unit}.support.treefile"], check=True)
        iq = f"{work}/supported.iqtree"
        if os.path.exists(iq):
            subprocess.run(["cp", iq, f"{OUT}/{unit}.support.iqtree"], check=True)
        subprocess.run(["rm", "-rf", work], check=True)
        return (f"OK   {unit} (taxa={shape[0]}, const={sum(counts)}, "
                f"fconst={','.join(map(str, counts))})")
    return f"FAIL {unit} exit={rc} -- see {work}/iqtree.stdout"


def main():
    if not os.path.exists(PARTITION):
        sys.exit(f"no frozen partition at {PARTITION}")
    units = sorted({r["unit"] for r in
                    csv.DictReader(open(PARTITION), delimiter="\t")})
    if len(units) != 85:
        sys.exit(f"expected 85 frozen units, got {len(units)}")

    jobs = []
    for u in units:
        for d in sorted(glob.glob(f"{CLUSTERS}/cluster_{u}__*")):
            if os.path.isdir(d):
                jobs.append((d, os.path.basename(d).replace("cluster_", "")))
    if len(jobs) != 170:
        sys.exit(f"expected 170 replicon-units, got {len(jobs)}")

    os.makedirs(OUT, exist_ok=True)
    print(f"frozen units {len(units)}, replicon-units {len(jobs)}, "
          f"forks {FORKS} x {THREADS} threads -> {OUT}")
    with open(LOG, "w") as fh:
        fh.write(f"basis=FINAL_BASIS_2026-08-22 units={len(units)} "
                 f"replicon_units={len(jobs)} model=GTR+-fconst seed={SEED}\n")
    done = 0
    with ProcessPoolExecutor(max_workers=FORKS) as ex:
        for msg in ex.map(run_one, jobs):
            done += 1
            with open(LOG, "a") as fh:
                fh.write(msg + "\n")
            if done % 20 == 0 or msg.startswith(("FAIL", "SKIP")):
                print(f"  [{done}/{len(jobs)}] {msg}")
    txt = open(LOG).read()
    print(f"\nOK {txt.count(chr(10)+'OK')+txt.startswith('OK')}, "
          f"SKIP {txt.count('SKIP ')}, FAIL {txt.count('FAIL ')} of {len(jobs)}")


if __name__ == "__main__":
    main()
