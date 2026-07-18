# Engineering Note Specification

## Purpose

Engineering Notes are the voice of a senior engineer mentoring the reader. They should feel like someone looking over your shoulder saying "I learned this the hard way."

## Format

```markdown
### Engineering Note

> Text here. Maximum 100 words.
```

The `### Engineering Note` heading is bold in the rendered output. The blockquote body is visually distinct from surrounding text (grey callout).

## Rules

- Maximum 100 words each
- Maximum 1 per major section (3-5 per chapter)
- Place immediately after the code or concept they reference — never before

## When to Use

| Use When | Don't Use When |
|----------|---------------|
| The reader might make a subtle mistake | The information is obvious |
| There's a trade-off worth explaining | The information belongs in the main text |
| A pattern has a common misuse | The information is a reference (put in a table) |
| Experience would save the reader time | The information is an API description |

## Tone

Must feel like mentorship, never documentation.

**Good:** "Waiting longer doesn't make automation more reliable. Waiting for the correct condition does."

**Good:** "You can retry indefinitely. Production systems shouldn't. Cap your retries, then escalate."

**Bad:** "The time.sleep() function pauses execution for a specified number of seconds."

**Bad:** "Note: This pattern is commonly used in production environments."

## Examples

### Good
```
### Engineering Note

> You could make this retry 50 times. It would still fail on the 51st. Fix the cause, not the retry count.
```

### Bad (just documentation)
```
### Engineering Note

> The retry decorator can accept max_attempts and delay parameters.
```

### Bad (too vague)
```
### Engineering Note

> This pattern is recommended for production use.
```
