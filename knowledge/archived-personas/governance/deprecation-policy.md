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
