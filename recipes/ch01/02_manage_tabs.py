"""
Recipe 2: Open and Manage Browser Tabs

Open multiple tabs, switch between them, and close them cleanly.
"""
import asyncio

from common.browser import launch_browser, close_browser


async def main():
    browser = await launch_browser()

    try:
        first = await browser.get("https://example.com")
        second = await browser.get("https://httpbin.org")

        print(f"First tab:  {await first.evaluate('document.title')}")
        print(f"Second tab: {await second.evaluate('document.title')}")

        # Switch back to the first tab
        await first.activate()
        print("Returned to first tab.")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
