# Manifesto v0.1 → Evidence Mapping — Updated

> **Date:** 2026-07-23  
> **Purpose:** Track evidence coverage for every factual claim in the manifesto. Indicates which gaps have been filled and which remain.

---

## Claims Status

### Chapter 1: The Missing Discipline

| Claim | Status | Source | Notes |
|---|---|---|---|
| "Hybrid perception is the production default" | ✅ Filled | Playwright MCP docs (compare table), Browser Use benchmark data, Stagehand v3 launch | Official Playwright docs explicitly list hybrid as "Production work — recommended default." |
| "Economics baked into architecture makes agent systems viable at scale" | ✅ Filled | arXiv 2511.19477v1, Cache effectiveness doc, Model routing doc | Three independent sources confirm caching + model routing = viability |

### Chapter 2: The Agent Execution Model

| Claim | Status | Source | Notes |
|---|---|---|---|
| "Eight nodes are structural requirements" | 🟡 Partial | Architecture stress-tested (5 packages) | Still no external validation — waiting for reviewer feedback |
| "ReAct practitioners discover verification/recovery/learning after months" | 🟡 Partial | Anecdotal/observation | Needs specific blog posts or conference talks documenting this pattern |

### Chapter 3: Execution Surfaces

| Claim | Status | Source | Notes |
|---|---|---|---|
| "AXTree-primary costs 200-400 tokens; vision costs 1,600+" | ✅ Filled | Playwright MCP docs (claims 3,000-5,000 for full screenshots) | Playwright says 200-400 for snapshots, 3,000-5,000+ for screenshots. Medium reports a single screenshot consuming 232K tokens when taken incorrectly. Range is conservative. |
| "Hybrid achieves ~90%+ reliability" | 🟡 Partial | Browser Use Cloud scores 78% on BU Bench, Stagehand v3 docs claim speedup | Production benchmark results (78% BU Bench) don't directly translate to per-step reliability. Claim is reasonable but needs direct measurement. |
| "Caching provides 70%+ hit rates" | ✅ Filled | Cache effectiveness doc — 74.9% from arXiv 2511.19477v1, Stagehand v3 shows 44% speedup | Strong evidence now exists |
| "Model routing saves 85%+" | ✅ Filled | Model routing doc — 92% savings from 85/10/5 split documented in arXiv 2511.19477v1, Browser Use Cloud results | Strong evidence now exists |

### Chapter 4: Why This Matters

| Claim | Status | Source | Notes |
|---|---|---|---|
| "Every team independently discovers caching cuts costs by 70%" | ✅ Filled | Cache effectiveness doc | Same source chain |
| "Security audits expose vulnerabilities from missing layers" | ✅ Filled | Security incidents doc — Palo Alto, Anthropic, Obsidian, HiddenLayer, OpenAI | Very strong evidence. Agents move 16× more data than humans; 17.8% prompt injection success without safeguards. |
| "Mature disciplines provide shared vocabulary" | 🟡 Partial | Abstract claim | Would benefit from ML Ops case study showing knowledge transfer improvement |

---

## New Evidence Files Created

| File | Category | Contains |
|------|----------|----------|
| `benchmarks/perception-costs.md` | Benchmark | AXTree vs vision token counts, production cost study |
| `engineering/cache-effectiveness.md` | Engineering | Stagehand v3, arXiv 2511.19477v1, cache mechanics |
| `engineering/model-routing.md` | Engineering | 85/10/5 budget split, Browser Use benchmark, intelligent trimming |
| `engineering/security-incidents.md` | Engineering | Palo Alto, Anthropic, Obsidian, OpenAI — real-world attacks |

---

## Remaining Critical Gaps

| Gap | Priority | What's Needed |
|-----|----------|--------------|
| Per-step reliability metrics for each perception modality | High | Measured AXTree-only vs vision-only vs hybrid success rates on real tasks |
| WebMCP adoption timeline and site operator incentives | Medium | Industry analysis of why sites would/wouldn't adopt |
| Prompt injection success rate comparisons across modalities | Medium | Published benchmark comparing vision-only vs hybrid injection resistance |

---

*End of Evidence Map Update — Version 0.1*
