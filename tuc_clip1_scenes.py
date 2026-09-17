# ============================================================================
#  ADOPTED 2026-09-17 from Animo render 340a15a4, which supersedes the version
#  previously committed here. That version re-paced acts 3 to 5 and fixed the
#  act 4 overprint; this one does both (carried from run 88f4dbee) and also
#  fixes five defects it missed, including an overprint in act 2's opening line
#  and a real bug in the Txt() helper, whose wrap detector compared only height.
#  A wrap that reflows into the same line box holds height constant (0.9998)
#  while width collapses to 78%, so Txt() now guards on width as well. That
#  guard is worth porting to aphl_common.py. See SALVAGE_TUC_CLIP1_2026-09-17.md.
#  The prior version is in git history at b2468bb.
# ============================================================================

from manim import *
import numpy as np

# ============================================================================
#  TUC BRIEFING SERIES - CLIP 1: "From one province to a global question"
#
#  Built to tuc_briefing/01_concept/BRIEF-01-from-one-province-to-a-global-question.md
#  Seven acts, one render each, concatenated. All new visuals, no reuse.
#
#  THIS CLIP SETS THE VISUAL SYSTEM FOR THE SERIES. Colors, type, the mark for a
#  genome, the mark for a unit, the schematic-versus-measured treatment and the
#  persistent identity of each genome count are established here and reused
#  unchanged in clips 2 to 4.
#
#  The design system is the APHL house system (FILM_SHARING_ARCHITECTURE section 1:
#  one design system, two vintages). Tokens and helpers below are aphl_common.py
#  verbatim, plus the series additions marked SERIES ADDITION.
#
#  Every on-screen figure verified against source before drawing:
#    312 / 259 patient / 53 environment ....... closeout slide 8, and reproduced
#        from FINAL_PANEL.tsv sample_id prefixes IP and IE
#    326 sequenced, 13 B. thailandensis, IP-0198 excluded ... closeout slide 8
#    219 of 312 no predicted determinant (70%) ............. closeout slide 12
#    ceftazidime 253 S of 258, trimethoprim 253 S of 258 ... closeout slide 10
#    11 non-susceptible, no concordant determinant ......... closeout slide 13
#    gyrA T83I in 2 isolates ............................... closeout slide 11
#    Kawang 2,773 genomes / 35 countries / Thailand 1,754 .. closeout slides 25, 26
#    ours 2,976 panel / 50 countries / 2,340 in 85 units ... TABLES.md Table 1
#    Thailand 1,753 in ours ................................ NUMBERS.tsv
#    276 of 312 enter, landing in 56 of 85 units ........... FINAL_PANEL joined
#        FINAL_PARTITION, recomputed 2026-09-17: 276, 56 units, 36 outside
#    42 environmental analysed, 34 share a unit with a patient isolate,
#        20 mixed units, 16 of them in-window ............. as above, joined to
#        GATE1_ALIGNMENT_2026-08-21.tsv
# ============================================================================

config.background_color = "#FFFFFF"     # never dark theme

# --- palette, by MEANING, never decorative -----------------------------------
TEAL      = "#00A0AF"   # genomic / sequence / the measured signal (fills/marks)
TEAL_TXT  = "#006E79"   # text-safe teal (any teal carrying a glyph)
TEAL_DK   = "#005057"   # deepest teal. SERIES: the funded isolates
TEAL_LT   = "#A3CCCC"   # light teal ramp. SERIES: public / background genomes
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

SUB_TOP = -3.0          # reserved bottom eighth carries captions


def Txt(s, font_size=DEFAULT_FONT_SIZE, **kw):
    """House crisp-text helper, with the wrap guard corrected.

    The spec's height-only wrap test misses one real failure mode, which this
    build hit in act 2: when Pango wraps a trailing word at large K it can place
    the wrapped fragment in the SAME line box as the following explicit newline,
    so the layout OVERPRINTS itself while its height is unchanged (measured:
    ratio 0.9998, height test passes) and only its width collapses (8.36 -> 6.52
    scene units, 78% of the K=1 layout). Width is therefore the reliable wrap
    detector, so a candidate K must keep both its height AND its width.
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
    n.to_edge(RIGHT, buff=0.5).set_y(SUB_TOP + 0.28)
    return n


def schematic_tag(s="Schematic, illustrative"):
    return Txt(s, font_size=18, font=FONT_BODY, color=SRCGRAY, slant=ITALIC)


def case_mark(radius=0.14, ring_gap=0.10):
    dot  = Dot(radius=radius, color=TEAL).set_fill(TEAL, 1.0).set_stroke(width=0)
    ring = Circle(radius=radius + ring_gap, color=TEAL_DK, stroke_width=3.0)
    g = VGroup(dot, ring)
    g.dot, g.ring = dot, ring
    return g


def small_dot(radius=0.055, color=TEAL, opacity=1.0):
    return Dot(radius=radius, color=color).set_fill(color, opacity).set_stroke(width=0)


# ---------------------------- SERIES ADDITIONS -------------------------------
# The marks the whole series inherits. Defined once here, reused in clips 2 to 4.

def funded_dot(kind="patient", r=0.070):
    """The continuity object: one of the 312 funded isolates.
    Patient and environment are one hue separated by fill against outline, which
    stays grayscale-safe and keeps both inside the genomic channel."""
    if kind == "patient":
        return Dot(radius=r, color=TEAL_DK).set_fill(TEAL_DK, 1.0).set_stroke(width=0)
    return Dot(radius=r, color=TEAL_DK).set_fill(opacity=0.0).set_stroke(TEAL_DK, 1.7)


def public_dot(r=0.05):
    """A genome from the public record, background to the funded set."""
    return Dot(radius=r, color=TEAL_LT).set_fill(TEAL_LT, 1.0).set_stroke(width=0)


def genome_strip(n=9, w=0.17, h=0.36, gap=0.05, color=TEAL):
    """A stylised core genome. Schematic, so it is always tagged as such."""
    rects = VGroup(*[Rectangle(width=w, height=h, stroke_width=0).set_fill(color, 1.0)
                     for _ in range(n)])
    rects.arrange(RIGHT, buff=gap)
    return rects


def unit_box(w=0.30, fill=None, stroke=None):
    """One analysis unit."""
    r = Rectangle(width=w, height=w, stroke_width=0 if stroke is None else 1.8)
    r.set_fill(fill if fill else TEAL_LT, 0.0 if fill is None else 0.95)
    if stroke:
        r.set_stroke(stroke, 1.8)
    return r


def dot_grid(n, cols, maker, buff=0.052):
    g = VGroup(*[maker(i) for i in range(n)])
    g.arrange_in_grid(cols=cols, buff=buff)
    return g


# Persistent identity for every genome count in the series. Four counts appear in
# this clip alone, so each one keeps the same swatch and the same wording wherever
# it is shown again. Any value from the closeout carries its framework on screen.
CHIP = {
    "funded": (TEAL_DK, "filled"),
    "ours":   (TEAL,    "filled"),
    "kawang": (SRCGRAY, "outline"),
}


def count_chip(value, label, kind, value_size=40, label_size=23, framework=None):
    col, style = CHIP[kind]
    sw = Rectangle(width=0.26, height=0.26, stroke_width=0 if style == "filled" else 1.8)
    if style == "filled":
        sw.set_fill(col, 0.95)
    else:
        sw.set_fill(opacity=0.0).set_stroke(col, 1.8)
    num = Txt(value, font_size=value_size, font=FONT_TITLE,
              color=TEAL_TXT if kind == "ours" else col)
    head = VGroup(sw, num).arrange(RIGHT, buff=0.20)
    lab = Body(label, font_size=label_size, color=INK)
    parts = [head, lab]
    if framework:
        parts.append(Body(framework, font_size=20, color=SRCGRAY))
    g = VGroup(*parts).arrange(DOWN, buff=0.13)
    return g


# ============================================================================
#  ACT 1. What this project built            target ~34 s
#  Entry: empty ground.   Exit: 312 marks, one province.
# ============================================================================
class TucC1Act1(Scene):
    def construct(self):
        src = source_note("Closeout deck, Nakhon Phanom, slide 8")
        title = Title("What this project built", font_size=34).to_edge(UP, buff=0.5)
        self.add(title, src)
        self.wait(0.6)                                                   # -> 0.6

        # --- 326 sequenced, reconciled to 312 confirmed ------------------
        seq = count_chip("326", "isolates sequenced", "funded", value_size=38)
        seq.move_to([-3.9, 1.35, 0])
        self.play(FadeIn(seq, shift=UP * 0.15, run_time=0.8))            # -> 1.4
        self.wait(0.8)                                                   # -> 2.2

        drop1 = Body("13 were B. thailandensis", font_size=21, color=SRCGRAY)
        drop2 = Body("one was not B. pseudomallei", font_size=21, color=SRCGRAY)
        drops = VGroup(drop1, drop2).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        drops.move_to([-0.35, 1.35, 0])
        arrow = Arrow([-2.75, 1.35, 0], [-1.85, 1.35, 0], buff=0, stroke_width=3,
                      color=INK, max_tip_length_to_length_ratio=0.28)
        self.play(GrowArrow(arrow, run_time=0.5), FadeIn(drops, run_time=0.6))  # -> 2.8
        self.wait(1.2)                                                   # -> 4.0

        conf = count_chip("312", "confirmed B. pseudomallei", "funded", value_size=40)
        conf.move_to([3.3, 1.35, 0])
        arrow2 = Arrow([1.75, 1.35, 0], [2.45, 1.35, 0], buff=0, stroke_width=3,
                       color=INK, max_tip_length_to_length_ratio=0.28)
        self.play(GrowArrow(arrow2, run_time=0.5),
                  FadeIn(conf, shift=RIGHT * 0.2, run_time=0.7))         # -> 4.5
        self.wait(1.5)                                                   # -> 6.0

        # --- the 312 as marks: 259 patient, 53 environment ----------------
        self.play(FadeOut(VGroup(seq, drops, arrow, arrow2), run_time=0.6),
                  conf.animate.move_to([-4.35, 1.88, 0]),
                  run_time=0.6)                                          # -> 6.6

        marks = dot_grid(312, 26,
                         lambda i: funded_dot("patient" if i < 259 else "environment"))
        marks.move_to([0, -0.34, 0])
        self.play(LaggedStartMap(FadeIn, marks, lag_ratio=0.0016, run_time=1.8))  # -> 8.4

        kp = VGroup(funded_dot("patient"),
                    Body("259 from patients", font_size=23, color=INK)
                    ).arrange(RIGHT, buff=0.22)
        ke = VGroup(funded_dot("environment"),
                    Body("53 from the environment", font_size=23, color=INK)
                    ).arrange(RIGHT, buff=0.22)
        keys = VGroup(kp, ke).arrange(RIGHT, buff=0.9).move_to([0, -1.86, 0])
        self.play(FadeIn(keys, run_time=0.7))                            # -> 9.1
        self.wait(1.7)                                                   # -> 10.8

        # --- the three findings that matter for what follows --------------
        # The marks step aside rather than shrinking. Scaling a text-bearing
        # group drops its glyphs under the legibility floor.
        self.play(FadeOut(VGroup(marks, keys, conf), run_time=0.7))      # -> 11.5

        f1 = Body("The local population is extraordinarily diverse,\nwith no dominant clone.",
                  font_size=23, color=INK, line_spacing=0.8)
        f2 = Body("Clinical and environmental isolates are drawn\nfrom one population.",
                  font_size=23, color=INK, line_spacing=0.8)
        f3 = Body("Sharing a sequence type is not enough to claim a link,\n"
                  "so attribution needs core-genome distance.",
                  font_size=23, color=TEAL_TXT, line_spacing=0.8)
        fs = VGroup(f1, f2, f3).arrange(DOWN, buff=0.44, aligned_edge=LEFT)
        fs.move_to([0, 0.05, 0])
        for i, f in enumerate(fs):
            self.play(FadeIn(f, shift=UP * 0.12, run_time=0.7))          # -> 12.2 / 14.6 / 17.0
            self.wait(1.7 if i < 2 else 0.9)

        rule = Line(fs[2].get_corner(DL) + [0, -0.16, 0],
                    fs[2].get_corner(DR) + [0, -0.16, 0],
                    stroke_width=2.5, color=TEAL)
        hinge = Body("That third finding is the question this series answers.",
                     font_size=22, color=TEAL_TXT).next_to(rule, DOWN, buff=0.24
                     ).align_to(fs, LEFT)
        self.play(Create(rule, run_time=0.6))                            # -> 18.5
        self.play(FadeIn(hinge, run_time=0.7))                           # -> 19.2
        self.wait(2.2)                                                   # -> 21.4

        self.play(FadeOut(VGroup(fs, rule, hinge), run_time=0.8))        # -> 22.2
        conf.move_to([0, 1.88, 0])
        self.play(FadeIn(marks, run_time=0.8), FadeIn(keys, run_time=0.8),
                  FadeIn(conf, run_time=0.8), run_time=0.8)              # -> 23.0
        prov = Body("One province. Nakhon Phanom.", font_size=24, color=INK
                    ).move_to([0, 1.12, 0])
        self.play(FadeIn(prov, run_time=0.7))                            # -> 23.7
        self.wait(10.1)                                                  # -> 34.0


# ============================================================================
#  ACT 2. Resistance, asked and closed        target ~51 s
#  Entry: 312 marks.   Exit: the resistance question visibly set aside.
# ============================================================================
class TucC1Act2(Scene):
    def construct(self):
        src = source_note("Closeout deck, slides 10 to 13")
        title = Title("Resistance, asked and closed", font_size=34).to_edge(UP, buff=0.5)
        self.add(title, src)

        marks = dot_grid(312, 26,
                         lambda i: funded_dot("patient" if i < 259 else "environment"))
        marks.move_to([0, -0.15, 0])
        conf = count_chip("312", "confirmed B. pseudomallei", "funded", value_size=40)
        conf.move_to([0, 1.72, 0])
        self.add(marks, conf)
        self.wait(0.6)                                                   # -> 0.6

        lead = Body("Emerging resistance was one of the things this sequencing\n"
                    "was meant to detect.", font_size=24, color=INK, line_spacing=0.8
                    ).move_to([0, 1.72, 0])
        self.play(FadeOut(conf, run_time=0.4), FadeIn(lead, run_time=0.7))  # -> 1.3
        self.wait(1.6)                                                   # -> 2.9

        # --- beat 1: no acquired resistance genes -------------------------
        self.play(FadeOut(lead, run_time=0.5),
                  marks.animate.scale(0.58).move_to([-4.6, 1.15, 0]), run_time=0.7)  # -> 3.6
        b1 = Body("No acquired resistance genes were detected.",
                  font_size=27, color=TEAL_TXT).move_to([0.55, 1.75, 0])
        b1s = Body("The determinants present are intrinsic to the species.\n"
                   "That is the baseline for the province, not a guarantee.",
                   font_size=23, color=INK, line_spacing=0.8
                   ).next_to(b1, DOWN, buff=0.26).align_to(b1, LEFT)
        self.play(FadeIn(b1, run_time=0.7))                              # -> 4.3
        self.wait(1.0)                                                   # -> 5.3
        self.play(FadeIn(b1s, run_time=0.7))                             # -> 6.0
        self.wait(2.6)                                                   # -> 8.6

        # --- beat 2: 219 of 312 carry no predicted determinant ------------
        BX, BY, BW, BH = -3.15, -0.55, 6.4, 0.62
        frac = 219.0 / 312.0
        seg_a = Rectangle(width=BW * frac, height=BH, stroke_width=0).set_fill(TEAL, 0.92)
        seg_b = Rectangle(width=BW * (1 - frac), height=BH, stroke_width=0
                          ).set_fill(GRIDGRAY, 1.0)
        bar = VGroup(seg_a, seg_b).arrange(RIGHT, buff=0).move_to([BX + BW / 2, BY, 0])
        bar_o = Rectangle(width=BW, height=BH, stroke_width=1.4, color=SRCGRAY
                          ).move_to(bar.get_center())
        lab_a = Body("219 of 312 carry no predicted determinant at all",
                     font_size=23, color="#FFFFFF").move_to(seg_a.get_center())
        pct = Body("seventy percent", font_size=24, color=TEAL_TXT
                   ).next_to(bar, DOWN, buff=0.24).align_to(bar, LEFT)
        self.play(FadeOut(VGroup(b1, b1s), run_time=0.5))                # -> 9.1
        self.play(Create(bar_o, run_time=0.5), FadeIn(bar, run_time=0.6))  # -> 9.7
        self.play(FadeIn(lab_a, run_time=0.5), FadeIn(pct, run_time=0.5))  # -> 10.2
        self.wait(2.8)                                                   # -> 13.0

        # --- beat 3: first-line therapy unaffected ------------------------
        self.play(FadeOut(VGroup(bar, bar_o, lab_a, pct), run_time=0.6))  # -> 13.6
        ft = Body("First-line therapy is unaffected.", font_size=27, color=TEAL_TXT
                  ).move_to([0.55, 1.75, 0])
        rows = VGroup()
        for name in ("ceftazidime", "trimethoprim"):
            n = Body(name, font_size=22, color=INK)
            v = Body("253 susceptible of 258 tested", font_size=22, color=TEAL_TXT)
            rows.add(VGroup(n, v).arrange(RIGHT, buff=0.55, aligned_edge=DOWN))
        rows.arrange(DOWN, buff=0.34, aligned_edge=LEFT).move_to([0.2, 0.55, 0])
        den = Body("patient isolates only", font_size=22, color=SRCGRAY
                   ).next_to(rows, DOWN, buff=0.3).align_to(rows, LEFT)
        self.play(FadeIn(ft, run_time=0.6))                              # -> 14.2
        self.play(LaggedStartMap(FadeIn, rows, lag_ratio=0.35, run_time=1.0))  # -> 15.2
        self.play(FadeIn(den, run_time=0.5))                             # -> 15.7
        self.wait(3.0)                                                   # -> 18.7

        # --- the honest loose end, stated as a plan -----------------------
        self.play(FadeOut(VGroup(ft, rows, den), run_time=0.6))          # -> 19.3
        le = Body("One loose end, and it is already scheduled.",
                  font_size=26, color=INK).move_to([0.55, 1.78, 0])
        self.play(FadeIn(le, run_time=0.7))                              # -> 20.0
        self.wait(1.2)                                                   # -> 21.2

        eleven = dot_grid(11, 11, lambda i: funded_dot("patient", r=0.085), buff=0.14)
        eleven.move_to([-1.6, 0.62, 0])
        el_l = Body("11 isolates were non-susceptible on the laboratory panel\n"
                    "with no concordant determinant in the genome.",
                    font_size=23, color=INK, line_spacing=0.8
                    ).next_to(eleven, DOWN, buff=0.34).align_to(eleven, LEFT)
        self.play(FadeIn(eleven, run_time=0.6))                          # -> 21.8
        self.play(FadeIn(el_l, run_time=0.7))                            # -> 22.5
        self.wait(2.4)                                                   # -> 24.9

        plan = Body("Repeat testing, with MIC determination, in the next phase.",
                    font_size=24, color=TEAL_TXT).move_to([0, -1.18, 0])
        plan_s = Body("Genomic prediction and laboratory testing are complementary.\n"
                      "The discordance is what triggers the repeat.",
                      font_size=23, color=SRCGRAY, line_spacing=0.8
                      ).next_to(plan, DOWN, buff=0.26)
        self.play(FadeIn(plan, run_time=0.7))                            # -> 25.6
        self.wait(1.0)                                                   # -> 26.6
        self.play(FadeIn(plan_s, run_time=0.7))                          # -> 27.3
        self.wait(2.6)                                                   # -> 29.9

        # --- the one quinolone-associated determinant, one clause ---------
        self.play(FadeOut(VGroup(eleven, el_l, plan, plan_s), run_time=0.6))  # -> 30.5
        gy = Body("Two isolates carry the only quinolone-associated\n"
                  "determinant found.",
                  font_size=23, color=INK, line_spacing=0.8
                  ).move_to([0.3, 0.72, 0])
        gy2 = Body("No fluoroquinolone is on the laboratory panel, so it needs\n"
                   "confirmation rather than reporting.",
                   font_size=23, color=SRCGRAY, line_spacing=0.8
                   ).next_to(gy, DOWN, buff=0.28).align_to(gy, LEFT)
        self.play(FadeIn(gy, run_time=0.7))                              # -> 31.2
        self.play(FadeIn(gy2, run_time=0.7))                             # -> 31.9
        self.wait(2.4)                                                   # -> 34.3

        # --- set the topic aside, explicitly ------------------------------
        self.play(FadeOut(VGroup(le, gy, gy2), run_time=0.6))            # -> 34.9
        bt = Body("Resistance: asked, answered, and set aside.",
                  font_size=26, color=INK)
        bt2 = Body("The province now has a baseline, so a future change is visible against it.",
                   font_size=23, color=SRCGRAY)
        # Size the band to its contents. bt2 measures 9.748u, so the original
        # 8.2u box had its border running straight through the text.
        box = Rectangle(width=max(bt.width, bt2.width) + 0.86, height=1.5,
                        stroke_width=1.8, color=GRAYOUT
                        ).set_fill(GRIDGRAY, 0.45).move_to([0, -0.90, 0])
        bt.move_to(box.get_center() + [0, 0.26, 0])
        bt2.move_to(box.get_center() + [0, -0.32, 0])
        self.play(Create(box, run_time=0.7), FadeIn(bt, run_time=0.6))   # -> 35.6
        self.play(FadeIn(bt2, run_time=0.6))                             # -> 36.2
        self.wait(1.6)                                                   # -> 37.8
        # Dimmed in place. Scaling the group would drop its text under the
        # legibility floor, and the dimming is what reads as "set aside".
        self.play(VGroup(box, bt, bt2).animate.set_opacity(0.38),
                  run_time=0.9)                                          # -> 38.7
        nxt = Body("The rest of this series is about a different question.",
                   font_size=25, color=INK).move_to([0.82, 0.75, 0])
        self.play(FadeIn(nxt, run_time=0.7))                             # -> 39.4
        self.wait(11.6)                                                  # -> 51.0


# ============================================================================
#  ACT 3. Two frameworks, reconciled          target ~40 s
#  Entry: 312 marks.   Exit: both panel sizes on screen, related.
#
#  The brief invited a refusal here: a reconciliation of two numbers risks being
#  the dullest 40 seconds in the series, and it offered "carry it in less time or
#  fold it into act 4". Kept at length but built as one collection drawn twice
#  rather than as a table: a shared Thailand core with two curations around it,
#  so the one-genome difference is the payoff rather than a row.
# ============================================================================
class TucC1Act3(Scene):
    def construct(self):
        src = source_note("Closeout slides 25 and 26, and Table 1")
        title = Title("Two frameworks, one collection", font_size=34).to_edge(UP, buff=0.5)
        self.add(title, src)
        self.wait(0.9)   # 0.5 -> 0.9, tail redistributed

        lead = Body("These genomes have been placed in a global framework twice.",
                    font_size=25, color=INK).move_to([0, 2.15, 0])
        self.play(FadeIn(lead, run_time=0.8))                            # -> 1.3
        self.wait(2.3)   # 1.4 -> 2.3, tail redistributed

        # --- the two frameworks, side by side -----------------------------
        kaw = count_chip("2,773", "genomes, 35 countries", "kawang",
                         value_size=44, framework="closeout framework")
        kaw.move_to([-3.35, 0.72, 0])
        ours = count_chip("2,976", "genomes, 50 countries", "ours",
                          value_size=44, framework="this work's panel")
        ours.move_to([3.35, 0.72, 0])
        self.play(FadeIn(kaw, shift=RIGHT * 0.2, run_time=0.8))          # -> 3.5
        self.wait(2.1)   # 1.2 -> 2.1, tail redistributed
        self.play(FadeIn(ours, shift=LEFT * 0.2, run_time=0.8))          # -> 5.5
        self.wait(3.0)   # 2.0 -> 3.0, tail redistributed

        warn = Body("Same underlying collection, curated twice for different questions.",
                    font_size=24, color=INK).move_to([0, -0.62, 0])
        self.play(FadeIn(warn, run_time=0.8))                            # -> 8.3
        self.wait(3.4)   # 2.4 -> 3.4, tail redistributed

        # --- the evidence: Thailand differs by one genome ------------------
        self.play(FadeOut(warn, run_time=0.5))                           # -> 11.2
        th_l = VGroup(Body("Thailand", font_size=22, color=INK),
                      Body("1,754", font_size=34, color=SRCGRAY, font=FONT_TITLE)
                      ).arrange(DOWN, buff=0.14).move_to([-3.35, -0.85, 0])
        th_r = VGroup(Body("Thailand", font_size=22, color=INK),
                      Body("1,753", font_size=34, color=TEAL_TXT, font=FONT_TITLE)
                      ).arrange(DOWN, buff=0.14).move_to([3.35, -0.85, 0])
        self.play(FadeIn(th_l, run_time=0.6), FadeIn(th_r, run_time=0.6))  # -> 11.8
        self.wait(2.5)   # 1.6 -> 2.5, tail redistributed
        span = Line([-2.25, -0.85, 0], [2.25, -0.85, 0], stroke_width=2, color=INK)
        one = Body("one genome apart", font_size=23, color=TEAL_TXT
                   ).move_to([0, -0.5, 0])
        self.play(Create(span, run_time=0.7))                            # -> 14.1
        self.play(FadeIn(one, run_time=0.6))                             # -> 14.7
        self.wait(3.2)   # 2.2 -> 3.2, tail redistributed

        ev = Body("That is the evidence they are one collection\nrather than two datasets.",
                  font_size=23, color=INK, line_spacing=0.8).move_to([0, -1.85, 0])
        self.play(FadeIn(ev, run_time=0.7))                              # -> 17.6
        self.wait(3.6)   # 2.6 -> 3.6, tail redistributed

        # --- what enters analysis, and why it is fewer --------------------
        self.play(FadeOut(VGroup(th_l, th_r, span, one, ev, kaw, lead), run_time=0.7),
                  ours.animate.move_to([-3.4, 1.15, 0]))                 # -> 20.9
        arrow = Arrow([-1.55, 1.15, 0], [-0.35, 1.15, 0], buff=0, stroke_width=3,
                      color=INK, max_tip_length_to_length_ratio=0.22)
        an = count_chip("2,340", "genomes enter analysis", "ours", value_size=44)
        an.move_to([2.15, 1.15, 0])
        self.play(GrowArrow(arrow, run_time=0.5),
                  FadeIn(an, shift=RIGHT * 0.2, run_time=0.7))           # -> 21.6
        self.wait(2.4)   # 1.4 -> 2.4, tail redistributed

        why = Body("A unit needs a minimum size before it can be measured at all,\n"
                   "so genomes without enough near relatives are assigned but not analysed.",
                   font_size=22, color=INK, line_spacing=0.8).move_to([0, -0.35, 0])
        self.play(FadeIn(why, run_time=0.8))                             # -> 23.8
        self.wait(3.6)   # 2.4 -> 3.6, tail redistributed

        units = count_chip("85", "analysis units", "ours", value_size=44)
        units.move_to([0, -1.75, 0])
        self.play(FadeIn(units, run_time=0.7))                           # -> 26.9
        self.wait(3.5)   # 12.8 -> 3.5, tail redistributed


# ============================================================================
#  ACT 4. Where the 312 went                  target ~54 s   THE CENTRAL ACT
#  Entry: both panels.   Exit: 312 marks distributed across 56 units.
#
#  Guard from the brief: do NOT put "two thirds" on screen. Clip 4 uses that
#  phrase for a different quantity. Say fifty six of eighty five.
# ============================================================================
class TucC1Act4(Scene):
    def construct(self):
        src = source_note("Frozen basis, 2,340 genomes in 85 units")
        title = Title("Where the 312 went", font_size=34).to_edge(UP, buff=0.5)
        self.add(title, src)

        # --- the partition that already exists ----------------------------
        rng = np.random.default_rng(4)
        HIT = sorted(rng.choice(85, size=56, replace=False).tolist())
        units = VGroup(*[unit_box(0.34, fill=TEAL_LT) for _ in range(85)])
        units.arrange_in_grid(rows=5, cols=17, buff=0.115).move_to([0, 0.15, 0])
        self.add(units)
        cap = Body("2,340 genomes, already sorted into 85 analysis units",
                   font_size=23, color=INK).move_to([0, 2.0, 0])
        self.add(cap)
        self.wait(2.0)   # 0.8 -> 2.0, tail redistributed

        drop = Body("Now drop the 312 into it.", font_size=26, color=INK
                    ).move_to([0, -1.85, 0])
        self.play(FadeIn(drop, run_time=0.7))                            # -> 1.5
        self.wait(3.1)   # 1.3 -> 3.1, tail redistributed

        # --- the funded isolates disperse through the structure -----------
        src_pt = np.array([-5.6, -1.85, 0])
        flyers = VGroup(*[funded_dot("patient" if i % 6 else "environment", r=0.05)
                          for i in range(56)])
        for f in flyers:
            f.move_to(src_pt)
        self.add(flyers)
        prov = Body("one province", font_size=20, color=TEAL_DK).move_to([-5.6, -2.3, 0])
        self.play(FadeIn(prov, run_time=0.5))                            # -> 3.3

        anims = []
        for k, ui in enumerate(HIT):
            anims.append(flyers[k].animate.move_to(units[ui].get_center()))
        self.play(LaggedStart(*anims, lag_ratio=0.028, run_time=3.4))    # -> 6.7
        self.play(*[units[ui].animate.set_fill(TEAL_DK, 0.92) for ui in HIT],
                  FadeOut(flyers, run_time=0.4), run_time=0.8)           # -> 7.5
        self.wait(3.1)   # 1.2 -> 3.1, tail redistributed

        n276 = count_chip("276", "of the 312 enter the analysed set", "funded",
                          value_size=40)
        n276.move_to([-3.75, -2.0, 0])
        n56 = count_chip("56 of 85", "units hold at least one of them", "funded",
                         value_size=40)
        n56.move_to([3.6, -2.0, 0])
        self.play(FadeOut(drop, run_time=0.4), FadeOut(prov, run_time=0.4),
                  FadeIn(n276, run_time=0.7))                            # -> 9.4
        self.wait(3.5)   # 1.6 -> 3.5, tail redistributed
        self.play(FadeIn(n56, run_time=0.7))                             # -> 11.7
        self.wait(4.1)   # 2.2 -> 4.1, tail redistributed

        notc = Body("Not a cluster. Not a corner.", font_size=26, color=TEAL_TXT
                    ).move_to([0, -1.25, 0])
        self.play(FadeIn(notc, run_time=0.7))                            # -> 14.6
        self.wait(4.6)   # 2.6 -> 4.6, tail redistributed

        spread = Body("A provincial collection reaching across the structure\n"
                      "of a global panel is what makes it able to answer\n"
                      "questions no single province could.",
                      font_size=23, color=INK, line_spacing=0.85).move_to([0, -1.55, 0])
        self.play(FadeOut(VGroup(notc, n276, n56), run_time=0.5))        # -> 17.7
        self.play(FadeIn(spread, run_time=0.8))                          # -> 18.5
        self.wait(5.4)   # 3.4 -> 5.4, tail redistributed

        # --- the 36 that did not enter, stated plainly --------------------
        self.play(FadeOut(spread, run_time=0.6),
                  units.animate.scale(0.86).move_to([0.85, 0.5, 0]),
                  cap.animate.set_opacity(0.0), run_time=0.8)            # -> 22.7

        th = VGroup(*[funded_dot("patient" if i % 6 else "environment", r=0.062)
                      for i in range(36)])
        th.arrange_in_grid(cols=6, buff=0.12).move_to([-4.55, 0.5, 0])
        th_l = Body("36 did not enter", font_size=23, color=INK
                    ).next_to(th, DOWN, buff=0.3)
        self.play(FadeIn(th, run_time=0.7), FadeIn(th_l, run_time=0.6))  # -> 23.4
        self.wait(3.7)   # 1.8 -> 3.7, tail redistributed

        # p2 flowed to about y = -2.55 while p3 was placed absolutely at -2.42,
        # so the two overprinted for the whole closing hold. All three are now
        # chained off p1, which cannot collide however the text reflows.
        p1 = Body("Every one of them has a nearest unit recorded.",
                  font_size=24, color=TEAL_TXT).move_to([0.6, -0.85, 0])
        p2 = Body("Their lineages are too rare in the global panel for a\n"
                  "measurable unit to form around them.",
                  font_size=22, color=INK, line_spacing=0.8
                  ).next_to(p1, DOWN, buff=0.28)
        self.play(FadeIn(p1, run_time=0.7))                              # -> 25.9
        self.wait(3.6)   # 1.6 -> 3.6, tail redistributed
        self.play(FadeIn(p2, run_time=0.7))                              # -> 28.2
        self.wait(4.8)   # 2.4 -> 4.8, tail redistributed

        p3 = Body("That is a finding about the panel, not a defect in the isolates.",
                  font_size=23, color=INK).next_to(p2, DOWN, buff=0.28)
        self.play(FadeIn(p3, run_time=0.7))                              # -> 31.3
        self.wait(3.72)   # 22.7 -> 3.72, tail redistributed (+1 frame, quantisation)


# ============================================================================
#  ACT 5. Patient and environment, at a second scale     target ~51 s
#  Entry: 312 across 56 units.   Exit: the mixed units marked.
# ============================================================================
class TucC1Act5(Scene):
    def construct(self):
        src = source_note("Frozen basis, joined per unit")
        title = Title("The same answer, a second time", font_size=34).to_edge(UP, buff=0.5)
        self.add(title, src)
        self.wait(2.0)   # 0.6 -> 2.0, tail redistributed

        recap = Body("The closeout found environmental isolates scattered among\n"
                     "patient isolates, with no separate environmental lineage.",
                     font_size=24, color=INK, line_spacing=0.8).move_to([0, 1.65, 0])
        recap_s = Body("That was one tree, of these 312 genomes.", font_size=22,
                       color=SRCGRAY).next_to(recap, DOWN, buff=0.3)
        self.play(FadeIn(recap, run_time=0.8))                           # -> 1.4
        self.wait(3.7)   # 1.6 -> 3.7, tail redistributed
        self.play(FadeIn(recap_s, run_time=0.6))                         # -> 3.6
        self.wait(4.1)   # 2.0 -> 4.1, tail redistributed

        test = Body("Test it again in a structure built independently,\n"
                    "which knew nothing about which isolate came from where.",
                    font_size=24, color=TEAL_TXT, line_spacing=0.8).move_to([0, 0.05, 0])
        self.play(FadeIn(test, run_time=0.8))                            # -> 6.4
        self.wait(4.8)   # 2.6 -> 4.8, tail redistributed

        # --- the 85 units, with the mixed ones marked ---------------------
        self.play(FadeOut(VGroup(recap, recap_s, test), run_time=0.7))   # -> 9.7
        rng = np.random.default_rng(11)
        MIXED = sorted(rng.choice(85, size=20, replace=False).tolist())
        INWIN = set(MIXED[:16])
        units = VGroup(*[unit_box(0.34, fill=TEAL_LT) for _ in range(85)])
        units.arrange_in_grid(rows=5, cols=17, buff=0.115).move_to([0, 0.75, 0])
        self.play(LaggedStartMap(FadeIn, units, lag_ratio=0.006, run_time=1.2))  # -> 10.9
        ul = Body("85 analysis units, built from 2,340 genomes",
                  font_size=22, color=INK).next_to(units, UP, buff=0.34)
        self.play(FadeIn(ul, run_time=0.6))                              # -> 11.5
        self.wait(3.5)   # 1.4 -> 3.5, tail redistributed

        self.play(*[units[i].animate.set_fill(TEAL_DK, 0.92) for i in MIXED],
                  run_time=1.0)                                          # -> 13.9
        ml = Body("20 units hold both a patient isolate and an environmental one",
                  font_size=23, color=TEAL_TXT).next_to(units, DOWN, buff=0.42)
        self.play(FadeIn(ml, run_time=0.7))                              # -> 14.6
        self.wait(4.3)   # 2.2 -> 4.3, tail redistributed

        # --- the headline share --------------------------------------------
        BX, BY, BW, BH = -3.2, -0.95, 6.4, 0.6
        frac = 34.0 / 42.0
        sa = Rectangle(width=BW * frac, height=BH, stroke_width=0).set_fill(TEAL_DK, 0.92)
        sb = Rectangle(width=BW * (1 - frac), height=BH, stroke_width=0
                       ).set_fill(GRIDGRAY, 1.0)
        bar = VGroup(sa, sb).arrange(RIGHT, buff=0).move_to([BX + BW / 2, BY, 0])
        bo = Rectangle(width=BW, height=BH, stroke_width=1.4, color=SRCGRAY
                       ).move_to(bar.get_center())
        bl = Body("34 of 42", font_size=24, color="#FFFFFF").move_to(sa.get_center())
        bt = Body("environmental isolates in the analysed set sit in a unit\n"
                  "that also holds a patient isolate",
                  font_size=23, color=INK, line_spacing=0.8
                  ).next_to(bar, DOWN, buff=0.24)
        self.play(FadeOut(ml, run_time=0.5))                             # -> 17.3
        self.play(Create(bo, run_time=0.5), FadeIn(bar, run_time=0.6),
                  FadeIn(bl, run_time=0.5))                              # -> 17.9
        self.play(FadeIn(bt, run_time=0.7))                              # -> 18.6
        self.wait(5.2)   # 3.0 -> 5.2, tail redistributed

        iw = Body("16 of the 20 mixed units sit inside the measurable range.",
                  font_size=23, color=SRCGRAY).move_to([0, -2.35, 0])
        self.play(FadeIn(iw, run_time=0.6))                              # -> 22.2
        self.wait(4.7)   # 2.4 -> 4.7, tail redistributed

        # --- the conclusion ------------------------------------------------
        self.play(FadeOut(VGroup(bar, bo, bl, bt, iw), run_time=0.6))    # -> 25.2
        c1 = Body("The same answer, from a different instrument.",
                  font_size=27, color=TEAL_TXT).move_to([0, -1.55, 0])
        c2 = Body("One local tree of 312 genomes said it. A global partition of\n"
                  "2,340 genomes, which never saw the labels, says it again.",
                  font_size=23, color=INK, line_spacing=0.8
                  ).next_to(c1, DOWN, buff=0.28)
        self.play(FadeIn(c1, run_time=0.7))                              # -> 25.9
        self.wait(3.9)   # 1.4 -> 3.9, tail redistributed
        self.play(FadeIn(c2, run_time=0.8))                              # -> 28.1
        self.wait(3.92)   # 22.9 -> 3.92, tail redistributed (+1 frame, quantisation)


# ============================================================================
#  ACT 6. The question this makes askable     target ~43 s
#  Entry: the mixed units.   Exit: the question on screen, unanswered.
#
#  Guard: do not hint at the answer. No country attribution implied anywhere.
# ============================================================================
class TucC1Act6(Scene):
    """The question this makes askable.   target 43.0 s, ~95 words.
    Entry: the mixed units.   Exit: the question on screen, unanswered.

    Rebuilt with visual steps rather than a stack of text fades: the first pass
    registered one detected moment across 43 s, which is the 7.09 failure in
    miniature. The brief asks for an animated step for every sentence.

    Guards: do not hint at the answer, imply no country attribution, and do not
    name the typing method. The sequence-type demonstration is illustrative, so
    it is tagged."""

    def construct(self):
        src = source_note("Closeout deck, slide 18")
        title = Title("The question this makes askable", font_size=34
                      ).to_edge(UP, buff=0.5)
        self.add(title, src)
        self.wait(0.8)

        # 1. the case arrives
        case = case_mark(radius=0.17).move_to([-5.15, 1.62, 0])
        cl = Body("A patient presents with no travel history.",
                  font_size=25, color=INK).next_to(case, RIGHT, buff=0.42)
        self.play(FadeIn(case.dot, scale=0.5, run_time=0.6),
                  Create(case.ring, run_time=0.6), run_time=0.6)
        self.play(FadeIn(cl, run_time=0.7))
        self.wait(3.0)

        # 2. its genome is the only evidence
        strip = genome_strip(n=11, color=TEAL_DK).move_to([-2.45, 0.62, 0])
        stag = schematic_tag().scale(0.95).move_to([4.35, 0.62, 0])
        self.play(LaggedStartMap(FadeIn, strip, lag_ratio=0.06, run_time=0.9))
        sl = Body("its genome", font_size=22, color=TEAL_TXT
                  ).next_to(strip, DOWN, buff=0.26)
        self.play(FadeIn(sl, run_time=0.6), FadeIn(stag, run_time=0.6), run_time=0.6)
        self.wait(3.0)

        only = Body("The only evidence of where the infection was acquired.",
                    font_size=25, color=INK).move_to([0.55, -0.35, 0])
        self.play(FadeIn(only, run_time=0.8))
        self.wait(4.4)

        # 3. what the closeout already settled
        self.play(FadeOut(VGroup(only, sl, strip, stag, cl), run_time=0.7),
                  case.animate.move_to([-5.15, 2.05, 0]), run_time=0.7)
        settled = Body("The closeout already settled two things about that.",
                       font_size=24, color=SRCGRAY).move_to([0, 1.28, 0])
        self.play(FadeIn(settled, run_time=0.7))
        self.wait(2.6)

        # two isolates carrying the same sequence type
        a = genome_strip(n=8, color=TEAL_DK).move_to([-3.05, 0.28, 0])
        b = genome_strip(n=8, color=TEAL_DK).move_to([3.05, 0.28, 0])
        tag_a = Body("same sequence type", font_size=21, color=PURPLE
                     ).move_to([0, 0.95, 0])
        brace_a = Line(a.get_top() + [0, 0.12, 0], b.get_top() + [0, 0.12, 0],
                       stroke_width=2, color=PURPLE)
        stag2 = schematic_tag().scale(0.95).move_to([4.5, -2.35, 0])
        self.play(LaggedStartMap(FadeIn, a, lag_ratio=0.05, run_time=0.5),
                  LaggedStartMap(FadeIn, b, lag_ratio=0.05, run_time=0.5),
                  FadeIn(stag2, run_time=0.5), run_time=1.0)
        self.play(Create(brace_a, run_time=0.6), FadeIn(tag_a, run_time=0.6),
                  run_time=0.6)
        self.wait(2.6)

        # but far apart across the whole genome
        axis = Line([-4.6, -1.25, 0], [4.6, -1.25, 0], stroke_width=2.5, color=INK)
        axl = Body("distance across the whole genome", font_size=21, color=INK
                   ).next_to(axis, DOWN, buff=0.26)
        ma = small_dot(0.085, TEAL_DK).move_to([-3.05, -1.25, 0])
        mb = small_dot(0.085, TEAL_DK).move_to([3.05, -1.25, 0])
        gap = Line([-2.9, -1.25, 0], [2.9, -1.25, 0], stroke_width=3.5, color=RUST)
        self.play(Create(axis, run_time=0.6), FadeIn(axl, run_time=0.5),
                  FadeIn(ma, run_time=0.4), FadeIn(mb, run_time=0.4),
                  run_time=0.8)
        self.play(Create(gap, run_time=0.8), run_time=0.8)
        p1 = Body("Sharing a sequence type will not answer it.",
                  font_size=24, color=RUST).move_to([0, -2.05, 0])
        self.play(FadeIn(p1, run_time=0.6), run_time=0.6)
        self.wait(3.2)

        p2 = Body("Core-genome distance is what the question needs.",
                  font_size=24, color=TEAL_TXT).move_to([0, -2.62, 0])
        self.play(FadeIn(p2, run_time=0.8))
        self.wait(4.4)

        # 4. the question itself
        self.play(FadeOut(VGroup(settled, a, b, tag_a, brace_a, axis, axl, ma, mb,
                                 gap, p1, p2, stag2), run_time=0.8),
                  case.animate.move_to([0, 1.72, 0]), run_time=0.8)
        q1 = Body("So: with core genomes, in a global frame,", font_size=30,
                  color=INK).move_to([0, 0.42, 0])
        self.play(FadeIn(q1, run_time=0.8))
        self.wait(1.4)
        q2 = Title("how far can you actually get?", font_size=44).move_to([0, -0.5, 0])
        self.play(Write(q2, run_time=1.4))
        self.wait(5.0)


# ============================================================================
#  ACT 7. What the rest of this takes         target 18.0 s, ~40 words
#  Entry: the question.   Exit: three titles, handing off to clip 2.
# ============================================================================
class TucC1Act7(Scene):
    def construct(self):
        title = Title("What the rest of this takes", font_size=34
                      ).to_edge(UP, buff=0.5)
        case = case_mark(radius=0.17).move_to([0, 1.88, 0])
        self.add(title, case)
        self.wait(1.0)

        spine = Line([-5.0, 0.15, 0], [5.0, 0.15, 0], stroke_width=2.5, color=GRIDGRAY)
        self.play(Create(spine, run_time=0.6))

        xs = [-3.35, 0.0, 3.35]
        steps = [("01", "Show that the measuring\ninstrument works."),
                 ("02", "Point it at the data."),
                 ("03", "The answer, and its limit.")]
        for x, (n, t) in zip(xs, steps):
            node = Circle(radius=0.20, color=TEAL, stroke_width=3.0
                          ).set_fill("#FFFFFF", 1.0).move_to([x, 0.15, 0])
            num = Txt(n, font_size=22, font=FONT_TITLE, color=TEAL_TXT
                      ).move_to([x, 0.78, 0])
            lab = Body(t, font_size=23, color=INK, line_spacing=0.8
                       ).move_to([x, -0.78, 0])
            self.play(Create(node, run_time=0.4), FadeIn(num, run_time=0.4),
                      FadeIn(lab, shift=UP * 0.1, run_time=0.6), run_time=0.7)
            self.wait(3.0)

        nxt = Body("Next: a ruler you can trust.", font_size=25, color=TEAL_TXT
                   ).move_to([0, -2.15, 0])
        self.play(FadeIn(nxt, run_time=0.7))
        self.wait(4.6)
