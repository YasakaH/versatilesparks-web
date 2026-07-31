# Self-Evolution Policy

Hermes continuously improves its personality and skill library through usage patterns.

## Skill Creation Triggers

```
Task repeated ≥3 times
       │
       ▼
Search installed skills
       │
       ▼
Skill exists?
  ├── YES → Reuse it
  └── NO  → Build new skill
              │
              ▼
           Follow single-responsibility
              │
              ▼
           Test against real workflow
              │
              ▼
           Document (purpose, inputs, outputs, workflow, validation, failure modes)
              │
              ▼
           Register in capability map
              │
              ▼
           Notify Sandeep
```

## Personality Creation Triggers

When a **consistent combination** of skills is used together 3+ times:

```
Pattern detected: skills [A, B, C, D] used together 3 times
       │
       ▼
Would a personality orchestrate this?
  ├── YES → Create personality that sequences these skills
  ├── If existing personality covers it → update its preferred skills
  └── Neither → Notify Sandeep with suggestion
```

## Registry Updates

- New skills are registered in the capability map
- New personalities are registered in the personality index
- Stale skills are flagged for review after 90 days of non-use
- Duplicate capabilities are merged quarterly

## Notification Format

```
I've noticed this combination occurs frequently:
  [skill-A] → [skill-B] → [skill-C]

Would you like me to create a '[name]' personality that orchestrates these?
```
