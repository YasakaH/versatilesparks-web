# Selenium Concept

## Identity
- id: selenium-concept
- type: concept
- title: Selenium Browser Automation Framework
- tags: [selenium, webdriver, framework, automation]

## Metadata
- created: 2025-07-28
- domain: browser-automation
- version: 0.1.0

## Semantic Layer
Selenium is a browser automation framework using the W3C WebDriver protocol. It supports multiple browsers (Chrome, Firefox, Edge, Safari) through browser-specific drivers. Selenium has three components: WebDriver API, IDE for record-and-playback, and Grid for distributed execution.

## Narrative Layer
Selenium dominated browser automation for a decade but is being replaced by CDP-native tools. Its main weakness is the WebDriver protocol overhead: each command is an HTTP round-trip, making it slower than CDP's WebSocket-based approach. Selenium also exposes the `navigator.webdriver` flag, making detection easier. The migration path is typically Playwright for cross-browser needs or nodriver for Chrome-only.
