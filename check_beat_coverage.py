"""Interleave detected visual beats with narration line starts, per act.

A clip passes every duration and silence check and can still be out of sync:
the narration describes beat N while the picture already shows beat N+2. That
reads as "the narration is still on the previous slide" and nothing in the
toolchain looks for it.

Do NOT try to compute a cumulative lag by pairing beat i with line i. There are
usually more beats than lines, so that number grows by construction and means
nothing. The honest signal is structural: how many visual changes pass with
nothing said, and whether a line lands while the thing it names is still up.
"""
import json, sys, os, csv

beats = json.load(open(sys.argv[1]))
narr_dir = sys.argv[2]
only = set(sys.argv[3:]) or None

def clips(b):
    if isinstance(b, dict):
        for k in ("clips", "videos", "items"):
            if k in b: return b[k]
        return [dict(v, name=k) for k, v in b.items()]
    return b

worst = []
for c in clips(beats):
    name = os.path.splitext(os.path.basename(
        c.get("name") or c.get("video") or c.get("path")))[0]
    if only and name not in only: continue
    ev = sorted(float(x["t"]) if isinstance(x, dict) else float(x)
                for x in (c.get("beats") or c.get("moments") or []))
    csvp = os.path.join(narr_dir, name + ".csv")
    if not os.path.isfile(csvp): continue
    rows = list(csv.DictReader(open(csvp)))
    lines = [(float(r["start_s"]), float(r["start_s"]) + float(r["target_dur_s"]),
              r["text"]) for r in rows]
    print(f"\n===== {name}   {len(ev)} visual moments, {len(lines)} lines")
    prev_end = 0.0
    for i, (st, en, txt) in enumerate(lines):
        skipped = [t for t in ev if prev_end <= t < st]
        if len(skipped) >= 2:
            print(f"  {'':6}     ... {len(skipped)} visual changes pass unsaid "
                  f"({', '.join('%.1f' % t for t in skipped)})")
            worst.append((name, st, len(skipped)))
        print(f"  {st:6.2f}  {txt[:66]}")
        prev_end = en
    trailing = [t for t in ev if t >= prev_end]
    if len(trailing) >= 2:
        print(f"  {'':6}     ... {len(trailing)} visual changes after the last line")
print("\n--- places where two or more visual changes pass with nothing said ---")
for n, t, k in sorted(worst, key=lambda z: -z[2]):
    print(f"  {n:24s} at {t:6.2f}s  {k} changes skipped")
