### CORE/CAPABILITY_REGISTRY.md

# Capability Registry v1
═════════════════════════

The registry connects capabilities (what needs to be done) to skills (how it gets done).
Personalities request capabilities. Skills advertise capabilities. The registry maps between them.

---

## Registry Schema

### Capability Entry
```yaml
capability:
  id: architecture-review          # Unique identifier
  description: "Evaluate system architecture for quality, coupling, and scalability"
  
  provided_by:                     # Skills that provide this capability
    - architecture-review-skill
    - codebase-review-skill        # Alternative with same capability
  
  requires:                        # Prerequisite capabilities
    - repository-analysis
  
  quality_score: 0.95              # Average quality of available implementations
  latency: low                     # Typical execution latency
  parallelizable: true             # Can run concurrently with other capabilities
  cost: medium                     # Token/compute cost
  confidence: high                 # Output reliability
```

### Skill Registration
```yaml
skill:
  id: architecture-review-skill
  version: 1.2.0
  
  capabilities:                    # All capabilities this skill provides
    - architecture-review
    - scalability-analysis
    - modularity-assessment
  
  inputs:
    repository_path: string
    analysis_depth: enum [shallow, deep]
  
  outputs:
    architecture_score: float
    recommendations: string[]
    risks: string[]
  
  dependencies:
    - repository-analysis-skill
  
  quality_score: 0.95
  latency: low
  parallelizable: true
  cost: medium
  deterministic: true
  tested: true
  
  metadata:
    owner: "cog-os"
    last_updated: "2026-07-12"
    test_coverage: 0.92
    documentation_url: "/skills/architecture-review"
```

## Capability Catalog

### Engineering Capabilities
| Capability | Skills | Parallel? |
|------------|--------|-----------|
| repository-analysis | repository-analysis | No (foundation) |
| architecture-review | architecture-review, codebase-review | Yes |
| code-review | code-review, requesting-code-review | Yes |
| performance-analysis | latency-analysis, performance-first, benchmarking | Yes |
| dependency-mapping | dependency-mapping, dependency-graph | Yes |
| technical-debt-analysis | technical-debt, simplify-code | Yes |
| testing | testing, tdd, test-driven-development | Yes |
| domain-modeling | domain-modeling, ubiquitous-language | Yes |

### AI Capabilities
| Capability | Skills | Parallel? |
|------------|--------|-----------|
| prompt-engineering | prompt-engineering, prompt-review | Yes |
| agent-evaluation | agent-evaluation, ai-evaluator | Yes |
| mcp-development | mcp-builder | No (foundation) |
| workflow-automation | workflow-automation, n8n-builder | Yes |

### Research Capabilities
| Capability | Skills | Parallel? |
|------------|--------|-----------|
| deep-research | deep-research | No (foundation) |
| source-verification | source-tracker, fact-checking | Yes |
| entity-analysis | entity-research, entity-research-skill | Yes |
| fact-checking | fact-checker, academic-reviewer | Yes |

### Security Capabilities
| Capability | Skills | Parallel? |
|------------|--------|-----------|
| security-review | security-review, security-audit | Yes |
| threat-modeling | threat-modeler | Yes |
| vulnerability-scanning | security-scan | Yes |

### Infrastructure Capabilities
| Capability | Skills | Parallel? |
|------------|--------|-----------|
| github-management | github-pr-workflow, github-issues, github-auth | Yes |
| containerization | docker-management | Yes |
| deployment | ci-cd-workflow | No (sequential) |

## Registry Query

```bash
# Find skills for a capability
capability: architecture-review
→ architecture-review-skill (score: 0.95)
→ codebase-review-skill (score: 0.88)

# Find capabilities of a skill
skill: performance-engineer
→ performance-analysis
→ benchmarking
→ latency-optimization
```

## Scoring Model v2

### Base Capability Score

```
Capability Score =
  quality       × 0.30
+ reliability   × 0.20
+ domain_fit    × 0.15
+ safety        × 0.15
+ speed         × 0.10
+ cost          × 0.05
+ recency       × 0.05
```

### Context-Adaptive Weighting

Instead of fixed weights, weights adapt to task type:

| Task Type | quality | reliability | domain_fit | safety | speed | cost | recency |
|-----------|---------|-------------|------------|--------|-------|------|---------|
| Architecture review | 0.55 | 0.25 | 0.10 | 0.05 | 0.05 | 0 | 0 |
| Quick code | 0.25 | 0.20 | 0.10 | 0.10 | 0.35 | 0 | 0 |
| Security audit | 0.30 | 0.20 | 0.15 | 0.30 | 0.05 | 0 | 0 |
| Content creation | 0.40 | 0.15 | 0.10 | 0.05 | 0.10 | 0.10 | 0.10 |

### Multipliers

```
Final Score = Base Capability Score × User Alignment × Context Fit
```

**User Alignment** — matches user preferences:
```yaml
user_alignment:
  explanation_style: 0.9    # 0.0-1.0
  verbosity_match: 0.8
  preferred_tools: 0.7
  coding_style_match: 0.9
```

**Context Fit** — matches current task context:
```yaml
context:
  task_type: architecture-review
  urgency: low
  dependencies: [repository-analysis]
```

### Skill Selection Pipeline

```
Candidate Skills
      |
      v
Capability Match (raw capability score)
      |
      v
Context Fit (current task, urgency, dependencies)
      |
      v
Persona Preference (persona's tier_1/tier_2/tier_3)
      |
      v
Cost/Safety Constraints (authority check)
      |
      v
Selected Skill
```

## Ranking

Skill ranking is computed dynamically:

```
Skill Score =
  Capability Match  × 0.40
+ Context Fit       × 0.25
+ Reliability       × 0.15
+ Safety            × 0.10
+ User Preference   × 0.10
```

This replaces static tier assignment with context-aware ranking.

## Registry Update Rules
1. When a new skill is registered, its capabilities are added to the graph
2. When a skill is deprecated, its capabilities are removed (with orphan check)
3. Multiple skills can provide the same capability (scoring decides)
4. A skill can provide multiple capabilities
5. Capability quality scores are updated based on execution feedback


### CORE/SKILL_CREATION_GUIDE.md

# Skill Creation Guide v1
═════════════════════════

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


### CORE/SKILL_SELECTION_POLICY.md

# Skill Selection Policy v1
═══════════════════════════

How personalities select which skills to invoke for a given task.

---

## Selection Algorithm

```
Task
  │
  ▼
1. Decompose ──────────────► Break task into sub-problems
  │
  ▼
2. Map to Capabilities ───► Each sub-problem → required capability
  │
  ▼
3. Query Registry ────────► Find skills that provide each capability
  │
  ▼
4. Score Candidates ──────► Rank matching skills
  │
  ▼
5. Select ─────────────────► Pick best skill for each capability
  │
  ▼
6. Plan Execution ────────► Determine order and parallelism
```

## Scoring Criteria

Each candidate skill is scored on these dimensions:

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Relevance | 40 | How directly the skill addresses the capability |
| Quality | 25 | Skill's track record, documentation, testing |
| Specificity | 20 | General vs. domain-specific (prefer specific) |
| Cost | 10 | Execution cost (tokens, time, API calls) |
| Freshness | 5 | Last updated — prefer current skills |

### Scoring Formula
```
Score = (Relevance × 0.40) + (Quality × 0.25) +
        (Specificity × 0.20) + (Cost_Score × 0.10) +
        (Freshness × 0.05)
```

## Selection Rules

### Rule 1: Prefer Specific Over General
A domain-specific skill beats a general-purpose skill every time.
`performance-review` > `general-analysis` when analyzing performance.

### Rule 2: Prefer Verified Over Claimed
A skill with test coverage beats one without.
A skill with documented outputs beats one without.

### Rule 3: Prefer Deterministic Over Probabilistic
Skills that produce the same output for the same input are preferred.
If a probabilistic skill is needed, run it twice and compare.

### Rule 4: Tiered Fallback
```
tier_1 available? → Execute tier_1
tier_1 unavailable? → Execute tier_2
tier_2 unavailable? → Execute tier_3
no tier matches? → Execute fallback
fallback fails? → Escalate
```

### Rule 5: Combine When Necessary
```
Single skill sufficient? → Execute it
Multiple skills needed? → Plan DAG
Skills overlap? → Deduplicate by preferring highest-ranked
```

## Skill Quality Attributes

Skills expose these attributes for ranking:

```yaml
purpose: "What this skill does"
capabilities: ["capability-1", "capability-2"]  # What it provides
deterministic: true                              # Same input → same output
tested: true                                     # Has test coverage
documented: true                                 # Has full documentation
domain: "general" | "specific"                   # Breadth of applicability
version: "1.2.0"                                 # Current version
cost_estimate: "low" | "medium" | "high"         # Relative execution cost
```

## Anti-Patterns in Skill Selection

- **Skill shopping:** Trying every matching skill instead of scoring and picking. Score once, execute the best.
- **Over-selection:** Invoking 5 skills when 2 suffice. Start minimal, expand only when results are insufficient.
- **Premature fallback:** Jumping to tier_2 before tier_1 completes. Let tier_1 finish before falling back.
- **Ignoring cost:** Always picking the most expensive skill. Consider whether the cheapest sufficient skill works first.



## Question
Review this chunk. What improvements, gaps, or issues do you see?