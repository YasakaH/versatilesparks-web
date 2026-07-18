"""
Recipe 43 (V2): Automate Shadow DOM Components

Problem: Web components encapsulate their DOM in shadow roots.
Standard selectors cannot reach inside — access via JS.
"""
import asyncio
import nodriver as uc


async def main():
    browser = await uc.start()
    page = await browser.get("https://example.com")

    # Check for shadow DOM
    has_shadow = await page.evaluate("() => {"
        "return !!document.querySelector('*').shadowRoot;"
    "}")
    print(f"Shadow DOM detected on page: {has_shadow}")

    # Access shadow DOM content via JS evaluate
    shadow_text = await page.evaluate("() => {"
        "const hosts = document.querySelectorAll('*');"
        "for (const h of hosts) {"
        "  if (h.shadowRoot) {"
        "    return h.shadowRoot.textContent.trim().slice(0, 100);"
        "  }"
        "}"
        "return 'no shadow DOM found';"
    "}")
    print(f"Shadow content: {shadow_text}")

    # If you know the host element, access directly
    await browser.stop()


if __name__ == "__main__":
    asyncio.run(main())
