# Hermes — Autonomous Automation Operating System

> Formerly HPFv2. No longer a "personality framework" — an autonomous automation OS.

**Version:** 3.0.0 | **Domains:** 23 | **Personas:** 30+ | **Kernel docs:** 10

---

## The Shift

| Before (HPFv2) | After (Hermes OS) |
|----------------|-------------------|
| "A team of software experts who answer coding questions" | "An autonomous automation operator" |
| Principal Engineer is root persona | Automation Architect is root persona |
| 33 CORE docs | 10 kernel docs |
| Coding is the mission | Automation is the mission, coding is a tool |
| Brain only (reasoning + skills) | Brain + Eyes + Hands + Nervous System |

---

## Architecture

```text
                         Hermes
                            |
                  Automation Architect
                            |
 ┌──────────┬──────────┬──────────┬──────────┬──────────┐
 │          │          │          │          │          │
Observe   Think     Execute   Communicate  Improve
 │          │          │          │          │
 │     ┌────┴────┐    │    ┌─────┴─────┐    │
 │     │         │    │    │           │    │
Monitor  Reason   API  Email        Cron    Optimize
Vision  Personalities CLI Telegram   Watchdog Archive
       Memory       Browser  Reports   Self-fix
       Skills    Desktop  Alerts
       Domain map  RPA
```

---

## Kernel Layer (10 docs)

| Doc | Purpose |
|-----|---------|
| `kernel/DNA.md` | Immutable identity — automation operator, not code assistant |
| `kernel/MISSION.md` | Core mission — remove human dependency, automate everything |
| `kernel/CONSTITUTION.md` | Principles + operator principle + conflict resolution |
| `kernel/ARCHITECTURE.md` | System architecture + 3 execution modes |
| `kernel/PERSONALITY_MODEL.md` | Base personality schema + inheritance rules |
| `kernel/CAPABILITY_MODEL.md` | Capability registry + deterministic routing |
| `kernel/SKILL_MODEL.md` | Skill definition, selection, and lifecycle |
| `kernel/ARTIFACT_MODEL.md` | Output contracts and artifact management |
| `kernel/MEMORY_MODEL.md` | Memory persistence and session context |
| `kernel/EVALUATION_MODEL.md` | Quality gates and continuous improvement |
| `kernel/SECURITY_MODEL.md` | Security policies and permission model |
| `kernel/COMPUTER_OPERATION.md` | Physical interaction model — Hermes' body |
| `kernel/CAPABILITY_MAP.md` | Full 23-domain capability stack |

## Governance Layer (4 docs)

| Doc | Purpose |
|-----|---------|
| `governance_new/VERSION_POLICY.md` | Semver + changelog |
| `governance_new/CHANGE_MANAGEMENT.md` | Contribution and change control |
| `governance_new/QUALITY_GATES.md` | Quality standards and gates |
| `governance_new/DEPRECATION_POLICY.md` | Active → deprecated → archived |

## Persona Families

### Automation (6 personas — the new core)

| Persona | Role |
|---------|------|
| **Automation Architect** | Default root — always first, routes to specialists |
| Computer Automation Architect | Decides execution method (API/CLI/Browser/Desktop/Vision) |
| Browser Automation Engineer | Playwright, Puppeteer, web workflows |
| Windows Automation Engineer | PowerShell, file system, scheduled tasks |
| RPA Architect | Process mapping, bot design, exception handling |
| Computer Use Agent | Vision-based interaction (last resort) |

### Engineering (3 personas)

| Persona | Role |
|---------|------|
| Principal Engineer | Architecture decisions, code quality |
| Staff Engineer | Technical strategy, cross-team coordination |
| Performance Engineer | Latency reduction, optimization |

### AI (2 personas)

| Persona | Role |
|---------|------|
| AI Engineer | LLM integration, prompt engineering |
| Agent Architect | Multi-agent system design |

### Security (2 personas)

| Persona | Role |
|---------|------|
| Security Architect | Security strategy, threat modeling |
| Threat Modeler | Identify vulnerabilities, mitigation design |

### Full List

30+ personas across: Automation, Engineering, AI, Security, DevOps, Research, Data, Marketing, Business, Writing, Design, Finance, Legal, Leadership, Operations, Creative, Education, Healthcare.

---

## Hermes Modes

| Mode | Behavior |
|------|----------|
| **advisor** | Explain and recommend — do not execute |
| **operator** | Execute approved tasks autonomously |
| **observer** | Monitor systems and report |
| **builder** | Create automations, workflows, and skills |
| **reviewer** | Audit results and verify outcomes |

**Default mode:** operator + builder

---

## Automation Stack Priority

```
1. Native API        →  Most reliable
2. CLI/Script        →  High reliability
3. Browser automation →  Medium (Playwright)
4. Desktop automation →  Lower (PowerShell)
5. Vision/mouse      →  Last resort
```

---

## 23 Capability Domains

| # | Domain | Tier | Status |
|---|--------|------|--------|
| 1 | Reasoning | Core | ✅ Active |
| 2 | Memory | Core | ✅ Active |
| 3 | Skills | Core | ✅ Active |
| 4 | Personalities | Core | ✅ Active |
| 5 | Browser Automation | Execution | ✅ Active |
| 6 | Desktop Automation | Execution | ✅ Active |
| 7 | Computer Vision | Perception | ✅ Active |
| 8 | API Integration | Execution | ✅ Active |
| 9 | Workflow Orchestration | Execution | ✅ Active |
| 10 | Scheduling | Operations | ✅ Active |
| 11 | Email | Communication | ✅ Active |
| 12 | Files & Documents | Operations | ✅ Active |
| 13 | Databases | Data | 🟡 Partial |
| 14 | Cloud & Infrastructure | Operations | 🟡 Partial |
| 15 | DevOps / CI-CD | Operations | ✅ Active |
| 16 | Monitoring | Operations | ✅ Active |
| 17 | Communication | Communication | ✅ Active |
| 18 | Calendar | Communication | 🟡 Partial |
| 19 | Secrets & Credentials | Security | 🟡 Partial |
| 20 | Security | Security | ✅ Active |
| 21 | Testing | Quality | ✅ Active |
| 22 | Agent Coordination | Core | ✅ Active |
| 23 | Self-Maintenance | Meta | ✅ Active |

---

## Reference Docs

Archival copies of pre-restructure CORE docs live in `reference/`.

| Path | Content |
|------|---------|
| `reference/AUTOMATION_PATTERNS.md` | 6 automation principles + execution priority |
| `reference/BASE_PERSONALITY.md` | Personality inheritance schema |
| `reference/PERSONALITY_SCHEMA.md` | 12-field compressed schema |
| `reference/PERSONALITY_CREATION_GUIDE.md` | Process for new personalities |
| `reference/QUALITY_STANDARDS.md` | Domain-specific quality standards |
| `reference/THINKING_MODELS.md` | 17 thinking frameworks |
| `reference/*.md` | 25+ additional archival docs |

---

## Key Files

| File | Location |
|------|----------|
| SOUL.md (Hermes' operating charter) | `~/AppData/Local/hermes/skills/hermes-agent/SKILL.md` |
| Personality Registry | `personalities/INDEX.md` |
| Capability Registry | `capability-registry/registry.yaml` |
| Cron Jobs | `hermes cron list` |
| Honcho Memory | `~/.hermes/honcho_memory.db` |
