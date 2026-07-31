> Originally from CORE/EVOLUTION_ENGINE.md

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
