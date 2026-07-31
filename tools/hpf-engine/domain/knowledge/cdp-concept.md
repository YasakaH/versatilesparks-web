# CDP Concept

## Identity
- id: cdp-concept
- type: concept
- title: Chrome DevTools Protocol
- tags: [cdp, protocol, browser]

## Metadata
- created: 2025-04-07
- domain: browser-automation
- version: 0.1.0

## Semantic Layer
CDP (Chrome DevTools Protocol) is a protocol for instrumenting Chromium-based browsers. It exposes JSON-RPC over WebSocket for controlling browser behavior.

## Narrative Layer
Most modern browser automation tools (Playwright, Puppeteer, nodriver) use CDP directly rather than the older WebDriver protocol. CDP provides finer-grained control over network, rendering, and debugging.
