"""
Recipe 13 (revised): Find Elements Using Stable Selectors

Choose selectors that remain reliable as websites evolve,
reducing maintenance and flaky automation.

Selector Priority
⭐⭐⭐⭐⭐ data-testid  — Best: purpose-built automation attribute
⭐⭐⭐⭐    id           — Very good: unique and stable
⭐⭐⭐     name         — Good: forms and inputs
⭐⭐       stable class — Fair: semantic classes unlikely to change
⭐        CSS hierarchy — Fragile: depends on page structure
🚫       XPath position — Very fragile: last resort only

Rule: Prefer selectors that describe the element's purpose,
not its position in the page.
"""
import asyncio

from common.browser import launch_browser, close_browser


async def main():
    browser = await launch_browser()

    try:
        page = await browser.get("https://example.com")

        # Best: stable CSS selector
        heading = await page.find("h1")
        print(f"Heading: {heading.text}")

        # ❌ Brittle: auto-generated class
        # await page.find(".css-18d91ab")  # May change between builds

        # ❌ Brittle: deep hierarchy
        # await page.find("body > div > main > section > div > ul > li:nth-child(4)")

        # ✅ Better: semantic selector
        link = await page.find("a")
        print(f"Link: {link.text} → {link.attrs.get('href', 'N/A')}")

    finally:
        await close_browser(browser)


if __name__ == "__main__":
    asyncio.run(main())
