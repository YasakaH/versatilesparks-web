# Retry Pattern

## Identity
- id: retry-pattern
- type: pattern
- title: Retry with Backoff for Browser Operations
- tags: [retry, backoff, resilience]

## Metadata
- created: 2025-04-07
- domain: browser-automation
- version: 0.1.0

## Semantic Layer
Retry with exponential backoff for transient browser failures (navigation timeout, element not found, staleness).

## Narrative Layer
Browser automation faces inherent flakiness. Retry with jittered backoff improves reliability 10x. Implement with circuit breaker to avoid hammering a dead browser.
