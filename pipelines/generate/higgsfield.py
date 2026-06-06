"""Thin Higgsfield REST client.

The MCP server we use during exploration wraps the same HTTPS API. This
module hits it directly so it can run in GitHub Actions without MCP.

Endpoint paths are filled in from HIGGSFIELD_API_BASE + the routes
documented in the Higgsfield developer dashboard. Adjust if Higgsfield
ships breaking changes.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any

import requests

API_BASE = os.environ.get("HIGGSFIELD_API_BASE", "https://api.higgsfield.ai")
API_KEY = os.environ["HIGGSFIELD_API_KEY"]

POLL_INTERVAL_SEC = 6
POLL_TIMEOUT_SEC = 60 * 15


class HiggsfieldError(RuntimeError):
    pass


@dataclass
class Job:
    id: str
    type: str        # "image" | "video"
    status: str
    url: str | None  # populated when status == "completed"


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }


def _post(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    r = requests.post(f"{API_BASE}{path}", json=payload, headers=_headers(), timeout=60)
    if not r.ok:
        raise HiggsfieldError(f"{r.status_code} {r.text}")
    return r.json()


def _get(path: str) -> dict[str, Any]:
    r = requests.get(f"{API_BASE}{path}", headers=_headers(), timeout=30)
    if not r.ok:
        raise HiggsfieldError(f"{r.status_code} {r.text}")
    return r.json()


def preflight_cost(payload: dict[str, Any]) -> float:
    """Ask Higgsfield how many credits the call would burn before submitting."""
    body = {**payload, "params": {**payload["params"], "get_cost": True}}
    out = _post("/v1/generate", body)
    return float(out["cost"]["credits_exact"])


def generate_image(prompt: str, model: str = "nano_banana_pro",
                   refs: list[str] | None = None, aspect_ratio: str = "9:16") -> Job:
    payload = {
        "params": {
            "model": model,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "medias": [{"role": "image", "value": rid} for rid in (refs or [])],
        }
    }
    out = _post("/v1/generate-image", payload)
    return Job(id=out["results"][0]["id"], type="image", status="pending", url=None)


def generate_video(prompt: str, start_image_job_id: str,
                   model: str = "seedance_2_0", duration: int = 5,
                   resolution: str = "720p", aspect_ratio: str = "9:16",
                   genre: str = "comedy") -> Job:
    payload = {
        "params": {
            "model": model,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
            "resolution": resolution,
            "genre": genre,
            "medias": [{"role": "start_image", "value": start_image_job_id}],
        }
    }
    out = _post("/v1/generate-video", payload)
    return Job(id=out["results"][0]["id"], type="video", status="pending", url=None)


def get_job(job_id: str) -> Job:
    out = _get(f"/v1/jobs/{job_id}")
    result = out["results"][0]
    raw = result.get("results", {}).get("rawUrl")
    return Job(id=result["id"], type=result["type"], status=result["status"], url=raw)


def wait_for(job_id: str) -> Job:
    """Block until a job finishes, raising on failure or timeout."""
    started = time.monotonic()
    while True:
        job = get_job(job_id)
        if job.status == "completed":
            return job
        if job.status == "failed":
            raise HiggsfieldError(f"job {job_id} failed")
        if time.monotonic() - started > POLL_TIMEOUT_SEC:
            raise HiggsfieldError(f"job {job_id} timed out (>{POLL_TIMEOUT_SEC}s)")
        time.sleep(POLL_INTERVAL_SEC)
