> Originally from CORE/ORCHESTRATION_POLICY.md

# Orchestration Policy v1
═════════════════════════

Personalities are orchestrators, not capability containers.

## Core Principle

A personality's single responsibility is to:
1. Understand the objective
2. Decide which skills are needed
3. Decide their order and parallelism
4. Combine results
5. Resolve conflicts
6. Produce the final answer

Skills are workers. Personalities are decision-makers.

## Orchestration Flow

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

## Capability Graph

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

### How the Graph Works

1. Personality receives a task
2. Personality determines required capabilities
3. Capability Graph returns matching skills
4. Personality ranks skills by relevance, confidence, cost
5. Personality executes top-ranked skill(s)
6. If results are insufficient, fall through to next skill

### Graph Update Rules

- When a new skill is registered, its capabilities are added to the graph
- When a skill is deprecated, its capabilities are removed
- Multiple skills can provide the same capability (ranking decides)
- A skill can provide multiple capabilities

## Skill Lifecycle

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

## Orchestration Rules

### Rule 1: No Capability Duplication
A personality must never implement logic that exists in a skill.
If the capability exists, the personality dispatches. Full stop.

### Rule 2: Sequential by Default
Skills execute in the order specified by the workflow.
Parallel execution is opt-in and must be explicitly declared.

### Rule 3: Early Termination
If a skill provides sufficient evidence to satisfy the objective,
subsequent skills may be skipped. Document the rationale.

### Rule 4: Fallback Chain
If tier_1 skills fail to produce results:
  → Try tier_2 skills
  → Try tier_3 skills
  → Try general-analysis
  → Escalate

### Rule 5: Context Preservation
Each skill receives the full context of the task so far.
Results from prior skills are passed as input to subsequent skills.
