#!/usr/bin/env python3
"""Pilot assembly: 6 stills + 1 narration -> 9:16 Short with Ken Burns + burned captions."""
import json, subprocess, sys, os, textwrap

SP = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1920
FPS = 30

# blocks: (image_file, caption_chunks[]) — chunks shown sequentially within block,
# block duration allocated proportionally to word count of narration text
BLOCKS = [
    ("img1.png", 25, ["57,000 jobs added in June", "barely HALF of what was expected", "Here's your week in money"]),
    ("img2.png", 28, ["Stocks didn't mind", "Dow +595 → RECORD HIGH", "major indexes up ~2% this week"]),
    ("img3.png", 26, ["Why is bad news good news?", "cooler jobs = less fear of a Fed hike", "less rate pressure → more appetite"]),
    ("img4.png", 30, ["not everyone joined the party", "chipmakers fell again — AI trade too hot?", "Apple quietly gained almost 5%"]),
    ("img5.png", 26, ["10-year Treasury yield → 4.46%", "Bitcoin back above $61,000", "after a 21-month low"]),
    ("img6.png", 22, ["softer economy = good news for markets", "...for now", "see you next Saturday"]),
]
DISCLAIMER = "Not financial advice. For information only."
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def probe_duration(path):
    out = subprocess.check_output(["ffprobe", "-v", "quiet", "-print_format", "json",
                                   "-show_format", path])
    return float(json.loads(out)["format"]["duration"])

def esc(s):
    return s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\’").replace("%", "\\%")

def main():
    audio = os.path.join(SP, "narration.wav")
    total = probe_duration(audio)
    words = sum(b[1] for b in BLOCKS)
    print(f"audio {total:.2f}s, {words} words")

    # per-block durations proportional to word count
    t = 0.0
    segments = []  # (img, start, dur, chunks)
    for img, wc, chunks in BLOCKS:
        dur = total * wc / words
        segments.append((img, t, dur, chunks))
        t += dur

    # build filter graph: one zoompan clip per image, concat, then drawtext captions
    inputs, filters, concat_refs = [], [], []
    for i, (img, start, dur, chunks) in enumerate(segments):
        inputs += ["-loop", "1", "-t", f"{dur:.3f}", "-framerate", str(FPS), "-i", os.path.join(SP, img)]
        frames = int(dur * FPS)
        zdir = "zoom+0.0009" if i % 2 == 0 else "1.28-0.0009*on"
        filters.append(
            f"[{i}:v]scale=1350:2400,zoompan=z='{zdir}':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},setsar=1[v{i}]"
        )
        concat_refs.append(f"[v{i}]")
    filters.append("".join(concat_refs) + f"concat=n={len(segments)}:v=1:a=0[base]")

    # captions: chunks evenly spaced within their block
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
    # disclaimer, small, whole video
    filters.append(
        f"{draw}drawtext=fontfile={FONT}:text='{esc(DISCLAIMER)}':fontsize=28:fontcolor=white@0.55:"
        f"borderw=2:bordercolor=black@0.5:x=(w-text_w)/2:y=h*0.955[vout]"
    )

    cmd = ["ffmpeg", "-y", *inputs, "-i", audio,
           "-filter_complex", ";".join(filters),
           "-map", "[vout]", "-map", f"{len(segments)}:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-shortest",
           os.path.join(SP, "week-in-money-pilot.mp4")]
    subprocess.run(cmd, check=True)
    print("done:", os.path.join(SP, "week-in-money-pilot.mp4"))

if __name__ == "__main__":
    main()
