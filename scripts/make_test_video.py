"""Generate a tiny 9:16 test MP4 for TikTok sandbox publish runs.

Uses the ffmpeg binary that ships with imageio-ffmpeg (already in
pyproject deps), so no system ffmpeg install is required. The output is
a 5-second 1080x1920 moving test pattern with audio — small enough to
upload in a single chunk and valid enough to pass TikTok's content
validation in sandbox mode.

Usage:
    python scripts/make_test_video.py              # writes assets/test/sandbox.mp4
    python scripts/make_test_video.py out.mp4      # writes to a custom path
    python scripts/make_test_video.py --duration 8 # 8-second clip
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import click
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "assets" / "test" / "sandbox.mp4"


@click.command()
@click.argument(
    "output",
    type=click.Path(dir_okay=False, path_type=Path),
    default=DEFAULT_OUT,
    required=False,
)
@click.option("--duration", type=int, default=5, show_default=True, help="Seconds.")
@click.option("--width", type=int, default=1080, show_default=True)
@click.option("--height", type=int, default=1920, show_default=True)
@click.option("--fps", type=int, default=30, show_default=True)
def main(output: Path, duration: int, width: int, height: int, fps: int) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    # Generate a vertical test pattern with a sine-wave audio track.
    cmd = [
        ffmpeg,
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"testsrc=duration={duration}:size={width}x{height}:rate={fps}",
        "-f",
        "lavfi",
        "-i",
        f"sine=frequency=440:duration={duration}",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-shortest",
        str(output),
    ]
    click.echo(f"Generating {output} ({width}x{height}, {duration}s, {fps}fps)...")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        click.echo(proc.stderr, err=True)
        sys.exit(proc.returncode)
    size = output.stat().st_size
    click.echo(f"Wrote {output} ({size:,} bytes)")


if __name__ == "__main__":
    main()
