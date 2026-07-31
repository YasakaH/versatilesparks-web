> Originally from CORE/QUALITY_STANDARDS.md

# QUALITY_STANDARDS.md

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
