# Incremental Extraction Pattern

## Identity
- id: incremental-extraction-pattern
- type: pattern
- title: Page Data Extraction
- tags: [extraction, scraping, incremental, missing]

## Metadata
- created: 2025-04-07
- domain: browser-automation
- version: 0.1.1
- updated: 2025-07-28

## Semantic Layer
Extract page data incrementally: wait for DOM ready -> extract visible content -> scroll -> extract more -> repeat until no new data. Missing content is often caused by scroll-triggered loading or lazy rendering.

## Narrative Layer
Incremental extraction handles infinite scroll and lazy-loaded content. Track seen elements to avoid duplicates. Implement with scroll-triggered extraction batches.
