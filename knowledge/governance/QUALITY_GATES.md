# Quality Gates

> Consolidated from: CORE/QUALITY_GATES.md, CORE/QUALITY_STANDARDS.md, CORE/OUTPUT_STANDARD.md, CORE/OBSERVABILITY.md

---

## From: QUALITY_GATES.md

Universal quality gates every output must pass.

---

## Gate Descriptions

| # | Gate | Question | Verifiable? |
|---|------|----------|-------------|
| 1 | Correct | Does the output correctly solve the stated problem? | ✓ |
| 2 | Complete | Are all required sections present? | ✓ |
| 3 | Verified | Are claims backed by evidence or explicit confidence? | ✓ |
| 4 | Source-backed | Are data sources cited and verifiable? | ✓ |
| 5 | Deterministic | Would the same input produce the same output? | Depends |
| 6 | Maintainable | Will this output still be useful in 6 months? | Subjective |
| 7 | Minimal | Does every element serve a purpose? | Subjective |
| 8 | Reusable | Can this output be repurposed for similar tasks? | Subjective |
| 9 | Safe | Does the output avoid harmful recommendations? | ✓ |
| 10 | Actionable | Does the output enable someone to act? | ✓ |

## Gate Details

### Gate 1: Correct
- Output addresses the exact problem stated
- No off-topic content
- No factual errors
- No logical contradictions

### Gate 2: Complete
- All template sections present
- No "TODO" markers
- No "I'll add later" disclaimers
- No required fields left blank

### Gate 3: Verified
- Every factual claim traces to a source
- Claims without sources are labeled as "experience" or "assumption"
- Uncertainty is explicitly stated
- Confidence level is provided

### Gate 4: Source-backed
- Sources are cited with enough detail to find them
- Primary sources preferred over secondary
- Source quality is noted (official doc, community, blog, LLM output)
- Conflicting sources are identified and resolved

### Gate 5: Deterministic
- Output format is consistent for same input type
- No random variation in structure
- Conditional branches are rule-based, not arbitrary
- If probabilistic elements exist, they're identified

### Gate 6: Maintainable
- Output would make sense to someone reading it 6 months later
- Reasoning is documented, not just conclusions
- Assumptions are called out (assumptions change over time)
- Dependencies on current tools/versions are noted

### Gate 7: Minimal
- No redundant information
- No fluff or filler
- Every paragraph serves the analysis
- "If in doubt, leave it out" — unless it's a required section

### Gate 8: Reusable
- Output structure follows the personality's template
- Key findings are extracted for cross-reference
- Output can be fed into downstream systems
- Format is machine-parseable where useful

### Gate 9: Safe
- No dangerously incomplete recommendations
- No security vulnerabilities introduced
- No privacy violations
- No legal/ethical violations
- Safety warnings are prominent, not buried

### Gate 10: Actionable
- Each recommendation includes a concrete next step
- Reader knows exactly what to do next
- Prerequisites and dependencies are stated
- Effort estimates are provided
- Success criteria are defined

## Personality-Specific Gates

In addition to universal gates, each personality defines domain-specific gates.
These are documented in the personality's QUALITY.md.

**Example (Security Engineer):**
```
□ Threat modeled
□ Secrets protected
□ Least privilege verified
□ Logging and monitoring considered
□ Input validation confirmed
□ Authentication/authorization verified
□ Encryption at rest and in transit
□ Recovery tested
```

**Example (Marketing Strategist):**
```
□ Target audience defined
□ Positioning clear and differentiated
□ Messaging reduces uncertainty
□ Channels selected based on audience behavior
□ Success metrics defined (not vanity)
□ Budget constraint respected
□ Competitive response anticipated
```

## Gate Failing Protocol

When a gate fails:

```
Gate Failed
  │
  ▼
Is it critical? ────Yes────► Fix before output
  │
  No
  │
  ▼
Is it fixable? ────Yes────► Fix
  │
  No
  │
  ▼
Document:
  - Which gate failed
  - Why
  - Impact of failure
  - Recommendation for future
  - Escalate if appropriate
```

---

## From: QUALITY_STANDARDS.md

## Purpose

Define the quality gates every Hermes output must pass. These are not aspirational — they are the minimum bar. Every persona inherits these standards and may add domain-specific gates on top.

## Universal Quality Gates

Every output (code, document, response, plan) must satisfy:

1. **Correctness** — Does it do what was asked?
2. **Safety** — Does it avoid harm, data loss, or irreversible damage?
3. **Clarity** — Can the user understand it without asking follow-ups?
4. **Completeness** — Does it answer the full question, not just part?
5. **Conciseness** — Is it as short as it can be without losing meaning?

## Technical Quality Gates

For code, architecture, and system outputs:

| Gate | Check | Fail if |
|------|-------|---------|
| Correctness | Does the code compile/pass tests? | Any test failure |
| Security | Any OWASP Top 10 violations? | Hardcoded secrets, injection vectors |
| Performance | Acceptable latency/complexity? | Nested loops over large datasets unnecessarily |
| Maintainability | Clean code, comments, patterns? | Deeply nested, no error handling |
| Testability | Can this be tested? | Tight coupling, global state |
| Observability | Errors logged? Metrics emitted? | Silent failures |
| Backward compatibility | Breaks existing interfaces? | Breaking API changes without migration |
| Idempotency | Safe to run multiple times? | Side effects on re-run |

## Content Quality Gates

For writing, documentation, and communication:

| Gate | Check | Fail if |
|------|-------|---------|
| Accuracy | Facts verified? | Hallucinations, outdated info |
| Structure | Logical flow? Headings, sections? | Wall of text |
| Tone | Appropriate for audience? | Too casual for executive, too formal for peer |
| Actionability | Does user know what to do next? | Vague conclusions |
| Attribution | Sources cited? | Claims without evidence |
| Formatting | Markdown, code blocks, lists? | Unreadable formatting |

## Domain-Specific Extensions

Quality gates can be extended per persona domain:

- **Security**: + penetration test, threat model review, compliance check
- **Finance**: + double-entry verification, audit trail, regulatory compliance
- **Legal**: + jurisdiction check, precedent validation, liability review
- **Medical** (if added): + peer review, evidence grading, privacy check

## Quality Levels

```
LEVEL 0 — Draft
  Internal only. May have errors. No gate checks required.

LEVEL 1 — Standard
  User-facing output. All Universal gates must pass.

LEVEL 2 — Reviewed
  Important decisions, arch changes, public content.
  Universal + Technical gates. Second persona review recommended.

LEVEL 3 — Critical
  Production changes, security policies, financial decisions.
  All gates. Mandatory second persona review. Escalation if fails.
```

## Escalation

If an output cannot pass quality gates:

1. Document which gates failed and why
2. Return to EXECUTION step in EXECUTION_WORKFLOW.md
3. If blocked > 2 attempts, escalate to user with options

## Anti-Patterns

- **Quality theater**: Checking boxes without actually verifying
- **Perfectionism**: Level 1 output doesn't need Level 3 gates
- **Rubber-stamping**: "Looks good" without actual review
- **Context-blindness**: Applying security gates to a draft README

---

## From: OUTPUT_STANDARD.md

Standardized output format for all personalities.

---

## Output Requirements

Every output MUST be:
1. **Structured:** Follows the personality's output template
2. **Verifiable:** Claims are backed by evidence or confidence levels
3. **Actionable:** Recommendations include concrete next steps
4. **Complete:** All required sections are present
5. **Self-contained:** Can be understood without reference to the conversation

## Standard Output Sections

### Header
```markdown
## [Personality Name] — [Task Summary]
**Confidence:** [High/Medium/Low/Speculative]
**Analysis time:** [Duration]
```

### Executive Summary
```markdown
## Summary
[3-5 bullet points covering: problem, finding, recommendation, risk, confidence]
```

### Analysis
```markdown
## Analysis
[Detailed findings organized by capability or workflow step]
```

### Recommendations
```markdown
## Recommendations
### Priority 1 (Do First)
- **[Action]** — Rationale, impact, effort estimate

### Priority 2 (Do Next)
- **[Action]** — Rationale, impact, effort estimate

### Priority N (Consider Later)
- **[Action]** — Rationale, impact, effort estimate
```

### Tradeoffs
```markdown
## Tradeoffs
| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| A | ... | ... | Recommended |
| B | ... | ... | Not recommended |
```

### Risks
```markdown
## Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ... | High/Med/Low | High/Med/Low | ... |
```

### Quality Gates
```markdown
## Quality Checklist
- [x] Solves original problem
- [x] Preserves architecture
- [ ] Edge cases documented
- [x] Failure modes identified
```
(Unchecked items require explanation)

### Appendix
```markdown
## Appendix
- Sources consulted
- Assumptions made
- Skills invoked
- Open questions
```

## Plain Text Output

When markdown is not available, use this structure:

```
TITLE: [Brief]
PERSONALITY: [Name]
CONFIDENCE: [Level]

FINDING
[Key finding]

RECOMMENDATION
[Key recommendation]

REASONING
[Brief reasoning]
```

## Output Anti-Patterns

- ❌ **Wall of text** — one paragraph for everything
- ❌ **Vague recommendations** — "improve performance" without specifics
- ❌ **Unlabeled confidence** — claiming something is true without stating certainty
- ❌ **Hidden assumptions** — decisions based on unstated premises
- ❌ **Missing tradeoffs** — only presenting the recommended option
- ❌ **Certainty without evidence** — "this is the best approach" without data
- ❌ **Ignoring escalation needs** — proceeding when the decision needed user input

---

## From: OBSERVABILITY.md

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

---
