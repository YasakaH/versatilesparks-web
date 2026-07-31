# Node 04: Scheduling — Reference Document

> **Status:** Wave 1 Draft
> **Package Version:** 0.1.0
> **Canon Version:** 1.0
> **Specification Version:** 2.0
> **Last Updated:** 2026-07-22

---

## 1. Scope Boundaries

### In Scope
- Temporal ordering of plan steps respecting dependency constraints
- Resource allocation and contention resolution (compute, API quotas, tool access)
- Concurrency control (parallel execution where dependencies allow)
- Priority scheduling based on urgency, deadlines, and critical path position
- Deadlock prevention and cycle detection in dynamic schedules
- Queue management for pending, active, and completed steps
- Dynamic rescheduling in response to execution failures or resource changes
- Resource bounds enforcement (no step exceeds declared constraints from Planning)

### Out of Scope
- Goal decomposition into steps (Node 03: Planning) — Scheduling orders what Planning decomposes; it does not create steps
- Intent formation and model routing (Node 02: Decision Engine) — Scheduling receives structured plans; Decision Engine forms intent
- Action execution on surfaces (Node 05: Execution) — Scheduling produces ordered task lists; Execution performs actions
- Outcome verification (Node 06: Verification) — Scheduling tracks completion status; Verification judges outcome quality
- Failure diagnosis and recovery (Node 07: Recovery) — Scheduling detects failures but does not diagnose root causes; Recovery repairs them
- Learning from scheduling outcomes (Node 08: Learning) — Scheduling uses historical data; Learning extracts patterns from outcomes
- Session memory management (Node 09: Working Memory) — Scheduling stores schedule state; Memory manages retention
- Persistent knowledge storage (Node 10: Long-term Memory) — Scheduling references learned timing data; Memory persists it
- Environment state tracking (Node 11: Environment State) — Scheduling reads resource availability; Environment State maintains it
- Observability and tracing (Node 12: Observability) — Scheduling emits spans; Observability aggregates them
- Token economics and inference cost modeling (Node 13: Economics) — Scheduling respects budget constraints; Economics models costs
- Security policy enforcement (Node 14: Security) — Scheduling respects security constraints from Planning; Security defines policies
- Governance and compliance checking (Node 15: Governance) — Scheduling respects compliance requirements from Planning; Governance defines them
- Runtime and compute environment (Node 16: Runtime) — Scheduling assigns resources; Runtime provisions them
- Execution surface specifics (Nodes 17–22) — Scheduling is surface-agnostic; surfaces provide capability metadata

---

## 2. Executive Summary

Scheduling is the temporal engine of the agent system. It answers "When should each step happen, in what order, and with which resources?" — transforming Planning's dependency graph into an executable timeline.

The critical architectural insight is that scheduling is fundamentally a **resource-constrained project scheduling problem** — a well-studied class in operations research that is NP-hard in its general form. Agent scheduling inherits this complexity but adds layers unique to AI agents: volatile resource availability (API rate limits change dynamically), non-deterministic step durations (LLM calls vary in latency), and dynamic priorities (a failed step may elevate downstream urgency).

Three scheduling paradigms coexist in production today: **queue-based scheduling** (FIFO or priority queues for linear plans), **dependency-ordered scheduling** (topological sort with parallelism where DAG allows), and **resource-aware scheduling** (optimizing for available compute, API quotas, and concurrent tool access). Which paradigm applies depends on plan structure and resource constraints.

Production systems increasingly use distributed task schedulers (Ray, Temporal, Celery) rather than in-process schedulers because agent plans require reliable queuing, retry semantics, and state persistence that custom implementations cannot guarantee at scale. The scheduler is not just an ordering function — it is the system's reliability layer.

---

## 3. Canon Definition

> **Canon Node 04: Scheduling**
> The process of temporally ordering plan steps, allocating resources, and managing concurrency to produce an executable task sequence.

**Purpose:** To transform Planning's structured plan into a temporally ordered, resource-allocated task list that Execution can perform reliably.

**Inputs:** Structured plan from Planning (Node 03); resource availability map from Environment State (Node 11) and Runtime (Node 16); execution history from Learning (Node 08).
**Outputs:** Scheduled task list with ordered steps, concurrency groups, and resource assignments → Execution (Node 05).
**Dependencies:** Planning (plan to order), Environment State (resource status), Runtime (provisioning), Learning (historical timing data).
**Feeds:** Execution (ordered task list), Observability (scheduling spans).

See also: Node 03: Planning, Node 05: Execution, Node 08: Learning, Node 11: Environment State, Node 16: Runtime.

---

## 4. Mental Model

### The Scheduling Pipeline

```
Structured Plan from Planning
         │
         ▼
Dependency Linearization ── Topological sort of DAG → executable order
         │
         ▼
Resource Mapping ── Match each step to available runtime/tools/surfaces
         │
         ▼
Concurrency Analysis ── Identify parallelizable step groups (independent nodes in DAG)
         │
         ▼
Priority Assignment ── Critical path steps = highest priority; blockers = urgent
         │
         ▼
Queue Construction ── Build initial execution queue with priority levels
         │
         ▼
Deadlock Check ── Detect circular wait conditions before schedule activation
         │
         ▼
Scheduled Task List Output
  ├─ Ordered steps (linearized execution order)
  ├─ Concurrency groups (parallelizable step sets)
  ├─ Resource assignments (runtime/tools per step)
  ├─ Priority queue (dynamic priority adjustments)
  └─ Deadline estimates (per-step and cumulative time estimates)
         │
         ▼
Execution (Node 05) ← Receives scheduled tasks for execution
```

### Three Primary Scheduling Paradigms

| Paradigm | Complexity | Parallelism | Best For |
|---|---|---|---|
| Queue-Based (FIFO/Priority) | Low | None | Linear plans, simple single-agent workflows |
| Dependency-Ordered (Topological) | Medium | DAG-parallel (independent branches) | Multi-step tasks with partial parallelism |
| Resource-Aware (Optimizing) | High | Full (resource-optimized) | Complex multi-agent plans with resource contention |

**Key insight:** These paradigms compose hierarchically. Production schedulers often use queue-based ordering within dependency-ordered phases, applying resource-aware optimization only at contention points. A pure topological sort is correct but suboptimal; a full optimizer is optimal but slow. The scheduler balances correctness against scheduling latency.

---

## 5. Design Invariants

These are timeless truths about Scheduling that survive tool changes, model shifts, and architecture evolution. If an assertion fails any test below, it belongs in Modules B or C, not here.

**Test criteria:**
1. True if all today's tools disappear? (Not a pattern/implementation detail)
2. Still true in 10 years as architectures evolve? (Not a trend)
3. Fundamental to this node's role in the system? (Not a supporting observation)

| # | Invariant | Rationale |
|---|---|---|
| 1 | **Dependency ordering is a hard constraint; everything else is soft.** | You cannot execute step B before step A if B depends on A. No amount of optimization, priority, or resource availability overrides this. Everything else (parallelism, resource assignment, priority reordering) is optional; dependency order is mandatory. |
| 2 | **Global optimality is unattainable in bounded time.** | The resource-constrained project scheduling problem is NP-hard. Any scheduler claiming optimal throughput is either approximating or running forever. Good schedulers are explicitly approximate — they find "good enough" solutions within latency budgets. |
| 3 | **Scheduling latency compounds across layers.** | Each scheduling decision adds delay. Deep dependency chains magnify this: a 1-second scheduling overhead per level creates 5 seconds of overhead in a 5-level plan. The scheduler must be faster than the steps it schedules. |
| 4 | **Dynamic scheduling is mandatory, not optional.** | LLM call latencies are non-deterministic. API rate limits fluctuate. Network conditions change. A static schedule (created once and executed) is inherently fragile. Schedulers must adapt to runtime conditions continuously. |
| 5 | **Resource contention creates implicit dependencies.** | Two independent steps that require the same exclusive resource cannot execute in parallel. The scheduler transforms this physical constraint into a temporary dependency edge, even though the plan's DAG showed no relationship. |
| 6 | **Deadlock is the default risk of concurrency.** | Circular wait (A waits for B's resource, B waits for A's resource) is structurally possible whenever shared resources and parallel execution coexist. Prevention is mandatory — hope is not a strategy. |
| 7 | **Schedule fidelity degrades over time.** | A schedule created at T=0 is less accurate at T=300 as conditions change. The longer the gap between scheduling and execution, the more rescheduling is needed. Schedulers are temporal artifacts — their accuracy decays. |

---

## Module A — Theory & Architecture

### 6. Historical Evolution

**Gantt Chart Era (1910s–1980s):** Industrial scheduling relied on manual Gantt charts and critical path method (CPM). These were deterministic models where task durations were fixed and resources were abundant. They worked for factory floors but could not handle the volatility of modern computing environments. [Primary: CPM/PERT Literature]

**Operating System Scheduling (1980s–2000s):** CPU schedulers (round-robin, priority-based, deadline-based) and distributed task schedulers (Apache Mesos, Kubernetes Scheduler) brought algorithmic rigor to resource allocation. These systems solved similar problems but at different scales and under different assumptions (deterministic tasks vs. probabilistic agent steps). [Primary: OS Scheduling Textbook]

**Workflow Engine Era (2000s–2010s):** Airflow, Luigi, and Apache Spark introduced declarative DAG-based scheduling for data pipelines. Steps were defined as nodes with explicit dependencies. These engines proved that DAG scheduling is a solved problem when task durations are predictable — precisely the assumption that breaks down for agent steps. [Engineering: Airflow Documentation]

**Agent Scheduling Emergence (2023–Present):** As LLM-based agents entered production, scheduling requirements diverged from traditional workflow engines. Key differences: non-deterministic task durations (LLM calls vary wildly), volatile resource availability (API rate limits change mid-plan), dynamic priorities (failed steps elevate urgency), and the need for sub-minute scheduling latency (agent loops move too fast for batch-oriented schedulers). Distributed task frameworks like Ray and Temporal are being adapted for agent workloads. [Engineering: Ray Task Scheduling]

### 7. Architecture Overview

Scheduling sits between Planning and Execution in the agent loop. It receives a structured plan and produces a scheduled task list. The architecture has five layers:

1. **Linearization Layer:** Converts the dependency DAG into a topologically sorted linear order. This is the correctness foundation — every node in the resulting list appears after all its prerequisites.

2. **Concurrency Layer:** Identifies independent nodes in the DAG and groups them into parallel execution batches. Parallelism is the primary throughput lever; the scheduler's quality is measured by how much parallel work it enables without violating dependencies.

3. **Resource Layer:** Maps each step to available runtime resources (containers, processes, tools, surfaces). Resolves conflicts when multiple steps compete for the same resource.

4. **Priority Layer:** Assigns and dynamically adjusts priorities based on: critical path proximity (steps on the longest dependency chain get higher priority), blockage detection (steps whose dependents are waiting get elevated priority), and urgency signals from external sources.

5. **Adaptation Layer:** Monitors execution and adjusts the schedule in response to: step completions (enabling dependent steps), step failures (triggering rescheduling), resource changes (API rate limit updates, tool crashes), and dynamic priority shifts.

### 8. Core Components

**Topological Sort:** The mathematical foundation of dependency-ordered scheduling. A topological sort produces a linear ordering of DAG nodes such that for every directed edge U→V, U appears before V in the ordering. If the graph contains cycles, topological sort fails — indicating a deadlock condition. Kahn's algorithm and DFS-based algorithms are the two standard approaches; Kahn's is preferred for its explicit cycle detection.

**Critical Path Method (CPM):** Identifies the longest dependency chain in the DAG, determining the minimum total duration of the plan. Steps on the critical path receive highest scheduling priority because any delay on these steps directly delays the entire plan. Non-critical steps have "slack" (time they can be delayed without affecting the plan finish time).

**Resource Allocator:** Maps plan steps to available compute resources. Each step declares its resource requirements (CPU cores, memory, tool access, surface type); the allocator finds matching available resources. When resources are scarce, the allocator makes trade-off decisions: which steps get resources first, which get deferred, and which get migrated to slower resources.

**Concurrency Manager:** Groups independent steps into parallel execution batches. At each scheduling point, the manager identifies all steps whose dependencies are satisfied and whose required resources are available — these form the current batch. The number of steps in a batch is constrained by available parallelism (CPU cores, concurrent API connections, etc.).

**Priority Queue Manager:** Maintains a dynamically re-prioritized queue of pending steps. Standard priority metrics:
- Base priority: assigned during initial scheduling (critical path steps = P1, others = P2–P5)
- Dynamic priority: adjusted at runtime based on blocking status, failure proximity, and urgency signals
- Preemption rules: P1 steps can interrupt P3+ steps, but never P1 or P2 steps (to prevent priority inversion)

**Deadlock Detector:** Continuously monitors for circular wait conditions. Two types:
- Static deadlock: detected during initial scheduling (cycles in the plan DAG) — fatal error, requires plan revision
- Dynamic deadlock: detected during execution (resource circular wait between parallel batches) — triggers rollback and reschedule

**Rescheduler:** Triggers when conditions change significantly: step failures, resource outages, priority escalations, or deadlines approaching. Incremental rescheduling modifies only affected portions of the schedule rather than recomputing from scratch.

### 9. Economics

Scheduling has relatively low token cost (it operates on structured data, not natural language) but significant compute and latency costs:

- Simple linear plans: ~10–50ms scheduling latency, ~100–500 tokens processed
- Medium dependency graphs: ~50–200ms, ~500–2,000 tokens
- Complex resource-aware schedules: ~200–1,000ms, ~2,000–10,000 tokens

**Cost optimization strategies:**
- Lazy evaluation: Only compute scheduling decisions for steps that are about to execute, not for the entire plan upfront
- Incremental rescheduling: Modify existing schedule rather than recomputing when conditions change
- Caching: Reuse successful schedule structures for recurring plan patterns
- Approximation: Use heuristic schedulers (greedy, genetic algorithms) instead of exact solvers for large DAGs

[Engineering: Ray Task Scheduling]
[Engineering: Temporal Workflow Engine]

---

## Module B — Operations & Implementations

### 10. Failure Modes

**Scheduling Failures:**
- Topological sort failure: Cycle detected in plan DAG. Cause: Planning produced a non-DAG dependency graph. Mitigation: reject plan; return to Planning for correction.
- Resource starvation: Steps wait indefinitely for unavailable resources. Cause: Limited resource pool combined with poor allocation strategy. Mitigation: implement resource preemption for high-priority steps.
- Priority inversion: Lower-priority step executes before higher-priority step despite dependency satisfaction. Cause: Race condition in concurrent priority queue updates. Mitigation: lock-free priority queue or centralized priority arbiter.

**Concurrency Failures:**
- Race conditions: Two parallel steps write to the same shared resource without coordination. Cause: Missing implicit dependency on shared resource. Mitigation: resource allocator treats shared resources as mutual exclusion locks.
- Deadlock: Circular wait between parallel steps competing for exclusive resources. Cause: Resource contention not modeled in plan DAG. Mitigation: deadlock detector + resource request ordering protocol.
- Starvation: A step is perpetually deferred in favor of higher-priority steps. Cause: Unbounded priority queue with no aging mechanism. Mitigation: implement priority aging (each wait second increments priority).

**Dynamic Scheduling Failures:**
- Stale schedule: Schedule created for old resource state is applied to new state. Cause: Race between schedule creation and resource availability check. Mitigation: validate resource state at execution time, not scheduling time.
- Cascading rescheduling: One failure triggers a chain of rescheduling events. Cause: Tight coupling between steps means one failure affects many dependents. Mitigation: localize rescheduling scope; only reschedule affected subgraph.

### 11. Security Considerations

**Scheduling-Specific Threats:**
- Priority manipulation: Malicious step elevates its own priority to consume disproportionate resources. Mitigation: validate priority assignments against declared step urgency.
- Resource hoarding: Compromised agent claims excessive resources for benign steps. Mitigation: enforce resource quotas per agent; implement fair-sharing algorithms.
- Schedule injection: Attacker injects malicious steps into the schedule queue. Mitigation: authenticate all queue mutations; validate step provenance against original plan.

[Primary: OS Scheduling Textbook]

### 12. Observability

Scheduling emits spans for every scheduling event: queue depth, concurrency level, scheduling latency, resource utilization, and priority distribution. OpenTelemetry conventions standardize these traces. At production scale, clustering scheduling failures (e.g., "deadlock on resource pool X" across thousands of runs) reveals systemic resource configuration problems.

**Key metrics:**
- Schedule correctness: % of executions where no dependency was violated
- Parallelism efficiency: Ratio of actual parallel steps to maximum possible parallel steps
- Scheduling overhead: % of total plan duration spent in scheduling vs. execution
- Resource utilization: Average percentage of available resources actively used
- Rescheduling frequency: Number of dynamic reschedules per plan (lower is better for stability)

### 13. Production Patterns

**Pattern 1: Topological Sort with Parallel Batching**
```
sorted_steps = topological_sort(plan.dag)
batch = []
for step in sorted_steps:
    if step.dependencies_satisfied():
        batch.append(step)
        if len(batch) == max_parallelism:
            execute_batch(batch)
            batch = []
execute_batch(batch)  # Remaining steps
```
Used by: Ray, Temporal, most DAG schedulers.
Scheduling latency: ~50–200ms. Reliability: ~99%+ (correct by construction).

**Pattern 2: Priority Queue with Dynamic Rescheduling**
```
queue = PriorityQueue()
queue.push_all(ready_steps, priority=critical_path_distance)
while queue not empty:
    step = queue.pop_highest_priority()
    result = execute(step)
    if success:
        queue.add_ready_step_dependents(step)
    elif failure and retryable:
        queue.requeue_with_backoff(step)
    else:
        escalate_to_recovery(step)
```
Used by: Agent frameworks with adaptive scheduling (custom implementations).
Scheduling latency: ~20–100ms. Reliability: ~95–98% (depends on retry logic quality).

**Pattern 3: Distributed Task Scheduling**
```
scheduler = Ray/Scheduler(cluster_resources)
job = scheduler.submit(dag_plan, resource_requirements)
handles = []
for batch in job.parallel_batches():
    handles.extend(scheduler.execute_in_parallel(batch))
results = scheduler.wait_for_all(handles)
job.complete(results)
```
Used by: Large-scale agent deployments requiring fault tolerance and cluster scaling.
Scheduling latency: ~100–500ms (cluster communication overhead). Reliability: ~99.9%+ (distributed fault tolerance).

### 14. Anti-patterns

1. **Linear scheduling for parallel-capable plans** — Executing DAG steps sequentially when independent branches exist wastes 30–70% of available parallelism. Every independent pair of steps should be batched. [Engineering: Ray Performance Benchmarks]

2. **Scheduling without resource validation** — Creating a schedule based on assumed resource availability that no longer exists. Resources must be validated at execution time, not scheduling time.

3. **Static schedules for volatile environments** — Creating a schedule once and executing it unchanged, even when API rate limits or network conditions change mid-plan. Dynamic rescheduling is mandatory for production systems.

4. **No deadlock prevention** — Assuming "it won't happen" rather than implementing circular wait detection. Deadlocks are a statistical certainty in concurrent systems with shared resources.

5. **Scheduling latency exceeding step latency** — When scheduling takes longer than individual steps, the scheduler becomes the bottleneck. This typically happens with overly complex resource-aware optimization on small plans. Simplify when N < 20 steps.

### 15. Current Implementations

**Ray Task Scheduling (2021–Present):** Distributed task scheduler optimized for Python workloads. Supports DAG-based task dependency, dynamic task generation, and fault-tolerant execution. Used extensively in ML training pipelines and increasingly in agent orchestration. [Engineering: Ray Task Scheduling]

**Temporal Workflow Engine (2019–Present):** Distributed workflow orchestration with guaranteed execution, automatic retries, and event-driven scheduling. Provides exactly-once execution semantics and durable state management. Adoption growing in agent systems requiring reliability guarantees. [Engineering: Temporal Documentation]

**Airflow DAG Execution (2014–Present):** Traditional data pipeline scheduler adapted for agent workflows. Handles dependency ordering and resource allocation but lacks sub-minute scheduling latency required for real-time agent loops. Used primarily for batch-oriented agent tasks. [Engineering: Airflow Architecture]

**Celery Task Queue (2009–Present):** Python distributed task queue with priority support and worker pools. Simple to configure, widely deployed. Lacks built-in DAG scheduling — requires manual dependency declaration. Suitable for simpler agent scheduling needs.

**Custom Agent Schedulers:** Many production agent frameworks implement bespoke schedulers tailored to their specific architecture patterns (LangGraph's built-in scheduler, custom Ray wrappers, etc.). No single industry-standard scheduler dominates agent workloads yet.

---

## Module C — Research & Future

### 16. Research Landscape

| Framework/System | Year | Key Finding |
|---|---|---|
| Ray Task Scheduling (Rai et al.) | 2018–Present | Distributed DAG scheduling achieves sub-millisecond task submission latency |
| Temporal Workflow Engine | 2019–Present | Durable workflow scheduling enables reliable long-running agent plans |
| Airflow DAG Scheduler | 2014–Present | Declarative DAG scheduling is mature for batch workloads; unsuitable for sub-minute agent loops |
| Kubernetes Scheduler | 2015–Present | Cluster-level resource scheduling scales to thousands of nodes; overkill for agent workloads |
| AgentFlow (Li et al.) | 2024 | Multi-agent scheduling optimized for LLM latency variance using predictive queuing |

**Standards:** OpenTelemetry GenAI conventions for scheduling spans (v1.41 draft). No formal agent scheduling API standard exists yet.

### 17. Open Questions

1. How do we schedule LLM-based steps when their duration distributions are heavily right-skewed (most calls fast, some take 30+ seconds)? Standard deviation-based planning massively overestimates average duration.

2. What scheduling algorithms best handle the combination of deterministic dependencies and stochastic execution times? Classical CPM assumes fixed durations; PERT assumes known distributions. Neither fits LLM variance well.

3. Can we achieve deterministic ordering guarantees (needed for reproducibility) while maintaining the flexibility of dynamic scheduling? These goals are in tension — deterministic scheduling is static; dynamic scheduling adapts.

4. How should multi-agent schedulers handle inter-agent communication latency? Current models assume near-zero communication cost between agents on the same cluster; cloud-distributed agents add 50–200ms per hop.

5. What are the scheduling implications of using smaller, faster models for simple steps vs. larger, slower models for complex steps? Heterogeneous model scheduling introduces a new dimension to the resource allocation problem.

### 18. Future Evolution

**2026–2027:** Specialized agent schedulers emerge that natively model LLM latency distributions. Predictive scheduling uses historical timing data to adjust schedules in real-time. Standardized agent scheduling APIs begin to appear.

**2027–2029:** Multi-agent schedulers optimize globally across agent boundaries, treating distributed agents as a single resource pool with explicit communication cost models. Automated deadlock prevention becomes standard.

**2029+:** Scheduling becomes adaptive and self-optimizing — schedulers learn their system's behavior patterns and proactively adjust to predicted load changes. The boundary between planning and scheduling blurs as planners generate schedules-as-they-go rather than plans-as-static-artifacts.

---

## Known Gaps

### Missing Evidence
- Empirical benchmarks comparing topological sort, priority queue, and resource-aware scheduling for agent workloads
- Quantitative analysis of scheduling latency vs. plan complexity across diverse production workloads
- Data on rescheduling frequency in real production agent systems (how often do schedules need dynamic adjustment?)

### Weak Conclusions
- "Scheduling latency should be sub-step-latency" is a design principle without measured thresholds — what is actually acceptable varies by plan length and urgency
- "Resource-aware scheduling provides diminishing returns for plans with <20 steps" is inferred from classical OR literature but not validated on agent-specific workloads
- Parallelism efficiency estimates (~30–70% waste from sequential execution of parallelizable plans) are extrapolated from DAG structures; actual gains depend on step types (I/O-bound vs. CPU-bound)

### Research Required
- Benchmark suite for agent scheduling algorithms (analogous to MLPerf for ML workloads)
- Latency distribution modeling for LLM step execution across different model sizes and contexts
- Cross-framework comparison of scheduling correctness guarantees (exactly-once, at-least-once, best-effort)

### Awaiting Industry Consensus
- Should there be a standardized agent scheduling API (like CRON for time-based tasks, but DAG-aware)?
- Who defines scheduling correctness — the framework authors, the planning layer, or the verification layer?
- What is the standard unit for measuring scheduling quality (makespan reduction, resource utilization, deadline adherence)?

---

## Sources

### Primary Sources
- [Ray Task Scheduling, Rai et al. 2018] "Ray: A Distributed Framework for Emerging AI Applications" — Distributed task scheduling with DAG support
- [CTE Textbook, Cormen et al.] "Introduction to Algorithms" — Topological sort, critical path method, and scheduling theory foundations
- [OS Scheduling Textbook, Tanenbaum] "Modern Operating Systems" — Process scheduling algorithms, priority inversion, deadlock prevention

### Engineering Sources
- [Ray Documentation] Ray task scheduling patterns, parallelism controls, and fault tolerance
- [Temporal Documentation] Durable workflow scheduling with exactly-once execution semantics
- [Airflow Architecture] DAG-based scheduling for batch-oriented workflows
- [Ray Performance Benchmarks] Parallelism efficiency measurements across different DAG structures

### Benchmark Sources
- [MLPerf Scheduling Benchmarks] Compute scheduler performance baselines (adapted for agent workload modeling)
- [AgentFlow Evaluation, Li et al. 2024] Multi-agent scheduling optimization for LLM latency variance

### Community Sources
- [GitHub Issues] Ray, Temporal, Airflow — scheduling failures, deadlock cases, resource contention issues
- [Reddit r/MachineLearning] Agent scheduling discussions and production experience sharing

---

## Interfaces

### Upstream
- Node 03: Planning (provides structured plan with steps, dependencies, and constraints)
- Node 08: Learning (provides historical execution timing data for priority adjustment)
- Node 11: Environment State (provides current resource availability)
- Node 16: Runtime (provisions compute resources as requested by scheduler)

### Downstream
- Node 05: Execution (receives scheduled task list with ordered steps and resource assignments)

### Reads
- Structured plan from Planning (steps, DAG, constraints)
- Resource availability from Environment State and Runtime
- Historical timing data from Learning node

### Writes
- Scheduled task list to Execution (ordered steps, concurrency groups, resource assignments, priorities)
- Working Memory (schedule state for session continuity)
- Observability (scheduling spans)

### Emits
- Scheduled Task List (ordered steps, concurrency groups, resource assignments, priority queue, deadline estimates)
- Schedule Span (queue_depth, concurrency_level, estimated_duration, scheduling_latency)

### Consumes
- Structured plan from Node 03: Planning
- Resource availability from Node 11: Environment State
- Historical data from Node 08: Learning
- Compute provisioning from Node 16: Runtime
