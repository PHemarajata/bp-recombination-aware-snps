"""Report overlapping on-screen text in a Manim scene file.

The frame audit in the clip-production toolchain checks small text and clipping
but not collisions, so an overprint can be held on screen for twenty seconds and
still pass. This walks the live scene graph at every animation boundary instead
of looking at pixels, which is why it does not confuse a grid of filled squares
for a line of text.

Usage:  manim -ql --disable_caching check_text_collisions.py <SceneName>
        (the scene is imported from the module named by CLIP_SOURCE below)
"""
from manim import *
import os, itertools, importlib.util

CLIP_SOURCE = os.environ.get("CLIP_SOURCE", "tuc_clip1_scenes.py")
MIN_OVERLAP = 0.12          # fraction of the smaller box's area
REPORT = []


def _visible_texts(scene):
    out = []
    for m in scene.mobjects:
        for sub in m.get_family():
            if not isinstance(sub, Text):
                continue
            if len(sub.submobjects) == 0 and len(sub.points) == 0:
                continue
            if _opacity(sub) <= 0.05:
                continue
            out.append(sub)
    return out


def _opacity(m):
    """Max fill opacity over a Text's glyphs. Text itself often carries None."""
    vals = []
    for leaf in m.get_family():
        v = getattr(leaf, "fill_opacity", None)
        if v is None:
            continue
        try:
            vals.append(float(v))
        except (TypeError, ValueError):
            pass
    return max(vals) if vals else 1.0


def _box(m):
    return (m.get_left()[0], m.get_right()[0], m.get_bottom()[1], m.get_top()[1])


def _overlap(a, b):
    ix = min(a[1], b[1]) - max(a[0], b[0])
    iy = min(a[3], b[3]) - max(a[2], b[2])
    if ix <= 0 or iy <= 0:
        return 0.0
    inter = ix * iy
    sa = (a[1] - a[0]) * (a[3] - a[2])
    sb = (b[1] - b[0]) * (b[3] - b[2])
    small = min(sa, sb)
    return inter / small if small > 0 else 0.0


class CollisionCheck:
    """Mixin: snapshot the scene graph after every play() and wait()."""

    def _snapshot(self):
        t = round(self.renderer.time, 2)
        texts = _visible_texts(self)
        for a, b in itertools.combinations(texts, 2):
            f = _overlap(_box(a), _box(b))
            if f >= MIN_OVERLAP:
                ta, tb = a.text[:46], b.text[:46]
                REPORT.append((t, ta, tb, f))
        # reserved bottom eighth
        for m in texts:
            if m.get_bottom()[1] < -3.0 and m.text.strip():
                REPORT.append((t, m.text[:46], "<reserved bottom eighth>", 1.0))

    def play(self, *a, **k):
        super().play(*a, **k)
        self._snapshot()

    def wait(self, *a, **k):
        super().wait(*a, **k)
        self._snapshot()

    def tear_down(self):
        seen = {}
        for t, ta, tb, f in REPORT:
            seen.setdefault((ta, tb), []).append((t, f))
        print("\n" + "=" * 72)
        print(f"TEXT COLLISION REPORT: {type(self).__name__}")
        print("=" * 72)
        if not seen:
            print(f"  clean -- {len(_visible_texts(self))} text objects at final frame")
        for (ta, tb), v in seen.items():
            print(f"  t {v[0][0]:.1f}-{v[-1][0]:.1f}s  overlap {max(x[1] for x in v):.0%}")
            print(f"     A: {ta!r}")
            print(f"     B: {tb!r}")
        print("=" * 72)
        super().tear_down()


_spec = importlib.util.spec_from_file_location("clipsrc", CLIP_SOURCE)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

for _name in dir(_mod):
    _obj = getattr(_mod, _name)
    if isinstance(_obj, type) and issubclass(_obj, Scene) and _obj is not Scene:
        globals()[_name] = type(_name, (CollisionCheck, _obj), {})
