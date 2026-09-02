#!/usr/bin/env python3
"""
The abstention rule: when should the method answer "unattributable" instead of
guessing a region?

WHY. W2 of the manuscript outline shows that above a nearest-neighbour distance
of ~0.30 the method is not identifying provenance -- it is reporting "unlike the
Asian majority of the panel", and a catch-all region label converts that into a
correct answer for the Americas and a confidently wrong one for Africa. D3
proposes turning that weakness into the paper's most useful methodological
contribution: decline to answer rather than answer wrongly.

This script picks the threshold, scores the rule, and reports what it declines.

WHAT IT DOES NOT DO -- and this is deliberate. It builds NO pool and computes NO
distances. It is a pure consumer of GROUPING_PREDICTIONS.tsv, which
grouping_test_bp.py writes with leave-group-out AND leave-outbreak-out already
applied. Five scorers in this project each reimplemented pool-building and four
of them had to be repaired for the same leak; a sixth would be a sixth chance to
leak silently. Run grouping_test_bp.py first.

THREE THINGS THIS MEASURES, because an abstention rule can look good for
reasons that are not real:

  1. THE FULL RISK-COVERAGE CURVE, not a single chosen operating point. A rule
     that answers only its most confident case always looks perfect.

  2. THE RANDOM-ABSTENTION BASELINE. Declining cases at random leaves the error
     rate unchanged, so the honest question is never "is selective accuracy
     higher than overall accuracy" -- it always is, if you decline enough. It is
     "is it higher than declining the same NUMBER of cases at random". This is
     the same discipline the project already applies to every accuracy figure.

  3. AN HONEST OPERATING POINT VIA LEAVE-ONE-OUT. Choosing a threshold on 46
     genomes and scoring it on those same 46 is the circular test this project
     has already been burned by. Here the threshold is chosen on the other 45
     and applied to the held-out genome, so the reported number is out-of-sample.

TWO CANDIDATE SIGNALS, because they ask different questions:
  nn_distance  "is anything near me at all"   -- the outline's proposal
  vote_share   "do the things near me agree"  -- neighbourhood consensus
  margin       "how far does the winner lead" -- consensus, decisiveness form
"""
import csv
import os
import statistics as st
from collections import Counter

B = os.path.dirname(os.path.abspath(__file__))
PREDS = f"{B}/GROUPING_PREDICTIONS.tsv"
CURVE = f"{B}/ABSTENTION_CURVE.tsv"
OPPT = f"{B}/ABSTENTION_OPERATING_POINTS.tsv"

# (column, direction). "hi" = a HIGH value is risky, so answer when v <= t.
#                      "lo" = a LOW  value is risky, so answer when v >= t.
SIGNALS = (("nn_distance", "hi"), ("vote_share", "lo"), ("margin", "lo"))

# The two headline analyses (see NUMBERS.tsv): country is best under nearest
# neighbour, region under modal k=20. Plus the deep split, as a positive control
# -- if the rule is doing anything sane it should decline almost nothing there,
# because Asia/non-Asia is already perfect.
HEADLINES = (("region_7way", "modal_k20"),
             ("country", "nearest_nb"),
             ("asia_vs_not", "modal_k20"))

TARGETS = (0.95, 0.90, 0.80, 0.70, 0.60, 0.50)


def answers(v, t, direction):
    return v <= t if direction == "hi" else v >= t


def curve(rows, col, direction):
    """Every distinct operating point: (threshold, coverage, sel_accuracy)."""
    vals = sorted({float(r[col]) for r in rows})
    pts = []
    for t in vals:
        kept = [r for r in rows if answers(float(r[col]), t, direction)]
        if not kept:
            continue
        acc = sum(int(r["correct"]) for r in kept) / len(kept)
        pts.append((t, len(kept) / len(rows), acc, len(kept)))
    return pts


def pick(rows, col, direction, target):
    """Lowest-risk threshold that still answers >= target of the training rows.

    Ties on coverage are broken toward higher accuracy, then toward the safer
    (more abstaining) threshold, so the choice is deterministic.
    """
    ok = [p for p in curve(rows, col, direction) if p[1] >= target]
    if not ok:
        return None
    best = max(ok, key=lambda p: (p[2], -p[1]))
    return best[0]


def loo(rows, col, direction, target):
    """Out-of-sample: threshold chosen on the other n-1, applied to the held-out."""
    ans = cor = 0
    for i in range(len(rows)):
        train = rows[:i] + rows[i + 1:]
        t = pick(train, col, direction, target)
        if t is None:
            continue
        r = rows[i]
        if answers(float(r[col]), t, direction):
            ans += 1
            cor += int(r["correct"])
    return ans, cor


def main():
    if not os.path.exists(PREDS):
        raise SystemExit(f"missing {PREDS} -- run grouping_test_bp.py first")
    allrows = list(csv.DictReader(open(PREDS), delimiter="\t"))
    if "vote_share" not in allrows[0]:
        raise SystemExit("GROUPING_PREDICTIONS.tsv predates the confidence "
                         "columns -- re-run grouping_test_bp.py")

    curve_out, op_out = [], []
    for g, est in HEADLINES:
        rows = [r for r in allrows
                if r["grouping"] == g and r["estimator"] == est]
        if not rows:
            continue
        n = len(rows)
        base = sum(int(r["correct"]) for r in rows) / n
        print(f"\n{'='*74}\n{g}  /  {est}   n={n}   answer-everything accuracy "
              f"{base:.1%}\n{'='*74}")

        for col, direction in SIGNALS:
            pts = curve(rows, col, direction)
            for t, cov, acc, k in pts:
                curve_out.append(dict(grouping=g, estimator=est, signal=col,
                                      threshold=f"{t:.5f}", n_answered=k,
                                      coverage=f"{cov:.4f}",
                                      selective_accuracy=f"{acc:.4f}"))

            print(f"\n  signal: {col}  ({'abstain above' if direction=='hi' else 'abstain below'} threshold)")
            print(f"    {'target':>7}{'thresh':>9}{'cov':>7}{'sel.acc':>9}"
                  f"{'random':>8}{'majority':>10}{'err-':>6}{'ok-':>5}"
                  f"   {'LOO cov':>8}{'LOO acc':>8}")
            for tg in TARGETS:
                t = pick(rows, col, direction, tg)
                if t is None:
                    continue
                kept = [r for r in rows if answers(float(r[col]), t, direction)]
                drop = [r for r in rows if not answers(float(r[col]), t, direction)]
                acc = sum(int(r["correct"]) for r in kept) / len(kept)
                # TWO baselines, because a selective accuracy can rise for two
                # quite different reasons and only one of them is the rule
                # working:
                #   random   -- declining the same NUMBER of cases at random
                #               leaves the expected error rate untouched, so
                #               this is just the answer-everything accuracy.
                #   majority -- the majority-class share OF THE RETAINED SUBSET.
                #               Abstention changes the class mix, so the old
                #               baseline does not transfer. If selective
                #               accuracy only tracks this, the rule has selected
                #               an easier subset, not a more reliable one.
                mj = Counter(r["truth"] for r in kept).most_common(1)[0][1] / len(kept)
                lift = acc - base
                err_avoided = sum(1 for r in drop if not int(r["correct"]))
                ok_lost = sum(1 for r in drop if int(r["correct"]))
                la, lc = loo(rows, col, direction, tg)
                lacc = lc / la if la else float("nan")
                print(f"    {tg:>7.0%}{t:>9.4f}{len(kept)/n:>7.1%}{acc:>9.1%}"
                      f"{base:>8.1%}{mj:>10.1%}{err_avoided:>6}{ok_lost:>5}"
                      f"   {la/n:>8.1%}{lacc:>8.1%}")
                op_out.append(dict(
                    grouping=g, estimator=est, signal=col,
                    target_coverage=f"{tg:.2f}", threshold=f"{t:.5f}",
                    n_answered=len(kept), coverage=f"{len(kept)/n:.4f}",
                    selective_accuracy=f"{acc:.4f}",
                    random_baseline=f"{base:.4f}",
                    retained_majority_baseline=f"{mj:.4f}",
                    lift=f"{lift:+.4f}", errors_avoided=err_avoided,
                    correct_lost=ok_lost,
                    loo_coverage=f"{la/n:.4f}",
                    loo_selective_accuracy=(f"{lacc:.4f}" if la else "NA")))

        # What does the rule actually decline? The operational question is not
        # the accuracy number, it is whether the declined set is enriched for
        # the errors -- and specifically whether it catches the confidently
        # wrong Sub-Saharan African calls that motivated the rule.
        errs = [r for r in rows if not int(r["correct"])]
        if errs:
            print(f"\n  the {len(errs)} error(s), and where each signal ranks them "
                  f"(1 = most abstainable of {n}):")
            for r in errs:
                rk = {}
                for col, direction in SIGNALS:
                    vs = sorted(rows, key=lambda x: float(x[col]),
                                reverse=(direction == "hi"))
                    rk[col] = [x["sample_id"] for x in vs].index(r["sample_id"]) + 1
                print(f"    {r['sample_id'][:26]:<28} {r['truth'][:24]:<26}"
                      f"-> {r['predicted'][:22]:<24}"
                      + "  ".join(f"{c}={rk[c]}" for c, _ in SIGNALS))

    for path, rows_, cols in (
            (CURVE, curve_out, ["grouping", "estimator", "signal", "threshold",
                                "n_answered", "coverage", "selective_accuracy"]),
            (OPPT, op_out, ["grouping", "estimator", "signal", "target_coverage",
                            "threshold", "n_answered", "coverage",
                            "selective_accuracy", "random_baseline",
                            "retained_majority_baseline", "lift",
                            "errors_avoided", "correct_lost",
                            "loo_coverage", "loo_selective_accuracy"])):
        with open(path, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t",
                               lineterminator="\n")
            w.writeheader()
            w.writerows(rows_)
        print(f"\nwrote {os.path.basename(path)}  ({len(rows_)} rows)")


if __name__ == "__main__":
    main()
