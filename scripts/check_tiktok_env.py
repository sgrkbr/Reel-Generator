"""Quick sanity check for TikTok env vars without leaking secrets."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


def _summarize(name: str) -> None:
    v = os.environ.get(name, "")
    if not v:
        print(f"{name:28s} EMPTY")
        return
    masked = f"{v[:6]}...{v[-4:]}" if len(v) > 10 else "(too short to mask)"
    print(
        f"{name:28s} {masked}   len={len(v):3d}   has_eq_inside={'YES' if '=' in v else 'no'}"
    )


for key in (
    "TIKTOK_CLIENT_KEY",
    "TIKTOK_CLIENT_SECRET",
    "TIKTOK_REDIRECT_URI",
    "TIKTOK_SCOPES",
):
    _summarize(key)
