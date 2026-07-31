# Health Check Pattern

## Identity
- id: health-check-pattern
- type: pattern
- title: Browser Health Verification
- tags: [health, monitoring, resilience]

## Metadata
- created: 2025-04-07
- domain: browser-automation
- version: 0.1.0

## Semantic Layer
Periodic health checks to verify browser responsiveness: ping CDP, evaluate JS, check page load state.

## Narrative Layer
Browsers can silently fail (OOM, crash, hang). A health check loop detects dead browsers and triggers reconnection. Implement with timeout to avoid hanging.
