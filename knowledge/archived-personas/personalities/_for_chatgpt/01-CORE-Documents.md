# HPF v2 — CORE Documents (27 files)

## Purpose
Foundation layer that all PERSONA.md files inherit. Think: "what every Hermes agent must know."

## File List

### Knowledge (5 files)
1. **CORE/DOMAIN_KNOWLEDGE.md** — Software engineering, architecture, domain-driven design
2. **CORE/TECH_STACK.md** — Languages, frameworks, runtime ecosystems (TypeScript, React, Node.js, Python)
3. **CORE/DEVELOPER_TOOLING.md** — IDEs, git, CI/CD, cloud providers, observability tools
4. **CORE/MCP_KNOWLEDGE.md** — Model Context Protocol, tool integration patterns
5. **CORE/SECURITY_KNOWLEDGE.md** — OWASP, authentication, authorization patterns

### Cognition (6 files)
6. **CORE/REASONING_PATTERNS.md** — Thinking models: first-principles, systems-thinking, trade-off analysis
7. **CORE/THINKING_MODELS.md** — Mental models catalog (Pareto, inversion, Bayesian updating, etc.)
8. **CORE/DECISION_FRAMEWORK.md** — When to ask vs infer, conflict resolution, priority scoring, decision documentation
9. **CORE/PLANNING_FRAMEWORK.md** — Task decomposition, complexity estimation, execution strategy selection
10. **CORE/VERIFICATION_PATTERNS.md** — Self-review checklist, test generation, assumption validation
11. **CORE/UNCERTAINTY_HANDLING.md** — How to handle low confidence, incomplete evidence, conflicting sources

### Runtime Behavior (6 files)
12. **CORE/CONTINUOUS_IMPROVEMENT.md** — Merges error handling + learning/adaptation into one feedback loop
13. **CORE/CAPABILITY_REGISTRY.md** — How to discover, evaluate, and use tools/personas
14. **CORE/SKILL_ARCHITECTURE.md** — How skills are structured, loaded, and executed
15. **CORE/SKILL_SELECTION_POLICY.md** — Policy for selecting among available skills
16. **CORE/CONVERSATION_MANAGEMENT.md** — Context handling, session management, memory
17. **CORE/OBSERVABILITY.md** — Tracing, logging, metrics for agent behavior

### Communication (4 files)
18. **CORE/ANSWER_PATTERNS.md** — How to structure responses (lead with answer, provide evidence)
19. **CORE/COMMUNICATION_PATTERNS.md** — How to challenge, escalate, disagree appropriately
20. **CORE/EXPLANATION_PATTERNS.md** — When to go deep vs shallow, analogies, examples
21. **CORE/OUTPUT_STANDARD.md** — Response format requirements

### Execution & Strategy (5 files)
22. **CORE/EXECUTION_WORKFLOW.md** — Standard lifecycle: Understand → Plan → Validate → Execute → Verify → Reflect
23. **CORE/ESCALATION_POLICY.md** — When to ask the user, when to refuse
24. **CORE/PRIORITIZATION_FRAMEWORK.md** — Correctness > Safety > Maintainability > Performance hierarchy
25. **CORE/CONFLICT_RESOLUTION_POLICY.md** — How persona advice conflicts are resolved

### Architecture & Standards (4 files)
26. **CORE/ARCHITECTURE_PRINCIPLES.md** — System design principles
27. **CORE/ENGINEERING_PRINCIPLES.md** — Engineering best practices

## Category Changes Since v1

| Change | Reason |
|--------|--------|
| DECISION_ENGINE merged INTO DECISION_FRAMEWORK | Overlap reduced from 2 files to 1 |
| Added PLANNING_FRAMEWORK | Runtime cognition gap identified in external review |
| Added VERIFICATION_PATTERNS | Runtime cognition gap identified in external review |
| Added UNCERTAINTY_HANDLING | Runtime cognition gap identified in external review |
| CONTINUOUS_IMPROVEMENT replaces ERROR_HANDLING + LEARNING_PATTERNS | Reduces duplication, single source of truth for adaptation |
| TOOL_KNOWLEDGE renamed to DEVELOPER_TOOLING | More precise naming |
| "Constraints" category split into "Runtime" and "Constraints" | ERROR_HANDLING and LEARNING aren't constraints — they're operational behavior |

## Question for ChatGPT
Are these 27 CORE docs the right set? Any gaps? Any that should be merged or split?
