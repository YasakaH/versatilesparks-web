# Part Introduction Specification

## Purpose

Part Introductions separate the book into major sections. They are 1-2 page essays that frame the next group of chapters. They exist to give the reader a sense of progression — "I finished one major topic and am starting another."

## When to Use

- Parts I, II, III, IV (V1)
- Part V (V2, Chapter 14 as capstone section)

## Format

```markdown
# Part [Roman Numeral] — [Title]

## [One-line essay subtitle that captures the engineering theme]

---

[Essay body — 1-2 pages]
```

## Structure

### Opening Statement (2-3 sentences)

A declarative statement that challenges the reader's assumption.

**Good:**
> "The browser has completed its work. Your automation successfully navigated, extracted, and stored data. Most tutorials stop here. Professional engineering begins here."

**Bad:**
> "In this part, we will learn about data collection and validation."

### Why This Part Exists (1 paragraph)

What does this part solve that previous parts didn't?

### Architecture Diagram (Mermaid, 1 per part)

Show how this part's chapters connect. Each chapter is a node.

```mermaid
graph LR
    Ch1[Chapter 1: Launch] --> Ch2[Chapter 2: Navigate]
    Ch2 --> Ch3[Chapter 3: Reliability]
```

### What You Will Build (1 paragraph)

Describe the capability the reader will have after finishing this part.

**Good:** "After Part III, you will be able to build a complete data pipeline that validates, deduplicates, and stores scraped information — not just extract it."

### Transition (2-3 sentences)

Link this part to the previous one and preview the next.

## Rules

- Maximum 2 pages
- No code in part introductions (diagrams only)
- Must include an architecture diagram showing chapter connections
- Must not introduce concepts that belong in individual chapters
- Write each part intro as if the reader just finished the previous part's last chapter
