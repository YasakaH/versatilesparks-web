# Chapter Template Specification

Every chapter (V1 and V2) follows this exact order. Sections marked optional may be omitted in V1 chapters only.

```text
# Chapter N — Title

## Subtitle (one-line summary of the chapter's engineering concept)

---

## Previously

Small box (1-3 lines) summarizing what the reader learned in the previous chapter.
Links to the previous chapter by name.

---

## Why This Exists

1-2 pages answering:
- What problem does this chapter solve?
- Why is this a hard problem?
- What happens if you skip this chapter?

Use a real business scenario to establish stakes.

---

## Mental Model

One-page conceptual diagram or explanation that frames the entire chapter.
This should be the single idea that, once understood, makes all the recipes obvious.

V1: 1 paragraph + 1 diagram
V2: 1 page + 1 architecture diagram + 1 lifecycle diagram

---

## Production Story

One realistic incident. See production-story.md for format.

V1: 200 words max
V2: 400 words max

---

## Learning Objectives

Bullet list of what the reader will know by chapter end.

V1: 3-5 items
V2: 5-7 items

---

## [Recipe 1–N]

Each recipe follows recipe-structure.md for its tier.

---

## Common Mistakes

See common-mistakes.md for format.

V1: 3-5 mistakes
V2: 6-10 mistakes

---

## Reflection Questions

See reflection-questions.md for format.

V1: 3 questions
V2: 5-7 questions

---

## Production Checklist

Concrete items the reader can verify before moving on.

V1: 5-8 items
V2: 8-12 items

---

## Chapter Connections

```text
Depends on: [Stable IDs of prerequisite recipes]
Uses: [common/*.py modules]
Leads to: [Chapters that depend on this one]
```

---

## Chapter Summary

One paragraph. Lead with the engineering principle, not a list of APIs.

End with a forward-looking sentence or question.

---

## Next Chapter

**Next: Chapter N — Title**

Brief preview (2-3 lines) of what the next chapter covers.
```

## Section Order Rules

1. The order above is **mandatory** — never reorder sections
2. Skip a section only if the spec explicitly allows it for the chapter's tier
3. Never add sections not defined in this template
4. Every `---` separator must have a blank line before and after
