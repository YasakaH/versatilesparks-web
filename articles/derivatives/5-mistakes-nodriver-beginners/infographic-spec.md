# Infographic — Spec

For a single static image (1200x1500 px, vertical, Pinterest/GitHub friendly).

## Content

Title: **"Why Browser Automation Fails in Production"**

Visual flow (from article):

```
Simple Script                       Production System
──────────────                      ─────────────────
Launch Browser                      Launch Browser
       │                                   │
       ▼                                   ▼
    Scrape                            Inject Stealth
       │                                   │
       ▼                                   ▼
    Crash                            Persistent Profile
                                           │
                                           ▼
                                     Retry With Backoff
                                           │
                                           ▼
                                      Health Check
                                           │
                                           ▼
                                      Proxy Rotation
                                           │
                                           ▼
                                       Success
```

Bottom strip (5 chips):

```
Stealth │ Session │ IP │ Profile │ Retry
```

Footer: small URL — `versatilesparks.qzz.io/blog/5-mistakes-nodriver-beginners`

## Filename & alt text (for Google Images)

- Filename: `nodriver-production-vs-simple-workflow.png`
- Alt: "nodriver production workflow showing stealth injection, persistent profile, retry with backoff, health check, and proxy rotation"

## Style

- Dark background (#0f172a), light text, one accent color (green for production, red for toy)
- Monospace-ish labels (developer audience)
- No stock photos

## Outputs

- PNG for Pinterest, reused for X and website if needed
