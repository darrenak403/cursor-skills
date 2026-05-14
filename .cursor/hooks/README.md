# Hooks in this kit

These scripts were authored for **Claude Code** (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, …) and often read or write paths under **`.claude/`** (for example `.claude/session-data`, `.claude/contexts`).

Cursor Agent hooks use **`.cursor/hooks.json`** with different event names and stdin/stdout contracts. Do not assume this Python code runs unchanged in Cursor.

## Options

1. **Claude Code only** — keep using `.claude/settings.json` in projects bootstrapped from this kit; ignore hook files under `.cursor/hooks/` for Cursor.
2. **Dual layout** — symlink `.claude` → `.cursor` at the project root so legacy hook paths resolve (verify side effects first).
3. **Port properly** — update each script to resolve a `project_kit_dir()` that prefers `.cursor` when present, and add a Cursor `hooks.json` that invokes the same entrypoints with the Cursor hook protocol.
