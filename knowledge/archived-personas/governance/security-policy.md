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
