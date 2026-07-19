# Python Browser Automation Cookbook

> **Production Automation Engineering Edition**
>
> 60 production-ready recipes using nodriver — build and operate browser automation that works the same on day 30 as it did on day 1.

---

## What This Repository Contains

```
cookbook/
├── README.md              ← this file (project overview)
├── book/                 ← manuscript source (Pandoc/Quarto-ready)
├── recipes/              ← runnable Python code (ch01 … ch14)
├── common/               ← reusable modules (browser, retry, recovery…)
├── website-next/          ← Next.js 16 marketing/docs site (static export)
│   ├── content/          ← MDX for books, concepts, recipes
│   ├── src/              ← App-router pages + components
│   └── scripts/          ← content validation + compile scripts
├── Products/             ← Gumroad product assets + listing copy (gitignored)
├── .github/workflows/    ← Cloudflare Pages deploy workflow
└── assets/               ← diagrams and images
```

## Editions

| Edition | Recipes | Audience | Price |
|---------|---------|----------|-------|
| V1 | 30 (Ch 1-8) | Getting started | $29 |
| V2 Bundle | 60 (Ch 1-14) | Production engineering | $59 |

## Quick Start

```bash
pip install nodriver
python recipes/ch01/01_launch_browser.py
```

## Website (website-next)

The marketing and documentation site is a Next.js 16 app that exports to static HTML.

```bash
cd website-next
npm ci
npm run build      # validates content, compiles MDX, exports to ./out
npx serve out     # preview locally
```

Deploys are automatic via `.github/workflows/deploy.yml`: every push to
`master` that touches `website-next/**` builds the site on GitHub Actions and
publishes `website-next/out` to Cloudflare Pages (`versatilesparks` project).

## Build From Source

```bash
# EPUB
pandoc book/index.md --from markdown --to epub3 --output releases/cookbook.epub

# MOBI (requires Calibre)
ebook-convert releases/cookbook.epub releases/cookbook.mobi
```

## Author

**Yasaka Hanini** — Browser automation engineer.

## License

All rights reserved. This material is a paid product and may not be redistributed.
