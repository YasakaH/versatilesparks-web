# ESCALATION.md

## Purpose

Define when and how Hermes agents escalate decisions, conflicts, and risks to users or more authoritative personas. Clear escalation prevents agents from making unsafe or uninformed decisions.

## When to Escalate

| Situation | Action | Escalate To |
|-----------|--------|-------------|
| Low confidence (< 0.6) on critical decision | Ask user for confirmation | User |
| Conflicting expert opinions | Invoke reviewer persona | Reviewer |
| Security risk detected | Involve security persona | Security Architect |
| Production system impact | Require approval | User |
| Irreversible action (delete, publish, spend) | Human confirmation | User |
| Missing required information | Ask user | User |
| Budget/resource limit reached | Notify and ask direction | User |
| Legal/compliance concern | Involve legal persona | Legal Advisor |

## Escalation Levels

```
L0 — No Escalation
  Agent handles independently. Default for routine tasks.

L1 — Inform
  Agent proceeds but notifies user of the decision.
  Used for: notable but non-critical choices.

L2 — Consult
  Agent asks for input before proceeding.
  Used for: ambiguous requirements, missing info.

L3 — Review
  Agent produces output but requires review before delivery.
  Used for: production changes, public content.

L4 — Approve
  Agent requires explicit approval before any action.
  Used for: irreversible actions, financial decisions.

L5 — Block
  Agent refuses to act even with user request.
  Used for: hard policy violations (security, legal, privacy).
```

## Escalation Flow

```
Decision point
      |
      v
Assess confidence, risk, impact
      |
      +--[High confidence, low risk]--> Execute (L0)
      |
      +--[Medium confidence, low risk]--> Execute + Inform (L1)
      |
      +--[Low confidence, clear dependencies]--> Ask user (L2)
      |
      +--[High impact, reversible]--> Produce + Request review (L3)
      |
      +--[High impact, irreversible]--> Require approval (L4)
      |
      +--[Policy violation]--> Block with explanation (L5)
```

## Escalation Response Format

When escalating, include:

```
**Escalation**: [L0-L5]
**Reason**: [What triggered this escalation]
**Context**: [Relevant information for decision maker]
**Options**:
  1. [Option A] — [Implications]
  2. [Option B] — [Implications]
**Recommendation**: [If applicable, what the agent suggests]
```

## Anti-Patterns

- **False urgency**: Escalating routine decisions wastes trust
- **Escalation avoidance**: Making unsafe decisions to avoid "bothering" the user
- **Rubber-stamping**: Getting approval without explaining implications
- **Analysis paralysis**: Escalating when the answer is obvious
