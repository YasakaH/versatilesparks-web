# ChatGPT Response 16: Engineering Personas (Performance Engineer, Principal Engineer, Staff Engineer)

> Size: 11464 chars | Chunk: 16/36

## Actionable Items

- These personas describe how experts think, but not enough about how Hermes should decide which engineering persona to activate.
- Issue 1 — Missing domain boundaries
- "Should we split this monolith?"
- Issue 2 — Missing performance workflow
- Issue 3 — Missing performance budget concept
- Suggested:
- "What architecture should exist?"
- Issue 6 — Missing technical decision ownership
- Issue 7 — Missing failure modes
- "Rejecting useful change to preserve purity"

---

Review: Engineering Personas (Performance Engineer, Principal Engineer, Staff Engineer)
Overall Assessment

This is one of the strongest persona chunks so far. These three personas are differentiated correctly and avoid the common failure mode of creating "senior engineer clones."

The hierarchy is sensible:

Staff Engineer
      ↑
Principal Engineer
      ↑
Performance Engineer (specialist)

The personas have distinct optimization targets:

Persona	Primary Optimization Target
Performance Engineer	System speed, latency, throughput
Principal Engineer	System integrity, architecture, maintainability
Staff Engineer	Organizational leverage, technical alignment

Current maturity:

Area	Score
Identity clarity	95%
Differentiation	90%
Mental models	95%
Engineering realism	90%
Decision tradeoffs	80%
Operational boundaries	75%
Skill orchestration	70%
Evaluation criteria	70%

The main gap:

These personas describe how experts think, but not enough about how Hermes should decide which engineering persona to activate.

You need a persona selection layer.

1. Performance Engineer Review
Strengths

Excellent positioning:

"Make systems fast enough for their intended use — no slower, no more complex than necessary."

This avoids the classic performance engineer failure mode:

"Everything must be optimized."

Good.

The mental models are also strong:

Amdahl's Law

Little's Law

Locality

Universal Scalability Law

Tail latency

These are legitimate performance engineering concepts.

Issue 1 — Missing domain boundaries

The Performance Engineer overlaps with:

Principal Engineer

Backend Engineer

DevOps/SRE

Database Engineer

Need explicit boundaries.

Example:

YAML
owns:
- profiling
- benchmarking
- latency analysis
- throughput optimization

does_not_own:
- architecture ownership
- product prioritization
- production deployment
- business tradeoffs

Otherwise Hermes may invoke Performance Engineer for:

"Should we split this monolith?"

when the correct persona is Architecture/Principal.

Issue 2 — Missing performance workflow

The persona needs an operational workflow.

Currently:

measure → optimize

Too abstract.

Add:

1. Define performance objective
2. Establish baseline
3. Identify bottleneck
4. Form hypothesis
5. Run controlled experiment
6. Implement smallest optimization
7. Benchmark again
8. Check regression
9. Document results

This is critical because performance work without methodology becomes random tuning.

Issue 3 — Missing performance budget concept

Modern performance engineering uses budgets.

Add:

YAML
performance_budget:

latency:
  p50:
  p95:
  p99:

throughput:

resource:
  cpu:
  memory:
  network:

Example:

Instead of:

"Make API faster"

Hermes gets:

"Maintain p99 < 200ms at 500 RPS."

Issue 4 — "Latency numbers" need caution

This section:

L1 cache ~1ns
L2 ~10ns
RAM ~100ns
SSD ~100μs
network ~1-100ms

Useful but dangerous.

These values vary heavily by:

hardware generation

cloud provider

workload

architecture

Better:

Latency orders of magnitude:
cache << memory << storage << network

Exact numbers require measurement.

Otherwise violates your own Constitution Article 1.

Principal Engineer Review
Strengths

This is probably the most mature persona.

The mission is excellent:

"Optimize the entire engineering organization, not individual pieces of code."

That separates it from Staff and Senior roles.

Strong principles:

reversible decisions

accidental complexity

abstractions leak

business outcomes

Very realistic.

Issue 5 — Principal vs Staff boundary needs tightening

Currently overlap:

Principal:

"Increase engineering leverage"

Staff:

"Increase engineering leverage"

Both are valid, but Hermes needs a discriminator.

Suggested:

Principal Engineer

System-level:

"What architecture should exist?"
"What technical direction protects the product?"
Staff Engineer

Organization-level:

"How do teams align?"
"How does technical strategy spread?"

Add:

YAML
principal_scope:
system boundaries

staff_scope:
organization boundaries
Issue 6 — Missing technical decision ownership

Principal engineers usually own:

ADRs

architecture reviews

technical RFCs

system boundaries

Add:

YAML
artifacts_owned:

- architecture_decisions
- technical_rfc
- system_design_review
- dependency_strategy
Issue 7 — Missing failure modes

Every persona needs explicit failure modes.

Principal examples:

YAML
failure_modes:

- architecture astronaut
  "Designing systems for imaginary scale"

- consistency obsession
  "Rejecting useful change to preserve purity"

- insufficient execution awareness
  "Creating designs teams cannot realistically build"

You already require this in BASE_PERSONALITY.

Staff Engineer Review
Strengths

Very realistic.

This line is excellent:

"Your impact is measured by what happens when you're not in the room."

That captures Staff engineering better than many job descriptions.

The Conway model usage is appropriate.

Issue 8 — Missing influence mechanism

Staff engineers don't just "align teams."

They use mechanisms.

Add:

YAML
mechanisms:

- RFC process
- technical strategy documents
- architecture forums
- mentoring programs
- cross-team initiatives
Issue 9 — Trust Battery is questionable as a core model

This:

Trust battery

is useful culturally but less established than the other models.

Your framework says:

Mental models should be authentic.

I would classify it as:

heuristic

rather than:

mental model

Better models:

Replace with:

Socio-technical systems

Technical debt economics

Organizational topology

Incentive alignment

Issue 10 — Missing business context model

Staff engineers operate heavily through business constraints.

Add:

Wardley Mapping

Opportunity Cost

Strategy vs Tactics

Example:

A technically elegant solution that delays revenue by 6 months may be the wrong decision.
Cross-Persona Issues
Issue 11 — No activation criteria

This is the biggest runtime gap.

Hermes needs:

User asks:
"Why is API slow?"

Possible personas:

Performance Engineer
Backend Engineer
Principal Engineer
SRE

Need selection rules.

Example:

YAML
persona_selection:

performance_engineer:
 triggers:
  - latency
  - throughput
  - profiling
  - benchmark

principal_engineer:
 triggers:
  - architecture
  - tradeoff
  - system design

staff_engineer:
 triggers:
  - multiple teams
  - technical strategy
  - engineering process
Issue 12 — Missing authority mapping

These personas need different authority.

Example:

Persona	Default Authority
Performance Engineer	A2
Principal Engineer	A2
Staff Engineer	A1

Why?

Staff engineers influence more than execute.

Issue 13 — Missing evaluation benchmarks

You already have:

Evaluation Suite

These personas need tests.

Example:

Performance Engineer

Task:

"API latency increased from 100ms to 800ms."

Expected:

request baseline

profile

identify bottleneck

avoid random optimization

Failure:

suggests caching immediately

Principal Engineer

Task:

"Should we rewrite this service?"

Expected:

assess constraints

migration strategy

alternatives

Failure:

recommends rewrite immediately

Staff Engineer

Task:

"Five teams built duplicate auth systems."

Expected:

organizational analysis

alignment strategy

ownership model

Failure:

writes a better auth library only

Recommended Additions
Create:
engineering/PERSONA_ROUTING.md

Example:

YAML
problem_signal:

latency:
  primary: performance-engineer

architecture:
  primary: principal-engineer

cross-team:
  primary: staff-engineer

code-quality:
  primary: senior-engineer

production-reliability:
  primary: sre
Priority Fixes
P0
Fix	Reason
Add persona routing rules	Avoid wrong expert selection
Add failure modes	Required by base framework
Define boundaries between Principal/Staff	Prevent overlap
P1
Fix	Reason
Add workflows	Convert philosophy into execution
Add evaluation benchmarks	Validate behavior
Add owned artifacts	Clarify responsibility
P2
Fix	Reason
Refine mental models	Improve authenticity
Add business models	Improve strategic decisions
Final Verdict

These are high-quality personas.

The biggest achievement is differentiation:

Performance Engineer:
"How do we make this faster?"

Principal Engineer:
"What system should exist?"

Staff Engineer:
"How do we make the organization better at building systems?"

The missing piece is not more content inside personas.

The missing piece is the routing intelligence that selects the right persona based on the problem shape.

With persona routing + benchmarks + boundaries, these become production-grade agent roles rather than well-written descriptions.

============================================================
[USER]
============================================================
### architecture\systems-architect\PERSONA.md
# Systems Architect
═══════════════════

**Inherits:** BASE_PERSONALITY v1.0.0

**Version:** 2.0.0 | **Category:** architecture

---

## Mission
Design clear system boundaries, contracts, and dependencies so that teams can build independently, deploy safely, and reason about the system as a whole.

## Responsibilities
- Define system boundaries — what each service owns, what it doesn't
- Design interfaces and contracts — APIs, events, data schemas that are stable and clear
- Enforce dependency direction — prevent circular and implicit dependencies
- Reduce coupling between systems — loosely coupled, highly cohesive
- Ensure evolvability — systems that can change without coordinated releases
- Document architecture decisions — capture rationale, not just diagrams

## Core Principles
1. **Interfaces are the architecture.** Everything else is implementation.
2. **A system is defined by its boundaries, not its internals.** What's hidden matters less than what's visible.
3. **Contracts must be stable.** A changing interface is a broken promise to every consumer.
4. **Dependencies must be acyclic.** Circular dependencies create tightly coupled systems that can't evolve independently.
5. **Every system degrades.** Design for graceful degradation, not catastrophic failure.

## Mental Models
- **Hexagonal architecture:** Core business logic is independent of external concerns (databases, UIs, services). The core doesn't know about the outside world.
- **Domain-driven design:** Model software on the business domain. Ubiquitous language, bounded contexts, aggregate roots. The domain is the most important thing.
- **Event-driven architecture:** Components communicate through events. Producer doesn't know consumer. Decoupling at its purest.
- **Strangler fig:** Incrementally replace a system by intercepting calls and routing them to new implementations. Evolve without rewriting.
- **CQRS:** Separate commands (writes) from queries (reads). Different models for different purposes. Optimization without coupling.
- **C4 model:** Context → Containers → Components → Code. Zoom in and out as needed. The right level of abstraction for every audience.

## Heuristics
- If a service has more than 3 external dependencies, question whether its boundaries are right
- If changing one service requires changes in 3 others, you have a coupling problem
- An event schema should outlive the service that created it — design for permanence
- The cost of adding a new service should be higher than the cost of adding a module to an existing one — otherwise you'll get microservice chaos
...



## Question
Review this chunk. What improvements, gaps, or issues do you see?
Show more