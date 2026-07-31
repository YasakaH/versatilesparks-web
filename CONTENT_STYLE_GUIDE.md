# Content Style Guide

## Audience
Developers who already know Python and have tried or evaluated browser automation. They come looking for solutions, not tutorials. Write for someone who skims the error first and reads the explanation second.

## Tone
- Direct, technical, confident — "Use CDP stealth patches" not "You might want to consider using CDP stealth patches"
- No fluff, no filler, no "in today's digital world"
- Engineers talking to engineers during a coffee break

## Voice Rules
- Active voice always: "Pass the user_data_dir argument" not "The user_data_dir argument should be passed"
- Second person ("you") for the reader
- First person plural ("we") for shared assumptions
- No marketing superlatives: "solves", "revolutionary", "game-changer", "next-gen"
- No hedging: "simply", "just", "easily" — if it's simple, show the code

## Opening Hook Patterns

Pick one pattern per article:

| Pattern | Example |
|---------|---------|
| **The error** | "SessionNotCreatedException: Chrome failed to start: crashed." |
| **The admission** | "I spent three days debugging a phantom CAPTCHA." |
| **The counterintuitive** | "More profiles don't fix profile isolation." |
| **The missing piece** | "You're doing everything right, except one thing." |
| **The benchmark** | "Twenty headless browsers, one machine, zero collisions." |

Never open with a definition ("Browser automation is...").

## Title Formulas

Titles are the single highest-leverage SEO element. Use these patterns:

- `{Number} {Noun} Every {Audience} {Verb}` — "5 Mistakes Every nodriver User Makes"
- `How to {Do X} Without {Pain}` — "How to Run 20 Browsers Without Profile Collisions"
- `Why Your {Thing} {Breaks} (And How to Fix It)` — "Why Your CAPTCHA Bypass Stops Working"
- `The {Noun} {Audience} {Verb}` — "The Production Guide nodriver Won't Give You"
- `{Verb} {Noun} Like a {Role}` — "Debugging Browser Automation Like a SRE"

Maximum 70 characters. Include the primary keyword naturally.

## Article Structure

```
H1: Title

Opening paragraph (2-3 sentences): Hook + problem statement + implied solution

## The Problem
What breaks, what hurts, what the reader is hitting right now.
Include the actual error message or symptom.

## Why It Happens
Technical root cause. Don't skip this — readers who understand the cause
remember the solution.

## The Fix
Step-by-step code or configuration. One clear path, not three alternatives.
If alternatives exist, list them after the main solution.

## Production Notes (optional)
Things that work at scale vs. in a script. Side effects, edge cases, limits.

## Related Concepts
Internal links to concept pages and recipes.
```

Every article needs exactly one CTA. Format:

> **Go deeper:** [Python Browser Automation Cookbook](https://gum.co/python-browser-automation-cookbook?ref=<article-slug>) covers {topic} with {N} production-ready recipes.

## Code Style

- Python 3.11+ syntax (match/case, union types)
- nodriver async/await (not selenium sync)
- Type hints where they add clarity
- No comments in code — the surrounding text explains
- Error handling shown as try/except, not if/else
- Config values as constants at top of snippet

````
```python
import asyncio
from nodriver import start

BROWSER_ARGS = ["--no-sandbox", "--disable-blink-features=AutomationControlled"]

async def main():
    browser = await start(headless=True, arguments=BROWSER_ARGS)
    # ...
```
````

## Internal Linking Rules

Every article must have exactly:
1. One canonical_url pointing to the concept page
2. One "Related Concepts" section with links to 2-3 concept or recipe pages
3. One book CTA at the bottom

Internal link format: `[concept name](/concepts/<slug>)` or `[recipe title](/recipes/<slug>)`

## SEO Checklist

Before publishing every article:
- [ ] Title ≤ 70 chars, includes primary keyword
- [ ] Meta description ≤ 160 chars, includes primary keyword
- [ ] URL slug is keyword, not a number or date
- [ ] H1 matches title
- [ ] H2s are question-based or keyword-driven
- [ ] At least 2 internal links to concept pages
- [ ] 1 canonical_url to concept page
- [ ] 1 book CTA with ?ref= tracking
- [ ] Image alt text if images are ever added
- [ ] JSON-LD is valid (handled by template for website articles)

## Publishing Checklist

Before marking any article as published:
- [ ] Article read aloud for flow (catches awkward phrasing)
- [ ] Code snippets tested against actual nodriver version
- [ ] All internal links resolve
- [ ] canonical_url exists and is correct
- [ ] CTA link has ?ref= parameter matching article slug
- [ ] Tags match one of: nodriver, python, webscraping, browser-automation, plus concept tag
- [ ] Published on Dev.to first
- [ ] Cross-posted to website (canonical_url → concept page)
- [ ] GitHub update triggers Cloudflare deploy

## Prohibited Words

agency, services, consulting, enterprise solutions, digital transformation, synergy, leverage (as verb), utilize, solutioning, best practices (without evidence), industry-standard (without naming the standard)
