# Dependency Matrix — Agent Systems Architecture

> **Status:** Active  
> **Date:** 2026-07-22  
> **Purpose:** Global architectural map showing which nodes depend on which. Auto-generated from CONTRACT.md files.

---

## Node Dependencies

| Node | Name | Depends On | Used By | Status |
|---|---|---|---|---|
| 01 | Perception | Environment State (11), Execution Surfaces (17–22), Working Memory (09) | Decision Engine (02), Verification (06) | ✅ Package complete |
| 02 | Decision Engine | Perception (01), Memory (09, 10, 11), Economics (13) | Planning (03), Execution (05) | 📝 Sprint 1 |
| 03 | Planning | Decision Engine (02) | Scheduling (04) | ✅ Package complete |
| 04 | Scheduling | Planning (03) | Execution (05) | ✅ Package complete |
| 05 | Execution | Scheduling (04), Planning (03) | Verification (06) | 📝 Sprint 1 |
| 06 | Verification | Execution (05), Perception (01) | Recovery (07), Learning (08) | 📝 Sprint 1 |
| 07 | Recovery | Verification (06) | Learning (08) | ⏸ Not in Wave 1 |
| 08 | Learning | Recovery (07), Past Experience (09–11) | Decision Engine (02), Planning (03) | ⏸ Not in Wave 1 |
| 09 | Working Memory | All nodes (session-scoped) | — | ⏸ Not in Wave 1 |
| 10 | Long-term Memory | All nodes (persistent) | — | ⏸ Not in Wave 1 |
| 11 | Environment State | All nodes (read) | — | ⏸ Not in Wave 1 |
| 12 | Observability | All nodes (traces) | — | ⏸ Not in Wave 1 |
| 13 | Economics | All nodes (cost data) | — | ⏸ Not in Wave 1 |
| 14 | Security | All nodes (policies) | — | ⏸ Not in Wave 1 |
| 15 | Governance | All nodes (compliance) | — | ⏸ Not in Wave 1 |
| 16 | Runtime | All nodes (compute) | — | ⏸ Not in Wave 1 |
| 17 | Browser Surface | — | Perception (01) | ⏸ Surface node |
| 18 | Desktop Surface | — | Perception (01) | ⏸ Surface node |
| 19 | Terminal Surface | — | Perception (01) | ⏸ Surface node |
| 20 | API Surface | — | Perception (01) | ⏸ Surface node |
| 21 | Mobile Surface | — | Perception (01) | ⏸ Surface node |
| 22 | IoT Surface | — | Perception (01) | ⏸ Surface node |

---

## Dependency Graph Notes

- Primary execution path: **01 → 02 → 03 → 04 → 05 → 06 → 07** with feedback loop from 07→08→02
- All nodes read from Environment State (11) and contribute traces to Observability (12)
- Economics (13) consumes cost data from all nodes; Security (14) and Governance (15) apply policies across all nodes
- Runtime (16) hosts all logic; Execution Surfaces (17–22) provide signal availability

---

*End of Dependency Matrix*
