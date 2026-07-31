# Cache Effectiveness in Browser Agent Perception

> **Source:** Stagehand v3, arXiv 2511.19477v1, browser agent benchmark data  
> **Date:** 2026-07-23  
> **Category:** Engineering

---

## Production Cache Hit Rates

| System | Cache Hit Rate | Notes |
|--------|---------------|-------|
| Production benchmark (arXiv 2511.19477v1) | **74.9%** of input tokens served from cache | Based on GPT-5.1 production workload |
| Stagehand v3 | **44% speedup** on cached paths | Automatic caching of discovered elements and actions |
| Browser Use | Caching used in production pipeline | Part of hybrid perception approach contributing to 97% Online-Mind2Web score |

Source: [arXiv 2511.19477v1](https://arxiv.org/abs/2511.19477), [Stagehand v3 Launch (Browserbase Blog)](https://www.browserbase.com/blog/stagehand-v3)

## How It Works

Perception caching hashes the current URL plus a structural fingerprint of the visible page state. On subsequent visits, it checks whether the cached observation matches the live hash. If they match, the previous observation is reused at near-zero marginal cost.

```javascript
// Stagehand v3 auto-caching example
const stagehand = new Stagehand({
  env: "BROWSERBASE",
  cacheDir: "action-cache", // Enable automatic caching
});

await stagehand.init();
// First run: uses LLM inference and caches
// Subsequent runs: reuses cached action (no LLM cost)
await stagehand.act("Click the sign in button");
```

## Why Cache Hit Rates Are So High

Many browser tasks involve revisiting the same pages repeatedly:
- Dashboards with stable layouts
- Multi-step forms where previous pages are revisited for verification
- Configuration screens that don't change between agent sessions

When a page structure hasn't changed, re-perceiving it costs nothing beyond verifying the hash matches. The cached observation carries all the semantic structure (AXTree refs, labels, states) without requiring any model call.

## Cost Impact

Without caching (>70% hit rate), browser agent economics are unsustainable at scale. For a typical production deployment processing 100K+ tasks/month:

- **With 74.9% cache hit rate:** ~$500/month in perception-related inference
- **Without caching:** ~$2,000–3,000/month in perception-related inference alone

Caching is not an optimization — it is the business model of production browser agents.

---

*End of Cache Effectiveness Data*
