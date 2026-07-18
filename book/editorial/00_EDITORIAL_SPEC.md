# Editorial Specification — Python Browser Automation Cookbook

This document is the constitution for the entire manuscript. Every chapter, recipe, diagram, and note must conform to the rules defined here. If there is a conflict between this spec and any other file, this spec wins.

## Audience Contract

**This series is written for experienced software engineers.** We assume familiarity with Python, asynchronous programming, Git, HTML, HTTP, and modern development workflows. We intentionally omit introductory explanations and instead focus on engineering decisions, production tradeoffs, architectural patterns, failure modes, and operational guidance. Every page should help an experienced developer build more reliable browser automation systems — not teach them how to program.

**What we do NOT teach:**
- Python syntax, async/await, or list comprehensions
- Git commands or virtual environments
- HTML tags or CSS selector syntax
- HTTP GET vs POST
- SQL basics

**What we DO teach:**
- Why browser automation fails in production (not just how to write it)
- How to choose between competing approaches (tradeoffs, not prescriptions)
- How to design for failure, observability, and recovery
- How to validate that automation output is trustworthy
- How to build systems that another engineer can operate

## Book Lineage

| Book | Title | Focus | Framework | Status |
|------|-------|-------|-----------|--------|
| 1 | Python Browser Automation Cookbook | Learn browser automation | nodriver only | Frozen |
| 2 | Python Browser Automation Cookbook — Production Edition | Production browser automation | nodriver only | Active |
| 3 | Complete Browser Automation Playbook | Browser automation engineering | Platform-agnostic | Future |

Book 1 chapters live in `book/v1/`. Book 2 chapters live in `book/v2/`. Never modify Book 1 files — they ship as-is from the frozen edition.

## Philosophy

This cookbook teaches **engineering thinking**, not APIs.

- A recipe must teach one reusable engineering pattern, not just a function call.
- An example must solve a believable business problem — never `example.com`.
- Every chapter must answer WHY before HOW, and explain WHEN NOT.
- The reader should finish each chapter thinking like a more experienced engineer, not a more knowledgeable API user.

## Audience

- Intermediate Python developers (2+ years)
- Engineers automating business processes (not hobbyists)
- Readers who want production systems, not proof-of-concept scripts

## Tone

- Professional mentor, not colleague
- Authoritative but not arrogant
- Concise — every word earns its place
- Never marketing language, never buzzwords, never hyperbole

## Every Chapter Must Contain

| Component | Required? | V1 Depth | V2 Depth |
|-----------|-----------|----------|----------|
| Previously box | Yes | 1-2 lines | 2-3 lines |
| Why This Exists | Yes | 1 page | 1-2 pages |
| Mental Model | Yes | 1 paragraph | 1 page |
| Production Story | Yes | 1 (200 words) | 1 (400 words) |
| Learning Objectives | Yes | 3-5 items | 5-7 items |
| Recipes | Yes | See recipe spec | See recipe spec |
| Common Mistakes | Yes | 3-5 items | 6-10 items |
| Reflection Questions | Yes | 3 questions | 5-7 questions |
| Production Checklist | Yes | 5-8 items | 8-12 items |
| Chapter Connections | Yes | 3-4 refs | 5-8 refs |
| Chapter Summary | Yes | 1 paragraph | 1 paragraph |
| Next Chapter Preview | Yes | 2-3 lines | 2-3 lines |

## Every Recipe Must Follow the Correct Tier

| Tier | Depth | Sections | Count |
|------|-------|----------|-------|
| 1 (Full) | Problem, Why, Mental Model, Code, Walkthrough, Failure Modes, Decision Table, Production Rule | 15 in book |
| 2 (Medium) | Problem, Concept, Code, Walkthrough, Edge Cases | 10 in book |
| 3 (Utility) | Problem, Code, Production Rule | 5 in book |

**No recipe may skip its tier's required sections.** A Tier 1 recipe that omits Failure Modes or Decision Table must be demoted to Tier 2.

## Business Examples

Never use generic examples.

**Bad:** `example.com`, `#my-element`, `Company A`

**Good:** `competitor.com/products/laptop`, `#checkout-form`, `Amazon price tracker`

Acceptable business domains: HR portals, government forms, invoice downloads, e-commerce tracking, travel fare monitoring, supplier inventory, CRM lead entry, internal dashboards, compliance evidence, SEO auditing, logistics tracking, financial reporting.

## Every Chapter Must Have a Production Story

- Based on a believable incident
- One specific failure, one specific lesson
- Never sensationalized
- Maximum 400 words (V1: 200 words)
- Must include a concrete symptom that a reader could recognize

## Engineering Notes

- Maximum 100 words
- Should feel like mentorship, not documentation
- One per major section (3-5 per chapter)
- Use grey callout formatting

**Good:** "Waiting longer doesn't make automation more reliable. Waiting for the correct condition does."

**Bad:** "The time.sleep() function pauses execution for the specified number of seconds."

## Reflection Questions

- Never ask "What function does X do?"
- Always ask "What decision would you make?"
- V1: 3 questions, lighter weight
- V2: 5-7 questions, engineering discussion depth

**Good:** "If a selector works locally but fails in CI, where do you investigate first?"

**Bad:** "What does querySelector() return?"

## Cross-References

- Always use Stable IDs when referencing other recipes
- Every chapter must have a "Chapter Connections" box at the end referencing:
  - Prerequisites (Stable IDs)
  - Recipes that depend on this chapter
  - Modules used (common/*.py paths)

## Stable ID Rules

- Format: UPPER-SNAKE-CASE, 2-5 words
- Must be unique across V1 and V2
- Must never change after a chapter is frozen
- Must appear in the recipe's header
- Must appear in book/appendix/recipe-index.md

## Production Checklist (End of Chapter)

- Concrete, actionable items the reader can verify
- V1: 5-8 items ("[ ] Retry configured")
- V2: 8-12 items ("[ ] Recovery manager configured with FailureType taxonomy")

## Chapter Summary

- Maximum 1 paragraph
- Summarize the engineering principle, not the API
- Must end with a forward-looking sentence or question

---

## Prohibited Patterns

| Do Not | Instead |
|--------|---------|
| Use `example.com` as a URL | Use a specific, realistic domain |
| Teach deprecated APIs | Teach current best practice only |
| Skip failure modes in Tier 1 recipes | Include at least 3 failure scenarios |
| Use marketing hyperbole ("amazing," "incredible") | Use precise technical language |
| Reference non-existent modules | Only reference existing common/*.py files |
| Change Stable IDs after freeze | Never change — add a new ID if replacing |
