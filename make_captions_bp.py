#!/usr/bin/env python3
"""
Build captions for the five Animo animations from the narration SRTs.

Two outputs, because they serve different players:

  narration/vtt/<base>.vtt        WebVTT, for the HTML <track> element. This is
                                  what a browser actually renders.
  video_captioned/<base>.mp4      the same video with a soft mov_text subtitle
                                  track, for VLC, QuickTime and downloads. A
                                  browser will NOT render mov_text, which is why
                                  the VTT exists separately.

FIXES THE DURATION OFFSET. Every narration .md assumes a clip 0.2 to 0.4 s longer
than the actual MP4, so the last cue can end past the final frame (7.09 ends at
26.93 against a 26.80 s clip). Cue ends are probed against the real container
duration and clamped, and the script reports every clamp it makes.

Fails rather than writing on a missing file, an overlapping pair of cues, or a
cue that starts after the video ends.

  python3 make_captions_bp.py
"""

import os
import re
import shutil
import subprocess
import sys

B = os.path.dirname(os.path.abspath(__file__))
ANIMO = os.path.expanduser("~/Downloads/ANIMO_DELIVERABLES_2026-09-09")
VID = f"{ANIMO}/video"
NAR = f"{ANIMO}/narration"
VTT = f"{NAR}/vtt"
OUTV = f"{B}/video_captioned"

BASES = ["7.01_negative_control", "7.03_detection_window",
         "7.07_recursive_subdivision", "7.09_tree_builder_paired",
         "7.12_outbreak_threshold"]

# The SRT does double duty: input to a voice engine, and source for captions.
# Those want opposite spellings. The phonetic forms exist so an engine does not
# say "eye kew dash tree", but a caption is read by eye and must show the real
# tool name. Restored for captions only. The .srt and .txt are left untouched so
# they remain correct as synthesis input. Mapping is from the narration .md files.
SAY_TO_WRITTEN = {
    "I.Q. Tree": "IQ-TREE",
    "racks M L": "RAxML",
    "rapid N J": "rapidnj",
}


def to_written(text):
    for say, written in SAY_TO_WRITTEN.items():
        text = text.replace(say, written)
    return text


def need(path):
    if not os.path.exists(path):
        sys.exit(f"FATAL: {path} not found.")
    return path


def probe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def t2s(t):
    h, m, rest = t.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def s2vtt(x):
    h = int(x // 3600); m = int((x % 3600) // 60)
    s = x - h * 3600 - m * 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def parse_srt(path):
    cues = []
    for block in re.split(r"\n\s*\n", open(path, encoding="utf-8").read().strip()):
        lines = [l for l in block.strip().split("\n") if l.strip()]
        tl = [l for l in lines if "-->" in l]
        if not tl:
            continue
        a, z = [t2s(x.strip()) for x in tl[0].split("-->")]
        text = " ".join(lines[lines.index(tl[0]) + 1:]).strip()
        if not text:
            sys.exit(f"FATAL: empty cue text in {path}")
        cues.append([a, z, text])
    if not cues:
        sys.exit(f"FATAL: no cues parsed from {path}")
    return cues


def main():
    for p in (VID, NAR):
        need(p)
    if shutil.which("ffmpeg") is None:
        sys.exit("FATAL: ffmpeg not on PATH.")
    os.makedirs(VTT, exist_ok=True)
    os.makedirs(OUTV, exist_ok=True)

    total_cues = 0
    for base in BASES:
        mp4 = need(f"{VID}/{base}.mp4")
        srt = need(f"{NAR}/{base}.srt")
        dur = probe_duration(mp4)
        cues = parse_srt(srt)

        for i in range(1, len(cues)):
            if cues[i][0] < cues[i - 1][1] - 1e-9:
                sys.exit(f"FATAL: {base} cue {i+1} starts before cue {i} ends.")
        if cues[0][0] < 0:
            sys.exit(f"FATAL: {base} first cue starts before zero.")
        if cues[0][0] >= dur:
            sys.exit(f"FATAL: {base} first cue starts after the video ends.")

        clamped = 0
        for c in cues:
            if c[1] > dur:
                c[1] = round(dur, 3)
                clamped += 1
            if c[0] >= c[1]:
                sys.exit(f"FATAL: {base} cue collapsed to zero length after clamp.")

        restored = 0
        for c in cues:
            w = to_written(c[2])
            if w != c[2]:
                restored += 1
            c[2] = w

        with open(f"{VTT}/{base}.vtt", "w", encoding="utf-8") as fh:
            fh.write("WEBVTT\n\n")
            for n, (a, z, t) in enumerate(cues, 1):
                fh.write(f"{n}\n{s2vtt(a)} --> {s2vtt(z)}\n{t}\n\n")

        # Mux from a corrected copy, not the raw .srt, so the desktop subtitle
        # track carries the written forms and the clamped end times too.
        cap_srt = f"{VTT}/{base}.captions.srt"
        with open(cap_srt, "w", encoding="utf-8") as fh:
            for n, (a, z, t) in enumerate(cues, 1):
                fh.write(f"{n}\n{s2vtt(a).replace('.', ',')} --> "
                         f"{s2vtt(z).replace('.', ',')}\n{t}\n\n")

        out = f"{OUTV}/{base}.mp4"
        r = subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", mp4, "-i", cap_srt,
             "-map", "0:v", "-map", "1:0", "-c:v", "copy",
             "-c:s", "mov_text", "-metadata:s:s:0", "language=eng",
             "-metadata:s:s:0", "title=Narration", out],
            capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"FATAL: ffmpeg failed on {base}:\n{r.stderr.strip()[:400]}")

        total_cues += len(cues)
        bits = []
        if clamped:
            bits.append(f"{clamped} cue end clamped to {dur:.3f}s")
        if restored:
            bits.append(f"{restored} tool name restored to written form")
        note = ", " + ", ".join(bits) if bits else ""
        print(f"  {base:28s} {len(cues):2d} cues, {dur:6.3f}s{note}")

    if total_cues < 40:
        sys.exit(f"FATAL: only {total_cues} cues across all clips, expected 46.")
    print(f"\nwrote {VTT}/ and {OUTV}/  ({total_cues} cues total)")


if __name__ == "__main__":
    main()
