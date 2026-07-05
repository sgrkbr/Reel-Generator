#!/usr/bin/env python3
"""Motion-graphics renderer: HTML template + audio -> 9:16 video with word-synced captions.

Usage:
  python3 render.py manifest.json                # full render
  python3 render.py manifest.json --stills 1,8,20   # preview PNGs at given seconds
Whisper word timestamps are used when faster-whisper is installed; otherwise
timings are synthesized from per-scene word counts (preview only).
"""
import json, math, os, subprocess, sys, shutil

SP = os.path.dirname(os.path.abspath(__file__))

def dur_of(path):
    out = subprocess.check_output(["ffprobe","-v","quiet","-print_format","json","-show_format",path])
    return float(json.loads(out)["format"]["duration"])

def whisper_words(audio):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return None
    model = WhisperModel("base.en", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(audio, word_timestamps=True)
    words = []
    for seg in segs:
        for w in seg.words:
            words.append({"txt": w.word.strip(), "t0": round(w.start,3), "t1": round(w.end,3)})
    return words

def synth_words(scenes, total):
    """Fallback: spread scene script text evenly across proportional time."""
    words, t = [], 0.0
    wsum = sum(s["words"] for s in scenes)
    for s in scenes:
        sd = total * s["words"]/wsum
        toks = s.get("script","x "*s["words"]).split()
        step = sd/max(len(toks),1)
        for k, tok in enumerate(toks):
            words.append({"txt": tok, "t0": round(t+k*step,3), "t1": round(t+(k+1)*step,3)})
        t += sd
    return words

def build_timeline(m, total, words):
    scenes = m["scenes"]
    tail = float(m.get("tail", 0))
    wsum = sum(s["words"] for s in scenes)
    # scene boundaries snapped to real word times
    cum, t0 = 0, 0.0
    for s in scenes:
        cum += s["words"]
        idx = min(int(round(len(words)*cum/wsum))-1, len(words)-1)
        t1 = words[idx]["t1"] if cum < wsum else total
        s["t0"], s["t1"] = round(t0,3), round(max(t1, t0+0.4),3)
        t0 = s["t1"]
    scenes[-1]["t1"] = total + tail
    # caption groups: <=4 words and <=1.6s
    caps, g = [], None
    for w in words:
        if g is None or len(g["words"])>=4 or w["t1"]-g["t0"]>1.6:
            g = {"t0": w["t0"], "t1": w["t1"], "words": []}
            caps.append(g)
        g["words"].append(w); g["t1"] = w["t1"]
    for i in range(len(caps)-1):           # hold until next group
        caps[i]["t1"] = caps[i+1]["t0"]
    caps[-1]["t1"] = total
    return {"total": total + tail, "brand": m["brand"], "ticker": m["ticker"],
            "scenes": scenes, "captions": caps}

def main():
    manifest = sys.argv[1]
    stills = None
    if "--stills" in sys.argv:
        stills = [float(x) for x in sys.argv[sys.argv.index("--stills")+1].split(",")]
    m = json.load(open(manifest))
    audio = os.path.join(SP, m["audio"])
    total = dur_of(audio)
    words = whisper_words(audio) if stills is None else None
    if words is None:
        words = synth_words(m["scenes"], total)
    data = build_timeline(m, total, words)
    json.dump(data, open(os.path.join(SP,"timeline.json"),"w"))

    from playwright.sync_api import sync_playwright
    fps = m.get("fps", 30)
    frames = os.path.join(SP, "frames")
    if stills is None:
        shutil.rmtree(frames, ignore_errors=True)
    os.makedirs(frames, exist_ok=True)
    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch()
        except Exception:
            browser = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        page = browser.new_page(viewport={"width":1080,"height":1920})
        page.goto("file://"+os.path.join(SP,"template.html"))
        page.evaluate("d => window.__setup(d)", data)
        page.wait_for_function("window.__ready === true", timeout=15000)
        if stills is not None:
            for t in stills:
                page.evaluate(f"window.__seek({t})")
                page.screenshot(path=os.path.join(frames, f"still_{t:05.1f}.png"))
            browser.close(); print("stills done"); return
        n = int((total + float(m.get("tail", 0)))*fps)
        for f in range(n):
            page.evaluate(f"window.__seek({f/fps})")
            page.screenshot(path=os.path.join(frames, f"f{f:05d}.jpg"), type="jpeg", quality=92)
            if f % 300 == 0: print(f"{f}/{n}")
        browser.close()
    out = os.path.join(SP, m["output"])
    subprocess.run(["ffmpeg","-y","-framerate",str(fps),"-i",os.path.join(frames,"f%05d.jpg"),
        "-i",audio,"-af",f"apad=pad_dur={m.get('tail',0)}",
        "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","160k","-shortest",out], check=True)
    print("done:", out)

if __name__ == "__main__":
    main()
