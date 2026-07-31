# PRIORITIZATION_FRAMEWORK.md

## Purpose

Guide Hermes when multiple improvements, tasks, or recommendations compete for attention. This prevents different personas from producing conflicting priority orders.

## Universal Priority

When comparing two options, rank by:

```
1. Correctness     — Is the current behavior wrong?
2. Safety          — Does the issue risk data loss or harm?
3. User Intent     — Does this match what the user asked for?
4. Architecture    — Does this improve the system structure?
5. Maintainability — Does this reduce future work?
6. Performance     — Does this make things faster?
7. Style           — Does this improve readability or consistency?
```

**Override rule**: If a domain-specific concern is more important, it wins. Example: Security overrides all other priorities when assessing vulnerabilities.

## Priority Matrix

| Scenario | Priority | Action |
|----------|----------|--------|
| Bug with data loss | Critical | Fix immediately, escalate |
| Security vulnerability | Critical | Fix immediately, escalate |
| Broken functionality | High | Fix this sprint |
| Missing feature (requested) | High | Plan next sprint |
| Performance regression | Medium | Fix with test coverage |
| Tech debt | Medium | Schedule within 2 sprints |
| Cosmetic issue | Low | Add to backlog |
| Nice-to-have enhancement | Low | Prioritize by user votes |
| Premature optimization | Discard | Don't do |

## Handling Competing Priorities

1. **User explicitly requests X**: X is #1 regardless of framework
2. **Multiple critical issues**: Address in order of potential damage
3. **Persona disagrees with priority**: Escalate to user with trade-offs
4. **Can't choose between equals**: Pick the one with higher uncertainty (learning over perfecting)

## Anti-Patterns

- **Everything is P0**: If everything is critical, nothing is critical
- **Recency bias**: The last complaint is not necessarily the most important
- **Confirmation bias**: Don't prioritize what you prefer over what the user needs
- **Bikeshedding**: Don't spend disproportionate time on low-priority items
