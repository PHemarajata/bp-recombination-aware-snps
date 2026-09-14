#!/usr/bin/env python3
"""
Re-time and rewrite the 7.01 narration against the animation's actual beats.

Beat times were read off the rendered MP4 by sampling frames at one second, not
inferred from the scene source. The previous script drifted: its third line
described on-screen text that had already gone, and the two null facts were
narrated three to four seconds after they appeared.

Writes narration_v2/7.01_negative_control.{csv,srt,txt}. START is the moment the
line begins. The pauses between lines are engineered and are part of the design.
"""
import csv, os, subprocess, sys

B = os.path.dirname(os.path.abspath(__file__))
ANIMO = os.path.expanduser("~/Downloads/ANIMO_DELIVERABLES_2026-09-09")
MP4 = f"{ANIMO}/video/7.01_negative_control.mp4"
OUT = f"{B}/narration_v2"
WPM = 132.0
BASE = "7.01_negative_control"

# start, text, the on-screen beat it is timed to
LINES = [
 (0.8,  "Every laboratory runs a no-template control.",
        "title, and the lab analogy appears"),
 (4.2,  "We ran the same idea on the recombination detector.",
        "simulate with zero recombination, identical pipeline"),
 (8.8,  "Almost every simulated run came back empty.",
        "the replicate count lands and the dots fill"),
 (12.4, "The few that did were vanishingly small.",
        "the largest value ever returned appears"),
 (15.8, "Now hold the axis linear and widen it.",
        "the on-screen instruction to widen the axis"),
 (20.4, "The scale stays linear the whole way. Only the width changes.",
        "the zoom begins and the readout starts climbing"),
 (26.6, "It widens until the real analysis groups appear.",
        "the real band enters the frame"),
 (30.6, "Each had its own matched simulation.",
        "the zoom completes and the band settles"),
 (34.2, "Separation is over four hundred fold.",
        "the separation headline appears"),
 (37.4, "So the tool is not inventing recombination.",
        "the closing verdict appears"),
]


def dur(text):
    return len(text.split()) / WPM * 60.0


def ts(x, sep=","):
    h = int(x // 3600); m = int((x % 3600) // 60); s = x - h*3600 - m*60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", sep)


def main():
    if not os.path.isfile(MP4):
        sys.exit(f"FATAL: {MP4} not found.")
    vdur = float(subprocess.run(
        ["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",MP4],
        capture_output=True, text=True, check=True).stdout.strip())
    os.makedirs(OUT, exist_ok=True)

    rows, speech = [], 0.0
    for i, (start, text, beat) in enumerate(LINES, 1):
        if any(ch.isdigit() for ch in text):
            sys.exit(f"FATAL: line {i} contains a digit. Spell numbers as words "
                     "so the engine paces them correctly.")
        for bad in ("—", "–", ";"):
            if bad in text:
                sys.exit(f"FATAL: line {i} contains a forbidden character.")
        d = dur(text)
        end = start + d
        nxt = LINES[i][0] if i < len(LINES) else vdur
        if end > nxt + 1e-9:
            sys.exit(f"FATAL: line {i} runs to {end:.2f}s into a slot ending "
                     f"{nxt:.2f}s. Shorten it or move the start.")
        if end > vdur:
            sys.exit(f"FATAL: line {i} runs past the {vdur:.3f}s clip.")
        speech += d
        rows.append({"clip": BASE, "line": i, "start_s": f"{start:.2f}",
                     "end_s": f"{end:.2f}", "dur_s": f"{d:.2f}",
                     "words": len(text.split()), "on_screen_beat": beat,
                     "text": text})

    with open(f"{OUT}/{BASE}.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    with open(f"{OUT}/{BASE}.srt", "w") as fh:
        for r in rows:
            fh.write(f"{r['line']}\n{ts(float(r['start_s']))} --> "
                     f"{ts(float(r['end_s']))}\n{r['text']}\n\n")
    with open(f"{OUT}/{BASE}.txt", "w") as fh:
        fh.write("\n\n".join(r["text"] for r in rows) + "\n")

    sil = (vdur - speech) / vdur * 100
    print(f"  {BASE}: {len(rows)} lines, {speech:.1f}s speech in {vdur:.1f}s, "
          f"{sil:.1f}% silent, {WPM:.0f} wpm")
    print(f"  wrote {OUT}/{BASE}.csv, .srt, .txt")


if __name__ == "__main__":
    main()
