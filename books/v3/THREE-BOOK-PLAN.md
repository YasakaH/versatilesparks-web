# Book Series Strategy

## Status: Flexible (not frozen)

This document describes the book series direction from the LongShot conversation (2026-07-27). Unlike research domains, book identities and publication order are deliberately **not frozen**. They will be decided when research dossiers reach maturity.

The HPF platform and the book series are separate governance tracks. Changes to one do not imply changes to the other.

---

## The Series

Three books. Three different perspectives on the same ecosystem. Not volumes — perspectives.

Currently scoped as candidates:

| Perspective | Working Title | Purpose | Audience |
|---|---|---|---|
| A | Browser Automation Engineering | Why browsers became execution environments for AI | Engineers moving from scripting to production |
| B | Production Browser Agent Infrastructure | How companies build reliable browser-agent infrastructure | Senior engineers and architects |
| C | Browser UX Engineering / Agent-Ready Web | The novel thesis: accessible web = agent API | Web developers, platform teams |

These titles are candidates, not commitments. Research may reveal that a different framing or order serves the series better.

---

## What Is Frozen

Research identities (see below). The canonical concept layer. The HPF governance track. Book identities are explicitly **not** frozen.

### Design Decisions

1. **No publication order frozen.** Perspective C is the most novel and may lead or follow depending on research maturity.
2. **Research dossiers precede books.** Domains are researched independently of any book schedule.
3. **HPF is not the book.** HPF owns the reusable knowledge layer. Books consume HPF knowledge objects.
4. **Cross-book object sharing.** A knowledge object can appear in all three books with different narrative framing.
5. **Book branding is flexible.** Final titles, angles, and publication order will be determined by research findings, not predetermined by this document.

---

## Research Domains (Frozen)

These are the permanent intellectual property. They are divided into two classes.

### Stable Domains (Evergreen — change rarely)

```
Browser Perception          — how sites detect automation
Browser Architecture        — CDP, WebDriver, process model, BiDi
Browser Economics           — detection arms race, CAPTCHA economics, ROI
Browser State               — navigation lifecycle, readiness, state machines
Browser Memory              — cache, persistence, session state
Browser Reliability         — health monitoring, recovery, fault tolerance
Browser Security            — isolation, sandboxing, fingerprinting
Browser Distributed Systems — multi-instance coordination, queues, proxy architecture
```

### Technology Profiles (Volatile — change frequently)

These are not first-class research domains. Each profile maps onto the stable domains.

```
WebMCP
Playwright
Browser Use
Claude / Operator
Chrome DevTools
Camoufox
Selenium
Nodriver
Puppeteer
undetected-chromedriver
```

### How Profiles Work

A technology profile documents how a specific tool or platform instantiates each stable domain concept.

For example, a Playwright profile would answer:

- **Perception**: How detectable is Playwright by default?
- **Architecture**: How does Playwright map to CDP vs WebDriver?
- **State**: How does Playwright manage navigation lifecycle?
- **Reliability**: What retry/health mechanisms does Playwright offer?

Profiles are derived from stable domains. They are never researched independently.

---

## Series Flow

```
Research Domains (Stable)
      ↓
Canonical Concepts
      ↓
HPF Knowledge Objects
      ↓
Books (Perspective A / B / C)
```

---

## Governance

| Layer | Status | Change Process |
|---|---|---|
| Research domains | **Frozen** | Governance review required |
| Technology profiles | Active | Added/removed as tools evolve |
| Canonical concepts | **Frozen** | Added when new research domain is frozen |
| HPF knowledge objects | Active | Improved via benchmark evidence |
| Book identities | Flexible | Decided at publication time |
| Publication order | Flexible | Decided when research dossiers mature |

---

*Source: LongShot conversation 1785309527487*
*Last updated: 2026-07-29*
