# Platform Policies & Constraints

Distribution rules per platform. Check this file before writing or posting derivatives.

| Platform  | Links | Notes |
| --------- | ----- | ----- |
| Dev.to    | ✅ allowed (1 CTA link max, canonical_url set) | tags: max 4, alphanumeric only, no hyphens |
| X/Twitter | ✅ allowed | thread spacing: ~5 min between tweets; no aggressive CTA |
| Reddit    | ⚠️ allowed but discouraged at first | no book mentions; discussion-first; link only after engagement |
| Quora     | ❌ NOT allowed | answers must be fully self-contained (policy since 2024); mention article topic only, no URL |
| LinkedIn  | ✅ allowed | ACCOUNT BANNED - do not plan LinkedIn distribution |
| YouTube   | ✅ allowed (description) | CHANNEL NOT CREATED - defer all video work |
| Hashnode  | ✅ allowed | token not configured |
| Medium    | ⚠️ | MEDIUM_TOKEN not in .env - blocked |
| GitHub    | ✅ allowed | HIGHEST priority channel for dev audience; free patterns repo (not book content); repo `YasakaH/nodriver-production-patterns` NOT created yet |
| GitHub Pages | ✅ allowed | free, Google-indexed; `username.github.io/nodriver-production-patterns` |
| Pinterest | ✅ allowed | diagrams/checklists/infographics only; never sales text; evergreen |
| Hacker News | ⚠️ | only genuinely useful submissions (pattern repo, technical write-up, benchmark); NEVER every article; audience overlaps with buyers |

## Derivative types per article

```
articles/derivatives/<article>/
├── x-post.md            # single pain-observation post
├── x-thread.md          # multi-tweet thread
├── reddit.md            # discussion (no link)
├── quora.md             # self-contained answer (NO links)
├── youtube-script.md    # 30s short script (deferred - no channel)
├── linkedin.md          # (blocked - account banned)
├── github-readme.md     # repo README draft
├── github-pattern.md    # one pattern doc for the patterns repo
├── pinterest-pins.md    # pin drafts (title + image text + link)
├── infographic-spec.md  # visual spec for a static image
└── distribution.json    # per-platform publish state
```

## Active constraints (2026-07-31)

1. **LinkedIn** — account banned. Do not produce LinkedIn derivatives; mark `status: blocked` in distribution.json.
2. **YouTube** — no channel. Video derivatives are `status: deferred`.
3. **Quora** — links not allowed in answers. Quora derivatives must be self-contained; never append a URL.

## Writing rules

- Never promise "full breakdown here: <link>" in Quora drafts.
- Reddit posts: no CTA, no book, no initial link.
- Dev.to articles: exactly one CTA link with `?ref=` attribution.
