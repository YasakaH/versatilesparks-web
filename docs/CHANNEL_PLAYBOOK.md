# Channel Playbook

Execution instructions per channel. Not strategy (see DECISIONS.md) — how to post, what to include, what never to do.

---

## X / Twitter

**Purpose:** awareness
**Post type:** lesson, failure pattern, observation
**Format:** single post OR thread (5-7 tweets, ~5 min spacing between tweets, or native thread composer)
**Link:** canonical website URL at the end, once
**Never:** buy-my-book posts, repeated links, daily posting (cap ~2-3 posts/week)
**Plan:** Free tier ONLY (500 posts/month, no billing). ~2-3 posts/week ≈ 10-15/month, well under the allowance. Never exceed ~400 posts in a rolling month.
**Posting:** drafts live in `articles/derivatives/<slug>/x-thread.md` (or `x-post.md` for single posts). Post with:
```
python tools/publisher/adapters/x.py --slug <slug> --dry-run   # review
python tools/publisher/adapters/x.py --slug <slug> --post      # publish
```
Credentials: `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_TOKEN_SECRET` (OAuth 1.0a, Read+Write) in `.env`.

Template:
```
[Pain observation — 2-3 lines, no fluff]
[5 items list or numbered breakdown]
[Production model — diagram-in-text]
[Full breakdown: <link>]
```

---

## Reddit

**Purpose:** community trust
**Post type:** question, discussion, experience share
**Format:** practitioner voice ("I ran into this... what fixed it was..."), ends with a discussion question
**Link:** NONE initially. Never a book mention. Link only after engagement, if at all.
**Subreddits:** r/webscraping (primary), r/Python (careful), r/learnpython (only if topic fits)
**Never:** article dumps, CTAs, "I wrote a book"

Template:
```
I've noticed [observation about failures].
People usually focus on [common focus], but run into [pain list].
A pattern that works better: [bullet list].
Curious how others handle [specific technical question]?
```

---

## Quora

**Purpose:** search capture
**Post type:** answer to an existing question (do not create questions)
**Format:** self-contained — problem → mechanism → fix. NO links allowed (policy).
**Length:** 100-250 words.
**Never:** URLs, book names, promotional phrasing. Brand recall only.

Template:
```
One thing I learned building browser automation systems:
[core insight — 2-3 sentences]
The mistake many people make: [quote the wrong belief]
It isn't. [correct the belief — sessions expire, tokens rotate...]
A production system should [the fix].
```

---

## GitHub (repo + gists)

**Purpose:** search + credibility
**Include:** patterns, checklists, examples, gists
**Format:** markdown, MIT license, soft "Related" section (cookbook link as reference, not CTA)
**Repo:** YasakaH/nodriver-production-patterns — add a pattern doc per article when it fits
**Gists:** one snippet per useful code block, public, descriptive filename + description
**Never:** full paid content, aggressive links, marketing language in README

Pattern doc template:
```
# <Pattern Name>

## Problem
## Rules (numbered)
## Example (code)
## Related (links to other patterns + cookbook reference)
```

---

## Pinterest

**Purpose:** evergreen visual discovery (indirect — Google Images indexing)
**Create:** diagrams, checklists, architecture visuals (1200x1500, dark bg, one accent color)
**Publish:** manual for now (D-019). 3-pin experiment first (pain / checklist / comparison)
**Link:** canonical website article (not book page)
**SEO:** descriptive filename (`nodriver-browser-profile-lifecycle.png`), full alt text, title+description contain natural keywords
**Never:** sales graphics, book covers, promotional copy on the image

---

## Dev.to

**Purpose:** search + technical authority
**Format:** full article, exactly ONE CTA link with `?ref=<slug>` at the end
**Canonical:** always set to website URL
**Tags:** max 4, alphanumeric, no hyphens
**Workflow:** publish as draft → verify via `/api/articles/me/unpublished` → set `published: true` → update → verify final URL (slug changes on publish)

---

## Website (conversion owner)

**Purpose:** convert. Sell here — this is the one place selling belongs.
**Flow:** article → related concepts/examples (internal links) → book page → Gumroad
**Never:** no-CTA doctrine here. The website converts aggressively.

---

## Hacker News

**Purpose:** selective credibility
**Post only when:** genuinely useful — open-source pattern repo, benchmark, technical investigation
**Never:** every article, book promotion, "I wrote a cookbook"
