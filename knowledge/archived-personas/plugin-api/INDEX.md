# Plugin & Extension API v1 — Index
══════════════════════════════════════

**Purpose:** Let Hermes grow without modifying the core. Plugins add capabilities, personalities, tools, and model integrations through a stable contract.

---

## Architecture

```
Hermes Core
    │
    └── Plugin API (stable contract)
           │
           ├── Skills           ← New abilities
           ├── Personalities    ← New expert reasoning patterns
           ├── Tools            ← External integrations (APIs, services)
           ├── Models           ← Model providers and routers
           ├── Memory Systems   ← Storage backends
           └── External Services ← Anything accessible via API
```

## Plugin Structure

```
plugin-name/
  ├── manifest.yaml          ← Required. Declares identity, capabilities, permissions.
  ├── skills/                ← Skill implementations
  ├── personalities/         ← Personality definitions
  ├── tools/                 ← Tool integrations
  ├── tests/                 ← Plugin-specific tests
  ├── documentation/         ← Plugin documentation
  └── README.md              ← Required. What, why, how.
```

## Plugin Lifecycle

```
Install ──→ Inspect ──→ Sandbox ──→ Test ──→ Approve ──→ Register ──→ Activate
  │            │           │          │         │            │            │
  │        Validate     Run in     Execute    Score >     Add to     Make
  │        manifest     isolated   3 tests    70%?       registry    available
  │        + schema     sandbox                                    for selection
  ▼
FAIL at any gate → Report with reason → Author revises → Resubmit
```
