# Article Definition of Done

An article is complete only when ALL of the following hold. This is the gate between "draft" and "done" — no subjective judgment.

## Content

- [ ] Website version exists (`website-next/content/articles/<slug>.mdx`, published: true)
- [ ] Dev.to version exists (draft or live, ID recorded in manifest)
- [ ] Canonical URL set → `https://versatilesparks.qzz.io/blog/<slug>`
- [ ] CTA `?ref=<slug>` parameter present (single CTA, no more)
- [ ] Frontmatter: title, description, date, tags (≤4, alphanumeric), slug, concepts
- [ ] No Selenium/Playwright comparison drift (nodriver-only)
- [ ] Build green (npx next build, 0 errors) + contract tests 71/71

## Distribution

- [ ] X post + thread created (`articles/derivatives/<slug>/`)
- [ ] Reddit discussion created (no link, no CTA)
- [ ] Quora answer created (self-contained, NO links)
- [ ] GitHub asset created IF applicable (pattern doc or gist)
- [ ] Pinterest pins created IF approved (3-visual experiment model)
- [ ] distribution.json exists with all derivative statuses

## Measurement

- [ ] Added to `articles/metrics-baseline.md` (table + immutable fields: article ID, published UTC)
- [ ] Manifest updated: published status, website + devto URLs
- [ ] Published date recorded (Dev.to)
- [ ] Gumroad `?ref=` tracking verified (end-to-end click test)

## Learning (D-026 operating principle)

Every article must teach something measurable. After publication, answer at
least: impressions vs. previous article? CTA clicks? Which derivative platform
drove traffic? Did the GitHub pattern get visits? Did readers reach the book
page? An article that only increases the content count is incomplete — one
that teaches something about the audience or funnel has produced value even
before revenue.

## Rules

- Article #N+1 starts only after Article #N's derivatives are deployed and observed
- Not every platform applies to every article — blocked/deferred platforms (LinkedIn, YouTube) are marked, not skipped silently
- "Done" without a metrics row is not done
