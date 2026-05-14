#!/usr/bin/env python3
"""Rewrite kit paths: .claude -> .cursor in commands, agents, contexts, coding-levels (run from any workspace that contains this .cursor/)."""
from __future__ import annotations

from pathlib import Path

BASE = Path(__file__).resolve().parent
DIRS = [BASE / "commands", BASE / "agents", BASE / "contexts", BASE / "coding-levels"]

REPLACEMENTS: list[tuple[str, str]] = [
    (".claude/", ".cursor/"),
    (
        "$CLAUDE_PROJECT_DIR",
        "the Cursor workspace root (the folder that contains this `.cursor` directory for this kit)",
    ),
]

LOAD_LINES = {
    BASE / "commands" / "ck" / "cook.md": (
        "Read `.cursor/skills/ck-cook/SKILL.md` (project skill `ck-cook`) and execute that workflow. "
        "Pass through any arguments the user provided: $ARGUMENTS"
    ),
    BASE / "commands" / "ck" / "plan.md": (
        "Read `.cursor/skills/ck-plan/SKILL.md` (project skill `ck-plan`) and execute that workflow. "
        "Pass through any arguments the user provided: $ARGUMENTS"
    ),
    BASE / "commands" / "ck" / "fix.md": (
        "Read `.cursor/skills/ck-fix/SKILL.md` (project skill `ck-fix`) and execute that workflow. "
        "Pass through any arguments the user provided: $ARGUMENTS"
    ),
    BASE / "commands" / "ck" / "brainstorm.md": (
        "Read `.cursor/skills/ck-brainstorm/SKILL.md` (project skill `ck-brainstorm`) and execute that workflow. "
        "Pass through any arguments the user provided: $ARGUMENTS"
    ),
}


def patch_text(path: Path, text: str) -> str:
    for a, b in REPLACEMENTS:
        text = text.replace(a, b)
    return text


def main() -> None:
    for d in DIRS:
        if not d.is_dir():
            continue
        for path in sorted(d.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".md", ".mdc", ".txt"}:
                continue
            raw = path.read_text(encoding="utf-8")
            text = patch_text(path, raw)
            if path in LOAD_LINES and "Load the `" in text:
                lines = text.splitlines()
                out: list[str] = []
                replaced = False
                for line in lines:
                    if (
                        not replaced
                        and line.startswith("Load the `")
                        and "skill" in line
                    ):
                        out.append(LOAD_LINES[path])
                        replaced = True
                    else:
                        out.append(line)
                text = "\n".join(out) + ("\n" if text.endswith("\n") else "")
            if text != raw:
                path.write_text(text, encoding="utf-8")
                print("patched", path.relative_to(BASE))


if __name__ == "__main__":
    main()
