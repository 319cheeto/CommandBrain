# Copilot Workspace Instructions — CommandBrain

> **This file is automatically loaded into every GitHub Copilot chat session in this workspace.**
> Edit it anytime to update the persistent context Copilot sees.

## Project Overview

- **Name:** CommandBrain
- **Author:** Joshua Sears (@319cheeto)
- **Repo:** https://github.com/319cheeto/CommandBrain
- **Purpose:** Offline Linux & security command reference for cybersecurity students. Search by *purpose* (e.g., `cb password cracking`) instead of memorizing command names.
- **Version:** 2.0.0
- **License:** MIT
- **Python:** 3.6+ (standard library only, no external dependencies)

## Architecture (4 core files)

| File | Role |
|------|------|
| `commandbrain.py` | All application logic: CLI, search, display, setup, import, workflows |
| `data.py` | All static data: 30 basic commands, 22 Kali tools, slang mappings, 5 workflows |
| `setup.py` | pip packaging (`cb` and `commandbrain` entry points) |
| `install.sh` / `install_windows.bat` | Installers (venv at `~/.commandbrain_env`, PATH setup) |

## Key Technical Details

- **Database:** SQLite at `~/.commandbrain.db` — created by `cb --setup [--kali]`
- **Search:** LIKE-based with fuzzy fallback (`difflib.get_close_matches`)
- **Display modes:** short (default), detailed (`-d`), examples-only (`-e`)
- **Color:** ANSI with auto-detection, `--no-color` flag, respects `NO_COLOR` env var
- **Entry point:** `main()` in `commandbrain.py` via argparse
- **Workflows:** 5 pentest chains (web-pentest, network-recon, password-attack, wireless-pentest, post-exploitation)

## About the Developer

- **Joshua Sears** — Cyber Security student (final year), part-time supplemental instructor teaching programming
- Has severe ADHD and dyslexia; takes longer to learn concepts but masters them deeply once learned
- Struggled hard learning Linux even as a programmer — building this tool for himself and students like him
- Students in his classes are already using CommandBrain and love it

## Session Memory

**CRITICAL: Always read `MEMORY.md` at the project root at the start of EVERY session.** It contains:
- Joshua's background and context
- Detailed session history and decisions
- Current TODO list and priorities
- Known issues and bugs
- Ideas and future plans

**At the end of every session, remind Joshua to update `MEMORY.md` (or offer to update it together).**
**MEMORY.md is gitignored (contains personal notes) but protected by OneDrive cloud backup.**
**If MEMORY.md is ever lost, check OneDrive recycle bin or version history to recover it.**

## Coding Conventions

- Single-file logic (`commandbrain.py`) — keep it consolidated, don't split into modules
- `C.COLOR` shorthand for ANSI codes (e.g., `C.CYAN`, `C.GREEN`, `C.END`)
- Tuples for command data: `(name, category, description, usage, examples, related_commands, notes, tags)`
- DB columns match tuple order with auto-increment `id` prepended
- User-facing text uses color formatting with fallback for no-color terminals
