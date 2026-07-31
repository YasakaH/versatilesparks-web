### CORE/EVOLUTION_ENGINE.md

# Evolution Engine v1
══════════════════════

Hermes continuously improves itself through systematic analysis of its own performance.

---

## Weekly Evolution Cycle

Every week, the Evolution Engine runs:

```
Collect Data (7 days of traces)
  │
  ▼
Analyze Patterns
  │
  ├── Which skills were never used?    → Archive or merge
  ├── Which personalities overlap?     → Merge or redirect
  ├── Which workflows repeat?          → Template → Playbook
  ├── Which failures repeat?           → Improve → Skill
  ├── Which bottlenecks exist?         → Optimize
  ├── Which costs are highest?         → Optimize routing
  └── Which confidence is lowest?      → Improve → Retrain
  │
  ▼
Generate Recommendations
  │
  ▼
Apply Automated Improvements
  │
  ▼
Review Manual-Suggested Improvements
  │
  ▼
Measure Impact (next week's data)
```

## Improvement Categories

### Skills
```
SKILL_NEVER_USED      → Archive (keep for reference, remove from active registry)
SKILL_LOW_CONFIDENCE  → Improve documentation, add examples, fix failure modes
SKILL_HIGH_COST       → Optimize token usage, find cheaper alternative
SKILL_DUPLICATES      → Merge with overlapping skill
SKILL_HIGH_ERROR      → Debug root cause, improve validation
SKILL_MISSING         → Create from repeated task pattern
```

### Personalities
```
PERSONALITY_NEVER_USED      → Archive
PERSONALITY_OVERLAP         → Merge with overlapping personality or clarify boundaries
PERSONALITY_LOW_SUCCESS     → Improve mental models, decision priorities, skill selection
PERSONALITY_HIGH_COST       → Optimize workflow, reduce unnecessary skill invocations
PERSONALITY_MISSING         → Create from personality creation guide
```

### Workflows
```
WORKFLOW_REPEATED_3x  → Template → Playbook
WORKFLOW_FAILING      → Debug failure points, add validation, add fallback skills
WORKFLOW_SLOW         → Parallelize independent steps, optimize skill selection
```

### Knowledge
```
OUTDATED_KNOWLEDGE    → Flag for review
MISSING_KNOWLEDGE     → Create from research
CONTRADICTORY         → Resolve or escalate
```

## Self-Correction Rules

### When a skill fails:
```
Skill fails
  │
  ├── Retry (up to 3x)
  │     └── Succeeds → Log as recovered failure
  │
  └── Fails after retries
        ├── Is alternative skill available? → Use fallback
        └── No alternative → Flag for creation
```

### When confidence is low:
```
Confidence < 0.6
  │
  ├── Can additional evidence be obtained? → Research
  ├── Can alternative personality produce better result? → Switch
  └── Neither → Flag as low-confidence output, mark for improvement
```

### When cost exceeds budget:
```
Cost > Budget
  │
  ├── Can a cheaper model be used? → Re-route
  ├── Can fewer skills be invoked? → Reduce scope
  ├── Can the prompt be optimized? → Reduce token usage
  └── None of above → Escalate with cost analysis
```

## Trigger Conditions

| Trigger | Action | Automation |
|---------|--------|------------|
| Skill unused for 30 days | Archive skill | Auto |
| Skill error rate > 10% | Flag for review | Auto (flag) |
| 3 identical task patterns | Create playbook | Suggest |
| 5 identical task patterns | Auto-create playbook | Auto |
| Personality never selected | Archive | Auto (after 45 days) |
| Personality > 30% overlap | Flag for merge | Suggest |
| Cost per request increased 50% | Alert + analyze | Auto (alert) |
| Confidence trending down | Alert + retrain | Auto (alert) |
| Repeated failure mode | Create prevention skill | Suggest |
| New domain emerges | Suggest new personality | Suggest |

## Evolution Score

Weekly health score (0-100):

```
Evolution Score = (Success Rate × 25) +
                 (Skill Utilization × 15) +
                 (Personality Utilization × 15) +
                 (Cost Efficiency × 15) +
                 (Confidence Average × 15) +
                 (Improvement Velocity × 15)
```

- **Success Rate:** % of tasks completed without error or escalation
- **Skill Utilization:** % of registered skills used in the last week
- **Personality Utilization:** % of personalities selected at least once
- **Cost Efficiency:** average cost per successful task vs. benchmark
- **Confidence Average:** average confidence across all outputs
- **Improvement Velocity:** new skills + improved personalities / week


### CORE/OBSERVABILITY.md

# Observability Framework v1
════════════════════════════

Every execution is instrumented. Every decision is traceable. Every failure is analyzable.

---

## What To Observe

### Per-Request
```yaml
request:
  id: uuid
  timestamp: ISO-8601
  user_intent: string
  intent_decomposition: string[]
  success_criteria: string[]
  constraints: string[]
```

### Per-Execution
```yaml
execution:
  id: uuid
  request_id: uuid
  personality_selected: string
  supporting_personalities: string[]
  capability_plan: capability[]
  execution_dag: DAG-structure
  total_duration_ms: int
  total_cost_tokens: int
  model_routing: {task: model}[]
```

### Per-Skill
```yaml
skill_invocation:
  id: uuid
  execution_id: uuid
  skill_name: string
  input: json
  output: json
  duration_ms: int
  tokens_used: int
  confidence: float
  success: boolean
  error: string | null
  retry_count: int
```

### Per-Personality
```yaml
personality_invocation:
  id: uuid
  execution_id: uuid
  personality_name: string
  role: primary|supporting|reviewer
  reasoning_summary: string
  quality_gates_passed: string[]
  quality_gates_failed: string[]
  conflicts_resolved: int
  conflicts_escalated: int
  output: json
```

### Quality
```yaml
quality_check:
  id: uuid
  execution_id: uuid
  gate_name: string
  passed: boolean
  details: string
```

### Learning
```yaml
learning_event:
  id: uuid
  execution_id: uuid
  event_type: skill_missing|personality_overlap|workflow_repeated|failure_pattern
  description: string
  recommendation: string
  actionable: boolean
```

## Trace Structure

Every execution produces a trace:

```json
{
  "trace_id": "uuid",
  "request": {...},
  "execution": {...},
  "skills": [...],
  "personalities": [...],
  "quality_checks": [...],
  "learning_events": [...],
  "cost": {
    "total_tokens": 12450,
    "total_cost_usd": 0.37,
    "model_breakdown": {"gpt-4o": 8900, "claude-sonnet": 3550}
  },
  "duration_ms": 23400,
  "conclusion": "success|failure|partial"
}
```

## Aggregation

### Hourly/Daily Aggregations
- Success rate by personality
- Average cost per request
- Most-used skills
- Most common failure modes
- Average confidence per domain
- Popular models by task type

### Weekly/Monthly
- Trend: success rate over time
- Trend: cost per request over time
- Skill usage heatmap
- Personality effectiveness (success rate × speed × cost)
- Learning velocity (new skills created, personalities improved)
- Regression detection (did anything get worse?)

## Alerting Thresholds

```yaml
alerts:
  error_rate_above: 0.10         # >10% error rate → alert
  cost_spike_above: 2.0          # >2x normal cost → alert
  confidence_below: 0.6          # Average confidence below 0.6 → alert
  duration_above_ms: 120000      # >2min for any request → investigate
  retry_count_above: 5           # >5 retries for any skill → investigate
```

## Storage

Traces stored in structured logs (JSONL):
```
/traces/YYYY/MM/DD/HH/mm-trace-id.json
```

Aggregations:
```
/metrics/hourly/YYYY-MM-DD-HH.json
/metrics/daily/YYYY-MM-DD.json
/metrics/weekly/YYYY-Www.json
```

## Query Examples

```json
// Find all failed executions in the last hour
GET /observability/failures?since=1h

// Find slowest skills this week
GET /observability/skills/slowest?period=week&limit=10

// Cost by personality this month
GET /observability/cost/by-personality?period=month

// Most common failure reasons
GET /observability/failures/reasons?period=day

// Learning events not yet actioned
GET /observability/learning/pending
```

## Observability Anti-Patterns

- **Logging everything without structure** — raw logs are noise without a schema
- **No aggregation** — millions of individual traces with no summary
- **Ignoring trends** — only looking at individual executions, not patterns
- **No alerting** — systems degrade slowly; without alerts you won't notice
- **Cost blindness** — not knowing which personalities or skills cost the most
- **Feedback loops not closed** — observing problems but never fixing them


### CORE/EVALUATION.md

# Evaluation Suite v1
══════════════════════

Standardized benchmarks for every personality and skill.

---

## Personality Benchmarks

Every personality must pass benchmark tasks for its domain.

### Format
```yaml
benchmark:
  personality: principal-engineer
  version: 1.0.0
  
  tasks:
    - id: arch-review-001
      name: "Monolith decomposition recommendation"
      input: "10-service monolith, team of 12 engineers, 3-year codebase"
      expected_workflow:
        - repository-analysis
        - architecture-review
        - dependency-mapping
      expected_output_types:
        - bounded_contexts
        - interface_contracts
        - migration_plan
      quality_gates:
        - loose_coupling_improved: boolean
        - interface_stability: boolean
        - migration_failure_modes: boolean
      pass_criteria:
        - "All expected workflow skills invoked"
        - "All quality gates pass"
        - "No constitution violations"
  
    - id: tech-debt-002
      name: "Technical debt assessment"
      input: "Python monolith, 500K LOC, 80% test coverage"
      expected_workflow:
        - repository-analysis
        - technical-debt-analysis
        - code-review
      quality_gates:
        - debt_categorized: boolean
        - remediation_prioritized: boolean
        - tradeoffs_documented: boolean
```

### Benchmark Categories

| Category | Tasks | Pass Criteria |
|----------|-------|---------------|
| Engineering | 10 tasks | All skills invoked, all quality gates pass |
| Architecture | 8 tasks | Clear boundaries, documented tradeoffs |
| AI | 8 tasks | Reliable outputs, cost budgets respected |
| Research | 6 tasks | Evidence hierarchy respected |
| Security | 6 tasks | Threats identified, mitigations proposed |
| Marketing | 5 tasks | Audience defined, positioning clear |

## Skill Benchmarks

Every skill must pass unit tests for its inputs/outputs.

```yaml
skill_benchmark:
  skill: architecture-review
  version: 1.0.0
  
  tests:
    - id: arch-unit-001
      name: "Two-service dependency analysis"
      input: {repos: ["service-a", "service-b"]}
      expected_output_contains: ["dependency", "interface", "coupling"]
      expected_confidence_above: 0.7
  
    - id: arch-unit-002
      name: "Empty repository"
      input: {repos: []}
      expected_error: "No repository data provided"
  
    - id: arch-unit-003
      name: "Large monolith (100K LOC)"
      input: {repos: ["monolith"], analysis_depth: "shallow"}
      expected_duration_below_ms: 30000
      expected_output_contains: ["boundaries", "recommendations"]
```

## Regression Detection

Run benchmarks weekly. Alert on:
- Personality success rate drop > 10%
- Skill failure rate increase > 5%
- Confidence score drop > 0.15
- Duration increase > 50%
- Cost increase > 50%

## New Personality Validation

Before a new personality is registered:

1. **Schema validation** — all required fields present
2. **Constitution check** — no violations
3. **Quality gate test** — all gates defined and testable
4. **Benchmark execution** — pass 3 domain-specific tasks
5. **Conflict check** — doesn't duplicate existing personality
6. **Registration** — added to capability registry



## Question
Review this chunk. What improvements, gaps, or issues do you see?