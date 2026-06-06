#!/usr/bin/env bash
# Scaffold a new content/ideas/<slug>.md from the template.
# Usage: ./scripts/new-idea.sh shared-calendar
set -euo pipefail
slug="${1:?usage: new-idea.sh <slug>}"
out="content/ideas/${slug}.md"
if [[ -e "$out" ]]; then
  echo "already exists: $out" >&2
  exit 1
fi
cat > "$out" <<EOF
---
slug: ${slug}
series: couple-things
title: "TODO"
length_sec: 35
hook: "TODO one-line hook"
characters: [mei, sam]
status: draft
created: $(date +%Y-%m-%d)
shots:
  - id: s1
    characters: [mei]
    props: []
    keyframe_prompt: |
      TODO
    video_prompt: |
      TODO
EOF
echo "created $out"
