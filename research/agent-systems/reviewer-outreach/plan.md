# Reviewer Outreach Plan — Manifesto v0.1

> **Date:** 2026-07-23  
> **Purpose:** Structured reviewer recruitment and feedback collection for The Agent Execution Model v0.1.

---

## Philosophy

Choose reviewers deliberately for diversity of perspective, not agreement. Five reviewers minimum. Each gets the same three questions to ensure comparable feedback.

## Selection Criteria

| Role | Why this perspective | What they'll challenge |
|---|---|---|
| Distributed systems engineer | Understands complex state machines, non-determinism, failure handling | Will test whether the eight-node loop maps to real distributed systems thinking |
| Browser automation engineer | Deep practical experience with AXTree, Playwright, Puppeteer | Will test whether the browser surface treatment matches production reality |
| AI infrastructure engineer | Builds tool-calling frameworks, model routing, observability | Will test whether the economics/observability layers are grounded or hand-wavy |
| Staff-level backend engineer | Thinks in architectures, has shipped production systems | Will test whether the proposal feels like a real discipline or just naming |
| Engineering manager / architect | Cares about team knowledge transfer, scaling, technical debt | Will test whether "shared vocabulary" and "compounding knowledge" resonate practically |

Do NOT select:
- People who already work on your project
- People hired to say "this is great"
- Beginners (they lack the comparison point to evaluate the framework)

## The Three Questions

Every reviewer gets exactly these three questions. No open-ended "what do you think?"

1. **What idea was most memorable?**  
   If they can't name one thing, the manifesto failed the Whiteboard test.

2. **Where did you stop believing the argument?**  
   This finds weak evidence, overreaching claims, and logical gaps before they reach public eyes.

3. **What important concept do you think is missing?**  
   This catches blind spots that the author couldn't see. If five people all say the same thing is missing, it needs to be addressed.

## Outreach Template

> Subject: I'd value your perspective on a technical proposal  
> 
> Hi [Name],  
> 
> I'm working on a framework for how engineers should think about autonomous agent systems at an architectural level — not a tutorial, not a product review, but a proposed structure for treating agent development as an engineering discipline rather than ad-hoc scripting.  
> 
> It's roughly 2,800 words. I'd appreciate your perspective as someone who [specific reason relevant to their expertise].  
> 
> I'm looking for three things:
> 1. What idea stuck with you after reading?
> 2. Where did you stop believing me? (This is the most valuable question.)
> 3. What am I missing?  
> 
> [Link to manifesto v0.1]  
> 
> No need to write anything formal — bullet points or voice notes are fine. I'm targeting [date] for responses so I can iterate before publication. Thanks for considering it.

## Feedback Processing

After collecting all responses:

1. **Group by theme** — what did multiple reviewers say? (Pattern = real issue, not outlier noise)
2. **Categorize by type** — factual correction vs. framing suggestion vs. missing context
3. **Determine action** — each finding gets one of three labels:
   - `fix` — factual error or clear miscommunication
   - `refine` — argument needs strengthening but is directionally correct
   - `defer` — valid point but belongs in Volume I, not the manifesto
4. **Generate manifesto v0.2 changelog** — document all changes from reviewer feedback

## Tracking Sheet

| Reviewer | Role | Sent Date | Response Date | Memorable Idea? | Belief Gap | Missing Concept | Action Taken |
|---|---|---|---|---|---|---|---|
| TBD | Distributed systems | | | | | | |
| TBD | Browser automation | | | | | | |
| TBD | AI infrastructure | | | | | | |
| TBD | Backend staff engineer | | | | | | |
| TBD | Engineering manager | | | | | | |

---

*End of Reviewer Outreach Plan — Version 0.1*
