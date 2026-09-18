from manim import *
import math

# ============================================================================
#  TUC BRIEFING SERIES - CLIP 2: "A ruler you can trust"
#
#  Built to the clip 2 brief. Six acts, delivered as SEVEN new renders plus two
#  reused merged clips, concatenated in this order:
#
#    1. Clip2TitleCard        ->  A ruler you can trust
#    2. Clip2Act1             ->  Why the obvious approach fails
#    3. Clip2Act2             ->  Partition first, because the biology says so
#    4. Clip2Act3Leadin       ->  How the detector actually works (lead-in)
#       [ DetectionWindowSweep.mp4  reused, 47.8 s ]
#    5. Clip2Act4Leadin       ->  Does it invent recombination? (lead-in)
#       [ NegativeControlZoom.mp4   reused, 41.5 s ]
#    6. Clip2Act5             ->  Does it find what is really there?
#    7. Clip2Act6             ->  What you now have
#
#  THE VISUAL SYSTEM IS INHERITED FROM CLIP 1 UNCHANGED. The header below is
#  clip 1's aphl_common verbatim, including the corrected Txt() wrap guard
#  (width AND height, see the docstring). The continuity object of THIS clip is
#  the log DIVERSITY AXIS drawn in act 2, matching the two reused clips exactly:
#  mean pairwise core SNPs in the unit, ticks 10 / 100 / 1,000 / 10,000, the
#  700 to 4,700 working window as a teal-outlined band. Everything after act 2
#  is placed on it.
#
#  Every on-screen figure verified against source before drawing:
#    negative control 1,519 replicates over 62 unit-replicons ... NUMBERS controls.null_replicates
#    20 replicates (1.32%) returning any call ................... NUMBERS controls.null_any_call
#    largest pooled r/m from clean input 0.00668 ............... NUMBERS controls.null_max_rm
#    separation 427x to 2,234x ................................. NUMBERS controls.null_separation
#    spike-in recovery 19/21 (91%) at divergence 0.002 ......... NUMBERS controls.spikein_recovery + TABLES Table 4
#    recovery curve 20 / 40 / 91 / 100 / 90 % ................. TABLES Table 4, divergence .0005/.001/.002/.005/.01
#    window floor 700, bracket (588, 755] ..................... NUMBERS rm.gate1_floor
#    window ceiling 4700, bracket (4631.8, 4731.6] ............ NUMBERS rm.gate1_ceiling
#    restriction-modification caveat: 106 strains, one Asian locale ... MANUSCRIPT Discussion
# ============================================================================

config.background_color = "#FFFFFF"     # never dark theme

# --- palette, by MEANING, never decorative -----------------------------------
TEAL      = "#00A0AF"   # genomic / sequence / the measured signal (fills/marks)
TEAL_TXT  = "#006E79"   # text-safe teal (any teal carrying a glyph)
TEAL_DK   = "#005057"   # deepest teal
TEAL_LT   = "#A3CCCC"   # light teal ramp
PURPLE    = "#9960A7"   # geography / place (reserved; not used in this clip)
RUST      = "#B42E34"   # a limit or a failure, adverse outcome ONLY
INK       = "#404040"   # default ink (labels/body)
GRIDGRAY  = "#E2E9EC"   # gridlines / neutral shaded zones
SRCGRAY   = "#6E6E6E"   # source-line gray
GRAYOUT   = "#6E6E6E"   # not measured / cited / set aside (outline-only)
AMBER     = "#EBAB21"
ORANGE    = "#E37C1D"

FONT_TITLE = "Franklin Gothic Medium"
FONT_BODY  = "Franklin Gothic Book"
DEFAULT_FONT_SIZE = 28
Text.set_default(font=FONT_BODY, color=INK)

SUB_TOP = -3.0          # reserved bottom eighth carries captions; keep marks above


def Txt(s, font_size=DEFAULT_FONT_SIZE, **kw):
    """House crisp-text helper, with the wrap guard corrected (inherited clip 1).

    The spec's height-only wrap test misses one real failure mode: when Pango
    wraps a trailing word at large K it can place the wrapped fragment in the
    SAME line box as the following explicit newline, so the layout OVERPRINTS
    itself while its height is unchanged and only its width collapses. Width is
    therefore the reliable wrap detector, so a candidate K keeps both.
    """
    base = Text(s, font_size=font_size, **kw)
    base_h, base_w = base.height, base.width
    K = 12
    while K > 1:
        m = Text(s, font_size=font_size * K, **kw)
        if m.height / K <= base_h * 1.3 and m.width / K >= base_w * 0.95:
            break
        K -= 2
    else:
        m, K = base, 1
    return m.scale(1.0 / K)


def Title(s, font_size=38, color=TEAL_TXT, **kw):
    kw.setdefault("font", FONT_TITLE)
    return Txt(s, font_size=font_size, color=color, **kw)


def Body(s, font_size=DEFAULT_FONT_SIZE, color=INK, **kw):
    kw.setdefault("font", FONT_BODY)
    return Txt(s, font_size=font_size, color=color, **kw)


def source_note(s):
    n = Txt(s, font_size=18, font=FONT_BODY, color=SRCGRAY)
    n.to_edge(LEFT, buff=0.55).set_y(SUB_TOP + 0.24)
    return n


def schematic_tag(s="Schematic, illustrative"):
    return Txt(s, font_size=18, font=FONT_BODY, color=SRCGRAY, slant=ITALIC)


def act_title(s, fs=34):
    return Title(s, font_size=fs).to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.7)


# ---------------------------------------------------------------------------
#  Clock: guarantees each act lands on its frame target regardless of the
#  arithmetic. Every run_time and wait stays on the 0.1 s grid (6-frame steps),
#  so hold_to() closes the remainder to an exact frame count.
# ---------------------------------------------------------------------------
class Clock:
    def __init__(self, scene):
        self.s = scene
        self.t = 0.0

    def play(self, *anims, rt=1.0, **kw):
        self.s.play(*anims, run_time=rt, **kw)
        self.t += rt

    def wait(self, d):
        self.s.wait(d)
        self.t += d

    def hold_to(self, T):
        # Pad from manim's REAL elapsed time, not the arithmetic total, so any
        # float drift accumulated across segments is absorbed here and the clip
        # lands on exactly round(T*60) frames.
        now = getattr(self.s, "renderer", None)
        now = now.time if now is not None and now.time is not None else self.t
        # pad in whole frames, with a half-frame bias so manim's wait never
        # floors a frame short of round(T*60).
        frames = round(T * 60) - round(now * 60)
        if frames > 0:
            self.s.wait(frames / 60.0 + 0.5 / 60.0)
        self.t = T


# ---------------------------------------------------------------------------
#  THE DIVERSITY AXIS  -- the continuity object of clip 2.
#  log10 of mean pairwise core SNPs in the unit, 10 to 10,000.
# ---------------------------------------------------------------------------
DAX_XL, DAX_XR = -5.4, 5.4
DAX_Y = -1.78
DAX_LO, DAX_HI = 10.0, 10000.0
WIN_LO, WIN_HI = 700.0, 4700.0
FLOOR_LO, FLOOR_HI = 588.0, 755.0        # floor bracket
CEIL_LO, CEIL_HI = 4631.8, 4731.6        # ceiling bracket


def dax_x(v):
    return DAX_XL + (math.log10(v) - 1.0) / 3.0 * (DAX_XR - DAX_XL)


def diversity_axis(y=DAX_Y, label=True):
    axis = Line([DAX_XL, y, 0], [DAX_XR, y, 0], stroke_width=2.4, color=INK)
    ticks = VGroup()
    labels = VGroup()
    for v, txt in [(10, "10"), (100, "100"), (1000, "1,000"), (10000, "10,000")]:
        x = dax_x(v)
        ticks.add(Line([x, y - 0.09, 0], [x, y + 0.09, 0], stroke_width=2.0, color=INK))
        labels.add(Body(txt, font_size=21, color=INK).move_to([x, y - 0.36, 0]))
    g = VGroup(axis, ticks, labels)
    g.axis, g.ticks, g.labels = axis, ticks, labels
    if label:
        cap = Body("mean pairwise core SNPs in the unit", font_size=21, color=INK)
        cap.move_to([0, y - 0.74, 0])
        g.add(cap)
        g.cap = cap
    return g


def window_band(y=DAX_Y, h=0.62):
    xl, xr = dax_x(WIN_LO), dax_x(WIN_HI)
    box = Rectangle(width=xr - xl, height=h, stroke_width=2.4, color=TEAL
                    ).set_fill(TEAL, 0.10).move_to([(xl + xr) / 2, y, 0])
    return box


def unit_dot(inside=True, r=0.058):
    c = TEAL if inside else RUST
    return Dot(radius=r, color=c).set_fill(c, 1.0).set_stroke(width=0)


# ============================================================================
#  TITLE CARD.  Holds ~1.5 s. Target 5.0 s.
# ============================================================================
class Clip2TitleCard(Scene):
    def construct(self):
        c = Clock(self)
        title = Title("A ruler you can trust", font_size=52).move_to([0, 0.75, 0])
        sub = Body("Clip two of four. The TUC briefing.", font_size=25,
                   color=SRCGRAY).move_to([0, -0.05, 0])

        # a short ruler motif: a measured segment with graduation ticks
        rl, rr = -2.6, 2.6
        ruler = Line([rl, -1.15, 0], [rr, -1.15, 0], stroke_width=2.6, color=TEAL_TXT)
        gticks = VGroup()
        n = 11
        for i in range(n):
            x = rl + (rr - rl) * i / (n - 1)
            hgt = 0.20 if i % 5 == 0 else 0.12
            gticks.add(Line([x, -1.15, 0], [x, -1.15 + hgt, 0],
                            stroke_width=2.0, color=TEAL_TXT))

        c.play(Write(title, run_time=1.2), rt=1.2)
        c.wait(0.5)
        c.play(FadeIn(sub, shift=UP * 0.12, run_time=0.7), rt=0.7)
        c.play(Create(ruler, run_time=0.6), LaggedStartMap(GrowFromEdge, gticks,
               edge=DOWN, lag_ratio=0.06, run_time=0.9), rt=0.9)
        # 2026-09-18: was hold_to(5.0). Clip two is the only film with a separate
        # title card, and a 5 s silent card plus act 1's lead-in opened the film
        # with 6.25 s of nothing. The brief asks for a 1 to 2 second hold.
        c.hold_to(3.6)


# ============================================================================
#  ACT 1.  Why the obvious approach fails.        target 48.0 s
#  Entry: clip 1's closing question.  Exit: r/m defined, one number refused.
#  Guard: never show a species-wide r/m value here.
# ============================================================================
class Clip2Act1(Scene):
    def construct(self):
        c = Clock(self)
        title = act_title("Why the obvious approach fails")
        self.add(title)
        c.wait(1.0)

        # two genomes differ for two reasons -----------------------------------
        lead = Body("Two genomes can differ for two different reasons.",
                    font_size=27, color=INK).move_to([0, 2.05, 0])
        c.play(FadeIn(lead, run_time=0.7), rt=0.7)
        c.wait(2.7)

        base_y = 0.95
        gline = Line([-4.6, base_y, 0], [4.6, base_y, 0], stroke_width=2.2, color=INK)
        c.play(Create(gline, run_time=0.7), rt=0.7)
        c.wait(1.0)

        # reason one: point mutation, ticks accumulate
        muts = VGroup()
        import random
        random.seed(7)
        xs = sorted(random.uniform(-4.4, 4.4) for _ in range(26))
        for x in xs:
            muts.add(Line([x, base_y - 0.16, 0], [x, base_y + 0.16, 0],
                          stroke_width=1.6, color=INK))
        m_lab = Body("mutation: point differences accumulate over time",
                     font_size=22, color=INK).move_to([0, base_y + 0.62, 0])
        c.play(LaggedStartMap(GrowFromCenter, muts, lag_ratio=0.02, run_time=1.1),
               rt=1.1)
        c.play(FadeIn(m_lab, run_time=0.6), rt=0.6)
        c.wait(4.1)

        # reason two: an imported block arrives
        bl, br = 1.1, 2.6
        block = Rectangle(width=br - bl, height=0.42, stroke_width=0
                          ).set_fill(TEAL_LT, 1.0).move_to([(bl + br) / 2, base_y, 0])
        b_lab = Body("recombination: a block of DNA arrives from another lineage",
                     font_size=22, color=TEAL_TXT).move_to([0, base_y - 0.66, 0])
        c.play(FadeIn(block, shift=DOWN * 0.25, run_time=0.8), rt=0.8)
        c.play(FadeIn(b_lab, run_time=0.6), rt=0.6)
        c.wait(4.4)

        # the ratio r/m --------------------------------------------------------
        c.play(FadeOut(VGroup(lead, m_lab, b_lab), run_time=0.6),
               VGroup(gline, muts, block).animate.shift(UP * 0.55).set_opacity(0.35),
               rt=0.6)
        ratio = Body("r / m", font_size=52, color=TEAL_TXT, font=FONT_TITLE
                     ).move_to([0, 0.35, 0])
        r_lab = Body("recombination", font_size=22, color=INK).move_to([-1.55, -0.5, 0])
        m_lab2 = Body("mutation", font_size=22, color=INK).move_to([1.35, -0.5, 0])
        rbrace = Line([-2.35, -0.15, 0], [-0.75, -0.15, 0], stroke_width=1.6, color=SRCGRAY)
        mbrace = Line([0.75, -0.15, 0], [2.05, -0.15, 0], stroke_width=1.6, color=SRCGRAY)
        c.play(Write(ratio, run_time=0.9), rt=0.9)
        c.play(FadeIn(VGroup(rbrace, r_lab), run_time=0.5),
               FadeIn(VGroup(mbrace, m_lab2), run_time=0.5), rt=0.6)
        c.wait(3.4)

        dep = Body("The one quantity everything downstream depends on.",
                   font_size=24, color=INK).move_to([0, -1.35, 0])
        c.play(FadeIn(dep, shift=UP * 0.1, run_time=0.7), rt=0.7)
        c.wait(4.4)

        # the trap -------------------------------------------------------------
        c.play(FadeOut(VGroup(gline, muts, block, dep), run_time=0.6),
               VGroup(ratio, rbrace, r_lab, mbrace, m_lab2).animate.scale(0.62)
               .move_to([-4.1, 1.7, 0]), rt=0.6)
        trap = Body("Now compute one r/m for the whole species.",
                    font_size=26, color=INK).move_to([0.4, 1.75, 0])
        c.play(FadeIn(trap, run_time=0.7), rt=0.7)
        c.wait(2.4)

        box = Rectangle(width=5.0, height=1.5, stroke_width=2.0, color=GRAYOUT
                        ).set_fill(GRIDGRAY, 0.4).move_to([0, 0.15, 0])
        box_lab = Body("r/m, species-wide", font_size=23, color=INK
                       ).move_to(box.get_center() + [0, 0.42, 0])
        refused = Body("not computed here", font_size=30, color=RUST, font=FONT_TITLE
                       ).move_to(box.get_center() + [0, -0.22, 0])
        c.play(Create(box, run_time=0.6), FadeIn(box_lab, run_time=0.6), rt=0.6)
        c.wait(2.0)
        c.play(FadeIn(refused, run_time=0.7), rt=0.7)
        c.wait(3.7)

        why = Body("One number averages across the structure and hides it.",
                   font_size=24, color=INK).move_to([0, -1.55, 0])
        c.play(FadeIn(why, run_time=0.7), rt=0.7)
        c.wait(4.1)

        nxt = Body("Clip three shows this number in its proper place.",
                   font_size=23, color=TEAL_TXT).move_to([0, -2.35, 0])
        c.play(FadeIn(nxt, run_time=0.7), rt=0.7)
        c.hold_to(48.0)


# ============================================================================
#  ACT 2.  Partition first, because the biology says so.     target 54.0 s
#  Entry: r/m defined.  Exit: the diversity axis drawn, window not yet placed.
#  Refusal note answered: the restriction-modification claim is drawn as a
#  clearly-labeled CITED schematic (outline gray, italic source), visibly an
#  argument from the literature, never as a measured result of this study. Only
#  the diversity axis at the end is the measured object.
# ============================================================================
class Clip2Act2(Scene):
    def construct(self):
        c = Clock(self)
        title = act_title("Partition first, because the biology says so")
        self.add(title)
        c.wait(0.7)

        # cited panel frame: everything inside is argued, not measured ----------
        panel = Rectangle(width=11.6, height=4.0, stroke_width=1.8, color=GRAYOUT
                          ).move_to([0, 0.55, 0])
        ptag = Body("From the literature, not measured in this study",
                    font_size=19, color=SRCGRAY, slant=ITALIC
                    ).next_to(panel.get_corner(UL), DR, buff=0.16).align_to(panel, LEFT).shift(RIGHT * 0.2)
        c.play(Create(panel, run_time=0.7), rt=0.7)
        c.play(FadeIn(ptag, run_time=0.5), rt=0.5)
        c.wait(1.6)

        # two clades as separate clusters -- each arrives on its own beat --------
        def cluster(cx, cy, col):
            import random
            random.seed(int(cx * 13) + 5)
            g = VGroup()
            for _ in range(9):
                x = cx + random.uniform(-0.55, 0.55)
                y = cy + random.uniform(-0.5, 0.5)
                g.add(Dot(radius=0.07, color=col).set_fill(col, 1.0).set_stroke(width=0)
                      .move_to([x, y, 0]))
            return g
        cA = cluster(-3.1, 1.05, TEAL)
        cB = cluster(3.1, 1.05, TEAL_DK)
        cA_l = Body("clade A", font_size=21, color=INK).move_to([-3.1, 0.32, 0])
        cB_l = Body("clade B", font_size=21, color=INK).move_to([3.1, 0.32, 0])
        c.play(FadeIn(cA, run_time=0.6), rt=0.6)
        c.wait(1.5)
        c.play(FadeIn(cB, run_time=0.6), rt=0.6)
        c.wait(1.5)
        c.play(FadeIn(cA_l, run_time=0.4, shift=UP * 0.28), rt=0.4)
        c.wait(0.6)
        c.play(FadeIn(cB_l, run_time=0.4, shift=UP * 0.28), rt=0.4)
        c.wait(1.2)

        # the barrier: R-M systems restrict DNA uptake between clades
        wall = DashedLine([0, 1.62, 0], [0, 0.35, 0], stroke_width=3.0, color=GRAYOUT)
        rm_l = Body("restriction-modification systems restrict DNA uptake between clades",
                    font_size=21, color=INK).move_to([0, 1.98, 0])
        c.play(Create(wall, run_time=0.6), rt=0.6)
        c.wait(0.7)
        c.play(FadeIn(rm_l, run_time=0.6, shift=UP * 0.28), rt=0.6)
        c.wait(1.8)

        # a block tries to cross and is stopped
        blk = Rectangle(width=0.5, height=0.28, stroke_width=0).set_fill(TEAL_LT, 1.0
                        ).move_to([-1.7, 1.05, 0])
        c.play(blk.animate.move_to([-0.55, 1.05, 0]), rt=0.8)
        stop = Cross(scale_factor=0.22, stroke_color=RUST, stroke_width=5
                     ).move_to([-0.2, 1.05, 0])
        c.play(FadeIn(stop, run_time=0.4), rt=0.4)
        c.wait(2.6)

        # so clades behave as functional units of genetic isolation
        units = Body("so genomic clades behave as functional units of isolation",
                     font_size=21, color=TEAL_TXT).move_to([0, -0.5, 0])
        c.play(FadeIn(units, run_time=0.6, shift=UP * 0.28), rt=0.6)
        c.wait(3.8)

        # the caveat, same cited treatment, revealed a line at a time ----------
        cav1 = Body("Shown for 106 strains in one restricted Asian locale.",
                    font_size=20, color=SRCGRAY, slant=ITALIC).move_to([0, -0.98, 0])
        cav2 = Body("Whether it holds globally has not been tested.",
                    font_size=20, color=SRCGRAY, slant=ITALIC).move_to([0, -1.36, 0])
        c.play(FadeIn(cav1, run_time=0.6, shift=UP * 0.28), rt=0.6)
        c.wait(3.2)
        c.play(FadeIn(cav2, run_time=0.6, shift=UP * 0.28), rt=0.6)
        c.wait(4.1)

        # the verdict: partition before measuring -- two lines, two beats -------
        c.play(FadeOut(VGroup(cA, cB, cA_l, cB_l, wall, rm_l, blk, stop, units,
                              cav1, cav2, ptag), run_time=0.7),
               panel.animate.set_opacity(0.0), rt=0.7)
        ver1 = Body("Partition before measuring.", font_size=26, color=INK
                    ).move_to([0, 2.15, 0])
        ver2 = Body("A biological requirement, not a computational convenience.",
                    font_size=26, color=INK).move_to([0, 1.55, 0])
        c.play(FadeIn(ver1, run_time=0.7, shift=UP * 0.28), rt=0.7)
        c.wait(2.9)
        c.play(FadeIn(ver2, run_time=0.7, shift=UP * 0.28), rt=0.7)
        c.wait(2.4)

        # draw the diversity axis -- the continuity object -- one part per beat --
        ax = diversity_axis()
        c.play(Create(ax.axis, run_time=0.9), rt=0.9)
        c.wait(1.6)
        c.play(LaggedStartMap(GrowFromCenter, ax.ticks, lag_ratio=0.15, run_time=0.9),
               rt=0.9)
        c.wait(2.3)
        c.play(FadeIn(ax.labels, run_time=0.6), rt=0.6)
        c.wait(1.7)
        c.play(FadeIn(ax.cap, run_time=0.6, shift=UP * 0.28), rt=0.6)
        c.wait(2.9)
        axl = Body("Measure r/m within each unit, along this axis of diversity.",
                   font_size=23, color=TEAL_TXT).move_to([0, -0.55, 0])
        c.play(FadeIn(axl, run_time=0.7, shift=UP * 0.28), rt=0.7)
        c.hold_to(54.0)


# ============================================================================
#  ACT 3 LEAD-IN.  How the detector actually works.          target 17.0 s
#  Entry: the diversity axis.  Hands to DetectionWindowSweep.mp4 (47.8 s).
# ============================================================================
class Clip2Act3Leadin(Scene):
    def construct(self):
        c = Clock(self)
        title = act_title("How the detector actually works")
        self.add(title)
        c.wait(1.2)

        # a genome stretch with a locally dense patch
        base_y = 1.35
        gline = Line([-5.0, base_y, 0], [5.0, base_y, 0], stroke_width=2.2, color=INK)
        import random
        random.seed(3)
        sparse = [random.uniform(-5.0, 0.4) for _ in range(10)]
        dense = [random.uniform(0.9, 2.4) for _ in range(16)]
        rest = [random.uniform(2.9, 5.0) for _ in range(6)]
        ticks = VGroup()
        for x in sparse + rest:
            ticks.add(Line([x, base_y - 0.16, 0], [x, base_y + 0.16, 0],
                           stroke_width=1.5, color=INK))
        dticks = VGroup()
        for x in dense:
            dticks.add(Line([x, base_y - 0.16, 0], [x, base_y + 0.16, 0],
                            stroke_width=1.7, color=TEAL_TXT))
        c.play(Create(gline, run_time=0.5),
               LaggedStartMap(GrowFromCenter, ticks, lag_ratio=0.02, run_time=0.8),
               rt=0.8)
        s1 = Body("The detector scans for a local excess of SNP density.",
                  font_size=26, color=INK).move_to([0, 2.3, 0])
        c.play(FadeIn(s1, run_time=0.6),
               LaggedStartMap(GrowFromCenter, dticks, lag_ratio=0.03, run_time=0.7),
               rt=0.7)
        scan = Rectangle(width=1.9, height=0.62, stroke_width=2.2, color=TEAL
                         ).move_to([1.65, base_y, 0])
        c.play(Create(scan, run_time=0.5), rt=0.5)
        c.wait(4.5)

        s2 = Body("Whether that excess is visible depends on the background.",
                  font_size=26, color=INK).move_to([0, 0.15, 0])
        c.play(FadeIn(s2, run_time=0.6), rt=0.6)
        c.wait(4.0)

        # two mini backgrounds: sparse -> visible, dense -> hidden
        def mini(cx, cy, dense_bg):
            import random
            random.seed(int(cx) + (99 if dense_bg else 1))
            ln = Line([cx - 2.0, cy, 0], [cx + 2.0, cy, 0], stroke_width=1.8, color=INK)
            g = VGroup(ln)
            nbg = 34 if dense_bg else 8
            for _ in range(nbg):
                x = cx + random.uniform(-2.0, 2.0)
                g.add(Line([x, cy - 0.13, 0], [x, cy + 0.13, 0], stroke_width=1.3,
                           color=INK))
            patch_col = GRAYOUT if dense_bg else TEAL_TXT
            for _ in range(10):
                x = cx + random.uniform(0.3, 1.1)
                g.add(Line([x, cy - 0.13, 0], [x, cy + 0.13, 0], stroke_width=1.6,
                           color=patch_col))
            return g
        left = mini(-2.7, -1.15, False)
        right = mini(2.7, -1.15, True)
        ll = Body("sparse background: the block stands out", font_size=20,
                  color=TEAL_TXT).move_to([-2.7, -1.95, 0])
        rl = Body("dense background: the block hides", font_size=20,
                  color=GRAYOUT).move_to([2.7, -1.95, 0])
        c.play(FadeIn(left, run_time=0.6), FadeIn(right, run_time=0.6), rt=0.7)
        c.play(FadeIn(ll, run_time=0.5), FadeIn(rl, run_time=0.5), rt=0.5)
        c.hold_to(17.0)


# ============================================================================
#  ACT 4 LEAD-IN.  Does it invent recombination?             target 17.0 s
#  Entry: as act 3 leaves it.  Hands to NegativeControlZoom.mp4 (41.5 s).
# ============================================================================
class Clip2Act4Leadin(Scene):
    def construct(self):
        c = Clock(self)
        title = act_title("Does it invent recombination?")
        self.add(title)
        c.wait(1.1)

        s1 = Body("Run the identical pipeline on populations simulated\n"
                  "with zero recombination.",
                  font_size=26, color=INK, line_spacing=0.85).move_to([0, 1.9, 0])
        c.play(FadeIn(s1, run_time=0.7), rt=0.7)
        c.wait(3.1)

        # pipeline: input -> same detector -> output
        b1 = Rectangle(width=3.0, height=0.9, stroke_width=2.0, color=INK
                       ).set_fill(GRIDGRAY, 0.5).move_to([-3.7, 0.55, 0])
        t1 = Body("zero-recombination\nsimulation", font_size=20, color=INK,
                  line_spacing=0.8).move_to(b1.get_center())
        b2 = Rectangle(width=2.5, height=0.9, stroke_width=2.0, color=TEAL
                       ).set_fill(TEAL, 0.10).move_to([0.15, 0.55, 0])
        t2 = Body("the same\ndetector", font_size=20, color=TEAL_TXT,
                  line_spacing=0.8).move_to(b2.get_center())
        a1 = Arrow(b1.get_right(), b2.get_left(), buff=0.12, stroke_width=3,
                   color=INK, max_tip_length_to_length_ratio=0.3)
        b3 = Rectangle(width=2.3, height=0.9, stroke_width=2.0, color=INK
                       ).set_fill(GRIDGRAY, 0.5).move_to([3.75, 0.55, 0])
        t3 = Body("what comes\nback", font_size=20, color=INK,
                  line_spacing=0.8).move_to(b3.get_center())
        a2 = Arrow(b2.get_right(), b3.get_left(), buff=0.12, stroke_width=3,
                   color=INK, max_tip_length_to_length_ratio=0.3)
        c.play(FadeIn(VGroup(b1, t1), run_time=0.5), rt=0.5)
        c.play(GrowArrow(a1, run_time=0.4), FadeIn(VGroup(b2, t2), run_time=0.5), rt=0.5)
        c.play(GrowArrow(a2, run_time=0.4), FadeIn(VGroup(b3, t3), run_time=0.5), rt=0.5)
        c.wait(3.1)

        # the counts, with denominators explicit
        rep = Body("1,519 replicates over 62 unit-replicons",
                   font_size=25, color=INK).move_to([0, -0.9, 0])
        c.play(FadeIn(rep, run_time=0.6), rt=0.6)
        c.wait(2.7)
        call = Body("20 returned any call at all, 1.32% of replicates",
                    font_size=25, color=TEAL_TXT).move_to([0, -1.65, 0])
        c.play(FadeIn(call, run_time=0.6), rt=0.6)
        c.hold_to(17.0)


# ============================================================================
#  ACT 5.  Does it find what is really there?                target 45.0 s
#  Entry: the null result.  Exit: the recovery sweep complete.
#  Guard: NOT a smooth curve. Five measured bars, each with its denominator.
#  Recovery is non-monotonic at the top (100% then 90%) and that is kept.
# ============================================================================
class Clip2Act5(Scene):
    def construct(self):
        c = Clock(self)
        title = act_title("Does it find what is really there?")
        self.add(title)
        src = source_note("Table 4. Recovery share, denominator = implanted tracts not already detected")
        self.add(src)
        c.wait(0.8)

        s1a = Body("Implant recombination tracts from donors of known divergence,",
                   font_size=25, color=INK).move_to([0, 2.5, 0])
        s1b = Body("then ask how many come back.",
                   font_size=25, color=INK).move_to([0, 2.1, 0])
        c.play(FadeIn(s1a, run_time=0.7), rt=0.7)
        c.wait(2.1)
        c.play(FadeIn(s1b, run_time=0.6), rt=0.6)
        c.wait(2.3)
        s1 = VGroup(s1a, s1b)

        rows = [("0.0005", "2.4", "4 of 20", 20, False),
                ("0.001", "4.2", "8 of 20", 40, False),
                ("0.002", "9.0", "19 of 21", 91, True),
                ("0.005", "25.0", "19 of 19", 100, False),
                ("0.01", "45.0", "19 of 21", 90, False)]
        xs = [-4.3, -2.15, 0.0, 2.15, 4.3]
        base_y = -1.7
        top_y = 1.55
        span = top_y - base_y
        axis = Line([-5.3, base_y, 0], [5.3, base_y, 0], stroke_width=2.2, color=INK)
        yax = Line([-5.3, base_y, 0], [-5.3, top_y + 0.15, 0], stroke_width=2.0, color=INK)
        yl = VGroup()
        for pct in (0, 50, 100):
            yy = base_y + span * pct / 100.0
            yl.add(Line([-5.42, yy, 0], [-5.3, yy, 0], stroke_width=1.6, color=INK))
            yl.add(Body(f"{pct}%", font_size=19, color=INK).move_to([-5.75, yy, 0]))
        ylab = Body("recovered", font_size=20, color=INK).rotate(PI / 2).move_to([-6.25, (base_y + top_y) / 2, 0])
        c.play(Create(axis, run_time=0.5), rt=0.5)
        c.wait(1.0)
        c.play(Create(yax, run_time=0.5), rt=0.5)
        c.wait(1.0)
        c.play(FadeIn(yl, run_time=0.5), rt=0.5)
        c.wait(0.9)
        c.play(FadeIn(ylab, run_time=0.5), rt=0.5)
        c.wait(1.2)

        for x, (dv, snp, frac, pct, hero) in zip(xs, rows):
            col = TEAL_DK if hero else TEAL
            h = span * pct / 100.0
            bar = Rectangle(width=1.35, height=h, stroke_width=0).set_fill(col, 1.0)
            bar.move_to([x, base_y + h / 2, 0])
            dvl = Body(dv, font_size=20, color=(TEAL_TXT if hero else INK)
                       ).move_to([x, base_y - 0.42, 0])
            snpl = Body(f"{snp} SNPs / 5 kb", font_size=17, color=SRCGRAY
                        ).move_to([x, base_y - 0.78, 0])
            fl = Body(frac, font_size=18, color="#FFFFFF").move_to([x, base_y + h - 0.28, 0])
            pl = Body(f"{pct}%", font_size=22, color=(TEAL_TXT if hero else INK),
                      font=FONT_TITLE).move_to([x, base_y + h + 0.28, 0])
            c.play(GrowFromEdge(bar, edge=DOWN, run_time=0.6), rt=0.6)
            c.play(FadeIn(VGroup(dvl, snpl), run_time=0.45), rt=0.45)
            c.wait(1.3)
            c.play(FadeIn(pl, run_time=0.35), FadeIn(fl, run_time=0.35), rt=0.4)
            c.wait(2.1)

        c.play(FadeOut(s1, run_time=0.4), rt=0.4)
        star = Body("the divergence this organism actually shows",
                    font_size=20, color=TEAL_TXT).move_to([0, top_y + 0.72, 0])
        c.play(FadeIn(star, run_time=0.6), rt=0.6)
        c.wait(2.8)

        note = Body("Below it detection falls away: the window's lower edge, from a second direction.",
                    font_size=21, color=INK).move_to([0, top_y + 0.72, 0])
        c.play(FadeOut(star, run_time=0.4), rt=0.4)
        c.play(FadeIn(note, run_time=0.6), rt=0.6)
        c.hold_to(45.0)


# ============================================================================
#  ACT 6.  What you now have.                                target 29.0 s
#  Entry: the sweep.  Exit: the window with both bounds, handing to clip 3.
#  Both bounds are BRACKETS, not points.
# ============================================================================
class Clip2Act6(Scene):
    def construct(self):
        c = Clock(self)
        title = act_title("What you now have")
        self.add(title)
        c.wait(1.1)

        ax = diversity_axis(label=False)
        band = window_band()
        self.add(ax)
        c.play(FadeIn(band, run_time=0.7), rt=0.7)
        c.wait(1.8)

        # three properties of the instrument -- tick then text, each its own beat
        claims = [
            "Returns essentially nothing when nothing is there.  1.32%",
            "Recovers nine tenths at the relevant divergence.  91%",
            "Works only between a measured lower edge and a measured upper edge.",
        ]
        cg = VGroup(*[Body(s, font_size=24, color=INK) for s in claims])
        cg.arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to([0, 1.95, 0])
        for m in cg:
            tick = Line(m.get_left() + [-0.5, -0.02, 0], m.get_left() + [-0.28, -0.02, 0],
                        stroke_width=3, color=TEAL)
            c.play(Create(tick, run_time=0.3), rt=0.3)
            c.play(FadeIn(m, shift=RIGHT * 0.1, run_time=0.6), rt=0.6)
            c.wait(2.5)

        def bracket(v_lo, v_hi):
            xl, xh = dax_x(v_lo), dax_x(v_hi)
            mid = (xl + xh) / 2
            half = max((xh - xl) / 2, 0.09)
            xl, xh = mid - half, mid + half
            y = DAX_Y
            seg = Line([xl, y, 0], [xh, y, 0], stroke_width=4, color=RUST)
            cap_l = Line([xl, y - 0.12, 0], [xl, y + 0.12, 0], stroke_width=4, color=RUST)
            cap_h = Line([xh, y - 0.12, 0], [xh, y + 0.12, 0], stroke_width=4, color=RUST)
            return VGroup(seg, cap_l, cap_h)
        fb = bracket(FLOOR_LO, FLOOR_HI)
        cb = bracket(CEIL_LO, CEIL_HI)
        bl_f = Body("lower edge 700, range 588 to 755", font_size=20, color=INK
                    ).move_to([0, 0.35, 0])
        bl_c = Body("upper edge 4,700, range 4,632 to 4,732", font_size=20, color=INK
                    ).move_to([0, -0.15, 0])
        note = Body("Both bounds are ranges, not points.", font_size=21,
                    color=TEAL_TXT).move_to([0, 0.9, 0])
        c.play(FadeIn(note, run_time=0.6), rt=0.6)
        c.wait(2.3)
        # floor bracket, then its label; ceiling bracket, then its label --------
        c.play(FadeIn(fb, run_time=0.5), rt=0.5)
        c.play(FadeIn(bl_f, run_time=0.5), rt=0.5)
        c.wait(2.8)
        c.play(FadeIn(cb, run_time=0.5), rt=0.5)
        c.play(FadeIn(bl_c, run_time=0.5), rt=0.5)
        c.wait(3.2)

        hand = Body("That is a ruler. Clip three points it at the data.",
                    font_size=25, color=TEAL_TXT).move_to([0, -0.62, 0])
        c.play(FadeIn(hand, run_time=0.7), rt=0.7)
        c.hold_to(29.0)
