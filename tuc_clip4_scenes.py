from manim import *
import numpy as np

# ============================================================================
#  TUC BRIEFING SERIES - CLIP 4: "How close is close enough?"
#
#  Built to the clip 4 brief. Nine acts. Seven rendered here, two dropped in
#  whole:
#    act 3 = OutbreakThreshold.mp4, the merged revised legacy clip, 44.9 s
#    act 6 = Act4NotSeparable.mp4, house act D, 51.0 s
#
#  THE CLAIM. One property of this organism, its recombination load, sets the
#  resolution limit on every question asked of a genome. It erases the fine
#  scale, where linkage and country live, and leaves the coarse scale, where
#  region lives, intact.
#
#  CONTINUITY OBJECT: the 46 scorable validation genomes, val_mark(). The same
#  46 marks in the same style in every act that follows their introduction, and
#  in act 9 they hand off to the 312 funded isolates.
#
#  EVERY NUMBER REPRODUCED FROM SOURCE BEFORE IT WAS DRAWN, 2026-09-17.
#  Repo: /Users/peerahemarajata/bp-recombination-aware-snps
#    46 scorable of 48 registered, 16 countries .. NUMBERS.tsv validation.*
#    ladder kappas 0.193 / 0.832 / 0.461 /
#        0.909 / 1.000, with accuracy, baseline
#        and estimator per rung ................. NUMBERS.tsv ladder.*
#    abstention 94.3% at 76.1% coverage,
#        out of sample ......................... NUMBERS.tsv abstention.region.
#                                                loo_selective_accuracy
#    country abstention fails, 37.5% equals
#        retained-majority 37.5% ............... NUMBERS.tsv abstention.country.
#                                                VERDICT
#    312 funded, 259 patient, 53 environment ... FINAL_PANEL.tsv IP/IE prefixes
#    276 enter, 56 of 85 units, 36 out ......... FINAL_PANEL join FINAL_PARTITION
#    34 of 47 in-window units .................. joined to GATE1_ALIGNMENT
#    10 in-window units fall below the 7-member
#        floor without their funded isolates ... recomputed. The analysed set's
#                                                smallest unit is 7 members
#    median r/m 7.7394 funded vs 7.6988 all .... GATE1_ALIGNMENT rm_corrected
#
#  CITED, NOT COMPUTED HERE, and labeled with its framework on screen:
#    association index by trait ................ Kawang closeout deck slide 25,
#                                                2,773 genomes, 35 countries
#    nine nominated pairs, six evaluable ....... Kawang closeout deck slide 23
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

FONT_TITLE = "Franklin Gothic Medium"
FONT_BODY  = "Franklin Gothic Book"
DEFAULT_FONT_SIZE = 28
Text.set_default(font=FONT_BODY, color=INK)

SUB_TOP = -3.0          # reserved bottom eighth carries captions
MARGIN  = 0.82          # 110 px at 1080p, so content lives inside +/- 6.29


def Txt(s, font_size=DEFAULT_FONT_SIZE, **kw):
    """House crisp-text helper, with the wrap guard corrected.

    The spec's height-only wrap test misses one real failure mode, found in
    clip 1 act 2: when Pango wraps a trailing word at large K it can place the
    wrapped fragment in the SAME line box as the following explicit newline, so
    the layout OVERPRINTS itself while its height is unchanged (measured height
    ratio 0.9998, which passes the 1.3 test) and only its width collapses
    (8.36 to 6.52 scene units, 78% of the K=1 layout). Width is therefore the
    reliable wrap detector, so a candidate K has to keep both.
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


def Title(s, font_size=34, color=TEAL_TXT, **kw):
    kw.setdefault("font", FONT_TITLE)
    return Txt(s, font_size=font_size, color=color, **kw)


def Body(s, font_size=DEFAULT_FONT_SIZE, color=INK, **kw):
    kw.setdefault("font", FONT_BODY)
    return Txt(s, font_size=font_size, color=color, **kw)


def title_at(s, **kw):
    """Titles own the top left, per the house spec and the act 3 clip."""
    return Title(s, **kw).to_edge(UP, buff=0.5).to_edge(LEFT, buff=MARGIN)


def source_note(s):
    """Source line bottom left, above the reserved caption band."""
    n = Body(s, font_size=20, color=SRCGRAY)
    n.to_edge(LEFT, buff=MARGIN).set_y(SUB_TOP + 0.28)
    return n


def schematic_tag(s="Schematic, illustrative"):
    return Body(s, font_size=20, color=SRCGRAY, slant=ITALIC)


def organism(s="B. pseudomallei", font_size=22, color=INK):
    return Body(s, font_size=font_size, color=color, slant=ITALIC)


# ---------------------------- SERIES MARKS -----------------------------------
# funded_dot and public_dot are clip 1's marks, unchanged, so act 9's handoff
# lands on the same object the series opened with.

def funded_dot(kind="patient", r=0.070):
    if kind == "patient":
        return Dot(radius=r, color=TEAL_DK).set_fill(TEAL_DK, 1.0).set_stroke(width=0)
    return Dot(radius=r, color=TEAL_DK).set_fill(opacity=0.0).set_stroke(TEAL_DK, 1.7)


def public_dot(r=0.05):
    return Dot(radius=r, color=TEAL_LT).set_fill(TEAL_LT, 1.0).set_stroke(width=0)


# CLIP 4 ADDITION. The continuity object: one of the 46 scorable validation
# genomes. A square, so it never reads as one of the round funded or public
# dots, and teal, so it stays inside the genomic channel. States are carried by
# fill against outline against hue, which stays legible in grayscale.
def val_mark(state="known", s=0.16):
    r = Square(side_length=s, stroke_width=0)
    if state == "known":              # scorable, answer known
        r.set_fill(TEAL, 1.0)
    elif state == "correct":          # retained and called correctly
        r.set_fill(TEAL_TXT, 1.0)
    elif state == "error":            # retained and called wrongly
        r.set_fill(RUST, 1.0)
    elif state == "declined":         # the rule abstained: outline only
        r.set_fill(opacity=0.0).set_stroke(TEAL_TXT, 1.8)
    else:                             # unscorable: outline only, gray
        r.set_fill(opacity=0.0).set_stroke(GRAYOUT, 1.8)
    return r


def val_grid(n=46, cols=12, s=0.16, buff=0.09, state="known"):
    g = VGroup(*[val_mark(state, s) for _ in range(n)])
    g.arrange_in_grid(cols=cols, buff=buff)
    return g


def dot_grid(n, cols, maker, buff=0.052):
    g = VGroup(*[maker(i) for i in range(n)])
    g.arrange_in_grid(cols=cols, buff=buff)
    return g


def pair_glyph(excluded=False, w=0.62):
    """One nominated patient and environment pair."""
    col = GRAYOUT if excluded else TEAL_DK
    a = Dot(radius=0.075, color=col).set_fill(col, 0.0 if excluded else 1.0
                                              ).set_stroke(col, 1.7)
    b = Dot(radius=0.075, color=col).set_fill(opacity=0.0).set_stroke(col, 1.7)
    link = Line(LEFT * w / 2, RIGHT * w / 2, stroke_width=2.0,
                color=GRIDGRAY if excluded else SRCGRAY)
    a.move_to(LEFT * w / 2)
    b.move_to(RIGHT * w / 2)
    g = VGroup(link, a, b)
    return g


def verdict_chip(text, kind="fail", font_size=21):
    """Verdict text is the redundant channel. Colour never carries a class
    on its own, per the accessibility rule."""
    col = {"fail": RUST, "pass": TEAL_TXT, "pending": GRAYOUT}[kind]
    lab = Body(text, font_size=font_size, color=col)
    bar = Line(UP * lab.height / 2, DOWN * lab.height / 2,
               stroke_width=3.0, color=col)
    bar.next_to(lab, LEFT, buff=0.16)
    return VGroup(bar, lab)


# ============================================================================
#  ACT 1. Two questions, one shape          target 45.0 s, ~100 words
#  Entry: black.   Exit: the two questions side by side, both unanswered.
# ============================================================================
class C4Act1(Scene):
    def construct(self):
        # --- film title card, holds 1.5 s, not five --------------------
        ft = Title("How close is close enough?", font_size=46).move_to([0, 0.42, 0])
        fs = Body("TUC briefing, clip four of four", font_size=25, color=SRCGRAY
                  ).move_to([0, -0.42, 0])
        self.play(FadeIn(ft, run_time=0.8), run_time=0.8)                 # 0.8
        self.play(FadeIn(fs, run_time=0.5), run_time=0.5)                 # 1.3
        self.wait(1.5)                                                    # 2.8
        self.play(FadeOut(ft, fs, run_time=0.6), run_time=0.6)    # 3.4

        title = title_at("Two questions, one shape")
        src = source_note("Closeout deck, Nakhon Phanom")
        self.play(FadeIn(title, run_time=0.6), FadeIn(src, run_time=0.6),
                  run_time=0.6)                                           # 4.0
        self.wait(0.4)                                                    # 4.4

        # --- a genome arrives ------------------------------------------
        gen = VGroup(funded_dot("patient", r=0.13))
        gen.move_to([0, 1.72, 0])
        g_lab = Body("A genome arrives from a patient.", font_size=26
                     ).next_to(gen, DOWN, buff=0.30)
        self.play(FadeIn(gen, scale=1.0, run_time=0.7), run_time=0.7)     # 5.1
        self.play(FadeIn(g_lab, shift=UP * 0.12, run_time=0.7), run_time=0.7)
        self.wait(2.9)                                                    # 8.7

        ask = Body("Two questions get asked of it.", font_size=26, color=TEAL_TXT
                   ).move_to(g_lab.get_center())
        self.play(FadeOut(g_lab, run_time=0.5), run_time=0.5)             # 9.2
        self.play(FadeIn(ask, run_time=0.6), run_time=0.6)                # 9.8
        self.wait(2.5)                                                    # 12.3

        # --- the two questions, both pending ---------------------------
        LX, RX, QY = -3.35, 3.35, -0.30
        q1t = Body("Did this patient and this soil sample\nshare a source?",
                   font_size=25, color=INK, line_spacing=0.85)
        q1t.move_to([LX, QY + 0.62, 0])
        pa = funded_dot("patient", r=0.085).move_to([LX - 0.42, QY - 0.42, 0])
        pb = funded_dot("environment", r=0.085).move_to([LX + 0.42, QY - 0.42, 0])
        plink = DashedLine([LX - 0.30, QY - 0.42, 0], [LX + 0.30, QY - 0.42, 0],
                           stroke_width=2.4, color=SRCGRAY, dash_length=0.07)
        q1k = Body("linkage", font_size=21, color=SRCGRAY
                   ).move_to([LX, QY - 0.95, 0])
        q1 = VGroup(q1t, pa, pb, plink, q1k)

        q2t = Body("Where was this infection\nacquired?",
                   font_size=25, color=INK, line_spacing=0.85)
        q2t.move_to([RX, QY + 0.62, 0])
        reg = VGroup(*[Square(side_length=0.22, stroke_width=1.8
                              ).set_fill(opacity=0.0).set_stroke(PURPLE, 1.8)
                       for _ in range(3)]).arrange(RIGHT, buff=0.14)
        reg.move_to([RX, QY - 0.42, 0])
        q2k = Body("geography", font_size=21, color=SRCGRAY
                   ).move_to([RX, QY - 0.95, 0])
        q2 = VGroup(q2t, reg, q2k)

        self.play(FadeIn(q1, shift=UP * 0.12, run_time=0.9), run_time=0.9)  # 13.2
        self.wait(4.1)                                                      # 17.3
        self.play(FadeIn(q2, shift=UP * 0.12, run_time=0.9), run_time=0.9)  # 18.2
        self.wait(4.1)                                                      # 22.3

        same = Body("They look like different questions. They are the same one.",
                    font_size=25, color=INK).move_to([0, -1.74, 0])
        self.play(FadeIn(same, run_time=0.7), run_time=0.7)                 # 23.0
        self.wait(3.3)                                                      # 26.3

        # --- the shape both questions share ----------------------------
        brace = Line([LX + 1.5, -1.30, 0], [RX - 1.5, -1.30, 0],
                     stroke_width=2.5, color=TEAL)
        shape = Body("How close is close enough to claim a link?",
                     font_size=28, color=TEAL_TXT).move_to([0, -2.22, 0])
        self.play(FadeOut(same, run_time=0.4), Create(brace, run_time=0.6),
                  run_time=0.6)                                             # 26.9
        self.play(FadeIn(shape, run_time=0.7), run_time=0.7)                # 27.6
        self.wait(4.2)                                                      # 31.8

        # --- name the Americas, which act 6 depends on having been said -
        am = Body("The applied goal is placing cases in the United States and the\n"
                  "wider Americas that have no travel history.",
                  font_size=24, color=INK, line_spacing=0.85)
        am.move_to([0, 2.26, 0])
        amk = VGroup(*[Square(side_length=0.20, stroke_width=0
                              ).set_fill(PURPLE, 1.0) for _ in range(2)]
                     ).arrange(RIGHT, buff=0.12)
        amk.next_to(am, LEFT, buff=0.34)
        self.play(FadeOut(gen, ask, run_time=0.5), run_time=0.5)    # 32.3
        self.play(FadeIn(am, run_time=0.7), FadeIn(amk, run_time=0.7),
                  run_time=0.7)                                             # 33.0
        self.wait(4.8)                                                      # 37.8

        # --- both get answered, and the answers differ -----------------
        diff = Body("Both get an answer. The two answers are not the same.",
                    font_size=25, color=INK).move_to([0, 1.30, 0])
        self.play(FadeIn(diff, run_time=0.7), run_time=0.7)                 # 38.5
        self.wait(3.3)                                                      # 41.8

        v1 = verdict_chip("unanswered", "pending").move_to([LX, -1.72, 0])
        v2 = verdict_chip("unanswered", "pending").move_to([RX, -1.72, 0])
        self.play(FadeIn(v1, run_time=0.6), FadeIn(v2, run_time=0.6),
                  run_time=0.6)                                             # 42.4
        self.wait(2.6)                                                      # 45.0


# ============================================================================
#  ACT 2. The linkage scale, set up          target 31.0 s, ~70 words
#  Entry: the two questions.   Exit: the near-identical band, empty.
# ============================================================================
class C4Act2(Scene):
    def construct(self):
        title = title_at("The linkage question, asked in the field")
        src = source_note("Closeout deck, Nakhon Phanom, slide 23")
        self.play(FadeIn(title, run_time=0.6), FadeIn(src, run_time=0.6),
                  run_time=0.6)                                             # 0.6
        self.wait(0.4)                                                      # 1.0

        lead = Body("The project already asked the linkage question in the field.",
                    font_size=26).move_to([0, 2.30, 0])
        self.play(FadeIn(lead, run_time=0.7), run_time=0.7)                 # 1.7
        self.wait(3.3)                                                      # 5.0

        # --- nine nominated pairs --------------------------------------
        pairs = VGroup(*[pair_glyph() for _ in range(9)])
        pairs.arrange_in_grid(cols=3, buff=(0.95, 0.52))
        pairs.move_to([-3.55, 0.30, 0])
        pl = Body("Nine nominated patient and\nenvironment pairs.",
                  font_size=24, line_spacing=0.85)
        pl.next_to(pairs, DOWN, buff=0.40)
        self.play(LaggedStartMap(FadeIn, pairs, lag_ratio=0.12, run_time=1.1),
                  run_time=1.1)                                             # 6.1
        self.play(FadeIn(pl, run_time=0.7), run_time=0.7)                   # 6.8
        self.wait(3.2)                                                      # 10.0

        # --- three fall to the exclusions ------------------------------
        drop = VGroup(pairs[2], pairs[5], pairs[8])
        ex1 = Body("Three fall to the", font_size=23, color=SRCGRAY)
        ex2 = organism("B. thailandensis", font_size=23, color=SRCGRAY)
        ex3 = Body("exclusions.", font_size=23, color=SRCGRAY)
        exg = VGroup(ex1, ex2, ex3).arrange(RIGHT, buff=0.16)
        exg.move_to([1.85, 1.52, 0])
        six = Body("Six are evaluable.", font_size=26, color=TEAL_TXT
                   ).move_to([1.85, 0.82, 0])
        self.play(drop.animate.set_opacity(0.22), FadeIn(exg, run_time=0.7),
                  run_time=0.8)                                             # 10.8
        self.play(FadeIn(six, run_time=0.6), run_time=0.6)                  # 11.4
        self.wait(3.6)                                                      # 15.0

        # --- the near-identical band, which act 3 opens on -------------
        AX0, AX1, AY = -4.90, 4.30, -1.42
        axis = Line([AX0, AY, 0], [AX1, AY, 0], stroke_width=2.2, color=INK)
        band = Rectangle(width=1.35, height=0.92, stroke_width=0
                         ).set_fill(GRIDGRAY, 1.0)
        band.move_to([AX0 + 0.675, AY + 0.46, 0])
        bl = Body("near-identical", font_size=21, color=INK)
        bl.move_to([AX0 + 0.675, AY + 1.16, 0])
        ax_l = Body("identical", font_size=20, color=SRCGRAY
                    ).next_to(axis.get_start(), DOWN, buff=0.22)
        ax_r = Body("distant", font_size=20, color=SRCGRAY
                    ).next_to(axis.get_end(), DOWN, buff=0.22)
        ax_t = Body("core-genome distance between a patient and an environment isolate",
                    font_size=20, color=SRCGRAY)
        ax_t.move_to([(AX0 + AX1) / 2, AY - 0.74, 0])
        self.play(FadeOut(pairs, pl, exg, six, run_time=0.5),
                  run_time=0.5)                                             # 15.5
        self.play(Create(axis, run_time=0.7), run_time=0.7)                 # 16.2
        self.play(FadeIn(band, run_time=0.6), FadeIn(bl, run_time=0.6),
                  FadeIn(VGroup(ax_l, ax_r, ax_t), run_time=0.6),
                  run_time=0.6)                                             # 16.8
        self.wait(2.2)                                                      # 19.0

        # --- where the six actually fell -------------------------------
        xs = [-1.60, -0.55, 0.62, 1.48, 2.55, 3.42]
        six_marks = VGroup(*[funded_dot("patient", r=0.085).move_to([x, AY + 0.46, 0])
                             for x in xs])
        self.play(LaggedStartMap(FadeIn, six_marks, lag_ratio=0.16, run_time=1.0),
                  run_time=1.0)                                             # 20.0
        self.wait(4.0)                                                      # 24.0

        find = Body("None of the six fell inside the near-identical range.",
                    font_size=26, color=INK).move_to([0, 1.58, 0])
        self.play(FadeIn(find, run_time=0.7), run_time=0.7)                 # 24.7
        self.wait(2.3)                                                      # 27.0

        # --- state it as a finding, and clear the band for act 3 -------
        kept = Body("That is a finding about the scale, not a disappointment.",
                    font_size=25, color=TEAL_TXT).move_to([0, 0.92, 0])
        self.play(FadeIn(kept, run_time=0.7), run_time=0.7)                 # 27.7
        self.wait(1.4)                                                      # 29.1
        self.play(FadeOut(six_marks, run_time=0.6), run_time=0.6)           # 29.7
        self.wait(1.3)                                                      # 31.0


# ============================================================================
#  ACT 4. The geography scale, set up       target 58.0 s, ~130 words
#  Entry: the 46 marks arrive.   Exit: 46 marks, each with a true label.
#
#  The brief's continuity note says the 46 appear in act 2, while act 2's own
#  entry and exit states carry the linkage band instead. Act-level states are
#  the more specific instruction, so the 46 are introduced here, at act 4's
#  stated entry. Flagged in NOTE.md.
# ============================================================================
class C4Act4(Scene):
    def construct(self):
        title = title_at("46 genomes with a known answer")
        src = source_note("Frozen validation set, 46 scorable of 48 registered")
        self.play(FadeIn(title, run_time=0.6), FadeIn(src, run_time=0.6),
                  run_time=0.6)                                             # 0.6
        self.wait(0.4)                                                      # 1.0

        # --- 48 registered ---------------------------------------------
        marks = val_grid(48, cols=12)
        marks.move_to([-3.05, 1.42, 0])
        m_lab = Body("48 genomes are registered with an\nexposure that is independently known.",
                     font_size=24, line_spacing=0.85)
        m_lab.next_to(marks, DOWN, buff=0.40).align_to(marks, LEFT)
        self.play(LaggedStartMap(FadeIn, marks, lag_ratio=0.012, run_time=1.0),
                  run_time=1.0)                                             # 2.0
        self.play(FadeIn(m_lab, run_time=0.7), run_time=0.7)                # 2.7
        self.wait(3.3)                                                      # 6.0

        # --- two cannot be scored --------------------------------------
        # Restyled IN PLACE, not transformed out of the grid. Putting a
        # sub-VGroup of `marks` into a later FadeOut silently cancels the
        # removal of every other mobject in that same call, because
        # Scene.remove extracts the parent's family rather than removing
        # the siblings. Reproduced on manim 0.21.0, and it had left the
        # whole first half of this act on screen for its remaining 34 s.
        u1 = val_mark("unscorable").move_to(marks[46].get_center())
        u2 = val_mark("unscorable").move_to(marks[47].get_center())
        o_l1 = Body("Africa", font_size=21, color=SRCGRAY)
        o_l2 = Body("Panama and Peru", font_size=21, color=SRCGRAY)
        o_ls = VGroup(o_l1, o_l2).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        o_ls.next_to(marks, RIGHT, buff=0.40).set_y(marks[46].get_center()[1])
        self.play(Transform(marks[46], u1, run_time=0.9),
                  Transform(marks[47], u2, run_time=0.9), run_time=0.9)     # 6.9
        self.play(FadeIn(o_ls, run_time=0.6), run_time=0.6)                 # 7.5
        self.wait(3.5)                                                      # 11.0

        o_why = Body("Two carry a non-country exposure,\nso they cannot be scored at all.",
                     font_size=23, color=INK, line_spacing=0.85)
        o_why.move_to([3.40, 0.10, 0])
        self.play(FadeIn(o_why, run_time=0.7), run_time=0.7)                # 11.7
        self.wait(3.3)                                                      # 15.0

        # --- 46 is the denominator of everything that follows ----------
        den = Body("46 scorable.", font_size=30, color=TEAL_TXT
                   ).move_to([-3.05, -0.72, 0])
        den2 = Body("This is the denominator of every score in this briefing.",
                    font_size=23, color=INK)
        den2.next_to(den, DOWN, buff=0.26).align_to(den, LEFT)
        self.play(FadeOut(m_lab, run_time=0.4), run_time=0.4)               # 15.4
        self.play(FadeIn(den, run_time=0.6), run_time=0.6)                  # 16.0
        self.play(FadeIn(den2, run_time=0.6), run_time=0.6)                 # 16.6
        self.wait(3.4)                                                      # 20.0

        cty = Body("They came from 16 exposure countries.",
                   font_size=23, color=INK)
        cty.next_to(den2, DOWN, buff=0.26).align_to(den, LEFT)
        self.play(FadeIn(cty, run_time=0.6), run_time=0.6)                  # 20.6
        self.wait(2.4)                                                      # 23.0

        # --- leave-group-out, stated plainly ---------------------------
        self.play(FadeOut(o_ls, o_why, den, den2, cty, run_time=0.6),
                  marks.animate.move_to([-4.30, 1.98, 0]).scale(0.78),
                  run_time=0.6)                                             # 23.6

        lgo_t = Body("Leave-group-out", font_size=27, color=TEAL_TXT
                     ).move_to([-0.30, 1.98, 0])
        grp = VGroup(*[public_dot(r=0.075) for _ in range(7)])
        grp.arrange_in_grid(cols=4, buff=0.22)
        grp.move_to([-1.55, 0.36, 0])
        tgt = val_mark("known", s=0.20).move_to(grp[0].get_center())
        box = Rectangle(width=grp.width + 0.40, height=grp.height + 0.40,
                        stroke_width=2.0, color=SRCGRAY
                        ).set_fill(opacity=0.0).move_to(grp.get_center())
        b_lab = Body("its whole outbreak or submission group",
                     font_size=20, color=SRCGRAY)
        b_lab.next_to(box, DOWN, buff=0.24)
        self.play(FadeIn(lgo_t, run_time=0.6), run_time=0.6)                # 24.2
        self.play(FadeIn(grp, run_time=0.6), FadeIn(tgt, run_time=0.6),
                  run_time=0.6)                                             # 24.8
        self.play(Create(box, run_time=0.6), FadeIn(b_lab, run_time=0.6),
                  run_time=0.6)                                             # 25.4
        self.wait(1.6)                                                      # 27.0

        s1 = Body("Hold out the whole group, not just the one genome.",
                  font_size=24, color=INK).move_to([2.35, 1.06, 0])
        self.play(FadeIn(s1, run_time=0.7), run_time=0.7)                   # 27.7
        self.wait(4.3)                                                      # 32.0

        s2 = Body("Sibling isolates from the same event\nwould otherwise hand the answer back.",
                  font_size=24, color=INK, line_spacing=0.85)
        s2.move_to([2.35, 0.14, 0])
        self.play(FadeIn(s2, run_time=0.7), run_time=0.7)                   # 32.7
        self.wait(4.3)                                                      # 37.0

        self.play(VGroup(grp, box, b_lab).animate.set_opacity(0.22),
                  run_time=0.9)                                             # 37.9
        rest = Body("The call is made from the rest of the panel.",
                    font_size=23, color=TEAL_TXT).move_to([-1.55, -1.28, 0])
        self.play(FadeIn(rest, run_time=0.6), run_time=0.6)                 # 38.5
        self.wait(3.0)                                                      # 41.5

        # --- what counts as correct, stated before any score -----------
        rule = Body("Correct means the predicted label equals the known one.",
                    font_size=25, color=INK).move_to([0, -1.94, 0])
        self.play(FadeIn(rule, run_time=0.7), run_time=0.7)                 # 42.2
        self.wait(4.3)                                                      # 46.5

        pre = Body("Stated before any score appears.", font_size=22,
                   color=SRCGRAY).move_to([0, -2.34, 0])
        self.play(FadeIn(pre, run_time=0.6), run_time=0.6)                  # 47.1
        self.wait(3.4)                                                      # 50.5

        # --- exit state: 46 marks, each with a true label --------------
        self.play(FadeOut(grp, box, b_lab, tgt, rest, lgo_t, s1, s2,
                          run_time=0.6), run_time=0.6)                      # 51.1
        m2 = val_grid(46, cols=12)
        m2.move_to([0, 0.34, 0])
        m2_l = Body("46 marks, each carrying its true exposure country.",
                    font_size=24, color=INK).next_to(m2, DOWN, buff=0.44)
        self.play(FadeOut(marks, run_time=0.5), FadeIn(m2, run_time=0.9),
                  run_time=0.9)                                             # 52.0
        self.play(FadeIn(m2_l, run_time=0.6), run_time=0.6)                 # 52.6
        self.wait(5.4)                                                      # 58.0


# ============================================================================
#  ACT 5. The ladder                        target 85.0 s, ~190 words
#  Entry: 46 labeled marks.  Exit: five rungs, each with kappa and baseline.
#
#  ORDERING. The rungs are ordered by the SCALE of the question, never by
#  their score, so the display runs 16 classes, then five, then the three
#  two-class questions. That ordering is what makes the result's own honesty
#  check visible: SEA vs non-SEA is a two-class question scoring 0.461, below
#  the five-class region question at 0.832. Sorting these five by kappa, or by
#  the order the brief's data table happens to list them in, produces a smooth
#  monotonic climb from 0.193 to 1.000 and deletes that dip. The brief names
#  that picture as the single most likely fabrication, so it is avoided here by
#  construction rather than by caption.
# ============================================================================
class C4Act5(Scene):
    # rung, classes, accuracy, baseline, kappa, estimator
    RUNGS = [
        ("Country",          "16 classes", "22%", "26%", 0.193, "nearest neighbour"),
        ("Region",           "5 classes",  "89%", "46%", 0.832, "modal k=20"),
        ("SEA vs non-SEA",   "2 classes",  "76%", "59%", 0.461, "modal k=20"),
        ("East vs West",     "2 classes",  "96%", "63%", 0.909, "modal k=20"),
        ("Asia vs non-Asia", "2 classes",  "100%", "59%", 1.000, "modal k=20"),
    ]
    NAME_X, BAR_X0, BAR_W = -6.20, -2.45, 3.35
    VAL_X, RIGHT_X = 1.06, 2.05
    ROW_Y = [1.30, 0.50, -0.30, -1.10, -1.90]

    def construct(self):
        title = title_at("The grouping ladder")
        src = source_note("Grouping ladder, 46 scorable genomes")
        self.play(FadeIn(title, run_time=0.6), FadeIn(src, run_time=0.6),
                  run_time=0.6)                                             # 0.6
        self.wait(0.4)                                                      # 1.0

        # --- the same 46, kept on screen as the continuity object ------
        marks = val_grid(46, cols=12)
        marks.move_to([0, 0.60, 0])
        same = Body("The same 46 genomes, scored five times.",
                    font_size=26, color=INK).next_to(marks, DOWN, buff=0.44)
        self.play(FadeIn(marks, run_time=0.8), run_time=0.8)                # 1.8
        self.play(FadeIn(same, run_time=0.7), run_time=0.7)                 # 2.5
        self.wait(3.5)                                                      # 6.0

        # --- define kappa, because the audience will interrogate it ----
        k1 = Body("Cohen's kappa scores agreement above what chance alone would give.",
                  font_size=25, color=INK).move_to([0, -1.18, 0])
        self.play(FadeIn(k1, run_time=0.7), run_time=0.7)                   # 6.7
        self.wait(4.3)                                                      # 11.0

        k2 = Body("Raw accuracy is not comparable across groupings,\n"
                  "so every rung carries its own baseline.",
                  font_size=25, color=TEAL_TXT, line_spacing=0.85)
        k2.move_to([0, -2.06, 0])
        self.play(FadeIn(k2, run_time=0.7), run_time=0.7)                   # 11.7
        self.wait(4.3)                                                      # 16.0

        # --- the axis -------------------------------------------------
        self.play(FadeOut(same, k1, k2, run_time=0.5),
                  marks.animate.scale(0.70).move_to([4.55, 2.55, 0]),
                  run_time=0.5)                                             # 16.5
        # left of the strip, not under it: under it collides with the country
        # rung's verdict chip, which owns that band
        m_tag = Body("the same 46", font_size=20, color=SRCGRAY)
        m_tag.next_to(marks, LEFT, buff=0.22)

        AXY = 1.92
        axis = Line([self.BAR_X0, AXY, 0], [self.BAR_X0 + self.BAR_W, AXY, 0],
                    stroke_width=1.8, color=SRCGRAY)
        ticks = VGroup()
        for frac, lab in ((0.0, "0"), (0.5, "0.5"), (1.0, "1.0")):
            x = self.BAR_X0 + frac * self.BAR_W
            ticks.add(Line([x, AXY, 0], [x, AXY + 0.11, 0],
                           stroke_width=1.8, color=SRCGRAY))
            ticks.add(Body(lab, font_size=20, color=SRCGRAY
                           ).move_to([x, AXY + 0.31, 0]))
        ax_t = Body("Cohen's kappa", font_size=21, color=INK)
        ax_t.move_to([self.BAR_X0 + self.BAR_W / 2, AXY + 0.72, 0])
        self.play(Create(axis, run_time=0.5), FadeIn(ticks, run_time=0.5),
                  FadeIn(ax_t, run_time=0.5), FadeIn(m_tag, run_time=0.5),
                  run_time=0.8)                                             # 17.3
        self.wait(1.7)                                                      # 19.0

        # --- the rungs, one at a time, in scale order -----------------
        rows, bars = [], []
        for i, (nm, cls, acc, base, kap, est) in enumerate(self.RUNGS):
            y = self.ROW_Y[i]
            col = RUST if i == 0 else TEAL
            name = Body(nm, font_size=23, color=INK)
            name.move_to([self.NAME_X, y + 0.14, 0], aligned_edge=LEFT)
            ncl = Body(cls, font_size=20, color=SRCGRAY)
            ncl.move_to([self.NAME_X, y - 0.18, 0], aligned_edge=LEFT)
            track = Line([self.BAR_X0, y, 0], [self.BAR_X0 + self.BAR_W, y, 0],
                         stroke_width=1.4, color=GRIDGRAY)
            bar = Rectangle(width=max(kap * self.BAR_W, 0.001), height=0.24,
                            stroke_width=0).set_fill(col, 1.0)
            bar.move_to([self.BAR_X0 + kap * self.BAR_W / 2, y, 0])
            val = Body(f"{kap:.3f}", font_size=25,
                       color=RUST if i == 0 else TEAL_TXT)
            val.move_to([self.VAL_X, y, 0], aligned_edge=LEFT)
            accl = Body(f"{acc} correct, {base} baseline", font_size=20, color=INK)
            accl.move_to([self.RIGHT_X, y + 0.15, 0], aligned_edge=LEFT)
            estl = Body(est, font_size=20, color=SRCGRAY)
            estl.move_to([self.RIGHT_X, y - 0.17, 0], aligned_edge=LEFT)
            rows.append(VGroup(name, ncl, track, bar, val, accl, estl))
            bars.append(bar)

        # rung 1, country
        self.play(FadeIn(rows[0], run_time=1.0), run_time=1.0)              # 20.0
        self.wait(4.0)                                                      # 24.0
        v_ct = verdict_chip("below its own baseline: no answer", "fail",
                            font_size=20)
        v_ct.move_to([1.90, self.ROW_Y[0] + 0.62, 0], aligned_edge=LEFT)
        self.play(FadeIn(v_ct, run_time=0.8), run_time=0.8)                 # 24.8
        self.wait(4.2)                                                      # 29.0

        self.play(FadeIn(rows[1], run_time=1.0), run_time=1.0)              # 30.0
        self.wait(4.0)                                                      # 34.0
        self.play(FadeIn(rows[2], run_time=1.0), run_time=1.0)              # 35.0
        self.wait(4.0)                                                      # 39.0
        self.play(FadeIn(rows[3], run_time=1.0), run_time=1.0)              # 40.0
        self.wait(3.0)                                                      # 43.0
        self.play(FadeIn(rows[4], run_time=1.0), run_time=1.0)              # 44.0
        self.wait(3.0)                                                      # 47.0

        # --- the three two-class rungs, bracketed ---------------------
        self.play(Indicate(VGroup(rows[2][1], rows[3][1], rows[4][1]),
                           color=TEAL_TXT, scale_factor=1.06, run_time=0.9),
                  run_time=0.9)                                             # 47.9
        self.wait(4.1)                                                      # 52.0

        span = Body("They span 0.461 to 1.000.", font_size=24, color=INK)
        span.move_to([self.NAME_X, -2.40, 0], aligned_edge=LEFT)
        self.play(Indicate(rows[2], color=RUST, scale_factor=1.03, run_time=1.0),
                  run_time=1.0)                                             # 53.0
        self.play(FadeIn(span, run_time=0.6), run_time=0.6)                 # 53.6
        self.wait(3.4)                                                      # 57.0

        coarse = Body("Coarser is not automatically better.",
                      font_size=25, color=TEAL_TXT)
        coarse.next_to(span, RIGHT, buff=0.42)
        self.play(FadeIn(coarse, run_time=0.7), run_time=0.7)               # 57.7
        self.wait(4.3)                                                      # 62.0

        ordr = Body("Rungs are ordered by the scale of the question, never by score.",
                    font_size=20, color=SRCGRAY)
        ordr.move_to([-1.60, -2.72, 0], aligned_edge=LEFT)
        self.play(FadeIn(ordr, run_time=0.7), run_time=0.7)                 # 62.7
        self.wait(4.3)                                                      # 67.0

        # --- the two headlines, with their estimators on screen -------
        self.play(Indicate(rows[1], color=TEAL_TXT, scale_factor=1.03,
                           run_time=1.0), run_time=1.0)                     # 68.0
        self.wait(4.0)                                                      # 72.0
        self.play(Indicate(rows[4], color=TEAL_TXT, scale_factor=1.03,
                           run_time=1.0), run_time=1.0)                     # 73.0
        self.wait(4.0)                                                      # 77.0

        self.play(Indicate(rows[0], color=RUST, scale_factor=1.03,
                           run_time=1.0), run_time=1.0)                     # 78.0
        self.wait(3.0)                                                      # 81.0
        self.wait(4.0)                                                      # 85.0


# ============================================================================
#  ACT 7. One mechanism, both ceilings      target 77.0 s, ~170 words
#  Entry: the five rungs.   Exit: the rungs re-read as an erosion gradient.
#
#  SCHEMATIC vs MEASURED. We measured r/m. The within-population versus
#  between-population erosion is the CITED EXPLANATION for the pattern, not a
#  quantity this study produced, so it is drawn in dashed outline with no fills
#  and carries a schematic tag for as long as it is on screen. The association
#  index bars beside it are measured, on a DIFFERENT panel, and carry that
#  panel's framework label. Nothing in this act is drawn as solidly as act 5's
#  rungs.
# ============================================================================
class C4Act7(Scene):
    AI = [("Region", 0.193, True), ("Country", 0.236, True),
          ("Collection decade", 0.581, False), ("Isolation source", 0.710, False),
          ("Thai province", 0.721, False)]

    def construct(self):
        title = title_at("One mechanism, both ceilings")
        src = source_note("Mechanism is schematic, not measured here")
        self.play(FadeIn(title, run_time=0.6), FadeIn(src, run_time=0.6),
                  run_time=0.6)                                             # 0.6
        self.wait(0.4)                                                      # 1.0

        # --- two populations, dashed outline, never solid --------------
        tag = schematic_tag("Schematic. The mechanism is cited, not measured here.")
        tag.move_to([0, -2.24, 0])

        def blob(cx, cy, n, seed):
            rng = np.random.default_rng(seed)
            g = VGroup()
            for _ in range(n):
                a, r = rng.uniform(0, 2 * np.pi), rng.uniform(0, 1) ** 0.5
                d = Dot(radius=0.055, color=TEAL_LT).set_fill(TEAL_LT, 1.0
                        ).set_stroke(width=0)
                d.move_to([cx + 0.92 * r * np.cos(a), cy + 0.62 * r * np.sin(a), 0])
                g.add(d)
            return g

        pL, pR = blob(-3.45, 0.50, 26, 11), blob(2.85, 0.50, 26, 12)
        ringL = DashedVMobject(Ellipse(width=2.30, height=1.60, color=TEAL_TXT,
                                       stroke_width=2.0).move_to([-3.45, 0.50, 0]),
                               num_dashes=34)
        ringR = DashedVMobject(Ellipse(width=2.30, height=1.60, color=TEAL_TXT,
                                       stroke_width=2.0).move_to([2.85, 0.50, 0]),
                               num_dashes=34)
        nL = Body("one population", font_size=20, color=SRCGRAY
                  ).move_to([-3.45, -0.62, 0])
        nR = Body("another population", font_size=20, color=SRCGRAY
                  ).move_to([2.85, -0.62, 0])
        self.play(FadeIn(VGroup(pL, pR), run_time=0.6),
                  Create(VGroup(ringL, ringR), run_time=0.8),
                  FadeIn(VGroup(nL, nR, tag), run_time=0.6), run_time=0.9)  # 1.9
        self.wait(3.1)                                                      # 5.0

        # --- movement inside a population is constant -----------------
        ins = VGroup()
        for (cx, cy), sd in (((-3.45, 0.50), 21), ((2.85, 0.50), 22)):
            rng = np.random.default_rng(sd)
            for _ in range(7):
                a1, a2 = rng.uniform(0, 2 * np.pi), rng.uniform(0, 2 * np.pi)
                p1 = [cx + 0.72 * np.cos(a1), cy + 0.46 * np.sin(a1), 0]
                p2 = [cx + 0.72 * np.cos(a2), cy + 0.46 * np.sin(a2), 0]
                ins.add(DashedLine(p1, p2, stroke_width=1.8, color=TEAL,
                                   dash_length=0.055))
        in_l = Body("Recombination moves DNA between lineages\ninside a population.",
                    font_size=25, color=INK, line_spacing=0.85)
        in_l.move_to([0, 2.24, 0])
        self.play(FadeIn(ins, run_time=0.8), run_time=0.9)                  # 5.9
        self.play(FadeIn(in_l, run_time=0.7), run_time=0.7)                 # 6.6
        self.wait(3.4)                                                      # 10.0

        # --- movement between populations is rare ---------------------
        btw = DashedLine([-2.32, 0.50, 0], [1.72, 0.50, 0], stroke_width=1.8,
                         color=SRCGRAY, dash_length=0.10)
        bt_l = Body("Between populations that movement is rare.",
                    font_size=25, color=INK).move_to([0, 1.62, 0])
        self.play(Create(btw, run_time=0.7), run_time=0.9)                  # 10.9
        self.play(FadeIn(bt_l, run_time=0.7), run_time=0.7)                 # 11.6
        self.wait(3.4)                                                      # 15.0

        cav = Body("This is the cited explanation for the pattern,\n"
                   "not a quantity this study measured.",
                   font_size=22, color=SRCGRAY, line_spacing=0.85)
        cav.move_to([0, -1.32, 0])
        self.play(FadeIn(cav, run_time=0.7), run_time=0.7)                  # 15.7
        self.wait(3.3)                                                      # 19.0

        # --- fine erased, coarse preserved ----------------------------
        self.play(FadeOut(in_l, bt_l, cav, run_time=0.5),
                  run_time=0.5)                                             # 19.5
        f_l = Body("Fine scale erased.", font_size=27, color=RUST
                   ).move_to([-3.45, 2.20, 0])
        f_x = VGroup(*[DashedLine([-4.25 + i * 0.52, 1.72, 0],
                                  [-4.05 + i * 0.52, 1.72, 0],
                                  stroke_width=2.4, color=RUST, dash_length=0.06)
                       for i in range(4)])
        self.play(FadeIn(f_l, run_time=0.7), FadeIn(f_x, run_time=0.7),
                  run_time=0.8)                                             # 20.3
        self.wait(2.7)                                                      # 23.0

        c_l = Body("Coarse scale preserved.", font_size=27, color=TEAL_TXT
                   ).move_to([2.85, 2.20, 0])
        c_k = Line([1.95, 1.72, 0], [3.75, 1.72, 0], stroke_width=2.6,
                   color=TEAL_TXT)
        self.play(FadeIn(c_l, run_time=0.7), Create(c_k, run_time=0.7),
                  run_time=0.8)                                             # 23.8
        self.wait(3.2)                                                      # 27.0

        # --- the two ceilings, named ----------------------------------
        self.play(FadeOut(pL, pR, ringL, ringR, nL, nR, ins, btw,
                                 f_x, c_k, f_l, c_l, run_time=0.6),
                  run_time=0.6)                                             # 28.4
        ce1 = Body("The linkage ceiling, from the field result.",
                   font_size=25, color=INK).move_to([0, 1.28, 0])
        ce2 = Body("The country ceiling, from the ladder.",
                   font_size=25, color=INK).move_to([0, 0.56, 0])
        self.play(FadeIn(ce1, run_time=0.6), run_time=0.6)                  # 29.0
        self.play(FadeIn(ce2, run_time=0.6), run_time=0.6)                  # 29.6
        self.wait(2.4)                                                      # 32.0

        one = Body("One cause explains both.", font_size=28, color=TEAL_TXT
                   ).move_to([0, -0.24, 0])
        self.play(FadeIn(one, run_time=0.7), run_time=0.7)                  # 32.7
        self.wait(3.3)                                                      # 36.0

        plus = Body("And this collection could not have settled country anyway.",
                    font_size=24, color=SRCGRAY).move_to([0, -0.92, 0])
        self.play(FadeIn(plus, run_time=0.7), run_time=0.7)                 # 36.7
        self.wait(4.3)                                                      # 41.0

        # --- corroboration, on a different panel, labeled as such -----
        self.play(FadeOut(ce1, ce2, one, plus, tag, run_time=0.6),
                  run_time=0.6)                                             # 41.6
        fw = Body("A second reading, on the Kawang framework: 2,773 genomes, "
                  "35 countries.", font_size=22, color=SRCGRAY)
        fw.move_to([0, 2.58, 0])
        BX0, BW, AXY2 = -1.90, 3.50, -1.52
        axis = Line([BX0, AXY2, 0], [BX0 + BW, AXY2, 0], stroke_width=1.8,
                    color=SRCGRAY)
        tk = VGroup()
        for frac, lab in ((0.0, "0"), (0.5, "0.5"), (1.0, "1.0")):
            x = BX0 + frac * BW
            tk.add(Line([x, AXY2, 0], [x, AXY2 - 0.10, 0], stroke_width=1.8,
                        color=SRCGRAY))
            tk.add(Body(lab, font_size=20, color=SRCGRAY
                        ).move_to([x, AXY2 - 0.29, 0]))
        at = Body("association index", font_size=21, color=INK
                  ).move_to([BX0 + BW / 2, -2.14, 0])
        lower = Body("lower means more structured", font_size=20, color=SRCGRAY
                     ).move_to([BX0 + BW / 2, -2.48, 0])
        self.play(FadeIn(fw, run_time=0.6), Create(axis, run_time=0.6),
                  FadeIn(tk, run_time=0.6), run_time=0.9)                   # 42.5
        self.wait(1.5)                                                      # 44.0

        AY = [1.30, 0.70, 0.10, -0.50, -1.10]
        rows = []
        for i, (nm, v, structured) in enumerate(self.AI):
            y = AY[i]
            nl = Body(nm, font_size=22, color=INK)
            nl.move_to([-6.20, y, 0], aligned_edge=LEFT)
            track = Line([BX0, y, 0], [BX0 + BW, y, 0], stroke_width=1.4,
                         color=GRIDGRAY)
            bar = Rectangle(width=v * BW, height=0.22, stroke_width=0)
            if structured:
                bar.set_fill(TEAL, 1.0)
            else:
                bar.set_fill(opacity=0.0).set_stroke(TEAL_TXT, 1.8)
            bar.move_to([BX0 + v * BW / 2, y, 0])
            vl = Body(f"{v:.3f}", font_size=22, color=TEAL_TXT)
            vl.move_to([BX0 + BW + 0.22, y, 0], aligned_edge=LEFT)
            kind = Body("strongly structured" if structured else "well mixed",
                        font_size=20, color=SRCGRAY)
            kind.move_to([3.40, y, 0], aligned_edge=LEFT)
            rows.append(VGroup(nl, track, bar, vl, kind))

        self.play(FadeIn(VGroup(rows[0], rows[1]), run_time=1.0),
                  run_time=1.0)                                             # 45.0
        self.wait(4.0)                                                      # 49.0
        self.play(FadeIn(VGroup(rows[2], rows[3], rows[4]), run_time=1.0),
                  run_time=1.0)                                             # 50.0
        self.wait(4.0)                                                      # 54.0
        self.play(FadeIn(VGroup(at, lower), run_time=0.7), run_time=0.7)    # 54.7
        self.wait(3.3)                                                      # 58.0

        pt = Body("The two geographic traits are the structured ones.",
                  font_size=24, color=TEAL_TXT).move_to([0, 1.74, 0])
        self.play(FadeIn(pt, run_time=0.7), run_time=0.7)                   # 58.7
        self.wait(4.3)                                                      # 63.0

        pt2 = Body("A different panel and a different method, pointing the same way.",
                   font_size=23, color=INK).move_to([0, 2.14, 0])
        self.play(FadeIn(pt2, run_time=0.7), run_time=0.7)                  # 63.7
        self.wait(4.3)                                                      # 68.0

        self.play(Indicate(VGroup(rows[0], rows[1]), color=TEAL_TXT,
                           scale_factor=1.02, run_time=1.0), run_time=1.0)  # 69.0
        self.wait(3.0)                                                      # 72.0
        self.wait(5.8)                                                      # 77.0


# ============================================================================
#  ACT 8. Knowing when not to answer        target 45.0 s, ~100 words
#  Entry: the five rungs, re-read.  Exit: retained and declined, separated.
#
#  The 94.3% at 76.1% is the OUT OF SAMPLE figure, threshold picked on the
#  other 45 genomes, which is the defensible one. 35 of 46 retained is 76.1%
#  and 33 of 35 correct is 94.3%, so the marks on screen reproduce the
#  headline exactly. Country appears here only as a failure.
# ============================================================================
class C4Act8(Scene):
    def construct(self):
        title = title_at("Knowing when not to answer")
        src = source_note("Abstention operating point, out of sample")
        self.play(FadeIn(title, run_time=0.6), FadeIn(src, run_time=0.6),
                  run_time=0.6)                                             # 0.6
        self.wait(0.4)                                                      # 1.0

        marks = val_grid(46, cols=12)
        marks.move_to([0, 1.72, 0])
        lead = Body("A rule that declines rather than guesses.",
                    font_size=27, color=TEAL_TXT).next_to(marks, DOWN, buff=0.42)
        self.play(FadeIn(marks, run_time=0.7), run_time=0.7)                # 1.7
        self.play(FadeIn(lead, run_time=0.7), run_time=0.9)                 # 2.6
        self.wait(2.4)                                                      # 5.0

        r1 = Body("Below a distance threshold the region call stands.",
                  font_size=24, color=INK).move_to([0, 0.24, 0])
        self.play(FadeIn(r1, run_time=0.7), run_time=0.7)                   # 5.7
        self.wait(3.3)                                                      # 9.0
        r2 = Body("Above it the genome is reported as unattributable.",
                  font_size=24, color=INK).move_to([0, -0.34, 0])
        self.play(FadeIn(r2, run_time=0.7), run_time=0.7)                   # 9.7
        self.wait(3.3)                                                      # 13.0

        # --- 35 retained, 11 declined, which is the headline itself ---
        kept = VGroup(*[val_mark("correct") for _ in range(33)]
                      + [val_mark("error") for _ in range(2)])
        kept.arrange_in_grid(cols=7, buff=0.09).move_to([-2.85, 0.92, 0])
        dec = val_grid(11, cols=4, state="declined").move_to([2.95, 0.92, 0])
        k_l = Body("35 retained", font_size=24, color=TEAL_TXT
                   ).move_to([-2.85, -0.10, 0])
        d_l = Body("11 declined", font_size=24, color=INK
                   ).move_to([2.95, -0.10, 0])
        self.play(FadeOut(lead, r1, r2, run_time=0.5),
                  FadeOut(marks, run_time=0.5), run_time=0.5)               # 13.5
        self.play(FadeIn(kept, run_time=1.0), FadeIn(dec, run_time=1.0),
                  FadeIn(VGroup(k_l, d_l), run_time=1.0), run_time=1.2)     # 14.7
        self.wait(3.3)                                                      # 18.0

        oos = Body("Out of sample, with the threshold chosen on the other 45.",
                   font_size=23, color=SRCGRAY).move_to([0, -0.72, 0])
        self.play(FadeIn(oos, run_time=0.7), run_time=0.7)                  # 18.7
        self.wait(4.3)                                                      # 23.0

        head = Body("94.3% correct on what it keeps, at 76.1% coverage.",
                    font_size=27, color=TEAL_TXT).move_to([0, -1.28, 0])
        self.play(FadeIn(head, run_time=0.9), run_time=0.9)                 # 23.9
        self.wait(4.1)                                                      # 28.0

        ss = Body("It declines both Sub-Saharan attractor errors.",
                  font_size=23, color=INK).move_to([0, -1.86, 0])
        self.play(Indicate(dec, color=TEAL_TXT, scale_factor=1.04, run_time=1.0),
                  run_time=1.0)                                             # 29.0
        self.play(FadeIn(ss, run_time=0.6), run_time=0.6)                   # 29.6
        self.wait(3.4)                                                      # 33.0

        er = Body("The two it keeps and gets wrong have genuine close relatives.",
                  font_size=23, color=RUST).move_to([0, -2.34, 0])
        self.play(FadeIn(er, run_time=0.7), run_time=0.7)                   # 33.7
        self.wait(3.3)                                                      # 37.0

        # --- it does not rescue country, and says so ------------------
        self.play(FadeOut(oos, ss, er, run_time=0.5), run_time=0.5)  # 37.5
        nc = Body("It does not rescue country.", font_size=27, color=RUST
                  ).move_to([0, -1.70, 0])
        nc2 = Body("Country's selective accuracy is 37.5%, and the retained-majority\n"
                   "baseline is also 37.5%. The rule found an easier subset, not a signal.",
                   font_size=22, color=INK, line_spacing=0.85)
        nc2.move_to([0, -2.22, 0])
        self.play(FadeIn(nc, run_time=0.7), run_time=0.9)                   # 38.4
        self.play(FadeIn(nc2, run_time=0.7), run_time=0.7)                  # 39.1
        self.wait(5.9)                                                      # 45.0


# ============================================================================
#  ACT 9. The accounting                    target 40.0 s, ~90 words
#  Entry: the retained set.  Exit: the 312, and one line about what to fund.
#  The continuity object hands off: the 46 validation squares become the 312
#  funded dots the series opened on.
# ============================================================================
class C4Act9(Scene):
    def construct(self):
        title = title_at("What this project added")
        src = source_note("Frozen basis, 2026-08-22")
        self.play(FadeIn(title, run_time=0.6), FadeIn(src, run_time=0.6),
                  run_time=0.6)                                             # 0.6
        self.wait(0.4)                                                      # 1.0

        # --- the handoff -----------------------------------------------
        v = val_grid(46, cols=12).move_to([0, 1.30, 0])
        self.add(v)
        marks = dot_grid(312, 26,
                         lambda i: funded_dot("patient" if i < 259 else "environment"))
        marks.scale(0.62).move_to([-3.72, 0.92, 0])
        hand = Body("The 46 hand off to the 312.", font_size=23, color=SRCGRAY
                    ).move_to([0, 2.42, 0])
        self.play(FadeOut(v, run_time=0.6), FadeIn(marks, run_time=0.9),
                  FadeIn(hand, run_time=0.6), run_time=1.2)                 # 2.2
        self.wait(2.8)                                                      # 5.0

        LX = 0.40
        def line(txt, y, fs=24, col=INK):
            t = Body(txt, font_size=fs, color=col)
            t.move_to([LX, y, 0], aligned_edge=LEFT)
            return t

        l1 = line("312 genomes sequenced by this project.", 1.84, 25, TEAL_TXT)
        self.play(FadeIn(l1, run_time=0.8), run_time=0.8)                   # 5.8
        self.wait(3.2)                                                      # 9.0
        l2 = line("276 enter the analysed set.", 1.22)
        self.play(FadeIn(l2, run_time=0.8), run_time=0.8)                   # 9.8
        self.wait(3.2)                                                      # 13.0
        l3 = line("They land in 56 of the 85 units.", 0.60)
        self.play(FadeIn(l3, run_time=0.8), run_time=0.8)                   # 13.8
        self.wait(3.2)                                                      # 17.0
        l4 = line("34 of the 47 in-window units hold one.", -0.02)
        self.play(FadeIn(l4, run_time=0.8), run_time=0.8)                   # 17.8
        self.wait(3.2)                                                      # 21.0
        l5 = line("Ten of those exist only because of them.", -0.64, 24, TEAL_TXT)
        self.play(FadeIn(l5, run_time=0.8), run_time=0.8)                   # 21.8
        self.wait(3.2)                                                      # 25.0

        rm = Body("Median r over m across those units is 7.74, against 7.70 in-window overall.",
                  font_size=22, color=INK).move_to([0, -1.20, 0])
        self.play(FadeIn(rm, run_time=0.9), run_time=0.9)                   # 25.9
        self.wait(3.1)                                                      # 29.0

        no = Body("The 36 that did not enter have lineages too rare for a unit to form.",
                  font_size=22, color=SRCGRAY)
        no.move_to([0, -1.72, 0])
        self.play(FadeIn(no, run_time=0.9), run_time=0.9)                   # 29.9
        self.wait(3.1)                                                      # 33.0

        end = Body("What moves the ceiling is references\n"
                   "in the right lineages, not more volume.",
                   font_size=24, color=TEAL_TXT, line_spacing=0.85)
        end.move_to([0, -2.36, 0])
        self.play(FadeIn(end, run_time=0.8), run_time=0.8)                  # 33.8
        self.wait(2.2)                                                      # 36.0
        self.wait(4.0)                                                      # 40.0
