"""
Recipe 22: Manage Multiple Accounts

Use separate browser profiles for different user accounts.
"""
import asyncio
from pathlib import Path

import nodriver as uc

from common.browser import close_browser

ACCOUNTS = {
    "alice": Path("profiles/alice"),
    "bob": Path("profiles/bob"),
}


async def run_session(name: str):
    """Run a browser session for a specific account."""
    profile = ACCOUNTS[name]
    profile.mkdir(parents=True, exist_ok=True)

    browser = await uc.start(user_data_dir=profile)
    try:
        page = await browser.get("https://example.com")
        print(f"[{name}] Profile: {profile.resolve()}")
        print(f"[{name}] Title:   {await page.evaluate('document.title')}")
    finally:
        await close_browser(browser)


async def main():
    for account in ACCOUNTS:
        await run_session(account)
        print()


if __name__ == "__main__":
    asyncio.run(main())
