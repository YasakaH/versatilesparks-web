"""
Recipe 40 (V2): Debug Automation Compatibility Issues

Chapter 10 — Browser Fingerprints, Reliability & Compatibility

Problem: "The site works manually but not automatically."
Systematic debugging checklist for environment mismatches.

Prerequisites:
  Recipe 36: Browser environment audit
  Recipe 10: Retry system
"""
import asyncio
import nodriver as uc


async def diagnose(page):
    """Run a battery of checks to identify automation blocking."""
    results = {}

    results["url"] = page.url
    results["js_enabled"] = await page.evaluate("navigator.cookieEnabled")
    results["webdriver"] = await page.evaluate("navigator.webdriver")
    results["chrome"] = await page.evaluate("!!window.chrome")
    results["permissions"] = await page.evaluate("() => {"
        "return navigator.permissions ? 'api exists' : 'no permissions api';"
    "}")

    # Check for common blocking elements
    captcha = await page.find("[id*='captcha'], [class*='captcha']", timeout=2)
    results["captcha_detected"] = captcha is not None

    challenge = await page.find("[id*='challenge'], iframe[src*='challenge']", timeout=2)
    results["challenge_detected"] = challenge is not None

    print("=== Compatibility Diagnostics ===")
    for k, v in results.items():
        status = "PASS" if v in (True, False, None, "api exists") else f"WARN: {v}"
        print(f"  {k}: {v}")


async def main():
    browser = await uc.start()
    page = await browser.get("https://example.com")
    await diagnose(page)
    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
