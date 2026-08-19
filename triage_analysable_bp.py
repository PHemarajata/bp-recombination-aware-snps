#!/usr/bin/env python3
"""N3: triage the 45 analysable-set production runs on union AND pooled r/m.

WHY BOTH. Neither statistic catches both failure modes (A.11):
  union collapses  -> recombination genuinely under-detected (below the floor)
  r/m collapses    -> Gubbins finds tracts but stops assigning SNPs to them
                      (above the ceiling, OR the cluster is bridged)

SCOPE NOTE -- CORRECTED 2026-08-11, the first version of this was wrong.
It claimed that because every unit here is inside the diversity range
(1,265-4,442 ska), the above-ceiling branch of the r/m failure mode is "excluded
by construction", so a low r/m must mean BRIDGING. **That does not hold.** The
r/m decline appears to begin BELOW the nominal 4,671 ceiling: the four
highest-diversity in-range units average r/m 3.05 against 7.19 for the twelve
below ska 3,900 (A.11l). So an RM-LOW flag on a high-diversity unit is
**ambiguous between bridging and ceiling onset** and must not be reported as
bridging. The evidence is 4 points and non-monotone, so the ambiguity is the
finding, not the gradient.

r/m remains the only post-hoc safety net for the 25 unscreened units (n < 25),
since both modality statistics fail below n=25 (A.11f) and r/m only fires after
Gubbins has run.

HEADLINE CONVENTION. union / r/m / tract for a unit = the MEAN OF THE TWO
`close__ska_map` ARMS (chr1, chr2). Verified against A.11: this reproduces the
published cluster_34, cluster_15 and cluster_10 rows exactly. The K96243 arms
are the contrast, not the headline.

THE TWO CUTOFFS ARE NOT EQUALLY WELL EVIDENCED -- say so in any write-up.

  union >= 0.47   NO LONGER INSENSITIVE -- revised 2026-08-11 (A.11k). The
                  41.4-point empty band that justified it held over the 19
                  calibration units and has since been POPULATED by three
                  production units (47.9%, 53.8%, 54.5%), one of them 0.9 points
                  above the cutoff. Cutoffs of 47/48/55/58% now give four
                  different answers. It is retained because the units just above
                  it carry healthy r/m (6.79, 7.71) -- the two detectors agree --
                  NOT because the choice does not matter. It does.

  r/m  >= 3.0     WEAK. There is no empty band. Over every run measured to date
                  the in-range evidence is ONE bridged unit (s1_L1_27, 2.57) and
                  one nearest working unit (cluster_15, 3.38) -- a 1.3x bracket
                  resting on a single point either side. This is the same shape
                  of reasoning that cost a factor of two on the floor (A.11b),
                  so treat an r/m flag as "re-examine", never as a verdict.

Usage:
    python3 triage_analysable_bp.py                 # all prod_* units
    python3 triage_analysable_bp.py --selftest
"""

import argparse
import os
import re
import statistics
import sys

import cap_location_bp as C

SELF = os.path.dirname(os.path.abspath(__file__))
UNITS_TABLE = os.path.join(SELF, "analysable_units.tsv")

UNION_MIN = C.UNION_MIN          # 0.47, reused deliberately -- one source of truth
RM_MIN = 3.0                     # see the caveat above; NOT a calibrated constant
RM_BRACKET = (2.57, 3.38)        # s1_L1_27 (bridged) .. cluster_15 (works)


def load_units(path=UNITS_TABLE):
    """unit -> {n, ska_mean, screened} from analysable_units.tsv."""
    out = {}
    with open(path) as fh:
        hdr = fh.readline().rstrip("\n").split("\t")
        for line in fh:
            f = line.rstrip("\n").split("\t")
            if len(f) < len(hdr):
                continue
            r = dict(zip(hdr, f))
            out[r["unit"]] = {
                "n": int(r["n"]),
                "ska": int(r["ska_mean"]),
                "screened": r["screened"],
                "source": r["source"],
            }
    return out


def median_ufboot(arm_dir):
    """Median ultrafast-bootstrap support over internal branches of one arm.

    IQ-TREE writes `)SUPPORT:LENGTH` at each internal node, so the support values
    are exactly the numbers following a closing paren. Returns nan if the tree is
    missing or has no internal node (possible only for degenerate 2-3 taxon
    trees, which cannot occur here -- every unit has n >= 7).
    """
    tf = os.path.join(arm_dir, "tree.treefile")
    if not os.path.exists(tf):
        return float("nan")
    vals = [float(x) for x in re.findall(r"\)(\d+(?:\.\d+)?):", open(tf).read())]
    return statistics.median(vals) if vals else float("nan")


def score_unit(outdir):
    """Mean of the two close__ska_map arms, or None if the unit is incomplete.

    `ufboot` is the WORST of the two replicons, not the mean: a unit whose
    chromosome 2 tree is unresolved is not rescued by a well-resolved
    chromosome 1, since both are needed.
    """
    d = os.path.join(outdir, "arms")
    if not os.path.isdir(d):
        return None
    vals, boots = [], []
    for arm in sorted(os.listdir(d)):
        if not arm.startswith("close__ska_map"):
            continue
        p = os.path.join(d, arm)
        if os.path.isdir(p):
            s = C.gubbins_stats(p)
            if s:
                vals.append(s)
                boots.append(median_ufboot(p))
    if len(vals) != 2:
        return None
    return {
        "union": statistics.mean(v["union"] for v in vals),
        "rm": statistics.mean(v["pooled_rm"] for v in vals),
        "tract": statistics.mean(v["median_block"] for v in vals),
        "ufboot": min(boots) if boots else float("nan"),
    }


# Below this n, union is materially depressed by unit size (A.11r: r(log n,
# union) = +0.81; mean union 74.9% at n>=45 vs 43.9% at n<25).
#
# 45 IS A ROUGH BOUNDARY, NOT A CALIBRATED ONE -- and the confound does not stop
# cleanly there: `s1_L1_27_L2_69` (n=45, union 49.5%) and `s3_L1_5` (n=51, 47.9%)
# both sit barely above the cutoff, while `s1_L1_28` (n=55) reaches 79.5%. The
# honest statement is that union is not comparable across sizes AT ALL and needs
# normalising; this constant only marks where the bias becomes impossible to
# ignore. Do not present it as a threshold.
SIZE_CONFOUND_N = 45


# Median ultrafast bootstrap below which a tree is REPORTED as poorly resolved.
#
# >>> THIS IS A REPORTING LINE, NOT A GATE. WITHDRAWN AS A CRITERION 2026-08-11
# >>> (Tier 0.1). It was adopted as a third acceptance criterion in A.11v and
# >>> that adoption was wrong, for a reason that has nothing to do with trees:
#
# 70 is the conventional threshold for STANDARD nonparametric bootstrap. IQ-TREE's
# ultrafast bootstrap is not on that scale -- UFBoot is much less conservative,
# and its own "supported" convention is >= 95 (UFBoot 95 ~ SBS 70). Applying 70
# to UFBoot values was therefore FAR MORE PERMISSIVE than the convention cited to
# justify it, not more conservative as intended.
#
# What settles it is not which number is right but how much rides on the choice:
#
#     no gate                30 units   933 genomes   33.3%
#     UFBoot >= 70           22 units   708 genomes   25.3%   <- what was adopted
#     UFBoot >= 80           17 units   632 genomes   22.6%
#     UFBoot >= 90           10 units   437 genomes   15.6%
#     UFBoot >= 95            7 units   176 genomes    6.3%   <- the real convention
#
# A headline coverage figure that moves 5.3x across the range of conventions a
# reasonable person might pick is not a measurement. Gating on support also
# DISCARDS a whole unit because part of its tree is uncertain, when the uncertain
# part is identifiable and can simply be collapsed.
#
# WHAT REPLACES IT: keep every unit that passes detection, collapse branches
# below support into polytomies (`collapse_unsupported_bp.py`), and carry the
# uncertainty into the downstream analysis instead of thresholding it away.
# Resolution is still REPORTED per unit, because A.11v's underlying observation
# is sound and worth knowing -- tree resolution is orthogonal to pooled r/m
# (r = -0.010) and to size (+0.171), so nothing else tells you about it.
UFBOOT_REPORT = 70.0

# Retained under the old name so anything importing it keeps working; both refer
# to the same reporting line, and neither is a gate.
UFBOOT_MIN = UFBOOT_REPORT

# Verdicts that mean "recombination was detected and assigned properly".
_USABLE = ("OK", "UNION-SIZE", "RM-MARGINAL")


def triage(union, rm, screened, n=None, ufboot=None):
    """Detection verdict. Tree resolution is REPORTED, never gated on.

    `ufboot` is accepted so that callers need not change, and so that a unit
    passing detection with a poorly-resolved tree is annotated -- but it can no
    longer change the verdict. See `UFBOOT_REPORT` for why the gate was dropped
    and `resolution_note` for what is reported instead.
    """
    return _detect(union, rm, screened, n)


def resolution_note(flag, ufboot):
    """Advisory string about tree resolution. Never affects the verdict.

    Returns "" when there is nothing to say, so it can be appended blindly.
    """
    if flag not in _USABLE or ufboot is None or ufboot != ufboot:
        return ""
    if ufboot >= UFBOOT_REPORT:
        return ""
    return ("tree poorly resolved (median UFBoot %.1f on the worse replicon) -- "
            "UNIT RETAINED; collapse branches below support into polytomies "
            "rather than dropping it" % ufboot)


def _detect(union, rm, screened, n=None):
    """Return (flag, note).

    A.11's design assumed union and r/m are COMPLEMENTARY -- each catching a
    failure the other misses. The production runs show they can also CONTRADICT
    each other on the same unit, which the design did not anticipate, so that
    case gets its own label rather than being silently resolved.

    Genuine detection failure has BOTH statistics collapse (cluster_62: union
    0.7%, r/m 0.07, tract 1,002 bp). A low union with a HEALTHY r/m and a normal
    tract is a different animal and is almost certainly not under-detection.
    """
    if union < UNION_MIN and rm >= RM_MIN:
        if n is not None and n < SIZE_CONFOUND_N:
            return "UNION-SIZE", ("union %.1f%% < %.0f%% but n=%d and r/m %.2f is "
                                  "HEALTHY -- union is size-confounded below n~%d "
                                  "(A.11r, r(log n, union)=+0.81); LIKELY A FALSE "
                                  "REJECTION, judge on r/m"
                                  % (100 * union, 100 * UNION_MIN, n, rm,
                                     SIZE_CONFOUND_N))
        return "DISAGREE", ("union %.1f%% < %.0f%% but r/m %.2f is HEALTHY -- "
                            "detectors contradict; probably NOT under-detection, "
                            "do not drop without deciding the tie-break"
                            % (100 * union, 100 * UNION_MIN, rm))
    if union < UNION_MIN:
        return "UNDER-DETECT", ("union %.1f%% < %.0f%% AND r/m %.2f low -- both "
                                "agree" % (100 * union, 100 * UNION_MIN, rm))
    if rm < RM_MIN:
        # Values just under the line are NOT a verdict: the cutoff's whole
        # supporting bracket is 2.57-3.38 (A.11j), so anything inside it is
        # indistinguishable from the threshold itself.
        if rm >= RM_BRACKET[0]:
            return "RM-MARGINAL", ("r/m %.2f is inside the cutoff's own support "
                                   "bracket %.2f-%.2f -- indistinguishable from "
                                   "the threshold; NOT evidence of bridging"
                                   % (rm, RM_BRACKET[0], RM_BRACKET[1]))
        why = "r/m %.2f < %.1f -- suspect BRIDGED" % (rm, RM_MIN)
        if screened == "yes":
            why += " (SCREENED unit -- unexpected, investigate)"
        elif screened.startswith("no"):
            why += " (unscreened sub-cluster, n<25: the expected catch)"
        else:
            why += " (PopPUNK strain, never modality-screened -- not the n<25 case)"
        return "RM-LOW", why
    return "OK", ""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prefix", default="prod_")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()

    units = load_units()
    done, pending = [], []
    for unit, meta in units.items():
        s = score_unit(os.path.join(SELF, args.prefix + unit))
        if s is None:
            pending.append((unit, meta))
        else:
            done.append((unit, meta, s, triage(s["union"], s["rm"], meta["screened"], meta["n"], s["ufboot"])))

    done.sort(key=lambda r: r[2]["rm"])
    print("%-18s %5s %6s %4s %8s %7s %7s %8s  %s"
          % ("unit", "n", "ska", "scr", "union", "r/m", "tract", "UFBoot", "flag"))
    for unit, meta, s, (flag, note) in done:
        res = resolution_note(flag, s["ufboot"])
        print("%-18s %5d %6d %4s %7.1f%% %7.2f %7.0f %8.1f  %-12s %s"
              % (unit, meta["n"], meta["ska"],
                 "y" if meta["screened"] == "yes" else "-",
                 100 * s["union"], s["rm"], s["tract"], s["ufboot"], flag,
                 note or res))

    usable = [r for r in done if r[3][0] in _USABLE]
    n_ok = sum(1 for r in done if r[3][0] == "OK")
    gen_ok = sum(r[1]["n"] for r in done if r[3][0] == "OK")
    gen_usable = sum(r[1]["n"] for r in usable)
    print("\n%d/%d units scored; %d OK (%d genomes), %d flagged, %d pending"
          % (len(done), len(units), n_ok, gen_ok, len(done) - n_ok, len(pending)))
    print("PASSING DETECTION (OK + UNION-SIZE + RM-MARGINAL): %d units, "
          "%d genomes = %.1f%% of 2,802"
          % (len(usable), gen_usable, 100.0 * gen_usable / 2802))
    if pending:
        print("pending: " + ", ".join(u for u, _ in sorted(pending)))

    low = [r for r in usable
           if r[2]["ufboot"] == r[2]["ufboot"] and r[2]["ufboot"] < UFBOOT_REPORT]
    print("\nunion cutoff %.2f is NOT insensitive -- A.11c's 41-pt empty band was "
          "populated by\nproduction units, and union is size-confounded "
          "(r(log n, union) = +0.80, partial\n+0.84 controlling diversity; "
          "A.11r/A.11y).\nUNION-SIZE rows are likely FALSE REJECTIONS: judge "
          "those on r/m." % UNION_MIN)
    print("r/m cutoff %.1f rests on ONE point either side, bracket %.2f-%.2f -- "
          "treat RM-LOW as 're-examine', not a verdict." % ((RM_MIN,) + RM_BRACKET))
    print("\nTHE UFBoot GATE IS WITHDRAWN (Tier 0.1). %d of the %d units passing "
          "detection have\na median UFBoot below %.0f and are RETAINED; they were "
          "previously dropped, costing\n8 units and 225 genomes on a threshold "
          "that is on the wrong scale (70 is the\nstandard-bootstrap convention, "
          "not UFBoot's, whose own line is 95). Collapse their\nunsupported "
          "branches with `collapse_unsupported_bp.py` instead of discarding them."
          % (len(low), len(usable), UFBOOT_REPORT))
    return 0


def selftest():
    fails = []

    def chk(desc, got, want, tol=1e-9):
        ok = abs(got - want) < tol if isinstance(want, float) else got == want
        if not ok:
            fails.append("%s: got %r want %r" % (desc, got, want))

    # Published A.11 rows must reproduce from the on-disk runs.
    for run, u_want, rm_want in (("reduced_cluster_34", 0.884, 12.12),
                                 ("reduced_cluster_15", 0.832, 3.38),
                                 ("reduced_cluster_10", 0.835, 1.73)):
        s = score_unit(os.path.join(SELF, run))
        if s is None:
            fails.append("%s: not scorable" % run)
            continue
        chk("%s union" % run, round(s["union"], 3), u_want, 6e-4)
        chk("%s r/m" % run, round(s["rm"], 2), rm_want, 6e-3)

    # Triage logic.
    # Both collapse -> genuine under-detection (cluster_62, cluster_53).
    chk("both low -> UNDER-DETECT", triage(0.007, 0.07, "yes")[0], "UNDER-DETECT")
    chk("cluster_53 -> UNDER-DETECT", triage(0.180, 1.25, "yes")[0], "UNDER-DETECT")
    # Contradiction -> its own label, NOT under-detection (s5_L1_2).
    chk("s5_L1_2 -> DISAGREE", triage(0.423, 8.54, "yes")[0], "DISAGREE")
    if "NOT under-detection" not in triage(0.423, 8.54, "yes")[1]:
        fails.append("DISAGREE note must say it is probably not under-detection")
    # A.11r: with n supplied, a small unit low on union but healthy on r/m is a
    # size artefact, not a disagreement of equals.
    chk("s5_L1_2 with n -> UNION-SIZE", triage(0.423, 8.54, "yes", 28)[0], "UNION-SIZE")
    chk("s2_L1_7 with n -> UNION-SIZE", triage(0.443, 5.90, "no_n_lt_25", 18)[0], "UNION-SIZE")
    chk("large unit keeps DISAGREE", triage(0.423, 8.54, "yes", 90)[0], "DISAGREE")
    # Both-low must still be UNDER-DETECT regardless of size.
    chk("small + both low -> UNDER-DETECT", triage(0.262, 0.79, "no_n_lt_25", 22)[0], "UNDER-DETECT")
    chk("low r/m -> RM-LOW", triage(0.80, 1.2, "no_n_lt_25")[0], "RM-LOW")
    chk("normal -> OK", triage(0.80, 7.2, "yes")[0], "OK")
    # s1_L1_27 (2.57) sits AT the bracket edge -> marginal, not a verdict.
    chk("s1_L1_27 -> RM-MARGINAL", triage(0.595, 2.57, "yes")[0], "RM-MARGINAL")
    chk("strain_13 -> RM-MARGINAL", triage(0.721, 2.89, "n/a", 36)[0], "RM-MARGINAL")
    # Clearly-low r/m is still RM-LOW, and must name the right group.
    chk("clear RM-LOW", triage(0.628, 2.03, "no_n_lt_25", 24)[0], "RM-LOW")
    if "n<25" not in triage(0.628, 2.03, "no_n_lt_25", 24)[1]:
        fails.append("unscreened sub-cluster must be named as such")
    if "PopPUNK strain" not in triage(0.72, 1.46, "n/a", 46)[1]:
        fails.append("a strain must NOT be described as the n<25 case")
    # cluster_15, the nearest working unit, must NOT be.
    chk("cluster_15 passes", triage(0.832, 3.38, "yes")[0], "OK")
    # An unscreened flag must name the compromise; a screened one must not.
    if "unscreened" not in triage(0.80, 1.2, "no_n_lt_25")[1]:
        fails.append("unscreened RM-LOW must say so")
    if "unexpected" not in triage(0.80, 1.2, "yes")[1]:
        fails.append("screened RM-LOW must flag as unexpected")

    # TIER 0.1 -- THE UFBoot GATE IS WITHDRAWN. Resolution must never change a
    # verdict. These are the regression tests for that contract: each pair is
    # identical except for UFBoot, and both members must agree.
    chk("resolved unit stays OK", triage(0.80, 7.2, "yes", 50, 95.0)[0], "OK")
    chk("UNRESOLVED no longer exists", triage(0.80, 7.2, "yes", 50, 53.0)[0], "OK")
    chk("a terrible UFBoot cannot drop a unit",
        triage(0.80, 7.2, "yes", 50, 12.0)[0], "OK")
    chk("UNION-SIZE is no longer gated",
        triage(0.40, 6.8, "no_n_lt_25", 21, 53.0)[0], "UNION-SIZE")
    chk("s16_L1_3 (r/m 10.43, UFBoot 43) is RETAINED",
        triage(0.291, 10.43, "no_n_lt_25", 8, 43.0)[0], "UNION-SIZE")
    chk("s1_L1_9, the floor anchor, is RETAINED",
        triage(0.738, 4.28, "yes", 90, 50.0)[0], "OK")
    chk("either side of the old 70 line agrees",
        triage(0.80, 7.2, "yes", 50, 69.9)[0] == triage(0.80, 7.2, "yes", 50, 70.0)[0],
        True)
    # A failing unit must NOT be relabelled by resolution either.
    chk("under-detect unaffected", triage(0.26, 0.79, "no_n_lt_25", 22, 95.0)[0],
        "UNDER-DETECT")
    chk("RM-LOW unaffected", triage(0.63, 2.03, "no_n_lt_25", 24, 95.0)[0], "RM-LOW")
    # Missing UFBoot must not silently reject.
    chk("no ufboot -> unchanged", triage(0.80, 7.2, "yes", 50, None)[0], "OK")
    chk("nan ufboot -> unchanged", triage(0.80, 7.2, "yes", 50, float("nan"))[0], "OK")

    # Resolution is still REPORTED -- withdrawing the gate must not lose the
    # information, only stop it deciding anything.
    if "RETAINED" not in resolution_note("OK", 43.0):
        fails.append("a low-support unit must be annotated as retained")
    if "collapse" not in resolution_note("OK", 43.0):
        fails.append("the annotation must point at the collapse remedy")
    chk("well-supported units get no note", resolution_note("OK", 96.0), "")
    chk("support at the reporting line is quiet", resolution_note("OK", 70.0), "")
    chk("failing units get no resolution note",
        resolution_note("UNDER-DETECT", 43.0), "")
    chk("missing ufboot gets no note", resolution_note("OK", float("nan")), "")

    for f in fails:
        print("FAIL " + f)
    print("selftest: %d checks failed" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
