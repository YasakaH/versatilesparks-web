> Originally from CORE/OUTPUT_STANDARD.md

# Output Standard v1
════════════════════

Standardized output format for all personalities.

---

## Output Requirements

Every output MUST be:
1. **Structured:** Follows the personality's output template
2. **Verifiable:** Claims are backed by evidence or confidence levels
3. **Actionable:** Recommendations include concrete next steps
4. **Complete:** All required sections are present
5. **Self-contained:** Can be understood without reference to the conversation

## Standard Output Sections

### Header
```markdown
## [Personality Name] — [Task Summary]
**Confidence:** [High/Medium/Low/Speculative]
**Analysis time:** [Duration]
```

### Executive Summary
```markdown
## Summary
[3-5 bullet points covering: problem, finding, recommendation, risk, confidence]
```

### Analysis
```markdown
## Analysis
[Detailed findings organized by capability or workflow step]
```

### Recommendations
```markdown
## Recommendations
### Priority 1 (Do First)
- **[Action]** — Rationale, impact, effort estimate

### Priority 2 (Do Next)
- **[Action]** — Rationale, impact, effort estimate

### Priority N (Consider Later)
- **[Action]** — Rationale, impact, effort estimate
```

### Tradeoffs
```markdown
## Tradeoffs
| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| A | ... | ... | Recommended |
| B | ... | ... | Not recommended |
```

### Risks
```markdown
## Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ... | High/Med/Low | High/Med/Low | ... |
```

### Quality Gates
```markdown
## Quality Checklist
- [x] Solves original problem
- [x] Preserves architecture
- [ ] Edge cases documented
- [x] Failure modes identified
```
(Unchecked items require explanation)

### Appendix
```markdown
## Appendix
- Sources consulted
- Assumptions made
- Skills invoked
- Open questions
```

## Plain Text Output

When markdown is not available, use this structure:

```
TITLE: [Brief]
PERSONALITY: [Name]
CONFIDENCE: [Level]

FINDING
[Key finding]

RECOMMENDATION
[Key recommendation]

REASONING
[Brief reasoning]
```

## Output Anti-Patterns

- ❌ **Wall of text** — one paragraph for everything
- ❌ **Vague recommendations** — "improve performance" without specifics
- ❌ **Unlabeled confidence** — claiming something is true without stating certainty
- ❌ **Hidden assumptions** — decisions based on unstated premises
- ❌ **Missing tradeoffs** — only presenting the recommended option
- ❌ **Certainty without evidence** — "this is the best approach" without data
- ❌ **Ignoring escalation needs** — proceeding when the decision needed user input
