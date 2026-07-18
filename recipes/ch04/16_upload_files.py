"""
Recipe 16: Upload Files

Upload files through browser file input elements.
"""
import asyncio
from pathlib import Path

from common.browser import launch_browser, close_browser


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://httpbin.org/forms/post")

        upload = await page.find("input[type='file']")

        # Create a test file to upload
        test_file = Path("test_upload.txt")
        test_file.write_text("Hello from nodriver cookbook!")

        await upload.send_file(str(test_file.resolve()))
        print(f"Uploaded: {test_file.resolve()}")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
