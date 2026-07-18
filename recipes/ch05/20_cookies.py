"""
Recipe 20 (revised): Work with Cookies

Read, save, and restore browser cookies. Understand cookie scope —
cookies belong to a specific domain, path, and protocol.

Cookie Properties:
  Domain    — Which host(s) receive the cookie
  Path      — Limits cookie to a URL path prefix
  Expiry    — When the cookie becomes invalid
  Secure    — Sent only over HTTPS
  HttpOnly  — Not readable by JavaScript (still sent with requests)

Rule: Treat cookies as session state. Reuse them only within
the scope for which they were created.
"""
import asyncio
import json
from pathlib import Path

from common.browser import launch_browser, close_browser

COOKIE_FILE = Path("cookies/session.json")


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://example.com")

        # Save cookies
        cookies = browser.cookies
        COOKIE_FILE.parent.mkdir(parents=True, exist_ok=True)
        COOKIE_FILE.write_text(json.dumps(cookies, indent=2))
        print(f"Cookies saved ({len(cookies)} items)")

        # Restore pattern:
        # with open(COOKIE_FILE) as f:
        #     saved = json.load(f)
        # Use the appropriate cookie API from your pinned nodriver version
        # to restore the saved cookies into the current browser context.

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
