#!/usr/bin/env python3
"""
Raw vs recombination-filtered pairwise SNP distances, per v4c replicon-unit.

Both external reviews of 2026-08-19 asked for the same thing: a single distance
number hides whether two genomes are close because they are related or because
Gubbins masked the genome out from under them. This emits both, plus the two
fractions needed to tell those apart.

Why this reads `.core.tab` and not the alignment
------------------------------------------------
The obvious route is mask_recombination.py over `<unit>.core.full.aln`, but that
means loading 25-648 MB per replicon-unit and writing a masked copy, on a volume
that is 94% full. It is unnecessary: `.core.tab` already holds every variant
site with per-taxon calls (370 KB against a 94 MB alignment on strain_4_L1_1),
and invariant sites contribute nothing to a pairwise SNP distance.

The three coordinate spaces were verified to coincide on strain_4_L1_1 chr1:
GFF `##sequence-region SEQUENCE 1 4046807`, alignment sequence length 4,046,807,
max `.core.tab` POS 4,046,592. All 1-based against the unit reference.

Two filtered distances, because masking is per-branch
----------------------------------------------------
Gubbins masks a position on the branches it was imported on, not globally, so
"the masked alignment" is not uniquely defined. Both are reported:

  per-taxon  the honest reading -- a site is ignored for a pair only if it was
             called recombinant in one of THAT pair's taxa. Matches what
             mask_recombination.py produces.
  global     conservative -- any site recombinant on >=1 branch is dropped for
             everybody. This is the denominator that also governs the constant
             site counts, so reporting it makes the sensitivity visible.

If the two disagree sharply the unit is one where masking is doing most of the
work, which is exactly the regime worth flagging.

Usage
-----
    recomb_filtered_distances_bp.py [--clusters DIR] [--out-dir DIR]
                                    [--summary FILE] [--unit SUBSTRING]
"""
import argparse
import collections
import csv
import glob
import os
import re
import sys

import numpy as np

B = os.path.dirname(os.path.abspath(__file__))
DEF_CLUSTERS = f"{B}/L1v4c_out/Clusters"


def parse_core_tab(path):
    """-> (taxa, positions int64[S], matrix uint8[T,S]). Alphabet is plain ATCG:
    keep_invariant_atcg guarantees it, so there is no ambiguity code to skip."""
    with open(path) as fh:
        header = fh.readline().rstrip("\n").split("\t")
        taxa = header[3:]
        pos, rows = [], []
        for line in fh:
            f = line.rstrip("\n").split("\t")
            if len(f) < 4:
                continue
            pos.append(int(f[1]))
            rows.append(f[3:])
    if not rows:
        return taxa, np.zeros(0, dtype=np.int64), np.zeros((len(taxa), 0), np.uint8)
    mat = np.array([[ord(c[0]) if c else 0 for c in r] for r in rows],
                   dtype=np.uint8).T          # -> taxa x sites
    return taxa, np.array(pos, dtype=np.int64), mat


GFF_TAXA = re.compile(r'taxa="([^"]*)"')


def parse_gff(path):
    """-> (intervals [(start, end, [taxon, ...])], seq_len)."""
    out, seq_len = [], 0
    if not os.path.isfile(path):
        return out, seq_len
    for line in open(path):
        if line.startswith("##sequence-region"):
            try:
                seq_len = int(line.split()[-1])
            except ValueError:
                pass
            continue
        if line.startswith("#"):
            continue
        f = line.rstrip("\n").split("\t")
        if len(f) < 9:
            continue
        m = GFF_TAXA.search(f[8])
        # taxa are space-separated; 123 of 188 intervals on strain_4_L1_1 carry
        # more than one, so this cannot be treated as a single name
        out.append((int(f[3]), int(f[4]), m.group(1).split() if m else []))
    return out, seq_len


def masked_bp(intervals, seq_len):
    """Union of recombinant intervals, in bp. Intervals overlap heavily, so this
    has to merge rather than sum -- summing double-counts and can exceed
    seq_len."""
    if not intervals:
        return 0
    spans = sorted((s, e) for s, e, _ in intervals)
    total, cur_s, cur_e = 0, *spans[0]
    for s, e in spans[1:]:
        if s > cur_e + 1:
            total += cur_e - cur_s + 1
            cur_s, cur_e = s, e
        else:
            cur_e = max(cur_e, e)
    return total + cur_e - cur_s + 1


def build_masks(taxa, pos, intervals):
    """-> (per_taxon bool[T,S], global bool[S]). True means 'recombinant here'."""
    T, S = len(taxa), len(pos)
    per = np.zeros((T, S), dtype=bool)
    glob_ = np.zeros(S, dtype=bool)
    idx = {t: i for i, t in enumerate(taxa)}
    for start, end, tx in intervals:
        lo = np.searchsorted(pos, start, "left")
        hi = np.searchsorted(pos, end, "right")
        if lo >= hi:
            continue
        glob_[lo:hi] = True
        for t in tx:
            i = idx.get(t)
            if i is not None:
                per[i, lo:hi] = True
    return per, glob_


def pairwise(mat, per=None, drop=None):
    """Pairwise SNP counts. `per` masks per-taxon, `drop` masks sites globally."""
    T, S = mat.shape
    keep = ~drop if drop is not None else np.ones(S, dtype=bool)
    d = np.zeros((T, T), dtype=np.int64)
    for i in range(T):
        for j in range(i + 1, T):
            ok = keep
            if per is not None:
                ok = ok & ~per[i] & ~per[j]
            n = int(np.count_nonzero((mat[i] != mat[j]) & ok))
            d[i, j] = d[j, i] = n
    return d


def tri(d):
    """Upper-triangle values as a flat array."""
    return d[np.triu_indices(d.shape[0], 1)] if d.shape[0] > 1 else np.zeros(0)


def stats(v):
    if v.size == 0:
        return {"median": "", "mean": "", "max": ""}
    return {"median": f"{np.median(v):.1f}", "mean": f"{v.mean():.1f}",
            "max": int(v.max())}


def write_matrix(path, taxa, d):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow([""] + taxa)
        for i, t in enumerate(taxa):
            w.writerow([t] + list(map(int, d[i])))


def load_rm(path):
    """unit -> corrected pooled r/m, if the v4c summary is present."""
    if not os.path.isfile(path):
        return {}
    out = {}
    for r in csv.DictReader(open(path), delimiter="\t"):
        try:
            out[r["unit"]] = float(r["rm_corrected"])
        except (KeyError, ValueError):
            pass
    return out


def callable_fraction(stats_path):
    """1 - max_column_missingness, read off the pipeline's own column filter."""
    if not os.path.isfile(stats_path):
        return ""
    for line in open(stats_path):
        if line.startswith("#max_column_missingness"):
            try:
                return f"{1.0 - float(line.split('\t')[1]):.4f}"
            except (IndexError, ValueError):
                return ""
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clusters", default=DEF_CLUSTERS)
    ap.add_argument("--out-dir", default=f"{B}/DISTANCES_v4c")
    ap.add_argument("--summary", default=f"{B}/DISTANCES_v4c_SUMMARY.tsv")
    ap.add_argument("--unit", help="only units whose dir name contains this")
    # E4. This was hardcoded to the reported run's table while every other input
    # was an argument, so running the script on a different run silently mixed
    # bases: unit_rm, expected_ratio_from_rm and ratio_over_expected came from
    # the reported run while every other column came from the new one. Same
    # class as E0 and E1: a default that points at a specific run.
    ap.add_argument("--rm", default=f"{B}/L1v4c_out/Summaries/recombination_rm.tsv",
                    help="r/m table; MUST come from the same run as --clusters")
    a = ap.parse_args()

    os.makedirs(a.out_dir, exist_ok=True)
    rm = load_rm(a.rm)
    rows = []
    dirs = sorted(glob.glob(os.path.join(a.clusters, "cluster_*")))
    if a.unit:
        dirs = [d for d in dirs if a.unit in os.path.basename(d)]

    for d in dirs:
        tab = glob.glob(f"{d}/*.core.tab")
        if not tab:
            print(f"  skip (no core.tab): {os.path.basename(d)}", file=sys.stderr)
            continue
        tab = tab[0]
        stem = os.path.basename(tab).replace(".core.tab", "")
        m = re.match(r"^(.*?)__(.*)_(\d+)$", stem)
        unit, replicon = (m.group(1), m.group(3)) if m else (stem, "")

        taxa, pos, mat = parse_core_tab(tab)
        intervals, seq_len = parse_gff(f"{d}/Gubbins/{stem}.recombination_predictions.gff")
        per, glob_ = build_masks(taxa, pos, intervals)

        d_raw = pairwise(mat)
        d_per = pairwise(mat, per=per)
        d_gl = pairwise(mat, drop=glob_)

        write_matrix(f"{a.out_dir}/{stem}.raw.tsv", taxa, d_raw)
        write_matrix(f"{a.out_dir}/{stem}.filtered_pertaxon.tsv", taxa, d_per)

        v_raw, v_per, v_gl = tri(d_raw), tri(d_per), tri(d_gl)
        s_raw, s_per, s_gl = stats(v_raw), stats(v_per), stats(v_gl)
        mbp = masked_bp(intervals, seq_len)
        ratio = (np.median(v_per) / np.median(v_raw)
                 if v_raw.size and np.median(v_raw) > 0 else "")

        rows.append({
            "unit": unit, "replicon": replicon, "n_taxa": len(taxa),
            "n_variant_sites": len(pos),
            "seq_len": seq_len, "n_recomb_intervals": len(intervals),
            "masked_bp": mbp,
            "masked_fraction": f"{mbp / seq_len:.4f}" if seq_len else "",
            "sites_recombinant_any_branch": int(glob_.sum()),
            "callable_fraction": callable_fraction(f"{d}/{stem}.column_filter.stats.tsv"),
            "raw_median": s_raw["median"], "raw_mean": s_raw["mean"], "raw_max": s_raw["max"],
            "filt_pertaxon_median": s_per["median"], "filt_pertaxon_mean": s_per["mean"],
            "filt_pertaxon_max": s_per["max"],
            "filt_global_median": s_gl["median"], "filt_global_mean": s_gl["mean"],
            "filt_global_max": s_gl["max"],
            "filtered_over_raw_median": f"{ratio:.4f}" if ratio != "" else "",
            # A pair's distance loses the SNPs that recombination brought in, so
            # filt/raw should track 1/(1+r/m). It does: rank correlation +0.75
            # across the 86 units. Observed sits ~1.75x below predicted because
            # per-taxon masking drops a site when EITHER member of the pair is
            # masked, which is more aggressive than r/m's per-branch accounting.
            # The RESIDUAL is the useful flag -- a raw threshold on filt/raw
            # catches 136 of 172 replicon-units, i.e. the normal state.
            #   >1  recombination is concentrated on few branches, most pairs spared
            #   <1  masking is hitting most pairs harder than the branch count implies
            "unit_rm": f"{rm[unit]:.4f}" if unit in rm else "",
            "expected_ratio_from_rm": f"{1 / (1 + rm[unit]):.4f}" if unit in rm else "",
            "ratio_over_expected": (f"{ratio * (1 + rm[unit]):.2f}"
                                    if unit in rm and ratio != "" else ""),
        })
        print(f"  {unit} rep{replicon}: n={len(taxa)} sites={len(pos)} "
              f"masked={mbp/seq_len:.1%} raw_med={s_raw['median']} "
              f"filt_med={s_per['median']}", flush=True)

    if not rows:
        sys.exit("no units processed")
    with open(a.summary, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t",
                           lineterminator="\n")
        w.writeheader(); w.writerows(rows)
    print(f"\nwrote {a.summary} ({len(rows)} replicon-units)")
    print(f"matrices in {a.out_dir}/")


if __name__ == "__main__":
    main()
