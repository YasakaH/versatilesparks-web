"""
Recipe 24 (revised): Handle Pagination

Navigate through multiple pages and collect data from each page.
Always include an exit strategy — never paginate without limits.
"""
import asyncio

from common.browser import launch_browser, close_browser
from common.logging import logger

MAX_PAGES = 100


async def extract_current_page(page):
    """Extract data from the current page."""
    items = await page.find_all("p")
    return [item.text for item in items if item.text.strip()]


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://example.com")
        results = []

        for page_number in range(1, MAX_PAGES + 1):
            results.extend(await extract_current_page(page))
            logger.info("Page %s: %s items", page_number, len(results))

            next_button = await page.find(
                "[data-testid='next-page']",
                timeout=2,
            )

            if next_button is None:
                logger.info("No next page found.")
                break

            disabled = next_button.attrs.get("disabled")
            if disabled is not None:
                logger.info("Last page reached.")
                break

            await next_button.click()
        else:
            logger.warning("Stopped after reaching MAX_PAGES (%s).", MAX_PAGES)

        print(f"Collected {len(results)} items total")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
