> Originally from CORE/CAPABILITY_REGISTRY.md

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
