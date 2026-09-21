from manim import *
import numpy as np

# ============================================================================
#  APHL / CDC Southeast Asia Applied Science Hub — house style, shared header
#  Film: "What a genome can and cannot tell you" (B. pseudomallei attribution)
#  Rendered per-act; acts hand off visually (exit state N = entry state N+1).
#
#  Header copied verbatim from
#  ~/.agi/renders/36e4638f-.../src/aphl_common.py, with one change:
#  schematic_tag()'s default string loses its em dash per the sweep in
#  ANIMO_MERGE_SPEC_2026-09-17.md section 5 (aphl_common.py line 63).
# ============================================================================

config.background_color = "#FFFFFF"     # never dark theme

# --- palette, by MEANING, never decorative -----------------------------------
TEAL      = "#00A0AF"   # genomic / sequence / the measured signal (fills/marks)
TEAL_TXT  = "#006E79"   # text-safe teal (any teal carrying a glyph)
TEAL_DK   = "#005057"   # reference genome / deepest teal
TEAL_LT   = "#A3CCCC"   # light teal ramp
PURPLE    = "#9960A7"   # geography / place (regions and countries)
RUST      = "#B42E34"   # a limit or a failure, adverse outcome ONLY
INK       = "#404040"   # default ink (labels/body)
GRIDGRAY  = "#E2E9EC"   # gridlines / neutral shaded zones
SRCGRAY   = "#6E6E6E"   # source-line gray
GRAYOUT   = "#6E6E6E"   # not measured / set aside (outline-only, no fill)
AMBER     = "#EBAB21"
ORANGE    = "#E37C1D"

FONT_TITLE = "Franklin Gothic Medium"
FONT_BODY  = "Franklin Gothic Book"

DEFAULT_FONT_SIZE = 28

Text.set_default(font=FONT_BODY, color=INK)

# reserved bottom eighth carries subtitles: keep content above y = -3.0
SUB_TOP = -3.0


def Txt(s, font_size=DEFAULT_FONT_SIZE, **kw):
    base_h = Text(s, font_size=font_size, **kw).height   # K=1 never wraps
    K = 12
    while K > 1:
        m = Text(s, font_size=font_size * K, **kw)
        if m.height / K <= base_h * 1.3:
            break
        K -= 2
    else:
        m, K = Text(s, font_size=font_size, **kw), 1
    return m.scale(1.0 / K)


def Title(s, font_size=38, color=TEAL_TXT, **kw):
    kw.setdefault("font", FONT_TITLE)
    return Txt(s, font_size=font_size, color=color, **kw)


def Body(s, font_size=DEFAULT_FONT_SIZE, color=INK, **kw):
    kw.setdefault("font", FONT_BODY)
    return Txt(s, font_size=font_size, color=color, **kw)


def source_note(s):
    n = Txt(s, font_size=18, font=FONT_BODY, color=SRCGRAY)
    n.to_edge(RIGHT, buff=0.5).set_y(SUB_TOP + 0.28)
    return n


def schematic_tag(s="Schematic, illustrative"):
    t = Txt(s, font_size=18, font=FONT_BODY, color=SRCGRAY, slant=ITALIC)
    return t


def case_mark(radius=0.14, ring_gap=0.10):
    dot  = Dot(radius=radius, color=TEAL).set_fill(TEAL, 1.0).set_stroke(width=0)
    ring = Circle(radius=radius + ring_gap, color=TEAL_DK, stroke_width=3.0)
    g = VGroup(dot, ring)
    g.dot, g.ring = dot, ring
    return g


def small_dot(radius=0.055, color=TEAL, opacity=1.0):
    return Dot(radius=radius, color=color).set_fill(color, opacity).set_stroke(width=0)


# ==============  ACT 4 (REBUILD) — WHY THE COUNTRY QUESTION CANNOT BE ANSWERED
#
# Replaces the shipped Act 4 per ANIMO_ACT4_REVISION_2026-09-17.md. The old act
# reported "six units pass both controls, all Southeast Asian" as its premise,
# displayed from 0.5 s to 44 s. NUMBERS.tsv contradicts both halves
# (phylo.spec_ladder, phylo.national_passes) and the manuscript states outright
# that it does not report a count of geographically structured units. So this is
# a replacement, not a patch.
#
# Runtime target 51.0 s and word budget 110 come from
# ANIMO_APHL_TIGHTEN_2026-09-17.md, which supersedes the 52-55 s / 90 words in
# the revision note (that predates the turbo_v2_5 @ 0.9 speed decision).
#
# Every on-screen figure verified against NUMBERS.tsv and, for beat 3, against
# GATE1_ALIGNMENT_2026-08-21.tsv:
#   phylo.thailand_share_analysed   66.7% (1561/2340), note says round to 67%
#   phylo.bioproject_nesting        Cramer's V 0.857, 95% single-country
#   americas.all_outside_window     5 of 5, two below at 243 and 211,
#                                   three above 5,198 to 7,776
#
# Beats:
#   beat 1  the collection is not a sample of the world   0.6 to 13.8
#   beat 2  country and study are nearly one variable    13.8 to 32.2  (centre)
#   beat 3  the Americas cannot be measured at all       32.2 to 43.8
#   pivot   narrow the question, hand to act 5           43.8 to 51.0
# ============================================================================
class Act4NotSeparable(Scene):
    def construct(self):
        src = source_note("Frozen basis, 2,340 genomes in 85 units")
        self.add(src)
        title = Title("Why this collection cannot answer the country question",
                      font_size=30).to_edge(UP, buff=0.5)
        self.add(title)
        self.wait(0.6)                                                    # -> 0.6

        # ============================ BEAT 1 =============================
        # The collection is not a sample of the world. A property of the public
        # record this collection inherited, NOT a flaw in the study.
        lead1 = Body("Start with what is in the collection.",
                     font_size=25, color=INK).move_to([0, 2.25, 0])
        self.play(FadeIn(lead1, run_time=0.8))                            # -> 1.4
        self.wait(0.8)                                                    # -> 2.2

        BW, BH, BY = 9.6, 0.78, 0.75
        frac = 1561.0 / 2340.0
        wl = BW * frac
        seg_th = Rectangle(width=wl, height=BH, stroke_width=0).set_fill(PURPLE, 0.90)
        seg_rest = Rectangle(width=BW - wl, height=BH, stroke_width=0).set_fill(GRIDGRAY, 1.0)
        bar = VGroup(seg_th, seg_rest).arrange(RIGHT, buff=0).move_to([0, BY, 0])
        outline = Rectangle(width=BW, height=BH, stroke_width=1.6,
                            color=SRCGRAY).move_to([0, BY, 0])

        lab_th = Body("Thailand", font_size=22, color="#FFFFFF").move_to(
            seg_th.get_center() + UP * 0.0)
        n_th = Body("1,561 genomes", font_size=19, color=PURPLE).move_to(
            [seg_th.get_center()[0], BY - BH / 2 - 0.34, 0])
        lab_rest = Body("every other country", font_size=20, color=INK).move_to(
            seg_rest.get_center())
        n_rest = Body("779", font_size=19, color=SRCGRAY).move_to(
            [seg_rest.get_center()[0], BY - BH / 2 - 0.34, 0])

        self.play(Create(outline), FadeIn(bar), run_time=1.2)             # -> 3.4
        self.play(FadeIn(lab_th), FadeIn(lab_rest), FadeIn(n_th), FadeIn(n_rest),
                  run_time=0.6)                                           # -> 4.0
        self.wait(1.6)                                                    # -> 5.6

        pct = Body("Two thirds of the analysed genomes come from one country.",
                   font_size=25, color=PURPLE).move_to([0, -0.55, 0])
        self.play(FadeIn(pct, run_time=0.8))                              # -> 6.4
        self.wait(2.4)                                                    # -> 8.8

        rec = Body("Most public genomes come from a few heavily studied places.",
                   font_size=23, color=INK).move_to([0, -1.25, 0])
        self.play(FadeIn(rec, run_time=0.8))                              # -> 9.6
        self.wait(3.4)                                                    # -> 13.0

        b1 = VGroup(lead1, bar, outline, lab_th, lab_rest, n_th, n_rest, pct, rec)
        self.play(FadeOut(b1, run_time=0.8))                              # -> 13.8

        # ============================ BEAT 2 =============================
        # The centre of the act. Country and collection history are not
        # separable here. State it as the finding. NO count of units, in either
        # direction, anywhere in this act.
        lead2 = Body("Now ask where those genomes were sequenced.",
                     font_size=25, color=INK).move_to([0, 2.60, 0])
        self.play(FadeIn(lead2, run_time=0.8))                            # -> 14.6
        self.wait(0.8)                                                    # -> 15.4

        # Both classes are statements about country, so both stay in the
        # geography channel and separate by fill against outline. Encoding the
        # six in teal would have put the measured-signal color on a fact about
        # place, which is the exact confusion the merge spec is fixing.
        N_PROJ, N_SINGLE = 119, 113
        sq = VGroup()
        for i in range(N_PROJ):
            if i < N_SINGLE:
                r = Rectangle(width=0.20, height=0.20, stroke_width=0)
                r.set_fill(PURPLE, 0.90)
            else:
                r = Rectangle(width=0.20, height=0.20, stroke_width=2.0,
                              color=PURPLE).set_fill(opacity=0.0)
            sq.add(r)
        sq.arrange_in_grid(rows=7, cols=17, buff=0.055).move_to([0, 1.30, 0])
        self.play(LaggedStart(*[FadeIn(s) for s in sq], lag_ratio=0.006),
                  run_time=1.4)                                           # -> 16.8
        self.wait(1.0)                                                    # -> 17.8

        key_one = Body("sampled a single country", font_size=20, color=PURPLE)
        key_one.move_to([-2.55, 0.05, 0])
        key_many = Body("sampled more than one", font_size=20, color=PURPLE)
        key_many.move_to([2.55, 0.05, 0])
        self.play(FadeIn(key_one), FadeIn(key_many), run_time=1.2)        # -> 19.0

        share = Body("113 of 119 sequencing projects sampled a single country.",
                     font_size=25, color=INK).move_to([0, -0.55, 0])
        self.play(FadeIn(share, run_time=0.8))                            # -> 19.8
        self.wait(2.6)                                                    # -> 22.4

        # One association, read against what it would have to be for the
        # country question to be identifiable at all.
        SL, SR, SY = -3.00, 3.00, -1.72
        scale_ln = Line([SL, SY, 0], [SR, SY, 0], stroke_width=2.5, color=INK)
        t0 = Line([SL, SY - 0.09, 0], [SL, SY + 0.09, 0], stroke_width=2, color=INK)
        t1 = Line([SR, SY - 0.09, 0], [SR, SY + 0.09, 0], stroke_width=2, color=INK)
        e0 = Body("0", font_size=19, color=INK).move_to([SL, SY - 0.30, 0])
        e1 = Body("1", font_size=19, color=INK).move_to([SR, SY - 0.30, 0])
        cap = Body("how closely country and sequencing project track each other\n"
                   "0 is separable, 1 is the same variable",
                   font_size=19, color=SRCGRAY, line_spacing=0.75).move_to(
            [0, SY + 0.52, 0])
        self.play(Create(scale_ln), Create(t0), Create(t1),
                  FadeIn(e0), FadeIn(e1), FadeIn(cap), run_time=1.0)      # -> 23.4

        vx = SL + 0.857 * (SR - SL)
        mk = Line([vx, SY - 0.22, 0], [vx, SY + 0.22, 0], stroke_width=5, color=RUST)
        mkl = Body("0.857", font_size=22, color=RUST).move_to([vx, SY - 0.32, 0])
        self.play(Create(mk), FadeIn(mkl), run_time=1.0)                  # -> 24.4
        self.wait(2.0)                                                    # -> 26.4

        find = Body("Country and collection history are not separable here.",
                    font_size=25, color=RUST).move_to([0, -2.42, 0])
        self.play(FadeIn(find, run_time=0.8))                             # -> 27.2
        self.wait(4.0)                                                    # -> 31.2

        b2 = VGroup(lead2, sq, key_one, key_many, share, scale_ln, t0, t1,
                    e0, e1, cap, mk, mkl, find)
        self.play(FadeOut(b2, run_time=1.0))                              # -> 32.2

        # ============================ BEAT 3 =============================
        # The Americas, where the applied question actually lives. All five
        # Americas-dominated units fall outside the detection window, so
        # recombination cannot be measured for any of them.
        lead3 = Body("Now the region the opening question cares about most.",
                     font_size=25, color=INK).move_to([0, 2.60, 0])
        self.play(FadeIn(lead3, run_time=0.8))                            # -> 33.0

        XL, XR = -5.2, 5.2
        SNPMAX = 8200.0
        AXY = -1.55
        def sx(snp):
            return XL + (snp / SNPMAX) * (XR - XL)

        axis = Line([XL, AXY, 0], [XR, AXY, 0], stroke_width=2.5, color=INK)
        axttl = Body("mean pairwise core SNPs  (diversity)", font_size=21,
                     color=INK).move_to([0, AXY - 0.62, 0])
        ticks, ticklabs = VGroup(), VGroup()
        for snp, lab in [(0, "0"), (700, "700"), (4700, "4,700"), (8000, "8,000")]:
            ticks.add(Line([sx(snp), AXY - 0.08, 0], [sx(snp), AXY + 0.08, 0],
                           stroke_width=2, color=INK))
            ticklabs.add(Body(lab, font_size=19, color=INK).move_to(
                [sx(snp), AXY - 0.30, 0]))
        band = Rectangle(width=sx(4700) - sx(700), height=1.50, stroke_width=0
                         ).set_fill(GRIDGRAY, 1.0)
        band.move_to([(sx(700) + sx(4700)) / 2, AXY + 0.75, 0])
        band_lbl = Body("detection window   700 to 4,700 core SNPs",
                        font_size=21, color=TEAL_TXT).move_to(
            [band.get_center()[0], AXY + 2.30, 0])
        self.play(FadeIn(band), Create(axis), FadeIn(axttl),
                  *[Create(t) for t in ticks], FadeIn(ticklabs),
                  FadeIn(band_lbl), run_time=1.2)                         # -> 34.2
        self.wait(0.6)                                                    # -> 34.8

        # Real values, GATE1_ALIGNMENT_2026-08-21.tsv:
        #   strain_22_L1_1 211.0 | strain_4_L1_1 243.3   (below the floor)
        #   strain_4_L1_2 5198.0 | strain_4_L1_3 7430.6 | strain_4_L1_4 7775.7
        AMER = [211.0, 243.3, 5198.0, 7430.6, 7775.7]
        marks = VGroup()
        for i, v in enumerate(AMER):
            yy = AXY + 0.46 + (0.30 if i % 2 else 0.0)
            marks.add(small_dot(0.085, RUST, 0.95).move_to([sx(v), yy, 0]))
        self.play(LaggedStart(*[FadeIn(m, scale=0.6) for m in marks],
                              lag_ratio=0.18), run_time=1.4)              # -> 36.2

        lb = Body("two below\nthe floor", font_size=19, color=RUST,
                  line_spacing=0.7).move_to([sx(227), AXY + 1.83, 0])
        rb = Body("three above the ceiling", font_size=19, color=RUST).move_to(
            [sx(6480), AXY + 1.83, 0])
        five = Body("Five Americas units. None of them inside the window.",
                    font_size=25, color=INK).move_to([0, 1.95, 0])
        self.play(FadeIn(lb), FadeIn(rb), FadeIn(five), run_time=0.8)     # -> 37.0
        self.wait(2.0)                                                    # -> 39.0

        cannot = Body("Recombination cannot even be measured for them.",
                      font_size=25, color=RUST).move_to([0, 1.40, 0])
        self.play(FadeIn(cannot, run_time=0.8))                           # -> 39.8
        self.wait(3.2)                                                    # -> 43.0

        b3 = VGroup(lead3, axis, axttl, ticks, ticklabs, band, band_lbl,
                    marks, lb, rb, five, cannot)
        self.play(FadeOut(b3, run_time=0.8))                              # -> 43.8

        # ============================= PIVOT =============================
        # The act must end here rather than on beat 3. This is what stops the
        # middle of the film reading as a list of things that did not work.
        p1 = Body("None of this says the genome is uninformative.",
                  font_size=27, color=INK).move_to([0, 1.15, 0])
        self.play(FadeIn(p1, run_time=0.8))                               # -> 44.6
        self.wait(1.4)                                                    # -> 46.0

        p2 = Body("It says the country question is not the one\nthis collection can settle.",
                  font_size=27, color=INK, line_spacing=0.85).move_to([0, 0.15, 0])
        self.play(FadeIn(p2, run_time=0.8))                               # -> 46.8
        self.wait(1.6)                                                    # -> 48.4

        p3 = Body("So ask the one it can.", font_size=30, color=TEAL_TXT).move_to(
            [0, -1.15, 0])
        # the case goes quiet through acts 2 to 4 and returns in act 5
        cm = case_mark(radius=0.11, ring_gap=0.09).move_to([0, -1.95, 0])
        self.play(FadeIn(p3), FadeIn(cm), run_time=0.8)                   # -> 49.2
        self.wait(1.8)                                                    # -> 51.0
