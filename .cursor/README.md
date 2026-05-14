# Cursor kit (repo `cursor-skills`)

This tree mirrors **`my-skills/.claude/`** for use in **Cursor**: same layout for `skills/`, `agents/`, `commands/`, `contexts/`, `coding-levels/`, and `hooks/`, plus Cursor-native **`rules/*.mdc`**. It lives under the **`cursor-skills`** repository as `.cursor/`.

## Layout

| Path | Role |
|------|------|
| `.cursor/skills/<name>/SKILL.md` | Project skills (Cursor `name` + `description` frontmatter; no `ck:` in `name`) |
| `.cursor/commands/ck/*.md` | Command prompts — body points at `.cursor/skills/...` |
| `.cursor/agents/*.md` | Subagent / Task prompt specs |
| `.cursor/contexts/*.md` | Mode snippets (dev / research / review) |
| `.cursor/coding-levels/*.md` | Style tiers |
| `.cursor/rules/*.mdc` | Cursor rules (globs + `alwaysApply`) |
| `.cursor/hooks/*.py` | **Claude Code–oriented** Python hooks (paths often still say `.claude` inside scripts) |

## Workspace root

Commands and init text use **“the Cursor workspace root (the folder that contains this `.cursor` directory for this kit)”** instead of `$CLAUDE_PROJECT_DIR`.

Open the **`cursor-skills`** repository root in Cursor so `.cursor/` paths resolve. To use from another app repo, copy this `.cursor` folder into that project’s root.

## Claude vs Cursor

- **`.claude/settings.json`** (hook wiring for Claude Code) is **not** auto-generated here. Cursor uses `.cursor/hooks.json` with a [different hook schema](https://docs.cursor.com) if you wire the same scripts.
- **`CLAUDE.md`**: the init wizard in `commands/ck/init.md` still speaks about `CLAUDE.md` in places; for Cursor-first projects prefer **`AGENTS.md`** at the repo root and adjust that wizard text if you rely on it.

## One-time maintenance scripts

- `.cursor/_fix_skills_frontmatter.py` — normalizes `SKILL.md` frontmatter after re-copying from `.claude/skills/`.
- `.cursor/_mirror_paths.py` — rewrites `.claude` → `.cursor` in commands/agents/contexts/coding-levels.

Re-run after refreshing skills from `my-skills/.claude/skills/`:

```bash
cd /path/to/cursor-skills   # this repo’s root
python3 .cursor/_fix_skills_frontmatter.py
python3 .cursor/_mirror_paths.py
```

## Hooks note

Python hooks under `.cursor/hooks/` were built for **Claude Code** session files (often under `.claude/session-data`). They are copied for parity; enabling them under Cursor requires either adapting paths to `.cursor/session-data` or symlinking `.claude` → `.cursor` at the project root — see `hooks/README.md`.
