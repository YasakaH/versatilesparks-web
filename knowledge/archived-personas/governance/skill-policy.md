# Governance v1 — Skill Policy
════════════════════════════════

## Purpose
Ensure every skill in the Hermes ecosystem is necessary, high-quality, and maintainable.

---

## Skill Creation Rules

A new skill must answer every question in this checklist before it can be registered:

| Question | Purpose | Evidence Required |
|----------|---------|-------------------|
| Why does this exist? | Problem statement | Documented use case |
| What problem does it solve? | Value proposition | At least one failing scenario |
| Why can't existing skills solve it? | Duplicate check | Search results from `registry.yaml` |
| What capability does it provide? | Registry entry | One or more capability IDs |
| Who can use it? | Personality mapping | Target persona(s) |
| What are the inputs? | Contract | Full input schema |
| What are the outputs? | Contract | Full output schema |
| How is success measured? | Evaluation | Pass/fail criteria, quality threshold |

## Skill Approval Process

```
Submit ──→ Static Review ──→ Security Check ──→ Duplicate Check ──→ Test Task ──→ Quality Score ──→ Register ──→ Available
  │            │                  │                   │                   │              │              │
  │            ▼                  ▼                   ▼                   ▼              ▼              ▼
  │        Syntax +          Sandbox +            Registry +          Run 3         Score > 70?    Add to
  │        structure         permissions          golden rule         benchmarks                   registry.yaml
  │         check             audit                search
  ▼
FAIL at any gate → Reject with reason → Author revises → Resubmit
```

## Duplicate Prevention

Before creating ANY skill:

1. **Search installed skills** — full registry search
2. **Search official registries** — `awesome-hermes-skills`, skill registries
3. **Search trusted GitHub repos** — verified publisher accounts
4. **Search MCP registries** — if applicable

If an existing skill provides overlapping capability:
- Can it be extended? → Extend
- Can it be composed? → Compose
- Is there a genuine gap? → Create (with justification)

## Deprecation Policy

```
active/ ──→ deprecated/ ──→ archived/
```

- **Active:** Available for selection. Quality score maintained.
- **Deprecated:** Still available. New personalities should not be trained on it. Warning displayed. Auto-archived after 90 days with zero usage.
- **Archived:** Not available for selection. History preserved. Can be restored with re-approval.

**Never delete.** Keep full history. Deprecation reason must be documented.

## Semantic Versioning

All skills follow semver:

```
skill-name vMAJOR.MINOR.PATCH

MAJOR: Breaking change (input/output contract change)
MINOR: New capability (backward compatible)
PATCH: Bug fix, optimization, documentation
```

API contract changes = MAJOR bump. Always.
