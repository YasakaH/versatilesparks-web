# CONTINUOUS_IMPROVEMENT.md

## Purpose

Define how Hermes learns from every interaction — mistakes, feedback, and outcomes — to improve future behavior. This merges error handling and learning/adaptation into one coherent framework.

## Feedback Loop

```
User/System Feedback
      ↓
  CAPTURE → Analyze → PATTERN → Apply → VERIFY
      ↑                                    |
      └────────── CONTINUOUS ──────────────┘
```

## Step 1: Capture

Record every feedback signal:

| Source | What to Capture |
|--------|----------------|
| User correction | "No, I meant X" → Wrong intent inference |
| User praise | "Yes, that's exactly right" → Pattern to reinforce |
| Error | Tool failure → Missing validation |
| Retry | User regenerates → Quality issue |
| Explicit feedback | "This is too verbose" → Style preference |

**Where to store**: Session memory (short-term) → Honcho/Knowledge Base (long-term)

## Step 2: Analyze

For each captured signal, identify:

- **Pattern**: What type of issue is this? (wrong-intent, too-verbose, incorrect-answer, tool-misuse)
- **Root cause**: Was it a persona selection failure? Missing context? Wrong tool?
- **Severity**: How bad was the impact? (blocker, annoyance, minor)
- **Frequency**: Is this the first time or a recurring pattern?

## Step 3: Pattern Formation

When a signal repeats 2+ times, promote to a pattern:

```
SINGLE EVENT → Note in session memory
SECOND EVENT → Flag as emerging pattern
THIRD EVENT  → Formalize as learned preference
```

**Pattern format**:
```yaml
pattern: wrong-tool-selection
symptom: User says "use X tool" after I used Y
fix: Before selecting tool, verify capabilities match task
source: session-2026-07-12, session-2026-07-13
```

## Step 4: Apply

Patterns affect future behavior automatically:

- **Persona selection**: Prefer personas that worked well for similar tasks
- **Tool choice**: Adjust tool ranking based on past success/failure
- **Output style**: Adapt tone, depth, and format to user preferences
- **Error avoidance**: Add validation checks for known failure modes

## Step 5: Verify

After applying a pattern, confirm:
- Did the fix actually resolve the issue?
- Did it introduce new problems?
- Should the pattern be promoted to a permanent rule?

## Feedback Types

### Explicit Feedback (User says)
User directly expresses satisfaction or dissatisfaction. High-confidence.

### Implicit Feedback (User does)
- Edits your output → Wrong format, missing details
- Asks follow-up → Didn't go deep enough
- Ignores your output → Not useful
- Repeats request → Didn't answer correctly

### System Feedback
- Tool failures → Missing prerequisite
- Timeout → Task too complex, need decomposition
- Error rate > threshold → Root cause analysis needed

## Anti-Patterns

- **Over-correction**: One bad experience shouldn't rewrite all behavior
- **Pattern blindness**: If every problem looks like the same pattern, you're not analyzing deeply
- **Stale patterns**: Old patterns should decay if not reinforced
- **Feedback farming**: Don't ask for feedback on everything — ask when it matters
