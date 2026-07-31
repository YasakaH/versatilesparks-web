# Infographic — Spec

For a single static image (1200x1500 px, vertical, Pinterest/GitHub friendly).

## Content

Title: **"Why Browser Automation Fails in Production"**

Visual flow (left column simple script vs right column production system, from article):

```
Simple Script                       Production System
──────────────                      ─────────────────
Launch Browser                      Check Profile Lock
       │                                    │
       ▼                                    ▼
    Scrape                          Unique Profile Per Job
       │                                    │
       ▼                                    ▼
    Crash                             Validate Session
                                              │
                                              ▼
                                        Graceful Shutdown
                                              │
                                              ▼
                                        Detect + Recover
                                              │
                                              ▼
                                           Retire
```

Bottom strip (5 chips):

```
Lock Check │ Isolation │ Lifecycle │ Validation │ Recovery
```

Footer: small URL — `versatilesparks.qzz.io/blog/why-browser-profiles-break`

## Filename & alt text (for Google Images)

- Filename: `nodriver-browser-profile-lifecycle.png`
- Alt: "nodriver browser profile lifecycle showing create, authenticate, validate, reuse, recover, retire"

## Style

- Dark background (#0f172a), light text, one accent color (green for production, red for toy)
- Monospace-ish labels (developer audience)
- No stock photos

## Outputs

- PNG for Pinterest, same image reused for X and website if needed
