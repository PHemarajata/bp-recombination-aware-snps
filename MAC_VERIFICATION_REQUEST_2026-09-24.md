# What the cloud session needs from the Mac

**2026-09-24.** To close `ABSTRACT_IDLABCON_REVIEW_2026-09-24.md` before the
October 2 deadline.

**Read this first: most of the corrections do not need the Mac.** Dropping the
resolution-curve sentence, dropping the bare 14/14 and 2/14 stratum, naming the
estimator on every accuracy, and giving country both baselines are all fixable
from documents already in the repository. The Mac run is what makes the
remaining figures defensible under this project's own rule, which is that
documents cite `NUMBERS.tsv` rather than restating numbers.

---

## 1. Two commands

```
cd ~/bp-recombination-aware-snps
python3 freeze_basis_bp.py
python3 generate_numbers.py
```

`freeze_basis_bp.py` exits non-zero on drift, so run it first and stop if it
fails. On the curated copy it reports 12 of 15 checks, which is expected and is
recorded in the runbook. `generate_numbers.py` writes `NUMBERS.tsv` in place.

## 2. Four files to send back

| file | what it settles |
|---|---|
| `NUMBERS.tsv` | every quotable figure, with its `QUOTE THIS` / `DO NOT QUOTE` annotations |
| `GROUPING_LADDER.tsv` | accuracy **and baseline** and kappa per grouping and estimator. This is the one that settles the region headline, its baseline, and the specification range |
| `GROUPING_PREDICTIONS.tsv` | per-genome calls, which is the only way to compute a **baseline per stratum**. `generate_numbers.py` emits the strata counts but not their baselines, and the missing baseline is exactly what made 14/14 unquotable |
| `RESOLUTION_CURVE.tsv` | the fold-range, the true endpoints, and which denominator the curve was scored on (26, 31 or 46) |

All four are text and small. None contains isolate-level sequence.

## 3. One question a single command answers

Whether in-house Nakhon Phanom isolates are among the 46 validation cases. This
decides how heavy the partner clearance conversation is, and two documents in
the repository currently contradict each other on it.

```
grep -c -E '^(IP|IE)-' EXPOSURE_OVERRIDES.tsv
head -1 EXPOSURE_OVERRIDES.tsv
```

Send the two numbers. If the count is 0, the validation set is entirely public
and `METHODS_DRAFT` §2.12.11a.2 is right. If it is not 0,
`BIOPROJECT_COUNTERFACTUAL_2026-09-02.md` §3 is right and partner isolates are
in the headline denominator.

## 4. Optional, only if the CDC reproduction goes into the abstract

The aromatherapy-outbreak numbers in `GROUPING_AND_CDC_2026-08-21.md` §1
(South Asia p = 2.8e-34, India against the rest of South Asia p = 0.351) are
quoted in prose there. If that result is going in the abstract, send whatever
file `grouping_test_bp.py` persists them to, so they are cited rather than
restated.

---

## 5. What each returned file changes in the abstract

- **`NUMBERS.tsv`** confirms or corrects 2,959, the 41% coverage, 312 in-house,
  46 scorable, 16 countries, and the recurrence gap.
- **`GROUPING_LADDER.tsv`** lets the region sentence name `modal_k20` and its
  baseline, and lets the country sentence carry both baselines.
- **`GROUPING_PREDICTIONS.tsv`** decides whether the close-relative stratum can
  go back in with its baseline attached, or stays out.
- **`RESOLUTION_CURVE.tsv`** decides whether any resolution sentence survives,
  and in what form.
- **The `EXPOSURE_OVERRIDES` count** decides the clearance paragraph.
