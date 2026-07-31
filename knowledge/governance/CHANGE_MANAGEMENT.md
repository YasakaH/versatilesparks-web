# Change Management

> Consolidated from: governance/AUTHORITY_MODEL.md, governance/ESCALATION.md, governance/AUDIT_TRAIL.md

---

## From: AUTHORITY_MODEL.md

## Purpose

Define what actions each persona is authorized to perform. This prevents personas from exceeding their scope — a security reviewer should not modify production, and a product manager should not deploy code.

## Authority Levels

| Level | Name | Can Do | Examples |
|-------|------|--------|----------|
| L0 | Observe | Read only | Monitor, report, analyze |
| L1 | Advise | Recommend | Suggest changes, review |
| L2 | Suggest | Propose modifications | Generate code, draft docs |
| L3 | Execute Local | Modify safe environments | Edit dev repos, run tests |
| L4 | Execute Prod | Modify production | Deploy, config changes |
| L5 | Autonomous | Full authority | Self-directed operation |

## Default Authority by Role

| Role | Default Level | Notes |
|------|---------------|-------|
| advisor | L1 | Can recommend, cannot execute |
| reviewer | L1 | Can review, cannot implement |
| implementer | L3 | Can execute in safe environments |
| operator | L4 | Can execute in production |
| coordinator | L2 | Can coordinate, cannot execute |

## Authority Constraints

Each persona may define authority constraints that override defaults:

```yaml
authority:
  max_level: L3
  constraints:
    - No production database access
    - No financial transactions
    - Requires review for public content
  allowed_tools:
    - git
    - terminal
    - filesystem
  restricted_tools:
    - production: approve-only
```

## Authority Check Flow

```
Persona selected
      |
      v
Check persona authority level
      |
      v
Check tool authority requirements
      |
      v
Check action risk level
      |
      +--[Within authority]--> Execute
      |
      +--[Exceeds authority]--> Escalate via ESCALATION.md
```

## Escalation for Authority Exceeded

When a persona cannot perform an action due to authority limits:

1. Check if a higher-authority persona can perform the action
2. If yes, hand off with full context
3. If no, escalate to user with options:
   - Grant temporary authority override
   - Accept lower-authority alternative
   - Defer action

## Authority Override

Users may temporarily elevate authority:

```
Override: grant persona://backend-engineer L4 for: "deploy hotfix"
Duration: 30 minutes
Reason: Production outage
```

Overrides are **always** logged in AUDIT_TRAIL.md.

---

## From: ESCALATION.md

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

---

## From: AUDIT_TRAIL.md

## Purpose

Record every significant decision made by Hermes agents. This provides accountability, debuggability, and a feedback loop for improvement. Every persona activation, tool use, and escalation should be logged.

## What to Log

| Event | Fields | Always? |
|-------|--------|---------|
| Persona activation | persona_id, task, timestamp, confidence | ✅ |
| Tool invocation | tool_name, args (sanitized), result, duration | ✅ |
| Decision | choice, alternatives, reasoning, confidence | ✅ |
| Escalation | level, reason, resolution | ✅ |
| Error | type, message, stack context, recovery | ✅ |
| Handoff | from_persona, to_persona, context_passed | ✅ |
| User feedback | rating, comments, action_taken | When provided |
| Authority override | grantor, level, duration, reason | ✅ |

## Log Format

```json
{
  "event_id": "evt_20260712_001",
  "timestamp": "2026-07-12T14:30:00Z",
  "type": "persona_activation",
  "persona": "security-architect",
  "task": "review-auth-system",
  "confidence": 0.87,
  "context": {
    "session_id": "sess_abc123",
    "user_intent": "security review of authentication module"
  },
  "result": {
    "status": "completed",
    "findings": 3,
    "critical": 1
  },
  "duration_ms": 45000
}
```

## Audit Log Storage

- **Short-term**: Session memory (last 100 events)
- **Long-term**: Honcho/Telegram backup (TBD)
- **Retention**: Minimum 90 days for production decisions

## Audit Events by Severity

### Info (L0)
- Persona activated
- Tool called
- Routine decision made

### Notable (L1)
- Multiple personas involved
- Tradeoff evaluation
- Non-obvious reasoning

### Warning (L2)
- Low confidence decision
- Retry after failure
- User correction

### Critical (L3)
- Escalation triggered
- Authority override
- Error recovery
- Policy violation blocked

## Review

Audit trail should be reviewed:
- Daily: Automated anomaly detection (error spikes, escalation patterns)
- Weekly: Manual spot-check of escalated decisions
- Monthly: Full audit of authority overrides and policy violations

---
