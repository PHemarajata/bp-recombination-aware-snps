"""Legacy five scenes, aligned to the house semantics. 2026-09-17.

Derived from ~/Downloads/ANIMO_DELIVERABLES_2026-09-09/source/scene.py, which is
the REVISED source: every section 11 fix was already applied there and rendered
on 2026-09-10. This file changes nothing about what those scenes do or how long
they take. All five render frame-for-frame identical in length to the delivered
clips, so every existing narration timing survives untouched.

What changed, and only this:

  PURPLE is reserved for geography in the house palette (aphl_common.py), and
  eight legacy uses were not geography: 7.03's mutation bar, label and percentage,
  and 7.12's detection curve, label, dot and caption. Both are a second measured
  or schematic quantity paired with a teal first, so both take the second teal
  step, TEAL_X #005057. Verified legible against TEAL #00A0AF at 7.03's flip.

  RUST is reserved for an adverse outcome, and the imported tract is the subject
  being detected, not a failure. The tract fill, stroke, label and its reveal
  toggle move to teal. Rust stays on NOT MARKED, the out-of-window dots, the
  below-floor and above-ceiling medians and the measured r/m verdict, which are
  all genuinely adverse.

  "group" becomes "unit", eight on-screen strings, one name per concept.

What deliberately did NOT change:

  The LOG diversity axes. An earlier merge spec called for adopting the house
  linear axis. That was wrong. 7.07 plots four values at 72, 123, 1310 and 1477,
  and on a linear axis 72 and 123 collapse together at the left edge, which
  destroys the clip's subject. The revision that drew the eighteen-fold drop
  considered exactly this and chose to keep log and annotate instead. 7.12 spans
  four orders of magnitude and needs log outright.

  The local seeds, random.Random(11), random.Random(20260909) and
  random.Random(7). Renders stay reproducible.

  Em dashes: there were none here. That sweep was only ever an APHL-side job.

Renders with Manim CE 0.21.0. Verified on macOS with all six Franklin Gothic
faces installed.
"""
from manim import *
import math, random

# ---------------------------------------------------------------------------
# APHL brand style. Five visuals: 7.1, 7.3, 7.7, 7.9, 7.12.
#
# PALETTE DISCIPLINE
#   #00A0AF is 3.2:1 on white -> fills, strokes and marks ONLY.
#   Any teal carrying a glyph uses #006E79 (6.0:1).
#   White knockout only on #006E79 / #005057 / #B42E34, never on #00A0AF.
#   Source line #6E6E6E (5.1:1). Every font_size >= 20.
#   Rust encodes a category only where that category IS the adverse outcome,
#   and the verdict is always named in text beside it.
#
# FONTS
#   Franklin Gothic is one family per weight, all faces reporting Regular, so
#   weight is selected by family name and weight= is never passed.
# ---------------------------------------------------------------------------

config.background_color = "#FFFFFF"

TEAL_D = "#006E79"      # text-safe teal
TEAL   = "#00A0AF"      # fills / strokes / marks only
TEAL_X = "#005057"
RUST   = "#B42E34"
PURPLE = "#9960A7"
INK    = "#404040"
RULE   = "#E2E9EC"
GRAY   = "#6E6E6E"
WHITE  = "#FFFFFF"

F_TITLE = "Franklin Gothic Medium"
F_BODY  = "Franklin Gothic Book"
F_EMPH  = "Franklin Gothic Demi"

Text.set_default(font=F_BODY, color=INK)


# Pango/cairo hint glyph advances to whole pixels at the size Text is laid out
# at, so a small font_size quantises inter-letter spacing coarsely and the
# error is then magnified when manim scales the vector result. Laying out at a
# large reference size and scaling down makes that rounding negligible.
# The reference cannot be arbitrarily large: past roughly 30 scene units of
# laid-out width manim wraps the string, which silently turns a one-line label
# into two. 48 is comfortably clear of that for every string in this deck, and
# _crisp steps the reference down if a future string ever does wrap.
REF_FS = 48
_LINE_H = 0.0120          # single-line height per unit of font_size


def _crisp(txt, size, font, color):
    want = txt.count("\n") + 1
    ref = REF_FS
    while True:
        m = Text(txt, font=font, font_size=ref, color=color)
        if max(1, round(m.height / (ref * _LINE_H))) <= want or ref <= 24:
            break
        ref -= 8
    m.scale(max(size, 20) / ref)
    return m


def T(t, size, color=TEAL_D):
    return _crisp(t, size, F_TITLE, color)


def L(t, size, color=INK, emph=False):
    return _crisp(t, size, F_EMPH if emph else F_BODY, color)


def source(scene, txt):
    s = L(txt, 20, GRAY)
    s.move_to([-6.30, -3.56, 0]).align_to([-6.30, -3.56, 0], LEFT)
    scene.add(s)
    return s


# ===========================================================================
# 7.1  The negative control
#
# REVISED per review.
#   1. The zoom used to run seven seconds in which only a corner readout
#      changed. An approach marker now slides in from the right edge, so
#      something is visibly closing the distance for the whole traverse.
#   2. The null used to shrink to a hairline and vanish exactly when the clip
#      made its claim about the null. An inset now holds it at its own fixed
#      scale, so BOTH compared objects are on screen at the moment of
#      comparison.
#   3. One name only. The clip used to say "no-template control" and then
#      "negative control" within six seconds.
#
# Continuous axis rescale: the change of scale IS the finding, so the scale
# stays linear, ticks update continuously, and the domain is shown numerically.
# ===========================================================================

XMAX_0, XMAX_1 = 0.008, 16.0
NULL_MAX = 0.00668
REAL_LO, REAL_HI = 2.85, 14.92
AXL1, AXR1, AXY1 = -5.50, 4.90, -1.15
INL, INR, INY = 3.30, 6.15, 2.02          # the inset, at its own fixed scale


class NegativeControlZoom(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        t0 = T("The no-template control", 42)
        s0 = L("Every laboratory runs one. You load the reaction with no template\n"
               "and you see what the machine reports anyway.", 24)
        s0.next_to(t0, DOWN, buff=0.40)
        VGroup(t0, s0).move_to(ORIGIN)
        self.play(Write(t0), run_time=1.2)                               # 0.0
        self.play(FadeIn(s0, shift=DOWN * 0.2), run_time=1.0)            # 1.2
        self.wait(1.2)                                                   # 2.2
        hdr = T("The no-template control", 32)                           # same name, once
        hdr.to_edge(UP, buff=0.45).to_edge(LEFT, buff=0.82)
        self.play(FadeOut(s0, shift=UP * 0.2), ReplacementTransform(t0, hdr),
                  run_time=1.0)                                          # 3.4
        source(self, "Source: negative control, 1,519 replicates over 62 unit-replicons.")
        meth = L("Simulate genomes with zero recombination. "
                 "Run the identical pipeline.", 24).move_to([0, 0.90, 0])
        self.play(FadeIn(meth), run_time=0.8)                            # 4.4
        self.wait(1.4)                                                   # 5.2
        self.play(FadeOut(meth), run_time=0.5)                           # 6.6

        t = ValueTracker(0.0)
        xmax = lambda: XMAX_0 * (XMAX_1 / XMAX_0) ** t.get_value()
        vx = lambda v: AXL1 + (v / xmax()) * (AXR1 - AXL1)

        axis = Line([AXL1, AXY1, 0], [AXR1, AXY1, 0], color=INK, stroke_width=1.6)

        def nice(xm):
            raw = xm / 4.0
            e = math.floor(math.log10(raw)); m = raw / 10.0 ** e
            for cc in (1.0, 2.0, 2.5, 5.0):
                if m <= cc:
                    return cc * 10.0 ** e
            return 10.0 ** (e + 1)

        def ticks():
            xm = xmax(); st = nice(xm); g = VGroup(); k = 0
            while k * st <= xm * 1.0001 and k < 40:
                v = k * st; x = vx(v)
                if x <= AXR1 + 0.02:
                    dd = max(0, -int(math.floor(math.log10(st) + 1e-9)))
                    lb = f"{v:,.0f}" if st >= 1 else f"{v:.{dd}f}"
                    g.add(Line([x, AXY1, 0], [x, AXY1 - 0.13, 0], color=INK, stroke_width=1.6),
                          L(lb, 20).move_to([x, AXY1 - 0.38, 0]))
                k += 1
            return g

        self.play(Create(axis), run_time=0.8)                            # 7.1
        self.add(always_redraw(ticks))
        axcap = L("r/m, recombination relative to mutation", 20)
        axcap.move_to([(AXL1 + AXR1) / 2, AXY1 - 0.80, 0])
        self.play(FadeIn(axcap), run_time=0.5)                           # 7.9

        nband = always_redraw(lambda: Rectangle(
            width=max(vx(NULL_MAX) - vx(0.0), 0.004), height=1.05,
            fill_color=TEAL, fill_opacity=0.35, stroke_color=TEAL, stroke_width=2
        ).move_to([(vx(0.0) + vx(NULL_MAX)) / 2, AXY1 + 0.55, 0]))
        rnd = random.Random(11)
        pool = sorted(rnd.uniform(0.04, 0.96) for _ in range(20))
        calls = lambda: VGroup(*[Dot([vx(NULL_MAX * f), AXY1 + 0.42, 0],
                                     radius=0.045, color=TEAL_X)
                                 for f in pool if vx(NULL_MAX * f) <= AXR1])
        self.play(FadeIn(nband), run_time=0.6)                           # 8.4
        intro = calls()
        self.play(LaggedStart(*[GrowFromCenter(x) for x in intro], lag_ratio=0.05),
                  run_time=1.0)                                          # 9.0
        self.remove(*intro)
        self.add(always_redraw(calls))

        caps = VGroup(
            L("1,519 replicates over 62 unit-replicons", 23),
            L("20 of them returned any call at all, which is 1.32%", 23, TEAL_D, emph=True),
            L("The largest value ever returned was 0.00668", 23),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        caps.next_to(hdr, DOWN, buff=0.38).align_to(hdr, LEFT)
        self.play(FadeIn(caps[0], shift=DOWN * 0.15), run_time=0.7)      # 10.0
        self.wait(1.7)                                                   # 10.7
        self.play(FadeIn(caps[1], shift=DOWN * 0.15), run_time=0.7)      # 12.4
        self.wait(1.6)                                                   # 13.1
        self.play(FadeIn(caps[2], shift=DOWN * 0.15), run_time=0.7)      # 14.7
        self.wait(1.6)                                                   # 15.4

        prompt = L("Now hold the axis linear and widen it until the real units appear.", 22)
        prompt.next_to(caps, DOWN, buff=0.30).align_to(caps, LEFT)
        self.play(FadeOut(caps, shift=UP * 0.2), FadeIn(prompt), run_time=0.8)   # 17.0

        # ---- the inset keeps the null on screen at its own scale, permanently
        ibox = Rectangle(width=INR - INL, height=0.86, stroke_color=RULE,
                         stroke_width=1.6, fill_color=WHITE, fill_opacity=1.0)
        ibox.move_to([(INL + INR) / 2, INY, 0])
        iax = Line([INL + 0.12, INY - 0.26, 0], [INR - 0.12, INY - 0.26, 0],
                   color=INK, stroke_width=1.2)
        iw = (INR - 0.12) - (INL + 0.12)
        inull = Rectangle(width=iw * (NULL_MAX / XMAX_0), height=0.34,
                          fill_color=TEAL, fill_opacity=0.35,
                          stroke_color=TEAL, stroke_width=1.6)
        inull.move_to([INL + 0.12 + iw * (NULL_MAX / XMAX_0) / 2, INY - 0.07, 0])
        idots = VGroup(*[Dot([INL + 0.12 + iw * (NULL_MAX / XMAX_0) * f, INY - 0.13, 0],
                             radius=0.026, color=TEAL_X) for f in pool])
        icap = L("the null, held at its own scale", 20, GRAY)
        icap.move_to([(INL + INR) / 2, INY + 0.62, 0])
        inset = VGroup(ibox, iax, inull, idots, icap)
        self.play(FadeIn(inset), run_time=0.8)                           # 17.8

        readout = always_redraw(lambda: VGroup(
            L("full width of this axis", 20, GRAY),
            L(f"r/m 0 to {xmax():,.3f}" if xmax() < 1 else f"r/m 0 to {xmax():,.2f}",
              26, INK, emph=True),
        ).arrange(DOWN, buff=0.10).move_to([(INL + INR) / 2, INY + 1.20, 0]))
        self.play(FadeIn(readout), run_time=0.6)                         # 18.6
        self.wait(1.2)                                                   # 19.2

        # ---- the approach marker: pinned at the edge, then it closes in
        def approach():
            x = vx(REAL_LO)
            pinned = x > AXR1 - 0.30
            xx = min(x, AXR1 - 0.30)
            tri = Triangle(fill_color=RUST, fill_opacity=1.0, stroke_width=0)
            tri.rotate(-PI / 2).scale(0.16).move_to([xx + 0.16, AXY1 + 0.55, 0])
            if not pinned:
                return VGroup()
            lab = L("real units", 20, RUST).next_to(tri, UP, buff=0.14)
            return VGroup(tri, lab)
        self.add(always_redraw(approach))

        rband = always_redraw(lambda: Rectangle(
            width=max(vx(min(REAL_HI, xmax())) - vx(REAL_LO), 0.001), height=1.05,
            fill_color=RUST, fill_opacity=0.35, stroke_color=RUST, stroke_width=2
        ).move_to([(vx(REAL_LO) + vx(min(REAL_HI, xmax()))) / 2, AXY1 + 0.55, 0])
            if xmax() > REAL_LO * 1.02 else VMobject())
        self.add(rband)
        self.add(always_redraw(lambda: Line([vx(0.0), AXY1, 0], [vx(0.0), AXY1 + 0.55, 0],
                                            color=TEAL_X, stroke_width=3)))

        self.play(t.animate.set_value(1.0), run_time=10.6, rate_func=smooth)   # 20.4 -> 31.0
        self.play(FadeOut(prompt), run_time=0.5)                         # 31.0

        nl = VGroup(L("everything the null ever produced", 20, TEAL_D),
                    L("0 to 0.00668", 22, TEAL_D, emph=True)).arrange(DOWN, buff=0.09)
        nl.move_to([vx(0.0) + 1.70, AXY1 + 2.02, 0])
        rl = VGroup(L("real analysis units", 20, RUST),
                    L("2.85 to 14.92", 22, RUST, emph=True)).arrange(DOWN, buff=0.09)
        rl.move_to([(vx(REAL_LO) + vx(REAL_HI)) / 2, AXY1 + 2.02, 0])
        self.play(FadeIn(nl, shift=DOWN * 0.15), FadeIn(rl, shift=DOWN * 0.15),
                  run_time=0.9)                                          # 31.5
        self.wait(1.8)                                                   # 32.4

        sep = T("Separation of 427x to 2,234x", 34, RUST)
        sep.next_to(hdr, DOWN, buff=0.40).align_to(hdr, LEFT)
        self.play(FadeIn(sep, shift=DOWN * 0.2), run_time=0.9)           # 34.2
        self.wait(2.3)                                                   # 35.1
        close = L("The tool is not manufacturing recombination.", 26, INK, emph=True)
        close.next_to(sep, DOWN, buff=0.24).align_to(sep, LEFT)
        self.play(FadeIn(close, shift=DOWN * 0.15), run_time=0.9)        # 37.4
        self.wait(3.2)                                                   # 38.3


# ===========================================================================
# 7.3  The detection window mechanism, deliverable section 3
#
# REVISED 2026-09-10 per brief section 11.2.
#   1. The counted-as bars are promoted to co-star with the genome track.
#      They are the mechanism the paper rests on, recombination moving out of
#      the numerator and into the denominator, and they were a low-contrast
#      footnote. They are now large, labeled and carry the percentages.
#   2. Dwell on the three real anchors, sprint between them. The readout used
#      to tick through about 44 values when only three matter, which trains
#      the eye to ignore it.
#   3. New beat at the above-ceiling state: the outline is hidden and the
#      audience is asked to find the imported piece. They cannot. That is the
#      finding experienced rather than watched, and the detector fails in
#      exactly the same way.
#
# The imported piece STILL never moves and never resizes. Only the background
# changes, and hiding an outline is not a move.
#
# Window [700, 4700] alignment-derived mean pairwise core SNPs.
# Anchors, each the unit closest to its own class median r/m:
#   strain_4_L1_1    243.3  r/m 1.25  below floor
#   strain_1_L1_23  1284.1  r/m 7.70  in window
#   strain_1_L1_11  5818.9  r/m 2.04  above ceiling
# Class medians: below 1.32, in 7.70, above 2.14. All 85 units as a strip,
# with NO curve fitted through them.
# ===========================================================================

TRK_L, TRK_R, TRK_Y, TRK_H = -5.90, 5.90, 2.28, 0.42
TR_A, TR_B = 0.615, 0.775
AX3_Y, AX3L, AX3R = -2.42, -5.30, 5.30
FLOOR, CEIL = 700.0, 4700.0
D3MIN = 15.0
ANCH3 = [(243.3, "strain_4_L1_1", 1.25, "below the floor"),
         (1284.1, "strain_1_L1_23", 7.70, "in the window"),
         (5818.9, "strain_1_L1_11", 2.04, "above the ceiling")]
U3 = [(15.4,'below'),(40.6,'below'),(42.8,'below'),(113.9,'below'),(121.5,'below'),(211.0,'below'),(243.3,'below'),(285.6,'below'),(405.0,'below'),(511.2,'below'),(535.0,'below'),(587.6,'below'),(754.8,'in'),(797.0,'in'),(840.1,'in'),(852.2,'in'),(909.4,'in'),(1032.9,'in'),(1120.5,'in'),(1121.3,'in'),(1284.1,'in'),(1310.3,'in'),(1334.7,'in'),(1348.8,'in'),(1355.2,'in'),(1433.8,'in'),(1513.6,'in'),(1573.9,'in'),(1595.7,'in'),(1610.4,'in'),(1676.1,'in'),(1828.5,'in'),(1908.8,'in'),(1949.9,'in'),(1996.3,'in'),(2010.3,'in'),(2014.6,'in'),(2109.1,'in'),(2211.5,'in'),(2259.7,'in'),(2298.9,'in'),(2449.1,'in'),(2738.6,'in'),(3020.5,'in'),(3020.7,'in'),(3079.6,'in'),(3363.0,'in'),(3374.8,'in'),(3402.6,'in'),(3417.2,'in'),(3424.0,'in'),(3452.1,'in'),(3759.3,'in'),(3903.0,'in'),(4011.6,'in'),(4247.0,'in'),(4463.1,'in'),(4524.9,'in'),(4631.8,'in'),(4731.6,'above'),(4750.2,'above'),(4923.3,'above'),(5168.5,'above'),(5198.0,'above'),(5721.1,'above'),(5818.9,'above'),(6094.2,'above'),(6213.6,'above'),(6361.8,'above'),(6364.6,'above'),(6386.6,'above'),(6531.6,'above'),(6629.2,'above'),(6796.8,'above'),(6839.4,'above'),(6909.7,'above'),(7207.9,'above'),(7430.6,'above'),(7775.7,'above'),(8197.2,'above'),(8342.7,'above'),(8541.1,'above'),(8648.0,'above'),(8756.6,'above'),(9131.1,'above')]

_r3 = random.Random(20260909)
_bgp = []
while len(_bgp) < 170:
    f = _r3.random()
    if not (TR_A - 0.012 < f < TR_B + 0.012):
        _bgp.append(f)
_trp = [TR_A + 0.012 + _r3.random() * (TR_B - TR_A - 0.024) for _ in range(26)]

nbg = lambda d: max(1, min(165, int(round(28.0 * (d / 1284.1) ** 0.90))))
ntr = lambda d: max(1, int(round(22.0 * (1.0 - math.exp(-d / 450.0)))))
det3 = lambda d: FLOOR <= d <= CEIL
fx3 = lambda f: TRK_L + f * (TRK_R - TRK_L)
sxd3 = lambda d: AX3L + (math.log10(d) - 1.0) / 3.0 * (AX3R - AX3L)


class DetectionWindowSweep(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        d = ValueTracker(D3MIN)
        rev = ValueTracker(1.0)          # 1 = piece outlined, 0 = outline hidden

        t0 = T("How the detector actually works", 40)
        s0 = L("It looks for a local excess of SNP density against the\n"
               "genome-wide background. That is the whole trick.", 24)
        s0.next_to(t0, DOWN, buff=0.40)
        VGroup(t0, s0).move_to(ORIGIN)
        self.play(Write(t0), run_time=1.2)                                  # 0.0
        self.play(FadeIn(s0, shift=DOWN * 0.2), run_time=1.0)               # 1.2
        self.wait(1)                                                        # 2.2
        hdr = T("The detection window", 32).to_edge(UP, buff=0.45).to_edge(LEFT, buff=0.82)
        self.play(FadeOut(s0, shift=UP * 0.2), ReplacementTransform(t0, hdr),
                  run_time=1.0)                                             # 3.2
        source(self, "Source: 85 analysis units. Track and bars are schematic.")

        track = Rectangle(width=TRK_R - TRK_L, height=TRK_H, stroke_color=INK,
                          stroke_width=1.4, fill_color=WHITE, fill_opacity=1.0)
        track.move_to([(TRK_L + TRK_R) / 2, TRK_Y, 0])
        tract = always_redraw(lambda: Rectangle(
            width=(TR_B - TR_A) * (TRK_R - TRK_L), height=TRK_H,
            stroke_color=TEAL, stroke_width=2.2 * rev.get_value(),
            fill_color=TEAL, fill_opacity=0.10 * rev.get_value()
        ).move_to([fx3((TR_A + TR_B) / 2), TRK_Y, 0]))
        tlab = always_redraw(lambda: L("one imported piece", 20, TEAL_D)
                             .set_opacity(rev.get_value())
                             .next_to(track, UP, buff=0.12)
                             .align_to([fx3(TR_B), 0, 0], RIGHT))
        self.play(Create(track), run_time=0.8)                              # 4.2
        self.add(tract, tlab)
        fixed = L("The imported piece never changes. Only the background does.",
                  23, INK, emph=True).move_to([0, 1.42, 0])
        self.play(FadeIn(fixed), run_time=0.9)                              # 5.0
        self.wait(1.4)                                                      # 5.9
        self.play(FadeOut(fixed), run_time=0.5)                             # 7.3

        def marks():
            cur = d.get_value(); g = VGroup()
            trc = TEAL if rev.get_value() > 0.5 else GRAY
            for f in _bgp[:nbg(cur)]:
                g.add(Line([fx3(f), TRK_Y - TRK_H / 2 + 0.05, 0],
                           [fx3(f), TRK_Y + TRK_H / 2 - 0.05, 0],
                           color=GRAY, stroke_width=1.6))
            for f in _trp[:ntr(cur)]:
                g.add(Line([fx3(f), TRK_Y - TRK_H / 2 + 0.05, 0],
                           [fx3(f), TRK_Y + TRK_H / 2 - 0.05, 0],
                           color=trc, stroke_width=2.1))
            return g
        self.add(always_redraw(marks))

        vd = always_redraw(lambda: (
            L("MARKED as imported", 26, TEAL_D, emph=True) if det3(d.get_value())
            else L("NOT MARKED", 26, RUST, emph=True)).move_to([0, 1.52, 0]))
        rs = always_redraw(lambda: L(
            "almost no SNPs anywhere, so nothing stands out" if d.get_value() < FLOOR else
            ("the piece is denser than its background, so it is found"
             if d.get_value() <= CEIL else
             "SNPs are dense everywhere, so the piece looks ordinary"),
            21, INK).move_to([0, 1.10, 0]))
        self.add(vd, rs)

        # ---------- the bars, promoted to co-star ----------
        BL, BM, BH = -2.05, 4.85, 0.50
        bhead = L("where those SNPs get counted", 21, GRAY)
        bhead.move_to([BL, 0.74, 0]).align_to([BL, 0, 0], LEFT)
        rl = L("recombination", 22, TEAL_D, emph=True)
        rl.move_to([BL - 0.22, 0.26, 0]).align_to([BL - 0.22, 0, 0], RIGHT)
        ml = L("mutation", 22, TEAL_X, emph=True)
        ml.move_to([BL - 0.22, -0.40, 0]).align_to([BL - 0.22, 0, 0], RIGHT)

        def shares():
            cur = d.get_value(); b, t = nbg(cur), ntr(cur)
            rec = t / (b + t) if det3(cur) else 0.0
            return rec, 1.0 - rec

        def mkbar(idx, col, y):
            def f():
                w = max(shares()[idx] * BM, 0.004)
                return Rectangle(width=w, height=BH, fill_color=col,
                                 fill_opacity=1.0, stroke_width=0).move_to([BL + w / 2, y, 0])
            return f
        pct = always_redraw(lambda: VGroup(
            L(f"{100*shares()[0]:.0f}%", 30, TEAL_D, emph=True).move_to([BL + BM + 0.62, 0.26, 0]),
            L(f"{100*shares()[1]:.0f}%", 30, TEAL_X, emph=True).move_to([BL + BM + 0.62, -0.40, 0])))
        bar_r = always_redraw(mkbar(0, TEAL, 0.26))
        bar_m = always_redraw(mkbar(1, TEAL_X, -0.40))
        self.play(FadeIn(bhead), FadeIn(rl), FadeIn(ml), run_time=0.7)      # 7.8
        self.add(bar_r, bar_m, pct)

        ax = Line([AX3L, AX3_Y, 0], [AX3R, AX3_Y, 0], color=INK, stroke_width=1.6)
        win = Rectangle(width=sxd3(CEIL) - sxd3(FLOOR), height=0.56, fill_color=TEAL,
                        fill_opacity=0.16, stroke_color=TEAL, stroke_width=1.6)
        win.move_to([(sxd3(FLOOR) + sxd3(CEIL)) / 2, AX3_Y + 0.10, 0])
        wtx = L("the working window, 700 to 4,700", 20, TEAL_D)
        wtx.move_to([(sxd3(FLOOR) + sxd3(CEIL)) / 2, AX3_Y + 0.58, 0])
        xt = VGroup()
        for v, lb in [(10, "10"), (100, "100"), (1000, "1,000"), (10000, "10,000")]:
            x = sxd3(v)
            xt.add(Line([x, AX3_Y, 0], [x, AX3_Y - 0.12, 0], color=INK, stroke_width=1.6),
                   L(lb, 20).move_to([x, AX3_Y - 0.36, 0]))
        axtx = L("mean pairwise core SNPs in the unit", 20)
        axtx.move_to([AX3R, AX3_Y - 0.72, 0]).align_to([AX3R, 0, 0], RIGHT)
        jr = random.Random(7)
        dots = VGroup(*[Dot([sxd3(v), AX3_Y + 0.10 + (jr.random() - 0.5) * 0.26, 0],
                            radius=0.034, color=(TEAL if c == 'in' else RUST),
                            fill_opacity=0.85) for v, c in U3])
        self.play(Create(ax), FadeIn(xt, lag_ratio=0.12), FadeIn(axtx), run_time=1.0)  # 8.5
        self.play(FadeIn(win), FadeIn(wtx), FadeIn(dots, lag_ratio=0.01), run_time=1.0)  # 9.5
        self.add(always_redraw(lambda: Line([sxd3(d.get_value()), AX3_Y - 0.24, 0],
                                            [sxd3(d.get_value()), AX3_Y + 0.42, 0],
                                            color=INK, stroke_width=3)))
        self.add(always_redraw(lambda: VGroup(
            L("unit diversity", 20, GRAY),
            L(f"{d.get_value():,.0f} SNPs", 28, INK, emph=True),
        ).arrange(DOWN, buff=0.10).to_corner(UR, buff=0.50)))
        self.wait(4.0)                                                      # 10.5  dwell, NOT MARKED

        def anchor(div, unit, rm, where):
            col = TEAL_D if where == "in the window" else RUST
            return VGroup(
                VGroup(L(unit, 20, INK, emph=True),
                       L(f"{div:,.0f} SNPs, {where}", 20)).arrange(RIGHT, buff=0.26),
                L(f"measured r/m {rm:.2f}", 23, col, emph=True),
            ).arrange(DOWN, buff=0.13).move_to([0, -1.24, 0])

        # ---------- sprint, then dwell. one anchor at a time ----------
        a = anchor(*ANCH3[0])
        self.play(d.animate.set_value(ANCH3[0][0]), run_time=1.1, rate_func=smooth)  # 14.5
        self.play(FadeIn(a), run_time=0.8)                                  # 15.6
        self.wait(4.4)                                                      # 16.4  dwell
        self.play(FadeOut(a), run_time=0.4)                                 # 20.8
        b = anchor(*ANCH3[1])
        self.play(d.animate.set_value(ANCH3[1][0]), run_time=1.0, rate_func=smooth)  # 21.2
        self.play(FadeIn(b), run_time=0.8)                                  # 22.2
        self.wait(4.8)                                                      # 23.0  dwell
        self.play(FadeOut(b), run_time=0.4)                                 # 27.8
        c = anchor(*ANCH3[2])
        self.play(d.animate.set_value(ANCH3[2][0]), run_time=1.4, rate_func=smooth)  # 28.2
        self.play(FadeIn(c), run_time=0.8)                                  # 29.6
        self.wait(3.0)                                                      # 30.4  dwell

        # ---------- hide the outline. the audience fails, and so did the tool ----------
        ask = L("the piece is still exactly where it was. can you find it?",
                22, INK, emph=True).move_to([0, -1.24, 0])
        self.play(FadeOut(c), run_time=0.4)                                 # 33.4
        self.play(rev.animate.set_value(0.0), FadeIn(ask), run_time=0.9)    # 33.8
        self.wait(2.6)                                                      # 34.7  the failure
        self.play(rev.animate.set_value(1.0), FadeOut(ask), run_time=0.9)   # 37.3
        self.wait(0.3)                                                      # 38.2

        s1 = L("Too similar and too different both give a low number.", 24, INK, emph=True)
        s1.move_to([0, -1.24, 0])
        self.play(FadeIn(s1), run_time=0.9)                                 # 38.5
        self.wait(3.6)                                                      # 39.4
        meds = VGroup(
            L("below floor    median r/m 1.32", 22, RUST),
            L("in window      median r/m 7.70", 22, TEAL_D, emph=True),
            L("above ceiling  median r/m 2.14", 22, RUST),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to([0, 0.06, 0])
        self.play(FadeOut(s1), run_time=0.4)                                # 43.0
        self.remove(bar_r, bar_m, pct)
        self.play(FadeOut(rl), FadeOut(ml), FadeOut(bhead), run_time=0.4)   # 43.4
        self.play(FadeIn(meds, lag_ratio=0.3), run_time=1.1)                # 43.8
        self.wait(1.4)                                                      # 44.9
        self.remove(vd, rs)
        last = L("The number alone cannot tell you which one you have.",
                 25, RUST, emph=True).move_to([0, 1.32, 0])
        self.play(FadeIn(last), run_time=0.9)                               # 46.3
        self.wait(0.6)                                                      # 47.2


# ===========================================================================
# 7.7  Recursive subdivision
#
# REVISED per review.
#   1. The bar and the plot are two views of the same objects and nothing
#      linked them. Each segment now FLIES from the bar down to its own
#      position on the diversity axis, so identity is shown, not inferred.
#      The bar stays intact behind, so conservation still reads.
#   2. The eighteen-fold drop is now drawn. The parent at 1,310 against its
#      own n = 98 child at 72 is a factor of eighteen, and on a log axis that
#      reads as a small step, so it is annotated explicitly.
#
# One level of subdivision only. The n = 98 child carries 72, recomputed on
# its own membership, not the unsplit parent's 1,310.
# ===========================================================================

B7L, B7R, B7Y, B7H = -4.50, 4.50, 1.86, 0.42
A7L, A7R, A7Y = -2.00, 3.05, -2.55
R7P, R7_1, R7_2, R7_3 = -0.15, -0.85, -1.45, -2.05
PFX7, NAME7, NUM7, RM7, CLS7 = -6.30, -5.32, -3.10, 3.95, 5.40
PAR7 = ("strain_1_L1_26", 153, 1310, 4.47, "in window")
KID7 = [("strain_1_L1_26", 98, 72, 1.07, "below window", R7_1),
        ("strain_1_L1_36", 47, 1477, 6.68, "in window", R7_2),
        ("strain_1_L1_37", 8, 123, 2.63, "below window", R7_3)]
sxd7 = lambda d: A7L + (math.log10(d) - 1.0) / (math.log10(3000.0) - 1.0) * (A7R - A7L)


class RecursiveSubdivision(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        title = T("What dividing a unit costs you", 36)
        title.to_edge(UP, buff=0.42).to_edge(LEFT, buff=0.82)
        sub = L("One analysis unit, divided once, on real data", 22)
        sub.next_to(title, DOWN, buff=0.20).align_to(title, LEFT)
        self.play(Write(title), run_time=1.2)                              # 0.0
        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.9)             # 1.2
        self.wait(2.1)                                                     # 2.1
        source(self, "Source: Table 3, the strain_1_L1_26 refinement.")

        bar = Rectangle(width=B7R - B7L, height=B7H, fill_color=TEAL_D,
                        fill_opacity=1.0, stroke_width=0)
        bar.move_to([(B7L + B7R) / 2, B7Y, 0])
        pname = VGroup(L(PAR7[0], 22, INK, emph=True),
                       L("before the division", 20, GRAY)).arrange(RIGHT, buff=0.30)
        pname.next_to(bar, UP, buff=0.16).align_to(bar, LEFT)
        pstat = L("153 genomes    1,310 mean pairwise core SNPs    r/m 4.47    in window", 20)
        pstat.next_to(bar, DOWN, buff=0.16).align_to(bar, LEFT)
        self.play(Create(bar), run_time=1.0)                               # 4.2
        self.play(FadeIn(pname, shift=DOWN * 0.15), FadeIn(pstat, shift=UP * 0.15),
                  run_time=0.8)                                            # 5.2
        self.wait(2.2)                                                     # 6.0
        why = L("The evidence that it held two populations was unambiguous, "
                "so it was divided.", 21).move_to([0, 1.00, 0])
        self.play(FadeIn(why, shift=UP * 0.2), run_time=0.9)               # 8.2
        self.wait(3.1)                                                     # 9.1

        segs, acc = VGroup(), 0.0
        for nm, n, dv, rm, cls, rw in KID7:
            x0 = B7L + (acc / 153.0) * (B7R - B7L)
            x1 = B7L + ((acc + n) / 153.0) * (B7R - B7L)
            acc += n
            segs.add(Rectangle(width=(x1 - x0) - 0.05, height=B7H, fill_color=TEAL_D,
                               fill_opacity=1.0, stroke_width=0
                               ).move_to([(x0 + x1) / 2, B7Y, 0]))
        self.play(FadeOut(why, shift=UP * 0.2), run_time=0.6)              # 12.2
        self.play(Transform(bar, segs), run_time=1.2, rate_func=smooth)    # 12.8
        seglabs = VGroup(*[L(str(k[1]), 21, WHITE, emph=True).move_to(r.get_center())
                           for r, k in zip(segs, KID7)])
        aname = VGroup(L("three children", 22, INK, emph=True),
                       L("after the division", 20, GRAY)).arrange(RIGHT, buff=0.30)
        aname.next_to(bar, UP, buff=0.16).align_to(bar, LEFT)
        self.play(FadeIn(seglabs, lag_ratio=0.22),
                  ReplacementTransform(pname, aname), run_time=0.8)        # 14.0
        cons = T("153 = 98 + 47 + 8", 25)
        cons.next_to(bar, DOWN, buff=0.18).align_to(bar, LEFT)
        self.play(FadeOut(pstat, shift=DOWN * 0.15), run_time=0.4)         # 14.8
        self.play(Write(cons), run_time=0.9)                               # 15.2
        self.wait(3.3)                                                     # 16.1

        shade = Rectangle(width=sxd7(700) - A7L, height=2.75, fill_color=RULE,
                          fill_opacity=1.0, stroke_width=0)
        shade.move_to([(A7L + sxd7(700)) / 2, A7Y + 1.38, 0])
        self.add(shade); self.bring_to_back(shade)
        grid = VGroup(*[Line([A7L, y, 0], [A7R, y, 0], color=RULE, stroke_width=1)
                        for y in (R7P, R7_1, R7_2, R7_3)])
        axis = Line([A7L, A7Y, 0], [A7R, A7Y, 0], color=INK, stroke_width=1.6)
        ticks = VGroup()
        for v, lb in [(10, "10"), (100, "100"), (1000, "1,000")]:
            x = sxd7(v)
            ticks.add(Line([x, A7Y, 0], [x, A7Y - 0.12, 0], color=INK, stroke_width=1.6),
                      L(lb, 20).move_to([x, A7Y - 0.36, 0]))
        axcap = L("mean pairwise core SNPs", 20)
        axcap.move_to([A7R, A7Y - 0.74, 0]).align_to([A7R, 0, 0], RIGHT)
        fl = DashedLine([sxd7(700), A7Y, 0], [sxd7(700), R7P + 0.42, 0], color=INK,
                        stroke_width=2, dash_length=0.10)
        flb = L("edge 700", 20, INK, emph=True).next_to(fl, UP, buff=0.10)
        blb = L("below the window", 20, GRAY).move_to([(A7L + sxd7(700)) / 2, R7P + 0.50, 0])
        self.play(Create(axis), FadeIn(ticks, lag_ratio=0.15), FadeIn(axcap),
                  Create(grid, lag_ratio=0.18), run_time=1.1)              # 19.4
        self.play(Create(fl), FadeIn(flb), FadeIn(blb), run_time=0.8)      # 20.5

        def rowlab(nm, n, y, phase):
            return VGroup(
                L(phase, 20, GRAY).move_to([PFX7, y, 0]).align_to([PFX7, y, 0], LEFT),
                L(nm, 20).move_to([NAME7, y, 0]).align_to([NAME7, y, 0], LEFT),
                L(f"n = {n}", 20).move_to([NUM7, y, 0]).align_to([NUM7, y, 0], LEFT))

        def rowval(dv, rm, cls, y, col):
            return VGroup(L(f"{dv:,}", 20, col).move_to([sxd7(dv), y + 0.30, 0]),
                          L(f"r/m {rm:.2f}", 20, col).move_to([RM7, y, 0]),
                          L(cls, 20, col).move_to([CLS7, y, 0]))

        # ---- the parent flies down from the bar to its own row ----
        pl = rowlab(PAR7[0], PAR7[1], R7P, "before")
        ghost = bar.copy().set_fill(TEAL_D, opacity=1.0)
        pdot = Dot([sxd7(PAR7[2]), R7P, 0], radius=0.10, color=TEAL_D)
        self.play(FadeIn(pl, shift=RIGHT * 0.2), run_time=0.7)             # 21.3
        self.play(Transform(ghost, pdot), run_time=1.1)                    # 22.0
        pv = rowval(PAR7[2], PAR7[3], PAR7[4], R7P, TEAL_D)
        self.play(FadeIn(pv), run_time=0.6)                                # 23.1
        self.wait(1.7)                                                     # 23.7

        # ---- each child segment flies to its own position ----
        kl, kg, kv = VGroup(), [], VGroup()
        for i, (nm, n, dv, rm, cls, y) in enumerate(KID7):
            kl.add(rowlab(nm, n, y, "after"))
            kv.add(rowval(dv, rm, cls, y, TEAL_D))
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in kl],
                              lag_ratio=0.22), run_time=0.9)               # 25.4
        anims = []
        for i, (nm, n, dv, rm, cls, y) in enumerate(KID7):
            g = segs[i].copy().set_fill(TEAL_D, opacity=1.0)
            kg.append(g)
            anims.append(Transform(g, Dot([sxd7(dv), y, 0], radius=0.10, color=TEAL_D)))
        self.play(LaggedStart(*anims, lag_ratio=0.30), run_time=1.7)       # 26.3
        self.play(FadeIn(kv, lag_ratio=0.2), run_time=0.6)                 # 28.0

        # ---- the two that fell, in the bar and on the axis at once ----
        drop = [0, 2]
        self.play(*[kg[i].animate.set_color(RUST) for i in drop],
                  *[kv[i].animate.set_color(RUST) for i in drop],
                  *[bar[i].animate.set_fill(RUST) for i in drop],
                  run_time=1.0, rate_func=smooth)                          # 28.6
        self.bring_to_front(seglabs)
        self.wait(0.6)                                                     # 29.6

        # ---- the eighteen-fold drop, drawn rather than left to arithmetic ----
        arc = CurvedArrow([sxd7(1310), R7P - 0.14, 0], [sxd7(72), R7_1 + 0.14, 0],
                          color=RUST, stroke_width=3, tip_length=0.18, angle=-0.55)
        dlab = L("eighteen times lower", 20, RUST, emph=True)
        dlab.move_to([1.38, R7_1 + 0.52, 0])
        self.play(Create(arc), FadeIn(dlab), run_time=1.0)                 # 30.2
        self.wait(1.2)                                                     # 31.2

        c = L("No rate can be interpreted for the two that fell below the window.", 21)
        c.move_to([0, 1.00, 0])
        self.play(FadeIn(c, shift=UP * 0.2), run_time=0.9)                 # 32.4
        self.wait(2.4)                                                     # 33.3


# ===========================================================================
# 7.9  The paired tree-builder plot, deliverable section 8
#
# REVISED 2026-09-10 per brief section 11.1.
# The old version plotted absolute r/m and connected the pairs. Seven of the
# twelve comparisons sit below r/m 5, so those lines were short, overlapping
# and nearly flat, and the finding was carried entirely by the text caption.
#
# This plots the DERIVED QUANTITY the claim is actually about: the ratio of
# the two builders, one dot per comparison, against a reference line at 1.0.
# Eleven dots below and one above is legible without reading anything.
# The worst case is the lowest dot rather than a label.
#
# Both skeletons are drawn before either is populated, so the comparison the
# clip exists to make is available throughout rather than only at the end.
#
# Six units by two replicons, replicons never averaged, both panels kept.
#   IQ-TREE  median 0.988,  7 of 12 below 1.0, sign test p = 0.77
#   rapidnj  median 0.922, 11 of 12 below 1.0, p = 0.0063, worst 45.5% low
# ===========================================================================

# unit, RAxML r/m, IQ-TREE ratio, rapidnj ratio   (ordered by RAxML r/m)
R9 = [
    ("s3_L1_10",  1.81, 0.982, 0.719), ("s1_L1_19",  2.02, 1.016, 0.930),
    ("s3_L1_10",  2.25, 0.972, 0.687), ("s1_L1_19",  2.59, 0.988, 0.913),
    ("strain_12", 3.04, 1.015, 0.976), ("s2_L1_8",   4.05, 1.126, 0.545),
    ("strain_12", 4.50, 1.009, 1.015), ("s2_L1_8",   7.55, 0.935, 0.889),
    ("s3_L1_8",   8.05, 0.949, 0.978), ("s3_L1_8",  10.25, 0.987, 0.979),
    ("s13_L1_1", 11.64, 1.049, 0.952), ("s13_L1_1", 14.13, 0.850, 0.819),
]
RLO, RHI = 0.50, 1.20
YB, YT = -1.80, 1.70
P1L, P1R = -4.75, -2.15
P2L, P2R = 1.05, 3.65


def sy9(r):
    return YB + (r - RLO) / (RHI - RLO) * (YT - YB)


def px9(L, R, i):
    return L + (R - L) * i / (len(R9) - 1.0)


class TreeBuilderPaired(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        title = T("Does the tree builder change the answer?", 36)
        title.to_edge(UP, buff=0.42).to_edge(LEFT, buff=0.82)
        sub = L("Each dot is one comparison, as a ratio against RAxML. "
                "Below the line means a lower rate.", 21)
        sub.next_to(title, DOWN, buff=0.20).align_to(title, LEFT)
        self.play(Write(title), run_time=1.2)                       # 0.0
        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.9)      # 1.2
        self.wait(1)                                                # 2.1
        source(self, "Source: 12 comparisons per builder. Replicons are not averaged.")

        # ---- both skeletons first, so the two panels are comparable throughout
        grid = VGroup()
        for v in (0.6, 0.8, 1.2):
            grid.add(Line([-5.55, sy9(v), 0], [4.15, sy9(v), 0], color=RULE, stroke_width=1),
                     L(f"{v:.1f}", 20).move_to([-5.95, sy9(v), 0]))
        ylab = L("ratio", 20, INK, emph=True).move_to([-5.95, YT + 0.30, 0])
        ref = Line([-5.55, sy9(1.0), 0], [4.15, sy9(1.0), 0], color=INK, stroke_width=2.2)
        reflab = L("1.0, the two builders agree", 20, INK, emph=True)
        reflab.move_to([-5.95, sy9(1.0), 0]).align_to([-5.95, 0, 0], LEFT)
        reflab.shift(RIGHT * 0.0)
        reflab = L("1.0", 20, INK, emph=True).move_to([-5.95, sy9(1.0), 0])

        h1 = L("IQ-TREE against RAxML", 22, INK, emph=True).move_to([(P1L + P1R) / 2, 2.06, 0])
        h2 = L("rapidnj against RAxML", 22, INK, emph=True).move_to([(P2L + P2R) / 2, 2.06, 0])
        self.play(Create(grid, lag_ratio=0.12), FadeIn(ylab), FadeIn(reflab),
                  run_time=1.2)                                     # 3.1
        self.play(Create(ref), run_time=0.9)         # 4.3
        self.play(FadeIn(h1), FadeIn(h2.copy().set_opacity(0.35)), run_time=0.6)  # 5.2
        self.add(h2.set_opacity(0.35))

        # ---- panel one populates
        d1 = VGroup(*[Dot([px9(P1L, P1R, i), sy9(r[2]), 0], radius=0.075,
                          color=(RUST if r[2] < 1.0 else TEAL)) for i, r in enumerate(R9)])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in d1], lag_ratio=0.28),
                  run_time=4.6)                                     # 5.8
        self.wait(1.2)                                              # 10.4
        a1 = VGroup(L("median ratio 0.988", 20),
                    L("7 of 12 below the line, sign test p = 0.77", 20),
                    L("no directional bias", 22, TEAL_D, emph=True)
                    ).arrange(DOWN, buff=0.15).move_to([(P1L + P1R) / 2, -2.66, 0])
        self.play(FadeIn(a1, lag_ratio=0.25), run_time=1.2)         # 11.6
        self.wait(1.6)                                              # 12.8

        # ---- panel two populates against the same skeleton
        self.play(h2.animate.set_opacity(1.0), run_time=0.8)        # 14.4
        d2 = VGroup(*[Dot([px9(P2L, P2R, i), sy9(r[3]), 0], radius=0.075,
                          color=(RUST if r[3] < 1.0 else TEAL)) for i, r in enumerate(R9)])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in d2], lag_ratio=0.28),
                  run_time=4.6)                                     # 15.2
        self.wait(0.8)                                              # 19.8
        a2 = VGroup(L("median ratio 0.922", 20),
                    L("11 of 12 below the line, sign test p = 0.0063", 20, RUST),
                    L("a systematic underestimate", 22, RUST, emph=True)
                    ).arrange(DOWN, buff=0.15).move_to([(P2L + P2R) / 2, -2.66, 0])
        self.play(FadeIn(a2, lag_ratio=0.25), run_time=1.2)         # 20.6
        self.wait(1.4)                                              # 21.8

        # ---- the worst case is now simply the lowest dot
        worst_i = min(range(len(R9)), key=lambda i: R9[i][3])
        wd = d2[worst_i]
        wl = L("45.5% low", 20, RUST, emph=True)
        wl.next_to(wd, RIGHT, buff=0.22)
        self.play(Indicate(wd, color=RUST, scale_factor=1.9), FadeIn(wl), run_time=1.2)
        self.wait(2.2)


# ===========================================================================
# 7.12  Why this reaches the outbreak call
#
# REVISED per review.
#   1. The four published anchors are now the SPINE. They are the only
#      measured values in the clip, and they used to arrive as thin dashed
#      verticals in the last third. They are drawn solid, full height, with
#      their values, before either curve exists.
#   2. The two curves are schematic, so they are now rendered visibly
#      sketchy: dashed, lighter, thinner. The field between them is much
#      fainter. Previously the most visually dominant object in the frame was
#      the least real one.
#   3. The decision band is given weight rather than reading as an edge case,
#      with everything outside it dimmed once the argument is made.
#
# The curves are NOT made to look more like data. The on-screen note saying
# they are schematic stays. No threshold is proposed.
# ===========================================================================

XL2, XR2, U2 = -5.10, 5.20, 4.5
Y02, Y12 = -1.52, 2.12
sx2 = lambda d: XL2 + (math.log10(d) / U2) * (XR2 - XL2)
sxu2 = lambda u: XL2 + (u / U2) * (XR2 - XL2)
sy2 = lambda p: Y02 + (p / 100.0) * (Y12 - Y02)
rec2 = lambda u: 100.0 / (1.0 + math.exp(-(u - 1.35) * 1.55))
det2 = lambda u: 5.0 + 95.0 / (1.0 + math.exp(-(u - 2.90) * 1.75))

ANCH12 = [(404, "404", "a genuinely clonal pair"),
          (1328, "1,328", "one point-source outbreak"),
          (20567, "20,567", ""),
          (21211, "21,211", "two isolates, same sequence type")]


class OutbreakThreshold(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        t0 = T("Why this reaches the outbreak call", 40)
        s0 = L("In an outbreak investigation a SNP threshold says that two genomes\n"
               "fewer than N SNPs apart probably share a source.", 24)
        s0.next_to(t0, DOWN, buff=0.40)
        VGroup(t0, s0).move_to(ORIGIN)
        self.play(Write(t0), run_time=1.2)                              # 0.0
        self.play(FadeIn(s0, shift=DOWN * 0.2), run_time=1.0)           # 1.2
        self.wait(2.4)                                                  # 2.2
        hdr = T("Why this reaches the outbreak call", 32)
        hdr.to_edge(UP, buff=0.45).to_edge(LEFT, buff=0.82)
        self.play(FadeOut(s0, shift=UP * 0.2), ReplacementTransform(t0, hdr),
                  run_time=1.0)                                         # 4.6
        source(self, "Source: published thresholds and outbreak reports. Curves are schematic.")

        axis = Line([XL2, Y02, 0], [XR2, Y02, 0], color=INK, stroke_width=1.6)
        xt = VGroup()
        for dd, lb in [(1, "1"), (10, "10"), (100, "100"), (1000, "1,000"), (10000, "10,000")]:
            x = sx2(dd)
            xt.add(Line([x, Y02, 0], [x, Y02 - 0.13, 0], color=INK, stroke_width=1.6),
                   L(lb, 20).move_to([x, Y02 - 0.37, 0]))
        xcap = L("SNP distance between two genomes", 20)
        xcap.move_to([XR2, Y02 - 0.76, 0]).align_to([XR2, 0, 0], RIGHT)
        yt = VGroup()
        for p in (0, 50, 100):
            yt.add(Line([XL2, sy2(p), 0], [XR2, sy2(p), 0], color=RULE, stroke_width=1),
                   L(f"{p}%", 20).move_to([XL2 - 0.55, sy2(p), 0]))
        self.play(Create(axis), FadeIn(xt, lag_ratio=0.12), FadeIn(xcap), run_time=1.1)  # 5.6
        self.play(FadeIn(yt, lag_ratio=0.15), run_time=0.7)             # 6.7

        band = Rectangle(width=sx2(15) - XL2, height=Y12 - Y02, fill_color=RULE,
                         fill_opacity=1.0, stroke_color=INK, stroke_width=1.8)
        band.move_to([(XL2 + sx2(15)) / 2, (Y02 + Y12) / 2, 0])
        self.add(band); self.bring_to_back(band)
        blab = VGroup(L("every outbreak call", 20), L("happens in here", 20),
                      L("0 to 15 SNPs", 21, INK, emph=True)).arrange(DOWN, buff=0.09)
        blab.move_to([(XL2 + sx2(15)) / 2, sy2(74), 0])
        self.play(FadeIn(band), FadeIn(blab), run_time=1.0)             # 7.4
        self.wait(2.8)                                                  # 8.4

        n15 = L("The upper bound of 15 rests on 17 informative pairs, in a single\n"
                "study, with no recombination correction.", 20)
        n15.move_to([2.05, sy2(58), 0])
        self.play(FadeIn(n15), run_time=0.9)                            # 11.2
        self.wait(1.6)                                                  # 12.1

        # ---- the spine: the only measured values in the clip, drawn solid ----
        spine = VGroup()
        for dv, big, desc in ANCH12:
            x = sx2(dv)
            spine.add(Line([x, Y02, 0], [x, Y12 + 0.06, 0], color=INK, stroke_width=2.6))
        tags = VGroup()
        tags.add(L("404", 20, INK, emph=True).move_to([sx2(404), Y12 + 0.30, 0]))
        tags.add(L("1,328", 20, INK, emph=True).move_to([sx2(1328), Y12 + 0.30, 0]))
        tags.add(L("20,567 and 21,211", 20, INK, emph=True)
                 .move_to([sx2(20889) - 0.55, Y12 + 0.30, 0]))
        # one legend row, each descriptor prefixed by its own measured value,
        # so the pairing is explicit without three scattered labels
        dsc = L("404 a genuinely clonal pair     1,328 one point-source outbreak     "
                "20,567 and 21,211 two isolates, same sequence type", 20, GRAY)
        dsc.move_to([0, Y02 - 1.14, 0])
        meas = L("measured values", 20, INK, emph=True)
        meas.move_to([XL2 + 0.10, Y12 + 0.30, 0]).align_to([XL2, 0, 0], LEFT)
        self.play(FadeIn(meas), LaggedStart(*[Create(s) for s in spine], lag_ratio=0.18),
                  run_time=1.4)                                         # 13.7
        self.play(FadeIn(tags, lag_ratio=0.2), FadeIn(dsc, lag_ratio=0.2), run_time=0.9)  # 15.1
        self.play(FadeOut(n15), run_time=0.4)                           # 16.0

        # ---- the schematic curves, deliberately sketchy ----
        us = [i * U2 / 200.0 for i in range(201)]
        cA_s = VMobject().set_points_smoothly([[sxu2(u), sy2(rec2(u)), 0] for u in us])
        cA = DashedVMobject(cA_s, num_dashes=52, dashed_ratio=0.55)
        cA.set_stroke(color=TEAL, width=3.0, opacity=0.8)
        lA = VGroup(L("how much of the distance", 20, TEAL_D),
                    L("is recombination", 20, TEAL_D, emph=True)).arrange(DOWN, buff=0.07)
        lA.move_to([3.30, sy2(84), 0])
        self.play(Create(cA), run_time=1.4)                             # 16.4
        self.play(FadeIn(lA), run_time=0.7)                             # 17.8
        self.wait(0.9)                                                  # 18.5

        cB_s = VMobject().set_points_smoothly([[sxu2(u), sy2(det2(u)), 0] for u in us])
        cB = DashedVMobject(cB_s, num_dashes=52, dashed_ratio=0.55)
        cB.set_stroke(color=TEAL_X, width=3.0, opacity=0.8)
        lB = VGroup(L("how much of it the", 20, TEAL_X),
                    L("filter detects", 20, TEAL_X, emph=True)).arrange(DOWN, buff=0.07)
        lB.move_to([2.95, sy2(22), 0])
        self.play(Create(cB), run_time=1.4)                             # 19.4
        self.play(FadeIn(lB), run_time=0.7)                             # 20.8
        self.wait(0.5)                                                  # 21.5

        gap = Polygon(*([[sxu2(u), sy2(rec2(u)), 0] for u in us] +
                        [[sxu2(u), sy2(det2(u)), 0] for u in reversed(us)]),
                      color=RUST, fill_color=RUST, fill_opacity=0.10, stroke_width=0)
        gl = L("this gap passes through unremoved", 20, RUST)
        gl.move_to([0.60, sy2(54), 0])
        self.play(FadeIn(gap), run_time=0.9)                            # 22.0
        self.bring_to_front(spine, tags, cA, cB, lA, lB, blab)
        self.play(FadeIn(gl), run_time=0.7)                             # 22.9
        self.wait(1.6)                                                  # 23.6
        self.play(FadeOut(gl), run_time=0.4)                            # 25.2

        ub = math.log10(15)
        dA = Dot([sx2(15), sy2(rec2(ub)), 0], radius=0.075, color=TEAL_D)
        dB = Dot([sx2(15), sy2(det2(ub)), 0], radius=0.075, color=TEAL_X)
        rd = VGroup(L("at the edge of the band", 20, GRAY),
                    L("recombination is already material", 21, TEAL_D),
                    L("detection is close to nothing", 21, TEAL_X)).arrange(DOWN, buff=0.13)
        rd.move_to([1.30, sy2(40), 0])
        self.play(GrowFromCenter(dA), GrowFromCenter(dB), FadeIn(rd), run_time=1.0)  # 25.6
        self.wait(4.2)                                                  # 26.6
        self.play(FadeOut(rd), run_time=0.5)                            # 30.8

        # ---- the outbreak anchor carries the argument ----
        ox = sx2(1328)
        hl = Line([ox, Y02, 0], [ox, Y12 + 0.06, 0], color=RUST, stroke_width=5)
        ocap = L("one point-source outbreak spanned 1,328 SNPs", 21, RUST, emph=True)
        ocap.move_to([0, Y02 - 1.60, 0])
        self.play(Create(hl), FadeIn(ocap), run_time=1.0)               # 31.3
        self.wait(2.2)                                                  # 32.3
        ocap2 = L("about five percent of it survived filtering", 21, RUST, emph=True)
        ocap2.move_to([0, Y02 - 1.60, 0])
        self.play(FadeOut(ocap), FadeIn(ocap2), run_time=0.8)           # 34.5
        self.wait(3.0)                                                  # 35.3
        self.play(FadeOut(ocap2), run_time=0.5)                         # 38.3

        sg = VGroup(L("It matters most, and is detected least,", 23),
                    L("exactly where outbreak calls are made.", 23, RUST, emph=True)
                    ).arrange(DOWN, buff=0.16).move_to([0, Y02 - 1.66, 0])
        self.play(FadeIn(sg, lag_ratio=0.4), run_time=1.0)              # 38.8
        self.wait(2.9)                                                  # 39.8
        rf = L("No threshold is proposed here.", 21, GRAY)
        rf.move_to([0, Y02 - 1.60, 0])
        self.play(FadeOut(sg), run_time=0.4)                            # 42.7
        self.play(FadeIn(rf), run_time=0.8)                             # 43.1
        self.wait(1.0)                                                  # 43.9
