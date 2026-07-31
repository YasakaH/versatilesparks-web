# Evaluation Suite v1 — Index
═══════════════════════════════

**Purpose:** Without evaluation, systems get bigger, not better. This is the quality control layer.

---

## Architecture

```
evaluation/
  │
  ├── benchmarks/           ← Golden tasks per domain (permanent, never changes)
  ├── personality-tests/    ← Test definitions per personality
  ├── skill-tests/          ← Test definitions per skill
  ├── regression/           ← Before/after comparison framework
  ├── scoring/              ← Quality scoring rubrics
  └── reports/              ← Historical results
```

## Evaluation Loop

```
Execute Task
  │
  ▼
Compare Output → Expected Output
  │
  ├── Match? → Pass → Update quality score (+)
  └── Mismatch? → Analyze → Score → Flag → Update knowledge
       │
       ▼
    Pass Threshold Met?
       │
       ├── Yes → Register result
       └── No → Flag for improvement
```

## Quality Dimensions

Every evaluation assesses across these dimensions:

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| Reasoning | 20% | Logical flow, consideration of alternatives |
| Architecture | 20% | Structural quality of the solution |
| Accuracy | 20% | Correctness of facts and recommendations |
| Safety | 15% | No harm, no vulnerability introduction |
| Efficiency | 10% | Costs, token usage, latency |
| Communication | 10% | Clarity, structure, appropriate detail |
| Creativity | 5% | Novelty of approach (where appropriate) |
