"""
Recipe 6: Capture Screenshots

Save browser screenshots for debugging, documentation,
and automation reports.
"""
import asyncio
from pathlib import Path

from common.browser import launch_browser, close_browser
from common.config import DOWNLOAD_DIR


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://example.com")
        path = DOWNLOAD_DIR / "screenshot_example.png"
        path.parent.mkdir(parents=True, exist_ok=True)

        await page.save_screenshot(path)
        print(f"Screenshot saved: {path.resolve()}")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
