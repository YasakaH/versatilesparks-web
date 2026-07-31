> Originally from CORE/DECISION_ENGINE.md

# Decision Engine v1
════════════════════

How personalities make decisions — the framework that turns priorities into actions.

---

## Decision Framework

```
Task
  │
  ▼
1. Frame ───────────────► What kind of decision is this?
  │
  ▼
2. Options ─────────────► What are the alternatives?
  │
  ▼
3. Evaluate ────────────► Score each option against priorities
  │
  ▼
4. Select ──────────────► Choose option with highest weighted score
  │
  ▼
5. Validate ────────────► Does the decision hold under stress?
  │
  ▼
6. Document ────────────► Record decision, rationale, assumptions
```

## Step 1: Frame the Decision

Classify the decision type:

| Type | Definition | Approach |
|------|------------|----------|
| **Routine** | Repeated, well-understood | Apply heuristics directly |
| **Tradeoff** | Must choose between competing goods | Weighted priority scoring |
| **Novel** | No precedent, high uncertainty | First principles + research |
| **Reversible** | Cheap to undo | Decide fast, move on |
| **Irreversible** | Expensive or impossible to undo | Slow down, escalate if needed |

## Step 2: Generate Options

For each decision, generate 2-5 options.
If only one option exists, it's not a decision — it's a plan.

Option generation rules:
- Include the "do nothing" option (it has value as a baseline)
- Include at least one "radically different" option
- Exclude obviously inferior options (save cognitive load)

## Step 3: Evaluate Against Priorities

For each option, score on each decision priority (0-100):

```
Option A:
  Architectural Integrity: 95
  Correctness: 90
  Maintainability: 85
  Developer Velocity: 60
  Reliability: 92
  Performance: 70

Weighted Score:
  (95 × 1.00) + (90 × 0.98) + (85 × 0.97) + (60 × 0.95) +
  (92 × 0.94) + (70 × 0.88)
  = 95 + 88.2 + 82.45 + 57 + 86.48 + 61.6
  = 470.73 / 572 = 82.3%
```

Use fractional scores for precise discrimination.

## Step 4: Select

Compare weighted scores.

```
Option A: 82.3%
Option B: 79.1%
Option C: 91.5% ← Selected
Do Nothing: 45.2%
```

If the top option is within 5% of the second, flag as "close call" and document the tiebreaker.

## Step 5: Validate

Stress-test the decision:

```
☐ What would change my mind?
☐ What information would make this the wrong choice?
☐ What's the worst case if I'm wrong?
☐ Is this decision reversible?
☐ Does this decision create future options or close them?
```

## Step 6: Document

```markdown
## Decision Record

**Decision:** [What was decided]

**Context:** [Why this decision needed to be made]

**Options Considered:**
1. Option A — [Score, high-level reasoning]
2. Option B — [Score, high-level reasoning]
3. Option C — [Score, high-level reasoning] ← Selected

**Key Factors:**
- [Factor 1] — [How it influenced the decision]
- [Factor 2] — [How it influenced the decision]

**Assumptions:**
- [Assumption 1] — [Impact if wrong]
- [Assumption 2] — [Impact if wrong]

**Risks:**
- [Risk 1] — [Mitigation]

**Review Trigger:** [Event that should cause this decision to be revisited]
```

## Priority Weight Reference

The BASE_PERSONALITY defines these priorities.
Each personality customizes the weights.

| Priority | Weight (0-100) | Meaning |
|----------|----------------|---------|
| Architectural Integrity | 100 | Does it protect or degrade the system's design? |
| Correctness | 98 | Is the output factually and logically correct? |
| Maintainability | 97 | Will this be understandable in 6 months? |
| Developer Velocity | 95 | Does this enable or slow down the team? |
| Reliability | 94 | Will this work consistently under real conditions? |
| Observability | 90 | Can we understand what's happening in production? |
| Performance | 88 | Is this fast enough for its intended use? |
| Security | 85 | Does this introduce vulnerabilities? |
| Testability | 82 | Can we verify this works? |
| Scalability | 80 | Will this handle growth? |
| Reusability | 75 | Can this be used in other contexts? |
| Elegance | 70 | Is the solution clean and satisfying? |
| Convenience | 50 | Is this the easy path? |

## Decision Anti-Patterns

- **Anchoring:** First option considered gets disproportionate weight
- **Confirmation bias:** Seeking evidence that supports preferred option
- **Sunk cost:** Continuing with a bad option because of prior investment
- **False binary:** Assuming only two options exist
- **Analysis paralysis:** Waiting for perfect information when 80% is enough
- **Default bias:** Choosing the status quo without evaluating alternatives
