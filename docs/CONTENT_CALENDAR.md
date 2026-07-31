# Content Calendar

What publishes when. Prevents production drift. Update as articles move through the pipeline.

## Cadence (target)

- 1 article per 1-2 weeks (quality over velocity)
- Derivatives within 3 days of article publish
- Metrics review weekly (collect.py --devto)

## August 2026

### Week 1 (Aug 3-9)

**Article #3:** "Why Your nodriver Session Dies Overnight (and How Production Systems Prevent It)"
- Brief status: not written yet (article #3)
- Pain pattern: session failures (continuation of beginner → profiles → sessions funnel)

**Derivatives (after publish):**
- X thread
- X single post
- Reddit discussion
- Quora answer (self-contained)
- GitHub pattern doc (session recovery / re-authentication)
- Pinterest pins + infographic
- distribution.json update

**Parallel:**
- Submit sitemap to Google Search Console
- Verify Gumroad `?ref=` attribution end-to-end
- Publish article #1 + #2 derivatives (X, Reddit, Quora) if not done in July

### Week 2 (Aug 10-16)

**Article #4:** TBD from briefs (options: downloads-fail, browser-crashes)
- Score with ARTICLE_SCORECARD.md before committing

### Week 3 (Aug 17-23)

**Article #5:** TBD

### Week 4 (Aug 24-30)

- First metrics review against baseline:
  - impressions, clicks (Search Console)
  - views, reads, reactions (Dev.to)
  - CTA clicks, sales (Gumroad)
- Decide: iterate on topics, CTA, or cadence

## Queue (from HPF briefs, cycle-005)

1. automation-detection-signals — What Automation Detection Looks Like in 2026 (intermediate, 2200w)
2. fresh-vs-persistent-profiles — Fresh vs Persistent Browser Profiles (beginner, 1500w)
3. browser-fingerprint-primer — How Browser Fingerprinting Works (beginner, 2000w)
4. anti-detection-strategy-guide — Anti-Detection Strategy (advanced, 3000w)

## Rules

- Article #3 must follow the pain-pattern title, not a tutorial title
- Do NOT write the next article until current derivatives are deployed and observed
- Score every proposed article with ARTICLE_SCORECARD.md before writing
- No article without: canonical website MDX, Dev.to version, ?ref CTA, derivative folder
- Pinterest visuals only after website conversion is verified (CTA, book page, Gumroad tracking)
