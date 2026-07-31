# Security Model

> Security boundaries, threat models, and safe operation principles.

## Core Principles
1. Least privilege — operate with minimum required access
2. Defense in depth — multiple layers of verification
3. Auditability — every security-relevant action is logged
4. Fail secure — default-deny on all permissions

## Security Gates
- **Input validation** — Sanitize all external inputs
- **Output review** — No sensitive data in responses
- **Escalation check** — Approve high-risk operations
- **Session isolation** — No cross-session data leakage
