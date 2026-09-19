#!/usr/bin/env python3
"""
Lay a synthesized room tone bed under a finished film.

Why this exists. The TUC films are assembled from parts whose narration is
placed line by line on a silent bed, so between lines the audio is digital
zero. Measured in half-second windows, clip 3 spent 14.6 percent of its runtime
below -60 dBFS. Two reference films in the same genre spent 0.3 and 2.9
percent. That dropout is most of why a concatenated film reads as a slideshow
rather than as a continuous piece, and it is worst exactly at the act seams,
where the tail of one part and the lead of the next are both silent.

A bed fixes it without touching anything that can desync. The video stream is
copied, no part is re-rendered, and no narration line moves, because the bed is
mixed under the already-finished film rather than into any part.

What the bed is. Band-limited pink noise, static, no rhythm and no melody. The
material's central finding is that a low number is a detection failure, and a
bed with a mood would editorialize a deliberately unglamorous result. Room tone
says "the room is on" and nothing else.

The defaults, and why:

  level -45 dBFS RMS   about 23 dB under the narration's -22 dB median. Present
                       but never competing. The reference films' bed-only
                       passages measure in this range.
  highpass 80 Hz       below this is rumble that costs headroom and says
                       nothing.
  lowpass 4000 Hz      speech intelligibility lives at 1 to 4 kHz. Keeping the
                       bed's top below that means it can never eat a consonant.

No sidechain ducking. At 23 dB of headroom it is not needed, and ducking pumps
at every line boundary, which is the same artifact being removed.

The level is reached by measurement, not by a hardcoded constant: a short probe
of the bed is generated and measured, and the amplitude is solved from it. So
changing the filters cannot silently move the level.

  python3 add_room_tone.py --in FILM.mp4 --out OUT.mp4 [--level -45]
  python3 add_room_tone.py --in FILM.mp4 --check     # measure only, write nothing
"""
import argparse
import array
import json
import math
import os
import subprocess
import sys
from shutil import which

PROBE_SECONDS = 10.0
PROBE_AMPLITUDE = 0.03
# Overlap-add looping. A supplied music bed is almost always shorter than the
# film and almost always fades at both ends, so butt-joining it leaves a hole at
# every loop point, which is the same dropout this tool exists to remove. Copies
# are instead placed every (usable_length - crossfade) seconds and summed, so
# each fade-out lands on the next fade-in. This is the same adelay-plus-amix
# pattern assemble_voice.py uses to place narration lines.
DEFAULT_XFADE = 4.0
# Output must stay aac / 48000 Hz / 1 channel. A film whose parts disagree on
# channel count plays silent after a concat that copies streams, and that bug
# measured as fine on every check that did not decode the audio.
OUT_RATE = 48000
OUT_CHANNELS = 1


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, **kw)


def probe_format(path):
    r = run(["ffprobe", "-v", "error", "-show_entries",
             "format=duration", "-show_streams", "-of", "json", path])
    if r.returncode != 0:
        sys.exit("FATAL: could not probe %s\n%s" % (path, r.stderr.decode()[:300]))
    d = json.loads(r.stdout)
    out = {"duration": float(d["format"]["duration"]), "video": None, "audio": None}
    for s in d["streams"]:
        if s["codec_type"] == "video" and out["video"] is None:
            out["video"] = {"codec": s.get("codec_name"),
                            "width": s.get("width"), "height": s.get("height"),
                            "fps": s.get("r_frame_rate")}
        elif s["codec_type"] == "audio" and out["audio"] is None:
            out["audio"] = {"codec": s.get("codec_name"),
                            "rate": int(s.get("sample_rate", 0)),
                            "channels": int(s.get("channels", 0))}
    return out


def decode_windows(source, is_lavfi=False, win=0.5):
    """RMS per window in dBFS, by full decode. A loudness filter is not used
    here on purpose: ffmpeg's tolerant decoder once reported a healthy figure
    for a film that played silent, because the container lied about itself."""
    pre = ["-f", "lavfi", "-i", source] if is_lavfi else ["-i", source, "-map", "0:a:0"]
    r = run(["ffmpeg", "-v", "error"] + pre +
            ["-f", "s16le", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", "-"])
    if r.returncode != 0:
        sys.exit("FATAL: decode failed for %s\n%s" % (source, r.stderr.decode()[:300]))
    a = array.array("h")
    a.frombytes(r.stdout[: len(r.stdout) // 2 * 2])
    if not a:
        sys.exit("FATAL: %s decoded to no audio at all." % source)
    n = int(16000 * win)
    out = []
    for i in range(0, max(1, len(a) - n), n):
        s = a[i:i + n]
        rms = math.sqrt(sum(x * x for x in s) / len(s)) + 1e-12
        out.append(20 * math.log10(rms / 32768))
    return out


def describe(windows, label):
    s = sorted(windows)
    below60 = sum(1 for x in s if x < -60)
    below40 = sum(1 for x in s if x < -40)
    print("  %-22s n=%4d  median %7.2f  min %8.2f  max %7.2f   "
          "below -60 dB %5.1f%%   below -40 dB %5.1f%%"
          % (label, len(s), s[len(s) // 2], s[0], s[-1],
             below60 / len(s) * 100, below40 / len(s) * 100))
    return {"median": s[len(s) // 2], "min": s[0], "max": s[-1],
            "pct_below_60": below60 / len(s) * 100,
            "pct_below_40": below40 / len(s) * 100}


def bed_filter(amplitude, duration, hp, lp):
    return ("anoisesrc=color=pink:r=%d:a=%s:d=%.3f,highpass=f=%d,lowpass=f=%d"
            % (OUT_RATE, amplitude, duration, hp, lp))


def solve_amplitude(target_db, hp, lp):
    """Generate a short probe, measure it, solve for the amplitude that lands
    on the target. Noise RMS is linear in amplitude, so one probe calibrates."""
    probe = bed_filter(PROBE_AMPLITUDE, PROBE_SECONDS, hp, lp)
    w = decode_windows(probe, is_lavfi=True)
    measured = sorted(w)[len(w) // 2]
    amp = PROBE_AMPLITUDE * (10 ** ((target_db - measured) / 20.0))
    print("  calibration            probe a=%.4f measured %.2f dB -> "
          "a=%.5f for %.1f dB" % (PROBE_AMPLITUDE, measured, amp, target_db))
    return amp, measured


def build_looped_bed(bed_path, target_duration, out_wav, trim_head, trim_tail,
                     xfade, compress, target_db):
    """Turn a supplied audio file into a seamless bed of exactly the length
    wanted, at exactly the level wanted.

    Three things get done, each because a supplied mix normally needs it:

      trim     a music bed usually fades in and out. Those fades are the
               loudest argument against looping it, so the faded ends are cut
               off and only full-level material is looped.
      overlap  copies are placed every (body - xfade) seconds and summed, so
               the join is a crossfade rather than a butt joint.
      compress a mix with a wide working range surges and recedes under
               narration. Flattening it is what makes it sit still.
    """
    src_dur = probe_format(bed_path)["duration"]
    body = src_dur - trim_head - trim_tail
    if body <= xfade + 1.0:
        sys.exit("FATAL: after trimming %.1f s off the head and %.1f s off the "
                 "tail, only %.1f s of bed is left, which cannot carry a %.1f s "
                 "crossfade." % (trim_head, trim_tail, body, xfade))
    stride = body - xfade
    # Every copy is faded in and out so that overlapping pairs sum to a constant.
    # The FIRST copy has nothing before it to sum with, so its fade in would be
    # an audible hole at t=0, which is exactly the defect being removed. Build
    # one crossfade longer than needed and cut that opening fade off, so the
    # film starts on bed already at full level.
    lead_in = xfade
    internal_target = target_duration + lead_in
    copies = int(math.ceil(internal_target / stride)) + 1

    chain = ["atrim=start=%.3f:end=%.3f" % (trim_head, src_dur - trim_tail),
             "asetpts=N/SR/TB",
             "aresample=%d" % OUT_RATE,
             "afade=t=in:st=0:d=%.3f:curve=tri" % xfade,
             "afade=t=out:st=%.3f:d=%.3f:curve=tri" % (body - xfade, xfade)]
    if compress:
        # Low threshold, moderate ratio, slow enough not to breathe.
        chain.append("acompressor=threshold=0.05:ratio=4:attack=200:release=1000")
    pre = ",".join(chain)

    parts = ["[0:a]%s,asplit=%d%s" % (pre, copies,
                                      "".join("[c%d]" % i for i in range(copies)))]
    labels = []
    for i in range(copies):
        ms = int(round(i * stride * 1000))
        parts.append("[c%d]adelay=%d|%d[d%d]" % (i, ms, ms, i))
        labels.append("[d%d]" % i)
    parts.append("%samix=inputs=%d:normalize=0:dropout_transition=0,"
                 "atrim=start=%.3f:end=%.3f,asetpts=N/SR/TB[bed]"
                 % ("".join(labels), copies, lead_in, lead_in + target_duration))

    r = run(["ffmpeg", "-y", "-v", "error", "-i", bed_path,
             "-filter_complex", ";".join(parts),
             "-map", "[bed]", "-c:a", "pcm_s16le",
             "-ar", str(OUT_RATE), "-ac", str(OUT_CHANNELS), out_wav])
    if r.returncode != 0:
        sys.exit("FATAL: could not build the looped bed\n%s"
                 % r.stderr.decode()[:600])

    # Level it by measurement, the same way the synthesized bed is leveled.
    w = decode_windows(out_wav)
    med = sorted(w)[len(w) // 2]
    gain = target_db - med
    r = run(["ffmpeg", "-y", "-v", "error", "-i", out_wav,
             "-af", "volume=%.3fdB" % gain,
             "-c:a", "pcm_s16le", "-ar", str(OUT_RATE), "-ac", str(OUT_CHANNELS),
             out_wav + ".lvl.wav"])
    if r.returncode != 0:
        sys.exit("FATAL: could not level the bed\n%s" % r.stderr.decode()[:600])
    os.replace(out_wav + ".lvl.wav", out_wav)

    w2 = sorted(decode_windows(out_wav, win=1.0))
    p10, p90 = w2[len(w2) // 10], w2[len(w2) * 9 // 10]
    print("  bed prepared           %.1f s source, trimmed to %.1f s body, "
          "%d copies, %.1f s crossfade" % (src_dur, body, copies, xfade))
    print("  bed level              median %.2f dB, working range p10..p90 "
          "%.2f dB, min %.2f" % (sorted(decode_windows(out_wav))[len(w) // 2],
                                 p90 - p10, w2[0]))
    return {"min": w2[0], "range": p90 - p10, "stride": stride}


def video_md5(path):
    r = run(["ffmpeg", "-v", "error", "-i", path, "-map", "0:v:0",
             "-c", "copy", "-f", "md5", "-"])
    return r.stdout.decode().strip() if r.returncode == 0 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="out")
    ap.add_argument("--level", type=float, default=-45.0,
                    help="bed RMS in dBFS (default -45)")
    ap.add_argument("--highpass", type=int, default=80)
    ap.add_argument("--lowpass", type=int, default=4000)
    ap.add_argument("--check", action="store_true",
                    help="measure the input and the bed, write nothing")
    ap.add_argument("--bed", help="audio file to loop instead of synthesized "
                                  "room tone")
    ap.add_argument("--bed-trim-head", type=float, default=0.0,
                    help="seconds to cut off the front of --bed, normally its "
                         "fade in")
    ap.add_argument("--bed-trim-tail", type=float, default=0.0,
                    help="seconds to cut off the end of --bed, normally its "
                         "fade out")
    ap.add_argument("--bed-xfade", type=float, default=DEFAULT_XFADE,
                    help="crossfade seconds at each loop point (default %.1f)"
                         % DEFAULT_XFADE)
    ap.add_argument("--compress", action="store_true",
                    help="flatten the bed's working range so it sits still "
                         "under narration")
    a = ap.parse_args()

    if not which("ffmpeg") or not which("ffprobe"):
        sys.exit("FATAL: ffmpeg and ffprobe must be on PATH.")
    if not os.path.isfile(a.inp):
        sys.exit("FATAL: %s not found." % a.inp)
    if not a.check and not a.out:
        sys.exit("FATAL: --out is required unless --check is given.")

    name = os.path.basename(a.inp)
    print("\n%s" % name)
    meta = probe_format(a.inp)
    if meta["audio"] is None:
        sys.exit("FATAL: %s has no audio stream." % name)
    print("  source                 %.3f s, video %s %dx%d @ %s, audio %s %d Hz %d ch"
          % (meta["duration"], meta["video"]["codec"], meta["video"]["width"],
             meta["video"]["height"], meta["video"]["fps"],
             meta["audio"]["codec"], meta["audio"]["rate"], meta["audio"]["channels"]))

    before = describe(decode_windows(a.inp), "before")

    if a.check and not a.bed:
        solve_amplitude(a.level, a.highpass, a.lowpass)
        print("  check only, nothing written")
        return

    os.makedirs(os.path.dirname(os.path.abspath(a.out or ".")) or ".", exist_ok=True)
    tmp_bed = None
    if a.bed:
        if not os.path.isfile(a.bed):
            sys.exit("FATAL: bed file %s not found." % a.bed)
        tmp_bed = (a.out or a.inp) + ".bed.wav"
        stats = build_looped_bed(a.bed, meta["duration"], tmp_bed,
                                 a.bed_trim_head, a.bed_trim_tail,
                                 a.bed_xfade, a.compress, a.level)
        if a.check:
            os.remove(tmp_bed)
            print("  check only, nothing written")
            return
        bed_in = ["-i", tmp_bed]
    else:
        amp, _ = solve_amplitude(a.level, a.highpass, a.lowpass)
        bed_in = ["-f", "lavfi", "-i",
                  bed_filter("%.6f" % amp, meta["duration"],
                             a.highpass, a.lowpass)]

    cmd = ["ffmpeg", "-y", "-v", "error",
           "-i", a.inp] + bed_in + [
           "-filter_complex",
           "[0:a]aresample=%d[v];[1:a]aresample=%d[b];"
           "[v][b]amix=inputs=2:duration=first:normalize=0,"
           "aformat=sample_rates=%d:channel_layouts=mono[aout]"
           % (OUT_RATE, OUT_RATE, OUT_RATE),
           "-map", "0:v:0", "-c:v", "copy",
           "-map", "[aout]", "-c:a", "aac", "-b:a", "160k",
           "-ar", str(OUT_RATE), "-ac", str(OUT_CHANNELS),
           "-movflags", "+faststart", a.out]
    r = run(cmd)
    if tmp_bed and os.path.isfile(tmp_bed):
        os.remove(tmp_bed)
    if r.returncode != 0:
        sys.exit("FATAL: ffmpeg failed on %s\n%s" % (name, r.stderr.decode()[:600]))

    # Verification. Each of these has a failure mode behind it.
    out_meta = probe_format(a.out)
    problems = []
    if abs(out_meta["duration"] - meta["duration"]) > 0.05:
        problems.append("duration moved: %.3f -> %.3f"
                        % (meta["duration"], out_meta["duration"]))
    oa = out_meta["audio"]
    if oa["rate"] != OUT_RATE or oa["channels"] != OUT_CHANNELS or oa["codec"] != "aac":
        problems.append("audio is %s %d Hz %d ch, must be aac %d Hz %d ch"
                        % (oa["codec"], oa["rate"], oa["channels"], OUT_RATE, OUT_CHANNELS))
    if video_md5(a.inp) != video_md5(a.out):
        problems.append("video stream changed; it must be a bit-identical copy")

    after = describe(decode_windows(a.out), "after")
    if after["pct_below_60"] > 0.5:
        problems.append("still %.1f%% of windows below -60 dB; the bed did not take"
                        % after["pct_below_60"])
    if after["median"] - before["median"] > 1.5:
        problems.append("median rose %.2f dB; the bed is too loud"
                        % (after["median"] - before["median"]))

    print("  wrote                  %s" % a.out)
    if problems:
        print("\n  FAILED:")
        for p in problems:
            print("    - %s" % p)
        sys.exit(1)
    print("  verified               duration held, video bit-identical, "
          "audio aac/%d/mono, silence removed" % OUT_RATE)


if __name__ == "__main__":
    main()
