# Evidence Citation Standard v1.0

> **Status:** Frozen  
> **Date:** 2026-07-22  
> **Purpose:** Uniform format for citing sources across all Research Packages. Ensures every factual claim is traceable to a source with known credibility level.

---

## Inline Citation Format

Every factual claim in Modules A–C ends with an inline tag: `[Type: ID]`

```markdown
The average cost per step is $0.0048 using GPT-5.1 [Benchmark: arxiv/2511.19477v1].
AXTree snapshots use ~93% fewer tokens than raw HTML [Primary: playwright/mcp-docs#ariaSnapshot].
A production team reported 85% budget-model routing [Engineering: browserbase/blog/2025-03-hybrid-perception — vendor-published].
```

**Rules:**
- Every sentence with a factual claim must have at least one citation.
- Sentences with no citations are assumed to be the author's own analysis (not factual claims).
- If a claim spans multiple sources, list all: [Primary: X, Benchmark: Y].
- Vendor-published numbers MUST include `— vendor-published` suffix.

---

## Source IDs (Short Names)

Use these short names in inline citations. The full source detail lives in `research/evidence/`.

| Short Name | Meaning | Type | Example File |
|---|---|---|---|
| `canon/01` | Canon Node reference | Canon | N/A (self-referential) |
| `arxiv/2511.19477v1` | Building Browser Agents paper | Benchmark | `evidence/papers/arxiv/2511.19477v1.md` |
| `w3c/webmcp-draft` | W3C WebMCP Draft | Primary | `evidence/specs/w3c/webmcp-draft.md` |
| `playwright/mcp-docs` | Playwright MCP server docs | Primary | `evidence/specs/playwright/mcp-docs.md` |
| `browserbase/hybrid-perception` | Browserbase engineering blog post | Engineering | `evidence/blogs/browserbase/hybrid-perception.md` |
| `webvoyager/benchmark` | WebVoyager benchmark results | Benchmark | `evidence/benchmarks/webvoyager.md` |
| `github/playwright-mcp` | GitHub issues/discussions | Community | `evidence/community/github/playwright-mcp.md` |

ID conventions:
- **Papers:** `source/type/short-name` (e.g., `arxiv/2511.19477v1`)
- **Specs:** `vendor/doc-short-name` (e.g., `w3c/webmcp-draft`)
- **Blogs:** `vendor/post-slug` (e.g., `browserbase/hybrid-perception`)
- **Benchmarks:** `benchmark-name` or `bench/evaluation-name` (e.g., `webvoyager/benchmark`, `bench/online-mind2web`)
- **Communities:** `platform/repo-or-topic` (e.g., `github/playwright-mcp`, `reddit/r-ai-agents`)

---

## Evidence Repository Layout

All evidence sources live in `research/evidence/`:

```text
research/evidence/
├── papers/             # Peer-reviewed papers, preprints
│   └── arxiv/
│       └── 2511.19477v1.md
├── specs/              # Official API docs, RFCs, standards
│   ├── w3c/
│   │   └── webmcp-draft.md
│   └── playwright/
│       └── mcp-docs.md
├── blogs/              # Engineering posts, vendor whitepapers
│   └── browserbase/
│       └── hybrid-perception.md
├── benchmarks/         # Measured performance data
│   ├── webvoyager.md
│   └── online-mind2web.md
├── community/          # Reddit, HN, Discord, GitHub discussions
│   └── github/
│       └── playwright-mcp.md
└── index.md            # Master catalog of all evidence sources
```

Each evidence file follows a standardized format:

```markdown
# Source Title

## Summary
1-3 paragraphs describing what this source contains and its relevance.

## Key Data Points
- Point 1 with numbers/values
- Point 2 with numbers/values

## Methodology
How the data was collected/produced (if applicable).

## Limitations
What this source does NOT cover. Biases to be aware of.

## Cross-References
Related sources that confirm, contradict, or extend findings.

## Tags
benchmark, cost-analysis, browser-agent, perception, hybrid
```

---

## Source Credibility Matrix

When evaluating whether a source supports a claim in Modules A–C:

| Credibility Tier | Supported Evidence Types | Typical Use |
|---|---|---|
| **Tier 1 (Highest)** | Canon, Primary, Benchmark | Foundational claims, cost models, success rates |
| **Tier 2 (High)** | Engineering (non-vendor), Benchmark | Supporting evidence, implementation patterns |
| **Tier 3 (Medium)** | Engineering (vendor-published) | Plausible claims, requires Tier 1 corroboration for major statements |
| **Tier 4 (Lowest)** | Community, Opinion | Context, emerging concerns, open questions only |

**Rule:** Major architectural claims (e.g., "hybrid perception is the industry default") require at least one Tier 1 or Tier 2 source. Opinions from community discussion cannot stand alone as evidence.

---

*End of Evidence Citation Standard v1.0*
