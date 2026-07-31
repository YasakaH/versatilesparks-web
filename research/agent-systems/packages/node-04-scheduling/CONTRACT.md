node: 04
name: Scheduling

consumes:
  structured_plan:
    description: Decomposed plan with steps, dependencies, and constraints from Planning
    format: plan object with steps, dependency DAG, constraints, failure_modes
    source: Node 03 (Planning)
  resource_availability:
    description: Current resource pool status (compute, API quotas, tool access)
    format: resource state map with availability percentages
    source: Node 11 (Environment State), Node 16 (Runtime)
  execution_history:
    description: Past execution durations and failure rates per step type
    format: structured timing and reliability data
    source: Node 08 (Learning)

produces:
  scheduled_task_list:
    description: Temporally ordered task list with resource assignments and concurrency groups
    includes:
      - ordered_steps: linearized execution order respecting dependencies
      - concurrency_groups: sets of steps that can execute in parallel
      - resource_assignments: which runtime/tools assigned to each step
      - priority_queue: dynamic priority adjustments based on urgency and dependencies
      - deadline_estimates: per-step and cumulative time estimates
    target: Node 05 (Execution)
  schedule_span:
    description: Observability span for every scheduling event
    format: structured telemetry (queue_depth, concurrency_level, estimated_duration)
    emits_to: Node 12 (Observability)

guarantees:
  - dependency_ordering: No step executes before its prerequisites complete
  - deadlock_prevention: Circular dependency detection prevents infinite wait states
  - resource_bounds: No step exceeds declared resource constraints from Planning
  - priority_integrity: Higher-priority urgent steps preempt lower-priority work within dependency bounds

does_not_guarantee:
  - plan_correctness: Scheduling orders what Planning produces; correctness is Planning's responsibility
    responsibility: Node 03 validates step decomposition and dependency graph
  - execution_success: Scheduling provides order; Execution (Node 05) performs the work
    responsibility: Verification (Node 06) judges whether execution met success criteria
  - optimal_throughput: Scheduling uses heuristic methods; global optimality is NP-hard
    responsibility: Trade-off between solution quality and scheduling latency is accepted
  - failure_recovery: Scheduling detects failures but does not diagnose or repair them
    responsibility: Recovery (Node 07) handles root cause analysis and path switching

side_effects:
  - writes_working_memory: Stores schedule state for session continuity
    scope: Session-scoped only (see Node 09)
  - emits_schedule_span: Creates an observability span for every scheduling event
    scope: Tracked in Observability node (Node 12)
  - reads_planning_node: Consumes plan structure and constraints from Node 03
    scope: Node 03 (Planning)

timing:
  min_latency_per_schedule: "~1s for linear plans with no concurrency"
  max_latency_per_schedule: "~10s for complex DAGs with resource contention resolution"
  throughput_constraint: Bounded by dependency graph size and resource pool query latency
  ordering: Schedules are produced sequentially per plan; concurrent plans compete for resources
