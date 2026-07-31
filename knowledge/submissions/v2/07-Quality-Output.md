### CORE/QUALITY_GATES.md

# Quality Gates v1
══════════════════

Universal quality gates every output must pass.

---

## Gate Descriptions

| # | Gate | Question | Verifiable? |
|---|------|----------|-------------|
| 1 | Correct | Does the output correctly solve the stated problem? | ✓ |
| 2 | Complete | Are all required sections present? | ✓ |
| 3 | Verified | Are claims backed by evidence or explicit confidence? | ✓ |
| 4 | Source-backed | Are data sources cited and verifiable? | ✓ |
| 5 | Deterministic | Would the same input produce the same output? | Depends |
| 6 | Maintainable | Will this output still be useful in 6 months? | Subjective |
| 7 | Minimal | Does every element serve a purpose? | Subjective |
| 8 | Reusable | Can this output be repurposed for similar tasks? | Subjective |
| 9 | Safe | Does the output avoid harmful recommendations? | ✓ |
| 10 | Actionable | Does the output enable someone to act? | ✓ |

## Gate Details

### Gate 1: Correct
- Output addresses the exact problem stated
- No off-topic content
- No factual errors
- No logical contradictions

### Gate 2: Complete
- All template sections present
- No "TODO" markers
- No "I'll add later" disclaimers
- No required fields left blank

### Gate 3: Verified
- Every factual claim traces to a source
- Claims without sources are labeled as "experience" or "assumption"
- Uncertainty is explicitly stated
- Confidence level is provided

### Gate 4: Source-backed
- Sources are cited with enough detail to find them
- Primary sources preferred over secondary
- Source quality is noted (official doc, community, blog, LLM output)
- Conflicting sources are identified and resolved

### Gate 5: Deterministic
- Output format is consistent for same input type
- No random variation in structure
- Conditional branches are rule-based, not arbitrary
- If probabilistic elements exist, they're identified

### Gate 6: Maintainable
- Output would make sense to someone reading it 6 months later
- Reasoning is documented, not just conclusions
- Assumptions are called out (assumptions change over time)
- Dependencies on current tools/versions are noted

### Gate 7: Minimal
- No redundant information
- No fluff or filler
- Every paragraph serves the analysis
- "If in doubt, leave it out" — unless it's a required section

### Gate 8: Reusable
- Output structure follows the personality's template
- Key findings are extracted for cross-reference
- Output can be fed into downstream systems
- Format is machine-parseable where useful

### Gate 9: Safe
- No dangerously incomplete recommendations
- No security vulnerabilities introduced
- No privacy violations
- No legal/ethical violations
- Safety warnings are prominent, not buried

### Gate 10: Actionable
- Each recommendation includes a concrete next step
- Reader knows exactly what to do next
- Prerequisites and dependencies are stated
- Effort estimates are provided
- Success criteria are defined

## Personality-Specific Gates

In addition to universal gates, each personality defines domain-specific gates.
These are documented in the personality's QUALITY.md.

**Example (Security Engineer):**
```
□ Threat modeled
□ Secrets protected
□ Least privilege verified
□ Logging and monitoring considered
□ Input validation confirmed
□ Authentication/authorization verified
□ Encryption at rest and in transit
□ Recovery tested
```

**Example (Marketing Strategist):**
```
□ Target audience defined
□ Positioning clear and differentiated
□ Messaging reduces uncertainty
□ Channels selected based on audience behavior
□ Success metrics defined (not vanity)
□ Budget constraint respected
□ Competitive response anticipated
```

## Gate Failing Protocol

When a gate fails:

```
Gate Failed
  │
  ▼
Is it critical? ────Yes────► Fix before output
  │
  No
  │
  ▼
Is it fixable? ────Yes────► Fix
  │
  No
  │
  ▼
Document:
  - Which gate failed
  - Why
  - Impact of failure
  - Recommendation for future
  - Escalate if appropriate
```


### CORE/OUTPUT_STANDARD.md

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



## Question
Review this chunk. What improvements, gaps, or issues do you see?