#!/usr/bin/env python3
"""
Re-time all five narration scripts against the animations' actual beats.

Beat times were read off the rendered MP4s by sampling frames at one second.
Nothing here is inferred from the scene source or from the previous script.

Writes narration_v2/<base>.{csv,srt,txt}. START is where the line begins. The
gaps between lines are engineered and are part of the design, so a line is never
stretched to fill one.

Refuses to write if a line runs into the next line's start or past the clip, if
it contains a digit, or if it uses a character the house style forbids.

  python3 retime_narration_bp.py
"""
import csv, os, subprocess, sys

B = os.path.dirname(os.path.abspath(__file__))
ANIMO = os.path.expanduser("~/Downloads/ANIMO_DELIVERABLES_2026-09-09")
OUT = f"{B}/narration_v2"
WPM = 132.0

# base -> [(start, text, the on-screen beat it is timed to), ...]
SCRIPTS = {
"7.01_negative_control": [
 (0.8,  "Every laboratory runs a no-template control.", "title, and the lab analogy appears"),
 (4.2,  "We ran the same idea on the recombination detector.", "simulate with zero recombination, identical pipeline"),
 (8.8,  "Almost every simulated run came back empty.", "the replicate count lands and the dots fill"),
 (12.4, "The few that did were vanishingly small.", "the largest value ever returned appears"),
 (15.8, "Now hold the axis linear and widen it.", "the on-screen instruction to widen the axis"),
 (20.4, "The scale stays linear the whole way. Only the width changes.", "the zoom begins, the readout climbs"),
 (26.6, "It widens until the real analysis groups appear.", "the real band enters the frame"),
 (30.6, "Each had its own matched simulation.", "the zoom completes and the band settles"),
 (34.2, "Separation is over four hundred fold.", "the separation headline appears"),
 (37.4, "So the tool is not inventing recombination.", "the closing verdict appears"),
],
"7.03_detection_window": [
 (0.6,  "The detector looks for a local excess of SNP density.", "the whole trick, stated on screen"),
 (5.4,  "One imported piece sits in this stretch. It never changes.", "the piece is labeled, then the never-changes line"),
 (10.2, "Below the floor there are almost no SNPs anywhere.", "NOT MARKED, almost no SNPs anywhere"),
 (16.6, "This is a real group, measured below the floor.", "the first real group resolves, below the floor"),
 (22.2, "Inside the window the piece is clearly denser, so it is found.", "the verdict flips to MARKED as imported"),
 (29.4, "Above the ceiling, SNPs are dense everywhere.", "the verdict flips back to NOT MARKED"),
 (33.2, "Now the piece looks ordinary, and is missed.", "the above-ceiling group resolves"),
 (38.4, "Too similar and too different both give a low number.", "the symmetry line appears"),
 (43.8, "Only inside the window is the number meaningful.", "the three class medians and the closing line"),
],
"7.07_recursive_subdivision": [
 (4.2,  "This group sat comfortably inside the working window.", "the parent bar and its statistics appear"),
 (8.2,  "The evidence it held two populations was clear.", "the on-screen justification for dividing"),
 (12.2, "So it was divided into three.", "the bar splits and the children are named"),
 (15.4, "Every genome carries over. Nothing is lost.", "the conservation line appears"),
 (19.4, "Now place the parent and the children on the diversity scale.", "the plot area and the floor line are drawn"),
 (25.4, "Watch where the children land.", "the children are plotted against the floor"),
 (28.4, "Two fall below the floor.", "the two below-floor bars turn red"),
 (31.2, "No rate can be interpreted for those two.", "the closing verdict appears"),
],
"7.09_tree_builder_paired": [
 (0.6,  "Does the choice of tree builder change the answer?", "title and subtitle"),
 (5.6,  "First, I.Q. Tree against racks M L, on the same alignments.", "the first panel header appears"),
 (11.6, "Lines scatter both ways. No directional bias.", "the first panel verdict appears"),
 (15.2, "Now rapid N J, against that same baseline.", "the second panel header appears"),
 (20.4, "Almost every line falls. That is systematic.", "the second panel verdict appears"),
 (23.8, "A fast default lowers the answer.", "the worst case is called out"),
],
"7.12_outbreak_threshold": [
 (0.6,  "In an outbreak, a SNP threshold suggests two genomes share a source.", "the premise appears"),
 (7.4,  "Published thresholds for this organism are very tight.", "the decision band is shaded"),
 (11.2, "The upper bound rests on one small study.", "the provenance of the upper bound appears"),
 (15.0, "This curve is the recombination share.", "the recombination curve is labeled"),
 (18.4, "This one is what the filter detects.", "the detection curve is labeled"),
 (22.0, "The field between them passes through unremoved.", "the field between the curves fills"),
 (25.6, "At the edge of the band, detection is close to nothing.", "the edge-of-band callout appears"),
 (32.2, "One published outbreak spanned a thousand SNPs.", "the outbreak marker appears"),
 (35.6, "Almost none of it survived recombination filtering.", "the surviving fraction is stated"),
 (38.9, "It matters most where it is detected least.", "the closing argument appears"),
 (42.9, "No threshold is proposed.", "the explicit refusal appears"),
],
}

BANNED = {"—": "em dash", "–": "en dash", ";": "semicolon",
          "‘": "curly quote", "’": "curly quote",
          "“": "curly quote", "”": "curly quote"}


def dur(t): return len(t.split()) / WPM * 60.0


def ts(x):
    h = int(x // 3600); m = int((x % 3600) // 60); s = x - h*3600 - m*60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def probe(p):
    return float(subprocess.run(
        ["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],
        capture_output=True, text=True, check=True).stdout.strip())


def main():
    os.makedirs(OUT, exist_ok=True)
    all_rows, total = [], 0
    for base, lines in SCRIPTS.items():
        mp4 = f"{ANIMO}/video/{base}.mp4"
        if not os.path.isfile(mp4):
            sys.exit(f"FATAL: {mp4} not found.")
        vdur = probe(mp4)
        rows, speech = [], 0.0
        for i, (start, text, beat) in enumerate(lines, 1):
            for ch, name in BANNED.items():
                if ch in text:
                    sys.exit(f"FATAL: {base} line {i} contains a {name}.")
            if any(c.isdigit() for c in text):
                sys.exit(f"FATAL: {base} line {i} contains a digit. Spell "
                         "numbers as words so the engine paces them.")
            d = dur(text); end = start + d
            nxt = lines[i][0] if i < len(lines) else vdur
            if end > nxt + 1e-9:
                sys.exit(f"FATAL: {base} line {i} ends {end:.2f}s into a slot "
                         f"closing at {nxt:.2f}s. Shorten it or move the start.")
            if end > vdur + 1e-9:
                sys.exit(f"FATAL: {base} line {i} runs past the {vdur:.3f}s clip.")
            speech += d
            rows.append({"clip": base, "line": i, "start_s": f"{start:.2f}",
                         "end_s": f"{end:.2f}", "dur_s": f"{d:.2f}",
                         "words": len(text.split()), "on_screen_beat": beat,
                         "text": text})
        with open(f"{OUT}/{base}.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
        with open(f"{OUT}/{base}.srt", "w") as fh:
            for r in rows:
                fh.write(f"{r['line']}\n{ts(float(r['start_s']))} --> "
                         f"{ts(float(r['end_s']))}\n{r['text']}\n\n")
        with open(f"{OUT}/{base}.txt", "w") as fh:
            fh.write("\n\n".join(r["text"] for r in rows) + "\n")
        sil = (vdur - speech) / vdur * 100
        if not 10.0 <= sil <= 35.0:
            sys.exit(f"FATAL: {base} is {sil:.1f}% silent, outside the "
                     "10 to 35 percent the design calls for.")
        all_rows += rows; total += len(rows)
        print(f"  {base:28s} {len(rows):2d} lines, {speech:5.1f}s in {vdur:5.1f}s, "
              f"{sil:4.1f}% silent")

    with open(f"{OUT}/all_clips.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(all_rows[0].keys()))
        w.writeheader(); w.writerows(all_rows)
    if total != 44:
        sys.exit(f"FATAL: {total} lines across five clips, expected 44.")
    print(f"\nwrote {OUT}/ for five clips, {total} lines, plus all_clips.csv")


if __name__ == "__main__":
    main()
