# Perception Cost Benchmarks

> **Source:** Evidence compiled from Playwright MCP docs, Medium posts, production benchmarks  
> **Date:** 2026-07-23  
> **Category:** Benchmark  
> **Tiers:** A + C (one D outlier)

---

## AXTree vs Vision Token Costs

### Playwright MCP — Official Comparison (Tier A)

| Metric | Snapshots (AXTree) | Screenshots (Vision) |
|--------|-------------------|---------------------|
| Token cost | ~200–400 tokens | ~3,000–5,000 tokens (vision model) |
| Precision | Exact — refs point to specific elements | Approximate — requires coordinate guessing |
| Speed | Instant — text parsing | Slower — vision model inference |
| Reliability | Deterministic — same structure = same interaction | Variable — layout changes break coordinates |
| Vision model required | No | Yes |

**Observation:** Playwright's official documentation compares AXTree snapshots directly against screenshots across six measurable dimensions. In every dimension, AXTree scores better or equal: lower tokens, exact precision, instant speed, deterministic reliability. The tradeoff is that AXTree only works on accessible UIs.

Source: [Playwright MCP Snapshots docs](https://playwright.dev/mcp/snapshots)

### Real-world screenshot disaster (Tier D)

A single full-page screenshot via Claude MCP at default resolution consumed **232,000 tokens** — more than a 200K context window has room for. The article reports this as an anecdotal finding but provides verifiable methodology (same tooling available to anyone running the Playwright MCP).

This illustrates an important principle: **the token cost of screenshots is highly variable.** On a small login form, a screenshot might cost 3,000 tokens. On a complex dashboard, a full-page screenshot can exceed 100,000 tokens. The average is misleading; the variance is the risk.

Source: [Medium, "One screenshot, 232,000 tokens" (May 2026)](https://medium.com/@7003425114klp/one-screenshot-232-000-tokens-0b37783438c7)

### Hybrid perception average (Tier E inference from Tier A + B)

Production hybrid systems (AXTree primary + vision fallback) report:

| Metric | Value | Assessment |
|--------|-------|-----------|
| Average tokens per step | 500–1,500 | Computed from typical AXTree hit rates (~70%) plus occasional vision fallback |
| Average latency per step | 5–15 seconds | Sum of AXTree fetch (~3-10s) plus occasional vision call (~15-60s) |
| Estimated reliability | ~90%+ | Inference from Stagehand/BU results showing similar figures |
| Fallback rate | ~30% of pages require vision | Industry estimate, not validated benchmark |

Used by: Stagehand, Browser Use, OpenAI CUA (hybrid variant).

---

## Production Benchmark: Full-System Costs (Tier B)

Source: arXiv 2511.19477v1 "Building Browser Agents: Architecture, Security, and Practical Solutions"

| Metric | Value | Notes |
|--------|-------|-------|
| Per-step average tokens | 8,958 | Includes perception + reasoning + action spans |
| Per-step average cost | $0.0048 | Based on GPT-5.1 pricing |
| Per-step average latency | 6.8 seconds | |
| Total for 30 reasoning steps | $0.1454 | |
| Cache hit rate | 74.9% of input tokens served from cache | Measured across production workload |

**Interpretation:** At these numbers, a 30-step task costs less than 15 cents in API calls alone. But the critical insight is the cache hit rate: if cache effectiveness drops below 70%, economics deteriorate rapidly. This suggests caching infrastructure must be treated as core platform, not optional optimization.

---

*End of Perception Cost Benchmarks*
