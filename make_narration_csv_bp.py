#!/usr/bin/env python3
"""
Narration for the current clips, as a CSV a voice studio can work from.

Beats were read off the rendered MP4s by sampling at one second. START is where
the line should begin. MAX_DUR is the ceiling before the next line starts, so a
studio adjusting timing knows how much room it has without recomputing anything.

Timing here is a starting point. The studio generates voice, adjusts final
timing, and exports the SRT, so this file is an input, not a contract.

  python3 make_narration_csv_bp.py
"""
import csv, os, subprocess, sys

B = os.path.dirname(os.path.abspath(__file__))
VID = os.path.expanduser("~/Downloads/ANIMO_DELIVERABLES_2026-09-09/video")
OUT = f"{B}/narration_csv"
WPM = 132.0

SAY = {"I.Q. Tree": "IQ-TREE", "racks M L": "RAxML", "rapid N J": "rapidnj"}

SCRIPTS = {
"7.01_negative_control": [
 (1.0,  "Every laboratory runs a no-template control.", "title and the lab analogy"),
 (5.2,  "We ran the same idea on the recombination detector.", "simulate with zero recombination, identical pipeline"),
 (9.6,  "Every simulated run should have found nothing.", "the replicate count lands, the dots fill"),
 (13.2, "Almost none of them did.", "the share that returned any call appears"),
 (15.8, "The largest value was vanishingly small.", "the largest value ever returned appears"),
 (19.4, "Now hold the axis linear and widen it.", "the widen instruction, then the readout"),
 (23.6, "The null stays visible, held at its own scale.", "the inset appears and the marker enters at the right"),
 (28.2, "The real groups arrive from the right.", "the real band enters the frame"),
 (32.4, "Each had its own matched simulation.", "both range labels resolve"),
 (35.6, "Separation is over four hundred fold.", "the separation headline appears"),
 (38.6, "The tool is not inventing recombination.", "the closing verdict"),
],
"7.03_detection_window": [
 (0.8,  "The detector looks for a local excess of SNP density.", "the whole trick, stated on screen"),
 (5.6,  "One imported piece sits in this stretch. It never changes.", "the piece is labeled, then the never-changes line"),
 (10.6, "Watch where those SNPs get counted.", "the counted-as bars appear"),
 (14.0, "Below the floor, nothing stands out. It all counts as mutation.", "the bars read nothing and everything"),
 (22.8, "Inside the window the piece is denser, so it is found.", "the verdict flips to marked"),
 (28.4, "Now part of the distance counts as recombination.", "the bars split"),
 (32.6, "Above the ceiling, SNPs are dense everywhere.", "the verdict flips back"),
 (36.2, "The piece has not moved. Can you still find it?", "the find-it challenge appears"),
 (40.8, "Too similar and too different both give a low number.", "the symmetry line"),
 (45.4, "Only the middle is measurable.", "the three class medians and the closing line"),
],
"7.07_recursive_subdivision": [
 (4.4,  "This group sat comfortably inside the working window.", "the parent bar and its statistics"),
 (8.6,  "The evidence it held two populations was clear.", "the justification for dividing"),
 (13.4, "So it was divided into three.", "the bar splits into three children"),
 (16.6, "Every genome carries over. Nothing is lost.", "the conservation line"),
 (20.4, "Now drop them onto the diversity scale.", "the bar descends into the plot"),
 (24.0, "The parent sat inside the range.", "the parent is plotted"),
 (27.4, "Its largest child lands eighteen times lower.", "the children plot and the drop is annotated"),
 (30.9, "Two fall below the floor. No rate can be read.", "the two below-floor bars turn red, closing line"),
],
"7.09_tree_builder_paired": [
 (0.8,  "Does the choice of tree builder change the answer?", "title and subtitle"),
 (5.0,  "Each dot is one comparison, as a ratio against racks M L.", "the axis and both panel headers"),
 (11.0, "Below the line means a lower rate.", "the reference line at parity"),
 (14.8, "I.Q. Tree scatters both ways. No bias.", "the first panel verdict"),
 (18.6, "Almost every rapid N J dot falls below.", "the second panel fills, then its verdict"),
 (23.0, "A fast default lowers the answer.", "the worst case is marked"),
],
"7.12_outbreak_threshold": [
 (1.0,  "In an outbreak, a SNP threshold suggests two genomes share a source.", "the premise"),
 (7.6,  "Published thresholds for this organism are very tight.", "the decision band is shaded"),
 (12.4, "The upper bound rests on one small study.", "the provenance of the upper bound"),
 (16.6, "These four marks are measured. The curves are not.", "the measured anchors appear as the spine"),
 (21.4, "One is the recombination share. The other is detection.", "both curves draw and are labeled"),
 (26.2, "At the edge of the band, detection is close to nothing.", "the gap fills, then the edge callout"),
 (32.2, "One outbreak spanned over a thousand SNPs.", "the outbreak marker is highlighted"),
 (35.8, "About five percent of it survived filtering.", "the surviving fraction"),
 (39.2, "It matters most where it is detected least.", "the closing argument"),
 (43.0, "No threshold is proposed.", "the explicit refusal"),
],
}
BANNED = {"—": "em dash", "–": "en dash", ";": "semicolon"}


def dur(t): return len(t.split()) / WPM * 60.0


def probe(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", p], capture_output=True, text=True,
        check=True).stdout.strip())


def main():
    os.makedirs(OUT, exist_ok=True)
    every, total = [], 0
    for base, lines in SCRIPTS.items():
        mp4 = f"{VID}/{base}.mp4"
        if not os.path.isfile(mp4):
            sys.exit(f"FATAL: {mp4} not found.")
        vdur = probe(mp4)
        rows, speech = [], 0.0
        for i, (start, text, anchor) in enumerate(lines, 1):
            for ch, name in BANNED.items():
                if ch in text:
                    sys.exit(f"FATAL: {base} line {i} has a {name}.")
            if any(c.isdigit() for c in text):
                sys.exit(f"FATAL: {base} line {i} has a digit. Spell numbers "
                         "as words so the engine paces them.")
            d = dur(text)
            nxt = lines[i][0] if i < len(lines) else vdur
            if start + d > nxt + 1e-9:
                sys.exit(f"FATAL: {base} line {i} needs {d:.2f}s from {start:.2f} "
                         f"but the next line starts at {nxt:.2f}.")
            speech += d
            rows.append({"clip": base, "line": i, "start_s": f"{start:.2f}",
                         "max_dur_s": f"{nxt - start:.2f}",
                         "target_dur_s": f"{d:.2f}", "words": len(text.split()),
                         "text": text, "on_screen_anchor": anchor})
        cols = list(rows[0].keys())
        with open(f"{OUT}/{base}.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
        with open(f"{OUT}/{base}.txt", "w") as fh:
            fh.write("\n".join(r["text"] for r in rows) + "\n")
        sil = (vdur - speech) / vdur * 100
        if not 10.0 <= sil <= 35.0:
            sys.exit(f"FATAL: {base} is {sil:.1f}% silent, outside 10 to 35.")
        every += rows; total += len(rows)
        print(f"  {base:28s} {len(rows):2d} lines, clip {vdur:5.2f}s, "
              f"{sil:4.1f}% silent")
    with open(f"{OUT}/all_clips.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(every[0].keys()))
        w.writeheader(); w.writerows(every)
    with open(f"{OUT}/pronunciation.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["written_form", "say_it_as"])
        for say, written in SAY.items():
            w.writerow([written, say])
    if total < 40:
        sys.exit(f"FATAL: only {total} lines across five clips.")
    print(f"\nwrote {OUT}/  {total} lines, plus all_clips.csv and pronunciation.csv")


if __name__ == "__main__":
    main()
