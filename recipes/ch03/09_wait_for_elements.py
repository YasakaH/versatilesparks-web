"""
Recipe 9 (revised): Wait for Meaningful State

Wait for application state — not just elements, not fixed sleep delays.

Wait for what matters:
  ✅ Element EXISTS     → Login button appeared
  ✅ TEXT changes       → Status message updated
  ✅ ATTRIBUTE changes  → Button became enabled
  ✅ SPINNER gone       → Loading completed
  ✅ Ready state        → Page finished loading

Rule: Wait for the condition that matters, not for an arbitrary
number of seconds. Never use asyncio.sleep() as a wait strategy.
"""
import asyncio

from common.browser import launch_browser, close_browser
from common.logging import logger


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://example.com")

        # Wait for ready state
        await page.wait_for()
        logger.info("Page ready: %s", await page.evaluate("document.readyState"))

        # Wait for element to exist
        heading = await page.select("h1", timeout=10)
        text = heading.text
        print(f"Heading: {text}")

        # ❌ Bad: fixed sleep
        # await asyncio.sleep(5)

        # ✅ Good: wait for meaningful state
        # Wait for button to be enabled (attribute change)
        # Wait for content to load (spinner disappears)
        # Wait for text to appear (text content)

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
