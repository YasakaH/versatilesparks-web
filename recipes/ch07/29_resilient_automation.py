"""
Recipe 29 (revised): Build Resilient Browser Automation

Handle interruptions and transient failures. Know when to RETRY
vs when to STOP — not every failure deserves another attempt.
"""
import asyncio

from common.browser import launch_browser, close_browser
from common.logging import logger
from common.retry import retry


async def main():
    browser = await launch_browser()

    try:
        url = "https://example.com"

        try:
            page = await retry(
                browser.get,
                url,
                exceptions=(TimeoutError, ConnectionError),
                max_retries=3,
                delay=1,
            )

        except (TimeoutError, ConnectionError):
            logger.error("Navigation failed after all retry attempts.")
            return

        except Exception:
            logger.exception("Non-retryable error. Stopping automation.")
            return

        title = await page.evaluate("document.title")
        logger.info("Navigation succeeded: %s", title)

        # Verify page state
        ready = await page.evaluate("document.readyState")
        if ready != "complete":
            logger.warning("Page not fully loaded: %s", ready)

        logger.info("Automation completed successfully")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
