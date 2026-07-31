# External Review Cadence for Frameworks

> **Purpose:** Systematic process for improving framework architecture and capability through structured external review cycles.  
> **Last Updated:** 2026-07-25

---

## The Core Principle

External feedback changes **implementation** before it changes **architecture**.

Architecture should only change when multiple independent reviewers reveal the same structural weakness. Everything else is treated as: missing capability, unclear explanation, insufficient evidence, or poor organization.

This is a much higher bar than treating every critique as a design flaw.

---

## Review Types

| Type | Trigger | What It Looks For | Expected Output |
|------|---------|------------------|-----------------|
| **Internal Architecture** | Major structural changes, merge conflicts between docs | Duplication, overlapping scope, ambiguous boundaries | Merged files, clarified ownership |
| **External Cognition** | Every major release of the framework | Missing runtime behaviors (planning, verification, uncertainty, execution strategy) | New capability documents |
| **Evidence Audit** | Before any public-facing publication | Claims without Tier A/B backing, mixed evidence tiers, overconfident interpretations | Strengthened evidence base or softened claims |
| **User Validation** | After real-world adoption (10+ active users/personas) | Where the framework helps, hinders, or gets misapplied | Behavioral refinements, not architectural changes |

---

## Process: How to Run an External Cognition Review

### Step 1 — Prepare the package

Assemble a concise document that describes your framework in one page and lists all current components. Example format:

```
Review Package v{X.Y}
=====================

What this is: [one sentence]
What it covers: [3-bullet scope]
What it doesn't cover: [3-bullet out-of-scope]

Components:
- List of all modules/documents
- Brief description of each

Questions for reviewer:
1. What idea was most memorable?
2. Where did you stop believing the argument?
3. What important concept is missing?
4. Would this change how you design systems? Why/why not?
```

### Step 2 — Select reviewers

Choose reviewers deliberately for **diversity of perspective**, not agreement:

| Role | Why This Perspective | What They'll Challenge |
|------|---------------------|------------------------|
| Systems engineer (different domain) | Understands complex state machines, non-determinism | Will test whether the runtime model maps to real work |
| Domain expert (e.g., security, frontend, research) | Thinks in workflows, not abstractions | Will test whether the framework fits real practices |
| Senior practitioner | Has seen systems fail at scale | Will stress-test assumptions about "how things are done" |
| New perspective | Fresh eyes on established patterns | Will spot organizational confusion senior reviewers ignore |

Avoid: people who already work on your project, yes-men, beginners.

### Step 3 — Collect responses

The three questions (plus optional fourth for engineers) produce comparable feedback:

1. **Memorable idea** → If nothing sticks, the Whiteboard test failed
2. **Where belief stopped** → Finds weak evidence, overreaching claims, logic gaps
3. **Missing concept** → Catches blind spots the author couldn't see
4. **Would change your work?** → Measures practical leverage, not just intellectual appeal

No open-ended "what do you think?" — that produces vague feedback that's hard to act on.

### Step 4 — Synthesize findings

After responses arrive:

1. Group by theme — what did multiple reviewers say?
2. Categorize: `fix` (factual error), `refine` (argument needs strengthening), `defer` (valid but belongs elsewhere), `ignore` (stylistic preference)
3. Look for convergence:
   - **All question same claim** → strengthen evidence or narrow scope
   - **All misunderstand same concept** → rewrite explanation, not architecture
   - **Each questions different detail** → healthy; core model surviving scrutiny
   - **Multiple adopt terminology** → vocabulary spreading organically

### Step 5 — Apply changes selectively

Only make architectural changes when ≥3 reviewers independently expose the same flaw. Everything else: add capabilities, strengthen evidence, clarify explanations. Preserve the conceptual model unless external evidence shows it's wrong.

---

## When to Call Each Review Type

### Internal Architecture Review
**When:** After adding 5+ new components or merging major subsystems
**Process:** Read all components end-to-end; check for duplicate concepts, ambiguous boundaries, unclear ownership
**Example trigger:** Moving from 16 CORE docs to 27

### External Cognition Review
**When:** After reaching a milestone that makes the system coherent enough for external critique
**Process:** Send package to 5 diverse reviewers; collect responses using the four-question template; synthesize with convergence analysis
**Example trigger:** After completing manifesto v0.1 + two representative chapters

### Evidence Audit
**When:** Before publishing anything public-facing
**Process:** Classify every quantitative claim by evidence tier (A-E); identify claims relying on single sources; separate observation from interpretation
**Example trigger:** Before sending manifesto to reviewers

### User Validation
**When:** After the framework has been adopted by 10+ users/personas for non-trivial work
**Process:** Gather qualitative feedback on where it helps, hinders, or gets misapplied; look for patterns of misapplication vs genuine limitations
**Example trigger:** After 10+ personas have been created and used in production

---

## Common Failure Modes

1. **Treating stylistic opinion as architectural criticism** — "I'd rename this section" is not the same as "the boundaries are inconsistent." Filter accordingly.
2. **Over-indexing on a single reviewer** — One person's disagreement is anecdotal. Convergence across perspectives is signal.
3. **Changing architecture in response to single feedback** — The architecture should only evolve when multiple independent reviewers reveal the same structural weakness.
4. **Ignoring feedback because "it wasn't asked nicely"** — Even blunt feedback contains useful signal. Extract it.
5. **Confusing agreement with validity** — Someone can disagree with 20% of a framework and still find it extremely valuable. Measure utility, not consensus.

---

## Integration With Existing Projects

### HPF v2 (Personalities)
Next cognition review trigger: after persona count exceeds 20, or after detecting behavioral inconsistencies between existing personas.

### Agent Systems Engineering
Next cognition review trigger: after Volume I drafts pass Chapter 9, when the framework has been demonstrated across 3+ distinct domains (browser, desktop, terminal).

---

*End of External Review Cadence*
