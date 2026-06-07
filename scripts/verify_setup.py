"""One-shot connectivity check for the secrets configured under Phase 7-γ.

Run via the verify-setup GitHub Action (or locally) AFTER the secrets in
docs/08 are populated. Does NOT burn Higgsfield credits or post anything
public — just hits cheap read endpoints and round-trips a tiny file
through R2.
"""

from __future__ import annotations

import json
import os
import sys
import uuid
from pathlib import Path

REQUIRED = [
    "HIGGSFIELD_API_KEY",
    "R2_ACCESS_KEY_ID",
    "R2_SECRET_ACCESS_KEY",
    "R2_ENDPOINT",
    "R2_BUCKET",
    "R2_PUBLIC_BASE_URL",
    "POSTIZ_BASE_URL",
    "POSTIZ_API_KEY",
]


def _check_env() -> None:
    missing = [k for k in REQUIRED if not os.environ.get(k)]
    if missing:
        raise SystemExit(f"missing required env vars: {', '.join(missing)}")
    print("env: all required secrets present")


def _check_higgsfield() -> None:
    import requests

    base = os.environ.get("HIGGSFIELD_API_BASE", "https://api.higgsfield.ai")
    key = os.environ["HIGGSFIELD_API_KEY"]
    r = requests.get(f"{base}/v1/balance", headers={"Authorization": f"Bearer {key}"}, timeout=15)
    r.raise_for_status()
    body = r.json()
    print(f"higgsfield: ok — balance={body.get('credits')} plan={body.get('subscription_plan_type')}")


def _check_r2_round_trip() -> None:
    import boto3
    import requests
    from botocore.config import Config

    bucket = os.environ["R2_BUCKET"]
    key = f"verify/{uuid.uuid4()}.txt"
    payload = f"verify {uuid.uuid4()}".encode()

    s3 = boto3.client(
        "s3",
        endpoint_url=os.environ["R2_ENDPOINT"],
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )
    s3.put_object(Bucket=bucket, Key=key, Body=payload, ContentType="text/plain")
    print(f"r2 upload: ok — {bucket}/{key}")

    public_url = f"{os.environ['R2_PUBLIC_BASE_URL'].rstrip('/')}/{key}"
    r = requests.get(public_url, timeout=15)
    if r.status_code != 200 or r.content != payload:
        raise SystemExit(
            f"r2 public read failed: {public_url} -> {r.status_code} (expected 200 with matching body)"
        )
    print(f"r2 public read: ok — {public_url}")

    s3.delete_object(Bucket=bucket, Key=key)
    print("r2 cleanup: ok")


def _check_postiz() -> None:
    import requests

    base = os.environ["POSTIZ_BASE_URL"].rstrip("/")
    key = os.environ["POSTIZ_API_KEY"]
    r = requests.get(
        f"{base}/public/v1/integrations",
        headers={"Authorization": f"Bearer {key}"},
        timeout=15,
    )
    r.raise_for_status()
    data = r.json()
    providers = sorted({i.get("providerIdentifier", "?") for i in data}) if isinstance(data, list) else []
    print(f"postiz: ok — {len(data) if isinstance(data, list) else '?'} integration(s) connected: {providers}")


def main() -> int:
    print("== Phase 7-γ verify ==")
    _check_env()
    print()
    _check_higgsfield()
    _check_r2_round_trip()
    _check_postiz()
    print()
    print("ALL GREEN — pipeline is wired up. Trigger generate.yml to run a real reel.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
