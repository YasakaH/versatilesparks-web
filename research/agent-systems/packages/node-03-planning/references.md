# Node 03: Planning — Reference Document

> **Status:** Wave 1 Draft
> **Package Version:** 0.1.0
> **Canon Version:** 1.0
> **Specification Version:** 2.0
> **Last Updated:** 2026-07-22

---

## 1. Scope Boundaries

### In Scope
- Goal decomposition into actionable, non-overlapping steps
- Constraint satisfaction and validation (budget, safety, ordering, resource)
- Plan representation formats (DAGs, dependency graphs, sequential plans)
- Dependency graph construction and cycle detection
- Failure anticipation and mitigation planning
- Multi-agent plan coordination (sub-goal allocation across agents)
- Plan verification readiness (producing checkable intermediate milestones)

### Out of Scope
- Perception of environmental signals (Node 01) — Planning consumes observations, does not perceive them
- Intent formation and model routing (Node 02: Decision Engine) — Planning decomposes intent; Decision Engine forms it
- Temporal resource allocation and concurrency control (Node 04: Scheduling) — Planning produces dependency graphs; Scheduling orders them temporally
- Action execution on surfaces (Node 05: Execution) — Planning declares what to do; Execution does it
- Outcome verification (Node 06: Verification) — Planning produces success criteria per step; Verification judges results
- Failure recovery and path switching (Node 07: Recovery) — Planning anticipates failures; Recovery diagnoses and repairs them
- Learning from past plans (Node 08: Learning) — Planning consults past experience; Learning extracts patterns from outcomes
- Session memory management (Node 09: Working Memory) — Planning stores plans; Memory manages retention
- Persistent knowledge storage (Node 10: Long-term Memory) — Planning references learned constraints; Memory persists them
- Environment state tracking (Node 11: Environment State) — Planning reads state; Environment State maintains it
- Observability and tracing (Node 12: Observability) — Planning emits spans; Observability aggregates them
- Token economics and inference cost modeling (Node 13: Economics) — Planning respects budget constraints; Economics models costs
- Security policy enforcement (Node 14: Security) — Planning declares safety constraints; Security enforces policies
- Governance and compliance checking (Node 15: Governance) — Planning respects compliance requirements; Governance defines them
- Runtime and compute environment (Node 16: Runtime) — Planning declares resource needs; Runtime provisions them
- Execution surface specifics (Nodes 17–22) — Planning is surface-agnostic; surfaces provide signal availability

---

## 2. Executive Summary

Planning is the cognitive bridge between intent and action. It answers the question "What exactly do I need to do, in what order, and what could go wrong?" — transforming the Decision Engine's high-level intent into a structured, executable plan.

The critical architectural insight is that planning is a **constraint satisfaction problem**, not merely a sequencing problem. Every step must satisfy budget constraints, safety constraints, ordering constraints, and resource constraints simultaneously. The plan is the artifact that makes all these constraints explicit and machine-readable.

Three planning paradigms dominate production agent systems today: **sequential decomposition** (linear step chains for simple tasks), **dependency-graph planning** (DAGs for tasks with parallelizable sub-goals), and **multi-agent coordination** (sub-goal allocation across multiple agents with inter-agent dependencies). Which paradigm applies depends on task complexity, available compute, and the number of agents in the system.

Planning quality directly bounds execution quality. A perfect scheduler cannot rescue a poorly decomposed plan, and flawless execution cannot compensate for missing dependency edges. Planning is the node where abstract intent becomes concrete action — and where most agent failures originate.

---

## 3. Canon Definition

> **Canon Node 03: Planning**
> The process of decomposing a goal into actionable steps with explicit dependencies, constraints, and failure anticipations.

**Purpose:** To transform high-level intent into a structured, executable plan that Scheduling can order and Execution can perform.

**Inputs:** Refined intent from Decision Engine (Node 02); environment state (Node 11); past experience and constraint patterns (Node 08: Learning).
**Outputs:** Structured plan with steps, dependency DAG, constraints, and failure modes → Scheduling (Node 04).
**Dependencies:** Decision Engine (intent to decompose), Environment State (constraint validation), Learning (historical patterns).
**Feeds:** Scheduling (plan to order), Observability (planning spans).

See also: Node 02: Decision Engine, Node 04: Scheduling, Node 08: Learning, Node 11: Environment State.

---

## 4. Mental Model

### The Planning Pipeline

```
Intent from Decision Engine
         │
         ▼
Goal Refinement ──┐
                 │  Is the goal atomic enough?
                 ▼
Constraint Analysis ── Budget, safety, ordering, resource limits
                 │
                 ▼
Step Decomposition ── Break goal into non-overlapping, executable steps
                 │
                 ▼
Dependency Graph Construction ── Identify prerequisites and parallelism opportunities
                 │
                 ▼
Failure Anticipation ── For each step: what could go wrong? Mitigation?
                 │
                 ▼
Structured Plan Output
  ├─ Steps (ordered list of actions)
  ├─ Dependencies (DAG of step prerequisites)
  ├─ Constraints (per-step resource/temporal requirements)
  └─ Failure Modes (anticipated risks with mitigations)
                 │
                 ▼
Scheduling (Node 04) ← Receives structured plan for temporal ordering
```

### Three Planning Paradigms

| Paradigm | Complexity | Parallelism | Best For |
|---|---|---|---|
| Sequential Decomposition | Low | None | Linear tasks (3–5 steps), single-agent workflows |
| Dependency-Graph Planning | Medium | Partial (DAG-parallel) | Multi-step tasks with independent sub-goals |
| Multi-Agent Coordination | High | Full (inter-agent) | Complex tasks requiring specialized agents |

**Key insight:** These paradigms are not mutually exclusive. Production systems often compose them — a sequential plan for the outer loop with dependency-graph sub-plans for complex steps. The paradigm choice is a Decision Engine output, not a Planning internal decision.

---

## 5. Design Invariants

These are timeless truths about Planning that survive tool changes, model shifts, and architecture evolution. If an assertion fails any test below, it belongs in Modules B or C, not here.

**Test criteria:**
1. True if all today's tools disappear? (Not a pattern/implementation detail)
2. Still true in 10 years as architectures evolve? (Not a trend)
3. Fundamental to this node's role in the system? (Not a supporting observation)

| # | Invariant | Rationale |
|---|---|---|
| 1 | **Every plan is a constraint satisfaction problem.** | Planning is never just sequencing — it is simultaneously satisfying budget, safety, ordering, and resource constraints. A plan that satisfies ordering but violates budget is not a plan; it is a wish list. |
| 2 | **Dependency graphs are the minimal correct representation.** | Linear plans lose parallelism information. Tree plans lose cross-cutting dependencies. Only a DAG captures all prerequisite relationships without redundancy. If a plan cannot be represented as a DAG, it is underspecified. |
| 3 | **Step granularity is a tradeoff, not an optimization.** | Too coarse: Scheduler cannot parallelize effectively. Too fine: Planning overhead dominates execution time. The optimal granularity is where planning cost equals the parallelism benefit gained — a structural property of the task, not a tuning knob. |
| 4 | **Unanticipated failure is the default state.** | Every step has unknown-unknown risks. Planning that does not explicitly anticipate failure modes is fragile by construction. The quality of a plan is measured by its failure coverage, not its happy-path length. |
| 5 | **Planning quality bounds execution quality.** | Mathematical constraint, not heuristic. A perfect scheduler cannot execute a poorly decomposed plan. Flawless execution cannot compensate for missing dependency edges. The plan is the upper bound on achievable outcomes. |
| 6 | **Decomposition creates new failure modes.** | Breaking a monolithic goal into steps introduces inter-step failure modes (step N produces wrong output for step N+1) that do not exist in the monolithic formulation. Planning must account for these emergent failures. |
| 7 | **Plans are hypotheses, not guarantees.** | A plan is a prediction about what sequence of actions will achieve a goal under stated constraints. It is falsifiable by execution. Good plans are designed to be tested incrementally, not executed atomically. |

---

## Module A — Theory & Architecture

### 6. Historical Evolution

**Deterministic Planning Era (1990s–2010s):** Classical AI planning used STRIPS and PDDL (Planning Domain Definition Language) to represent goals, actions, and preconditions as formal logic. planners like Fast Downward and SATPLAN could solve complex logistics problems but required hand-authored domain models. [Primary: AI Planning Survey, Ghallab et al.]

**LLM-Assisted Planning Era (2023–2024):** Large language models entered planning as decomposers — given a goal, generate steps. Early approaches used Chain-of-Thought prompting for step generation. ReAct patterns combined reasoning with action traces, producing plans that interleaved thought and execution. [Primary: ReAct Pattern, Yao et al. 2022]

**Multi-Agent Planning Era (2024–2025):** Frameworks like AutoGen and LangGraph introduced structured multi-agent planning where agents negotiate sub-goals, share plans, and coordinate through message passing. LangGraph's "planner-executor" pattern became the dominant architecture for complex tasks. [Engineering: LangGraph Planning Patterns, 2024]

**Production Planning Era (2025–Present):** Real-world agent deployments revealed that planning quality is the single largest predictor of task success rate. Production systems now treat planning as a distinct, testable node — not an implicit LLM capability. Dependency graphs, constraint solvers, and failure anticipation are explicit, not emergent.

### 7. Architecture Overview

Planning sits between the Decision Engine and Scheduling in the agent loop. It receives a refined intent and produces a structured plan. The architecture has three layers:

1. **Goal Refinement Layer:** Converts high-level intent into a decomposable goal statement. Validates that the goal is atomic enough for decomposition but not so granular that it duplicates Scheduling's work.

2. **Decomposition Layer:** The core planning engine. Applies constraint satisfaction to break the goal into steps, constructs a dependency DAG, and validates that all declared constraints can be satisfied simultaneously.

3. **Anticipation Layer:** For each step in the plan, identifies failure modes and proposes mitigations. Produces a "plan risk profile" that Scheduling uses for priority assignment.

### 8. Core Components

**Goal Refinement:** The Decision Engine provides intent; Planning refines it into a decomposable goal. This involves clarifying ambiguous objectives, identifying implicit constraints, and establishing measurable success criteria per step. A goal that is too vague ("research competitors") produces a useless plan. A goal that is too specific ("open Chrome, navigate to competitor.com, screenshot") leaves no room for adaptive execution.

**Step Decomposition:** Breaking the goal into executable steps. Each step must be:
- Atomic: Cannot be further decomposed without losing semantic meaning
- Non-overlapping: No two steps accomplish the same sub-goal
- Executable: Can be performed by available execution surfaces
- Verifiable: Has observable success criteria

**Dependency Graph Construction:** Identifying prerequisite relationships between steps. A dependency graph (DAG) encodes:
- Direct dependencies (step B requires step A's output)
- Indirect dependencies (step C requires step B, which requires step A)
- Parallelism opportunities (steps A and B have no dependency relationship)
- Critical path (longest dependency chain determines minimum plan duration)

**Constraint Satisfaction:** Validating that all constraints are simultaneously satisfiable. Constraints fall into four categories:
- Budget: Token limits, monetary cost ceilings per step and overall
- Safety: Actions that must never be performed, data that must never be accessed
- Ordering: Temporal prerequisites that must be respected
- Resource: Tool availability, API quota limits, concurrent execution limits

**Failure Anticipation:** For each step, identifying what could go wrong and how to handle it. This is not exhaustive enumeration (impossible) but systematic coverage of known failure patterns:
- External failure: Target system unavailable, API rate-limited, network timeout
- Internal failure: Step produces incorrect output, wrong format, missing data
- Environmental failure: Page changed, UI updated, state drifted between steps
- Cascading failure: Step N failure propagates to steps N+1 through N+k

**Multi-Agent Coordination:** When multiple agents participate in a plan, Planning must allocate sub-goals and manage inter-agent dependencies. Key concerns:
- Sub-goal assignment: Which agent handles which step?
- Inter-agent messaging: How do agents communicate progress and failures?
- Conflict resolution: What happens when two agents compete for the same resource?
- Coordination overhead: Communication costs vs. parallelism benefits

### 9. Economics

Planning has significant token and latency costs, particularly for complex dependency graphs. Production data shows:

- Simple sequential plans (3–5 steps): ~500–1,000 tokens, ~2–5 seconds
- Medium dependency graphs (10–20 steps): ~2,000–5,000 tokens, ~5–15 seconds
- Complex multi-agent plans (30+ steps): ~5,000–15,000 tokens, ~15–30 seconds

**Cost optimization strategies:**
- Progressive refinement: Start with a coarse plan, refine only uncertain steps
- Cached plans: Reuse successful plan structures for similar intents
- Plan verification before scheduling: Catch constraint violations before they reach Execution
- Granularity control: Avoid over-decomposition; each step should be meaningful, not minimal

[Primary: ReAct Planning Traces, Yao et al.]
[Engineering: LangGraph Planning Patterns, 2024]

---

## Module B — Operations & Implementations

### 10. Failure Modes

**Decomposition Failures:**
- Over-decomposition: Too many tiny steps → planning overhead dominates execution. Mitigation: enforce minimum step semantic weight.
- Under-decomposition: Steps too large → Scheduler cannot parallelize effectively. Mitigation: require each step to have observable success criteria.
- Circular dependencies: Step A requires B, B requires A → deadlock. Mitigation: topological sort with cycle detection.
- Missing dependencies: Step B starts before A completes → race conditions. Mitigation: explicit prerequisite declaration per step.

**Constraint Violations:**
- Budget overflow: Plan exceeds token or monetary budget. Mitigation: hard budget check before plan output.
- Safety violation: Plan includes forbidden actions. Mitigation: constraint pre-filter before decomposition.
- Resource conflict: Two steps require the same exclusive resource simultaneously. Mitigation: resource reservation in dependency graph.

**Plan Representation Failures:**
- DAG serialization errors: Invalid graph structure (nodes without edges, orphan nodes). Mitigation: graph validation on output.
- Dependency depth limits: Extremely deep chains cause scheduling latency. Mitigation: flatten where possible; flag deep chains for manual review.
- Ambiguous step descriptions: Steps described in natural language without structured fields. Mitigation: enforce structured step format.

### 11. Security Considerations

**Plan-Level Threats:**
- Prompt injection through goal: Malicious goal text causes Planning to generate unsafe steps. Mitigation: sanitize goal input; apply security policy (Node 14) before decomposition.
- Constraint bypass: Adversarial goals designed to slip past constraint checks. Mitigation: defense-in-depth — validate constraints at both Planning and Execution stages.
- Information leakage through plan: Plan reveals sensitive environment state. Mitigation: apply data classification rules to plan output.

**Multi-Agent Planning Threats:**
- Agent impersonation: Malicious agent claims to be a legitimate planner. Mitigation: authenticate agent identities; validate plan signatures.
- Sub-goal hijacking: Attacker redirects an agent's sub-goal to unintended target. Mitigation: verify sub-goal alignment with parent plan at each agent boundary.

[Primary: AI Planning Survey, Ghallab et al.]

### 12. Observability

Planning emits spans for every planning event: step count, dependency depth, constraint count, failure mode count, and planning duration. OpenTelemetry conventions standardize these traces. At production scale, clustering planning failures (e.g., "constraint violation on budget" across thousands of plans) reveals systemic planning weaknesses.

**Key metrics:**
- Plan success rate: % of plans that reach Execution without constraint violation
- Decomposition depth: Average number of plan levels (flat vs. hierarchical)
- Dependency density: Average edges per node in the DAG
- Failure coverage: % of steps with at least one anticipated failure mode

### 13. Production Patterns

**Pattern 1: Sequential Decomposition with Verification Gates**
```
for each step in plan:
    execute(step)
    if not verify(step.success_criteria):
        escalate_to_recovery()
```
Used by: ReAct-based agents, simple single-agent workflows.
Token cost: ~500–1,000 per plan. Reliability: ~70–85% on well-defined tasks.

**Pattern 2: Dependency-Graph Planning with Critical Path Analysis**
```
plan = decompose_goal(intent)
dag = build_dependency_graph(plan.steps)
critical_path = find_longest_path(dag)
failure_modes = anticipate_failures(dag)
output = {steps, dag, critical_path, failure_modes}
```
Used by: LangGraph planner-executor, AutoGen multi-agent planning.
Token cost: ~2,000–5,000 per plan. Reliability: ~85–95% on complex tasks.

**Pattern 3: Multi-Agent Coordination with Sub-Goal Allocation**
```
sub_goals = allocate_sub_goals(intent, agent_capabilities)
for each agent in sub_agents:
    agent_plan = decompose(sub_goal, agent.constraints)
    register_inter_agent_dependencies(agent_plan)
coordination_plan = resolve_conflicts(all_agent_plans)
```
Used by: AutoGen, multi-agent orchestration frameworks.
Token cost: ~5,000–15,000 per plan. Reliability: ~75–90% (depends on coordination overhead).

### 14. Anti-patterns

1. **Implicit planning through raw LLM prompting** — Generating steps via a single LLM call with no structured output format. Produces non-verifiable plans that cannot be scheduled or traced. [Engineering: LangGraph Planning Patterns]

2. **Over-decomposition** — Breaking every action into micro-steps. Planning overhead exceeds execution benefit. A plan with 100 steps for a 5-step task is worse than no plan.

3. **Missing dependency edges** — Assuming parallelism where dependencies exist. Leads to race conditions and silent data corruption. Always explicit > always implicit.

4. **No failure anticipation** — Plans that only cover the happy path are fragile in production. Every critical path step needs at least one failure mode and mitigation.

5. **Planning without constraint validation** — Generating plans that violate budget, safety, or resource constraints. Constraint validation must happen during planning, not during execution.

### 15. Current Implementations

**LangGraph Planning Patterns (2024–Present):** Structured planner-executor loop where a dedicated planning node decomposes goals into sub-tasks with explicit state management. Dominant in production agent frameworks. [Engineering: LangGraph Planning Patterns]

**AutoGen Multi-Agent Planning (2023–Present):** Multi-agent conversation framework where agents negotiate sub-goals through message passing. Supports role-based planning (developer, tester, reviewer agents). [Engineering: AutoGen Multi-Agent Planning]

**ReAct Planning Traces (2022–Present):** Reason-Act pattern where planning interleaves with execution. Each step generates a reasoning trace, executes an action, observes the result, and continues. Simple but effective for linear tasks. [Primary: ReAct Pattern, Yao et al. 2022]

**Tool-Use Planning:** Modern LLMs with function-calling capabilities generate plans as structured JSON with typed tool calls per step. Eliminates natural language ambiguity in step descriptions.

---

## Module C — Research & Future

### 16. Research Landscape

| Paper/Framework | Year | Key Finding |
|---|---|---|
| ReAct (Yao et al.) | 2022 | Interleaved reasoning and action traces improve planning transparency |
| Tree of Thoughts (Yao et al.) | 2023 | Tree-based planning explores multiple decomposition paths before committing |
| LangGraph Planning Patterns | 2024 | Structured planner-executor loop dominates production agent architectures |
| AutoGen Multi-Agent Planning | 2023–2024 | Multi-agent negotiation produces higher-quality plans for complex tasks |
| Plan-and-Solve (Wang et al.) | 2023 | Explicit planning before execution significantly improves LLM task success rates |
| Reflexion (Shinn et al.) | 2023 | Plans that incorporate self-reflection on past failures improve over iterations |

**Standards:** OpenTelemetry GenAI conventions for planning spans (v1.41 draft). No formal planning representation standard exists yet — DAG serialization formats vary by framework.

### 17. Open Questions

1. Can we automate dependency graph validation? Current approaches rely on LLM-generated plans; formal verification would catch structural errors before scheduling.

2. What is the optimal granularity boundary for step decomposition? Empirical data on "too many steps" vs. "too few steps" is scarce.

3. How do we measure plan quality independently of execution success? A plan can be structurally perfect but based on incorrect assumptions about the environment.

4. Can multi-agent planning converge on optimal sub-goal allocation without centralized coordination? Distributed planning algorithms from classical AI may offer solutions.

5. What planning paradigms survive the transition from single-agent to multi-agent systems? Linear decomposition works for one agent but breaks down with ten.

### 18. Future Evolution

**2026–2027:** Formal planning representation standards emerge (OpenTelemetry or W3C). Automated dependency graph validation becomes standard. Planning cost decreases as models produce structured plans more efficiently.

**2027–2029:** Multi-agent planning protocols standardize inter-agent dependency management. Plans become self-verifying — each step includes its own verification criteria and failure recovery instructions.

**2029+:** Planning becomes a specialized sub-model rather than an LLM capability. Dedicated planning models produce provably correct dependency graphs, while general-purpose LLMs handle step refinement and adaptation.

---

## Known Gaps

### Missing Evidence
- Empirical data on optimal step granularity across task complexity levels
- Quantitative comparison of sequential vs. DAG vs. multi-agent planning success rates on production workloads
- Longitudinal data on plan reuse rates (how often similar intents produce identical plans)

### Weak Conclusions
- "Planning quality bounds execution quality" is theoretically sound but lacks production measurement — no benchmark exists for "plan quality" independent of execution
- Token cost estimates for complex multi-agent plans are extrapolated from smaller plans; actual costs may differ significantly
- Failure mode coverage rates are estimated at ~60–80% for structured planning but have not been measured across diverse task domains

### Research Required
- Formal verification methods for dependency graphs produced by LLMs
- Cross-framework benchmark for plan quality (structural correctness, constraint satisfaction, failure coverage)
- Economic analysis of planning overhead vs. execution efficiency gains

### Awaiting Industry Consensus
- Should planning output use a standardized format (JSON Schema for plans, PDDL for constraints, or something new)?
- Who should own plan verification — Planning itself, or a separate Verification node specialized for plans?
- What constitutes a "minimum viable plan" — is there a formal definition of plan correctness?

---

## Sources

### Primary Sources
- [ReAct Pattern, Yao et al. 2022] "ReAct: Synergizing Reasoning and Acting in Language Models" — Interleaved reasoning-action planning traces
- [AI Planning Survey, Ghallab et al.] "Automated Planning: Theory and Practice" — Classical planning foundations, STRIPS, PDDL
- [Tree of Thoughts, Yao et al. 2023] "Tree of Thoughts: Deliberate Problem Solving with Large Language Models" — Tree-based planning exploration

### Engineering Sources
- [LangGraph Planning Patterns] Structured planner-executor loop patterns for production agent frameworks
- [AutoGen Multi-Agent Planning] Multi-agent conversation and sub-goal negotiation patterns

### Benchmark Sources
- [Plan-and-Solve Benchmark, Wang et al. 2023] Explicit planning improves LLM task success rates by ~30% on complex tasks
- [Reflexion Benchmark, Shinn et al. 2023] Self-reflective planning improves over iterations

### Community Sources
- [GitHub Issues] LangGraph, AutoGen — planning failures, dependency resolution issues, multi-agent coordination challenges

---

## Interfaces

### Upstream
- Node 02: Decision Engine (provides refined intent to decompose)
- Node 08: Learning (provides past plan patterns and constraint experiences)
- Node 11: Environment State (provides current conditions for constraint validation)

### Downstream
- Node 04: Scheduling (receives structured plan with steps, dependencies, and constraints)

### Reads
- Refined intent from Decision Engine
- Environment state for constraint validation
- Past experience from Learning node

### Writes
- Structured plan to Scheduling (steps, dependency DAG, constraints, failure modes)
- Working Memory (plan state for session continuity)
- Observability (planning spans)

### Emits
- Structured Plan (steps, dependency DAG, constraints, failure modes)
- Plan Span (step_count, dependency_depth, estimated_cost, planning_duration)

### Consumes
- Refined intent from Node 02: Decision Engine
- Environment state from Node 11
- Past experience from Node 08: Learning
