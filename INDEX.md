# Versatile Sparks — Unified Project

This is the single root for all workstreams: books (V1, V2, V3), website, marketing, knowledge framework (HPF), research, and publishing tooling.

**Old scattered locations:** All consolidated here as of Jul 29, 2026.

---

## Directory Structure

```
cookbook/                          ← Git root (versatilesparks-publishing)
│
├── INDEX.md                       ← This file
├── ANCHORED_SUMMARY.md            ← "Why" documentation (decision log, session references)
├── MARKETING.md                   ← Marketing strategy, backlinks plan, conversion funnel
├── PROJECT-ROADMAP.md             ← Overall project roadmap (frozen Jul 29)
├── OPERATING-MODEL.md             ← 40/30/20/10 workstream split
├── PLATFORM-ARCHITECTURE.md       ← Stack architecture diagram (frozen Jul 29)
│
├── 📚 books/                      ← All book content
│   ├── v1/                        ← Python Browser Automation Cookbook ($29, 30 recipes)
│   ├── v2/                        ← Browser Automation Playbook ($59, 60 recipes)
│   ├── v3/                        ← V3 book (in ideation, see THREE-BOOK-PLAN.md)
│   ├── kdp/                       ← KDP submission packages
│   ├── products/                  ← Gumroad release ZIPs + listings
│   └── recipes/                   ← Source recipe scripts (ch01-ch14)
│
├── 🌐 website-next/               ← Next.js 16 knowledge-graph site
│   ├── ARCHITECTURE.md            ← Technical architecture (what + how)
│   └── ...                        ← App Router pages, components, content MDX
│
├── 📝 articles/                   ← Publishing pipeline
│   ├── draft/                     ← Unpublished articles
│   ├── published/                 ← Live articles
│   ├── templates/                 ← Article templates
│   └── EDITORIAL_CALENDAR.md      ← 20-article plan mapped to concepts
│
├── 🧰 tools/                      ← Build tools and scripts
│   ├── book-build/                ← 104 V1/V2 book generation scripts
│   ├── hpf-engine/                ← HPF engine (schema, validator, evaluation)
│   ├── publisher/                 ← Multi-platform publishing CLI
│   ├── scripts/                   ← Utility scripts (cookie copy, etc.)
│   └── build_personas.py          ← Persona builder
│
├── 🧠 knowledge/                  ← HPF (Human Process Framework)
│   ├── hpf-core/                  ← Git repo (github.com/YasakaH/hpf-core.git)
│   │   ├── canon/concepts/        ← 12 canonical concept definitions
│   │   ├── research/              ← Research methodologies
│   │   ├── product/               ← Product definitions
│   │   ├── engineering/           ← Engineering personae
│   │   └── ...                    ← Other persona directories
│   ├── core/                      ← 27 original CORE documents (archival)
│   ├── kernel/                    ← 13 kernel docs (post-restructure)
│   ├── governance/                ← 4 consolidated governance docs
│   ├── schema/                    ← Schema definitions (SCHEMA.md, REASONING_MODES.md)
│   ├── archived-personas/         ← 34 HPF persona directories (archival)
│   ├── submissions/               ← ChatGPT pipeline submissions
│   │   ├── v1/                    ← 7-file submission
│   │   ├── v2/                    ← 30-file submission
│   │   ├── feedback/              ← ChatGPT feedback data
│   │   └── *.py                   ← Submission scripts
│   ├── INDEX.md                   ← Hermes system index (archival)
│   ├── DNA.md                     ← Hermes DNA v1 (archival)
│   ├── _hpf_v2_impl_plan.txt      ← HPF v2 implementation plan
│   └── _hpf_v2_issue_desc.txt     ← HPF v2 issue description
│
├── 🔬 research/                   ← Market and systems research
│   ├── market/                    ← Automation reliability research
│   ├── agent-systems/             ← Agent Systems Engineering research
│   ├── transcripts/               ← Research interview transcripts
│   └── _deep_research_conversation.json  ← Deep research session data
│
├── 🖼️ assets/                     ← Shared images, covers, thumbnails
├── dist/                          ← Build output
├── releases/                      ← Versioned release archives
│
├── website/                       ← Old static HTML site (archival)
├── browser-automation-starter/    ← Template project for readers
├── common/                        ← Shared Python modules (browser, retry, recovery)
│
├── .github/                       ← CI/CD workflows (Cloudflare Pages deploy)
└── .env                           ← API keys (not committed)
```

---

## Workstreams

| Stream | Location | Status | Active thread |
|--------|----------|--------|---------------|
| **V1 + V2 Books** | `books/v1/`, `books/v2/` | Published on Gumroad | This thread |
| **Website** | `website-next/` | Live at versatilesparks.qzz.io | This thread |
| **Content Pipeline** | `articles/`, `tools/publisher/` | Dev.to + GitHub live | This thread |
| **V3 Book** | `books/v3/` | Ideation (THREE-BOOK-PLAN.md) | Other opencode thread |
| **HPF / Knowledge** | `knowledge/hpf-core/` | Active development | Other opencode thread |
| **Research** | `research/` | Phase 2 in progress | Other opencode thread |

---

## Key Remotes

| Repo | Remote | Local Path |
|------|--------|------------|
| Books + Website (this repo) | `github.com/sandeepvara/versatilesparks-publishing.git` | `cookbook/` |
| HPF Core | `github.com/YasakaH/hpf-core.git` | `cookbook/knowledge/hpf-core/` |

---

## Thread Boundaries (Critical)

| Thread | Workstream | Ownership | Handoff |
|--------|-----------|-----------|---------|
| **This thread** | Books V1/V2, website, content pipeline, marketing, SEO, metrics, publishing | `books/v1/`, `books/v2/`, `website-next/`, `articles/`, `tools/publisher/`, `MARKETING.md`, `METRICS.md`, `CONTENT_STYLE_GUIDE.md` | Receives research output from HPF thread, publishes it |
| **Other thread** | V3 book, HPF research, knowledge graph, patterns, typed edges, content pipeline automation | `books/v3/`, `knowledge/`, `research/`, `knowledge/hpf-core/` | Produces structured knowledge, content ideas, patterns |

### What this thread does NOT own
- **Pre-research / knowledge discovery** — HPF thread handles all concept extraction, pattern identification, and content ideation
- **Pattern library** — HPF thread extracts patterns (retry, backoff, circuit-breaker, etc.) from research
- **Typed relationship discovery** — HPF thread identifies REQUIRES/IMPLEMENTS/SOLVES edges between entities
- **Content pipeline automation** — HPF thread builds the workflow (IDEA → OUTLINE → DRAFT → REVIEWED → PUBLISHED → MEASURED)
- **Problem extraction** — HPF thread identifies developer pain points and error patterns from research

### What this thread owns
- **Content production** — Takes HPF-identified concepts/patterns/articles and writes them
- **Publishing** — Dev.to, website, GitHub (Medium when token available)
- **SEO & measurement** — Canonical URLs, meta descriptions, revenue/article tracking
- **Website** — `website-next/` app, routes, components, styling
- **Marketing strategy** — Conversion funnel, content clusters, backlinks, editorial calendar execution
- **Contribute upstream** — When this thread discovers new patterns or problems during writing, feed back to HPF thread via `knowledge/` or HANDOFF.md

## How to Use This Structure

- **This thread:** Edit files in `cookbook/`, `website-next/`, `articles/`, `tools/`
- **Other thread:** Edit files in `books/v3/`, `knowledge/`, `research/`
- **Shared assets:** Images and covers in `assets/` are used by both books and website
- **Canon concepts:** `knowledge/hpf-core/canon/concepts/` are the single source of truth for all 12 concepts used by the website
