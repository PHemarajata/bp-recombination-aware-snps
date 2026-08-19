#!/usr/bin/env python3
"""Add lineterminator="\\n" to every csv writer that currently defaults to CRLF.

Bug 2 in HANDOFF_A100_2026-08-19.md: csv.DictWriter/csv.writer default to
lineterminator="\\r\\n", and open(..., newline="") preserves it. Fix each writer
that lacks an explicit lineterminator. Idempotent — a writer already carrying
lineterminator= is left alone.

Usage:
    python3 fix_crlf_writers.py build_v4c_panel.py partition_v4c.sh [...]
    python3 fix_crlf_writers.py --check <files>   # report only, change nothing

Run it on BOTH boxes' copies. On the A100 the files are under ~/v4c_partition/.
"""
import re
import sys

# csv.writer(...) or csv.DictWriter(...) that does NOT already name lineterminator.
# Handles the call whether or not it spans the arg list; we only require the
# opening "csv.(DictW|w)riter(" and insert before its closing paren on that call.
CALL = re.compile(r'csv\.(DictWriter|writer)\(')

def fix_line(line):
    if 'lineterminator' in line:
        return line, 0
    out = line
    count = 0
    for m in CALL.finditer(line):
        # find the matching close paren for this call
        i = m.end()
        depth = 1
        while i < len(out) and depth:
            if out[i] == '(':
                depth += 1
            elif out[i] == ')':
                depth -= 1
            i += 1
        if depth == 0:
            close = i - 1
            out = out[:close] + ', lineterminator="\\n"' + out[close:]
            count += 1
            # re-scan from after our insertion is unnecessary for one-per-line use
            break
    return out, count

def main():
    args = sys.argv[1:]
    check = '--check' in args
    files = [a for a in args if a != '--check']
    if not files:
        sys.exit(__doc__)
    total = 0
    for path in files:
        try:
            src = open(path).read().splitlines(keepends=True)
        except OSError as e:
            print(f"  SKIP {path}: {e}")
            continue
        changed = 0
        for n, line in enumerate(src):
            if CALL.search(line) and 'lineterminator' not in line:
                new, c = fix_line(line)
                if c:
                    src[n] = new
                    changed += c
                    print(f"  {path}:{n+1}  + lineterminator")
        if changed and not check:
            open(path, 'w').write(''.join(src))
        total += changed
        tag = "would fix" if check else "fixed"
        print(f"{path}: {tag} {changed} writer(s)")
    if check:
        print(f"\n--check: {total} writer(s) need the fix (nothing written)")
    else:
        print(f"\ndone: {total} writer(s) patched")

if __name__ == "__main__":
    main()
