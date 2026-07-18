# Python Browser Automation Cookbook

> **Production Automation Engineering Edition**
>
> 60 production-ready recipes using nodriver — build and operate browser automation that works the same on day 30 as it did on day 1.

---

## What This Repository Contains

```
cookbook/
├── README.md              ← this file (project overview)
├── book/                  ← manuscript source (Pandoc-ready)
│   ├── chapters/          ← 15 chapter files split from the book
│   ├── appendix/          ← recipe index, architecture map
│   ├── styles/            ← EPUB CSS
│   └── metadata.yaml      ← Pandoc metadata
├── recipes/               ← runnable Python code
│   ├── ch01/ … ch14/      ← 60 recipe files, organized by chapter
├── common/                ← reusable modules
│   ├── browser.py         ← browser lifecycle
│   ├── retry.py           ← retry with backoff
│   ├── idempotency.py     ← @idempotent decorator, UPSERT
│   ├── network_queue.py   ← asyncio.Queue CDP handler
│   ├── data_pipeline.py   ← validation, quarantine, alerts
│   ├── metrics.py         ← observability collector
│   ├── recovery.py        ← RecoveryManager, FailureType
│   └── visual_diff.py     ← DOM region comparison
├── assets/                ← diagrams and images
├── tools/                 ← build scripts
└── releases/              ← generated PDFs/EPUBs
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
