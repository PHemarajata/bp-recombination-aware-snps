from manim import *
import numpy as np

# ============================================================================
#  TUC BRIEFING SERIES - CLIP 3: "What the ruler measured"
#
#  Seven acts. Five rendered here, two dropped in whole as the merged revised
#  legacy renders:
#    act 4 lead-in (C3Act4Lead) then RecursiveSubdivision.mp4, 35.7 s
#    act 5 lead-in (C3Act5Lead) then TreeBuilderPaired.mp4, 26.6 s
#
#  THE CLAIM. Applying the measured window turns one uninterpretable average
#  into a measurement and a diagnosis: inside the window the recombination to
#  mutation ratio is 7.70, outside it is 1.99, and that contrast means a low
#  ratio is the detector failing rather than the genome being quiet.
#
#  CONTINUITY OBJECT: the 85 analysis units. They arrive in act 1 as 85
#  undifferentiated marks on a diversity axis and stay on screen, in the same
#  style, for the whole clip. Their diversity positions are MEASURED, read from
#  GATE1_ALIGNMENT_2026-08-21.tsv aln_mean_pairwise_snps, not placed by hand.
#
#  EVERY NUMBER REPRODUCED FROM SOURCE BEFORE IT WAS DRAWN, 2026-09-17.
#  Repo: /Users/peerahemarajata/bp-recombination-aware-snps
#    naive pooled median 5.51, labeled the number being corrected . rm.median_all_units
#    in-window 47 units, median 7.70, IQR 5.72 to 9.41, 1,388 genomes . TABLES.md Table 2
#    below floor 12 units, median 1.32, 349 genomes ................. TABLES.md Table 2
#    above ceiling 26 units, median 2.14, 603 genomes ............... TABLES.md Table 2
#    pooled outside window, 38 units, median 1.99 ................... rm.median_outside_gate1
#    window floor 700, bracket (588, 755]; ceiling 4700 ............. rm.gate1_floor / ceiling
#    floor sensitivity 7.70, 7.70, 7.74, 7.78 at 588/700/755/840 .... rm.floor_sensitivity
#    tree builder: IQ-TREE vs RAxML 0.988, 7 of 12, p 0.77 ......... TABLES.md Table 5
#        rapidnj vs RAxML 0.922, 11 of 12, p 0.0063 ................. TABLES.md Table 5
#    34 of 47 in-window units contain funded isolates,
#        10 fall below the 7-member floor without them,
#        their median r/m 7.74 against 7.70 for all in-window ...... FINAL_BASIS join GATE1
#
#  TWO NUMBER COLLISIONS, both handled per the brief:
#    7.74 is act 6's floor-755 sensitivity AND act 7's funded median. Act 6
#      shows its four values as DEVIATIONS from 7.70 (+0.00 +0.00 +0.04 +0.08),
#      so the absolute 7.74 appears only in act 7.
#    47 is a unit count (act 2 in-window) and a genome count (Table 3 middle
#      child, in the reused act 4). Units and genomes are labeled distinctly.
# ============================================================================

config.background_color = "#FFFFFF"     # never dark theme

TEAL      = "#00A0AF"   # genomic / the measured signal (fills, marks)
TEAL_TXT  = "#006E79"   # text-safe teal (any teal carrying a glyph)
TEAL_DK   = "#005057"   # deepest teal. SERIES: the funded isolates
TEAL_LT   = "#A3CCCC"   # light teal. background / unclassified
PURPLE    = "#9960A7"   # geography (not used in this clip)
RUST      = "#B42E34"   # a limit or a failure, adverse outcome ONLY
INK       = "#404040"   # default ink
GRIDGRAY  = "#E2E9EC"   # gridlines / neutral shaded zones
SRCGRAY   = "#6E6E6E"   # source-line gray
GRAYOUT   = "#6E6E6E"

FONT_TITLE = "Franklin Gothic Medium"
FONT_BODY  = "Franklin Gothic Book"
DEFAULT_FONT_SIZE = 28
Text.set_default(font=FONT_BODY, color=INK)

SUB_TOP = -3.0          # reserved bottom eighth carries captions
MARGIN  = 0.82          # 110 px at 1080p; content inside +/- 6.29


def Txt(s, font_size=DEFAULT_FONT_SIZE, **kw):
    """House crisp-text helper with the corrected wrap guard (clip 1 fix):
    width, not height, detects a Pango wrap, because a wrapped fragment placed
    in the same line box as an explicit newline leaves height unchanged and
    only collapses width."""
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


def Title(s, font_size=34, color=TEAL_TXT, **kw):
    kw.setdefault("font", FONT_TITLE)
    return Txt(s, font_size=font_size, color=color, **kw)


def Body(s, font_size=DEFAULT_FONT_SIZE, color=INK, **kw):
    kw.setdefault("font", FONT_BODY)
    return Txt(s, font_size=font_size, color=color, **kw)


def title_block(title, subtitle=None):
    """Left-aligned teal title with an optional gray subtitle beneath it,
    matching the two reused clips."""
    t = Title(title).to_edge(UP, buff=0.5).to_edge(LEFT, buff=MARGIN)
    g = VGroup(t)
    if subtitle:
        s = Body(subtitle, font_size=22, color=INK).next_to(t, DOWN, buff=0.18
                 ).to_edge(LEFT, buff=MARGIN)
        g.add(s)
    return g


def source_note(s):
    n = Body(s, font_size=20, color=SRCGRAY)
    n.to_edge(LEFT, buff=MARGIN).set_y(SUB_TOP + 0.28)
    return n


# ---- the diversity axis, shared across acts --------------------------------
# x maps unit diversity (mean pairwise core SNPs) on a log scale. The window
# [700, 4700] is a vertical band; both bounds are brackets, drawn with soft
# edges in act 6.
AX_L, AX_R = -5.60, 5.30          # axis extent in scene x
DIV_LO, DIV_HI = 12.0, 11000.0    # log domain covering 15 to 9131
FLOOR, CEIL = 700.0, 4700.0
FLOOR_BR = (588.0, 755.0)
CEIL_BR = (4632.0, 4732.0)


def div_x(d):
    t = (np.log10(d) - np.log10(DIV_LO)) / (np.log10(DIV_HI) - np.log10(DIV_LO))
    return AX_L + t * (AX_R - AX_L)


UNITS = [
    (15.4, "b", 0), (40.6, "b", 0), (42.8, "b", 0), (113.9, "b", 0), (121.5, "b", 1), (211.0, "b", 0),
    (243.3, "b", 0), (285.6, "b", 0), (405.0, "b", 0), (511.2, "b", 0), (535.0, "b", 1), (587.6, "b", 1),
    (754.8, "i", 0), (797.0, "i", 0), (840.1, "i", 1), (852.2, "i", 1), (909.4, "i", 1), (1032.9, "i", 1),
    (1120.5, "i", 1), (1121.3, "i", 1), (1284.1, "i", 1), (1310.3, "i", 1), (1334.7, "i", 0), (1348.8, "i", 1),
    (1355.2, "i", 1), (1433.8, "i", 1), (1513.6, "i", 1), (1573.9, "i", 0), (1595.7, "i", 0), (1610.4, "i", 1),
    (1676.1, "i", 1), (1828.5, "i", 0), (1908.8, "i", 1), (1949.9, "i", 1), (1996.3, "i", 0), (2010.3, "i", 0),
    (2014.6, "i", 1), (2109.1, "i", 0), (2211.5, "i", 1), (2259.7, "i", 0), (2298.9, "i", 0), (2449.1, "i", 1),
    (2738.6, "i", 1), (3020.5, "i", 1), (3020.7, "i", 1), (3079.6, "i", 1), (3363.0, "i", 1), (3374.8, "i", 1),
    (3402.6, "i", 1), (3417.2, "i", 1), (3424.0, "i", 1), (3452.1, "i", 0), (3759.3, "i", 1), (3903.0, "i", 1),
    (4011.6, "i", 0), (4247.0, "i", 1), (4463.1, "i", 1), (4524.9, "i", 1), (4631.8, "i", 1), (4731.6, "a", 0),
    (4750.2, "a", 1), (4923.3, "a", 1), (5168.5, "a", 1), (5198.0, "a", 0), (5721.1, "a", 1), (5818.9, "a", 1),
    (6094.2, "a", 1), (6213.6, "a", 1), (6361.8, "a", 1), (6364.6, "a", 1), (6386.6, "a", 1), (6531.6, "a", 1),
    (6629.2, "a", 1), (6796.8, "a", 1), (6839.4, "a", 0), (6909.7, "a", 0), (7207.9, "a", 1), (7430.6, "a", 0),
    (7775.7, "a", 0), (8197.2, "a", 1), (8342.7, "a", 0), (8541.1, "a", 1), (8648.0, "a", 1), (8756.6, "a", 1),
    (9131.1, "a", 1),
]


# The band is 1.9 tall about UY, so it reaches 1.05 at the top and -0.85 at the
# bottom. Text laid across either edge is half on the tint and half on the page
# and reads as broken. Clip 3 shipped ten of these because "the gap above the
# axis" was taken to start at -0.75. Exactly one text row fits above the band
# and exactly one fits below it; put every line on one of them.
BAND_TOP  =  1.05
BAND_BOT  = -0.85
ROW_ABOVE =  1.36
ROW_BELOW = -1.18


# ---- unit-mark helpers -----------------------------------------------------
ORANGE = "#E37C1D"                  # above-ceiling class only
UY = 0.10                          # baseline y for the unit strip
CLS_COL = {"i": TEAL, "b": RUST, "a": ORANGE}

def unit_dot(state="plain", r=0.058):
    """One analysis unit. Plain (unclassified) is light teal. Classified marks
    carry their class by hue AND by which side of the window band they sit on,
    so hue is never the only channel."""
    col = {"plain": TEAL_LT, "i": TEAL, "b": RUST, "a": ORANGE,
           "funded": TEAL_DK}[state]
    return Dot(radius=r, color=col).set_fill(col, 1.0).set_stroke(width=0)


def jitter_y(i, band=0.62, seed=7):
    rng = np.random.default_rng(seed + i * 131)
    return UY + rng.uniform(-band, band)


def unit_strip(states=None, funded_ring=False):
    """Place the 85 measured units along the log diversity axis, jittered in y
    so a strip of 85 reads as a cloud rather than a line."""
    g = VGroup()
    for i, (d, c, f) in enumerate(UNITS):
        st = "plain" if states is None else (c if states == "class" else states)
        dot = unit_dot(st).move_to([div_x(d), jitter_y(i), 0])
        dot.unit_i, dot.unit_c, dot.unit_f, dot.unit_d = i, c, f, d
        g.add(dot)
    return g


def axis_line():
    ax = Line([AX_L, -1.55, 0], [AX_R, -1.55, 0], stroke_width=2.0, color=INK)
    ticks = VGroup()
    for d, lab in ((100, "100"), (1000, "1,000"), (10000, "10,000")):
        x = div_x(d)
        ticks.add(Line([x, -1.55, 0], [x, -1.67, 0], stroke_width=2.0, color=INK))
        ticks.add(Body(lab, font_size=20, color=SRCGRAY).move_to([x, -1.90, 0]))
    cap = Body("unit diversity, mean pairwise core SNPs", font_size=20, color=INK)
    cap.move_to([(AX_L + AX_R) / 2, -2.34, 0])
    return VGroup(ax, ticks, cap)


def window_band(soft=False):
    x0, x1 = div_x(FLOOR), div_x(CEIL)
    band = Rectangle(width=x1 - x0, height=1.9, stroke_width=0
                     ).set_fill(GRIDGRAY, 1.0)
    band.move_to([(x0 + x1) / 2, UY, 0])
    if soft:
        # both bounds are brackets: show the floor and ceiling as bands, not lines
        fb = Rectangle(width=div_x(FLOOR_BR[1]) - div_x(FLOOR_BR[0]), height=1.9,
                       stroke_width=0).set_fill(TEAL_LT, 0.7)
        fb.move_to([(div_x(FLOOR_BR[0]) + div_x(FLOOR_BR[1])) / 2, UY, 0])
        cb = Rectangle(width=div_x(CEIL_BR[1]) - div_x(CEIL_BR[0]), height=1.9,
                       stroke_width=0).set_fill(TEAL_LT, 0.7)
        cb.move_to([(div_x(CEIL_BR[0]) + div_x(CEIL_BR[1])) / 2, UY, 0])
        return VGroup(band, fb, cb)
    return VGroup(band)


# ============================================================================
#  ACT 1. Eighty-five units, one ruler        target 31.0 s, ~70 words
#  Entry: black.  Exit: 85 marks on the diversity axis, unclassified.
# ============================================================================
class C3Act1(Scene):
    def construct(self):
        # title card, 1.5 s hold
        ft = Title("What the ruler measured", font_size=46).move_to([0, 0.42, 0])
        fs = Body("TUC briefing, clip three of four", font_size=25, color=SRCGRAY
                  ).move_to([0, -0.42, 0])
        self.play(FadeIn(ft, run_time=0.8), run_time=0.8)                  # 0.8
        self.play(FadeIn(fs, run_time=0.5), run_time=0.5)                  # 1.3
        self.wait(1.5)                                                     # 2.8
        self.play(FadeOut(ft, fs, run_time=0.6), run_time=0.6)             # 3.4

        head = title_block("Eighty-five units, one ruler")
        src = source_note("85 analysis units, 2,340 genomes. Diversity is measured")
        self.play(FadeIn(head, run_time=0.6), FadeIn(src, run_time=0.6),
                  run_time=0.6)                                            # 4.0
        self.wait(0.6)                                                     # 4.6

        recall = Body("Clip two built one instrument: the recombination window.",
                      font_size=26, color=INK).move_to([0, 1.75, 0])
        self.play(FadeIn(recall, run_time=0.7), run_time=0.7)              # 5.3
        self.wait(3.7)                                                     # 9.0

        point = Body("Now point it at the eighty-five units.",
                     font_size=26, color=TEAL_TXT).move_to([0, 1.10, 0])
        self.play(FadeIn(point, run_time=0.7), run_time=0.7)              # 9.7
        self.wait(2.3)                                                     # 12.0

        # the axis, then the 85 measured marks
        axis = axis_line()
        self.play(Create(axis[0], run_time=0.7), FadeIn(axis[1], run_time=0.7),
                  FadeIn(axis[2], run_time=0.7), run_time=0.9)             # 12.9
        self.wait(1.1)                                                     # 14.0

        strip = unit_strip(states="plain")
        self.play(LaggedStartMap(FadeIn, strip, lag_ratio=0.014, run_time=2.0),
                  run_time=2.0)                                            # 16.0
        n_lab = Body("Each mark is one unit, placed by its diversity.",
                     font_size=24, color=INK).move_to([0, 2.55, 0])
        self.play(FadeIn(n_lab, run_time=0.7), run_time=0.7)              # 16.7
        self.wait(3.3)                                                     # 20.0

        rm_lab = Body("Each unit also has a recombination-to-mutation ratio.",
                      font_size=24, color=INK).move_to([0, 1.75, 0])
        self.play(FadeOut(VGroup(recall, point), run_time=0.5),
                  FadeIn(rm_lab, run_time=0.6), run_time=0.6)              # 20.6
        self.wait(3.4)                                                     # 24.0

        # the window was measured first: this is a test, not a selection
        first = Body("The window was measured before any of these ratios were read.",
                     font_size=25, color=INK).move_to([0, 1.10, 0])
        self.play(FadeIn(first, run_time=0.7), run_time=0.7)              # 24.7
        self.wait(3.3)                                                     # 28.0

        # MOVED 2026-09-18: y 0.45 sat inside the unit strip (UY 0.10 +/- 0.62),
        # so this line printed across the dots. Below the strip, above the axis.
        test = Body("That makes this a test, not a selection.",
                    font_size=25, color=TEAL_TXT).move_to([0, -1.00, 0])
        self.play(FadeIn(test, run_time=0.7), run_time=0.7)              # 28.7
        self.wait(2.3)                                                     # 31.0


# ============================================================================
#  ACT 2. The split, and the contrast        target 65.0 s, ~145 words
#  Entry: 85 unclassified marks.  Exit: three classes, each with its median.
# ============================================================================
class C3Act2(Scene):
    def construct(self):
        head = title_block("The split, and the contrast")
        src = source_note("Table 2, Gate 1 classification. Medians are measured r/m")
        axis = axis_line()
        strip = unit_strip(states="plain")
        self.add(head, src, axis, strip)
        self.wait(0.6)                                                    # 0.6

        # --- the naive number, named as the thing being corrected ------
        naive = Body("Pooled across all eighty-five units, the median ratio is",
                     font_size=25, color=INK).move_to([-0.7, 2.55, 0])
        nv = Body("5.51", font_size=34, color=INK, font=FONT_TITLE)
        nv.next_to(naive, RIGHT, buff=0.30)
        self.play(FadeIn(naive, run_time=0.6), FadeIn(nv, run_time=0.6),
                  run_time=0.7)                                           # 1.3
        self.wait(2.7)                                                    # 4.0
        corr = Body("This blends real measurements with detection failures. "
                    "It is not a result.", font_size=23, color=RUST)
        corr.move_to([0, 1.95, 0])
        self.play(FadeIn(corr, run_time=0.7), run_time=0.7)              # 4.7
        self.wait(3.3)                                                    # 8.0

        # --- apply the window ------------------------------------------
        band = window_band()
        b_lab = Body("the measured window", font_size=21, color=INK)
        b_lab.move_to([(div_x(FLOOR) + div_x(CEIL)) / 2, ROW_ABOVE, 0])
        self.play(FadeOut(VGroup(naive, nv, corr), run_time=0.5),
                  run_time=0.5)                                           # 8.5
        self.play(FadeIn(band, run_time=0.8), FadeIn(b_lab, run_time=0.6),
                  run_time=0.8)                                           # 9.3
        # band sits behind the marks
        band.set_z_index(-1)
        self.wait(1.7)                                                    # 11.0

        # --- classify the marks in place -------------------------------
        anims = []
        for d in strip:
            anims.append(d.animate.set_color(CLS_COL[d.unit_c]))
        self.play(*anims, run_time=1.2)                                   # 12.2
        self.wait(2.8)                                                    # 15.0

        # --- three class rows, each with count, median, genome count ---
        ROWS = [
            ("In the window",    "47 units",  "7.70", "1,388 genomes", TEAL_TXT),
            ("Below the window", "12 units",  "1.32", "349 genomes",   RUST),
            ("Above the window", "26 units",  "2.14", "603 genomes",   ORANGE),
        ]
        LX = -6.05
        head_u = Body("units", font_size=20, color=SRCGRAY).move_to([-0.05, 2.82, 0])
        head_m = Body("median r/m", font_size=20, color=SRCGRAY).move_to([1.75, 2.82, 0])
        head_g = Body("genomes", font_size=20, color=SRCGRAY).move_to([3.75, 2.82, 0])
        # RAISED 2026-09-18 from [2.15, 1.65, 1.15]: the third row sat at 1.15 and
        # its median and genome count were cut by the top edge of the band.
        RY = [2.36, 1.86, ROW_ABOVE]
        built = []
        for i, (nm, un, md, gn, col) in enumerate(ROWS):
            sw = Square(side_length=0.20, stroke_width=0).set_fill(col, 1.0
                        ).move_to([LX, RY[i], 0])
            name = Body(nm, font_size=22, color=INK).next_to(sw, RIGHT, buff=0.18)
            un_l = Body(un, font_size=22, color=INK).move_to([-0.05, RY[i], 0])
            md_l = Body(md, font_size=24, color=col, font=FONT_TITLE
                        ).move_to([1.75, RY[i], 0])
            gn_l = Body(gn, font_size=21, color=SRCGRAY).move_to([3.75, RY[i], 0])
            built.append(VGroup(sw, name, un_l, md_l, gn_l))
        self.play(FadeIn(VGroup(head_u, head_m, head_g), run_time=0.5),
                  FadeOut(b_lab, run_time=0.5), run_time=0.5)             # 15.5
        self.play(FadeIn(built[0], run_time=0.8), run_time=0.8)          # 16.3
        self.wait(3.7)                                                   # 20.0
        self.play(FadeIn(built[1], run_time=0.8), run_time=0.8)          # 20.8
        self.wait(2.2)                                                   # 23.0
        self.play(FadeIn(built[2], run_time=0.8), run_time=0.8)          # 23.8
        self.wait(3.2)                                                   # 27.0

        # MOVED 2026-09-18 from y 0.62, the top edge of the unit strip, then to
        # ROW_BELOW because -0.95 still clipped the band. "IQR" is the last piece
        # of statistical shorthand on screen in this clip; it says the same thing.
        iqr = Body("Half of them fall between 5.72 and 9.41.", font_size=23,
                   color=TEAL_TXT).move_to([-3.55, ROW_BELOW, 0], aligned_edge=LEFT)
        self.play(FadeIn(iqr, run_time=0.6), run_time=0.6)              # 27.6
        # EXTENDED 2026-09-18 from 3.4 s. Five measured facts are on screen here
        # and 3.4 s is not long enough to say them, so the narration finished
        # describing the rows well after they had been wiped.
        self.wait(8.4)                                                   # 36.0

        # --- the contrast, which is the whole act ----------------------
        # Values live in the top band, never over a mark, so a number can never
        # sit on the wrong-colored cloud. In-window marks stay teal at full
        # opacity; the below-floor and above-ceiling marks dim as they pool.
        self.play(FadeOut(VGroup(head_u, head_m, head_g, built[0], built[1],
                                 built[2], iqr), run_time=0.6), run_time=0.6)  # 31.6
        dim = [d.animate.set_opacity(0.32) for d in strip if d.unit_c != "i"]
        self.play(*dim, run_time=0.8)                                    # 32.4
        inw = Body("Inside the window", font_size=24, color=TEAL_TXT
                   ).move_to([-3.35, 2.62, 0])
        inw_v = Body("7.70", font_size=38, color=TEAL_TXT, font=FONT_TITLE
                     ).next_to(inw, DOWN, buff=0.20)
        self.play(FadeIn(inw, run_time=0.5), FadeIn(inw_v, run_time=0.6),
                  run_time=0.7)                                          # 33.1
        self.wait(3.9)                                                   # 37.0

        out = Body("Pooled outside it, 38 units", font_size=24, color=INK
                   ).move_to([3.15, 2.62, 0])
        out_v = Body("1.99", font_size=38, color=INK, font=FONT_TITLE
                     ).next_to(out, DOWN, buff=0.20)
        self.play(FadeIn(out, run_time=0.5), FadeIn(out_v, run_time=0.6),
                  run_time=0.7)                                          # 37.7
        self.wait(4.3)                                                   # 42.0

        # MOVED 2026-09-18 from y -0.80, which was cut by the band's lower edge.
        # Only one text row fits below the band and the closing line needs it.
        vs = Body("Same arithmetic. Two populations of units.",
                  font_size=25, color=INK).move_to([0, 1.40, 0])
        self.play(FadeIn(vs, run_time=0.7), run_time=0.7)               # 42.7
        self.wait(4.3)                                                   # 47.0

        point = Body("The contrast between 7.70 and 1.99 is the finding.",
                     font_size=26, color=TEAL_TXT).move_to([0, ROW_BELOW, 0])
        self.play(FadeIn(point, run_time=0.7), run_time=0.7)           # 47.7
        self.wait(4.3)                                                   # 52.0

        # restore the full strip for the act 3 held frame
        self.play(FadeOut(VGroup(inw, inw_v, out, out_v, vs, point),
                          run_time=0.6),
                  *[d.animate.set_opacity(1.0) for d in strip if d.unit_c != "i"],
                  run_time=0.8)                                          # 52.8
        settle = Body("Three classes. One of them is the measurement.",
                      font_size=24, color=INK).move_to([0, 2.55, 0])
        self.play(FadeIn(settle, run_time=0.7), run_time=0.7)          # 53.5
        # SHORTENED 2026-09-18 from 11.5 s. The act was padded to a stated
        # 65 s target, so it ended with an eleven-second hold on a still frame
        # that nothing was said over. With act 3's own lead-in that produced
        # twelve and a half seconds of dead air, which is what a viewer hears
        # as the audio dropping out.
        self.wait(4.5)                                                   # 58.0


# ============================================================================
#  ACT 3. The reversal                        target 48.0 s, ~110 words
#  Entry: three classes.  Exit: the same three classes, re-read.
#  Deliberately still: narration over a held frame. The stillness is the point.
# ============================================================================
class C3Act3(Scene):
    def construct(self):
        head = title_block("The reversal")
        src = source_note("Nothing new appears. The same picture, read the other way")
        axis = axis_line()
        strip = unit_strip(states="class")
        band = window_band()
        band.set_z_index(-1)
        self.add(head, src, axis, band, strip)
        self.wait(1.0)                                                    # 1.0

        # the single most important idea in the series, stated slowly
        l1 = Body("A unit below the window is not a unit with little recombination.",
                  font_size=26, color=INK).move_to([0, 2.55, 0])
        # the picture is held but recedes: dim the marks so the re-reading text
        # is legible over them. Nothing new appears, which the stillness keeps.
        self.play(FadeIn(l1, run_time=0.8),
                  *[d.animate.set_opacity(0.32) for d in strip], run_time=0.8)  # 1.8
        self.wait(4.2)                                                    # 6.0

        # point at the below-floor cloud
        b_note = Body("below the window: too little diversity to find any",
                      font_size=22, color=RUST).move_to([-3.40, ROW_ABOVE, 0])
        self.play(FadeIn(b_note, run_time=0.7), run_time=0.7)           # 6.7
        self.wait(4.3)                                                    # 11.0

        l2 = Body("The detector returns a small number, and the small number "
                  "means nothing.", font_size=25, color=INK).move_to([0, 1.86, 0])
        self.play(FadeIn(l2, run_time=0.8), run_time=0.8)               # 11.8
        self.wait(4.2)                                                    # 16.0

        # point at the above-ceiling cloud
        # MOVED 2026-09-18. At y 0.95 this label was printed across the shaded
        # window itself, which is the one thing on screen it is not about.
        a_note = Body("above the window: the estimate falls apart",
                      font_size=22, color=ORANGE).move_to([3.15, ROW_ABOVE, 0])
        self.play(FadeIn(a_note, run_time=0.7), run_time=0.7)           # 16.7
        self.wait(4.3)                                                    # 21.0

        # the line, held
        # MOVED 2026-09-18. The rule ran across the unit strip at y -0.20 and the
        # headline sat inside it at 0.30, so the single most important line in the
        # series was printed over the data. The two build-up lines have been read
        # by now, so they clear and the headline takes their space.
        rule = Line([-4.6, 1.55, 0], [4.6, 1.55, 0], stroke_width=2.0, color=TEAL)
        big = Body("A low ratio is a detection failure, not a quiet genome.",
                   font_size=30, color=TEAL_TXT).move_to([0, 2.10, 0])
        # the two pointers have been read by now and the rule would cross them
        self.play(FadeOut(VGroup(l1, l2, b_note, a_note), run_time=0.6),
                  Create(rule, run_time=0.7), run_time=0.7)             # 21.7
        self.play(FadeIn(big, run_time=0.9), run_time=0.9)              # 22.6
        self.wait(5.4)                                                    # 28.0

        # let it sit, then one closing clause
        # MOVED 2026-09-18 from -0.82 and -1.26. There is room for exactly one
        # line between the band and the axis, so these two take it in turn
        # rather than one of them being cut by the band's lower edge.
        close = Body("Only the units inside the window are quiet or loud on purpose.",
                     font_size=24, color=INK).move_to([0, ROW_BELOW, 0])
        self.play(FadeIn(close, run_time=0.8), run_time=0.8)            # 28.8
        self.wait(4.2)                                                    # 33.0

        keep = Body("Every number outside the window is the ruler running out of range.",
                    font_size=24, color=INK).move_to([0, ROW_BELOW, 0])
        self.play(FadeOut(close, run_time=0.5),
                  FadeIn(keep, run_time=0.8), run_time=0.8)             # 33.8
        self.wait(6.2)                                                    # 40.0
        self.wait(8.0)                                                    # 48.0


# ============================================================================
#  ACT 4 LEAD-IN. First silent failure: a correct split         target 14.0 s
#  Entry: three classes.  Exit: hands to RecursiveSubdivision.mp4 (35.7 s).
#  Frames why a unit can leave the measurable set for a good reason.
# ============================================================================
class C3Act4Lead(Scene):
    def construct(self):
        head = title_block("A class is not permanent")
        src = source_note("Worked demonstration. Not part of the reported 85 units")
        axis = axis_line()
        strip = unit_strip(states="class")
        band = window_band()
        band.set_z_index(-1)
        self.add(head, src, axis, band, strip)
        self.wait(0.8)                                                    # 0.8

        l1 = Body("The classes are not fixed.", font_size=27, color=TEAL_TXT
                  ).move_to([0, 2.55, 0])
        self.play(FadeIn(l1, run_time=0.7), run_time=0.7)               # 1.5
        self.wait(2.5)                                                    # 4.0

        l2 = Body("A decision taken for good reasons elsewhere in the pipeline",
                  font_size=25, color=INK).move_to([0, 1.86, 0])
        self.play(FadeIn(l2, run_time=0.7), run_time=0.7)               # 4.7
        self.wait(2.3)                                                    # 7.0

        # one in-window mark drifts left, across the floor
        target = None
        for d in strip:
            if d.unit_c == "i" and d.unit_d < 900:
                target = d
                break
        arrow = Arrow(target.get_center() + [0.1, 0.6, 0],
                      [div_x(300), UY + 0.35, 0], buff=0.1, stroke_width=3,
                      color=INK, max_tip_length_to_length_ratio=0.12)
        l3 = Body("can move a unit out of the measurable set,",
                  font_size=25, color=INK).move_to([0, ROW_ABOVE, 0])
        self.play(FadeIn(l3, run_time=0.6), run_time=0.6)               # 7.6
        self.play(target.animate.move_to([div_x(300), UY + 0.35, 0]).set_color(RUST),
                  GrowArrow(arrow, run_time=0.9), run_time=0.9)          # 8.5
        self.wait(1.5)                                                    # 10.0

        # MOVED 2026-09-18 from y 0.50 (inside the unit strip), then to
        # ROW_BELOW because -0.95 still clipped the band's lower edge.
        l4 = Body("with no one noticing the cost.", font_size=25, color=RUST
                  ).move_to([0, ROW_BELOW, 0])
        self.play(FadeIn(l4, run_time=0.7), run_time=0.7)               # 10.7
        self.wait(1.3)                                                    # 12.0

        # MOVED 2026-09-18 from y -0.30, which was inside the band AND on top of
        # the unit marks. The opening line has been read, so it gives up its row.
        nxt = Body("Watch one real unit divide.", font_size=24, color=INK
                   ).move_to([0, 2.55, 0])
        # The whole sentence has been read, so it clears: leaving it up while
        # the hand-off line sits above it puts the two in the wrong reading order.
        self.play(FadeOut(VGroup(l1, l2, l3, l4), run_time=0.5),
                  FadeIn(nxt, run_time=0.7), run_time=0.7)              # 12.7
        self.wait(1.3)                                                    # 14.0


# ============================================================================
#  ACT 5 LEAD-IN. Second silent failure: the tree builder       target 14.0 s
#  Entry: as act 4 leaves it.  Exit: hands to TreeBuilderPaired.mp4 (26.6 s).
# ============================================================================
class C3Act5Lead(Scene):
    def construct(self):
        head = title_block("The tree underneath the number")
        src = source_note("r/m is estimated on a tree")
        self.play(FadeIn(head, run_time=0.6), FadeIn(src, run_time=0.6),
                  run_time=0.6)                                           # 0.6
        self.wait(0.4)                                                    # 1.0

        l1 = Body("Every ratio was estimated on a tree.", font_size=27, color=INK
                  ).move_to([0, 2.10, 0])
        self.play(FadeIn(l1, run_time=0.7), run_time=0.7)               # 1.7
        self.wait(2.3)                                                    # 4.0

        # a small schematic tree
        root = [-0.2, 1.15, 0]
        a = [-1.7, -0.35, 0]; b = [-0.55, -0.35, 0]; c = [1.35, -0.35, 0]
        mid = [0.4, 0.42, 0]
        tree = VGroup(
            Line(root, [-1.1, 0.42, 0], stroke_width=2.4, color=GRAYOUT),
            Line([-1.1, 0.42, 0], a, stroke_width=2.4, color=GRAYOUT),
            Line([-1.1, 0.42, 0], b, stroke_width=2.4, color=GRAYOUT),
            Line(root, mid, stroke_width=2.4, color=GRAYOUT),
            Line(mid, c, stroke_width=2.4, color=GRAYOUT),
        )
        tips = VGroup(*[Dot(radius=0.07, color=TEAL).set_fill(TEAL, 1.0)
                        .move_to(p) for p in (a, b, c)])
        self.play(Create(tree, run_time=0.9), FadeIn(tips, run_time=0.6),
                  run_time=0.9)                                           # 4.9
        self.wait(1.1)                                                    # 6.0

        q = Body("Does the choice of tree builder change the answer?",
                 font_size=26, color=TEAL_TXT).move_to([0, -1.35, 0])
        self.play(FadeIn(q, run_time=0.8), run_time=0.8)                # 6.8
        self.wait(3.2)                                                    # 10.0

        setup = Body("Six units, two replicons, twelve comparisons.",
                     font_size=24, color=INK).move_to([0, -2.05, 0])
        self.play(FadeIn(setup, run_time=0.7), run_time=0.7)            # 10.7
        self.wait(3.3)                                                    # 14.0


# ============================================================================
#  ACT 6. Is the window itself arbitrary?     target 28.0 s, ~65 words
#  Entry: twelve comparisons.  Exit: 7.70 restated, now with its bracket.
#
#  REFUSAL CLAUSE ANSWERED. A sensitivity is not a result. Drawn so the viewer
#  sees "the answer does not depend on this choice": the four recomputed medians
#  are plotted as DEVIATIONS from 7.70 on a tight axis, a nearly flat line, not
#  as four fresh numbers. This also resolves the 7.74 collision with act 7,
#  because the absolute value never appears here.
# ============================================================================
class C3Act6(Scene):
    # lower-edge candidate, in-window median at that edge
    FLOORS = [(588, 7.70), (700, 7.70), (755, 7.74), (840, 7.78)]

    def construct(self):
        head = title_block("Is the window itself arbitrary?")
        src = source_note("Where the lower edge sits. In-window median at four candidates")
        self.play(FadeIn(head, run_time=0.6), FadeIn(src, run_time=0.6),
                  run_time=0.6)                                           # 0.6
        self.wait(0.4)                                                    # 1.0

        l1 = Body("The lower edge is a range, not a point: 588 to 755.",
                  font_size=25, color=INK).move_to([0, 2.35, 0])
        self.play(FadeIn(l1, run_time=0.7), run_time=0.7)                # 1.7
        self.wait(3.3)                                                    # 5.0

        # a deviation axis centered on 7.70; a tight scale makes flatness the point
        AXL, AXR, AXY = -3.4, 3.4, -0.15
        base = Line([AXL, AXY, 0], [AXR, AXY, 0], stroke_width=2.4, color=TEAL)
        base_lab = Body("median 7.70", font_size=22, color=TEAL_TXT
                        ).move_to([4.45, AXY, 0])
        gtop = DashedLine([AXL, AXY + 1.0, 0], [AXR, AXY + 1.0, 0],
                          stroke_width=1.2, color=GRIDGRAY, dash_length=0.08)
        gtop_l = Body("+0.5", font_size=20, color=SRCGRAY).next_to(gtop, LEFT, buff=0.16)
        gbot = DashedLine([AXL, AXY - 1.0, 0], [AXR, AXY - 1.0, 0],
                          stroke_width=1.2, color=GRIDGRAY, dash_length=0.08)
        gbot_l = Body("-0.5", font_size=20, color=SRCGRAY).next_to(gbot, LEFT, buff=0.16)
        self.play(FadeOut(l1, run_time=0.4), Create(base, run_time=0.7),
                  FadeIn(base_lab, run_time=0.6), run_time=0.7)           # 5.7
        self.play(FadeIn(VGroup(gtop, gtop_l, gbot, gbot_l), run_time=0.5),
                  run_time=0.5)                                           # 6.2
        self.wait(1.8)                                                    # 8.0

        l2 = Body("Recompute the median at four candidate edges.",
                  font_size=25, color=INK).move_to([0, 2.35, 0])
        self.play(FadeIn(l2, run_time=0.7), run_time=0.7)                # 8.7
        self.wait(2.3)                                                    # 11.0

        xs = [-2.5, -0.85, 0.85, 2.5]
        dots = VGroup(); labs = VGroup()
        for (fl, med), x in zip(self.FLOORS, xs):
            dev = med - 7.70
            y = AXY + dev * 2.0
            dot = Dot(radius=0.09, color=TEAL_DK).set_fill(TEAL_DK, 1.0).move_to([x, y, 0])
            fl_l = Body(f"edge {fl}", font_size=20, color=INK).move_to([x, AXY - 1.45, 0])
            dv_l = Body(f"+{dev:.2f}", font_size=21, color=TEAL_TXT
                        ).move_to([x, y + 0.32, 0])
            dots.add(dot); labs.add(VGroup(fl_l, dv_l))
        for i in range(4):
            self.play(FadeIn(dots[i], run_time=0.4), FadeIn(labs[i], run_time=0.4),
                      run_time=0.5)                                       # 13.0
        self.wait(2.0)                                                    # 15.0

        read = Body("The four medians deviate by at most eight hundredths.",
                    font_size=25, color=INK).move_to([0, 2.35, 0])
        self.play(FadeOut(l2, run_time=0.4), FadeIn(read, run_time=0.7),
                  run_time=0.7)                                           # 15.7
        self.wait(3.3)                                                    # 19.0

        verdict = Body("The headline does not depend on where that edge sits.",
                       font_size=27, color=TEAL_TXT).move_to([0, 1.55, 0])
        self.play(FadeIn(verdict, run_time=0.8), run_time=0.8)           # 19.8
        self.wait(4.2)                                                    # 24.0

        restate = Body("7.70 stands, across the whole range.", font_size=25, color=INK
                       ).move_to([0, -2.10, 0])
        self.play(FadeIn(restate, run_time=0.7), run_time=0.7)           # 24.7
        # 2026-09-18: was 3.3 s. This act was the least silent in the clip at
        # 9.4% and left no room to say the sensitivity result plainly instead of
        # reciting four near-identical numbers.
        self.wait(5.3)                                                    # 30.0


class C3Act7(Scene):
    def construct(self):
        head = title_block("Whose measurement this is")
        src = source_note("Funded units joined to Gate 1. Counts and medians measured")
        axis = axis_line()
        strip = unit_strip(states="class")
        band = window_band()
        band.set_z_index(-1)
        self.add(head, src, axis, band, strip)
        self.wait(0.6)                                                    # 0.6

        # zones: prose in the top band (y >= 1.6), the median readout in the
        # gap between the strip and the axis (y in -0.75 to -1.35). Nothing
        # written in the axis-label rows below -1.55.
        l1 = Body("Forty-seven units carry the measurement.", font_size=26,
                  color=TEAL_TXT).move_to([0, 2.55, 0])
        self.play(FadeIn(l1, run_time=0.6),
                  *[d.animate.set_opacity(0.28) for d in strip if d.unit_c != "i"],
                  run_time=0.8)                                           # 1.4
        self.wait(2.6)                                                    # 4.0

        rings = VGroup()
        for d in strip:
            if d.unit_c == "i" and d.unit_f:
                rings.add(Circle(radius=0.12, color=TEAL_DK, stroke_width=2.6
                                 ).move_to(d.get_center()))
        l2 = Body("Thirty-four of them contain isolates this project sequenced.",
                  font_size=25, color=INK).move_to([0, 1.86, 0])
        self.play(FadeOut(l1, run_time=0.4), FadeIn(l2, run_time=0.6),
                  run_time=0.6)                                           # 4.6
        self.play(LaggedStartMap(Create, rings, lag_ratio=0.05, run_time=1.4),
                  run_time=1.4)                                           # 6.0
        self.wait(3.0)                                                    # 9.0

        l3 = Body("Without them, ten of those thirty-four would hold fewer than "
                  "seven genomes.", font_size=24, color=INK).move_to([0, 2.55, 0])
        self.play(FadeOut(l2, run_time=0.4), FadeIn(l3, run_time=0.7),
                  run_time=0.7)                                           # 9.7
        self.wait(3.3)                                                    # 13.0

        l4 = Body("Those ten would not exist as measurements at all.",
                  font_size=24, color=RUST).move_to([0, 1.90, 0])
        self.play(FadeIn(l4, run_time=0.7), run_time=0.7)                # 13.7
        self.wait(3.3)                                                    # 17.0

        # the two medians, in the gap above the axis
        self.play(FadeOut(VGroup(l3, l4), run_time=0.5), run_time=0.5)   # 17.5
        # MOVED 2026-09-18 from y -0.92. The comment above said the gap above
        # the axis starts at -0.75; it starts at -0.85, where the band ends, so
        # "all in-window 7.70" was cut by the band's lower edge.
        fA = Body("the 34 funded units", font_size=22, color=TEAL_DK
                  ).move_to([-3.55, ROW_BELOW, 0])
        fV = Body("7.74", font_size=28, color=TEAL_DK, font=FONT_TITLE
                  ).next_to(fA, RIGHT, buff=0.26)
        aA = Body("all 47 in-window units", font_size=22, color=TEAL_TXT
                  ).move_to([1.75, ROW_BELOW, 0])
        aV = Body("7.70", font_size=28, color=TEAL_TXT, font=FONT_TITLE
                  ).next_to(aA, RIGHT, buff=0.26)
        self.play(FadeIn(VGroup(fA, fV), run_time=0.7), run_time=0.7)    # 18.2
        self.wait(1.8)                                                   # 20.0
        self.play(FadeIn(VGroup(aA, aV), run_time=0.7), run_time=0.7)    # 20.7
        self.wait(3.3)                                                   # 24.0

        # REWORDED 2026-09-18. "Load-bearing and representative" is a phrase
        # from the grant, not a sentence anyone hears once and understands.
        point = Body("Ten units depend on them. The number does not.",
                     font_size=26, color=TEAL_TXT).move_to([0, 2.55, 0])
        self.play(FadeIn(point, run_time=0.8), run_time=0.8)             # 24.8
        self.wait(4.2)                                                   # 29.0

        nxt = Body("Clip four asks what this ruler can place, and what it cannot.",
                   font_size=24, color=INK).move_to([0, 1.90, 0])
        self.play(FadeIn(nxt, run_time=0.8), run_time=0.8)               # 29.8
        # 2026-09-18: the closing line was rewritten longer, and the film ends
        # here, so the last words need somewhere to land.
        self.wait(8.7)                                                   # 38.5
