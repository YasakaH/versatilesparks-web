# Deployment — versatilesparks.qzz.io

Workflow and commands for the hosting architecture. Account identifiers and
machine-specific paths are intentionally **not** here — they live in the
local, gitignored `docs/DEPLOYMENT_PRIVATE.md`.

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

## Pages project

| Item | Value |
|---|---|
| Project name | `versatilesparks` |
| Domains | `versatilesparks.pages.dev`, `versatilesparks.qzz.io` |
| Production branch | `main` |
| Output dir | `website-next/out` (static export, `trailingSlash: true`) |

The canonical hostname is its own Cloudflare zone (not a record under a parent
zone), so the custom domain binding is independent.

## GitHub secrets (YasakaH/versatilesparks-web)

| Secret | Purpose |
|---|---|
| `CLOUDFLARE_API_TOKEN` | Scoped token (Account → Cloudflare Pages → Edit) |
| `CLOUDFLARE_ACCOUNT_ID` | Account identifier |

Both set and validated (workflow run `30675512185`, 2026-08-01, success).
Tokens are never committed; they live in GitHub Actions secrets and the local
hermes `.env`.

## Commands

Manual deploy (fallback when CI not used):

```
cd website-next
npm run build
npx wrangler pages deploy website-next/out --project-name=versatilesparks --branch main
```

CI trigger: push to `main` touching `website-next/**`, or `workflow_dispatch`.

Verify after deploy:

- https://versatilesparks.qzz.io/ → 200
- https://versatilesparks.qzz.io/blog/why-browser-profiles-break/ → 200 (GitHub pattern links + Gumroad CTA)
- https://versatilesparks.qzz.io/sitemap.xml → 200 (a stale 404 after deploy is an edge cache artifact; it self-heals or add `?cb=` to bust)

## Notes / footguns

- `npm run build` wipes `website-next/out/` (deleted the CNAME during Iteration 13 — only relevant if GH Pages is ever re-enabled, which it should not be).
- Never run `git add -A` from inside the cookbook while a deployment repo's `.git` is missing — this is how `.reddit-creds.json` leaked (Iteration 13 post-mortem).
- `knowledge/hpf-core` is a nested repo — never commit it to the publishing repo (gitlink removed 2026-08-01).
- API token minting is dashboard-only; wrangler OAuth scopes cannot create tokens.
- OAuth access via `npx wrangler login` only (refresh token auto-renews on this machine).
