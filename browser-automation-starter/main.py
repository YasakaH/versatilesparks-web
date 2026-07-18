import asyncio
from common.browser import launch_browser, close_browser
from common.logging import logger


async def main():
    logger.info("Starting automation")
    browser = await launch_browser()
    page = await browser.get("https://example.com")
    title = await page.title()
    logger.info(f"Loaded: {title}")
    await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
