"""Refresh the TikTok access_token using the saved refresh_token.

The access_token lives ~24h; refresh_token lives ~60d and rotates each
refresh. Run this whenever publishing fails with token-expired, or on a
cron before each publish run.

Usage:
    python scripts/tiktok_refresh.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from _env_file import update_env

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"

# Add repo root to sys.path so we can import the pipelines package when
# this script is invoked from anywhere.
sys.path.insert(0, str(ROOT))

from pipelines.publish.tiktok import refresh_access_token  # noqa: E402


def main() -> None:
    load_dotenv(ENV_PATH)
    client_key = os.environ.get("TIKTOK_CLIENT_KEY")
    client_secret = os.environ.get("TIKTOK_CLIENT_SECRET")
    refresh_token = os.environ.get("TIKTOK_REFRESH_TOKEN")
    if not (client_key and client_secret and refresh_token):
        sys.exit(
            "Missing TIKTOK_CLIENT_KEY / TIKTOK_CLIENT_SECRET / "
            "TIKTOK_REFRESH_TOKEN in .env. Run scripts/tiktok_auth.py first."
        )

    print("Refreshing access token...")
    payload = refresh_access_token(
        client_key=client_key,
        client_secret=client_secret,
        refresh_token=refresh_token,
    )
    access_token = payload.get("access_token", "")
    new_refresh_token = payload.get("refresh_token", refresh_token)
    open_id = payload.get("open_id", os.environ.get("TIKTOK_OPEN_ID", ""))
    expires_in = payload.get("expires_in", "?")

    if not access_token:
        sys.exit(f"No access_token in response: {payload}")

    update_env(
        ENV_PATH,
        {
            "TIKTOK_ACCESS_TOKEN": access_token,
            "TIKTOK_REFRESH_TOKEN": new_refresh_token,
            "TIKTOK_OPEN_ID": open_id,
        },
    )

    print("Success. .env updated:")
    print(f"  TIKTOK_OPEN_ID        = {open_id}")
    print(f"  TIKTOK_ACCESS_TOKEN   = ({len(access_token)} chars, hidden)")
    print(f"  TIKTOK_REFRESH_TOKEN  = ({len(new_refresh_token)} chars, hidden)")
    print(f"  expires_in            = {expires_in} seconds")


if __name__ == "__main__":
    main()
