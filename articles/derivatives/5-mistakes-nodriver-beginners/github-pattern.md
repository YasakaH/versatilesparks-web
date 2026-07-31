# GitHub — Pattern Doc Draft

Lives at `patterns/retry-with-backoff.md` in `YasakaH/nodriver-production-patterns`

---

# Retry with Backoff

## Problem

In production, failures are the norm. A network timeout, a CAPTCHA redirect, or a missing element kills a naive script — usually at 2 AM.

## Rules

1. **Retry with exponential backoff** (2s, 4s, 8s...), never a hot loop.
2. **Fail loudly on the last attempt** — a retry chain that swallows the final error hides the job.
3. **Health-check the browser before retrying** — if the browser died, retrying the URL won't help.

## Example

```python
import asyncio

async def robust_get(browser, url, retries=3):
    for attempt in range(retries):
        try:
            return await browser.get(url)
        except Exception as e:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)
```

## Related

- `browser-profile-management.md`
- `production-readiness.md`
