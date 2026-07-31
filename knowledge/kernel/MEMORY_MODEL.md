# Memory Model

> Governs how Hermes captures, stores, retrieves, and expires knowledge.

## Memory Levels
- **Ephemeral** — Current task context (lost after completion)
- **Session** — Conversation state (persists for session duration)
- **Long-term** — Stable preferences, rules, skills (survives restarts)
- **System** — Hermes knowledge base (versioned, audited)

## Memory Manager (subsystem, not personality)
Responsibilities:
1. **Capture** — Extract learnings from completed tasks
2. **Classify** — Assign memory level based on stability/relevance
3. **Retrieve** — Context-aware recall with decay weighting
4. **Expire** — TTL-based cleanup with confirmation for long-term
5. **Audit** — Log all memory operations for review

## Sync Strategy
- Local SQLite store (Honcho-compatible)
- Telegram backup for long-term/system memory
- 30-minute sync cadence for new entries
