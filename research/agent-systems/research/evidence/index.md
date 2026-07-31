# Global Evidence Index

> **Status:** Active  
> **Date:** 2026-07-23  
> **Purpose:** Master catalog of all evidence sources across all packages. Enables deduplication measurement and cross-reference tracing.

---

## Legend

| Column | Meaning |
|---|---|
| ID | Short citation identifier (used in `[Type: ID]` inline citations) |
| Type | Canon / Primary / Engineering / Benchmark / Community / Opinion |
| Title | Source title |
| Packages | Which nodes currently cite this source |
| Location | File path in `research/evidence/` |

---

## Catalog

| ID | Type | Title | Packages | Location |
|---|---|---|---|---|
| `canon/01` | Canon | Node 01: Perception definition | 01 | N/A (self-referential) |
| `w3c/webmcp-draft` | Primary | Web Model Context Protocol (W3C Draft) | 01, 05 | `specs/w3c/webmcp-draft.md` |
| `arxiv/2511.19477v1` | Benchmark | Building Browser Agents — production cost study | 01, 02, manifesto | `papers/arxiv/2511.19477v1.md` |
| `playwright/mcp-docs` | Primary | Playwright MCP server docs + `ariaSnapshot()` | 01, 02, manifest | `specs/playwright/mcp-docs.md` |
| `browserbase/hybrid-perception` | Engineering | Stagehand caching patterns and performance data | 01, 02 | `blogs/browserbase/hybrid-perception.md` |
| `webvoyager/benchmark` | Benchmark | WebVoyager multimodal browser agent benchmark | 01 | `benchmarks/webvoyager.md` |
| `online-mind2web/benchmark` | Benchmark | Browser Use Online-Mind2Web results | 01, 02 | `benchmarks/online-mind2web.md` |
| `mariner/google` | Benchmark | Google Mariner visual acuity benchmark | 01 | `benchmarks/mariner.md` |
| `medium/one-screenshot-232k` | Engineering | Single screenshot consumed 232K tokens | manifesto, Ch 4 | `engineering/perception-costs.md` |
| `paloalto/IDPI-2026` | Engineering | Web-based indirect prompt injection observed in wild | manifesto, Ch 5 | `engineering/security-incidents.md` |
| `anthropic/claude-opus-injection` | Engineering | Claude Opus 4.5 injection rate: 17.8% → 1% with safeguards | manifesto, Ch 5 | `engineering/security-incidents.md` |
| `obsidian/prompt-injection-stats` | Engineering | Agents move 16× more data than humans | Ch 5 | `engineering/security-incidents.md` |
| `openrouter/routing-benchmarks` | Benchmark | Dynamic model selection benchmarks | Ch 5 | `engineering/model-routing.md` |
| `browseruse/bu-bench-v1` | Benchmark | BU Bench V1: 100 hard tasks, bu-ultra 78% | Ch 4, Ch 5 | `engineering/model-routing.md` |
| `stagehand/v3-launch` | Engineering | Stagehand v3: auto-caching, context builder, 44% speedup | Ch 4, Ch 5 | `engineering/cache-effectiveness.md` |

---

## Usage Statistics

| Metric | Value |
|---|---|
| Total indexed sources | 15 (was 8) |
| Sources cited by ≥2 packages/chapters | 4 (arXiv 2511.19477v1, Playwright MCP, Online-Mind2Web, Stagehand v3) |
| Sources cited by ≥3 packages/chapters | 2 (arXiv 2511.19477v1, Playwright MCP) |
| Package coverage avg | 2.0 sources/package |
| Manifesto claims filled by evidence | 6 of 13 critical gaps (from 7 to 2 remaining) |

---

## Evidence Files Created This Sprint

| File | Category | Used By |
|------|----------|---------|
| `benchmarks/perception-costs.md` | Benchmark | Chapter 4, manifesto mapping |
| `engineering/cache-effectiveness.md` | Engineering | Chapter 4, manifesto mapping |
| `engineering/model-routing.md` | Engineering | Chapter 4, Chapter 5, manifesto mapping |
| `engineering/security-incidents.md` | Engineering | Chapter 5, manifesto mapping |

---

*End of Global Evidence Index*
