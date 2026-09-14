#!/usr/bin/env python3
"""
Bridge the narration SRTs to a voice engine, per cue.

Extracts one text file per cue in cue order, then writes two ready-to-run
synthesis drivers, one for macOS `say` and one for ElevenLabs. Both write their
audio where make_narrated_videos_bp.py expects it.

  voice/<clip>/01.txt ... NN.txt   the line text, in cue order
  voice/say_macos.sh               run on the Mac, no API key, no network
  voice/elevenlabs.py              run anywhere, needs ELEVENLABS_API_KEY

TEXT COMES FROM THE .srt, NOT THE .vtt. The SRT carries the phonetic spellings
the pack wrote for a voice engine, "I.Q. Tree", "racks M L", "rapid N J". Those
are what should be spoken. The .vtt carries the written tool names, because
captions are read by eye. Do not synthesize from the VTT.

  python3 make_voice_lines_bp.py
"""

import os
import re
import sys

B = os.path.dirname(os.path.abspath(__file__))
ANIMO = os.path.expanduser("~/Downloads/ANIMO_DELIVERABLES_2026-09-09")
NAR = f"{ANIMO}/narration"
VOICE = f"{B}/voice"

BASES = ["7.01_negative_control", "7.03_detection_window",
         "7.07_recursive_subdivision", "7.09_tree_builder_paired",
         "7.12_outbreak_threshold"]

# The pack is timed at this rate. macOS `say` takes words per minute directly,
# so the timings and the engine agree exactly. Most cloud engines do not expose
# a rate, which is why --check exists.
WPM = 132


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
        text = " ".join(lines[lines.index(tl[0]) + 1:]).strip()
        if not text:
            sys.exit(f"FATAL: empty cue text in {path}")
        cues.append((a, z, text))
    if not cues:
        sys.exit(f"FATAL: no cues in {path}")
    return cues


def main():
    if not os.path.isdir(NAR):
        sys.exit(f"FATAL: {NAR} not found.")
    os.makedirs(VOICE, exist_ok=True)

    total = 0
    counts = {}
    for base in BASES:
        srt = f"{NAR}/{base}.srt"
        if not os.path.isfile(srt):
            sys.exit(f"FATAL: {srt} not found.")
        cues = parse_srt(srt)
        d = f"{VOICE}/{base}"
        os.makedirs(d, exist_ok=True)
        for n, (a, z, text) in enumerate(cues, 1):
            with open(f"{d}/{n:02d}.txt", "w", encoding="utf-8") as fh:
                fh.write(text + "\n")
        counts[base] = len(cues)
        total += len(cues)
        print(f"  {base:28s} {len(cues):2d} lines")

    if total != 46:
        sys.exit(f"FATAL: extracted {total} lines, expected 46.")

    write_say(counts)
    write_eleven(counts)
    print(f"\nwrote {total} line files, plus voice/say_macos.sh and "
          f"voice/elevenlabs.py")
    print("Then: python3 make_narrated_videos_bp.py --check")


def write_say(counts):
    p = f"{VOICE}/say_macos.sh"
    lines = [
        "#!/bin/bash",
        "# Synthesize every narration line with the macOS built-in voice.",
        "# No API key, no network, no cost. Run this ON THE MAC, in voice/.",
        "#",
        "# Pick a voice first:   say -v '?'",
        "# Better voices install under System Settings > Accessibility >",
        "# Spoken Content > System Voice > Manage Voices. Premium ones are",
        "# a large improvement over the defaults.",
        "#",
        "# -r 132 matches the rate the narration pack was timed at, so the",
        "# lines should land close to their slots on the first try.",
        "set -euo pipefail",
        "",
        'VOICE_NAME="${1:-Samantha}"',
        f'RATE="${{2:-{WPM}}}"',
        'echo "voice=$VOICE_NAME rate=$RATE wpm"',
        "",
        'for d in */ ; do',
        '  d="${d%/}"',
        '  [ -d "$d" ] || continue',
        '  for t in "$d"/*.txt ; do',
        '    [ -e "$t" ] || continue',
        '    out="${t%.txt}.aiff"',
        '    say -v "$VOICE_NAME" -r "$RATE" -o "$out" -f "$t"',
        '    echo "  $out"',
        '  done',
        'done',
        "",
        'echo "done. Now run: python3 make_narrated_videos_bp.py --check"',
        "",
    ]
    open(p, "w").write("\n".join(lines))
    os.chmod(p, 0o755)


def write_eleven(counts):
    p = f"{VOICE}/elevenlabs.py"
    src = '''#!/usr/bin/env python3
"""
Synthesize every narration line with ElevenLabs, one file per cue.

  export ELEVENLABS_API_KEY=...
  python3 elevenlabs.py                      # default voice
  python3 elevenlabs.py --voice-id <id>      # pick a voice
  python3 elevenlabs.py --speed 0.95         # slow down if lines overrun

Writes NN.mp3 beside each NN.txt. Skips any line already synthesized, so a
re-run only fills gaps and you can safely redo a single line by deleting it.

ElevenLabs does not take words per minute, so lines will not land exactly on
the pack's 132 wpm timing. That is expected. Run
  python3 make_narrated_videos_bp.py --check
afterward and fix only the lines it names.
"""
import os, sys, glob, json, urllib.request

KEY = os.environ.get("ELEVENLABS_API_KEY")
if not KEY:
    sys.exit("set ELEVENLABS_API_KEY first")

args = sys.argv[1:]
def opt(flag, default):
    return args[args.index(flag) + 1] if flag in args else default

VOICE_ID = opt("--voice-id", "21m00Tcm4TlvDq8ikWAM")   # Rachel, a safe default
MODEL    = opt("--model", "eleven_multilingual_v2")
SPEED    = float(opt("--speed", "1.0"))

settings = {"stability": 0.5, "similarity_boost": 0.75}
if SPEED != 1.0:
    settings["speed"] = SPEED     # supported on newer models; harmless if not

made = skipped = 0
for txt in sorted(glob.glob("*/*.txt")):
    out = txt[:-4] + ".mp3"
    if os.path.exists(out):
        skipped += 1
        continue
    text = open(txt, encoding="utf-8").read().strip()
    body = json.dumps({"text": text, "model_id": MODEL,
                       "voice_settings": settings}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        "?output_format=mp3_44100_128",
        data=body,
        headers={"xi-api-key": KEY, "Content-Type": "application/json",
                 "Accept": "audio/mpeg"})
    try:
        with urllib.request.urlopen(req) as r:
            open(out, "wb").write(r.read())
    except Exception as e:
        sys.exit(f"failed on {txt}: {e}")
    made += 1
    print(f"  {out}")

print(f"\\n{made} synthesized, {skipped} already present")
print("Now run: python3 make_narrated_videos_bp.py --check")
'''
    open(p, "w").write(src)
    os.chmod(p, 0o755)


if __name__ == "__main__":
    main()
