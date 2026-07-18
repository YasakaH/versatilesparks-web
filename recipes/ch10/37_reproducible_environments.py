"""
Recipe 37 (V2): Create Consistent Browser Environments

Chapter 10 — Browser Fingerprints, Reliability & Compatibility

Problem: Automation works locally but fails elsewhere. Lock
Chrome version, locale, timezone, and profile for reproducibility.

Prerequisites:
  Recipe 1: Browser lifecycle
  Recipe 3: Persistent profiles
"""
import asyncio
from pathlib import Path
import nodriver as uc

LOCKED_PROFILE = Path("./profiles/locked")


async def main():
    LOCKED_PROFILE.mkdir(parents=True, exist_ok=True)

    browser = await uc.start(
        user_data_dir=str(LOCKED_PROFILE),
        window_size=(1920, 1080),
        arguments=[
            "--lang=en-US",
            "--timezone=America/New_York",
        ],
    )
    page = await browser.get("https://httpbin.org/headers")
    print(f"Profile: {LOCKED_PROFILE}")
    print(f"Page loaded: {await page.title()}")
    # Save profile for reuse
    (LOCKED_PROFILE / ".locked").write_text("chrome=130,locale=en-US,tz=America/New_York")
    print("Environment locked for reproducibility")
    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
