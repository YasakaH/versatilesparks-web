# Layers

## 1. Why Six Layers?

Memory, Economics, Observability, Security, Governance, Runtime. They don't appear in your agent tutorial. They don't show up in framework documentation. But every production agent system discovers them — usually the hard way, after scaling costs explode or a security audit fails or you realize nobody knows why a specific decision was made.

These aren't optional features you bolt on. They're structural consequences of the Agent Execution Model. Remove any one and the system breaks at scale. Not "might break" — "will break." Here's why each emerges necessarily.

## 2. Memory: The Context Problem

Every agent operates inside a context window with finite capacity. Every problem it faces has infinite scope. This gap between bounded perception and unbounded problems is the fundamental memory challenge.

The solution isn't "use a bigger model." Bigger models mean higher cost, higher latency, and diminishing returns. The solution is structured memory across three layers:

**Working Memory** holds recent observations and decisions within the current task context. It's the agent's short-term workspace — what happened in the last five steps, what intent was formed, what actions are pending. When context fills, working memory compresses: keep the signal, discard the noise.

**Long-term Memory** stores patterns, strategies, and knowledge that persist across sessions. Successful paths get cached. Failed approaches get avoided. Environmental knowledge gets indexed. This is how agents get faster and more reliable over time instead of repeating the same mistakes.

**Environment State** is the external reality — cookies, session data, local storage, network state — maintained independently of the agent's perception. The environment has its own state that exists whether the agent observes it or not. Tracking this distinction prevents stale-perception bugs where the agent acts on outdated understanding.

Without structured memory, every step starts from zero. With it, agents compound knowledge across sessions — getting faster, cheaper, and more reliable as they accumulate experience. That compounding effect is what separates a production system from a proof-of-concept.

## 3. Economics: The Cost Problem

Perception modality selection is a cost decision. AXTree costs 200-400 tokens; vision costs 1,600+. Every observation has a budget impact. Every retry has a budget impact. Every hour of compute has a budget impact.

When economics lives outside the architecture — tracked in spreadsheets, discovered after the fact, optimized through vague "use cheaper models" advice — systems fail silently. You don't know which module is bleeding money until it's too late.

When economics is a first-class architectural layer — woven into Perception's modality selection, Decision Engine's model routing, Planning's step estimation, and Execution's resource allocation — every decision carries cost awareness. Perception chooses AXTree over vision because the budget model can handle the observation. Decision Engine routes straightforward classification to a $0.001 model and reserves $0.10 models for ambiguous cases. Planning anticipates that complex pages need fallback chains and budgets accordingly.

The economics layer answers questions that ad-hoc architectures can't: What does this task cost per step? What's our cache hit rate? Which modalities are most expensive relative to their reliability? Where do retries concentrate? Who approved this action?

Cost control isn't an optimization for agent systems — it's a structural requirement. Without the economics layer, systems either bleed money unnoticed or operate conservatively because nobody understands the cost profile. With it, economics becomes measurable, predictable, and optimizable the same way any other system metric.

## 4. Observability: The Traceability Problem

Deterministic systems produce deterministic results. Non-deterministic systems produce probabilistic outcomes. When a non-deterministic system operates autonomously and makes wrong decisions, you need to know: which decision was wrong, why it was made, and what evidence was available when it was made.

This is the observability problem. And it's the difference between debugging and mystery.

Observability works through two linked concepts:

**Spans** are individual operations — one perception event, one model call, one action. Each span records what happened, when it happened, how long it took, and what it cost. Spans are the atomic units of traceability.

**Traces** chain spans together into causal sequences. When Verification detects a failure, the trace shows you exactly which decision led to it. Which observation had low confidence. Which model was routed. Which action was taken. Why the success criteria weren't met.

Without observability, agent failures are black boxes. You see "task failed" and have no way to reconstruct why. With it, every failure is decomposable into its component decisions, each with full context: the observation that triggered it, the model that evaluated it, the action it produced, the verification that judged it.

Observability isn't a logging feature. It's the mechanism that lets probabilistic systems be accountable. Without it, autonomous agents are unfalsifiable by design — you literally cannot determine whether a failure came from bad perception, poor decision-making, execution errors, or insufficient verification.

## 5. Security: The Access Problem

An agent that can perceive and act on environments is, by definition, a privileged access point. It reads your data. It modifies your state. It makes decisions on your behalf. If that agent is compromised, the attacker doesn't just read your data — they have full operational access to everything the agent can reach.

This creates security requirements that don't exist in traditional software:

**Context isolation** separates the agent's instruction set from the data it processes. A malicious webpage cannot inject instructions into the agent through page content. Context isolation ensures that what the agent was told to do is never confused with what it observed doing.

**Instruction quarantine** keeps user/environment content separate from system prompts. Page text, form fields, error messages — all treated as data, not instructions. The agent executes its goals against the data without confusing the two.

**Action approval gates** add human-in-the-loop checkpoints for sensitive operations. Writing data, modifying configurations, transferring resources — these require explicit approval rather than autonomous execution.

**Same-origin boundaries** restrict what an agent can access based on trust relationships. An agent authorized to operate on example.com should not automatically have permission to modify settings on admin.example.com. Boundary enforcement prevents lateral movement.

Security isn't a compliance checkbox for agent systems. It's an architectural necessity that emerges directly from the agent's ability to perceive and act autonomously in shared environments. Traditional software security focuses on protecting systems from external attackers. Agent security must also protect external systems from internal failures — because a buggy agent is functionally equivalent to an attacker with legitimate credentials.

## 6. Governance: The Accountability Problem

When systems make autonomous decisions at scale, someone needs to answer: Was this decision correct? Does it comply with policy? Should we allow this pattern? How do we ensure consistency?

Governance answers these questions through mechanisms that operate at the architectural level rather than the application level:

**Policy enforcement** defines what the agent can and cannot do. Rate limits, allowed surfaces, data handling constraints, approval requirements — all codified as policies that every node respects, not as optional checks that developers remember to implement.

**Audit trails** record every significant decision and its justification. Not just "what happened" but "why it was chosen." This differs from observability: traces show causality; audits show decision rationale. Both are necessary.

**Compliance checking** verifies that agent operations conform to regulatory and organizational requirements. Data handling rules, retention policies, access controls — enforced architecturally rather than as an afterthought.

**Consistency controls** ensure that similar tasks follow similar patterns. If two agents process payment forms, they should use the same verification steps, apply the same security checks, and follow the same governance rules. Consistency isn't about identical behavior — it's about predictable, auditable behavior.

Governance exists because autonomy without accountability is recklessness. The architecture provides the structure that makes autonomous agents trustworthy: auditable decisions, enforceable policies, consistent patterns, and clear responsibility boundaries.

## 7. Runtime: The Foundation

Everything runs somewhere. The runtime layer provides the compute environment, network connectivity, and surface access that every other layer depends on. Containers, servers, edge devices — the runtime is where logic lives and where surface connections happen.

Runtime choices cascade through the entire architecture. Containerized runtimes provide isolation and reproducibility. Edge runtimes reduce latency but constrain resources. Serverless runtimes scale automatically but introduce cold-start penalties. Each runtime choice affects economics, security boundaries, observability granularity, and execution surface capabilities.

Runtime is foundational because it determines what's possible at the physical level. No amount of architectural elegance compensates for a runtime that can't support the required throughput, latency, or surface access patterns.

---

*End of Chapter 3 — Layers*
