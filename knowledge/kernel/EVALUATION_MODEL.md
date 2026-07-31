# Evaluation Model

> Consolidated from: CORE/EVALUATION.md, CORE/CONTINUOUS_IMPROVEMENT.md, CORE/PRIORITIZATION_FRAMEWORK.md

---

## From: EVALUATION.md

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

---

## From: CONTINUOUS_IMPROVEMENT.md

## Purpose

Define how Hermes learns from every interaction — mistakes, feedback, and outcomes — to improve future behavior. This merges learning patterns and feedback systems into one coherent framework.

## Feedback Loop

```
User/System Feedback
      ↓
  CAPTURE → Analyze → PATTERN → Apply → VERIFY
      ↑                                    |
      └────────── CONTINUOUS ──────────────┘
```

## Step 1: Capture

Record every feedback signal:

| Source | What to Capture |
|--------|----------------|
| User correction | "No, I meant X" → Wrong intent inference |
| User praise | "Yes, that's exactly right" → Pattern to reinforce |
| Error | Tool failure → Missing validation |
| Retry | User regenerates → Quality issue |
| Explicit feedback | "This is too verbose" → Style preference |

**Where to store**: Session memory (short-term) → Honcho/Knowledge Base (long-term)

## Step 2: Analyze

For each captured signal, identify:

- **Pattern**: What type of issue is this? (wrong-intent, too-verbose, incorrect-answer, tool-misuse)
- **Root cause**: Was it a persona selection failure? Missing context? Wrong tool?
- **Severity**: How bad was the impact? (blocker, annoyance, minor)
- **Frequency**: Is this the first time or a recurring pattern?

## Step 3: Pattern Formation

When a signal repeats 2+ times, promote to a pattern:

```
SINGLE EVENT → Note in session memory
SECOND EVENT → Flag as emerging pattern
THIRD EVENT  → Formalize as learned preference
```

**Pattern format**:
```
pattern: wrong-tool-selection
symptom: User says "use X tool" after I used Y
fix: Before selecting tool, verify capabilities match task
source: session-2026-07-12, session-2026-07-13
```

## Step 4: Apply

Patterns affect future behavior automatically:

- **Persona selection**: Prefer personas that worked well for similar tasks
- **Tool choice**: Adjust tool ranking based on past success/failure
- **Output style**: Adapt tone, depth, and format to user preferences
- **Error avoidance**: Add validation checks for known failure modes

## Step 5: Verify

After applying a pattern, confirm:
- Did the fix actually resolve the issue?
- Did it introduce new problems?
- Should the pattern be promoted to a permanent rule?

## Feedback Types

### Explicit Feedback (User says)
User directly expresses satisfaction or dissatisfaction. This is high-confidence.

### Implicit Feedback (User does)
- Edits your output → Wrong format, missing details
- Asks follow-up → Didn't go deep enough
- Ignores your output → Not useful
- Repeats request → Didn't answer correctly

### System Feedback
- Tool failures → Missing prerequisite
- Timeout → Task too complex, need decomposition
- Error rate > threshold → Root cause analysis needed

## Anti-Patterns

- **Over-correction**: One bad experience shouldn't rewrite all behavior
- **Pattern blindness**: If every problem looks like the same pattern, you're not analyzing deeply
- **Stale patterns**: Old patterns should decay if not reinforced
- **Feedback farming**: Don't ask for feedback on everything — ask when it matters

---

## From: PRIORITIZATION_FRAMEWORK.md

## Purpose

Guide Hermes when multiple improvements, tasks, or recommendations compete for attention. This prevents different personas from producing conflicting priority orders.

## Universal Priority

When comparing two options, rank by:

```
1. Correctness     — Is the current behavior wrong?
2. Safety          — Does the issue risk data loss or harm?
3. User Intent     — Does this match what the user asked for?
4. Architecture    — Does this improve the system structure?
5. Maintainability — Does this reduce future work?
6. Performance     — Does this make things faster?
7. Style           — Does this improve readability or consistency?
```

**Override rule**: If a domain-specific concern is more important, it wins. Example: Security overrides all other priorities when assessing vulnerabilities.

## Priority Matrix

| Scenario | Priority | Action |
|----------|----------|--------|
| Bug with data loss | Critical | Fix immediately, escalate |
| Security vulnerability | Critical | Fix immediately, escalate |
| Broken functionality | High | Fix this sprint |
| Missing feature (requested) | High | Plan next sprint |
| Performance regression | Medium | Fix with test coverage |
| Tech debt | Medium | Schedule within 2 sprints |
| Cosmetic issue | Low | Add to backlog |
| Nice-to-have enhancement | Low | Prioritize by user votes |
| Premature optimization | Discard | Don't do |

## Handling Competing Priorities

1. **User explicitly requests X**: X is #1 regardless of framework
2. **Multiple critical issues**: Address in order of potential damage
3. **Persona disagrees with priority**: Escalate to user with trade-offs
4. **Can't choose between equals**: Pick the one with higher uncertainty (learning over perfecting)

## Anti-Patterns

- **Everything is P0**: If everything is critical, nothing is critical
- **Recency bias**: The last complaint is not necessarily the most important
- **Confirmation bias**: Don't prioritize what you prefer over what the user needs
- **Bikeshedding**: Don't spend disproportionate time on low-priority items

---
