#!/usr/bin/env python3
"""Manifest-driven assembly: stills + narration -> 9:16 Short with Ken Burns + burned captions.

Usage: python3 assemble.py <manifest.json>
Manifest: {"audio": "narration.wav", "output": "out.mp4",
           "blocks": [{"image": "img1.png", "words": 25, "captions": ["..."]}]}
Asset paths are relative to the manifest's directory.
"""
import json, subprocess, sys, os, textwrap

W, H = 1080, 1920
FPS = 30
DISCLAIMER = "Not financial advice. For information only."
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def probe_duration(path):
    out = subprocess.check_output(["ffprobe", "-v", "quiet", "-print_format", "json",
                                   "-show_format", path])
    return float(json.loads(out)["format"]["duration"])

def esc(s):
    return s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\’").replace("%", "\\%")

def main(manifest_path):
    sp = os.path.dirname(os.path.abspath(manifest_path))
    m = json.load(open(manifest_path))
    blocks = m["blocks"]
    audio = os.path.join(sp, m["audio"])
    total = probe_duration(audio)
    words = sum(b["words"] for b in blocks)
    print(f"audio {total:.2f}s, {words} words")

    t = 0.0
    segments = []  # (img, start, dur, captions)
    for b in blocks:
        dur = total * b["words"] / words
        segments.append((b["image"], t, dur, b["captions"]))
        t += dur

    inputs, filters, concat_refs = [], [], []
    for i, (img, start, dur, chunks) in enumerate(segments):
        inputs += ["-loop", "1", "-t", f"{dur:.3f}", "-framerate", str(FPS), "-i", os.path.join(sp, img)]
        frames = int(dur * FPS)
        zdir = "zoom+0.0009" if i % 2 == 0 else "1.28-0.0009*on"
        filters.append(
            f"[{i}:v]scale=1350:2400,zoompan=z='{zdir}':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},setsar=1[v{i}]"
        )
        concat_refs.append(f"[v{i}]")
    filters.append("".join(concat_refs) + f"concat=n={len(segments)}:v=1:a=0[base]")

    draw = "[base]"
    idx = 0
    for img, start, dur, chunks in segments:
        cd = dur / len(chunks)
        for j, chunk in enumerate(chunks):
            s, e = start + j * cd, start + (j + 1) * cd
            wrapped = "\n".join(textwrap.wrap(chunk, 24))
            out = f"[c{idx}]"
            filters.append(
                f"{draw}drawtext=fontfile={FONT}:text='{esc(wrapped)}':fontsize=64:fontcolor=white:"
                f"borderw=5:bordercolor=black@0.85:x=(w-text_w)/2:y=h*0.72:line_spacing=14:"
                f"enable='between(t,{s:.3f},{e:.3f})'{out}"
            )
            draw = out
            idx += 1
    filters.append(
        f"{draw}drawtext=fontfile={FONT}:text='{esc(DISCLAIMER)}':fontsize=28:fontcolor=white@0.55:"
        f"borderw=2:bordercolor=black@0.5:x=(w-text_w)/2:y=h*0.955[vout]"
    )

    outpath = os.path.join(sp, m["output"])
    cmd = ["ffmpeg", "-y", *inputs, "-i", audio,
           "-filter_complex", ";".join(filters),
           "-map", "[vout]", "-map", f"{len(segments)}:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-shortest", outpath]
    subprocess.run(cmd, check=True)
    print("done:", outpath)

if __name__ == "__main__":
    main(sys.argv[1])
