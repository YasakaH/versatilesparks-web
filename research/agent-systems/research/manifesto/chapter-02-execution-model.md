# The Agent Execution Model

## 1. The Loop — One Mental Model

Everything about agent systems converges on a single structure. Not twenty-four nodes. Not a complex flowchart. A loop.

```
Perception → Decision → Planning → Scheduling → Execution → Verification → Recovery → Learning
                      ↑                                                    │
                      └───────────────────────────── Feedback ─────────────┘
```

This is not a workflow diagram. It's an **architecture**. Every component has a defined role, clear boundaries, and explicit interfaces with its neighbors. When you understand this loop, you understand agent systems. Everything else is detail.

**Perception** converts environmental signals into structured observations with confidence scores. It answers: "What is happening right now?"

**Decision Engine** transforms observations into refined intents. It answers: "Given what we see, what should we do and how confident are we?"

**Planning** decomposes intents into actionable step sequences with dependencies and failure anticipation. It answers: "How do we get from here to there?"

**Scheduling** orders steps temporally, manages concurrency, and allocates resources. It answers: "In what order and on what resources do these steps actually execute?"

**Execution** carries out scheduled actions on execution surfaces. It answers: "What does 'doing it' look like?"

**Verification** checks whether execution achieved its intended outcome against success criteria. It answers: "Did we actually succeed?"

**Recovery** handles detected failures through root cause diagnosis, retry strategies, and escalation. It answers: "When things go wrong, what systematic response do we have?"

**Learning** improves future performance based on past experience. It answers: "How do we get better next time?"

These eight nodes are not optional components you add or remove based on your use case. They are **structural requirements** that emerge from the fundamental challenge of building autonomous systems that interact with uncertain environments. You can collapse some (Planning and Scheduling might live in one module), but you cannot eliminate any without breaking the system at scale.

## 2. The Structure That Emerges Naturally

Around this core loop, six architectural layers emerge organically. They are not add-ons. They are structural necessities that appear in every production agent system, regardless of surface or implementation.

**Memory** exists because agents operate in bounded context windows but face unbounded problems. Working Memory (current context), Long-term Memory (retrievable knowledge), and Environment State (external reality) form the memory triad. Without structured memory, every step starts from zero.

**Economics** exists because every operation has a cost — tokens, latency, compute, human review. Perception modality selection is a cost decision. Model routing is a cost decision. Caching strategy is a cost decision. When economics becomes a first-class concern woven into every layer rather than an afterthought tracked separately, agent systems become economically viable.

**Observability** exists because non-deterministic systems must be traceable. Spans (individual operations) chain into traces (causal chains). Without observability, failures are mysteries instead of solvable problems.

**Security** exists because agents that can perceive and act on environments are, by definition, a security attack surface. Context isolation, instruction quarantine, action approval gates, and same-origin boundaries are not optional features — they are architectural necessities for any agent interacting with environments containing hostile actors.

**Governance** exists because non-deterministic systems operating at scale create accountability problems. Audit trails, policy enforcement, compliance checking, and data handling rules ensure that agent systems remain traceable, auditable, and compliant even when individual decisions are probabilistic.

**Runtime** exists because logic needs a host. The runtime environment (container, server, edge device) provides compute resources, network connectivity, and access to execution surfaces. It is the foundation upon which everything else runs.

Six layers. Eight loop nodes. One architecture. This is the entire mental model. Everything in agent systems engineering maps to this structure.

## 3. Why This Is Different From "Build a Loop"

You've probably heard advice like "build a perception-decision-action loop" or "use ReAct patterns." The difference between that guidance and Agent Systems Engineering is the difference between saying "build a car" and providing a complete automotive architecture.

A ReAct pattern gives you Perception → Decision → Action. Your loop has eight nodes and six layers. The ReAct practitioner discovers after three months of production debugging that they needed verification (did the action actually succeed?), recovery (what happens when it doesn't?), and learning (how do we prevent this same failure next time?). These aren't extensions of ReAct — they're structural necessities that emerge when systems scale beyond proof-of-concept.

More importantly, the Agent Execution Model provides **interfaces** between nodes. When your Verification node detects a task failure, it doesn't guess what kind of failure occurred. It knows the contract: Execution produces observable outputs, Verification compares expected vs. actual, and Recovery receives classified failures with specific diagnosis requirements.

This is what makes it an architecture and not a pattern. Patterns tell you what to do. Architectures tell you what to depend on, what to guarantee, and what to explicitly not guarantee. When two teams build agent systems using the same architecture, they share a vocabulary that lets them compare notes, share evidence, and avoid each other's mistakes. When they build using different patterns, they reinvent each other's problems.

## 4. The Architecture in Practice

Here's what this looks like on a real task — navigating a web application, completing a form, submitting data:

**Perception** reads the page. It selects AXTree as primary modality (200-400 tokens, fast, reliable on accessible sites). It generates a structured observation with confidence score 0.92 — the AXTree shows all form fields clearly.

**Decision Engine** receives the observation. Confidence is high, so it routes to a budget model ($0.0002 per token) rather than frontier. Intent: "fill name, email, message fields and submit."

**Planning** decomposes the intent into steps: navigate to form → read field labels → fill name → fill email → fill message → click submit → verify submission. Dependencies are explicit: fill steps require label observations. Failure anticipation identifies that email format validation might fail.

**Scheduling** orders the steps sequentially (form filling requires linear order) and allocates resources: AXTree captures for each field, vision only if a field lacks proper labels. Budget model gets all reasoning; frontier model only if the page contains an unexpected CAPTCHA.

**Execution** performs the actions: uses Playwright MCP to fill fields via AXTree, submits form, logs each span for observability. Token cost tracked at every step.

**Verification** compares the post-submission page state against expected outcomes. Observation confidence drops to 0.65 — the page changed but the AXTree is unclear about whether success was achieved. Verification reports "partial success, low confidence."

**Recovery** classifies the failure: not a technical error, but ambiguous outcome. Strategy: re-perceive with vision to confirm success state, then decide.

**Learning** stores the successful path pattern: "forms with properly labeled fields → AXTree primary works reliably at $0.0002/token." Future similar forms inherit this cached strategy.

Eight nodes. Six layers operating behind the scenes. One coherent architecture. No ad-hoc decisions. No "figure it out as we go." This is what a disciplined approach looks like.

---

*End of Chapter 2 — The Agent Execution Model*
