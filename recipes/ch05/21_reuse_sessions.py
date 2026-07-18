"""
Recipe 21 (revised): Reuse Authenticated Sessions

Never trust saved cookies until the application proves the session
is still authenticated. Pattern: load → verify → login if expired.
"""
import asyncio
from pathlib import Path

from common.browser import launch_browser, close_browser
from common.logging import logger

COOKIE_FILE = Path("cookies/authenticated.json")


async def session_valid(page) -> bool:
    """Check whether the current session is still authenticated."""
    await page.get("https://example.com")
    account = await page.find("[data-testid='account-menu']", timeout=2)
    return account is not None


async def login(page):
    """Login routine from Recipe 19."""
    logger.info("Logging in...")
    # await (await page.find("#email")).send_keys(USERNAME)
    # await (await page.find("#password")).send_keys(PASSWORD)
    # await (await page.find("button[type='submit']")).click()


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://example.com")

        # Load cookies here (from Recipe 20)

        if await session_valid(page):
            logger.info("Existing session is valid.")
        else:
            logger.info("Session expired. Logging in.")
            await login(page)
            # Save fresh cookies here

        print(f"Session ready: {await page.evaluate('document.title')}")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
