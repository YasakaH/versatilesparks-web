"""
Recipe 39 (V2): Environment Snapshot

Record the complete browser environment — Chrome version, OS,
timezone, locale, viewport — so you can compare environments
when automation behaves differently across machines.
"""
import asyncio, json, platform, sys
from datetime import datetime
import nodriver as uc


async def take_snapshot():
    browser = await uc.start()
    page = await browser.get("about:blank")
    env = await page.evaluate("""() => ({
        userAgent: navigator.userAgent,
        language: navigator.language,
        platform: navigator.platform,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        screen: { width: screen.width, height: screen.height }
    })""")
    await browser.stop()
    snapshot = {
        "timestamp": datetime.utcnow().isoformat(),
        "python": sys.version.split()[0],
        "os": platform.system(),
        "browser": env,
    }
    return snapshot


async def main():
    snap = await take_snapshot()
    print(json.dumps(snap, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
