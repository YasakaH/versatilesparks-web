# Model Routing and Budget Awareness

> **Source:** arXiv 2511.19477v1, Browser Use benchmark, industry research  
> **Date:** 2026-07-23  
> **Category:** Engineering

---

## The Architecture of Economic Awareness

Production browser agents do not treat all tasks equally. They route different parts of their pipeline to different model tiers based on task complexity and risk:

### Typical Budget Allocation

| Tier | % of Tasks | Model Type | Cost Profile | Examples |
|------|-----------|------------|-------------|----------|
| Budget | ~85% | $0.0002–$0.001/token | Near-zero per call | Simple navigation, form filling, AXTree reads |
| Balanced | ~10% | $0.01–$0.03/token | Moderate per call | Ambiguous UI decisions, multi-step reasoning |
| Frontier | ~5% | $0.03–$0.10+/token | Expensive per call | CAPTCHA solving, novel page types, high-risk actions |

This tiered approach yields approximately **92% savings** over using frontier models for everything.

Source: [arXiv 2511.19477v1](https://arxiv.org/abs/2511.19477), [OpenRouter routing benchmarks](https://openrouter.ai/routing/benchmarks)

## Production Results

### Browser Use Cloud Performance

Browser Use Cloud (bu-ultra) achieved **78% success rate** on BU Bench V1 (100 hard browser tasks), significantly outperforming open-source alternatives running at comparable cost:

| Model | Score | Notes |
|-------|-------|-------|
| claude-fable-5 (open source) | 80.0% | $580.87 per 100-task run |
| Browser Use Cloud (bu-ultra) | 78.0% | Fully managed infrastructure |
| ChatBrowserUse-2 (cloud LLM + OSS library) | 63.3% | Purpose-built for browser automation |
| claude-opus-4-6 | 62.0% | Standalone open-source model |
| gemini-3-1-pro | 59.3% | Standalone open-source model |
| claude-sonnet-4-6 | 59.0% | Standalone open-source model |
| gpt-5 | 52.4% | Standalone open-source model |

Source: [Browser Agent Benchmark (browser-use.com, Jan 2026)](https://browser-use.com/posts/ai-browser-agent-benchmark)

Key insight: The 16-point gap between Browser Use Cloud and the best open-source model comes from full-stack optimization (stealth proxies, CAPTCHA solving, persistent filesystem, optimized tool orchestration) — not just a better LLM. This demonstrates that **architecture matters more than model choice** at production scale.

Throughput comparison: Browser Use Cloud runs ~14 tasks/hour, compared to GPT-5 at ~6 tasks/hour. Each step is slower with a smaller LLM, but fewer total steps are needed because the agent doesn't get confused by poor perception.

## Intelligent Trimming

Before feeding an observation to the Decision Engine, a lightweight model strips irrelevant DOM elements, collapses expandable sections, removes hidden/out-of-viewport content, and keeps only what's semantically relevant to the current task.

Counterintuitive finding: trimming actually increases tool calls by **34%** (because more granular observations lead to more targeted decisions), but total cost drops by **57%** because trimmed observations carry dramatically fewer tokens per call.

Source: [arXiv 2511.19477v1](https://arxiv.org/abs/2511.19477)

## OpenRouter Routing Benchmarks

OpenRouter provides routing benchmarks across model providers, showing how model selection directly impacts task cost and latency:

- Smaller models (e.g., Qwen, Mistral variants) handle straightforward classification/navigation at fractions of the cost of frontier models
- Larger models (Claude Opus, GPT-5) provide marginal gains on simple tasks but significant advantages on complex reasoning
- The optimal strategy is dynamic: use smallest capable model for each subtask

---

*End of Model Routing Data*
