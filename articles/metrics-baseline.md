# Article Metrics Baseline

First article in the live validation phase. Published 2026-07-30.

## 5 Mistakes New nodriver Users Make (and How to Avoid Them)

- **Article ID (Dev.to):** `4271273`
- **Published UTC:** `2026-07-30T17:51:49.908Z`
- **Slug:** `5-mistakes-nodriver-beginners`
- **Dev.to:** https://dev.to/fromyasaka/5-mistakes-new-nodriver-users-make-and-how-to-avoid-them-3dap
- **Website (canonical):** https://versatilesparks.qzz.io/blog/5-mistakes-nodriver-beginners
- **CTA:** https://gum.co/python-browser-automation-cookbook?ref=5-mistakes-nodriver-beginners

| Metric         | Day 0 (2026-07-30) | Day 1 | Day 2 | Day 7 | Day 30 |
| -------------- | ----: | ----: | ----: | ----: | -----: |
| Views          |     0 |       |       |       |        |
| Reads          |       |       |       |       |        |
| Read %         |       |       |       |       |        |
| Reactions      |     0 |       |       |       |        |
| CTA Clicks     |       |       |       |       |        |
| Cookbook Sales |       |       |       |       |        |
| Comments       |     0 |       |       |       |        |
| Search Console impressions | | | | | |
| Search Console clicks | | | | | |

**Derived metrics (computed from raw rows above):**

```text
CTA Conversion %   = CTA Clicks / Views
Sales Conversion % = Sales / CTA Clicks
```

**Source notes:**
- Views/Reactions/Comments: Dev.to API via `python tools/publisher/metrics/collect.py --devto`
- Views source: per-article `page_views_count` (`/articles/me/all`) — API does expose views, currently 0 (no traffic yet)
- Read time: `/analytics/totals` returns `average_read_time_in_seconds` + `total_read_time_in_seconds` — captured in snapshot `sources.devto.account`
- Immutable daily snapshots: `metrics/raw/YYYY-MM-DD.json` (never overwritten without `--force`); source-scoped layout: `{date, collected_at, sources: {devto: {account, articles}, ...}}`
- Each snapshot emits FeedbackRecords to `knowledge/feedback/` (signal_type `metrics_snapshot`)
- Day 0 row recorded from first snapshot `metrics/raw/2026-07-31.json` (published the prior day)
- Legacy article discovered: #4243839 "Why Selenium Died..." (published 2026-07-27) also tracked
- CTA Clicks: Gumroad analytics (referrer `?ref=5-mistakes-nodriver-beginners`)
- Cookbook Sales: Gumroad
- Search Console: Google Search Console, site `versatilesparks.qzz.io`

**Rule:** baseline only. Do not optimize content until multiple articles are published and compared.

## Why Your nodriver Browser Profiles Break (and How to Fix Them)

- **Article ID (Dev.to):** `4282020`
- **Published UTC:** 2026-07-31 (published live after draft review)
- **Slug:** `why-browser-profiles-break`
- **Dev.to:** https://dev.to/fromyasaka/why-your-nodriver-browser-profiles-break-and-how-to-fix-them-521c
- **Website (canonical):** https://versatilesparks.qzz.io/blog/why-browser-profiles-break
- **CTA:** https://gum.co/python-browser-automation-cookbook?ref=why-browser-profiles-break

| Metric         | Day 0 (2026-07-31) | Day 1 | Day 2 | Day 7 | Day 30 |
| -------------- | ----: | ----: | ----: | ----: | -----: |
| Views          |     0 |       |       |       |        |
| Reads          |       |       |       |       |        |
| Read %         |       |       |       |       |        |
| Reactions      |     0 |       |       |       |        |
| CTA Clicks     |       |       |       |       |        |
| Cookbook Sales |       |       |       |       |        |
| Comments       |     0 |       |       |       |        |
| Search Console impressions | | | | | |
| Search Console clicks | | | | | |

Day-0 row will be captured by the next `collect.py --devto` run.
