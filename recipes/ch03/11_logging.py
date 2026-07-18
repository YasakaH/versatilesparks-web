"""
Recipe 11: Add Useful Logging to Browser Automation

Produce logs that help diagnose failures without overwhelming
your output.
"""
import asyncio

from common.browser import launch_browser, close_browser
from common.logging import logger


async def main():
    logger.info("Starting browser")
    browser = await launch_browser()

    try:
        logger.info("Navigating to example.com")
        page = await browser.get("https://example.com")

        title = await page.evaluate("document.title")
        logger.info(f"Page loaded: {title}")

    except Exception as e:
        logger.error(f"Automation failed: {e}")
        raise

    finally:
        logger.info("Closing browser")
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
