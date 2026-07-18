# Reflection Questions Specification

## Purpose

Reflection questions force readers to think like engineers instead of just copying code. They are the difference between "I read this chapter" and "I learned from this chapter."

## Format

```markdown
## Reflection Questions

1. [Question 1 — V1: 1-2 sentences, V2: 2-3 sentences]

2. [Question 2]

3. [Question 3]

[V2 only — questions 4 through 5-7]
```

## Rules

- V1: Exactly 3 questions
- V2: 5-7 questions, each requiring deeper analysis
- Never ask about API syntax or function names
- Always ask about engineering decisions, trade-offs, or diagnosis

## Question Types

### Decision Questions

Ask the reader to choose between approaches and justify:

> "A selector works locally but fails in CI. Where do you investigate first?"

### Diagnosis Questions

Describe a symptom and ask what the root cause might be:

> "Your automation runs successfully every night. The exit code is 0. A week later, someone notices Friday's data is empty. What should you check first?"

### Trade-off Questions

Present two valid approaches and ask which is better for a given scenario:

> "Would you validate all records before storing any, or store each record immediately and reject invalid ones later?"

### Design Questions

Ask how the reader would structure a solution:

> "You have 5 suppliers, each with different websites and authentication. Do you write 5 separate scripts or one script with 5 configurations?"

## Prohibited Patterns

**Bad (API recall):** "What does the validate_product() function return?"

**Bad (trivia):** "How many validation layers does Chapter 13 define?"

**Bad (yes/no):** "Should you validate before storage?"

## Good Examples (V1)

1. Why is a browser profile different from a Python session?
2. When should you use a persistent profile versus a temporary one?
3. What happens if two workers share the same profile directory?

## Good Examples (V2)

1. If a selector works locally but fails in CI, where do you investigate first — the selector or the environment?
2. Your automation completes successfully but produces zero records. Which monitoring metric would catch this?
3. Would you retry a browser crash? Why or why not? At what point does retrying become harmful?
4. You have 5 suppliers, each with different authentication. Do you write one script with 5 configurations or 5 separate scripts?
5. What metric would tell you an automation is degrading even though it still completes?
6. Which failures should trigger automatic retry, and which should immediately alert a human?
