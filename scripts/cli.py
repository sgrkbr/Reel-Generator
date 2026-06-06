"""Local-dev entry point for the generate pipeline.

Usage:
    python scripts/cli.py generate loud-snack
    python scripts/cli.py preflight loud-snack
"""

from __future__ import annotations

import sys
from pathlib import Path

import click

# Ensure the repo root is on sys.path so `from pipelines.generate...` works
# when invoked as `python scripts/cli.py`.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("slug")
def generate(slug: str) -> None:
    """End-to-end: keyframe → video → concat → R2 → write content/ready/."""
    from pipelines.generate.orchestrator import run
    out = run(slug)
    click.echo(f"wrote {out}")


@cli.command()
@click.argument("slug")
def preflight(slug: str) -> None:
    """Sum Higgsfield preflight costs for every shot in `<slug>.md`."""
    import frontmatter

    from pipelines.generate import higgsfield

    idea = (
        Path(__file__).resolve().parents[1]
        / "content" / "ideas" / f"{slug}.md"
    )
    shots = frontmatter.load(idea).metadata["shots"]
    total = 0.0
    for shot in shots:
        # Per-shot pair: 1 image + 1 video.
        img_cost = higgsfield.preflight_cost({
            "params": {
                "model": "nano_banana_pro",
                "prompt": shot["keyframe_prompt"],
                "aspect_ratio": "9:16",
            }
        })
        vid_cost = higgsfield.preflight_cost({
            "params": {
                "model": "seedance_2_0",
                "prompt": shot["video_prompt"],
                "aspect_ratio": "9:16",
                "duration": 5,
                "resolution": "720p",
            }
        })
        total += img_cost + vid_cost
        click.echo(f"{shot['id']}: image={img_cost} video={vid_cost}")
    click.echo(f"total: {total} credits")


if __name__ == "__main__":
    cli()
