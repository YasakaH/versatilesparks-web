"""
Recipe 34 (V2): Measure Browser Performance

Problem: Slow automation is hard to diagnose. Measure navigation
timing, DOM size, and Core Web Vitals via CDP.
"""
import asyncio
import nodriver as uc


async def main():
    browser = await uc.start()
    page = await browser.get("https://httpbin.org/delay/1")

    cdp = page._connection
    await cdp.send(uc.cdp.performance.enable())

    metrics = await cdp.send(uc.cdp.performance.get_metrics())
    print("CDP Metrics:")
    for m in metrics.metrics[:8]:
        print(f"  {m.name}: {m.value:.2f}")

    timing = await page.evaluate("() => {"
        "const p = performance.timing;"
        "return {"
        "ttfb: p.responseStart - p.requestStart,"
        "domReady: p.domContentLoadedEventEnd - p.navigationStart,"
        "fullLoad: p.loadEventEnd - p.navigationStart"
        "};"
    "}")
    print(f"\nTTFB: {timing['ttfb']}ms")
    print(f"DOM Ready: {timing['domReady']}ms")
    print(f"Full Load: {timing['fullLoad']}ms")
    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
