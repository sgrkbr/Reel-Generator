"""Upload a finished reel to Cloudflare R2 and return its public URL."""

from __future__ import annotations

import os
from pathlib import Path

import boto3
from botocore.config import Config


def _client():
    return boto3.client(
        "s3",
        endpoint_url=os.environ["R2_ENDPOINT"],
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )


def upload(local_path: Path, key: str, content_type: str = "video/mp4") -> str:
    """Upload `local_path` to R2 under `key`; return its public URL."""
    bucket = os.environ["R2_BUCKET"]
    _client().upload_file(
        str(local_path), bucket, key,
        ExtraArgs={"ContentType": content_type, "CacheControl": "public, max-age=86400"},
    )
    base = os.environ["R2_PUBLIC_BASE_URL"].rstrip("/")
    return f"{base}/{key}"
