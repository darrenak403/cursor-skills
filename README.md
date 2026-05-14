# cursor-skills

Standalone repo for the **Cursor** kit (moved from `Claude-kit/my-skills/.cursor`). It mirrors the Claude Code layout: `skills/`, `agents/`, `commands/`, `contexts/`, `coding-levels/`, `hooks/`, and Cursor **`rules/*.mdc`**, all under **`.cursor/`**.

## Use this repo

1. **Clone / open as the Cursor workspace** — paths in commands assume the workspace root is this repository (the folder that contains `.cursor/`).

2. **Install into another project** — copy the whole `.cursor` directory:

```bash
rsync -a ./.cursor/ /path/to/your-app/.cursor/
```

3. **Install only personal skills** (merge into your user skills):

```bash
./scripts/sync-skills-to-home.sh
```

## Sync with the Claude kit (`my-skills`)

The authoritative Claude bundle still lives in **`Claude-kit/my-skills/.claude/`**. After you change skills or commands there:

```bash
rsync -a ../my-skills/.claude/skills/ ./.cursor/skills/
# then re-run normalizers from repo root:
python3 ./.cursor/_fix_skills_frontmatter.py
python3 ./.cursor/_mirror_paths.py
```

(Adjust `../my-skills` if your clone layout differs.)

## Docs

- Full layout and hook notes: [`.cursor/README.md`](.cursor/README.md)

## Related

- Claude mirror: `my-skills/.claude/` in the monorepo (see `my-skills/CLAUDE.md`).
