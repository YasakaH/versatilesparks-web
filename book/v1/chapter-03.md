# Chapter 3: Production Foundations

## The Problem This Chapter Solves

Developers skip the "boring" stuff — waiting, retrying, logging, configuration — and jump straight to interaction scripts. Their scripts work for a day, then break on a slow network, a missing element, or an unhandled error. The boring stuff is not boring. It is the difference between a script and a system.


## Recipe 9: Wait for Meaningful State

**File:** `recipes/09_wait_for_elements.py`

### Why This Matters

The most common root cause of automation failures is acting before the page is ready. Developers write `time.sleep(3)` which works on their machine and breaks on the server. The fix is not a longer sleep. The fix is waiting for a specific condition.

### Wait for What Matters

| Condition | What it signals | How to Wait |
|-----------|----------------|-------------|
| Element exists | In the DOM | `page.find("selector", timeout=N)` |
| Text appears | Content rendered | `page.wait_for(text="...")` |
| Spinner disappears | Loading finished | Poll until not found |
| URL changed | Navigation completed | Check `page.url` |
| Element removed | Action processed | Poll until element gone |

### The Code

```python
import asyncio
from common.browser import launch_browser, close_browser

async def main():
    browser = await launch_browser()
    page = await browser.get("https://example.com")
    heading = await page.find("h1", timeout=5)
    if heading:
        print(f"Heading: {heading.text}")
    link = await page.find("a")
    if link:
        print(f"First link: {link.text}")
    await close_browser(browser)

if __name__ == "__main__":
    asyncio.run(main())
```

### Code Walkthrough

`page.find()` with a `timeout` waits up to that many seconds. nodriver retries internally. Without a timeout, it returns immediately or returns None.

### Decision Table: Wait Strategy

| Page Type | Strategy | Why |
|-----------|----------|-----|
| Static HTML | No wait | Content is immediate |
| Server-rendered | `find()` with 5s timeout | Server response time |
| SPA | `find()` + text check | JS renders asynchronously |
| Infinite scroll | Scroll + item count | Multiple load events |
| With loading spinners | Wait for spinner to disappear | Signals loading complete |

### Production Rule

Never use `time.sleep()`. Wait for a specific condition. If you do not know what to wait for, your automation is guessing.

### Used In Real Projects

**Good fit:** Every automation project without exception.
**Avoid:** No situation. You always need to wait for something.


## Recipe 10: Retry Transient Failures

**File:** `recipes/10_retry_failures.py`

### Why This Matters

Networks fail. Servers timeout. Pages crash. Some failures are temporary and worth retrying. Others are permanent and retrying wastes time. The skill is knowing the difference.

### When to Retry vs When to Stop

| Failure | Retry? | Why |
|---------|--------|-----|
| TimeoutError | ✅ | Network blip, server under load |
| ConnectionError | ✅ | Temporary routing issue |
| HTTP 500 / 502 / 503 | ✅ | Server may recover |
| Element not found once | ✅ | Page may not be ready |
| Invalid CSS selector | ❌ | Will never work |
| Invalid credentials | ❌ | Will never work |
| CAPTCHA | ❌ | Will not resolve itself |
| Element not found after 3 retries | ❌ | Page likely changed |

### The Code

```python
import asyncio
from common.browser import launch_browser, close_browser
from common.retry import retry

async def main():
    browser = await launch_browser()
    page = await retry(
        browser.get,
        "https://httpbin.org/delay/3",
        exceptions=(TimeoutError, ConnectionError),
        max_retries=3,
        delay=1,
    )
    print(f"Loaded: {await page.title()}")
    await close_browser(browser)

if __name__ == "__main__":
    asyncio.run(main())
```

### Code Walkthrough

The `retry()` helper takes a callable and retryable exceptions. If the callable raises one of those, it waits `delay` seconds and tries again, up to `max_retries` times.

**Bad practice:**
```python
await retry(fn, exceptions=(Exception,))  # Retries everything
```
A selector typo gets retried 3 times before failing. Wasted time, hides bugs.

**Good practice:**
```python
await retry(fn, exceptions=(TimeoutError, ConnectionError))  # Only transient
```
A typo fails immediately on the first call. You see the error and fix it.

### Production Rule

Be specific about which exceptions to retry. A broad `except Exception` hides bugs behind retries.

### Used In Real Projects

**Good fit:** Network-dependent operations, page loads, form submissions.
**Avoid:** Local operations (file reads, selector queries) that never fail transiently.


## Recipe 11: Add Useful Logging

**File:** `recipes/11_logging.py`

### Why This Matters

Unattended automation produces no visible output. When it fails, you need to know *where* and *why* without re-running. Good logging answers both questions.

### The Code

```python
import asyncio
from common.browser import launch_browser, close_browser
from common.logging import logger

async def main():
    logger.info("Starting browser automation")
    browser = await launch_browser()
    logger.info("Browser launched")
    page = await browser.get("https://example.com")
    title = await page.title()
    logger.info(f"Page loaded: {title}")
    await close_browser(browser)
    logger.info("Done")

if __name__ == "__main__":
    asyncio.run(main())
```

### Code Walkthrough

The `logger` wraps Python's standard logging with a consistent format. Log levels:

| Level | When to Use |
|-------|-------------|
| `debug` | Development details you turn off in production |
| `info` | Normal progress milestones |
| `warning` | Something unexpected but recoverable |
| `error` | Failure that stops automation |

### Production Rule

Log at `info` for normal progress and `error` for failures. Use `debug` during development and turn it off in production. Too much logging is as bad as too little.

### Used In Real Projects

**Good fit:** Every unattended automation run.
**Avoid:** Outputting sensitive data (passwords, tokens, personal information).


## Recipe 12: Customize Cookbook Configuration

**File:** `recipes/12_configuration.py`

### Why This Matters

Hardcoded values — timeouts, ports, headless mode — make automation brittle. The same code that runs on your laptop must run on a server with different settings.

### The Code

```python
import asyncio
from common.config import HEADLESS, TIMEOUT, LOG_LEVEL, logger
from common.browser import launch_browser, close_browser

async def main():
    logger.info(f"Headless: {HEADLESS}, Timeout: {TIMEOUT}s, Log level: {LOG_LEVEL}")
    browser = await launch_browser()
    page = await browser.get("https://example.com", timeout=TIMEOUT)
    await close_browser(browser)

if __name__ == "__main__":
    asyncio.run(main())
```

### Code Walkthrough

`config.py` reads environment variables with sensible defaults:

| Variable | Default | Override | Description |
|----------|---------|----------|-------------|
| `HEADLESS` | `false` | `HEADLESS=true` | Run without GUI |
| `TIMEOUT` | `30` | `TIMEOUT=60` | Default operation timeout |
| `LOG_LEVEL` | `info` | `LOG_LEVEL=debug` | Logging verbosity |

### Production Rule

Environment variables for configuration. Same code, different environments.

### Used In Real Projects

**Good fit:** Deploying the same code to dev, staging, and production environments.
**Avoid:** Hardcoding production credentials in scripts (use environment variables or a secrets manager).


