# Attribution: the specification curve

**2026-09-02.** The same treatment applied to the geographic result, applied to
attribution. Four specification dimensions were varied: **estimator** (4),
**scale** (5), **baseline** (majority-class vs marginal chance), and **attractor
stratum** (whether a close relative exists in the pool).

**Two results, and they differ completely.** Country attribution fails almost
everywhere. Region attribution is robust for one estimator and fragile for
another. Neither is a single number.

---

## 1. The baseline choice alone flips the country verdict

For country / nearest-neighbour, n = 46:

| quantity | value |
|---|---|
| observed accuracy | 0.217 |
| **majority-class baseline** (always predict the modal truth) | **0.261** |
| **marginal chance agreement** (what kappa uses) | **0.030** |
| kappa | 0.193 |

**The two baselines differ by 0.231**, and they give opposite verdicts. Against
marginal chance the result "succeeds" at kappa 0.193, which reads as modest but
real. Against the majority class it **fails**: predicting Thailand for every
sample would score higher.

Both are computed from the same predictions. **Reporting only kappa would present
a failing classifier as a working one.**

## 2. Country: 1 of 12 specifications beats the majority baseline

| estimator | all | close relative | no close relative |
|---|---|---|---|
| nearest_nb | 0.217 *(maj 0.261)* | 0.174 *(0.435)* | **0.261** *(0.217)* BEATS |
| modal_k20 | 0.152 *(0.261)* | 0.261 *(0.435)* | 0.043 *(0.217)* |
| hybrid | 0.130 *(0.261)* | 0.261 *(0.435)* | 0.000 *(0.217)* |
| group_test | 0.000 *(0.261)* | 0.000 *(0.435)* | 0.000 *(0.217)* |

Accuracy ranges **0.000 to 0.261** across the twelve specifications, and **only
one beats its own stratum's baseline** -- nearest-neighbour where no close
relative exists, at 0.261 against 0.217. That margin is **one genome out of 23**.

**Country attribution fails robustly.** The single pass is within noise of the
baseline and is not a result.

## 3. Region: robust for one estimator, fragile for another

| estimator | all | close relative | no close relative |
|---|---|---|---|
| **modal_k20** | **0.891** *(maj 0.457)* | **0.913** *(0.739)* | **0.870** *(0.522)* |
| nearest_nb | 0.804 *(0.457)* | 0.696 *(0.739)* **fails** | 0.913 *(0.522)* |
| hybrid | 0.652 *(0.457)* | 0.913 *(0.739)* | 0.391 *(0.522)* **fails** |
| group_test | 0.543 *(0.457)* | 0.739 *(0.739)* **fails** | 0.348 *(0.522)* **fails** |

Accuracy ranges **0.348 to 0.913**. Seven of twelve specifications beat their
baseline.

**`modal_k20` is the only estimator that beats its baseline in all three strata**
(0.891 / 0.913 / 0.870). That is the defensible attribution result.
Nearest-neighbour **fails where a close relative exists** (0.696 against a 0.739
baseline), which is precisely the attractor artifact.

## 4. A correction to how the attractor artifact was described

An earlier note in this project recorded that "both scales score higher where no
relative exists", implying attribution succeeds by avoiding attractors. **That is
an artifact of comparing raw accuracies across strata with different baselines.**

The close-relative stratum has a **much higher majority baseline** (0.739 against
0.522 at region scale, 0.435 against 0.217 at country scale), because a pool
containing a close relative is a pool where one class dominates. Beating the
baseline there is harder, not easier.

Measured against each stratum's own baseline, the effect is **estimator-dependent
and changes sign**: nearest-neighbour fails in the close-relative stratum while
`modal_k20` beats it comfortably. The artifact is real for nearest-neighbour and
absent for the modal estimator.

## 5. What to report

1. **Country: report the failure, not the kappa.** No estimator beats always
   predicting the modal country. State both baselines so the reader can see why
   kappa looks positive.
2. **Region: report `modal_k20`, and report that the estimator choice matters.**
   0.891 overall, and it is the only estimator robust across attractor strata.
   Nearest-neighbour at 0.804 looks comparable overall but fails where a close
   relative exists.
3. **Report the curve, not a point.** Region accuracy spans 0.348 to 0.913 across
   specifications; country spans 0.000 to 0.261.
4. **State that the estimator is part of the number**, exactly as the confounder
   specification is part of the geographic count. The same lesson, in a second
   analysis.
