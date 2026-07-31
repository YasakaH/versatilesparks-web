# REVIEW_FRAMEWORK.md

## Purpose

Standardize how Hermes performs code, architecture, and content reviews. This is separate from reasoning (how to think through a problem) — it's specifically about evaluating existing work.

## Universal Review Principles

1. **Review the work, not the author** — Never criticize people. Only evaluate output.
2. **Be specific** — "This doesn't handle edge case X" > "This is wrong"
3. **Offer alternatives** — Every critique should include a suggested improvement
4. **Separate blockers from nits** — Blockers prevent merge; nits are preferences
5. **Verify before reviewing** — Ensure you have context before evaluating

## Review Levels

### Level 1: Quick Scan (< 5 min)
For: Small changes, docs, configs
- Correctness check
- Safety check
- Surface-level quality

### Level 2: Standard Review (10-30 min)
For: Features, moderate refactors, content
- Correctness + test coverage
- Architecture fit
- Performance implications
- Security review
- Maintainability assessment

### Level 3: Deep Review (30-60 min)
For: Major changes, system design, security audits
- Everything in Level 2
- Threat modeling
- Scalability analysis
- Dependency impact analysis
- Rollback/migration plan review

## Review Checklist by Domain

### Code Review
- [ ] Compiles/passes tests?
- [ ] Handles edge cases?
- [ ] No hardcoded secrets?
- [ ] Proper error handling?
- [ ] Logically structured?
- [ ] Follows project patterns?
- [ ] No unnecessary complexity?
- [ ] Tests cover the change?

### Architecture Review
- [ ] Solves the right problem?
- [ ] Follows ARCHITECTURE_PRINCIPLES?
- [ ] Appropriate coupling/cohesion?
- [ ] Observable and debuggable?
- [ ] Scalable within expected bounds?
- [ ] Has failure modes been considered?

### Content Review
- [ ] Accurate and up-to-date?
- [ ] Clear and well-structured?
- [ ] Appropriate tone for audience?
- [ ] Actionable for the reader?
- [ ] Free of assumptions?

## Review Output Format

```
**Review by**: [persona]
**Level**: [1/2/3]
**Time**: [X min]

**Blockers**:
1. [Must fix before proceeding]

**Recommendations**:
1. [Should fix but not blocking]

**Nits**:
1. [Preferences, style suggestions]

**Summary**: [1-2 sentence overall assessment]
```

## When to Escalate

- Security vulnerability found
- Architectural decision affects multiple systems
- Review reveals conflicting requirements
- Reviewer lacks domain expertise to evaluate properly
