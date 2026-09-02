#!/usr/bin/env python3
"""
Test the nu hypothesis for the depressed-r/m residue.

The claim
---------
Gubbins finds recombination by looking for regions of unusually DENSE SNPs. An
import only looks dense if the donor differed from the recipient. ClonalFrameML
estimates that divergence explicitly as **nu**. So where nu is low -- donors
nearly identical to recipients -- imports carry too few SNPs to raise a density
signal, Gubbins reports a low r/m, and the unit looks like a detection failure
when recombination is in fact happening.

Prediction: **units where Gubbins and ClonalFrameML disagree most should be the
units with the lowest nu.** i.e. a NEGATIVE correlation between nu and the
CFML/Gubbins ratio.

The trap in the obvious test
----------------------------
ClonalFrameML's r/m is derived as (R/theta) x delta x nu, so nu sits in the
numerator of the ratio being tested:

    ratio = r/m_CFML / r/m_Gubbins = (R/theta . delta . nu) / r/m_Gubbins

Raising nu therefore raises the ratio *mechanically*, independent of any
biology. That bias runs OPPOSITE to the prediction, which makes the test
conservative: a negative correlation has to overcome a built-in positive one.
Reported below as "mechanical expectation" so the two are not confused.

A cleaner test avoids the shared term entirely: correlate nu against
**Gubbins r/m alone**. Gubbins never sees nu, so any relationship there is not
an artefact of shared arithmetic. Prediction: positive -- low nu, low Gubbins
r/m.

Usage:  nu_hypothesis_bp.py [--replicon chr1|chr2|both]
"""
import argparse
import csv
import glob
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clonalframe_nu_bp as cf

B = os.path.dirname(os.path.abspath(__file__))


def load(replicon):
    gub = {r["unit"]: float(r["rm_corrected"])
           for r in csv.DictReader(open(f"{B}/L1v4c_out/Summaries/recombination_rm.tsv"),
                                   delimiter="\t") if r.get("rm_corrected")}
    rows = []
    for p in sorted(glob.glob(f"{B}/cfml/strain_*_L1_*__{replicon}/cfml.em.txt")):
        unit = os.path.basename(os.path.dirname(p)).rsplit("__", 1)[0]
        em = cf.parse_em(p)
        if "R/theta" not in em or unit not in gub or gub[unit] <= 0:
            continue
        rm_cf = cf.derived_rm(em)
        if not np.isfinite(rm_cf) or rm_cf <= 0:
            continue
        rows.append({"unit": unit, "replicon": replicon,
                     "rm_gubbins": gub[unit], "rm_cfml": rm_cf,
                     "R_theta": em["R/theta"], "delta": em.get("delta", np.nan),
                     "nu": em["nu"], "ratio": rm_cf / gub[unit]})
    return rows


def rep(name, x, y, expect):
    r, p = stats.spearmanr(x, y)
    flag = "  <-- as predicted" if ((r < 0) == (expect == "neg") and p < 0.05) else ""
    print(f"  {name:<46} rho={r:+.3f}  p={p:.4f}  n={len(x)}{flag}")
    return r, p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replicon", default="both", choices=("chr1", "chr2", "both"))
    ap.add_argument("--out", default=f"{B}/NU_HYPOTHESIS.tsv")
    a = ap.parse_args()

    reps = ("chr1", "chr2") if a.replicon == "both" else (a.replicon,)
    allrows = []
    for rp in reps:
        rows = load(rp)
        if len(rows) < 8:
            print(f"{rp}: only {len(rows)} units, skipping")
            continue
        allrows += rows
        nu = np.array([r["nu"] for r in rows])
        rg = np.array([r["rm_gubbins"] for r in rows])
        rc = np.array([r["rm_cfml"] for r in rows])
        ratio = np.array([r["ratio"] for r in rows])
        dl = np.array([r["delta"] for r in rows])
        rt = np.array([r["R_theta"] for r in rows])

        print(f"\n{'='*78}\n{rp}  (n = {len(rows)} units)\n{'='*78}")
        print(f"  nu      median {np.median(nu):.4f}   range {nu.min():.4f} - {nu.max():.4f}")
        print(f"  delta   median {np.median(dl):7.0f} bp range {dl.min():.0f} - {dl.max():.0f}")
        print(f"  R/theta median {np.median(rt):.3f}    range {rt.min():.3f} - {rt.max():.3f}")
        print(f"  r/m     Gubbins median {np.median(rg):.2f}   CFML median {np.median(rc):.2f}"
              f"   ratio median {np.median(ratio):.1f}x")

        print("\n  --- the clean test: Gubbins never sees nu ---")
        rep("nu  vs  Gubbins r/m            (expect +)", nu, rg, "pos")
        print("\n  --- the confounded test (mechanical bias runs the OTHER way) ---")
        rep("nu  vs  CFML/Gubbins ratio     (expect -)", nu, ratio, "neg")
        print("\n  --- controls ---")
        rep("nu  vs  CFML r/m", nu, rc, "any")
        rep("delta vs Gubbins r/m", dl, rg, "any")
        rep("R/theta vs Gubbins r/m", rt, rg, "any")

        # does nu explain Gubbins r/m once R/theta and delta are accounted for?
        X = np.column_stack([np.log(rt), np.log(dl), np.log(nu)])
        keep = np.isfinite(X).all(axis=1) & np.isfinite(np.log(rg))
        if keep.sum() > 12:
            Xk = np.column_stack([np.ones(keep.sum()), X[keep]])
            yk = np.log(rg[keep])
            beta, *_ = np.linalg.lstsq(Xk, yk, rcond=None)
            resid = yk - Xk @ beta
            r2 = 1 - resid.var() / yk.var()
            print(f"\n  --- log-log regression: log(Gubbins r/m) ~ log R/theta + log delta + log nu ---")
            print(f"      coef  R/theta {beta[1]:+.3f}   delta {beta[2]:+.3f}   nu {beta[3]:+.3f}"
                  f"    R^2={r2:.3f}  n={keep.sum()}")
            print(f"      (if Gubbins simply measured (R/theta).delta.nu, all three would be ~+1)")

        # the units Gubbins would reject
        lo = [r for r in rows if r["rm_gubbins"] < 3.0]
        if lo:
            nl = np.array([r["nu"] for r in lo]); nh = np.array([r["nu"] for r in rows if r["rm_gubbins"] >= 3.0])
            print(f"\n  --- units Gubbins would REJECT (r/m < 3.0): {len(lo)} of {len(rows)} ---")
            print(f"      their nu  : median {np.median(nl):.4f}")
            if len(nh):
                u, pu = stats.mannwhitneyu(nl, nh)
                print(f"      others' nu: median {np.median(nh):.4f}   Mann-Whitney p={pu:.4f}")
            print(f"      CFML says their r/m is: median {np.median([r['rm_cfml'] for r in lo]):.2f}")
            resc = [r for r in lo if r["rm_cfml"] >= 3.0]
            print(f"      would be RESCUED by CFML (CFML r/m >= 3.0): {len(resc)} of {len(lo)}")

    if allrows:
        with open(a.out, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(allrows[0]), delimiter="\t",
                               lineterminator="\n")
            w.writeheader(); w.writerows(allrows)
        print(f"\nwrote {a.out}  ({len(allrows)} replicon-units)")


if __name__ == "__main__":
    main()
