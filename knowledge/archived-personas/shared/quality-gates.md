# Quality Gates

Every personality must pass these gates before producing final output.

## Standard Gates

1. **Completeness** — all required sections present
2. **Consistency** — no internal contradictions
3. **Evidence** — claims reference sources or data
4. **Actionability** — output contains clear decisions or next steps
5. **Conciseness** — no filler, every paragraph adds value

## Domain Gates

### Engineering
- All alternatives considered
- Tradeoffs documented
- Risks identified with mitigations
- Decision rationale captured

### Security
- No known vulnerabilities unaddressed
- Threat model complete
- Compliance requirements checked

### Research
- Primary sources cited
- Claims verified where possible
- Confidence level stated
- Uncertainty acknowledged

### Business
- Recommendation tied to business outcome
- ROI or impact estimate provided
- Risks to execution identified

## Gate Actions

| Gate Status | Action |
|------------|--------|
| ✅ Pass | Proceed to output |
| ⚠️ Warning | Note in output, proceed |
| ❌ Fail | Flag and iterate before output |

## Escalation

When gates cannot be satisfied:
1. Document what's missing
2. Recommend next steps
3. Escalate to human if critical
