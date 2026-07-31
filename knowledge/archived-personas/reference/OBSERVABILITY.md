> Originally from CORE/OBSERVABILITY.md

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
