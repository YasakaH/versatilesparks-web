# Architecture

> Consolidated from: CORE/ARCHITECTURE_PRINCIPLES.md, CORE/ORCHESTRATION_POLICY.md, CORE/EVOLUTION_ENGINE.md

---

## Execution Modes

Hermes runs tasks in one of three modes. Most tasks never need a DAG.

| Mode | Frequency | When | How |
|------|-----------|------|-----|
| **Direct** | ~80% | Single expert, linear question → answer | One personality, one skill. Execute, return. |
| **Collaborative** | ~15% | Multiple perspectives needed but no dependencies | N experts in parallel → synthesis |
| **Orchestrated** | ~5% | Dependencies exist, artifacts must compose | Full DAG with ordered stages |

### Direct Mode (80%)
```
Question
  │
  ▼
Route to best-matching personality
  │
  ▼
Execute single skill
  │
  ▼
Return answer
```

### Collaborative Mode (15%)
```
Question
  │
  ▼
Route to N independent personalities
  │
  ├── Personality A ──► Output A
  ├── Personality B ──► Output B
  └── Personality C ──► Output C
  │
  ▼
Synthesis → Unified answer
```

### Orchestrated Mode (5%)
Trigger DAG only when:
- 3+ independent outputs needed
- Dependencies exist between outputs
- Artifacts must combine at the end
- Failure cost is high

```
Discovery → Research → Design → Review → Execution
                │           │
                ▼           ▼
            Validation   Prototype
```

### Mode Selection
```
Can one personality handle it?   → Direct
Multiple independent opinions?   → Collaborative
Sequential dependencies exist?   → Orchestrated
```

---

## From: ARCHITECTURE_PRINCIPLES.md

### Purpose

Define the architectural principles every Hermes agent applies when designing, evaluating, or modifying systems. These are universal — they apply regardless of domain, language, or framework.

### Principles

#### 1. Deep Modules over Shallow Modules
Prefer modules that hide complexity behind simple interfaces. A deep module does one thing well and has a simple API relative to the complexity it manages.

#### 2. Composition over Inheritance
Favor assembling behavior from small, interchangeable parts over deep class hierarchies. Composition is easier to test, change, and reason about.

#### 3. Loose Coupling, High Cohesion
Modules should have minimal dependencies on each other (loose coupling) and strong internal relatedness (high cohesion).

#### 4. Explicit over Implicit
Make dependencies, side effects, and data flow visible. Magic (automatic behavior) is convenient but makes systems unpredictable.

#### 5. Policies over Flags
Replace boolean flags with explicit policy objects. A flag like `enabled: true` becomes a policy like `rate_limit: { max: 100, window: 60s }`.

#### 6. Immutable State Where Possible
Prefer immutable data structures. When state must change, make the transition explicit and atomic.

#### 7. Idempotency
Design operations so they can be safely retried. The same input should always produce the same outcome.

#### 8. Fail Fast, Fail Clearly
Validate inputs early. When something goes wrong, produce a clear error message — not a cryptic exception or silent no-op.

#### 9. Observability First
Every component should expose: what it's doing, how long it took, what errors occurred, and what it depends on. Log events, not just errors.

#### 10. You Aren't Gonna Need It (YAGNI)
Build what you need now, not what you might need later. Premature abstraction is the root of most over-engineering.

#### 11. Keep It Simple, Stupid (KISS)
The simplest solution that satisfies requirements is usually the best. Complexity should be justified by necessity, not cleverness.

#### 12. Don't Repeat Yourself (DRY)
Every piece of knowledge should have a single, unambiguous representation. But prefer duplication over the wrong abstraction.

### Domain-Specific Extensions

| Domain | Additional Principles |
|--------|----------------------|
| Frontend | Progressive enhancement, accessibility first, mobile-first |
| Backend | Stateless when possible, database-as-boundary, API-first |
| Data | Immutable data lake, schema-on-read, idempotent pipelines |
| Security | Least privilege, defense in depth, zero trust |
| AI/ML | Reproducible experiments, data versioning, model governance |

---

## From: ORCHESTRATION_POLICY.md

Personalities are orchestrators, not capability containers.

### Core Principle

A personality's single responsibility is to:
1. Understand the objective
2. Decide which skills are needed
3. Decide their order and parallelism
4. Combine results
5. Resolve conflicts
6. Produce the final answer

Skills are workers. Personalities are decision-makers.

### Orchestration Flow

```
Task
  │
  ▼
Intent Analysis ─────────► What is being asked?
  │
  ▼
Capability Planning ────► What capabilities are needed?
  │
  ▼
Skill Selection ─────────► Which skills provide those capabilities?
  │
  ▼
Execution Planning ─────► What order? What's parallel?
  │
  ▼
Execution ───────────────► Invoke skills
  │
  ▼
Result Merging ─────────► Combine outputs
  │
  ▼
Conflict Resolution ────► Resolve disagreements
  │
  ▼
Validation ──────────────► Pass quality gates
  │
  ▼
Output ─────────────────► Deliver final answer
```

### Capability Graph

Skills advertise capabilities. Personalities request capabilities.
The capability graph maps capabilities ← skills.

```
Capability: code-review
  Provided by: code-review skill, requesting-code-review skill

Capability: performance-analysis
  Provided by: latency-analysis skill, performance-first skill

Capability: research
  Provided by: research skill, deep-research skill, entity-research skill
```

#### How the Graph Works

1. Personality receives a task
2. Personality determines required capabilities
3. Capability Graph returns matching skills
4. Personality ranks skills by relevance, confidence, cost
5. Personality executes top-ranked skill(s)
6. If results are insufficient, fall through to next skill

#### Graph Update Rules

- When a new skill is registered, its capabilities are added to the graph
- When a skill is deprecated, its capabilities are removed
- Multiple skills can provide the same capability (ranking decides)
- A skill can provide multiple capabilities

### Skill Lifecycle

```
Discovery ──► Registration ──► Ranking ──► Execution ──► Feedback
                                                             │
                                                             ▼
                                                         Reinforcement
```

1. **Discovery:** Find skill via capability matching
2. **Registration:** Skill added to execution plan
3. **Ranking:** Score skill by relevance, quality, cost
4. **Execution:** Run skill with provided context
5. **Feedback:** Record outcome for future ranking

### Orchestration Rules

#### Rule 1: No Capability Duplication
A personality must never implement logic that exists in a skill.
If the capability exists, the personality dispatches. Full stop.

#### Rule 2: Sequential by Default
Skills execute in the order specified by the workflow.
Parallel execution is opt-in and must be explicitly declared.

#### Rule 3: Early Termination
If a skill provides sufficient evidence to satisfy the objective,
subsequent skills may be skipped. Document the rationale.

#### Rule 4: Fallback Chain
If tier_1 skills fail to produce results:
  → Try tier_2 skills
  → Try tier_3 skills
  → Try general-analysis
  → Escalate

#### Rule 5: Context Preservation
Each skill receives the full context of the task so far.
Results from prior skills are passed as input to subsequent skills.

---

## From: EVOLUTION_ENGINE.md

Hermes continuously improves itself through systematic analysis of its own performance.

### Weekly Evolution Cycle

Every week, the Evolution Engine runs:

```
Collect Data (7 days of traces)
  │
  ▼
Analyze Patterns
  │
  ├── Which skills were never used?    → Archive or merge
  ├── Which personalities overlap?     → Merge or redirect
  ├── Which workflows repeat?          → Template → Playbook
  ├── Which failures repeat?           → Improve → Skill
  ├── Which bottlenecks exist?         → Optimize
  ├── Which costs are highest?         → Optimize routing
  └── Which confidence is lowest?      → Improve → Retrain
  │
  ▼
Generate Recommendations
  │
  ▼
Apply Automated Improvements
  │
  ▼
Review Manual-Suggested Improvements
  │
  ▼
Measure Impact (next week's data)
```

### Improvement Categories

#### Skills
```
SKILL_NEVER_USED      → Archive (keep for reference, remove from active registry)
SKILL_LOW_CONFIDENCE  → Improve documentation, add examples, fix failure modes
SKILL_HIGH_COST       → Optimize token usage, find cheaper alternative
SKILL_DUPLICATES      → Merge with overlapping skill
SKILL_HIGH_ERROR      → Debug root cause, improve validation
SKILL_MISSING         → Create from repeated task pattern
```

#### Personalities
```
PERSONALITY_NEVER_USED      → Archive
PERSONALITY_OVERLAP         → Merge with overlapping personality or clarify boundaries
PERSONALITY_LOW_SUCCESS     → Improve mental models, decision priorities, skill selection
PERSONALITY_HIGH_COST       → Optimize workflow, reduce unnecessary skill invocations
PERSONALITY_MISSING         → Create from personality creation guide
```

#### Workflows
```
WORKFLOW_REPEATED_3x  → Template → Playbook
WORKFLOW_FAILING      → Debug failure points, add validation, add fallback skills
WORKFLOW_SLOW         → Parallelize independent steps, optimize skill selection
```

#### Knowledge
```
OUTDATED_KNOWLEDGE    → Flag for review
MISSING_KNOWLEDGE     → Create from research
CONTRADICTORY         → Resolve or escalate
```

### Self-Correction Rules

#### When a skill fails:
```
Skill fails
  │
  ├── Retry (up to 3x)
  │     └── Succeeds → Log as recovered failure
  │
  └── Fails after retries
        ├── Is alternative skill available? → Use fallback
        └── No alternative → Flag for creation
```

#### When confidence is low:
```
Confidence < 0.6
  │
  ├── Can additional evidence be obtained? → Research
  ├── Can alternative personality produce better result? → Switch
  └── Neither → Flag as low-confidence output, mark for improvement
```

#### When cost exceeds budget:
```
Cost > Budget
  │
  ├── Can a cheaper model be used? → Re-route
  ├── Can fewer skills be invoked? → Reduce scope
  ├── Can the prompt be optimized? → Reduce token usage
  └── None of above → Escalate with cost analysis
```

### Trigger Conditions

| Trigger | Action | Automation |
|---------|--------|------------|
| Skill unused for 30 days | Archive skill | Auto |
| Skill error rate > 10% | Flag for review | Auto (flag) |
| 3 identical task patterns | Create playbook | Suggest |
| 5 identical task patterns | Auto-create playbook | Auto |
| Personality never selected | Archive | Auto (after 45 days) |
| Personality > 30% overlap | Flag for merge | Suggest |
| Cost per request increased 50% | Alert + analyze | Auto (alert) |
| Confidence trending down | Alert + retrain | Auto (alert) |
| Repeated failure mode | Create prevention skill | Suggest |
| New domain emerges | Suggest new personality | Suggest |

### Evolution Score

Weekly health score (0-100):

```
Evolution Score = (Success Rate × 25) +
                 (Skill Utilization × 15) +
                 (Personality Utilization × 15) +
                 (Cost Efficiency × 15) +
                 (Confidence Average × 15) +
                 (Improvement Velocity × 15)
```

- **Success Rate:** % of tasks completed without error or escalation
- **Skill Utilization:** % of registered skills used in the last week
- **Personality Utilization:** % of personalities selected at least once
- **Cost Efficiency:** average cost per successful task vs. benchmark
- **Confidence Average:** average confidence across all outputs
- **Improvement Velocity:** new skills + improved personalities / week
