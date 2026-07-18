"""
Recipe 3 (revised): Reuse a Browser Profile Across Sessions

Save your browser profile so cookies, logins, and other browser state
persist between automation runs.

Browser Profile Contents (stored in Chrome's user-data-dir):
  ✅ Cookies, local storage, session storage
  ✅ Browser preferences (language, permissions)
  ✅ Cache, history, extensions
  ❌ Python variables (they exist only while your script runs)
  ❌ Automation logic (your code lives outside the browser)
  ❌ Retry counters, application state in memory

Mental model: The profile remembers browser state, not automation state.
"""
import asyncio
from pathlib import Path

import nodriver as uc

from common.browser import close_browser

PROFILE_DIR = Path("profiles/recipe3")


async def main():
    browser = await uc.start(
        user_data_dir=PROFILE_DIR,
        headless=False,
    )

    try:
        page = await browser.get("https://example.com")
        title = await page.evaluate("document.title")
        print(title)
        print(f"Profile: {PROFILE_DIR.resolve()}")
        print("Run this recipe twice — cookies persist between runs.")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
