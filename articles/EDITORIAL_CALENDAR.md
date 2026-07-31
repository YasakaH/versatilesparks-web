# Editorial Calendar — Browser Automation Content

**Goal:** 20 articles in 60 days → drive readers through concept pages → convert to book sales.

Each article maps to one of the 12 website concepts. The concept page on versatilesparks.qzz.io is the hub; articles are spokes distributed to Dev.to, Medium, and GitHub.

---

## Article Template

Every article should follow this structure:

```markdown
---
title: "..."
published: false
tags: [nodriver, python, webscraping, browser-automation, <concept-tag>]
canonical_url: https://versatilesparks.qzz.io/concepts/<slug>
---

[Problem statement — what breaks, what hurts]

[Debugging/walkthrough — specific error, step-by-step fix]

[Production pattern — how to do it right]

**CTA:** "This is one of 87 production recipes in the [Python Browser Automation Cookbook](https://gum.co/python-browser-automation-cookbook?ref=<article-slug>)."
```

---

## Article Queue

### Week 1

| # | Title | Cluster | Slug | Draft |
|---|-------|---------|------|-------|
| 1 | 5 Mistakes New nodriver Users Make (and How to Avoid Them) | General | `5-mistakes-nodriver-beginners` | ✅ Done |
| 2 | How nodriver Handles Browser Sessions (And Why It Matters) | Sessions | `nodriver-sessions-guide` | ❌ |

### Week 2

| # | Title | Cluster | Slug |
|---|-------|---------|------|
| 3 | Why Your nodriver Script Gets Blocked (And How to Fix It) | Anti Detection | `nodriver-getting-blocked` |
| 4 | Browser Profiles in nodriver: The Complete Guide | Profiles | `nodriver-browser-profiles` |

### Week 3

| # | Title | Cluster | Slug |
|---|-------|---------|------|
| 5 | How to Rotate Proxies with nodriver | Proxies | `nodriver-proxy-rotation` |
| 6 | Understanding Browser Fingerprints for Automation | Fingerprints | `browser-fingerprints-explained` |

### Week 4

| # | Title | Cluster | Slug |
|---|-------|---------|------|
| 7 | CDP Fundamentals: What nodriver Does Under the Hood | CDP | `cdp-fundamentals-nodriver` |
| 8 | Persistent Cookie Strategies for nodriver | Cookies | `nodriver-cookie-strategies` |

### Week 5

| # | Title | Cluster | Slug |
|---|-------|---------|------|
| 9 | Debugging Network Interception in nodriver | Network Interception | `nodriver-network-debugging` |
| 10 | How to Handle Login Flows with nodriver | Authentication | `nodriver-login-automation` |

### Week 6

| # | Title | Cluster | Slug |
|---|-------|---------|------|
| 11 | Scaling nodriver: From 1 Browser to 100 | Scaling | `scaling-nodriver` |
| 12 | Production Monitoring for Browser Automation | Observability | `browser-automation-monitoring` |

### Week 7

| # | Title | Cluster | Slug |
|---|-------|---------|------|
| 13 | Error Recovery Patterns in nodriver | Recovery | `nodriver-error-recovery` |
| 14 | nodriver vs Playwright: When to Use Which | Comparison | `nodriver-vs-playwright` |

### Week 8

| # | Title | Cluster | Slug |
|---|-------|---------|------|
| 15 | Anti-Detection Techniques That Actually Work | Anti Detection | `anti-detection-techniques` |
| 16 | Building a nodriver Profile Farm | Profiles | `nodriver-profile-farm` |

### Week 9

| # | Title | Cluster | Slug |
|---|-------|---------|------|
| 17 | Session Sharing Across nodriver Instances | Sessions | `session-sharing-nodriver` |
| 18 | How to Test Anti-Detection Configurations | Fingerprints | `test-anti-detection` |

### Week 10

| # | Title | Cluster | Slug |
|---|-------|---------|------|
| 19 | The nodriver Production Checklist | General | `nodriver-production-checklist` |
| 20 | From Script to System: Architecture for Browser Automation | General | `browser-automation-architecture` |

---

## Writing Checklist

Before marking an article as "published":

- [ ] Title includes primary keyword
- [ ] Opening paragraph states the problem
- [ ] Step-by-step walkthrough with code
- [ ] At least one specific error/mistake addressed
- [ ] Links to the concept page on versatilesparks.qzz.io
- [ ] Links to related article (internal cross-link)
- [ ] CTA to the relevant book with `?ref=` tracking parameter
- [ ] Tags include [nodriver, python, webscraping, browser-automation] + concept tag
- [ ] Published to Dev.to
- [ ] Republished to Medium (via adapter, if token exists)
- [ ] Added to tracking dashboard

---

## Concept ↔ Article Mapping

| Concept | Articles | Book Recipes |
|---------|----------|-------------|
| Anti Detection | #3, #15 | recipe-v1-5, recipe-v2-12, recipe-v2-13 |
| Authentication | #10 | recipe-v2-8, recipe-v2-9 |
| CDP | #7 | recipe-v2-14, recipe-v2-15 |
| Cookies | #8 | recipe-v1-4 |
| Fingerprints | #6, #18 | recipe-v1-3, recipe-v2-10, recipe-v2-11 |
| Network Interception | #9 | recipe-v2-16 |
| Observability | #12 | recipe-v2-20 |
| Profiles | #4, #16 | recipe-v1-1, recipe-v1-2, recipe-v2-6 |
| Proxies | #5 | recipe-v2-7 |
| Recovery | #13 | recipe-v2-19 |
| Scaling | #11 | recipe-v2-17, recipe-v2-18 |
| Sessions | #2, #17 | recipe-v1-3, recipe-v2-1, recipe-v2-2, recipe-v2-3 |
