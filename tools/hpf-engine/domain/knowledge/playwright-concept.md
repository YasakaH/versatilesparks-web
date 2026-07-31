# Playwright Concept

## Identity
- id: playwright-concept
- type: concept
- title: Playwright Browser Automation Framework
- tags: [playwright, cdp, automation, framework]

## Metadata
- created: 2025-07-28
- domain: browser-automation
- version: 0.1.0

## Semantic Layer
Playwright is a browser automation framework by Microsoft that uses CDP directly over WebSocket. It supports Chromium, Firefox, and WebKit with a single API. Key features: auto-waiting for elements, network interception, browser contexts for isolation, trace viewer for debugging, and codegen for test recording.

## Narrative Layer
Playwright is the strongest cross-browser CDP-native tool. Its auto-waiting eliminates most selector flakiness by design. The browser context model provides native isolation without managing profiles manually. For teams needing cross-browser coverage, Playwright is the pragmatic choice despite being heavier than nodriver for Chrome-only cases.
