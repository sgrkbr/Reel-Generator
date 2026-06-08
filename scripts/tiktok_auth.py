"""TikTok Login Kit OAuth flow — sandbox helper.

Opens the TikTok authorization page in your default browser. After you
authorize, TikTok redirects to the GitHub Pages callback page where the
authorization code is shown. Paste it back into this script and it will
exchange the code for an access + refresh token and write them to .env.

Usage (from repo root, with .venv active and .env populated with
TIKTOK_CLIENT_KEY / TIKTOK_CLIENT_SECRET):

    python scripts/tiktok_auth.py

Prerequisite: the TikTok account you want to authorize must be added as
a sandbox Target user in the TikTok for Developers portal.
"""

from __future__ import annotations

import os
import secrets
import sys
import urllib.parse
import webbrowser
from pathlib import Path

import requests
from dotenv import load_dotenv

AUTHORIZE_URL = "https://www.tiktok.com/v2/auth/authorize/"
TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"


def _build_authorize_url(client_key: str, redirect_uri: str, scope: str, state: str) -> str:
    params = {
        "client_key": client_key,
        "scope": scope,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "state": state,
    }
    return f"{AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"


def _exchange_code(client_key: str, client_secret: str, code: str, redirect_uri: str) -> dict:
    resp = requests.post(
        TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "client_key": client_key,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        },
        timeout=30,
    )
    if resp.status_code != 200:
        raise SystemExit(f"Token exchange failed [{resp.status_code}]: {resp.text}")
    payload = resp.json()
    if "error" in payload and payload.get("error"):
        raise SystemExit(f"Token exchange returned error: {payload}")
    return payload


def _update_env(values: dict[str, str]) -> None:
    lines = ENV_PATH.read_text().splitlines() if ENV_PATH.exists() else []
    keys_to_set = set(values.keys())
    out: list[str] = []
    for line in lines:
        key = line.split("=", 1)[0].strip() if "=" in line and not line.lstrip().startswith("#") else None
        if key in keys_to_set:
            out.append(f"{key}={values[key]}")
            keys_to_set.discard(key)
        else:
            out.append(line)
    for k in keys_to_set:
        out.append(f"{k}={values[k]}")
    ENV_PATH.write_text("\n".join(out) + "\n")


def main() -> None:
    load_dotenv(ENV_PATH)

    client_key = os.environ.get("TIKTOK_CLIENT_KEY")
    client_secret = os.environ.get("TIKTOK_CLIENT_SECRET")
    redirect_uri = os.environ.get(
        "TIKTOK_REDIRECT_URI", "https://sgrkbr.github.io/Reel-Generator/callback.html"
    )
    scope = os.environ.get("TIKTOK_SCOPES", "user.info.basic,video.publish,video.upload")

    if not client_key or not client_secret:
        sys.exit("TIKTOK_CLIENT_KEY / TIKTOK_CLIENT_SECRET missing in .env")

    state = secrets.token_urlsafe(16)
    url = _build_authorize_url(client_key, redirect_uri, scope, state)

    print()
    print("Opening TikTok authorization page in your browser...")
    print()
    print("If it doesn't open automatically, copy and paste this URL:")
    print()
    print(f"  {url}")
    print()
    print(f"State (expected back unchanged): {state}")
    print()
    webbrowser.open(url)

    print("After authorizing in TikTok, you'll land on the callback page.")
    print("Copy the 'code' value shown there and paste it below.")
    print()
    code = input("code: ").strip()
    if not code:
        sys.exit("No code provided. Aborting.")

    returned_state = input(f"state (paste to verify, or press Enter to skip): ").strip()
    if returned_state and returned_state != state:
        sys.exit(f"State mismatch (expected {state}, got {returned_state}). Aborting.")

    print()
    print("Exchanging code for tokens...")
    payload = _exchange_code(client_key, client_secret, code, redirect_uri)

    access_token = payload.get("access_token", "")
    refresh_token = payload.get("refresh_token", "")
    open_id = payload.get("open_id", "")
    expires_in = payload.get("expires_in", "?")
    scopes_granted = payload.get("scope", "?")

    if not access_token:
        sys.exit(f"No access_token in response: {payload}")

    _update_env(
        {
            "TIKTOK_ACCESS_TOKEN": access_token,
            "TIKTOK_REFRESH_TOKEN": refresh_token,
            "TIKTOK_OPEN_ID": open_id,
        }
    )

    print()
    print("Success. Tokens written to .env:")
    print(f"  TIKTOK_OPEN_ID        = {open_id}")
    print(f"  TIKTOK_ACCESS_TOKEN   = ({len(access_token)} chars, hidden)")
    print(f"  TIKTOK_REFRESH_TOKEN  = ({len(refresh_token)} chars, hidden)")
    print(f"  expires_in            = {expires_in} seconds")
    print(f"  scope                 = {scopes_granted}")


if __name__ == "__main__":
    main()
