"""Flag narration spoken while the on-screen line it paraphrases is NOT up.

Pairs the on-screen text timeline (trace_onscreen_text.py) with the narration
CSV. For each line, finds the on-screen string it shares the most content words
with; if that string's visible window does not contain the line's start, the
narration is describing a slide the viewer is no longer looking at.

NOTE Manim's Text.text comes back with the spaces stripped ("Shownfor106strains
inonerestrictedAsianlocale"), so words cannot be tokenized out of it. Match by
substring against the normalized on-screen string instead. Tokenizing it was
why the first version of this check reported zero on a clip with known defects.
"""
import json, sys, os, csv, re

STOP = set("""the a an and or of to in is are it its that this on for with as by be was
were from at not no so than then they them their there here what which when how does do
can any all one two has have had will would there into out up down more most other same
own only just also very each both while after before over under again further""".split())
MIN_SHARED = 3

SPOKEN = {"one":"1","two":"2","three":"3","four":"4","five":"5","six":"6","seven":"7",
          "eight":"8","nine":"9","ten":"10","eleven":"11","twelve":"12","twenty":"2",
          "thirty":"3","forty":"4","fifty":"5","sixty":"6","seventy":"7","eighty":"8",
          "ninety":"9","hundred":"100","thousand":"000","percent":"%","point":"."}

trace = json.load(open(sys.argv[1]))
narr_dirs = sys.argv[2].split(",")

def norm(s):
    return re.sub(r"[^a-z0-9%]", "", s.lower())

def content_words(s):
    return [w for w in re.findall(r"[a-z]+", s.lower())
            if w not in STOP and len(w) > 3]

flags = []
checked = 0
for scene, rows in trace.items():
    csvp = next((os.path.join(d, scene + ".csv") for d in narr_dirs
                 if os.path.isfile(os.path.join(d, scene + ".csv"))), None)
    if not csvp:
        print(f"  (no narration csv for {scene})"); continue
    for r in csv.DictReader(open(csvp)):
        checked += 1
        st, txt = float(r["start_s"]), r["text"]
        cw = content_words(txt)
        best = None
        for o in rows:
            on = norm(o["text"])
            shared = [w for w in cw if w in on]
            if len(shared) >= MIN_SHARED and (best is None or len(shared) > len(best[1])):
                best = (o, shared)
        if not best:
            continue
        o, shared = best
        if o["first"] - 0.6 <= st <= o["last"] + 0.6:
            continue
        off = st - o["last"] if st > o["last"] else st - o["first"]
        flags.append((scene, st, off, txt, o, shared))

print(f"checked {checked} lines against {sum(len(v) for v in trace.values())} on-screen strings\n")
for s, st, off, txt, o, sh in sorted(flags, key=lambda z: -abs(z[2])):
    when = (f"{off:.1f}s AFTER it was wiped" if off > 0
            else f"{abs(off):.1f}s BEFORE it appears")
    print(f"  {s} @ {st:6.2f}s   spoken {when}")
    print(f"      says      : {txt[:72]}")
    print(f"      on screen : {o['first']:.2f} -> {o['last']:.2f}  {o['text'][:58]}")
    print(f"      shared    : {', '.join(sh)}")
print(f"\n{len(flags)} flagged")
