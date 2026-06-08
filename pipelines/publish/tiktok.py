"""TikTok Content Posting API client (Direct Post via push_by_file).

Thin, single-account wrapper around the official v2 endpoints. Designed
for the Couple Things publishing tool where:

- Only the brand's own TikTok account (registered as a sandbox target
  user, later moved to production) is ever authenticated.
- Videos are pre-rendered MP4s smaller than 64 MB, so a single-chunk
  upload is enough.
- All long-lived state (client key/secret, access + refresh tokens) lives
  in ``.env``; this module reads it and writes refreshed tokens back.

References:
- https://developers.tiktok.com/doc/content-posting-api-reference-direct-post
- https://developers.tiktok.com/doc/login-kit-manage-user-access-tokens
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import requests

API_BASE = "https://open.tiktokapis.com"
TOKEN_URL = f"{API_BASE}/v2/oauth/token/"
CREATOR_INFO_URL = f"{API_BASE}/v2/post/publish/creator_info/query/"
INIT_DIRECT_POST_URL = f"{API_BASE}/v2/post/publish/video/init/"
STATUS_URL = f"{API_BASE}/v2/post/publish/status/fetch/"

# Sandbox + production both accept these. SELF_ONLY is always allowed; the
# others may be filtered by creator_info_query in sandbox mode.
PRIVACY_LEVELS = (
    "PUBLIC_TO_EVERYONE",
    "MUTUAL_FOLLOW_FRIENDS",
    "FOLLOWER_OF_CREATOR",
    "SELF_ONLY",
)

# Single-chunk upload limit. TikTok requires chunking for files larger
# than this; for our 30-60s animated shorts we stay well under it.
SINGLE_CHUNK_MAX_BYTES = 64 * 1024 * 1024


@dataclass
class TikTokError(Exception):
    """Raised when a TikTok API call returns a non-ok error code."""

    code: str
    message: str
    log_id: str | None = None
    http_status: int | None = None

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"TikTok API error [{self.code}] {self.message} (log_id={self.log_id}, http={self.http_status})"


def _raise_if_error(payload: dict, http_status: int) -> None:
    err = payload.get("error") or {}
    code = err.get("code")
    if code and code != "ok":
        raise TikTokError(
            code=code,
            message=err.get("message", ""),
            log_id=err.get("log_id"),
            http_status=http_status,
        )


def refresh_access_token(
    *, client_key: str, client_secret: str, refresh_token: str
) -> dict[str, Any]:
    """Exchange a refresh_token for a fresh access_token.

    Returns the raw token payload. Caller is responsible for persisting
    the new access_token / refresh_token (refresh_token rotates).
    """
    resp = requests.post(
        TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "client_key": client_key,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        timeout=30,
    )
    payload = resp.json()
    if resp.status_code != 200 or payload.get("error"):
        raise TikTokError(
            code=payload.get("error", "http_error"),
            message=payload.get("error_description", resp.text),
            log_id=payload.get("log_id"),
            http_status=resp.status_code,
        )
    return payload


def query_creator_info(access_token: str) -> dict[str, Any]:
    """Fetch creator-level constraints (allowed privacy levels, max
    duration, etc.). Must be called before init to comply with TikTok's
    UX rules.
    """
    resp = requests.post(
        CREATOR_INFO_URL,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        timeout=30,
    )
    payload = resp.json()
    _raise_if_error(payload, resp.status_code)
    return payload.get("data", {})


def init_direct_post(
    *,
    access_token: str,
    title: str,
    video_size: int,
    privacy_level: str,
    disable_comment: bool = False,
    disable_duet: bool = False,
    disable_stitch: bool = False,
    video_cover_timestamp_ms: int = 1000,
    brand_content_toggle: bool = False,
    brand_organic_toggle: bool = False,
) -> dict[str, Any]:
    """Initialize a direct-post upload session.

    Returns ``{"publish_id": "...", "upload_url": "..."}``.
    """
    if privacy_level not in PRIVACY_LEVELS:
        raise ValueError(f"privacy_level must be one of {PRIVACY_LEVELS}, got {privacy_level!r}")
    if video_size > SINGLE_CHUNK_MAX_BYTES:
        raise ValueError(
            f"video_size {video_size} exceeds single-chunk limit "
            f"{SINGLE_CHUNK_MAX_BYTES}; chunked upload not implemented yet"
        )

    body = {
        "post_info": {
            "title": title,
            "privacy_level": privacy_level,
            "disable_duet": disable_duet,
            "disable_comment": disable_comment,
            "disable_stitch": disable_stitch,
            "video_cover_timestamp_ms": video_cover_timestamp_ms,
            "brand_content_toggle": brand_content_toggle,
            "brand_organic_toggle": brand_organic_toggle,
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": video_size,
            "chunk_size": video_size,
            "total_chunk_count": 1,
        },
    }
    resp = requests.post(
        INIT_DIRECT_POST_URL,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        json=body,
        timeout=30,
    )
    payload = resp.json()
    _raise_if_error(payload, resp.status_code)
    return payload.get("data", {})


def upload_video(*, upload_url: str, video_bytes: bytes) -> None:
    """Upload the full video as a single chunk to the TikTok-issued URL."""
    size = len(video_bytes)
    headers = {
        "Content-Type": "video/mp4",
        "Content-Length": str(size),
        "Content-Range": f"bytes 0-{size - 1}/{size}",
    }
    resp = requests.put(upload_url, headers=headers, data=video_bytes, timeout=300)
    if resp.status_code not in (200, 201):
        raise TikTokError(
            code="upload_failed",
            message=f"PUT {upload_url} returned {resp.status_code}: {resp.text[:500]}",
            http_status=resp.status_code,
        )


def fetch_publish_status(*, access_token: str, publish_id: str) -> dict[str, Any]:
    """Query the current publish state. The ``status`` field transitions
    through ``PROCESSING_UPLOAD`` / ``PROCESSING_DOWNLOAD`` /
    ``PUBLISH_COMPLETE`` / ``FAILED``.
    """
    resp = requests.post(
        STATUS_URL,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        json={"publish_id": publish_id},
        timeout=30,
    )
    payload = resp.json()
    _raise_if_error(payload, resp.status_code)
    return payload.get("data", {})


def publish_video_file(
    *,
    access_token: str,
    video_path: Path,
    title: str,
    privacy_level: str = "SELF_ONLY",
    poll_interval_seconds: float = 5.0,
    poll_timeout_seconds: float = 300.0,
    on_status: Callable[[dict[str, Any]], None] | None = None,
    **post_info_kwargs: Any,
) -> dict[str, Any]:
    """End-to-end direct post: init → upload → poll → terminal status.

    Returns the final status payload. Raises ``TikTokError`` on API-level
    failures, ``TimeoutError`` if polling exceeds the timeout.
    """
    video_bytes = video_path.read_bytes()
    init_data = init_direct_post(
        access_token=access_token,
        title=title,
        video_size=len(video_bytes),
        privacy_level=privacy_level,
        **post_info_kwargs,
    )
    publish_id = init_data["publish_id"]
    upload_url = init_data["upload_url"]

    if on_status:
        on_status({"phase": "uploading", "publish_id": publish_id, "size": len(video_bytes)})
    upload_video(upload_url=upload_url, video_bytes=video_bytes)

    deadline = time.monotonic() + poll_timeout_seconds
    while time.monotonic() < deadline:
        status_data = fetch_publish_status(access_token=access_token, publish_id=publish_id)
        if on_status:
            on_status({"phase": "polling", "publish_id": publish_id, **status_data})
        status = status_data.get("status")
        if status in {"PUBLISH_COMPLETE", "SEND_TO_USER_INBOX"}:
            return status_data
        if status in {"FAILED", "PUBLISH_FAILED"}:
            raise TikTokError(
                code=status,
                message=status_data.get("fail_reason", "publish failed"),
            )
        time.sleep(poll_interval_seconds)
    raise TimeoutError(
        f"Publish did not reach a terminal state within {poll_timeout_seconds}s "
        f"(publish_id={publish_id})"
    )


def env_credentials() -> dict[str, str]:
    """Read all required TikTok credentials from the environment."""
    required = ("TIKTOK_CLIENT_KEY", "TIKTOK_CLIENT_SECRET", "TIKTOK_ACCESS_TOKEN")
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        raise RuntimeError(
            f"Missing TikTok env vars: {', '.join(missing)}. "
            "Run scripts/tiktok_auth.py or scripts/tiktok_refresh.py first."
        )
    return {
        "client_key": os.environ["TIKTOK_CLIENT_KEY"],
        "client_secret": os.environ["TIKTOK_CLIENT_SECRET"],
        "access_token": os.environ["TIKTOK_ACCESS_TOKEN"],
        "refresh_token": os.environ.get("TIKTOK_REFRESH_TOKEN", ""),
        "open_id": os.environ.get("TIKTOK_OPEN_ID", ""),
    }
