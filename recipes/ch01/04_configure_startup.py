"""
Recipe 4: Customize Browser Startup Options

Configure how Chrome starts by changing headless mode, language,
window size, and other launch options.
"""
import asyncio

from common.browser import launch_browser, close_browser


async def main():
    browser = await launch_browser(
        headless=True,
    )

    try:
        page = await browser.get("https://example.com")
        print(await page.evaluate("document.title"))

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
