"""ffmpeg helpers — download shot mp4s and concat them into one reel."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import imageio_ffmpeg
import requests


FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def download(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with dest.open("wb") as f:
            shutil.copyfileobj(r.raw, f)
    return dest


def concat(shot_paths: list[Path], out_path: Path) -> Path:
    """Lossless concat. All shots must share codec/resolution/fps —
    Seedance 2.0 720p std outputs do, so -c copy is safe.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    list_file = out_path.with_suffix(".txt")
    list_file.write_text("".join(f"file '{p.resolve()}'\n" for p in shot_paths))
    subprocess.run(
        [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
         "-c", "copy", str(out_path)],
        check=True,
    )
    list_file.unlink(missing_ok=True)
    return out_path
