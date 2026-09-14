#!/usr/bin/env python3
"""
Stage a transfer folder for redesigning the video edition with Claude Design.

The delivered video edition inlines the five MP4s as base64, which is hostile to
editing. This folder instead references the videos as files, so the HTML stays
small and a design tool and a human can both work on it. A re-embed tool is
included to fold the videos back into a single offline file after the redesign.

Every file here is aggregate or a rendered figure. No isolate-level table is
included, and the build audits its own output and fails on any genome accession
outside the four public run IDs already allowed, or any restricted column.

  python3 stage_for_claude_design_bp.py
"""

import base64
import csv
import hashlib
import os
import re
import shutil
import sys

B = os.path.dirname(os.path.abspath(__file__))
SRC = f"{B}/VIRTUAL_MANUSCRIPT.html"
ANIMO = os.path.expanduser("~/Downloads/ANIMO_DELIVERABLES_2026-09-09")
OUT = f"{B}/CLAUDE_DESIGN_STAGING_2026-09-09"

ALLOWED_ACCESSIONS = {"SRR2896257", "SRR2896259", "SRR2896271", "ERR9980356"}
ACC = re.compile(r"\b(?:GCF|GCA|SRR|ERR|DRR)[_0-9]{6,}")
RESTRICTED = re.compile(r"exposure_country|isolation_location|validation_label", re.I)

# key -> (basename, caption, insert-before marker)
SPECS = {
 "neg": ("7.01_negative_control",
   "Rendered animation, 42 seconds. The negative control, drawn as a zoom-out "
   "because the 427x to 2,234x separation cannot be shown to scale on one static axis.",
   '  <div class="callout def">\n    <strong>How the negative control was built.</strong>'),
 "win": ("7.03_detection_window",
   "Rendered animation, 48 seconds. One continuous sweep across group diversity, "
   "with the imported piece held fixed and only the background changing.",
   '  <p>\n    The middle case is the one everybody pictures.'),
 "split": ("7.07_recursive_subdivision",
   "Rendered animation, 35 seconds. One real group of 153 dividing into 98, 47 "
   "and 8, with two of the three children landing below the floor.",
   '  <p>\n    The division itself was correct, because the evidence'),
 "tree": ("7.09_tree_builder_paired",
   "Rendered animation, 27 seconds. Twelve paired comparisons per builder. The "
   "two maximum-likelihood builders agree, the distance-based one is consistently lower.",
   '  <p>\n    The third row is the one that identifies the cause.'),
 "outbreak": ("7.12_outbreak_threshold",
   "Rendered animation, 45 seconds. Recombination as a share of SNP distance "
   "against how much of it the filter detects, with the outbreak decision band "
   "where the two diverge. Curves are schematic and no threshold is proposed.",
   '  <div class="callout warn">\n    <strong>Why this reaches the bench and the outbreak call.</strong>'),
}

CSS = (
  "\n/* video edition: rendered animations referenced as files */\n"
  ".vfig{margin:26px 0}\n"
  ".vid{width:100%;height:auto;display:block;border:1px solid var(--rule);"
  "border-radius:12px;background:var(--plate);box-shadow:var(--shadow)}\n"
  ".vcap{font-family:\"IBM Plex Mono\",monospace;font-size:12px;line-height:1.5;"
  "color:var(--muted);margin:0 0 9px}\n"
)


def ref_figure(base, cap):
    return (
      '  <figure class="vfig wide">\n'
      f'    <figcaption class="vcap">{cap}</figcaption>\n'
      '    <video class="vid" controls preload="metadata" playsinline '
      f'poster="stills/{base}.png">\n'
      f'      <source src="video/{base}.mp4" type="video/mp4">\n'
      '      Your browser cannot play video. The final frame is in stills/.\n'
      '    </video>\n'
      '  </figure>\n'
    )


def build_html():
    html = open(SRC, encoding="utf-8").read()
    html = html.replace("</style>", CSS + "</style>", 1)
    html = html.replace("<title>The Detection Window</title>",
                        "<title>The Detection Window, Video Edition, work copy</title>", 1)
    for key, (base, cap, marker) in SPECS.items():
        if html.count(marker) != 1:
            sys.exit(f"FATAL: marker for {key} occurs {html.count(marker)} times.")
        html = html.replace(marker, ref_figure(base, cap) + "\n" + marker, 1)
    if html.count("<video") != len(SPECS):
        sys.exit("FATAL: wrong video count after injection.")
    return html


def main():
    for p in (SRC, f"{ANIMO}/video", f"{ANIMO}/stills"):
        if not os.path.exists(p):
            sys.exit(f"FATAL: {p} not found.")
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(f"{OUT}/video")
    os.makedirs(f"{OUT}/stills")
    os.makedirs(f"{OUT}/design")
    os.makedirs(f"{OUT}/context")

    open(f"{OUT}/virtual_manuscript_video.html", "w", encoding="utf-8").write(build_html())

    for key, (base, _c, _m) in SPECS.items():
        shutil.copy2(f"{ANIMO}/video/{base}.mp4", f"{OUT}/video/{base}.mp4")
        shutil.copy2(f"{ANIMO}/stills/{base}.png", f"{OUT}/stills/{base}.png")

    design = {
        os.path.expanduser("~/CLIP_GENERATION_STANDARD.md"):
            "CLIP_GENERATION_STANDARD.md",
        f"{ANIMO}/README.md": "design/ANIMO_STYLE_AND_SCENES.md",
        f"{ANIMO}/source/scene.py": "design/animo_scene.py",
        f"{B}/VM_HANDOFF_PACK/text/P-writing-prompt.md": "design/P-writing-prompt.md",
    }
    context = {
        f"{B}/ANIMO_BRIEF_2026-09-09.md": "context/ANIMO_BRIEF_2026-09-09.md",
        f"{B}/NUMBERS.tsv": "context/NUMBERS.tsv",
        f"{B}/TABLES.md": "context/TABLES.md",
    }
    for src, dst in {**design, **context}.items():
        if not os.path.isfile(src):
            sys.exit(f"FATAL: {src} not found.")
        shutil.copy2(src, f"{OUT}/{dst}")

    nar = f"{B}/narration_csv"
    if os.path.isdir(nar):
        os.makedirs(f"{OUT}/narration", exist_ok=True)
        for fn in sorted(os.listdir(nar)):
            if fn.endswith((".csv", ".txt", ".md")):
                shutil.copy2(f"{nar}/{fn}", f"{OUT}/narration/{fn}")

    write_embed_tool()
    write_readme()

    # Audit the built folder, not the plan.
    bad_acc, bad_field = [], []
    n_text = 0
    for root, _d, files in os.walk(OUT):
        for fn in files:
            p = os.path.join(root, fn)
            if os.path.splitext(fn)[1].lower() in (".mp4", ".png"):
                continue
            n_text += 1
            s = open(p, errors="replace").read()
            found = set(ACC.findall(s)) - ALLOWED_ACCESSIONS
            if found:
                bad_acc.append((os.path.relpath(p, OUT), sorted(found)[:3]))
            if os.path.basename(p).endswith(".tsv") and RESTRICTED.search(s.split("\n", 1)[0]):
                bad_field.append(os.path.relpath(p, OUT))
    if n_text < 8:
        sys.exit(f"FATAL: only {n_text} text files audited, expected the full set.")
    if bad_acc:
        for rel, s in bad_acc:
            print(f"  DENIED {rel}: {s}", file=sys.stderr)
        sys.exit("FATAL: staging folder carries genome accessions.")
    if bad_field:
        sys.exit(f"FATAL: restricted columns in {bad_field}.")

    rels = sorted(os.path.relpath(os.path.join(r, f), OUT)
                  for r, _d, fs in os.walk(OUT) for f in fs)
    lines = [f"{hashlib.sha256(open(f'{OUT}/{r}', 'rb').read()).hexdigest()}  {r}"
             for r in rels if r != "MANIFEST.sha256"]
    open(f"{OUT}/MANIFEST.sha256", "w").write("\n".join(lines) + "\n")

    total = sum(os.path.getsize(os.path.join(r, f))
                for r, _d, fs in os.walk(OUT) for f in fs)
    print(f"wrote {OUT}/  {total/1024/1024:.1f} MB, {len(rels)+1} files")
    print(f"  audit: 0 accessions outside the allowlist, 0 restricted columns, "
          f"{n_text} text files checked")


def write_embed_tool():
    tool = '''#!/usr/bin/env python3
"""
Fold referenced videos and posters back into one offline HTML file.

Run this AFTER the redesign, on the rebuilt HTML, to produce the single
self-contained file the presentation wants. It replaces every
  src="video/NAME.mp4"      with a base64 data: URI
  poster="stills/NAME.png"  with a base64 data: URI

  python3 embed_videos.py INPUT.html OUTPUT.html
"""
import base64, os, re, sys

def data_uri(path, mime):
    with open(path, "rb") as fh:
        return f"data:{mime};base64," + base64.b64encode(fh.read()).decode("ascii")

def main():
    if len(sys.argv) != 3:
        sys.exit("usage: python3 embed_videos.py INPUT.html OUTPUT.html")
    inp, out = sys.argv[1], sys.argv[2]
    here = os.path.dirname(os.path.abspath(inp)) or "."
    html = open(inp, encoding="utf-8").read()
    n_v = n_p = 0

    def sub_src(m):
        nonlocal n_v
        rel = m.group(1)
        p = os.path.join(here, rel)
        if not os.path.isfile(p):
            sys.exit(f"missing video: {p}")
        n_v += 1
        return f'src="{data_uri(p, "video/mp4")}"'

    def sub_poster(m):
        nonlocal n_p
        rel = m.group(1)
        p = os.path.join(here, rel)
        if not os.path.isfile(p):
            sys.exit(f"missing poster: {p}")
        n_p += 1
        return f'poster="{data_uri(p, "image/png")}"'

    html = re.sub(r'src="(video/[^"]+\\.mp4)"', sub_src, html)
    html = re.sub(r'poster="(stills/[^"]+\\.png)"', sub_poster, html)
    open(out, "w", encoding="utf-8").write(html)
    print(f"wrote {out}  {os.path.getsize(out)/1024/1024:.1f} MB, "
          f"{n_v} videos and {n_p} posters embedded")
    if n_v == 0:
        sys.exit("WARNING: embedded 0 videos. Check the src paths match video/NAME.mp4")

if __name__ == "__main__":
    main()
'''
    open(f"{OUT}/embed_videos.py", "w").write(tool)


def write_readme():
    txt = """# Redesign staging: virtual manuscript, video edition

For Claude Design on your Mac. The job is to look at the video edition, apply a
coherent design system, and rebuild it.

## Your role here is BUILDER

`CLIP_GENERATION_STANDARD.md` in this folder defines how this work is divided.
Section 2 is the ownership table. Against it:

| role | who | owns |
|---|---|---|
| concept owner | Claude Code | the content, the claims, any narration and captions |
| **builder** | **you** | **the audit, the encoding, the visual system** |
| verifier | Claude Code | checking the rebuilt artifact against the source data |

**Yours.** Auditing this brief against what is here before redesigning. Refusing
anything the content does not support. Every encoding and layout decision. The
design system itself.

**Not yours.** Changing what any figure says. Rewriting narration or captions.
Deciding that a number should be different.

**The standard's rule that matters most here.** Reserve solid, precise rendering
for measured values, and make anything schematic look schematic. The most visually
dominant object on a page should never be its least real one.

## What is here

```
virtual_manuscript_video.html   the deliverable to redesign. Videos are
                                REFERENCED as files, not inlined, so this stays
                                small and editable. Open it with video/ and
                                stills/ beside it.
video/                          the five rendered animations, 1080p60 MP4
stills/                         the final frame of each, used as the poster
design/
  ANIMO_STYLE_AND_SCENES.md     the APHL brand system the animations use:
                                colors, fonts, layout bands, style rules
  animo_scene.py                the Manim source for all five animations
  P-writing-prompt.md           the writing-style constraint. It is hard
context/
  ANIMO_BRIEF_2026-09-09.md     the science, the numbers that must not drift
                                (section 5), and the framings that are forbidden
                                (section 6). Read these two before changing text
  NUMBERS.tsv                   single source of truth for every headline number
  TABLES.md                     the generated tables
embed_videos.py                 fold the videos back into ONE offline file after
                                the redesign
```

## Two design systems are in play. That is the decision to make.

The current HTML carries its own system: IBM Plex type, a warm palette defined as
CSS custom properties at the top of the file, and full light and dark theming.
The animations carry a different one: the APHL brand in `design/`, with Franklin
Gothic and a teal-and-rust palette. Applying a design system means reconciling
these two, not layering a third on top. Pick one direction and make the page and
the videos read as one thing.

## Constraints that outrank aesthetics

- **Numbers must not drift.** Every figure on the page traces to `NUMBERS.tsv`.
  A redesign changes how things look, never what they say. If a number is unclear,
  it is in `NUMBERS.tsv` or `context/TABLES.md`, and if it is in neither it is not
  established.
- **Forbidden framings** are listed in the brief, section 6. The big ones: never
  present a low r/m as a low recombination rate, never compare a country number to
  a region number without both estimators shown, never imply prior studies were
  wrong.
- **Writing style** in `design/P-writing-prompt.md` is a hard constraint. No em
  dashes, no en dashes, no semicolons, American spelling, short sentences.
- **Offline and self-contained.** The final artifact opens offline in a browser
  with no external requests. Keep the videos local. When done, run
  `embed_videos.py` to produce the single-file version.
- **Theme-aware, if the current theming is kept.** The page reads in light and
  dark. A redesign that drops one should do so on purpose, not by accident.
- **Presenter controls.** Arrow and page keys move between sections so a remote
  works, motion is button-triggered and replayable, and reduced motion is
  respected. Keep these.

## When the redesign is done

```bash
python3 embed_videos.py virtual_manuscript_video.html virtual_manuscript_video_single.html
```

That produces the single offline file for the talk. Check the result opens by
double-click and every video plays.

## What is deliberately not here

No isolate-level data. This project works with a US Tier 1 Select Agent, and the
per-genome tables that join an accession to geography are never transferred. None
of them is needed to redesign a page. If a rebuild seems to need one, it does not,
and the answer is an aggregate already in `NUMBERS.tsv` or `TABLES.md`.
"""
    open(f"{OUT}/README.md", "w").write(txt)


if __name__ == "__main__":
    main()
