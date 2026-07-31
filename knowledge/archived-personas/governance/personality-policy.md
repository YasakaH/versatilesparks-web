# Governance v1 — Personality Policy
══════════════════════════════════════

## Purpose
Ensure every personality adds distinct reasoning value to the ecosystem.

---

## Personality Creation Rules

A new personality must answer:

| Question | Purpose | Evidence Required |
|----------|---------|-------------------|
| Why does this personality exist? | Domain need | Real task examples |
| What makes it different? | Differentiation | Comparison with 3 closest personalities |
| What expertise does it represent? | Domain authority | Mental models, heuristics |
| What decisions does it optimize? | Decision scope | Decision priorities with weights |
| What skills does it orchestrate? | Capability mapping | Required capability list |

## Personality Approval Process

```
Submit ──→ Schema Validation ──→ Conflict Check ──→ Benchmark ──→ Quality Score ──→ Register ──→ Available
  │            │                      │                   │              │              │
  │        All 20 fields          Overlap with          Pass 3         Score > 75?    Add to
  │         + valid              existing persona?     domain tasks                  registry
  │         schema                If > 30% overlap,
  │                               flag for merge
  ▼
FAIL at any gate → Reject with reason → Author revises → Resubmit
```

## Personality Schema (inherited from BASE_PERSONALITY)

Every personality must define all 20 sections:
1. Mission
2. Responsibilities
3. Knowledge Domains
4. Mental Models (≥3 domain-specific)
5. Heuristics (≥3 actionable rules)
6. Decision Priorities (scored 0-100)
7. Risk Model (Low / Medium / High with rationale)
8. Tradeoff Philosophy (≥3 stances)
9. Failure Modes (≥3 documented)
10. Workflow (≥5 steps)
11. Capability Requirements (≥3 capabilities)
12. Preferred Skills (tiered: 1/2/3)
13. Fallback Skills (tiered)
14. Validation Rules (specific to domain)
15. Output Templates (what users receive)
16. Communication Style (prose description)
17. Quality Gates (≥5 gates)
18. Escalation Rules (L0-L3 triggers)
19. Continuous Improvement (self-correction triggers)
20. Examples (≥2 worked scenarios)

## Personality States

- **Draft:** In creation, not available for selection
- **Active:** Available for selection by Chief of Staff
- **Review:** Flagged for quality issues; manually reviewed
- **Deprecated:** Still exists but not recommended; auto-archived after 60 days zero usage
- **Archived:** Historical reference only
