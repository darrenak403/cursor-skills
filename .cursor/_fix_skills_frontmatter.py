#!/usr/bin/env python3
"""One-shot normalizer for Cursor SKILL.md frontmatter under .cursor/skills/."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "skills"

DROP_KEYS = ("user-invocable", "when_to_use", "license", "version")

NAME_MAP = {
    "ck:plan": "ck-plan",
    "ck:cook": "ck-cook",
    "ck:fix": "ck-fix",
    "ck:brainstorm": "ck-brainstorm",
}


def normalize_name(raw: str, folder: str) -> str:
    raw = raw.strip()
    if raw in NAME_MAP:
        return NAME_MAP[raw]
    if re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", raw or ""):
        return raw
    return folder.replace("_", "-")


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    if end == -1:
        return False
    fm = text[3:end]
    body = text[end + 4 :]
    folder = path.parent.name
    lines_out: list[str] = []
    for line in fm.splitlines():
        key = line.split(":", 1)[0].strip() if ":" in line else ""
        if key in DROP_KEYS:
            continue
        if key == "name":
            _, _, rest = line.partition(":")
            name = normalize_name(rest, folder)
            lines_out.append(f"name: {name}")
            continue
        lines_out.append(line)
    new_fm = "\n".join(lines_out).strip("\n") + "\n"
    new_text = f"---\n{new_fm}---{body}"
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for f in sorted(ROOT.rglob("SKILL.md")):
        if process_file(f):
            changed += 1
            print("updated", f.relative_to(ROOT.parent))
    print("done, files changed:", changed)


if __name__ == "__main__":
    main()
