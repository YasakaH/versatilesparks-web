# Chapter Introduction Specification

## Purpose

The chapter introduction sets expectations. It answers: "Why should I read this chapter?" without the reader needing to guess.

## Components (in order)

### Previously Box

Optional for Part I Chapter 1. Required for all others.

```markdown
---

## Previously

✓ [What chapter N-1 taught] (Chapter N-1 Name)
✓ [Another skill from chapter N-1]

Now we build on those skills to [purpose of this chapter].
---
```

1-3 lines maximum. Links to the previous chapter by name.

### Why This Exists

1-2 pages. Must answer:

- What problem does this chapter solve?
- Why is this a hard problem?
- What happens if you skip this chapter?

Start with a concrete business scenario:

**Good:** "A retailer checks competitor prices manually every morning. Three analysts. Four hours. Every day. This chapter teaches you to automate that."

**Bad:** "This chapter teaches web scraping."

### Mental Model

One paragraph + optionally a diagram. The single most important concept of the chapter.

**Good:** "Think of the browser like a restaurant kitchen. Your automation is the chef. CDP events are the orders coming in. If you do heavy cooking while taking orders, the orders pile up."

### Production Story

One realistic incident. See production-story.md for format and constraints.

### Learning Objectives

```markdown
## Chapter Goals

By the end of this chapter, you will know:
- [Skill 1]
- [Skill 2]
- [Skill 3]
- [V2: Skill 4]
- [V2: Skill 5]
```

V1: 3-5 items, each a practical skill
V2: 5-7 items, each an engineering capability

## Section Order (Mandatory)

```text
Previously
    ↓
Why This Exists
    ↓
Mental Model
    ↓
Production Story
    ↓
Learning Objectives
    ↓
[Recipes follow]
```
