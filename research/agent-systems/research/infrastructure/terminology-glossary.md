# Terminology Glossary v1.0

> **Status:** Frozen  
> **Date:** 2026-07-22  
> **Purpose:** Single authoritative vocabulary for Agent Systems Engineering. Every node document MUST use these definitions consistently.

---

## Glossary

| Term | Definition |
|---|---|
| **observation** | A structured representation of environmental state produced by perception. Must include confidence score and timestamp. Distinguish from raw signal — an observation is a transformed, tokenized artifact ready for consumption. |
| **signal** | Raw data from an execution surface before transformation. Can be pixels, bytes, DOM nodes, audio waves, or sensor readings. Signals become observations after modality selection and transformation. |
| **modality** | The method of converting signals into observations. Examples: vision (screenshot→tokens), AXTree (DOM accessibility tree→structured nodes), WebMCP (typed tool call→structured response). Each has different cost/reliability/coverage tradeoffs. |
| **confidence** | A numeric value (0.0–1.0) attached to every observation indicating reliability for the current task. Determined by signal completeness, temporal freshness, modality-task match quality, and cross-modal agreement. |
| **environment** | The external world the agent interacts with, including execution surfaces, data stores, connected services, and physical systems (IoT/robotics). Has state that exists independently of the agent's perception. |
| **state** | The current condition of the environment at a point in time. Distinguish from memory — state exists outside the agent; memory is the agent's internal representation of past states. |
| **execution surface** | The medium through which an agent perceives and acts. Surface types: Browser, Desktop/GUI, Terminal/CLI, API/Service, Mobile/App, IoT/Robotics. Each surface offers different signal availability. |
| **runtime** | The compute environment hosting agent logic. Distinct from execution surface: runtime is WHERE code runs, surface is WHAT the agent interacts with. Example: Docker container (runtime) running Playwright to interact with a browser (surface). |
| **verification** | Systematic checking whether execution achieved intended outcomes against pre-defined success criteria. Not perception — perception captures "what happened," verification evaluates "did we achieve what we wanted?" |
| **recovery** | Structured handling of failures detected by verification. Includes root cause diagnosis, retry strategies, path switching, and escalation. Recovery feeds failure patterns into learning. |

---

*End of Terminology Glossary v1.0*
