"""
Recipe 12: Customize Cookbook Configuration

Centralize browser defaults so every recipe shares consistent
behavior.
"""
import asyncio

from common.browser import launch_browser, close_browser
from common.config import HEADLESS, DEFAULT_TIMEOUT, WINDOW_SIZE


async def main():
    print(f"HEADLESS={HEADLESS}, TIMEOUT={DEFAULT_TIMEOUT}s, WINDOW={WINDOW_SIZE}")

    browser = await launch_browser(headless=HEADLESS)

    try:
        page = await browser.get("https://example.com")
        print(f"Title: {await page.evaluate('document.title')}")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
