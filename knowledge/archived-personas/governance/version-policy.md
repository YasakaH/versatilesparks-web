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
