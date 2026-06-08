"""Publish a video to TikTok via Content Posting API (Direct Post).

For Sandbox apps, only the registered target user can authorize, and the
post is only visible to that user. Default privacy is SELF_ONLY for
sandbox safety. Override with ``--privacy PUBLIC_TO_EVERYONE`` once the
app is approved for production.

Usage:
    python scripts/tiktok_publish.py path/to/video.mp4 --title "Test post"
    python scripts/tiktok_publish.py path/to/video.mp4 \
        --title "Live post" --privacy PUBLIC_TO_EVERYONE
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import click
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
sys.path.insert(0, str(ROOT))

from pipelines.publish.tiktok import (  # noqa: E402
    PRIVACY_LEVELS,
    TikTokError,
    publish_video_file,
    query_creator_info,
)


def _on_status(event: dict) -> None:
    phase = event.pop("phase", "?")
    pid = event.pop("publish_id", "?")
    extras = ", ".join(f"{k}={v}" for k, v in event.items() if v not in (None, ""))
    click.echo(f"[{phase}] publish_id={pid} {extras}")


@click.command()
@click.argument("video", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--title", required=True, help="Post caption / title shown on TikTok.")
@click.option(
    "--privacy",
    type=click.Choice(PRIVACY_LEVELS, case_sensitive=False),
    default="SELF_ONLY",
    show_default=True,
    help="Privacy level. Sandbox apps are limited; SELF_ONLY is always safe.",
)
@click.option("--disable-comment", is_flag=True, help="Disable comments on the post.")
@click.option("--disable-duet", is_flag=True, help="Disable duets.")
@click.option("--disable-stitch", is_flag=True, help="Disable stitches.")
@click.option(
    "--cover-ms",
    type=int,
    default=1000,
    show_default=True,
    help="Video cover frame timestamp in milliseconds.",
)
@click.option(
    "--show-creator-info/--no-creator-info",
    default=True,
    show_default=True,
    help="Pre-flight: query creator info (allowed privacy levels, max duration).",
)
def main(
    video: Path,
    title: str,
    privacy: str,
    disable_comment: bool,
    disable_duet: bool,
    disable_stitch: bool,
    cover_ms: int,
    show_creator_info: bool,
) -> None:
    load_dotenv(ENV_PATH)
    access_token = os.environ.get("TIKTOK_ACCESS_TOKEN")
    if not access_token:
        raise click.ClickException(
            "TIKTOK_ACCESS_TOKEN missing. Run scripts/tiktok_auth.py first "
            "(or scripts/tiktok_refresh.py if it expired)."
        )

    size = video.stat().st_size
    click.echo(f"Video: {video} ({size:,} bytes)")
    click.echo(f"Title: {title}")
    click.echo(f"Privacy: {privacy}")

    if show_creator_info:
        click.echo("Querying creator info...")
        try:
            info = query_creator_info(access_token)
        except TikTokError as e:
            raise click.ClickException(str(e))
        click.echo(json.dumps(info, indent=2, ensure_ascii=False))
        allowed = info.get("privacy_level_options") or []
        if allowed and privacy.upper() not in {p.upper() for p in allowed}:
            raise click.ClickException(
                f"Privacy {privacy} not in allowed list {allowed}. "
                "Pick one of the allowed values."
            )

    click.echo("Starting direct post...")
    try:
        final = publish_video_file(
            access_token=access_token,
            video_path=video,
            title=title,
            privacy_level=privacy.upper(),
            disable_comment=disable_comment,
            disable_duet=disable_duet,
            disable_stitch=disable_stitch,
            video_cover_timestamp_ms=cover_ms,
            on_status=_on_status,
        )
    except TikTokError as e:
        raise click.ClickException(str(e))
    except TimeoutError as e:
        raise click.ClickException(str(e))

    click.echo("Done. Final status:")
    click.echo(json.dumps(final, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
