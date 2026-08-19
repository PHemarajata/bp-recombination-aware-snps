#!/usr/bin/env python3
"""Measure true within-cluster core-SNP diversity directly, replacing the Mash proxy.

WHY. `cluster_diversity_bp.py` estimates diversity as mean_mash * 3,805,619.
Four clusters have now been measured against real alignments (Appendix A.5/A.6)
and the proxy does not merely mis-scale, it MIS-RANKS:

    cluster        mean_mash    proxy   measured   bias
    cluster_53      0.000595     2263        535   4.23x
    cluster_16      0.001288     4903       3639   1.35x
    cluster_8       0.002147     8172       9252   0.88x
    cluster_0       0.003368    12818       9433   1.36x

cluster_8 and cluster_0 differ 1.6-fold in Mash distance and have essentially
the same true diversity. So Mash cannot be used to triage clusters by diversity,
nor to target a cluster of a wanted diversity -- two selection attempts using it
missed by 1.9x and 2.1x.

WHAT THIS DOES INSTEAD. `ska build` + `ska distance` gives pairwise SNP
distances directly from split k-mers: no reference, no alignment, no Gubbins.
That is minutes per cluster rather than the ~90 minutes a full 12-arm
reference-sensitivity run costs, so all 91 multi-genome clusters are affordable.

CALIBRATE BEFORE TRUSTING. `--validate` scores the four measured anchors and
sweeps --min-freq, because `ska distance` with min-freq 0 counts k-mers present
in any pair, whereas the anchors were measured on a CORE alignment. Pick the
min-freq that reproduces the anchors, then use it for the sweep. Do not skip
this step -- that is the mistake that produced the Mash proxy's credibility.

Usage:
    python3 measure_diversity_bp.py --validate [--threads 8]
    python3 measure_diversity_bp.py --cluster-list FILE --label NAME [--min-freq 0.9]
    python3 measure_diversity_bp.py --all --membership FILE --fasta-dir DIR
    python3 measure_diversity_bp.py --selftest
"""

import argparse
import csv
import os
import statistics
import subprocess
import sys
import tempfile

# Measured whole-genome mean pairwise SNPs, from the close-reference arms.
ANCHORS = {
    "cluster_53": 535.0,
    "cluster_16": 3639.0,
    "cluster_8": 9252.0,
    "cluster_0": 9433.0,
}
CONDA_SH = "/home/phemarajata/miniforge3/etc/profile.d/conda.sh"
ENV = "bp-gubbins"


def _bash(script):
    """Run a snippet under a shell that has sourced conda.sh.

    `conda` is not on PATH in a non-login shell and the failure is a bare
    exit 127 (handoff trap 11), so source it explicitly every time.
    """
    full = ("set +u; . {conda}; conda activate {env}; set -u\n".format(
        conda=CONDA_SH, env=ENV) + script)
    p = subprocess.run(["bash", "-c", full], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("failed (%d):\n%s" % (p.returncode, p.stderr[-2000:]))
    return p


def build_skf(list_file, workdir, threads):
    """`ska build` -- the expensive step. Cache and reuse across min-freq values."""
    skf = os.path.join(workdir, "cluster")
    if not os.path.exists(skf + ".skf"):
        _bash("ska build -o {skf} -f {lst} -k 31 --threads {th}\n".format(
            skf=skf, lst=list_file, th=threads))
        if not os.path.exists(skf + ".skf"):
            raise RuntimeError("ska build produced no .skf at %s.skf" % skf)
    return skf + ".skf"


def run_distance(skf, workdir, min_freq, threads):
    """`ska distance` -- cheap, and the only step min-freq affects."""
    dist = os.path.join(workdir, "distances_mf%s.tsv" % str(min_freq).replace(".", "p"))
    _bash("ska distance -o {dist} --min-freq {mf} --threads {th} {skf}\n".format(
        dist=dist, mf=min_freq, th=threads, skf=skf))
    if not os.path.exists(dist):
        raise RuntimeError("ska distance produced no output at %s" % dist)
    return dist


def parse_distances(path):
    """Pull the SNP-distance column out of `ska distance` output.

    ska 0.5.0 writes a header; the SNP-distance column is named like
    'distance' or 'snps'/'mismatches'. Resolve by name, never by index, since
    column order is not part of the interface.
    """
    with open(path) as fh:
        rdr = csv.reader(fh, delimiter="\t")
        header = next(rdr)
        low = [h.strip().lower() for h in header]
        col = None
        for want in ("snps", "snp_distance", "distance", "mismatches"):
            if want in low:
                col = low.index(want)
                break
        if col is None:
            raise RuntimeError("no SNP-distance column in %r" % (header,))
        vals = []
        for row in rdr:
            if len(row) <= col:
                continue
            try:
                vals.append(float(row[col]))
            except ValueError:
                continue
    return vals


def summarise(vals):
    if not vals:
        return None
    vals_sorted = sorted(vals)
    return {
        "n_pairs": len(vals),
        "mean": sum(vals) / len(vals),
        "median": statistics.median(vals_sorted),
        "max": vals_sorted[-1],
    }


def measure(list_file, min_freq, threads, workdir=None):
    """One (cluster, min-freq) measurement. Pass workdir to reuse a built .skf."""
    own = workdir is None
    wd = workdir or tempfile.mkdtemp(prefix="skadiv_")
    try:
        skf = build_skf(list_file, wd, threads)
        return summarise(parse_distances(run_distance(skf, wd, min_freq, threads)))
    finally:
        if own:
            _rmtree(wd)


def _rmtree(wd):
    for root, dirs, files in os.walk(wd, topdown=False):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            os.rmdir(os.path.join(root, d))
    os.rmdir(wd)


def validate(threads, freqs):
    """Sweep --min-freq against the measured anchors, building each .skf ONCE."""
    print("Calibrating `ska distance` against %d measured anchors." % len(ANCHORS))
    print("Target = whole-genome mean pairwise SNPs from the close-reference arms.")
    print("`ska build` runs once per cluster; only `ska distance` repeats.\n")

    ordered = sorted(ANCHORS.items(), key=lambda kv: kv[1])
    results = {}   # (cluster, mf) -> mean
    for cl, truth in ordered:
        lst = "cluster_metadata_%s_genomes.tsv" % cl
        if not os.path.exists(lst):
            print("  %-12s SKIPPED (no %s)" % (cl, lst))
            continue
        wd = tempfile.mkdtemp(prefix="skadiv_%s_" % cl)
        try:
            build_skf(lst, wd, threads)
            for mf in freqs:
                try:
                    st = measure(lst, mf, threads, workdir=wd)
                    results[(cl, mf)] = st["mean"] if st else None
                except RuntimeError as exc:
                    print("  %s @ min-freq %s FAILED: %s" % (cl, mf, str(exc)[:160]))
                    results[(cl, mf)] = None
            got = [results.get((cl, mf)) for mf in freqs]
            print("  %-12s truth %6.0f | %s" % (cl, truth, "  ".join(
                "mf%s: %s" % (mf, ("%.0f" % g) if g else "-")
                for mf, g in zip(freqs, got))))
        finally:
            _rmtree(wd)

    print("\nRatio to truth (want tight around 1.00 across ALL anchors):")
    hdr = ("%-10s" % "min-freq" + "".join("%12s" % cl.replace("cluster_", "c")
                                          for cl, _ in ordered)
           + "%10s%10s" % ("spread", "worst"))
    print(hdr)
    print("-" * len(hdr))
    best = None
    for mf in freqs:
        ratios = []
        cells = []
        for cl, truth in ordered:
            g = results.get((cl, mf))
            if g:
                ratios.append(g / truth)
                cells.append("%12.2f" % (g / truth))
            else:
                cells.append("%12s" % "-")
        # Score on WORST deviation from 1.0, not on spread. Spread alone rewards
        # a setting that is uniformly biased -- min-freq 1.0 scored "tightest"
        # while underestimating every anchor by 14-28%.
        worst = max(abs(r - 1.0) for r in ratios) if ratios else float("inf")
        spread = (max(ratios) / min(ratios)) if len(ratios) >= 2 and min(ratios) > 0 else float("inf")
        print("%-10s%s%10s%10s" % (mf, "".join(cells),
                                   "%.2f" % spread if spread != float("inf") else "-",
                                   "%+.0f%%" % (100 * worst) if worst != float("inf") else "-"))
        if len(ratios) == len(ordered) and worst < (best[1] if best else float("inf")):
            best = (mf, worst)

    print()
    if best:
        print("Best by WORST deviation: min-freq %s (worst anchor off by %.0f%%)." % (best[0], 100 * best[1]))
        print("Adopt it only if that worst deviation is acceptable AND the ratios do not")
        print("drift monotonically with cluster size -- drift means the statistic is still")
        print("not core. Scatter without drift is residual noise and is tolerable.")
    else:
        print("No min-freq produced a value for every anchor; cannot calibrate.")
    return 0



def sweep_all(membership, fasta_dir, out_path, min_freq, threads, min_n=2):
    """Measure every multi-genome cluster. Resumable, and failure-isolated.

    Incremental append with a flush per cluster, so a crash three hours in
    keeps everything already measured. Re-running skips clusters already
    present in out_path. One cluster that fails is logged and skipped rather
    than aborting the other ninety (handoff trap 7).
    """
    members = {}
    with open(membership) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            members.setdefault(r["cluster_id"], []).append(r["sample_id"])
    targets = {c: ids for c, ids in members.items() if len(ids) >= min_n}

    done = set()
    if os.path.exists(out_path):
        with open(out_path) as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                if (r.get("status") or "") == "ok":
                    done.add(r["cluster_id"])
        print("resuming: %d of %d clusters already measured" % (len(done), len(targets)))

    todo = [c for c in sorted(targets, key=lambda c: -len(targets[c])) if c not in done]
    print("measuring %d clusters at --min-freq %s, %d threads\n" % (len(todo), min_freq, threads))

    new_file = not os.path.exists(out_path)
    with open(out_path, "a") as out:
        if new_file:
            out.write("cluster_id\tn\tn_pairs\tmean_snps\tmedian_snps\tmax_snps\tstatus\n")
            out.flush()
        for i, cl in enumerate(todo, 1):
            ids = targets[cl]
            lst = None
            try:
                with tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False) as fh:
                    n_ok = 0
                    for sid in ids:
                        fa = os.path.join(fasta_dir, sid + ".fasta")
                        if os.path.exists(fa):
                            fh.write("%s\t%s\n" % (sid, fa))
                            n_ok += 1
                    lst = fh.name
                if n_ok < min_n:
                    out.write("%s\t%d\t\t\t\t\tno_fasta\n" % (cl, len(ids)))
                    out.flush()
                    print("  [%3d/%3d] %-14s SKIP (only %d fasta found)" % (i, len(todo), cl, n_ok))
                    continue
                st = measure(lst, min_freq, threads)
                if not st:
                    raise RuntimeError("no distances produced")
                out.write("%s\t%d\t%d\t%.2f\t%.2f\t%.2f\tok\n"
                          % (cl, n_ok, st["n_pairs"], st["mean"], st["median"], st["max"]))
                out.flush()
                print("  [%3d/%3d] %-14s n=%-4d mean=%9.1f median=%9.1f max=%9.1f"
                      % (i, len(todo), cl, n_ok, st["mean"], st["median"], st["max"]))
            except Exception as exc:
                out.write("%s\t%d\t\t\t\t\tFAILED\n" % (cl, len(ids)))
                out.flush()
                print("  [%3d/%3d] %-14s FAILED: %s" % (i, len(todo), cl, str(exc)[:140]))
            finally:
                if lst and os.path.exists(lst):
                    os.unlink(lst)

    print("\nwrote %s" % out_path)
    return 0



def modality(d):
    """Structure metrics on a sorted pairwise-distance list (A.9 Finding 3).

    mean/median and their ratio CANNOT detect a mixture: cluster_48 has
    mean 4,562 vs median 4,581 and is three sub-lineages. These two can.

      gap_over_mean : largest gap inside the middle 90% of the distribution,
                      divided by the mean. Big gap => distinct sub-populations.
      empty_bins    : 20-bin histogram bins holding <2% of pairs.

    Reference points, chr1 alignments: cluster_16 (continuous, the one cluster
    where recombination inference worked) 0.043 / 4-of-20; cluster_48 (three
    sub-lineages) 0.128 / 12-of-20; cluster_5 (rejected) 0.399 / 5-of-20.
    """
    if len(d) < 20:
        return None
    mean = sum(d) / len(d)
    mn, mx = d[0], d[-1]
    core = d[int(0.05 * len(d)):int(0.95 * len(d))]
    gap = max(core[i + 1] - core[i] for i in range(len(core) - 1)) if len(core) > 1 else 0.0
    # Bin over the OBSERVED range, not 0..max. Binning from zero puts every
    # low bin out of reach for a cluster with no near-identical pairs and
    # falsely flags it as a mixture -- caught by selftest, not by inspection.
    nb = 20
    span = mx - mn
    hist = [0] * nb
    for x in d:
        hist[min(nb - 1, int(nb * (x - mn) / span)) if span else 0] += 1
    empty = sum(1 for h in hist if h < 0.02 * len(d))
    return {"gap": gap, "gap_over_mean": (gap / mean) if mean else float("nan"),
            "empty_bins": empty, "mean": mean,
            "median": d[len(d) // 2], "max": mx}


# A cluster is a MIXTURE if EITHER statistic fires. CALIBRATED 2026-08-11 by
# subsampling 7 continuous + 3 mixture clusters -- ALL inside the operating
# range -- down to smaller n, 25 reps per size (Appendix A.11f,
# `validate_modality_bp.py`).
#
# TWO statistics are required; neither alone suffices:
#   gap/mean   tight core + outliers: one big gap over a SMALL mean.
#              cluster_53 = 1.55, s1_L1_5 = 6.71
#   empty_bins several clumps over a WIDE range: each gap small relative to a
#              LARGE mean, so gap/mean misses it. cluster_48 is 4-modal yet
#              scores gap/mean 0.128; empty_bins 0.60 catches it.
#
# Measured: 100% of mixtures caught from n=25 up, ~15-21% false-mixture rate.
# That asymmetry is deliberate -- a mixture slipping through is caught
# downstream by r/m (bridged clusters give 0.94-1.49), whereas a wrongly
# rejected continuous cluster is a SILENT loss.
#
# Superseded values: MIX_GAP was 0.09 with n>=30 (A.11b), which rejected
# essentially everything small, and empty_bins had been dropped as
# non-discriminating. Both errors came from panels containing OUT-OF-RANGE
# clusters.
MIX_GAP = 1.0
MIX_EMPTY = 0.45
MIN_N_MODALITY = 25   # below this the two classes overlap at every threshold


def is_mixture(m, n=None):
    """Flag a mixture. Returns True/False, or None when n is below the floor.

    ORDER MATTERS: apply the DIVERSITY gate first. gap/mean divides by the mean,
    so on a very tight cluster one divergent genome yields an enormous ratio --
    which is exactly how the first calibration attempt failed (A.11f).
    """
    if n is not None and n < MIN_N_MODALITY:
        return None
    return m["gap_over_mean"] > MIX_GAP or (m["empty_bins"] / 20.0) > MIX_EMPTY


def screen_all(membership, fasta_dir, out_path, min_freq, threads, min_n=20):
    """Modality-screen every cluster with >= min_n genomes. Resumable."""
    members = {}
    with open(membership) as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            members.setdefault(r["cluster_id"], []).append(r["sample_id"])
    refs = {}
    if os.path.exists("cluster_references.tsv"):
        with open("cluster_references.tsv") as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                refs[r["cluster_id"]] = r.get("status", "")
    targets = {c: ids for c, ids in members.items() if len(ids) >= min_n}

    done = set()
    if os.path.exists(out_path):
        with open(out_path) as fh:
            for r in csv.DictReader(fh, delimiter="\t"):
                done.add(r["cluster_id"])
        print("resuming: %d already screened" % len(done))
    todo = [c for c in sorted(targets, key=lambda c: -len(targets[c])) if c not in done]
    print("screening %d clusters (n >= %d), %d threads\n" % (len(todo), min_n, threads))

    new = not os.path.exists(out_path)
    with open(out_path, "a") as out:
        if new:
            out.write("cluster_id\tn\tref_status\tmean_snps\tmedian_snps\tmax_snps\t"
                      "gap\tgap_over_mean\tempty_bins\tstructure\tusable_testcase\n")
            out.flush()
        for i, cl in enumerate(todo, 1):
            lst = None
            try:
                with tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False) as fh:
                    k = 0
                    for sid in targets[cl]:
                        fa = os.path.join(fasta_dir, sid + ".fasta")
                        if os.path.exists(fa):
                            fh.write("%s\t%s\n" % (sid, fa)); k += 1
                    lst = fh.name
                if k < min_n:
                    print("  [%3d/%3d] %-14s SKIP (%d fasta)" % (i, len(todo), cl, k)); continue
                wd = tempfile.mkdtemp(prefix="scr_")
                try:
                    skf = build_skf(lst, wd, threads)
                    d = sorted(parse_distances(run_distance(skf, wd, min_freq, threads)))
                finally:
                    _rmtree(wd)
                m = modality(d)
                if not m:
                    print("  [%3d/%3d] %-14s SKIP (too few pairs)" % (i, len(todo), cl)); continue
                mix = is_mixture(m, k)
                st = refs.get(cl, "")
                if mix is None:
                    usable = "no"      # too small to judge, not judged bad
                else:
                    usable = "yes" if (not mix and st == "ready") else "no"
                out.write("%s\t%d\t%s\t%.1f\t%.1f\t%.1f\t%.0f\t%.4f\t%d\t%s\t%s\n"
                          % (cl, k, st, m["mean"], m["median"], m["max"], m["gap"],
                             m["gap_over_mean"], m["empty_bins"],
                             ("undecidable" if mix is None else
                              ("mixture" if mix else "continuous")), usable))
                out.flush()
                print("  [%3d/%3d] %-14s n=%-3d mean=%8.0f gap/mean=%.3f empty=%2d/20 %-11s %s"
                      % (i, len(todo), cl, k, m["mean"], m["gap_over_mean"],
                         m["empty_bins"],
                         ("undecidable" if mix is None else
                          ("mixture" if mix else "continuous")),
                         "USABLE" if usable == "yes" else ""))
            except Exception as exc:
                print("  [%3d/%3d] %-14s FAILED: %s" % (i, len(todo), cl, str(exc)[:120]))
            finally:
                if lst and os.path.exists(lst):
                    os.unlink(lst)
    print("\nwrote %s" % out_path)
    return 0


def selftest():
    fails = []

    st = summarise([1.0, 2.0, 3.0, 10.0])
    if st["n_pairs"] != 4:
        fails.append("n_pairs")
    if abs(st["mean"] - 4.0) > 1e-9:
        fails.append("mean: got %r" % st["mean"])
    if abs(st["median"] - 2.5) > 1e-9:
        fails.append("median: got %r" % st["median"])
    if abs(st["max"] - 10.0) > 1e-9:
        fails.append("max")
    if summarise([]) is not None:
        fails.append("empty should be None")

    # column resolution must be by NAME, and tolerate reordering
    for header, want in ((["sample1", "sample2", "distance"], 5.0),
                         (["sample1", "sample2", "snps", "mismatches"], 5.0),
                         (["snps", "sample1", "sample2"], 5.0)):
        with tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False) as fh:
            fh.write("\t".join(header) + "\n")
            row = ["a"] * len(header)
            idx = [h.lower() for h in header].index("snps" if "snps" in header else "distance")
            row[idx] = "5.0"
            fh.write("\t".join(row) + "\n")
            p = fh.name
        got = parse_distances(p)
        os.unlink(p)
        if got != [want]:
            fails.append("column resolution for %r: got %r" % (header, got))

    # a header with no recognisable distance column must raise, not guess
    with tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False) as fh:
        fh.write("a\tb\tc\n1\t2\t3\n")
        p = fh.name
    try:
        parse_distances(p)
        fails.append("unknown header should raise")
    except RuntimeError:
        pass
    os.unlink(p)

    # modality: a clean unimodal spread must not be flagged
    uni = sorted(1000 + (i % 200) for i in range(400))
    m = modality(uni)
    if is_mixture(m):
        fails.append("unimodal spread misflagged as mixture (gap/mean %.3f)"
                     % m["gap_over_mean"])
    # the seven calibration clusters must all classify correctly (ska scale)
    # cluster_48: 4-modal, gap/mean 0.128 (BELOW threshold) but empty 12/20.
    # gap/mean ALONE would pass it -- empty_bins must catch it.
    if is_mixture({"gap_over_mean": 0.128, "empty_bins": 12}, 50) is not True:
        fails.append("cluster_48 must be caught by empty_bins")
    if is_mixture({"gap_over_mean": 0.128, "empty_bins": 4}, 50) is not False:
        fails.append("low gap AND few empty bins must be continuous")
    # cluster_53: tight core + outliers, caught by gap/mean
    if is_mixture({"gap_over_mean": 1.549, "empty_bins": 15}, 49) is not True:
        fails.append("cluster_53 must be caught by gap/mean")
    # known continuous full-size values must pass
    for gm, eb in ((0.004, 1), (0.041, 8), (0.067, 5)):
        if is_mixture({"gap_over_mean": gm, "empty_bins": eb}, 50) is not False:
            fails.append("continuous (gap %.3f, empty %d) misclassified" % (gm, eb))
    # below the size floor the answer is UNDECIDABLE, not "mixture"
    if is_mixture({"gap_over_mean": 5.0, "empty_bins": 18}, 12) is not None:
        fails.append("n<%d must return None, not a verdict" % MIN_N_MODALITY)
    # modality: two well-separated clumps must be flagged
    bi = sorted([100 + (i % 50) for i in range(200)] + [5000 + (i % 50) for i in range(200)])
    if not is_mixture(modality(bi)):
        fails.append("bimodal distribution not flagged as mixture")
    # mean==median must NOT rescue a mixture (the cluster_48 trap)
    mm = modality(bi)
    if abs(mm["mean"] - 2575) > 200:
        fails.append("bimodal mean sanity: got %r" % mm["mean"])
    if modality([1, 2, 3]) is not None:
        fails.append("too-few-pairs should return None")

    if fails:
        print("SELFTEST FAILED (%d)" % len(fails))
        for f in fails:
            print("  " + f)
        return 1
    print("selftest: 24/24 checks passed")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cluster-list")
    ap.add_argument("--label", default="cluster")
    ap.add_argument("--min-freq", type=float, default=0.0,
                    help="CALIBRATED default: 0.0 (all four anchors within 13%%)")
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--all", action="store_true",
                    help="measure every multi-genome cluster")
    ap.add_argument("--screen-all", action="store_true",
                    help="modality-screen every cluster with n>=20 (A.9 Finding 3)")
    ap.add_argument("--min-n", type=int, default=20)
    ap.add_argument("--membership",
                    default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "inputs", "cluster_membership_2802.tsv"),
                    help="local canonical copy; the original pipeline path vanished 2026-08-10")
    ap.add_argument("--fasta-dir",
                    default="/home/phemarajata/Downloads/final_deduped_all_BP_with_locations")
    ap.add_argument("--out", default="cluster_diversity_measured.tsv")
    ap.add_argument("--freqs", default="0.0,0.5,0.9,0.95,1.0",
                    help="min-freq values to sweep in --validate")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if args.validate:
        return validate(args.threads, [f.strip() for f in args.freqs.split(",")])
    if args.all:
        return sweep_all(args.membership, args.fasta_dir, args.out,
                         args.min_freq, args.threads)
    if args.screen_all:
        out = args.out if args.out != "cluster_diversity_measured.tsv" else "cluster_modality.tsv"
        return screen_all(args.membership, args.fasta_dir, out,
                          args.min_freq, args.threads, args.min_n)
    if not args.cluster_list:
        ap.error("need --cluster-list, or --validate, or --selftest")

    st = measure(args.cluster_list, args.min_freq, args.threads)
    if not st:
        print("no distances produced", file=sys.stderr)
        return 2
    print("%s\tpairs=%d\tmean=%.1f\tmedian=%.1f\tmax=%.1f"
          % (args.label, st["n_pairs"], st["mean"], st["median"], st["max"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
