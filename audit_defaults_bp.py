#!/usr/bin/env python3
"""Fail if any script has an argparse INPUT default naming a specific run.

Six instances of one bug have now been found in this repository, and every one
produced a plausible wrong number rather than an error:

  E0  phylogeography_association_bp.py  --assignments/--trees  -> v1 paths
  E1  gate1_from_alignment_bp.py        --mash                 -> an 86-unit file
  E4  recomb_filtered_distances_bp.py   hardcoded r/m table
      gate1_from_alignment_bp.py        one window, two metrics -> 8.05 not 7.70
      manuscript_numbers_bp.py          same, in the manuscript's own numbers
      recomb_filtered_distances_bp.py   --clusters -> the HYBRID Clusters dir

They were all found by accident. This finds the next one on purpose, and runs in
CI so it cannot be reintroduced.

WHAT IS AND IS NOT FLAGGED. Only INPUT arguments: reading the wrong file silently
mixes bases, whereas writing to a stale output path is visible the moment you
look at it. Reference datasets that are not run artifacts are fine, and so are
defaults naming the reported run's own frozen artifacts, because those are the
ones you want. Both are allowlisted below by name, so an addition is a decision.

  python3 audit_defaults_bp.py        # exit 1 on any finding
"""
import ast
import os
import re
import sys

# Tokens that name a specific run, partition or hardware execution.
RUNISH = re.compile(
    r"L1_out|L1v3_out|L1v4b_out|L1v4c_out|L1_ASSIGNMENTS|86units|_86\b"
    r"|v3_|v4b_|trackA|A100|PANEL_v4|DISTANCES_v4c|Clusters|\.L1_run_",
    re.I)

# Arguments that READ. Writing somewhere stale is visible; reading is not.
INPUTISH = re.compile(
    r"^--(assign|trees|clusters|strains|rm$|mash|distance|diversity|panel|"
    r"partition|refbranch|input|meta|tree|aln|alignment)", re.I)

# Deliberate exceptions. Each is a decision, not an oversight.
ALLOW = {
    # The reported run's own frozen artifacts: these defaults are the ones you
    # want, and gate1_from_alignment_bp.py verifiably reproduces
    # GATE1_ALIGNMENT_2026-08-21.tsv with no arguments at all.
    ("gate1_from_alignment_bp.py", "--distances"),
    ("gate1_from_alignment_bp.py", "--rm"),
    ("manuscript_numbers_bp.py", "--rm"),
    # A published external reference dataset, not a run artifact.
    ("phylogeography_diagnostics_bp.py", "--clusters"),
}

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    findings = []
    for fn in sorted(f for f in os.listdir(here) if f.endswith(".py")):
        try:
            tree = ast.parse(open(os.path.join(here, fn)).read())
        except Exception:
            continue
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call)
                    and getattr(node.func, "attr", "") == "add_argument"):
                continue
            if not (node.args and isinstance(node.args[0], ast.Constant)):
                continue
            flag = node.args[0].value
            if not isinstance(flag, str) or not INPUTISH.match(flag):
                continue
            if (fn, flag) in ALLOW:
                continue
            for kw in node.keywords:
                if kw.arg != "default":
                    continue
                try:
                    val = ast.unparse(kw.value)
                except Exception:
                    continue
                if val in ("None", "True", "False") or val.isdigit():
                    continue
                if RUNISH.search(val):
                    findings.append((fn, node.lineno, flag, val))

    if findings:
        print("FAIL: input arguments defaulting to a specific run or partition.\n")
        for fn, ln, flag, val in findings:
            print(f"  {fn}:{ln}  {flag} = {val}")
        print("\nReading the wrong input does not raise; it produces a plausible")
        print("wrong number. Make the argument required, or add it to ALLOW here")
        print("with a comment saying why the default is the one you want.")
        return 1
    print(f"OK: no input argument defaults to a specific run "
          f"({len(ALLOW)} deliberate exceptions)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
