# Decision Register

Record of irreversible / load-bearing decisions. Append-only. Date each entry.

---

## D-001 — Website is canonical, Dev.to is distribution
**Date:** 2026-07-30
**Decision:** versatilesparks.qzz.io is the canonical source of truth; Dev.to is a distribution channel; every Dev.to article sets canonical_url to the website version.
**Reason:** Dev.to is rented land. The website owns SEO value, email capture, analytics, product funnel, internal links.

## D-002 — No top-of-funnel content
**Date:** 2026-07-30
**Decision:** Only decision-stage content. No generic tutorials, no "what is browser automation" content.
**Reason:** Audience is developers already past discovery; content must map to cookbook buyer intent.

## D-003 — Hashnode Pro not worth it pre-revenue
**Date:** 2026-07-30
**Decision:** No $15/mo Hashnode Pro; API publishing stays placeholder.
**Reason:** Cost without proven conversion.

## D-004 — Infrastructure freeze
**Date:** 2026-07-31
**Decision:** No new infrastructure, abstractions, metadata fields, pipeline stages, or frameworks until production usage reveals real bottlenecks.
**Reason:** Architecture reached the point where it serves the product; remaining work is operational (publish, observe, learn).

## D-005 — Metrics snapshots are immutable
**Date:** 2026-07-31
**Decision:** One file per UTC day in metrics/raw/, never modified after writing; --force for development only.
**Reason:** Without immutability, later analysis is questionable ("did traffic change, or did we rewrite history?").

## D-006 — No derived metrics in raw snapshots
**Date:** 2026-07-31
**Decision:** Raw files store only API-observed values (views, reactions). Derived metrics (CTR, conversion %) computed at analysis time.
**Reason:** Derived metrics can change; raw observations should not.

## D-007 — Source-scoped snapshot layout
**Date:** 2026-07-31
**Decision:** `{sources: {devto: {account, articles}, gumroad: {account, products}, ...}}` — each platform keeps its natural hierarchy instead of being forced into one shape.
**Reason:** Avoids inventing generic top-level fields that become awkward; natural scaling when Gumroad/Search Console/GitHub land.

## D-008 — Metrics collectors are not scheduled
**Date:** 2026-07-31
**Decision:** Run collect.py manually; no Windows Task Scheduler until 3-5 articles published or multiple data sources.
**Reason:** Schema is still evolving in the pilot week; automation of an evolving process creates churn.

## D-009 — Do not optimize on one article's data
**Date:** 2026-07-31
**Decision:** No content strategy changes until several articles are published and compared.
**Reason:** 100 views and 5000 views are both single data points; resist overfitting.

## D-010 — GitHub is discovery layer, not sales page
**Date:** 2026-07-31
**Decision:** Free GitHub assets (repo + gists) contain patterns/checklists/examples only; README uses a soft "Related" section, not a CTA.
**Reason:** Developers distrust promotional repos; the repo itself builds trust. Complete implementations stay in the paid cookbook.

## D-011 — Free/paid content boundary
**Date:** 2026-07-31
**Decision:** Free (GitHub): concepts, patterns, checklists, small examples, gists. Paid (cookbook): complete 30 recipes, project scaffold, utility library, Docker templates, debugging workflows, case studies.
**Reason:** The repo should create desire, not replace the book.

## D-012 — Quora: no links
**Date:** 2026-07-31
**Decision:** Quora answers are fully self-contained; never append URLs (policy since 2024).
**Reason:** Quora restricts links; violation risks answers being suppressed.

## D-013 — Reddit: discussion first, no CTA
**Date:** 2026-07-31
**Decision:** Reddit posts are discussion questions; no book mention, no initial link, no CTA.
**Reason:** Reddit hates marketing; the answer itself must stand alone; link only after engagement.

## D-014 — LinkedIn and YouTube blocked
**Date:** 2026-07-31
**Decision:** LinkedIn = blocked (account banned). YouTube = deferred (channel not created). Derivatives stay on disk; manifests mark status.
**Reason:** Platform reality, not choice. Revisit only if the ban lifts or a channel is created.

## D-015 — Checklist is not email-gated (yet)
**Date:** 2026-07-31
**Decision:** The nodriver Production Checklist distributes openly (Pinterest → checklist page → cookbook CTA). Email gating deferred until traffic exists.
**Reason:** Not enough traffic to optimize email; gate later when conversion data exists.

## D-016 — No paid ads before conversion is proven
**Date:** 2026-07-31
**Decision:** No paid advertising until the organic funnel shows measurable clicks and sales.
**Reason:** Ads amplify a funnel that hasn't proven it converts.

## D-017 — Article #3 title/angle
**Date:** 2026-07-31
**Decision:** Article #3 = "Why Your nodriver Session Dies Overnight (and How Production Systems Prevent It)" — pain pattern continuation (beginner mistakes → profile failures → session failures).
**Reason:** Keeps the "problem → nodriver → cookbook" boundary; not a tutorial title.

## D-018 — No aggressive promotion anywhere
**Date:** 2026-07-31
**Decision:** Never "buy my book" posts, no link-dropping in communities, no daily promotional tweets.
**Reason:** Goal is the right 500 developers finding "this person understands my production pain"; aggressive promotion gets accounts ignored, downranked, or banned (see LinkedIn).

## D-019 — Pinterest manual-first; API automation deferred
**Date:** 2026-07-31
**Decision:** Do not automate Pinterest publishing before validating Pinterest as a traffic source. Publish first 3 pins manually, observe 30 days.
**Reason:** Current constraint is content validation, not publishing capacity. Manual volume is tiny (<1 hr/month at 12-24 pins/month); an API adapter (Pinterest API v5, requires developer app + Standard access approval + OAuth PKCE) saves almost nothing and violates the infra freeze.
**Trigger to revisit:** >50 pins/month, OR Pinterest becomes top-3 traffic source, OR manual publishing becomes painful. Then: `tools/publisher/adapters/pinterest.py` (same architecture).

## D-020 — Pinterest audience assumption: indirect, not direct
**Date:** 2026-07-31
**Decision:** Pinterest is not a direct developer acquisition channel. Its value is likely indirect: Google Images/Search indexing of diagrams, checklists, and architecture visuals.
**Reason:** Developers do not browse Pinterest; they find indexed visuals via search. The pin's job is to rank the visual, not to sell in the feed.

## D-021 — Funnel integrity gate (not sales gate) for Pinterest
**Date:** 2026-07-31
**Decision:** Pinterest publishing requires funnel integrity, NOT sales: article loads, CTA visible, Gumroad ?ref tracking works, book page exists. Do not wait for first sales — Pinterest may generate them.
**Reason:** Requiring sales before enabling a traffic source that has never been tested is circular.
