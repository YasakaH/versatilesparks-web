"""
Recipe 1: Launch Your First Browser Session

Learn how to launch a Chrome browser with nodriver, open a web page,
and close the browser cleanly.
"""
import asyncio

from common.browser import launch_browser, close_browser


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://example.com")
        title = await page.evaluate("document.title")
        print(f"Page title: {title}")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
