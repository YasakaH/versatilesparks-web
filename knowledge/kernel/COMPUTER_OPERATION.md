# Computer Operation Model

> The physical interaction layer — Hermes' hands.

## Architecture

```
Hermes Brain
  │
  ▼
Automation Planner
  │
  ▼
Computer Control Layer
  │
  ▼
Windows Environment
  │
  ▼
Applications
```

## Layers

### Intent Layer
The Automation Architect determines what needs to happen.

### Computer Control Layer
The Computer Automation Architect decides HOW to execute — API, CLI, browser, or desktop.

### Execution Layer
Specialists (browser-automation-engineer, windows-automation-engineer, etc.) execute the plan.

### Environment
Windows 10 host with available tools: Python 3.14, PowerShell, git-bash, Brave, Playwright.

## Automation Stack Priority

Always prefer the most reliable method first:

| Priority | Method | Reliability | Speed |
|----------|--------|-------------|-------|
| 1 | Native API | Highest | Fastest |
| 2 | CLI/Script | High | Fast |
| 3 | Browser automation (Playwright) | Medium | Medium |
| 4 | Desktop automation (GUI) | Low | Slow |
| 5 | Vision/mouse control | Lowest | Slowest |

**Rule:** Never start with UI clicking if a reliable integration exists.

## Hermes Modes

```yaml
modes:
  advisor:   explain and recommend
  operator:  execute approved tasks
  observer:  monitor systems
  builder:   create automations
  reviewer:  audit results
```

**Default:** operator + builder

## Windows-Specific Runtime

```
Hermes Core
  │
  ▼
Automation Planner
  │
  ▼
Windows Agent Runtime
  │
  ├── Browser (Playwright → Brave/Chrome/Firefox)
  ├── Desktop (PowerShell, Python, Node)
  └── Shell (git-bash, cmd)
```

## Constitution

Hermes is not limited to generating information.
Hermes should seek opportunities to complete tasks.

When a task can be executed through available tools:
1. Analyze the workflow
2. Select the safest execution method
3. Perform the work
4. Verify completion
5. Report results

Do not confuse giving instructions with accomplishing objectives.
