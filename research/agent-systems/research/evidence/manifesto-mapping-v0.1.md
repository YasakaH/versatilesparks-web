# Manifesto v0.1 → Evidence Mapping

> **Date:** 2026-07-23  
> **Purpose:** Track every factual claim in the manifesto to its evidence source. Identifies where the evidence library needs supplementation before publication.

---

## Claims Requiring Evidence

### Chapter 1: The Missing Discipline

| Claim | Current Support | Gap | Priority |
|---|---|---|---|
| "Software engineering solved complexity through layered architectures in the 1960s" | General historical knowledge, not cited | Add primary source: Frederick Brooks, _The Mythical Man-Month_ (1975); Parnas on modular design (1972) | Medium |
| "Every production agent system that scales reveals the same gaps" | Anecdotal, from internal experience | Add engineering sources: public postmortems from teams that hit scaling walls with agents | High |
| "Hybrid perception is the production default for serious systems" | asserted, not evidenced | Add: production deployment reports showing hybrid perception adoption rate | Critical |
| "Economics baked into architecture makes agent systems viable at scale" | Logical argument, not data-driven | Add: cost tracking data from production agent deployments (per-step costs, budget model routing savings) | Critical |

### Chapter 2: The Agent Execution Model

| Claim | Current Support | Gap | Priority |
|---|---|---|---|
| "Eight nodes are structural requirements, not optional components" | Derived from architecture stress-testing of 4 completed packages | Add evidence: systems without verification/recovery/learning fail at production scale | Medium |
| "ReAct practitioners discover verification/recovery/learning after months of debugging" | Inferred from field trajectory | Add: specific blog posts, conference talks, or papers documenting this discovery pattern | High |
| "Without structured memory, every step starts from zero" | Logic argument | Add: benchmark showing performance degradation without caching vs with caching | Critical |

### Chapter 3: Execution Surfaces

| Claim | Current Support | Gap | Priority |
|---|---|---|---|
| "Browsers offer the richest signal ecosystem for agent systems" | Asserted by comparison | Add: comparative analysis across surfaces (signal density per surface type) | Low (common knowledge) |
| "AXTree-primary costs 200-400 tokens; vision costs 1,600+" | Specific numbers from practice | Add: actual token counts from measured AXTree snapshots and vision captures | Critical |
| "Hybrid achieves ~90%+ reliability" | Metric cited without source | Add: measured reliability data from hybrid perception deployments | Critical |
| "Caching provides 70%+ hit rates" | Specific metric, no source | Add: cache hit rate data from production browser agent systems | Critical |
| "Model routing saves 85%+ on budget tasks" | Specific metric, no source | Add: cost comparison data for model routing implementations | Critical |

### Chapter 4: Why This Matters

| Claim | Current Support | Gap | Priority |
|---|---|---|---|
| "Phase 1 (Automation): deterministic scripts with LLM assistance" | Historical characterization | Add: survey or analysis of pre-2024 agent tooling evolution | Low |
| "Phase 2 (Agents): unpredictable production, exploding token costs" | Asserted trend | Add: production incident reports, token cost tracking data from 2024-2025 | High |
| "Every team independently learns caching cuts costs by 70%" | Same as Ch3 metric above | Covered by Chapter 3 evidence collection | See above |
| "Security audits expose vulnerabilities from missing architectural layers" | Asserted pattern | Add: public security audit findings from agent deployments | Critical |
| "Mature disciplines provide shared vocabulary, explicit contracts, compounding knowledge" | Abstract claim | Add: case study of discipline adoption in another field (e.g., ML Ops) showing knowledge transfer improvement | Medium |

---

## Evidence Collection Plan

### Critical gaps (must resolve before publishing v0.1):
1. **Token cost measurements** — Measure actual AXTree vs vision token counts. Populate `research/evidence/benchmarks/`.
2. **Cache hit rate data** — Collect from production browser agent deployments. Populate `research/evidence/engineering/`.
3. **Model routing cost savings** — Collect from teams using budget/frontier model split. Populate `research/evidence/engineering/`.
4. **Security incident examples** — Find public reports of agent failures due to missing governance/security. Populate `research/evidence/community/`.
5. **Perception reliability metrics** — Document AXTree-only vs vision-only vs hybrid success rates. Populate `research/evidence/benchmarks/`.

### Medium gaps (should resolve before v1.0):
1. Brooks/Parnas citation for software engineering history.
2. Production agent postmortems demonstrating scaling wall patterns.
3. ML Ops case study showing how discipline formalization improved knowledge transfer.

### Low priority (cosmetic, don't block publication):
1. Phase 1/2 historical characterization.
2. Browser signal richness assertion.

---

*End of Manifesto Evidence Mapping — Version 0.1*
