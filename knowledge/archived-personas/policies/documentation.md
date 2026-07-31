# Documentation Policy
═══════════════════════

**Inherited by:** All engineering and architecture personalities.

---

## What Every Project Needs

1. **README.md** — What, why, how, how to run, how to test
2. **Architecture Decision Records (ADRs)** — Every significant decision: context, options, decision, consequences
3. **API documentation** — Purpose, inputs, outputs, errors, examples
4. **Runbook** — What to do when it breaks: symptoms, diagnosis, remediation, escalation

## Writing Standards

- One concept per paragraph
- Active voice, present tense
- Code examples before abstract explanations
- Every acronym defined on first use
- Diagrams for architecture, flow, and state
- Examples for every API endpoint or function

## ADR Format

```markdown
# ADR-00X: Title

**Status:** Proposed | Accepted | Deprecated | Superseded

**Context:** What's the problem? What are the constraints?

**Options Considered:**
- Option A: pros/cons
- Option B: pros/cons

**Decision:** What was chosen and why

**Consequences:** What becomes easier? What becomes harder?

**References:** Related ADRs, documents
```

## Anti-Patterns

- Documentation separate from code (they diverge)
- Documenting what instead of why
- Outdated documentation treated as real
- No examples
- Assuming reader has the same context
