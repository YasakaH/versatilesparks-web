"""
Recipe 27: Extract Images and Media

Collect image URLs and other media assets from a page.
"""
import asyncio
from urllib.parse import urljoin

from common.browser import launch_browser, close_browser


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://example.com")

        images = await page.find_all("img")
        base_url = await page.evaluate("location.href")

        for img in images:
            src = img.attrs.get("src", "")
            alt = img.attrs.get("alt", "(no alt text)")

            if not src:
                continue

            # Handle lazy-loaded images
            if not src or src.startswith("data:"):
                src = img.attrs.get("data-src", src)

            full_url = urljoin(base_url, src)
            print(f"[{alt}] {full_url}")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
