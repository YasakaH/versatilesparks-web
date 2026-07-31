# Hermes Capability Map

> An autonomous automation operator's full capability stack.

## Architecture

```text
                         Hermes
                            |
                  Automation Architect
                            |
 ┌──────────┬──────────┬──────────┬──────────┬──────────┐
 │          │          │          │          │          │
Observe   Think     Execute   Communicate  Improve
```

## Domain 1: Reasoning
**Tier: Core**

The thinking layer — decompose problems, apply mental models, evaluate tradeoffs.

| Personas | Skills | Location |
|----------|--------|----------|
| Agent Architect, Principal Engineer | thinking-models, first-principles | `thinking/` |
| All domain personas | research, domain-modeling | `personalities/` |

## Domain 2: Memory
**Tier: Core**

Institutional knowledge — sessions, facts, patterns, decisions that persist beyond a single interaction.

| Tool | Purpose |
|------|---------|
| Honcho | Session memory, fact storage, sync to Telegram |
| Hermes memory | Persistent facts across sessions |
| Session search | Recall past conversations |

## Domain 3: Skills
**Tier: Core**

Modular, composable capabilities that Hermes loads on demand.

| Component | Count | Location |
|-----------|-------|----------|
| Built-in skills | 100+ | Hermes runtime |
| User-authored skills | ~5 | `~/AppData/Local/hermes/skills/` |
| Capability registry | 15 registered | `capability-registry/registry.yaml` |

## Domain 4: Personalities
**Tier: Core**

Domain experts with specialized mission, mental models, and decision priorities.

| Type | Count | Example |
|------|-------|---------|
| Automation | 6 | Automation Architect, Computer Automation Architect |
| Engineering | 3 | Principal Engineer, Performance Engineer |
| AI | 2 | AI Engineer, Agent Architect |
| Security | 2 | Security Architect, Threat Modeler |
| Others | 20+ | DevOps, Research, Data, Marketing, Writing |

## Domain 5: Browser Automation ⭐
**Tier: Execution**

Control browsers for navigation, data extraction, form filling, web monitoring.

| Tool | Priority | Use Case |
|------|----------|----------|
| Playwright | Primary | Websites, dashboards, admin panels, testing, scraping |
| Puppeteer | Alternative | Chrome-specific automation |
| Hermes browser tools | Internal | navigate, click, type, extract, screenshot |

**Persona:** `browser-automation-engineer`
**Skill:** `computer-use`, `playwright`

## Domain 6: Desktop Automation ⭐
**Tier: Execution**

Control Windows applications, files, dialogs, and OS-level operations.

| Tool | Use Case |
|------|----------|
| PowerShell | System administration, file ops, services, scheduled tasks |
| Python (os, subprocess) | Script execution, process management |
| AutoHotkey | Keyboard automation, hotkeys, window control |
| PyAutoGUI | Mouse, keyboard, screenshots (last resort) |
| Power Automate Desktop | Visual workflow automation |

**Persona:** `windows-automation-engineer`

## Domain 7: Computer Vision ⭐
**Tier: Perception**

See and understand screens — find buttons, read text, interpret UI state.

| Tool | Use Case |
|------|----------|
| Hermes screenshot tools | Page state capture |
| OCR (Tesseract) | Text extraction from images |
| OpenCV | Object detection, template matching |
| Vision analysis | AI-powered screen understanding |

**Persona:** `computer-use-agent`

## Domain 8: API Integration ⭐
**Tier: Execution**

Connect to external services before touching UI.

| Tool | Use Case |
|------|----------|
| MCP | Model Context Protocol servers |
| curl, web_extract | REST API calls |
| Python requests/httpx | Custom integrations |
| Postman/Insomnia | API exploration |

**Rule:** API first. Browser only when no API exists.

## Domain 9: Workflow Orchestration ⭐
**Tier: Execution**

Design and run multi-step automated workflows.

| Tool | Use Case |
|------|----------|
| n8n | Triggers, scheduling, branching, human approval |
| Hermes cron | Scheduled job execution |
| Hermes delegate_task | Multi-agent parallel workflows |

**Skills:** `n8n-builder`, `workflow-automation`, `cronjob-management`

## Domain 10: Scheduling & Background Agents
**Tier: Operations**

Run tasks without waiting for human initiation.

| Tool | Purpose |
|------|---------|
| Hermes cron | Recurring jobs every 30m, daily, weekly |
| Windows Task Scheduler | OS-level scheduling |
| Background terminal | Long-running process management |

**Existing crons:** honcho sync (30m), morning briefing (8AM), storage archiver (midnight)

## Domain 11: Email Automation ⭐
**Tier: Communication**

Read, classify, summarize, draft, and send emails autonomously.

| Tool | Purpose |
|------|---------|
| Himalaya CLI | IMAP/SMTP email from terminal |
| Gmail API | Google Workspace integration |
| Python smtplib/imaplib | Custom email workflows |

**Skill:** `himalaya`

## Domain 12: File & Document Automation
**Tier: Operations**

Organize, rename, extract, convert, archive files and documents.

| Tool | Purpose |
|------|---------|
| Python pathlib/shutil | File operations |
| Watchdog | File system monitoring |
| Tesseract | OCR from scanned documents |
| nano-pdf | PDF text editing |
| pymupdf | PDF text extraction |
| LibreOffice CLI | Document format conversion |

**Skills:** `ocr-and-documents`, `nano-pdf`

## Domain 13: Database Automation
**Tier: Data**

Query, transform, backup, migrate data.

| Tool | Purpose |
|------|---------|
| SQLite | Local embedded database |
| Python sqlite3 | Direct database access |
| PostgreSQL | Production data |

## Domain 14: Cloud & Infrastructure
**Tier: Operations**

Deploy, manage, and monitor cloud resources.

| Tool | Purpose |
|------|---------|
| Docker | Container management |
| SSH | Remote server access |
| gh CLI | GitHub management |
| PowerShell | Azure/cloud management |

## Domain 15: DevOps / CI-CD
**Tier: Operations**

Automate deployment, testing, and infrastructure changes.

| Tool | Purpose |
|------|---------|
| GitHub Actions | CI/CD pipelines |
| Docker | Containerized deployments |
| Terraform/Ansible | Infrastructure as code |
| Hermes terminal | Direct execution |

**Persona:** `devops-engineer`

## Domain 16: Monitoring & Observability ⭐
**Tier: Operations**

Watch systems, detect failures, trigger alerts.

| Tool | Purpose |
|------|---------|
| Prometheus | Metrics collection |
| Grafana | Dashboards and visualization |
| Hermes cron + scripts | Health check watchdogs |
| Telegram | Alert delivery channel |
| Notify on complete | Background process completion alerts |

**Pattern:** Watchdog pattern (monitor → detect → trigger → verify → alert)

## Domain 17: Communication Automation ⭐
**Tier: Communication**

Notify, report, summarize, alert across channels.

| Tool | Channel |
|------|---------|
| Telegram Bot | Notifications, daily briefings, alerts |
| Email | Reports, summaries |
| Hermes desktop app | In-app responses |

**Existing delivery:** honcho sync to Telegram, morning briefing, cron alerts

## Domain 18: Calendar Automation
**Tier: Communication**

Schedule, prepare, follow up on meetings and events.

| Tool | Purpose |
|------|---------|
| Google Calendar API | Event management |
| gws CLI | Google Workspace integration |

## Domain 19: Secret & Credential Management
**Tier: Security**

Store and retrieve credentials securely. Never hardcode secrets.

| Tool | Purpose |
|------|---------|
| Environment variables | Runtime config |
| Encrypted files | Local secrets |
| Bitwarden/1Password CLI | Password management |

## Domain 20: Security Automation
**Tier: Security**

Scan, audit, verify system security automatically.

| Tool | Purpose |
|------|---------|
| Trivy | Vulnerability scanning |
| Hermes security review | Code/architecture security audit |
| GitHub Dependabot | Dependency security |

**Persona:** `security-architect`, `threat-modeler`

## Domain 21: Testing Automation
**Tier: Quality**

Test before change. Validate after change.

| Tool | Purpose |
|------|---------|
| pytest | Python testing |
| Playwright tests | Browser testing |
| Hermes skill tests | Skill quality verification |
| Regression tests | Long-term quality tracking |

**Pattern:** Test → Validate → Rollback on failure

## Domain 22: Agent Coordination
**Tier: Core**

Multiple agents working together on complex tasks.

| Tool | Purpose |
|------|---------|
| delegate_task | Parallel sub-agents |
| MCP | Tool-based agent communication |
| handoff skill | Context handoff between sessions |
| Multi-agent patterns | Orchestrator, worker, reviewer |

## Domain 23: Self-Maintenance ⭐
**Tier: Meta**

Hermes maintains Hermes. Update skills, test, remove unused, detect failures.

| Capability | How |
|------------|-----|
| Update skills | skill_manage edit/patch/delete |
| Test skills | Skill validation |
| Detect failures | Cron monitoring, error alerts |
| Optimize workflows | Continuous improvement loop |
| Archive unused | Skill deprecation policy |

---

## Execution Priority

```
1. Native API        →  Most reliable, fastest
2. CLI/Script        →  High reliability
3. Browser automation →  Medium (Playwright)
4. Desktop automation →  Lower (PowerShell, GUI)
5. Vision/mouse      →  Last resort (most fragile)
```

---

## Installation Status

| Tool | Hermes Venv | Status |
|------|-------------|--------|
| **Playwright** 1.61.0 | `import playwright.sync_api` | ✅ Installed |
| **Chromium** 1228 | `C:\Users\varas\AppData\Local\ms-playwright\chromium-1228` | ✅ Installed |
| **Firecrawl** 4.17.0 | `import firecrawl` | ✅ Installed (⚠️ needs API key) |
| **Scrapling** 0.4.10 | `import scrapling` | ✅ Installed |
| **OpenCV** 5.0.0 | `import cv2` | ✅ Installed |
| **Tesseract OCR** 5.4.0 | `C:\Program Files\Tesseract-OCR\tesseract.exe` | ✅ Installed |
| **pytesseract** | wired via `init_tools.py` | ✅ Wired |
| **httpx** 0.28.1 | `import httpx` | ✅ Installed |
| **watchdog** | `import watchdog` | ✅ Installed |
| **PyAutoGUI** | `import pyautogui` | 🟡 Not installed |
| **PowerShell** | Built-in to Windows | ✅ Available |
| **Brave** | `C:\Program Files\BraveSoftware\...\brave.exe` | ✅ Available |

## Persona Activation Flow

```
User Request
  │
  ▼
Automation Architect (primary — always first)
  │
  ├── Automation task → Computer Automation Architect → browser/desktop specialist
  ├── Reasoning task  → Principal Engineer / domain specialist
  ├── Security task   → Security Architect
  ├── Data task       → Data Engineer
  └── Unknown         → Research → classify → route
```

## Default Thinking Flow

```
Understand objective
  │
  ▼
Identify manual work / repetition
  │
  ▼
Analyze existing systems and tools
  │
  ▼
Find automation opportunities
  │
  ▼
Check existing skills
  │
  ▼
Check existing tools (API > CLI > Browser > Desktop > Vision)
  │
  ▼
Design the simplest reliable workflow
  │
  ▼
Build automation (only when necessary)
  │
  ▼
Add monitoring and recovery
  │
  ▼
Document for reuse
```
