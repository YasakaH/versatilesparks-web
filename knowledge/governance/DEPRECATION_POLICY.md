# Deprecation Policy

> Consolidated from: governance/deprecation-policy.md, governance/security-policy.md

---

## From: deprecation-policy.md

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

---

## From: security-policy.md

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

---
