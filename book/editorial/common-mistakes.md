# Common Mistakes Specification

## Purpose

A Common Mistakes section at the end of each chapter makes the chapter's lessons memorable by showing what "wrong" looks like. Readers remember mistakes better than explanations.

## Format

```markdown
## Common Mistakes

### ❌ [Mistake Name]

[One paragraph explanation. What the reader might do wrong and what to do instead.]
```

The `❌` character is mandatory — it creates visual recognition across chapters.

## Rules

- V1: 3-5 mistakes per chapter
- V2: 6-10 mistakes per chapter
- Each mistake must be a specific, actionable pattern (not a general warning)
- Mistakes must be realistically common — things a reader would actually try

## Good Examples

```
### ❌ Sleeping instead of waiting

Using `time.sleep(5)` instead of waiting for a specific condition. This fails on slow connections (5 seconds not enough) and wastes time on fast ones. Always wait for a visible, enabled element.

### ❌ Selecting by nth-child

Selectors like `div:nth-child(3)` break when the page adds or removes elements. Use data attributes or stable text content instead.
```

## Bad Examples

```
### ❌ Writing bad code

Always write good code. (Too vague — not actionable)

### ❌ Not using best practices

Follow best practices. (Nothing specific to remember)
```

## Placement

Always after recipes, before Reflection Questions.

```text
Recipes
    ↓
Common Mistakes
    ↓
Reflection Questions
    ↓
Production Checklist
```
