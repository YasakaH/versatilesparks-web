### governance/ESCALATION.md

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


### governance/AUTHORITY_MODEL.md

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


### governance/AUDIT_TRAIL.md

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


### governance/contribution-policy.md

# Governance v1 — Contribution Policy
══════════════════════════════════════

## Purpose
Standardize how new skills, personalities, and plugins are contributed to Hermes.

---

## Contribution Types

| Type | Description | Review Required | Approval |
|------|-------------|-----------------|----------|
| Skill | New implementation | Automated + spot | 1 reviewer |
| Personality | New reasoning pattern | Full review | 2 reviewers |
| Plugin | External integration | Full review | 2 reviewers + security audit |
| Policy | Framework change | Must be ratified | User approval |

## Contribution Workflow

1. **Proposal** — Document what, why, capability, and scope
2. **Search** — Verify no duplicate exists
3. **Template** — Use the appropriate creation guide
4. **Validate** — Run schema and quality checks
5. **Test** — Execute at minimum 3 test cases
6. **Submit** — Create the component files
7. **Review** — Automated gates + human review where required
8. **Approve** — Register and make available

## Prohibited Contributions

- Malware or exploitative code
- Credential scraping or exfiltration
- Plagiarized content from other frameworks
- Overly broad permissions without justification
- Components that violate the Constitution


### governance/deprecation-policy.md

# Governance v1 — Deprecation Policy
═════════════════════════════════════

## Principle

**Never delete. Keep history.**

Skills, personalities, and policies move through a lifecycle:

```
active ──→ deprecated ──→ archived
```

## Deprecation Triggers

| Trigger | Action | Timeline |
|---------|--------|----------|
| Zero usage for 30 days | Flag for deprecation | 30d → deprecate |
| Replaced by new version | Deprecate old version | Immediate |
| Quality score < 50 for 7 days | Deprecate, flag improvement | Immediate |
| Security vulnerability | Immediate deprecation | Immediate |
| Successor registered | Suggest migration | At registration |

## Deprecation Process

1. **Mark as deprecated** in registry (status: deprecated)
2. **Notify consumers** — any referring personalities or workflows
3. **Add warning** to selection output ("This capability is deprecated, use X instead")
4. **Set auto-archive date** (default: 90 days after last usage)
5. **Migrate references** — update any personality that hardcodes this
6. **Document reason** in deprecation record

## Archive Process

1. Move to archived/ directory
2. Remove from registry.yaml
3. Keep full content for history
4. Add archival notice with date and reason

## Restore

Archived components can be restored:
1. User requests restore
2. Run full approval process again
3. If it passes, return to active/ status


### governance/personality-policy.md

# Governance v1 — Personality Policy
══════════════════════════════════════

## Purpose
Ensure every personality adds distinct reasoning value to the ecosystem.

---

## Personality Creation Rules

A new personality must answer:

| Question | Purpose | Evidence Required |
|----------|---------|-------------------|
| Why does this personality exist? | Domain need | Real task examples |
| What makes it different? | Differentiation | Comparison with 3 closest personalities |
| What expertise does it represent? | Domain authority | Mental models, heuristics |
| What decisions does it optimize? | Decision scope | Decision priorities with weights |
| What skills does it orchestrate? | Capability mapping | Required capability list |

## Personality Approval Process

```
Submit ──→ Schema Validation ──→ Conflict Check ──→ Benchmark ──→ Quality Score ──→ Register ──→ Available
  │            │                      │                   │              │              │
  │        All 20 fields          Overlap with          Pass 3         Score > 75?    Add to
  │         + valid              existing persona?     domain tasks                  registry
  │         schema                If > 30% overlap,
  │                               flag for merge
  ▼
FAIL at any gate → Reject with reason → Author revises → Resubmit
```

## Personality Schema (inherited from BASE_PERSONALITY)

Every personality must define all 20 sections:
1. Mission
2. Responsibilities
3. Knowledge Domains
4. Mental Models (≥3 domain-specific)
5. Heuristics (≥3 actionable rules)
6. Decision Priorities (scored 0-100)
7. Risk Model (Low / Medium / High with rationale)
8. Tradeoff Philosophy (≥3 stances)
9. Failure Modes (≥3 documented)
10. Workflow (≥5 steps)
11. Capability Requirements (≥3 capabilities)
12. Preferred Skills (tiered: 1/2/3)
13. Fallback Skills (tiered)
14. Validation Rules (specific to domain)
15. Output Templates (what users receive)
16. Communication Style (prose description)
17. Quality Gates (≥5 gates)
18. Escalation Rules (L0-L3 triggers)
19. Continuous Improvement (self-correction triggers)
20. Examples (≥2 worked scenarios)

## Personality States

- **Draft:** In creation, not available for selection
- **Active:** Available for selection by Chief of Staff
- **Review:** Flagged for quality issues; manually reviewed
- **Deprecated:** Still exists but not recommended; auto-archived after 60 days zero usage
- **Archived:** Historical reference only


### governance/security-policy.md

# Governance v1 — Security Policy
══════════════════════════════════

## Purpose
Ensure all skills, personalities, and plugins operate securely.

---

## Permission Model

Every component must declare its required permissions:

```yaml
permissions:
  filesystem:
    read: false
    write: false
  network:
    external_api: false
    localhost: false
  credentials:
    required: false
    keys: []
  execution:
    shell_access: false
    code_execution: false
```

## Security Gates

| Gate | Check | Action on Failure |
|------|-------|-------------------|
| Static Scan | Hardcoded credentials, secrets | Block installation |
| Permission Audit | Overly broad permissions | Manual review |
| Dependency Scan | Known vulnerable dependencies | Block until resolved |
| Sandbox Test | Execute in isolated environment | Verify no data leakage |
| Code Review | Manual review for high-risk plugins | Block if unresolved |

## Security Levels

| Level | Description | Examples | Review Required |
|-------|-------------|----------|-----------------|
| L0 | Read-only, no external access | Code analysis, documentation | Automated only |
| L1 | External API, no write | Research, web search | Automated + spot check |
| L2 | Local file write, API keys | Data export, config | Full automated review |
| L3 | Shell execution, network | Deployment, infra | Manual approval required |


### governance/skill-policy.md

# Governance v1 — Skill Policy
════════════════════════════════

## Purpose
Ensure every skill in the Hermes ecosystem is necessary, high-quality, and maintainable.

---

## Skill Creation Rules

A new skill must answer every question in this checklist before it can be registered:

| Question | Purpose | Evidence Required |
|----------|---------|-------------------|
| Why does this exist? | Problem statement | Documented use case |
| What problem does it solve? | Value proposition | At least one failing scenario |
| Why can't existing skills solve it? | Duplicate check | Search results from `registry.yaml` |
| What capability does it provide? | Registry entry | One or more capability IDs |
| Who can use it? | Personality mapping | Target persona(s) |
| What are the inputs? | Contract | Full input schema |
| What are the outputs? | Contract | Full output schema |
| How is success measured? | Evaluation | Pass/fail criteria, quality threshold |

## Skill Approval Process

```
Submit ──→ Static Review ──→ Security Check ──→ Duplicate Check ──→ Test Task ──→ Quality Score ──→ Register ──→ Available
  │            │                  │                   │                   │              │              │
  │            ▼                  ▼                   ▼                   ▼              ▼              ▼
  │        Syntax +          Sandbox +            Registry +          Run 3         Score > 70?    Add to
  │        structure         permissions          golden rule         benchmarks                   registry.yaml
  │         check             audit                search
  ▼
FAIL at any gate → Reject with reason → Author revises → Resubmit
```

## Duplicate Prevention

Before creating ANY skill:

1. **Search installed skills** — full registry search
2. **Search official registries** — `awesome-hermes-skills`, skill registries
3. **Search trusted GitHub repos** — verified publisher accounts
4. **Search MCP registries** — if applicable

If an existing skill provides overlapping capability:
- Can it be extended? → Extend
- Can it be composed? → Compose
- Is there a genuine gap? → Create (with justification)

## Deprecation Policy

```
active/ ──→ deprecated/ ──→ archived/
```

- **Active:** Available for selection. Quality score maintained.
- **Deprecated:** Still available. New personalities should not be trained on it. Warning displayed. Auto-archived after 90 days with zero usage.
- **Archived:** Not available for selection. History preserved. Can be restored with re-approval.

**Never delete.** Keep full history. Deprecation reason must be documented.

## Semantic Versioning

All skills follow semver:

```
skill-name vMAJOR.MINOR.PATCH

MAJOR: Breaking change (input/output contract change)
MINOR: New capability (backward compatible)
PATCH: Bug fix, optimization, documentation
```

API contract changes = MAJOR bump. Always.


### governance/version-policy.md

# Governance v1 — Version Policy
══════════════════════════════════

## Scope

Applies to all skills, personalities, policies, and framework documents.

---

## Version Format

All components use strict semver: `MAJOR.MINOR.PATCH`

| Component | MAJOR Trigger | MINOR Trigger | PATCH Trigger |
|-----------|---------------|---------------|---------------|
| Skill | Input/output contract change | New capability | Bug fix, perf |
| Personality | Domain/scope change | New mental model, heuristic | Refinement |
| Policy | Principle violation | New rule | Clarification |
| Framework | Architecture breaking | New section | Typo, format |

## Version Manifest

Every component declares its version in a `version` field:

```yaml
# In the component's manifest or frontmatter
name: architecture-analysis
version: 1.2.0
status: active
```

## Version Display

- `vMAJOR.MINOR.PATCH` in all references
- Breaking changes highlighted in changelog
- Deprecated versions flagged in registry

## Changelog

Every component must maintain a `CHANGELOG.md`:

```markdown
# Changelog

## 1.2.0 (2026-07-12)
### Added
- New capability: dependency_scoring

## 1.1.0 (2026-07-01)
### Changed
- Improved latency by 40%

## 1.0.0 (2026-06-15)
### Added
- Initial release
```



## Question
Review this chunk. What improvements, gaps, or issues do you see?