#!/usr/bin/env python3
"""
Build VIRTUAL_MANUSCRIPT_VIDEO.html from VIRTUAL_MANUSCRIPT.html plus the five
Animo animations, embedded as base64 data URIs.

The non-video deliverable is hand-authored source and has no generator. This
script is the generator for the video edition ONLY. It leaves the interactive
file untouched and writes a separate output, so the lean file stays the primary
deliverable. Each video uses its own still as the poster, so every section shows
a complete final frame before play.

Fails rather than writing if any marker is not unique or any asset is missing, so
the build cannot silently drop a video or inject one in the wrong place.

  python3 make_virtual_manuscript_video_bp.py
"""

import base64
import os
import sys

B = os.path.dirname(os.path.abspath(__file__))
SRC = f"{B}/VIRTUAL_MANUSCRIPT.html"
OUT = f"{B}/VIRTUAL_MANUSCRIPT_VIDEO.html"
ANIMO = os.path.expanduser("~/Downloads/ANIMO_DELIVERABLES_2026-09-09")
# --narrated swaps in the voiced clips from make_narrated_videos_bp.py without
# anyone having to edit this file. Posters and captions are unchanged either way,
# because narration does not alter a frame.
NARRATED = "--narrated" in sys.argv
VID = f"{B}/video_narrated" if NARRATED else f"{ANIMO}/video"
STL = f"{ANIMO}/stills"
VTT = f"{ANIMO}/narration/vtt"

# key -> (mp4 basename, still basename, caption, insert-before marker)
SPECS = {
 "neg": ("7.01_negative_control", "7.01_negative_control",
   "Rendered animation, 42 seconds. The negative control, drawn as a zoom-out "
   "because the 427x to 2,234x separation cannot be shown to scale on one static axis.",
   '  <div class="callout def">\n    <strong>How the negative control was built.</strong>'),
 "win": ("7.03_detection_window", "7.03_detection_window",
   "Rendered animation, 48 seconds. One continuous sweep across group diversity, "
   "with the imported piece held fixed and only the background changing.",
   '  <p>\n    The middle case is the one everybody pictures.'),
 "split": ("7.07_recursive_subdivision", "7.07_recursive_subdivision",
   "Rendered animation, 35 seconds. One real group of 153 dividing into 98, 47 "
   "and 8, with two of the three children landing below the floor.",
   '  <p>\n    The division itself was correct, because the evidence'),
 "tree": ("7.09_tree_builder_paired", "7.09_tree_builder_paired",
   "Rendered animation, 27 seconds. Twelve paired comparisons per builder. The "
   "two maximum-likelihood builders agree, the distance-based one is consistently lower.",
   '  <p>\n    The third row is the one that identifies the cause.'),
 "outbreak": ("7.12_outbreak_threshold", "7.12_outbreak_threshold",
   "Rendered animation, 45 seconds. Recombination as a share of SNP distance "
   "against how much of it the filter detects, with the outbreak decision band "
   "where the two diverge. Curves are schematic and no threshold is proposed.",
   '  <div class="callout warn">\n    <strong>Why this reaches the bench and the outbreak call.</strong>'),
}

CSS = (
  "\n/* video edition: embedded rendered animations */\n"
  ".vfig{margin:26px 0}\n"
  ".vid{width:100%;height:auto;display:block;border:1px solid var(--rule);"
  "border-radius:12px;background:var(--plate);box-shadow:var(--shadow)}\n"
  ".vcap{font-family:\"IBM Plex Mono\",monospace;font-size:12px;line-height:1.5;"
  "color:var(--muted);margin:0 0 9px}\n"
)
OLD_TITLE = "<title>The Detection Window</title>"
NEW_TITLE = "<title>The Detection Window, Video Edition</title>"


def b64(path):
    if not os.path.isfile(path):
        sys.exit(f"FATAL: asset not found: {path}")
    with open(path, "rb") as fh:
        return base64.b64encode(fh.read()).decode("ascii")


def figure(mp4, still, cap):
    v = b64(f"{VID}/{mp4}.mp4")
    p = b64(f"{STL}/{still}.png")
    # Captions are inlined as a data: URI too, so the file stays self-contained.
    # A browser renders WebVTT via <track>; it will NOT render the mov_text track
    # that make_captions_bp.py muxes into video_captioned/ for desktop players.
    t = b64(f"{VTT}/{mp4}.vtt")
    return (
      '  <figure class="vfig wide">\n'
      f'    <figcaption class="vcap">{cap}</figcaption>\n'
      '    <video class="vid" controls preload="none" playsinline '
      f'poster="data:image/png;base64,{p}">\n'
      f'      <source src="data:video/mp4;base64,{v}" type="video/mp4">\n'
      '      <track kind="captions" srclang="en" label="Narration" default '
      f'src="data:text/vtt;base64,{t}">\n'
      '      Your browser cannot play embedded video. The final frame is shown '
      'above as the poster.\n'
      '    </video>\n'
      '  </figure>\n'
    )


def main():
    if not os.path.isfile(SRC):
        sys.exit(f"FATAL: {SRC} not found.")
    if NARRATED:
        missing = [k for k, (m, _s, _c, _mk) in SPECS.items()
                   if not os.path.isfile(f"{VID}/{m}.mp4")]
        if missing:
            sys.exit(f"FATAL: --narrated given but {VID} is missing clips for "
                     f"{', '.join(sorted(missing))}. Run "
                     "make_narrated_videos_bp.py first.")
        print("  using narrated clips from video_narrated/")
    html = open(SRC, encoding="utf-8").read()

    if html.count("</style>") < 1:
        sys.exit("FATAL: no </style> to inject CSS before.")
    html = html.replace("</style>", CSS + "</style>", 1)

    if OLD_TITLE not in html:
        sys.exit(f"FATAL: title not found: {OLD_TITLE}")
    html = html.replace(OLD_TITLE, NEW_TITLE, 1)

    for key, (mp4, still, cap, marker) in SPECS.items():
        n = html.count(marker)
        if n != 1:
            sys.exit(f"FATAL: marker for {key} occurs {n} times, expected 1.")
        html = html.replace(marker, figure(mp4, still, cap) + "\n" + marker, 1)

    if html.count("<video") != len(SPECS):
        sys.exit(f"FATAL: {html.count('<video')} video elements, expected {len(SPECS)}.")
    if html.count("<track kind=\"captions\"") != len(SPECS):
        sys.exit(f"FATAL: {html.count('<track kind=')} caption tracks, "
                 f"expected {len(SPECS)}.")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"wrote {OUT}  {os.path.getsize(OUT)/1024/1024:.1f} MB"
          f"{'  (narrated)' if NARRATED else '  (silent)'}")
    print(f"  {html.count('<video')} videos, "
          f"{html.count('poster=\"data:image/png')} posters, "
          f"{html.count('<track kind=')} caption tracks, all markers unique")


if __name__ == "__main__":
    main()
