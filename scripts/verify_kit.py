#!/usr/bin/env python3
"""
Verify cursor-skills kit: agents/commands presence + frontmatter, hooks py_compile + smoke stdin.

Run from repo root:
  python3 scripts/verify_kit.py

Exit 0 if no hard failures; still prints WARN for path / doc mismatches.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CURSOR = REPO / ".cursor"
HOOKS = CURSOR / "hooks"
AGENTS = CURSOR / "agents"
COMMANDS = CURSOR / "commands"
SKILLS = CURSOR / "skills"


def eprint(*a: object) -> None:
    print(*a, file=sys.stderr)


def check_agents() -> list[str]:
    issues: list[str] = []
    for f in sorted(AGENTS.glob("*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        if len(text.strip()) < 80:
            issues.append(f"WARN agent thin content: {f.name} ({len(text)} chars)")
        if not text.lstrip().startswith("---"):
            issues.append(f"WARN agent missing YAML frontmatter: {f.name}")
    if not list(AGENTS.glob("*.md")):
        issues.append("FAIL no agents/*.md")
    return issues


def check_commands() -> list[str]:
    issues: list[str] = []
    for f in sorted(COMMANDS.rglob("*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        if not text.lstrip().startswith("---"):
            issues.append(f"FAIL command missing YAML frontmatter: {f.relative_to(CURSOR)}")
        if ".claude/" in text:
            issues.append(f"WARN command still references .claude/: {f.relative_to(CURSOR)}")
    if not list(COMMANDS.rglob("*.md")):
        issues.append("FAIL no commands")
    # init.md documents old rule filenames
    init = COMMANDS / "ck" / "init.md"
    if init.exists():
        t = init.read_text(encoding="utf-8", errors="replace")
        if "rules/agents.md" in t or "rules/commands.md" in t or "rules/skills.md" in t:
            issues.append(
                "WARN init.md still lists legacy rules/*.md — expect ck-*-design.mdc in kit"
            )
    return issues


def check_skills() -> list[str]:
    issues: list[str] = []
    for f in sorted(SKILLS.rglob("SKILL.md")):
        rel = f.relative_to(SKILLS)
        text = f.read_text(encoding="utf-8", errors="replace")
        if not text.lstrip().startswith("---"):
            issues.append(f"FAIL skill missing frontmatter: {rel}")
    if not list(SKILLS.rglob("SKILL.md")):
        issues.append("FAIL no SKILL.md under skills/")
    return issues


def py_compile_hooks() -> list[str]:
    import ast

    issues: list[str] = []
    for f in sorted(HOOKS.rglob("*.py")):
        try:
            ast.parse(f.read_text(encoding="utf-8", errors="replace"), filename=str(f))
        except SyntaxError as e:
            issues.append(f"FAIL syntax {f.relative_to(REPO)}: {e}")
    return issues


def smoke_hook(path: Path, stdin: str, env: dict | None = None) -> tuple[int, str, str]:
    r = subprocess.run(
        [sys.executable, str(path)],
        input=stdin,
        text=True,
        capture_output=True,
        cwd=str(REPO),
        env={**dict(**__import__("os").environ), **(env or {})},
        timeout=30,
    )
    return r.returncode, r.stdout, r.stderr


def check_hooks_runtime() -> list[str]:
    issues: list[str] = []
    tests: list[tuple[str, Path, str]] = [
        ("dev_rules_reminder", HOOKS / "dev_rules_reminder.py", '{"message":"/ck:cook test"}'),
        ("privacy_block", HOOKS / "privacy_block.py", "{}"),
        ("session_end", HOOKS / "session_end.py", "{}"),
        ("pre_compact", HOOKS / "pre_compact.py", "{}"),
        ("subagent_init", HOOKS / "subagent_init.py", "{}"),
        ("caveman_watch", HOOKS / "caveman_watch.py", '{"message":"be brief"}'),
        ("artifact_fold", HOOKS / "artifact_fold.py", "{}"),
        ("session_init", HOOKS / "session_init.py", "{}"),
        ("build_check", HOOKS / "build_check.py", "{}"),
        ("simplify_gate", HOOKS / "simplify_gate.py", "{}"),
        ("session_state", HOOKS / "session_state.py", "{}"),
    ]
    for name, script, stdin in tests:
        if not script.exists():
            issues.append(f"FAIL missing hook {name}")
            continue
        code, out, err = smoke_hook(script, stdin)
        if code not in (0, 2):
            issues.append(f"FAIL hook {name} exit={code} stderr={err[:500]!r}")
        elif code == 2:
            issues.append(f"INFO hook {name} exit=2 (deny) stderr={err[:200]!r}")

    # suggest_compact: no __main__, executed as script body
    sc = HOOKS / "suggest_compact.py"
    if sc.exists():
        code, out, err = smoke_hook(sc, "")
        if code != 0:
            issues.append(f"FAIL suggest_compact exit={code}")

    return issues


def check_portability() -> list[str]:
    """Hooks still target Claude Code paths (.claude) in several places."""
    issues: list[str] = []
    dr = HOOKS / "dev_rules_reminder.py"
    if dr.exists() and 'root / ".claude" / "contexts"' in dr.read_text(encoding="utf-8", errors="replace"):
        issues.append(
            "WARN portability: dev_rules_reminder reads .claude/contexts only — "
            "kit contexts live under .cursor/contexts/"
        )
    cfg = HOOKS / "lib" / "ck_config_utils.py"
    if cfg.exists() and 'root / ".claude"' in cfg.read_text(encoding="utf-8", errors="replace"):
        issues.append(
            "WARN portability: get_sessions_dir() uses <root>/.claude/session-data — "
            "pure .cursor installs need symlink or code change for session files"
        )
    return issues


def main() -> int:
    if not CURSOR.is_dir():
        eprint("Run from cursor-skills repo root (.cursor/ missing)")
        return 2

    all_issues: list[str] = []
    all_issues += check_agents()
    all_issues += check_commands()
    all_issues += check_skills()
    all_issues += py_compile_hooks()
    all_issues += check_hooks_runtime()
    all_issues += check_portability()

    fails = [x for x in all_issues if x.startswith("FAIL")]
    warns = [x for x in all_issues if x.startswith("WARN")]
    infos = [x for x in all_issues if x.startswith("INFO")]

    print("=== verify_kit.py ===")
    print(f"Repo: {REPO}")
    print(f"Agents: {len(list(AGENTS.glob('*.md')))} md")
    print(f"Commands: {len(list(COMMANDS.rglob('*.md')))} md")
    print(f"Skills: {len(list(SKILLS.rglob('SKILL.md')))} SKILL.md (all levels)")
    print(f"Hooks py: {len(list(HOOKS.rglob('*.py')))} files")
    print()
    for row in fails + warns + infos:
        print(row)

    print()
    if fails:
        print(f"Result: {len(fails)} FAIL, {len(warns)} WARN")
        return 1
    print(f"Result: OK ({len(warns)} WARN)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
