"""End-to-end pipeline for one reel.

Reads content/ideas/<slug>.md (frontmatter + a `shots:` list), generates
each shot via Higgsfield (keyframe → video), concatenates, uploads to R2,
and writes content/ready/<slug>.json with the metadata Postiz needs.

Shot frontmatter shape (mirrors the storyboard convention in
docs/04-production-pipeline.md):

    shots:
      - id: s1
        keyframe_prompt: |
          ...
        video_prompt: |
          ...
        characters: [mei, sam]
        props: [chip_bag_v1]
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import frontmatter
import yaml

from . import assemble, higgsfield, r2

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "raw"
FINAL_DIR = REPO_ROOT / "final" / "9x16"
READY_DIR = REPO_ROOT / "content" / "ready"
CHARACTERS_YAML = REPO_ROOT / "config" / "characters.yaml"
SERIES_YAML = REPO_ROOT / "config" / "series.yaml"


@dataclass
class ShotResult:
    id: str
    keyframe_job: str
    video_job: str
    local_path: Path


def _refs_for(entries: list[str], characters_cfg: dict[str, Any]) -> list[str]:
    """Resolve character/prop slugs to Higgsfield job IDs for use as medias[].

    Falls back through pinned_image_jobs (most recent first) since not every
    asset has been promoted to a Soul or Reference Element yet.
    """
    refs: list[str] = []
    for slug in entries:
        cfg = characters_cfg.get(slug) or characters_cfg.get("props", {}).get(slug)
        if not cfg:
            raise ValueError(f"unknown reference slug: {slug}")
        pinned = cfg.get("pinned_image_jobs") or []
        if not pinned:
            raise ValueError(f"no pinned ref image for slug: {slug}")
        refs.append(pinned[0])
    return refs


def _style_refs(characters_cfg: dict[str, Any]) -> list[str]:
    """Global style references injected into every keyframe generation so the
    brand look stays locked across shots."""
    return list(characters_cfg.get("style_references") or [])


def run(slug: str) -> Path:
    idea_path = REPO_ROOT / "content" / "ideas" / f"{slug}.md"
    post = frontmatter.load(idea_path)
    shots = post.metadata["shots"]
    series = post.metadata["series"]

    characters_cfg = yaml.safe_load(CHARACTERS_YAML.read_text())
    series_cfg = yaml.safe_load(SERIES_YAML.read_text())[series]

    style_refs = _style_refs(characters_cfg)
    results: list[ShotResult] = []
    for shot in shots:
        refs = style_refs + _refs_for(
            (shot.get("characters") or []) + (shot.get("props") or []),
            characters_cfg,
        )
        kf = higgsfield.generate_image(shot["keyframe_prompt"], refs=refs)
        kf = higgsfield.wait_for(kf.id)
        vid = higgsfield.generate_video(shot["video_prompt"], start_image_job_id=kf.id)
        vid = higgsfield.wait_for(vid.id)
        assert vid.url, "completed video missing url"
        local = assemble.download(vid.url, RAW_DIR / slug / f"{shot['id']}.mp4")
        results.append(ShotResult(shot["id"], kf.id, vid.id, local))

    reel_path = assemble.concat([r.local_path for r in results], FINAL_DIR / f"{slug}.mp4")
    public_url = r2.upload(reel_path, key=f"reels/{slug}.mp4")

    READY_DIR.mkdir(parents=True, exist_ok=True)
    out = {
        "slug": slug,
        "series": series,
        "title": post.metadata.get("title", slug),
        "hook": post.metadata.get("hook", ""),
        "length_sec": post.metadata.get("length_sec"),
        "video_url": public_url,
        "shots": [
            {"id": r.id, "keyframe_job": r.keyframe_job, "video_job": r.video_job}
            for r in results
        ],
        "series_cfg": series_cfg,
    }
    ready_path = READY_DIR / f"{slug}.json"
    ready_path.write_text(json.dumps(out, indent=2))
    return ready_path
