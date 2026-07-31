> Originally from CORE/PERSONALITY_CREATION_GUIDE.md

# Personality Creation Guide v1
══════════════════════════════

How to create a new personality in the Hermes Personality Framework.

---

## Step-by-Step

```
Need new personality?
  │
  ▼
1. Search installed personalities ──► Exists? → Reuse
  │                                      No? → Continue
  ▼
2. Identify domain and category
  │
  ▼
3. Inherit BASE_PERSONALITY
  │
  ▼
4. Override unique fields
  │
  ▼
5. Validate against schema
  │
  ▼
6. Register in capacity registry
  │
  ▼
7. Create 3 example scenarios
  │
  ▼
8. Test with a real task
  │
  ▼
   Done
```

## Step 1: Search

Before creating, search:
1. Installed personalities — does one already cover this domain?
2. Is the domain already served by an existing personality with a different name?
3. Can the task be accomplished by selecting a different set of skills on an existing personality?

**If a close match exists but isn't perfect:** extend it. Don't create a new one.

## Step 2: Categorize

| Category | Example Roles | Domain Characteristics |
|----------|---------------|----------------------|
| engineering | principal-engineer, backend-engineer, devops-engineer | Building and maintaining software |
| architecture | software-architect, systems-architect, solution-architect | System design and structure |
| ai | ai-engineer, prompt-engineer, agent-architect | AI system design and development |
| research | research-scientist, fact-checker, competitive-intelligence | Investigation and analysis |
| devops | devops-engineer, platform-engineer, sre | Infrastructure and operations |
| security | security-architect, threat-modeler, security-engineer | Protection and compliance |
| product | product-manager, product-owner, technical-product-manager | Product definition and strategy |
| design | ux-designer, ui-designer, design-system-architect | User experience and interface |
| data | data-scientist, data-engineer, data-analyst | Data analysis and engineering |
| business | business-strategist, management-consultant, operations-consultant | Strategy and operations |
| finance | financial-analyst, investment-analyst, risk-analyst | Financial analysis and decisions |
| legal | legal-advisor, contract-reviewer, compliance-advisor | Legal and compliance |
| writing | technical-writer, copywriter, editor | Content and documentation |
| marketing | seo-strategist, content-strategist, brand-strategist | Marketing and growth |
| operations | project-manager, program-manager, scrum-master | Process and delivery |
| education | tutor, curriculum-designer, learning-coach | Teaching and learning |
| healthcare | healthcare-consultant, clinical-analyst, medical-researcher | Healthcare domain |
| leadership | cto, ceo, engineering-manager | Organizational leadership |
| creative | creative-director, game-designer, story-architect | Creative direction |

## Step 3: Inherit

Every personality must extend BASE_PERSONALITY:

```markdown
---
name: my-new-personality
version: 1.0.0
category: engineering
inherits: BASE_PERSONALITY v1.0.0
overrides:
  - mission
  - mental_models
  - decision_priorities
  - workflow
  - preferred_skills
---
```

## Step 4: Override

Override ONLY these fields (minimum viable override):

### Required Override
- **Mission** — Always custom
- **Mental Models** — Domain-specific models that define expert thinking
- **Decision Priorities** — Weights reflecting domain tradeoffs
- **Workflow** — Steps specific to this role
- **Preferred Skills** — Skills this personality primarily orchestrates

### Strongly Recommended Override
- **Core Principles** — Beliefs unique to this domain
- **Heuristics** — Rules of thumb developed through experience
- **Failure Modes** — How this personality fails when wrong
- **Anti-Patterns** — What this personality actively avoids
- **Quality Gates** — Domain-specific verification steps
- **Output Templates** — If the standard template doesn't fit

### Optional Override
Everything else inherits from BASE_PERSONALITY.

## Override Declaration

Every override must declare why:

```yaml
overrides:
  mission: "Specialized for performance engineering — mission is narrower than base"
  mental_models: "Performance domain requires different framing than general engineering"
  decision_priorities: "Weights prioritize latency and throughput over elegance"
  workflow: "Performance analysis follows a specific profiler→analyze→optimize pattern"
```

## Step 5: Validate

After creating, run the personality through these checks:

- [ ] Schema compliance — all required fields present
- [ ] Overrides declared — rationale provided for each
- [ ] Skills exist — referenced skills are in the capability registry
- [ ] Internal consistency — no field contradicts another
- [ ] Decision priorities sum to meaningful tradeoffs (not all 100)
- [ ] Workflow is actionable — concrete steps, not abstractions
- [ ] Mental models are authentic — sound like an expert, not a job description
- [ ] Quality gates are testable — each can be answered yes/no
- [ ] Escalation path terminates — every option leads to continue/ask/stop

## Step 6: Register

```bash
# Add to the capability registry
personalities/CORE/capability-register.json
```

## Step 7: Example Scenarios

Create 3 example scenarios to validate the personality:

```
## Example 1: [Common task]
Task: [Description]
Expected workflow: [Which skills, in what order]
Expected output: [What the personality should produce]

## Example 2: [Edge case]
Task: [Description]
Expected handling: [How the personality should deal with ambiguity]

## Example 3: [Escalation]
Task: [Description]
Expected escalation: [When and how to ask the user]
```

## Step 8: Test

Run the personality against a real task. Verify:
- Workflow is followed correctly
- Skills are selected appropriately
- Quality gates pass
- Output matches expectations
- Edge cases are handled

## When NOT to Create a Personality

- ✗ The task can be done by combining existing personalities
- ✗ The domain is already covered by another name
- ✗ The personality would have no unique skills or mental models
- ✗ The personality would duplicate logic from an existing one
- ✗ The use case is a one-off, not a recurring pattern

## Design Principles

1. **One mission, many skills.** A personality's mission is its unique contribution. Skills are shared.
2. **Depth over breadth.** A personality that deeply understands one domain beats one that superficially covers many.
3. **Reality over labels.** Mental models should reflect how experts actually think, not what job descriptions say.
4. **Tradeoffs over platitudes.** Decision priorities with real weights force honest tradeoffs.
5. **Failure modes as features.** Explicit failure modes make the personality more useful, not less.
