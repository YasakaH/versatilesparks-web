# Deployment — versatilesparks.qzz.io

Permanent reference for the hosting architecture. Verified live 2026-08-01.

## Architecture

```
git push (main, website-next/**)
        ↓
GitHub Actions (deploy.yml)
        ↓
npm ci && npm run build (website-next/)
        ↓
wrangler pages deploy website-next/out --project-name=versatilesparks
        ↓
Cloudflare Pages → versatilesparks.qzz.io
```

One origin. DNS untouched (stays Cloudflare). GitHub Pages: retired, do not re-enable.

## Cloudflare account

| Item | Value |
|---|---|
| Email | `libdynwordpress@yahoo.com` |
| Account ID | `64fde5841a5f46bceb8bff5ccffa6a34` |
| Login method | `npx wrangler login` (OAuth, browser) |

Wrangler stores credentials at
`C:\Users\varas\AppData\Roaming\xdg.config\.wrangler\config\default.toml`
(note: NOT `~/.wrangler` on this machine). The OAuth token has `pages:write`,
`zone:read`, `ssl_certs:write` — enough to deploy manually, not enough to
mint API tokens (403) or purge cache (401).

## Pages project

| Item | Value |
|---|---|
| Project name | `versatilesparks` |
| Domains | `versatilesparks.pages.dev`, `versatilesparks.qzz.io` |
| Production branch | `main` |
| Output dir | `website-next/out` (static export, `trailingSlash: true`) |

## Zones in this account

- `versatilesparks.qzz.io` — **its own zone** (not a record under `qzz.io`); DNS record for the Pages binding lives here
- `libdynconnect.com` — unrelated zone, same account

## GitHub secrets (YasakaH/versatilesparks-web)

| Secret | Value source |
|---|---|
| `CLOUDFLARE_API_TOKEN` | Dashboard → Profile → API Tokens (scoped: Account → Cloudflare Pages → Edit). Stored: GitHub Actions secret + hermes `.env`. **Never commit.** |
| `CLOUDFLARE_ACCOUNT_ID` | See table above. Stored: GitHub Actions secret + hermes `.env`. |

Token status: set and validated via workflow run `30675512185` (2026-08-01, success).

## Commands

Manual deploy (fallback when CI not used):

```
cd website-next
npm run build
npx wrangler pages deploy website-next/out --project-name=versatilesparks --branch main
```

CI trigger: push to `main` touching `website-next/**` or `workflow_dispatch`.

Verify after deploy:

- https://versatilesparks.qzz.io/ → 200
- https://versatilesparks.qzz.io/blog/why-browser-profiles-break/ → 200 (GitHub pattern links + Gumroad CTA)
- https://versatilesparks.qzz.io/sitemap.xml → 200 (a stale 404 after deploy is an edge cache artifact; it self-heals or add `?cb=` to bust)

## Notes / footguns

- `npm run build` wipes `website-next/out/` (deleted the CNAME during Iteration 13 — only relevant if GH Pages is ever re-enabled, which it should not be).
- Never run `git add -A` from inside the cookbook while a deployment repo's `.git` is missing — this is how `.reddit-creds.json` leaked (Iteration 13 post-mortem).
- `knowledge/hpf-core` is a nested repo — never commit it to the publishing repo (gitlink removed 2026-08-01).
- API token minting is dashboard-only; the OAuth scopes cannot create tokens.
