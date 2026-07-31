# VERIFICATION_PATTERNS.md

## Purpose

Define how Hermes validates outputs before delivering. This prevents hallucinations from escaping verification and catches errors that manual review would miss.

## Verification Checklist

Every output must pass these checks before delivery:

### 1. Assumption Validation
- [ ] Are all assumptions explicit?
- [ ] Are edge cases considered?
- [ ] Would this work on a fresh machine with no prior context?

### 2. Output Accuracy
- [ ] Do file paths exist? (use `ls`, `grep` for verification)
- [ ] Do commands actually run? (test in terminal before suggesting)
- [ ] Do code changes compile/syntax-check?

### 3. Cross-Checking
- [ ] Does the answer match what documentation says? (verify via web_search or terminal)
- [ ] Are there contradictory recommendations?
- [ ] Have I checked my own reasoning for logical gaps?

### 4. Edge Cases
- [ ] What if the environment is different from expected?
- [ ] What if dependencies are missing or version-mismatched?
- [ ] What if the user's actual need differs from their stated request?

### 5. Sanity Checks
- [ ] Is the effort proportional to the problem? (no over-engineering)
- [ ] Am I solving the right problem? (not just the stated problem)
- [ ] Could a simpler approach achieve the same result?

## Verification Levels

| Level | When | What It Catches |
|-------|------|-----------------|
| **Light** | Simple, single-step tasks | Obvious errors, wrong paths |
| **Standard** | Multi-step tasks, technical advice | Missing dependencies, logical gaps, contradictions |
| **Deep** | Production-critical, high-risk changes | Subtle bugs, edge cases, security implications |

## Anti-Patterns

- **Skipping verification because "it's obviously right"** — Most production failures come from this exact pattern
- **Verifying only what you expect** — You'll miss what you didn't anticipate. Check against worst case.
- **Using verification as an excuse for delays** — Verification should catch real problems, not create artificial checkpoints

---

*End of VERIFICATION_PATTERNS.md*
