#!/usr/bin/env python3
"""
Lay synthesized narration onto the silent Animo clips. Engine agnostic.

You supply one audio file per SRT cue. This places each at its absolute in time
on a silent bed cut to the clip's REAL probed duration, then muxes with the video
stream copied. Nothing is time stretched and the video is never re-encoded.

WHY PER LINE RATHER THAN ONE PASS. Engines vary their rate, especially around
numbers, so a single render drifts away from the animation. The SRT in times are
absolute against the start of each MP4, so placing line by line keeps every line
on the beat it describes.

  voice/<base>/01.wav, 02.wav, ...   one file per cue, in cue order
                                     any ffmpeg-readable format works

  python3 make_narrated_videos_bp.py            # build
  python3 make_narrated_videos_bp.py --check    # report fit, write nothing
  python3 make_narrated_videos_bp.py --force    # build despite overruns

FAILS LOUD ON OVERRUN. If a spoken line is longer than the gap before the next
cue, the two would talk over each other. That is reported per line and refused,
because the fix is to re-synthesize that line or slow the clip, not to let the
mix hide it. --force proceeds and lets them overlap.

Reads the durations from the files, which also corrects the 0.2 to 0.4 s that the
narration .md files assume over the real clips.
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
VOICE = f"{B}/voice"
OUT = f"{B}/video_narrated"

BASES = ["7.01_negative_control", "7.03_detection_window",
         "7.07_recursive_subdivision", "7.09_tree_builder_paired",
         "7.12_outbreak_threshold"]

# .aiff is first because macOS `say` writes AIFF by default. ffmpeg reads it.
AUDIO_EXT = (".aiff", ".aif", ".wav", ".mp3", ".m4a", ".flac", ".ogg",
             ".opus", ".aac")
CHECK = "--check" in sys.argv
FORCE = "--force" in sys.argv


def probe(path, entries):
    return subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", entries,
         "-of", "csv=p=0", path],
        capture_output=True, text=True, check=True).stdout.strip()


def t2s(t):
    h, m, rest = t.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def parse_srt(path):
    cues = []
    for block in re.split(r"\n\s*\n", open(path, encoding="utf-8").read().strip()):
        lines = [l for l in block.strip().split("\n") if l.strip()]
        tl = [l for l in lines if "-->" in l]
        if not tl:
            continue
        a, z = [t2s(x.strip()) for x in tl[0].split("-->")]
        cues.append((a, z, " ".join(lines[lines.index(tl[0]) + 1:]).strip()))
    return cues


def voice_files(base, n_cues):
    d = f"{VOICE}/{base}"
    if not os.path.isdir(d):
        return None
    files = sorted(f for f in os.listdir(d) if f.lower().endswith(AUDIO_EXT))
    if not files:
        return None
    if len(files) != n_cues:
        sys.exit(f"FATAL: {base} has {len(files)} audio files for {n_cues} cues. "
                 f"Name them in cue order, for example 01.wav to "
                 f"{n_cues:02d}.wav.")
    return [os.path.join(d, f) for f in files]


def main():
    if shutil.which("ffmpeg") is None:
        sys.exit("FATAL: ffmpeg not on PATH.")
    for p in (VID, NAR):
        if not os.path.isdir(p):
            sys.exit(f"FATAL: {p} not found.")
    os.makedirs(OUT, exist_ok=True)

    built = skipped = 0
    problems = []

    for base in BASES:
        mp4, srt = f"{VID}/{base}.mp4", f"{NAR}/{base}.srt"
        for p in (mp4, srt):
            if not os.path.isfile(p):
                sys.exit(f"FATAL: {p} not found.")
        vdur = float(probe(mp4, "format=duration"))
        cues = parse_srt(srt)
        if not cues:
            sys.exit(f"FATAL: no cues in {srt}")

        wavs = voice_files(base, len(cues))
        if wavs is None:
            print(f"  {base:28s} no audio in voice/{base}/, skipped")
            skipped += 1
            continue

        # Fit report: does each spoken line finish before the next one starts?
        overruns = []
        for i, (a, _z, text) in enumerate(cues):
            adur = float(probe(wavs[i], "format=duration"))
            limit = (cues[i + 1][0] - a) if i + 1 < len(cues) else (vdur - a)
            if adur > limit + 1e-3:
                overruns.append((i + 1, adur, limit, text[:44]))
        if overruns:
            problems.append((base, overruns))
            for n, adur, limit, text in overruns:
                print(f"  OVERRUN {base} cue {n}: {adur:.2f}s spoken into a "
                      f"{limit:.2f}s slot  \"{text}\"")
            if not FORCE:
                continue

        if CHECK:
            print(f"  {base:28s} {len(cues)} cues fit, video {vdur:.3f}s")
            continue

        # One silent bed at the real duration, each line delayed to its in time.
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", mp4]
        for w in wavs:
            cmd += ["-i", w]
        parts, labels = [], []
        for i, (a, _z, _t) in enumerate(cues):
            ms = int(round(a * 1000))
            parts.append(f"[{i+1}:a]aresample=48000,adelay={ms}|{ms}[a{i}]")
            labels.append(f"[a{i}]")
        parts.append(
            "".join(labels) +
            f"amix=inputs={len(cues)}:normalize=0:dropout_transition=0,"
            f"apad,atrim=0:{vdur:.6f},asetpts=N/SR/TB[aout]")
        cmd += ["-filter_complex", ";".join(parts),
                "-map", "0:v", "-map", "[aout]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                "-shortest", f"{OUT}/{base}.mp4"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"FATAL: ffmpeg failed on {base}:\n{r.stderr.strip()[:600]}")

        got = float(probe(f"{OUT}/{base}.mp4", "format=duration"))
        if abs(got - vdur) > 0.15:
            sys.exit(f"FATAL: {base} output is {got:.3f}s against a {vdur:.3f}s "
                     "source. Audio changed the length.")
        print(f"  {base:28s} narrated, {len(cues)} lines, {got:.3f}s")
        built += 1

    print()
    if problems and not FORCE:
        print(f"REFUSED {len(problems)} clip(s) with overrunning lines. "
              "Re-synthesize those lines shorter, or pass --force to let them "
              "overlap.")
    if CHECK:
        print("check only, nothing written")
    elif built:
        print(f"wrote {built} narrated clip(s) to {OUT}/")
        print("Re-embed with: python3 make_virtual_manuscript_video_bp.py "
              "(point VID at video_narrated/ first)")
    if not built and not CHECK and skipped == len(BASES):
        print(f"Nothing to do. Put one audio file per cue in {VOICE}/<clip>/ "
              "named in cue order, then run again.")


if __name__ == "__main__":
    main()
