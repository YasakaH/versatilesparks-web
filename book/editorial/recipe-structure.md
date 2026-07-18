# Recipe Structure Specification

Each recipe tier defines mandatory and optional sections. No recipe may include sections from a higher tier unless it is classified at that tier.

---

## Tier 1 — Full Production Depth (15 recipes)

Mandatory sections in order:

```text
## Recipe N — Title

**Tier: Full Production Depth**
**Stable ID:** UPPER-SNAKE-CASE
**Depends On:** Stable IDs of prerequisite recipes
**File:** `recipes/chNN/filename.py`

### Problem

One paragraph describing the concrete problem this recipe solves.
Include a specific business scenario, never a generic example.

### Why This Recipe Exists

One paragraph explaining the engineering concept behind the solution.
What would go wrong if you didn't have this pattern?

### Mental Model

A conceptual framing that makes the solution feel obvious.
1 paragraph + optionally a small diagram.

### Code

Runnable code block (max 25 lines for excerpts, unlimited for complete modules).
Must include all imports.

### Walkthrough

Step-by-step explanation of the code.
Each paragraph maps to one code section.

### Failure Modes

Minimum 3 failures in table format:

| Failure | Cause | Solution |
|---------|-------|----------|

### Decision Table

Table that helps the reader choose between approaches:

| Situation | Choice |
|-----------|--------|

### Production Rule

Single sentence blockquote starting with "> **Production Rule:**"

### Engineering Note (optional)

Grey callout, max 100 words. One per recipe.
```

---

## Tier 2 — Medium Depth (10 recipes)

```text
## Recipe N — Title

**Tier: Medium Depth**
**Stable ID:** UPPER-SNAKE-CASE
**File:** `recipes/chNN/filename.py`

### Problem

One paragraph. Business scenario required.

### Concept

The core idea, explained without full code.

### Code

Runnable code block.

### Walkthrough

Brief explanation.

### Edge Cases

2-3 edge cases in bullet or table format.

### Production Rule

Single sentence blockquote.
```

---

## Tier 3 — Utility Depth (5 recipes)

```text
## Recipe N — Title

**Tier: Utility Depth**
**Stable ID:** UPPER-SNAKE-CASE
**File:** `recipes/chNN/filename.py`

### Problem

One paragraph.

### Code

Runnable code block.

### Production Rule

Single sentence blockquote.
```

---

## Recipe Rules (All Tiers)

- Every recipe must have a **Stable ID**
- Every recipe file must reference the Stable ID in its docstring or comments
- Every Stable ID must appear in book/appendix/recipe-index.md
- File paths in the chapter must match the actual file location
- Code must include all imports — no hidden dependencies
- Business examples must be specific (competitor product URLs, realistic domains)
- Never teach deprecated APIs

## Capstone Recipes (Ch 14, Tier 1 variant)

Capstone recipes follow the standard Tier 1 structure but replace the "Code" section with an "Implementation" section that describes system-by-system architecture rather than line-by-line code. See Chapter 14 for examples.

Capstone recipe sections:

```text
Business Problem
Requirements
Constraints
Architecture (diagram)
Technology Decisions (table)
Implementation
Failure Scenarios (table)
Scaling Path
Lessons Learned (editorial only)
```
