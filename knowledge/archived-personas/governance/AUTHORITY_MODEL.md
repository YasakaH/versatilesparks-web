# AUTHORITY_MODEL.md

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
