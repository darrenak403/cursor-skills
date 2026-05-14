#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${CURSOR_USER_SKILLS_DIR:-$HOME/.cursor/skills}"
mkdir -p "$DEST"
rsync -a "$ROOT/.cursor/skills/" "$DEST/"
echo "Merged .cursor/skills/ from $ROOT into $DEST"
