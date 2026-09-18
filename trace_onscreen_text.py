"""Dump when each on-screen text string appears and disappears in a Manim scene.

WHY THIS EXISTS. A clip can pass the duration, silence, gap and collision checks
and still be out of sync, because those all ask about TIMING and none asks about
CONTENT. TUC clip 2's act 2 narrates "the evidence is a hundred and six strains
in one Asian locale" twelve seconds after the on-screen line saying exactly that
has been wiped. The viewer sees the narration stuck on the previous slide.

Pair this with the narration CSV: if a line paraphrases an on-screen string, it
should be spoken while that string is visible.

Usage:  CLIP_SOURCE=scenes.py manim -ql --disable_caching trace_onscreen_text.py SceneName
"""
from manim import *
import os, json, importlib.util

CLIP_SOURCE = os.environ.get("CLIP_SOURCE", "tuc_clip2_scenes.py")
OUT = os.environ.get("TRACE_OUT", "onscreen_trace.json")
SEEN = {}


def _visible(scene):
    out = {}
    for m in scene.mobjects:
        for sub in m.get_family():
            if not isinstance(sub, Text):
                continue
            if len(sub.submobjects) == 0 and len(sub.points) == 0:
                continue
            ops = [float(getattr(g, "fill_opacity", 1.0) or 0.0)
                   for g in sub.get_family() if getattr(g, "fill_opacity", None) is not None]
            if ops and max(ops) <= 0.05:
                continue
            out[id(sub)] = sub.text
    return out


class Trace:
    def _snap(self):
        t = round(self.renderer.time, 2)
        vis = _visible(self)
        for k, txt in vis.items():
            r = SEEN.setdefault(k, {"text": txt, "first": t, "last": t})
            r["last"] = t

    def play(self, *a, **k):
        super().play(*a, **k); self._snap()

    def wait(self, *a, **k):
        super().wait(*a, **k); self._snap()

    def tear_down(self):
        rows = sorted(SEEN.values(), key=lambda r: (r["first"], r["last"]))
        name = type(self).__name__
        print("\n" + "=" * 74)
        print(f"ON-SCREEN TEXT TIMELINE: {name}")
        print("=" * 74)
        for r in rows:
            print(f"  {r['first']:6.2f} -> {r['last']:6.2f}   {r['text'][:58]}")
        print("=" * 74)
        path = OUT
        blob = json.load(open(path)) if os.path.isfile(path) else {}
        blob[name] = rows
        json.dump(blob, open(path, "w"), indent=1)
        super().tear_down()


_spec = importlib.util.spec_from_file_location("clipsrc", CLIP_SOURCE)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
for _n in dir(_mod):
    _o = getattr(_mod, _n)
    if isinstance(_o, type) and issubclass(_o, Scene) and _o is not Scene:
        globals()[_n] = type(_n, (Trace, _o), {})
