"""
Recipe 28 (revised): Build Automation That Resembles Normal Browser Usage

Configure browser sessions and interaction patterns that reduce
unnecessary automation friction through consistency, not tricks.
"""
import asyncio
from pathlib import Path

from common.browser import launch_browser, close_browser

PROFILE_DIR = Path("profiles/recipe28")


async def main():
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    browser = await launch_browser(
        user_data_dir=PROFILE_DIR,
    )

    try:
        page = await browser.get("https://example.com")
        title = await page.evaluate("document.title")
        print(f"Profile: {PROFILE_DIR.resolve()}")
        print(f"Title:   {title}")

        # What helps:
        # - Reuse browser profiles for consistent state
        # - Maintain consistent viewport/language (set in config.py)
        # - Wait for meaningful application state
        # - Reuse authenticated sessions
        # - Avoid unnecessary browser restarts

        # What NOT to rely on:
        # - Random mouse movement or typing delays
        # - User-agent rotation
        # - Proxy rotation or fingerprint spoofing
        # These are context-dependent, not universal best practices.

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
