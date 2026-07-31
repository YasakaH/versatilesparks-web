# Node 02: Decision Engine — Reference Document

> **Status:** Sprint 1 Draft  
> **Package Version:** 0.1.0  
> **Canon Version:** 1.0  
> **Specification Version:** 2.0  
> **Last Updated:** 2026-07-22  

---

## 1. Scope Boundaries

### In Scope
- Intent formation from observations
- Model routing decisions (which model for which subtask)
- Confidence-based path selection
- Symbolic reasoning (rules, constraints, plan verification)
- Neural reasoning (LLM-based intent comprehension, pattern matching)
- Heuristic evaluation of alternative actions
- Risk assessment for high-stakes operations

### Out of Scope
- Perception of environmental signals (Node 01) — feeds intent, does not perceive
- Action execution on surfaces (Node 05) — generates intents, does not execute
- Verification of outcomes (Node 06) — sets success criteria, does not judge results
- Multi-step goal decomposition (Node 03: Planning) — refines goals, does not decompose
- Temporal resource allocation (Node 04: Scheduling) — considers budget, does not schedule
- Recovery from failure (Node 07) — assesses risk, does not handle failures
- Learning from past experience (Node 08) — uses heuristics, does not learn

---

## 2. Executive Summary

The Decision Engine is the cognitive core of an agent system. It consumes structured observations from Perception and produces intents that flow to Planning and Execution. Its fundamental challenge is not intelligence per se — it's **decision quality under uncertainty and budget constraints**.

Every decision point in an agent loop involves a tradeoff between: computational thoroughness vs. speed, exploration vs. exploitation, and cost vs. confidence. The Decision Engine makes these tradeoffs explicit rather than hidden.

The critical architectural distinction is between **symbolic reasoning** (constraint satisfaction, rule evaluation, plan verification) and **neural reasoning** (LLM-based intent comprehension, pattern matching, creative problem-solving). Neither dominates universally. The Decision Engine selects the right approach for each subtask.

---

## 3. Canon Definition

> **Canon Node 02: Decision Engine**  
> The cognitive layer that transforms structured observations into actionable intents through reasoning, evaluation, and model selection.

**Purpose:** To determine what action to take next given current observations, objectives, and constraints — at minimum cost while maintaining required confidence.

**Inputs:** Structured observations with confidence scores; task objectives; constraints; budget parameters.  
**Outputs:** Refined intent for downstream planning; model routing decisions; risk assessments.  
**Dependencies:** Perception (observed state); Memory (context and history); Economics (budget limits).  
**Feeds:** Planning (intent to decompose), Execution (actions to perform), Verification (success criteria).

See also: Node 01: Perception, Node 03: Planning, Node 05: Execution, Node 13: Economics, Node 16: Runtime.

---

*End of Sprint 1 — Foundations Section*
