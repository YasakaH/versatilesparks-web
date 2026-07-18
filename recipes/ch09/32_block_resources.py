"""
Recipe 32 (V2): Block Unnecessary Resources for Performance

Chapter 9 — Advanced Browser Engineering

Problem: Pages load images, ads, analytics, and videos that
slow down automation. Block selectively without breaking layout.

Prerequisites:
  Recipe 31: Network traffic inspection
"""
import asyncio
import nodriver as uc

BLOCKED_PATTERNS = [".png", ".jpg", ".gif", "analytics", "tracking", "facebook"]


async def on_request(event):
    url = event.request.url
    if any(p in url for p in BLOCKED_PATTERNS):
        print(f"Blocked: {url[:100]}")
        return {"cancel": True}
    return {"cancel": False}


async def main():
    browser = await uc.start()
    page = await browser.get("https://example.com")
    page.add_handler(uc.cdp.network.RequestWillBeSent, on_request)
    await page.get("https://httpbin.org/image/png")
    await page.sleep(2)
    print("Resource blocking active")
    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
