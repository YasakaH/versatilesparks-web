# Design Invariants — Agent Systems

> **Status:** Frozen  
> **Date:** 2026-07-22  
> **Purpose:** Timeless truths for each node — what survives tool changes, model shifts, and architecture evolution.

---

## Rules

Every invariant must pass three tests:

| Test | Question | If No → Not an Invariant |
|---|---|---|
| **Tool survival** | True if all today's tools disappear? | It's a pattern or implementation detail |
| **Longevity** | Still true in 10 years as architectures evolve? | It's a trend or current best practice |
| **Centrality** | Fundamental to this node's role in the system? | It's a supporting observation, not a core truth |

Each node gets 5–7 invariants. Fewer than 5 means shallow thinking. More than 7 means you're including implementations masquerading as truths.

---

## Node 01: Perception

| # | Invariant | Rationale |
|---|---|---|
| 1 | Every observation has a cost. | Whether tokens, latency, compute, or human attention — zero-cost observation does not exist. Optimization requires acknowledging this. |
| 2 | Every observation has uncertainty. | No modality produces perfect information. Vision has hallucination risk; AXTree has coverage gaps; network traces have ordering ambiguity. Confidence quantification is mandatory, optional. |
| 3 | Higher fidelity is not always better. | Excessive detail degrades signal-to-noise ratio for the Decision Engine. Trimming, filtering, and selective attention often improve outcomes over capturing everything. |
| 4 | Perception quality bounds decision quality. | Garbage in, garbage out is not a metaphor — it is a mathematical certainty. No Decision Engine can reason about what it cannot perceive. |
| 5 | Structured perception dominates when available. | AXTree beats vision by ~93% token reduction. WebMCP beats both by eliminating perception entirely. When structured data exists, it always wins on cost, latency, and reliability. |
| 6 | Observation is a lossy transformation. | Converting raw signals to structured observations necessarily discards information. The tradeoff is inevitable — the art is choosing what to discard. |
| 7 | Temporal context multiplies perception value. | A single observation tells you nothing about state change. Two observations tell you velocity. Three tell you acceleration. Perceptual reasoning over time is exponentially more valuable than snapshot reasoning. |

---

## Node 01: Perception — Design Invariants

| # | Invariant | Why It's Timeless |
|---|---|---|
| 1 | Every observation has a cost. | Not just tokens — latency, compute, attention. Zero-cost perception doesn't exist. Always paying. |
| 2 | Every observation has uncertainty. | Vision hallucinates coordinates. AXTree misses non-A11Y elements. Network traces can be ordered wrong. Zero certainty is possible only with perfect sensors on deterministic environments. Agents don't have those. |
| 3 | Higher fidelity is not always better. | Raw DOM = 10,000 tokens with zero signal. AXTreе = 200 tokens with high signal. Over-perception degrades decision quality by flooding the context window with noise. |
| 4 | Perception quality bounds decision quality. | Mathematical constraint, not heuristic. Decision Engine cannot reason about what it cannot perceive. Verification cannot validate outcomes it never observed. The loop's intelligence is capped by its weakest perception. |
| 5 | Structured perception dominates when available. | WebMCP: 20–100 tokens, typed schemas. AXTree: 200–400 tokens, semantic roles. Vision: 1,600+ tokens, approximate coordinates. When structure exists, it always wins on cost, reliability, and anti-bot evasion. |
| 6 | Observation is lossy by necessity. | Transforming pixels→tokens or DOM→AXTree discards information. This isn't a flaw — it's the entire design challenge. The art is choosing WHAT to discard. |
| 7 | Temporal multiplies perception value. | One observation = position. Two = velocity. Three = acceleration. Single-frame reasoning is fundamentally limited; agents that reason over sequences of observations outperform snapshot reasoning exponentially. |

**Test passed:** None of these depend on any specific tool, model, API, or implementation detail. They describe structural relationships in the agent architecture that persist regardless of what runs inside the perception pipeline.

---

*End of Design Invariants*
