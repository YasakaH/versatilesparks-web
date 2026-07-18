# Chapter 1: Getting Started

## The Problem This Chapter Solves

Browser automation fails most often because developers treat the browser as a simple object. It is not. It is a separate operating system process that speaks a wire protocol. Launching it, managing its lifecycle, and reusing its state across runs are not "setup steps." They are the foundation your automation reliability depends on.

This chapter covers four recipes. Each solves one piece of the browser lifecycle:

1. Launch and close — the minimal loop
2. Tabs — working with multiple pages
3. Profiles — persisting state across runs
4. Configuration — controlling how the browser starts


## Recipe 1: Launch and Close a Browser

**File:** `recipes/01_launch_browser.py`

### Why This Matters

Your Python code controls a **separate Chrome process** through a **WebSocket connection**. This is not a library calling internal functions. It is an inter-process communication channel. If you do not understand this, every timeout error and connection refused will look like a bug when it is actually a lifecycle misunderstanding.

The minimal loop — launch, navigate, close — is the heartbeat of every automation project. Get this right and everything else follows.

### The Code

```python
import asyncio
from common.browser import launch_browser, close_browser

async def main():
    browser = await launch_browser()
    page = await browser.get("https://example.com")
    title = await page.title()
    print(f"Page title: {title}")
    await close_browser(browser)

if __name__ == "__main__":
    asyncio.run(main())
```

### Code Walkthrough

`launch_browser()` starts Chrome with a temporary profile and connects via CDP. Every call gets a clean session with no leftover state from previous runs.

`browser.get()` navigates to a URL and returns an object representing the page. It waits for the page's load event before returning.

`await page.title()` retrieves the document title. This is a simple CDP script evaluation.

`close_browser()` terminates the browser process. If you forget this, Chrome stays running in the background.

### Decision Table

| Goal | Fresh launch | Reuse profile |
|------|-------------|---------------|
| One-off scrape | ✅ | ❌ |
| Run every hour | ❌ | ✅ |
| Test environment | ✅ | ❌ |
| Authenticated session | ❌ | ✅ |

### Production Rule

Always call `close_browser()`. An orphaned browser process consumes memory and may block the CDP port for the next run.

### Used In Real Projects

**Good fit:** One-off scrapes, testing, development exploration.
**Avoid:** Long-running servers where browser instances accumulate.


## Recipe 2: Open and Manage Browser Tabs

**File:** `recipes/02_manage_tabs.py`

### Why This Matters

Each browser tab is an independent execution context with its own cookies, local storage, and DOM. When you open a new tab, you get a fresh environment even within the same browser process. This is useful for parallel scraping, multi-account testing, and separating concerns without launching multiple browser processes.

### The Code

```python
import asyncio
from common.browser import launch_browser, close_browser

async def main():
    browser = await launch_browser()
    tab1 = await browser.get("https://example.com")
    tab2 = await browser.create_new_page()
    await tab2.get("https://httpbin.org")
    all_tabs = browser.tabs
    print(f"Open tabs: {len(all_tabs)}")
    await tab1.bring_to_front()
    await close_browser(browser)

if __name__ == "__main__":
    asyncio.run(main())
```

### Code Walkthrough

`browser.create_new_page()` opens a blank tab. `browser.get()` can also create a new tab if the current one is busy. `browser.tabs` returns the list of open tab objects. `bring_to_front()` activates a specific tab, which matters for screenshots and focus-dependent interactions.

### Decision Table

| Scenario | New tab | Reuse tab |
|----------|---------|-----------|
| Parallel data collection from different domains | ✅ | ❌ |
| Sequential navigation on one site | ❌ | ✅ |
| Login first, then scrape | ❌ | ✅ |
| Compare two pages simultaneously | ✅ | ❌ |

### Production Rule

Use tabs for parallel work, not sequential steps. A single tab with sequential navigation is simpler and less error-prone.

### Used In Real Projects

**Good fit:** Price comparison, multi-site monitoring, A/B testing tools.
**Avoid:** Long-running automation where tabs accumulate memory.


## Recipe 3: Reuse a Browser Profile Across Sessions

**File:** `recipes/03_persistent_profile.py`

### Why This Matters

Every fresh browser launch starts with no cookies, no local storage, no saved logins. For automation that needs to stay logged in across runs, you need a persistent profile directory. The profile is a directory on your filesystem where Chrome stores its state. Point to the same directory every time, and you get the same session.

### What's Inside a Browser Profile

| Data | Stored? | Useful For |
|------|---------|------------|
| Cookies | ✅ | Login session |
| Local storage | ✅ | Site preferences |
| Cache | ✅ | Faster page loads |
| Extensions | ✅ | Custom browser tools |
| History | ❌ | Not useful for automation |

### The Code

```python
import asyncio
from pathlib import Path
from common.browser import launch_browser, close_browser

PROFILE_DIR = Path("./profiles/my_profile")
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

async def main():
    browser = await launch_browser(user_data_dir=str(PROFILE_DIR))
    page = await browser.get("https://example.com")
    print(f"Using profile: {PROFILE_DIR}")
    await close_browser(browser)

if __name__ == "__main__":
    asyncio.run(main())
```

### Code Walkthrough

`user_data_dir` tells Chrome where to store and load profile data. On the first run, Chrome creates the directory with default settings. On subsequent runs, Chrome loads the existing data, including cookies and local storage.

### Decision Table

| Factor | Fresh profile | Persistent profile |
|--------|---------------|-------------------|
| Start clean | ✅ Always | ❌ Has previous state |
| Resume login | ❌ | ✅ |
| Disk usage | None | ~50 MB after first run |
| Reproducibility | High | Depends on state |
| Security risk | Minimal | Profile has data |

### Production Rule

Use persistent profiles for authenticated sessions. Use fresh profiles for one-off scrapes where reproducibility matters more than speed.

### Used In Real Projects

**Good fit:** Daily dashboard data collection, admin panel automation, internal tool workflows.
**Avoid:** CI/CD pipelines where each run must start from a known clean state.


## Recipe 4: Customize Browser Startup Options

**File:** `recipes/04_configure_startup.py`

### Why This Matters

Default Chrome settings assume a human user with a monitor and keyboard. Automation often needs no window, no extensions, no audio, or a specific viewport. These are not preferences. They are configuration that affects whether your automation works at all in a given environment.

### The Code

```python
import asyncio
import os
from common.browser import launch_browser, close_browser

async def main():
    headless = os.environ.get("HEADLESS", "false").lower() == "true"
    browser = await launch_browser(
        headless=headless,
        window_size=(1920, 1080),
        arguments=["--disable-extensions", "--mute-audio"],
    )
    page = await browser.get("https://example.com")
    print(f"Headless: {headless}")
    await close_browser(browser)

if __name__ == "__main__":
    asyncio.run(main())
```

### Code Walkthrough

`launch_browser()` passes `headless`, `window_size`, and `arguments` through to Chrome. The `config.py` module provides defaults so you don't repeat arguments in every script.

### Decision Table

| Argument | Effect | Use Case |
|----------|--------|----------|
| `--headless=new` | No visible window | Servers, CI |
| `--window-size=1920,1080` | Large desktop viewport | Layout-dependent automation |
| `--disable-extensions` | Fewer processes, less memory | Scraping |
| `--mute-audio` | No sound | Background execution |
| `--proxy-server=...` | Route traffic | IP rotation, geo-testing |

### Production Rule

Put browser arguments in `config.py`, not in your recipe scripts. When a Chrome update deprecates an argument, you change it in one place.

### Used In Real Projects

**Good fit:** Server deployments, Docker containers, scheduled cron tasks.
**Avoid:** No situation — every automation project needs configuration.


