"""
Recipe 8: Inspect Browser State

Read information about the current page and browser session
to verify automation is behaving as expected.
"""
import asyncio

from common.browser import launch_browser, close_browser


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://example.com")

        print(f"Title:      {await page.evaluate('document.title')}")
        print(f"URL:        {await page.evaluate('location.href')}")
        print(f"ReadyState: {await page.evaluate('document.readyState')}")
        print(f"Cookies:    {await page.evaluate('document.cookie')}")
        link_count = await page.evaluate('document.querySelectorAll("a").length')
        print(f"Links:      {link_count}")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
