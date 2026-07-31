# Evidence Tier Classification Guide

> **Status:** Active  
> **Date:** 2026-07-23  
> **Purpose:** Standardize evidence classification so every quantitative claim carries a confidence label readers can immediately interpret.

---

## Tiers

| Tier | Label | Source Type | Examples |
|------|-------|-------------|----------|
| A | Standard / Peer-reviewed | Formal standards, peer-reviewed papers, RFCs, W3C drafts, government reports | W3C WebMCP Draft, NIST publications, arXiv papers with methodology sections |
| B | Engineering Data | Reproducible engineering measurements, production benchmarks from independent parties | Browser Use BU Bench V1 (open source benchmark suite), Skyvern WebBench |
| C | Vendor Claims | Benchmarks or data published by the vendor who has incentive to look good | "Browser Use Cloud leads at 78%," Stagehand "44% speedup" (single-vendor) |
| D | Anecdotal Reports | Blog posts, Medium articles, conference talks without reproducible methodology | "One screenshot, 232K tokens" Medium post, LinkedIn posts |
| E | Author Inference | Conclusions drawn by the framework authors from observed data | "Caching is not an optimization — it is the business model" |

## Claim Annotation Format

Every quantitative claim should carry a tier annotation:

```markdown
**Claim:** Hybrid perception achieves ~90%+ reliability.

Evidence:
- Tier B: Browser Use Cloud scores 78% on 100-hard-task benchmark (BU Bench V1)
- Tier C: Stagehand v3 launch claims 44% speedup on cached paths
- Tier E: Authors infer 90%+ from observation that hybrid systems dominate production

Assessment: Moderate confidence. The 90% figure is inference grounded in Tier B and C sources.
Would benefit from Tier A or B data measuring per-step reliability across modalities.
```

```markdown
**Claim:** AXTree costs 200-400 tokens; screenshots cost 3,000-5,000+.

Evidence:
- Tier A: Playwright MCP documentation (official)

Assessment: High confidence. Direct from official specification.
```

```markdown
**Claim:** Prompt injection success rate drops from 17.8% to ~1% with safeguards.

Evidence:
- Tier A: Anthropic Claude Opus 4.5 system card (quantified claim)

Assessment: High confidence. From model vendor's own research.
```

## Production Rule

Before including any quantitative claim in the manifesto, books, talks, or articles:

1. **Assign a tier** to every source supporting the claim.
2. **Never cite a single Tier C source** as primary evidence for a significant claim. Cross-reference with at least one Tier B or A.
3. **Always separate Observation from Interpretation.** Observations are what the data shows. Interpretations are what we think it means. Reviewers can challenge interpretations without being accused of misunderstanding facts.

---

*End of Evidence Tier Classification Guide*
