# Node 01: Perception — Reference Document

> **Status:** Pilot Draft  
> **Package Version:** 0.1.0  
> **Canon Version:** 1.0  
> **Specification Version:** 2.0  
> **Last Updated:** 2026-07-22  

---

## 1. Scope Boundaries

### In Scope
- Sensory acquisition from any execution surface
- Modality selection (vision, text, structured data, audio, sensor streams)
- Signal transformation (compression, tokenization, filtering)
- Observation quality assessment (confidence, completeness, freshness)
- Temporal context management (change detection between observations)

### Out of Scope
- Planning and goal decomposition (Node 03) — handled by Decision Engine's intent
- Decision and reasoning (Node 02) — perception feeds intent, does not evaluate it
- Verification and outcome checking (Node 06) — perception provides evidence; verification judges it
- Recovery and error handling (Node 07) — perception records failures; recovery diagnoses them
- Learning and caching (Node 08) — perception patterns are stored; learning decides what to store
- Token economics and inference cost (Node 13) — cost-awareness is a design constraint, not a cost model
- Execution Runtime selection (Node 16) — runtime provides the surface; perception reads from it

---

## 2. Executive Summary

Perception is the first node in the agent loop. It converts raw environmental signals into structured observations that the Decision Engine can consume. The critical insight is that perception is a cost-quality tradeoff, not just a technical choice. Every modality has a different token cost, latency, reliability profile, and failure mode.

Three architectures coexist in production today: vision-based (screenshots), accessibility-tree-based (AXTree), and hybrid (AXTree primary + vision fallback). A fourth is emerging: WebMCP (structured tool exposure via `navigator.modelContext`). Which you use depends on the surface, the task, and the budget.

Perception quality determines everything downstream. Garbage in, garbage out is not a metaphor for agents — it is a mathematical certainty. The Decision Engine cannot reason about what it cannot perceive, and the Verification node cannot validate outcomes it never observed.

---

## 3. Canon Definition

> **Canon Node 01: Perception**  
> The process of converting environmental signals into structured observations that can be consumed by the Decision Engine.

**Purpose:** To answer "What is happening right now?" with sufficient fidelity to make correct decisions.

**Inputs:** Raw environment signals (pixels, bytes, streams, events); execution surface capabilities; previous observations.  
**Outputs:** Structured observations; confidence scores; observation metadata.  
**Dependencies:** Execution Surface (what data types are available); Working Memory (stores recent observations); Economics (modality selection is a cost decision).  
**Feeds:** Decision Engine (primary input — all reasoning starts from perception).

See also: Node 11: Environment State, Node 12: Observability, Node 13: Economics, Nodes 17–22: Execution Surfaces.

---

## 4. Mental Model

### The Perception Funnel

```
Raw Environment
       │
       ▼
Signal Acquisition  ← What data sources are available?
       │
       ▼
Modality Selection  ← Which representation? (vision / AXTree / structured / sensor)
       │
       ▼
Signal Transformation ← Compression, tokenization, filtering
       │
       ▼
Structured Observation ← Output for Decision Engine
       │
       ▼
Confidence Assessment ← How reliable is this observation?
       │
       ▼
Structured Observation + Confidence Score → Decision Engine
```

### Three Primary Architectures

| Architecture | Signal Type | Tokens/Step | Latency | Best For |
|---|---|---|---|---|
| Vision | Screenshot pixels | 1,600–2,000+ | 15–60s | Canvas apps, unknown UIs, cross-platform |
| AXTree | Accessibility tree (ARIA roles/names) | 200–400 | 3–10s | A11Y-compliant sites, high-volume automation |
| Hybrid | AXTree + selective vision | 500–1,500 avg | 5–15s | Production work — recommended default |
| WebMCP | Typed JS function calls | 20–100 | 1–2s | Websites that expose tools natively |

**Key insight:** These are not competing technologies. They operate at different abstraction layers. Confusing them is the source of much disappointment with browser agents. A serious product uses more than one.

---

## 5. Design Invariants

These are timeless truths about Perception that survive tool changes, model shifts, and architecture evolution. If an assertion fails any test below, it belongs in Modules B or C, not here.

**Test criteria:**
1. True if all today's tools disappear? (Not a pattern/implementation detail)
2. Still true in 10 years as architectures evolve? (Not a trend)
3. Fundamental to this node's role in the system? (Not a supporting observation)

| # | Invariant | Rationale |
|---|---|---|
| 1 | **Every observation has a cost.** | Not just tokens — latency, compute, attention. Zero-cost perception doesn't exist. Always paying. |
| 2 | **Every observation has uncertainty.** | Vision hallucinates coordinates. AXTree misses non-A11Y elements. Network traces can be ordered wrong. Zero certainty is possible only with perfect sensors on deterministic environments. Agents don't have those. |
| 3 | **Higher fidelity is not always better.** | Raw DOM = 10,000 tokens with zero signal. AXTree = 200 tokens with high signal. Over-perception degrades decision quality by flooding the context window with noise. |
| 4 | **Perception quality bounds decision quality.** | Mathematical constraint, not heuristic. Decision Engine cannot reason about what it cannot perceive. Verification cannot validate outcomes it never observed. |
| 5 | **Structured perception dominates when available.** | WebMCP: 20–100 tokens, typed schemas. AXTree: 200–400 tokens, semantic roles. Vision: 1,600+ tokens, approximate coordinates. When structure exists, it wins on cost, reliability, and anti-bot evasion. |
| 6 | **Observation is lossy by necessity.** | Transforming pixels→tokens or DOM→AXTree discards information. This isn't a flaw — it's the entire design challenge. The art is choosing WHAT to discard. |
| 7 | **Temporal multiplies perception value.** | One observation = position. Two = velocity. Three = acceleration. Single-frame reasoning is fundamentally limited; agents that reason over sequences outperform snapshot reasoning exponentially. |

---

## Module A — Theory & Architecture

### 6. Historical Evolution

Pre-Agent Era (2000–2019): Browser automation was deterministic. Scripts used CSS selectors, XPath, element IDs. No "perception" — the script knew exactly what to look for because it wrote the selectors. Tools: Selenium (2004), Puppeteer (2017).

Early Agent Era (2020–2023): LLMs entered via screenshots. WebVoyager (2023) used vision-only: screenshot → LLM describes → LLM acts. Simple but expensive. Token costs were 10–100x scripted automation.

AXTree Convergence (2024–2025): Playwright introduced `ariaSnapshot()` and the Playwright MCP server. Agents could read structured UI metadata instead of guessing from pixels. Browser Use, MultiOn, and the wave of MCP servers shipped through 2025 reading AXTrees.

Hybrid Era (2025–Present): Production teams found AXTree alone insufficient — many sites are not fully WCAG-compliant. Solution: AXTree primary, vision fallback. Stagehand pioneered this. Google Mariner achieved 83.5% on visual acuity benchmarks using hybrid approaches.

Structured Tool Era (Emerging): WebMCP (W3C Draft, Feb 2026) lets websites expose typed tool calls directly. Eliminates perception entirely — the website offers structured data rather than the agent extracting it.

### 7. Architecture Overview

Perception is a pipeline: signal acquisition → modality selection → transformation → structured output + confidence score.

The modality selection layer is the architectural heart. It answers: given the task, the surface, and the budget, which observation method yields the best signal-to-noise ratio at lowest cost?

### 8. Core Components

**Signal Acquisition:** What raw data is available? Different surfaces offer different signal types:
- Browser: DOM, AXTree, screenshots, console logs, network traffic, storage, events
- Desktop: screen pixels, OS accessibility tree, window titles, clipboard
- Terminal: stdout/stderr streams, exit codes, process state
- API: JSON/XML responses, WebSocket events, HTTP status codes
- Mobile: view hierarchy, touch events, screen pixels, push notifications
- IoT: sensor streams (camera, lidar, IMU), actuator state, telemetry

**Modality Selection:** Choosing the right observation method. This is where economics meets engineering — every modality trades off cost against reliability against coverage.

**Signal Transformation:** Raw signals must become structured observations. Includes compression (stripping presentational noise), tokenization (converting to model format), and filtering (keeping only relevant elements).

**Confidence Assessment:** Every observation carries a confidence score. Factors include: A11Y compliance of target site, signal completeness, temporal freshness, modality-task match, and cross-modal agreement.

### 9. Economics

From arXiv 2511.19477v1 (production benchmark on GPT-5.1):
- Per-step average: 8,958 tokens, $0.0048, 6.8 seconds
- Cache hit rate: 74.9% of input tokens served from cache
- Total for 30 reasoning steps: $0.1454

Without caching (>70% hit rate), browser agent economics are unsustainable at scale. Caching is not an optimization — it is the business model.

**Cost optimization levers:** Intelligent trimming (~57% total cost reduction despite 34% more tool calls), model routing (85% budget / 10% balanced / 5% frontier = ~92% savings), perception caching (Stagehand v3 achieves 44% speedup on cached paths).

---

## Module B — Operations & Implementations

### 10. Failure Modes

**AXTree Failures:**
- Missing ARIA labels (developers omit `aria-label`, `role`) → Fall back to vision for that element
- Dynamic content not exposed (SPAs update DOM without updating AXTree) → Refresh AXTree; use network interception
- Custom widgets (canvas, SVG, custom controls) → No AXTree representation; vision mandatory
- WCAG non-compliance → AXTree confusing or incomplete; trust hybrid pattern

**Vision Failures:**
- OCR errors (text too small, blurry, rotated) → Low confidence; use AXTree as primary
- Coordinate hallucination (model guesses wrong click position) → Re-perceive with higher resolution
- Context loss (screenshot shows only viewport) → Scroll and re-perceive
- Temporal inconsistency (page changes between perception and action) → Re-perceive immediately before action
- Cost overrun (too many vision steps) → Switch to AXTree where possible

**Hybrid Failures:**
- Fallback cascade (AXTree fails → vision fails → no observation) → Escalate to human; log pattern
- Inconsistent state (AXTree and screenshot show different content) → Use network traffic as tiebreaker
- Latency accumulation (multiple fallbacks add up) → Cache successful paths; pre-fetch common observations

### 11. Security Considerations

**Perception as Attack Surface:**
- Prompt injection via page content (malicious webpage content injected into perception) → Context isolation; instruction quarantine
- Visual adversarial attacks (pixel perturbations confuse vision models) → AXTree primary; multiple vision models for consensus
- AXTree poisoning (malicious ARIA labels mislead agent) → Cross-validate AXTree with DOM structure
- Perception-based data exfiltration (agent reads PII from page) → Governance gates; PII redaction in traces

**WebMCP-Specific Threats:**
- Malicious tool registration → Same-origin boundary; CSP inheritance; `agent.requestUserInteraction()` for sensitive ops
- Misleading tool descriptions → Hash-pin tool definitions; validate descriptions against schema
- Cross-tab tool exposure → Isolation: never co-load exfiltration-capable + untrusted-content-reading tools

[Primary: W3C WebMCP Security Review Draft, Feb 2026]

### 12. Observability

Perception emits spans for every observation: token count, modality used, confidence score, and duration. OpenTelemetry GenAI conventions (`gen_ai.client.operation.duration`, `gen_ai.client.token.usage`) standardize these traces. At production scale, clustering perception failures (e.g., "selector not found" across thousands of runs) reveals systemic problems.

### 13. Production Patterns

**Pattern 1: AXTree-First with Vision Fallback**
```
observation = get_axtree_snapshot()
IF observation.confidence < THRESHOLD:
    observation = take_screenshot_and_analyze()
```
Token cost: 500–1,500 avg/step. Reliability: ~90%+. Used by: Stagehand, Browser Use.

**Pattern 2: Intelligent Trimming**
Lightweight model filters snapshots before full LLM processing. 57% total cost reduction despite 34% more tool calls. [Benchmark: arXiv 2511.19477v1]

**Pattern 3: Perception Caching**
Hash current URL + page structure fingerprint → reuse observation if unchanged. 74.9% cache hit rates in production.

### 14. Anti-patterns

1. **Screenshot-only perception** — 10x+ token waste; at 100K tasks/month, vision-only costs $10,000–30,000 in inference alone.
2. **Raw DOM dumping** — 10,000–15,000 tokens/page. No semantic structure. Compressed AXTree achieves same results at 200–400 tokens.
3. **No confidence assessment** — Feeding low-quality observations to the Decision Engine guarantees bad decisions.
4. **Single-modality-for-everything** — 30%+ of production sites have poor A11Y compliance. AXTree alone fails on custom widgets, canvas, non-standard controls.
5. **Perception without temporal awareness** — Pages change. AJAX loads. Stale observations lead to actions on wrong state.

### 15. Current Implementations

**Browser Surface:** Playwright MCP (AXTree), Browser Use (AXTree+Vision, 97% Online-Mind2Web), Stagehand (AXTree-cached + Vision fallback), Skyvern (Vision-first), Claude Computer Use (Vision-only), OpenAI CUA (Hybrid), dev-browser (AXTree+CDP, 30% faster, 40% cheaper than PW MCP).

**Desktop Surface:** Claude Computer Use (Vision+OS AXTree), OpenAI CUA (Vision), SikuliX (Image matching).

**API Surface:** Direct HTTP clients (JSON parsing), GraphQL subscriptions, gRPC streaming, message queues.

---

## Module C — Research & Future

### 16. Research Landscape

| Paper/Standard | Year | Key Finding |
|---|---|---|
| WebVoyager (he et al.) | 2024 | Multimodal browser agent combining screenshots + text; ~59% task success on benchmark |
| Mariner (Google) | 2025 | 83.5% on visual acuity benchmark; hybrid perception (AXTree + vision) |
| Online-Mind2Web (Browser Use) | 2026 | 97% task completion; hybrid perception with intelligent caching |
| Building Browser Agents (arXiv 2511.19477v1) | 2025 | Production cost study: $0.0048/step, 8,958 tokens/step, 6.8s/step; 74.9% cache hit |
| WebMCP Security Review (W3C) | 2026 | Browser-native tool exposure; hash-pin requirements for tool integrity |

**Standards:** WCAG 2.2 (A11Y compliance), OpenTelemetry GenAI (v1.41 draft, standardized perception tracing), WebMCP (W3C Draft, Chrome 149 origin trial).

### 17. Open Questions

1. Why do some sites have excellent AXTrees while others have almost none? Development culture issue? Framework issue? Both?
2. When will WebMCP move from origin trial to stable standard? What incentives do sites have to expose tools vs. fight agents?
3. When AXTree and vision disagree, which wins? Are there cases where a third modality (network, console) should be the tiebreaker?
4. Can we do "low-resolution perception" for quick decisions and "high-resolution" only when needed (IoT/edge use case)?
5. As agents become ubiquitous, will sites deliberately degrade their AXTrees or inject misleading ARIA labels to block automated access?

### 18. Future Evolution

**2026–2027:** WebMCP moves toward W3C Recommendation. AXTree quality improves as frameworks auto-generate better ARIA labels. 70%+ perception cache hit rates become standard.

**2027–2029:** Multi-modal perception is default — agents auto-select modality based on task, site quality, and cost. Perception-as-a-service APIs return optimized observations (compressed, filtered, confidence-scored) for any URL.

**2029+:** WebMCP replaces scraping for compliant sites. Perception becomes invisible — the system handles modality selection transparently. Universal architecture works across browser, desktop, mobile, IoT, and robotics surfaces.

---

## Known Gaps

### Missing Evidence
- Precise WebMCP adoption timeline and incentive analysis for site operators
- Quantitative comparison of AXTree-vs-vision success rates on WCAG-non-compliant production sites
- Longitudinal data on perception cache invalidation frequency in real production systems

### Weak Conclusions
- Confidence thresholds for modality selection lack empirical calibration — the 0.7 threshold used in patterns is a reasonable heuristic, not a measured value
- "30% of sites fail AXTree" is an industry estimate, not a validated benchmark

### Research Required
- Measurement of prompt injection success rates via page content vs. vision-only inputs
- Benchmarking of multi-modal cross-validation overhead vs. single-modality accuracy gains
- Economic analysis of WebMCP tool-registration costs for site operators vs. agent integration savings

### Awaiting Industry Consensus
- Should perception confidence scores be standardized (OpenTelemetry GenAI is working on this)?
- Who maintains AXTree quality metrics — W3C, framework authors, or independent auditors?
- What constitutes a "good" vs "bad" AXTree for agent consumption? No taxonomy exists yet.

---

## Sources

### Primary Sources
- [arXiv 2511.19477v1] "Building Browser Agents: Architecture, Security, and Practical Solutions" — Production cost study
- [W3C WebMCP Draft] "Web Model Context Protocol" — Browser-native tool exposure specification
- [Playwright MCP Docs] Official documentation for Playwright's MCP server and `ariaSnapshot()`
- [Dev.to Runtime Snapshots #16] Sentry/e2llm three-architecture taxonomy with benchmarking

### Engineering Sources
- [Browserbase Engineering Blog] Stagehand caching patterns and performance data
- [Browser Use Docs] Online-Mind2Web benchmark results and hybrid perception approach

### Benchmark Sources
- [WebVoyager Benchmark] Multimodal browser agent task success rates
- [Online-Mind2Web Benchmark] 97% task completion with hybrid perception
- [Google Mariner] 83.5% visual acuity benchmark score

### Community Sources
- [GitHub Issues] Playwright MCP, Browser Use, Stagehand — perception failures and workarounds

---

## Interfaces

### Upstream
- Node 11: Environment State (source of raw signals)
- Nodes 17–22: Execution Surfaces (signal availability per surface)

### Downstream
- Node 02: Decision Engine (receives structured observations + confidence score)

### Reads
- Environment State (current conditions)
- Working Memory (recent observations for context)

### Writes
- Working Memory (current observation stored)
- Long-term Memory (successful perception strategies cached via Learning node)

### Emits
- Structured Observation (text, tokens, embeddings, scalars)
- Confidence Score (0.0–1.0)
- Observation Metadata (timestamp, source surface, token count, cost)

### Consumes
- Raw signals from Execution Surface (pixels, bytes, streams, events)
- Context from Working Memory (previous observations for temporal alignment)
