"""
Recipe 26 (revised): Download Files Reliably

Chrome download lifecycle: click → temp download → growing file → rename → done.
A file existing on disk does NOT mean the download is complete.
"""
import asyncio
from pathlib import Path

from common.browser import launch_browser, close_browser
from common.config import DOWNLOAD_DIR


async def download_finished(path: Path, stable_seconds: float = 2.0) -> bool:
    """Check if a download has finished by monitoring file size."""
    if not path.exists():
        return False
    size = path.stat().st_size
    await asyncio.sleep(stable_seconds)
    return path.exists() and path.stat().st_size == size


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://example.com")

        links = await page.find_all("a")
        download_links = []
        for link in links:
            href = link.attrs.get("href", "")
            if any(ext in href for ext in [".pdf", ".csv", ".zip"]):
                download_links.append((link.text.strip(), href))

        if not download_links:
            print("No download links found on this page.")
            return

        for name, url in download_links:
            print(f"Download: {name} → {url}")

        # In production: configure Chrome's download directory,
        # click download link, poll using download_finished().

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
