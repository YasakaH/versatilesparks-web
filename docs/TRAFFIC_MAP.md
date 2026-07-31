# Traffic Map

How traffic moves into the funnel, and how to attribute buyers to channels.

## Flow

```
                        Pinterest (evergreen)
                             |
GitHub --------> Website <-------- Dev.to
    |               |                |
    |               |                |
    |            Search              |
    |               |                |
    |               v                |
    +---------> Cookbook Page <------+
                    |
                    v
                 Gumroad
```

## Source roles

| Source    | Intent                   | Expected visitor | Attribution signal                    |
| --------- | ------------------------ | ---------------- | ------------------------------------- |
| GitHub    | technical credibility    | developer        | ?ref=github-* or repo referrer        |
| Dev.to    | learning / problem-solving | developer       | canonical link + ?ref=<slug>          |
| Reddit    | discussion               | researcher       | no link (discussion only) — brand later |
| X        | awareness                | developer        | ?ref=<slug> on website CTA            |
| Pinterest | visual discovery         | beginner         | pin link → website article            |
| Search    | high intent              | buyer            | Search Console (queries → pages)      |
| Quora     | search capture           | seeker           | no link allowed — brand recall only   |

**Rule:** when metrics arrive, answer "which channel brought buyers" — not "which channel got views."

---

## Conversion event taxonomy

```
visitor
   ↓
article_view
   ↓
cta_visible
   ↓
cta_click
   ↓
gumroad_visit
   ↓
checkout_started
   ↓
purchase
```

### Diagnostic use

- 1000 article views → 20 Gumroad visits = **CTA problem** (offer, placement, wording)
- 20 Gumroad visits → 0 purchases = **product page / pricing / trust problem**
- Views but no cta_clicks = article doesn't connect to the offer
- Gumroad visits but no checkouts = landing page problem

### Where each event is measured

| Event          | Source                                  |
| -------------- | --------------------------------------- |
| article_view   | Dev.to `/analytics/totals` + Search Console impressions |
| cta_visible    | not measurable (assume = article end reach) |
| cta_click      | Gumroad referrer `?ref=<slug>`          |
| gumroad_visit  | Gumroad analytics (product page views)   |
| checkout_started | Gumroad analytics                    |
| purchase       | Gumroad sales                           |

---

## Content multiplication matrix

One article produces:

```
ARTICLE
 |
 +-- Dev.to article        (authority)
 +-- Website article       (conversion owner)
 +-- X thread              (awareness)
 +-- X single post         (awareness)
 +-- Reddit discussion     (community trust)
 +-- Quora answer          (search capture, no link)
 +-- GitHub pattern doc    (developer trust)
 +-- GitHub gist           (code search)
 +-- Pinterest pins        (visual discovery)
 +-- Infographic           (visual + Google Images)
 +-- YouTube short         (deferred — no channel)
 +-- LinkedIn post         (blocked — account banned)
 +-- Checklist page        (lead capture, not gated yet)
```

This is the growth engine: ~10 discovery surfaces per article, all routing to the website.

---

## CTA policy by layer

- **Derivatives (Reddit, Quora, X, GitHub):** minimal or no CTA — trust first
- **Dev.to:** exactly one CTA link with `?ref=<slug>` — tolerated
- **Website: sell aggressively.** The website is where conversion belongs: article → related concepts → book page → Gumroad. No "no CTA" doctrine applies here.
