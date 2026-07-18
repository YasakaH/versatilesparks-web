"""
Recipe 10 (revised): Retry Transient Failures

Automatically retry temporary browser failures using the shared
retry helper. Not every failure deserves another attempt —
learn which ones do.
"""
import asyncio

from common.browser import launch_browser, close_browser
from common.retry import retry


async def main():
    browser = await launch_browser()

    try:
        # ✅ Good: retry only transient failures
        page = await retry(
            browser.get,
            "https://example.com",
            exceptions=(TimeoutError, ConnectionError),
            max_retries=3,
            delay=1,
        )

        title = await page.evaluate("document.title")
        print(f"Title: {title}")

        # ❌ Bad: retrying a permanent failure (wrong selector)
        # await retry(
        #     page.find,
        #     "div.this-selector-does-not-exist",
        #     exceptions=(Exception,),  # Too broad!
        # )
        # No amount of retries fixes an incorrect selector.

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
