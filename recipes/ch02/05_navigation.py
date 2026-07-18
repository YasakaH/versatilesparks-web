"""
Recipe 5: Navigate Like a User

Control browser navigation by moving backward, forward, refreshing
pages, and waiting for navigation to complete.
"""
import asyncio

from common.browser import launch_browser, close_browser


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://example.com")
        print("1:", await page.evaluate("location.href"))

        # Navigate to a new page
        await page.get("https://httpbin.org")
        print("2:", await page.evaluate("location.href"))

        # Go back
        await page.back()
        print("3:", await page.evaluate("location.href"))

        # Go forward
        await page.forward()
        print("4:", await page.evaluate("location.href"))

        # Reload
        await page.reload()
        print("5:", await page.evaluate("location.href"))

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
