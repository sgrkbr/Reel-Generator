"""Shared helper for updating .env files in place (used by tiktok_auth /
tiktok_refresh). Keeps existing comments and ordering; rewrites only the
lines whose key matches a value being set, and appends new keys at the
end if not present.
"""

from __future__ import annotations

from pathlib import Path


def update_env(env_path: Path, values: dict[str, str]) -> None:
    """Set or overwrite the given KEY=VALUE pairs in env_path, preserving
    other lines (including blanks and comments).
    """
    lines = env_path.read_text().splitlines() if env_path.exists() else []
    keys_to_set = set(values.keys())
    out: list[str] = []
    for line in lines:
        stripped = line.lstrip()
        if "=" in line and not stripped.startswith("#"):
            key = line.split("=", 1)[0].strip()
            if key in keys_to_set:
                out.append(f"{key}={values[key]}")
                keys_to_set.discard(key)
                continue
        out.append(line)
    for k in keys_to_set:
        out.append(f"{k}={values[k]}")
    env_path.write_text("\n".join(out) + "\n")
