# Plugin API v1 — Security & Permissions
══════════════════════════════════════════

## Permission Model

Every plugin declares permissions explicitly. No implicit trust.

```
Permission Categories:
  filesystem: { read: bool, write: bool }
  network: { external_apis: string[], localhost: bool }
  credentials: { required: bool, keys: string[] }
  execution: { shell_access: bool, code_execution: bool }
```

## Permission Levels

| Level | Icon | Description | Audit Required |
|-------|------|-------------|----------------|
| **L0** | 🔒 | Read-only, no external | Automated only |
| **L1** | 🔐 | External API, no write | Automated + spot check |
| **L2** | ⚠️ | File write, credentials | Full automated review |
| **L3** | 🚨 | Shell exec, network write | Manual approval |

## Permission Boundaries

- A plugin cannot access files outside its designated directory
- A plugin cannot access credentials it didn't declare
- A plugin cannot spawn network connections it didn't declare
- A plugin cannot modify other plugins, skills, or personalities
- A plugin's execution is sandboxed from the host system

## Approval Matrix

| Permission | L0 | L1 | L2 | L3 |
|------------|----|----|----|----|
| Read-only files | Auto | Auto | Auto | Auto |
| External API (read) | Auto | Auto | Spot | Manual |
| File write | Auto | Spot | Full | Manual |
| Credentials | Auto | Spot | Full | Manual |
| Shell exec | - | - | Manual | Manual |
| Network (write) | - | Spot | Manual | Manual |
