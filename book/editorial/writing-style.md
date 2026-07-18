# Writing Style Guide

## Tone

The book's voice is a **senior engineer mentoring a capable junior colleague**.

- Professional but not corporate
- Direct but not harsh
- Confident but not arrogant
- Precise but not pedantic

## Sentence Rules

- Prefer 18-25 words per sentence
- Maximum 35 words
- One idea per sentence
- Break complex ideas across 2-3 sentences

**Good:** "The browser sends a CDP event. Your handler receives it. Heavy work in the handler blocks the next event."

**Bad:** "When the browser sends a CDP event, your handler receives it, and if you do heavy work inside the handler, it will block the next event from being processed until the handler completes."

## Paragraph Rules

- Maximum 5 lines
- One topic per paragraph
- Use a blank line between paragraphs (Markdown)
- Lead with the conclusion

**Good:**
> "Use filelock for scheduling locks. It is cross-platform, has zero external dependencies except the library itself, and is easy to understand. For distributed systems, graduate to Redis or PostgreSQL advisory locks."

**Bad:**
> "There are several approaches to implementing scheduling locks. The first approach is filelock, which works cross-platform and has minimal dependencies. Another approach uses Redis, which works across multiple machines..."

## Heading Levels

- `#` — Chapter title only (one per file)
- `##` — Component (Why This Exists, Mental Model, Production Story, each recipe title)
- `###` — Subsection within a component (Problem, Code, Failure Modes)
- `####` — Never use. Restructure instead.

## Lists

- Maximum 7 bullets per list
- Each bullet must start with a capital letter
- Each bullet must end with a period if it's a complete sentence
- Parallel structure within a list

**Good:**
- Browser version
- Python version
- Operating system

**Bad:**
- Browser version
- Checking Python version
- The operating system matters

## Analogy Rules

- Maximum one analogy per major section
- Never mix metaphors within the same section
- Analogies must match the reader's likely experience (restaurant, workshop, building — not rocket science or professional sports)
- State the analogy explicitly, then map it to the technical concept

**Good:** "Think of an iframe like a locked office in a building. You cannot shout from the lobby. You must enter the office first."

**Bad:** "The iframe is a butterfly in a garden of code."

## Code Blocks

- Every code block must be runnable or be a clearly labeled excerpt
- Include `import` statements in every code block (no hidden imports)
- Use type hints in all Python examples
- Limit code blocks to 25 lines unless explaining a complete module
- Never use `pass` as a placeholder — provide a comment explaining what goes there

## Callouts

Use`>` blockquotes for production rules:

```markdown
> **Production Rule:** Text here.
```

Use`---` with bold heading for engineering notes:

```markdown
### Engineering Note
> Text here.
```

Use`❌` for common mistakes:

```markdown
### ❌ Mistake Name
```

## Prohibited Words

| Avoid | Use Instead |
|-------|-------------|
| amazing, incredible, fantastic | (remove entirely) |
| basically, essentially, simply | (remove — if it's simple, it doesn't need saying) |
| just | (remove — "just install" → "install") |
| very, really, extremely | (use precise adjective instead) |
| solution (without stating the problem) | state the problem first |
| utilize | use |
| leverage | use |
| robust | specific quality (fault-tolerant, maintainable) |
| cutting-edge | (remove — implies future irrelevance) |
| state-of-the-art | (remove) |

## Pronouns

- Prefer "you" (the reader) and "we" (author + reader)
- Avoid "I" except in production stories
- Avoid "one" — too formal
- Use "they" as singular when gender is unknown or irrelevant

## Formatting

- Use backticks for: code, file paths, Stable IDs, module names, function names
- Use **bold** for: key terms on first use, production rules labels
- Use *italic* sparingly — only for emphasis that changes meaning

## Consistency

Once a term is used for a concept, never change it:

| Use | Don't Use |
|-----|-----------|
| browser profile | user data directory, Chrome profile |
| Stable ID | recipe ID, identifier, slug |
| production rule | rule, guideline, best practice |
| engineering note | note, tip, pro tip |
| failure mode | error case, edge case, failure scenario |
