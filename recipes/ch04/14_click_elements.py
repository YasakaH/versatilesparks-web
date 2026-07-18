"""
Recipe 14 (revised): Click Elements Reliably

A visible element is not necessarily a clickable element.
Always verify: exists → visible → enabled → not blocked by overlay.
"""
import asyncio

from common.browser import launch_browser, close_browser
from common.logging import logger


async def click_safely(page, selector):
    """Find, scroll to, wait for enabled, then click."""
    button = await page.find(selector)
    await button.scroll_into_view()

    # Wait for element to become enabled
    while button.attrs.get("disabled") is not None:
        await asyncio.sleep(0.2)

    try:
        await button.click()
    except Exception as exc:
        logger.error("Click failed: %s", exc)
        raise


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://example.com")

        link = await page.find("a")
        print(f"Clicking: {link.text}")
        await click_safely(page, "a")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
