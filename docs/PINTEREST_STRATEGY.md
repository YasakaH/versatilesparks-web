# Pinterest Strategy

Evergreen visual discovery for technical content. Diagrams/checklists only — never sales graphics.

## Why it fits

The articles naturally produce visual material:

- lifecycle diagrams
- checklists
- failure charts
- architecture diagrams (Simple vs Production)

Pinterest users save systems and checklists, not advertisements.

## Audience assumption (D-020)

Pinterest is NOT a direct developer acquisition channel. Its value is indirect: Google Images/Search indexing of diagrams, checklists, and architecture visuals. Developers find the indexed visuals via search. The pin's job is to rank the visual, not to sell in the feed.

## First experiment (3 pins, 30-day observation)

Controlled test — answer "can a technical infographic attract developer traffic?"

1. **Pain pin** — "Why Browser Automation Scripts Fail Overnight" → captures people with the problem
2. **Checklist pin** — "nodriver Production Readiness Checklist" → captures people preparing deployment
3. **Comparison pin** — "Simple Browser Script vs Production Automation System" → creates curiosity

All link to canonical website articles (not the book page). Track: impressions → saves → outbound clicks → article views → CTA clicks → Gumroad visits.

### 30-day evaluation

| Metric             | Meaning                |
| ------------------ | ---------------------- |
| Impressions        | Pinterest distribution |
| Saves              | content usefulness     |
| Outbound clicks    | actual interest        |
| Article engagement | landing page quality   |
| CTA clicks         | commercial intent      |

## When to automate (D-019)

Not now. Triggers to revisit: >50 pins/month, OR Pinterest becomes top-3 traffic source, OR manual publishing becomes painful. Then: `tools/publisher/adapters/pinterest.py` (Pinterest API v5, OAuth PKCE, Standard access approval).

## Pin inventory (per article)

### Article #1 — 5-mistakes-nodriver-beginners

1. **"5 nodriver Mistakes That Break Production Scripts"** — checklist image (stealth, session, IP, profile, retry)
2. **"Simple Script vs Production Workflow"** — contrast diagram (Launch→Scrape→Crash vs full pipeline)

### Article #2 — why-browser-profiles-break

1. **"Browser Automation Production Checklist"** — checklist image (profile, session, retry, health, recovery)
2. **"Why Browser Automation Fails in Production"** — contrast diagram
3. **"Browser Profile Lifecycle"** — Create→Login→Validate→Reuse→Refresh→Retire

## Image specs

- 1200x1500 px vertical (2:3)
- Dark background (#0f172a), light text, one accent color (green production / red failure)
- Monospace-ish labels (developer audience)
- No stock photos
- Infographic spec per article in `articles/derivatives/<slug>/infographic-spec.md`

## SEO

- **Filenames:** descriptive — `nodriver-browser-profile-lifecycle.png`, `nodriver-production-vs-simple-workflow.png` (never `image1.png`)
- **Alt text:** full descriptive sentence ("nodriver browser profile lifecycle showing create, authenticate, validate, reuse, recover, retire")
- **Link:** canonical website article URL (not Dev.to)

## Publishing rules

- Create 3 visuals first, test before scaling to 20
- No sales copy on pins
- Pin → website article (not book page directly)
- Link via checklist page when it exists

## Status

```
Pinterest:
Strategy      ✅
Visual specs  ✅
Account       pending
Automation    deferred (D-019)
Publishing    manual first
Validation    not started
```

## Entry gate (D-021)

Pinterest publishing requires funnel integrity, NOT sales:

- ✅ Article loads (website)
- ✅ CTA visible
- ✅ Gumroad ?ref tracking works
- ✅ Book page exists

Do not wait for actual sales — Pinterest may generate the first buyers.
