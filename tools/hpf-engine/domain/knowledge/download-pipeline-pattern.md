# Download Pipeline Pattern

## Identity
- id: download-pipeline-pattern
- type: pattern
- title: Production Download Pipeline
- tags: [download, pipeline, extraction, production, scraping]

## Metadata
- created: 2025-07-28
- domain: browser-automation
- version: 0.1.0

## Semantic Layer
A download pipeline manages browser-based data extraction at scale: queue URLs, launch browser sessions, navigate to targets, extract structured data, validate output, store results, handle failures. Key stages: URL frontier, session pool, extraction worker, data validator, storage backend. Each stage is decoupled through message queues for independent scaling.

## Narrative Layer
Production download pipelines decouple concerns through queues. A Redis-backed URL frontier feeds sessions from a pre-warmed pool. Extraction workers run browser automation against each URL, validate schema compliance, and push to storage. Failed URLs go to a dead-letter queue for retry with backoff. This architecture handles millions of URLs by bottlenecking only at the browser session pool, which is scaled horizontally.
