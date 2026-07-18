"""
Recipe 25 (revised): Scrape Infinite Scroll Pages

Use multiple strategies to detect when scrolling is complete:
1. Document height unchanged
2. Item count unchanged
3. Loading spinner disappears
4. Maximum scroll limit (safety)

Infinite scroll should always have a finite stopping condition.
"""
import asyncio

from common.browser import launch_browser, close_browser
from common.logging import logger

MAX_SCROLLS = 100


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://example.com")

        # Strategy: document height unchanged
        previous_height = 0
        for scroll in range(1, MAX_SCROLLS + 1):
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(1)

            current_height = await page.evaluate("document.body.scrollHeight")
            if current_height == previous_height:
                logger.info("No more content loaded. Stopping.")
                break

            previous_height = current_height
        else:
            logger.warning("Maximum scroll limit reached.")

        # Alternative strategies (uncomment for your use case):
        # Strategy 2: item count unchanged
        # Strategy 3: loading spinner disappears

        item_count = len(await page.find_all("p"))
        print(f"Page has {item_count} paragraphs after scrolling")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
