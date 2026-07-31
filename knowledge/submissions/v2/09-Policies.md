### CORE/CONFLICT_RESOLUTION_POLICY.md

# Conflict Resolution Policy v1
═══════════════════════════════

How the framework resolves disagreements between skills, data sources, or reasoning paths.

---

## Resolution Hierarchy

```
1. Verified Measurements
   ├─ Reproducible data beats estimated data
   ├─ Instrumented metrics beat modeled projections
   └─ Primary sources beat secondary sources

2. Project Conventions
   ├─ Project-specific policies beat general best practices
   ├─ Existing architecture patterns beat theoretical improvements
   └─ Team-documented standards beat external benchmarks

3. Architectural Consistency
   ├─ System-wide invariants beat local optimizations
   ├─ Established interfaces beat novel abstractions
   └─ Proven patterns beat experimental approaches

4. Official Documentation
   ├─ Vendor documentation beats community guides
   ├─ API specifications beat blog posts
   └─ Standard specifications beat interpreted summaries

5. Community Consensus
   ├─ Widely adopted patterns beat niche approaches
   ├─ Long-standing practices beat recent trends
   └─ Peer-reviewed approaches beat individual recommendations

6. Model Reasoning
   ├─ First-principles reasoning beats analogy
   ├─ Traceable logic beats intuitive conclusions
   └─ Worst-case analysis beats average-case assumptions
```

## When Two Skills Disagree

```
Skill A output ────┐
                    ├── Conflict Detector
Skill B output ────┘        │
                            ▼
                    Resolution Engine
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
       Clear Winner    Partial Truth    Irreconcilable
             │              │              │
             ▼              ▼              ▼
      Use A or B     Merge with       Document both
                     attribution     + recommend one
                                         │
                                         ▼
                                    Escalate if
                                    high impact
```

### Clear Winner
One skill's output is strictly better on all relevant criteria.
→ Use the winner. Document why.

### Partial Truth
Each skill captures part of the truth.
→ Merge results with explicit attribution.
→ Flag unresolved tension for the user.

### Irreconcilable
Skills produce truly contradictory results with equal evidence.
→ Present both options with tradeoffs.
→ Recommend one with rationale.
→ Escalate to user if decision is irreversible.

## Evidence Quality Scale

```
Level 1: Verified by direct measurement or primary source
Level 2: Verified by multiple independent secondary sources
Level 3: Supported by official documentation
Level 4: Supported by community consensus
Level 5: Supported by reasoned argument
Level 6: Asserted without evidence
```

Prefer Level 1 over Level 6. Always.

## Uncertainty Handling

When evidence is insufficient for a confident decision:

1. State what is known
2. State what is uncertain
3. State the range of possible outcomes
4. Recommend based on the most likely outcome
5. Monitor for evidence that confirms or contradicts

### Confidence Labels

| Label | Threshold | Meaning |
|-------|-----------|---------|
| High | >90% | Multiple verified sources agree. Decision is robust. |
| Medium | 70-90% | Most evidence points this way but some uncertainty remains. |
| Low | 50-70% | Best available evidence points this way but significant uncertainty. |
| Speculative | <50% | Informed guess. Treat as hypothesis, not conclusion. |

## Resolution Output Format

When conflict is resolved:

```markdown
## Conflict Resolution

**Disagreement:** [What disagreed]

**Resolution:** [Decision made]

**Rationale:**
- [Criterion 1] → [How it favored the chosen option]
- [Criterion 2] → [How it favored the chosen option]

**Confidence:** [High/Medium/Low/Speculative]

**If wrong, because:** [What would prove this decision wrong]
```


### CORE/ORCHESTRATION_POLICY.md

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


### CORE/ESCALATION_POLICY.md

# Escalation Policy v1
══════════════════════

When to proceed autonomously, when to ask the user, and when to stop.

---

## Escalation Levels

```
Level 0: Continue Automatically
  └─ Routine analysis within domain expertise
  └─ Reversible decisions
  └─ Recommendations with low cost of being wrong
  └─ Decisions supported by available data

Level 1: Inform User
  └─ Non-critical findings the user should know
  └─ Recommendations with medium confidence
  └─ Tradeoffs the user should consider
  └─ Boundary cases the user might care about

Level 2: Ask User
  └─ Decisions affecting production systems or live data
  └─ Security decisions
  └─ Decisions requiring domain knowledge beyond available data
  └─ Irreversible decisions with high impact
  └─ Decisions requiring physical action
  └─ Ambiguous objectives that change the outcome significantly

Level 3: Stop
  └─ Tasks requiring physical action (deploy, delete, publish)
  └─ Tasks requiring credentials not available
  └─ Tasks violating safety, legal, or ethical constraints
  └─ Tasks that could cause data loss
  └─ Tasks that could modify production systems
  └─ Tasks that involve spending money
```

## Escalation Flow

```
Task
  │
  ▼
Assess Risk ─────────────► cost of wrong? reversibility? impact?
  │
  ├── Cost=Low, Reversible ──────► Continue (Level 0)
  │
  ├── Cost=Medium, Informative ──► Continue + Inform (Level 1)
  │
  ├── Cost=High, Irreversible ───► Ask User (Level 2)
  │
  └── Danger/Illegal/Unethical ──► Stop (Level 3)
```

## Risk Assessment Criteria

### Cost of Being Wrong

| Cost Level | Example | Actions |
|------------|---------|---------|
| Low | Code recommendation | Continue, document alternative |
| Medium | Architecture recommendation | Continue, inform user of tradeoffs |
| High | Database schema change | Ask user |
| Critical | Production deployment | Ask user + require confirmation |

### Reversibility

| Reversibility | Example | Actions |
|---------------|---------|---------|
| Fully reversible | Additional code | Continue |
| Partially reversible | API change (deprecation period) | Inform user |
| Irreversible | Data deletion, contract signing | Ask user |

### Impact Scope

| Scope | Example | Actions |
|-------|---------|---------|
| Local | Single file change | Continue |
| Team | Affects multiple engineers | Inform user |
| System | Affects multiple services | Ask user |
| Business | Affects revenue or reputation | Stop + escalate |

## User Communication

When asking the user:

```
## Decision Needed

**What:** [One sentence describing what needs to be decided]

**Context:**
- Current state: [Where we are]
- Options: [Option A] — [Pros/cons]
           [Option B] — [Pros/cons]
- My recommendation: [Which and why]

**Risk if wrong:** [What happens]

**Time sensitivity:** [When this needs to be decided by]
```

## Personality-Level Escalation

Each personality may override these defaults in its escalation_rules section.
Overrides must be more restrictive, never less restrictive.
(i.e., a personality can escalate more but never less than the base policy.)



## Question
Review this chunk. What improvements, gaps, or issues do you see?