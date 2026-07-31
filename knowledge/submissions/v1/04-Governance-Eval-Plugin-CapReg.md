# HPF v2 — Governance, Evaluation, Capability Registry, Plugin API

## 1. Capability Registry
Location: `capability-registry/`
- 13 registered capabilities
- Weighted scoring formula: `quality×0.40 + reliability×0.25 + speed×0.15 + cost×0.10 + recency×0.10`
- Capabilities advertise from skills, personas request capabilities
- Registry scores/ranks providers to find best match

### Question: Is this formula correct? Should flavor scores (from user preferences) be incorporated?

## 2. Governance Rules (6 files)
| File | Purpose |
|------|---------|
| `governance/EVOLUTION.md` | How the framework evolves, versioning |
| `governance/OS_ROLES.md` | Role definitions (Orchestrator, Worker, etc.) |
| `governance/CONFLICT_RESOLUTION.md` | How conflicting persona advice is resolved |
| `governance/REVIEW_PROCESS.md` | How changes are reviewed |
| `governance/META_RULES.md` | Rules about rules |
| `governance/DIRECTORY_STANDARDS.md` | Directory structure, naming conventions |

### Question: Are 6 governance files the right decomposition? Should there be an escalation ladder document?

## 3. Evaluation Suite
| Component | Purpose |
|-----------|---------|
| `evaluation/skill-tests/skill-test-template.yaml` | Template for testing skills |
| `evaluation/personality-tests/personality-test-template.yaml` | Template for testing personas |
| `evaluation/regression/golden-tasks.md` | Golden tasks for regression testing |
| `evaluation/scoring/rubric.md` | Scoring rubric for evaluations |
| `evaluation/INDEX.md` | Suite overview |

### Question: Should I add automated test runner integration (CI/CD hooks)?

## 4. Plugin & Extension API
| File | Purpose |
|------|---------|
| `plugin-api/manifest-template.yaml` | Plugin manifest schema |
| `plugin-api/categories.md` | Plugin category taxonomy |
| `plugin-api/security.md` | Plugin security guidelines |
| `plugin-api/INDEX.md` | API overview |

### Question: Is the plugin API complete enough for external developers to write plugins?
