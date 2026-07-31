# Browser Profiles Concept

## Identity
- id: browser-profiles-concept
- type: concept
- title: Isolated Browser Profiles
- tags: [profiles, isolation, persistence]

## Metadata
- created: 2025-04-07
- domain: browser-automation
- version: 0.1.0

## Semantic Layer
Browser profiles provide isolated environments with persistent storage, cookies, and local state.

## Narrative Layer
Each automation session should use a fresh profile or clean profile for isolation. Persistent profiles maintain auth state across sessions. Profile management prevents cross-contamination.
