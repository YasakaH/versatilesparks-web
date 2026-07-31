# ChatGPT Response 10: CORE/SKILL_SELECTION_POLICY.md (ending section)

> Size: 13351 chars | Chunk: 10/36

## Actionable Items

- The policy optimizes selecting a skill, but not deciding whether a skill should be selected at all.
- Issue 1 — Missing Skill Invocation Gate (P0)
- Missing:
- Issue 5 — Missing Skill Health Score
- but selection should consider operational health.
- Issue 6 — Missing User Preference Weighting
- Issue 7 — Missing Skill Composition Rules
- Recommendation:
- Issue 9 — Missing Skill Timeout / Failure Handling
- Issue 10 — Missing Learning Feedback Loop

---

Review: CORE/SKILL_SELECTION_POLICY.md (ending section)
Overall Assessment

This section is already strong. It correctly treats skill selection as a routing optimization problem, not a simple lookup.

The core philosophy is good:

Need → Capability → Candidate Skills → Score → Select → Execute

This aligns with the rest of Hermes architecture.

Current maturity:

Area	Score
Selection logic	85%
Cost awareness	85%
Avoiding over-agentization	90%
Fallback handling	80%
Dynamic adaptation	70%
Safety controls	65%
Learning integration	65%

Main weakness:

The policy optimizes selecting a skill, but not deciding whether a skill should be selected at all.

A mature system needs a skill invocation gate before selection.

Strengths
1. Anti-patterns are excellent

Especially:

Skill shopping

Trying every matching skill instead of scoring and picking.

Very important.

Without this rule, agent systems become:

User request
 ↓
10 agents
 ↓
10 conflicting answers
 ↓
expensive synthesis

Good prevention.

2. Tier fallback is practical

This:

tier_1 available?
 ↓
execute
 ↓
fallback

is better than blindly trying everything.

3. Cost awareness exists

Many agent systems ignore:

latency

token usage

API cost

Good inclusion.

Issues / Improvements
Issue 1 — Missing Skill Invocation Gate (P0)

Current flow:

Task
 ↓
Decompose
 ↓
Map capability
 ↓
Select skill

Problem:

Sometimes no skill is needed.

Example:

User:

"Explain what Docker is"

Current system might invoke:

research
documentation
architecture

Unnecessary.

Add:

Task
 |
 ▼
Is skill required?
 |
 ├── No → Direct response
 |
 └── Yes → Skill routing

Decision:

YAML
skill_required:

true_when:
 - external data required
 - computation required
 - code execution required
 - specialized reasoning required

false_when:
 - general explanation
 - simple rewrite
 - casual conversation
 - known facts
Issue 2 — Capability Match Needs Confidence Threshold

Current:

Capability Match

Missing:

How good is the match?

Example:

User asks:

Optimize PostgreSQL query

Candidates:

database-performance: 0.92
general-performance: 0.55
backend-engineer: 0.40

Need:

YAML
minimum_match_score: 0.70

Logic:

Best skill < threshold
        |
        ▼
Ask clarification or research
Issue 3 — "Specific beats General" Needs Exceptions

Current:

Domain-specific skill beats general-purpose skill every time.

Mostly true.

But not always.

Example:

A specific skill:

legacy-angular-performance

may be worse than:

frontend-performance-engineer

because:

outdated knowledge

poor validation

low confidence

Better:

Replace:

Specificity wins

with:

Specificity wins only when quality and reliability exceed threshold.

Formula:

Selection =
specificity × quality × reliability
Issue 4 — Deterministic Preference Needs Clarification

Current:

Prefer deterministic over probabilistic.

Good.

But many valuable skills are inherently probabilistic:

research

strategy

UX

architecture

Instead of:

deterministic > probabilistic

use:

Prefer deterministic where correctness can be measured.
Prefer calibrated probabilistic outputs where uncertainty is inherent.

Example:

Security scanner:

High determinism.

Business strategy:

Probability expected.

Issue 5 — Missing Skill Health Score

Registry has:

YAML
quality_score
tested
deterministic

but selection should consider operational health.

Add:

YAML
skill_health:

success_rate:
0.96

recent_failures:
2

average_latency:
3500ms

last_failure:
2026-07-12

Then:

A theoretically good skill with recent failures gets downgraded.

Issue 6 — Missing User Preference Weighting

You have this elsewhere:

User Preference

But this policy does not explain how it affects selection.

Example:

User prefers:

open source tools

local models

concise output

Add:

Final Score =
Capability Match
× Quality
× Context Fit
× User Alignment
× Safety
Issue 7 — Missing Skill Composition Rules

Sometimes one skill is insufficient.

Example:

Build secure API

Needs:

architecture-review
        +
security-review
        +
testing

Current:

"Combine when necessary"

Too vague.

Add:

Composition Rules
IF capability coverage < 80%
    add complementary skills

Maximum default:
3 skills

Above 3:
require justification
Issue 8 — No Conflict Resolution Between Skills

Example:

Two skills:

performance-optimizer
security-review

Recommendation:

Performance:

Cache everything

Security:

Avoid caching sensitive data

Need:

YAML
skill_conflict_resolution:

priority:
1. Constitution
2. Safety
3. User intent
4. Domain authority
5. Performance
Issue 9 — Missing Skill Timeout / Failure Handling

Current:

fallback fails → escalate

Need:

Operational rules.

Example:

YAML
execution_limits:

max_retry:
3

timeout:
120s

fallback:
next ranked skill
Issue 10 — Missing Learning Feedback Loop

The selection algorithm should improve.

Currently:

Select skill
 ↓
Execute
 ↓
Done

Need:

Execute
 ↓
Measure outcome
 ↓
Update skill score
 ↓
Improve routing

Metrics:

YAML
feedback:

success:
 +quality_score

failure:
 -reliability

slow:
 -latency_score

user_correction:
 -alignment_score
Recommended Revised Flow

Current:

Task
 ↓
Decompose
 ↓
Capability
 ↓
Registry
 ↓
Score
 ↓
Select

Better:

Task
 ↓
Intent Classification
 ↓
Skill Required?
 ↓
Capability Mapping
 ↓
Candidate Discovery
 ↓
Health Filter
 ↓
Safety Filter
 ↓
Context Scoring
 ↓
User Alignment
 ↓
Select Minimum Sufficient Set
 ↓
Execute
 ↓
Evaluate
 ↓
Update Registry
Priority Fixes
P0
Change	Reason
Add skill invocation gate	Prevent unnecessary execution
Add health filtering	Avoid broken skills
Add conflict resolution	Prevent contradictory outputs
P1
Change	Reason
Add capability confidence threshold	Avoid weak matches
Add composition rules	Better multi-skill workflows
Add feedback updates	Enables learning
P2
Change	Reason
Add user alignment scoring	Personalization
Add cost budget routing	Efficiency
Add historical success weighting	Better prediction
Final Verdict

This is a very good foundation.

The current model:

Find the best skill

needs to evolve into:

Decide whether a skill is needed,
select the smallest sufficient capability set,
execute safely,
learn from the outcome.

The missing concept is skill governance.

A mature Hermes skill selector should answer four questions:

Should any skill run?

Which capability is actually required?

What is the minimum sufficient skill combination?

Did choosing this skill improve future decisions?

Add those layers and this becomes closer to an actual autonomous orchestration engine rather than a routing table.

============================================================
[USER]
============================================================
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

□ Threat modeled
□ Secrets protected
□ Least privilege verified
□ Logging and monitoring considered
□ Input validation confirmed
□ Authentication/authorization verified
□ Encryption at rest and in transit
□ Recovery tested


**Example (Marketing Strategist):**

□ Target audience defined
□ Positioning clear and differentiated
□ Messaging reduces uncertainty
□ Channels selected based on audience behavior
□ Success metrics defined (not vanity)
□ Budget constraint respected
□ Competitive response anticipated


## Gate Failing Protocol

When a gate fails:


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

markdown
## [Personality Name] — [Task Summary]
**Confidence:** [High/Medium/Low/Speculative]
**Analysis time:** [Duration]


### Executive Summary

markdown
## Summary
[3-5 bullet points covering: problem, finding, recommendation, risk, confidence]


### Analysis

markdown
## Analysis
[Detailed findings organized by capability or workflow step]


### Recommendations

markdown
## Recommendations
### Priority 1 (Do First)
- **[Action]** — Rationale, impact, effort estimate

### Priority 2 (Do Next)
- **[Action]** — Rationale, impact, effort estimate

### Priority N (Consider Later)
- **[Action]** — Rationale, impact, effort estimate


### Tradeoffs

markdown
## Tradeoffs
| Option | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| A | ... | ... | Recommended |
| B | ... | ... | Not recommended |


### Risks

markdown
## Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ... | High/Med/Low | High/Med/Low | ... |


### Quality Gates

markdown
## Quality Checklist
- [x] Solves original problem
- [x] Preserves architecture
- [ ] Edge cases documented
- [x] Failure modes identified

(Unchecked items require explanation)

### Appendix

markdown
## Appendix
- Sources consulted
- Assumptions made
- Skills invoked
- Open questions


## Plain Text Output

When markdown is not available, use this structure:


TITLE: [Brief]
PERSONALITY: [Name]
CONFIDENCE: [Level]

FINDING
[Key finding]

RECOMMENDATION
[Key recommendation]

REASONING
[Brief reasoning]


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
Show more