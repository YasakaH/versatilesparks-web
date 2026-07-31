# Orchestration Policy

Personalities are orchestrators, not capability containers.

## Core Principle

A personality's responsibility is to **reason, prioritize, sequence, and coordinate** existing skills to accomplish an objective. It should never duplicate logic that belongs in a skill.

## Orchestration Flow

```
Input
  │
  ▼
Personality analyzes intent
  │
  ▼
Personality identifies required capabilities
  │
  ▼
Personality queries Skill Registry
  │
  ▼
Skills selected and sequenced (DAG)
  │
  ▼
Skills executed (parallel where possible)
  │
  ▼
Results combined and conflicts resolved
  │
  ▼
Quality gates applied
  │
  ▼
Final output
```

## Skill Selection Rules

1. **Prefer specialized over general** — if `architecture-review` exists, use it before `general-analysis`
2. **Prefer verified over unverified** — skills with test evidence rank higher
3. **Compose before build** — chain existing skills before creating new ones
4. **Parallelize independent work** — skills with no dependencies run concurrently

## Conflict Resolution

When two skills produce disagreeing outputs:

1. Prefer verified evidence
2. Prefer deterministic outputs
3. Prefer newer information
4. Prefer project conventions
5. Explain disagreements explicitly
6. Never silently choose one result

## Capability Advertising

Skills advertise capabilities via their `description` and `tags` in SKILL.md:

```yaml
capabilities:
  - architecture-review
  - code-review
  - performance-analysis
  - documentation
```

Personalities request capabilities, not skill names. The registry maps capabilities to skills.
