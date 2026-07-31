# Personality Schema v2
══════════════════════

Formal schema for the Hermes Personality Framework v2.

Every field is required unless marked "optional". Each layer can be inherited independently.

---

## Layer 1 — Identity (7 fields)

Stable identity. Changes rarely.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✓ | kebab-case unique identifier |
| `version` | semver | ✓ | Current version |
| `domain` | enum | ✓ | Primary domain (engineering, ai, security, product, design, data, business, finance, legal, writing, marketing, operations, leadership, creative) |
| `description` | text | ✓ | One-liner purpose |
| `primary_role` | enum | ✓ | advisor, implementer, reviewer, operator, coordinator |
| `secondary_roles` | enum[] | optional | Additional roles |
| `inherits` | string | ✓ | Path to inherited base personality |
| `overrides` | string[] | ✓ | Fields that differ from the inherited base |

## Layer 2 — Competency (4 fields)

What the persona can do.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `expertise` | string[] | ✓ | Specialized knowledge areas |
| `capabilities` | string[] | ✓ | Capability IDs this persona provides |
| `primary_skills` | string[] | ✓ | Skill names this persona primarily uses |
| `authority_level` | enum | ✓ | L0-Observe, L1-Advise, L2-Suggest, L3-ExecuteLocal, L4-ExecuteProd, L5-Autonomous |

## Layer 3 — Cognition (4 fields)

How the persona thinks and decides.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `thinking_model` | ref | ✓ | Thinking model from the thinking library |
| `reasoning_patterns` | ref[] | ✓ | Reasoning patterns to apply (first-principles, systems-thinking, etc.) |
| `decision_framework` | ref | ✓ | Decision framework reference (default: CORE/DECISION_FRAMEWORK.md) |
| `prioritization` | ref | ✓ | Prioritization reference (default: CORE/PRIORITIZATION_FRAMEWORK.md) |

## Layer 4 — Behavior (5 fields)

How the persona interacts and produces output.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `interaction_pattern` | text | ✓ | How the persona engages with users and problems |
| `communication_style` | text | ✓ | Voice, tone, and style for output |
| `output_preferences` | object | ✓ | Preferred output format, depth, style |
| `quality_gates` | ref[] | ✓ | Quality standards reference (default: CORE/QUALITY_STANDARDS.md) |
| `output_templates` | text[] | ✓ | Standard output structures |

## Layer 5 — Governance (5 fields)

How the persona operates safely and is evaluated.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `constraints` | string[] | ✓ | Domain-specific constraints |
| `evaluation_criteria` | string[] | ✓ | How to measure success |
| `tool_access` | object | ✓ | Allowed and restricted tools |
| `escalation_rules` | rule[] | ✓ | When to continue, ask, or stop |
| `error_policy` | ref | ✓ | Error handling reference (default: CORE/ERROR_HANDLING.md) |

## Layer 6 — Runtime (5 fields)

How the persona initializes, depends on others, and shuts down.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema_version` | string | ✓ | Version of the schema this persona uses |
| `dependencies` | object | ✓ | `required` and `optional` capability-based or persona-based dependencies |
| `context_requirements` | object | ✓ | `required` and `optional` information needed |
| `hooks` | object | optional | Lifecycle: `on_activate`, `on_deactivate`, `on_error` |
| `handoff_protocol` | object | optional | `preferred_targets`, `required_output` for delegation |

## Layer 7 — Improvement (3 fields)

How the persona learns and is extended.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `improvement_feedback` | string[] | ✓ | What feedback helps this persona improve |
| `anti_patterns` | text[] | ✓ | Common mistakes this persona avoids |
| `example_scenarios` | (problem → approach)[] | ✓ | 3-5 representative tasks |

## Complete Field Summary

```
Identity (7)
  name, version, domain, description, primary_role, secondary_roles, inherits, overrides

Competency (4)
  expertise, capabilities, primary_skills, authority_level

Cognition (4)
  thinking_model, reasoning_patterns, decision_framework, prioritization

Behavior (5)
  interaction_pattern, communication_style, output_preferences, quality_gates, output_templates

Governance (5)
  constraints, evaluation_criteria, tool_access, escalation_rules, error_policy

Runtime (5)
  schema_version, dependencies, context_requirements, hooks, handoff_protocol

Improvement (3)
  improvement_feedback, anti_patterns, example_scenarios

Total: 33 fields (7+4+4+5+5+5+3)
```

## Inheritance Rules

1. A persona inherits the full base layer by default
2. Override only fields that differ — explain WHY in `overrides`
3. Each layer can be overridden independently
4. Multiple inheritance is allowed via composition (not chain)
5. Schema version must be declared to validate against the correct spec

## Validation

Every personality MUST pass:

1. **Schema compliance** — all required fields present
2. **Internal consistency** — no field contradicts another
3. **Authority-role match** — authority level is compatible with role
4. **Dependency resolution** — referenced capabilities/skills exist
5. **Hook validity** — referenced hooks exist in runtime
6. **Decision framework consistency** — weights are integers 0-100
