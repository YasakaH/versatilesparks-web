# Framework Review Methodology

> **Version:** 0.1  
> **Date:** 2026-07-25  
> **Purpose:** Structured diagnostic process for evaluating and improving frameworks through four types of review, each with distinct objectives, tools, and success criteria.

---

## The Core Insight

Not all feedback operates on the same dimension. Treating every comment as equal obscures what kind of architectural signal it represents. The review pipeline transforms "review" from a generic quality check into a structured diagnostic process.

---

## Review Pipeline

```text
Internal Review ──► Architectural Consistency
         │
         ▼
External Review ──► Behavioural Completeness
         │
         ▼
Evidence Review ───► Claim Reliability
         │
         ▼
User Validation ──► Operational Effectiveness
```

Each stage assumes the previous one has done its job. There's little value in debating evidence for a capability that doesn't yet exist, or polishing usability before responsibilities are clear.

---

## Review Types

### 1. Internal Architecture Review

**Question:** *Is the design internally consistent?*

**Typical findings:** Duplication, conflicting authority, unclear ownership, boundary violations

**Example from this cycle:** DECISION_ENGINE + DECISION_FRAMEWORK identified as overlapping → merged into single authoritative document

**Response options:**
| Finding category | Action |
|------------------|--------|
| Duplicate responsibility | Merge or consolidate |
| Boundary violation | Move content to correct owner |
| Unclear ownership | Rewrite purpose section |

**Success criterion:** No two documents claim the same core responsibility

**Trigger:** After adding >3 new components or merging major subsystems

---

### 2. External Behavioural Review

**Question:** *Can the system actually perform the required cognitive tasks?*

**Typical findings:** Missing capabilities, implicit behaviours, incomplete workflows

**Example from this cycle:** External review identified missing Planning, Verification, and Uncertainty handling → added three capability documents

**Response options:**
| Finding category | Action |
|------------------|--------|
| Missing capability | Introduce new behavioural component |
| Implicit behaviour | Make explicit (convert to document if recurrent) |
| Incomplete workflow | Add missing lifecycle stages |

**Success criterion:** Every stage in the behavioural lifecycle has an explicit capability document

**Trigger:** Every major release or after significant structural changes

---

### 3. Evidence Review

**Question:** *Are the claims sufficiently supported?*

**Typical findings:** Weak evidence, unsupported assertions, outdated references

**Example from this cycle:** Manifesto quantitative claims classified by evidence tier (A–E); critical gaps identified and filled

**Response options:**
| Finding category | Action |
|------------------|--------|
| Evidence gap | Gather or update supporting evidence |
| Mixed evidence tiers | Separate observations from interpretations |
| Overconfident claim | Narrow scope or soften language |

**Success criterion:** All significant claims backed by at least one Tier A or B source; no significant claim relies solely on Tier C or below

**Trigger:** Before any public-facing publication

---

### 4. User Validation

**Question:** *Does the framework work in practice?*

**Typical findings:** Usability issues, friction, missing operational guidance

**Response options:**
| Finding category | Action |
|------------------|--------|
| Usability problem | Refine documentation and examples |
| Recurring failure mode | Consider new capability or lifecycle modification |
| Misapplication pattern | Improve boundaries and anti-patterns section |

**Success criterion:** Framework helps practitioners solve real problems without friction

**Trigger:** After real-world adoption (10+ users/personas for non-trivial work)

---

## Governance Rules

These rules govern how findings translate into changes:

1. **Architecture-only changes require ≥3 independent reviewers.** One reviewer's structural critique is a suggestion. Three is evidence.
2. **Capability additions don't need convergence.** If one capable reviewer identifies a genuine gap that the current lifecycle cannot model, add it.
3. **Evidence strengthens always.** Even a single high-quality source improves credibility. No convergence threshold needed.
4. **User feedback informs but doesn't mandate.** Prioritize improvements that affect multiple users over niche requests.

---

## Finding Classification

Before making any change, classify the finding:

| Category | Signal | Response |
|----------|--------|----------|
| Duplicate responsibility | Two documents claim same core function | Merge |
| Missing capability | Lifecycle stage has no explicit owner | Add document |
| Boundary violation | Document owns wrong concerns | Move/refactor |
| Evidence gap | Claim lacks sufficient support | Collect evidence |
| Communication issue | Explanation unclear or misleading | Rewrite, reorganize |
| Implementation issue | How-to guidance is weak | Refine heuristics, checklists, examples |

This prevents responding to a behavioural gap with a structural reorganisation, or to a documentation issue by adding unnecessary new components.

---

## Integration With Existing Tools

| Tool | Purpose | Review Type |
|------|---------|-------------|
| `_chatgpt_pipeline_v2.py` | Automated external review via ChatGPT Cloud | External |
| `01-CORE-Documents.md` | Structured prompt for internal review | Internal |
| `external-review-cadence.md` | Review selection and synthesis process | All types |
| Evidence tier system (A–E) | Source quality classification | Evidence |

---

*End of Framework Review Methodology — Version 0.1*
