# Technical reference — `.cursor/` (portable kit)

For the **full setup guide (Vietnamese)**, see the repository **[`README.md`](../README.md)**.

## Layout (after copy to `<workspace>/`)

```text
<workspace>/
  .cursor/
    skills/           # SKILL.md per skill folder
    rules/*.mdc       # Cursor rules (globs relative to workspace root)
    commands/         # Project commands (Markdown)
    agents/
    contexts/
    coding-levels/
    hooks/            # Optional Python (Claude Code–oriented)
    _fix_skills_frontmatter.py
    _mirror_paths.py
```

## Workspace rule

Cursor resolves `.cursor/**` from the **opened workspace folder**. That folder must **directly** contain `.cursor/`.

## Post-merge maintenance

From the workspace root (the directory that contains `.cursor/`):

```bash
python3 .cursor/_fix_skills_frontmatter.py
python3 .cursor/_mirror_paths.py
```

## Hooks

Skills, rules, commands, and agents work after a plain copy. **Python hooks** are not active in Cursor until you add a compatible `.cursor/hooks.json`. See [`hooks/README.md`](hooks/README.md).
