#!/usr/bin/env python3
"""Exact binomial test and confidence interval for an attribution accuracy.

WHY THIS EXISTS. The attribution result is reported as an accuracy against a
majority-class baseline (country 10/46 against 26.1%, region 41/46 against
45.7%) and as Cohen's kappa. Neither carries a test or an interval, and the
ID Lab Con call for abstracts asks for statistical significance where
applicable. This supplies it.

WHAT IT COMPUTES, for `correct` successes in `n` trials against a baseline rate:

  * accuracy, as a proportion
  * one-sided exact binomial p for H1: accuracy > baseline
        This is the test the claim needs. "Did not exceed chance" is a
        statement about the upper tail, so a one-sided test is the honest one.
  * two-sided exact binomial p, by the method of small p-values
        Reported alongside because it answers the different question of
        whether the accuracy is distinguishable from the baseline at all.
  * Clopper-Pearson exact 95% interval, and the Wilson score interval

THREE CAVEATS THAT MUST TRAVEL WITH THE OUTPUT. They are printed with it.

  1. The baseline is the observed share of the commonest class in the same
     sample, not a rate known in advance. Treating it as fixed is conventional
     and slightly anti-conservative.
  2. The trials are not fully independent. The 46 scorable genomes come from 45
     individuals, and outbreak groups are held out together rather than being
     independent draws. A binomial interval therefore reads narrower than the
     design justifies.
  3. A label-permutation test over the actual holdout would answer this better
     and needs the per-genome assignments, not the summary counts.

USAGE. Every input is required; there are no defaults, so this cannot quietly
score a stale set of counts.

  python3 attribution_significance_bp.py --correct 10 --n 46 --baseline 0.2609
  python3 attribution_significance_bp.py --correct 41 --n 46 --baseline-correct 21
  python3 attribution_significance_bp.py --correct 10 --n 46 --baseline-correct 12 \
      --label attribution.country.nearest_neighbour --tsv
"""
import argparse
import sys
from math import comb, sqrt


def pmf(k, n, p):
    if p <= 0.0:
        return 1.0 if k == 0 else 0.0
    if p >= 1.0:
        return 1.0 if k == n else 0.0
    return comb(n, k) * p**k * (1.0 - p) ** (n - k)


def sf_ge(k, n, p):
    """P(X >= k)."""
    return sum(pmf(i, n, p) for i in range(k, n + 1))


def cdf_le(k, n, p):
    """P(X <= k)."""
    return sum(pmf(i, n, p) for i in range(0, k + 1))


def two_sided(k, n, p):
    """Exact two-sided p by the method of small p-values."""
    obs = pmf(k, n, p)
    # Guard against summing terms that are equal only to floating-point noise.
    tol = obs * 1e-7
    return min(1.0, sum(pmf(i, n, p) for i in range(n + 1) if pmf(i, n, p) <= obs + tol))


def clopper_pearson(k, n, alpha=0.05):
    """Exact interval, by bisection on the binomial tails. No SciPy needed."""

    def solve(target, lo, hi, fn):
        for _ in range(200):
            mid = (lo + hi) / 2.0
            if fn(mid) > target:
                hi = mid
            else:
                lo = mid
        return (lo + hi) / 2.0

    # Lower bound: the p at which P(X >= k) = alpha/2. P(X >= k) rises with p.
    low = 0.0 if k == 0 else solve(alpha / 2.0, 0.0, 1.0, lambda p: sf_ge(k, n, p))
    # Upper bound: the p at which P(X <= k) = alpha/2. P(X <= k) FALLS with p, so
    # bisect on its increasing complement against 1 - alpha/2. Targeting alpha/2
    # here instead solves P(X <= k) = 0.975 and returns a bound far too low: for
    # 10/46 it gives 12.6% where the answer is 36.4%, which looks like a
    # plausible interval rather than an error.
    high = 1.0 if k == n else solve(1.0 - alpha / 2.0, 0.0, 1.0,
                                    lambda p: 1.0 - cdf_le(k, n, p))
    return low, high


def wilson(k, n, z=1.959963984540054):
    phat = k / n
    d = 1.0 + z * z / n
    centre = (phat + z * z / (2 * n)) / d
    half = z * sqrt(phat * (1 - phat) / n + z * z / (4 * n * n)) / d
    return centre - half, centre + half


def selftest():
    """Check Clopper-Pearson against published values, and the tails against
    hand-computable cases. The upper bound was wrong once, in a way that still
    printed a plausible-looking interval, so it is pinned here."""
    checks = [
        ((0, 10), (0.0000, 0.3085)),
        ((10, 10), (0.6915, 1.0000)),
        ((2, 20), (0.0123, 0.3170)),
        ((10, 46), (0.1095, 0.3636)),
    ]
    for (k, n), (elo, ehi) in checks:
        lo, hi = clopper_pearson(k, n)
        assert abs(lo - elo) < 5e-4, f"CP low {k}/{n}: {lo:.4f} != {elo}"
        assert abs(hi - ehi) < 5e-4, f"CP high {k}/{n}: {hi:.4f} != {ehi}"
    # The interval must contain the point estimate, and bracket it sanely.
    for n in (5, 17, 46, 100):
        for k in range(n + 1):
            lo, hi = clopper_pearson(k, n)
            assert lo <= k / n <= hi, f"CP does not contain {k}/{n}"
    # A fair coin: P(X >= n) = 0.5**n exactly.
    assert abs(sf_ge(10, 10, 0.5) - 0.5**10) < 1e-12
    # Two-sided p at the mean of a symmetric binomial is 1.
    assert abs(two_sided(5, 10, 0.5) - 1.0) < 1e-12
    # A one-sided p must fall as the count rises.
    ps = [sf_ge(k, 46, 12 / 46) for k in range(5, 20)]
    assert all(b <= a for a, b in zip(ps, ps[1:])), "one-sided p is not monotone"
    print("selftest: ok")


def main():
    if "--selftest" in sys.argv:
        selftest()
        return
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true",
                    help="verify the interval against published values and exit")
    ap.add_argument("--correct", type=int, required=True,
                    help="number of correctly attributed cases")
    ap.add_argument("--n", type=int, required=True,
                    help="number of scorable cases")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--baseline", type=float,
                   help="majority-class baseline as a proportion, e.g. 0.2609")
    g.add_argument("--baseline-correct", type=int,
                   help="majority-class count, from which the rate is n-derived")
    ap.add_argument("--label", default="",
                    help="name for the row, e.g. attribution.country.nearest_neighbour")
    ap.add_argument("--tsv", action="store_true",
                    help="emit NUMBERS.tsv-style rows instead of prose")
    a = ap.parse_args()

    if not 0 <= a.correct <= a.n or a.n <= 0:
        sys.exit("correct must lie in [0, n] and n must be positive")
    p0 = a.baseline if a.baseline is not None else a.baseline_correct / a.n
    if not 0.0 < p0 < 1.0:
        sys.exit("baseline must lie strictly between 0 and 1")

    k, n = a.correct, a.n
    acc = k / n
    p_greater = sf_ge(k, n, p0)
    p_two = two_sided(k, n, p0)
    cp_lo, cp_hi = clopper_pearson(k, n)
    w_lo, w_hi = wilson(k, n)
    tag = a.label or f"{k}/{n}"

    if a.tsv:
        rows = [
            (f"{tag}.accuracy", f"{acc:.4f}"),
            (f"{tag}.baseline", f"{p0:.4f}"),
            (f"{tag}.p_one_sided_greater", f"{p_greater:.4g}"),
            (f"{tag}.p_two_sided", f"{p_two:.4g}"),
            (f"{tag}.ci95_exact_low", f"{cp_lo:.4f}"),
            (f"{tag}.ci95_exact_high", f"{cp_hi:.4f}"),
        ]
        for key, val in rows:
            print(f"{key}\t{val}")
        return

    print(f"{tag}")
    print(f"  accuracy                 {k}/{n} = {acc*100:.1f}%")
    print(f"  majority baseline        {p0*100:.1f}%")
    print(f"  exact 95% CI             {cp_lo*100:.1f}% to {cp_hi*100:.1f}%  (Clopper-Pearson)")
    print(f"  Wilson 95% CI            {w_lo*100:.1f}% to {w_hi*100:.1f}%")
    print(f"  P(X >= {k}) at baseline   {p_greater:.4g}   <- one-sided, H1: accuracy > baseline")
    print(f"  two-sided exact p        {p_two:.4g}")
    inside = cp_lo <= p0 <= cp_hi
    print(f"  baseline inside the CI?  {'yes' if inside else 'no'}")
    print()
    print("  Caveats: the baseline is estimated from this same sample; the trials")
    print("  are not fully independent (46 genomes from 45 individuals, outbreak")
    print("  groups held out together); a label-permutation test would be better")
    print("  and needs the per-genome assignments rather than these counts.")


if __name__ == "__main__":
    main()
