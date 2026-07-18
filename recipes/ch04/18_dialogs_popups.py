"""
Recipe 18 (revised): Handle Dialogs, Pop-ups & Unexpected Modals

Treat unexpected modals as recoverable UI state, not fatal errors.
Recovery pattern: attempt → blocked? → detect modal → dismiss → retry once.
"""
import asyncio

from common.browser import launch_browser, close_browser
from common.logging import logger


async def dismiss_cookie_banner(page):
    """Dismiss cookie consent banners if present."""
    banner = await page.find(
        "[data-testid='accept-cookies'], button:has-text('Accept')",
        timeout=2,
    )
    if banner:
        await banner.click()
        logger.info("Cookie banner dismissed.")
        return True
    return False


async def click_with_modal_recovery(page, selector):
    """Click an element, recovering from one unexpected modal."""
    try:
        await (await page.find(selector)).click()
    except Exception:
        await dismiss_cookie_banner(page)
        # Retry once after removing the blocker
        await (await page.find(selector)).click()


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://example.com")

        await dismiss_cookie_banner(page)
        print(f"Page ready: {await page.evaluate('document.title')}")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
