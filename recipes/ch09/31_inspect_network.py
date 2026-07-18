"""
Recipe 31 (V2): Intercept and Analyze Network Traffic with CDP

Chapter 9 — Advanced Browser Engineering

Problem: Modern web applications rarely contain all their data
in the initial HTML. Learn to observe, analyze, and control
network requests via CDP.

Prerequisites:
  Recipe 1: Browser lifecycle
  Recipe 5: Page navigation
"""
import asyncio
import nodriver as uc


async def on_request(event):
    url = event.request.url[:150]
    method = event.request.method
    print(f"{method}: {url}")


async def main():
    browser = await uc.start()
    page = await browser.get("https://example.com")
    # Register CDP handler for all outgoing requests
    page.add_handler(uc.cdp.network.RequestWillBeSent, on_request)
    await page.get("https://httpbin.org/get")
    await page.sleep(3)
    print("Network inspection active")
    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
