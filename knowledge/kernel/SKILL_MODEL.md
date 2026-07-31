# Skill Model

> Consolidated from: CORE/SKILL_CREATION_GUIDE.md

---

## From: SKILL_CREATION_GUIDE.md

How to create a new skill in the Hermes Personality Framework.

---

## Principle

Skills advertise **capabilities**. Personalities request capabilities.
The capability graph connects them automatically.

A skill should be:
1. **Single responsibility** — does one thing well
2. **Composable** — output can feed into other skills
3. **Deterministic** — same input → same output
4. **Testable** — can verify it works
5. **Documented** — purpose, inputs, outputs, dependencies

## When to Create

```
Task repeated ≥3 times?
  │
  ├─ Yes → Can a skill handle it?
  │          ├─ Yes → Create skill
  │          └─ No  → Create personality that orchestrates existing skills
  │
  └─ No → Can existing skills handle it?
           ├─ Yes → Use existing
           └─ No  → Is it a capability missing from the registry?
                      ├─ Yes → Create skill
                      └─ No  → Revisit: does a capability exist but with different name?
```

## Skill Structure

Every skill follows this structure:

```yaml
name: skill-name
version: 1.0.0
capabilities: ["capability-1", "capability-2"]  # What this skill provides
deterministic: true
tested: true
documented: true
domain: general|specific

depends_on: []          # Skills this skill depends on
conflicts_with: []       # Skills that conflict with this one
cost_estimate: low|medium|high
```

### Skill Document Template

```markdown
# Skill: [Name]

## Purpose
One sentence. What this skill does.

## Capabilities
- `capability-1`: Description
- `capability-2`: Description

## Inputs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| input_1 | string | ✓ | What this input is |
| input_2 | number | | Optional description |

## Outputs
| Field | Type | Description |
|-------|------|-------------|
| result_1 | string | What this output contains |
| result_2 | object | Structure of the result |

## Dependencies
- `skill-name` — why it's needed
- `tool-name` — what external tool

## Workflow
1. Step description
2. Step description
3. Step description

## Validation
How to verify the skill produced correct output:
- Check X
- Validate Y
- Test Z

## Failure Modes
- [Failure] → [What it looks like] → [Recovery]

## Examples
```json
{
  "input": {...},
  "expected_output": {...}
}
```

## Version History
- 1.0.0 — Initial implementation
```

## Skill Capability Registration

When a skill is created, its capabilities must be registered:

```json
{
  "skill-name": ["capability-1", "capability-2"],
  "capability-1": ["skill-name", "other-skill-with-same-capability"]
}
```

Add both directions so the graph can be traversed by capability and by skill.

## Skill Selection Metadata

Skills should expose metadata for the selection algorithm:

```yaml
ranking_metadata:
  relevance: 0.95       # How directly the skill addresses its primary capability
  quality_score: 0.90   # Documentation quality, test coverage
  specificity: 0.80     # 0.0=general, 1.0=very specific
  avg_execution_cost: medium
  last_updated: "2026-07-12"
```

## Capability Naming Convention

Capabilities use kebab-case and follow a verb-noun or domain-action pattern:

```
code-review              ✓ (domain-action)
performance-analysis     ✓ (domain-action)
github-pull-request      ✓ (tool-action)
deep-research            ✓ (modifier-action)
seo-audit                ✓ (domain-action)
```

Avoid:
```
analyze-things           ✗ (too vague)
code                     ✗ (too broad)
do-stuff                 ✗ (meaningless)
```

## Skill Categories

| Category | Examples |
|----------|----------|
| code-analysis | code-review, repository-analysis, static-analysis |
| architecture | architecture-review, dependency-mapping, domain-modeling |
| research | deep-research, source-verification, entity-analysis |
| security | security-review, threat-modeling, vulnerability-scanning |
| testing | unit-testing, integration-testing, benchmark |
| devops | github-management, docker-deployment, ci-config |
| marketing | seo-audit, competitive-analysis, keyword-research |
| writing | documentation, technical-writing, content-creation |
| ai | prompt-engineering, agent-evaluation, mcp-development |
| data | data-analysis, data-visualization, statistical-modeling |
| workflow | automation, orchestration, scheduling |
| infrastructure | cloud-management, docker, linux-administration |

## Anti-Patterns

- **Monster skill** — a skill that does many things. Break into smaller skills.
- **Capability-name mismatch** — skill does A but claims capability B. Be accurate.
- **Hidden dependencies** — skill relies on unstated tools or data. Document everything.
- **No failure modes** — every skill can fail. Document how it does.
- **Over-general** — "analyzes things" is not a capability. Be specific.
- **Undocumented** — if there's no SKILL.md, it doesn't exist.

---
