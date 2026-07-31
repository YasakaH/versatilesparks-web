# Metrics Playbook

## The Only Metric That Matters

**Revenue per article.** Every article is an investment of writing time. If an article generates $0 after 30 days, retire or rewrite it.

## Article-Level Dashboard

| Metric | Where | Calculation |
|--------|-------|-------------|
| Publish date | MANUAL | Date first published |
| Days live | Auto | Today - publish date |
| Views | Dev.to stats, Google Analytics | Total unique visitors |
| Read ratio | Dev.to stats | (Reads / Views) × 100 |
| Book clicks | Gumroad ?ref= tracking | Clicks on article-specific ?ref= link |
| Sales | Gumroad dashboard | Purchases attributed to article ?ref= |
| Revenue | Gumroad dashboard | Sales × book price |
| Writing time | MANUAL | Hours spent researching + writing + editing |
| Revenue/hour | Revenue / Writing time | True ROI |

Track these in a spreadsheet, one row per article, updated weekly.

## Tracking Setup

### Gumroad ?ref= Links
Every article CTA must use a unique `?ref=` parameter:
```
https://gum.co/python-browser-automation-cookbook?ref=5-mistakes-nodriver
```
Gumroad automatically attributes sales to the `?ref` value. Check: Gumroad → Sales → Filter by `?ref=`.

### Dev.to Stats
Dev.to shows views, reads, and read ratio per article. Check: Dashboard → Posts.

### Google Analytics
The static site has no analytics library. Options:
- **Phase 1 (now):** Manual tracking via Gumroad ?ref= only. No GA needed yet.
- **Phase 2 (after 10 articles):** Add Cloudflare Web Analytics (free, no JS, privacy-preserving).
- **Phase 3 (after 20 articles):** Consider Plausible or Fathom ($10-15/mo) if revenue supports it.

## Decision Thresholds

| Metric | Action |
|--------|--------|
| Article $0 after 30 days | Retire or rewrite |
| Revenue/hour < $10 | Stop writing this type of article |
| Read ratio < 20% | Improve hook and opening |
| Read ratio > 60% | Expand — topic has demand |
| Book click rate < 2% | Move CTA higher, make it stronger |
| Book click rate > 10% | Add second CTA mid-article |
| Single article > 50% of revenue | Double down on that concept cluster |

## Content Performance Review

Every 4 weeks:
1. Sort articles by Revenue (descending)
2. Identify top 3 — what do they have in common? (concept, format, title pattern)
3. Identify bottom 3 — what failed?
4. Retire bottom performers (unpublish or rewrite)
5. Plan next 4 weeks based on top patterns

## Cost Tracking

| Activity | Estimated Time |
|----------|---------------|
| Research | 1-2 hours |
| Writing | 2-3 hours |
| Editing | 30-60 min |
| Publishing to all platforms | 15-30 min |
| Weekly metrics update | 15 min |

Track actual time. Revenue/hour after 30 days determines whether the article type is worth continuing.

## Measurement Cadence

| Frequency | Task |
|-----------|------|
| Per publish | Record writing time |
| Weekly | Update article dashboard |
| Monthly | Content performance review |
| Quarterly | Pivot or double-down decision |
