# Agent Systems Engineering — Volume I: Browser Systems

## Architecture Design Document

> **Version:** 0.1 (Draft)  
> **Date:** 2026-07-23  
> **Status:** Design review in progress  
> **Audience:** Engineers building production browser agents who want architectural depth, not surface-level tutorials

---

## 1. Audience

**Primary audience:** Experienced software engineers (3+ years production experience) who are currently building or evaluating browser-based AI agent systems and have hit the scaling wall — token costs, reliability gaps, security concerns, debuggability problems. They can already make simple agents work. They need a framework to make them work at scale.

This is NOT for:
- Beginners learning what LLMs are
- Product managers evaluating tools
- Security auditors looking for compliance checklists
- Researchers writing papers

These audiences exist, but they're not this book. This book is for engineers who have the tooling fundamentals down and need the architectural discipline to go next.

## 2. Promise

> **Learn how to engineer browser agents as production systems rather than automation scripts.**

Every chapter serves this promise. If a section doesn't help an engineer move from "script" to "system," it belongs elsewhere.

## 3. Relationship to the Manifesto

The manifesto proposes Agent Systems Engineering as a discipline with eight nodes and six layers. Volume I takes that abstract architecture and grounds it in the single most data-rich execution surface: the browser. 

Readers who finish the manifesto will understand WHY the architecture exists. Readers who finish Volume I will understand HOW it works in practice on browsers. The manifesto provides the mental model; Volume I provides the implementation patterns, evidence, and gotchas.

They reinforce each other: the manifesto convinces readers the discipline matters, Volume I shows them the discipline works.

## 4. Chapter Structure

### Part I: Foundations

**Chapter 1: The Browser as a hostile environment**
Why browser automation is fundamentally different from API automation or CLI scripting. The browser contains active adversaries (anti-bot systems, prompt injection through page content), unpredictable state changes, dynamic content, and heterogeneous accessibility. This chapter establishes WHY browser agents need discipline instead of ad-hoc solutions.

Maps to manifesto Chapter 1 (the missing discipline) + manifesto Chapter 3 (browser surface deep-dive).

No reference package needed — this is the introductory framing chapter.

**Chapter 2: The Execution Model applied to browsers**
Introduce the eight-node loop specifically for browser contexts. Each node gets one section describing its role in a browser agent system, its inputs/outputs, and typical failure modes. This is the map chapter — readers see the full territory before diving into details.

Maps to manifesto Chapter 2 (execution model) + reference packages:
- Node 01 (Perception) ✅ complete
- Node 02 (Decision Engine) 📝 foundations only
- Node 03 (Planning) ✅ complete  
- Node 04 (Scheduling) ✅ complete
- Node 05 (Execution) ⏸ empty scaffold
- Node 06 (Verification) ⏸ empty scaffold

Gaps exposed by this mapping:
- **Node 02 (Decision Engine)** — needs expansion beyond foundations for browser context
- **Node 05 (Execution)** — required for browser execution patterns (DOM mutations, event simulation)
- **Node 06 (Verification)** — required for browser verification (page state comparison, success criteria)

**Chapter 3: Six layers for browser agents**
How Memory, Economics, Observability, Security, Governance, and Runtime manifest in browser systems. This chapter makes the abstract concrete — what does "memory" mean when your agent navigates between pages? What does "economics" look like when every AXTree snapshot costs tokens?

Maps to manifesto Chapter 3 (layers). No reference packages directly — these are cross-cutting concerns covered per-surface in each volume.

### Part II: Perception and Decision

**Chapter 4: Perception architectures for browsers**
Deep dive into Node 01 applied to browsers. AXTree reading vs. vision capture vs. hybrid. Signal quality hierarchy (AXTree > WebMCP > Vision > DOM scraping). Confidence scoring for observations. Caching strategies. Cache hit rates and cost optimization.

Maps to: Node 01 (Perception) ✅ — fully complete, primary source.

**Chapter 5: Decision making in uncertain environments**
Deep dive into Node 02 applied to browsers. Model routing by task complexity. Intent classification. Confidence threshold decisions. When to use budget models vs. frontier models. Error diagnosis frameworks.

Maps to: Node 02 (Decision Engine) 📝 — needs expansion from foundations to full Module A/B/C treatment.

### Part III: Planning, Scheduling, and Execution

**Chapter 6: Planning browser workflows**
Deep dive into Node 03 applied to browsers. Decomposing browser tasks into steps. Dependency graphs for page navigation sequences. Failure anticipation for web forms, CAPTCHAs, dynamic loading.

Maps to: Node 03 (Planning) ✅ — fully complete, primary source.

**Chapter 7: Scheduling browser actions**
Deep dive into Node 04 applied to browsers. Concurrency for multi-tab operations. Resource allocation across parallel browser instances. Latency management. Queue management for sequential browser actions.

Maps to: Node 04 (Scheduling) ✅ — fully complete, primary source.

**Chapter 8: Executing browser actions**
Deep dive into Node 05 applied to browsers. Playwright, Puppeteer, Selenium patterns. Event loop interaction. DOM mutation handling. Native action simulation (click, type, navigate, scroll). Timing considerations.

Maps to: Node 05 (Execution) ⏸ — EMPTY. Requires full package development for this chapter.

### Part IV: Verification, Recovery, and Learning

**Chapter 9: Verifying browser outcomes**
Deep dive into Node 06 applied to browsers. Page state comparison. Success criteria for browser tasks. Visual verification vs. structural verification. Handling partial success states.

Maps to: Node 06 (Verification) ⏸ — EMPTY. Requires full package development for this chapter.

**Chapter 10: Recovery strategies for browser failures**
How Recovery handles classified failures. Retry strategies with backoff. Escalation paths. Human-in-the-loop for ambiguous cases. Root cause diagnosis patterns specific to browser contexts.

Maps to manifesto layers (Security, Governance). Node 07 (Recovery) not yet started — may need to be built if browser recovery requires specific treatment.

**Chapter 11: Learning from browser experience**
How Learning improves future browser performance. Pattern caching for common page types. Environmental knowledge indexing. Adaptation to site layout changes. Transfer patterns across similar websites.

Maps to manifesto layers (Memory). No new package needed — this draws from established long-term memory patterns.

### Part V: Production Browser Agents

**Chapter 12: Economics at browser scale**
Token cost breakdown for browser agents. Budget-aware model routing. Caching economics. Cost optimization patterns. When expensive perception pays for itself. Cost accounting frameworks.

Maps to manifesto layer (Economics). Cross-cutting — applies across all browser chapters.

**Chapter 13: Security and governance for browser agents**
Context isolation in browser environments. Prompt injection defenses. Same-origin boundary enforcement. Action approval gates. Audit trails for browser automation. Compliance patterns.

Maps to manifesto layers (Security, Governance). Critical for production deployment.

**Chapter 14: Building production browser agent systems**
Putting it all together. End-to-end architecture for a serious browser agent system. Runtime choices (containerized vs. bare metal). Monitoring setup. Team coordination patterns. Organizing around the execution model. Case studies from production deployments.

Maps to manifesto Chapter 5 (Why this matters). This is the synthesis chapter.

## 5. Package Mapping Summary

| Chapter | Topic | Reference Package | Status | Action Required |
|---|---|---|---|---|
| Ch 1 | Browser as hostile env | N/A | N/A | Introductory framing |
| Ch 2 | Execution Model for browsers | Loop overview | N/A | Synthesizes multiple packages |
| Ch 3 | Six layers for browsers | N/A | N/A | Cross-cutting concerns |
| Ch 4 | Browser Perception | Node 01 ✅ | Complete | Expand with browser-specific evidence |
| Ch 5 | Browser Decision | Node 02 📝 | Needs expansion | Expand from foundations to full draft |
| Ch 6 | Browser Planning | Node 03 ✅ | Complete | Expand with browser-specific evidence |
| Ch 7 | Browser Scheduling | Node 04 ✅ | Complete | Expand with browser-specific evidence |
| Ch 8 | Browser Execution | Node 05 ⏸ | EMPTY | Must write full package |
| Ch 9 | Browser Verification | Node 06 ⏸ | EMPTY | Must write full package |
| Ch 10 | Recovery | Manifesto layers | No package | Synthesis from established patterns |
| Ch 11 | Learning | Manifesto layers | No package | Synthesis from established patterns |
| Ch 12 | Economics | Manifesto layer | No package | Synthesis from established patterns |
| Ch 13 | Security/Governance | Manifesto layers | No package | Synthesis from established patterns |
| Ch 14 | Production systems | Manifesto Chapter 5 | No package | Synthesis chapter |

**Packages requiring development for Volume I:**
1. **Node 02 (Decision Engine)** — expand from foundations to full draft (~27KB → ~30KB)
2. **Node 05 (Execution)** — write from scratch (~27KB estimated)
3. **Node 06 (Verification)** — write from scratch (~27KB estimated)

**Packages sufficient as-is:**
- Node 01 (Perception) ✅
- Node 03 (Planning) ✅
- Node 04 (Scheduling) ✅

## 6. Research Gap Analysis

### Immediate gaps (block chapter writing):
- **Node 05 (Execution)** — Browser event loop interaction, DOM mutation handling, native action patterns. No existing content.
- **Node 06 (Verification)** — Page state comparison, visual vs structural verification, success criteria definition. No existing content.

### Deferred gaps (can synthesize from manifesto + existing packages):
- **Decision Engine browser-specifics** — Node 02 foundations exist; needs browser evidence expansion (not full package rewrite).
- **Browser recovery strategies** — Can draw from existing verification + general recovery principles in manifesto.
- **Browser economics data** — Existing evidence library has some browser data; may need supplementation during writing.

### Design decision needed:
Should Nodes 05 and 06 be written as standalone packages first, or should we begin drafting Chapters 8-9 using the manifesto + available evidence and let the package writing emerge from the book drafting process? 

The manifesto spec says research should be driven by product needs. This suggests: begin writing Chapters 8-9 now, and formalize Nodes 05-06 packages only for material that gets developed in those chapters. This is the "let products drive research" approach.

## 7. Writing Plan

### Phase 1: Package expansion (pre-work)
Write Nodes 02-expanded, 05-full, 06-full using the reference specification. These become the technical foundation for Chapters 5, 8, 9.

OR (alternative): Begin drafting Chapters 4-11 immediately using manifesto + existing packages. Let chapter drafts identify exactly what additional package material is needed. Write missing package material only for what chapters require.

Recommendation: Go with alternative. The "products drive research" principle means starting chapter drafts, not filling the backlog preemptively.

### Phase 2: Chapter drafting (core work)
Draft Chapters 1-14 using manifesto + existing packages + browser-specific research. This runs concurrently with any targeted package expansions.

### Phase 3: Evidence supplementation
Populate `research/evidence/` with browser-specific sources identified during chapter writing. This feeds both the book and the remaining packages.

## 8. Success Criteria

Volume I succeeds when:

1. **An experienced browser automation engineer reads it and says: "I've been doing pieces of this without knowing there was a unified framework."** (Manifesto validation applied to browser surface)
2. **Zero chapters drift into tutorial mode.** Every section serves the promise: production systems, not automation scripts.
3. **A reader can apply the eight-node loop to a new browser task they haven't seen before.** (Framework transferability)
4. **The book demonstrates that the same architecture from the manifesto works concretely on browsers.** (Cross-domain proof)
5. **Readers start saying "this is a verification problem" in their own team discussions.** (Vocabulary adoption)

## 9. External Milestones

| Milestone | Description | Target |
|---|---|---|
| Volume I Architecture Frozen | Audience, promise, chapter structure, mapping, gaps defined | Now ✅ |
| First chapter draft | Chapter 4 (Perception) — uses existing Node 01 package | TBD |
| Node 05 complete | Execution package for browser drafting | TBD |
| Node 06 complete | Verification package for browser drafting | TBD |
| Full chapter drafts | All 14 chapters drafted | TBD |
| Internal review | Read-through by 2-3 engineers outside core project | TBD |
| v0.1 release | Publication-ready volume | TBD |

## 10. Book vs Manifesto Relationship

| Aspect | Manifesto | Volume I |
|---|---|---|
| Purpose | Propose the discipline | Apply it to browsers |
| Scope | All surfaces, all layers | Browser surface only |
| Depth | One mental model | Deep application |
| Tone | Argumentative, persuasive | Technical, instructional |
| Size | ~2,800 words | ~40-60,000 words |
| Audience | Any experienced engineer | Browser automation engineers |
| Format | Essay/proposal | Technical book |
| Citation | Minimal | Heavy (per package spec) |

They are complementary, not redundant. The manifesto answers "why should this exist?" Volume I answers "here's how it works here."

---

*End of Volume I Architecture Design Document — Version 0.1 (Draft)*
