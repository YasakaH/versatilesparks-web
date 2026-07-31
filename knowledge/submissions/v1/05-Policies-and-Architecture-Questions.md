# HPF v2 — Policies & Architecture Questions

## 7 Policies

| Policy | Purpose |
|--------|---------|
| `policies/SECURITY.md` | Authentication, authorization, data protection |
| `policies/PRIVACY.md` | PII handling, data retention, user consent |
| `policies/ETHICS.md` | Ethical guidelines, bias detection, fairness |
| `policies/QUALITY.md` | Code quality, testing standards, documentation |
| `policies/COMMUNICATION.md` | Communication patterns, escalation, notification |
| `policies/DECISION_MAKING.md` | Decision framework, risk assessment, approvals |
| `policies/TOOL_USE.md` | Tool selection, verification, safety |

## Architectural Questions for ChatGPT

1. **Personality as Orchestrator**: Currently, personas are Orchestrators that invoke Skills (Workers). Should I separate the orchestrator behavior into a dedicated meta-layer, keeping personas as pure domain-knowledge containers?

2. **Skill Selection**: Currently skills advertise capabilities via the Capability Registry. The persona selects skills based on capability match. Should I add a weighting/ranking layer for skill selection?

3. **Conflict Resolution**: When multiple personas disagree (e.g., Security says "block it", Product says "ship it"), how should the agent decide? Current design: priority-based escalation.

4. **Observability**: Should every persona activation be logged with outcome metrics (usefulness score, error rate, invocation count)?

5. **Plugin Lifecycle**: Should plugins be able to install/activate personas? Or should plugins be limited to tool/skill contributions?

6. **Versioning**: Should PERSONA.md files have explicit version dependencies on CORE docs and specific skill versions?

7. **Testing Strategy**: How to unit-test a persona's behavior when it depends on LLM output?
