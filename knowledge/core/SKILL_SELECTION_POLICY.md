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
