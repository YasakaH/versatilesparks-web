# Chapter 2: Browser Control

## The Problem This Chapter Solves

Launching a browser is one thing. Controlling it — navigating, capturing state, running scripts inside pages, inspecting cookies — is another. Most developers know the first recipe and skip the next three. Then they hit a problem that screenshots or JavaScript or state inspection would have solved in seconds.

This chapter covers four browser control operations you will use in nearly every automation project.


## Recipe 5: Navigate Like a User

**File:** `recipes/05_navigation.py`

### Why This Matters

Navigation is not just "go to a URL." You need to scroll, wait for JavaScript-rendered content, and verify where the browser ended up. A navigation that works on your machine may timeout on a server.

### The Code

```python
import asyncio
from common.browser import launch_browser, close_browser

async def main():
    browser = await launch_browser()
    page = await browser.get("https://httpbin.org")
    await page.scroll_down(delta_y=500)
    await page.sleep(1)
    url = page.url
    print(f"Current URL: {url}")
    await close_browser(browser)

if __name__ == "__main__":
    asyncio.run(main())
```

### Code Walkthrough

`browser.get()` waits for the load event. `scroll_down()` moves the viewport. `page.url` reads the current URL synchronously.

### Production Rule

Do not use `time.sleep()`. Use nodriver's built-in wait mechanisms (Recipe 9).

### Used In Real Projects

**Good fit:** Any automation that visits multiple pages.
**Avoid:** API-first applications where the browser is just a rendering layer.


## Recipe 6: Capture Screenshots

**File:** `recipes/06_screenshots.py`

### Why This Matters

Screenshots are your primary debugging tool when automation runs unattended. A log message says "button not found." A screenshot shows *why* — cookie banner covering it, page still loading, unexpected error page.

### The Code

```python
import asyncio
from common.browser import launch_browser, close_browser

async def main():
    browser = await launch_browser()
    page = await browser.get("https://example.com")
    await page.save_screenshot()
    print("Screenshot captured")
    await close_browser(browser)

if __name__ == "__main__":
    asyncio.run(main())
```

### Code Walkthrough

`page.save_screenshot()` captures the visible viewport. Without a path argument, it saves to a timestamped filename. Provide a path to save with a known name.

### Production Rule

Capture screenshots on failure, not on every step. Too many screenshots slow automation and fill disk space.

### Used In Real Projects

**Good fit:** Debugging CI failures, visual regression testing, generating previews.
**Avoid:** High-frequency automation where disk I/O matters.


## Recipe 7: Execute JavaScript in the Page

**File:** `recipes/07_javascript.py`

### Why This Matters

Not everything is exposed through nodriver's API. Sometimes you need to read data that only exists in JavaScript memory, trigger a function, or measure page performance. `evaluate()` is your escape hatch.

### The Code

```python
import asyncio
from common.browser import launch_browser, close_browser

async def main():
    browser = await launch_browser()
    page = await browser.get("https://example.com")
    try:
        result = await page.evaluate("document.title")
        print(f"Title via JS: {result}")
        dimensions = await page.evaluate("({w: innerWidth, h: innerHeight})")
        print(f"Viewport: {dimensions['w']}x{dimensions['h']}")
    except Exception as e:
        print(f"JS execution failed: {e}")
    await close_browser(browser)

if __name__ == "__main__":
    asyncio.run(main())
```

### Code Walkthrough

`page.evaluate()` runs JavaScript in the page context. Return values are serialized to JSON. You can return numbers, strings, arrays, objects. You cannot return DOM elements or functions.

### Why It Fails

| Issue | Symptom | Fix |
|-------|---------|-----|
| Page not loaded | Timeout | Wait before evaluating |
| DOM element returned | Serialization error | Extract properties in JS |
| Content Security Policy | Blocked | Cannot bypass |
| Too-large result | Truncated | Return smaller objects |

### Production Rule

Always wrap `evaluate()` in try/except. JS execution is the most common single point of failure in browser automation.

### Used In Real Projects

**Good fit:** Extracting SPA state, triggering React/Vue actions, reading performance metrics.
**Avoid:** Data available through `element.text` or `element.attrs` — those are faster.


## Recipe 8: Inspect Browser State

**File:** `recipes/08_browser_state.py`

### Why This Matters

Automation produces side effects: cookies set, local storage populated, session tokens created. Inspecting this state is how you verify that your automation actually did what you think it did.

### The Code

```python
import asyncio
from common.browser import launch_browser, close_browser

async def main():
    browser = await launch_browser()
    page = await browser.get("https://httpbin.org/cookies/set?name=value")
    cookies = browser.cookies
    print(f"Cookies: {cookies}")
    ls = await page.get_local_storage()
    print(f"Local storage: {ls}")
    await close_browser(browser)

if __name__ == "__main__":
    asyncio.run(main())
```

### Code Walkthrough

`browser.cookies` returns all browser cookies as a list of dictionaries. Each includes `name`, `value`, `domain`, `path`, `httpOnly`, `secure`, and `expires`. `get_local_storage()` returns all local storage key-value pairs for the current origin.

### Production Rule

Read state to verify automation side effects. Do not assume the browser state is what you expect.

### Used In Real Projects

**Good fit:** Debugging login flows, verifying session persistence, auditing cookie scope.
**Avoid:** Production logging of cookie values (security risk).


