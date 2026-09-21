#!/usr/bin/env python3
"""
Move a rendered part from the white page to the pale page, without its source.

Why this exists. `Act4NotSeparable.mp4` is 51.0 s of clip 4 and has no source:
not in `tuc_legacy_scenes_merged.py`, not in `tuc_clip4_scenes.py` beyond a
comment, and `git log --all -S "class Act4NotSeparable"` over the whole history
returns nothing. It is the only orphan among the 34 delivered parts. Without it
clip 4 cannot follow a series-wide palette change, which blocks the change for
the whole series.

This re-colours the rendered pixels instead. **Re-rendering from source is
always better.** Use this only for a part whose source is genuinely gone.

WHAT IT DOES

Two colours move and nothing else:

    page   #FFFFFF -> #F0F4F5
    band   #E2E9EC -> #D7DEE1      (GRIDGRAY / RULE, the shaded zones)

Everything darker is left alone: the inks, the teal, the rust, the purple. The
lightest colour that must NOT move is TEAL_LT #A3CCCC = (163,204,204), and the
band is (226,233,236), so per channel there is a 63- and 29-level gap to put a
knee in.

HOW IT WAS VALIDATED, and how well it works

Two legacy parts exist rendered BOTH ways, from the clip 3 palette work, which
gives exact ground truth. Applying this to the white render of
`RecursiveSubdivision` and comparing against the true pale render:

    mean absolute per-channel error   0.33 / 255
    pixels exactly right              87.0 %
    page white -> #F0F4F5             exact
    band gray  -> off by 1 level      (h264 quantization, not the curve)
    teal ink                          unchanged, as required

Residual error is 0.74 % of pixels off by more than 10 levels, and 69 % of
those sit on anti-aliased glyph edges where a blend toward white becomes a
blend toward pale. That part is unavoidable without the source.

THE ONE REAL LIMITATION

A per-pixel curve cannot know an element's opacity, so anything drawn
*translucent over the page* lands wrong: its composite changes when the page
changes, and the curve sees only the result. In `RecursiveSubdivision` a teal
fill at partial opacity, #78B8C0, should become #6CB4BC and stays put, a
12-level error on one channel over 0.03 % of the frame.

`Act4NotSeparable` is 93 % page, then the band, opaque purple #9960A7, and the
inks. Its sampled palette contains no translucent fill, so it should do better
than the validation scene rather than worse. Check any new target the same way
before trusting this.

WHY THE CURVE HAS SO MANY CONTROL POINTS

ffmpeg's `curves` fits a natural cubic spline, so two points do not give a
straight line between them. With only a knee and the two mapped points the
spline bulged through the midtones and lifted teal ink #006D77 to #008990. The
identity anchors below the knee are what hold it flat.

  python3 shift_page_color.py --in PART.mp4 --out OUT.mp4
  python3 shift_page_color.py --in PART.mp4 --print-filter
"""
import argparse
import os
import subprocess
import sys
from shutil import which

# knee: below this a channel is untouched. TEAL_LT sits at (163,204,204).
KNEE = {"r": 200, "g": 215, "b": 215}
# (input, output) for the two page colours, per channel
MAP = {
    "r": [(226, 215), (255, 240)],
    "g": [(233, 222), (255, 244)],
    "b": [(236, 225), (255, 245)],
}
ANCHOR_STEP = 24


def curve_for(ch):
    k = KNEE[ch]
    pts = [(v, v) for v in range(0, k, ANCHOR_STEP)] + [(k, k)] + MAP[ch]
    return " ".join("%.4f/%.4f" % (i / 255.0, o / 255.0) for i, o in pts)


def filter_string():
    return "curves=r='%s':g='%s':b='%s'" % (curve_for("r"), curve_for("g"),
                                            curve_for("b"))


def probe(path, entries, stream=None):
    cmd = ["ffprobe", "-v", "error"]
    if stream:
        cmd += ["-select_streams", stream]
    cmd += ["-show_entries", entries, "-of", "csv=p=0", path]
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="out")
    ap.add_argument("--print-filter", action="store_true")
    ap.add_argument("--crf", default="16",
                    help="x264 quality. This is a re-encode of an already lossy "
                         "part, so keep it high (default 16)")
    a = ap.parse_args()

    if a.print_filter:
        print(filter_string())
        return
    if not a.out:
        sys.exit("FATAL: --out is required unless --print-filter is given.")
    if not which("ffmpeg"):
        sys.exit("FATAL: ffmpeg not on PATH.")
    if not os.path.isfile(a.inp):
        sys.exit("FATAL: %s not found." % a.inp)

    name = os.path.basename(a.inp)
    src_frames = probe(a.inp, "stream=nb_frames", "v:0")
    src_dur = float(probe(a.inp, "format=duration"))
    has_audio = bool(probe(a.inp, "stream=codec_name", "a:0"))
    print("%s: %s frames, %.3f s, audio %s"
          % (name, src_frames, src_dur, "yes" if has_audio else "no"))

    cmd = ["ffmpeg", "-y", "-v", "error", "-i", a.inp,
           "-vf", filter_string(),
           "-c:v", "libx264", "-crf", a.crf, "-preset", "slow",
           "-pix_fmt", "yuv420p"]
    cmd += ["-c:a", "copy"] if has_audio else ["-an"]
    cmd += [a.out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FATAL: ffmpeg failed\n%s" % r.stderr[:600])

    out_frames = probe(a.out, "stream=nb_frames", "v:0")
    out_dur = float(probe(a.out, "format=duration"))
    problems = []
    if out_frames != src_frames:
        problems.append("frame count %s -> %s" % (src_frames, out_frames))
    if abs(out_dur - src_dur) > 0.02:
        problems.append("duration %.3f -> %.3f" % (src_dur, out_dur))
    print("wrote %s: %s frames, %.3f s" % (a.out, out_frames, out_dur))
    if problems:
        print("FAILED:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("verified: length unchanged. The video was re-encoded, so it is NOT "
          "bit-identical; that is inherent to re-colouring without the source.")


if __name__ == "__main__":
    main()
