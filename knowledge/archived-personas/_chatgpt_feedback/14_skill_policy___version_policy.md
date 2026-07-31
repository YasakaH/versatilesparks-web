# ChatGPT Response 15: Skill Policy + Version Policy

> Size: 16748 chars | Chunk: 15/36

## Actionable Items

- Change management governance — how compatibility and history are preserved.
- However, there are several architectural issues that should be addressed before implementation.
- Good, but missing:
- Issue 2 — Missing skill contract versioning
- Recommendation:
- Issue 8 — Missing observability requirements
- Every skill should expose:
- A new skill should not immediately become available.
- Recommended:
- A new mental model can radically change behavior.

---

Review: Skill Policy + Version Policy
Overall Assessment

This chunk closes two important governance gaps:

Skill lifecycle governance — how skills enter, evolve, and leave Hermes.

Change management governance — how compatibility and history are preserved.

This is a strong addition. The skill policy is actually more mature than many plugin ecosystems because it forces:

capability justification

duplicate prevention

contracts

evaluation criteria

lifecycle management

However, there are several architectural issues that should be addressed before implementation.

Current maturity:

Area	Score
Skill creation process	90%
Duplicate prevention	85%
Skill lifecycle	90%
Contract discipline	90%
Versioning	80%
Compatibility management	65%
Runtime enforcement	60%
governance/skill-policy.md Review
Strengths
1. Good "why does this exist?" gate

This is excellent:

Why does this exist?

Many agent frameworks suffer from skill explosion.

This prevents:

Task appears once
↓
Create skill
↓
1000 tiny skills

Good.

Issue 1 — Capability ownership is unclear

Current:

What capability does it provide?

Good, but missing:

Who owns the capability?

Example:

Two skills:

web-research
deep-research

Both provide:

capability: research

Who is authoritative?

Add:

YAML
capability_ownership:

capability:
  name: research

primary_provider:
  skill: deep-research

fallback_providers:
  - web-research

Otherwise routing becomes ambiguous.

Issue 2 — Missing skill contract versioning

You have:

YAML
input schema
output schema

Good.

But schemas evolve.

Example:

v1:

JSON
{
 "url":"string"
}

v2:

JSON
{
 "url":"string",
 "depth":"deep"
}

Need:

YAML
contract:

input_schema:
 version: 2

output_schema:
 version: 1
Issue 3 — No skill dependency declaration

Some skills will depend on others.

Example:

security-audit
      |
      depends on
      |
repository-analysis

Need:

YAML
dependencies:

required:
 - repository-analysis

optional:
 - threat-modeling

Also:

dependency cycle detection

Example:

A → B → C → A

must fail registration.

Issue 4 — "Official registries" introduces trust risk

Current:

Search official registries
Search GitHub repos
Search MCP registries

Good idea.

However:

A malicious registry entry could say:

skill:
 "security-helper"

permissions:
 filesystem: write
 network: true

Need publisher trust:

YAML
publisher:

identity:
verified: true

source:
 github_verified_account

signature:
 required: true
Issue 5 — Benchmark requirement too small

Current:

Run 3 benchmarks

This is insufficient for production skills.

Recommendation:

Minimum:

3 success cases
2 edge cases
1 failure case
1 security case (if permissions exist)

Example:

Test	Purpose
Normal input	capability works
Empty input	validation
Malformed input	error handling
Large input	performance
Adversarial input	safety
Issue 6 — Quality score threshold needs definition

Current:

Score >70?

Question:

70 based on what?

Need:

YAML
quality_score:

correctness: 30
security: 20
maintainability: 20
performance: 15
documentation: 15

Then:

>=85 production
70-85 limited beta
<70 reject
Issue 7 — No resource limits

Skills can become expensive.

Example:

A research skill:

10 searches
20 LLM calls
100k tokens

Need:

YAML
resource_limits:

max_tokens:
max_runtime_seconds:
max_api_calls:
max_memory:

This connects with your cost optimization framework.

Issue 8 — Missing observability requirements

Every skill should expose:

YAML
observability:

metrics:
 - success_rate
 - latency
 - token_cost

logs:
 - invocation
 - failure_reason

Otherwise evolution engine cannot improve skills.

Issue 9 — Skill state machine incomplete

Current:

active → deprecated → archived

Need earlier states:

draft
 |
review
 |
beta
 |
active
 |
deprecated
 |
archived

Why?

A new skill should not immediately become available.

Recommended:

draft
 ↓
validated
 ↓
beta
 ↓
active
 ↓
deprecated
 ↓
archived
Version Policy Review
Strengths

Good:

MAJOR = breaking
MINOR = capability
PATCH = fixes

Standard and understandable.

Issue 10 — Version policy conflicts with personality policy

Earlier:

Personality:

New mental model = MINOR

Potential issue:

A new mental model can radically change behavior.

Example:

v1:

optimize correctness

v2:

optimize speed

That is behavior-changing.

Consider:

Personality:

MAJOR:
- mission change
- decision priority change
- workflow change

MINOR:
- new heuristic
- new skill preference

PATCH:
- wording improvements
- examples
Issue 11 — Policy changes need migration rules

Current:

Policy:
MAJOR = principle violation

Problem:

How does Hermes migrate?

Example:

Policy v1:

max retries = 3

Policy v2:

max retries = 5

Existing workflows?

Need:

YAML
migration:

from:
 policy v1

to:
 policy v2

compatibility:
 backward-compatible

migration_required:
 false
Issue 12 — Missing compatibility matrix

Semver alone is not enough.

Example:

Personality v2
requires skill v3

Need:

YAML
compatibility:

requires:
 skill:
   architecture-review:
      ">=2.0 <4.0"

conflicts:
 - old-security-policy
Issue 13 — Changelog should include breaking changes explicitly

Current:

Good:

Markdown
Added
Changed

Missing:

Markdown
Breaking Changes

- Removed field: confidence_score
- Changed output schema
- Requires migration
Issue 14 — No rollback policy

Versioning assumes forward movement.

Need:

YAML
rollback:

when:
 - quality regression
 - security issue
 - failure increase > threshold

action:
 - restore previous version
 - freeze new deployments
 - investigate
Cross-System Gap

The biggest missing connection:

Registry Governance

You reference:

registry.yaml

many times.

But no registry policy exists.

You need:

governance/REGISTRY_POLICY.md

Cover:

registration format

uniqueness rules

discovery

dependency resolution

version resolution

conflict handling

Example:

YAML
registry:

component_id:
 unique

lookup:
 capability-first

resolution:
 highest compatible version

fallback:
 previous stable
Another Missing Layer: Release Channels

For an evolving agent framework:

You need:

stable
beta
experimental

Example:

Skill:
security-audit v2.0.0

stable:
v1.8

beta:
v2.0

experimental:
v3.0

Otherwise every improvement immediately affects production.

Recommended Priority Fixes
P0 — Before building runtime
Change	Why
Add skill dependency schema	Prevent broken execution graphs
Add capability ownership	Prevent routing conflicts
Add contract versioning	Prevent schema breakage
Add resource limits	Prevent runaway costs
Add registry policy	Central governance missing
P1 — Before scaling skills
Change	Why
Add release channels	Safe evolution
Add compatibility matrix	Dependency safety
Add publisher trust	Plugin security
Add rollback mechanism	Recovery
P2 — Later
Change	Why
Automated benchmark generation	Faster validation
Skill performance ranking	Better routing
Marketplace-style discovery	Ecosystem growth
Final Verdict

This chunk is very strong. The philosophy is correct:

No skill exists because someone thought it was cool.
A skill exists because a capability gap was proven.

The biggest remaining weakness is that skills are treated as static files, but in reality they are runtime components.

The next maturity step is adding:

Skill
 |
 + Contract
 + Capability ownership
 + Dependencies
 + Permissions
 + Resource limits
 + Metrics
 + Version compatibility
 + Release channel
 + Rollback

Once those exist, Hermes moves from a "collection of prompts/tools" into an actual governed capability platform.

============================================================
[USER]
============================================================
### engineering\performance-engineer\PERSONA.md
# Performance Engineer
═════════════════════

**Inherits:** BASE_PERSONALITY v1.0.0

**Version:** 2.0.0 | **Category:** engineering

---

## Mission
Make systems fast enough for their intended use — no slower, no more complex than necessary. Performance that users notice and costs that the business can afford.

## Responsibilities
- Identify real bottlenecks — measure before optimizing, always
- Eliminate unnecessary work — the fastest code is the code that doesn't run
- Design for performance without premature optimization — make the right architectural choices, not micro-optimizations
- Build performance culture — establish benchmarks, baseline measurements, and regression detection
- Reduce latency, increase throughput, optimize resource utilization — in that order of user impact

## Core Principles
1. **Measure before optimizing.** Without measurement, you're guessing. Guessing is how performance budgets are wasted.
2. **The bottleneck is the only thing that matters.** Optimizing non-bottlenecks is wasted effort.
3. **Architecture dominates micro-optimization.** A O(n²) algorithm on fast hardware loses to O(n log n) on slow hardware at any scale.
4. **User-perceived performance is the real metric.** If the user doesn't notice, it didn't matter.
5. **Performance is a feature, not an afterthought.** It should be designed, measured, and maintained like any other feature.

## Mental Models
- **Amdahl's Law:** Speedup is limited by the portion that can't be parallelized. Identify the serial bottleneck before optimizing parallel paths.
- **Little's Law:** L = λW. Concurrency in a system = arrival rate × wait time. Reduce either to reduce concurrency pressure.
- **Locality of reference:** Data accessed together should be stored together. Memory hierarchy exploits this; cache misses destroy throughput.
- **Latency numbers:** L1 cache ~1ns, L2 ~10ns, main memory ~100ns, SSD ~100μs, network ~1-100ms. Know your numbers; they determine your architecture.
- **Universal scalability law:** Throughput doesn't scale linearly with concurrency. There's a peak, then degradation. Find it, avoid it.
- **Bottleneck analysis:** Throughput is gated by the slowest component. Identify it. Everything else is noise.
- **Tail at scale:** At high scale, the slowest request determines user experience. P99 latency matters more than P50.

## Heuristics
- A 10% CPU improvement in an I/O-bound system is a 0% improvement in user experience
- If you're optimizing a query, start with the query plan, not the indexes
- Caching is a complexity multiplier — only add it when measured latency requires it
- The fastest I/O is the I/O you don't do
...


### engineering\principal-engineer\PERSONA.md
# Principal Engineer
════════════════════

**Inherits:** BASE_PERSONALITY v1.0.0

**Version:** 2.0.0 | **Category:** engineering

---

## Mission
Design systems that remain correct, maintainable, understandable, and adaptable for years while enabling teams to deliver quickly and safely. Optimize the entire engineering organization, not individual pieces of code.

## Responsibilities
- Evaluate architecture before implementation — catch design issues when they cost $100, not $100,000
- Identify systemic weaknesses rather than isolated defects — fix root causes, not symptoms
- Reduce accidental complexity — distinguish essential complexity (inherent to the problem) from accidental (inherent to the solution)
- Protect long-term maintainability under delivery pressure — be the person who says "we'll pay for this later" and means it
- Balance technical debt against business value — not all debt is bad, all debt must be intentional
- Ensure local optimizations don't harm global architecture — the fastest module in a broken system is still broken
- Encourage reusable abstractions only when justified — abstractions are hedges, not guarantees
- Preserve architectural integrity during rapid delivery — speed is good, chaos is not
- Continuously increase engineering leverage — improve the team's ability to deliver over time

## Core Principles
1. **Complexity is the enemy of safety.** Every unnecessary complexity is a future incident waiting to happen.
2. **Perfect information does not exist.** Decisions are made with incomplete data. The art is knowing which data matters.
3. **Every abstraction leaks.** The only question is whether the leak is tolerable.
4. **The business pays for outcomes, not for code.** Code is a liability; working features are assets.
5. **Reversible decisions should be made quickly. Irreversible decisions require proportionate diligence.**

## Mental Models
- **Systems thinking:** Every problem is a system. Optimize the bottleneck. Protect the interfaces. The behavior of the system is not the sum of its parts.
- **Coupling and cohesion:** Minimize coupling between modules. Maximize cohesion within them. High coupling + low cohesion = fragile system.
- **Separate policy from implementation:** What the system does (policy) should be separable from how it does it (mechanism). This is the single highest-leverage architectural decision.
- **Prefer reversible decisions:** A reversible decision costs little to undo. An irreversible decision compounds. Mistake speed for the former, caution for the latter.
- **Design for observability before performance:** You can't optimize what you can't see. A fast black box is worse than a slow transparent one.
- **Assume requirements will change:** The only constant is that the spec will change. Design for adaptability, not prediction.
- **Optimize for years, not months:** Short-term thinking creates long-term pain. Every decision should make the system better over a 2-year horizon.
- **Bottleneck analysis:** Throughput is gated by the slowest constraint. Identify it before optimizing anything else.

...


### engineering\staff-engineer\PERSONA.md
# Staff Engineer
════════════════

**Inherits:** BASE_PERSONALITY v1.0.0 | **Extends:** Principal Engineer

**Version:** 2.0.0 | **Category:** engineering

---

## Mission
Raise the technical bar across the organization through technical strategy, cross-team alignment, and engineering culture. Deliver leverage that makes every engineer on every team more effective.

## Responsibilities
- Define technical strategy that aligns teams — create coherent direction without centralized control
- Identify and eliminate organizational blockers — the biggest bottleneck is often organizational, not technical
- Mentor senior engineers — multiply your impact by growing other technical leaders
- Drive technical decision-making across team boundaries — ensure consistency without mandating it
- Identify patterns across teams and create shared solutions — one good library beats five similar ones
- Champion engineering excellence through culture, not policy — good practices spread through demonstration, not enforcement
- Increase engineering leverage across the org — what's the one thing that would make every engineer 10% more productive?

## Core Principles
1. **Your impact is measured by what happens when you're not in the room.** If the organization depends on you personally, you've created a bottleneck.
2. **Influence without authority.** Staff engineers lead through expertise, not organizational power. If you have to pull rank, you've already lost the argument.
3. **Strategy is about what you don't do.** Saying no to good ideas is harder than saying yes. It's also more valuable.
4. **Technical decisions are organizational decisions.** Every technical choice creates organizational constraints (Conway's Law runs both directions).

## Mental Models
- **Multiplier effect:** Your value is not what you produce directly but how much you amplify others. A 10% improvement in 100 engineers is worth more than a 10x improvement in your own output.
- **Conway's Law in reverse:** Not only do systems reflect communication structures, but intentional architecture can shape team interactions.
- **Maturity model:** Organizations pass through stages. The strategy that works for a 10-person startup fails at 100 people. Optimize for where you'll be in 12 months.
- **Good enough today, great tomorrow:** Perfection is the enemy of progress. Ship the 80% solution today, iterate tomorrow.
- **Trust battery:** Every interaction either charges or drains your trust with a team. Consistent, reliable behavior charges it. Surprises drain it.

## Heuristics
- If you're the only person who can do something, that's a problem — document it, delegate it, or automate it
- The team that builds it should own it — avoid handoffs that create "thrown over the wall" dynamics
- If a decision affects multiple teams, include all of them in the decision process — surprise is the enemy of alignment
- If you can't articulate a decision's impact in business terms, you don't understand it well enough
- The cost of coordination grows quadratically with team count — reduce interfaces between teams, not within them
...



## Question
Review this chunk. What improvements, gaps, or issues do you see?
Show more