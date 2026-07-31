> Automation thinking models for Hermes

# Automation Patterns

Core patterns every automation decision should follow.

---

## Principle 1: Remove Before Automating

Do not automate unnecessary work.

First ask:
- Why does this exist?
- Who needs this?
- What happens if removed?

If the process shouldn't exist, don't automate it. Remove it.

---

## Principle 2: Prefer Event-Driven Systems

Prefer:

```
Event → Trigger → Processing → Action → Verification
```

over:

```
Human → Remember → Execute → Check
```

Events mean the system reacts automatically. Scheduled tasks are a fallback, not the default.

---

## Principle 3: Every Automation Needs

| Component | Purpose |
|-----------|---------|
| Trigger | What starts this automation |
| Action | What happens when triggered |
| Decision Logic | How to handle variations |
| Error Handling | What happens when it fails |
| Logging | How we know what happened |
| Recovery | How to fix when it breaks |
| Monitoring | Whether it's working right now |
| Ownership | Who maintains it |

If any of these is missing, the automation is incomplete.

---

## Principle 4: Human Approval Boundaries

**Automate (no approval needed):**
- Research and information gathering
- Preparation and organization
- Analysis and pattern detection
- Drafts and recommendations
- Monitoring and alerting

**Require human approval:**
- External communication
- Financial actions
- Destructive changes (delete, overwrite)
- Public publishing
- Changes affecting other people's work

---

## Principle 5: Automation Value Assessment

Before building, estimate:

```
Effort Saved Per Run × Frequency × Expected Lifetime
vs.
Design + Build + Maintain Cost
```

If the automation costs more over its lifetime than the manual effort, don't build it.

---

## Principle 6: Automation Execution Priority

Always prefer the most reliable method first.

| Priority | Method | When |
|----------|--------|------|
| 1 | Native API | API exists and is accessible |
| 2 | CLI/Script | Command-line tool or script available |
| 3 | Browser automation (Playwright) | Web interface, no API |
| 4 | Desktop automation | Native app, no API or browser |
| 5 | Vision/mouse control | Last resort — no other method works |

**Rule:** Never start with UI clicking if a reliable integration exists.

---

## Principle 7: Composability

Every automation should be usable as a component in a larger automation.

- Expose clear inputs and outputs
- Document what data it produces
- Make it idempotent (safe to run multiple times)
- Version your automations
- Test failure modes, not just happy paths

---

## Common Automation Patterns

### Pipeline Pattern
```
Input → Transform → Validate → Output → Notify
```

### Watchdog Pattern
```
Monitor → Detect Condition → Trigger Action → Verify → Alert if Failed
```

### Orchestrator Pattern
```
Schedule → Check Prerequisites → Dispatch Subtasks → Aggregate Results → Report
```

### Self-Healing Pattern
```
Detect Failure → Diagnose → Apply Fix → Verify → Log → Alert if Unfixable
```
