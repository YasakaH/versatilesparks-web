# Selector Strategy Pattern

## Identity
- id: selector-strategy-pattern
- type: pattern
- title: Resilient Element Selection
- tags: [selector, strategy, resilience]

## Metadata
- created: 2025-04-07
- domain: browser-automation
- version: 0.1.0

## Semantic Layer
Multiple selector strategies ranked by reliability: data-testid > id > CSS class > XPath. Fallback chain on failure.

## Narrative Layer
Brittle selectors cause 80% of automation failures. Use data-testid attributes where possible. Fall back gracefully through the selector chain.
