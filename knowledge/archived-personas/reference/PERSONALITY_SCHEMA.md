> Originally from CORE/PERSONALITY_SCHEMA.md

# Personality Schema v2 (Compressed)

Formal schema for the Hermes Personality Framework v2.

**Principle:** Required fields answer "Can Hermes use this safely?"
Optional fields answer "Can Hermes optimize this?"

---

## Required Fields (12)

Every personality MUST have these. No exceptions.

| # | Field | Type | Description |
|---|-------|------|-------------|
| 1 | `id` | string (kebab-case) | Unique identifier, e.g. `security-architect` |
| 2 | `name` | string | Human-readable name, e.g. "Security Architect" |
| 3 | `version` | semver | Current version, e.g. `1.2.0` |
| 4 | `purpose` | text | One-liner describing what this personality does |
| 5 | `category` | enum | Primary domain: engineering, ai, security, product, design, data, business, finance, legal, writing, marketing, operations, education, healthcare, leadership, creative |
| 6 | `inputs` | string[] | What information this personality requires to operate |
| 7 | `outputs` | string[] | What this personality produces |
| 8 | `capabilities` | string[] | Capability IDs this personality provides (from registry) |
| 9 | `owner` | string | Who maintains this personality |
| 10 | `status` | enum | active, deprecated, archived |
| 11 | `created` | date (ISO 8601) | When this personality was created |
| 12 | `updated` | date (ISO 8601) | Last modification date |

### Minimal Example

```yaml
id: security-architect
name: Security Architect
version: 1.0.0
purpose: Review system architectures for security vulnerabilities
category: security
inputs:
  - System architecture description
  - Threat model
outputs:
  - Security assessment report
  - Vulnerability list
  - Remediation recommendations
capabilities:
  - security-review
  - threat-modeling
owner: cog-os
status: active
created: 2026-07-01
updated: 2026-07-12
```

---

## Optional Extension Fields

Add these only when they add value. Not every personality needs them.

### Security Extensions
```yaml
security:
  clearance_level: confidential | restricted | public
  data_handling: string[]
  audit_events: string[]
```

### Evaluation Extensions
```yaml
evaluation:
  success_criteria: string[]
  quality_gates: string[]
  review_frequency: daily | weekly | monthly
```

### Dependencies
```yaml
dependencies:
  required:
    - capability: repository-analysis
  optional:
    - capability: performance-analysis
  skills:
    - architecture-review-skill
```

### Examples
```yaml
examples:
  - task: "Review microservices decomposition"
    expected_workflow:
      - Analyze current architecture
      - Identify coupling patterns
      - Recommend decomposition
    expected_output: "Architecture assessment with risk scoring"
```

### Metrics
```yaml
metrics:
  avg_response_time: 2.3s
  success_rate: 0.95
  cost_per_call: 0.02
  last_100_decisions: 85
```

### Changelog
```yaml
changelog:
  - version: 1.0.0
    date: 2026-07-01
    changes:
      - Initial creation
  - version: 1.1.0
    date: 2026-07-12
    changes:
      - Added threat-modeling capability
      - Updated security clearance
```

---

## Inheritance

Every personality inherits from BASE_PERSONALITY by default. Override only fields that differ.

```yaml
inherits: BASE_PERSONALITY v1.0.0
overrides:
  - purpose: "Specialized for security — narrower mission than base"
  - capabilities: "Security review + threat modeling instead of general engineering"
```

---

## Validation

Every personality MUST pass:

1. **Required fields present** — all 12 required fields have values
2. **Internal consistency** — no field contradicts another
3. **Category exists** — category is from the approved list
4. **Capability resolution** — referenced capabilities exist in the registry
5. **Version format** — valid semver
6. **Dates valid** — ISO 8601 format, created ≤ updated

---

## Summary

| Layer | Count | Purpose |
|-------|-------|---------|
| **Required** | 12 | Safe operation |
| **Extensions** | 6 optional groups | Optimization |
| **Inheritance** | 2 fields | Reuse |
| **Total** | 12 mandatory + optional | |

Required (12): id, name, version, purpose, category, inputs, outputs, capabilities, owner, status, created, updated
