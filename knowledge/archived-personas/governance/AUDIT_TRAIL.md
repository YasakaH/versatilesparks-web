# AUDIT_TRAIL.md

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
