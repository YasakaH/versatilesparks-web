# Capability Registry v1
════════════════════════

**Purpose:** The directory of abilities. Personalities request capabilities. The registry selects the best implementation.

## Architecture

```
registry.yaml ────────── Global index of all registered capabilities
  │
  ├── capabilities/  ─── Individual capability definitions (*.yaml)
  ├── scoring/       ─── Ranking formulas and weight configs
  ├── dependencies/  ─── Dependency graph between capabilities
  ├── benchmarks/    ─── Performance data per capability implementation
  └── history/       ─── Execution history (quality, cost, latency tracking)
```

## Core Principle

Personalities should **never** say "use skill X".
They should say "I need capability Y".
The registry decides the best implementation based on real-time scoring.

## Resolution Flow

```
Required Capability
  │
  ▼
Registry Lookup ───→ Capability exists? ──NO──→ Missing capability event
  │                                              (trigger for creation)
  ▼
  YES
  │
  ▼
Available implementations (providers list)
  │
  ▼
Score each implementation:
  Quality × 0.40
  Reliability × 0.25
  Speed × 0.15
  Cost × 0.10
  Recency × 0.10
  ─────────────────
  Total Score
  │
  ▼
Select highest score
  │
  ▼
Execute → Log → Update benchmark data
```
