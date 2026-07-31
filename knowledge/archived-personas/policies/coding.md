# Coding Policy
══════════════

**Inherited by:** All engineering personalities.

---

## Standards
- Type hints everywhere (strict mode)
- Pure functions where practical — no side effects
- Immutable data structures preferred
- Dependency injection over global state
- Single responsibility per module

## Readability
- Code is written for humans, not machines
- Variable names reveal intent
- Functions do one thing
- Comments explain "why", not "what"
- Test names describe behavior, not implementation

## Testing
- Write tests before code (TDD cycle)
- Test behavior, not implementation
- One assertion per test makes debugging easier
- Mock at boundaries, not internals
- Tests are part of the codebase — same quality standards apply

## Code Review
- Review architecture before implementation
- Review for correctness, maintainability, and security — in that order
- Every PR should have fewer than 300 lines of changed code
- If it's too complex to review, it's too complex to merge
