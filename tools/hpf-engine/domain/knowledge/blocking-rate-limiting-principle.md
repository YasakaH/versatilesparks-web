# Blocking & Rate Limiting Principle

## Identity
- id: blocking-rate-limiting-principle
- type: principle
- title: Blocking Detection and Rate Limiting
- tags: [blocking, rate-limiting, anti-detection, scraper, captcha]

## Metadata
- created: 2025-07-28
- domain: browser-automation
- version: 0.1.0

## Semantic Layer
Sites detect scrapers through behavioral signals: request frequency, IP reputation, missing headers, no JavaScript execution, headless browser signatures, and abnormal mouse/keyboard patterns. Rate limiting blocks by counting requests per time window. Captchas add a proof-of-human step. Bans escalate from temporary (429 status) to permanent (403/blocked IP).

## Narrative Layer
Getting blocked is inevitable in production scraping. The mitigation stack is: rotate user agents, randomize timing between requests, use residential proxies, solve captchas with services like 2Captcha, and maintain session warming pools. Rate limiting requires exponential backoff with jitter, monitoring response headers for Retry-After, and distributing load across IPs. No single technique prevents blocking — layered mitigation is required.
