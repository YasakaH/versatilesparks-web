"""Example recipe: find and click an element."""

import asyncio
from common.browser import launch_browser, close_browser
from common.logging import logger


async def main():
    logger.info("Starting example recipe")
    browser = await launch_browser()
    page = await browser.get("https://example.com")
    link = await page.find("a")
    if link:
        logger.info(f"Found link: {link.text}")
    await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
