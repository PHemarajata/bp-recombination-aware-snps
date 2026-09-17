#!/usr/bin/env python3
"""Regression test for build_narration.py caption emission.

Two faults, both found only by rendering the delivered HTML in a browser:
  1. cue text was emitted unwrapped, so a long line was TRUNCATED by the player
  2. every cue carried line:94%, which drew captions through the control bar
"""
import json, os, re, subprocess, sys, tempfile, shutil
SCRIPT = os.path.expanduser("~/skills/narrated-clip-production/scripts/build_narration.py")
LONG = ("This organism lives in soil and surface water across the tropics, "
        "so people meet it where they live and work.")            # 110 chars
def make_clip(path, dur=10.0):
    subprocess.run(["ffmpeg","-v","error","-f","lavfi","-i",
        f"color=c=white:s=640x360:d={dur}:r=30","-pix_fmt","yuv420p","-y",path],check=True)
def run(tmp, *extra):
    vid=f"{tmp}/clip.mp4"; make_clip(vid)
    json.dump({"wpm":150,"say_as":{},"clips":[{"video":vid,"lines":[
        {"start_s":1.0,"text":LONG,"anchor":""}]}]}, open(f"{tmp}/spec.json","w"))
    r=subprocess.run([sys.executable,SCRIPT,f"{tmp}/spec.json","--out",tmp,*extra],
                     capture_output=True,text=True)
    if r.returncode!=0: raise SystemExit(f"build_narration failed:\n{r.stdout}\n{r.stderr}")
    return open(f"{tmp}/clip.vtt").read(), open(f"{tmp}/clip.srt").read()

def cue_text_lines(vtt):
    out=[]
    for blk in re.split(r"\n\s*\n", vtt.strip()):
        L=[x for x in blk.splitlines() if x.strip()]
        if not L or L[0]=="WEBVTT": continue
        i=next((k for k,x in enumerate(L) if "-->" in x),None)
        if i is not None: out.extend(L[i+1:])
    return out

fails=[]
tmp=tempfile.mkdtemp()
try:
    vtt,srt = run(tmp)
    # FAULT 1: cue text must wrap
    longest=max((len(x) for x in cue_text_lines(vtt)), default=0)
    if longest > 60:
        fails.append(f"FAULT 1 vtt: longest caption line is {longest} chars, expected <= 60 (unwrapped)")
    longest_srt=max((len(x) for x in cue_text_lines(srt)), default=0)
    if longest_srt > 60:
        fails.append(f"FAULT 1 srt: longest caption line is {longest_srt} chars, expected <= 60")
    # wrapping must not lose or reorder words
    joined=" ".join(cue_text_lines(vtt))
    if joined.split() != LONG.split():
        fails.append(f"FAULT 1b: wrapping changed the words: {joined[:70]!r}")
    # FAULT 2: no line:NN% by default
    if "line:" in vtt:
        fails.append(f"FAULT 2: default output carries a cue setting: {re.search(r'line:[0-9.]+%',vtt).group(0)}")
    # opt-in must still work
    vtt2,_ = run(tempfile.mkdtemp(), "--vtt-line", "90")
    if "line:90%" not in vtt2:
        fails.append("FAULT 3: --vtt-line 90 did not emit line:90%")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("\n".join(fails) if fails else "ALL PASS")
sys.exit(1 if fails else 0)
