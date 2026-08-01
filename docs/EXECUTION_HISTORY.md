# Publishing System Execution History

> Complete chronological record of every publishing/marketing iteration from Milestone 1 closure onwards. This is not a summary. Preserve decisions, reasoning, files changed, commands executed, failures, corrections, and final state.

---

## Phase 0 — Initial Objective

**Goal:**
- Sell Python Browser Automation Cookbook ($29)
- Generate revenue
- Avoid aggressive promotion / platform bans
- Build organic discovery channels

**Core funnel:**
```
Developer problem
        ↓
Educational content
        ↓
Canonical website
        ↓
Cookbook CTA
        ↓
Purchase
```

**Thread architecture:** HPF (Knowledge OS, separate process) → KnowledgePackage JSON v1.0 → Publishing (this process) → FeedbackRecord → HPF.

**Infrastructure freeze declared:** no new abstractions, metadata fields, pipeline stages, or frameworks until production usage reveals real bottlenecks.

---

## Iteration 1 — Article Pipeline (pre-existing)

**Files:**
```
tools/publisher/
├── publisher.py
├── models.py
├── config.py
├── publish.py
├── consume_handoff.py
├── requirements.txt
└── adapters/
    ├── devto.py
    ├── hashnode.py
    ├── website.py
    ├── github.py
    └── medium.py
```

**Decisions:**
- Publishing abstraction created (Publisher base class)
- Dev.to became the primary live adapter
- Hashnode API publishing requires Pro → placeholder
- Medium adapter exists but MEDIUM_TOKEN not in .env → blocked
- GitHub adapter exists (GitHub Pages / repo publishing)

**Contract system (Milestone 1):**
- KnowledgePackage schema v1.0 (schema_version, producer, producer_version, compatibility, generated_at)
- Quality gate in consume_handoff.py (duplicate briefs, missing concepts, orphan problems, invalid audience, missing CTA, missing root_cause)
- `--strict` mode: warnings → errors in release mode
- 71 contract tests in tests/test_contracts.py
- Manifest inversion: articles/json/manifest.json generated with _meta provenance
- Feedback records: knowledge/feedback/*.json, flat directory, domain_hierarchy in metadata
- Feedback fields: performance {views, reads, book_clicks, sales}, questions[], new_aliases[]

---

## Iteration 2 — Article #1 Creation

**File:** `articles/draft/5-mistakes-nodriver-beginners.md`

**Original angle:** stealth, sessions, proxy, profiles, retry (5 beginner mistakes)

**Corrections applied:**
- Removed aggressive anti-detection claims (softened to "verify and, where appropriate, customise")
- Changed from "nodriver advantage" framing toward production reliability
- Intro strengthened around "nodriver removes Selenium's safety rails" narrative
- CTA strengthened to "survive for days — not minutes" production focus
- Tags fixed for Dev.to: [nodriver, python, webscraping, cdp] (max 4, alphanumeric, no hyphens)

**Final positioning:** Production mistakes new nodriver users encounter.

**Files created:**
- `website-next/content/articles/5-mistakes-nodriver-beginners.mdx`
- `website-next/src/app/blog/[slug]/page.tsx` (SSG route, canonical, OG, JSON-LD, concept links)
- `website-next/src/components/BlogPageClient.tsx`
- compile-content.js extended to load articles (5 categories: concepts, recipes, books, problems, articles)

**Failure encountered:** TypeScript build error — `.find()` returned `(Concept | undefined)[]`, type predicate was wrong. Fixed by typing allConcepts as any[].

---

## Iteration 3 — Dev.to Publishing (Article #1)

**Article ID:** `4271273`

**URL:** https://dev.to/fromyasaka/5-mistakes-new-nodriver-users-make-and-how-to-avoid-them-3dap

**Canonical:** https://versatilesparks.qzz.io/blog/5-mistakes-nodriver-beginners

**Publish flow (learned here):**
1. publish.py with --draft → draft created (ID returned)
2. Verify via `/articles/me/unpublished` endpoint (drafts not visible on `/articles/4271273`)
3. Set `published: true` in frontmatter
4. publish.py --action update --id → goes live
5. Slug changes when publishing (temp-slug → final: `-3dap`)

**Feedback record emitted:** publisher-article_published-*.json

**Metrics Day 0:** Views 0, Reactions 0, Comments 0. Published 2026-07-30T17:51:49Z.

**Decision:** Do not optimize based on one article. Baseline only.

---

## Iteration 4 — Metrics System

**Files created:**
```
metrics/
├── raw/          # immutable daily snapshots
└── METRICS_SCHEMA.md

tools/publisher/metrics/
├── __init__.py
├── collect.py    # CLI: --devto --gumroad --search-console --github --all --force --no-feedback
├── devto.py      # working collector
├── gumroad.py    # stub (needs GUMROAD_TOKEN)
├── search_console.py  # stub (needs GSC credentials)
└── github.py     # stub (needs repo config)
```

**Key decisions:**
- Daily immutable snapshots (one file per UTC day, never overwritten without --force)
- Source-scoped layout (each platform keeps its natural shape)
- No derived metrics in raw files
- Metrics collectors are a separate bounded context (Observation)
- Feedback records: one per article per snapshot (signal_type metrics_snapshot)

**Dev.to API investigation (probe results):**
- `/articles/me/all` returns per-article `page_views_count` (field exists; 0 = no traffic)
- `/analytics/totals` works with API key → page_views, reactions, comments, follows + read time (average_read_time_in_seconds, total_read_time_in_seconds)
- `/analytics/historical` works → per-day breakdown
- Same API key works for all three endpoints → views/reads fully automatable

**Schema evolution (corrected early, cheap):**
- v1: flat {account, articles} → v2: {sources: {devto: {account, articles}}} (one snapshot on disk at the time; regenerated with --force --no-feedback)

**First snapshot:** metrics/raw/2026-07-31.json — discovered legacy article #4243839 ("Why Selenium Died...", published 07-27) also tracked.

**Deferred (not done):** daily scheduling — wait until 3-5 articles or multiple sources. One daily FeedbackRecord per snapshot instead of per-article — switch before article count grows.

---

## Iteration 5 — Article #2

**File:** `articles/draft/why-browser-profiles-break.md`

**Reason:** Follow-up from article #1; establishes production pain authority; beginner → production funnel.

**Target pain:** profile locking, profile corruption, session expiry, state management. Brief from HPF cycle-005.

**Structure:** Hook → profile anatomy → 5 mistakes (profiles-as-folders, shared profiles, no lifecycle, persistent≠permanent, no recovery) → production picture + table → CTA.

**Constraint honored:** no Selenium/Playwright comparison drift; nodriver-specific throughout.

**Word count:** ~1555 (brief target 1800; reviewer: do not expand).

**Corrections applied (reviewer pass, 9.1/10):**
- Title: "Why Browser Profiles Break (and How to Fix It)" → "Why Your nodriver Browser Profiles Break (and How to Fix Them)"
- Added nodriver/CDP ownership sentence in profile anatomy paragraph
- Softened corruption claim ("One common cause...")
- CTA: "the cookbook goes much deeper" → "the Python Browser Automation Cookbook goes deeper into these production patterns"

**Published:** Dev.to ID `4282020`, URL https://dev.to/fromyasaka/why-your-nodriver-browser-profiles-break-and-how-to-fix-them-521c, canonical https://versatilesparks.qzz.io/blog/why-browser-profiles-break, published 2026-07-31. Moved to articles/published/.

**Manifest updated** with published: true + both URLs. Metrics baseline table added per article.

---

## Iteration 6 — Derivative Content System

**Created:** `articles/derivatives/<article-slug>/` per article.

**Structure:**
```
x-post.md            # single pain-observation post
x-thread.md          # multi-tweet thread
reddit.md            # discussion (no link initially)
quora.md             # answer (self-contained)
youtube-script.md    # 30s short script
linkedin.md          # engineering lesson post
github-readme.md     # repo README draft
github-pattern.md    # one pattern doc
pinterest-pins.md    # pin drafts (title + image text + link)
infographic-spec.md  # visual spec
distribution.json    # per-platform publish state + conversion counters
```

**Reason:** One article → multiple discovery surfaces; article is the source asset, each platform gets a communication artifact (not copies).

**Platform mapping decisions:**
- Dev.to: search + technical authority (1 CTA link max)
- Website: conversion layer (canonical owner)
- X: awareness, observation posts, no repeated selling
- Reddit: community trust, discussion only, no CTA, no book mention, no initial link
- Quora: search capture, self-contained answers
- LinkedIn: professional trust — **BLOCKED, account banned**
- YouTube: future discovery — **DEFERRED, channel not created**
- GitHub: developer trust/search
- Pinterest: evergreen visual discovery

**distribution.json:** tracks per-platform status (ready/published/blocked/deferred), dates, URLs, and conversion counters {gumroad_clicks, sales}.

---

## Iteration 7 — Platform Corrections (user feedback)

**LinkedIn:** account banned → status blocked in manifests, PLATFORM_POLICIES.md
**YouTube:** channel not created → status deferred
**Quora:** links NOT allowed (policy since 2024) → answers rewritten to be fully self-contained; manifests + policies updated; never append URL

**PLATFORM_POLICIES.md created** (`articles/derivatives/PLATFORM_POLICIES.md`) — durable table: link policy per platform, active constraints, writing rules. Mandatory check before writing/posting derivatives.

---

## Iteration 8 — GitHub Execution

**Repo created:** https://github.com/YasakaH/nodriver-production-patterns (public, MIT, description "A collection of patterns for building reliable Python browser automation with nodriver")

**Contents:**
```
README.md
LICENSE (MIT)
patterns/
├── browser-profile-management.md
├── retry-with-backoff.md
└── session-health-check.md
checklists/
└── production-readiness.md
```

**Decision:** repo named nodriver-production-patterns over python-browser-automation (too broad; paid product owns that term).

**Correction applied:** README changed from direct CTA to a softer "Related" section (low pressure; GitHub users dislike marketing funnels).

**Free/paid boundary (frozen):**
- Free (GitHub): concepts, patterns, checklists, small examples, gists
- Paid (cookbook): complete 30 recipes, full project scaffold, reusable utility library, Docker deployment templates, debugging workflows, complete case studies

**Commands executed (for reproduction):**
```
gh repo create nodriver-production-patterns --public --description "..." --license MIT
git init -b main && git add -A && git commit
git remote add origin https://github.com/YasakaH/nodriver-production-patterns.git
git push -u origin main   # FAILED: no credentials
git remote set-url origin "https://YasakaH:<PAT>@github.com/..."
git push   # FAILED: non-fast-forward (gh seeded README/LICENSE commit)
git pull --rebase   # FAILED: identity not configured + index changes
git config user.name "YasakaH"; git config user.email "yasakah@users.noreply.github.com"
git push --force-with-lease origin main   # SUCCESS (seed commit replaced)
```

**Failure chain recorded:** missing PAT in remote URL → seed-commit conflict → missing git identity → dirty index → resolved with local config + force-with-lease (safe: remote only contained auto-seeded files).

---

## Iteration 9 — GitHub Gists

**Created (all public, Google-indexed snippets):**
1. `gist-profile.py` — nodriver profile manager: per-task profile dir + stale SingletonLock check → https://gist.github.com/YasakaH/fafb63f18728933ae7dabfad2076fd5d
2. `gist-session.py` — session health check: validate auth before real work → https://gist.github.com/YasakaH/2554c0743fab99791c0c56006d6fc54a
3. `gist-retry.py` — retry with exponential backoff → https://gist.github.com/YasakaH/4c5b8e2fe9bda13e36df372fe51aec0a

**Reason:** capture Google-indexed code searches; developers search code snippets; low commitment vs full repo.

---

## Current System State

**Published:**
- Articles: 2 on Dev.to (4271273, 4282020) + 2 on website (/blog/...)
- GitHub: 1 public repo, 3 public gists
- Website: 122 pages, 0 errors, 0 warnings (Next.js 16 static export)

**Ready (not yet posted):**
- Pinterest visuals (specs + pin drafts; visuals not created)
- Reddit discussions (both articles)
- X posts + threads (both articles)
- Quora answers (both articles, self-contained)
- Infographics (specs only; images not created)

**Not done:**
- Pinterest publishing
- Search Console submission
- Gumroad attribution testing
- Sales measurement
- Email capture (checklist not gated — wait for traffic)

---

## Current Funnel

```
Pinterest / GitHub / Dev.to / Reddit / X / Quora
                    ↓
              versatilesparks.qzz.io
                    ↓
            Cookbook CTA (?ref=article-slug)
                    ↓
                  Gumroad
```

## Rules Frozen

**Do NOT:**
- Create more infrastructure
- Create more abstractions
- Build more publishing tools

Until: traffic exists, clicks measured, sales measured.

**Do:**
- Publish, observe, learn, improve
- Measure against baseline, not optimism

---

## Next Actions

1. Create 3 Pinterest visuals (not 20)
2. Publish X derivatives (thread first, 5-min spacing)
3. Publish Reddit discussions (no link initially)
4. Publish Quora answers (no links)
5. Measure traffic (collect.py --devto daily, manual)
6. Article #3: "Why Your nodriver Session Dies Overnight (and How Production Systems Prevent It)" — only after derivatives deployed and observed
7. Adjust based on data

---

## Iteration 10 — Documentation Consolidation

**Created:**
- `docs/EXECUTION_HISTORY.md` — complete chronological execution log (this file)
- `docs/DECISIONS.md` — register of 18 irreversible decisions
- `docs/TRAFFIC_MAP.md` — traffic flow, source roles, conversion event taxonomy (visitor → article_view → cta_click → gumroad_visit → checkout_started → purchase), content multiplication matrix, CTA policy by layer
- `docs/PINTEREST_STRATEGY.md` — pin inventory, image specs, SEO (filenames + alt text), publishing rules

**GitHub SEO touch (Iteration 9 follow-up):**
- Added contextual "Python Browser Automation Cookbook" reference to Related sections of all 3 repo pattern files (browser-profile-management, retry-with-backoff, session-health-check)
- Executed via Python requests (PowerShell Out-File BOM breaks gh api JSON; `-b` shorthand fails in PowerShell)

**Correction recorded:** "no CTA anywhere" is wrong — derivatives are low-CTA, but the **website converts aggressively** (article → related concepts → book page → Gumroad).

---

## Iteration 11 — Content Calendar + Scorecard

**Created:**
- `docs/CONTENT_CALENDAR.md` — August schedule (article #3 Week 1, #4-5 Weeks 2-3, metrics review Week 4), derivative deployment cadence, brief queue from cycle-005, and rules (score before writing, deploy derivatives before next article, Pinterest only after conversion verified)
- `docs/ARTICLE_SCORECARD.md` — 5-metric scoring gate (buyer pain, nodriver relevance, cookbook connection, search potential, derivative potential; ≥35/50 or reframe). Both published articles retroactively scored (43, 44). Reframe rule: turn technical topics toward pain before rejecting.
- Hacker News added to PLATFORM_POLICIES.md — selective, genuine-value-only channel (repo, write-up, benchmark), never every article

**Caution adopted from review:** Pinterest visuals deferred until website conversion is verified (article CTA exists ✓, book page exists ✓ at /books/cookbook, Gumroad ?ref tracking pending end-to-end test).

---

## Iteration 12 — Definition of Done + Pinterest Experiments

**Created:**
- `docs/ARTICLE_DEFINITION_OF_DONE.md` — completion gate: content (website+devto, canonical, ?ref CTA, tags, no tool-drift, build+tests green), distribution (X, Reddit, Quora, GitHub, Pinterest as applicable, distribution.json), measurement (baseline row, manifest, published date, Gumroad tracking verified). "Article #N+1 starts only after #N's derivatives are deployed and observed."

**Updated:**
- `docs/ARTICLE_SCORECARD.md` — 6th metric added (Originality / competitive gap); gate now ≥42/60; retroactive scores re-graded (51, 53)
- `docs/DECISIONS.md` — D-019 (Pinterest manual-first, API automation deferred with revisit triggers), D-020 (Pinterest audience is indirect: Google Images indexing, not direct dev channel), D-021 (funnel integrity gate, not sales gate, for Pinterest)
- `docs/PINTEREST_STRATEGY.md` — audience assumption, 3-pin controlled experiment (pain / checklist / comparison), 30-day evaluation table, status block, entry gate
- A header ordering error in DECISIONS.md (D-018 displaced) was caught and fixed

**Pinterest API research recorded:** official API v5 exists (OAuth PKCE, pins:write scope, Trial= sandbox-only → Standard access requires demo video + review); community MCP servers exist but inherit the same auth/approval path; no official CLI. All deferred per D-019 — volume is ~12-24 pins/month, <1 hr manual.

---

## Iteration 13 — Deployment audit: dead domain caught; site redeployed to GitHub Pages

**Trigger:** Funnel integrity verification (Step 3 of execution order) — verify website article loads, CTA visible, Gumroad tracking, Search Console.

**Discovery sequence:**
1. `versatilesparks.com` fails DNS resolution on every resolver (8.8.8.8, 1.1.1.1, local).
2. Verisign RDAP (`https://rdap.verisign.com/com/v1/domain/versatilesparks.com`) → 404 — **the domain is not registered at all.**
3. Every canonical URL, derivative link, Pinterest pin, and sitemap pointed at a dead domain. The funnel integrity gate (D-021) was failing at the first check: "article loads".
4. The static export (122 pages) was built but **never deployed**; no hosting config existed (no vercel.json/netlify.toml).
5. Investigation revealed `versatilesparks.qzz.io` **already resolves** (Cloudflare-proxied, 104.21.43.220 / 172.67.186.97) and serves an **older, partial Next.js build** (root 200; /blog/*, /books/*, /about.html, /problems.html all 404; only ~2 top-level HTML files) from an unknown origin host.

**Decision (user):** Zero-budget constraint wins. Do NOT buy versatilesparks.com. Canonical becomes `https://versatilesparks.qzz.io`. Deploy static export to GitHub Pages under YasakaH account; user configures qzz.io DNS to point there. (The qzz.io record is Cloudflare-proxied; DNS flip is a user action.)

**Changes made:**
- `website-next/src/**` — 11 files: `SITE_URL` constant `https://versatilesparks.com` → `https://versatilesparks.qzz.io` (blog/[slug], problems, recipes, books, concepts pages, sitemap.ts, robots.ts, layout.tsx, LegalLayout.tsx, terms page text)
- `website-next/src/db/knowledge-base.json` — both article canonical_url fields (later regenerated by compile-content.js anyway)
- `website-next/next.config.ts` — added `trailingSlash: true` (export now produces `/blog/<slug>/index.html` instead of flat `.html`, matching sitemap/canonical clean URLs)
- `website-next/src/components/ContentBody.tsx` — **discovered raw markdown leaked into rendered pages** (CTA rendered as literal `[Python Browser Automation Cookbook](https://gum.co/...)` text — the conversion CTA was NOT a link). ContentBody only handled paragraphs/###/ol/fenced-code. Extended with: `##`/`###` headings, `**bold**`, `` `inline code` ``, `[links](url)`, `---` rules, `- ` unordered lists. Inline tokenizer is regex-based, dependency-free, no dangerouslySetInnerHTML. Both article pages verified: CTA is a real `<a href="https://gum.co/...?ref=...">`, 6-7 `<h2>`, 12-17 `<strong>`, rules and lists render; zero visible markdown leaks (remaining hits are in the serialized RSC `<script>` payload, invisible).
- Batch URL migration across the repo (161 replacements, 36 files): articles/ (drafts, published, derivatives, metrics-baseline, EDITORIAL_CALENDAR, manifest.json), docs/ (DECISIONS, EXECUTION_HISTORY, ARTICLE_DEFINITION_OF_DONE), MARKETING.md, INDEX.md, tools/publisher/consume_handoff.py, website-next (MDX, scripts, public/search-index.json, ARCHITECTURE.md). **Excluded: `metrics/raw/2026-07-31.json` (immutable snapshot, D-005).**
- Dev.to live canonicals updated via API for both articles:
  - #4271273 → https://versatilesparks.qzz.io/blog/5-mistakes-nodriver-beginners
  - #4282020 → https://versatilesparks.qzz.io/blog/why-browser-profiles-break
- Distribution manifests updated (canonical URL + pinterest_pins entry now records the 3 experiment visuals).

**Deployment (GitHub Pages):**
- Repo created: `YasakaH/versatilesparks-web` (public). Note: `gh repo create` silently attached to a repo that already existed with prior history (source + a Cloudflare Pages workflow commit from the abandoned migration; history preserved on the old refs).
- `out/` initialized as git repo, `CNAME` file = `versatilesparks.qzz.io`, pushed to `main` (1098 files, 12.9k lines), Pages enabled via API (`build_type=legacy`, source main/root).
- Rebuild pushed as second commit → legacy Pages build **stuck "building" for 20+ min then errored** ("Page build failed.") — root cause never fully confirmed; suspected force-push-during-build. Resolved by recreating the commit as a fast-forward squash on top of the previously built commit (f82111c) and force-pushing again. New build in progress.
- Site will serve at `https://versatilesparks.qzz.io/` (GitHub Pages + CNAME) **only after the user flips DNS**. Until then qzz.io serves the old stale build and `yasakah.github.io/versatilesparks-web/` redirects to the custom domain.

**Commands that mattered:**
- `gh api -X POST repos/YasakaH/versatilesparks-web/pages -f build_type=legacy -f "source[branch]=main" -f "source[path]=/"`
- PowerShell 5.1 quirks: `Get-Content -Raw` unavailable (use `[System.IO.File]::ReadAllText`), `gh repo list`/`--jq` arg parsing, `git` prompts for credentials (push with `https://YasakaH:PAT@github.com/...` inline, never persisted in config).

**Blockers for user:**
- DNS flip: `versatilesparks.qzz.io` → CNAME `YasakaH.github.io` (or GitHub Pages A records 185.199.108.153/109/110/111). If the record is Cloudflare-proxied, set origin to the CNAME target and keep proxy on (Cloudflare edge TLS terminates HTTPS regardless of GitHub's cert state).
- After flip, re-verify article pages + sitemap from the live domain.

**Post-deployment follow-up (corruption + credential exposure):**
1. The first Pages builds errored ("Page build failed."). Root cause: a botched squash attempt — `git read-tree 9b25fc1^{tree}` failed under PowerShell (`^{tree}` misparsed), leaving the working tree of the out/.git repo polluted with **the entire cookbook source** (INDEX.md, MARKETING.md, tools/, .reddit-creds.json, .reddit-*.files, book covers, etc.). `git add -A` swept it all into the deployment commit, deleting 404.html/CNAME and publishing cookbook source — including Reddit API credentials — to the PUBLIC repo.
2. **Remediation:** rebuilt the deployment in a clean temp dir (`deploy-clean`) from the verified export, added CNAME, committed only the 1098 export files (verified: no reddit/.env/creds files), force-pushed. Remote tree verified clean (1455 entries, CNAME + 404.html + blog present, zero suspicious files). Pages build of the clean commit 8a18c14 → **built**. Direct TLS-skipped fetch against Pages IP 185.199.108.153 with Host=versatilesparks.qzz.io → HTTP 200, article page + gum.co CTA with ?ref verified.
3. **Outstanding risk:** `.reddit-creds.json` (client_id, refresh_token, user_agent — client_secret was null) exists in the public repo's old commit history (unreachable objects; ref-less commits are GC'd by GitHub eventually, but may persist for a long time and may be in Pages build artifacts). **The user should rotate the Reddit credentials** (regenerate refresh token / client) and move the creds file out of the cookbook root.
4. The `npm run build` output dir is wiped on every build — the CNAME file must be re-created after each build (or a deploy script should add it). Noted as a repeatable footgun.

**Verified end-state:**
- Site content correct: trailingSlash URLs, qzz.io canonicals, rendered markdown (CTA = real link), sitemap/robots on qzz.io, zero .com references outside the immutable metrics snapshot.
- GitHub Pages: built, serving at custom domain once DNS flips.

---

## Iteration 14 — Hosting consolidation: Cloudflare Pages origin, GitHub Pages retired

**Reviewer direction (user):** Do not point qzz.io to GitHub Pages. Keep DNS untouched. Cloudflare Pages is already in the stack — restore it as the single origin. Restructure the repo to commit source, not generated output, and let Cloudflare (via workflow) build and deploy.

**Investigation findings:**
1. The old GitHub Actions workflow was recovered from history (`6836893`): `npm ci && npm run build` in `website-next/`, then `cloudflare/wrangler-action@v3 pages deploy website-next/out --project-name=versatilesparks`. Needs two repo secrets: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID` (neither exists on the repo; no CF credentials anywhere locally — the user must add them).
2. The Cloudflare Pages project (`versatilesparks`) is presumed alive: qzz.io serves an old Next.js build through Cloudflare IPs — consistent with a stale Pages deployment.
3. **Root cause of the Iteration 13 corruption finally identified:** `npm run build` wipes `website-next/out/` — including the out/.git that had been initialized for deployment. Subsequent `git add -A` from that directory walked up and operated on the **cookbook's real .git** (which held the full original history), sweeping the entire cookbook worktree (including `.reddit-creds.json`) into deployment commits. The cookbook repo and the deployment repo were one repo all along.
4. Secret audit of the full git history: `.env` was never committed (gitignored); `.reddit-creds.json` appears in exactly one commit (f82111c, the corrupted one) — now unreachable on the remote after the clean force-push. Exposure limited to Reddit client_id + refresh_token. GUMROAD_ACCESS_TOKEN never leaked.

**Changes made:**
- `.gitignore`: added `.reddit-*` (covers .reddit-creds.json, engagement log, last-run files, status).
- `.github/workflows/deploy.yml`: branch trigger `master` → `main`.
- Repo rebuilt as **source repo** on the clean original history: branch reset to `6836893` (last clean source commit), worktree staged with the full current cookbook state, `.reddit-*` untracked, sample PDFs in `website-next/out/downloads` untracked, committed as `adc07f3` (1263 files changed vs 6836893). Force-pushed to `YasakaH/versatilesparks-web` main.
- **GitHub Pages disabled** (DELETE /pages). DNS untouched. Main now = source (website-next/, articles/, docs/, tools/, workflow).
- Remote tree verified via API: deploy.yml present, website-next source present, zero secret files.

**User action required (single remaining step):**
1. Add secrets to `YasakaH/versatilesparks-web`: `CLOUDFLARE_API_TOKEN` (Pages:Edit permission) and `CLOUDFLARE_ACCOUNT_ID` (Account → Workers & Pages → right sidebar).
2. Trigger the workflow (push or workflow_dispatch) — it builds and deploys to project `versatilesparks`.
3. If the project was deleted: create in Cloudflare dashboard → Pages → Create → Connect to GitHub → repo → framework preset Next.js → root `website-next` → build `npm ci && npm run build` → output `out/` → then verify qzz.io custom domain binding.
4. Verify at https://versatilesparks.qzz.io/blog/why-browser-profiles-break (article + CTA).
5. Rotate Reddit credentials (D-023).

**Publishing behavior after this:** `git push` of `website-next/**` changes auto-deploys. Article/doc pushes do not trigger (workflow path filter). Local flow: edit article → `npm run build` local verification → push → live.

---

## Iteration 15 — Cloudflare account identification

**Question:** which Cloudflare account hosts `versatilesparks.qzz.io`?

**Findings:**
- `qzz.io` is a real registered domain; NS = `ns1/2/3.qzz.io` (self-hosted authoritative DNS with glue); apex `142.171.123.133` is a live VPS (unreachable from the VPN network, but resolves).
- `versatilesparks.qzz.io` → Cloudflare proxied IPs → the `qzz.io` zone lives in Cloudflare (orange-cloud record for the subdomain).
- `versatilesparks.pages.dev` resolves → the Cloudflare Pages project `versatilesparks` exists with a prior deployment.
- No Cloudflare credentials existed on this machine (no env keys, no wrangler config, no tokens in `.env` files, no hardcoded account ID in any git history).
- The earlier public-DNS test failures were caused by the local VPN (`bdvpnservice_1`, DNS 198.18.0.33/127.0.0.1) blocking direct DNS/IP traffic — DoH (dns.google / cloudflare-dns.com) resolves everything correctly. DNS was never broken.

**Answer (user-provided):** Cloudflare account email = user's account (identifiers in local gitignored `docs/DEPLOYMENT_PRIVATE.md`). The zone `versatilesparks.qzz.io` + Pages project `versatilesparks` + custom domain binding live in this account.

**Secrets policy:** never store the account email in public files; do not commit any CF token. Deployment credentials live in GitHub Actions secrets + hermes `.env` (user-scoped machine file).

## Iteration 15b — First successful deployment to qzz.io

**Access obtained:** user ran `npx wrangler login` (Cloudflare OAuth, wrangler 4.118.0). Credentials stored at `C:\Users\varas\AppData\Roaming\xdg.config\.wrangler\config\default.toml` (NOT `~/.wrangler`). OAuth token has `pages:write`, `zone:read`, `ssl_certs:write` — enough to deploy, not enough to mint API tokens (POST /user/tokens → 403) or purge cache (401).

**Account map (verified via API):**
- Account: user's Cloudflare account (ID in `docs/DEPLOYMENT_PRIVATE.md` + hermes `.env` as `CLOUDFLARE_ACCOUNT_ID`)
- Zones: `libdynconnect.com` (active) + `versatilesparks.qzz.io` (active) — the canonical is its own zone, not a record in a parent qzz.io zone
- Pages project `versatilesparks`: domains `versatilesparks.pages.dev` + `versatilesparks.qzz.io`, production branch `main`

**Deployment executed (2026-08-01):** `npx wrangler pages deploy website-next/out --project-name=versatilesparks --branch main` → 1080 files uploaded, deployment `a0956c3a`.

**Verified live on https://versatilesparks.qzz.io:**
- `/` 200 (new build), article `/blog/why-browser-profiles-break/` 200 with GitHub pattern links + Gumroad CTA
- `/robots.txt` 200, `/sitemap.xml` 200 (initial 404 was a stale edge-cached 404 from the previous deployment; self-healed)

**Remaining for full CI:** the GitHub Actions workflow needs `CLOUDFLARE_API_TOKEN` (scoped: Account → Cloudflare Pages → Edit). Cannot be created via API (OAuth lacks token-edit permission). User creates it in dashboard (Profile → API Tokens → Create Custom Token → Pages:Edit → Account). Fallback until then: manual deploy per push:
```
cd website-next && npm run build
npx wrangler pages deploy website-next/out --project-name=versatilesparks --branch main
```
wrangler is authenticated on this machine, so the OAuth flow stays valid (refresh token auto-renews).

---

## Session Context Preservation

**Environment:**
- Working dir: C:\Users\varas\AppData\Local\hermes
- Cookbook repo: E:\Hermes Projects\cookbook
- .env at C:\Users\varas\AppData\Local\hermes\.env: DEVTO_API_KEY, HASHNODE_TOKEN, GITHUB_PAT, GOOGLE_API_KEY, MISTRAL_API_KEY, NVIDIA_API_KEY — NO Cloudflare or Medium credentials
- GitHub: YasakaH (gh authenticated via GITHUB_PAT)
- Cloudflare migration ABORTED (repo under sandeepvara's GitHub, not YasakaH's Cloudflare)
- Push to sandeepvara/versatilesparks-publishing still blocked (no credentials)

**Commands (from cookbook/):**
```
python tools/publisher/consume_handoff.py --scaffold|--outline|--problems|--manifest|--validate-only|--strict|--dry-run
python tools/publisher/publish.py devto <file> --draft|--action update --id <id> [--feedback] [--views N ...]
python tools/publisher/metrics/collect.py --devto [--force] [--no-feedback]
python tests/test_contracts.py   # 71/71 pass
node website-next/scripts/compile-content.js
npx next build   # in website-next/
```
