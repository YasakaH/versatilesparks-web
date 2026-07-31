# Capability Model

> Consolidated from: CORE/CAPABILITY_REGISTRY.md, CORE/SKILL_SELECTION_POLICY.md

---

## From: CAPABILITY_REGISTRY.md

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
# Find skills by capability
multica capability query architecture-review

# Find capabilities by skill
multica capability reverse skill-id

# Check coverage
multica capability coverage
```

## Registry Update Rules

1. When a new skill is registered, its capabilities are added to the graph
2. When a skill is deprecated, its capabilities are removed (with orphan check)
3. Multiple skills can provide the same capability (scoring decides)
4. A skill can provide multiple capabilities
5. Capability quality scores are updated based on execution feedback

---

## From: SKILL_SELECTION_POLICY.md

How personalities select which skills to invoke for a given task.

---

## Selection Algorithm

### Step 1: Deterministic Rules (apply first, no scoring)

Rules checked in order. First match wins.

```
IF security or safety implication        → route to Security Architect
IF architecture or design decision       → route to Systems Architect
IF business + technology tradeoff        → route to CTO
IF user needs learning/explanation       → route to Educator
IF code review needed                    → route to Technical Reviewer
IF data analysis required                → route to Data Scientist
```

### Step 2: Capability Match (when no deterministic rule fires)

```
Task
  │
  ▼
1. Decompose ──────────────► Break task into sub-problems
  │
  ▼
2. Map to Capabilities ────► Each sub-problem → required capability
  │
  ▼
3. Query Registry ─────────► Find skills that provide each capability
  │
  ▼
4. Filter Candidates ──────► Apply exclusion rules (cost, test coverage, version)
  │
  ▼
5. Select ─────────────────► If 1 candidate → execute it
                          If >1 candidate AND 100+ historical routing decisions exist → score
                          If >1 candidate AND <100 decisions → use domain-priority order
  │
  ▼
6. Execute ────────────────► Determine mode: Direct / Collaborative / Orchestrated
```

### Step 3: Scoring (only as tiebreaker after 100+ routing decisions)

Scoring is used ONLY when deterministic rules and capability matching leave multiple candidates AND 100+ routing decisions exist to validate weights.

| Dimension | Priority | Description |
|-----------|----------|-------------|
| Relevance | High | How directly the skill addresses the capability |
| Quality | Medium | Skill's track record, documentation, testing |
| Specificity | Medium | General vs. domain-specific (prefer specific) |
| Cost | Low | Execution cost (tokens, time, API calls) |
| Freshness | Low | Last updated — prefer current skills |

**Anti-pattern:** The 40/30/20/10 scoring formula creates an illusion of precision. Do not use weighted scoring before 100+ routing decisions validate the weights against real outcomes.

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

### Rule 5: Combine Using Execution Modes
```
Single skill sufficient? → Execute it (Direct mode)
Multiple skills, no dependencies? → Execute in parallel (Collaborative mode)
Multiple skills, dependencies exist? → Plan DAG (Orchestrated mode)
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

- **Skill shopping:** Trying every matching skill instead of picking one. Filter first, pick once.
- **Over-selection:** Invoking 5 skills when 2 suffice. Start minimal, expand only when results are insufficient.
- **Premature fallback:** Jumping to tier_2 before tier_1 completes. Let tier_1 finish before falling back.
- **Ignoring cost:** Always picking the most expensive skill. Consider whether the cheapest sufficient skill works first.
- **False precision:** Using weighted scoring before collecting 100+ data points. The weights are meaningless without history.

---

## Registry Update Rules (combined)

1. When a new skill is registered, its capabilities are added to the graph
2. When a skill is deprecated, its capabilities are removed (with orphan check)
3. Multiple skills can provide the same capability (scoring decides)
4. A skill can provide multiple capabilities
5. Capability quality scores are updated based on execution feedback
