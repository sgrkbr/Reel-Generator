"""Sanity-check TikTok access token by calling /v2/user/info/."""

from __future__ import annotations

import json
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

USER_INFO_URL = "https://open.tiktokapis.com/v2/user/info/"
FIELDS = "open_id,union_id,avatar_url,display_name"


def main() -> None:
    token = os.environ.get("TIKTOK_ACCESS_TOKEN")
    if not token:
        sys.exit("TIKTOK_ACCESS_TOKEN missing. Run scripts/tiktok_auth.py first.")

    resp = requests.get(
        USER_INFO_URL,
        params={"fields": FIELDS},
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    print(f"HTTP {resp.status_code}")
    try:
        payload = resp.json()
    except ValueError:
        print(resp.text)
        sys.exit(1)
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
