"""
Recipe 36 (V2): Audit Your Browser Environment

Chapter 10 — Browser Fingerprints, Reliability & Compatibility

Problem: "My automation works manually but fails when automated.
What does the website see differently?"

Collect every browser signal a website can observe, so you can
identify environment inconsistencies before they cause failures.

Prerequisites:
  Recipe 1: Browser lifecycle
  Recipe 5: Page navigation
"""
import asyncio, json
import nodriver as uc


async def main():
    browser = await uc.start()
    page = await browser.get("https://example.com")

    fp = await page.evaluate("() => ({"
        "ua: navigator.userAgent,"
        "platform: navigator.platform,"
        "langs: navigator.languages,"
        "cpus: navigator.hardwareConcurrency,"
        "memory: navigator.deviceMemory || 'unknown',"
        "screen: screen.width+'x'+screen.height+'x'+screen.colorDepth,"
        "tz: Intl.DateTimeFormat().resolvedOptions().timeZone,"
        "plugins: Array.from(navigator.plugins||[]).map(p=>p.name).join(',')"
    "})")
    print(json.dumps(fp, indent=2))
    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
