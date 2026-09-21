#!/usr/bin/env python3
"""
Point a build directory's spec at its own parts, wherever the directory now is.

`spec_v2.json` stores an ABSOLUTE path per clip. Move or rename the build
directory and every one of those paths dangles, so `build_narration.py` and
`assemble_voice.py` fail or, worse, quietly work against whatever still happens
to sit at the old path.

This has bitten three times in one day: a folder organizer nested every build
directory under `~/Downloads/TUC Films/`, restoring them broke nothing only
because they went back to the same names, and then one build directory was moved
to the Desktop and its nine paths went stale.

The fix is not to forbid moving the folder. It is to make the spec point at
whatever directory it is actually sitting in.

  python3 repoint_spec.py --spec PATH/beats/spec_v2.json        # repoint to its own dir
  python3 repoint_spec.py --spec ... --check                    # report only
  python3 repoint_spec.py --spec ... --parts-dir DIR            # explicit override

Only the directory part of each path changes. Filenames, line text, start times
and everything else are untouched.
"""
import argparse
import json
import io
import os
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--parts-dir",
                    help="where the parts really are. Default: the 'parts' "
                         "directory beside the spec's own build directory.")
    ap.add_argument("--check", action="store_true", help="report, write nothing")
    a = ap.parse_args()

    spec = os.path.abspath(os.path.expanduser(a.spec))
    if not os.path.isfile(spec):
        sys.exit("FATAL: %s not found." % spec)

    # spec lives at <build>/beats/spec_v2.json, so parts are at <build>/parts
    build = os.path.dirname(os.path.dirname(spec))
    parts = os.path.abspath(os.path.expanduser(a.parts_dir)) if a.parts_dir \
        else os.path.join(build, "parts")
    if not os.path.isdir(parts):
        sys.exit("FATAL: no parts directory at %s" % parts)

    s = json.load(open(spec))
    rows, changed, missing = [], 0, 0
    for c in s["clips"]:
        old = c["video"]
        name = os.path.basename(old)
        new = os.path.join(parts, name)
        ok_old = os.path.isfile(old)
        ok_new = os.path.isfile(new)
        if not ok_new:
            missing += 1
        if old != new:
            changed += 1
        rows.append((name, ok_old, ok_new, old != new))
        if not a.check:
            c["video"] = new

    print("spec  %s" % spec)
    print("parts %s" % parts)
    print()
    print("%-26s %-12s %-12s %s" % ("part", "old path", "new path", ""))
    for name, ok_old, ok_new, diff in rows:
        print("  %-24s %-12s %-12s %s"
              % (name, "resolves" if ok_old else "DANGLING",
                 "resolves" if ok_new else "MISSING",
                 "repointed" if diff else "unchanged"))
    print()
    if missing:
        sys.exit("FATAL: %d part(s) are not in %s. Nothing written."
                 % (missing, parts))
    if a.check:
        print("check only. %d of %d path(s) would change." % (changed, len(rows)))
        return
    if not changed:
        print("already correct, nothing written.")
        return
    io.open(spec, "w", encoding="utf-8").write(
        json.dumps(s, indent=2, ensure_ascii=False))
    print("repointed %d of %d path(s). Line text and start times untouched."
          % (changed, len(rows)))


if __name__ == "__main__":
    main()
