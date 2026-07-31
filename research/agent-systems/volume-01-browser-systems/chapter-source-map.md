# Volume I — Chapter Source Map

> **Date:** 2026-07-23  
> **Purpose:** Publishing dependency graph for Agent Systems Engineering — Volume I: Browser Systems.  
> Shows which chapters are ready to draft, which need package development, and which synthesize from manifesto layers.

---

## Package → Chapter Mapping

| Chapter | Title | Source Package | Status | Notes |
|---|---|---|---|---|
| Ch 1 | The Browser as a Hostile Environment | None (framing) | ✅ Ready | Introductory chapter, no package required |
| Ch 2 | The Execution Model Applied to Browsers | All core nodes | ✅ Ready | Synthesizes the eight-node loop |
| Ch 3 | Six Layers for Browser Agents | Manifesto layers | ✅ Ready | Cross-cutting concerns, no packages |
| **Ch 4** | **Perception Architectures for Browsers** | **Node 01** | **✅ Sources complete** | **Highest-fidelity translation test** |
| **Ch 5** | **Decision Making in Uncertain Environments** | **Node 02** | **🟡 Draft ready** | **Uses Node 02 foundations + new evidence** |
| Ch 6 | Planning Browser Workflows | Node 03 | ✅ Sources complete | |
| Ch 7 | Scheduling Browser Actions | Node 04 | ✅ Sources complete | |
| **Ch 8** | **Executing Browser Actions** | **Node 05** | **❌ Missing** | **Must be written** |
| **Ch 9** | **Verifying Browser Outcomes** | **Node 06** | **❌ Missing** | **Must be written** |
| Ch 10 | Recovery Strategies for Browser Failures | Manifesto layers (Recovery) | 📝 Synthesis | No dedicated package yet |
| Ch 11 | Learning from Browser Experience | Manifesto layers (Memory/Learning) | 📝 Synthesis | No dedicated package yet |
| Ch 12 | Economics at Browser Scale | Manifesto layer (Economics) | 📝 Synthesis | No dedicated package yet |
| Ch 13 | Security & Governance for Browser Agents | Manifesto layers (Security + Governance) | 📝 Synthesis | No dedicated package yet |
| Ch 14 | Building Production Browser Agent Systems | Manifesto Ch 5 (Why This Matters) | 📝 Synthesis | Final synthesis chapter |

---

## Priority Path (Critical Dependencies)

```
Ch4 (Node 01) ✅
  ↓
Ch5 (Node 02) ⚠️ ← expand foundations with browser evidence
  ↓
Ch6 (Node 03) ✅
  ↓
Ch7 (Node 04) ✅
  ↓
Ch8 (Node 05) ❌ ← must write full package
  ↓
Ch9 (Node 06) ❌ ← must write full package
  ↓
Ch10-Ch14 → synthesis from manifesto layers
```

**Total packages needing work for Volume I:** 3 (Nodes 02-expanded, 05-full, 06-full)  
**Total packages sufficient as-is:** 3 (Nodes 01, 03, 04)  
**Total synthesis chapters (no packages):** 5 (Chapters 10-14)

---

## Publishing Principle

> **Packages never become chapters.**  
> Packages answer research questions. Chapters answer reader questions.

Every chapter will be written fresh using package material as source, not as outline. The transformation pipeline is:

```
Reference Package (what is X?)
    ↓ transform
Engineering Narrative (why does X fail at scale?)
    ↓ compile
Book Chapter (how do you build X that survives production?)
```

---

*End of Chapter Source Map — Version 0.1*
