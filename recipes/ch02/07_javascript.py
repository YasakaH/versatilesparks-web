"""
Recipe 7 (revised): Execute JavaScript in the Page

Run JavaScript inside the browser to retrieve information.
Always handle JS evaluation failures — they WILL happen in production.

Why evaluate() can fail:
- Invalid JavaScript (syntax errors)
- Page navigated mid-execution
- Referencing undefined variables
- Browser disconnected

Serialization limits:
  ✅ Works: strings, numbers, booleans, arrays, plain objects
  ❌ Doesn't work: live DOM elements, Window objects, functions
  Use evaluate() to retrieve DATA, not browser objects.
"""
import asyncio

from common.browser import launch_browser, close_browser
from common.logging import logger


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://example.com")

        try:
            title = await page.evaluate("document.title")
            url = await page.evaluate("location.href")
            ready = await page.evaluate("document.readyState")
        except Exception as exc:
            logger.error("JavaScript evaluation failed: %s", exc)
            return

        print(f"Title:  {title}")
        print(f"URL:    {url}")
        print(f"Ready:  {ready}")

        # ❌ These would FAIL — can't return live DOM objects:
        # await page.evaluate("document.body")  # HTMLBodyElement
        # await page.evaluate("window")         # Window object

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
