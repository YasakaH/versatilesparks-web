# Handoff: Unified Folder Structure (Jul 29, 2026)

**TL;DR:** All scattered HPF files have been consolidated under `cookbook/`. Your existing paths at `E:\Hermes Projects\` root still exist (source files couldn't be deleted due to file locks), but the new canonical locations are below.

## What Moved Where

| Old Location | New Location |
|---|---|
| `E:\Hermes Projects\CORE\` | `cookbook\knowledge\core\` |
| `E:\Hermes Projects\kernel\` | `cookbook\knowledge\kernel\` |
| `E:\Hermes Projects\governance_new\` | `cookbook\knowledge\governance\` |
| `E:\Hermes Projects\_for_chatgpt\` | `cookbook\knowledge\submissions\v1\` |
| `E:\Hermes Projects\_for_chatgpt_v2\` | `cookbook\knowledge\submissions\v2\` |
| `E:\Hermes Projects\personas\` | `cookbook\knowledge\hpf-core\` |
| `E:\Hermes Projects\Agent Systems\` | `cookbook\research\agent-systems\` |
| `E:\Hermes Projects\automation-reliability-research\` | `cookbook\research\market\` |
| `E:\Hermes Projects\_hpf_v2_impl_plan.txt` | `cookbook\knowledge\_hpf_v2_impl_plan.txt` |
| `E:\Hermes Projects\_hpf_v2_issue_desc.txt` | `cookbook\knowledge\_hpf_v2_issue_desc.txt` |
| `C:\Users\varas\AppData\Local\Temp\opencode\hpf-core\SCHEMA.md` | `cookbook\knowledge\schema\SCHEMA.md` |
| `C:\Users\varas\AppData\Local\Temp\opencode\hpf-core\REASONING_MODES.md` | `cookbook\knowledge\schema\REASONING_MODES.md` |
| `E:\Hermes Projects\personas\THREE-BOOK-PLAN.md` | `cookbook\books\v3\THREE-BOOK-PLAN.md` |
| `E:\Hermes Projects\personas\PROJECT-ROADMAP.md` | `cookbook\PROJECT-ROADMAP.md` |
| `E:\Hermes Projects\personas\OPERATING-MODEL.md` | `cookbook\OPERATING-MODEL.md` |
| `E:\Hermes Projects\personas\PLATFORM-ARCHITECTURE.md` | `cookbook\PLATFORM-ARCHITECTURE.md` |
| `E:\Hermes Projects\personas\build_personas.py` | `cookbook\tools\build_personas.py` |

## Path Fallback for This Thread

The old files at `E:\Hermes Projects\` root still exist (locked by this thread or can't be deleted because of Git tracking). When this thread references paths like `CORE\`, `kernel\`, `personas\`, etc., you should:

1. **Prefer the new path** under `cookbook\knowledge\` or `cookbook\research\`
2. If the old path doesn't exist, check `cookbook\` — it's been moved

## V3 + HPF Work

V3 book ideation lives in `cookbook\books\v3\THREE-BOOK-PLAN.md`. The HPF core (canon concepts, personae, governance) lives in `cookbook\knowledge\hpf-core\` which preserves its own `.git` history pointing to `github.com/YasakaH/hpf-core.git`.

## Resolution (Jul 29, 2026 — Final Move)

All remaining scattered files have now been consolidated:

| Old Location | New Location |
|---|---|
| `E:\Hermes Projects\_*.py` (104 scripts) | `cookbook\tools\book-build\` |
| `E:\Hermes Projects\ai\, architecture\, ...` (34 dirs) | `cookbook\knowledge\archived-personas\` |
| `E:\Hermes Projects\transcript_*.txt` (3 files) | `cookbook\research\transcripts\` |
| `E:\Hermes Projects\_payload.json` | `cookbook\knowledge\submissions\` |
| `E:\Hermes Projects\_deep_research_conversation.json` | `cookbook\research\` |
| `E:\Hermes Projects\_copy_cookies.ps1` | `cookbook\tools\scripts\` |
| `E:\Hermes Projects\cookbook.zip` | `cookbook\dist\` |
| `E:\Hermes Projects\log.txt` | `cookbook\tools\book-build\` |
| `E:\Hermes Projects\INDEX.md` | `cookbook\knowledge\INDEX.md` |
| `E:\Hermes Projects\DNA.md` | `cookbook\knowledge\DNA.md` |

**Only two items remain at `E:\Hermes Projects\` root:**
- `cookbook/` — the unified repo
- `personas/` — empty directory, locked by the other opencode thread; can be deleted when that thread releases its lock

## INDEX.md

See `cookbook\INDEX.md` for the full directory map.
